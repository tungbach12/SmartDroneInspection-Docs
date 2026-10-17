---
title: "Frontend Architecture"
weight: 10
aliases:
  - /architecture/frontend-architecture/
---

# Frontend Architecture

## Decision

The web client is one React single-page application organized as a feature-first
modular monolith. It serves the Admin, Client, and Operations workspaces from
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
| `/admin/*` | `ADMIN` | Dashboard, assets, asset catalog, inspections, reports, maintenance |
| `/client/*` | `ORG_ADMIN` | Dashboard, assets (Assets, Drones, Permits), inspections, reports, maintenance, workforce (Users, Credentials) |
| `/operations/*` | `INSPECTOR`, `MAINTENANCE_ENGINEER` | Dashboard for both; inspections/reports for Inspector; maintenance for Maintenance Engineer |

The central `app/permissions/accessPolicy.ts` is the frontend navigation and
route-guard policy. It follows the screen-access matrix in Report 3, section
3.1.3. The operations workspace does not show the Assets section. A user with
roles in multiple workspaces selects one at `/portals`; the shell also offers a
workspace switcher. Existing flat paths such as `/assets` redirect to the authorized workspace
path or to the chooser when more than one workspace is valid.

Within the Client workspace, Assets contains the existing infrastructure asset
view plus the MF1 Drone inventory/documents and organization-recorded permit
views. Workforce contains Users and Credentials. These sections are granted only
to `ORG_ADMIN`; platform `ADMIN` retains platform screens and does not inherit
customer resource-management authority. Operations does not expose these Client
resource screens.

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

## MF2 assignment, preparation, readiness and field-session screens

The Inspections workspace places the assignment inbox before the inspection
list. For an assigned Inspector, assignment responses are available in the
inbox; the selected inspection can open its MF2 preparation panel. An
`ORG_ADMIN` can inspect the compliance gate and use the readiness review panel
to approve or return a submitted preparation. These client controls follow the
backend contract; organization ownership, Inspector assignment, reviewer
independence and current workflow state are enforced server-side. Acceptance of
an assignment is not readiness approval.

The web workspace retains the existing MF3 inspection workflow after adding
MF2: evidence intake and retry, evidence-quality decisions, finding/AI-candidate
review and report draft authoring remain available in the selected inspection.
Do not replace these MF3 actions with the MF2 preparation panels.

## MF3 inspection and report screens

`inspections/:inspectionId` is a four-tab workspace layout (`evidence`,
`findings`, `report`, `preparation`) with an index redirect to `evidence`. Each
stage owns its own sub-page and local input state; the layout renders only the
inspection header, the stage tabs, and an outlet. Report document editing stays
on the separate `reports/:inspectionId` page.

The `evidence` tab stages a multi-file queue and uploads it with one existing
single-file mutation call per file in order; a failed file stays in the queue
with its error without blocking the rest. Below it, the single shot-list
comparison field plus "Accept evidence set" records the MF3-03 set-level
decision, disabled until at least one evidence item exists and the comparison
is non-empty. The `findings` tab runs advisory detection automatically as a single
pass over the images that have no candidate once the set is accepted, shows each
candidate with its defect photo resolved from the evidence content endpoint and
its own severity/location inputs for Confirm/Modify, and surfaces the MF3-09
reviewer verdict on undecided findings. The images of that pass are analysed in
parallel and each result is written into the candidate cache as it arrives, so a
row flips to "Detection complete" and its candidates appear in the Findings list
as soon as that image's response lands instead of after the slowest image; a
failure or timeout on one image leaves the others running and reports itself. The
automatic pass is offered once per
inspection and remembered for the tab session, so reopening Findings does not
restart detection. An image that already has candidates shows "Detection complete"
and offers no re-run control because MF3-05 returns existing candidates rather
than rerunning inference; the explicit per-image **Analyze** action remains
available for unanalysed images. A finding remains linked to its evidence;
location prose is optional where the image/component context is clear. Manual
findings require source evidence.

Pending candidates block **Confirm findings and continue**. An empty set requires
explicit acknowledgment that no finding was observed within the covered scope.
Confirmation records a backend snapshot and moves to Report without creating a
version or calling the drafting model. The Inspector may reopen Findings before
submission; material changes clear confirmation and require reconfirmation.

The `report` tab reads backend workflow state and separately offers **Generate
report draft** or manual structured authoring, both disabled until the current
findings confirmation is valid. A failed model request creates no version; the
Inspector may then explicitly choose manual authoring. The report-document link
is enabled only after a version exists. While generation is pending, the UI shows
an indeterminate wait state because the API exposes no progress percentage. The
author reviews and verifies each section before submission. ORG_ADMIN performs
independent finding/report review, return or approval and publication on the
separate report page. The `preparation` tab mounts MF2 panels unchanged.

`/inspections` loads the assignment inbox and a server-paged, backend-scoped
inspection collection; users select a row instead of entering an identifier by
hand. The `?view=reports` filter switches the same list, its totals, and its
summary cards to the server-paged `/with-reports` collection, so the report
queue is that filtered view and `/reports` redirects to it. An assigned Inspector
may open the evidence workspace, upload `WEB_UPLOAD` evidence, and record the
substantive evidence-quality decision. The same collection is visible to
same-organization ORG_ADMINs and platform ADMINs as read-only inspection rows;
the Inspector-only mutation workspace stays hidden from those roles. `MAINTENANCE_ENGINEER` users are directed to Maintenance rather than shown an inspection list.
Analysis and draft generation stay disabled until the evidence set is accepted,
because the backend refuses both. The API computes evidence checksums and is the
authorization boundary; the browser never receives a direct MinIO URL.

The report document page presents only the actions permitted by the current
capability and by whether the signed-in user is the version's author: the
Inspector verifies and submits, while a same-organization ORG_ADMIN who is not
the author returns, approves, and publishes. Independence, role, organization
and active-account checks are enforced; reviewer professional qualification is
not validated at runtime. A return requires a stated reason.
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

When the reverse proxy enforces a request-body limit, keep it at or above the
backend's request bound (`EVIDENCE_MAX_REQUEST_SIZE`, 20 MB) rather than at the
per-file limit (`EVIDENCE_MAX_FILE_SIZE`, 10 MB). A proxy bound equal to the
per-file limit rejects a permitted upload before the backend sees it, and the
client then receives the proxy's own error page instead of the API's structured
`413` (`PAYLOAD_TOO_LARGE` or `EVIDENCE_TOO_LARGE`) that the upload UI reports.

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
