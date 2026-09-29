# FE-03: Inspection Request and Work Assignment

## Scope baseline

WF2 unifies PERIODIC and AD_HOC requests. Client request details and Service Manager review lead to a versioned quotation and service-order confirmation. The Client approves post-service payment terms before assignment; no upfront payment or online payment gateway is required.

## Current acceptance cases

These four cases map to FE-03 and WF2. WF2-001 and WF2-002 were in workbook Function B; WF2-003 and WF2-004 were in Function C.

| Test Case ID | Test Case Description | Test Case Procedure | Expected Results | Pre-conditions | Round 1 | Test date | Tester | Round 2 | Test date | Tester | Round 3 | Test date | Tester | Note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| WF2-001 | Client creates an ad-hoc inspection request. | Sign in as Client; select an owned asset; enter scope, location, and preferred timing; submit. | Request is accepted with an auditable creator and organization; invalid scope is rejected. | Owned asset exists; client is active. | Pending |  |  | Pending |  |  | Pending |  |  |  |
| WF2-002 | Service Manager prepares and sends a quotation. | Sign in as Service Manager; open the request; add price, scope, and validity; save a version; send it. | A versioned quotation is stored and visible to the correct client; prior versions remain traceable. | Request is actionable; manager is active. | Pending |  |  | Pending |  |  | Pending |  |  |  |
| WF2-003 | Client approves a quotation and confirms the service order. | Sign in as Client; review the latest quotation; approve it; open the order and billing status. | The approved quotation becomes the confirmed order; the first service billing milestone is recorded. | Quotation is in an approvable state; client owns the request. | Pending |  |  | Pending |  |  | Pending |  |  |  |
| WF2-004 | Service Manager assigns an Inspector with assignment scope. | Sign in as Service Manager; assign an active Inspector; open the task as the Inspector; attempt an unrelated task. | Assigned Inspector can access only the assigned task; unassigned or conflicting access is denied. | Confirmed order exists; candidate Inspector is active. | Pending |  |  | Pending |  |  | Pending |  |  |  |

## Coverage boundary

WF1-004 verifies periodic request generation, while WF2-001 verifies ad-hoc request creation. The current cases do not explicitly record one end-to-end periodic-request-to-quotation path.
