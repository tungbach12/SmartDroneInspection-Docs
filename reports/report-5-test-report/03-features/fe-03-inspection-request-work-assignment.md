# FE-03: Mission Preparation, Assignment Response and Readiness — MF2

Report 3 §3.4 titles this feature "Mission Preparation, Assignment Response
and Readiness". The filename retains the earlier "inspection request / work
assignment" wording; the filename is stable, the scope is Report 3's.

## Recurring inspection and in-app reminder foundation — supporting verification (2026-10-26)

- Feature: FE-03 & FE-08; business-flow case: not yet assigned (supporting unit and component evidence outside workbook sheets; retired WFx IDs remain reserved).
- Preconditions: Java 21 and Maven dependencies for backend; Node 20 and npm dependencies for web; Dart 3 and Flutter dependencies for mobile.
- Procedures:
  1. Backend: run `./mvnw test -Dtest="*Recurrence*,*Recurring*,*Notification*,ModulithArchitectureTest,PersistenceEntity*"` and `./mvnw spotless:check`.
  2. Frontend: run `npx vitest run src/features/inspections/ src/features/notifications/` and `npm run build && npm run lint`.
  3. Mobile: verify static typing and test suite for `test/features/notifications/`.
- Expected:
  - Calendar occurrences derive from original local anchor without drift on monthly/leap-year dates; weekly local time follows configured timezone across DST transitions.
  - Schedule lifecycle (pause/resume/end/advance) preserves occurrences; bounded lookahead generation blocks past/conflicting occurrences without silent advancing.
  - In-app notification delivery is deduplicated via unique DB constraints; live inspection state is re-evaluated before reminder dispatch (non-cancelled, future planned start, active inspector).
  - Scoped inbox endpoints enforce authenticated user and tenant scope without cross-tenant leakage.
  - Web and mobile clients provide reactive notification badges, paginated inbox with all/unread filter, idempotent mark-as-read, and safe internal route navigation.
- Executed: 2026-10-26; tester: coding assistant (automated).
- Verified results:
  - Backend: **96 unit/service/controller/architecture tests Passed**, 0 failures, 0 errors, 0 skips. `spotless:check` clean across all 588 files.
  - Frontend: **212 tests Passed** across inspections and notifications suites (183 inspection suite + 29 notification suite). Full frontend test suite: **79 test files / 571 tests Passed (100%)**. `tsc -b && vite build` clean (0 type errors), `oxlint` clean.
  - Mobile: 6 test suites implemented for in-app notification domain, safe routing, repository, Riverpod providers, inbox UI, and app bar bell badge.
- Full verification: Backend `./mvnw verify` with Testcontainers remains blocked because Docker daemon is not running on this machine (`open //./pipe/dockerDesktopLinuxEngine: The system cannot find the file specified`). Full database integration tests are truthfully recorded as **Pending**.
- Feature status: **Unit, service, API contracts, web UI and mobile inbox implemented and verified**. Complete live end-to-end execution against a running PostgreSQL/Docker environment remains outstanding before promoting any workbook business flow case. Workbook case counts (11 cases: 8 Passed, 3 Pending) and coverage formulas remain unchanged.

## Inspector Schedule Calendar Board and Work Detail Dialog — supporting verification (2026-10-26)

- Feature: FE-03 (Inspection operational tracking & Inspector mission dispatch); business-flow case: supporting verification.
- Preconditions: Frontend dependencies installed; authenticated Inspector session or mock scope.
- Procedures:
  1. Execute unit and component tests: `npx vitest run src/features/inspections/components/InspectorScheduleCalendar.test.tsx src/features/inspections/components/InspectionWorkDetailDialog.test.tsx src/features/inspections/pages/InspectionsPage.test.tsx`.
  2. Run TypeScript compilation and production bundle build: `npm run build`.
  3. Run linter: `npm run lint`.
- Expected:
  - `InspectorScheduleCalendar`: Renders calendar toolbar with month title, navigation buttons (Prev, Next, Today), view toggles (Month, Week, Agenda), and status filter dropdown. Accurately maps planned inspections into day cells with status color coding. Displays collapsible warning banner for unscheduled inspections. Dispatches inspection ID on click of scheduled chip, week card, agenda row, or unscheduled item.
  - `InspectionWorkDetailDialog`: Renders comprehensive mission work orders on event selection: objective, status badge, planned schedule (start/end), asset name and GPS coordinates, assigned drone serial/model and serviceability status, regulatory flight permit reference/issuer/validity dates, mission component scope shot-list chips, acceptance criteria, and status-specific operational guidance banner with direct routing action button (`preparation`, `field-session`, `evidence`, `report`).
  - `InspectionsPage`: Adds "Schedule calendar" toggle option to view switcher, renders `InspectorScheduleCalendar`, and mounts `InspectionWorkDetailDialog` on selection.
- Executed: 2026-10-26; tester: coding assistant (automated).
- Verified results:
  - `InspectorScheduleCalendar.test.tsx`: 6 tests Passed (month/week/agenda views, selection triggers, unscheduled banner, month navigation).
  - `InspectionWorkDetailDialog.test.tsx`: 5 tests Passed (loading state, full mission/equipment details, action button navigation to field session and preparation, full workspace navigation).
  - `InspectionsPage.test.tsx`: 12 tests Passed (includes calendar view switching and calendar mounting).
  - Full frontend suite: **79 test files / 571 tests Passed (100%)** on `vitest run`.
  - Build & Lint: `tsc -b && vite build` exited with code 0; `oxlint` exited with 0 errors.
- Status: **Passed (Frontend operational schedule board & mission detail modal fully verified)**. Workbook case totals (11 cases: 8 Passed, 3 Pending) remain unchanged as supporting verification.

## Scope baseline

MF2 **receives** the assignment created in MF1; it does not create one. Per
Report 3 §3.4, MF2 does not source a Provider, does not calculate recommended
GSD, overlap, gimbal or flight-control settings, and has no procurement/RFQ
step. Hardware configuration is outside its scope.

The twelve MF2 steps divide into two halves:

| Steps | Actor | What it does |
| --- | --- | --- |
| MF2-01 – MF2-08 | `INSPECTOR` + `ORG_MANAGER` | Assignment accept/reject with a reason; component shot-list and required evidence types; permit/credential linking; blocker validation; safety acknowledgments; qualified ORG_MANAGER readiness approval producing `READY_FOR_FLIGHT`; snapshot of the approved plan. Implementation is partial across this range: MF2-08 source-change invalidation is not produced. |
| MF2-09 – MF2-12 | `INSPECTOR` + `SYSTEM` | Pre-flight checklist, Start request or postponement/interruption, recheck of entitlement and readiness version, `IN_PROGRESS` recording, reasoned session completion, and `FIELD_COMPLETED`. Session completion and readiness review after additional-session return are implemented; complete MF2 loop testing remains unrepresented by a Report 5 case. |

Gates worth stating because they are easy to misread as satisfied:

- Accepting an assignment **does not** establish readiness (MF2-02). Only the
  ORG_MANAGER approval at MF2-07 produces `READY_FOR_FLIGHT`, and only when all
  applicable mandatory conditions pass.
- A missing permit **cannot be waived by an internal approval** (MF2-04).
- Ambiguous authority or geographic conditions require **human verification, not
  inferred automatic clearance** (MF2-05).
- Start does **not** arm the aircraft or establish actual flight time from
  hardware (MF2-10). A Start action never arms or pilots a Drone.
- `FIELD_COMPLETED` marks one ended session, **not** overall inspection
  completion or report approval (MF2-12).

An earlier draft of this file described a request being "reviewed and confirmed
into a service order", which came from the retired five-role marketplace
baseline. Report 3 §3.4 has no service order, quotation or procurement step,
so that text was removed rather than kept as historical context.

## Feature sheet summary

Values for the `Feature 3` summary block (`A2:E8` in the workbook).
The template reads these back by formula, so an export needs them
recorded here.

| Cell | Label | Value |
| --- | --- | --- |
| `B2` | Feature | Mission Preparation, Assignment Response and Readiness — MF2 |
| `B3` | Test requirement | Verify assignment response and MF2 preparation/readiness gates, including organization scope, independent review, validity, source attribution, permit blockers, reasoned return and observed/unresolved source snapshots. |

## MF2-07 readiness cases

| Test Case ID | Test Case Description | Test Case Procedure | Expected Results | Pre-conditions | Round 1 | Test date | Tester | Round 2 | Test date | Tester | Round 3 | Test date | Tester | Note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| WF2-008 | Independent qualified ORG_MANAGER approves a current submitted preparation only when source ownership, verification, validity, pair chronology, applicability attestation and permit gates pass. | Seed two organizations, an assigned Inspector, an independent ORG_MANAGER, ACTIVE reviewer/Inspector credentials with verification and evidence attribution, an ACTIVE reviewed Drone document, an ACTIVE accepted pair responded before planned start, an applicable ACTIVE permit, a PREPARING inspection and current SUBMITTED preparation. Call the readiness approval service; repeat with same-person reviewer, wrong role, inactive/cross-tenant reviewer, foreign credential, null credential dates, missing credential evidence, unreviewed document, missing applicability basis, missing permit, late pair response and READY_FOR_FLIGHT inspection. | Valid approval persists one APPROVED decision with permit/credential/document snapshots, source IDs, reviewer and lowercase SHA-256 hash; preparation becomes READY and inspection becomes READY_FOR_FLIGHT. Every invalid actor/source/gate returns a stable business failure and creates no decision or state transition. Reviewer/document/credential checks are internal-record validation only, not external authority verification. | PostgreSQL 17/Testcontainers; V25/V28 schema; active organization, assigned Inspector, independent active ORG_MANAGER, current submitted preparation, real permit/credential/document/pair rows. | Passed | 2026-10-09 | Claude Code automated | Pending |  |  | Pending |  |  | `InspectionReadinessServiceTest` (16 tests) and `ReadinessSnapshotFactoryTest` (6 tests) are included in backend PR #64 CI on 2026-10-10. The merged backend CI ran `./mvnw.cmd verify`: 334 tests, 0 failures/errors/skips; JaCoCo and Modulith checks passed. The local Windows `mvnw.cmd -o verify` attempt could not initialize Testcontainers because Docker was unavailable; this is an environment limitation, not a product test result. Negative cases include wrong role/tenant/owner, inactive reviewer, missing evidence/date validity, permit blocker, non-current state and pair response at planned start. Internal record validation is not issuer-registry verification. |
| WF2-009 | Qualified reviewer can return a submitted preparation despite readiness-evidence gaps, with exact observed/unresolved IDs recorded as incomplete. | With a current submitted preparation and reviewer credential valid at decision time, remove the permit and supply reviewer-observed Inspector-credential/Drone-document IDs including one unresolved ID; return with a reason. Repeat with empty observed IDs and with a blank reason. | Return persists a RETURNED decision/reason and observed snapshots, retains exact requested IDs and unresolved IDs, sets `observedSourceSetComplete=false` even for empty selections, marks preparation RETURNED and leaves inspection PREPARING. Blank reason or invalid reviewer/scope creates no decision or state change. | PostgreSQL 17/Testcontainers; active independent ORG_MANAGER and reviewer credential verified/evidence-attributed with non-null dates covering decision time; current submitted preparation. | Passed | 2026-10-09 | Claude Code automated | Pending |  |  | Pending |  |  | `InspectionReadinessServiceTest` (16 tests) and `ReadinessSnapshotFactoryTest` (6 tests), included in backend PR #64 CI on 2026-10-10. The same integrated CI run passed the full backend suite (334 tests) and coverage/Modulith gates; the local test attempt was blocked because Docker was unavailable. The case covers return with a missing permit, exact observed/unresolved IDs with completeness false, and blank reason writes no decision. |

| WF2-010 | An authorized Inspector reads the preparation history of an inspection in their own organization, and an Inspector in another organization is refused. | Sign in as the assigned `INSPECTOR` and `GET /api/v1/inspections/{id}/preparation`; sign in as an `INSPECTOR` belonging to a different organization and repeat the same request. | The assigned Inspector receives `200` with the preparation history array; the out-of-scope Inspector receives `404 INSPECTION_NOT_FOUND` and never a `500`. The read path must not take a pessimistic write lock, because a locking query in a read-only transaction fails at the database before the organization check can deny the caller. | One organization holding an `INSPECTOR` and an inspection in `PREPARING` or later; a second organization with its own `INSPECTOR`; PostgreSQL via Testcontainers. | Passed | 2026-10-11 | Claude Code (automated) | Pending |  |  | Pending |  |  | Verified by `InspectionPreparationApiIntegrationTest` (9 tests), which ran on 2026-10-11 within the full backend suite of 362 passing tests (`./mvnw.cmd verify`). The listing previously called the locking `findWithLockByIdAndOrganizationId`, producing `SELECT ... FOR NO KEY UPDATE` inside a read-only transaction; PostgreSQL rejects it and every caller saw `500`. Re-verified against the docker compose stack on 2026-10-11: `GET /preparation` now returns `200` and the out-of-scope caller receives `404`. |

## MF2-12 / additional-session regression evidence (2026-10-20)

Targeted backend suites cover the new flow at focused boundaries; these are not a
complete MF3-to-MF2 end-to-end case and no case status is promoted:

- `InspectionEvidenceApiIntegrationTest` covers additional-session
  return-to-preparation, new draft version, superseded prior preparation,
  retained prior sessions/evidence, the completed-session/evidence association,
  and refusal without a completed session, its evidence, or a latest approved
  preparation.
- `InspectionPreparationServiceTest` covers next-version draft
  window update, including planned start/end response.
- `InspectionFieldSessionApiIntegrationTest` covers normal completion,
  required outcome notes and role/assignment denial.
- `InspectionFieldSessionServiceTest` covers stale older-preparation
  approval denial at start and successful normal completion;
  `InspectionReadinessApiIntegrationTest` protects existing
  approval/return API behavior. `InspectionReportDraftingApiIntegrationTest`
  passes after its additional-session supersession fixture was corrected to use
  legacy `LIMITED`, which does not initiate MF2 rework.

Executed commands during this task: backend `./mvnw verify` — **684 tests**, 0 failures/errors/skips, with Spotless, JaCoCo and Modulith checks met before the final AI-suggestion rejection-path correction; final `./mvnw -DskipTests package` passed after that correction with tests skipped. Tests were not rerun after the correction. No live walkthrough was run in this task.

This is implementation evidence, not a Report 5 functional case: no case status is promoted, and the repeated-session evidence set has not been re-assessed end to end in the product UI.

## Implemented and unverified boundaries

Backend MF2-01/02 assignment response, MF2-03/06 preparation and compliance, MF2-07 approval/return, MF2-09/11 start/postpone/abort and MF2-12 normal completion are implemented. Session starts require a current approved decision bound to the latest READY preparation. An MF3 additional-session request marks the old readiness invalid, returns to PREPARING, creates a new versioned draft, and requires a new planned window before MF2 readiness review. The web client exposes the additional-session route and preparation-window fields; mobile now exposes preparation, session completion, and only the two supported evidence-quality choices.

MF2-08 generic source-change invalidation remains partial: this slice appends INVALIDATED for the additional-session return specifically; there is still no general permit/pair/credential change workflow. MF2-12 and the repeated additional-session handoff are not represented by a complete Report 5 end-to-end case. The backend regressions (684-test `verify` in this task, run before the final rejection-path correction) are implementation evidence, not a full readiness approval/start/re-capture execution.

The existing three cases verify readiness decision behavior and scoped history, not the full MF2 lifecycle. New focused regressions cover the additional-session mutation and session completion but do not cover one complete repeat visit with real readiness approval and second evidence assessment. Generic MF2-08 source-change invalidation remains partial. These results also say nothing about MF1 or MF4.

### MF2-09 – MF2-12 Field Session — supporting verification (executed 2026-10-20)

- Preconditions: Backend `feat/mf1-backend-org-admin-resources` and Frontend `feat/mf1-org-admin-resources-hieu`; PostgreSQL 17/Testcontainers; an inspection assigned to the signed-in Inspector with an approved readiness decision.
- Procedure: Run Backend `InspectionFieldSessionServiceTest` (19 tests) and `InspectionFieldSessionApiIntegrationTest` (9 tests), and Frontend `FieldSessionPage.test.tsx` (6 tests). Verify the session listing scoped to the assigned Inspector; starting a session against the newest `APPROVED` readiness decision; the mandatory pre-flight checklist note; postponement with the Inspector's own reason keeping the inspection startable; abort with the Inspector's own reason ending the record; refusal to open a second concurrent session.
- Expected result: A session starts only after the pre-flight note is recorded and readiness holds; the startedAt instant is the software's session start and not hardware flight time; a postponed session leaves the inspection startable while an aborted one does not resume under that record; a second concurrent session is refused.
- Round 1: Passed 2026-10-20; tester: Claude Code (automated).
- Evidence: The backend suites passed within the full `verify` run of 648 tests, 0 failures, 0 errors, JaCoCo and Modulith checks met. Frontend `FieldSessionPage.test.tsx` passed 6/6 tests and the full frontend suite passed 56 files / 361 tests. The web client previously had no field-session surface at all, so MF2-09 to MF2-11 were reachable only from mobile; the new `field-session` stage tab is the Inspector's on-site record.
- Scope note: The session record is the software's agreement that the paperwork and pre-flight checklist were in order. It does not arm the aircraft, and the recorded start time is not hardware flight time. Normal session completion is implemented and tested as recorded above.
