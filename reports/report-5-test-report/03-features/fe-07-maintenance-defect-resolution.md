# FE-07: Maintenance and Defect Resolution

## Scope baseline

WF4 links approved defects to separately confirmed maintenance orders and tickets. The platform supports Engineer assignment after the maintenance order and post-service payment terms are approved. The Engineer uploads before/after evidence and marks the work resolved; the Service Manager requests rework or releases the result, and the Client closes it or requests a new re-inspection through WF2. Client acceptance is the maintenance billing milestone.

## Current acceptance cases

WF4-001 through WF4-003 map to FE-07.

| Test Case ID | Test Case Description | Test Case Procedure | Expected Results | Pre-conditions | Round 1 | Test date | Tester | Round 2 | Test date | Tester | Round 3 | Test date | Tester | Note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| WF4-001 | Client creates a maintenance ticket from an accepted finding. | Sign in as Client; open a released report; choose an accepted finding; create a ticket; list tickets. | Ticket is linked to the finding and client organization; another organization cannot see it. | Released report and accepted finding exist. | Pending |  |  | Pending |  |  | Pending |  |  |  |
| WF4-002 | Maintenance Engineer updates only assigned work. | Assign an assessment/execution task; sign in as the engineer; update status and notes; attempt an unassigned ticket. | Assigned work can be updated; unassigned or cross-organization work is denied. | Ticket is actionable; engineer is active and assigned. | Pending |  |  | Pending |  |  | Pending |  |  |  |
| WF4-003 | Approval, rework/reinspection, and post-service billing status are recorded. | Complete maintenance; submit for client approval; approve or request rework; if approved, inspect the second billing milestone and invoice/payment status. | Approval or rework state is auditable; reinspection is a new controlled step; payment status is recorded without requiring an online gateway. | Maintenance result and invoice record exist. | Pending |  |  | Pending |  |  | Pending |  |  |  |

## Coverage boundary

The current case procedures cover ticket creation, assigned work, Client decision, rework/reinspection state, and billing status. They do not explicitly list before/after evidence assertions, Service Manager release, or Client close/handoff as separate checks.
