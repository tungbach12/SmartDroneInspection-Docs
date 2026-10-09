# Project Report — Week 3

**Project name:** SmartDroneInspection: AI-powered Infrastructure Inspection Management Platform  
**Group:** FA26SE112  
**Reporting period:** 21–27 September 2026  
**Personal contribution recorded:** Trần Tùng Bách

> Jira statuses are the snapshot retrieved on 9 October 2026. Completed items below were last updated on 24 September in Jira. Later tasks are listed in the plan, not represented as completed.

## I. Status Report

| # | Project Task | In-charge | Status | Notes (Work Item in Details) |
|---:|---|---|---|---|
| 1 | Smoke-test authentication fixtures and migrations V1–V9 | Trần Tùng Bách | Done in Jira | [SCRUM-58](https://capstonefall26.atlassian.net/browse/SCRUM-58). Foundation check for the inspection workflow. Due 28 Sep; last updated 24 Sep. |
| 2 | Create an accepted-assignment fixture for independent inspection testing | Trần Tùng Bách | Done in Jira | [SCRUM-63](https://capstonefall26.atlassian.net/browse/SCRUM-63). Enabled WF3 tests before the full WF2 runtime was ready while retaining real role/organization identifiers. Due 28 Sep; last updated 24 Sep. |
| 3 | Implement assignment-scoped inspection start and checklist responses | Trần Tùng Bách | Done in Jira | [SCRUM-83](https://capstonefall26.atlassian.net/browse/SCRUM-83). Enforced accepted-assignee scope and required checklist responses. Due 30 Sep; last updated 24 Sep. |
| 4 | Connect the mobile assigned-inspection list and start flow | Trần Tùng Bách | Done in Jira | [SCRUM-84](https://capstonefall26.atlassian.net/browse/SCRUM-84). Connected the Inspector's assigned-work view and authorized start action. Due 1 Oct; last updated 24 Sep. |

## II. Project Issues

| # | Project Issue | Owner | Status | Notes (Solution, Suggestion, etc.) |
|---:|---|---|---|---|
| 1 | WF3 tests depend on an accepted-assignment state before the full WF2 runtime handoff is ready | Trần Tùng Bách | Mitigated for independent tests | SCRUM-63 supplies a scoped fixture. Replace it with the real WF2 handoff when integration is ready; the fixture does not prove the integrated handoff. |

## III. Next Week Plan

| # | Project Work Item | In-charge | Deadline | Notes (Task Details, etc.) |
|---:|---|---|---|---|
| 1 | Implement evidence validation, checksum, retry-safe metadata, and MinIO storage | Trần Tùng Bách | 6 Oct 2026 | [SCRUM-85](https://capstonefall26.atlassian.net/browse/SCRUM-85). Reject corrupt/unsupported media and prevent retry-created duplicate evidence records. |
| 2 | Add configured AI-candidate ingestion with safe failure behavior | Trần Tùng Bách | 7 Oct 2026 | [SCRUM-86](https://capstonefall26.atlassian.net/browse/SCRUM-86). Preserve model, confidence, and bounding-box details; evidence remains usable if AI is unavailable. |
| 3 | Implement candidate confirmation/modification/rejection and manual findings | Trần Tùng Bách | 8 Oct 2026 | [SCRUM-87](https://capstonefall26.atlassian.net/browse/SCRUM-87). Pending or rejected AI candidates must not become official findings. |

## IV. Other Project Matters/Suggestions

| # | Project Matter/Suggestions | Raised By | Date | Notes |
|---:|---|---|---|---|
| 1 | Preserve assignment and organization authorization in inspection start/update paths | Trần Tùng Bách | 27 Sep 2026 | Client-side assigned-work visibility does not replace backend scope enforcement. |
