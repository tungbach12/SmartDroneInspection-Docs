# Project Report — Week 2

**Project name:** SmartDroneInspection: AI-powered Infrastructure Inspection Management Platform  
**Group:** FA26SE112  
**Reporting period:** 14–20 September 2026  
**Personal contribution recorded:** Trần Tùng Bách

> Jira statuses are the snapshot retrieved on 9 October 2026; update timestamps are not assumed to be exact completion timestamps.

## I. Status Report

| # | Project Task | In-charge | Status | Notes (Work Item in Details) |
|---:|---|---|---|---|
| 1 | Prepare a concise WF3 inspection and AI-verification presentation | Trần Tùng Bách | Done in Jira | [SCRUM-37](https://capstonefall26.atlassian.net/browse/SCRUM-37). Covered evidence capture/storage, advisory YOLO candidates, Inspector confirmation/modification/rejection, report review, and Client sign-off. Due and last updated 20 Sep. |
| 2 | Reconcile the earlier WF1–WF3 presentation draft | Trần Tùng Bách | Done in Jira — deprecated task | [SCRUM-41](https://capstonefall26.atlassian.net/browse/SCRUM-41). Historical presentation work; explicitly Deprecated and not active scope. Due 19 Sep. |
| 3 | Design and initialize the WF3 database schema baseline | Trần Tùng Bách | Done in Jira | [SCRUM-43](https://capstonefall26.atlassian.net/browse/SCRUM-43). Covered inspection sessions, evidence, AI candidates, verified findings, checklists, reports, and approvals. Jira due 28 Sep; last updated 20 Sep. |
| 4 | Prepare project-context slides about infrastructure-inspection challenges | Trần Tùng Bách | Done in Jira | [SCRUM-47](https://capstonefall26.atlassian.net/browse/SCRUM-47). Presented manual-inspection limitations and the B2B inspection-service opportunity. Due and last updated 20 Sep. |
| 5 | Finalize the WF3 field-inspection, AI-verification, and report-delivery flow | Trần Tùng Bách | Done in Jira | [SCRUM-52](https://capstonefall26.atlassian.net/browse/SCRUM-52). Clarified manual RC flight execution, media ingestion, advisory AI, Inspector review, report drafting, and Client sign-off. Due and last updated 20 Sep. |

## II. Project Issues

| # | Project Issue | Owner | Status | Notes (Solution, Suggestion, etc.) |
|---:|---|---|---|---|
| 1 | A deprecated slide task remains visible alongside the current WF3 presentation task | Trần Tùng Bách | Recorded | Retain SCRUM-41 as historical/deprecated and use SCRUM-37 for the current WF3 presentation. |
| 2 | Presentation and schema work do not demonstrate an integrated end-to-end implementation | Trần Tùng Bách | Follow-up required | Track executable inspection, evidence, review, and report behavior separately from slide/schema deliverables. |

## III. Next Week Plan

| # | Project Work Item | In-charge | Deadline | Notes (Task Details, etc.) |
|---:|---|---|---|---|
| 1 | Smoke-test existing authentication and database migrations | Trần Tùng Bách | 28 Sep 2026 | [SCRUM-58](https://capstonefall26.atlassian.net/browse/SCRUM-58). Verify clean startup, Flyway V1–V9, and role fixtures without default credentials. |
| 2 | Create an accepted-assignment test fixture | Trần Tùng Bách | 28 Sep 2026 | [SCRUM-63](https://capstonefall26.atlassian.net/browse/SCRUM-63). Let WF3 tests start before the full WF2 runtime is ready while retaining real organization/role scope. |
| 3 | Implement assignment-scoped inspection start and checklist responses | Trần Tùng Bách | 30 Sep 2026 | [SCRUM-83](https://capstonefall26.atlassian.net/browse/SCRUM-83). Only an accepted assignee can start/update; required checklist responses are enforced. |
| 4 | Connect the mobile assigned-inspection list and start action | Trần Tùng Bách | 1 Oct 2026 | [SCRUM-84](https://capstonefall26.atlassian.net/browse/SCRUM-84). Show authorized assigned inspections and the corresponding start/resume action. |

## IV. Other Project Matters/Suggestions

| # | Project Matter/Suggestions | Raised By | Date | Notes |
|---:|---|---|---|---|
| 1 | Keep AI output advisory and Inspector verification explicit in presentation material | Trần Tùng Bách | 20 Sep 2026 | The workflow description does not imply autonomous defect approval or drone control. |
