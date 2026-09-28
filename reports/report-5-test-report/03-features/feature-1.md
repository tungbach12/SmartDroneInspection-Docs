# Feature 1 sheet — FE-01 foundation, FE-02 assets, and FE-03 service intake

This file mirrors the fixed `Feature 1` workbook sheet. It is not the SRS
feature `FE-01`; it contains the WF1/FE-02 and WF2/FE-03 cases. The FE-01 W3
foundation gate is recorded above the functional rows and is not counted as a
Report 5 case.

| Template field | Value |
| --- | --- |
| Feature | Feature 1 sheet — FE-01 foundation, FE-02/FE-03 service intake |
| Test requirement | FE-01 foundation gate; FE-02 asset ownership and periodic planning; FE-03 client request, quotation/order, and assignment controls |
| Number of TCs | 17 |
| Case mapping | WF1-001–004 and WF1-011–016 → FE-02; WF1-017–019 and WF2-001–004 → FE-03 |

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
  the full frontend suite at that auth-flow run passed 45/45, including the 19
  portal-policy tests. The later complete run passed 52/52 after adding the
  shared-envelope tests and WF3 inspection/report page tests; see the
  cross-cutting verification below.
- Scope note: the transport is mocked in these frontend tests. A live browser
  to Spring auth API end-to-end run was not part of this verification; these
  results are not an end-to-end test claim.

### Cross-cutting successful API response-envelope verification

This is a supporting contract verification, not an additional business-flow
case or workbook row. It verifies the shared successful-JSON contract without
changing the 15 functional workbook cases.

- Preconditions: the backend and first-party clients use the same versioned
  response contract; Docker-backed backend integration tests are available.
- Procedure: run `.\mvnw.cmd verify` in `backend`, `npm.cmd test` in
  `frontend`, `flutter test` and `flutter analyze` in `mobile`; inspect the
  server/client adapter assertions for success envelopes, Problem Details, and
  bodyless logout behavior.
- Expected result: successful JSON bodies expose `success`, `message`, and
  `data`; web/mobile callers receive the inner typed payload; error responses
  remain Problem Details; `204 No Content` remains bodyless. Binary streaming
  controllers are intentionally not wrapped by the JSON envelope.
- Round 1 result: **Passed** on 2026-09-24; tester: Codex (automated).
- Evidence: backend `ApiResponseTest` and `WorkflowBaselineTest`; frontend
  `src/shared/api/apiResponse.test.ts`; mobile
  `test/core/network/api_response_interceptor_test.dart`. Full verification
  commands and results are listed in the delivery hand-off.

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

## Function D — FE-02/FE-03 schedule proposals and due-cycle handoff (WF1 revision)

These cases were added by the 2026-09-28 WF1 revision. `WF1-017` is a
**producer-side** verification: it asserts event identity, payload, and
per-cycle idempotency with an in-process listener standing in for the WF2
consumer. The consumer half (one `PERIODIC` request per replayed event) is
pending T021.

| Test Case ID | Test Case Description | Test Case Procedure | Expected Results | Pre-conditions | Round 1 | Test date | Tester | Round 2 | Test date | Tester | Round 3 | Test date | Tester | Note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| WF1-011 | Client registers an asset. | Sign in as Client; submit code, name, category, and location; read the created asset. | The asset is created once in `PENDING_REVIEW`, linked to the client organization, and readable only by that organization. | Client is active with organization scope; an active category exists. | Passed | 2026-09-28 | Hiếu | Passed | 2026-09-28 | Hiếu | Passed | 2026-09-28 | Hiếu | Automated evidence: `AssetApiIntegrationTest.clientCreatesAssetInPendingReviewState`; `AssetWorkflowIntegrationTest.fullWf1FlowFromAssetCreationToDueEvent`. |
| WF1-012 | Service Manager approves a pending asset. | Sign in as Service Manager; approve the asset; read the generated proposals. | The asset becomes `ACTIVE` and one `GENERATED` proposal exists per suggested frequency of its category. | Asset is `PENDING_REVIEW`; its category has suggested frequencies and an active checklist template. | Passed | 2026-09-28 | Hiếu | Passed | 2026-09-28 | Hiếu | Passed | 2026-09-28 | Hiếu | Automated evidence: `AssetReviewApiIntegrationTest.managerApprovalActivatesAssetAndGeneratesOneProposalPerSuggestion`. |
| WF1-013 | Service Manager rejects a pending asset. | Sign in as Service Manager; reject the asset; list its proposals. | The asset becomes `REJECTED` and no proposals are created. | Asset is `PENDING_REVIEW`. | Passed | 2026-09-28 | Hiếu | Passed | 2026-09-28 | Hiếu | Passed | 2026-09-28 | Hiếu | Automated evidence: `AssetReviewApiIntegrationTest.approvalRequiresSuggestedFrequenciesAndRejectionLeavesNoProposals`. |
| WF1-014 | Service Manager reviews schedule proposals. | Sign in as Service Manager; approve one proposal; reject another; approve one with an adjusted interval. | Approved proposals become `MANAGER_APPROVED` with the adjusted frequency retained; rejected proposals become `MANAGER_REJECTED`; only the Service Manager may review. | Asset is `ACTIVE`; its proposals are `GENERATED`. | Passed | 2026-09-28 | Hiếu | Passed | 2026-09-28 | Hiếu | Passed | 2026-09-28 | Hiếu | Automated evidence: `ScheduleProposalApiIntegrationTest.managerReviewsProposalAndClientOnlySeesApprovedOwnOrg`; `AssetReviewApiIntegrationTest.onlyServiceManagerCanReview`. |
| WF1-015 | Client selects one approved proposal. | Sign in as Client; read the approved options; select one; read the asset schedules. | Exactly one `ACTIVE` schedule exists for the asset; the selected proposal is `CLIENT_SELECTED` and its approved siblings are `SUPERSEDED`. | At least one `MANAGER_APPROVED` proposal on an owned asset that has no active schedule. | Passed | 2026-09-28 | Hiếu | Passed | 2026-09-28 | Hiếu | Passed | 2026-09-28 | Hiếu | Automated evidence: `ScheduleProposalApiIntegrationTest.selectingCreatesOneScheduleSupersedesSiblingsAndIsNotRepeatable`; `AssetWorkflowIntegrationTest.fullWf1FlowFromAssetCreationToDueEvent`. |
| WF1-016 | Selection cannot be repeated or cross organizations. | Select the same proposal twice; select a foreign-organization proposal; operate on a foreign-organization schedule. | The second selection conflicts; foreign-organization proposal and schedule access returns not found without exposing details. | An active schedule already exists; a foreign-organization proposal exists. | Passed | 2026-09-28 | Hiếu | Passed | 2026-09-28 | Hiếu | Passed | 2026-09-28 | Hiếu | Automated evidence: `ScheduleProposalApiIntegrationTest.crossOrgSelectionAndNonManagerReviewAreDenied`; `InspectionScheduleServiceTest.crossOrgScheduleOperationsAreDenied`. |
| WF1-017 | The due-cycle publisher emits one event per cycle. | Force `next_due_at` into the past; run the publisher twice; inspect the published events. | Exactly one `InspectionScheduleDue` event carries the correct organization, asset, checklist template, and due cycle; a replayed run publishes nothing. | An `ACTIVE` schedule has `next_due_at` in the past. | Passed | 2026-09-28 | Hiếu | Passed | 2026-09-28 | Hiếu | Passed | 2026-09-28 | Hiếu | Automated evidence: `PeriodicRequestHandoffTest.publishesExactlyOneEventPerDueScheduleCycleAndReplayIsSilent`; `AssetWorkflowIntegrationTest.fullWf1FlowFromAssetCreationToDueEvent`. |
| WF1-018 | Asset document upload is validated and scoped. | Upload a png/jpeg/webp/pdf within 10 MB to an active asset; upload an unsupported type, an oversize file, and a document to a pending asset; list and stream as another organization. | Only supported types within the size limit reach storage; unsupported types and oversize files are rejected; a pending asset rejects upload; another organization cannot list or stream the document. | An active asset exists; type and size fixtures are available. | Passed | 2026-09-28 | Hiếu | Passed | 2026-09-28 | Hiếu | Passed | 2026-09-28 | Hiếu | Automated evidence: `AssetDocumentApiIntegrationTest.activeAssetDocumentUploadsAndListsForOwnOrgOnly`; `unsupportedTypeOversizeAndPendingAssetsAreRejected`; `returnsAssetOnlyForItsOrganization`. |
| WF1-019 | Negative scope sweep across every WF1 endpoint. | Exercise each WF1 endpoint across two organizations and the five roles, including unauthenticated access. | Role and organization scope are enforced on every endpoint; a Service Manager cannot create assets or manage the catalog; a Client cannot review assets; unauthenticated access returns a Problem Details 401. | Two organizations and the five role fixtures exist. | Passed | 2026-09-28 | Hiếu | Passed | 2026-09-28 | Hiếu | Passed | 2026-09-28 | Hiếu | Automated evidence: `AssetWorkflowIntegrationTest.negativeScopeSweepAcrossEveryWf1Endpoint`; `managerReviewQueueIsPlatformScopedAndClosedToOtherRoles`. |
