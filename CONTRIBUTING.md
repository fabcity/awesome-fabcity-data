# Contributing to awesome-fabcity-data

This list is opinionated curation, not exhaustive cataloguing. Adding an entry should mean *somebody used this in production* or *somebody audited it as fit-for-purpose for a fab-lab or partner-city use case*. We'd rather have a smaller, current, honest list than a large, half-stale one.

If your contribution doesn't fit that frame — e.g. you found a generic dataset list and want to mirror it here — that's not a fit. Submit upstream to [`awesomedata/awesome-public-datasets`](https://github.com/awesomedata/awesome-public-datasets) instead, where the criteria are different. We may then pull individual entries from there if they pass our fit test.

## What kinds of entries belong here

A source belongs in this list if **all three** are true:

1. **It carries an open license** (CC-BY-4.0, CC0, ODbL, MIT, public domain, or equivalent). Paywalled-tier APIs with a free quota are acceptable if the free tier is non-trivial; full paywalls are not.
2. **It maps cleanly onto a Fab City pillar × scale.** If you can't pick a pillar (environmental / social / economic / governance) and a scale (planet / bioregion / region / city / community) without contortion, the source probably doesn't fit our framing.
3. **It has been used or audited by somebody in the network.** Either a PLANETAI connector exists, a fab lab has integrated it, a partner city has built on it, or a research collaborator has vetted it. Curation reflects use, not just hope.

If only two of three are true, open an issue rather than a PR — let's discuss before adding.

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
status: live             # live | stale | paywalled | deprecated | planned
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

## What we won't accept

- Mirrors of upstream lists with no added curation.
- Datasets behind hard paywalls with no free tier.
- Datasets with unclear licensing where the maintainer hasn't responded to clarification.
- Entries that exist only because the contributor wants visibility for their own project.
- Generic ML-training datasets (ImageNet, COCO, MS-MARCO) — they're foundational for ML but not for measurement of distributed production.

## Code of Conduct

Be honest, be useful, be brief. If you wouldn't say it in a fab lab to someone you respect, don't put it in a PR comment.

The Fab City network operates under [Fab Charter](https://fabfoundation.org/about/) principles and [Contributor Covenant 2.1](https://www.contributor-covenant.org/version/2/1/code_of_conduct/). Issues go to community@fab.city.
