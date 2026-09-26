# Report 5 template layout reference

This is a structural reference for the supplied workbook at
`capstone-official-docs/2_SEP490/Report5_Test Report.xlsx`. The copy in
`template/` must remain byte-for-byte unchanged unless the report owner
explicitly approves a new template version.

## Sheet order and used areas

| Order | Sheet name | Used area observed in the template | Editable source |
| ---: | --- | --- | --- |
| 1 | `Cover` | `A2:F17` | `00-cover/cover.md`, `00-cover/record-of-changes.md` |
| 2 | `Test Cases` | `B1:F21` | `01-test-cases/test-case-list.md` |
| 3 | `Test Statistics` | `A1:H18` | `02-test-statistics/test-statistics.md` |
| 4 | `Feature 1` | `A2:R19` | FE-02 and FE-03 sources, grouped by sheet only when exporting |
| 5 | `Feature 2` | `A2:R18` | FE-04 through FE-07 sources, grouped by sheet only when exporting |

Do not rename sheets or introduce a third feature sheet. If the project later
needs more feature groups, extend the existing feature tables or obtain an
approved Report 5 template revision first.

## `Cover`

The sheet contains project metadata followed by a record-of-change table. The
change table columns are:

`Effective Date` · `Version` · `Change Item` · `A / D / M` · `Change Description` · `Reference`

## `Test Cases`

The sheet contains project/environment metadata and a case index with these
columns, in this exact order:

`No` · `Function Name` · `Sheet Name` · `Description` · `Pre-Condition`

The working source keeps all cases in one table, including cases that belong to
both business workflows represented by a feature sheet.

## `Test Statistics`

The module summary columns are:

`No` · `Module code` · `Passed` · `Failed` · `Pending` · `N/A` · `Number of test cases`

The workbook also includes subtotal/coverage rows. Keep the formulas and
labels from the template when entering the Markdown totals.

## `Feature 1` and `Feature 2`

Both feature sheets use the same test execution columns:

`Test Case ID` · `Test Case Description` · `Test Case Procedure` ·
`Expected Results` · `Pre-conditions` · `Round 1` · `Test date` · `Tester` ·
`Round 2` · `Test date` · `Tester` · `Round 3` · `Test date` · `Tester` · `Note`

The template also has three trailing blank columns in the used range. They are
formatting space, not new fields; leave them untouched.

Each sheet groups rows under `Function A`, `Function B`, and so on. The eight
Markdown feature sources are separated by FE code; workbook rows are combined
from those files only when exporting. Each case retains its FE and WF codes.

| FE source | Workbook destination | Stable case IDs |
| --- | --- | --- |
| FE-01 identity/access governance | Supporting evidence, outside case sheets | No WFx IDs |
| FE-02 asset registry/inspection schedule | `Feature 1` | WF1-001–WF1-004 |
| FE-03 inspection request/work assignment | `Feature 1` | WF2-001–WF2-004 |
| FE-04 inspection execution/evidence | `Feature 2` | WF3-001–WF3-002 |
| FE-05 defect detection/verification | `Feature 2` | WF3-003 |
| FE-06 inspection report/approval | `Feature 2` | WF3-004 |
| FE-07 maintenance/defect resolution | `Feature 2` | WF4-001–WF4-003 |
| FE-08 dashboard/analytics/notifications | Coverage gap; no current workbook case | None assigned |

The sheet names are template labels, not SRS feature identifiers. The current
mapping is:

| Workbook sheet | Included SRS features | Included WF IDs |
| --- | --- | --- |
| `Feature 1` | FE-02 and FE-03; FE-01 gate tracked separately | WF1-001–004 and WF2-001–004 |
| `Feature 2` | FE-04, FE-05, FE-06, and FE-07 | WF3-001–004 and WF4-001–003 |

There are exactly eight FE-specific Markdown source files. The two fixed
workbook sheets are presentation groupings, not source files or SRS features.
FE-08 currently has no assigned case and remains an explicit coverage gap.

## Visual and status rules

- Preserve the template's dark navy header, green function bars, light-blue
  section bars, borders, merged cells, and spacing.
- Status values are exactly `Passed`, `Failed`, `Pending`, or `N/A`.
- Dates use `YYYY-MM-DD`.
- Do not put credentials, tokens, private keys, or personal secrets in any
  case description, note, or evidence reference.

## Pre-existing template issues

The supplied workbook contains existing formula/name problems in the project
metadata area (including `#REF!` values and an `ACTION` defined name pointing
to `#REF!`). Its Feature 1 status summary also has missing Pending/N/A formulas
and Round 2/3 summary cells reference Round 1 status data. The generated
preview corrects only those per-round summary formulas in the output copy so
the counts reflect each round; the original workbook under `template/` remains
unchanged. The metadata `#REF!` values and `ACTION` name remain untouched.
