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
Report 3 §3.9 remains unverified at the workbook acceptance level**, including the
role-separation rules above.

Supporting verification for the 2026-10-26 in-app notification inbox slice
(cross-referenced in `03-features/fe-03-inspection-request-work-assignment.md`)
covers backend unit/service/controller/architecture checks (part of the 96-test
recurrence/notification slice) and web inbox UI/routing checks (part of the
212-test inspections/notifications subset and integrated Frontend PR #62
`80/80` files / `576/576` tests). Mobile notification inbox delivery is **not
delivered** in the mobile repository (no tracked notification files, tests, or
open PR). On the backend, `V4__recurring_inspection_schedules.sql` and
`V5__notification_inbox_deduplication.sql` follow immutable `V1`/`V2` and
forward cleanup `V3__drop_unused_wf1_columns.sql`; post-`V3`/`V4`/`V5` full
`./mvnw.cmd verify` and real `V1`→`V5` upgrade regression passed **845/845
tests** (`4aa04cc9-e4fa-4347-9c8d-3a8f15c1d13c.log`).

This file records the FE-08 scope without inventing a test-case ID or claiming
workbook case execution. Dashboard, analytics and notification acceptance cases
remain to be assigned and recorded before FE-08 can be reported as tested in the
workbook. This remains an explicit, truthful coverage gap.

## Feature sheet summary

Values for the `Feature 8` summary block (`A2:E8` in the workbook).
The template reads these back by formula, so an export needs them
recorded here.

| Cell | Label | Value |
| --- | --- | --- |
| `B2` | Feature | Dashboard, Analytics and Notifications |
| `B3` | Test requirement | Would verify role-scoped dashboards, approved-finding analytics and notification delivery. No case is assigned; FE-08 is an explicit coverage gap. |
