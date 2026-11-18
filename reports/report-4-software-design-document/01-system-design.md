---
title: "Report 4 - System Design"
document_type: report4-sdd-section
weight: 15
source: "report4-software-design-document.docx"
---

# II. Software Design Document

## 1. System Design

### 1.1 System Architecture

**Current application scope:** Four login roles (`ADMIN`, `MANAGER`, `CUSTOMER`, `INSPECTOR`), eight active features (`FE-01`–`FE-08`) grouped as two per main flow across `MF1`–`MF4`. The inspection scope is buildings only. Corrective maintenance is neither modelled nor exposed: no maintenance package, class, table, or endpoint exists in the delivered codebase. Re-inspection against a published report is modelled, and is designed under `FE-08`.

SmartDroneInspection uses a modular client-server architecture that separates the client presentation sub-systems (Web Portal Application and Mobile Field Application), the modular monolith backend application server (Java 21 and Spring Boot 4.1 with Spring Modulith), the persistence and object storage layer (PostgreSQL 17 and MinIO object storage), and external or containerized systems (YOLO11 defect detection service, OpenAI-compatible vision and narrative-drafting gateway, SmartDroneHub telemetry and flight video service, PayOS and VNPay payment gateways, and Google OAuth 2.0).

```mermaid
%% title: System Architecture Diagram
flowchart TD
  subgraph Clients["Client Presentation Sub-Systems"]
    CLIENT_WEB["Web Portal Application\n(React 19, TypeScript, Material UI)"]
    CLIENT_MOB["Mobile Field Application\n(Flutter, Dart, Riverpod)"]
  end

  subgraph Backend["Application Server Sub-System (Java 21 & Spring Boot Modulith)"]
    SEC_FILTER["Security & Access Filter\n(SecurityConfig, JWT, OAuth 2.0, CSRF & AuthRateLimitFilter)"]
    MOD_USERS["users\n(Identity, 4-Role Access, Profiles, Applications & Audit)"]
    MOD_CONTRACTS["contracts\n(Service Requests, VND Quotations, Agreements, Dispatch & Billing)"]
    MOD_ASSETS["assets\n(Building Assets, Categories, Airspace Advisory & Owned Drones)"]
    MOD_INSP["inspections\n(Flight Permits, Field Sessions, Evidence, Findings & PDF Reports)"]
    MOD_NOTIF["notifications & dashboard\n(In-App Notifications & Role Dashboards)"]
    MOD_INFRA["infrastructure & shared\n(MinIO, YOLO11/LLM Clients, SmartDroneHub & Payment Gateways)"]
  end

  subgraph DataAndStorage["Persistence & Object Storage Sub-Systems"]
    DB_PG[("PostgreSQL 17\n(41 Tables, No Vector Store)")]
    STORE_MINIO[("MinIO Object Storage\n(inspection-evidence Bucket)")]
  end

  subgraph ExternalAndAI["External Systems & AI Services"]
    AI_SERVICE["YOLO11 Defect Detection Service\n(Python FastAPI & Ultralytics)"]
    LLM_GATEWAY["AI Vision & Narrative Drafting\n(OpenAI-Compatible Gateway)"]
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
  SEC_FILTER --> MOD_NOTIF

  MOD_CONTRACTS --> MOD_INFRA
  MOD_ASSETS --> MOD_INFRA
  MOD_INSP --> MOD_INFRA
  MOD_NOTIF --> MOD_INFRA

  MOD_INFRA -->|"JDBC / JPA"| DB_PG
  MOD_INFRA -->|"S3 Object Streaming"| STORE_MINIO
  MOD_INFRA -->|"Multipart Image Defect Inference"| AI_SERVICE
  MOD_INFRA -->|"Vision Fallback & Narrative Drafting"| LLM_GATEWAY
  MOD_INFRA <-->|"Telemetry, Flight Report & MP4 Sync"| DRONE_HUB
  MOD_INFRA <-->|"Payment Links & Signed Webhooks"| PAY_GATEWAY
  MOD_USERS <-->|"OAuth 2.0 Authorization"| GOOGLE_OAUTH
```

**Explanation of Architecture Components**

1. **Web Portal Application (`SmartDroneInspection-frontend`)**: Single-page web sub-system built with React 19, strict TypeScript, Vite, and Material UI. It delivers four role-scoped portals (`/admin`, `/manager`, `/client`, `/operations`) for the four human roles. A section a role may not use has no route at all, so denial is enforced at the routing boundary by `accessPolicy.ts` as well as at the API. The web application is the only client for `ADMIN`, `MANAGER`, and `INSPECTOR`; every field, commercial, and review task is performed here.
2. **Mobile Field Application (`SmartDroneInspection-mobile`)**: Cross-platform mobile sub-system built with Flutter, Dart, Riverpod, GoRouter, and Dio. It is **Customer-only**: `session_provider.dart` and `auth_user.dart` restrict entry to `CUSTOMER` accounts, and the network layer returns the `CUSTOMER_ONLY_MOBILE` error code for any other role. It covers sign-in, organization registration, buildings, service requests with order chat, inspection tracking, published reports, and notifications. Inspectors record field sessions through the operations web portal, not the mobile application.
3. **Application Server (`SmartDroneInspection-backend`)**: Modular monolith backend sub-system built with Java 21, Spring Boot 4.1.0, and Spring Modulith 2.1.1 across eight modules. It enforces role-based and organization-scoped authorization (`SecurityConfig`, `ActorZone`), domain state transitions, server-side A4 PDF report rendering (openhtmltopdf), security audit logging (`SecurityAuditService`), and transactional cross-module domain events through the Modulith `event_publication` outbox. Module boundaries are declared per module in `package-info.java` and asserted by `ModulithArchitectureTest`, so an undeclared cross-module dependency fails the build.
4. **YOLO11 Defect Detection Service (`ai-inference`)**: Containerized Python FastAPI microservice running trained Ultralytics YOLO11s weights (`MBDD2025`) to detect five building-defect classes (`crack`, `leakage`, `abscission`, `corrosion`, `bulge`) on inspection photographs and video keyframes, returning normalized bounding boxes and confidence scores.
5. **AI Vision and Narrative Drafting Gateway**: External OpenAI-compatible language and vision service providing two advisory capabilities:
   - **Vision Fallback** (`PrimaryWithFallbackInference`, `OpenAiCompatibleInferenceClient`): Secondary image defect detection invoked when the primary YOLO11 service returns no detections or is unreachable. A user may opt out of the fallback for their own account through `vision_fallback_enabled`.
   - **Narrative Drafting** (`ReportDraftClient`): A single-shot request that turns the confirmed inspection context into structured narrative text for the executive summary. It is not a retrieval-augmented system; no document corpus is searched, and no embedding is computed.
6. **SmartDroneHub Telemetry and Flight Video Service**: External drone ground-control and telemetry system accessed through `SmartDroneHubClient` and `InspectionDroneHubService`. It supplies read-only live mission telemetry, persists post-flight report metrics and GPS flight traces (`flight_trace_json`) into `field_sessions`, and synchronizes recorded mission MP4 videos into inspection `evidence`. The platform never sends flight commands to it.
7. **Relational Database (PostgreSQL 17)**: Persists the 41-table relational schema through Flyway migrations `V1__baseline.sql` and `V2__remove_finding_recommended_action.sql`. `V1` is a consolidated baseline holding the complete current schema and the catalog seeds; `V2` is a forward migration that merges the former `recommended_action` column into `technical_notes` and drops it. A test asserts the applied migration set is exactly `["1","2"]`, so an accidental renumbering fails the build. **The schema contains no vector column**: the `pgvector` extension is created conditionally for image compatibility but no embedding is ever stored, and there is no retrieval-augmented query path.
8. **Object Storage (MinIO)**: S3-compatible private bucket (`inspection-evidence`) managed through `MinioEvidenceObjectStore` to store signed service agreements, chat attachments, pilot licence scans, three-document drone registration files, building engineering documents, flight permits, field photographs and MP4 videos, and published PDF reports. Binary content is served only through short-lived HMAC media tickets and HTTP Range streaming.
9. **Online Payment Gateways (PayOS and VNPay) & Google OAuth 2.0**: External payment gateways (`PayOSPaymentGateway` VietQR with HMAC-SHA256 webhooks and `VnPayPaymentGateway` v2.1.0 with HMAC-SHA512 webhooks) for VND inspection fee settlement, and Google OAuth 2.0 (`OAuth2Controller`, `GoogleOAuthService`) for federated identity. Both payment gateways are configuration-gated and disabled by default; the application starts and remains operable without them.

**Component responsibilities**

| Component | Technology | Responsibility |
| :--- | :--- | :--- |
| Web Portal Application | React 19, strict TypeScript, Vite, Material UI | Four role-scoped portals; route-level denial; all administrative, commercial, field, and review work. |
| Mobile Field Application | Flutter, Dart, Riverpod, GoRouter, Dio | Customer-only mobile access to buildings, requests, tracking, reports, and notifications. |
| Application Server | Java 21, Spring Boot 4.1.0, Spring Modulith 2.1.1 | Domain logic, authorization, state transitions, PDF rendering, audit, and event publication. |
| YOLO11 Detection Service | Python FastAPI, Ultralytics YOLO11s | Primary building-defect candidate detection over photographs and video keyframes. |
| Vision & Drafting Gateway | OpenAI-compatible HTTP API | Vision fallback detection and single-shot narrative drafting. |
| SmartDroneHub | External ground station | Read-only telemetry, flight traces, and mission video. |
| PostgreSQL | PostgreSQL 17 | 41-table relational persistence, audit trail, and event outbox. |
| MinIO | S3-compatible object storage | Private storage of documents, evidence media, and published PDF reports. |
| PayOS / VNPay / Google OAuth 2.0 | External HTTPS services | Service-fee settlement and federated sign-in. |

### 1.2 Package Diagram

SmartDroneInspection comprises three application sub-systems: the **Backend Application Server** (`com.smartdroneinspection`), the **Web Portal Application** (`SmartDroneInspection-frontend/src`), and the **Mobile Field Application** (`SmartDroneInspection-mobile/lib`). The package diagrams and package descriptions for each sub-system are presented below.

#### 1.2.1 Backend Application Server Package Diagram

```mermaid
%% title: Backend Subsystem Package Diagram
flowchart TD
  subgraph RootPkg["com.smartdroneinspection"]
    USERS["users\n(Authentication, Sessions, Profiles, Applications & Audit)"]
    CONTRACTS["contracts\n(Service Requests, VND Quotes, Agreements, Dispatch & PayOS/VNPay)"]
    ASSETS["assets\n(Asset Catalog, Building Assets, Airspace Advisory & Owned Drones)"]
    INSPECTIONS["inspections\n(Inspections, Field Sessions, Evidence, Findings & PDF Reports)"]
    NOTIFICATIONS["notifications\n(In-App Notification Inbox & Event Listeners)"]
    DASHBOARD["dashboard\n(Role-Scoped Operational Metrics)"]
    INFRASTRUCTURE["infrastructure\n(MinIO, YOLO11/LLM Clients, SmartDroneHub & Payment Gateways)"]
    SHARED["shared\n(SecurityConfig, Responses, Roles, Ports, Validation & Exceptions)"]
  end

  CONTRACTS --> ASSETS
  CONTRACTS --> USERS
  CONTRACTS --> INSPECTIONS
  ASSETS --> USERS
  INSPECTIONS --> ASSETS
  INSPECTIONS --> USERS
  NOTIFICATIONS -.->|"Domain Events"| INSPECTIONS
  DASHBOARD --> ASSETS
  DASHBOARD --> INSPECTIONS
  USERS --> SHARED
  CONTRACTS --> SHARED
  ASSETS --> SHARED
  INSPECTIONS --> SHARED
  NOTIFICATIONS --> SHARED
  INFRASTRUCTURE --> SHARED
  INFRASTRUCTURE -.->|"SPI / Gateway Ports"| INSPECTIONS
  INFRASTRUCTURE -.->|"Gateway Ports"| CONTRACTS
```

The eight modules declare their permitted collaborators in `@ApplicationModule(allowedDependencies = {...})`. `contracts` may reach `assets::domain`, `assets::enums`, `assets::repository`, `users`, and `inspections::spi`; `inspections` may reach `assets::domain`, `assets::enums`, `assets::repository`, `assets::reportcontext`, `users`, and its own `reportcontext`; `notifications` may reach `inspections::events` and `users::events`; `infrastructure` may reach `inspections::spi` and `contracts::gateway`. Directional control therefore passes through narrow named sub-packages rather than whole modules.

**Package Descriptions**

| No | Package | Description |
| :---: | :--- | :--- |
| 01 | `com.smartdroneinspection.users` | Manages user authentication (password, `OtpChallenge` verification, and Google OAuth 2.0), active sessions (`AuthSession`), JWT and refresh cookies (`AccessTokenService`, `RefreshCookieService`), IP rate limiting (`AuthRateLimitFilter`), account lockout (`LoginFailureService`), security audit logging (`SecurityAuditService`), Inspector profiles (`InspectorProfile`) and flight logs (`InspectorFlightLog`), the public partner Inspector application and its review into a provisioned account (`InspectorApplication`), customer airspace registration reviews (`ProspectiveCustomerRegistration`), and platform user administration. |
| 02 | `com.smartdroneinspection.contracts` | Manages one-time and recurring inspection service requests (`ServiceRequest`), order chat messages and their private attachments (`ServiceRequestMessage`, `ServiceRequestMessageAttachment`), versioned VND quotations (`ServiceRequestQuote`), signed service agreement files, inspection occurrence dispatch (`ServiceRequestOccurrence`), platform finance rates (`InspectionFinanceSettings`), and PayOS/VNPay online payment checkout and webhook processing. |
| 03 | `com.smartdroneinspection.assets` | Manages global building asset categories (`AssetCategory`), customer building assets (`Asset`), category-scoped inspection checkpoints (`InspectionItem`), building reference documents (`AssetDocument`), Vietnam airspace evaluation (`AirspaceAdvisoryService`), drone document and feature configuration (`DroneDocumentConfig`, `DroneFeatureConfig`), and Inspector-owned drone registration and approval (`DroneRegistrationApplication`, `Drone`). |
| 04 | `com.smartdroneinspection.inspections` | Coordinates scheduled inspection missions (`Inspection`), the flight-permit upload and independent verification gate, on-site field sessions (`FieldSession`), `SmartDroneHub` telemetry and flight-video sync (`InspectionDroneHubService`), Manager recovery dispatch after an aborted session, photograph and MP4 evidence with resumable uploads (`Evidence`, `EvidenceUploadSession`), YOLO11 defect analysis and confirmed findings (`Finding`), the four-state inspection report (`InspectionReport`), and deterministic A4 PDF rendering (`PdfReportRenderer`). |
| 05 | `com.smartdroneinspection.notifications` | Delivers deduplicated in-app notifications (`NotificationController`, `NotificationService`) to users in response to domain events published by `inspections` and `users`, with a deduplication key that prevents a retried event from producing a duplicate notice. |
| 06 | `com.smartdroneinspection.dashboard` | Aggregates operational summaries, mission queues, and asset health indicators (`DashboardController`, `DashboardAnalyticsService`) tailored to each of the four user roles. |
| 07 | `com.smartdroneinspection.infrastructure` | Implements technical outbound adapters for MinIO object storage (`MinioEvidenceObjectStore`), YOLO11 and OpenAI-compatible AI clients (`YoloInferenceClient`, `OpenAiCompatibleInferenceClient`, `PrimaryWithFallbackInference`, `ReportDraftClient`), `SmartDroneHub` telemetry and video integration (`SmartDroneHubClient`), FFmpeg video processing, and PayOS/VNPay payment gateways (`PayOSPaymentGateway`, `VnPayPaymentGateway`). |
| 08 | `com.smartdroneinspection.shared` | Provides cross-cutting HTTP security configuration (`SecurityConfig`), shared API response wrappers (`ApiResponse`, `Result`), role constants (`Roles`), cross-module service ports (`EvidenceObjectStore`, `AiInferencePort`, `SmartDroneHubPort`, payment ports), upload validation (`EvidenceUploadValidator`), RFC 7807 error handling (`GlobalExceptionHandler`), and bilingual localization (`RequestLocale`). |

#### 1.2.2 Web Portal Application Package Diagram

```mermaid
%% title: Web Portal Subsystem Package Diagram
flowchart TD
  subgraph WebRoot["SmartDroneInspection-frontend/src"]
    APP["app\n(AppShell, Router, AccessPolicy, Capability & Theme)"]
    FEAT_AUTH["features/auth\n(Login, Register, OTP, OAuthCallback & RequireAuth)"]
    FEAT_ADMIN["features/admin\n(Platform Users, Licence Classes, Drone Config & Reviews)"]
    FEAT_LANDING["features/landing\n(Public Landing & Portal Selection)"]
    FEAT_ASSETS["features/assets\n(Asset Catalog, Asset Documents & Owned Drones)"]
    FEAT_CONTRACTS["features/contracts\n(Service Requests, Order Chat, VND Quotes & Agreements)"]
    FEAT_INSP["features/inspections\n(Schedule Calendar, Field Sessions, SmartDroneHub & Findings)"]
    FEAT_REPORTS["features/reports\n(Report Draft, Independent Review & PDF Download)"]
    FEAT_DASH["features/dashboard\n(Operational Metrics)"]
    FEAT_NOTIF["features/notifications\n(Notification Inbox & Badge)"]
    WEB_SHARED["shared\n(Axios Client, Airspace Maps, i18n & UI Kit)"]
  end

  APP --> FEAT_AUTH
  APP --> FEAT_ADMIN
  APP --> FEAT_LANDING
  APP --> FEAT_ASSETS
  APP --> FEAT_CONTRACTS
  APP --> FEAT_INSP
  APP --> FEAT_REPORTS
  APP --> FEAT_DASH
  APP --> FEAT_NOTIF
  FEAT_AUTH --> WEB_SHARED
  FEAT_ADMIN --> WEB_SHARED
  FEAT_ASSETS --> WEB_SHARED
  FEAT_CONTRACTS --> WEB_SHARED
  FEAT_INSP --> WEB_SHARED
  FEAT_REPORTS --> WEB_SHARED
  FEAT_DASH --> WEB_SHARED
  FEAT_NOTIF --> WEB_SHARED
```

**Package Descriptions**

| No | Package | Description |
| :---: | :--- | :--- |
| 01 | `src/app` | Contains the application shell (`AppShell`), route configuration (`router.tsx`), the four-portal route access policy (`accessPolicy.ts`), capability helpers (`capability.ts`), portal selection (`PortalSelectionPage`), and design tokens and theme (`tokens.ts`, `theme.ts`, `ColorModeContext`). |
| 02 | `src/features/auth` | Implements customer organization registration, partner Inspector application submission, email/password and OTP sign-in, Google OAuth 2.0 callback handling, session bootstrapping, and route guards (`RequireAuth`). |
| 03 | `src/features/admin` | Provides platform account administration, pilot-licence class maintenance, drone document and feature configuration, platform finance settings, AI inference settings, and the airspace, partner-application, and drone-registration review queues. |
| 04 | `src/features/landing` | Provides the public landing experience and the role-aware entry point into the four portals. |
| 05 | `src/features/assets` | Provides building asset management, reference document streaming, and Inspector-owned drone registration and inventory. |
| 06 | `src/features/contracts` | Implements one-time and recurring service requests, in-context order chat with attachments, VND quotation issuance and acceptance, signed contract upload, and occurrence dispatch, with separate `customer` and `manager` presentation branches. |
| 07 | `src/features/inspections` | Implements the Inspector schedule calendar, the customer inspection progress view, on-site field session and `SmartDroneHub` telemetry controls, flight-permit upload and review, photo and MP4 evidence upload, and YOLO11 defect review. |
| 08 | `src/features/reports` | Implements pre-submission report drafting, independent Manager review and publication, and on-demand PDF download. |
| 09 | `src/features/dashboard`, `src/features/notifications` | Provide four-role operational metrics and the in-app notification inbox with unread badge. |
| 10 | `src/shared` | Provides the Axios HTTP client with automatic token refresh, CSRF handling, and RFC 7807 problem parsing (`api`), the interactive Vietnam airspace planner and map (`airspace`), bilingual EN/VI localization (`i18n`), and the shared UI kit including authenticated media components (`ui`, `AuthenticatedImage`, `AuthenticatedMedia`). |

#### 1.2.3 Mobile Field Application Package Diagram

```mermaid
%% title: Mobile Field Subsystem Package Diagram
flowchart TD
  subgraph MobRoot["SmartDroneInspection-mobile/lib"]
    MOB_CORE["core\n(Dio Network, TokenStore, GoRouter, Theme & Localization)"]
    MOB_AUTH["features/auth\n(LoginPage, OAuthCallback & SessionProvider)"]
    MOB_ASSETS["features/assets\n(AssetsPage & AssetRepository)"]
    MOB_CONTRACTS["features/contracts\n(RequestsPage, NewRequest & RequestChat)"]
    MOB_INSP["features/inspections\n(InspectionsPage & InspectionDetail)"]
    MOB_DASH["features/dashboard\n(Customer Home)"]
    MOB_NOTIF["features/notifications\n(Notification List)"]
    MOB_PROFILE["features/profile\n(ProfilePage & Language Selector)"]
    MOB_SHARED["shared/widgets & l10n\n(AsyncValueWidget & EN/VI Localizations)"]
  end

  MOB_AUTH --> MOB_CORE
  MOB_ASSETS --> MOB_CORE
  MOB_CONTRACTS --> MOB_CORE
  MOB_INSP --> MOB_CORE
  MOB_DASH --> MOB_CORE
  MOB_NOTIF --> MOB_CORE
  MOB_PROFILE --> MOB_CORE
  MOB_AUTH --> MOB_SHARED
  MOB_ASSETS --> MOB_SHARED
  MOB_CONTRACTS --> MOB_SHARED
  MOB_INSP --> MOB_SHARED
  MOB_DASH --> MOB_SHARED
  MOB_NOTIF --> MOB_SHARED
  MOB_PROFILE --> MOB_SHARED
```

**Package Descriptions**

| No | Package | Description |
| :---: | :--- | :--- |
| 01 | `lib/core` | Provides the shared Dio HTTP client with authentication, API-response, and locale-header interceptors (`network`), secure token storage (`flutter_secure_storage`), application routing (`app_router.dart`), environment configuration (`env`), and theme and localization providers. |
| 02 | `lib/features/auth` | Implements mobile credential sign-in, Google OAuth 2.0 deep-link callback handling, and Riverpod session state. `session_provider.dart` enforces that only `CUSTOMER` accounts enter the application; the network layer raises `CUSTOMER_ONLY_MOBILE` for any other role. |
| 03 | `lib/features/assets` | Displays the organization's building assets, coordinates, and inspection checkpoints, with `data`, `domain`, and `presentation` layers. |
| 04 | `lib/features/contracts` | Implements the customer service-request list, new-request submission, request detail, and order-chat conversation. |
| 05 | `lib/features/inspections` | Implements the customer inspection list and inspection detail, including the published report and its findings. |
| 06 | `lib/features/dashboard`, `lib/features/notifications` | Provide the customer home summary and the in-app notification list. |
| 07 | `lib/features/profile`, `lib/shared` & `lib/l10n` | Provide user profile viewing and language switching, reusable asynchronous state widgets, and generated English/Vietnamese localization bundles from `app_en.arb` and `app_vi.arb`. |
