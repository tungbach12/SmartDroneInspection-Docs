---
title: "Report 5 - Software Test Documentation"
document_type: report5-doc-section
weight: 15
source: "Report5_Test Documentation.docx"
---

# II. Testing Documentation

## 1. Scope of Testing

**Features and Functions to be Tested (`FE-01` to `FE-08`)**

Testing covers the complete SmartDroneInspection platform across the Web Portal (`SmartDroneInspection-frontend`), Flutter Mobile Field Application (`SmartDroneInspection-mobile`), Spring Boot 4.1 Modulith Backend (`SmartDroneInspection-backend`, Flyway `V1`–`V28` schema with 36 PostgreSQL 17 tables), and AI/Telemetry/Payment integrations across all eight product features (`FE-01` to `FE-08`, two features per team member) and business rules (`BR-01` to `BR-49`):
- **`FE-01` — Customer Registration, Sign-In and Account Access** *(Owner: Trần Hoàng Trung Hiếu)*: Customer organization and initial asset registration with No-Fly Zone airspace gate (`ProspectiveCustomerRegistration`), Argon2id credential sign-in, consolidated `OtpChallenge` verification (`LOGIN`, `REGISTRATION`, `PASSWORD_RESET`), Google OAuth 2.0 (Web callback & Mobile `smartdrone://auth` deep link), HS256 JWT + HmacSHA256 refresh rotation (`AuthSession`), `/api/v1/users/me` profile, CSRF & IP rate-limiting (`AuthRateLimitFilter`, `10 req/60s`), and 5-role `ActorZone` RBAC (`ADMIN`, `MANAGER`, `CUSTOMER`, `INSPECTOR`, `MAINTENANCE_ENGINEER`).
- **`FE-02` — Partner Qualification, Workforce, Assets and Drone Registration** *(Owner: Trần Hoàng Trung Hiếu)*: Platform-provisioned `INSPECTOR` accounts with pilot license profiles (`inspector_profiles`) and flight logs (`inspector_flight_logs`), restricted-airspace Customer registration review (`AirspaceReviewController`), Customer `MAINTENANCE_ENGINEER` workforce provisioning (`WorkforceController`), infrastructure asset catalog with `inspection_items` checkpoints, SHA-256 reference documents in MinIO and No-Fly Zone guard, and Inspector-owned Drone registration with 3 mandatory documents (`REGISTRATION`, `OWNERSHIP`, `INSPECTION`).
- **`FE-03` — Recurring Service Requests, Occurrences and Notifications** *(Owner: Phùng Trung Quốc)*: Recurring `ServiceRequest` cadence validation (`DAY`/`WEEK`/`MONTH`), count-bound and end-date-bound `ServiceRequestOccurrence` materialization with month-end date anchoring, parent signed contract inheritance, and deduplicated in-app notifications (`uq_notifications_deduplication_key`) driven by Spring Modulith transactional domain events (`event_publication`).
- **`FE-04` — Service Requests, Quotations, Agreements and Dispatch** *(Owner: Phùng Trung Quốc)*: One-time and recurring customer service requests, Order Chat (`ServiceRequestMessage`), versioned VND quotations (`ServiceRequestQuote`), signed paper service agreement upload/streaming, cross-organization Inspector and owned Drone dispatch (`Mf2InspectionAssignmentAdapter`) with schedule-conflict guards, abort recovery dispatch (`reschedule`, `reassign`, `cancel`), and interactive Vietnam Airspace evaluation (`AirspaceAdvisoryService`, `AirspaceNoFlyMap`, `AirspaceAdvisoryCard`).
- **`FE-05` — Flight Permit and On-Site Field Sessions** *(Owner: Trần Tùng Bách)*: Aviation flight permit upload with pilot license validity checked at upload time (`uploadFlightPermit`), field session start requiring a stored permit file key (`hasFlightPermit()`), Web/Flutter Mobile on-site field sessions (`Start` $\rightarrow$ `Complete` or `Abort` with automatic mission reopen to `SCHEDULED` and manager alert), `SmartDroneHub` live telemetry, persisted flight report metrics, GPS flight trace (`V28` `flight_trace_json`), and mission MP4 video sync (`InspectionDroneHubService`), 5-role operational analytics dashboards (`DashboardAnalyticsService`), Inspector Schedule Calendar, and Customer 5-Stage Inspection Progress Tracker.
- **`FE-06` — Evidence, Findings, Reports and Payment** *(Owner: Trần Tùng Bách)*: Multipart photo (`10 MB`) and streaming `video/mp4` (`500 MB`) evidence intake (`file_picker` on Mobile, `AuthenticatedMedia` and interactive video frame cropping on Web) with EXIF GPS extraction, `YOLO11` (`MBDD2025`) photo and video keyframe defect detection (`POST /evidence/{id}/analyze` & `/analyze-video`) with automatic Vision LLM fallback (`PrimaryWithFallbackInference`), findings baseline confirmation (`findings_confirmed_at`), 4-state Inspection Report lifecycle (`SUBMITTED`, `RETURNED`, `PUBLISHED`, `SUPERSEDED`), AI Executive Summary generation, independent `MANAGER` direct approval and publication (`SUBMITTED` $\rightarrow$ `PUBLISHED`), on-demand A4 PDF rendering (`PdfReportRenderer`), Customer report acceptance, and online VND payment settlement via **PayOS (VietQR)** and **VNPay (`v2.1.0`)**.
- **`FE-07` — Maintenance Work Orders, Estimates and Repair Execution** *(Owner: Trương Thái Như)*: Forwarded defect triage into 12-state `MaintenanceWorkOrder`s, `pgvector` RAG repair scope advisor (`TCVN`/`EN`/`ISO` with `DeterministicScopeFallback`) and 1-click `initialTasks` provisioning, engineering team role assignment (`LEAD`, `REPORT_AUTHOR`, `MEMBER`, and independent `acceptingReviewerUserId`), RAG Cost & Norms Estimator (`suggest-estimate`), independent Customer budget & Change Order approval, field repair execution with before/after proof, and 1-click Team Lead batch work-log verification (`batch-verify`).
- **`FE-08` — Completion, Re-inspection and Work-Order Closeout** *(Owner: Trương Thái Như)*: Smart template auto-drafted Maintenance Completion Report (`auto-draft`), RAG Technical Acceptance Compliance Audit (`acceptance-compliance`), event-driven 3-step/3-way Re-inspection defect verification loop (`reinspection_defect_verifications`: Prior Defect vs Engineer Repair Proof vs Drone Re-capture), automatic work-order reinstatement upon re-inspection publication (`WorkOrderReinspectionListener`), independent Customer acceptance, baseline-to-actual cost inheritance & reconciliation, and Work Order closure (`CLOSED`).

**Non-Functional Requirements to be Tested (`NFR-01` to `NFR-06`)**

- **`NFR-01` (Performance — API Latency)**: Standard JSON API actions, searches, and paged list views achieve `p95 <= 2.0 seconds` (`<= 500 ms` target on local/containerized probes) with `0%` 5xx errors under `50` concurrent users (`WF2-016`).
- **`NFR-02` (Performance — AI Inference Latency & Fallback)**: Single-image `YOLO11` defect detection and `pgvector` RAG advisory requests complete within `<= 5.0 seconds` and fall back deterministically when external AI endpoints are offline (`WF3-007`, `WF4-002`).
- **`NFR-03` (Security — Multi-Zone & 5-Role Isolation)**: `100%` of unauthorized or cross-organization API/route requests are blocked with `403 Forbidden` or `404 Not Found` and `0` cross-tenant data disclosures (`WF1-005`, `WF2-020`).
- **`NFR-04` (Security — Lockout, Rate-Limiting & Session Rotation)**: Account locks for `15 minutes` after `5` failed login attempts, requests exceeding `10 req/60s` per IP return `429 Too Many Requests`, and replayed refresh tokens revoke the active `AuthSession` (`WF1-004`).
- **`NFR-05` (Reliability — Document & Published PDF Immutability)**: Signed contracts, SHA-256 asset documents, and published A4 PDF reports remain immutable across version supersession (`WF1-012`, `WF3-016`).
- **`NFR-06` (Maintainability — Modulith Boundaries, Schema & Coverage Gate)**: `0` Spring Modulith boundary violations, verified 36-table `Flyway V1–V28` schema inventory, and `>= 80%` JaCoCo backend coverage (`WF4-005`).

**Items Not to be Tested (Out of Scope)**

- Physical unmanned aircraft radio-control (RC) actuation, hardware flight controller firmware, and physical structural construction work (`BR-16`).
- Native mobile OS push notification gateways (APNs/FCM) and third-party commercial SMTP relay infrastructure (in-app notifications and OTP challenges are verified through the application database and API).
- Internal banking core systems of VietQR/PayOS and VNPay beyond signed checkout URL generation and HMAC-SHA256 / HMAC-SHA512 webhook verification.

**Stages and Levels of Testing**

- **Unit Testing**:
  - *In-charge*: Individual feature developers (`Trần Hoàng Trung Hiếu`, `Phùng Trung Quốc`, `Trần Tùng Bách`, `Trương Thái Như`).
  - *Inputs / Time*: Domain entities, services, utility classes, React components/hooks, and Flutter widgets/repositories; executed continuously on every local build and pull request commit (`Milestone 1`–`Milestone 5`).
  - *Focuses*: Domain invariants, state-transition guards, password/role policies, financial calculators, EXIF extraction, HMAC signature verification, deterministic fallbacks, and UI component rendering.
  - *Acceptance Criteria*: `100%` of unit tests pass across JUnit Jupiter (`111` backend test classes), Vitest (`78` frontend test files), and Flutter Test (`15` mobile test files) with `>= 80%` backend JaCoCo line coverage.
- **Integration Testing**:
  - *In-charge*: Feature owners for `MF1`–`MF4` (`Hiếu`, `Quốc`, `Bách`, `Như`).
  - *Inputs / Time*: Spring Boot REST controllers, JPA repositories, Flyway migrations `V1`–`V28`, Spring Security filter chain, and MinIO object storage; executed on every pull request via Testcontainers (`Milestone 1`–`Milestone 5`).
  - *Focuses*: Database schema migration integrity (`36` tables), composite tenant foreign keys, `ActorZone` and `@PreAuthorize` authorization, Spring Modulith event outbox delivery (`event_publication`), MinIO streaming, and PDF rendering.
  - *Acceptance Criteria*: `0` Spring Modulith boundary violations, all `28` Flyway migrations and `36` tables verified (`FullDatabaseSchemaMigrationTest`, `RuntimePersistenceInventoryTest`), and `100%` of API integration tests passing.
- **System Testing**:
  - *In-charge*: Full-stack engineering team (`Hiếu`, `Quốc`, `Bách`, `Như`).
  - *Inputs / Time*: Complete multi-container system (Backend, Frontend, Mobile, PostgreSQL 17 `pgvector`, MinIO, FastAPI YOLO11, SmartDroneHub, PayOS/VNPay webhooks) and SRS/SDD specifications (`Milestone 2`–`Milestone 5`).
  - *Focuses*: End-to-end main business flows (`WF-01` through `WF-04` in `ConnectedMainFlowE2eIntegrationTest`), cross-client synchronization between Web and Mobile, and non-functional thresholds (`NFR-01`–`NFR-06`).
  - *Acceptance Criteria*: All 4 connected main workflows (`MF1` $\rightarrow$ `MF2` $\rightarrow$ `MF3` $\rightarrow$ `MF4`) execute end-to-end without error and all 6 NFR targets are satisfied.
- **Acceptance Testing**:
  - *In-charge*: All 4 team members under the review of project supervisors (`Phạm Minh Trí`, `Đặng Ngọc Minh Đức`).
  - *Inputs / Time*: Report 3 SRS (`FE-01`–`FE-08`, `BR-01`–`BR-49`) and the 65 functional test cases in `Report5_Test Report.xlsx` (`Milestone 3`–`Milestone 5`).
  - *Focuses*: Verification of business acceptance rules, separation of duties (independent report publication, independent budget approval, and independent maintenance acceptance), and staging walkthroughs on `https://smartdroneinspection.duckdns.org`.
  - *Acceptance Criteria*: `>= 90%` pass rate across `Feature 1`–`Feature 8` with `0` open Critical or High severity defects.

**Constraints and Assumptions**

- **Containerized Infrastructure Constraint**: Backend database and object storage integration tests require a running Docker daemon to provision `pgvector/pgvector:pg17` and `minio/minio` Testcontainers instances.
- **External AI & Telemetry Service Assumption**: When the external OpenAI-compatible LLM gateway or YOLO11 container is unreachable in isolated test runs, the system is designed to route automatically to `PrimaryWithFallbackInference` and `DeterministicScopeFallback` so business workflows remain testable and deterministic.
- **Payment Gateway Sandbox Assumption**: Online payment verification uses deterministic HMAC-SHA256 (PayOS) and HMAC-SHA512 (VNPay) test credentials and signed webhook payloads rather than live commercial bank debits.
- **Aviation & Field Operation Boundary (`BR-16`)**: Flight permits, airspace evaluations, and `SmartDroneHub` telemetry logs represent software governance records; physical aircraft flight safety remains the responsibility of licensed human pilots.

---

## 2. Test Strategy

This section defines the testing types, the four test levels at which they are executed, and the supporting tools used to verify functional and non-functional quality across the project.

### 2.1 Testing Types
- **Functional & Business Rule Testing**:
  - *Objective*: Verify that every mandatory feature (`FE-01`–`FE-08`) and business rule (`BR-01`–`BR-49`) behaves according to the SRS specifications and API contracts.
  - *Technique*: Equivalence partitioning, boundary-value analysis (`10 MB` photo/document and `500 MB` MP4 video file limits, `[-90..90]`/`[-180..180]` coordinates, `0..100%` finance rates), and positive/negative API/UI scenarios.
  - *Completion Criteria*: Complete functional test coverage across `Feature 1`–`Feature 8` with all automated test suites passing.
- **Domain State Machine Transition Testing**:
  - *Objective*: Ensure every lifecycle entity transitions only along valid, authorized edges and rejects illegal or out-of-order state mutations (`400 Bad Request` / `409 Conflict`).
  - *Technique*: State-transition path coverage across `ServiceRequest` (6 states), `ServiceRequestOccurrence` (payment & payout lifecycles), `Asset` (3 states), `Drone` (3 states), `DroneRegistrationApplication` (3 states), `Inspection` (6 states), `FieldSession` (4 states), `Finding` (2 states), `InspectionReport` (4 states: `SUBMITTED`, `RETURNED`, `PUBLISHED`, `SUPERSEDED`), `ReinspectionDefectVerification` (3-way), and `MaintenanceWorkOrder` (12 states).
  - *Completion Criteria*: `100%` of domain entity state machines covered by positive and negative transition tests.
- **Security, RBAC & Multi-Zone Isolation Testing**:
  - *Objective*: Verify zero cross-tenant data leakage, strict `ActorZone` and role separation of duties (authors/team members cannot self-approve or self-accept; Customers cannot read unpublished reports), CSRF enforcement, account lockout, and IP rate-limiting.
  - *Technique*: Cross-organization ID probing, 5-role matrix permutation testing, token revocation checks, and brute-force rate-limit simulation (`AuthRateLimitFilter`).
  - *Completion Criteria*: `100%` of unauthorized or cross-scope requests rejected (`NFR-03`, `NFR-04`).
- **AI Vision, Executive Summary & pgvector RAG Advisory Testing**:
  - *Objective*: Verify accurate bounding-box parsing from `YOLO11`, automatic Vision LLM fallback on empty/offline results, AI Executive Summary generation, and `pgvector` cosine similarity retrieval (`TCVN`/`EN`/`ISO`) with deterministic fallback.
  - *Technique*: Mocked and containerized inference responses, empty-detection fallback simulation (`PrimaryWithFallbackInferenceTest`), and offline LLM fallback assertions (`DeterministicScopeFallbackTest`).
  - *Completion Criteria*: `100%` of AI advisory endpoints return valid structured responses or deterministic fallbacks within `<= 5.0 seconds` (`NFR-02`).
- **Performance, Payment Webhook & PDF Immutability Testing**:
  - *Objective*: Validate API response latency (`NFR-01`), PayOS HMAC-SHA256 and VNPay HMAC-SHA512 webhook signature verification, and published PDF report immutability (`NFR-05`).
  - *Technique*: Concurrent virtual-user API probes, tampered-signature webhook rejection tests (`PayOSCryptoTest`, `VnPayCryptoTest`), and multi-version PDF supersession checks (`InspectionReportSectionsApiIntegrationTest`).
  - *Completion Criteria*: All performance, cryptographic signature, and document immutability assertions pass with zero regressions.
- **User Interface, Localization & Regression Testing**:
  - *Objective*: Verify responsive Web and Mobile UI behavior, bilingual English/Vietnamese (`en`/`vi`) localization, dark/light mode persistence, and zero regression across schema or feature updates.
  - *Technique*: Component/widget rendering tests in Vitest and Flutter Test, `Accept-Language` header negotiation tests, and automated CI regression runs.
  - *Completion Criteria*: All Web, Mobile, and Backend localization and regression suites pass.

### 2.2 Test Levels

The project executes four sequential test levels:
- **Unit Level**: Verifies isolated domain entities, value objects, services, cryptographic helpers, React components/hooks, and Flutter widgets/repositories using in-memory mocks and fast test runners.
- **Integration Level**: Verifies module boundaries (`Spring Modulith`), Flyway database migrations (`V1`–`V28`, 36 tables), JPA repositories, MockMvc security filter chains, MinIO storage adapters, and payment/AI client adapters against containerized PostgreSQL 17 and MinIO instances.
- **System Level**: Verifies end-to-end multi-role business workflows (`WF-01` to `WF-04`), cross-module domain events, and non-functional performance/security thresholds across the integrated stack.
- **Acceptance Level**: Verifies business rules (`BR-01`–`BR-49`) and user requirements across the 8 product features (`FE-01`–`FE-08` / `Feature 1`–`Feature 8`) against the SRS acceptance criteria.

| Type of Tests | Unit | Integration | System | Acceptance |
| --- | :---: | :---: | :---: | :---: |
| Functional & Business Rule Testing | X | X | X | X |
| Domain State Machine Transition Testing | X | X | X | X |
| API & Database Persistence Testing (`Flyway V1–V28`, 36 PostgreSQL 17 tables) |  | X | X |  |
| Security, RBAC & ActorZone Isolation Testing | X | X | X | X |
| AI Vision, Executive Summary & pgvector RAG Testing | X | X | X | X |
| Performance, PayOS/VNPay Webhook & PDF Immutability Testing |  | X | X | X |
| User Interface, Localization (EN/VI) & Regression Testing | X | X | X | X |

### 2.3 Supporting Tools

The following tools are employed for test authoring, execution, coverage verification, and report generation:

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

The table below lists the project members and supervisors involved in test design, execution, and review:

| Worker/Doer | Role | Specific Responsibilities/Comments |
| --- | --- | --- |
| **Trần Hoàng Trung Hiếu** (`SE184212`) | Project Leader & Tester (`MF1`: `FE-01`, `FE-02` Owner) | Owns functional and integration test cases on Sheets **`Feature 1` and `Feature 2`** covering `FE-01` (Customer Registration, Sign-In & 5-Role Access Control) and `FE-02` (Partner Qualification, Workforce, Assets & Drone Registration). |
| **Phùng Trung Quốc** (`SE170027`) | Backend / Mobile Engineer & Tester (`MF2`: `FE-03`, `FE-04` Owner) | Owns functional and integration test cases on Sheets **`Feature 3` and `Feature 4`** covering `FE-03` (Recurring Service Requests, Occurrences & Notifications) and `FE-04` (Service Requests, VND Quotations, Agreements, Dispatch & Airspace Map). |
| **Trần Tùng Bách** (`SE180220`) | Full-Stack / AI Engineer & Tester (`MF3`: `FE-05`, `FE-06` Owner) | Owns functional and integration test cases on Sheets **`Feature 5` and `Feature 6`** covering `FE-05` (Flight Permit Gate, Field Sessions, SmartDroneHub, Dashboard & Calendar) and `FE-06` (Evidence Intake, YOLO11 Detection, Reports & PayOS/VNPay). |
| **Trương Thái Như** (`SE180082`) | Full-Stack Engineer & Tester (`MF4`: `FE-07`, `FE-08` Owner) | Owns functional and integration test cases on Sheets **`Feature 7` and `Feature 8`** covering `FE-07` (Maintenance Work Orders, RAG Scope/Norms Advisor & Repair Execution) and `FE-08` (Completion Report, 3-Way Re-inspection Verification & Cost Closure). |
| **Phạm Minh Trí & Đặng Ngọc Minh Đức** | Supervisors / Reviewers | Review test strategy, audit traceability across Reports 3–5, and evaluate defense readiness. |

### 3.2 Test Environment

The software, hardware, and cloud infrastructure used to execute the test suites are detailed below:

| Purpose | Tool | Provider | Version |
| --- | --- | --- | --- |
| Cloud Staging Server | Ubuntu Linux VPS (`https://smartdroneinspection.duckdns.org`, Docker Compose, Nginx, Tailscale) | Cloud VPS / DuckDNS | `Ubuntu 24.04` / `Docker 27.x` |
| Backend Runtime & API Container | Eclipse Temurin JRE Alpine + Spring Boot Modulith | Adoptium / Broadcom | `Java 21` / `4.1.0` |
| Relational & Vector Database Server | PostgreSQL with `pgvector` and `pgcrypto` (36 tables, `V1`–`V28`) | PostgreSQL Global Dev Group | `17` (`pgvector:pg17`) |
| S3-Compatible Object Storage | MinIO Server (`inspection-evidence` bucket) | MinIO Inc. | `RELEASE.2025` |
| Computer Vision & Telemetry Services | FastAPI + Ultralytics YOLO11 (`MBDD2025`) & `SmartDroneHub` Service | Python / Ultralytics / In-house | `Python 3.11` / `8.3.55` |
| Web & Mobile Test Clients | Google Chrome / Edge (Desktop) + Flutter Android Client | Google / Microsoft | `Evergreen` / `API 34` |

### 3.3 Test Milestones

Testing activities are scheduled across five project milestones aligned with the iterative build plan:

| Milestone Task | Start Date | End Date |
| --- | --- | --- |
| Milestone 1: Unit & Migration Foundation Gate (Schema, Auth, RBAC, Modulith Boundaries) | `2026-09-15` | `2026-10-08` |
| Milestone 2: Core Inspection, MinIO, YOLO11 & PDF Reporting Integration Testing | `2026-10-09` | `2026-10-22` |
| Milestone 3: Review 2 Baseline & RAG Maintenance Verification (`Round 1` Execution) | `2026-10-23` | `2026-10-27` |
| Milestone 4: 5-Role Platform Service Consolidation (`V7`–`V28`), Contracts, PayOS/VNPay & 3-Way Re-inspection (`Round 2` & `Round 3`) | `2026-10-28` | `2026-11-04` |
| Milestone 5: Final Staging Walkthroughs & Live Demo Rehearsal (`100%` Workflows, `>= 90%` Pass Rate across `Feature 1`–`Feature 8`) | `2026-11-05` | `2026-11-30` |

---

## 4. Test Cases

The project's test cases are organized into two complementary deliverables following the capstone templates:

- **Unit Test Cases (`Report5_Unit Test.xls` & Repository Unit Test Suites)**:
  - **Backend Unit & Slice Tests (`SmartDroneInspection-backend/src/test/java`)**: `111` JUnit Jupiter test classes verifying domain state transitions (`AssetTest`, `DroneTest`, `ServiceRequestTest`, `FindingTest`, `InspectionReportTest`, `MaintenanceWorkOrderLifecycleTest`), service logic (`ContractWorkflowServiceTest`, `InspectorProfileServiceTest`, `EvidenceServiceTest`, `MaintenanceScopeAdvisorServiceTest`, `DeterministicScopeFallbackTest`), cryptographic verification (`PayOSCryptoTest`, `VnPayCryptoTest`, `PasswordPolicyTest`), and architecture/schema contracts (`ModulithArchitectureTest`, `FullDatabaseSchemaMigrationTest`, `RuntimePersistenceInventoryTest`).
  - **Frontend Unit & Component Tests (`SmartDroneInspection-frontend/src`)**: `78` Vitest and React Testing Library test files verifying 5-role route guards (`accessPolicy.test.ts`, `router.test.ts`), airspace maps (`AirspaceNoFlyMap.test.tsx`), schedule calendars (`InspectorScheduleCalendar.test.tsx`), evidence/findings/report workflows (`InspectionEvidencePage.test.tsx`, `InspectionFindingsPage.test.tsx`, `InspectionDraftPage.test.tsx`, `ReportDetailPage.test.tsx`), and maintenance views (`MaintenancePage.test.tsx`).
  - **Mobile Unit & Widget Tests (`SmartDroneInspection-mobile/test`)**: `15` Flutter test files verifying mobile authentication, `AirspaceAdvisoryCard`, `FieldSessionPage`, photo/MP4 capture, bilingual localization (`locale_provider_test.dart`), and `MaintenanceRepository`.
- **Other Test Cases — Integration, System, and Acceptance Testing (`Report5_Test Report.xlsx`)**:
  - Contains **65 functional test cases** (`WF1-001`–`WF4-016` plus `WF3-017`) partitioned across **8 Feature sheets (`Feature 1` through `Feature 8`, mapped 1-to-1 to `FE-01` through `FE-08`, 2 features per team member)**:
    - **`Feature 1` (`FE-01` — Trần Hoàng Trung Hiếu, `5` TCs: `WF1-001`–`WF1-005`)**: Customer airspace registration, Argon2id & Google OAuth2 sign-in, OTP verification, session rotation, `/users/me`, and 5-role `ActorZone` RBAC.
    - **`Feature 2` (`FE-02` — Trần Hoàng Trung Hiếu, `11` TCs: `WF1-006`–`WF1-016`)**: Platform-provisioned Inspector profiles & flight logs, restricted-airspace Customer review, Customer Maintenance Engineer provisioning, Asset catalog with No-Fly Zone guard, and Inspector-owned Drone 3-document registration & approval.
    - **`Feature 3` (`FE-03` — Phùng Trung Quốc, `5` TCs: `WF1-017`–`WF1-021`)**: Recurring service request occurrence materialization, month-end date anchoring, recurrence window validation, deduplicated outbox notifications, and connected `WF-01`/`WF-02` flow.
    - **`Feature 4` (`FE-04` — Phùng Trung Quốc, `5` TCs: `WF2-001`–`WF2-005`)**: Service requests, VND quotations, Order Chat, signed paper contract upload, cross-org partner dispatch, abort re-dispatch, and Vietnam Airspace Map.
    - **`Feature 5` (`FE-05` — Trần Tùng Bách, `11` TCs: `WF2-008`–`WF2-009`, `WF2-011`–`WF2-012`, `WF2-015`–`WF2-020`, `WF3-009`)**: Flight permit upload gate, 2-outcome field sessions (`Start`, `Complete`, `Abort`) with `SmartDroneHub` telemetry/trace sync, 5-role dashboard, schedule calendar, and 5-stage Customer Progress Tracker.
    - **`Feature 6` (`FE-06` — Trần Tùng Bách, `12` TCs: `WF3-001`–`WF3-008`, `WF3-010`, `WF3-012`, `WF3-016`, `WF3-017`)**: Photo & streaming MP4 video evidence intake, `YOLO11` + Vision LLM fallback, findings baseline confirmation (`findings_confirmed_at`), 4-state inspection report (`SUBMITTED`, `RETURNED`, `PUBLISHED`, `SUPERSEDED`), AI Executive Summary, direct Manager publication, on-demand PDF rendering, and PayOS VietQR / VNPay settlement.
    - **`Feature 7` (`FE-07` — Trương Thái Như, `11` TCs: `WF4-001`–`WF4-011`)**: Work order creation with 1-click RAG initial tasks, team assignment, RAG cost norms estimator (`suggest-estimate`), Customer budget/Change Order approval, field repair execution, and 1-click batch work-log verification.
    - **`Feature 8` (`FE-08` — Trương Thái Như, `5` TCs: `WF4-012`–`WF4-016`)**: Smart auto-drafted completion report (`auto-draft`), RAG acceptance compliance audit (`acceptance-compliance`), 3-step/3-way Re-inspection defect verification loop, independent Customer acceptance, and cost reconciliation/closure.

---

## 5. Test Reports

**Test Results and Statistics Summary**

The execution results recorded in `Report5_Test Report.xlsx` (`Test Statistics` and `Feature 1`–`Feature 8`) are summarized below:
- **Total Functional Test Cases**: `65` (`64` baseline cases + `WF3-017`)
- **Round 1 Execution Totals**: `60 Passed`, `0 Failed`, `5 Pending`, `0 N/A`
  - `Feature 1` (`FE-01`): `5 Passed`, `0 Failed`, `0 Pending` (`5` total — `100.00%`)
  - `Feature 2` (`FE-02`): `10 Passed`, `0 Failed`, `1 Pending` (`11` total — `90.91%`)
  - `Feature 3` (`FE-03`): `5 Passed`, `0 Failed`, `0 Pending` (`5` total — `100.00%`)
  - `Feature 4` (`FE-04`): `5 Passed`, `0 Failed`, `0 Pending` (`5` total — `100.00%`)
  - `Feature 5` (`FE-05`): `10 Passed`, `0 Failed`, `1 Pending` (`11` total — `90.91%`)
  - `Feature 6` (`FE-06`): `10 Passed`, `0 Failed`, `2 Pending` (`12` total — `83.33%`)
  - `Feature 7` (`FE-07`): `10 Passed`, `0 Failed`, `1 Pending` (`11` total — `90.91%`)
  - `Feature 8` (`FE-08`): `5 Passed`, `0 Failed`, `0 Pending` (`5` total — `100.00%`)
- **Test Coverage & Successful Coverage**: `92.31%` overall (`60 / 65`), and `93.75%` (`60 / 64`) against the 64-case baseline, exceeding the `>= 90%` project quality gate.
- **Round 2 & Round 3 Regression Results**:
  - **Round 2**: Re-verified all `15` automated `FE-07` (`WF4-001`–`WF4-010`) and `FE-08` (`WF4-012`–`WF4-016`) maintenance cases (`15 Passed`, `0 Failed`).
  - **Round 3**: Re-verified direct report publication (`SUBMITTED -> PUBLISHED`, `WF3-006`) and on-demand PDF rendering/supersession (`WF3-016`) in `FE-06` (`2 Passed`, `0 Failed`).

**Relevant Test Analysis**

1. **Functional & Main Workflow Readiness**: All 4 end-to-end main business workflows (`WF-01` Onboarding/Assets/Drones, `WF-02` Service Requests/Contracts/Dispatch/Field Sessions, `WF-03` Evidence/YOLO11/Reports/PayOS-VNPay, and `WF-04` Maintenance/RAG/3-Way Re-inspection/Closure) have passing automated integration and end-to-end coverage (`ConnectedMainFlowE2eIntegrationTest`), with `0` failed test cases across all 8 features.
2. **Analysis of Remaining `Pending` Cases (`5` Cases)**: The `5` `Pending` items (`WF1-010` in `FE-02`, `WF2-015` in `FE-05`, `WF3-017` and `WF3-012` in `FE-06`, and `WF4-011` in `FE-07`) are manual live-staging walkthroughs on `https://smartdroneinspection.duckdns.org` and live external Vision provider checks scheduled for Milestone 5 rehearsal. Their underlying backend services, state transitions, and UI components are already covered by passing automated unit and integration tests.
3. **Non-Functional Requirement Verification Analysis**: All 6 quantified NFRs (`NFR-01` through `NFR-06`) are backed by dedicated test cases (`WF2-016`, `WF3-007`, `WF1-005`, `WF1-004`, `WF3-016`, `WF4-005`), confirming sub-500 ms API p95 latency on containerized probes, `~1.4 s` YOLO11 single-image inference latency, `100%` cross-tenant RBAC isolation, and `0` Spring Modulith architectural violations.
4. **Defect Resolution & Quality Gate Analysis**: All `6` defects discovered during development and integration testing (audit flush ordering in `FE-01`, cross-tenant email existence masking in `FE-02`, cross-org partner scope in `FE-04`, image `ImageIO` decoding & MP4 streaming validation and report outlet context in `FE-06`, and re-inspection completion report reinstatement in `FE-08`, tracked in `Report3_Project Tracking.xlsx`) have been fixed, covered by automated regression tests, and closed (`0` open defects).
