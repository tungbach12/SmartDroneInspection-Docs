# Test Statistics sheet source

This table mirrors the `Test Statistics` sheet. Keep the workbook's summary
formulas and labels; update the values from the feature files after each test
round.

## Project metadata

| Field | Value |
| --- | --- |
| Project Name | SmartDroneInspection |
| Project Code | GFA26SE139 |
| Test round | Current case inventory: 73 active IDs across twenty-four atomic features `FE-01` to `FE-24` (preserving all 64 historical records verbatim plus 3 unexecuted standalone coverage cases `WF3-032` in `FE-05`, `WF2-021` in `FE-11`, and `WF3-033` in `FE-22` as `N/A / Pending / Pending` and 6 executed MF2 cases `WF2-022`–`WF2-027`). Flyway set `["1","2","3","4","60","61","62","63","64","65","66","67","68","69","70","71"]`; 50 application tables (49 `RUNTIME_ENTITY_TABLES`, 52 total tables). Current Round 1 records 51 Passed, 0 Failed, 9 Pending, and 13 N/A (`51/60 = 85.00%`). The active-scope historical Round 1 subtotal remains 56 cases (45 Passed, 0 Failed, 8 Pending, 3 N/A; 90.00% passed). Round 3 has 13 Passed executions: `WF3-005`, `WF3-006`, `WF3-009`, `WF3-016`, `WF3-018`, `WF3-019`, `WF3-021`, `WF3-026`, `WF3-027`, `WF3-028`, `WF3-029`, `WF3-030`, and `WF3-031`; `WF3-020` and `WF3-022`–`WF3-025` remain Pending in Round 3. Focused acceptance-timeout, ledger, and payout checks (`WF2-021`, `WF3-032`, `WF3-033`) remain unexecuted as standalone workbook rows (`N/A / Pending / Pending`). |
| Last updated | 2026-11-23 (Report 5 v3.14: added two executed Round 1 MF2 cases `WF2-026` in `FE-08` and `WF2-027` in `FE-10` covering Flyway `V70` Manager–Inspector Partner Chat, Flyway `V71` per-request Manager checkpoints configuration & dispatch propagation, explicit quote `datetime-local` inputs, and compact role-scoped Overview modals; updated inventory `71 -> 73` active cases, Round 1 `51 Passed / 0 Failed / 9 Pending / 13 N/A` (`51/60 = 85.00%`). Verified 2026-11-23: non-Docker/non-FFmpeg backend suite `762/762` passed (Docker Desktop daemon offline during full `mvnw verify` prevented Testcontainers integration classes from running, and host lacks `ffmpeg`), `ModulithArchitectureTest` `3/3` passed, `RuntimePersistenceInventoryTest`/`FullDatabaseSchemaMigrationTest` updated to `V70`–`V71` (`50`/`49`/`52`) and compiled (`spotless:apply test-compile` clean); full Frontend Vitest (`npx vitest run --maxWorkers=3`) `97` files passed / `4` skipped (`735` passed / `4` skipped), `oxlint` (`0` errors), and `tsc -b && vite build` passed, plus live browser verification on `http://localhost:3000/manager/contracts` with PostgreSQL `V71`.) |

### Round scope

Historical counts preserve the original eight-feature snapshot, including retired maintenance cases, legacy recurrence scenarios `WF1-018`/`WF1-019`/`WF1-021`, and implementation-specific `WF3-017`. Current Round 1 counts apply to the 73 active IDs in `FE-01`-`FE-24`; ten prior later additions (`WF3-018`–`WF3-020`, `WF3-022`–`WF3-025`, `WF3-029`–`WF3-031`) plus the three unexecuted standalone breakout cases (`WF3-032`, `WF2-021`, `WF3-033`) are N/A for Round 1 (`13 N/A`), and `WF3-021`, `WF3-026`–`WF3-028` are Pending in Round 1. Round 3 executed counts include only cases with Passed or Failed results (`WF3-005`, `WF3-006`, `WF3-009`, `WF3-016`, `WF3-018`, `WF3-019`, `WF3-021`, `WF3-026`–`WF3-031`); `WF3-020`, `WF3-022`–`WF3-025`, `WF3-032`, `WF2-021`, and `WF3-033` remain Pending.

## Module summary

| No | Module code | Passed | Failed | Pending | N/A | Number of test cases |
| ---: | --- | ---: | ---: | ---: | ---: | ---: |
| 1 | FE-01 Account Authentication, OTP & 4-Role Access Control | 6 | 0 | 1 | 0 | 7 |
| 2 | FE-02 Partner Inspector Application & Qualification Management | 3 | 0 | 1 | 0 | 4 |
| 3 | FE-03 Inspector-Owned Drone Registration & Fleet Management | 3 | 0 | 0 | 0 | 3 |
| 4 | FE-04 Interactive Location Map & No-Fly Zone Airspace Screening | 3 | 0 | 0 | 0 | 3 |
| 5 | FE-05 Financial History & Revenue/Payment Ledger | 0 | 0 | 0 | 1 | 1 |
| 6 | FE-06 Building Asset Registry, Checkpoints & Reference Documents | 3 | 0 | 0 | 0 | 3 |
| 7 | FE-07 Restricted Airspace Review & Clearance Decision | 1 | 0 | 0 | 0 | 1 |
| 8 | FE-08 Service Requests (One-Time & Recurring) & VND Quotations | 6 | 0 | 0 | 0 | 6 |
| 9 | FE-09 Offline Signed Contract & Occurrence Dispatch Scheduling | 5 | 0 | 1 | 0 | 6 |
| 10 | FE-10 Dual-Channel Messaging (Order Chat & Inspection Chat) | 2 | 0 | 0 | 0 | 2 |
| 11 | FE-11 Assignment Acceptance Timeout & Escalation Handling | 0 | 0 | 0 | 1 | 1 |
| 12 | FE-12 System Notifications & Alert Center | 2 | 0 | 0 | 0 | 2 |
| 13 | FE-13 Flight Permit Upload & Independent Verification Gate | 2 | 0 | 0 | 3 | 5 |
| 14 | FE-14 On-Site Field Session & SmartDroneHub MAVLink Telemetry | 4 | 0 | 0 | 1 | 5 |
| 15 | FE-15 Field Evidence Intake & Chunked Video Processing Pipeline | 1 | 0 | 0 | 4 | 5 |
| 16 | FE-16 AI Defect Detection (`YOLO11` + Vision Fallback) & Findings Confirmation | 6 | 0 | 1 | 0 | 7 |
| 17 | FE-17 AI Case/Standard Retrieval (`pgvector` RAG), Note Drafting & Report Summary | 0 | 0 | 0 | 2 | 2 |
| 18 | FE-18 Inspection Report Compilation, Independent Review & Official Publication | 4 | 0 | 0 | 0 | 4 |
| 19 | FE-19 Customer Report Acceptance & Clarification Workflow | 0 | 0 | 1 | 0 | 1 |
| 20 | FE-20 Online Service Fee Payment (`Sepay` VietQR & `VNPay`) | 0 | 0 | 0 | 2 | 2 |
| 21 | FE-21 Payment Deadlines, Invoices & Payment Document Management | 0 | 0 | 2 | 0 | 2 |
| 22 | FE-22 Partner Inspector Payout Reconciliation | 0 | 0 | 0 | 1 | 1 |
| 23 | FE-23 Evidence-Backed Refunds & Receivable Recovery | 0 | 0 | 1 | 0 | 1 |
| 24 | FE-24 Post-Remediation Re-inspection & Defect Verification | 0 | 0 | 1 | 1 | 2 |
| **Current Round 1 subtotal** |  | **51** | **0** | **9** | **16** | **76** |
| **Historical Round 1 subtotal** |  | **45** | **0** | **8** | **3** | **56** |
| **Historical Review 2 baseline (original eight-feature snapshot)** |  | **60** | **0** | **4** | **0** | **64** |
| **Historical implementation-specific pending** |  | **0** | **0** | **1** | **0** | **1** |
| **Round 3 executed cases** |  | **13** | **0** | **0** | **0** | **13** |
| **V29 Round 3 cases** |  | **2** | **0** | **0** | **0** | **2** |
| **Current inventory** |  |  |  |  |  | **76** |
