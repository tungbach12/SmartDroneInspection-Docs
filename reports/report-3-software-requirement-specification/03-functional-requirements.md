---
title: "Report 3 - Functional Requirements"
document_type: report3-srs-section
weight: 35
source: "report3-software-requirement-specification.docx"
---

## 3. Functional Requirements

### 3.1 System Functional Overview

SmartDroneInspection supports six product features (`FE-01` to `FE-06`) across three business flows (`MF1` to `MF3`): user and organization onboarding; inspection requests and dispatch; and field inspection, evidence, reporting, and payment. Corrective maintenance is outside the application scope. Existing maintenance database schema and records are retained for data preservation, but the application no longer exposes maintenance workflows. The requirements below describe expected service outcomes and business controls, not claims about current implementation.

#### 3.1.1 Screens Flow

```mermaid
%% title: Business Screens Flow Diagram
flowchart TD
  SIGNIN["FE-01: Customer Registration and User Sign-in"] --> ONBOARD["FE-02: Partner, Customer Workforce and Asset Onboarding"]
  SIGNIN --> REQUEST["FE-03: Recurring Requests and Occurrences"]
  SIGNIN --> QUOTE["FE-04: Requests, VND Quotations and Signed Agreements"]
  QUOTE --> DISPATCH["FE-04: Partner Assignment and Dispatch"]
  DISPATCH --> PERMIT["FE-05: Permit and Field Readiness"]
  PERMIT --> FIELD["FE-05: Record On-site Field Session"]
  FIELD --> EVIDENCE["FE-06: Evidence and Human-Reviewed Findings"]
  EVIDENCE --> PREPARE["FE-06: Prepare and Submit Report"]
  PREPARE --> REVIEW["FE-06: Independent Review and Publication"]
  REVIEW --> PAYMENT["FE-06: Customer Report Acceptance and Payment"]
```

#### 3.1.2 Screen Descriptions

| # | Feature | Screen | Description |
| --- | --- | --- | --- |
| 1 | FE-01 | Customer Registration and User Sign-in | Allows a Customer to register an organization with an initial asset subject to airspace screening, and allows users to sign in and manage their account. |
| 2 | FE-01 | Account and Session Management | Allows users to maintain their account information and end active sessions. Access is limited to their authorized responsibilities. |
| 3 | FE-02 | Partner Provisioning and Workforce | The target service requires platform-governed partner qualification and review and drone registration review. The current service provisions Inspector accounts through platform staff; it does not provide self-service Inspector applications or application review. |
| 4 | FE-02 | Asset and Drone Registration | Supports Customer asset and checkpoint management and Inspector registration of owned drones with required supporting documents. |
| 5 | FE-03 | Recurring Requests and Occurrences | Allows Customers and `MANAGER` to manage recurring service requests and the inspection occurrences due under an agreed request. |
| 6 | FE-03 | Notifications | The target service requires relevant notices about records and decisions within authorized access, including reminders for future recurring occurrences. Automatic occurrence reminders are not implemented in the current service. |
| 7 | FE-04 | Service Requests, Quotations, Chat and Agreements | Allows Customers to request inspections, negotiate through contextual messages, review and accept VND quotations, and access the signed agreement record. |
| 8 | FE-04 | Partner Assignment and Airspace Information | Allows `MANAGER` to assign qualified Inspectors and eligible drones, account for schedule conflicts across customer organizations, and review relevant airspace information. |
| 9 | FE-05 | Permit and Field Session | Allows assigned Inspectors to provide a mission flight permit and record the start, completion, or abort of field work with required notes. |
| 10 | FE-06 | Evidence and Findings Review | Allows Inspectors to provide and review inspection photographs and videos, consider advisory defect suggestions, and confirm the findings baseline. |
| 11 | FE-06 | Report Preparation, Publication and Payment | Supports author preparation and submission, independent review and publication, Customer report acceptance, and service-fee payment (report export to PDF is an auxiliary deliverable download). |

#### 3.1.3 Screen Authorization

The following matrix describes which roles may carry out the named business activities. Access to a screen or record is not itself permission to perform an action; organization ownership, assignment, qualifications, and separation-of-duties requirements also apply.

| Business activity | `ADMIN` | `MANAGER` | `CUSTOMER` | `INSPECTOR` |
| --- | :---: | :---: | :---: | :---: |
| Sign in and manage own account | X | X | X | X |
| Govern platform accounts, asset categories, and finance settings | X |  |  |  |  |
| Review customer airspace cases, partner qualification records, and drone registrations | X | X |  |  |  |
| Provide partner qualification information through platform-governed admission; manage own drone registrations |  |  |  | X |  |
| Manage organization assets |  |  | X |  |
| Manage recurring service requests and occurrences |  | X | X |  |  |
| Create service request, negotiate, and accept quotation |  | X | X |  |  |
| Issue VND quotation and record signed agreement |  | X |  |  |  |
| Assign, reschedule, reassign, or cancel an inspection |  | X |  |  |  |
| Provide mission permit and record assigned field work |  |  |  | X |  |
| Provide evidence and confirm findings |  |  |  | X |  |
| Prepare and submit inspection report |  |  |  | X |  |
| Independently review and publish inspection report | X | X |  |  |  |
| Accept published report, pay fee, and refer defects |  |  | X |  |  |

#### 3.1.4 Business Support Functions

| # | Feature | Business support function | Required outcome |
| --- | --- | --- | --- |
| 1 | FE-01 | Sign-in and account protection | Only the account holder can use their account. Repeated failed sign-in attempts are limited, and a security-sensitive account change ends affected active sessions. |
| 2 | FE-02 / FE-04 | Airspace screening and information | Asset and mission locations are compared with relevant airspace information. The result informs internal review and does not grant legal permission to fly. |
| 3 | FE-03 | Recurring request coordination | Each occurrence under an accepted recurring service request is identifiable, assigned, and tracked separately while remaining linked to the agreed request and signed agreement. |
| 4 | FE-03 | Notifications | Relevant lifecycle updates are communicated to the responsible users without creating duplicate notices for the same event. |
| 5 | FE-04 | Partner qualification and availability | Assignment considers active partner status, current pilot credentials, drone eligibility, ownership, and overlapping commitments across customer organizations. |
| 6 | FE-06 | Evidence and advisory analysis | Inspection evidence is associated with the relevant field work. Automated defect suggestions remain unconfirmed until reviewed by the assigned Inspector. |
| 7 | FE-06 | Report preparation and publication | The Inspector prepares and submits the report; a different authorized reviewer makes the publication decision. Published reports are preserved, and a change is issued as a new version. |
| 8 | FE-06 | Service payment and settlement | Customer acceptance and payment are recorded against the applicable inspection occurrence; partner settlement is tracked distinctly from Customer payment. |

#### 3.1.5 Business Domain Concepts

```mermaid
%% title: Business Domain Concepts Diagram
flowchart LR
  CUSTOMER["Customer Organization"] --> ASSET["Infrastructure Asset"]
  CUSTOMER --> REQUEST["Service Request"]
  REQUEST --> QUOTE["VND Quotation"]
  REQUEST --> AGREEMENT["Signed Service Agreement"]
  REQUEST --> OCCURRENCE["Inspection Occurrence"]
  OCCURRENCE --> INSPECTION["Inspection"]
  INSPECTOR["Inspector"] --> INSPECTION
  DRONE["Inspector-Owned Drone"] --> INSPECTION
  ASSET --> INSPECTION
  INSPECTION --> SESSION["Field Session"]
  SESSION --> EVIDENCE["Inspection Evidence"]
  EVIDENCE --> FINDING["Confirmed Finding"]
  INSPECTION --> REPORT["Inspection Report"]
  REPORT --> PAYMENT["Service Payment"]
```

The target business record set includes customer organizations and users; Inspector qualification information; owned drone registrations; infrastructure assets and reference documents; service requests, quotations, messages, signed agreements, and occurrences; inspections, permits, field sessions, evidence, findings, and report versions; payment and partner settlement records; relevant activity history. In the current service, Inspector accounts are provisioned by platform staff rather than through self-service applications. These concepts describe business information without prescribing how it is stored.

---

### 3.2 FE-01 Customer Registration, Sign-in and Account Access

#### 3.2.1 Customer Registration and User Sign-in
- **Function trigger**: A prospective Customer registers an organization and first asset, or a user signs in.
- **Actors**: All Roles; automated identity service.
- **Function description**: Register customer organizations subject to airspace screening and provide authorized users with secure access to their assigned responsibilities.
- **Requirements**:
  - Customer registration includes a responsible person, organization identity, and initial asset location and description.
  - A location within a prohibited No-Fly Zone is not eligible for registration. A location requiring review remains pending for `ADMIN` decision. A location that passes the service's screening may proceed; this is not legal flight clearance.
  - Users sign in using an available supported method and are directed to work appropriate to their role.
  - After five consecutive unsuccessful password attempts, sign-in is temporarily restricted for 15 minutes.
- **Normal cases**: A Customer whose initial location passes screening can proceed with organization and asset onboarding; an authorized user signs in successfully.
- **Abnormal cases**: A prohibited location is not accepted; an airspace case requiring review cannot be treated as approved until `ADMIN` records a decision; incorrect credentials do not grant access.

#### 3.2.2 Account Management and Four-Role Access
- **Function trigger**: A user updates their account information, changes a password, or ends an active session.
- **Actors**: All Roles.
- **Function description**: Maintain account access according to the four canonical roles and the user's organization, partner, and work assignment.
- **Requirements**:
  - Recognized roles are `ADMIN`, `MANAGER`, `CUSTOMER`, and `INSPECTOR`.
  - `CUSTOMER` access is limited to their own customer organization. An `INSPECTOR` may access only assigned inspections. `ADMIN` and `MANAGER` access is limited to their platform responsibilities.
  - Account or role changes and user-requested session revocation take effect for active access. Historical activity remains attributable to the responsible user.
  - A role, account, or screen does not confer legal aviation authority, professional qualification, or authority to bypass a review gate.
- **Normal cases**: Users manage their own allowed account information and access only the records and activities within their authorized scope.
- **Abnormal cases**: Attempts to access another organization's records, an unassigned inspection, or an action outside the user's role are denied.

---

### 3.3 FE-02 Partner Qualification, Workforce, Assets and Drone Registration

#### 3.3.2 Infrastructure Assets, Airspace Screening and Inspector-Owned Drones
- **Function trigger**: A Customer registers or updates an asset, or an existing Inspector submits registration information for an owned drone. Drone registration is distinct from partner account admission.
- **Actors**: `CUSTOMER`, `INSPECTOR`, `ADMIN`, `MANAGER`.
- **Function description**: Maintain customer infrastructure and partner-owned drone records needed to plan and conduct inspections.
- **Requirements**:
  - An asset record identifies the infrastructure, its location and category, and the inspection checkpoints relevant to it. Related reference documents may be associated with the asset.
  - Asset creation is blocked for a location identified as prohibited airspace; a location requiring review follows the applicable human review process.
  - An Inspector drone registration includes identifying details, at least one real drone photo (`DRONE_IMAGE`), structured outdoor flight capabilities (maximum wind resistance, optical zoom, thermal camera, RTK GNSS positioning), selected feature/safety checklist items configured by `ADMIN` (`drone_feature_configs`), and supporting documents defined by `ADMIN`-configured requirements (`drone_document_configs`). By default, `REGISTRATION` and `OWNERSHIP` are active and required while `INSPECTION` is optional/inactive unless enabled by `ADMIN`.
  - An Inspector may also submit a renewal or update application for an existing active drone they own; duplicate serial submissions for drones owned by another Inspector or organization, or when a `PENDING` application already exists, are rejected.
  - `ADMIN` or `MANAGER` reviews the drone registration and records an attributable decision. Only a drone accepted for service may be considered for assignment to its owning Inspector.
  - Drone records are classified by Maximum Take-Off Weight (MTOW) into the 5 categories of Article 4 of Decree 288/2025/ND-CP; airframes with MTOW >= 2.0 kg (Category 3+) require the assigned Inspector to hold a Class B pilot license (Article 27 of Decree 288/2025/ND-CP) during quotation, mission dispatch, reassignment, and flight-permit verification.
- **Normal cases**: A Customer maintains eligible assets; an `ADMIN` configures active drone document requirements and capability/safety checklist items; an Inspector submits drone photos, capabilities, and required documents for review and, after approval, the drone may be considered for partner assignments.
- **Abnormal cases**: Prohibited locations cannot be registered as eligible assets; missing required drone documents, missing drone photo (`DRONE_IMAGE`), duplicate serial owned by another actor, or an unresolved drone review prevents the drone from being used for an inspection.

---

### 3.4 FE-03 Recurring Service Requests, Occurrences and Notifications

#### 3.4.1 Recurring Service Requests and Occurrences
- **Function trigger**: A Customer submits or updates a recurring service request, or `MANAGER` prepares one of its inspection occurrences.
- **Actors**: `CUSTOMER`, `MANAGER`, automated service support.
- **Function description**: The target service shall support recurring inspection requests and the coordination of distinct service occurrences under one agreed request. In the current service, planned occurrences are materialized when the recurring request's quotation is accepted; this is not time-based generation, and automatic future-occurrence reminders are not implemented.
- **Requirements**:
  - A new recurring service request uses a monthly interval of 1–120 months, including common 1, 3, 6, 9, and 12 month choices. A request is bounded by either 2–100 occurrences or an end date that produces 2–100 occurrences.
  - A new Customer request contains the asset, first requested inspection date, and one-time/recurring choice. Detailed scope and inspection-items are established during Manager quotation, not required in the request form.
  - The first requested inspection date must be at least 20 calendar days after the current date in the platform's `Asia/Ho_Chi_Minh` business timezone. This is a product scheduling lead-time policy to allow processing and preparation; it is not represented as a statutory 20-day legal deadline.
  - The requested agreement term end is derived from the requested first date and recurrence bound. For count-bound schedules it is the last calculated occurrence date; for end-date schedules it is the selected end date. The Manager's quoted first occurrence anchors the schedule and must not fall before the requested start or cause the planned schedule to exceed the requested agreement term.
  - The recurring schedule preview and quote must use the Customer-requested first date as the anchor; the Manager cannot shift the first occurrence to another date. Calendar-month arithmetic is anchored to that requested day and clamps to the last valid day of shorter months (for example, a day 31 monthly series uses the last day in February).
  - Before a recurring quote is saved or accepted and before its occurrences are materialized, the selected partner Inspector's pilot license and the selected drone's registration must remain valid at every planned occurrence start. If any scheduled occurrence falls on or after the applicable expiry instant, the workflow rejects the quote/acceptance and does not create partial occurrence records. The Manager must select an eligible partner or adjust the request schedule through a newly agreed request.
  - Each occurrence, when prepared for delivery, is identifiable by its planned period, assignment, delivery, and payment status, and remains associated with its parent request.
  - Where the parties agree, one signed service agreement may cover the occurrences within its stated term. Each occurrence still requires its own partner assignment, readiness checks, inspection, reporting, and settlement.
  - Occurrence planning and any reminders shall follow the agreed request. Time passing alone does not authorize an inspection or partner assignment.
- **Normal cases**: The Customer chooses an asset, a first date at least 20 days ahead, and either one-time or a recurring monthly cadence with a 2–100 occurrence or end-date bound. The parties agree a signed service agreement and coordinate each occurrence using the agreed timing and scope.
- **Abnormal cases**: An earlier requested start date is rejected; a recurring schedule resolving to fewer than two or more than 100 occurrences is rejected; a quote that cannot fit the agreed term cannot be accepted/materialized; an occurrence is not dispatched if the assigned partner or drone is unavailable or no longer meets applicable requirements. A change to the agreed frequency or term requires the parties' agreement.

#### 3.4.2 Notifications
- **Function trigger**: A significant service, inspection, or payment decision occurs, or a user reviews available notices.
- **Actors**: All Roles; service support.
- **Function description**: The target service should inform responsible users about relevant events and actions while respecting access boundaries. Automatic recurring-occurrence reminders are a target requirement, not a current capability claim.
- **Requirements**:
  - Where provided, notices identify the event, when it occurred, and the relevant record or action.
  - The target notification service should avoid duplicate notices for the same event when processing is retried.
  - Following a notice never grants access to its target record; the user's normal authorization still applies.
  - Automatic reminders for future occurrences are required in the target service but are not implemented in the current service.

- **Normal cases**: A user receives and reviews a relevant notice and can navigate to an authorized record.
- **Abnormal cases**: A user cannot view or act on a record outside their organization, role, or assignment because they received a notice.

---

### 3.5 FE-04 Service Requests, Quotations, Agreements and Dispatch

#### 3.5.1 Service Request, VND Quotation, Negotiation and Signed Agreement
- **Function trigger**: A Customer submits a one-time or recurring service request, exchanges messages with `MANAGER` via the dedicated Messages inbox, or accepts a quotation; the parties sign an offline service agreement.
- **Actors**: `CUSTOMER`, `MANAGER`.
- **Function description**: Establish an agreed inspection scope and commercial terms before inspection work is dispatched.
- **Requirements**:
  - A new Customer service request identifies the asset and requested timing, and is one-time or recurring. Detailed inspection scope is agreed in the Manager's quotation; the Customer request form does not require free-text scope or display the configured inspection-item checklist. For one-time requests, the Customer chooses a single date (`requestedFrom` equals `requestedUntil`); `MANAGER` cannot propose a different date. Both one-time and recurring first dates must be at least 20 calendar days after the current date in `Asia/Ho_Chi_Minh` business time as an internal scheduling policy.
  - Customer and `MANAGER` can exchange contextual messages via the dedicated left-nav Messages inbox. A message does not itself change quotation terms.
  - `MANAGER` issues and edits a single active VND quotation stating scope, timing, and price per occurrence directly without maintaining historical quote revisions. For recurring requests, the quotation's first occurrence must use the Customer-requested first date as its schedule anchor; `MANAGER` cannot shift that date. The Customer accepts the current active quote. The selected partner Inspector's pilot license and the selected drone's registration must cover every scheduled occurrence start before the quote is saved, accepted, or occurrences are materialized; any expired credential rejects the operation without partial occurrence records.
  - When the Customer accepts the quote, an immutable snapshot of agreed terms (`accepted_terms_snapshot`) is stored and terms are locked against further modification.
  - The parties sign the service agreement offline. `MANAGER` records the signed document after execution. A commercial request is not ready for field dispatch until the signed agreement has been recorded.
  - A recurring agreement applies only to the term and occurrences it describes.
  - The request-detail lifecycle indicator presents four concise stages with role-specific labels: for `CUSTOMER`, submit request, review Manager quotation, accept terms and sign the agreement, and await scheduled inspection; for `MANAGER`, review the Customer request, prepare and discuss the quotation, record the signed agreement, and assign the inspection team. The indicator omits explanatory subtext; authoritative actions and requirements remain in their corresponding panels.
  - In the Service Requests list, status uses the shared inspection status-chip visual style and is paired with a compact four-step progress subtitle derived from the request state. `OPEN` is step 1, `QUOTED` step 2, `ACCEPTED` and `CONTRACT_SIGNED` step 3, and `ASSIGNED` step 4. `CANCELLED` remains terminal and does not imply progress through the active workflow.
- **Normal cases**: The Customer submits a request (single date for one-time); `MANAGER` issues or directly edits the active VND quotation; the Customer accepts the active quote or messages `MANAGER` via the Messages inbox to negotiate; terms lock upon acceptance; the parties sign an agreement; and `MANAGER` records it.
- **Abnormal cases**: A first requested date earlier than the 20-day product lead time is rejected (`400`). A multi-day date range for a one-time request is rejected (`400`). A recurring quotation that shifts the Customer-requested first date is rejected. An accepted quote cannot be modified or deleted. A dispatch cannot proceed without an accepted quotation and recorded signed agreement. A message is not treated as quote acceptance or as a change in price or scope.

#### 3.5.2 Partner Assignment, Dispatch Recovery and Airspace Information
- **Function trigger**: `MANAGER` assigns an Inspector and owned drone to an agreed occurrence, or responds to an aborted field session.
- **Actors**: `MANAGER`, `ADMIN`, `CUSTOMER`, `INSPECTOR`, automated service support.
- **Function description**: Assign a qualified partner and eligible drone to an occurrence, manage dispatch changes, and provide relevant airspace information.
- **Requirements**:
  - Assignment uses a Inspector and drone eligible for the work; the drone must be owned by that Inspector and have passed its required review.
  - Assignment considers current pilot qualifications and overlapping commitments across all customer organizations.
  - After an abort, `MANAGER` may reschedule, reassign, or cancel the dispatch. The decision and its reason are attributable.
  - Airspace information supports planning but does not certify legal clearance or authorize flight.
- **Normal cases**: An available, qualified Inspector and eligible owned drone are assigned to an occurrence; after an abort, `MANAGER` records an appropriate recovery decision.
- **Abnormal cases**: Conflicting commitments, expired pilot credentials, an unapproved drone, or a drone not owned by the selected Inspector prevent assignment.

---

### 3.6 FE-05 Flight Permit and On-site Field Sessions

#### 3.6.1 Flight Permit and On-site Field Session
- **Function trigger**: The assigned Inspector prepares to perform field work, starts a session, completes it, or aborts it.
- **Actors**: `INSPECTOR`, `MANAGER`.
- **Function description**: Record required mission documentation and accountable on-site session outcomes. An optional SmartDroneHub integration may display read-only MAVLink telemetry or clearly labelled demo telemetry; the service does not plan routes or control aircraft.
- **Requirements**:
  - Before field work begins, the assigned Inspector provides the required mission flight permit and current pilot credentials. These checks do not grant governmental authorization.
  - Starting a session records a pre-flight safety note addressing relevant aircraft, battery, and environmental conditions.
  - For a permitted active field session, the assigned Inspector may start an explicitly selected live Mission Planner MAVLink telemetry connection or a separate telemetry-only demonstration. A live stream is assigned to at most one active session; the Hub does not arm, guide, upload flight plans to, or control an aircraft.
  - MAVLink is optional. If the aircraft or its manufacturer application cannot provide the live Hub connection, the assigned Inspector may import an exported SRT, CSV, KML, or GPX flight log. The system validates and normalizes available GPS positions, timestamps, altitude, speed, heading, and battery values; fields absent from the source are shown as unavailable rather than fabricated. Imported trace and computed summary are persisted with the source format identified.
  - If no supported log is available, the assigned Inspector may submit an accountable manual flight declaration with a reason, estimated duration, optional estimated maximum altitude, and field note. The report must clearly distinguish this declaration from telemetry and imported logs; it does not claim an independently verified flight path.
  - The service may show received flight mode, position, altitude, speed, heading, battery, and waypoint telemetry, persist the session's observed flight report and GPS flight trace (`flight_trace_json`) on closure so both `INSPECTOR` and `MANAGER`/`CUSTOMER` reviewers can audit the flown path, and synchronize mission recording video (`video/mp4`) or camera snapshots from `SmartDroneHub` into the authenticated evidence store.
  - Completion records the outcome. An abort records the reason and alerts `MANAGER` to arrange rescheduling, reassignment, or cancellation.
- **Normal cases**: The Inspector records readiness, starts and completes a session, and provides field evidence; optionally, the Inspector views read-only Hub telemetry during the active session, imports a supported flight log when live MAVLink is unavailable, or submits a clearly labelled manual flight declaration when no supported log is available. The Inspector and authorized reviewers can view the persisted report and any available GPS trace after closure; or the Inspector records an abort and `MANAGER` handles dispatch recovery.
- **Abnormal cases**: The service prevents a session from being recorded as ready to start when the required permit, current pilot credentials, or safety note is missing, or after field work has already been completed (`FIELD_COMPLETED`). Unsupported, empty, malformed, oversized, or GPS-less imported logs are rejected with a corrective error. A software record is not a physical flight command; a missing or stale live MAVLink heartbeat prevents live telemetry from being treated as connected; a single live stream cannot serve concurrent sessions. Manual declarations remain explicitly unverified and are not presented as measured telemetry.

---

### 3.7 FE-06 Evidence, Findings, Reports and Payment

#### 3.7.1 Inspection Evidence and Findings Confirmation
- **Function trigger**: An assigned Inspector provides inspection evidence and reviews candidate findings.
- **Actors**: `INSPECTOR`, automated advisory service.
- **Function description**: Maintain evidence for an inspection and establish an accurate, human-confirmed findings baseline.
- **Requirements**:
  - Evidence may include photographs and high-resolution MP4 video (up to 500 MB), with relevant capture time, location information when available, and structural location notes. From a stored MP4 flight video, the assigned Inspector may pause and interactively crop/extract a video frame into an image evidence item, or run automated YOLO11 video keyframe scanning to extract defect frames into Evidence and propose candidate findings. Missing camera or location metadata is disclosed and does not by itself invalidate otherwise suitable evidence.
  - Evidence that cannot be used or is a duplicate within the same inspection is identified for the Inspector.
  - Automated visual analysis may suggest possible defects. Each suggestion remains advisory until the assigned Inspector confirms, edits, or rejects it. The Inspector may record a finding manually when appropriate evidence is available.
  - Only findings confirmed by the Inspector are part of the official baseline and eligible for an inspection report.
  - If automated analysis is unavailable, the Inspector can still review evidence and record findings manually.
- **Normal cases**: The Inspector reviews evidence, resolves each automated suggestion, adds any supported manual findings, and confirms the official findings baseline.
- **Abnormal cases**: The findings baseline cannot be confirmed while unresolved candidate suggestions remain. An unconfirmed or rejected suggestion is excluded from official findings.

#### 3.7.2 Inspection Report Preparation, Independent Publication and Payment
- **Function trigger**: The report author prepares and submits an inspection report after findings confirmation; an independent reviewer assesses it; the Customer reviews the published report and initiates online payment via VNPay or PayOS.
- **Actors**: `INSPECTOR`, `MANAGER`, `ADMIN`, `CUSTOMER`, automated advisory service, payment service (`VNPay Gateway`, `PayOS Gateway`).
- **Function description**: Deliver a human-prepared and independently reviewed inspection report, provide any AI summary as advisory material, and record Customer acceptance and service payment via VNPay (v2.1.0 HMAC-SHA512) or PayOS VietQR.
- **Requirements**:
  - The report author uses the confirmed findings and relevant field records to prepare and submit the inspection report for independent review. Submission is an explicit report-preparation action; merely visiting a screen does not submit it.
  - A report summary generated with AI is advisory, based on verified inspection information, and reviewed by a person before reliance on it.
  - A `MANAGER` or `ADMIN` reviewer who is not the report author either publishes the submitted report as the official deliverable or returns it to the author with reasons. Approval and publication are one reviewer decision; no separate approved-but-unpublished state is required.
  - A published report is preserved as a versioned record. Any correction is issued as a new version, with prior versions retained.
  - Customers see the official published report, not internal drafts or unapproved findings. The applicable payment rule governs access to the official deliverable.
  - When the Customer accepts a published report, the service records the acceptance and applicable fee as due (`PAYMENT_DUE`). Online checkout supports both **VNPay** (`POST /api/v1/inspections/{inspectionId}/vnpay/create-payment-url`, verified via HMAC-SHA512 on `GET /api/v1/webhooks/vnpay/ipn` and `GET /api/v1/webhooks/vnpay/return`) and **PayOS VietQR** (`POST /api/v1/inspections/{inspectionId}/payos/create-payment-link`, verified via HMAC-SHA256 on `POST /api/v1/webhooks/payos`). Payment is recorded against the relevant occurrence (`PAID`); partner settlement is recorded automatically upon verified payment when an inspector is assigned.
  - If payment services are unavailable, the business must retain an authorized, attributable way to record payment confirmation rather than treat an unconfirmed payment as settled.
- **Normal cases**: The Inspector prepares and submits a report; an independent platform reviewer publishes it or returns it for revision; the Customer reviews and accepts a published report and pays through VNPay or PayOS (or authorized manual confirmation).
- **Abnormal cases**: A report author cannot review or publish their own report. A returned report includes reasons and remains available for revision. A Customer cannot access an unpublished report as an official deliverable, and payment is not marked settled without verified cryptographic signature or authorized confirmation.

---

### 3.8 Retired Feature Scope

Corrective maintenance work orders, repair execution, maintenance-specific re-inspection, and maintenance cost closeout are removed from the application. The service ends at inspection report acceptance and payment. Customers arrange any corrective work outside this application. Existing maintenance database schema and persisted records are retained unchanged; they are not exposed as application workflows.
