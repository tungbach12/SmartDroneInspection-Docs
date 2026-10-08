# MF1 Asset and Pair Setup Implementation Plan

> **SUPERSEDED 2026-10-08:** Use the three coordinated plans `2026-10-08-mf1-01-07-resources.md`, `2026-10-08-mf1-08-10-asset-pair.md`, and `2026-10-08-mf1-11-14-inspection-dispatch.md` for the complete MF1 scope. This earlier single-slice draft is retained only as history; do not execute it separately.

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Deliver MF1-08–MF1-10 so an ORG_ADMIN creates an organization-scoped asset with exactly one active Inspector/Drone default pair in a single transaction.

**Architecture:** Keep the use case in the `assets` module. Add only the minimal Drone read/runtime mapping and asset-pair persistence needed because V25/V26 have tables but current main has no Drone or pair Java runtime. Validate the Inspector through the existing `users.UserAccess` module boundary, derive organization from the authenticated ORG_ADMIN, and save the asset and pair atomically. Do not implement inspection creation, schedule generation, dispatch, MF2 readiness, or general workforce/Drone provisioning.

**Tech Stack:** Java 21, Spring Boot 4.1, Spring Modulith, Spring Data JPA, Flyway V24–V26 target schema, PostgreSQL Testcontainers, JUnit 5, AssertJ, MockMvc.

**Spec:** `docs/superpowers/specs/2026-10-08-mf1-asset-pair-setup-design.md`

## Global Constraints

- Current roles are exactly `ADMIN`, `ORG_ADMIN`, `INSPECTOR`, and `MAINTENANCE_ENGINEER`.
- `ORG_ADMIN` is scoped to one customer organization; organization IDs come from the authenticated principal, never the request body.
- The pair is a default operational assignment, not a Drone reservation, permit, or flight-readiness decision.
- Asset and pair are committed together or neither is committed.
- Preserve current assets module ownership and `ApiResponse<T>` / ProblemDetail conventions.
- Do not implement MF1-01–07 provisioning, MF1-11–14 inspection creation/dispatch, MF2, or any MF3/MF4 workflow.
- Do not grant `ADMIN` global asset reads or support access in this slice.
- Do not rewrite V1–V26. Add a forward migration only if verified live schema deficiencies require it; prefer no migration because V25/V26 already define the target tables and tenant constraints.
- Preserve historical Report 5 WFx IDs and outcomes; add new MF1 cases under FE-02 and the fixed `Feature 1` sheet.
- Never push, open a PR, merge, deploy, or send external messages without explicit authorization.

## Review Focus

1. **Cross-tenant identifier substitution:** same-role ORG_ADMIN supplies an Inspector or Drone ID from another organization → reject without exposing foreign data, and persist neither asset nor pair.
2. **Inactive or wrong-role workforce member:** a same-organization user is suspended or lacks INSPECTOR role → reject without partial creation.
3. **Inactive/unavailable Drone:** same-organization Drone is MAINTENANCE/SUSPENDED/RETIRED → reject without partial creation.
4. **Persistence failure after asset insert:** pair FK/unique/insert failure occurs → transaction rolls back asset and pair together.
5. **Duplicate normalized asset code:** concurrent/retried create collides with unique organization/code → return established conflict and leave no orphan pair.

---

## File Structure

```text
backend/src/main/java/com/smartdroneinspection/assets/
  api/AssetController.java                         (modify: pair fields flow through create)
  api/dto/request/CreateAssetRequest.java          (modify: required inspectorId and droneId)
  api/dto/response/AssetResponse.java              (modify: return default pair references)
  domain/Asset.java                                (modify only if accessor/ownership integration is required)
  domain/Drone.java                                (new: minimal mapping to existing drones table)
  domain/AssetPairAssignment.java                  (new: current pair aggregate/mapping)
  repository/DroneRepository.java                  (new: organization-scoped lookup)
  repository/AssetPairAssignmentRepository.java    (new: active pair lookup)
  service/AssetService.java                        (modify: validate and persist pair in same transaction)
  service/DroneService.java                        (only if Task 1 establishes a necessary minimal same-tenant Drone inventory API)
  api/DroneController.java                         (only if Task 1 establishes that the user journey otherwise cannot select an existing Drone)
  api/dto/{request,response}/Drone*                (only if Task 1 establishes this necessary current contract)
backend/src/test/java/com/smartdroneinspection/assets/
  AssetPairAssignmentTest.java                     (new: state/invariants)
  AssetPairApiIntegrationTest.java                 (new: asset+pair positive/negative/rollback tests)
  AssetApiIntegrationTest.java                     (modify: create contract and tenant scope)
  AssetPersistenceTest.java                        (modify only if mapping validation requires it)
backend/src/test/java/com/smartdroneinspection/users/
  UserAccessServiceTest.java                       (modify only if UserAccess boundary is extended)
docs/reports/report-5-test-report/
  01-test-cases/test-case-list.md                  (new MF1 cases; no historical ID changes)
  03-features/fe-02-asset-registry-inspection-schedule.md (new current MF1 cases; preserve historical WF1 section)
  02-test-statistics/test-statistics.md            (recount after execution)
  00-cover/cover.md                                (version/date/scope)
  00-cover/record-of-changes.md                    (append row)
```

---

### Task 1: Map target schema and decide the Drone-selection prerequisite

**Files:**
- Read: `backend/src/main/resources/db/migration/V25__enterprise_saas_target_schema.sql` (`drones`, `asset_pair_assignments`)
- Read: `backend/src/main/resources/db/migration/V26__enterprise_saas_runtime_cutover.sql` (composite tenant FKs and partial unique index)
- Read: `backend/src/main/java/com/smartdroneinspection/assets/api/AssetController.java`, `AssetService.java`, `CreateAssetRequest.java`, `AssetResponse.java`
- Read: `backend/src/main/java/com/smartdroneinspection/users/UserAccess.java` and `UserAccessService.java`
- Tests: `WorkflowBaselineTest`, `V25TargetSchemaFoundationTest`, `RuntimePersistenceInventoryTest`

**Interfaces:**
- Consumes: current `AssetService.create(UUID actorId, CreateAssetRequest request)`; `UserAccess.findActiveUser(UUID)`; V25/V26 tables.
- Produces: an implementation decision recorded in the execution ledger: how an ORG_ADMIN has an existing same-org ACTIVE Drone ID to select, and whether this slice needs a minimal Drone catalog write/list API or can depend on a separately delivered Drone inventory. Do not proceed to Task 2 by assuming an impossible UI/API flow.

- [ ] **Step 1: Verify runtime and migration state**

Run:

```bash
cd D:/CTP/SmartDroneInspection-Backend
git status --short -b
git rev-parse --short HEAD
grep -R "class Drone\|interface DroneRepository\|class AssetPairAssignment" src/main/java || true
grep -n "CREATE TABLE IF NOT EXISTS drones\|CREATE TABLE IF NOT EXISTS asset_pair_assignments\|uq_asset_pair_assignments_active_asset\|fk_asset_pair_assignments_.*tenant" src/main/resources/db/migration/V25__enterprise_saas_target_schema.sql src/main/resources/db/migration/V26__enterprise_saas_runtime_cutover.sql
```

Expected: no Drone/pair runtime classes; V25/V26 contain target tables and tenant constraints.

- [ ] **Step 2: Check for an existing tenant-scoped Drone management path**

Inspect current controllers and SRS. If no UI/API/manual fixture can create a Drone, include only the minimum Drone create/list capability needed to satisfy the asset-pair user journey; keep it in `assets`, require ORG_ADMIN, derive organization from principal, and reject duplicate serial numbers per organization. If another approved task is supplying this, document the exact dependency and pause this plan until it is available.

- [ ] **Step 3: Record scope ruling**

Record the chosen dependency and any API surface in the execution ledger before implementation. Explicitly state whether Drone provisioning is included; do not add workforce credential/permit verification or MF2 readiness checks.

**Verification:** no product code changes in this task; use source search and the latest schema tests as evidence.

---

### Task 2: Add failing domain and API tests for asset-pair creation

**Files:**
- Create: `backend/src/test/java/com/smartdroneinspection/assets/AssetPairAssignmentTest.java`
- Create: `backend/src/test/java/com/smartdroneinspection/assets/AssetPairApiIntegrationTest.java`
- Modify: `backend/src/test/java/com/smartdroneinspection/assets/AssetApiIntegrationTest.java`
- Reuse: `AssetTestFixture` for ORG_ADMIN, INSPECTOR, second-tenant users and category; add Drone fixtures to the owning asset test fixture only when Task 1 decides the needed Drone runtime path.

**Interfaces:**
- Consumes: V25/V26 target schema; current asset API envelope and `UserAccess` facade.
- Produces: tests that specify asset creation request includes `inspectorId` and `droneId`, pair is active/default, and asset/pair persist atomically.

- [ ] **Step 1: Write integration tests first**

Add tests for:

```text
ORG_ADMIN creates asset with same-org active Inspector and Drone → 201; exactly one asset and one ACTIVE pair
request-provided organizationId cannot widen or change organization scope
foreign-organization Inspector → denied; asset count and pair count unchanged
foreign-organization Drone → denied; asset count and pair count unchanged
same-org suspended/disabled or non-INSPECTOR user → denied; no rows persist
same-org MAINTENANCE/SUSPENDED/RETIRED Drone → denied; no rows persist
duplicate normalized asset code → 409; no orphan pair
pair persistence failure after asset flush → transaction rolls back both rows
current asset list/detail still returns only caller organization's assets
```

Use Testcontainers PostgreSQL and actual MockMvc requests; do not mock repository writes for atomicity assertions. Query both `assets` and `asset_pair_assignments` by organization/test IDs after every rejection.

- [ ] **Step 2: Run tests and verify RED**

Run:

```bash
cd D:/CTP/SmartDroneInspection-Backend
./mvnw -Dtest=AssetPairAssignmentTest,AssetPairApiIntegrationTest,AssetApiIntegrationTest test
```

Expected: compilation/test failures because request contract, pair mapping, and validation are not implemented. Fix test fixture/compilation mistakes only; do not write production code until the behavior fails for the expected missing implementation.

---

### Task 3: Implement minimal Drone and pair persistence mappings

**Files:**
- Create: `backend/src/main/java/com/smartdroneinspection/assets/domain/Drone.java`
- Create: `backend/src/main/java/com/smartdroneinspection/assets/domain/AssetPairAssignment.java`
- Create: `backend/src/main/java/com/smartdroneinspection/assets/repository/DroneRepository.java`
- Create: `backend/src/main/java/com/smartdroneinspection/assets/repository/AssetPairAssignmentRepository.java`
- Modify `package-info.java` only if an existing module API/named-interface boundary requires it.
- Migration: none unless Task 1 found a concrete schema deficiency; if so, stop and add a new forward migration plus schema tests, never alter V24–V26.

**Interfaces:**
- Consumes: V25/V26 target table names/columns and composite constraints.
- Produces:
  - `DroneRepository.findByIdAndOrganizationId(UUID droneId, UUID organizationId)`
  - `AssetPairAssignmentRepository.findByAssetIdAndStatus(UUID assetId, PairAssignmentStatus.ACTIVE)`
  - minimal asset-pair creation method with organization, asset, Inspector, Drone, start time, and assigning ORG_ADMIN.

- [ ] **Step 1: Add mapping tests or extend persistence validation tests**

Pin table/column names, `serviceability`, pair status/validity, and V26 composite tenant FKs. Test the real Flyway schema with Hibernate validation.

- [ ] **Step 2: Implement the minimal JPA mappings and repositories**

Map only fields used by MF1-08–10. Do not add Drone documents, permits, qualification workflows, history editing, or generic abstractions here.

- [ ] **Step 3: Run mapping tests**

Run:

```bash
./mvnw -Dtest=AssetPairAssignmentTest,AssetPersistenceTest,PersistenceEntityMappingTest,PersistenceEntityOwnershipTest test
```

Expected: focused mappings pass and Modulith ownership remains `assets`-owned; no `assets` import of `workforce` HTTP APIs.

---

### Task 4: Implement atomic, organization-scoped create with pair

**Files:**
- Modify: `backend/src/main/java/com/smartdroneinspection/assets/api/dto/request/CreateAssetRequest.java`
- Modify: `backend/src/main/java/com/smartdroneinspection/assets/api/dto/response/AssetResponse.java`
- Modify: `backend/src/main/java/com/smartdroneinspection/assets/service/AssetService.java`
- Modify: `backend/src/main/java/com/smartdroneinspection/assets/api/AssetController.java` only if response construction/request signature needs adjustment.
- Modify/extend: `backend/src/main/java/com/smartdroneinspection/users/UserAccess.java` and implementation/test only if needed to expose an active Inspector's role/scope through the existing module boundary.

**Interfaces:**
- Consumes: `DroneRepository.findByIdAndOrganizationId`, `UserAccess.findActiveUser`, `AssetPairAssignmentRepository`, current category and asset repositories.
- Produces: `AssetService.create(UUID actorId, CreateAssetRequest request)` creates the asset and default pair in one `@Transactional` method; typed request requires `inspectorId`, `droneId`; response identifies their IDs and active pair reference without claiming dispatch/readiness.

- [ ] **Step 1: Implement typed request validation**

Add `@NotNull UUID inspectorId` and `@NotNull UUID droneId`. Do not accept `organizationId`.

- [ ] **Step 2: Implement actor and resource validation before writes**

Resolve the active actor through `UserAccess`; require `ORG_ADMIN` and non-null organization. Resolve Inspector and Drone with organization-scoped queries. Require Inspector active with role `INSPECTOR`; require Drone `ACTIVE`. Resolve active category. Foreign-tenant records return `404 NOT_FOUND`; same-tenant unavailable/wrong-role resources return stable validation or conflict ProblemDetail. Preserve existing duplicate-code conflict.

- [ ] **Step 3: Implement transaction with both writes**

Within the same `@Transactional` method, save asset, create an ACTIVE default pair with assigning actor/time and `valid_from`, and flush pair before returning. Any pair failure must propagate and roll back the asset. Do not catch persistence errors and continue.

- [ ] **Step 4: Map response and verify focused RED→GREEN**

Run:

```bash
./mvnw -Dtest=AssetPairAssignmentTest,AssetPairApiIntegrationTest,AssetApiIntegrationTest test
```

Expected: all positive and negative tests pass; asset and pair row counts match their atomicity assertions.

---

### Task 5: Documentation and Report 5 evidence

**Files:**
- Modify: `reports/report-3-software-requirement-specification/03-functional-requirements.md` §3.3.1, only if implemented request/response/error details clarify the contract.
- Modify: `reports/report-3-software-requirement-specification/00-record-of-changes.md`
- Modify: `project-reference/business-flows.md` MF1-08–10 only if behavior/text must be clarified.
- Modify: `project-reference/database-design.md` implementation status only if mapping/schema changed; target table definitions remain authoritative.
- Modify: `backend/flows/assets-and-scheduling.md` into current MF1 asset/pair setup reference or add a current MF1 asset setup page; remove claims that the removed schedule-proposal workflow is current.
- Modify: Report 5 `01-test-cases/test-case-list.md`, `03-features/fe-02-asset-registry-inspection-schedule.md`, `02-test-statistics/test-statistics.md`, `00-cover/cover.md`, `00-cover/record-of-changes.md`.

**Interfaces:**
- Consumes: executed Task 2–4 tests and actual final API/schema behavior.
- Produces: new stable target test IDs for MF1-08–10, traced to `FE-02`, `MF1`, fixed workbook sheet `Feature 1`; do not change historical WF1-001–WF1-019 IDs or statuses.

- [ ] **Step 1: Add test-case index rows**

Add cases for atomic asset+pair creation, duplicate code, foreign Inspector/Drone rejection, inactive/wrong-role resource rejection, rollback after pair persistence failure, and tenant-scoped read. Use new stable IDs; do not reuse historical IDs or alter historical WF1 outcomes.

- [ ] **Step 2: Record actual results only**

In the FE-02 detailed feature source, include procedure, expected result, preconditions, execution status, exact date/tester, and test method evidence. Keep all not-yet-run cases Pending.

- [ ] **Step 3: Recount statistics/cover**

Recalculate Feature 1 and grand total from the detailed sources; update cover version/date and append report change history. Preserve historical outcomes.

- [ ] **Step 4: Verify docs**

Run `git diff --check`, check all new links, and reconcile Report 3/business-flow/database/API statements with the code actually delivered.

---

## Final Verification

```bash
cd D:/CTP/SmartDroneInspection-Backend
./mvnw spotless:check
./mvnw verify
cd D:/CTP/SmartDroneInspection-Frontend
npm run lint
npm test
npm run build
cd D:/CTP/SmartDroneInspection-Docs
git diff --check
```

No frontend/mobile behavior is planned; do not edit those repositories in this slice. Run frontend checks only if the shared API contract is changed there by an explicitly approved follow-up.
