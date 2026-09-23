#!/usr/bin/env python3
"""Push the registry into the Airtable mirror. One way, git wins.

    python scripts/sync_airtable.py --plan     # what the repo produces. No key, no network.
    python scripts/sync_airtable.py --check    # compare against Airtable; exit 1 if stale
    python scripts/sync_airtable.py --write    # upsert, keyed on slug / on name

Two tables, both one-way:

    data/{pillar}/{scale}/{slug}.yaml  ->  Data Sources   keyed on `slug`
    REVIEWERS.md                       ->  Reviewers      keyed on `name`

Both directions are deliberate. The reason is the one `wired_in_planetai` taught: a hand-typed
claim in one system about another drifts, and by September 2026 sixteen of thirty-two flags were
wrong. A mirror that anybody can edit is the same mistake with a nicer interface, so nothing here
reads Airtable back into the repo. For REVIEWERS.md the rule is sharper still — each row belongs
to the person named in it, and a third party editing somebody's "will not review" in a shared base
is precisely what one-way prevents.

**What Airtable is for, and what it is not.** It is for coordination — who could review what, which
territory is next, what is stuck. It is NOT where a review lives. A review is testimony with an
author, a date and a place, and it lives at `reviews/{entry}/{date}-{reviewer}.yaml` where it can be
dereferenced. This script carries a *summary* of that testimony (how many, by whom, when) so a
queue can be built on it; the testimony itself stays in git.

WHY THIS EXISTS NOW. The mirror was last synced 2026-07-04 with 32 of what are now 237 entries, and
it still carries a `wired` checkbox. CONTRIBUTING 2b says `wired_in_planetai` is "removed in the
release after the mirror reads `adapter` instead" — so this script is the gate on deleting that
field. It writes `adapter` and `feeds_cells` and does not write `wired`.

Standard library only, deliberately: the repo's dependencies are pyyaml and jsonschema, and one
more for an HTTP POST is not a trade worth making. PyYAML is already here.

    AIRTABLE_API_KEY          required for --check and --write (a personal access token)
    AIRTABLE_BASE             default appmNQaDGEFE9VcYh  (FCI Observations)
    AIRTABLE_TABLE            default Data Sources
    AIRTABLE_REVIEWERS_TABLE  default Reviewers
"""
from __future__ import annotations

import json
import os
import sys
import time
import urllib.error
import urllib.request
from datetime import date
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.stderr.write("Missing dependency. Install with: pip install pyyaml\n")
    sys.exit(2)

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
REVIEWS = ROOT / "reviews"
REVIEWERS_MD = ROOT / "REVIEWERS.md"

BASE = os.environ.get("AIRTABLE_BASE", "appmNQaDGEFE9VcYh")
TABLE = os.environ.get("AIRTABLE_TABLE", "Data Sources")
REVIEWERS_TABLE = os.environ.get("AIRTABLE_REVIEWERS_TABLE", "Reviewers")
API = "https://api.airtable.com/v0"
USABLE = ("usable", "usable-with-caveats")
BATCH = 10          # Airtable's per-request record limit
PAUSE = 0.25        # its rate limit is 5 requests/second


def _s(v):
    """Airtable wants a string or null, never a date object."""
    return None if v is None else str(v)


def reviews_by_entry() -> dict[str, list[dict]]:
    out: dict[str, list[dict]] = {}
    if not REVIEWS.is_dir():
        return out
    for p in sorted(REVIEWS.rglob("*.yaml")):
        r = yaml.safe_load(p.read_text(encoding="utf-8")) or {}
        if isinstance(r, dict) and r.get("entry"):
            out.setdefault(r["entry"], []).append(r)
    return out


def build() -> list[dict]:
    """One Airtable record per entry. Field names, not ids, so a human can read a diff."""
    revs = reviews_by_entry()
    today = date.today().isoformat()
    rows = []
    for p in sorted(DATA.rglob("*.yaml")):
        e = yaml.safe_load(p.read_text(encoding="utf-8")) or {}
        rel = p.relative_to(DATA)
        slug = rel.with_suffix("").as_posix()
        mine = sorted(revs.get(slug, []), key=lambda r: str(r.get("date", "")))
        usable = [r for r in mine if r.get("verdict") in USABLE]
        newest = usable[-1] if usable else None
        rows.append({
            "slug": slug,
            "name": e.get("name"),
            "url": e.get("url"),
            "pillar": e.get("pillar"),
            "scale": e.get("scale"),
            "status": e.get("status"),
            "license": e.get("license"),
            "api": _s(e.get("api")),
            "pilots": e.get("pilot_relevance") or [],
            "tags": e.get("tags") or [],
            "upstream_listed_in": e.get("upstream_listed_in") or [],
            "added": _s(e.get("added")),
            "updated": _s(e.get("updated")),
            "description": (e.get("description") or "").strip(),
            "notes": (e.get("notes") or "").strip(),
            # The fields this sync exists to add.
            "adapter": e.get("adapter"),
            "feeds_cells": e.get("feeds_cells") or [],
            "role": e.get("role") or [],
            "act_kind": e.get("act_kind"),
            "reviews_count": len(usable),
            "last_reviewed": _s(newest.get("date")) if newest else None,
            "last_reviewer": newest.get("by") if newest else None,
            "last_synced": today,
        })
    return rows


def _declared(cell: str) -> str | None:
    """`*not declared*` is not a value. An empty cell means nobody has said anything, and copying
    the words into Airtable would turn a silence into a claim somebody did not make."""
    c = cell.strip().strip("*_").strip()
    return None if c.lower() in ("", "not declared", "none") else cell.strip()


def build_reviewers() -> list[dict]:
    """The markdown table in REVIEWERS.md, one record per row.

    REVIEWERS.md is the source of record and this only ever reads it, because each row there
    belongs to the person named in it — "open a PR that changes it, and do not wait for
    permission" is the file's own instruction, and a shared base cannot honour that.
    """
    if not REVIEWERS_MD.is_file():
        return []
    written: dict[str, int] = {}
    for rs in reviews_by_entry().values():
        for r in rs:
            if r.get("by"):
                written[r["by"]] = written.get(r["by"], 0) + 1

    today = date.today().isoformat()
    rows, in_table = [], False
    for raw in REVIEWERS_MD.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line.startswith("|"):
            in_table = False
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) != 4:
            continue
        if cells[0] == "Name":              # the header names the columns
            in_table = True
            continue
        if not in_table:
            continue
        if set("".join(cells)) <= set("-: "):   # the | --- | separator
            continue
        name, org, terr, wont = (_declared(c) for c in cells)
        if not name:
            continue
        rows.append({
            "name": name,
            "org": org,
            "territories": [t.strip() for t in terr.split(",") if t.strip()] if terr else [],
            "will_not_review": wont,
            "reviews_written": written.get(name, 0),
            "last_synced": today,
        })
    return rows


# ---------------------------------------------------------------- Airtable
def _req(method: str, url: str, payload: dict | None = None) -> dict:
    key = os.environ.get("AIRTABLE_API_KEY")
    if not key:
        sys.stderr.write(
            "AIRTABLE_API_KEY is not set, so this cannot reach Airtable.\n"
            "  --plan needs no key and shows exactly what would be written.\n")
        sys.exit(2)
    body = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(url, data=body, method=method, headers={
        "Authorization": f"Bearer {key}", "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as ex:
        sys.stderr.write(f"Airtable {method} {url} -> {ex.code}\n{ex.read().decode()[:600]}\n")
        raise


# The seven fields this sync adds, with the types they need. Airtable's `typecast` can invent a new
# OPTION inside an existing select; it cannot invent a FIELD, so an upsert naming one that does not
# exist fails the whole batch with UNKNOWN_FIELD_NAME. --check therefore looks at the table's schema
# first and says which are missing, because that is the error somebody would otherwise hit at record 1.
# They were created in the FCI Observations base on 2026-09-23; this list is what a fresh base needs.
NEW_FIELDS = {
    "adapter":       "singleLineText   — core:<fn> or pack:<id>; replaces the `wired` checkbox",
    "feeds_cells":   "multipleSelects  — the Index cells a node fills from this source",
    "role":          "multipleSelects  — observe | act",
    "act_kind":      "singleSelect     — facility | equipment | design | repair | material | match | network",
    "reviews_count": "number           — usable reviews in reviews/<slug>/",
    "last_reviewed": "date             — newest usable review",
    "last_reviewer": "singleLineText   — who wrote it",
}


def table_fields() -> set[str] | None:
    """Field names the table actually has, from the metadata API. None if it cannot be read —
    a token without schema scope still works for records, so this is a warning and not a failure."""
    try:
        meta = _req("GET", f"{API}/meta/bases/{BASE}/tables")
    except Exception:
        return None
    for t in meta.get("tables", []):
        if t.get("name") == TABLE or t.get("id") == TABLE:
            return {f["name"] for f in t.get("fields", [])}
    return None


def fetch(table: str, key: str) -> dict[str, dict]:
    """Every record in a table, keyed on the field the upsert merges on."""
    url = f"{API}/{BASE}/{urllib.request.quote(table)}"
    out, offset = {}, None
    while True:
        page = _req("GET", url + (f"?offset={offset}" if offset else ""))
        for rec in page.get("records", []):
            f = rec.get("fields", {})
            if f.get(key):
                out[f[key]] = f
        offset = page.get("offset")
        if not offset:
            return out
        time.sleep(PAUSE)


def differs(want: dict, have: dict) -> list[str]:
    """Which fields disagree. `last_synced` is excluded — it changes every run by design."""
    bad = []
    for k, v in want.items():
        if k == "last_synced":
            continue
        h = have.get(k)
        if isinstance(v, list):
            if sorted(v) != sorted(h or []):
                bad.append(k)
        elif (v or None) != (h or None):
            bad.append(k)
    return bad


def push(table: str, rows: list[dict], key: str, argv: list[str]) -> int:
    """Report the difference between `rows` and `table`, and with --write close it.

    Returns 1 when --check finds the mirror behind, so this can be a scheduled alarm.
    """
    try:
        have = fetch(table, key)
    except urllib.error.HTTPError as ex:
        if ex.code == 404:
            print(f"\n{table}: no such table in base {BASE}. Skipped.")
            return 0
        raise

    add = [r for r in rows if r[key] not in have]
    upd = [(r, differs(r, have[r[key]])) for r in rows if r[key] in have]
    upd = [(r, d) for r, d in upd if d]
    gone = sorted(set(have) - {r[key] for r in rows})

    print(f"\n{table}: Airtable has {len(have)}; the repo has {len(rows)}.")
    print(f"  {len(add)} to add, {len(upd)} to update, "
          f"{len(rows) - len(add) - len(upd)} already current.")
    for r in add[:10]:
        print(f"      + {r[key]}")
    if len(add) > 10:
        print(f"      + … and {len(add) - 10} more")
    for r, d in upd[:10]:
        print(f"      ~ {r[key]}: {', '.join(d)}")
    if len(upd) > 10:
        print(f"      ~ … and {len(upd) - 10} more")
    if gone:
        print(f"  {len(gone)} rows in Airtable are not in the repo. This script never deletes; "
              f"they are listed so somebody can decide:")
        for s in gone[:10]:
            print(f"      ? {s}")

    if "--check" in argv:
        if add or upd:
            print(f"  {table} is behind. Run with --write.", file=sys.stderr)
            return 1
        print(f"  {table} matches the repo.")
        return 0
    if "--write" not in argv:
        return 0

    url = f"{API}/{BASE}/{urllib.request.quote(table)}"
    sent = 0
    for i in range(0, len(rows), BATCH):
        chunk = rows[i:i + BATCH]
        _req("PATCH", url, {
            "performUpsert": {"fieldsToMergeOn": [key]},
            "records": [{"fields": r} for r in chunk],
            "typecast": True,   # lets a new `status` or `feeds_cells` option create itself
        })
        sent += len(chunk)
        print(f"  upserted {sent}/{len(rows)}")
        time.sleep(PAUSE)
    print(f"  {sent} records upserted, keyed on {key}. git remains the source of record.")
    return 0


def main(argv: list[str]) -> int:
    rows = build()
    people = build_reviewers()

    if "--plan" in argv:
        print(f"{len(rows)} records from {DATA.relative_to(ROOT)}/ -> base {BASE}, table {TABLE!r}\n")
        counts = {}
        for r in rows:
            counts[r["status"]] = counts.get(r["status"], 0) + 1
        print("  by status:      " + ", ".join(f"{k} {v}" for k, v in sorted(counts.items())))
        print(f"  with adapter:   {sum(1 for r in rows if r['adapter'])}")
        print(f"  feeding a cell: {sum(1 for r in rows if r['feeds_cells'])}")
        print(f"  with a review:  {sum(1 for r in rows if r['reviews_count'])}")
        # The same three tiers the `needs_review` formula computes in Airtable. A flat "has nobody
        # read this" flag returns 221 of 237, which is not a queue, it is the list.
        q = {1: 0, 2: 0, 3: 0}
        for r in rows:
            if r["status"] == "candidate":
                q[1] += 1
            elif r["adapter"] or r["reviews_count"]:
                continue
            elif r["status"] != "live":
                # deprecated, stale, planned, paywalled: not review work. Asking a volunteer to
                # read a source this list already calls deprecated wastes the scarcest thing here.
                continue
            elif [x for x in r["pilots"] if x != "global"]:
                q[2] += 1
            else:
                q[3] += 1
        print(f"  review queue:   {q[1]} candidate · {q[2]} a pilot city depends on it · {q[3]} unread")
        print("\n  `wired` is NOT written: this sync replaces it with `adapter` (CONTRIBUTING 2b).")
        print(f"\n{len(people)} reviewers from REVIEWERS.md -> table {REVIEWERS_TABLE!r}")
        for p in people:
            print(f"      {p['name']:18} {p['org'] or '—'}")
            print(f"      {'':18} territories: {', '.join(p['territories']) or 'not declared'}"
                  f" · will not review: {p['will_not_review'] or 'not declared'}")
        print(f"\n  sample record:\n{json.dumps(rows[0], indent=4, ensure_ascii=False)}")
        return 0

    present = table_fields()
    missing = [f for f in NEW_FIELDS if present is not None and f not in present]
    if missing:
        print(f"  {len(missing)} field(s) this sync writes do not exist in {TABLE!r} yet. Create them,")
        print( "  then re-run — Airtable's typecast can add a select OPTION but never a FIELD:")
        for f in missing:
            print(f"      {f:15} {NEW_FIELDS[f]}")
        print()
        if "--write" in argv:
            print("  refusing to write: the fields above do not exist and the batch would fail.",
                  file=sys.stderr)
            return 1
    if present is not None and "wired" in present:
        print("  note: the table still has a `wired` checkbox. This sync stops writing it; it can be")
        print("        deleted once nothing reads it, which is what CONTRIBUTING 2b is waiting for.")

    code = push(TABLE, rows, "slug", argv)
    code = max(code, push(REVIEWERS_TABLE, people, "name", argv))

    if "--check" not in argv and "--write" not in argv:
        print("\n  nothing written. Pass --write to upsert, or --plan to see the records offline.")
    return code


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
