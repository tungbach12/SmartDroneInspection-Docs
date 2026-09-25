# Research: WF3 Jira Completion

**Research date**: 2026-09-24<br>
**Outcome**: no new product or platform choice is needed. Retain the existing modular-monolith, PostgreSQL, MinIO, React, and Flutter architecture; finish the nine open Jira tasks as three feature slices with one WF3 integration gate.

## Sources examined

- Live Jira query recorded in [jira-scope.md](jira-scope.md), plus parent Epics SCRUM-56, SCRUM-106, and SCRUM-107.
- Report 3 sections 3.5–3.7 and [WF3 business flow](../../../../project-reference/business-flows.md).
- [Database design, WF3 schema](../../../../project-reference/database-design.md) and the completed SCRUM-43 schema-design task.
- Existing FE-04 [start/checklist API contract](../2026-09-22-week-3-wf3-inspection-delivery/contracts/w3-inspection-start-and-checklist.md), backend InspectionController, mobile InspectionRepository, and current web inspection page.
- Existing four-week plan's WF3 dependency gate (G3 accepted-assignment input, G4 accepted-report handoff).
- Official [MinIO Java SDK](https://github.com/minio/minio-java) example and [Spring Modulith application-events guidance](https://docs.spring.io/spring-modulith/reference/events.html).

## Decisions

### 1. Keep WF3 inside the existing inspections capability

**Decision**: Put evidence, candidate/verified finding, report, and review orchestration in the existing backend inspections module. Keep application services/controllers/DTOs there. Define the concrete outbound boundaries as feature-owned ports in inspections/spi, expose that package through the named spi interface, and implement MinIO and YOLO adapters in infrastructure/storage and infrastructure/ai. Business code must not import infrastructure.

**Rationale**: FE-04/05/06 share the inspection aggregate and are one WF3 lifecycle. The database design assigns WF3 records to inspections; Jira already points to inspections services and tests.

**Alternatives considered**: separate AI or reports business modules; rejected for this scope because no separate lifecycle or ownership boundary is in the task set and it would add cross-module coupling. A feature-owned SPI is retained only for the real outbound MinIO/YOLO boundaries required by the backend architecture.

### 2. Store bytes in MinIO and metadata in PostgreSQL; make retries idempotent

**Decision**: Define an inspections-owned EvidenceObjectStore port and implement it with MinIO's S3-compatible Java client in infrastructure/storage. Validate media and stream-compute SHA-256 before persistence. Scope duplicate detection to inspection plus checksum, use the existing unique constraint as the concurrency backstop, and return the existing evidence on an identical retry. Stream content only after backend scope checks; do not expose object keys or unrestricted URLs. A stable evidence/object identity and compensation on a failed metadata write must prevent orphaned objects from becoming visible.

**Rationale**: This matches SCRUM-85, the evidence data dictionary, and the official MinIO Java client examples. Current backend source has no MinIO Java SDK client yet; adding the narrowly required SDK dependency is part of T025, not a speculative platform layer.

**Alternatives considered**: storing file bytes in PostgreSQL (rejected by the design), trusting client-provided checksum (rejected; server computes it), or adding a shared generic storage module (rejected; the feature-owned port is implemented by the concrete infrastructure adapter).

### 3. Treat AI output as advisory and failure as non-blocking to evidence

**Decision**: Define an inspections-owned inference port and implement the configured YOLO client in infrastructure/ai. Call it only for validated eligible evidence. Persist model/version, label, confidence, and bounding box as candidate data. Only Inspector confirmation/modification or a manual finding creates official verified findings. On inference failure, leave the evidence available and allow manual entry; do not fabricate an AI candidate or block evidence access.

**Rationale**: This is explicit in Report 3, WF3 business-flow exception rules, SCRUM-86, and SCRUM-87. It preserves human review as the publication gate.

**Alternatives considered**: AI auto-promotion (rejected), discarding or hiding the evidence after AI failure (rejected), and adding a new queue/retry platform (out of scope; use existing event/configuration facilities only if already present).

### 4. Use the existing schema and append-only report-version model

**Decision**: Reuse the WF3 entities/tables defined by migration V7: inspections, checklist_responses, evidence, ai_finding_candidates, verified_findings, inspection_reports, report_versions, and peer_reviews. Accepted report versions are immutable; revisions create new linked versions. Plan no schema migration unless implementation proves a required field or constraint is absent; any change must be a new forward migration.

**Rationale**: SCRUM-43 is Done and the database design documents these tables and constraints. The current source contains the inspection aggregate and WF3 domain entities; remaining Jira work is primarily use-case, integration, client, and regression work.

**Alternatives considered**: redesigning the WF3 schema or adding a version table in this plan (rejected without an evidenced gap).

**Implementation outcome**: Report acceptance tests exposed missing persisted Client decision attribution. Forward-only migration V10 adds `client_decision_by_user_id` and `client_decision_reason`; V9 remains the notifications migration. This is the only schema change in the delivery.

### 5. Keep authorization and separation of duties in backend use cases

**Decision**: Scope every command/query to the authenticated user, active organization, accepted assignment, and report lifecycle. A Peer Reviewer must not be the report author; only a Service Manager may assign/release; a Client receives released report versions only.

**Rationale**: Role visibility is not a security boundary. Report 3 and the existing start/checklist contract define backend enforcement and hidden-resource behavior.

**Alternatives considered**: frontend-only guards (rejected), or treating a role check as sufficient (rejected).

### 6. Keep cross-feature handoffs as small Modulith events

**Decision**: Treat the accepted WF2 assignment as the WF3 input and publish a small accepted-report/billing-handoff event after Client acceptance through the inspections named events interface. Include identifiers/state needed for the handoff, not evidence bytes or secrets. Do not add a broker or generic event bus. The separate invoice implementation remains outside Bách's nine open Jira tasks.

**Rationale**: The master plan names G3/G4 handoffs and T030 explicitly requires a billing/WF4 read handoff; Spring Modulith's event publication registry records transactional listener publications and tracks completion/failure.

**Alternatives considered**: direct calls into another module's controller/service/repository (rejected by architecture), new message broker (unneeded), or implementing invoice persistence in T030 (outside its Jira scope and separately owned).

### 7. Adapt obsolete documentation targets to the current docs tree

**Decision**: For SCRUM-93, document the flow under the current docs repository's top-level backend area (planned path: `backend/flows/inspections-and-reports.md`, relative to the docs repo) if that flow guide is created. Do not recreate the retired `docs/content/` tree.

**Rationale**: The workspace documentation map and current repository structure supersede the path copied into the Jira description.

## Schedule and capacity

The nine open tasks total 13 estimated person-days and have explicit due dates from 2026-10-06 through 2026-10-23. The SCRUM-56 Epic states a 2026-09-28–2026-10-23 plan window. Jira labels the same work with internal weeks W2–W4 and sprints W4–W6; retain both fields, schedule by due date, and do not assume unrecorded capacity.

## Clarification status

No unresolved product decision blocks the plan. Inference-service endpoint/credentials are environment configuration, not a new contract choice; tests should use a stub and runtime secrets must stay outside source control. Exact response/file-size limits must follow existing project configuration and SRS non-functional requirements, not be invented here. T030 is scoped to the acceptance event/handoff; coordinate its consumer with the separately owned invoice task.
