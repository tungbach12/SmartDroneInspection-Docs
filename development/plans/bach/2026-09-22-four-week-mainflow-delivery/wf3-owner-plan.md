# WF3 Plan — Bách

**Owner**: Bách
**Flow**: WF3 — Inspection, Evidence, Findings, and Report
**Jira Epic**: `SCRUM-56`
**Capacity**: 17 planned days + 3 reserve days

## Outcome

An accepted assignment produces an evidence-backed, human-verified, immutable report. AI output
remains a candidate until an Inspector verifies it, and the report author cannot peer-review it.

## Owner tasks

- `T003` — accepted-assignment fixture for independent WF3 development.
- `T023`–`T024` — assignment-scoped inspection/checklist and mobile start view.
- `T025`–`T027` — evidence storage, candidate ingestion, and verified/manual findings.
- `T028`–`T030` — report versions, peer review, release, and Client acceptance.
- `T031`–`T033` — web/mobile screens, regression, and flow documentation.

The full task descriptions, estimates, acceptance criteria, and Jira mapping remain in
[tasks.md](tasks.md).

## Delivery windows

| Jira sprint | Dates | Focus |
| --- | --- | --- |
| W3 — Foundation & DB | Sep 28–Oct 2 | Assignment fixture, inspection/checklist API |
| W4 — WF1 & WF2 Core | Oct 5–9 | Evidence, AI candidates, verified findings |
| W5 — WF3 & WF4 Core | Oct 12–16 | Report versions, review, release, acceptance |
| W6 — Integration & Demo | Oct 19–23 | Web/mobile completion and regression |

## Handoff and acceptance

- Only the accepted assignee can start/update an inspection and submit evidence.
- Unsupported/corrupt files fail safely; retries do not duplicate evidence records.
- Rejected or unreviewed candidates never become official findings.
- Accepted reports are immutable versions; the author and peer reviewer must be different.
- G4 is green when Client-accepted findings are available for WF4 ticket creation.

## References

- [Shared four-week plan](plan.md)
- [Shared handoff contract](flow-handoffs.md)
- [Jira import guide](jira-import-guide.md)
