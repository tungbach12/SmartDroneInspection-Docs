# Report 5 — Test Report working folder

This folder separates the contents of the supplied `Report5_Test Report.xlsx`
template so the team can update test cases without repeatedly rebuilding the
whole workbook.

Version 3.20 lists 80 cases across 24 features, with 78 active and two superseded FE-13 cases. Round 1 records 52 Passed, 0 Failed, 9 Pending and 19 N/A. Round 3 records 16 executed passes. The FE-24 case notes track follow-up verification for duplicate re-inspection and verdict expiry. See the [26 November regression evidence](regression-evidence-2026-11-26.md) and [Test Documentation, Section 5](../report-5-test-documentation/01-testing-documentation.md#5-test-reports) for suite results.

The original workbook template remains unchanged; generated copies contain twenty-four active feature sheets (`Feature 1`–`Feature 24`). Maintenance feature sheets and cases are retired historical material, not current coverage.

## Naming layers and mapping

The supplied template has two feature sheets (`Feature 1`, `Feature 2`). Generated
workbooks extend it to twenty-four active feature sheets (`Feature 1`–`Feature 24`), one per
current Report 3 feature (`FE-01`–`FE-24`). Sheet `Feature N` contains SRS feature `FE-0N`.

| Layer | Meaning | Example |
| --- | --- | --- |
| Workbook sheet | Generated Report 5 grouping; one sheet per FE | `Feature 24` |
| SRS feature | Product capability from Report 3 | `FE-24 — Post-Remediation Re-inspection & Defect Verification` |
| WF test ID | Business-flow traceability ID | `WF3-031` |

## Source of truth and template rule

- `template/Report5_Test Report.xlsx` is an unchanged copy of the supplied
  workbook. Do not edit this copy to add new sections or rename sheets.
- Exactly twenty-four active FE-specific Markdown files in `03-features/` are the editable
  feature sources (`fe-01` through `fe-24`). Keep test case IDs stable when a
  case is reworded or re-tested.
- When the report is ready for submission, use the exporter to produce a copy
  of the official template with twenty-four generated feature sheets. Read
  [template-layout.md](template-layout.md) first: it carries the exact cell
  addresses, the per-sheet summary block, and the template defects that will
  otherwise corrupt an export.

## Folder map

| Folder/file | Workbook area | Purpose |
| --- | --- | --- |
| `00-cover/` | `Cover` | Project metadata and record of changes. |
| `01-test-cases/` | `Test Cases` | Complete index of all 80 listed test cases (78 active) across `Feature 1`–`Feature 24`. |
| `02-test-statistics/` | `Test Statistics` | Module totals, coverage, and execution summary across active `Feature 1`–`Feature 24`. |
| `03-features/fe-01-*.md` – `fe-05-*.md` | `Feature 1`–`5` sheets | Owner: Trần Hoàng Trung Hiếu (`WF1-001`..`WF3-032`, 18 cases). |
| `03-features/fe-06-*.md` – `fe-12-*.md` | `Feature 6`–`12` sheets | Owner: Phùng Trung Quốc (24 cases). |
| `03-features/fe-13-*.md` – `fe-18-*.md` | `Feature 13`–`18` sheets | Owner: Trần Tùng Bách (29 cases). |
| `03-features/fe-19-*.md` – `fe-24-*.md` | `Feature 19`–`24` sheets | Owner: Trương Thái Như (`WF3-012`..`WF3-033`, 9 cases). |
| `template-layout.md` | All sheets | Exact sheet, column, and section reference. |
| `template/Report5_Test Report.xlsx` | All sheets | Original-format workbook copy. |

The `FE-01`–`FE-24` codes and their Report 3 sections are:

| FE | Report 3 § | Report 3 feature title | Owner | Cases |
| --- | --- | --- | --- | ---: |
| `FE-01` | `3.2` | Account Authentication, OTP & 4-Role Access Control | Trần Hoàng Trung Hiếu (`SE184212`) | 7 |
| `FE-02` | `3.3` | Partner Inspector Application & Qualification Management | Trần Hoàng Trung Hiếu (`SE184212`) | 4 |
| `FE-03` | `3.4` | Inspector-Owned Drone Registration & Fleet Management | Trần Hoàng Trung Hiếu (`SE184212`) | 3 |
| `FE-04` | `3.5` | Interactive Location Map & No-Fly Zone Airspace Screening | Trần Hoàng Trung Hiếu (`SE184212`) | 3 |
| `FE-05` | `3.6` | Financial History & Revenue/Payment Ledger | Trần Hoàng Trung Hiếu (`SE184212`) | 1 |
| `FE-06` | `3.7` | Building Asset Registry, Checkpoints & Reference Documents | Phùng Trung Quốc (`SE170027`) | 3 |
| `FE-07` | `3.8` | Restricted Airspace Advisory Warning & Immediate Onboarding | Phùng Trung Quốc (`SE170027`) | 1 |
| `FE-08` | `3.9` | Service Requests (One-Time & Recurring) & VND Quotations | Pham Trung Quoc (`SE170027`) | 6 |
| `FE-09` | `3.10` | Offline Signed Contract & Occurrence Dispatch Scheduling | Pham Trung Quoc (`SE170027`) | 6 |
| `FE-10` | `3.11` | Dual-Channel Messaging (Order Chat & Inspection Chat) | Phùng Trung Quốc (`SE170027`) | 2 |
| `FE-11` | `3.12` | Assignment Acceptance Timeout & Escalation Handling | Phùng Trung Quốc (`SE170027`) | 1 |
| `FE-12` | `3.13` | System Notifications & Alert Center | Pham Trung Quoc (`SE170027`) | 3 |
| `FE-13` | `3.14` | Flight Permit Upload & Independent Verification Gate | Trần Tùng Bách (`SE180220`) | 2 |
| `FE-14` | `3.15` | On-Site Field Session & SmartDroneHub MAVLink Telemetry | Trần Tùng Bách (`SE180220`) | 5 |
| `FE-15` | `3.16` | Field Evidence Intake & Chunked Video Processing Pipeline | Trần Tùng Bách (`SE180220`) | 5 |
| `FE-16` | `3.17` | AI Defect Detection (`YOLO11` + Vision Fallback) & Findings Confirmation | Trần Tùng Bách (`SE180220`) | 7 |
| `FE-17` | `3.18` | AI Case/Standard Retrieval (`pgvector` RAG), Note Drafting & Report Summary | Trần Tùng Bách (`SE180220`) | 2 |
| `FE-18` | `3.19` | Inspection Report Compilation, Independent Review & Official Publication | Trần Tùng Bách (`SE180220`) | 4 |
| `FE-19` | `3.20` | Customer Report Acceptance & Clarification Workflow | Trương Thái Như (`SE180082`) | 1 |
| `FE-20` | `3.21` | Online Service Fee Payment (`Sepay` VietQR & `VNPay`) | Trương Thái Như (`SE180082`) | 2 |
| `FE-21` | `3.22` | Payment Deadlines, Invoices & Payment Document Management | Trương Thái Như (`SE180082`) | 2 |
| `FE-22` | `3.23` | Partner Inspector Payout Reconciliation | Trương Thái Như (`SE180082`) | 1 |
| `FE-23` | `3.24` | Evidence-Backed Refunds & Receivable Recovery | Trương Thái Như (`SE180082`) | 1 |
| `FE-24` | `3.25` | Post-Remediation Re-inspection & Defect Verification | Trương Thái Như (`SE180082`) | 2 |

Each active FE file's H1 carries its current Report 3 title. Retired maintenance case sources are removed from the active suite.

## Editing workflow

1. Add or update the case in its owning active FE-specific file first (`fe-01`–`fe-24`).
2. Keep the existing active ID formats (`WF1-...` to `WF3-...`) stable; do not add `WF4` cases.
3. Mirror every case in `01-test-cases/test-case-list.md`.
4. Record execution only in the matching Round 1, Round 2, or Round 3 cell.
   Use only `Passed`, `Failed`, `Pending`, or `N/A`.
5. Update the corresponding module row and totals in
   `02-test-statistics/test-statistics.md`. `Module code` must match the
   feature sheet's `Feature` name (`B2`).
6. Keep the current Round 1 subtotal, historical Round 1 subtotal, Round 3
   executed subtotal, and V29 subset distinct in `test-statistics.md`; separately identify later schema cases such as V33–V35 that remain Pending.
7. Before exporting, check that the number of cases, IDs, statuses, dates, and
   testers agree across all Markdown files and the workbook.

## Generate and verify a workbook copy

Run from the docs repository root:

```powershell
python -I tools/export_report5.py
python -I -m unittest discover -s tools/tests -p "test_*.py" -v
```
