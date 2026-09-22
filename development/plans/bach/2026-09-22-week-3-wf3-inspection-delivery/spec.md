# Feature Specification: FE-04 — Week 3 WF3 Inspection Execution and Evidence Foundation

**Feature Branch**: `docs/four-week-mainflow-jira`
**Created**: 2026-09-22
**Status**: Implemented and verified
**Input**: User description: "Align the Week 3 WF3 inspection delivery slice with the FE-04 Jira parent and the FE-01 foundation dependency."

**Owner**: Bách
**Feature code**: `FE-04 — Inspection Execution & Evidence Management`
**Jira sprint**: `W3 — Foundation & DB` (`SCRUM` sprint `36`)
**Dates**: 2026-09-28–2026-10-02
**Jira parent**: `SCRUM-56 — FE-04 | WF3 — Inspection Execution & Evidence Management`
**Jira tasks**: `SCRUM-63/T003`, `SCRUM-83/T023`, `SCRUM-84/T024`
**Related foundation dependency**: `SCRUM-58/T001` belongs to `SCRUM-108 — FE-01 | W3 — Identity & Access Governance`; its authentication and schema smoke gate is owned by Bách and remains a prerequisite, not part of this FE-04 slice. Evidence storage/MinIO belongs to `T025/SCRUM-85` under FE-04.

## User Scenarios & Testing

### User Story 1 — View assigned inspection work (Priority: P1)

As an Inspector, I want to see only accepted inspection assignments that belong to me so that I
can work on authorized field inspections without seeing another Inspector's work.

**Why this priority**: Assignment scope is the safety boundary for the inspection process and is
required before any inspection data can be recorded.

**Independent Test**: Use two active Inspectors with assignments in the same environment. Each
Inspector can list only their own accepted assignment, while an inactive or unrelated Inspector
receives no usable access.

**Acceptance Scenarios**:

1. **Given** an active Inspector has an accepted assignment, **when** they open their inspection
   work list, **then** only their accepted assignment is shown.
2. **Given** another Inspector or an inactive Inspector requests the work list, **when** the request
   is evaluated, **then** the assignment is not exposed.

---

### User Story 2 — Start or resume an inspection (Priority: P1)

As an assigned Inspector, I want to start an inspection and safely retry the action so that network
retries do not create duplicate inspection records.

**Why this priority**: A single inspection record is necessary for trustworthy evidence, checklist,
and report history.

**Independent Test**: Start the same accepted assignment twice and verify that both attempts refer to
one in-progress inspection.

**Acceptance Scenarios**:

1. **Given** an accepted assignment has no inspection, **when** the assigned Inspector starts it,
   **then** one in-progress inspection is created for that assignment.
2. **Given** the assignment already has an in-progress inspection, **when** the assigned Inspector
   retries start, **then** the existing inspection is returned and no duplicate is created.
3. **Given** the inspection is completed or released, **when** anyone attempts to reopen it through
   this slice, **then** the state remains closed to reopening.

---

### User Story 3 — Record valid checklist responses (Priority: P1)

As an assigned Inspector, I want to save valid responses for the inspection checklist so that the
inspection has complete, attributable field results.

**Why this priority**: Checklist responses are the minimum inspection result needed before evidence,
findings, and report work can proceed.

**Independent Test**: Save a valid response, then attempt a blank required response and a response
from a different checklist template; verify the valid response is retained and invalid responses are
rejected.

**Acceptance Scenarios**:

1. **Given** an in-progress inspection and a checklist item from its active template, **when** the
   assigned Inspector saves a valid response, **then** the response is stored with the Inspector and
   the recorded time.
2. **Given** a required checklist item, **when** the Inspector submits an empty or invalid response,
   **then** the response is rejected with a clear validation result.
3. **Given** a checklist item belongs to another template, **when** the Inspector submits it,
   **then** the response is rejected and no cross-template data is stored.

### Edge Cases

- A start request is retried after a timeout; it must remain idempotent.
- An accepted assignment is changed to an invalid state before start; the Inspector must not start it.
- The assignment belongs to another organization or Inspector; no inspection or checklist data is
  disclosed.
- The Inspector becomes inactive after opening the work list; subsequent protected actions are denied.
- A checklist item is removed or becomes inactive between list and save; the response is rejected
  without changing existing valid responses.
- The field client has a loading, empty, or error state; it must not imply that an unauthorized
  assignment is available.

## Requirements

### Functional Requirements

- **FR-001**: The system MUST list only accepted inspection assignments that are assigned to the
  authenticated active Inspector.
- **FR-002**: The system MUST prevent access to assignments belonging to another Inspector or
  organization.
- **FR-003**: The system MUST create at most one inspection for an accepted assignment.
- **FR-004**: The system MUST return the existing in-progress inspection when the assigned Inspector
  retries a start action.
- **FR-005**: The system MUST prevent completed or released inspections from being reopened through
  this feature.
- **FR-006**: The system MUST derive the inspection's assignment, asset, service order, author, and
  checklist context from trusted assignment data rather than accepting conflicting client values.
- **FR-007**: The system MUST accept checklist responses only for items belonging to the inspection's
  checklist template.
- **FR-008**: The system MUST reject blank or invalid responses for required checklist items.
- **FR-009**: The system MUST record the authenticated Inspector and response time for every accepted
  checklist response.
- **FR-010**: The field inspection experience MUST show clear loading, empty, success, and error
  states without replacing server-side authorization.

### Key Entities

- **Accepted assignment**: The authorized work allocation connecting an Inspector, organization,
  asset, and service order.
- **Inspection**: The single inspection session created from an accepted assignment, with lifecycle
  state and checklist context.
- **Checklist template and item**: The active inspection questions and their response rules.
- **Checklist response**: An Inspector-attributed answer recorded against one inspection item.

## Success Criteria

### Measurable Outcomes

- **SC-001**: In authorization tests covering two organizations and two Inspectors, 100% of list,
  start, and checklist actions outside the assigned scope are denied without disclosing protected
  data.
- **SC-002**: Retrying the start action at least five times for the same accepted assignment produces
  exactly one inspection record in every test run.
- **SC-003**: 100% of required-item tests reject blank or invalid responses, while 100% of valid
  responses retain the correct Inspector and recorded time.
- **SC-004**: The Week 3 acceptance suite passes for fixture creation, assignment scope, start
  idempotency, checklist validation, and non-assignee denial before the three FE-04 tasks are closed.
- **SC-005**: An Inspector can find an assigned accepted inspection and start or resume it in under
  two minutes in the demonstration environment.

## Assumptions

- The FE-01 W3 foundation gate (`SCRUM-58/T001`) provides working authentication and a compatible
  data baseline before FE-04 validation begins. FE-04 evidence storage is tracked separately in
  `T025/SCRUM-85`.
- FE-02/WF1 provides the active checklist template and required checklist items used by the fixture.
- WF2 may still be incomplete during Week 3, so a deterministic accepted-assignment fixture is an
  approved test seam and does not create a second production workflow.
- FE-05 AI candidate verification and FE-06 report approval are separate WF3 feature parents and
  remain outside this Week 3 slice.
- Evidence upload beyond the focused inspection start/checklist slice, AI candidates, verified
  findings, report versions, peer review, release, Client acceptance, and inspection photos are
  later tasks (`T025`–`T033`).
- Existing inspection data concepts are sufficient for this slice; no new data concept is introduced.
