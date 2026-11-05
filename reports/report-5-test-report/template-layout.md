# Report 5 template layout reference

This is a structural reference for the supplied workbook at
`capstone-official-docs/Report5_Test Report.xlsx`. The copy in
`template/` must remain byte-for-byte unchanged unless the report owner
explicitly approves a new template version.

## Sheet order and used areas

The supplied workbook has five sheets and two feature sheets. Generated workbooks
extend that source template with six cloned feature sheets so Report 5 has one
feature sheet for each Report 3 feature. The original file in `template/` is
unchanged. `Feature N` maps to `FE-0N` (Report 3 §§3.2–3.9).

| Order | Sheet name | Used area in the supplied template / generated output | Editable source |
| ---: | --- | --- | --- |
| 1 | `Cover` | `A2:F17` / content-driven | `00-cover/cover.md`, `00-cover/record-of-changes.md` |
| 2 | `Test Cases` | `B1:F21` / content-driven | `01-test-cases/test-case-list.md` |
| 3 | `Test Statistics` | `A1:H18` / `A1:H22` with eight module rows | `02-test-statistics/test-statistics.md` |
| 4–11 | `Feature 1`–`Feature 8` | `A2:R19` / content-driven; one sheet per FE | Matching `03-features/fe-01` through `fe-08` source |

The generator clones the official feature-sheet layout, including its widths,
styles, print settings and metadata block. It adds no rows or columns to the
execution table; it adds worksheets because the SRS has eight product features.
Adding or reordering an SRS FE requires updating case routing and the summary
row together.

## `Cover`

The sheet contains project metadata followed by a record-of-change table. The
change table columns are, verbatim from row 10:

`Effective Date` · `Version` · `Change Item` · `*A,D,M` · `Change description` · `Reference`

Earlier drafts of these sources headed this table `A / D / M` and `Change
Description`. Those were normalised English, not the template's labels; the
template itself reads `*A,D,M` and `Change description`. Use the template's own
text so a copied value lands in a column whose header already matches.

## `Test Cases`

The sheet contains project/environment metadata and a case index with these
columns, in this exact order:

`No` · `Function Name` · `Sheet Name` · `Description` · `Pre-Condition`

The working source keeps all cases in one table, including cases that belong to
all eight feature sheets.

**Sheet-name spacing.** The template's own placeholder cells in `Sheet Name`
read `Feature1` and `Feature2` (no space, `D9:D13`), while the actual sheet tabs
are `Feature 1` and `Feature 2` (with a space). The Markdown sources use the
tab names with a space, because that is what identifies the destination sheet.
Whoever exports must not copy the unspaced placeholder into the cell: it would
point at a sheet that does not exist.

## `Test Statistics`

The module summary columns are:

`No` · `Module code` · `Passed` · `Failed` · `Pending` · `N/A` · `Number of  test cases`

Note the double space in the template's own last header — `H10` reads
`Number of  test cases`. The Markdown tables spell it with single spacing so
they stay internally consistent; the spacing difference is cosmetic and does not
affect an export, because the workbook keeps its own header cell.

In the supplied template, module rows 11–12 contain formulas that point to
`Feature 1` and `Feature 2`. Generated workbooks extend the same mapping pattern
to rows 11–18, pointing row N+10 at sheet `Feature N`:

- Column `C` references the sheet's `B2` Feature name.
- Columns `D:G` reference `B6:E6`, the Round 1 status counts.
- Column `H` references `B4`, the number of test cases.

So `Module code` reports the SRS feature name in the sheet's `Feature` cell
(`B2`), not the workbook sheet name. The generated workbook has eight module
rows. `Sub total` moves to row 19 and sums the eight feature rows; coverage is
computed from it at rows 21–22:

- `Test coverage` = `(Passed + Failed) * 100 / (Number of TCs - N/A)`
- `Test successful coverage` = `Passed * 100 / (Number of TCs - N/A)`

With the current 67-case inventory, Round 1 has `60 Passed`, `0 Failed`, `5
Pending`, and `2 N/A`; the two N/A cases were added for V29 after Round 1. The
historical Round 1 subtotal remains 65 cases (`60 Passed`, `5 Pending`, `0
Failed`, `0 N/A`), so the historical coverage remains `92.31%`; pending cases
remain in the denominator. Keep workbook formulas; change underlying statuses
in the feature Markdown files.

The generated statistics sheet places the current Round 1 subtotal at row 19,
the historical Round 1 subtotal at row 20, Round 3 executed cases at row 21,
the V29 Round 3 subset at row 22, the spacer at row 23, and coverage at rows
24–25. Round 3 executed totals include only Passed/Failed cases: four in total,
including WF3-018/019 as the two-case V29 subset.

## Feature sheets (supplied template and generated workbook)

The supplied template's `Feature 1` and `Feature 2`, and the six cloned sheets
in generated outputs, use the same test execution columns:

`Test Case ID` · `Test Case Description` · `Test Case Procedure` ·
`Expected Results` · `Pre-conditions` · `Round 1` · `Test date` · `Tester` ·
`Round 2` · `Test date` · `Tester` · `Round 3` · `Test date` · `Tester` · `Note`

The used range also extends to `R`, but only `A10:O10` are execution headers.
The three trailing columns are **not** additional case fields:

| Column | Content | Border |
| --- | --- | --- |
| `P` | empty | none |
| `Q` | empty, but `Q10` carries a background fill | none |
| `R` | `R2:R5` hold the status legend `Passed`, `Failed`, `Pending`, `N/A` | none |

`R2:R5` is a legend, not data: it repeats the four status words the round
summary above counts. It sits outside the bordered summary block, which spans
`A2:E8` only, and outside the bordered case table, which spans `A10:O…`. The
`Q10` fill is a leftover — the cell has no header text and no border.

Leave `P:R` alone. Copying a case row into `P:Q` would push content past the
table's right edge, and typing over `R2:R5` would destroy the legend.

### Per-sheet summary block (`A2:E8`)

Every generated feature sheet repeats this block above the case table, fully
bordered (`B2:E2`, `B3:E3` and `B4:E4` are merged), and `Test Statistics` reads
its values back out by formula:

| Cell | Label | Formula |
| --- | --- | --- |
| `A2`/`B2` | `Feature` | Feature name, e.g. `Evidence Intake, YOLO11 Detection, Auto-Compiled Report & PayOS` |
| `A3`/`B3` | `Test requirement` | One-line description of what this sheet tests |
| `A4`/`B4` | `Number of TCs` | Supplied template: `=COUNTA(A12:A1000)` / `=COUNTA(A12:A998)`. Generated copies count only stable WFx case IDs in `A11:A1000`, excluding FE function bars. |
| `A5:E5` | `Testing Round` | Column headers `Passed`, `Failed`, `Pending`, `N/A` |
| `A6`/`B6:E6` | `Round 1` | `=COUNTIF($F$11:$F$1000, B$5)` etc. |
| `A7`/`B7:E7` | `Round 2` | `=COUNTIF($I$11:$I$1000, B$5)` etc. |
| `A8`/`B8:E8` | `Round 3` | `=COUNTIF($L$11:$L$1000, B$5)` etc. |

`Number of TCs` and the per-round counts are workbook formulas over the case
rows, so they need no Markdown source. `Feature` name and `Test requirement`
are typed values with no formula behind them, and the Markdown equivalent is
the `Feature sheet summary` table in each matching `fe-0N-…md` file. Populate
`B2`/`B3` on every sheet because the `Test Statistics` module rows read every
`Feature N!B2`.

| FE source | Workbook destination | Stable case IDs |
| --- | --- | --- |
| FE-01 Authentication, Google OAuth2 & 5-Role Access Control (§3.2) | `Feature 1` | WF1-001 to WF1-005 (5 cases) |
| FE-02 Partner Onboarding, Workforce, Asset & Inspector Drone Registry (§3.3) | `Feature 2` | WF1-006 to WF1-016 (11 cases) |
| FE-03 Recurring Service Requests, Contract Occurrences & Outbox Notifications (§3.4) | `Feature 3` | WF1-017 to WF1-021 (5 cases) |
| FE-04 Service Requests, Quotations, Contracts, Dispatch & Airspace Map (§3.5) | `Feature 4` | WF2-001 to WF2-005 (5 cases) |
| FE-05 Flight Permit Gate, Field Execution, Dashboard & Calendar (§3.6) | `Feature 5` | WF2-008, WF2-009, WF2-011, WF2-012, WF2-015 to WF2-020, WF3-009 (11 cases) |
| FE-06 Evidence Intake, YOLO11 Detection, Auto-Compiled Report & PayOS (§3.7) | `Feature 6` | WF3-001 to WF3-008, WF3-010, WF3-012, WF3-016 to WF3-019 (14 cases) |
| FE-07 Maintenance Work Orders, RAG Scope/Norms Advisor & Repair Execution (§3.8) | `Feature 7` | WF4-001 to WF4-011 (11 cases) |
| FE-08 Completion Report, 3-Way Re-inspection Verification & Cost Closure (§3.9) | `Feature 8` | WF4-012 to WF4-016 (5 cases) |

All 67 current cases are distributed across `Feature 1` through `Feature 8`
(`5 + 11 + 5 + 5 + 11 + 14 + 11 + 5 = 67`):

| Workbook sheet | Included SRS feature | Included WF IDs |
| --- | --- | --- |
| `Feature 1` | FE-01 — Authentication, Google OAuth2 & 5-Role Access Control | WF1-001 to WF1-005 |
| `Feature 2` | FE-02 — Partner Onboarding, Workforce, Asset & Inspector Drone Registry | WF1-006 to WF1-016 |
| `Feature 3` | FE-03 — Recurring Service Requests, Contract Occurrences & Outbox Notifications | WF1-017 to WF1-021 |
| `Feature 4` | FE-04 — Service Requests, Quotations, Contracts, Dispatch & Airspace Map | WF2-001 to WF2-005 |
| `Feature 5` | FE-05 — Flight Permit Gate, Field Execution, Dashboard & Calendar | WF2-008, WF2-009, WF2-011, WF2-012, WF2-015 to WF2-020, WF3-009 |
| `Feature 6` | FE-06 — Evidence Intake, YOLO11 Detection, Auto-Compiled Report & PayOS | WF3-001 to WF3-008, WF3-010, WF3-012, WF3-016 to WF3-019 |
| `Feature 7` | FE-07 — Maintenance Work Orders, RAG Scope/Norms Advisor & Repair Execution | WF4-001 to WF4-011 |
| `Feature 8` | FE-08 — Completion Report, 3-Way Re-inspection Verification & Cost Closure | WF4-012 to WF4-016 |

## Visual and status rules

- Preserve the template's header, function bars, section bars, borders, merged
  cells, and spacing. Open the workbook and copy the existing cell styles; do
  not re-create them from a description.
- Status values are exactly `Passed`, `Failed`, `Pending`, or `N/A`.
- Dates use `YYYY-MM-DD`.
- Do not put credentials, tokens, private keys, or personal secrets in any
  case description, note, or evidence reference.

### Metadata blocks to fill on export

Each sheet has a metadata area above its table. `Cover` has **no merge** on
`Version` — it is a plain label/value pair at `E6`, unlike the merged value
cells beside it:

| Sheet | Merged cells | Labels and their value cells |
| --- | --- | --- |
| `Cover` | `B2:F2`, `B4:D4`, `B5:D5`, `B6:D6` | `TEST REPORT DOCUMENT`; `Project Name` `B4`, `Project Code` `B5`, `Document Code` `B6`, `Creator` `F4` (`E4` label), `Issue Date` `F5`, `Version` `F6` (`E6` label) |
| `Test Cases` | `B3:C3`, `B4:C4`, `B5:C5`, `D3:F3`, `D4:F4`, `D5:F5` | `Project Name` `D3`, `Project Code` `D4`, `Test Environment Setup Description` `D5` |
| `Test Statistics` | `B1:H1`, `C3:D3`, `C4:D4`, `C5:D5`, `C6:H6`, `E3:F3`, `E4:F4`, `E5:F5` | `TEST STATISTICS`; `Project Name` `C3`, `Project Code` `C4`, `Document Code` `C5`, `Notes` `C6`, `Creator` `G3`, `Reviewer/Approver` `G4`, `Issue Date` `H5` |

## Pre-existing template issues

These were verified by reading the workbook directly. `template/` is
byte-for-byte identical to the supplied workbook (both SHA-256
`DE84DD6F…F4D1`), so the same defects exist in both copies.

1. **`Test Cases!D3` and `D4` are `=#REF!`.** The project name and project code
   on the `Test Cases` sheet do not resolve.
2. **A defined name `ACTION` points to `#REF!`,** at workbook level and again
   scoped to `Cover`. It appears to be an unused leftover from an earlier
   macro.
3. **Both feature sheets' Round 2 and Round 3 summary rows count the Round 1
   column.** `Feature 1` `B7:E7` and `B8:E8` use `=COUNTIF($F10:$F998, …)`, the
   same `$F` range as Round 1 (`$F` is the `Round 1` status column). `Feature 2`
   does the same with `$F10:$F996`. Column `$I` holds Round 2 and `$L` holds
   Round 3, so the Round 2/3 summaries in the raw template mirror Round 1
   instead of counting their own column.
4. **`Feature 2!A18` holds a stray `6`** below the last case row, where the
   template expects a case ID or a `Function` bar.

## Generated copies

The independent exporter [export_report5.py](../../tools/export_report5.py)
uses this original workbook as a read-only format source. It clones the
original case/function/history row styles, preserving sheet names, column
order, widths, legend, comments, printer settings and theme/style parts.

In output copies only, case totals use `COUNTIF` over stable WFx IDs so
function bars are not counted as cases; Round 2/3 use the `I`/`L` status
columns, and zero-case coverage is guarded. The template calculation chain
contains references to metadata formulas replaced by source values; it is
removed with its relationship/content-type entry so Excel can rebuild that
non-format index. No original template is modified.
