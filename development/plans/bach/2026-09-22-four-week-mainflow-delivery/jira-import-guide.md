# Jira import guide — four-week main flows

Use [jira-import.csv](jira-import.csv) with Jira Cloud **External System Import → CSV**. The CSV
is also the reconciliation source for the Jira issues imported on 2026-09-22. It has four Epics followed by
45 Tasks. Every Task has a stable `T001`–`T045` prefix matching [tasks.md](tasks.md), a parent
Epic, an owner label, a week label, a platform label, an estimate, a sprint and a due date.

## Current Jira schedule

The target project is `SCRUM` (SmartDroneInspection) and the board is `SCRUM board` (board ID 1).
The current active sprint, `Week 2 — Workflows & Slides`, ends on 2026-09-25. Sprint 36's
existing database issues were kept and renamed to `W3 — Foundation & DB`.
The future sprint setup is now:

| Sprint | Start | End | Purpose |
| --- | --- | --- | --- |
| W3 — Foundation & DB | 2026-09-28 09:00 | 2026-10-02 23:59 | DB work, fixtures, contracts and first vertical slices |
| W4 — WF1 & WF2 Core | 2026-10-05 09:00 | 2026-10-09 23:59 | WF1/WF2 core and handoffs |
| W5 — WF3 & WF4 Core | 2026-10-12 09:00 | 2026-10-16 23:59 | WF3/WF4 core and report-to-maintenance handoff |
| W6 — Integration & Demo | 2026-10-19 09:00 | 2026-10-23 23:59 | Client/mobile completion, billing and integrated demo |

The CSV contains matching `Sprint` and `Due Date` values. Due dates are date-only and
distributed within each owner's five-day capacity; they are not all set to the sprint end.

## Before import

1. Confirm the Jira project key, permissions to import, and that the project has `Epic` and
   `Task` work types. Do not import into a production board without checking the preview.
2. Confirm the four account IDs or email addresses for Hiếu, Quốc, Bách and Như. The CSV
   intentionally omits `Assignee` because names are not reliable Jira identifiers. Assign after
   import using the `owner-hieu`, `owner-quoc`, `owner-bach`, `owner-nhu` labels, or add a verified
   Assignee column before importing.
3. Review the scope and dependencies in [plan.md](plan.md) and [tasks.md](tasks.md). The week
   labels are planning buckets, not due dates; this avoids incorrect dates if the team calendar
   differs from the assumed five-day workweek.
4. Save/import the CSV as UTF-8 so Vietnamese owner names and acceptance criteria remain intact.

## Field mapping

| CSV column | Jira field | Notes |
| --- | --- | --- |
| `Work item ID` | Work item ID / Issue ID | Temporary import identifier, not a Jira key. |
| `Work type` | Work type / Issue type | `Epic` or `Task`; adapt only if project work types differ. |
| `Summary` | Summary | `T001`–`T045` prefixes make post-import reconciliation easy. |
| `Epic Name` | Epic Name, if requested | Populated for Epics only; otherwise leave unmapped. |
| `Parent` | Parent | Each Task points to one of the four preceding Epic import IDs. Do not map to legacy `Epic Link`. |
| `Description` | Description | Owner, week, path, acceptance and source task ID. |
| `Original Estimate` | Original Estimate | Seconds: 1 day = 28,800; map only if Jira time tracking is enabled. |
| `Sprint` | Sprint | Map to the exact sprint names created above. |
| `Due Date` | Due date | Date-only deadline generated from owner capacity. |
| Four `Labels` columns | Labels | Flow, week, owner, and platform. |

The importer may show slightly different field names by Jira project configuration. Use the
preview to verify that exactly four Epics and 45 child Tasks are created; a Task with no parent
means the hierarchy mapping failed. The file puts Epics before Tasks to make the parent IDs
resolvable during import. See Atlassian's [CSV import guide](https://support.atlassian.com/jira-cloud-administration/docs/import-data-from-a-csv-file/), [CSV preparation guide](https://support.atlassian.com/jira-software-cloud/docs/prepare-a-csv-file-for-import/), and [parent-ID mapping guidance](https://support.atlassian.com/jira/kb/map-issueid-parentid-fields-jira-csv-import/).

## After import

1. Reconcile all `T001`–`T045` summaries once; confirm four Epics and no orphan Tasks. The
   completed import mapping is recorded in [jira-import-result.md](jira-import-result.md).
2. Assign verified Jira users by the `owner-*` labels and verify the four Jira sprint buckets:
   W3 Sep 28–Oct 2, W4 Oct 5–9, W5 Oct 12–16, W6 Oct 19–23 (2026).
3. Create issue links for the handoff gates in [tasks.md](tasks.md): T010/T014→T012/T021,
   T018/T023→T021/T033, T030/T034→T033/T045, and T041/T014→T045. The CSV parent relationship
   alone does not express these cross-Epic dependencies.
4. Confirm each owner's weekly load is at most five estimated days. Totals are Hiếu 17,
   Quốc 17, Bách 17, Như 20 days. Như has no reserve; use the other owners' reserved time for
   integration support without changing WF4's accountability.
5. Link the actual backend, frontend, mobile and docs PRs to the relevant Jira Tasks. Keep one
   focused PR per repository and follow [Git and pull request workflow](../../../git-and-pull-requests.md).

Do not treat a successful CSV import as implementation. Every Task still needs code review,
the stated acceptance result, scope/security tests, and the repository's verification commands.
