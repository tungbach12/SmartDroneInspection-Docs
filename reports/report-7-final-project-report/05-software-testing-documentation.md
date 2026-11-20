---
title: "Report 7 - Software Testing Documentation"
document_type: report7-section
weight: 50
source: "Report7_Final Project Report.docx"
---
# V. Software Testing Documentation

## 1. Scope of Testing

Testing covers the delivered platform across the web portals, the customer mobile application, the backend, and the AI, telemetry, and payment integrations, for all eight features `FE-01`–`FE-08` and the business rules `BR-01`–`BR-55`. The inspection scope is buildings only.

`FE-01` covers customer registration with airspace screening, sign-in by password, one-time code, and Google, session rotation, the account profile, and four-role authorization at both the route and the API boundary. `FE-02` covers the public partner application, licence records and flight logs, admission review, and inspector-owned drone registration. `FE-03` covers buildings, checkpoints and reference documents, recurring occurrence materialization, and deduplicated notifications. `FE-04` covers requests, order chat, VND quotations, signed agreements, dispatch, and airspace evaluation. `FE-05` covers the permit gate, field sessions, telemetry, and abort recovery. `FE-06` covers evidence intake, YOLO11 detection with vision fallback, and findings confirmation. `FE-07` covers report compilation, advisory narrative drafting, independent review, and publication. `FE-08` covers customer acceptance, PayOS and VNPay settlement, payouts, refunds, and the re-inspection verification loop.

In scope: building inspection including tenant-isolated `DroneKnowledgeAI` advisory retrieval over engineering standards and historical finding cases (`BR-55`). Out of scope: physical aircraft control and flight-controller firmware; corrective maintenance execution and its repair knowledge base; non-building infrastructure; native push delivery and commercial mail relay; banking core systems behind the payment gateways; and mobile behaviour for roles other than `CUSTOMER`.

Four levels were executed. Unit level verifies entities, services, components, and widgets in isolation. Integration level verifies controllers, repositories, migrations, the security filter chain, object storage, and the event outbox against containerized services. System level verifies connected flows and non-functional thresholds across the integrated stack. Acceptance level verifies business rules and acceptance criteria per feature.

Constraints: integration tests need a running Docker daemon; when the inference container or the drafting gateway is unreachable the system routes to its fallbacks so workflows stay testable; payment verification uses signed test credentials rather than live debits; and permits, airspace results, and reports are governance records, not government clearance.

## 2. Test Strategy

### 2.1 Testing Types

Functional and business rule testing applies equivalence partitioning and boundary analysis to the stated limits — 10 MB photographs, 2 GB video in 10 MiB chunks, coordinate ranges, rate percentages, the twenty-day lead time, and the occurrence and interval bounds. Domain state machine testing walks every lifecycle entity along its valid edges and asserts that illegal edges are refused. Security and scope isolation testing probes cross-organization identifiers, permutes the four roles across the four portals, and simulates brute-force sign-in. AI testing verifies bounding-box parsing, automatic vision fallback, and the deterministic template path. Performance and payment testing covers response latency, tampered-signature webhook rejection, and published-report immutability. Interface, localization, and regression testing covers component rendering, `Accept-Language` negotiation, theme persistence, and repeated full-suite runs.

### 2.2 Test Levels

| Type of Tests | Unit | Integration | System | Acceptance |
| --- | :---: | :---: | :---: | :---: |
| Functional and Business Rule Testing | X | X | X | X |
| Domain State Machine Transition Testing | X | X | X | X |
| API and Database Persistence Testing | | X | X | |
| Security and Scope Isolation Testing | X | X | X | X |
| AI Vision, Narrative Drafting and Fallback Testing | X | X | X | X |
| Performance, Payment Webhook and PDF Integrity Testing | | X | X | X |
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
| Report workbook generation and verification | Custom Python OOXML exporter and unittest suite | In-house | `Python 3.12+` |

## 3. Test Plan

### 3.1 Human Resources

| Worker/Doer | Role | Specific Responsibilities/Comments |
| --- | --- | --- |
| Trần Hoàng Trung Hiếu | Project Leader and Tester (`FE-01`, `FE-02` owner) | Owns the cases and regression runs for registration, access control, partner admission, buildings, and drones. |
| Phùng Trung Quốc | Backend and Mobile Engineer and Tester (`FE-03`, `FE-04` owner) | Owns the cases and regression runs for recurring requests, notifications, quotations, agreements, and dispatch. |
| Trần Tùng Bách | Full-Stack and AI Engineer and Tester (`FE-05`, `FE-06` owner) | Owns the cases and regression runs for the permit gate, field sessions, evidence, detection, reports, and payment. |
| Trương Thái Như | Full-Stack Engineer and Tester | Supports cross-feature regression, environment provisioning, and workbook reconciliation. |
| Supervisors | Reviewers | Review the strategy, audit traceability across Reports 3–5, and evaluate defence readiness. |

### 3.2 Test Environment

| Purpose | Tool | Provider | Version |
| --- | --- | --- | --- |
| Application runtime | Java 21 with Spring Boot Modulith | Eclipse Temurin / Broadcom | `Java 21` / `4.1.0` |
| Relational database | PostgreSQL (45 application tables / 47 total, migrations `V1`–`V4`, `V60`–`V65`) | PostgreSQL Global Development Group | `17` |
| Object storage | MinIO (`inspection-evidence` bucket) | MinIO Inc. | `RELEASE.2025` |
| Test containers | Testcontainers with `pgvector:pg17` and `adobe/s3mock` | AtomicJar / Docker | `PostgreSQL 17` |
| Computer vision service | FastAPI with Ultralytics YOLO11s | Python / Ultralytics | `YOLO11s` |
| Web client under test | Chrome and Edge (desktop) | Google / Microsoft | Evergreen |
| Mobile client under test | Flutter test runner and Android client | Google | `Flutter 3.x` |
| Local execution platform | Windows 11 with Git Bash | Microsoft | `10.0.26200` |

### 3.3 Test Milestones

| Milestone Task | Start Date | End Date |
| --- | --- | --- |
| Milestone 1: Unit and migration foundation gate | `2026-09-15` | `2026-10-08` |
| Milestone 2: Core inspection, storage, detection and PDF integration testing | `2026-10-09` | `2026-10-22` |
| Milestone 3: Review baseline and scope retirement verification | `2026-10-23` | `2026-10-27` |
| Milestone 4: Four-role, eight-feature consolidation across `MF1`–`MF4` with contracts and payment | `2026-10-28` | `2026-11-04` |
| Milestone 5: Final regression, staging walkthrough, and defence rehearsal | `2026-11-05` | `2026-11-30` |

## 4. Test Cases

Unit test cases live in the repository suites. On 20 Nov 2026 the backend `.\mvnw.cmd verify` exited 0 with `971` tests passed, `0` failures, Spring Modulith boundary verification passed and JaCoCo coverage checks met. The frontend `npm test` ran `97` files (`93` passed, `4` skipped) and `724` tests (`720` passed, `4` skipped, `0` failed), covering the four-portal access policy, the airspace map, the calendar, evidence/findings/report screens, the re-inspection verdict-expiry warning, quick status filter chips, and `DroneKnowledgeAI` note drafting (`DraftNoteAction` / `Draft all notes`) and references. The mobile suite (`PR #27`, `9939c00`) passed `56` tests with `0` failures, covering customer-only admission, localization, verdict expiry, payment-document PDF, Inspector–Customer chat, the knowledge strip, and the customer screens. Report 5 tracks `64` active case IDs across `FE-01`–`FE-08`, including `WF3-029` (DroneKnowledgeAI note drafting, local 384d RAG, status filters & tenant isolation), `WF3-030` (advisory knowledge references in the AI summary) and `WF3-031` (Customer Mobile parity from `PR #27`).

Integration, system, and acceptance cases live in `Report5_Test Report.xlsx`, partitioned across eight feature sheets with columns for the procedure, expected results, preconditions, three execution rounds, the test date, the tester, and a note recording the mode and the automated evidence.

## 5. Test Reports

### 5.1 Automated Suite Results

![Automated test inventory](assets/charts/test-inventory.png)

*Figure 7.9 — Verified automated test inventory by repository at handover.*

| Suite | Command | Scope | Result |
| --- | --- | --- | --- |
| Backend | `.\mvnw.cmd verify` | Domain, service, controller, repository, migration, storage, architecture and knowledge retrieval tests | `971` tests passed, `0` failures, `0` errors; Spring Modulith boundary verification and JaCoCo coverage gate met. `spotless:check` passed. |
| Web portal | `npm test` | Components, pages, access policy, API clients, verdict-expiry warnings, filter chips and DroneKnowledgeAI note drafting | `97` files (`93` passed, `4` skipped), `724` tests (`720` passed, `4` skipped), `0` failed. `npm run lint` returned `0` errors and `npm run build` exited `0`. |
| Mobile | `flutter test` | Customer-only session, localization, verdict expiry, payment PDF, chat, knowledge strip and screens (`PR #27`) | `56` tests passed, `0` failures; `dart format --set-exit-if-changed .` and `flutter analyze` both passed. |

### 5.2 Acceptance Case Execution

![Acceptance case execution status](assets/charts/acceptance-status.png)

*Figure 7.10 — Round 1 acceptance case status for the 64 active cases across `FE-01`–`FE-08`.*

| Feature | Total cases | Passed | Failed | Pending | N/A | Coverage focus |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| `FE-01` | 8 | 7 | 0 | 1 | 0 | Registration, airspace screening, sign-in, sessions, and the four-role boundary |
| `FE-02` | 7 | 6 | 0 | 1 | 0 | Partner application, admission, licence records, and drone registration review |
| `FE-03` | 8 | 8 | 0 | 0 | 0 | Buildings, checkpoints, documents, occurrences, and notifications |
| `FE-04` | 8 | 7 | 0 | 1 | 0 | Requests, quotations, signed agreements, dispatch, and eligibility |
| `FE-05` | 7 | 6 | 0 | 0 | 1 | Permit verification, field sessions, telemetry, and abort recovery |
| `FE-06` | 14 | 7 | 0 | 2 | 5 | Evidence intake, detection, findings baseline, and re-inspection evidence |
| `FE-07` | 5 | 4 | 0 | 0 | 1 | Report compilation, independent review, and publication |
| `FE-08` | 7 | 0 | 0 | 4 | 3 | Acceptance, PayOS and VNPay settlement, payouts, and refunds |
| **Total** | **64** | **45** | **0** | **9** | **10** | All eight features |

The Round 1 inventory recorded `45` passed and `0` failed cases across `64` active cases: `9` pending and `10` N/A. The N/A rows include `WF3-029`, `WF3-030` and `WF3-031`, which were added later than Round 1 and are reported in Round 3 rather than back-filled.

Report 5 records `13` executed Round 3 cases with `0` failures: `WF3-005`, `WF3-006`, `WF3-009`, `WF3-016`, `WF3-018`, `WF3-019`, `WF3-021`, `WF3-026`, `WF3-027`, `WF3-028`, `WF3-029`, `WF3-030` and `WF3-031`; `WF3-020` and `WF3-022`–`WF3-025` remain Pending. `PaymentDueAndDocumentApiIntegrationTest` supplies the connected-HTTP evidence for `WF3-026`/`WF3-027`; `WF3-028` records fresh re-inspection evidence, `WF3-019` the current payout contract, and `WF3-029`–`WF3-031` the `DroneKnowledgeAI` retrieval, advisory summary references and Customer Mobile parity verified on 19 Nov 2026.

### 5.3 Cross-Cutting Assertions

| Assertion | Test | What it proves |
| --- | --- | --- |
| Schema baseline is exact | `FullDatabaseSchemaMigrationTest` | The applied migration set is exactly `V1`, `V2`, `V3`, `V4`, `V60`, `V61`, `V62`, `V63`, `V64` and `V65`; the inventory is exactly 47 relations in `public` (45 application tables, the `event_publication` outbox and `flyway_schema_history`), with 44 JPA runtime entity tables. |
| Module boundaries hold | `ModulithArchitectureTest` | No module reaches another outside its declared `allowedDependencies`. |
| Lifecycle is connected | `ConnectedMainFlowE2eIntegrationTest` | Onboarding, building and drone registration, request and quotation, dispatch, evidence and detection, publication, and settlement execute in one run. |
| A report author cannot publish | Reviewer-scope and role-policy tests | Publication requires a reviewer who is not the author. |
| A permit uploader cannot verify | Permit review tests | Verification requires a distinct manager or administrator. |
| Media is scoped | Evidence ticket tests | A signed ticket grants access to one evidence record and nothing else. |
| Payment needs a signature | PayOS and VNPay webhook tests | A redirect alone never settles a payment; a tampered callback is rejected. |
| Knowledge retrieval & note drafting are tenant-isolated | `HistoricalCaseServiceTest`, `HistoricalCaseApiIntegrationTest`, `InspectionFindingsPage.test.tsx`, `KnowledgeRecommendationPanel.test.tsx`, `knowledge_recommendation_test.dart` | `DroneKnowledgeAI` returns `PGVECTOR_RAG` via local `fastembed` (`vector(384)`) when embeddings exist and deterministic `HYBRID_MATCH` otherwise, plus `AI_VISION_RAG` for note drafting; benchmark cases are anonymized, cross-organization cases and the current inspection are excluded, and the customer mobile strip hides when empty. |
| Payment deadline and documents over HTTP | `PaymentDueAndDocumentApiIntegrationTest` | On Testcontainers PostgreSQL 17 and the real security filter chain: acceptance stamps `payment_due_at` once, the document endpoint returns `409` before acceptance, a notice PDF after acceptance and a receipt after verified payment, foreign-organization callers receive `404`, and a repeated overdue scan sends no second reminder. Report 5 records this as the Round 3 Passed evidence for `WF3-026` and `WF3-027`. |
| Expired re-inspection verdict is surfaced early | `verdictExpiry.ts`, `VerdictExpiryBanner`, `ValidityNotice`, `ReinspectionWorkflow.test.tsx` | The Web client distinguishes lapsed `RESOLVED` verdicts from those lapsing within 14 days and warns before report authoring; the backend remains the authority that refuses an expired verdict with `RESOLUTION_EXPIRED`. |

### 5.4 Defects and Limitations

| ID | Severity | Status | Description | Impact |
| --- | --- | --- | --- | --- |
| `DEF-01` | Low | Open | The mobile `UserRole` enumeration still parses the retired `MAINTENANCE_ENGINEER` role. | Harmless at runtime because the session gate admits `CUSTOMER` only, but the stale member should be removed. |
| `DEF-02` | Low | Open | The backend E2E runner script resolves its frontend root to a directory that does not exist in the workspace. | The script cannot execute as written; the connected lifecycle is verified by the integration test instead. |

Neither defect affects a delivered feature path, and neither is claimed as passing. Cases not executed in this run remain `Pending` in the workbook.

