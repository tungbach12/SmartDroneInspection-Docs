# MF4 Web and Mobile Clients — Design

**Owner:** Như
**Date:** 10 October 2026
**Status:** Proposed design; awaiting review
**Repos:** `SmartDroneInspection-Frontend`, `SmartDroneInspection-Mobile`; API dependency is backend branch `feat/maintenance-mf4-work-order`
**Product traceability:** FE-07 / MF4; Report 3 §3.8

## 1. Purpose and success criteria

Complete user-facing MF4 for web and mobile by consuming the backend REST API
through each app's existing auth, routing and state-management layers. Clients do
not duplicate the business workflow or treat route visibility as authorization.

Success means:

1. `ORG_ADMIN` can triage a published repair candidate, create/monitor a work
   order, designate an available team, review estimates/changes, perform
   independent acceptance, reconcile costs and close accepted work in web.
2. `MAINTENANCE_ENGINEER` can see only assigned work on mobile, inspect tasks and
   source context, record/submit work logs, propose changes and prepare/submit
   completion reports where supported.
3. Both clients show state-appropriate named actions, handle loading/empty/error
   states accessibly, preserve server `ProblemDetail` messages, and refresh
   server state after transitions. No client invents costs, credentials,
   notifications, evidence or linked inspections.
4. Frontend lint/build/tests and mobile format/analyze/tests pass, and UI behavior
   is tested against the real API contract.

## 2. Verified current state

### Web

- React 19, strict TypeScript, Vite, React Router, MUI, TanStack Query, Zustand,
  Axios, React Hook Form and Zod are installed and used by existing feature code.
- One SPA serves `admin`, `client` (`ORG_ADMIN`) and `operations`
  (`INSPECTOR`/`MAINTENANCE_ENGINEER`) workspaces.
- `src/features/maintenance/pages/MaintenancePage.tsx` is a placeholder. The
  route exists, but current `accessPolicy.ts` includes `ADMIN` while the MF4
  backend controllers only allow `ORG_ADMIN` and `MAINTENANCE_ENGINEER`. Design
  corrects this UX mismatch and does not add backend authority to `ADMIN`.
- Shared Axios already unwraps `{success,message,data}`, handles refresh and
  standardizes API errors. Use TanStack Query for remote state, RHF/Zod for
  non-trivial forms and shared MUI/status/error components.

### Mobile

- Flutter/Dart, Riverpod, GoRouter, Dio and an auth interceptor/token store are
  present. Dio unwraps the standard success envelope and returns `ApiResult` from
  repositories.
- `lib/features/tasks/presentation/tasks_page.dart` is a placeholder. `/tasks`
  exists in the authenticated bottom navigation; router currently lacks
  role-based route hiding/guarding.
- `MAINTENANCE_ENGINEER` already exists in the mobile auth role enum.
- Current inspection repository has older endpoint names that do not match the
  backend reset contract. MF4 must use the current maintenance controllers only.

### Backend API and blocking gaps

Success JSON uses `ApiResponse<T>`; feature clients consume `data` after the
shared interceptor. Binary downloads, if later added, require a separate file
transport. The current MF4 routes live under `/api/v1/maintenance`.

- **No eligible-team-member lookup exists.** `AssignTeamRequest` requires user
  UUIDs and the backend only validates them after submission. Do not ask an
  ORG_ADMIN to paste UUIDs or fake a picker. Team editing is blocked until a
  same-organization eligible-engineer endpoint exists.
- **No assigned-work inbox endpoint exists.** `GET /work-orders` is
  organization-scoped, not assignment-scoped. Mobile must not fetch every order
  and filter locally, as that would disclose unrelated team metadata. A
  `/work-orders/mine` or equivalent server-scoped route is a prerequisite for a
  real mobile inbox.
- Estimate endpoints support create/list/submit/approve/reject but not edit line
  items. Re-submission/version replacement after rejection must be confirmed and
  tested before the UI offers a retry path.
- The service must enforce estimate approver separation from the estimate
  preparer/report author, independently of the client. Current domain/UI
  contract needs this guard before showing the approval action as available.
- There is no credentials/skills administration or skill-matching API. Interim
  MF4-04 allows no credential record; a present non-active/expired credential is
  rejected. Clients must label this as unverified, not qualified.
- There is no maintenance evidence upload/MinIO workflow, rendered completion
  report artifact/download, or notification delivery.
- `REINSPECTION_REQUIRED` is recorded but does not create/dispatch linked MF1.
  Show it as awaiting follow-up, never as a created inspection.

## 3. Proposed client split

### Web: ORG_ADMIN planning and review console

Only `ORG_ADMIN` receives maintenance UI actions. Remove `ADMIN` from the web
maintenance access policy because the backend has no ADMIN maintenance authority.
The operations workspace keeps Maintenance for `MAINTENANCE_ENGINEER`.

1. **Candidate triage:** read `/repair-candidates`; show source report/finding,
   asset, severity and recommended action; create a work order for a selected
   finding. Empty/loading/error and duplicate-source behavior are explicit.
2. **Work-order list/detail:** server-paged list and detail; show source IDs,
   corrective scope, state, team, tasks, estimates, changes, work logs, report
   versions, acceptance decisions and cost summary using only returned data.
3. **Team:** view team assignments. Add/edit membership UI only after the eligible
   member lookup prerequisite exists; until then show assignment as unavailable,
   not a UUID field.
4. **Estimate/change decisions:** designated budget approver can approve/return
   estimate and approve/reject/return a change, always with reasons where the API
   requires them. Pending/rejected changes never display as authorized budget.
5. **Acceptance/reconciliation/close:** actions only for the designated independent
   ORG_ADMIN; technical acceptance and cost reconciliation remain separate.
   Rework and reinspection decisions require comments.
6. **Honest gaps:** no “credential verified” badge, no notification-sent state,
   no evidence-attachment claim, and re-inspection decision shows follow-up not
   created.

Use feature-owned `maintenance/api`, query hooks, types and components. Query keys
cover candidate/list/detail/subresources; invalidate only affected keys after
mutations. Do not optimistically advance workflow state unless there is explicit
rollback handling.

### Mobile: assigned engineer execution

Only active `MAINTENANCE_ENGINEER` users see the `/tasks` destination; backend
assignment checks remain authoritative.

1. **Inbox/detail:** blocked until a server-side assigned-work endpoint exists.
   Do not use the organization-wide list and client-filter.
2. **Task execution:** show approved scope, assigned tasks, dates and source
   finding; lead uses release/start/declare-complete. Team members record hours,
   as-left condition and readings JSON; they submit their own logs. The lead
   verifies logs before declaring completion.
3. **Changes:** team member proposes a reason/delta; show pending decision and
   approved/rejected status from the server.
4. **Completion report:** designated author creates/verifies/submits the
   structured report. Do not generate LLM text locally or claim an attachment.
5. **Rework:** lead resumes after reviewer return. Reinspection is display-only
   until MF1 dispatch exists.

Use a feature-owned `tasks`/maintenance repository following the existing Dio,
`ApiResult`, immutable model and Riverpod patterns. Map API errors with the
shared failure mapper. Never cache assignments as an authorization source.

## 4. Current API map and UI owner

Paths below are relative to `/api/v1` after each app's shared base URL.

| Action | Web | Mobile | API path |
| --- | --- | --- | --- |
| List candidates / create work order | ORG_ADMIN | — | `GET maintenance/repair-candidates`; `POST maintenance/work-orders` |
| List/detail work orders | ORG_ADMIN | blocked pending assigned-work endpoint | `GET maintenance/work-orders`; `GET maintenance/work-orders/{id}` |
| View/designate team | ORG_ADMIN view; edit blocked pending member lookup | view assigned only | `GET/POST maintenance/work-orders/{id}/team` |
| Tasks | ORG_ADMIN reads | lead creates/reads; member executes assigned task | `GET/POST maintenance/work-orders/{id}/tasks` |
| Estimate | designated budget approver reviews | lead creates/submits | `GET/POST maintenance/work-orders/{id}/estimate-versions`; `POST .../{versionNo}/submit|approve|reject` |
| Execution logs | ORG_ADMIN reads | engineer record/submit; lead verify | `GET/POST maintenance/work-orders/{id}/work-logs`; `POST .../{logId}/submit|verify` |
| Change control | budget approver decides | team proposes | `GET/POST maintenance/work-orders/{id}/changes`; `POST .../{changeNumber}/approve|reject|return` |
| Completion report | ORG_ADMIN reads | report author create/verify/submit | `GET/POST maintenance/work-orders/{id}/reports`; `POST .../{versionNo}/verify|submit` |
| Acceptance | independent reviewer decides | read decision | `GET/POST maintenance/work-orders/{id}/acceptance-decisions` |
| Reconcile/close/rework | designated reviewer | lead resumes rework | `GET/POST .../cost-reconciliation`; `POST .../close`; `POST .../resume-after-rework` |

## 5. Security and error handling

- Role visibility is UX only; service scope checks and tenant-scoped repository
  queries are security authority. Cross-tenant reads remain 404.
- An engineer must be an active work-order team member before writing a work log;
  task assignment must also be within the active team. A lead verifies; a distinct
  independent ORG_ADMIN accepts and reconciles.
- Do not allow ADMIN to create, approve or accept MF4 work. Do not let the
  executing team accept its own work or the estimate author approve the estimate.
- Preserve server error codes/messages for duplicate source, state conflict,
  invalid credentials, out-of-scope users, missing rates, wrong currency and
  reviewer separation. Never auto-retry non-idempotent POSTs.
- After a successful transition, refetch its work order and relevant subresource;
  failed transitions keep server status unchanged in the UI.
- Browser tokens stay in memory; refresh remains in shared Axios/HttpOnly cookie
  flow. Mobile uses existing secure token store and shared Dio interceptor.

## 6. Tests and rollout

### Frontend

- API serialization and typed response/error tests for every consumed route.
- Query invalidation tests for named transitions.
- Role policy tests: `ORG_ADMIN` and `MAINTENANCE_ENGINEER` can see their
  capability sections; `ADMIN` cannot invoke MF4 actions.
- React Testing Library for candidate/work-order states, validation, designated
  approver/reviewer actions, empty/error handling, and member picker disabled
  until backend lookup exists.
- Required checks: `npm test -- --run`, `npm run lint`, `npm run build`.

### Mobile

- Model/repository tests for inbox/detail/task/log/change/report payloads and
  `ApiResult` failures.
- Riverpod/page tests for role gate, no cross-team records, loading/empty/error,
  work-log validation/submission, lead verification and rework resume.
- Required checks: `dart format --set-exit-if-changed .`, `flutter analyze`,
  `flutter test`.

### Cross-client

- Backend integration remains the cross-client source of truth: same-organization
  work, cross-tenant refusal, non-team writer, wrong approver, self-acceptance,
  expired credential, unpriced estimate, rejected change, completion-before-log
  verification, currency mismatch, close-before-reconciliation.
- Client cases become `Passed` only after each platform test is executed; update
  Report 5 FE-07, case index, statistics and change history without reusing retired
  IDs.

## 7. Blocking backend/API prerequisites and phases

1. **Backend contract prerequisites:** same-organization eligible engineer lookup
   for team assignments; server-side `GET /work-orders/mine` or equivalent;
   backend-enforced estimate preparer/approver separation; define safe estimate
   re-versioning after rejection; ensure work-log verification and actual-line
   retrieval fit the client contract. No UUID paste fields or full-organization
   mobile filtering.
2. **Web client:** candidate triage and work-order/review console for the APIs
   already usable; team editing stays visibly blocked until prerequisite lookup.
3. **Mobile client:** assigned-work inbox stays blocked until `/mine`; then task,
   work-log, change, report-author and rework-resume flows.
4. **Client verification/docs:** route/API tests, lint/build/analyze/test, Report 5
   cases/evidence and Nhu's plan update.
5. **Later target work:** mandatory credential presence, skill model, credential
   administration, notification delivery, MinIO evidence object workflow/report
   artifact, and MF1 re-inspection dispatch. These are not simulated in clients.

## 8. Decisions for review

- Remove `ADMIN` from maintenance frontend visibility: **recommended**, matching
  current backend role checks and the four-role MF4 business flow.
- Do not show MAINTENANCE_ENGINEER a mobile maintenance inbox until the backend
  assignment-scoped route exists: **recommended**, to avoid cross-team metadata
  exposure.
- Build client screens only against the feature-branch backend contract; no
  fallback to legacy ticket/quotation endpoints from the pre-reset system.
