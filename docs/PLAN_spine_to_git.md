# Plan — the Index spine leaves Airtable

**Status: Phase 1. Nothing here is built.** For Tomas and Lucas to approve or strike. Phase 2 is five pull
requests across three repositories and begins on "go", not before.

Everything in §1 was read from the live base and the live API on 19 September 2026, not from the review
that asked for this document. Four of its premises turned out to be wrong, and one of them changes the
plan.

---

## §1 · What is actually there, measured today

### The whole live Fab City Index is one cell

```
$ curl https://index.fab.city/api/cells/barcelona.json
{ "city": "barcelona", "format": "fci-cells-v0", "count": 1,
  "cells": { "Environmental|City": {
      "value": 18.4, "unit": "µg/m³ PM2.5 (hourly mean)",
      "source": "Smart Citizen kit — manual seed",
      "observed_at": "2026-06-06T16:00:00.000Z", "state": "partial",
      "notes": "S1 hand-written seed observation; replaced by the S2 Smart Citizen adapter…" } } }
```

`bali`, `boston` and `santiago` each answer `"count": 0, "cells": {}`. That is the public read surface of
the Fab City Index, in full, on 19 September 2026: **one hand-written seed from 6 June, marked `partial`,
whose own note says it was superseded.**

### The base behind it holds seven rows, and six of them cannot be read

`Observations` (`tbl8VZoGMr6kdE4QX`) has **7 records**, all created 6–7 June, all with
`observed_at = 2026-06-06T16:00:00Z`:

| city | cell | state | source |
|---|---|---|---|
| barcelona | `Environmental\|City` | partial | Smart Citizen kit — manual seed |
| madrid | `Environmental\|City` | **live** | AirVisual Pro |
| bilbao | `Environmental\|City` | partial | Euskadi Air Network |
| sevilla | `Environmental\|Residential` | **live** | Netatmo Weather Station |
| valencia | `Environmental\|Harbor` | **live** | Smart Citizen kit — auto |
| malaga | `Environmental\|Beach` | **live** | Weather Underground |
| zaragoza | `Environmental\|Industrial` | mock | Citizen Science Project |

Three things follow, and each is a reason to move rather than a reason to wait:

- **Six of the seven cities are not in `ALLOWED_CITIES`.** `cells-worker/worker.js:12` serves
  `["barcelona","boston","santiago","bali"]` and 404s everything else. Madrid, Bilbao, Sevilla, Valencia,
  Málaga and Zaragoza are in the spine and invisible. Nothing told anybody.
- **Four of the seven cell keys are not `Pillar|Scale`.** `Environmental|Residential`, `|Harbor`, `|Beach`,
  `|Industrial` are not among the twenty keys `SPEC.md §1` defines, and `cells-ingest/ingest.py`'s
  `VALID_CELLS` would refuse every one of them. **The spine contains rows our own writer would reject.**
- **Four rows say `state: live` and are invented.** "Simulated reading", "Weather Underground",
  "Netatmo Weather Station", "AirVisual Pro" — demo seeds from the 6 June thin slice, carrying the one
  word the whole methodology rests on. `live` means measured here. None of these were.

### The sources half already flows git → Airtable, and it stopped eleven weeks ago

The base's `Data Sources` table (`tblT49HDoAswQYBfs`) describes itself:

> *Registry of open-data sources, synced one-way from the awesome-fabcity-data GitHub repo
> (`data/{pillar}/{scale}/{slug}.yaml` = source of record). Do not hand-edit synced fields.*

So the direction this plan proposes is **already the established one for half the base**. It holds **32
rows, `last_synced: 2026-07-04`**. This repository holds **209** entries and was re-pinned this morning.

That is the most important thing in this document. The one git → Airtable mirror that exists ran once, fell
85% behind, and nobody noticed for eleven weeks, **because nothing checks it.** Any plan whose last step is
"a scheduled job mirrors the built JSON into Airtable so the spreadsheet views survive" has to answer why
that mirror will not do the same. §4 answers it.

### What else lives in the base, which the review did not account for

- **`FCI Coverage Tracker`** (`tbl9tfpEsxoxQAh0w`): 61 localities × 8 per-territory cells, plus a
  four-rung budget ladder. Its own description says *"this table is the resume point — a scheduled task
  reads it, takes the next pending wave, writes results, and stops."* It is a **work queue**, not a spine,
  and this plan does not move it. Said explicitly because "move the Index out of Airtable" would otherwise
  be read as including it.
- **`Observations.Source Link`**, a linked-record field into `Data Sources`, added as *"structured
  replacement for the free-text `source` field"*. In git this becomes a `source_slug` string keyed on the
  slug this repository already uses (`governance/city/open-data-bcn`), which is better than a record id and
  is checkable by the validator. Gain, not loss.
- Four formula fields (`day`, `year`, `month`, `value_state_concat`). View conveniences; they regenerate.

### Corrections to the brief

| the review said | what is true |
|---|---|
| table `FCI Observations` | the table is `Observations`; `FCI Observations` is the base's name |
| `cells-ingest` is a private repo | it is `fci-index/cells-ingest/`, a directory in the site repo |
| `cells-ingest` writes rows | it **upserts one row per `(city, cell)`** and says why: "appending would grow the table forever" |
| "one hand-edited row is the whole of Barcelona's live data" | right, and it is `partial`, not `live` — and it is the whole of *every* pilot's data |

---

## §2 · The decisions

### 1. A separate repository: `fabcity/fci-observations`

Not an `observations/` tree here. Sources and observations differ in every axis that matters: cadence (a
source changes a few times a year, an observation every hour), writer (a human in a PR versus a machine
with a deploy key), volume, and blast radius. A machine pushing hourly into this repository would bury the
human-reviewed source edits it exists to protect, and CI here would run 209 dataset validations on every
observation push.

They stay joined by the **slug**, which costs nothing and is already the key both ends use.

### 2. Append-only JSONL, one file per pilot per year

```
observations/<pilot>/<YYYY>.jsonl      one fci-cells-v0 row per line, append-only
```

**This is a change of semantics and it is the point.** Today `cells-ingest` upserts one row per
`(city, cell)`, so the spine is the size of the matrix and has no past: yesterday's Barcelona number is
gone, overwritten. Append-only means the Index gets a time series and a `git log`, which is the thing
nobody can reconstruct later. Newest-per-`(city, cell)` at read time gives exactly today's document back.

JSONL rather than YAML-per-row because these are machine-written and there will eventually be a lot of
them; one line appended is a clean diff and a trivial merge.

**Consequence that must not be missed:** `worker.js:72` fetches with `pageSize=100` and **no pagination**.
It works today because there are 7 rows. Against a history it would silently serve a truncated window.
Whatever the worker reads after this, it does not read Airtable — §5 — and this is one reason why.

### 3. The schema is `SPEC.md §1`'s row, plus two fields it does not have

`schema/fci-cells-v0.json` in the new repository:

```
city         one of the four pilot keys            required
cell         one of the 20 "Pillar|Scale" keys     required
value        number                                required
unit         string                                required
source       free text, as today                   required
observed_at  RFC 3339, not in the future           required
state        live | partial | mock                 required
notes        string                                optional   (in Airtable and in the served doc; NOT in SPEC.md §1 — see below)
source_slug  awesome-fabcity-data slug             optional   (replaces the Source Link record id)
published_by node fingerprint                      optional   (once PR #93 lands; see §7)
```

**`notes` is a discrepancy to settle, not to paper over.** `SPEC.md §1` writes the row as
`{city, cell, value, unit, source, observed_at, state}` — seven fields. Airtable, `ingest.py:126` and the
served document all carry an eighth, `notes`, and Barcelona's only cell uses it to say the row is a seed.
Either `fci-cells-v0` has eight fields and `SPEC.md` is wrong, or it has seven and the worker is publishing
an undeclared field. **Phase 2 cannot start until this is answered**, because it decides whether the
schema's `additionalProperties` is `false`.

Recommendation: eight fields, and fix `SPEC.md`. A number with nowhere to say "this is a seed" is a number
that lies more easily.

### 4. The validator refuses what is in the spine today

`scripts/validate.py` in the new repo, modelled on this repository's, failing on: an unknown pilot; a cell
key outside the twenty; `state` outside `live|partial|mock`; `observed_at` in the future; a duplicate
`(city, cell, observed_at)`; a `source_slug` that names no entry in this repository's pinned registry.

Run against the seven rows exported today it **fails five of them** — six cities and four cell keys are
invalid, overlapping. That is the correct result and §6 is what to do about it.

### 5. The worker stops reading Airtable and serves the built JSON

`scripts/build_api.py` in the new repo folds the JSONL to newest-per-cell and writes
`api/cells/<city>.json` and `api/cells/index.json` — **byte-identical in shape to what the worker serves
today**, `format: "fci-cells-v0"`, the same `cells` map keyed by cell. No consumer changes. The built files
are committed, not only built in CI, so the repository alone is the Index: a `git clone` brings back
everything, which is the whole point of the exercise.

`cells-worker` serves them from the repo's Pages deployment. The Airtable path stays behind
`SPINE_SOURCE=airtable` for one month, and `live.js:15`'s hard-coded
`https://fci-cells.tomas-74b.workers.dev/...` staging fallback — a personal subdomain in production
JavaScript — goes at the same time.

The worker also gains the rate-limit binding the agent-ready memo asked for. It has none today.

### 6. The migration is an honest export, and it will not validate

The review asked for "export every current Airtable row once, validate, commit as the first history". The
export exists; the validation fails. Three choices, and this is the one Tomas decides:

- **(a) Commit all seven as history, with a `RETRACTED.md` naming what was wrong.** The `git log` starts
  with the truth about itself. The validator gets a one-time `--legacy` flag for the initial import only.
- **(b) Commit only Barcelona's row** — the one the read API actually serves and the only one a reader has
  ever seen — and record the other six in `RETRACTED.md` without importing them. **Recommended.** Six rows
  no reader has ever been served are not history; they are a demo fixture, and four of them assert `live`.
- **(c) Start empty.** Cleanest, and it throws away the only artefact of the June thin slice.

Whichever is chosen: the four `live` rows do not enter the spine carrying that word. This is the moment
the Index stops asserting something it cannot support, and it costs nothing today precisely because there
is nothing there.

### 7. The write path: a deploy key per pilot, not a token

`cells-ingest` stops holding an Airtable PAT with `data.records:write` on the whole base — one token that
can rewrite every pilot's numbers — and holds a **per-pilot deploy key** with write access scoped to that
pilot's directory, enforced by a `CODEOWNERS`-style path check in CI on push.

Push, not a PR. A PR per hourly observation is a queue nobody drains, and the validator in CI is the gate
that matters. `FCI_PUBLISHER=1` stays exactly as it is, and so does the refusal at `ingest.py:141`. The
dry run prints the JSONL line it would append rather than an Airtable payload.

Once PR #93 (node identity) lands, `published_by` carries the child's fingerprint and the pilot's key
becomes checkable against the node that claims to have produced the row. Until then the deploy key is the
only identity and the plan does not pretend otherwise.

---

## §3 · What does not change

- **The read contract.** `fci-cells-v0`, the four pilot keys, newest-per-cell, the `cells` map shape,
  `Cache-Control: public, max-age=300`. A consumer that works today works after.
- **The tier rule.** One node per pilot publishes; a home node never does
  (`skills/publish-to-index/SKILL.md`). Unchanged in words and in code.
- **State is never upgraded.** `live` means measured here, a model or portal is `partial`, aggregation
  never promotes.
- **`FCI Coverage Tracker`** stays in Airtable and stays a work queue.
- **This repository.** `data/`, its schema, its validator and its generated README are untouched.

---

## §4 · The Airtable mirror, and why it will not rot like the last one

The spreadsheet views are genuinely useful and the mirror should exist. But the `Data Sources` evidence in
§1 is that an unchecked mirror silently falls 85% behind and nobody finds out for eleven weeks.

So the mirror is **checked or it is abandoned**, and there is no third option:

- a scheduled job writes the built JSON into `Observations` and records `last_synced`;
- the same job **fails loudly** when `last_synced` is older than its own interval, into the same place a
  failing CI run goes;
- `Data Sources` gets the same check in the same PR, because it is broken right now and fixing the thing
  that taught us the lesson is the cheapest part of this plan.

If nobody will own a failing alarm, the honest move is to delete the mirror and let Airtable hold nothing,
rather than hold something stale that looks current.

---

## §5 · The rollback, and what it costs

The worker's Airtable branch stays behind `SPINE_SOURCE=airtable` for **one month** from the day the Pages
read goes live. Flipping one variable returns the old path. After a month it is deleted, in a PR that says
so.

What rollback does **not** cover: observations appended to git during that month are not in Airtable unless
the mirror ran. The mirror is therefore load-bearing during the rollback window and optional after it — an
argument for building §4 first, not last.

---

## §6 · Phase 2, in order, one PR per repository

1. **`fabcity/fci-observations`** (new) — schema, validator, CI, the export decided in §6, `build_api.py`,
   the built `api/`, README with the read contract, `llms.txt`. *This repository has no `llms.txt` either;
   worth adding here in the same week.*
2. **`fci-index/cells-worker`** — read the built JSON; add the rate-limit binding; Airtable behind
   `SPINE_SOURCE=airtable`; delete the `tomas-74b.workers.dev` fallback from `public/js/live.js:15`.
3. **`fci-index/cells-ingest`** — write JSONL to git; keep `FCI_PUBLISHER=1`; dry run prints the line.
4. **The mirror job**, with its own staleness alarm, and the same alarm retro-fitted to `Data Sources`.
5. **`planetai-node`** — `SPEC.md §1` names the repository and schema URL instead of the base id, and
   settles `notes` (§3 above); `skills/publish-to-index/SKILL.md` describes the new last mile. Tag.

**Blocked on a decision, not on code:** §3's `notes` question and §6's choice of (a), (b) or (c).

---

## §7 · Handoff

- **The deploy keys are held by the Foundation**, one per pilot, issued by hand exactly as the Airtable
  tokens are today. Nothing about who may publish changes.
- **A fifth pilot is one folder, one key, one PR** — and one line in `ALLOWED_CITIES`, which is currently
  hard-coded in two places (`worker.js:12` and `ingest.py:56`) with a comment asking that they be kept in
  step. In the new repository it is one file that both read.
- **The methodology page authors** need to know that `fci-cells-v0` is now defined by a schema file with a
  URL, and that the four `live` demo rows are gone. If any methodology text cites a number from the seven,
  it is citing a seed.
- **The Airtable read path is deleted one month after the Pages read goes live.** Put the date in the PR
  that ships step 2.

---

## §8 · What Tomas and Lucas are being asked

| § | the call | if struck |
|---|---|---|
| 1 | separate repo `fci-observations` | an `observations/` tree here, with machine pushes landing in the humans' repo |
| 2 | append-only JSONL, newest-per-cell at read | keep the upsert, keep a spine with no past |
| 3 | **`notes` is the eighth field of `fci-cells-v0`; fix `SPEC.md`** | seven fields, and the worker stops publishing `notes` — which deletes Barcelona's only honest sentence |
| 6 | **import Barcelona only; the other six to `RETRACTED.md`** | (a) import all seven as history, or (c) start empty |
| 7 | per-pilot deploy key, push not PR | a PR per observation, and a queue |
| 4 | the mirror is checked or deleted | an unchecked mirror, which §1 shows is a stale one |

Nothing in this document touches production DNS, the worker route, or the Airtable base. Reads only, and
the base was not written to.

**Phase 2 begins on "go", not before.**
