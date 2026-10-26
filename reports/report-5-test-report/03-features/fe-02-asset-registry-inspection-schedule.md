# FE-02: Asset, Drone, Workforce and Compliance Catalog — MF1

Report 3 §3.3 titles this feature "Asset, Drone, Workforce and Compliance
Catalog". The filename retains the earlier "asset registry / inspection
schedule" wording; the filename is stable, the scope is Report 3's.

## Scope baseline

MF1 retains the agreed asset-creation assignment: **ORG_MANAGER creates an asset
together with one responsible Inspector and one specific Drone**, then creates
inspections that inherit that pair. Re-inspecting an existing asset does not
recreate the asset. This is MF1, the source of the MF2 assignment FE-03
consumes.

The fourteen MF1 steps divide as:

| Steps | Actor | What it does |
| --- | --- | --- |
| MF1-01 – MF1-05 | `ORG_MANAGER` + `SYSTEM` | Organization identity and authorized reviewers; subscription entitlement check; Inspector/Engineer provisioning; skills and credential records; document validation with expiry warnings. |
| MF1-06 – MF1-07 | `ORG_MANAGER` + `PLATFORM_MANAGER` | Owned Drone registration by unique identifier, serviceability and documents, plus B2B Drone Leasing (`PLATFORM_MANAGER` pool management, `ORG_MANAGER` lease request/payment, automatic `LEASED` customer fleet provisioning with `lease_expires_at`, and manual reclaim); flight permits and compliance files with issuer, scope and conditions. |
| MF1-08 – MF1-10 | `ORG_MANAGER` + `SYSTEM` | Asset profile, and in the **same workflow** selection of exactly one Inspector and one Drone; validation and audit that saves asset and pair together. |
| MF1-11 – MF1-14 | `ORG_MANAGER` + `SYSTEM` | Create the inspection for that asset; inherit the current pair into a snapshot; confirm with a recorded reassignment reason; dispatch with document references. |

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

The five canonical roles are `ADMIN`, `PLATFORM_MANAGER`, `ORG_MANAGER`, `INSPECTOR` and
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

The backend implements catalog CRUD and now has a local asset-pair default API
for DRAFT creation, history, explicit activation and supersession. Those changes
have not passed their Testcontainers API procedures because Docker is unavailable;
they are recorded as Pending below rather than reported as tested. This is not the
full MF1 resource-creation workflow: atomic asset-plus-pair creation, inspection
creation/snapshot/dispatch and client flow remain outstanding. FE-02 verification
therefore remains a coverage gap.

### Backend pair-default API — supporting verification (integration Pending)

- Preconditions: Backend branch `feat/quoc-mf1-mf4-e2e`; PostgreSQL and MinIO Testcontainers available; active subscription; own-organization active asset, active Inspector, and serviceable Drone; second organization and second same-organization Inspector for scope/supersession checks.
- Procedure: Run `./mvnw.cmd '-Dtest=AssetPairAdminApiIntegrationTest' test`. Verify ORG_MANAGER can create a `DRAFT` default pair and list only own-asset history; wrong role is denied; foreign asset/Drone and foreign/suspended Inspector are rejected; unavailable Drone, invalid window, blank reason and future-effective activation are refused; an unentitled organization cannot create pairs; explicit activation requires a reason and supersedes the previous active default with audit while preserving its prior Inspector response.
- Expected result: Pair history remains tenant scoped, draft creation does not expose an active default, exactly one active default exists per asset, and supersession never erases historical response fields.
- Round 1: Pending 2026-10-21; tester: Claude Code (automated test authored, execution blocked).
- Evidence: `./mvnw.cmd '-Dtest=AssetPairAdminApiIntegrationTest' test` failed before Spring context initialization because Testcontainers could not find a Docker environment. Test compilation passed with `./mvnw.cmd '-DskipTests' test-compile`; separate domain tests passed, but do not substitute for this API integration procedure.
- Scope note: No UI, inspection creation/dispatch, or end-to-end client journey is verified by this API test. No WFx workbook row or stable case ID is fabricated; the FE-02 coverage gap remains.

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
- Procedure: Run `npx vitest run --pool=forks --maxWorkers=1 src/features/assets/api/assetsApi.test.ts src/features/assets/hooks/useDrones.test.tsx src/features/assets/pages/DroneInventoryPanel.test.tsx`. Verify Drone list/create/detail/selection/serviceability and document list/upload/status URLs; JSON-string `payloadMetadata`; multipart fields without client checksum; ORG_MANAGER create/serviceability/upload controls; loading/empty/retry, server 413/415 feedback, expired status, no flight-clearance wording; lazy detail queries; selected file not held in TanStack mutation variables and cleared after upload/close.
- Expected result: The client follows the existing API contract, sends no organization field or checksum, tenant scope stays server-owned, detail queries run only while open, and serviceability is never described as flight permission/readiness.
- Round 1: Passed 2026-10-13; tester: Claude Code (automated).
- Evidence: focused command passed 3 files / 31 tests before final integration. Full suite on the clean release branch after `origin/main` merge: `npm test -- --maxWorkers=1` passed 51 files / 336 tests.
- Scope note: This is mocked-transport component/contract verification; no live MinIO, authenticated browser/backend round-trip or manual browser check is claimed.

### Frontend MF1-07 permit records and internal review — supporting verification (executed 2026-10-13)

- Preconditions: Same Frontend release branch; synthetic fixtures matching `CreateFlightPermitRequest`, `ReviewFlightPermitRequest` and `FlightPermitResponse`.
- Procedure: Run `npx vitest run --pool=forks --maxWorkers=1 src/features/assets/api/assetsApi.test.ts src/features/assets/hooks/useFlightPermits.test.tsx src/features/assets/pages/FlightPermitPanel.test.tsx src/features/assets/pages/AssetsPage.resources.test.tsx`. Verify list/create/review endpoints, no tenant field, JSON-string scope/conditions, optional raw asset/evidence IDs, six supported statuses, date-order and malformed JSON validation, required internal review reason, form reset after cancel, non-verification copy, ORG_MANAGER-only tabs/actions and list loading/empty/retry.
- Expected result: The UI mirrors backend DTOs; permit status is labeled organization-recorded; no authority/registry verification, legal clearance, or permission-to-fly claim is implied; there are no invented asset/evidence pickers; canceled drafts do not persist.
- Round 1: Passed 2026-10-13; tester: Claude Code (automated).
- Evidence: focused command passed 4 files / 33 tests; create-cancel reset regression passed in `FlightPermitPanel.test.tsx` (7/7). Final clean-branch regression passed 51 files / 336 tests.
- Review note: Independent React review confirmed DTO alignment and caught stale form state after cancel/success; the dialog now remounts on each open cycle and has a regression test.
- Scope note: Mocked transport only; no live backend, authority/registry lookup, or manual browser verification claimed.

### Integrated Frontend role/access and verification — supporting evidence (executed 2026-10-13)

- Preconditions: Frontend `feat/mf1-org-admin-resources`, current upstream main merged, canonical roles `ADMIN`, `PLATFORM_MANAGER`, `ORG_MANAGER`, `INSPECTOR`, `MAINTENANCE_ENGINEER`.
- Procedure: `npm test -- --maxWorkers=1`; `npm run build`; `npm run lint`; focused direct guards via `npx vitest run --pool=forks --maxWorkers=1 src/app/permissions/accessPolicy.test.ts src/app/router/router.test.ts src/features/auth/components/RequireAuth.resources.test.tsx src/features/assets/pages/AssetsPage.resources.test.tsx`; `git diff --check`.
- Expected result: All automated tests pass; route guards permit ORG_MANAGER and direct guard tests redirect the other roles to Forbidden; strict build passes; lint exits zero; whitespace check is clean.
- Round 1: Passed 2026-10-13; tester: Claude Code (automated).
- Evidence: full suite 51 files / 336 tests; focused guard suite 9 files / 95 tests; `npm run build` passed; `npm run lint` exited 0 with six existing `react(only-export-components)` Fast Refresh warnings (in `Toast.tsx`, `main.tsx`, `ReportSectionForm.tsx`, and `router.tsx`); `git diff --check` passed. Manual browser verification was not run because the connected browser was `about:blank`.
- Scope note: Role guards are navigation protection; backend authorization remains authoritative. No changes were made to backend APIs/schema in this Frontend task.

### MF1-08 – MF1-10 Asset Creation and Default Pair Assignment — supporting verification (executed 2026-10-20)

- Preconditions: Backend `feat/mf1-backend-org-admin-resources` and Frontend `feat/mf1-org-admin-resources-hieu`; PostgreSQL 17/Testcontainers; active ORG_MANAGER, Inspector and Drone within the same organization.
- Procedure: Run Backend `AssetApiIntegrationTest` and Frontend `AssetsPage.pairing.test.tsx`. Verify asset creation with default Inspector and Drone pair; tenant-scoped validation rejecting foreign inspectors, foreign drones, or retired drones; pair persistence in `asset_pair_assignments` with `ACTIVE` status; active pair retrieval and reassignment with recorded reason; drawer pairing display and "New inspection" row trigger.
- Expected result: Assets save atomically with their active default operational pair; cross-tenant references fail with 400 `INVALID_INSPECTOR` or `INVALID_DRONE`; reassignment supersedes the previous pair and creates a new active version; UI displays the assigned pair with inspector and drone details.
- Round 1: Passed 2026-10-20; tester: Claude Code (automated).
- Evidence: Backend `AssetApiIntegrationTest` passed 11/11 tests; Frontend `AssetsPage.pairing.test.tsx` passed 3/3 tests.

### MF1-11 – MF1-14 Inspection Creation and Pair Inheritance/Reassignment — supporting verification (executed 2026-10-20)

- Preconditions: Backend `feat/mf1-backend-org-admin-resources` and Frontend `feat/mf1-org-admin-resources-hieu`; PostgreSQL 17/Testcontainers; active asset with assigned default pair.
- Procedure: Run Backend `InspectionCreationApiIntegrationTest` and Frontend `CreateInspectionDialog.test.tsx`. Verify inspection creation inheriting asset default pair snapshot; date ordering and non-empty objective validation; schedule conflict check for overlapping active missions on the same Inspector or Drone (MF1-12); optional override of inspector or drone with mandatory reassignment reason; dispatch to `ASSIGNED` status; rejection of inspections on unpaired or foreign assets; ORG_MANAGER only creation authorization.
- Expected result: Inspections inherit the active operational pair snapshot without mutating asset defaults; planned dates, objective, and schedule conflicts are enforced; unauthorized roles receive 403; dispatched inspections are ready for MF2 inspector assignment response.
- Round 1: Passed 2026-10-20; tester: Claude Code (automated).
- Evidence: Backend `InspectionCreationApiIntegrationTest` passed 7/7 tests; full backend verify passed 644 tests, JaCoCo and Modulith checks; Frontend `CreateInspectionDialog.test.tsx` passed 3/3 tests; full frontend suite passed 53 files / 342 tests and build succeeded.

### MF2-09 – MF2-12 Field Session — supporting verification (executed 2026-10-20)

- Preconditions: Backend `feat/mf1-backend-org-admin-resources` and Frontend `feat/mf1-org-admin-resources-hieu`; PostgreSQL 17/Testcontainers; an inspection assigned to the signed-in Inspector with an approved readiness decision.
- Procedure: Run Backend `InspectionFieldSessionApiIntegrationTest` and Frontend `FieldSessionPage.test.tsx`. Verify the Inspector's session list; starting a session against the newest `APPROVED` readiness decision; the mandatory pre-flight checklist note; postponement with the Inspector's own reason; abort with the Inspector's own reason; refusal to open a second session while one is open.
- Expected result: A session starts only after the pre-flight note is recorded and readiness holds; the startedAt instant is the software's session start and not hardware flight time; postponement keeps the inspection startable while abort ends the record; a second concurrent session is refused.
- Round 1: Passed 2026-10-20; tester: Claude Code (automated).
- Evidence: Backend `InspectionFieldSessionServiceTest` (19 tests) and `InspectionFieldSessionApiIntegrationTest` (9 tests) passed; Frontend `FieldSessionPage.test.tsx` passed 6/6 tests; full frontend suite passed 56 files / 361 tests.

### MF4-01 – MF4-20 Maintenance Work Order Lifecycle — supporting verification (executed 2026-10-20)

- Preconditions: Backend `feat/mf1-backend-org-admin-resources` and Frontend `feat/mf1-org-admin-resources-hieu`; PostgreSQL 17/Testcontainers; an organization with a published repair-required finding and an ORG_MANAGER plus MAINTENANCE_ENGINEER.
- Procedure: Run Backend `MaintenanceApiIntegrationTest` (25 tests) and Frontend `MaintenancePage.test.tsx`. Verify the repair-candidate triage list (MF3-13 handoff), work order creation with priority, due date, corrective scope and acceptance criteria (MF4-01/02), team designation of exactly one lead, one report author and one independent accepting reviewer (MF4-03/04), task creation (MF4-05), estimate versions with system-computed totals and approval (MF4-06/07/08), the execution transitions release/start/declare-complete (MF4-09/10/14), work logs with hours and as-left condition (MF4-11), change requests and their decisions (MF4-12/13), completion report drafting, verification and submission (MF4-15/16/17), independent acceptance (MF4-18), cost reconciliation with the computed variance (MF4-19), and closure (MF4-20).
- Expected result: Each transition is a named action rather than a generic state change; the role decides which actions are offered while the backend stays the enforcement boundary; the accepting reviewer may not be on the executing team; actual cost lines never overwrite an estimate line; the variance is computed by the platform; a work order closes only after independent acceptance and cost reconciliation.
- Round 1: Passed 2026-10-20; tester: Claude Code (automated).
- Evidence: Backend `MaintenanceApiIntegrationTest` passed 25/25 tests; full backend verify passed 648 tests, 0 failures, 0 errors, JaCoCo and Modulith checks met; Frontend `MaintenancePage.test.tsx` passed 6/6 tests and the full frontend suite passed 56 files / 361 tests.

### FE-01 Platform Account Administration — supporting verification (executed 2026-10-20)

- Preconditions: Backend `feat/mf1-backend-org-admin-resources` and Frontend `feat/mf1-org-admin-resources-hieu`; PostgreSQL 17/Testcontainers; an active platform ADMIN and an organization-scoped ORG_MANAGER.
- Procedure: Run Backend `PlatformUserListApiIntegrationTest` and `AdminUserApiIntegrationTest`, and Frontend `PlatformUsersPage.test.tsx`. Verify the platform-wide account list with roles and actor zone; refusal of that list to a non-platform caller; password reset of another account with session revocation; the one-time temporary password shown once and never retrievable again; suspension through the named status change.
- Expected result: The platform administrator (`ADMIN`) manages the administrator-managed accounts only (`ADMIN`, `PLATFORM_MANAGER`, and initial `ORG_MANAGER`); a customer's own workforce is administered by that organization's ORG_MANAGER through a different contract; a password reset revokes the account's sessions and forces a new password at next sign-in; the temporary password is shown once.
- Round 1: Passed 2026-10-20; tester: Claude Code (automated).
- Evidence: Backend `PlatformUserListApiIntegrationTest` passed 3/3 tests and `AdminUserApiIntegrationTest` passed; Frontend `PlatformUsersPage.test.tsx` passed 4/4 tests. The `GET /api/v1/platform/users` listing was added by this work because the ADMIN portal had no way to read the accounts it manages.

### Asset-Specific Recurring Inspection Schedule Creation and Lifecycle — supporting verification (executed 2026-10-26)

- Preconditions: Active organization with registered assets, active default operational pair (Inspector and Drone), and an ORG_MANAGER account.
- Procedure:
  1. In `AssetsPage`, verify the "Recurring schedule" action button on each active asset row, preselecting the asset and opening `CreateInspectionDialog` directly in `RECURRING` mode.
  2. In `AssetDetailDrawer`, verify the dedicated `AssetRecurringSchedulesSection` listing active/paused recurring schedules for that specific asset, displaying objective, cadence (e.g. Every 2 WEEK), assigned inspector, status chip, and direct modal inspection trigger.
  3. In `RecurringSchedulesPanel`, verify the asset filter dropdown (`assetId`) filtering recurring schedules by individual asset.
  4. Run `npx vitest run src/features/assets/pages/AssetsPage.recurringSchedules.test.tsx` and full assets suite `npx vitest run src/features/assets`.
- Expected result:
  - An ORG_MANAGER can initiate recurring inspection schedules directly per asset from both the table row action and the asset detail drawer.
  - The dialog inherits the asset's active operational pair and locks the asset selection.
  - The asset drawer displays existing recurring inspection schedules scoped to that asset, providing quick overview of recurrence frequency, inspector assignment, and status.
  - The recurring schedules management panel filters schedules by asset identifier.
- Round 1: Passed 2026-10-26; tester: Claude Code (automated).
- Evidence: `AssetsPage.recurringSchedules.test.tsx` passed 2/2 tests; full `src/features/assets` suite passed 17 files / 83 tests (100%); `tsc -b && vite build` clean; `oxlint` clean.

### Single Active Recurring Schedule per Asset & Free-text JSON Normalization — supporting verification (executed 2026-10-26)

- Preconditions: Active organization with registered asset and default operational pair; existing active recurring inspection schedule.
- Procedure:
  1. Run Backend `RecurringInspectionScheduleServiceTest` and `InspectionCreationApiIntegrationTest`. Verify:
     - Rejection of creating a second active recurring schedule on the same asset with `ACTIVE_SCHEDULE_EXISTS` (HTTP 409 Conflict).
     - Automatic normalization of free-text strings (`scope`, `componentScope`, `acceptanceCriteria`) into valid JSON primitive strings in `Inspection` and `RecurringInspectionSchedule` domain entities, preventing PostgreSQL `jsonb` syntax errors.
  2. In `CreateInspectionDialog`, verify:
     - Warning alert rendered when attempting to configure a recurring schedule on an asset with an active schedule running.
     - Form submit button disabled with guidance to end the existing schedule before creating a new one.
     - `ensureJsonString` client-side formatting ensuring clean JSON transmission.
  3. In `AssetRecurringSchedulesSection`, verify the "+ Add schedule" action is replaced with an "Active schedule running" status chip when an active schedule is present.
- Expected result:
  - An asset can only hold at most one `ACTIVE` recurring inspection schedule at any given time.
  - Free-text inputs in inspection creation forms are safely sanitized into valid JSON for PostgreSQL `jsonb` columns.
  - UI provides clear feedback and prevents duplicate active schedules.
- Round 1: Passed 2026-10-26; tester: Claude Code (automated).
- Evidence: Backend `RecurringInspectionScheduleServiceTest` passed 9/9 tests; `InspectionCreationApiIntegrationTest` passed 8/8 tests; Frontend `CreateInspectionDialog.test.tsx` passed 7/7 tests; `AssetsPage.recurringSchedules.test.tsx` passed 4/4 tests; `npm run build` and `npm run lint` clean.

### Asset Retirement & Contract Completion Archival — supporting verification (executed 2026-10-26)

- Preconditions: Active organization with registered asset; active ORG_MANAGER account.
- Procedure:
  1. In Backend, run `AssetApiIntegrationTest`. Verify:
     - `POST /api/v1/assets/{assetId}/retire` transitions asset status from `ACTIVE` to `RETIRED`.
     - Retiring an already retired asset is rejected with 409 `INVALID_STATE`.
     - Non-manager roles are forbidden from retiring assets (403 Forbidden).
  2. In Frontend `AssetDetailDrawer`, verify:
     - "Complete & Archive Asset" action button displayed for active assets under manager role.
     - Confirmation modal requiring user approval to retire the asset and archive the contract.
     - Retired assets render informational archival banner, hide new inspection creation triggers, while preserving full document repository and historical inspection logs.
  3. Run `npx vitest run src/features/assets/pages/AssetsPage.recurringSchedules.test.tsx`.
- Expected result:
  - An asset can be safely closed/archived when the contract or project concludes.
  - Retired assets cannot receive new inspection dispatches or edits.
  - All historical inspections, reports, and technical documents remain permanently archived and referenceable.
- Round 1: Passed 2026-10-26; tester: Claude Code (automated).
- Evidence: Backend `AssetApiIntegrationTest` passed 13/13 tests; Frontend `AssetsPage.recurringSchedules.test.tsx` passed 4/4 tests; `npm run build` clean; `oxlint` clean.

## Feature sheet summary

Values for the `Feature 2` summary block (`A2:E8` in the workbook).
The template reads these back by formula, so an export needs them
recorded here.

| Cell | Label | Value |
| --- | --- | --- |
| `B2` | Feature | Asset, Drone, Workforce and Compliance Catalog — MF1 |
| `B3` | Test requirement | Would verify atomic asset registration with its assigned Inspector and Drone, compliance records and due-cycle inspection generation. Default-pair draft/history/activation API exists, but integration remains Pending and inspection creation/dispatch is unimplemented, so no workbook case is recorded. |
