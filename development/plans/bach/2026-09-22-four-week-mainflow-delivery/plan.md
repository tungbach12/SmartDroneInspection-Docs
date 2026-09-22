# Implementation Plan: WF1–WF4 in Four Weeks

**Branch**: `docs/four-week-mainflow-jira` | **Date**: 2026-09-22 | **Spec**: [spec.md](spec.md)

**Input**: Four members, one owner per main flow, with backend, web, and appropriate mobile work
represented as Jira tasks.

## Summary

Deliver a demonstrable SmartDroneInspection lifecycle in four five-day Jira sprints starting in
Jira Week 3 (after the currently active Week 2 sprint):
Client asset/schedule → inspection request/approved order/accepted assignment → Inspector evidence,
verified findings, peer-reviewed report/Client acceptance → maintenance assessment, approved work,
result decision, and post-service invoice status. Each flow has one owner and an independently
testable output. Downstream owners start from test fixtures, then replace them with the real handoff
as predecessor flows become ready.

This is a **time-boxed main-flow release**, not full parity with every optional SRS screen and
operational exception. The four-week target assumes four full-time members, a working PostgreSQL
and MinIO environment, and no redesign of the existing authentication or physical schema.

## Technical Context

**Language/Version**: Java 21 backend; React 19 with strict TypeScript web; Flutter/Dart mobile.

**Primary Dependencies**: Spring Boot 4.1, Spring Modulith, Spring Security, Flyway, Material UI,
TanStack Query, Riverpod, Dio, MinIO, optional configured YOLO service.

**Storage**: PostgreSQL migrations V1–V9 and MinIO. A forward migration is required for the
inspection invoice reference; no existing migration is rewritten.

**Testing**: Backend `mvn verify` including Modulith and coverage; web lint/build and flow tests;
mobile format/analyze/test; authenticated end-to-end workflow scenarios.

**Target Platform**: Backend API, browser portal, Android/iOS field client.

**Project Type**: Four independent Git repositories (`backend`, `frontend`, `mobile`, `docs`) in
one workspace.

**Performance Goals**: Due-cycle retry creates exactly one request; upload retry does not create
duplicate evidence; ordinary list/detail actions remain responsive for the demo dataset.

**Constraints**: Organization and assignment scope, author/reviewer separation, immutable accepted
versions, no upfront payment, no online gateway, no autonomous drone operation. Use existing auth.

**Scale/Scope**: Four flow owners × 20 development days = 80 person-days. Planned Jira work is
approximately 71 person-days, leaving nine team-days for integration and defects. Estimates are
planning assumptions, not a claim that the code is already implemented.

## Constitution Check

| Gate | Plan evidence | Result |
| --- | --- | --- |
| Capability ownership and simplicity | Tasks stay in `assets`, `inspectionrequests`, `inspections`, `maintenance`, and a small real `billing` slice; no speculative folders. | Pass |
| Scoped authorization | Every backend flow has negative tests for organization or assignment scope. | Pass |
| Typed boundaries | Contract handoffs and DTO updates are explicit before client work. | Pass |
| Evidence-based verification | Each owner has an independent flow gate and Week 4 integrated checks. | Pass |
| Auditable delivery | One feature branch and focused PR per repository; owners review cross-repository contract changes. | Pass |

The design below rechecks the same gates after resolving dependencies. There is no planned
constitution exception.

## Four-Week Schedule

The week windows are planning buckets, not Jira due dates. Jira account IDs and calendar settings
are unknown, so the CSV uses week labels and owner labels. Confirm actual working days before
committing to an external deadline.

| Week | Dates (2026) | WF1 — Hiếu | WF2 — Quốc | WF3 — Bách | WF4 — Như | Shared exit gate |
| --- | --- | --- | --- | --- | --- | --- |
| W1 / Jira Week 3 | Sep 28–Oct 2 | Admin catalog and scoped asset API | Request API, manager quotation API, handoff contract | Accepted-assignment fixture, inspection/checklist API, mobile assigned view | Accepted-report fixture, ticket create API/UI, execution mobile UI against fixture | Four flows start independently; auth/schema/storage smoke-tested and handoff DTOs frozen. |
| W2 / Jira Week 4 | Oct 5–9 | Schedules, idempotent due event, WF1→WF2 test | Approval/order and Inspector assignment APIs | Evidence storage, AI candidates and verified/manual findings | Engineer assessment, maintenance quotation/order, mobile assessment | WF1→WF2 and WF2→WF3 backend handoffs pass; no bypass of approved order. |
| W3 / Jira Week 5 | Oct 12–16 | Asset/document and schedule/catalog web screens | Client/manager commercial screens; handoff test | Report versions, peer review, release/acceptance APIs | Work logs/evidence, change order, release/resolution APIs | Accepted report can feed WF4; author/reviewer and change-approval gates pass. |
| W4 / Jira Week 6 | Oct 19–23 | WF1 regression, docs, integration support | Inspector mobile response, WF2 regression, docs, integration support | Web inspection/report, mobile checklist/photo, WF3 regression | Manager/Client maintenance web, live mobile execution, two invoice milestones, full WF4 regression | Full five-role demo, negative-scope tests, quality gates, and linked PRs green. |

### Owner and capacity rule

| Owner | Flow | Planned estimate | Reserve | Delivery responsibility |
| --- | --- | ---: | ---: | --- |
| Hiếu | WF1 | 17 days | 3 days | Asset and scheduling backend/web, catalog, due-cycle handoff, tests. |
| Quốc | WF2 | 17 days | 3 days | Request/order/assignment backend/web, Inspector mobile response, tests. |
| Bách | WF3 | 17 days | 3 days | Inspection/evidence/findings/report backend/web and focused mobile, tests. |
| Như | WF4 + billing | 20 days | 0 days | Ticket/assessment/execution/resolution backend/web/mobile and both invoice milestones. |

WF4 is the critical capacity risk. Hiếu, Quốc, and Bách keep ownership of their own flows but
use reserve days for contract review, integration test pairing, and defect fixes that unblock WF4.
If the four members are not full-time, re-estimate dates before Jira sprint commitment.

### Required handoff gates

| Gate | Target | Producer → consumer | Contract and test |
| --- | --- | --- | --- |
| G1 | End W1 | Shared auth/catalog → all flows | Five roles and seed fixture login; V1–V9 migration and MinIO smoke test. |
| G2 | End W2 | WF1 → WF2 | One periodic request per asset/schedule/due cycle; Client can complete it. |
| G3 | End W2 | WF2 → WF3 | Confirmed order plus accepted Inspector assignment creates ready inspection. |
| G4 | End W3 | WF3 → WF4 | Released and Client-accepted immutable report exposes verified findings for ticket creation. |
| G5 | W4 | WF4 → WF2 | Re-inspection decision creates a linked ad hoc request; no module dependency cycle. |

No owner waits for the predecessor's entire flow. A stable fixture supplies the predecessor state
until the real contract passes. Every change to a handoff shape needs both producer and consumer
tests in the same week.

### Jira sprint mapping

The existing Jira board is `SCRUM board` in project `SCRUM`. Its active sprint, `Week 2 —
Workflows & Slides`, ends on 2026-09-25. Existing future sprint 36, `Week 3 — Database Schema`,
is reused as `W3 — Foundation & DB` so its four database tasks remain visible while
the four flow owners start from fixtures and the frozen handoff contract. Three future sprints are
then added:

| Jira sprint | Dates (Vietnam time) | Delivery purpose |
| --- | --- | --- |
| W3 — Foundation & DB | Sep 28–Oct 2, 2026 | Existing DB work, auth/storage smoke test, fixtures, contracts and each flow's first vertical slice. |
| W4 — WF1 & WF2 Core | Oct 5–9, 2026 | Scheduling, request/order/assignment and first real WF1→WF2/WF2→WF3 handoffs. |
| W5 — WF3 & WF4 Core | Oct 12–16, 2026 | Evidence, findings, reports, assessment, execution and WF3→WF4 handoff. |
| W6 — Integration & Demo | Oct 19–23, 2026 | Mobile/web completion, billing slice, negative authorization tests and five-role demo. |

The CSV maps its internal W1–W4 labels to Jira Weeks 3–6 and includes a date-only `Due Date`
for every task. Existing DB and report/slide issues are preserved; the imported plan is labeled
`plan-2026-09-22` so it can be filtered and reconciled without silently rewriting old work.

### Scope controls for the deadline

- Build one usable web path per Client, Service Manager, and Admin action. Use focused mobile
  screens for Inspector assignment/inspection and Maintenance Engineer assessment/execution.
- Evidence is primarily uploaded through web; mobile photo upload is a focused field option.
- AI candidate processing is integrated where a configured inference service exists. Manual
  findings keep WF3 executable during outages; the configured AI path needs a smoke test.
- In-app status and traceability are sufficient for the four-week demo. Email notification delivery,
  broad analytics, advanced file resumability, offline sync, and online payments are follow-ups.
- Preserve quotation/order/report versions and the named decision branches; do not replace them
  with a single mutable status field to save time.

## Project Structure

### Documentation (this feature)

```text
docs/content/development/plans/bach/2026-09-22-four-week-mainflow-delivery/
├── spec.md
├── plan.md
├── research.md
├── data-model.md
├── flow-handoffs.md
├── quickstart.md
├── tasks.md
├── jira-import.csv
└── jira-import-guide.md
```

### Source Code (repository root)

```text
backend/src/main/java/com/smartdroneinspection/
├── users/                 # Existing authentication and organization identity
├── assets/                # WF1 owner
├── inspectionrequests/    # WF2 owner
├── inspections/           # WF3 owner
├── maintenance/           # WF4 owner
└── billing/               # Created only with the cross-flow invoice runtime slice
backend/src/test/java/com/smartdroneinspection/
frontend/src/features/{assets,inspectionrequests,inspections,reports,maintenance}/
mobile/lib/features/{inspections,tasks}/
```

**Structure Decision**: Keep the current capability modules and existing auth. The file paths in
`tasks.md` are ownership targets; a task may add a class only when that use case is implemented.
Move the existing maintenance invoice entity/repository into `billing` when the cross-flow invoice
service and migration land. This is a real current use case, not a placeholder module.

## Review and Delivery Gates

1. Each Jira Task is at most two estimated days, has one owner, an observable acceptance condition,
   exact affected paths, a week label, and a dependency where needed.
2. Each owner opens small PRs in the relevant repository. A frontend/mobile PR depending on a new
   endpoint links the backend PR and merges after the backend contract is stable.
3. Before a PR merges: `backend` runs `mvn verify`; `frontend` runs lint/build; `mobile` runs
   format/analyze/test; `docs` runs `git diff --check` and link review. Record blocked checks.
4. Week 4 demo uses five distinct role accounts and two organizations. It shows normal closure,
   one quote/assignment revision, rejected self-review, and one rework or re-inspection branch.
5. Cut optional polish before cutting authorization, version history, traceability, or cross-flow
   handoff tests. If G3 or G4 slips beyond its target week, report a revised date immediately.

## Complexity Tracking

No constitution violation is planned. The only new capability, `billing`, is justified by two
current invoice sources and is created with the working invoice use case and forward migration.
