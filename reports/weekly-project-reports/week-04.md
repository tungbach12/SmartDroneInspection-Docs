# Project Report — Week 4

**Project name:** SmartDroneInspection: AI-powered Infrastructure Inspection Management Platform  
**Group:** FA26SE112  
**Reporting period:** 28 September–4 October 2026  
**Personal contribution recorded:** Trần Tùng Bách

> The WF3 Jira backlog below is grouped here as planned work for the current delivery cycle. Statuses are the 9 October Jira snapshot, not a historical 4 October snapshot; these tasks are not represented as completed during this reporting period.

## I. Status Report

| # | Project Task | In-charge | Status | Notes (Work Item in Details) |
|---:|---|---|---|---|
| 1 | Validate inspection evidence, calculate checksums, prevent duplicate retries, and store files in MinIO | Trần Tùng Bách | To Do in Jira | [SCRUM-85](https://capstonefall26.atlassian.net/browse/SCRUM-85). Due 6 Oct. Still To Do on 9 Oct; confirm progress/blockers and update Jira. |
| 2 | Ingest configured AI defect candidates with safe failure behavior | Trần Tùng Bách | To Do in Jira | [SCRUM-86](https://capstonefall26.atlassian.net/browse/SCRUM-86). Due 7 Oct. Still To Do on 9 Oct; confirm progress/blockers and update Jira. |
| 3 | Add Inspector actions to confirm, modify, or reject AI candidates and create manual findings | Trần Tùng Bách | To Do in Jira | [SCRUM-87](https://capstonefall26.atlassian.net/browse/SCRUM-87). Due 8 Oct. Still To Do on 9 Oct; confirm progress/blockers and update Jira. |
| 4 | Build inspection-report drafts and immutable version snapshots | Trần Tùng Bách | To Do in Jira | [SCRUM-88](https://capstonefall26.atlassian.net/browse/SCRUM-88). Due 13 Oct; revisions create versions and accepted versions cannot be overwritten. |
| 5 | Enforce report author/peer-reviewer separation | Trần Tùng Bách | To Do in Jira | [SCRUM-89](https://capstonefall26.atlassian.net/browse/SCRUM-89). Due 14 Oct; deny self-review and record a change request or technical approval. |
| 6 | Implement manager release and Client acceptance/revision actions | Trần Tùng Bách | To Do in Jira | [SCRUM-90](https://capstonefall26.atlassian.net/browse/SCRUM-90). Due 15 Oct; show Clients only released versions and provide the WF4/billing handoff upon acceptance. |
| 7 | Connect web inspection/report screens to authorized lifecycle actions | Trần Tùng Bách | To Do in Jira | [SCRUM-91](https://capstonefall26.atlassian.net/browse/SCRUM-91). Due 20 Oct. |
| 8 | Add mobile checklist and photo capture with failure/retry feedback | Trần Tùng Bách | To Do in Jira | [SCRUM-92](https://capstonefall26.atlassian.net/browse/SCRUM-92). Due 21 Oct. |
| 9 | Run report, workflow-handoff, and authorization regression tests | Trần Tùng Bách | To Do in Jira | [SCRUM-93](https://capstonefall26.atlassian.net/browse/SCRUM-93). Due 23 Oct. The task cites a retired `docs/content/` path; use the current documentation structure instead. |

## II. Project Issues

| # | Project Issue | Owner | Status | Notes (Solution, Suggestion, etc.) |
|---:|---|---|---|---|
| 1 | SCRUM-85, SCRUM-86, and SCRUM-87 remained To Do in the 9 Oct Jira snapshot despite recorded due dates of 6–8 Oct | Trần Tùng Bách | Requires status/blocker confirmation | Confirm progress and blockers in Jira before treating the work as complete or dates as accepted; a stale status alone does not prove failure. |
| 2 | SCRUM-93 points to a retired documentation path | Trần Tùng Bách | Mitigation identified | Keep documentation under the current repository structure; do not recreate `docs/content/`. |

## III. Next Week Plan

| # | Project Work Item | In-charge | Deadline | Notes (Task Details, etc.) |
|---:|---|---|---|---|
| 1 | Confirm or complete evidence storage and validation | Trần Tùng Bách | Reconfirm in Jira | Carry over [SCRUM-85](https://capstonefall26.atlassian.net/browse/SCRUM-85) if still open; its due date has passed. |
| 2 | Confirm or complete safe AI-candidate ingestion | Trần Tùng Bách | Reconfirm in Jira | Carry over [SCRUM-86](https://capstonefall26.atlassian.net/browse/SCRUM-86) if still open; evidence must remain usable when AI is unavailable. |
| 3 | Confirm or complete Inspector finding-verification actions | Trần Tùng Bách | Reconfirm in Jira | Carry over [SCRUM-87](https://capstonefall26.atlassian.net/browse/SCRUM-87) if still open; unreviewed/rejected candidates remain unofficial. |
| 4 | Begin report versioning, independent review, and release/Client acceptance | Trần Tùng Bách | 13–15 Oct 2026 | [SCRUM-88](https://capstonefall26.atlassian.net/browse/SCRUM-88), [SCRUM-89](https://capstonefall26.atlassian.net/browse/SCRUM-89), and [SCRUM-90](https://capstonefall26.atlassian.net/browse/SCRUM-90). Follow dependencies and keep Jira status current. |

## IV. Other Project Matters/Suggestions

| # | Project Matter/Suggestions | Raised By | Date | Notes |
|---:|---|---|---|---|
| 1 | Reconcile Jira status and due dates before the next progress review | Trần Tùng Bách | 9 Oct 2026 | The current status snapshot cannot establish when a task was started or completed. |
