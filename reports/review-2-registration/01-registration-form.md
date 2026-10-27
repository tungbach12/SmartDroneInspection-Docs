---
title: "SWP490 Review 2 - Capstone Project Registration Form (Proposed Final v2.0)"
document_type: review2-registration
version: "2.0"
date: "2026-10-27"
project_code: "GFA26SE139"
group_name: "FA26SE112"
---

# I. Capstone Project Registration Form (Version 2.0)

| Field | Value |
| --- | --- |
| **Document Code** | `SWP490_GFA26SE139_R2_Registration` |
| **Version** | `2.0 (Proposed Final at Review 2)` |
| **Effective Date** | `2026-10-27` |
| **Class / Group Name** | `FA26SE112` |
| **Project Code** | `GFA26SE139` |
| **Duration Time** | `From 09/2026 to 03/2027` |
| **Profession & Specialty** | `Software Engineering (SE)` |
| **Kind of Person Making Register** | `Lecturer & Students` |

## 1. Register Information for Supervisors

| No. | Full Name | Phone | E-Mail | Title |
| :---: | --- | --- | --- | --- |
| 1 | Phạm Minh Trí | — | `tripm14@fpt.edu.vn` | Giảng viên (Supervisor) |
| 2 | Đặng Ngọc Minh Đức | — | `ducdnm2@fpt.edu.vn` | Giảng viên (Co-Supervisor) |

## 2. Register Information for Students

| No. | Full Name | Student Code | Phone | E-Mail | Role in Group |
| :---: | --- | :---: | :---: | --- | :---: |
| 1 | Trần Hoàng Trung Hiếu | `SE184212` | `0963832382` | `hieuthtse184212@fpt.edu.vn` | Leader |
| 2 | Phùng Trung Quốc | `SE170027` | `0896986551` | `quocptse170027@fpt.edu.vn` | Member |
| 3 | Trương Thái Như | `SE180082` | `0328416716` | `nhuttse180082@fpt.edu.vn` | Member |
| 4 | Trần Tùng Bách | `SE180220` | `0378351050` | `bachttse180220@fpt.edu.vn` | Member |

## 3. Register Content of Capstone Project

### 3.1. Capstone Project Name
- **3.1.1. English**: `SmartDroneInspection: AI-powered Infrastructure Inspection Management Platform`
- **3.1.2. Vietnamese**: `SmartDroneInspection: Nền tảng Quản lý Kiểm tra Hạ tầng bằng Drone tích hợp AI`

### 3.2. Main Proposal Content (Including Result and Product)

#### a) Context
Infrastructure assets such as bridges, commercial buildings, roads, transmission towers, solar farms, wind turbines, and industrial facilities require periodic structural inspections to ensure operational safety, regulatory compliance, and timely maintenance remediation. Traditional manual inspection processes are labor-intensive, fragmented across spreadsheets and paper checklists, and hazardous for field personnel.

While commercial drones allow organizations to capture high-resolution aerial imagery efficiently, infrastructure-owning enterprises still lack a centralized, multi-tenant Software-as-a-Service (SaaS) platform that governs the complete enterprise lifecycle: tenant subscription & B2B drone leasing, asset checkpoint registration, aviation flight-permit readiness gates, field flight session logging, AI-assisted defect detection with mandatory human verification, certified PDF inspection reporting, and engineering maintenance work orders with itemized budget and acceptance controls.

Furthermore, physical aircraft flight control (RC telemetry and autopilot execution) must remain strictly separated from enterprise business governance. **SmartDroneInspection** is engineered as a multi-tenant Enterprise SaaS & B2B Drone Leasing platform that manages the end-to-end inspection and maintenance lifecycle across Web and Mobile clients while enforcing human-in-the-loop accountability over AI computer vision and generative language models.

#### b) Proposed Solutions
**SmartDroneInspection** is architected as a modular, multi-tenant business and engineering governance platform rather than a real-time aircraft flight controller. It isolates platform governance from customer enterprise workspaces across **five distinct human roles**:

**Human Actors (5 Roles across 2 Governance Zones)**
- **Platform Admin (`Platform Admin` — Platform Zone)**: Governs technical platform administration, provisions platform accounts (`Platform Admin`, `Platform Manager`) and customer workspace managers (`Organization Manager`), maintains the global infrastructure asset category catalog (`asset_categories`), and reviews platform-wide security/audit logs (`audit_events`). Enforces strict single-role separation of duties (Platform Admin and Platform Manager single-role separation).
- **Platform Manager (`Platform Manager` — Platform Zone)**: Governs commercial enterprise SaaS subscriptions (`subscriptions`, `payment_transactions`), reconciles corporate wire or PayPal Orders v2 payments, manages the platform's serial-numbered leasable drone pool (`platform_drones`), approves and provisions B2B drone lease contracts (`drone_leases`) into customer fleets, and reclaims leased drones upon contract expiration.
- **Organization Manager (`Organization Manager` — Customer Enterprise Zone)**: Registers and administers the customer organization workspace; requests Enterprise subscriptions (1, 6, 12, or custom 1–120 months) and B2B drone leases; provisions workforce accounts (`Inspector`, `Maintenance Engineer`); registers owned/leased drones (`drones`) and infrastructure assets (`assets`, `asset_documents`) with standardized inspection checkpoints (`inspection_items`); schedules one-off (`inspections`) and recurring inspection schedules (`recurring_inspection_schedules`, `schedule_occurrences`) with direct Inspector + Drone conflict checking; reviews and publishes immutable PDF inspection reports (`inspection_reports`); forwards confirmed defects to maintenance; approves repair estimates and change orders; and performs independent technical work acceptance (`maintenance_acceptance_decisions`), cost reconciliation, and work order closure (`maintenance_work_orders`).
- **Inspector (`Inspector` — Customer Enterprise Zone)**: Self-declares remote pilot license credentials (`pilot_license_*`); uploads mission-specific aviation flight permits (`Ready for Flight` operational gate); executes on-site field flight sessions (`field_sessions`) via Web or Flutter Mobile app; uploads aerial photographic evidence (`evidence`) with EXIF GPS/capture-time extraction; triggers advisory YOLO11 defect detection; verifies, edits, or manually records findings (`findings`); confirms the official findings baseline; and authors, verifies (`Author Verified`), and submits structured inspection report drafts (`inspection_reports`).
- **Maintenance Engineer (`Maintenance Engineer` — Customer Enterprise Zone)**: Participates in corrective maintenance work orders as designated `Team Lead`, `Report Author`, or `Team Member` (`maintenance_team_members`); uses the RAG-assisted Maintenance Scope Advisor (`repair_knowledge_chunks`); decomposes repair tasks (`maintenance_tasks`); prepares itemized cost estimates (`maintenance_estimate_versions`, `maintenance_cost_lines`); logs field repair execution (`maintenance_work_logs`) and change orders (`maintenance_change_orders`); and authors/verifies maintenance completion reports (`maintenance_reports`).

**Twelve Core Product Features (`FE-01` to `FE-12` — 2 Functions per Feature = 24 Functions, 3 Features per Member)**
1. **`FE-01` — Authentication & Access Control** *(Owner: Trần Tùng Bách)*: Organization self-registration with active Terms/Privacy consent, Web/Mobile Argon2id sign-in, HS256 JWT + HmacSHA256 refresh token rotation, CSRF & IP rate limiting (`10 req/60s`), and 5-role RBAC separation of duties (Platform Admin and Platform Manager single-role separation).
2. **`FE-02` — Workforce & Subscription Management** *(Owner: Trần Hoàng Trung Hiếu)*: Platform user administration, customer workforce provisioning (`Inspector`, `Maintenance Engineer`), Inspector remote pilot license self-declaration, and Enterprise Subscription billing (`1..120` months via Corporate Wire & PayPal Orders v2 + signed Webhooks).
3. **`FE-03` — Asset & Drone Fleet Management** *(Owner: Trần Hoàng Trung Hiếu)*: Global asset categories, tenant infrastructure assets with GPS coordinates and standardized inspection checkpoints (`inspection_items`), reference engineering documents in MinIO, asset retirement archival, owned drone inventory, and B2B Platform Drone Leasing (`platform_drones` → `drone_leases` → `drones`).
4. **`FE-04` — Recurring Schedule & Notifications** *(Owner: Trần Hoàng Trung Hiếu)*: Timezone-anchored recurring inspection schedules (`Week`, `Month`, `Year`), rolling 14-day occurrence generation, `Blocked` occurrence retry/skip, 3-day advance reminders, and deduplicated event-driven in-app notifications (`notifications` + `event_publication` outbox).
5. **`FE-05` — Mission Dispatch & Airspace Advisory** *(Owner: Phùng Trung Quốc)*: One-off inspection mission scheduling with direct Inspector + Drone conflict checking, and the interactive Vietnam Airspace & No-Fly Zone Map (`AirspaceNoFlyMap` on Web, `AirspaceAdvisoryCard` on Mobile, `/api/v1/airspace/zones` & `/evaluate` under Decree No. 288/2025/NĐ-CP).
6. **`FE-06` — Flight Readiness & Field Execution** *(Owner: Phùng Trung Quốc)*: Self-service aviation flight permit upload gate (`Assigned` → `Ready for Flight` upon unexpired pilot license check) and Web/Flutter Mobile on-site field flight session logging (`Start`, `Postpone`, `Abort`, `Complete`, and Additional Sessions).
7. **`FE-07` — Operational Dashboard & Schedule Calendar** *(Owner: Phùng Trung Quốc)*: Role-scoped operational analytics dashboards, server-paged inspection/report queues, interactive Month/Week/Agenda `InspectorScheduleCalendar`, Enterprise Dark Mode, and bilingual (EN/VI) localization.
8. **`FE-08` — Evidence Management & AI Defect Detection** *(Owner: Trần Tùng Bách)*: Multipart evidence intake into MinIO with EXIF GPS/timestamp extraction, single/bulk soft-retirement, Inspector-invoked Ultralytics `YOLO11 (MBDD2025)` defect detection (with multimodal fallback), human finding verification (`Confirmed`), and confirmed findings baseline lock (`Report Draft`).
9. **`FE-09` — Inspection Reporting & Publication** *(Owner: Trần Tùng Bách)*: Context-grounded LLM & manual report drafting, live OpenHTMLtoPDF preview, author verification (`Author Verified`), independent `Organization Manager` approval/return, immutable A4 PDF publication as an immutable PDF document (`Published`), and per-finding corrective handoff (`Repair Pending` / `Completed`).
10. **`FE-10` — Maintenance Planning & AI Scope Advisory** *(Owner: Trương Thái Như)*: Forwarded defect triage, `pgvector` RAG engineering standard scope advisor (`TCVN 9343:2012`, `EN 1504-9`, `ISO 12944-5` + `DeterministicScopeFallback`), work order creation (`Draft`), team role assignment (`Team Lead`, `Report Author`, `Team Member`, independent reviewer), and task decomposition.
11. **`FE-11` — Cost Estimation & Repair Execution** *(Owner: Trương Thái Như)*: Versioned itemized cost estimation (`Labor`, `Material`, `Equipment`), independent budget approval (`Approved`), Change Order governance, and Web/Mobile repair task execution with Team Lead work log verification (`Verified` → `Work Completed`).
12. **`FE-12` — Maintenance Acceptance & Cost Closure** *(Owner: Trương Thái Như)*: Author-verified maintenance completion report PDF, independent technical acceptance (`Accepted` / `Rework Required` / `Re-Inspection Required`), actual cost reconciliation (`Cost Reconciled`), and work order closure (`Closed`).

#### c) Functional Requirements Summary (12 Features / 24 Functions)
- **`FE-01` Authentication & Access Control**: (1) Organization Registration & User Sign-In; (2) Session Management & Role-Based Access Control.
- **`FE-02` Workforce & Subscription Management**: (1) Workforce Provisioning & Pilot License Profile; (2) Enterprise Subscription & Online Payment.
- **`FE-03` Asset & Drone Fleet Management**: (1) Infrastructure Asset & Document Management; (2) Drone Inventory & B2B Drone Leasing.
- **`FE-04` Recurring Schedule & Notifications**: (1) Recurring Inspection Schedule Management; (2) Event-Driven In-App Notifications.
- **`FE-05` Mission Dispatch & Airspace Advisory**: (1) Inspection Mission Scheduling & Conflict Check; (2) Interactive Airspace & No-Fly Zone Map.
- **`FE-06` Flight Readiness & Field Execution**: (1) Flight Permit Upload & Readiness Gate; (2) On-Site Field Flight Session Logging.
- **`FE-07` Operational Dashboard & Schedule Calendar**: (1) Multi-Role Operational Analytics Dashboard; (2) Inspector Schedule Calendar & Localization.
- **`FE-08` Evidence Management & AI Defect Detection**: (1) Inspection Evidence Upload & Metadata Management; (2) AI Defect Detection & Finding Verification.
- **`FE-09` Inspection Reporting & Publication**: (1) AI-Assisted & Manual Report Drafting; (2) Report Review, PDF Publication & Maintenance Handoff.
- **`FE-10` Maintenance Planning & AI Scope Advisory**: (1) Work Order Creation & AI Repair Scope Advisory; (2) Maintenance Team & Task Assignment.
- **`FE-11` Cost Estimation & Repair Execution**: (1) Cost Estimation, Budget Approval & Change Orders; (2) Field Repair Execution & Work Log Verification.
- **`FE-12` Maintenance Acceptance & Cost Closure**: (1) Maintenance Completion Reporting & Technical Acceptance; (2) Cost Reconciliation & Work Order Closure.

#### d) Non-Functional Requirements Summary
- **Performance (`NFR-01`, `NFR-02`)**: 95th percentile (`p95`) latency $\le 2,000\text{ ms}$ for standard JSON REST API endpoints under 50 concurrent users; single-image YOLO11 CPU inference latency $\le 5,000\text{ ms}$ for images up to $10\text{ MB}$.
- **Security & Multi-Tenant Isolation (`NFR-03`, `NFR-04`)**: 100% tenant boundary isolation via composite database foreign keys `(id, organization_id)` and Spring Security `@PreAuthorize` checks; Argon2id password hashing, 15-minute HS256 JWT access tokens, 7-day HmacSHA256 rotated refresh tokens, CSRF protection, and IP rate-limiting ($10\text{ req} / 60\text{ s}$ on auth endpoints).
- **Reliability & Data Integrity (`NFR-05`)**: 100% immutability of published inspection and maintenance PDF reports stored in MinIO with complete version history (`Superseded`); graceful manual fallback when AI vision or LLM services are offline.
- **Maintainability & Automated Test Quality (`NFR-06`)**: Spring Modulith 2.1 boundary verification (`ModulithArchitectureTest` = 0 cycle/visibility violations), $\ge 80\%$ backend JaCoCo instruction/line coverage gate in CI, and $\ge 50\%$ automated execution across functional test cases.

#### e) Theory & Practical (Technologies)
- **Backend**: Java `21`, Spring Boot `4.1.0`, Spring Modulith `2.1.1`, Spring Security OAuth2 Resource Server (Nimbus JWT), Spring Data JPA / Hibernate, Flyway, OpenHTMLtoPDF `1.0.10`, MinIO SDK `9.0.3`.
- **AI & Computer Vision Microservice**: Python `3.11`, FastAPI `0.115.6`, Uvicorn `0.34.0`, Ultralytics `8.3.55` (`YOLO11` trained on `MBDD2025` dataset, PyTorch `2.5.1`), plus OpenAI-compatible Vision Fallback, LLM Report Drafting, and `pgvector` RAG Maintenance Scope Advisor.
- **Frontend Web Portal**: React `19.2.8`, TypeScript `6.0.2`, Vite `8.2.2`, Material UI (`@mui/material` `9.4.0`), TanStack React Query `5.102.8`, React Router `7.18.3`, Zustand `5.0.15`, React Hook Form + Zod.
- **Mobile Application**: Flutter (`1.0.0+1`), Dart `3.13.2`, Riverpod `3.4.2`, GoRouter `18.0.0`, Dio `5.11.0`, Freezed `4.0.1`.
- **Database & Object Storage**: PostgreSQL `17` with `pgvector` (`hnsw` cosine index) and `pgcrypto`; MinIO S3-compatible object storage.
- **Third-Party Payment & DevOps**: PayPal REST API v2 (Orders v2 & Webhook verification); Docker & Docker Compose, Nginx `1.27-alpine`, GitHub Actions CI/CD, Tailscale SSH deployment to staging/production (`smartdroneinspection.duckdns.org`).

#### f) Products (Expected Deliverables)
1. **SmartDroneInspection Web Portal** (Multi-portal React 19 SPA: Admin, Client/Organization Manager, Operations).
2. **SmartDroneInspection Mobile Application** (Flutter cross-platform app for Field Inspectors & Maintenance Engineers).
3. **Spring Boot 4.1 Modular Monolith Backend API** (9 Spring Modulith modules, 21 REST controllers, Flyway `V1`–`V5` schema).
4. **Containerized YOLO11 Defect Detection Microservice** (`FastAPI` + `best.pt` weights) & RAG/LLM Integration Adapters.
5. **Docker Compose Deployment Package, Automated Test Suites & Full SEP490 Documentation** (Reports 1–7, Review 2 Package).

#### g) Proposed Tasks (Work Packages — Mapped 1-to-1 to Git Authorship)
- **Work Package 1 — Requirement Specification, Architecture & Database Foundation**: Finalize 5-role Enterprise SaaS & B2B Drone Leasing SRS/SDD, Flyway `V1`–`V5` 30-table schema, and Spring Modulith boundaries *(Owner: All members, Led by Trần Hoàng Trung Hiếu)*.
- **Work Package 2 — Workforce, Subscriptions, Assets, B2B Drone Leasing & Recurring Schedules (`FE-02`, `FE-03`, `FE-04` — `WF-01`)**: Platform/Workforce user governance, pilot licenses, PayPal/wire subscriptions, B2B drone leasing pool, asset registry with checkpoints, recurring inspection schedules, and in-app notifications *(Owner: Trần Hoàng Trung Hiếu)*.
- **Work Package 3 — Mission Dispatch, Airspace Map, Flight Permit Gate, Field Sessions & Dashboards (`FE-05`, `FE-06`, `FE-07` — `WF-02`)**: One-off/scheduled mission dispatch, interactive Vietnam Airspace & No-Fly Zone Map, self-service flight permit upload gate, Web & Flutter mobile field session execution, operational dashboards, and Inspector Schedule Calendar *(Owner: Phùng Trung Quốc)*.
- **Work Package 4 — Authentication/RBAC, Evidence Intake, YOLO11 Defect Detection & Inspection Report Publication (`FE-01`, `FE-08`, `FE-09` — `WF-03`)**: Argon2id/JWT/CSRF/RBAC security foundation, EXIF/MinIO evidence management, FastAPI YOLO11 inference & vision fallback, human findings verification, LLM/manual report drafting, OpenHTMLtoPDF rendering, independent review/publication, and corrective handoff *(Owner: Trần Tùng Bách)*.
- **Work Package 5 — Maintenance Work Orders, RAG Scope Advisor, Cost Estimation, Field Repair & Acceptance Closure (`FE-10`, `FE-11`, `FE-12` — `WF-04`)**: `pgvector` RAG repair standard advisor, work order lifecycle, team/task planning, itemized estimates, change orders, mobile/web work logs with Lead verification, completion report PDFs, independent technical acceptance, cost reconciliation, and closure *(Owner: Trương Thái Như)*.
