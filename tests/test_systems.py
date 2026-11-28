#!/usr/bin/env python3
"""Tests for the places' country codes, and (in later tasks) national systems and place profiles.
Run from repo root:

    python tests/test_systems.py

Plain script, no pytest, like tests/test_schema.py: a temp copy of the tree, a real subprocess run of
scripts/validate.py or scripts/build_index.py, because what is asserted is what CI does.
"""
import contextlib
import io
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
FAILS = 0


def copy_tree() -> Path:
    """A copy of the repository without .git, in a fresh temp dir."""
    dst = Path(tempfile.mkdtemp()) / "tree"
    shutil.copytree(ROOT, dst, ignore=shutil.ignore_patterns(".*", "__pycache__"))
    return dst


def edit(path: Path, fn) -> None:
    path.write_text(fn(path.read_text(encoding="utf-8")), encoding="utf-8")


def run_validate(tree: Path) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, str(tree / "scripts" / "validate.py")],
                          capture_output=True, text=True, cwd=tree)


def build_in(tree: Path) -> dict:
    """Run build_index.py in the tree and return its index.json, parsed."""
    subprocess.run([sys.executable, str(tree / "scripts" / "build_index.py")],
                   capture_output=True, text=True, cwd=tree, check=True)
    return json.loads((tree / "index.json").read_text(encoding="utf-8"))


def seen_by(fn, *args) -> tuple[int, str]:
    """Call a validate.py pass in this process; return (failures, what it printed)."""
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        res = fn(*args)
    return (res if isinstance(res, int) else res[0]), buf.getvalue()


sys.path.insert(0, str(ROOT / "scripts"))
import validate  # noqa: E402

ALL_READINGS = {f"R{i}": {} for i in range(1, 15)}
ALL_ENTRIES = {"economic/community/openstreetmap", "environmental/planet/ember-yearly-electricity"}


def check(cond: bool, name: str) -> None:
    global FAILS
    print(f"  [{'ok' if cond else 'FAIL'}] {name}")
    FAILS += not cond


print("== places carry their country code")
tree = copy_tree()
edit(tree / "places.yaml", lambda s: s.replace('    iso3: IDN\n', '', 1))
out = run_validate(tree)
check(out.returncode != 0 and "iso3" in out.stdout + out.stderr, "a place with no iso3 fails")

tree = copy_tree()
edit(tree / "places.yaml", lambda s: s.replace('iso3: IDN', 'iso3: idn', 1))
check(run_validate(tree).returncode != 0, "iso3 must be three capital letters")

tree = copy_tree()
edit(tree / "places.yaml", lambda s: s.replace('iso3: IDN', 'iso3: FRA', 1))
out = run_validate(tree)
check(out.returncode != 0 and "iso3" in out.stdout + out.stderr, "one country, two codes fails")

for key in ("country", "slug"):
    tree = copy_tree()
    edit(tree / "places.yaml", lambda s, key=key: s.replace(f'{key}: ', f'x{key}: ', 1))
    out = run_validate(tree)
    check(out.returncode != 0 and "[FAIL] places.yaml" in out.stdout and "Traceback" not in out.stderr,
          f"a place with no {key} fails with a line, not a traceback")

check(run_validate(copy_tree()).returncode == 0, "the real tree passes")
idx = build_in(copy_tree())
check(all(len(p.get("iso3", "")) == 3 for p in idx["places"]), "index.json places carry iso3")

print("== power systems")
def swapped(pts):
    return [[b, a] for a, b in pts]


CASES = [
    ("an open polygon",              lambda d: d["polygon"].pop(), "not closed"),
    ("a polygon of three points",    lambda d: d.__setitem__("polygon", d["polygon"][:3]), "too short"),
    ("an id that is not the file",   lambda d: d.__setitem__("id", "java"), "is not the file name"),
    ("estimated with no factors",    lambda d: d.pop("capacity_factors"), "needs `capacity_factors`"),
    ("a reading with a bad name",    lambda d: d.__setitem__("readings", ["R15"]), "does not match"),
    ("a source that does not exist", lambda d: d.__setitem__("sources", ["economic/community/nope"]),
     "economic/community/nope is not an entry in data/"),
    ("no attribution",               lambda d: d.pop("attribution"), "'attribution' is a required property"),
    ("an unknown key",               lambda d: d.__setitem__("colour", "blue"), "Additional properties"),
    ("national with a polygon",      lambda d: d.__setitem__("mix", {"kind": "national", "fossil_share": 0.5, "year": 2024}),
     "a national system needs `country`"),
    ("an open ring",                 lambda d: d["rings"]["city"].pop(), "not closed"),
    ("a list where a mapping goes",  lambda d: d.__setitem__("rings", []), "is not of type 'object'"),
    ("a polygon with lat and lon swapped", lambda d: d.__setitem__("polygon", swapped(d["polygon"])),
     "114.42 is greater than the maximum of 90"),
    ("a ring with lat and lon swapped", lambda d: d["rings"].__setitem__("city", swapped(d["rings"]["city"])),
     "is greater than the maximum of 90"),
    ("a hand-written id that is a country code", lambda d: d.__setitem__("id", "idn"),
     "is the code of a country"),
]
for name, change, why in CASES:
    tree = copy_tree(); p = tree / "systems/energy/bali.yaml"
    d = yaml.safe_load(p.read_text()); change(d)
    if d.get("id") == "idn":
        p = p.rename(p.with_name("idn.yaml"))
    p.write_text(yaml.safe_dump(d, allow_unicode=True))
    out = run_validate(tree)
    check(out.returncode != 0 and f"systems/energy/{p.name}" in out.stdout and why in out.stdout
          and "Traceback" not in out.stderr, f"systems: {name} fails, saying why")

NATIONAL = {"id": "idn", "name": "National electricity mix, Indonesia", "country": "IDN",
            "mix": {"kind": "national", "fossil_share": 0.84, "year": 2025},
            "readings": ["R2"], "attribution": ["Ember Yearly Electricity Data, CC BY 4.0"],
            "notes": "National fossil share of generation, as Ember publishes it."}
for name, change, ok, why in [
        ("a valid national system passes", lambda d: None, True, ""),
        ("a national system with no country fails", lambda d: d.pop("country"), False, "a national system needs `country`"),
        ("a national system with an unknown country fails", lambda d: d.__setitem__("country", "XXX"), False,
         "is no place's iso3"),
        ("a national system whose id is not its country fails", lambda d: d.__setitem__("id", "indonesia"), False,
         "must be its country in lower case")]:
    tree = copy_tree(); d = dict(NATIONAL); change(d)
    (tree / f"systems/energy/{d.get('id', 'idn')}.yaml").write_text(yaml.safe_dump(d, allow_unicode=True))
    out = run_validate(tree)
    check((out.returncode == 0) == ok and why in out.stdout and "Traceback" not in out.stderr, f"systems: {name}")

tree = copy_tree(); d = dict(NATIONAL); d["id"] = "indonesia"
(tree / "systems/energy/indonesia.yaml").write_text(yaml.safe_dump(d, allow_unicode=True))
out = run_validate(tree)
check(out.returncode != 0 and "must be its country in lower case" in out.stdout,
      "systems: two national files for one country fail")

# Rules the schema pattern pre-empts through the command line: call the pass with a readings table or an
# entry list that lacks one id.
fails, said = seen_by(validate.pass_systems, ALL_ENTRIES, {k: v for k, v in ALL_READINGS.items() if k != "R2"})
check(fails and "reading R2 is not in readings.yaml" in said, "systems: a reading missing from readings.yaml fails")
fails, said = seen_by(validate.pass_systems, set(), ALL_READINGS)
check(fails and "is not an entry in data/" in said, "systems: a source missing from data/ fails")

check(run_validate(copy_tree()).returncode == 0, "systems: the real tree passes")

print("== the national line")
sys.path.insert(0, str(ROOT / "scripts"))
import national_energy  # noqa: E402

HEADER = ("Area,ISO 3 code,Year,Area type,Electricity source,Is aggregated source,Generation (TWh),"
          "Generation YoY change (TWh),Generation YoY change (%),Share of generation (%),"
          "Share of generation YoY change (% points),Capacity (GW),Emissions (MtCO2e),"
          "Emissions YoY change (MtCO2e),Emissions YoY change (%),Share of emissions (%),"
          "Emissions intensity (gCO2e/kWh),Continent,Ember region,EU member,OECD member,G20 member,"
          "G7 member,ASEAN member")


def ember_row(area, iso, year, source, aggregated, share, kind="Country or economy"):
    cells = [area, iso, year, kind, source, aggregated, "1.0", "", "", share] + [""] * 14
    return ",".join(str(c) for c in cells)


fx = Path(tempfile.mkdtemp())
(fx / "t.csv").write_text("\n".join([
    HEADER,
    ember_row("Indonesia", "IDN", 2023, "Fossil", "True", "84.905"),
    ember_row("Indonesia", "IDN", 2024, "Fossil", "True", "80.0"),
    ember_row("Indonesia", "IDN", 2024, "Coal", "False", "50.0"),
    ember_row("Spain", "ESP", 2023, "Fossil", "True", "28.111"),
    ember_row("Spain", "ESP", 2024, "Fossil", "True", "23.2564"),
    ember_row("France", "FRA", 2024, "Fossil", "True", ""),
    ember_row("Zeroland", "ZZZ", 2024, "Fossil", "True", "0.0"),
    ember_row("ASEAN", "", 2024, "Fossil", "True", "70.0", kind="Region"),
]) + "\n", encoding="utf-8")
rows = national_energy.rows(fx / "t.csv")
check(rows["IDN"] == (2024, 0.8) and rows["ESP"] == (2024, 0.2326), "the latest year with a figure wins, as a share 0 to 1")
check(rows["ZZZ"] == (2024, 0.0), "a genuine zero share is kept as (year, 0.0)")
check("FRA" not in rows and "BTN" not in rows and "" not in rows, "no figure, no row: never a zero")
out = fx / "out"
written, skipped = national_energy.write(rows, {"IDN": "Indonesia", "ESP": "Spain", "FRA": "France", "BTN": "Bhutan", "ZZZ": "Zeroland"}, out)
check(sorted(written) == ["esp", "idn", "zzz"] and sorted(skipped) == ["BTN", "FRA"], "skipped countries are reported")
check(yaml.safe_load((out / "zzz.yaml").read_text())["mix"]["fossil_share"] == 0.0, "a genuine zero share is written")
check(national_energy.older(rows, ["idn", "esp", "zzz"]) == "older year: none"
      and national_energy.older({**rows, "ESP": (2023, 0.3)}, ["idn", "esp", "zzz"]) == "older year: ESP 2023",
      "the script names the countries whose year is older than the newest")
d = yaml.safe_load((out / "idn.yaml").read_text())
check(d["name"] == "National electricity mix, Indonesia" and d["notes"].startswith(
      "Share of electricity generation from fossil fuels in Indonesia, 2024, from Ember's"),
      "the national file's name and notes read as the Index words them")
check(d["mix"] == {"kind": "national", "fossil_share": 0.8, "year": 2024} and d["country"] == "IDN"
      and "polygon" not in d and d["readings"] == ["R2"], "a national system has a country and no polygon")
(out / "esp.yaml").write_text("id: esp\nmix: {kind: estimated, method: capacity-factors}\n")
written, skipped = national_energy.write(rows, {"ESP"}, out)
check(written == [] and skipped == ["ESP"] and "estimated" in (out / "esp.yaml").read_text(),
      "a file that is not national is never overwritten")

print("== place profiles")
PCASES = [
    # (name, change, the file the mutated profile is written to, the words of the rule it must trip)
    ("a place that is not in places.yaml", lambda d: d.__setitem__("place", "nowhere"), "nowhere",
     "place nowhere is not in places.yaml"),
    ("a fictional place",                  lambda d: d.__setitem__("place", "uqbar"), "uqbar",
     "profiles are for real places"),
    ("a place that is not the file name",  lambda d: d.__setitem__("place", "barcelona"), "bali",
     "is not the file name"),
    ("a system that does not exist",       lambda d: d["energy"].__setitem__("system", "nowhere"), "bali",
     "is not a system in systems/energy/"),
    ("a national system",                  lambda d: d["energy"].__setitem__("system", "idn"), "bali",
     "is a national system"),
    ("a repeated utility id",              lambda d: d["water"]["utilities"].append(dict(d["water"]["utilities"][0])), "bali",
     "repeats"),
    ("a reading with a bad name",          lambda d: d["water"]["utilities"][0].__setitem__("readings", ["R15"]), "bali",
     "does not match"),
    ("a source that does not exist",       lambda d: d["water"]["utilities"][0].__setitem__("sources", ["economic/community/nope"]), "bali",
     "economic/community/nope is not an entry in data/"),
    ("an open ring",                       lambda d: d["energy"].__setitem__("rings", {"city": [[0, 0], [1, 0], [1, 1], [0, 1]]}), "bali",
     "not closed"),
    ("a ring with lat and lon swapped",    lambda d: d["energy"].__setitem__("rings", {"city": swapped([[115.08, -8.55], [115.28, -8.55], [115.28, -8.86], [115.08, -8.55]])}), "bali",
     "115.08 is greater than the maximum of 90"),
    ("neither energy nor water",           lambda d: (d.pop("energy"), d.pop("water")), "bali", "is not valid under any of the given schemas"),
    ("a utility of no kind",               lambda d: d["water"]["utilities"][0].pop("kind"), "bali", "'kind' is a required property"),
    ("an unknown key",                     lambda d: d.__setitem__("colour", "blue"), "bali", "Additional properties"),
]
for name, change, fname, why in PCASES:
    tree = copy_tree(); p = tree / "profiles/bali.yaml"
    (tree / "systems/energy/idn.yaml").write_text(yaml.safe_dump(NATIONAL, allow_unicode=True))
    d = yaml.safe_load(p.read_text()); change(d)
    if fname != "bali":
        p.unlink(); p = p.with_name(f"{fname}.yaml")
    p.write_text(yaml.safe_dump(d, allow_unicode=True))
    out = run_validate(tree)
    check(out.returncode != 0 and f"profiles/{fname}.yaml" in out.stdout and why in out.stdout
          and "Traceback" not in out.stderr, f"profiles: {name} fails, saying why")

fails, said = seen_by(validate.pass_profiles, {}, ALL_ENTRIES, {k: v for k, v in ALL_READINGS.items() if k not in ("R10", "R11")})
check(fails and "reading R10 is not in readings.yaml" in said, "profiles: a reading missing from readings.yaml fails")

check(run_validate(copy_tree()).returncode == 0, "profiles: the real tree passes")

print("== index.json carries systems and profiles")
idx = build_in(copy_tree())
ids = [s["id"] for s in idx["systems"]["energy"]]
check({"bali", "balearic", "idn"} <= set(ids), "systems.energy holds bali, balearic and idn")
hand = [s["id"] for s in idx["systems"]["energy"] if s["mix"]["kind"] != "national"]
check(ids[:len(hand)] == sorted(hand) and ids[len(hand):] == sorted(ids[len(hand):]),
      "hand-written systems first, then national, each sorted by id")
check(idx["profiles"][0]["place"] == "bali", "profiles[0] is bali")
check(all(k in idx for k in "generated source note counts entries cells coverage readings places observations fictional".split()),
      "every earlier top-level key is still there")
check(list(idx["counts"]) == ["entries", "cells", "places_served", "reviews"], "counts keeps its keys")
check("systems/" in idx["note"] and "profiles/" in idx["note"], "the note names systems/ and profiles/")

if FAILS:
    print(f"\n{FAILS} check(s) failed.", file=sys.stderr)
    sys.exit(1)
print("\nall passed.")
