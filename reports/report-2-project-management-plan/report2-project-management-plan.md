---
title: "Report 2 Project Management Plan"
document_type: capstone-report
report_number: 2
source_docx: report2-project-management-plan.docx
---

# I. Record of Changes

| Date | A* / M, D | In charge | Change Description |
| --- | --- | --- | --- |
| 11 Sep 2026 | A | Team | Version 1.0: Initial Project Management Plan (PMP). |
| 03 Nov 2026 | M | Team | Version 2.0: Synchronized WBS, risk register, RACI matrix, and quality plan with the 5-role / 8-feature target. |
| 17 Nov 2026 | M | Team | Version 3.0: Rewritten against the delivered product. WBS re-derived for the then-current six-feature set (`FE-01`–`FE-06`) and twelve functions; effort re-estimated and reconciled with available team capacity; risk register, training plan, deliverables, RACI, and tools aligned to the four-role scope and the `V1`+`V2` schema baseline. |
| 18 Nov 2026 | M | Team | Version 3.1: WBS re-derived for the four-main-flow, eight-feature model (`MF1`–`MF4`, `FE-01`–`FE-08`, two features per flow) at sixteen functions. Total effort re-estimated to 208 man-days and reconciled against the same 300 person-day raw allocation at 70% effective capacity. Risk 1, the objectives, the quality table, the training plan, and the deliverable descriptions updated to match. |
| 19 Nov 2026 | M | Team | Version 3.2: Synchronized scope, WBS, risk register, deliverables, and tooling with the delivered forward-only `V1`–`V4` and `V60`–`V62` schema (45 application tables / 47 total PostgreSQL tables) and `DroneKnowledgeAI` historical-case recommendation; recorded Mobile Customer parity (`PR #27`) and the final verified automated test execution. Total effort remains reconciled at 208 man-days across 300 raw person-days. |
| 20 Nov 2026 | M | Team | Version 3.3: Extended the schema and AI tooling baseline through `V63`–`V65` (applied Flyway set `V1`–`V4` and `V60`–`V65`, retaining 45 application tables / 47 total PostgreSQL tables): `70.00` default AI auto-confirm threshold (`V63`), historical published-case backfill (`V64`), local `fastembed` `vector(384)` multilingual embeddings hosted in `ai-inference` (`V65`), finding/batch AI note drafting (`Draft note with AI` / `Draft all notes`), and finding confirmation status filter chips. |
| 21 Nov 2026 | M | Team | Version 3.4: Split the WBS and RACI matrix into twenty-four atomic product features (`FE-01`–`FE-24`) plus four cross-cutting workstreams aligned to member ownership and weighted contribution (`24%` Hiếu / `50` md, `24%` Quốc / `50` md, `28%` Bách / `58` md, `24%` Như / `50` md; `208` man-days total), and synchronized plain-text building ownership details, concise recurring request titles, and streamlined service-request and quotation workflows. |

*A - Added M - Modified D - Deleted

# II. Project Management Plan

## 1. Overview

### 1.1 Scope & Estimation

SmartDroneInspection is a platform-operated service for infrastructure inspection. Customer organizations register their assets, raise one-time or recurring inspection service requests, negotiate priced quotations, accept them, and sign a paper service agreement. The platform then coordinates qualified partner drone Inspectors to execute the flights, collect photographic and video evidence, confirm defect findings against vision-model proposals, and produce an inspection report that a Manager independently reviews and publishes for the Customer's acceptance and payment.

The delivered scope covers four main flows — onboarding (`MF1`), buildings and commercial agreement through dispatch (`MF2`), field work through evidence and findings (`MF3`), and report review through payment settlement (`MF4`) — organised as twenty-four atomic product features (`FE-01`–`FE-24`) without grouping unrelated workflows. Work is decomposed below by owner workstream and cross-cutting tracks; complexity uses `Simple`, `Medium`, and `Complex`, and effort is expressed in man-days.

The delivered persistence baseline covers 45 application tables (47 total PostgreSQL tables) managed through forward-only migrations and verified by automated schema checks. It encompasses plain-text building ownership details alongside structural specifications, the tenant-isolated `DroneKnowledgeAI` case and engineering-standard advisor with automatic keyword fallback when embeddings are unavailable, configurable AI auto-confirm defaults (`70%`), historical case indexing, re-inspection verdict expiry and payment-due deadlines, optional quotation-stage partner assignment, private Inspector–Customer inspection chat, streamlined service-request and quotation screens, and full Customer mobile app parity. The total effort remains reconciled at **208 man-days** (`50 / 50 / 58 / 50` = `24% / 24% / 28% / 24%`) against 300 raw person-days.

| # | WBS Item | Complexity | Est. Effort (man-days) |
| --- | --- | --- | --- |
| 1 | Onboarding, Airspace Map & Financial Ledger (`FE-01`–`FE-05`) | Complex | 43 |
| 1.1 | `FE-01` Account Authentication, OTP & 4-Role Access Control (`MF1`) | Complex | 10 |
| 1.2 | `FE-02` Partner Inspector Application & Qualification Management (`MF1`) | Complex | 9 |
| 1.3 | `FE-03` Inspector-Owned Drone Registration & Fleet Management (`MF1`) | Complex | 10 |
| 1.4 | `FE-04` Interactive Location Map & No-Fly Zone Airspace Screening (`MF1`) | Medium | 7 |
| 1.5 | `FE-05` Financial History & Revenue/Payment Ledger (`MF4` ledger views) | Medium | 7 |
| 2 | Buildings, Commercial Service, Chat & Notifications (`MF2`, `FE-06`–`FE-12`) | Complex | 45 |
| 2.1 | `FE-06` Building Asset Registry, Checkpoints & Reference Documents | Complex | 8 |
| 2.2 | `FE-07` Restricted Airspace Review & Clearance Decision | Medium | 5 |
| 2.3 | `FE-08` Service Requests (One-Time & Recurring) & VND Quotations | Complex | 9 |
| 2.4 | `FE-09` Offline Signed Contract & Occurrence Dispatch Scheduling | Complex | 8 |
| 2.5 | `FE-10` Dual-Channel Messaging (Order Chat & Inspection Chat) | Medium | 6 |
| 2.6 | `FE-11` Assignment Acceptance Timeout & Escalation Handling | Simple | 4 |
| 2.7 | `FE-12` System Notifications & Alert Center | Medium | 5 |
| 3 | Field Execution, AI Inference/RAG & Report Publication (`MF3` + `FE-18`, `FE-13`–`FE-18`) | Complex | 48 |
| 3.1 | `FE-13` Flight Permit Upload & Independent Verification Gate (`MF3`) | Medium | 7 |
| 3.2 | `FE-14` On-Site Field Session & SmartDroneHub MAVLink Telemetry (`MF3`) | Complex | 8 |
| 3.3 | `FE-15` Field Evidence Intake & Chunked Video Processing Pipeline (`MF3`) | Complex | 9 |
| 3.4 | `FE-16` AI Defect Detection (`YOLO11` + Vision Fallback) & Findings Confirmation (`MF3`) | Complex | 8 |
| 3.5 | `FE-17` AI Case/Standard Retrieval (`pgvector` RAG), Note Drafting & Report Summary (`MF3`) | Complex | 8 |
| 3.6 | `FE-18` Inspection Report Compilation, Independent Review & Official Publication (`MF4`) | Complex | 8 |
| 4 | Acceptance, Payment Settlement, Payouts & Re-inspection (`MF4`, `FE-19`–`FE-24`) | Complex | 42 |
| 4.1 | `FE-19` Customer Report Acceptance & Clarification Workflow | Medium | 6 |
| 4.2 | `FE-20` Online Service Fee Payment (`PayOS` VietQR & `VNPay`) | Complex | 9 |
| 4.3 | `FE-21` Payment Deadlines, Invoices & Payment Document Management | Medium | 7 |
| 4.4 | `FE-22` Partner Inspector Payout Reconciliation | Medium | 7 |
| 4.5 | `FE-23` Evidence-Backed Refunds & Receivable Recovery | Complex | 7 |
| 4.6 | `FE-24` Post-Remediation Re-inspection & Defect Verification | Medium | 6 |
| 5 | Cross-cutting foundation | Complex | 18 |
| 5.1 | Backend Spring Modulith boundaries, PostgreSQL/Flyway architecture & audit trail | Complex | 6 |
| 5.2 | Customer Mobile App (Flutter) co-development, localization & media foundation | Complex | 8 |
| 5.3 | Cross-module integration & environment verification support | Medium | 4 |
| 6 | Verification, coordination & documentation | Medium | 12 |
| 6.1 | Project coordination & supervisor liaison | Simple | 3 |
| 6.2 | Cross-module QA verification & documentation support | Simple | 1 |
| 6.3 | Automated test reconciliation, Report 5 workbook & docs standardization | Medium | 8 |
| Total Estimated Effort (man-days) | 208 |  |  |

**Capacity reconciliation.** Four team members work across a fifteen-week semester at an assumed twenty working days per month, giving a raw allocation of `4 members × 3.75 months × 20 days = 300` person-days. Applied at roughly 70% effective capacity — allowing for lectures, review preparation, and rework, with documentation counted inside the breakdown above rather than deducted from it — the available development capacity is about 208 man-days. Effort distribution across the four members matches their recorded project weights: **Trần Hoàng Trung Hiếu** `50` md (`43` feature + `4` mobile + `3` leadership/coordination = `24%`), **Phùng Trung Quốc** `50` md (`45` feature + `4` cross-module + `1` QA/docs = `24%`), **Trần Tùng Bách** `58` md (`48` feature + `6` architecture + `4` mobile = `28%`), and **Trương Thái Như** `50` md (`42` feature + `8` QA/Report 5/docs = `24%`).

### 1.2 Project Objectives

The objective is to deliver a working, demonstrable platform that completes the four main flows end to end across web and mobile, with a backend that enforces role, ownership, and assignment boundaries.

Quality targets, measured against the final integrated build: every delivered feature linked to executed automated or manual test evidence; at least 80% line coverage on the backend core modules; zero Spring Modulith boundary violations; and no open Critical defects at submission.

| # | Testing Stage | Test Coverage | No. of Defects | % of Defect | Notes |
| --- | --- | --- | --- | --- | --- |
| 1 | Reviewing | Peer review on every pull request | Not tracked by count | Not applicable | Review is a gate, not a defect metric. |
| 2 | Unit Test | Target ≥ 80% line coverage on backend core modules; frontend and mobile unit suites maintained | Recorded in Report 5 | Recorded in Report 5 | Executed totals and coverage are reported in Report 5. |
| 3 | Integration Test | Backend API and persistence contracts exercised against real PostgreSQL and object storage | Recorded in Report 5 | Recorded in Report 5 | Executed totals are reported in Report 5. |
| 4 | System Test | End-to-end flows `MF1`–`MF4` across all four roles | Recorded in Report 5 | Recorded in Report 5 | Executed totals are reported in Report 5. |
| 5 | Acceptance Test | Customer, Manager, Inspector, and Administrator scenarios on the deployed build | Recorded in Report 5 | Recorded in Report 5 | Executed totals are reported in Report 5. |

Milestone Timeliness (%): target at least 90%; Review 1 in Week 4, Review 2 in Week 8, Defense 1.1 in Week 13, and final submission in Week 15.

Allocated Effort (man-days): requirements and project management 20; architectural and database design 14; implementation 140; testing, deployment, and documentation 34. Total 208 man-days.

### 1.3 Project Risks

| # | Risk Description | Impact | Possibility | Response Plans |
| --- | --- | --- | --- | --- |
| 1 | Scope exceeds four-person capacity across backend, web, mobile, and AI work. | High | Medium | Bound the scope to twenty-four atomic product features (`FE-01`–`FE-24`) distributed proportionally by team capacity (`24%` Hiếu / `24%` Quốc / `28%` Bách / `24%` Như), and track the WBS weekly. Corrective maintenance was removed from scope when it threatened the schedule. |
| 2 | Contract drift between the four repositories — a backend contract change not reflected in the web or mobile client. | High | High | Keep one focused pull request per repository and merge in a documented order; exercise the changed endpoint through the client tests before merging; re-read live code rather than stale documentation when reconciling. |
| 3 | The self-hosted vision model or the external language-model endpoint is unavailable during a demonstration. | High | Medium | Route inference through a primary-with-fallback strategy; accept manually entered findings when no detector responds; keep report compilation deterministic so a report can always be produced; for `DroneKnowledgeAI` recommendations, fall back to deterministic keyword-based similarity when embeddings are unconfigured, and keep recommendations advisory so findings can still be confirmed by the Inspector. |
| 4 | Report content diverges from the confirmed findings. | High | Low | Compile the report from confirmed findings rather than free text, and require an independent Manager to approve publication. |
| 5 | Cross-customer data leakage or privilege escalation between the four roles. | High | Low | Enforce role checks at every endpoint, add ownership and assignment checks inside services, and keep separation of duties between report author and report reviewer. |
| 6 | The same Inspector or aircraft is double-booked across two customer organizations. | High | Medium | Check schedule conflicts across all customer organizations before assigning an occurrence, and require a currently valid pilot licence and an eligible aircraft. |
| 7 | Unverified payment or report download before settlement. | High | Low | Accept payment only through gateway callbacks with verified signatures, and withhold the report deliverable until the occurrence is accepted or paid. |
| 8 | Large photographs and video exhaust storage or memory during upload. | Medium | Medium | Normalise images on intake, accept video through resumable chunked uploads, transcode asynchronously, and stream playback with signed, time-limited access. |
| 9 | Database schema churn destabilises the deployment. | Medium | Medium | Consolidate the migration history into a single baseline plus forward-only changes, and assert the migration set in an automated test. |
| 10 | Concurrent deployments from separate repositories collide on the shared host. | Medium | Low | Serialise deployments behind a lock and take a database backup before each release. |

## 2. Management Approach

### 2.1 Project Process

![Agile Scrum project management process](assets/image13.png)

Figure 1. Agile Scrum project management process.

The SmartDroneInspection project adopts the Agile Scrum methodology as its primary project management approach. This methodology combines the structured framework of Scrum with the adaptability of Agile practices, enabling the team to maintain high delivery efficiency and responsiveness to changes across its four repositories — backend service, web portals, Customer mobile app, and documentation. Scrum is selected because:

- The project scope evolves based on supervisor feedback, domain regulations, and academic milestone requirements across the twenty-four atomic product features (`FE-01`–`FE-24`).
- The team size is small, consisting of 4 members, making Scrum lightweight, transparent, and effective.
- Incremental delivery allows early end-to-end validation of core building-inspection workflows (`MF1` onboarding and airspace screening, `MF2` service requests and dispatch, `MF3` field execution and AI defect detection, and `MF4` report publication and online payment settlement).
- Frequent sprint reviews and supervisor checkpoints help reduce late-stage integration and API-contract rework between the web, mobile, and backend repositories.

The project is divided into short sprints aligned with the five delivery milestones, with each sprint focusing on a prioritized vertical slice of product features, automated verification, and matching documentation updates.

### 2.2 Quality Management

To ensure project quality throughout development, the team continuously applies the following practices:

- **Requirement Reviewing:** Validate functional requirements, four-role boundaries, and acceptance criteria in Report 3 before implementation begins.
- **Code Review:** Require non-author peer review on every pull request across the backend, web frontend, mobile client, and documentation repositories before merging.
- **Unit and Integration Testing:** Verify individual modules, schema migrations, and API contracts automatically against real PostgreSQL and object storage, while tracing functional test cases cleanly in Report 5.
- **Daily Stand-ups:** Hold short daily team syncs to track sprint progress, coordinate cross-repository merge order, and clear blockers early.

### 2.3 Training Plan

| Training Area | Participants | When, Duration | Waiver Criteria |
| --- | --- | --- | --- |
| Inspection service domain and the `MF1`–`MF4` workflows | All members | Week 1, 2 hours | Walk through all four flows and every status transition unaided. |
| Spring Boot 4.1, Spring Modulith, PostgreSQL, and object storage | All members | Week 2, 2 hours | Deliver one scoped endpoint with an integration test against real infrastructure. |
| React 19, Material UI, and Flutter | All members | Week 2, 2 hours | Build a role-guarded web screen and a mobile upload flow. |
| Vision-model inference, report compilation, and payment gateways | Bách, Quốc, Như | Week 3, 2 hours | Run detector inference, compile and publish an inspection report, and complete a gateway callback in a sandbox. |

## 3. Project Deliverables

| # | Deliverable | Due Date | Notes |
| --- | --- | --- | --- |
| D1 | Report 1 — Project Introduction | Week 2 | Product background, three-system comparison, vision, and 24-feature (`FE-01`–`FE-24`) scope. |
| D2 | Report 2 — Project Management Plan | Week 3 | 24-feature work breakdown (`208` md), risk register, weighted RACI, and quality plan. |
| D3 | Review 1 Gate Package | Week 4 | Registration form, management plan, draft requirements, and architecture baseline. |
| D4 | Report 3 — Software Requirement Specification | Week 8 | Complete requirements for four roles and 24 atomic features (`FE-01`–`FE-24`), with screen and authorization matrices. |
| D5 | Report 4 — Software Design Document | Week 8 | System architecture, package and 45-table database design, and per-feature detailed design diagrams. |
| D6 | Report 5 — Test Documentation and Test Report | Week 8, updated Week 13 | Testing plan plus the 24-sheet, 67-case executed test workbook (`Feature 1`–`Feature 24`). |
| D7 | Review 2 Submission Package | Week 8 | The four review artefacts required at the second review. |
| D8 | Integrated Release and Verification | Week 13 | All four flows demonstrated on the deployed build. |
| D9 | Final Submission Package (Reports 1–7) | Weeks 14–15 | Final release, deployed demonstration, and complete documentation. |

## 4. Responsibility Assignments

One primary owner is assigned to each of the twenty-four atomic features (`FE-01`–`FE-24`) and four cross-cutting workstreams, matching commit authorship and contribution percentages across the backend, web, mobile, and documentation repositories. Columns use the four students' initials: **H** — Trần Hoàng Trung Hiếu (`SE184212`, `24%`); **Q** — Phùng Trung Quốc (`SE170027`, `24%`); **N** — Trương Thái Như (`SE180082`, `24%`); **B** — Trần Tùng Bách (`SE180220`, `28%`).

D~Do; R~Review; S~Support; I~Informed; <blank>- Omitted

| Responsibility | H | Q | N | B | Supervisors |
| --- | --- | --- | --- | --- | --- |
| `FE-01` Account Authentication, OTP & 4-Role Access Control | D | S | R | S | R |
| `FE-02` Partner Inspector Application & Qualification Management | D | S | R | S | I |
| `FE-03` Inspector-Owned Drone Registration & Fleet Management | D | R | S | S | R |
| `FE-04` Interactive Location Map & No-Fly Zone Airspace Screening | D | S | R | S | I |
| `FE-05` Financial History & Revenue/Payment Ledger | D | S | R | S | I |
| `FE-06` Building Asset Registry, Checkpoints & Reference Documents | S | D | R | S | R |
| `FE-07` Restricted Airspace Review & Clearance Decision | S | D | R | S | I |
| `FE-08` Service Requests (One-Time & Recurring) & VND Quotations | R | D | S | S | R |
| `FE-09` Offline Signed Contract & Occurrence Dispatch Scheduling | R | D | S | S | R |
| `FE-10` Dual-Channel Messaging (Order Chat & Inspection Chat) | S | D | R | S | I |
| `FE-11` Assignment Acceptance Timeout & Escalation Handling | S | D | R | S | I |
| `FE-12` System Notifications & Alert Center | S | D | S | R | I |
| `FE-13` Flight Permit Upload & Independent Verification Gate | S | R | S | D | R |
| `FE-14` On-Site Field Session & SmartDroneHub MAVLink Telemetry | R | S | S | D | R |
| `FE-15` Field Evidence Intake & Chunked Video Processing Pipeline | S | S | R | D | R |
| `FE-16` AI Defect Detection (`YOLO11` + Vision Fallback) & Findings Confirmation | S | R | S | D | R |
| `FE-17` AI Case/Standard Retrieval (`pgvector` RAG), Note Drafting & Report Summary | R | S | S | D | R |
| `FE-18` Inspection Report Compilation, Independent Review & Official Publication | R | S | R | D | R |
| `FE-19` Customer Report Acceptance & Clarification Workflow | R | S | D | S | R |
| `FE-20` Online Service Fee Payment (`PayOS` VietQR & `VNPay`) | S | S | D | R | R |
| `FE-21` Payment Deadlines, Invoices & Payment Document Management | S | R | D | S | I |
| `FE-22` Partner Inspector Payout Reconciliation | R | S | D | S | R |
| `FE-23` Evidence-Backed Refunds & Receivable Recovery | S | S | D | R | R |
| `FE-24` Post-Remediation Re-inspection & Defect Verification | R | S | D | R | R |
| `CC-01` Project coordination & supervisor liaison | D | S | S | S | R |
| `CC-02` Backend Spring Modulith & PostgreSQL/Flyway architecture | R | S | S | D | R |
| `CC-03` Customer Mobile App (Flutter) co-development & i18n | D | S | R | D | I |
| `CC-04` Automated test reconciliation, Report 5 workbook & docs standardization | R | S | D | R | R |

## 5. Project Communications

| Communication Item | Who/ Target | Purpose | When, Frequency | Type, Tool, Method(s) |
| --- | --- | --- | --- | --- |
| Daily progress sync | All members | Report progress and clear blockers | Working days | Chat channel and pull-request comments |
| Weekly planning and work-breakdown review | Leader and team | Update the breakdown, defects, and weekly report | Weekly | Online meeting with the tracking workbook |
| Supervisor checkpoint | Team and supervisors | Review requirements, design, and test artefacts; demonstrate progress | Weekly to bi-weekly | In person or video call, with document review |
| Pull request and verification gate | Author and reviewer | Confirm module boundaries and all test suites pass | Every change before merge | Pull request with local verification record |
| Milestone gate review | Team, supervisors, and council | Review 1 (Week 4), Review 2 (Week 8), Defense 1.1 (Week 13) | Weeks 4, 8, 13, and 15 | Live demonstration and formal submission |

## 6. Configuration Management

### 6.1 Document Management

Project documents are authored in version-controlled Markdown under the documentation repository and converted to the official university Word and Excel templates by a Python export toolchain. That toolchain fills the templates rather than rebuilding them, so each release keeps the official styles, numbering, and formulas intact; the Markdown remains the editable source and every change is reviewable in version control.

### 6.2 Source Code Management

Source code is managed in four independent GitHub repositories — backend, web frontend, mobile application, and documentation. Each repository has its own workflow, and a cross-repository change is delivered as one focused pull request per repository, merged in a documented order. Database evolution is forward-only: the migration history is a single consolidated baseline plus subsequent forward migrations, and an automated test asserts the exact set of applied versions so an accidental renumbering fails the build.

### 6.3 Tools & Infrastructures

| Category | Tools / Infrastructure |
| --- | --- |
| Technology | Java 21, Spring Boot 4.1, Spring Modulith, Spring Security with JWT and Google OAuth2, Hibernate/JPA, Flyway; Python with FastAPI and Ultralytics for the vision service; React 19, TypeScript, Vite, Material UI, TanStack Query; Flutter with Riverpod and GoRouter |
| Database | PostgreSQL 17 with pgcrypto and pgvector (`vector(384)`, HNSW cosine index for the `DroneKnowledgeAI` `inspection_knowledge_chunks` and `historical_finding_cases` retrieval layer powered by local `fastembed` `paraphrase-multilingual-MiniLM-L12-v2` embeddings; `HYBRID_MATCH` fallback when the embedding endpoint is unavailable) |
| IDEs/Editors | Visual Studio Code, IntelliJ IDEA, Android Studio |
| Diagramming | Mermaid and Draw.io sources kept in version control alongside the reports |
| Documentation | Markdown in the documentation repository with automated OOXML export to the official Word and Excel templates |
| Version Control | Git and GitHub, with protected branches and pull-request review |
| Deployment server | Docker Compose on a Linux host, Nginx for the web client, object storage for evidence media |
| Project management | GitHub pull requests and issues, a project tracking workbook, and weekly reporting |
