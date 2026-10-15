# FE-06: Inspection Report Drafting, Review and Publication — MF3

Report 3 §3.7 titles this feature "Inspection Report Drafting, Review and
Publication". The filename retains the earlier "inspection report / approval"
wording; the filename is stable, the scope is Report 3's.

## Scope baseline

The report author is the assigned `INSPECTOR`; a qualified same-organization
`ORG_ADMIN` who is not the author reviews and publishes. There is no Client
acceptance step and no separate Manager release in the current four-role
system, so the earlier five-role review/release/acceptance case does not apply
and has been removed from this report.

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

These remain open gaps; the `Passed` FE-06 cases do not establish all of §3.7.

## Current cases

The added aggregate-confirmation and separate draft-choice requirement is tracked
as `WF3-011`. It remains Pending until the complete backend/UI scenario is run;
component-level green tests are not represented as execution of that case.

| Test Case ID | Test Case Description | Test Case Procedure | Expected Results | Pre-conditions | Round 1 | Test date | Tester | Round 2 | Test date | Tester | Round 3 | Test date | Tester | Note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| WF3-005 | AI Vision candidates and the inspection-report draft are verified by the author Inspector before ORG_ADMIN publication. | Provide eligible confirmed evidence; attempt analysis before the Inspector accepts the evidence set; confirm analysis is refused and manual finding entry still works; author a draft (automated where configured, otherwise the manual structured draft); verify and submit as the author Inspector; attempt a return without a reason; return with a reason; attempt to review one's own report; resubmit and approve as a qualified ORG_ADMIN. | Only human-confirmed findings enter official outputs; the author Inspector's authorship and the qualified ORG_ADMIN's independent approval are recorded; unverified draft text cannot be published; a failed or unconfigured drafting service still permits a structured manual draft under the same review gates. | Assigned inspection with an accepted evidence quality decision and a qualified reviewer in the same organization. | Passed | 2026-10-08 | Claude Code (automated) | Pending |  |  | Pending |  |  | Verified by `InspectionReportApiIntegrationTest` (14 tests) and, on 2026-10-11, `InspectionReportDraftingApiIntegrationTest` (5 tests): `draftingProposesSectionValuesThatTheAuthorCanReadBack`, `draftingRecordsItsProvenanceOnTheVersion`, `draftingNeverAltersAReviewedFinding`, `aFailedGenerationLeavesNoVersionAndReportsTheFailure`, and `theManualDraftRemainsAvailableWhenDraftingIsUnconfigured`. The section-authoring path is exercised in `InspectionReportSectionsApiIntegrationTest`. `ReportDraftClientTest` (6 tests) covers the section-proposal prompt, absent-section handling and the failure path. Full run 2026-10-11 within the backend suite of 362 passing tests. A live external vision-model walkthrough was recorded on 2026-10-12 (three PENDING candidates returned; see historical verification row in `test-statistics.md`); this does not verify the report-drafting LLM provider. The automated report-drafting path uses a deterministic `ReportDraftPort`; the live drafting-provider happy path remains unexecuted. The 2026-10-12 web split keeps the backend contract unchanged: the Report stage generates the MF3-07 draft behind the existing ACCEPTED gate (409 otherwise), keeps the manual narrative/disclosure seed form, and carries the version-gated "Open the report document" link to `reports/:inspectionId`. Covered by frontend `InspectionDraftPage.test.tsx` (generation blocked until accepted; manual seed payload; report link disabled until a version exists). **MF3-04 enforcement added 2026-10-13:** `ReportService.verifyVersion` and `submitVersion` compare the current evidence checksum hash with the version snapshot; mismatch returns 409 `REPORT_SNAPSHOT_STALE`. **Passed in backend PR #69 CI run 38325774461:** `./mvnw -B verify` ran 491 tests, 0 failures/errors/skips; `evidenceAddedAfterTheDraftMakesVerificationStale` and `evidenceAddedAfterVerificationMakesSubmitStale` executed under Testcontainers. The separate local `mvn.cmd -o verify` attempt remains recorded as Docker-blocked (263 environment errors) in `test-statistics.md`. |
| WF3-006 | The approved report version is immutable and source-traceable, publication stores its PDF deliverable and records the checksum, and only independently confirmed repair-required findings are handed to MF4. | Publish an approved report; verify stored PDF/checksum and immutable version; confirm only reviewer-confirmed/modified repair-required findings are handed off. Supplementary evidence-location regression: preview a report with linked confirmed finding and evidence, then inspect the PDF evidence-register row and finding details. | The published artifact is retrievable/checksum-verifiable and immutable; only independently confirmed repair-required findings enter corrective work; evidence register displays linked official component/location when capture location is absent; finding details retain their location. | Published MF3 review artifacts; report preview fixtures with linked evidence and a reviewer-confirmed finding with component/location. | Passed | 2026-10-11 | Claude Code (automated) | Pending |  |  | Pending |  |  | Existing WF3-006 publication/immutability result retained. Supplementary evidence-location PDF regression passed 2026-10-13; this does not establish full §3.7.2 compliance. |
| WF3-011 | Inspector confirms the resolved findings set before separately choosing AI-assisted or manual report authoring. | Exercise pending candidates, resolved candidates, proposed/manual findings, explicit no-findings acknowledgment, confirmation and separate draft choice; mutate evidence/findings after confirmation; attempt approval/publication with an undecided proposal. | Pending candidates and unacknowledged empty scope block confirmation; confirmation advances workflow only and creates no report/version or AI call; both draft methods require a current confirmation; material edits reopen Findings and require reconfirmation; ORG_ADMIN must decide every proposal before report approval/publication; only independently confirmed repair-required findings enter MF4. | Assigned Inspector; completed inspection; accepted evidence-quality decision; Testcontainers/PostgreSQL and stubbed inference/draft ports; web UI/API tests. | Pending |  |  | Pending |  |  | Pending |  |  | New case for the MF3 gate and alternatives. Keep Pending until the complete backend and frontend scenario has executed; focused component tests alone are not this case. |


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

- `./mvnw.cmd -B verify` — **645 tests, 0 failures, 0 errors, 0 skipped; BUILD SUCCESS.** Includes
  the new `InspectionReportSectionsApiIntegrationTest.previewRendersAnInspectorConfirmedFindingThatHasNoReviewerDecisionYet`
  (observed red first: the PDF read "6. Confirmed findings / No confirmed findings were recorded for
  this version") and `previewOmitsAFindingTheReviewerRejected`.
- Frontend `npm test -- --run` — 54 files, **358 tests passed**; `npm run lint` unchanged at the
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

## Feature sheet summary

Values for the `Feature 6` summary block (`A2:E8` in the workbook).
The template reads these back by formula, so an export needs them
recorded here.

| Cell | Label | Value |
| --- | --- | --- |
| `B2` | Feature | Inspection Report Drafting, Review and Publication — MF3 |
| `B3` | Test requirement | Verifies section authoring, author verification, independent review, return, approval, and immutable publication of the version together with its checksummed PDF deliverable, including the manual structured draft used when drafting is unavailable. |
