# FE-04: Field Records, Evidence and Inspector Quality Decision

Report 3 §3.5 titles this feature "Field Records, Evidence and Inspector
Quality Decision". The filename retains the earlier "inspection execution /
evidence management" wording; the filename is stable, the scope is Report 3's.

## Scope baseline

Report 3 §3.5 gives FE-04 two halves: the **session-record obligations of MF2**
(MF2-09–MF2-12) and the **evidence steps of MF3** (MF3-01–MF3-04). Backend/mobile MF2 session start, postponement, abort and normal completion now exist; the additional-session round-trip still lacks complete Report 5 end-to-end execution.

The `inspections` module implements the MF3 half: scoped evidence upload with a
server-computed checksum and idempotent retry, evidence listing and streaming,
the assigned Inspector's substantive evidence-quality decision that gates AI
analysis and report drafting, and the scoped inspection and report collections
that make those records reachable.

Normal field-session completion uses `POST /api/v1/inspections/{inspectionId}/field-sessions/{sessionId}/completion` with required outcome notes. It closes only the assigned Inspector's current in-progress session as `FIELD_COMPLETED`; it does not assert hardware telemetry, flight-control, or statutory incident reporting. Weather/site-safety postponement remains a separate MF2 action. Manual drone piloting remains outside the platform target.

## Feature sheet summary

Values for the `Feature 4` summary block (`A2:E8` in the workbook). The
template reads these back by formula, so an export needs them recorded here.

| Cell | Label | Value |
| --- | --- | --- |
| `B2` | Feature | MF3 inspection evidence, findings and reporting |
| `B3` | Test requirement | An authorized Inspector uploads evidence with server-computed traceability, records the evidence-quality decision, and reaches assigned MF3 work through a role-scoped list. |

`B4` (`Number of TCs`) and `B5:E8` (per-round counts) are workbook formulas
over the case rows below; do not type values into the Markdown for them.

## Current cases

| Test Case ID | Test Case Description | Test Case Procedure | Expected Results | Pre-conditions | Round 1 | Test date | Tester | Round 2 | Test date | Tester | Round 3 | Test date | Tester | Note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| WF3-002 | Assigned Inspector uploads supported evidence with checksum and source traceability and records the evidence-quality decision with its shot-list comparison. | Upload a valid PNG; retry the identical bytes; list and stream the evidence as the assignee and as a same-organization ORG_ADMIN; attempt upload and read as an unrelated Inspector; submit an unsupported content type, an empty file, an oversize file above the configured 10 MB per-file / 20 MB per-request limits, a truncated PNG header, and non-image bytes declared as `image/png`; submit a half-supplied GPS pair; attempt every quality decision before writing a shot-list comparison; record an accepted decision with a prose shot-list comparison; attempt a limited decision with no reason; confirm the stored decision carries the comparison. | Object-store bytes and PostgreSQL metadata remain consistent; checksum/source/uploader are server-traceable; an identical re-upload returns the existing evidence rather than a duplicate; out-of-scope Inspectors are refused; unsupported content, empty, oversize and **corrupt/undecodable image** input are rejected and leave no evidence row (an over-limit request is `413` — `PAYLOAD_TOO_LARGE` from the multipart parser or `EVIDENCE_TOO_LARGE` from the service guard, whose message now derives the configured 10 MB limit); half-supplied GPS is rejected; **no decision is recorded without a shot-list comparison**; a limited/return decision without a stated reason is refused; the Inspector's prose and the comparison survive the round trip. | An assigned inspection in `FIELD_COMPLETED` or `REPORT_DRAFT`, PostgreSQL via Testcontainers, MinIO via shared test infrastructure, and a supported image available. | Passed | 2026-10-11 | Claude Code (automated) | Pending |  |  | Pending |  |  | Historical result: `InspectionEvidenceApiIntegrationTest` (10 tests at the time), which ran again on 2026-10-11 within the full backend suite of 362 passing tests (`./mvnw.cmd verify`, JaCoCo gate met, Modulith boundary clean). **The suite now contains 12 tests in the current backend source (source count, not a fresh run):** the intake limits changed to 10 MB per file / 20 MB per request and the MockMvc oversize assertion observes the service guard's `413 EVIDENCE_TOO_LARGE`, while a real servlet container may answer `PAYLOAD_TOO_LARGE` first; Re-verified 2026-10-16: the suite's 12 tests (including the corrected oversize-request branch) passed in the five-suite targeted run (81 tests, zero failures) and in the full `.\mvnw.cmd verify` gate (650 tests; Spotless, JaCoCo and Modulith checks met). Object storage is exercised through a real MinIO container, not an in-memory store, so bucket creation and streaming put/get run on every suite. Live MinIO runtime was exercised during earlier browser and API walkthroughs. **MF3-03 product defect found 2026-10-12 and fixed:** the workspace now collects and sends comparison for all four decisions, blocks decision until evidence exists and comparison is non-empty, and presents preview/checksum/provenance. Verified live on inspection `2586669b-bb13-487b-902b-10af6591cb70`; frontend `InspectionEvidencePage.test.tsx` covers the evidence/comparison gates, four outcome payloads and required reasons, staged-file retry, and register rendering. **Backend enforcement added 2026-10-13:** `EvidenceQualityService.decide` rejects null/blank comparison for each substantive decision with 400 `EVIDENCE_QUALITY_INVALID`; `InspectionEvidenceApiIntegrationTest.everyDecisionRequiresAShotListComparison` verifies a blank comparison is rejected without adding decision history. **Passed in backend PR #69 CI run 38325774461:** `./mvnw -B verify`, 491 tests, 0 failures/errors/skips; this integration assertion ran under Testcontainers. The separate local run on 2026-10-13 remained Docker-blocked (263 environment errors); see `test-statistics.md`. |
| WF3-009 | A caller reaches MF3 through a server-paged, role-scoped list, and the report queue is the same collection filtered to inspections that carry a report. | List as an assigned Inspector who also belongs to an organization holding an inspection assigned to someone else; list as a same-organization ORG_ADMIN; list as an ORG_ADMIN from another organization; list as a platform ADMIN; list as a MAINTENANCE_ENGINEER; request page 1 size 2 then page 3 of 5 rows; request `pageSize=5000`; filter to inspections with a report; read a row's inline report summary. | An Inspector sees only assigned inspections and never a colleague's; an ORG_ADMIN sees their own organization only and another organization sees nothing; a platform ADMIN reads across organizations but has no write path; MAINTENANCE_ENGINEER is refused; paging reports `totalCount`/`totalPages` and the last page holds the remainder; an oversized page size is clamped to 100; `/with-reports` returns only inspections carrying a report and carries each row's `reportStatus`/`reportVersionNo`. | Two organizations with fixtures for `INSPECTOR`, `ORG_ADMIN` and platform `ADMIN`, plus a `MAINTENANCE_ENGINEER`; PostgreSQL via Testcontainers. | Passed | 2026-10-09 | Claude Code (automated) | Pending |  |  | Pending |  |  | Verified by `InspectionListApiIntegrationTest` (11 tests). The platform-ADMIN case asserts membership of both tenants rather than an absolute total, because the suite shares one container. Two test-helper defects were found and fixed during this run: creating a cross-tenant fixture inspection violated the composite `(asset_id, organization_id)` and `(inspector_id, organization_id)` foreign keys, which the helper had to satisfy. The 2026-10-12 web split keeps this backend contract unchanged: the inspections list's `?view=reports` filter reads the same server-paged `/with-reports` collection (rows, totals, and summary cards all follow the active view), `/reports` redirects to that filtered view, and the report document's back button returns to it. Covered by frontend `InspectionsPage.test.tsx` (queue defaults to the report filter on `?view=reports`; the toggle switches the list to the report collection) and `ReportsPage.test.tsx` (`/reports` redirects to the owning portal's inspections list with `?view=reports`). |

## Coverage boundary

`WF3-002` covers evidence intake and the Inspector's quality decision. `WF3-009`
covers discovery and scoping of the same records, and the inline report summary
that keeps the inspections and reports screens consistent.

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

`EvidenceQualityService` accepts an additional-session request only from a
`FIELD_COMPLETED` inspection whose latest completed field session carries
available evidence, with a latest READY preparation and matching latest APPROVED
readiness decision. It appends the request plus an INVALIDATED readiness row,
supersedes the prior preparation, creates the next draft and returns to PREPARING
in one transaction. The new preparation requires a future window before
submission; ORG_ADMIN review still gates Start. Prior sessions/evidence remain.
API compatibility enum values `REUPLOAD_REQUIRED` and `LIMITED` remain available
for legacy history/API callers, but web/mobile active Inspector UI only exposes
Accept and Additional session.

Verification in this task: backend `./mvnw verify` passed **684 tests**, 0 failures/errors/skips, with Spotless, JaCoCo and Modulith checks met; `./mvnw -DskipTests package` passed. Frontend `npm run build` passed; mobile code generation passed, but Android build was blocked by the missing Android SDK and the project has no web target. Docs `git diff --check` passed. Frontend/mobile tests and live walkthrough were not run in this task. The repeated visit was not re-assessed as a new evidence set in the product UI, so no case status is changed.

### Capture retirement and bulk batch retirement — 2026-10-17

When captures need replacement (e.g. blurred photos) or an entire batch/flight session is invalid (e.g. imported the wrong SD card or incorrect site captures with hundreds of images):
- Individual retirement: `POST /api/v1/inspections/{id}/evidence/{evidenceId}/retire` marks a capture retired with an attributable reason (`retired_at`, `retired_by_user_id`, `retirement_reason`) without deleting original bytes or checksums.
- Bulk retirement: `POST /api/v1/inspections/{id}/evidence/bulk-retire` applies a single shared reason across a target list of evidence IDs (or all unretired captures if empty/null), enabling one-click retirement of an entire mistaken batch.
- A capture citing active findings cannot be retired until the findings are re-linked or removed.
- Evidence register defaults to active captures and provides search, media-type and evidence-status filters; retired audit copies stay out of the register until requested. Selection checkboxes and a "Bulk retire all active / selected" action use a shared reason form.
- The register reads `GET /api/v1/inspections/{id}/evidence/query`, which filters and pages in the database (`status`, `mediaType`, `search`, `page`, `pageSize`) and returns the inspection's active/retired counts plus the newest capture-added and capture-retired instants, so the status counts and the stale-decision check come from one payload. The existing unpaged `GET .../evidence` list remains for the Findings, Reports and other readers.
- The Findings stage filters retired captures from analysis and candidate lists, and does not load retired images as candidate/reviewer finding photos.
- Verification: backend `InspectionReportApiIntegrationTest.evidenceQueryFiltersAndPagesWithStableScope` covers the filtered/paged read (defaults, status, media type, case-insensitive search, page 2, `pageSize=5000` clamped to 100, ORG_ADMIN read, unrelated Inspector 404) and the pre-existing `inspectorCanBulkRetireCapturesWithASingleSharedReason` still passes; backend `./mvnw.cmd clean verify` passed 665 tests with Spotless, JaCoCo and Modulith checks met on 2026-10-18. Frontend targeted `InspectionEvidencePage.test.tsx` and `InspectionFindingsPage.test.tsx` passed 45 tests; full frontend suite passed 55 files / 389 tests; lint and build passed. A previous live walkthrough retired a batch of 9 captures in one click, showing `Active (0)` and `Retired audit (12)` while preserving all files and database records.


Evidence uploads distinguish a new file, an active same-checksum retry (`deduplicated=true`), and an identical file already retired (`409 EVIDENCE_DUPLICATE_RETIRED`). A same-name/different-content upload is a new item. MF3 success/failure toasts are surfaced through the shared toast host. Evidence now owns one shared asset-area location, set by the assigned Inspector and propagated to its findings; GPS and detector pixel boxes remain separate metadata.

### Mutation outcome notifications — 2026-10-19

The MF3 workflow mutations now report their outcome through the shared toast host instead of leaving
a successful decision silent. Each hook keeps its inline alert detail for validation and read
errors; the toast is the acknowledgement that the server accepted the change.

- Evidence: upload (`Uploaded <file>` / `Already uploaded: <file>`), retirement, bulk retirement,
  shared evidence location.
- Findings: evidence-quality decision, advisory analysis (including the empty-result and failure
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
