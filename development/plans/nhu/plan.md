# WF4 Plan — Như

**Owner**: Như
**Flow**: WF4 — Maintenance and Billing
**Jira Epic**: `SCRUM-57`
**Capacity**: 20 planned days + 0 reserve days

## Current status — 10 Oct 2026

The original WF4 tasks below describe the retired five-role baseline. The current
backend target is Enterprise SaaS MF4; use the current Report 3 and business-flow
references as the source of truth, not the old Client/Manager/provider ticket
contract in this plan.

- Backend work is on `feat/maintenance-mf4-work-order`, pushed to origin.
- Commits `e687088`, `fb83725`, `eb6a515`, `3692216`, `24a1128` and `e65386f`
  are on the pushed branch; the MF4 backend REST/workflow slice is committed and
  the MF2 mainline is merged in.
- Implemented: repair candidates, work orders, internal team/tasks, priced
  estimate approval/rework, work-log submission/lead verification, change
  decisions, completion reports, independent acceptance/rework, actual-cost
  reconciliation, and closeout. Re-inspection is recorded but does not dispatch
  MF1.
- Security audit applied: maintenance engineers read only work orders assigned
  to their team (others return not-found), cross-tenant source validation runs
  before duplicate disclosure, requested team members are persisted, the budget
  approver is rejected inside the executing team, and a second team designation
  cannot silently overwrite the first.
- Final backend verification: `./mvnw.cmd spotless:apply verify` passes 457
  tests; Spotless, Modulith boundary checks and JaCoCo 80% gate pass after the
  MF2 mainline merge and assignment-scope security audit.
- Report 5 records `WF3-010`–`WF3-012` under FE-07, and the integrated report
  has 10 selected cases across MF2-07, MF3 and the MF4 backend slice. These
  cases are not full MF4 acceptance.
- Credential rule currently allows no record but rejects a recorded credential
  that is non-ACTIVE or expired. This deviates from Report 3's required-presence
  gate; applicable skills are not modelled.
- Still outstanding: required-credential issuance/verification and skill
  matching; notifications; linked MF1 re-inspection dispatch; before/during/after
  evidence object workflow and rendered completion-report artifact; maintenance
  web/mobile clients; and remaining MF4 target gates. Do not claim full MF4
  acceptance from the backend API surface alone.

## Outcome

Accepted findings become assessed, approved, executed, released, and resolved maintenance work.
Inspection and maintenance use separate post-service invoice status; the first release has no
online payment gateway.

## Owner tasks

- `T004` — accepted-report/finding fixture for independent WF4 development.
- `T034`–`T035` — ticket creation and Client ticket view.
- `T036`–`T038` — assessment, quotation/order versions, approval, and execution assignment.
- `T039`–`T041` — assigned work/evidence, change approval, release, resolution, and re-inspection.
- `T042`–`T045` — Manager/Client web, Engineer mobile execution, invoice milestones, and regression.

The full task descriptions, estimates, acceptance criteria, and Jira mapping remain in
[tasks.md](../bach/2026-09-22-four-week-mainflow-delivery/tasks.md).

## Delivery windows

| Jira sprint | Dates | Focus |
| --- | --- | --- |
| W3 — Foundation & DB | Sep 28–Oct 2 | Ticket API/UI and execution fixture UI |
| W4 — WF1 & WF2 Core | Oct 5–9 | Assessment, estimate, quote/order, mobile assessment |
| W5 — WF3 & WF4 Core | Oct 12–16 | Work evidence, change order, release/resolution |
| W6 — Integration & Demo | Oct 19–23 | Web/mobile completion, invoices, regression |

## Handoff and acceptance

- Ticket creation requires at least one own-organization verified finding from an accepted report.
- Approved scope/order is required before execution; extra work waits for Client approval.
- Assigned Engineers alone can write work logs and required before/after evidence.
- Re-inspection creates one linked WF2 request without a module dependency cycle.
- Record one invoice per accepted inspection report or maintenance order with manual payment status.
- G5 and the full five-role journey are green before release.

## References

- [Shared four-week plan](../bach/2026-09-22-four-week-mainflow-delivery/plan.md)
- [Shared handoff contract](../bach/2026-09-22-four-week-mainflow-delivery/flow-handoffs.md)
- [Jira import guide](../bach/2026-09-22-four-week-mainflow-delivery/jira-import-guide.md)
