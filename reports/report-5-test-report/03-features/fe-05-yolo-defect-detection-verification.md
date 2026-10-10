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

Shared `Feature 2` block; see `fe-04-…md` for the canonical values. FE-05
contributes only case rows to it.

## Current case

| Test Case ID | Test Case Description | Test Case Procedure | Expected Results | Pre-conditions | Round 1 | Test date | Tester | Round 2 | Test date | Tester | Round 3 | Test date | Tester | Note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| WF3-003 | Inspector verifies AI candidates or records a manual finding. | Request analysis before the Inspector accepts the evidence set; analyze a representative accepted image; verify its returned candidate provenance, confidence, normalized box, and pending status; attempt analysis as a different Inspector; record a manual finding with prose measurement; record the reviewer's decision on the finding. | Analysis is refused until the Inspector accepts the evidence; valid model detections are persisted only as `PENDING`; out-of-scope Inspectors are refused; a manual finding is available without analysis; a finding is official only after a `CONFIRMED` or `MODIFIED` decision. | An assigned `FIELD_COMPLETED` inspection, accepted image evidence, PostgreSQL, and an authorized Inspector and ORG_ADMIN in the same organization. | Passed | 2026-10-08 | Claude Code (automated) | Pending |  |  | Pending |  |  | Verified with `InspectionReportApiIntegrationTest.analysisIsRefusedUntilTheInspectorAcceptsTheEvidence`, `analysisRequiresAssignmentAndAcceptedEvidenceAndPersistsOnlyPendingCandidates`, `manualFindingIsAvailableWithoutAnyAnalysis`, `aFindingMeasurementIsStorableAsProse`, and `anotherInspectorCannotAddAFinding`; plus `AiFindingCandidateTest` (4 candidate-review cases). These ran again on 2026-10-09 within the full backend suite of 156 passing tests. A live compatible-vision call against a Wikimedia Commons CC0 iron-bridge corrosion photograph returned three `PENDING` candidates with provider provenance and normalized boxes; the seeded 1x1 placeholder PNGs correctly returned none. No API key, prompt, or image bytes were recorded. |
