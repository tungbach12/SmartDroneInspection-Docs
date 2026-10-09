# Test Statistics sheet source

This table mirrors the `Test Statistics` sheet. Keep the workbook's summary
formulas and labels; update the values from the feature files after each test
round.

## Project metadata

| Field | Value |
| --- | --- |
| Project Name | SmartDroneInspection |
| Project Code | SEP490 — *confirm with project owner* |
| Test round | Historical WF1–WF4 evidence plus Enterprise SaaS target cases. `WF2-008` and `WF2-009` have Round 1 automated PostgreSQL evidence recorded; their Rounds 2–3 and other unexecuted target rounds remain `Pending`. |
| Last updated | 2026-10-09 |

## Module summary

| No | Module code | Passed | Failed | Pending | N/A | Number of test cases |
| ---: | --- | ---: | ---: | ---: | ---: | ---: |
| 1 | Feature 1 sheet (FE-02/WF1 + FE-03/WF2 + target MF1–MF2; FE-01 gate separate) | 13 | 0 | 9 | 0 | 22 |
| 2 | Feature 2 sheet (FE-04–FE-07; WF3 + WF4 + target MF3–MF4) | 4 | 0 | 9 | 0 | 13 |
| **Subtotal** |  | **17** | **0** | **18** | **0** | **35** |

## Supporting FE-01 verification (not workbook cases)

Supporting gates are excluded from the functional workbook totals. On
2026-10-08 the Enterprise SaaS reset was executed and recorded: backend
`./mvnw clean verify` passed 88 tests (exit 0) covering organization
registration into `audit_events`, fail-closed V24 role migration, the exact
41-table target schema and Modulith boundaries; frontend passed 128 tests plus
build; mobile passed 16 tests with format/analyze clean. These gates change no
workbook case status. On
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
procedure and scope. Target organization/entitlement and role
separation-of-duties checks (`FE01-T01` and `FE01-T02`) are recorded as pending
supporting gates. They remain outside the fixed workbook count, as specified in
the Report 5 mapping.

These are workbook-sheet totals, not FE totals. The eight detailed sources are
organized by FE; FE-08 has no assigned functional case in this baseline and is
not included in the denominator. The WF1–WF4 results are historical/retired v1
evidence; their recorded `Passed` statuses remain evidence only for the earlier
five-role behavior tested, not for the current reset branch. The `WF1-011`–
`WF1-019` cases record the schedule-proposal revision of v1 WF1. Eleven target
acceptance cases (`WF2-005`–`WF2-009` and `WF3-005`–`WF4-005`) describe Enterprise
SaaS MF1–MF4 criteria. `WF2-008` and `WF2-009` passed Round 1 on 2026-10-09
using automated PostgreSQL/Testcontainers integration tests; their Rounds 2–3
remain `Pending`. The other unexecuted target cases remain `Pending` in every
round. `WF2-007` remains the broad MF2 gate; `WF2-008` and `WF2-009` detail
independent approval and return-observation semantics. V24/V25 reset verification
is not workflow execution.

## Coverage summary

The summary counts each unique workbook case once using its latest completed
result across recorded rounds. The WF3-002 Round 2 recheck and the WF3-004
Round 2 narrative config/provenance recheck are not additional cases, so the
baseline Feature 2 sheet still contributes 7 historical v1 cases. Both WF3-004
rounds completed as `Passed`, so the historical v1 Feature 2 `Passed` count is 4.
The nine WF1 cases added on 2026-09-28 (`WF1-011`–`WF1-019`) raise the historical
Feature 1 sheet to 17. The nine target cases added on 2026-10-03 (`WF2-005`–
`WF2-007` on Feature 1, and `WF3-005`–`WF4-005` on Feature 2) expanded the index
to 33 at that historical revision. Two detailed MF2-07 cases (`WF2-008`–`WF2-009`) added on 2026-10-09 bring
the total to 35. They cover independent approval gates and return observed-source
auditing. The nine MF1–MF4 target cases previously recorded remain `Pending`. WF2-008
and WF2-009 are `Passed` in Round 1 from the 2026-10-09 PostgreSQL/Testcontainers
integration run recorded in FE-03; their Rounds 2–3 remain `Pending`. The full Backend
`./mvnw clean verify` passed 220 tests with JaCoCo coverage and Modulith checks
met. Current formal totals are 17 Passed, 18 Pending, 0 Failed and 0 N/A across
35 cases. Preserve historical v1 Passed results as v1 evidence only, and never
represent a target feature as passed without recorded execution.

Use the same definitions as the workbook:

- **Test coverage** = cases with a recorded status (`Passed`, `Failed`, or
  `N/A`) ÷ total cases.
- **Successful coverage** = `Passed` cases ÷ total cases.

| Measure | Value at baseline | Formula/source |
| --- | ---: | --- |
| Test coverage | 17 / 35 = 48.6% | Count non-`Pending` statuses in Feature 1 and Feature 2. |
| Successful coverage | 17 / 35 = 48.6% | Count `Passed` statuses in Feature 1 and Feature 2. |

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
