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
wired_in_planetai: false
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

### 3. Regenerate the README

```bash
python scripts/build_readme.py > README.md
```

Don't hand-edit README sections that come from YAML — they'll be overwritten. The intro, taxonomy, contributing pointer, and footer are the only hand-maintained parts.

### 4. Open a PR

Title: `Add: {Source Name}` or `Update: {Source Name}` or `Remove: {Source Name} (reason)`.

Body should answer: who in the network uses it, which pillar × scale, why it belongs here.

## Updating an existing entry

Entries decay. APIs migrate, organisations rebrand, licenses change. If you spot drift, open a PR that:

1. Updates the entry's `status`, `url`, `license`, or `notes` as needed.
2. Bumps the `updated` field to today's ISO date.

If a source is deprecated or paywalled, **mark it but don't remove it** — preserving the history is part of the curation. Removal is for entries that genuinely don't belong (off-topic, never were a fit).

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
