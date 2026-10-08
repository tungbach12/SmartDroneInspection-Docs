# Report 5 — Test Report working folder

This folder separates the contents of the supplied `Report5_Test Report.xlsx`
template so the team can update test cases without repeatedly rebuilding the
whole workbook.

**Implementation boundary (updated 2026-10-07):** The earlier WF1–WF4 cases are historical/retired v1 five-role baseline tests, not the current 2026-10-07 Enterprise SaaS target (four human roles — `ADMIN`, `ORG_ADMIN`, `INSPECTOR`, `MAINTENANCE_ENGINEER` — and four connected Main Flows MF1–MF4). Their recorded `Passed` results remain valid evidence only for the v1 behavior actually exercised; do not reuse them as proof of target behavior or the current reset branch. Backend V24/V25/V26 completed the identity, target-schema and runtime-cutover work on 8 October 2026, and that execution is recorded in the FE-01 Round 2 sections. MF1–MF4 workflow implementation remains out of reset scope. All nine target acceptance cases remain `Pending`, with no execution date/tester until actually run. The original workbook and preview output remain unchanged.

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
| `03-features/fe-01-identity-access-governance.md` | Support evidence | FE-01 gates; not part of the 15 WFx workbook cases. |
| `03-features/fe-02-asset-registry-inspection-schedule.md` | `Feature 1` sheet | v1 SF prerequisite cases WF1-001–WF1-004, WF1-011–WF1-016. |
| `03-features/fe-03-inspection-request-work-assignment.md` | `Feature 1` sheet | v1 WF1/WF2 cases and target MF1/MF2 cases WF2-005–WF2-007. |
| `03-features/fe-04-inspection-execution-evidence-management.md` | `Feature 2` sheet | v1 MF3/WF3-001–WF3-002. |
| `03-features/fe-05-yolo-defect-detection-verification.md` | `Feature 2` sheet | v1 MF3/WF3-003. |
| `03-features/fe-06-inspection-report-approval.md` | `Feature 2` sheet | v1 MF3/WF3-004 and target MF3/MF4 cases WF3-005–WF3-008. |
| `03-features/fe-07-maintenance-defect-resolution.md` | `Feature 2` sheet | v1 WF4/WF4-001–WF4-003 and target MF4 cases WF4-004–WF4-005. |
| `03-features/fe-08-dashboard-analytics-notifications.md` | Coverage gap | No WFx case in the current baseline; do not infer execution. |
| `template-layout.md` | All sheets | Exact sheet, column, and section reference. |
| `template/Report5_Test Report.xlsx` | All sheets | Original-format workbook copy. |

## Current and target test scope

Historical cases cover the v1 WF1–WF4 baseline and do not test autonomous drone
flight. Target-only cases extend traceability to the Enterprise SaaS target with
four human roles and four connected Main Flows (MF1–MF4). The fixed workbook
sheets combine groups, while FE codes identify SRS capabilities and WFx IDs
retain stable case identity:

1. FE-01 — identity/access foundation, including the W3 auth/migration smoke gate and shared API contract supporting checks. These supporting gates are documented separately and are not additional functional workbook cases. Target FE-01 organization/entitlement and separation-of-duties checks remain Pending support gates outside the workbook count.
2. FE-02 — asset and inspection scheduling (WF1; `WF1-001`–`WF1-004`).
3. FE-03 — client request, quotation/order, and service assignment (WF2; `WF2-001`–`WF2-004`).
4. FE-04 — inspection execution and evidence (WF3; `WF3-001`–`WF3-002`).
5. FE-05 — YOLO-assisted defect detection and verification (WF3; `WF3-003`).
6. FE-06 — inspection report and approval (WF3; `WF3-004`).
7. FE-07 — maintenance ticket, assessment/execution, rework, and billing status (WF4; `WF4-001`–`WF4-003`).
8. FE-08 — dashboard, analytics, and notifications. No test case is assigned
   in the baseline or added target cases; this remains an explicit coverage gap.

The nine cases WF2-005–WF4-005 are target acceptance criteria only and remain
`Pending` until the associated implementation and verification evidence exist.
They cover workspace/subscription entitlement, MF1 asset + Inspector/Drone pair setup,
MF2 mission preparation/readiness, MF3 human verification and immutable report
publication, and MF4 team/cost/acceptance boundaries. Their existence does not claim
runtime delivery.

The FE-01 W3 auth/migration smoke gate is tracked by Jira `SCRUM-58/T001` under
`SCRUM-108`; it is a delivery gate and is not counted in the functional Report 5
case index. The workbook now maps 24 v1 WF1–WF4 cases plus nine target-only
Pending cases, for 33 total: 13 Passed, 20 Pending, and zero Failed at the recorded
baseline. MinIO/evidence storage is tracked separately under FE-04/WF3 task
`T025/SCRUM-85`. CI uses S3Mock for S3 API integration coverage; that mock does not
replace runtime verification against MinIO.

Implemented v1 role codes are `ADMIN`, `CLIENT`, `SERVICE_MANAGER`, `INSPECTOR`, and
`MAINTENANCE_ENGINEER`. The current target role codes are `ADMIN`, `ORG_ADMIN`,
`INSPECTOR`, and `MAINTENANCE_ENGINEER`; those target roles are not yet runtime-verified.
A role check never replaces organization ownership,
assignment, or separation-of-duties checks.

## Editing workflow

1. Add or update the case in its owning FE-specific file first. FE-01 support
   evidence stays in FE-01; do not create aggregate sources by workbook sheet.
2. Keep the existing ID format (`WF1-001`, `WF2-001`, `WF3-001`, `WF4-001`)
   stable. Add the mapped FE code in the function name or mapping note; do not
   interpret the workbook sheet number as the FE code.
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
actually executed. Do not put passwords, tokens, private keys, or customer
secrets in test evidence or notes.
