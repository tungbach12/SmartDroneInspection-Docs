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

Role checks are not sufficient by themselves. Services enforce organization scope, assignment scope, and separation of duties.

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

The first organization representative (an `ORG_ADMIN`) may self-register a new organization through `POST /register`. The request contains the representative's name and credentials together with the organization name and unique organization code. The backend creates the organization and the first user in one transaction, activates both immediately, and assigns only the `ORG_ADMIN` role in the `CUSTOMER_ORGANIZATION` actor zone. There is no email-verification or administrator-approval gate in v1.

Registration cannot create or select `ADMIN`, `INSPECTOR`, or `MAINTENANCE_ENGINEER`. Email and organization-code uniqueness, password policy, request rate limits, organization isolation, and an append-only `ORGANIZATION_REGISTRATION` audit event are enforced by the backend. The registration response contains the created organization and user profile but no access or refresh token; the representative signs in through the normal login flow.

The browser and mobile request body is:

| Field | Meaning |
| --- | --- |
| `email` | Representative's login email. Lookup is case-insensitive. |
| `fullName` | Representative's display name. |
| `organizationName` | Name of the new customer organization. |
| `organizationCode` | Unique 3–64 character code using letters, numbers, `-`, or `_`; it is stored in uppercase. |
| `password` | A 15–128 Unicode-character password validated by the shared password policy. |

Successful registration returns `201 Created` with the organization identifier/code and the new user profile. It does not issue tokens, set a refresh cookie, or expose the password.

The `data` payload is `{ organizationId, organizationName, organizationCode, user }`; `user` contains the new user's identifier, normalized email, name, role list (`ORG_ADMIN`), actor zone, and organization identifier. The complete success body is `{ success: true, message: "Success", data: { ... } }`.

## Platform user administration
Platform user management is under `/api/v1/platform/users/**` and requires `ADMIN`:
- `POST /api/v1/platform/users` creates a provisioned account.
- `POST /api/v1/platform/users/{userId}/reset-password` issues a new setup credential.
- `PUT /api/v1/platform/users/{userId}/roles` changes roles and revokes the user's sessions.
- `PATCH /api/v1/platform/users/{userId}/status` activates, suspends, or disables an account.

## Workforce credential visibility

MF2-07 readiness approval requires the reviewer to name their own credential, the assigned Inspector's credentials and the assigned Drone's documents. Those identifiers cannot be invented by a client, so two read routes expose them. Both require `ORG_ADMIN` in the caller's own organization.

- `GET /api/v1/workforce/credentials/me` returns **the caller's own** credentials. There is no id, user or organization parameter, so a caller cannot ask about anyone else's record.
- `GET /api/v1/inspections/{id}/readiness/sources` returns the credentials of the inspection's assigned Inspector and the documents of its assigned Drone, reached through that inspection.

These routes return metadata, not documents. A credential travels as type, issuer, reference, issue and expiry dates, status, and whether the stored record says it was verified and when. A Drone document travels the same way. No file content, no download link and no `evidenceId` download path is exposed here; MF2-07's decision is based on the reference and the validity window, and the reviewer confirms the paperwork itself.

The scope rule is the reason this is an ORG_ADMIN capability rather than a public or Inspector one: reviewing an Inspector's qualification is an employer's management act. It is deliberately narrow in two ways. It is a **same-organization** read only, so one tenant's workforce records cannot be reached through another tenant's inspection. And `drone_documents` carries no organization column of its own, so the Drone's owner is joined in: filtering on the Drone alone would let a caller enumerate another organization's documents by guessing a Drone id.

A cross-tenant caller receives `404 INSPECTION_NOT_FOUND` rather than an empty list, because an empty list would confirm that an inspection with that id exists. An Inspector receives `403`: they are the subject of the record being reviewed, not the reviewer of it.

This is an internal-record check. A stored record saying a credential was verified is not issuer-registry verification, and `READY_FOR_FLIGHT` is not external flight authority.

## Mobile flow

Mobile endpoints mirror the auth contract under `/api/v1/mobile/auth/**`. Mobile clients receive access and refresh tokens in JSON and store them with platform secure storage. Browser `Origin` requests are rejected on these endpoints.

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
