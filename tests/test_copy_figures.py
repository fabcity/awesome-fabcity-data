#!/usr/bin/env python3
"""The one-way copy's tests. Run from repo root:

    python tests/test_copy_figures.py

Every record is built here, in Airtable's REST shape and keyed by field name, so nothing reaches
Airtable or GitHub. Every file the copy produces is also checked against
schema/observation.schema.json: a test that passes on a document the schema would refuse still fails.
Not pytest, for the reason tests/test_schema.py gives.
"""
import contextlib
import io
import json
import re
import shutil
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


def test_not_held_without_consent_is_held():
    """Ruling: "we do not hold it" is itself an answer the city has not released."""
    for consent in ("no", "ask", None):
        fig = only_figure(copy(rec(not_held=True, may_publish=consent, value=None))[0])
        assert fig["state"] == "held" and "value" not in fig and "terms" not in fig, (consent, fig)
        assert "source_url" not in fig and "source_name" not in fig, (consent, fig)


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


def test_contact_in_terms_refused():
    """An email or phone number in any published text field refuses the record, and is never repeated."""
    bad = rec(terms="Reuse allowed; ask ana.perez@city.go.id or +62 812 3456 7890")
    docs, skips = copy(bad)
    assert docs == {} and len(skips) == 1 and "`terms`" in skips[0], (docs, skips)
    assert "ana.perez" not in skips[0] and "3456" not in skips[0], skips
    assert cf.source_issue(bad, READINGS["R1"]) is None


def test_contact_phone_in_source_name_refused():
    bad = rec(source_name="Waste office, call +62 361 222 333")
    docs, skips = copy(bad)
    assert docs == {} and len(skips) == 1 and "`source_name`" in skips[0], (docs, skips)
    assert "222 333" not in skips[0], skips
    assert cf.source_issue(bad, READINGS["R1"]) is None
    for field in ("district", "unit"):
        docs, skips = copy(rec(**{field: "ask ana@city.go.id"}))
        assert docs == {} and f"`{field}`" in skips[0], (field, docs, skips)


def test_year_ranges_are_not_phone_numbers():
    """A phone number is 9 or more digits. Statistics titles carry year ranges and codes."""
    for title in ("Waste statistics 2015-2024", "Waste statistics 2015 - 2024"):
        fig = only_figure(copy(rec(source_name=title, terms="CC-BY-4.0, Eurostat KS-GQ-18-006-EN-N"))[0])
        assert fig["source_name"] == title, fig
    for phone in ("+62 812 3456 7890", "0300-1234567", "(0361) 222-3333"):
        docs, skips = copy(rec(sent_by_role=f"lead, {phone}"))
        assert docs == {} and len(skips) == 1 and "`sent_by_role`" in skips[0], (phone, docs, skips)


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
def fixes(*records):
    return cf.taken_back(list(records), PLACES, FICTIONAL, set(READINGS))


def test_needs_a_fix_is_not_written_and_removed():
    """Ruling 1: an earlier run wrote the figure, then the team marked it `needs a fix`."""
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        docs, _ = copy(rec())
        assert cf.apply(docs, root, write=True) == ([BALI], [], [])
        docs, skips = copy(rec(state="needs a fix"))
        assert docs == {} and len(skips) == 1 and "needs a fix" in skips[0], (docs, skips)
        assert cf.apply(docs, root, write=True, taken=fixes(rec(state="needs a fix"))) == ([], [], [BALI])
        assert not (root / BALI).exists() and not (root / BALI).parent.exists()


def test_needs_a_fix_leaves_the_rest_of_the_file():
    """Ruling 1, one figure of two: the other year stays in the file."""
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        both = (rec(rid="recA", year=2024, value=398), rec(rid="recB", year=2025))
        cf.apply(copy(*both)[0], root, write=True)
        listing = (rec(rid="recB", year=2025, state="needs a fix"),)
        assert cf.apply(copy(*listing)[0], root, write=True, taken=fixes(*listing)) == ([], [BALI], [])
        left = yaml.safe_load((root / BALI).read_text(encoding="utf-8"))["figures"]
        assert [(f["year"], f["value"]) for f in left] == [(2024, 398)], left


def test_two_parts_of_one_reading_are_kept():
    """R1 asks for tonnes and a share. Both for 2025 survive, in the listing and on disk, and a
    later figure in one unit replaces only its own unit."""
    tonnes = rec(rid="recA", value=412.5, unit="t/yr")
    share = rec(rid="recB", value=38, unit="%")
    docs, _ = copy(tonnes, share)
    units = sorted(f["unit"] for f in docs[BALI]["figures"])
    assert units == ["%", "t/yr"], units
    newer = rec(rid="recC", created="2027-02-01T08:00:00.000Z", value=40, unit="%")
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        cf.apply(docs, root, write=True)
        cf.apply(copy(newer)[0], root, write=True)
        figs = yaml.safe_load((root / BALI).read_text(encoding="utf-8"))["figures"]
    assert sorted((f["unit"], f["value"]) for f in figs) == [("%", 40), ("t/yr", 412.5)], figs


def test_partial_listing_removes_nothing():
    """Concern 5: --write with a partial --records listing and no --prune removes nothing; --prune does."""
    full = [rec(rid="recA", year=2024, value=398), rec(rid="recB", year=2025),
            rec(rid="recC", reading_id=["R2"], value=3.1)]
    with tempfile.TemporaryDirectory() as td:
        root, real = Path(td), cf.ROOT
        shutil.copy(ROOT / "readings.yaml", root / "readings.yaml")

        def run(records, *flags):
            (root / "rows.json").write_text(json.dumps(records), encoding="utf-8")
            with contextlib.redirect_stdout(io.StringIO()):
                return cf.main(["--write", "--records", str(root / "rows.json"), *flags])

        try:
            cf.ROOT = root
            run(full)
            before = {p: p.read_text(encoding="utf-8") for p in (root / "observations").rglob("*.yaml")}
            assert len(before) == 2, before
            run(full[1:2])
            after = {p: p.read_text(encoding="utf-8") for p in (root / "observations").rglob("*.yaml")}
            assert after == before, "a partial listing changed observations/ without --prune"
            run(full[1:2], "--prune")
            left = sorted(p.relative_to(root).as_posix() for p in (root / "observations").rglob("*.yaml"))
            assert left == [BALI], left
            assert len(yaml.safe_load((root / BALI).read_text(encoding="utf-8"))["figures"]) == 1
        finally:
            cf.ROOT = real


def test_withdrawn_consent_removes_value_even_when_skipped():
    """The city takes consent back on a newer record that is skipped for another reason (here a
    `fictional` box that disagrees with the place). Its earlier published value does not stay."""
    published = rec(rid="recA", created="2027-01-10T08:00:00.000Z")
    withdrawn = rec(rid="recB", created="2027-02-01T08:00:00.000Z", may_publish="ask", fictional=True)
    regranted = rec(rid="recC", created="2027-03-01T08:00:00.000Z", value=415)
    for listing in ((withdrawn,), (published, withdrawn)):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            cf.apply(copy(published)[0], root, write=True)
            docs, skips = copy(*listing)
            assert docs == {} and len(skips) == 1, (len(listing), docs, skips)
            assert cf.apply(docs, root, write=True, taken=fixes(*listing)) == ([], [], [BALI]), len(listing)
    # A newer yes puts a figure back.
    fig = only_figure(copy(published, withdrawn, regranted)[0])
    assert (fig["value"], fig["sent_on"]) == (415, "2027-03-01"), fig


def test_workflow_fails_loudly_and_files_after_the_gates():
    """figures-to-pr.yml: a failed copy fails the job, and no source is filed before the gates pass."""
    wf = yaml.safe_load((ROOT / ".github" / "workflows" / "figures-to-pr.yml").read_text(encoding="utf-8"))
    steps = wf["jobs"]["figures"]["steps"]
    runs = [s.get("run", "") for s in steps]
    for run in runs:
        if "|" in run.replace("||", ""):
            assert "set -o pipefail" in run, run
    gates = next(i for i, s in enumerate(steps) if "gates" in s.get("name", ""))
    filing = [i for i, run in enumerate(runs) if "--file-sources" in run]
    assert filing and all(i > gates for i in filing), (gates, filing)
    assert "validate.py" in runs[gates] and "test_copy_figures.py" in runs[gates], runs[gates]


def test_missing_role_is_not_given():
    """Concern 4: the form does not require a role, so an empty one is written as `not given`."""
    fig = only_figure(copy(rec(sent_by_role=None))[0])
    assert (fig["state"], fig["sent_by_role"]) == ("candidate", "not given"), fig
    code, out, _ = parse_issue(cf.source_issue(rec(sent_by_role=None), READINGS["R1"])[1])
    assert code == 0, out


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
    assert tags("© the statistics office of Bali, reuse with attribution") == ["city-sent", "reading-r1", "cited-figure"]
    assert tags("CC BY 4.0") == ["city-sent", "reading-r1"]
    assert tags("Open Government Licence v3.0") == ["city-sent", "reading-r1"]
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


def test_prompt_tags_pass_the_schema():
    """The tags each prompt asks an agent to file are the ones the copy files, and the schema takes them."""
    pattern = re.compile(json.loads((ROOT / "schema" / "dataset.schema.json").read_text(encoding="utf-8"))
                         ["properties"]["tags"]["items"]["pattern"])
    for rid, r in READINGS.items():
        line = r["prompt"].split("### Tags\n", 1)[1].splitlines()[0].strip()
        assert line == f"city-sent, reading-{rid.lower()}", (rid, line)
        assert all(pattern.match(t) for t in sfi.csv(line)), (rid, line)


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
