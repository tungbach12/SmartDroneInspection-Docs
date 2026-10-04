# WF2 Plan — Quốc

**Owner**: Quốc
**Flow**: WF2 — Request, Order, and Assignment
**Jira Epic**: `SCRUM-55`
**Capacity**: 17 planned days + 3 reserve days

## Outcome

A system-generated periodic request, or a linked ad hoc re-inspection request, becomes a
confirmed order and an accepted Inspector assignment without bypassing quotation approval or
organization scope.

> **Target redesign note (2026-10-03):** The approved transactional chain uses five MFs; MF1 owns request/RFQ, quotation, electronic order and partner-dependent conditional funding. The dedicated MF2 is **Drone Mission Planning & Airspace Clearance**: Provider workforce drafts versioned, SOW/equipment-specific GSD, overlap, AGL/waypoints and shot items, then verifies applicable airspace status and flight-permit requirements under current law. No global numeric mission default or drone-control feature is implied.
>
> `PLATFORM_OPERATOR` publishes one uniform Provider-paid commission and versioned funding/review/cancellation/retention/warranty policies. Values accepted in an order are snapshotted; policy updates are prospective. Conditional funding/hold/release is possible only through an authorized partner product that supports the agreed terms; the Platform is not a funds custodian and Operator decisions are not legal arbitration. This is target scope for a separate re-estimated sprint, not part of the WF2 baseline tasks above. See the drone-centric implementation plan and `project-reference/business-flows.md`.

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
