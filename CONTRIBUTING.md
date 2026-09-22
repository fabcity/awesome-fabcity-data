# Contributing to awesome-fabcity-data

This list is opinionated curation, not exhaustive cataloguing. Adding an entry should mean *somebody used this in production* or *somebody audited it as fit-for-purpose for a fab-lab or partner-city use case*. We'd rather have a smaller, current, honest list than a large, half-stale one.

If your contribution doesn't fit that frame — e.g. you found a generic dataset list and want to mirror it here — that's not a fit. Submit upstream to [`awesomedata/awesome-public-datasets`](https://github.com/awesomedata/awesome-public-datasets) instead, where the criteria are different. We may then pull individual entries from there if they pass our fit test.

## What kinds of entries belong here

A source belongs in this list if **all three** are true:

1. **It carries an open license** (CC-BY-4.0, CC0, ODbL, MIT, public domain, or equivalent). Paywalled-tier APIs with a free quota are acceptable if the free tier is non-trivial; full paywalls are not.
2. **It maps cleanly onto a Fab City pillar × scale.** If you can't pick a pillar (environmental / social / economic / governance) and a scale (planet / bioregion / region / city / community) without contortion, the source probably doesn't fit our framing.
3. **Somebody has read it, or something reads it — and the entry says which.** This is two states, not
   one, and `status` is where the difference lives.

### Criterion 3 is two states

This criterion used to read *"it has been used or audited by somebody in the network"*, and every
entry that met the first two criteria was filed as `live`. That was one word doing two jobs. In
September 2026, 189 of the 203 `live` entries named no adapter and no reviewer: the list was
asserting a hundred and eighty-nine times that somebody had used or audited a source, with nothing
in the repository behind the claim. The sources were real and the verification was real. The
sentence was not.

So the state splits in two, and both halves are checkable:

| | What it claims | What has to exist |
| --- | --- | --- |
| **`candidate`** | It fits a named indicator row, its licence and endpoint are verified, and **nobody has read it for a real territory yet.** | `notes` saying what you verified and what is still missing. Nothing else. |
| **`live`** | A named person read it for a real place, or code reads it. | A file under [`reviews/`](reviews/) with verdict `usable` or `usable-with-caveats`, **or** an `adapter` naming what reads it. |

`candidate` is not a lower tier or a waiting room with a bad name. It is the honest state of a
source somebody went and checked, and it is where a new entry normally starts — **file new entries
as `candidate` unless you are also writing the review or the adapter.** A list where most entries
are candidates is a list telling the truth about itself; the previous version, where all of them
were `live`, was not.

`scripts/validate.py` counts the entries that claim `live` with neither a review nor an adapter and
prints them under a header saying what they are. It is a warning, not a failure — 189 files turning
red on the day the rule lands would get the rule deleted rather than the debt paid. `--strict`
makes it a failure, for when the network decides to flip it.

If criteria 1 and 2 hold but you have no reading and no code, that is not a reason to stay out of
the list — it is a `candidate`. If **1 or 2** fails, open an issue rather than a PR.

## Adding an entry

Every entry is a single YAML file under `data/{pillar}/{scale}/{slug}.yaml`. The slug is lowercase-hyphenated and unique within its directory.

### 1. Copy the template

```yaml
name: Source Name
url: https://example.org/
description: |
  One- to two-sentence summary. What is it; what does it carry; who runs it.
pillar: environmental    # environmental | social | economic | governance
scale: city              # planet | bioregion | region | city | community
status: candidate        # candidate | live | stale | paywalled | deprecated | planned
                         # candidate = verified, unread by anyone; needs `notes`. Start here.
                         # live = a review file exists, or `adapter` names code that reads it.
license: CC-BY-4.0
api: https://api.example.org/v1
pilot_relevance: [barcelona, boston]
tags: [air-quality, citizen-science]
added: 2026-05-04
adapter: pack:coast      # core:<fn> in the node's app/sources.py or app/bootstrap.py, or pack:<id>.
                         # Omit it if nothing reads this source yet — that is the honest majority.
feeds_cells: [Environmental|Bioregion]   # Index cells a node fills from it. Pillar|Scale, capitalised.
auth: none               # none | key-free-rate-limited | api-key | registration | paid
role: [observe]          # observe | act. Omit = [observe]. `act` requires act_kind.
wired_in_planetai: false # deprecated, derived — set `adapter` instead, and leave this off new entries
upstream_listed_in: []
notes: |
  Optional longer-form notes: API quirks, rate limits, citation
  requirements, recommended usage patterns. Multiple paragraphs ok.
```

Required: `name`, `url`, `description`, `pillar`, `scale`, `status`, `license`. Everything else is optional but recommended.

### 2. Validate locally

```bash
python scripts/validate.py
```

This walks `data/` and validates each YAML against `schema/dataset.schema.json`. CI runs the same check on every PR.

### 2a. How to review a source

Reviewing is the other way to contribute, and it needs no write access, no fork and no YAML.

**Open a [source review](.github/ISSUE_TEMPLATE/source-review.yml) issue.** One field per key of
`schema/review.schema.json`; a workflow parses it, writes the review file, and opens a pull request
for a maintainer to merge. If your verdict is `usable`, the same PR flips the entry's one `status:`
line from `candidate` to `live`.

What a review is:

- **One source, one territory, one person.** Not a batch and not a team. The point is that somebody
  can be asked about it in six months, which is why `by` is a person's name and `org` says whose
  hands it passed through.
- **A named place.** `territory` is Barcelona, Menorca, Santiago — somewhere with administrative
  codes you can actually check against. Not "global", and not the source's own coverage claim.
- **What you actually checked**, from five: `licence`, `endpoint`, `admin-code`, `vintage`,
  `field-fit`. A short list is honest. An unticked box is not a failure — it is the next reviewer's
  work, and they can see it is waiting.
- **A verdict.** `usable` promotes a candidate. `usable-with-caveats` records the reading and
  deliberately leaves the status alone, because a caveat is a thing a person should read before this
  list says `live`. `unusable` is a real answer and is kept like the others: somebody tried, and
  the next person does not have to try the same thing.
- **Notes.** Required by nothing and worth more than the rest of the file put together. The join you
  had to build by hand, the rate limit, the series that ends in March without saying so.

If your organisation publishes the source, tick **Self-declared**. It is not disqualifying — you
probably know its licence and vintage better than anyone — and it is recorded because a publisher's
reading and an outsider's are different kinds of evidence.

Reviews live at `reviews/{pillar}/{scale}/{slug}/{date}-{reviewer-slug}.yaml`, beside the entry they
are about. `scripts/validate.py` fails if a review names an entry that does not exist or sits in the
wrong directory, so a review always points at something real. A worked example, heavily commented,
is at [`docs/review.example.yaml`](docs/review.example.yaml).

**Reviews expire.** `scripts/check_review.py` warns when the newest usable review of a `live` entry
passes 365 days and fails CI past 730, printing the exact `status:` line to flip back to `candidate`.
A reading is evidence about a source at a moment: the `data.seoul.go.kr` pages served a termination
notice for months without changing a status code. Entries standing on an `adapter` are not failed —
there the code is the evidence, and `scripts/wired.py` checks that it resolves.

Who can review what, and who would rather not be asked: [`REVIEWERS.md`](REVIEWERS.md). Add
yourself — especially if you maintain open data for a pledged Fab City.

### 2b. What reads it: `adapter`, not `wired_in_planetai`

`wired_in_planetai` was a boolean typed in this repository asserting runtime state in another one. It
drifted the way such a claim always drifts: sixteen of thirty-two were ticked in September, one of them
a `paywalled` source no node can call, and three were simply wrong until someone read the code. The fix
is not a better boolean. It is a pointer.

**`adapter`** names the thing that reads this source: `core:<fn>` for a function in the node's
`app/sources.py` or `app/bootstrap.py` (`core:ckan`, `core:power_climatology`), `pack:<id>` for a pack
directory (`pack:coast`, `pack:earth`). It is a string, not a list, on purpose — a source with several
readers names its primary one here and the rest in `notes`, because a list invites the fiction that
this file tracks the node's call graph. It does not. It answers one question: is there code, and where
do I start reading it.

**`feeds_cells`** names the Index cells a node fills from this source, in the node's own spelling —
`Environmental|Bioregion`, capitalised, pipe-separated. This is not the entry's own `pillar`/`scale`,
which say where the source publishes its strongest signal. A source filed under `economic/community`
can feed `Economic|Community` and nothing else, or feed three cells, or feed none. An empty list says
something a missing one does not: *code reads this, and no Index cell comes out of it.* Several of the
node's own sources are in exactly that state — a model point sample is a boundary condition, not a cell.

Together they let a node compute what a person used to count by hand: which cells of the 4×5 matrix
have a registered source, which of those have an adapter, and which have neither. `planetai sources
--cell "Social|City"` is that query.

Unlike the boolean, both halves of `adapter` are checkable, and CI checks them:

```bash
python scripts/wired.py            # report
python scripts/wired.py --check    # what CI runs
```

A pack that reads a source this list calls unwired fails. An `adapter` naming a pack the node does not
have, or a function that is not in `app/sources.py` or `app/bootstrap.py`, fails. There is no half this
cannot see, which is the entire argument for replacing the boolean rather than repairing it.

`wired_in_planetai` stays for now — the Airtable Data Sources mirror still reads it — and
`scripts/validate.py` prints a warning for every entry that says `true` and names no `adapter`. Do not
set it on a new entry. It is removed in the release after the mirror reads `adapter` instead.

### 2c. Observe or act: `role` and `act_kind`

Every one of the first 209 entries answers the same question — *what is happening here*. None of them
answers *where do I go about it*. A fab lab and a PM2.5 model are both a name, a URL and a pillar ×
scale, and nothing in the file tells them apart.

**`role`** does. `observe` means the source tells a node what is happening. `act` means it tells a
person where to go and do something. Some sources are both: a registry of fab labs is `[observe, act]`
— an activity index measures *from* it, and a person can walk into one of the labs it lists. Absent
means `[observe]`; the validator does not fill it in, and you should not type it on a measurement
source just to be explicit.

**`act_kind`** says what kind of thing to act with, and is required whenever `role` contains `act` — an
act source that cannot say what it offers is a link, not an entry. `facility` is a place with machines;
`design` is a commons of things to build; `repair` is somewhere to fix what you have; `match` is a
matcher over the other two; `network` is a set of places bound by a commitment rather than by
capability; `material` is a stock or a stream of stuff. `equipment` is held back deliberately — it is
for the day one facility's own OKW machine record is an entry, which is not what a directory of
thousands of facilities is.

Act sources do **not** get a directory of their own. They stay in the pillar × scale tree where they
belong, and `role` is the only thing that marks them. See "Pillar / scale judgment calls" below.

### 3. Regenerate the README

```bash
python scripts/build_readme.py
```

The script rewrites `README.md` IN PLACE, between the `<!-- BEGIN GENERATED -->` and
`<!-- END GENERATED -->` sentinels, and prints a one-line summary to stdout. Do **not**
redirect it into `README.md` — the shell truncates the file before the script runs and
the hand-maintained intro and outro are destroyed.

Don't hand-edit README sections that come from YAML — they'll be overwritten. The intro, taxonomy, contributing pointer, and footer are the only hand-maintained parts.

### 4. Open a PR

Title: `Add: {Source Name}` or `Update: {Source Name}` or `Remove: {Source Name} (reason)`.

Body should answer: who in the network uses it, which pillar × scale, why it belongs here.

## Updating an existing entry

Entries decay. APIs migrate, organisations rebrand, licenses change. If you spot drift, open a PR that:

1. Updates the entry's `status`, `url`, `license`, or `notes` as needed.
2. Bumps the `updated` field to today's ISO date.

If a source is deprecated or paywalled, **mark it but don't remove it** — preserving the history is part of the curation. Removal is for entries that genuinely don't belong (off-topic, never were a fit).

### Finding the drift

```bash
python scripts/linkcheck.py                      # every entry's url and api
python scripts/linkcheck.py --only status=live   # just the ones claiming to be alive
```

It asks each URL whether it answers and sorts the replies into categories. **It reports; it does not
judge**, and it is deliberately not in CI: 317 requests to 163 third parties on every pull request
would be rude, and the answers are too ambiguous to gate on.

Read the output with that ambiguity in mind. On the 19 September 2026 run, 41 URLs returned 404 and
**most of them were fine** — an API base path 404s by design, and `datacatalog.worldbank.org` serves a
404 to anything without Javascript while rendering the dataset perfectly in a browser. Six were real:
the `data.seoul.go.kr` pages now render the portal's own 서비스 종료 안내, a termination notice, which no
status code revealed. `blocked` (401/403) is usually a bot check in front of a healthy site, and a
timeout from one laptop is not evidence about a server.

So: only `dns` and `gone` are worth opening, every one of them is worth opening **in a browser**, and
nothing should be marked `deprecated` on a status code alone.

## Pillar / scale judgment calls

A few that come up often:

- **Procurement data** is governance, not economic. The signal it carries is "what the public sector is choosing to buy"; the economic-pillar version of that is supply-chain or sectoral-productivity data.
- **Sensor networks at the community tier** (Smart Citizen, Sensor.Community, AirGradient) belong at `community` scale even though they aggregate up. We classify by where the *atomic measurement* happens.
- **City open-data portals** are governance at city scale, not a multi-pillar entry, even though a portal carries datasets that touch all four pillars. Add specific datasets within the portal as separate entries when they're material.
- **Earth-system models** (Aurora, GraphCast, GenCast, AlphaEarth) are environmental at planet scale. Their model weights are infrastructure; their forecasts are the data we list.
- **Act sources stay in the tree.** A directory of fab labs, a commons of designs, a repair-café map — these are not a sixth pillar or a parallel directory. They are filed by pillar and scale like everything else and marked with `role: [act]`. A fab lab is `economic/community`: production capacity where people are. A design commons is `economic/planet`: the library has no location, only the thing built from it does. A register of regional manufacturers is `economic/region`. One tree, so the measurement of a thing and the thing itself can sit next to each other — the Fab Lab Activity Index and fablabs.io are the same subject seen from the observe and act sides.
- **A design library is `planet` scale, always.** The temptation is to file it where its users are. Resist it: scale here means where the source publishes its strongest signal, and a commons publishes globally. What is local is the making, not the library.

## The cell map: `cells/`

An entry says what a source carries. A cell says what the Index *claims* when that cell of the
4 × 5 matrix is filled — its indicator categories, the minimum set of indicators below which the
cell is not filled but decorated, and `does_not_claim`: what a filled cell must never be read as
saying. Three reference stations describe a city's regulatory compliance, not where a child walks
to school, and the only place that sentence can live is next to the cell.

One file per cell at `cells/{pillar}-{scale}.yaml`, lowercase, matching its own `cell:` key.
Validated by `scripts/validate.py` against `schema/cell.schema.json`; worked example at
[`docs/cell.example.yaml`](docs/cell.example.yaml). The map is empty on purpose — what each cell
claims is the network's decision, not a thing to be inferred from whatever sources happen to exist.

## What we won't accept

- Mirrors of upstream lists with no added curation.
- Datasets behind hard paywalls with no free tier.
- Datasets with unclear licensing where the maintainer hasn't responded to clarification.
- Entries that exist only because the contributor wants visibility for their own project.
- Generic ML-training datasets (ImageNet, COCO, MS-MARCO) — they're foundational for ML but not for measurement of distributed production.

## Code of Conduct

Be honest, be useful, be brief. If you wouldn't say it in a fab lab to someone you respect, don't put it in a PR comment.

The Fab City network operates under [Fab Charter](https://fabfoundation.org/about/) principles and [Contributor Covenant 2.1](https://www.contributor-covenant.org/version/2/1/code_of_conduct/). Issues go to community@fab.city.
