# FE-06: Inspection Report Drafting, Review and Publication — MF3

Report 3 §3.7 titles this feature "Inspection Report Drafting, Review and
Publication". The filename retains the earlier "inspection report / approval"
wording; the filename is stable, the scope is Report 3's.

## Scope baseline

The report author is the assigned `INSPECTOR`; a same-organization `ORG_ADMIN`
who is not the author reviews and publishes. Runtime review enforces role,
organization, active-account and separation-of-duties checks, but it does not
validate reviewer credentials: professional qualification is an explicit
implementation gap and runtime review must not be described as qualified.
There is no Client acceptance step and no separate Manager release in the
current four-role system, so the earlier five-role review/release/acceptance
case does not apply and has been removed from this report.

The model drafts; humans decide. A draft is only generated from authorized
inspection sources, the author must verify what was generated, and a reviewer
who is not the author approves. Nothing publishes on a timer, and a published
version is immutable.

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

The added aggregate-confirmation and separate draft-choice requirement is tracked
as `WF3-011`. The post-publication corrective-outcome and handoff requirement is
tracked as `WF3-012`. Both remain Pending until their complete backend/UI
scenarios are run; component-level green tests are not represented as execution
of either case.

| Test Case ID | Test Case Description | Test Case Procedure | Expected Results | Pre-conditions | Round 1 | Test date | Tester | Round 2 | Test date | Tester | Round 3 | Test date | Tester | Note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| WF3-005 | AI Vision candidates and the inspection-report draft are verified by the author Inspector before ORG_ADMIN publication. | Provide eligible confirmed evidence; attempt analysis before the Inspector accepts the evidence set; confirm analysis is refused and manual finding entry still works; author a draft (automated where configured, otherwise the manual structured draft); verify and submit as the author Inspector; attempt a return without a reason; return with a reason; attempt to review one's own report; resubmit and approve as an independent ORG_ADMIN. | Only human-confirmed findings enter official outputs; the author Inspector's authorship and the independent ORG_ADMIN's approval are recorded (runtime does not validate reviewer credentials); unverified draft text cannot be published; a failed or unconfigured drafting service still permits a structured manual draft under the same review gates. | Assigned inspection with an accepted evidence quality decision and an independent active ORG_ADMIN in the same organization. | Passed | 2026-10-08 | Claude Code (automated) | Pending |  |  | Pending |  |  | Historical verification (2026-10-08 through 2026-10-11): `InspectionReportApiIntegrationTest` (14 tests at that time) and, on 2026-10-11, `InspectionReportDraftingApiIntegrationTest` (5 tests at that time): `draftingProposesSectionValuesThatTheAuthorCanReadBack`, `draftingRecordsItsProvenanceOnTheVersion`, `draftingNeverAltersAReviewedFinding`, `aFailedGenerationLeavesNoVersionAndReportsTheFailure`, and `theManualDraftRemainsAvailableWhenDraftingIsUnconfigured`. The section-authoring path is exercised in `InspectionReportSectionsApiIntegrationTest`. `ReportDraftClientTest` (6 tests) covers the section-proposal prompt, absent-section handling and the failure path. Full run 2026-10-11 within the backend suite of 362 passing tests. A live external vision-model walkthrough was recorded on 2026-10-12 (three PENDING candidates returned; see historical verification row in `test-statistics.md`); this does not verify the report-drafting LLM provider. The automated report-drafting path uses a deterministic `ReportDraftPort`; the live drafting-provider happy path remains unexecuted. The 2026-10-12 web split keeps the backend contract unchanged: the Report stage generates the MF3-07 draft behind the existing ACCEPTED gate (409 otherwise), keeps the manual narrative/disclosure seed form, and carries the version-gated "Open the report document" link to `reports/:inspectionId`. Covered by frontend `InspectionDraftPage.test.tsx` (generation blocked until accepted; manual seed payload; report link disabled until a version exists). **MF3-04 enforcement added 2026-10-13:** `ReportService.verifyVersion` and `submitVersion` compare the current evidence checksum hash with the version snapshot; mismatch returns 409 `REPORT_SNAPSHOT_STALE`. **Passed in backend PR #69 CI run 38325774461:** `./mvnw -B verify` ran 491 tests, 0 failures/errors/skips; `evidenceAddedAfterTheDraftMakesVerificationStale` and `evidenceAddedAfterVerificationMakesSubmitStale` executed under Testcontainers. The separate local `mvn.cmd -o verify` attempt remains recorded as Docker-blocked (263 environment errors) in `test-statistics.md`. **Current source counts are larger — `InspectionReportApiIntegrationTest` 26, `InspectionReportDraftingApiIntegrationTest` 10, `InspectionReportSectionsApiIntegrationTest` 22 (counted from the test sources, not a run record) — and the current source's MF3 suites passed the executed 2026-10-16 runs (81 targeted tests; 650-test full `.\mvnw.cmd verify` gate), but the case remains Pending until the complete end-to-end scenario executes.** |
| WF3-006 | The approved report version is immutable and source-traceable, publication stores its PDF deliverable and records the checksum, and only reviewer-confirmed findings with an MF3-12 corrective-work outcome are handed to MF4. | Publish an approved report; verify stored PDF/checksum and immutable version; confirm only reviewer-confirmed/modified findings with a corrective-work outcome are handed off. Supplementary evidence-location regression: preview a report with linked confirmed finding and evidence, then inspect the PDF evidence-register row and finding details. | The published artifact is retrievable/checksum-verifiable and immutable; only findings with an explicit corrective-work outcome enter corrective work; evidence register displays linked official component/location when capture location is absent; finding details retain their location. | Published MF3 review artifacts; report preview fixtures with linked evidence and a reviewer-confirmed finding with component/location. | Passed | 2026-10-11 | Claude Code (automated) | Pending |  |  | Pending |  |  | Historical result retained. **The current source separates MF3-12/13 from publication:** publish now ends at `REPORT_PUBLISHED`, and the corrective outcome plus recorded handoff happen afterwards, tracked by `WF3-012` (Pending). The executed evidence for this case was recorded on the pre-change flow, so the `Passed` status refers to that run; the current source's MF3 suites passed the executed 2026-10-16 runs (81 targeted tests; 650-test full `.\mvnw.cmd verify` gate), but the case remains Pending until the complete end-to-end scenario executes. Supplementary evidence-location PDF regression passed 2026-10-13; this does not establish full §3.7.2 compliance. |
| WF3-011 | Inspector confirms the resolved findings set before separately choosing AI-assisted or manual report authoring. | Exercise pending candidates, resolved candidates, proposed/manual findings, explicit no-findings acknowledgment, confirmation and separate draft choice; mutate evidence/findings after confirmation; attempt approval/publication with an undecided proposal. | Pending candidates and unacknowledged empty scope block confirmation; confirmation advances workflow only and creates no report/version or AI call; both draft methods require a current confirmation; material edits reopen Findings and require reconfirmation; ORG_ADMIN must decide every proposal before report approval/publication; only reviewer-confirmed findings with an MF3-12 corrective-work outcome are handed to MF4 (see `WF3-012`). | Assigned Inspector; completed inspection; accepted evidence-quality decision; Testcontainers/PostgreSQL and stubbed inference/draft ports; web UI/API tests. | Pending |  |  | Pending |  |  | Pending |  |  | New case for the MF3 gate and alternatives. Keep Pending until the complete backend and frontend scenario has executed; focused component tests alone are not this case. |
| WF3-012 | After publication, the Organization Admin records a corrective-action outcome for every confirmed/modified finding and the System records the MF3-13 handoff to MF4 (or a reasoned no-repair close) without creating a work order. | Publish an approved report and confirm the inspection reaches `REPORT_PUBLISHED` with an unchanged PDF; attempt the corrective handoff before any outcome (expect `409 CORRECTIVE_ACTION_REVIEW_INCOMPLETE`); record a work-required outcome with priority and due date plus a no-action outcome with rationale; attempt a priority on a no-action outcome (expect rejection); repeat a recorded outcome (expect `409 CORRECTIVE_ACTION_ALREADY_RECORDED`); complete the handoff (expect `REPAIR_PENDING` and only work-required finding IDs); repeat the handoff (expect `409 CORRECTIVE_HANDOFF_ALREADY_COMPLETED`); for a scope whose official findings are all recorded as no-action, complete the handoff (expect `COMPLETED` with no handed-off finding IDs); for a scope with an empty confirmed findings set, record the no-repair outcome with rationale and confirm `COMPLETED`; attempt `no-corrective-work` when official findings exist (expect `409 CORRECTIVE_ACTION_REVIEW_REQUIRED`). | MF3-11 publication ends at `REPORT_PUBLISHED`; each official finding gets one attributable MF3-12 outcome (work-required requires priority; due date optional; no-action carries neither); MF3-13 handoff records actor/time and marks only work-required findings for MF4, completing the inspection when none require work; a scope with no official findings closes through `no-corrective-work` with a recorded rationale; no MF4 work order is created; the published PDF is never modified. | Published MF3 report with confirmed/modified findings (plus an empty-findings variant); active independent ORG_ADMIN; PostgreSQL via Testcontainers; current backend source. | Pending |  |  | Pending |  |  | Pending |  |  | New case for MF3-12/13. Current backend source contains assertions for this path (`InspectionReportApiIntegrationTest`: publish-then-outcome, no-repair durability, handoff completeness and work-required handoff). The current source's MF3 suites passed the executed 2026-10-16 runs (81 targeted tests; 650-test full `.\mvnw.cmd verify` gate), but the case remains Pending until the complete end-to-end scenario executes. |


## Targeted report-content regression — 2026-10-13

The PDF preview regression in `InspectionReportSectionsApiIntegrationTest.previewRendersConfirmedFindingsAndAttachedEvidence` passed: a confirmed finding's component/location is rendered in its linked evidence-register row, and the finding section retains the same location. Frontend `ReportDerivedSections.test.tsx` passed the GPS-precedence, official-finding fallback, and pending-finding exclusion cases. Live authenticated UI verification also passed: inspection `78b9c412-a04d-43c6-abbd-ef54d5a58932`, version v5, shows `Pier 2 north face` both on the confirmed finding and on its linked `spalling.jpg` evidence row. This remains narrow evidence-location coverage only; the broader §3.7.2 report-content verification gap stays open.

### WF3 drafting-input follow-up — 2026-10-14

The focused draft-context slice now passes inspection objective/scope/component scope/criteria, accepted evidence metadata, inspection-scoped AI candidate and field-session records, and the latest Inspector-recorded evidence-quality decision (shot-list comparison and any limitation). It uses only the latest decision: a newer non-accepted decision blocks drafting and is not replaced by an older acceptance. Prompt rules keep official findings separate from advisory candidates and field-session records separate from proof of aircraft operation; planned dates and assigned Drone references remain labelled as planning data. No checklist-answer or Inspector-observation source was identified, so those values are not supplied. `ReportDraftClientTest` passed 6 tests and the Testcontainers-backed `InspectionReportDraftingApiIntegrationTest` passed 9 tests. These tests do not establish full §3.7.1–§3.7.3 compliance.

### Disposable Inspector walkthrough — 2026-10-14

Against local Docker services rebuilt from the current WF3 sources, an Inspector used the UI on disposable inspection `2fa8fd35-285a-43c4-a616-69d05cc8250d` (`FIELD_COMPLETED`). Six synthetic local JPG fixtures uploaded successfully; the Inspector recorded an explicit test-only coverage comparison and accepted the evidence set. Automatic detection stored 17 `PENDING` candidates across all six images; zero official findings and zero field sessions existed. The final analysis request appeared aborted in the browser when navigating away, but a read-only DB check confirmed candidate records for all six images, including three for `coating-blister.jpg`.

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

### MF3-12/13 post-publication correction and handoff — 2026-10-16

Report 3 MF3-12/MF3-13 are now specified and coded as post-publication
steps, pending verification (see the verification status below): publication
ends at `REPORT_PUBLISHED` with the stored, checksummed PDF;
the Organization Admin then records one attributable corrective-action outcome
per confirmed/modified finding (`correctiveActionRequired` with a required
rationale, a required priority for work-required outcomes and an optional due
date) or an explicit reasoned no-repair outcome; the handoff records the actor
and moves the inspection to `REPAIR_PENDING` when work is required, or to
`COMPLETED` when every official finding was recorded as no-action. An
explicitly confirmed empty findings set closes to `COMPLETED` through
`no-corrective-work` with a recorded rationale. The
handoff does not create an MF4 work order — that workflow is not implemented.
`V30__mf3_corrective_action_and_decision_revision.sql` carries the schema.

Verification status: the backend paths executed green on 2026-10-16 — the five
named MF3 suites passed 81 tests (12/11/26/10/22; `InspectionReportApiIntegrationTest`
contains the 26 MF3-12/13 assertions) and the full `.\mvnw.cmd verify` gate
passed 650 tests with the Spotless, JaCoCo and Modulith checks met. Frontend
verification of the MF3-12 controls passed on 2026-10-17 (focused suite 18/18;
full suite 55 files / 375 tests; lint and build clean).
`WF3-012` remains Pending until the complete end-to-end scenario is executed.
Reviewer credential qualification remains unvalidated at runtime and is reported
as a gap rather than assumed.

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

## Feature sheet summary

Values for the `Feature 6` summary block (`A2:E8` in the workbook).
The template reads these back by formula, so an export needs them
recorded here.

| Cell | Label | Value |
| --- | --- | --- |
| `B2` | Feature | Inspection Report Drafting, Review and Publication — MF3 |
| `B3` | Test requirement | Verifies section authoring, author verification, independent review, return, approval, and immutable publication of the version together with its checksummed PDF deliverable, including the manual structured draft used when drafting is unavailable, and the post-publication corrective-action outcome and recorded MF4 handoff or reasoned no-repair close. |
