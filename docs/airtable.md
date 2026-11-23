# Where the data track lives in Airtable

Base `appmNQaDGEFE9VcYh` ("FCI Observations", Fab City Foundation workspace). Made 23 November 2026. No token is kept here.

Existing tables, left as they were: `Observations` (`tbl8VZoGMr6kdE4QX`), the prototype's public feed, which this track leaves alone, `Data Sources`, `Reviewers`, `FCI Coverage Tracker` (`tbl9tfpEsxoxQAh0w`). The only change to the tracker is a reverse link field `Cohort` (`fldMwBgyzM8e6fmFh`).

## Readings (`tblQTZ5xv3Cx1RXBm`)

Copied one way from `readings.yaml` by `scripts/sync_airtable.py --write`. All fourteen rows exist, R1 to R14, last synced 23 November 2026. R1 is `recXEOmoelK9Vtm20`.

| field | id | type |
|---|---|---|
| id (primary) | fldeWFhpmIbqQkdjr | single line text |
| name | fldDfi1JudpcaGLBh | single line text |
| plain | fldIlZadaUAuEaMob | long text |
| unit | fldu3Mo5mTKf43cmq | single line text |
| years | fld9EewRpKfxa2ahE | single line text |
| held_by | fldqKJnKOo8Qa78v0 | single line text |
| tests | fldZNRiUbghqBXArK | single line text |
| cells | fldCFfGqjMSBY0qbu | single line text |
| last_synced | fld1l51sgtwBoe2Nx | date |
| City figures (reverse link) | fldDGM2GYlKpCwp6A | link |

## City figures (`tblgsmFzzFYy0iCbC`)

| field | id | type |
|---|---|---|
| place (primary) | fldYu2PYEOJfMXTcW | single line text |
| reading | fldjIuwBpGS0CGzDV | link to Readings |
| year | fldQMCOKb45uHo0Zx | number, 0 decimals |
| value | fldzf6ud2USILM7Sm | number, 4 decimals |
| unit | fldBASPkx0l99UI9b | single line text |
| district | fldBUmgLkfQvkYD6i | single line text |
| source_url | fldnVgM4SbFf6L9j7 | url |
| source_name | fldWwZcOJPSSzU95q | single line text |
| terms | fldqwDMvQX1Vf3IXT | long text |
| not_held | fldMjrXBz04NwcHfm | checkbox |
| sent_by | fld0uT1cAzMeXcts0 | single line text |
| sent_by_role | fldf66ckr3ro5U7Qv | single line text |
| may_publish | fldBeBOpR3znY6liQ | single select: yes, no, ask |
| state | fldtmxmNwwmFgr4mX | single select: sent, needs a fix, copied, checked |
| team_note | fld24Kk9UKKN53Isz | long text |
| checked_by | fldP7Zz0m3i3yZkLc | single line text |
| checked_on | fldjLVF1zZN6B81Fs | date |
| copied_on | fldfPQcrpYa0tQXff | date |
| fictional | fldFw3FQhjjZhxXjg | checkbox |
| reading_id | fldhPl2VRiyugO4eJ | lookup of Readings.id |
| sender_note | fld4FMryaJZu7kw43 | long text |

`state` has no default, so a row from the form arrives with `state` empty, and the copy reads empty as `sent`.

`sender_note` (added 23 November 2026) holds anything the sender wants to tell the Fab City team, in any language. It stays in Airtable. `scripts/copy_figures.py` never copies it.

`scripts/copy_figures.py` copies this table one way into `observations/`, and its docstring says what goes out and what stays here. It only reads Airtable. `.github/workflows/figures-to-pr.yml` runs it daily once the repository secret `AIRTABLE_TOKEN` is set; until then it runs by hand on an export of the whole table: `python3 scripts/copy_figures.py --records rows.json --write`. Export every row, not a selection: a withdrawal only counts while its row is in the listing.

The team reads the skipped list in each daily figures pull request. When every record is skipped and `observations/` has nothing new, no pull request opens, and the list is only in the log of the workflow's step "Copy the figures". A skipped record is fixed in Airtable, and the next run picks it up.

## Cohort (`tblefySK5wVdZWnHu`)

| field | id | type |
|---|---|---|
| place (primary) | fld3uvJZYQcOeaXPA | single line text, the place slug |
| name | fldV21oNP6IQAoM9h | single line text |
| followed | fldFv97quuX8ysidg | single select: core, optional |
| lead_name | fldrwVPBTDoztko9d | single line text |
| lead_role | fldtqL9zSR5KOtvhS | single line text |
| city_rep_name | fldUYHphOO25hflbD | single line text |
| city_rep_role | fldFyNqDvN2jCVPzo | single line text |
| request_sent_on | fldHzTB7iVP8uvb0k | date |
| next_follow_up | fld786iSF9U9ZnJaF | date |
| follow_up_by | fldtPmeWx0xiWXAEd | single line text, `Lars` on all fifteen rows |
| FCI Coverage Tracker | fldoP3DT7CXIrFXTe | link to the tracker row with the same Locality |

The connector cannot set a default value, so `follow_up_by` is typed on each row; a new row needs it typed. Fifteen rows: ten core (barcelona, bali, boston, charlotte, santiago-de-chile, hamburg, montreal, paris, amsterdam, oulu) and five optional (kamakura, seoul, shenzhen, goa, kerala). Every one is linked to its tracker row. No contact details are held.

## The form "Send a figure"

Page `pagsz9HlBft5pJIP8`, a standalone form on `City figures`. It is published to the base and is not yet public (see the open point below). The question that fills `sender_note` is in the working draft.

- Form address: `https://airtable.com/appmNQaDGEFE9VcYh/pagsz9HlBft5pJIP8/form`
- Share settings: `https://airtable.com/appmNQaDGEFE9VcYh/pagsz9HlBft5pJIP8/form?share=show`
- Editor: `https://airtable.com/appmNQaDGEFE9VcYh/pagsz9HlBft5pJIP8/edit`

It asks for place, reading, year, value, unit, district, source link, source name, terms of use, "my city does not hold this figure", name, role and "may we publish it". Place, reading, name and "may we publish it" are required. The internal fields (`state`, `team_note`, `checked_by`, `checked_on`, `copied_on`, `fictional`) are not on the form.

The working draft has changes the published form does not have yet. The last question, "Anything you want to tell us, in any language", fills `sender_note`. Year is required, and its help says that for a reading the city does not hold, it gives the latest year it looked. The role's help asks for a role, such as data officer at the city council. They reach the live form the next time someone publishes it. The connector can publish, and publishing is Tomas's call.

### Open point: public access and prefill, not yet confirmed

When I opened the address above in a browser with no Airtable session it went to the Airtable sign-in page, so the form is not yet open to anyone with the link. The connector can publish a form but cannot turn on "anyone with the link can fill in"; that is a switch in the share settings page above, and someone signed in has to flip it.

For the same reason prefill is untested. The page `/operate/city-data` (fci-ingestion-tool, `formUrl` in `js/city-data.js`) prefills the form with the table's field names, `prefill_place` and `prefill_reading`:

```
https://airtable.com/appmNQaDGEFE9VcYh/pagsz9HlBft5pJIP8/form?prefill_place=uqbar&prefill_reading=R1
```

It embeds the same form from `https://airtable.com/embed/appmNQaDGEFE9VcYh/pagsz9HlBft5pJIP8/form` with the same two parameters. A linked-record field is normally prefilled with the linked row's primary field, here `R1`, the `id` of the Readings row. Once the form is public, open the address above and check that Place reads `uqbar` and Reading reads `R1`. If it does not, try the form's labels instead (`prefill_Place`, `prefill_Reading`); `formUrl` is the one place to change. If the page-style form refuses both, the fallback is a form made in Airtable's older Forms view of the grid, which accepts them.

## The team view

Grid view `viw66ZB5HWVZc3FEk` on `City figures`, named "By place and reading", grouped by `place` then `reading`, both ascending. It does not put followed places first, because `City figures` has no field that says whether a place is followed. A lookup from `Cohort.followed` would do it, and none has been added.
