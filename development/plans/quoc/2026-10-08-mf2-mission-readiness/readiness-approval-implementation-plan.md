# MF2-07 Readiness Approval Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:subagent-driven-development` (recommended) or `superpowers:executing-plans` to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implement MF2-07 as a fail-closed, independently reviewed readiness decision that only moves a current submitted preparation and its inspection to `READY_FOR_FLIGHT` after scoped credential, permit, pair, Drone-document and reviewer-attestation checks pass.

**Architecture:** `workforce` owns credential persistence and exposes immutable read summaries through `workforce::credential`; `assets` owns Drone-document persistence and exposes immutable read summaries through `assets::readiness`. `inspections` consumes only those named interfaces and owns preparation-state changes, the transactional review service, canonical snapshots and source hashing. Commit 13 includes these three modules' minimum reader/service code in one logical backend commit; HTTP routes and material-change invalidation remain commit 14.

**Tech Stack:** Java 21, Spring Boot 4.1, Spring Modulith 2.1, Spring Data JPA, Hibernate JSONB support, PostgreSQL 17/Testcontainers, JUnit 5, AssertJ, Maven Wrapper, Spotless.

**Spec:** `development/plans/quoc/2026-10-08-mf2-mission-readiness/readiness-approval-design.md`

## Global Constraints

- Roles remain `ADMIN`, `ORG_ADMIN`, `INSPECTOR`, `MAINTENANCE_ENGINEER`; an `ORG_ADMIN` role alone does not establish reviewer qualification.
- Reviewer credential must belong to the active reviewer and organization, be `ACTIVE`, carry internal verification attribution and source-evidence reference, and have non-null issue/expiry bounds covering `decided_at` for both approve and return; approve additionally requires coverage at `planned_start`.
- Selected Inspector credentials must be scoped to the assigned user and organization, `ACTIVE`, internally verified with source-evidence attribution, and have non-null issue/expiry bounds covering planned start. Selected Drone documents must be scoped through the assigned Drone and its organization, `ACTIVE`, internally reviewed with reviewer/time attribution, and have non-null validity bounds covering planned start; V25 has no evidence FK on Drone documents, so do not require one.
- Null issue/expiry or valid-from/valid-until bounds fail closed for approval.
- Credential type is free-form; the qualified reviewer attests applicability by `applicabilityComplete=true` and a traceable `applicabilityBasisReference`. Empty category selections also require a category-specific non-applicability reason; a free-form reason without a traceable basis is insufficient.
- Machine-checkable permit blockers (`PERMIT_MISSING`, `PERMIT_NOT_ISSUED`, `EXEMPTION_BASIS_MISSING`, invalid/expired) are never overridable by reviewer attestation.
- Missing records are never interpreted as “not applicable”; missing/invalid readiness-only records may be documented and returned for remediation but do not block the return operation.
- `inspection_preparations` has no organization column; tenant scope must be enforced through the owning inspection.
- Lock the inspection and preparation for review; decision insert, preparation transition and inspection transition must be one transaction.
- No Flyway migration, no HTTP endpoint/DTO, no change invalidation, no frontend/mobile work in this slice.
- Keep the original 20-commit delivery accounting: MF2 readiness design and implementation are the planned commit 13 scope; commit 14 remains API/invalidation. Do not add standalone feature commits for individual module readers.
- Never commit secrets, tokens, local `.env` files, generated files or unrelated work.

## Review Focus

1. **Reviewer or assigned Inspector absent, inactive, cross-tenant, or same person:** refuse review before writing a decision; test in Task 7.
2. **Credential/document id belongs to another user, organization, inspection Drone, or is not found:** fail closed and write no decision; tests in Tasks 2, 4 and 7.
3. **Credential is pending/unverified/evidence-less or has null/out-of-window issue/expiry bounds; Drone document is pending/unreviewed or has null/out-of-window validity bounds:** fail closed; credentials require evidence attribution, while Drone documents require reviewer/time attribution (V25 has no evidence FK); tests in Tasks 2, 4 and 7.
4. **Inspection has no planned start, current pair with `assignment_response=ACCEPTED` and `responded_at < planned_start`, pair validity covering planned start, usable Drone, current submitted preparation, clear non-overridable permit gate, or required applicability/human-verification basis:** approval is refused without partial state; tests in Tasks 5–7.
5. **Concurrent reviews or late persistence/hash failure:** at most one decision wins and no partial transition remains; tests in Task 7 where reproducible with PostgreSQL.

---

### Task 1: Workforce credential persistence model

**Files:**
- Create: `src/main/java/com/smartdroneinspection/workforce/domain/enums/WorkforceCredentialStatus.java`
- Create: `src/main/java/com/smartdroneinspection/workforce/domain/WorkforceCredential.java`
- Create: `src/test/java/com/smartdroneinspection/workforce/WorkforceCredentialPersistenceTest.java`
- Modify: `src/test/java/com/smartdroneinspection/database/RuntimePersistenceInventoryTest.java`

**Interfaces:**
- Consumes: existing V25 `workforce_credentials` table.
- Produces: JPA entity `WorkforceCredential`, with exact Java fields `organizationId`, `userId`, `credentialType`, `issuer`, `credentialReference`, `issuedAt`, `expiresAt`, `status`, `evidenceId`, `verifiedByUserId`, `verifiedAt`, `verificationReason`, `createdAt`, `updatedAt`, and `rowVersion`; no cross-module exposure yet.

- [ ] **Step 1: Write the persistence test first.** Use `@SpringBootTest`, `@Import(TestcontainersConfiguration.class)`, `@Transactional`, `EntityManager` and `JdbcTemplate`. Insert an organization and an active ORG_ADMIN via the existing `UserRepository`; insert a credential row with `status='ACTIVE'`, dates, evidence UUID, verifier UUID/time/reason, then `entityManager.find(WorkforceCredential.class, id)` and assert mapped owner, status, evidence and verification attribution. This must fail to compile because the entity/status enum do not exist.
- [ ] **Step 2: Run RED.** Run `./mvnw.cmd test -Dtest=WorkforceCredentialPersistenceTest`; expected: test compile failure naming the missing production types, not a Docker or formatter error.
- [ ] **Step 3: Implement only the mapping.** Map V25 columns exactly: `id`, `organization_id`, `user_id`, `credential_type`, `issuer`, `credential_reference`, `issued_at`, `expires_at`, `status`, `evidence_id`, `verified_by_user_id`, `verified_at`, `verification_reason`, `created_at`, `updated_at`, `row_version`. Use `@Version` for `row_version`; store times as `Instant`; status enum must contain exactly `DRAFT`, `PENDING_REVIEW`, `ACTIVE`, `EXPIRING_SOON`, `EXPIRED`, `REJECTED`, `SUSPENDED`. Do not add CRUD workflow or an `isQualified` rule to the entity.
- [ ] **Step 4: Register the entity and run GREEN.** Add `workforce_credentials` to `RUNTIME_ENTITY_TABLES`; run `./mvnw.cmd test -Dtest=WorkforceCredentialPersistenceTest,RuntimePersistenceInventoryTest`; expected: both persistence round-trip and table inventory pass on PostgreSQL 17.
- [ ] **Step 5: Format and inspect.** Run `./mvnw.cmd spotless:apply`, then `./mvnw.cmd test -Dtest=WorkforceCredentialPersistenceTest,RuntimePersistenceInventoryTest`; inspect `git diff --check` before continuing.

### Task 2: Workforce-owned credential read interface

**Files:**
- Create: `src/main/java/com/smartdroneinspection/workforce/credential/WorkforceCredentialAccess.java`
- Create: `src/main/java/com/smartdroneinspection/workforce/credential/WorkforceCredentialSummary.java`
- Create: `src/main/java/com/smartdroneinspection/workforce/credential/package-info.java`
- Create: `src/main/java/com/smartdroneinspection/workforce/service/WorkforceCredentialAccessService.java`
- Create: `src/main/java/com/smartdroneinspection/workforce/repository/WorkforceCredentialRepository.java`
- Create: `src/main/java/com/smartdroneinspection/workforce/repository/package-info.java`
- Modify: `src/main/java/com/smartdroneinspection/workforce/package-info.java`
- Create: `src/test/java/com/smartdroneinspection/workforce/WorkforceCredentialAccessIntegrationTest.java`

**Interfaces:**
- Consumes: `WorkforceCredential` and its repository, both internal to `workforce`.
- Produces: named interface `workforce::credential`; exact method `Optional<WorkforceCredentialSummary> findByIdAndOrganizationIdAndUserId(UUID credentialId, UUID organizationId, UUID userId)`. Summary fields: id, organizationId, userId, credentialType, issuer, credentialReference, issuedAt, expiresAt, status, evidenceId, verifiedByUserId, verifiedAt, verificationReason. No JPA type crosses the boundary.

- [ ] **Step 1: Write the boundary integration test.** Persist credentials for the reviewer, another user in the same organization, and a user in another organization. Assert the public access service returns the summary only for the exact `(credentialId, organizationId, userId)` tuple and returns empty for each mismatched tuple. Test the real repository/service, not a mocked repository.
- [ ] **Step 2: Run RED.** Run `./mvnw.cmd test -Dtest=WorkforceCredentialAccessIntegrationTest`; expected: compile failure for the absent interface/service/repository.
- [ ] **Step 3: Implement scoped repository and named interface.** Derive the finder `findByIdAndOrganizationIdAndUserId`; implement the service as a direct read-only mapping to the summary record. Add `@Transactional(readOnly=true)` at the application boundary. Expose only package `workforce.credential`; do not expose `workforce.domain` or `workforce.repository`.
- [ ] **Step 4: Verify Modulith dependency.** Add `workforce::credential` to inspections' allowed dependencies only in Task 5; for this task, run `./mvnw.cmd test -Dtest=WorkforceCredentialAccessIntegrationTest,ModulithArchitectureTest` and ensure Workforce remains dependent only on `shared` and `users`.
- [ ] **Step 5: Format and inspect.** Run Spotless and `git diff --check`; confirm the access contract imports no JPA annotations, repositories or entity classes in its public signature.

### Task 3: Assets Drone-document persistence model

**Files:**
- Create: `src/main/java/com/smartdroneinspection/assets/domain/DroneDocument.java`
- Create: `src/main/java/com/smartdroneinspection/assets/domain/enums/DroneDocumentStatus.java`
- Create: `src/main/java/com/smartdroneinspection/assets/repository/DroneDocumentRepository.java`
- Modify: `src/test/java/com/smartdroneinspection/database/RuntimePersistenceInventoryTest.java`
- Create: `src/test/java/com/smartdroneinspection/assets/DroneDocumentPersistenceTest.java`

**Interfaces:**
- Consumes: V25 `drone_documents`, with parent `drones`.
- Produces: assets-owned entity and repository. Status vocabulary is `PENDING_REVIEW`, `ACTIVE`, `EXPIRED`, `REJECTED`, `REVOKED`.

- [ ] **Step 1: Write the PostgreSQL mapping test.** Insert a Drone and a document with active status, validity, object key/checksum, uploader and reviewer attribution; load it through JPA and assert source fields. Assert missing `reviewed_by_user_id`/`reviewed_at` remain null and can be distinguished from reviewed records. This fails before the entity/repository exists.
- [ ] **Step 2: Run RED.** Run `./mvnw.cmd test -Dtest=DroneDocumentPersistenceTest`; expected: missing entity/repository compilation error.
- [ ] **Step 3: Map schema without inventing policy.** Map V25 fields including `drone_id`, type, issuer/reference, validity, status, storage key/checksum, uploader/reviewer/time, and `created_at`. Use enum values exactly matching the CHECK constraint. Do not infer which types are mandatory; the schema has no mandatory flag.
- [ ] **Step 4: Add the exact scoped repository lookup.** Implement `@Query("select document from DroneDocument document join Drone drone on drone.id = document.droneId where drone.organizationId = :organizationId and document.droneId = :droneId and document.id in :documentIds") List<DroneDocument> findForReadiness(@Param("organizationId") UUID organizationId, @Param("droneId") UUID droneId, @Param("documentIds") Collection<UUID> documentIds)`. Return no storage object key through the public cross-module DTO. For an empty ID list, the access service returns `List.of()` without issuing the `IN` query.
- [ ] **Step 5: Register and verify.** Add `drone_documents` to the runtime entity inventory. Run `./mvnw.cmd test -Dtest=DroneDocumentPersistenceTest,RuntimePersistenceInventoryTest` and require real PostgreSQL success.

### Task 4: Assets-owned readiness source interface (Drone document and assignment pair)

**Files:**
- Create: `src/main/java/com/smartdroneinspection/assets/readiness/DroneDocumentReadinessAccess.java`
- Create: `src/main/java/com/smartdroneinspection/assets/readiness/DroneDocumentSummary.java`
- Create: `src/main/java/com/smartdroneinspection/assets/readiness/AssetPairReadinessSummary.java`
- Create: `src/main/java/com/smartdroneinspection/assets/readiness/package-info.java`
- Create: `src/main/java/com/smartdroneinspection/assets/service/DroneDocumentReadinessAccessService.java`
- Modify: `src/main/java/com/smartdroneinspection/assets/repository/AssetPairAssignmentRepository.java`
- Modify: `src/main/java/com/smartdroneinspection/assets/package-info.java`
- Create: `src/test/java/com/smartdroneinspection/assets/DroneDocumentReadinessAccessIntegrationTest.java`

**Interfaces:**
- Consumes: assets-internal Drone, DroneDocument, and AssetPairAssignment repositories/entities.
- Produces: named interface `assets::readiness`; method `List<DroneDocumentSummary> findForDrone(UUID organizationId, UUID droneId, List<UUID> documentIds)` and `Optional<AssetPairReadinessSummary> findPairForInspection(UUID organizationId, UUID pairId, UUID assetId)`.
- `DroneDocumentSummary`: document ID, Drone ID, document type, issuer/reference, valid-from/until, status, reviewed-by/at, uploaded-by, created-at, checksum; exclude `object_key`.
- `AssetPairReadinessSummary`: pair ID, organization ID, asset ID, inspector user ID, Drone ID, pair status, valid-from/until, assignment response and responded-at. The repository finder scopes all of organization/pair/asset; caller checks response chronology against planned start. No JPA type crosses the interface.

- [ ] **Step 1: Write scope integration tests.** Assert a requested ID belonging to the correct Drone/organization is returned; IDs from another Drone or organization are never returned; an unknown ID is omitted so the caller can detect incomplete resolution; returned summary omits object key by type design. Also create V27 pair fixtures for same-org and cross-org pairs; assert `findPairForInspection` only resolves the exact organization/pair/asset tuple and returns response/time fields without exposing the JPA entity.
- [ ] **Step 2: Run RED.** Run `./mvnw.cmd test -Dtest=DroneDocumentReadinessAccessIntegrationTest`; expected: missing interface implementation compilation failure.
- [ ] **Step 3: Implement read-only adapter.** Resolve only documents matching both requested IDs and the target Drone, and ensure parent Drone organization matches. Return immutable summaries sorted by document UUID for stable downstream snapshots. No “applicable” or “mandatory” inference belongs in assets.
- [ ] **Step 4: Expose only the named interface.** Add `assets::readiness` as a named interface; do not allow inspections to import `DroneDocument` or its repository. Add the interface dependency to inspections in Task 5 only.
- [ ] **Step 5: Verify assets behavior.** Run `./mvnw.cmd test -Dtest=DroneDocumentReadinessAccessIntegrationTest,ModulithArchitectureTest`; then inspect the Modulith model for no dependency cycle.

### Task 5: Preparation state transition and review locks/repository

**Files:**
- Modify: `src/main/java/com/smartdroneinspection/inspections/service/InspectionPreparationService.java`
- Modify: `src/main/java/com/smartdroneinspection/inspections/domain/Inspection.java`
- Modify: `src/main/java/com/smartdroneinspection/inspections/repository/InspectionRepository.java`
- Modify: `src/main/java/com/smartdroneinspection/inspections/repository/InspectionPreparationRepository.java`
- Create: `src/main/java/com/smartdroneinspection/inspections/repository/InspectionReadinessDecisionRepository.java`
- Modify: `src/main/java/com/smartdroneinspection/inspections/package-info.java`
- Modify: `src/test/java/com/smartdroneinspection/inspections/InspectionPreparationServiceTest.java`
- Modify: `src/test/java/com/smartdroneinspection/database/RuntimePersistenceInventoryTest.java`

**Interfaces:**
- Consumes: current Inspection, Preparation and ReadinessDecision entities plus the `workforce::credential` and `assets::readiness` read interfaces.
- Produces: `InspectionRepository.findWithLockByIdAndOrganizationId(UUID id, UUID organizationId)`, `InspectionPreparationRepository.findWithLockByIdAndInspectionId(UUID id, UUID inspectionId)`, and `InspectionReadinessDecisionRepository.findFirstByInspectionIdOrderByDecidedAtDesc(UUID inspectionId)`; `ASSIGNED -> PREPARING` transition when preparation starts.

- [ ] **Step 1: Add preparation transition tests first.** Add cases to `InspectionPreparationServiceTest`: first draft on an `ASSIGNED` inspection leaves status `PREPARING`; editing an existing draft in `PREPARING` stays there; attempting to prepare an inspection in `READY_FOR_FLIGHT` is refused with no mutation. Run `./mvnw.cmd test -Dtest=InspectionPreparationServiceTest`; the new status assertions must fail before production changes.
- [ ] **Step 2: Implement the transition narrowly.** In `prepareShotList`, when no draft exists, require `ASSIGNED` and call a domain transition dedicated to `PREPARING`; allow edits when already `PREPARING`; refuse all other statuses. Save both preparation and inspection in the existing transaction.
- [ ] **Step 3: Add locked review finders.** In `InspectionRepository`, add `findWithLockByIdAndOrganizationId` using `PESSIMISTIC_WRITE`. In `InspectionPreparationRepository`, add a query that locks only when preparation ID and inspection ID match, and a finder for the latest preparation version. Do not accept an organization from the request; service derives it from `UserAccess`.
- [ ] **Step 4: Add readiness decision repository.** Create `InspectionReadinessDecisionRepository extends JpaRepository<InspectionReadinessDecision, UUID>` with a scoped history finder by inspection and a latest-decision finder. Add `inspection_readiness_decisions` to `RUNTIME_ENTITY_TABLES` if not already present.
- [ ] **Step 5: Run repository/query checks.** Run `./mvnw.cmd test -Dtest=InspectionPreparationServiceTest,InspectionReadinessDecisionPersistenceTest,RuntimePersistenceInventoryTest,ModulithArchitectureTest`; expected: all derived queries parse at context startup, status transition cases pass, inventory stays exact.

### Task 6: Review command and deterministic source snapshot/hash

**Files:**
- Create: `src/main/java/com/smartdroneinspection/inspections/service/ReadinessReviewCommand.java`
- Create: `src/main/java/com/smartdroneinspection/inspections/service/ReadinessSnapshotFactory.java`
- Create: `src/test/java/com/smartdroneinspection/inspections/ReadinessSnapshotFactoryTest.java`

**Interfaces:**
- `ReadinessReviewCommand` fields: `UUID reviewerCredentialId`, `List<UUID> inspectorCredentialIds`, `List<UUID> droneDocumentIds`, `boolean applicabilityComplete`, `String applicabilityBasisReference`, `String noInspectorCredentialReason`, `String noDroneDocumentReason`, `String humanVerificationBasis`.
- `ReadinessReturnCommand` fields: `UUID reviewerCredentialId`, `List<UUID> inspectorCredentialIdsObserved`, `List<UUID> droneDocumentIdsObserved`, `String reason`. Its source lists are exactly the records the reviewer observed/attempted to inspect; persist submitted IDs, resolved summaries and unresolved IDs. Always set `observedSourceSetComplete=false` unconditionally because reviewer-selected IDs are not an exhaustive registry. An empty list records an empty observed set only, not non-applicability or completeness.
- `ReadinessFinding` is a stable `(String code, String detail)` record.
- `ReadinessSnapshotInput` contains decision type, inspection, preparation, optional pair, compliance result, reviewer/source summaries, command attestations, exact observed IDs and unresolved IDs.
- `ReadinessSnapshotFactory.create(ReadinessSnapshotInput) -> Snapshot`; `Snapshot` has the V25 JSON strings/ID arrays `permitSnapshot`, `permitSnapshotIds`, `credentialSnapshot`, `credentialSnapshotIds`, `droneDocumentSnapshot`, `droneDocumentSnapshotIds`, and lowercase 64-character SHA-256 hex `sourceHash`.
- `permitSnapshot.source_envelope` durably stores inspection objective, scope, component_scope, acceptance criteria, schedule ID/due-cycle, planned window, exact pair/response facts, full submitted preparation content/version, and return observed-ID completeness metadata. Return always records `observedSourceSetComplete=false`, because the command list is reviewer-selected rather than an exhaustive registry. Preserve the exact submitted IDs and unresolved IDs. This preserves source values instead of relying on a hash to reconstruct them.

- [ ] **Step 1: Write snapshot behavior tests.** Assert equivalent source objects in a different input-list order produce byte-identical snapshot strings and identical hash after sorting by UUID. Assert changing a selected credential expiry, permit status, applicability basis, human-verification basis, inspection scope, pair response time or preparation version changes the hash. Assert `permit_snapshot.source_envelope` contains objective/scope/component scope/acceptance criteria/schedule/due cycle/planned window/pair facts/full submitted preparation content. Test both decision types; for RETURNED assert exact selected source IDs, unresolved IDs and `observedSourceSetComplete=false`, including an empty observed list. Calculate expected SHA-256 from a literal documented canonical UTF-8 payload fixture.
- [ ] **Step 2: Run RED.** Run `./mvnw.cmd test -Dtest=ReadinessSnapshotFactoryTest`; expected: missing command/factory compile failure.
- [ ] **Step 3: Implement stable snapshot records.** Define fixed-field source records and a shared `ReadinessSnapshotInput` containing decision type, inspection/pair, preparation, compliance, credential/document summaries, attestations, explicitly observed source IDs and unresolved source IDs. Factory returns the six V25 JSON/ID columns plus hash. Sort collections by UUID, serialize stable records with Jackson 3, and hash canonical UTF-8 bytes with SHA-256 lowercase hex.
- [ ] **Step 4: Verify hash contract.** Run `./mvnw.cmd test -Dtest=ReadinessSnapshotFactoryTest`; expected: stable hash for reordered inputs, changed hash for each material source mutation, and exact observed-set metadata for RETURNED.

### Task 7: Readiness review service—test first, then implement

**Files:**
- Create: `src/main/java/com/smartdroneinspection/inspections/service/InspectionReadinessService.java`
- Modify: `src/test/java/com/smartdroneinspection/inspections/InspectionReadinessServiceTest.java`
- Modify: `src/main/java/com/smartdroneinspection/inspections/service/ComplianceGateService.java` only if needed to expose machine findings without leaking HTTP DTOs; otherwise adapt through its existing response.

**Interfaces:**
- `approve(UUID reviewerId, UUID inspectionId, UUID preparationId, ReadinessReviewCommand command) -> InspectionReadinessDecision`
- `returnPreparation(UUID reviewerId, UUID inspectionId, UUID preparationId, ReadinessReturnCommand command) -> InspectionReadinessDecision`
- Consumes repositories, `UserAccess`, `ComplianceGateService`, `WorkforceCredentialAccess`, `DroneDocumentReadinessAccess`, and `ReadinessSnapshotFactory`.

- [ ] **Step 1: Adapt and complete integration tests.** Keep all fixtures real with PostgreSQL/Testcontainers. Add credential/document rows through owning repositories or explicit SQL fixture helpers. All approval calls take a `ReadinessReviewCommand` with reviewer credential ID and applicability attestations; all return calls take a `ReadinessReturnCommand` with reviewer credential ID and the observed source IDs. Required behavior: independent ORG_ADMIN approves with valid reviewer/Inspector credentials, selected reviewed Drone document, applicable permit, complete attestations; assigned Inspector/same-person reviewer, wrong role, inactive user, wrong org and foreign preparation are refused; wrong-owner, missing-verification/evidence attribution, inactive, expired and null-date credential records are refused; Drone document missing review attribution, wrong Drone/organization, missing/invalid selected Drone docs and permit blockers are refused; empty approval lists without traceable basis and missing human-verification basis are refused; return remains possible with missing readiness evidence when reason/reviewer credential are valid at `decidedAt`, records exactly observed IDs and sets `observedSourceSetComplete=false` unconditionally; non-current/non-submitted/ready/returned preparations cannot be reviewed; pair response at/after planned start is refused; mutation of each snapshotted plan/preparation/pair/source field changes the hash and JSON input list order does not.
- [ ] **Step 2: Run RED.** Run `./mvnw.cmd test -Dtest=InspectionReadinessServiceTest`; expected: test compile failure naming missing service and/or required readiness interfaces. Resolve fixture compile errors without adding production code.
- [ ] **Step 3: Implement reviewer actor and scope checks.** Resolve active user through `UserAccess`; require `ORG_ADMIN` and non-null organization; load/lock inspection within that organization; require `inspection.status == PREPARING`; reject when `reviewerId == inspection.inspectorId`. Load exact latest preparation under lock; require matching inspection, newest version and `SUBMITTED`. Use stable BusinessException codes specified in the spec.
- [ ] **Step 4: Implement credential and document validation.** Resolve selected reviewer credential with `(id, organizationId, reviewerId)` through Workforce SPI; require ACTIVE, verifier ID/time, evidence ID and non-null `issuedAt <= decidedAt <= expiresAt` for both decisions; approval additionally requires `issuedAt <= plannedStart <= expiresAt`. Resolve every supplied Inspector credential by exact assigned Inspector and organization; require ACTIVE, verification/evidence attribution, non-null issue/expiry bounds and validity at planned start. Resolve every requested Drone document for exact assigned Drone/organization; require the complete ID set resolved, ACTIVE, reviewer/time attribution, non-null validity bounds and coverage of planned start. Null bounds block approval. Reject missing `applicabilityComplete`, blank basis reference, empty-list category reason, and missing `humanVerificationBasis` when required. Do not silently accept omitted IDs or treat an empty list as exemption.
- [ ] **Step 5: Implement pair and machine-gate validation.** Require non-null planned start and end; resolve the inspection's pair via `AssetPairReadinessSummary` scoped by organization/pair/asset; require pair status `ACTIVE`, response `ACCEPTED`, `respondedAt != null && respondedAt.isBefore(plannedStart)`, `validFrom <= plannedStart`, and `validUntil == null || validUntil >= plannedStart`; require pair Inspector/Drone/asset exactly match inspection snapshot. Require current Drone `ACTIVE`. Evaluate ComplianceGate; every machine blocker is non-overridable and prevents approval. If human verification is flagged, require explicit attestation and a nonblank traceable basis reference.
- [ ] **Step 6: Implement atomic approve/return transitions.** Build a `ReadinessSnapshotInput`; persist `InspectionReadinessDecision` and state changes in one transaction. Approval marks preparation `READY` and inspection `PREPARING -> READY_FOR_FLIGHT`. Return command includes reviewer credential ID and explicit observed Inspector-credential/Drone-document IDs. Require that reviewer credential be `ACTIVE`, owned by the reviewer/org, have verification/evidence attribution, and have non-null issue/expiry bounds covering `decidedAt`; do not require planned-time/pair/permit/Inspector credential/Drone document readiness gates. Require a reason; read only supplied source IDs, persist resolved summaries, exact requested/unresolved IDs and `observedSourceSetComplete=false`, mark preparation `RETURNED`, and leave inspection `PREPARING`. Empty observed IDs are not non-applicability. Authorization/current-preparation/reason validation must precede writes; database failure rolls back all writes.
- [ ] **Step 7: Run service integration tests.** Run `./mvnw.cmd test -Dtest=InspectionReadinessServiceTest,ReadinessSnapshotFactoryTest,WorkforceCredentialAccessIntegrationTest,DroneDocumentReadinessAccessIntegrationTest`; expected: all approval, return, ownership, gate, JSON and hash cases pass against real PostgreSQL. Include a V27 pair whose `responded_at` equals or follows `planned_start`; approval must fail and leave all state unchanged.
- [ ] **Step 8: Run architecture and source-format checks.** Run `./mvnw.cmd test -Dtest=ModulithArchitectureTest,RuntimePersistenceInventoryTest`; run `./mvnw.cmd spotless:check`; fix only commit-13 issues.

### Task 8: Documentation synchronization and final commit 13 verification

**Files:**
- Modify: `SmartDroneInspection-Docs/reports/report-3-software-requirement-specification/03-functional-requirements.md` MF2-06/07 rows and `00-record-of-changes.md` if implementation tightens the observable requirement.
- Modify: `SmartDroneInspection-Docs/project-reference/business-flows.md` MF2-06/07 details for reviewer credential and attributable applicability attestation.
- Modify: Report 5 editable Markdown case index, FE-03 detail and statistics/cover/history for the added approval/denial cases, following AGENTS.md; do not invent execution evidence or mark tests passed until run.
- No frontend/mobile/API contract changes in commit 13; commit 14 handles the API.

- [ ] **Step 1: Update docs from actual implemented behavior only.** State that reviewer must be a separate active ORG_ADMIN with a recorded ACTIVE credential and evidence/verification attribution, and that the reviewer explicitly attests document applicability. Clearly state internal record validation does not verify with an authority. Do not claim all national aviation rules are automatically checked.
- [ ] **Step 2: Update Report 5 test traceability.** Add cases using stable FE/WF IDs and workbook sheet mapping only after verifying next available IDs and existing FE-03 section; record execution date/status based on the actual test run. Recount statistics and change history as prescribed by repository AGENTS.md.
- [ ] **Step 3: Inspect cross-repository diffs.** In Backend and Docs separately, run `git diff --check`, `git status --short`, inspect staged/untracked files and ensure no generated artifacts, secrets or unrelated changes.
- [ ] **Step 4: Run full Backend verification.** From `SmartDroneInspection-Backend`, run `./mvnw.cmd clean verify` with Java 21 and Docker available. Expected: all tests pass, JaCoCo gate met and Modulith boundaries pass. Report any known pre-existing issue rather than hiding it.
- [ ] **Step 5: Run Docs checks.** From `SmartDroneInspection-Docs`, run `git diff --check`; run Hugo build only if the repository/theme toolchain is available.
- [ ] **Step 6: Commit only after all required verification.** Keep the Backend implementation grouped as MF2 commit 13; use a focused Docs commit if documentation traceability requires a separate repository commit, counting it against the team's overall 20-commit accounting before later group-F commits. Do not push.

## Required implementation handoff

- Report exact Backend and Docs commands and outcomes.
- Note that credential/document eligibility is internal-record validation, not issuer registry verification.
- Note that commit 14 API and change invalidation are intentionally pending.
- List changed files and any failure or blocked check; do not claim readiness end-to-end until the API and field-session commits are complete.
