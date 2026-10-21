# MF1 Frontend Resource Management Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Deliver the ORG_ADMIN-only Frontend workflows for MF1-02–MF1-07 workforce, credential, Drone/document, and permit management using the existing backend contracts.

**Architecture:** Add a focused `features/workforce` feature for users and credentials; extend the existing `features/assets` feature for Drones, Drone documents, and permits. Compose two ORG_ADMIN-only client workspace sections in the existing route/access policy and shared shell. Use the shared Axios client and TanStack Query; do not create new state infrastructure or alter backend contracts.

**Tech Stack:** React 19, strict TypeScript, Vite, Material UI, React Router, TanStack Query, existing shared Axios client and UI helpers, Vitest and React Testing Library.

**Spec:** `docs/superpowers/specs/2026-10-12-mf1-frontend-resource-management-design.md`

## Global Constraints

- Only `ORG_ADMIN` sees MF1 resource-management routes and actions; frontend guards are UX only and backend authorization remains authoritative.
- Do not send `organizationId`; the backend derives tenant scope from the authenticated principal.
- Use the shared Axios client and TanStack Query for server state; do not persist server data or secrets in Zustand/browser storage.
- Display a provisioning temporary password once in local component state, clear it when the result surface closes, and never cache it.
- Credential/permit review is internal customer review, not government/authority verification; Drone `ACTIVE` is not legal flight clearance.
- Do not invent backend endpoints, evidence pickers/uploads, subscription activation, or ADMIN cross-tenant resource reads.
- Preserve existing API payloads and shared error handling; no new dependencies or backend/schema changes.
- Keep the test report and frontend behavior in sync; do not mark tests passed until executed.

## Review Focus

1. **Temporary password lifetime:** provisioning result renders once, never enters query cache/storage, and is cleared on close/unmount.
2. **Cross-tenant IDs:** user/evidence/asset/drone/permit IDs supplied in forms must not trigger an unscoped follow-up lookup; show generic unavailable/not-found errors.
3. **Malformed JSONB fields:** metadata/scope/conditions must be serialized as valid JSON and validation failures remain actionable 400s.
4. **Multipart limits/content types:** oversized or unsupported files must show server errors; the app cap may differ from the servlet multipart cap.
5. **Review semantics:** approve/reject and permit statuses must be described as internal/customer-recorded, never externally verified or cleared to fly.

---

## File Structure

| File | Responsibility |
|---|---|
| `src/app/permissions/accessPolicy.ts` | Add client-only Workforce section and exact section labels/role allowlist. |
| `src/app/permissions/accessPolicy.test.ts` | Assert Workforce visible to ORG_ADMIN and denied to the other three roles. |
| `src/app/layouts/AppShell.tsx` | Add the Workforce navigation entry using the existing shell. |
| `src/app/router/router.tsx` | Lazy-load the new Workforce page under existing portal guard model. |
| `src/features/workforce/api/workforceApi.ts` | Typed users/credentials contracts, URLs, and query-key factories. |
| `src/features/workforce/hooks/useWorkforce.ts` | Query/mutation hooks and invalidation/toast handling. |
| `src/features/workforce/pages/WorkforcePage.tsx` | Users/Credentials tabs and list state. |
| `src/features/workforce/components/` | Focused create/edit/review dialogs and one-time password result; create only components with multiple responsibilities worth isolating. |
| `src/features/assets/api/droneApi.ts` | Typed Drone and Drone document contracts/query keys. |
| `src/features/assets/api/permitApi.ts` | Typed permit contracts/query keys. |
| `src/features/assets/hooks/useDrones.ts` | Drone/document query and mutation hooks. |
| `src/features/assets/hooks/useFlightPermits.ts` | Permit list/create/review hooks. |
| `src/features/assets/pages/AssetsPage.tsx` or a sibling client resource page | Add client-only Drone/Permit tabs while preserving current asset page and ADMIN behavior. Choose after reading current composition; avoid a duplicate assets feature. |
| Relevant `*.test.ts(x)` alongside APIs, hooks, policy, and pages | Behavioral tests for contract, role and UI acceptance. |

## Task 1: Establish MF1 route policy and Workforce entry shell

**Files:**
- Modify: `src/app/permissions/accessPolicy.ts`
- Modify: `src/app/permissions/accessPolicy.test.ts`
- Modify: `src/app/layouts/AppShell.tsx`
- Modify: `src/app/router/router.tsx`
- Test: existing policy/router test files

**Interfaces:**
- Consumes: current `PortalId`, `SectionId`, `SECTION_ROLE_ACCESS`, `PORTAL_CONFIG`, `getSectionPath`, and `RequireAuth` patterns.
- Produces: a client-only `workforce` section and route path `/client/workforce`; `ADMIN`, `INSPECTOR`, and `MAINTENANCE_ENGINEER` must not access it.

- [ ] **Step 1: Write failing access-policy tests** for `ORG_ADMIN` access and denial for the other three roles, plus multi-role users whose additional non-ORG_ADMIN role does not grant the Workforce route.
- [ ] **Step 2: Run the policy test** with `npm test -- --run src/app/permissions/accessPolicy.test.ts`; expect new assertions to fail because `workforce` is not a section.
- [ ] **Step 3: Add the Workforce section and label** to the central policy and add a shell navigation item; do not add a second role map.
- [ ] **Step 4: Add a lazy Workforce route** under `/client`, guarded by the existing section role lookup; preserve all current paths and portal entry behavior.
- [ ] **Step 5: Run policy/router tests** and confirm `ORG_ADMIN` succeeds while `ADMIN`, `INSPECTOR`, and `MAINTENANCE_ENGINEER` route to the existing forbidden behavior.
- [ ] **Step 6: Commit** as `feat(workforce): add org admin workforce route`.

## Task 2: Workforce users API, hooks, and list/provision UI

**Files:**
- Create: `src/features/workforce/api/workforceApi.ts`
- Create: `src/features/workforce/hooks/useWorkforce.ts`
- Create: `src/features/workforce/pages/WorkforcePage.tsx`
- Create: `src/features/workforce/components/ProvisionWorkforceUserDialog.tsx`
- Create: `src/features/workforce/components/TemporaryPasswordDialog.tsx`
- Test: corresponding API, hook, and component tests

**Interfaces:**
- Consumes: shared `api`, `getErrorMessage`, `PageHeader`, `DataTable`, `QueryState`, `EmptyState`, `useToastStore`, and Task 1 route.
- Produces: `workforceApi.listUsers(): Promise<WorkforceUser[]>`, `workforceApi.provisionUser(input): Promise<ProvisionedWorkforceUser>`, `workforceApi.updateUserStatus(userId,input)`, `workforceApi.updateUserRoles(userId,input)`; query keys rooted at `['workforce']`.

- [ ] **Step 1: Write failing API tests** asserting exact backend paths and payloads for list, provision, status, and role update. Assert no payload includes `organizationId`.
- [ ] **Step 2: Run the API tests** and observe missing API exports/expected request calls.
- [ ] **Step 3: Implement typed API interfaces** from backend DTOs: user fields `userId,email,fullName,roles,status,organizationId`; provisioning response `{ user, temporaryPassword }`; accepted roles exactly `INSPECTOR | MAINTENANCE_ENGINEER`.
- [ ] **Step 4: Write failing hook tests** for list query, successful create invalidation, status/role mutation invalidation, and failed mutation error preservation.
- [ ] **Step 5: Implement hooks** using TanStack Query and existing toast/error conventions; do not cache the one-time password in a query.
- [ ] **Step 6: Write failing component tests** for loading, error/retry, empty, list, create form role options, and temporary-password one-time display/clear-on-close.
- [ ] **Step 7: Implement Users UI** using MUI and existing page/table/dialog patterns. Provision form validates email, name, and at least one allowed role; on success pass password only through local dialog state and clear on close/unmount.
- [ ] **Step 8: Run Workforce API/hooks/page tests** and confirm all states and password-lifetime assertions.
- [ ] **Step 9: Commit** as `feat(workforce): add org admin user management`.

## Task 3: Workforce credential list/create/internal-review UI

**Files:**
- Modify: `src/features/workforce/api/workforceApi.ts`
- Modify: `src/features/workforce/hooks/useWorkforce.ts`
- Create: `src/features/workforce/components/CreateCredentialDialog.tsx`
- Create: `src/features/workforce/components/ReviewCredentialDialog.tsx`
- Modify: `src/features/workforce/pages/WorkforcePage.tsx`
- Test: credential API/hooks/dialog/page tests

**Interfaces:**
- Consumes: Task 2 user list/API and query keys.
- Produces: `workforceApi.listCredentials(): Promise<WorkforceCredential[]>`, `createCredential(input)`, `reviewCredential(id,input)`; credential fields match backend response and status vocabulary.

- [ ] **Step 1: Write failing API contract tests** for `GET/POST /workforce/credentials` and `PUT /workforce/credentials/{credentialId}/review`; assert date fields serialize as ISO instants, `evidenceId` is optional, and organization is never sent.
- [ ] **Step 2: Run tests and observe RED** for missing methods.
- [ ] **Step 3: Implement typed API methods and hooks**; invalidate credentials and workforce list where subject status affects display.
- [ ] **Step 4: Write failing UI tests** for subject selection from same-org user list, optional evidence ID input, date order feedback, expiry status display, approve/reject reason, and no external-verification language.
- [ ] **Step 5: Implement credential tab**. Use existing workforce users query for subjects. Do not add an evidence picker/upload flow. Render `EXPIRING_SOON`, `EXPIRED`, `REJECTED`, and `SUSPENDED` distinctly and describe status as recorded/internal.
- [ ] **Step 6: Run credential-focused tests** and verify no password or access token is rendered/cached.
- [ ] **Step 7: Commit** as `feat(workforce): add credential records and review UI`.

## Task 4: Drone inventory, serviceability, and Drone documents

**Files:**
- Create: `src/features/assets/api/droneApi.ts`
- Create: `src/features/assets/hooks/useDrones.ts`
- Create: Drone list/create/detail UI components/pages under `src/features/assets/`
- Test: Drone API/hook/list/document component tests

**Interfaces:**
- Consumes: existing asset feature UI/shared helpers and Task 1/2 role navigation patterns.
- Produces: `droneApi.list(): Promise<Drone[]>`, `getById(id)`, `create(input)`, `updateServiceability(id,input)`, `listDocuments(id)`, `uploadDocument(id,formData)`, `updateDocumentStatus(droneId,documentId,input)`.

- [ ] **Step 1: Write failing API tests** for all Drone/document URLs, typed request bodies, JSON-string `payloadMetadata`, multipart upload field names, and no organization parameter.
- [ ] **Step 2: Run API tests and observe RED** for the missing Drone API module.
- [ ] **Step 3: Implement typed API functions and query-key factories**. For multipart, pass `FormData` through the shared Axios client without manually setting a JSON content type.
- [ ] **Step 4: Write failing component tests** for ORG_ADMIN-only create/serviceability/upload controls, list/detail loading/empty/error states, supported file selection, 413/415 display, expired-document display, and the fact that ACTIVE serviceability is not shown as flight clearance.
- [ ] **Step 5: Implement the Drone tab** in the client Assets resource view. Keep create fields aligned to the backend DTO and serialize payload metadata as a valid JSON string.
- [ ] **Step 6: Implement Drone detail/document UI** with upload/list/status actions; never expose object keys as download URLs or add a client checksum field.
- [ ] **Step 7: Run API, component, asset regression and access-policy tests**.
- [ ] **Step 8: Commit** as `feat(assets): add org admin drone management UI`.

## Task 5: Permit list/create/internal-review UI

**Files:**
- Create: `src/features/assets/api/permitApi.ts` or add permit types/functions to `droneApi.ts` only if the existing assets API module remains cohesive after inspection
- Create: `src/features/assets/hooks/useFlightPermits.ts`
- Create: Permit form/list/review components under `src/features/assets/`
- Test: permit API/hooks/form/list tests

**Interfaces:**
- Consumes: existing shared API/error/query patterns and Task 4’s client Assets resource navigation.
- Produces: `permitApi.list(): Promise<FlightPermit[]>`, `create(input)`, `review(permitId,input)`; statuses exactly `APPLICATION | ACTIVE | EXPIRED | REJECTED | REVOKED | NOT_APPLICABLE`.

- [ ] **Step 1: Write failing API tests** for exact GET/POST/PUT paths, JSON-string serialization of `geographicScope`/`conditions`, optional IDs, and absence of organization data.
- [ ] **Step 2: Run tests and observe RED** for missing API functions.
- [ ] **Step 3: Implement API/query hooks** with list invalidation after create/review.
- [ ] **Step 4: Write failing UI tests** for the six recorded status values, date-order validation, malformed JSON feedback, same-org asset/evidence IDs remaining optional references, review reason, and explicit non-verification wording.
- [ ] **Step 5: Implement permit UI**. The copy must identify the status as the organization’s own record. Do not label ACTIVE “verified”, “approved by authority”, “legal”, or “cleared to fly”; do not infer flight readiness.
- [ ] **Step 6: Run permit tests and verify all role restrictions**.
- [ ] **Step 7: Commit** as `feat(assets): add org admin permit management UI`.

## Task 6: Integrated role/security regression, full validation, and documentation

**Files:**
- Modify: `src/app/permissions/accessPolicy.test.ts`, router tests, relevant feature tests
- Modify docs repository: Report 5 feature/statistics/cover sources and frontend architecture guide if navigation structure changed materially

**Interfaces:**
- Consumes: Workforce and Assets routes/components from Tasks 1–5.
- Produces: verified end-to-end FE role visibility and recorded frontend test results; no backend/API changes.

- [ ] **Step 1: Add or complete cross-role access tests** for all four roles: ORG_ADMIN sees both entries; ADMIN/INSPECTOR/MAINTENANCE_ENGINEER cannot render them by direct URL; existing role-specific MF2/MF3 pages remain accessible as before.
- [ ] **Step 2: Run focused route and feature tests** and fix regressions before full suite.
- [ ] **Step 3: Run `npm run build`** and confirm strict TypeScript/Vite build passes.
- [ ] **Step 4: Run `npm run lint`**. If Windows Application Control blocks the native oxlint binding, record the exact error as blocked; do not claim lint passed.
- [ ] **Step 5: Run `npm test -- --run`**; if the known worker startup causes timeouts, rerun with the supported bounded-worker command and record the exact command/results.
- [ ] **Step 6: Update Report 5 editable Markdown** with actual FE case procedures/results; preserve workbook sheet mapping and do not mark unexecuted backend/API assumptions passed.
- [ ] **Step 7: Run `git diff --check` in Frontend and Docs**, inspect staged changes, and commit Docs separately from Frontend.
- [ ] **Step 8: Commit Frontend** as `feat(mf1): add org admin resource management UI` and Docs as `docs(mf1): record frontend resource management coverage`.

## Verification Matrix

| Check | Command | Expected |
|---|---|---|
| Frontend type/build | `npm run build` | TypeScript and Vite build pass |
| Frontend lint | `npm run lint` | Pass, or recorded blocked due native binding policy |
| Frontend tests | `npm test -- --run` | All existing/new tests pass; exact counts recorded |
| Frontend whitespace | `git diff --check` | No whitespace errors |
| Docs whitespace | `git diff --check` in Docs repository | No whitespace errors |

## User Review Gate

This plan is presented for review only. Do not implement, commit, push, open a PR, or merge until the user explicitly approves this plan and chooses an execution method.
