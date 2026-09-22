# Jira import result — 2026-09-22

The four-week main-flow plan was imported into the SmartDroneInspection Jira project `SCRUM` on
2026-09-22 through the Atlassian Jira connector. The existing report, slide and database work was
preserved.

## Sprints

| Jira sprint ID | Name | Dates (Vietnam time) |
| ---: | --- | --- |
| 36 | W3 — Foundation & DB | 2026-09-28–2026-10-02 |
| 37 | W4 — WF1 & WF2 Core | 2026-10-05–2026-10-09 |
| 38 | W5 — WF3 & WF4 Core | 2026-10-12–2026-10-16 |
| 39 | W6 — Integration & Demo | 2026-10-19–2026-10-23 |

Sprint 36 was the existing future `Week 3 — Database Schema` sprint. Its four database issues
remain in place under the shorter name and updated foundation goal.

The three unfinished database issues were rescheduled inside W3: SCRUM-44 and SCRUM-45 are due
2026-09-30, and SCRUM-46 is due 2026-10-02. The already completed SCRUM-43 was left unchanged.

## Imported hierarchy

| Flow | Epic | Task keys |
| --- | --- | --- |
| WF1 — Assets and Periodic Scheduling | [SCRUM-54](https://capstonefall26.atlassian.net/browse/SCRUM-54) | T005–T013 → SCRUM-65–SCRUM-73 |
| WF2 — Request, Order and Assignment | [SCRUM-55](https://capstonefall26.atlassian.net/browse/SCRUM-55) | T002 → SCRUM-59; T014–T022 → SCRUM-74–SCRUM-82 |
| WF3 — Inspection, Evidence and Report | [SCRUM-56](https://capstonefall26.atlassian.net/browse/SCRUM-56) | T003 → SCRUM-63; T023–T033 → SCRUM-83–SCRUM-93 |
| WF4 — Maintenance and Billing | [SCRUM-57](https://capstonefall26.atlassian.net/browse/SCRUM-57) | T004 → SCRUM-64; T034–T045 → SCRUM-94–SCRUM-105 |

All imported tasks have the `imported-mainflow` and `plan-2026-09-22` labels, a real Jira
assignee, a parent Epic, a sprint and a date-only due date. The exact task text, path and acceptance
criterion remain in [jira-import.csv](jira-import.csv) and [tasks.md](tasks.md).

The live canonical mapping for `T001` was subsequently corrected to [SCRUM-58](https://capstonefall26.atlassian.net/browse/SCRUM-58)
under [SCRUM-108](https://capstonefall26.atlassian.net/browse/SCRUM-108) — FE-01 Identity & Access
Governance, owned by Bách. Its scope is authentication and migrations V1–V9 only; FE-04 evidence
storage/MinIO remains [T025/SCRUM-85](https://capstonefall26.atlassian.net/browse/SCRUM-85).

## Handoff links

The following `Blocks` links were created:

- SCRUM-70 (T010) blocks SCRUM-74 (T014): WF1 due-cycle event → WF2 consumer.
- SCRUM-78 (T018) blocks SCRUM-83 (T023): accepted assignment → WF3 inspection.
- SCRUM-90 (T030) blocks SCRUM-94 (T034): accepted report → WF4 ticket.
- SCRUM-101 (T041) blocks SCRUM-74 (T014): re-inspection → linked WF2 request.
- SCRUM-90 (T030) and SCRUM-101 (T041) block SCRUM-104 (T044): accepted service milestones → billing status.

## Import cleanup

During field validation, two duplicate retry issues were created and then marked `duplicate-import`
and `do-not-use`: SCRUM-61 and SCRUM-62. A temporary field-mapping check, SCRUM-60, was marked
`import-check` and `do-not-use`. They are not part of T001–T045 and should be excluded from active
board filters. The canonical T001 and T002 are SCRUM-58 and SCRUM-59. The old high-level WF1 and
WF4 placeholders, SCRUM-50 and SCRUM-53, were marked `superseded`, removed from the old active
sprint and linked in their descriptions to the new Epics; they were not deleted for history.

Useful verification queries:

```jql
project = SCRUM AND labels = "imported-mainflow" ORDER BY key ASC
project = SCRUM AND labels in ("duplicate-import", "import-check")
```
