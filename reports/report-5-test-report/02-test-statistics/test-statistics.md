# Test Statistics sheet source

This table mirrors the `Test Statistics` sheet. Keep the workbook's summary
formulas and labels; update the values from the feature files after each test
round.

## Project metadata

| Field | Value |
| --- | --- |
| Project Name | SmartDroneInspection |
| Project Code | GFA26SE139 |
| Test round | 65 functional test cases across 8 product features FE-01 to FE-08 (2 features per team member, mapped 1-to-1 to Feature 1 to Feature 8) verified against the Flyway V1–V28 PostgreSQL 17 schema (36 tables): Round 1 records 60 Passed, 0 Failed, 5 Pending (92.31% overall / 93.75% of the 64-case baseline); Round 2 verified all 15 automated FE-07/FE-08 maintenance cases; Round 3 verified WF3-006 and WF3-016 direct report publication and on-demand PDF supersession. |
| Last updated | 2026-11-04 (Synchronized with Flyway V1–V28 schema, 4-state InspectionReport lifecycle, SmartDroneHub V28 telemetry/trace sync, and PayOS VietQR / VNPay v2.1.0 online payment gateways; 60 Passed, 0 Failed, 5 Pending across 65 cases). |

## Module summary

| No | Module code | Passed | Failed | Pending | N/A | Number of test cases |
| ---: | --- | ---: | ---: | ---: | ---: | ---: |
| 1 | Authentication, Google OAuth2 & 5-Role Access Control | 5 | 0 | 0 | 0 | 5 |
| 2 | Partner Onboarding, Workforce, Asset & Inspector Drone Registry | 10 | 0 | 1 | 0 | 11 |
| 3 | Recurring Service Requests, Contract Occurrences & Outbox Notifications | 5 | 0 | 0 | 0 | 5 |
| 4 | Service Requests, Quotations, Contracts, Dispatch & Airspace Map | 5 | 0 | 0 | 0 | 5 |
| 5 | Flight Permit Gate, Field Execution, Dashboard & Calendar | 10 | 0 | 1 | 0 | 11 |
| 6 | Evidence Intake, YOLO11 Detection, Auto-Compiled Report & PayOS | 10 | 0 | 2 | 0 | 12 |
| 7 | Maintenance Work Orders, RAG Scope/Norms Advisor & Repair Execution | 10 | 0 | 1 | 0 | 11 |
| 8 | Completion Report, 3-Way Re-inspection Verification & Cost Closure | 5 | 0 | 0 | 0 | 5 |
| **Subtotal** |  | **60** | **0** | **5** | **0** | **65** |
| **Review 2 baseline** |  | **60** | **0** | **4** | **0** | **64** |
| **Implementation-specific pending** |  | **0** | **0** | **1** | **0** | **1** |
