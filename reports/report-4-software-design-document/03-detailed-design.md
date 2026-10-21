---
title: "Report 4 - Detailed Design"
document_type: report4-sdd-section
weight: 35
source: "report4-software-design-document.docx"
---

## 3. Detailed Design

### 3.1 Identity, Enterprise Subscription and Workforce Governance

#### 3.1.1 Class Diagram

```mermaid
%% title: Identity and Workforce Management Class Diagram
classDiagram
  class AuthController {
    +login(LoginRequest) ApiResponse~AuthResponse~
    +refreshToken(HttpServletRequest) ApiResponse~TokenResponse~
    +logout(HttpServletRequest) void
  }
  class UserService {
    +createOrganization(OrgRegistrationInput) Organization
    +provisionUser(CreateUserInput) UserDto
    +attachCredential(UUID userId, CredentialInput) CredentialDto
    +revokeSession(UUID userId) void
  }
  class SubscriptionService {
    +activateSubscription(UUID orgId, SubscriptionInput) SubscriptionDto
    +checkEntitlement(UUID orgId) EntitlementStatus
  }
  class User {
    -UUID id
    -String email
    -String passwordHash
    -Role role
    -Organization organization
  }
  class Credential {
    -UUID id
    -String certificateNumber
    -LocalDate expiryDate
    -boolean verified
  }
  AuthController --> UserService
  UserService --> User
  UserService --> Credential
  SubscriptionService --> Organization
```

- **AuthController**: Exposes authentication endpoints for web and mobile clients; coordinates password verification and token generation.
- **UserService**: Manages tenant organization onboarding, workforce user creation, credential validation, and session revocation.
- **SubscriptionService**: Governs enterprise subscription plans, payment confirmation recording, and quota enforcement.

#### 3.1.2 User Authentication Sequence Diagram

```mermaid
%% title: User Authentication Sequence Diagram
sequenceDiagram
  autonumber
  actor User as System User
  participant Client as Web / Mobile Client
  participant AuthCtrl as AuthController
  participant UserSvc as UserService
  participant TokenSvc as TokenProvider
  participant DB as PostgreSQL Database

  User->>Client: Enter Email & Password
  Client->>AuthCtrl: POST /api/v1/auth/login
  AuthCtrl->>UserSvc: authenticate(email, rawPassword)
  UserSvc->>DB: findByEmail(email)
  DB-->>UserSvc: User Record (passwordHash, role, orgId)
  UserSvc->>UserSvc: verifyArgon2idHash(rawPassword, passwordHash)
  UserSvc->>TokenSvc: generateTokens(user)
  TokenSvc-->>UserSvc: AccessToken & RefreshToken
  UserSvc-->>AuthCtrl: AuthResponse (UserDTO, Tokens)
  AuthCtrl-->>Client: 200 OK (Set-Cookie: refreshToken, Body: accessToken)
  Client-->>User: Navigate to Role Dashboard
```

- Steps 1–3: The user submits login credentials through the client application over HTTPS.
- Steps 4–6: The authentication service verifies credentials against the database using Argon2id password hashing.
- Steps 7–9: The token provider issues a short-lived memory access token and an encrypted HttpOnly refresh token.
- Step 10: The client transitions to the authenticated operational dashboard.

#### 3.1.3 Workforce Provisioning Sequence Diagram

```mermaid
%% title: Workforce Provisioning Sequence Diagram
sequenceDiagram
  autonumber
  actor Admin as Organization Admin
  participant Client as Web Portal
  participant UserCtrl as UserController
  participant UserSvc as UserService
  participant DB as PostgreSQL Database

  Admin->>Client: Fill User Form & Attach Professional License
  Client->>UserCtrl: POST /api/v1/workforce/users
  UserCtrl->>UserSvc: provisionUser(input, credentialFile)
  UserSvc->>UserSvc: validateLicensePeriod(issueDate, expiryDate)
  UserSvc->>DB: saveUserWithRole(user, credential)
  DB-->>UserSvc: Saved Entities
  UserSvc-->>UserCtrl: UserProvisionedResponse
  UserCtrl-->>Client: 201 Created (UserDTO)
  Client-->>Admin: Display Success Notification
```

---

### 3.2 Infrastructure Asset, Equipment Fleet and Compliance Registry

#### 3.2.1 Class Diagram

```mermaid
%% title: Asset and Fleet Management Class Diagram
classDiagram
  class AssetController {
    +createAsset(CreateAssetRequest) ApiResponse~AssetDto~
    +getAsset(UUID id) ApiResponse~AssetDetailDto~
    +reassignDefaultPair(UUID id, PairRequest) ApiResponse~AssetDto~
  }
  class AssetService {
    +registerAsset(AssetInput) Asset
    +updateOperationalPair(UUID assetId, UUID inspectorId, UUID droneId) AssetPair
  }
  class DroneService {
    +registerDrone(DroneInput) Drone
    +updateServiceability(UUID droneId, ServiceabilityStatus) void
  }
  class Asset {
    -UUID id
    -String assetCode
    -String name
    -AssetCategory category
    -AssetPair defaultPair
  }
  class Drone {
    -UUID id
    -String serialNumber
    -String model
    -ServiceabilityStatus status
  }
  AssetController --> AssetService
  AssetService --> Asset
  AssetService --> DroneService
  DroneService --> Drone
```

- **AssetController**: REST endpoints for asset catalog management, technical specifications, and operational pair assignments.
- **AssetService**: Enforces asset code uniqueness within organizations, atomically binds default Inspector-Drone pairs, and maintains assignment history.
- **DroneService**: Tracks drone hardware inventory, maintenance hours, and serviceability transitions.

#### 3.2.2 Asset Registration and Default Pair Assignment Sequence Diagram

```mermaid
%% title: Asset Registration and Default Pair Assignment Sequence Diagram
sequenceDiagram
  autonumber
  actor Admin as Organization Admin
  participant Client as Web Portal
  participant AssetCtrl as AssetController
  participant AssetSvc as AssetService
  participant DroneSvc as DroneService
  participant DB as PostgreSQL Database

  Admin->>Client: Enter Asset Profile & Select Default Inspector + Drone
  Client->>AssetCtrl: POST /api/v1/assets
  AssetCtrl->>AssetSvc: createAssetWithPair(input)
  AssetSvc->>DroneSvc: verifyDroneServiceable(droneId)
  DroneSvc->>DB: findDroneById(droneId)
  DB-->>DroneSvc: Drone (status=SERVICEABLE)
  AssetSvc->>DB: saveAssetAndPair(asset, inspectorId, droneId)
  DB-->>AssetSvc: Persisted Asset Entity
  AssetSvc-->>AssetCtrl: AssetDto
  AssetCtrl-->>Client: 201 Created
  Client-->>Admin: Show Asset Detail Drawer
```

---

### 3.3 Flight Mission Planning and Readiness Authorization

#### 3.3.1 Class Diagram

```mermaid
%% title: Mission Planning and Readiness Class Diagram
classDiagram
  class InspectionController {
    +createInspection(CreateInspectionRequest) ApiResponse~InspectionDto~
    +submitPreparation(UUID id, PreparationRequest) ApiResponse~PreparationDto~
    +reviewReadiness(UUID id, ReadinessRequest) ApiResponse~ReadinessDecisionDto~
  }
  class InspectionService {
    +dispatchInspection(InspectionInput) Inspection
    +validateScheduleConflict(UUID droneId, UUID inspectorId, DateWindow) void
  }
  class ReadinessService {
    +evaluateReadiness(UUID preparationId, ReadinessDecisionInput) ReadinessDecision
  }
  class Inspection {
    -UUID id
    -InspectionStatus status
    -LocalDate plannedStartDate
    -LocalDate plannedEndDate
    -User inspector
    -Drone drone
  }
  InspectionController --> InspectionService
  InspectionController --> ReadinessService
  InspectionService --> Inspection
```

- **InspectionController**: Handles mission scheduling, preparation submissions, and administrative readiness decisions.
- **InspectionService**: Manages mission creation, validates scheduling conflicts across drone fleets, and tracks mission states.
- **ReadinessService**: Evaluates flight clearances against valid permits, pilot credentials, and weather constraints.

#### 3.3.2 Mission Dispatch and Readiness Authorization Sequence Diagram

```mermaid
%% title: Mission Dispatch and Readiness Authorization Sequence Diagram
sequenceDiagram
  autonumber
  actor Admin as Organization Admin
  actor Inspector as Assigned Inspector
  participant Client as Web / Mobile Client
  participant InspCtrl as InspectionController
  participant InspSvc as InspectionService
  participant ReadSvc as ReadinessService
  participant DB as PostgreSQL Database

  Admin->>Client: Dispatch Inspection Mission
  Client->>InspCtrl: POST /api/v1/inspections
  InspCtrl->>InspSvc: scheduleMission(input)
  InspSvc->>InspSvc: checkConflict(droneId, inspectorId, dates)
  InspSvc->>DB: saveInspection(status=ASSIGNED)
  DB-->>InspSvc: Saved Inspection
  InspSvc-->>Client: 201 Created

  Inspector->>Client: Submit Component Shot-List & Safety Notes
  Client->>InspCtrl: POST /api/v1/inspections/{id}/preparation
  InspCtrl->>InspSvc: recordPreparation(shotList, compliance)
  InspSvc->>DB: savePreparation(status=READY_FOR_REVIEW)
  DB-->>InspSvc: Preparation Record

  Admin->>Client: Evaluate Submitted Preparation
  Client->>InspCtrl: POST /api/v1/inspections/{id}/readiness
  InspCtrl->>ReadSvc: recordDecision(APPROVE)
  ReadSvc->>DB: updateInspection(status=APPROVED_FOR_FLIGHT)
  DB-->>ReadSvc: Updated Record
  ReadSvc-->>Client: 200 OK (Readiness Decision)
  Client-->>Inspector: Notify Mission Cleared for Flight
```

---

### 3.4 Field Survey Execution and Evidence Management

#### 3.4.1 Class Diagram

```mermaid
%% title: Field Survey and Evidence Management Class Diagram
classDiagram
  class FieldSessionController {
    +startSession(UUID inspectionId, SessionStartRequest) ApiResponse~FieldSessionDto~
    +endSession(UUID inspectionId, SessionEndRequest) ApiResponse~FieldSessionDto~
  }
  class EvidenceController {
    +uploadEvidence(UUID inspectionId, MultipartFile file) ApiResponse~EvidenceDto~
    +evaluateQuality(UUID inspectionId, QualityRequest) ApiResponse~QualityDecisionDto~
  }
  class EvidenceService {
    +storeEvidence(UUID inspectionId, byte[] content, Metadata) Evidence
    +computeSha256(byte[] data) String
  }
  class FieldSession {
    -UUID id
    -SessionStatus status
    -Instant startedAt
    -Instant endedAt
    -String preFlightNote
  }
  class Evidence {
    -UUID id
    -String objectKey
    -String sha256Checksum
    -Double latitude
    -Double longitude
  }
  FieldSessionController --> FieldSession
  EvidenceController --> EvidenceService
  EvidenceService --> Evidence
```

- **FieldSessionController**: On-site session tracking interface for remote pilots to record pre-flight notes and session outcomes.
- **EvidenceController**: Multi-file ingestion controller managing media streaming, checksum validation, and quality evaluations.
- **EvidenceService**: Calculates SHA-256 digests, streams binaries to MinIO object storage, and extracts embedded EXIF telemetry.

#### 3.4.2 Field Flight Session and Evidence Upload Sequence Diagram

```mermaid
%% title: Field Flight Session and Evidence Upload Sequence Diagram
sequenceDiagram
  autonumber
  actor Inspector as Remote Pilot / Inspector
  participant Mobile as Flutter Mobile App
  participant SessCtrl as FieldSessionController
  participant EviCtrl as EvidenceController
  participant EviSvc as EvidenceService
  participant MinIO as MinIO Object Storage
  participant DB as PostgreSQL Database

  Inspector->>Mobile: Fill Pre-Flight Checklist Note & Press Start
  Mobile->>SessCtrl: POST /api/v1/inspections/{id}/field-sessions
  SessCtrl->>DB: checkReadinessApproved(inspectionId)
  DB-->>SessCtrl: Approved
  SessCtrl->>DB: saveSession(status=IN_PROGRESS, preFlightNote)
  DB-->>SessCtrl: Active Session
  SessCtrl-->>Mobile: 201 Created (Session ID)

  Inspector->>Mobile: Select Inspection Photographs & Upload
  Mobile->>EviCtrl: POST /api/v1/inspections/{id}/evidence (Binary Stream)
  EviCtrl->>EviSvc: ingestFile(bytes, filename)
  EviSvc->>EviSvc: computeSha256(bytes)
  EviSvc->>DB: checkDuplicateHash(sha256)
  DB-->>EviSvc: Unique Hash
  EviSvc->>MinIO: putObject(bucket, key, bytes)
  MinIO-->>EviSvc: Stored (ETag)
  EviSvc->>DB: saveEvidence(objectKey, sha256, gpsCoordinates)
  DB-->>EviSvc: Evidence Record
  EviSvc-->>EviCtrl: EvidenceDto
  EviCtrl-->>Mobile: 200 OK
```

---

### 3.5 AI-Assisted Defect Detection and Inspector Verification

#### 3.5.1 Class Diagram

```mermaid
%% title: Defect Detection and Verification Class Diagram
classDiagram
  class DefectAnalysisController {
    +triggerDetection(UUID inspectionId) ApiResponse~List~FindingCandidateDto~~
    +verifyCandidate(UUID candidateId, VerificationRequest) ApiResponse~FindingDto~
    +confirmFindings(UUID inspectionId) ApiResponse~void~
  }
  class YoloClientAdapter {
    +detectDefects(byte[] imageBytes) List~DefectBoundingBox~
  }
  class FindingService {
    +processDetectionOutput(UUID evidenceId, List~DefectBoundingBox~) void
    +confirmFinding(UUID candidateId, FindingInput) Finding
    +confirmFindingSet(UUID inspectionId) void
  }
  class FindingCandidate {
    -UUID id
    -String defectClass
    -Double confidence
    -BoxCoordinates coordinates
  }
  class Finding {
    -UUID id
    -DefectType defectType
    -Severity severity
    -String location
  }
  DefectAnalysisController --> FindingService
  FindingService --> YoloClientAdapter
  FindingService --> FindingCandidate
  FindingService --> Finding
```

- **DefectAnalysisController**: REST endpoints for triggering computer vision analysis and recording inspector finding decisions.
- **YoloClientAdapter**: HTTP client invoking the external YOLO11s FastAPI microservice, returning parsed bounding boxes and classes.
- **FindingService**: Manages finding lifecycle transitions, converts verified candidates to official findings, and locks finding sets.

#### 3.5.2 YOLO11s Defect Detection and Verification Sequence Diagram

```mermaid
%% title: YOLO11s Defect Detection and Verification Sequence Diagram
sequenceDiagram
  autonumber
  actor Inspector as Assigned Inspector
  participant Client as Web Portal
  participant AnalysisCtrl as DefectAnalysisController
  participant FindingSvc as FindingService
  participant YoloAdapter as YoloClientAdapter
  participant YoloSvc as YOLO11s Microservice
  participant DB as PostgreSQL Database

  Inspector->>Client: Confirm Evidence Quality (ACCEPTED)
  Client->>AnalysisCtrl: POST /api/v1/inspections/{id}/detection
  AnalysisCtrl->>FindingSvc: analyzeInspectionEvidence(inspectionId)
  FindingSvc->>DB: getActiveEvidence(inspectionId)
  DB-->>FindingSvc: Evidence List
  
  loop For Each Image
    FindingSvc->>YoloAdapter: detectDefects(imageBytes)
    YoloAdapter->>YoloSvc: POST /predict (Image Payload)
    YoloSvc-->>YoloAdapter: Bounding Boxes & Defect Classes
    YoloAdapter-->>FindingSvc: Detections (Class, Confidence, Box)
    FindingSvc->>DB: saveFindingCandidates(detections)
  end

  FindingSvc-->>Client: Return Candidates List
  Inspector->>Client: Review Bounding Box, Adjust Severity & Click Confirm
  Client->>AnalysisCtrl: PUT /api/v1/findings/candidates/{id}/verify
  AnalysisCtrl->>FindingSvc: verifyFinding(candidateId, CONFIRMED)
  FindingSvc->>DB: promoteCandidateToOfficialFinding(candidateId)
  DB-->>FindingSvc: Official Finding Record
  FindingSvc-->>Client: 200 OK (Confirmed Finding)
```

---

### 3.6 Inspection Report Drafting, Review and Publication

#### 3.6.1 Class Diagram

```mermaid
%% title: Inspection Reporting and Publication Class Diagram
classDiagram
  class ReportController {
    +generateDraft(UUID inspectionId, DraftRequest) ApiResponse~ReportVersionDto~
    +submitReport(UUID versionId) ApiResponse~void~
    +reviewReport(UUID versionId, ReportDecisionRequest) ApiResponse~void~
    +downloadPdf(UUID versionId) ResponseEntity~Resource~
  }
  class ReportService {
    +synthesizeDraft(UUID inspectionId, Method method) ReportVersion
    +publishReport(UUID versionId) ReportVersion
    +handoffToMaintenance(UUID inspectionId, List~UUID~ findingIds) void
  }
  class PdfReportRenderer {
    +renderPdf(ReportRenderContext context) byte[]
  }
  class ReportVersion {
    -UUID id
    -Integer versionNumber
    -ReportStatus status
    -String renderedObjectKey
    -String sha256Checksum
  }
  ReportController --> ReportService
  ReportService --> PdfReportRenderer
  ReportService --> ReportVersion
```

- **ReportController**: Endpoints for draft synthesis, authoring edits, administrative approval, and compiled PDF downloads.
- **ReportService**: Manages grounded prompt synthesis, section persistence, approval gate enforcement, and maintenance defect handoffs.
- **PdfReportRenderer**: Generates publication-grade A4 PDF documents from clean HTML/CSS templates via OpenHTMLtoPDF.

#### 3.6.2 Report Synthesis, Review and Immutable Publication Sequence Diagram

```mermaid
%% title: Report Synthesis, Review and Immutable Publication Sequence Diagram
sequenceDiagram
  autonumber
  actor Inspector as Report Author
  actor Admin as Organization Admin
  participant Client as Web Portal
  participant RepCtrl as ReportController
  participant RepSvc as ReportService
  participant LLM as LLM Report Engine
  participant Renderer as PdfReportRenderer
  participant MinIO as MinIO Object Storage
  participant DB as PostgreSQL Database

  Inspector->>Client: Request AI Report Draft Synthesis
  Client->>RepCtrl: POST /api/v1/inspections/{id}/report/draft
  RepCtrl->>RepSvc: generateDraft(inspectionId)
  RepSvc->>DB: assembleGroundedContext(asset, findings, checklists)
  DB-->>RepSvc: Context Entities
  RepSvc->>LLM: synthesizeSections(context)
  LLM-->>RepSvc: Generated Section Narratives
  RepSvc->>DB: saveDraftVersion(sections)
  DB-->>RepSvc: Draft Version Record
  RepSvc-->>Client: 200 OK (Report Draft)

  Inspector->>Client: Edit Section Text & Click Submit
  Client->>RepCtrl: PUT /api/v1/reports/versions/{id}/submit
  RepCtrl->>RepSvc: submitVersion(versionId)
  RepSvc->>DB: updateStatus(SUBMITTED)
  DB-->>RepSvc: Updated Record

  Admin->>Client: Review Report Narrative & Click Approve
  Client->>RepCtrl: POST /api/v1/reports/versions/{id}/decision (APPROVE)
  RepCtrl->>RepSvc: publishReport(versionId)
  RepSvc->>Renderer: renderPdf(renderContext)
  Renderer-->>RepSvc: PDF Binary Bytes
  RepSvc->>RepSvc: computeSha256(pdfBytes)
  RepSvc->>MinIO: putObject(reportKey, pdfBytes)
  MinIO-->>RepSvc: Stored Deliverable
  RepSvc->>DB: markPublished(reportKey, sha256, status=PUBLISHED)
  DB-->>RepSvc: Published Entity
  RepSvc-->>Client: 200 OK (Published Deliverable)
```

---

### 3.7 Maintenance Remediation, Cost Control and Acceptance

#### 3.7.1 Class Diagram

```mermaid
%% title: Maintenance Management Class Diagram
classDiagram
  class MaintenanceController {
    +createWorkOrder(CreateWorkOrderRequest) ApiResponse~WorkOrderDto~
    +submitEstimate(UUID orderId, EstimateRequest) ApiResponse~EstimateVersionDto~
    +approveBudget(UUID orderId) ApiResponse~void~
    +logWork(UUID taskId, WorkLogRequest) ApiResponse~WorkLogDto~
    +acceptWorkOrder(UUID orderId, AcceptanceRequest) ApiResponse~void~
  }
  class WorkOrderService {
    +initializeWorkOrder(WorkOrderInput) MaintenanceWorkOrder
    +recordTaskLog(UUID taskId, WorkLogInput) WorkLog
    +closeWorkOrder(UUID orderId, AcceptanceInput) void
  }
  class CostCalculationEngine {
    +calculateBaseline(EstimateVersion) BigDecimal
    +reconcileVariance(BigDecimal budget, BigDecimal actuals) VarianceReport
  }
  class MaintenanceWorkOrder {
    -UUID id
    -WorkOrderStatus status
    -User teamLead
    -User reportAuthor
  }
  class MaintenanceTask {
    -UUID id
    -String title
    -User assignedTo
    -TaskStatus status
  }
  MaintenanceController --> WorkOrderService
  WorkOrderService --> CostCalculationEngine
  WorkOrderService --> MaintenanceWorkOrder
  WorkOrderService --> MaintenanceTask
```

- **MaintenanceController**: Manages work orders, task planning, daily execution logging, cost estimations, and closure approvals.
- **WorkOrderService**: Orchestrates work order state transitions, enforces separation of duties, and persists repair evidence.
- **CostCalculationEngine**: Computes deterministic decimal totals for baseline budgets, approved change orders, and actual expenses.

#### 3.7.2 Work Order Planning, Cost Estimation and Technical Acceptance Sequence Diagram

```mermaid
%% title: Work Order Planning, Cost Estimation and Technical Acceptance Sequence Diagram
sequenceDiagram
  autonumber
  actor Admin as Organization Admin
  actor Lead as Maintenance Team Lead
  actor Engineer as Maintenance Engineer
  participant Client as Web Portal
  participant MaintCtrl as MaintenanceController
  participant MaintSvc as WorkOrderService
  participant CostEngine as CostCalculationEngine
  participant DB as PostgreSQL Database

  Admin->>Client: Forward Confirmed Defects & Create Work Order
  Client->>MaintCtrl: POST /api/v1/maintenance/work-orders
  MaintCtrl->>MaintSvc: createOrder(findingIds, teamMembers, leadId, authorId)
  MaintSvc->>DB: saveWorkOrder(status=PLANNING)
  DB-->>MaintSvc: Created Work Order
  MaintSvc-->>Client: 201 Created

  Lead->>Client: Compile Itemized Cost Estimate (Labor, Materials, Rentals)
  Client->>MaintCtrl: POST /api/v1/maintenance/work-orders/{id}/estimate
  MaintCtrl->>MaintSvc: recordEstimate(items)
  MaintSvc->>CostEngine: calculateBaseline(items)
  CostEngine-->>MaintSvc: Baseline Total (Decimal)
  MaintSvc->>DB: saveEstimateBaseline(items, total)
  DB-->>MaintSvc: Estimate Record

  Admin->>Client: Review Estimate & Approve Budget Baseline
  Client->>MaintCtrl: POST /api/v1/maintenance/work-orders/{id}/budget/approve
  MaintSvc->>DB: updateWorkOrder(status=APPROVED)

  Engineer->>Client: Record Daily Work Log & Upload After-Repair Photos
  Client->>MaintCtrl: POST /api/v1/maintenance/tasks/{id}/work-logs
  MaintSvc->>DB: saveWorkLogAndEvidence(log, photos)

  Lead->>Client: Submit Maintenance Completion Report
  Client->>MaintCtrl: POST /api/v1/maintenance/work-orders/{id}/completion-report

  Admin->>Client: Conduct Technical Acceptance & Reconcile Costs
  Client->>MaintCtrl: POST /api/v1/maintenance/work-orders/{id}/accept
  MaintCtrl->>MaintSvc: closeOrder(acceptanceDecision)
  MaintSvc->>CostEngine: reconcileVariance(budget, actuals)
  CostEngine-->>MaintSvc: Variance Statement
  MaintSvc->>DB: closeWorkOrder(status=CLOSED)
  DB-->>MaintSvc: Closed Entity
  MaintSvc-->>Client: 200 OK (Work Order Closed)
```

---

### 3.8 Operational Dashboard and System Notifications

#### 3.8.1 Class Diagram

```mermaid
%% title: Dashboard and Notification Service Class Diagram
classDiagram
  class DashboardController {
    +getMetrics(HttpServletRequest) ApiResponse~DashboardMetricsDto~
    +getNotifications() ApiResponse~List~NotificationDto~~
  }
  class DashboardAnalyticsService {
    +compilePlatformMetrics() PlatformMetrics
    +compileEnterpriseMetrics(UUID orgId) EnterpriseMetrics
  }
  class NotificationService {
    +publishNotification(DomainEvent event) void
    +markRead(UUID notificationId) void
  }
  DashboardController --> DashboardAnalyticsService
  DashboardController --> NotificationService
```

- **DashboardController**: Provides scoped metrics and active notification queues tailored to the authenticated user's role.
- **DashboardAnalyticsService**: Executes optimized aggregation queries across assets, mission statuses, defect severities, and budgets.
- **NotificationService**: Listens to published application domain events and delivers in-app alert badges and outbound email notifications.

#### 3.8.2 Event-Driven Notification Dispatch Sequence Diagram

```mermaid
%% title: Event-Driven Notification Dispatch Sequence Diagram
sequenceDiagram
  autonumber
  participant Domain as Application Domain Service
  participant EventBus as Spring Event Publisher
  participant NotifSvc as NotificationService
  participant EmailGateway as JavaMailSender
  participant DB as PostgreSQL Database
  actor User as Target Stakeholder

  Domain->>EventBus: publishEvent(MissionReadinessApprovedEvent)
  EventBus->>NotifSvc: handleEvent(event)
  NotifSvc->>DB: resolveRecipients(inspectorId, orgAdminId)
  DB-->>NotifSvc: User Contacts
  NotifSvc->>DB: saveNotificationRecord(title, message, deepLink)
  DB-->>NotifSvc: Persisted Alert
  NotifSvc->>EmailGateway: sendMimeMessage(recipientEmail, body)
  EmailGateway-->>User: Deliver Operational Email Notification
  NotifSvc-->>User: Real-Time WebSocket In-App Badge Increment
```
