# Test Statistics sheet source

This table mirrors the `Test Statistics` sheet. Keep the workbook's summary
formulas and labels; update the values from the feature files after each test
round.

## Project metadata

| Field | Value |
| --- | --- |
| Project Name | SmartDroneInspection |
| Project Code | GFA26SE139 |
| Test round | Current case inventory: 67 IDs across 8 features FE-01 to FE-08, including two Round 3 V29 finance cases. Historical Round 1/2 figures below are retained as originally recorded. Round 3 includes two earlier FE-06 cases (WF3-006, WF3-016) plus the V29 cases WF3-018/019. V29 schema, persistence inventory, finance lifecycle, PayOS, and VNPay tests passed with Docker/Testcontainers on 2026-11-05; other feature suites were not run. |
| Last updated | 2026-11-05 (V29 schema, finance lifecycle, PayOS/VNPay integrations Passed; non-payment feature suites not run. Historical Round 1 totals remain 65 IDs: 60 Passed, 0 Failed, 5 Pending; 92.31% overall / 93.75% of the 64-case historical baseline). |

### Round 1 and Round 3 summaries

Feature rows and the current Round 1 subtotal reflect all 67 current case IDs; the two V29 cases added later are `N/A` in Round 1. The separate historical Round 1 subtotal preserves the original 65-case results. Historical counts include legacy recurrence scenarios WF1-018, WF1-019, and WF1-021 (excluded from current target coverage) and implementation-specific WF3-017. Historical totals and pass-rate formulas must not be read as current V1–V29 results. The Round 3 executed subtotal counts cases with an executed `Passed` or `Failed` result; the V29 row is a subset of that subtotal. Specifically, WF3-006, WF3-016, WF3-018, and WF3-019 were Passed. Focused V29 schema, payment lifecycle, PayOS, and VNPay verification passed on 2026-11-05; non-payment feature verification was not run in this change.

## Module summary

| No | Module code | Passed | Failed | Pending | N/A | Number of test cases |
| ---: | --- | ---: | ---: | ---: | ---: | ---: |
| 1 | Authentication, Google OAuth2 & 5-Role Access Control | 5 | 0 | 0 | 0 | 5 |
| 2 | Partner Onboarding, Workforce, Asset & Inspector Drone Registry | 10 | 0 | 1 | 0 | 11 |
| 3 | Recurring Service Requests, Contract Occurrences & Outbox Notifications | 5 | 0 | 0 | 0 | 5 |
| 4 | Service Requests, Quotations, Contracts, Dispatch & Airspace Map | 5 | 0 | 0 | 0 | 5 |
| 5 | Flight Permit Gate, Field Execution, Dashboard & Calendar | 10 | 0 | 1 | 0 | 11 |
| 6 | Evidence Intake, YOLO11 Detection, Auto-Compiled Report & PayOS | 10 | 0 | 2 | 2 | 14 |
| 7 | Maintenance Work Orders, RAG Scope/Norms Advisor & Repair Execution | 10 | 0 | 1 | 0 | 11 |
| 8 | Completion Report, 3-Way Re-inspection Verification & Cost Closure | 5 | 0 | 0 | 0 | 5 |
| **Current Round 1 subtotal** |  | **60** | **0** | **5** | **2** | **67** |
| **Historical Round 1 subtotal** |  | **60** | **0** | **5** | **0** | **65** |
| **Historical Review 2 baseline** |  | **60** | **0** | **4** | **0** | **64** |
| **Historical implementation-specific pending** |  | **0** | **0** | **1** | **0** | **1** |
| **Round 3 executed cases** |  | **4** | **0** | **0** | **0** | **4** |
| **V29 Round 3 cases** |  | **2** | **0** | **0** | **0** | **2** |
| **Current inventory** |  |  |  |  |  | **67** |
