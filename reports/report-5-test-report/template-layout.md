# Report 5 template layout reference

This is a structural reference for the supplied workbook at
`capstone-official-docs/Report5_Test Report.xlsx`. The copy in
`template/` must remain byte-for-byte unchanged unless the report owner
explicitly approves a new template version.

## Sheet order and used areas

The supplied workbook has five sheets and two feature sheets. Generated workbooks
extend that source template with cloned feature sheets so Report 5 has twenty-four active
feature sheets (`Feature 1`–`Feature 24`), one for each current Report 3 atomic feature (`FE-01`–`FE-24`). The original file in `template/` is
unchanged. `Feature N` maps to `FE-0N` for active Report 3 sections `§§3.2–3.25` (`FE-01`–`FE-24`). Retired maintenance sheets and cases are historical and excluded.

| Order | Sheet name | Used area in the supplied template / generated output | Editable source |
| ---: | --- | --- | --- |
| 1 | `Cover` | `A2:F17` / content-driven | `00-cover/cover.md`, `00-cover/record-of-changes.md` |
| 2 | `Test Cases` | `B1:F21` / content-driven | `01-test-cases/test-case-list.md` |
| 3 | `Test Statistics` | `A1:H18` / `A1:H41` with twenty-four module rows | `02-test-statistics/test-statistics.md` |
| 4–27 | `Feature 1`–`Feature 24` | `A2:R19` / content-driven; one sheet per active FE | Matching `03-features/fe-01` through `fe-24` source |

The generator clones the official feature-sheet layout, including its widths,
styles, print settings and metadata block. It adds no rows or columns to the
execution table; it adds worksheets because the SRS has twenty-four product features.
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
all twenty-four active feature sheets.

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
to rows 11–34, pointing row N+10 at sheet `Feature N`:

- Column `C` references the sheet's `B2` Feature name.
- Columns `D:G` reference `B6:E6`, the Round 1 status counts.
- Column `H` references `B4`, the number of test cases.

So `Module code` reports the SRS feature name in the sheet's `Feature` cell
(`B2`), not the workbook sheet name. The generated workbook has twenty-four active module
rows (`11–34`). `Sub total` moves to row `35`; historical and Round 3 summaries follow, with
coverage below them:

- `Test coverage` = `(Passed + Failed) * 100 / (Number of TCs - N/A)`
- `Test successful coverage` = `Passed * 100 / (Number of TCs - N/A)`

With the active 73-case inventory (`64` historical cases + `3` unexecuted standalone cases `WF3-032`, `WF2-021`, `WF3-033` + `6` executed MF2 manager-flow cases `WF2-022`–`WF2-027`), Round 1 has `51 Passed`, `0 Failed`, `9 Pending`, and `13 N/A` (`51 / 60 = 85.00%`). Retired maintenance cases are excluded from active counts. Keep workbook formulas and change underlying statuses in the feature Markdown files.

The generated statistics sheet places twenty-four module rows at `11–34`, current Round 1
subtotal at row `35`, historical active-scope Round 1 at row `36` (`45/0/8/3/56`), Round 3 executed
cases at row `37` (`13/13`), the V29 Round 3 subset at row `38` (`2/2`), spacer at row `39`, and coverage
at rows `40–41` (`83.33%`). Round 3 executed totals include only Passed/Failed cases
(`13` cases: `WF3-005`, `WF3-006`, `WF3-009`, `WF3-016`, `WF3-018`, `WF3-019`, `WF3-021`, `WF3-026`–`WF3-031`). The V29 subset covers `WF3-018` and `WF3-019`, both Round 3 `Passed`.

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
| `FE-01` Account Authentication, OTP & 4-Role Access Control (`§3.2`) | `Feature 1` | `WF1-001`, `WF1-003`–`005`, `WF1-022`, `WF2-019`, `WF2-020` (7 cases) |
| `FE-02` Partner Inspector Application & Qualification Management (`§3.3`) | `Feature 2` | `WF1-006`–`008`, `WF1-010` (4 cases) |
| `FE-03` Inspector-Owned Drone Registration & Fleet Management (`§3.4`) | `Feature 3` | `WF1-014`–`016` (3 cases) |
| `FE-04` Interactive Location Map & No-Fly Zone Airspace Screening (`§3.5`) | `Feature 4` | `WF1-002`, `WF2-004`, `WF2-005` (3 cases) |
| `FE-05` Financial History & Revenue/Payment Ledger (`§3.6`) | `Feature 5` | `WF3-032` (1 case; `N/A / Pending / Pending`) |
| `FE-06` Building Asset Registry, Checkpoints & Reference Documents (`§3.7`) | `Feature 6` | `WF1-011`–`013` (3 cases) |
| `FE-07` Restricted Airspace Review & Clearance Decision (`§3.8`) | `Feature 7` | `WF1-009` (1 case) |
| `FE-08` Service Requests (One-Time & Recurring) & VND Quotations (`§3.9`) | `Feature 8` | `WF1-017`–`019` (3 cases) |
| `FE-09` Offline Signed Contract & Occurrence Dispatch Scheduling (`§3.10`) | `Feature 9` | `WF1-021`, `WF2-002`, `WF2-003`, `WF2-015`, `WF2-016` (5 cases) |
| `FE-10` Dual-Channel Messaging (Order Chat & Inspection Chat) (`§3.11`) | `Feature 10` | `WF2-001` (1 case) |
| `FE-11` Assignment Acceptance Timeout & Escalation Handling (`§3.12`) | `Feature 11` | `WF2-021` (1 case; `N/A / Pending / Pending`) |
| `FE-12` System Notifications & Alert Center (`§3.13`) | `Feature 12` | `WF1-020` (1 case) |
| `FE-13` Flight Permit Upload & Independent Verification Gate (`§3.14`) | `Feature 13` | `WF2-008`, `WF2-009` (2 cases) |
| `FE-14` On-Site Field Session & SmartDroneHub MAVLink Telemetry (`§3.15`) | `Feature 14` | `WF2-011`, `WF2-012`, `WF2-017`, `WF2-018`, `WF3-020` (5 cases) |
| `FE-15` Field Evidence Intake & Chunked Video Processing Pipeline (`§3.16`) | `Feature 15` | `WF3-002`, `WF3-022`–`025` (5 cases) |
| `FE-16` AI Defect Detection (`YOLO11` + Vision Fallback) & Findings Confirmation (`§3.17`) | `Feature 16` | `WF3-001`, `WF3-003`, `WF3-004`, `WF3-007`, `WF3-008`, `WF3-010`, `WF3-017` (7 cases) |
| `FE-17` AI Case/Standard Retrieval (`pgvector` RAG), Note Drafting & Report Summary (`§3.18`) | `Feature 17` | `WF3-029`, `WF3-030` (2 cases) |
| `FE-18` Inspection Report Compilation, Independent Review & Official Publication (`§3.19`) | `Feature 18` | `WF3-005`, `WF3-006`, `WF3-009`, `WF3-016` (4 cases) |
| `FE-19` Customer Report Acceptance & Clarification Workflow (`§3.20`) | `Feature 19` | `WF3-012` (1 case) |
| `FE-20` Online Service Fee Payment (`Sepay` VietQR & `VNPay`) (`§3.21`) | `Feature 20` | `WF3-018`, `WF3-019` (2 cases) |
| `FE-21` Payment Deadlines, Invoices & Payment Document Management (`§3.22`) | `Feature 21` | `WF3-026`, `WF3-027` (2 cases) |
| `FE-22` Partner Inspector Payout Reconciliation (`§3.23`) | `Feature 22` | `WF3-033` (1 case; `N/A / Pending / Pending`) |
| `FE-23` Evidence-Backed Refunds & Receivable Recovery (`§3.24`) | `Feature 23` | `WF3-021` (1 case) |
| `FE-24` Post-Remediation Re-inspection & Defect Verification (`§3.25`) | `Feature 24` | `WF3-028`, `WF3-031` (2 cases) |

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
