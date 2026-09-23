#!/usr/bin/env python3
"""
Validate this repository's three kinds of file, and then the one join between them.

Run from repo root:
    python scripts/validate.py
    python scripts/validate.py --strict     # the join fails instead of warning

    pass 1  data/**/*.yaml      dataset entries, against schema/dataset.schema.json
    pass 2  reviews/**/*.yaml   source reviews, against schema/review.schema.json
    pass 3  cells/*.yaml        Index cells,    against schema/cell.schema.json
    join    every `status: live` entry must carry a usable review or an `adapter`

The join is the point of the whole thing, and today it is a warning. 189 of the 203 live entries
name no adapter and no reviewer — that is the debt criterion 3 of CONTRIBUTING was hiding, and
printing it is what makes it payable. It does not fail CI, because a gate that turns 189 files red
on the day it lands gets deleted rather than paid. `--strict` is the same check as a failure, for
the day the network decides to flip it.

Exits 0 on success, 1 on validation failure. CI uses this exit code.

Dependencies (install once):
    pip install pyyaml jsonschema
"""

import datetime as _dt
import json
import sys
from pathlib import Path

try:
    import yaml
    import jsonschema
    # jsonschema 4.x carries Draft202012Validator; older versions fall back
    # to Draft7Validator (compatible enough for our schema).
    Validator = (
        getattr(jsonschema, "Draft202012Validator", None)
        or jsonschema.Draft7Validator
    )
except ImportError:
    sys.stderr.write(
        "Missing dependencies. Install with: pip install 'pyyaml' 'jsonschema>=4'\n"
    )
    sys.exit(2)


ROOT = Path(__file__).resolve().parent.parent
SCHEMA_PATH = ROOT / "schema" / "dataset.schema.json"
REVIEW_SCHEMA_PATH = ROOT / "schema" / "review.schema.json"
CELL_SCHEMA_PATH = ROOT / "schema" / "cell.schema.json"
DATA_DIR = ROOT / "data"
REVIEWS_DIR = ROOT / "reviews"
CELLS_DIR = ROOT / "cells"

USABLE = ("usable", "usable-with-caveats")

PILLARS = ["Environmental", "Social", "Economic", "Governance"]
SCALES = ["Planet", "Bioregion", "Region", "City", "Community"]


def _coerce_dates(obj):
    """PyYAML parses bare ISO dates (2026-05-04) as datetime.date objects.
    The schema expects ISO strings (date-formatted). Convert recursively."""
    if isinstance(obj, _dt.date) and not isinstance(obj, _dt.datetime):
        return obj.isoformat()
    if isinstance(obj, _dt.datetime):
        return obj.isoformat()
    if isinstance(obj, dict):
        return {k: _coerce_dates(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_coerce_dates(v) for v in obj]
    return obj


def _message(err) -> str:
    """jsonschema renders a failed `not` by printing the whole instance back at you. The only `not` in
    this schema is act_kind-without-act, so say that instead of dumping 2 kB of YAML into CI's log."""
    if err.validator == "not" and err.validator_value == {"required": ["act_kind"]}:
        return "act_kind is set but role does not contain 'act' — act_kind belongs only to an act source"
    return err.message


def _validator(path: Path):
    return Validator(json.loads(path.read_text(encoding="utf-8")))


def _read(path: Path, rel: Path):
    """Load one YAML mapping. Returns (mapping, None) or (None, printable reason)."""
    try:
        doc = yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as e:
        return None, f"invalid YAML — {e}"
    if not isinstance(doc, dict):
        return None, "top-level must be a mapping (dict)"
    return _coerce_dates(doc), None


def _schema_errors(validator, doc, rel) -> int:
    """Print every schema error for one document. Returns 1 if any, else 0."""
    errors = sorted(validator.iter_errors(doc), key=lambda e: e.path)
    for err in errors:
        loc = ".".join(str(p) for p in err.path) or "<root>"
        print(f"[FAIL] {rel} :: {loc} — {_message(err)}")
    return 1 if errors else 0


def candidate_needs_notes(entry: dict) -> str | None:
    """A `candidate` is a claim that somebody verified the licence and the endpoint and that nobody
    has read it for a real territory. Unqualified, that claim is indistinguishable from a link
    somebody liked, so `notes` carries what was checked and what is still missing. Not expressible
    in the schema: minLength cannot see the value of another key. tests/test_schema.py calls this."""
    if entry.get("status") != "candidate":
        return None
    notes = entry.get("notes")
    if not isinstance(notes, str) or not notes.strip():
        return ("status is candidate and `notes` is empty — say what was verified (licence, "
                "endpoint, which indicator row) and what nobody has done yet")
    return None


def pass_entries() -> tuple[int, dict]:
    """Pass 1: data/**/*.yaml. Returns (failures, {registry id: entry})."""
    validator = _validator(SCHEMA_PATH)
    yaml_files = sorted(DATA_DIR.rglob("*.yaml"))
    if not yaml_files:
        print(f"No YAML files found under {DATA_DIR}", file=sys.stderr)
        return 1, {}

    failures = 0
    warnings = []
    seen_slugs = {}
    entries: dict[str, dict] = {}
    for path in yaml_files:
        rel = path.relative_to(ROOT)
        entry, why = _read(path, rel)
        if why:
            print(f"[FAIL] {rel}: {why}")
            failures += 1
            continue

        # Schema validation
        if _schema_errors(validator, entry, rel):
            failures += 1
            continue

        # Path / pillar / scale consistency
        pillar = entry["pillar"]
        scale = entry["scale"]
        expected_dir = DATA_DIR / pillar / scale
        if path.parent.resolve() != expected_dir.resolve():
            print(
                f"[FAIL] {rel}: pillar/scale ({pillar}/{scale}) does not match "
                f"location ({path.parent.relative_to(DATA_DIR)})"
            )
            failures += 1
            continue

        # Slug uniqueness within pillar
        slug = path.stem
        key = (pillar, slug)
        if key in seen_slugs:
            print(f"[FAIL] {rel}: duplicate slug {slug!r} also in {seen_slugs[key]}")
            failures += 1
            continue
        seen_slugs[key] = rel

        # `candidate` without notes — validator logic, not schema. See candidate_needs_notes().
        why = candidate_needs_notes(entry)
        if why:
            print(f"[FAIL] {rel}: {why}")
            failures += 1
            continue

        entries[path.relative_to(DATA_DIR).with_suffix("").as_posix()] = entry
        print(f"[ ok ] {rel}")

    print(f"\n{len(yaml_files)} entr{'y' if len(yaml_files) == 1 else 'ies'} checked.")
    return failures, entries


def pass_reviews(entry_ids) -> tuple[int, dict]:
    """Pass 2: reviews/**/*.yaml. Returns (failures, {registry id: [review, ...]}).

    Two pointers have to hold: the `entry` key must name a source this list actually carries, and
    the file must live in that source's own directory. Either one alone is forgeable by a typo."""
    validator = _validator(REVIEW_SCHEMA_PATH)
    files = sorted(REVIEWS_DIR.rglob("*.yaml"))
    failures = 0
    reviews: dict[str, list] = {}
    for path in files:
        rel = path.relative_to(ROOT)
        review, why = _read(path, rel)
        if why:
            print(f"[FAIL] {rel}: {why}")
            failures += 1
            continue
        if _schema_errors(validator, review, rel):
            failures += 1
            continue

        rid = review["entry"]
        if rid not in entry_ids:
            print(f"[FAIL] {rel}: entry {rid!r} has no file at data/{rid}.yaml — "
                  f"a review of a source this list does not carry is not a review of anything")
            failures += 1
            continue

        expected_dir = REVIEWS_DIR / rid
        if path.parent.resolve() != expected_dir.resolve():
            print(f"[FAIL] {rel}: lives in {path.parent.relative_to(ROOT).as_posix()}/ but "
                  f"reviews {rid} — move it to reviews/{rid}/")
            failures += 1
            continue

        reviews.setdefault(rid, []).append(review)
        print(f"[ ok ] {rel} — {review['verdict']} for {review['territory']}, {review['by']}")

    print(f"\n{len(files)} review{'' if len(files) == 1 else 's'} checked.")
    return failures, reviews


def pass_cells() -> tuple[int, dict]:
    """Pass 3: cells/*.yaml. Returns (failures, {cell key: cell}). The filename is the cell key,
    lowercased and hyphenated; a cell whose name and key disagree is two cells, and the second one
    is invisible."""
    validator = _validator(CELL_SCHEMA_PATH)
    files = sorted(CELLS_DIR.glob("*.yaml"))
    failures, cells = 0, {}
    for path in files:
        rel = path.relative_to(ROOT)
        cell, why = _read(path, rel)
        if why:
            print(f"[FAIL] {rel}: {why}")
            failures += 1
            continue
        if _schema_errors(validator, cell, rel):
            failures += 1
            continue

        pillar, _, scale = cell["cell"].partition("|")
        expected = f"{pillar.lower()}-{scale.lower()}.yaml"
        if path.name != expected:
            print(f"[FAIL] {rel}: cell is {cell['cell']!r}, so the file must be "
                  f"cells/{expected} — filename and key must agree")
            failures += 1
            continue

        cells[cell["cell"]] = cell
        print(f"[ ok ] {rel} — {len(cell['minimum_indicators'])} minimum indicator(s)")

    print(f"\n{len(files)} cell{'' if len(files) == 1 else 's'} checked "
          f"of the {len(PILLARS) * len(SCALES)} in the matrix.")
    return failures, cells


def cell_join(entries: dict, cells: dict, strict: bool) -> int:
    """Does the map close? `feeds_cells` and `cells/` are two halves of one claim — the entry says
    it can fill a cell, the cell says what filling it means — and nothing has been checking that
    they agree.

    The failure mode here is specific: a mistyped cell key is not a broken reference that blows up,
    it is an entry that looks mapped and feeds nothing, and a cell nothing feeds is a column of the
    Index that cannot be filled. Neither is visible to a schema, because both halves are valid on
    their own. That is exactly the shape of `wired_in_planetai`, and the lesson is the same one:
    check the join, not the two sides.
    """
    fed: dict[str, int] = {}
    dangling = []
    for rid, entry in sorted(entries.items()):
        for c in entry.get("feeds_cells") or []:
            fed[c] = fed.get(c, 0) + 1
            if c not in cells:
                dangling.append((rid, c))

    # A typo, and an invisible one. There are none today, which is the cheapest possible moment to
    # close it: a gate that lands at zero costs nothing and never lets the first one through.
    for rid, c in dangling:
        print(f"[FAIL] data/{rid}.yaml: feeds_cells names {c!r}, and cells/ has no such cell")

    # A cell nothing feeds. NOT a failure: some cells are computed by the core at any scale and
    # carry no registry entry on purpose — their `notes` say so, and that is a real answer.
    empty = sorted(k for k in cells if not fed.get(k))
    if empty:
        print(f"\n[warn] {len(empty)} cell(s) have no source feeding them. Check each one's "
              f"`notes` says why — a cell the core computes needs no entry, a cell nobody can "
              f"fill is a column of the Index that stays blank:")
        for k in empty:
            print(f"       cells/{k.split('|')[0].lower()}-{k.split('|')[1].lower()}.yaml")

    # Observe-side entries feeding nothing. Counted, not failed: a public budget line and a fab lab
    # directory are both legitimately in this list without filling a pillar × scale cell, and
    # forcing a reason onto every one of them would be 80 edits to say "not applicable".
    def observes(e: dict) -> bool:
        # Absent `role` means [observe] — schema 2c. A source that is both still observes, so it
        # belongs on this side of the count; only a pure `[act]` entry does not.
        return "observe" in (e.get("role") or ["observe"])

    unmapped = sorted(rid for rid, e in entries.items()
                      if e["status"] == "live" and observes(e) and not e.get("feeds_cells"))
    observed = sum(1 for e in entries.values() if e["status"] == "live" and observes(e))
    if unmapped:
        print(f"\n[warn] {len(unmapped)} of {observed} live observe-side entries feed no Index "
              f"cell. Not wrong on its own — budget lines and directories belong in this list "
              f"without filling a pillar × scale cell — but it is the number that says how much "
              f"of what is collected the Index can actually read.")

    print(f"\n{len(cells) - len(empty)} of {len(cells)} cells have at least one source; "
          f"{sum(fed.values())} feeds_cells entries across {len(cells)} cells.")

    if dangling and strict:
        print("\n--strict: a feeds_cells value naming no cell is a failure.", file=sys.stderr)
    return len(dangling)


def join(entries: dict, reviews: dict, strict: bool) -> int:
    """The join: `status: live` has to be backed by something. Either a named person read this
    source for a real territory and said it was usable, or code reads it and `adapter` says where.

    Not a failure in this commit. 189 of the 203 live entries have neither, and that is the honest
    state of a list whose criterion 3 asked for use-or-audit and had nowhere to record either. A
    gate that turns 189 files red on the day it lands gets deleted; a counted warning gets paid
    down. `--strict` is the flip, for when the count is small enough to be an error."""
    unbacked = []
    for rid, entry in entries.items():
        if entry["status"] != "live":
            continue
        if entry.get("adapter"):
            continue
        if any(r["verdict"] in USABLE for r in reviews.get(rid, [])):
            continue
        unbacked.append(rid)

    live = sum(1 for e in entries.values() if e["status"] == "live")
    backed = live - len(unbacked)
    print(f"\n{backed} of {live} live entries carry a usable review or an adapter.")

    if not unbacked:
        return 0

    label = "[FAIL]" if strict else "[warn]"
    print(f"\n{label} {len(unbacked)} live entries carry neither a review nor an adapter. "
          f"Each one asserts that somebody in the network uses or has audited this source "
          f"(CONTRIBUTING criterion 3) with nothing in the repository behind the claim. Two ways "
          f"to settle one: open a source-review issue so a named person's reading lands in "
          f"reviews/, or — if nothing has read it for a real territory — set `status: candidate` "
          f"and say so in `notes`.")
    for rid in unbacked:
        print(f"       data/{rid}.yaml")
    if strict:
        print(f"\n--strict: the join is a failure.", file=sys.stderr)
        return len(unbacked)
    return 0


def main(argv: list[str]) -> int:
    strict = "--strict" in argv

    print("== pass 1: data/ — dataset entries")
    failures, entries = pass_entries()

    print("\n== pass 2: reviews/ — who read what, for where")
    f2, reviews = pass_reviews(set(entries))
    failures += f2

    print("\n== pass 3: cells/ — what the Index claims, and what it does not")
    f3, cells = pass_cells()
    failures += f3

    print("\n== join: does `live` mean anything on each entry that claims it")
    failures += join(entries, reviews, strict)

    print("\n== join: does the cell map close")
    failures += cell_join(entries, cells, strict)

    if failures:
        print(f"\n{failures} file(s) failed validation.", file=sys.stderr)
        return 1
    print(f"\n{len(entries)} entries, {sum(len(v) for v in reviews.values())} reviews, "
          f"{len(sorted(CELLS_DIR.glob('*.yaml')))} cells: all passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
