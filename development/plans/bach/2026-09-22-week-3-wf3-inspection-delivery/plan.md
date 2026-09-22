# Implementation Plan: FE-04 — Week 3 WF3 Inspection Execution and Evidence Foundation

**Branch**: `docs/four-week-mainflow-jira`
**Date**: 2026-09-22
**Spec**: [spec.md](spec.md)
**Owner**: Bách
**Jira parent**: `SCRUM-56 — FE-04 | WF3 — Inspection Execution & Evidence Management`

## Summary

Implement the smallest FE-04/WF3 vertical slice required by Jira Week 3: seed an accepted-assignment
fixture, enforce assignment-scoped inspection start/checklist behavior in the backend, and connect
the Inspector mobile inbox/start view. Reuse the current entities, repositories, migrations, auth,
and bearer transport.

## Technical context

| Area | Decision |
| --- | --- |
| Backend | Java 21, Spring Boot 4.1, Spring Modulith; `inspections` owns orchestration. |
| Persistence | Existing PostgreSQL schema and JPA entities from migrations V6–V7; no new migration. |
| Clients | Flutter/Riverpod/Dio mobile screen; same bearer resource contract as the web API. |
| Auth | Existing authenticated principal; Inspector role plus accepted-assignment scope. |
| Tests | Focused Spring tests, repository scope assertions, and mobile contract/widget checks. |
| Constraints | Do not import another module's controller, DTO, entity, or repository. Do not trust client-supplied organization, asset, author, or checklist IDs. |

## Constitution check

| Principle | Evidence | Result |
| --- | --- | --- |
| Capability ownership | Fixture and application behavior belong to `inspections`; mobile stays under `features/inspections`. | Pass |
| Scoped authorization | Every command resolves the accepted assignment for the authenticated Inspector. | Pass |
| Typed boundaries | Request/response records and stable ProblemDetail codes are documented before client work. | Pass |
| Evidence-based verification | Each acceptance criterion has a focused automated assertion and a Week 3 exit check. | Pass |
| Auditable delivery | Work is isolated to the docs plan and later per-repository feature branches; no `main` changes. | Pass |

## Design

1. `T003`: build deterministic test data for an active organization, Inspector, asset, service
   order, accepted assignment, checklist template, and required items.
2. `T023`: add the inspection application service and thin controller actions for scoped list,
   start/resume, and checklist-response upsert. Start is idempotent per accepted assignment.
3. `T024`: connect the mobile assigned list/start page to the stable DTO; keep authorization on the
   backend and surface loading/empty/error states.
4. Run the acceptance matrix and record evidence in the three FE-04 Jira tasks and the
   implementation PR. Do not pull FE-05 candidate verification or FE-06 report approval work into
   this sprint slice.

## Delivery sequence

| Date | Task | Exit condition |
| --- | --- | --- |
| 2026-09-28 | `SCRUM-63/T003` fixture | Tests can start from an accepted assignment without a completed WF2 runtime. |
| 2026-09-29–30 | `SCRUM-83/T023` backend | Scope, start/resume idempotency, template checks, and required responses pass. |
| 2026-10-01 | `SCRUM-84/T024` mobile | Inspector sees only assigned work and can start/resume it through the API. |
| 2026-10-02 | Integration reserve | Focused tests, API review, and Jira closeout evidence are recorded. |

## Project structure

```text
docs/development/plans/bach/2026-09-22-week-3-wf3-inspection-delivery/
├── spec.md
├── plan.md
├── research.md
├── data-model.md
├── contracts/
│   └── w3-inspection-start-and-checklist.md
├── quickstart.md
└── tasks.md

backend/src/main/java/com/smartdroneinspection/inspections/
├── api/
├── domain/
├── repository/
└── service/

backend/src/test/java/com/smartdroneinspection/inspections/
└── InspectionWorkflowTest.java

mobile/lib/features/inspections/presentation/
└── inspections_page.dart
```

## Verification

```powershell
cd backend
.\mvnw.cmd -Dtest=InspectionFixtureTest,InspectionWorkflowTest test

cd ..\mobile
dart format --set-exit-if-changed .
flutter analyze
flutter test
```

Run the full repository checks before the PR is merged, as required by the repository conventions.
