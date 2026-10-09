# MF2-07/08 Readiness Approval - Design

**Status:** Approved for implementation planning
**Owner:** Quoc
**Date:** 2026-10-08
**Scope:** Backend readiness-review service and its owning-module read contracts; no HTTP API or change-invalidation implementation in this design stage.

## 1. Purpose and decisions already approved

Implement the MF2-07 decision that reviews one submitted preparation and may move an inspection to `READY_FOR_FLIGHT` only when machine-checkable gates pass and the qualified reviewer attests that the applicable compliance basis is complete. An approval records who reviewed which preparation and source records; a return records a reason without making the inspection ready.

Decisions agreed with the user:

- Reviewer qualification must not be inferred from `ORG_ADMIN` role alone.
- Use approach A: credential access remains owned by `workforce`; `inspections` consumes a narrow, read-only named interface, not workforce persistence entities or repositories.
- The reviewer identifies an active credential belonging to them and attests it is appropriate to this inspection's scope. This records an internal review assertion; it is not authority-registry verification or proof of statutory authority.
- The reviewer explicitly attests whether the applicable Inspector credentials and Drone documents are complete. Where no document is applicable, the reviewer records that determination and its basis.
- Missing, invalid, expired, wrong-owner, or wrong-organization records fail closed. No approval is created while a machine-checkable blocker remains.
- Path A: starting preparation moves an `ASSIGNED` inspection to `PREPARING`; only a current submitted preparation on a `PREPARING` inspection can be reviewed.
- Keep commit 14 (HTTP API and material-change invalidation) out of commit 13 implementation.

## 2. Module boundaries and contracts

### Workforce owns credentials

Add the minimal V25-backed workforce implementation needed for this use case within the single planned MF2 commit 13:

- `WorkforceCredential` entity mapped to `workforce_credentials`, including organization/user ownership, type, issuer/reference, issue/expiry dates, status, verification attribution, timestamps and `row_version`.
- A workforce-owned repository with organization- and user-scoped lookups.
- A read-only `WorkforceCredentialAccess` contract in a named interface such as `workforce::credential`. It returns immutable credential summaries and never exposes a JPA entity or repository.
- The inspections module may depend on this named interface only. Workforce does not depend on inspections.

A credential is eligible for readiness evidence only when it is `ACTIVE`, belongs to the specified organization and subject, has verification attribution and a source-evidence reference, and has an explicit validity interval covering the inspection's planned start time. Because V25 permits nullable `issued_at`/`expires_at`, either null bound is treated as unknown and blocks readiness approval (fail-closed); the UI/return flow must request clarification or correction rather than infer an unbounded credential. The credential type remains free-form; a human reviewer attests applicability rather than the system pretending to know a universal licensing taxonomy.

### Assets owns Drone documents

Add the minimal V25-backed `DroneDocument` entity, repository and read-only named interface required to check and snapshot documents for the Drone assigned to this inspection, within the same MF2 commit 13. The public contract returns immutable summaries, not persistence types. Each selected document must belong to the assigned Drone and organization, have `ACTIVE` status, carry review attribution (`reviewed_by_user_id` and `reviewed_at`), and have non-null `valid_from` and `valid_until` covering the planned start time; either null date bound blocks approval. The selected reviewer/Inspector credential rows must belong to the expected user and organization, be `ACTIVE`, carry verification attribution (`verified_by_user_id`, `verified_at`) and a source-evidence reference, and have non-null issue/expiry bounds covering planned start; either null bound blocks approval. Eligibility is a record-state check, not independent validation against an issuer registry.

The schema does not mark credential or Drone-document types as mandatory, so the reviewer must attest the applicable set. The command requires `applicabilityComplete=true` and a nonblank `applicabilityBasisReference` naming the internal policy, inspection scope determination, or reviewed source used to decide which credential/document types apply. If a category has no selected records, it also requires a category-specific non-applicability reason and the same traceable basis reference. A free-form statement without a traceable reference is not accepted. The platform stores but does not externally verify this internal policy/reference or independently decide that the selected set is legally complete. Any selected but missing, unowned, unverified, inactive or out-of-window record is a hard blocker. Permit handling remains stricter: `PERMIT_MISSING`, an unissued permit, or `EXEMPTION_BASIS_MISSING` from `ComplianceGateService` cannot be waived by the attestation.

### Inspections owns the review use case

`InspectionReadinessService` is the only orchestrator for the decision and state changes. It owns an inspections-side command value for the internal service operation, later mapped to a request DTO in commit 14. It uses the existing user, inspection, preparation, pair, permit, Drone and compliance contracts, plus the two narrowly scoped read interfaces above.

The inspections service must not import workforce or assets JPA entities/repositories for these new capabilities. It receives only the already-approved assets interfaces and the new credential/document read interfaces.

Each reader must enforce ownership in its own query. The Workforce lookup matches credential ID, organization ID and subject user ID. The Drone-document lookup joins `drone_documents.drone_id` to `drones.id` and matches the assigned Drone and `drones.organization_id`; the document table has no organization column. The approval service separately verifies that the preparation's `inspection_id` matches the locked inspection and that the preparation's `inspector_user_id` equals the inspection's assigned `inspector_id`. A credential belonging to another Inspector or a document belonging to another Drone is never accepted as evidence.

## 3. Review command and attestations

An approval command contains:

- inspection ID and preparation ID;
- the reviewer's selected credential ID;
- zero or more credential IDs for the assigned Inspector that the reviewer determined applicable;
- zero or more Drone-document IDs that the reviewer determined applicable;
- `applicabilityComplete=true` and a nonblank `applicabilityBasisReference` identifying the internal policy/scope determination or reviewed source used to decide which credential and Drone-document classes apply;
- when the Inspector-credential or Drone-document ID list is empty, a nonblank category-specific non-applicability reason plus the traceable applicability basis reference. A reason without the reference is insufficient.
- a nonblank `humanVerificationBasis` when ComplianceGate reports `requiresHumanVerification=true`. Machine blockers such as missing permit, unissued permit or exemption without a legal basis remain non-overridable.

A returned decision contains a nonblank reason and requires an independently qualified reviewer plus a submitted preparation owned by the assigned Inspector. Its command carries the reviewer credential ID plus optional Inspector-credential/Drone-document IDs the reviewer actually examined or attempted to resolve. It does not require readiness-only records to be present or valid: return must remain available to request missing or invalid evidence. The service records exactly those supplied source IDs and snapshots the scoped records it can resolve. An empty selection is an honest empty observed set, not a claim that no records are applicable; return snapshots are not approval evidence. In the return snapshot, `observedSourceSetComplete` is always `false`: the supplied IDs are a reviewer-selected observation set, never an exhaustive registry/catalog. Missing IDs are listed as unresolved. The reviewer credential must be active, verified/evidence-referenced, correctly owned and have non-null issue/expiry dates covering `decided_at` for both approve and return; approval additionally requires it valid at `planned_start`.

The attestation is attributable to the named reviewer and stored in the review decision/review basis snapshot and source hash. It is a human declaration, not an electronic signature, legal conclusion, or authority verification.

## 4. Approval and return flows

Both operations run in one transaction and serialize review of an inspection by locking the inspection and target preparation. All preparation writes that can affect review eligibility (`prepareShotList`, `submit`, `startRevision`, and creation of a new version) must acquire the same inspection row lock before reading or mutating preparation state, using the consistent lock order `inspection -> preparation`. This shared lock protocol prevents a newer version or edited submission from racing the review. Keep optimistic `row_version` checks as a second guard for stale detached writes.

Common checks:

1. The actor exists, is active, has `ORG_ADMIN`, and belongs to the inspection's organization.
2. The reviewer is not the assigned Inspector; same-person review is refused even if the account also has `ORG_ADMIN`.
3. The inspection is `PREPARING`; the target preparation belongs to that inspection, is the highest version, and is `SUBMITTED`.
4. The selected reviewer credential is active, internally verified with source evidence, owned by the reviewer and organization, and valid at both `decided_at` and `planned_start` for approval. For return, it must be valid at `decided_at` only because a planned-time/readiness gate is not required. Applicable Inspector credentials and Drone documents supplied for approval receive equivalent owner/org/time/status validation at planned start.
5. The inspection has a non-null planned start and end. Its `asset_pair_assignment_id` resolves to an `asset_pair_assignments` row with the same organization, asset, assigned Inspector and Drone as the inspection; `status == ACTIVE`; `assignment_response == ACCEPTED`; `responded_at` is non-null and strictly before `planned_start`; and `valid_from <= planned_start <= valid_until` when `valid_until` is present. V25 pair status does not encode Inspector acceptance; that is the separate V27 response pair. A stale, suspended, superseded, unanswered, rejected, acceptance at/after planned start, expired-at-planned-start or mismatched pair blocks approval. The assigned Drone must be `ACTIVE` at review time.

Approval-only checks:

6. `ComplianceGateService` reports no machine-detectable permit blocker. Human-verification findings require the reviewer attestation and a recorded basis; they are never silently interpreted as clear.
7. The reviewer confirms the applicable document/qualification set is complete, or supplies the required basis for an empty set. Selected credentials and documents must all pass their source-module checks. A `requiresHumanVerification` finding requires a separate basis attestation; permit blockers remain non-overridable.
8. Build fixed-schema snapshots using only the existing V25 decision columns: `credential_snapshot` contains reviewer/Inspector credential summaries plus credential applicability attestation and basis; `credential_snapshot_ids` contains those sorted credential IDs. `drone_document_snapshot` contains the document applicability attestation/basis, selected document summaries and completeness-of-resolution findings; `drone_document_snapshot_ids` contains those sorted document IDs. `permit_snapshot` contains permit summaries, all ComplianceGate blockers/verification findings, human verification basis, and a `source_envelope` with immutable copies of inspection ID, organization, asset, schedule ID, due-cycle key, objective, `scope`, `component_scope`, `acceptance_criteria`, planned start/end, status, pair ID/status/response/validity/assignee/Drone, and the full submitted preparation fields/version/content; `permit_snapshot_ids` contains sorted permit IDs. This explicit envelope is required because a hash alone cannot reconstruct source values and underlying rows may later change. The reviewer ID and preparation version also use their dedicated columns. `source_hash` covers a canonical envelope of all three JSON snapshots/ID lists, reviewer ID, preparation ID/version and content, all listed inspection/pair/schedule/scope facts, attestations and selected credential/document IDs. Sort records by UUID, use stable field ordering, canonical UTF-8 JSON and SHA-256 lowercase hex; do not hash unordered/map iteration output.
9. Persist an `APPROVED` decision with those snapshots, IDs and hash; mark the preparation `READY`; transition the inspection `PREPARING -> READY_FOR_FLIGHT`. Any failure rolls back all three writes.

Return flow:

- Apply account/organization authorization, reviewer independence, active reviewer credential ownership/verification and current submitted preparation ownership/version checks. Do not require planned time, a clear permit gate, complete Inspector credentials, or present/valid Drone documents to return; these may be exactly why the preparation is being returned.
- Require a nonblank return reason.
- Read any supplied/linked source records in a tenant/subject/Drone-scoped way. Snapshot records that are available and list missing, invalid or unresolved source IDs and the gate findings in `permit_snapshot`/related snapshot JSON. The return hash represents observed state and is explicitly not approval evidence.
- Persist a `RETURNED` decision with the observed source snapshot/hash and reason; mark the preparation `RETURNED`; leave inspection at `PREPARING` so the Inspector can revise.
- Do not create a decision or change state when authorization, reviewer qualification/independence, submitted-preparation ownership/currentness, or the nonblank reason fails.

## 5. Preparation-state transition and concurrency

Update `InspectionPreparationService.prepareShotList` so starting preparation transitions an `ASSIGNED` inspection to `PREPARING`. Repeated edits while already `PREPARING` remain allowed. Other statuses are refused rather than silently reopened. This makes the state machine required by the SRS real and establishes the status prerequisite for review.

A returned preparation is revised through the existing `startRevision()` flow and resubmitted as the current version before review. Re-review cannot act on an earlier submitted version after a newer version exists.

All `InspectionPreparationService` methods that create/edit/submit/reopen a preparation acquire `InspectionRepository.findWithLockByIdAndOrganizationId` before touching preparation rows. Review acquires the same inspection lock first, then locks the preparation; every path uses that order. The latest-version read occurs only after acquiring the inspection lock. `@Version row_version` remains enabled on entities; if an optimistic-lock conflict occurs, fail the transaction with a conflict and do not retry approval automatically.

## 6. Failure behavior

- Inactive/missing account, non-ORG_ADMIN actor or no organization: `403 FORBIDDEN`.
- Inspection outside organization: `404 INSPECTION_NOT_FOUND`.
- Reviewer is assigned Inspector: `403 REVIEWER_NOT_INDEPENDENT`.
- Inspection not `PREPARING`, preparation not current or not `SUBMITTED`: `409` with a specific readiness/preparation code.
- Credential missing, not active, wrong owner/org, missing verification/evidence attribution, null issue/expiry bound, or outside validity: fail closed with a specific credential blocker.
- Pair, Drone, permit or selected Drone-document mismatch/invalidity, including null document validity bounds: fail closed with a specific blocker; no `APPROVED` decision or `READY_FOR_FLIGHT` state is written.
- Return without reason: the application service uses `RETURN_REASON_REQUIRED`; commit 14 defines the HTTP status mapping.
- Missing/invalid evidence blocks approval but does not block a qualified reviewer from returning a submitted preparation; the return snapshot records unresolved sources and findings.
- Database or snapshot/hash failure rolls the transaction back; never leave decision, preparation and inspection states inconsistent.
- Lock timeout or optimistic-lock conflict returns a conflict and writes no decision; never retry approval against a changed preparation automatically.

## 7. Testing

Before production code, write readiness-service tests to this contract and run them red. Tests must cover:

- successful approval with independently qualified ORG_ADMIN, reviewer and Inspector credentials carrying verification attribution and source-evidence references, valid applicable Drone documents carrying review attribution, a clear permit gate and completed attestations; assert persisted decision/snapshots/hash and both state transitions;
- reviewer who is the assigned Inspector, wrong role, inactive user, wrong organization, wrong credential owner/status, missing verification attribution/source evidence, null issue/expiry bounds, and credential outside the planned-start validity interval;
- preparation belonging to a different inspection, preparation Inspector differing from the inspection assignment, credential for another Inspector, and Drone document for another Drone/organization;
- no or stale pair, pair response missing/REJECTED/recorded at or after planned start, pair validity not covering planned start, pair assignee/Drone/asset mismatch, unserviceable/missing Drone, absent planned time, missing/invalid permit, and selected Drone document with missing review attribution, null validity bound or planned time outside its validity interval;
- snapshot preservation of objective, schedule/due-cycle, scope/component_scope, acceptance criteria and planned window; mutating any one source field changes the stored envelope/hash.
- missing applicability attestation and empty credential/document selection without the corresponding non-applicability basis; machine-checkable permit blockers remain non-overridable;
- non-current, unsubmitted, already-ready or returned preparation;
- successful return with reason and missing evidence, refused blank reason, and no change to inspection status;
- canonical persisted snapshot envelope reconstructs the reviewed inspection/pair and full preparation content plus reviewer, attestations, source summaries and IDs; reordering source lists does not change the hash;
- transaction rollback leaves no decision/readiness state when any gate fails;
- concurrent preparation edit/new-version attempt blocks behind the inspection lock; competing approval creates at most one decision; optimistic-lock/timeout conflict returns no partial transition.

Use real PostgreSQL/Testcontainers for module persistence/scope tests and retain the existing Modulith boundary test. Run `./mvnw.cmd clean verify` before completion.

## 8. Explicit scope boundaries and known limitations

- No HTTP controller/request-response contract, frontend or mobile changes in this design's implementation slice; these remain commit 14 and later.
- No change invalidation when plans, permits or documents change; commit 14 owns that behavior. The approval snapshot/hash provides the source basis needed for it.
- No government registry or external professional-certification verification. An ACTIVE row with internal verification/review attribution and an evidence reference is only an internally reviewed record; it is not proof that an issuing authority has confirmed it.
- Because schema lacks a mandatory-document policy, the human review attestation is explicit and attributable; the application never equates absence of a row with exemption. An empty selected credential/document list blocks approval unless its corresponding explicit non-applicability basis is recorded. The reviewer’s basis is an internal review reference, not an automated legal determination. Machine-checkable permit blockers remain non-overridable.
- No new migration: required source tables and readiness decision/preparation tables already exist in V25. Entity/repository/read-interface code must map those tables exactly.
- The backend repository must stay clean of partial readiness tests and production code until this spec is approved and the implementation plan is reviewed.
