---
title: "Report 5 — Test Report"
weight: 10
---

# Report 5 — Test Report

This folder is the editable source for the Report 5 workbook (`Report5_Test Report.xlsx`). The workbook
template is kept unchanged under `template/`; the Markdown files are the
working source for current test cases, execution rounds, and statistics across four login roles (`ADMIN`, `MANAGER`, `CUSTOMER`, `INSPECTOR`) and twenty-four atomic features (`FE-01` to `FE-24`) spanning four main flows (`MF1` to `MF4`). Legacy maintenance tests are retired from active coverage.

See [README.md](README.md) for the editing workflow.

Current scope revision: **3.12** (2026-11-23). The 2026-11-23 `FE-06` checkpoint-lock evidence adds backend 1/1 and frontend 2/2 coverage with counts unchanged; v3.12 then aligned the FE-07/FE-08/FE-10 wording with the delivered ADMIN-only airspace review, dispatch-time partner eligibility, and shared chat limits. The active inventory tracks **67 cases** across twenty-four sheets (`Feature 1`–`Feature 24`, mapped 1-to-1 to `FE-01`–`FE-24`). Current-scope Round 1 includes 45 Passed, 0 Failed, 9 Pending, and 13 N/A (`45 / 54 = 83.33%`). Earlier snapshots that still carried retired maintenance cases are historical context only. Round 3 has 13 Passed executions, including `WF3-029` (DroneKnowledgeAI recommendation, AI note drafting, local 384d RAG & tenant isolation), `WF3-030` (advisory knowledge references) and `WF3-031` (Customer Mobile parity from `PR #27`); newly unbundled cases `WF3-032` (`FE-05`), `WF2-021` (`FE-11`), and `WF3-033` (`FE-22`) remain `N/A / Pending / Pending` without fabricated results, while `WF3-020` and `WF3-022`–`WF3-025` remain Pending until live Nginx/Docker Compose E2E verification.
