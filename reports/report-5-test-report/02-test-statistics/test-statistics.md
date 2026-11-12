# Test Statistics sheet source

This table mirrors the `Test Statistics` sheet. Keep the workbook's summary
formulas and labels; update the values from the feature files after each test
round.

## Project metadata

| Field | Value |
| --- | --- |
| Project Name | SmartDroneInspection |
| Project Code | GFA26SE139 |
| Test round | Current case inventory: 52 active IDs across six features FE-01 to FE-06. Current Round 1 records 45 Passed, 0 Failed, 4 Pending, and 3 N/A cases added later. The active-scope historical Round 1 subtotal is 49 cases (45 Passed, 0 Failed, 4 Pending; 91.84% passed). These recalculated counts exclude retired maintenance cases and are not directly comparable with the original eight-feature report. Round 3 has four Passed executions: WF3-006, WF3-016, WF3-018 and WF3-019. WF3-020 remains Pending in Round 3. The two V29 finance cases were verified against Flyway V1–V29 on PostgreSQL 17 with Docker/Testcontainers on 2026-11-05; other feature suites were not run. Focused recurring-qualification regression checks are recorded as evidence only and do not change case statuses or totals. |
| Last updated | 2026-11-12 (focused recurring-partner qualification regression checks passed: backend ContractWorkflowServiceTest and PartnerRegistryServiceTest 50/50; frontend ContractsPage.test.tsx 7/7 and production build passed. These checks are not connected end-to-end evidence; WF2-001 Round 2 remains Pending until Customer→Manager→signed-contract→dispatch execution.) |

### Round scope

Historical counts preserve the original eight-feature report, including retired maintenance cases, legacy recurrence scenarios WF1-018/WF1-019/WF1-021, and implementation-specific WF3-017. Current Round 1 counts apply only to the 52 active IDs in FE-01–FE-06; three later additions are N/A for that round. Round 3 executed counts include only cases with Passed or Failed results; WF3-020 remains Pending, and the two V29 cases are included in the four Passed Round 3 cases.

## Module summary

| No | Module code | Passed | Failed | Pending | N/A | Number of test cases |
| ---: | --- | ---: | ---: | ---: | ---: | ---: |
| 1 | Authentication, Google OAuth2 & 5-Role Access Control | 5 | 0 | 0 | 0 | 5 |
| 2 | Partner Onboarding, Workforce, Asset & Inspector Drone Registry | 10 | 0 | 1 | 0 | 11 |
| 3 | Recurring Service Requests, Contract Occurrences & Outbox Notifications | 5 | 0 | 0 | 0 | 5 |
| 4 | Service Requests, Quotations, Contracts, Dispatch & Airspace Map | 5 | 0 | 0 | 0 | 5 |
| 5 | Flight Permit Gate, Field Execution, Dashboard & Calendar | 10 | 0 | 1 | 1 | 12 |
| 6 | Evidence Intake, YOLO11 Detection, Auto-Compiled Report & PayOS | 10 | 0 | 2 | 2 | 14 |
| **Current Round 1 subtotal** |  | **45** | **0** | **4** | **3** | **52** |
| **Historical Round 1 subtotal** |  | **45** | **0** | **4** | **0** | **49** |
| **Historical Review 2 baseline (original eight-feature report)** |  | **60** | **0** | **4** | **0** | **64** |
| **Historical implementation-specific pending** |  | **0** | **0** | **1** | **0** | **1** |
| **Round 3 executed cases** |  | **4** | **0** | **0** | **0** | **4** |
| **V29 Round 3 cases** |  | **2** | **0** | **0** | **0** | **2** |
| **Current inventory** |  |  |  |  |  | **52** |
