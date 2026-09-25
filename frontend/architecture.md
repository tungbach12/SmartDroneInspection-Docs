---
title: "Frontend Architecture"
weight: 10
aliases:
  - /architecture/frontend-architecture/
---

# Frontend Architecture

## Decision

The web client is one React single-page application organized as a feature-first
modular monolith. It serves the Admin, Client, and operations workspaces from
one deployment and origin. Role-based routes and navigation provide separate
entry experiences without duplicating the frontend or replacing backend
authorization.

The current stack is React 19, strict TypeScript, Vite, React Router Data Mode,
Material UI, TanStack Query, Zustand, and Axios. Keep this API-first SPA; do not
introduce micro-frontends or a separate app/port per role. Reconsider server
rendering only if a concrete route needs public SEO, server rendering, or a
backend-for-frontend boundary.

## Source layout

```text
frontend/src/
  app/
    layouts/       Shared shell components, one shell configured per workspace
    pages/         App-level pages such as the multi-workspace chooser
    permissions/   Central role-to-workspace and screen-navigation policy
    router/        Route tree, guards, and legacy path redirects
    theme/         Material UI theme and layout tokens
  features/
    auth/          Session UX, role types, sign-in, access-denied page
    assets/        Asset pages, API, and hooks
    inspections/   Inspection pages and workflow UI
    reports/       Report pages and workflow UI
    maintenance/   Maintenance pages and workflow UI
    ...            Add a feature when it has real implementation
  shared/
    api/           Axios client and transport helpers
    ui/            Feature-neutral reusable presentation components
  assets/          Imported static assets
```

Keep pages, API calls, hooks, components, and feature-specific types with their
owning business feature. `app/` composes features and owns cross-feature route
policy. Put code in `shared/` only when it is feature-neutral and reused.
Avoid deep cross-feature imports and empty architecture layers.

## Multi-role route model

All workspaces use the same built application and browser origin. Route prefixes
provide distinct entry pages and layouts:

| Entry route | Roles | Visible sections |
| --- | --- | --- |
| `/admin/*` | `ADMIN` | Dashboard, assets, inspections, reports, maintenance |
| `/client/*` | `CLIENT` | Dashboard, assets, inspections, reports, maintenance |
| `/operations/*` | `SERVICE_MANAGER`, `INSPECTOR`, `MAINTENANCE_ENGINEER` | Dashboard for all three; inspections/reports for Service Manager and Inspector; maintenance for Service Manager and Maintenance Engineer |

The central `app/permissions/accessPolicy.ts` is the frontend navigation and
route-guard policy. It follows the screen-access matrix in Report 3, section
3.1.3. The operations workspace does not show the Assets section. A user with
roles in multiple workspaces selects one at `/portals`; the shell also offers a
workspace switcher. Existing flat paths such as `/assets` redirect to an
authorized workspace path or to the chooser when more than one workspace is
valid.

These checks improve navigation and do not authorize API calls. The backend
must still enforce role, organization, ownership, assignment, resource scope,
workflow state, and separation-of-duties rules. Within a visible section, the
API response and available actions remain scoped to the current user and
resource.

## State and data flow

- TanStack Query owns server state, cache invalidation, and request lifecycle.
- Query-key factories keep list and detail caches predictable.
- Zustand owns small client-only state such as the current user's in-memory
  session and UI notifications. Do not duplicate query data in Zustand.
- Keep temporary form, dialog, and view state local to its component.
- Axios provides the versioned `/api/v1` client and single-flight access-token
  refresh handling. The browser does not persist credentials in local storage;
  refresh credentials use the protected HttpOnly-cookie flow.
- The shared Axios response interceptor unwraps successful `{ success, message,
  data }` API envelopes so feature API modules continue to consume typed payloads.
  RFC 9457 error bodies, `204 No Content`, and binary evidence downloads remain
  unchanged.

## WF3 inspection and report screens

`/inspections` loads only accepted assignments visible to the authenticated
Inspector. It starts or resumes an inspection, reads the published checklist
and saved responses, uploads evidence as `WEB_UPLOAD`, and exposes candidate
verification/manual-finding actions. The API computes evidence checksums and
is the authorization boundary; the browser never receives a direct MinIO URL.

`/reports` uses the same versioned report API for Inspector authors/reviewers,
Service Managers, and Clients. It presents only actions permitted by the
current role, while the backend scopes report lists and mutations to author,
reviewer, organization, workflow state, and separation-of-duties rules. Client
evidence content is streamed through the authenticated report endpoint.

## Browser authentication flow

- `/login` is the shared sign-in page for every role. Users do not select a
  role; the backend returns the account's assigned roles and organization scope.
- On app startup, the client obtains a CSRF token and attempts one cookie-backed
  refresh. The access token and user profile stay in Zustand memory only. An
  expired or revoked refresh cookie leaves the user signed out; protected routes
  preserve their internal return path and check the destination against the
  role-to-screen policy after sign-in.
- Successful sign-in opens the only permitted workspace, or `/portals` when the
  user spans workspaces. Return paths are validated as internal and role-
  permitted before navigation.
- `/register` is only for first-Client organization onboarding. It calls the
  existing `/auth/register` contract, which creates the organization and Client
  profile but does not sign the user in. Platform and service-workforce roles
  cannot be self-selected or self-registered.
- Administrator-issued temporary credentials enter the required first-password
  setup step before creating a browser session. Authenticated users can change
  their password or revoke every session from Account security. Single-device
  sign-out revokes that browser session.
- Login, registration, password setup/change, refresh, and logout requests first
  call `/auth/csrf` and send the returned token in its declared header. This
  follows Spring Security's SPA CSRF flow and obtains a fresh token after
  authentication/logout clears the cookie. The shared Axios client sends
  credentials, retries an expired access-token request once through
  single-flight refresh, and uses the browser Web Locks API when available to
  serialize refresh rotation across tabs. It clears memory state if refresh is
  rejected.
- The login and Client registration surfaces use the light color scheme with
  ocean-blue/teal accents. The global application theme remains switchable.
- Email password recovery and MFA are not offered by the current backend/SRS;
  the page directs account-recovery requests to an administrator instead of
  presenting a nonfunctional reset link.

## Routing, authorization, and deployment

React Router Data Mode owns nested portal routes, lazy feature pages, and route
guards. Each workspace reuses feature pages and shared UI while configuring a
role-appropriate navigation list. Legacy flat feature paths redirect to the
canonical route so bookmarks and existing links do not silently bypass the
screen policy.

During local development, Vite proxies `/api` to the Spring Boot default
`http://localhost:8080`; the frontend and API therefore use the same browser
origin for CSRF and refresh cookies.

Serve the built SPA from one host/port and configure the static host or reverse
proxy to return `index.html` for valid nested frontend paths. Keep the API under
its existing versioned contract. Do not treat a route guard, hidden menu item,
URL prefix, or separate port as a security boundary.

Canonical roles are `ADMIN`, `CLIENT`, `SERVICE_MANAGER`, `INSPECTOR`, and
`MAINTENANCE_ENGINEER`. The first Client representative may register the
organization and its first Client account through the backend contract; the
web client cannot self-assign platform or service-workforce roles.

## UI and verification conventions

Material UI provides the shared theme, including light and dark color schemes.
Feature-neutral components such as `DataTable`, `LoadingButton`, `StatusChip`,
`PageHeader`, `ConfirmDialog`, and `QueryState` live in `src/shared/ui/`.

Run `npm test` for the role-to-workspace access-policy tests, `npm run lint` for
Oxlint checks, and `npm run build` for strict TypeScript validation and the
production Vite build.
