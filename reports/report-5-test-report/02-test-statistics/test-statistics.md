# Test Statistics sheet source

This table mirrors the `Test Statistics` sheet. Keep the workbook's summary
formulas and labels; update the values from the feature files after each test
round.

## Project metadata

| Field | Value |
| --- | --- |
| Project Name | SmartDroneInspection |
| Project Code | GFA26SE139 |
| Test round | Current case inventory: 77 listed rows (75 active IDs across twenty-four atomic features `FE-01` to `FE-24` plus 2 historical superseded `FE-13` cases `WF2-008`/`WF2-009`, preserving all historical records plus 3 unexecuted standalone coverage cases `WF3-032` in `FE-05`, `WF2-021` in `FE-11`, and `WF3-033` in `FE-22` as `N/A / Pending / Pending`, 7 executed MF2 cases `WF2-022`–`WF2-028`, and 3 unexecuted/planned `FE-13` cases `WF2-029`–`WF2-031`). Flyway set `["1","2","3","4","60"–"80"]`; 53 application tables (52 `RUNTIME_ENTITY_TABLES`, 55 total tables). Current Round 1 records 52 Passed, 0 Failed, 9 Pending, and 16 N/A (`52/61 = 85.25%`). The active-scope historical Round 1 subtotal remains 56 cases (45 Passed, 0 Failed, 8 Pending, 3 N/A; 90.00% passed). Round 3 has 13 Passed executions: `WF3-005`, `WF3-006`, `WF3-009`, `WF3-016`, `WF3-018`, `WF3-019`, `WF3-021`, `WF3-026`, `WF3-027`, `WF3-028`, `WF3-029`, `WF3-030`, and `WF3-031`; `WF3-020` and `WF3-022`–`WF3-025` remain Pending in Round 3. Focused acceptance-timeout, ledger, and payout checks (`WF2-021`, `WF3-032`, `WF3-033`) remain unexecuted as standalone workbook rows (`N/A / Pending / Pending`). |
| Last updated | 2026-11-25 (Report 5 v3.15: added executed Round 1 case `WF2-028` in `FE-12` covering full-lifecycle bilingual `"Tiếng Việt \| English"` In-App notifications across all 5 workflow pillars, best-effort critical SMTP emails, PostgreSQL-safe `PATCH /api/v1/notifications/read-all`, locale-based rendering, 3-channel chat badge/mark-as-read sync, safe query deep-links, and Admin/Manager toast feedback; updated inventory `76 -> 77` rows (`75` active), Round 1 `52 Passed / 0 Failed / 9 Pending / 16 N/A` (`52/61 = 85.25%`). Verified 2026-11-25: Backend `.\mvnw.cmd spotless:check test "-Dtest=ModulithArchitectureTest,*Notification*Test,AssetNotificationAndExpiryTest,PilotLicenseExpiryCheckServiceTest"` passed `71/71` (including Testcontainers PostgreSQL 17 `NotificationWorkflowIntegrationTest`), and modified service suites passed `160/160`; Frontend `npm run lint` (`0` errors), `npm run build` (`tsc -b && vite build`), and full Vitest `npx vitest run --maxWorkers=3` passed `114/118` files (`4` deprecated skipped, `812` tests passed / `4` skipped / `0` failed).) |

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
| 12 | FE-12 System Notifications & Alert Center | 3 | 0 | 0 | 0 | 3 |
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
| **Current Round 1 subtotal** |  | **52** | **0** | **9** | **16** | **77** |
| **Historical Round 1 subtotal** |  | **45** | **0** | **8** | **3** | **56** |
| **Historical Review 2 baseline (original eight-feature snapshot)** |  | **60** | **0** | **4** | **0** | **64** |
| **Historical implementation-specific pending** |  | **0** | **0** | **1** | **0** | **1** |
| **Round 3 executed cases** |  | **13** | **0** | **0** | **0** | **13** |
| **V29 Round 3 cases** |  | **2** | **0** | **0** | **0** | **2** |
| **Current inventory** |  |  |  |  |  | **77** |
