# FE-01: Identity, Enterprise Subscription and Workforce Governance

Report 3 §3.2 titles this feature "Identity, Enterprise Subscription and
Workforce Governance". The filename retains the earlier "identity / access
governance" wording; the filename is stable, the scope is Report 3's.

## Implemented four-role baseline

The recorded authentication, organization-scope and audit checks below concern the existing `ADMIN`, `CLIENT`, `SERVICE_MANAGER`, `INSPECTOR`, and `MAINTENANCE_ENGINEER` roles. They do not verify the 2026-10-07 Enterprise SaaS target roles `ADMIN`, `ORG_ADMIN`, `INSPECTOR`, and `MAINTENANCE_ENGINEER`, or the new tenant/subscription entitlement and workforce-governance rules. Proposed target checks are Pending below; no existing Passed result is reused as evidence for those roles.

## Supporting verification

The checks below support FE-01 but are not additional WFx functional cases and are excluded from the workbook totals.

### W3 authentication and migration foundation gate

Jira SCRUM-58/T001 under SCRUM-108 covers the W3 smoke check for existing authentication and migrations V1–V9. It is owned by Bách and remains a delivery prerequisite for the test environment; it is not counted as an additional functional case in this workbook.

Automated execution on 2026-09-22: Passed. WorkflowBaselineTest verified Flyway versions V1–V9 on a clean PostgreSQL Testcontainers database, and generated credentials authenticated all five role fixtures: ADMIN, CLIENT, SERVICE_MANAGER, INSPECTOR, and MAINTENANCE_ENGINEER. No fixture uses a default password or committed secret. MinIO/evidence storage is tracked separately under FE-04/WF3 (T025/SCRUM-85) and is not part of the FE-01 gate.

### Role-aware portal and navigation

- Preconditions: The canonical five role codes and Report 3 section 3.1.3 screen-access matrix are available to the frontend policy.
- Procedure: Run npm test in the frontend repository; assert access-policy decisions for every workspace/section/role combination, single- and multi-workspace entry targets, legacy-path redirect targets, and the no-access fallback.
- Expected result: Policy decisions match the SRS matrix; a user with multiple workspaces is sent to the chooser; an unavailable section resolves to the access-denied path.
- Round 1: Passed on 2026-09-24; tester: Codex (automated).
- Evidence: src/app/permissions/accessPolicy.test.ts — 19 tests passed.

### Browser authentication flow

- Preconditions: The versioned browser auth endpoints and canonical role contract are available; frontend tests use a mocked HTTP transport.
- Procedure: Run npm.cmd test in frontend; verify form validation, fetching /auth/csrf and sending its declared header before auth mutations, sign-in request/response mapping, cookie-backed refresh, Client registration, first-password setup and logout, plus role-aware return routing and rejection of external/unauthorized return paths.
- Expected result: Access tokens are returned to in-memory session state only; browser refresh credentials are not read from or stored in web storage; registration submits only the Client onboarding contract; assigned backend roles determine the destination; rejected refresh clears the local session.
- Round 1: Passed on 2026-09-24; tester: Codex (automated).
- Evidence: src/shared/api/client.test.ts, src/features/auth/api/authApi.test.ts, src/features/auth/schemas/authSchemas.test.ts, src/features/auth/utils/authRedirect.test.ts, and src/features/auth/api/sessionBootstrap.test.ts — 26 auth-flow tests passed; the full frontend suite at that auth-flow run passed 45/45, including the 19 portal-policy tests. The later complete run passed 52/52 after adding shared-envelope tests and WF3 inspection/report page tests.
- Scope note: The transport is mocked in these frontend tests. A live browser-to-Spring-auth-API end-to-end run was not part of this verification. These results are not an end-to-end test claim.

### Client self-registration persistence gate

- Preconditions: The versioned browser auth endpoints are available; the backend integration environment provisions PostgreSQL through Testcontainers with Flyway migrations V1–V10 applied.
- Procedure: Run `.\mvnw.cmd test -Dtest=ClientRegistrationApiIntegrationTest` in SmartDroneInspection-backend; POST `/api/v1/auth/register` through MockMvc with a CSRF token; assert 201 Created, the normalized organization code, the `CLIENT` role on the created user, and a `CLIENT_REGISTRATION`/`SUCCESS` row in `security_audit_events` whose `subject_user_id` references the created user.
- Expected result: Registration persists the organization, user, role assignment, and security audit event in one transaction without violating the `security_audit_events.subject_user_id` foreign key.
- Round 1: Passed on 2026-09-28; tester: Codex (automated).
- Evidence: Backend `src/test/java/com/smartdroneinspection/users/ClientRegistrationApiIntegrationTest.java` plus the updated `ClientRegistrationServiceTest`; full `.\mvnw.cmd verify` passed 165/165 tests with the JaCoCo and Spring Modulith gates.
- Defect note: Before this round, `POST /api/v1/auth/register` returned 500 because `ClientRegistrationService` passed the generated user id to `SecurityAuditService.record` (raw `JdbcTemplate` SQL) before Hibernate flushed the `users` insert, so the audit insert failed the foreign key introduced in `V3__authentication.sql` (present since commit 46baa59). The fix flushes the saved user before the audit write.
- Scope note: This is an API-level integration test against a real database, not a live browser end-to-end run.

### Admin user creation persistence gate

- Preconditions: An ADMIN account exists; the backend integration environment provisions PostgreSQL through Testcontainers with Flyway migrations V1-V10 applied.
- Procedure: Run `.\mvnw.cmd test -Dtest=AdminUserApiIntegrationTest` in SmartDroneInspection-backend; POST `/api/v1/platform/users` through MockMvc as an ADMIN JWT with a CSRF token; assert 201 Created, the `MAINTENANCE_ENGINEER` role on the created user, a non-empty temporary password, and a `USER_CREATED`/`SUCCESS` row in `security_audit_events` whose `actor_user_id` is the admin and whose `subject_user_id` references the created user.
- Expected result: Creation persists the user, role assignment, and security audit event in one transaction without violating the `security_audit_events.subject_user_id` foreign key.
- Round 1: Passed on 2026-09-28; tester: Claude Code (automated).
- Evidence: Backend `src/test/java/com/smartdroneinspection/users/AdminUserApiIntegrationTest.java` plus `AdminUserServiceTest`; full `.\mvnw.cmd verify` passed 167/167 tests with the JaCoCo and Spring Modulith gates.
- Defect note: Before this round, `POST /api/v1/platform/users` returned 500 for the same cause as the client-registration defect above: `AdminUserService.create` passed the generated user id to `SecurityAuditService.record` (raw `JdbcTemplate` SQL) before Hibernate flushed the `users` insert. The fix uses `saveAndFlush` before the audit write. Verified RED first: the new integration test failed with 500 instead of 201 on the unfixed code, then passed after the one-line fix.
- Scope note: This is an API-level integration test against a real database, not a live browser end-to-end run.

### Cross-cutting successful API response-envelope verification

This is a shared API contract check recorded here for traceability. It is not an FE-01-only acceptance case or an additional workbook row.

- Preconditions: The backend and first-party clients use the same versioned response contract; Docker-backed backend integration tests are available.
- Procedure: Run .\mvnw.cmd verify in backend, npm.cmd test in frontend, and flutter test plus flutter analyze in mobile; inspect server/client adapter assertions for success envelopes, Problem Details, and bodyless logout behavior.
- Expected result: Successful JSON bodies expose success, message, and data; web/mobile callers receive the inner typed payload; error responses remain Problem Details; 204 No Content remains bodyless. Binary streaming controllers are intentionally not wrapped by the JSON envelope.
- Round 1: Passed on 2026-09-24; tester: Codex (automated).
- Evidence: Backend ApiResponseTest and WorkflowBaselineTest; frontend src/shared/api/apiResponse.test.ts; mobile test/core/network/api_response_interceptor_test.dart. Full verification commands and results are listed in the delivery hand-off.

## Proposed MF1 target cases (not executed)

These FE-01 target cases are supporting checks outside the fixed WFx workbook rows, matching the existing FE-01 foundation-gate convention. They do not alter workbook statistics. Every status below is Pending with no execution date or tester.

| Target check | Procedure | Expected result | Preconditions | Status | Evidence |
| --- | --- | --- | --- | --- | --- |
| FE01-T01 Organization and subscription entitlement gate | Register an enterprise organization; attempt MF1 setup before ADMIN activates the subscription; activate with ADMIN; attempt cross-tenant workspace access; reactivate after an existing subscription's end date. | MF1 setup is blocked until entitlement is active; ADMIN activates/reactivates the workspace; an ended active row is marked EXPIRED with audit before the replacement term; a user from another organization cannot read or mutate the workspace. | Two organizations; inactive subscription; ended ACTIVE subscription fixture; Docker/Testcontainers PostgreSQL. | Partial — entitlement and tenant-isolation checks Passed 2026-10-10; subscription activation/reactivation API tests Pending 2026-10-21 | `SubscriptionEntitlementServiceTest` — 4/4; cross-tenant isolation via `WorkforceApiIntegrationTest`; `SubscriptionActivationApiIntegrationTest` authored for activation/audit/authorization/period/window/duplicate/organization/resource-gate/reactivation but blocked before context startup because Testcontainers has no Docker environment. |
| FE01-T02 Role separation of duties | Attempt ORG_ADMIN setup actions as `INSPECTOR`/`MAINTENANCE_ENGINEER`; attempt Inspector/Engineer evidence-quality actions as `ORG_ADMIN` or `ADMIN`; attempt independent maintenance acceptance by the report author or repair team. | Only ORG_ADMIN manages organization resources/workforce/teams; Inspectors and Engineers act only on assigned work; ADMIN has no default customer technical or acceptance authority; author/executing-team self-acceptance is denied. | Target four-role fixtures and one assigned inspection/work-order exist. | Partial — workforce side Passed 2026-10-11; maintenance self-acceptance still Pending | `WorkforceApiIntegrationTest` 22/22 and `WorkforceServiceTest` 13/13, including cross-tenant email non-disclosure: a foreign email returns `404 USER_NOT_FOUND`, while a same-organization duplicate remains `409 EMAIL_ALREADY_EXISTS`; privileged-role and peer-ORG_ADMIN mutations remain blocked. MF4 independent maintenance acceptance is unimplemented. |

### Review-fix verification (executed 11 October 2026)

- Preconditions: Integrated MF1 branch with PostgreSQL Testcontainers available; two organization fixtures and active ORG_ADMIN actors.
- Procedure: Run `./mvnw -Dtest=WorkforceApiIntegrationTest,DroneApiIntegrationTest,DroneDocumentApiIntegrationTest,DronePersistenceTest,CompliancePersistenceTest,EvidenceOwnershipServiceTest,WorkforceCredentialExpiryWindowTest test` and attempt provisioning with an email owned by another organization.
- Expected result: A globally unique email must not become an existence oracle: foreign-organization email returns the same non-disclosing `404 USER_NOT_FOUND` used for an absent user; same-organization duplicate remains a useful `409 EMAIL_ALREADY_EXISTS`. Persistence fixtures must roll back so later tests do not depend on execution order.
- Round 4: Passed on 2026-10-11; tester: Claude Code (automated). The focused command passed 68 tests; the full `./mvnw verify` passed 301 tests, 0 failures, 0 errors, coverage gate met.
- Defect note: The security review found `AdminUserService`'s global email check exposed `409 EMAIL_ALREADY_EXISTS` for another tenant's address. The fix scopes the non-disclosure decision at `UserAccessService` before delegation to the platform-admin service, preserving same-organization conflict behavior. The order-dependent persistence failure was reproduced by running `DronePersistenceTest` before `DroneApiIntegrationTest` (1 failure), then eliminated by adding transactional rollback to the persistence tests. |

### Enterprise SaaS entitlement and workforce governance (executed 10 October 2026)

These execute the previously Pending `FE01-T01`/`FE01-T02` checks for the MF1
resource-setup slice. They are supporting gates outside the fixed WFx workbook
rows, matching the existing FE-01 foundation-gate convention, so they do not
alter workbook statistics.

#### Subscription entitlement gate

- Preconditions: Backend branch `integrate/mf1-resources`; PostgreSQL 17 through Testcontainers; Flyway `V25__enterprise_saas_target_schema.sql` creating `subscriptions`.
- Procedure: Run `./mvnw -Dtest=SubscriptionEntitlementServiceTest test`; call `SubscriptionEntitlement.requireActive(organizationId, at)` for an in-window ACTIVE subscription, for a subscription whose exclusive `endsAt` has passed, and for expired, suspended and missing subscriptions.
- Expected result: `requireActive` returns normally only for an ACTIVE subscription whose window covers the instant; every other case raises a `FORBIDDEN` `SUBSCRIPTION_INACTIVE` ProblemDetail. A null `startsAt`/`endsAt` is treated as unbounded, and one organization's entitlement never satisfies another's.
- Round 3: Passed on 2026-10-10; tester: Claude Code (automated).
- Evidence: `SubscriptionEntitlementServiceTest` — 4/4. Part of the merged `./mvnw verify` run: 254 tests, 0 failures, 0 errors, `All coverage checks have been met.`, BUILD SUCCESS.
- Scope note: This verifies the entitlement decision itself. Subscription activation/reactivation is now implemented locally, but its API integration procedure remains Pending because Docker/Testcontainers was unavailable on 2026-10-21.

#### ORG_ADMIN workforce provisioning and role-safe lifecycle

- Preconditions: Same merged baseline; an active `ORG_ADMIN` in a `CUSTOMER_ORGANIZATION` zone, plus a second organization fixture for isolation checks.
- Procedure: Run `./mvnw -Dtest=WorkforceApiIntegrationTest,WorkforceServiceTest test`; exercise `POST/GET/PATCH/PUT /api/v1/workforce/users` as ORG_ADMIN, then call the public `UserAccess` facade directly to attempt granting `ORG_ADMIN` or `ADMIN`, and to mutate a peer ORG_ADMIN's status and roles.
- Expected result: Provisioning returns 201 with a one-time temporary password; organization scope comes from the authenticated actor and a request-supplied organization is ignored; only `INSPECTOR` and `MAINTENANCE_ENGINEER` are accepted; reads stay available while writes require entitlement; a rejected operation writes no user, role, audit, session or refresh-token row and leaves a peer ORG_ADMIN unchanged.
- Round 3: Passed on 2026-10-10; tester: Claude Code (automated).
- Evidence: `WorkforceApiIntegrationTest` 20/20 and `WorkforceServiceTest` 13/13, inside the 254-test merged run above.
- Defect note: An earlier implementation of this gate was rejected in review because `UserAccessService` relied on `RolePolicy`, which permits `ORG_ADMIN` for customer users. A direct facade call could therefore grant a privileged role or alter a peer ORG_ADMIN. Five direct-facade regression tests were written first and observed failing 5/5, then the workforce role allowlist and target-membership check were added and those five passed.
- Known gap: the peer-admin rejection tests assert the target's auth session is not revoked but do **not** assert the associated refresh token remains unrevoked. The role guard itself is covered.
- Scope note: This covers provisioning and lifecycle only. Credential records are recorded separately below.

### Enterprise SaaS identity, registration and target-schema reset (executed 8 October 2026)

- Preconditions: Backend branch `feat/enterprise-saas-reset` with forward migrations `V24__enterprise_saas_role_and_schema_alignment.sql`, `V25__enterprise_saas_target_schema.sql` and `V26__enterprise_saas_runtime_cutover.sql`; PostgreSQL 17 provided through Testcontainers.
- Procedure: Run `./mvnw clean verify` in SmartDroneInspection-Backend; execute `OrganizationRegistrationApiIntegrationTest`, `V24PopulatedMigrationTest`, `V25TargetSchemaFoundationTest`, `FullDatabaseSchemaMigrationTest`, `RuntimePersistenceInventoryTest`, `RolePolicyTest` and `ModulithArchitectureTest` as part of that gate.
- Expected result: `POST /api/v1/auth/register` returns 201 and persists the organization, its first `ORG_ADMIN` in the `CUSTOMER_ORGANIZATION` zone, and one `ORGANIZATION_REGISTRATION`/`SUCCESS` row in `audit_events` in a single transaction; V24 fails closed on unmappable provider/workforce identities, duplicate target-role collapse and invalid tenant scope; the migrated runtime schema is exactly the 41 target application tables plus `event_publication` and `flyway_schema_history`.
- Round 2: Passed on 2026-10-08; tester: Hermes (automated).
- Evidence: Full backend gate `./mvnw clean verify` — 88 tests, 0 failures, 0 errors, JaCoCo coverage gate and Spring Modulith boundary verification passed. `AuditEvents`-targeted assertions live in `OrganizationRegistrationApiIntegrationTest`; the exact inventory is asserted by `FullDatabaseSchemaMigrationTest#flywayCreatesExactlyTheFortyOneTargetTablesAndFrameworkRegistry` and `RuntimePersistenceInventoryTest#applicationTableInventoryContainsOnlyTheFortyOneTargetTables`.
- Change note: This supersedes the earlier `security_audit_events`/`CLIENT_REGISTRATION` wording above. That table was a v1 artifact and is dropped by V26; the target audit home is `audit_events` with action `ORGANIZATION_REGISTRATION`. The earlier Round 1 results remain recorded as historical v1 evidence for the version actually tested.
- Scope note: This gate covers identity, registration, audit and target schema only. It is **not** evidence that MF1–MF4 workflow behavior exists.

### Frontend and mobile role-contract gates (executed 8 October 2026)

- Preconditions: Frontend and mobile clients aligned to the four canonical roles `ADMIN`, `ORG_ADMIN`, `INSPECTOR`, `MAINTENANCE_ENGINEER`.
- Procedure: Run `npm run lint && npm test && npm run build` in SmartDroneInspection-Frontend; run `dart format --output=none --set-exit-if-changed .`, `flutter analyze` and `flutter test` in SmartDroneInspection-Mobile (Flutter 3.47.6 / Dart 3.13.5).
- Expected result: Provider/marketplace UI and API client code is removed; registration posts the organization-onboarding contract; unknown or retired role codes are rejected rather than coerced; mobile stores tokens only in secure storage.
- Round 2: Passed on 2026-10-08; tester: Hermes (automated).
- Evidence: Frontend 25 test files / 128 tests passed and production build succeeded (5 `react(only-export-components)` fast-refresh lint warnings, no errors). Mobile: format clean (0 changed), `flutter analyze` reported one pre-existing `info` lint in `lib/core/router/app_router.dart` that is not part of this change, and 16/16 tests passed.
- Scope note: Frontend tests use a mocked transport; mobile tests use fakes. Neither is a live browser/device end-to-end run.

#### MF1-04/05 workforce credential records and internal review

- Preconditions: Same merged baseline at `dcd6516`; `V25` table `workforce_credentials`; an active ORG_ADMIN, a same-organization workforce subject, and a same-organization evidence record.
- Procedure: Run `./mvnw -Dtest=WorkforceCredentialApiIntegrationTest,WorkforceCredentialPersistenceTest,EvidenceOwnershipServiceTest test`; exercise `POST /api/v1/workforce/credentials`, the list endpoint, and `PUT /{id}/review`; submit a foreign subject, a foreign `evidenceId`, an expiry that precedes its issue date, a blank `credentialType`, and a blank rejection reason.
- Expected result: Credential creation succeeds only for a same-organization subject and same-organization evidence; a foreign subject and foreign evidence both return 404 with an identical problem body so the endpoint cannot be used to probe another tenant's identifiers; an inverted date range returns 400; a review records reviewer, timestamp and reason together; expiry status is derived at read time; the credential record survives its subject being suspended; and no field or status claims government or authority verification.
- Round 3: Passed on 2026-10-10; tester: Claude Code (automated).
- Evidence: `WorkforceCredentialApiIntegrationTest` 15/15, `WorkforceCredentialPersistenceTest` 5/5, `EvidenceOwnershipServiceTest` 3/3, inside the 254-test merged run above.
- Module-boundary note: verifying `evidence_id` tenant ownership required a path from `workforce` to `inspections`. A single-method facade `com.smartdroneinspection.inspections.EvidenceOwnership` was added at the `inspections` module root, and `workforce` was granted a module-root dependency on `inspections` — not `inspections::repository`, so Spring Modulith still forbids importing the evidence repositories or entities. The boundary was checked with a temporary probe that imported `EvidenceRepository` and correctly failed verification; the probe was removed before commit.
- Configuration note: the `EXPIRING_SOON` horizon is bound to `app.workforce.credential-expiring-soon-window` (env `CREDENTIAL_EXPIRING_SOON_WINDOW`, default `60d`) via `WorkforceProperties`, so a deployment can change it without a rebuild. No requirement document specifies a window — MF1-05 asks only that expiry warnings be calculated — so 60 days is a product decision made for commercial drone inspection, where operator credentials and liability insurance are annual or longer. Covered by `WorkforceCredentialExpiryWindowTest` (5 cases), which proves the configured window and not a literal decides the status, and pins the default across `application.yml`, the properties class and the entity fallback so those three cannot drift apart silently.
- Scope note: `EXPIRING_SOON` exists only on `workforce_credentials`. `flight_permits` (MF1-07) has no such status, so permit records carry no expiring-soon signal in this release.

### Frontend MF1 resource-navigation and integration verification (executed 13 October 2026)

This is supporting frontend evidence, outside the fixed WFx workbook rows, consistent with the FE-01 foundation-gate convention. Workbook statistics remain unchanged.

- Preconditions: Frontend branch `feat/mf1-fe-drones`; four canonical roles; React Router guard and local test fixtures.
- Procedure: Run `npx vitest run --pool=forks --maxWorkers=1 src/app/permissions/accessPolicy.test.ts src/app/router/router.test.ts src/features/auth/components/RequireAuth.resources.test.tsx src/features/assets/pages/AssetsPage.resources.test.tsx`; evaluate the access-policy matrix, direct `RequireAuth` outcomes for `/client/workforce` and `/client/assets`, and the resource-tab composition.
- Expected result: ORG_ADMIN can enter the client Workforce and Assets guard; ADMIN, INSPECTOR and MAINTENANCE_ENGINEER are redirected to the forbidden surface on direct access; Drones and Permits tabs render only for ORG_ADMIN; existing Admin/Operations route entries remain matched.
- Round 1: Passed on 2026-10-13; tester: Claude Code (automated).
- Evidence: focused command passed 4 files / 44 tests, including direct guard behavior for both paths across all four roles.
- Scope note: This is a component/guard test using the real RequireAuth component, not a browser-to-backend end-to-end authorization test. Backend authorization remains authoritative.

## Coverage boundary

The recorded gates verify authentication/migration setup, v1 role-to-screen policy, browser-auth contracts, v1 Client-registration persistence and audit, the shared API envelope, and — from Round 2 — Enterprise SaaS organization registration against `audit_events`, the fail-closed V24 role migration, the exact 41-table target schema, and client role-contract alignment for the four canonical roles.

They do **not** establish the requirements in Report 3 §3.2 that carry authority
or entitlement meaning:

| Report 3 §3.2 requirement | Status here |
| --- | --- |
| Subscription activation is a separate entitlement decision (`FE01-T01`) | Unverified. |
| A report reviewer must be **identified and qualified** for the scope; account administration rights alone confer no professional authority (`FE01-T02`) | Unverified. |
| Inspectors and Engineers can act only on their assignments; team designations narrow permission further | Only partly evidenced — `WF3-009` verifies list scope, not act-on-assignment scope. |
| ENTERPRISE offers only 1-, 6- and 12-month periods; no trial or unlimited-use promise is presumed | Unverified. |
| Removing a user from a team or replacing a report author ends future authority **without erasing prior attribution** | Unverified. |
| Logout, password/role/status change and revocation invalidate affected sessions | Unverified. |
| MF1–MF4 workflow behavior | Out of reset scope per §3.1. |
| Live browser end-to-end registration/login | Not run. |

## Feature sheet summary

Values for the `Feature 1` summary block (`A2:E8` in the workbook).
The template reads these back by formula, so an export needs them
recorded here.

| Cell | Label | Value |
| --- | --- | --- |
| `B2` | Feature | Identity, Enterprise Subscription and Workforce Governance |
| `B3` | Test requirement | Verifies workspace entitlement, organization and assignment scope for the four-role target. Supporting checks only; no WFx functional case is assigned. |
