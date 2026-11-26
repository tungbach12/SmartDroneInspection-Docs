---
title: "Report 7 - Software Testing Documentation"
document_type: report7-section
weight: 50
source: "Report7_Final Project Report.docx"
---
# V. Software Testing Documentation

## 1. Scope of Testing

The test scope covers all 24 features across the web portal, Customer mobile app, backend, and AI, telemetry, and payment integrations.

- **`MF1` — Onboarding and access.** Account registration, sign-in, role permissions, Inspector and drone registration, and airspace screening.
- **`MF2` — Requests and dispatch.** Building records, quotations, signed contracts, Inspector and drone assignment, messaging, and notifications.
- **`MF3` — Field work and findings.** Flight permit submission, field sessions and telemetry, evidence upload and processing, AI-assisted analysis, and findings confirmation.
- **`MF4` — Reporting and settlement.** Independent review and publication, Customer acceptance, payments, Inspector payouts, refunds, and re-inspection.

Chapter III, Section 3.8 defines the product scope. Payment tests use test credentials and simulated gateway callbacks.

Four levels were executed. Unit level verifies entities, services, components, and widgets in isolation. Integration level verifies controllers, repositories, migrations, the security filter chain, object storage, and the event outbox against containerized services. System level verifies connected flows and non-functional thresholds across the integrated stack. Acceptance level verifies business rules and acceptance criteria per feature.

Integration tests require Docker. The test strategy includes fallback behavior when AI services are unavailable.

## 2. Test Strategy

### 2.1 Testing Types

Functional tests cover workflow rules, permitted status changes, and limits such as file sizes and scheduling dates. Security tests cover sign-in protection and access by role, ownership, and assignment.

Integration and system tests cover evidence processing, AI fallbacks, payment callback verification, response times, and published-report integrity. Interface and regression tests cover localization, theme settings, and behavior across releases.

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
| Report workbook generation and verification | Custom Python OOXML exporter and unittest suite | In-house | `Python 3.12+` |

## 3. Test Plan

### 3.1 Human Resources

| Worker/Doer | Role | Specific Responsibilities/Comments |
| --- | --- | --- |
| Trần Hoàng Trung Hiếu (`SE184212`) | Project Leader and Tester (`FE-01`–`FE-05`) | Owns the cases and regression runs for authentication/OTP/4-role RBAC (`FE-01`), partner admission (`FE-02`), owned-drone fleet (`FE-03`), airspace map (`FE-04`), and financial history ledger (`FE-05`), plus Customer Mobile co-testing. |
| Phùng Trung Quốc (`SE170027`) | Backend and Mobile Engineer and Tester (`FE-06`–`FE-12`) | Owns the cases and regression runs for building assets (`FE-06`), restricted-airspace advisories (`FE-07`), service requests & VND quotes (`FE-08`), signed contracts & dispatch (`FE-09`), Order, Partner, and Inspection Chat (`FE-10`), assignment timeout (`FE-11`), and notifications (`FE-12`). |
| Trần Tùng Bách (`SE180220`) | Full-Stack and AI Engineer and Tester (`FE-13`–`FE-18`) | Owns the cases and regression runs for flight permits (`FE-13`), field telemetry (`FE-14`), evidence/chunked video pipeline (`FE-15`), YOLO11 + fallback confirmation (`FE-16`), `DroneKnowledgeAI` RAG & drafting (`FE-17`), and report publication (`FE-18`), plus backend/DB architecture & Mobile co-testing. |
| Trương Thái Như (`SE180082`) | Full-Stack Engineer and Tester (`FE-19`–`FE-24`) | Owns the cases and regression runs for customer acceptance (`FE-19`), Sepay VietQR/VNPay settlement (`FE-20`), payment deadlines/documents (`FE-21`), Inspector payouts (`FE-22`), refunds & receivables (`FE-23`), and re-inspection (`FE-24`), plus automated test reconciliation & Report 5 workbook maintenance. |
| Supervisors | Reviewers | Review the strategy, audit traceability across Reports 3–5, and evaluate defence readiness. |

### 3.2 Test Environment

| Purpose | Tool | Provider | Version |
| --- | --- | --- | --- |
| Application runtime | Java 21 with Spring Boot Modulith | Eclipse Temurin / Broadcom | `Java 21` / `4.1.0` |
| Relational database | PostgreSQL (`53` application tables / `55` total in `public`, migrations `V1`–`V4`, `V60`–`V80`) | PostgreSQL Global Development Group | `17` |
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
| Milestone 2: Core inspection, storage, detection and report integration testing | `2026-10-09` | `2026-10-22` |
| Milestone 3: Review baseline and scope retirement verification | `2026-10-23` | `2026-10-27` |
| Milestone 4: Four-role, multi-flow consolidation across `MF1`–`MF4` with contracts and payment | `2026-10-28` | `2026-11-04` |
| Milestone 5: Final regression, 24-feature decomposition (`FE-01`–`FE-24`), staging walkthrough, and defence rehearsal | `2026-11-05` | `2026-11-30` |

## 4. Test Cases

The backend, web, and mobile automated suites are summarized in Section 5.1. The Report 5 workbook (`Report5_Test Report.xlsx`, version 3.15) records 75 active integration, system, and acceptance cases and two superseded flight-permit cases. Its 24 feature sheets list the procedures, expected results, and results of each test round.

## 5. Test Reports

### 5.1 Automated Suite Results

![Automated test inventory](assets/charts/test-inventory.png)

*Figure 7.9 — Verified automated test inventory by repository at handover.*

| Suite | Command | Scope | Result |
| --- | --- | --- | --- |
| Backend | `.\mvnw.cmd test` | Domain, service, controller, repository, migration (`V1`–`V4`, `V60`–`V80`), storage, architecture and knowledge retrieval tests | `1,052` tests passed, `0` failures, `0` errors; Spring Modulith boundary verification and `55`-table schema migration gate passed (25 Nov 2026 verification). |
| Web portal | `npm test` (`npx vitest run`) | Components, pages, access policy, API clients, Sepay/VNPay payout & settlement UI, ratings, bilingual notifications, and DroneKnowledgeAI note drafting | Full suite (25 Nov 2026): `120` files (`116` passed, `4` deprecated skipped), `830` tests (`826` passed, `4` skipped), `0` failed; `npm run lint` (`0` errors) and `npm run build` exited `0`. |
| Mobile | `flutter test` | Customer-only access, localization, verdict expiry, payment PDF, chat, knowledge references, and Customer screens | `58` tests passed with `0` failures. `flutter analyze` passed. |

### 5.2 Acceptance Case Execution

![Acceptance case execution status](assets/charts/acceptance-status.png)

*Figure 7.10 — Round 1 acceptance case status for the 77 listed rows (75 active) across FE-01–FE-24 (Report 5 v3.15).*

| Feature | Total cases | Passed | Failed | Pending | N/A | Coverage focus |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| `FE-01` | 7 | 6 | 0 | 1 | 0 | Registration, OTP, Google OAuth2, sessions, profile, EN/VI i18n, and 4-role RBAC |
| `FE-02` | 4 | 3 | 0 | 1 | 0 | Partner Inspector application, non-disclosing email checks, `inspector_profiles`, and flight logs |
| `FE-03` | 3 | 3 | 0 | 0 | 0 | Admin drone checklists, owned-drone registration/renewal, photos, and serviceability states |
| `FE-04` | 3 | 3 | 0 | 0 | 0 | Interactive coordinate map, coordinate bounds validation, and hard No-Fly Zone gate |
| `FE-05` | 1 | 0 | 0 | 0 | 1 | Scoped Customer/Inspector/Manager financial history ledgers (`WF3-032`: `N/A / Pending / Pending`) |
| `FE-06` | 3 | 3 | 0 | 0 | 0 | Building registry (`V66` `ownership_information`), checkpoints (`V80` + lock), MinIO docs, and retirement lock |
| `FE-07` | 1 | 1 | 0 | 0 | 0 | Restricted-airspace `MSG28` amber advisory and immediate onboarding (`WF1-009` Passed) |
| `FE-08` | 6 | 6 | 0 | 0 | 0 | Compact requests & concise recurring titles, cadence bounds/month-end anchoring, and VND quotes |
| `FE-09` | 6 | 5 | 0 | 1 | 0 | Signed agreements, occurrence dispatch conflict/eligibility guards, abort recovery, Mobile E2E |
| `FE-10` | 2 | 2 | 0 | 0 | 0 | Separated Customer–Manager Order Chat, Partner Chat (`V79`), and Customer–Inspector Inspection Chat |
| `FE-11` | 1 | 0 | 0 | 0 | 1 | Assignment acceptance timeout and escalation alert (`WF2-021`: `N/A / Pending / Pending`) |
| `FE-12` | 3 | 3 | 0 | 0 | 0 | Deduplicated bilingual (`EN`/`VI`) Modulith notifications (`WF2-028`) and `targetPath` safety |
| `FE-13` | 5 | 2 | 0 | 0 | 3 | Self-attested flight permit gate (`APPROVED` on valid upload) and drone/window reset (`WF2-029`–`WF2-031`) |
| `FE-14` | 5 | 4 | 0 | 0 | 1 | Multi-sortie field session start/complete/abort, MAVLink telemetry, log import, dashboards, calendar |
| `FE-15` | 5 | 1 | 0 | 0 | 4 | EXIF image normalization/thumbnails, duplicate numbering, 2 GiB chunked MP4, FFmpeg, Range tickets |
| `FE-16` | 7 | 6 | 0 | 1 | 0 | YOLO11 (`70%` default) + Vision fallback, filter chips, baseline confirmation, and fresh evidence |
| `FE-17` | 2 | 0 | 0 | 0 | 2 | Tenant-isolated `DroneKnowledgeAI` local 384d RAG, note drafting, Mobile strip, and summary refs |
| `FE-18` | 4 | 4 | 0 | 0 | 0 | Five-state report lifecycle, compilation, independent Manager review (`Approved -> Payout -> Published`), PDF export |
| `FE-19` | 1 | 0 | 0 | 1 | 0 | Customer report acceptance (`ACCEPTED`), ratings (`V70`/`V73`), clarification paths, staging handoff |
| `FE-20` | 2 | 0 | 0 | 0 | 2 | Normalized `V29`/`V67`–`V68` finance schema, Sepay VietQR & VNPay HMAC webhooks, and masked views |
| `FE-21` | 2 | 0 | 0 | 2 | 0 | Payment due deadline (`payment_due_at`), single overdue reminder, and notice/receipt PDF |
| `FE-22` | 1 | 0 | 0 | 0 | 1 | Partner Inspector payout reconciliation (`ELIGIBLE -> PAID`, Sepay VietQR `SDIPAY`, idempotency; `WF3-033`) |
| `FE-23` | 1 | 0 | 0 | 1 | 0 | Refund initiation holds, exact allocation, legacy reconciliation, and Inspector receivables |
| `FE-24` | 2 | 0 | 0 | 1 | 1 | Post-remediation re-inspection verdicts (`RESOLVED`/`UNRESOLVED`/`INCONCLUSIVE`) & Mobile parity |
| **Total** | **77** | **52** | **0** | **9** | **16** | Report 5 `v3.15` (`75` active cases + `2` historical superseded `FE-13` cases) |

In Round 1, 52 of the 61 applicable cases passed and 9 were pending, with zero failures. The other 16 rows were marked N/A.

Report 5 records 13 passes and zero failures in Round 3 (`WF3-005`, `WF3-006`, `WF3-009`, `WF3-016`, `WF3-018`, `WF3-019`, `WF3-021`, and `WF3-026`–`WF3-031`). `WF3-020`, `WF3-022`–`WF3-025`, `WF3-032`, `WF2-021`, and `WF3-033` remain pending.

The cases cover payouts (`WF3-019`), payment deadlines and documents (`WF3-026`, `WF3-027`), fresh re-inspection evidence (`WF3-028`), and knowledge references on web and mobile (`WF3-029`–`WF3-031`).

### 5.3 Cross-Cutting Assertions

| Assertion | Test | What it verifies |
| --- | --- | --- |
| Database schema matches the release | `FullDatabaseSchemaMigrationTest` | Flyway applies `V1`–`V4` and `V60`–`V80`. The test checks all 55 expected tables in `public`, including the event outbox and the Flyway migration ledger. |
| Module boundaries hold | `ModulithArchitectureTest` | No module reaches another outside its declared `allowedDependencies`. |
| Lifecycle is connected | `ConnectedMainFlowE2eIntegrationTest` | Onboarding, building and drone registration, request and quotation, dispatch, evidence and detection, publication, and settlement execute in one run. |
| A report author cannot publish | Reviewer-scope and role-policy tests | Publication requires a `MANAGER` reviewer who is not the author (`ADMIN` is read-only). |
| Flight permit self-attestation holds | Permit policy and workflow tests | Valid permit upload immediately transitions the permit to `APPROVED`; drone change or out-of-window reschedule resets to `PENDING_REVIEW` (`ADMIN`/`MANAGER` cannot alter). |
| Media is scoped | Evidence ticket tests | A signed ticket grants access to one evidence record and nothing else. |
| Payment needs a signature | `SepayWebhookControllerTest`, `VnPayWebhookAndGatewayTest` & webhook tests | A browser redirect alone never settles a payment; missing/forged `Authorization: Apikey` or VNPay HMAC-SHA512 signatures are rejected, while Sepay inbound outcomes persist idempotently in `gateway_inbound_transactions`. |
| Knowledge retrieval and note drafting | `HistoricalCaseServiceTest`, `HistoricalCaseApiIntegrationTest`, `InspectionFindingsPage.test.tsx`, `KnowledgeRecommendationPanel.test.tsx`, `knowledge_recommendation_test.dart` | Tests cover vector retrieval (`PGVECTOR_RAG`), keyword fallback (`HYBRID_MATCH`), and note drafting (`AI_VISION_RAG`). Results exclude the current inspection and other Customers' records. The mobile reference strip hides when empty. |
| Payment deadline and documents over HTTP | `PaymentDueAndDocumentApiIntegrationTest` | Acceptance sets `payment_due_at` once. The document API returns `409` before acceptance, a notice after acceptance, and a receipt after payment. Another Customer receives `404`. Repeated scans send one overdue reminder. Report 5 records the results under `WF3-026` and `WF3-027`. |
| Expired re-inspection verdict is surfaced early | `verdictExpiry.ts`, `VerdictExpiryBanner`, `ValidityNotice`, `ReinspectionWorkflow.test.tsx` | The Web client distinguishes lapsed `RESOLVED` verdicts from those lapsing within 14 days and warns before report authoring; the backend remains the authority that refuses an expired verdict with `RESOLUTION_EXPIRED`. |

### 5.4 Defects and Limitations

| ID | Severity | Status | Description | Impact |
| --- | --- | --- | --- | --- |
| `DEF-01` | Low | Resolved | The mobile `UserRole` enumeration included the retired `MAINTENANCE_ENGINEER` role. The enumeration now matches the four platform roles. | `flutter analyze` and all 58 mobile tests passed. The mobile app restricts sign-in to Customers. |
| `DEF-02` | Low | Open | The backend E2E runner script resolves its frontend root to a directory that does not exist in the workspace. | The script cannot execute as written; the connected lifecycle is verified by the integration test instead. |

Neither defect affects a delivered feature path, and neither is claimed as passing. Cases not executed in this run remain `Pending` in the workbook.

