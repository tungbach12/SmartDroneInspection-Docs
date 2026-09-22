# Research: FE-04 — Week 3 WF3 Inspection Execution and Evidence Foundation

**Date**: 2026-09-22

## Decision 1 — Jira is the delivery source

Jira sprint `36` is `W3 — Foundation & DB` from 2026-09-28 to 2026-10-02. Bách's committed
FE-04 tasks under parent `SCRUM-56` are `SCRUM-63/T003`, `SCRUM-83/T023`, and `SCRUM-84/T024`;
all were `To Do` at the live read on 2026-09-22. The older WF3 database issue `SCRUM-43` is
`Done`. The FE-01 foundation task `SCRUM-58/T001` is also in W3 and covers authentication and
migrations under parent `SCRUM-108`. MinIO/evidence storage belongs to the later FE-04 task
`T025/SCRUM-85`, not to FE-01.

The local four-week plan remains the parent roadmap; this folder is the focused FE-04 owner plan
for the current sprint.

## Decision 2 — Reuse the existing schema

Migrations V6–V7 and the current `inspections` entities already represent assignments,
inspections, checklist responses, evidence, findings, and reports. Week 3 adds FE-04 behavior and
tests, not another table or parallel persistence model.

## Decision 3 — Fixture first, real handoff later

WF2's database task is still in progress, so T003 provides a valid accepted assignment. The
fixture must use the same IDs, status values, constructors, and repositories as production code.
The real WF2 → WF3 event is integrated at the later G3 gate.

## Decision 4 — Mobile is focused field work

Mobile covers the Inspector assignment inbox and start action in FE-04 during Week 3.
Evidence/photo capture beyond this slice, FE-05 findings, and FE-06 report review stay in later
tasks. This keeps the mobile slice useful without duplicating the web report workflow.
