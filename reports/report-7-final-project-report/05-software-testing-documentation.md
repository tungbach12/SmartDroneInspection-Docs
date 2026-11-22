---
title: "Report 7 - Software Testing Documentation"
document_type: report7-section
weight: 50
source: "Report7_Final Project Report.docx"
---
# V. Software Testing Documentation

## 1. Scope of Testing

Testing covers the delivered platform across the web portals, the customer mobile application, the backend, and the AI, telemetry, and payment integrations, for all twenty-four atomic product features (`FE-01`–`FE-24`) organized across the four main operational flows (`MF1`–`MF4`) and business rules `BR-01`–`BR-55`. The inspection scope is buildings only.

- **`MF1` — Identity, Partner/Drone Onboarding & Airspace Screening (`FE-01`–`FE-04`):** Customer registration, password/OTP/Google sign-in, session rotation, `/users/me` profile, bilingual localization, and four-role portal/API RBAC (`FE-01`); public partner application, admission, `inspector_profiles` licence credentials, and flight logs (`FE-02`); Admin drone document/feature config and Inspector-owned drone registration/fleet lifecycle (`FE-03`); and interactive Vietnam coordinate map and No-Fly Zone screening (`FE-04`).
- **`MF2` — Buildings, Airspace Clearance, Commercial Service & Notifications (`FE-06`–`FE-12`):** Building assets (`V66` `ownership_information`), checkpoints, and MinIO reference documents (`FE-06`); restricted-airspace customer review (`FE-07`); minimal compact service requests (`PR #139`) with concise recurring titles (`PR #164`), monthly cadence bounds/month-end anchoring, Manager claim, and VND quotations (`FE-08`); offline signed agreements, occurrence materialization, and cross-organization dispatch (`FE-09`); separated Customer–Manager Order Chat and Customer–Inspector Inspection Chat (`FE-10`); Admin-configurable Step 4 assignment acceptance timeout (`FE-11`); and Spring Modulith outbox notifications (`FE-12`).
- **`MF3` — Flight Permits, Field Telemetry, Evidence Pipeline & AI/RAG Analysis (`FE-13`–`FE-17`):** Mission flight-permit upload and independent Manager/Admin verification gate (`FE-13`); field sessions, SmartDroneHub MAVLink traces, log imports/declarations, dashboards, and calendar (`FE-14`); EXIF-first image normalization/thumbnails, duplicate auto-numbering, resumable `2 GiB` chunked MP4 upload, FFmpeg transcoding, and HMAC HTTP Range streaming (`FE-15`); YOLO11 (`70%` default per `V63`) + Vision fallback detection, filter chips, Inspector baseline confirmation, and fresh re-inspection evidence gating (`FE-16`); and tenant-isolated `DroneKnowledgeAI` local 384d `fastembed` RAG (`V64`/`V65`), single/batch AI note drafting (`Draft note with AI` / `Draft all notes`), Mobile `KnowledgeReferencesStrip`, and `ReportAiSummaryCard` references (`FE-17`).
- **`MF4` — Report Publication, Acceptance, Payment Settlement, Ledger & Re-inspection (`FE-05`, `FE-18`–`FE-24`):** Role-scoped Customer/Inspector/Manager financial history ledgers (`FE-05`); 4-state inspection report compilation, independent Manager review banning self-publication, on-demand PDF export, and `/with-reports` queues (`FE-18`); Customer report acceptance gating invoicing and clarification workflow (`FE-19`); `V29` / `V67`–`V68` Sepay VietQR and VNPay v2.1.0 checkout, webhook auditing, cancel/expiry order release, and role-masked finance projections (`FE-20`); acceptance-stamped payment deadlines, daily single overdue reminders, and payment notice/receipt PDF downloads (`FE-21`); Partner Inspector payout reconciliation (`ELIGIBLE -> PAID`, idempotency, caps) (`FE-22`); evidence-backed refunds, payout holds, legacy reconciliation, and Inspector receivable recovery (`FE-23`); and post-remediation re-inspection with three-way verdicts (`RESOLVED`, `UNRESOLVED`, `INCONCLUSIVE`), `RESOLVED` verdict expiry tracking, and Mobile parity (`FE-24`).

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
| Phùng Trung Quốc (`SE170027`) | Backend and Mobile Engineer and Tester (`FE-06`–`FE-12`) | Owns the cases and regression runs for building assets (`FE-06`), restricted-airspace clearance (`FE-07`), service requests & VND quotes (`FE-08`), signed contracts & dispatch (`FE-09`), dual chat (`FE-10`), assignment timeout (`FE-11`), and notifications (`FE-12`). |
| Trần Tùng Bách (`SE180220`) | Full-Stack and AI Engineer and Tester (`FE-13`–`FE-18`) | Owns the cases and regression runs for flight permits (`FE-13`), field telemetry (`FE-14`), evidence/chunked video pipeline (`FE-15`), YOLO11 + fallback confirmation (`FE-16`), `DroneKnowledgeAI` RAG & drafting (`FE-17`), and report publication (`FE-18`), plus backend/DB architecture & Mobile co-testing. |
| Trương Thái Như (`SE180082`) | Full-Stack Engineer and Tester (`FE-19`–`FE-24`) | Owns the cases and regression runs for customer acceptance (`FE-19`), Sepay VietQR/VNPay settlement (`FE-20`), payment deadlines/documents (`FE-21`), Inspector payouts (`FE-22`), refunds & receivables (`FE-23`), and re-inspection (`FE-24`), plus automated test reconciliation & Report 5 workbook maintenance. |
| Supervisors | Reviewers | Review the strategy, audit traceability across Reports 3–5, and evaluate defence readiness. |

### 3.2 Test Environment

| Purpose | Tool | Provider | Version |
| --- | --- | --- | --- |
| Application runtime | Java 21 with Spring Boot Modulith | Eclipse Temurin / Broadcom | `Java 21` / `4.1.0` |
| Relational database | PostgreSQL (48 application tables / 50 total, migrations `V1`–`V4`, `V60`–`V69`) | PostgreSQL Global Development Group | `17` |
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

Unit test cases live in the repository suites. On 20 Nov 2026 the backend `.\mvnw.cmd verify` exited 0 with `971` tests passed, `0` failures, Spring Modulith boundary verification passed and JaCoCo coverage checks met (prior to `PR #164` adding `V66__asset_ownership_information.sql` and `PR #166` adding `V67`–`V68`). The frontend full `npm test` ran `97` files (`93` passed, `4` skipped) and `724` tests (`720` passed, `4` skipped, `0` failed), covering the four-portal access policy, the airspace map, the calendar, evidence/findings/report screens, the re-inspection verdict-expiry warning, quick status filter chips, and `DroneKnowledgeAI` note drafting (`DraftNoteAction` / `Draft all notes`) and references; after `PR #139` and `PR #140` merged on `main`, `npm run lint` (`0` errors), `npm run build`, and `npx vitest run src/features/auth` (`11` files / `60` tests) passed. Additionally, on 21–22 Nov 2026 for `FE-20` hardening (`backend PR #166`, `frontend PR #142`), focused verification passed `99/99` backend payment tests, `40/40` frontend finance tests (`tsc --noEmit` `0` errors), and `12/12` Playwright payment checks + `10/10` DS-04a/DS-04b dry-run on PostgreSQL 17 (`V67`–`V68`). The mobile suite (`PR #27`–`PR #28`) passed `56` tests with `0` failures, covering customer-only admission, localization, verdict expiry, payment-document PDF, Inspector–Customer chat, the knowledge strip, and the customer screens. Report 5 (`v3.10`) tracks `67` active case IDs across `FE-01`–`FE-24`: all `64` historical records preserved verbatim plus `3` honest unexecuted (`N/A / Pending / Pending`) standalone breakout cases (`WF3-032` in `FE-05`, `WF2-021` in `FE-11`, `WF3-033` in `FE-22`).

Integration, system, and acceptance cases live in `Report5_Test Report.xlsx`, partitioned across twenty-four feature sheets (`Feature 1`–`Feature 24`, mapped 1-to-1 to `FE-01`–`FE-24`) with columns for the procedure, expected results, preconditions, three execution rounds, the test date, the tester, and a note recording the mode and the automated evidence.

## 5. Test Reports

### 5.1 Automated Suite Results

![Automated test inventory](assets/charts/test-inventory.png)

*Figure 7.9 — Verified automated test inventory by repository at handover.*

| Suite | Command | Scope | Result |
| --- | --- | --- | --- |
| Backend | `.\mvnw.cmd verify` | Domain, service, controller, repository, migration, storage, architecture and knowledge retrieval tests | `971` tests passed, `0` failures, `0` errors; Spring Modulith boundary verification and JaCoCo coverage gate met. `spotless:check` passed (20 Nov 2026 full verification). |
| Web portal | `npm test` / `npx vitest run src/features/auth` | Components, pages, access policy, API clients, verdict-expiry warnings, filter chips and DroneKnowledgeAI note drafting | Full suite (20 Nov 2026): `97` files (`93` passed, `4` skipped), `724` tests (`720` passed, `4` skipped), `0` failed; post-`PR #140` on `main`: `npm run lint` (`0` errors), `npm run build` exited `0`, auth Vitest `11` files / `60` tests passed. |
| Mobile | `flutter test` | Customer-only session, localization, verdict expiry, payment PDF, chat, knowledge strip and screens (`PR #27`–`PR #28`) | `56` tests passed, `0` failures; `dart format --set-exit-if-changed .` and `flutter analyze` both passed. |

### 5.2 Acceptance Case Execution

![Acceptance case execution status](assets/charts/acceptance-status.png)

*Figure 7.10 — Round 1 acceptance case status for the `67` active cases across `FE-01`–`FE-24`.*

| Feature | Total cases | Passed | Failed | Pending | N/A | Coverage focus |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| `FE-01` | 7 | 6 | 0 | 1 | 0 | Registration, OTP, Google OAuth2, sessions, profile, EN/VI i18n, and 4-role RBAC |
| `FE-02` | 4 | 3 | 0 | 1 | 0 | Partner Inspector application, non-disclosing email checks, `inspector_profiles`, and flight logs |
| `FE-03` | 3 | 3 | 0 | 0 | 0 | Admin drone checklists, owned-drone registration/renewal, photos, and serviceability states |
| `FE-04` | 3 | 3 | 0 | 0 | 0 | Interactive coordinate map, coordinate bounds validation, and hard No-Fly Zone gate |
| `FE-05` | 1 | 0 | 0 | 0 | 1 | Scoped Customer/Inspector/Manager financial history ledgers (`WF3-032`: `N/A / Pending / Pending`) |
| `FE-06` | 3 | 3 | 0 | 0 | 0 | Building registry (`V66` `ownership_information`), checkpoints, MinIO docs, and retirement lock |
| `FE-07` | 1 | 1 | 0 | 0 | 0 | Restricted-airspace onboarding queue review and mandatory rejection reason audit |
| `FE-08` | 3 | 3 | 0 | 0 | 0 | Compact requests & concise recurring titles, cadence bounds/month-end anchoring, and VND quotes |
| `FE-09` | 5 | 4 | 0 | 1 | 0 | Signed agreements, occurrence dispatch conflict/eligibility guards, abort recovery, Mobile E2E |
| `FE-10` | 1 | 1 | 0 | 0 | 0 | Separated Customer–Manager Order Chat and Customer–Inspector Inspection Chat with attachments |
| `FE-11` | 1 | 0 | 0 | 0 | 1 | Step 4 assignment acceptance timeout & escalation alert (`WF2-021`: `N/A / Pending / Pending`) |
| `FE-12` | 1 | 1 | 0 | 0 | 0 | Deduplicated Modulith `event_publication` notifications and `targetPath` safety |
| `FE-13` | 2 | 2 | 0 | 0 | 0 | Flight permit upload validation, independent review blocking self-review, and reschedule reset |
| `FE-14` | 5 | 4 | 0 | 0 | 1 | Field session start/complete/abort, MAVLink telemetry, log import, KPI dashboards, and calendar |
| `FE-15` | 5 | 1 | 0 | 0 | 4 | EXIF image normalization/thumbnails, duplicate numbering, 2 GiB chunked MP4, FFmpeg, Range tickets |
| `FE-16` | 7 | 6 | 0 | 1 | 0 | YOLO11 (`70%` default) + Vision fallback, filter chips, baseline confirmation, and fresh evidence |
| `FE-17` | 2 | 0 | 0 | 0 | 2 | Tenant-isolated `DroneKnowledgeAI` local 384d RAG, note drafting, Mobile strip, and summary refs |
| `FE-18` | 4 | 4 | 0 | 0 | 0 | Four-state report lifecycle, compilation, independent review banning self-publication, PDF export |
| `FE-19` | 1 | 0 | 0 | 1 | 0 | Customer report acceptance (`ACCEPTED`), clarification paths, and staging handoff |
| `FE-20` | 2 | 0 | 0 | 0 | 2 | Normalized `V29`/`V67`–`V68` finance schema, Sepay VietQR & VNPay HMAC webhooks, and masked views |
| `FE-21` | 2 | 0 | 0 | 2 | 0 | Payment due deadline (`payment_due_at`), single overdue reminder, and notice/receipt PDF |
| `FE-22` | 1 | 0 | 0 | 0 | 1 | Partner Inspector payout reconciliation (`ELIGIBLE -> PAID`, idempotency; `WF3-033`: `N/A / Pending / Pending`) |
| `FE-23` | 1 | 0 | 0 | 1 | 0 | Refund initiation holds, exact allocation, legacy reconciliation, and Inspector receivables |
| `FE-24` | 2 | 0 | 0 | 1 | 1 | Post-remediation re-inspection verdicts (`RESOLVED`/`UNRESOLVED`/`INCONCLUSIVE`) & Mobile parity |
| **Total** | **67** | **45** | **0** | **9** | **13** | All twenty-four atomic features (`64` historical + `3` unexecuted standalone cases) |

The Round 1 inventory recorded `45` passed and `0` failed cases across `67` active cases: `9` pending and `13` N/A (`45/54 = 83.33%` Round 1 coverage). The `13` N/A rows comprise `10` post-Round-1 additions (`WF3-018`–`WF3-020`, `WF3-022`–`WF3-025`, `WF3-029`–`WF3-031`) plus `3` newly unbundled standalone breakout cases (`WF3-032` in `FE-05`, `WF2-021` in `FE-11`, `WF3-033` in `FE-22`) kept honestly at `N/A / Pending / Pending`. Historical Round 1 remains unchanged (`45 Passed / 0 Failed / 8 Pending / 3 N/A = 56` cases).

Report 5 records `13` executed Round 3 cases with `0` failures: `WF3-005`, `WF3-006`, `WF3-009`, `WF3-016`, `WF3-018`, `WF3-019`, `WF3-021`, `WF3-026`, `WF3-027`, `WF3-028`, `WF3-029`, `WF3-030` and `WF3-031`; `WF3-020`, `WF3-022`–`WF3-025`, `WF3-032`, `WF2-021`, and `WF3-033` remain Pending. `PaymentDueAndDocumentApiIntegrationTest` supplies the connected-HTTP evidence for `WF3-026`/`WF3-027`; `WF3-028` records fresh re-inspection evidence, `WF3-019` the current payout contract, and `WF3-029`–`WF3-031` the `DroneKnowledgeAI` retrieval, advisory summary references and Customer Mobile parity.

### 5.3 Cross-Cutting Assertions

| Assertion | Test | What it proves |
| --- | --- | --- |
| Schema baseline is exact | `FullDatabaseSchemaMigrationTest` | The applied migration set is `V1`–`V4` and `V60`–`V69` (`["1","2","3","4","60","61","62","63","64","65","66","67","68","69"]`); the inventory is 50 relations in `public` (48 application tables, the `event_publication` outbox and `flyway_schema_history`), with 47 JPA runtime entity tables including `assets.ownership_information`, `service_payments.gateway_order_created_at`, `gateway_inbound_transactions`, `inspection_flight_permits`, and `field_session_telemetry`. |
| Module boundaries hold | `ModulithArchitectureTest` | No module reaches another outside its declared `allowedDependencies`. |
| Lifecycle is connected | `ConnectedMainFlowE2eIntegrationTest` | Onboarding, building and drone registration, request and quotation, dispatch, evidence and detection, publication, and settlement execute in one run. |
| A report author cannot publish | Reviewer-scope and role-policy tests | Publication requires a reviewer who is not the author. |
| A permit uploader cannot verify | Permit review tests | Verification requires a distinct manager or administrator. |
| Media is scoped | Evidence ticket tests | A signed ticket grants access to one evidence record and nothing else. |
| Payment needs a signature | `SepayWebhookControllerTest`, `VnPayWebhookAndGatewayTest` & webhook tests | A browser redirect alone never settles a payment; missing/forged `Authorization: Apikey` or VNPay HMAC-SHA512 signatures are rejected, while Sepay outcomes persist idempotently in `gateway_inbound_transactions`. |
| Knowledge retrieval & note drafting are tenant-isolated | `HistoricalCaseServiceTest`, `HistoricalCaseApiIntegrationTest`, `InspectionFindingsPage.test.tsx`, `KnowledgeRecommendationPanel.test.tsx`, `knowledge_recommendation_test.dart` | `DroneKnowledgeAI` returns `PGVECTOR_RAG` via local `fastembed` (`vector(384)`) when embeddings exist and deterministic `HYBRID_MATCH` otherwise, plus `AI_VISION_RAG` for note drafting; benchmark cases are anonymized, cross-organization cases and the current inspection are excluded, and the customer mobile strip hides when empty. |
| Payment deadline and documents over HTTP | `PaymentDueAndDocumentApiIntegrationTest` | On Testcontainers PostgreSQL 17 and the real security filter chain: acceptance stamps `payment_due_at` once, the document endpoint returns `409` before acceptance, a notice PDF after acceptance and a receipt after verified payment, foreign-organization callers receive `404`, and a repeated overdue scan sends no second reminder. Report 5 records this as the Round 3 Passed evidence for `WF3-026` and `WF3-027`. |
| Expired re-inspection verdict is surfaced early | `verdictExpiry.ts`, `VerdictExpiryBanner`, `ValidityNotice`, `ReinspectionWorkflow.test.tsx` | The Web client distinguishes lapsed `RESOLVED` verdicts from those lapsing within 14 days and warns before report authoring; the backend remains the authority that refuses an expired verdict with `RESOLUTION_EXPIRED`. |

### 5.4 Defects and Limitations

| ID | Severity | Status | Description | Impact |
| --- | --- | --- | --- | --- |
| `DEF-01` | Low | Open | The mobile `UserRole` enumeration still parses the retired `MAINTENANCE_ENGINEER` role. | Harmless at runtime because the session gate admits `CUSTOMER` only, but the stale member should be removed. |
| `DEF-02` | Low | Open | The backend E2E runner script resolves its frontend root to a directory that does not exist in the workspace. | The script cannot execute as written; the connected lifecycle is verified by the integration test instead. |

Neither defect affects a delivered feature path, and neither is claimed as passing. Cases not executed in this run remain `Pending` in the workbook.

