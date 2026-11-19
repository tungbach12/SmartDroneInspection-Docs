---
title: "Report 5 — Test Report"
weight: 10
---

# Report 5 — Test Report

This folder is the editable source for the Report 5 workbook (`Report5_Test Report.xlsx`). The workbook
template is kept unchanged under `template/`; the Markdown files are the
working source for current test cases, execution rounds, and statistics across four login roles (`ADMIN`, `MANAGER`, `CUSTOMER`, `INSPECTOR`) and eight active features (`FE-01` to `FE-08`) grouped as two features per main flow (`MF1` to `MF4`). Legacy maintenance tests are retired from active coverage.

See [README.md](README.md) for the editing workflow.

Current scope revision: **3.7** (2026-11-19). The active inventory tracks **64 cases** across eight sheets (`FE-01`–`FE-08`). Current-scope Round 1 includes 45 Passed, 0 Failed, 9 Pending, and 10 N/A. Earlier snapshots that still carried retired maintenance cases are historical context only. Round 3 has 13 Passed executions, including `WF3-029` (DroneKnowledgeAI recommendation & tenant isolation), `WF3-030` (advisory knowledge references) and `WF3-031` (Customer Mobile parity from `PR #27`); `WF3-020` and `WF3-022`–`WF3-025` remain Pending until live Nginx/Docker Compose E2E verification.
