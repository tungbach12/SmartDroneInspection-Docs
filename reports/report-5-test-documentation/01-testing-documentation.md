---
title: "Report 5 - Software Test Documentation"
document_type: report5-doc-section
weight: 15
source: "Report5_Test Documentation.docx"
---

# II. Testing Documentation

## 1. Scope of Testing

**Features and Requirements in Scope**

The testing scope encompasses the complete **SmartDroneInspection** multi-tenant Enterprise SaaS & B2B Drone Leasing platform across Web (`SmartDroneInspection-frontend`), Mobile (`SmartDroneInspection-mobile`), Backend Modular Monolith (`SmartDroneInspection-backend`), and Self-Hosted AI Computer Vision (`ai-inference`), covering **twelve product features (`FE-01` to `FE-12`)**:
- **`FE-01` — Authentication & Access Control** *(Owner: Trần Tùng Bách)*: Organization self-registration with active Terms/Privacy consent, Web/Mobile login, Argon2id password security, HS256 JWT + HmacSHA256 refresh rotation, CSRF & IP rate-limiting (`10 req/60s`), and 5-role RBAC separation of duties (Platform Admin and Platform Manager single-role separation).
- **`FE-02` — Workforce & Subscription Management** *(Owner: Trần Hoàng Trung Hiếu)*: Platform user administration, customer workforce provisioning (`Inspector`, `Maintenance Engineer`), Inspector remote pilot license self-declaration, and Enterprise Subscription billing (`1..120` months via Corporate Wire & PayPal Orders v2 + signed Webhooks).
- **`FE-03` — Asset & Drone Fleet Management** *(Owner: Trần Hoàng Trung Hiếu)*: Global asset categories, tenant assets with GPS coordinates and standardized inspection checkpoints (`inspection_items`), reference engineering documents in MinIO, asset retirement archival, owned drone inventory, and B2B Platform Drone Leasing (`platform_drones`, `drone_leases`).
- **`FE-04` — Recurring Schedule & Notifications** *(Owner: Trần Hoàng Trung Hiếu)*: Timezone-anchored recurring inspection schedules (`Week`, `Month`, `Year`), rolling 14-day occurrence generator, `Blocked` occurrence retry/skip, 3-day advance reminder job, and deduplicated in-app notification inbox (`notifications` + `event_publication` outbox).
- **`FE-05` — Mission Dispatch & Airspace Advisory** *(Owner: Phùng Trung Quốc)*: One-off inspection mission scheduling with direct Inspector + Drone conflict checking, and the interactive Vietnam Airspace & No-Fly Zone Map (`AirspaceNoFlyMap` on Web, `AirspaceAdvisoryCard` on Mobile, `/api/v1/airspace/zones` & `/evaluate` under Decree No. 288/2025/NĐ-CP).
- **`FE-06` — Flight Readiness & Field Execution** *(Owner: Phùng Trung Quốc)*: Self-service aviation flight permit upload gate (`Assigned -> Ready for Flight` upon unexpired pilot license check) and Web/Flutter Mobile on-site field flight session execution (`Start`, `Postpone`, `Abort`, `Complete`, and Additional Sessions).
- **`FE-07` — Operational Dashboard & Schedule Calendar** *(Owner: Phùng Trung Quốc)*: Role-scoped operational analytics dashboards, server-paged inspection/report queues, interactive Month/Week/Agenda `InspectorScheduleCalendar`, Enterprise Dark Mode, and bilingual (EN/VI) localization.
- **`FE-08` — Evidence Management & AI Defect Detection** *(Owner: Trần Tùng Bách)*: Multipart evidence intake into MinIO, JPEG EXIF GPS/timestamp extraction, single/bulk soft-retirement (`is_deleted = true`), Inspector-invoked Ultralytics `YOLO11 (MBDD2025)` defect detection (with multimodal fallback), human finding verification (`Confirmed`), and confirmed findings baseline lock (`Report Draft`).
- **`FE-09` — Inspection Reporting & Publication** *(Owner: Trần Tùng Bách)*: Context-grounded LLM & manual report drafting, live OpenHTMLtoPDF preview, author verification (`Author Verified`), independent `Organization Manager` approval/return, immutable A4 PDF publication as an immutable PDF document (`Published`), and per-finding corrective handoff (`Repair Pending` / `Completed`).
- **`FE-10` — Maintenance Planning & AI Scope Advisory** *(Owner: Trương Thái Như)*: Forwarded defect triage, `pgvector` RAG engineering standard scope advisor (`TCVN 9343:2012`, `EN 1504-9`, `ISO 12944-5` + `DeterministicScopeFallback`), work order creation (`Draft`), team role assignment (`Team Lead`, `Report Author`, `Team Member`, independent reviewer), and task decomposition.
- **`FE-11` — Cost Estimation & Repair Execution** *(Owner: Trương Thái Như)*: Versioned itemized cost estimation (`Labor`, `Material`, `Equipment`), independent budget approval (`Approved`), Change Order governance, and Web/Mobile repair task execution with Team Lead work log verification (`Verified` -> `Work Completed`).
- **`FE-12` — Maintenance Acceptance & Cost Closure** *(Owner: Trương Thái Như)*: Author-verified maintenance completion report PDF, independent technical acceptance (`Accepted` / `Rework Required` / `Re-Inspection Required`), actual cost reconciliation (`Cost Reconciled`), and work order closure (`Closed`).

**Out-of-Scope Items**

- Physical unmanned aircraft radio-control (RC) actuation, autopilot telemetry streaming, and hardware flight controller firmware testing (`BR-16`).
- Live production banking settlement outside PayPal Sandbox / mock webhook verification and corporate wire reference reconciliation.
- Native OS push notifications (APNs/FCM) and external SMTP delivery (notifications are delivered via the deduplicated in-app notification inbox).

**Stages and Levels of Testing**

- **Unit Testing**: Owned by individual feature developers (`Hiếu`, `Quốc`, `Bách`, `Như`); executed on every commit via JUnit 5, Vitest, and Flutter Test (`>= 80%` backend JaCoCo coverage gate).
- **Integration Testing**: Executed in CI against real containerized **PostgreSQL 17 (`pgvector:pg17`)** and **MinIO** instances via Testcontainers, verifying Flyway migrations `V1`–`V5`, Spring Modulith boundaries (`ModulithArchitectureTest`), REST controllers, security filters, and OpenHTMLtoPDF rendering.
- **System & End-to-End Workflow Testing**: Executed against the full-stack Docker environment (`ConnectedMainFlowE2eIntegrationTest`) and the cloud Staging server (`https://smartdroneinspection.duckdns.org`).
- **Acceptance Testing (Defense 1.1 & Viva Readiness)**: Conducted against locked Review 2 Commitment targets (`64` functional test cases across `Feature 1`–`Feature 12` in `Report5_Test Report.xlsx` and `8` Demo Scenarios `DS-01a/b`–`DS-04a/b`).

---

## 2. Test Strategy

### 2.1 Testing Types
- **Functional & Business Rule Testing**:
  - *Objective*: Verify that every mandatory feature (`FE-01`–`FE-12`) and business rule (`BR-01`–`BR-49`) behaves according to the SRS specifications.
  - *Technique*: Equivalence partitioning, boundary-value analysis (`1..120` subscription months, `1..60` lease months, `10 MB` file limits, `[-90..90]`/`[-180..180]` coordinates), and positive/negative API/UI scenarios.
  - *Completion Criteria*: At least 3 test cases per mandatory feature (1 Happy path, 1 Validation/Business Rule, 1 Exception/Authorization) with 100% of happy-path test cases passing.
- **State Machine Transition Testing**:
  - *Objective*: Ensure every lifecycle entity transitions only along valid, authorized edges and rejects illegal or out-of-order state mutations (`400 Bad Request` / `409 Conflict`).
  - *Technique*: State-transition path coverage across `Subscription`, `DroneLease`, `Asset`, `Drone`, `RecurringInspectionSchedule`, `Inspection`, `FieldSession`, `Finding`, `InspectionReport`, and `MaintenanceWorkOrder`.
  - *Completion Criteria*: 100% of main entity state machines covered by positive and negative transition tests (`18` state transition test cases).
- **Security, RBAC & Multi-Tenant Isolation Testing**:
  - *Objective*: Verify zero cross-tenant data leakage, strict role separation of duties (Platform Admin and Platform Manager single-role separation; authors/team members cannot self-approve or self-accept), CSRF enforcement, account lockout, and IP rate-limiting.
  - *Technique*: Cross-organization ID probing, role matrix permutation testing, token revocation checks, and brute-force rate-limit simulation (`AuthRateLimitFilter`).
  - *Completion Criteria*: `100%` of unauthorized or cross-tenant requests rejected (`NFR-03`, `NFR-04`).
- **Performance, Integrity & Non-Functional Testing**:
  - *Objective*: Validate API response latency (`NFR-01`), YOLO11 inference latency (`NFR-02`), published PDF report immutability (`NFR-05`), and modular architecture / coverage gates (`NFR-06`).
  - *Technique*: Concurrent API timing assertions, container inference benchmarks, published PDF immutability assertions, and automated JaCoCo + Spring Modulith verification in GitHub Actions.
  - *Completion Criteria*: All 6 locked NFR thresholds met and verified by reproducible tests.

### 2.2 Test Levels

| Type of Tests | Unit | Integration | System | Acceptance |
| --- | :---: | :---: | :---: | :---: |
| Functional & Business Rule Testing | X | X | X | X |
| Domain State Machine Transition Testing | X | X | X | X |
| API & Database Persistence Testing |  | X | X |  |
| Security, RBAC & Multi-Tenant Isolation Testing | X | X | X | X |
| AI Vision, LLM & RAG Fallback Resilience Testing | X | X | X | X |
| Performance & Document Immutability (NFR) Testing |  | X | X | X |

### 2.3 Supporting Tools

| Purpose | Tool | Vendor/In-house | Version |
| --- | --- | --- | --- |
| Backend Unit & Integration Testing Framework | JUnit Jupiter / Spring Boot Test / MockMvc | Open Source (Eclipse / Broadcom) | `6.0.x` / `4.1.0` |
| Containerized Database & S3 Test Harness | Testcontainers (`pgvector:pg17` & `MinIO`) | AtomicJar / Docker | `1.20.x` / `PG 17` |
| Architectural Boundary & Code Coverage Gate | Spring Modulith Test / JaCoCo Maven Plugin | Broadcom / EclEmma | `2.1.1` / `0.8.13` |
| Frontend Component & Unit Testing | Vitest / React Testing Library / JSDOM | Open Source (Vite / Testing Library) | `5.0.1` / `16.3.3` |
| Mobile Widget & Repository Testing | Flutter Test / Dart Analyzer | Google | `Dart 3.13.2` |
| Full-Stack E2E & Browser Automation | Node.js E2E Runner / Playwright MCP | Open Source / Microsoft | `Node 22` / `1.50+` |
| Continuous Integration & Deployment | GitHub Actions (`ci.yml`, `deploy.yml`) | GitHub | `v4` |
| Report & Workbook OOXML Verification | Custom Python OOXML Exporter & Unittest Suite | In-house (`SmartDroneInspection-docs/tools`) | `Python 3.12` |

---

## 3. Test Plan

### 3.1 Human Resources

| Worker/Doer | Role | Specific Responsibilities/Comments |
| --- | --- | --- |
| **Trần Hoàng Trung Hiếu** (`SE184212`) | Project Leader & Tester (`WF-01` Owner) | Owns **16 functional test cases (`WF1-006`–`WF1-021` on Sheets `Feature 2`, `Feature 3`, `Feature 4`)** covering `FE-02` (Workforce & Subscription Management), `FE-03` (Asset & Drone Fleet Management), and `FE-04` (Recurring Schedule & Notifications). |
| **Phùng Trung Quốc** (`SE170027`) | Backend / Mobile Engineer & Tester (`WF-02` Owner) | Owns **16 functional test cases (`WF2-001`–`005`, `008`, `009`, `011`, `012`, `015`–`020`, `WF3-009` on Sheets `Feature 5`, `Feature 6`, `Feature 7`)** covering `FE-05` (Mission Dispatch & Airspace Advisory), `FE-06` (Flight Readiness & Field Execution), and `FE-07` (Operational Dashboard & Schedule Calendar). |
| **Trần Tùng Bách** (`SE180220`) | Full-Stack / AI Engineer & Tester (`WF-03` Owner) | Owns **16 functional test cases (`WF1-001`–`005`, `WF3-001`–`008`, `010`, `012`, `016` on Sheets `Feature 1`, `Feature 8`, `Feature 9`)** covering `FE-01` (Authentication & Access Control), `FE-08` (Evidence Management & AI Defect Detection), and `FE-09` (Inspection Reporting & Publication). |
| **Trương Thái Như** (`SE180082`) | Full-Stack Engineer & Tester (`WF-04` Owner) | Owns **16 functional test cases (`WF4-001`–`WF4-016` on Sheets `Feature 10`, `Feature 11`, `Feature 12`)** covering `FE-10` (Maintenance Planning & AI Scope Advisory), `FE-11` (Cost Estimation & Repair Execution), and `FE-12` (Maintenance Acceptance & Cost Closure). |
| **Phạm Minh Trí & Đặng Ngọc Minh Đức** | Supervisors / Reviewers | Review test strategy, verify Review 2 self-review & commitment targets, and audit Defense 1.1 readiness. |

### 3.2 Test Environment

| Purpose | Tool | Provider | Version |
| --- | --- | --- | --- |
| Cloud Staging & Review 2 Demo Environment | Ubuntu Linux VPS2 (`https://smartdroneinspection.duckdns.org`, Docker Compose, Nginx, Tailscale) | Cloud VPS / DuckDNS | `Ubuntu 24.04` / `Docker 27.x` |
| Backend Runtime & API Container | Eclipse Temurin JRE Alpine + Spring Boot | Adoptium / Broadcom | `Java 21` / `4.1.0` |
| Relational & Vector Database Server | PostgreSQL with `pgvector` and `pgcrypto` | PostgreSQL Global Dev Group | `17` (`pgvector:pg17`) |
| S3-Compatible Object Storage | MinIO Server (`inspection-evidence` bucket) | MinIO Inc. | `RELEASE.2025` |
| Computer Vision Defect Inference Container | Python Slim + FastAPI + Ultralytics YOLO11 (`MBDD2025`) | Python / Ultralytics | `Python 3.11` / `8.3.55` |
| Web & Mobile Test Clients | Google Chrome / Edge + Flutter Android Emulator | Google / Microsoft | `Evergreen` / `API 34` |

### 3.3 Test Milestones

| Milestone Task | Start Date | End Date |
| --- | --- | --- |
| Milestone 1: Unit & Migration Foundation Gate (`V1`–`V5` Schema, Auth, RBAC, Modulith Boundaries) | `2026-09-15` | `2026-10-08` |
| Milestone 2: Iteration 1 Feature & Integration Testing (`FE-01`–`FE-09`, MinIO, YOLO11, PayPal/Wire) | `2026-10-09` | `2026-10-22` |
| Milestone 3: Review 2 Full 12-Feature & 64-Case Baseline (`FE-01`–`FE-12`, B2B Drone Leasing, Recurrence, Airspace Map, RAG MF4) | `2026-10-23` | `2026-10-27` |
| Milestone 4: Post-Review 2 Pending Case Closure & Staging Stress/NFR Verification | `2026-10-28` | `2026-11-15` |
| Milestone 5: Defense 1.1 Full Regression & Live Demo Rehearsal (`100%` Workflows, `>= 90%` Pass Rate) | `2026-11-16` | `2026-11-30` |

---

## 4. Test Cases

**Review 2 Minimum Test Case Formula Calculation (SWP490 Section 09.3)**

In strict compliance with **SWP490 Review 2 Guidelines (Section 09.3)**, the functional test case inventory in `Report5_Test Report.xlsx` is structured and committed across the **12 Mandatory Features (`FE-01` to `FE-12`)**:
- **12 Mandatory Features (`FE-01` to `FE-12`) x 3 TCs = 36 Test Cases** (`12` Main Flow cases + `12` Validation/Business Rule cases + `12` Exception/RBAC cases).
- **4 Main Business Workflows (`WF-01` to `WF-04`) x 1 E2E TC = 4 Test Cases** (`WF1-021`, `WF2-016`, `WF3-008`, `WF4-016`).
- **18 Main Entity State Transitions (including invalid transition rejection) x 1 TC = 18 Test Cases** across `Subscription`, `DroneLease`, `Asset`, `Drone`, `RecurringInspectionSchedule`, `Inspection`, `FieldSession`, `Finding`, `InspectionReport`, and `MaintenanceWorkOrder`.
- **6 Locked Non-Functional Requirements (`NFR-01` to `NFR-06`) x 1 TC = 6 Test Cases** (`WF2-016` `NFR-01`, `WF3-007` `NFR-02`, `WF1-005` `NFR-03`, `WF1-004` `NFR-04`, `WF3-016` `NFR-05`, `WF4-005` `NFR-06`).
- **Total Committed Functional Test Cases**: **36 + 4 + 18 + 6 = 64 Test Cases** distributed across `Feature 1`–`Feature 12` (`16` Test Cases per Team Member).

**Test Case Artifacts**

- **Unit Test Cases**: `Report5_Unit Test.xls` / Automated JUnit 5 (`77` backend classes / `850` tests), Vitest (`81` frontend files / `602` tests), and Flutter Test (`14` mobile files / `20` tests).
- **Other Test Cases (IT, ST, AT)**: `Report5_Test Report.xlsx` (`Cover`, `Test Cases`, `Test Statistics`, and `Feature 1` through `Feature 12`).

---

## 5. Test Reports

**Execution Summary Statistics (Review 2 Baseline — Round 1)**

All 64 functional test cases in `Report5_Test Report.xlsx` have been mapped to the 12 product features (`FE-01`–`FE-12`) and 4 team members (`16` cases each):
- **Total Test Cases**: `64`
- **Passed**: `60` (`93.75%` Test Successful Coverage — exceeds the Defense 1.1 `>= 90%` minimum threshold; `100%` of mandatory feature happy-path cases Passed)
- **Failed**: `0` (`0.00%`)
- **Pending**: `4` (`6.25%` — 1 manual staging/mobile walkthrough per member scheduled for Milestone 4 completion prior to Defense 1.1: `WF1-010` Hiếu, `WF2-015` Quốc, `WF3-012` Bách, `WF4-011` Như)
- **N/A**: `0` (`0.00%`)
- **CI Test Automation Ratio**: `56 / 64` cases (`87.50%`) are automated in CI (exceeding the Defense 1.1 `>= 50%` automation threshold); `8 / 64` (`12.50%`) are manual staging/mobile walkthrough verifications.
- **Defect Status**: `0` open Critical or High defects in `Report3_Project Tracking.xlsx`.
