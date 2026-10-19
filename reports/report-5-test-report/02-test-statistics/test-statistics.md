# Test Statistics sheet source

This table mirrors the `Test Statistics` sheet. Keep the workbook's summary
formulas and labels; update the values from the feature files after each test
round.

## Project metadata

The 15 October MF3 aggregate-confirmation gate and confirmed-findings rendering
correction have been implemented and verified. The matching end-to-end case,
`WF3-011`, is Pending; the 16 October post-publication corrective-outcome and
handoff change (`WF3-012`) is also Pending. The 11-case denominator includes
both. The MF3-12/13 backend paths executed green on 2026-10-16 (81 targeted WF3
tests; 650-test full `verify` gate); the cases remain Pending until their
complete end-to-end procedures execute. Do not read
narrow unit/integration results below as a pass for either new case.

| Field | Value |
| --- | --- |
| Project Name | SmartDroneInspection |
| Project Code | SEP490 — *confirm with project owner* |
| Test round | **2026-10-19: Source-backed MF3 report context and PDF alignment.** Backend `./mvnw.cmd -B verify` passed **668 tests**, 0 failures/errors/skips, with Spotless, JaCoCo and Modulith checks met. Targeted reports/session run covers `InspectionReportApiIntegrationTest` (32), `InspectionReportDraftingApiIntegrationTest` (11), `InspectionReportSectionsApiIntegrationTest` (22), `InspectionFieldSessionApiIntegrationTest` (9), and `ReportDraftClientTest` (6). It asserts report DTO organization/asset labels, preparation and session information in PDF text, no conditional-free checklist/session boilerplate, pre-flight note persistence/readback, and stored item-level checklist answers filtered to the session template. Frontend `ReportDerivedSections.test.tsx` passed 6 tests; `npx tsc --noEmit` and `npm run build` passed; `npm run lint` exited 0 with the same six Fast Refresh warnings. Published artifacts were not changed; no workflow decision was executed. **Previous round — 2026-10-19: Organization Admin reviewer workspace and report queue.** Frontend `npm test -- --run` passed 55 files / **427 tests**; `npx tsc --noEmit` and `npm run build` passed; `npm run lint` exited 0 with the same six Fast Refresh warnings. The focused reviewer-flow suites passed 8 files / 123 tests, including client-only route matching and role-specific navigation. The UI presents reviewer-first inspection tabs and a report queue with report-status actions; evidence and findings are read-only. No backend/API authorization or case status changed. **Previous round — 2026-10-19: Empty analysis persisted and every MF3 mutation reports its outcome. Backend `./mvnw.cmd -B clean verify` passed **667 tests**, 0 failures/errors/skips, with the Spotless, JaCoCo and Modulith checks met; the new `emptyAnalysisResultIsPersistedAsCompletedAndDoesNotRerunAutomatically` asserts that a zero-detection analysis is stored as completed and that the automatic pass does not re-issue it. Frontend `npm test -- --run` passed 55 files / **414 tests**; `useInspections.test.tsx` asserts the success text and the error severity of ten MF3 mutations (retirement, bulk retirement, shared evidence location, candidate review, manual finding add/update/remove, evidence-quality decision, findings confirmation, report submission), and `InspectionFindingsPage.test.tsx` asserts the "No defects detected" state after a completed empty analysis. `npx tsc --noEmit` clean, `npm run lint` exit 0 with the same 6 pre-existing Fast Refresh warnings, `npm run build` clean. The Analyse flow was also driven in a Playwright-managed browser against a synthetic Inspector session and a mocked API (no live credentials copied): the real Findings button sent `POST /api/v1/inspections/2fa8fd35-285a-43c4-a616-69d05cc8250d/evidence/evidence-defect-02/analyze?replace=false`, the info toast "Analysis completed; no defects were detected in this image." appeared, the chip switched to "No defects detected", and the control offered "Analyze again". **Previous round — **2026-10-18: MF3 end-to-end contract alignment.** Backend `./mvnw.cmd -B clean verify` passed **665 tests**, 0 failures/errors/skips, with Spotless, JaCoCo and Modulith checks met. Frontend `npm test -- --run` passed 55 files / **390 tests**; one earlier run had a transient Windows filesystem `UNKNOWN: open` error loading the unrelated WorkforcePage suite (its isolated 30/30 run passed); the final full suite passed all 54 files / **390 tests**. The final Findings provider-label suite passed 27/27; `npx tsc --noEmit`, lint and build passed. Oxlint reported six Fast Refresh warnings (shared app components and ReportSectionForm exports), no lint errors. Focused integration tests cover evidence duplicate status/retired conflict/shared location, report-level approval and corrective-action workflow, empty manual draft and fallback routing. **Previous round — 2026-10-18: Evidence-quality decision made cheaper on the happy path and its disclosure made visible.** An Inspector review of the MF3-03 panel found that the mandatory "Limitation or reason" field was always editable even for a plain acceptance (where the backend ignores it), and that the recorded shot-list comparison and reason were never shown back to anyone — the text only reached the draft prompt, so a junk value like `sd` could stand as the report's coverage disclosure unnoticed. The reason field now appears only after one of the reason-carrying decisions (re-upload, additional session, accept with limitation) is chosen and is confirmed separately, so an ordinary acceptance stays a single click; the recorded decision, comparison and reason are displayed in the panel, labelled as no longer current when the evidence set has changed since; and the consequence of each non-accepting decision ("does not unlock automated processing", detection/drafting need an accepted set) is stated before it is recorded. Only an accepted set unlocks advisory detection and report drafting, so no gate changed: `LIMITED` remains not detection-eligible per Report 3 MF3-05. No backend, schema or endpoint change; the four decision types are unchanged. Verified: frontend `npm test -- --run` passed 55 files / **390 tests** (the Evidence page suite gained a case asserting the recorded disclosure renders), `npx tsc --noEmit` clean, `npm run lint` exit 0 with the same 6 pre-existing warnings, `npm run build` clean, and the web container rebuilt and serving the change. No case status changed: 11 cases (8 Passed, 3 Pending). **Previous round — 2026-10-18: Evidence register filtered and paged by the server.** The Evidence tab no longer loads every capture to filter in the browser. `GET /api/v1/inspections/{inspectionId}/evidence/query` filters by `status` (`ACTIVE`\|`RETIRED`\|`ALL`), `mediaType` (`IMAGE`\|`VIDEO`\|`DOCUMENT`\|`ALL`) and case-insensitive file-name/content-type `search`, and pages with `page`/`pageSize` (default 50, clamped to 1-100), ordered by `createdAt` then `id`. Scope stays in the service: an unrelated Inspector gets 404 and a same-organization ORG_ADMIN may read. The response adds the inspection's `activeCount`/`retiredCount` and newest capture-added/capture-retired instants that drive the status counts and the stale-decision check. The unpaged `GET .../evidence` list still serves the Findings and Reports readers. Verified: backend `./mvnw.cmd clean verify` passed **665 tests**, 0 failures/errors/skips, with the Spotless, JaCoCo and Modulith checks met, including the new `evidenceQueryFiltersAndPagesWithStableScope` integration test; frontend `npm test -- --run` passed 55 files / **389 tests** with `npm run lint` and `npm run build` clean. **Previous round — 2026-10-17: Active evidence register filters and retired-capture exclusion in Findings.** Evidence register defaults to active captures and supports filename/content-type search, media-type filtering, and an explicit status filter for retired audit records. The Findings screen excludes retired evidence from the analysis queue and candidate groups and does not load retired image content in reviewer finding cards; retired pending candidates do not block active review. Frontend `npm test -- --run src/features/inspections/pages/InspectionEvidencePage.test.tsx src/features/inspections/pages/InspectionFindingsPage.test.tsx` passed 45 tests; full `npm test -- --run` passed 55 files / **389 tests**; `npm run lint` and `npm run build` passed. **Previous round — 2026-10-17: Bulk capture retirement for mistaken batches.** Added bulk evidence retirement (`POST /api/v1/inspections/{id}/evidence/bulk-retire`) to solve the operational problem of importing an entire wrong flight session or SD card batch (up to hundreds or thousands of captures) without having to retire each image individually. A single shared reason is recorded across all target captures while preserving original bytes and checksums for audit. Evidence register UI adds `Active`, `Retired audit`, and `All` filter tabs, selection checkboxes, and a bulk retire toolbar. Verified: backend `./mvnw -B verify` passed **664 tests**, 0 failures/errors/skips; frontend `npm test -- --run` passed 55 files / **385 tests** with lint and build clean. Live walkthrough retired a batch of 9 captures in one click, updating counts to `Active (0)` and `Retired audit (12)`. **Previous round — 2026-10-17: Findings CRUD, evidence retirement, author withdrawal, and review return reasons.** While a report is not submitted, the assigned Inspector can perform full CRUD on findings and retire captures: findings can be updated and soft-deleted with an attributable reason (`deleted_at`, `deleted_by_user_id`, `deletion_reason` stored for audit, filtered from active reads via `@SQLRestriction`); captures can be retired with an attributable reason (`retired_at`, `retired_by_user_id`, `retirement_reason`) without deleting original bytes; an author can withdraw a submitted report before reviewer action (returning it to author revision with `withdrawn_by_user_id`, `withdrawn_at`, `withdrawal_reason` stored); and reviewer returns explicitly distinguish `TEXT_REVISION` from `FINDINGS_REVISION` (which reopens findings and clears live reviewer decisions for revision). Forward migration `V32__mf3_findings_correction_and_author_withdrawal.sql` adds the audit and return columns. Verified: backend `./mvnw -B verify` passed **663 tests**, 0 failures/errors/skips, with Spotless, JaCoCo and Modulith checks met; frontend `npm test -- --run` passed 55 files / **384 tests** with lint and build clean. Live walkthrough verified in-place finding update, soft-delete with audit reason, capture retirement with "Retired — audit copy" chip and stale quality alert, and withdrawal/return reason handling. **Previous round — 2026-10-17: The Inspector can re-detect an image after the detector changes.** Analysis without `replace` still answers with the capture's existing candidates, while `?replace=true` runs the detector again and swaps the capture's unreviewed candidates for the new result, keeping candidates the Inspector already decided and producing the detections before removing the old ones. The findings panel offers **Analyze again** on such an image. Verified live on `11111111-2222-3333-4444-555555555552`: Analyze again on `shot-02-blade-leading-edge-crack.jpg` reached the detector (`POST /predict` 200, no fallback) and replaced its three `capstone` suggestions, after which the capture honestly reported no detected defects. Backend `./mvnw -B verify` passed **658 tests**, 0 failures/errors/skips, Spotless/JaCoCo/Modulith met; frontend `npm test -- --run` passed 55 files / 378 tests with lint and build clean. **Previous round — 2026-10-17: The trained YOLO11s detector is the default advisory provider.** The repository now serves the project's own YOLO11s model trained on MBDD2025 (crack, leakage, abscission, corrosion, bulge) from a new `ai-inference` service, and the backend routes analysis to it first with the OpenAI-compatible vision endpoint as the option behind it; the fallback answers only when the detector cannot, not when the detector returns no detections. Verified on the live stack: `POST /predict` returned detections for real sample images, the analyze endpoint returned a `yolo11s`/`mbdd2025-v1` candidate in 1.4 s, and with the detector stopped the same endpoint logged the fallback and answered from `capstone`/`gemini-3.8-flash-n` in 27 s. A latent defect was found and fixed: the JDK client's h2c upgrade made uvicorn answer `400 Unsupported upgrade request`, so the detector had never worked and the vision fallback had been serving every analysis silently. Backend `./mvnw -B verify` passed **657 tests**, 0 failures/errors/skips, with the Spotless, JaCoCo and Modulith checks met. **Previous round — 2026-10-17: Advisory detection runs in parallel with per-image updates.** The automatic MF3-05 pass analysed one image at a time; it now sends every unanalysed image at once and writes each response into the candidate cache as it arrives, so a row flips to `Detection complete` and its candidates appear in the Findings list as soon as that image answers, and one image failing or timing out no longer stops the rest. Verified live on inspection `11111111-2222-3333-4444-555555555552`: the banner read `Analysing 4 images in parallel…` with four rows in flight, the count stepped 4 → 2 → 0 as responses landed, and a 30 s timeout on one image left the other three running. Frontend `npm test -- --run` passed 55 files / 377 tests (one new case asserts a single call carrying every unanalysed image); `npm run lint` and `npm run build` exited 0. The suite also gained a shared `asyncUtilTimeout` so the heaviest page tests stop failing against a still-loading page when all 55 jsdom environments run at once. **Previous round — 2026-10-17: MF3-12/13 end-to-end walkthrough on the deployed stack; four defects found and fixed (`WF3-012` partly executed, still Pending).** The MF3 chain was driven through the running web client and the API against the merged source: MF3-06a confirmation recorded actor/time/snapshot without creating a version; the automated draft failure produced no partial version and no fallback; the manual draft created a version without LLM provenance; the stale draft was refused with `REPORT_SNAPSHOT_STALE`; review kept approval disabled until every proposal had a decision; publication ended at `REPORT_PUBLISHED` with the stored, checksummed PDF; the MF3-12 outcome and the MF3-13 handoff moved the inspection to `REPAIR_PENDING` with only the work-required finding handed off and no MF4 work order created; the negative paths returned `CORRECTIVE_HANDOFF_ALREADY_COMPLETED`, `CORRECTIVE_ACTION_ALREADY_RECORDED`, `CORRECTIVE_ACTION_REVIEW_REQUIRED` and `CORRECTIVE_ACTION_REVIEW_INCOMPLETE`, and a priority on a no-action outcome was refused with `400`. Four defects were found and fixed: the MF3-12 panel stayed hidden after publishing until a manual reload (missing workflow-state invalidation), the web container capped requests at 10 MB while the backend allows 20 MB so an oversize upload was answered with an nginx HTML page instead of the API error, the V30 backfill attributed pre-publication reviewer dispositions as post-publication outcomes, and the per-image chip labelled AI detections as findings. Backend `./mvnw -B verify` passed 651 tests, 0 failures/errors/skips (Spotless, JaCoCo and Modulith checks met); frontend `npm test -- --run` passed 55 files / 376 tests; lint and build exited 0. `WF3-012` remains Pending because the all-no-action close and the empty-findings no-repair close were not executed. **Previous round — 2026-10-16/17: MF3-12/13 post-publication corrective outcome and handoff implemented and verified (`WF3-012`, Pending).** Backend `.\mvnw.cmd verify` passed 650 tests, 0 failures/errors/skips (the five named MF3 suites contributed 81: 12 / 11 / 26 / 10 / 22) with the Spotless, JaCoCo and Modulith checks met; the evidence upload bounds changed to 10 MB per file / 20 MB per request. The frontend MF3-12 panel placement was corrected (it previously rendered only outside published versions); the focused suite passed 18/18, the full suite passed 55 files / 375 tests, and lint/build exited 0 on 2026-10-17. `WF3-012` remains Pending until its complete end-to-end scenario executes. **Previous round — 2026-10-15: MF3 confirmation and report-rendering regression correction.** Backend `./mvnw.cmd -B verify` passed 645 tests, 0 failures/errors/skips. Frontend `npm test -- --run` passed 54 files / 362 tests; lint exited 0 with six existing warnings; build passed. The Report 5 exporter suite passed 29 tests. (Test discovery was rerun with the docs repository's absolute path after an initial relative-path invocation from another working directory could not import the start directory.) Browser verification confirmed reopening Findings does not trigger automatic detection and Inspector-confirmed proposals appear in report output. These are supplementary regression checks; `WF3-011` remains Pending until its complete end-to-end procedure executes. Prior 2026-10-14 draft-context verification and exploratory walkthrough remain recorded below. |
| Last updated | 2026-10-19 (Report 5 version 4.35) |

## Module summary

| No | Module code | Passed | Failed | Pending | N/A | Number of test cases |
| ---: | --- | ---: | ---: | ---: | ---: | ---: |
| 1 | Identity, Enterprise Subscription and Workforce Governance | 0 | 0 | 0 | 0 | 0 |
| 2 | Asset, Drone, Workforce and Compliance Catalog — MF1 | 0 | 0 | 0 | 0 | 0 |
| 3 | Mission Preparation, Assignment Response and Readiness — MF2 | 3 | 0 | 0 | 0 | 3 |
| 4 | MF3 inspection evidence, findings and reporting | 2 | 0 | 0 | 0 | 2 |
| 5 | AI Vision Candidates and Human Finding Decisions | 1 | 0 | 1 | 0 | 2 |
| 6 | Inspection Report Drafting, Review and Publication — MF3 | 2 | 0 | 2 | 0 | 4 |
| 7 | Team Maintenance, Cost Control and Completion Reporting — MF4 | 0 | 0 | 0 | 0 | 0 |
| 8 | Dashboard, Analytics and Notifications | 0 | 0 | 0 | 0 | 0 |
| **Subtotal** |  | **8** | **0** | **3** | **0** | **11** |

`Module code` is not a free label. Each row's `C` cell is a formula —
`='Feature N'!B2` — so this column reports whatever sits in that sheet's
`Feature` cell (`B2`). The values above therefore match the `Feature sheet
summary` block recorded in each `fe-0N-…md` source, not the sheet names. The
remaining five columns are also formulas (`D:G` = `B6:E6` per-round counts,
`H` = `B4`), so nothing in this table is typed by hand at export.

One sheet per Report 3 feature means eight module rows. `Feature N` tests
`FE-0N`, so the module numbering is not free either: adding a feature to Report
3 adds the matching row here and the matching sheet in the workbook.

Because there are eight modules, `Sub total` moves from row 14 to **row 19**,
`Test coverage` to row 21 and `Test successful coverage` to row 22.

### Why most modules are empty

- **Modules 1, 2, 7 and 8 have no cases.** FE-01's supporting gates are
  recorded outside the case sheets. MF1 (catalog) and MF4 (maintenance) remain
  Report 3 requirements but are not implemented. FE-08 has no assigned case.
- **Module 3 has three MF2 cases.** `WF2-008` and `WF2-009` cover MF2-07
  readiness approval/return; `WF2-010` covers scoped preparation-history
  listing. They do not establish that all MF2 steps are complete or tested.
  MF2-08 source-change invalidation is partial;
  MF2-12 session end/`FIELD_COMPLETED` remains unimplemented.
- **Modules 4, 5 and 6 hold the eight MF3 cases**: FE-04 (evidence intake and
  scoped collections) has 2, FE-05 (advisory detection and human finding
  verification) has 2 (one passed, `WF3-003`, and one pending, `WF3-010`),
  and FE-06 (report review/publication `WF3-005`/`WF3-006` plus pending findings
  confirmation/draft choice `WF3-011` and pending post-publication corrective
  outcome/handoff `WF3-012`) has 4.

### Test coverage

The template computes both figures from the `Sub total` row and its own
formulas, `(Passed + Failed) * 100 / (Number of TCs - N/A)` and
`Passed * 100 / (Number of TCs - N/A)`. Pending cases remain in the denominator.
With 11 cases, 8 `Passed`, 3 `Pending`, and none `N/A`, test coverage and
successful coverage are each 72.73%. These rates describe recorded cases, not
product or full MF2 coverage. Update the underlying round statuses, never the
percentages.

## Reset and reconciliation scope

The previous statistics mixed a retired five-role WF1–WF4 baseline with
unimplemented Enterprise SaaS MF1–MF4 target cases, giving 33 cases with 13
`Passed` — a total that did not describe any single system. The 2026-10-09
reset removed obsolete and unimplemented rows, leaving five executed MF3 cases.
On 2026-10-10, after fast-forwarding the merged implementation PRs, the two
MF2-07 readiness cases `WF2-008` and `WF2-009` were restored to FE-03 based on
their test procedures and successful backend PR #64 CI. The current mainline
revisions are backend `84fcc16`, frontend `287d5a4`, and mobile `91092e6`.

| Change | Before reset | After reset | Current |
| --- | ---: | ---: | ---: |
| Cases | 33 | 5 | 11 |
| Passed | 13 | 5 | 8 |
| Failed | 0 | 0 | 0 |
| Pending | 20 | 0 | 3 |
| N/A | 0 | 0 | 0 |

The 28 removed cases (`WF1-001`–`WF1-019`, `WF2-001`–`WF2-007`, `WF3-001`,
`WF3-004`, `WF3-007`, `WF3-008`, `WF4-001`–`WF4-005`) described behavior that
no longer exists or has never been implemented. Their IDs stay reserved.

The increase from five to eleven cases reflects restored Report 5 coverage for
implemented MF2-07 approval/return, the scoped MF2 preparation-history read,
the pending MF3 reviewed-candidate correction/rejection case `WF3-010`, the
new Pending MF3 findings-confirmation/draft-choice case `WF3-011`, and the
Pending MF3-12/13 post-publication corrective-outcome and handoff case
`WF3-012`. It does not claim the remaining MF2 workflow is complete: MF2-08
invalidation is partial and MF2-12 session end remains unimplemented.

## Verification recorded this round

The MF2-07 case statuses are supported by the backend PR #64 CI run on
2026-10-10. Earlier MF3 evidence is retained from its own documented runs.
The 2026-10-14 integration-suite failure is retained as history and superseded
by the successful full verification on 2026-10-15; that 15 October run predates
the MF3-12/13 change. The new corrective-outcome/handoff paths and the changed
evidence-size bounds were then verified on 2026-10-16: the five named MF3 suites
passed 81 tests and the full `.\mvnw.cmd verify` gate passed 650 tests with the
Spotless, JaCoCo and Modulith checks met. `WF3-010`, `WF3-011` and `WF3-012`
remain Pending; these automated runs do not constitute their complete end-to-end
procedures.

| Check | Command | Result |
| --- | --- | --- |
| MF3 confirmation/review backend integration rerun | `./mvnw.cmd spotless:apply`; `./mvnw.cmd -Dtest=InspectionReportApiIntegrationTest,InspectionReportDraftingApiIntegrationTest test` | **Not yet passing as of 2026-10-14.** The previous affected-suite run executed 32 tests with 2 remaining failures in report-return/reviewer-decision fixture behavior; stale evidence submit and all 10 drafting tests passed. Do not count WF3-011 as executed/passed. |
| Frontend findings/report review focused suite | `npm test -- --run src/features/reports/pages/ReportDetailPage.test.tsx src/features/reports/components/ReportDerivedSections.test.tsx src/features/inspections/pages/InspectionFindingsPage.test.tsx src/features/inspections/pages/InspectionDraftPage.test.tsx` | **Passed 2026-10-14.** 4 files, 29 tests, 0 failures. Includes disabled approval until reviewer decisions and confirmed findings gates. Not a complete WF3-011 end-to-end execution. |
| Frontend lint | `npm run lint` | **Passed 2026-10-14** (exit 0; six existing Fast Refresh warnings). |
| Frontend production build | `npm run build` | **Passed 2026-10-14.** TypeScript and Vite production build succeeded. |
| Backend full suite + coverage gate + Modulith boundaries | PR #64 CI workflow: `Verify (Spotless + tests + JaCoCo + Modulith checks)` | **Passed.** 334 tests, 0 failures, 0 errors, 0 skipped; JaCoCo coverage checks and Spring Modulith checks passed. The CI job ran the Maven verify build; this record does not claim a local Maven command was executed successfully. |
| Backend full MF3 confirmation/rendering suite | `./mvnw.cmd -B verify` | **Passed 2026-10-15.** 647 tests, 0 failures/errors/skips; BUILD SUCCESS. JaCoCo coverage and Spring Modulith checks passed. Includes findings confirmation/reopen/snapshot gates, Inspector-confirmed report inclusion/reviewer-rejected exclusion, post-publication finding-decision refusal, repeated candidate-review conflict handling, and evidence-upload refusal after publication. Predates the MF3-12/13 change. |
| MF3 targeted backend suites | `.\mvnw.cmd -Dtest=InspectionEvidenceApiIntegrationTest,InspectionReportApiIntegrationTest,InspectionListApiIntegrationTest,InspectionReportDraftingApiIntegrationTest,InspectionReportSectionsApiIntegrationTest test` | **Passed 2026-10-16.** 81 tests, 0 failures/errors/skips; BUILD SUCCESS. Per suite: `InspectionEvidenceApiIntegrationTest` 12, `InspectionListApiIntegrationTest` 11, `InspectionReportApiIntegrationTest` 26, `InspectionReportDraftingApiIntegrationTest` 10, `InspectionReportSectionsApiIntegrationTest` 22. Includes the MF3-12/13 corrective-outcome/handoff paths and the corrected evidence-size bounds. |
| Backend full suite after MF3-12/13 | `.\mvnw.cmd verify` | **Passed 2026-10-16.** 650 tests, 0 failures, 0 errors, 0 skipped; BUILD SUCCESS. Spotless, JaCoCo coverage gate and Spring Modulith checks passed. Includes the MF3-12/13 paths, the all-no-action completion, and the corrected evidence-size bounds. This is the current full-suite record for the slice. |
| Frontend MF3-12 corrective panel focused suite | `npx vitest run src/features/reports/pages/ReportDetailPage.test.tsx` | **Passed 2026-10-17.** 18/18 tests, exit 0. After the panel-placement fix (`npm run build` green; 2 of the 4 new panel tests passed immediately; the other 2 initially failed only because MUI appends a required-asterisk to their labels and were switched to regex matchers). The final revision passed, and `npm run lint` (exit 0; six pre-existing warnings) and `npm test -- --run` (55 files / 375 tests passed) also passed. |
| Frontend full suite after MF3-12 panel fix | `npm test -- --run` | **Passed 2026-10-17.** 55 test files, 375 tests passed, exit 0. Includes the five new MF3-12 panel tests. |
| Frontend full MF3 confirmation/rendering suite | `npm test -- --run` | **Passed 2026-10-15.** 54 files, 363 tests passed. Includes regressions for rejected-only no-findings acknowledgment, optional location prose, candidate-query loading guard, returned-report author verification, published-report UI state, and report finding-status copy. |
| Frontend lint and production build | `npm run lint`; `npm run build` | **Passed 2026-10-15.** Lint exit 0 with six existing warnings; TypeScript and production build succeeded. |
| Report 5 exporter tests | `python -I -m unittest discover -s "E:\\Dev\\Repos\\Capstone\\SmartDroneInspection-docs\\tools\\tests" -p "test_*.py" -v` | **Passed 2026-10-15.** 29 tests passed. The first relative-path invocation from outside the docs repository failed discovery; the absolute-path rerun passed. |
| Docs whitespace check | `git diff --check` | **Passed 2026-10-15.** No whitespace errors. |
| Report 5 exporter tests (11-case expectations) | `python -I -m unittest discover -s tools/tests -p "test_*.py" -v` | **Passed 2026-10-17.** 29 tests, OK, exit 0. First execution after the expectations changed to 11 cases / 8 Passed / 3 Pending / 72.73 % and `WF3-012` on Feature 6. |
| Docs whitespace/conflict check | `git diff --check` | **Passed 2026-10-17.** Clean (exit code 0, empty output), reproduced twice. |
| Browser regression walkthrough | Local browser on inspection `e3e11000-561b-4f81-8173-868772a15c02` | **Passed 2026-10-15.** Reopening Findings caused no automatic analyze request; Inspector-confirmed proposals appeared in the report with reviewer status shown, and rejected findings remained excluded. This is supplementary MF3-10 evidence, not completion of WF3-011. |
| Backend local full suite (re-run, Docker available) | `./mvnw.cmd verify` | **Passed 2026-10-12.** 364 tests, 0 failures, 0 errors, 0 skipped; JaCoCo gate met ("All coverage checks have been met"); Spring Modulith boundary checks passed; BUILD SUCCESS. This is prior successful evidence; the 2026-10-13 rerun below is separate. |
| Backend affected WF3 integration assertions | PR #69 CI, run [38325774461](https://github.com/tungbach12/SmartDroneInspection-Backend/actions/runs/38325774461) — `./mvnw -B verify` | **Passed 2026-10-13.** Full `verify` completed with 491 tests, 0 failures, 0 errors, 0 skipped; Spotless clean, JaCoCo coverage checks met, and Spring Modulith checks passed. This run exercised the new comparison enforcement, finding-author no-self-review, and report snapshot stale-at-verify/submit integration assertions. |
| Backend full suite rerun (local) | `mvn.cmd -o verify` | **Blocked by environment 2026-10-13.** 491 tests discovered; 0 assertion failures and 263 errors because Testcontainers could not find a Docker environment. This local attempt is superseded for code verification by the successful CI run above; retain it as an environment record, not a product failure or pass. |
| MF3 end-to-end API walkthrough against the running stack | `powershell -File .scratch/mf3-evidence-and-report/run-wf3-8080.ps1 -InspectionId <uuid>` | **Passed 2026-10-11.** 38 assertions, 0 failures, against `spring-boot:run` on port 8080 with live PostgreSQL and MinIO. Covers evidence intake, checksum dedupe, type/size/empty/corrupt rejection, quality decision, manual finding and reviewer decision, report draft → verify → submit → return → resubmit → approve → publish, separation of duties, cross-tenant isolation, and publication immutability. Not a substitute for the automated suite; it exercises the same HTTP surface against real infrastructure. |
| Frontend lint | `npm run lint` | Passed with 6 `react(only-export-components)` warnings (exit 0). |
| Frontend full suite | `npm test -- --run` | **Passed 2026-10-13.** 42 files, 227 tests, 0 failures. |
| Frontend typecheck | `npx tsc --noEmit` | Passed 2026-10-13. |
| Frontend build | `npm run build` | Passed 2026-10-13. |
| Frontend focused inspections/reports/app suites (historical) | `npx vitest run src/features/inspections src/features/reports src/app/permissions/accessPolicy.test.ts` | **Passed 2026-10-12.** 13 files, 98 tests, 0 failures. Superseded by the broader 2026-10-13 full suite row above; retained as historical evidence. |
| MF3 live walkthrough with a real vision model (historical) | Browser walkthrough against the running stack (Vite 3000 → backend 8080 → 9router) | **Passed 2026-10-12.** Accepted an evidence set on inspection `2586669b…`; MF3-05 returned three `PENDING` candidates with provenance `capstone · gemini-3.8-flash-n`. Re-opening reran detection on the second image only and returned existing candidates without duplication. No API key, prompt, or image bytes recorded. |
| Mobile formatting | `dart format --set-exit-if-changed .` | **Passed 2026-10-13.** 63 files checked, no changes. |
| Mobile analysis | `flutter analyze` | **Passed 2026-10-13.** No issues found. |
| Mobile full suite | `flutter test` | **Passed 2026-10-13.** 44 tests, including ACCEPTED-only eligibility and four evidence-quality request payloads. |

| Report evidence-location regression | `cmd /c mvnw.cmd -Dtest=InspectionReportSectionsApiIntegrationTest#previewRendersConfirmedFindingsAndAttachedEvidence test` | **Passed 2026-10-13.** 1 test, 0 failures/errors/skips. PDF preview extraction confirmed the linked official finding's component/location in the evidence register and retained the finding's own location. |
| Frontend report evidence-location regression | `npm test -- --run src/features/reports/components/ReportDerivedSections.test.tsx` | **Passed 2026-10-13.** 1 file, 3 tests: GPS precedence, linked official finding fallback, pending finding excluded. |
| Frontend lint and build | `npm run lint && npm run build` | **Passed 2026-10-13.** Lint exit 0 with existing Fast Refresh warnings; TypeScript and Vite production build passed. |
| Live authenticated report UI | Dedicated local Chromium tab: `http://localhost/client/reports/78b9c412-a04d-43c6-abbd-ef54d5a58932` | **Passed 2026-10-13.** Version v5 displays `Pier 2 north face` on the confirmed finding and linked `spalling.jpg` evidence row. |
| Authenticated evidence previews | `npm test -- --run src/shared/ui/AuthenticatedImage.test.tsx`; live report reload in the local browser | **Passed 2026-10-13.** 2 tests passed. The shared API client's current Bearer token is used for image requests; after reloading, each of the six evidence images loaded with `naturalWidth: 1024`. |
| WF3 report drafting prompt contract | `cmd /c mvnw.cmd -Dtest=ReportDraftClientTest test` | **Passed 2026-10-14.** 6 tests, 0 failures/errors/skips. Asserts official findings/candidates are distinct, candidate status is advisory, session fields are labelled as records, Inspector quality comparison is not independent proof, and planned values are not actual observations. |
| WF3 report drafting API integration | `cmd /c mvnw.cmd -Dtest=ReportDraftClientTest,InspectionReportDraftingApiIntegrationTest test` | **Passed 2026-10-14.** 15 tests total: client 6/6 and Testcontainers API integration 9/9. Integration coverage includes candidate/session context, quality data from the API, and a later non-accepted quality decision blocking draft creation after prior acceptance. |
| WF3 Findings Inspector-only controls | `npm test -- --run src/features/inspections/pages/InspectionFindingsPage.test.tsx` | **Passed 2026-10-14.** 8 tests, including accepted-evidence Org Admin: no automatic or manual Analyze action is sent/shown, while reviewer decision control remains available. This is test coverage, not a live Org Admin walkthrough. |
| Frontend lint/build after WF3 role guard | `npm run lint && npm run build` | **Passed 2026-10-14** (existing Fast Refresh warnings; typecheck/build passed). Docker web image also built successfully for the live walkthrough. |
| WF3 live Inspector walkthrough | Local Docker UI/API with disposable inspection `2fa8fd35-285a-43c4-a616-69d05cc8250d` | **Exploratory only, 2026-10-14.** Six synthetic images uploaded; evidence quality accepted with a clearly test-only comparison; 17 pending candidates persisted across all six images; one DRAFT generated and left unverified/unsubmitted/unpublished. One browser analysis request returned `ERR_ABORTED` on navigation, but read-only DB inspection confirmed candidate rows for the sixth image as well. The generated text still called synthetic fixtures submitted captures and recommended physical validation; do not treat this run as successful professional author attestation or a passed WFx case. This live draft predates the later evidence-quality prompt update. |

The backend case-specific tests (`InspectionReadinessServiceTest`,
`ReadinessSnapshotFactoryTest`, and `InspectionReadinessApiIntegrationTest`)
were included in the historical successful 334-test PR #64 CI suite. The
historical 2026-10-12 local full run also passed 364 tests, but is not evidence
for assertions added afterward. On 2026-10-13, a separate full local rerun
discovered 491 tests and reported 0 assertion failures but 263 Testcontainers
errors because Docker was unavailable at that time. For the current WF3 source
context, Docker was available: the focused prompt/client and Testcontainers API
integration suites passed as recorded above. A local Docker UI/API walkthrough
also exercised real configured-model drafting on synthetic disposable data; it
is exploratory only and does not verify author attestation or professional
inspection claims. Full backend verification was not rerun for this slice.
The earlier MF3 work closed the JaCoCo gate after it had failed at 74.66% line
coverage on the original baseline and 78% after `InspectionListApiIntegrationTest`.
`ReportDraftConfigurationTest` covers startup validation requiring endpoint, API
key, model name and positive timeout; those historical checks do not establish
full §3.7.2 content or §3.7.3 safeguard coverage.

## Supporting export-tool verification (not workbook cases)

Executed on 2026-10-10 by Claude Code (automated). These are documentation-tool
checks, not additional product test cases. The previously verified export had a
five-case denominator because it predates the MF2 reconciliation; the current
source denominator is ten, including pending `WF3-010` and `WF3-011`. Export-tool checks do
not change any round status/date/tester.

| Check | Command | Result |
| --- | --- | --- |
| Independent exporter suites | `python -I -m unittest discover -s tools/tests -p "test_*.py" -v` | 29 tests passed: individual CLI execution, source tables, template styles/page settings, all three round/date/tester groups, original input preservation, safe outputs, Markdown readability, eight-sheet routing/statistics, and all eight FE summary blocks. |
| Prior full source-backed generation | `python -I tools/export_all.py --output reports/generated/2026-10-10-eight-features-final-v4` | Nine files generated before the MF2 reconciliation: Reports 1–3, Report 5 and five weekly workbooks. Missing editable sources were reported rather than fabricated. |
| Historical Report 5 generation (2026-10-10) | `python -I tools/export_all.py --only report5 --output reports/generated/2026-10-10-mf2-final` | Generated seven cases routed to Feature 3 (2), Feature 4 (2), Feature 5 (1), Feature 6 (2); this export predates WF2-010 and WF3-010. Manifest confirms input hashes unchanged and format parts preserved. |
| Historical Report 5 Office validation (2026-10-10) | `./tools/verify_office_reports.ps1 -OutputDirectory reports/generated/2026-10-10-mf2-final` | Excel opened and recalculated the 11-sheet workbook. Historical export: 7 cases / 7 Passed / 100% coverage and successful coverage; Round 2 and Round 3 each have 7 Pending. Source first-executed date/tester retained (2026-10-09 / Claude Code automated). Original generated package hash unchanged after Office read. |
| PDF preview | Office `-ExportPdf` attempt | Did not complete; blocked PDF export was stopped. No visual-PDF acceptance is claimed. |

Mermaid diagrams remain source text with manifest warnings, and long Excel
cells may require visual review. Package/style preservation and Office-open
verification are not a claim of final submission readiness.

## Supporting FE-01 verification (not workbook cases)

Supporting gates are excluded from the functional workbook totals. FE-01
auth-flow and role-policy evidence is recorded in
`03-features/fe-01-identity-access-governance.md`. Those gates change no
workbook case status.

## Coverage summary

Eight of the eleven listed cases have executed automated-test evidence;
`WF3-010`, `WF3-011` and `WF3-012` remain Pending. These metrics describe the
recorded cases, not full feature or product coverage.

- **Test coverage** = `(Passed + Failed) × 100 ÷ (Number of TCs − N/A)` =
  `(8 + 0) × 100 ÷ (11 − 0)` = 72.73%.
- **Test successful coverage** = `Passed × 100 ÷ (Number of TCs − N/A)` =
  `8 × 100 ÷ (11 − 0)` = 72.73%.
Both match the template formulas: pending cases remain in the denominator and
only `N/A` cases are excluded. These percentages are not product coverage: FE-02/MF1, most MF2 steps,
MF4/FE-07 and FE-08 remain
unverified or unimplemented, and FE-01 support evidence is outside the
workbook-case denominator.

The eight module rows are workbook-sheet totals, one per SRS feature; they are not counts of business workflows.

## Outstanding gaps

| Area | Status |
| --- | --- |
| MF1 asset/drone/workforce/compliance catalog | Workflow implementation and executed test evidence absent; no case. |
| MF2 assignment/preparation/compliance | Implemented in part; Report 5 covers readiness decision approval/return (`WF2-008`/`WF2-009`) and scoped preparation-history listing (`WF2-010`); remaining MF2 coverage gaps remain. |
| MF2-08 source-change invalidation | Partial: start rejects unless newest readiness decision is APPROVED; no source-change workflow appends INVALIDATED. |
| MF2-12 session end / FIELD_COMPLETED handoff | Not implemented; no case. |
| MF4 maintenance/cost/completion reporting | Workflow implementation and executed test evidence absent; no case. The MF3-13 handoff records eligible findings and inspection status only and does **not** create a work order; `WF3-012` is Pending. |
| FE-02 catalog CRUD | Implemented as a dependency of MF3, but no executed case is recorded for it. |
| FE-06 MF3-12/13 corrective outcome and handoff | Code and V30 schema exist and executed green on 2026-10-16 (81 targeted tests; 650-test full `verify`), but no case is passed yet. `WF3-012` (Pending) tracks the publish → per-finding outcome → work-required handoff, all-no-action completion, and empty-scope no-repair scenario. |
| FE-06 MF3-09 reviewer credential qualification | Runtime validates role, organization, active account and separation of duties only; no credential or professional-qualification check. Explicit implementation gap. |
| FE-06 MF3-07 source-input coverage | Objective/scope/criteria, evidence metadata, scoped candidates/sessions, and the latest accepted Inspector evidence-quality comparison have prompt/context test coverage; a synthetic disposable live run generated a draft. No dedicated checklist-answer or Inspector-observation source was identified; per-section source citations and complete source-state coverage remain unverified. The live draft predates the final quality-context addition. |
| FE-06 required report content (Report 3 §3.7.2) | Linked evidence component/location projection and targeted WF3 prompt/source-input coverage are recorded; full required section-content verification remains unverified. The synthetic live draft disclosed missing fields but also described fixture images as submitted captures and recommended physical validation. |
| FE-06 LLM safeguards (Report 3 §3.7.3) | Prompt constraints and candidate/official-finding distinction have focused coverage; full safeguards, including numeric-table sourcing and untrusted evidence-metadata handling, are not asserted by `WF3-005`/`WF3-006`. |
| FE-01 subscription/workforce governance | Supporting evidence is outside workbook functional-case totals; current-role scope should be reverified separately. |
| FE-08 dashboard/analytics/notifications | No assigned case. |
| Mobile client | `flutter analyze` and `flutter test` passed (40 tests); no WFx case was added for mobile behavior. |
| Live external LLM drafting provider | Exercised against disposable synthetic evidence only; not valid evidence of real inspection output or author attestation. The run remained an unsubmitted DRAFT. |
| Backend full-suite verification | **Passed 2026-10-16.** `.\mvnw.cmd verify` ran 650 tests, 0 failures/errors/skips; BUILD SUCCESS; Spotless, JaCoCo coverage gate and Spring Modulith checks met. Supersedes the historical 2026-10-13 environment errors and the 2026-10-15 run that predated the MF3-12/13 change. |

## Update rules

1. Update the Round 1/2/3 status in the feature source first.
2. Recount `Passed`, `Failed`, `Pending`, and `N/A` per feature.
3. Update all eight module rows and the subtotal row above.
4. Recalculate coverage; never mark a pending case as passed just to improve
   the percentage.
5. Never record a case for a workflow that has no implementation.
