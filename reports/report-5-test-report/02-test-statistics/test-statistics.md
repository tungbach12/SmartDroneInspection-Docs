# Test Statistics sheet source

This table mirrors the `Test Statistics` sheet. Keep the workbook's summary
formulas and labels; update the values from the feature files after each test
round.

## Project metadata

| Field | Value |
| --- | --- |
| Project Name | SmartDroneInspection |
| Project Code | GFA26SE139 |
| Test round | Current case inventory: 64 active IDs across eight features `FE-01` to `FE-08` (two per main flow `MF1` to `MF4`), including profile update `WF1-022`. FE-04 Manager assignment, Inspector–Customer chat and chat-attachment checks are recorded as focused evidence under existing `WF2-001` and do not add another case ID or change Round 2 status. Flyway set `["1","2","3","4","60","61","62","63","64","65"]`; 45 application tables (44 JPA runtime entities, 47 total tables). Current Round 1 records 45 Passed, 0 Failed, 9 Pending, and 10 N/A. The active-scope historical Round 1 subtotal is 56 cases (45 Passed, 0 Failed, 8 Pending, 3 N/A; 90.00% passed). These recalculated counts exclude the retired maintenance cases that the original eight-feature snapshot had carried. Round 3 has 13 Passed executions: `WF3-005`, `WF3-006`, `WF3-009`, `WF3-016`, `WF3-018`, `WF3-019`, `WF3-021`, `WF3-026`, `WF3-027`, `WF3-028`, `WF3-029`, `WF3-030`, and `WF3-031`; `WF3-020` and `WF3-022`–`WF3-025` remain Pending in Round 3. The historical V29 finance cases were verified against Flyway V1–V29 on PostgreSQL 17 with Docker/Testcontainers on 2026-11-05; focused recurring-qualification, eligibility-hardening, refund, and V55 media-optimization checks are recorded as evidence only and do not change unexecuted round statuses. |
| Last updated | 2026-11-21 (Report 5 v3.9: the online payment channel changed from PayOS to Sepay and FE-08 `WF3-012` was re-worded for the VietQR transfer code. Sepay swap re-verification on Testcontainers PostgreSQL 17 after rebasing onto `main`: `SepayGatewayTest` 6/6, `SepayWebhookControllerTest` 5/5, `SepayPaymentIntegrationTest` 2/2, `VnPayPaymentIntegrationTest` 1/1, `ContractWorkflowServiceTest` 63/63, `ServiceRequestOccurrenceTest` 22/22 and `OccurrenceFinanceResponseTest` 3/3. A full `verify` was not re-run after the rebase. Case counts are unchanged: 64 active cases (Round 1 45 Passed / 0 Failed / 9 Pending / 10 N/A; Round 3 executed 13), and `WF3-012` stays Pending until the live staging walkthrough runs.) |

### Round scope

Historical counts preserve the original eight-feature snapshot, including retired maintenance cases, legacy recurrence scenarios `WF1-018`/`WF1-019`/`WF1-021`, and implementation-specific `WF3-017`. Current Round 1 counts apply only to the 64 active IDs in `FE-01`–`FE-08`; ten later additions (`WF3-018`–`WF3-020`, `WF3-022`–`WF3-025`, `WF3-029`–`WF3-031`) are N/A for that round and `WF3-021`, `WF3-026`–`WF3-028` are Pending in Round 1. Round 3 executed counts include only cases with Passed or Failed results (`WF3-005`, `WF3-006`, `WF3-009`, `WF3-016`, `WF3-018`, `WF3-019`, `WF3-021`, `WF3-026`–`WF3-031`); `WF3-020` and `WF3-022`–`WF3-025` remain Pending.

## Module summary

| No | Module code | Passed | Failed | Pending | N/A | Number of test cases |
| ---: | --- | ---: | ---: | ---: | ---: | ---: |
| 1 | FE-01 Authentication, Account Access & Four-Role Portal Scope | 7 | 0 | 1 | 0 | 8 |
| 2 | FE-02 Partner Inspector Application & Owned Drone Registry | 6 | 0 | 1 | 0 | 7 |
| 3 | FE-03 Buildings, Airspace Screening, Occurrences & Notifications | 8 | 0 | 0 | 0 | 8 |
| 4 | FE-04 Service Requests, VND Quotations, Agreements & Dispatch | 7 | 0 | 1 | 0 | 8 |
| 5 | FE-05 Flight Permit Gate & On-Site Field Sessions | 6 | 0 | 0 | 1 | 7 |
| 6 | FE-06 Evidence Intake & Human-Reviewed Defect Detection | 7 | 0 | 2 | 5 | 14 |
| 7 | FE-07 Inspection Report Preparation, Review & Publication | 4 | 0 | 0 | 1 | 5 |
| 8 | FE-08 Customer Acceptance & Payment Settlement | 0 | 0 | 4 | 3 | 7 |
| **Current Round 1 subtotal** |  | **45** | **0** | **9** | **10** | **64** |
| **Historical Round 1 subtotal** |  | **45** | **0** | **8** | **3** | **56** |
| **Historical Review 2 baseline (original eight-feature snapshot)** |  | **60** | **0** | **4** | **0** | **64** |
| **Historical implementation-specific pending** |  | **0** | **0** | **1** | **0** | **1** |
| **Round 3 executed cases** |  | **13** | **0** | **0** | **0** | **13** |
| **V29 Round 3 cases** |  | **2** | **0** | **0** | **0** | **2** |
| **Current inventory** |  |  |  |  |  | **64** |
