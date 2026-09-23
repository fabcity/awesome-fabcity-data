#!/usr/bin/env python3
"""Check `adapter` against what the node repo actually declares.

    python scripts/wired.py              # report
    python scripts/wired.py --check      # exit 1 if a pack reads a source no adapter names

The node declares what it reads: every `packs/*/pack.yaml` there carries
`sources: [<pillar>/<scale>/<slug>, ...]`, the same ids this list files its entries under. That is
checkable, and this checks it in both directions, which is the whole argument for `adapter`.

- A pack declares a source and no entry here names an `adapter` for it. This list is wrong about a
  fact it can see, and `--check` fails.
- An `adapter` names something the node does not have: `pack:<id>` with no such directory, or
  `core:<fn>` with no such function in `app/sources.py` or `app/bootstrap.py`. Also a failure. A
  pointer whose whole justification is that it can be dereferenced has to be dereferenced.

This replaced `wired_in_planetai`, retired 2026-09-23. That was a boolean typed in this repository
asserting runtime state in another one, and it drifted exactly as such a claim does. At the end it
read 26 true, of which 12 had no pack declaring them and no adapter naming anything, unverifiable
in either direction. The field was two claims wearing one name, node pack or anything downstream
including index.fab.city, and nothing ever answered which. `adapter` answers one question and can
be checked on both sides.

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


def node_offers() -> tuple[set[str], set[str]]:
    """What `adapter:` is allowed to name: every pack directory under packs/, and every top-level
    function in app/sources.py and app/bootstrap.py. Read from the node's published main, same as
    node_declares(), so a laptop's half-finished branch cannot make this pass or fail."""
    packs: set[str] = set()
    funcs: set[str] = set()
    ls = git(NODE, "ls-tree", "-r", "--name-only", REF, "packs")
    if ls.returncode == 0 and ls.stdout.strip():
        packs = {n.split("/")[1] for n in ls.stdout.split() if n.startswith("packs/") and "/" in n[6:]}
        for mod in ("app/sources.py", "app/bootstrap.py"):
            funcs |= set(re.findall(r"^def ([a-z_]+)\(", git(NODE, "show", f"{REF}:{mod}").stdout, re.M))
    else:
        packs = {d.name for d in sorted(NODE.glob("packs/*")) if d.is_dir()}
        for mod in ("app/sources.py", "app/bootstrap.py"):
            f = NODE / mod
            if f.exists():
                funcs |= set(re.findall(r"^def ([a-z_]+)\(", f.read_text(), re.M))
    return packs, {f for f in funcs if not f.startswith("_")}


def adapters() -> dict[str, str]:
    """Every entry's `adapter:` value, keyed by registry id. Read as text, one flat key per file."""
    out = {}
    for p in sorted((ROOT / "data").rglob("*.yaml")):
        m = re.search(r"^adapter:\s*[\"']?([a-z_:0-9-]+)[\"']?\s*$", p.read_text(), re.M)
        if m:
            out[str(p.relative_to(ROOT / "data"))[: -len(".yaml")]] = m.group(1)
    return out


def main(argv: list[str]) -> int:
    if not (NODE / "packs").is_dir() and git(NODE, "rev-parse", "--git-dir").returncode != 0:
        print(f"  - wired check skipped ({NODE} is not here; it is a sibling checkout, not a dependency)")
        return 0

    declared, at = node_declares()
    ad = adapters()
    missing = sorted(declared - set(ad))  # a pack reads it and no adapter here names anything

    print(f"  {len(declared)} sources declared by node packs ({at}); {len(ad)} entries name an adapter")

    if missing:
        print(f"  x {len(missing)} entr{'y' if len(missing) == 1 else 'ies'} a pack reads and no adapter names:")
        for i in missing:
            print(f"      data/{i}.yaml — name what reads it: adapter: pack:<id> (CONTRIBUTING 2b)")

    # `adapter` is the replacement for that boolean, and its whole justification is that a pointer can be
    # dereferenced. So dereference it: pack:<id> must be a directory under packs/, core:<fn> a function in
    # app/sources.py or app/bootstrap.py. Both directions are errors — there is no second half this cannot see.
    packs, funcs = node_offers()
    dangling = []
    for rid, a in sorted(ad.items()):
        kind, _, name = a.partition(":")
        known = packs if kind == "pack" else funcs
        if known and name not in known:
            dangling.append((rid, a, "no such pack" if kind == "pack" else "no such function"))

    if dangling:
        print(f"  x {len(dangling)} adapter{'' if len(dangling) == 1 else 's'} naming something the node does not have:")
        for rid, a, why in dangling:
            print(f"      data/{rid}.yaml — adapter: {a} ({why} on {at})")
    elif ad:
        print(f"  {len(ad)} adapters all resolve in the node ({at})")

    return 1 if ((missing or dangling) and "--check" in argv) else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
