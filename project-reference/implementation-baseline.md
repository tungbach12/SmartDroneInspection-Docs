---
title: "Verified Implementation Baseline (2026-11-20)"
weight: 20
---

# Verified Implementation Baseline

**Purpose.** This page is the single factual source that every formal report in `reports/` is checked
against. It records what the running system actually does at commit time, verified by reading the
source, not by trusting earlier drafts. When a report and this page disagree, this page wins until
the code changes.

**Snapshot.** Backend `7964677`, frontend `5ab880d`, mobile `21af14a`, all merged 2026-11-20. Documentation repo synced with `V63`–`V65`.

---

## 1. Product scope

| Fact | Value |
|---|---|
| Product | SmartDroneInspection — AI-powered Infrastructure Inspection Management Platform |
| Project code | `GFA26SE139` |
| Group | `FA26SE112` |
| Login roles | **4**: `ADMIN` (Platform Admin), `MANAGER` (Platform Manager), `CUSTOMER` (Customer Organization user), `INSPECTOR` (Partner Drone Inspector) |
| Retired | `MAINTENANCE_ENGINEER`, the corrective-maintenance workflow and its work orders, repair-scope advisory, and cost estimation |
| Features | **8**: `FE-01` … `FE-08`, two per main flow |
| Main flows | `MF1` (onboarding and partner admission: `FE-01`, `FE-02`), `MF2` (buildings, requests, quotes, agreements, dispatch: `FE-03`, `FE-04`), `MF3` (field work, evidence, findings: `FE-05`, `FE-06`), `MF4` (report review and payment settlement: `FE-07`, `FE-08`) |
| Re-inspection | **In scope under `FE-08`.** `POST /inspections/{id}/reinspections` opens a loop against a published report, and `ReinspectionDefectVerification` records each source defect as `RESOLVED`, `UNRESOLVED`, or `INCONCLUSIVE`. It reuses the `MF2`–`MF4` flows rather than adding a maintenance flow. |
| Automated actors | AI Vision (YOLO11s + LLM fallback), LLM report drafter, Sepay, VNPay, Google OAuth2, SMTP/SMS OTP |

**Role enforcement, in order of authority.** A fifth role cannot exist:
1. `shared/auth/Roles.java` declares exactly the four constants.
2. Database CHECK `users.ck_users_roles` allows a comma-list of only those four.
3. `users/domain/RolePolicy` rejects multi-role and empty role sets — one role per user.
4. `AccessTokenService` writes a `roles` JWT claim; `SecurityConfig.jwtAuthenticationConverter()` maps
   it with the `ROLE_` prefix.
5. 219 endpoints carry `@PreAuthorize`.
6. Services add ownership/assignment/qualification checks on top of role (`UserAccess`,
   `Mf2ActorPolicy`, `EvidenceOwnershipService`, `ReportService` separation of duties).

Legacy input aliases still accepted by `UserRole.fromName()` for old records:
`PLATFORM_MANAGER`, `SERVICE_MANAGER`, `ORG_MANAGER`, `ORG_ADMIN`, `CLIENT`.

---

## 2. Backend architecture

| Fact | Value |
|---|---|
| Stack | Java 21, Spring Boot **4.1.0**, Spring Modulith **2.1.1** |
| Modules | 8: `users`, `assets`, `contracts`, `inspections`, `notifications`, `dashboard`, `infrastructure`, `shared` |
| Boundary enforcement | `ModulithArchitectureTest` runs `modules.verify()` and asserts `maintenance`, `workforce`, `inspectionrequests` are absent |
| Controllers | 28 |
| Endpoints | **239** — 81 GET, 117 POST, 22 PUT, 10 PATCH, 9 DELETE |
| API base path | `/api/v1` |
| Domain events | 15 — 12 in `inspections/events`, 2 in `users/events`, 1 in `shared/api` |
| Event listener classes | 4 (`InspectionNotificationListener`, `InspectorApplicationNotificationListener`, `PilotLicenseExpiryCheckService`, `AssetRegistrationListener`) |
| Scheduled jobs | `InspectionLifecycleMonitor`, `VideoProcessingWorker`, evidence upload expiry sweeper, pilot-license expiry check |

Module dependency rules live in each module's `package-info.java` (`@ApplicationModule`), and the
`shared` module exposes named interfaces `api`, `auth`, `config`, `exception`, `storage`.

---

## 3. Database

| Fact | Value |
|---|---|
| Engine | PostgreSQL 17 with the `pgvector` image (`pgvector/pgvector:pg17`) |
| Migrations | **14 files**: `V1__baseline.sql`, `V2__remove_finding_recommended_action.sql`, `V3__reinspection_resolved_validity.sql`, `V4__payment_due_expiry.sql`, `V60__quote_partner_assignment_optional.sql`, `V61__inspection_chat_and_dispatch_settings.sql`, `V62__inspection_knowledge_rag.sql`, `V63__ai_auto_confirm_default_70.sql`, `V64__backfill_published_historical_cases.sql`, `V65__rag_local_embeddings_384.sql`, `V66__asset_ownership_information.sql`, `V67__gateway_order_created_at.sql`, `V68__gateway_inbound_transactions.sql`, and `V69__split_inspection_flight_permits_and_field_session_telemetry.sql` |
| Migration assertion | `FullDatabaseSchemaMigrationTest` asserts `flyway_schema_history` versions are exactly `["1","2","3","4","60","61","62","63","64","65","66","67","68","69"]` |
| Tables | **48** application tables (**47** JPA runtime entities including `event_publication`; **50** total tables in `public`) |
| `pgvector` usage | `V62` enables `pgvector` and `V65` configures `vector(384)` HNSW `vector_cosine_ops` indexes on `inspection_knowledge_chunks` and `historical_finding_cases` backed by local `fastembed` (`paraphrase-multilingual-MiniLM-L12-v2`) in `ai-inference`, with `HYBRID_MATCH` fallback, `V64` backfill, and startup missing-vector backfill (`ApplicationReadyEvent`). |

### Table inventory (41)

| # | Table | Cols | Purpose |
|---|---|---:|---|
| 1 | `users` | 17 | Account, single role, lockout and OTP state, AI fallback preference |
| 2 | `auth_sessions` | 9 | Refresh sessions with rotation (`token_hash`, `previous_token_hash`), per-client |
| 3 | `otp_challenges` | 16 | One-time codes for login, registration, password reset |
| 4 | `audit_events` | 11 | Actor, action, aggregate, before/after status, trace id |
| 5 | `prospective_customer_registrations` | 21 | Pre-account customer applications, airspace review state |
| 6 | `pilot_license_classes` | 6 | UAV licence class catalog used for assignment qualification |
| 7 | `event_publication` | 9 | Spring Modulith transactional outbox |
| 8 | `asset_categories` | 6 | Asset classification catalog |
| 9 | `assets` | 17 | Customer-owned infrastructure asset, JSON location/profile, inspection items |
| 10 | `asset_documents` | 11 | Uploaded asset documents with SHA-256 checksum and object key |
| 11 | `inspection_items` | 8 | Per-asset inspection checkpoints |
| 12 | `checklist_templates` | 9 | Pre-flight / post-flight checklist template rows |
| 13 | `drones` | 21 | Drone records; CHECK enforces exactly one owner scope |
| 14 | `drone_document_configs` | 11 | Admin-configurable required registration documents |
| 15 | `drone_feature_configs` | 11 | Admin-configurable drone feature catalog |
| 16 | `drone_registration_applications` | 21 | Inspector drone registration with document and review state |
| 17 | `inspections` | 41 | Inspection occurrence: status, assignment, flight-permit block, schedule |
| 18 | `field_sessions` | 23 | On-site session, telemetry source, flight trace and metrics |
| 19 | `evidence` | 27 | Photo/video evidence, processing state, object keys, source-video lineage |
| 20 | `evidence_upload_sessions` | 24 | Resumable chunked upload state |
| 21 | `findings` | 14 | Defect findings, bounding box, model name/confidence, technical notes |
| 22 | `inspection_reports` | 11 | Versioned report, status, return reason, AI summary |
| 23 | `inspector_reliability_events` | 7 | Assignment/field reliability signals |
| 24 | `reinspection_defect_verifications` | 8 | Re-inspection defect verdicts |
| 25 | `service_requests` | 29 | One-time/recurring service request, status, owner customer |
| 26 | `service_request_quotes` | 14 | Versioned VND quotations |
| 27 | `service_request_occurrences` | 12 | Scheduled occurrences under a request |
| 28 | `service_request_messages` | 6 | Order-chat negotiation messages |
| 29 | `service_request_message_attachments` | 8 | Chat attachments |
| 30 | `service_invoices` | 9 | Service invoices |
| 31 | `service_payments` | 11 | Payments incl. refunded amount and refund status |
| 32 | `service_refunds` | 25 | Refund allocations; CHECK requires the allocation components to sum to the amount |
| 33 | `inspector_payouts` | 11 | Partner payouts |
| 34 | `inspector_receivables` | 10 | Amounts owed by Inspectors |
| 35 | `inspector_receivable_recoveries` | 7 | Recovery of receivables |
| 36 | `inspection_finance_settings` | 6 | Commission/VAT/TNCN rates |
| 37 | `inspector_applications` | 24 | Partner Inspector applications and review |
| 38 | `inspector_profiles` | 23 | Inspector profile, licences, partner status |
| 39 | `inspector_flight_logs` | 14 | Flight log intake (including non-MAVLink) |
| 40 | `notifications` | 12 | In-app/email notification with dedupe and read state |
| 41 | `platform_ai_settings` | 6 | Singleton AI settings: auto-confirm flag and threshold (`default 70.00` since `V63`, lowered from `85.00`) |
| 42 | `platform_operations_settings` | 4 | Singleton operations settings: Step 4 assignment acceptance timeout (`V61`) |
| 43 | `inspection_messages` | — | Inspector–Customer per-inspection chat thread (`V61`) |
| 44 | `inspection_message_attachments` | — | Private MinIO chat attachments (`V61`) |
| 45 | `inspection_knowledge_chunks` | — | Seeded engineering standards/guidelines with `vector(384)` HNSW (`V62`, `V65`) |
| 46 | `historical_finding_cases` | — | Published/benchmark historical defect cases with `vector(384)` HNSW (`V62`, `V64`, `V65`) |
| 47 | `gateway_inbound_transactions` | — | Idempotent inbound payment webhook audit log (`V68`) |
| 48 | `inspection_flight_permits` | — | Dedicated 1-to-1 flight-permit upload & review gate split from `inspections` (`V69`) |
| 49 | `field_session_telemetry` | — | Dedicated 1-to-1 SmartDroneHub flight metrics, trace JSON & synced video split from `field_sessions` (`V69`) |

The full column-level dump (every column, type, default and CHECK constraint) is reproducible with
`tools/` conventions from `SmartDroneInspection-backend/src/main/resources/db/migration/V1__baseline.sql`.

---

## 4. AI

| Fact | Value |
|---|---|
| Primary detector | YOLO11s, self-hosted FastAPI service in `ai-inference/` |
| Model version | `yolo11s`, `mbdd2025-v1` |
| Training data | MBDD2025 UAV building-defect dataset, CC BY 4.0 |
| Classes (fixed order) | `crack`, `leakage`, `abscission`, `corrosion`, `bulge` |
| Inference settings | confidence 0.20, image size 1024 |
| Held-out metrics | 1,448 test images — precision 0.8571, recall 0.7955, mAP50 0.8580, mAP50-95 0.4876 |
| Fallback | OpenAI-compatible vision model when YOLO cannot process an image |
| Routing | `PrimaryWithFallbackInference` as the `@Primary AiInferencePort`, enabled by `AnyAiInferenceProviderEnabledCondition` |
| Per-user opt-out | `users.vision_fallback_enabled`, `PUT /users/me/ai-fallback-preference` |
| Narrative drafting | `ReportDraftClient` — one HTTP call per draft, strict JSON shape, anti-hallucination system prompt. **Not retrieval-augmented.** |
| PDF rendering | Deterministic HTML template (`ReportHtmlTemplate`, 7 numbered sections) → openhtmltopdf/PdfBox. Not AI-generated. |
| Governance | Admin-only `GET|PUT /inspections/ai-settings`, singleton settings, `rejected_pending_count` analytics |

Per-class metrics are also recorded in `ai-inference/models/training/test_metrics.json`.

---

## 5. Payments

| Gateway | Version / mechanism | Webhook | Default |
|---|---|---|---|
| Sepay (VietQR) | `Authorization: Apikey` header (`MessageDigest.isEqual` SHA-256) | `POST /api/v1/webhooks/sepay` | disabled (`SEPAY_ENABLED=false`) |
| VNPay | API 2.1.0, HMAC-SHA512 | `GET /webhooks/vnpay/ipn`, `/return` | disabled (`VNPAY_ENABLED=false`) |

Both run behind a `Disabled*Gateway` fallback so the application boots with payments off. Payment is
a configuration-gated feature, not a missing one. Deliverable release is gated by
`shared/api/InspectionPaymentGate` (`isPaymentDue`, `isAcceptedOrPaid`).

---

## 6. Storage and media

- MinIO object storage, bucket `inspection-evidence`, enabled by `app.storage.minio.enabled`.
- Resumable chunked upload sessions; the session state machine is
  `OPEN → COMPLETING → PROCESSING → READY | FAILED | CANCELLED | EXPIRED`.
- FFmpeg normalisation to ≤1920×1080 plus 480px thumbnails; keyframe extraction ≤1280×720;
  `max-concurrent-jobs: 2`.
- Media access uses HMAC-SHA256 signed tickets (5-minute TTL) so `GET /evidence/{id}/stream` can be
  `permitAll()` while still being protected — required for HTTP Range video playback.

---

## 7. Authentication

- JWT with a `roles` claim; authorities prefixed `ROLE_`.
- Two security filter chains: `browserAuthChain` (`/api/v1/auth/**`, cookie CSRF) and `apiChain`
  (stateless JWT resource server, CSRF disabled).
- Refresh-token rotation recorded in `auth_sessions.previous_token_hash`.
- Rate limiting per IP for OTP and login (`AuthRateLimitFilter`).
- Password policy, Argon2id hashing, forced password change flag.
- Google OAuth2 web and mobile callbacks (`smartdrone://auth/callback`).
- OTP delivery by email (SMTP) and SMS (Twilio).
- Bootstrap administrator disabled by default (`AUTH_BOOTSTRAP_ENABLED=false`).

---

## 8. Frontend

| Fact | Value |
|---|---|
| Stack | React 19, strict TypeScript, Vite 8, Material UI 9, React Router 7, TanStack Query 5, react-hook-form 7 + Zod 4, Zustand 5, axios, MapLibre GL |
| Portals | 4 — `admin` (`/admin`), `manager` (`/manager`), `client` (`/client`), `operations` (`/operations`) |
| Sections | 14 — `dashboard`, `contracts` (Service requests), `messages`, `assets`, `asset-catalog`, `inspections`, `reports`, `platform-users`, `finance-settings`, `pilot-license-classes`, `onboarding-reviews`, `inspector-drones`, `notifications`, `settings` |
| Authorisation model | `src/app/permissions/accessPolicy.ts` — a `SectionId × PortalId → roles` matrix; **a denied section has no route at all** |
| ~Pages | ~40 routed page components |
| Inspection workspace | Nested routes: `tracking`, `evidence`, `findings`, `report`, `audit`, `review`, `settlement`, `permit`, `pre-flight`, `field-session`, `post-flight` |
| Bilingual | English and Vietnamese via `LocaleProvider` |

### Screen authorization matrix (derived from `accessPolicy.ts`)

| Section | ADMIN | MANAGER | CUSTOMER | INSPECTOR | Notes |
|---|:---:|:---:|:---:|:---:|---|
| Dashboard | X | X | X | X | Role-specific variant per portal |
| Service requests | X | X | X | — | |
| Messages | — | X | X | — | Scoped manager/customer inbox |
| Assets | X | X | X | — | |
| Asset catalog | X | — | — | — | Platform administration |
| Inspections | X | X | X | X | Workspace tabs differ by role |
| Reports | X | X | X | X | Queue is `inspections?view=reports` |
| Platform accounts | X | X | — | — | Labelled **Partner inspectors** in the manager portal |
| Finance settings | X | — | — | — | |
| UAV licence classes | X | — | — | — | Admin-only by route construction |
| Onboarding reviews | X | X | — | — | MF1 review queue |
| My drones | — | — | — | X | Inspector-owned drone registration |
| Notifications | X | X | X | X | |
| Settings | X | X | X | X | Profile, security, notification prefs |

Data-scope rule: role never implies record access. `ADMIN`/`MANAGER` see platform-scoped data;
`CUSTOMER` sees only its own organization's records; `INSPECTOR` sees only assigned inspections.
`Query All Data` is limited to `ADMIN` and `MANAGER`; `Query Own Data` is the norm for `CUSTOMER`
and `INSPECTOR`.

### Navigation groups
MAIN MENU (dashboard) · OPERATIONS (service requests, messages, assets, assignments, schedule,
inspections, my drones) · GOVERNANCE (onboarding reviews, platform accounts, asset catalog, UAV
licence classes, finance settings, AI settings) · ACCOUNT (notifications, settings).
`assignments` and `schedule` are query-parameter views of `/operations/inspections`, not sections.

---

## 9. Mobile

| Fact | Value |
|---|---|
| Scope | **Customer-only portal.** `session_provider.dart` enforces `isCustomer` and bounces every other role to `/login`. |
| Stack | Flutter, Riverpod 3, GoRouter 18, Dio 5, flutter_secure_storage |
| Routes | 14 — login, register, forgot-password, OAuth callback, home, assets, asset detail, requests, new request, request detail, request chat, inspections, inspection detail (3 tabs), profile, notifications |
| Bottom navigation | 5 branches — Dashboard, Assets, Requests, Inspections, Account |
| Inspection detail tabs | Tracking, Official Report, Settlement |
| Bilingual | English and Vietnamese |

Known defect to record in Report 5: `lib/features/auth/domain/models/user_role.dart` still parses the
removed `MAINTENANCE_ENGINEER` role.

---

## 10. Deployment

| Component | Detail |
|---|---|
| Backend compose | 5 services — `postgres` (`pgvector/pgvector:pg17`, 5432), `minio` (9000/9001), `ai-inference` (8000), `smartdronehub` (8090 + 14551/udp), `backend` (8080) |
| Frontend compose | `web` — nginx serving the built SPA, `WEB_PORT` (80 default, 18080 on the deployment host) |
| Shared network | `backend_smartdroneinspection-network` (external to the frontend stack) |
| Backend image | Multi-stage Maven build → Temurin 21 JRE Alpine, `ffmpeg` installed, non-root user |
| Frontend → backend | Vite dev proxy `/api → localhost:8080`; nginx `/api/ → backend:8080` with buffering off for uploads |
| Profiles | `application.yml` (dev defaults) and `application-prod.yml` (secure cookies, Swagger off) |
| CI | Manual `workflow_dispatch` only; run `./mvnw verify` locally before merging |

---

## 11. Test evidence

| Suite | Measure | Result |
|---|---|---|
| Backend | Classes with `@Test` | 119 |
| Backend | `@Test` methods | 610 |
| Backend | Tests executed | **971, 0 failures, 0 errors, 0 skipped** (`.\mvnw.cmd verify`, 2026-11-20; Spotless, Modulith & JaCoCo gates met) |
| Backend | Stack | JUnit 6, AssertJ, Mockito, Testcontainers (PostgreSQL + MinIO) |
| Frontend | Test files / cases | 97 files (`93` passed, `4` skipped) / `724` tests (`720` passed, `4` skipped, `0` failed) (Vitest, 2026-11-20) |
| Mobile | Test files / cases | 56 tests passed, 0 failures (`flutter test`, 2026-11-20) |

The e2e harness under `SmartDroneInspection-backend/e2e/` is **scaffolding, not a working suite** —
`run-e2e.mjs` points at a directory that no longer exists. Cite it as scaffolding.

---

## 12. Known inconsistencies — do not propagate

1. Backend `README.md` still lists removed modules `inspectionrequests`, `maintenance`, `workforce`.
2. Any "5 roles" or `MAINTENANCE_ENGINEER` reference as active login roles.
3. Any `vector(1536)`, `85.00` default threshold, or `"There is no RAG"` claim (`V62`–`V65` delivered `vector(384)` local `fastembed` RAG and `70.00` default).
4. Any Flyway range other than `["1","2","3","4","60","61","62","63","64","65"]`.
5. Any application-table count other than 45 (47 total PostgreSQL tables).
6. Mobile inspector field-session screens — the app is Customer-only.
7. `frontend/.../AssetReviewPage.tsx` and `ScheduleProposalsPage.tsx` are deprecated.
8. `ReportsPage.tsx` is a redirect shim; the queue is `inspections?view=reports`.
9. `app.maintenance-advisor.*` config keys bind to nothing.
10. `e2e/scripts/run-e2e.mjs` points at a non-existent frontend directory.
