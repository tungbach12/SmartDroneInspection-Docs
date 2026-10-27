# Project Tracking Workbook Source (`Report3_Project Tracking.xlsx`)

## 1. WBS (Work Breakdown Structure)

| # | Function/Screen | Feature | Level* | Function/Screen Details | Planned | Status |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | Organization Registration & User Sign-In | FE-01 | Medium | Tenant onboarding with active Terms/Privacy consent and Argon2id authentication (Web & Mobile). | Iteration 1 | Completed |
| 2 | Session Management & Role-Based Access Control | FE-01 | Complex | HS256 JWT (15m), HmacSHA256 refresh rotation (7d), CSRF, IP rate limiting (10 req/60s), and 5-role RBAC (Platform Admin and Platform Manager single-role separation). | Iteration 1 | Completed |
| 3 | Workforce Provisioning & Pilot License Profile | FE-02 | Medium | Platform user admin, customer workforce provisioning (Inspector, Maintenance Engineer), and pilot license self-declaration. | Iteration 1 | Completed |
| 4 | Enterprise Subscription & Online Payment | FE-02 | Complex | 1..120m Enterprise subscription contract preview, wire confirmation by Platform Manager, and PayPal Orders v2 + signed webhook settlement. | Iteration 1 | Completed |
| 5 | Infrastructure Asset & Document Management | FE-03 | Complex | Global asset categories, tenant assets with GPS coordinates, standardized inspection_items checkpoints, reference documents in MinIO, and asset retirement. | Iteration 1 | Completed |
| 6 | Drone Inventory & Drone Equipment Leasing | FE-03 | Complex | Customer owned/leased drone fleet, platform leasable drone pool (platform_drones), drone equipment lease contracts (drone_leases), auto-provisioning, and reclaim. | Iteration 1 | Completed |
| 7 | Recurring Inspection Schedule Management | FE-04 | Complex | Timezone-anchored recurrence (WEEK/MONTH/YEAR), 14-day rolling scheduler job, 3-day reminder job, and Blocked occurrence retry/skip. | Iteration 1 | Completed |
| 8 | Event-Driven In-App Notifications | FE-04 | Medium | Spring Modulith event_publication outbox listeners and deduplicated in-app notification inbox (uq_notifications_deduplication_key). | Iteration 1 | Completed |
| 9 | Inspection Mission Scheduling & Conflict Check | FE-05 | Complex | One-off inspection dispatch with direct Inspector + Drone assignment and concurrent time-window overlap detection. | Iteration 1 | Completed |
| 10 | Interactive Airspace & No-Fly Zone Map | FE-05 | Complex | OpenStreetMap + SVG vector airspace overlay (AirspaceNoFlyMap on Web, AirspaceAdvisoryCard on Mobile) evaluating No-Fly Zone & Restricted Zone (MSG28). | Iteration 1 | Completed |
| 11 | Flight Permit Upload & Readiness Gate | FE-06 | Medium | Self-service aviation flight permit upload to MinIO with pilot license expiry check and automatic Assigned -> Ready for Flight transition. | Iteration 1 | Completed |
| 12 | On-Site Field Flight Session Logging | FE-06 | Complex | Web & Flutter Mobile field session start (with pre-flight checklist note), postponement, abort, completion (Field Completed), and additional sessions. | Iteration 1 | Completed |
| 13 | Multi-Role Operational Analytics Dashboard | FE-07 | Medium | Role-scoped operational KPIs, radial gauges, stacked bar charts, and server-paged inspection/report queues. | Iteration 1 | Completed |
| 14 | Inspector Schedule Calendar & Localization | FE-07 | Medium | Interactive Month/Week/Agenda InspectorScheduleCalendar, InspectionWorkDetailDialog, Enterprise Dark Mode, and EN/VI localization. | Iteration 1 | Completed |
| 15 | Inspection Evidence Upload & Metadata Management | FE-08 | Complex | Multipart evidence upload to MinIO, ImageIO decode check, EXIF GPS/timestamp extraction, duplicate filename guard, and single/bulk soft-retire. | Iteration 1 | Completed |
| 16 | AI Defect Detection & Finding Verification | FE-08 | Complex | Self-hosted FastAPI + Ultralytics YOLO11 (MBDD2025) inference, multimodal fallback, human finding confirmation, and findingsSnapshotHash lock (Report Draft). | Iteration 1 | Completed |
| 17 | AI-Assisted & Manual Report Drafting | FE-09 | Complex | Context-grounded LLM & manual report section synthesis, section editing, live OpenHTMLtoPDF preview, and author verification/submission (Submitted). | Iteration 1 | Completed |
| 18 | Report Review, PDF Publication & Maintenance Handoff | FE-09 | Complex | Independent Organization Manager approve/return, immutable A4 PDF compilation to MinIO (Published), and per-finding corrective handoff. | Iteration 1 | Completed |
| 19 | Work Order Creation & AI Repair Scope Advisory | FE-10 | Complex | Forwarded defect triage, pgvector RAG engineering standard advisor (TCVN/EN/ISO + DeterministicScopeFallback), and work order creation (Draft). | Iteration 1 | Completed |
| 20 | Maintenance Team & Task Assignment | FE-10 | Medium | Appointment of LEAD, Report Author, MEMBER, and independent acceptingReviewerUserId, plus sequential Planned task decomposition. | Iteration 1 | Completed |
| 21 | Cost Estimation, Budget Approval & Change Orders | FE-11 | Complex | Versioned LABOR/MATERIAL/EQUIPMENT cost estimates, independent Organization Manager budget approval, and formal Change Order variance governance. | Iteration 1 | Completed |
| 22 | Field Repair Execution & Work Log Verification | FE-11 | Complex | Web & Flutter Mobile work order release/start, task work logs (hours, as-left condition, test readings), Team Lead verification, and completion declaration. | Iteration 1 | Completed |
| 23 | Maintenance Completion Reporting & Technical Acceptance | FE-12 | Complex | Author-verified completion report PDF, independent technical acceptance (Accepted / Rework Required / Re-Inspection Required), and auto re-inspection trigger. | Iteration 1 | Completed |
| 24 | Cost Reconciliation & Work Order Closure | FE-12 | Complex | Itemized Actual cost recording, BigDecimal budget variance reconciliation (Cost Reconciled), and work order / inspection closure (Closed / Completed). | Iteration 1 | Completed |
| 25 | Full-Stack CI/CD & Staging Deployment Pipeline | FE-01..FE-12 | Medium | GitHub Actions CI (850 JUnit, 602 Vitest, 20 Flutter tests) and locked Tailscale SSH deployment + pg_dump backup to smartdroneinspection.duckdns.org. | Iteration 1 | Completed |

## 2. Issues

| # | Issue | Potential Impact | Priority | Owner | Open Date | Close Date | Status | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | External SmartDroneHub API unavailable for live drone mission telemetry | Could block mission execution if coupled to external flight controller API | High | Trần Hoàng Trung Hiếu | 2026-09-18 | 2026-10-08 | Closed | Replaced external dependency with self-contained Enterprise Inspection & Drone Equipment Leasing + Self-Service Flight Permit Gate (Registration v2.0). |
| 2 | JDK HttpClient HTTP/2 (h2c) upgrade header rejected by Uvicorn FastAPI YOLO11 server | Caused 400 Unsupported upgrade request on primary YOLO11 inference calls | High | Trần Tùng Bách | 2026-10-16 | 2026-10-17 | Closed | Pinned HttpClient.Version.HTTP_1_1 in YoloInferenceClient and added regression test in YoloInferenceClientTest. |
| 3 | Month-end and leap-year drift in naive date addition for recurring schedules | Could permanently shift 31st-of-month schedules to the 28th after February | Medium | Trần Hoàng Trung Hiếu | 2026-10-23 | 2026-10-26 | Closed | Implemented original-anchor calendar arithmetic with clamping in RecurringInspectionSchedule and verified in InspectionRecurrenceTest. |
| 4 | Unreachable LLM endpoint during offline/staging maintenance planning | Could block work order task decomposition if RAG advisor had no fallback | Medium | Trương Thái Như | 2026-10-22 | 2026-10-24 | Closed | Added DeterministicScopeFallback grounded in seeded TCVN/EN/ISO repair_knowledge_chunks. |
| 5 | Concurrent GitHub Actions deployments from backend and frontend repos to VPS2 | Could cause port or container race conditions during simultaneous merges | Medium | Trần Tùng Bách | 2026-10-15 | 2026-10-19 | Closed | Added flock -w 900 /tmp/sdi-deploy.lock and pre-deploy pg_dump backup in deploy.yml. |

## 3. Defects

| Feature | Function/Screen | Tester | Defect Description | Assign To | Status | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| FE-01 | Organization Registration & Platform User Create | Trần Tùng Bách | Raw JdbcTemplate audit insert referenced generated user_id before Hibernate flushed users row, causing FK violation (500). | Trần Tùng Bách | Closed | Fixed on 2026-09-28 using saveAndFlush before SecurityAuditService.record; verified by OrganizationRegistrationApiIntegrationTest & AdminUserApiIntegrationTest. |
| FE-02 | Workforce Provisioning Email Check | Trần Hoàng Trung Hiếu | Global email uniqueness check returned 409 Email Already Exists for another tenant's email, acting as a cross-tenant existence oracle. | Trần Hoàng Trung Hiếu | Closed | Fixed on 2026-10-11: foreign-tenant email returns non-disclosing 404 User Not Found while same-tenant duplicate returns 409; verified in WorkforceApiIntegrationTest. |
| FE-08 | Evidence Intake Image Validation | Trần Tùng Bách | EvidenceService.upload checked MIME type and size but did not decode image bytes, allowing truncated/corrupt PNGs to be stored. | Trần Tùng Bách | Closed | Fixed on 2026-10-11: added ImageIO decode check rejecting corrupt images with 400 Evidence Invalid; verified in InspectionEvidenceApiIntegrationTest. |
| FE-09 | Report Publish Workflow State Refresh | Trần Tùng Bách | Frontend usePublishReportVersion hook did not invalidate workflow-state query, hiding the corrective handoff panel until manual reload. | Trần Tùng Bách | Closed | Fixed on 2026-10-17 by invalidating workflow-state query on publish; verified in ReportDetailPage.test.tsx. |
| FE-09 | Nginx Upload Size Limit Mismatch | Trần Tùng Bách | Frontend nginx.conf defaulted to 10M while backend allowed 20M multipart requests, returning HTML 413 instead of RFC 9457 ProblemDetail. | Trần Tùng Bách | Closed | Fixed on 2026-10-17 by setting client_max_body_size 20M in nginx.conf. |
| FE-04 | Flyway V1-V5 Schema Inventory Assertion | Trần Hoàng Trung Hiếu | Adding recurring_inspection_schedules, schedule_occurrences, and notification deduplication_key required forward migrations V3, V4, V5 without mutating V1/V2. | Trần Tùng Bách | Closed | Fixed on 2026-10-26: sequenced V3, V4, V5 and passed FullDatabaseSchemaMigrationTest (850/850 backend tests green). |

## 4. Q&A

| Date | Question | By | Priority | Status | Note (answer, other notes) |
| --- | --- | --- | --- | --- | --- |
| 2026-09-25 | Should SmartDroneInspection directly control drone flight paths or consume/log mission execution? | Trần Hoàng Trung Hiếu | High | Closed | Mentor confirmed: platform is an enterprise inspection & maintenance management Enterprise, not a hardware flight controller (BR-16). |
| 2026-10-08 | How should platform administration be separated from commercial subscription and drone lease settlements? | Phạm Minh Trí (Supervisor) | High | Closed | Split platform zone into ADMIN (technical/user/catalog governance) and Platform Manager (subscription & drone equipment lease settlement) with strict XOR separation of duties (BR-01, BR-29). |
| 2026-10-15 | Should AI defect detection run automatically on every uploaded photo or only when invoked by the Inspector? | Trần Tùng Bách | Medium | Closed | Mentor & team agreed: detection is explicitly Inspector-invoked per image (with parallel batch support) and remains Pending until human confirmation (BR-20). |
| 2026-10-22 | How can maintenance work orders suggest engineering repair scopes when an external LLM is unavailable? | Trương Thái Như | Medium | Closed | Seeded 5 civil engineering standards (TCVN 9343:2012, EN 1504-9, ISO 12944-5, ASTM C1583, TCVN 9361:2012) into repair_knowledge_chunks with DeterministicScopeFallback. |
