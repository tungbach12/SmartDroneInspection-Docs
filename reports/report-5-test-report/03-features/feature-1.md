# Feature 1 sheet — FE-01 foundation, FE-02 assets, and FE-03 service intake

This file mirrors the fixed `Feature 1` workbook sheet. It is not the SRS
feature `FE-01`; it contains the WF1/FE-02 and WF2/FE-03 cases. The FE-01 W3
foundation gate is recorded above the functional rows and is not counted as a
Report 5 case.

| Template field | Value |
| --- | --- |
| Feature | Feature 1 sheet — FE-01 foundation, FE-02/FE-03 service intake |
| Test requirement | FE-01 foundation gate; FE-02 asset ownership and periodic planning; FE-03 client request, quotation/order, and assignment controls |
| Number of TCs | 8 |
| Case mapping | WF1-001–004 → FE-02; WF2-001–004 → FE-03 |

## FE-01 W3 foundation gate

Jira `SCRUM-58/T001` under `SCRUM-108` covers the W3 smoke check for existing
authentication and migrations V1–V9. It is owned by Bách and remains a
delivery prerequisite for the test environment; it is not counted as an
additional functional case in this workbook.

Automated execution on 2026-09-22: `Passed`. `WorkflowBaselineTest` verified
Flyway versions V1-V9 on a clean PostgreSQL Testcontainers database, and generated credentials authenticated
all five role fixtures (`ADMIN`, `CLIENT`, `SERVICE_MANAGER`, `INSPECTOR`, and
`MAINTENANCE_ENGINEER`). No fixture uses a default password or committed
secret. MinIO/evidence storage is tracked separately under FE-04/WF3 (`T025/SCRUM-85`)
and is not part of the FE-01 gate.

### FE-01 role-aware portal/navigation verification

This is a supporting automated verification of the existing Report 3 screen
access matrix, not an additional functional workbook case.

- Preconditions: the canonical five role codes and Report 3 section 3.1.3
  screen-access matrix are available to the frontend policy.
- Procedure: run `npm test` in the frontend repository; assert the access-policy
  decisions for every workspace/section/role combination, single- and
  multi-workspace entry targets, legacy-path redirect targets, and the no-access
  fallback.
- Expected result: policy decisions match the SRS matrix; a user with multiple
  workspaces is sent to the chooser; an unavailable section resolves to the
  access-denied path.
- Round 1 result: **Passed** on 2026-09-24; tester: Codex (automated).
- Evidence: `src/app/permissions/accessPolicy.test.ts` — 19 tests passed.

### FE-01 browser authentication flow verification

This supporting automated gate verifies the frontend against the existing
browser-auth contract. It is not an additional WFx functional case or workbook
row, and it does not change the 15 functional cases below.

- Preconditions: the versioned browser auth endpoints and canonical role
  contract are available; frontend tests use a mocked HTTP transport.
- Procedure: run `npm.cmd test` in `frontend`; verify form validation, fetching
  `/auth/csrf` and sending its declared header before auth mutations,
  request/response mapping for sign-in,
  cookie-backed refresh, Client registration, first-password setup and logout,
  plus role-aware return routing and rejection of external/unauthorized return
  paths.
- Expected result: access tokens are returned to in-memory session state only;
  browser refresh credentials are not read from or stored in web storage;
  registration submits only the Client onboarding contract; assigned backend
  roles determine the destination; rejected refresh clears the local session.
- Round 1 result: **Passed** on 2026-09-24; tester: Codex (automated).
- Evidence: `src/shared/api/client.test.ts`,
  `src/features/auth/api/authApi.test.ts`,
  `src/features/auth/schemas/authSchemas.test.ts`,
  `src/features/auth/utils/authRedirect.test.ts`, and
  `src/features/auth/api/sessionBootstrap.test.ts` — 26 auth-flow tests passed;
  the full frontend suite passed 45/45, including the 19 portal-policy tests.
- Scope note: the transport is mocked in these frontend tests. Live browser to
  Spring API integration was not executed because Docker/backend was
  unavailable in this environment; this result is not an end-to-end test claim.

## Function A — FE-02 asset catalog and organization scope (WF1)

| Test Case ID | Test Case Description | Test Case Procedure | Expected Results | Pre-conditions | Round 1 | Test date | Tester | Round 2 | Test date | Tester | Round 3 | Test date | Tester | Note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| WF1-001 | Admin publishes an inspection category and checklist. | Sign in as Admin; create or update the category and checklist; activate it; read it from planning. | Only a valid active category/checklist is available for planning and its version is retained. | Admin is active; checklist validation passes. | Pending |  |  | Pending |  |  | Pending |  |  |  |
| WF1-002 | Client creates an asset for its own organization. | Sign in as Client; submit asset identity and location; save; open the asset list. | Asset is created once, linked to the client organization, and visible to that organization. | Client is active and has organization scope. | Pending |  |  | Pending |  |  | Pending |  |  |  |
| WF1-003 | Client cannot access another organization's asset. | Sign in as a client from organization A; request an asset owned by organization B; try read and update operations. | The API denies both operations without exposing asset details. | Organizations A and B and their assets exist. | Pending |  |  | Pending |  |  | Pending |  |  |  |

## Function B — FE-02 scheduling and FE-03 request/quotation (WF1 → WF2)

| Test Case ID | Test Case Description | Test Case Procedure | Expected Results | Pre-conditions | Round 1 | Test date | Tester | Round 2 | Test date | Tester | Round 3 | Test date | Tester | Note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| WF1-004 | Periodic schedule creates one due inspection request. | Create an active schedule; advance to its due cycle; run the scheduler twice; inspect requests. | Exactly one request is created for the asset and cycle; a retry does not duplicate it. | Active asset, schedule, checklist, and scheduler are available. | Pending |  |  | Pending |  |  | Pending |  |  |  |
| WF2-001 | Client creates an ad-hoc inspection request. | Sign in as Client; select an owned asset; enter scope, location, and preferred timing; submit. | Request is accepted with an auditable creator and organization; invalid scope is rejected. | Owned asset exists; client is active. | Pending |  |  | Pending |  |  | Pending |  |  |  |
| WF2-002 | Service Manager prepares and sends a quotation. | Sign in as Service Manager; open the request; add price, scope, and validity; save a version; send it. | A versioned quotation is stored and visible to the correct client; prior versions remain traceable. | Request is actionable; manager is active. | Pending |  |  | Pending |  |  | Pending |  |  |  |

## Function C — FE-03 order confirmation and assignment (WF2)

| Test Case ID | Test Case Description | Test Case Procedure | Expected Results | Pre-conditions | Round 1 | Test date | Tester | Round 2 | Test date | Tester | Round 3 | Test date | Tester | Note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| WF2-003 | Client approves a quotation and confirms the service order. | Sign in as Client; review the latest quotation; approve it; open the order and billing status. | The approved quotation becomes the confirmed order; the first service billing milestone is recorded. | Quotation is in an approvable state; client owns the request. | Pending |  |  | Pending |  |  | Pending |  |  |  |
| WF2-004 | Service Manager assigns an Inspector with assignment scope. | Sign in as Service Manager; assign an active Inspector; open the task as the Inspector; attempt an unrelated task. | Assigned Inspector can access only the assigned task; unassigned or conflicting access is denied. | Confirmed order exists; candidate Inspector is active. | Pending |  |  | Pending |  |  | Pending |  |  |  |
