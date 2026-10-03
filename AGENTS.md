# For the agent working in this repository

This is the registry of open data sources behind the Fab City Index and the PLANETAI nodes: one YAML file per source
under `data/{pillar}/{scale}/{slug}.yaml`, dated reviews under `reviews/`, the twenty Index cells under `cells/`, and
the 61 places in `places.yaml`. `index.json` and the middle of `README.md` are generated from the YAML; never edit
either by hand. The README is for people; this file routes you to the section written for what you are doing.

You work for a person, and the person is the contributor. Everything you file is theirs, from their GitHub account,
with your name in `assisted_by`.

## What the person in front of you is asking for

| the person says | read | then do this |
|---|---|---|
| "my city has no data for X", "add a source" | `CONTRIBUTING.md`, *Filing a source with an agent* (it has a brief written for you) | Find the gap at `index.fab.city/api/v0/places/<slug>.json`, verify licence and endpoint yourself, write the entry as `status: candidate`. Show the person the entry and the evidence before opening a pull request. |
| "is this source usable for our place?", "review it" | `REVIEWING.md`, *Reviewing with an agent* | A review is an issue titled `review: <pillar>/<scale>/<slug>`, filed from the person's account with their name and yours in `Assisted by`. A workflow writes the file under `reviews/` and opens the pull request; do not write review files by hand. |
| "this link is dead", "the licence changed", "it moved" | `CONTRIBUTING.md`, *Updating an existing entry* | Edit the one YAML file, say in `notes` what you read and when, regenerate (below). `python3 scripts/linkcheck.py` finds the rest of the drift. |
| "does a node read this source?" | `CONTRIBUTING.md` §2b | `adapter` names the code (`core:<fn>` or `pack:<id>`) in planetai-node. Set it only when that code exists on the node's `main`. |
| "add our city" | `places.yaml`'s header | Places come from the Index's coverage tracker, not from this repository. Ask a maintainer; do not add a slug here. |
| "CI is red and I changed nothing" | `.github/workflows/validate.yml` | The last step reads planetai-node's live `main`. Run `scripts/wired.py --check` against a clean checkout of this repo's `main`; if it fails there too, the node moved and your branch is innocent. Fix it in its own pull request. |

## Before you open a pull request

What CI runs, in its order, from the repository's root:

```
pip install -r requirements.txt
python3 tests/test_schema.py
python3 scripts/validate.py
python3 scripts/check_review.py
python3 scripts/build_index.py          # rewrites index.json; commit what it writes
python3 scripts/build_readme.py         # rewrites the generated middle of README.md; commit it
PLANETAI_NODE_REPO=../planetai-node python3 scripts/wired.py --check
```

All of them must exit 0. When you rebase or merge, regenerate `index.json` with `build_index.py` rather than resolving
it by hand: git merges it line by line and a clean merge can still be wrong.

## What must hold

- **An agent files `candidate`, never `live`.** `live` needs a person's review in `reviews/` or an `adapter`, and
  `validate.py` refuses anything else.
- **Every figure in `notes` is one you read**, from where, on what date. The licence is quoted from the publisher's own
  terms page, never from a portal's label. If you could not read something, `notes` says so.
- **Open means open.** Non-commercial, no-derivatives, all-rights-reserved or revocable terms do not go in as a source;
  stop and tell the person. `CONTRIBUTING.md` *When you cannot read the licence* covers the grey cases.
- **`places` names only places whose data you checked in the source itself.** A national dataset is not automatically
  data for every city in that country.
- **`pillar` and `scale` are where the source's strongest signal is**; `feeds_cells` is which Index cells a node fills
  from it, in the node's spelling (`Environmental|Bioregion`). They are different questions.
- **Your name never goes in `Your name`** on a review, and the parser refuses it.

## What not to do

- Do not merge. A maintainer merges, because a merged `candidate` moves a place's Index score before any review.
- Do not edit `index.json`, the generated part of `README.md`, or anything under `reviews/` by hand.
- Do not relax a check in `scripts/` or the workflow to get an entry through; if a check is wrong, say so in its own
  pull request.
