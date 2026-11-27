# Test Statistics sheet source

This table mirrors the `Test Statistics` sheet. Keep the workbook's summary
formulas and labels; update the values from the feature files after each test
round.

## Project metadata

| Field | Value |
| --- | --- |
| Project Name | SmartDroneInspection |
| Project Code | GFA26SE139 |
| Test round | Final Release — Round 3 (All 24 modules). Inventory comprises 80 rows across 24 features: 77 active verified cases and 3 retired/superseded N/A cases (`WF2-008`, `WF2-009`, `WF2-015`). Round 1 retains 52 Passed, 0 Failed, 9 Pending, 19 N/A; Round 3 records 77 Passed, 0 Failed, 0 Pending, 3 N/A. |
| Last updated | 2026-11-27 (Report 5 v3.21). Reconciled all 24 feature sheets for Final Release Round 3 with live `agent-browser` walkthroughs and Nov 26–27 automated suites. |

### Round scope

The historical Round 1 subtotal is 56 cases (45/56 Passed). Final Release Round 3 executes all 77 active cases across all 24 features (`77/77 Passed`, `0 Failed`, `0 Pending`, and `3 N/A` for superseded `WF2-008`/`WF2-009` and retired mobile case `WF2-015`).

## Module summary

| No | Module code | Passed | Failed | Pending | N/A | Number of test cases |
| ---: | --- | ---: | ---: | ---: | ---: | ---: |
| 1 | FE-01 Account Authentication, OTP & 4-Role Access Control | 7 | 0 | 0 | 0 | 7 |
| 2 | FE-02 Partner Inspector Application & Qualification Management | 4 | 0 | 0 | 0 | 4 |
| 3 | FE-03 Inspector-Owned Drone Registration & Fleet Management | 3 | 0 | 0 | 0 | 3 |
| 4 | FE-04 Interactive Location Map & No-Fly Zone Airspace Screening | 3 | 0 | 0 | 0 | 3 |
| 5 | FE-05 Financial History & Revenue/Payment Ledger | 1 | 0 | 0 | 0 | 1 |
| 6 | FE-06 Building Asset Registry, Checkpoints & Reference Documents | 3 | 0 | 0 | 0 | 3 |
| 7 | FE-07 Restricted Airspace Advisory Warning & Immediate Onboarding | 1 | 0 | 0 | 0 | 1 |
| 8 | FE-08 Service Requests (One-Time & Recurring) & VND Quotations | 6 | 0 | 0 | 0 | 6 |
| 9 | FE-09 Offline Signed Contract & Occurrence Dispatch Scheduling | 6 | 0 | 0 | 1 | 7 |
| 10 | FE-10 Dual-Channel Messaging (Order Chat & Inspection Chat) | 2 | 0 | 0 | 0 | 2 |
| 11 | FE-11 Assignment Acceptance Timeout & Escalation Handling | 2 | 0 | 0 | 0 | 2 |
| 12 | FE-12 System Notifications & Alert Center | 3 | 0 | 0 | 0 | 3 |
| 13 | FE-13 Flight Permit Upload & Independent Verification Gate | 4 | 0 | 0 | 2 | 6 |
| 14 | FE-14 On-Site Field Session & SmartDroneHub MAVLink Telemetry | 5 | 0 | 0 | 0 | 5 |
| 15 | FE-15 Field Evidence Intake & Chunked Video Processing Pipeline | 5 | 0 | 0 | 0 | 5 |
| 16 | FE-16 AI Defect Detection (`YOLO11` + Vision Fallback) & Findings Confirmation | 7 | 0 | 0 | 0 | 7 |
| 17 | FE-17 AI Case/Standard Retrieval (`pgvector` RAG), Note Drafting & Report Summary | 2 | 0 | 0 | 0 | 2 |
| 18 | FE-18 Inspection Report Compilation, Independent Review & Official Publication | 4 | 0 | 0 | 0 | 4 |
| 19 | FE-19 Customer Report Acceptance & Clarification Workflow | 1 | 0 | 0 | 0 | 1 |
| 20 | FE-20 Online Service Fee Payment (`Sepay` VietQR & `VNPay`) | 2 | 0 | 0 | 0 | 2 |
| 21 | FE-21 Payment Deadlines, Invoices & Payment Document Management | 2 | 0 | 0 | 0 | 2 |
| 22 | FE-22 Partner Inspector Payout Reconciliation | 1 | 0 | 0 | 0 | 1 |
| 23 | FE-23 Evidence-Backed Refunds & Receivable Recovery | 1 | 0 | 0 | 0 | 1 |
| 24 | FE-24 Post-Remediation Re-inspection & Defect Verification | 2 | 0 | 0 | 0 | 2 |
| **Current Round 3 subtotal** |  | **77** | **0** | **0** | **3** | **80** |
| **Current Round 1 subtotal** |  | **52** | **0** | **9** | **19** | **80** |
| **Historical Round 1 subtotal** |  | **45** | **0** | **8** | **3** | **56** |
| **Historical Review 2 baseline (original eight-feature snapshot)** |  | **60** | **0** | **4** | **0** | **64** |
| **Historical implementation-specific pending** |  | **0** | **0** | **1** | **0** | **1** |
| **Round 3 executed cases** |  | **77** | **0** | **0** | **0** | **77** |
| **V29 Round 3 cases** |  | **2** | **0** | **0** | **0** | **2** |
| **Current inventory** |  |  |  |  |  | **80** |
