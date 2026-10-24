# Project Report — Week 4

**Project name:** SmartDroneInspection: AI-powered Infrastructure Inspection Management Platform  
**Group:** FA26SE112  
**Reporting period:** 28 September–4 October 2026  
**Team members:** Trần Hoàng Trung Hiếu, Phùng Trung Quốc, Trần Tùng Bách, Trương Thái Như

> Week 4 delivered the drone-centric mainflow redesign (MF1–MF5), Docker containerization, periodic schedule proposals, and mobile field checklist prototypes.

## I. Status Report

| # | Project Task | In-charge | Status | Notes (Work Item in Details) |
|---:|---|---|---|---|
| 1 | Rework WF1: Asset Registration & Periodic Scheduling aligned with drone-centric model | Trần Hoàng Trung Hiếu | Completed | [REWORK-WF1]. Realigned asset catalog, drone inventory, and periodic scheduling with configurable intervals. |
| 2 | Synchronize SRS, business flows, data model, and test report for schedule proposals in docs | Trần Hoàng Trung Hiếu | Completed | Committed PR #25 across documentation repository to align schedule proposal lifecycle. |
| 3 | Implement frontend screens for asset catalog, periodic schedule proposal creation, and review | Trần Hoàng Trung Hiếu | Completed | Delivered frontend PR #9 adding asset lists, schedule proposal modals, and catalog management. |
| 4 | Author Report 5 test cases FE-01 (Asset Registration) and FE-02 (Periodic Scheduling) | Trần Hoàng Trung Hiếu | Completed | Documented test scenarios, preconditions, steps, and expected results for asset and schedule features. |
| 5 | Rework WF2: Inspection Requests & Assignments with strict readiness checks | Phùng Trung Quốc | Completed | [REWORK-WF2]. Added pre-flight readiness checks: flight permits, pilot credentials, checklist templates. |
| 6 | Document periodic inspection handoff and mission preparation state machine | Phùng Trung Quốc | Completed | Committed PR #26 and #27 aligning request creation from approved periodic proposals to pilot dispatch. |
| 7 | Draft SDD Section 3: Sequence diagram for inspection request triage, quote review, and assignment | Phùng Trung Quốc | Completed | Modeled end-to-end interactions between Client, Org Admin, and Inspector in UML sequence diagrams. |
| 8 | Scaffold Flutter mobile app: Implement inspection assignment card and preparation checklist | Phùng Trung Quốc | Completed | Built Flutter UI for assigned inspection card, permit summary view, and readiness checklist submission. |
| 9 | Rework WF3: Field Inspection, AI-Assisted Verification & Reporting | Trần Tùng Bách | Completed | [REWORK-WF3]. Decoupled flight execution phase from post-flight evidence processing and report authoring. |
| 10 | Containerize backend (Spring Boot 3) and frontend (Nginx SPA) with Docker Compose | Trần Tùng Bách | Completed | Added multi-stage Dockerfiles and `docker-compose.yml` for unified local and CI containerized deployment. |
| 11 | Align project scope in docs: Drone-centric mainflows (MF1–MF5), canonical roles, author verification | Trần Tùng Bách | Completed | Updated SRS and PMP: unified PROVIDER_MANAGER role, removed peer review requirement, made author verify AI. |
| 12 | Fix backend security-audit insert foreign key flush issue | Trần Tùng Bách | Completed | Resolved persistence order issue where user must be flushed before security audit records are written. |
| 13 | Rework WF4: Maintenance Assessment & Defect Resolution from published findings | Trương Thái Như | Completed | [REWORK-WF4]. Modeled maintenance work order ingestion directly from confirmed report defect findings. |
| 14 | Formalize Maintenance Work Order state machine in SRS Section 3.4 | Trương Thái Như | Completed | Defined lifecycle: NEW -> ESTIMATING -> APPROVED -> IN_PROGRESS -> RESOLVED -> CLOSED. |
| 15 | Draft SDD Section 3: Sequence diagrams for maintenance contractor dispatch and client sign-off | Trương Thái Như | Completed | Modeled maintenance quotation review, contractor assignment, task execution, and client approval. |
| 16 | Review Flyway schema migrations V10–V21 for maintenance ticket and defect linkages | Trương Thái Như | Completed | Verified foreign keys, check constraints, and DISPUTED status transitions in migration V21. |

## II. Project Issues

| # | Project Issue | Owner | Status | Notes (Solution, Suggestion, etc.) |
|---:|---|---|---|---|
| 1 | SCRUM-85 to SCRUM-87 backlog items were planned for implementation in subsequent sprint | Trần Tùng Bách | Recorded | Carried over into Week 5 sprint for complete evidence storage, YOLO inference, and findings review. |
| 2 | Documentation had references to retired `docs/content/` directory | Trần Tùng Bách | Resolved | Re-anchored all documentation paths to the active repository layout. |

## III. Next Week Plan

| # | Project Work Item | In-charge | Deadline | Notes (Task Details, etc.) |
|---:|---|---|---|---|
| 1 | Execute Enterprise SaaS architecture and role cutover (V22–V25) | Trần Tùng Bách | 11 Oct 2026 | Migrate to multi-tenant organization schema and canonical role model. |
| 2 | Implement full MF1 resource management (drones, permits, workforce credentials) | Trần Hoàng Trung Hiếu | 11 Oct 2026 | Deliver backend entities and APIs for Org Admin resource operations. |
| 3 | Implement mobile field session execution (MF2-09 to MF2-11) and readiness reviews | Phùng Trung Quốc | 11 Oct 2026 | Wire mobile field session routes with backend readiness checks. |
| 4 | Implement maintenance work order aggregate and task items (MF4-01 to MF4-08) | Trương Thái Như | 11 Oct 2026 | Build backend domain models and repositories for maintenance execution. |

## IV. Other Project Matters/Suggestions

| # | Project Matter/Suggestions | Raised By | Date | Notes |
|---:|---|---|---|---|
| 1 | Maintain clean git history and pull request standards across all four repos | Trần Tùng Bách | 4 Oct 2026 | Enforce conventional commits and peer review for all merges into main. |
