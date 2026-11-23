# Uqbar

Uqbar is an invented city, named after the country Borges made up. Every figure for it is made up, and so are its sources, its offices and the person who sent them. It exists only in `fictional.yaml` and `observations/uqbar/`. It is not in `places.yaml`, it is in no count of places, and it never appears in the `coverage` of `index.json`.

I made it to run one city through the whole path: a row in the Airtable table `City figures`, then `scripts/copy_figures.py`, then a file in `observations/`, so that every state a figure can be in shows up once. The city is about 400,000 people. Each row carries `sent_by` "Uqbar demonstration", `sent_by_role` "invented, for the demonstration", the source names read like what they are (for example "Uqbar city waste department, annual report"), and the terms say "Invented for the demonstration". The rows were entered on 23 November 2026 and copied the same day.

## What each figure shows

| reading | what Uqbar's figure shows | state it demonstrates |
|---|---|---|
| R1 Waste | 168,000, 171,500 and 169,200 t/yr for 2023 to 2025. The 2025 row was reviewed by the team (demonstration). | three years; `candidate` for 2023 and 2024, `live` for 2025 |
| R2 Energy | 6.42, 6.38 and 6.31 million MWh/yr for 2023 to 2025. | three years, all `candidate` |
| R3 Wholesale food | The city says it does not hold the figure. | `not-held`, no value |
| R4 Material used by the region | 11.8 t per person in 2025. | one year, `candidate` |
| R5 Imports and exports | 5.4 billion UQD in 2025, from a source whose terms are "© the statistics office of Uqbar, reuse with attribution". | `candidate` with a cited source that is not open |
| R6 Businesses | 31,200 businesses in 2025 (the total, not one code). | one year, `candidate` |
| R7 Repair and reuse | 86 repair businesses in 2025. | one year, `candidate` |
| R8 Labs and workshops | 7 labs in 2025. | one year, `candidate` |
| R9 City purchasing | 940 million UQD in 2025. | one year, `candidate` |
| R10 City powers | 1, meaning yes, to one question of the powers questionnaire, 2025. | one year, `candidate` |
| R11 Access | The city sent 14.2% but did not agree to publish it. | `held`: the file carries no value, no source and no terms |
| R12 Land limits | Nothing sent, no row at all. | no file: reads "not looked for yet" |
| R13 Material coming in | 3.91, 3.98 and 3.95 million t/yr for 2023 to 2025. | three years, all `candidate` |
| R14 Exchange with member cities | 5 designs made locally that came from another member city, 2025. | one year, `candidate` |

Nineteen rows made thirteen files. R12 has none.

## The bar

A place counts when it has answered at least 8 of the 14 readings (a figure, a source, a review or "not held") and has three years for at least one of R1, R2 or R13 (design section 10).

- Answered: R1, R2, R3, R4, R5, R6, R7, R8, R9, R10, R13 and R14 carry a figure or "not held", which is 12. R11 is an answer the city chose not to release, so it is left out of that count and Uqbar still has 12. R12 is open.
- Three years: R1, R2 and R13 each have 2023, 2024 and 2025.

Uqbar clears the bar on both tests, by hand. It still counts nowhere: the bar is a way to check the path, and the place is not real.
