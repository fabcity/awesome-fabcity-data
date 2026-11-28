#!/usr/bin/env python3
"""Write a national power system for each country of places.yaml from Ember's Yearly Electricity Data.

    python3 scripts/national_energy.py <path to release_generation_yearly_global.csv>

Reads the rows whose "Electricity source" is "Fossil" and whose "Is aggregated source" is True: their
"Share of generation (%)" is the share of a country's generation from fossil fuels, in percent. The latest
year with a figure wins, per country, and the script prints the countries whose year is older than the newest written. A country with no figure gets no file, never a zero. A file whose
mix.kind is not national is never overwritten. No network: the CSV is a path the person gives.
"""
import csv
import sys
from datetime import date
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent


def rows(csv_path) -> dict[str, tuple[int, float]]:
    """iso3 -> (year, fossil share 0..1), the latest year with a figure."""
    out: dict[str, tuple[int, float]] = {}
    with open(csv_path, newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            iso, pct = r["ISO 3 code"], r["Share of generation (%)"]
            if r["Electricity source"] != "Fossil" or r["Is aggregated source"] != "True" or not iso or not pct:
                continue
            year = int(r["Year"])
            if iso not in out or year > out[iso][0]:
                out[iso] = (year, round(float(pct) / 100, 4))
    return out


def write(table: dict[str, tuple[int, float]], wanted: dict | set, out_dir) -> tuple[list[str], list[str]]:
    """Write systems for the wanted iso3 codes. `wanted` is a set, or a dict iso3 -> country name.
    Returns (written file ids, skipped iso3 codes)."""
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    names = wanted if isinstance(wanted, dict) else {}
    written, skipped = [], []
    for iso in sorted(wanted):
        path = out_dir / f"{iso.lower()}.yaml"
        if iso not in table:
            skipped.append(iso)
            continue
        if path.exists() and (yaml.safe_load(path.read_text(encoding="utf-8")) or {}).get("mix", {}).get("kind") != "national":
            skipped.append(iso)
            continue
        year, share = table[iso]
        country = names.get(iso, iso)
        doc = {
            "id": iso.lower(),
            "name": f"National electricity mix, {country}",
            "country": iso,
            "mix": {"kind": "national", "fossil_share": share, "year": year},
            "readings": ["R2"],
            "sources": ["environmental/planet/ember-yearly-electricity"],
            "attribution": ["Ember Yearly Electricity Data, CC BY 4.0"],
            "notes": (f"Share of electricity generation from fossil fuels in {country}, {year}, from Ember's "
                      f"Yearly Electricity Data (Fossil, share of generation). Written by scripts/national_energy.py "
                      f"on {date.today().isoformat()}."),
        }
        path.write_text(yaml.safe_dump(doc, allow_unicode=True, sort_keys=False, width=110), encoding="utf-8")
        written.append(iso.lower())
    return written, skipped


def older(table: dict[str, tuple[int, float]], written: list[str]) -> str:
    """One line naming the written countries whose year is older than the newest year among them."""
    years = {i.upper(): table[i.upper()][0] for i in written}
    newest = max(years.values(), default=0)
    behind = [f"{i} {y}" for i, y in sorted(years.items()) if y < newest]
    return "older year: " + (", ".join(behind) if behind else "none")


def main(argv) -> int:
    if len(argv) != 2:
        print(__doc__)
        return 2
    places = yaml.safe_load((ROOT / "places.yaml").read_text(encoding="utf-8"))["places"]
    wanted = {p["iso3"]: p["country"] for p in places}
    table = rows(argv[1])
    written, skipped = write(table, wanted, ROOT / "systems" / "energy")
    print(f"wrote {len(written)}: {' '.join(written)}")
    print(f"skipped {len(skipped)} (no figure, or not a national file): {' '.join(skipped)}")
    print(older(table, written))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
