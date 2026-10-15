# Test Statistics sheet source

This table mirrors the `Test Statistics` sheet. Keep the workbook's summary
formulas and labels; update the values from the feature files after each test
round.

## Project metadata

The 15 October MF3 aggregate-confirmation gate and confirmed-findings rendering
correction have been implemented and verified. The matching end-to-end case,
`WF3-011`, is Pending; the 10-case denominator includes it. Do not read narrow
unit/integration results below as a pass for the whole new case.

| Field | Value |
| --- | --- |
| Project Name | SmartDroneInspection |
| Project Code | SEP490 — *confirm with project owner* |
| Test round | **2026-10-15: MF3 confirmation and report-rendering regression correction.** Backend `./mvnw.cmd -B verify` passed 645 tests, 0 failures/errors/skips. Frontend `npm test -- --run` passed 54 files / 362 tests; lint exited 0 with six existing warnings; build passed. The Report 5 exporter suite passed 29 tests. (Test discovery was rerun with the docs repository's absolute path after an initial relative-path invocation from another working directory could not import the start directory.) Browser verification confirmed reopening Findings does not trigger automatic detection and Inspector-confirmed proposals appear in report output. These are supplementary regression checks; `WF3-011` remains Pending until its complete end-to-end procedure executes. Prior 2026-10-14 draft-context verification and exploratory walkthrough remain recorded below. |
| Last updated | 2026-10-15 (Report 5 version 4.20) |

## Module summary

| No | Module code | Passed | Failed | Pending | N/A | Number of test cases |
| ---: | --- | ---: | ---: | ---: | ---: | ---: |
| 1 | Identity, Enterprise Subscription and Workforce Governance | 0 | 0 | 0 | 0 | 0 |
| 2 | Asset, Drone, Workforce and Compliance Catalog — MF1 | 0 | 0 | 0 | 0 | 0 |
| 3 | Mission Preparation, Assignment Response and Readiness — MF2 | 3 | 0 | 0 | 0 | 3 |
| 4 | MF3 inspection evidence, findings and reporting | 2 | 0 | 0 | 0 | 2 |
| 5 | AI Vision Candidates and Human Finding Decisions | 1 | 0 | 1 | 0 | 2 |
| 6 | Inspection Report Drafting, Review and Publication — MF3 | 2 | 0 | 1 | 0 | 3 |
| 7 | Team Maintenance, Cost Control and Completion Reporting — MF4 | 0 | 0 | 0 | 0 | 0 |
| 8 | Dashboard, Analytics and Notifications | 0 | 0 | 0 | 0 | 0 |
| **Subtotal** |  | **8** | **0** | **2** | **0** | **10** |

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
- **Modules 4, 5 and 6 hold the seven MF3 cases**: FE-04 (evidence intake and
  scoped collections) has 2, FE-05 (advisory detection and human finding
  verification) has 2 (one passed, `WF3-003`, and one pending, `WF3-010`),
  and FE-06 (report review/publication `WF3-005`/`WF3-006` plus pending findings
  confirmation/draft choice `WF3-011`) has 3.

### Test coverage

The template computes both figures from the `Sub total` row and its own
formulas, `(Passed + Failed) * 100 / (Number of TCs - N/A)` and
`Passed * 100 / (Number of TCs - N/A)`. Pending cases remain in the denominator.
With 10 cases, 8 `Passed`, 2 `Pending`, and none `N/A`, test coverage and
successful coverage are each 80.00%. These rates describe recorded cases, not
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
| Cases | 33 | 5 | 10 |
| Passed | 13 | 5 | 8 |
| Failed | 0 | 0 | 0 |
| Pending | 20 | 0 | 2 |
| N/A | 0 | 0 | 0 |

The 28 removed cases (`WF1-001`–`WF1-019`, `WF2-001`–`WF2-007`, `WF3-001`,
`WF3-004`, `WF3-007`, `WF3-008`, `WF4-001`–`WF4-005`) described behavior that
no longer exists or has never been implemented. Their IDs stay reserved.

The increase from five to ten cases reflects restored Report 5 coverage for
implemented MF2-07 approval/return, the scoped MF2 preparation-history read,
the pending MF3 reviewed-candidate correction/rejection case `WF3-010`, and the
new Pending MF3 findings-confirmation/draft-choice case `WF3-011`. It does not claim the remaining MF2 workflow is complete: MF2-08
invalidation is partial and MF2-12 session end remains unimplemented.

## Verification recorded this round

The MF2-07 case statuses are supported by the backend PR #64 CI run on
2026-10-10. Earlier MF3 evidence is retained from its own documented runs.
The 2026-10-14 integration-suite failure is retained as history and superseded
by the successful full verification on 2026-10-15. WF3-011 remains Pending;
these regression checks do not constitute its complete end-to-end procedure.

| Check | Command | Result |
| --- | --- | --- |
| MF3 confirmation/review backend integration rerun | `./mvnw.cmd spotless:apply`; `./mvnw.cmd -Dtest=InspectionReportApiIntegrationTest,InspectionReportDraftingApiIntegrationTest test` | **Not yet passing as of 2026-10-14.** The previous affected-suite run executed 32 tests with 2 remaining failures in report-return/reviewer-decision fixture behavior; stale evidence submit and all 10 drafting tests passed. Do not count WF3-011 as executed/passed. |
| Frontend findings/report review focused suite | `npm test -- --run src/features/reports/pages/ReportDetailPage.test.tsx src/features/reports/components/ReportDerivedSections.test.tsx src/features/inspections/pages/InspectionFindingsPage.test.tsx src/features/inspections/pages/InspectionDraftPage.test.tsx` | **Passed 2026-10-14.** 4 files, 29 tests, 0 failures. Includes disabled approval until reviewer decisions and confirmed findings gates. Not a complete WF3-011 end-to-end execution. |
| Frontend lint | `npm run lint` | **Passed 2026-10-14** (exit 0; six existing Fast Refresh warnings). |
| Frontend production build | `npm run build` | **Passed 2026-10-14.** TypeScript and Vite production build succeeded. |
| Backend full suite + coverage gate + Modulith boundaries | PR #64 CI workflow: `Verify (Spotless + tests + JaCoCo + Modulith checks)` | **Passed.** 334 tests, 0 failures, 0 errors, 0 skipped; JaCoCo coverage checks and Spring Modulith checks passed. The CI job ran the Maven verify build; this record does not claim a local Maven command was executed successfully. |
| Backend full MF3 confirmation/rendering suite | `./mvnw.cmd -B verify` | **Passed 2026-10-15.** 647 tests, 0 failures/errors/skips; BUILD SUCCESS. JaCoCo coverage and Spring Modulith checks passed. Includes findings confirmation/reopen/snapshot gates, Inspector-confirmed report inclusion/reviewer-rejected exclusion, post-publication finding-decision refusal, repeated candidate-review conflict handling, and evidence-upload refusal after publication. |
| Frontend full MF3 confirmation/rendering suite | `npm test -- --run` | **Passed 2026-10-15.** 54 files, 363 tests passed. Includes regressions for rejected-only no-findings acknowledgment, optional location prose, candidate-query loading guard, returned-report author verification, published-report UI state, and report finding-status copy. |
| Frontend lint and production build | `npm run lint`; `npm run build` | **Passed 2026-10-15.** Lint exit 0 with six existing warnings; TypeScript and production build succeeded. |
| Report 5 exporter tests | `python -I -m unittest discover -s "E:\\Dev\\Repos\\Capstone\\SmartDroneInspection-docs\\tools\\tests" -p "test_*.py" -v` | **Passed 2026-10-15.** 29 tests passed. The first relative-path invocation from outside the docs repository failed discovery; the absolute-path rerun passed. |
| Docs whitespace check | `git diff --check` | **Passed 2026-10-15.** No whitespace errors. |
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

Eight of the ten listed cases have executed automated-test evidence; `WF3-010`
and `WF3-011` remain Pending. These metrics describe the recorded cases, not
full feature or product coverage.

- **Test coverage** = `(Passed + Failed) × 100 ÷ (Number of TCs − N/A)` =
  `(8 + 0) × 100 ÷ (10 − 0)` = 80.00%.
- **Test successful coverage** = `Passed × 100 ÷ (Number of TCs − N/A)` =
  `8 × 100 ÷ (10 − 0)` = 80.00%.
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
| MF4 maintenance/cost/completion reporting | Workflow implementation and executed test evidence absent; no case. |
| FE-02 catalog CRUD | Implemented as a dependency of MF3, but no executed case is recorded for it. |
| FE-06 MF3-07 source-input coverage | Objective/scope/criteria, evidence metadata, scoped candidates/sessions, and the latest accepted Inspector evidence-quality comparison have prompt/context test coverage; a synthetic disposable live run generated a draft. No dedicated checklist-answer or Inspector-observation source was identified; per-section source citations and complete source-state coverage remain unverified. The live draft predates the final quality-context addition. |
| FE-06 required report content (Report 3 §3.7.2) | Linked evidence component/location projection and targeted WF3 prompt/source-input coverage are recorded; full required section-content verification remains unverified. The synthetic live draft disclosed missing fields but also described fixture images as submitted captures and recommended physical validation. |
| FE-06 LLM safeguards (Report 3 §3.7.3) | Prompt constraints and candidate/official-finding distinction have focused coverage; full safeguards, including numeric-table sourcing and untrusted evidence-metadata handling, are not asserted by `WF3-005`/`WF3-006`. |
| FE-01 subscription/workforce governance | Supporting evidence is outside workbook functional-case totals; current-role scope should be reverified separately. |
| FE-08 dashboard/analytics/notifications | No assigned case. |
| Mobile client | `flutter analyze` and `flutter test` passed (40 tests); no WFx case was added for mobile behavior. |
| Live external LLM drafting provider | Exercised against disposable synthetic evidence only; not valid evidence of real inspection output or author attestation. The run remained an unsubmitted DRAFT. |
| Backend full-suite verification | Not rerun for this slice. Historical 2026-10-13 local full-suite attempt had Testcontainers environment errors; the current focused Testcontainers drafting API suite passed. |

## Update rules

1. Update the Round 1/2/3 status in the feature source first.
2. Recount `Passed`, `Failed`, `Pending`, and `N/A` per feature.
3. Update all eight module rows and the subtotal row above.
4. Recalculate coverage; never mark a pending case as passed just to improve
   the percentage.
5. Never record a case for a workflow that has no implementation.
