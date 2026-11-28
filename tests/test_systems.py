#!/usr/bin/env python3
"""Tests for the places' country codes, and (in later tasks) national systems and place profiles.
Run from repo root:

    python tests/test_systems.py

Plain script, no pytest, like tests/test_schema.py: a temp copy of the tree, a real subprocess run of
scripts/validate.py or scripts/build_index.py, because what is asserted is what CI does.
"""
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FAILS = 0


def copy_tree() -> Path:
    """A copy of the repository without .git, in a fresh temp dir."""
    dst = Path(tempfile.mkdtemp()) / "tree"
    shutil.copytree(ROOT, dst, ignore=shutil.ignore_patterns(".git", ".superpowers", "__pycache__"))
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

check(run_validate(copy_tree()).returncode == 0, "the real tree passes")
idx = build_in(copy_tree())
check(all(len(p.get("iso3", "")) == 3 for p in idx["places"]), "index.json places carry iso3")

if FAILS:
    print(f"\n{FAILS} check(s) failed.", file=sys.stderr)
    sys.exit(1)
print("\nall passed.")
