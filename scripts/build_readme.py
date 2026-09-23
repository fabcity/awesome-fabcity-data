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
REVIEWS_DIR = ROOT / "reviews"
README = ROOT / "README.md"

# The verdicts that make an entry `live`, duplicated from scripts/validate.py rather than imported:
# validate.py pulls in jsonschema, and this script's contract is that pyyaml alone regenerates the
# README. Two words are cheaper than that dependency. If they ever disagree, validate.py is right.
USABLE = ("usable", "usable-with-caveats")

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

# Candidates get their own block inside each scale, with the heading saying what the word means, so
# that nobody has to look it up to read the list. Empty blocks are not rendered — this script has
# always skipped empty pillars and empty scales, and twenty "Candidates" headings over nothing would
# be decoration. When the first candidate lands, its scale grows this heading and no other line moves.
CANDIDATES_HEADING = "#### Candidates — verified, not yet reviewed by anyone in the network"


def initials(name: str) -> str:
    """'A. Reviewer' -> 'AR'. Three letters at most: the marker is a pointer into reviews/, not a
    byline, and the full name, org and territory are all in the review file."""
    return "".join(
        w[0] for w in name.replace(".", " ").split() if w[:1].isalpha()
    ).upper()[:3]


def load_reviews() -> Dict[str, str]:
    """{registry id: 'AR 2026-09'} from the newest usable review of each entry.

    Dates are compared as ISO strings — PyYAML hands back a datetime.date for a bare date and a str
    for a quoted one, and str() of either sorts correctly to the day."""
    newest: Dict[str, tuple] = {}
    for path in sorted(REVIEWS_DIR.rglob("*.yaml")):
        review = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        if review.get("verdict") not in USABLE:
            continue
        rid = review.get("entry")
        when = str(review.get("date", ""))[:10]
        by = review.get("by", "")
        if not (rid and when and by):
            continue
        if rid not in newest or when > newest[rid][0]:
            newest[rid] = (when, by)
    return {rid: f"{initials(by)} {when[:7]}" for rid, (when, by) in newest.items()}


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
        "candidate": "🌱 `candidate`",
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


def render_entry(entry: Dict[str, Any], reviews: Dict[str, str]) -> str:
    name = entry["name"]
    url = entry["url"]
    desc = entry["description"].strip().replace("\n", " ")
    status = fmt_status(entry["status"])
    license_ = entry["license"]
    pilots = fmt_pilots(entry.get("pilot_relevance", []))
    # The 🔌 badge is drawn from `adapter`, which replaced a hand-typed boolean: a pointer at code that
    # reads the source can be checked against that code, and the boolean never could. See CONTRIBUTING §2b.
    adapter = entry.get("adapter")
    act_kind = entry.get("act_kind")

    parts = [f"**[{name}]({url})** — {status} · `{license_}`"]
    # Right after the licence, because it is the same kind of fact: who vouched for this, and when.
    # Initials and month from the newest usable review file; the reading itself is in reviews/.
    reviewed = reviews.get(entry["_path"][len("data/"):-len(".yaml")])
    if reviewed:
        parts.append(f"reviewed {reviewed}")
    if pilots:
        parts.append(f"_{pilots}_")
    if adapter:
        parts.append(f"🔌 `{adapter}`")
    if act_kind:
        parts.append(f"🛠 {act_kind}")

    head = " · ".join(parts)
    return f"- {head}\n  {desc}"


def render_generated() -> str:
    entries = load_entries()
    reviews = load_reviews()
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
            # Candidates are held back into their own block below. They are in the list because
            # somebody verified the licence and the endpoint; they are not mixed in with the
            # entries a person read, because that is the distinction the block is for.
            for e in (x for x in scale_entries if x["status"] != "candidate"):
                lines.append(render_entry(e, reviews))
            lines.append("")
            candidates = [x for x in scale_entries if x["status"] == "candidate"]
            if candidates:
                lines.append(f"{CANDIDATES_HEADING}\n")
                for e in candidates:
                    lines.append(render_entry(e, reviews))
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
