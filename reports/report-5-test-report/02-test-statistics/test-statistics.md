# Test Statistics sheet source

This table mirrors the `Test Statistics` sheet. Keep the workbook's summary
formulas and labels; update the values from the feature files after each test
round.

## Project metadata

| Field | Value |
| --- | --- |
| Project Name | SmartDroneInspection |
| Project Code | SEP490 — *confirm with project owner* |
| Test round | Round 1 — Week 3 automated verification |
| Last updated | 2026-09-24 |

## Module summary

| No | Module code | Passed | Failed | Pending | N/A | Number of test cases |
| ---: | --- | ---: | ---: | ---: | ---: | ---: |
| 1 | Feature 1 sheet (WF1/FE-02 + WF2/FE-03; FE-01 W3 gate separate) | 0 | 0 | 8 | 0 | 8 |
| 2 | Feature 2 sheet (WF3/FE-04–FE-06 + WF4/FE-07) | 1 | 0 | 6 | 0 | 7 |
| **Subtotal** |  | **1** | **0** | **14** | **0** | **15** |

## Supporting FE-01 verification (not workbook cases)

The FE-01 supporting gates are excluded from the functional workbook totals:
19 role-to-screen policy tests and 26 browser-auth frontend tests passed in the
45-test frontend suite on 2026-09-24. The browser-auth checks use a mocked HTTP
transport; live Spring API integration was not run because Docker/backend was
unavailable. See `03-features/feature-1.md` for the detailed procedure and
scope.

## Coverage summary

Use the same definitions as the workbook:

- **Test coverage** = cases with a recorded status (`Passed`, `Failed`, or
  `N/A`) ÷ total cases.
- **Successful coverage** = `Passed` cases ÷ total cases.

| Measure | Value at baseline | Formula/source |
| --- | ---: | --- |
| Test coverage | 1 / 15 = 6.7% | Count non-`Pending` statuses in Feature 1 and Feature 2. |
| Successful coverage | 1 / 15 = 6.7% | Count `Passed` statuses in Feature 1 and Feature 2. |

The two module rows are workbook-sheet totals, not SRS feature totals. This is
why the Feature 2 sheet legitimately contains `WF4-001`–`WF4-003`: those cases
map to FE-07 and WF4, even though they share the fixed Feature 2 sheet with
the WF3/FE-04–FE-06 cases.

## Update rules

1. Update the Round 1/2/3 status in the feature source first.
2. Recount `Passed`, `Failed`, `Pending`, and `N/A` per feature.
3. Update the two module rows and subtotal row above.
4. Recalculate coverage; never mark a pending case as passed just to improve
   the percentage.
