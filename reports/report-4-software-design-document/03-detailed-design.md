---
title: "Report 4 - Detailed Design"
document_type: report4-sdd-section
weight: 35
source: "report4-software-design-document.docx"
---

## 3. Detailed Design
### 3.1 MF1 — FE-01 Registration, Sign-in and Account Access

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

### 3.2 MF1 — FE-02 Partner Inspector and Drone Registration

This section presents the detailed design for `FE-02`: the public partner Inspector application with licence scan, platform review and account provisioning, the pilot-licence profile and flight-log records, and Inspector-owned drone registration against the administrator-configurable document set with platform approval.

#### 3.2.1 Class Diagram

```mermaid
%% title: FE-02 Partner Inspector Admission and Owned Drone Registration Class Diagram
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
  class InspectorApplicationController {
    +submit(req) ApiResponse
    +uploadLicenseScan(file) UploadedKeyResponse
    +listPending() List~InspectorApplicationResponse~
    +listApprovedAwaitingContract() List~InspectorApplicationResponse~
    +approve(id, req) UserResponse
    +reject(id, req) ApiResponse
    +uploadSignedContract(id, file) InspectorApplicationResponse
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
  class InspectorApplication {
    -UUID id
    -String email
    -String pilotLicenseNumber
    -String pilotLicenseClass
    -String status
    -UUID approvedUserId
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
  PlatformUserController --> InspectorProfile
  InspectorProfileController --> InspectorProfile
  InspectorApplicationController --> InspectorApplication
  InspectorApplication --> InspectorProfile
  DroneRegistrationApplicationController --> DroneRegistrationApplication
  DroneRegistrationApplication --> Drone
```

**Class Specifications**

| No | Class | Description |
| :---: | :--- | :--- |
| 01 | `PlatformUserController` & `InspectorProfileController` | Allow platform administrators and managers to provision `INSPECTOR` accounts, maintain pilot license credentials in `inspector_profiles`, upload license scans, and record flight logs in `inspector_flight_logs`. |
| 02 | `InspectorApplicationController` & `InspectorApplicationService` | Accept the public partner Inspector application and licence scan without authentication, expose the pending and approved-awaiting-contract review queues to `MANAGER` and `ADMIN`, record approval or rejection with reasons, and on approval provision the `INSPECTOR` account and its `InspectorProfile`. Record the signed partner contract after approval. |
| 03 | `DroneRegistrationApplicationController` & `DroneRegistrationApplicationService` | Handle Inspector-owned drone registration submissions with three required documents (`REGISTRATION`, `OWNERSHIP`, and `INSPECTION`) and platform review decisions. |
| 04 | `InspectorApplication`, `InspectorProfile` & `Drone` | Domain entities representing a pending partner application, an Inspector's licence and onboarding state, and an approved Inspector-owned drone. |

#### 3.2.2 Partner Inspector Application, Review and Account Provisioning Sequence Diagram

```mermaid
%% title: FE-02 Partner Inspector Application, Review and Account Provisioning Sequence Diagram
sequenceDiagram
  autonumber
  actor Public as Prospective Inspector
  actor Reviewer as Manager or Admin
  actor Insp as Inspector
  participant AppCtrl as InspectorApplicationController
  participant PlatCtrl as PlatformUserController / InspectorProfileController
  participant UserSvc as InspectorApplicationService / AdminUserService / InspectorProfileService
  participant Events as Spring Modulith event_publication
  participant DB as PostgreSQL & MinIO

  Public->>AppCtrl: POST /api/v1/inspector-applications/license-scan (multipart)
  AppCtrl->>UserSvc: storeLicenseScan(file)
  UserSvc->>DB: Write scan to MinIO and return object key
  Public->>AppCtrl: POST /api/v1/inspector-applications (identity, licence, scan key)
  AppCtrl->>UserSvc: submit(request)
  UserSvc->>DB: Verify normalized email has no account and no open application
  UserSvc->>DB: Insert inspector_applications row with status PENDING_REVIEW
  UserSvc->>Events: Publish InspectorApplicationSubmittedEvent
  AppCtrl-->>Public: Return 201 Created (no account exists yet)

  Reviewer->>AppCtrl: GET /api/v1/inspector-applications
  AppCtrl->>UserSvc: listPending()
  UserSvc->>DB: Query pending applications
  Reviewer->>AppCtrl: GET /api/v1/inspector-applications/{id}/license-scan
  AppCtrl->>UserSvc: readLicenseScan(id)
  UserSvc->>DB: Stream licence scan through a scoped media ticket

  alt Approved
    Reviewer->>AppCtrl: POST /api/v1/inspector-applications/{id}/approve
    AppCtrl->>UserSvc: approve(id, request)
    UserSvc->>DB: Lock application, insert users row with role INSPECTOR and insert inspector_profiles
    UserSvc->>DB: Link approved_user_id and set notification state
    AppCtrl-->>Reviewer: Return provisioned UserResponse
  else Rejected
    Reviewer->>AppCtrl: POST /api/v1/inspector-applications/{id}/reject (rejectionReason)
    AppCtrl->>UserSvc: reject(id, request)
    UserSvc->>DB: Set status REJECTED with reason and store review attribution
    AppCtrl-->>Reviewer: Return ApiResponse with no content
  end

  Reviewer->>AppCtrl: POST /api/v1/inspector-applications/{id}/signed-contract (multipart)
  AppCtrl->>UserSvc: uploadSignedContract(id, file)
  UserSvc->>DB: Store partner contract and SHA-256 in MinIO and inspector_applications
  Insp->>PlatCtrl: PUT /api/v1/platform/inspectors/{id} and POST /license-scan
  PlatCtrl->>UserSvc: updateProfile(userId, req) and uploadLicenseScan(userId, file)
  UserSvc->>DB: Update inspector_profiles and store the renewed licence scan
  Insp->>PlatCtrl: GET /api/v1/platform/inspectors/{id}/flight-logs
  PlatCtrl->>UserSvc: listFlightLogs(userId)
  UserSvc->>DB: Query inspector_flight_logs
```

### 3.3 MF2 — FE-03 Buildings, Airspace Screening and Notifications

This section presents the detailed design for `FE-03`: the customer building catalogue with category-scoped inspection checkpoints and SHA-256 reference documents under the No-Fly Zone airspace gate, the platform review of restrictive-airspace registrations, recurring service request occurrence materialization with month-end anchoring, and deduplicated in-app notifications delivered through the Spring Modulith transactional event outbox.

#### 3.3.1 Class Diagram

```mermaid
%% title: FE-03 Building Catalogue, Occurrences and Notification Inbox Class Diagram
classDiagram
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
  class AirspaceReviewController {
    +listPending() List~ProspectiveCustomerRegistrationResponse~
    +approve(registrationId) ProspectiveCustomerRegistrationResponse
    +reject(registrationId, req) ProspectiveCustomerRegistrationResponse
  }
  class Asset {
    -UUID id
    -UUID ownerCustomerId
    -String assetCode
    -String name
    -BigDecimal latitude
    -BigDecimal longitude
    -AssetStatus status
  }
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
    +onFieldSessionAborted(event) void
    +onInspectionDeclined(event) void
    +onInspectionOverdue(event) void
    +onFieldSessionHung(event) void
    +onFieldSessionForceAborted(event) void
    +onInspectionRescheduled(event) void
    +onInspectionAssignmentRevoked(event) void
    +onFlightPermitSubmitted(event) void
    +onFlightPermitReviewed(event) void
  }
  class InspectorApplicationNotificationListener {
    +onApplicationSubmitted(event) void
  }
  class PilotLicenseExpiryCheckService {
    +checkExpiringLicenses() void
  }
  class Notification {
    -UUID id
    -UUID recipientUserId
    -String eventType
    -String title
    -NotificationStatus status
    -String deduplicationKey
  }
  AssetController --> Asset
  AssetDocumentController --> Asset
  ContractWorkflowService --> ServiceRequestOccurrence
  NotificationController --> NotificationService
  InspectionNotificationListener --> Notification
  InspectorApplicationNotificationListener --> Notification
  NotificationService --> Notification
```

**Class Specifications**

| No | Class | Description |
| :---: | :--- | :--- |
| 01 | `AssetController`, `AssetDocumentController` & `AirspaceReviewController` | Manage customer buildings, category-scoped inspection checkpoints (`inspection_items`), and SHA-256 engineering reference documents in MinIO, blocking building creation inside prohibited No-Fly Zones, and let `ADMIN` or `MANAGER` review pending restrictive-airspace customer registrations with a mandatory rejection reason. |
| 02 | `ContractWorkflowService` & `ServiceRequestOccurrence` | Materialize count-bound or end-date-bound `ServiceRequestOccurrence` rows with month-end anchoring when a Customer accepts a recurring quotation and the signed contract is recorded. |
| 03 | `NotificationController` & `NotificationService` | Provide the role- and organization-scoped in-app notification inbox, unread notification counter, and idempotent `SENT -> READ` updates for signed-in users. |
| 04 | `InspectionNotificationListener`, `InspectorApplicationNotificationListener` & `PaymentSettlementNotificationListener` | Consume transactional Spring Modulith domain events and persist deduplicated notifications. The inspection listener handles `InspectionAssignedEvent`, `InspectionDeclinedEvent`, `InspectionOverdueEvent`, `InspectionRescheduledEvent`, `InspectionAssignmentRevokedEvent`, `FieldSessionAbortedEvent`, `FieldSessionHungEvent`, `FieldSessionForceAbortedEvent`, `FlightPermitSubmittedEvent`, `FlightPermitReviewedEvent`, `ReportSubmittedEvent`, `ReportReturnedEvent`, and `ReportPublishedEvent`; the application listener handles `InspectorApplicationSubmittedEvent`; the payment listener handles `PaymentSettledEvent`. `PilotLicenseExpiryCheckService` runs the scheduled licence-expiry sweep rather than consuming an event. |
| 05 | `Asset` & `Notification` | Domain entities representing a customer building under the airspace gate and an in-app user notification protected by `uq_notifications_deduplication_key`. |

#### 3.3.2 Building Asset and Reference Document Registration Sequence Diagram

```mermaid
%% title: FE-03 Building Asset and Reference Document Registration Sequence Diagram
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

#### 3.3.3 Recurring Service Request Occurrence Materialization Sequence Diagram

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

#### 3.3.4 Event-Driven Notification Inbox and Read Status Sequence Diagram

```mermaid
%% title: FE-03 Event-Driven Notification Inbox and Read Status Sequence Diagram
sequenceDiagram
  autonumber
  actor Mgr as Manager or Customer
  actor User as Recipient User
  participant DomainSvc as Inspections / Contracts / Users Service
  participant Outbox as Spring Modulith Outbox (event_publication)
  participant Listener as Inspection / Inspector Application NotificationListener
  participant NotifCtrl as NotificationController
  participant NotifSvc as NotificationService
  participant DB as PostgreSQL

  Mgr->>DomainSvc: Execute domain action (e.g., assign an inspection, abort a session, submit an application)
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

### 3.4 MF2 — FE-04 Service Requests, VND Quotations, Agreements and Dispatch

This section presents the detailed design for `FE-04` (request-level single-Manager ownership, serialized Manager self-claim, ADMIN-only audited assignment correction, assignment-scoped Manager details and commercial workflows, Customer-only assigned-Manager contact projection, three-dot action menu and overview, Service Request Messages inbox, single active VND quotation, signed paper contract upload, cross-organization partner Inspector and owned Drone dispatch, abort recovery dispatch, and Vietnam airspace evaluation).

#### 3.4.1 Class Diagram

```mermaid
%% title: FE-04 Service Request, Quotation, Signed Contract and Dispatch Class Diagram
classDiagram
  class ContractWorkflowController {
    +list(actorId) List~ServiceRequestResponse~
    +claimRequest(reqId) ServiceRequestResponse
    +reassignRequest(reqId, managerId) ServiceRequestResponse
    +unassignRequest(reqId) ServiceRequestResponse
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
    -UUID assignedManagerId
    -Instant managerAssignedAt
    -UUID managerAssignedByUserId
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
| 01 | `ContractWorkflowController` & `ContractWorkflowService` | Manage role-scoped service requests: Managers claim unassigned rows under a pessimistic request lock, and only the assigned Manager receives detailed conversation/commercial access. ADMIN uses an assignment-only registry to assign, reassign, or unassign with audit events and cannot act as a Manager. The owning Customer alone receives the assigned active Manager contact. The Customer/Manager UI provides a three-dot menu, structured overview, request progress navigation, and left-nav Messages inbox. |
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

  Mgr->>Ctrl: POST /api/v1/contracts/requests/{id}/claim
  Ctrl->>Svc: claimRequest(managerId, requestId)
  Svc->>DB: Lock request row and assign only if no current Manager

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

### 3.5 MF3 — FE-05 Flight Permit and On-site Field Sessions

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

### 3.6 MF3 — FE-06 Evidence Intake and Human-Reviewed Defect Detection

This section presents the detailed design for `FE-06`: photograph intake with EXIF extraction and bounded normalization, resumable chunked MP4 upload with asynchronous FFmpeg transcoding and ticketed Range playback, YOLO11 defect detection with an OpenAI-compatible vision fallback, the human-reviewed findings baseline that fixes which defects become official, and tenant-isolated DroneKnowledgeAI recommendations that ground each finding in historical cases and engineering standards.

#### 3.6.1 Class Diagram

```mermaid
%% title: FE-06 Evidence Intake and Human-Reviewed Defect Detection Class Diagram
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
  class HistoricalCaseService {
    +recommendForFinding(actorId, inspId, findingId, limit) KnowledgeRecommendationResponse
    +recommendForInspection(actorId, inspId, limit) KnowledgeRecommendationResponse
    +indexPublishedFindings(inspId) void
    +findKnowledgeReferences(inspId) List~KnowledgeReferenceSummary~
  }
  class HistoricalCaseAdvisorPort {
    <<interface>>
    +embed(text) Optional
  }
  class DroneKnowledgeClient {
    +embed(text) Optional
  }
  class KnowledgeRecommendationResponse {
    +String retrievalMode
    +List~CaseMatch~ cases
    +List~GuidelineMatch~ guidelines
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
  EvidenceService --> Evidence
  FindingService --> Finding
  FindingService --> PrimaryWithFallbackInference
  FindingService --> HistoricalCaseService : advisory recommendations
  HistoricalCaseService --> HistoricalCaseAdvisorPort
  DroneKnowledgeClient ..|> HistoricalCaseAdvisorPort
  HistoricalCaseService --> KnowledgeRecommendationResponse
  Evidence "1" o-- "0..*" Finding : locates
```

**Class Specifications**

| No | Class | Description |
| :---: | :--- | :--- |
| 01 | `EvidenceService` & `ImageNormalizer` | Extract EXIF GPS/time/orientation prior to decoding, normalize oversized (`> 2048 px`) or rotated photographs, generate `480 px` JPEG thumbnails (`?variant=thumb`), serve authenticated object reads (`HEAD`, `200`, `206` Partial Content, `416`), retry failed video processing, and soft-retire captures. |
| 02 | `EvidenceUploadSessionService` | Coordinates resumable multipart MP4 uploads up to `2 GB` (`2 GiB`) using bounded `10 MiB` chunks (`OPEN -> COMPLETING -> COMPLETED`/`FAILED`/`CANCELLED`/`EXPIRED`) through MinIO S3 multipart streaming without full-video JVM buffering, and cleans up expired/aborted sessions. |
| 03 | `VideoProcessingWorker`, `FfmpegVideoTranscoder` & `MediaTicketService` | Poll durable DB-backed `PENDING` video jobs, run argument-array FFmpeg transcoding (`<= 1080p` H.264 `+faststart` MP4 + `480 px` poster) with `raw_object_key` retained until verification or retryable failure, and mint short-lived HMAC tickets (`POST .../media-ticket` -> `GET/HEAD .../stream?ticket=...`) for native `<video>` Range playback. |
| 04 | `FindingService` & `PrimaryWithFallbackInference` | Invoke Ultralytics YOLO11 (`YoloInferenceClient`) and Vision LLM fallback (`OpenAiCompatibleInferenceClient`) defect detection on photographs and video keyframes, manage manual and AI-suggested findings, and lock the confirmed findings baseline (`inspections.findings_confirmed_at`). |
| 05 | `Evidence`, `EvidenceUploadSession` & `Finding` | Domain entities representing normalized/processed inspection media, resumable upload sessions, and AI-proposed (`PENDING`) or Inspector-confirmed (`CONFIRMED`) structural defects. |
| 06 | `HistoricalCaseService` (`inspections.service`) | Tenant-isolated advisory retrieval and AI note drafting in `inspections`. `recommendForFinding(actorId, inspectionId, findingId, limit)` and `recommendForInspection(actorId, inspectionId, limit)` first call `EvidenceService.requireInspectionInScope`, then embed the finding description and query `inspection_knowledge_chunks`/`historical_finding_cases`. `draftFindingNote(command)` combines matched cases/guidelines and optional evidence image context (`EvidenceService.readAdvisoryImage`) via `HistoricalCaseAdvisorPort` to return an editable technical note (`DraftFindingNoteResponse`) in the requested locale (`AI_VISION_RAG`, `PGVECTOR_RAG`, or deterministic `HYBRID_MATCH`). `indexPublishedFindings(inspectionId)` publishes confirmed findings with re-inspection `resolution_status` when a report is published, `backfillMissingEmbeddings()` fills null vectors on `ApplicationReadyEvent`, and `findKnowledgeReferences(inspectionId)` supplies compact references to the AI summary. |
| 07 | `HistoricalCaseAdvisorPort` (`inspections.spi`) & `DroneKnowledgeClient` (`infrastructure.ai`) | The outbound advisor port owned by `inspections` and its HTTP/1.1 adapter. `embed(text)` calls `POST /v1/embeddings` on `app.knowledge-ai.embedding-base-url` (default `http://ai-inference:8000`, serving local `fastembed` `paraphrase-multilingual-MiniLM-L12-v2` 384-dimensional vectors), returning empty on timeout, authentication failure or malformed response. `draftNote(...)` calls `/v1/chat/completions` for optional RAG + image narrative drafting. Retrieval scope is `(organization_id = actor org OR is_anonymized_benchmark = TRUE) AND (source_inspection_id IS NULL OR source_inspection_id <> current inspection)`, so no cross-organization PII leaks. |
| 08 | `KnowledgeRecommendationResponse` & `DraftFindingNoteResponse` | Advisory DTOs exposing retrieved cases/guidelines and drafted finding notes (`POST /api/v1/inspections/{inspectionId}/findings/{findingId}/draft-note`). The Web `DraftNoteAction` (`Draft note with AI`, collapsed `References`) and batch `Draft all notes (N)` toolbar button replace the inline `Similar Cases & Guide` strip (`KnowledgeRecommendationPanel`), writing drafted text only into the editable note field without auto-confirming. |

#### 3.6.2 Photo/Video Evidence Intake, YOLO11 Detection and Findings Confirmation Sequence Diagram

```mermaid
%% title: FE-06 Photo and Video Evidence Intake, YOLO11 Detection and Findings Confirmation Sequence Diagram
sequenceDiagram
  autonumber
  actor Insp as Assigned Inspector
  participant Ctrl as InspectionController
  participant EvidSvc as EvidenceService
  participant FindSvc as FindingService
  participant AI as PrimaryWithFallbackInference
  participant HistSvc as HistoricalCaseService
  participant Advisor as HistoricalCaseAdvisorPort
  participant DB as PostgreSQL & MinIO

  Insp->>Ctrl: POST /api/v1/inspections/{id}/evidence (photo <= 10 MB or compatibility video <= 20 MiB)
  Ctrl->>EvidSvc: upload(inspectorId, inspectionId, file)
  EvidSvc->>DB: Extract EXIF first, normalize >2048 px / rotated image, create 480 px thumb, store in MinIO, save Evidence

  Insp->>Ctrl: POST /evidence/uploads -> PUT .../parts/{n} (10 MiB chunks <= 2 GB) -> POST .../complete
  Ctrl->>EvidSvc: EvidenceUploadSessionService + VideoProcessingWorker (FFmpeg <=1080p faststart + poster, raw deleted only when verified READY)
  EvidSvc->>DB: Commit Evidence rendition keys & telemetry, or retain raw as retryable FAILED

  Insp->>Ctrl: POST .../evidence/{evidId}/media-ticket -> GET/HEAD .../stream?ticket=... (Range)
  Ctrl->>EvidSvc: Validate short-lived HMAC ticket & stream HTTP 206 Partial Content from MinIO

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

  Insp->>Ctrl: GET /api/v1/inspections/{id}/findings/{findingId}/recommendations?limit=3 (or POST .../draft-note)
  Ctrl->>HistSvc: recommendForFinding / draftFindingNote(actorId, inspectionId, findingId, ...)
  HistSvc->>DB: requireInspectionInScope(actorId, inspectionId) and load the finding
  HistSvc->>Advisor: embed(findingDescription)
  Advisor-->>HistSvc: 384-dim vector from local FastEmbed /v1/embeddings or empty when unavailable
  alt Embedding available
    HistSvc->>DB: pgvector cosine query (PGVECTOR_RAG) filtered by tenant scope
  else Embedding unavailable
    HistSvc->>DB: deterministic HYBRID_MATCH over category and defect label
  end
  HistSvc-->>Insp: KnowledgeRecommendationResponse / DraftFindingNoteResponse (advisory note in editable field)
  Note over Insp,DB: Web DraftNoteAction (Draft note with AI + collapsed References) & batch Draft all notes pop directly into edit mode
```

### 3.7 MF4 — FE-07 Inspection Report Preparation, Review and Publication

This section presents the detailed design for `FE-07`: the four-state inspection report lifecycle
(`SUBMITTED`, `RETURNED`, `PUBLISHED`, `SUPERSEDED`), report content compiled from the confirmed
findings and the inspected checkpoints, single-shot advisory narrative drafting enriched with
source-backed DroneKnowledgeAI references, independent Manager review of a report the reviewer did
not author, publication with automatic indexing of confirmed findings, and on-demand A4 PDF
rendering of the published version.

#### 3.7.1 Class Diagram

```mermaid
%% title: FE-07 Inspection Report Preparation, Review and Publication Class Diagram
classDiagram
  class InspectionController {
    +generateAiSummary(inspId, locale) ReportAiSummaryResponse
    +generateDraft(inspId) InspectionReportResponse
    +submitVersion(inspId, verId) InspectionReportResponse
    +reviewVersion(inspId, verId, req) ReportPublishedResponse
    +withdrawVersion(inspId, verId, req) InspectionReportResponse
    +downloadArtefact(inspId, verId, locale) ResponseEntity
  }
  class ReportService {
    +generateDraft(actorId, inspId) InspectionReportResponse
    +authorManualDraft(actorId, inspId, req) InspectionReportResponse
    +verifyVersion(actorId, inspId, verId) InspectionReportResponse
    +submitVersion(actorId, inspId, verId) InspectionReportResponse
    +reviewVersion(actorId, inspId, verId, approve, reason) ReportPublishedResponse
    +requestCustomerClarification(actorId, inspId, verId, req) ReportPublishedResponse
    +withdrawVersion(actorId, inspId, verId, req) InspectionReportResponse
    +listVersions(actorId, inspId) List~InspectionReportResponse~
    +preview(actorId, inspId, verId) ResponseEntity
    +downloadArtefact(actorId, inspId, verId, locale) ResponseEntity
  }
  class ReportDraftClient {
    +draft(narrativeRequest) ReportNarrative
  }
  class HistoricalCaseService {
    +findKnowledgeReferences(inspId) List~KnowledgeReferenceSummary~
    +indexPublishedFindings(inspId) void
    +recommendForInspection(actorId, inspId, limit) KnowledgeRecommendationResponse
  }
  class ReportAiSummaryResponse {
    +String executiveSummary
    +List~KnowledgeReferenceSummary~ knowledgeReferences
  }
  class KnowledgeReferenceSummary {
    +String kind
    +String codeOrLabel
    +String summary
    +Double similarity
  }
  class PdfReportRenderer {
    +render(context, locale) byte[]
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
  InspectionController --> ReportService
  InspectionController --> HistoricalCaseService : knowledge-recommendations
  ReportService --> InspectionReport
  ReportService --> ReportDraftClient
  ReportService --> HistoricalCaseService : knowledge references
  ReportService --> ReportAiSummaryResponse
  ReportAiSummaryResponse o-- KnowledgeReferenceSummary
  ReportService --> PdfReportRenderer
```

**Class Specifications**

| No | Class | Description |
| :---: | :--- | :--- |
| 01 | `InspectionController` & `ReportService` | Compile report content from the confirmed findings baseline and the inspected checkpoints, accept an authored or AI-drafted version, verify it, submit it for review, and expose the version history to authorized readers. |
| 02 | `ReportDraftClient` | Produce a single-shot advisory executive summary through the configured OpenAI-compatible endpoint. The narrative request is not itself retrieval-augmented and the rendered report falls back to the deterministic template when the model is unavailable; however `ReportService` now supplies source-backed reference strings from `HistoricalCaseService` so the summary is grounded in indexed standards and historical cases. |
| 03 | `ReportService` (review path) | Enforce independent review: a `MANAGER` or `ADMIN` who is not the author may publish the submitted version, returning the lifecycle to `FIELD_COMPLETED` on rejection with a recorded reason, or superseding an earlier published version on approval. |
| 04 | `PdfReportRenderer` | Render the published version on demand as an A4 PDF from normalized ready image bytes, skipping video binaries, caching the artefact at `reports/<versionId>.pdf` in MinIO, and streaming it to the caller. |
| 05 | `InspectionReport` | Domain entity holding the version number, lifecycle status, reviewer identity, return reason, and submission and publication timestamps. |
| 06 | `HistoricalCaseService` (report path) | `findKnowledgeReferences(inspectionId)` returns compact source-backed references from `inspection_knowledge_chunks` and tenant-visible `historical_finding_cases`; `indexPublishedFindings(inspectionId)` copies the published report's confirmed findings into `historical_finding_cases` with `is_anonymized_benchmark = FALSE`. `recommendForInspection(actorId, inspectionId, limit)` backs `GET /api/v1/inspections/{inspectionId}/knowledge-recommendations?limit=4`, which the Web report summary renders as a `Matched Cases & Standards` footer. |
| 07 | `ReportAiSummaryResponse` & `KnowledgeReferenceSummary` | `generateAiSummary` returns the advisory narrative plus `knowledgeReferences` (`kind`, `codeOrLabel`, `summary`, normalized `similarity`); the list is empty when DroneKnowledgeAI is unavailable, so the UI degrades cleanly. References are advisory only and never alter the confirmed findings or publication decision. |
| 08 | Web `ReportAiSummaryCard` & `EvidenceCaptureGroup` (`DraftNoteAction`) | `src/features/reports/ReportAiSummaryCard` renders the `Matched Cases & Standards` footer from `knowledgeReferences`, while `DraftNoteAction` inside `src/features/inspections/components/EvidenceCaptureGroup.tsx` renders `Draft note with AI` with collapsed `References` inside finding cards alongside the toolbar `Draft all notes (N)` action and confirmation status filter chips. |

#### 3.7.2 Report Submission, Manager Direct Publication and On-Demand PDF Export Sequence Diagram

```mermaid
%% title: FE-07 Report Submission, Independent Review and On-Demand PDF Export Sequence Diagram
sequenceDiagram
  autonumber
  actor Insp as Assigned Inspector
  actor Mgr as Independent Manager
  actor Caller as Authorized User
  participant Ctrl as InspectionController
  participant RepSvc as ReportService
  participant HistSvc as HistoricalCaseService
  participant Pdf as PdfReportRenderer
  participant DB as PostgreSQL & MinIO

  Insp->>Ctrl: POST /api/v1/inspections/{id}/report/ai-summary & POST /report/draft
  Ctrl->>RepSvc: generateAiSummary(...) & generateDraft(inspectorId, inspectionId)
  RepSvc->>HistSvc: findKnowledgeReferences(inspectionId) for source-backed references
  HistSvc-->>RepSvc: KnowledgeReferenceSummary list or empty when unavailable
  Note over Ctrl,DB: GET /knowledge-recommendations renders Matched Cases & Standards in ReportAiSummaryCard
  RepSvc->>DB: Create InspectionReport (status = SUBMITTED) and move Inspection to UNDER_REVIEW

  alt Manager Returns Report with Feedback
    Mgr->>Ctrl: POST /api/v1/inspections/{id}/report/versions/{verId}/review (approve = false, reason)
    Ctrl->>RepSvc: reviewVersion(managerId, inspectionId, verId, false, reason)
    RepSvc->>DB: Mark InspectionReport RETURNED and revert Inspection to FIELD_COMPLETED
  else Manager Approves and Directly Publishes Report
    Mgr->>Ctrl: POST /api/v1/inspections/{id}/report/versions/{verId}/review (approve = true)
    Ctrl->>RepSvc: reviewVersion(managerId, inspectionId, verId, true, null)
    RepSvc->>DB: Mark prior published version SUPERSEDED, set current version PUBLISHED, and Inspection COMPLETED
    RepSvc->>HistSvc: indexPublishedFindings(inspectionId) for future recommendations
  end

  Caller->>Ctrl: GET /api/v1/inspections/{id}/report/versions/{verId}/document
  Ctrl->>RepSvc: downloadArtefact(actorId, inspectionId, verId, locale)
  RepSvc->>Pdf: Render A4 PDF on demand if not cached, store at reports/{verId}.pdf in MinIO, and stream bytes
```

### 3.8 MF4 — FE-08 Customer Report Acceptance and Payment Settlement

This section presents the detailed design for `FE-08`: customer acceptance of a published report,
the `V4` payment-due window with a single overdue reminder and a notice/receipt PDF, VND settlement
through PayOS VietQR and VNPay with signed webhook verification, Manager-recorded partner settlement
with payouts and refunds, Inspector–Customer inspection chat with a configurable assignment-acceptance
timeout from `V61`, and the re-inspection loop opened against a published report to re-assess each
originally confirmed defect three ways with `V3` verdict validity.

#### 3.8.1 Class Diagram

```mermaid
%% title: FE-08 Customer Acceptance, Payment Settlement and Re-inspection Class Diagram
classDiagram
  class InspectionController {
    +createQuickReinspection(inspId, req) InspectionResponse
    +getReinspectionVerifications(inspId) List~ReinspectionVerificationResponse~
    +updateReinspectionVerification(inspId, verificationId, req) ReinspectionVerificationResponse
  }
  class ContractWorkflowService {
    +customerAcceptReport(custId, reqId, occId, verId) ServiceRequestResponse
    +createOccurrencePayOSCheckout(custId, reqId, occId, req) PayOSCheckoutResponse
    +createOccurrenceVnPayCheckout(custId, reqId, occId, req, ip) VnPayCheckoutResponse
    +handlePayOSWebhook(payload) void
    +handleVnPayWebhook(params) VnPayIpnResponse
    +recordOccurrencePayout(mgrId, reqId, occId, req) ServiceRequestResponse
    +initiateRefund(mgrId, reqId, occId, req) ServiceRefundResponse
    +completeRefund(mgrId, reqId, occId, refundId, req) ServiceRefundResponse
  }
  class ReinspectionVerificationService {
    +initializeVerificationsForReinspection(reinspectionId, sourceInspectionId) int
    +getVerifications(actorId, inspectionId) List~ReinspectionVerificationResponse~
    +updateVerification(actorId, inspectionId, verificationId, req) ReinspectionVerificationResponse
  }
  class PayOSWebhookController {
    +handleWebhook(payload) void
  }
  class VnPayWebhookController {
    +handleIpn(params) VnPayIpnResponse
  }
  class PaymentDocumentService {
    +download(actorId, inspId) byte[]
  }
  class InspectionChatController {
    +listThreads(actorId) List~InspectionChatThreadResponse~
    +getThread(actorId, inspId) InspectionChatThreadResponse
    +postMessage(actorId, inspId, body, files) InspectionChatThreadResponse
    +markMessagesRead(actorId, inspId) InspectionChatThreadResponse
    +downloadMessageAttachment(actorId, inspId, messageId, attachmentId) ResponseEntity
  }
  class InspectionChatService {
    +postMessage(actorId, inspId, body, files) InspectionChatThreadResponse
    +markMessagesRead(actorId, inspId) InspectionChatThreadResponse
  }
  class ServicePayment {
    -UUID id
    -UUID invoiceId
    -String provider
    -BigDecimal amountVnd
    -PaymentStatus status
    -String providerTransactionRef
    -Instant paymentDueAt
    -Instant paymentOverdueNotifiedAt
  }
  class ServiceRefund {
    -UUID id
    -UUID paymentId
    -BigDecimal amountVnd
    -RefundStatus status
    -String evidenceReference
  }
  class ReinspectionDefectVerification {
    -UUID id
    -UUID reinspectionId
    -UUID sourceFindingId
    -UUID newEvidenceId
    -DefectResolutionStatus resolutionStatus
    -String inspectorNotes
    -Instant verifiedAt
    -Instant validUntil
  }
  ContractWorkflowService --> ServicePayment
  ContractWorkflowService --> ServiceRefund
  PayOSWebhookController --> ContractWorkflowService
  VnPayWebhookController --> ContractWorkflowService
  InspectionController --> PaymentDocumentService
  InspectionChatController --> InspectionChatService
  ReinspectionVerificationService --> ReinspectionDefectVerification
```

**Class Specifications**

| No | Class | Description |
| :---: | :--- | :--- |
| 01 | `ContractWorkflowService`, `PayOSWebhookController` & `VnPayWebhookController` | Record Customer acceptance (`PAYMENT_DUE`), issue PayOS/VNPay checkout links, verify signed callbacks, and settle Customer payment (`PAID`) with Inspector payout `ELIGIBLE` only. `MANAGER` records actual payout references; unresolved orders cannot be replaced, and only provider-confirmed PayOS cancellation clears an unpaid order. Manager-recorded external refunds use a capped auditable ledger and hold payout until explicit reconciliation records the actual final payout and attribution. |
| 02 | `ServicePayment` & `ServiceRefund` | Domain entities representing a provider payment against a service invoice and an evidence-backed refund with its allocation. |
| 03 | `ReinspectionVerificationService` | Open a re-inspection against a source inspection, initialize one `ReinspectionDefectVerification` row per originally confirmed defect, and record each three-way outcome (`RESOLVED`, `UNRESOLVED`, `INCONCLUSIVE`) with the inspector's note and the supporting evidence capture. Recording is refused while the re-inspection is still `SCHEDULED` or `IN_PROGRESS`, and locked once a report for it is `SUBMITTED` or `PUBLISHED`. |
| 04 | `ReinspectionDefectVerification` | Domain entity linking the re-inspection, the source finding, the replacement evidence, and the recorded resolution status. |
| 05 | `PaymentDocumentService` (`V4`) | Renders the payment notice/receipt PDF at `GET /api/v1/inspections/{inspectionId}/report/payment-document`. On acceptance, `service_payments.payment_due_at` is set from the configurable window (default 15 days) and `payment_overdue_notified_at` guards a single overdue reminder; both deadlines are surfaced on Web and Mobile. |
| 06 | `InspectionChatController` & `InspectionChatService` (`V61`) | Inspector–Customer chat through `GET /api/v1/inspections/messages/threads`, `GET /api/v1/inspections/{inspectionId}/messages`, `POST /api/v1/inspections/{inspectionId}/messages`, `POST /{inspectionId}/messages/read`, and `GET /{inspectionId}/messages/{messageId}/attachments/{attachmentId}`. The body is capped at 4000 characters, attachments at 20 MiB each, and every read rechecks inspection scope. `platform_operations_settings.assignment_acceptance_timeout_hours` (default 24) bounds dispatch acceptance before automatic unassignment. |
| 07 | `ReinspectionVerificationService` (validity path, `V3`) | A `RESOLVED` verdict requires fresh evidence captured in the re-inspection's completed field-session window and stores `verified_at` plus a derived `valid_until`. Web `VerdictExpiryBanner` (`verdictExpiry.ts`) and Mobile `verdict_expiry.dart` split verdicts into expired and expiring-soon, so stale verdicts cannot close regressed defects. |
| 08 | Mobile Customer parity (`PR #27`) | `KnowledgeReferencesStrip` (`knowledge_references_strip.dart`), `InspectionChatPage` (`inspection_chat_page.dart`), `verdict_expiry.dart`, and payment-due/PDF document support keep the Customer Flutter app aligned with the Web portal across the published-report and re-inspection stages. |

#### 3.8.2 Customer Report Acceptance and PayOS / VNPay Online Payment Sequence Diagram

```mermaid
%% title: FE-08 Customer Report Acceptance and PayOS / VNPay Online Payment Sequence Diagram
sequenceDiagram
  autonumber
  actor Cust as Customer
  participant Ctrl as InspectionController / ContractWorkflowController
  participant Webhooks as PayOSWebhookController / VnPayWebhookController
  participant ContractSvc as ContractWorkflowService
  participant DocSvc as PaymentDocumentService
  participant PayGW as PayOSPaymentGateway / VnPayPaymentGateway
  participant DB as PostgreSQL

  Cust->>Ctrl: POST /api/v1/inspections/{id}/report/versions/{verId}/accept
  Ctrl->>ContractSvc: customerAcceptReport(customerId, requestId, occurrenceId, versionId)
  ContractSvc->>DB: Verify report is PUBLISHED and transition occurrence paymentStatus to PAYMENT_DUE
  ContractSvc->>DB: Set payment_due_at from the configurable window (default 15 days)
  Cust->>Ctrl: GET /api/v1/inspections/{id}/report/payment-document
  Ctrl->>DocSvc: download(customerId, inspectionId)
  DocSvc-->>Cust: Notice/receipt PDF carrying the due date and payment instructions

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

  ContractSvc->>DB: Transition customer payment to PAID and payout to ELIGIBLE, then a Manager records the actual payout separately
  Note over ContractSvc,DB: Refund initiation occurs before manual external transfer and immediately holds any unpaid Inspector payout
```

#### 3.8.3 Refund Initiation, External Completion, Legacy Reconciliation and Receivable Recovery

Manager-only operations run under a locked occurrence transaction. `POST /contracts/requests/{requestId}/occurrences/{occurrenceId}/refunds` validates captured balance and a case-insensitive request reference, reserves the refund amount, and holds an unpaid payout before any external transfer. No gateway or bank transfer is initiated by the system. After the Manager completes the transfer outside the platform, `POST .../refunds/{refundId}/complete` accepts a unique external reference and accounting allocations whose sum exactly equals the refund. Cancellation requires a reason and is rejected after completion; hold release is recalculated against all other pending and unallocated legacy rows.

Legacy `COMPLETED` refunds with unknown allocation are reconciled one row at a time by ID through `POST .../refunds/{refundId}/reconcile-allocation`. The evidence reference, note, Manager and time are stored with the allocation. Already-paid Inspector payouts are immutable: initiation records the receivable/platform-absorption plan and completion adds an `inspector_receivables` row. Managers record actual collections separately through `POST .../receivables/{receivableId}/recover`; row locking and optimistic versioning prevent concurrent over-recovery, and the system never offsets future payouts automatically. Manager finance responses list the refund and receivable ledgers; Customer responses mask internal recovery details. The Contracts UI presents separate forms for initiation, completion/cancellation, refund-ID legacy reconciliation, and manual receivable recovery.

---

### 3.9 Design Constraints and Exclusions

**No maintenance design exists.** Corrective maintenance — work orders, repair scope advisory, repair execution, completion reporting, and cost close-out — is absent from the delivered codebase. There is no maintenance package, class, endpoint, or table, so there is no retained schema to document. `reinspection_defect_verifications` is part of the inspection design, not of a maintenance design: it records the three-way comparison between an original finding and its re-observed evidence during a re-inspection, including the `V3` `valid_until` expiry of a `RESOLVED` verdict, and that loop is designed in `FE-08`.

**DroneKnowledgeAI is advisory, tenant-isolated and degradation-tolerant.** `V62` creates the `pgvector` extension, `V64` backfills published historical cases, and `V65` persists `vector(384)` embeddings in `inspection_knowledge_chunks` (eight seeded engineering standards) and `historical_finding_cases` (six anonymized benchmarks plus published confirmed findings), each with an HNSW `vector_cosine_ops` index. `HistoricalCaseService` backfills missing vectors on `ApplicationReadyEvent` and queries these stores behind the inspections-owned `HistoricalCaseAdvisorPort`, using `PGVECTOR_RAG` via the local `fastembed` `/v1/embeddings` endpoint inside `ai-inference` when available and deterministic `HYBRID_MATCH` otherwise, as well as `AI_VISION_RAG` for localized finding note drafting (`POST .../draft-note`). Retrieval is scoped by `(organization_id = actor org OR is_anonymized_benchmark = TRUE) AND (source_inspection_id IS NULL OR source_inspection_id <> current inspection)`, so no cross-organization PII is exposed. Recommendations, drafted notes, and knowledge references never confirm a finding, publish a report, clear a location for flight, or authorize maintenance.

**Buildings only.** Building-defect classes, inspection checkpoints, and asset categories are all building-specific. No design element addresses bridges, transmission towers, solar farms, roads, dams, tunnels, ports, or pipelines.

**Separation of duties is a design constraint, not a UI convention.** The reviewer of a flight permit or a report must differ from its author, enforced by comparing the acting user against the stored author or submitter inside the service transaction. This rule is implemented in the domain services rather than in the client, so a direct API call cannot bypass it.

**External services never substitute for human authority.** The detection service, the vision fallback, the narrative drafter, the DroneKnowledgeAI case/standard advisor, and the airspace advisory all produce advisory output. None of them can confirm a finding, approve a permit, publish a report, or clear a location for flight; each of those transitions requires an authenticated human decision recorded with its actor and time.
