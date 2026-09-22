# WF2 Plan — Quốc

**Owner**: Quốc
**Flow**: WF2 — Request, Order, and Assignment
**Jira Epic**: `SCRUM-55`
**Capacity**: 17 planned days + 3 reserve days

## Outcome

An ad hoc or periodic request becomes a confirmed order and an accepted Inspector assignment,
without bypassing quotation approval or organization scope.

## Owner tasks

- `T002` — freeze the shared handoff DTO and state contract.
- `T014`–`T016` — request creation/event consumption and quotation revisions.
- `T017`–`T018` — Client approval, order transition, assignment, rejection, and reassignment.
- `T019`–`T020` — web commercial screens and Inspector mobile response.
- `T021`–`T022` — WF1/WF3 handoff tests, security regression, and documentation.

The full task descriptions, estimates, acceptance criteria, and Jira mapping remain in
[tasks.md](../bach/2026-09-22-four-week-mainflow-delivery/tasks.md).

## Delivery windows

| Jira sprint | Dates | Focus |
| --- | --- | --- |
| W3 — Foundation & DB | Sep 28–Oct 2 | Request, quotation, and handoff contract |
| W4 — WF1 & WF2 Core | Oct 5–9 | Approval/order and Inspector assignment |
| W5 — WF3 & WF4 Core | Oct 12–16 | Client/Manager screens and handoff test |
| W6 — Integration & Demo | Oct 19–23 | Inspector mobile response and regression |

## Handoff and acceptance

- Derive Client organization from the authenticated principal.
- Only the current quotation revision can receive a decision; older revisions remain readable.
- Assignment requires a confirmed order and only the assigned active Inspector can respond.
- G3 is green when the accepted assignment creates a ready WF3 inspection.

## References

- [Shared four-week plan](../bach/2026-09-22-four-week-mainflow-delivery/plan.md)
- [Shared handoff contract](../bach/2026-09-22-four-week-mainflow-delivery/flow-handoffs.md)
- [Jira import guide](../bach/2026-09-22-four-week-mainflow-delivery/jira-import-guide.md)
