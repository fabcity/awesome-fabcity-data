#!/usr/bin/env python3
"""Turn a `source: <id>` issue into a candidate entry under data/.

    python scripts/source_from_issue.py --issue 120 --body-file body.md --created 2026-11-06
    python scripts/source_from_issue.py --selftest

Called by .github/workflows/source-to-pr.yml, the way review_from_issue.py is called by
review-to-pr.yml. Two bodies arrive here: the one GitHub renders from
.github/ISSUE_TEMPLATE/source-submit.yml, and the one index.fab.city/operate/add-source writes,
which carries the same `### <label>` fields and then a `### Entry (YAML)` block with the whole entry.
The fields are what this reads. The YAML block is only cross-checked against them, and a
disagreement is reported in the output for the PR body, never used to fill a field.

Exit codes, which the workflow branches on:

    0   an entry was written; the JSON on stdout says where
    3   the id `pillar/scale/slug` already exists under data/ — write nothing, comment on the issue
    4   the body is missing a required field, or has an answer the schema or validate.py would
        refuse — write nothing, comment on the issue

Every entry this writes is `status: candidate`. `live` needs a review or an adapter, and a person
files those; see CONTRIBUTING.md, "Criterion 3 is two states".
"""
from __future__ import annotations

import argparse
import datetime as _dt
import json
import os
import re
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
from review_from_issue import NO_RESPONSE, agent_named, parse_body, slug as person_slug, yaml_scalar  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
TEMPLATE = ROOT / ".github" / "ISSUE_TEMPLATE" / "source-submit.yml"
SCHEMA = ROOT / "schema" / "dataset.schema.json"
PLACES = ROOT / "places.yaml"

CELL_RE = re.compile(r"^(Environmental|Social|Economic|Governance)\|(Planet|Bioregion|Region|City|Community)$")
SLUG_RE = re.compile(r"^[a-z0-9-]+$")
FENCE_RE = re.compile(r"```ya?ml\s*\n(.*?)```", re.S)
REFILE = ("Edit the issue body, then remove and re-add the `source-submission` label, "
          "or file it again as a new issue.")

# The join between the form, the site's page and this script is the label TEXT. selftest() asserts
# the template still carries every one of these.
FIELDS = {
    "name": "Name",
    "url": "Home URL",
    "api": "API or download URL",
    "description": "Description",
    "cell": "Cell",
    "license": "Licence",
    "auth": "Authentication",
    "places": "Places",
    "tags": "Tags",
    "by": "Your name",
    "org": "Organisation",
    "assisted_by": "Assisted by",
    "notes": "Notes",
}
# `notes` is required here although the schema does not: validate.py refuses a candidate without them.
REQUIRED = ("name", "url", "description", "cell", "license", "by", "org", "notes")


def csv(raw: str) -> list[str]:
    seen, out = set(), []
    for item in (x.strip() for x in raw.split(",")):
        if item and item not in seen:
            seen.add(item)
            out.append(item)
    return out


def entry_slug(name: str) -> str:
    """The site's rule: lowercase, runs of anything else become one dash, at most 60 characters."""
    return person_slug(name)[:60].strip("-") if person_slug(name) != "anon" else ""


def known_places() -> set[str]:
    if not PLACES.is_file():
        return set()
    return {p["slug"] for p in (yaml.safe_load(PLACES.read_text(encoding="utf-8")) or {}).get("places", [])}


def schema_breaks(entry: dict) -> list[str]:
    """What the dataset schema would refuse that a form cannot stop: length limits, enums, URL shape,
    slug patterns. Read from the schema so there is one copy of the numbers."""
    props = json.loads(SCHEMA.read_text(encoding="utf-8"))["properties"]
    broken = []
    for key, value in entry.items():
        rule = props.get(key, {})
        label = FIELDS.get(key, key)
        if isinstance(value, str):
            if "maxLength" in rule and len(value) > rule["maxLength"]:
                broken.append(f"**{label}** is {len(value):,} characters and the limit is {rule['maxLength']:,}")
            if "minLength" in rule and len(value) < rule["minLength"]:
                broken.append(f"**{label}** is {len(value)} characters and the minimum is {rule['minLength']}")
            if "enum" in rule and value not in rule["enum"]:
                broken.append(f"**{label}** is `{value}`, which is not one of " + ", ".join(f"`{v}`" for v in rule["enum"]))
            if rule.get("format") == "uri" and not re.match(r"^https?://\S+$", value):
                broken.append(f"**{label}** is `{value}`, which is not a URL")
        elif isinstance(value, list) and (pat := rule.get("items", {}).get("pattern")):
            bad = [v for v in value if not re.match(pat, v)]
            if bad:
                broken.append(f"**{label}** has " + ", ".join(f"`{v}`" for v in bad)
                              + ", which must be lowercase letters, digits and dashes")
    return broken


def render_entry(e: dict) -> str:
    """The entry file, in the template's key order, so it reads like the ones written by hand."""
    block = lambda key, text: [f"{key}: |", *[f"  {line}".rstrip() for line in text.split("\n")]]
    lines = [f"name: {yaml_scalar(e['name'])}", f"url: {yaml_scalar(e['url'])}",
             *block("description", e["description"]),
             f"pillar: {e['pillar']}", f"scale: {e['scale']}", "status: candidate",
             f"license: {yaml_scalar(e['license'])}"]
    if e.get("api"):
        lines.append(f"api: {yaml_scalar(e['api'])}")
    if e.get("places"):
        lines.append("places: [" + ", ".join(e["places"]) + "]")
    if e.get("tags"):
        lines.append("tags: [" + ", ".join(e["tags"]) + "]")
    lines.append(f"added: {e['added']}")
    if e.get("assisted_by"):
        lines.append(f"assisted_by: {yaml_scalar(e['assisted_by'])}")
    lines.append(f"feeds_cells: [{e['cell']}]")
    lines.append(f"auth: {e['auth']}")
    lines += block("notes", e["notes"])
    return "\n".join(lines) + "\n"


def crosscheck(body: str, entry: dict) -> list[str]:
    """The site's `### Entry (YAML)` block against the fields. Keys that disagree, for the PR body."""
    m = FENCE_RE.search(body)
    if not m:
        return []
    try:
        theirs = yaml.safe_load(m.group(1))
    except yaml.YAMLError:
        return ["the YAML block did not parse"]
    if not isinstance(theirs, dict):
        return ["the YAML block is not a mapping"]
    diff = []
    for key in ("name", "url", "pillar", "scale", "license", "auth", "api", "places", "tags"):
        if key in theirs and theirs[key] != entry.get(key) and not (theirs[key] in (None, "", []) and not entry.get(key)):
            diff.append(key)
    if theirs.get("status") not in (None, "candidate"):
        diff.append("status")
    return diff


def build(body: str, issue: int, created: str) -> tuple[int, dict]:
    answers = parse_body(body)
    get = lambda key: answers.get(FIELDS[key], "").strip()

    missing = [FIELDS[k] for k in REQUIRED if not get(k)]
    if missing:
        return 4, {"error": "missing", "fields": ", ".join(missing),
                   "message": "This source is missing a required answer: **" + "**, **".join(missing)
                              + "**. " + REFILE}

    cell = get("cell")
    if not CELL_RE.match(cell):
        return 4, {"error": "cell-malformed", "cell": cell,
                   "message": f"**Cell** is `{cell}`, which is not one of the twenty `Pillar|Scale` cells "
                              "(e.g. `Environmental|City`). " + REFILE}
    pillar, scale = (p.lower() for p in cell.split("|"))

    by = get("by")
    if (who := agent_named(by)) or get("assisted_by").lower() == by.lower():
        return 4, {"error": "contributor-is-agent", "by": by,
                   "message": f"**Your name** reads `{by}`, which "
                              + (f"names an AI agent or tool ({who})" if who else "is the same as **Assisted by**")
                              + ". The contributor is the person who answers for the entry: put your own full name "
                              "there, and the agent in **Assisted by**. " + REFILE}

    stem = entry_slug(get("name"))
    if not stem:
        return 4, {"error": "name-unsluggable", "name": get("name"),
                   "message": f"**Name** is `{get('name')}`, which leaves nothing for a file name once "
                              "lowercased to letters, digits and dashes. " + REFILE}
    entry_id = f"{pillar}/{scale}/{stem}"

    notes = get("notes").rstrip() + f"\n\nFiled by {by}, {get('org')}, from #{issue}"
    entry = {
        "name": get("name"), "url": get("url"), "description": get("description"),
        "pillar": pillar, "scale": scale, "status": "candidate", "license": get("license"),
        "api": get("api") or None, "places": csv(get("places")), "tags": csv(get("tags")),
        "added": created, "assisted_by": get("assisted_by") or None, "feeds_cells": [cell],
        "auth": get("auth") or "none", "notes": notes, "cell": cell,
    }
    checkable = {k: v for k, v in entry.items() if k != "cell" and v not in (None, [])}
    if broken := schema_breaks(checkable):
        return 4, {"error": "schema", "fields": ", ".join(broken),
                   "message": "This source does not fit the dataset schema: " + "; ".join(broken) + ". " + REFILE}
    if unknown := [p for p in entry["places"] if p not in known_places()]:
        return 4, {"error": "places-unknown", "fields": ", ".join(unknown),
                   "message": "**Places** names " + ", ".join(f"`{p}`" for p in unknown)
                              + ", which the Index does not track: a place is a slug from `places.yaml` "
                              "(the list at index.fab.city/api/coverage.json). " + REFILE}

    path = DATA_DIR / f"{entry_id}.yaml"
    if path.exists():
        return 3, {"error": "entry-exists", "entry": entry_id,
                   "message": f"`data/{entry_id}.yaml` already exists, so nothing has been written. If this is "
                              "the same source, review it instead (a `review: ` issue) or edit the entry in a "
                              "pull request. If it is a different source with the same name, change **Name** so "
                              "the slug differs, then " + REFILE[0].lower() + REFILE[1:]}

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_entry(entry), encoding="utf-8")
    return 0, {
        "entry": entry_id, "name": entry["name"], "by": by, "org": get("org"), "cell": cell,
        "entry_path": path.relative_to(ROOT).as_posix(),
        "branch": f"source-{person_slug(entry_id)}-{issue}",
        "crosscheck": ", ".join(crosscheck(body, entry)),
    }


SAMPLE = """### Name

Example City Air Portal

### Home URL

https://example.org/air

### API or download URL

https://example.org/api/air/v1

### Description

Hourly readings from the example city's regulatory air-quality stations, published by its council on a CKAN portal.

### Cell

Environmental|City

### Licence

CC-BY-4.0

### Authentication

none

### Places

barcelona, bali

### Tags

air-quality, regulatory-monitoring

### Your name

Lars Taylor

### Organisation

Fab City Foundation

### Assisted by

Claude Code

### Notes

VERIFIED: 2026-11-06, the portal's dataset page and the API.
LICENCE: the dataset page says "CC BY 4.0" under Llicència.
ENDPOINT: /api/air/v1 returned 11 stations, hourly NO2 and PM10 for 2025.

### Entry (YAML)

```yaml
# data/environmental/city/example-city-air-portal.yaml
name: "Example City Air Portal"
url: "https://example.org/air"
description: |
  Hourly readings from the example city's regulatory air-quality stations, published by its council on a CKAN portal.
pillar: environmental
scale: city
status: candidate
license: "CC-BY-4.0"
api: "https://example.org/api/air/v1"
places: ["barcelona", "bali"]
tags: ["air-quality", "regulatory-monitoring"]
added: 2026-11-06
assisted_by: "Claude Code"
feeds_cells: ["Environmental|City"]
auth: none
notes: |
  VERIFIED: 2026-11-06, the portal's dataset page and the API.
```

_Filed from index.fab.city. The name above is the person's; this account only carries it._
"""


def selftest() -> int:
    """The parse, the id, the refusals and the written file, on a temp tree — and the written file
    against the real schema and validate.py's candidate rule."""
    import tempfile

    import jsonschema

    global ROOT, DATA_DIR, PLACES
    sys.path.insert(0, str(ROOT / "scripts"))
    from validate import _coerce_dates, candidate_needs_notes

    bad = 0

    def check(label: str, got, want):
        nonlocal bad
        if got != want:
            bad += 1
            print(f"[FAIL] {label}: got {got!r}, wanted {want!r}")
        else:
            print(f"[ ok ] {label}")

    fields = parse_body(SAMPLE)
    check("parse: every label found", [v for v in FIELDS.values() if v not in fields], [])
    check("parse: the YAML block is its own section", "Entry (YAML)" in fields, True)
    check("slug: the site's rule", entry_slug("Barcelona Open Data — Air quality"), "barcelona-open-data-air-quality")
    check("slug: nothing left is nothing", entry_slug("—"), "")
    check("csv: commas, blanks, duplicates", csv("a, b ,,a"), ["a", "b"])

    if TEMPLATE.is_file():
        labels = [l.strip().strip('"\'') for l in re.findall(r"^\s+label: (.+)$", TEMPLATE.read_text(encoding="utf-8"), re.M)]
        check("template: every label this script looks for exists in the form", [v for v in FIELDS.values() if v not in labels], [])
        options = re.findall(r"^\s+- ((?:Environmental|Social|Economic|Governance)\|\w+)$", TEMPLATE.read_text(encoding="utf-8"), re.M)
        check("template: twenty cells in the dropdown", len(options), 20)

    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    validator = jsonschema.Draft202012Validator(schema)
    places = known_places()

    real = (ROOT, DATA_DIR, PLACES)
    with tempfile.TemporaryDirectory() as td:
        ROOT = Path(td)
        DATA_DIR = ROOT / "data"
        PLACES = ROOT / "places.yaml"
        PLACES.write_text(yaml.safe_dump({"places": [{"slug": p} for p in sorted(places)]}))

        code, out = build(SAMPLE, 120, "2026-11-06")
        check("build: exit 0", (code, out.get("error")), (0, None))
        check("build: id from Cell and Name", out.get("entry"), "environmental/city/example-city-air-portal")
        check("build: path", out.get("entry_path"), "data/environmental/city/example-city-air-portal.yaml")
        check("build: branch", out.get("branch"), "source-environmental-city-example-city-air-portal-120")
        check("build: the YAML block agrees with the fields", out.get("crosscheck"), "")
        text = (ROOT / out["entry_path"]).read_text()
        check("write: candidate", "status: candidate\n" in text, True)
        check("write: added is the issue date", "added: 2026-11-06\n" in text, True)
        check("write: feeds_cells", "feeds_cells: [Environmental|City]\n" in text, True)
        check("write: places", "places: [barcelona, bali]\n" in text, True)
        check("write: assisted_by", "assisted_by: Claude Code\n" in text, True)
        check("write: notes end with the filer", text.rstrip().endswith("Filed by Lars Taylor, Fab City Foundation, from #120"), True)
        doc = _coerce_dates(yaml.safe_load(text))
        errs = [e.message for e in validator.iter_errors(doc)]
        check("write: the file passes the dataset schema", errs, [])
        check("write: and validate.py's candidate rule", candidate_needs_notes(doc), None)
        check("write: no `cell` key leaked", "cell" in doc, False)

        code2, out2 = build(SAMPLE, 121, "2026-11-06")
        check("build: the same id again exits 3", (code2, out2.get("error")), (3, "entry-exists"))
        check("build: and says so in one postable line", out2.get("message", "\n").count("\n"), 0)

        no_yaml = SAMPLE.split("### Entry (YAML)")[0]
        c, o = build(no_yaml.replace("Example City Air Portal", "Example Two"), 122, "2026-11-06")
        check("build: the form's shape, no YAML block, exits 0", (c, o.get("crosscheck")), (0, ""))
        c, o = build(SAMPLE.replace("Example City Air Portal", "Example Three", 1), 123, "2026-11-06")
        check("build: a YAML block that disagrees is reported, not used", (c, o.get("crosscheck"), o.get("entry")),
              (0, "name", "environmental/city/example-three"))

        for label, body, want in (
            ("missing Licence", SAMPLE.replace("CC-BY-4.0\n\n### Authentication", "_No response_\n\n### Authentication"), "missing"),
            ("missing Notes", SAMPLE.replace("VERIFIED: 2026-11-06, the portal's dataset page and the API.\nLICENCE", "_No response_\n\n### Entry (YAML)\n\n```yaml\nLICENCE"), "missing"),
            ("a cell typed by hand", SAMPLE.replace("Environmental|City\n\n### Licence", "Air|City\n\n### Licence"), "cell-malformed"),
            ("an agent as the contributor", SAMPLE.replace("Lars Taylor", "Claude Code"), "contributor-is-agent"),
            ("a description over 320", SAMPLE.replace("Hourly readings", "x" * 330 + " readings", 1), "schema"),
            ("notes over 4,000 with the filer line", SAMPLE.replace("ENDPOINT:", "x" * 4000), "schema"),
            ("a home URL that is not one", SAMPLE.replace("https://example.org/air\n", "example.org/air\n", 1), "schema"),
            ("an auth outside the enum", SAMPLE.replace("none\n\n### Places", "free\n\n### Places"), "schema"),
            ("a tag with a space", SAMPLE.replace("air-quality, regulatory-monitoring", "air quality"), "schema"),
            ("a place the Index does not track", SAMPLE.replace("barcelona, bali", "atlantis"), "places-unknown"),
            ("a name that slugs to nothing", SAMPLE.replace("Example City Air Portal", "—", 1), "name-unsluggable"),
        ):
            c, o = build(body.replace("example-city-air-portal", "x-" + str(abs(hash(label)) % 1000)), 130, "2026-11-06")
            check(f"build: {label} exits 4", (c, o.get("error")), (4, want))
            check(f"build: {label} message is one postable line", o.get("message", "\n").count("\n"), 0)
        written = sorted(p.relative_to(DATA_DIR).as_posix() for p in DATA_DIR.rglob("*.yaml"))
        check("build: the refusals wrote nothing", written,
              ["environmental/city/example-city-air-portal.yaml", "environmental/city/example-three.yaml",
               "environmental/city/example-two.yaml"])
    ROOT, DATA_DIR, PLACES = real

    print(f"\nsource_from_issue selftest: {bad} failed.")
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
                fh.write(f"{key}={' '.join(str(value).split())}\n")
    return code


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
