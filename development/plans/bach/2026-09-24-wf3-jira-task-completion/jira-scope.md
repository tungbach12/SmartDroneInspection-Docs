# Jira Scope Snapshot — Bách / WF3

**Checked**: 2026-09-24<br>
**Jira site**: [capstonefall26.atlassian.net](https://capstonefall26.atlassian.net)<br>
**Assignee identity**: `currentUser()` resolved to `trantungbach26`.<br>
**JQL**: `project = SCRUM AND assignee = currentUser() ORDER BY key ASC`

The live query returned **27 assigned SCRUM issues**, one complete page (isLast=true). The Flow 3 selection below used WF3 labels, parent feature summaries, and issue summaries—not only one label. It contains **16 issues: 9 To Do, 6 Done, and 1 deprecated issue marked Done**. Eleven other assigned issues do not belong to WF3 and are outside this plan.

## WF3 parents

| Jira | Parent feature | Live status | Plan dates / note |
| --- | --- | --- | --- |
| [SCRUM-56](https://capstonefall26.atlassian.net/browse/SCRUM-56) | FE-04 — Inspection Execution & Evidence Management | To Do | Epic states 2026-09-28–2026-10-23; owner Bách. |
| [SCRUM-106](https://capstonefall26.atlassian.net/browse/SCRUM-106) | FE-05 — YOLO-assisted Defect Detection & Verification | To Do | Owner label owner-bach; children SCRUM-86–87. |
| [SCRUM-107](https://capstonefall26.atlassian.net/browse/SCRUM-107) | FE-06 — Inspection Report & Approval | To Do | Owner label owner-bach; children SCRUM-88–93. |

These parent Epics are reported by the current user but are not themselves assigned to the user; the 27 count above is the assignee query, while parents are listed for traceability.

## Outstanding assigned tasks — included in this plan

All nine rows below are Medium priority and currently To Do in Jira. Dates and estimates are taken from the live issue descriptions; due date is not inferred to be a start date.

| Jira / task | Feature | Work and acceptance from Jira | Internal week | Jira sprint | Due | Estimate |
| --- | --- | --- | --- | --- | --- | --- |
| [SCRUM-85 / T025](https://capstonefall26.atlassian.net/browse/SCRUM-85) | FE-04 | Validate evidence; SHA-256 and retry-safe metadata; MinIO storage. Reject corrupt/unsupported media; retries cannot duplicate an inspection evidence record. | W2 | W4 — WF1 & WF2 Core | 2026-10-06 | 2d |
| [SCRUM-86 / T026](https://capstonefall26.atlassian.net/browse/SCRUM-86) | FE-05 | Ingest configured AI candidates with model/confidence/bounding box; AI outage must leave evidence usable. | W2 | W4 — WF1 & WF2 Core | 2026-10-07 | 1d |
| [SCRUM-87 / T027](https://capstonefall26.atlassian.net/browse/SCRUM-87) | FE-05 | Implement confirm/modify/reject and manual finding; rejected/unreviewed candidates never become official findings. | W2 | W4 — WF1 & WF2 Core | 2026-10-08 | 1d |
| [SCRUM-88 / T028](https://capstonefall26.atlassian.net/browse/SCRUM-88) | FE-06 | Build report draft and immutable version snapshots; revisions create new versions and accepted versions cannot be overwritten. | W3 | W5 — WF3 & WF4 Core | 2026-10-13 | 2d |
| [SCRUM-89 / T029](https://capstonefall26.atlassian.net/browse/SCRUM-89) | FE-06 | Enforce author/reviewer separation; deny self-review and record change request or technical approval. | W3 | W5 — WF3 & WF4 Core | 2026-10-14 | 1d |
| [SCRUM-90 / T030](https://capstonefall26.atlassian.net/browse/SCRUM-90) | FE-06 | Manager release and Client accept/revision; Client sees only released version; acceptance emits billing/WF4 read handoff. | W3 | W5 — WF3 & WF4 Core | 2026-10-15 | 1d |
| [SCRUM-91 / T031](https://capstonefall26.atlassian.net/browse/SCRUM-91) | FE-06 | Connect web inspection and report screens; Inspector, reviewer, Manager, and Client get authorized actions/states. | W4 | W6 — Integration & Demo | 2026-10-20 | 2d |
| [SCRUM-92 / T032](https://capstonefall26.atlassian.net/browse/SCRUM-92) | FE-04 | Add mobile checklist and photo capture with failure/retry feedback for the assigned Inspector. | W4 | W6 — Integration & Demo | 2026-10-21 | 1d |
| [SCRUM-93 / T033](https://capstonefall26.atlassian.net/browse/SCRUM-93) | FE-06 | Run report/authorization regression: G3/G4 handoffs, self-review denial, hidden drafts, manual fallback, immutable acceptance. | W4 | W6 — Integration & Demo | 2026-10-23 | 2d |

**Remaining estimate**: 13 person-days across the nine open tasks. Availability/capacity is not specified by Jira and must not be assumed.

## Completed and deprecated WF3-related assigned work

These issues are included to make the ownership audit complete; they are not reopened or scheduled again.

| Jira | Summary | Live status | Plan treatment |
| --- | --- | --- | --- |
| [SCRUM-37](https://capstonefall26.atlassian.net/browse/SCRUM-37) | WF3 inspection/AI/report delivery slide | Done | Presentation prerequisite completed. |
| [SCRUM-41](https://capstonefall26.atlassian.net/browse/SCRUM-41) | Deprecated WF1–WF3 slides | Done | Historical, explicitly deprecated; no planned work. |
| [SCRUM-43](https://capstonefall26.atlassian.net/browse/SCRUM-43) | WF3 database schema design/bootstrap | Done | Schema design baseline; do not redesign schema in this plan. |
| [SCRUM-52](https://capstonefall26.atlassian.net/browse/SCRUM-52) | Finalize WF3 main flow and diagram | Done | Business-flow baseline. |
| [SCRUM-63 / T003](https://capstonefall26.atlassian.net/browse/SCRUM-63) | Accepted-assignment fixture | Done | Reuse as independent WF3 test precondition. Jira due date: 2026-09-28. |
| [SCRUM-83 / T023](https://capstonefall26.atlassian.net/browse/SCRUM-83) | Assignment-scoped start/checklist backend | Done | Baseline contract and backend behavior. Jira due date: 2026-09-30. |
| [SCRUM-84 / T024](https://capstonefall26.atlassian.net/browse/SCRUM-84) | Mobile assigned-inspection list/start | Done | Baseline mobile integration. Jira due date: 2026-10-01. |

## Planning notes from the Jira descriptions

- The Jira sprint labels (W4, W5, W6) differ from the internal-week labels (W2–W4); preserve both labels and use the explicit due dates for planning.
- The old master plan's T023/T024 items explain WF3 sequencing; this new plan uses live Jira statuses, so completed work remains a prerequisite rather than a new task.
- SCRUM-90 is the WF3 billing handoff; the separate invoice implementation is outside these nine assigned tickets and must be coordinated with its owner.
- SCRUM-93 currently names the retired path docs/content/backend/flows/inspections-and-reports.md. The implementation must not recreate docs/content/; update the relevant documentation under the current docs/backend/ structure instead.
- No Jira issues were edited by this audit.
