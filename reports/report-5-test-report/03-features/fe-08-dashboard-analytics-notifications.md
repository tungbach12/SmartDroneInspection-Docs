# FE-08: Dashboard, Analytics and Notifications

## Scope baseline

Role-filtered views across the four canonical roles — `ADMIN`, `ORG_ADMIN`,
`INSPECTOR`, `MAINTENANCE_ENGINEER` — as Report 3 §3.9 specifies:

- **`ADMIN`** views subscriptions, technical health and platform/security audit,
  **not** customer technical approvals or repair budgets by default.
- **`ORG_ADMIN`** views own assets, workforce/Drone availability,
  credential/permit expiry, inspection/report queues, team workload, repair
  estimate/actual variance, and pending acceptance/cost decisions.
- **`INSPECTOR`** views assigned inspections, quality decisions, draft
  authoring and returned work. **Engineers** view their assigned team/task
  responsibilities; lead and report-author actions appear **only** for the
  designated people.

Two rules that a dashboard can easily violate:

- Official findings analytics use **approved** findings; candidate and draft
  counts stay **separate**. Mixing them would present unreviewed model output as
  official.
- Dashboards **distinguish** field completed, report published, repairs pending,
  team work completed, technically accepted and closed — these are different
  states and collapsing them misreports progress.

Notifications cover assignment/response, document expiry, readiness changes,
upload/AI completion or failure, returned reports, budget/change decisions,
rework and closure. Notifications **do not waive backend scope checks**: a
notification is not an authorization, and the backend remains the authority.

Tenant isolation is **not** absolute. Per Report 3 §3.5.1, a platform `ADMIN`
holds a separate, read-only cross-tenant capability that confers no organization
authority and no authoring, review or publication right. Isolation applies to
every organization-scoped role; it is bounded, not total, and that boundary is
verified by `WF3-009`.

## Current test coverage

The Report 5 baseline contains no WFx test case mapped to FE-08. **All of
Report 3 §3.9 is unverified**, including the role-separation rules above.

This file records the FE-08 scope without inventing a test-case ID or claiming
execution. Dashboard, analytics and notification acceptance cases remain to be
assigned and recorded before FE-08 can be reported as tested. This is an
explicit, truthful coverage gap.
