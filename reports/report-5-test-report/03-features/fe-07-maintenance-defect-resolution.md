# FE-07: Maintenance and Defect Resolution

## Scope baseline

MF4 starts from a published MF3 report containing a human-confirmed,
repair-required finding. The intended target remains the full maintenance flow
in Report 3 §3.8. The backend slice now exposes a repair-candidate read port,
work-order lifecycle API, internal team/task/estimate and change control,
work-log/report/acceptance records, cost reconciliation and closeout.

This is **backend API verification**, not full product acceptance: no web/mobile
maintenance UI or notification delivery is included, skills are not modelled,
and a re-inspection decision does not dispatch the MF1 inspection.

## Current cases

| Test Case ID | Test Case Description | Test Case Procedure | Expected Results | Pre-conditions | Round 1 | Test date | Tester | Round 2 | Test date | Tester | Round 3 | Test date | Tester | Note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| WF3-010 | ORG_ADMIN creates a work order only for a published repair-required finding in their organization. | Read `/api/v1/maintenance/repair-candidates`; create a work order from the candidate; read it back; try to read it from another organization, open a second active order for the same finding, and create as MAINTENANCE_ENGINEER; then create an order and verify it disappears from active candidates. | Valid same-organization order is persisted as DRAFT and source IDs are traceable; cross-tenant read returns 404; duplicate active finding returns 409; non-ORG_ADMIN creation is denied; active candidate list excludes its finding. | Testcontainers PostgreSQL; published report/version and human-confirmed repair-required finding; two organizations; active ORG_ADMIN and MAINTENANCE_ENGINEER. | Passed | 2026-10-10 | Claude Code (automated) | Pending |  |  | Pending |  |  | `MaintenanceApiIntegrationTest.orgAdminCreatesAndReadsWorkOrderFromOwnOrganization`, `anotherOrganizationCannotReadWorkOrderEvenWhenItKnowsTheId`, `duplicateActiveFindingCannotOpenSecondWorkOrder`, `maintenanceEngineerCannotOpenWorkOrder`, `repairCandidatesShowPublishedFindingsUntilAnActiveWorkOrderExists`. |
| WF3-011 | ORG_ADMIN assigns a same-organization team with independent reviewer; the lead plans priced work and only the designated budget approver can decide. | Assign lead/report author/reviewer; test expired credential; test absent credential under the recorded interim rule; try reviewer who is also the lead; add task; create an estimate with priced line and inspect SYSTEM total; submit and try approval by a different ORG_ADMIN; return estimate by the designated approver; verify missing-rate rejection; propose a change, try decision by the wrong ORG_ADMIN, approve with the designated approver, then reject another change and inspect its status. | Reviewer must be an active same-organization ORG_ADMIN outside the team; present expired credential blocks assignment while no record is allowed; task can only be assigned to active team member; server computes amount and baseline; missing price is rejected; only designated approver decides; returned estimate re-enters REWORK_REQUIRED; only approved changes affect authorized scope/budget. | WF3-010 work order; two ORG_ADMIN users; MAINTENANCE_ENGINEER team fixtures; no credentials or an expired ACTIVE credential; PostgreSQL/Testcontainers. | Passed | 2026-10-10 | Claude Code (automated) | Pending |  |  | Pending |  |  | `adminAssignsIndependentTeamAndEngineerReadsAssignments`, `teamCannotIncludeReviewerWhoIsAlsoTheLead`, `expiredCredentialBlocksTeamAssignment`, `unrecordedCredentialDoesNotBlockAssignmentPerApprovedInterimRule`, `leadCreatesEstimateAndSystemCalculatesItsTotal`, `estimateRejectsMissingRateRatherThanTreatingItAsZero`, `unrelatedOrgAdminCannotApproveEstimate`, `designatedApproverCanReturnSubmittedEstimateForRework`, `teamEngineerCanRequestChangeAndOnlyBudgetApproverCanApproveIt`, `rejectedChangeDoesNotIncreaseAuthorizedBaseline`. Credentials are interim/conditional; skills are not modelled. |
| WF3-012 | Assigned team records and verifies work; the designated report author submits completion; independent reviewer accepts; authorized reviewer reconciles costs and closes. | Approve/release/start work; record a work log, attempt completion before all logs are verified, submit and verify as lead; declare completion; report author creates/verifies/submits report; try acceptance as MAINTENANCE_ENGINEER; accept as designated reviewer; reconcile actual lines including a wrong-currency attempt; compare approved baseline, actual, variance and percentage; close. Separately return for rework and resume execution. | Team completion is blocked until all work logs are verified; report author is the submitting author; team cannot accept its own work; acceptance and reconciliation are separate; wrong currency is rejected; SYSTEM computes variance; closure requires acceptance and reconciliation; reviewer rework returns to executable work. | WF3-011 work order with approved estimate, assigned team and task; submitted/verified work log; completion report; independent reviewer; PostgreSQL/Testcontainers. | Passed | 2026-10-10 | Claude Code (automated) | Pending |  |  | Pending |  |  | `completesWorkOrderThroughIndependentAcceptanceAndCostReconciliation`, `leadCanResumeExecutionAfterReviewerRequiresRework`, `reconciliationRejectsActualLineInDifferentCurrencyFromApprovedBaseline`; domain tests `MaintenanceWorkLogTest`, `MaintenanceWorkOrderLifecycleTest`. MF4 re-inspection only records its decision/resume state; linked MF1 dispatch is not tested or implemented. |

## Coverage boundary and outstanding work

- The former `WF4-001`–`WF4-005` cases were removed on 2026-10-09. Those IDs
  remain reserved and are never reused; the current cases continue at `WF3-010`
  because `WF3-007`/`WF3-008` are also reserved.
- `WF3-006` remains an MF3 publication test owned by FE-06. It verifies the
  published-finding handoff but does not substitute for the maintenance cases
  above.
- MF4-04 deviation: no credential record is allowed because no credential
  issuance/verification workflow exists; a recorded credential that is not
  ACTIVE or is expired blocks assignment. Applicable skills have no model.
- MF4-18 `REINSPECTION_REQUIRED` can be recorded, but creation/dispatch of the
  linked MF1 inspection is not implemented. Notifications, S3 evidence upload
  and completion-report object rendering are also not verified here.
- Round 2 and Round 3 are `Pending`; no execution is claimed for those rounds.
