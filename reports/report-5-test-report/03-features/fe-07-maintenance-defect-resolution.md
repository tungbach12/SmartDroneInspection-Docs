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

No workbook test case is mapped to FE-07 in this report.

The former `WF4-001`–`WF4-005` cases were removed on 2026-10-09 because they
described the retired five-role baseline or unimplemented Enterprise SaaS MF4
target behavior. The `maintenance` module has persistence foundations but no
implemented MF4 use-case/API workflow, so there is no runtime to execute and no
MF4 test result to record.

`WF3-006` verifies that publication hands repair-required finding IDs to the
maintenance boundary. That is an MF3 publication test owned by FE-06; it does
**not** verify maintenance ticket creation, execution, cost control, or
acceptance.

This is an explicit coverage gap. The removed `WF4-*` IDs stay reserved and are
never reused.

### MF4-01 – MF4-20 Work Order Lifecycle — supporting verification (executed 2026-10-20)

- Preconditions: Backend `feat/mf1-backend-org-admin-resources` and Frontend `feat/mf1-org-admin-resources-hieu`; PostgreSQL 17/Testcontainers; an organization with a published repair-required finding, an ORG_ADMIN and a MAINTENANCE_ENGINEER.
- Procedure: Run Backend `MaintenanceApiIntegrationTest` (25 tests) and Frontend `MaintenancePage.test.tsx` (6 tests). Verify the repair-candidate triage list that carries the MF3-13 handoff; work order creation with priority, due date, corrective scope and acceptance criteria (MF4-01/02); team designation of exactly one lead, one report author and one independent accepting reviewer (MF4-03/04); task creation by the lead (MF4-05); estimate versions with system-computed totals (MF4-06/07) and their approval by the budget approver (MF4-08); the execution transitions release, start and declare-complete (MF4-09/10/14); work logs recording hours, as-left condition and test readings (MF4-11); change requests with approve, reject and return decisions (MF4-12/13); completion report drafting, verification and submission (MF4-15/16/17); independent acceptance with accept, return for rework and request re-inspection (MF4-18); cost reconciliation with the computed variance (MF4-19); and closure (MF4-20).
- Expected result: Each transition is a named action rather than a generic state change; the role decides which actions are offered while the backend stays the enforcement boundary; the accepting reviewer may not be drawn from the executing team; the lead and report author may be the same engineer; actual cost lines never overwrite an estimate line and the variance is computed by the platform from the approved baseline, the approved change deltas and the reconciled actuals; a work order closes only after independent acceptance and cost reconciliation.
- Round 1: Passed 2026-10-20; tester: Claude Code (automated).
- Round 2: Passed 2026-10-24; tester: Như / Claude Code (automated & live walkthrough).
- Evidence: Backend `MaintenanceApiIntegrationTest` passed 26/26 tests (including plain-text `jsonb` normalization across all 8 maintenance entities, work-log interval derivation, and `REINSPECTION_REQUIRED` execution resumption) alongside `MaintenanceScopeAdvisorServiceTest` (3/3), `DeterministicScopeFallbackTest` (5/5), `MaintenanceScopeAdvisorClientTest` (2/2), `MaintenanceReportRendererTest` (2/2), `MaintenanceNotificationListenerTest` (5/5), and `ModulithArchitectureTest` (3/3). Frontend `MaintenancePage.test.tsx` passed 8/8 tests (`npm run lint` and `npm run build` clean) and a 16-step live browser/API walkthrough verified RAG scope suggestion, team assignment, task status progression, estimate approval, work log verification, change order approval, completion report PDF download, independent acceptance, cost reconciliation, and work order closure. Mobile `maintenance_repository_test.dart` passed 8/8 unit tests.
- Scope note: MF4-21 follow-up and warranty conditions have no backend endpoint and are not claimed here. The cost register is an internal record; it is not a statutory tax invoice and no payment is captured.

## Feature sheet summary

Values for the `Feature 7` summary block (`A2:E8` in the workbook).
The template reads these back by formula, so an export needs them
recorded here.

| Cell | Label | Value |
| --- | --- | --- |
| `B2` | Feature | Team Maintenance, Cost Control and Completion Reporting — MF4 |
| `B3` | Test requirement | Would verify repair team assignment, cost reconciliation and completion acceptance. MF4 is unimplemented, so no case is recorded. |
