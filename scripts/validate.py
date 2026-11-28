#!/usr/bin/env python3
"""
Validate this repository's four kinds of file, and then the joins between them.

Run from repo root:
    python scripts/validate.py
    python scripts/validate.py --strict     # the join fails instead of warning

    pass 1  data/**/*.yaml      dataset entries, against schema/dataset.schema.json
    pass 2  reviews/**/*.yaml   source reviews, against schema/review.schema.json
    pass 3  cells/*.yaml        Index cells,    against schema/cell.schema.json
    pass 4  readings.yaml       the fourteen readings asked of a city, against schema/reading.schema.json
    pass 5  observations/**     the figures a place sent for a reading, against schema/observation.schema.json
    pass 6  systems/energy/*    the power systems places sit on, against schema/system.schema.json
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
import re
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
READING_SCHEMA_PATH = ROOT / "schema" / "reading.schema.json"
OBSERVATION_SCHEMA_PATH = ROOT / "schema" / "observation.schema.json"
SYSTEM_SCHEMA_PATH = ROOT / "schema" / "system.schema.json"
SYSTEMS_DIR = ROOT / "systems"
PROFILE_SCHEMA_PATH = ROOT / "schema" / "profile.schema.json"
PROFILES_DIR = ROOT / "profiles"
READINGS_PATH = ROOT / "readings.yaml"
FICTIONAL_PATH = ROOT / "fictional.yaml"
OBSERVATIONS_DIR = ROOT / "observations"
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


PLACES_PATH = ROOT / "places.yaml"
# No places.yaml means no known places: an entry without `places` still passes, one naming a place fails.
_PLACES = ((yaml.safe_load(PLACES_PATH.read_text(encoding="utf-8")) or {}).get("places", [])
           if PLACES_PATH.is_file() else [])
KNOWN_PLACES = {p["slug"] for p in _PLACES}
PLACES_ISO3 = {p["slug"]: p.get("iso3") for p in _PLACES}


# Invented places (fictional.yaml). They are never real places: no source may name one.
FICTIONAL = ({p["slug"] for p in (yaml.safe_load(FICTIONAL_PATH.read_text(encoding="utf-8")) or {}).get("places", [])}
             if FICTIONAL_PATH.is_file() else set())


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

        # `places` must name places the Index tracks (places.yaml), or the site counts nothing for them.
        for p in entry.get("places") or []:
            if p in FICTIONAL:
                print(f"[FAIL] {rel}: {p} is fictional and cannot be a source's place")
                failures += 1
        unknown = [p for p in entry.get("places") or [] if p not in KNOWN_PLACES and p not in FICTIONAL]
        if unknown:
            print(f"[FAIL] {rel}: places {unknown} are not in places.yaml")
            failures += 1
            continue

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


READINGS_ASKED = 14


def pass_readings() -> tuple[int, dict[str, dict]]:
    """Pass 4: readings.yaml. Returns (failures, {reading id: reading}).

    The request a city answers is fourteen readings, R1 to R14, and a figure is filed against one
    by id, so an id that repeats sends two cities' answers to one place. Every `cells` value has to
    name a file in cells/ (pass 3 holds filename and key together, so the filenames are the keys).
    The readings are part of the registry, so a missing readings.yaml is a failure."""
    if not READINGS_PATH.is_file():
        print(f"[FAIL] {READINGS_PATH.name}: not found, and the registry needs its {READINGS_ASKED} readings")
        return 1, {}
    rel = READINGS_PATH.relative_to(ROOT)
    doc, why = _read(READINGS_PATH, rel)
    if why or not isinstance(doc.get("readings"), list):
        print(f"[FAIL] {rel}: {why or 'needs a `readings:` list'}")
        return 1, {}

    validator = _validator(READING_SCHEMA_PATH)
    known_cells = {"|".join(w.capitalize() for w in p.stem.split("-")) for p in CELLS_DIR.glob("*.yaml")}
    failures, readings, seen = 0, {}, set()
    for i, reading in enumerate(doc["readings"]):
        if not isinstance(reading, dict):
            print(f"[FAIL] {rel} :: readings.{i} — must be a mapping")
            failures += 1
            continue
        if _schema_errors(validator, reading, f"{rel} :: readings.{i}"):
            failures += 1
            continue
        rid = reading["id"]
        if rid in seen:
            print(f"[FAIL] {rel}: duplicate reading {rid}")
            failures += 1
            continue
        seen.add(rid)
        unknown = [c for c in reading["cells"] if c not in known_cells]
        if unknown:
            print(f"[FAIL] {rel}: {rid} names cells {unknown}, and cells/ has no such cell")
            failures += 1
            continue
        readings[rid] = reading
        print(f"[ ok ] {rel} :: {rid} — {reading['tests']}, {', '.join(reading['cells'])}")

    if len(doc["readings"]) != READINGS_ASKED:
        print(f"[FAIL] {rel}: has {len(doc['readings'])} readings, and the Index asks for {READINGS_ASKED}")
        failures += 1
    print(f"\n{len(readings)} of {READINGS_ASKED} readings checked.")
    return failures, readings


def pass_observations(readings: dict[str, dict]) -> int:
    """Pass 5: observations/{place}/{reading}.yaml, the figures a place has sent for one reading.
    The place must be in places.yaml or fictional.yaml, `fictional: true` must be there exactly
    when it is in fictional.yaml, the reading must be in readings.yaml, and the path must say the
    same place and reading the file does. Returns the number of failing files."""
    validator = _validator(OBSERVATION_SCHEMA_PATH)
    failures = n = 0
    for path in sorted(OBSERVATIONS_DIR.rglob("*.yaml")):
        rel = path.relative_to(ROOT)
        n += 1
        doc, why = _read(path, rel)
        if why:
            print(f"[FAIL] {rel}: {why}")
            failures += 1
            continue
        if _schema_errors(validator, doc, rel):
            failures += 1
            continue
        place, reading = doc["place"], doc["reading"]
        problems = []
        if place not in KNOWN_PLACES and place not in FICTIONAL:
            problems.append(f"unknown place {place}: it is in neither places.yaml nor fictional.yaml")
        elif (place in FICTIONAL) != (doc.get("fictional") is True):
            problems.append(f"{place} {'is' if place in FICTIONAL else 'is not'} in fictional.yaml, "
                            f"so `fictional` must be {'true' if place in FICTIONAL else 'absent or false'}")
        if reading not in readings:
            problems.append(f"reading {reading} is not in readings.yaml")
        if path.relative_to(OBSERVATIONS_DIR).as_posix() != f"{place}/{reading}.yaml":
            problems.append(f"path must be observations/{place}/{reading}.yaml")
        for m in problems:
            print(f"[FAIL] {rel}: {m}")
        if problems:
            failures += 1
        else:
            print(f"[ ok ] {rel} :: {len(doc['figures'])} figure(s)")
    print(f"\n{n - failures} of {n} observation files checked.")
    return failures


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


def reading_tags(entries: dict, readings: dict[str, dict]) -> int:
    """A `reading-r<n>` tag says the source holds that reading's figure for its places, and the city
    page shows the source under that reading only. The tag has to name a reading in readings.yaml."""
    failures = 0
    for rid, e in sorted(entries.items()):
        bad = [t for t in e.get("tags") or [] if t.startswith("reading-") and t[len("reading-"):].upper() not in readings]
        if bad:
            failures += 1
            print(f"  FAIL  data/{rid}.yaml: {', '.join(bad)} names no reading in readings.yaml")
    if not failures:
        print("  ok    every reading tag names a reading")
    return failures


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


def pass_places() -> int:
    """Every place carries `iso3` (three capitals), and one country has one code."""
    failures, by_country = 0, {}
    for p in _PLACES:
        iso3 = p.get("iso3")
        if not isinstance(iso3, str) or not re.fullmatch(r"[A-Z]{3}", iso3):
            print(f"  [FAIL] places.yaml: {p['slug']} `iso3` must be three capital letters, got {iso3!r}")
            failures += 1
        elif by_country.setdefault(p["country"], (iso3, p["slug"]))[0] != iso3:
            first = by_country[p["country"]]
            print(f"  [FAIL] places.yaml: {p['slug']} `iso3` {iso3} differs from {first[0]} on {first[1]}, same country")
            failures += 1
    print(f"\n{len(_PLACES)} places checked.")
    return failures


def _open_rings(polygon, rings: dict) -> list[str]:
    """Problems for each ring (the polygon, and the named rings) whose first point differs from its last."""
    named = [("polygon", polygon)] if polygon else []
    named += [(f"rings.{k}", v) for k, v in rings.items()]
    return [f"{name} is not closed (first point differs from last)" for name, pts in named if pts[0] != pts[-1]]


def pass_systems(entry_ids: set[str], readings: dict) -> tuple[int, dict[str, dict]]:
    """Pass 6: systems/energy/<id>.yaml, the power systems places sit on. Returns (failures, {id: system}).

    Beyond the schema: the file is named for its id; a national system has `country` (one a place in
    places.yaml carries) and no polygon, any other has a polygon; every polygon and ring is closed; an
    estimated mix has capacity_factors; every `sources` id is an entry and every `readings` id a reading."""
    validator = _validator(SYSTEM_SCHEMA_PATH)
    failures, systems = 0, {}
    for path in sorted(SYSTEMS_DIR.glob("energy/*.yaml")):
        rel = path.relative_to(ROOT)
        doc, why = _read(path, rel)
        if why:
            print(f"[FAIL] {rel}: {why}")
            failures += 1
            continue
        if _schema_errors(validator, doc, rel):
            failures += 1
            continue
        problems = []
        if doc["id"] != path.stem:
            problems.append(f"id {doc['id']!r} is not the file name {path.stem!r}")
        kind = doc["mix"]["kind"]
        if kind == "national":
            if "country" not in doc:
                problems.append("a national system needs `country`")
            elif doc["country"] not in set(PLACES_ISO3.values()):
                problems.append(f"country {doc['country']} is no place's iso3 in places.yaml")
            if "polygon" in doc:
                problems.append("a national system has no polygon")
        elif "polygon" not in doc:
            problems.append("needs a `polygon`")
        if kind == "estimated" and "capacity_factors" not in doc:
            problems.append("an estimated mix needs `capacity_factors`")
        problems += _open_rings(doc.get("polygon"), doc.get("rings", {}))
        problems += [f"source {s} is not an entry in data/" for s in doc.get("sources", []) if s not in entry_ids]
        problems += [f"reading {r} is not in readings.yaml" for r in doc["readings"] if r not in readings]
        for pr in problems:
            print(f"[FAIL] {rel}: {pr}")
        if problems:
            failures += 1
            continue
        systems[doc["id"]] = doc
        print(f"[ ok ] {rel} :: {kind}, {', '.join(doc['readings'])}")
    print(f"\n{len(systems)} systems checked.")
    return failures, systems


def pass_profiles(systems: dict, entry_ids: set[str], readings: dict) -> tuple[int, dict[str, dict]]:
    """Pass 7: profiles/<place>.yaml, what a place knows about itself. Returns (failures, {place: profile}).

    Beyond the schema: the file is named for its place; the place is a real one in places.yaml (a fictional
    place has no profile); `energy.system` is a hand-written system, not a national one; rings are closed;
    utility ids are unique in the profile; every `sources` id is an entry and every `readings` id a reading."""
    validator = _validator(PROFILE_SCHEMA_PATH)
    failures, profiles = 0, {}
    for path in sorted(PROFILES_DIR.glob("*.yaml")):
        rel = path.relative_to(ROOT)
        doc, why = _read(path, rel)
        if why:
            print(f"[FAIL] {rel}: {why}")
            failures += 1
            continue
        if _schema_errors(validator, doc, rel):
            failures += 1
            continue
        problems = []
        if doc["place"] != path.stem:
            problems.append(f"place {doc['place']!r} is not the file name {path.stem!r}")
        if doc["place"] in FICTIONAL:
            problems.append(f"{doc['place']} is in fictional.yaml; profiles are for real places")
        elif doc["place"] not in KNOWN_PLACES:
            problems.append(f"place {doc['place']} is not in places.yaml")
        energy = doc.get("energy")
        if energy:
            system = systems.get(energy["system"])
            if system is None:
                problems.append(f"energy.system {energy['system']!r} is not a system in systems/energy/")
            elif system["mix"]["kind"] == "national":
                problems.append(f"energy.system {energy['system']!r} is a national system; "
                                f"a place with none of its own leaves `energy` out and falls to its country's")
            problems += _open_rings(None, energy.get("rings", {}))
        utilities = (doc.get("water") or {}).get("utilities", [])
        ids = [u["id"] for u in utilities]
        problems += [f"utility id {i} repeats" for i in sorted({i for i in ids if ids.count(i) > 1})]
        for u in utilities:
            problems += [f"{u['id']}: source {s} is not an entry in data/" for s in u.get("sources", []) if s not in entry_ids]
            problems += [f"{u['id']}: reading {r} is not in readings.yaml" for r in u["readings"] if r not in readings]
        for pr in problems:
            print(f"[FAIL] {rel}: {pr}")
        if problems:
            failures += 1
            continue
        profiles[doc["place"]] = doc
        print(f"[ ok ] {rel} :: {'energy' if energy else ''}{' + ' if energy and utilities else ''}"
              f"{str(len(utilities)) + ' utilities' if utilities else ''}")
    print(f"\n{len(profiles)} profiles checked.")
    return failures, profiles


def main(argv: list[str]) -> int:
    strict = "--strict" in argv

    print("== places.yaml: the places the Index tracks")
    failures = pass_places()

    print("\n== pass 1: data/ — dataset entries")
    f1, entries = pass_entries()
    failures += f1

    print("\n== pass 2: reviews/ — who read what, for where")
    f2, reviews = pass_reviews(set(entries))
    failures += f2

    print("\n== pass 3: cells/ — what the Index claims, and what it does not")
    f3, cells = pass_cells()
    failures += f3

    print("\n== pass 4: readings.yaml — what the Index asks of a city")
    f4, readings = pass_readings()
    failures += f4

    print("\n== pass 5: observations/ — what places have sent")
    failures += pass_observations(readings)

    print("\n== pass 6: systems/ — the power systems places sit on")
    f6, systems = pass_systems(set(entries), readings)
    failures += f6

    print("\n== pass 7: profiles/ — what a place knows about itself")
    f7, profiles = pass_profiles(systems, set(entries), readings)
    failures += f7

    print("\n== join: reading tags name readings")
    failures += reading_tags(entries, readings)

    print("\n== join: does `live` mean anything on each entry that claims it")
    failures += join(entries, reviews, strict)

    print("\n== join: does the cell map close")
    failures += cell_join(entries, cells, strict)

    if failures:
        print(f"\n{failures} file(s) failed validation.", file=sys.stderr)
        return 1
    print(f"\n{len(entries)} entries, {sum(len(v) for v in reviews.values())} reviews, "
          f"{len(sorted(CELLS_DIR.glob('*.yaml')))} cells, {len(readings)} readings, {len(systems)} systems, {len(profiles)} profiles: all passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
