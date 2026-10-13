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
| WF3-003 | Inspector verifies AI candidates or records a manual finding. | Request analysis before the Inspector accepts the evidence set; analyze a representative accepted image; verify its returned candidate provenance, confidence, normalized box, and pending status; re-analyze the same accepted image and confirm the candidate set is unchanged; attempt analysis as a different Inspector; confirm a candidate through the Findings stage and check the created finding is still undecided; record a manual finding with prose measurement; sign in as a qualified ORG_ADMIN in the same organization and record the reviewer's decision on that finding; attempt decision by the finding creator and verify refusal; confirm the Inspector is not offered the reviewer decision. | Analysis is refused until the Inspector accepts the evidence; valid model detections are persisted only as `PENDING`; re-analysis of an already analysed image returns the existing candidates and creates no duplicate; out-of-scope Inspectors are refused; a confirmed candidate creates a `VerifiedFinding` whose `decision` is still null, because MF3-06 records a recommendation and not the official decision; a manual finding is available without analysis; a finding is official only after the qualified reviewer other than its creator records `CONFIRMED` or `MODIFIED`, stamping reviewer and time. | An assigned `FIELD_COMPLETED` inspection, accepted image evidence, PostgreSQL, and an authorized Inspector and ORG_ADMIN in the same organization. | Passed | 2026-10-12 | Claude Code (automated) | Pending |  |  | Pending |  |  | Verified with `InspectionReportApiIntegrationTest.analysisIsRefusedUntilTheInspectorAcceptsTheEvidence`, `analysisRequiresAssignmentAndAcceptedEvidenceAndPersistsOnlyPendingCandidates`, `reAnalysingTheSameEvidenceReturnsTheExistingCandidatesInsteadOfDuplicatingThem`, `manualFindingIsAvailableWithoutAnyAnalysis`, `aFindingMeasurementIsStorableAsProse`, and `anotherInspectorCannotAddAFinding`; plus `AiFindingCandidateTest` (4 candidate-review cases) and frontend `InspectionFindingsPage.test.tsx` (auto-detection runs for unanalysed images only; Confirm sends `CONFIRMED` with per-candidate severity/location; candidate cards render evidence-linked defect photos; reviewer control appears only for ORG_ADMIN on undecided findings). **WF3 alignment follow-up, 2026-10-13:** `FindingService.decideFinding` rejects the finding creator with 403 `FINDING_REVIEWER_INVALID`; `InspectionReportApiIntegrationTest.findingAuthorCannotDecideTheirOwnFinding` covers a persisted dual-role author and independent reviewer. **Passed in backend PR #69 CI run 38325774461:** `./mvnw -B verify` ran 491 tests with 0 failures/errors/skips; the finding-author test and related comparison/snapshot integration assertions executed under Testcontainers. The separate local full run remains recorded as Docker-blocked (263 environment errors) in `test-statistics.md`. |
