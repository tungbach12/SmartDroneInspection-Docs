# FE-06: Inspection Report Drafting, Review and Publication — MF3

Report 3 §3.7 titles this feature "Inspection Report Drafting, Review and
Publication". The filename retains the earlier "inspection report / approval"
wording; the filename is stable, the scope is Report 3's.

## Scope baseline

The report author is the assigned `INSPECTOR`; a same-organization `ORG_MANAGER`
who is not the author reviews and publishes. Runtime review enforces role,
organization, active-account and separation-of-duties checks, but it does not
validate reviewer credentials: professional qualification is an explicit
implementation gap and runtime review must not be described as qualified.
There is no Client acceptance step and no separate Manager release in the
current Enterprise SaaS system, so the earlier marketplace review/release/acceptance
case does not apply and has been removed from this report.

The model drafts only when the assigned Inspector requests it; humans decide.
The author records coverage and limitations, verifies the generated content, and
a reviewer who is not the author approves. Nothing publishes on a timer, and a
published version is immutable. The MF1 inspection scope (`objective`, `scope`,
`component_scope`, `acceptance_criteria`) remains stored on the inspection and
is not replaced by report content.

## Unverified requirements inside this feature

`WF3-005` and `WF3-006` exercise authorship, return, approval and immutability.
They do **not** establish:

- **Report 3 §3.7.1 MF3-07 source completeness** — a focused draft-context test and
  disposable live walkthrough now demonstrate inspection objective/scope/criteria,
  recorded evidence metadata, inspection-scoped candidate records and field-session
  records entering the model input. They do not cover persisted Inspector observations
  or checklist answers; no dedicated inspection-scoped source for either was identified.
  The walkthrough did not assert source-citation links per section or prove safe output
  for every candidate review state.
- **Report 3 §3.7.2 "Required Inspection Report Content"** — the required
  content sections of a released report.
- **Report 3 §3.7.3 "LLM Safeguards"** — all drafting safeguards, including
  numeric-table sourcing rules and handling of untrusted evidence metadata.
- **Report 3 §3.7.1 MF3-09 reviewer credential qualification** — runtime
  validates role, organization, active account and separation of duties only.
  No credential or professional-qualification check exists.
- **Report 3 §3.7.1 MF3-12/MF3-13 corrective outcome and handoff** — code and
  schema exist and the backend paths executed green on 2026-10-16 (81 targeted
  WF3 tests and the 650-test full `verify` gate), but no case is passed until
  `WF3-012`'s complete end-to-end scenario executes; it remains Pending.

These remain open gaps; the `Passed` FE-06 cases do not establish all of §3.7.

## Current cases

### Source-backed report context and PDF alignment — 2026-10-19

Backend changes now expose tenant-scoped organization/asset/Drone identity and stored preparation,
readiness, evidence, findings-confirmation and field-session details in the report-version
response. The historical implementation returned evidence-quality context; it is not part of the simplified
target contract. The delivered PDF composes the same available records and omits absent-record boilerplate;
pre-flight free text is labelled as an Inspector-entered note, not proof of an itemized checklist or
flight. `V35__persist_field_session_preflight_note.sql` persists the required note from the existing
start-session request. Item-level checklist responses are drafted/rendered only when a persisted
response joins to a session and one of that session template's item records.

Executed evidence (2026-10-19): backend `./mvnw.cmd -B verify` passed 668 tests, 0 failures,
errors or skips; Spotless, JaCoCo and Spring Modulith checks passed. New/updated assertions cover
response context identity, PDF rendering of asset/preparation/Drone/session facts without the old
unconditional checklist boilerplate, persistence/readback of the pre-flight note, and passing only
stored checklist responses from the session's template to draft context. Frontend
`ReportDerivedSections.test.tsx` passed 6 tests; `npx tsc --noEmit` passed; `npm run build` passed;
`npm run lint` exited 0 with the same six Fast Refresh warnings. Published report artifacts were not
rewritten and no approve/publish or other irreversible workflow action was performed. These are
supplementary source-context regressions, not a pass of WF3-005/006 or full §3.7.2 content compliance.

### Organization Manager reviewer workspace — 2026-10-19

The Client report queue now presents Organization Manager work as a distinct WF3 reviewer task rather
than the Inspector's field-work screen with disabled controls. `/client/inspections?view=reports`
uses the existing server-paged `/with-reports` collection and presents page-scoped counts for
submitted decisions, approved-but-unpublished reports, and published follow-up; rows use
review-specific status labels and route to a status-appropriate review, publish, or outcome action.
This is a view of the current page only, not a cross-page aggregate. The reviewer inspection
workspace opens on **Review report**, names the Organization Manager responsibility, returns to the
review queue, and also labels Evidence, Findings and Preparation as review/readiness contexts. The
Evidence page hides upload, retire, quality-decision editing and shot-list input while showing the
Inspector's recorded comparison and the read-only register. Findings shows the Inspector-confirmed
set and separately labels pending AI candidates as advisory; it has no detection or finding controls.
The former report-draft tab is a read-only version-status/link view for this role. The existing
`reports/:inspectionId` page remains the owner of report-level approve/return, publish and
post-publication corrective outcomes; no backend authorization or API contract changed.

Executed evidence (2026-10-19):

- Frontend targeted review-flow tests — 7 files / 99 tests passed, including ORG_MANAGER queue rows
  with `SUBMITTED` / `APPROVED` / `PUBLISHED` next actions, report-queue navigation, reviewer tabs,
  read-only evidence and findings screens, Inspector-only draft controls, and the existing report
  approve/return/publish actions.
- `npx tsc --noEmit` — passed; `npm run build` — passed. `npm run lint` — exit 0 with six existing
  `react(only-export-components)` Fast Refresh warnings.
- No backend role, organization, author separation, qualification or workflow gate changed; UI
  visibility remains navigation only. No Report 5 case status changed; WF3-005/006/011/012 retain
  their existing statuses and acceptance boundaries.

The added aggregate-confirmation and separate draft-choice requirement is tracked
as `WF3-011`. The post-publication corrective-outcome and handoff requirement is
tracked as `WF3-012`. Both remain Pending until their complete backend/UI
scenarios are run; component-level green tests are not represented as execution
of either case.

| Test Case ID | Test Case Description | Test Case Procedure | Expected Results | Pre-conditions | Round 1 | Test date | Tester | Round 2 | Test date | Tester | Round 3 | Test date | Tester | Note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| WF3-005 | AI Vision candidates and the inspection-report draft are verified by the author Inspector before ORG_MANAGER publication. | Provide active evidence; explicitly invoke analysis on a selected image and verify manual finding entry remains available; author a draft (automated where configured, otherwise the manual structured draft); verify and submit as the author Inspector; attempt a return without a reason; return with a reason; attempt to review one's own report; resubmit and approve as an independent ORG_MANAGER. | Only human-confirmed findings enter official outputs; the author Inspector's authorship and the independent ORG_MANAGER's approval are recorded (runtime does not validate reviewer credentials); unverified draft text cannot be published; a failed or unconfigured drafting service still permits a structured manual draft under the same review gates. | Assigned inspection with active evidence and a confirmed findings set (empty only with Inspector acknowledgment), plus an independent active ORG_MANAGER in the same organization. | Passed | 2026-10-08 | Claude Code (automated) | Pending |  |  | Pending |  |  | Historical, pre-simplification verification (2026-10-08 through 2026-10-11): `InspectionReportApiIntegrationTest` (14 tests at that time) and, on 2026-10-11, `InspectionReportDraftingApiIntegrationTest` (5 tests at that time): `draftingProposesSectionValuesThatTheAuthorCanReadBack`, `draftingRecordsItsProvenanceOnTheVersion`, `draftingNeverAltersAReviewedFinding`, `aFailedGenerationLeavesNoVersionAndReportsTheFailure`, and `theManualDraftRemainsAvailableWhenDraftingIsUnconfigured`. The section-authoring path is exercised in `InspectionReportSectionsApiIntegrationTest`. `ReportDraftClientTest` (6 tests) covers the section-proposal prompt, absent-section handling and the failure path. Full run 2026-10-11 within the backend suite of 362 passing tests. A live external vision-model walkthrough was recorded on 2026-10-12 (three PENDING candidates returned; see historical verification row in `test-statistics.md`); this does not verify the report-drafting LLM provider. The automated report-drafting path uses a deterministic `ReportDraftPort`; the live drafting-provider happy path remains unexecuted. The 2026-10-12 web split preceded the current target contract. Historical frontend coverage expected an ACCEPTED gate; this target instead requires active evidence plus a current confirmed findings set and has no evidence-quality decision. **MF3-04 enforcement added 2026-10-13:** `ReportService.verifyVersion` and `submitVersion` compare the current evidence checksum hash with the version snapshot; mismatch returns 409 `REPORT_SNAPSHOT_STALE`. **Passed in backend PR #69 CI run 38325774461:** `./mvnw -B verify` ran 491 tests, 0 failures/errors/skips; `evidenceAddedAfterTheDraftMakesVerificationStale` and `evidenceAddedAfterVerificationMakesSubmitStale` executed under Testcontainers. The separate local `mvn.cmd -o verify` attempt remains recorded as Docker-blocked (263 environment errors) in `test-statistics.md`. **Current source counts are larger — `InspectionReportApiIntegrationTest` 26, `InspectionReportDraftingApiIntegrationTest` 10, `InspectionReportSectionsApiIntegrationTest` 22 (counted from the test sources, not a run record) — and the current source's MF3 suites passed the executed 2026-10-16 runs (81 targeted tests; 650-test full `.\mvnw.cmd verify` gate), but the case remains Pending until the complete end-to-end scenario executes.** |
| WF3-006 | The approved report version is immutable and source-traceable, publication stores its PDF deliverable and records the checksum; per-finding Maintenance forwarding is a separate post-publication action. | Publish an approved report; verify stored PDF/checksum and immutable version; verify the PDF evidence register and finding details use available linked evidence location metadata. | The published artifact is retrievable/checksum-verifiable and immutable; only subsequently selected findings receive `forwarded_to_maintenance_at`; the PDF evidence register shows linked evidence location where available. | Published MF3 review artifacts; report preview fixtures with linked evidence and a confirmed finding. | Passed | 2026-10-11 | Claude Code (automated) | Pending |  |  | Pending |  |  | Historical result retained. **The current source separates MF3-12/13 from publication:** publish now ends at `REPORT_PUBLISHED`, and the corrective outcome plus recorded handoff happen afterwards, tracked by `WF3-012` (Pending). The executed evidence for this case was recorded on the pre-change flow, so the `Passed` status refers to that run; the current source's MF3 suites passed the executed 2026-10-16 runs (81 targeted tests; 650-test full `.\mvnw.cmd verify` gate), but the case remains Pending until the complete end-to-end scenario executes. Supplementary evidence-location PDF regression passed 2026-10-13; this does not establish full §3.7.2 compliance. |
| WF3-011 | Inspector resolves proposals, explicitly confirms a non-empty or acknowledged-empty findings set, and separately chooses AI-assisted or manual report authoring. | Exercise pending proposals, resolved proposals, manual findings, confirmation, separate draft choice, and explicit acknowledgment when no findings exist; invoke analysis explicitly for a selected image; mutate evidence/findings after confirmation; attempt drafting or publication with an undecided proposal. | Unresolved proposals block confirmation; empty scope requires Inspector acknowledgment; confirmation creates no report/version or AI call; AI/manual draft choices are separate; material edits reopen Findings and require reconfirmation; no evidence-quality acceptance or automatic analysis gate exists. | Assigned Inspector; completed inspection with active evidence; Testcontainers/PostgreSQL and stubbed inference/draft ports; web UI/API tests. | Pending |  |  | Pending |  |  | Pending |  |  | Target case definition updated for explicit AI invocation and no evidence-quality gate. Historical implementation/status notes elsewhere remain dated evidence; keep Pending until the complete backend and frontend target scenario executes.
| WF3-012 | After publication, the Organization Manager selects confirmed findings to forward to MF4, and the System records per-finding forwarding plus the inspection's overall status without creating a work order. | Publish an approved report and confirm the inspection reaches `REPORT_PUBLISHED` with an unchanged PDF; select a subset of confirmed findings to forward; verify only selected finding IDs receive `forwarded_to_maintenance_at`; verify inspection status becomes `REPAIR_PENDING`; repeat with no selected findings and verify `COMPLETED`; repeat with an explicitly acknowledged empty findings set and verify `COMPLETED`; verify the audit event identifies actor, report version, selected IDs and before/after status; verify the UI asks for explicit confirmation before empty-selection completion and a completed inspection refuses later forwarding; confirm no no-repair rationale or per-finding corrective-action rationale/priority/due-date is requested or stored. | MF3-11 publication ends at `REPORT_PUBLISHED`; selected findings receive a per-finding forward timestamp; inspection status is `REPAIR_PENDING` if any finding was forwarded and `COMPLETED` if none were forwarded on a newly published inspection (including an acknowledged empty set); an audit event preserves actor, report version, selected IDs and status transition without duplicate handoff fields on the inspection; no MF4 work order is created; the published PDF is never modified. | Published MF3 report with confirmed/modified findings (plus an empty-findings variant); active independent ORG_MANAGER; PostgreSQL via Testcontainers; target implementation. | Pending |  |  | Pending |  |  | Pending |  |  | Target case definition updated from per-finding corrective outcomes to per-finding forwarding. Historical implementation and executed 2026-10-16/17 evidence refer to the superseded workflow and do not verify this target. Current source updates assertions for selected IDs, durable handoff audit, empty-selection completion and refusal after completion; backend Testcontainers execution remains blocked by Docker unavailability, so retain Pending until a complete target end-to-end run. |


## Targeted report-content regression — 2026-10-13

The PDF preview regression in `InspectionReportSectionsApiIntegrationTest.previewRendersConfirmedFindingsAndAttachedEvidence` passed: a confirmed finding's component/location is rendered in its linked evidence-register row, and the finding section retains the same location. Frontend `ReportDerivedSections.test.tsx` passed the GPS-precedence, official-finding fallback, and pending-finding exclusion cases. Live authenticated UI verification also passed: inspection `78b9c412-a04d-43c6-abbd-ef54d5a58932`, version v5, shows `Pier 2 north face` both on the confirmed finding and on its linked `spalling.jpg` evidence row. This remains narrow evidence-location coverage only; the broader §3.7.2 report-content verification gap stays open.

### WF3 drafting-input follow-up — 2026-10-14 (historical contract)

The historical draft-context slice passed inspection scope, accepted evidence metadata, AI candidate and field-session records, and an Inspector-recorded evidence-quality decision. It used the latest decision as a gate. The simplified target removes that decision/context and requires coverage and limitations to be authored in report sections. The recorded historical tests do not verify the target contract or full §3.7.1–§3.7.3 compliance.

### Disposable Inspector walkthrough — 2026-10-14

Historical execution (pre-simplification): against local Docker services, an Inspector used the UI on disposable inspection `2fa8fd35-285a-43c4-a616-69d05cc8250d` (`FIELD_COMPLETED`). Six synthetic local JPG fixtures uploaded successfully; the Inspector recorded a test-only coverage comparison and accepted the evidence set. Automatic detection stored 17 `PENDING` candidates across all six images; zero official findings and zero field sessions existed. The final analysis request appeared aborted in the browser when navigating away, but a read-only DB check confirmed candidate records for all six images, including three for `coating-blister.jpg`. The quality decision and automatic-analysis behavior are superseded by the current target contract and are not evidence for it.

The generated draft was inspected read-only. It included objective/scope/component scope/criteria, six evidence files, 17 pending candidates and missing-data disclosures, but not the Inspector-entered quality comparison; this walkthrough predates the later quality-context code/test change above. It correctly called the inspection planned and equipment/method/conditions unrecorded, but the executive summary still described synthetic fixtures as submitted captures and recommendations proposed physical validation. The evidence is synthetic: **author verification was not performed**, and the report was not saved, submitted, approved, or published. This exploratory run is not a passed WF3 test case. The final analysis request reported `ERR_ABORTED` in the browser after navigation, but read-only DB inspection confirmed stored candidates for all six images (17 total, including three for `coating-blister.jpg`). Existing inspection `78b9c412-a04d-43c6-abbd-ef54d5a58932` was inspected read-only; no changes were made to it.

### MF3-10 confirmed-findings rendering correction — 2026-10-15

The rendered document previously required a reviewer decision before listing a finding, so a finding
the Inspector had confirmed was omitted from section 6 while the drafted executive summary and
conclusions cited it. That contradicted the Findings UI ("Included in the report draft as a verified
finding") and left the document disagreeing with the reviewed set. An Inspector-confirmed proposal is
now listed from the draft onward; the MF3-09 verdict refines a proposed finding rather than deciding
whether it appears. Only a rejected finding is excluded, and approval/publication still refuse while
any proposal is undecided, so a delivered report never carries a pending verdict. An undecided
finding renders its decision as "Awaiting reviewer decision" instead of being presented as decided.

Executed evidence:

- `./mvnw.cmd -B verify` — **645 tests, 0 failures, 0 errors, 0 skipped; BUILD SUCCESS** for the
  initial 4.19 correction. The 4.20 full rerun passed **647 tests, 0 failures, 0 errors, 0 skipped;
  BUILD SUCCESS**, including `InspectionReportApiIntegrationTest.aReturnedVersionDoesNotAllowFindingDecisionsAfterPublication`,
  `InspectionEvidenceApiIntegrationTest.evidenceUploadIsRejectedAfterReportPublication`,
  `InspectionReportSectionsApiIntegrationTest.previewRendersAnInspectorConfirmedFindingThatHasNoReviewerDecisionYet`
  (observed red first: the PDF read "6. Confirmed findings / No confirmed findings were recorded for
  this version") and `previewOmitsAFindingTheReviewerRejected`.
- Frontend `npm test -- --run` — 54 files, **363 tests passed**; `npm run lint` unchanged at the
  6 pre-existing warnings; `npm run build` succeeded. New cases:
  `ReportDerivedSections.test.tsx` "lists a finding the Inspector confirmed that has no reviewer
  decision yet" and "excludes a finding the reviewer rejected".
- Live browser check on inspection `e3e11000-561b-4f81-8173-868772a15c02` (Field Inspector): the
  report's Confirmed findings section now lists both `corrosion` (MEDIUM, UNREVIEWED, attached
  `bolt-corrosion.jpg` with its defect photograph) and `sdfsdf` (LOW, CONFIRMED), matching the
  two findings the drafted executive summary already claimed. The frontend section filter carried the
  same defect and was corrected with it.

No WF3-005/006/011 case status changed; these are supplementary regression coverage for MF3-10
rendering, and do not establish full §3.7.2 report-content compliance.

### MF3-12/13 post-publication per-finding forwarding — target clarification

The simplified target publishes the immutable, checksummed report at MF3-11.
After publication, the Organization Manager selects confirmed finding IDs to
forward. Selected findings receive `forwarded_to_maintenance_at`; a newly
published inspection becomes `REPAIR_PENDING` when IDs are selected and
`COMPLETED` when the selected list is empty. A completed inspection cannot later
change this Maintenance disposition. No corrective-action rationale, priority,
due date, or no-repair rationale is collected by MF3. An append-only
`audit_events` row preserves the reviewer, report version, selected IDs and
before/after aggregate inspection status; duplicate handoff columns are not
stored on `inspections`. The handoff does not create an MF4 work order.

V39 is a forward Flyway migration, not a code-first cutover. It removes the
quality-decision table and audited legacy fields, adds per-finding forwarding
and version submission timestamps, and renames the report return-reason column.
It has been applied to fresh disposable PostgreSQL schemas from V1–V38. A
representative populated fixture confirmed distinct finding-note preservation,
transfer of a single unambiguous linked finding location to evidence, and legacy
handoff timestamp/selected-ID/actor audit migration. Fail-closed guards for
overlength notes, missing linked evidence and conflicting locations were
exercised. Disposable verification databases were dropped. The local
`smartdroneinspection` database was not changed because its V38 Flyway history
is inconsistent with its schema.

Verification status: backend compile and focused source/domain tests passed.
The full backend `./mvnw -B verify` attempt did not pass because Docker is
unavailable (Testcontainers errors; no assertion failures were established).
Frontend build and lint passed, as did 25 focused report UI tests. Mobile
format, analyze and 49 tests passed. `WF3-012` remains Pending; no Report 5 case
or statistics are promoted by these checks. Reviewer credential qualification
remains unvalidated at runtime.

### MF3-12/13 no-repair rationale UI regression — 2026-10-22 (superseded behavior)

The earlier workflow required an Organization Manager rationale when no repair work was selected. The simplified target removes the inspection-level rationale, uses `inspections.status` for the aggregate outcome and records the reviewer/selection/status transition in `audit_events`. The historical page-level test and its 2026-10-22 execution evidence remain unchanged as evidence for the earlier behavior; they do not verify the current target. `WF3-012` remains Pending.

### MF3-12/13 end-to-end walkthrough and the defects it fixed — 2026-10-17

The MF3 chain was then executed end to end through the running web client and the
API against the merged source, on the rebuilt stack with `V30` and `V31` applied.
Observed and verified: MF3-06a confirmation recorded the actor, time and snapshot
and created no report version; the automated-draft failure produced no partial
version and no automatic fallback; the manual draft created a version without LLM
provenance; the pre-confirmation draft was refused with `REPORT_SNAPSHOT_STALE`;
review kept approval disabled and reported `Decide every proposed finding before
approving the report` until every proposal had an attributable decision;
publication ended at `REPORT_PUBLISHED` with the stored checksummed PDF and an
empty handed-off finding list; the MF3-12 outcome and the MF3-13 handoff moved the
inspection to `REPAIR_PENDING` with exactly the work-required finding handed off
and no `maintenance_work_orders` row created. Negative paths: repeating the
handoff returned `409 CORRECTIVE_HANDOFF_ALREADY_COMPLETED`, repeating a recorded
outcome `409 CORRECTIVE_ACTION_ALREADY_RECORDED`, `no-corrective-work` with
official findings `409 CORRECTIVE_ACTION_REVIEW_REQUIRED`, the handoff with an
incomplete outcome set `409 CORRECTIVE_ACTION_REVIEW_INCOMPLETE`, and a priority
on a no-action outcome `400`.

Four defects the walkthrough exposed were fixed in this round:

1. `usePublishReportVersion` invalidated only the version list, so the MF3-12
   panel stayed hidden after publishing until a manual reload even though the page
   told the reviewer to record outcomes. The hook now invalidates the workflow
   state too, and `ReportDetailPage.test.tsx` covers the publish-to-panel
   transition (it fails without the fix).
2. The web container's `client_max_body_size` capped requests at 10 MB while the
   backend allows 10 MB per file / 20 MB per request, so an oversize upload was
   answered with an nginx HTML page and the client showed
   `Request failed with status code 413`. The proxy bound now matches the backend
   request bound, so the backend's structured 413 reaches the user.
3. The `V30` cutover backfill attributed a pre-publication reviewer disposition as
   the post-publication outcome of a report published later, and the reviewer
   could not change it. `V31__mf3_corrective_outcome_follows_publication.sql`
   clears those outcomes, publication clears an outcome recorded before the new
   version, and
   `InspectionReportApiIntegrationTest.publishingClearsACorrectiveOutcomeRecordedBeforeThePublication`
   covers it.
4. The per-image chip counted AI candidates but read `No findings found`, which
   contradicted the finding actually linked to that image. It now reads
   `No detected defects`.

Executed after the fixes: backend `./mvnw -B verify` passed 651 tests, 0
failures/errors/skips, with the Spotless, JaCoCo and Modulith checks met;
frontend `npm test -- --run` passed 55 files / 376 tests; `npm run lint` and
`npm run build` exited 0. `WF3-012` still stays Pending: the all-no-action close
(`COMPLETED` with no handed-off findings) and the explicitly confirmed
empty-findings no-repair close were not executed.

### Findings CRUD, author withdrawal, and review return reasons — 2026-10-17

While a report is not submitted, the assigned Inspector can perform full CRUD on findings and retire captures:
- `PUT /api/v1/inspections/{id}/findings/{findingId}` updates finding details and re-links active evidence.
- `DELETE /api/v1/inspections/{id}/findings/{findingId}` soft-deletes a finding with an attributable deletion reason (`deleted_at`, `deleted_by_user_id`, `deletion_reason` stored for audit; excluded from active reads via `@SQLRestriction`). If linked to an AI candidate, the candidate reopens to `PENDING`.
- `POST /api/v1/inspections/{id}/evidence/{evidenceId}/retire` marks a capture retired with an attributable reason (`retired_at`, `retired_by_user_id`, `retirement_reason`) without deleting original bytes or metadata. A capture cannot be retired while an active finding cites it.
- `POST /api/v1/inspections/{id}/report/versions/{versionId}/withdraw` lets the author withdraw a submitted report before any reviewer action, returning it to author revision with `withdrawn_by_user_id`, `withdrawn_at`, and `withdrawal_reason` stored. Evidence and findings remain intact.
- Reviewer return now requires `reasonType`: `TEXT_REVISION` (leaves findings decisions intact) or `FINDINGS_REVISION` (reopens findings, clears live reviewer decisions, and invalidates confirmation so the Inspector can revise findings and re-draft).
- V32 forward migration adds the audit and return columns (`V32__mf3_findings_correction_and_author_withdrawal.sql`).
- Executed verification: backend `./mvnw -B verify` passed 663 tests, 0 failures/errors/skips; frontend `npm test -- --run` passed 55 files / 384 tests, lint and build clean. Live walkthrough verified finding creation, in-place edit, soft-delete with audit reason, capture retirement with "Retired — audit copy" chip, and withdrawal / return reason handling.

## Feature sheet summary

Values for the `Feature 6` summary block (`A2:E8` in the workbook).
The template reads these back by formula, so an export needs them
recorded here.

| Cell | Label | Value |
| --- | --- | --- |
| `B2` | Feature | Inspection Report Drafting, Review and Publication — MF3 |
| `B3` | Test requirement | Verifies Inspector-authored coverage/limitations, manual or explicitly requested AI-assisted drafting, author verification, independent review, return, approval and immutable publication of the version with its checksummed PDF; after publication, selected findings are forwarded per finding and inspection status records the overall outcome. |

### Bilingual report drafting and PDF rendering — 2026-10-22

The drafting context carries the request locale, so the AI narrative is drafted
in the requested language while the supplied source values are preserved
verbatim: the prompt explicitly instructs the model not to translate or
paraphrase an Inspector-authored note, finding text or answer. The recorded
prompt version moved to `mf3-report-v3-bilingual` to mark that behaviour.

The generated PDF renders its system-managed labels, headings and page furniture
in the requested locale. An authored narrative section, a finding text and a
recorded note are embedded unchanged, so switching the locale cannot alter a
published observation. `ReportDraftClientTest` asserts the Vietnamese prompt and
the preserved source values; `ReportHtmlTemplateLocalizationTest` asserts the
Vietnamese PDF labels and the unchanged `Normal wear` note and authored summary.

Verification in this task: backend `./mvnw -B clean verify` passed, including the
localized prompt, PDF and report API tests. No Report 5 case status changed; the
live drafting-provider path remains unexecuted as recorded above.
