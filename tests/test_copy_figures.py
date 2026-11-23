#!/usr/bin/env python3
"""The one-way copy's tests. Run from repo root:

    python tests/test_copy_figures.py

Every record is built here, in Airtable's REST shape and keyed by field name, so nothing reaches
Airtable or GitHub. Every file the copy produces is also checked against
schema/observation.schema.json: a test that passes on a document the schema would refuse still fails.
Not pytest, for the reason tests/test_schema.py gives.
"""
import json
import sys
import tempfile
from pathlib import Path

import jsonschema
import yaml

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import copy_figures as cf  # noqa: E402
import source_from_issue as sfi  # noqa: E402
from sync_airtable import build_readings  # noqa: E402
from validate import _coerce_dates, candidate_needs_notes  # noqa: E402

PLACES = {"bali", "barcelona"}
FICTIONAL = {"uqbar"}
READINGS = {r["id"]: r for r in yaml.safe_load((ROOT / "readings.yaml").read_text(encoding="utf-8"))["readings"]}
OBSERVATION = jsonschema.Draft202012Validator(
    json.loads((ROOT / "schema" / "observation.schema.json").read_text(encoding="utf-8")))
DATASET = jsonschema.Draft202012Validator(
    json.loads((ROOT / "schema" / "dataset.schema.json").read_text(encoding="utf-8")))
BALI = "observations/bali/R1.yaml"


def rec(created="2027-01-10T08:00:00.000Z", rid="recA", **fields):
    """One `City figures` row as the REST API returns it. A field set to None is left out, the way
    Airtable leaves out an empty cell."""
    f = {"place": "bali", "reading": ["recXEOmoelK9Vtm20"], "reading_id": ["R1"], "year": 2025,
         "value": 412.5, "unit": "t/yr", "source_url": "https://data.example.org/waste",
         "source_name": "Bali waste statistics", "terms": "CC-BY-4.0", "sent_by": "Ana Pérez",
         "sent_by_role": "head of the waste department", "may_publish": "yes", "state": "sent"}
    f.update(fields)
    return {"id": rid, "createdTime": created, "fields": {k: v for k, v in f.items() if v is not None}}


def copy(*records):
    docs, skips = cf.to_observations(list(records), PLACES, FICTIONAL, set(READINGS))
    for path, doc in docs.items():
        errs = [e.message for e in OBSERVATION.iter_errors(doc)]
        assert not errs, f"{path} fails the observation schema: {errs}"
    return docs, skips


def only_figure(docs):
    assert list(docs) == [BALI], list(docs)
    assert len(docs[BALI]["figures"]) == 1, docs[BALI]["figures"]
    return docs[BALI]["figures"][0]


# --- the brief's cases --------------------------------------------------------------------------
def test_published_figure_is_candidate():
    docs, skips = copy(rec())
    fig = only_figure(docs)
    assert (fig["state"], fig["value"], fig["sent_on"]) == ("candidate", 412.5, "2027-01-10"), fig
    assert skips == [], skips
    text = cf.render(docs[BALI])
    # Ruling 9: the role is public, the person's name stays in Airtable.
    assert "Ana" not in text and "sent_by:" not in text, text
    assert "sent_by_role: head of the waste department" in text, text


def test_ask_is_held():
    fig = only_figure(copy(rec(may_publish="ask"))[0])
    assert fig["state"] == "held" and "value" not in fig, fig
    assert "source_url" not in fig and "terms" not in fig, fig


def test_not_held_has_no_value():
    fig = only_figure(copy(rec(not_held=True, value=None, source_url=None, source_name=None))[0])
    assert fig["state"] == "not-held" and "value" not in fig, fig


def test_later_figure_replaces_earlier():
    early = rec(created="2027-01-10T08:00:00.000Z", rid="recA", value=400)
    late = rec(created="2027-02-01T08:00:00.000Z", rid="recB", value=412.5)
    for order in ((early, late), (late, early)):
        fig = only_figure(copy(*order)[0])
        assert (fig["value"], fig["sent_on"]) == (412.5, "2027-02-01"), fig


def test_unknown_place_is_skipped():
    docs, skips = copy(rec(place="atlantis"))
    assert docs == {}, docs
    assert len(skips) == 1 and "atlantis" in skips[0], skips


def test_contact_details_refused():
    for bad in (rec(sent_by_role="lead, ana@example.org"), rec(sent_by="Ana +62 812 3456 7890")):
        docs, skips = copy(bad)
        assert docs == {}, docs
        assert len(skips) == 1, skips
        # The reason is printed in a public workflow log, so it never repeats what was typed.
        assert "example.org" not in skips[0] and "3456" not in skips[0], skips


def test_checked_is_live():
    fig = only_figure(copy(rec(state="checked", checked_by="Fab City data team", checked_on="2027-02-03"))[0])
    assert fig["state"] == "live", fig
    assert (fig["checked_by"], fig["checked_on"]) == ("Fab City data team", "2027-02-03"), fig


def test_fictional_files_no_source():
    uqbar = rec(place="uqbar", fictional=True, sent_by_role="invented, for the demonstration")
    docs, skips = copy(uqbar)
    assert list(docs) == ["observations/uqbar/R1.yaml"] and skips == [], (docs, skips)
    assert docs["observations/uqbar/R1.yaml"]["fictional"] is True
    assert cf.source_issue(uqbar, READINGS["R1"]) is None


def parse_issue(body):
    """source_from_issue's own build, on a temp tree, against the real places.yaml."""
    real = sfi.ROOT, sfi.DATA_DIR, sfi.PLACES
    with tempfile.TemporaryDirectory() as td:
        try:
            sfi.ROOT, sfi.DATA_DIR, sfi.PLACES = Path(td), Path(td) / "data", ROOT / "places.yaml"
            code, out = sfi.build(body, 900, "2027-01-10")
            text = (Path(td) / out["entry_path"]).read_text(encoding="utf-8") if code == 0 else ""
        finally:
            sfi.ROOT, sfi.DATA_DIR, sfi.PLACES = real
    return code, out, text


def test_source_issue_parses():
    title, body = cf.source_issue(rec(), READINGS["R1"])
    code, out, text = parse_issue(body)
    assert code == 0, out
    assert title == f"source: {out['entry']}", (title, out["entry"])
    entry = _coerce_dates(yaml.safe_load(text))
    errs = [e.message for e in DATASET.iter_errors(entry)]
    assert not errs, errs
    assert candidate_needs_notes(entry) is None
    assert (entry["status"], entry["places"], entry["url"]) == (
        "candidate", ["bali"], "https://data.example.org/waste"), entry
    notes = " ".join(entry["notes"].split()).lower()
    assert "filed from a figure sent through index.fab.city" in notes, notes
    assert "not yet verified by the fab city team" in notes, notes
    assert "Ana" not in body, body


# --- the controller's rulings -------------------------------------------------------------------
def test_needs_a_fix_is_not_written_and_removed():
    """Ruling 1: an earlier run wrote the figure, then the team marked it `needs a fix`."""
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        docs, _ = copy(rec())
        assert cf.apply(docs, root, write=True) == ([BALI], [], [])
        docs, skips = copy(rec(state="needs a fix"))
        assert docs == {} and len(skips) == 1 and "needs a fix" in skips[0], (docs, skips)
        assert cf.apply(docs, root, write=True) == ([], [], [BALI])
        assert not (root / BALI).exists() and not (root / BALI).parent.exists()


def test_rerun_writes_nothing():
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        docs, _ = copy(rec(), rec(rid="recB", year=2024, value=398))
        cf.apply(docs, root, write=True)
        assert cf.apply(copy(rec(rid="recB", year=2024, value=398), rec())[0], root, write=True) == ([], [], [])


def test_empty_state_is_sent():
    """Ruling 3: the form leaves `state` empty."""
    assert copy(rec(state=None)) == copy(rec(state="sent"))
    assert only_figure(copy(rec(state=None))[0])["state"] == "candidate"


def test_cited_figure_tag():
    """Ruling 4: terms that are not a known open licence tag the source `cited-figure`."""
    tags = lambda terms: sfi.csv(sfi.parse_body(cf.source_issue(rec(terms=terms), READINGS["R1"])[1])["Tags"])
    assert tags("© the statistics office of Bali, reuse with attribution") == ["city-sent", "reading-R1", "cited-figure"]
    assert tags("CC BY 4.0") == ["city-sent", "reading-R1"]
    assert tags("Open Government Licence v3.0") == ["city-sent", "reading-R1"]
    code, out, _ = parse_issue(cf.source_issue(rec(terms="reuse with attribution"), READINGS["R1"])[1])
    assert code == 0, out


def test_no_source_is_skipped():
    """Ruling 7: a value with neither a link nor a name for its source is not written."""
    docs, skips = copy(rec(source_url=None, source_name=None))
    assert docs == {} and len(skips) == 1 and "no source" in skips[0], (docs, skips)
    # A named document with no link is a source; it is written, and there is nothing to file.
    named = rec(source_url=None)
    assert only_figure(copy(named)[0])["source_name"] == "Bali waste statistics"
    assert cf.source_issue(named, READINGS["R1"]) is None


def test_fictional_checkbox_must_match_place():
    """Ruling 8: the place decides; a checkbox that disagrees skips the record."""
    for bad in (rec(fictional=True), rec(place="uqbar")):
        docs, skips = copy(bad)
        assert docs == {} and len(skips) == 1 and "fictional" in skips[0], (docs, skips)


def test_reading_is_the_lookup_not_the_link():
    docs, _ = copy(rec(reading=["recR13xxxxxxxxxxx"], reading_id=["R1"]))
    assert list(docs) == [BALI], docs
    docs, skips = copy(rec(reading_id=None))
    assert docs == {} and len(skips) == 1, (docs, skips)


def test_build_readings():
    rows = build_readings()
    assert [r["id"] for r in rows] == [f"R{i}" for i in range(1, 15)], rows
    keys = {"id", "name", "plain", "unit", "years", "held_by", "tests", "cells", "last_synced"}
    for r in rows:
        assert set(r) == keys, r
        assert all(isinstance(v, str) and v for v in r.values()), r
    assert rows[0]["years"] == "2023, 2024, 2025" and rows[0]["cells"] == "Environmental|City", rows[0]


if __name__ == "__main__":
    failed = 0
    for name, fn in [(n, f) for n, f in globals().items() if n.startswith("test_") and callable(f)]:
        try:
            fn()
            print(f"[ ok ] {name}")
        except Exception as ex:  # noqa: BLE001 - every failure is reported, then the run fails
            failed += 1
            print(f"[FAIL] {name}: {type(ex).__name__}: {ex}")
    print(f"\ntest_copy_figures: {failed} failed.")
    sys.exit(1 if failed else 0)
