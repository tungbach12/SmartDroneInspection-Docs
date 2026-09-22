# WF4 Plan — Như

**Owner**: Như
**Flow**: WF4 — Maintenance and Billing
**Jira Epic**: `SCRUM-57`
**Capacity**: 20 planned days + 0 reserve days

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
