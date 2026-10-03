# FE-07: Maintenance and Defect Resolution

## Implemented v1 baseline and proposed MF5 target

The existing WF4 cases below describe the five-role maintenance/order/billing baseline and remain Pending where unexecuted. They do not prove a licensed payment-partner arrangement, uniform Provider commission, contractual warranty retention or the proposed Provider-specific workforce scope. The MF5 redesign is represented by new Pending target cases, not by silently changing existing results.

## Current acceptance cases

WF4-001 through WF4-003 map to FE-07.

| Test Case ID | Test Case Description | Test Case Procedure | Expected Results | Pre-conditions | Round 1 | Test date | Tester | Round 2 | Test date | Tester | Round 3 | Test date | Tester | Note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| WF4-001 | Client creates a maintenance ticket from an accepted finding. | Sign in as Client; open a released report; choose an accepted finding; create a ticket; list tickets. | Ticket is linked to the finding and client organization; another organization cannot see it. | Released report and accepted finding exist. | Pending |  |  | Pending |  |  | Pending |  |  |  |
| WF4-002 | Maintenance Engineer updates only assigned work. | Assign an assessment/execution task; sign in as the engineer; update status and notes; attempt an unassigned ticket. | Assigned work can be updated; unassigned or cross-organization work is denied. | Ticket is actionable; engineer is active and assigned. | Pending |  |  | Pending |  |  | Pending |  |  |  |
| WF4-003 | Approval, rework/reinspection, and post-service billing status are recorded. | Complete maintenance; submit for client approval; approve or request rework; if approved, inspect the second billing milestone and invoice/payment status. | Approval or rework state is auditable; reinspection is a new controlled step; payment status is recorded without requiring an online gateway. | Maintenance result and invoice record exist. | Pending |  |  | Pending |  |  | Pending |  |  |  |

## Coverage boundary

The current case procedures cover ticket creation, assigned work, Client decision, rework/reinspection state, and billing status. They do not explicitly list before/after evidence assertions, Service Manager release, or Client close/handoff as separate checks.

## Proposed MF5 target cases (not executed)

| Test Case ID | Test Case Description | Test Case Procedure | Expected Results | Pre-conditions | Round 1 | Test date | Tester | Round 2 | Test date | Tester | Round 3 | Test date | Tester | Note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| WF4-004 | Maintenance Provider is scoped and order-snapshotted retention is released without double commission. | Create a ticket from accepted findings; invite two maintenance Providers; publish retention/warranty policy P1; approve one work order with P1; submit before/after evidence; publish P2; accept completion and release retention under the partner fixture. Attempt access by the losing Provider. | Only winning Provider/assigned engineer can work; the order retains P1 after P2 is published; partner settles eligible amounts net of one `C = r × B`; later release of `H` adds no commission; tax records remain separate. | Accepted report, two Providers, qualified engineer, versioned policy fixtures and authorized partner fixture exist. | Pending |  |  | Pending |  |  | Pending |  |  | Target MF5; no implementation evidence. |
| WF4-005 | Rework, change order and warranty complaint preserve authorized money and scope. | Submit a scope increase before approval; attempt extra work; approve the change and provide additional funding only if supported/required; reject defective completion; file a warranty complaint and attempt retention release before/after partner confirms permitted hold handling. | Extra work waits for approval and accepted funding terms; defective included work can be returned; disputed retention is not released unless the accepted terms and partner product permit it; actual service-price refunds reverse corresponding commission only. | Approved maintenance order, before/after evidence, accepted policy snapshot and partner capability fixtures exist. | Pending |  |  | Pending |  |  | Pending |  |  | Target only; no partner or complaint workflow executed. |
