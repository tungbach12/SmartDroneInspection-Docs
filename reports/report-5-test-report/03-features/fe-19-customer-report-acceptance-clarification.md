# FE-19: Customer Report Acceptance & Clarification Workflow

Synchronized with Report 3 SRS v2.2 and Report 4 SDD v2.4; upstream of the `(FE-19)` test sheet in `Report5_Test Report.xlsx`.

## Feature sheet summary

Values for the `Feature 19` summary block (`A2:E8` in the workbook).

| Cell | Label | Value |
| --- | --- | --- |
| `B2` | Feature | Customer Report Acceptance & Clarification Workflow |
| `B3` | Test requirement | Verifies Customer review of published inspection reports, formal report acceptance (`ACCEPTED`) triggering commercial invoicing readiness, clarification request paths, and live Customer acceptance walkthroughs. |

## Test case execution records

| Test Case ID | Test Case Description | Test Case Procedure | Expected Results | Pre-conditions | Round 1 | Test date | Tester | Round 2 | Test date | Tester | Round 3 | Test date | Tester | Note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| WF3-012 | Customer reviews published report, downloads PDF & receipt, settles fee, and initiates re-inspection. | 1. Sign in as Customer and open a Published inspection on `/client/inspections`.<br>2. Verify Report stage shows published reference, Accepted status, Download Report, findings map, and video captures.<br>3. Open Service Payment stage and verify paid invoice breakdown, Download Receipt (PDF), Rate Inspector, and Schedule Re-inspection. | Published report and settled VNPay/Sepay invoice details, PDF actions, and re-inspection entry point render cleanly with zero maintenance work-order UI. | Customer test account with published & settled inspection records. | Pending |  |  | Pending |  |  | Passed | 2026-11-27 | Trương Thái Như | Verified via live Web walkthrough (agent-browser) & payment integration tests. |
| WF3-035 | Customer clarification request, pre-acceptance payment lock, and unpublished draft isolation. | 1. Probe an unaccepted or unpublished report as Customer and attempt to generate a Sepay payment link before acceptance.<br>2. Request clarification as Customer and verify a Manager cannot call Customer clarification endpoints. | Customers see only Published versions and cannot create payment links before accepting the report; clarification requests persist for the report while Manager callers are denied. | Submitted and published report versions with Manager and Customer accounts. | N/A |  |  | N/A |  |  | Passed | 2026-11-27 | Trương Thái Như | Verified via report reviewer scope & Sepay integration tests. |
