# FE-04: Field Records and Evidence

Report 3 §3.5 covers MF2 field-session records and MF3 evidence intake. Evidence
quality is not a separate MF3 decision or gate. The filename retains the earlier
"inspection execution / evidence management" wording; the filename is stable.

## Scope baseline

Report 3 §3.5 gives FE-04 two halves: the **session-record obligations of MF2**
(MF2-09–MF2-12) and **evidence intake in MF3** (MF3-01/02). Backend/mobile MF2
session start, postponement, abort and normal completion exist; the additional-
session round-trip still lacks complete Report 5 end-to-end execution.

The simplified MF3 target stores scoped evidence with available capture metadata,
retains retired evidence as a soft-deleted audit copy, and exposes scoped evidence
listing/streaming. It has no evidence-quality decision or `ACCEPTED` gate. The
Inspector records coverage/limitations in the report, and requests any additional
field session in MF2. Evidence remains editable by the assigned Inspector in
`FIELD_COMPLETED` and during `REPORT_DRAFT`; source edits refresh findings
confirmation and stale any earlier report version. Evidence is locked while a
report is `SUBMITTED` and unlocked after eligible withdrawal or reviewer return;
approved/published sources are immutable.

Normal field-session completion uses `POST /api/v1/inspections/{inspectionId}/field-sessions/{sessionId}/completion` with required outcome notes. It closes only the assigned Inspector's current in-progress session as `FIELD_COMPLETED`; it does not assert hardware telemetry, flight-control, or statutory incident reporting. Weather/site-safety postponement remains a separate MF2 action. Manual drone piloting remains outside the platform target.

## Feature sheet summary

Values for the `Feature 4` summary block (`A2:E8` in the workbook). The
template reads these back by formula, so an export needs them recorded here.

| Cell | Label | Value |
| --- | --- | --- |
| `B2` | Feature | MF3 inspection evidence, findings and reporting |
| `B3` | Test requirement | An authorized Inspector uploads and reads inspection evidence without an evidence-quality decision gate, and reaches assigned MF3 work through a role-scoped list. |

`B4` (`Number of TCs`) and `B5:E8` (per-round counts) are workbook formulas
over the case rows below; do not type values into the Markdown for them.

## Current cases

| Test Case ID | Test Case Description | Test Case Procedure | Expected Results | Pre-conditions | Round 1 | Test date | Tester | Round 2 | Test date | Tester | Round 3 | Test date | Tester | Note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| WF3-002 | Assigned Inspector uploads supported evidence with file metadata and scoped read access; no evidence-quality decision is required. | Upload a valid PNG and a file with the same sanitized filename but different bytes; list and stream evidence as the assigned Inspector and same-organization ORG_ADMIN; attempt upload/read as an unrelated Inspector; submit unsupported content, empty, oversize, truncated/corrupt image input, and a half-supplied GPS pair. | Stored bytes and evidence metadata remain consistent; repeated sanitized filenames follow the documented duplicate policy without claiming checksum identity; out-of-scope Inspectors are refused; unsupported, empty, oversize and corrupt/undecodable input is rejected without an evidence row (over-limit requests return `413` via the multipart parser or service guard); half-supplied GPS is rejected; no quality-decision request or comparison is required. | An assigned inspection in `FIELD_COMPLETED`, PostgreSQL via Testcontainers, MinIO via shared test infrastructure, and supported image files. | Passed | 2026-10-11 | Claude Code (automated) | Pending |  |  | Pending |  |  | Historical result retained: the passed Round 1 run verified then-current checksum/source deduplication and the evidence-quality decision flow. Backend intake and storage assertions were also included in the executed 2026-10-16 five-suite run (81 targeted tests; full `verify` 650 tests). These are historical implementation results, not verification of this revised filename-based/no-quality-gate target; do not promote or alter the recorded Round 1 status. In the current worktree, V39 migration checks passed on disposable PostgreSQL and the backend evidence suite was updated to exercise MF2 Additional Session instead of the retired decision endpoint; its Docker-backed HTTP execution remains pending.
| WF3-009 | A caller reaches MF3 through a server-paged, role-scoped list, and the report queue is the same collection filtered to inspections that carry a report. | List as an assigned Inspector who also belongs to an organization holding an inspection assigned to someone else; list as a same-organization ORG_ADMIN; list as an ORG_ADMIN from another organization; list as a platform ADMIN; list as a MAINTENANCE_ENGINEER; request page 1 size 2 then page 3 of 5 rows; request `pageSize=5000`; filter to inspections with a report; read a row's inline report summary. | An Inspector sees only assigned inspections and never a colleague's; an ORG_ADMIN sees their own organization only and another organization sees nothing; a platform ADMIN reads across organizations but has no write path; MAINTENANCE_ENGINEER is refused; paging reports `totalCount`/`totalPages` and the last page holds the remainder; an oversized page size is clamped to 100; `/with-reports` returns only inspections carrying a report and carries each row's `reportStatus`/`reportVersionNo`. | Two organizations with fixtures for `INSPECTOR`, `ORG_ADMIN` and platform `ADMIN`, plus a `MAINTENANCE_ENGINEER`; PostgreSQL via Testcontainers. | Passed | 2026-10-09 | Claude Code (automated) | Pending |  |  | Pending |  |  | Verified by `InspectionListApiIntegrationTest` (11 tests). The platform-ADMIN case asserts membership of both tenants rather than an absolute total, because the suite shares one container. Two test-helper defects were found and fixed during this run: creating a cross-tenant fixture inspection violated the composite `(asset_id, organization_id)` and `(inspector_id, organization_id)` foreign keys, which the helper had to satisfy. The 2026-10-12 web split keeps this backend contract unchanged: the inspections list's `?view=reports` filter reads the same server-paged `/with-reports` collection (rows, totals, and summary cards all follow the active view), `/reports` redirects to that filtered view, and the report document's back button returns to it. Covered by frontend `InspectionsPage.test.tsx` (queue defaults to the report filter on `?view=reports`; the toggle switches the list to the report collection) and `ReportsPage.test.tsx` (`/reports` redirects to the owning portal's inspections list with `?view=reports`). |

## Coverage boundary

`WF3-002` covers evidence intake without a separate quality-decision gate.
`WF3-009` covers discovery and scoping of the same records, and the inline
report summary that keeps the inspections and reports screens consistent.

Neither case covers the MF2 session-record obligations assigned to FE-04 by
Report 3. Session start, postponement, abort and completion have backend runtime
and targeted tests, but Report 5 has no complete session case. Report 3 §3.7.2
and §3.7.3 (required report content and LLM safeguards) belong to FE-06 and are
likewise not asserted by these cases;
see `fe-06-…md`.

### MF2 session completion and MF3 additional-session boundaries — 2026-10-20

Targeted backend evidence is recorded in FE-03; this FE-04 source does not yet
have a Report 5 case for the complete MF2 session lifecycle. Normal completion
stores `outcomeNotes`, `endedAt`, and session status `FIELD_COMPLETED`, then
returns the inspection from `IN_PROGRESS` to `FIELD_COMPLETED` atomically. The
assigned active Inspector alone can complete their current session against the
current readiness decision. Weather/site-safety postponement is unchanged and
remains a distinct MF2 path.

The target Additional Session action belongs to the MF2 preparation/readiness flow, not the MF3 Evidence screen. It is available only after a completed session, active evidence for that visit, a latest READY preparation and matching APPROVED readiness decision. It appends an INVALIDATED readiness row, supersedes the prior preparation, creates the next draft and returns the inspection to PREPARING in one transaction. The new preparation requires a future window before submission; ORG_ADMIN review still gates Start. Prior sessions/evidence remain. The web Inspector action is in Preparation; mobile exposes it only where its Preparation screen supports the same guarded flow.

Verification in this task: backend `./mvnw verify` passed **684 tests**, 0 failures/errors/skips, with Spotless, JaCoCo and Modulith checks met before the final AI-suggestion rejection-path correction; final `./mvnw -DskipTests package` passed after that correction without executing tests. Frontend `npm run build` passed; mobile code generation passed, but Android build was blocked by the missing Android SDK and the project has no web target. Docs `git diff --check` passed. Frontend/mobile tests and live walkthrough were not run in this task. The repeated visit was not re-assessed as a new evidence set in the product UI, so no case status is changed.

### MF3 report-draft source editing and submission lock — 2026-10-27

The Inspector can upload/retire captures and update shared evidence location while
`FIELD_COMPLETED` or `REPORT_DRAFT`. If a report is already drafted, evidence edits
reopen the findings gate so the Inspector confirms the current source set before
creating a new version; prior versions remain stale and cannot be verified or
submitted. `SUBMITTED` locks evidence changes; withdrawing before reviewer action
or receiving a reviewer return unlocks the editable workflow. `APPROVED`,
`PUBLISHED`, `REPAIR_PENDING` and `COMPLETED` remain immutable. The Evidence UI
shows no `Reopen Findings` action during draft authoring; it shows a read-only
message while submitted or final.

Executed evidence for the affected evidence and report integration classes is
recorded in FE-05/WF3-010; this subsection does not claim a complete Report 5 case
pass.

### Capture retirement and bulk batch retirement — 2026-10-17

When captures need replacement (e.g. blurred photos) or an entire batch/flight session is invalid (e.g. imported the wrong SD card or incorrect site captures with hundreds of images):
- Individual retirement: `POST /api/v1/inspections/{id}/evidence/{evidenceId}/retire` marks a capture retired (`retired_at`) without deleting original bytes. The simplified contract has no separate retire actor/reason fields or reason input.
- Bulk retirement: `POST /api/v1/inspections/{id}/evidence/bulk-retire` retires a target list of evidence IDs (or all unretired captures if empty/null), enabling one-click retirement of an entire mistaken batch; it does not persist a reason.
- A capture citing active findings cannot be retired until the findings are re-linked or removed.
- Evidence register defaults to active captures and provides search, media-type and evidence-status filters; retired audit copies stay out of the register until requested. Selection checkboxes and a "Bulk retire all active / selected" action use a shared reason form.
- The register reads `GET /api/v1/inspections/{id}/evidence/query`, which filters and pages in the database (`status`, `mediaType`, `search`, `page`, `pageSize`) and returns the inspection's active/retired counts plus the newest capture-added and capture-retired instants, so the status counts and the stale-decision check come from one payload. The existing unpaged `GET .../evidence` list remains for the Findings, Reports and other readers.
- The Findings stage filters retired captures from analysis and candidate lists, and does not load retired images as candidate/reviewer finding photos.
- Historical verification: backend `InspectionReportApiIntegrationTest.evidenceQueryFiltersAndPagesWithStableScope` covered the filtered/paged read and the earlier `inspectorCanBulkRetireCapturesWithASingleSharedReason`; backend `./mvnw.cmd clean verify` passed 665 tests on 2026-10-18. Frontend targeted evidence/findings tests, full suite, lint and build passed at that time. Those runs predate the simplified retirement contract and do not verify it. A previous live walkthrough retired a batch of 9 captures in one click, showing `Active (0)` and `Retired audit (12)` while preserving bytes and records.


Historical uploads distinguished active same-checksum retries and retired duplicate files. The simplified target uses a repeated sanitized filename as the inspection duplicate rule, not content identity; a same-name/different-content capture requires a distinct sanitized name. MF3 success/failure toasts are surfaced through the shared toast host. Evidence owns one shared asset-area location, set by the assigned Inspector and propagated to linked findings; GPS and detector pixel boxes remain separate metadata.

### Mutation outcome notifications — 2026-10-19

The MF3 workflow mutations now report their outcome through the shared toast host instead of leaving
a successful decision silent. Each hook keeps its inline alert detail for validation and read
errors; the toast is the acknowledgement that the server accepted the change.

- Evidence: upload (`Uploaded <file>` / `Already uploaded: <file>`), retirement, bulk retirement,
  shared evidence location.
- Findings: Inspector-invoked advisory analysis (including empty-result and failure
  toasts), candidate review/revision, manual finding add/update/remove, findings confirmation and
  reopen.
- Reports: AI-assisted draft, empty manual draft, section save, author verification, submission,
  review (approve/return), withdrawal, publication and the MF3-12 corrective outcomes.
- Verification: frontend `useInspections.test.tsx` asserts the success text and the error severity
  for ten MF3 mutations; full frontend suite passed 55 files / 414 tests with `tsc`, lint and build.
  The Analyse flow was also driven in a Playwright-managed browser against a synthetic Inspector and
  a mocked API, confirming the real Findings button issues
  `POST /api/v1/inspections/{id}/evidence/{evidenceId}/analyze?replace=false`, shows
  "Analysis completed; no defects were detected in this image." and switches the chip to
  "No defects detected" with "Analyze again" offered. No live credentials were used.

### Bilingual checklist content — 2026-10-22

The checklist read and response routes are Inspector-scoped and resolve their
language from `Accept-Language`, with English as the explicit default and
fallback. `V39__add_vietnamese_checklist_content.sql` adds nullable
`name_vi`/`description_vi` to `checklist_templates` and
`section_name_vi`/`prompt_vi`/`guidance_vi` to `checklist_items`. A localized read
returns the Vietnamese column when present and falls back to the English column
when it is absent or blank, so an untranslated template never returns empty
content. The columns are read-only in this release: the backend exposes no
write path for a Vietnamese checklist value and the repository ships no
checklist seed data, so checklist content currently reads as English in either
locale. The Vietnamese read path itself is exercised by the tests below.

The Inspector's recorded answer value, note and completion time are returned
exactly as written in either locale. `InspectionChecklistApiIntegrationTest`
asserts the route shape, the localized system text and the unchanged authored
note; `V39VietnameseChecklistMigrationTest` applies V39 to a populated
pre-V39 database and confirms the English columns are untouched and the
Vietnamese columns are nullable.

Verification in this task: backend `./mvnw -B clean verify` passed, including
`InspectionChecklistApiIntegrationTest` (9 tests),
`ChecklistTemplatePersistenceTest` (3 tests),
`V39VietnameseChecklistMigrationTest`, `RuntimePersistenceInventoryTest` and
`ComplianceApiIntegrationTest`. The Testcontainers MinIO initializer selects a
multi-architecture image on ARM64 so the integration context starts natively.
No Report 5 case status changed; a dedicated end-to-end checklist-localization
case is still outstanding.
