# FE-05: AI Vision Candidates and Human Finding Decisions

Report 3 §3.6 titles this feature "AI Vision Candidates and Human Finding
Decisions". The filename retains the earlier "YOLO / defect detection
verification" wording; the filename is stable, the scope is Report 3's. Report 3
names no specific detection vendor or model family.

## Scope baseline

The `inspections` module implements the MF3 finding slice of FE-05: advisory AI
candidates that stay separate from human-verified findings, a manual finding
path that remains available when inference is refused or fails, and the
Inspector resolution and confirmation of findings, plus report-level Organization Admin review (role, organization, active-account and separation-of-duties checks; reviewer credential qualification is not validated at runtime). Organization Admin per-finding verdicts are not part of the current product flow; post-publication corrective outcomes remain per finding. Report 3 requires that manual entry
survives an AI outage, so the manual path is not conditional on AI
availability.

Detection runs against active evidence only. Retired evidence is excluded from
automatic/manual detection lists and candidate groups; retired images are not
loaded as finding photos. Detection is served by the project's YOLO11s inference
service first, with the OpenAI-compatible vision adapter behind the
inspections-owned `AiInferencePort` as fallback. Credentials are environment-only.
Both adapters are implementation choices behind the requirement, not part of it.

## Feature sheet summary

Values for the `Feature 5` summary block (`A2:E8` in the workbook). The
exporter maps this file to the matching SRS feature sheet.

| Cell | Label | Value |
| --- | --- | --- |
| `B2` | Feature | AI Vision Candidates and Human Finding Decisions |
| `B3` | Test requirement | Verifies human review of advisory AI suggestions and manual findings; unconfirmed detections do not enter official findings, and rejected AI suggestions are removed rather than retained as finding-level audit records. |

## Current case

| Test Case ID | Test Case Description | Test Case Procedure | Expected Results | Pre-conditions | Round 1 | Test date | Tester | Round 2 | Test date | Tester | Round 3 | Test date | Tester | Note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| WF3-003 | Inspector verifies AI suggestions or records a manual finding. | Request analysis before the Inspector accepts the evidence set; analyze a representative accepted image; verify its returned finding provenance, confidence, normalized box and pending status; re-analyze the same accepted image and confirm the finding set is unchanged; attempt analysis as a different Inspector; confirm one suggestion and verify its finding remains pending until the Inspector confirms the findings set; reject another suggestion and verify it is removed from the retained finding records; record a manual finding with prose measurement; confirm the findings set; attempt an out-of-scope Inspector read. | Analysis is refused until the Inspector accepts the evidence; valid model detections are persisted only as `PENDING`; re-analysis of an already analysed image returns existing findings and creates no duplicate; out-of-scope Inspectors are refused; confirming a suggestion creates/updates a unified `Finding` whose status remains `PENDING` until Inspector confirmation; rejecting a suggestion removes it from retained finding records and creates no finding; manual findings remain available without analysis; confirmed findings become reportable after the assigned Inspector confirms the set. The Organization Admin approves or returns the submitted report as a whole; no Admin per-finding decision is made. | An assigned `FIELD_COMPLETED` inspection, accepted image evidence, PostgreSQL, and an authorized Inspector and ORG_ADMIN in the same organization. | Passed | 2026-10-12 | Claude Code (automated) | Pending |  |  | Pending |  |  | Verified with `InspectionReportApiIntegrationTest.analysisIsRefusedUntilTheInspectorAcceptsTheEvidence`, `analysisRequiresAssignmentAndAcceptedEvidenceAndPersistsOnlyPendingCandidates`, `reAnalysingTheSameEvidenceReturnsTheExistingCandidatesInsteadOfDuplicatingThem`, `manualFindingIsAvailableWithoutAnyAnalysis`, `aFindingMeasurementIsStorableAsProse`, and `anotherInspectorCannotAddAFinding`; plus `AiFindingCandidateTest` (4 candidate-review cases) and frontend `InspectionFindingsPage.test.tsx` (auto-detection runs for unanalysed images only; Confirm sends `CONFIRMED` with per-candidate severity/location; candidate cards render evidence-linked defect photos; reviewer control appears only for ORG_ADMIN on undecided findings). **WF3 alignment follow-up, 2026-10-13:** `FindingService.decideFinding` rejects the finding creator with 403 `FINDING_REVIEWER_INVALID`; `InspectionReportApiIntegrationTest.findingAuthorCannotDecideTheirOwnFinding` covers a persisted dual-role author and independent reviewer. **Passed in backend PR #69 CI run 38325774461:** `./mvnw -B verify` ran 491 tests with 0 failures/errors/skips; the finding-author test and related comparison/snapshot integration assertions executed under Testcontainers. The separate local full run remains recorded as Docker-blocked (263 environment errors) in `test-statistics.md`. |
| WF3-010 | Assigned Inspector corrects a finding before report submission; report return for findings/evidence revision reopens Inspector review. | Revise an AI-originated finding or manual finding, confirm the findings set, create and submit a report, return it for findings/evidence revision, and verify Inspector confirmation is invalidated and must be recorded again; reject an AI suggestion and verify it is removed rather than retained as a finding record. | Before submission the Inspector may correct the finding; after report submission edits are locked; a report-level findings/evidence return reopens the Inspector stage and requires reconfirmation. Rejecting an AI suggestion creates no finding and removes it from retained finding records; explicit removal of an Inspector working-set finding remains attributable and auditable. Organization Admin does not decide findings individually. | Assigned Inspector; AI-originated or manual finding and submitted report fixtures. | Pending |  |  | Pending |  |  | Pending |  |  | Implementation and correction-call unit test exist; executed evidence for the complete revision, rejection/removal, lock and immutable-decision paths is not recorded. |

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

### The trained YOLO11s detector is the default advisory provider — 2026-10-17

The advisory adapters existed but no detector was ever served, so every analysis ran through the
OpenAI-compatible vision endpoint. The repository now ships the detector that was trained for this
project and makes it the default provider, with the vision endpoint as the option behind it.

- `ai-inference/` in the backend repository serves the **YOLO11s** model trained on **MBDD2025**
  (`crack`, `leakage`, `abscission`, `corrosion`, `bulge`) with FastAPI/uvicorn and the weights
  mounted at runtime. Compose runs it as the `ai-inference` service and the backend reaches it at
  `http://ai-inference:8000`. The weights and the training notebook are kept in
  `ai-inference/` with a README that records the kernel, the dataset and the re-download command.
- The service answers the raw-body contract `YoloInferenceClient` already sent (the notebook's
  original `app.py` used a multipart `UploadFile`, which the Spring client never sends).
- `PrimaryWithFallbackInference` routes analysis to the detector first and to the vision endpoint
  only when the detector cannot answer — a connection failure, a timeout or an error status. A
  valid response with zero detections is final and does not trigger fallback.
  With neither provider configured the endpoints still report that automated analysis is not
  configured, and candidates keep the `modelName`/`modelVersion` of the provider that produced them.

Defect found and fixed while wiring this up: the JDK HTTP client attempts an **h2c upgrade** on a
plain-http endpoint, and uvicorn answers that with `400 Unsupported upgrade request`, so the
detector failed on every call and the vision fallback silently served all analysis. The YOLO client
now pins HTTP/1.1, and
`YoloInferenceConfigurationTest.theDetectorClientSpeaksHttp11SoAnAsgiServerAcceptsTheRequest` fails
without the pin by refusing the upgrade the way uvicorn does.

Executed evidence (live stack, `docker compose`, MBDD2025 weights in place):

- `curl http://localhost:8000/health` — `{"status":"ok","model":"yolo11s","version":"mbdd2025-v1"}`.
- `POST /predict` with raw image bytes — `sample-images/concrete-crack.jpg` returned three
  detections (`abscission` 0.5644, `crack` 0.5462, `abscission` 0.2553) with normalized boxes;
  `sample-images/bearing-seat.jpg` returned `abscission` 0.5029.
- `POST /api/v1/inspections/{id}/evidence/{evidenceId}/analyze` with the detector running —
  one candidate, `modelName=yolo11s`, `modelVersion=mbdd2025-v1`, `predictedLabel=abscission`,
  in **1.4 s**.
- The same endpoint with the `ai-inference` service stopped — the backend logged
  `Primary detector failed (YOLO inference request failed); using the configured fallback detector`
  and returned `capstone`/`gemini-3.8-flash-n` `corrosion` 0.97 in 27 s, so the option degrades
  rather than removes the advisory step.
- Backend `./mvnw -B verify` — **657 tests, 0 failures/errors/skips**, Spotless, JaCoCo and Modulith
  checks met.

`WF3-003` stays Pending for its full case procedure; this round adds the detector path and its
fallback rather than executing that case.

### The Inspector can re-detect an image after the detector changes — 2026-10-17

Detection ran once per capture: an image that already had candidates offered no control, because
MF3-05 makes a repeated analysis answer with the existing candidates rather than run the detector
again. That left no way to move a capture from one detector to another — the switch to the trained
YOLO11s model left every earlier suggestion in place with no way to refresh it.

- `POST /evidence/{evidenceId}/analyze?replace=true` is the explicit re-run: it produces the new
  detections first and then swaps the capture's **unreviewed** findings for them. An Inspector-
  confirmed finding survives, so the inspected record is never erased. Producing detections before
  deleting keeps a detector failure from emptying the capture. Rejected AI suggestions are removed
  rather than retained as finding-level audit records.
- The findings panel now offers **Analyze again** on an image that already has candidates (the
  automatic pass and the first analysis are unchanged), and its explanation states that a re-run
  replaces the unreviewed suggestions and keeps the decided ones.
- The candidate cache is updated per response as before, so the replaced image's suggestions change
  in place.

Executed evidence:

- `npm test -- --run src/features/inspections/pages/InspectionFindingsPage.test.tsx` — 23 passed,
  including `re-runs detection on an analysed image and asks the server to replace its suggestions`
  and `analyses an image that has no candidates without replacing anything`.
- `npm test -- --run` — 55 files, 378 tests, 0 failures; `npm run lint` and `npm run build` exit 0.
- `InspectionReportApiIntegrationTest.anExplicitReRunReplacesUnreviewedCandidatesAndKeepsTheReviewedOnes`
  — a pending finding from the first detector is replaced by the new detector result, while
  Inspector-confirmed findings survive.
- Live walkthrough on `11111111-2222-3333-4444-555555555552`: **Analyze again** on
  `shot-02-blade-leading-edge-crack.jpg` issued `POST /predict` `200` to the detector (no fallback),
  replaced its three `capstone` suggestions, and the row returned to **Analyze** with
  "No detected defects" — the detector found nothing on that turbine-blade capture, which is the
  honest result for a model trained on MBDD2025 building defects.
- Backend `./mvnw -B verify` — **658 tests, 0 failures/errors/skips**; Spotless, JaCoCo and Modulith
  checks met.

`WF3-003` stays Pending for its full case procedure.

### Empty detection results are explicit and persisted — 2026-10-18

A successful analysis that returns no candidates is now recorded separately from an image that has never been analysed. The Findings page labels the image **No defects detected**, provides an informational toast, and leaves **Analyze again** available. Failures produce an error toast while retaining the inline error detail. The persisted status prevents the automatic pass from repeating an empty result after reload; a deliberate Analyze again still runs the detector. A valid empty YOLO result remains final and never invokes the optional vision fallback.

Executed evidence:

- Backend `InspectionReportApiIntegrationTest.emptyAnalysisResultIsPersistedAsCompletedAndDoesNotRerunAutomatically` — passed; verifies the empty candidate response, persisted completed status/count, and no second inference call.
- Frontend focused API, hook and Findings suites — 3 files / 32 tests passed, including zero-result notification, inference-failure notification, persisted-status rendering and the Analyze-again action.
- Full frontend suite re-run 2026-10-19 — 55 files / 414 tests passed; `useInspections.test.tsx` also asserts the success text and error severity of the other ten MF3 mutations.
- Playwright (2026-10-19), synthetic Inspector session and mocked API, no live credentials: the Findings **Analyze** button sent `POST /api/v1/inspections/2fa8fd35-285a-43c4-a616-69d05cc8250d/evidence/evidence-defect-02/analyze?replace=false`, the info toast “Analysis completed; no defects were detected in this image.” appeared, the per-image chip read **No defects detected**, and the control became **Analyze again**.
- `WF3-003` remains Pending; these focused regressions do not substitute for its full case procedure.

### Retired evidence excluded from Findings — 2026-10-17

The evidence register defaults to active captures and offers filename/content-type search,
media-type filters, and an explicit evidence-status filter to view retired audit records.
Findings filters retired captures out of automatic and manual detection rows, candidate groups,
and the active candidate review count. Reviewer finding cards load a source photo only when its
linked evidence is still active; historical finding text remains visible without requesting a
retired source image. A pending candidate linked to retired evidence is excluded from the current
active review gate, so it cannot block active findings progress.

Executed evidence:

- `npm test -- --run src/features/inspections/pages/InspectionEvidencePage.test.tsx src/features/inspections/pages/InspectionFindingsPage.test.tsx` — 45 passed, including retired-default/status filter, filename/media filters, retired candidate exclusion, detection exclusion, and reviewer photo exclusion.
- `npm test -- --run` — 55 files / 389 tests passed.
- `npm run lint` — passed with six existing `react(only-export-components)` warnings outside the changed files.
- `npm run build` — passed.

## 2026-10-18 role and detection preference alignment

Inspector candidate confirmation now establishes reportable finding state; the Organization Admin makes one report-level approve/return decision and separately records MF3-12 corrective outcomes after publication. Removed the obsolete Admin finding-decision endpoint and panel. Added a persistent Inspector preference (default ON) to disable the automatic YOLO-failure vision fallback; empty YOLO results never invoke fallback. Verified backend `PrimaryWithFallbackInferenceTest` and full integration suite.
