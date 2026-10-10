# Report 5 — Test Report working folder

This folder separates the contents of the supplied `Report5_Test Report.xlsx`
template so the team can update test cases without repeatedly rebuilding the
whole workbook.

**Scope (reset 2026-10-09):** This report covers the **implemented MF3 slice
only** — inspection evidence, defect findings, and reporting — for the four
current roles (`ADMIN`, `ORG_ADMIN`, `INSPECTOR`, `MAINTENANCE_ENGINEER`). The
previous content mixed a retired five-role WF1–WF4 baseline with unimplemented
MF1–MF2/MF4 target cases; those 28 cases were removed because they described
behavior that no longer exists or has never been built. Every remaining case has
an executed automated test behind it.

MF1, MF2, MF4, FE-02, FE-03, FE-07, and FE-08 are **untested**, and that is
recorded as a coverage gap rather than filled with a pending or invented case.
The original workbook and preview output remain unchanged.

## Naming layers and mapping

`Feature 1` and `Feature 2` are fixed workbook sheet names from the supplied
template. They are not the SRS feature codes `FE-01` and `FE-02`.

| Layer | Meaning | Example |
| --- | --- | --- |
| Workbook sheet | Fixed Report 5 grouping | `Feature 2` |
| SRS feature | Product capability from Report 3 | `FE-06 — Inspection Report and Approval` |
| WF test ID | Business-flow traceability ID | `WF3-005` |

Do not rename the files or IDs to make the sheet number look like an SRS
feature code. After the reset, all cases sit on `Feature 2`, and `Feature 1` is
empty because MF1/MF2 are unimplemented.

## Source of truth and template rule

- `template/Report5_Test Report.xlsx` is an unchanged copy of the supplied
  workbook. Do not edit this copy to add new sections or rename sheets.
- Exactly eight FE-specific Markdown files in `03-features/` are the editable
  feature sources. There are no aggregate `feature-1.md` or `feature-2.md`
  sources. Keep test case IDs stable when a case is reworded or re-tested.
- When the report is ready for submission, copy the Markdown values into the
  workbook while preserving the template's sheet names, order, column order,
  status vocabulary, and table layout. Read
  [template-layout.md](template-layout.md) first: it carries the exact cell
  addresses, the per-sheet summary block that the Markdown has no equivalent
  for, and the template defects that will otherwise corrupt an export.
- The source template is intentionally not “corrected” here. Its existing
  formula/name issues, including `#REF!` values in the project metadata area
  and a stray count in `Feature 2!A18`, are recorded in
  [template-layout.md](template-layout.md) and should be handled only with the
  report owner’s approval.
- The workbook's `Sheet Name` column placeholder reads `Feature1`/`Feature2`
  without a space, but the real tabs are `Feature 1`/`Feature 2`. The Markdown
  uses the tab names; do not copy the placeholder spelling into the cell.

## Folder map

| Folder/file | Workbook area | Purpose |
| --- | --- | --- |
| `00-cover/` | `Cover` | Project metadata and record of changes. |
| `01-test-cases/` | `Test Cases` | The index of all cases and their preconditions. |
| `02-test-statistics/` | `Test Statistics` | Module totals, coverage, and execution summary. |
| `03-features/fe-01-identity-access-governance.md` | Support evidence | FE-01 gates; not a workbook case. |
| `03-features/fe-02-asset-registry-inspection-schedule.md` | Coverage gap | No current case; MF1 catalog workflow unimplemented. |
| `03-features/fe-03-inspection-request-work-assignment.md` | Coverage gap | No current case; MF2 mission preparation unimplemented. |
| `03-features/fe-04-inspection-execution-evidence-management.md` | `Feature 2` sheet | `WF3-002`, `WF3-009`. |
| `03-features/fe-05-yolo-defect-detection-verification.md` | `Feature 2` sheet | `WF3-003`. |
| `03-features/fe-06-inspection-report-approval.md` | `Feature 2` sheet | `WF3-005`, `WF3-006`. |
| `03-features/fe-07-maintenance-defect-resolution.md` | Coverage gap | No current case; MF4 unimplemented. |
| `03-features/fe-08-dashboard-analytics-notifications.md` | Coverage gap | No assigned case; do not infer execution. |

The FE-xx codes and their Report 3 sections are:

| FE | Report 3 § | Report 3 feature title |
| --- | --- | --- |
| FE-01 | 3.2 | Identity, Enterprise Subscription and Workforce Governance |
| FE-02 | 3.3 | Asset, Drone, Workforce and Compliance Catalog — MF1 |
| FE-03 | 3.4 | Mission Preparation, Assignment Response and Readiness — MF2 |
| FE-04 | 3.5 | Field Records, Evidence and Inspector Quality Decision |
| FE-05 | 3.6 | AI Vision Candidates and Human Finding Decisions |
| FE-06 | 3.7 | Inspection Report Drafting, Review and Publication — MF3 |
| FE-07 | 3.8 | Team Maintenance, Cost Control and Completion Reporting — MF4 |
| FE-08 | 3.9 | Dashboard, Analytics and Notifications |

Each FE file's H1 now carries the Report 3 title. The filenames keep their
original wording and are left alone: renaming them would break every link and
reviewer's bookmark for no reporting benefit.
| `template-layout.md` | All sheets | Exact sheet, column, and section reference. |
| `template/Report5_Test Report.xlsx` | All sheets | Original-format workbook copy. |

## Current test scope

All five current cases belong to MF3:

1. FE-01 — identity/access supporting gates. Recorded separately in the FE-01
   file; not a workbook case.
2. FE-02 — asset registry and schedule. No case (see coverage gap).
3. FE-03 — inspection request and assignment. No case; MF1/MF2 unimplemented.
4. FE-04 — inspection evidence and the Inspector's quality decision
   (`WF3-002`), and the scoped inspection/report collections (`WF3-009`).
5. FE-05 — advisory detection and human finding verification (`WF3-003`).
6. FE-06 — report review, publication, and immutability (`WF3-005`, `WF3-006`).
7. FE-07 — maintenance and defect resolution. No case; MF4 unimplemented.
8. FE-08 — dashboard, analytics, and notifications. No assigned case; explicit
   coverage gap.

Totals: **5 cases, 5 `Passed`, 0 `Failed`, 0 `Pending`.** Coverage of 100% is
coverage of the implemented slice only, not of the SRS. Removed case IDs stay
reserved and are never reused; new cases continue from `WF3-010` after
`WF3-009`.

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
   `02-test-statistics/test-statistics.md`. `Module code` must match the
   feature sheet's `Feature` name (`B2`), not the sheet name — in the workbook
   that column is a formula reading `B2`, so the two must not drift apart.
6. Before exporting, check that the number of cases, IDs, statuses, dates, and
   testers agree across all Markdown files and the workbook.

### Feature-sheet summary block

Each feature sheet carries a summary block at `A2:E8` (`Feature`,
`Test requirement`, `Number of TCs`, and per-round `Passed`/`Failed`/
`Pending`/`N/A` counts), and `Test Statistics` reads its values back out by
formula. `Number of TCs` and the round counts are formulas and need no Markdown
source; the `Feature` name and `Test requirement` line are typed values, and
the `Feature sheet summary` table in `fe-04-…md` is their recorded source.
Populate `Feature 1` too — `Test Statistics!C11` reads it even though that
sheet has no cases.

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
