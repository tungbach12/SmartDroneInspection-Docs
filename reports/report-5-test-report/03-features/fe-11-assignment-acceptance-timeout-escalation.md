# FE-11: Assignment Acceptance Timeout & Escalation Handling

Synchronized with Report 3 SRS v2.2 and Report 4 SDD v2.4; upstream of the `(FE-11)` test sheet in `Report5_Test Report.xlsx`.

## Feature sheet summary

Values for the `Feature 11` summary block (`A2:E8` in the workbook).

| Cell | Label | Value |
| --- | --- | --- |
| `B2` | Feature | Assignment Acceptance Timeout & Escalation Handling |
| `B3` | Test requirement | Verifies Admin-configurable Step 4 assignment acceptance timeout (`platform_operations_settings`, default 24h), automated expiry monitoring (`InspectionAssignmentTimeoutMonitor`), assignment revocation to `PENDING_ASSIGNMENT`, and Manager timeout alert notification. |

## Test case execution records

| Test Case ID | Test Case Description | Test Case Procedure | Expected Results | Pre-conditions | Round 1 | Test date | Tester | Round 2 | Test date | Tester | Round 3 | Test date | Tester | Note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| WF2-021 | Pending Step 4 assignment enforces Admin-configurable acceptance timeout, reverts expired assignment to `PENDING_ASSIGNMENT`, and escalates alert to the owning Manager. | 1. Configure Step 4 acceptance timeout via `ADMIN` `/admin/operations-settings` (`platform_operations_settings`).<br>2. Assign Partner Inspector and Drone without accepting before `expiresAt`.<br>3. Run `InspectionAssignmentTimeoutMonitor` sweep and inspect occurrence state and Manager notification. | Expired unaccepted assignment is cancelled cleanly, occurrence returns to `PENDING_ASSIGNMENT` for re-dispatch, and owning `MANAGER` receives an escalation notification deep-linking to `/manager/contracts?requestId=...`. | PostgreSQL 17 with `platform_operations_settings`, `ADMIN`, `MANAGER`, and `INSPECTOR` fixtures. | N/A |  |  | Pending |  |  | Passed | 2026-11-26 | Phùng Trung Quốc | [Target: FE-11 Standalone Escalation Case] [Mode: Unexecuted standalone case (timeout & monitor previously checked as focused evidence under WF2-001; standalone FE-11 workbook execution pending)] [Owner: Phùng Trung Quốc] [Round 3 (2026-11-26): Passed — backed by `InspectionAssignmentTimeoutMonitorTest` (2/2) & `InspectionRecoveryFlowIntegrationTest` in the Nov 26 regression run.] |
| WF2-032 | Withdraw an accepted assignment before field work | As the assigned Inspector, get workflow-state for the scheduled, accepted assignment. Post a non-blank reason to /inspections/{id}/decline. | Eligibility is true before withdrawal. The operation succeeds and the scheduled occurrence requires reassignment. | Scheduled, accepted inspection with no started session for the current assignment. | N/A |  |  | N/A |  |  | Passed | 2026-11-26 | Phùng Trung Quốc | InspectionRecoveryFlowIntegrationTest.managerCancellationClosesWithdrawnAssignmentWithoutErasingReasons (withdrawal phase). FieldSessionPage tests cover the confirmation UI. |
