# Test Statistics sheet source

This table mirrors the `Test Statistics` sheet. Keep the workbook's summary
formulas and labels; update the values from the feature files after each test
round.

## Project metadata

| Field | Value |
| --- | --- |
| Project Name | SmartDroneInspection |
| Project Code | GFA26SE139 |
| Test round | Current case inventory: 67 active IDs across twenty-four atomic features `FE-01` to `FE-24` (preserving all 64 historical records verbatim plus 3 unexecuted standalone coverage cases `WF3-032` in `FE-05`, `WF2-021` in `FE-11`, and `WF3-033` in `FE-22` as `N/A / Pending / Pending`). Flyway set `["1","2","3","4","60","61","62","63","64","65","66"]`; 45 application tables (44 JPA runtime entities, 47 total tables). Current Round 1 records 45 Passed, 0 Failed, 9 Pending, and 13 N/A (`45/54 = 83.33%`). The active-scope historical Round 1 subtotal remains 56 cases (45 Passed, 0 Failed, 8 Pending, 3 N/A; 90.00% passed). Round 3 has 13 Passed executions: `WF3-005`, `WF3-006`, `WF3-009`, `WF3-016`, `WF3-018`, `WF3-019`, `WF3-021`, `WF3-026`, `WF3-027`, `WF3-028`, `WF3-029`, `WF3-030`, and `WF3-031`; `WF3-020` and `WF3-022`–`WF3-025` remain Pending in Round 3. Focused acceptance-timeout, ledger, and payout checks (`WF2-021`, `WF3-032`, `WF3-033`) remain unexecuted as standalone workbook rows (`N/A / Pending / Pending`). |
| Last updated | 2026-11-21 (Report 5 v3.9: unbundled eight grouped modules into twenty-four atomic feature sheets `FE-01`–`FE-24`, preserved all 64 historical case executions and added 3 honest unexecuted standalone cases (`WF3-032`, `WF2-021`, `WF3-033`) totaling 67 active cases, updated `WF3-012` for Sepay VietQR, and synchronized Flyway `V66` (`assets.ownership_information`) plus `frontend PR #139`/`#140`. Full repository baselines verified on 2026-11-20: backend `.\mvnw.cmd verify` 971 passed / 0 failures with Spotless/Modulith/JaCoCo gates met; frontend `npm test` 97 files (93 passed, 4 skipped) / 724 tests (720 passed, 4 skipped, 0 failed); Mobile `flutter test` 56 passed / 0 failures; post-`PR #140` frontend lint (`0` errors), build, and focused auth Vitest (`11` files / `60` tests passed); post-Sepay rebase Testcontainers PostgreSQL 17 checks: `SepayGatewayTest` 6/6, `SepayWebhookControllerTest` 5/5, `SepayPaymentIntegrationTest` 2/2, `VnPayPaymentIntegrationTest` 1/1, `ContractWorkflowServiceTest` 63/63, `ServiceRequestOccurrenceTest` 22/22, and `OccurrenceFinanceResponseTest` 3/3.) |

### Round scope

Historical counts preserve the original eight-feature snapshot, including retired maintenance cases, legacy recurrence scenarios `WF1-018`/`WF1-019`/`WF1-021`, and implementation-specific `WF3-017`. Current Round 1 counts apply to the 67 active IDs in `FE-01`–`FE-24`; ten prior later additions (`WF3-018`–`WF3-020`, `WF3-022`–`WF3-025`, `WF3-029`–`WF3-031`) plus the three unexecuted standalone breakout cases (`WF3-032`, `WF2-021`, `WF3-033`) are N/A for Round 1 (`13 N/A`), and `WF3-021`, `WF3-026`–`WF3-028` are Pending in Round 1. Round 3 executed counts include only cases with Passed or Failed results (`WF3-005`, `WF3-006`, `WF3-009`, `WF3-016`, `WF3-018`, `WF3-019`, `WF3-021`, `WF3-026`–`WF3-031`); `WF3-020`, `WF3-022`–`WF3-025`, `WF3-032`, `WF2-021`, and `WF3-033` remain Pending.

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
| 8 | FE-08 Service Requests (One-Time & Recurring) & VND Quotations | 3 | 0 | 0 | 0 | 3 |
| 9 | FE-09 Offline Signed Contract & Occurrence Dispatch Scheduling | 4 | 0 | 1 | 0 | 5 |
| 10 | FE-10 Dual-Channel Messaging (Order Chat & Inspection Chat) | 1 | 0 | 0 | 0 | 1 |
| 11 | FE-11 Assignment Acceptance Timeout & Escalation Handling | 0 | 0 | 0 | 1 | 1 |
| 12 | FE-12 System Notifications & Alert Center | 1 | 0 | 0 | 0 | 1 |
| 13 | FE-13 Flight Permit Upload & Independent Verification Gate | 2 | 0 | 0 | 0 | 2 |
| 14 | FE-14 On-Site Field Session & SmartDroneHub MAVLink Telemetry | 4 | 0 | 0 | 1 | 5 |
| 15 | FE-15 Field Evidence Intake & Chunked Video Processing Pipeline | 1 | 0 | 0 | 4 | 5 |
| 16 | FE-16 AI Defect Detection (`YOLO11` + Vision Fallback) & Findings Confirmation | 6 | 0 | 1 | 0 | 7 |
| 17 | FE-17 AI Case/Standard Retrieval (`pgvector` RAG), Note Drafting & Report Summary | 0 | 0 | 0 | 2 | 2 |
| 18 | FE-18 Inspection Report Compilation, Independent Review & Official Publication | 4 | 0 | 0 | 0 | 4 |
| 19 | FE-19 Customer Report Acceptance & Clarification Workflow | 0 | 0 | 1 | 0 | 1 |
| 20 | FE-20 Online Service Fee Payment (`PayOS` VietQR & `VNPay`) | 0 | 0 | 0 | 2 | 2 |
| 21 | FE-21 Payment Deadlines, Invoices & Payment Document Management | 0 | 0 | 2 | 0 | 2 |
| 22 | FE-22 Partner Inspector Payout Reconciliation | 0 | 0 | 0 | 1 | 1 |
| 23 | FE-23 Evidence-Backed Refunds & Receivable Recovery | 0 | 0 | 1 | 0 | 1 |
| 24 | FE-24 Post-Remediation Re-inspection & Defect Verification | 0 | 0 | 1 | 1 | 2 |
| **Current Round 1 subtotal** |  | **45** | **0** | **9** | **13** | **67** |
| **Historical Round 1 subtotal** |  | **45** | **0** | **8** | **3** | **56** |
| **Historical Review 2 baseline (original eight-feature snapshot)** |  | **60** | **0** | **4** | **0** | **64** |
| **Historical implementation-specific pending** |  | **0** | **0** | **1** | **0** | **1** |
| **Round 3 executed cases** |  | **13** | **0** | **0** | **0** | **13** |
| **V29 Round 3 cases** |  | **2** | **0** | **0** | **0** | **2** |
| **Current inventory** |  |  |  |  |  | **67** |
