#!/usr/bin/env python3
"""Copy the figures cities send from Airtable into observations/, one way.

    python scripts/copy_figures.py --plan                     # what would change, and what is skipped and why
    python scripts/copy_figures.py --check                    # exit 1 when observations/ differs from Airtable
    python scripts/copy_figures.py --write [--file-sources]   # write the files; file each new source as an issue
    python scripts/copy_figures.py --plan --records rows.json # records from a file, no network

A figure's home is the Airtable table `City figures`, filled through the form "Send a figure"
(docs/airtable.md). This reads that table and nothing else, and never writes to it. observations/ is
a mirror of it: every *.yaml there is rewritten from Airtable on each run, and a file Airtable no
longer produces is removed, so a figure the team marks `needs a fix` leaves the public record on
the next run. Change a figure in Airtable, never in the file.

What goes out, and what stays in Airtable:

    may_publish yes, a value      `candidate`, or `live` once the team sets state `checked`
    may_publish no or ask         `held`, with no value, no source and no terms
    not_held ticked               `not-held`, with no value
    sent_by (the person's name)   never; the file carries `sent_by_role`
    state `needs a fix`           nothing

A record is skipped, with a reason printed, when its place is in neither places.yaml nor
fictional.yaml, when the `fictional` box disagrees with the place, when its reading is not one of
R1 to R14, when a name or role looks like an email address or phone number, when a value comes
with no source, or when the figure would not pass schema/observation.schema.json. Reasons name the
Airtable record, never what the person typed.

--records takes a JSON list of records in Airtable's REST shape, keyed by field name:
[{"id": "rec…", "createdTime": "…", "fields": {"place": "bali", "reading_id": ["R1"], …}}].
Without it the table is read over the REST API with the token in AIRTABLE_TOKEN (sync_airtable._req).
`createdTime` is the day a figure was sent; the later of two figures for the same place, reading,
year and district replaces the earlier one here, and Airtable keeps both.

--file-sources opens a `source: <id>` issue, with `gh`, for each published figure whose source_url
no entry in data/ holds as `url` or `api`, unless an issue with that title already exists (open
or closed), so a daily run never files a source twice. source-to-pr.yml turns the issue into a
`candidate` entry. A fictional place never files a source.
"""
from __future__ import annotations

import argparse
import contextlib
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

import jsonschema
import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
from source_from_issue import FIELDS, entry_slug  # noqa: E402
from sync_airtable import API, BASE, PAUSE, _req  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
TABLE = os.environ.get("AIRTABLE_FIGURES_TABLE", "tblgsmFzzFYy0iCbC")   # City figures
SCHEMA = jsonschema.Draft202012Validator(
    json.loads((ROOT / "schema" / "observation.schema.json").read_text(encoding="utf-8")))
# One copy of the rule: the schema's own pattern for an email address or a phone number.
CONTACT = re.compile(SCHEMA.schema["$defs"]["plain"]["not"]["pattern"])
SLUG = re.compile(r"^[a-z0-9-]+$")
KEYS = ("year", "state", "value", "unit", "district", "source_url", "source_name", "terms",
        "sent_by_role", "sent_on", "checked_by", "checked_on")
HEADER = "# Copied from Airtable `City figures` by scripts/copy_figures.py. Change a figure there, not here.\n"
# Known open licences, matched loosely: lowercased, everything but letters and digits dropped, then
# looked for anywhere in the terms. ponytail: a phrase like "not public domain" still matches; a
# person reads every filed source before it merges.
OPEN = ("ccby40", "ccbysa40", "cc0", "creativecommonsattribution40", "creativecommonsattributionsharealike40",
        "odbl", "opendatabaselicen", "ogluk", "opengovernmentlicen", "pddl", "publicdomain")


def _places(path: Path) -> dict[str, str]:
    doc = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    return {p["slug"]: p.get("name", p["slug"]) for p in doc.get("places", [])}


PLACES = _places(ROOT / "places.yaml")
FICTIONAL = _places(ROOT / "fictional.yaml")


def _text(v) -> str:
    return " ".join(str(v or "").split())


def figure(rec: dict, places: set[str], fictional: set[str], readings: set[str]):
    """(place, reading, figure) for one Airtable record, or the reason it is skipped."""
    f = rec.get("fields", {})
    place = _text(f.get("place")).lower()
    ids = f.get("reading_id") or []
    ids = [_text(i) for i in (ids if isinstance(ids, list) else [ids])]
    who = f"{rec.get('id', 'a record')} ({place if SLUG.match(place) else 'place?'} {'/'.join(ids) or 'reading?'} {f.get('year', 'year?')})"

    if place not in places and place not in fictional:
        named = repr(place) if SLUG.match(place) else "that is not a slug"
        return f"{who}: place {named} is in neither places.yaml nor fictional.yaml"
    if bool(f.get("fictional")) != (place in fictional):
        return f"{who}: the `fictional` box is {'ticked' if f.get('fictional') else 'empty'}, and {place} " \
               f"{'is' if place in fictional else 'is not'} in fictional.yaml"
    if len(ids) != 1 or ids[0] not in readings:
        return f"{who}: the reading must be one of R1 to R14"
    state = _text(f.get("state")).lower() or "sent"
    if state == "needs a fix":
        return f"{who}: the team marked it `needs a fix`"
    if state not in ("sent", "copied", "checked"):
        return f"{who}: state {state!r} is not one of sent, needs a fix, copied, checked"
    for key in ("sent_by", "sent_by_role", "checked_by"):
        if CONTACT.search(_text(f.get(key))):
            return f"{who}: `{key}` looks like it holds an email address or a phone number"

    year = f.get("year")
    fig = {"year": int(year) if isinstance(year, float) and year.is_integer() else year,
           "district": _text(f.get("district")), "sent_by_role": _text(f.get("sent_by_role")),
           "sent_on": str(rec.get("createdTime", ""))[:10]}
    if f.get("not_held"):
        fig["state"] = "not-held"
    elif _text(f.get("may_publish")).lower() != "yes":
        fig["state"] = "held"
    else:
        if f.get("value") is None:
            return f"{who}: may be published but has no value"
        if not (_text(f.get("source_url")) or _text(f.get("source_name"))):
            return f"{who}: a value with no source (neither source_url nor source_name)"
        live = state == "checked"
        fig.update(state="live" if live else "candidate", value=f["value"], unit=_text(f.get("unit")),
                   source_url=_text(f.get("source_url")), source_name=_text(f.get("source_name")),
                   terms=str(f.get("terms") or "").strip(),
                   checked_by=_text(f.get("checked_by")) if live else "",
                   checked_on=_text(f.get("checked_on")) if live else "")
    fig = {k: fig[k] for k in KEYS if fig.get(k) not in (None, "")}

    doc = {"place": place, "reading": ids[0], "figures": [fig]}
    errors = sorted(SCHEMA.iter_errors(doc), key=lambda e: list(e.path))
    if errors:
        # Never err.message for anything but `required`: it repeats the value back.
        e = errors[0]
        at = ".".join(str(p) for p in list(e.path)[2:]) or "the figure"
        return f"{who}: does not fit schema/observation.schema.json, " + (
            e.message if e.validator == "required" else f"{at} fails `{e.validator}`")
    return place, ids[0], fig


def to_observations(records: list[dict], places: set[str], fictional: set[str],
                    readings: set[str]) -> tuple[dict[str, dict], list[str]]:
    """Airtable records -> {"observations/{place}/{reading}.yaml": doc}, and the skip reasons."""
    latest, skips = {}, []
    for rec in records:
        got = figure(rec, places, fictional, readings)
        if isinstance(got, str):
            skips.append(got)
            continue
        place, reading, fig = got
        key = (place, reading, fig["year"], fig.get("district", ""))
        sent = str(rec.get("createdTime", ""))
        if key not in latest or sent >= latest[key][0]:
            latest[key] = (sent, fig)

    docs: dict[str, dict] = {}
    for key in sorted(latest, key=lambda k: (k[0], k[1], str(k[2]), k[3])):
        place, reading = key[:2]
        doc = docs.setdefault(f"observations/{place}/{reading}.yaml", {
            "place": place, "reading": reading, **({"fictional": True} if place in fictional else {}),
            "figures": []})
        doc["figures"].append(latest[key][1])
    return docs, skips


def render(doc: dict) -> str:
    return HEADER + yaml.safe_dump(doc, sort_keys=False, allow_unicode=True, width=1000)


def apply(docs: dict[str, dict], root: Path, write: bool) -> tuple[list[str], list[str], list[str]]:
    """Files to add, change and remove under root/observations/; with write, make it so."""
    want = {p: render(d) for p, d in docs.items()}
    have = {p.relative_to(root).as_posix(): p.read_text(encoding="utf-8")
            for p in (root / "observations").rglob("*.yaml")}
    add = sorted(set(want) - set(have))
    change = sorted(p for p in want if p in have and have[p] != want[p])
    gone = sorted(set(have) - set(want))
    if write:
        for p in add + change:
            (root / p).parent.mkdir(parents=True, exist_ok=True)
            (root / p).write_text(want[p], encoding="utf-8")
        for p in gone:
            (root / p).unlink()
            with contextlib.suppress(OSError):   # only when the place has no file left
                (root / p).parent.rmdir()
    return add, change, gone


def is_open(terms: str) -> bool:
    flat = re.sub(r"[^a-z0-9]", "", terms.lower())
    return any(o in flat for o in OPEN)


def source_issue(record: dict, reading: dict) -> tuple[str, str] | None:
    """The `source: <id>` issue for the source behind a published figure, in the shape
    source_from_issue.py parses. None for a fictional place, a figure that is not published, and a
    figure with no source_url. Whether data/ already holds the URL is the caller's question."""
    f = record.get("fields", {})
    place, url = _text(f.get("place")).lower(), _text(f.get("source_url"))
    if (place in FICTIONAL or f.get("fictional") or place not in PLACES or not url or f.get("not_held")
            or _text(f.get("may_publish")).lower() != "yes"):
        return None
    where, rid = PLACES[place], reading["id"]
    reading_name = reading["name"][0].lower() + reading["name"][1:]
    name = (_text(f.get("source_name")) or f"{reading['name']}, {where}")[:120]
    terms = _text(f.get("terms")) or "not stated"
    pillar, scale = (p.lower() for p in reading["cells"][0].split("|"))
    tags = ["city-sent", f"reading-{rid}"] + ([] if is_open(terms) else ["cited-figure"])
    answers = {
        "name": name,
        "url": url,
        "description": f"{name}, the source {where} named for its figure on {reading_name}, "
                       f"reading {rid} of the Fab City Index."[:320],
        "cell": reading["cells"][0],
        "license": terms,
        "places": place,
        "tags": ", ".join(tags),
        "by": _text(f.get("sent_by_role")),
        "org": where,
        "notes": f"Filed from a figure sent through index.fab.city: {where}, reading {rid}, "
                 f"{f.get('year', 'no year given')}. Not yet verified by the Fab City team. Nobody has "
                 "opened the source, read its terms on the publisher's own page or checked the figure "
                 "against it.",
    }
    body = "\n\n".join(f"### {label}\n\n{answers.get(key) or '_No response_'}" for key, label in FIELDS.items())
    return f"source: {pillar}/{scale}/{entry_slug(name)}", body + "\n"


def held_urls() -> set[str]:
    out = set()
    for p in (ROOT / "data").rglob("*.yaml"):
        e = yaml.safe_load(p.read_text(encoding="utf-8")) or {}
        out |= {str(e[k]).rstrip("/") for k in ("url", "api") if e.get(k)}
    return out


def sources(records: list[dict], readings: dict[str, dict]) -> list[tuple[str, str]]:
    """One issue per new source behind a published figure, first figure first."""
    held, seen, out = held_urls(), set(), []
    for rec in records:
        got = figure(rec, set(PLACES), set(FICTIONAL), set(readings))
        if isinstance(got, str) or got[2]["state"] not in ("candidate", "live"):
            continue
        issue = source_issue(rec, readings[got[1]])
        url = _text(rec["fields"].get("source_url")).rstrip("/")
        if issue and url not in held and issue[0] not in seen:
            seen.add(issue[0])
            out.append(issue)
    return out


def file_sources(issues: list[tuple[str, str]]) -> None:
    for title, body in issues:
        found = subprocess.run(
            ["gh", "issue", "list", "--state", "all", "--limit", "100", "--search", f'in:title "{title}"',
             "--json", "title", "--jq", ".[].title"],
            capture_output=True, text=True, check=True).stdout.splitlines()
        if title in found:
            print(f"  = {title}: an issue already exists")
            continue
        subprocess.run(["gh", "issue", "create", "--title", title, "--body-file", "-"],
                       input=body, text=True, check=True)
        print(f"  + {title}: filed")


def fetch_records() -> list[dict]:
    """Every record in City figures, over REST. GET only."""
    url = f"{API}/{BASE}/{TABLE}"
    out, offset = [], None
    while True:
        page = _req("GET", url + (f"?offset={offset}" if offset else ""))
        out += page.get("records", [])
        offset = page.get("offset")
        if not offset:
            return out
        time.sleep(PAUSE)


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    mode = ap.add_mutually_exclusive_group(required=True)
    for m in ("--plan", "--check", "--write"):
        mode.add_argument(m, action="store_true")
    ap.add_argument("--records", help="a JSON list of records in Airtable's REST shape, read instead of Airtable")
    ap.add_argument("--file-sources", action="store_true", help="open a `source:` issue for each new source")
    a = ap.parse_args(argv)
    if a.file_sources and not a.write:
        ap.error("--file-sources goes with --write: a plan or a check files nothing")

    if a.records:
        records = json.loads(Path(a.records).read_text(encoding="utf-8"))
        records = records.get("records", []) if isinstance(records, dict) else records
    else:
        records = fetch_records()
    readings = {r["id"]: r for r in yaml.safe_load((ROOT / "readings.yaml").read_text(encoding="utf-8"))["readings"]}
    docs, skips = to_observations(records, set(PLACES), set(FICTIONAL), set(readings))
    add, change, gone = apply(docs, ROOT, write=a.write)

    figures = sum(len(d["figures"]) for d in docs.values())
    print(f"{len(records)} records in City figures -> {figures} figures in {len(docs)} files under observations/")
    print(f"  {len(add)} to add, {len(change)} to change, {len(gone)} to remove, "
          f"{len(docs) - len(add) - len(change)} already current.")
    for sign, paths in (("+", add), ("~", change), ("-", gone)):
        for p in paths:
            print(f"      {sign} {p}")
    if skips:
        print(f"  {len(skips)} records skipped:")
        for s in skips:
            print(f"      ! {s}")
    issues = sources(records, readings)
    if issues:
        print(f"  {len(issues)} sources the registry does not hold:")
        for title, _ in issues:
            print(f"      ? {title}")

    if a.check and (add or change or gone):
        print("  observations/ is behind Airtable. Run with --write.", file=sys.stderr)
        return 1
    if a.write:
        print("  written. Airtable is unchanged: this copy only reads it.")
    if a.file_sources:
        file_sources(issues)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
