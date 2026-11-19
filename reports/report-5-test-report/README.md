# Report 5 — Test Report working folder

This folder separates the contents of the supplied `Report5_Test Report.xlsx`
template so the team can update test cases without repeatedly rebuilding the
whole workbook.

**Scope and status (updated 2026-11-19):** The current Report 5 inventory holds **64 active test cases** mapped 1-to-1 to eight product features (`FE-01`–`FE-08`, `Feature 1`–`Feature 8`, two per main flow `MF1`–`MF4`), aligned with Flyway `V1`–`V4` and `V60`–`V62` (`["1","2","3","4","60","61","62"]`; 45 application tables, 44 JPA runtime entities, 47 total tables). Current-scope Round 1 totals are 45 `Passed`, 0 `Failed`, 9 `Pending`, and 10 `N/A`. Round 3 has 13 executed `Passed` cases, including `WF3-029` (DroneKnowledgeAI historical case recommendation & tenant isolation), `WF3-030` (advisory knowledge references in the AI summary) and `WF3-031` (Customer Mobile parity from `PR #27`), verified on 2026-11-19 with backend `.\mvnw.cmd verify` (958 tests passed, 0 failures, Modulith and JaCoCo gates met), frontend `npm test` (97 test files, 93 passed / 4 skipped; 716 tests, 712 passed / 4 skipped) and Mobile `flutter test` (56 passed, 0 failures). `WF3-020` and `WF3-022`–`WF3-025` remain `Pending` in Round 3 pending live Nginx/Docker Compose E2E verification; `WF2-001` Round 2 remains `Pending` pending connected cross-role verification.

The original workbook template remains unchanged; generated copies contain eight active feature sheets (`Feature 1`–`Feature 8`). Maintenance feature sheets and cases are retired historical material, not current coverage.

## Naming layers and mapping

The supplied template has two feature sheets (`Feature 1`, `Feature 2`). Generated
workbooks extend it to eight active feature sheets (`Feature 1`–`Feature 8`), one per
current Report 3 feature (`FE-01`–`FE-08`). Sheet `Feature N` contains SRS feature `FE-0N`.

| Layer | Meaning | Example |
| --- | --- | --- |
| Workbook sheet | Generated Report 5 grouping; one sheet per FE | `Feature 8` |
| SRS feature | Product capability from Report 3 | `FE-08 — Customer Acceptance & Payment Settlement` |
| WF test ID | Business-flow traceability ID | `WF3-031` |

## Source of truth and template rule

- `template/Report5_Test Report.xlsx` is an unchanged copy of the supplied
  workbook. Do not edit this copy to add new sections or rename sheets.
- Exactly eight active FE-specific Markdown files in `03-features/` are the editable
  feature sources (`fe-01` through `fe-08`). Keep test case IDs stable when a
  case is reworded or re-tested.
- When the report is ready for submission, use the exporter to produce a copy
  of the official template with eight generated feature sheets. Read
  [template-layout.md](template-layout.md) first: it carries the exact cell
  addresses, the per-sheet summary block, and the template defects that will
  otherwise corrupt an export.

## Folder map

| Folder/file | Workbook area | Purpose |
| --- | --- | --- |
| `00-cover/` | `Cover` | Project metadata and record of changes. |
| `01-test-cases/` | `Test Cases` | Complete index of all 64 active test cases across `Feature 1`–`Feature 8`. |
| `02-test-statistics/` | `Test Statistics` | Module totals, coverage, and execution summary across active `Feature 1`–`Feature 8`. |
| `03-features/fe-01-authentication-account-access-four-role-portal-scope.md` | `Feature 1` sheet | `FE-01` (`WF1-001`–`005`, `WF1-022`, `WF2-019`, `WF2-020`: 8 cases, Owner: Trần Hoàng Trung Hiếu). |
| `03-features/fe-02-partner-inspector-application-owned-drone-registry.md` | `Feature 2` sheet | `FE-02` (`WF1-006`–`008`, `WF1-010`, `WF1-014`–`016`: 7 cases, Owner: Trần Hoàng Trung Hiếu). |
| `03-features/fe-03-buildings-airspace-screening-occurrences-notifications.md` | `Feature 3` sheet | `FE-03` (`WF1-009`, `011`–`013`, `017`–`020`: 8 cases, Owner: Phùng Trung Quốc). |
| `03-features/fe-04-service-requests-vnd-quotations-agreements-dispatch.md` | `Feature 4` sheet | `FE-04` (`WF1-021`, `WF2-001`–`005`, `WF2-015`, `WF2-016`: 8 cases, Owner: Phùng Trung Quốc). |
| `03-features/fe-05-flight-permit-gate-on-site-field-sessions.md` | `Feature 5` sheet | `FE-05` (`WF2-008`, `009`, `011`, `012`, `017`, `018`, `020`: 7 cases, Owner: Trần Tùng Bách). |
| `03-features/fe-06-evidence-intake-human-reviewed-defect-detection.md` | `Feature 6` sheet | `FE-06` (`WF3-001`–`004`, `007`, `008`, `010`, `017`, `022`–`025`, `028`, `029`: 14 cases, Owner: Trần Tùng Bách). |
| `03-features/fe-07-inspection-report-preparation-review-publication.md` | `Feature 7` sheet | `FE-07` (`WF3-005`, `006`, `009`, `016`, `030`: 5 cases, Owner: Trần Tùng Bách). |
| `03-features/fe-08-customer-acceptance-payment-settlement.md` | `Feature 8` sheet | `FE-08` (`WF3-012`, `018`, `019`, `021`, `026`, `027`, `031`: 7 cases, Owner: Trương Thái Như). |
| `template-layout.md` | All sheets | Exact sheet, column, and section reference. |
| `template/Report5_Test Report.xlsx` | All sheets | Original-format workbook copy. |

The `FE-01`–`FE-08` codes and their Report 3 sections are:

| FE | Report 3 § | Report 3 feature title | Owner |
| --- | --- | --- | --- |
| `FE-01` | `3.2` | Authentication, Account Access & Four-Role Portal Scope | Trần Hoàng Trung Hiếu (`SE184212`) |
| `FE-02` | `3.3` | Partner Inspector Application & Owned Drone Registry | Trần Hoàng Trung Hiếu (`SE184212`) |
| `FE-03` | `3.4` | Buildings, Airspace Screening, Occurrences & Notifications | Phùng Trung Quốc (`SE170027`) |
| `FE-04` | `3.5` | Service Requests, VND Quotations, Agreements & Dispatch | Phùng Trung Quốc (`SE170027`) |
| `FE-05` | `3.6` | Flight Permit Gate & On-Site Field Sessions | Trần Tùng Bách (`SE180220`) |
| `FE-06` | `3.7` | Evidence Intake & Human-Reviewed Defect Detection | Trần Tùng Bách (`SE180220`) |
| `FE-07` | `3.8` | Inspection Report Preparation, Review & Publication | Trần Tùng Bách (`SE180220`) |
| `FE-08` | `3.9` | Customer Acceptance & Payment Settlement | Trương Thái Như (`SE180082`) |

Each active FE file's H1 carries its current Report 3 title. Retired maintenance case sources are removed from the active suite.

## Editing workflow

1. Add or update the case in its owning active FE-specific file first (`fe-01`–`fe-08`).
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
