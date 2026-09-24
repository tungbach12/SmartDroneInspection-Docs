# Implementation Plan: WF3 Jira Delivery Completion (FE-04–FE-06)

**Branch**: docs/bach-wf3-jira-task-plan | **Date**: 2026-09-24 | **Spec**: [spec.md](spec.md)<br>
**Jira scope**: [jira-scope.md](jira-scope.md)

**Input**: WF3 feature specification and live Jira assignment snapshot in this folder.

## Summary

Complete the nine remaining assigned WF3 Jira tasks, SCRUM-85–SCRUM-93 / T025–T033, estimated at 13 person-days. The delivery covers FE-04 evidence capture, FE-05 AI-assisted finding verification, and FE-06 report review and Client acceptance. Build on the completed assignment/start/checklist work; store evidence bytes in MinIO and metadata in PostgreSQL; treat AI output as advisory; enforce assignment, organization, ownership, and reviewer separation in backend use cases; then integrate web/mobile actions and regression evidence. Preserve the WF4/billing handoff without including the separately owned invoice implementation.

Implementation detail and proposed API shapes are in [research.md](research.md), [data-model.md](data-model.md), and [contracts/wf3-api-and-handoff-contract.md](contracts/wf3-api-and-handoff-contract.md). The proposed routes and DTOs must be reconciled with current code and the versioned API before implementation.

## Technical Context

**Language/Version**: Java 21, TypeScript/React 19, Dart/Flutter<br>
**Primary Dependencies**: Spring Boot 4.1, Spring Modulith, React/Vite/Material UI, Flutter/Riverpod/GoRouter/Dio; add the MinIO Java SDK for evidence storage and call the configured YOLO service<br>
**Storage**: PostgreSQL using the V7 WF3 schema plus V10 Client-decision audit fields; MinIO for evidence bytes<br>
**Testing**: JUnit/Testcontainers, Vitest, Flutter test/analyze/format, plus documented Report 5 acceptance cases<br>
**Target Platform**: Existing Spring API, web, and mobile deployments<br>
**Project Type**: Cross-repository product feature backed by a modular-monolith API<br>
**Performance Goals**: No new numeric target is stated in Jira or the reviewed SRS; preserve configured upload/API limits<br>
**Constraints**: Backend authorization is authoritative; accepted report versions are immutable; no secrets or protected evidence in logs; migrations are forward-only and only for proven schema gaps; no speculative broker or abstraction<br>
**Scale/Scope**: Three features, one WF3 journey, nine open assigned issues, 13 estimated person-days; completed/deprecated WF3 issues are prerequisites/history, not new implementation scope

## Constitution Check

| Principle | Assessment |
| --- | --- |
| Capability ownership and simplicity | Pass: keep WF3 lifecycle in the existing inspections capability and existing client feature folders; add only concrete MinIO/inference integration needed by the tickets. |
| Scoped authorization and safe data | Pass: enforce role plus organization, accepted assignment, ownership, and author/reviewer separation on the backend. |
| Typed boundaries and contract discipline | Pass: document versioned DTO/API shapes; confirm final routes and schemas against implementation before client integration. |
| Evidence-based verification | Pass as a plan: specify focused tests and Report 5 updates. No implementation checks are claimed as already run. |
| Auditable delivery | Pass: use the named docs branch, retain Jira traceability, report exact future checks/results; no commit, push, or PR is included. |

**Implementation re-check**: Reused the V7 WF3 schema and feature boundaries. Focused Client-decision acceptance tests proved the audit actor/reason were not persisted, so forward migration V10 adds those two fields; V9 remains the notifications migration. No other schema migration or module boundary was added.

## Scope and Jira sequence

The live assignee query returned 27 SCRUM issues. Sixteen are WF3-related: nine open, six Done, and one explicitly deprecated issue marked Done. The nine open items below are the implementation scope; full ownership/status/sprint/week/estimate detail is in [jira-scope.md](jira-scope.md).

| Order | Jira / task | Feature | Planned outcome | Due |
| --- | --- | --- | --- | --- |
| 1 | SCRUM-85 / T025 | FE-04 | Validate/hash evidence, retry-safe MinIO object plus PostgreSQL metadata; reject corrupt/unsupported media. | 2026-10-06 |
| 2 | SCRUM-86 / T026 | FE-05 | Persist configured YOLO results as candidates with model/version/geometry; AI failure leaves evidence usable. | 2026-10-07 |
| 3 | SCRUM-87 / T027 | FE-05 | Inspector confirms/modifies/rejects candidates or records manual findings; pending/rejected candidates stay unofficial. | 2026-10-08 |
| 4 | SCRUM-88 / T028 | FE-06 | Build report drafts and immutable versions; revisions append linked versions. | 2026-10-13 |
| 5 | SCRUM-89 / T029 | FE-06 | Enforce independent peer review; record change request or technical approval; deny self-review. | 2026-10-14 |
| 6 | SCRUM-90 / T030 | FE-06 | Manager release, Client accept/revision, and accepted-report/WF4 billing handoff. | 2026-10-15 |
| 7 | SCRUM-91 / T031 | FE-06 | Integrate web inspection/report screens with authorized lifecycle states/actions. | 2026-10-20 |
| 8 | SCRUM-92 / T032 | FE-04 | Mobile checklist/photo capture with validation, failure, and retry feedback. | 2026-10-21 |
| 9 | SCRUM-93 / T033 | FE-06 | G3/G4, authorization, report visibility, manual fallback, and immutable-acceptance regression. | 2026-10-23 |

### Proposed delivery windows

- 2026-09-28–2026-10-06: T025, building on completed T023/T024.
- 2026-10-06–2026-10-08: T026–T027.
- 2026-10-09–2026-10-15: T028–T030.
- 2026-10-16–2026-10-23: T031–T033.

These are sequencing windows based on Epic dates and Jira due dates, not a capacity commitment. Jira internal-week labels W2–W4 differ from sprint labels W4–W6; preserve both and plan by explicit due dates.

## Implementation approach

1. **Confirm prerequisites and API contract.** Recheck repo status, controllers, entities, V7 migration, and adjacent tests. Preserve the completed accepted-assignment fixture and start/checklist contract. Confirm endpoint names, upload limits, stable errors, and typed DTOs before parallel client work; the contract artifact is proposed, not an assertion that all endpoints already exist.
2. **T025 evidence slice.** Validate media type, size, and content at the boundary; compute SHA-256 server-side; derive uploader and scope from authenticated context; store bytes in MinIO and metadata/object reference in PostgreSQL. Define an inspections-owned SPI port and implement it in the infrastructure storage adapter. Make retries idempotent by inspection plus checksum, handle concurrent duplicates, and clean up failed writes without exposing orphan objects. Serve evidence only through scope-checked backend reads; never return unrestricted object URLs. Missing GPS remains valid.
3. **T026–T027 candidate/verification slice.** Define an inspections-owned inference SPI port and implement the configured YOLO adapter under infrastructure/ai. Call inference only for eligible evidence. Persist model/version, label, confidence, and bounding box as candidate data. AI failure must not block evidence access or manual findings. Only authorized Inspector confirmation/modification or manual creation produces official findings; pending/rejected candidates do not appear in reports or official counts.
4. **T028–T030 report lifecycle.** Compile reports from checklist, evidence, and verified findings. Store revisions as new immutable versions. Enforce reviewer assignment and author/reviewer separation in backend logic; bind each review decision to the exact version. Require completeness and technical approval before manager release. Clients see released versions and only their linked evidence. Acceptance locks the version and publishes a minimal internal handoff.
5. **T031–T032 client integration.** Update the existing web inspection/report pages and mobile inspection feature with typed API models and meaningful loading, empty, validation, retry, and permission-denied states. Client guards are navigation only, not security.
6. **T033 regression and closeout.** Verify G3 assignment input and G4 accepted-report handoff, negative authorization paths, AI/manual fallback, hidden drafts, and immutable acceptance. Update Report 5 index, detailed Feature 2 procedures, statistics, cover, and change history. Update Report 3/business-flow/API docs if implementation changes or clarifies a product contract.

## Dependencies and scope boundaries

- Completed prerequisites: SCRUM-63/T003 accepted-assignment fixture; SCRUM-83/T023 backend start/checklist; SCRUM-84/T024 mobile assigned-inspection list/start; SCRUM-43 schema design/bootstrap.
- Sequence: T025 precedes inference; T026 candidates feed T027 verification; verified findings feed T028; review/release/acceptance are T028–T030; web/regression depend on the agreed contracts. T032 can proceed after checklist/evidence contract freeze.
- G3 is the accepted WF2 assignment input. G4 is the accepted-report/WF4 billing handoff. T030 owns the WF3 event/contract, not invoice persistence or payment processing; coordinate with that separate owner.
- SCRUM-93 cites the retired docs/content/backend/flows/inspections-and-reports.md path. Use the current top-level docs tree, including backend/flows/inspections-and-reports.md when appropriate; do not recreate docs/content/.
- Do not reopen completed issues, edit Jira, take over FE-01/WF1/WF2/WF4 implementation, train a model, add online payments, or pilot drones.

## Data, security, and failure handling

- Reuse V7 schema and documented invariants in [data-model.md](data-model.md); the proven Client decision audit gap is handled by forward-only migration V10 and documented in the database design.
- Scope every query and command by authenticated user, organization, accepted assignment, and workflow state. Deny author self-review and expose only released versions to Clients.
- Do not trust client-provided checksum, identity, organization, reviewer, or report status. Never log evidence bytes, credentials, or protected content; do not expose MinIO secrets or unrestricted object URLs.
- Storage failure must not expose metadata for unavailable bytes. AI failure must not hide existing evidence. Revisions must not mutate older or accepted versions.
- Keep handoffs inside existing Modulith event mechanisms; do not add a broker or queue for these tickets.

## Verification plan

| Scope | Required checks |
| --- | --- |
| T025 / FE-04 | Valid/invalid media; server checksum; duplicate/concurrent retry; interrupted upload and cleanup; GPS absent; scoped content reads; wrong Inspector/cross-organization denial; MinIO and metadata consistency. |
| T026–T027 / FE-05 | Candidate provenance/shape; confirm/modify/reject/manual; pending/rejected exclusion from reports; AI failure retains evidence and manual path. |
| T028–T030 / FE-06 | Draft composition; append-only versions; self-review denial; reviewer decision; manager-only release; Client draft/comment isolation; released evidence visibility; accept/revision; immutability; one G4 handoff. |
| T031–T032 / clients | Web/mobile happy path and loading/empty/error/retry/permission states; typed contract compatibility. |
| T033 / regression | G3/G4, organization/assignment boundaries, AI/manual path, reviewer separation, hidden drafts, released visibility, accepted-version immutability. |

Run the commands in [quickstart.md](quickstart.md) after implementation. Report exact executed commands and outcomes; record skipped live-YOLO tests honestly. Update Report 5 with stable IDs, procedures, expected results, dates, tester, and evidence. Pending is not completion.

## Documentation impact

Implementation clarified and documented the checklist read contract, optional YOLO adapter contract, Client decision audit fields, and accepted-report handoff. Report 3 functional requirements and its change history, business-flow/database references, backend/frontend/mobile guidance, and all required Report 5 Markdown sources were updated. Report 5 retains the supplied workbook layout and stable case IDs. Automated regression passed; live YOLO deployment and interactive browser/device walkthroughs remain unrun and are called out in [quickstart.md](quickstart.md).

## Project Structure

### Documentation (this feature)

```text
docs/development/plans/bach/2026-09-24-wf3-jira-task-completion/
├── plan.md
├── spec.md
├── tasks.md
├── jira-scope.md
├── research.md
├── data-model.md
├── quickstart.md
└── contracts/
    └── wf3-api-and-handoff-contract.md
```

### Source code (existing owning repositories)

```text
backend/src/main/java/com/smartdroneinspection/inspections/
├── api/                         # controller and request/response DTOs
├── domain/                      # existing WF3 entities and states
├── repository/                  # existing persistence
├── service/                     # use-case orchestration
└── spi/                         # named feature-owned outbound ports for MinIO and YOLO

backend/src/main/java/com/smartdroneinspection/infrastructure/
├── ai/                           # configured YOLO adapter
└── storage/                      # MinIO evidence adapter

backend/src/test/java/com/smartdroneinspection/inspections/
# extend feature-owned tests and workflow fixtures

frontend/src/features/
├── inspections/pages/InspectionsPage.tsx
└── reports/pages/ReportsPage.tsx

mobile/lib/features/inspections/
├── data/
├── domain/
└── presentation/

docs/reports/report-3-software-requirement-specification/
docs/project-reference/
docs/reports/report-5-test-report/
```

**Structure Decision**: Extend existing inspections and client feature folders. Define only the feature-owned SPI ports required for the concrete MinIO and YOLO integrations; implement them from infrastructure without importing infrastructure into inspections. Keep contracts and test evidence in their owning docs/repositories. Do not create separate AI/report business modules or generic abstractions without real consumers.

## Complexity Tracking

No constitution violations or unjustified complexity are planned. MinIO and the configured YOLO call are concrete T025/T026 requirements; add only dependencies needed to fulfill them.
