# Upstream contribution drafts

Curated submissions to other public dataset registries, prepared in their native schemas.

The point of this directory is to make our upstream contributions reciprocal and visible. We pull from these registries; we should also push back what's demonstrably missing and that the Fab City network can vouch for.

## apd-core (`awesomedata/awesome-public-datasets`)

Six entry drafts in `apd-core/` ready to PR to [`awesomedata/apd-core`](https://github.com/awesomedata/apd-core/tree/master/core). Each is a single YAML file matching the apd-core entry schema, sized for one PR per entry so reviewers can accept them individually.

| Slug | Category | Why it's missing | Why we vouch for it |
| --- | --- | --- | --- |
| `smart-citizen` | EarthScience | No community-tier sensor APIs in the list | FabLab BCN / IAAC origin; PLANETAI uses it |
| `bali-satu-data` | Government | Indonesia underrepresented | PLANETAI Wave 28 / Bali pilot |
| `open-data-bcn` | Government | Spain underrepresented | PLANETAI Wave 21 / Barcelona pilot |
| `materialflows-net` | Economics | UN IRP MFA absent | Used in PLANETAI Wave 16 Sankey + crosswalk |
| `chilecompra` | Government | LATAM procurement absent | Santiago pilot, H₀-A baseline |
| `lkpp-spse` | Government | Indonesian procurement absent | Bali pilot, H₀-A baseline |

### How to submit

For each entry:

1. Fork [`awesomedata/apd-core`](https://github.com/awesomedata/apd-core).
2. Copy the YAML from `apd-core/{slug}.yml` to `core/{Category}/{slug}.yml` in your fork.
3. Open a PR with title `Add: {Source Name}` and a body explaining the source's significance in 2-3 sentences. Cross-link from the PR back to the matching entry in `fab-city/awesome-fabcity-data` as evidence the source is in production use.

Each PR should be independent — apd-core reviewers prefer atomic, single-source PRs over batch contributions.

### Naming convention in apd-core

apd-core uses kebab-case slugs and matches the file-name to the dataset name. Categories are existing top-level directories under `core/` (Agriculture, Architecture, Biology, ..., Transportation). Don't invent categories. If the natural fit is between two categories, pick the one with more existing entries of similar type.
