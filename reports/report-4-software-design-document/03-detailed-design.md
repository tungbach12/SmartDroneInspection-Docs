---
title: "Report 4 - Detailed Design"
document_type: report4-sdd-section
weight: 35
source: "report4-software-design-document.docx"
---

## 3. Detailed Design

### 3.1 FE-01 Customer Registration, Sign-In and Account Access

This section presents the detailed design for `FE-01` (Customer organization and initial asset registration with No-Fly Zone airspace screening, Argon2id credential sign-in, consolidated OTP verification, Google OAuth 2.0 federation, JWT session rotation, and four-role `ActorZone` access control).

#### 3.1.1 Class Diagram

```mermaid
%% title: FE-01 Customer Registration, Sign-In and Account Access Class Diagram
classDiagram
  class BrowserAuthController {
    +register(req) ApiResponse
    +sendRegistrationOtp(req) ApiResponse
    +login(req) ApiResponse
    +verifyLoginOtp(req) ApiResponse
    +sendPasswordResetOtp(req) ApiResponse
    +confirmPasswordReset(req) ApiResponse
    +changePassword(req) ApiResponse
    +refresh() ApiResponse
  }
  class MobileAuthController {
    +login(req) ApiResponse
    +verifyLoginOtp(req) ApiResponse
    +changePassword(req) ApiResponse
    +refresh(req) ApiResponse
    +logout(req) ApiResponse
  }
  class OAuth2Controller {
    +authorizeGoogle(clientType) void
    +googleCallback(code, state) void
  }
  class UserProfileController {
    +getProfile() CurrentUserResponse
    +updatePilotLicense(req) CurrentUserResponse
    +updateAiFallbackPreference(req) CurrentUserResponse
  }
  class AuthService {
    +registerCustomer(req) RegistrationResult
    +login(email, password) LoginResult
    +loginWithGoogle(profile) LoginResult
  }
  class User {
    -UUID id
    -UUID organizationId
    -String email
    -String fullName
    -UserStatus status
    -ActorZone actorZone
    -String roles
  }
  class OtpChallenge {
    -UUID id
    -OtpChallengePurpose purpose
    -UUID userId
    -String destination
    -Instant expiresAt
    -Instant consumedAt
  }
  class ProspectiveCustomerRegistration {
    -UUID id
    -UUID userId
    -String organizationName
    -String assetName
    -BigDecimal latitude
    -BigDecimal longitude
    -String airspaceClassification
    -String status
  }
  BrowserAuthController --> AuthService
  BrowserAuthController --> OtpChallenge
  MobileAuthController --> AuthService
  MobileAuthController --> OtpChallenge
  OAuth2Controller --> AuthService
  UserProfileController --> AuthService
  AuthService --> User
  AuthService --> ProspectiveCustomerRegistration
```

**Class Specifications**

| No | Class | Description |
| :---: | :--- | :--- |
| 01 | `BrowserAuthController` & `MobileAuthController` | Handle customer registration, email and password sign-in, one-time verification code delivery and confirmation, password reset, password change, and session token refresh for web (`HttpOnly` cookie) and mobile (`Bearer` / refresh token) clients. |
| 02 | `OAuth2Controller` | Handles federated Google OAuth 2.0 sign-in and callback redirection for web browsers and mobile deep links (`smartdrone://auth`). |
| 03 | `UserProfileController` | Allows signed-in users to retrieve their current profile (`/api/v1/users/me`), update pilot license credentials, and configure AI vision fallback preferences. |
| 04 | `AuthService` | Coordinates Argon2id credential verification, account lockout after repeated failed attempts (`LoginFailureService`), airspace screening during customer onboarding (`CustomerAirspacePolicyAdapter`), and JWT session issuance (`AccessTokenService`, `RefreshCookieService`). |
| 05 | `User` & `OtpChallenge` | Domain entities representing user accounts across the four active system roles (`ADMIN`, `MANAGER`, `CUSTOMER`, `INSPECTOR`) and consolidated time-limited OTP challenges (`LOGIN`, `REGISTRATION`, `PASSWORD_RESET`). |
| 06 | `ProspectiveCustomerRegistration` | Domain entity recording a customer organization and initial asset registration request along with its airspace classification result (`CLEAR_ZONE`, `RESTRICTED_ZONE`, `NO_FLY_ZONE`). |

#### 3.1.2 Customer Organization and Initial Asset Registration Sequence Diagram

```mermaid
%% title: FE-01 Customer Organization and Initial Asset Registration Sequence Diagram
sequenceDiagram
  autonumber
  actor Cust as Prospective Customer
  participant Web as Web Portal (RegisterPage)
  participant Ctrl as BrowserAuthController
  participant OtpSvc as RegistrationOtpService
  participant RegSvc as OrganizationRegistrationService
  participant Airspace as CustomerAirspacePolicyAdapter
  participant DB as PostgreSQL

  Cust->>Web: Enter email and request registration OTP
  Web->>Ctrl: POST /api/v1/auth/register/otp
  Ctrl->>OtpSvc: sendRegistrationOtp(email, clientIp)
  OtpSvc->>DB: Save REGISTRATION OtpChallenge (otp_challenges)
  OtpSvc-->>Web: Return challengeId and masked destination

  Cust->>Web: Submit organization details, OTP code, and initial asset coordinates
  Web->>Ctrl: POST /api/v1/auth/register
  Ctrl->>OtpSvc: verifyAndConsume(challengeId, email, otpCode)
  OtpSvc->>DB: Mark OtpChallenge consumed
  Ctrl->>RegSvc: register(request)
  RegSvc->>Airspace: evaluateFirstAsset(latitude, longitude)
  alt Prohibited No-Fly Zone (NO_FLY_ZONE)
    Airspace-->>RegSvc: Prohibited zone detected
    RegSvc-->>Web: Reject registration (403 Forbidden)
  else Restricted Zone (RESTRICTED_ZONE)
    Airspace-->>RegSvc: Restricted zone requires review
    RegSvc->>DB: Save PENDING ProspectiveCustomerRegistration and User
    RegSvc-->>Web: Return 201 Created (pending platform review)
  else Clear Zone (CLEAR_ZONE)
    Airspace-->>RegSvc: Clear zone approved
    RegSvc->>DB: Save ACTIVE Organization, CUSTOMER User, initial Asset, and AuditEvent
    RegSvc-->>Web: Return 201 Created (account active)
  end
```

#### 3.1.3 User Sign-In, OTP Verification and Google OAuth 2.0 Sequence Diagram

```mermaid
%% title: FE-01 User Sign-In, OTP Verification and Google OAuth 2.0 Sequence Diagram
sequenceDiagram
  autonumber
  actor User as System User
  participant App as Web Portal / Mobile App
  participant Ctrl as BrowserAuthController / OAuth2Controller
  participant Auth as AuthService
  participant Otp as LoginOtpService
  participant DB as PostgreSQL

  alt Email & Password Sign-In
    User->>App: Enter email and password
    App->>Ctrl: POST /api/v1/auth/login (or /api/v1/mobile/auth/login)
    Ctrl->>Auth: login(email, password, clientIp, userAgent)
    Auth->>DB: Verify Argon2id password hash and lockout status (users)
    alt OTP Challenge Required
      Auth->>Otp: createLoginChallenge(user, clientIp)
      Otp->>DB: Save LOGIN OtpChallenge (otp_challenges)
      Auth-->>App: Return otpRequired = true and challengeId
      User->>App: Enter 6-digit OTP code
      App->>Ctrl: POST /api/v1/auth/login/otp/verify
      Ctrl->>Otp: verifyChallenge(challengeId, otpCode)
      Otp->>DB: Mark OtpChallenge consumed and set user.otp_verified = true
    end
    Auth->>DB: Create active AuthSession (auth_sessions) and AuditEvent
    Auth-->>App: Return HS256 JWT access token and refresh credential
  else Google OAuth 2.0 Sign-In
    User->>App: Click Sign in with Google
    App->>Ctrl: GET /api/v1/auth/oauth2/google?client=web|mobile
    Ctrl-->>User: Redirect to Google OAuth 2.0 consent screen
    User->>Ctrl: GET /api/v1/auth/oauth2/google/callback?code=...&state=...
    Ctrl->>Auth: loginWithGoogle(googleProfile, clientType)
    Auth->>DB: Match active User and create AuthSession (auth_sessions)
    Ctrl-->>App: Redirect to Web callback or Mobile smartdrone://auth deep link
  end
```

---

### 3.2 FE-02 Partner Qualification, Workforce, Assets and Drone Registration

This section presents the detailed design for `FE-02` (Platform-provisioned Inspector accounts, pilot license profiles and flight logs, restricted-airspace customer review, infrastructure asset catalog with `inspection_items` checkpoints and reference documents, and Inspector-owned drone 3-document registration).

#### 3.2.1 Class Diagram

```mermaid
%% title: FE-02 Partner Qualification, Workforce, Assets and Drone Registration Class Diagram
classDiagram
  class PlatformUserController {
    +listUsers(page, size, query) PagedResponse
    +createUser(req) ApiResponse
    +updateRoles(userId, req) ApiResponse
    +updateStatus(userId, req) ApiResponse
  }
  class InspectorProfileController {
    +listInspectors() List~InspectorProfileResponse~
    +updateProfile(userId, req) InspectorProfileResponse
    +uploadLicenseScan(userId, file) InspectorProfileResponse
    +recordFlightLog(userId, req) InspectorFlightLogResponse
  }
  class WorkforceController {
    +createWorkforceUser(req) ApiResponse
    +listWorkforceUsers(page, size, query) PagedResponse
  }
  class AssetController {
    +createAsset(req) ApiResponse
    +listAssets(page, size, query) PagedResponse
    +updateAsset(assetId, req) AssetView
    +retireAsset(assetId) AssetView
  }
  class AssetDocumentController {
    +upload(assetId, docType, file) AssetDocumentResponse
    +list(assetId) List~AssetDocumentResponse~
    +download(assetId, docId) ResponseEntity
  }
  class DroneRegistrationApplicationController {
    +uploadEvidence(docType, file) UploadedKeyResponse
    +submit(req) ApiResponse
    +listPending() List~DroneRegistrationResponse~
    +approve(appId, req) DroneRegistrationResponse
    +reject(appId, req) DroneRegistrationResponse
  }
  class InspectorProfile {
    -UUID userId
    -String pilotLicenseNumber
    -String pilotLicenseClass
    -Instant pilotLicenseExpiresAt
    -BigDecimal priorFlightHours
  }
  class DroneRegistrationApplication {
    -UUID id
    -UUID inspectorUserId
    -String serialNumber
    -String registrationFileKey
    -String ownershipFileKey
    -String inspectionFileKey
    -String status
  }
  class Drone {
    -UUID id
    -UUID inspectorOwnerId
    -String serialNumber
    -String model
    -DroneServiceability serviceability
  }
  class Asset {
    -UUID id
    -UUID organizationId
    -String assetCode
    -String name
    -BigDecimal latitude
    -BigDecimal longitude
    -AssetStatus status
  }
  PlatformUserController --> InspectorProfile
  InspectorProfileController --> InspectorProfile
  DroneRegistrationApplicationController --> DroneRegistrationApplication
  DroneRegistrationApplication --> Drone
  AssetController --> Asset
  AssetDocumentController --> Asset
```

**Class Specifications**

| No | Class | Description |
| :---: | :--- | :--- |
| 01 | `PlatformUserController` & `InspectorProfileController` | Allow platform administrators and managers to provision `INSPECTOR` accounts, maintain pilot license credentials in `inspector_profiles`, upload license scans, and record flight logs in `inspector_flight_logs`. |
| 02 | `WorkforceController` & `WorkforceService` | Retired maintenance-account provisioning; not an active product API or workflow. |
| 03 | `AssetController` & `AssetDocumentController` | Manage customer infrastructure assets, structural inspection checkpoints (`inspection_items`), and SHA-256 engineering reference documents in MinIO, blocking asset creation inside prohibited No-Fly Zones. |
| 04 | `DroneRegistrationApplicationController` & `DroneRegistrationApplicationService` | Handle Inspector-owned drone registration submissions with three required documents (`REGISTRATION`, `OWNERSHIP`, and `INSPECTION`) and platform review decisions. |
| 05 | `InspectorProfile`, `Drone` & `Asset` | Domain entities representing Inspector qualifications, approved Inspector-owned drones, and customer infrastructure assets. |

#### 3.2.2 Inspector Provisioning, License Profile and Customer Workforce Sequence Diagram

```mermaid
%% title: FE-02 Inspector Provisioning, License Profile and Customer Workforce Sequence Diagram
sequenceDiagram
  autonumber
  actor Admin as Admin or Manager
  actor Cust as Customer
  actor Insp as Inspector
  participant PlatCtrl as PlatformUserController / InspectorProfileController
  participant WorkCtrl as WorkforceController
  participant UserSvc as AdminUserService / InspectorProfileService / WorkforceService
  participant DB as PostgreSQL & MinIO

  Admin->>PlatCtrl: POST /api/v1/platform/users (role = INSPECTOR)
  PlatCtrl->>UserSvc: createUser(request)
  UserSvc->>DB: Insert User (actor_zone = INSPECTOR_PARTNER) and InspectorProfile
  DB-->>Admin: Return provisioned Inspector account (201 Created)

  Admin->>PlatCtrl: PUT /api/v1/platform/inspectors/{id} & POST /license-scan
  PlatCtrl->>UserSvc: updateProfile(userId, req) & uploadLicenseScan(userId, file)
  UserSvc->>DB: Store license scan in MinIO and update inspector_profiles
  Insp->>PlatCtrl: GET /api/v1/platform/inspectors/{id}/flight-logs
  PlatCtrl->>UserSvc: listFlightLogs(userId)
  UserSvc->>DB: Query inspector_flight_logs

  Note over Cust,WorkCtrl: Legacy maintenance provisioning interaction; excluded from current scope
  WorkCtrl->>UserSvc: createWorkforceUser(customerActorId, request)
  UserSvc->>DB: Verify same-tenant email uniqueness and insert User (must_change_password = true)
  Note over Cust,DB: Legacy maintenance records are retained; no provisioning workflow is exposed
```

#### 3.2.3 Infrastructure Asset and Reference Document Registration Sequence Diagram

```mermaid
%% title: FE-02 Infrastructure Asset and Reference Document Registration Sequence Diagram
sequenceDiagram
  autonumber
  actor Cust as Customer
  participant AssetCtrl as AssetController / AssetDocumentController
  participant AssetSvc as AssetService / AssetDocumentService
  participant Airspace as AirspaceAdvisoryService
  participant Store as MinioEvidenceObjectStore
  participant DB as PostgreSQL

  Cust->>AssetCtrl: POST /api/v1/assets (assetCode, coordinates, inspectionItems)
  AssetCtrl->>AssetSvc: createAsset(actorId, request)
  AssetSvc->>Airspace: evaluate(latitude, longitude, maxAltitudeMeters)
  alt Coordinates inside Prohibited No-Fly Zone
    Airspace-->>AssetSvc: NO_FLY_ZONE classification
    AssetSvc-->>Cust: Return 403 Forbidden (ASSET_IN_NO_FLY_ZONE)
  else Clear or Restricted Zone
    Airspace-->>AssetSvc: CLEAR_ZONE or RESTRICTED_ZONE
    AssetSvc->>DB: Verify unique (organization_id, asset_code) and save ACTIVE Asset
    AssetSvc-->>Cust: Return created Asset with inspection_items JSONB (201 Created)
  end

  Cust->>AssetCtrl: POST /api/v1/assets/{assetId}/documents (MultipartFile)
  AssetCtrl->>AssetSvc: uploadDocument(actorId, assetId, docType, file)
  AssetSvc->>AssetSvc: Compute SHA-256 checksum and check duplicate on asset
  AssetSvc->>Store: put(objectKey, contentType, sizeBytes, stream)
  AssetSvc->>DB: Insert AssetDocument (asset_documents)
  AssetSvc-->>Cust: Return AssetDocumentResponse (201 Created)
```

#### 3.2.4 Inspector-Owned Drone Registration and Approval Sequence Diagram

```mermaid
%% title: FE-02 Inspector-Owned Drone Registration and Approval Sequence Diagram
sequenceDiagram
  autonumber
  actor Insp as Inspector
  actor Mgr as Admin or Manager
  participant Ctrl as DroneRegistrationApplicationController
  participant Svc as DroneRegistrationApplicationService
  participant Store as MinioEvidenceObjectStore
  participant DB as PostgreSQL

  Insp->>Ctrl: POST /api/v1/drones/registrations/evidence (REGISTRATION, OWNERSHIP, INSPECTION)
  Ctrl->>Svc: uploadEvidence(inspectorId, docType, file)
  Svc->>Store: Store 3 supporting document files in MinIO
  Store-->>Svc: Return registrationFileKey, ownershipFileKey, inspectionFileKey

  Insp->>Ctrl: POST /api/v1/drones/registrations (serialNumber, model, 3 file keys)
  Ctrl->>Svc: submit(inspectorId, request)
  Svc->>DB: Verify all 3 document keys present, unique serialNumber, and save PENDING application
  DB-->>Insp: Confirm application submitted (201 Created)

  Mgr->>Ctrl: POST /api/v1/platform/drone-registrations/{id}/approve
  Ctrl->>Svc: approve(reviewerId, applicationId, request)
  Svc->>DB: Create ACTIVE Drone (inspector_owner_id = inspectorId) and mark application APPROVED
  DB-->>Mgr: Return approved DroneRegistrationResponse (200 OK)
```

---

### 3.3 FE-03 Recurring Service Requests, Occurrences and Notifications

This section presents the detailed design for `FE-03` (Recurring service request cadence validation, count-bound and end-date-bound `ServiceRequestOccurrence` materialization with month-end date anchoring, and deduplicated in-app notifications via the Spring Modulith transactional event outbox).

#### 3.3.1 Class Diagram

```mermaid
%% title: FE-03 Recurring Occurrences and Notification Inbox Class Diagram
classDiagram
  class ContractWorkflowService {
    +acceptQuote(actorId, reqId, versionNo) ServiceRequestResponse
    +uploadSignedContract(actorId, reqId, file) ServiceRequestResponse
    +assignOccurrence(actorId, reqId, occId, assignReq) ServiceRequestResponse
  }
  class ServiceRequestOccurrence {
    -UUID id
    -UUID requestId
    -int occurrenceIndex
    -Instant plannedStartAt
    -Instant plannedEndAt
    -OccurrenceStatus status
  }
  class NotificationController {
    +listNotifications(page, size, unreadOnly) NotificationPageResponse
    +getUnreadCount() NotificationUnreadCountResponse
    +markRead(notificationId) NotificationResponse
  }
  class NotificationService {
    +list(userId, page, pageSize, unreadOnly) NotificationPageResponse
    +unreadCount(userId) NotificationUnreadCountResponse
    +markAsRead(userId, notificationId) NotificationResponse
  }
  class InspectionNotificationListener {
    +onInspectionAssigned(event) void
    +onInspectionReminderDue(event) void
    +onFieldSessionAborted(event) void
  }
  class MaintenanceNotificationListener {
    +onWorkOrderAssigned(event) void
    +onEstimateApproved(event) void
    +onChangeOrderApproved(event) void
    +onAcceptanceRecorded(event) void
    +onWorkOrderClosed(event) void
  }
  class Notification {
    -UUID id
    -UUID organizationId
    -UUID recipientUserId
    -String eventType
    -String title
    -NotificationStatus status
    -String deduplicationKey
  }
  ContractWorkflowService --> ServiceRequestOccurrence
  NotificationController --> NotificationService
  InspectionNotificationListener --> Notification
  MaintenanceNotificationListener --> Notification
  NotificationService --> Notification
```

**Class Specifications**

| No | Class | Description |
| :---: | :--- | :--- |
| 01 | `ContractWorkflowService` & `ServiceRequestOccurrence` | Materialize count-bound or end-date-bound `ServiceRequestOccurrence` rows with month-end anchoring when a Customer accepts a recurring quotation and the signed contract is recorded. |
| 02 | `NotificationController` & `NotificationService` | Provide the role- and organization-scoped in-app notification inbox, unread notification counter, and idempotent `SENT -> READ` updates for signed-in users. |
| 03 | `InspectionNotificationListener` & `MaintenanceNotificationListener` | Consume transactional Spring Modulith domain events (`InspectionAssignedEvent`, `InspectionReminderDueEvent`, `FieldSessionAbortedEvent`, `WorkOrderAssignedEvent`, `EstimateApprovedEvent`, `ChangeOrderApprovedEvent`, `AcceptanceRecordedEvent`, `WorkOrderClosedEvent`) to persist deduplicated notifications. |
| 04 | `Notification` | Domain entity representing an in-app user notification protected by `uq_notifications_deduplication_key`. |

#### 3.3.2 Recurring Service Request Occurrence Materialization Sequence Diagram

```mermaid
%% title: FE-03 Recurring Service Request Occurrence Materialization Sequence Diagram
sequenceDiagram
  autonumber
  actor Cust as Customer
  actor Mgr as Manager
  participant Ctrl as ContractWorkflowController
  participant Svc as ContractWorkflowService
  participant Store as MinioEvidenceObjectStore
  participant DB as PostgreSQL

  Cust->>Ctrl: POST /api/v1/contracts/requests (requestType = RECURRING, cadence, bound)
  Ctrl->>Svc: create(customerId, request)
  Svc->>DB: Validate exactly one recurrence bound (occurrenceCount xor recurrenceEndDate) and save ServiceRequest

  Mgr->>Ctrl: POST /api/v1/contracts/requests/{id}/quotes
  Ctrl->>Svc: issueQuote(managerId, requestId, quoteInput)
  Svc->>DB: Validate first occurrence window within requested range and save ServiceRequestQuote

  Cust->>Ctrl: POST /api/v1/contracts/requests/{id}/accept?versionNo=1
  Ctrl->>Svc: acceptQuote(customerId, requestId, versionNo)
  Svc->>Svc: materializeOccurrences(request, acceptedQuote) with month-end date anchoring
  Svc->>DB: Insert ServiceRequestOccurrence rows (1..N) and mark request ACCEPTED

  Mgr->>Ctrl: POST /api/v1/contracts/requests/{id}/signed-contract (MultipartFile)
  Ctrl->>Svc: uploadSignedContract(managerId, requestId, file)
  Svc->>Store: Store signed paper agreement in MinIO
  Svc->>DB: Record contract_object_key on parent ServiceRequest (CONTRACT_SIGNED)
```

#### 3.3.3 Event-Driven Notification Inbox and Read Status Sequence Diagram

```mermaid
%% title: FE-03 Event-Driven Notification Inbox and Read Status Sequence Diagram
sequenceDiagram
  autonumber
  actor Mgr as Manager or Customer
  actor User as Recipient User
  participant DomainSvc as Inspection / Maintenance Service
  participant Outbox as Spring Modulith Outbox (event_publication)
  participant Listener as Inspection / Maintenance NotificationListener
  participant NotifCtrl as NotificationController
  participant NotifSvc as NotificationService
  participant DB as PostgreSQL

  Mgr->>DomainSvc: Execute domain action (e.g., assign inspection, abort session, approve estimate)
  DomainSvc->>Outbox: Publish domain event within transaction
  Outbox->>Listener: Deliver event asynchronously to @ApplicationModuleListener
  Listener->>DB: Insert Notification (status = SENT) guarded by uq_notifications_deduplication_key

  User->>NotifCtrl: GET /api/v1/notifications & GET /api/v1/notifications/unread-count
  NotifCtrl->>NotifSvc: list(userId, page, pageSize, unreadOnly) & unreadCount(userId)
  NotifSvc->>DB: Query recipient-scoped notifications and unread count
  DB-->>User: Return NotificationPageResponse and unread count

  User->>NotifCtrl: PATCH /api/v1/notifications/{id}/read
  NotifCtrl->>NotifSvc: markAsRead(userId, notificationId)
  NotifSvc->>DB: Update Notification status SENT -> READ and set read_at timestamp
```

---

### 3.4 FE-04 Service Requests, Quotations, Agreements and Dispatch

This section presents the detailed design for `FE-04` (Service request creation, Order Chat negotiation, versioned VND quotations, signed paper contract upload, cross-organization partner Inspector and owned Drone dispatch, abort recovery dispatch, and Vietnam airspace evaluation).

#### 3.4.1 Class Diagram

```mermaid
%% title: FE-04 Service Request, Quotation, Signed Contract and Dispatch Class Diagram
classDiagram
  class ContractWorkflowController {
    +list() List~ServiceRequestResponse~
    +create(req) ServiceRequestResponse
    +postMessage(reqId, msg) ServiceRequestResponse
    +issueQuote(reqId, quoteReq) ServiceRequestResponse
    +acceptQuote(reqId, versionNo) ServiceRequestResponse
    +uploadSignedContract(reqId, file) ServiceRequestResponse
    +downloadSignedContract(reqId) InputStreamResource
    +assignOccurrence(reqId, occId, assignReq) ServiceRequestResponse
  }
  class ContractWorkflowService {
    +create(actorId, req) ServiceRequestResponse
    +issueQuote(actorId, reqId, quoteReq) ServiceRequestResponse
    +acceptQuote(actorId, reqId, versionNo) ServiceRequestResponse
    +uploadSignedContract(actorId, reqId, file) ServiceRequestResponse
    +assignOccurrence(actorId, reqId, occId, assignReq) ServiceRequestResponse
  }
  class Mf2InspectionAssignmentAdapter {
    +assign(orgId, assetId, inspectorId, droneId, startAt, endAt, actorId) UUID
  }
  class AirspaceAdvisoryService {
    +listZones() List~AirspaceZoneView~
    +evaluate(lat, lon, maxAltitudeMeters) AirspaceEvaluationResult
  }
  class ServiceRequest {
    -UUID id
    -UUID organizationId
    -UUID assetId
    -RequestType requestType
    -ServiceRequestStatus status
    -Integer acceptedQuoteVersion
    -String contractObjectKey
  }
  class ServiceRequestQuote {
    -UUID id
    -UUID requestId
    -int versionNo
    -UUID inspectorId
    -UUID droneId
    -BigDecimal pricePerOccurrenceVnd
  }
  class ServiceRequestOccurrence {
    -UUID id
    -UUID requestId
    -UUID inspectionId
    -OccurrenceStatus status
    -OccurrencePaymentStatus paymentStatus
    -Long payosOrderCode
    -String paymentMethod
  }
  ContractWorkflowController --> ContractWorkflowService
  ContractWorkflowService --> ServiceRequest
  ContractWorkflowService --> ServiceRequestQuote
  ContractWorkflowService --> ServiceRequestOccurrence
  ContractWorkflowService --> Mf2InspectionAssignmentAdapter
```

**Class Specifications**

| No | Class | Description |
| :---: | :--- | :--- |
| 01 | `ContractWorkflowController` & `ContractWorkflowService` | Manage customer inspection service requests, order chat messages, versioned VND quotations, quote acceptance, signed paper agreement uploads, and occurrence dispatch. |
| 02 | `Mf2InspectionAssignmentAdapter` & `PartnerRegistryService` | Validate Inspector pilot license status, drone ownership, and cross-organization schedule availability before creating a scheduled inspection mission. |
| 03 | `AirspaceController` & `AirspaceAdvisoryService` | Expose Vietnam No-Fly and Restricted airspace polygons and evaluate target coordinates and altitudes using Haversine distance checks. |
| 04 | `ServiceRequest`, `ServiceRequestQuote` & `ServiceRequestOccurrence` | Domain entities representing the customer request, each proposed VND quotation version, and the individual inspection occurrences generated upon quote acceptance. |

#### 3.4.2 Service Request, Order Chat and VND Quotation Sequence Diagram

```mermaid
%% title: FE-04 Service Request, Order Chat and VND Quotation Sequence Diagram
sequenceDiagram
  autonumber
  actor Cust as Customer
  actor Mgr as Manager
  participant Ctrl as ContractWorkflowController
  participant Svc as ContractWorkflowService
  participant Partner as PartnerRegistryService
  participant FinSvc as InspectionFinanceSettingsService
  participant DB as PostgreSQL

  Cust->>Ctrl: POST /api/v1/contracts/requests
  Ctrl->>Svc: create(customerId, request)
  Svc->>DB: Verify active Asset in Customer organization and save OPEN ServiceRequest

  Cust->>Ctrl: POST /api/v1/contracts/requests/{id}/messages
  Ctrl->>Svc: postMessage(customerId, requestId, body)
  Svc->>DB: Save ServiceRequestMessage

  Mgr->>Ctrl: POST /api/v1/contracts/requests/{id}/quotes
  Ctrl->>Svc: issueQuote(managerId, requestId, quoteInput)
  Svc->>Partner: isEligibleInspector(inspectorId, startAt) & isEligibleDrone(droneId, inspectorId)
  Svc->>FinSvc: requireConfiguredRates()
  Svc->>DB: Save immutable ServiceRequestQuote version (VND) and mark request QUOTED

  Cust->>Ctrl: POST /api/v1/contracts/requests/{id}/accept?versionNo=v
  Ctrl->>Svc: acceptQuote(customerId, requestId, versionNo)
  Svc->>DB: Verify versionNo is latest, materialize occurrences, and mark request ACCEPTED
```

#### 3.4.3 Signed Contract Upload, Occurrence Dispatch and Airspace Check Sequence Diagram

```mermaid
%% title: FE-04 Signed Contract Upload, Occurrence Dispatch and Airspace Check Sequence Diagram
sequenceDiagram
  autonumber
  actor Mgr as Manager
  participant Ctrl as ContractWorkflowController / AirspaceController
  participant Svc as ContractWorkflowService / AirspaceAdvisoryService
  participant AssignPort as Mf2InspectionAssignmentAdapter
  participant Store as MinioEvidenceObjectStore
  participant DB as PostgreSQL

  Mgr->>Ctrl: GET /api/v1/airspace/evaluate?latitude=...&longitude=...
  Ctrl->>Svc: evaluate(latitude, longitude, maxAltitudeMeters)
  Svc-->>Mgr: Return AirspaceEvaluationResult (CLEAR_ZONE, RESTRICTED_ZONE, or NO_FLY_ZONE)

  Mgr->>Ctrl: POST /api/v1/contracts/requests/{id}/signed-contract (PDF/DOCX/JPEG/PNG)
  Ctrl->>Svc: uploadSignedContract(managerId, requestId, file)
  Svc->>Store: Store agreement file in MinIO
  Svc->>DB: Record contract_object_key and transition request to CONTRACT_SIGNED

  Mgr->>Ctrl: POST /api/v1/contracts/requests/{id}/occurrences/{occId}/assign
  Ctrl->>Svc: assignOccurrence(managerId, requestId, occId, assignInput)
  Svc->>DB: Check hasScheduleConflict(inspectorId, droneId, startAt, endAt)
  Svc->>AssignPort: assign(orgId, assetId, inspectorId, droneId, startAt, endAt, managerId)
  AssignPort->>DB: Create SCHEDULED Inspection and publish InspectionAssignedEvent
  Svc->>DB: Link inspectionId on ServiceRequestOccurrence and mark request ASSIGNED
```

---

### 3.5 FE-05 Flight Permit and On-Site Field Sessions

This section presents the detailed design for `FE-05` (Aviation flight permit upload with pilot license validation, on-site field session execution, `SmartDroneHub` live telemetry, flight trace and MP4 video sync, session abort and Manager recovery dispatch, four-role operational dashboards, and Inspector Schedule Calendar).

#### 3.5.1 Class Diagram

```mermaid
%% title: FE-05 Flight Permit Gate and Field Inspection Execution Class Diagram
classDiagram
  class InspectionController {
    +uploadFlightPermit(inspId, file) InspectionResponse
    +reschedule(inspId, req) InspectionResponse
    +reassign(inspId, req) InspectionResponse
    +cancel(inspId, req) InspectionResponse
  }
  class InspectionListController {
    +listInspections(page, pageSize, status) PagedResponse
    +getInspection(inspId) InspectionDetailResponse
    +flightPermitContent(inspId) ResponseEntity
  }
  class InspectionFieldSessionController {
    +listSessions(inspId) List~FieldSessionResponse~
    +start(inspId, req) FieldSessionResponse
    +complete(inspId, sessId, req) FieldSessionResponse
    +abort(inspId, sessId, req) FieldSessionResponse
    +droneHubStatus(inspId) DroneHubStatusResponse
    +connectDroneHub(inspId, sessId, req) DroneHubStatusResponse
    +getFlightReport(inspId, sessId) DroneFlightReportResponse
    +syncFlightVideo(inspId, sessId) EvidenceResponse
  }
  class InspectionCreationService {
    +uploadFlightPermit(actorId, inspId, file) Inspection
    +reschedule(actorId, inspId, startAt, endAt) Inspection
    +reassign(actorId, inspId, inspectorId, droneId) Inspection
    +cancel(actorId, inspId, reason) Inspection
  }
  class InspectionFieldSessionService {
    +start(actorId, inspId, safetyNote) FieldSession
    +complete(actorId, inspId, sessId, notes) FieldSession
    +abort(actorId, inspId, sessId, reason) FieldSession
  }
  class InspectionDroneHubService {
    +status(actorId, inspId) DroneHubStatusResponse
    +connect(actorId, inspId, sessId, req) DroneHubStatusResponse
    +disconnect(actorId, inspId, sessId) DroneHubStatusResponse
    +getFlightReport(actorId, inspId, sessId) DroneFlightReportResponse
    +syncFlightVideo(actorId, inspId, sessId) EvidenceResponse
  }
  class Inspection {
    -UUID id
    -UUID organizationId
    -UUID assetId
    -UUID inspectorId
    -UUID droneId
    -InspectionStatus status
    -String flightPermitFileKey
    +hasFlightPermit() boolean
    +moveTo(nextStatus) void
    +reopenAfterSessionAbort() void
  }
  class FieldSession {
    -UUID id
    -UUID inspectionId
    -FieldSessionStatus status
    -Instant startedAt
    -Instant endedAt
    -String preFlightChecklistNote
    -String outcomeNotes
    -String abortReason
    -String telemetrySource
    -Integer flightDurationSeconds
    -BigDecimal distanceFlownMeters
    -String flightTraceJson
    -UUID flightVideoEvidenceId
    +start(startedAt) void
    +complete(endedAt, notes) void
    +abort(endedAt, reason) void
    +recordFlightReport(...) void
  }
  InspectionController --> InspectionCreationService
  InspectionFieldSessionController --> InspectionFieldSessionService
  InspectionFieldSessionController --> InspectionDroneHubService
  InspectionCreationService --> Inspection
  InspectionFieldSessionService --> Inspection
  InspectionFieldSessionService --> FieldSession
  InspectionDroneHubService --> FieldSession
  Inspection "1" *-- "1..*" FieldSession : executes
```

**Class Specifications**

| No | Class | Description |
| :---: | :--- | :--- |
| 01 | `InspectionController`, `InspectionListController` & `InspectionCreationService` | Handle mission flight permit uploads (checking assigned Inspector pilot license validity at upload time), scoped mission queries, flight permit streaming, and Manager recovery actions (`reschedule`, `reassign`, or `cancel`) when an on-site field session is aborted. |
| 02 | `InspectionFieldSessionController` & `InspectionFieldSessionService` | Govern on-site field session execution, enforcing that a session can start only when the inspection is `SCHEDULED` with `hasFlightPermit() == true`, and recording either normal completion (`FIELD_COMPLETED`) or session abort (`ABORTED` with mission reopen to `SCHEDULED`). |
| 03 | `InspectionDroneHubService` & `SmartDroneHubClient` | Connect an active field session to `SmartDroneHub`, stream live telemetry, persist post-flight report metrics and GPS flight traces (`flight_trace_json`) on `FieldSession`, and synchronize recorded mission MP4 videos into inspection `Evidence`. |
| 04 | `DashboardController` & `DashboardAnalyticsService` | Aggregate 5-role operational KPIs, mission queues, confirmed defect severity distributions, and inspection-service metrics only. |
| 05 | `Inspection` & `FieldSession` | Domain entities representing the 6-state inspection mission aggregate and the 4-state on-site flight session with persisted telemetry, GPS flight trace, and synced video reference (`V28`). |

#### 3.5.2 Flight Permit Gate, Field Session Execution and SmartDroneHub Sync Sequence Diagram

```mermaid
%% title: FE-05 Flight Permit Gate, Field Session Execution and SmartDroneHub Sync Sequence Diagram
sequenceDiagram
  autonumber
  actor Insp as Assigned Inspector
  participant Ctrl as InspectionController / InspectionFieldSessionController
  participant Svc as InspectionCreationService / InspectionFieldSessionService
  participant HubSvc as InspectionDroneHubService
  participant Hub as SmartDroneHubClient
  participant DB as PostgreSQL & MinIO

  Insp->>Ctrl: POST /api/v1/inspections/{id}/flight-permit (MultipartFile)
  Ctrl->>Svc: uploadFlightPermit(inspectorId, inspectionId, file)
  Svc->>DB: Verify Inspector pilot license is unexpired, store permit in MinIO, and save flight_permit_file_key

  Insp->>Ctrl: POST /api/v1/inspections/{id}/field-sessions (preFlightChecklistNote)
  Ctrl->>Svc: start(inspectorId, inspectionId, preFlightChecklistNote)
  Svc->>DB: Verify hasFlightPermit() == true, create IN_PROGRESS FieldSession, and mark Inspection IN_PROGRESS

  Insp->>Ctrl: POST /api/v1/inspections/{id}/field-sessions/{sessId}/drone-hub/connect
  Ctrl->>HubSvc: connect(inspectorId, inspectionId, sessId, request)
  HubSvc->>Hub: startMission(missionPayload)
  Insp->>Ctrl: GET /flight-report & POST /sync-video
  Ctrl->>HubSvc: getFlightReport(...) & syncFlightVideo(...)
  HubSvc->>Hub: Fetch telemetry metrics, GPS trace, and recorded MP4 video
  HubSvc->>DB: Persist flight_trace_json on field_sessions and MP4 Evidence in MinIO

  Insp->>Ctrl: POST /api/v1/inspections/{id}/field-sessions/{sessId}/completion (outcomeNotes)
  Ctrl->>Svc: complete(inspectorId, inspectionId, sessId, outcomeNotes)
  Svc->>DB: Transition FieldSession and Inspection to FIELD_COMPLETED
```

#### 3.5.3 Field Session Abort and Manager Recovery Dispatch Sequence Diagram

```mermaid
%% title: FE-05 Field Session Abort and Manager Recovery Dispatch Sequence Diagram
sequenceDiagram
  autonumber
  actor Insp as Assigned Inspector
  actor Mgr as Manager
  participant SessCtrl as InspectionFieldSessionController
  participant InspCtrl as InspectionController
  participant SessSvc as InspectionFieldSessionService
  participant CreateSvc as InspectionCreationService
  participant DB as PostgreSQL

  Insp->>SessCtrl: POST /api/v1/inspections/{id}/field-sessions/{sessId}/abort (abortReason)
  SessCtrl->>SessSvc: abort(inspectorId, inspectionId, sessId, abortReason)
  SessSvc->>DB: Mark FieldSession ABORTED, reopen Inspection to SCHEDULED, and publish FieldSessionAbortedEvent
  SessSvc-->>Mgr: Deliver in-app abort alert notification

  alt Reschedule Inspection Window
    Mgr->>InspCtrl: PUT /api/v1/inspections/{id}/schedule (plannedStartAt, plannedEndAt)
    InspCtrl->>CreateSvc: reschedule(managerId, inspectionId, startAt, endAt)
    CreateSvc->>DB: Check partner schedule conflicts and update planned window
  else Reassign Inspector and Owned Drone
    Mgr->>InspCtrl: PUT /api/v1/inspections/{id}/assignment (inspectorId, droneId)
    InspCtrl->>CreateSvc: reassign(managerId, inspectionId, inspectorId, droneId)
    CreateSvc->>DB: Validate pilot license, drone ownership, and schedule availability, then update assignment
  else Cancel Inspection Mission
    Mgr->>InspCtrl: POST /api/v1/inspections/{id}/cancellation (reason)
    InspCtrl->>CreateSvc: cancel(managerId, inspectionId, reason)
    CreateSvc->>DB: Transition Inspection to CANCELLED
  end
```

---

### 3.6 FE-06 Evidence, Findings, Reports and Payment

This section presents the detailed design for `FE-06` (Photograph and streaming MP4 video evidence intake, Ultralytics YOLO11 defect detection with Vision LLM fallback, findings baseline confirmation, 4-state inspection report authoring and direct Manager publication, on-demand A4 PDF rendering, Customer report acceptance, and PayOS VietQR / VNPay v2.1.0 online payment settlement).

#### 3.6.1 Class Diagram

```mermaid
%% title: FE-06 Evidence, AI Defect Detection, Inspection Report and Payment Class Diagram
classDiagram
  class EvidenceService {
    +upload(actorId, inspId, file) EvidenceResponse
    +listForInspection(actorId, inspId) EvidencePageResponse
    +openContent(actorId, inspId, evidId) EvidenceContent
    +retire(actorId, inspId, evidId) void
  }
  class FindingService {
    +analyzeEvidence(actorId, inspId, evidId, replace) List~FindingResponse~
    +analyzeVideo(actorId, inspId, evidId, req) VideoAnalysisResponse
    +createManual(actorId, inspId, req) FindingResponse
    +review(actorId, inspId, findingId, decision) FindingResponse
    +confirmFindings(actorId, inspId, ack) void
  }
  class PrimaryWithFallbackInference {
    +predict(imageBytes, contentType) List~DetectedBox~
  }
  class ReportService {
    +generateDraft(actorId, inspId) InspectionReportResponse
    +authorManualDraft(actorId, inspId, req) InspectionReportResponse
    +submitVersion(actorId, inspId, verId) InspectionReportResponse
    +generateAiSummary(actorId, inspId, locale) ReportAiSummaryResponse
    +reviewVersion(actorId, inspId, verId, approve, reason) InspectionReportResponse
    +downloadArtefact(actorId, inspId, verId, locale) DownloadedReport
  }
  class ContractWorkflowService {
    +customerAcceptReport(custId, reqId, occId, verId) ServiceRequestResponse
    +createOccurrencePayOSCheckout(custId, reqId, occId, req) PayOSCheckoutResponse
    +createOccurrenceVnPayCheckout(custId, reqId, occId, req, ip) VnPayCheckoutResponse
    +handlePayOSWebhook(payload) void
    +handleVnPayWebhook(params) VnPayIpnResponse
    +recordOccurrencePayout(mgrId, reqId, occId, req) ServiceRequestResponse
  }
  class Evidence {
    -UUID id
    -UUID inspectionId
    -String fileName
    -String contentType
    -String objectKey
    -BigDecimal latitude
    -BigDecimal longitude
    -boolean isDeleted
  }
  class Finding {
    -UUID id
    -UUID inspectionId
    -UUID evidenceId
    -String findingCode
    -String defectLabel
    -FindingSeverity severity
    -FindingStatus status
    -BigDecimal confidence
  }
  class InspectionReport {
    -UUID id
    -UUID inspectionId
    -int versionNo
    -ReportStatus status
    -UUID reviewerUserId
    -String returnReason
    -Instant submittedAt
    -Instant publishedAt
  }
  EvidenceService --> Evidence
  FindingService --> Finding
  FindingService --> PrimaryWithFallbackInference
  ReportService --> InspectionReport
  ContractWorkflowService --> InspectionReport
  Evidence "1" o-- "0..*" Finding : locates
```

**Class Specifications**

| No | Class | Description |
| :---: | :--- | :--- |
| 01 | `EvidenceService` | Uploads, validates, streams, and soft-retires field photographs (`10 MB`) and MP4 videos (`500 MB`) associated with an inspection session while extracting EXIF GPS coordinates and capture timestamps. |
| 02 | `FindingService` & `PrimaryWithFallbackInference` | Invoke Ultralytics YOLO11 (`YoloInferenceClient`) and Vision LLM fallback (`OpenAiCompatibleInferenceClient`) defect detection on photographs and video keyframes, manage manual and AI-suggested findings, and lock the confirmed findings baseline (`inspections.findings_confirmed_at`). |
| 03 | `ReportService`, `PdfReportRenderer` & `InspectionReport` | Compile and submit 4-state inspection reports (`SUBMITTED`, `RETURNED`, `PUBLISHED`, `SUPERSEDED`), synthesize AI executive summaries (`ReportDraftClient`), enforce independent Manager direct publication, and render on-demand A4 PDFs (`reports/<versionId>.pdf`). |
| 04 | `ContractWorkflowService`, `PayOSWebhookController` & `VnPayWebhookController` | Record Customer acceptance of a published report (`PAYMENT_DUE`), generate PayOS VietQR (`PayOSPaymentGateway`) and VNPay v2.1.0 (`VnPayPaymentGateway`) checkout links in VND, verify signed webhook callbacks, and settle customer payment (`PAID`) and partner payout (`ELIGIBLE`/`PAID`). |
| 05 | `Evidence` & `Finding` | Domain entities representing stored inspection media and AI-proposed (`PENDING`) or Inspector-confirmed (`CONFIRMED`) structural defects. |

#### 3.6.2 Photo/Video Evidence Intake, YOLO11 Detection and Findings Confirmation Sequence Diagram

```mermaid
%% title: FE-06 Photo/Video Evidence Intake, YOLO11 Detection and Findings Confirmation Sequence Diagram
sequenceDiagram
  autonumber
  actor Insp as Assigned Inspector
  participant Ctrl as InspectionController
  participant EvidSvc as EvidenceService
  participant FindSvc as FindingService
  participant AI as PrimaryWithFallbackInference
  participant DB as PostgreSQL & MinIO

  Insp->>Ctrl: POST /api/v1/inspections/{id}/evidence (photo or video/mp4)
  Ctrl->>EvidSvc: upload(inspectorId, inspectionId, file)
  EvidSvc->>DB: Validate MIME/size, extract EXIF GPS, store object in MinIO, and save Evidence

  Insp->>Ctrl: POST /api/v1/inspections/{id}/evidence/{evidId}/analyze (or /analyze-video)
  Ctrl->>FindSvc: analyzeEvidence(inspectorId, inspectionId, evidId, replace)
  FindSvc->>AI: predict(imageBytes, contentType)
  AI-->>FindSvc: Return YOLO11 bounding boxes (or Vision LLM fallback boxes if empty/offline)
  FindSvc->>DB: Save PENDING Finding rows
  FindSvc-->>Insp: Return candidate Findings with bounding boxes and confidence scores

  Insp->>Ctrl: POST /findings/{findingId}/confirmation & PUT /findings/{findingId}
  Ctrl->>FindSvc: review(inspectorId, inspectionId, findingId, decision)
  FindSvc->>DB: Update Finding status to CONFIRMED (or soft-delete rejected candidate)

  Insp->>Ctrl: POST /api/v1/inspections/{id}/findings/confirm
  Ctrl->>FindSvc: confirmFindings(inspectorId, inspectionId, acknowledgeNoFindings)
  FindSvc->>DB: Verify zero PENDING findings remain and set inspections.findings_confirmed_at
```

#### 3.6.3 Report Submission, Manager Direct Publication and On-Demand PDF Export Sequence Diagram

```mermaid
%% title: FE-06 Report Submission, Manager Direct Publication and On-Demand PDF Export Sequence Diagram
sequenceDiagram
  autonumber
  actor Insp as Assigned Inspector
  actor Mgr as Independent Manager
  actor Caller as Authorized User
  participant Ctrl as InspectionController
  participant RepSvc as ReportService
  participant Pdf as PdfReportRenderer
  participant DB as PostgreSQL & MinIO

  Insp->>Ctrl: POST /api/v1/inspections/{id}/report/ai-summary & POST /report/draft
  Ctrl->>RepSvc: generateAiSummary(...) & generateDraft(inspectorId, inspectionId)
  RepSvc->>DB: Create InspectionReport (status = SUBMITTED) and move Inspection to UNDER_REVIEW

  alt Manager Returns Report with Feedback
    Mgr->>Ctrl: POST /api/v1/inspections/{id}/report/versions/{verId}/review (approve = false, reason)
    Ctrl->>RepSvc: reviewVersion(managerId, inspectionId, verId, false, reason)
    RepSvc->>DB: Mark InspectionReport RETURNED and revert Inspection to FIELD_COMPLETED
  else Manager Approves and Directly Publishes Report
    Mgr->>Ctrl: POST /api/v1/inspections/{id}/report/versions/{verId}/review (approve = true)
    Ctrl->>RepSvc: reviewVersion(managerId, inspectionId, verId, true, null)
    RepSvc->>DB: Mark prior published version SUPERSEDED, set current version PUBLISHED, and Inspection COMPLETED
  end

  Caller->>Ctrl: GET /api/v1/inspections/{id}/report/versions/{verId}/document
  Ctrl->>RepSvc: downloadArtefact(actorId, inspectionId, verId, locale)
  RepSvc->>Pdf: Render A4 PDF on demand if not cached, store at reports/{verId}.pdf in MinIO, and stream bytes
```

#### 3.6.4 Customer Report Acceptance and PayOS / VNPay Online Payment Sequence Diagram

```mermaid
%% title: FE-06 Customer Report Acceptance and PayOS / VNPay Online Payment Sequence Diagram
sequenceDiagram
  autonumber
  actor Cust as Customer
  participant Ctrl as InspectionController / ContractWorkflowController
  participant Webhooks as PayOSWebhookController / VnPayWebhookController
  participant ContractSvc as ContractWorkflowService
  participant PayGW as PayOSPaymentGateway / VnPayPaymentGateway
  participant DB as PostgreSQL

  Cust->>Ctrl: POST /api/v1/inspections/{id}/report/versions/{verId}/accept
  Ctrl->>ContractSvc: customerAcceptReport(customerId, requestId, occurrenceId, versionId)
  ContractSvc->>DB: Verify report is PUBLISHED and transition occurrence paymentStatus to PAYMENT_DUE

  alt PayOS VietQR Checkout
    Cust->>Ctrl: POST /api/v1/contracts/requests/{reqId}/occurrences/{occId}/payos/checkout
    Ctrl->>ContractSvc: createOccurrencePayOSCheckout(customerId, reqId, occId, req)
    ContractSvc->>PayGW: createPaymentLink(orderCode, amountVnd, description)
    PayGW-->>Cust: Return VietQR checkoutUrl and QR payload
    PayGW->>Webhooks: POST /api/v1/webhooks/payos (HMAC-SHA256 signed payload)
    Webhooks->>ContractSvc: handlePayOSWebhook(payload)
  else VNPay v2.1.0 Checkout
    Cust->>Ctrl: POST /api/v1/contracts/requests/{reqId}/occurrences/{occId}/vnpay/checkout
    Ctrl->>ContractSvc: createOccurrenceVnPayCheckout(customerId, reqId, occId, req, clientIp)
    ContractSvc->>PayGW: createPaymentUrl(txnRef, amountVnd, clientIp)
    PayGW-->>Cust: Return signed VNPay v2.1.0 paymentUrl
    PayGW->>Webhooks: GET /api/v1/webhooks/vnpay/ipn (HMAC-SHA512 signed query params)
    Webhooks->>ContractSvc: handleVnPayWebhook(params)
  end

  ContractSvc->>DB: Transition occurrence paymentStatus to PAID and partner payoutStatus to ELIGIBLE/PAID
```

---

---

### 3.7 Retired Maintenance Scope

Maintenance work-order, repair, maintenance-specific re-inspection, and cost-closeout features are not part of the application. Existing database tables and records for those features are retained unchanged for data preservation; they are not exposed through application workflows. Inspection re-inspection functionality, where required as part of an inspection process, remains within FE-05/FE-06 only where specified by those requirements.
