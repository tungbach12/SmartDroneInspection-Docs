# Test Statistics sheet source

This table mirrors the `Test Statistics` sheet. Keep the workbook's summary
formulas and labels; update the values from the feature files after each test
round.

## Project metadata

| Field | Value |
| --- | --- |
| Project Name | SmartDroneInspection |
| Project Code | SEP490 — *confirm with project owner* |
| Test round | Historical WF1–WF4 evidence plus 2026-10-03 target SF/MF1–MF5 case design; no new target runtime execution in Report 5. Backend MF2 mission-plan integration tests were added under PR #54 (`364a23e`, `MissionPlanApiIntegrationTest`, `DroneMissionPlanTest`, `MissionShotItemCoordinateConstraintTest`), but no executed Report 5 run is recorded, so MF2 cases remain `Pending`. |
| Last updated | 2026-10-06 |

## Module summary

| No | Module code | Passed | Failed | Pending | N/A | Number of test cases |
| ---: | --- | ---: | ---: | ---: | ---: | ---: |
| 1 | Feature 1 sheet (FE-02/WF1 + FE-03/WF2 + target MF2; FE-01 gate separate) | 9 | 0 | 11 | 0 | 20 |
| 2 | Feature 2 sheet (FE-04–FE-07; WF3 + WF4 + target MF3–MF5) | 4 | 0 | 9 | 0 | 13 |
| **Subtotal** |  | **13** | **0** | **20** | **0** | **33** |

## Supporting FE-01 verification (not workbook cases)

Supporting gates are excluded from the functional workbook totals. On
2026-09-24, 19 role-to-screen policy tests and 26 browser-auth frontend tests
passed; the full frontend suite passed 52/52, including three shared API
envelope checks and the WF3 inspection/report page tests. Backend API-envelope
and Problem Details checks passed as part of `mvnw verify`; mobile envelope
checks passed as part of `flutter test`, and `flutter analyze` reported no
issues. Browser-auth checks use a mocked HTTP transport; this delivery did not
execute a live browser-to-auth-API end-to-end test. On 2026-09-28, the backend
client self-registration persistence gate passed: `POST /api/v1/auth/register`
returns 201 and persists organization, user, `CLIENT` role, and the
`CLIENT_REGISTRATION` audit row in one transaction
(`ClientRegistrationApiIntegrationTest`, part of the 165/165 `mvnw verify`
run). On 2026-09-28, the backend admin user creation persistence gate passed:
`POST /api/v1/platform/users` returns 201 and persists the user, role
assignment, and the `USER_CREATED` audit row in one transaction
(`AdminUserApiIntegrationTest`, part of the 167/167 `mvnw verify` run).
See `03-features/fe-01-identity-access-governance.md` for the detailed
procedure and scope. Target provider-vetting and operator-isolation checks
(`FE01-T01` and `FE01-T02`) are recorded as pending supporting gates. They
remain outside the fixed workbook count, as specified in the Report 5 mapping.

These are workbook-sheet totals, not FE totals. The eight detailed sources are
organized by FE; FE-08 has no assigned functional case in this baseline and is
not included in the denominator. The `WF1-011`–`WF1-019` cases cover the
schedule-proposal revision of WF1, while `WF2-005`–`WF2-007` (Feature 1) and
`WF3-005`–`WF4-005` (Feature 2) represent newly defined target acceptance cases
for SF/MF1–MF5, all tracked truthfully as `Pending`. `WF2-007` specifically
exercises the MF2 Drone Mission Plan, SOW-based GSD/overlap requirements and
applicable permit/airspace gates.

## Coverage summary

The summary counts each unique workbook case once using its latest completed
result across recorded rounds. The WF3-002 Round 2 recheck and the WF3-004
Round 2 narrative config/provenance recheck are not additional cases, so the
baseline Feature 2 sheet still contributes 7 baseline cases. Both WF3-004 rounds
completed as `Passed`, so the Feature 2 `Passed` count is unchanged at 4.
The nine WF1 cases added on 2026-09-28 (`WF1-011`-`WF1-019`) raise the baseline
Feature 1 sheet to 17. The nine target cases added on 2026-10-03 (`WF2-005`–`WF2-007`
on Feature 1, and `WF3-005`–`WF4-005` on Feature 2) expand the total test case index
to 33. They define target MF1–MF5 coverage for Provider RFQ isolation, uniform
commission/policy snapshots, MF2 mission-specific GSD/overlap/permit checks,
Platform AI consumption, review/settlement, complaint workflow pauses,
and maintenance change/warranty. All nine remain `Pending` in every
round because no target runtime implementation/evidence was executed; planned
features must never be represented as passed.

Use the same definitions as the workbook:

- **Test coverage** = cases with a recorded status (`Passed`, `Failed`, or
  `N/A`) ÷ total cases.
- **Successful coverage** = `Passed` cases ÷ total cases.

| Measure | Value at baseline | Formula/source |
| --- | ---: | --- |
| Test coverage | 13 / 33 = 39.4% | Count non-`Pending` statuses in Feature 1 and Feature 2. |
| Successful coverage | 13 / 33 = 39.4% | Count `Passed` statuses in Feature 1 and Feature 2. |

The two module rows are workbook-sheet totals, not SRS feature totals. This is
why the Feature 2 sheet legitimately contains `WF4-001`–`WF4-003`: those cases
map to FE-07 and WF4, even though they share the fixed Feature 2 sheet with
the WF3/FE-04–FE-06 cases. The `WF1-011`–`WF1-019` cases cover the
schedule-proposal revision of WF1 and live on the same Feature 1 sheet as the
earlier WF1/FE-02 and WF2/FE-03 cases.

## Update rules

1. Update the Round 1/2/3 status in the feature source first.
2. Recount `Passed`, `Failed`, `Pending`, and `N/A` per feature.
3. Update the two module rows and subtotal row above.
4. Recalculate coverage; never mark a pending case as passed just to improve
   the percentage.
