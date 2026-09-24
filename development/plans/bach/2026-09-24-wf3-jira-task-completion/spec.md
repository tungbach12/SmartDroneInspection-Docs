# Feature Specification: WF3 Delivery Completion (FE-04–FE-06)

**Owner**: Trần Tùng Bách<br>
**Status**: Implemented; live YOLO deployment validation not run<br>
**Jira snapshot**: 2026-09-24<br>
**Scope directory**: `docs/development/plans/bach/2026-09-24-wf3-jira-task-completion/`

## Goal

Complete Bách's remaining assigned Jira work for WF3 as one traceable delivery plan: valid inspection evidence is stored and retry-safe; AI detections remain candidates until Inspector verification; and versioned inspection reports pass independent peer review, manager release, and Client acceptance/revision.

## Product scope

- FE-04 — Inspection Execution & Evidence Management (`SCRUM-56`).
- FE-05 — YOLO-assisted Defect Detection & Verification (`SCRUM-106`).
- FE-06 — Inspection Report & Approval (`SCRUM-107`).
- One WF3 journey begins from an accepted WF2 assignment and ends with a released and Client-accepted report, with a stable handoff to WF4/billing.
- Jira task status and ownership inventory is in [jira-scope.md](jira-scope.md); the plan addresses the nine live `To Do` issues only. Completed issues are retained as prerequisites/evidence, not reopened.

## Actors and authorization

- **Inspector / report author**: only the accepted, active assignee executes the inspection, uploads evidence, and creates/verifies findings for that inspection.
- **Peer Reviewer**: a qualified Inspector assigned by a Service Manager; must be different from the report author.
- **Service Manager**: assigns the reviewer, checks completeness, and releases a technically approved version.
- **Client**: can view only released report versions for its organization and may accept or request revision; it cannot edit technical findings.
- **Backend**: authoritative for role, organization, ownership, assignment, state, and separation-of-duties checks. Client route visibility is not an authorization boundary.

## User stories and acceptance criteria

### US1 — Capture a complete, authorized inspection record

As the assigned Inspector, I can complete required checklist responses and upload supported evidence to my accepted inspection so the report has traceable field data.

Acceptance:
1. Only the accepted active assignee can start/update the inspection or access its evidence; another Inspector and another organization cannot read or mutate it.
2. Upload validates file type, size, and content; records SHA-256, uploader, source, and available capture/GPS metadata; file bytes go to MinIO and metadata/object reference go to PostgreSQL.
3. A repeated upload of the same evidence for the same inspection does not create a second evidence record. An interrupted retry does not corrupt or duplicate the record.
4. Missing GPS is recorded as absent and does not invalidate otherwise valid evidence. Unsupported or corrupted media is rejected with a stable API error.

### US2 — Review AI candidates and record verified findings

As the assigned Inspector, I can confirm, modify, reject, or manually add findings while AI failure leaves stored evidence usable.

Acceptance:
1. An eligible evidence image may produce a candidate containing model name/version, predicted label, confidence, and bounding box.
2. Candidate records are not official findings. Rejected or unreviewed candidates never appear in report content or official statistics.
3. Confirm/modify operations create or update only an authorized verified finding; a manual finding is supported when AI misses a defect.
4. If the configured YOLO service is unavailable or fails, evidence remains available and the Inspector can use the manual finding path; the failure does not turn an unverified candidate into an official finding.

### US3 — Review, release, and accept an immutable report

As the report author, reviewer, Service Manager, or Client, I can progress the same inspection report through versioned technical review and customer acceptance with the correct visibility and separation of duties.

Acceptance:
1. The report draft compiles checklist responses, evidence, and Inspector-verified findings; each revision creates a new traceable version.
2. A report author cannot review/approve their own report. The assigned reviewer can request changes or technically approve; prior versions and decisions remain traceable.
3. The Service Manager can release only a technically approved, complete version. Internal drafts and peer-review comments are not Client-visible.
4. The Client sees only released versions and can accept or request clarification/revision without editing technical content.
5. Client acceptance makes that version immutable and preserves the approval history. A later correction creates a linked version rather than overwriting the accepted one.
6. Acceptance records the inspection billing milestone and publishes the agreed WF4/billing handoff; invoice persistence is coordinated with the separate billing owner/task, not silently added to this WF3 Jira scope.

### US4 — Use the workflow from web and mobile

As an authorized project user, I see only the actions and report state allowed for my role and assignment on the web or mobile client.

Acceptance:
1. Web inspection/report screens present authorized Inspector, reviewer, Manager, and Client actions and meaningful loading/empty/error states.
2. Mobile presents assigned inspections, checklist capture, and photo upload with visible validation, retry, and authorization errors.
3. Both clients consume the versioned backend contract; all security decisions remain server-side.

## Non-goals

- Drone piloting, flight-path control, autonomous telemetry, or a separate drone-operation integration.
- YOLO model training or a new AI platform; use the configured inference service and preserve manual review.
- Reworking FE-01 authentication, WF1/WF2, or WF4 implementation owned by other assignees.
- Online payments, invoice gateway integration, or expanding Bách's Jira assignment to implement the separate invoice task.
- A schema redesign or new generic module, event bus, queue, cache, or abstraction without an acceptance-driven need.

## Dependencies and source of truth

- Preconditions: a confirmed service order and accepted Inspector assignment from WF2; `SCRUM-63/T003` supplies an independent accepted-assignment fixture.
- Existing FE-04 start/list/checklist work (`SCRUM-83/T023`, `SCRUM-84/T024`) is marked Done in Jira and is the baseline for remaining evidence work (`SCRUM-85/T025`).
- Report 3 sections 3.5–3.7 and the WF3 business flow define behavior; database design defines the current WF3 schema. Jira issue IDs define Bách's delivery scope and due dates.
- Source references: [Report 3 functional requirements](../../../../reports/report-3-software-requirement-specification/03-functional-requirements.md), [WF3 business flow](../../../../project-reference/business-flows.md), [database design](../../../../project-reference/database-design.md), and the [Jira inventory](jira-scope.md).
