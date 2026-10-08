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

A credential is eligible for readiness evidence only when it is `ACTIVE`, belongs to the specified organization and subject, and is valid at the inspection's planned start time (not issued after that time and not expired before it). The type remains a free-form source value; a human reviewer attests applicability rather than the system pretending to know a universal licensing taxonomy.

### Assets owns Drone documents

Add the minimal V25-backed `DroneDocument` entity, repository and read-only named interface required to check and snapshot documents for the Drone assigned to this inspection, within the same MF2 commit 13. The public contract returns immutable summaries, not persistence types. Each selected document must belong to the assigned Drone and organization, have `ACTIVE` status, carry review attribution (`reviewed_by_user_id` and `reviewed_at`), and cover the planned start time. The selected reviewer/Inspector credential rows must belong to the expected user and organization, be `ACTIVE`, carry verification attribution (`verified_by_user_id`, `verified_at`) and a source-evidence reference, and cover the planned start time. Eligibility is a record-state check, not independent validation against an issuer registry.

The schema does not mark document types as mandatory. The reviewer therefore supplies the applicability attestation described below. The system validates every selected document and fails closed on invalid selected records; it does not infer that a document is optional merely because no row exists.

### Inspections owns the review use case

`InspectionReadinessService` is the only orchestrator for the decision and state changes. It owns an inspections-side command value for the internal service operation, later mapped to a request DTO in commit 14. It uses the existing user, inspection, preparation, pair, permit, Drone and compliance contracts, plus the two narrowly scoped read interfaces above.

The inspections service must not import workforce or assets JPA entities/repositories for these new capabilities. It receives only the already-approved assets interfaces and the new credential/document read interfaces.

## 3. Review command and attestations

An approval command contains:

- inspection ID and preparation ID;
- the reviewer's selected credential ID;
- zero or more credential IDs for the assigned Inspector that the reviewer determined applicable;
- zero or more Drone-document IDs that the reviewer determined applicable;
- an explicit confirmation that applicable qualifications, permits and Drone-document requirements were reviewed and are complete;
- an explanation when the reviewer determines no Inspector credential or no Drone document is applicable.

A returned decision contains a nonblank reason. It still requires an independently qualified reviewer and snapshots the records available at review time, but does not require clearance of every readiness blocker because its purpose is to request remediation.

The attestation is attributable to the named reviewer and stored in the review decision/review basis snapshot and source hash. It is a human declaration, not an electronic signature, legal conclusion, or authority verification.

## 4. Approval and return flows

Both operations run in one transaction and serialize review of an inspection by locking the inspection and target preparation.

Common checks:

1. The actor exists, is active, has `ORG_ADMIN`, and belongs to the inspection's organization.
2. The reviewer is not the assigned Inspector; same-person review is refused even if the account also has `ORG_ADMIN`.
3. The inspection is `PREPARING`; the target preparation belongs to that inspection, is the highest version, and is `SUBMITTED`.
4. The selected reviewer credential is active, verified according to the workforce source record, owned by the reviewer and organization, and valid at planned start. Applicable Inspector credentials and Drone documents supplied by the reviewer receive equivalent owner/org/time/status validation.
5. A current active accepted pair exists and matches the inspection's Inspector and Drone. The assigned Drone is serviceable at review time. Missing planned time, missing pair, a stale/expired pair, or missing/unserviceable Drone blocks approval.

Approval-only checks:

6. `ComplianceGateService` reports no machine-detectable permit blocker. Human-verification findings require the reviewer attestation and a recorded basis; they are never silently interpreted as clear.
7. The reviewer confirms the applicable document/qualification set is complete, or supplies a reason for any declared non-applicability. Selected credentials and documents must all pass their source-module checks.
8. Build deterministic snapshots for the inspection/pair, submitted preparation version, permits, reviewer and Inspector credentials, and Drone documents. Hash the canonical snapshot representation (SHA-256, lowercase hex); do not hash unordered/map iteration output.
9. Persist an `APPROVED` decision with snapshots, IDs and hash; mark the preparation `READY`; transition the inspection `PREPARING -> READY_FOR_FLIGHT`. Any failure rolls back all three writes.

Return flow:

- Apply common identity, reviewer-independence, qualification, current-preparation and source-record checks.
- Require a nonblank return reason.
- Persist a `RETURNED` decision with the observed source snapshot/hash and reason; mark the preparation `RETURNED`; leave inspection at `PREPARING` so the Inspector can revise.
- Do not create a decision or change state when validation fails.

## 5. Preparation-state transition

Update `InspectionPreparationService.prepareShotList` so starting preparation transitions an `ASSIGNED` inspection to `PREPARING`. Repeated edits while already `PREPARING` remain allowed. Other statuses are refused rather than silently reopened. This makes the state machine required by the SRS real and establishes the status prerequisite for review.

A returned preparation is revised through the existing `startRevision()` flow and resubmitted as the current version before review. Re-review cannot act on an earlier submitted version after a newer version exists.

## 6. Failure behavior

- Inactive/missing account, non-ORG_ADMIN actor or no organization: `403 FORBIDDEN`.
- Inspection outside organization: `404 INSPECTION_NOT_FOUND`.
- Reviewer is assigned Inspector: `403 REVIEWER_NOT_INDEPENDENT`.
- Inspection not `PREPARING`, preparation not current or not `SUBMITTED`: `409` with a specific readiness/preparation code.
- Credential missing, not active, wrong owner/org or outside validity: fail closed with a specific credential blocker.
- Pair, Drone, permit or selected Drone-document mismatch/invalidity: fail closed with a specific blocker; no `APPROVED` decision or `READY_FOR_FLIGHT` state is written.
- Return without reason: `400`/`409` with `RETURN_REASON_REQUIRED` according to the established API error contract when commit 14 defines the HTTP mapping; the application service uses a stable business error code.
- Database or snapshot/hash failure rolls the transaction back; never leave decision, preparation and inspection states inconsistent.

## 7. Testing

Before production code, write readiness-service tests to this contract and run them red. Tests must cover:

- successful approval with independently qualified ORG_ADMIN, reviewer and Inspector credentials carrying verification attribution and source-evidence references, valid applicable Drone documents carrying review attribution, a clear permit gate and completed attestations; assert persisted decision/snapshots/hash and both state transitions;
- reviewer who is the assigned Inspector, wrong role, inactive user, wrong organization, wrong credential owner/status/expiry, missing verification attribution/source evidence, and credential that is not valid at planned start;
- no or stale pair, unserviceable/missing Drone, absent planned time, missing/invalid permit, and selected Drone document with missing review attribution or invalid validity window;
- incomplete applicability attestation and no-applicable-document declarations without a basis;
- non-current, unsubmitted, already-ready or returned preparation;
- successful return with reason, refused blank reason, and no change to inspection status;
- transaction rollback leaves no decision/readiness state when any gate fails;
- race-safe locking for competing reviewers where supported by the integration-test framework.

Use real PostgreSQL/Testcontainers for module persistence/scope tests and retain the existing Modulith boundary test. Run `./mvnw.cmd clean verify` before completion.

## 8. Explicit scope boundaries and known limitations

- No HTTP controller/request-response contract, frontend or mobile changes in this design's implementation slice; these remain commit 14 and later.
- No change invalidation when plans, permits or documents change; commit 14 owns that behavior. The approval snapshot/hash provides the source basis needed for it.
- No government registry or external professional-certification verification. An ACTIVE row with internal verification/review attribution and an evidence reference is only an internally reviewed record; it is not proof that an issuing authority has confirmed it.
- Because schema lacks a mandatory-document policy, the human review attestation is explicit and attributable; the application never equates absence of a row with exemption. A document/credential not selected and attested as applicable cannot be silently treated as evidence that all conditions are satisfied.
- No new migration: required source tables and readiness decision/preparation tables already exist in V25. Entity/repository/read-interface code must map those tables exactly.
- The backend repository must stay clean of partial readiness tests and production code until this spec is approved and the implementation plan is reviewed.
