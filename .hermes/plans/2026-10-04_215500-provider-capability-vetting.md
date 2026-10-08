# Provider Capability Selection and Independent Vetting Implementation Plan

> **For Hermes:** Use subagent-driven-development skill to implement this plan task-by-task.

**Goal:** Implement provider onboarding and vetting so a Provider Organization can declare inspection capability, maintenance capability, or both, while the Platform Operator verifies each declared capability independently without adding a new role.

**Architecture:** Add provider capability/vetting as a real vertical slice rather than encoding the choice in the existing user role. Keep the six canonical roles unchanged: the Provider Manager represents the organization, the Platform Operator performs vetting, and capability records determine eligibility for inspection or maintenance work. Store shared provider identity separately from capability-specific evidence and decisions so one capability can be `VERIFIED` while the other is `PENDING`, `ADDITIONAL_INFO_REQUIRED`, or `REJECTED`.

**Tech Stack:** Java 21, Spring Boot 4.1, Spring Modulith, PostgreSQL/Flyway, Spring MVC validation, React 19, TypeScript, Vite, Material UI, Vitest/React Testing Library, Maven wrapper.

---

## Current context and assumptions

- The SRS change is already present on the docs branch `docs/provider-capability-vetting`.
- Existing SRS files define the six-role target model and now contain BR-05 and BR-41, UC-03, Provider Organization requirements, and the SRS change record.
- The backend currently has no provider-vetting module, provider capability entity, provider-vetting API, or provider-specific migration.
- The backend still contains legacy role constants/schema (`ADMIN`, `CLIENT`, `SERVICE_MANAGER`, `INSPECTOR`, `MAINTENANCE_ENGINEER` in Java; older role literals in `V3__authentication.sql`). This implementation must not silently rename roles. First reconcile the runtime role baseline and authorization mapping with the target SRS.
- Existing provider-facing business modules are `inspectionrequests` and `maintenance`; do not create speculative top-level `missions`, `reports`, `defects`, or `tickets` modules.
- The current implementation is not proof that the target multi-provider flow is deployed. All target API/UI work must be labelled and tested as new capability.
- Do not include the unrelated untracked docs files `slide2_context.md` or `slide4_actors_functions.pptx` in commits.
- No deployment, push, PR, or external message is part of this plan unless separately authorized.

## Acceptance criteria

1. Provider onboarding requires the Provider Manager to choose `INSPECTION`, `MAINTENANCE`, or both.
2. Shared provider legal identity is collected once; capability-specific evidence is collected and stored separately.
3. Inspection evidence supports the declared inspection scope, including applicable drone registrations, qualified pilot credentials, and insurance. Mission-specific permits remain an MF2 concern and are not treated as provider capability approval.
4. Maintenance evidence supports the declared repair scope, qualified personnel, and applicable credentials/insurance. Inspection evidence cannot substitute for it.
5. The Platform Operator can decide each capability independently: verify, request additional information, or reject.
6. A provider verified for inspection but not maintenance can participate only in inspection eligibility gates; the inverse is also true.
7. Choosing both capabilities does not merge or bypass the two vetting decisions.
8. Every decision and evidence change is auditable and scoped to the Provider Organization.
9. No new “Maintenance Provider Manager” role is created; `PROVIDER_MANAGER` remains the existing canonical provider representative in the target model.
10. SRS, business-flow references, API/UI documentation, and Report 5 traceability are synchronized with the implementation status.

---

## Task 1: Reconcile the runtime role and provider-organization baseline

**Objective:** Establish the actual role, actor-zone, organization, and authorization baseline before adding provider capability data.

**Files to inspect/modify:**
- Inspect: `backend/src/main/java/com/smartdroneinspection/shared/auth/Roles.java`
- Inspect: `backend/src/main/java/com/smartdroneinspection/users/domain/enums/UserRole.java`
- Inspect: `backend/src/main/java/com/smartdroneinspection/users/domain/enums/ActorZone.java`
- Inspect: `backend/src/main/java/com/smartdroneinspection/users/domain/User.java`
- Inspect: `backend/src/main/resources/db/migration/V3__authentication.sql`
- Inspect: `docs/reports/report-3-software-requirement-specification/01-overall-description.md`
- Inspect: `docs/reports/report-3-software-requirement-specification/03-functional-requirements.md`
- Test: `backend/src/test/java/com/smartdroneinspection/users/RolePolicyTest.java`

**Steps:**

1. Write or extend a failing contract test that identifies the canonical role/zone mapping required for provider capability administration:
   - `PROVIDER_MANAGER` is the provider organization representative in the target contract.
   - `PLATFORM_OPERATOR` performs provider vetting.
   - `INSPECTOR` and `MAINTENANCE_ENGINEER` remain workforce roles, not organization-level vetting roles.
   - No `MAINTENANCE_PROVIDER_MANAGER` role is allowed.
2. Run the focused test and confirm it fails only because the current runtime role baseline has not been reconciled.
3. Inspect the current migration and user-role persistence before choosing the smallest compatibility approach. Do not rewrite an applied migration.
4. Implement only the role mapping needed by the accepted target contract, preserving existing data compatibility through a forward migration or explicit translation where required.
5. Run the focused role tests and the users module tests.

**Expected verification:** Existing role tests remain green; the new contract test proves the implementation does not introduce a separate maintenance manager role.

**Commit:** `feat: reconcile provider role baseline`

---

## Task 2: Define provider capability and vetting domain values

**Objective:** Create domain types for declared capabilities, independent vetting status, and evidence categories without coupling the domain to HTTP or Infrastructure.

**Files:**
- Create or modify under the owning provider capability module, selected after Task 1:
  - `backend/src/main/java/com/smartdroneinspection/<provider-module>/domain/enums/ProviderCapability.java`
  - `backend/src/main/java/com/smartdroneinspection/<provider-module>/domain/enums/CapabilityVettingStatus.java`
  - `backend/src/main/java/com/smartdroneinspection/<provider-module>/domain/enums/ProviderEvidenceType.java`
  - `backend/src/main/java/com/smartdroneinspection/<provider-module>/domain/ProviderOrganization.java`
  - `backend/src/main/java/com/smartdroneinspection/<provider-module>/domain/ProviderCapabilityVetting.java`
  - `backend/src/main/java/com/smartdroneinspection/<provider-module>/domain/ProviderEvidence.java`
- Test: `backend/src/test/java/com/smartdroneinspection/<provider-module>/ProviderCapabilityDomainTest.java`

**Design constraints:**

- Use capability values `INSPECTION` and `MAINTENANCE`; the UI’s “both” option creates two capability records, not a third persisted capability.
- Use explicit states such as `PENDING`, `ADDITIONAL_INFO_REQUIRED`, `VERIFIED`, and `REJECTED`.
- A provider may have at most one current vetting record per capability, with history preserved through decision/audit records or immutable revisions.
- Model shared organization identity independently from capability-specific evidence.
- Keep evidence metadata free of passwords, API keys, tokens, or other secrets. Store only authorized object references and verification metadata.
- Make status transitions explicit; reject an update that would silently mark the other capability verified.

**TDD cycle:**

1. Add failing tests for inspection-only, maintenance-only, and both-capabilities declarations.
2. Add a failing test proving one capability can be `VERIFIED` while the other is `ADDITIONAL_INFO_REQUIRED`.
3. Add a failing test rejecting duplicate/current capability records or invalid status transitions.
4. Implement the minimal domain model and invariants.
5. Run the focused domain tests and refactor only after green.

**Commit:** `feat: add provider capability vetting domain`

---

## Task 3: Add the forward database migration and persistence mappings

**Objective:** Persist provider identity, declared capabilities, capability-specific evidence, independent decisions, and audit history with database constraints.

**Files:**
- Create: `backend/src/main/resources/db/migration/V12__provider_capability_vetting.sql` (use the next verified migration number if the repository has advanced)
- Create or modify persistence mappings under the selected provider module:
  - `.../domain/ProviderOrganization.java`
  - `.../domain/ProviderCapabilityVetting.java`
  - `.../domain/ProviderEvidence.java`
  - `.../repository/ProviderOrganizationRepository.java`
  - `.../repository/ProviderCapabilityVettingRepository.java`
  - `.../repository/ProviderEvidenceRepository.java`
- Test:
  - `backend/src/test/java/com/smartdroneinspection/database/FullDatabaseSchemaMigrationTest.java`
  - `backend/src/test/java/com/smartdroneinspection/database/PersistenceEntityMappingTest.java`
  - New provider schema contract test under `backend/src/test/java/com/smartdroneinspection/<provider-module>/`

**Migration requirements:**

- Use a new forward migration; never rewrite `V1`–`V11`.
- Define foreign keys to the existing organization/user tables with explicit delete behavior.
- Add a unique constraint for `(provider_organization_id, capability)` on the current capability record.
- Constrain capability and status values at the database layer.
- Store evidence category, object reference, checksum/metadata where the existing storage contract supports it, submitted/verified timestamps, and the deciding operator.
- Add indexes for provider organization, capability/status, and decision time.
- Preserve historical decisions rather than overwriting audit history.
- Do not store raw uploaded documents in PostgreSQL if the project’s MinIO object-store contract is the established path.

**TDD/verification:**

1. Add schema contract assertions first for the unique capability pair, status checks, FK ownership, and audit columns.
2. Run the schema contract test against the current baseline and observe the expected failure.
3. Add the migration and mappings.
4. Run clean-database migration tests and persistence mapping tests.
5. Inspect generated/actual schema for constraints, indexes, and delete behavior.

**Commit:** `feat: persist provider capability vetting`

---

## Task 4: Implement provider onboarding and capability declaration API

**Objective:** Allow a Provider Manager to register/update the provider organization and declare inspection, maintenance, or both with capability-specific evidence metadata.

**Files:**
- Create under the selected provider module:
  - `.../api/ProviderOrganizationController.java`
  - `.../api/dto/request/ProviderOnboardingRequest.java`
  - `.../api/dto/request/ProviderCapabilityRequest.java`
  - `.../api/dto/request/ProviderEvidenceRequest.java`
  - `.../api/dto/response/ProviderOrganizationResponse.java`
  - `.../api/dto/response/ProviderCapabilityResponse.java`
  - `.../service/ProviderOnboardingService.java`
  - `.../service/ProviderCapabilityAuthorizationService.java`
- Modify only shared authorization wiring required by the endpoint.
- Tests:
  - New controller/service unit tests in the provider module.
  - New integration test under `backend/src/test/java/com/smartdroneinspection/<provider-module>/ProviderOnboardingApiIntegrationTest.java`.

**API behavior:**

- `POST /api/v1/provider-organizations` (or the repository’s established versioning/path convention) accepts shared identity plus a non-empty set of capabilities.
- `INSPECTION` requires inspection evidence fields; `MAINTENANCE` requires maintenance evidence fields; selecting both requires both evidence groups.
- Reject an empty capability set, unknown capability, duplicate capability, missing capability-specific evidence, or cross-organization update.
- Return `ApiResponse<T>` for JSON success and RFC 9457 `ProblemDetail` for validation/authorization errors.
- Enforce that only the authenticated `PROVIDER_MANAGER` for the owning organization can edit its onboarding data.
- Do not allow a Provider Manager to approve its own capability; submission leaves decisions pending.
- Keep the endpoint separate from mission-specific airspace/permit clearance.

**TDD cycle:**

1. Add failing API tests for inspection-only, maintenance-only, and both.
2. Add failing tests for missing evidence, empty capabilities, duplicate capabilities, and unauthorized organization access.
3. Add the minimum service/controller implementation.
4. Verify response shape, status codes, authorization, and persisted rows.
5. Run the provider API slice and all users/auth regression tests.

**Commit:** `feat: add provider capability onboarding api`

---

## Task 5: Implement Platform Operator vetting and independent decisions

**Objective:** Let the Platform Operator review evidence and decide each capability independently.

**Files:**
- Create:
  - `.../api/ProviderVettingController.java`
  - `.../api/dto/request/CapabilityVettingDecisionRequest.java`
  - `.../api/dto/response/CapabilityVettingDecisionResponse.java`
  - `.../service/ProviderVettingService.java`
  - `.../service/ProviderEligibilityService.java`
- Modify authorization/configuration only as required by the existing access-policy pattern.
- Tests:
  - `ProviderVettingServiceTest.java`
  - `ProviderVettingApiIntegrationTest.java`
  - Extend provider authorization/organization-scope tests.

**API behavior:**

- `GET /api/v1/provider-organizations/{id}/vetting` returns both capability records and their current statuses.
- `POST /api/v1/provider-organizations/{id}/capabilities/{capability}/decision` accepts `VERIFIED`, `ADDITIONAL_INFO_REQUIRED`, or `REJECTED` plus a required reason/evidence note where applicable.
- Only `PLATFORM_OPERATOR` can decide; `PLATFORM_ADMIN` cannot perform business vetting unless the approved authorization contract explicitly says otherwise.
- Decision for `INSPECTION` must not change `MAINTENANCE`, and vice versa.
- A provider is eligible for inspection only when inspection capability is `VERIFIED`; maintenance eligibility requires maintenance capability `VERIFIED`.
- Record deciding operator, timestamp, reason, prior status, and audit event.
- Reject decisions against another tenant/provider organization and reject decisions on undeclared capabilities.

**TDD cycle:**

1. Add a failing test verifying inspection approval leaves maintenance pending.
2. Add a failing test verifying maintenance rejection does not revoke inspection approval.
3. Add failing tests for unauthorized roles, missing reasons, undeclared capabilities, and invalid transitions.
4. Implement the minimum service and controller behavior.
5. Run integration tests against a clean database and verify audit history.

**Commit:** `feat: add independent provider vetting decisions`

---

## Task 6: Enforce capability eligibility in inspection and maintenance flows

**Objective:** Prevent a provider from quoting, receiving assignments, or creating orders for a capability that has not been independently verified.

**Files:**
- Inspect and modify the existing inspection flow:
  - `backend/src/main/java/com/smartdroneinspection/inspectionrequests/...`
  - `backend/src/test/java/com/smartdroneinspection/inspectionrequests/InspectionQuotationTest.java`
  - `backend/src/test/java/com/smartdroneinspection/inspectionrequests/InspectionAssignmentTest.java`
- Inspect and modify the existing maintenance flow:
  - `backend/src/main/java/com/smartdroneinspection/maintenance/...`
  - `backend/src/test/java/com/smartdroneinspection/maintenance/...`
- Add or modify a named provider eligibility facade/API exposed according to Spring Modulith rules; do not import another module’s HTTP controller.

**Behavior:**

- Inspection quotation/assignment paths require verified inspection capability.
- Maintenance quotation/order/assignment paths require verified maintenance capability.
- A provider with both capabilities verified may use both flows; one verified capability must not unlock the other.
- Preserve existing organization, ownership, assignment, and separation-of-duties checks.
- Return the project’s established domain/API error for an ineligible provider; do not silently hide the provider or fall through to an unrelated error.

**TDD cycle:**

1. Add red tests for inspection-only, maintenance-only, both-verified, and neither-verified providers in both relevant flow modules.
2. Run the focused tests and confirm the missing eligibility gate.
3. Add the smallest cross-module eligibility contract and implementation.
4. Run all quotation, order, and assignment tests plus Modulith architecture tests.
5. Review dependency direction to ensure business modules do not import Infrastructure or another module’s HTTP API.

**Commit:** `feat: enforce capability-specific provider eligibility`

---

## Task 7: Add Platform Operator vetting UI and Provider Manager onboarding UI

**Objective:** Expose the capability choice and separate decision states in the React application without changing role names.

**Files:**
- Inspect: `frontend/src/app/permissions/accessPolicy.ts`
- Inspect: `frontend/src/app/router/router.tsx`
- Create or modify:
  - `frontend/src/features/providers/api/providerVettingApi.ts`
  - `frontend/src/features/providers/types/providerVetting.ts`
  - `frontend/src/features/providers/components/CapabilitySelector.tsx`
  - `frontend/src/features/providers/components/CapabilityEvidenceForm.tsx`
  - `frontend/src/features/providers/components/CapabilityStatusChip.tsx`
  - `frontend/src/features/providers/pages/ProviderOnboardingPage.tsx`
  - `frontend/src/features/providers/pages/ProviderVettingPage.tsx`
  - `frontend/src/features/providers/pages/*.test.tsx`
  - `frontend/src/app/router/router.tsx` (route only if needed)
  - `frontend/src/app/permissions/accessPolicy.ts` (permissions only if needed)

**UI behavior:**

- Provider Manager sees a multi-select with exactly: Inspection, Maintenance, Both (implemented as two selected capabilities).
- Selecting both renders two independent evidence sections and two independent statuses.
- Platform Operator sees each capability as a separate review card with evidence, status, decision controls, and reason.
- The UI must clearly show “Inspection verified” and “Maintenance pending/rejected/etc.” independently.
- Client and workforce roles do not see provider-vetting administration screens.
- UI guards are not the authorization boundary; the backend remains authoritative.

**TDD cycle:**

1. Add failing component tests for capability selection and separate status rendering.
2. Add tests for missing evidence validation and capability-specific error responses.
3. Implement the minimal feature components and route permissions.
4. Run feature tests, `npm run lint`, and `npm run build`.

**Commit:** `feat: add provider capability vetting ui`

---

## Task 8: Synchronize documentation and Report 5 traceability

**Objective:** Bring all affected project documentation in line with the implemented behavior and record the executable acceptance evidence.

**Files:**
- Modify: `docs/project-reference/business-flows.md` (SF-02/SF-03 and provider eligibility language)
- Modify: `docs/reports/report-3-software-requirement-specification/01-overall-description.md`
- Modify: `docs/reports/report-3-software-requirement-specification/02-user-requirements.md`
- Modify: `docs/reports/report-3-software-requirement-specification/03-functional-requirements.md`
- Modify: `docs/reports/report-3-software-requirement-specification/00-record-of-changes.md`
- Modify: `docs/reports/report-5-test-report/01-test-cases/test-case-list.md`
- Modify: `docs/reports/report-5-test-report/03-features/feature-1.md` or `feature-2.md` according to the existing mapping
- Modify: `docs/reports/report-5-test-report/02-test-statistics/test-statistics.md`
- Modify: `docs/reports/report-5-test-report/00-cover/cover.md`
- Modify: `docs/reports/report-5-test-report/00-cover/record-of-changes.md`

**Documentation requirements:**

- Keep the six-role model and `PROVIDER_MANAGER`; do not add a maintenance manager role.
- Describe `INSPECTION`, `MAINTENANCE`, and both as capability selection, not roles.
- Document independent vetting states and eligibility gates.
- Add stable test IDs and WF/FE mapping without renaming existing Report 5 cases or sheets.
- Record real test outcomes only. Unexecuted cases remain `Pending`, never `Passed`.
- If the implementation changes API/schema contracts, update the owning API/data documentation as required by `AGENTS.md`.

**Commit:** `docs: record provider capability vetting behavior`

---

## Task 9: Full verification and handoff

**Objective:** Verify the complete vertical slice and leave a reviewable, clean branch.

**Commands:**

```bash
# Backend, from /home/ubuntu/SmartDroneInspection/backend
./mvnw verify

# Frontend, from /home/ubuntu/SmartDroneInspection/frontend
npm run lint
npm run build

# Docs, from /home/ubuntu/SmartDroneInspection/docs
git diff --check
```

**Additional checks:**

- Run focused provider domain/API/persistence tests before the full suites.
- Run clean-database migration tests and inspect constraints/indexes.
- Run Spring Modulith architecture tests.
- Run frontend provider feature tests.
- Verify the final diff contains only intended files and no secrets, generated files, or the unrelated slide files.
- Verify branch/status in all affected repositories with `git status --short --branch`.
- If Hugo is installed, run the docs build; if unavailable, report that limitation explicitly.
- Do not claim deployment or runtime availability unless a separately authorized deployment and endpoint check is performed.

**Final report must include:** changed files, exact verification commands/results, role-model preservation, documentation impact, remaining target-vs-implemented limitations, and any pending Report 5 cases.

---

## Risks, tradeoffs, and open questions

- **Role mismatch:** The docs target model uses `PLATFORM_OPERATOR`/`PROVIDER_MANAGER`, while the current backend migration and constants use legacy names. This must be resolved deliberately before implementation; a silent rename risks breaking existing authentication data.
- **Provider organization ownership:** The current user model has a nullable `organization_id`, but the organization table is generic. Confirm whether provider organization identity belongs in the existing `organizations` table or requires a provider-specific subtype/ownership field before migration.
- **Evidence storage:** The existing MinIO adapter is inspections-owned. Decide whether provider documents need a shared storage port or a provider-owned port; do not import Infrastructure directly into the provider module.
- **Capability records versus role assignments:** Capabilities must remain organization eligibility data, not user roles. Do not add capability values to `UserRole`.
- **Existing flow readiness:** Inspection and maintenance quotation/assignment paths may not yet have provider organizations in their data model. Gate enforcement may require a compatibility bridge first; do not invent provider IDs or bypass current ownership checks.
- **SRS status:** The SRS update exists, but implementation is not yet verified. After implementation, update wording from target-only to implemented only where tests and runtime evidence support it.
- **Report 5 scope:** This is a new cross-cutting behavior. Use the existing fixed workbook mapping and preserve pending status for cases not executed.
- **Legal evidence:** “Applicable” credentials must remain configurable and reviewed; the system should not hard-code legal conclusions beyond the accepted requirements.
