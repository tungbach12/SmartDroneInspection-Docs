---
description: "Dependency-ordered implementation tasks for WF3 FE-04–FE-06"
---

# Tasks: WF3 Jira Delivery Completion (FE-04–FE-06)

**Inputs**: [spec.md](spec.md), [plan.md](plan.md), [research.md](research.md), [data-model.md](data-model.md), [API contract](contracts/wf3-api-and-handoff-contract.md), and [quickstart.md](quickstart.md).

**Scope**: Nine open assigned Jira tasks SCRUM-85–SCRUM-93 / Jira task IDs T025–T033. Spec Kit IDs T001–T031 below are a separate sequential task numbering scheme.

**Priority note**: The spec does not assign P1/P2 labels. The story order below is an implementation sequence inferred from the plan's data dependencies and Jira due dates, not a product-priority decision.

**Tests**: Automated tests and Report 5 cases are included because the workspace rules require feature tests, executed verification, and traceable test-report updates for completion. Write the story tests first and confirm they fail for the missing behavior before implementing it.

**Setup status**: Backend, frontend, mobile, and docs repositories plus their test/lint/build tooling already exist; no project bootstrap task is needed.

**Organization**: Tasks are grouped by the four user stories in spec.md. Paths are relative to the Capstone workspace root.

## Format

Required checklist shape: Tnnn, optional [P], optional [US#], action with exact file path(s).
- [P] marks work that can run in parallel without editing the same files or depending on unfinished tasks.
- [US#] maps to the matching user story in spec.md. Foundation and polish tasks have no story label.
- Jira SCRUM keys and Jira task IDs are included in descriptions for traceability; they do not replace Spec Kit task IDs.

## Phase 1: Setup

**Purpose**: Project initialization.

No tasks: the repositories and test/build tooling are already initialized.

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Freeze cross-client contracts and shared authorization fixtures before story implementation.

- [X] T001 Reconcile proposed evidence, candidate, report, review, release, and Client-decision routes/DTOs/error codes against the current InspectionController, auth scope, and web/mobile networking conventions; update the agreed versioned contract in docs/development/plans/bach/2026-09-24-wf3-jira-task-completion/contracts/wf3-api-and-handoff-contract.md.
- [X] T002 [P] Extend accepted-assignment test fixtures with distinct authorized/unauthorized Inspectors and organizations plus the checklist/report inputs needed by the WF3 tests in backend/src/test/java/com/smartdroneinspection/inspections/InspectionFixture.java.

**Checkpoint**: T001–T002 are complete; all story tests use the same accepted-assignment and scope model.

---

## Phase 3: User Story 1 — Capture a Complete, Authorized Inspection Record (Sequence P1, MVP; SCRUM-85)

**Goal**: The accepted assignee can save checklist-linked evidence with validated content, server-computed checksum, retry safety, and MinIO/PostgreSQL consistency.

**Independent Test**: Given a seeded accepted assignment and in-progress inspection, test a valid upload, invalid/corrupt files, missing GPS, same-content retry, interrupted storage, and wrong-assignee/cross-organization access without requiring AI or report services.

### Tests for User Story 1

- [X] T003 [P] [US1] Add failing evidence-service tests for content/type/size validation, server SHA-256, duplicate and concurrent retry, missing GPS, scoped object reads, and storage/metadata failure in backend/src/test/java/com/smartdroneinspection/inspections/EvidenceServiceTest.java.
- [X] T004 [P] [US1] Add failing API integration tests for accepted-assignee upload/read authorization, cross-organization denial, stable ProblemDetail errors, and MinIO/PostgreSQL consistency in backend/src/test/java/com/smartdroneinspection/inspections/EvidenceApiIntegrationTest.java.

### Implementation for User Story 1

- [X] T005 [US1] Add the MinIO Java SDK and environment-bound bucket/endpoint configuration without committing credentials in backend/pom.xml, backend/src/main/resources/application.yml, and backend/src/main/resources/application-prod.yml.
- [X] T006 [US1] Define the inspections-owned EvidenceObjectStore port and annotate inspections/spi with @NamedInterface("spi"); implement MinIO upload/read/cleanup plus evidence persistence with inspection-plus-checksum idempotency in backend/src/main/java/com/smartdroneinspection/inspections/spi/package-info.java, backend/src/main/java/com/smartdroneinspection/inspections/spi/EvidenceObjectStore.java, backend/src/main/java/com/smartdroneinspection/infrastructure/storage/MinioEvidenceObjectStore.java, backend/src/main/java/com/smartdroneinspection/inspections/service/EvidenceService.java, backend/src/main/java/com/smartdroneinspection/inspections/repository/EvidenceRepository.java, and backend/src/main/java/com/smartdroneinspection/inspections/domain/Evidence.java.
- [X] T007 [US1] Add typed multipart metadata/response DTOs plus scoped upload/list/content-stream endpoints, with stable validation and scope errors and no unrestricted object URLs, in backend/src/main/java/com/smartdroneinspection/inspections/api/InspectionController.java, backend/src/main/java/com/smartdroneinspection/inspections/api/dto/request/EvidenceUploadMetadataRequest.java, and backend/src/main/java/com/smartdroneinspection/inspections/api/dto/response/EvidenceResponse.java.
- [X] T008 [US1] From backend/, run .\mvnw.cmd -Dtest=EvidenceServiceTest,EvidenceApiIntegrationTest test and record actual procedure, expected result, status, date, tester, and evidence for stable cases WF3-001/WF3-002 mapped to FE-04 in docs/reports/report-5-test-report/01-test-cases/test-case-list.md and docs/reports/report-5-test-report/03-features/feature-2.md; never mark an unrun check Passed.

**Checkpoint**: FE-04 upload/list behavior is independently testable against the accepted-assignment fixture; evidence bytes and metadata agree and unauthorized access is denied.

---

## Phase 4: User Story 2 — Review AI Candidates and Record Verified Findings (Sequence P2; SCRUM-86–SCRUM-87)

**Goal**: YOLO output stays advisory until the assigned Inspector confirms/modifies it; manual findings remain available when AI fails.

**Independent Test**: Given persisted evidence and an authorized Inspector, a deterministic AI stub creates a candidate with model/version/label/confidence/bounding box; confirm/modify/reject/manual paths enforce state and scope; pending/rejected candidates never become report findings; AI failure does not hide evidence.

### Tests for User Story 2

- [X] T009 [P] [US2] Add failing service tests for AI candidate provenance, confirm/modify/reject transitions, manual findings, pending/rejected exclusion, and inference failure in backend/src/test/java/com/smartdroneinspection/inspections/AiFindingServiceTest.java.
- [X] T010 [P] [US2] Add failing API integration tests for candidate review authorization, assignment/organization scope, invalid state transitions, and stable errors in backend/src/test/java/com/smartdroneinspection/inspections/AiFindingApiIntegrationTest.java.

### Implementation for User Story 2

- [X] T011 [US2] Add the inspections-owned inference port and its infrastructure implementation for the configured YOLO service, with environment-bound settings and timeout/error mapping in backend/src/main/java/com/smartdroneinspection/inspections/spi/AiInferencePort.java, backend/src/main/java/com/smartdroneinspection/infrastructure/ai/YoloInferenceClient.java, backend/src/main/java/com/smartdroneinspection/infrastructure/ai/YoloInferenceProperties.java, and backend/src/main/resources/application.yml.
- [X] T012 [US2] Implement advisory candidate ingestion plus Inspector verification/manual-finding use cases; ensure only verified findings are official, using backend/src/main/java/com/smartdroneinspection/inspections/service/AiFindingService.java, backend/src/main/java/com/smartdroneinspection/inspections/repository/AiFindingCandidateRepository.java, backend/src/main/java/com/smartdroneinspection/inspections/repository/VerifiedFindingRepository.java, backend/src/main/java/com/smartdroneinspection/inspections/domain/AiFindingCandidate.java, and backend/src/main/java/com/smartdroneinspection/inspections/domain/VerifiedFinding.java.
- [X] T013 [US2] Add typed candidate-review/manual-finding DTOs and scoped controller operations in backend/src/main/java/com/smartdroneinspection/inspections/api/InspectionController.java, backend/src/main/java/com/smartdroneinspection/inspections/api/dto/request/ReviewFindingCandidateRequest.java, backend/src/main/java/com/smartdroneinspection/inspections/api/dto/request/CreateManualFindingRequest.java, and backend/src/main/java/com/smartdroneinspection/inspections/api/dto/response/AiFindingCandidateResponse.java.
- [X] T014 [US2] From backend/, run .\mvnw.cmd -Dtest=AiFindingServiceTest,AiFindingApiIntegrationTest test and record actual procedure, expected result, status, date, tester, and evidence for stable case WF3-003 mapped to FE-05 in docs/reports/report-5-test-report/01-test-cases/test-case-list.md and docs/reports/report-5-test-report/03-features/feature-2.md.

**Checkpoint**: FE-05 is testable using seeded evidence and a deterministic inference stub; AI failure preserves the manual path and no unverified candidate is official.

---

## Phase 5: User Story 3 — Review, Release, and Accept an Immutable Report (Sequence P3; SCRUM-88–SCRUM-90)

**Goal**: Build traceable report versions, enforce independent technical review and manager release, expose only released versions to Clients, and publish one accepted-report billing handoff.

**Independent Test**: Given seeded checklist responses, evidence, and verified findings, verify draft composition, append-only revisions, self-review denial, assigned-reviewer decisions, manager-only release, Client visibility/decision, accepted-version immutability, and idempotent handoff without running AI.

### Tests for User Story 3

- [X] T015 [P] [US3] Add failing report-service tests for draft composition, version snapshots, revision links, and accepted-version immutability in backend/src/test/java/com/smartdroneinspection/inspections/InspectionReportServiceTest.java.
- [X] T016 [P] [US3] Add failing API/security integration tests for self-review denial, reviewer assignment, manager release, Client draft/comment isolation, released-version evidence streaming, Client accept/revision, and duplicate acceptance handoff in backend/src/test/java/com/smartdroneinspection/inspections/InspectionReportApiIntegrationTest.java.

### Implementation for User Story 3

- [X] T017 [US3] Implement report draft composition and immutable version creation using existing WF3 entities and scoped repositories in backend/src/main/java/com/smartdroneinspection/inspections/service/InspectionReportService.java, backend/src/main/java/com/smartdroneinspection/inspections/domain/InspectionReport.java, backend/src/main/java/com/smartdroneinspection/inspections/domain/ReportVersion.java, backend/src/main/java/com/smartdroneinspection/inspections/repository/InspectionReportRepository.java, and backend/src/main/java/com/smartdroneinspection/inspections/repository/ReportVersionRepository.java.
- [X] T018 [US3] Implement version-bound peer review, manager release, Client accept/revision, and released-version evidence streaming with role plus resource-scope checks; persist the acceptance milestone without implementing invoice persistence in backend/src/main/java/com/smartdroneinspection/inspections/api/InspectionReportController.java, backend/src/main/java/com/smartdroneinspection/inspections/api/dto/request/PeerReviewDecisionRequest.java, backend/src/main/java/com/smartdroneinspection/inspections/api/dto/request/ClientReportDecisionRequest.java, backend/src/main/java/com/smartdroneinspection/inspections/api/dto/response/ReportVersionResponse.java, backend/src/main/java/com/smartdroneinspection/inspections/service/InspectionReportService.java, backend/src/main/java/com/smartdroneinspection/inspections/domain/PeerReview.java, and backend/src/main/java/com/smartdroneinspection/inspections/repository/PeerReviewRepository.java.
- [X] T019 [US3] Annotate inspections/events with @NamedInterface("events") and expose the accepted-report event through it; publish once after the acceptance transaction using existing Spring Modulith publication handling, with no evidence bytes/secrets or direct WF4 module calls, in backend/src/main/java/com/smartdroneinspection/inspections/events/package-info.java, backend/src/main/java/com/smartdroneinspection/inspections/events/ReportAcceptedEvent.java, and backend/src/main/java/com/smartdroneinspection/inspections/service/InspectionReportService.java.
- [X] T020 [US3] From backend/, run .\mvnw.cmd -Dtest=InspectionReportServiceTest,InspectionReportApiIntegrationTest test and record actual procedure, expected result, status, date, tester, and evidence for stable case WF3-004 mapped to FE-06 in docs/reports/report-5-test-report/01-test-cases/test-case-list.md and docs/reports/report-5-test-report/03-features/feature-2.md.

**Checkpoint**: FE-06 can be tested from seeded verified data; drafts/comments remain private, accepted versions cannot be overwritten, and one G4 handoff is observable.

---

## Phase 6: User Story 4 — Use the Workflow from Web and Mobile (Sequence P4; SCRUM-91/SCRUM-92)

**Goal**: Provide role-appropriate web report/inspection actions and mobile assigned-inspection checklist/photo capture with explicit validation, retry, and authorization states.

**Independent Test**: With API responses mocked or a seeded backend, verify permitted actions and loading/empty/error states on web, then assigned-inspector checklist/photo upload and retry behavior on mobile; confirm backend remains the authority.

### Tests for User Story 4

- [X] T021 [US4] Add @testing-library/react with its @testing-library/dom peer dependency and jsdom as frontend test-only dependencies; configure Vitest's DOM environment per the [Vitest environment guide](https://vitest.dev/guide/environment.html) and [React Testing Library installation](https://testing-library.com/docs/react-testing-library/intro/); then write failing inspection-page behavior tests for scoped evidence loading, upload errors, and retries in frontend/package.json, frontend/package-lock.json, frontend/vite.config.ts, and frontend/src/features/inspections/pages/InspectionsPage.test.tsx.
- [X] T022 [US4] After T021 establishes the shared DOM test environment, add failing report-page behavior tests for reviewer/manager/Client actions, hidden drafts, released reports/evidence, and decisions in frontend/src/features/reports/pages/ReportsPage.test.tsx.
- [X] T023 [P] [US4] Add Flutter repository/widget tests for checklist save, photo upload, retry feedback, and authorization failures in mobile/test/features/inspections/inspection_capture_test.dart and mobile/test/features/inspections/inspection_repository_test.dart.

### Implementation for User Story 4

- [X] T024 [P] [US4] Replace the inspection placeholder with typed API/query integration, scoped evidence preview, and Inspector evidence/candidate actions using frontend/src/features/inspections/api/inspectionApi.ts, frontend/src/features/inspections/hooks/useInspections.ts, and frontend/src/features/inspections/pages/InspectionsPage.tsx.
- [X] T025 [P] [US4] Replace the reports placeholder with typed version/review/release/Client-decision queries, released evidence preview, and role-appropriate states using frontend/src/features/reports/api/reportApi.ts, frontend/src/features/reports/hooks/useReports.ts, and frontend/src/features/reports/pages/ReportsPage.tsx.
- [X] T026 [P] [US4] Extend the existing mobile inspection model/repository for checklist and multipart evidence calls; add the smallest device photo-picker dependency only if none is already available, and regenerate rather than hand-edit generated files in mobile/lib/features/inspections/domain/models/inspection_evidence.dart, mobile/lib/features/inspections/data/inspection_repository.dart, mobile/pubspec.yaml, and mobile/pubspec.lock.
- [X] T027 [US4] Add assigned-inspection detail, checklist/photo capture, progress/error/retry UI and provider state in mobile/lib/features/inspections/presentation/inspection_detail_page.dart and mobile/lib/features/inspections/presentation/providers/inspection_detail_provider.dart.
- [X] T028 [US4] From frontend/, run npm.cmd test -- src/features/inspections/pages/InspectionsPage.test.tsx src/features/reports/pages/ReportsPage.test.tsx; from mobile/, run flutter test test/features/inspections/inspection_capture_test.dart test/features/inspections/inspection_repository_test.dart; add verified web/mobile procedure, status, date, tester, and evidence to docs/reports/report-5-test-report/03-features/feature-2.md without renaming the workbook sheet or stable WFx IDs.

**Checkpoint**: Web/mobile flows consume the frozen versioned API, show correct role-specific affordances and recovery states, and all security decisions remain server-side.

---

## Phase 7: Polish and Cross-Cutting Concerns

**Purpose**: Full WF3 regression, synchronize current documentation, and reconcile final Report 5 totals.

- [X] T029 Run the full G3/G4 WF3 regression using docs/development/plans/bach/2026-09-24-wf3-jira-task-completion/quickstart.md: from backend/, run .\mvnw.cmd verify; from frontend/, run npm.cmd test, npm.cmd run lint, npm.cmd run build; from mobile/, run dart format --set-exit-if-changed ., flutter analyze, flutter test; from docs/, run git diff --check and local-link review. Retain exact pass/fail/skip output and leave Failed cases visible until resolved or explicitly accepted.
- [X] T030 Synchronize tested behavior and contracts in docs/project-reference/business-flows.md and docs/backend/flows/inspections-and-reports.md; review docs/reports/report-3-software-requirement-specification/03-functional-requirements.md and 00-record-of-changes.md and update them only if implementation changes or clarifies product requirements; update docs/backend, docs/frontend, and docs/mobile contract guidance where the API/client contract actually changed, never restore docs/content/.
- [X] T031 Reconcile stable FE/WF mappings and detailed outcomes, recount Passed/Failed/Pending/N/A, validate totals/coverage, and append the report-history row in docs/reports/report-5-test-report/01-test-cases/test-case-list.md, docs/reports/report-5-test-report/03-features/feature-2.md, docs/reports/report-5-test-report/02-test-statistics/test-statistics.md, docs/reports/report-5-test-report/00-cover/cover.md, and docs/reports/report-5-test-report/00-cover/record-of-changes.md.

---

## Dependencies and Execution Order

### Phase dependencies

- **Setup (Phase 1)**: No work; repositories and tooling exist.
- **Foundational (Phase 2)**: T001 and T002 can proceed in parallel; both block story implementation.
- **US1 (Phase 3)**: Depends on T001–T002. T003/T004 tests precede T005–T007 implementation; T008 executes them and records FE-04 results.
- **US2 (Phase 4)**: Depends on the frozen contract and FE-04 evidence API/storage. T009/T010 tests precede T011–T013; T014 verifies/report-maps FE-05.
- **US3 (Phase 5)**: Depends on FE-04 evidence and FE-05 verified findings for the integrated journey. T015/T016 tests precede T017–T019; T020 verifies/report-maps FE-06.
- **US4 (Phase 6)**: Depends on stable backend contracts and endpoints from US1–US3. Web tests/implementation and mobile tests/repository work can proceed in parallel where marked; mobile detail UI follows T026.
- **Polish (Phase 7)**: T029 requires all stories; T030/T031 follow verified behavior and actual results.

### User story test dependencies

- **US1**: Seeded accepted assignment/in-progress inspection; independent of AI and reports.
- **US2**: Seeded persisted evidence; independent of live YOLO through a deterministic stub.
- **US3**: Seeded checklist/evidence/verified findings; independent of live AI.
- **US4**: Mocked or seeded API; verify web/mobile visible behavior, while server authorization is asserted by backend tests.

### Parallel opportunities

- T001 and T002 can proceed together.
- T003 with T004; T009 with T010; T015 with T016. T023 can run in parallel with T021; T022 follows T021 because it uses the shared React DOM test setup.
- After the backend contracts exist, T024, T025, and T026 can be assigned across web-inspections, web-reports, and mobile work; T027 follows T026.
- Do not parallelize tasks that edit the same API contract, InspectionController, InspectionReportService, application.yml, or Report 5 aggregate files without coordinating the shared edit.

## Parallel Examples

```text
After foundational T001–T002:
- T003 Evidence service tests
- T004 Evidence API tests

After FE-04 is complete:
- T009 AI/finding service tests
- T010 Candidate-review API tests

After FE-05 is complete:
- T015 Report lifecycle tests
- T016 Report authorization/handoff tests

After backend APIs are stable:
- T021 Web inspections tests
- T023 Mobile capture tests

After T021:
- T022 Web reports tests
```

## Implementation Strategy

### MVP first

1. Complete T001–T002.
2. Complete US1 (T003–T008): authorized evidence upload, MinIO/PostgreSQL consistency, retry safety, and FE-04 test evidence.
3. Stop and validate the FE-04 slice against WF3-001/WF3-002 before proceeding to AI or report work.

### Incremental delivery

1. Deliver FE-04 evidence slice and its truthful Report 5 record.
2. Add FE-05 candidate review/manual fallback and WF3-003 evidence.
3. Add FE-06 versioned report/review/release/acceptance and WF3-004 evidence.
4. Integrate web/mobile affordances and retry/error states.
5. Run G3/G4 regression, synchronize applicable docs, and close Report 5 totals/history.

## Notes

- Spec Kit task IDs T001–T031 are not Jira task IDs T025–T033.
- Keep the fixed Report 5 workbook sheet name Feature 2; WF3-001/WF3-002 map to FE-04, WF3-003 to FE-05, and WF3-004 to FE-06.
- Do not implement invoice persistence or payment gateway work under SCRUM-90; publish only the accepted-report handoff.
- Do not create a schema migration unless focused acceptance tests demonstrate a real V7 gap; if necessary, use a new forward migration and synchronize database documentation.
- Report 3 and Report 5 are requirements of the final feature handoff; Pending may describe tests not yet run but never claims completion.
