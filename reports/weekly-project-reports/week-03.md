# Project Report — Week 3

**Project name:** SmartDroneInspection: AI-powered Infrastructure Inspection Management Platform  
**Group:** FA26SE112  
**Reporting period:** 21–27 September 2026  
**Team members:** Trần Hoàng Trung Hiếu, Phùng Trung Quốc, Trần Tùng Bách, Trương Thái Như

> Week 3 established the relational database design for all four workflows, standard API response envelopes, assignment-scoped execution fixtures, and AI report drafting SPIs.

## I. Status Report

| # | Project Task | In-charge | Status | Notes (Work Item in Details) |
|---:|---|---|---|---|
| 1 | Design and initialize WF1 database schema: assets, sub-assets, drone models, and schedules | Trần Hoàng Trung Hiếu | Completed | [SCRUM-44](https://capstonefall26.atlassian.net/browse/SCRUM-44). Designed tables for asset registry, drone fleet inventory, and periodic scheduling. |
| 2 | Author schedule proposal flow specification and implementation plan in docs | Trần Hoàng Trung Hiếu | Completed | Committed `docs(wf1): add schedule proposal flow spec and implementation plan` for automated proposal creation. |
| 3 | Draft SDD Section 2: Relational database design for asset catalog and fleet inventory | Trần Hoàng Trung Hiếu | Completed | Documented schema definitions, data dictionary, and indexing strategies for MF1 tables. |
| 4 | Design and initialize WF2 database schema: inspection requests, service orders, and assignments | Phùng Trung Quốc | Completed | [SCRUM-45](https://capstonefall26.atlassian.net/browse/SCRUM-45), [SCRUM-51](https://capstonefall26.atlassian.net/browse/SCRUM-51). Defined schema for requests, assignments, and mission readiness. |
| 5 | Draft SDD Section 2: Database tables for inspection preparations and readiness decisions | Phùng Trung Quốc | Completed | Documented table structures for readiness checklists, permit links, and pilot acknowledgments. |
| 6 | Design mobile inspection assignment inbox wireframes and interaction flows | Phùng Trung Quốc | Completed | Specified mobile inspector workflow: view assigned requests, accept/reject, and inspect pre-flight checklist. |
| 7 | Smoke-test authentication fixtures, Flyway migrations V1–V9, and role security | Trần Tùng Bách | Completed | [SCRUM-58](https://capstonefall26.atlassian.net/browse/SCRUM-58). Verified clean startup, migration sequence, and RBAC authorization. |
| 8 | Create accepted-assignment test fixtures for decoupled WF3 testing | Trần Tùng Bách | Completed | [SCRUM-63](https://capstonefall26.atlassian.net/browse/SCRUM-63). Allowed WF3 inspection tests to run independently with authentic organization scope. |
| 9 | Implement assignment-scoped inspection start, checklist responses, and mobile list flow | Trần Tùng Bách | Completed | [SCRUM-83](https://capstonefall26.atlassian.net/browse/SCRUM-83), [SCRUM-84](https://capstonefall26.atlassian.net/browse/SCRUM-84). Enforced assigned-inspector scope and mandatory pre-flight checks. |
| 10 | Standardize REST API response envelopes and implement AI ReportDraftPort SPI | Trần Tùng Bách | Completed | Wrapped all backend responses in `ApiResponse<T>` and implemented OpenAI-compatible report drafting adapter. |
| 11 | Design and initialize WF4 database schema: maintenance tickets, work orders, and resolutions | Trương Thái Như | Completed | [SCRUM-46](https://capstonefall26.atlassian.net/browse/SCRUM-46). Designed tables for maintenance tickets, repair tasks, and defect closure records. |
| 12 | Draft SRS Section 3.4 Detailed Use Cases: Ticket intake from published reports | Trương Thái Như | Completed | Specified use cases for converting confirmed defects into maintenance work orders with cost estimates. |
| 13 | Draft SDD Section 2: Relational tables for maintenance cost lines and contractor tracking | Trương Thái Như | Completed | Documented schema definitions, foreign key integrity constraints, and contractor assignment tables. |

## II. Project Issues

| # | Project Issue | Owner | Status | Notes (Solution, Suggestion, etc.) |
|---:|---|---|---|---|
| 1 | WF3 tests depended on accepted-assignment state before full WF2 runtime was ready | Trần Tùng Bách | Mitigated | Created test fixture SCRUM-63 to supply valid assignment states without blocking WF3 progress. |
| 2 | Frontend and mobile clients needed consistent JSON unwrapping logic | Trần Tùng Bách | Resolved | Standardized `ApiResponse<T>` envelope unwrapping across web and Flutter clients. |

## III. Next Week Plan

| # | Project Work Item | In-charge | Deadline | Notes (Task Details, etc.) |
|---:|---|---|---|---|
| 1 | Rework workflows to align with drone-centric mainflow model (MF1–MF5) | All Members | 4 Oct 2026 | Refactor flows to emphasize drone missions and configurable organization policies. |
| 2 | Implement Docker multi-container stack for local development and CI testing | Trần Tùng Bách | 4 Oct 2026 | Build Dockerfiles for backend, frontend (Nginx SPA), and Docker Compose orchestration. |
| 3 | Author initial test cases for Report 5 (Test Report) | Trần Hoàng Trung Hiếu & Trương Thái Như | 4 Oct 2026 | Define functional test cases for asset setup and maintenance workflows. |

## IV. Other Project Matters/Suggestions

| # | Project Matter/Suggestions | Raised By | Date | Notes |
|---:|---|---|---|---|
| 1 | Preserve assignment and organization authorization in all inspection endpoints | Trần Tùng Bách | 27 Sep 2026 | Enforce tenant boundaries strictly at the service layer, not relying solely on client-side routing. |
