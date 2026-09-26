#!/usr/bin/env python3
"""Turn a `source-review` issue into a review file, and promote a candidate that earned it.

    python scripts/review_from_issue.py --issue 212 --body-file body.md --created 2026-09-22
    python scripts/review_from_issue.py --selftest

Called by .github/workflows/review-to-pr.yml. It exists as a script rather than as a heredoc
inside that workflow for one reason: this is the only code in the repository that WRITES to
data/, and code that writes to data/ should be readable in a diff and runnable on a laptop.

Exit codes, which the workflow branches on:

    0   a review file was written; the JSON on stdout says what happened
    3   the issue names an entry this list does not carry — write nothing, comment on the issue
    4   the issue body is missing a required field, or an answer the schema would refuse — write
        nothing, comment on the issue

**The promotion rule.** A review whose verdict is exactly `usable` promotes its entry from
`candidate` to `live`, and only if the file carries the line `status: candidate` exactly once. The
edit is a one-line text substitution on that one line. It is deliberately not a YAML load-and-dump:
round-tripping an entry through PyYAML reorders keys, drops comments, reflows block scalars and
turns dates into quoted strings — a 60-line diff on a file nobody meant to touch. Every other
byte of the entry is preserved.

`usable-with-caveats` writes the review and does NOT promote. The caveat is the reason: somebody
should read it before the list says `live`. The PR body says so, and the flip is one line away.
"""
from __future__ import annotations

import argparse
import datetime as _dt
import json
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
REVIEWS_DIR = ROOT / "reviews"
TEMPLATE = ROOT / ".github" / "ISSUE_TEMPLATE" / "source-review.yml"
SCHEMA = ROOT / "schema" / "review.schema.json"

ENTRY_RE = re.compile(r"^[a-z]+/[a-z]+/[a-z0-9-]+$")
CANDIDATE_LINE = "status: candidate"
PROMOTED_LINE = "status: live"

# A rendered issue form is `### <label>` followed by the answer. The join between this script and
# the form is therefore the label TEXT, not the field id — so these strings must match
# .github/ISSUE_TEMPLATE/source-review.yml exactly. selftest() asserts that they do, by reading
# the template; a renamed label fails the test rather than silently writing a review with a hole.
FIELDS = {
    "entry": "Entry",
    "by": "Your name",
    "org": "Organisation",
    "date": "Date you read it",
    "territory": "Territory you read it for",
    "checked": "What you checked",
    "verdict": "Verdict",
    "self_declared": "Self-declared",
    "assisted_by": "Assisted by",
    "note": "Notes for the next reader",
}
REQUIRED = ("entry", "by", "org", "territory", "verdict")
NO_RESPONSE = "_no response_"


def parse_body(body: str) -> dict[str, str]:
    """{label: raw answer} from a rendered GitHub issue form."""
    out, label, buf = {}, None, []
    for line in body.replace("\r\n", "\n").split("\n"):
        if line.startswith("### "):
            if label is not None:
                out[label] = "\n".join(buf).strip()
            label, buf = line[4:].strip(), []
        elif label is not None:
            buf.append(line)
    if label is not None:
        out[label] = "\n".join(buf).strip()
    return {k: ("" if v.lower() == NO_RESPONSE else v) for k, v in out.items()}


def checked_boxes(raw: str) -> list[str]:
    """The ticked items of a checkboxes field: `- [x] licence`. Order follows the form, so reviews
    list what was checked in the same order every time."""
    return [m.group(1).strip() for m in re.finditer(r"^\s*- \[[xX]\]\s*(.+)$", raw, re.M)]


def slug(name: str) -> str:
    """'Lars Taylor' -> 'lars-taylor'. Filenames, so: lowercase, ASCII-ish, no surprises."""
    return re.sub(r"-+", "-", re.sub(r"[^a-z0-9]+", "-", name.lower())).strip("-") or "anon"


def iso_date(raw: str, fallback: str) -> str:
    """The reviewer's date if it is a real ISO date, else the day the issue was opened. A typo in a
    date field should not throw away a review; it should quietly become the date we do know."""
    try:
        return _dt.date.fromisoformat(raw.strip()[:10]).isoformat()
    except (ValueError, IndexError):
        return fallback


def free_path(directory: Path, stem: str) -> Path:
    """`{stem}.yaml`, or `{stem}-2.yaml` if that exists, then -3. Two people reviewing the same
    source on the same day is a good day for this list, not a collision to resolve by overwriting
    somebody's reading."""
    path = directory / f"{stem}.yaml"
    n = 2
    while path.exists():
        path = directory / f"{stem}-{n}.yaml"
        n += 1
    return path


def yaml_scalar(value: str) -> str:
    """Quote a one-line string for YAML when it could be read as anything but a string. Written by
    hand rather than with yaml.dump because these files are read by people as often as by code."""
    if value == "" or re.search(r'^[\s>|&*!%@`\'"-]|[:#]\s|[:\s]$', value) or value.lower() in (
        "true", "false", "null", "yes", "no", "on", "off", "~"
    ):
        return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'
    return value


def render_review(r: dict) -> str:
    """The review file. Key order is the schema's required-first order, so every review in the
    repository reads the same way down the page."""
    lines = [
        f"entry: {r['entry']}",
        f"by: {yaml_scalar(r['by'])}",
        f"org: {yaml_scalar(r['org'])}",
        f"date: {r['date']}",
        f"territory: {yaml_scalar(r['territory'])}",
        "checked:",
        *[f"  - {c}" for c in r["checked"]],
        f"verdict: {r['verdict']}",
        f"self_declared: {'true' if r['self_declared'] else 'false'}",
        *([f"assisted_by: {yaml_scalar(r['assisted_by'])}"] if r.get("assisted_by") else []),
        f"issue: {r['issue']}",
    ]
    if r.get("note"):
        lines.append("note: |")
        lines += [f"  {line}".rstrip() for line in r["note"].split("\n")]
    return "\n".join(lines) + "\n"


def promote(path: Path, verdict: str) -> bool:
    """Flip `status: candidate` to `status: live`, by substituting that one line and nothing else.
    Returns whether it happened. Requires the line to appear exactly once: a file with two of them
    is a file somebody should look at, not one a workflow should guess about."""
    if verdict != "usable":
        return False
    lines = path.read_text(encoding="utf-8").splitlines(keepends=True)
    hits = [i for i, line in enumerate(lines) if line.rstrip("\n") == CANDIDATE_LINE]
    if len(hits) != 1:
        return False
    lines[hits[0]] = lines[hits[0]].replace(CANDIDATE_LINE, PROMOTED_LINE)
    path.write_text("".join(lines), encoding="utf-8")
    return True


def schema_breaks(review: dict) -> list[str]:
    """Each answer the schema would refuse that the form cannot stop: a string over its
    `maxLength`, or a value outside an `enum` (an issue body can be edited by hand)."""
    props = json.loads(SCHEMA.read_text(encoding="utf-8"))["properties"]
    broken = []
    for key, rule in props.items():
        value = review.get(key)
        if not isinstance(value, str):
            continue
        label = FIELDS.get(key, key)
        if "maxLength" in rule and len(value) > rule["maxLength"]:
            broken.append(f"**{label}** is {len(value):,} characters and the limit is "
                          f"{rule['maxLength']:,}")
        if "enum" in rule and value not in rule["enum"]:
            broken.append(f"**{label}** is `{value}`, which is not one of "
                          + ", ".join(f"`{v}`" for v in rule["enum"]))
    return broken


def build(body: str, issue: int, created: str) -> tuple[int, dict]:
    answers = parse_body(body)
    get = lambda key: answers.get(FIELDS[key], "").strip()

    review = {
        "entry": get("entry").strip().strip("/"),
        "by": get("by"),
        "org": get("org"),
        "territory": get("territory"),
        "verdict": get("verdict"),
        "checked": checked_boxes(answers.get(FIELDS["checked"], "")),
        "self_declared": bool(checked_boxes(answers.get(FIELDS["self_declared"], ""))),
        "assisted_by": get("assisted_by"),
        "note": get("note"),
        "date": iso_date(get("date"), created),
        "issue": issue,
    }

    missing = [FIELDS[k] for k in REQUIRED if not review[k]]
    if not review["checked"]:
        missing.append(FIELDS["checked"])
    if missing:
        return 4, {"error": "missing", "fields": ", ".join(missing),
                   "message": "This review is missing a required answer: **"
                              + "**, **".join(missing) + "**. Edit the issue body to fill it in, "
                              "then remove and re-add the `source-review` label, or open the review again as a new issue."}
    if not ENTRY_RE.match(review["entry"]):
        return 4, {"error": "entry-malformed", "entry": review["entry"],
                   "message": f"`{review['entry']}` is not a registry id. It must look like "
                              "`{pillar}/{scale}/{slug}` — the entry's path under `data/` with "
                              "the `.yaml` removed, e.g. `environmental/city/openaq`. Edit the "
                              "issue body, then remove and re-add the `source-review` label, or open it again as a new issue."}

    # The schema's own limits, read from the schema so there is one copy of them. Without this a
    # note over maxLength parsed fine, the review file was written, and validate.py then failed the
    # gates step — after the last point where anybody comments on the issue. The reviewer heard
    # nothing. Found on the first real review (a 2,984-character note), before it was filed.
    if broken := schema_breaks(review):
        return 4, {"error": "schema", "fields": ", ".join(broken),
                   "message": "This review does not fit the review schema: " + "; ".join(broken)
                              + ". Edit the issue body, then remove and re-add the "
                              "`source-review` label, or open the review again as a new issue."}

    entry_path = DATA_DIR / f"{review['entry']}.yaml"
    if not entry_path.is_file():
        return 3, {"error": "entry-missing", "entry": review["entry"],
                   "message": f"There is no entry at `data/{review['entry']}.yaml`, so there is "
                              "nothing here to review and nothing has been written. If the source "
                              "belongs in this list, add the entry first (see CONTRIBUTING) — a "
                              "new source starts at `status: candidate`. If the id is just a typo, "
                              "fix the issue body and re-add the `source-review` label, or open it again as a new issue."}

    directory = REVIEWS_DIR / review["entry"]
    directory.mkdir(parents=True, exist_ok=True)
    path = free_path(directory, f"{review['date']}-{slug(review['by'])}")
    path.write_text(render_review(review), encoding="utf-8")

    return 0, {
        "entry": review["entry"],
        "by": review["by"],
        "org": review["org"],
        "verdict": review["verdict"],
        "territory": review["territory"],
        "date": review["date"],
        "review_path": path.relative_to(ROOT).as_posix(),
        "entry_path": entry_path.relative_to(ROOT).as_posix(),
        "promoted": promote(entry_path, review["verdict"]),
        "branch": f"review-{slug(review['entry'])}-{review['date']}-{issue}",
    }


SAMPLE = """### Entry

environmental/city/example-city-air-portal

### Your name

Lars Taylor

### Organisation

Fab City Foundation

### Date you read it

2026-09-18

### Territory you read it for

Barcelona

### What you checked

- [X] licence
- [x] endpoint
- [ ] admin-code
- [x] vintage
- [ ] field-fit

### Verdict

usable

### Self-declared

- [ ] My organisation publishes this source

### Assisted by

Claude Code

### Notes for the next reader

Hourly data is 40 minutes behind wall clock.
Two stations stopped reporting PM2.5 in March.
"""


def selftest() -> int:
    """The parse, the filename, the promotion and the one-line-ness of it, on a temp tree."""
    import shutil
    import tempfile

    bad = 0

    def check(label: str, got, want):
        nonlocal bad
        if got != want:
            bad += 1
            print(f"[FAIL] {label}: got {got!r}, wanted {want!r}")
        else:
            print(f"[ ok ] {label}")

    fields = parse_body(SAMPLE)
    check("parse: every label found", sorted(fields), sorted(FIELDS.values()))
    check("parse: single-line answer", fields["Entry"], "environmental/city/example-city-air-portal")
    check("parse: multi-line answer keeps its newline",
          fields["Notes for the next reader"].count("\n"), 1)
    check("parse: ticked boxes only, upper or lower x",
          checked_boxes(fields["What you checked"]), ["licence", "endpoint", "vintage"])
    check("parse: unticked checkbox is not self-declared",
          bool(checked_boxes(fields["Self-declared"])), False)
    check("parse: _No response_ becomes empty",
          parse_body("### Verdict\n\n_No response_\n")["Verdict"], "")
    check("slug", slug("Lars Taylor"), "lars-taylor")
    check("slug: punctuation and accents-free fallback", slug("J. Vivanco-Álvarez"), "j-vivanco-lvarez")
    check("date: a real one is kept", iso_date("2026-09-18", "2026-09-22"), "2026-09-18")
    check("date: a typo falls back to the issue's day", iso_date("18/09/2026", "2026-09-22"), "2026-09-22")
    check("date: blank falls back too", iso_date("", "2026-09-22"), "2026-09-22")

    # The template's labels are the join between the form and this script. Assert they agree.
    if TEMPLATE.is_file():
        labels = re.findall(r"^\s+label: (.+)$", TEMPLATE.read_text(encoding="utf-8"), re.M)
        labels = [l.strip().strip('"\'') for l in labels]
        missing = [v for v in FIELDS.values() if v not in labels]
        check("template: every label this script looks for exists in the form", missing, [])

    global ROOT, DATA_DIR, REVIEWS_DIR
    real_root = ROOT
    with tempfile.TemporaryDirectory() as td:
        ROOT = Path(td)
        DATA_DIR, REVIEWS_DIR = ROOT / "data", ROOT / "reviews"
        entry_dir = DATA_DIR / "environmental" / "city"
        entry_dir.mkdir(parents=True)
        entry = entry_dir / "example-city-air-portal.yaml"
        original = ("name: Example City Air Portal\n"
                    "url: https://example.org/air\n"
                    "description: A source used only to test the review workflow, twenty characters and more.\n"
                    "pillar: environmental\n"
                    "scale: city\n"
                    "status: candidate\n"
                    "license: CC-BY-4.0\n"
                    "tags: [air-quality]   # a comment that must survive\n"
                    "notes: |\n"
                    "  Licence and endpoint verified. Nobody has read it for a territory.\n")
        entry.write_text(original)

        code, out = build(SAMPLE, 212, "2026-09-22")
        check("build: exit 0", code, 0)
        check("build: review path", out.get("review_path"),
              "reviews/environmental/city/example-city-air-portal/2026-09-18-lars-taylor.yaml")
        check("build: promoted a usable review", out.get("promoted"), True)
        after = entry.read_text()
        check("promote: one line changed, and only that one",
              after, original.replace("status: candidate", "status: live"))
        check("promote: the comment survived", "# a comment that must survive" in after, True)

        written = (ROOT / out["review_path"]).read_text()
        check("write: issue number recorded", "issue: 212" in written, True)
        check("write: checked list in form order",
              "checked:\n  - licence\n  - endpoint\n  - vintage\n" in written, True)
        check("write: note folded as a block scalar", "note: |\n  Hourly data" in written, True)

        # Second review of the same source, same day, same person: -2, nobody overwritten.
        code2, out2 = build(SAMPLE, 213, "2026-09-22")
        check("build: a second identical review gets -2", out2.get("review_path"),
              "reviews/environmental/city/example-city-air-portal/2026-09-18-lars-taylor-2.yaml")
        check("build: and does not re-promote an entry already live", out2.get("promoted"), False)
        code3, out3 = build(SAMPLE, 214, "2026-09-22")
        check("build: a third gets -3", out3.get("review_path"),
              "reviews/environmental/city/example-city-air-portal/2026-09-18-lars-taylor-3.yaml")
        check("write: the agent is named, the person is still the reviewer",
              ("assisted_by: Claude Code" in written, "by: Lars Taylor" in written), (True, True))
        solo = build(SAMPLE.replace("### Assisted by\n\nClaude Code", "### Assisted by\n\n_No response_"), 13, "2026-09-22")
        check("write: no agent, no assisted_by line", "assisted_by" in (ROOT / solo[1]["review_path"]).read_text(), False)

        # usable-with-caveats writes the review and leaves the status alone.
        entry.write_text(original)
        code4, out4 = build(SAMPLE.replace("\nusable\n", "\nusable-with-caveats\n"), 215, "2026-09-22")
        check("build: usable-with-caveats does not promote", out4.get("promoted"), False)
        check("build: and leaves the entry byte-identical", entry.read_text(), original)

        # Two candidate lines: ambiguous, so touch nothing.
        entry.write_text(original + "status: candidate\n")
        code5, out5 = build(SAMPLE, 216, "2026-09-22")
        check("build: two `status: candidate` lines promote nothing", out5.get("promoted"), False)

        # An entry this list does not carry.
        code6, out6 = build(SAMPLE.replace("example-city-air-portal", "nothing-here"), 217, "2026-09-22")
        check("build: unknown entry exits 3", (code6, out6.get("error")), (3, "entry-missing"))

        # A body with a required field left blank.
        code7, out7 = build(SAMPLE.replace("Barcelona", "_No response_"), 218, "2026-09-22")
        check("build: a missing required field exits 4", (code7, out7.get("fields")),
              (4, "Territory you read it for"))
        check("build: and says so in one postable line",
              (out7["message"].count("\n"), out7["message"].startswith("This review is missing")),
              (0, True))

        # Answers the form lets through and the schema refuses. These used to exit 0 and fail
        # later, in validate.py, where nothing comments on the issue.
        written_before = len(list(REVIEWS_DIR.rglob("*.yaml")))
        code8, out8 = build(SAMPLE.replace("Two stations", "x" * 2001), 219, "2026-09-22")
        check("build: a note over the schema's maxLength exits 4",
              (code8, out8.get("fields", "").startswith("**Notes for the next reader** is 2,")),
              (4, True))
        check("build: and writes nothing", len(list(REVIEWS_DIR.rglob("*.yaml"))), written_before)
        code9, out9 = build(SAMPLE.replace("\nusable\n", "\ngreat\n"), 220, "2026-09-22")
        check("build: a hand-typed verdict outside the enum exits 4",
              (code9, "`great`" in out9.get("message", "")), (4, True))
        check("build: and the message is one postable line", out9.get("message", "\n").count("\n"), 0)
    ROOT = real_root
    DATA_DIR, REVIEWS_DIR = ROOT / "data", ROOT / "reviews"

    print(f"\nreview_from_issue selftest: {bad} failed.")
    return 1 if bad else 0


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--issue", type=int)
    ap.add_argument("--body-file")
    ap.add_argument("--created", default=_dt.date.today().isoformat())
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args(argv)

    if args.selftest:
        return selftest()
    if not (args.issue and args.body_file):
        ap.error("--issue and --body-file are required")

    code, out = build(Path(args.body_file).read_text(encoding="utf-8"), args.issue, args.created)
    print(json.dumps(out, indent=2))
    if github_output := os.environ.get("GITHUB_OUTPUT"):
        with open(github_output, "a", encoding="utf-8") as fh:
            for key, value in out.items():
                if isinstance(value, bool):
                    value = str(value).lower()
                fh.write(f"{key}={' '.join(str(value).split())}\n")
    return code


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
