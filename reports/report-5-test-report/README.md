# Report 5 — Test Report working folder

This folder separates the contents of the supplied `Report5_Test Report.xlsx`
template so the team can update test cases without repeatedly rebuilding the
whole workbook.

## Naming layers and mapping

`Feature 1` and `Feature 2` are fixed workbook sheet names from the supplied
template. They are not the SRS feature codes `FE-01` and `FE-02`.

| Layer | Meaning | Example |
| --- | --- | --- |
| Workbook sheet | Fixed Report 5 grouping | `Feature 2` |
| SRS feature | Product capability from Report 3 | `FE-07 — Maintenance and Defect Resolution` |
| WF test ID | Business-flow traceability ID | `WF4-001` |

The template combines business flows across its two feature sheets. Therefore
`WF4-001` in the `Feature 2` sheet is correct: it is an FE-07 test case from
WF4, not an FE-02 test case. Do not rename the files or IDs to make the sheet
number look like an SRS feature code.

## Source of truth and template rule

- `template/Report5_Test Report.xlsx` is an unchanged copy of the supplied
  workbook. Do not edit this copy to add new sections or rename sheets.
- The Markdown files are the editable working source. Keep test case IDs
  stable when a case is reworded or re-tested.
- When the report is ready for submission, copy the Markdown values into the
  workbook while preserving the template's sheet names, order, column order,
  status vocabulary, colours, and table layout.
- The source template is intentionally not “corrected” here. Its existing
  formula/name issues, including `#REF!` values in the project metadata area,
  are recorded in [template-layout.md](template-layout.md) and should be
  handled only with the report owner’s approval.

## Folder map

| Folder/file | Workbook area | Purpose |
| --- | --- | --- |
| `00-cover/` | `Cover` | Project metadata and record of changes. |
| `01-test-cases/` | `Test Cases` | The index of all cases and their preconditions. |
| `02-test-statistics/` | `Test Statistics` | Module totals, coverage, and execution summary. |
| `03-features/feature-1.md` | `Feature 1` sheet | WF1/FE-02 and WF2/FE-03 cases; FE-01 gate is recorded separately. |
| `03-features/feature-2.md` | `Feature 2` sheet | WF3/FE-04–FE-06 and WF4/FE-07 cases. |
| `template-layout.md` | All sheets | Exact sheet, column, and section reference. |
| `template/Report5_Test Report.xlsx` | All sheets | Original-format workbook copy. |

## Current test scope

The working cases cover the four main business flows without testing drone
flight control. The fixed workbook sheets combine these groups, while FE codes
identify SRS capabilities and WF codes retain business-flow traceability:

1. FE-01 — identity/access foundation, including the W3 auth/migration smoke gate and shared API contract supporting checks. These supporting gates are documented separately and are not additional functional workbook cases.
2. FE-02 — asset and inspection scheduling (WF1; `WF1-001`–`WF1-004`).
3. FE-03 — client request, quotation/order, and service assignment (WF2; `WF2-001`–`WF2-004`).
4. FE-04 — inspection execution and evidence (WF3; `WF3-001`–`WF3-002`).
5. FE-05 — YOLO-assisted defect detection and verification (WF3; `WF3-003`).
6. FE-06 — inspection report and approval (WF3; `WF3-004`).
7. FE-07 — maintenance ticket, assessment/execution, rework, and billing status (WF4; `WF4-001`–`WF4-003`).

The FE-01 W3 auth/migration smoke gate is tracked by Jira `SCRUM-58/T001` under
`SCRUM-108`; it is a delivery gate and is not counted as one of the 15
functional Report 5 cases. MinIO/evidence storage is tracked separately under
FE-04/WF3 task `T025/SCRUM-85`. CI uses S3Mock for S3 API integration coverage;
that mock does not replace runtime verification against MinIO.

Current role codes are `ADMIN`, `CLIENT`, `SERVICE_MANAGER`, `INSPECTOR`, and
`MAINTENANCE_ENGINEER`. A role check never replaces organization ownership,
assignment, or separation-of-duties checks.

## Editing workflow

1. Add or update the case in the appropriate feature file first.
2. Keep the existing ID format (`WF1-001`, `WF2-001`, `WF3-001`, `WF4-001`)
   stable. Add the mapped FE code in the function name or mapping note; do not
   interpret the workbook sheet number as the FE code.
3. Mirror every case in `01-test-cases/test-case-list.md`.
4. Record execution only in the matching Round 1, Round 2, or Round 3 cell.
   Use only `Passed`, `Failed`, `Pending`, or `N/A`.
5. Update the corresponding module row and totals in
   `02-test-statistics/test-statistics.md`.
6. Before exporting, check that the number of cases, IDs, statuses, dates, and
   testers agree across all Markdown files and the workbook.

## Execution status convention

- `Pending`: the case is defined but has not completed that round.
- `Passed`: expected result was observed and evidence is available.
- `Failed`: the result differs from the expected result; link the defect in
  the `Note` column.
- `N/A`: the round is intentionally not applicable and has an explanation in
  `Note`.

Dates use `YYYY-MM-DD`; leave the date and tester blank until the round is
actually executed. Do not put passwords, tokens, private keys, or customer
secrets in test evidence or notes.
