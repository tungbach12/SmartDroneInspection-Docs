# Report 5 — Test Report working folder

This folder separates the contents of the supplied `Report5_Test Report.xlsx`
template so the team can update test cases without repeatedly rebuilding the
whole workbook.

**Scope (updated 2026-10-10):** This report records the two re-verified MF2-07
readiness cases, selected MF3 cases, and three executed MF4 backend API cases
for the four roles (`ADMIN`, `ORG_ADMIN`, `INSPECTOR`, `MAINTENANCE_ENGINEER`).
The 2026-10-09 reset removed 28 retired/unimplemented cases; their IDs remain
reserved. The MF2 readiness cases were re-integrated onto current `origin/main`
and verified; three FE-07 cases were added for the tested MF4 backend slice.
Every indexed case has executed Round 1 evidence.

This is **not full product or SRS coverage**. MF1, MF2 outside MF2-07, and the
remaining MF4 requirements—skills/credential administration, notifications,
linked MF1 re-inspection dispatch, evidence object/report rendering and
maintenance web/mobile clients—remain unverified. The original workbook and
preview output remain unchanged.

## Naming layers and mapping

`Feature 1` and `Feature 2` are fixed workbook sheet names from the supplied
template. They are not the SRS feature codes `FE-01` and `FE-02`.

| Layer | Meaning | Example |
| --- | --- | --- |
| Workbook sheet | Fixed Report 5 grouping | `Feature 2` |
| SRS feature | Product capability from Report 3 | `FE-06 — Inspection Report and Approval` |
| WF test ID | Business-flow traceability ID | `WF3-005` |

Do not rename the files or IDs to make the sheet number look like an SRS
feature code. The MF2-07 cases sit on `Feature 1` and the MF3/MF4 backend cases
on `Feature 2`; that grouping is a template label, not a feature code.

## Source of truth and template rule

- `template/Report5_Test Report.xlsx` is an unchanged copy of the supplied
  workbook. Do not edit this copy to add new sections or rename sheets.
- Exactly eight FE-specific Markdown files in `03-features/` are the editable
  feature sources. There are no aggregate `feature-1.md` or `feature-2.md`
  sources. Keep test case IDs stable when a case is reworded or re-tested.
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
| `03-features/fe-01-identity-access-governance.md` | Support evidence | FE-01 gates; not a workbook case. |
| `03-features/fe-02-asset-registry-inspection-schedule.md` | Coverage gap | No current case; see the file. |
| `03-features/fe-03-inspection-request-work-assignment.md` | `Feature 1` sheet | `WF2-008`, `WF2-009` (MF2-07 readiness). |
| `03-features/fe-04-inspection-execution-evidence-management.md` | `Feature 2` sheet | `WF3-002`, `WF3-009`. |
| `03-features/fe-05-yolo-defect-detection-verification.md` | `Feature 2` sheet | `WF3-003`. |
| `03-features/fe-06-inspection-report-approval.md` | `Feature 2` sheet | `WF3-005`, `WF3-006`. |
| `03-features/fe-07-maintenance-defect-resolution.md` | `Feature 2` sheet | `WF3-010`–`WF3-012`; partial MF4 backend API evidence and explicit remaining gaps. |
| `03-features/fe-08-dashboard-analytics-notifications.md` | Coverage gap | No assigned case; do not infer execution. |
| `template-layout.md` | All sheets | Exact sheet, column, and section reference. |
| `template/Report5_Test Report.xlsx` | All sheets | Original-format workbook copy. |

## Current test scope

Ten current cases: two MF2-07 readiness cases, five selected MF3 cases and three selected MF4 backend cases.

1. FE-01 — identity/access supporting gates. Recorded separately in the FE-01
   file; not a workbook case.
2. FE-02 — asset registry and schedule. No case (see coverage gap).
3. FE-03 — MF2-07 readiness approval and return (`WF2-008`, `WF2-009`).
4. FE-04 — inspection evidence and the Inspector's quality decision
   (`WF3-002`), and the scoped inspection/report collections (`WF3-009`).
5. FE-05 — advisory detection and human finding verification (`WF3-003`).
6. FE-06 — report review, publication, and immutability (`WF3-005`, `WF3-006`).
7. FE-07 — maintenance and defect resolution backend API cases (`WF3-010`–`WF3-012`); remaining MF4 scope is documented as a gap.
8. FE-08 — dashboard, analytics, and notifications. No assigned case; explicit
   coverage gap.

Totals: **10 cases, 10 `Passed`, 0 `Failed`, 0 `Pending`.** Coverage of 100%
is coverage of these selected executed cases only, not full product/SRS coverage.
Removed case IDs stay reserved and are never reused; the added FE-07 cases use
`WF3-010`–`WF3-012` after `WF3-009`.

MinIO/evidence storage is tracked under FE-04. CI uses S3Mock for S3 API
integration coverage; that mock does not replace runtime verification against
MinIO. A role check never replaces organization ownership, assignment, or
separation-of-duties checks.

## Editing workflow

1. Add or update the case in its owning FE-specific file first. FE-01 support
   evidence stays in FE-01; do not create aggregate sources by workbook sheet.
2. Keep the existing ID format (`WF3-002`, `WF3-009`) stable. Add the mapped FE
   code in the function name or mapping note; do not interpret the workbook
   sheet number as the FE code.
3. Mirror every case in `01-test-cases/test-case-list.md`.
4. Record execution only in the matching Round 1, Round 2, or Round 3 cell.
   Use only `Passed`, `Failed`, `Pending`, or `N/A`.
5. Update the corresponding module row and totals in
   `02-test-statistics/test-statistics.md`. The workbook feature sheets are
   output groupings only; each may contain cases from multiple FE sources.
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
actually executed. Do not record a case for a workflow that has no
implementation, and do not put passwords, tokens, private keys, or customer
secrets in test evidence or notes.
