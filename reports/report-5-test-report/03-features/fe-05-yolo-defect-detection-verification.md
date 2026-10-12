# FE-05: AI Vision Candidates and Human Finding Decisions

Report 3 §3.6 titles this feature "AI Vision Candidates and Human Finding
Decisions". The filename retains the earlier "YOLO / defect detection
verification" wording; the filename is stable, the scope is Report 3's. Report 3
names no specific detection vendor or model family.

## Scope baseline

The `inspections` module implements the MF3 finding slice of FE-05: advisory AI
candidates that stay separate from human-verified findings, a manual finding
path that remains available when inference is refused or fails, and the
qualified reviewer's decision on a finding. Report 3 requires that manual entry
survives an AI outage, so the manual path is not conditional on AI
availability.

Detection is served by an optional OpenAI-compatible vision adapter behind the
inspections-owned `AiInferencePort`, with a mutually exclusive YOLO alternative.
Credentials are environment-only. Both adapters are implementation choices
behind the requirement, not part of it.

## Feature sheet summary

Values for the `Feature 5` summary block (`A2:E8` in the workbook). The
exporter maps this file to the matching SRS feature sheet.

| Cell | Label | Value |
| --- | --- | --- |
| `B2` | Feature | AI Vision Candidates and Human Finding Decisions |
| `B3` | Test requirement | Verifies human review of advisory AI candidates and manual findings; unconfirmed detections do not enter official findings. |

## Current case

| Test Case ID | Test Case Description | Test Case Procedure | Expected Results | Pre-conditions | Round 1 | Test date | Tester | Round 2 | Test date | Tester | Round 3 | Test date | Tester | Note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| WF3-003 | Inspector verifies AI candidates or records a manual finding. | Request analysis before the Inspector accepts the evidence set; analyze a representative accepted image; verify its returned candidate provenance, confidence, normalized box, and pending status; re-analyze the same accepted image and confirm the candidate set is unchanged; attempt analysis as a different Inspector; confirm a candidate through the Inspector workspace and check the created finding is still undecided; record a manual finding with prose measurement; sign in as a qualified ORG_ADMIN in the same organization and record the reviewer's decision on that finding; confirm the Inspector is not offered the reviewer decision. | Analysis is refused until the Inspector accepts the evidence; valid model detections are persisted only as `PENDING`; re-analysis of an already analysed image returns the existing candidates and creates no duplicate; out-of-scope Inspectors are refused; a confirmed candidate creates a `VerifiedFinding` whose `decision` is still null, because MF3-06 records a recommendation and not the official decision; a manual finding is available without analysis; a finding is official only after the qualified reviewer's `CONFIRMED` or `MODIFIED` decision, which stamps the deciding reviewer and time. | An assigned `FIELD_COMPLETED` inspection, accepted image evidence, PostgreSQL, and an authorized Inspector and ORG_ADMIN in the same organization. | Passed | 2026-10-12 | Claude Code (automated) | Pending |  |  | Pending |  |  | Verified with `InspectionReportApiIntegrationTest.analysisIsRefusedUntilTheInspectorAcceptsTheEvidence`, `analysisRequiresAssignmentAndAcceptedEvidenceAndPersistsOnlyPendingCandidates`, `reAnalysingTheSameEvidenceReturnsTheExistingCandidatesInsteadOfDuplicatingThem`, `manualFindingIsAvailableWithoutAnyAnalysis`, `aFindingMeasurementIsStorableAsProse`, and `anotherInspectorCannotAddAFinding`; plus `AiFindingCandidateTest` (4 candidate-review cases) and frontend `InspectorWorkspace.test.tsx` (9 cases). Re-ran on 2026-10-12 within the full backend suite of 364 passing tests and the full frontend suite of 219 tests across 39 files. The Inspector workspace now orders the steps as MF3-01/02 upload, MF3-03 quality decision, then MF3-05 detection, and detection fires automatically once the evidence set is accepted; only `ACCEPTED` is eligible, so a `LIMITED` decision leaves detection and draft generation to the manual path. A live compatible-vision call against a Wikimedia Commons CC0 iron-bridge corrosion photograph returned three `PENDING` candidates with provider provenance and normalized boxes; the seeded 1x1 placeholder PNGs correctly returned none. No API key, prompt, or image bytes were recorded. **Two defects found by walking MF3 in a browser on 2026-10-12, both fixed.** (1) The client sent `decision: CONFIRM`/`MODIFY`/`REJECT` where `AiFindingCandidateStatus` accepts `CONFIRMED`/`MODIFIED`/`REJECTED`, so every MF3-06 candidate decision was refused with `400 InvalidFormatException` on `ReviewCandidateRequest["decision"]` and the Confirm/Modify/Reject buttons had never produced a finding from the UI. Verified fixed live: confirming a `corrosion` candidate on inspection `2586669b-bb13-487b-902b-10af6591cb70` created an `AI_CONFIRMED` `VerifiedFinding` whose `decision` column stayed null, which is the MF3-06 → MF3-09 hand-off the backend models. (2) MF3-09's finding decision had **no client surface at all**: `useDecideFinding` existed in the hooks and `POST /inspections/{id}/findings/{findingId}/decision` existed behind `hasRole('ORG_ADMIN')`, but no component rendered either, so a finding recorded by an Inspector could never become official through the product. The qualified reviewer's Confirm/Modify/Reject control now renders on the inspection route for an `ORG_ADMIN` and is withheld from the Inspector; verified live by recording a `CONFIRMED` decision that set `decision`, `decided_by_user_id` and `decided_at` on the same finding, after which the control disappears rather than inviting a second decision. The workspace itself moved onto the inspection's own route, so a deep link and a row click reach the same MF3 flow. |
