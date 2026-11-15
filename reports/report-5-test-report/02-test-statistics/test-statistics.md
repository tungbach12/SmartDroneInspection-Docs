# Test Statistics sheet source

This table mirrors the `Test Statistics` sheet. Keep the workbook's summary
formulas and labels; update the values from the feature files after each test
round.

## Project metadata

| Field | Value |
| --- | --- |
| Project Name | SmartDroneInspection |
| Project Code | GFA26SE139 |
| Test round | Current case inventory: 57 active IDs across six features FE-01 to FE-06. Current Round 1 records 45 Passed, 0 Failed, 5 Pending, and 7 N/A cases added later. The active-scope historical Round 1 subtotal is 49 cases (45 Passed, 0 Failed, 4 Pending; 91.84% passed). These recalculated counts exclude retired maintenance cases and are not directly comparable with the original eight-feature report. Round 3 currently has three Passed executions: WF3-006, WF3-016, and WF3-018; WF3-019 and WF3-021 remain Pending pending finance/refund lifecycle re-execution; WF3-020 and WF3-022–WF3-025 remain Pending in Round 3. The historical V29 finance cases were verified against Flyway V1–V29 on PostgreSQL 17 with Docker/Testcontainers on 2026-11-05; focused recurring-qualification, eligibility-hardening, refund, and V55 media-optimization checks are recorded as evidence only and do not change unexecuted round statuses. |
| Last updated | 2026-11-15 (full backend `./mvnw.cmd spotless:apply verify` ran 596/596 passing tests with Docker/Testcontainers active including `FlightPermitVerificationIntegrationTest`; `./mvnw.cmd jacoco:check@verify` exited at the pre-existing `0.80` bundle gate with `0.71` line / `0.70` instruction. Frontend `npm run lint` (0 errors, 40 warnings), `npm run build` (`tsc -b && vite build`), and Vitest (570 passed, 4 pre-existing skipped out of 574 across 79 passed and 4 skipped of 83 files, plus 6 targeted flight-permit test files 77/77) passed; live Nginx proxy & Docker Compose E2E walkthrough remain Pending.) |

### Round scope

Historical counts preserve the original eight-feature report, including retired maintenance cases, legacy recurrence scenarios WF1-018/WF1-019/WF1-021, and implementation-specific WF3-017. Current Round 1 counts apply only to the 57 active IDs in FE-01–FE-06; seven later additions (`WF3-018`–`WF3-020`, `WF3-022`–`WF3-025`) are N/A for that round and WF3-021 is Pending. Round 3 executed counts include only cases with Passed or Failed results (`WF3-006`, `WF3-016`, `WF3-018`); WF3-019–WF3-025 remain Pending.

## Module summary

| No | Module code | Passed | Failed | Pending | N/A | Number of test cases |
| ---: | --- | ---: | ---: | ---: | ---: | ---: |
| 1 | Authentication, Google OAuth2 & 5-Role Access Control | 5 | 0 | 0 | 0 | 5 |
| 2 | Partner Onboarding, Workforce, Asset & Inspector Drone Registry | 10 | 0 | 1 | 0 | 11 |
| 3 | Recurring Service Requests, Contract Occurrences & Outbox Notifications | 5 | 0 | 0 | 0 | 5 |
| 4 | Service Requests, Quotations, Contracts, Dispatch & Airspace Map | 5 | 0 | 0 | 0 | 5 |
| 5 | Flight Permit Gate, Field Execution, Dashboard & Calendar | 10 | 0 | 1 | 1 | 12 |
| 6 | Evidence Intake, YOLO11 Detection, Auto-Compiled Report & PayOS | 10 | 0 | 3 | 6 | 19 |
| **Current Round 1 subtotal** |  | **45** | **0** | **5** | **7** | **57** |
| **Historical Round 1 subtotal** |  | **45** | **0** | **4** | **0** | **49** |
| **Historical Review 2 baseline (original eight-feature report)** |  | **60** | **0** | **4** | **0** | **64** |
| **Historical implementation-specific pending** |  | **0** | **0** | **1** | **0** | **1** |
| **Round 3 executed cases** |  | **3** | **0** | **0** | **0** | **3** |
| **V29 Round 3 cases** |  | **1** | **0** | **1** | **0** | **2** |
| **Current inventory** |  |  |  |  |  | **57** |
