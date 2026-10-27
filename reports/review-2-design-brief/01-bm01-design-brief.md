---
title: "SWP490 Review 2 - BM01 Design Brief"
document_type: review2-bm01
version: "1.0"
date: "2026-10-27"
project_code: "GFA26SE139"
group_name: "FA26SE112"
---

# I. BM01 – Design Brief (Sections 0–8)

## 0. Header

| Field | Value |
| --- | --- |
| **Project Code & Name** | `GFA26SE139` — SmartDroneInspection: AI-powered Infrastructure Inspection Management Platform |
| **Group Name & Members** | `FA26SE112` — Trần Hoàng Trung Hiếu (`SE184212`, Leader), Phùng Trung Quốc (`SE170027`), Trương Thái Như (`SE180082`), Trần Tùng Bách (`SE180220`) |
| **Supervisors (GVHD)** | Phạm Minh Trí (`tripm14@fpt.edu.vn`), Đặng Ngọc Minh Đức (`ducdnm2@fpt.edu.vn`) |
| **Repository & Tag (`review-2`)** | `https://github.com/tungbach12/SmartDroneInspection-Backend` (`-Frontend`, `-Mobile`, `-Docs` @ tag `review-2`) |
| **Staging URL** | `https://smartdroneinspection.duckdns.org` |
| **Document Version & Date** | `Version 1.0` — `2026-10-27` |

---

## 1. Scope

### 1.1 Summary of Changes vs. Registration Form v1.0 (Details in BM03)
- **Self-Contained Enterprise Inspection, Drone Equipment Leasing & Airspace Advisory**: Replaced external `SmartDroneHub` dependency with an internal multi-tenant enterprise subscription model (`subscriptions`, `payment_transactions`), platform leasable drone pool (`platform_drones`), drone equipment lease contracts (`drone_leases`), customer owned/leased fleet (`drones`), timezone-anchored recurring schedules (`recurring_inspection_schedules`, `schedule_occurrences`), interactive Vietnam Airspace & No-Fly Zone Map (`AirspaceNoFlyMap` / `AirspaceAdvisoryCard`), and a self-service aviation flight permit upload gate (`Ready for Flight`).
- **Five-Role Governance Model**: Refined human roles to `Platform Admin (ADMIN)`, `Platform Manager`, `Organization Manager`, `Inspector`, and `Maintenance Engineer` with strict separation of duties (Platform Admin and Platform Manager single-role separation; independent report and maintenance reviewers).
- **Java 21 / Spring Boot 4.1.0 & Concrete Engineering AI**: Standardized backend on `Spring Boot 4.1.0 + Spring Modulith 2.1.1 + PostgreSQL 17 (pgvector) + MinIO` and grounded AI into three human-in-the-loop services: (1) Self-hosted FastAPI `YOLO11 (MBDD2025)` defect detection, (2) Context-grounded `LLM Report Drafting`, and (3) `pgvector` `RAG Maintenance Scope Advisor` (`TCVN 9343:2012`, `EN 1504-9`, `ISO 12944-5`).

### 1.2 Explicitly Out of Scope (What We Will Not Do & Why)
1. **Real-Time Drone Flight Control & Hardware Autopilot Telemetry**: Physical UAV piloting and radio-control actuation are safety-critical hardware operations regulated under Decree No. 288/2025/NĐ-CP (`BR-16`); the platform governs mission compliance, field session logs, evidence, AI analysis, and engineering remediation.
2. **Autonomous AI Approval or Unreviewed Publication**: AI vision and LLM outputs are strictly advisory (`Pending` findings / `Draft` report sections) and never auto-publish reports or auto-approve repair budgets (`BR-20`, `BR-27`).
3. **External SMTP Email & Native OS Push (APNs/FCM)**: Operational alerts are delivered through the deduplicated in-app notification inbox (`/api/v1/notifications` + Spring Modulith transactional outbox `event_publication`).

---

## 2. System at a Glance (130 Words)

**SmartDroneInspection** is a multi-tenant Enterprise Inspection and Drone Equipment Leasing platform designed for infrastructure-owning enterprises (bridge authorities, power utilities, industrial operators) to digitize the complete structural inspection-to-maintenance lifecycle. Platform Managers govern tenant subscriptions and lease serial-numbered drones into customer fleets. Organization Managers register infrastructure assets with standardized checkpoints, schedule one-off or recurring drone missions with conflict detection, approve immutable PDF inspection reports, and control maintenance budgets. Field Inspectors use the Flutter mobile app and Web portal to evaluate Vietnam no-fly zone advisories, upload flight permits, log on-site survey sessions, ingest EXIF-geotagged aerial imagery into MinIO, run YOLO11 computer vision defect detection, verify findings, and draft reports. Maintenance Engineers use the `pgvector` RAG Scope Advisor to plan repair tasks, submit cost estimates, log verified repairs, and complete independent technical acceptance *(see SDD §1.1 System Architecture)*.

---

## 3. Key Design Decisions (Exactly 5 Decisions)

| # | Options Considered | Chosen Option | Rationale | Owner |
| :---: | --- | --- | --- | :---: |
| 1 | (A) Distributed microservices per domain vs. (B) **Spring Modulith 2.1.1 Modular Monolith + Isolated FastAPI YOLO11 Container** | **Option B**: 9 Spring Modulith modules in one JVM + separate Python FastAPI `YOLO11` container | Enforces strict compile-time module boundaries (`ModulithArchitectureTest`) and ACID transactions across the 30 PostgreSQL tables while isolating heavy PyTorch/Ultralytics CPU inference in its own container. | **Trần Tùng Bách** |
| 2 | (A) 38-table multi-step preparation & admin readiness review vs. (B) **Streamlined 30-Table Schema (`V1`–`V5`) with Airspace Map & Self-Service Permit Gate** | **Option B**: Direct Inspector + Drone dispatch + Haversine Airspace Map + Self-Service Permit Upload (`Assigned -> Ready for Flight`) | Eliminated 8 redundant intermediary tables (`V3`), stored `inspection_items` checkpoints on `assets`, and automated flight readiness upon verified permit upload and unexpired pilot license check (`BR-05`, `BR-15`). | **Phùng Trung Quốc** |
| 3 | (A) Auto-running cloud vision on every upload vs. (B) **Inspector-Invoked Self-Hosted `YOLO11 (MBDD2025)` + Opt-In Vision Fallback + Snapshot Hash Gate** | **Option B**: On-demand `PrimaryWithFallbackInference` + confirmed findings baseline lock | Gives Inspectors full control over inference (`1.4 s` local YOLO11 latency, zero external image leakage by default) and binds `Report Draft` versions to the confirmed findings set (`409 Report Snapshot Stale` on drift). | **Trần Tùng Bách** |
| 4 | (A) Free-form LLM maintenance prompting vs. (B) **`pgvector` RAG Scope Advisor (`repair_knowledge_chunks`) + `DeterministicScopeFallback`** | **Option B**: Standards-grounded RAG (`TCVN 9343:2012`, `EN 1504-9`, `ISO 12944-5`) with deterministic fallback | Grounds corrective scope, acceptance criteria, and suggested tasks in official civil engineering standards and guarantees `100%` availability even when external LLM endpoints are offline. | **Trương Thái Như** |
| 5 | (A) Browser-trusted payment callbacks vs. (B) **Dual Enterprise Settlement (Platform Manager Wire Confirmation + Server-Captured PayPal Orders v2 & Signed Webhooks)** | **Option B**: Server-to-server PayPal Orders v2 capture/webhook verification + offline wire reconciliation | Prevents client-side price/capture spoofing (`BR-10`, `BR-11`), supports enterprise wire workflows when `PAYPAL_ENABLED=false`, and enforces Platform Admin and Platform Manager single-role separation separation of duties. | **Trần Hoàng Trung Hiếu** |

---

## 4. Top Risks (Exactly 3 Risks)

| # | Design Risk | Potential Impact | Verification & Mitigation Mechanism |
| :---: | --- | --- | --- |
| 1 | **AI Vision / LLM Service Unavailability or Hallucinated Outputs** | Could block field defect logging, report drafting, or work order scope planning if workflows hard-depend on AI availability or accept unverified outputs. | **Mitigation**: All AI outputs are advisory (`Pending` / `Draft`); manual finding creation (`POST /findings`), manual structured report drafting (`/report/draft/manual`), and `DeterministicScopeFallback` work 100% offline. **Verified by**: `WF3-005`, `WF3-007`, `WF4-002`. |
| 2 | **Cross-Tenant Data Leakage or Separation-of-Duties Bypass in Multi-Role Workflows** | A tenant could read/mutate another organization's assets/reports, or an author/team lead could self-approve reports, budgets, or work acceptance. | **Mitigation**: Composite tenant FKs `(id, organization_id)` in PostgreSQL 17, `@PreAuthorize` + service-level tenant scoping, Platform Admin and Platform Manager single-role separation, and distinct `reviewerUserId` / `budgetApproverUserId` / `acceptingReviewerUserId` guards. **Verified by**: `WF1-003`, `WF1-005`, `WF1-007`, `WF3-006`, `WF4-007`, `WF4-013`. |
| 3 | **Calendar Drift & Resource Double-Booking in Recurring Inspection Schedules** | Naive month addition shifts 31st-of-month schedules permanently after February, and concurrent schedulers could create duplicate inspections. | **Mitigation**: Original-anchor local timezone arithmetic with month-end clamping (`RecurringInspectionSchedule`), unique `(schedule_id, occurrence_index)` constraint, and explicit `Blocked` occurrences on resource conflict. **Verified by**: `WF1-017`, `WF1-018`, `WF1-019`, `WF2-002`. |

---

## 5. Known Gaps (Synchronized with BM02 Self-Review Report)

| Gap ID | Source (`BM02`) | Description of Gap across Registration / SRS / SDD / Code | Resolution Plan, Owner & Target Deadline |
| :---: | :---: | --- | --- |
| `GAP-01` | `SR-08` (`Medium`) | **4 Pending Manual Staging/Mobile Test Cases (`WF1-010`, `WF2-015`, `WF3-012`, `WF4-011`)**: 60/64 (`93.75%`) functional test cases in Report 5 are `Passed`; 4 staging/mobile edge walkthroughs remain `Pending`. | Execute live staging walkthroughs on `smartdroneinspection.duckdns.org` and record Round 2 `Passed` evidence in Report 5. **Owners**: Hiếu (`WF1-010`), Quốc (`WF2-015`), Bách (`WF3-012`), Như (`WF4-011`) — **Deadline: `2026-11-15`**. |
| `GAP-02` | `SR-09` (`Medium`) | **Mobile In-App Notification Inbox UI Slice**: Backend `/api/v1/notifications` and Web notification bell/inbox are complete (`602/602` Vitest green), but Flutter mobile app does not yet expose the notification inbox screen. | Add `NotificationsPage` and unread badge polling in `SmartDroneInspection-mobile` consuming `/api/v1/notifications`. **Owner**: **Trần Hoàng Trung Hiếu** — **Deadline: `2026-11-12`**. |
| `GAP-03` | `SR-10` (`Low`) | **Unrouted Legacy Frontend Files**: `AssetReviewPage.tsx`, `InspectionSchedulesPage.tsx`, and `ScheduleProposalsPage.tsx` are disabled in `accessPolicy.ts` (`[]` roles) and superseded by `AssetsPage.tsx` and `RecurringSchedulesPage.tsx`. | Delete unrouted legacy files and keep `npm test` + `npm run build` green. **Owner**: **Trần Hoàng Trung Hiếu** — **Deadline: `2026-11-05`**. |

---

## 6. Mandatory Features (`FE-01` to `FE-12` — 3 Features per Member)

| ID | Feature Name (`SRS §3.2–3.13`) | Testable Acceptance Criteria (Pass / Fail) | Report 5 Test Cases (`64` Total) | Owner |
| :---: | --- | --- | --- | :---: |
| `FE-01` | **Authentication & Access Control** (§3.2) | `POST /auth/register` with active Terms/Privacy consent creates `Active` `Organization` + `Organization Manager` and `Organization Registration` audit row; enforces Argon2id/JWT/CSRF, IP rate-limit (`10 req/60s`), and Platform Admin and Platform Manager single-role separation (`403` on cross-role call). | `WF1-001` to `WF1-005` (`5` TCs on `Feature 1`) | **Trần Tùng Bách** |
| `FE-02` | **Workforce & Subscription Management** (§3.3) | `Organization Manager` provisions `Inspector`/`Maintenance Engineer`; `Inspector` self-declares pilot license; `Platform Manager` wire confirmation or verified PayPal capture activates `Subscription` (`Pending -> Active`, max 1 active per org). | `WF1-006` to `WF1-010` (`5` TCs on `Feature 2`) | **Trần Hoàng Trung Hiếu** |
| `FE-03` | **Asset & Drone Fleet Management** (§3.4) | `Organization Manager` creates `Asset` with unique `asset_code`, GPS, and `inspection_items` checkpoints, uploads reference engineering documents to MinIO, retires assets (`Retired`), and leases drones from `platform_drones` (`Pending -> Active -> Reclaimed`). | `WF1-011` to `WF1-016` (`6` TCs on `Feature 3`) | **Trần Hoàng Trung Hiếu** |
| `FE-04` | **Recurring Schedule & Notifications** (§3.5) | `POST /inspection-schedules` (`Week`/`Month`/`Year`) generates rolling 14-day `Generated` occurrences (or `Blocked` with retry/skip) without month-end drift, and dispatches deduplicated in-app notifications (`Sent -> Read`). | `WF1-017` to `WF1-021` (`5` TCs on `Feature 4`) | **Trần Hoàng Trung Hiếu** |
| `FE-05` | **Mission Dispatch & Airspace Advisory** (§3.6) | `POST /api/v1/inspections` assigns active `Inspector` and `Active` `Drone` (`Assigned`) and rejects overlapping time windows (`409`); `/api/v1/airspace/evaluate` classifies coordinates into `No-Fly Zone`, `Restricted Zone`, or `Clear Zone` (`MSG28`). | `WF2-001` to `WF2-005` (`5` TCs on `Feature 5`) | **Phùng Trung Quốc** |
| `FE-06` | **Flight Readiness & Field Execution** (§3.7) | Assigned `Inspector` with valid pilot license uploads permit (`Assigned -> Ready for Flight`) and starts (`-> In Progress`), postpones (`Postponed`), or completes (`-> Field Completed`) field sessions on Web and Flutter Mobile. | `WF2-008`, `009`, `011`, `012`, `015`, `016` (`6` TCs on `Feature 6`) | **Phùng Trung Quốc** |
| `FE-07` | **Operational Dashboard & Schedule Calendar** (§3.8) | Renders role-scoped KPIs, server-paged `/inspections` and `/with-reports` queues, Month/Week/Agenda `InspectorScheduleCalendar`, Enterprise Dark Mode, and bilingual (EN/VI) localization. | `WF3-009`, `WF2-017` to `WF2-020` (`5` TCs on `Feature 7`) | **Phùng Trung Quốc** |
| `FE-08` | **Evidence Management & AI Defect Detection** (§3.9) | `POST /evidence` stores valid images in MinIO with EXIF GPS/time extraction and rejects duplicate filenames (`409`); `POST /analyze` runs `YOLO11 (MBDD2025)` returning `Pending` boxes; `Inspector` confirms findings and locks `findings_snapshot_hash` (`Report Draft`). | `WF3-002`, `003`, `001`, `004`, `007`, `010` (`6` TCs on `Feature 8`) | **Trần Tùng Bách** |
| `FE-09` | **Inspection Reporting & Publication** (§3.10) | `Inspector` generates LLM/manual draft (`Draft -> Author Verified -> Submitted`); independent `Organization Manager` approves and publishes immutable A4 PDF to MinIO (`Published`, `Report Published`) and forwards findings (`Repair Pending` / `Completed`). | `WF3-005`, `006`, `008`, `012`, `016` (`5` TCs on `Feature 9`) | **Trần Tùng Bách** |
| `FE-10` | **Maintenance Planning & AI Scope Advisory** (§3.11) | `Organization Manager` creates `MaintenanceWorkOrder` (`Draft`) from forwarded finding and assigns `Team Lead`, `Report Author`, and independent `acceptingReviewerUserId`; `Maintenance Engineer` uses `pgvector` RAG Scope Advisor (`TCVN`/`EN`/`ISO` + fallback) and plans tasks. | `WF4-001` to `WF4-005` (`5` TCs on `Feature 10`) | **Trương Thái Như** |
| `FE-11` | **Cost Estimation & Repair Execution** (§3.12) | Team submits itemized estimate (`-> Awaiting Approval`), `Organization Manager` approves (`-> Approved`) and governs Change Orders; team releases (`Ready`), starts (`In Progress`), Lead-verifies `MaintenanceWorkLog`s (`Verified`), and declares complete (`Work Completed`). | `WF4-006` to `WF4-011` (`6` TCs on `Feature 11`) | **Trương Thái Như** |
| `FE-12` | **Maintenance Acceptance & Cost Closure** (§3.13) | `Report Author` submits completion report (`Submitted for Acceptance`); independent `Organization Manager` records `Accepted` (rendering completion PDF) or `REWORK`/`REINSPECTION`, reconciles `Actual` costs (`Cost Reconciled`), and closes (`Closed`). | `WF4-012` to `WF4-016` (`5` TCs on `Feature 12`) | **Trương Thái Như** |

---

## 7. Non-Functional Requirements (Max 6 Rows)

| ID | Category | Metric | Threshold | Measurement Method & Verification Case |
| :---: | --- | --- | --- | --- |
| `NFR-01` | **API Performance** | 95th percentile (`p95`) HTTP response latency & 5xx error rate for standard JSON REST APIs under 50 concurrent users. | `p95 <= 2,000 ms` & `0%` 5xx errors over 60s window. | Automated concurrent API probe against containerized Spring Boot 4.1 + PostgreSQL 17 (`WF2-016`). |
| `NFR-02` | **AI Inference Latency** | End-to-end single-image defect detection latency (`POST /evidence/{id}/analyze`, JPEG up to `10 MB`). | `<= 5,000 ms` on CPU container (`~1.4 s` measured on `mbdd2025-v1`). | Automated `YoloInferenceClientTest` & live container `/predict` timing (`WF3-007`). |
| `NFR-03` | **Multi-Tenant & RBAC Security** | Cross-tenant and unauthorized role access rejection rate across all 22 REST controllers and 3 web portals. | `100%` rejected with `403 Forbidden` or `404 Not Found` (`0` data leaks). | Automated Spring Security Testcontainers & Vitest route guard suites (`WF1-005`). |
| `NFR-04` | **Auth & Rate-Limit Security** | Consecutive failed login lockout count, per-IP auth POST rate limit, and Argon2id + refresh token rotation. | Lockout at `5` failed logins (`15m`); `11th` req/`60s` rejected (`429`); replayed token rejected (`401`). | Automated `PasswordPolicyTest`, `AuthRateLimitFilter` & session rotation tests (`WF1-004`). |
| `NFR-05` | **Report & Document Immutability** | Post-publication edit rejection rate and PDF archival availability for published Inspection and Maintenance reports. | `100%` of published PDFs readable from storage; `100%` of post-publish edits rejected (`409`). | Automated `AssetDocumentApiIntegrationTest`, `InspectionReportSectionsApiIntegrationTest` & `MaintenanceReportRendererTest` (`WF3-016`). |
| `NFR-06` | **Modularity & CI Automation** | Spring Modulith cycle/visibility violations, backend JaCoCo coverage, and Report 5 CI test automation ratio. | `0` Modulith violations; `>= 80%` JaCoCo coverage; `>= 50%` TCs automated (`87.50%` actual). | GitHub Actions `ci.yml` (`./mvnw -B verify` `850` tests, Vitest `602` tests, Flutter `20` tests — `WF4-005`). |

---

## 8. Ownership Map (1 Row per Team Member — Verified against Git History)

| Member (Code & Role) | Owned Subsystems & Modules (3 Features / 6 Functions) | Owned Mandatory Features | Owned Main Workflow | Committed Test Cases (`64` Total) |
| --- | --- | :---: | :---: | :---: |
| **Trần Hoàng Trung Hiếu** (`SE184212` — Leader) | **1.** `workforce` & `subscriptions` (Workforce, Pilot Licenses, Enterprise Plans, Wire & PayPal Orders v2)<br>**2.** `assets` (Asset Catalog, Checkpoints, Reference Documents, Owned Drones & Drone Equipment Leasing)<br>**3.** `inspections` Recurrence (`RecurringInspectionSchedulerJob`) & `notifications` Outbox Inbox | `FE-02`, `FE-03`, `FE-04` | **`WF-01`**: Enterprise Onboarding, Drone Equipment Leasing & Recurring Schedule Setup | **`16` TCs** (`WF1-006` to `WF1-021` on `Feature 2, 3, 4`: `15 Passed`, `1 Pending`; `14 Auto`, `2 Manual`) |
| **Phùng Trung Quốc** (`SE170027` — Member) | **1.** `inspections` Dispatch, Conflict Engine & `AirspaceAdvisoryService` (`AirspaceNoFlyMap` / `AirspaceAdvisoryCard`)<br>**2.** Self-Service Flight Permit Upload Gate (`Ready for Flight`) & On-Site `FieldSession`s (Web & Mobile)<br>**3.** `dashboard` Analytics, `InspectorScheduleCalendar`, Dark Mode & EN/VI Localization | `FE-05`, `FE-06`, `FE-07` | **`WF-02`**: Mission Dispatch, Airspace Check, Flight Permit Gate & Field Execution | **`16` TCs** (`WF2-001`–`005`, `008`, `009`, `011`, `012`, `015`–`020`, `WF3-009` on `Feature 5, 6, 7`: `15 Passed`, `1 Pending`; `14 Auto`, `2 Manual`) |
| **Trần Tùng Bách** (`SE180220` — Member) | **1.** `users` Authentication, Argon2id, JWT/Refresh Cookie, CSRF/Rate-Limit & 5-Role RBAC (`RolePolicy`)<br>**2.** `Evidence` Intake (EXIF/MinIO), FastAPI `YOLO11 (MBDD2025)` Detection & `Finding` Snapshot Lock<br>**3.** LLM/Manual `InspectionReport` Authoring, OpenHTMLtoPDF Publication (`Published`) & Corrective Handoff | `FE-01`, `FE-08`, `FE-09` | **`WF-03`**: Evidence Intake, AI Defect Verification, Report Publication & Handoff | **`16` TCs** (`WF1-001`–`005`, `WF3-001`–`008`, `010`, `012`, `016` on `Feature 1, 8, 9`: `15 Passed`, `1 Pending`; `14 Auto`, `2 Manual`) |
| **Trương Thái Như** (`SE180082` — Member) | **1.** `maintenance` Work Orders, `pgvector` RAG Scope Advisor (`TCVN`/`EN`/`ISO` + Fallback) & Team/Task Planning<br>**2.** Itemized Cost Estimates (`Estimate`), Change Orders & Web/Mobile Task `MaintenanceWorkLog` Verification<br>**3.** `MaintenanceReportVersion` PDF, Independent Acceptance (`Accepted`/`REWORK`/`REINSPECTION`) & Cost Closure | `FE-10`, `FE-11`, `FE-12` | **`WF-04`**: Maintenance Work Order, RAG Estimation, Field Repair, Acceptance & Closure | **`16` TCs** (`WF4-001` to `WF4-016` on `Feature 10, 11, 12`: `15 Passed`, `1 Pending`; `14 Auto`, `2 Manual`) |
