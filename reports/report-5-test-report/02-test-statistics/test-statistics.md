# Test Statistics sheet source

This table mirrors the `Test Statistics` sheet. Keep the workbook's summary
formulas and labels; update the values from the feature files after each test
round.

## Project metadata

| Field | Value |
| --- | --- |
| Project Name | SmartDroneInspection |
| Project Code | SEP490 — *confirm with project owner* |
| Test round | **2026-10-10 reconciliation retains the implemented MF3 slice.** All five cases below are evidenced by executed backend and web tests. MF1, MF2 and MF4 workflow implementations are not present in the current backend baseline, so there is no MF2 case; this is a coverage gap, not a passing or passing-by-default result. |
| Last updated | 2026-10-10 |

## Module summary

| No | Module code | Passed | Failed | Pending | N/A | Number of test cases |
| ---: | --- | ---: | ---: | ---: | ---: | ---: |
| 1 | Identity, Enterprise Subscription and Workforce Governance | 0 | 0 | 0 | 0 | 0 |
| 2 | Asset, Drone, Workforce and Compliance Catalog — MF1 | 0 | 0 | 0 | 0 | 0 |
| 3 | Mission Preparation, Assignment Response and Readiness — MF2 | 0 | 0 | 0 | 0 | 0 |
| 4 | MF3 inspection evidence, findings and reporting | 2 | 0 | 0 | 0 | 2 |
| 5 | AI Vision Candidates and Human Finding Decisions | 1 | 0 | 0 | 0 | 1 |
| 6 | Inspection Report Drafting, Review and Publication — MF3 | 2 | 0 | 0 | 0 | 2 |
| 7 | Team Maintenance, Cost Control and Completion Reporting — MF4 | 0 | 0 | 0 | 0 | 0 |
| 8 | Dashboard, Analytics and Notifications | 0 | 0 | 0 | 0 | 0 |
| **Subtotal** |  | **5** | **0** | **0** | **0** | **5** |

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

- **Modules 1, 2, 3, 7 and 8 have no cases.** FE-01's supporting gates are
  recorded outside the case sheets. MF1 (catalog), MF2 (preparation/readiness)
  and MF4 (maintenance) remain Report 3 requirements, but their workflow
  services/endpoints and executed cases are absent from the current mainline; there is no case to record for
  modules 2, 3 and 7. FE-08 has no assigned case at all. These are accurate
  coverage gaps, not formatting errors.
- **Modules 4, 5 and 6 hold all five cases**: FE-04 (evidence intake and the
  scoped collections) has 2, FE-05 (advisory detection and human finding
  verification) has 1, and FE-06 (report review, publication and immutability)
  has 2.

### Test coverage

The template computes both figures from the `Sub total` row and its own
formulas, `(Passed + Failed) * 100 / (Number of TCs - N/A)` and
`Passed * 100 / (Number of TCs - N/A)`. With 5 cases, all `Passed`, none `N/A`,
both are 100%. Update the underlying round statuses, never the percentages.

## Reset and reconciliation scope

The previous statistics mixed a retired five-role WF1–WF4 baseline with
unimplemented Enterprise SaaS MF1–MF4 target cases, giving 33 cases with 13
`Passed` — a total that did not describe any single system. On 2026-10-09 that
content was removed and the report was reset to the MF3 slice only. On
2026-10-10, the PR #45 readiness claims were checked against backend `main`
(`d385a7d`): it contains MF2 readiness schema, but no readiness implementation
or named readiness tests. Therefore `WF2-008` and `WF2-009` are not included in
the current totals and are not reported as Passed. The Report 3 MF2 requirements
remain unchanged.

| Change | Before | After |
| --- | ---: | ---: |
| Cases | 33 | 5 |
| Passed | 13 | 5 |
| Failed | 0 | 0 |
| Pending | 20 | 0 |
| N/A | 0 | 0 |

The 28 removed cases (`WF1-001`–`WF1-019`, `WF2-001`–`WF2-007`, `WF3-001`,
`WF3-004`, `WF3-007`, `WF3-008`, `WF4-001`–`WF4-005`) described behavior that
no longer exists or has never been implemented. Their IDs stay reserved.

The drop from 13 `Passed` to 5 is the honest consequence of that removal. It is
not a regression, and it is **not** evidence that anything stopped working.

## Verification recorded this round

These results are the previously recorded verification for the MF3 slice; no
new product suites were run during this documentation merge. They do not support
MF2 readiness implementation or case status.

| Check | Command | Result |
| --- | --- | --- |
| Backend full suite + coverage gate + Modulith boundaries | `./mvnw -o verify` | **Passed.** 162 tests, 0 failures, 0 errors; Spotless clean; Spring Modulith boundary test passed. |
| New collection scope and paging | `./mvnw -o -Dtest=InspectionListApiIntegrationTest test` | 11/11 passed. |
| Draft-service configuration guards | `./mvnw -o -Dtest=ReportDraftConfigurationTest test` | 6/6 passed. |
| Frontend lint | `npm run lint` | No errors; 4 pre-existing fast-refresh warnings in unrelated files. |
| Frontend build | `npm run build` | Built successfully. |
| Frontend suite | `npm test -- --run` | 161/161 passed across 31 files. |

**The JaCoCo 80% gate now passes: 80.47% line and 80.34% instruction coverage.**
The gate was failing before this work — 74.66% line coverage on the original
baseline, 78% after `InspectionListApiIntegrationTest` was added. It was closed
with real tests over uncovered production code, not by excluding anything:
`ReportDraftConfigurationTest` covers the startup validation that refuses to
create a draft client unless endpoint, API key, model name and a positive
timeout are all present. Without that guard a partially configured drafting
service would fail at the first manual report, after an Inspector has already
gathered evidence.

## Supporting export-tool verification (not workbook cases)

Executed on 2026-10-10 by Claude Code (automated). These are documentation-tool
checks, not additional product test cases, and they do not change the five-case
workbook denominator or any round status/date/tester.

| Check | Command | Result |
| --- | --- | --- |
| Independent exporter suites | `python -I -m unittest discover -s tools/tests -p "test_*.py" -v` | 29 tests passed: individual CLI execution, source tables, template styles/page settings, all three round/date/tester groups, original input preservation, safe outputs, Markdown readability, eight-sheet routing/statistics, and all eight FE summary blocks. |
| Full source-backed generation | `python -I tools/export_all.py --output reports/generated/2026-10-10-eight-features-final-v4` | Nine files generated: Reports 1–3, Report 5 and five weekly workbooks. Reports with no editable source are reported as missing, not fabricated. |
| Real Office validation | `./tools/verify_office_reports.ps1 -OutputDirectory reports/generated/2026-10-10-eight-features-final-v4` | All nine files opened in local Word/Excel without saving over outputs. Report 3 opened at 58 pages with the TOC refreshed; Report 5 opened with eight feature sheets and recalculated to 5 cases, 5 Passed, 100% implemented-slice coverage, and 5 Pending in Round 2 and Round 3; first executed date/tester retained. |
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

Every case below has an executed automated test behind it, so coverage equals
success rate this round.

- **Test coverage** = `(Passed + Failed) × 100 ÷ (Number of TCs − N/A)` =
  `(5 + 0) × 100 ÷ (5 − 0)` = 100%.
- **Test successful coverage** = `Passed × 100 ÷ (Number of TCs − N/A)` =
  `5 × 100 ÷ (5 − 0)` = 100%.

Both match the template's own formulas, which exclude `N/A` cases from the
denominator rather than counting them as unverified.

These percentages describe only the MF3 slice. They must not be read as product
coverage: MF1, MF2, MF4, FE-02, FE-03, FE-07 and FE-08 are untested, and the
denominator is the implemented scope, not the SRS. Report 3 defines eight
features and roughly sixty business-flow steps; five cases over three of them
is a small fraction of the SRS, and the 100% figure is a statement about the
executed slice, not about the product.

The eight module rows are workbook-sheet totals, one per SRS feature; they are not counts of business workflows.

## Outstanding gaps

| Area | Status |
| --- | --- |
| MF1 asset/drone/workforce/compliance catalog | Workflow implementation and executed test evidence absent from current backend mainline; no case. |
| MF2 mission preparation/assignment/readiness | Report 3 requirement retained; workflow implementation and readiness tests absent from current backend mainline; no case. |
| MF4 maintenance/cost/completion reporting | Workflow implementation and executed test evidence absent from current backend mainline; no case. |
| FE-04 MF2 session records (Report 3 MF2-09–MF2-12) | No endpoint; assigned to FE-04 by Report 3 but unverified. MF3 entry is via the scoped list (`WF3-009`). |
| FE-02 catalog CRUD | Implemented as a dependency of MF3, but no executed case is recorded for it. |
| FE-06 required report content (Report 3 §3.7.2) | Not asserted by `WF3-005`/`WF3-006`. |
| FE-06 LLM safeguards (Report 3 §3.7.3) | Not asserted by `WF3-005`/`WF3-006`. |
| FE-01 subscription/workforce governance | Recorded `Pending`; existing evidence is against the retired role set. |
| FE-08 dashboard/analytics/notifications | No assigned case. |
| Mobile client | No verification recorded this round. |
| Live external LLM drafting provider | Not exercised; manual structured draft is the tested path. |
| JaCoCo 80% gate | Passing at 80.47% lines / 80.34% instructions. |

## Update rules

1. Update the Round 1/2/3 status in the feature source first.
2. Recount `Passed`, `Failed`, `Pending`, and `N/A` per feature.
3. Update all eight module rows and the subtotal row above.
4. Recalculate coverage; never mark a pending case as passed just to improve
   the percentage.
5. Never record a case for a workflow that has no implementation.
