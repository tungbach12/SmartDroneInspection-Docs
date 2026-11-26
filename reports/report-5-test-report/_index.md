---
title: "Report 5 — Test Report"
weight: 10
---

# Report 5 — Test Report

This folder is the editable source for the Report 5 workbook (`Report5_Test Report.xlsx`). The workbook
template is kept unchanged under `template/`; the Markdown files are the
working source for current test cases, execution rounds, and statistics across four login roles (`ADMIN`, `MANAGER`, `CUSTOMER`, `INSPECTOR`) and twenty-four atomic features (`FE-01` to `FE-24`) spanning four main flows (`MF1` to `MF4`). Legacy maintenance tests are retired from active coverage.

See [README.md](README.md) for the editing workflow.

Current scope revision: **3.17** (2026-11-26). Report 5 lists 77 cases across 24 feature sheets, including 75 active cases and two superseded flight-permit cases. Current Round 1 records 52 Passed, 0 Failed, 9 Pending, and 16 N/A. Round 3 records 13 Passed executions. The FE-06 evidence records three passing web checks for Customer and Manager checkpoint visibility. FE-14 records Customer flight-data access checks before and after report publication. See the [test statistics](02-test-statistics/test-statistics.md) for round totals.
