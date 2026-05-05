#!/usr/bin/env python3
"""
Generate the data sections of README.md from data/{pillar}/{scale}/*.yaml files.

The README has a hand-maintained intro + outro, and a generated middle
between two sentinel comments:

    <!-- BEGIN GENERATED -->
    ... auto-generated content ...
    <!-- END GENERATED -->

This script reads every YAML entry, sorts by pillar then scale then name,
and writes a Markdown listing between those sentinels. Re-running the script
is idempotent.

Run from repo root:
    python scripts/build_readme.py

Dependencies:
    pip install pyyaml
"""

import sys
from pathlib import Path
from typing import Any, Dict, List

try:
    import yaml
except ImportError:
    sys.stderr.write("Missing dependency. Install with: pip install pyyaml\n")
    sys.exit(2)


ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
README = ROOT / "README.md"

PILLAR_ORDER = ["environmental", "social", "economic", "governance"]
SCALE_ORDER = ["planet", "bioregion", "region", "city", "community"]
PILLAR_LABEL = {
    "environmental": "Environmental",
    "social": "Social",
    "economic": "Economic",
    "governance": "Governance",
}
SCALE_LABEL = {
    "planet": "Planet",
    "bioregion": "Bioregion",
    "region": "Region",
    "city": "City",
    "community": "Community",
}

BEGIN = "<!-- BEGIN GENERATED -->"
END = "<!-- END GENERATED -->"


def load_entries() -> List[Dict[str, Any]]:
    entries = []
    for path in sorted(DATA_DIR.rglob("*.yaml")):
        with path.open(encoding="utf-8") as fh:
            entry = yaml.safe_load(fh) or {}
        entry["_path"] = path.relative_to(ROOT).as_posix()
        entries.append(entry)
    return entries


def fmt_status(s: str) -> str:
    icons = {
        "live": "✅ `live`",
        "stale": "⏳ `stale`",
        "paywalled": "💲 `paywalled`",
        "deprecated": "⛔ `deprecated`",
        "planned": "📋 `planned`",
    }
    return icons.get(s, f"`{s}`")


def fmt_pilots(pilots: List[str]) -> str:
    if not pilots:
        return ""
    short = {
        "barcelona": "BCN",
        "boston": "BOS",
        "santiago": "SCL",
        "bali": "BLI",
        "global": "★",
    }
    return " · ".join(short.get(p, p) for p in pilots)


def render_entry(entry: Dict[str, Any]) -> str:
    name = entry["name"]
    url = entry["url"]
    desc = entry["description"].strip().replace("\n", " ")
    status = fmt_status(entry["status"])
    license_ = entry["license"]
    pilots = fmt_pilots(entry.get("pilot_relevance", []))
    wired = "🔌 wired in PLANETAI" if entry.get("wired_in_planetai") else ""

    parts = [f"**[{name}]({url})** — {status} · `{license_}`"]
    if pilots:
        parts.append(f"_{pilots}_")
    if wired:
        parts.append(wired)

    head = " · ".join(parts)
    return f"- {head}\n  {desc}"


def render_generated() -> str:
    entries = load_entries()
    by_pillar_scale: Dict[str, Dict[str, list]] = {}
    for e in entries:
        by_pillar_scale.setdefault(e["pillar"], {}).setdefault(e["scale"], []).append(e)

    lines = []
    for pillar in PILLAR_ORDER:
        if pillar not in by_pillar_scale:
            continue
        lines.append(f"## {PILLAR_LABEL[pillar]}\n")
        for scale in SCALE_ORDER:
            scale_entries = by_pillar_scale[pillar].get(scale, [])
            if not scale_entries:
                continue
            lines.append(f"### {SCALE_LABEL[scale]}\n")
            scale_entries.sort(key=lambda e: e["name"].lower())
            for e in scale_entries:
                lines.append(render_entry(e))
            lines.append("")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    if not README.exists():
        sys.stderr.write(f"{README} not found\n")
        return 1
    text = README.read_text(encoding="utf-8")

    generated = render_generated()
    block = f"{BEGIN}\n\n{generated}\n{END}"

    if BEGIN in text and END in text:
        before = text.split(BEGIN)[0]
        after = text.split(END, 1)[1]
        new_text = f"{before}{block}{after}"
    else:
        # First-time install: append the block to the end with a heading sentinel
        new_text = text.rstrip() + "\n\n" + block + "\n"

    README.write_text(new_text, encoding="utf-8")
    print(f"Wrote {README} with {len(load_entries())} entries.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
