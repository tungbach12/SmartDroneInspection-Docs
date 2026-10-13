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
| WF3-005 | AI Vision candidates and the inspection-report draft are verified by the author Inspector before ORG_ADMIN publication. | Provide eligible confirmed evidence; attempt analysis before the Inspector accepts the evidence set; confirm analysis is refused and manual finding entry still works; author a draft (automated where configured, otherwise the manual structured draft); verify and submit as the author Inspector; attempt a return without a reason; return with a reason; attempt to review one's own report; resubmit and approve as a qualified ORG_ADMIN. | Only human-confirmed findings enter official outputs; the author Inspector's authorship and the qualified ORG_ADMIN's independent approval are recorded; unverified draft text cannot be published; a failed or unconfigured drafting service still permits a structured manual draft under the same review gates. | Assigned inspection with an accepted evidence quality decision and a qualified reviewer in the same organization. | Passed | 2026-10-08 | Claude Code (automated) | Pending |  |  | Pending |  |  | Verified by `InspectionReportApiIntegrationTest` (14 tests) and, on 2026-10-11, `InspectionReportDraftingApiIntegrationTest` (5 tests): `draftingProposesSectionValuesThatTheAuthorCanReadBack`, `draftingRecordsItsProvenanceOnTheVersion`, `draftingNeverAltersAReviewedFinding`, `aFailedGenerationLeavesNoVersionAndReportsTheFailure`, and `theManualDraftRemainsAvailableWhenDraftingIsUnconfigured`. The section-authoring path is exercised in `InspectionReportSectionsApiIntegrationTest`. `ReportDraftClientTest` (6 tests) covers the section-proposal prompt, absent-section handling and the failure path. Full run 2026-10-11 within the backend suite of 362 passing tests. A live external vision-model walkthrough was recorded on 2026-10-12 (three PENDING candidates returned; see historical verification row in `test-statistics.md`); this does not verify the report-drafting LLM provider. The automated report-drafting path uses a deterministic `ReportDraftPort`; the live drafting-provider happy path remains unexecuted. The 2026-10-12 web split keeps the backend contract unchanged: the Report stage generates the MF3-07 draft behind the existing ACCEPTED gate (409 otherwise), keeps the manual narrative/disclosure seed form, and carries the version-gated "Open the report document" link to `reports/:inspectionId`. Covered by frontend `InspectionDraftPage.test.tsx` (generation blocked until accepted; manual seed payload; report link disabled until a version exists). **MF3-04 enforcement added 2026-10-13:** `ReportService.verifyVersion` and `submitVersion` compare the current evidence checksum hash with the version snapshot; mismatch returns 409 `REPORT_SNAPSHOT_STALE`. **Passed in backend PR #69 CI run 38325774461:** `./mvnw -B verify` ran 491 tests, 0 failures/errors/skips; `evidenceAddedAfterTheDraftMakesVerificationStale` and `evidenceAddedAfterVerificationMakesSubmitStale` executed under Testcontainers. The separate local `mvn.cmd -o verify` attempt remains recorded as Docker-blocked (263 environment errors) in `test-statistics.md`. |

## Feature sheet summary

Values for the `Feature 6` summary block (`A2:E8` in the workbook).
The template reads these back by formula, so an export needs them
recorded here.

| Cell | Label | Value |
| --- | --- | --- |
| `B2` | Feature | Inspection Report Drafting, Review and Publication — MF3 |
| `B3` | Test requirement | Verifies section authoring, author verification, independent review, return, approval, and immutable publication of the version together with its checksummed PDF deliverable, including the manual structured draft used when drafting is unavailable. |
