# Test Statistics sheet source

This table mirrors the `Test Statistics` sheet. Keep the workbook's summary
formulas and labels; update the values from the feature files after each test
round.

## Project metadata

| Field | Value |
| --- | --- |
| Project Name | SmartDroneInspection |
| Project Code | GFA26SE139 |
| Test round | Current case inventory: 58 active IDs across eight features FE-01 to FE-08 (two per main flow MF1 to MF4), including profile update `WF1-022`. FE-04 Manager assignment and chat-attachment checks are recorded as focused evidence under existing `WF2-001` and do not add another case ID or change Round 2 status. Current Round 1 records 45 Passed, 0 Failed, 6 Pending, and 7 N/A cases added later. The active-scope historical Round 1 subtotal is 50 cases (45 Passed, 0 Failed, 5 Pending; 90.00% passed). These recalculated counts exclude the retired maintenance cases that the original eight-feature snapshot had carried. Round 3 currently has three Passed executions: WF3-006, WF3-016, and WF3-018; WF3-019 and WF3-021 remain Pending pending finance/refund lifecycle re-execution; WF3-020 and WF3-022–WF3-025 remain Pending in Round 3. The historical V29 finance cases were verified against Flyway V1–V29 on PostgreSQL 17 with Docker/Testcontainers on 2026-11-05; focused recurring-qualification, eligibility-hardening, refund, and V55 media-optimization checks are recorded as evidence only and do not change unexecuted round statuses. |
| Last updated | 2026-11-16 (Backend focused controller tests 7/7 and service tests 54/54, migration/inventory tests 5/5, and WorkflowBaselineTest 3/3 passed. Full `./mvnw.cmd verify` ran 626 tests with 4 errors and 4 failures: four FFmpeg-dependent tests cannot launch `ffmpeg`; schema inventory expectations were corrected and focused tests pass. Vitest cannot start (`Cannot read properties of undefined (reading 'config')`) even on a trivial test and on pure upstream; frontend production build succeeds. Local disposable UI E2E uploaded PNG+PDF and both scoped downloads returned 200; WF2-001 Round 2 remains Pending pending full connected roles and valid-image rendering.) |

### Round scope

Historical counts preserve the original eight-feature snapshot, including retired maintenance cases, legacy recurrence scenarios WF1-018/WF1-019/WF1-021, and implementation-specific WF3-017. Current Round 1 counts apply only to the 58 active IDs in FE-01–FE-08; seven later additions (`WF3-018`–`WF3-020`, `WF3-022`–`WF3-025`) are N/A for that round and WF3-021 is Pending. Round 3 executed counts include only cases with Passed or Failed results (`WF3-006`, `WF3-016`, `WF3-018`); WF3-019–WF3-025 remain Pending.

## Module summary

| No | Module code | Passed | Failed | Pending | N/A | Number of test cases |
| ---: | --- | ---: | ---: | ---: | ---: | ---: |
| 1 | FE-01 Authentication, Account Access & Four-Role Portal Scope | 7 | 0 | 1 | 0 | 8 |
| 2 | FE-02 Partner Inspector Application & Owned Drone Registry | 6 | 0 | 1 | 0 | 7 |
| 3 | FE-03 Buildings, Airspace Screening, Occurrences & Notifications | 8 | 0 | 0 | 0 | 8 |
| 4 | FE-04 Service Requests, VND Quotations, Agreements & Dispatch | 7 | 0 | 1 | 0 | 8 |
| 5 | FE-05 Flight Permit Gate & On-Site Field Sessions | 6 | 0 | 0 | 1 | 7 |
| 6 | FE-06 Evidence Intake & Human-Reviewed Defect Detection | 7 | 0 | 1 | 4 | 12 |
| 7 | FE-07 Inspection Report Preparation, Review & Publication | 4 | 0 | 0 | 0 | 4 |
| 8 | FE-08 Customer Acceptance & Payment Settlement | 0 | 0 | 2 | 2 | 4 |
| **Current Round 1 subtotal** |  | **45** | **0** | **6** | **7** | **58** |
| **Historical Round 1 subtotal** |  | **45** | **0** | **5** | **0** | **50** |
| **Historical Review 2 baseline (original eight-feature snapshot)** |  | **60** | **0** | **4** | **0** | **64** |
| **Historical implementation-specific pending** |  | **0** | **0** | **1** | **0** | **1** |
| **Round 3 executed cases** |  | **3** | **0** | **0** | **0** | **3** |
| **V29 Round 3 cases** |  | **1** | **0** | **1** | **0** | **2** |
| **Current inventory** |  |  |  |  |  | **58** |
