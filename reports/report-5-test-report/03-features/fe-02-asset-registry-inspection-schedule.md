# FE-02: Asset Registry and Inspection Schedule

## Scope baseline

An organization registers and maintains its assets, asset documents and
recurring inspection schedules; categories and checklist templates are
maintained centrally. The current roles are `ADMIN`, `ORG_ADMIN`, `INSPECTOR`
and `MAINTENANCE_ENGINEER`.

## Current test coverage

No workbook test case is mapped to FE-02 in this report.

The former `WF1-001`–`WF1-019` cases were removed on 2026-10-09 because they
described the retired five-role WF1 baseline (Service Manager review, Client
asset registration, schedule proposals). That is not the current system, so
their recorded results are not evidence for it.

The current backend does implement an asset catalog with organization scoping
and a paged list, but **no executed test case is recorded here for it**, so it
is not reported as tested. This is an explicit, truthful coverage gap: FE-02
verification is outstanding and must be executed and recorded before the
feature can be reported as verified.

The removed `WF1-*` case IDs stay reserved and are never reused.

## MF1-06 organization Drone inventory and Drone documents (executed 10 October 2026)

This is supporting evidence for the MF1 resource-setup slice, recorded here
outside the fixed WFx workbook rows so the workbook totals are unchanged.

### Drone inventory

- Preconditions: Backend branch `integrate/mf1-resources` at `dcd6516`; PostgreSQL 17 through Testcontainers; `V25` tables `drones` and `drone_documents`; an active ORG_ADMIN plus a second organization for isolation checks.
- Procedure: Run `./mvnw -Dtest=DroneApiIntegrationTest,DronePersistenceTest test`; create, list, fetch and change serviceability for a same-organization Drone; submit a duplicate serial number; request a foreign-organization Drone; query the selection endpoint; and attempt an out-of-set `serviceability` value.
- Expected result: Create returns 201 and organization scope comes from the authenticated actor, never the request; a duplicate serial returns 409; a foreign-organization Drone returns 404 with a problem body identical to a missing Drone's, so existence elsewhere is not disclosed; the selection endpoint returns only same-organization `ACTIVE` drones and asserts no permit, clearance or readiness claim; an unknown enum value returns 400, not 500.
- Round 3: Passed on 2026-10-10; tester: Claude Code (automated).
- Evidence: `DroneApiIntegrationTest` 12/12 and `DronePersistenceTest` 10/10, inside the merged `./mvnw verify` run: 254 tests, 0 failures, 0 errors, `All coverage checks have been met.`, BUILD SUCCESS.
- Entitlement note: writes require an active subscription; reads stay available without one, following the MF1-02 precedent.

### Drone documents

- Preconditions: Same merged baseline; an `EvidenceObjectStore` is available for the upload path.
- Procedure: Run `./mvnw -Dtest=DroneDocumentApiIntegrationTest test`; upload a document to a same-organization Drone with a forged client-supplied checksum; upload a duplicate object key; attempt a cross-organization Drone; move a document to `REVOKED` and attempt to change its status afterwards; and read a document whose `valid_until` has passed.
- Expected result: The stored `checksum_sha256` is the server-derived digest of the uploaded bytes, never the client-asserted value; a duplicate object key is rejected; cross-organization access is refused; a revoked document cannot change status; and reads report `EXPIRED` derived from the validity window.
- Round 3: Passed on 2026-10-10; tester: Claude Code (automated).
- Evidence: `DroneDocumentApiIntegrationTest` 7/7, inside the 254-test merged run above.
- Design note: V25 declares `drone_documents.checksum_sha256` `NOT NULL` but the shared `EvidenceObjectStore.put` port takes no checksum argument. The checksum is therefore computed server-side over the buffered bytes and the existing port was left unchanged, so no second storage adapter was introduced and no constraint was relaxed.
- Defect note: An unknown enum value in any request body returned 500 rather than 400 across the whole application. A `GlobalExceptionHandler` mapping for `HttpMessageNotReadableException` was added, turning it into a 400 `VALIDATION_FAILED` problem. This was a pre-existing platform-wide gap, not a Drone-specific one.
- Scope note: Document upload is exercised against a mocked `EvidenceObjectStore`, matching the existing `AssetDocumentApiIntegrationTest`. No live MinIO round-trip is claimed.

### Still unverified for FE-02

MF1-07 permit and compliance records, MF1-08–10 asset creation with the required
Inspector/Drone pair, and inspection scheduling are not implemented in this slice
and have no executed case.
