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
They do **not** assert:

- **Report 3 §3.7.2 "Required Inspection Report Content"** — the required
  content sections of a released report.
- **Report 3 §3.7.3 "LLM Safeguards"** — the drafting safeguards, including
  numeric-table sourcing rules and handling of untrusted evidence metadata.

These are open gaps within an otherwise-verified feature and are recorded here
so a reader does not infer that a `Passed` FE-06 covers the whole of §3.7.

## Current cases

| Test Case ID | Test Case Description | Test Case Procedure | Expected Results | Pre-conditions | Round 1 | Test date | Tester | Round 2 | Test date | Tester | Round 3 | Test date | Tester | Note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| WF3-005 | AI Vision candidates and the inspection-report draft are verified by the author Inspector before ORG_ADMIN publication. | Provide eligible confirmed evidence; attempt analysis before the Inspector accepts the evidence set; confirm analysis is refused and manual finding entry still works; author a draft (automated where configured, otherwise the manual structured draft); verify and submit as the author Inspector; attempt a return without a reason; return with a reason; attempt to review one's own report; resubmit and approve as a qualified ORG_ADMIN. | Only human-confirmed findings enter official outputs; the author Inspector's authorship and the qualified ORG_ADMIN's independent approval are recorded; unverified draft text cannot be published; a failed or unconfigured drafting service still permits a structured manual draft under the same review gates. | Assigned inspection with an accepted evidence quality decision and a qualified reviewer in the same organization. | Passed | 2026-10-08 | Claude Code (automated) | Pending |  |  | Pending |  |  | Verified by `InspectionReportApiIntegrationTest` (14 tests) and, on 2026-10-11, `InspectionReportDraftingApiIntegrationTest` (5 tests): `draftingProposesSectionValuesThatTheAuthorCanReadBack`, `draftingRecordsItsProvenanceOnTheVersion`, `draftingNeverAltersAReviewedFinding`, `aFailedGenerationLeavesNoVersionAndReportsTheFailure`, and `theManualDraftRemainsAvailableWhenDraftingIsUnconfigured`. The section-authoring path is exercised in `InspectionReportSectionsApiIntegrationTest`. `ReportDraftClientTest` (6 tests) covers the section-proposal prompt, absent-section handling and the failure path. Full run 2026-10-11 within the backend suite of 362 passing tests. The live external LLM-provider happy path remains unexecuted; the automated path is stubbed with a deterministic `ReportDraftPort`. |
| WF3-006 | MF3 publishes an immutable approved inspection report version **and its PDF deliverable** and hands repair-required findings to MF4. | Complete the MF3 review; publish the approved version; confirm publication stored a PDF artefact and recorded its object key and SHA-256; download the artefact and confirm it is a readable PDF carrying the report reference; confirm the recorded checksum matches the stored bytes; inspect the version metadata (author, reviewer, timestamps, evidence snapshot hash); confirm a published version is never edited; publish the same version a second time; publish a later version and confirm the earlier version's artefact is untouched and superseded; publish when the inspection is in `REPAIR_PENDING` (correction version) and verify publication succeeds; verify preview renders confirmed findings and attached defect photographs; verify only repair-required findings are handed to MF4 and a no-repair outcome does not create an empty work order. | The approved version is immutable, traceable and carries a retained, checksum-verifiable PDF deliverable; confirmed defect photographs are embedded directly within their finding cards in both the web UI and Section 6 of the PDF; publication does not complete without the stored artefact; a repeat publish of the same version is refused; publishing a correction from `REPAIR_PENDING` succeeds and supersedes the prior published version; only repair-required findings become MF4 work orders; a no-repair outcome closes the inspection without inventing corrective scope. | An approved MF3 report version and confirmed findings exist. | Passed | 2026-10-11 | Claude Code (automated) | Pending |  |  | Pending |  |  | **Promoted from `Pending` to `Passed` on 2026-10-11** now that the deliverable assertions actually run. New `InspectionReportSectionsApiIntegrationTest` (19 tests) covers: `publishingStoresTheDocumentAndRecordsAChecksumThatMatchesTheStoredBytes`, `thePublishedDocumentCanBeDownloadedWithTheReportReferenceInTheFileName`, `publishingAFurtherVersionDoesNotOverwriteTheEarlierArtefact` (asserting `SUPERSEDED` on prior version without SQL overrides), `aRepeatPublishIsRefusedAndLeavesTheFirstArtefactIntact`, `downloadingAVersionWithNoStoredDocumentIsNotFoundRatherThanAServerError`, `aCrossOrganizationDownloadIsRefused`, `previewRendersConfirmedFindingsAndAttachedEvidence`, and `thePublishedDocumentCarriesSelectableTextAndTheAuthoredSections` (reads the text back out of the PDF with PDFBox to prove the report is selectable text, not an image). Previously executed immutability and MF4 hand-off assertions re-confirmed in `InspectionReportApiIntegrationTest` (14 tests). Full run 2026-10-11 within the backend suite of 363 passing tests (`./mvnw.cmd verify`); coverage gate met, Modulith boundary clean. |

## Feature sheet summary

Values for the `Feature 6` summary block (`A2:E8` in the workbook).
The template reads these back by formula, so an export needs them
recorded here.

| Cell | Label | Value |
| --- | --- | --- |
| `B2` | Feature | Inspection Report Drafting, Review and Publication — MF3 |
| `B3` | Test requirement | Verifies section authoring, author verification, independent review, return, approval, and immutable publication of the version together with its checksummed PDF deliverable, including the manual structured draft used when drafting is unavailable. |
