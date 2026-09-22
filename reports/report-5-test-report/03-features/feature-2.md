# Feature 2 sheet — FE-04/FE-05/FE-06 inspection delivery and FE-07 maintenance

This file mirrors the fixed `Feature 2` workbook sheet. It is not the SRS
feature `FE-02`; the template groups WF3 inspection/report work and WF4
maintenance work on this sheet. FE codes identify the product capabilities,
while WF codes remain the test-case IDs.

| Template field | Value |
| --- | --- |
| Feature | Feature 2 sheet — FE-04/FE-05/FE-06 WF3 delivery and FE-07 close-out |
| Test requirement | FE-04 assigned execution/evidence, FE-05 candidate verification, FE-06 report approval, and FE-07 maintenance work, rework, and post-service billing status |
| Number of TCs | 7 |
| Case mapping | WF3-001–002 → FE-04; WF3-003 → FE-05; WF3-004 → FE-06; WF4-001–003 → FE-07 |

## Function D — FE-04 execution/evidence, FE-05 findings, and FE-06 report approval (WF3)

| Test Case ID | Test Case Description | Test Case Procedure | Expected Results | Pre-conditions | Round 1 | Test date | Tester | Round 2 | Test date | Tester | Round 3 | Test date | Tester | Note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| WF3-001 | Assigned Inspector starts and completes the inspection checklist. | Sign in as the assigned Inspector; open the task; start the inspection; complete required checklist items; save progress. | Only the assigned Inspector can update the task; required items and timestamps are retained. | Confirmed order and assignment exist; checklist is published. | Passed | 2026-09-22 | Codex (automated) | Pending |  |  | Pending |  |  | Backend `InspectionFixtureTest` and `InspectionWorkflowTest` passed with assignment scope, five start retries, valid response persistence, blank/foreign-item rejection; mobile inspection contract test passed. Full backend `mvnw verify` passed 100 tests with coverage and Modulith checks; mobile format, analyze, and test passed. |
| WF3-002 | Inspector uploads authorized evidence with source traceability. | From the assigned inspection, upload valid evidence; link it to the inspection/checklist context; save and retry the upload. | Evidence metadata, ownership, checksum, and source traceability are retained; invalid, duplicate, or unassigned uploads are rejected. | Inspection is started; evidence type and file constraints are available. | Pending |  |  | Pending |  |  | Pending |  |  | MinIO Compose liveness was checked as infrastructure, but evidence validation, checksum, retry safety, and storage behavior remain pending under FE-04 task `T025/SCRUM-85`. |
| WF3-003 | Inspector verifies AI candidates or adds a manual finding. | Submit eligible evidence for analysis; review the candidate as the assigned Inspector; confirm, modify, reject, or add a manual finding; inspect report data. | Candidate status and reviewer decision are auditable; only confirmed, modified, or manual findings enter official report content; rejected/unverified candidates remain non-official. | Eligible evidence exists; AI integration is available or manual fallback is enabled. | Pending |  |  | Pending |  |  | Pending |  |  |  |
| WF3-004 | Report author cannot peer-review their own report. | Create a draft report as Inspector A; attempt review as Inspector A; retry as an authorized different reviewer; release. | Self-review is denied; a different authorized reviewer can approve; released version is immutable. | Draft report exists; author and reviewer accounts are distinct and active. | Pending |  |  | Pending |  |  | Pending |  |  |  |

## Function E — FE-07 maintenance assessment and execution (WF4)

| Test Case ID | Test Case Description | Test Case Procedure | Expected Results | Pre-conditions | Round 1 | Test date | Tester | Round 2 | Test date | Tester | Round 3 | Test date | Tester | Note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| WF4-001 | Client creates a maintenance ticket from an accepted finding. | Sign in as Client; open a released report; choose an accepted finding; create a ticket; list tickets. | Ticket is linked to the finding and client organization; another organization cannot see it. | Released report and accepted finding exist. | Pending |  |  | Pending |  |  | Pending |  |  |  |
| WF4-002 | Maintenance Engineer updates only assigned work. | Assign an assessment/execution task; sign in as the engineer; update status and notes; attempt an unassigned ticket. | Assigned work can be updated; unassigned or cross-organization work is denied. | Ticket is actionable; engineer is active and assigned. | Pending |  |  | Pending |  |  | Pending |  |  |  |
| WF4-003 | Approval, rework/reinspection, and post-service billing status are recorded. | Complete maintenance; submit for client approval; approve or request rework; if approved, inspect the second billing milestone and invoice/payment status. | Approval or rework state is auditable; reinspection is a new controlled step; payment status is recorded without requiring an online gateway. | Maintenance result and invoice record exist. | Pending |  |  | Pending |  |  | Pending |  |  |  |
