# Report 5 — Test Report working folder

This folder separates the contents of the supplied `Report5_Test Report.xlsx`
template so the team can update test cases without repeatedly rebuilding the
whole workbook.

**Scope (updated 2026-10-10):** This report records seven executed cases for the
four current roles (`ADMIN`, `ORG_ADMIN`, `INSPECTOR`, `MAINTENANCE_ENGINEER`):
two MF2-07 readiness decision cases and five MF3 cases. The earlier content
mixed a retired five-role WF1–WF4 baseline with unimplemented MF1–MF4 target
cases; obsolete and unsupported cases were removed during the 2026-10-09 reset.
The two MF2 cases were restored after the merged backend/frontend/mobile PRs
were integrated locally: backend `84fcc16`, frontend `287d5a4`, mobile `91092e6`.

This does not claim complete MF2 coverage. MF2-08 source-change invalidation is
partial (session start checks the newest decision and requires APPROVED, but no
source-change flow appends INVALIDATED); MF2-12 session end and
`FIELD_COMPLETED` handoff remain unimplemented. MF1, MF4 and FE-08 remain gaps.
The original workbook template remains unchanged; generated copies contain eight
feature sheets as requested.

## Naming layers and mapping

The supplied template has two feature sheets (`Feature 1`, `Feature 2`). Generated
workbooks extend it to eight feature sheets (`Feature 1`–`Feature 8`), one per
Report 3 feature. The original template remains unchanged. Sheet `Feature N`
contains SRS feature `FE-0N`; these are separate naming layers, not synonyms.
Feature 1 (supporting FE-01), Feature 2 (FE-02), Feature 7 (FE-07) and
Feature 8 (FE-08) have no cases. Feature 3 (FE-03) contains `WF2-008` and
`WF2-009`; Features 4–6 contain the five MF3 cases. All eight sheets remain so
the workbook mirrors the eight SRS features.

| Layer | Meaning | Example |
| --- | --- | --- |
| Workbook sheet | Generated Report 5 grouping; one sheet per FE | `Feature 6` |
| SRS feature | Product capability from Report 3 | `FE-06 — Inspection Report and Approval` |
| WF test ID | Business-flow traceability ID | `WF3-005` |

Do not rename the files or IDs to make the sheet number look like an SRS
feature code. In the generated workbook, `WF2-008`/`WF2-009` sit on `Feature 3` (FE-03),
and MF3 cases sit on `Feature 4`, `Feature 5`, and `Feature 6` (FE-04–FE-06).
The remaining four sheets have zero cases, preserving the one-sheet-per-SRS-
feature mapping.

## Source of truth and template rule

- `template/Report5_Test Report.xlsx` is an unchanged copy of the supplied
  workbook. Do not edit this copy to add new sections or rename sheets.
- Exactly eight FE-specific Markdown files in `03-features/` are the editable
  feature sources. There are no aggregate `feature-1.md` or `feature-2.md`
  sources. Keep test case IDs stable when a case is reworded or re-tested.
- When the report is ready for submission, use the exporter to produce a copy
  of the official template with eight generated feature sheets. The supplied
  template remains unchanged; generated copies preserve its cell layout,
  status vocabulary, and formatting. Read
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
| `03-features/fe-03-inspection-request-work-assignment.md` | `Feature 3` sheet | `WF2-008`, `WF2-009` (MF2-07 readiness approval/return); other MF2 steps remain gaps or partial. |
| `03-features/fe-04-inspection-execution-evidence-management.md` | `Feature 4` sheet | `WF3-002`, `WF3-009`. |
| `03-features/fe-05-yolo-defect-detection-verification.md` | `Feature 5` sheet | `WF3-003`. |
| `03-features/fe-06-inspection-report-approval.md` | `Feature 6` sheet | `WF3-005`, `WF3-006`. |
| `03-features/fe-07-maintenance-defect-resolution.md` | Coverage gap | No current case; MF4 unimplemented. |
| `03-features/fe-08-dashboard-analytics-notifications.md` | Coverage gap | No assigned case; do not infer execution. |
| `template-layout.md` | All sheets | Exact sheet, column, and section reference. |
| `template/Report5_Test Report.xlsx` | All sheets | Original-format workbook copy. |

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

## Current test scope

All verification statuses below describe the current source after the MF2 PR integration; the dated change history records superseded earlier states.

1. FE-01 — identity/access supporting gates. Recorded separately in the FE-01
   file; not a workbook case.
2. FE-02 — asset registry and schedule. No case (see coverage gap).
3. FE-03 — MF2-07 readiness approval/return (`WF2-008`, `WF2-009`); other MF2
   implementation and case-coverage gaps remain documented.
4. FE-04 — inspection evidence and the Inspector's quality decision
   (`WF3-002`), and the scoped inspection/report collections (`WF3-009`).
5. FE-05 — advisory detection and human finding verification (`WF3-003`).
6. FE-06 — report review, publication, and immutability (`WF3-005`, `WF3-006`).
7. FE-07 — maintenance and defect resolution. No case; MF4 unimplemented.
8. FE-08 — dashboard, analytics, and notifications. No assigned case; explicit
   coverage gap.

Totals: **7 cases, 7 `Passed`, 0 `Failed`, 0 `Pending`.** Coverage of 100% is
only of these seven recorded cases, not the SRS or the complete MF2 workflow.
Removed case IDs stay reserved and are never reused; new cases continue from
`WF3-010` after `WF3-009`.

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
the `Feature sheet summary` table in each `fe-0N-…md` file is the recorded
source for its matching sheet. Populate all eight summary blocks, including the
five sheets with no current cases, because the statistics formulas read every
sheet's `B2` value.

## Generate and verify a workbook copy

Report 5 has its own exporter; it does not depend on Report 1–3 export logic.
Run from the docs repository root:

```powershell
python -I tools/export_report5.py
python -I -m unittest discover -s tools/tests -p test_report5.py -v
```

Use `python -I tools/export_all.py` for all source-backed reports and weekly
reports. Outputs and their verification manifests go into a fresh
`reports/generated/<run>/` folder. Original templates are never overwritten.
See [export tools](../../tools/README.md) for the independent commands and
Office verification procedure.

The generated copy preserves sheet order, columns and source round evidence.
It keeps FE function bars and repairs only the output's count/round formulas:
case totals count WFx IDs, not function-bar text, and Round 2/3 count their own
status columns. The stale calculation chain is removed from output copies so
Excel can rebuild it. No product case status changes during export.

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
