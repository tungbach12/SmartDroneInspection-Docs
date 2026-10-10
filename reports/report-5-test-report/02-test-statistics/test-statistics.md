# Test Statistics sheet source

This table mirrors the `Test Statistics` sheet. Keep the workbook's summary
formulas and labels; update the values from the feature files after each test
round.

## Project metadata

| Field | Value |
| --- | --- |
| Project Name | SmartDroneInspection |
| Project Code | SEP490 — *confirm with project owner* |
| Test round | **2026-10-10: MF2-07 readiness, selected MF3 behavior, and selected MF4 backend API behavior.** Every indexed case has executed Round 1 evidence. MF1, MF2 outside MF2-07, and remaining MF4 requirements are explicit gaps. |
| Last updated | 2026-10-10 |

## Module summary

| No | Module code | Passed | Failed | Pending | N/A | Number of test cases |
| ---: | --- | ---: | ---: | ---: | ---: | ---: |
| 1 | Feature 1 sheet (FE-03/MF2-07 readiness) | 2 | 0 | 0 | 0 | 2 |
| 2 | Feature 2 sheet (FE-04/FE-05/FE-06/FE-07; MF3/MF4 backend slice) | 8 | 0 | 0 | 0 | 8 |
| **Subtotal** |  | **10** | **0** | **0** | **0** | **10** |

## Reset and re-integration scope

On 2026-10-09 the statistics were reset to the executed MF3 slice alone
(5 cases, 5 `Passed`), because the previous totals mixed a retired five-role
WF1–WF4 baseline with unimplemented Enterprise SaaS MF1–MF4 target cases.

On 2026-10-10, the two MF2-07 readiness cases (`WF2-008`, `WF2-009`) were
re-integrated onto current mainline and re-verified. Three selected MF4 backend
cases (`WF3-010`–`WF3-012`) were also added from executed Testcontainers/MockMvc
scenarios. The current denominator is ten cases across both fixed workbook
feature sheets.

| Change | 2026-10-09 reset | 2026-10-10 integrated scope |
| --- | ---: | ---: |
| Cases | 5 | 10 |
| Passed | 5 | 10 |
| Failed | 0 | 0 |
| Pending | 0 | 0 |
| N/A | 0 | 0 |

The 28 cases removed by the reset (`WF1-001`–`WF1-019`, `WF2-001`–`WF2-007`,
`WF3-001`, `WF3-004`, `WF3-007`, `WF3-008`, `WF4-001`–`WF4-005`) described
retired or unimplemented behavior. Their IDs stay reserved and are never reused.

## Verification recorded this round

| Check | Command | Result |
| --- | --- | --- |
| Backend full suite + coverage gate + Modulith boundaries | `./mvnw.cmd spotless:apply verify` | **Passed.** 279 tests, 0 failures, 0 errors; Spotless clean; Spring Modulith boundary test and JaCoCo 80% gate passed. |
| MF4 API integration scenarios | Included in backend `verify` | Passed within the 279-test suite; covers tenant scope, candidates/work orders, team and credential policy, estimate/change control, work logs/report gates, independent acceptance, currency-checked reconciliation, rework and closeout. |
| Frontend lint/build/suite | `npm run lint`; `npm run build`; `npm test -- --maxWorkers=2` | Passed as recorded in the upstream 2026-10-10 Docs update: lint has 4 pre-existing unrelated warnings; build succeeded; 190/190 tests passed. These are not rerun in this backend task. |
| Mobile format/analyze/suite | `dart format --output=none --set-exit-if-changed .`; `flutter analyze`; `flutter test` | Passed as recorded in the upstream 2026-10-10 Docs update: 62 files unchanged, no analyzer issues, 40/40 tests passed. These are not rerun in this backend task. |

The JaCoCo 80% gate passed in the final backend run. No exclusions were added
to weaken the gate; backend integration and domain tests exercise the delivered
MF4 slice.

## Supporting FE-01 verification (not workbook cases)

Supporting gates are excluded from the functional workbook totals. FE-01
auth-flow and role-policy evidence is recorded in
`03-features/fe-01-identity-access-governance.md`. Those gates change no
workbook case status.

## Coverage summary

Every indexed case has an executed automated test behind it, so coverage equals
success rate for this selected set of scenarios.

- **Test coverage** = cases with a recorded status (`Passed`, `Failed`, or
  `N/A`) ÷ total cases = 10 / 10 = 100%.
- **Successful coverage** = `Passed` cases ÷ total cases = 10 / 10 = 100%.

These percentages are not full product/SRS coverage. MF1, MF2 outside MF2-07,
and MF4 skill/credential administration, notifications, linked MF1 re-inspection,
evidence-object/report rendering, and web/mobile maintenance clients remain
unverified. The denominator is the selected tested scope, not the full SRS.

The two module rows are fixed workbook-sheet totals, not SRS feature totals.

## Outstanding gaps

| Area | Status |
| --- | --- |
| MF1 asset/schedule setup | Unimplemented; no case. |
| MF2 readiness approval/return (MF2-07) | Implemented and verified; `WF2-008`, `WF2-009` Passed Round 1. Readiness sources are organization-scoped; the decision fixtures include reviewer/credential/document/permit gates. |
| MF2 material-change invalidation (MF2-08) | Partly implemented: a session start refuses a latest non-approved decision; no service currently writes `INVALIDATED`. |
| MF2 field session start/postpone/abort (MF2-09/10/11) | Runtime and client tests exist, but no workbook case in this report. MF2-12 session-end/MF3 hand-off is not implemented. |
| MF2 preparation and assignment response (MF2-01/02/03/06) | Runtime/client tests exist but no workbook cases beyond MF2-07. |
| MF4 backend maintenance API | Partial: `WF3-010`–`WF3-012` passed for selected backend paths. Required credential presence, skill matching/credential administration, notifications, linked MF1 re-inspection dispatch, evidence object workflow/report rendering and maintenance clients remain unverified. |
| FE-02 asset catalog | Implemented but no executed case recorded here. |
| FE-08 dashboard/analytics/notifications | No assigned case; notification delivery remains unimplemented. |
| Live external LLM drafting provider | Not exercised; manual structured draft is the tested path. |
| JaCoCo 80% gate | Passed in backend `verify` on 2026-10-10. |

## Update rules

1. Update the Round 1/2/3 status in the feature source first.
2. Recount `Passed`, `Failed`, `Pending`, and `N/A` per feature.
3. Update the two module rows and subtotal row above.
4. Recalculate coverage; never mark a pending case as passed just to improve
the percentage.
5. Never record a case for a workflow that has no implementation.
