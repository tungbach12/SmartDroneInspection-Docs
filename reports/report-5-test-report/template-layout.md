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
| 4 | `Feature 1` | `A2:R19` | `03-features/feature-1.md` |
| 5 | `Feature 2` | `A2:R18` | `03-features/feature-2.md` |

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

Each sheet groups rows under `Function A`, `Function B`, and so on. The
Markdown files preserve those function headings while adding the current FE
feature code and retaining the WF business-flow code in the heading text.

The sheet names are template labels, not SRS feature identifiers. The current
mapping is:

| Workbook sheet | Included SRS features | Included WF IDs |
| --- | --- | --- |
| `Feature 1` | FE-02 and FE-03; FE-01 gate tracked separately | WF1-001–004 and WF2-001–004 |
| `Feature 2` | FE-04, FE-05, FE-06, and FE-07 | WF3-001–004 and WF4-001–003 |

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
to `#REF!`). They are documented here so they are not mistaken for a newly
introduced test failure. Do not silently change them while filling cases.
