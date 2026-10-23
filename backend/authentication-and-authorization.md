---
title: "Authentication and Access Control"
weight: 30
aliases:
  - /authentication/
  - /security/authentication/
---

# Authentication and Access Control

This document describes the deliberately small authentication surface for the current project. It is production-oriented without adding banking-grade ceremony that the product does not need.

## Identity and roles

Users are stored in PostgreSQL and authenticate with email and password. Email is normalized for lookup; passwords are never trimmed or stored in plain text.

Current roles (Enterprise SaaS target, 4 roles):

- `ADMIN` - platform tenant/subscription administration and global support.
- `ORG_ADMIN` - customer-organization administration, review, and acceptance.
- `INSPECTOR` - assigned inspections, field sessions, evidence, and assigned inspection report verification.
- `MAINTENANCE_ENGINEER` - assigned maintenance work and assigned maintenance report verification.

Users also have an actor zone:

- `PLATFORM`
- `CUSTOMER_ORGANIZATION`

Role checks are not sufficient by themselves. Services enforce organization scope, assignment scope, and separation of duties. For MF2, assignment response and field-session operations are restricted to the assigned active Inspector; preparation/source access and readiness decisions additionally enforce organization ownership, current workflow state, and independent reviewer rules. Internal credential/document verification and evidence-attribution checks do not verify an external issuer registry or determine statutory applicability.

## Browser flow

Browser endpoints are under `/api/v1/auth/**`:

| Endpoint | Purpose |
| --- | --- |
| `GET /csrf` | Obtain the CSRF token used by browser requests. |
| `POST /register` | Create an active ORG_ADMIN account and its new organization. |
| `POST /login` | Authenticate with email and password. |
| `POST /password/setup` | Complete an administrator-issued first-password setup. |
| `POST /refresh` | Rotate the browser refresh token. |
| `POST /logout` | Revoke the current session. |
| `POST /logout-all` | Revoke all sessions for the user. |
| `GET /me` | Return the current user and roles. |
| `POST /password/change` | Change the password and invalidate old sessions. |

The access token is returned in the login response and held in web memory only. The refresh token is an opaque `HttpOnly`, `Secure`, `SameSite=Strict` cookie scoped to the auth API. It is never written to `localStorage` or returned in JSON.

Browser auth uses CSRF protection and an exact CORS allowlist. Successful JSON API responses use `{ success, message, data }`; authentication payloads such as the CSRF token or auth flow are inside `data`. The shared browser/mobile HTTP clients unwrap this envelope. `204 No Content` responses remain bodyless. API errors use RFC 9457 Problem Details with a stable `code` and `traceId`; login failures use a generic message.

The SPA calls `GET /api/v1/auth/csrf` before each browser-auth POST and sends
the returned `token` using the returned `headerName`. Fetching the token again
after authentication or logout is required because Spring Security clears the
previous CSRF cookie during those transitions.

## Organization onboarding

The first organization representative (an `ORG_ADMIN`) may self-register a new organization through the browser-only `POST /api/v1/auth/register` endpoint. The request contains the representative's name and credentials together with the organization name/code and explicit acceptance of the active Terms of Service and Privacy Notice. The backend creates the organization and first user in one transaction, activates both immediately, and assigns only the `ORG_ADMIN` role in the `CUSTOMER_ORGANIZATION` actor zone. There is no email-verification or administrator-approval gate in v1.

Registration cannot create or select `ADMIN`, `INSPECTOR`, or `MAINTENANCE_ENGINEER`. Email and organization-code uniqueness, password policy, request rate limits, organization isolation, affirmative dual consent, and exact active policy-version checks are enforced by the backend. Missing/false acceptance or a stale policy version is rejected with HTTP 400 before tenant/user persistence. On success, the append-only `ORGANIZATION_REGISTRATION` audit event records the policy versions, acceptance flags, server UTC timestamp, IP address, and bounded user-agent in `safe_metadata`, in the same database transaction. This is application audit evidence, not a certified digital signature or a guarantee of legal enforceability. The registration response contains the created organization and user profile but no access or refresh token; the representative signs in through the normal login flow.

The browser registration request body is:

| Field | Meaning |
| --- | --- |
| `email` | Representative's login email. Lookup is case-insensitive. |
| `fullName` | Representative's display name. |
| `organizationName` | Name of the new customer organization. |
| `organizationCode` | Unique 3–64 character code using letters, numbers, `-`, or `_`; it is stored in uppercase. |
| `password` | A 15–128 Unicode-character password validated by the shared password policy. |
| `termsAccepted` | Required boolean; must be explicitly `true`. |
| `termsVersion` | Required Terms of Service version; must exactly match the server's active version (`2026.1`). |
| `privacyNoticeAccepted` | Required boolean; must be explicitly `true`. |
| `privacyNoticeVersion` | Required Privacy Notice version; must exactly match the server's active version (`2026.1`). |

Successful registration returns `201 Created` with the organization identifier/code and the new user profile. It does not issue tokens, set a refresh cookie, or expose the password.

The `data` payload is `{ organizationId, organizationName, organizationCode, user }`; `user` contains the new user's identifier, normalized email, name, role list (`ORG_ADMIN`), actor zone, and organization identifier. The complete success body is `{ success: true, message: "Success", data: { ... } }`.

## Platform user and subscription administration
Platform user management is under `/api/v1/platform/users/**` and requires `ADMIN`:
- `POST /api/v1/platform/users` creates a provisioned account.
- `POST /api/v1/platform/users/{userId}/reset-password` issues a new setup credential.
- `PUT /api/v1/platform/users/{userId}/roles` changes roles and revokes the user's sessions.
- `PATCH /api/v1/platform/users/{userId}/status` activates, suspends, or disables an account.

Subscription activation is a separate Platform ADMIN operation:
- `POST /api/v1/platform/organizations/{organizationId}/subscriptions` activates one ENTERPRISE subscription for an existing organization.
- The caller must be an active platform `ADMIN` with no organization scope. Organization Admins cannot self-activate; missing organizations are returned as not found.
- Supported billing periods are 1, 6, or 12 months. Activation records the confirming actor/time and an audit reason; a second currently active subscription is rejected with `409 SUBSCRIPTION_ALREADY_ACTIVE`.
- Subscription activation does not change organization-registration behavior. Newly registered workspaces remain unentitled until separately activated; entitled resource writes are gated while reads/history remain available.

## Tenant resource administration (MF1)

MF1 organization resources are managed by `ORG_ADMIN` only, under tenant-scoped
endpoints. `ADMIN` has no default customer-side authority over them.

- `/api/v1/workforce/users/**` — provision, list, and change status or roles for
  `INSPECTOR` and `MAINTENANCE_ENGINEER` accounts.
- `/api/v1/workforce/credentials/**` — record and internally review the documents an
  organization holds about its own workforce members.
- `/api/v1/drones/**` — tenant Drone inventory, serviceability, and Drone documents.

Authorization rules that hold across these endpoints:

- **Organization scope always comes from the authenticated actor**, never from the request
  body. A request-supplied organization is ignored.
- **Only `INSPECTOR` and `MAINTENANCE_ENGINEER` are grantable** through the workforce API.
  The public users facade independently enforces this allowlist, so a direct facade call
  cannot promote a user to `ORG_ADMIN`/`ADMIN` or alter a peer `ORG_ADMIN`. This was a
  review finding: relying on the general role policy alone permitted it.
- **Foreign-tenant references are indistinguishable from missing ones.** A foreign subject,
  Drone, evidence reference, or workforce email returns 404 with the same problem body as a
  genuinely absent record, so an endpoint cannot be used to discover another tenant's identifiers.
  A duplicate email inside the actor's own organization remains a useful 409 conflict; this is
  not a cross-tenant existence signal.
- **JSONB request fields are validated before persistence.** Drone `payloadMetadata` must be a
  valid JSON document; malformed input returns `400 VALIDATION_FAILED` rather than exposing a
  database/coercion failure as a 500.
- **Subscription entitlement gates writes, not reads.** New or changed MF1 records require an
  active subscription; an expired tenant keeps read and history access rather than losing it.
- **Credential and permit review is an internal human decision.** It records reviewer,
  timestamp and reason for the organization's own audit trail. It is never a government,
  registry, or authority verification, and no field or status claims one.

### Module boundaries

Cross-module access uses narrow module-root facades rather than repositories or entities.
`SubscriptionEntitlement.requireActive(UUID, Instant)` and
`inspections.EvidenceOwnership.existsInOrganization(UUID, UUID)` exist for this reason:
`workforce` and `assets` depend on those module roots, not on `inspections::repository`,
so Spring Modulith still forbids importing another module's persistence types.

### Operational thresholds

MF1 thresholds that affect what a customer sees are configuration, not constants, so a
deployment can change them without a rebuild:

| Setting | Environment variable | Default | Meaning |
| --- | --- | --- | --- |
| `app.workforce.credential-expiring-soon-window` | `CREDENTIAL_EXPIRING_SOON_WINDOW` | `60d` | How far ahead a reviewed credential is shown as expiring soon. A display warning derived from the recorded expiry date — not a statutory renewal rule. Chosen for commercial drone inspection, where operator credentials and liability insurance are annual or longer; no requirement document specifies a window, so it is a product decision. |
| `app.assets.drone-document-max-file-size` | `DRONE_DOCUMENT_MAX_FILE_SIZE` | `10MB` | Largest accepted Drone document upload. |
| `app.assets.document-max-file-size` | `ASSET_DOCUMENT_MAX_FILE_SIZE` | `10MB` | Largest accepted asset document upload. |

These are bound by `@ConfigurationProperties` classes (`WorkforceProperties`, `AssetProperties`)
in the modules that own them. Accepted content types remain a fixed set on both document upload
paths — a wildcard would defeat the check.

A related setting, `app.evidence.max-file-size`, exists in `application.yml` but is not bound to
any properties class. It should not be assumed to control these limits.

**Scope of the expiry warning.** `EXPIRING_SOON` exists only on `workforce_credentials`
(MF1-04/05). `flight_permits` (MF1-07) has no such status, so flight-permit records carry no
expiring-soon signal in this release. That matters when comparing durations: under
Nghị định 288/2025/NĐ-CP a recreational permit lasts up to 10 days while a commercial one
lasts 12 months, and only the second kind is relevant to this product.

## Mobile flow

Mobile endpoints mirror the auth contract under `/api/v1/mobile/auth/**`. Mobile clients receive access and refresh tokens in JSON and store them with platform secure storage. Browser `Origin` requests are rejected on these endpoints.

MF2 inspection APIs are separate from authentication: the backend derives the active Inspector and organization from the authenticated principal. A caller cannot choose an arbitrary Inspector/organization in assignment response, preparation, or field-session requests. Readiness approval/return and readiness-source listing require an `ORG_ADMIN` scoped to the inspection's organization, and approval enforces reviewer/author separation of duties. See [inspection runtime flow](flows/inspections-and-reports/) for route-level details and current partial/unimplemented boundaries.

Mobile exposes `/login`, `/password/setup`, `/refresh` and `/logout` only. Organization onboarding is a browser-first flow: the mobile app has no registration endpoint and an `ORG_ADMIN` registers on the web client before signing in on mobile.

## Tokens and sessions

- Access tokens are currently signed with HMAC-SHA256 (`HS256`) and a short default lifetime of 15 minutes. The secret is supplied through configuration and must be replaced with a high-entropy production secret.
- Claims contain the user subject, issuer, audience, expiry, session id, auth version, roles, actor zone, and organization id when applicable. Email and profile data are not token claims.
- Refresh tokens are opaque random values with a 7-day default lifetime. Only their hash is persisted; each use rotates the token and records the session family.
- Logout, password change, disable, or role change revokes sessions and increments the user auth version so existing access tokens stop working quickly.

## Passwords and abuse controls

- Password hashing uses Spring Security's `DelegatingPasswordEncoder` with Argon2id as the preferred encoder.
- Passwords are 15-128 Unicode characters. There is no periodic forced rotation or arbitrary composition rule.
- Login attempts are rate-limited per account and return `429` with `Retry-After` when exceeded. Refresh-token rotation rejects reuse.
- Security events record login success/failure, lockout, refresh reuse, logout, and account changes without recording credentials or tokens.

## Intentionally out of scope for v1

The current product does not need TOTP enrollment, recovery codes, Redis-backed challenge orchestration, email password recovery, or a separate identity provider. Controlled organization self-registration is in scope; self-registration of platform or workforce roles is not. These other capabilities can be added behind the same service boundary if risk or product scope changes.

## Production configuration

Production must provide secrets through the deployment secret manager. Relevant settings include `AUTH_JWT_SECRET`, `AUTH_REFRESH_TOKEN_PEPPER`, `AUTH_SECURE_COOKIES`, and `AUTH_ALLOWED_ORIGINS`. The one-time administrator bootstrap uses `AUTH_BOOTSTRAP_ENABLED`, `AUTH_BOOTSTRAP_EMAIL`, and `AUTH_BOOTSTRAP_PASSWORD`; disable it after the first account is created. Development-only fallback secrets must not be accepted in a production profile.

See the repository `README.md` files for local commands and the architecture pages for implementation details.
