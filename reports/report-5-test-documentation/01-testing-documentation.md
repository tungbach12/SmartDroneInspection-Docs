---
title: "Report 5 - Software Test Documentation"
document_type: report5-doc-section
weight: 15
source: "Report5_Test Documentation.docx"
---

# II. Testing Documentation

## 1. Scope of Testing

**Features and Requirements in Scope**

This document defines the software test strategy, test levels, test environment, and traceability scope for the SmartDroneInspection platform across the Web Portal, Flutter Mobile Field Application, Spring Boot Modulith Backend (`V1`–`V28` PostgreSQL 17 schema, 36 tables), and AI-assisted inspection and maintenance services. The eight product features (`FE-01` to `FE-08`, two features per team member) in scope are:
- **`FE-01` — Authentication, Google OAuth2 & 5-Role Access Control** *(Owner: Trần Hoàng Trung Hiếu)*: Customer registration with initial asset & No-Fly Zone airspace gate (`ProspectiveCustomerRegistration`), Argon2id sign-in, consolidated `OtpChallenge` verification (`LOGIN`, `REGISTRATION`, `PASSWORD_RESET`), Google OAuth2 (Web callback & Mobile `smartdrone://auth` deep link), HS256 JWT + HmacSHA256 refresh rotation (`AuthSession`), decoupled `/api/v1/users/me` profile, CSRF & IP rate-limiting (`AuthRateLimitFilter`, `10 req/60s`), and 5-role `ActorZone` RBAC (`ADMIN`, `MANAGER`, `CUSTOMER`, `INSPECTOR`, `MAINTENANCE_ENGINEER`).
- **`FE-02` — Partner Onboarding, Workforce, Asset & Inspector Drone Registry** *(Owner: Trần Hoàng Trung Hiếu)*: Platform-provisioned `INSPECTOR` accounts with pilot license profiles (`inspector_profiles`) and flight logs (`inspector_flight_logs`), restricted-airspace Customer registration review (`AirspaceReviewController`), Customer `MAINTENANCE_ENGINEER` workforce provisioning (`WorkforceController`), infrastructure asset catalog with `inspection_items` checkpoints, SHA-256 reference documents in MinIO and No-Fly Zone guard, and Inspector-owned Drone registration with 3 mandatory documents (`REGISTRATION`, `OWNERSHIP`, `INSPECTION`).
- **`FE-03` — Recurring Service Requests, Contract Occurrences & Outbox Notifications** *(Owner: Phùng Trung Quốc)*: Recurring `ServiceRequest` cadence validation (`DAY`/`WEEK`/`MONTH`), count-bound and end-date-bound `ServiceRequestOccurrence` materialization with month-end anchoring, parent signed contract inheritance, and deduplicated in-app notifications (`uq_notifications_deduplication_key`) driven by Spring Modulith transactional domain events (`event_publication`).
- **`FE-04` — Service Requests, Quotations, Contracts, Dispatch & Airspace Map** *(Owner: Phùng Trung Quốc)*: One-time and recurring customer service requests, Order Chat (`ServiceRequestMessage`), versioned VND quotations (`ServiceRequestQuote`), signed paper service agreement upload/streaming, cross-organization Inspector and owned Drone dispatch (`Mf2InspectionAssignmentAdapter`) with schedule-conflict guards, abort recovery dispatch (`reschedule`, `reassign`, `cancel`), and interactive Vietnam Airspace evaluation (`AirspaceAdvisoryService`, `AirspaceNoFlyMap`, `AirspaceAdvisoryCard`).
- **`FE-05` — Flight Permit Gate, Field Execution, Dashboard & Calendar** *(Owner: Trần Tùng Bách)*: Aviation flight permit upload with pilot license validity checked at upload time (`uploadFlightPermit`), field session start requiring a stored permit file key (`hasFlightPermit()`), Web/Flutter Mobile on-site field sessions (`Start` $\rightarrow$ `Complete` or `Abort` with automatic mission reopen to `SCHEDULED` and manager alert), `SmartDroneHub` live telemetry, persisted flight report metrics, GPS flight trace (`V28` `flight_trace_json`), and mission MP4 video sync (`InspectionDroneHubService`), 5-role operational analytics dashboards (`DashboardAnalyticsService`), Inspector Schedule Calendar, and Customer 5-Stage Inspection Progress Tracker.
- **`FE-06` — Evidence Intake, YOLO11 Detection, Auto-Compiled Report & PayOS** *(Owner: Trần Tùng Bách)*: Multipart photo (`10 MB`) and streaming `video/mp4` (`500 MB`) evidence intake (`file_picker` on Mobile, `AuthenticatedMedia` and interactive video frame cropping on Web) with EXIF GPS extraction, `YOLO11` (`MBDD2025`) photo and video keyframe defect detection (`POST /evidence/{id}/analyze` & `/analyze-video`) with automatic Vision LLM fallback (`PrimaryWithFallbackInference`), findings baseline confirmation (`findings_confirmed_at`), 4-state Inspection Report lifecycle (`SUBMITTED`, `RETURNED`, `PUBLISHED`, `SUPERSEDED`), AI Executive Summary generation, independent `MANAGER` direct approval and publication (`SUBMITTED` $\rightarrow$ `PUBLISHED`), on-demand A4 PDF rendering (`PdfReportRenderer`), Customer report acceptance, and online VND payment settlement via **PayOS (VietQR)** and **VNPay (`v2.1.0`)**.
- **`FE-07` — Maintenance Work Orders, RAG Scope/Norms Advisor & Repair Execution** *(Owner: Trương Thái Như)*: Forwarded defect triage into 12-state `MaintenanceWorkOrder`s, `pgvector` RAG repair scope advisor (`TCVN`/`EN`/`ISO` with `DeterministicScopeFallback`) and 1-click `initialTasks` provisioning, engineering team role assignment (`LEAD`, `REPORT_AUTHOR`, `MEMBER`, and independent `acceptingReviewerUserId`), RAG Cost & Norms Estimator (`suggest-estimate`), independent Customer budget & Change Order approval, field repair execution with before/after proof, and 1-click Team Lead batch work-log verification (`batch-verify`).
- **`FE-08` — Completion Report, 3-Way Re-inspection Verification & Cost Closure** *(Owner: Trương Thái Như)*: Smart template auto-drafted Maintenance Completion Report (`auto-draft`), RAG Technical Acceptance Compliance Audit (`acceptance-compliance`), event-driven 3-step/3-way Re-inspection defect verification loop (`reinspection_defect_verifications`: Prior Defect vs Engineer Repair Proof vs Drone Re-capture), automatic work-order reinstatement upon re-inspection publication (`WorkOrderReinspectionListener`), independent Customer acceptance, baseline-to-actual cost inheritance & reconciliation, and Work Order closure (`CLOSED`).

**Out-of-Scope Items**

- Physical unmanned aircraft radio-control (RC) actuation, autopilot hardware control, and flight controller firmware testing (`BR-16`).
- Native OS push notifications (APNs/FCM) and external SMTP delivery (notifications are delivered via the deduplicated in-app notification inbox).

**Stages and Levels of Testing**

- **Unit Testing**: Owned by individual feature developers (`Hiếu`, `Quốc`, `Bách`, `Như`); executed via JUnit Jupiter (`SmartDroneInspection-backend`), Vitest (`SmartDroneInspection-frontend`), and Flutter Test (`SmartDroneInspection-mobile`) with a `>= 80%` backend JaCoCo coverage gate.
- **Integration Testing**: Executed with containerized **PostgreSQL 17 (`pgvector:pg17`)** and **MinIO** via Testcontainers across the **Flyway `V1`–`V28` schema (36 tables)**, verifying Spring Modulith boundaries (`ModulithArchitectureTest`), REST controllers, security filters, PayOS/VNPay webhook verification, and OpenHTMLtoPDF rendering.
- **System & End-to-End Workflow Testing**: Executed against the full-stack environment (`ConnectedMainFlowE2eIntegrationTest`) and the cloud Staging server (`https://smartdroneinspection.duckdns.org`).
- **Acceptance Testing**: Conducted against the 65 functional test cases across `Feature 1`–`Feature 8` in `Report5_Test Report.xlsx`.

---

## 2. Test Strategy

### 2.1 Testing Types
- **Functional & Business Rule Testing**:
  - *Objective*: Verify that every mandatory feature (`FE-01`–`FE-08`) and business rule (`BR-01`–`BR-49`) behaves according to the SRS specifications and live API contracts.
  - *Technique*: Equivalence partitioning, boundary-value analysis (`10 MB` photo/document and `500 MB` MP4 video file limits, `[-90..90]`/`[-180..180]` coordinates, `0..100%` finance rates), and positive/negative API/UI scenarios.
  - *Completion Criteria*: Complete functional test coverage across `Feature 1`–`Feature 8` with all automated test suites passing.
- **State Machine Transition Testing**:
  - *Objective*: Ensure every lifecycle entity transitions only along valid, authorized edges and rejects illegal or out-of-order state mutations (`400 Bad Request` / `409 Conflict`).
  - *Technique*: State-transition path coverage across `ServiceRequest` (6 states), `ServiceRequestOccurrence` (payment & payout lifecycles), `Asset` (3 states), `Drone` (3 states), `DroneRegistrationApplication` (3 states), `Inspection` (6 states), `FieldSession` (4 states), `Finding` (2 states), `InspectionReport` (4 states: `SUBMITTED`, `RETURNED`, `PUBLISHED`, `SUPERSEDED`), `ReinspectionDefectVerification` (3-way), and `MaintenanceWorkOrder` (12 states).
  - *Completion Criteria*: 100% of domain entity state machines covered by positive and negative transition tests.
- **Security, RBAC & Multi-Zone Isolation Testing**:
  - *Objective*: Verify zero cross-tenant data leakage, strict `ActorZone` and role separation of duties (authors/team members cannot self-approve or self-accept; Customers cannot read unpublished reports), CSRF enforcement, account lockout, and IP rate-limiting.
  - *Technique*: Cross-organization ID probing, 5-role matrix permutation testing, token revocation checks, and brute-force rate-limit simulation (`AuthRateLimitFilter`).
  - *Completion Criteria*: `100%` of unauthorized or cross-scope requests rejected (`NFR-03`, `NFR-04`).
- **Performance, Integrity & Non-Functional Testing**:
  - *Objective*: Validate API response latency (`NFR-01`), YOLO11 + Vision fallback inference latency (`NFR-02`), signed contract and published PDF report immutability (`NFR-05`), and modular architecture / coverage gates (`NFR-06`).
  - *Technique*: Concurrent API timing assertions, container inference benchmarks, `SHA-256` and version-supersession immutability assertions, and automated JaCoCo + Spring Modulith verification.
  - *Completion Criteria*: All 6 locked NFR thresholds met and verified by reproducible tests.

### 2.2 Test Levels

| Type of Tests | Unit | Integration | System | Acceptance |
| --- | :---: | :---: | :---: | :---: |
| Functional & Business Rule Testing | X | X | X | X |
| Domain State Machine Transition Testing | X | X | X | X |
| API & Database Persistence Testing (`Flyway V1–V28`, 36 PostgreSQL 17 tables) |  | X | X |  |
| Security, RBAC & ActorZone Isolation Testing | X | X | X | X |
| AI Vision, Executive Summary & pgvector RAG Testing | X | X | X | X |
| Performance, PayOS/VNPay Webhook & PDF Immutability Testing |  | X | X | X |

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
| Report & Workbook OOXML Verification | Custom Python OOXML Exporter & Unittest Suite | In-house (`SmartDroneInspection-docs/tools`) | `Python 3.12+` |

---

## 3. Test Plan

### 3.1 Human Resources

| Worker/Doer | Role | Specific Responsibilities/Comments |
| --- | --- | --- |
| **Trần Hoàng Trung Hiếu** (`SE184212`) | Project Leader & Tester (`MF1`: `FE-01`, `FE-02` Owner) | Owns functional test cases on Sheets **`Feature 1` and `Feature 2`** covering `FE-01` (Authentication, Google OAuth2 & 5-Role Access Control) and `FE-02` (Partner Onboarding, Workforce, Asset & Inspector Drone Registry). |
| **Phùng Trung Quốc** (`SE170027`) | Backend / Mobile Engineer & Tester (`MF2`: `FE-03`, `FE-04` Owner) | Owns functional test cases on Sheets **`Feature 3` and `Feature 4`** covering `FE-03` (Recurring Service Requests, Contract Occurrences & Outbox Notifications) and `FE-04` (Service Requests, Quotations, Contracts, Dispatch & Airspace Map). |
| **Trần Tùng Bách** (`SE180220`) | Full-Stack / AI Engineer & Tester (`MF3`: `FE-05`, `FE-06` Owner) | Owns functional test cases on Sheets **`Feature 5` and `Feature 6`** covering `FE-05` (Flight Permit Gate, Field Execution, Dashboard & Calendar) and `FE-06` (Evidence Intake, YOLO11 Detection, Auto-Compiled Report & PayOS). |
| **Trương Thái Như** (`SE180082`) | Full-Stack Engineer & Tester (`MF4`: `FE-07`, `FE-08` Owner) | Owns functional test cases on Sheets **`Feature 7` and `Feature 8`** covering `FE-07` (Maintenance Work Orders, RAG Scope/Norms Advisor & Repair Execution) and `FE-08` (Completion Report, 3-Way Re-inspection Verification & Cost Closure). |
| **Phạm Minh Trí & Đặng Ngọc Minh Đức** | Supervisors / Reviewers | Review test strategy, verify quality targets, and audit Defense readiness. |

### 3.2 Test Environment

| Purpose | Tool | Provider | Version |
| --- | --- | --- | --- |
| Cloud Staging Environment | Ubuntu Linux VPS (`https://smartdroneinspection.duckdns.org`, Docker Compose, Nginx, Tailscale) | Cloud VPS / DuckDNS | `Ubuntu 24.04` / `Docker 27.x` |
| Backend Runtime & API Container | Eclipse Temurin JRE Alpine + Spring Boot | Adoptium / Broadcom | `Java 21` / `4.1.0` |
| Relational & Vector Database Server | PostgreSQL with `pgvector` and `pgcrypto` | PostgreSQL Global Dev Group | `17` (`pgvector:pg17`) |
| S3-Compatible Object Storage | MinIO Server (`inspection-evidence` bucket) | MinIO Inc. | `RELEASE.2025` |
| Computer Vision Defect Inference Container | Python Slim + FastAPI + Ultralytics YOLO11 (`MBDD2025`) | Python / Ultralytics | `Python 3.11` / `8.3.55` |
| Web & Mobile Test Clients | Google Chrome / Edge + Flutter Android Client | Google / Microsoft | `Evergreen` / `API 34` |

### 3.3 Test Milestones

| Milestone Task | Start Date | End Date |
| --- | --- | --- |
| Milestone 1: Unit & Migration Foundation Gate (Schema, Auth, RBAC, Modulith Boundaries) | `2026-09-15` | `2026-10-08` |
| Milestone 2: Core Inspection, MinIO, YOLO11 & PDF Reporting Integration Testing | `2026-10-09` | `2026-10-22` |
| Milestone 3: Review 2 Baseline & RAG Maintenance Verification | `2026-10-23` | `2026-10-27` |
| Milestone 4: 5-Role Platform Service Consolidation (`V7`–`V28`), Contracts, PayOS/VNPay & 3-Way Re-inspection Verification | `2026-10-28` | `2026-11-03` |
| Milestone 5: Final Regression & Live Demo Rehearsal (`100%` Workflows, `>= 90%` Pass Rate across `Feature 1`–`Feature 8`) | `2026-11-04` | `2026-11-30` |

---

## 4. Test Cases

**8-Feature Functional Test Suite Structure (`FE-01` to `FE-08`)**

The functional test case inventory in `Report5_Test Report.xlsx` is organized across **8 Feature sheets (`Feature 1` through `Feature 8`, mapped 1-to-1 to `FE-01` through `FE-08`, 2 features per team member)**:
- **`Feature 1` (`FE-01` — Trần Hoàng Trung Hiếu)**: Customer airspace registration, Argon2id & Google OAuth2 sign-in, OTP verification, session rotation, `/users/me`, and 5-role `ActorZone` RBAC (`WF1-001`–`WF1-005` — `5` TCs).
- **`Feature 2` (`FE-02` — Trần Hoàng Trung Hiếu)**: Platform-provisioned Inspector profiles & flight logs, Customer Maintenance Engineer provisioning, Asset catalog with No-Fly Zone guard, and Inspector-owned Drone 3-document registration & review (`WF1-006`–`WF1-016` — `11` TCs).
- **`Feature 3` (`FE-03` — Phùng Trung Quốc)**: Recurring service request occurrence generation, month-end date anchoring, recurrence window validation, and deduplicated transactional outbox notifications (`WF1-017`–`WF1-021` — `5` TCs).
- **`Feature 4` (`FE-04` — Phùng Trung Quốc)**: Service requests, VND quotations, Order Chat, signed paper contract upload, cross-org partner dispatch, abort re-dispatch, and Vietnam Airspace Map (`WF2-001`–`WF2-005` — `5` TCs).
- **`Feature 5` (`FE-05` — Trần Tùng Bách)**: Flight permit upload gate, 2-outcome field sessions (`Start`, `Complete`, `Abort`) with `SmartDroneHub` telemetry/trace sync, 5-role dashboard, schedule calendar, and 5-stage Customer Progress Tracker (`WF2-008`–`WF2-009`, `WF2-011`–`WF2-012`, `WF2-015`–`WF2-020`, `WF3-009` — `11` TCs).
- **`Feature 6` (`FE-06` — Trần Tùng Bách)**: Photo & streaming MP4 video evidence intake, `YOLO11` + Vision LLM fallback, findings preview & baseline confirmation (`findings_confirmed_at`), 4-state inspection report (`SUBMITTED`, `RETURNED`, `PUBLISHED`, `SUPERSEDED`), AI Executive Summary, direct Manager publication, on-demand PDF rendering, and PayOS VietQR / VNPay settlement (`WF3-001`–`WF3-008`, `WF3-010`, `WF3-012`, `WF3-016`, `WF3-017` — `12` TCs).
- **`Feature 7` (`FE-07` — Trương Thái Như)**: Work order creation with 1-click RAG initial tasks, team assignment, RAG cost norms estimator (`suggest-estimate`), Customer budget/Change Order approval, field repair execution, and 1-click batch work-log verification (`WF4-001`–`WF4-011` — `11` TCs).
- **`Feature 8` (`FE-08` — Trương Thái Như)**: Smart auto-drafted completion report (`auto-draft`), RAG acceptance compliance audit (`acceptance-compliance`), 3-step/3-way Re-inspection defect verification loop, independent Customer acceptance, and cost reconciliation/closure (`WF4-012`–`WF4-016` — `5` TCs).

**Test Case Artifacts**

- **Unit & Integration Test Suites**: Automated JUnit Jupiter & Testcontainers (`SmartDroneInspection-backend`, 111 test classes), Vitest (`SmartDroneInspection-frontend`, 78 test files), and Flutter Test (`SmartDroneInspection-mobile`, 15 test files).
- **System & Functional Test Workbook**: `Report5_Test Report.xlsx` (`Cover`, `Test Cases`, `Test Statistics`, and `Feature 1` through `Feature 8`).

---

## 5. Test Reports

**Execution Summary Across `Feature 1` through `Feature 8`**

The functional test suite in `Report5_Test Report.xlsx` tracks **65 test cases** (`64` baseline cases + `WF3-017`) across the 8 product features (`FE-01` to `FE-08`):
- **Total Test Cases**: `65` (`5 + 11 + 5 + 5 + 11 + 12 + 11 + 5 = 65`)
- **Round 1 Passed**: `60` (`92.31%` overall / `93.75%` of the 64-case baseline)
- **Round 1 Failed**: `0`
- **Round 1 Pending**: `5` (`WF1-010`, `WF2-015`, `WF3-017`, `WF3-012`, `WF4-011` — manual staging walkthroughs and live provider checks scheduled for Milestone 5)
- **Round 1 N/A**: `0`
- **Round 2 & Round 3 Regression**: Round 2 verified all 15 automated `FE-07` and `FE-08` maintenance cases (`15 Passed`), and Round 3 verified direct report publication and on-demand PDF supersession in `FE-06` (`WF3-006`, `WF3-016` `Passed`).
- **Defect Status**: All 6 historical defects tracked in `Report3_Project Tracking.xlsx` have been resolved, verified by automated regression tests, and closed (`0` open Critical or High defects).
