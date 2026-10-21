# MF1–MF4 Full-Flow E2E Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:subagent-driven-development` (recommended) or `superpowers:executing-plans` to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implement and verify one connected MF1→MF4 Enterprise SaaS lifecycle through Backend, Web and Flutter Web, using a disposable local stack and no direct database state changes between business steps.

**Architecture:** Backend contracts and transitions are implemented first, preserving the existing `AssetPairAssignment`, `Inspection`, `FieldSession`, MF3 report, and MF4 work-order aggregates. The Web client handles ORG_ADMIN setup/review/report governance; Flutter Web handles Inspector field work and Maintenance Engineer task work. A dedicated isolated Compose project and Playwright orchestration then run one lifecycle plus refusal paths. Database changes, when required, are forward-only migrations. Existing user changes in Backend and Docs are preserved and excluded unless explicitly part of a task below.

**Tech Stack:** Java 21, Spring Boot 4.1, Spring Modulith, PostgreSQL 17/Testcontainers, MinIO, Flyway; React 19, strict TypeScript, Vite, MUI, TanStack Query, Axios; Flutter 3.47.7/Dart 3.13.5, Riverpod, GoRouter, Dio, Freezed; Playwright for browser orchestration; Docker Compose isolated E2E project.

**Spec:** `development/plans/quoc/2026-10-20-mf1-mf4-e2e-design.md`; normative acceptance: Report 3 §3.3–§3.8 and `project-reference/business-flows.md` MF1–MF4.

## Global Constraints

- Preserve current user changes in Backend (`InspectionEvidenceApiIntegrationTest.java`, `.claude/worktrees/`) and Docs; never reset, overwrite, or stage unrelated files.
- Create new implementation branches from current fetched `origin/main` only after the user selects the plan execution method; keep each repository independent and record the selected merge order.
- Keep roles exactly `ADMIN`, `ORG_ADMIN`, `INSPECTOR`, `MAINTENANCE_ENGINEER`; derive user and tenant scope from authenticated principals, never request authority fields.
- Keep report author/reviewer, executing team/acceptor, and estimate/cost responsibilities separate per Report 3; no self-approval or self-acceptance.
- Never state that software pilots/arms a Drone or verifies legal permission, external issuer registry, professional qualification, real flight time, or telemetry it did not capture.
- E2E uses synthetic organization/users/files and local deterministic AI/report-draft adapters; no production/VPS, customer data, committed secrets, or external model calls.
- Use Flutter Web on Chrome as the agreed mobile-client E2E surface. Native Android camera/secure-storage behavior is a separate later device/emulator verification and must not be claimed here.
- E2E setup must use a unique project name, no fixed container names, distinct or dynamically mapped ports, unique network and unique named volumes; teardown may remove only that run's resources. Do not start/recreate/stop existing `smartdroneinspection-*` compose containers or volumes.
- All business transitions in the E2E scenario go through Web/Mobile/API. No SQL state seeding or updates between MF1 and MF4. Initial identity/bootstrap is the only environment setup shortcut allowed.
- Add/modify migrations only when the current task proves schema work is required; use a new forward-only migration, never edit V1–V35.
- Test-driven development: each behavior starts with a failing test. Run the affected suite, then the repository full checks before handoff.
- Preserve existing Report 5 case IDs and mapping. Never mark a test case `Passed` unless its full defined procedure ran; keep 11-case baseline (8 Passed/3 Pending) until cases are formally added and executed.
- No push, PR, merge, deployment, or external communication without a separate explicit request.

## Review Focus

1. **Tenant/assignment spoofing at every stage:** foreign IDs, guessed work-order/session/evidence IDs, and unassigned users must fail with stable scoped errors and no writes.
2. **MF1 pair atomicity and historical snapshot:** inactive Inspector/Drone, wrong organization, unavailable Drone, schedule conflicts, reassignment reason, and later asset-default changes must never produce a partial asset or rewrite a dispatched inspection.
3. **Readiness/session transition integrity:** stale/expired/invalidated readiness, concurrent starts, postpone/abort vs normal end, incomplete checklist, and duplicate end must not create false `FIELD_COMPLETED` or duplicate active sessions.
4. **Evidence/report provenance:** corrupt/oversized images, failed object storage, evidence-session mismatch, stale report snapshots, AI empty/failure/manual fallback, reviewer self-review, and publication failure must not leave partial or misleading official reports.
5. **MF4 evidence, costs and closeout:** before/after evidence pairs, unpriced estimate lines, pending/rejected change orders, wrong-currency actuals, missing work-log proof, acceptance/rework/reinspection, and cost reconciliation must gate completion/closure correctly.

---

## File responsibilities and cross-task contracts

### Backend (`SmartDroneInspection-Backend`)

- Modify `assets/domain/AssetPairAssignment.java`, `assets/service/AssetPairAssignmentService.java`, and the existing pair repository to expose the ORG_ADMIN asset-default-pair lifecycle. Keep it as one active default pair per asset; do not treat the pair response as an answer to every future inspection.
- Create an inspections-owned inspection-assignment aggregate/repository/service for dispatch, list, detail and response. Each inspection gets an independent Inspector/Drone/date/scope snapshot and response. Do not add a second asset-pair table.
- Add/modify pair DTO/controller under `assets/api/` for the default pair; add inspection create/dispatch DTOs/controllers/services under `inspections`; preserve MF3 endpoints and collection reads.
- Existing `asset_pair_assignments` rows start DRAFT and have `activate`, `suspend`, and `supersede`; this aggregate is the asset-level default pair. V28 adds nullable `assignment_response`/`responded_at` to that pair and fixes response vocabulary at `ACCEPTED`/`REJECTED`. Preserve the V28 constraint and legacy endpoint behavior for compatibility, but new MF1 dispatch must use a separate inspection-specific assignment aggregate: each inspection gets its own Inspector/Drone/date/scope snapshot and independent response. Do not use the asset-level response field to represent multiple inspection answers.
- Add normal completion to `FieldSession` and `InspectionFieldSessionService`/controller; completion records actor/time/result and transitions inspection to `FIELD_COMPLETED` only under the required checklist/session gates.
- Add inspection-scoped checklist-response API/service/repository if schema and current entity inventory show only read-side/persistence remnants. Do not invent new checklist tables if the existing `checklist_responses`, `ChecklistItem`, and `ChecklistTemplate` contract can be reused.
- Reuse existing `evidence.maintenance_work_order_id`, `maintenance_task_id`, and `EvidenceKind` (`BEFORE_MAINTENANCE`, `AFTER_MAINTENANCE`) for maintenance evidence. The current work-log request has no evidence IDs or finding/component pairing contract, so add typed evidence references and domain/service validation that the before/after records attach to the same work order/task/source finding. Add a forward migration only if the current schema cannot persist required pair identity/metadata; do not add a duplicate evidence table by default. Add deterministic completion-report draft contract only if the current manual report payload cannot satisfy MF4-15–17 workflow semantics while preserving manual fallback.
- Reuse `MaintenanceController`, `MaintenanceExecutionController`, `WorkOrderService`, `MaintenanceExecutionService`, `MaintenanceTestFixture`, and `MaintenanceApiIntegrationTest`; do not replace them wholesale.
- Add E2E environment assets under a dedicated path such as `e2e/compose.e2e.yml`, `e2e/.env.e2e.example` (no secrets), and scripts/test configuration. The E2E compose must have no `container_name`, distinct project/volume/network names, isolated ports, and no command that targets the existing compose project.

### Frontend (`SmartDroneInspection-Frontend`)

- Extend `features/assets/api/assetApi.ts`, `features/assets/hooks/useAssets.ts`, and `features/assets/pages/AssetsPage.tsx` for asset pair assignment and inspection creation/dispatch. Add feature-local dialogs/pages only where needed; keep TanStack Query server-state ownership.
- Extend `features/inspections/api/inspectionApi.ts`, `hooks/useInspections.ts`, and preparation/review pages for checklist/session-end display/action only if needed by the ORG_ADMIN flow; do not duplicate Inspector field execution UI on Web.
- Replace `features/maintenance/pages/MaintenancePage.tsx` placeholder with role-specific task/work-order views. Add maintenance API/types/hooks/components/tests under `src/features/maintenance/`; use shared Axios, Problem Details handling, existing UI kit and role navigation.
- Add Playwright config and E2E specs under a clearly named `e2e/` or `tests/e2e/` location; browser automation must consume only isolated E2E URLs and generated test credentials.

### Mobile (`SmartDroneInspection-Mobile`)

- Extend `features/inspections/data/inspection_repository.dart`, models/providers/pages for assignment→inspection navigation, preparation/checklist responses, and normal session end. Add Freezed/JSON model source only if the API contract needs it; regenerate generated files using build_runner.
- Replace `features/tasks/presentation/tasks_page.dart` placeholder with the assigned maintenance-work list; add task-detail/work-log/evidence UI and repository/providers under `features/tasks/` using Dio and Riverpod.
- Add API contract/repository tests and widget tests. Do not add unrequested MF1 admin management screens; MF1 setup remains Web-first by the approved design.
- Configure Flutter Web test build for Chrome; preserve native secure storage and camera behavior as out of scope for this browser run. Provide an explicit test-only camera/evidence input seam if browser plugin behavior is unavailable, and label it so it cannot be mistaken for native verification.

### Docs (`SmartDroneInspection-Docs`)

- Keep current MF1–MF4 inventory accurate in `project-reference/business-flows.md`, backend/frontend/mobile architecture, and `project-reference/database-design.md` when contracts/schema change.
- Add/update Report 3 requirement text and its record of changes for behavior/API/data changes.
- Add valid Report 5 case definitions only after executable procedures exist; update index, owning FE file, statistics, cover and record of changes; do not fabricate statuses.
- Preserve current uncommitted Docs changes. Do not overwrite or stage the pre-existing plans or `.claude/` content.

---

## Implementation Tasks

### Task 1: Build the disposable E2E environment and prove isolation

**Files:**
- Create: `SmartDroneInspection-Backend/e2e/compose.e2e.yml`
- Environment variables are generated into a run-local ignored temp file by `run-e2e.mjs`; no secret-bearing `.env.e2e` template is committed.
- Create: `SmartDroneInspection-Backend/e2e/scripts/start-e2e.*`, `stop-e2e.*` or one cross-platform orchestrator
- Modify: none in the existing default `docker-compose.yml`; E2E definition is a separate Compose file and must use generated project-specific resources
- Create: Backend E2E infrastructure smoke test

**Interfaces:**
- Produces a run identifier/project name `sdi-e2e-<run-id>` and isolated Postgres, MinIO, network and volumes.
- Produces base URLs for Backend (`/api/v1`), Frontend and Flutter Web and a readiness result.
- Teardown accepts only the exact run identifier created by start; it cannot fall back to the default compose project.

- [ ] **Step 1: Add an isolation test/static assertion** that parses the E2E Compose config and fails if any service has `container_name`, a volume/network name shared with current compose, or default fixed host ports `5432`, `9000`, `9001`, `8000`, `8080`, `80`.
- [ ] **Step 2: Run the isolation test** and verify it fails because the E2E compose file does not yet exist.
- [ ] **Step 3: Add the E2E Compose file** with unique project-scoped volumes/network, ephemeral/dedicated host ports, Postgres healthcheck, MinIO healthcheck and Backend/Web services built from current source. Use deterministic model/draft adapters; do not start AI inference or external providers.
- [ ] **Step 4: Add start/stop orchestration** that requires an explicit run id, waits by health condition, prints only URLs/status, and uses only the named E2E compose file/project. Stop/remove only containers and volumes belonging to that run.
- [ ] **Step 5: Run the isolation test and compose config validation**. Inspect `docker compose -f e2e/compose.e2e.yml -p sdi-e2e-plan config`; verify actual project names/ports and confirm existing `smartdroneinspection-*` containers/volumes remain unchanged.
- [ ] **Step 6: Review the isolated infra diff and record the local checkpoint.** Do not stage/commit without the user’s separate authorization.

### Task 2: Provision E2E identities and subscription through authorized APIs

**Files:**
- Inspect/modify Backend `subscriptions/domain/Subscription.java`, `SubscriptionRepository.java`, `SubscriptionEntitlementService.java`, `users/service/BootstrapAdministrator.java`, `users/api/PlatformUserController.java`, and subscription/user services.
- Create: typed ADMIN subscription request/response DTOs and integration tests; add a Frontend Platform Admin control only if Report 3 requires the product UI to expose activation, otherwise E2E uses the authorized platform API as environment setup.
- Modify E2E bootstrap/scripts from Task 1 to accept generated test emails/passwords via ignored run-local values and never print them.

**Interfaces:**
- Create the isolated Platform ADMIN using the existing E2E-only bootstrap configuration (`AUTH_BOOTSTRAP_ENABLED`, email and password); do not create it by SQL. Register the test organization and first ORG_ADMIN with the existing `POST /api/v1/auth/register` flow. Registration currently creates no subscription and must remain that way.
- Authenticate the disposable Platform `ADMIN`; add an ADMIN-authorized subscription create/activation API under the `/api/v1/platform/*` convention (proposed path: `POST /api/v1/platform/organizations/{organizationId}/subscriptions`) to create one ENTERPRISE subscription with allowed period (`1`, `6`, or `12` months), effective window, test reference/reason and actor/time audit. ORG_ADMIN cannot self-activate. Lock the exact path/replay behavior in RED tests before implementation.
- After activation, provision the Inspector and Maintenance Engineer using the existing ORG_ADMIN workforce API. Keep password material in process memory or run-local ignored configuration and pass it directly to role-specific browser contexts; never echo/store it in tracked files.
- Keep `Subscription` immutable to consuming modules; mutations belong to the subscriptions-owned service and ADMIN API. Ensure replay does not create multiple active subscriptions.

- [x] **Step 1: Add registration/onboarding integration test assertions** proving registration creates the organization/ORG_ADMIN but does not silently activate a subscription.
- [x] **Step 2: Add subscription ADMIN API tests** for activation, wrong role, unknown organization, invalid billing period/window, duplicate active subscription, audit actor/reason/time, reactivation after an ended term, and entitlement gating.
- [ ] **Step 3: Run focused tests** and observe absent activation contract/failure before implementation. (The integration suites compile but cannot start because Testcontainers cannot find Docker; no live RED result was observed.)
- [x] **Step 4: Implement the smallest subscriptions-owned service/controller/DTO contract**; do not make `Subscription` mutable from workforce/assets modules or create a public self-activation path. Reactivation locks the current ACTIVE row and expires/audits an ended term before creating its replacement.
- [x] **Step 5: Extend E2E bootstrap** to start Backend with the run-local Platform ADMIN bootstrap values, register the organization via API, authenticate ADMIN through login, activate entitlement through the new ADMIN API, and provision workforce through the ORG_ADMIN API. Fail before MF1 if any authorization or entitlement step is denied; never insert user or subscription rows directly.
- [ ] **Step 6: Run onboarding/entitlement integration tests and verify customer resource writes are denied before activation and allowed after. Record local checkpoint; do not stage/commit without separate authorization.** (Regression/API tests are present; execution is blocked before Spring context startup because Docker/Testcontainers is unavailable.)

**Task 2 checkpoint (2026-10-21):** `./mvnw.cmd '-DskipTests' test-compile` passed; `./mvnw.cmd '-Dtest=AssetPairAssignmentTest,ModulithArchitectureTest' test` passed 13 tests; the full E2E bootstrap/isolation Node suite passed 6 tests. `SubscriptionActivationApiIntegrationTest` and `OrganizationRegistrationApiIntegrationTest` remain unexecuted due to unavailable Docker. No changes staged or committed.

### Task 3: Add MF1 pair-assignment lifecycle on existing aggregate (asset defaults)

**Files:**
- Modify: Backend `assets/domain/AssetPairAssignment.java`
- Modify: Backend `assets/service/AssetPairAssignmentService.java`
- Modify: Backend `assets/repository/AssetPairAssignmentRepository.java`
- Create/modify: Backend pair request/response DTOs and `assets/api/AssetPairAssignmentAdminController.java`
- Create/modify: Backend `AssetPairAdminApiIntegrationTest` for asset-default pair create/activate/read/supersede
- Pair dispatch/response is implemented separately in Task 4’s inspection-owned assignment entity/API/tests

**Interfaces:**
- `POST /api/v1/assets/{assetId}/pair-assignments`: creates a DRAFT default pair with Inspector ID, Drone ID, `validFrom`, optional `validUntil`, and reason/effective scope; actor and organization derive from JWT.
- `GET /api/v1/assets/{assetId}/pair-assignments`: returns own-organization asset-pair history.
- `POST /api/v1/assets/{assetId}/pair-assignments/{pairId}/activate` (or one documented equivalent): validates the pair and makes it the one active asset default. Superseding/ending an active pair requires a reason; dispatched inspection snapshots are immutable.
- Responses are typed DTOs and reuse the `AssetPairAssignment` aggregate; no entity crosses the API. This API manages defaults only; Inspector response happens on a separate inspection-specific assignment API in Task 4.

- [x] **Step 1: Add API tests** for ORG_ADMIN success, wrong role, foreign asset/user/Drone, inactive/suspended Inspector, unavailable Drone, invalid dates, reason validation, history visibility, activation and supersession preserving old rows. API integration execution remains pending; the executed domain tests cover draft preparation and reason-preserving supersession. The API test also checks that a future-effective draft cannot be activated early and that an unentitled organization cannot create a pair.
- [ ] **Step 2: Run the focused pair API test** and observe the expected missing-route failures. (It now compiles, but no live RED result was observed; Testcontainers cannot find Docker.)
- [x] **Step 3: Implement pair default creation as DRAFT and explicit activation/supersession.** Do not publish DRAFT pairings into the Inspector inbox; only active, currently valid per-inspection dispatch records appear there. Do not write V28's pair-level `assignment_response` as part of inspection dispatch.
- [x] **Step 4: Add the smallest service/controller/DTO/repository changes** that satisfy those tests; re-check whether current schema supports default effective dates/history before deciding on a migration. If schema is inadequate, add a new forward migration and mapping tests rather than altering V25 or V28. Preserve V28's paired-null CHECK and ACCEPTED/REJECTED vocabulary. (The existing schema supports this slice; no migration was added.)
- [ ] **Step 5: Run the focused pair API test plus pair domain/service tests** and verify tenant non-disclosure, activation rules, and no cross-inspection response coupling. (Ten domain tests passed; API/tenant behavior is not verified because Docker is unavailable.)
- [x] **Step 6: Review the focused Backend diff and record a local checkpoint.** Do not stage or commit without separate user authorization.

**Task 3 checkpoint (2026-10-21):** Backend test compilation passed; `AssetPairAssignmentTest` and Modulith boundary tests passed 13/13. `AssetPairAdminApiIntegrationTest` could not start due to missing Docker/Testcontainers. No migration, staging, or commit.

### Task 4: Create MF1 inspections and dispatch from Web/API

**Files:**
- Create: Backend `inspections/domain/InspectionAssignment.java` (or equivalent inspection-owned immutable dispatch snapshot), repository, application service, request/response DTOs, and controller for dispatch/list/detail/respond.
- Modify: Backend `Inspection.java`, `InspectionRepository.java`, asset-pair access contract (do not import another module's `api/` package), `InspectionAssignmentApiIntegrationTest.java`, and `InspectionCreationApiIntegrationTest.java`.
- Modify: Frontend `features/assets/api/assetApi.ts`, `hooks/useAssets.ts`, `pages/AssetsPage.tsx`, `features/inspections/api/inspectionApi.ts`, `hooks/useInspections.ts`, `AssignmentInboxPanel.tsx` and their tests.

**Interfaces:**
- `POST /api/v1/inspections`: request includes `assetId`, objective, structured scope/component scope/acceptance criteria and `plannedStartAt`/`plannedEndAt`; organization/creator derive from JWT. The API resolves the active asset-default pair inside the organization and validates pair/Inspector/Drone eligibility and schedule conflict before creating an immutable inspection snapshot.
- A separate inspection-dispatch operation (e.g. `POST /api/v1/inspections/{inspectionId}/dispatch`) atomically creates the per-inspection assignment record, linking inspection, asset, source asset-pair ID, Inspector, Drone and effective dates. Dispatch verifies the inspection is draft and rechecks that the referenced default pair is eligible. Reassignment follows Report 3 §3.3.1: changing an asset default affects future inspections only; an inspection-specific reassignment or change to future defaults requires an explicit reason and immutable version/history. Do not invent a free Inspector/Drone selector outside that policy.
- The dispatch response returns inspection ID/status, immutable pair snapshot, a distinct inspection-assignment ID and assignment version.
- New `/api/v1/inspection-assignments/mine`, `/{inspectionAssignmentId}`, and `/{inspectionAssignmentId}/response` operations list/read/respond to per-inspection assignment records. The legacy pair-level response endpoint remains unchanged for compatibility and is not used by new dispatches.
- Web creates the draft inspection then confirms/dispatches it; never sends organization/actor authority fields.

- [ ] **Step 1: Add Backend tests** for valid draft creation, source asset and active-default validation, scope/date validation, duplicate cadence key, wrong tenant, unavailable pair/resources, and inspection snapshot immutability after asset-default changes.
- [ ] **Step 2: Run the focused integration suite** and confirm the create endpoint/operation is absent.
- [ ] **Step 3: Implement draft creation** using `Inspection`'s existing full constructor and current V25–V35 schema; derive org/creator and resolve the active asset default inside Backend.
- [ ] **Step 4: Add separate Backend dispatch API tests** for draft-only dispatch, assignment row created atomically with status transition, independent response fields, stale/changed pair rejection, explicit reason on allowed override, cross-tenant/role rejection, and repeated dispatch conflict without duplicate records.
- [ ] **Step 5: Implement inspection-specific assignment entity/service/controller** with a new forward migration (V36 or the next available version) only after confirming no existing schema can hold the record. Preserve the V28 pair response columns/constraints; update legacy assignment reads intentionally and retain the old pair-level endpoint contract.
- [ ] **Step 6: Add Frontend API/hook tests** for request serialization, create→detail state, dispatch mutation/cache invalidation, validation errors and preserving form data on failure.
- [ ] **Step 7: Implement the ORG_ADMIN inspection wizard** in existing Assets/Inspection surfaces; select the active asset-default pair, create a draft, show the snapshot, and require an explicit confirmation before dispatch. Backend remains authority.
- [ ] **Step 8: Run Backend creation/dispatch integration tests and Frontend relevant tests/lint/build.** Record local checkpoints only; do not stage/commit without separate authorization.

### Task 5: Implement checklist-response API and MF2 preparation navigation

**Files:**
- Inspect/reuse: Backend `ChecklistTemplate`, `ChecklistItem`, `checklist_responses`, `InspectionPreparationController/Service`.
- Create/modify: Backend checklist response DTO/controller/service/repository/tests only if no runtime writer currently exists.
- Modify: Mobile `inspection_repository.dart`, assignment inbox page, inspection detail page, providers, router and tests.

**Interfaces:**
- A scoped read endpoint returns the assigned inspection's current checklist template/items/version and existing responses.
- An Inspector-only write endpoint saves item responses/notes against the inspection and current checklist template/version; actor derives from JWT and assignment/tenant scope is enforced.
- Assignment cards expose a navigation action to `/inspection/:inspectionId`; successful accept refreshes assignment state without hiding the inspection route.

- [ ] **Step 1: Add API tests** for correct read/write, wrong assignment/tenant/role, stale template version, invalid answer type, and no partial update on validation failure.
- [ ] **Step 2: Run focused tests** and observe missing API or missing navigation behavior.
- [ ] **Step 3: Implement using existing checklist response storage**; do not create duplicate checklist tables. If schema cannot support session attribution/current version, document and add a forward migration with populated-database coverage.
- [ ] **Step 4: Add Mobile repository and widget tests** proving assignment→detail navigation, checklist load/save, response persistence/reload, failure state and preserved values.
- [ ] **Step 5: Implement the navigation and checklist UI** with Riverpod and existing GoRouter; keep errors retryable and label unsupplied device telemetry as absent.
- [ ] **Step 6: Run focused Backend and Mobile suites, then required Mobile analyze/format/tests. Record local checkpoints only; do not stage/commit without separate authorization.**

### Task 6: Add normal MF2 field-session completion and readiness-safe transition

**Files:**
- Modify: Backend `inspections/domain/FieldSession.java`, `Inspection.java`, `InspectionFieldSessionService.java`, `InspectionFieldSessionController.java`, response/request DTOs.
- Modify: Backend `InspectionFieldSessionServiceTest.java`, `InspectionFieldSessionApiIntegrationTest.java`.
- Modify: Mobile field-session repository/model/provider/panel/page/tests.

**Interfaces:**
- Add `POST /api/v1/inspections/{inspectionId}/field-sessions/{sessionId}/completion` (or use the repository’s chosen REST-equivalent path consistently) with final checklist outcome, collected coverage/limitations, observations/incidents and optional linked evidence references; actor/inspection/session scope derives from authenticated caller/resource.
- Completion closes only an `IN_PROGRESS` session, records actor/time/result, and transitions inspection to `FIELD_COMPLETED` in the same transaction only after required checklist/session data validates.
- Postponed and aborted sessions keep their distinct states/reasons and cannot be submitted as normally completed.

- [ ] **Step 1: Add RED service/API tests** for normal end, required final checklist/coverage, wrong Inspector/tenant, not-open session, repeated end, aborted/postponed session, missing readiness, and transaction rollback.
- [ ] **Step 2: Run the affected tests** and verify the expected absent-method/route failure.
- [ ] **Step 3: Implement domain transition and locked service operation** with inspection-first lock and refresh; keep no-actuation semantics.
- [ ] **Step 4: Add the API request/response/controller action** and tests proving `FIELD_COMPLETED` becomes visible to MF3 only after successful end.
- [ ] **Step 5: Add Mobile repository/widget tests then End session UI** with required summary/limitations and explicit server error when gates fail.
- [ ] **Step 6: Run affected Backend/Mobile suites and full relevant repository checks. Record local checkpoints only; do not stage/commit without separate authorization.**

### Task 7: Build a Web→Flutter Web Playwright E2E foundation

**Files:**
- Modify: Frontend `package.json`, `package-lock.json`, Vite configuration only if required, and create E2E config/spec/support files.
- Modify: Backend E2E scripts/config created in Task 1.
- Create: Flutter Web test entry/support route/provider overrides under Mobile test support if required.
- `vite.config.ts`: currently proxies `/api` to hard-coded `http://localhost:8080`; make the proxy target environment-configurable with the existing default unchanged (e.g. `VITE_API_PROXY_TARGET ?? 'http://localhost:8080'`) so the isolated E2E host port can be supplied without changing normal dev behavior.

**Interfaces:**
- One orchestration command starts only the isolated E2E project from Task 1, starts Backend/Web/Flutter Web, waits on health endpoints, then runs named Playwright stages; always writes a sanitized run summary and ensures cleanup is scoped to the E2E run ID.
- Flutter Web is launched with `--dart-define=API_BASE_URL=http://127.0.0.1:<mapped-backend-port>/api/v1`; the runner obtains the mapped port from the E2E environment output, not a fixed existing-stack port.
- Task 2's application-level bootstrap registers the organization, signs in the test Platform ADMIN and activates entitlement; subsequent test users are provisioned through the authenticated ORG_ADMIN workforce API. No raw token is logged or committed.

- [ ] **Step 1: Add a Playwright login/navigation smoke test** for Web and Flutter Web using the disposable users created through Task 2; assert health/UI and no external identity provider.
- [ ] **Step 2: Add integration/orchestration smoke test** that fails if the existing `smartdroneinspection-postgres`/MinIO container IDs or volumes change during the E2E start/stop cycle.
- [ ] **Step 3: Add one Playwright test dependency** to `package.json`/`package-lock.json` only after execution-plan approval; use the lockfile-pinned package and do not add another runner. Build Flutter Web and launch it with the runtime `--dart-define=API_BASE_URL` emitted by the E2E orchestrator; add a startup assertion that the URL is non-empty and points to the isolated run.
- [ ] **Step 4: Make Vite's `/api` proxy target configurable with the current `http://localhost:8080` default** and pass the E2E-mapped Backend URL through environment; assert ordinary `npm run dev` retains its existing default.
- [ ] **Step 5: Add deterministic local inference/draft adapter wiring** via test-profile config; tests assert requests never leave the local E2E network and responses carry stable synthetic provenance.
- [ ] **Step 6: Run smoke E2E on Web+Flutter Web** and verify cleanup leaves existing compose containers untouched. Record a local checkpoint; do not stage/commit without separate authorization.

### Task 8: Complete MF3 cross-client E2E bridge

**Files:**
- Modify/add Frontend report/evidence/findings APIs/pages/tests only for gaps found by E2E.
- Modify/add Mobile upload/quality APIs/pages/tests only for needed field steps.
- Modify Backend only if E2E reveals a confirmed API-contract or state-transition defect; write RED test first.

**Interfaces:**
- Require MF2 normal completion state and current accepted evidence quality before findings/report gates.
- Inspector findings confirmation is bound to current evidence/findings snapshot; ORG_ADMIN report review remains separate.
- Publish yields immutable PDF/checksum; post-publication corrective outcomes are separately recorded and then handed off; handoff itself creates no work order.

- [ ] **Step 1: Add Playwright stage test** that drives a completed inspection through evidence upload, accepted quality decision, deterministic inference/manual finding, finding confirmation, structured report draft, author verification/submission, independent ORG_ADMIN review/publication and PDF retrieval.
- [ ] **Step 2: Add post-publication tests** for corrective outcome, handoff/reasoned no-repair path and explicit assertion that handoff does not create a work order.
- [ ] **Step 3: Run each stage and inspect persisted/read-back values via UI and read APIs.**
- [ ] **Step 4: For each failure, trace UI request→API validation/authorization→service/transaction→storage/response; fix one root cause at a time with RED→GREEN regression tests.
- [ ] **Step 5: Keep `WF3-010/011/012` Pending unless their full Report 5 procedures are completed; add new valid cases only through the Report 5 mapping workflow.**

### Task 9: Implement maintenance evidence and completion-report contract gaps

**Files:**
- Modify/create Backend maintenance DTO/domain/service/controller/migration/test files under `maintenance/`.
- Use existing `MaintenanceApiIntegrationTest`, `MaintenanceWorkLog`, `MaintenanceReportVersion`, `MaintenanceCostLine`, and repositories.

**Interfaces:**
- Work-log actual evidence must identify evidence type (`BEFORE`, `DURING`, `AFTER`), target task/finding/component and object reference, with Backend proving the evidence belongs to the work order’s organization and source scope.
- Completion report can be generated through a deterministic local provider for integration; author can edit manually under same gates; structured cost totals are system-derived.
- No report may claim acceptance before the independent reviewer decision. Reinspection outcome must create/associate a new MF1 inspection or remain explicitly blocked; do not mark closure successful without the linked record where required. MF4-21 follow-up/warranty conditions must have an attributable persistence/readback contract; do not infer a warranty duration or claim a countdown when no supplied terms exist.

- [ ] **Step 1: Add RED API/domain tests** for `EvidenceKind.BEFORE_MAINTENANCE` and `AFTER_MAINTENANCE` records paired to the same task and source finding, foreign inspection/work-order/evidence rejection, missing proof blocking completion/report, structured actual-cost validation, report-draft provenance, author edit/submit, acceptance, reinspection linkage, and MF4-21 follow-up/warranty terms persistence/readback without fabricated default duration.
- [ ] **Step 2: Inspect V25 evidence columns (`maintenance_work_order_id`, `maintenance_task_id`, `kind`) and maintenance report snapshot fields.** Confirm which required pair/finding identity cannot be represented by those fields/JSON.
- [ ] **Step 3: Add a new forward Flyway migration only for a proven storage gap** (for example, a durable evidence→source-finding pairing); add clean and populated migration tests. If current fields and a typed JSON pair contract meet Report 3, do not create a migration.
- [ ] **Step 4: Implement minimum typed contracts/service checks and deterministic report-draft port**; preserve manual report fallback and keep costs calculated from structured lines.
- [ ] **Step 5: Run focused `MaintenanceApiIntegrationTest` cases and full Backend verify. Record a local checkpoint; do not stage/commit without separate authorization.**

### Task 10: Implement MF4 Web ORG_ADMIN work-order and acceptance workspace

**Files:**
- Create: Frontend `src/features/maintenance/api/maintenanceApi.ts`, `hooks/useMaintenance.ts`, work-order list/detail/forms/components and tests.
- Modify: `src/features/maintenance/pages/MaintenancePage.tsx`, route/navigation only if route structure requires it; `inspectionApi.ts`/MF3 corrective page for link to repair candidates only where necessary.

**Interfaces:**
- API methods/types match current Backend DTOs: list repair candidates/work orders; create order; assign team; inspect tasks/estimate/change/report/acceptance/reconciliation state; perform only ORG_ADMIN-owned decisions.
- ORG_ADMIN screens cover repair-candidate intake/triage/team/reviewer assignment, baseline/change approval, independent acceptance/rework/reinspection decision, cost reconciliation, and close. Backend remains authority.

- [ ] **Step 1: Add API-hook tests** asserting exact URLs/DTOs, cache invalidation, Problem Details handling and no actor/org fields.
- [ ] **Step 2: Add page/component tests** for loading/empty/error/retry, ORG_ADMIN actions, reviewer separation, missing evidence/cost gates and no premature close.
- [ ] **Step 3: Replace static placeholder with responsive work-order list/detail and workflow actions** using shared UI kit and existing feature conventions.
- [ ] **Step 4: Run maintenance tests, full Frontend Vitest, lint and production build. Record a local checkpoint; do not stage/commit without separate authorization.**

### Task 11: Implement MF4 Mobile Engineer task workflow

**Files:**
- Create: Mobile `lib/features/tasks/data/maintenance_repository.dart` (or keep data under existing feature `tasks`), domain models only as needed, Riverpod providers, detail/work-log/evidence widgets and tests.
- Modify: `lib/features/tasks/presentation/tasks_page.dart`, `app_router.dart`, `inspection_repository.dart` only if a shared maintenance navigation contract requires it.

**Interfaces:**
- `GET /api/v1/maintenance/work-orders` returns only current Engineer’s assigned team scope; task/detail endpoints remain backend scoped.
- Engineer can read own work orders/tasks, record task progress/hours/material actuals, upload/link before/during/after evidence, submit work logs and request a change; cannot approve estimates/changes, accept their own work or close orders.

- [ ] **Step 1: Add repository tests** for assigned order list/detail, task log payload, paired evidence refs, change request and scope/refusal responses.
- [ ] **Step 2: Add widget tests** for loading/empty/error, required fields, evidence pair gate, work-log submission and server refusal preservation.
- [ ] **Step 3: Implement task list and task detail UI** in existing `/tasks` route; add inspection/order deep links only after verifying route parameters and auth bootstrap behavior on Flutter Web.
- [ ] **Step 4: Check each existing plugin under Flutter Web. Use a clearly named test-only evidence file input seam if camera/gallery plugin cannot run on web; do not claim it verifies native camera.**
- [ ] **Step 5: Run `dart run build_runner build --delete-conflicting-outputs` only if model source changed; then run Mobile format/analyze/tests. Record a local checkpoint; do not stage/commit without separate authorization.**

### Task 12: Run and stabilize the full isolated MF1–MF4 Playwright journey

**Files:**
- Create: E2E orchestrator/spec/fixtures and sanitized report output under the E2E test locations agreed in Tasks 1 and 6.
- Modify only tests/config or confirmed production defects; never edit test expectations to accept broken behavior.

**Interfaces:**
- `npm run e2e:mf1-mf4` (or the single command selected in Task 1) starts isolated services, seeds only through application flows, runs browser contexts by role, stores screenshots/log summaries, and cleans its exact run resources.

- [ ] **Step 1: Add the happy-path test first** with named browser contexts `orgAdmin`, `inspector`, `maintenanceEngineer`, `independentReviewer`; preserve auth storage in-memory/test context and redact credentials from artifacts.
- [ ] **Step 2: Run the full journey only after Tasks 2–11 are locally integrated into one candidate baseline; fail fast at the first real API/client boundary if a prerequisite is missing. Never skip a stage with DB/manual state changes.**
- [ ] **Step 3: Drive MF1 create users/credentials/resources/asset-pair/inspection/dispatch. Assert new inspection-specific assignment appears in Inspector inbox with matching asset/pair snapshot; assert V28 pair-level response fields remain unchanged for the new dispatch.**
- [ ] **Step 4: Drive MF2 assignment response/preparation/permit link/readiness review/session start and end. Assert normal session end alone transitions to `FIELD_COMPLETED`.**
- [ ] **Step 5: Drive MF3 evidence/quality/findings/report/review/publication/corrective outcome. Assert the exact source snapshot, PDF checksum and handoff IDs through UI/read API.**
- [ ] **Step 6: Drive MF4 work-order/team/task/estimate approval/release/work logs/paired evidence/change if needed/completion report/independent acceptance/cost reconciliation/MF4-21 follow-up record/close. Assert `CLOSED`, required corrective scope resolved, and linked report/findings/evidence; do not fabricate a warranty term.**
- [ ] **Step 7: Run negative-path test contexts** for foreign tenant, unassigned Inspector/Engineer, self reviewer/acceptor, stale readiness, invalid state, missing before/after proof, unapproved cost/change, and close before all gates. Assert stable errors and no partial mutation.
- [ ] **Step 8: Run the journey twice against fresh E2E run IDs** to prove cleanup/repeatability; compare existing compose container/volume IDs before and after.
- [ ] **Step 9: Fix each confirmed defect one at a time with a regression test; rerun failed stage and full E2E. Never bypass a gate with SQL or fixed IDs.**
- [ ] **Step 10: Collect sanitized logs/screenshots and publish only local artifact/report outputs. Tear down only the E2E project and verify user’s existing local services/data are still running and unchanged.**

### Task 13: Synchronize docs and Report 5 evidence

**Files:**
- Modify Report 3 `03-functional-requirements.md` and `00-record-of-changes.md` for behavior/API/schema decisions.
- Modify `project-reference/business-flows.md`, `database-design.md`, stack architecture/API docs.
- Modify Report 5 `01-test-cases/test-case-list.md`, owning FE-02/03/04/05/06/07 sources, `02-test-statistics/test-statistics.md`, cover and change history. Preserve exactly eight FE files and stable reserved IDs.

**Interfaces:**
- New test IDs must use FE mapping and workflow IDs agreed with Docs before writing procedures. Existing removed `WF4-*` IDs remain reserved; do not reuse them without explicit product-owner decision.
- Case `Passed` means its full written procedure ran on the final source with evidence; supporting tests stay supporting evidence and do not change WFx status automatically.

- [ ] **Step 1: Map each new cross-layer acceptance scenario to an existing stable ID or propose new non-conflicting IDs in Docs before execution.**
- [ ] **Step 2: Record full procedures/preconditions/expected results/evidence/date/tester in the owning FE file and mirror each case in the index.**
- [ ] **Step 3: Recount all eight feature summaries, statistics, coverage formulas; verify totals equal case rows.**
- [ ] **Step 4: Update Report 3 SRS/change record and business/data/API/stack docs for every changed contract or schema rule.**
- [ ] **Step 5: Run exporter unit tests and `git diff --check`; do not regenerate or modify the supplied workbook template unless separately requested.**

### Task 14: Final verification and independent review

**Files:** all changed files in the four independent repositories; no changes to user-owned untracked data.

- [ ] **Step 1: Backend:** Java 21 + Docker, `./mvnw.cmd clean verify`; record exact test count, Spotless, JaCoCo and Modulith result.
- [ ] **Step 2: Frontend:** `npm run lint`, `npm run build`, `npm test -- --maxWorkers=2`, and isolated E2E command; record pre-existing warnings separately.
- [ ] **Step 3: Mobile:** format check, `flutter analyze`, `flutter test`, Flutter Web build/test and E2E; native Android remains explicitly unverified.
- [ ] **Step 4: Docs:** `git diff --check`, link/path validation and Report 5 exporter tests; Hugo only if available.
- [ ] **Step 5: Review each repo diff and staged diff** for unrelated files, generated files, IDs/status drift, credentials/test data, and cross-repo contract mismatch.
- [ ] **Step 6: Request one independent review of the final implementation** and resolve Critical/Important findings with RED→GREEN tests.
- [ ] **Step 7: Hand off exact changed paths, branch/commit state, commands/results, full-flow E2E evidence, remaining native-device gaps, and any user-owned files left untouched.** No push/PR/merge/deploy until separately requested.

## Execution order and cross-repository integration

1. Task 1 proves isolated stack safety; Task 2 adds authorized disposable subscription activation so resource writes can execute without SQL seeding.
2. Task 3 creates/activates asset defaults and per-inspection assignment lifecycle; Task 4 creates/dispatches inspections and adds the ORG_ADMIN Web setup UI.
3. Task 5 implements checklist responses and Flutter assignment navigation; Task 6 implements normal field-session completion and `FIELD_COMPLETED`.
4. Task 7 builds Playwright/Flutter-Web smoke infrastructure only after API URL injection and plugin compatibility are verified.
5. Task 8 closes and tests the MF3 handoff bridge; Task 9 closes any MF4 evidence/report/reinspection API gaps confirmed by tests.
6. Tasks 10/11 integrate the existing MF4 APIs into Web/Flutter clients.
7. Task 12 runs the full E2E only after all preceding API/client tasks are locally integrated into one candidate baseline. Task 13 synchronizes requirement/test documentation; Task 14 runs final checks and independent review.

Keep repositories independent. Backend contracts/schema tasks precede Frontend/Mobile contract clients; E2E requires the compatible branches combined locally in a disposable candidate baseline. Docs changes follow confirmed API/behavior contracts. Do not merge shared `main`, push, PR, or deploy as part of this plan without a separate user instruction.
