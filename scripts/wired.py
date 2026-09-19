#!/usr/bin/env python3
"""Check `wired_in_planetai` against what the node repo actually declares.

    python scripts/wired.py              # report
    python scripts/wired.py --check      # exit 1 if a pack reads a source this list calls unwired

`wired_in_planetai` is typed by hand, and a hand-typed claim about another repository drifts the
moment either side moves. The node declares what it reads: every `packs/*/pack.yaml` there carries
`sources: [<pillar>/<scale>/<slug>, ...]`, the same ids this list files its entries under. That is
checkable, and this checks it.

**Two directions, and only one of them is an error.**

- A pack declares a source and the entry says `wired_in_planetai: false` (or says nothing). That is
  this list being wrong about a fact it can see, and `--check` fails on it.
- An entry says `true` and no pack declares it. That is *reported, not failed*, because this script
  cannot see the other half of the node — `config/channels.yml` and `app/bootstrap.py` read sources
  (AirGradient, PurpleAir, Smart Citizen, NASA POWER, CAMS) without naming a registry id anywhere —
  and it cannot see the Index side at all. Some of those flags are probably right.

That second list is the open question rather than a bug: **what does `wired_in_planetai` mean?** A
node pack only, or anything downstream of this registry including index.fab.city? Until that is
answered, the field is two claims wearing one name. Answer it, then this script can fail on both
directions, or the field can split in two.

The node repo is a sibling checkout and is absent in CI unless the workflow checks it out; without
it this prints one line and exits 0. Point it somewhere else with PLANETAI_NODE_REPO.
"""
from __future__ import annotations

import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
NODE = Path(os.environ.get("PLANETAI_NODE_REPO", ROOT.parent / "planetai-node"))
REF = "origin/main"


def git(repo: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True, timeout=10)


def node_declares() -> tuple[set[str], str]:
    """Every id named by a `sources:` line in the node's packs, read from its published main rather
    than from whatever branch the checkout happens to be on."""
    ids: set[str] = set()
    ls = git(NODE, "ls-tree", "-r", "--name-only", REF, "packs")
    if ls.returncode == 0 and ls.stdout.strip():
        at = git(NODE, "log", "-1", "--format=%h %cs", REF).stdout.strip()
        for path in (n for n in ls.stdout.split() if n.endswith("pack.yaml")):
            text = git(NODE, "show", f"{REF}:{path}").stdout
            m = re.search(r"^sources:\s*\[(.*?)\]", text, re.M | re.S)
            if m:
                ids |= {s.strip() for s in m.group(1).split(",") if s.strip()}
        return ids, f"{REF} @ {at}"
    for p in sorted(NODE.glob("packs/*/pack.yaml")):
        m = re.search(r"^sources:\s*\[(.*?)\]", p.read_text(), re.M | re.S)
        if m:
            ids |= {s.strip() for s in m.group(1).split(",") if s.strip()}
    return ids, "working tree"


def flagged() -> set[str]:
    """Entries claiming a wiring. Read as text: the file is one flat mapping and this is one key."""
    out = set()
    for p in sorted((ROOT / "data").rglob("*.yaml")):
        if re.search(r"^wired_in_planetai:\s*true\s*$", p.read_text(), re.M):
            out.add(str(p.relative_to(ROOT / "data"))[: -len(".yaml")])
    return out


def main(argv: list[str]) -> int:
    if not (NODE / "packs").is_dir() and git(NODE, "rev-parse", "--git-dir").returncode != 0:
        print(f"  - wired check skipped ({NODE} is not here; it is a sibling checkout, not a dependency)")
        return 0

    declared, at = node_declares()
    claims = flagged()
    missing = sorted(declared - claims)          # a pack reads it; this list does not say so
    unbacked = sorted(claims - declared)         # this list says so; no pack declares it

    print(f"  {len(declared)} sources declared by node packs ({at}); {len(claims)} entries flagged wired")

    if missing:
        print(f"  x {len(missing)} entr{'y' if len(missing) == 1 else 'ies'} a pack reads and this list calls unwired:")
        for i in missing:
            print(f"      data/{i}.yaml — set wired_in_planetai: true")

    if unbacked:
        print(f"  · {len(unbacked)} flagged wired with no pack declaring them. Not an error: the node also reads")
        print("    sources through config/channels.yml and app/bootstrap.py without naming a registry id,")
        print("    and the Index is not visible from here. See the header — the word needs a definition.")
        for i in unbacked:
            print(f"      data/{i}.yaml")

    return 1 if (missing and "--check" in argv) else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
