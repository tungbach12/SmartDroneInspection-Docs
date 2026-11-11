# Test Statistics sheet source

This table mirrors the `Test Statistics` sheet. Keep the workbook's summary
formulas and labels; update the values from the feature files after each test
round.

## Project metadata

| Field | Value |
| --- | --- |
| Project Name | SmartDroneInspection |
| Project Code | GFA26SE139 |
| Test round | Current case inventory: 69 IDs across eight features FE-01 to FE-08. WF3-020 remains Pending in Round 3; new WF3-021 (V33 payment/refund/order/payout controls) is Pending until schema-backed integration checks execute. Current Round 1 records 60 Passed, 0 Failed, 6 Pending, and three later additions marked N/A because they were added after that round. Historical Round 1 remains 65 cases (60 Passed, 0 Failed, 5 Pending; 92.31% overall / 93.75% of the 64-case baseline). Round 3 currently has three Passed executions: WF3-006, WF3-016 and WF3-018; WF3-019 is Pending pending re-execution against the revised payout contract. WF3-018 is the only current Passed V29 subset case. Historical V29 integration execution ran on 2026-11-05; on 2026-11-11 the focused ContractWorkflowServiceTest and ModulithArchitectureTest passed 39 tests, while V33 database/gateway integration checks were not run because Docker is unavailable. |
| Last updated | 2026-11-11 (added Pending WF3-021; focused unit/architecture tests passed, V33 DB/integration verification remains unexecuted). |

### Round scope

Historical counts include legacy recurrence scenarios WF1-018, WF1-019, and WF1-021 (excluded from the current target) and implementation-specific WF3-017. The current Round 1 subtotal includes all current case IDs, with WF3-020 and later V29 additions marked N/A and WF3-021 Pending; the separate historical subtotal preserves the original 65-case results. Round 3 executed counts include only cases with Passed or Failed results, and the V29 subtotal is included within that count.

## Module summary

| No | Module code | Passed | Failed | Pending | N/A | Number of test cases |
| ---: | --- | ---: | ---: | ---: | ---: | ---: |
| 1 | Authentication, Google OAuth2 & 5-Role Access Control | 5 | 0 | 0 | 0 | 5 |
| 2 | Partner Onboarding, Workforce, Asset & Inspector Drone Registry | 10 | 0 | 1 | 0 | 11 |
| 3 | Recurring Service Requests, Contract Occurrences & Outbox Notifications | 5 | 0 | 0 | 0 | 5 |
| 4 | Service Requests, Quotations, Contracts, Dispatch & Airspace Map | 5 | 0 | 0 | 0 | 5 |
| 5 | Flight Permit Gate, Field Execution, Dashboard & Calendar | 10 | 0 | 1 | 1 | 12 |
| 6 | Evidence Intake, YOLO11 Detection, Auto-Compiled Report & PayOS | 10 | 0 | 3 | 2 | 15 |
| 7 | Maintenance Work Orders, RAG Scope/Norms Advisor & Repair Execution | 10 | 0 | 1 | 0 | 11 |
| 8 | Completion Report, 3-Way Re-inspection Verification & Cost Closure | 5 | 0 | 0 | 0 | 5 |
| **Current Round 1 subtotal** |  | **60** | **0** | **6** | **3** | **69** |
| **Historical Round 1 subtotal** |  | **60** | **0** | **5** | **0** | **65** |
| **Historical Review 2 baseline** |  | **60** | **0** | **4** | **0** | **64** |
| **Historical implementation-specific pending** |  | **0** | **0** | **1** | **0** | **1** |
| **Round 3 executed cases** |  | **3** | **0** | **0** | **0** | **3** |
| **V29 Round 3 cases** |  | **1** | **0** | **1** | **0** | **2** |
| **Current inventory** |  |  |  |  |  | **69** |
