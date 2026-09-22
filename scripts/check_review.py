#!/usr/bin/env python3
"""Reviews decay. This says which ones have.

    python scripts/check_review.py              # report; exit 1 if any review is past 730 days
    python scripts/check_review.py --selftest   # the threshold arithmetic, asserted

A review is evidence about a source at a moment: somebody read it, for a named territory, and
said it was usable. Sources move — the Seoul portals put up a termination notice without changing
a status code, and `data.gov` paths migrate quietly. A reading from 2024 is not a claim about
today, and the way this list has failed before is by letting a claim outlive the reading behind it.

    newest usable review   < 365 days   nothing to say
                           > 365 days   warn — somebody should read it again
                           > 730 days   FAIL — the claim has outlived its evidence

On a failure it prints the exact `status:` line to flip back to `candidate`, with the file and the
line number, because the remedy is one text substitution and a person should not have to find it.
The flip is not done here: no script in this repository edits an entry file.

**What is skipped, and why.** An entry with an `adapter` and no review is not this script's
business at all — the adapter is the evidence, and scripts/wired.py already fails if it names a
pack or a function the node does not have. An entry with an adapter *and* a decayed review is
warned about but never failed: it stands on the code leg of `live` regardless of the review, so
telling anyone to flip it to `candidate` would be wrong advice. Entries with no evidence of either
kind are the join in scripts/validate.py, not this.
"""
from __future__ import annotations

import datetime as _dt
import sys
from pathlib import Path

import yaml

from validate import USABLE  # same repo, same word for what makes an entry live

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
REVIEWS_DIR = ROOT / "reviews"

WARN_DAYS = 365
FAIL_DAYS = 730


def age_verdict(days: int) -> str:
    """ok below the warn line, warn above it, fail above the fail line. Strictly greater on both:
    a review on the day it turns 365 is not yet a year stale."""
    if days > FAIL_DAYS:
        return "fail"
    if days > WARN_DAYS:
        return "warn"
    return "ok"


def _date(value) -> _dt.date | None:
    if isinstance(value, _dt.datetime):
        return value.date()
    if isinstance(value, _dt.date):
        return value
    try:
        return _dt.date.fromisoformat(str(value))
    except ValueError:
        return None


def newest_usable(rid: str):
    """The newest review of this entry whose verdict supports `live`. An `unusable` review is not
    evidence for a live status, so it does not stop the clock; it is a person's business, and the
    join in validate.py is what notices an entry whose only review says it does not work."""
    best = None
    for path in sorted((REVIEWS_DIR / rid).glob("*.yaml")):
        review = yaml.safe_load(path.read_text(encoding="utf-8"))
        if not isinstance(review, dict) or review.get("verdict") not in USABLE:
            continue
        when = _date(review.get("date"))
        if when and (best is None or when > best[0]):
            best = (when, review, path)
    return best


def status_line(path: Path) -> tuple[int, str]:
    """The entry's `status:` line, verbatim, with its 1-indexed line number — so the remedy can be
    printed as the substitution it is."""
    for n, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if line.startswith("status:"):
            return n, line
    return 0, "status: live"


def selftest() -> int:
    assert age_verdict(0) == "ok"
    assert age_verdict(WARN_DAYS) == "ok", "365 days exactly is not yet stale"
    assert age_verdict(WARN_DAYS + 1) == "warn"
    assert age_verdict(FAIL_DAYS) == "warn", "730 days exactly warns, does not fail"
    assert age_verdict(FAIL_DAYS + 1) == "fail"
    assert age_verdict(10_000) == "fail"
    print("age_verdict: 6 assertions, all hold "
          f"(warn past {WARN_DAYS} days, fail past {FAIL_DAYS})")
    return 0


def main(argv: list[str]) -> int:
    if "--selftest" in argv:
        return selftest()

    today = _dt.date.today()
    warns, fails, checked = [], [], 0

    for path in sorted(DATA_DIR.rglob("*.yaml")):
        entry = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        if entry.get("status") != "live":
            continue
        rid = path.relative_to(DATA_DIR).with_suffix("").as_posix()
        best = newest_usable(rid)
        if best is None:
            continue          # no review: the adapter's job, or the join's. Not this script's.
        checked += 1
        when, review, rpath = best
        days = (today - when).days
        verdict = age_verdict(days)
        if verdict == "ok":
            continue
        row = (rid, path, rpath, review, when, days)
        # An adapter holds the entry up on its own, so a decayed review is a warning there and
        # never a failure — flipping a source the node reads to `candidate` would be a lie.
        fails.append(row) if verdict == "fail" and not entry.get("adapter") else warns.append(row)

    print(f"{checked} live entr{'y carries' if checked == 1 else 'ies carry'} a usable review; "
          f"{len(warns)} past {WARN_DAYS} days, {len(fails)} past {FAIL_DAYS}.")

    for rid, path, rpath, review, when, days in warns:
        print(f"\n  · data/{rid}.yaml — newest usable review is {days} days old "
              f"({when}, {review['by']}, {review['org']}, for {review['territory']})")
        print(f"    {rpath.relative_to(ROOT).as_posix()} — read it again, or let it decay one more year")

    for rid, path, rpath, review, when, days in fails:
        n, line = status_line(path)
        print(f"\n  x data/{rid}.yaml — newest usable review is {days} days old "
              f"({when}, {review['by']}, {review['org']}, for {review['territory']}). "
              f"The claim has outlived its evidence.")
        print(f"    data/{rid}.yaml:{n}")
        print(f"      - {line}")
        print(f"      + status: candidate")
        print(f"    Then say in `notes` that the {when} review has expired, or open a "
              f"source-review issue and let a fresh reading put it back.")

    if fails:
        print(f"\n{len(fails)} entr{'y' if len(fails) == 1 else 'ies'} claim `live` on a review "
              f"older than {FAIL_DAYS} days.", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
