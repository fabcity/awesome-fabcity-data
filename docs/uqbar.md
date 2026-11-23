# Uqbar

Uqbar is an invented city, named after the country Borges made up. Every figure for it is made up, and so are its sources, its offices and the person who sent them. It exists only in `fictional.yaml` and `observations/uqbar/`. It is not in `places.yaml`, so no count of places includes it and it never appears in the `coverage` of `index.json`.

I made it to run one city through the whole path. A figure starts as a row in the Airtable table `City figures`, `scripts/copy_figures.py` copies it, and it ends up as a file in `observations/`. Every state a figure can be in shows up at least once. The city has about 400,000 people. Each row says `sent_by` is "Uqbar demonstration" and `sent_by_role` is "invented, for the demonstration". The source names read like what they are, for example "Uqbar city waste department, annual report", and the terms say "Invented for the demonstration". I entered the rows on 23 November 2026 and copied them the same day.

A reading with two parts is sent as two figures with different units. R1 asks for tonnes and for the share collected separately, so Uqbar has both for each year, and the copy keeps both.

## What each figure shows

| reading | what Uqbar's figure shows | state it demonstrates |
|---|---|---|
| R1 Waste | 168,000, 171,500 and 169,200 t/yr for 2023 to 2025, and 31.5%, 33.8% and 36.2% collected separately. The 2025 rows were reviewed by the team (demonstration). | three years in two units; `candidate` for 2023 and 2024, `live` for 2025 |
| R2 Energy | 6.42, 6.38 and 6.31 million MWh/yr for 2023 to 2025. | three years, all `candidate` |
| R3 Wholesale food | The city says it does not hold the figure. | `not-held`, no value |
| R4 Material used by the region | 11.8 t per person in 2025. | one year, `candidate` |
| R5 Imports and exports | 5.4 billion UQD in 2025, from a source whose terms are "© the statistics office of Uqbar, reuse with attribution". | `candidate` with a cited source that is not open |
| R6 Businesses | 31,200 businesses in 2025 (the total, not one code). | one year, `candidate` |
| R7 Repair and reuse | 86 repair businesses in 2025. | one year, `candidate` |
| R8 Labs and workshops | 7 labs in 2025. | one year, `candidate` |
| R9 City purchasing | 940 million UQD in 2025. | one year, `candidate` |
| R10 City powers | 3 of the 4 powers held in 2025 (taxes it can levy, land it owns, utilities it runs, rules for its own purchasing). | one year, `candidate` |
| R11 Access | The city sent 14.2% but did not agree to publish it. | `held`: the file carries no value, no source and no terms |
| R12 Land limits | Nothing sent, no row at all. | no file: reads "not looked for yet" |
| R13 Material coming in | 3.91, 3.98 and 3.95 million t/yr for 2023 to 2025. | three years, all `candidate` |
| R14 Exchange with member cities | 5 designs made locally that came from another member city, 2025. | one year, `candidate` |

Twenty-two rows made thirteen files. R12 has none.

## The bar

A place counts when it has answered at least 8 of the 14 readings (a figure, a source, a review or "not held") and has three years for at least one of R1, R2 or R13 (design section 10).

Uqbar has answered 12 readings. R1, R2, R4 to R10, R13 and R14 carry a figure, and R3 says the city does not hold it. R11 is an answer the city chose not to release, so I left it out of the count, and R12 is still open. R1, R2 and R13 each have 2023, 2024 and 2025.

Uqbar clears the bar on both tests, checked by hand. It still counts nowhere, because the bar only checks the path and the place is not real.
