# Test Statistics sheet source

This table mirrors the `Test Statistics` sheet. Keep the workbook's summary
formulas and labels; update the values from the feature files after each test
round.

## Project metadata

| Field | Value |
| --- | --- |
| Project Name | SmartDroneInspection |
| Project Code | GFA26SE139 |
| Test round | Current case inventory: 53 active IDs across six features FE-01 to FE-06. Current Round 1 records 45 Passed, 0 Failed, 5 Pending, and 3 N/A cases added later. The active-scope historical Round 1 subtotal is 49 cases (45 Passed, 0 Failed, 4 Pending; 91.84% passed). These recalculated counts exclude retired maintenance cases and are not directly comparable with the original eight-feature report. Round 3 currently has three Passed executions: WF3-006, WF3-016, and WF3-018; WF3-019 and WF3-021 remain Pending pending finance/refund lifecycle re-execution; WF3-020 remains Pending in Round 3. The historical V29 finance cases were verified against Flyway V1–V29 on PostgreSQL 17 with Docker/Testcontainers on 2026-11-05; focused recurring-qualification, eligibility-hardening, and refund regression checks are recorded as evidence only and do not change case statuses or totals. |
| Last updated | 2026-11-14 (full backend `./mvnw test` passed 566/566 with Docker/Testcontainers active, and focused eligibility/dispatch/session/Modulith suites passed 151/151: `DroneTest`, `DroneApiIntegrationTest`, `UserAccessInspectorProfileProjectionTest`, `InspectorProfileServiceTest`, `PartnerCandidateEvaluationTest`, `PartnerRegistryServiceTest`, `Mf2InspectionAssignmentAdapterTest`, `ContractWorkflowServiceTest`, `InspectionCreationServiceTest`, `InspectionFieldSessionDroneGuardTest`, `InspectionCreationApiIntegrationTest`, `InspectionManagerDispatchApiIntegrationTest`, `InspectionFieldSessionServiceTest`, `InspectionFieldSessionApiIntegrationTest`, `ModulithArchitectureTest`. `./mvnw jacoco:check@verify` exited at the `0.80` bundle gate with `0.72` line / `0.70` instruction. No existing round status was changed; WF2-001 Round 2 and WF3-019/WF3-021 Round 3 remain Pending.) |

### Round scope

Historical counts preserve the original eight-feature report, including retired maintenance cases, legacy recurrence scenarios WF1-018/WF1-019/WF1-021, and implementation-specific WF3-017. Current Round 1 counts apply only to the 53 active IDs in FE-01–FE-06; three later additions are N/A for that round and WF3-021 is Pending. Round 3 executed counts include only cases with Passed or Failed results (`WF3-006`, `WF3-016`, `WF3-018`); WF3-019, WF3-020, and WF3-021 remain Pending.

## Module summary

| No | Module code | Passed | Failed | Pending | N/A | Number of test cases |
| ---: | --- | ---: | ---: | ---: | ---: | ---: |
| 1 | Authentication, Google OAuth2 & 5-Role Access Control | 5 | 0 | 0 | 0 | 5 |
| 2 | Partner Onboarding, Workforce, Asset & Inspector Drone Registry | 10 | 0 | 1 | 0 | 11 |
| 3 | Recurring Service Requests, Contract Occurrences & Outbox Notifications | 5 | 0 | 0 | 0 | 5 |
| 4 | Service Requests, Quotations, Contracts, Dispatch & Airspace Map | 5 | 0 | 0 | 0 | 5 |
| 5 | Flight Permit Gate, Field Execution, Dashboard & Calendar | 10 | 0 | 1 | 1 | 12 |
| 6 | Evidence Intake, YOLO11 Detection, Auto-Compiled Report & PayOS | 10 | 0 | 3 | 2 | 15 |
| **Current Round 1 subtotal** |  | **45** | **0** | **5** | **3** | **53** |
| **Historical Round 1 subtotal** |  | **45** | **0** | **4** | **0** | **49** |
| **Historical Review 2 baseline (original eight-feature report)** |  | **60** | **0** | **4** | **0** | **64** |
| **Historical implementation-specific pending** |  | **0** | **0** | **1** | **0** | **1** |
| **Round 3 executed cases** |  | **3** | **0** | **0** | **0** | **3** |
| **V29 Round 3 cases** |  | **1** | **0** | **1** | **0** | **2** |
| **Current inventory** |  |  |  |  |  | **53** |
