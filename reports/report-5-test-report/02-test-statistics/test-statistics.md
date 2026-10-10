# Test Statistics sheet source

This table mirrors the `Test Statistics` sheet. Keep the workbook's summary
formulas and labels; update the values from the feature files after each test
round.

## Project metadata

| Field | Value |
| --- | --- |
| Project Name | SmartDroneInspection |
| Project Code | SEP490 — *confirm with project owner* |
| Test round | **2026-10-10 reconciliation: MF2-07 readiness decisions plus the implemented MF3 slice.** Seven cases are recorded: `WF2-008`/`WF2-009` cover MF2-07; five cover MF3. MF2-08 source-change invalidation is partial and MF2-12 session end is unimplemented; neither is claimed as covered. |
| Last updated | 2026-10-10 |

## Module summary

| No | Module code | Passed | Failed | Pending | N/A | Number of test cases |
| ---: | --- | ---: | ---: | ---: | ---: | ---: |
| 1 | Identity, Enterprise Subscription and Workforce Governance | 0 | 0 | 0 | 0 | 0 |
| 2 | Asset, Drone, Workforce and Compliance Catalog — MF1 | 0 | 0 | 0 | 0 | 0 |
| 3 | Mission Preparation, Assignment Response and Readiness — MF2 | 2 | 0 | 0 | 0 | 2 |
| 4 | MF3 inspection evidence, findings and reporting | 2 | 0 | 0 | 0 | 2 |
| 5 | AI Vision Candidates and Human Finding Decisions | 1 | 0 | 0 | 0 | 1 |
| 6 | Inspection Report Drafting, Review and Publication — MF3 | 2 | 0 | 0 | 0 | 2 |
| 7 | Team Maintenance, Cost Control and Completion Reporting — MF4 | 0 | 0 | 0 | 0 | 0 |
| 8 | Dashboard, Analytics and Notifications | 0 | 0 | 0 | 0 | 0 |
| **Subtotal** |  | **7** | **0** | **0** | **0** | **7** |

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
- **Module 3 has the two MF2-07 readiness cases** (`WF2-008`, `WF2-009`). They
  cover readiness approval/return only; they do not establish that all MF2
  steps are complete or tested. MF2-08 source-change invalidation is partial;
  MF2-12 session end/`FIELD_COMPLETED` remains unimplemented.
- **Modules 4, 5 and 6 hold the five MF3 cases**: FE-04 (evidence intake and
  scoped collections) has 2, FE-05 (advisory detection and human finding
  verification) has 1, and FE-06 (report review, publication and immutability)
  has 2.

### Test coverage

The template computes both figures from the `Sub total` row and its own
formulas, `(Passed + Failed) * 100 / (Number of TCs - N/A)` and
`Passed * 100 / (Number of TCs - N/A)`. With 7 cases, all `Passed`, none `N/A`,
both are 100%. This is the rate for the recorded seven cases, not product or
full MF2 coverage. Update the underlying round statuses, never the percentages.

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
| Cases | 33 | 5 | 7 |
| Passed | 13 | 5 | 7 |
| Failed | 0 | 0 | 0 |
| Pending | 20 | 0 | 0 |
| N/A | 0 | 0 | 0 |

The 28 removed cases (`WF1-001`–`WF1-019`, `WF2-001`–`WF2-007`, `WF3-001`,
`WF3-004`, `WF3-007`, `WF3-008`, `WF4-001`–`WF4-005`) described behavior that
no longer exists or has never been implemented. Their IDs stay reserved.

The increase from five to seven cases reflects restored Report 5 coverage for
implemented MF2-07 approval/return. It does not claim the remaining MF2 workflow
is complete: MF2-08 invalidation is partial and MF2-12 session end remains
unimplemented.

## Verification recorded this round

The MF2-07 case statuses are supported by the backend PR #64 CI run on
2026-10-10. Earlier MF3 evidence is retained from its own documented runs. The
following fresh checks were run during this reconciliation:

| Check | Command | Result |
| --- | --- | --- |
| Backend full suite + coverage gate + Modulith boundaries | PR #64 CI workflow: `Verify (Spotless + tests + JaCoCo + Modulith checks)` | **Passed.** 334 tests, 0 failures, 0 errors, 0 skipped; JaCoCo coverage checks and Spring Modulith checks passed. The CI job ran the Maven verify build; this record does not claim a local Maven command was executed successfully. |
| Backend local full suite | `mvnw.cmd -o verify` | **Blocked by environment.** Testcontainers could not find a Docker environment; do not treat local test errors as product failures or passes. |
| Frontend lint | `npm run lint` | Passed with 4 `react(only-export-components)` warnings. |
| Frontend build | `npm run build` | Passed. |
| Frontend full suite | `npm test -- --run --maxWorkers=1` | Exit code 0. |
| Frontend affected test files | `npm test -- --run src/features/inspections/pages/InspectionsPage.test.tsx src/features/reports/pages/ReportsPage.test.tsx --maxWorkers=1` | 17/17 passed on rerun after transient failures in an earlier parallel full-suite run. |
| Mobile formatting | `dart format --set-exit-if-changed .` | 62 files checked, no changes. |
| Mobile analysis | `flutter analyze` | No issues found. |
| Mobile suite | `flutter test` | 40 passed. |

The backend case-specific tests (`InspectionReadinessServiceTest`,
`ReadinessSnapshotFactoryTest`, and `InspectionReadinessApiIntegrationTest`)
were included in the successful 334-test PR #64 CI suite. No statement here
claims the backend local suite passed.
The earlier MF3 work closed the JaCoCo gate after it had failed at 74.66% line
coverage on the original baseline and 78% after `InspectionListApiIntegrationTest`.
`ReportDraftConfigurationTest` covers startup validation requiring endpoint,
API key, model name and positive timeout. The PR #64 CI confirmation records
that the integrated backend coverage checks passed; local Docker-dependent
Testcontainers execution was unavailable in this session.

## Supporting export-tool verification (not workbook cases)

Executed on 2026-10-10 by Claude Code (automated). These are documentation-tool
checks, not additional product test cases. The previously verified export had a
five-case denominator because it predates this seven-case reconciliation; the
current source denominator is seven. Export-tool checks do not change any round
status/date/tester.

| Check | Command | Result |
| --- | --- | --- |
| Independent exporter suites | `python -I -m unittest discover -s tools/tests -p "test_*.py" -v` | 29 tests passed: individual CLI execution, source tables, template styles/page settings, all three round/date/tester groups, original input preservation, safe outputs, Markdown readability, eight-sheet routing/statistics, and all eight FE summary blocks. |
| Prior full source-backed generation | `python -I tools/export_all.py --output reports/generated/2026-10-10-eight-features-final-v4` | Nine files generated before the MF2 reconciliation: Reports 1–3, Report 5 and five weekly workbooks. Missing editable sources were reported rather than fabricated. |
| Current Report 5 generation | `python -I tools/export_all.py --only report5 --output reports/generated/2026-10-10-mf2-final` | Generated seven cases routed to Feature 3 (2), Feature 4 (2), Feature 5 (1), Feature 6 (2); manifest confirms input hashes unchanged and format parts preserved. |
| Current Report 5 Office validation | `./tools/verify_office_reports.ps1 -OutputDirectory reports/generated/2026-10-10-mf2-final` | Excel opened and recalculated the 11-sheet workbook. 7 cases / 7 Passed / 100% coverage and successful coverage; Round 2 and Round 3 each have 7 Pending. Source first-executed date/tester retained (2026-10-09 / Claude Code automated). Original generated package hash unchanged after Office read. |
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

Every listed case has executed automated-test evidence. These metrics describe
the seven recorded cases, not full feature or product coverage.

- **Test coverage** = `(Passed + Failed) × 100 ÷ (Number of TCs − N/A)` =
  `(7 + 0) × 100 ÷ (7 − 0)` = 100%.
- **Test successful coverage** = `Passed × 100 ÷ (Number of TCs − N/A)` =
  `7 × 100 ÷ (7 − 0)` = 100%.

Both match the template's own formulas, which exclude `N/A` cases from the
denominator rather than counting them as unverified. These percentages are not
product coverage: FE-02/MF1, most MF2 steps, MF4/FE-07 and FE-08 remain
unverified or unimplemented, and FE-01 support evidence is outside the
workbook-case denominator.

The eight module rows are workbook-sheet totals, one per SRS feature; they are not counts of business workflows.

## Outstanding gaps

| Area | Status |
| --- | --- |
| MF1 asset/drone/workforce/compliance catalog | Workflow implementation and executed test evidence absent; no case. |
| MF2 assignment/preparation/compliance | Implemented in part; no Report 5 cases beyond readiness decision approval/return (`WF2-008`/`WF2-009`). |
| MF2-08 source-change invalidation | Partial: start rejects unless newest readiness decision is APPROVED; no source-change workflow appends INVALIDATED. |
| MF2-12 session end / FIELD_COMPLETED handoff | Not implemented; no case. |
| MF4 maintenance/cost/completion reporting | Workflow implementation and executed test evidence absent; no case. |
| FE-02 catalog CRUD | Implemented as a dependency of MF3, but no executed case is recorded for it. |
| FE-06 required report content (Report 3 §3.7.2) | Not asserted by `WF3-005`/`WF3-006`. |
| FE-06 LLM safeguards (Report 3 §3.7.3) | Not asserted by `WF3-005`/`WF3-006`. |
| FE-01 subscription/workforce governance | Supporting evidence is outside workbook functional-case totals; current-role scope should be reverified separately. |
| FE-08 dashboard/analytics/notifications | No assigned case. |
| Mobile client | `flutter analyze` and `flutter test` passed (40 tests); no WFx case was added for mobile behavior. |
| Live external LLM drafting provider | Not exercised in this reconciliation; manual structured draft is covered by existing MF3 evidence. |
| Backend local environment | Docker unavailable for local Testcontainers; backend verification is based on successful PR #64 CI, not local test pass. |

## Update rules

1. Update the Round 1/2/3 status in the feature source first.
2. Recount `Passed`, `Failed`, `Pending`, and `N/A` per feature.
3. Update all eight module rows and the subtotal row above.
4. Recalculate coverage; never mark a pending case as passed just to improve
   the percentage.
5. Never record a case for a workflow that has no implementation.
