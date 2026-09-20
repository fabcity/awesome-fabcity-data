#!/usr/bin/env python3
"""The schema's own tests. Run from repo root:

    python tests/test_schema.py

`scripts/validate.py` proves the 209 real entries pass. That is only half a gate: a schema that
accepts everything also passes it. These are the cases that must FAIL, plus the handful that must
pass for a reason the real data does not yet demonstrate — `role`, `act_kind` and `adapter` have no
entries behind them until the act sources land.

Deliberately not pytest: this repo's dependencies are pyyaml and jsonschema, and a test file that
adds a third to assert twenty things is worse than the twenty asserts.
"""
import json
import sys
from pathlib import Path

import jsonschema
import yaml

ROOT = Path(__file__).resolve().parent.parent
SCHEMA = json.loads((ROOT / "schema" / "dataset.schema.json").read_text(encoding="utf-8"))
V = jsonschema.Draft202012Validator(SCHEMA)

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

    # --- the closed door ----------------------------------------------------------------------
    ("an invented key",                 {"adapters": "core:ckan"}, False),
]


def main() -> int:
    bad = 0
    for label, patch, want in CASES:
        entry = {**BASE, **patch}
        errs = [e.message for e in V.iter_errors(entry)]
        got = not errs
        if got != want:
            bad += 1
            print(f"[FAIL] {label}: expected {'valid' if want else 'invalid'}, got "
                  f"{'valid' if got else 'invalid'} {errs[:1]}")
        else:
            print(f"[ ok ] {label}")

    # The act_kind conditional produces jsonschema's worst error message; validate.py rewrites it.
    sys.path.insert(0, str(ROOT / "scripts"))
    from validate import _message  # noqa: E402
    err = next(e for e in V.iter_errors({**BASE, "act_kind": "facility"}))
    if "act_kind is set but role does not contain" not in _message(err):
        bad += 1
        print(f"[FAIL] validate._message did not rewrite the `not` error: {_message(err)[:80]}")
    else:
        print("[ ok ] validate._message rewrites the act_kind error to one readable line")

    print(f"\n{len(CASES) + 1} case(s), {bad} failed.")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
