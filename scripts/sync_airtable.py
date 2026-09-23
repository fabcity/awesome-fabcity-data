#!/usr/bin/env python3
"""Push the registry into the Airtable `Data Sources` mirror. One way, git wins.

    python scripts/sync_airtable.py --plan     # what the repo produces. No key, no network.
    python scripts/sync_airtable.py --check    # compare against Airtable; exit 1 if stale
    python scripts/sync_airtable.py --write    # upsert, keyed on slug

`data/{pillar}/{scale}/{slug}.yaml` is the source of record and this script only ever writes in
that direction. The Airtable table says so in its own description, and the reason is the one
`wired_in_planetai` taught: a hand-typed claim in one system about another drifts, and by September
2026 sixteen of thirty-two flags were wrong. A mirror that anybody can edit is the same mistake with
a nicer interface, so nothing here reads Airtable back into the repo.

**What Airtable is for, and what it is not.** It is for coordination — who could review what, which
territory is next, what is stuck. It is NOT where a review lives. A review is testimony with an
author, a date and a place, and it lives at `reviews/{entry}/{date}-{reviewer}.yaml` where it can be
dereferenced. This script carries a *summary* of that testimony (how many, by whom, when) so a
queue can be built on it; the testimony itself stays in git.

WHY THIS EXISTS NOW. The mirror was last synced 2026-07-04 with 32 of what are now 238 entries, and
it still carries a `wired` checkbox. CONTRIBUTING §2b says `wired_in_planetai` is "removed in the
release after the mirror reads `adapter` instead" — so this script is the gate on deleting that
field. It writes `adapter` and `feeds_cells` and does not write `wired`.

Standard library only, deliberately: the repo's dependencies are pyyaml and jsonschema, and one
more for an HTTP POST is not a trade worth making. PyYAML is already here.

    AIRTABLE_API_KEY    required for --check and --write (a personal access token)
    AIRTABLE_BASE       default appmNQaDGEFE9VcYh  (FCI Observations)
    AIRTABLE_TABLE      default Data Sources
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

BASE = os.environ.get("AIRTABLE_BASE", "appmNQaDGEFE9VcYh")
TABLE = os.environ.get("AIRTABLE_TABLE", "Data Sources")
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


def fetch() -> dict[str, dict]:
    """Every record in the table, keyed on slug."""
    url = f"{API}/{BASE}/{urllib.request.quote(TABLE)}"
    out, offset = {}, None
    while True:
        page = _req("GET", url + (f"?offset={offset}" if offset else ""))
        for rec in page.get("records", []):
            f = rec.get("fields", {})
            if f.get("slug"):
                out[f["slug"]] = f
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


def main(argv: list[str]) -> int:
    rows = build()
    if "--plan" in argv:
        print(f"{len(rows)} records from {DATA.relative_to(ROOT)}/ -> base {BASE}, table {TABLE!r}\n")
        counts = {}
        for r in rows:
            counts[r["status"]] = counts.get(r["status"], 0) + 1
        print("  by status:      " + ", ".join(f"{k} {v}" for k, v in sorted(counts.items())))
        print(f"  with adapter:   {sum(1 for r in rows if r['adapter'])}")
        print(f"  feeding a cell: {sum(1 for r in rows if r['feeds_cells'])}")
        print(f"  with a review:  {sum(1 for r in rows if r['reviews_count'])}")
        print(f"\n  `wired` is NOT written: this sync replaces it with `adapter` (CONTRIBUTING 2b).")
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
    if present is not None and "wired" in present:
        print("  note: the table still has a `wired` checkbox. This sync stops writing it; it can be")
        print("        deleted once nothing reads it, which is what CONTRIBUTING 2b is waiting for.\n")

    have = fetch()
    add = [r for r in rows if r["slug"] not in have]
    upd = [(r, differs(r, have[r["slug"]])) for r in rows if r["slug"] in have]
    upd = [(r, d) for r, d in upd if d]
    gone = sorted(set(have) - {r["slug"] for r in rows})

    print(f"  Airtable has {len(have)}; the repo has {len(rows)}.")
    print(f"  {len(add)} to add, {len(upd)} to update, {len(rows) - len(add) - len(upd)} already current.")
    for r in add[:10]:
        print(f"      + {r['slug']}")
    if len(add) > 10:
        print(f"      + … and {len(add) - 10} more")
    for r, d in upd[:10]:
        print(f"      ~ {r['slug']}: {', '.join(d)}")
    if len(upd) > 10:
        print(f"      ~ … and {len(upd) - 10} more")
    if gone:
        print(f"  {len(gone)} rows in Airtable are not in the repo. This script never deletes; "
              f"they are listed so somebody can decide:")
        for s in gone[:10]:
            print(f"      ? {s}")

    if "--check" in argv:
        if add or upd:
            print("\n  the mirror is behind. Run with --write.", file=sys.stderr)
            return 1
        print("\n  the mirror matches the repo.")
        return 0

    if missing and "--write" in argv:
        print("\n  refusing to write: the fields above do not exist and the batch would fail.",
              file=sys.stderr)
        return 1

    if "--write" not in argv:
        print("\n  nothing written. Pass --write to upsert, or --plan to see the records offline.")
        return 0

    url = f"{API}/{BASE}/{urllib.request.quote(TABLE)}"
    sent = 0
    for i in range(0, len(rows), BATCH):
        chunk = rows[i:i + BATCH]
        _req("PATCH", url, {
            "performUpsert": {"fieldsToMergeOn": ["slug"]},
            "records": [{"fields": r} for r in chunk],
            "typecast": True,   # lets a new `status` or `feeds_cells` option create itself
        })
        sent += len(chunk)
        print(f"  upserted {sent}/{len(rows)}")
        time.sleep(PAUSE)
    print(f"\n  {sent} records upserted, keyed on slug. git remains the source of record.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
