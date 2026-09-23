#!/usr/bin/env python3
"""Ask every entry's `url` and `api` whether it still answers, and say what came back.

    python3 scripts/linkcheck.py                 # markdown report on stdout
    python3 scripts/linkcheck.py --json out.json # the same as data
    python3 scripts/linkcheck.py --only status=live

`status: live` is a claim this list makes on somebody else's behalf, and entries decay — CONTRIBUTING
says so and asks for a PR when they do. Since `planetai-node` began vendoring this registry as a pinned
snapshot that ships in its tarball, a stale `live` is a promise a household's node makes too.

**This reports; it does not judge.** A 403 from Cloudflare is not a dead source, it is a bot check, and
plenty of live government portals answer 403 to anything without a browser. The categories below keep
those apart, and only `gone` and `dns` are safe to act on without a person looking.

Polite by construction: one worker per host at a time, a real User-Agent that says who is asking and
why, HEAD before GET, a Range header so a GET fetches a kilobyte rather than a dataset, and a pause
between requests to the same host.
"""
from __future__ import annotations

import argparse
import collections
import concurrent.futures as cf
import datetime as dt
import json
import re
import threading
import time
import urllib.error
import urllib.request
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
# ASCII only: urllib encodes headers as latin-1, and an em dash here made every request fail before
# it was sent. Client-side, so nobody was troubled by it, but nothing was checked either.
UA = ("awesome-fabcity-data linkcheck (+https://github.com/fabcity/awesome-fabcity-data) "
      "- verifying our own catalogue entries, low volume, occasional")
TIMEOUT = 20
PAUSE = 1.0                     # seconds between two requests to the same host

_host_locks: dict[str, threading.Lock] = {}
_locks_guard = threading.Lock()


def host_of(u: str) -> str:
    m = re.match(r"https?://([^/]+)", u or "")
    return m.group(1).lower() if m else ""


def lock_for(host: str) -> threading.Lock:
    with _locks_guard:
        return _host_locks.setdefault(host, threading.Lock())


def classify(code: int | None, err: str) -> str:
    if code is None:
        if "NameResolution" in err or "getaddrinfo" in err or "Name or service" in err:
            return "dns"
        return "unreachable"
    if 200 <= code < 300:
        return "ok"
    if code in (301, 302, 303, 307, 308):
        return "redirect"
    if code in (401, 403):
        return "blocked"       # a bot check or a login wall, not evidence of death
    if code == 404 or code == 410:
        return "gone"
    if code == 429:
        return "ratelimited"
    if 500 <= code:
        return "server-error"  # theirs, today; says nothing about the entry
    return f"http-{code}"


def ask(url: str) -> dict:
    """HEAD, then GET a kilobyte if HEAD is refused. Returns what happened, never raises."""
    host = host_of(url)
    if not host:
        return {"url": url, "verdict": "not-a-url", "code": None, "final": None}
    with lock_for(host):
        out = _one(url, "HEAD")
        if out["verdict"] in ("blocked", "unreachable") or out["code"] in (405, 501):
            time.sleep(PAUSE)
            out = _one(url, "GET")
        time.sleep(PAUSE)
    return out


def _one(url: str, method: str) -> dict:
    req = urllib.request.Request(url, method=method, headers={
        "User-Agent": UA, "Accept": "*/*", **({"Range": "bytes=0-1023"} if method == "GET" else {})})
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
            final = r.geturl()
            return {"url": url, "code": r.status, "final": final if final != url else None,
                    "verdict": "redirect-followed" if final != url and host_of(final) != host_of(url)
                               else classify(r.status, ""), "method": method}
    except urllib.error.HTTPError as e:
        return {"url": url, "code": e.code, "final": None, "verdict": classify(e.code, ""), "method": method}
    except Exception as e:                                  # noqa: BLE001 — every failure is a result here
        return {"url": url, "code": None, "final": None,
                "verdict": classify(None, f"{type(e).__name__}: {e}"), "method": method,
                "error": f"{type(e).__name__}: {e}"[:120]}


def entries(only: str | None) -> list[dict]:
    rows = []
    for p in sorted((ROOT / "data").rglob("*.yaml")):
        d = yaml.safe_load(p.read_text()) or {}
        if only:
            k, _, v = only.partition("=")
            if str(d.get(k, "")) != v:
                continue
        rows.append({"id": str(p.relative_to(ROOT / "data"))[:-len(".yaml")],
                     "name": d.get("name", ""), "status": d.get("status", ""),
                     "url": d.get("url"), "api": d.get("api"),
                     "adapter": d.get("adapter")})
    return rows


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--json"); ap.add_argument("--only"); ap.add_argument("--workers", type=int, default=8)
    a = ap.parse_args()

    rows = entries(a.only)
    targets = []
    for r in rows:
        for field in ("url", "api"):
            u = r.get(field)
            if isinstance(u, str) and u.startswith("http"):
                targets.append((r["id"], field, u))

    results: dict[tuple[str, str], dict] = {}
    with cf.ThreadPoolExecutor(max_workers=a.workers) as ex:
        futs = {ex.submit(ask, u): (i, f) for i, f, u in targets}
        for n, fut in enumerate(cf.as_completed(futs), 1):
            results[futs[fut]] = fut.result()
            if n % 25 == 0:
                print(f"  … {n}/{len(targets)}", flush=True)

    by_id = collections.defaultdict(dict)
    for (i, f), res in results.items():
        by_id[i][f] = res

    report = {"at": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
              "checked": len(targets), "entries": len(rows),
              "rows": [{**r, "checks": by_id.get(r["id"], {})} for r in rows]}
    if a.json:
        Path(a.json).write_text(json.dumps(report, indent=2))

    tally = collections.Counter()
    for r in report["rows"]:
        for f, res in r["checks"].items():
            tally[res["verdict"]] += 1
    print("\n## verdicts")
    for k, v in tally.most_common():
        print(f"  {v:4d}  {k}")

    for want in ("gone", "dns", "unreachable", "ratelimited", "server-error", "redirect-followed"):
        hits = [(r, f, res) for r in report["rows"] for f, res in r["checks"].items() if res["verdict"] == want]
        if not hits:
            continue
        print(f"\n## {want} ({len(hits)})")
        for r, f, res in sorted(hits, key=lambda h: h[0]["id"]):
            flag = f" ⚑{r['adapter']}" if r["adapter"] else ""
            extra = f" → {res['final']}" if res.get("final") else (f"  {res.get('error','')}" if res.get("error") else "")
            print(f"  {r['id']}  [{r['status']}]{flag}\n      {f}: {res['url']}{extra}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
