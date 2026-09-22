# Tasks: FE-04 — Week 3 WF3 Inspection Execution and Evidence Foundation

## Jira ownership

- Feature: `FE-04 — Inspection Execution & Evidence Management`.
- Parent: `SCRUM-56 — FE-04 | WF3 — Inspection Execution & Evidence Management`.
- Sprint: `W3 — Foundation & DB` (`SCRUM` sprint `36`).
- Owner: Bách.
- Foundation dependency: `SCRUM-58/T001` is now under `SCRUM-108 — FE-01 | W3 — Identity & Access Governance` and covers authentication and migrations V1–V9. MinIO/evidence storage is owned by the later FE-04 task `T025/SCRUM-85`.

## [X] T003 — `SCRUM-63` — Accepted-assignment fixture (1 day)

- Create `backend/src/test/java/com/smartdroneinspection/inspections/InspectionFixture.java`.
- Seed an active organization, Inspector, asset, service order, accepted assignment, active
  checklist template, and required checklist item.
- Use production entities/repositories and real role/status values.
- Add a focused fixture test proving organization and assignee IDs are preserved.

## [X] T023 — `SCRUM-83` — Assignment-scoped inspection/checklist backend (2 days)

- Implement the application service and thin API actions described in the contract.
- Resolve assignment and resource scope from the authenticated principal.
- Make start/resume idempotent and prevent reopening invalid states.
- Validate checklist-template ownership and required response values.
- Add positive, non-assignee, inactive-user, foreign-template, and retry tests.

## [X] T024 — `SCRUM-84` — Inspector mobile assigned list/start (1 day)

- Connect `mobile/lib/features/inspections/presentation/inspections_page.dart` to the bearer API.
- Show only server-authorized accepted assignments.
- Add loading, empty, error, start, and resume states.
- Do not add evidence/photo/report functionality in this task.

## Exit gate

The three tasks are ready for review when the focused backend and mobile checks pass, the API
contract matches the implementation, and no FE-05/FE-06 report or AI work is mixed into the PR.

Verification note: backend focused tests, full `verify`, and Modulith architecture checks pass with
Docker. The separate FE-01 foundation gate is also verified by
`backend/src/test/java/com/smartdroneinspection/WorkflowBaselineTest.java`: Flyway V1-V9 applied
on a clean database and all five generated role fixtures authenticated without default credentials.
The local MinIO service was checked separately as infrastructure for the later FE-04 evidence task;
it is not part of the FE-01 acceptance scope. Mobile format, analysis, and tests pass.
