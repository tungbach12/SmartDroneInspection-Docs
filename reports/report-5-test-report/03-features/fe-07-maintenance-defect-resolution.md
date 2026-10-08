# FE-07: Maintenance and Defect Resolution

## Implemented v1 baseline and Enterprise SaaS target

**Historical v1 scope record:** The earlier WF4 cases described the five-role maintenance/order/billing baseline, with statuses recorded at the time of execution. Preserve those results as historical evidence only; they do not prove Enterprise SaaS MF4 behavior on the reset branch. Target MF4 requires internal repair team, designated lead/report author, approved estimate/change/actual control, author-verified LLM completion report, independent ORG_ADMIN acceptance and cost reconciliation; these are represented by separate Pending target cases.

## Historical v1 acceptance cases (retired from the Enterprise SaaS target)

WF4-001 through WF4-003 map to FE-07 in the earlier five-role baseline. Preserve every recorded status and note as historical evidence; those cases do not establish current reset-branch MF4 runtime behavior. The target MF4 criteria are the separate Pending cases below.

| Test Case ID | Test Case Description | Test Case Procedure | Expected Results | Pre-conditions | Round 1 | Test date | Tester | Round 2 | Test date | Tester | Round 3 | Test date | Tester | Note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| WF4-001 | Client creates a maintenance ticket from an accepted finding. | Sign in as Client; open a released report; choose an accepted finding; create a ticket; list tickets. | Ticket is linked to the finding and client organization; another organization cannot see it. | Released report and accepted finding exist. | Pending |  |  | Pending |  |  | Pending |  |  |  |
| WF4-002 | Maintenance Engineer updates only assigned work. | Assign an assessment/execution task; sign in as the engineer; update status and notes; attempt an unassigned ticket. | Assigned work can be updated; unassigned or cross-organization work is denied. | Ticket is actionable; engineer is active and assigned. | Pending |  |  | Pending |  |  | Pending |  |  |  |
| WF4-003 | Approval, rework/reinspection, and post-service billing status are recorded. | Complete maintenance; submit for client approval; approve or request rework; if approved, inspect the second billing milestone and invoice/payment status. | Approval or rework state is auditable; reinspection is a new controlled step; payment status is recorded without requiring an online gateway. | Maintenance result and invoice record exist. | Pending |  |  | Pending |  |  | Pending |  |  |  |

## Coverage boundary

Historical v1 case procedures covered ticket creation, assigned work, Client decision, rework/reinspection state, and billing status. They do not separately assert before/after evidence, Service Manager release, or Client close/handoff; these historical cases do not verify current MF4 target behavior.

## Enterprise SaaS target cases for MF4 (not executed)

| Test Case ID | Test Case Description | Test Case Procedure | Expected Results | Pre-conditions | Round 1 | Test date | Tester | Round 2 | Test date | Tester | Round 3 | Test date | Tester | Note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| WF4-004 | ORG_ADMIN triages a published MF3 report into an MF4 work order: scope, acceptance criteria, team, lead, report author and independent accepting reviewer. | Publish an MF3 report with confirmed repair-required findings; ORG_ADMIN creates/triages the work order and names one lead, one report author and an independent accepting ORG_ADMIN; attempt creation with a duplicate active scope or with the accepting reviewer inside the executing team. | The work order links the published report version and finding IDs; exactly one lead and one report author are designated; the accepting reviewer is qualified, independent and not the author; duplicate active scope requires an explicit reason; a no-repair outcome creates no empty work order. | Published MF3 report with repair-required findings and workforce fixtures exist. | Pending |  |  | Pending |  |  | Pending |  |  | Target MF4; no implementation evidence. |
| WF4-005 | Estimate baseline, approved change orders, actuals and before/after evidence reconcile before completion acceptance. | Team lead prepares an itemized estimate; ORG_ADMIN approves the scope/budget baseline; a scope increase is submitted as a change order and approved/rejected; members record actuals, work logs and paired before/after evidence; a missing or duplicate actual blocks final reconciliation. | The initial baseline `E0` is immutable; revised authorized amount `B = E0 + sum(approved changes)`; actuals `A` reconcile with variance `V = A − B`; unauthorized extra work is blocked; unresolved missing/duplicate/unapproved costs block closure. | Approved MF4 work order, workforce assignments and cost-line fixtures exist. | Pending |  |  | Pending |  |  | Pending |  |  | Target MF4; no change-order or warranty workflow executed. |
