# FE-05: AI Vision Candidates and Human Finding Decisions

Report 3 §3.6 titles this feature "AI Vision Candidates and Human Finding
Decisions". The filename retains the earlier "YOLO / defect detection
verification" wording; the filename is stable, the scope is Report 3's. Report 3
names no specific detection vendor or model family.

## Scope baseline

The `inspections` module implements the MF3 finding slice of FE-05: advisory AI
candidates that stay separate from human-verified findings, a manual finding
path that remains available when inference is refused or fails, and the
independent Organization Admin decision on a finding (role, organization,
active-account and separation-of-duties checks; reviewer credential
qualification is not validated at runtime). Report 3 requires that manual entry
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
| WF3-003 | Inspector verifies AI candidates or records a manual finding. | Request analysis before the Inspector accepts the evidence set; analyze a representative accepted image; verify its returned candidate provenance, confidence, normalized box, and pending status; re-analyze the same accepted image and confirm the candidate set is unchanged; attempt analysis as a different Inspector; confirm a candidate through the Findings stage and check the created finding is still undecided; record a manual finding with prose measurement; sign in as an ORG_ADMIN in the same organization and record the reviewer's decision on that finding; attempt decision by the finding creator and verify refusal; confirm the Inspector is not offered the reviewer decision. | Analysis is refused until the Inspector accepts the evidence; valid model detections are persisted only as `PENDING`; re-analysis of an already analysed image returns the existing candidates and creates no duplicate; out-of-scope Inspectors are refused; a confirmed candidate creates a `VerifiedFinding` whose `decision` is still null, because MF3-06 records a recommendation and not the official decision; a manual finding is available without analysis; a finding is official only after the independent ORG_ADMIN other than its creator records `CONFIRMED` or `MODIFIED`, stamping reviewer and time (qualification is not validated at runtime). | An assigned `FIELD_COMPLETED` inspection, accepted image evidence, PostgreSQL, and an authorized Inspector and ORG_ADMIN in the same organization. | Passed | 2026-10-12 | Claude Code (automated) | Pending |  |  | Pending |  |  | Verified with `InspectionReportApiIntegrationTest.analysisIsRefusedUntilTheInspectorAcceptsTheEvidence`, `analysisRequiresAssignmentAndAcceptedEvidenceAndPersistsOnlyPendingCandidates`, `reAnalysingTheSameEvidenceReturnsTheExistingCandidatesInsteadOfDuplicatingThem`, `manualFindingIsAvailableWithoutAnyAnalysis`, `aFindingMeasurementIsStorableAsProse`, and `anotherInspectorCannotAddAFinding`; plus `AiFindingCandidateTest` (4 candidate-review cases) and frontend `InspectionFindingsPage.test.tsx` (auto-detection runs for unanalysed images only; Confirm sends `CONFIRMED` with per-candidate severity/location; candidate cards render evidence-linked defect photos; reviewer control appears only for ORG_ADMIN on undecided findings). **WF3 alignment follow-up, 2026-10-13:** `FindingService.decideFinding` rejects the finding creator with 403 `FINDING_REVIEWER_INVALID`; `InspectionReportApiIntegrationTest.findingAuthorCannotDecideTheirOwnFinding` covers a persisted dual-role author and independent reviewer. **Passed in backend PR #69 CI run 38325774461:** `./mvnw -B verify` ran 491 tests with 0 failures/errors/skips; the finding-author test and related comparison/snapshot integration assertions executed under Testcontainers. The separate local full run remains recorded as Docker-blocked (263 environment errors) in `test-statistics.md`. |
| WF3-010 | Assigned Inspector corrects a reviewed candidate and its linked undecided finding before reviewer decision or report lock; rejection removes that finding, while final reviewer decisions remain immutable. | Review a candidate, correct its label/details and linked undecided finding, reject the corrected candidate, and verify removal of the linked undecided finding. Repeat after a reviewer decision and after report submission/publication to verify revision is refused and final decisions remain unchanged. | Before a lock, the Inspector's correction updates the reviewed candidate and linked undecided finding; rejection removes the linked undecided finding. After reviewer decision or report lock, correction is refused; final reviewer decisions remain immutable. | Assigned Inspector; reviewed candidate with linked undecided finding; fixtures for reviewer-decided and submitted/published report states. | Pending |  |  | Pending |  |  | Pending |  |  | Implementation and a frontend correction-call unit test exist, but executed evidence for the complete revision, rejection, lock, and immutable-decision paths is not recorded. |

### WF3 role-gating follow-up — 2026-10-14

The assigned Inspector is the only role that may trigger automatic or manual AI detection. The Findings UI now hides Analyze/Re-run controls and skips the auto-analysis effect for ORG_ADMIN reviewers; reviewer verdict controls remain available. `InspectionFindingsPage.test.tsx` passed 8 tests, including the new accepted-evidence ORG_ADMIN case. The Report 3 §3.7.1 requirement was clarified to match the existing backend `INSPECTOR` endpoint authorization. No WF3-003 case status changed.

### Reopen no longer restarts detection — 2026-10-15

Reopening Findings returned the inspection to `FIELD_COMPLETED`, which re-armed the automatic
detection effect and silently ran the model on any image that had produced no candidate. The
automatic pass is now a single offer per inspection, remembered for the tab session per user and
inspection, so reopening the reviewed set does not restart detection. Because MF3-05 makes re-running
an analysed image return its existing candidates, an image that already has a candidate no longer
offers a detection control; the "Detection complete" chip carries that state, and detection stays
available from the explicit per-image **Analyze** action.

Executed evidence:

- `npm test -- --run src/features/inspections/pages/InspectionFindingsPage.test.tsx` — 15 passed.
  Includes the new `does not auto-analyze again after the Inspector reopens findings` and
  `offers no re-run control on an image whose detection already ran` cases.
- `npm test -- --run` — 54 files, 363 tests, 0 failures.

### Detection runs in parallel with per-image updates — 2026-10-17

The automatic pass analysed one image at a time: it awaited each request before starting the next,
so a set of six images took six round trips in sequence and the page showed a single "Analysing
<file>…" row while the rest waited. The pass now sends every unanalysed image at once and writes
each response into the candidate cache as it arrives, so that image's row flips to "Detection
complete" and its candidates appear in the Findings list immediately. One image failing or timing
out no longer stops the rest: the failure is reported and the manual path stays open. The hook that
owned a single in-flight request (`useAnalyzeEvidence`) now owns the set of in-flight images, so the
automatic pass and the explicit per-image **Analyze** action share one source of truth.

Executed evidence:

- Live walkthrough on inspection `11111111-2222-3333-4444-555555555552` (six images already
  analysed, three more added for the run): the banner read "Analysing 4 images in parallel…" with
  four rows spinning at once, and the in-flight count stepped 4 → 2 → 0 as individual responses
  landed, with the completed rows updating in place. One image's inference call exceeded the 30 s
  client timeout and did not stop the other three; its candidate was nevertheless stored by the
  backend, and the row showed "Detection complete" after the next load.
- `npm test -- --run src/features/inspections/pages/InspectionFindingsPage.test.tsx` — 22 passed,
  including `analyses every unanalysed image in one parallel pass` (asserts a single call carrying
  every unanalysed image id) and `runs detection automatically once accepted, and only for
  unanalysed images` (asserts the PDF is not analysed).
- `npm test -- --run` — 55 files, 377 tests, 0 failures; `npm run lint` and `npm run build` exit 0.
- `npm run lint` — unchanged baseline of 6 pre-existing `react(only-export-components)` warnings,
  none in the changed files.
- `npm run build` — succeeded.
- Browser walkthrough on inspection `e3e11000-561b-4f81-8173-868772a15c02` (Field Inspector,
  Inspector role): with no flag stored, first visit issued one
  `POST /evidence/{id}/analyze`; after reload with the flag stored, **no** analyze request was
  issued; confirming findings issued no analyze request; clicking **Reopen Findings** returned
  `POST /findings/reopen` `200` with **no** analyze request, and the stage showed "Detection
  complete" with no control on the analysed image; clicking the remaining **Analyze** button still
  issued its analyze request. `analyze` is Inspector-only, so no negative-role case applies to this
  change.

No WF3-003 case status changed; the case already records that re-analysis returns existing
candidates rather than duplicating them. A repeated Inspector review of a non-pending candidate
now returns `409 CANDIDATE_ALREADY_REVIEWED`; use the revision action to make changes. |
