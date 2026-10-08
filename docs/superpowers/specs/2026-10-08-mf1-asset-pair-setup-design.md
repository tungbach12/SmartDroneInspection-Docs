# MF1 Asset and Pair Setup Design

**Date:** 2026-10-08  
**Status:** Draft for review  
**Scope:** Backend vertical slice for Report 3 FE-02 / MF1-08–MF1-10  
**Out of scope:** MF1-01–07 workforce/Drone/compliance provisioning; MF1-11–14 inspection creation, assignment confirmation, and dispatch; MF2 readiness/field behavior; frontend/mobile UI; workflow completion claims.

## 1. Purpose and source of truth

Implement the MF1 requirement that an `ORG_ADMIN` creates an asset together with exactly one default Inspector/Drone pair, and the backend validates and stores both atomically. A failed pair validation must not leave a persisted asset without its required pair.

Current requirements are `project-reference/business-flows.md` v4.0, MF1-08–10, and Report 3 `03-functional-requirements.md` §3.3.1, MF1-08–10. The old schedule-proposal WF1 contract is retired and must not be restored. The Enterprise SaaS reset plan `.hermes/plans/2026-10-07_enterprise-saas-backend-and-full-db.md` excludes MF1–MF4 workflow execution from the reset itself; this spec is a separately approved feature slice after that reset.

## 2. Confirmed design

### 2.1 Behavior

- `ORG_ADMIN` submits the asset fields already supported by the current asset API, plus exactly one `inspectorId` and one `droneId`.
- The organization identifier is derived from the authenticated principal. A request-supplied organization identifier is never trusted.
- Before persistence, the use case validates that the Inspector is an active `INSPECTOR` in the same organization, the Drone exists in the same organization and has serviceability `ACTIVE`, and the asset category is permitted for the organization under the current catalog rules.
- The asset and an `ACTIVE` `asset_pair_assignments` row are saved in one transaction. The assignment has the same organization and asset IDs, the selected Inspector/Drone IDs, `valid_from`, and the assigning ORG_ADMIN attribution.
- A failure at any validation or persistence step leaves neither a partially created asset nor a pair assignment.
- The pair is the asset's current default operational assignment. It does not reserve the Drone exclusively and does not represent a flight permit or readiness decision.
- Asset update does not silently rewrite an existing pair. Reassignment/history behavior is a separate slice unless a required current acceptance criterion proves it is necessary here.

### 2.2 Authorization and errors

- Only `ORG_ADMIN` may create the asset and pair.
- Cross-organization Inspector/Drone IDs are denied without exposing foreign records. Use the repository's established non-disclosure response (`404 NOT_FOUND`) for foreign tenant resources; malformed, missing, disabled, wrong-role, or unavailable same-tenant selections return a validation/conflict ProblemDetail according to existing API conventions.
- Duplicate asset code in the organization remains `409 DUPLICATE_CODE`.
- No endpoint or query grants `ADMIN` implicit cross-tenant asset access as a side effect of this feature. Platform global support access remains a separately ruled authorization contract.

### 2.3 Persistence boundary

- `assets` owns `Asset`, `Drone`, and `AssetPairAssignment` because the approved ownership decision assigns Drone inventory and asset pair records to `assets`; `workforce` owns people qualifications/credentials.
- Cross-module user data is obtained through a narrow `users` module boundary such as the existing `UserAccess` facade, extended only if needed to validate that a selected user is an active INSPECTOR in the caller's organization.
- The Drone must be read using an organization-scoped repository query.
- Persist `AssetPairAssignment` in the same `@Transactional` use case as `Asset`; keep controller thin.
- V25 already creates `drones` and `asset_pair_assignments`, and V26 adds composite tenant FKs plus one-active-pair-per-asset uniqueness. No migration is expected unless verified live mapping gaps prove the existing target schema insufficient. Never rewrite V1–V26.

## 3. Current implementation boundary and dependency

At backend `main` (`36b2e3b`), `assets` already has `Asset`, `AssetService`, `AssetController`, categories, and documents. `UserAccess.ActiveUser` exposes roles and organization scope. The physical target tables `drones` and `asset_pair_assignments` exist in V25/V26.

No Drone JPA entity/repository/API was found in `src/main/java`; `workforce` has only `package-info.java`; and there is no pair-assignment runtime. Therefore this slice may add only the smallest Drone inventory persistence/API surface required to select an existing same-organization active Drone, or it must depend on an already-delivered equivalent if the implementation plan confirms one. It must not invent subscription, credential-vetting, flight-permit, or readiness workflows. New Drone records are not part of asset creation.

## 4. Acceptance criteria

1. A valid same-organization ORG_ADMIN request creates exactly one asset and exactly one active pair assignment in one transaction.
2. The returned asset response identifies the selected Inspector and Drone pair (or exposes an explicitly typed pair reference agreed in the implementation plan); it does not claim inspection dispatch/readiness.
3. A duplicate asset code returns 409 and writes neither asset nor pair.
4. A missing/inactive/wrong-role/foreign-organization Inspector is rejected; no asset or pair remains.
5. A missing/inactive/foreign-organization Drone is rejected; no asset or pair remains.
6. Any pair insert/FK/uniqueness failure rolls back the asset insert.
7. Cross-organization list/detail/update behavior remains scoped and all existing asset-document authorization remains unchanged.
8. Organization and identity are derived/scoped from the authenticated user, never from a client-supplied tenant ID.
9. Tests use a real PostgreSQL/Testcontainers database for transaction, FK and uniqueness behavior; no mock-only proof of atomicity.
10. Report 5 records the implemented acceptance cases only after execution; no historical test ID is renamed or overwritten.

## 5. Explicitly unresolved product boundary

- This slice creates the asset and default pair only. It does not create an inspection, schedule, or due-cycle event. The current contract permits cadence where needed, but schedule-driven inspection generation is a separate workflow decision and is not inferred from the retired proposal flow.


The requirements and review rules differ on platform-wide `ADMIN` asset visibility: the role says global support access, while the asset service currently scopes non-ORG_ADMIN callers through organization and no safe cross-tenant support policy is defined. This feature will not add global `ADMIN` asset access. If administrators must inspect assets, define an audited, read-only, reason-bearing support-access rule in a separate authorization decision.

## 6. Verification and documentation

- Focused backend integration tests: valid atomic create; duplicate code; inactive/wrong-role/cross-org Inspector; missing/inactive/cross-org Drone; forced pair persistence failure rollback; asset list/detail organization scope.
- Run `./mvnw -Dtest='...asset pair and asset API test classes...' test`, then `./mvnw verify`.
- Update Report 3 §3.3.1 and its record of changes, business flow MF1-08–10 if semantics change, database design implementation status only if persistence changes, backend API/architecture docs, and Report 5 case index/details/statistics/cover using new stable cases.
- Final handoff lists exact commands and `Documentation impact`.

## 7. Risks

- The schema exists but runtime Drone inventory is absent; adding a minimal entity/repository/API adds cross-repository interface surface and must be planned as part of the same backend vertical slice.
- Same-organization FK guarantees currently exist for `asset_pair_assignments` after V26, but role and active-status checks remain application responsibilities.
- The atomic requirement is only satisfied if the use-case transaction covers both inserts and all failures propagate to rollback.
