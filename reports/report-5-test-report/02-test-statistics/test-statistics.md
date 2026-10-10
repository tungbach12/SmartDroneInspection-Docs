# Test Statistics sheet source

This table mirrors the `Test Statistics` sheet. Keep the workbook's summary
formulas and labels; update the values from the feature files after each test
round.

## Project metadata

| Field | Value |
| --- | --- |
| Project Name | SmartDroneInspection |
| Project Code | SEP490 — *confirm with project owner* |
| Test round | **2026-10-09 reset to the implemented MF3 slice.** All cases below are evidenced by executed backend and web tests. MF1, MF2 and MF4 are unimplemented and therefore have no case; this is recorded as a coverage gap, not as a passing or passing-by-default result. |
| Last updated | 2026-10-09 |

## Module summary

| No | Module code | Passed | Failed | Pending | N/A | Number of test cases |
| ---: | --- | ---: | ---: | ---: | ---: | ---: |
| 1 | MF1/MF2 (not implemented) | 0 | 0 | 0 | 0 | 0 |
| 2 | MF3 inspection evidence, findings and reporting | 5 | 0 | 0 | 0 | 5 |
| **Subtotal** |  | **5** | **0** | **0** | **0** | **5** |

`Module code` is not a free label. In the template `C11` and `C12` are formulas
— `='Feature 1'!B2` and `='Feature 2'!B2` — so this column reports whatever sits
in each sheet's `Feature` cell (`B2`). The values above therefore match the
`Feature sheet summary` block recorded in `fe-04-…md`, not the sheet names. The
remaining five columns are also formulas (`D11:G11` = `B6:E6` per-round counts,
`H11` = `B4` = `COUNTA`), so nothing in this table is typed by hand at export.

### Why the module split is uneven

- **Module 1 is empty.** MF1 (catalog creation) and MF2 (mission preparation and
  readiness) are unimplemented, so there is no case to record. The `Feature 1`
  sheet stays empty, which is an accurate gap, not a formatting error.
- **Module 2 holds all five cases**, covering FE-04 (evidence intake and the
  scoped collections), FE-05 (advisory detection and human finding
  verification) and FE-06 (report review, publication and immutability).

### Test coverage

The template computes both figures from the `Sub total` row and its own
formulas, `(Passed + Failed) * 100 / (Number of TCs - N/A)` and
`Passed * 100 / (Number of TCs - N/A)`. With 5 cases, all `Passed`, none `N/A`,
both are 100%. Update the underlying round statuses, never the percentages.

## Reset scope

The previous statistics mixed a retired five-role WF1–WF4 baseline with
unimplemented Enterprise SaaS MF1–MF4 target cases, giving 33 cases with 13
`Passed` — a total that did not describe any single system. On 2026-10-09 that
content was removed and the report was reset to the MF3 slice only.

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

The two module rows are workbook-sheet totals, not SRS feature totals.

## Outstanding gaps

| Area | Status |
| --- | --- |
| MF1 asset/drone/workforce/compliance catalog | Workflow unimplemented; no case. |
| MF2 mission preparation/assignment/readiness | Workflow unimplemented; no case. |
| MF4 maintenance/cost/completion reporting | Unimplemented; no case. |
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
3. Update the two module rows and subtotal row above.
4. Recalculate coverage; never mark a pending case as passed just to improve
   the percentage.
5. Never record a case for a workflow that has no implementation.
