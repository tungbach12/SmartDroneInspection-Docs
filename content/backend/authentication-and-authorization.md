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

Current roles:

- `ADMIN` - platform-wide administration.
- `CLIENT` - customer-organization workflows.
- `SERVICE_MANAGER` - service request and result operations.
- `INSPECTOR` - assigned inspections and reports.
- `MAINTENANCE_ENGINEER` - assigned maintenance work.

Users also have an actor zone:

- `PLATFORM`
- `CUSTOMER_ORGANIZATION`
- `SERVICE_WORKFORCE`

Role checks are not sufficient by themselves. Services enforce organization scope, assignment scope, and separation of duties.

## Browser flow

Browser endpoints are under `/api/v1/auth/**`:

| Endpoint | Purpose |
| --- | --- |
| `GET /csrf` | Obtain the CSRF token used by browser requests. |
| `POST /login` | Authenticate with email and password. |
| `POST /password/setup` | Complete an administrator-issued first-password setup. |
| `POST /refresh` | Rotate the browser refresh token. |
| `POST /logout` | Revoke the current session. |
| `POST /logout-all` | Revoke all sessions for the user. |
| `GET /me` | Return the current user and roles. |
| `POST /password/change` | Change the password and invalidate old sessions. |

The access token is returned in the login response and held in web memory only. The refresh token is an opaque `HttpOnly`, `Secure`, `SameSite=Strict` cookie scoped to the auth API. It is never written to `localStorage` or returned in JSON.

Browser auth uses CSRF protection and an exact CORS allowlist. API errors use RFC 7807 with a stable `code` and `traceId`; login failures use a generic message.
## Platform user administration
Platform user management is under `/api/v1/platform/users/**` and requires `ADMIN`:
- `POST /api/v1/platform/users` creates a provisioned account.
- `POST /api/v1/platform/users/{userId}/reset-password` issues a new setup credential.
- `PUT /api/v1/platform/users/{userId}/roles` changes roles and revokes the user's sessions.
- `PATCH /api/v1/platform/users/{userId}/status` activates, suspends, or disables an account.

## Mobile flow

Mobile endpoints mirror the auth contract under `/api/v1/mobile/auth/**`. Mobile clients receive access and refresh tokens in JSON and store them with platform secure storage. Browser `Origin` requests are rejected on these endpoints.

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

The current product does not need TOTP enrollment, recovery codes, Redis-backed challenge orchestration, public registration, email password recovery, or a separate identity provider. These can be added behind the same service boundary if risk or product scope changes.

## Production configuration

Production must provide secrets through the deployment secret manager. Relevant settings include `AUTH_JWT_SECRET`, `AUTH_REFRESH_TOKEN_PEPPER`, `AUTH_SECURE_COOKIES`, and `AUTH_ALLOWED_ORIGINS`. The one-time administrator bootstrap uses `AUTH_BOOTSTRAP_ENABLED`, `AUTH_BOOTSTRAP_EMAIL`, and `AUTH_BOOTSTRAP_PASSWORD`; disable it after the first account is created. Development-only fallback secrets must not be accepted in a production profile.

See the repository `README.md` files for local commands and the architecture pages for implementation details.
