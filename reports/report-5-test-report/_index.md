---
title: "Report 5 — Test Report"
weight: 10
---

# Report 5 — Test Report

This folder is the editable source for the Report 5 workbook (`Report5_Test Report.xlsx`). The workbook
template is kept unchanged under `template/`; the Markdown files are the
working source for test cases, execution rounds, and statistics across the five
canonical roles (`ADMIN`, `MANAGER`, `CUSTOMER`, `INSPECTOR`, `MAINTENANCE_ENGINEER`) and eight product features (`FE-01` to `FE-08`, 2 features per team member).

See [README.md](README.md) for the editing workflow.

Current source revision: **2.3** (2026-11-12). The current inventory tracks **69 cases** across `Feature 1` through `Feature 8`. Current Round 1 columns record 60 Passed, 0 Failed, 6 Pending, and 3 N/A; the separate historical Round 1 subtotal remains 65 cases (60 Passed, 0 Failed, 5 Pending; 92.31% overall / 93.75% baseline pass rate). Round 3 currently has three Passed executions (`WF3-006`, `WF3-016`, `WF3-018`); `WF3-019` remains Pending pending finance lifecycle re-verification, and `WF3-021` remains Pending until V35 database integration can run. Focused `ContractWorkflowServiceTest` passed 36/36; Contracts frontend build/lint passed; the focused API test passed 8 tests. A broader Contracts selection failed during setup and is not counted as passed.
