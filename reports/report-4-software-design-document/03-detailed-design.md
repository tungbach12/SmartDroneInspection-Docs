---
title: "Report 4 - Detailed Design"
document_type: report4-sdd-section
weight: 35
source: "report4-software-design-document.docx"
---

## 3. Detailed Design

### 3.1 FE-01 Authentication & Access Control

#### 3.1.1 Class Diagram

```mermaid
%% title: Identity, Workforce and Subscription Class Diagram
classDiagram
  class BrowserAuthController {
    +csrf(CsrfToken) Map
    +register(OrganizationRegistrationRequest) ResponseEntity~ApiResponse~
    +login(LoginRequest, HttpServletRequest, HttpServletResponse) ResponseEntity~ApiResponse~
    +setupInitialPassword(InitialPasswordSetupRequest) ResponseEntity~ApiResponse~
    +refresh(HttpServletRequest, HttpServletResponse) ResponseEntity~ApiResponse~
    +updatePilotLicense(Jwt, UpdatePilotLicenseRequest) ResponseEntity~ApiResponse~
  }
  class PlatformUserController {
    +listUsers(int, int, String) ApiResponse~PagedResponse~
    +createUser(Jwt, CreatePlatformUserRequest) ResponseEntity~ApiResponse~
    +updateRoles(Jwt, UUID, UpdatePlatformUserRolesRequest) ApiResponse
    +updateStatus(Jwt, UUID, UpdateUserStatusRequest) ApiResponse
  }
  class WorkforceController {
    +createWorkforceUser(Jwt, CreateWorkforceUserRequest) ResponseEntity~ApiResponse~
    +listWorkforceUsers(Jwt, int, int, String) ApiResponse~PagedResponse~
    +updateRoles(Jwt, UUID, UpdateWorkforceRolesRequest) ApiResponse
  }
  class SubscriptionController {
    +getCurrent(Jwt) ApiResponse~CurrentSubscriptionView~
    +requestSubscription(Jwt, CreateSubscriptionRequest) ResponseEntity~ApiResponse~
    +createPayPalOrder(Jwt, CreatePayPalOrderRequest) ApiResponse~PayPalOrderCreatedView~
    +capturePayPalOrder(Jwt, CapturePayPalOrderRequest) ApiResponse~SubscriptionView~
  }
  class PlatformSubscriptionController {
    +listSubscriptions(String, int, int) ApiResponse~PagedResponse~
    +confirmPayment(Jwt, UUID, ConfirmSubscriptionPaymentRequest) ApiResponse~SubscriptionView~
  }
  class PayPalWebhookController {
    +handleWebhook(String, Map) ResponseEntity~Void~
  }
  class User {
    -UUID id
    -UUID organizationId
    -String normalizedEmail
    -UserStatus status
    -ActorZone actorZone
    -String roles
    -String pilotLicenseNumber
    -Instant pilotLicenseExpiresAt
  }
  class Subscription {
    -UUID id
    -UUID organizationId
    -Integer billingPeriodMonths
    -BigDecimal agreedAmountUsd
    -Status status
    -Instant startsAt
    -Instant endsAt
  }
  BrowserAuthController --> User
  PlatformUserController --> User
  WorkforceController --> User
  SubscriptionController --> Subscription
  PlatformSubscriptionController --> Subscription
  PayPalWebhookController --> Subscription
```

**Class Specifications**

- **BrowserAuthController & MobileAuthController**: Expose web (`/api/v1/auth`) and native mobile (`/api/v1/mobile/auth`) authentication endpoints, enforcing `AuthRateLimitFilter` (`10` req/60s per IP), Argon2id password verification, `HS256` JWT issuance (`15m` TTL), and `HmacSHA256` refresh session rotation (`auth_sessions`, `7d` TTL).
- **PlatformUserController**: Governs platform-zone accounts (`ADMIN` XOR `PLATFORM_MANAGER`) and customer `ORG_MANAGER` accounts with one-time temporary passwords and session revocation.

#### 3.1.2 User Authentication Sequence Diagram

```mermaid
%% title: User Authentication Sequence Diagram
sequenceDiagram
  autonumber
  actor User as System User
  participant Client as Web / Mobile Client
  participant AuthCtrl as BrowserAuthController
  participant AuthSvc as AuthService
  participant JwtSvc as AccessTokenService
  participant DB as PostgreSQL (users & auth_sessions)

  User->>Client: Submit Email & Password
  Client->>AuthCtrl: POST /api/v1/auth/login (with X-XSRF-TOKEN)
  AuthCtrl->>AuthSvc: login(email, rawPassword, ip, userAgent)
  AuthSvc->>DB: findByNormalizedEmail(email)
  DB-->>AuthSvc: User (passwordHash, status, roles, failedLoginCount, lockoutUntil)
  AuthSvc->>AuthSvc: verifyLockoutAndArgon2id(rawPassword, passwordHash)
  AuthSvc->>JwtSvc: issueAccessToken(user, 15m TTL)
  JwtSvc-->>AuthSvc: HS256 JWT AccessToken
  AuthSvc->>DB: insertAuthSession(tokenHash=HmacSHA256(refreshToken), 7d TTL)
  AuthSvc-->>AuthCtrl: LoginResult(accessToken, refreshTokenCookie, userView)
  AuthCtrl-->>Client: 200 OK (sdi_refresh HttpOnly cookie + accessToken JSON)
```

---

### 3.2 FE-02 Workforce & Subscription Management

#### 3.2.1 Class Diagram

Refer to the shared Identity, Workforce and Subscription Class Diagram in **Section 3.1.1** (`WorkforceController`, `SubscriptionController`, `PlatformSubscriptionController`, `PayPalWebhookController`, `User`, and `Subscription`).

#### 3.2.2 Workforce Provisioning & Pilot License Sequence Diagram

```mermaid
%% title: Workforce Provisioning and Pilot License Sequence Diagram
sequenceDiagram
  autonumber
  actor OM as Organization Manager
  actor Insp as Inspector
  participant Client as Web / Mobile Portal
  participant WfCtrl as WorkforceController
  participant AuthCtrl as BrowserAuthController
  participant DB as PostgreSQL (users & audit_events)

  OM->>Client: Provision Workforce Account (INSPECTOR)
  Client->>WfCtrl: POST /api/v1/workforce/users
  WfCtrl->>DB: insertUser(orgId, roles='INSPECTOR', mustChangePassword=true)
  DB-->>WfCtrl: Created User + One-Time Password
  WfCtrl-->>Client: 201 Created (WorkforceUserCreatedResponse)

  Insp->>Client: Complete Password Setup & Enter Pilot License Details
  Client->>AuthCtrl: PUT /api/v1/auth/me/pilot-license (number, class, expiresAt, fileKey)
  AuthCtrl->>DB: updateUserPilotLicense(userId, licenseFields)
  DB-->>AuthCtrl: Updated User Profile
  AuthCtrl-->>Client: 200 OK (CurrentUserResponse)
```

#### 3.2.3 PayPal Subscription Payment & Webhook Capture Sequence Diagram

```mermaid
%% title: PayPal Subscription Payment and Webhook Capture Sequence Diagram
sequenceDiagram
  autonumber
  actor OM as Organization Manager
  participant Client as Web Portal
  participant SubCtrl as SubscriptionController
  participant SubSvc as SubscriptionService
  participant PayPal as PayPal Orders v2 API
  participant DB as PostgreSQL (subscriptions & payment_transactions)

  OM->>Client: Request ENTERPRISE Plan (6 Months) & Click Pay with PayPal
  Client->>SubCtrl: POST /api/v1/subscriptions/paypal/create-order
  SubCtrl->>SubSvc: createPayPalOrder(orgId, subscriptionId)
  SubSvc->>PayPal: POST /v2/checkout/orders (agreedAmountUsd, USD)
  PayPal-->>SubSvc: OrderCreated (paypalOrderId, approveUrl)
  SubSvc->>DB: savePaymentTransaction(status=PENDING, paypalOrderId)
  SubSvc-->>Client: 200 OK (paypalOrderId, approveUrl)

  OM->>PayPal: Approve Payment on PayPal Hosted Checkout
  PayPal-->>Client: Redirect onApprove(paypalOrderId)
  Client->>SubCtrl: POST /api/v1/subscriptions/paypal/capture-order
  SubCtrl->>SubSvc: capturePayPalOrder(orgId, subscriptionId, paypalOrderId)
  SubSvc->>PayPal: POST /v2/checkout/orders/{orderId}/capture
  PayPal-->>SubSvc: CaptureResponse (status=COMPLETED, captureId, amount)
  SubSvc->>DB: markTransactionCompleted & activateSubscription(status=ACTIVE)
  SubSvc-->>Client: 200 OK (SubscriptionView status=ACTIVE)
```

---

### 3.3 FE-03 Asset & Drone Fleet Management

#### 3.3.1 Class Diagram

```mermaid
%% title: Asset, Drone Fleet and Drone Equipment Leasing Class Diagram
classDiagram
  class AssetController {
    +createAsset(Jwt, CreateAssetRequest) ResponseEntity~ApiResponse~
    +listAssets(Jwt, int, int, String) ApiResponse~PagedResponse~
    +updateAsset(Jwt, UUID, UpdateAssetRequest) ApiResponse~AssetView~
    +retireAsset(Jwt, UUID) ApiResponse~AssetView~
  }
  class AssetDocumentController {
    +uploadDocument(Jwt, UUID, MultipartFile, String, LocalDate) ResponseEntity~ApiResponse~
    +downloadDocument(Jwt, UUID, UUID) ResponseEntity~byte[]~
  }
  class DroneController {
    +createDrone(Jwt, CreateDroneRequest) ResponseEntity~ApiResponse~
    +changeServiceability(Jwt, UUID, ChangeServiceabilityRequest) ApiResponse~DroneView~
    +updateRegistration(Jwt, UUID, UpdateDroneRegistrationRequest) ApiResponse~DroneView~
  }
  class DroneLeaseController {
    +listAvailablePoolDrones() ApiResponse~List~
    +requestLease(Jwt, CreateDroneLeaseRequest) ResponseEntity~ApiResponse~
    +createPayPalOrder(Jwt, UUID) ApiResponse~PayPalOrderCreatedView~
    +capturePayPalOrder(Jwt, UUID, CaptureDroneLeasePayPalRequest) ApiResponse~DroneLeaseView~
  }
  class PlatformDroneLeaseController {
    +addPoolDrone(Jwt, CreatePlatformDroneRequest) ResponseEntity~ApiResponse~
    +confirmWirePayment(Jwt, UUID, ConfirmDroneLeasePaymentRequest) ApiResponse~DroneLeaseView~
    +reclaimLease(Jwt, UUID) ApiResponse~DroneLeaseView~
  }
  class Asset {
    -UUID id
    -UUID organizationId
    -String assetCode
    -String inspectionItems
    -AssetStatus status
  }
  class PlatformDrone {
    -UUID id
    -String serialNumber
    -BigDecimal monthlyRateUsd
    -PlatformDroneStatus status
  }
  class DroneLease {
    -UUID id
    -UUID platformDroneId
    -UUID organizationId
    -UUID customerDroneId
    -DroneLeaseStatus status
  }
  class Drone {
    -UUID id
    -UUID organizationId
    -String serialNumber
    -DroneOwnershipType ownershipType
    -DroneServiceability serviceability
  }
  AssetController --> Asset
  AssetDocumentController --> Asset
  DroneController --> Drone
  DroneLeaseController --> DroneLease
  PlatformDroneLeaseController --> PlatformDrone
  PlatformDroneLeaseController --> DroneLease
  DroneLease --> Drone
```

**Class Specifications**

- **AssetController & AssetDocumentController**: Manage infrastructure assets (`assets`) with GPS coordinates and standardized `inspection_items` checkpoints, SHA-256 deduplicated documents in MinIO (`asset_documents`), and terminal asset retirement (`RETIRED`).
- **DroneController, DroneLeaseController & PlatformDroneLeaseController**: Govern customer owned/leased drones (`drones`), platform leasable drone pool (`platform_drones`), and drone equipment lease contracts (`drone_leases`) with automatic customer fleet provisioning and reclaim.

#### 3.3.2 Drone Equipment Leasing & Automatic Fleet Provisioning Sequence Diagram

```mermaid
%% title: Drone Equipment Leasing and Fleet Provisioning Sequence Diagram
sequenceDiagram
  autonumber
  actor OM as Organization Manager
  actor PM as Platform Manager
  participant Client as Web Portal
  participant LeaseCtrl as DroneLeaseController
  participant PlatCtrl as PlatformDroneLeaseController
  participant LeaseSvc as DroneLeaseService
  participant DB as PostgreSQL (platform_drones, drone_leases, drones)

  OM->>Client: Select AVAILABLE PlatformDrone & Request Lease (12 Months)
  Client->>LeaseCtrl: POST /api/v1/drone-leases (platformDroneId, leasePeriodMonths=12)
  LeaseCtrl->>LeaseSvc: requestLease(orgId, userId, request)
  LeaseSvc->>DB: verifyPlatformDroneAvailable & insertDroneLease(status=PENDING)
  DB-->>LeaseSvc: Saved DroneLease (PENDING)
  LeaseSvc-->>Client: 201 Created (DroneLeaseView)

  PM->>Client: Verify Wire Settlement & Confirm Lease Payment
  Client->>PlatCtrl: POST /api/v1/platform/drone-leases/{leaseId}/confirm-payment
  PlatCtrl->>LeaseSvc: confirmWirePayment(pmUserId, leaseId, externalReference)
  LeaseSvc->>DB: markPlatformDroneLeased(status=LEASED)
  LeaseSvc->>DB: upsertCustomerDrone(ownershipType=LEASED, serviceability=ACTIVE, leaseExpiresAt)
  LeaseSvc->>DB: activateDroneLease(status=ACTIVE, customerDroneId)
  DB-->>LeaseSvc: Activated Lease & Provisioned Customer Drone
  LeaseSvc-->>Client: 200 OK (DroneLeaseView status=ACTIVE)
```

---

### 3.4 FE-04 Recurring Schedule & Notifications

#### 3.4.1 Class Diagram

```mermaid
%% title: Notification Inbox and Event Listeners Class Diagram
classDiagram
  class NotificationController {
    +listNotifications(Jwt, int, int, boolean) ApiResponse~PagedResponse~
    +getUnreadCount(Jwt) ApiResponse~UnreadCountResponse~
    +markRead(Jwt, UUID) ApiResponse~NotificationItemResponse~
  }
  class NotificationService {
    +createInAppNotification(UUID orgId, UUID recipientId, String eventType, String title, String body, String targetPath, String deduplicationKey) void
    +markAsRead(UUID orgId, UUID recipientId, UUID notificationId) Notification
  }
  class InspectionNotificationListener {
    +onInspectionAssigned(InspectionAssignedEvent) void
    +onInspectionReminderDue(InspectionReminderDueEvent) void
  }
  class MaintenanceNotificationListener {
    +onWorkOrderAssigned(WorkOrderAssignedEvent) void
    +onEstimateApproved(EstimateApprovedEvent) void
    +onAcceptanceRecorded(AcceptanceRecordedEvent) void
    +onWorkOrderClosed(WorkOrderClosedEvent) void
  }
  class Notification {
    -UUID id
    -UUID organizationId
    -UUID recipientUserId
    -NotificationStatus status
    -String deduplicationKey
    -String targetPath
  }
  NotificationController --> NotificationService
  InspectionNotificationListener --> NotificationService
  MaintenanceNotificationListener --> NotificationService
  NotificationService --> Notification
```

**Class Specifications**

- **InspectionScheduleController & RecurringInspectionScheduleService**: Manage timezone-anchored recurring schedules (`recurring_inspection_schedules`, `schedule_occurrences`), rolling 14-day generation (`RecurringInspectionSchedulerJob`), 3-day advance reminders (`InspectionReminderJob`), and `BLOCKED` occurrence retry/skip.
- **NotificationController & InspectionNotificationListener / MaintenanceNotificationListener**: Persist deduplicated in-app notifications (`uq_notifications_deduplication_key`) via Spring Modulith's `event_publication` outbox and serve recipient-scoped inbox queries.

#### 3.4.2 Event-Driven Transactional Outbox Notification Sequence Diagram

```mermaid
%% title: Event-Driven Transactional Outbox Notification Sequence Diagram
sequenceDiagram
  autonumber
  participant InspSvc as Inspection / Maintenance Service
  participant Outbox as Spring Modulith Outbox (event_publication)
  participant Listener as InspectionNotificationListener
  participant NotifSvc as NotificationService
  participant DB as PostgreSQL (notifications)
  actor User as Recipient User (Web / Mobile)

  InspSvc->>Outbox: publishEvent(InspectionAssignedEvent / WorkOrderAssignedEvent)
  Outbox->>Listener: @ApplicationModuleListener invoke on commit
  Listener->>NotifSvc: createInAppNotification(orgId, recipientId, deduplicationKey, targetPath)
  NotifSvc->>DB: insertIgnoreOnConflict(deduplication_key, status=SENT)
  DB-->>NotifSvc: Persisted Notification

  User->>DB: GET /api/v1/notifications & GET /api/v1/notifications/unread-count
  DB-->>User: Scoped Notifications + Unread Count
  User->>DB: PATCH /api/v1/notifications/{id}/read
  DB-->>User: 200 OK (status=READ, readAt=now)
```

#### 3.4.3 WF-01 Activity Diagram — Enterprise Onboarding, Leasing & Recurring Scheduling

```mermaid
%% title: WF-01 Activity Diagram - Enterprise Onboarding, Drone Equipment Leasing and Recurring Scheduling
flowchart TD
  subgraph OM1["Organization Manager (ORG_MANAGER)"]
    A1(["Start: Register Organization & ORG_MANAGER"])
    A2["Request Enterprise Subscription (1/6/12m) -> Subscription: PENDING"]
    A4["Request Drone Equipment Lease from Pool -> DroneLease: PENDING"]
    A6["Register Infrastructure Asset (Checkpoints) & Upload AssetDocument (SHA-256)"]
    A7["Create RecurringInspectionSchedule (WEEK/MONTH/YEAR) -> Schedule: ACTIVE"]
  end

  subgraph PM1["Platform Manager (PLATFORM_MANAGER) / PayPal"]
    A3["Confirm Subscription Wire / PayPal Capture -> Subscription: ACTIVE"]
    A5["Confirm Lease Payment -> DroneLease: ACTIVE, PlatformDrone: LEASED,\nCustomer Drone Provisioned (LEASED, ACTIVE)"]
  end

  subgraph SYS1["Automated System (RecurringInspectionSchedulerJob & Outbox)"]
    A8{"Pre-Checks & Conflict\nValidation Pass?"}
    A9["Create ScheduleOccurrence: GENERATED &\nDispatched Inspection: ASSIGNED"]
    A10["Create ScheduleOccurrence: BLOCKED\n(record blockedReason for retry/skip)"]
    A11(["End: Emit InspectionAssignedEvent -> In-App Notification SENT"])
  end

  A1 --> A2 --> A3 --> A4 --> A5 --> A6 --> A7 --> A8
  A8 -->|"Yes"| A9 --> A11
  A8 -->|"No (Conflict / Expired License)"| A10
```

---

### 3.5 FE-05 Mission Dispatch & Airspace Advisory

#### 3.5.1 Class Diagram

```mermaid
%% title: Inspection Mission, Recurring Schedule and Permit Gate Class Diagram
classDiagram
  class InspectionListController {
    +createInspection(Jwt, CreateInspectionRequest) ResponseEntity~ApiResponse~
    +getInspection(Jwt, UUID) ApiResponse~InspectionSummaryResponse~
    +listInspections(Jwt, int, int) ApiResponse~PagedResponse~
  }
  class InspectionScheduleController {
    +createSchedule(Jwt, CreateRecurringScheduleRequest) ResponseEntity~ApiResponse~
    +pauseSchedule(Jwt, UUID) ApiResponse~RecurringScheduleResponse~
    +resumeSchedule(Jwt, UUID) ApiResponse~RecurringScheduleResponse~
    +endSchedule(Jwt, UUID) ApiResponse~RecurringScheduleResponse~
    +retryOccurrence(Jwt, UUID, UUID) ApiResponse~ScheduleOccurrenceResponse~
    +skipOccurrence(Jwt, UUID, UUID, SkipOccurrenceRequest) ApiResponse~ScheduleOccurrenceResponse~
  }
  class InspectionController {
    +uploadFlightPermit(Jwt, UUID, MultipartFile) ApiResponse~FlightPermitResponse~
  }
  class RecurringInspectionScheduleService {
    +createSchedule(UUID, UUID, CreateRecurringScheduleRequest) RecurringScheduleResponse
    +generateDueOccurrences(Instant) int
    +retryOccurrence(UUID, UUID, UUID) ScheduleOccurrenceResponse
  }
  class Inspection {
    -UUID id
    -UUID organizationId
    -UUID assetId
    -UUID inspectorId
    -UUID droneId
    -InspectionStatus status
    -String flightPermitFileKey
  }
  class RecurringInspectionSchedule {
    -UUID id
    -RecurrenceUnit recurrenceUnit
    -int recurrenceInterval
    -Instant nextOccurrence
    -RecurringScheduleStatus status
  }
  InspectionListController --> Inspection
  InspectionController --> Inspection
  InspectionScheduleController --> RecurringInspectionScheduleService
  RecurringInspectionScheduleService --> RecurringInspectionSchedule
  RecurringInspectionScheduleService --> Inspection
```

**Class Specifications**

- **InspectionListController & InspectionCreationService**: Handle one-off inspection mission scheduling (`POST /api/v1/inspections`), validating active subscription, active asset, active Inspector, serviceable Drone, and concurrent time-window conflicts.
- **AirspaceController & AirspaceAdvisoryService**: Expose `/api/v1/airspace/zones` and `/api/v1/airspace/evaluate`, computing Haversine distance against published Vietnam `NO_FLY_ZONE` and `RESTRICTED_ZONE` areas (Decree No. 288/2025/NĐ-CP) and returning `MSG28` advisories.

#### 3.5.2 Mission Dispatch and Self-Service Permit Upload Sequence Diagram

```mermaid
%% title: Mission Dispatch and Self-Service Permit Upload Sequence Diagram
sequenceDiagram
  autonumber
  actor OM as Organization Manager
  actor Inspector as Assigned Inspector
  participant Client as Web / Mobile Client
  participant ListCtrl as InspectionListController
  participant InspCtrl as InspectionController
  participant MinIO as MinIO Object Storage
  participant DB as PostgreSQL (inspections, users)

  OM->>Client: Dispatch Mission (Select Asset, Active Inspector, Serviceable Drone)
  Client->>ListCtrl: POST /api/v1/inspections
  ListCtrl->>DB: verifyNoScheduleOverlap & insertInspection(status=ASSIGNED)
  DB-->>ListCtrl: Saved Inspection (ASSIGNED)
  ListCtrl-->>Client: 201 Created (InspectionSummaryResponse)

  Inspector->>Client: Upload Mission Flight Permit Document (PDF/Image)
  Client->>InspCtrl: POST /api/v1/inspections/{id}/flight-permit (MultipartFile)
  InspCtrl->>DB: checkCallerIsAssignedInspector & pilotLicenseExpiresAt >= plannedStartAt
  InspCtrl->>MinIO: putObject(inspection-evidence, permitObjectKey, bytes)
  MinIO-->>InspCtrl: Stored Object Key
  InspCtrl->>DB: recordFlightPermit(permitKey, fileName) -> status=READY_FOR_FLIGHT
  DB-->>InspCtrl: Updated Inspection (READY_FOR_FLIGHT)
  InspCtrl-->>Client: 200 OK (FlightPermitResponse status=READY_FOR_FLIGHT)
```

---

### 3.6 FE-06 Flight Readiness & Field Execution

#### 3.6.1 Class Diagram

```mermaid
%% title: Field Session and Evidence Management Class Diagram
classDiagram
  class InspectionFieldSessionController {
    +listSessions(Jwt, UUID) ApiResponse~List~
    +startSession(Jwt, UUID, StartFieldSessionRequest) ResponseEntity~ApiResponse~
    +postponeSession(Jwt, UUID, UUID, SessionReasonRequest) ApiResponse~FieldSessionView~
    +completeSession(Jwt, UUID, UUID, CompleteFieldSessionRequest) ApiResponse~FieldSessionView~
    +abortSession(Jwt, UUID, UUID, SessionReasonRequest) ApiResponse~FieldSessionView~
  }
  class InspectionController {
    +uploadEvidence(Jwt, UUID, MultipartFile, UUID, Instant, BigDecimal, BigDecimal, String) ResponseEntity~ApiResponse~
    +queryEvidence(Jwt, UUID, String, String, String, int, int) ApiResponse~PagedResponse~
    +retireEvidence(Jwt, UUID, UUID) ApiResponse~EvidenceItemResponse~
    +streamEvidenceContent(Jwt, UUID, UUID) ResponseEntity~byte[]~
  }
  class ExifMetadataExtractor {
    +extract(byte[] imageBytes) ExifMetadata
  }
  class FieldSession {
    -UUID id
    -UUID inspectionId
    -String status
    -String preFlightChecklistNote
    -String outcomeNotes
  }
  class Evidence {
    -UUID id
    -UUID inspectionId
    -UUID fieldSessionId
    -String fileName
    -String objectKey
    -BigDecimal latitude
    -BigDecimal longitude
    -boolean isDeleted
  }
  InspectionFieldSessionController --> FieldSession
  InspectionController --> Evidence
  InspectionController --> ExifMetadataExtractor
```

**Class Specifications**

- **InspectionController (Flight Permit Gate)**: Validates assigned Inspector identity and unexpired remote pilot license (`pilot_license_expires_at >= planned_start_at`), stores the flight permit in MinIO, and transitions `Inspection` `ASSIGNED -> READY_FOR_FLIGHT`.
- **InspectionFieldSessionController**: Manages on-site `FieldSession` execution (`start`, `postpone`, `complete`, `abort`, and additional sessions from `FIELD_COMPLETED`) guided by `assets.inspection_items`.

#### 3.6.2 Field Flight Session and Evidence Upload Sequence Diagram

```mermaid
%% title: Field Flight Session and Evidence Upload Sequence Diagram
sequenceDiagram
  autonumber
  actor Inspector as Assigned Inspector
  participant Mobile as Flutter Mobile / Web Client
  participant SessCtrl as InspectionFieldSessionController
  participant InspCtrl as InspectionController
  participant Exif as ExifMetadataExtractor
  participant MinIO as MinIO Object Storage
  participant DB as PostgreSQL (inspections, field_sessions, evidence)

  Inspector->>Mobile: Enter Pre-Flight Checklist Note & Start Session
  Mobile->>SessCtrl: POST /api/v1/inspections/{id}/field-sessions
  SessCtrl->>DB: verifyInspectionReadyForFlight & insertFieldSession(status=IN_PROGRESS)
  SessCtrl->>DB: updateInspectionStatus(IN_PROGRESS)
  SessCtrl-->>Mobile: 201 Created (FieldSessionView status=IN_PROGRESS)

  Inspector->>Mobile: Complete Survey Against Asset Checkpoints
  Mobile->>SessCtrl: POST /api/v1/inspections/{id}/field-sessions/{sessionId}/completion
  SessCtrl->>DB: completeSession(outcomeNotes) & updateInspectionStatus(FIELD_COMPLETED)
  SessCtrl-->>Mobile: 200 OK (FieldSessionView status=FIELD_COMPLETED)

  Inspector->>Mobile: Upload Aerial Evidence Image (JPEG/PNG)
  Mobile->>InspCtrl: POST /api/v1/inspections/{id}/evidence (MultipartFile)
  InspCtrl->>DB: verifyUniqueSanitizedFilenameInInspection(inspectionId, fileName)
  InspCtrl->>Exif: extract(imageBytes) -> captureTime, latitude, longitude
  InspCtrl->>MinIO: putObject(inspection-evidence, objectKey, imageBytes)
  InspCtrl->>DB: insertEvidence(objectKey, captureTime, latitude, longitude)
  InspCtrl-->>Mobile: 201 Created (EvidenceUploadResponse)
```

#### 3.6.3 WF-02 Activity Diagram — Mission Dispatch, Flight Permit Gate & Field Execution

```mermaid
%% title: WF-02 Activity Diagram - Mission Dispatch, Flight Permit Gate and Field Execution
flowchart TD
  subgraph OM2["Organization Manager (ORG_MANAGER)"]
    B1(["Start: Dispatch Inspection Mission (Asset, Inspector, Drone)"])
  end

  subgraph IN2["Assigned Inspector (INSPECTOR - Web / Flutter Mobile)"]
    B3["Declare / Verify Unexpired Remote Pilot License"]
    B4["Upload Aviation Flight Permit Document (PDF/Image)"]
    B6["Start On-Site FieldSession with Pre-Flight Checklist Note"]
    B7{"Field Weather &\nCoverage Outcome?"}
    B8["Complete FieldSession with Outcome Notes"]
    B9["Postpone FieldSession with Reason"]
    B10["Upload Aerial Evidence Media (JPEG/PNG)"]
  end

  subgraph SYS2["Automated System (InspectionService & ExifMetadataExtractor)"]
    B2["Validate Resource Overlap -> Inspection: ASSIGNED"]
    B5["Store Permit in MinIO & Validate License -> Inspection: READY_FOR_FLIGHT"]
    B11["Inspection: IN_PROGRESS & FieldSession: IN_PROGRESS"]
    B12["Inspection: FIELD_COMPLETED & FieldSession: FIELD_COMPLETED"]
    B13["Extract EXIF GPS/Timestamp, Reject Duplicate Filename & Store in MinIO"]
    B14(["End: Evidence Register Ready for Defect Analysis"])
  end

  B1 --> B2 --> B3 --> B4 --> B5 --> B6 --> B11 --> B7
  B7 -->|"Survey Completed"| B8 --> B12 --> B10 --> B13 --> B14
  B7 -->|"Weather Postponed"| B9 --> B5
```

---

### 3.7 FE-07 Operational Dashboard & Schedule Calendar

#### 3.7.1 Class Diagram

Refer to the Notification, Dashboard and Schedule Class Diagrams in **Sections 3.4.1 and 3.5.1** (`DashboardAnalyticsService`, `InspectionListController`, `InspectionScheduleController`, and `NotificationController`).

#### 3.7.2 Role-Scoped Dashboard & Schedule Calendar Sequence Diagram

Refer to the scoped inspection/schedule query and outbox notification sequence in **Section 3.4.2**.

---

### 3.8 FE-08 Evidence Management & AI Defect Detection

#### 3.8.1 Class Diagram

```mermaid
%% title: YOLO11 Defect Detection and Finding Verification Class Diagram
classDiagram
  class InspectionController {
    +analyzeEvidence(Jwt, UUID, UUID, boolean) ApiResponse~EvidenceAnalysisResponse~
    +createFinding(Jwt, UUID, CreateFindingRequest) ResponseEntity~ApiResponse~
    +updateFinding(Jwt, UUID, UUID, UpdateFindingRequest) ApiResponse~FindingResponse~
    +confirmFinding(Jwt, UUID, UUID) ApiResponse~FindingResponse~
    +deleteFinding(Jwt, UUID, UUID) ResponseEntity~Void~
    +confirmFindingsBaseline(Jwt, UUID, ConfirmFindingsRequest) ApiResponse~WorkflowStateResponse~
  }
  class PrimaryWithFallbackInference {
    +analyze(byte[] imageBytes, String contentType, boolean allowFallback) InferenceResult
  }
  class YoloInferenceClient {
    +predict(byte[] imageBytes, String contentType) List~DetectedBox~
  }
  class OpenAiCompatibleInferenceClient {
    +predict(byte[] imageBytes, String contentType) List~DetectedBox~
  }
  class Finding {
    -UUID id
    -UUID inspectionId
    -UUID evidenceId
    -String findingCode
    -String defectLabel
    -FindingSeverity severity
    -String boundingBox
    -FindingStatus status
    -String modelName
    -BigDecimal confidence
    -boolean isDeleted
  }
  InspectionController --> PrimaryWithFallbackInference
  PrimaryWithFallbackInference --> YoloInferenceClient
  PrimaryWithFallbackInference --> OpenAiCompatibleInferenceClient
  InspectionController --> Finding
```

**Class Specifications**

- **InspectionController (Evidence & Findings)** & **ExifMetadataExtractor**: Decode uploaded image bytes, extract EXIF GPS/capture timestamps, store objects in MinIO, support single/bulk soft-retirement (`is_deleted = true`), manage `Finding` CRUD/confirmation, and lock `findings_snapshot_hash` (`FIELD_COMPLETED -> REPORT_DRAFT`).
- **PrimaryWithFallbackInference, YoloInferenceClient & OpenAiCompatibleInferenceClient**: Invoke the self-hosted FastAPI Ultralytics `YOLO11 (mbdd2025-v1)` container (`POST /predict`) with optional multimodal vision fallback.

#### 3.8.2 YOLO11 Defect Detection and Verification Sequence Diagram

```mermaid
%% title: YOLO11 Defect Detection and Verification Sequence Diagram
sequenceDiagram
  autonumber
  actor Inspector as Assigned Inspector
  participant Client as Web Portal
  participant InspCtrl as InspectionController
  participant Infer as PrimaryWithFallbackInference
  participant YoloSvc as FastAPI YOLO11 (/predict)
  participant DB as PostgreSQL (findings, inspections)

  Inspector->>Client: Select Active Evidence Image & Click Analyze
  Client->>InspCtrl: POST /api/v1/inspections/{id}/evidence/{evidenceId}/analyze
  InspCtrl->>Infer: analyze(imageBytes, contentType, visionFallbackEnabled)
  Infer->>YoloSvc: POST /predict (multipart image)
  YoloSvc-->>Infer: Detections (defectLabel, confidence, normalizedBoundingBox)
  InspCtrl->>DB: insertFindings(status=PENDING, modelName='yolo11s', confidence, boundingBox)
  DB-->>InspCtrl: Persisted PENDING Findings
  InspCtrl-->>Client: 200 OK (EvidenceAnalysisResponse)

  Inspector->>Client: Review Bounding Box, Edit Severity & Confirm Finding
  Client->>InspCtrl: POST /api/v1/inspections/{id}/findings/{findingId}/confirmation
  InspCtrl->>DB: confirmByInspector() -> status=CONFIRMED
  InspCtrl-->>Client: 200 OK (FindingResponse status=CONFIRMED)

  Inspector->>Client: Confirm Official Findings Set Baseline
  Client->>InspCtrl: POST /api/v1/inspections/{id}/findings/confirm
  InspCtrl->>DB: ensureNoUnresolvedPendingFindings & computeSnapshotHash -> status=REPORT_DRAFT
  InspCtrl-->>Client: 200 OK (WorkflowStateResponse status=REPORT_DRAFT)
```

---

### 3.9 FE-09 Inspection Reporting & Publication

#### 3.9.1 Class Diagram

```mermaid
%% title: Inspection Report Authoring, Review and PDF Publication Class Diagram
classDiagram
  class InspectionController {
    +generateAiReportDraft(Jwt, UUID) ResponseEntity~ApiResponse~
    +createManualReportDraft(Jwt, UUID) ResponseEntity~ApiResponse~
    +updateReportSections(Jwt, UUID, UUID, UpdateReportSectionsRequest) ApiResponse~ReportVersionResponse~
    +previewReportPdf(Jwt, UUID, UUID) ResponseEntity~byte[]~
    +verifyReportAsAuthor(Jwt, UUID, UUID) ApiResponse~ReportVersionResponse~
    +submitReportVersion(Jwt, UUID, UUID) ApiResponse~ReportVersionResponse~
    +reviewReportVersion(Jwt, UUID, UUID, ReviewReportRequest) ApiResponse~ReportVersionResponse~
    +publishReportVersion(Jwt, UUID, UUID) ApiResponse~ReportVersionResponse~
    +completeCorrectiveHandoff(Jwt, UUID, CorrectiveHandoffRequest) ApiResponse~CorrectiveHandoffResponse~
  }
  class ReportDraftClient {
    +generateDraftSections(GroundedReportPrompt prompt) DraftSections
  }
  class PdfReportRenderer {
    +render(InspectionReportRenderModel model) byte[]
  }
  class InspectionReport {
    -UUID id
    -UUID inspectionId
    -int versionNo
    -ReportStatus status
    -String contentSnapshot
    -UUID reviewerUserId
    -String renderedObjectKey
    -String renderedChecksumSha256
  }
  InspectionController --> ReportDraftClient
  InspectionController --> PdfReportRenderer
  InspectionController --> InspectionReport
```

**Class Specifications**

- **InspectionController (Reports & Corrective Handoff)**: Orchestrates LLM (`ReportDraftClient`) and manual report draft creation (`DRAFT`), section editing, live PDF preview, author verification (`AUTHOR_VERIFIED`), submission (`SUBMITTED`), independent `ORG_MANAGER` review (`APPROVED` / `RETURNED`), immutable PDF publication (`PUBLISHED`), and per-finding corrective handoff (`REPAIR_PENDING` / `COMPLETED`).
- **PdfReportRenderer**: Renders publication-grade A4 PDF documents via OpenHTMLtoPDF and computes 64-character SHA-256 digests stored in MinIO.

#### 3.9.2 Report Synthesis, Review and Immutable Publication Sequence Diagram

```mermaid
%% title: Report Synthesis, Review and Immutable Publication Sequence Diagram
sequenceDiagram
  autonumber
  actor Inspector as Assigned Inspector (Author)
  actor OM as Independent Organization Manager
  participant Client as Web Portal
  participant InspCtrl as InspectionController
  participant LLM as ReportDraftClient (LLM)
  participant Renderer as PdfReportRenderer
  participant MinIO as MinIO Object Storage
  participant DB as PostgreSQL (inspection_reports, inspections, findings)

  Inspector->>Client: Generate Report Draft (AI-Assisted or Manual)
  Client->>InspCtrl: POST /api/v1/inspections/{id}/report/draft
  InspCtrl->>LLM: generateDraftSections(asset, checkpoints, confirmedFindings)
  LLM-->>InspCtrl: Structured JSON Sections
  InspCtrl->>DB: insertInspectionReport(versionNo, status=DRAFT, contentSnapshot)
  InspCtrl-->>Client: 201 Created (ReportVersionResponse status=DRAFT)

  Inspector->>Client: Edit Sections, Author-Verify & Submit for Review
  Client->>InspCtrl: POST /api/v1/inspections/{id}/report/versions/{vId}/verify
  InspCtrl->>DB: verifyAsAuthor() -> status=AUTHOR_VERIFIED
  Client->>InspCtrl: POST /api/v1/inspections/{id}/report/versions/{vId}/submit
  InspCtrl->>DB: submit() -> status=SUBMITTED (locks source findings/evidence)

  OM->>Client: Approve & Publish Report Version
  Client->>InspCtrl: POST /api/v1/inspections/{id}/report/versions/{vId}/review (approve=true)
  InspCtrl->>DB: reviewBy(omUserId != inspectorId, approve=true) -> status=APPROVED
  Client->>InspCtrl: POST /api/v1/inspections/{id}/report/versions/{vId}/publish
  InspCtrl->>Renderer: render(reportContext) -> pdfBytes
  InspCtrl->>MinIO: putObject(inspection-evidence, renderedObjectKey, pdfBytes)
  InspCtrl->>DB: publish(renderedObjectKey, sha256) -> Report: PUBLISHED, Inspection: REPORT_PUBLISHED
  InspCtrl-->>Client: 200 OK (Published PDF & SHA-256 Digest)
```

#### 3.9.3 WF-03 Activity Diagram — AI Defect Detection, Report Publication & Corrective Handoff

```mermaid
%% title: WF-03 Activity Diagram - AI Defect Detection, Report Publication and Corrective Handoff
flowchart TD
  subgraph IN3["Assigned Inspector (INSPECTOR)"]
    C1(["Start: Select Active Evidence Image & Click Analyze"])
    C3["Review Pending Proposals: Confirm / Modify / Soft-Delete / Add Manual"]
    C4["Confirm Findings Set Baseline -> Inspection: REPORT_DRAFT"]
    C5["Generate Report Draft (LLM / Manual) -> Report: DRAFT"]
    C6["Edit Sections, Preview PDF, Verify (AUTHOR_VERIFIED) & Submit (SUBMITTED)"]
  end

  subgraph AI3["YOLO11 Service / LLM Gateway / PdfReportRenderer"]
    C2["Run YOLO11 (mbdd2025-v1) -> Save Findings: PENDING"]
    C9["Render Immutable A4 PDF + SHA-256 to MinIO ->\nReport: PUBLISHED, Inspection: REPORT_PUBLISHED"]
  end

  subgraph OM3["Independent Organization Manager (ORG_MANAGER)"]
    C7{"Approve or Return\nSubmitted Report?"}
    C8["Approve Report (APPROVED) & Trigger Publish"]
    C10["Return Report with Reason -> Report: RETURNED (Unlocks Edits)"]
    C11["Select Confirmed Findings for Corrective Handoff ->\nInspection: REPAIR_PENDING (or COMPLETED)"]
    C12(["End: Forwarded Findings Ready for MF4 Maintenance"])
  end

  C1 --> C2 --> C3 --> C4 --> C5 --> C6 --> C7
  C7 -->|"Return"| C10 --> C6
  C7 -->|"Approve"| C8 --> C9 --> C11 --> C12
```

---

### 3.10 FE-10 Maintenance Planning & AI Scope Advisory

#### 3.10.1 Class Diagram

```mermaid
%% title: Maintenance Work Order, RAG Advisor and Cost Control Class Diagram
classDiagram
  class MaintenanceController {
    +suggestScope(Jwt, ScopeSuggestionRequest) ApiResponse~ScopeSuggestionResponse~
    +createWorkOrder(Jwt, CreateWorkOrderRequest) ResponseEntity~ApiResponse~
    +assignTeam(Jwt, UUID, AssignTeamRequest) ApiResponse~List~
    +createTask(Jwt, UUID, CreateMaintenanceTaskRequest) ResponseEntity~ApiResponse~
    +createEstimateVersion(Jwt, UUID, CreateEstimateVersionRequest) ResponseEntity~ApiResponse~
    +submitEstimateVersion(Jwt, UUID, int) ApiResponse~EstimateVersionView~
    +approveEstimateVersion(Jwt, UUID, int) ApiResponse~EstimateVersionView~
  }
  class MaintenanceExecutionController {
    +releaseWorkOrder(Jwt, UUID) ApiResponse~WorkOrderView~
    +startWorkOrder(Jwt, UUID) ApiResponse~WorkOrderView~
    +createWorkLog(Jwt, UUID, CreateWorkLogRequest) ResponseEntity~ApiResponse~
    +submitWorkLog(Jwt, UUID, UUID) ApiResponse~WorkLogView~
    +verifyWorkLog(Jwt, UUID, UUID) ApiResponse~WorkLogView~
    +declareComplete(Jwt, UUID) ApiResponse~WorkOrderView~
    +createReportVersion(Jwt, UUID, CreateMaintenanceReportRequest) ResponseEntity~ApiResponse~
    +verifyReportVersion(Jwt, UUID, int) ApiResponse~MaintenanceReportView~
    +submitReportVersion(Jwt, UUID, int) ApiResponse~MaintenanceReportView~
    +recordAcceptanceDecision(Jwt, UUID, RecordAcceptanceRequest) ResponseEntity~ApiResponse~
    +reconcileCosts(Jwt, UUID, ReconcileCostsRequest) ApiResponse~CostReconciliationView~
    +closeWorkOrder(Jwt, UUID) ApiResponse~WorkOrderView~
  }
  class MaintenanceScopeAdvisorService {
    +suggestScope(ScopeSuggestionRequest) ScopeSuggestionResponse
  }
  class MaintenanceReportRenderer {
    +render(MaintenanceReportRenderModel) byte[]
  }
  class MaintenanceWorkOrder {
    -UUID id
    -WorkOrderStatus status
    -UUID budgetApproverUserId
    -UUID teamLeadUserId
    -UUID reportAuthorUserId
    -UUID acceptingReviewerUserId
  }
  MaintenanceController --> MaintenanceScopeAdvisorService
  MaintenanceController --> MaintenanceWorkOrder
  MaintenanceExecutionController --> MaintenanceWorkOrder
  MaintenanceExecutionController --> MaintenanceReportRenderer
```

**Class Specifications**

- **MaintenanceController**: Manages repair candidate queries, `MaintenanceWorkOrder` creation (`DRAFT`), team role assignment (`LEAD`, `REPORT_AUTHOR`, `MEMBER`, independent `acceptingReviewerUserId`), `MaintenanceTask` decomposition, and `MaintenanceEstimateVersion` submission/approval.
- **MaintenanceScopeAdvisorService & DeterministicScopeFallback**: Retrieve civil engineering repair standards (`TCVN 9343:2012`, `EN 1504-9`, `ISO 12944-5`, `ASTM C1583`, `TCVN 9361:2012`) from `repair_knowledge_chunks` (`pgvector`) and synthesize corrective scope, acceptance criteria, and suggested tasks.

#### 3.10.2 Work Order Planning, Cost Estimation and Technical Acceptance Sequence Diagram

```mermaid
%% title: Work Order Planning, Cost Estimation and Technical Acceptance Sequence Diagram
sequenceDiagram
  autonumber
  actor OM as Organization Manager (Approver / Independent Reviewer)
  actor Lead as Maintenance Engineer (LEAD & REPORT_AUTHOR)
  participant Client as Web / Mobile Client
  participant MaintCtrl as MaintenanceController
  participant ExecCtrl as MaintenanceExecutionController
  participant Advisor as MaintenanceScopeAdvisorService
  participant DB as PostgreSQL (maintenance_* tables)
  participant MinIO as MinIO Object Storage

  OM->>Client: Create WorkOrder from Forwarded Finding & Assign Team
  Client->>MaintCtrl: POST /api/v1/maintenance/work-orders & POST /team
  MaintCtrl->>DB: insertWorkOrder(status=DRAFT) & saveTeam(LEAD, REPORT_AUTHOR, acceptingReviewerUserId)

  Lead->>Client: Request RAG Scope Advice, Create Tasks & Submit Estimate
  Client->>MaintCtrl: POST /api/v1/maintenance/suggest-scope
  MaintCtrl->>Advisor: suggestScope(defectLabel, severity, category) -> TCVN/EN/ISO standards
  Advisor-->>Client: CorrectiveScope, AcceptanceCriteria & SuggestedTasks
  Client->>MaintCtrl: POST /estimate-versions & POST /estimate-versions/1/submit
  MaintCtrl->>DB: saveEstimateLines(ESTIMATE) & updateWorkOrder(status=AWAITING_APPROVAL)

  OM->>Client: Approve Estimate Baseline (omUserId != preparedByUserId)
  Client->>MaintCtrl: POST /api/v1/maintenance/work-orders/{id}/estimate-versions/1/approve
  MaintCtrl->>DB: approveEstimate() -> WorkOrder: APPROVED

  Lead->>Client: Release (READY), Start (IN_PROGRESS), Log & Verify WorkLogs, Declare Complete
  Client->>ExecCtrl: POST /release -> POST /start -> POST /work-logs -> POST /verify -> POST /declare-complete
  ExecCtrl->>DB: verifyAllLogsVerified & updateWorkOrder(status=WORK_COMPLETED)

  Lead->>Client: Author, Verify (AUTHOR_VERIFIED) & Submit Completion Report
  Client->>ExecCtrl: POST /reports -> POST /reports/1/verify -> POST /reports/1/submit
  ExecCtrl->>DB: updateWorkOrder(status=SUBMITTED_FOR_ACCEPTANCE)

  OM->>Client: Record Independent Acceptance (ACCEPTED), Reconcile Actual Costs & Close
  Client->>ExecCtrl: POST /acceptance-decisions (ACCEPTED) -> POST /cost-reconciliation -> POST /close
  ExecCtrl->>MinIO: storeRenderedCompletionPdf(sha256)
  ExecCtrl->>DB: updateWorkOrder(ACCEPTED -> COST_RECONCILED -> CLOSED)
  ExecCtrl-->>Client: 200 OK (WorkOrderView status=CLOSED)
```

---

### 3.11 FE-11 Cost Estimation & Repair Execution

#### 3.11.1 Class Diagram

Refer to the Maintenance Work Order, RAG Advisor and Cost Control Class Diagram in **Section 3.10.1** (`MaintenanceController` and `MaintenanceExecutionController`).

#### 3.11.2 Estimate Approval, Change Order & Verified Work Log Sequence Diagram

Refer to Steps 3–5 of the Work Order Planning, Cost Estimation and Technical Acceptance Sequence Diagram in **Section 3.10.2**.

---

### 3.12 FE-12 Maintenance Acceptance & Cost Closure

#### 3.12.1 Class Diagram

Refer to `MaintenanceExecutionController` and `MaintenanceReportRenderer` in **Section 3.10.1**.

#### 3.12.2 Completion Report, Independent Acceptance & Cost Reconciliation Sequence Diagram

Refer to Steps 6–7 of the Sequence Diagram in **Section 3.10.2**.

#### 3.12.3 WF-04 Activity Diagram — Maintenance Work Order Lifecycle & Cost Reconciliation

```mermaid
%% title: WF-04 Activity Diagram - Maintenance Work Order Lifecycle and Cost Reconciliation
flowchart TD
  subgraph OM4["Organization Manager (Budget Approver & Independent Reviewer)"]
    D1(["Start: Create WorkOrder from Forwarded Finding -> WorkOrder: DRAFT"])
    D2["Assign Team (LEAD, REPORT_AUTHOR, MEMBER) & Independent Reviewer"]
    D5{"Approve Estimate\nBaseline?"}
    D6["Approve Estimate -> Estimate: APPROVED, WorkOrder: APPROVED"]
    D10{"Independent Technical\nAcceptance Decision?"}
    D11["Record ACCEPTED -> Render Completion PDF + SHA-256 -> WorkOrder: ACCEPTED"]
    D12["Record REWORK_REQUIRED / REINSPECTION_REQUIRED"]
    D13["Reconcile Actual Cost Lines vs. Baseline + Change Deltas -> COST_RECONCILED"]
    D14(["End: Close WorkOrder (CLOSED) & Update Inspection to COMPLETED"])
  end

  subgraph ME4["Maintenance Engineer Team (LEAD, REPORT_AUTHOR, MEMBER)"]
    D3["Invoke RAG Scope Advisor (TCVN/EN/ISO), Plan Tasks & Submit Estimate -> AWAITING_APPROVAL"]
    D7["Release (READY) & Start (IN_PROGRESS) WorkOrder"]
    D8["Log Task WorkLogs (SUBMITTED), Lead Verifies (VERIFIED) & Declare Complete -> WORK_COMPLETED"]
    D9["Author, Verify (AUTHOR_VERIFIED) & Submit Completion Report -> SUBMITTED_FOR_ACCEPTANCE"]
  end

  D1 --> D2 --> D3 --> D5
  D5 -->|"Reject"| D3
  D5 -->|"Approve"| D6 --> D7 --> D8 --> D9 --> D10
  D10 -->|"Rework / Reinspection"| D12 --> D8
  D10 -->|"Accepted"| D11 --> D13 --> D14
```
