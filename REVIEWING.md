# How to review a source

You have been asked to read one dataset and say whether it works for a place you know. That is the
whole job. It takes about twenty minutes, you need no GitHub account to start, no write access, and
you never touch YAML.

This is the walkthrough. [`CONTRIBUTING.md` §2a](CONTRIBUTING.md#2a-how-to-review-a-source) is the
reference — what the fields mean and where reviews are stored. Read this one first.

## Why anyone wants this

Every entry in this list carries a `status`. `candidate` means somebody verified the source exists
and nobody has read it for anywhere real. `live` means a named person read it for a named place and
said it works — or that code in a node reads it every day.

**Reviews are still rare.** Most entries have none, and a `candidate` stays one until somebody's
reading promotes it. The numbers are not written here, because they would be stale by the next
merge: `counts` at the top of [`index.json`](index.json) is generated and always current, and each
section of the [README](README.md) lists its candidates. That is not a backlog to feel bad about;
it is the reason your twenty minutes is worth more here than almost anywhere else in this
repository.

**You are reviewing a source, not approving it.** `unusable` is a genuinely useful answer. So is
"I only got through two of the five checks."

## Before you start: pick your territory

A review is always *for somewhere*. Not "global", not the source's own coverage claim — a real place
whose administrative codes you can check against, because you know them.

If you cannot name the territory, you cannot do the review. Pick one you would notice a wrong number
in.

## The five checks

Tick only what you actually did. A short honest list beats a full dishonest one, and an unticked box
is the next reviewer's work, visibly waiting.

### 1. `licence`

Read the terms, not the `license:` field. Four shapes have already bitten this list:

- **Split by component** — the headline licence covers part of the data and a stricter one covers
  the rest.
- **Date-bounded** — open "as of" a date, so an older series sits under a different regime.
- **Named like an open licence and isn't** — a licence can borrow ODbL's text and forbid commercial
  use.
- **Data governed differently from the website** — a CC-BY notice can cover editorial content while
  the statistics sit under something else entirely.

You are answering: *do the terms permit what this list implies — a node reading it and publishing a
derived number?* If the answer is no, that is a finding, not a failure.

### 2. `endpoint`

Fetch it from your own machine and look inside the response.

**HTTP 200 is not the check.** The check is whether there is data in it for your place. A source can
answer 200 with an empty body, a login wall, or a page that says the service ended.

### 3. `admin-code`

Do the source's identifiers join to your territory's own codes — INE, IBGE, INEGI, FIPS, ISO 3166-2,
Permendagri/BPS, SIREN?

This is the check most likely to find something, because a wrong join produces a plausible number
rather than an error.

### 4. `vintage`

How old is the newest record, and how often does it actually move? A page that says "updated
monthly" and last moved in 2019 is a finding. Note the newest date you can see.

### 5. `field-fit`

Does the source carry the indicators the entry is filed against?

This is now concrete. An entry's `feeds_cells` names the Index cells it claims to fill, and
[`cells/`](cells/) says what filling one means. Open the cell file and read
`minimum_indicators` — those are the rows the source has to be able to produce.

## A worked example, start to finish

`social/city/eurostat-urban-audit`, read for **Barcelona**. Everything below was actually run; the
numbers are real.

The entry says `feeds_cells: ['Social|City']`, so
[`cells/social-city.yaml`](cells/social-city.yaml) is the target:

```yaml
minimum_indicators:
- name: Resident population        # count, latest
- name: Population density         # persons/km2, latest
- name: Housing cost burden or overcrowding   # percent, latest
```

**Endpoint.** The entry's `api:` is `.../statistics/1.0/data/urb_cpop1`. The obvious query fails:

```
?geo=ES002C&format=JSON
  -> 400  INVALID_QUERY_DIMENSION: Dimension "GEO" is not defined
```

Every other Eurostat dataset uses `geo`. Urban Audit uses **`cities`**. Worth knowing before you
conclude the endpoint is broken. Also: a request that is too big returns **413**, and the body says
*"Your request will be treated asynchronously. Please try again later."* — that is a queue, not a
rejection.

```
?cities=ES002C&time=2023&format=JSON&lang=EN
  -> 200, 75 indicators, 57 values
     DE1001V  Population on the 1st of January, total   3767382
```

**Admin-code — and here is the finding.** That label reads *Barcelona (greater city)*. Barcelona the
municipality is about 1.6 million. Checking the codelist:

| code | label | 2023 population |
| --- | --- | --- |
| `ES002C` | Barcelona (greater city) | 3,767,382 |
| `ES002C1` | Barcelona | **no values at all** |
| `ES002F` | Barcelona (functional urban area) | — |

`ES002C1` is the municipality, and querying it returns **HTTP 200, 37 years, zero values**. The code
exists, the request succeeds, every cell is empty.

So a reviewer who checked only the endpoint would file Barcelona's population as 3.77 million — off
by more than a factor of two — and nothing anywhere would have raised an error. That is exactly what
the `admin-code` check is for, and it took one extra query to find.

**Verdict.** `usable-with-caveats`: the source works and serves the cell, but only at greater-city
geography, and the note has to say so. It deliberately does **not** promote the entry to `live` —
a caveat is something a person should read before this list makes a claim.

## Choosing a verdict

| verdict | what it means | what it does |
| --- | --- | --- |
| `usable` | a node or a city can read this for your territory as it stands | promotes a `candidate` to `live` in the same PR |
| `usable-with-caveats` | it works, and the notes say what a reader must know first | records the reading, leaves the status alone, on purpose |
| `unusable` | it does not work for your territory, and the notes say why | records the reading so the next person does not repeat it |

If your organisation publishes the source, tick **Self-declared**. Not disqualifying — you probably
know its licence and vintage better than anyone — but a publisher's reading and an outsider's are
different kinds of evidence and a reader is entitled to know which one this is.

## The notes field is the point

Required by nothing, worth more than the rest of the file put together. The join you had to build by
hand. The rate limit. The series that ends in March without saying so. The code that returns 200 and
nothing else.

Write it for the next person, who is not you and has twenty minutes.

## Submitting

Open a [source review issue](../../issues/new?template=source-review.yml). One field per key of the
review schema, the entry id is prefilled if you came from the registry table, and that is the end of
your involvement.

A workflow then writes the review file, promotes the entry if your verdict earned it, and opens a
pull request for a maintainer to merge. You will get a comment on your issue either way — including
when something is wrong with it, which is not a rebuke, it is the parser telling you it did not want
to guess.

## Good answers that do not look like answers

- **"Blocked — it needs an account."** Several sources here are stuck behind registration. Say so
  and stop; nobody should create accounts to satisfy a checklist.
- **"Two of five checks."** File it. Three boxes unticked is three pieces of work somebody can see.
- **"The licence is unreadable."** A real finding, and more useful than a guess.
- **"It moved."** Endpoints change. A review that says where it moved to saves the next person the
  search.

---

Who can review what, and who would rather not be asked: [`REVIEWERS.md`](REVIEWERS.md). Add yourself
— especially if you maintain open data for a pledged Fab City. You are the best possible reviewer
for your own city's sources, and for the national feeds that cover it.
