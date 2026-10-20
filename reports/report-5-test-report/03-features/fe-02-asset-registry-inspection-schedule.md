# FE-02: Asset, Drone, Workforce and Compliance Catalog — MF1

Report 3 §3.3 titles this feature "Asset, Drone, Workforce and Compliance
Catalog". The filename retains the earlier "asset registry / inspection
schedule" wording; the filename is stable, the scope is Report 3's.

## Scope baseline

MF1 retains the agreed asset-creation assignment: **ORG_ADMIN creates an asset
together with one responsible Inspector and one specific Drone**, then creates
inspections that inherit that pair. Re-inspecting an existing asset does not
recreate the asset. This is MF1, the source of the MF2 assignment FE-03
consumes.

The fourteen MF1 steps divide as:

| Steps | Actor | What it does |
| --- | --- | --- |
| MF1-01 – MF1-05 | `ORG_ADMIN` + `SYSTEM` | Organization identity and authorized reviewers; subscription entitlement check; Inspector/Engineer provisioning; skills and credential records; document validation with expiry warnings. |
| MF1-06 – MF1-07 | `ORG_ADMIN` | Drone registration by unique identifier, serviceability and documents; flight permits and compliance files with issuer, scope and conditions. |
| MF1-08 – MF1-10 | `ORG_ADMIN` + `SYSTEM` | Asset profile, and in the **same workflow** selection of exactly one Inspector and one Drone; validation and audit that saves asset and pair together. |
| MF1-11 – MF1-14 | `ORG_ADMIN` + `SYSTEM` | Create the inspection for that asset; inherit the current pair into a snapshot; confirm with a recorded reassignment reason; dispatch with document references. |

Gates worth stating because they are easy to misread as satisfied:

- **No partially created complete asset with a missing pair** (MF1-10). Asset
  assignment is not a flight permit, nor an exclusive reservation of the Drone.
- An updated asset default **never rewrites past inspection snapshots**
  (MF1-12).
- Unresolved conflicts, disabled users or unavailable Drones **block dispatch**
  (MF1-13).
- Cadence changes affect **future due work only**, not published history.
- An informational airspace warning **does not authorize flight** (MF1-08).
- Machine validation of a document **is not government verification** (MF1-05).

The four canonical roles are `ADMIN`, `ORG_ADMIN`, `INSPECTOR` and
`MAINTENANCE_ENGINEER`.

## Current test coverage

No workbook test case is mapped to FE-02 in this report. MF1-06 Drone and
MF1-07 permit backend behavior is implemented and has backend plus Frontend
supporting evidence recorded below, outside the fixed WFx workbook rows. MF1-01,
MF1-08–MF1-14 remain unimplemented/unverified in this Frontend slice; the
Frontend UI does not establish the asset-plus-Inspector/Drone assignment and
dispatch workflow.

The former `WF1-001`–`WF1-019` cases were removed on 2026-10-09 because they
described the retired five-role WF1 baseline (Service Manager review, Client
asset registration, schedule proposals). That is not the current system, so
their recorded results are not evidence for it.

The backend does implement a catalog with organization scoping and a paged
list, and the WF3 inspection collection depends on it. That is catalog CRUD,
not the MF1 resource-creation workflow, and **no executed test case is recorded
here for it**, so it is not reported as tested. This is an explicit, truthful
coverage gap: FE-02 verification is outstanding and must be executed and
recorded before the feature can be reported as verified.

### Steps that would be covered first

| Step | Gate to verify |
| --- | --- |
| MF1-09 – MF1-10 | An asset cannot be saved complete without exactly one Inspector and one Drone. |
| MF1-12 | An inspection snapshots the pair; later asset default changes do not rewrite it. |
| MF1-13 | A reassignment requires a recorded reason and is versioned. |
| MF1-02 | A lapsed subscription denies the operation without deleting existing history. |

The removed `WF1-*` case IDs stay reserved and are never reused.

### Frontend MF1-06 Drone inventory and documents — supporting verification (executed 2026-10-13)

- Preconditions: Frontend `feat/mf1-org-admin-resources` based on current `origin/main`; Vitest/jsdom; synthetic API responses conforming to Backend Drone DTOs.
- Procedure: Run `npx vitest run --pool=forks --maxWorkers=1 src/features/assets/api/assetsApi.test.ts src/features/assets/hooks/useDrones.test.tsx src/features/assets/pages/DroneInventoryPanel.test.tsx`. Verify Drone list/create/detail/selection/serviceability and document list/upload/status URLs; JSON-string `payloadMetadata`; multipart fields without client checksum; ORG_ADMIN create/serviceability/upload controls; loading/empty/retry, server 413/415 feedback, expired status, no flight-clearance wording; lazy detail queries; selected file not held in TanStack mutation variables and cleared after upload/close.
- Expected result: The client follows the existing API contract, sends no organization field or checksum, tenant scope stays server-owned, detail queries run only while open, and serviceability is never described as flight permission/readiness.
- Round 1: Passed 2026-10-13; tester: Claude Code (automated).
- Evidence: focused command passed 3 files / 31 tests before final integration. Full suite on the clean release branch after `origin/main` merge: `npm test -- --maxWorkers=1` passed 51 files / 336 tests.
- Scope note: This is mocked-transport component/contract verification; no live MinIO, authenticated browser/backend round-trip or manual browser check is claimed.

### Frontend MF1-07 permit records and internal review — supporting verification (executed 2026-10-13)

- Preconditions: Same Frontend release branch; synthetic fixtures matching `CreateFlightPermitRequest`, `ReviewFlightPermitRequest` and `FlightPermitResponse`.
- Procedure: Run `npx vitest run --pool=forks --maxWorkers=1 src/features/assets/api/assetsApi.test.ts src/features/assets/hooks/useFlightPermits.test.tsx src/features/assets/pages/FlightPermitPanel.test.tsx src/features/assets/pages/AssetsPage.resources.test.tsx`. Verify list/create/review endpoints, no tenant field, JSON-string scope/conditions, optional raw asset/evidence IDs, six supported statuses, date-order and malformed JSON validation, required internal review reason, form reset after cancel, non-verification copy, ORG_ADMIN-only tabs/actions and list loading/empty/retry.
- Expected result: The UI mirrors backend DTOs; permit status is labeled organization-recorded; no authority/registry verification, legal clearance, or permission-to-fly claim is implied; there are no invented asset/evidence pickers; canceled drafts do not persist.
- Round 1: Passed 2026-10-13; tester: Claude Code (automated).
- Evidence: focused command passed 4 files / 33 tests; create-cancel reset regression passed in `FlightPermitPanel.test.tsx` (7/7). Final clean-branch regression passed 51 files / 336 tests.
- Review note: Independent React review confirmed DTO alignment and caught stale form state after cancel/success; the dialog now remounts on each open cycle and has a regression test.
- Scope note: Mocked transport only; no live backend, authority/registry lookup, or manual browser verification claimed.

### Integrated Frontend role/access and verification — supporting evidence (executed 2026-10-13)

- Preconditions: Frontend `feat/mf1-org-admin-resources`, current upstream main merged, canonical roles `ADMIN`, `ORG_ADMIN`, `INSPECTOR`, `MAINTENANCE_ENGINEER`.
- Procedure: `npm test -- --maxWorkers=1`; `npm run build`; `npm run lint`; focused direct guards via `npx vitest run --pool=forks --maxWorkers=1 src/app/permissions/accessPolicy.test.ts src/app/router/router.test.ts src/features/auth/components/RequireAuth.resources.test.tsx src/features/assets/pages/AssetsPage.resources.test.tsx`; `git diff --check`.
- Expected result: All automated tests pass; route guards permit ORG_ADMIN and direct guard tests redirect the other three roles to Forbidden; strict build passes; lint exits zero; whitespace check is clean.
- Round 1: Passed 2026-10-13; tester: Claude Code (automated).
- Evidence: full suite 51 files / 336 tests; focused guard suite 9 files / 95 tests; `npm run build` passed; `npm run lint` exited 0 with six existing `react(only-export-components)` Fast Refresh warnings (in `Toast.tsx`, `main.tsx`, `ReportSectionForm.tsx`, and `router.tsx`); `git diff --check` passed. Manual browser verification was not run because the connected browser was `about:blank`.
- Scope note: Role guards are navigation protection; backend authorization remains authoritative. No changes were made to backend APIs/schema in this Frontend task.

### MF1-08 – MF1-10 Asset Creation and Default Pair Assignment — supporting verification (executed 2026-10-20)

- Preconditions: Backend `feat/mf1-backend-org-admin-resources` and Frontend `feat/mf1-org-admin-resources-hieu`; PostgreSQL 17/Testcontainers; active ORG_ADMIN, Inspector and Drone within the same organization.
- Procedure: Run Backend `AssetApiIntegrationTest` and Frontend `AssetsPage.pairing.test.tsx`. Verify asset creation with default Inspector and Drone pair; tenant-scoped validation rejecting foreign inspectors, foreign drones, or retired drones; pair persistence in `asset_pair_assignments` with `ACTIVE` status; active pair retrieval and reassignment with recorded reason; drawer pairing display and "New inspection" row trigger.
- Expected result: Assets save atomically with their active default operational pair; cross-tenant references fail with 400 `INVALID_INSPECTOR` or `INVALID_DRONE`; reassignment supersedes the previous pair and creates a new active version; UI displays the assigned pair with inspector and drone details.
- Round 1: Passed 2026-10-20; tester: Claude Code (automated).
- Evidence: Backend `AssetApiIntegrationTest` passed 11/11 tests; Frontend `AssetsPage.pairing.test.tsx` passed 3/3 tests.

### MF1-11 – MF1-14 Inspection Creation and Pair Inheritance/Reassignment — supporting verification (executed 2026-10-20)

- Preconditions: Backend `feat/mf1-backend-org-admin-resources` and Frontend `feat/mf1-org-admin-resources-hieu`; PostgreSQL 17/Testcontainers; active asset with assigned default pair.
- Procedure: Run Backend `InspectionCreationApiIntegrationTest` and Frontend `CreateInspectionDialog.test.tsx`. Verify inspection creation inheriting asset default pair snapshot; date ordering and non-empty objective validation; optional override of inspector or drone with mandatory reassignment reason; dispatch to `ASSIGNED` status; rejection of inspections on unpaired or foreign assets; ORG_ADMIN only creation authorization.
- Expected result: Inspections inherit the active operational pair snapshot without mutating asset defaults; planned dates and objective are enforced; unauthorized roles receive 403; dispatched inspections are ready for MF2 inspector assignment response.
- Round 1: Passed 2026-10-20; tester: Claude Code (automated).
- Evidence: Backend `InspectionCreationApiIntegrationTest` passed 6/6 tests; full backend verify passed 640 tests, JaCoCo and Modulith checks; Frontend `CreateInspectionDialog.test.tsx` passed 3/3 tests; full frontend suite passed 53 files / 342 tests and build succeeded.

## Feature sheet summary

Values for the `Feature 2` summary block (`A2:E8` in the workbook).
The template reads these back by formula, so an export needs them
recorded here.

| Cell | Label | Value |
| --- | --- | --- |
| `B2` | Feature | Asset, Drone, Workforce and Compliance Catalog — MF1 |
| `B3` | Test requirement | Would verify asset registration with its assigned Inspector and Drone pair, compliance documents and due-cycle inspection generation. MF1 is unimplemented, so no case is recorded. |
