# Test Statistics sheet source

This table mirrors the `Test Statistics` sheet. Keep the workbook's summary
formulas and labels; update the values from the feature files after each test
round.

## Project metadata

| Field | Value |
| --- | --- |
| Project Name | SmartDroneInspection |
| Project Code | SEP490 — *confirm with project owner* |
| Test round | **2026-10-10 backend MF3 + MF4 API slice.** Round 1 cases below have executed backend evidence. MF1/MF2 remain unimplemented; MF4 skills/credential issuance, notifications, MF1 re-inspection dispatch, evidence rendering and web/mobile clients remain unverified. |
| Last updated | 2026-10-10 |

## Module summary

| No | Module code | Passed | Failed | Pending | N/A | Number of test cases |
| ---: | --- | ---: | ---: | ---: | ---: | ---: |
| 1 | Feature 1 sheet (no cases: MF1/MF2 unimplemented) | 0 | 0 | 0 | 0 | 0 |
| 2 | Feature 2 sheet (FE-04/FE-05/FE-06/FE-07; MF3/MF4 backend slice) | 8 | 0 | 0 | 0 | 8 |
| **Subtotal** |  | **8** | **0** | **0** | **0** | **8** |

## Reset scope

The previous statistics mixed a retired five-role WF1–WF4 baseline with
unimplemented Enterprise SaaS MF1–MF4 target cases, giving 33 cases with 13
`Passed` — a total that did not describe any single system. On 2026-10-09 that
content was removed and the report was reset to the executed MF3 slice. On
2026-10-10 three FE-07 cases were added for MF4 backend behavior exercised by
Testcontainers/MockMvc integration tests; target behavior not implemented or
not executed remains outside the case denominator and is listed as a gap.

| Change | Before | After |
| --- | ---: | ---: |
| Cases | 33 | 5 at reset; 8 current |
| Passed | 13 | 5 at reset; 8 current |
| Failed | 0 | 0 |
| Pending | 20 | 0 |
| N/A | 0 | 0 |

The 28 cases removed at the 2026-10-09 reset (`WF1-001`–`WF1-019`,
`WF2-001`–`WF2-007`, `WF3-001`, `WF3-004`, `WF3-007`, `WF3-008`,
`WF4-001`–`WF4-005`) described retired or unimplemented behavior. Their IDs stay
reserved. The three FE-07 cases added on 2026-10-10 use new IDs after `WF3-009`;
they do not reuse the removed IDs.

The drop from 13 `Passed` to 5 at reset was the honest consequence of removing
inapplicable cases; it was not evidence that anything stopped working. The
increase from 5 to 8 is new executed evidence for the selected MF4 API slice.

## Verification recorded this round

| Check | Command | Result |
| --- | --- | --- |
| Backend full suite + coverage gate + Modulith boundaries | `.\mvnw.cmd spotless:apply verify` | **Passed.** 279 tests, 0 failures, 0 errors; Spotless clean; Spring Modulith boundary test and JaCoCo 80% gate passed. |
| MF4 API integration tests | Included in backend `verify` | Passed as part of the 278-test suite; covers work-order scope, team/credential, estimate approval/rework, execution, change control, report acceptance, reconciliation and closeout. |
| Frontend lint/build/suite | Not rerun in this backend-only task | No new frontend verification claimed. |
| Mobile format/analyze/suite | Not rerun in this backend-only task | No new mobile verification claimed. |

The JaCoCo 80% gate passed in the final backend run. No exclusion was added to
make the gate pass; real MF4 integration tests exercise the new routes and
service branches.

## Supporting FE-01 verification (not workbook cases)

Supporting gates are excluded from the functional workbook totals. FE-01
auth-flow and role-policy evidence is recorded in
`03-features/fe-01-identity-access-governance.md`. Those gates change no
workbook case status.

## Coverage summary

Every indexed case below has an executed automated test behind it, so coverage
equals success rate for this selected set of backend scenarios.

- **Test coverage** = cases with a recorded status (`Passed`, `Failed`, or
  `N/A`) ÷ total cases = 8 / 8 = 100%.
- **Successful coverage** = `Passed` cases ÷ total cases = 8 / 8 = 100%.

These percentages describe only the selected, executed backend cases; they must
not be read as full product or SRS coverage. MF1 and MF2 workflows, remaining
FE-02/FE-03 behavior, MF4 skill matching/credential issuance, notifications, MF1
re-inspection dispatch, evidence object upload/report rendering, web/mobile UI,
and FE-08 remain unverified. The denominator is the selected tested scope, not
the full SRS.

The two module rows are workbook-sheet totals, not SRS feature totals.

## Outstanding gaps

| Area | Status |
| --- | --- |
| MF1 asset/schedule setup | Unimplemented; no case. |
| MF2 request/assignment/readiness | Unimplemented; no case. |
| MF4 backend maintenance API | Partial: three FE-07 cases passed for the tested REST slice; skills/credential issuance, notifications, MF1 re-inspection dispatch, evidence object workflow, report rendering and clients remain unverified. |
| MF2 assignment/checklist entry | No endpoint; MF3 reachable only via the scoped list (`WF3-009`). |
| FE-02 asset catalog | Implemented but no executed case recorded here. |
| FE-08 dashboard/analytics/notifications | No assigned case. |
| Mobile client | No verification recorded this round. |
| Live external LLM drafting provider | Not exercised; manual structured draft is the tested path. |
| JaCoCo 80% gate | Passed in backend `verify` on 2026-10-10. |

## Update rules

1. Update the Round 1/2/3 status in the feature source first.
2. Recount `Passed`, `Failed`, `Pending`, and `N/A` per feature.
3. Update the two module rows and subtotal row above.
4. Recalculate coverage; never mark a pending case as passed just to improve
the percentage.
5. Never record a case for a workflow that has no implementation.
