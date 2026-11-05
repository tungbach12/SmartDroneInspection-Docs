---
title: "Report 4 - System Design"
document_type: report4-sdd-section
weight: 15
source: "report4-software-design-document.docx"
---

# II. Software Design Document

## 1. System Design

### 1.1 System Architecture

SmartDroneInspection uses a modular client-server architecture that separates the client presentation sub-systems (Web Portal Application and Mobile Field Application), the modular monolith backend application server (Java 21 and Spring Boot 4.1 with Spring Modulith), the persistence and object storage layer (PostgreSQL 17 with `pgvector` and MinIO object storage), and external or containerized systems (YOLO11 defect detection service, OpenAI-compatible AI Vision/Summary/RAG gateway, SmartDroneHub telemetry and flight video service, PayOS and VNPay payment gateways, and Google OAuth 2.0).

```mermaid
%% title: System Architecture Diagram
flowchart TD
  subgraph Clients["Client Presentation Sub-Systems"]
    CLIENT_WEB["Web Portal Application\n(React 19, TypeScript, Material UI)"]
    CLIENT_MOB["Mobile Field Application\n(Flutter, Dart, Riverpod)"]
  end

  subgraph Backend["Application Server Sub-System (Java 21 & Spring Boot Modulith)"]
    SEC_FILTER["Security & Access Filter\n(SecurityConfig, JWT, OAuth 2.0, CSRF & AuthRateLimitFilter)"]
    MOD_USERS["users & workforce\n(Identity, 5-Role Access, Profiles, Audit & Workforce)"]
    MOD_CONTRACTS["contracts\n(Service Requests, VND Quotations, Agreements & Billing)"]
    MOD_ASSETS["assets\n(Infrastructure Assets, Airspace Zones & Owned Drones)"]
    MOD_INSP["inspections\n(Flight Permits, Field Sessions, Evidence, Findings & PDF Reports)"]
    MOD_MAINT["maintenance\n(Work Orders, Repair Planning, Work Logs, Acceptance & PDF Reports)"]
    MOD_NOTIF["notifications & dashboard\n(In-App Notifications & Role Dashboards)"]
    MOD_INFRA["infrastructure & shared\n(MinIO, YOLO11/LLM Clients, SmartDroneHub & Payment Gateways)"]
  end

  subgraph DataAndStorage["Persistence & Object Storage Sub-Systems"]
    DB_PG[("PostgreSQL 17 + pgvector\n(36 Tables & Vector Index)")]
    STORE_MINIO[("MinIO Object Storage\n(inspection-evidence Bucket)")]
  end

  subgraph ExternalAndAI["External Systems & AI Services"]
    AI_SERVICE["YOLO11 Defect Detection Service\n(Python FastAPI & Ultralytics)"]
    LLM_GATEWAY["AI Vision, Summary & RAG Service\n(OpenAI-Compatible Gateway)"]
    DRONE_HUB["SmartDroneHub Service\n(Live Telemetry, Flight Trace & MP4 Video)"]
    PAY_GATEWAY["Online Payment Gateways\n(PayOS VietQR & VNPay v2.1.0)"]
    GOOGLE_OAUTH["Google OAuth 2.0\n(Federated Sign-In)"]
  end

  CLIENT_WEB -->|"HTTPS REST API & HttpOnly Cookies"| SEC_FILTER
  CLIENT_MOB -->|"HTTPS REST API & Bearer Tokens"| SEC_FILTER

  SEC_FILTER --> MOD_USERS
  SEC_FILTER --> MOD_CONTRACTS
  SEC_FILTER --> MOD_ASSETS
  SEC_FILTER --> MOD_INSP
  SEC_FILTER --> MOD_MAINT
  SEC_FILTER --> MOD_NOTIF

  MOD_CONTRACTS --> MOD_INFRA
  MOD_ASSETS --> MOD_INFRA
  MOD_INSP --> MOD_INFRA
  MOD_MAINT --> MOD_INFRA
  MOD_NOTIF --> MOD_INFRA

  MOD_INFRA -->|"JDBC / JPA & Vector Queries"| DB_PG
  MOD_INFRA -->|"S3 Object Streaming"| STORE_MINIO
  MOD_INFRA -->|"Multipart Image Defect Inference"| AI_SERVICE
  MOD_INFRA -->|"Vision Fallback, Summary & RAG"| LLM_GATEWAY
  MOD_INFRA <-->|"Telemetry, Flight Report & MP4 Sync"| DRONE_HUB
  MOD_INFRA <-->|"Payment Links & Signed Webhooks"| PAY_GATEWAY
  MOD_USERS <-->|"OAuth 2.0 Authorization"| GOOGLE_OAUTH
```

**Explanation of Architecture Components**

1. **Web Portal Application (`SmartDroneInspection-frontend`)**: Single-page web sub-system built with React 19.2.8, TypeScript 6.0.2, Vite, TanStack Query, Zustand, and Material UI. It delivers role-scoped workspaces (`/admin`, `/client`, `/operations`) for the five human roles (`ADMIN`, `MANAGER`, `CUSTOMER`, `INSPECTOR`, and `MAINTENANCE_ENGINEER`), supporting customer onboarding, asset and drone administration, service request negotiation, `SmartDroneHub` telemetry viewing, interactive video frame cropping, defect finding review, report publication, online payment (PayOS and VNPay), and maintenance governance.
2. **Mobile Field Application (`SmartDroneInspection-mobile`)**: Cross-platform mobile sub-system built with Flutter, Dart 3.13.2, Riverpod, GoRouter, and Dio for field personnel (`INSPECTOR` and `MAINTENANCE_ENGINEER`). It supports native mobile sign-in (`/api/v1/mobile/auth` with `flutter_secure_storage`), Google OAuth 2.0 deep links (`smartdrone://auth`), pre-flight airspace advisories (`AirspaceAdvisoryCard`), flight permit uploads, on-site field session tracking (`Start`, `Complete`, `Abort`), streaming photograph and MP4 video evidence uploads (`file_picker`), and maintenance work log execution.
3. **Application Server (`SmartDroneInspection-backend`)**: Modular monolith backend sub-system built with Java 21, Spring Boot 4.1.0, and Spring Modulith 2.1.1. It enforces role-based and organization-scoped authorization (`SecurityConfig`, `ActorZone`), domain state transitions, server-side A4 PDF report rendering (`OpenHTMLtoPDF`), security audit logging (`SecurityAuditService`), and transactional cross-module domain events (`event_publication`).
4. **YOLO11 Defect Detection Service (`ai-inference`)**: Containerized Python 3.11 FastAPI microservice running trained Ultralytics YOLO11 weights (`MBDD2025`) to detect five structural defect classes (`crack`, `leakage`, `abscission`, `corrosion`, and `bulge`) on inspection photographs and video keyframes, returning normalized bounding boxes and confidence scores.
5. **AI Vision, Executive Summary, and RAG Advisory Gateway**: External OpenAI-compatible language and vision service providing three advisory capabilities:
   - **Vision Fallback** (`PrimaryWithFallbackInference`, `OpenAiCompatibleInferenceClient`): Secondary image defect detection invoked when the primary YOLO11 service returns no detections or is unreachable.
   - **Executive Summary Generation** (`ReportDraftClient`): Synthesizes structured executive summaries from confirmed inspection findings, with a deterministic template fallback when offline.
   - **Maintenance RAG Advisor** (`MaintenanceScopeAdvisorClient`, `MaintenanceScopeAdvisorService`, `DeterministicScopeFallback`): Searches engineering standard excerpts stored in `repair_knowledge_chunks` to recommend repair scopes, initial maintenance tasks, standard construction cost norms, and completion compliance checks.
6. **SmartDroneHub Telemetry and Flight Video Service**: External drone ground-control and telemetry system accessed through `SmartDroneHubClient` and `InspectionDroneHubService`. It provides live mission telemetry, persists post-flight report metrics and GPS flight traces (`flight_trace_json`) into `field_sessions`, and synchronizes recorded mission MP4 videos into inspection `evidence`.
7. **Relational and Vector Database (PostgreSQL 17)**: Persists all 36 schema tables across Flyway migrations `V1`–`V28` (35 application tables plus `event_publication` for the Spring Modulith transactional outbox) and 1536-dimensional `pgvector` embeddings for engineering standards.
8. **Object Storage (MinIO)**: S3-compatible private bucket (`inspection-evidence`) managed through `MinioEvidenceObjectStore` to store signed service agreements, pilot license scans, 3-document drone registration files, asset engineering documents, flight permits, field photographs and MP4 videos, and published PDF reports.
9. **Online Payment Gateways (PayOS and VNPay) & Google OAuth 2.0**: External payment gateways (`PayOSPaymentGateway` VietQR with HMAC-SHA256 webhooks and `VnPayPaymentGateway` v2.1.0 with HMAC-SHA512 webhooks) for VND inspection fee settlement, and Google OAuth 2.0 (`OAuth2Controller`, `GoogleOAuthService`) for federated identity verification.

---

### 1.2 Package Diagram

SmartDroneInspection comprises three application sub-systems: the **Backend Application Server** (`com.smartdroneinspection`), the **Web Portal Application** (`SmartDroneInspection-frontend/src`), and the **Mobile Field Application** (`SmartDroneInspection-mobile/lib`). The package diagrams and package descriptions for each sub-system are presented below.

#### Backend Application Server Package Diagram

```mermaid
%% title: Backend Subsystem Package Diagram
flowchart TD
  subgraph RootPkg["com.smartdroneinspection"]
    USERS["users\n(Authentication, Sessions, Profiles, Rate Limit & Audit)"]
    WORKFORCE["workforce\n(Customer Maintenance Engineer Provisioning)"]
    CONTRACTS["contracts\n(Service Requests, VND Quotes, Agreements & PayOS/VNPay)"]
    ASSETS["assets\n(Asset Catalog, Customer Assets, Airspace & Owned Drones)"]
    INSPECTIONS["inspections\n(Inspections, Field Sessions, SmartDroneHub, Evidence, Findings & PDF Reports)"]
    MAINTENANCE["maintenance\n(Work Orders, RAG Advisor, Tasks, Work Logs, Acceptance & PDF Reports)"]
    NOTIFICATIONS["notifications\n(In-App Notification Inbox & Event Listeners)"]
    DASHBOARD["dashboard\n(Role-Scoped Operational Metrics)"]
    INFRASTRUCTURE["infrastructure\n(MinIO, YOLO11/LLM Clients, SmartDroneHub & Payment Gateways)"]
    SHARED["shared\n(SecurityConfig, Responses, Roles, Ports, Validation & Exceptions)"]
  end

  WORKFORCE --> USERS
  CONTRACTS --> ASSETS
  CONTRACTS --> USERS
  CONTRACTS --> INSPECTIONS
  ASSETS --> USERS
  INSPECTIONS --> ASSETS
  INSPECTIONS --> USERS
  MAINTENANCE --> INSPECTIONS
  MAINTENANCE --> USERS
  NOTIFICATIONS -.->|"Domain Events"| INSPECTIONS
  NOTIFICATIONS -.->|"Domain Events"| MAINTENANCE
  INSPECTIONS <-->|"Re-inspection Events & SPI"| MAINTENANCE
  DASHBOARD --> ASSETS
  DASHBOARD --> INSPECTIONS
  DASHBOARD --> MAINTENANCE
  USERS --> SHARED
  CONTRACTS --> SHARED
  ASSETS --> SHARED
  INSPECTIONS --> SHARED
  MAINTENANCE --> SHARED
  NOTIFICATIONS --> SHARED
  INFRASTRUCTURE --> SHARED
```

**Package Descriptions (Backend Application Server)**

| No | Package | Description |
| :---: | :--- | :--- |
| 01 | `com.smartdroneinspection.users` | Manages user authentication (password, `OtpChallenge` verification, and Google OAuth 2.0), active sessions (`AuthSession`), JWT/refresh cookies (`AccessTokenService`, `RefreshCookieService`), IP rate limiting (`AuthRateLimitFilter`), account lockout (`LoginFailureService`), security audit logging (`SecurityAuditService`), Inspector profiles (`InspectorProfile`) and flight logs (`InspectorFlightLog`), customer airspace registration reviews (`ProspectiveCustomerRegistration`), and platform user administration. |
| 02 | `com.smartdroneinspection.workforce` | Allows Customer organization accounts (`WorkforceController`, `WorkforceService`) to provision and manage `MAINTENANCE_ENGINEER` accounts scoped strictly to their own customer organization. |
| 03 | `com.smartdroneinspection.contracts` | Manages one-time and recurring inspection service requests (`ServiceRequest`), order chat messages (`ServiceRequestMessage`), versioned VND quotations (`ServiceRequestQuote`), signed service agreement files, inspection occurrence dispatch (`ServiceRequestOccurrence`), platform finance rates (`InspectionFinanceSettings`), and PayOS/VNPay online payment checkout and webhook processing. |
| 04 | `com.smartdroneinspection.assets` | Manages global asset categories (`AssetCategory`), customer infrastructure assets (`Asset`) and inspection checkpoints, engineering reference documents (`AssetDocument`), Vietnam airspace evaluations (`AirspaceAdvisoryService`), and Inspector-owned drone registrations (`DroneRegistrationApplication`, `Drone`). |
| 05 | `com.smartdroneinspection.inspections` | Coordinates scheduled inspection missions (`Inspection`), flight permit uploads, on-site field sessions (`FieldSession`), `SmartDroneHub` live telemetry and flight video sync (`InspectionDroneHubService`), manager recovery dispatch after aborted sessions, photograph and MP4 video evidence (`Evidence`), AI defect analysis and confirmed findings (`Finding`), 4-state inspection report compilation/publication (`InspectionReport`), server-side PDF rendering (`PdfReportRenderer`), and three-way re-inspection verification (`ReinspectionDefectVerification`). |
| 06 | `com.smartdroneinspection.maintenance` | Governs 12-state corrective maintenance work orders (`MaintenanceWorkOrder`), repair team allocation (`MaintenanceTeamMember`), `pgvector` RAG-assisted repair scope and cost estimation (`MaintenanceScopeAdvisorService`, `DeterministicScopeFallback`), versioned estimates (`MaintenanceEstimateVersion`), cost lines (`MaintenanceCostLine`), change orders (`MaintenanceChangeOrder`), task work logs (`MaintenanceWorkLog`) and batch verification, maintenance completion reports (`MaintenanceReportVersion`, `MaintenanceReportRenderer`), customer acceptance decisions (`MaintenanceAcceptanceDecision`), and cost reconciliation. |
| 07 | `com.smartdroneinspection.notifications` | Delivers deduplicated in-app notifications (`NotificationController`, `NotificationService`) to users in response to domain events published by `inspections` (`InspectionNotificationListener`) and `maintenance` (`MaintenanceNotificationListener`). |
| 08 | `com.smartdroneinspection.dashboard` | Aggregates operational summaries, mission queues, asset health indicators, and maintenance budget metrics (`DashboardController`, `DashboardAnalyticsService`) tailored to each of the five user roles. |
| 09 | `com.smartdroneinspection.infrastructure` | Implements technical outbound adapters for MinIO object storage (`MinioEvidenceObjectStore`), YOLO11 and OpenAI-compatible AI clients (`YoloInferenceClient`, `OpenAiCompatibleInferenceClient`, `PrimaryWithFallbackInference`, `ReportDraftClient`, `MaintenanceScopeAdvisorClient`), `SmartDroneHub` telemetry/video integration (`SmartDroneHubClient`), and PayOS/VNPay payment gateways (`PayOSPaymentGateway`, `VnPayPaymentGateway`). |
| 10 | `com.smartdroneinspection.shared` | Provides cross-cutting HTTP security configuration (`SecurityConfig`), shared API response wrappers (`ApiResponse`, `Result`), role constants (`Roles`), cross-module service ports (`EvidenceObjectStore`, `AiInferencePort`, `SmartDroneHubPort`, `PayOSPaymentPort`, `VnPayPaymentPort`), file upload validation (`EvidenceUploadValidator`), RFC 7807 error handling (`GlobalExceptionHandler`), and bilingual localization (`RequestLocale`). |

#### Web Portal Application Package Diagram

```mermaid
%% title: Web Portal Subsystem Package Diagram
flowchart TD
  subgraph WebRoot["SmartDroneInspection-frontend/src"]
    APP["app\n(AppShell, Router, Role AccessPolicy & Theme)"]
    FEAT_AUTH["features/auth\n(Login, Register, OTP, OAuthCallback & RequireAuth)"]
    FEAT_ADMIN["features/admin\n(Platform Users, Airspace/Drone Reviews & Finance Settings)"]
    FEAT_WORKFORCE["features/workforce\n(Customer Maintenance Engineer Management)"]
    FEAT_ASSETS["features/assets\n(Asset Catalog, Asset Documents & Owned Drones)"]
    FEAT_CONTRACTS["features/contracts\n(Service Requests, Order Chat, VND Quotes & Agreements)"]
    FEAT_INSP["features/inspections\n(Schedule Calendar, Field Sessions, SmartDroneHub & Findings)"]
    FEAT_REPORTS["features/reports\n(Report Review, PDF Export & PayOS/VNPay Checkout)"]
    FEAT_MAINT["features/maintenance\n(Work Orders, RAG Advisor, Work Logs & Acceptance)"]
    FEAT_NOTIF["features/notifications & dashboard & landing\n(NotificationBell, 5-Role Dashboard & Landing Portal)"]
    WEB_SHARED["shared\n(Axios Client, AirspaceNoFlyMap, LocaleProvider & UI Components)"]
  end

  APP --> FEAT_AUTH
  APP --> FEAT_ADMIN
  APP --> FEAT_WORKFORCE
  APP --> FEAT_ASSETS
  APP --> FEAT_CONTRACTS
  APP --> FEAT_INSP
  APP --> FEAT_REPORTS
  APP --> FEAT_MAINT
  APP --> FEAT_NOTIF
  FEAT_AUTH --> WEB_SHARED
  FEAT_ADMIN --> WEB_SHARED
  FEAT_WORKFORCE --> WEB_SHARED
  FEAT_ASSETS --> WEB_SHARED
  FEAT_CONTRACTS --> WEB_SHARED
  FEAT_INSP --> WEB_SHARED
  FEAT_REPORTS --> WEB_SHARED
  FEAT_MAINT --> WEB_SHARED
  FEAT_NOTIF --> WEB_SHARED
```

**Package Descriptions (Web Portal Application)**

| No | Package | Description |
| :---: | :--- | :--- |
| 01 | `src/app` | Contains application-wide shell layouts (`AppShell`), route configuration (`router`), 5-role route access policies (`accessPolicy.ts`, `capability.ts`), and dark/light theme tokens (`ColorModeContext`). |
| 02 | `src/features/auth` | Implements customer organization registration (`RegisterPage`), email/password and OTP sign-in (`LoginPage`), Google OAuth 2.0 callback handling (`OAuthCallbackPage`), session bootstrapping (`AuthSessionBootstrapper`), and route guards (`RequireAuth`). |
| 03 | `src/features/admin` & `src/features/workforce` | Provide platform account administration (`PlatformUsersPage`), restricted-airspace and drone registration review queues (`Mf1ReviewPage`), platform finance settings (`PlatformFinanceSettingsPage`), and Customer `MAINTENANCE_ENGINEER` provisioning (`WorkforcePage`). |
| 04 | `src/features/assets` | Provides infrastructure asset management (`AssetsPage`), reference document streaming (`documentApi.ts`), and Inspector-owned drone registration and inventory (`DroneInventoryPanel`). |
| 05 | `src/features/contracts` | Implements one-time and recurring service requests, in-context Order Chat, VND quotation issuance and acceptance, signed contract upload, and occurrence dispatch (`ContractsPage`). |
| 06 | `src/features/inspections` | Implements the Inspector Schedule Calendar (`InspectorScheduleCalendar`), Customer 5-Stage Progress Tracker (`InspectionProgressPage`), on-site field session & `SmartDroneHub` telemetry controls (`FieldSessionPage`), photo/MP4 evidence upload (`InspectionEvidencePage`), and YOLO11 defect review (`InspectionFindingsPage`). |
| 07 | `src/features/reports` | Implements pre-submission report preview (`InspectionDraftPage`), independent Manager review and direct publication, on-demand PDF download, PayOS VietQR and VNPay online payment checkout (`ReportDetailPage`), and defect forwarding (`CorrectiveDispositionPage`). |
| 08 | `src/features/maintenance` | Implements the 12-state maintenance work order workspace (`MaintenancePage`), including `pgvector` RAG scope/cost norms suggestions, team assignment, change orders, batch work-log verification, auto-drafted completion reports, 3-way re-inspection review, and cost reconciliation. |
| 09 | `src/features/notifications`, `dashboard` & `landing` | Provide the in-app notification inbox (`NotificationBell`), 5-role operational analytics dashboard (`DashboardPage`), and public/role landing console (`LandingPage`). |
| 10 | `src/shared` | Provides the shared Axios HTTP client with automatic token refresh and CSRF handling (`shared/api`), interactive Vietnam airspace map (`AirspaceNoFlyMap`), bilingual EN/VI localization (`LocaleProvider`), and authenticated media components (`AuthenticatedImage`, `AuthenticatedMedia`). |

#### Mobile Field Application Package Diagram

```mermaid
%% title: Mobile Field Subsystem Package Diagram
flowchart TD
  subgraph MobRoot["SmartDroneInspection-mobile/lib"]
    MOB_CORE["core\n(Dio Network Client, TokenStore, GoRouter, Theme & Localization)"]
    MOB_AUTH["features/auth\n(LoginPage, OAuthCallbackScreen & SessionProvider)"]
    MOB_ASSETS["features/assets\n(AssetsPage, AssetRepository & Asset Models)"]
    MOB_INSP["features/inspections\n(InspectionsPage, AirspaceAdvisoryCard, FieldSessionPage & Evidence Upload)"]
    MOB_TASKS["features/tasks\n(TasksPage, WorkOrderDetailPage, RecordWorkLogSheet & MaintenanceRepository)"]
    MOB_PROFILE["features/profile\n(ProfilePage & Language Selector)"]
    MOB_SHARED["shared/widgets & l10n\n(CommonWidgets, AsyncValueWidget & EN/VI AppLocalizations)"]
  end

  MOB_AUTH --> MOB_CORE
  MOB_ASSETS --> MOB_CORE
  MOB_INSP --> MOB_CORE
  MOB_TASKS --> MOB_CORE
  MOB_PROFILE --> MOB_CORE
  MOB_AUTH --> MOB_SHARED
  MOB_ASSETS --> MOB_SHARED
  MOB_INSP --> MOB_SHARED
  MOB_TASKS --> MOB_SHARED
  MOB_PROFILE --> MOB_SHARED
```

**Package Descriptions (Mobile Field Application)**

| No | Package | Description |
| :---: | :--- | :--- |
| 01 | `lib/core` | Provides the shared Dio HTTP client (`auth_interceptor.dart`, `api_response_interceptor.dart`, `locale_header_interceptor.dart`), secure token storage (`token_store.dart` via `flutter_secure_storage`), application routing (`app_router.dart`), environment configuration (`app_environment.dart`), and theme/localization providers. |
| 02 | `lib/features/auth` | Implements mobile credential sign-in (`login_page.dart`), Google OAuth 2.0 deep-link callback handling (`oauth_callback_screen.dart`), and Riverpod session state management (`session_provider.dart`, `auth_repository.dart`). |
| 03 | `lib/features/assets` | Displays organization and assigned infrastructure assets, coordinates, and inspection checkpoints (`assets_page.dart`, `asset_repository.dart`). |
| 04 | `lib/features/inspections` | Implements assigned inspection mission queues (`inspections_page.dart`), pre-flight Vietnam airspace radar advisories (`airspace_advisory_card.dart`), flight permit upload, on-site field session execution (`field_session_page.dart`), and streaming photograph/MP4 evidence uploads (`inspection_repository.dart`). |
| 05 | `lib/features/tasks` | Implements Maintenance Engineer work order and task queues (`tasks_page.dart`, `work_order_detail_page.dart`), work order release/start, field work log recording (`record_work_log_sheet.dart`), Team Lead verification, and completion declaration (`maintenance_repository.dart`). |
| 06 | `lib/features/profile`, `lib/shared` & `lib/l10n` | Provide user profile and language switching (`profile_page.dart`), reusable asynchronous state widgets (`async_value_widget.dart`, `common_widgets.dart`), and generated English/Vietnamese localization bundles (`app_localizations_en.dart`, `app_localizations_vi.dart`). |
