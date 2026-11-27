---
title: "Report 5 - Software Test Documentation"
document_type: report5-doc-section
weight: 15
source: "Report5_Test Documentation.docx"
---

# II. Testing Documentation

## 1. Scope of Testing

This document defines the testing scope, strategy, plan, and execution results for SmartDroneInspection. Verification covers all 24 product features (`FE-01` to `FE-24`) across the Spring Boot backend, the React web portal, the Flutter Customer mobile application, and external integrations for artificial intelligence (AI), Micro Air Vehicle Link (MAVLink) telemetry, and online payments.

| Feature | Function | Role | Description |
| --- | --- | --- | --- |
| `FE-01` Identity and Access | Sign-up, Email One-Time Password (OTP), Sign-in, Password Reset, and Role-Based Access Control (RBAC) | All Roles | Verify registration, OTP expiry, JSON Web Token (JWT) issuance, password reset, and strict portal and Application Programming Interface (API) role isolation. |
| `FE-02` Partner Admission | Inspector Onboarding Application and Contract Review | Applicant, Manager | Verify multi-step pilot licence submission, signed partner contract upload, and Manager approval or rejection transitions. |
| `FE-03` Drone Fleet | Drone Registration, Specifications, Documents, and Expiry Tracking | Inspector, Manager, Admin | Verify aircraft registration, Maximum Take-Off Weight (MTOW) rules under Decree 288/2025/ND-CP, document verification, and expiry reminders. |
| `FE-04` Airspace Screening | Interactive Airspace Map and Zone Evaluation | All Roles | Verify prohibited no-fly blocking, restricted-zone warnings, and safe-zone confirmation against building coordinates. |
| `FE-05` Financial Ledger | Role-Scoped Payment, Payout, and Refund History | Customer, Manager, Inspector | Verify scoped transaction lists, status filters, and masking of platform margins and internal notes from Inspectors. |
| `FE-06` Building Assets | Building CRUD, Coordinates, Photos, and Inspection Items | Customer, Manager, Admin | Verify building registration, ownership isolation, checkpoint templates, and retirement guards on active inspections. |
| `FE-07` Restricted Airspace Policy | Restricted-Zone Warning and Permit Requirement Propagation | Customer, Manager, Inspector | Verify restricted-zone advisories surface during asset setup, quotation, dispatch, and flight permit checks. |
| `FE-08` Service Requests and Quotes | One-Time and Recurring Requests, VND Quotations, and Checkpoints | Customer, Manager | Verify 20-day lead-time rules, active-request duplicate guards, Vietnamese Dong (VND) quote calculations, and checkpoint locking after dispatch. |
| `FE-09` Contracts and Dispatch | Signed Agreement Upload, Crew Eligibility, and Cancellation | Customer, Manager | Verify immutable accepted terms, signed contract gate, licence-class and schedule conflict checks, and post-withdrawal cancellation. |
| `FE-10` Messaging | Order Chat, Partner Chat, and Inspection Chat | Customer, Manager, Inspector | Verify channel isolation, 10 MiB per-file and 20 MiB per-message attachment limits, and unread badge synchronization. |
| `FE-11` Assignment Acceptance | Inspector Acceptance, Decline, Pre-Field Withdrawal, and Timeout | Inspector, Manager | Verify pending-acceptance workflow, pre-field withdrawal flagging reassignment, post-abort withdrawal rejection, and timeout recovery. |
| `FE-12` Notifications | In-App Bilingual Feed and Critical Email Delivery | All Roles | Verify bilingual notification generation across all workflow events, mark-as-read state checks, and Simple Mail Transfer Protocol (SMTP) email fallbacks. |
| `FE-13` Flight Permits | Self-Attested Flight Permit Upload and Validity Resets | Inspector | Verify permit attachment moves status to `APPROVED` and drone change or out-of-window reschedule resets to `PENDING_REVIEW`. |
| `FE-14` Field Sessions and Telemetry | Multi-Flight Sessions, MAVLink Logs, and Abort Recovery | Inspector, Manager, Customer | Verify session start, telemetry ingestion, completion, and Customer visibility of stored flight logs only after report publication. |
| `FE-15` Evidence Pipeline | Image Upload, Chunked Video Upload, and Signed Media Tickets | Inspector, Manager, Customer | Verify upload validation, single-use scoped media tickets, and cross-customer access denial. |
| `FE-16` Defect Detection | YOLO11 Inference, Fallback Review, and Findings Confirmation | Inspector | Verify automated candidate detection, graceful fallback when AI is offline, manual bounding boxes, and findings baseline lock. |
| `FE-17` Knowledge Retrieval | DroneKnowledgeAI Retrieval-Augmented Generation (RAG) and Note Drafting | Inspector, Customer | Verify `pgvector` semantic search, keyword fallback, tenant isolation, and clean hiding of empty mobile reference strips. |
| `FE-18` Report Publication | Draft Authoring, Independent Manager Review, and Two-Step Publish | Inspector, Manager | Verify separation of duties (author cannot review), payout-before-publish gate, and read-only enforcement for Administrators. |
| `FE-19` Report Acceptance | Customer Deliverable Review, Acceptance, and Clarification | Customer, Manager | Verify Customer access gating until `PUBLISHED`, formal acceptance timestamping, and clarification request handling. |
| `FE-20` Online Settlement | Sepay VietQR and VNPay Checkout and Webhook Verification | Customer, Manager | Verify payment initiation, signature validation, idempotent webhook ledger persistence, and amount-mismatch rejection. |
| `FE-21` Payment Deadlines and Documents | Payment Due Date, Overdue Reminders, Notice and Receipt Portable Document Format (PDF) | Customer, Manager | Verify due-date assignment on acceptance, PDF generation states (`409` before acceptance, notice after acceptance, receipt after payment), and single overdue reminders. |
| `FE-22` Inspector Payouts | Partner Bank Details, Sepay Payout QR, and Settlement Confirmation | Manager, Inspector | Verify bank-account prerequisite checks, payout calculation, hold enforcement during refunds, and settlement confirmation. |
| `FE-23` Refunds and Receivables | Offline Refund Allocation and Post-Payout Inspector Receivables | Manager, Inspector | Verify five-way refund allocation balance, immutable paid payouts, receivable recovery tracking, and masked Inspector projections. |
| `FE-24` Post-Remediation Re-inspection | Linked Re-inspection Creation, Three-Way Verification, and Verdict Expiry | Customer, Manager, Inspector, Admin | Verify role guards, duplicate open re-inspection blocking (`REINSPECTION_ALREADY_OPEN`), fresh in-session evidence checks, report locks, and 14-day verdict expiry warnings. |

Chapter III, Section 3.8 of the Software Requirement Specification (SRS) defines out-of-scope boundaries, including corrective maintenance execution, live aircraft piloting, and 3D reconstruction. Payment tests run against sandbox credentials and simulated gateway callbacks.

### 1.1 Test Model

SmartDroneInspection uses a workflow-driven test model organized around the four connected main flows (`MF1` to `MF4`) rather than isolated screens:

- **MF1: Onboarding and readiness (`FE-01` to `FE-05`).** Accounts register and authenticate, Managers approve Partner Inspectors with signed contracts, Inspectors register compliant drones, and Customers register buildings with airspace screening.
- **MF2: Commercial workflow and dispatch (`FE-06` to `FE-12`).** Customers open building inspection requests, Managers prepare VND quotations and record signed contracts, eligible crews are dispatched, and Inspectors accept, decline, or withdraw before field work.
- **MF3: Permits, field operations, and findings (`FE-13` to `FE-17`).** Inspectors attach flight permits, complete multi-flight field sessions, upload photos or chunked video, run AI-assisted defect detection with fallback support, and confirm the findings baseline.
- **MF4: Reporting, settlement, and re-inspection (`FE-18` to `FE-24`).** Inspectors author reports, Managers approve and settle partner payouts before publishing, Customers accept and pay via Sepay VietQR or VNPay, and post-remediation re-inspections verify prior defects with fresh evidence.

### 1.2 Test Level

#### 1.2.1 Unit Testing

Unit tests verify domain entities, value objects, state machines, service business rules, React components, and Flutter widgets in isolation with mocked dependencies.

#### 1.2.2 Integration Testing

Integration tests verify REST controllers, JPA repositories, Flyway schema migrations, Spring Security filters, object storage tickets, payment webhooks, and the event outbox against containerized PostgreSQL 17 (`pgvector:pg17`) and S3Mock services.

#### 1.2.3 System Testing

System tests verify end-to-end connected main flows (`ConnectedMainFlowE2eIntegrationTest`), cross-module Spring Modulith boundaries, AI service degradation paths, and non-functional thresholds across the integrated stack.

#### 1.2.4 Acceptance Testing

Acceptance tests validate every product feature (`FE-01` to `FE-24`) against SRS business rules (`BR-01` to `BR-55`) and record multi-round execution outcomes in `Report5_Test Report.xlsx`.

#### 1.2.5 Definition of Done (DoD)

A feature or defect fix satisfies the Definition of Done when:

- Automated unit and integration tests pass with zero failures and meet the JaCoCo coverage gate.
- Spotless formatting (`spotless:check`), frontend lint (`npm run lint`), TypeScript compilation (`tsc --noEmit`), and `flutter analyze` exit with zero errors.
- Cross-module architecture boundaries pass `ModulithArchitectureTest`.
- Companion acceptance cases in `Report5_Test Report.xlsx` and traceability links are updated.

#### 1.2.6 User Acceptance Testing (UAT)

UAT executes role-scoped walkthroughs across the four web portals (`ADMIN`, `MANAGER`, `CUSTOMER`, `INSPECTOR`) and the Customer mobile application on local staging builds with seeded building, drone, and payment fixtures.

### 1.3 Assumptions and Constraints

#### 1.3.1 Assumptions

- Docker Desktop is available on the test workstation to run Testcontainers (`pgvector:pg17` and `adobe/s3mock`) during full backend verification.
- Third-party payment gateways (Sepay VietQR and VNPay sandbox) and SMTP servers are emulated through deterministic fixtures and signed webhook payloads in automated suites.
- Demonstration accounts represent each canonical role with realistic building and aircraft compliance metadata.

#### 1.3.2 Constraints

- External AI inference (FastAPI YOLO11s) and embedding services may be offline during continuous integration; tests must verify deterministic fallback paths without blocking workflows.
- Live drone flight control and civil aviation authority portals are external to the platform and are validated through uploaded permit documents and MAVLink telemetry logs.
- Native mobile testing covers the `CUSTOMER` role exclusively, matching the product boundary in the SRS.

### 1.4 Coverage Matrix (Design Domains, Roles, and Test Artefacts)

| Design Domain (Report 4) | Roles | Representative Functions | Verified By |
| --- | --- | --- | --- |
| `users` | All Roles | Registration, OTP, JWT sign-in, password reset, partner onboarding | `AuthControllerIntegrationTest`, `OnboardingWorkflowIntegrationTest`, `LoginPage.test.tsx`, `auth_repository_test.dart` |
| `assets` | Customer, Manager, Inspector, Admin | Building CRUD, airspace advisory, drone fleet, document and feature config | `AirspaceAdvisoryServiceTest`, `AssetCatalogPage.test.tsx`, `InspectorDroneRegistrationPage.test.tsx` |
| `contracts` | Customer, Manager, Inspector | Service requests, VND quotes, signed contracts, dispatch, Order and Partner chat, Sepay/VNPay, payouts, refunds | `ContractWorkflowServiceTest`, `SepayPaymentIntegrationTest`, `VnPayPaymentIntegrationTest`, `PaymentDueAndDocumentApiIntegrationTest`, `ContractsPage.test.tsx` |
| `inspections` | Inspector, Manager, Customer, Admin | Permits, multi-flight sessions, evidence tickets, AI findings, RAG notes, reports, re-inspection verifications | `ReinspectionWorkflowIntegrationTest`, `InspectionRecoveryFlowIntegrationTest`, `InspectionCreationLifecycleTest`, `ReportServiceReviewerScopeTest`, `ReinspectionWorkflow.test.tsx` |
| `notifications` | All Roles | Bilingual in-app notifications, read-all guard, critical SMTP emails | `NotificationWorkflowIntegrationTest`, `NotificationsPage.test.tsx`, `notificationFeed.test.ts` |
| `dashboard` | All Roles | Role-scoped analytics, queues, revenue charts | `DashboardAnalyticsServiceTest`, `DashboardPage.test.tsx` |
| `shared` and `database` | System | Spring Modulith boundaries, Flyway `V1` to `V4` and `V60` to `V80` migrations, 55-table inventory | `ModulithArchitectureTest`, `FullDatabaseSchemaMigrationTest`, `RuntimePersistenceInventoryTest` |
| `mobile` | Customer | Customer-only sign-in, building list, requests, chat, report view, payment PDFs, verdict expiry chips | `flutter test` (58 tests), `flutter analyze` |

### 1.5 Non-Screen System Functions

| No. | Non-Screen System Function |
| --- | --- |
| 1 | Flyway automated schema migration (`V1` to `V4` and `V60` to `V80`) across 53 application tables (55 total tables in `public`). |
| 2 | Spring Modulith event publication registry and transactional outbox delivery between domain modules. |
| 3 | Scheduled drone registration and pilot licence expiry scanner triggering 30-, 7-, 1-, and 0-day reminders. |
| 4 | Scheduled pending-acceptance timeout monitor flagging expired Inspector assignments for Manager reassignment. |
| 5 | Scheduled payment-overdue scanner issuing one reminder per unpaid accepted report past `payment_due_at`. |
| 6 | Sepay VietQR webhook `Authorization: Apikey` signature verification and idempotent `gateway_inbound_transactions` ledger persistence. |
| 7 | VNPay HMAC-SHA512 return and Instant Payment Notification (IPN) verification plus automatic order release on cancel or expiry. |
| 8 | Scoped single-object signed media ticket issuance and expiry validation for MinIO evidence downloads. |
| 9 | Local multilingual embedding generation and `pgvector` indexing with automatic keyword fallback (`HYBRID_MATCH`) when embeddings are unavailable. |
| 10 | Server-side re-inspection integrity guards blocking duplicate open re-inspections (`REINSPECTION_ALREADY_OPEN`), non-fresh evidence (`EVIDENCE_NOT_FRESH`, `EVIDENCE_REUSED`), and expired `RESOLVED` verdicts (`RESOLUTION_EXPIRED`). |

## 2. Test Strategy

The test strategy balances fast isolated checks with containerized integration suites so regressions are detected before release packaging.

### 2.1 Testing Types

Functional tests verify workflow rules, permitted state transitions, duplicate guards, and input limits such as attachment sizes and 20-day scheduling lead times. Security tests verify authentication protection, JWT validation, and data isolation by role, ownership, and assignment.

Integration and system tests verify evidence pipelines, AI fallback behavior, payment webhook signature checks, response times, and published-report integrity. Interface and regression tests verify English and Vietnamese localization, dark-mode theme behavior, and cross-release stability.

### 2.2 Test Levels

| Type of Tests | Unit | Integration | System | Acceptance |
| --- | :---: | :---: | :---: | :---: |
| Functional and Business Rule Testing | X | X | X | X |
| Domain State Machine Transition Testing | X | X | X | X |
| API and Database Persistence Testing | | X | X | |
| Security and Scope Isolation Testing | X | X | X | X |
| AI Vision, Narrative Drafting and Fallback Testing | X | X | X | X |
| Performance, Payment Webhook and Report Integrity Testing | | X | X | X |
| User Interface, Localization and Regression Testing | X | X | X | X |

### 2.3 Supporting Tools

| Purpose | Tool | Vendor/In-house | Version |
| --- | --- | --- | --- |
| Backend unit and integration testing | JUnit Jupiter, Spring Boot Test, MockMvc | Open Source / Broadcom | `JUnit 6.x` / `4.1.0` |
| Containerized database and storage harness | Testcontainers (`pgvector:pg17`, `adobe/s3mock`) | AtomicJar / Docker | `1.20.x` / `PostgreSQL 17` |
| Architectural boundary verification | Spring Modulith Test | Broadcom | `2.1.1` |
| Backend coverage measurement | JaCoCo Maven Plugin | EclEmma | `0.8.13` |
| Frontend component and unit testing | Vitest, React Testing Library, JSDOM | Open Source | `5.0.1` / `16.3.3` |
| Mobile widget and repository testing | Flutter Test, Dart Analyzer | Google | `Flutter 3.x` |
| Report workbook generation and verification | Custom Python Office Open XML (OOXML) exporter and unittest suite | In-house | `Python 3.12+` |

## 3. Test Plan

The test plan assigns feature ownership across all four team members, specifies the execution environment, and tracks five verification milestones.

### 3.1 Human Resources

| Worker/Doer | Role | Specific Responsibilities/Comments |
| --- | --- | --- |
| Trần Hoàng Trung Hiếu (`SE184212`) | Project Leader and Tester (`FE-01` to `FE-05`) | Owns test cases and regression runs for authentication, OTP, and 4-role RBAC (`FE-01`), partner admission (`FE-02`), drone fleet (`FE-03`), airspace map (`FE-04`), and financial ledger (`FE-05`), plus Customer Mobile co-testing. |
| Phùng Trung Quốc (`SE170027`) | Backend and Mobile Engineer and Tester (`FE-06` to `FE-12`) | Owns test cases and regression runs for building assets (`FE-06`), restricted-airspace advisories (`FE-07`), service requests and VND quotes (`FE-08`), signed contracts and dispatch (`FE-09`), Order, Partner, and Inspection Chat (`FE-10`), assignment timeout (`FE-11`), and notifications (`FE-12`). |
| Trần Tùng Bách (`SE180220`) | Full-Stack and AI Engineer and Tester (`FE-13` to `FE-18`) | Owns test cases and regression runs for flight permits (`FE-13`), field telemetry (`FE-14`), evidence and chunked video pipeline (`FE-15`), YOLO11 and fallback confirmation (`FE-16`), `DroneKnowledgeAI` RAG and drafting (`FE-17`), and report publication (`FE-18`), plus backend architecture and Mobile co-testing. |
| Trương Thái Như (`SE180082`) | Full-Stack Engineer and Tester (`FE-19` to `FE-24`) | Owns test cases and regression runs for Customer acceptance (`FE-19`), Sepay VietQR and VNPay settlement (`FE-20`), payment deadlines and documents (`FE-21`), Inspector payouts (`FE-22`), refunds and receivables (`FE-23`), and re-inspection (`FE-24`), plus automated test reconciliation and Report 5 workbook maintenance. |
| Supervisors | Reviewers | Review test strategy, audit traceability across Reports 3 to 5, and evaluate defence readiness. |

### 3.2 Test Environment

| Purpose | Tool | Provider | Version |
| --- | --- | --- | --- |
| Application runtime | Java 21 with Spring Boot Modulith | Eclipse Temurin / Broadcom | `Java 21` / `4.1.0` |
| Relational database | PostgreSQL (`53` application tables / `55` total in `public`, migrations `V1` to `V4`, `V60` to `V80`) | PostgreSQL Global Development Group | `17` |
| Object storage | MinIO (`inspection-evidence` bucket) | MinIO Inc. | `RELEASE.2025` |
| Test containers | Testcontainers with `pgvector:pg17` and `adobe/s3mock` | AtomicJar / Docker | `PostgreSQL 17` |
| Computer vision service | FastAPI with Ultralytics YOLO11s | Python / Ultralytics | `YOLO11s` |
| Web client under test | Chrome and Edge (desktop) | Google / Microsoft | Evergreen |
| Mobile client under test | Flutter test runner and Android client | Google | `Flutter 3.x` |
| Local execution platform | Windows 11 with PowerShell and Git Bash | Microsoft | `10.0.26200` |

### 3.3 Test Milestones

| Milestone Task | Start Date | End Date |
| --- | --- | --- |
| Milestone 1: Unit and migration foundation gate | `2026-09-15` | `2026-10-08` |
| Milestone 2: Core inspection, storage, detection, and report integration testing | `2026-10-09` | `2026-10-22` |
| Milestone 3: Review baseline and scope retirement verification | `2026-10-23` | `2026-10-27` |
| Milestone 4: Four-role, multi-flow consolidation across `MF1` to `MF4` with contracts and payment | `2026-10-28` | `2026-11-04` |
| Milestone 5: Final regression, 24-feature decomposition (`FE-01` to `FE-24`), staging walkthrough, and defence rehearsal | `2026-11-05` | `2026-11-30` |

## 4. Test Cases

The companion workbook (`Report5_Test Report.xlsx`, version 3.20) documents 80 test case rows across 24 feature sheets (`Feature 1` to `Feature 24`), comprising 78 active integration, system, and acceptance cases and 2 superseded flight-permit cases. Each feature sheet records case identifiers, preconditions, step-by-step procedures, expected results, and execution outcomes across Round 1, Round 2, and Round 3. Section 5.1 summarizes the automated backend, web, and mobile test suites that back these cases.

## 5. Test Reports

This section summarizes automated suite executions, acceptance test round outcomes, cross-cutting release assertions, and known defects.

### 5.1 Automated Suite Results

| Suite | Command | Scope | Result |
| --- | --- | --- | --- |
| Backend full suite | `.\mvnw.cmd verify` | Domain, service, controller, repository, migration, storage, architecture, and knowledge retrieval tests | Full rerun on 26 Nov 2026: 1,060 passed, 0 failures, 0 errors. JaCoCo coverage checks passed. |
| Backend focused reruns | `.\mvnw.cmd spotless:apply test` | Flight-data ownership, publication, assignment withdrawal, and duplicate open re-inspection guard (`ContractWorkflowServiceTest`, `InspectionCreationLifecycleTest`, `ReinspectionWorkflowIntegrationTest`) | 26 to 27 Nov 2026: 86/86 contract and creation lifecycle checks passed; 14 flight-log checks and 31 report API checks passed; Spotless clean. |
| Backend connected rerun | `.\mvnw.cmd -o surefire:test` | End-to-end onboarding through publication and migrated schema inventory | All 4 connected and schema inventory checks passed. |
| Web portal | `npm test` and `npx tsc --noEmit` | Components, pages, access policy, API clients, settlement, notifications, and re-inspection expiry banners across Inspector, Manager, and Customer | Release revision `bcb7b48` + 27 Nov 2026 rerun: 831+ passed, 0 failures (39/39 passed on focused re-inspection and report review suites). Lint, `tsc --noEmit`, and build exited 0. |
| Mobile | `flutter test` and `flutter analyze` | Customer-only access, localization, verdict expiry chips, payment PDFs, chat, knowledge references, and Customer screens | 26 Nov 2026: 58 tests passed, and `flutter analyze` reported 0 issues. |

During the initial backend run, Testcontainers timed out while starting PostgreSQL (875 passes and 184 startup errors). The subsequent full rerun completed all 1,060 tests and passed the JaCoCo coverage gate.

During the initial shared-checkout web run, Vite denied the MapLibre worker path for 5 files. Running against an isolated checkout and allowing the installed MapLibre dependency path resolved those 5 files (62/62 tests passed).

### 5.2 Acceptance Case Execution

![Acceptance case execution status](assets/charts/acceptance-status.png)

*Figure 5.1: Round 1 status for the 77-case baseline before adding the three assignment-withdrawal cases.*

| Main Flow and Features | Cases | Passed | Failed | Pending | N/A |
| --- | ---: | ---: | ---: | ---: | ---: |
| MF1 Onboarding and assets (`FE-01` to `FE-07`) | 22 | 19 | 0 | 2 | 1 |
| MF2 Commercial workflow and dispatch (`FE-08` to `FE-12`) | 20 | 16 | 0 | 1 | 3 |
| MF3 Permits, field operations, evidence, and findings (`FE-13` to `FE-17`) | 25 | 13 | 0 | 1 | 11 |
| MF4 Reports, settlement, and re-inspection (`FE-18` to `FE-24`) | 13 | 4 | 0 | 5 | 4 |
| Total | 80 | 52 | 0 | 9 | 19 |

In Round 1, 52 of 61 applicable cases passed and 9 remained pending, with zero failures. The remaining 19 rows were marked N/A for Round 1 because those capabilities were delivered in later iterations.

Round 3 records 16 passes and zero failures (`WF3-005`, `WF3-006`, `WF3-009`, `WF3-016`, `WF3-018`, `WF3-019`, `WF3-021`, `WF3-026` to `WF3-031`, and `WF2-032` to `WF2-034`). Eight cases (`WF2-021`, `WF3-020`, `WF3-022` to `WF3-025`, `WF3-032`, and `WF3-033`) remain pending full manual staging execution.

The assignment-withdrawal regression passed all 15 checks across the recovery integration and inspection lifecycle suites:

- **WF2-032 (`FE-11`):** The assigned Inspector withdrew before field work, and the scheduled occurrence required Manager reassignment.
- **WF2-033 (`FE-13`):** Withdrawal after a field abort was rejected with HTTP `409 ASSIGNMENT_FIELD_WORK_STARTED`.
- **WF2-034 (`FE-09`):** The Manager cancelled the occurrence after withdrawal, preserving both reasons and clearing the reassignment flag.

### 5.3 Cross-Cutting Assertions

| Assertion | Test | What It Verifies |
| --- | --- | --- |
| Database schema matches the release | `FullDatabaseSchemaMigrationTest` | Flyway applies `V1` to `V4` and `V60` to `V80` and confirms all 55 expected tables in `public`, including the event outbox and Flyway schema history. |
| Module boundaries hold | `ModulithArchitectureTest` | No module accesses another outside its declared `allowedDependencies`. |
| Lifecycle is connected | `ConnectedMainFlowE2eIntegrationTest` | Building and drone setup, request and quotation, dispatch, field evidence, findings, Manager review, partner payout, and publication execute in one connected run. |
| A report author cannot publish | `ReportServiceReviewerScopeTest` | Publication requires a `MANAGER` reviewer who is not the author, while `ADMIN` remains read-only (`REPORT_SCOPE_DENIED`). |
| Customer flight data requires publication | `InspectionFieldSessionControllerFlightLogTest`, `InspectionDroneHubFlightLogTest` | The owning Customer sees progress before publication without flight logs and gains access to stored flight records only after publication. Other Customers are denied. |
| Flight permit self-attestation holds | `FlightPermitPolicyTest`, `FlightPermitVerificationIntegrationTest` | Valid permit upload moves status to `APPROVED`; drone changes or out-of-window reschedules reset to `PENDING_REVIEW`. |
| Media is scoped | `EvidenceServiceTest` | A signed media ticket grants access to one evidence record and expires cleanly. |
| Payment needs a verified signature | `SepayWebhookControllerTest`, `VnPayWebhookAndGatewayTest` | Browser redirects never settle payments; invalid `Authorization: Apikey` or VNPay HMAC-SHA512 signatures are rejected, and Sepay callbacks persist idempotently in `gateway_inbound_transactions`. |
| Knowledge retrieval and note drafting | `HistoricalCaseServiceTest`, `HistoricalCaseApiIntegrationTest`, `KnowledgeRecommendationPanel.test.tsx`, `knowledge_recommendation_test.dart` | Covers `PGVECTOR_RAG`, `HYBRID_MATCH` fallback, and `AI_VISION_RAG` note drafting while excluding other Customers' records and hiding empty mobile reference strips. |
| Payment deadline and documents over HTTP | `PaymentDueAndDocumentApiIntegrationTest` | Acceptance sets `payment_due_at` once; the document API returns `409` before acceptance, a payment notice after acceptance, and a receipt after payment. Other Customers receive `404`. |
| Duplicate open re-inspection is blocked | `ReinspectionWorkflowIntegrationTest`, `ContractWorkflowService`, `InspectionCreationService` | Attempting to create a second active MF2 re-inspection request or direct re-inspection for the same `sourceInspectionId` fails with HTTP `409 REINSPECTION_ALREADY_OPEN`. |
| Expired re-inspection verdict is surfaced early across roles | `verdictExpiry.ts`, `VerdictExpiryBanner.tsx`, `ReinspectionWorkflow.test.tsx` | Inspector, Manager, and Customer Web portals plus Customer Mobile display 14-day expiry warnings and expired alerts; the backend blocks authoring, submission, approval, and publication with `409 RESOLUTION_EXPIRED`. |

### 5.4 Release Workflow Verification

`ConnectedMainFlowE2eIntegrationTest` runs one complete inspection across `MF1` to `MF4` using isolated role accounts to verify cross-module state transitions.

#### MF1: Onboarding and Readiness

The connected test provisions distinct Customer, Manager, and Inspector accounts, registers the Inspector's drone, and creates the Customer's building with inspection items. Schema tests separately verify all 55 tables after applying every Flyway migration.

#### MF2: Quotation and Dispatch

The Customer opens an inspection request, the Manager prepares the VND quotation and completes contracting and dispatch, and the assigned Inspector accepts the occurrence. Subsequent field steps consume this exact occurrence.

#### MF3: Permits, Field Session, and Findings

The Inspector uploads a self-attested flight permit, starts and completes the field session (`IN_PROGRESS` to `FIELD_COMPLETED`), uploads evidence, confirms findings, and submits the drafted report. Dedicated `FE-13` to `FE-17` suites cover permit rejection, field exceptions, chunked video, and AI fallback behavior.

#### MF4: Independent Review, Publication, and Settlement

The Manager approves the submitted report, settles the partner payout fixture, and publishes the deliverable. Browser and API checks confirm that the Customer sees progress without flight logs before publication and accesses both the Findings report and Flight operations tabs afterward. Payment suites verify Sepay VietQR and VNPay signatures, idempotency, and PDF notice/receipt states.

### 5.5 Defects and Limitations

| ID | Severity | Status | Description | Impact |
| --- | --- | --- | --- | --- |
| `DEF-01` | Low | Resolved | The mobile `UserRole` enum previously included the retired `MAINTENANCE_ENGINEER` value. It now matches the four canonical platform roles. | `flutter analyze` and all 58 mobile tests pass, restricting mobile sign-in to Customers. |
| `DEF-02` | Low | Open | The legacy backend E2E runner script resolves its frontend root to a directory that does not exist in the current multi-repo workspace. | `ConnectedMainFlowE2eIntegrationTest` and Playwright web checks provide the active end-to-end verification path. |

The companion workbook preserves all historical acceptance round results, including pending cases. Automated Surefire and Vitest suites verify the underlying service, controller, and UI assertions, while full manual walkthroughs remain tracked in the workbook.
