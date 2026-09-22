# Week 4 Validation Runbook

This is the acceptance run to execute **after** the Jira tasks are implemented. It is not a
claim that the current backend already supports these routes.

## Prerequisites

- PostgreSQL and MinIO are reachable through the backend local Compose setup.
- Backend migrations V1–V9 and the new forward invoice migration apply cleanly to an empty
  database. If a configured YOLO service is available, run its smoke check; otherwise use the
  manual-finding path and record AI integration as blocked.
- Create five separate role accounts: Admin, Client, Service Manager, Inspector author, and
  Maintenance Engineer. Create a **second Inspector** for peer review and a second organization
  for negative-scope checks. No default password is placed in fixtures or this document.
- A deterministic test dataset has an active category, checklist, and a due schedule. Fixtures
  may be created through test builders or authorized API calls.

## Repository checks

Run and record the exact result in each flow's Jira closeout task and PR:

```powershell
cd backend
.\mvnw.cmd verify

cd ..\frontend
npm run lint
npm run build

cd ..\mobile
dart format --set-exit-if-changed .
flutter analyze
flutter test

cd ..\docs
git diff --check
```

Run the Hugo build only when Hugo and the configured theme are available. A missing Docker
environment blocks container-backed tests; report it as blocked rather than passed.

## Independent flow checks

| Flow | Start fixture | Actions | Expected output |
| --- | --- | --- | --- |
| WF1 | Client + active catalog | Create asset/document and schedule; trigger same due cycle twice; pause asset/schedule. | One scoped periodic request and no duplicate. |
| WF2 | Authorized asset/request | Submit request; review; quote; revise once; approve; confirm; assign; reject with reason; reassign and accept. | Confirmed order and accepted assignment; previous versions remain. |
| WF3 | Accepted Inspector assignment | Start inspection; complete checklist; upload evidence; verify an AI candidate or add manual finding; draft; submit; peer review by another Inspector; release; Client accept. | Accepted immutable report with only verified findings. |
| WF4 | Accepted report with verified finding | Create ticket; assign/complete assessment; approve quote/order; execute; submit before/after evidence; release; Client accept. | Closed ticket and maintenance invoice status. |

## Cross-flow demonstration

1. Client creates an asset and schedule. Due-cycle processing creates one WF2 request.
2. Service Manager quotes the request; Client approves the post-service terms; Inspector accepts
   the assignment. No upfront payment action is required.
3. Inspector records evidence and verified finding. A different Inspector approves the technical
   report. Service Manager releases it; Client accepts it. Inspection invoice status is recorded.
4. Client creates a ticket from the accepted finding. Engineer assesses and executes approved
   work with before/after evidence. Service Manager releases; Client accepts. Maintenance invoice
   status is recorded separately.
5. In a second ticket, Client requests re-inspection. Verify exactly one linked `AD_HOC` WF2
   request. A rework branch may be demonstrated instead if the re-inspection contract is covered
   by an automated integration test.

## Negative checks

- Client in organization B cannot access organization A's asset, report, ticket, or invoice.
- Unassigned Inspector or Engineer cannot view or mutate assignment-specific records.
- Report author cannot peer-review their own report.
- An unconfirmed order cannot be assigned or executed.
- Rejected or unverified AI candidates do not appear in the released report.
- Repeating due-cycle processing, evidence submission, or final acceptance creates no duplicate.
- Accepted report version and approved order versions cannot be overwritten.

## Exit evidence

Keep the backend test report, web/mobile verification logs, OpenAPI contract result, and a short
screen recording or screenshots of the five-role journey. In Jira, close a flow only when its
independent check passes. Close the four-week milestone only when the cross-flow run and the
negative checks pass or the remaining blocker is explicitly accepted by the team.
