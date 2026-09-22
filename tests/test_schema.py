#!/usr/bin/env python3
"""The schema's own tests. Run from repo root:

    python tests/test_schema.py

`scripts/validate.py` proves the real entries pass. That is only half a gate: a schema that
accepts everything also passes it. These are the cases that must FAIL, plus the handful that must
pass for a reason the real data does not yet demonstrate — `role`, `act_kind` and `adapter` have no
entries behind them until the act sources land, and reviews/ and cells/ are empty by design.

Three sections: the dataset schema, then the review and cell schemas, then the two rules that are
not in any schema at all — `candidate` requires `notes`, and a cell's filename must match its key.
Those two live in scripts/validate.py, so they are tested where they live: a temp tree and a real
subprocess run, because the thing being asserted is what CI does, not what a validator object says.

Deliberately not pytest: this repo's dependencies are pyyaml and jsonschema, and a test file that
adds a third to assert twenty things is worse than the twenty asserts.
"""
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import jsonschema
import yaml

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from validate import _coerce_dates, _message, candidate_needs_notes  # noqa: E402


def _v(name: str) -> jsonschema.Draft202012Validator:
    return jsonschema.Draft202012Validator(
        json.loads((ROOT / "schema" / f"{name}.schema.json").read_text(encoding="utf-8"))
    )


SCHEMA = json.loads((ROOT / "schema" / "dataset.schema.json").read_text(encoding="utf-8"))
V = _v("dataset")
VR = _v("review")
VC = _v("cell")

# A minimal entry that satisfies every `required` key, so each case below tests exactly one thing.
BASE = yaml.safe_load("""
name: Test Source
url: https://example.org/
description: A source that exists only to be validated against, twenty characters and then some.
pillar: environmental
scale: city
status: live
license: CC-BY-4.0
""")

# (label, patch, should_validate)
CASES = [
    # --- adapter: a pointer at the code that reads this source -------------------------------
    ("adapter core:openmeteo_air",      {"adapter": "core:openmeteo_air"}, True),
    ("adapter core:ckan",               {"adapter": "core:ckan"}, True),
    ("adapter pack:open-data-health",   {"adapter": "pack:open-data-health"}, True),
    # NB: `pack:nope` is SYNTACTICALLY fine — the schema cannot know the node's pack list, and it is
    # scripts/wired.py, with the node checked out, that fails on a pack which does not exist.
    ("adapter pack:nope (syntax ok)",   {"adapter": "pack:nope"}, True),
    ("adapter Pack:Nope",               {"adapter": "Pack:Nope"}, False),
    ("adapter core:open-meteo",         {"adapter": "core:open-meteo"}, False),   # core is a fn name, snake_case
    ("adapter pack:Open_Data",          {"adapter": "pack:Open_Data"}, False),    # pack is a dir name, kebab-case
    ("adapter with no prefix",          {"adapter": "openmeteo"}, False),
    ("adapter as a list",               {"adapter": ["core:ckan"]}, False),

    # --- feeds_cells: the Index cells a node fills, in the node's own key spelling -------------
    ("feeds_cells one cell",            {"feeds_cells": ["Governance|City"]}, True),
    ("feeds_cells two cells",           {"feeds_cells": ["Environmental|Community", "Social|Community"]}, True),
    ("feeds_cells empty list",          {"feeds_cells": []}, True),   # 'reads it, fills nothing' is sayable
    ("feeds_cells lowercase",           {"feeds_cells": ["environmental|community"]}, False),
    ("feeds_cells unknown scale",       {"feeds_cells": ["Environmental|Nation"]}, False),
    ("feeds_cells unknown pillar",      {"feeds_cells": ["Ecological|City"]}, False),
    ("feeds_cells slash not pipe",      {"feeds_cells": ["Environmental/City"]}, False),
    ("feeds_cells duplicated",          {"feeds_cells": ["Governance|City", "Governance|City"]}, False),

    # --- auth ---------------------------------------------------------------------------------
    ("auth none",                       {"auth": "none"}, True),
    ("auth key-free-rate-limited",      {"auth": "key-free-rate-limited"}, True),
    ("auth paid",                       {"auth": "paid"}, True),
    ("auth free",                       {"auth": "free"}, False),
    ("auth true",                       {"auth": True}, False),

    # --- role and act_kind move together ------------------------------------------------------
    ("role absent, act_kind absent",    {}, True),
    ("role [observe]",                  {"role": ["observe"]}, True),
    ("role [act] + act_kind",           {"role": ["act"], "act_kind": "facility"}, True),
    ("role [observe, act] + act_kind",  {"role": ["observe", "act"], "act_kind": "network"}, True),
    ("role [act] without act_kind",     {"role": ["act"]}, False),
    ("act_kind without role",           {"act_kind": "facility"}, False),
    ("act_kind with role [observe]",    {"role": ["observe"], "act_kind": "repair"}, False),
    ("role empty list",                 {"role": []}, False),
    ("role duplicated",                 {"role": ["observe", "observe"]}, False),
    ("role make-believe verb",          {"role": ["decide"]}, False),
    ("act_kind make-believe kind",      {"role": ["act"], "act_kind": "vibe"}, False),

    # --- notes: long enough to quote the clause a licence turns on ----------------------------
    ("notes at the 4000 ceiling",       {"notes": "x" * 4000}, True),
    ("notes one over",                  {"notes": "x" * 4001}, False),
    ("notes at the old 2000 limit",     {"notes": "x" * 2000}, True),

    # --- the closed door ----------------------------------------------------------------------
    ("an invented key",                 {"adapters": "core:ckan"}, False),

    # --- status: candidate ---------------------------------------------------------------------
    # The schema knows the word; that `notes` must be non-empty alongside it is validator logic,
    # and is asserted in TREE_CASES below — minLength cannot see the value of another key.
    ("status candidate",                {"status": "candidate"}, True),
    ("status candidate + notes",        {"status": "candidate", "notes": "Licence and endpoint verified; nobody has read it for a territory."}, True),
    ("status made-up",                  {"status": "promising"}, False),
]

# A minimal review that satisfies every `required` key. Reviews carry a `date`, and PyYAML hands
# back a datetime.date for a bare ISO date, which fails `type: string` before format is ever
# considered — so run it through validate's own coercion, the same one the validator uses.
REVIEW = yaml.safe_load("""
entry: environmental/city/example-city-air-portal
by: A. Reviewer
org: Example Fab Lab
date: 2026-09-18
territory: Example City
checked: [licence, endpoint]
verdict: usable
""")

REVIEW_CASES = [
    ("review minimal valid",            {}, True),
    ("review + note and self_declared", {"note": "Station ids are the portal's own.", "self_declared": True}, True),
    ("review + issue number",           {"issue": 212}, True),
    ("review verdict usable-with-caveats", {"verdict": "usable-with-caveats"}, True),
    ("review verdict unusable",         {"verdict": "unusable"}, True),
    ("review unknown verdict",          {"verdict": "probably-fine"}, False),
    ("review verdict as a list",        {"verdict": ["usable"]}, False),
    ("review missing territory",        {"territory": None}, False),
    ("review empty checked",            {"checked": []}, False),
    ("review checked unknown item",     {"checked": ["vibes"]}, False),
    ("review checked duplicated",       {"checked": ["licence", "licence"]}, False),
    ("review entry with no scale",      {"entry": "environmental/thing"}, False),
    ("review entry capitalised",        {"entry": "Environmental|City"}, False),
    ("review entry with .yaml",         {"entry": "environmental/city/thing.yaml"}, False),
    ("review self_declared not a bool", {"self_declared": "yes"}, False),
    ("review issue not an int",         {"issue": "212"}, False),
    ("review an invented key",          {"reviewer": "A. Reviewer"}, False),
]

# A minimal cell. `does_not_claim` is required, and required to be specific enough to be worth
# reading — the schema can only enforce the first half of that.
CELL = yaml.safe_load("""
cell: Environmental|City
indicator_categories: [air quality]
minimum_indicators:
  - name: PM2.5 annual mean
    unit: ug/m3
    aggregation: mean
does_not_claim: Reference-station data does not claim neighbourhood exposure.
""")

CELL_CASES = [
    ("cell minimal valid",              {}, True),
    ("cell + notes",                    {"notes": "Water quality has no entry filed against it."}, True),
    ("cell lowercase key",              {"cell": "environmental|city"}, False),
    ("cell slash not pipe",             {"cell": "Environmental/City"}, False),
    ("cell unknown scale",              {"cell": "Environmental|Nation"}, False),
    ("cell no indicator_categories",    {"indicator_categories": []}, False),
    ("cell no minimum_indicators",      {"minimum_indicators": []}, False),
    ("cell indicator without unit",     {"minimum_indicators": [{"name": "PM2.5", "aggregation": "mean"}]}, False),
    ("cell indicator without aggregation", {"minimum_indicators": [{"name": "PM2.5", "unit": "ug/m3"}]}, False),
    ("cell indicator extra key",        {"minimum_indicators": [{"name": "PM2.5", "unit": "ug/m3", "aggregation": "mean", "source": "x"}]}, False),
    ("cell missing does_not_claim",     {"does_not_claim": None}, False),
    ("cell does_not_claim too short",   {"does_not_claim": "nothing"}, False),
    ("cell an invented key",            {"cells": "Environmental|City"}, False),
]


# --- the rules that are in no schema ----------------------------------------------------------
# `candidate` requires `notes`, and a cell's filename must match its `cell` key. Both live in
# scripts/validate.py because neither is expressible in JSON Schema: one key's constraint depends
# on another's value, and the other depends on the file's own name. So they are tested through
# validate.py on a temp tree, in a real subprocess — what is being asserted is what CI does.

CANDIDATE = """name: Temp Tree Source
url: https://example.org/
description: A source that exists only to be validated against, twenty characters and then some.
pillar: environmental
scale: city
status: candidate
license: CC-BY-4.0
notes: |
  Licence and endpoint verified on 2026-09-18; fits the PM2.5 annual mean row of
  Environmental|City. Nobody has read it for a real territory.
"""

GOOD_REVIEW = """entry: environmental/city/temp-tree-source
by: A. Reviewer
org: Example Fab Lab
date: 2026-09-18
territory: Example City
checked: [licence, endpoint]
verdict: usable
"""

GOOD_CELL = """cell: Environmental|City
indicator_categories: [air quality]
minimum_indicators:
  - name: PM2.5 annual mean
    unit: ug/m3
    aggregation: mean
does_not_claim: Reference-station data does not claim neighbourhood exposure.
"""

ENTRY_AT = "data/environmental/city/temp-tree-source.yaml"

# (label, {path: text}, should_pass, a phrase the output must carry when it fails)
TREE_CASES = [
    ("tree: candidate with notes",
     {ENTRY_AT: CANDIDATE}, True, None),
    ("tree: candidate with no notes at all",
     {ENTRY_AT: CANDIDATE.split("notes:")[0]}, False, "status is candidate and `notes` is empty"),
    ("tree: candidate with empty notes",
     {ENTRY_AT: CANDIDATE.split("notes:")[0] + 'notes: "   "\n'}, False, "`notes` is empty"),
    ("tree: cell filename matches its key",
     {ENTRY_AT: CANDIDATE, "cells/environmental-city.yaml": GOOD_CELL}, True, None),
    ("tree: cell filename does not match its key",
     {ENTRY_AT: CANDIDATE, "cells/environmental-region.yaml": GOOD_CELL}, False, "filename and key must agree"),
    ("tree: review in its entry's directory",
     {ENTRY_AT: CANDIDATE,
      "reviews/environmental/city/temp-tree-source/2026-09-18-a-reviewer.yaml": GOOD_REVIEW}, True, None),
    ("tree: review in somebody else's directory",
     {ENTRY_AT: CANDIDATE,
      "reviews/environmental/city/other-source/2026-09-18-a-reviewer.yaml": GOOD_REVIEW}, False, "move it to reviews/"),
    ("tree: review of an entry that does not exist",
     {"reviews/environmental/city/temp-tree-source/2026-09-18-a-reviewer.yaml": GOOD_REVIEW,
      "data/environmental/city/something-else.yaml": CANDIDATE}, False, "has no file at data/"),
]


def run_tree(files: dict) -> tuple[int, str]:
    """Run scripts/validate.py against a throwaway repo holding exactly `files`. schema/ and
    scripts/ are copied rather than symlinked: validate.py resolves its ROOT from __file__, and a
    symlink would point it back at this repository and validate the real 217 entries."""
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        for sub in ("schema", "scripts"):
            shutil.copytree(ROOT / sub, root / sub)
        for rel, text in files.items():
            f = root / rel
            f.parent.mkdir(parents=True, exist_ok=True)
            f.write_text(text, encoding="utf-8")
        for sub in ("reviews", "cells"):
            (root / sub).mkdir(exist_ok=True)
        proc = subprocess.run([sys.executable, "scripts/validate.py"], cwd=root,
                              capture_output=True, text=True)
        return proc.returncode, proc.stdout + proc.stderr


def patched(base: dict, patch: dict) -> dict:
    """base + patch, where a None in the patch means *remove that key* — the way to say 'missing'."""
    merged = {**base, **patch}
    return {k: v for k, v in merged.items() if v is not None}


def check(validator, base: dict, cases: list) -> int:
    bad = 0
    for label, patch, want in cases:
        # PyYAML hands back datetime.date for a bare ISO date, which fails `type: string`. The
        # validator coerces the same way for real files; do it here so the case tests its subject.
        doc = _coerce_dates(patched(base, patch))
        errs = [e.message for e in validator.iter_errors(doc)]
        got = not errs
        if got != want:
            bad += 1
            print(f"[FAIL] {label}: expected {'valid' if want else 'invalid'}, got "
                  f"{'valid' if got else 'invalid'} {errs[:1]}")
        else:
            print(f"[ ok ] {label}")
    return bad


def main() -> int:
    bad = check(V, BASE, CASES)

    print()
    bad += check(VR, REVIEW, REVIEW_CASES)

    print()
    bad += check(VC, CELL, CELL_CASES)

    # The act_kind conditional produces jsonschema's worst error message; validate.py rewrites it.
    print()
    err = next(e for e in V.iter_errors({**BASE, "act_kind": "facility"}))
    if "act_kind is set but role does not contain" not in _message(err):
        bad += 1
        print(f"[FAIL] validate._message did not rewrite the `not` error: {_message(err)[:80]}")
    else:
        print("[ ok ] validate._message rewrites the act_kind error to one readable line")

    # The same candidate rule as TREE_CASES asserts end to end, called directly — so that a
    # failure says which half broke: the rule, or the run that is supposed to apply it.
    if candidate_needs_notes({"status": "candidate"}) is None:
        bad += 1
        print("[FAIL] candidate_needs_notes let a candidate with no notes through")
    elif candidate_needs_notes({"status": "live"}) is not None:
        bad += 1
        print("[FAIL] candidate_needs_notes objected to an entry that is not a candidate")
    else:
        print("[ ok ] candidate_needs_notes wants notes on a candidate and nowhere else")

    print()
    for label, files, want, phrase in TREE_CASES:
        code, out = run_tree(files)
        got = code == 0
        if got != want:
            bad += 1
            print(f"[FAIL] {label}: expected validate.py to {'pass' if want else 'fail'}, "
                  f"exit was {code}")
            print("       " + "\n       ".join(l for l in out.splitlines() if "[FAIL]" in l)[:400])
        elif phrase and phrase not in out:
            bad += 1
            print(f"[FAIL] {label}: failed as expected but never said {phrase!r}")
        else:
            print(f"[ ok ] {label}")

    total = len(CASES) + len(REVIEW_CASES) + len(CELL_CASES) + len(TREE_CASES) + 2
    print(f"\n{total} case(s), {bad} failed.")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
