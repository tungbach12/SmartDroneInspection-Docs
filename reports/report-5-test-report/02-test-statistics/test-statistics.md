# Test Statistics sheet source

This table mirrors the `Test Statistics` sheet. Keep the workbook's summary
formulas and labels; update the values from the feature files after each test
round.

## Project metadata

| Field | Value |
| --- | --- |
| Project Name | SmartDroneInspection |
| Project Code | SEP490 — *confirm with project owner* |
| Test round | Week 3 verification, plus the 2026-09-28 WF1 schedule-proposal revision |
| Last updated | 2026-09-28 |

## Module summary

| No | Module code | Passed | Failed | Pending | N/A | Number of test cases |
| ---: | --- | ---: | ---: | ---: | ---: | ---: |
| 1 | Feature 1 sheet (WF1/FE-02 + WF2/FE-03; FE-01 W3 gate separate) | 9 | 0 | 8 | 0 | 17 |
| 2 | Feature 2 sheet (WF3/FE-04–FE-06 + WF4/FE-07) | 4 | 0 | 3 | 0 | 7 |
| **Subtotal** |  | **13** | **0** | **11** | **0** | **24** |

## Supporting FE-01 verification (not workbook cases)

Supporting gates are excluded from the functional workbook totals. On
2026-09-24, 19 role-to-screen policy tests and 26 browser-auth frontend tests
passed; the full frontend suite passed 52/52, including three shared API
envelope checks and the WF3 inspection/report page tests. Backend API-envelope
and Problem Details checks passed as part of `mvnw verify`; mobile envelope
checks passed as part of `flutter test`, and `flutter analyze` reported no
issues. Browser-auth checks use a mocked HTTP transport; this delivery did not
execute a live browser-to-auth-API end-to-end test. See
`03-features/feature-1.md` for the detailed procedure and scope.

## Coverage summary

The summary counts each unique workbook case once using its latest completed
result across recorded rounds. The WF3-002 Round 2 recheck is not an additional
case, so the Feature 2 sheet still contributes 7. The nine WF1 cases added on
2026-09-28 (`WF1-011`-`WF1-019`) raise the Feature 1 sheet to 17 and the
grand total to 24. `WF1-017` counts as `Passed` for its producer-side
assertions only; its WF2 consumer half is pending T021 and is recorded as a note
rather than a separate case.

Use the same definitions as the workbook:

- **Test coverage** = cases with a recorded status (`Passed`, `Failed`, or
  `N/A`) ÷ total cases.
- **Successful coverage** = `Passed` cases ÷ total cases.

| Measure | Value at baseline | Formula/source |
| --- | ---: | --- |
| Test coverage | 13 / 24 = 54.2% | Count non-`Pending` statuses in Feature 1 and Feature 2. |
| Successful coverage | 13 / 24 = 54.2% | Count `Passed` statuses in Feature 1 and Feature 2. |

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
