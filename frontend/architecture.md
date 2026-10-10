---
title: "Frontend Architecture"
weight: 10
aliases:
  - /architecture/frontend-architecture/
---

# Frontend Architecture

## Decision

The web client is one React single-page application organized as a feature-first
modular monolith. It serves the Admin, Organization, and field workspaces from
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
| `/org/*` | `ORG_ADMIN` | Dashboard, assets, inspections, reports, maintenance |
| `/field/*` | `INSPECTOR`, `MAINTENANCE_ENGINEER` | Dashboard for both; inspections/reports for Inspector; maintenance for Maintenance Engineer |

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

## MF2 preparation and MF3 inspection and report screens

`/inspections` loads a server-paged, backend-scoped inspection collection; users
select a row instead of entering an identifier by hand. The selected inspection
opens the MF2 mission-preparation panel above the MF3 evidence workspace, because
preparation is what comes first: the Inspector records the component shot-list,
evidence types, access constraints and hazards, submits it with a safety
acknowledgment, and an organization reviewer then decides whether the mission may
fly.

The panel edits the **current** preparation version rather than starting a blank
form, since MF2-07 reviews one specific version. The editor is keyed on that
version, so its fields always belong to the version on screen rather than being
re-seeded after every fetch. Submission is offered only for a submitted version,
and the fields are disabled once the version is `READY`: a readiness decision is
about a particular compliance basis, so editing after it would leave the decision
pointing at content nobody reviewed.

The compliance gate renders blockers as a list carrying their server codes rather
than as an error. MF2-07 needs every blocker at once, and an empty list still
means a named reviewer has to decide, so the empty state says exactly that instead
of reading as clearance.

The MF2-01/02 assignment endpoints and the checklist endpoints do not exist in the
current backend. The API client still carries those functions from an earlier
baseline and nothing calls them; they are not a working path and are not presented
in the UI.

An assigned Inspector may open the evidence workspace, upload `WEB_UPLOAD`
evidence, and record the substantive evidence-quality decision. The same collection
is visible to same-organization ORG_ADMINs and platform ADMINs as read-only
inspection rows; the Inspector-only mutation workspace stays hidden from those
roles, while an organization reader keeps the permit-linking form and the
compliance gate. Maintenance Engineers are directed to Maintenance rather than shown
an inspection list. Analysis and draft generation stay disabled until the evidence
set is accepted, because the backend refuses both. The API computes evidence
checksums and is the authorization boundary; the browser never receives a direct
MinIO URL.

`/reports` uses the same inspection list filtered to rows that carry a report,
with report status/version shown inline. Selecting a row loads that inspection's
report versions. The page presents only the actions permitted by the current
capability and by whether the signed-in user is the version's author: the
Inspector verifies and submits, while a qualified ORG_ADMIN who is not the
author returns, approves, and publishes. A return requires a stated reason.
Platform ADMIN may read cross-tenant rows but does not receive author, reviewer,
or publication actions. The backend scopes every list and mutation by
assignment, organization, platform read-only authority, workflow state, and
separation-of-duties rules.

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
- `/register` is only for first organization onboarding. It calls the
  existing `/auth/register` contract, which creates the organization and
  ORG_ADMIN profile but does not sign the user in. Platform and field roles
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
- The login and organization registration surfaces use the light color scheme with
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

Canonical roles are `ADMIN`, `ORG_ADMIN`, `INSPECTOR`, and
`MAINTENANCE_ENGINEER`. The first organization representative may register the
organization and its first ORG_ADMIN account through the backend contract; the
web client cannot self-assign platform or field roles.

## UI and verification conventions

Material UI provides the shared theme, including light and dark color schemes.
Feature-neutral components such as `DataTable`, `LoadingButton`, `StatusChip`,
`PageHeader`, `ConfirmDialog`, and `QueryState` live in `src/shared/ui/`.

Run `npm test` for the role-to-workspace access-policy tests, `npm run lint` for
Oxlint checks, and `npm run build` for strict TypeScript validation and the
production Vite build.

### Shared workspace shell and color schemes

The Admin, Client, and Operations portals use one Lytic-inspired workspace frame:
a persistent role-filtered side rail, compact page header, account menu, and theme
control. Dashboard composition is shared, while navigation and summary content
remain role-specific. The light scheme is the first-visit default; an explicit
user choice toggles the stored browser scheme. Dark mode uses a near-black
sidebar and panels (`#030712`), a slate canvas (`#111827`), and blue accents
(`#3758F9`), following the Lytic reference. Do not infer that role-specific
metrics exist: show aggregate values only from APIs available to that role, and
keep unavailable summaries clearly unavailable rather than inventing data.
