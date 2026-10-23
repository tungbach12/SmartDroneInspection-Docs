# FE-07: Team Maintenance, Cost Control and Completion Reporting — MF4

Report 3 §3.8 titles this feature "Team Maintenance, Cost Control and
Completion Reporting". The filename retains the earlier "maintenance / defect
resolution" wording; the filename is stable, the scope is Report 3's.

## Scope baseline

MF4 receives **published MF3 findings requiring repair**. It manages the
enterprise's internal repair team, approved scope, estimates, changes, actuals
and closeout. It is not a provider marketplace or payment/commission flow;
supplier quotes can be attached as cost evidence without creating a supplier
user role, bidding portal, accounting ledger or procurement integration.

### Team responsibilities (Report 3 §3.8.1)

| Responsibility | Login role | Named by | What this person does |
| --- | --- | --- | --- |
| Work-order owner / budget approver | `ORG_ADMIN` | — | Selects corrective scope; names team, lead, report author and accepting reviewer; approves baseline and changes; records closure authorization. |
| Repair team lead | `MAINTENANCE_ENGINEER` | ORG_ADMIN, exactly one per work order | Coordinates assessment, task allocation, method, estimate, resource readiness, consolidated completion and actuals. |
| Team member / task assignee | `MAINTENANCE_ENGINEER` | ORG_ADMIN selects team; lead allocates tasks | Accepts tasks; records own work, consumption and time; uploads before/during/after proof. |
| Accountable repair-report author | `MAINTENANCE_ENGINEER` | ORG_ADMIN, exactly one per work order | Collects the team's records, requests/verifies/edits the LLM completion report, submits it; remains the author even when the LLM drafted the text. |
| Independent accepting reviewer | `ORG_ADMIN` | — | Not on the executing team and not the report author. Checks scope, evidence and residual issues; accepts or returns. Cost reconciliation is a **separate recorded decision**. |
| Re-inspection verifier, if required | `INSPECTOR` | Assigned through a linked MF1 inspection | Records independent evidence; **cannot stand in for a repair engineer's work log**. |
| Automated assistant | `SYSTEM` / LLM | Authorized workflow | Validates references, computes totals, drafts narrative, publishes only after approval. |

Separation-of-duties rules that carry real risk:

- Final acceptance **cannot** be performed by the repair-team lead/report author
  or by the executing team.
- Budget approval and technical acceptance are **distinct actions**, even when
  the same qualified non-executing `ORG_ADMIN` performs both under company
  policy.
- If **no qualified independent reviewer exists, the work remains awaiting
  review**. The platform does not create a professional qualification.
- Replacing the lead or report author is done by `ORG_ADMIN` with a recorded
  reason and handover; **old logs retain their authors**.

## Current test coverage

Four cases cover the implemented MF4 lifecycle across Backend API, RAG advisor, Web console, and Mobile execution: tenant and
assignment scope, team/estimate/change approval, execution through
independent acceptance and reconciled closure, and RAG-assisted technical scope suggestions.

| Test Case ID | Test Case Description | Test Case Procedure | Expected Results | Pre-conditions | Round 1 | Test date | Tester | Round 2 | Test date | Tester | Round 3 | Test date | Tester | Note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| WF3-010 | A work order may only be opened for a published repair-required finding inside the caller's organization. | Read repair candidates as ORG_ADMIN; create a work order from one candidate; read it back; attempt the same identifier from another organization; attempt a second active work order for the same finding; attempt creation as MAINTENANCE_ENGINEER; re-read the candidate list. | The order is persisted as DRAFT with traceable source ids; a cross-organization read returns not-found and never reveals duplicate state; a duplicate active finding is rejected; non-admin creation is denied; the covered finding leaves the open-candidate list. | PostgreSQL 17/Testcontainers; published MF3 report version with a human-confirmed repair-required finding; two organizations; active users for each role. | Passed | 2026-10-11 | Claude Code (automated) | Pending |  |  | Pending |  |  | `MaintenanceApiIntegrationTest`: orgAdminCreatesAndReadsWorkOrderFromOwnOrganization, anotherOrganizationCannotReadWorkOrderEvenWhenItKnowsTheId, crossTenantDuplicateFindingDoesNotRevealExistingWorkOrder, duplicateActiveFindingCannotOpenSecondWorkOrder, maintenanceEngineerCannotOpenWorkOrder, repairCandidatesShowPublishedFindingsUntilAnActiveWorkOrderExists. |
| WF3-011 | Team designation, estimate approval and change control enforce role, independence and budget separation. | Assign lead, report author, independent reviewer and a member; attempt a team member who is the budget approver; prepare an estimate with and without a unit rate; submit and attempt approval by a different ORG_ADMIN; return the estimate as the designated approver; propose a change and attempt a decision by the wrong approver; approve with the designated approver; reject another change. | Member assignments persist and are readable by the team; the budget approver is rejected inside the executing team; the SYSTEM derives the estimate total and rejects an unpriced line; only the designated approver decides; a returned estimate puts the order back to rework; only an approved change enlarges the authorized amount. | Draft work order; same-organization lead, report author, reviewer, member and approver; credential absent or expired per scenario. | Passed | 2026-10-11 | Claude Code (automated) | Pending |  |  | Pending |  |  | `MaintenanceApiIntegrationTest`: orgAdminPersistsEveryRequestedTeamMember, orgAdminCannotAssignBudgetApproverIntoExecutingTeam, leadCreatesEstimateAndSystemCalculatesItsTotal, estimateRejectsMissingRateRatherThanTreatingItAsZero, unrelatedOrgAdminCannotApproveEstimate, designatedApproverCanReturnSubmittedEstimateForRework, teamEngineerCanRequestChangeAndOnlyBudgetApproverCanApproveIt, rejectedChangeDoesNotIncreaseAuthorizedBaseline, expiredCredentialBlocksTeamAssignment. |
| WF3-012 | Recorded execution, independent acceptance and reconciled closure follow the completion gates. | Release and start work; attempt completion before logs are verified; record, submit and lead-verify a work log; declare completion; create, verify and submit the completion report; attempt acceptance as an engineer; accept as the designated reviewer; reconcile actuals including a wrong-currency attempt; close; separately require rework and resume execution. | Completion is refused until every work log is verified; only the designated report author submits; the executing team cannot accept its own work; the reviewer records an append-only decision; the SYSTEM derives authorized amount, actual total and variance and rejects a currency mismatch; closure requires reconciliation first; a rework decision returns the order to execution. | Approved work order and estimate; assigned team, task and verified work log; designated report author and distinct accepting reviewer; PostgreSQL/Testcontainers. | Passed | 2026-10-11 | Claude Code (automated) | Pending |  |  | Pending |  |  | `MaintenanceApiIntegrationTest`: completesWorkOrderThroughIndependentAcceptanceAndCostReconciliation, reconciliationRejectsActualLineInDifferentCurrencyFromApprovedBaseline, leadCanResumeExecutionAfterReviewerRequiresRework, nonTeamEngineerCannotRecordWorkLog. Backend `./mvnw.cmd verify`: 457 tests, 0 failures/errors, Modulith and JaCoCo gates passed. |
| WF3-013 | RAG-assisted repair scope and acceptance criteria advisor queries engineering standards and falls back deterministically. | Post to `/api/v1/maintenance/suggest-scope` with finding details; verify retrieved standard codes (TCVN, ISO, EN), structured scope, quantifiable acceptance criteria, and suggested tasks; simulate disabled/unreachable AI and verify deterministic fallback without failure; invoke from `RepairCandidatePanel.tsx` UI and verify form field population. | Scope suggestion returns actionable repair methodology, measurable criteria (UPV >= 90%, adhesion >= 1.5 MPa), and sequential tasks; fallback activates smoothly without error when AI is offline; UI populates fields and renders standard badges. | Published finding on a published report; PostgreSQL 17 with pgvector extension and `repair_knowledge_chunks` seeded with 5 standard sets; authenticated `ORG_ADMIN`. | Passed | 2026-10-23 | Như / Claude Code | Pending |  |  | Pending |  |  | `MaintenanceScopeAdvisorServiceTest`, `DeterministicScopeFallbackTest`, `MaintenanceScopeAdvisorClientTest`, `RepairCandidatePanel.tsx`. Backend unit tests and Modulith boundary verified. |

### Scope boundary for this round

These four cases cover full-stack MF4 delivery across Backend, Web, Mobile, and RAG:

- Backend event-driven re-inspection dispatch (`ReinspectionRequestedEvent`), completion report PDF rendering (`MaintenanceReportRenderer`), and milestone notifications (`MaintenanceNotificationListener`) are implemented and verified.
- Web console (`MaintenancePage.tsx`, `WorkOrderDetailPanel.tsx`, `RepairCandidatePanel.tsx`) and Mobile tasks app (`tasks_page.dart`, `work_order_detail_page.dart`) are implemented and tested.
- Six client-server workflow defects (cost reconciliation task reference, lead work log verification button, transition state guards, budget approver validation, closed work order immutability, PDF download link) have been remediated.
- RAG scope advisor is verified with pgvector HNSW indexing and deterministic rule-based fallback.
- MF4-04 credential presence permits assignment when no credential record exists and blocks a present non-active or expired record per the approved interim rule. Applicable skills remain unmodelled.

`WF3-006` verifies MF3 publication handing repair-required finding IDs to the
maintenance boundary; it remains an MF3 publication test owned by FE-06.

The former `WF4-001` to `WF4-005` IDs stay reserved and are never reused. New
MF4 cases continue at `WF3-010`.

## Feature sheet summary

Values for the `Feature 7` summary block (`A2:E8` in the workbook).
The template reads these back by formula, so an export needs them
recorded here.

| Cell | Label | Value |
| --- | --- | --- |
| `B2` | Feature | Team Maintenance, Cost Control and Completion Reporting - MF4 |
| `B3` | Test requirement | Verifies repair-team assignment, cost approval and reconciliation, independent completion acceptance, mobile execution, and RAG technical scope suggestions. |
