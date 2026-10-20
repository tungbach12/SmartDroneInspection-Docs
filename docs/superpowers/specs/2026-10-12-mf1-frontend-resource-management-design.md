# MF1 Frontend Resource Management Design

**Status:** Draft for user review — conversational design approved; this written specification still awaits review  
**Date:** 12 October 2026  
**Repositories:** SmartDroneInspection-Frontend (`hieu`), SmartDroneInspection-Backend (`hieu`), SmartDroneInspection-Docs (`hieu`)  
**Scope:** Frontend flows for MF1-02–MF1-07, consuming the already-implemented backend APIs. This design does not claim that the Frontend is implemented.

## 1. Purpose and success criteria

Deliver a usable Frontend for the MF1 resource-management capabilities already available in the backend: organization workforce provisioning, workforce credential records and internal review, Drone inventory and documents, and organization-recorded flight permits/compliance inputs.

Success means:

- An `ORG_ADMIN` can perform the supported MF1 workflows from the browser without supplying or selecting another organization.
- `ADMIN`, `INSPECTOR`, and `MAINTENANCE_ENGINEER` do not see or enter these customer resource-management screens.
- The Frontend uses the existing backend contract and the shared Axios/TanStack Query patterns, displays actionable loading/empty/error/success states, and does not invent backend capabilities.
- A temporary password is displayed only in the successful provisioning response and is never placed in browser storage or query cache.
- Credential/permit review is described as an internal customer decision, never as government or authority verification.

Out of scope: MF1-01 workspace/company profile, MF1-08–14 asset pairing and inspection setup, subscription activation/renewal UI, new backend endpoints, mobile UI, and any external authority/registry integration.

## 2. Role and navigation model

MF1 administration belongs to the `ORG_ADMIN` client workspace. The Frontend adds two top-level client-portal entries:

1. **Workforce** at `/client/workforce`, with tabs/routes for `Users` and `Credentials`.
2. **Assets** remains at `/client/assets` and gains resource tabs/routes for `Assets`, `Drones`, and `Permits`.

Only `ORG_ADMIN` sees and can route to the new Workforce and resource-management UI. `ADMIN` retains its platform workspace and does not receive customer technical/resource authority. `INSPECTOR` and `MAINTENANCE_ENGINEER` retain their Operations workspace and assigned-work capabilities, but receive no MF1 resource-management actions. These Frontend guards are navigation UX only; backend authorization remains authoritative.

Use the existing central `app/permissions/accessPolicy.ts`, `AppShell` navigation composition, router guards, and `RequireAuth` conventions. Do not create another role map or a parallel shell.

## 3. Feature ownership and data flow

### 3.1 Workforce feature

Add a focused `features/workforce` feature for workforce API clients, typed DTOs, query keys/hooks, and pages/components. It owns:

- `Users`: list, provision, update member status, update member roles.
- `Credentials`: list, create, and record an internal review decision.

Use the shared Axios instance, which unwraps the existing success envelope, and TanStack Query for all server state. Keep form/modal state local. Mutations invalidate the relevant workforce list/detail query keys. Do not put server responses in Zustand.

### 3.2 Assets feature

Keep Drone and permit flows under the existing `features/assets` owner; add only the API/types/hooks/pages/components needed for these concrete screens:

- Drone list, create, detail, and serviceability update.
- Drone document list, multipart upload, and status update within the Drone detail view.
- Flight permit list, create, and internal review.

Use query keys and mutations local to the assets feature. The existing asset CRUD/documents flows remain unchanged except for shared navigation composition where needed.

### 3.3 Organization scope

The Frontend must not send an `organizationId` to widen scope. The backend derives scope from the authenticated `ORG_ADMIN`. List endpoints return only that organization’s records. For the workforce create DTO, the `roles` input is restricted in the UI to `INSPECTOR` and `MAINTENANCE_ENGINEER`; the backend remains the enforcement boundary.

## 4. Existing backend contracts

All URLs below are relative to the shared `/api/v1` client base.

### Workforce users

- `POST /workforce/users` — `{ email, fullName, roles }`; returns `{ user, temporaryPassword }` once.
- `GET /workforce/users` — organization-scoped member list.
- `PATCH /workforce/users/{userId}/status` — status update.
- `PUT /workforce/users/{userId}/roles` — role update, limited to Inspector/Engineer roles.

Provisioning success must show the temporary password in a one-time result surface with copy and acknowledgement controls. Do not write it into `localStorage`, `sessionStorage`, Zustand persistence, or query cache. When the result surface closes, clear its local state. The UI must not promise that email delivery occurred.

### Workforce credentials

- `POST /workforce/credentials` — `{ userId, credentialType, issuer?, credentialReference?, issuedAt?, expiresAt?, evidenceId? }`.
- `GET /workforce/credentials` — organization-scoped credential list.
- `PUT /workforce/credentials/{credentialId}/review` — `{ decision: APPROVE | REJECT, reason }`.

`issuedAt`/`expiresAt` are ISO-8601 instants. The UI may select an organization workforce subject from the users list. The backend accepts only an `evidenceId`; it does not currently provide an evidence search/picker or a credential-evidence upload route. Therefore `evidenceId` is an optional reference field in this slice; do not fabricate a picker or upload workflow. Credential state shows the backend-derived expiry warning. The configured 60-day horizon is a product default, overridable per deployment; it is not a statutory renewal interval. Reviews are internal human decisions and do not represent government verification.

### Drone inventory and documents

- `POST /drones` — `{ serialNumber, model?, manufacturer?, payloadMetadata?, notes? }`.
- `GET /drones` — organization-scoped Drone list.
- `GET /drones/{droneId}` — organization-scoped detail.
- `GET /drones/selection` — only same-organization serviceability `ACTIVE` Drones; this is not a permit/readiness assertion.
- `PATCH /drones/{droneId}/serviceability` — `{ serviceability }`.
- `POST /drones/{droneId}/documents` — multipart file and metadata fields.
- `GET /drones/{droneId}/documents` — documents for the authorized Drone.
- `PATCH /drones/{droneId}/documents/{documentId}/status` — `{ status }`.

`payloadMetadata` is a JSON string on the request contract; the UI should use a typed JSON editor or structured key/value form and serialize to valid JSON. Do not imply that Drone `ACTIVE` serviceability means legally cleared to fly. Document upload accepts the finite backend content-type allowlist and the configured 10 MB application cap; multipart infrastructure limits may be stricter, so surface server 413 errors. Checksum is server-derived and is not a user-editable field. Status expiry is derived for display; review status and derived expiry status should be labelled distinctly where both matter.

### Flight permits/compliance

- `POST /flight-permits` — `{ permitType, assetId?, areaReference?, issuingAuthority?, permitReference?, geographicScope?, validFrom?, validUntil?, conditions?, status?, sourceEvidenceId? }`.
- `GET /flight-permits` — organization-scoped list.
- `PUT /flight-permits/{permitId}/review` — `{ status, reason }`.

`geographicScope` and `conditions` are JSON strings in the current request contract; serialize valid JSON documents. `assetId` and `sourceEvidenceId` are optional references, but no asset/evidence picker is currently specified for this FE slice; use optional ID fields, not fabricated resource discovery. The displayed statuses are organization-recorded (`APPLICATION`, `ACTIVE`, `EXPIRED`, `REJECTED`, `REVOKED`, `NOT_APPLICABLE`). The application and all explanatory copy must say these are what the organization records. No label, icon, status or helper text may imply registry, government, authority verification, legal clearance, or permission to fly.

## 5. Forms, errors, and interaction states

Use the existing MUI theme and shared UI components (`PageHeader`, `DataTable`, `EmptyState`, `QueryState`, `StatusChip`, toast/error helpers). Use React Hook Form/Zod for non-trivial forms where it matches existing feature conventions; do not add a new dependency.

Every query view has loading, error/retry, empty and success states. Every mutation disables duplicate submission while pending, maps RFC 9457 responses through existing shared error helpers, and invalidates relevant query keys after success.

Expected cases:

- `400 VALIDATION_FAILED`: show field/form validation feedback and preserve the user’s non-secret draft.
- `403` / `SUBSCRIPTION_INACTIVE`: explain that the organization’s subscription blocks writes; reads remain available.
- `404` for foreign/missing references: show a generic “not found or unavailable in this organization” message; do not attempt an unscoped follow-up lookup.
- `409 EMAIL_ALREADY_EXISTS` for a duplicate inside the current organization: ask the ORG_ADMIN to choose another address or inspect the organization’s list. A foreign email also returns generic `404`, so the UI must not say whether that address is registered elsewhere.
- `413 PAYLOAD_TOO_LARGE` and unsupported media type: show the server’s actionable upload message and preserve safe form fields; do not retain file bytes after completion/close.
- Network/5xx: show retry for idempotent reads only. Do not automatically retry provisioning, upload, or status/review mutations.

## 6. Acceptance criteria by role

### ORG_ADMIN

- Can navigate to Workforce and Assets resource tabs.
- Can provision a workforce member with only allowed roles; sees a one-time temporary-password result; cannot retrieve the password later from the list.
- Can list users, change status/roles, create/list credentials, and record approve/reject decisions with a reason.
- Can create/list/read/update Drone serviceability, upload/list/update Drone documents, and create/list/review permits.
- Sees only records belonging to their organization. Foreign references produce generic unavailable/not-found feedback.
- Sees expiry warnings without any claim of external verification.

### ADMIN

- Does not see or route into ORG_ADMIN customer technical/resource management UI.
- Retains existing platform pages. The current backend has several GET controller annotations that include ADMIN while their service requires an organization scope; this FE design deliberately does not depend on those routes. Any platform-wide read requirement needs a separate backend authorization decision and must not be inferred from the annotation alone.

### INSPECTOR

- Does not see Workforce or customer resource-management tabs/routes.
- Existing assigned inspection/evidence/report behavior remains unchanged.

### MAINTENANCE_ENGINEER

- Does not see Workforce or customer resource-management tabs/routes.
- Existing maintenance behavior remains unchanged.

## 7. Test plan

- Access-policy unit tests assert MF1 sections visible to ORG_ADMIN and absent for ADMIN/INSPECTOR/MAINTENANCE_ENGINEER in this customer-resource workflow.
- Router tests assert direct unauthorized navigation resolves to the existing forbidden/redirect behavior.
- API unit tests assert typed URL/body/multipart encoding and response mapping; no caller-supplied organization is sent.
- Component/integration tests cover loading, empty, error, mutation success/failure, role-gated actions, one-time temporary-password cleanup, expiry labels, and no-external-verification copy.
- Build check: `npm run build`.
- Lint check: `npm run lint` (the current Windows environment may block oxlint’s native binding; if so, record that exact blocker rather than claiming lint passed).
- Test check: `npm test -- --run` (if this environment’s worker startup causes timeout, rerun with bounded Vitest workers and record the exact command).

## 8. Boundaries and non-goals

- No changes to Backend endpoints or database schema are part of this Frontend spec.
- No UI for MF1-01 workspace/company identity, MF1-08–14 asset pair/inspection setup, subscription activation/renewal, or mobile MF1.
- No permit authority lookup, no government-verification claim, no legal-flight-clearance calculation.
- No evidence upload/picker for credential `evidenceId` or permit `sourceEvidenceId` until a suitable backend contract exists.
- No platform ADMIN cross-tenant read UI for MF1 resources until backend service scoping is explicitly designed.
- Do not push, open PR, or merge without explicit authorization.
