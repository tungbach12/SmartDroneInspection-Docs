---
title: "Report 5 — Test Report"
weight: 10
---

# Report 5 — Test Report

This folder is the editable source for the Report 5 workbook (`Report5_Test Report.xlsx`). The workbook
template is kept unchanged under `template/`; the Markdown files are the
working source for current test cases, execution rounds, and statistics across four login roles (`ADMIN`, `MANAGER`, `CUSTOMER`, `INSPECTOR`) and eight active features (`FE-01` to `FE-08`) grouped as two features per main flow (`MF1` to `MF4`). Legacy maintenance tests are retired from active coverage.

See [README.md](README.md) for the editing workflow.

Current scope revision: **3.3** (2026-11-18). The active inventory tracks **61 cases** across eight sheets (`FE-01`–`FE-08`). Current-scope Round 1 includes 45 Passed, 0 Failed, 9 Pending, and 7 N/A. Earlier snapshots that still carried retired maintenance cases are historical context only. Round 3 currently has four Passed executions (`WF3-006`, `WF3-016`, `WF3-018`, `WF3-028`); `WF3-019` and `WF3-021` remain Pending pending finance/refund lifecycle re-execution, `WF3-026`–`WF3-027` remain Pending for connected scheduled/HTTP execution, and `WF3-022`–`WF3-025` remain Pending until live Nginx/Docker Compose E2E verification.
