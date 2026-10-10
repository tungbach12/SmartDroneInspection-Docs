# Test Statistics sheet source

This table mirrors the `Test Statistics` sheet. Keep the workbook's summary
formulas and labels; update the values from the feature files after each test
round.

## Project metadata

| Field | Value |
| --- | --- |
| Project Name | SmartDroneInspection |
| Project Code | SEP490 — *confirm with project owner* |
| Test round | **2026-10-10: the implemented MF3 slice plus the re-integrated MF2-07 readiness cases.** Every case below is evidenced by executed backend and web tests. MF1, MF4, and MF2 outside MF2-07 remain unimplemented and therefore have no case; that is recorded as a coverage gap, not as a passing or passing-by-default result. |
| Last updated | 2026-10-10 |

## Module summary

| No | Module code | Passed | Failed | Pending | N/A | Number of test cases |
| ---: | --- | ---: | ---: | ---: | ---: | ---: |
| 1 | Feature 1 sheet (FE-03/MF2-07 readiness) | 2 | 0 | 0 | 0 | 2 |
| 2 | Feature 2 sheet (FE-04/FE-05/FE-06; MF3) | 5 | 0 | 0 | 0 | 5 |
| **Subtotal** |  | **7** | **0** | **0** | **0** | **7** |

## Reset and re-integration scope

On 2026-10-09 the statistics were reset to the implemented MF3 slice alone
(5 cases, 5 `Passed`), because the previous totals mixed a retired five-role
WF1–WF4 baseline with unimplemented Enterprise SaaS MF1–MF4 target cases.

On 2026-10-10 the MF2-07 readiness decision service was re-integrated onto the
current `origin/main` (`d385a7d`) and re-verified there, which restored
`WF2-008` and `WF2-009` as `Passed` on the `Feature 1` sheet.

| Change | 2026-10-09 reset | 2026-10-10 re-integration |
| --- | ---: | ---: |
| Cases | 5 | 7 |
| Passed | 5 | 7 |
| Failed | 0 | 0 |
| Pending | 0 | 0 |
| N/A | 0 | 0 |

The 28 cases removed by the reset (`WF1-001`–`WF1-019`, `WF2-001`–`WF2-007`,
`WF3-001`, `WF3-004`, `WF3-007`, `WF3-008`, `WF4-001`–`WF4-005`) described
behavior that no longer exists or has never been implemented. Their IDs stay
reserved and are never reused.

## Verification recorded this round

| Check | Command | Result |
| --- | --- | --- |
| Backend full suite + coverage gate + Modulith boundaries | `./mvnw.cmd clean verify` | **Passed.** 293 tests, 0 failures, 0 errors, 0 skipped; Spotless clean; Spring Modulith boundary test passed (3/3); JaCoCo gate met. |
| Frontend lint | `npm run lint` | No errors; 4 pre-existing fast-refresh warnings in unrelated files. |
| Frontend build | `npm run build` | Built successfully. |
| Frontend suite | `npm test -- --maxWorkers=2` | 164/164 passed across 32 files. |
| Mobile format | `dart format --output=none --set-exit-if-changed .` | 56 files unchanged. |
| Mobile analyze | `flutter analyze` | No issues. |
| Mobile tests | `flutter test` | 16/16 passed. |

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

- **Test coverage** = cases with a recorded status (`Passed`, `Failed`, or
  `N/A`) ÷ total cases = 7 / 7 = 100%.
- **Successful coverage** = `Passed` cases ÷ total cases = 7 / 7 = 100%.

These percentages describe only the implemented MF3 slice plus MF2-07 readiness.
They must not be read as product coverage: MF1, MF4, MF2 outside MF2-07, FE-02,
FE-07 and FE-08 are untested, and the denominator is the implemented scope, not
the SRS.

The two module rows are workbook-sheet totals, not SRS feature totals.

## Outstanding gaps

| Area | Status |
| --- | --- |
| MF1 asset/schedule setup | Unimplemented; no case. |
| MF2 readiness approval/return (MF2-07) | Implemented and verified; `WF2-008`, `WF2-009` `Passed` Round 1. The HTTP endpoints were added on 2026-10-10 and are covered by `InspectionReadinessApiIntegrationTest`. |
| MF2 material-change invalidation (MF2-08) | Partly implemented. A session start refuses anything but the newest `APPROVED` decision, so an appended `INVALIDATED` or `RETURNED` decision wins over an older approval. **No service writes `INVALIDATED` yet**, because nothing can currently change a readiness source after approval. The schema already permits it. |
| MF2 field session start/postpone/abort (MF2-09/10/11) | Implemented as a service with automated evidence (`InspectionFieldSessionServiceTest`, 16 tests). **No HTTP contract and no workbook case yet.** |
| MF2 session end and MF3 hand-off (MF2-12) | Not implemented. |
| MF2 preparation and assignment response (MF2-01/02/03/06) | Implemented and covered by `InspectionPreparationApiIntegrationTest` and `InspectionAssignmentApiIntegrationTest`, but not yet given workbook cases of their own. |
| MF4 maintenance/cost/acceptance | Unimplemented; no case. |
| MF2 assignment/checklist entry | No endpoint; MF3 reachable only via the scoped list (`WF3-009`). |
| FE-02 asset catalog | Implemented but no executed case recorded here. |
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
