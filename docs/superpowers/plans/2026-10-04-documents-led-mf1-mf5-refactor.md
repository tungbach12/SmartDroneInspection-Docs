# Documents-Led MF1–MF5 Refactor Implementation Plan

> **⚠️ SUPERSEDED (06 Oct 2026).** The business contract was revised after this plan was written: settlement is now **direct bank transfer with no platform custody** (`project-reference/business-flows.md` v3.3). Advance funding, payment-partner ports/settlement tasks (notably Task 4.2), dispute holds and warranty retention are **void**. Scope also narrowed: **MF2 and MF5 application code is out of scope** — database schema only, and no frontend/mobile code for MF2/MF5. Execution continues on branches `refactor/simplified-flow-db` (migrations) and `refactor/simplified-flow-docs` (documents); the `refactor/mf1-mf5-*` worktree branches are abandoned. This document is retained as historical context only — do not execute its remaining tasks without re-planning against the current contract.

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:subagent-driven-development` (recommended) or `superpowers:executing-plans` to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Refactor the backend, frontend, mobile client, database schema, and project documentation from the implemented v1 WF1–WF4 baseline into the documents-defined six-role, multi-provider MF1–MF5 target without inventing a separate maintenance-manager role or claiming unimplemented integrations are complete.

**Architecture:** Preserve the Spring Modulith modular-monolith shape and feature ownership, but align identity, actor zones, provider organizations, capability-specific vetting, workflow state, and authorization with the target documents. Deliver the refactor in vertical phases: establish canonical identity and Supporting Flow first, then MF1/MF2, MF3, MF4, MF5, and finally synchronize web/mobile clients and evidence documentation. Use additive/forward migrations and explicit compatibility bridges where the v1 schema or API cannot be changed atomically.

**Tech Stack:** Java 21, Spring Boot 4.1, Spring Modulith 2.1.1, Spring Data JPA, PostgreSQL, Flyway, MinIO, React 19, TypeScript 6, Vite, Vitest, Flutter/Dart 3.13, Riverpod, Dio, GoRouter, Freezed/json_serializable.

**Spec:** `docs/docs/superpowers/specs/2026-10-04-documents-led-mf1-mf5-refactor-design.md`

## Global Constraints

- The current source and migrations are the v1 implementation baseline; the target documents are the product contract.
- The target has exactly six canonical roles: `PLATFORM_ADMIN`, `PLATFORM_OPERATOR`, `CLIENT`, `PROVIDER_MANAGER`, `INSPECTOR`, `MAINTENANCE_ENGINEER`.
- Provider capability is organization eligibility data, not a role; “both” means two independent capability records.
- `PROVIDER_MANAGER` remains the single Provider Organization representative; do not create `MAINTENANCE_PROVIDER_MANAGER`.
- Supporting Flow contains organization registration, Provider vetting, asset master data, and recurring schedule setup; Main Flows are MF1–MF5.
- PostgreSQL is the transactional source of truth; MinIO stores file bytes and PostgreSQL stores authorized object metadata.
- Never rewrite an applied Flyway migration; use forward migrations and auditable, idempotent backfills.
- Successful JSON responses use `{ success, message, data }`; errors use RFC 9457 Problem Details with stable code and trace ID.
- Backend authorization enforces organization, Provider, ownership, assignment, release, and separation-of-duties scope; UI guards are not security.
- The Platform does not pilot drones, custody deposits, or issue legal arbitration awards.
- Target payment-partner, airspace/permit, settlement, hold, and retention integrations are not marked implemented without real adapters and integration evidence.
- Existing v1 Report 5 WFx IDs and historical outcomes remain stable; new target tests remain `Pending` until actually executed.
- Never stage or commit unrelated work, generated files, secrets, `.env`, or the pre-existing docs files `slide2_context.md` and `slide4_actors_functions.pptx`.
- Use isolated feature branches/worktrees for implementation. Do not push, open a PR, merge, deploy, or send external messages without explicit authorization.

## Review Focus

1. **Legacy role-value migration:** old `ADMIN`/`SERVICE_MANAGER` values must not be silently reinterpreted; test the exact mapping and revocation behavior before changing authorization.
2. **Provider capability independence:** verifying inspection must not verify or unlock maintenance, and vice versa; test the four combinations (neither, inspection only, maintenance only, both).
3. **Cross-organization and assignment scope:** every read/write must scope from the authenticated principal before loading a record; test same-role foreign-organization access and unassigned workforce access.
4. **Target-only integrations:** unsupported payment, airspace, settlement, hold, and retention paths must fail closed and preserve the accepted order/report state; test configured versus unavailable adapters.
5. **Client contract drift:** backend envelope/error/role changes must remain decodable by web and mobile clients during the migration; run contract fixtures against all three clients.

---

## Phase 0 — Worktree, baselines, and contract inventory

### Task 0.1: Create isolated implementation worktrees and record clean baselines

**Files:**
- Inspect only: `backend/`, `frontend/`, `mobile/`, `docs/`
- Create outside repositories: one worktree/branch per repository using `superpowers:using-git-worktrees`.

**Interfaces:**
- Consumes: repository roots and current branches.
- Produces: isolated branches with recorded baseline commands and no unrelated files staged.

- [ ] **Step 1: Detect current worktree state**

Run in each repository:

```bash
GIT_DIR=$(cd "$(git rev-parse --git-dir)" && pwd -P)
GIT_COMMON=$(cd "$(git rev-parse --git-common-dir)" && pwd -P)
git branch --show-current
git status --short --branch
```

Expected: docs is on `docs/provider-capability-vetting` with SRS edits and unrelated slides; backend/frontend/mobile are on `main` with no tracked changes. Preserve these states.

- [ ] **Step 2: Create worktrees only after confirming the destination is ignored**

Use the native worktree mechanism if available; otherwise use `.worktrees/<branch>` after verifying:

```bash
git check-ignore -q .worktrees
```

Use branch names:

```text
refactor/mf1-mf5-backend
refactor/mf1-mf5-frontend
refactor/mf1-mf5-mobile
refactor/mf1-mf5-docs
```

- [ ] **Step 3: Run baseline checks before changing source**

```bash
# backend
cd backend && ./mvnw test

# frontend
cd frontend && npm test && npm run build

# mobile
cd mobile && flutter test && flutter analyze

# docs
git diff --check
```

Record failures as baseline failures; do not attribute them to the refactor.

- [ ] **Step 4: Commit only a baseline/plan pointer if the repository convention requires one**

Do not commit generated reports or unrelated files. The docs design and plan are already committed separately.

**Verification:** Four repository statuses are known; baseline test/build results are recorded; no source implementation has started.

---

### Task 0.2: Build the canonical role, flow, API, and data contract matrix

**Files:**
- Create in docs worktree: `docs/superpowers/plans/mf1-mf5-contract-matrix.md`
- Read: `docs/reports/report-3-software-requirement-specification/01-overall-description.md`
- Read: `docs/reports/report-3-software-requirement-specification/02-user-requirements.md`
- Read: `docs/reports/report-3-software-requirement-specification/03-functional-requirements.md`
- Read: `docs/reports/report-3-software-requirement-specification/04-non-functional-requirements.md`
- Read: `docs/reports/report-3-software-requirement-specification/05-requirement-appendix.md`
- Read: `docs/project-reference/business-flows.md`
- Read: `docs/project-reference/database-design.md`
- Read: `docs/reports/report-5-test-report/01-test-cases/test-case-list.md`

**Interfaces:**
- Consumes: Report 3, business-flow, database-design, and Report 5 source documents.
- Produces: a reviewable matrix mapping each role, SF/MF flow, entity, endpoint/client screen, authorization rule, and test ID to its current implementation status.

- [ ] **Step 1: Extract the six roles and actor zones**

The matrix must contain exactly these rows:

```text
PLATFORM_ADMIN       -> PLATFORM_GOVERNANCE
PLATFORM_OPERATOR    -> PLATFORM_GOVERNANCE
CLIENT               -> CUSTOMER_ORGANIZATION
PROVIDER_MANAGER     -> SERVICE_PROVIDER
INSPECTOR            -> SERVICE_PROVIDER
MAINTENANCE_ENGINEER -> SERVICE_PROVIDER
```

- [ ] **Step 2: Map every target flow to implementation modules**

Use these mandatory mappings:

```text
SF  -> users + assets
MF1 -> inspectionrequests
MF2 -> inspections (mission planning)
MF3 -> inspections
MF4 -> inspections + partner ports + notifications
MF5 -> maintenance
```

- [ ] **Step 3: Mark implementation status honestly**

Use only `implemented`, `partial`, `target-only`, or `blocked-by-baseline`. Do not convert a document claim into an implementation claim.

- [ ] **Step 4: Add the matrix’s negative test obligations**

At minimum include role migration, Provider capability independence, cross-organization reads, unassigned workforce access, author-verification release, before/after completion, and unsupported partner integration behavior.

- [ ] **Step 5: Review the matrix against the SRS**

Run:

```bash
git diff --check
```

**Verification:** Every design requirement points to a later task and a test/documentation artifact; no role or Main Flow is omitted.

**Commit:** `docs: add MF1-MF5 contract matrix`

---

## Phase 1A — WF1 Asset Catalog, Review, Scheduling, and Due-Cycle Refactor

WF1 already has a Java implementation under `backend/src/main/java/com/smartdroneinspection/assets/`. This phase audits and aligns that implementation to the documents before later SF/MF1 work consumes it; it must not recreate WF1 tables or silently discard the current schedule/proposal behavior.

### Task 0.3: Lock the documented WF1 state and authorization contract with regression tests

**Files:**
- Read/modify tests under `backend/src/test/java/com/smartdroneinspection/assets/`:
  - `AssetWorkflowIntegrationTest.java`
  - `AssetReviewApiIntegrationTest.java`
  - `ScheduleProposalApiIntegrationTest.java`
  - `InspectionScheduleServiceTest.java`
  - `PeriodicRequestHandoffTest.java`
  - `AssetDocumentApiIntegrationTest.java`
- Read: `backend/src/main/java/com/smartdroneinspection/assets/domain/Asset.java`, `ScheduleProposal.java`, `InspectionSchedule.java`
- Read: Report 3 FE-02/FE-03 and Report 5 WF1-001–WF1-019.

**Interfaces:**
- Consumes: existing WF1 Java entities/services/controllers and the current Report 3/Report 5 contract.
- Produces: executable regression coverage for asset `PENDING_REVIEW`/`ACTIVE`/`REJECTED`, proposal approval/selection, schedule idempotency, document scope, and due-cycle handoff.

- [ ] **Step 1: Add red tests for any documented behavior missing from the current suite**

Cover exactly these behaviors:

```text
Client-created asset starts PENDING_REVIEW
only the authorized Service Manager/target operator can approve or reject it
rejected assets create no schedule proposals
one generated proposal exists per category suggestion and asset review path
Client selects one approved proposal and sibling proposals are superseded
repeating selection or selecting another organization’s proposal is denied
due-cycle replay emits at most one request handoff
asset documents enforce type/size/state/organization scope
```

- [ ] **Step 2: Run focused tests and observe expected failures**

```bash
cd /home/ubuntu/SmartDroneInspection/backend
./mvnw -Dtest=AssetWorkflowIntegrationTest,AssetReviewApiIntegrationTest,ScheduleProposalApiIntegrationTest,InspectionScheduleServiceTest,PeriodicRequestHandoffTest,AssetDocumentApiIntegrationTest test
```

- [ ] **Step 3: Implement only the missing WF1 behavior in existing `assets` boundaries**

Keep entities in `assets`, use organization-scoped repository queries, and preserve the existing `InspectionScheduleDue` event contract used by `inspectionrequests`.

- [ ] **Step 4: Run the focused WF1 suite and the full assets package**

```bash
./mvnw -Dtest='com.smartdroneinspection.assets.**' test
```

**Commit:** `refactor: align WF1 asset and schedule behavior`

---

### Task 0.4: Reconcile WF1 schema/migration and API contract with Report 3

**Files:**
- Inspect/modify: `backend/src/main/resources/db/migration/V5__asset_catalog_and_planning.sql`
- Inspect/modify: `backend/src/main/resources/db/migration/V11__schedule_proposals_and_category_policy.sql`
- Modify only with a new forward migration if required: `backend/src/main/resources/db/migration/V12__wf1_contract_alignment.sql` (verify current highest migration first).
- Inspect/modify entities/repositories/controllers under `backend/src/main/java/com/smartdroneinspection/assets/`.
- Tests: `backend/src/test/java/com/smartdroneinspection/assets/AssetSchemaMigrationTest.java`, `InspectionSchedulePersistenceTest.java`, `ScheduleProposalModelTest.java`, `AssetPersistenceTest.java`.

**Interfaces:**
- Consumes: regression behavior from Task 1A.1.
- Produces: schema constraints for organization-scoped asset codes, proposal selection idempotency, due-cycle uniqueness, state transitions, and document metadata.

- [ ] **Step 1: Add failing SQL/entity assertions for every required constraint**

Assert unique organization/code, valid status transitions, one active schedule, one due-cycle request identity, proposal sibling supersession, and scoped document ownership.

- [ ] **Step 2: Run migration/schema tests and confirm red where the current schema is incomplete**

```bash
./mvnw -Dtest=AssetSchemaMigrationTest,InspectionSchedulePersistenceTest,ScheduleProposalModelTest,AssetPersistenceTest,FullDatabaseSchemaSqlContractTest test
```

- [ ] **Step 3: Add the smallest forward migration and mapping changes**

Never rewrite V5/V11. Keep all timestamps UTC, use explicit foreign-key delete behavior, and preserve existing rows.

- [ ] **Step 4: Run clean migration and assets persistence verification**

```bash
./mvnw -Dtest=AssetSchemaMigrationTest,InspectionSchedulePersistenceTest,ScheduleProposalModelTest,AssetPersistenceTest,FullDatabaseSchemaMigrationTest,FullDatabaseSchemaSqlContractTest test
```

**Commit:** `refactor: harden WF1 schema and idempotency`

---

### Task 0.5: Synchronize WF1 web/mobile behavior and Report 5 evidence

**Files:**
- Frontend: `frontend/src/features/assets/`, especially `AssetsPage.tsx`, `AssetReviewPage.tsx`, `ScheduleProposalsPage.tsx`, `InspectionSchedulesPage.tsx`, and their tests.
- Mobile: existing asset/inspection assignment consumers under `mobile/lib/features/assets/` and `mobile/lib/features/inspections/` only where the API state contract changes.
- Docs: `docs/reports/report-5-test-report/01-test-cases/test-case-list.md`, `03-features/fe-02-asset-registry-inspection-schedule.md`, `03-features/fe-03-inspection-request-work-assignment.md`, and statistics/cover files after real execution.

**Interfaces:**
- Consumes: WF1 backend response/error/state contracts.
- Produces: UI states matching `PENDING_REVIEW`, proposal decisions, selected/superseded proposals, active schedules, and due-cycle handoff.

- [ ] **Step 1: Add failing frontend tests for missing WF1 states and negative scope**

Cover loading/error/empty states, asset review decision visibility, proposal selection idempotency, and foreign-organization denial.

- [ ] **Step 2: Run the focused frontend tests and observe red**

```bash
cd /home/ubuntu/SmartDroneInspection/frontend
npm test -- --run src/features/assets
```

- [ ] **Step 3: Implement the smallest feature-local UI/API changes**

Do not move WF1 business rules into the client; preserve shared API envelope/error decoding.

- [ ] **Step 4: Run frontend and backend WF1 verification**

```bash
npm test
npm run lint
npm run build
cd /home/ubuntu/SmartDroneInspection/backend
./mvnw -Dtest='com.smartdroneinspection.assets.**',PeriodicRequestHandoffTest test
```

**Commit:** `feat: align WF1 clients and verification evidence`

---

## Phase 1 — Canonical identity, Provider Organization, and Supporting Flow

### Task 1.1: Add failing tests for canonical role and actor-zone policy

**Files:**
- Modify: `backend/src/main/java/com/smartdroneinspection/shared/auth/Roles.java`
- Modify: `backend/src/main/java/com/smartdroneinspection/users/domain/enums/UserRole.java`
- Modify: `backend/src/main/java/com/smartdroneinspection/users/domain/enums/ActorZone.java`
- Modify: `backend/src/main/java/com/smartdroneinspection/users/domain/RolePolicy.java`
- Test: `backend/src/test/java/com/smartdroneinspection/users/RolePolicyTest.java`
- Test: `backend/src/test/java/com/smartdroneinspection/users/AdminUserServiceTest.java`

**Interfaces:**
- Consumes: existing `RolePolicy.validate(ActorZone, UUID, Set<UserRole>)` and user role persistence.
- Produces: canonical role enum/string values and a role-policy contract consumed by authentication, API authorization, web, and mobile.

- [ ] **Step 1: Write red tests for the target policy**

Add behavior-level tests equivalent to:

```java
@Test
void platformOperatorIsPlatformGovernanceAndMayVetProviders() {
  assertThat(policy.allowedZone(UserRole.PLATFORM_OPERATOR))
      .isEqualTo(ActorZone.PLATFORM_GOVERNANCE);
  assertThat(policy.canPerform(UserRole.PLATFORM_OPERATOR, CapabilityAction.VET_PROVIDER))
      .isTrue();
}

@Test
void providerManagerIsProviderOrganizationScoped() {
  assertThat(policy.allowedZone(UserRole.PROVIDER_MANAGER))
      .isEqualTo(ActorZone.SERVICE_PROVIDER);
  assertThat(policy.canPerform(UserRole.PROVIDER_MANAGER, CapabilityAction.VET_PROVIDER))
      .isFalse();
}

@Test
void maintenanceProviderManagerRoleDoesNotExist() {
  assertThat(Arrays.stream(UserRole.values()).map(Enum::name))
      .doesNotContain("MAINTENANCE_PROVIDER_MANAGER");
}
```

Use the project’s actual policy API; these names are the required behavior, not permission to invent a public API without checking existing patterns.

- [ ] **Step 2: Run the focused tests and confirm expected red failures**

```bash
cd backend
./mvnw -Dtest=RolePolicyTest,AdminUserServiceTest test
```

Expected: failures identify missing target role/zone/action behavior, not compilation errors caused by the test itself.

- [ ] **Step 3: Commit the red tests**

```bash
git add src/test/java/com/smartdroneinspection/users/RolePolicyTest.java
 git commit -m "test: define canonical provider role policy"
```

---

### Task 1.2: Implement canonical roles, actor zones, role migration, and session invalidation

**Files:**
- Modify: `backend/src/main/java/com/smartdroneinspection/shared/auth/Roles.java`
- Modify: `backend/src/main/java/com/smartdroneinspection/users/domain/enums/UserRole.java`
- Modify: `backend/src/main/java/com/smartdroneinspection/users/domain/enums/ActorZone.java`
- Modify: `backend/src/main/java/com/smartdroneinspection/users/domain/RolePolicy.java`
- Modify: `backend/src/main/java/com/smartdroneinspection/users/domain/User.java`
- Modify: `backend/src/main/java/com/smartdroneinspection/users/service/AdminUserService.java`
- Create: `backend/src/main/resources/db/migration/V12__canonical_roles_and_provider_scope.sql` (use the next unused version after rechecking)
- Modify/add: role and authentication integration tests.

**Interfaces:**
- Consumes: red role-policy tests from Task 1.1.
- Produces: canonical `UserRole`, `ActorZone.PLATFORM_GOVERNANCE`, `ActorZone.SERVICE_PROVIDER`, provider linkage fields, and an explicit role migration/backfill contract.

- [ ] **Step 1: Define the explicit legacy mapping before editing values**

Record and test a mapping table. Do not silently choose one:

```text
ADMIN                  -> PLATFORM_ADMIN
CLIENT                 -> CLIENT
SERVICE_MANAGER        -> reviewed mapping: PLATFORM_OPERATOR or PROVIDER_MANAGER
INSPECTOR              -> INSPECTOR
MAINTENANCE_ENGINEER   -> MAINTENANCE_ENGINEER
```

If current data cannot distinguish `SERVICE_MANAGER`, stop the migration at `blocked-by-baseline` and keep a compatibility mapping until the owner approves the data split. Do not map it by guess.

- [ ] **Step 2: Implement canonical enums and domain policy**

Update the zone checks so platform roles have no organization/provider ID, customer users have `organization_id`, and service-provider users have `provider_id`. Keep role combinations explicit and reject cross-zone combinations that the SRS does not permit.

- [ ] **Step 3: Add a forward migration with constraints and backfill safety**

The migration must:

```sql
-- outline only; implement against the reviewed current schema
-- add provider_id and canonical actor-zone values
-- update role literals only through the approved mapping
-- reject ambiguous SERVICE_MANAGER rows instead of guessing
-- preserve user/auth history and invalidate sessions after role changes
```

Add checks for mutually exclusive `organization_id`/`provider_id` ownership and indexes for provider-scoped lookups.

- [ ] **Step 4: Run focused red-to-green tests**

```bash
./mvnw -Dtest=RolePolicyTest,AdminUserServiceTest,AdminUserApiIntegrationTest test
```

- [ ] **Step 5: Run schema and architecture checks**

```bash
./mvnw -Dtest=PersistenceEntityMappingTest,FullDatabaseSchemaSqlContractTest,ModulithArchitectureTest test
```

**Commit:** `refactor: align canonical roles and actor zones`

---

### Task 1.3: Add Provider Organization and capability-vetting aggregates

**Files:**
- Create under `backend/src/main/java/com/smartdroneinspection/users/`:
  - `domain/ProviderOrganization.java`
  - `domain/ProviderCapability.java`
  - `domain/ProviderCapabilityEvidence.java`
  - `domain/ProviderVettingDecision.java`
  - `domain/enums/ProviderCapabilityType.java`
  - `domain/enums/ProviderCapabilityStatus.java`
  - `domain/enums/ProviderEvidenceType.java`
  - repositories and scoped service/facade classes following existing users conventions.
- Modify: `backend/src/main/resources/db/migration/V13__provider_organizations_and_capability_vetting.sql`
- Tests: new `ProviderCapabilityDomainTest.java`, `ProviderCapabilityPersistenceTest.java`, and SQL contract coverage.

**Interfaces:**
- Consumes: canonical role/zone/provider linkage from Task 1.2.
- Produces: a named users-module facade such as `ProviderEligibilityFacade` with explicit methods:

```java
boolean isVerified(UUID providerId, ProviderCapabilityType capability);
ProviderCapabilitySnapshot capability(UUID providerId, ProviderCapabilityType capability);
```

The facade must be the only cross-module path used by inspectionrequests/inspections/maintenance.

- [ ] **Step 1: Write failing domain tests**

Cover:

```text
inspection only -> one inspection capability record
maintenance only -> one maintenance capability record
both -> two records, not a BOTH enum
verify inspection -> maintenance remains PENDING
reject maintenance -> inspection remains VERIFIED
undeclared capability decision -> rejected
Provider Manager cannot self-approve
```

- [ ] **Step 2: Run the focused test to verify red**

```bash
./mvnw -Dtest=ProviderCapabilityDomainTest test
```

- [ ] **Step 3: Implement aggregate invariants and status transitions**

Use append-only decision history. Require operator ID and reason for decisions. Keep shared legal identity separate from capability-specific evidence. Store MinIO object keys/checksums/metadata, never raw protected file contents or secrets.

- [ ] **Step 4: Add migration and persistence tests**

Assert unique `(provider_id, capability)`, status checks, evidence ownership, decision actor/time, and foreign-key behavior. Run:

```bash
./mvnw -Dtest=ProviderCapabilityPersistenceTest,FullDatabaseSchemaMigrationTest,FullDatabaseSchemaSqlContractTest test
```

- [ ] **Step 5: Verify Modulith visibility**

```bash
./mvnw -Dtest=ModulithArchitectureTest test
```

**Commit:** `feat: add provider organization and capability vetting`

---

### Task 1.4: Implement Supporting Flow onboarding and independent vetting APIs

**Files:**
- Create under `backend/src/main/java/com/smartdroneinspection/users/api/`:
  - `ProviderOrganizationController.java`
  - `ProviderVettingController.java`
  - `dto/request/ProviderOnboardingRequest.java`
  - `dto/request/CapabilityEvidenceRequest.java`
  - `dto/request/VettingDecisionRequest.java`
  - response records.
- Create/modify: `backend/src/main/java/com/smartdroneinspection/users/service/ProviderOnboardingService.java`
- Create/modify: `backend/src/main/java/com/smartdroneinspection/users/service/ProviderVettingService.java`
- Modify: shared security and error mapping only where required.
- Tests: `ProviderOnboardingApiIntegrationTest.java`, `ProviderVettingApiIntegrationTest.java`, `ProviderAuthorizationScopeTest.java`.

**Interfaces:**
- Consumes: `ProviderEligibilityFacade` and the users persistence aggregates.
- Produces:

```text
POST /api/v1/provider-organizations
GET  /api/v1/provider-organizations/{providerId}/capabilities
POST /api/v1/provider-organizations/{providerId}/capabilities/{capability}/decisions
```

Use the existing envelope/error conventions; final endpoint names must be recorded in the contract matrix.

- [ ] **Step 1: Write red API tests**

Test:

```text
Provider Manager declares inspection only
Provider Manager declares maintenance only
Provider Manager declares both and supplies both evidence groups
empty capability set -> 400 ProblemDetail
missing capability evidence -> 400 ProblemDetail
Provider Manager decision attempt -> 403
Platform Operator verifies inspection only -> maintenance unchanged
foreign Provider scope -> 404/403 according to existing security policy
```

- [ ] **Step 2: Run the focused API tests and confirm red**

```bash
./mvnw -Dtest=ProviderOnboardingApiIntegrationTest,ProviderVettingApiIntegrationTest,ProviderAuthorizationScopeTest test
```

- [ ] **Step 3: Implement onboarding and vetting transactions**

Validate capability-specific evidence, append decisions, emit audit events, and preserve idempotency/state checks. Do not let provider onboarding create an accepted inspection/maintenance order or grant mission clearance.

- [ ] **Step 4: Run green API and auth regressions**

```bash
./mvnw -Dtest=ProviderOnboardingApiIntegrationTest,ProviderVettingApiIntegrationTest,ProviderAuthorizationScopeTest,AdminUserApiIntegrationTest test
```

**Commit:** `feat: add provider onboarding and vetting api`

---

## Phase 2 — MF1 and MF2 request, quotation, order, mission, and clearance refactor

### Task 2.1: Add capability eligibility gates to MF1 inspection sourcing

**Files:**
- Modify: `backend/src/main/java/com/smartdroneinspection/inspectionrequests/domain/InspectionRequest.java`
- Modify: `backend/src/main/java/com/smartdroneinspection/inspectionrequests/domain/InspectionQuotation.java`
- Modify: `backend/src/main/java/com/smartdroneinspection/inspectionrequests/domain/InspectionServiceOrder.java`
- Modify: `backend/src/main/java/com/smartdroneinspection/inspectionrequests/domain/InspectionAssignment.java`
- Modify corresponding services/repositories.
- Tests: existing `InspectionQuotationTest.java`, `InspectionAssignmentTest.java`, `InspectionServiceOrderTest.java`, plus provider eligibility tests.

**Interfaces:**
- Consumes: `ProviderEligibilityFacade.isVerified(providerId, INSPECTION)`.
- Produces: inspection quote/order/assignment transitions that fail closed unless inspection capability is verified.

- [ ] **Step 1: Add red tests for provider eligibility**

```text
unverified inspection capability cannot quote
maintenance-only provider cannot quote inspection
inspection-verified provider can quote
both-verified provider can quote
foreign Provider cannot read rival bid/order
```

- [ ] **Step 2: Run existing plus new focused tests and confirm red**

```bash
./mvnw -Dtest=InspectionQuotationTest,InspectionAssignmentTest,InspectionServiceOrderTest,ProviderEligibilityInspectionTest test
```

- [ ] **Step 3: Add the named-facade call at the service transition boundary**

Do not import users controllers, repositories, or entities into `inspectionrequests`. Keep provider ID scalar at persistence boundaries.

- [ ] **Step 4: Verify green and Modulith boundaries**

```bash
./mvnw -Dtest=InspectionQuotationTest,InspectionAssignmentTest,InspectionServiceOrderTest,ProviderEligibilityInspectionTest,ModulithArchitectureTest test
```

**Commit:** `feat: gate MF1 inspection work by provider capability`

---

### Task 2.2: Add MF1 quotation/order policy snapshots and fail-closed funding boundary

**Files:**
- Modify: `backend/src/main/resources/db/migration/V14__mf1_policy_snapshots.sql`
- Modify: `inspectionrequests/domain/InspectionQuotation.java`
- Modify: `inspectionrequests/domain/InspectionServiceOrder.java`
- Create/modify policy value/snapshot types and repositories.
- Create partner port under `inspectionrequests/spi/` or the owning module boundary.
- Tests: `InspectionCommercialPersistenceTest.java`, `InspectionServiceOrderTest.java`, new `InspectionPolicySnapshotTest.java`, partner-boundary tests.

**Interfaces:**
- Consumes: verified Provider eligibility and accepted quotation/order.
- Produces: immutable accepted order snapshot containing policy versions/values and a partner capability check before funding-dependent execution.

- [ ] **Step 1: Write red tests**

Test:

```text
quotation excludes Platform AI/data/storage charges
one uniform Provider-paid commission is snapshotted
later policy publication does not mutate accepted order
unsupported partner product blocks funding-dependent execution
no funding requirement does not create a payment gate
```

- [ ] **Step 2: Run focused tests and observe red**

```bash
./mvnw -Dtest=InspectionCommercialPersistenceTest,InspectionServiceOrderTest,InspectionPolicySnapshotTest test
```

- [ ] **Step 3: Implement snapshot/value mapping and partner port**

Keep the port disabled/fail-closed when no supported adapter exists. Never store payment secrets or claim that the Platform holds funds.

- [ ] **Step 4: Run persistence/schema tests**

```bash
./mvnw -Dtest=InspectionCommercialPersistenceTest,InspectionPolicySnapshotTest,FullDatabaseSchemaMigrationTest,FullDatabaseSchemaSqlContractTest test
```

**Commit:** `feat: snapshot MF1 commercial terms safely`

---

### Task 2.3: Implement MF2 mission plans, shot items, and clearance state

**Files:**
- Create under `backend/src/main/java/com/smartdroneinspection/inspections/`:
  - `domain/DroneMissionPlan.java`
  - `domain/MissionShotItem.java`
  - `domain/enums/AirspaceCheckStatus.java`
  - `domain/enums/MissionPlanStatus.java`
  - repositories, service, root facade, API DTOs/controller.
- Create: `backend/src/main/resources/db/migration/V15__drone_mission_plans_and_clearance.sql`
- Tests: `DroneMissionPlanTest.java`, `MissionPlanApiIntegrationTest.java`, `MissionPlanPersistenceTest.java`.

**Interfaces:**
- Consumes: accepted inspection service order and Provider Manager/Inspector scope.
- Produces:

```java
MissionPlanId create(UUID serviceOrderId, MissionPlanDraft draft, PrincipalScope scope);
MissionPlanSnapshot approve(UUID missionPlanId, PrincipalScope scope);
```

- [ ] **Step 1: Add red domain/API tests**

Cover:

```text
GSD/overlap/equipment/AGL/shot items are required by the SOW
manual flight is valid without waypoint coordinates
waypoint fields validate when waypoint-assisted capture is selected
public airspace lookup does not equal clearance
mission release is blocked until applicable clearance/permit state is verified
cross-provider mission access is denied
```

- [ ] **Step 2: Run focused tests and confirm red**

```bash
./mvnw -Dtest=DroneMissionPlanTest,MissionPlanApiIntegrationTest,MissionPlanPersistenceTest test
```

- [ ] **Step 3: Implement aggregate, migration, API, and scoped repository queries**

Keep mission-plan IDs scalar across modules and expose only a named root facade/events interface.

- [ ] **Step 4: Run green tests and Modulith verification**

```bash
./mvnw -Dtest=DroneMissionPlanTest,MissionPlanApiIntegrationTest,MissionPlanPersistenceTest,ModulithArchitectureTest test
```

**Commit:** `feat: implement MF2 mission planning and clearance state`

---

## Phase 3 — MF3 inspection, evidence, findings, and report release

### Task 3.1: Align inspection execution and evidence with MF2 assignment scope

**Files:**
- Modify: `backend/src/main/java/com/smartdroneinspection/inspections/domain/Inspection.java`
- Modify: `backend/src/main/java/com/smartdroneinspection/inspections/service/InspectionService.java`, `EvidenceService.java`, the existing `InspectionController.java`, and `InspectionReportController.java` only where mission/assignment scope enters the current flow.
- Modify: `backend/src/main/java/com/smartdroneinspection/inspections/repository/InspectionRepository.java`, `EvidenceRepository.java`, and `InspectionAssignmentRepository.java` with scoped queries.
- Modify: MinIO feature port/adapters only through existing `inspections/spi` boundary.
- Test: existing `backend/src/test/java/com/smartdroneinspection/inspections/InspectionWorkflowTest.java`, `EvidenceServiceTest.java`, and `EvidenceApiIntegrationTest.java`, plus a new mission-linked scope test in the same package.

**Interfaces:**
- Consumes: approved mission-plan snapshot and accepted Provider/Inspector assignment.
- Produces: inspection start/evidence APIs that require assigned scope, preserve checksum/source metadata, reject duplicate context-scoped evidence, and keep manual fallback available when AI is unavailable.

- [ ] **Step 1: Add red tests for mission-linked execution**

```text
inspection cannot start without approved plan/clearance
assigned Inspector can start only their own inspection
unassigned Inspector is denied
valid evidence persists server checksum and source metadata
duplicate checksum in one work context is rejected
missing GPS is recorded, not automatically rejected
AI unavailable preserves evidence/manual finding path
```

- [ ] **Step 2: Run focused tests and confirm red**

```bash
./mvnw -Dtest=InspectionWorkflowTest,EvidenceServiceTest,EvidenceApiIntegrationTest test
```

- [ ] **Step 3: Implement mission linkage and scope checks**

Preserve the existing MinIO object-storage security rule: object possession/path does not grant access.

- [ ] **Step 4: Run green tests**

```bash
./mvnw -Dtest=InspectionWorkflowTest,EvidenceServiceTest,EvidenceApiIntegrationTest test
```

**Commit:** `refactor: align MF3 execution with mission scope`

---

### Task 3.2: Replace target peer-review behavior with author verification and Provider Manager completeness

**Files:**
- Modify: `backend/src/main/java/com/smartdroneinspection/inspections/domain/InspectionReport.java`, `ReportVersion.java`, `PeerReview.java`, and the relevant report status enums.
- Modify: `backend/src/main/java/com/smartdroneinspection/inspections/service/InspectionReportService.java`, `api/InspectionReportController.java`, report request/response DTOs, and report repositories.
- Test: existing `backend/src/test/java/com/smartdroneinspection/inspections/InspectionReportServiceTest.java`, `InspectionReportApiIntegrationTest.java`, and `ReportSnapshotSerializationTest.java`; create `ReportAuthorVerificationTest.java` in the same package.
- Documentation: Report 3 and Report 5 references in Phase 7, not mixed into the first code commit.

**Interfaces:**
- Consumes: verified findings, evidence, checklist, SOW/mission snapshot, and assigned report author.
- Produces: explicit report transitions:

```text
DRAFT -> AUTHOR_VERIFIED -> MANAGER_RELEASED -> CLIENT_ACCEPTED | CLIENT_CLARIFICATION | COMPLAINT
```

- [ ] **Step 1: Add red report-transition tests**

```text
AI draft remains labelled as draft
report author must verify/edit required sections before submit
non-author Inspector cannot verify another author’s draft
Provider Manager checks completeness and can return with reasons
Client cannot see unreleased/unverified draft
accepted version is immutable; correction creates linked version
old v1 peer-review records remain readable as historical data
```

- [ ] **Step 2: Run focused tests and confirm red**

```bash
./mvnw -Dtest=InspectionReportServiceTest,InspectionReportApiIntegrationTest,ReportSnapshotSerializationTest,ReportAuthorVerificationTest test
```

- [ ] **Step 3: Implement state machine and audit snapshots**

Do not delete historical peer-review rows. Separate historical data compatibility from the target transition path.

- [ ] **Step 4: Run green report tests and persistence checks**

```bash
./mvnw -Dtest=InspectionReportServiceTest,InspectionReportApiIntegrationTest,ReportSnapshotSerializationTest,ReportAuthorVerificationTest,FullDatabaseSchemaSqlContractTest test
```

**Commit:** `refactor: align MF3 report verification and release`

---

## Phase 4 — MF4 Client decisions, complaints, and integration boundaries

### Task 4.1: Implement immutable Client report decision and complaint states

**Files:**
- Modify: inspection report/order domain and API files.
- Create or modify complaint/dispute domain under `inspections` or the owning capability identified by the contract matrix.
- Create forward migration: next verified version for dispute/decision tables.
- Tests: report decision API tests and new `ComplaintWorkflowTest.java`, `ComplaintApiIntegrationTest.java`.

**Interfaces:**
- Consumes: Manager-released report and accepted order snapshot.
- Produces: Client decision commands returning immutable decision/audit records and internal Platform Operator outcome commands.

- [ ] **Step 1: Add red tests**

```text
Client can accept released report
Client can request clarification during review period
Client can file complaint scoped to accepted order/report
timely complaint blocks deemed acceptance
Operator can record Platform Terms outcome
Operator cannot issue a legal arbitration result
external remedy language remains in API/documentation messages
```

- [ ] **Step 2: Run focused tests and confirm red**

```bash
./mvnw -Dtest=ComplaintWorkflowTest,ComplaintApiIntegrationTest,InspectionReportApiIntegrationTest test
```

- [ ] **Step 3: Implement immutable decision/complaint records and transitions**

Use the existing response/error contract and append-only audit records. Do not create an online payment balance in the Platform.

- [ ] **Step 4: Run green tests**

```bash
./mvnw -Dtest=ComplaintWorkflowTest,ComplaintApiIntegrationTest,InspectionReportApiIntegrationTest test
```

**Commit:** `feat: implement MF4 report decisions and complaints`

---

### Task 4.2: Add fail-closed payment-partner ports and order-snapshot settlement rules

**Files:**
- Create feature-owned ports under `inspectionrequests/spi/` or the module owning the order transaction.
- Create adapters/configuration under `backend/src/main/java/com/smartdroneinspection/infrastructure/` only after the port exists.
- Modify order/settlement state and migration.
- Tests: `PaymentPartnerBoundaryTest.java`, `SettlementPolicyTest.java`, `ComplaintHoldBoundaryTest.java`.

**Interfaces:**
- Consumes: accepted order’s immutable policy snapshot and complaint/Client decision state.
- Produces:

```java
PartnerCapabilityResult supports(PartnerOperation operation, OrderPolicySnapshot snapshot);
PartnerTransactionStatus requestSettlement(SettlementCommand command);
PartnerTransactionStatus requestHold(HoldCommand command);
```

- [ ] **Step 1: Write red port/boundary tests**

```text
unconfigured partner -> funding/settlement/hold operation blocked
unsupported terms -> operation blocked
supported fixture -> only accepted order terms sent
commission applies once to eligible VAT-exclusive value
refund reverses proportional commission
retention release does not apply a second commission
```

- [ ] **Step 2: Run focused tests and confirm red**

```bash
./mvnw -Dtest=PaymentPartnerBoundaryTest,SettlementPolicyTest,ComplaintHoldBoundaryTest test
```

- [ ] **Step 3: Implement port, deterministic test adapter, and safe production configuration**

Do not claim a real bank/payment integration; the deterministic fixture proves contract behavior only.

- [ ] **Step 4: Run green tests and architecture checks**

```bash
./mvnw -Dtest=PaymentPartnerBoundaryTest,SettlementPolicyTest,ComplaintHoldBoundaryTest,ModulithArchitectureTest test
```

**Commit:** `feat: add fail-closed MF4 partner boundaries`

---

## Phase 5 — MF5 maintenance, evidence, retention, and linked re-inspection

### Task 5.1: Gate maintenance work by maintenance capability and accepted findings

**Files:**
- Modify: `backend/src/main/java/com/smartdroneinspection/maintenance/domain/MaintenanceTicket.java`
- Modify: `backend/src/main/java/com/smartdroneinspection/maintenance/repository/MaintenanceTicketRepository.java`, `MaintenanceTicketFindingRepository.java`, and `MaintenanceAssessmentRepository.java`, plus the first maintenance application services/controllers created by this phase.
- Create tests: `backend/src/test/java/com/smartdroneinspection/maintenance/MaintenanceTicketTest.java`, `backend/src/test/java/com/smartdroneinspection/maintenance/MaintenanceAssessmentTest.java`, and `backend/src/test/java/com/smartdroneinspection/maintenance/ProviderEligibilityMaintenanceTest.java`.

**Interfaces:**
- Consumes: verified maintenance capability and accepted inspection report finding facade.
- Produces: maintenance ticket creation and assessment transitions requiring an accepted report finding and maintenance-provider eligibility.

- [ ] **Step 1: Add red tests**

```text
unverified maintenance capability cannot issue maintenance quotation/order
inspection-only provider cannot perform maintenance
maintenance-verified provider can assess/quote
both-verified provider can perform maintenance
maintenance ticket without accepted-report finding is rejected
cross-organization finding/ticket access is rejected
```

- [ ] **Step 2: Run focused tests and confirm red**

```bash
./mvnw -Dtest=MaintenanceTicketTest,MaintenanceAssessmentTest,ProviderEligibilityMaintenanceTest test
```

- [ ] **Step 3: Implement eligibility and accepted-finding gates through named facades**

Keep cross-module references as scalar IDs and preserve existing maintenance module ownership.

- [ ] **Step 4: Run green tests**

```bash
./mvnw -Dtest=MaintenanceTicketTest,MaintenanceAssessmentTest,ProviderEligibilityMaintenanceTest,ModulithArchitectureTest test
```

**Commit:** `feat: gate MF5 by provider capability and accepted findings`

---

### Task 5.2: Implement maintenance order, assignment, change control, and mandatory before/after evidence

**Files:**
- Modify maintenance domain/API/service/repository files:
  - `MaintenanceQuotation.java`
  - `MaintenanceOrder.java`
  - `MaintenanceAssignment.java`
  - `MaintenanceWorkLog.java`
  - `MaintenanceChangeRequest.java`
- Create/modify next forward migration for workflow constraints.
- Tests: existing maintenance tests, new `MaintenanceOrderWorkflowTest.java`, `MaintenanceEvidenceApiIntegrationTest.java`.

**Interfaces:**
- Consumes: maintenance ticket/assessment and Provider capability eligibility.
- Produces: versioned order/assignment/change/evidence state machine with before/after completion gate.

- [ ] **Step 1: Add red tests**

```text
assessment must be accepted before quotation
order snapshots funding/retention/warranty values only when adopted
additional work pauses until Client-approved change order
Maintenance Engineer sees only assigned work
completion without paired before/after evidence is rejected
Client can accept/rework/request reinspection
```

- [ ] **Step 2: Run focused tests and confirm red**

```bash
./mvnw -Dtest=MaintenanceOrderWorkflowTest,MaintenanceEvidenceApiIntegrationTest test
```

- [ ] **Step 3: Implement state transitions and MinIO evidence metadata**

Use evidence object key/checksum/size/media metadata and the existing feature-owned storage port. Never expose an object path as authorization.

- [ ] **Step 4: Run green tests and schema tests**

```bash
./mvnw -Dtest=MaintenanceOrderWorkflowTest,MaintenanceEvidenceApiIntegrationTest,FullDatabaseSchemaMigrationTest,FullDatabaseSchemaSqlContractTest test
```

**Commit:** `feat: implement MF5 maintenance execution and evidence`

---

### Task 5.3: Implement optional warranty retention and linked re-inspection boundary

**Files:**
- Modify: maintenance order/settlement services and API DTOs.
- Modify: `inspectionrequests` root facade/event contract for a linked re-inspection request.
- Create/modify next forward migration for retention/warranty and linkage fields.
- Tests: `MaintenanceWarrantyRetentionTest.java`, `MaintenanceReinspectionTest.java`, partner boundary tests.

**Interfaces:**
- Consumes: accepted maintenance order snapshot and completion evidence.
- Produces:

```java
WarrantyReleaseResult release(UUID maintenanceOrderId, PartnerContext partnerContext);
UUID requestReinspection(UUID maintenanceTicketId, ReinspectionScope scope);
```

- [ ] **Step 1: Add red tests**

```text
no adopted retention -> no retention balance/release
adopted retention -> values are immutable in order snapshot
unresolved supported warranty complaint blocks release
eligible release creates no second commission
reinspection creates linked request and returns to documented sourcing/planning flow
```

- [ ] **Step 2: Run focused tests and confirm red**

```bash
./mvnw -Dtest=MaintenanceWarrantyRetentionTest,MaintenanceReinspectionTest test
```

- [ ] **Step 3: Implement retention/reinspection behavior with partner fail-closed checks**

Do not create a second Platform commission and do not imply that cash release occurred when the partner only accepted an instruction.

- [ ] **Step 4: Run green tests**

```bash
./mvnw -Dtest=MaintenanceWarrantyRetentionTest,MaintenanceReinspectionTest,SettlementPolicyTest test
```

**Commit:** `feat: add MF5 warranty retention and reinspection`

---

## Phase 6 — Web and mobile contract/client refactor

### Task 6.1: Migrate frontend role/access policy and API contract types

**Files:**
- Modify: `frontend/src/features/auth/store/authStore.ts`
- Modify: `frontend/src/app/permissions/accessPolicy.ts`
- Modify: `frontend/src/app/router/router.tsx`
- Modify: `frontend/src/shared/api/client.ts`
- Modify: `frontend/src/shared/api/apiResponse.ts`
- Modify: `frontend/src/shared/api/errorMessage.ts`
- Tests: access-policy tests and auth/router tests.

**Interfaces:**
- Consumes: canonical backend role strings and `ApiResponse<T>`/Problem Details contracts.
- Produces: typed `Role` union and route/portal policies for six roles, with explicit Platform Governance, Customer, and Service Provider zones.

- [ ] **Step 1: Add red access-policy tests**

```text
PLATFORM_ADMIN sees technical governance only
PLATFORM_OPERATOR sees business/provider-vetting operations
CLIENT sees customer workspace
PROVIDER_MANAGER sees provider workspace
INSPECTOR sees assigned inspection/report screens
MAINTENANCE_ENGINEER sees assigned maintenance screens
legacy role values are rejected or explicitly translated during compatibility window
```

- [ ] **Step 2: Run red tests**

```bash
cd frontend
npm test -- --run src/app/permissions/accessPolicy.test.ts
```

- [ ] **Step 3: Implement role/zone policy and contract decoding**

Keep UI route guards additive and backend authorization authoritative. Preserve legacy route redirects only while the compatibility matrix says they are needed.

- [ ] **Step 4: Run green tests, lint, and build**

```bash
npm test
npm run lint
npm run build
```

**Commit:** `refactor: align frontend roles and actor zones`

---

### Task 6.2: Build Provider onboarding and Platform Operator vetting UI

**Files:**
- Create: `frontend/src/features/providers/types/providerVetting.ts`
- Create: `frontend/src/features/providers/api/providerVettingApi.ts`
- Create: `frontend/src/features/providers/hooks/useProviderVetting.ts`
- Create: `frontend/src/features/providers/components/CapabilitySelector.tsx`
- Create: `frontend/src/features/providers/components/CapabilityEvidenceForm.tsx`
- Create: `frontend/src/features/providers/components/CapabilityStatusCard.tsx`
- Create: `frontend/src/features/providers/pages/ProviderOnboardingPage.tsx`
- Create: `frontend/src/features/providers/pages/ProviderVettingPage.tsx`
- Modify: `frontend/src/app/router/router.tsx`, `frontend/src/app/permissions/accessPolicy.ts`
- Tests: colocated `*.test.tsx` files.

**Interfaces:**
- Consumes: provider onboarding/vetting endpoints from Task 1.4.
- Produces: typed forms and review controls showing independent inspection/maintenance statuses.

- [ ] **Step 1: Add red component tests**

```text
selecting both renders two capability evidence sections
inspection verification does not change maintenance status
missing capability evidence blocks submission
Provider Manager cannot render operator decision controls
operator can choose verify/additional-info/reject with reason
loading/empty/API-error states are recoverable
```

- [ ] **Step 2: Run focused tests and confirm red**

```bash
npm test -- --run src/features/providers
```

- [ ] **Step 3: Implement feature-local API/hooks/components**

Use typed data and callbacks; do not put provider business logic in global state or route components. Keep each component responsible for one reason to change.

- [ ] **Step 4: Run full frontend verification**

```bash
npm test
npm run lint
npm run build
```

**Commit:** `feat: add provider capability and vetting screens`

---

### Task 6.3: Align frontend MF1–MF5 workflow screens incrementally

**Files:**
- Modify existing features under:
  - `frontend/src/features/assets/`
  - `frontend/src/features/inspections/`
  - `frontend/src/features/reports/`
  - `frontend/src/features/maintenance/`
- Create feature-local API/types/pages only where the backend contract matrix requires them.
- Tests: existing feature tests plus new MF1–MF5 transition tests.

**Interfaces:**
- Consumes: backend endpoint contracts produced by Phases 2–5.
- Produces: role-scoped screens for request/RFQ/order, mission/clearance, evidence/report, Client decision/complaint, and maintenance/retention.

- [ ] **Step 1: Add one red test per flow boundary**

```text
MF1 shows only capability-eligible Provider choices/quotes
MF2 distinguishes manual plan from waypoint-assisted plan and clearance status
MF3 blocks report submission until author verification
MF4 blocks client acceptance/settlement when complaint/review state forbids it
MF5 blocks completion without paired before/after evidence
```

- [ ] **Step 2: Implement each screen against typed APIs**

Keep each flow’s loading, empty, validation, conflict, and authorization state explicit.

- [ ] **Step 3: Run feature tests and build**

```bash
npm test
npm run lint
npm run build
```

**Commit:** `feat: align frontend MF1-MF5 workflows`

---

### Task 6.4: Align mobile authentication and assigned workforce workflows

**Files:**
- Modify: `mobile/lib/core/network/api_response_interceptor.dart`
- Modify: `mobile/lib/core/network/api_failure.dart`
- Modify: `mobile/lib/core/network/api_result.dart`
- Modify: `mobile/lib/core/network/auth_interceptor.dart`
- Modify: `mobile/lib/core/router/app_router.dart`
- Modify existing inspection files under `mobile/lib/features/inspections/`
- Create/modify maintenance files under `mobile/lib/features/maintenance/`
- Create/modify generated source inputs only; regenerate `.g.dart`/`.freezed.dart` with build_runner.
- Tests: repository/provider/widget tests under `mobile/test/`.

**Interfaces:**
- Consumes: backend APIs and response/error contracts from Phases 1–5.
- Produces: secure assigned Inspector and Maintenance Engineer workflows with no client-side replacement for backend authorization.

- [ ] **Step 1: Add red Dart tests**

```text
expired/revoked session clears secure token and routes to login
assigned Inspector can load only assigned mission/checklist/evidence
unassigned workforce request renders authorization failure
Maintenance Engineer can upload paired before/after evidence
upload retry does not duplicate evidence
ApiResponse<T> and ProblemDetail decode correctly
```

- [ ] **Step 2: Run focused red tests**

```bash
cd mobile
flutter test test/features test/core
```

- [ ] **Step 3: Implement repositories/providers/pages**

Use Riverpod for async/shared state, Dio’s shared client, and secure storage. Do not edit generated files directly.

- [ ] **Step 4: Regenerate and verify**

```bash
flutter pub get
 dart run build_runner build --delete-conflicting-outputs
 dart format --set-exit-if-changed .
 flutter analyze
 flutter test
```

**Commit:** `feat: align mobile assigned-work workflows`

---

## Phase 7 — Documentation, Report 5 evidence, and cross-repository contracts

### Task 7.1: Synchronize target documents with implemented status

**Files:**
- Modify: `docs/project-reference/business-flows.md`
- Modify: `docs/project-reference/database-design.md`
- Modify: `docs/docs/backend/architecture.md` if path is corrected in the docs repository
- Modify: `docs/reports/report-3-software-requirement-specification/00-record-of-changes.md`
- Modify: `docs/reports/report-3-software-requirement-specification/01-overall-description.md`
- Modify: `docs/reports/report-3-software-requirement-specification/02-user-requirements.md`
- Modify: `docs/reports/report-3-software-requirement-specification/03-functional-requirements.md`
- Modify: `docs/reports/report-3-software-requirement-specification/04-non-functional-requirements.md`
- Modify: `docs/reports/report-3-software-requirement-specification/05-requirement-appendix.md`

**Interfaces:**
- Consumes: verified code/API/schema behavior from Phases 1–6.
- Produces: no stale target/implemented claims and one source-of-truth role/flow/data vocabulary.

- [ ] **Step 1: Add a documentation consistency check**

Create a script or test under `docs/tools/` that verifies the six roles, MF1–MF5, no maintenance-manager role, and required capability-vetting language appear consistently in the authoritative documents.

- [ ] **Step 2: Run it red against any stale document wording**

```bash
python3 docs/tools/check-contract-consistency.py
```

- [ ] **Step 3: Update only claims supported by executed implementation evidence**

Keep target-only disclaimers for unimplemented payment/airspace/settlement integrations. Update implementation-status sections and change logs with exact migration/API/test evidence.

- [ ] **Step 4: Run docs checks**

```bash
git diff --check
python3 docs/tools/check-contract-consistency.py
```

**Commit:** `docs: synchronize MF1-MF5 implementation status`

---

### Task 7.2: Add Report 5 test cases and evidence without changing historical IDs

**Files:**
- Modify: `docs/reports/report-5-test-report/01-test-cases/test-case-list.md`
- Modify matching feature sources:
  - `docs/reports/report-5-test-report/03-features/fe-01-identity-access-governance.md`
  - `docs/reports/report-5-test-report/03-features/fe-03-inspection-request-work-assignment.md`
  - `docs/reports/report-5-test-report/03-features/fe-04-inspection-execution-evidence-management.md`
  - `docs/reports/report-5-test-report/03-features/fe-06-inspection-report-approval.md`
  - `docs/reports/report-5-test-report/03-features/fe-07-maintenance-defect-resolution.md`
- Modify: `docs/reports/report-5-test-report/02-test-statistics/test-statistics.md`
- Modify: `docs/reports/report-5-test-report/00-cover/cover.md`
- Modify: `docs/reports/report-5-test-report/00-cover/record-of-changes.md`

**Interfaces:**
- Consumes: exact executed backend/frontend/mobile test results.
- Produces: stable test IDs mapped to FE codes and `WFx`/MF acceptance, with truthful statuses.

- [ ] **Step 1: Add cases for new target behavior**

At minimum cover:

```text
provider declares inspection/maintenance/both
separate capability decisions
capability-specific inspection eligibility
capability-specific maintenance eligibility
role/organization/assignment negative scope
MF2 manual/waypoint clearance boundary
MF3 author verification and Manager completeness
MF4 complaint/partner fail-closed boundary
MF5 before/after completion and optional retention
```

Preserve fixed workbook sheets and existing IDs. New cases remain `Pending` until the exact test command runs.

- [ ] **Step 2: Record full procedure/evidence in the matching feature files**

Each executed case must record preconditions, procedure, expected result, status, date, tester, and evidence note.

- [ ] **Step 3: Recount statistics from detailed feature files**

```bash
python3 docs/tools/recount-report5-statistics.py
```

Expected: totals equal the detailed files; no unexecuted case is counted as `Passed`.

- [ ] **Step 4: Update cover and change history**

Record the scope and actual verification date. Keep target-only cases visibly pending when dependencies are unavailable.

**Commit:** `docs: add MF1-MF5 verification traceability`

---

## Phase 8 — Cross-repository contract verification and final review

### Task 8.1: Add contract fixtures shared by backend, frontend, and mobile

**Files:**
- Create documented fixtures under `docs/project-reference/api-contract-fixtures/`.
- Backend contract tests under `backend/src/test/java/com/smartdroneinspection/shared/` and owning feature tests.
- Frontend contract tests under `frontend/src/shared/api/`.
- Mobile contract tests under `mobile/test/core/network/`.

**Interfaces:**
- Consumes: final API response/error/role contracts.
- Produces: matching decode/validation behavior for web/mobile and stable backend serialization.

- [ ] **Step 1: Add red fixtures/tests**

Cover one success envelope, one `204` response, one binary evidence response, one RFC 9457 error with code/trace ID, canonical role payload, and capability status payload.

- [ ] **Step 2: Run each client’s contract test and confirm failures identify drift**

```bash
cd backend && ./mvnw -Dtest=ApiResponseTest test
cd frontend && npm test -- --run src/shared/api
cd mobile && flutter test test/core/network
```

- [ ] **Step 3: Align serializers/decoders without changing the documented envelope**

- [ ] **Step 4: Run all three contract suites**

**Commit:** `test: verify cross-client MF1-MF5 contracts`

---

### Task 8.2: Full repository verification and spec-compliance review

**Files:**
- No intended source changes; inspect all four repository diffs.
- Review against: `docs/superpowers/specs/2026-10-04-documents-led-mf1-mf5-refactor-design.md`.

**Interfaces:**
- Consumes: all completed task commits and verification artifacts.
- Produces: final compliance report and explicit remaining target-only/blocked items.

- [ ] **Step 1: Run backend verification**

```bash
cd backend
./mvnw verify
```

- [ ] **Step 2: Run frontend verification**

```bash
cd frontend
npm test
npm run lint
npm run build
```

- [ ] **Step 3: Run mobile verification**

```bash
cd mobile
flutter pub get
 dart run build_runner build --delete-conflicting-outputs
 dart format --set-exit-if-changed .
 flutter analyze
 flutter test
```

- [ ] **Step 4: Run docs verification**

```bash
cd docs
git diff --check
python3 docs/tools/check-contract-consistency.py
```

If Hugo is installed, run the repository’s documented Hugo build; otherwise report that it was unavailable.

- [ ] **Step 5: Inspect final diffs and status**

```bash
for repo in backend frontend mobile docs; do
  echo "--- $repo ---"
  git -C "$repo" status --short --branch
  git -C "$repo" diff --check
  git -C "$repo" diff --stat
 done
```

Confirm no secrets, generated artifacts, unrelated slides, accidental role aliases, or direct edits to generated Dart files.

- [ ] **Step 6: Run whole-branch review**

Use `superpowers:requesting-code-review` against the design and this plan. The review must classify findings as blocking or non-blocking and check spec compliance before code quality.

- [ ] **Step 7: Prepare final handoff**

Report:

```text
Completed and verified:
- exact repository/branch and commits
- exact commands/results
- implemented roles/flows/contracts

Target-only or blocked:
- unconfigured payment/settlement/hold integrations
- unavailable airspace/permit external verification
- any pending Report 5 cases

Documentation impact:
- changed Report 3/business-flow/database/API/Report 5 files

Remaining risk:
- data migration, compatibility window, deployment sequencing
```

Do not merge, push, deploy, or declare the refactor complete until all blocking review findings and failed verification checks are resolved or explicitly accepted by the user.

---

## Plan self-review checklist

- [x] Every design section maps to one or more implementation tasks.
- [x] Supporting Flow and MF1–MF5 are represented.
- [x] Backend, frontend, mobile, database, and documentation responsibilities are separated.
- [x] Six-role model and capability-as-organization-data rule are explicit.
- [x] Legacy role migration is treated as a decision/data problem, not guessed.
- [x] Each behavioral slice begins with a failing test and specifies a real command.
- [x] Cross-organization, assignment, capability independence, target-only integration, and client contract failure modes are pinned to tests.
- [x] Forward-only migrations and generated-file rules are explicit.
- [x] Report 5 IDs/history are preserved and unexecuted cases remain Pending.
- [x] No task instructs an implementer to claim deployment or external integration success without evidence.
- [x] No source code was changed while writing this plan.
