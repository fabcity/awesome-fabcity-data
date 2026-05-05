#!/usr/bin/env python3
"""
Validate every YAML entry under data/ against schema/dataset.schema.json.

Run from repo root:
    python scripts/validate.py

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
DATA_DIR = ROOT / "data"


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


def main() -> int:
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    validator = Validator(schema)

    yaml_files = sorted(DATA_DIR.rglob("*.yaml"))
    if not yaml_files:
        print(f"No YAML files found under {DATA_DIR}", file=sys.stderr)
        return 1

    failures = 0
    seen_slugs = {}
    for path in yaml_files:
        rel = path.relative_to(ROOT)
        try:
            entry = yaml.safe_load(path.read_text(encoding="utf-8"))
        except yaml.YAMLError as e:
            print(f"[FAIL] {rel}: invalid YAML — {e}")
            failures += 1
            continue

        if not isinstance(entry, dict):
            print(f"[FAIL] {rel}: top-level must be a mapping (dict)")
            failures += 1
            continue

        # Coerce datetime.date / datetime.datetime to ISO strings for schema
        entry = _coerce_dates(entry)

        # Schema validation
        errors = sorted(validator.iter_errors(entry), key=lambda e: e.path)
        if errors:
            for err in errors:
                loc = ".".join(str(p) for p in err.path) or "<root>"
                print(f"[FAIL] {rel} :: {loc} — {err.message}")
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

        print(f"[ ok ] {rel}")

    if failures:
        print(f"\n{failures} file(s) failed validation.", file=sys.stderr)
        return 1
    print(f"\n{len(yaml_files)} file(s) passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
