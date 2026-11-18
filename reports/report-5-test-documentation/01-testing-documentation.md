---
title: "Report 5 - Software Test Documentation"
document_type: report5-doc-section
weight: 15
source: "Report5_Test Documentation.docx"
---

# II. Testing Documentation

## 1. Scope of Testing

**Features and Functions to be Tested (`FE-01` to `FE-08`)**

Testing covers the delivered SmartDroneInspection platform across the Web Portal (`SmartDroneInspection-frontend`), the Customer Mobile Application (`SmartDroneInspection-mobile`), the Spring Boot 4.1 Modulith backend (`SmartDroneInspection-backend`, Flyway `V1__baseline.sql` + `V2__remove_finding_recommended_action.sql`, 41 PostgreSQL 17 tables), and the AI, telemetry, and payment integrations across all eight product features — two per main flow `MF1` to `MF4` — and the business rules `BR-01`–`BR-54`. The inspection scope is buildings only.

- **`MF1` `FE-01` — Registration, Sign-in and Account Access** *(Owner: Trần Hoàng Trung Hiếu)*: Customer organization and initial building registration with the No-Fly Zone airspace gate (`ProspectiveCustomerRegistration`), password sign-in with a memory-hard hash, consolidated one-time-code verification (`LOGIN`, `REGISTRATION`, `PASSWORD_RESET`), Google OAuth 2.0 (web callback and mobile deep link), JWT access tokens with refresh-token rotation (`AuthSession`), the `/api/v1/users/me` profile, CSRF and IP rate limiting (`AuthRateLimitFilter`), and four-role route-level and API-level authorization (`accessPolicy.ts`, `@PreAuthorize`).
- **`MF1` `FE-02` — Partner Inspector and Drone Registration** *(Owner: Trần Hoàng Trung Hiếu)*: Public partner Inspector application with licence scan, review and account provisioning (`InspectorApplicationController`), pilot licence profiles (`inspector_profiles`) and flight logs (`inspector_flight_logs`), and Inspector-owned drone registration with the configurable three-document set.
- **`MF2` `FE-03` — Buildings, Airspace Screening and Notifications** *(Owner: Phùng Trung Quốc)*: The building asset catalogue with `inspection_items` checkpoints and SHA-256 reference documents in MinIO under a No-Fly Zone guard, restricted-airspace customer review (`AirspaceReviewController`), recurring `ServiceRequest` cadence validation, count-bound and end-date-bound `ServiceRequestOccurrence` materialization with month-end anchoring, and deduplicated in-app notifications (`uq_notifications_deduplication_key`) driven by Spring Modulith transactional domain events through the `event_publication` outbox.
- **`MF2` `FE-04` — Service Requests, VND Quotations, Agreements and Dispatch** *(Owner: Phùng Trung Quốc)*: One-time and recurring service requests, request-level Manager ownership and claim, order chat with private attachments, versioned VND quotations whose accepted terms are frozen into an immutable snapshot, signed paper service agreement upload and streaming, cross-organization Inspector and owned-drone dispatch with schedule-conflict guards, abort recovery dispatch, and the interactive Vietnam airspace evaluation.
- **`MF3` `FE-05` — Flight Permit and On-Site Field Sessions** *(Owner: Trần Tùng Bách)*: Mission flight-permit upload with file-signature, SHA-256 and structured-metadata checks, mandatory verification by a Manager or Administrator who is not the uploader, the field-session gate that refuses to start without a verified permit, on-site field sessions (`Start` → `Complete` or `Abort` with automatic mission reopen and Manager follow-up), `SmartDroneHub` telemetry, persisted flight report metrics and GPS flight trace (`flight_trace_json`), mission MP4 video sync, the role-scoped dashboards, the Inspector schedule calendar, and the customer progress view.
- **`MF3` `FE-06` — Evidence Intake and Human-Reviewed Defect Detection** *(Owner: Trần Tùng Bách)*: Photograph intake (10 MB, EXIF extraction before normalization to at most 2048 px, 480 px JPEG thumbnail) and resumable chunked `video/mp4` upload (10 MiB chunks up to 2 GB, asynchronous FFmpeg normalization to at most 1080p faststart with a 480 px poster, ticketed HTTP Range streaming), YOLO11 detection with automatic vision fallback, and findings baseline confirmation.
- **`MF4` `FE-07` — Inspection Report Preparation, Review and Publication** *(Owner: Trần Tùng Bách)*: The four-state inspection report lifecycle (`SUBMITTED`, `RETURNED`, `PUBLISHED`, `SUPERSEDED`), tab-visit auto-compiled report content, single-shot advisory narrative drafting, independent Manager review of a report the reviewer did not author, publication, and on-demand A4 PDF rendering of the published version.
- **`MF4` `FE-08` — Customer Report Acceptance and Payment Settlement** *(Owner: Trương Thái Như)*: Customer report acceptance, VND settlement through PayOS (VietQR) and VNPay with HMAC webhook verification, the re-inspection loop opened against a published report, and Manager-recorded partner settlement, payouts, and refunds.

**Non-Functional Requirements to be Tested (`NFR-01` to `NFR-08`)**

- **`NFR-01` (Performance — User Response Time)**: Standard user actions, searches, and paged list views reach `p95 <= 2.0 s` with `0%` server errors under `50` concurrent users.
- **`NFR-02` (Performance — Detection Latency)**: A single-image defect suggestion completes within `<= 5.0 s` for supported inputs, and detection falls back to the secondary provider or to manual entry when the primary service is unavailable.
- **`NFR-03` (Security — Role, Organization and Assignment Isolation)**: `100%` of unauthorized or cross-scope requests are blocked and `0` cross-organization disclosures occur.
- **`NFR-04` (Security — Sign-In Resistance and Access Revocation)**: Sign-in is restricted for `15 minutes` after `5` failures, more than `10` sign-in requests per minute per address are blocked, and a revoked session cannot continue to be used.
- **`NFR-05` (Reliability — Record Integrity)**: Signed documents, building documents, and published reports keep `100%` integrity and `100%` of unauthorized in-place changes are prevented.
- **`NFR-06` (Reliability — Upload Resilience)**: `100%` of interrupted video uploads are resumable and `100%` of failed transcodes retain their source for an explicit retry.
- **`NFR-07` (Maintainability — Verification Coverage and Module Boundaries)**: All eight features have applicable verification cases and `0` module boundary violations occur.
- **`NFR-08` (Portability — Rebuild and Migration Set)**: The service starts from the compose stack with the migration set exactly the declared baseline plus forward migrations.

**Items Not to be Tested (Out of Scope)**

- Physical unmanned-aircraft control, flight-controller firmware, radio-link operation, and physical structural repair work. The platform records governance and evidence; it does not fly the aircraft.
- Corrective maintenance execution: work orders, repair-scope advisory, repair execution, completion reporting, and cost close-out. No such code or schema exists in the delivered product. The platform does provide a re-inspection loop against a published report, which is tested under `FE-08`.
- Non-building infrastructure domains — bridges, transmission towers, solar farms, roads, dams, tunnels, ports, and pipelines.
- Retrieval-augmented advisory over an engineering-standard corpus. No vector column, embedding, or retrieval path exists.
- Native mobile push delivery through APNs or FCM, and commercial SMTP relay infrastructure. In-app notifications and one-time codes are verified through the application API and database.
- Internal banking core systems behind VietQR/PayOS and VNPay, beyond signed checkout generation and HMAC webhook verification.
- Mobile application behaviour for `ADMIN`, `MANAGER`, or `INSPECTOR` accounts. The mobile application admits `CUSTOMER` only, so other roles are verified to be refused rather than exercised.

**Stages and Levels of Testing**

- **Unit Testing**:
  - *In-charge*: The owning feature developer for each feature.
  - *Inputs / Time*: Domain entities, services, utilities, React components and hooks, and Flutter widgets and repositories; executed on every local build and pull request.
  - *Focuses*: Domain invariants and state-transition guards, password and role policy, financial calculation, EXIF extraction, HMAC signature verification, deterministic fallbacks, and component rendering.
  - *Acceptance Criteria*: `100%` of unit tests pass across JUnit Jupiter, Vitest, and Flutter Test, with the backend line coverage reported rather than asserted as a gate.
- **Integration Testing**:
  - *In-charge*: The owning feature developer for each feature.
  - *Inputs / Time*: Spring REST controllers, JPA repositories, Flyway migrations, the Spring Security filter chain, MinIO object storage, and the Modulith event outbox; executed on every pull request using Testcontainers.
  - *Focuses*: Schema migration integrity and the exact applied migration set, ownership and assignment foreign keys, authorization at the API boundary, event-outbox delivery, object streaming, and PDF rendering.
  - *Acceptance Criteria*: `0` Spring Modulith boundary violations, the 41-table inventory and the `["1","2"]` migration set verified, and `100%` of integration tests passing.
- **System Testing**:
  - *In-charge*: The full engineering team.
  - *Inputs / Time*: The complete multi-container system — backend, frontend, mobile client, PostgreSQL 17, MinIO, the YOLO11 inference service, SmartDroneHub, and the payment webhooks — against the SRS and SDD.
  - *Focuses*: End-to-end connected flows through `ConnectedMainFlowE2eIntegrationTest`, cross-client consistency between the web and mobile clients, and the quantified non-functional thresholds.
  - *Acceptance Criteria*: The connected `MF1` → `MF2` → `MF3` → `MF4` lifecycle executes end-to-end without error and the applicable NFR targets hold.
- **Acceptance Testing**:
  - *In-charge*: All team members, under supervisor review.
  - *Inputs / Time*: Report 3 SRS (`FE-01`–`FE-08`, `BR-01`–`BR-54`) and the functional case workbooks.
  - *Focuses*: Business acceptance rules, separation of duties, and staging walkthroughs.
  - *Acceptance Criteria*: The documented pass rate across `Feature 1`–`Feature 8` with `0` open Critical or High severity defects.

**Constraints and Assumptions**

- **Containerized infrastructure**: Database and object-storage integration tests require a running Docker daemon to provision the PostgreSQL and S3-compatible Testcontainers instances.
- **External AI and telemetry availability**: When the inference container or the language-model gateway is unreachable, the system routes to the vision fallback and to the deterministic PDF template so that business workflows remain testable.
- **Payment sandbox**: Payment verification uses deterministic HMAC test credentials and signed webhook payloads rather than live bank debits.
- **Aviation boundary**: Flight permits, airspace evaluations, and telemetry traces are software governance records. Physical flight safety remains the responsibility of the licensed human pilot, and no test claims governmental clearance.

---

## 2. Test Strategy

This section defines the testing types, the four test levels at which they are executed, and the supporting tools used to verify functional and non-functional quality.

### 2.1 Testing Types

- **Functional and Business Rule Testing**:
  - *Objective*: Verify that every feature (`FE-01`–`FE-08`) and business rule (`BR-01`–`BR-54`) behaves according to the SRS and API contracts.
  - *Technique*: Equivalence partitioning, boundary-value analysis (10 MB photo and document limits, 2 GB resumable video with 10 MiB chunks, latitude and longitude ranges, 0–100% finance rates, 20-calendar-day scheduling lead time, 2–100 occurrence bounds, 1–120 month intervals), and positive and negative API and UI scenarios.
  - *Completion Criteria*: Complete functional coverage across `Feature 1`–`Feature 8` with the automated suites passing.
- **Domain State Machine Transition Testing**:
  - *Objective*: Ensure every lifecycle entity transitions only along valid, authorized edges and rejects illegal or out-of-order mutation with a client error rather than a silent write.
  - *Technique*: State-transition path coverage across `ServiceRequest`, `ServiceRequestOccurrence`, `Asset`, `Drone`, `DroneRegistrationApplication`, `InspectorApplication`, `Inspection` (including the flight-permit verification status), `FieldSession`, `Finding`, `ServicePayment`, `ServiceRefund`, and `InspectionReport`.
  - *Completion Criteria*: `100%` of domain state machines covered by positive and negative transition tests.
- **Security and Scope Isolation Testing**:
  - *Objective*: Verify zero cross-organization leakage, strict role separation of duties, route-level denial, CSRF enforcement, account lockout, and IP rate limiting.
  - *Technique*: Cross-organization identifier probing, four-role and four-portal matrix permutation, token revocation checks, and brute-force rate-limit simulation.
  - *Completion Criteria*: `100%` of unauthorized or cross-scope requests rejected (`NFR-03`, `NFR-04`).
- **AI Vision, Narrative Drafting and Deterministic Fallback Testing**:
  - *Objective*: Verify accurate bounding-box parsing from YOLO11, automatic vision fallback on empty or unreachable results, single-shot narrative drafting, and deterministic template rendering when the model is unavailable.
  - *Technique*: Mocked and containerized inference responses, empty-detection fallback simulation, and offline drafter fallback assertions.
  - *Completion Criteria*: `100%` of advisory endpoints return valid structured output or a deterministic fallback within the stated latency bound (`NFR-02`).
- **Performance, Payment Webhook and PDF Integrity Testing**:
  - *Objective*: Validate response latency (`NFR-01`), PayOS HMAC-SHA256 and VNPay HMAC-SHA512 webhook verification, and published-report immutability (`NFR-05`).
  - *Technique*: Concurrent request probes, tampered-signature webhook rejection tests, and multi-version supersession checks.
  - *Completion Criteria*: All performance, cryptographic, and immutability assertions pass with zero regressions.
- **User Interface, Localization and Regression Testing**:
  - *Objective*: Verify responsive web and mobile behaviour, English/Vietnamese localization, light/dark theme persistence, and zero regression across schema or feature changes.
  - *Technique*: Component and widget rendering tests in Vitest and Flutter Test, `Accept-Language` negotiation tests, and repeated full-suite regression runs.
  - *Completion Criteria*: All web, mobile, and backend localization and regression suites pass.

### 2.2 Test Levels

The project executes four sequential test levels:

- **Unit Level**: Verifies isolated domain entities, value objects, services, cryptographic helpers, React components and hooks, and Flutter widgets and repositories with in-memory substitutes.
- **Integration Level**: Verifies module boundaries, Flyway migrations and the 41-table inventory, JPA repositories, MockMvc security filter chains, MinIO adapters, and the payment and AI client adapters against containerized PostgreSQL and S3-compatible services.
- **System Level**: Verifies end-to-end multi-role business flows, cross-module domain events, and non-functional thresholds across the integrated stack.
- **Acceptance Level**: Verifies business rules and user requirements across the eight features against the SRS acceptance criteria.

| Type of Tests | Unit | Integration | System | Acceptance |
| --- | :---: | :---: | :---: | :---: |
| Functional and Business Rule Testing | X | X | X | X |
| Domain State Machine Transition Testing | X | X | X | X |
| API and Database Persistence Testing |  | X | X |  |
| Security and Scope Isolation Testing | X | X | X | X |
| AI Vision, Narrative Drafting and Fallback Testing | X | X | X | X |
| Performance, Payment Webhook and PDF Integrity Testing |  | X | X | X |
| User Interface, Localization and Regression Testing | X | X | X | X |

### 2.3 Supporting Tools

The following tools are used for test authoring, execution, coverage measurement, and report generation.

| Purpose | Tool | Vendor/In-house | Version |
| --- | --- | --- | --- |
| Backend unit and integration testing | JUnit Jupiter, Spring Boot Test, MockMvc | Open Source (Eclipse Foundation) / Broadcom | `JUnit 6.x` / `Spring Boot 4.1.0` |
| Containerized database and object-storage harness | Testcontainers (`pgvector:pg17`, `adobe/s3mock`) | AtomicJar / Docker | `1.20.x` / `PostgreSQL 17` |
| Architectural boundary verification | Spring Modulith Test | Broadcom | `2.1.1` |
| Backend coverage measurement | JaCoCo Maven Plugin | EclEmma | `0.8.13` |
| Frontend component and unit testing | Vitest, React Testing Library, JSDOM | Open Source (Vite / Testing Library) | `5.0.1` / `16.3.3` |
| Mobile widget and repository testing | Flutter Test, Dart Analyzer | Google | `Dart 3.x` / `Flutter 3.x` |
| Report workbook generation and verification | Custom Python OOXML exporter and unittest suite | In-house (`SmartDroneInspection-docs/tools`) | `Python 3.12+` |

---

## 3. Test Plan

### 3.1 Human Resources

The table below lists the project members and supervisors involved in test design, execution, and review.

| Worker/Doer | Role | Specific Responsibilities/Comments |
| --- | --- | --- |
| **Trần Hoàng Trung Hiếu** | Project Leader and Tester (`MF1`: `FE-01`, `FE-02` owner) | Owns the test cases and regression runs for `Feature 1` (customer registration, sign-in, account access, and four-role authorization) and `Feature 2` (partner application and admission, building assets, and Inspector-owned drone registration). |
| **Phùng Trung Quốc** | Backend and Mobile Engineer and Tester (`MF2`: `FE-03`, `FE-04` owner) | Owns the test cases and regression runs for `Feature 3` (buildings, airspace screening, recurring requests, and notifications) and `Feature 4` (service requests, VND quotations, agreements, and dispatch). |
| **Trần Tùng Bách** | Full-Stack and AI Engineer and Tester (`MF3`/`MF4`: `FE-05`, `FE-06`, `FE-07` owner) | Owns the test cases and regression runs for `Feature 5` (flight permit gate, field sessions, telemetry), `Feature 6` (evidence intake and YOLO11 detection), and `Feature 7` (report preparation, review, and publication). |
| **Trương Thái Như** | Full-Stack Engineer and Tester (`MF4`: `FE-08` owner) | Owns the test cases and regression runs for `Feature 8` (customer acceptance, PayOS and VNPay settlement, and partner payouts), and supports cross-feature regression, environment provisioning, and workbook reconciliation. |
| **Supervisors** | Reviewers | Review the test strategy, audit traceability across Reports 3–5, and evaluate defence readiness. |

### 3.2 Test Environment

The software, hardware, and infrastructure used to execute the suites are listed below.

| Purpose | Tool | Provider | Version |
| --- | --- | --- | --- |
| Application runtime and API host | Java 21 JRE with Spring Boot Modulith | Eclipse Temurin / Broadcom | `Java 21` / `Spring Boot 4.1.0` |
| Relational database | PostgreSQL (41 tables, Flyway `V1` + `V2`) | PostgreSQL Global Development Group | `17` |
| Object storage | S3-compatible MinIO (`inspection-evidence` bucket) | MinIO Inc. | `RELEASE.2025` |
| Test database and storage containers | Testcontainers with `pgvector:pg17` and `adobe/s3mock` | AtomicJar / Docker | `PostgreSQL 17` |
| Computer vision service | FastAPI with Ultralytics YOLO11s (`MBDD2025`) | Python / Ultralytics | `Python 3.x` / `YOLO11s` |
| Web client under test | Google Chrome and Microsoft Edge (desktop) | Google / Microsoft | Evergreen |
| Mobile client under test | Flutter test runner and Android client | Google | `Flutter 3.x` / `API 34` |
| Operating system for local execution | Windows 11 with Git Bash | Microsoft | `10.0.26200` |

### 3.3 Test Milestones

Testing activities are scheduled across five milestones aligned with the iterative build plan.

| Milestone Task | Start Date | End Date |
| --- | --- | --- |
| Milestone 1: Unit and migration foundation gate — schema baseline, authentication, authorization, Modulith boundaries | `2026-09-15` | `2026-10-08` |
| Milestone 2: Core inspection, MinIO evidence, YOLO11 detection and PDF reporting integration testing | `2026-10-09` | `2026-10-22` |
| Milestone 3: Review 2 baseline and maintenance-scope retirement verification (Round 1 execution) | `2026-10-23` | `2026-10-27` |
| Milestone 4: Four-role, eight-feature consolidation across `MF1`–`MF4` — consolidated `V1` baseline, contracts, PayOS/VNPay, re-inspection (Rounds 2 and 3) | `2026-10-28` | `2026-11-04` |
| Milestone 5: Final regression, staging walkthrough and defence rehearsal across `Feature 1`–`Feature 8` | `2026-11-05` | `2026-11-30` |

---

## 4. Test Cases

The project's test cases are organized into two complementary deliverables.

- **Unit Test Cases (repository test suites)**:
  - **Backend (`SmartDroneInspection-backend/src/test/java`)**: JUnit Jupiter test classes verifying domain state transitions, service logic, cryptographic verification, and architecture and schema contracts. Notable classes include `AssetTest`, `DroneTest`, `ServiceRequestTest`, `FindingTest`, `InspectionReportTest`, `ContractWorkflowServiceTest`, `InspectorApplicationServiceTest`, `InspectorProfileServiceTest`, `EvidenceServiceTest`, `PayOSCryptoTest`, `VnPayCryptoTest`, `PasswordPolicyTest`, `ModulithArchitectureTest`, `FullDatabaseSchemaMigrationTest`, `RuntimePersistenceInventoryTest`, and `ConnectedMainFlowE2eIntegrationTest`.
  - **Frontend (`SmartDroneInspection-frontend/src`)**: Vitest and React Testing Library files verifying the four-portal route guards (`accessPolicy.test.ts`, `router.test.ts`), the airspace map, the schedule calendar, and the evidence, findings, and report workflows.
  - **Mobile (`SmartDroneInspection-mobile/test`)**: Flutter test files verifying customer-only session admission, localization, and the customer screens.
- **Other Test Cases — Integration, System, and Acceptance Testing (`Report5_Test Report.xlsx`)**:
  - Contains the functional cases partitioned across eight feature sheets (`Feature 1` through `Feature 8`, mapped one-to-one to `FE-01` through `FE-08`), with columns for the procedure, expected results, preconditions, three execution rounds, the test date, the tester, and a note recording the mode and the automated evidence.
  - `Feature 1` (`FE-01`) covers customer airspace registration, sign-in, one-time-code verification, session rotation, the account profile, and the four-role access matrix.
  - `Feature 2` (`FE-02`) covers partner application admission, Inspector licence records and flight logs, and Inspector-owned drone registration and approval.
  - `Feature 3` (`FE-03`) covers the building asset registry with its No-Fly Zone guard, restricted-airspace customer review, recurring occurrence materialization, month-end anchoring, recurrence bounds, and deduplicated outbox notifications.
  - `Feature 4` (`FE-04`) covers service requests, VND quotations, order chat, signed-agreement upload, cross-organization dispatch, abort re-dispatch, and the airspace map.
  - `Feature 5` (`FE-05`) covers the flight-permit gate with independent verification, field-session start, completion and abort, telemetry and trace sync, the dashboards, and the calendar.
  - `Feature 6` (`FE-06`) covers photo and video evidence intake, YOLO11 detection with vision fallback, and findings confirmation.
  - `Feature 7` (`FE-07`) covers the four-state report lifecycle, tab-visit report compilation, advisory narrative drafting, independent Manager review, and publication with PDF rendering.
  - `Feature 8` (`FE-08`) covers customer report acceptance, PayOS and VNPay settlement, the re-inspection loop, and partner payout and refund settlement.

---

## 5. Test Reports

**Test Results and Statistics Summary**

Execution results are recorded in `Report5_Test Report.xlsx` (`Test Statistics` and `Feature 1`–`Feature 8`) and in the automated suite runs cited below.

| Suite | Scope | Result |
| --- | --- | --- |
| Backend (`./mvnw test`) | Domain and integration tests, including Modulith boundary and schema-migration assertions | `119` test classes, `627` tests: `627` passed, `0` failed, `0` errors, `0` skipped. JaCoCo line coverage `72.2%` (`13,586 / 18,805`), branch coverage `51.9%` (`4,735 / 9,123`). |
| Frontend (`npm test -- --run`) | Component, page, access-policy and API-client tests | `89` test files (`85` passed, `4` skipped), `627` tests (`623` passed, `4` skipped), `0` failed. |
| Mobile (`flutter test`) | Customer-only session, localization and screen tests | `42` cases in `13` files; all passed |

**Relevant Test Analysis**

1. **Functional and Main Workflow Readiness**: The connected lifecycle is exercised end-to-end by `ConnectedMainFlowE2eIntegrationTest`, which drives onboarding, building and drone registration, service request, quotation and occurrence dispatch, evidence and detection, report publication, and settlement within one integration run.
2. **Schema and Boundary Discipline**: `FullDatabaseSchemaMigrationTest` asserts that the applied migration set is exactly `["1","2"]`, and `RuntimePersistenceInventoryTest` and `PersistenceEntityMappingTest` verify the 41-table inventory and the entity-to-column mapping. `ModulithArchitectureTest` asserts that no module reaches another outside its declared `allowedDependencies`.
3. **Authorization Coverage**: `RolePolicyTest`, `Mf2ActorPolicyTest`, and `ReportServiceReviewerScopeTest` verify separation of duties — a report author cannot review or publish their own report and a permit uploader cannot verify their own permit — while the frontend `accessPolicy.test.ts` and `router.test.ts` verify that a denied section has no route for that role.
4. **Known Defects**: Two defects remain open and are recorded rather than omitted. First, `SmartDroneInspection-mobile/lib/features/auth/domain/models/user_role.dart` still enumerates and parses the retired `MAINTENANCE_ENGINEER` role; the behaviour is harmless because the session gate admits `CUSTOMER` only, but the stale enum member should be removed. Second, `SmartDroneInspection-backend/e2e/scripts/run-e2e.mjs` resolves its frontend root to a directory that does not exist in the workspace, so the E2E runner cannot execute as written. Neither defect affects a delivered feature path, and neither is reported as passing.

**Execution note**

The pass and count figures above are taken from the runs executed while preparing this revision. Cases that were not executed in that run remain `Pending` in the workbook and are not claimed as passing.
