---
title: "Report 5 - Software Test Documentation"
document_type: report5-doc-section
weight: 15
source: "Report5_Test Documentation.docx"
---

# II. Testing Documentation

## 1. Scope of Testing

**Features and Functions to be Tested (`FE-01` to `FE-24`)**

Testing covers the delivered SmartDroneInspection platform across the Web Portal (`SmartDroneInspection-frontend`), the Customer Mobile Application (`SmartDroneInspection-mobile`, Customer parity delivered in `PR #27`–`PR #28`), the Spring Boot 4.1 Modulith backend (`SmartDroneInspection-backend`, Flyway `V1__baseline.sql`, `V2__remove_finding_recommended_action.sql`, `V3__reinspection_resolved_validity.sql`, `V4__payment_due_expiry.sql`, `V60__quote_partner_assignment_optional.sql`, `V61__inspection_chat_and_dispatch_settings.sql`, `V62__inspection_knowledge_rag.sql`, `V63__ai_auto_confirm_default_70.sql`, `V64__backfill_published_historical_cases.sql`, `V65__rag_local_embeddings_384.sql`, `V66__asset_ownership_information.sql`, `V67__gateway_order_created_at.sql`, `V68__gateway_inbound_transactions.sql`, and `V69__split_inspection_flight_permits_and_field_session_telemetry.sql` — applied set `["1","2","3","4","60","61","62","63","64","65","66","67","68","69"]`, `48` application tables, `47` JPA runtime entity tables, `50` total tables in the `public` schema), and the AI, telemetry, and payment integrations across twenty-four atomic product features (`FE-01`–`FE-24`, organized across main flows `MF1`–`MF4`) and the business rules `BR-01`–`BR-55`. The inspection scope is buildings only.

- **`FE-01` Account Authentication, OTP & 4-Role Access Control** *(MF1)*: Customer organization and initial building registration (`ProspectiveCustomerRegistration`), memory-hard password sign-in, consolidated one-time-code verification (`LOGIN`, `REGISTRATION`, `PASSWORD_RESET`), Google OAuth 2.0 (web callback and mobile deep link), JWT access tokens with refresh-token rotation (`AuthSession`), `/api/v1/users/me` profile update, CSRF and IP rate limiting (`AuthRateLimitFilter`), bilingual localization, dark/light theme persistence, and four-role route-level and API-level authorization (`accessPolicy.ts`, `@PreAuthorize`).
- **`FE-02` Partner Inspector Application & Qualification Management** *(MF1)*: Public partner Inspector application with licence scan, review and account provisioning (`InspectorApplicationController`), non-disclosing email checks, pilot licence profiles (`inspector_profiles`) and flight logs (`inspector_flight_logs`), and qualification validity checks at planned flight start.
- **`FE-03` Inspector-Owned Drone Registration & Fleet Management** *(MF1)*: Admin-configured drone document/feature checklists (`drone_document_configs`, `drone_feature_configs`), Inspector-owned drone registration with photos and required documents (`DroneRegistrationApplicationController`), Manager approval into `drones`, registration expiry eligibility checks, and `ACTIVE <-> IN_MAINTENANCE -> RETIRED` serviceability transitions.
- **`FE-04` Interactive Location Map & No-Fly Zone Airspace Screening** *(MF1)*: `AirspaceAdvisoryService`, Web `AirspaceNoFlyMap`, and Mobile `AirspaceAdvisoryCard` coordinate evaluation (`NO_FLY_ZONE`, `RESTRICTED_ZONE`, `CLEAR_ZONE`), out-of-bounds coordinate validation, and hard No-Fly Zone registration blocking.
- **`FE-05` Financial History & Revenue/Payment Ledger** *(MF4)*: Organization-scoped Customer payment history ledger, Inspector earnings history ledger, and Platform Manager revenue ledger queries across `/client`, `/operations`, and `/manager` finance tabs.
- **`FE-06` Building Asset Registry, Checkpoints & Reference Documents** *(MF2)*: Building asset catalogue with plain-text ownership description (`assets.ownership_information`, `V66`) alongside `technical_profile jsonb`, `inspection_items` checkpoints, SHA-256 reference documents in MinIO, duplicate-checksum guards, and `ACTIVE -> RETIRED` terminal locking.
- **`FE-07` Restricted Airspace Review & Clearance Decision** *(MF2)*: Platform `ADMIN`/`MANAGER` review queue for restricted-airspace `prospective_customer_registrations` (`AirspaceReviewController`), mandatory rejection remarks, and audited organization/asset activation.
- **`FE-08` Service Requests (One-Time & Recurring) & VND Quotations** *(MF2)*: Minimal compact one-time and recurring requests with concise generated recurring titles (`SmartDroneInspection-backend PR #164`, `SmartDroneInspection-frontend PR #139`), monthly cadence bounds (2–100 occurrences, 20-calendar-day lead time), month-end date anchoring, request-level Manager claim, and versioned VND quotations with immutable accepted snapshots and optional partner nomination.
- **`FE-09` Offline Signed Contract & Occurrence Dispatch Scheduling** *(MF2)*: Signed paper contract upload and streaming, recurring `ServiceRequestOccurrence` materialization, cross-organization schedule-conflict guards (`hasScheduleConflict`), qualification validity checks across all materialized dates, abort recovery dispatch (`reschedule`/`reassign`/`cancel`), and Customer Mobile field walkthrough parity.
- **`FE-10` Dual-Channel Messaging (Order Chat & Inspection Chat)** *(MF2)*: Dedicated Customer–Manager commercial order chat and separated Customer–Inspector per-inspection chat (`inspection_messages`, `inspection_message_attachments`), up to five attachments (10 MiB each / 20 MiB total), authenticated image preview/download, ADMIN chat read exclusion, and Customer Mobile `Inspector` inbox parity.
- **`FE-11` Assignment Acceptance Timeout & Escalation Handling** *(MF2)*: Admin-configurable Step 4 assignment acceptance timeout (`platform_operations_settings`, default 24 hours) monitored by `InspectionAssignmentTimeoutMonitor`, automatically cancelling unaccepted assignments, notifying the owning Manager, and reverting the occurrence to `PENDING_ASSIGNMENT`.
- **`FE-12` System Notifications & Alert Center** *(MF2)*: Deduplicated in-app notifications (`uq_notifications_deduplication_key`) published asynchronously via Spring Modulith transactional domain events (`event_publication`), idempotent `SENT -> READ` acknowledgement, and deep-link `targetPath` sanitization.
- **`FE-13` Flight Permit Upload & Independent Verification Gate** *(MF3)*: Mission flight-permit upload with magic-byte, SHA-256, drone serial and validity-window checks, mandatory independent Manager/Admin review (`PENDING_REVIEW -> APPROVED/REJECTED`) blocking self-review, reschedule/reassignment permit reset, and hard pre-session permit gate.
- **`FE-14` On-Site Field Session & SmartDroneHub MAVLink Telemetry** *(MF3)*: Field session lifecycle (`Start -> Complete / Abort`), mission reopen on abort, `SmartDroneHub` MAVLink trace persistence (`flight_trace_json`), non-MAVLink SRT/CSV/KML/GPX log import with accountable manual declaration, four-role KPI dashboard, and `InspectorScheduleCalendar`.
- **`FE-15` Field Evidence Intake & Chunked Video Processing Pipeline** *(MF3)*: Photo intake (`<= 10 MB`, EXIF extraction prior to `<= 2048 px` upright normalization and `480 px` JPEG thumbnails), duplicate-filename auto-numbering, resumable `OPEN -> COMPLETING -> PROCESSING` chunked MP4 uploads up to `2 GiB`, async FFmpeg `<= 1080p` faststart + poster normalization with raw retention, and short-lived HMAC media tickets with HTTP Range (`206`/`416`) playback.
- **`FE-16` AI Defect Detection (`YOLO11` + Vision Fallback) & Findings Confirmation** *(MF3)*: FastAPI `YOLO11` (`MBDD2025`) photo/video detection (`70%` default auto-confirm threshold per `V63`), `PrimaryWithFallbackInference` Vision fallback on empty/unreachable results, explicit `?replace=true` re-analysis, confirmation status filter chips (`All active`, `Unconfirmed`, `Confirmed`), Inspector-only baseline confirmation, source lock during report review, and fresh field-session gating for `RESOLVED` re-inspection evidence.
- **`FE-17` AI Case/Standard Retrieval (`pgvector` RAG), Note Drafting & Report Summary** *(MF3)*: Tenant-isolated `DroneKnowledgeAI` recommendation lookup (`inspection_knowledge_chunks`, `historical_finding_cases` backfilled in `V64`), local `fastembed` `vector(384)` cosine retrieval (`V65`) with `HYBRID_MATCH` fallback, per-finding and batch AI note drafting (`Draft note with AI` / `Draft all notes`), Customer Mobile `KnowledgeReferencesStrip`, and `ReportAiSummaryCard` executive summary drafting with `Matched Cases & Standards`.
- **`FE-18` Inspection Report Compilation, Independent Review & Official Publication** *(MF4)*: Four-state report lifecycle (`SUBMITTED`, `RETURNED`, `PUBLISHED`, `SUPERSEDED`), tab-visit auto-compiled report content, independent Manager review banning self-publication, on-demand A4 PDF generation without loading raw video bytes into memory, immutable version supersession, and server-paged role-scoped `/with-reports` queues.
- **`FE-19` Customer Report Acceptance & Clarification Workflow** *(MF4)*: Customer report review, formal acceptance (`ACCEPTED`), and clarification request workflow gating commercial invoicing and live staging report handoff.
- **`FE-20` Online Service Fee Payment (`Sepay` VietQR & `VNPay`)** *(MF4)*: Normalized `V29` finance tables (`service_invoices`, `service_payments`, `inspector_payouts`) plus `V67` (`gateway_order_created_at`) and `V68` (`gateway_inbound_transactions`), Sepay VietQR (`Authorization: Apikey` constant-time SHA-256 verification, receiving-account check, idempotent webhook audit trail, and 3-second auto-close QR polling) and VNPay v2.1.0 (HMAC-SHA512 checkout/Return/IPN verification, automatic order release on cancel/expiry, and direct `/settlement` return), whole-VND validation, and role-masked nested financial projections (`forCustomer`, `forInspector` with `inspectorRefundSummaries`, `forManager`).
- **`FE-21` Payment Deadlines, Invoices & Payment Document Management** *(MF4)*: Acceptance-stamped `payment_due_at` deadline (`app.payment-due.due-window`, default 15 days), daily `PaymentDueExpiryService` single overdue reminder without access revocation, and role-scoped `GET /api/v1/inspections/{id}/report/payment-document` notice/receipt PDF downloads.
- **`FE-22` Partner Inspector Payout Reconciliation** *(MF4)*: Platform Manager payout ledger generation (`ELIGIBLE -> PAID`), manual bank transfer reference reconciliation, idempotent duplicate-payout guard, and payout cap enforcement against captured occurrence revenue and active refund holds.
- **`FE-23` Evidence-Backed Refunds & Receivable Recovery** *(MF4)*: Refund initiation holding unpaid partner payouts, evidence-backed transfer completion and exact allocation, legacy refund-by-ID reconciliation, post-payout Inspector receivable creation and manual recovery without auto-offsetting future payouts, and cumulative refund caps.
- **`FE-24` Post-Remediation Re-inspection & Defect Verification** *(MF4)*: Follow-up re-inspection opening against a published report, three-way defect verification verdicts (`RESOLVED`, `UNRESOLVED`, `INCONCLUSIVE`), `RESOLVED` verdict expiry tracking (`VerdictExpiryBanner` / Mobile `verdict_expiry.dart`), and end-to-end WF-03/Customer Mobile verification parity (`PR #27`).

**Non-Functional Requirements to be Tested (`NFR-01` to `NFR-08`)**

- **`NFR-01` (Performance — User Response Time)**: Standard user actions, searches, and paged list views reach `p95 <= 2.0 s` with `0%` server errors under `50` concurrent users.
- **`NFR-02` (Performance — Detection Latency)**: A single-image defect suggestion completes within `<= 5.0 s` for supported inputs, and detection falls back to the secondary provider or to manual entry when the primary service is unavailable.
- **`NFR-03` (Security — Role, Organization and Assignment Isolation)**: `100%` of unauthorized or cross-scope requests are blocked and `0` cross-organization disclosures occur.
- **`NFR-04` (Security — Sign-In Resistance and Access Revocation)**: Sign-in is restricted for `15 minutes` after `5` failures, more than `10` sign-in requests per minute per address are blocked, and a revoked session cannot continue to be used.
- **`NFR-05` (Reliability — Record Integrity)**: Signed documents, building documents, and published reports keep `100%` integrity and `100%` of unauthorized in-place changes are prevented.
- **`NFR-06` (Reliability — Upload Resilience)**: `100%` of interrupted video uploads are resumable and `100%` of failed transcodes retain their source for an explicit retry.
- **`NFR-07` (Maintainability — Verification Coverage and Module Boundaries)**: All twenty-four features (`FE-01`–`FE-24`) have applicable verification cases and `0` module boundary violations occur.
- **`NFR-08` (Portability — Rebuild and Migration Set)**: The service starts from the compose stack with the migration set exactly `["1","2","3","4","60","61","62","63","64","65","66","67","68","69"]` — the declared baseline plus forward migrations — and the 48-application-table inventory (47 JPA runtime entities, 50 total tables).

**Items Not to be Tested (Out of Scope)**

- Physical unmanned-aircraft control, flight-controller firmware, radio-link operation, and physical structural repair work. The platform records governance and evidence; it does not fly the aircraft.
- Corrective maintenance execution and its knowledge corpus: work orders, repair-scope advisory over `repair_knowledge_chunks`, repair execution, completion reporting, and cost close-out. No such code, schema, or login role (`MAINTENANCE_ENGINEER`) is in the delivered product. The platform does provide a re-inspection loop against a published report, which is tested under `FE-24`.
- Non-building infrastructure domains — bridges, transmission towers, solar farms, roads, dams, tunnels, ports, and pipelines.
- Retrieval-augmented advisory over the *corrective-maintenance* `repair_knowledge_chunks` corpus. In contrast, the delivered `DroneKnowledgeAI` retrieval and note drafting over `inspection_knowledge_chunks` (seeded engineering standards `TCVN 9343:2012`, `TCVN 9361:2012`, `EN 1504-9`, `ISO 12944-5`, `ASTM C1583`) and `historical_finding_cases` (anonymized benchmarks plus published tenant-private findings) IS in scope and tested under `FE-17`/`FE-18` by `HistoricalCaseServiceTest`, `HistoricalCaseApiIntegrationTest`, the Web `InspectionFindingsPage.test.tsx` / `KnowledgeRecommendationPanel.test.tsx` / `ReportAiSummaryCard.test.tsx` tests, the live `PGVECTOR_RAG` & `AI_VISION_RAG` checks, and the Mobile `knowledge_recommendation_test.dart`. Every recommendation and drafted note is advisory and never exposes another organization's data.
- Native mobile push delivery through APNs or FCM, and commercial SMTP relay infrastructure. In-app notifications and one-time codes are verified through the application API and database.
- Internal banking core systems behind Sepay VietQR and VNPay, beyond signed checkout generation, VietQR composition, and webhook/IPN verification.
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
  - *Focuses*: Schema migration integrity and the exact applied migration set, ownership and assignment foreign keys, authorization at the API boundary, event-outbox delivery, object streaming, and versioned report publication.
  - *Acceptance Criteria*: `0` Spring Modulith boundary violations, the `48`-application-table inventory (`47` JPA runtime entities, `50` total tables) and the `["1","2","3","4","60","61","62","63","64","65","66","67","68","69"]` migration set verified, and `100%` of integration tests passing.
- **System Testing**:
  - *In-charge*: The full engineering team.
  - *Inputs / Time*: The complete multi-container system — backend, frontend, mobile client, PostgreSQL 17, MinIO, the YOLO11 inference service, SmartDroneHub, and the payment webhooks — against the SRS and SDD.
  - *Focuses*: End-to-end connected flows through `ConnectedMainFlowE2eIntegrationTest`, cross-client consistency between the web and mobile clients, and the quantified non-functional thresholds.
  - *Acceptance Criteria*: The connected `MF1` → `MF2` → `MF3` → `MF4` lifecycle executes end-to-end without error and the applicable NFR targets hold.
- **Acceptance Testing**:
  - *In-charge*: All team members, under supervisor review.
  - *Inputs / Time*: Report 3 SRS (`FE-01`–`FE-24`, `BR-01`–`BR-55`) and the functional case workbooks.
  - *Focuses*: Business acceptance rules, separation of duties, and staging walkthroughs.
  - *Acceptance Criteria*: The documented pass rate across `Feature 1`–`Feature 24` with `0` open Critical or High severity defects.

**Constraints and Assumptions**

- **Containerized infrastructure**: Database and object-storage integration tests require a running Docker daemon to provision the PostgreSQL and S3-compatible Testcontainers instances.
- **External AI and telemetry availability**: When the inference container or the language-model gateway is unreachable, the system routes to the vision fallback and to deterministic report compilation so that business workflows remain testable.
- **Payment sandbox**: Payment verification uses deterministic HMAC test credentials and signed webhook payloads rather than live bank debits.
- **Aviation boundary**: Flight permits, airspace evaluations, and telemetry traces are software governance records. Physical flight safety remains the responsibility of the licensed human pilot, and no test claims governmental clearance.

---

## 2. Test Strategy

This section defines the testing types, the four test levels at which they are executed, and the supporting tools used to verify functional and non-functional quality.

### 2.1 Testing Types

- **Functional and Business Rule Testing**:
  - *Objective*: Verify that every feature (`FE-01`–`FE-24`) and business rule (`BR-01`–`BR-55`) behaves according to the SRS and API contracts.
  - *Technique*: Equivalence partitioning, boundary-value analysis (10 MB photo and document limits, 2 GB resumable video with 10 MiB chunks, latitude and longitude ranges, 0–100% finance rates, 20-calendar-day scheduling lead time, 2–100 occurrence bounds, 1–120 month intervals), and positive and negative API and UI scenarios.
  - *Completion Criteria*: Complete functional coverage across `Feature 1`–`Feature 24` with the automated suites passing.
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
- **Performance, Payment Webhook and Report Integrity Testing**:
  - *Objective*: Validate response latency (`NFR-01`), Sepay `Authorization: Apikey` webhook verification & idempotent audit logging (`gateway_inbound_transactions`), VNPay v2.1.0 HMAC-SHA512 Return/IPN verification, and published-report immutability (`NFR-05`).
  - *Technique*: Concurrent request probes, tampered-signature webhook rejection tests, and multi-version supersession checks.
  - *Completion Criteria*: All performance, cryptographic, and immutability assertions pass with zero regressions.
- **User Interface, Localization and Regression Testing**:
  - *Objective*: Verify responsive web and mobile behaviour, English/Vietnamese localization, light/dark theme persistence, and zero regression across schema or feature changes.
  - *Technique*: Component and widget rendering tests in Vitest and Flutter Test, `Accept-Language` negotiation tests, and repeated full-suite regression runs.
  - *Completion Criteria*: All web, mobile, and backend localization and regression suites pass.

### 2.2 Test Levels

The project executes four sequential test levels:

- **Unit Level**: Verifies isolated domain entities, value objects, services, cryptographic helpers, React components and hooks, and Flutter widgets and repositories with in-memory substitutes.
- **Integration Level**: Verifies module boundaries, Flyway migrations (`V1`–`V4`, `V60`–`V69`) and the 48-application-table inventory (47 JPA runtime entities, 50 total tables), JPA repositories, MockMvc security filter chains, MinIO adapters, and the payment, AI-vision and DroneKnowledgeAI client adapters against containerized PostgreSQL and S3-compatible services.
- **System Level**: Verifies end-to-end multi-role business flows, cross-module domain events, and non-functional thresholds across the integrated stack.
- **Acceptance Level**: Verifies business rules and user requirements across all twenty-four features (`FE-01`–`FE-24`) against the SRS acceptance criteria.

| Type of Tests | Unit | Integration | System | Acceptance |
| --- | :---: | :---: | :---: | :---: |
| Functional and Business Rule Testing | X | X | X | X |
| Domain State Machine Transition Testing | X | X | X | X |
| API and Database Persistence Testing |  | X | X |  |
| Security and Scope Isolation Testing | X | X | X | X |
| AI Vision, Narrative Drafting and Fallback Testing | X | X | X | X |
| Performance, Payment Webhook and Report Integrity Testing |  | X | X | X |
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
| **Trần Hoàng Trung Hiếu** | Project Leader and Tester (`FE-01`–`FE-05`) | Owns the test cases and regression runs for `Feature 1` (`FE-01` authentication, OTP, Google OAuth2 & 4-role access), `Feature 2` (`FE-02` partner Inspector application & qualifications), `Feature 3` (`FE-03` Inspector-owned drone registration & fleet lifecycle), `Feature 4` (`FE-04` interactive location map & NFZ screening), and `Feature 5` (`FE-05` financial history & ledger views), plus Customer Mobile co-testing and team coordination. |
| **Phùng Trung Quốc** | Backend and Mobile Engineer and Tester (`FE-06`–`FE-12`) | Owns the test cases and regression runs for `Feature 6` (`FE-06` building assets, `V66` ownership info, checkpoints & MinIO docs), `Feature 7` (`FE-07` restricted-airspace clearance review), `Feature 8` (`FE-08` one-time/recurring requests & VND quotations), `Feature 9` (`FE-09` signed contracts & occurrence dispatch), `Feature 10` (`FE-10` Order Chat & Inspection Chat), `Feature 11` (`FE-11` assignment acceptance timeout & escalation), and `Feature 12` (`FE-12` system notifications). |
| **Trần Tùng Bách** | Full-Stack and AI Engineer and Tester (`FE-13`–`FE-18`) | Owns the test cases and regression runs for `Feature 13` (`FE-13` flight permit upload & verification gate), `Feature 14` (`FE-14` field sessions & SmartDroneHub MAVLink telemetry), `Feature 15` (`FE-15` photo/chunked-video intake & streaming), `Feature 16` (`FE-16` YOLO11 + vision fallback detection & confirmation), `Feature 17` (`FE-17` `DroneKnowledgeAI` RAG retrieval, note drafting & AI summary), and `Feature 18` (`FE-18` report compilation, independent review & publication), plus backend/DB architecture & Customer Mobile co-testing. |
| **Trương Thái Như** | Full-Stack Engineer and Tester (`FE-19`–`FE-24`) | Owns the test cases and regression runs for `Feature 19` (`FE-19` customer report acceptance & clarification), `Feature 20` (`FE-20` Sepay VietQR & VNPay v2.1.0 payment settlement), `Feature 21` (`FE-21` payment due deadlines, notices & receipt PDFs), `Feature 22` (`FE-22` partner Inspector payout reconciliation), `Feature 23` (`FE-23` evidence-backed refunds & receivable recovery), and `Feature 24` (`FE-24` post-remediation re-inspection & verdict verification), plus automated test reconciliation, `Report5_Test Report.xlsx` workbook maintenance, and docs standardization. |
| **Supervisors** | Reviewers | Review the test strategy, audit traceability across Reports 3–5, and evaluate defence readiness. |

### 3.2 Test Environment

The software, hardware, and infrastructure used to execute the suites are listed below.

| Purpose | Tool | Provider | Version |
| --- | --- | --- | --- |
| Application runtime and API host | Java 21 JRE with Spring Boot Modulith | Eclipse Temurin / Broadcom | `Java 21` / `Spring Boot 4.1.0` |
| Relational database | PostgreSQL (`pgvector:pg17`; Flyway `V1`–`V4`, `V60`–`V69`; 48 application tables / 47 JPA runtime entities / 50 total tables) | PostgreSQL Global Development Group | `17` |
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
| Milestone 2: Core inspection, MinIO evidence, YOLO11 detection and inspection report integration testing | `2026-10-09` | `2026-10-22` |
| Milestone 3: Review 2 baseline and maintenance-scope retirement verification (Round 1 execution) | `2026-10-23` | `2026-10-27` |
| Milestone 4: Four-role, multi-flow consolidation across `MF1`–`MF4` — consolidated `V1` baseline, contracts, PayOS/VNPay, re-inspection (Rounds 2 and 3) | `2026-10-28` | `2026-11-04` |
| Milestone 5: Final regression, 24-feature decomposition verification (`Feature 1`–`Feature 24`), staging walkthrough and defence rehearsal | `2026-11-05` | `2026-11-30` |

---

## 4. Test Cases

The project's test cases are organized into two complementary deliverables.

- **Unit Test Cases (repository test suites)**:
  - **Backend (`SmartDroneInspection-backend/src/test/java`)**: JUnit Jupiter test classes verifying domain state transitions, service logic, cryptographic verification, and architecture and schema contracts. Notable classes include `AssetTest`, `DroneTest`, `ServiceRequestTest`, `FindingTest`, `InspectionReportTest`, `ContractWorkflowServiceTest`, `InspectorApplicationServiceTest`, `InspectorProfileServiceTest`, `EvidenceServiceTest`, `SepayGatewayTest`, `SepayWebhookControllerTest`, `VnPayCryptoTest`, `VnPayWebhookAndGatewayTest`, `OccurrenceFinanceResponseTest`, `PasswordPolicyTest`, `ModulithArchitectureTest`, `FullDatabaseSchemaMigrationTest`, `RuntimePersistenceInventoryTest`, `HistoricalCaseServiceTest`, `HistoricalCaseApiIntegrationTest`, `PaymentDueExpiryServiceTest`, `PaymentDocumentServiceTest`, `ReinspectionWorkflowIntegrationTest`, and `ConnectedMainFlowE2eIntegrationTest`.
  - **Frontend (`SmartDroneInspection-frontend/src`)**: Vitest and React Testing Library files verifying the four-portal route guards (`accessPolicy.test.ts`, `router.test.ts`), the airspace map, the schedule calendar, the evidence, findings, and report workflows, and the `DroneKnowledgeAI` controls (`InspectionFindingsPage.test.tsx`, `KnowledgeRecommendationPanel.test.tsx`, `ReportAiSummaryCard.test.tsx`).
  - **Mobile (`SmartDroneInspection-mobile/test`)**: Flutter test files verifying customer-only session admission, localization, the customer screens, and `PR #27` parity (`knowledge_recommendation_test.dart`, `verdict_expiry_test.dart`, `inspection_customer_sync_test.dart`).
- **Other Test Cases — Integration, System, and Acceptance Testing (`Report5_Test Report.xlsx`)**:
  - Contains the `67` functional cases partitioned across twenty-four atomic feature sheets (`Feature 1` through `Feature 24`, mapped one-to-one to `FE-01` through `FE-24`), with columns for the procedure, expected results, preconditions, three execution rounds, the test date, the tester, and a note recording the mode and the automated evidence (`WF3-032`, `WF2-021`, and `WF3-033` are recorded honestly as `N/A / Pending / Pending` pending dedicated standalone UI/E2E walkthroughs).
  - `Feature 1` (`FE-01`) covers customer registration, sign-in, OTP verification, Google OAuth2, session rotation, profile self-service, bilingual/dark-mode UI, and the four-role access matrix.
  - `Feature 2` (`FE-02`) covers partner Inspector admission, non-disclosing email checks, pilot licence profiles, flight logs, and qualification expiry checks.
  - `Feature 3` (`FE-03`) covers Admin-configured drone document/feature checklists, Inspector-owned drone registration/renewal, photo requirements, and `ACTIVE <-> IN_MAINTENANCE -> RETIRED` serviceability transitions.
  - `Feature 4` (`FE-04`) covers `AirspaceAdvisoryService`, Web `AirspaceNoFlyMap`, Mobile `AirspaceAdvisoryCard`, coordinate range validation, and hard No-Fly Zone registration blocking.
  - `Feature 5` (`FE-05`) covers scoped financial history and revenue/payment ledger views across Customer, Inspector, and Manager portals (`WF3-032` unexecuted coverage placeholder).
  - `Feature 6` (`FE-06`) covers building asset registration (`assets.ownership_information` per `V66`), checkpoints, SHA-256 MinIO reference documents, duplicate guards, and retirement locking.
  - `Feature 7` (`FE-07`) covers platform review and auditable approval/rejection of restricted-airspace customer registrations.
  - `Feature 8` (`FE-08`) covers minimal compact one-time and recurring requests with concise generated recurring titles, monthly bounds/month-end anchoring, Manager claim, and versioned VND quotations.
  - `Feature 9` (`FE-09`) covers offline signed contract upload, recurring occurrence materialization, cross-org dispatch schedule-conflict guards, abort recovery dispatch, and Mobile walkthrough parity.
  - `Feature 10` (`FE-10`) covers separated Customer–Manager Order Chat and Customer–Inspector Inspection Chat with up to five private attachments and ADMIN read exclusion.
  - `Feature 11` (`FE-11`) covers Admin-configured Step 4 assignment acceptance timeout (`platform_operations_settings`) and automated escalation (`WF2-021` unexecuted standalone placeholder).
  - `Feature 12` (`FE-12`) covers event-driven deduplicated notifications (`uq_notifications_deduplication_key`), `event_publication` outbox delivery, idempotent read state, and deep-link sanitization.
  - `Feature 13` (`FE-13`) covers mission flight-permit upload, magic-byte/SHA-256/serial/window checks, independent Manager/Admin verification, reset on reschedule, and pre-session permit gate.
  - `Feature 14` (`FE-14`) covers on-site field session lifecycle (`Start -> Complete / Abort`), SmartDroneHub MAVLink traces, SRT/CSV/KML/GPX log import/declaration, 4-role KPI dashboards, and Inspector calendar.
  - `Feature 15` (`FE-15`) covers photo intake (`<= 2048 px` / EXIF / `480 px` thumb), duplicate auto-numbering, resumable `2 GiB` chunked MP4 uploads, async FFmpeg transcoding, and HMAC HTTP Range streaming.
  - `Feature 16` (`FE-16`) covers YOLO11 detection (`70%` threshold per `V63`), Vision fallback, `?replace=true`, status filter chips (`All active`/`Unconfirmed`/`Confirmed`), Inspector baseline confirmation, and fresh re-inspection evidence gating.
  - `Feature 17` (`FE-17`) covers tenant-isolated `DroneKnowledgeAI` recommendation lookup, local 384d `fastembed` retrieval (`V65`), historical case backfill (`V64`), single/batch AI note drafting, and `ReportAiSummaryCard` references.
  - `Feature 18` (`FE-18`) covers the four-state inspection report lifecycle, tab-visit auto-compilation, independent Manager review banning self-publication, on-demand PDF export, and role-scoped `/with-reports` queues.
  - `Feature 19` (`FE-19`) covers Customer report review, acceptance gating invoicing, clarification requests, and staging acceptance walkthroughs.
  - `Feature 20` (`FE-20`) covers normalized `V29` finance persistence plus `V67`–`V68`, Sepay VietQR and VNPay v2.1.0 checkout and webhook/IPN settlement verification, cancel/expiry order release, and role-masked finance projections.
  - `Feature 21` (`FE-21`) covers payment due window (`payment_due_at`), single daily overdue notification without access revocation, and scoped notice/receipt PDF downloads.
  - `Feature 22` (`FE-22`) covers Manager payout ledger generation (`ELIGIBLE -> PAID`), bank transfer reference reconciliation, idempotency, and payout caps (`WF3-033` unexecuted standalone placeholder).
  - `Feature 23` (`FE-23`) covers refund initiation payout holds, evidence-backed transfer completion and exact allocation, legacy refund reconciliation, and post-payout Inspector receivable recovery.
  - `Feature 24` (`FE-24`) covers follow-up re-inspection opening, three-way defect verification verdicts (`RESOLVED`, `UNRESOLVED`, `INCONCLUSIVE`), `RESOLVED` verdict expiry tracking, and Mobile parity.

---

## 5. Test Reports

**Test Results and Statistics Summary**

Execution results are recorded in `Report5_Test Report.xlsx` (`Test Statistics` and `Feature 1`–`Feature 24`) and in the automated suite runs cited below.

| Suite | Scope | Result |
| --- | --- | --- |
| Backend (`.\mvnw.cmd spotless:check` + `.\mvnw.cmd verify`) | Domain, integration, Modulith boundary, schema-migration, DroneKnowledgeAI and finance tests | `spotless:check` passed; `verify` exited `0` with **971 tests passing**, **0 failures**, Spring Modulith boundary verification passed, and JaCoCo coverage checks met (as recorded on 2026-11-20 prior to `PR #164`). |
| Frontend (`npm run lint` + `npm run build` + `npm test`) | Component, page, access-policy, DroneKnowledgeAI advisory and API-client tests | Full baseline (2026-11-20): `npm run lint` (`0` errors), `npm run build` exited `0`, `npm test` `97` files (`93` passed, `4` skipped), `724` tests (`720` passed, `4` skipped, `0` failed); post-`PR #140` focused auth/Vite verification: `npm run lint` (`0` errors), `npm run build`, `npx vitest run src/features/auth` (`11` files / `60` tests passed). |
| Mobile (`dart format --set-exit-if-changed .` + `flutter analyze` + `flutter test`) | Customer-only session, localization, screen and `PR #27`–`PR #28` parity tests | `85` files formatted with `0` changes; `flutter analyze` reported `No issues found!`; `flutter test` passed **56 tests, 0 failures** (including `knowledge_recommendation_test.dart`, `verdict_expiry_test.dart` and `inspection_customer_sync_test.dart`). |

**Relevant Test Analysis**

1. **Functional and Main Workflow Readiness**: The connected lifecycle is exercised end-to-end by `ConnectedMainFlowE2eIntegrationTest`, which drives onboarding, building and drone registration, service request, quotation and occurrence dispatch, evidence and detection, report publication, and settlement within one integration run.
2. **Schema and Boundary Discipline**: `FullDatabaseSchemaMigrationTest` asserts that the applied migration set is exactly `["1","2","3","4","60","61","62","63","64","65","66","67","68","69"]`, and `RuntimePersistenceInventoryTest` and `PersistenceEntityMappingTest` verify the 48-application-table inventory (47 JPA runtime entities, 50 total tables) and the entity-to-column mapping (including `assets.ownership_information` from `V66`, `service_payments.gateway_order_created_at` from `V67`, `gateway_inbound_transactions` from `V68`, and `inspection_flight_permits` + `field_session_telemetry` from `V69`). `ModulithArchitectureTest` asserts that no module reaches another outside its declared `allowedDependencies`. `HistoricalCaseApiIntegrationTest` additionally verifies tenant isolation: a caller cannot retrieve another organization's tenant-private finding case, while anonymized benchmark cases remain readable.
3. **Authorization Coverage**: `RolePolicyTest`, `Mf2ActorPolicyTest`, and `ReportServiceReviewerScopeTest` verify separation of duties — a report author cannot review or publish their own report and a permit uploader cannot verify their own permit — while the frontend `accessPolicy.test.ts` and `router.test.ts` verify that a denied section has no route for that role.
4. **Known Defects**: Two defects remain open and are recorded rather than omitted. First, `SmartDroneInspection-mobile/lib/features/auth/domain/models/user_role.dart` still enumerates and parses the retired `MAINTENANCE_ENGINEER` role; the behaviour is harmless because the session gate admits `CUSTOMER` only, but the stale enum member should be removed. Second, `SmartDroneInspection-backend/e2e/scripts/run-e2e.mjs` resolves its frontend root to a directory that does not exist in the workspace, so the E2E runner cannot execute as written. Neither defect affects a delivered feature path, and neither is reported as passing.
5. **Advisory AI Retrieval and Cross-Client Parity**: `HistoricalCaseServiceTest` and `HistoricalCaseApiIntegrationTest` verify tenant-isolated historical-case recommendation and AI note drafting over `inspection_knowledge_chunks` and `historical_finding_cases`, including `PGVECTOR_RAG` cosine retrieval via local `fastembed` `vector(384)` embeddings (`V65`), `AI_VISION_RAG`, the deterministic `HYBRID_MATCH` fallback with `[0.0, 1.0]` normalized similarity, `POST /api/v1/inspections/{inspectionId}/findings/{findingId}/draft-note`, `GET /api/v1/inspections/{inspectionId}/findings/{findingId}/recommendations` and `GET /api/v1/inspections/{inspectionId}/knowledge-recommendations`. On the Web portal, `DraftNoteAction` inside `EvidenceCaptureGroup.tsx` (`Draft note with AI` + collapsed `References`), batch `Draft all notes (N)`, `All active` / `Unconfirmed` / `Confirmed` confirmation status filter chips, and `ReportAiSummaryCard` replace the inline `Similar Cases & Guide` strip, while Customer Mobile `KnowledgeReferencesStrip` (`knowledge_recommendation_test.dart`), `verdict_expiry_test.dart`, and `inspection_customer_sync_test.dart` cover Mobile parity (`PR #27`–`PR #28`). All recommendations and drafted notes remain advisory and never override the human Inspector's confirmation or another organization's data isolation.

**Execution note**

The pass and count figures above are taken from the verified automated runs and workbook records (`45 Passed`, `0 Failed`, `9 Pending`, `13 N/A` in Round 1 across `67` cases; `13 Passed` in Round 3). Cases that were not executed in a given round (including the three newly broken-out standalone cases `WF3-032`, `WF2-021`, and `WF3-033`) remain `N/A` or `Pending` in the workbook and are not claimed as passing.
