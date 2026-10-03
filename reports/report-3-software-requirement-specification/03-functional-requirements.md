---
title: "Report 3 - Functional Requirements"
document_type: report3-srs-section
weight: 35
source: "report3-software-requirement-specification.docx"
---

## 3. Functional Requirements

### 3.1 System Functional Overview

#### 3.1.1 Screens Flow

The browser application provides administration, Client, and Service Manager workflows. The mobile application provides assigned Inspector and Maintenance Engineer workflows. Each route is filtered by authenticated role and resource scope, while the backend remains the authorization authority.

![SmartDroneInspection screen flow](assets/screen-flow.png)

#### 3.1.2 Screen Descriptions

| # | Feature | Screen | Description |
| --- | --- | --- | --- |
| 1 | Authentication | Login | Authenticate an issued account across any actor zone and route the user to the permitted portal experience. |
| 1a | Authentication | Client Enterprise Registration | Register a new customer organization and its initial Client administrator account atomically. |
| 1b | Authentication | Provider Onboarding Registration | Register an independent service provider company, upload business license, drone registration codes per Luật PKND 2024, and third-party insurance. |
| 2 | Authentication | First Password Setup | Replace administrator-provisioned setup password before normal application access. |
| 3 | Common | Role Dashboard | Show role-filtered operational queues, upcoming flight deadlines, escrow balances, and recent inspection results. |
| 4 | Common | Profile and Security | View account information, update security settings, and revoke active sessions. |
| 5 | Platform Governance | User Management | Provision accounts, assign canonical roles, manage operational status, and audit security events. |
| 5a | Platform Governance | Provider Vetting Portal | Platform Operator portal to review provider business licenses, pilot certificates, drone registries, and insurance policies to approve or reject provider credentials. |
| 6 | Administration | Asset Categories & Checklists | Maintain standardized asset categories, checklist templates, and suggested inspection frequencies. |
| 7 | Assets | Asset Inventory & Airspace Map | Search, filter, and inspect asset profiles with integrated `cambay.mod.gov.vn` restricted airspace overlays. |
| 8 | Assets | Asset Details & Documents | Maintain asset specifications, upload engineering drawings, and review historical inspection/maintenance records. |
| 9 | Planning | Inspection Cadences | Manage proposed and selected recurring inspection schedules for active assets. |
| 10 | Sourcing & Bidding | Inspection Request & RFQ | Create inspection requests; choose direct provider selection or broadcast open RFQs with camera shot list and GSD resolution specifications. |
| 11 | Commercial | Quotation Management | Provider Manager prepares versioned quotations (covering direct flight and labor fees); Client reviews, requests revision, or accepts. |
| 12 | Commercial | Service Order & Conditional Funding | Review the electronic order, uniform Provider-paid commission terms and any contractually required advance funding via an authorized bank/payment partner; the Platform does not independently custody deposits. |
| 13 | Assignments | Flight Assignment & Permits | Provider Manager verifies pilot credentials, attaches Cục Tác chiến flight permit references, and issues flight assignments to Inspector. |
| 14 | Inspection | My Flight Missions | Mobile and web portal showing only assignments dispatched to the authenticated Inspector. |
| 15 | Inspection | Field Survey Session | Start inspection session, execute mandatory checklist items, and record flight progress. |
| 16 | Inspection | Evidence Ingestion | Chunked upload of photos and videos to MinIO with EXIF GPS extraction and SHA-256 digital integrity checksums. |
| 17 | AI Assistance | AI Candidate Review | Review centralized YOLO model detections; confirm, modify, reject candidates, or manually add unflagged defects. |
| 18 | Reports | Draft Compilation & Narrative | Compile technical report drafts with on-demand platform LLM narrative summary assistance. |
| 19 | Reports | Internal Peer Review | Cross-review of technical report by an independent Inspector within the same Provider (self-approval prohibited). |
| 20 | Reports | Provider QA Release | Provider Manager reviews deliverable completeness against contractual SOW and formally releases report to Client. |
| 21 | Reports | Released Report Review | Client portal to view, download, accept report, request clarification, or trigger dispute within 5-day review window. |
| 22 | Dispute Resolution | Dispute Filing & Internal Resolution | Client or Provider files a contractual complaint; Platform Operator reviews traceable evidence against SOW and coordinates internal remedies under public terms without replacing court or commercial arbitration. |
| 23 | Financial | Escrow Cash Flow & Payouts | Platform Operator monitors escrow pool, oversees auto-settlement, and coordinates net disbursements to providers. |
| 24 | Maintenance | Maintenance Ticket | Create repair ticket linked directly to verified defects from an accepted inspection report. |
| 25 | Maintenance | Defect Assessment | Maintenance Engineer conducts remote/on-site technical assessment, estimating scope, materials, and labor. |
| 26 | Maintenance | Maintenance Quotation & Order | Provider Manager prepares a maintenance quotation with an expressly agreed warranty-retention term; Client approves and funds the order through the qualified payment partner where the contract requires it. |
| 27 | Maintenance | Execution & Before/After Proof | Maintenance Engineer records work log, materials used, and captures mandatory before/after photo evidence. |
| 28 | Maintenance | Change Order Management | Document unforeseen damage; pause extra work until Client approves change order and supplemental escrow deposit. |
| 29 | Maintenance | Completion & Warranty Release | Client inspects before/after evidence to approve completion (releasing 90% payout) and final 10% retention release after 30-day warranty. |
| 30 | Audit | Security & Commercial Audit | Search immutable audit trails across authorization, escrow transactions, and dispute rulings within authorized scope. |

#### 3.1.3 Screen Authorization

The matrix maps screens to the six canonical roles across the three actor zones. `M` = Manage; `V` = View; `O` = Own organization scope only; `A` = Assigned resource scope only; `R` = Release or coordinate; blank = Denied. Backend authorization remains authoritative.

| Screen | Platform Admin | Platform Operator | Client | Provider Manager | Inspector | Maintenance Engineer |
| --- | --- | --- | --- | --- | --- | --- |
| Role Dashboard | V (System) | V (Platform) | V (Own Org) | V (Own Org) | V (Assigned) | V (Assigned) |
| User & System Security | Manage |  |  |  |  |  |
| Provider Vetting Portal | V | Manage |  | V (Own Org) |  |  |
| Standard Checklists & Categories | Manage | V | V | V | V | V |
| Asset Inventory & Details | V | V | Manage (Own Org)|  |  |  |
| Inspection Request & RFQ | V | Coordinate | Manage (Own Org)| V (Eligible RFQs)|  |  |
| Quotation Management | V | Coordinate | Decide (Own Org)| Manage (Own Org)|  |  |
| Service Order & Escrow Deposit | V | Monitor / Freeze | Decide (Own Org)| View (Own Org) |  |  |
| Flight Assignment & Permits | V | Coordinate | View (Own Org) | Manage (Own Org)| Respond (Assigned)|  |
| Field Survey & Evidence | V | View | View released | View (Own Org) | Manage (Assigned)|  |
| AI Candidate Review | V | View | View verified | View (Own Org) | Manage (Assigned)|  |
| Draft Report & Narrative | V | View |  | View (Own Org) | Manage (Authored)|  |
| Internal Peer Review | V | View |  | Assign reviewer | Manage (Assigned)|  |
| Report Release & Review | V | Coordinate | Accept / Clarify | Release (Own Org)| View (Authored) |  |
| Dispute Filing & Arbitration | V (Audit) | Arbitrate / Ruling | File (Own Org) | File / Respond | Consult |  |
| Escrow Payouts & Billing | V (System) | Disburse / Refund | View (Own Org) | View (Own Org) |  |  |
| Maintenance Ticket | V | Coordinate | Manage (Own Org)| View (Eligible) |  | View (Assigned) |
| Maintenance Assessment | V | Coordinate | View (Own Org) | Manage (Own Org)|  | Manage (Assigned) |
| Maintenance Quotation & Order | V | Monitor / Freeze | Decide (Own Org)| Manage (Own Org)|  | View (Assigned) |
| Execution & Before/After Proof | V | View | View (Own Org) | View (Own Org) |  | Manage (Assigned) |
| Maintenance Warranty Release | V | Disburse Retention | Accept / Dispute | View (Own Org) |  | View (Assigned) |
| Audit History | Manage & View | Authorized View | View (Own Org) | View (Own Org) | View (Assigned) | View (Assigned) |

#### 3.1.4 Non-Screen Functions

| # | Feature | System Function | Description |
| --- | --- | --- | --- |
| 1a | Authentication | Client registration | Atomically register customer organization and primary client administrator account. |
| 1b | Authentication | Provider onboarding vetting | Validate provider corporate credentials, pilot license registry, and drone identification numbers against regulatory registries. |
| 1 | Authentication | Token validation & revocation | Validate access tokens, enforce multi-tenant organization scoping, and rotate refresh tokens. |
| 2 | Airspace | Restricted airspace geofence check | Intersect asset coordinates with national no-fly and restricted airspace polygons (`cambay.mod.gov.vn`). |
| 3 | Planning | Periodic request generation | Automatically generate request packages from due cycles of Client-selected active schedules. |
| 4 | Commercial | Conditional funding and dispute hold | Receive verified transaction status from an authorized bank/payment partner; instruct conditional hold/release only within that partner's licensed product and accepted contract terms. Platform does not independently custody customer deposits. |
| 5 | Commercial | Auto-settlement scheduler | Under the proposed accepted review-window terms, instruct the authorized payment partner to settle eligible service funds net of the Platform's one published commission `C = r × B`; never collect commission twice on warranty-retention release. |
| 6 | Files | Evidence intake & validation | Validate file formats, calculate SHA-256 checksums, reject duplicates, and persist objects in MinIO with EXIF metadata. |
| 7 | AI Assistance | YOLO defect inference | Platform-hosted YOLO inference server detects cracks, spalling, and corrosion, publishing non-official candidates. |
| 8 | AI Assistance | LLM narrative draft generation | Platform-hosted LLM generates technical draft narrative summaries from snapshot data on Inspector demand. |
| 9 | Reports | Immutable versioning | Enforce append-only version snapshots upon Client acceptance; prevent tampering with finalized findings. |
| 10 | Dispute | Internal complaint resolution | Coordinate authorized payment-partner release/hold instructions, reshoot or justified refund under published Platform Terms; preserve lawful court and commercial-arbitration rights. |
| 11 | Maintenance | Warranty retention timer | Withhold 10% retention money in escrow; disburse automatically after 30 days without defect recurrence. |
| 12 | Audit | Forensic event logging | Immutable logging of security, authentication, financial escrow, and arbitration events without storing secrets. |

#### 3.1.5 Entity Relationship Diagram

The diagram describes the multi-provider platform domain model with tripartite escrow and dispute governance.

![SmartDroneInspection entity relationship diagram](assets/erd.png)

**Entities Description**

| # | Entity | Description |
| --- | --- | --- |
| 1 | Organization | Customer enterprise owning infrastructure assets and Client accounts. |
| 1a | Provider Organization | Independent commercial inspection/maintenance company with verified legal license, drone permits, and pilot roster. |
| 2 | User | System user account bound to an actor zone and owning customer or provider organization. |
| 3 | User Role Assignment | Role assignment enforcing canonical permissions across the three actor zones. |
| 4 | Auth Session | Web or mobile session token with independent revocation tracking. |
| 5 | Asset Category | Standard classification governing checklist templates and suggested inspection frequencies. |
| 6 | Checklist Template | Versioned inspection checklist definition with typed response requirements. |
| 7 | Asset | Customer infrastructure item with geographic coordinates and airspace restrictions. |
| 8 | Asset Document | Technical drawing, manual, or completion record associated with an asset. |
| 9 | Inspection Schedule | Recurring cadence established by Client generating due inspection request packages. |
| 10 | Inspection Request | RFQ or scheduled inspection demand specifying shot list, resolution, and constraints. |
| 11 | Inspection Quotation | Versioned commercial proposal submitted by a provider covering direct flight and labor fees. |
| 12 | Inspection Service Order | Legally binding electronic contract binding Client and Provider to approved quotation terms. |
| 12a | Conditional Settlement Transaction (target) | Proposed record of partner-confirmed funding, order-locked one-rate commission, disputed/retained amounts, refunds and payout; not a Platform bank account or an existing Flyway table. |
| 13 | Inspection Assignment | Flight mission assignment issued by Provider Manager to a certified Inspector. |
| 14 | Inspection | Active inspection mission execution record bound to an accepted order. |
| 15 | Checklist Response | Recorded inspection answers to checklist items. |
| 16 | Evidence | Stored visual file in MinIO with SHA-256 checksum, GPS, and timestamp digital provenance. |
| 17 | AI Finding Candidate | Non-official defect candidate generated by platform-hosted YOLO model. |
| 18 | Verified Finding | Inspector-confirmed defect with location, severity, and technical notes. |
| 19 | Inspection Report | Formal aggregate reporting document linked to an inspection. |
| 20 | Report Version | Versioned technical deliverable with peer review and release tracking. |
| 21 | Peer Review | Internal cross-review conducted by an independent Inspector within the same Provider. |
| 22 | Dispute Ticket | Formal dispute filed by Client or Provider freezing escrow and initiating operator arbitration. |
| 22a | Dispute Evidence | Forensic digital evidence (logs, MinIO files, SOW) attached to an active dispute. |
| 23 | Maintenance Ticket | Customer repair request referencing verified findings from an accepted report. |
| 24 | Maintenance Assessment | Technical estimate of repair scope, materials, labor, and cost range. |
| 25 | Maintenance Quotation | Versioned repair quotation with a disclosed contractual warranty-retention term if adopted; the illustrative 10% is not a statutory obligation. |
| 26 | Maintenance Order | Approved repair contract governing physical execution and two-stage escrow release. |
| 27 | Maintenance Assignment | Execution assignment dispatched to a Maintenance Engineer. |
| 28 | Maintenance Work Log | Recorded work progress, materials, and mandatory before/after photo evidence. |
| 29 | Change Request | Supplemental scope and cost approval record for unforeseen subsurface damage. |
| 30 | Invoice | Commercial billing record between Provider and Client, or platform fee statement. |
| 31 | Notification | Delivery record for workflow, deadline, escrow, and arbitration notices. |
| 32 | Audit Event | Immutable security, access, transaction, and decision event log. |

### 3.2 FE-01 Identity, Multi-Tenant Governance and Provider Vetting

FE-01 provides Client organization self-registration, Service Provider company onboarding and compliance vetting by `PLATFORM_OPERATOR`, account authentication, role- and organization-based access control, session revocation, and security audit logging. Backend authorization strictly separates `PLATFORM_GOVERNANCE`, `CUSTOMER_ORGANIZATION`, and `SERVICE_PROVIDER` actor zones.

#### 3.2.1 Identity, Vetting and Authorization Rules

- All users sign in through the versioned authentication API. The browser keeps access tokens in memory, uses the protected refresh-cookie flow, and does not persist credentials in browser storage. Mobile authentication uses the secure token-delivery contract and platform secure storage.
- A Client representative may self-register a new customer organization and its initial Client administrator account atomically.
- An independent service provider company registers by submitting corporate credentials: legal company name, tax code, business registration license, UAV identification registration numbers per *Luật Phòng không nhân dân 2024* & *Nghị định 288/2025/NĐ-CP*, certified drone pilot roster, and third-party aviation liability insurance.
- `PLATFORM_OPERATOR` audits and vets provider credentials in the Provider Vetting Portal, transitioning status to `VERIFIED` upon approval, or requesting supplementary documentation. Unverified providers cannot submit quotations or receive flight missions.
- `PLATFORM_ADMIN` maintains administrative security policies, technical parameters, and standard checklist templates.
- Logout, password change, disablement, role reassignment, and session revocation immediately invalidate affected active sessions.

### 3.3 FE-02 Asset Registry and Airspace Compliance

FE-02 lets a Client register enterprise infrastructure assets, check geographical coordinates against national no-fly zone databases, upload technical asset documentation, and select recurring inspection cadences.

#### 3.3.1 Manage Assets and Airspace Verification

**Function trigger:** The Client registers an asset or opens asset planning.

**Function description:**

- The Client enters asset identity, category, technical description, site-access constraints, responsible contacts, and precise GPS coordinates (latitude/longitude) defining the structure's physical envelope.
- The system automatically performs an airspace compliance check intersecting asset coordinates with national no-fly and restricted airspace geofences published on `cambay.mod.gov.vn` per *Quyết định 18/2020/QĐ-TTg*. Assets within restricted zones are flagged with mandatory flight-permit prerequisites.
- The Client uploads and versions engineering blueprints, completion manuals, and historical inspection records to MinIO.
- The Client sets up recommended recurring inspection cadences (e.g., monthly, quarterly, annual). Upon due cycle arrival, the scheduler automatically generates a periodic inspection request package inheriting asset metadata and constraints, routing it into MF2 sourcing.

**Validation and exception requirements:** Coordinates falling within prohibited military/aviation no-fly zones require explicit acknowledgment of special military flight clearances. Duplicate asset codes within the same organization are rejected. Retrying the due-cycle publisher cannot create duplicate request packages for the same cycle.

**Result:** An active asset profile with airspace compliance status and recurring inspection cadences ready for procurement sourcing.

### 3.4 FE-03 Inspection Sourcing, Quotation, Escrow and Flight Authorization

FE-03 targets procurement sourcing (direct selection or open RFQ), versioned Provider quotations, electronic service orders and conditional funding through an authorized bank/payment partner. It locks the Platform-published uniform Provider commission policy on each order. This target is not an implemented payment system or a conclusion that *Nghị định 52/2024/NĐ-CP* authorizes the Platform itself to pool customer funds.

#### 3.4.1 Source Provider, Deposit Escrow and Authorize Flight

**Function trigger:** An active inspection schedule reaches its due cycle, or Client creates an inspection demand/re-inspection.

**Function description:**

- The Client reviews the request package, defines image resolution requirements (Ground Sample Distance - GSD), specifies mandatory camera angles (Shot list), and selects the procurement mechanism:
  - *Direct Selection*: Dispatches RFQ directly to a pre-selected verified Provider.
  - *Open RFQ*: Broadcasts RFQ to all verified Providers qualified for the asset's geographic region.
- `PROVIDER_MANAGER` reviews asset coordinates, airspace flags, and SOW to prepare a versioned quotation. Quotation line items bóc tách transparently: (1) Field flight survey fee; (2) Engineering and pilot labor fees; (3) Deployment logistics; (4) Applicable VAT. **Platform centrally absorbs AI YOLO model inference, LLM narrative drafting, and MinIO storage costs in its own operational budget; providers do not charge clients for platform AI or storage.**
- The Client reviews quotations, requests adjustments (creating versioned revisions), and accepts the preferred quotation.
- The system drafts a legally binding electronic **Inspection Service Order** binding Client and Provider.
- The order captures the published uniform Platform commission policy version and rate `r`, accepted by the Provider under standard terms. If the order requires advance funding (illustratively 100%), the Client pays through an authorized partner whose contracted product supports conditional release; a partner-confirmed receipt, not a Platform account balance, enables the agreed execution gate. The order's contractual effect follows the accepted electronic terms, not funding alone.
- `PROVIDER_MANAGER` attaches Cục Tác chiến flight permit documentation (if required by airspace classification), assigns an active certified `INSPECTOR`, and dispatches the flight mission package.
- The assigned Inspector accepts or rejects the assignment. Acceptance transitions the inspection to `READY_FOR_INSPECTION`.

**Validation and exception requirements:** Flight execution follows the funding/permit conditions locked in the accepted order and requires partner confirmation where funding is agreed. Cancellation refunds and any dry-run fee depend on published, accepted terms and actual work already incurred; 24-hour and 20% figures are illustrative, not statutory defaults. Unsafe weather may justify documented rescheduling under the order terms without assuming every weather event automatically constitutes legal force majeure.

**Result:** A confirmed service order funded in escrow and an accepted Inspector assignment authorized for field execution.

### 3.5 FE-04 Inspection Execution and Evidence Management

FE-04 provides the assigned Inspector's inspection session, checklist execution, evidence intake, metadata, checksum, duplicate prevention, retry behavior, and authorized MinIO storage.

#### 3.5.1 Execute Inspection and Upload Evidence

**Function trigger:** The assigned Inspector opens an accepted assignment and starts the inspection session.

**Function description:**

- The system records the start time, responsible Inspector, asset, confirmed scope, and checklist version.
- The assigned Inspector can retrieve the published checklist and saved responses through `GET /api/v1/inspections/{inspectionId}/checklist`; checklist responses are saved through the inspection-scoped API and remain attributable to the authenticated Inspector.
- The Inspector performs the field inspection according to the confirmed scope. Manual drone piloting remains outside the platform.
- The Inspector uploads images and documents. The backend validates type and size, calculates a checksum, prevents duplicate records, and stores authorized content in MinIO.
- Web and mobile uploads use the same inspection-scoped API. Available capture time, source (`WEB_UPLOAD`, `MOBILE_UPLOAD`, `SD_CARD`, or `IMPORTED`), GPS, and external reference are stored as metadata. Missing GPS is recorded but does not automatically invalidate evidence.

**Validation and exception requirements:** Unsupported or corrupted files are rejected. Interrupted uploads retry without duplicate evidence records. An Inspector cannot update another Inspector's assignment without a separate authorized role and scope.

**Result:** The inspection has a session record, completed checklist responses, and traceable evidence ready for finding verification.

### 3.6 FE-05 YOLO-Assisted Defect Detection and Verification

FE-05 generates non-official defect candidates from eligible inspection images and requires human verification before findings are used in reports or statistics.

#### 3.6.1 AI Candidate Generation and Review

**Function trigger:** An eligible evidence image is available after upload validation.

**Function description:**

- When YOLO inference is enabled, the configured service receives only eligible authorized images and returns a candidate label, confidence, bounding box, and model version. If inference is disabled or unavailable, evidence remains available and the Inspector can add a manual finding.
- The Inspector reviews every candidate and chooses Confirm, Modify, or Reject.
- The Inspector may manually add a finding that the AI service did not detect.
- Only confirmed, modified, or manually added findings enter official statistics and report content.

**Validation and exception requirements:** AI failure does not discard evidence or prevent manual finding entry. Rejected or unverified candidates remain non-official. An Inspector cannot verify findings outside the assigned inspection scope.

**Result:** The inspection has traceable, Inspector-verified findings that can be used by FE-06.

### 3.7 FE-06 Inspection Report Approval, Conditional Settlement and Internal Dispute Resolution

FE-06 targets versioned technical inspection reports, independent provider peer review, QA release, accepted-contract settlement through an authorized payment partner, and internal complaint handling by `PLATFORM_OPERATOR`. Current implementation and target additions are separated in Report 5; this section does not claim the proposed payment/dispute features are deployed.

#### 3.7.1 Review, Release, Conditional Settlement and Internal Resolution

**Function trigger:** The Inspector completes checklist responses and verified findings.

**Function description:**

- The system compiles a report draft from checklist responses, MinIO evidence, and verified findings.
- The Inspector may request an on-demand AI-assisted narrative draft in `DRAFT` status. The draft is generated by the platform-hosted LLM service from snapshot data and stored for human correction. The Inspector edits the text before submitting for peer review.
- The report is submitted for **Internal Peer Review**: An independent certified Inspector within the same Provider organization verifies evidence support, defect classifications, checklist consistency, and conclusions. *Self-review is strictly prohibited.*
- When technically approved, `PROVIDER_MANAGER` checks deliverable completeness against contractual SOW and formally releases the report to the Client. The review period is a published contractual term, not a statutory five-day period.
- **Client Decision & Proposed Settlement Path**:
  - The Client reviews the report and may accept it, request clarification, or file a supported complaint.
  - If the Client takes no action by the contractually agreed review deadline and no valid clarification/dispute is open, deemed acceptance may apply only if the accepted terms expressly provide it.
  - Acceptance/deemed acceptance makes the report version immutable and marks the inspection `COMPLETED`. The licensed partner settles eligible funds using the uniform Platform-set commission locked on the order: `B = eligible VAT-exclusive Provider service amount − Provider-funded discount − valid VAT-exclusive price refund` (not below zero), `C = r × B`; Provider receives its eligible service proceeds net of `C` and Platform separately invoices `C` plus applicable Platform VAT. Provider still invoices the Client for the full agreed service consideration and applicable Provider VAT.
  - AI YOLO, LLM narrative, data processing, and MinIO are Platform-provided capabilities used by Provider/Client; Provider quotations do not add those as separate Client fees.
- **Dispute Filing & Internal Platform Resolution Path**:
  - Client or Provider may file a contractual complaint over quality, safety, or commercial terms. The licensed partner pauses release of the disputed portion where its product and agreed terms permit; undisputed amounts may be settled.
  - `PLATFORM_OPERATOR` handles the case under the public Platform Terms, comparing SOW and traceable MinIO evidence. Hash/GPS metadata supports integrity but is not automatically conclusive legal evidence.
  - Internal outcomes may include a no-charge reshoot, justified contract termination with a calculated refund, or dismissal and release of eligible funds. Refunds of actual service price reverse proportional commission (`r × refunded VAT-exclusive service price`) and generate the appropriate invoice adjustments. The internal process does not replace court or lawful commercial arbitration.

**Validation and exception requirements:** Internal drafts, rejected AI candidates, and peer-review comments are hidden from customer visibility. Accepted reports are immutable; corrections require a new linked version. Provider cross-organization access and concurrent accept/dispute/settlement must be denied or serialized. The proposed payment and dispute features are not represented as implemented.

**Result:** Target: a verified report with auditable acceptance or internal complaint resolution and a reconciled partner settlement; implementation evidence remains tracked separately.

### 3.8 FE-07 Maintenance, Work Orders and Warranty Retention

FE-07 targets maintenance assessment, versioned work orders, before/after evidence, change control and optional contractual warranty retention. An illustrative 10% retention is neither a statutory requirement nor an implemented payment mechanism; any release uses an authorized partner and does not earn Platform commission twice on the same service value.

#### 3.8.1 Create and Assess Maintenance Ticket

**Function trigger:** The Client selects one or more verified defects from an accepted report and creates a maintenance ticket.

**Function description:**

- The system links the repair ticket to the Client organization, asset, accepted report version, selected defect findings, and supporting evidence.
- The Client specifies priority, preferred deadline, site-access constraints, and special instructions.
- A qualified Maintenance Engineer performs remote or on-site technical assessment, submitting required repair scope, materials, labor hours, duration, and cost range.
- The Engineer must accept the assessment assignment before submitting technical estimates; provider managers do not fabricate technical estimates.

**Validation and exception requirements:** A maintenance ticket must reference at least one verified defect from an accepted report owned by the Client's organization.

**Result:** A traceable technical repair assessment ready for commercial contracting.

#### 3.8.2 Prepare and Approve Maintenance Order with Warranty Retention

**Function trigger:** The Maintenance Engineer submits the technical repair assessment.

**Function description:**

- `PROVIDER_MANAGER` prepares a versioned maintenance quotation based on the assessment.
- Quotations disclose whether the parties adopt warranty retention, its amount/base and release conditions; an illustrative 10% and 30 days are configurable contractual proposals, not legal defaults.
- The Client and Provider approve an electronic **Maintenance Work Order** and its captured Platform commission policy version.
- Where advance funding is agreed, the Client funds the order through the authorized bank/payment partner. Platform does not take custody of deposits.
- `PROVIDER_MANAGER` assigns an active `MAINTENANCE_ENGINEER` for physical execution.

**Validation and exception requirements:** Physical repair execution follows the contract's approved funding and assignment gates; a 100% advance is a proposed commercial option, not a statutory or already-deployed requirement.

**Result:** An approved maintenance order funded in escrow and an accepted execution assignment.

#### 3.8.3 Execute Work, Change Orders and Before/After Proof

**Function trigger:** The assigned Maintenance Engineer opens an accepted execution assignment.

**Function description:**

- The Engineer records physical work progress, material consumption, and labor hours.
- **Mandatory Photo Proof**: The Engineer must capture and upload paired **Before and After photo evidence** to MinIO, substantiating the physical defect remediation.
- If unexpected subsurface damage or cost increases occur, the Engineer pauses extra work and submits a **Change Order**. Work remains halted until the Client approves the change order and deposits supplemental escrow funds.
- The Engineer submits the final work completion package.

**Validation and exception requirements:** Completion submission without paired before and after evidence is rejected. Unapproved work outside scope is prohibited.

**Result:** A verifiable maintenance completion report ready for completion acceptance.

#### 3.8.4 Two-Stage Settlement, Warranty Release and Closure

**Function trigger:** The Maintenance Engineer submits the completion package.

**Function description:**

- `PROVIDER_MANAGER` checks completion evidence against the approved order and releases the result to the Client.
- The Client reviews before/after evidence and selects Accept, Request Rework, or Request Re-inspection:
  - *Acceptance (Stage 1 Settlement)*: The partner settles eligible repair consideration net of the **single order-locked Platform commission `C = r × B`**, holding any expressly agreed warranty retention `H = h × B` under the partner's authorized product; an illustrative `h = 10%` and 30-day warranty are policy options only. The defect transitions to `RESOLVED`.
  - *Request Rework*: Returns the ticket to execution for remediation under the warranty/work-order terms; no additional fee is presumed for correcting defective included work.
  - *Request Re-inspection*: Creates a linked drone inspection request returning to MF2 when the Client contracts a separate verification service.
- **Stage 2 Settlement (Warranty Expiration)**: At the agreed warranty deadline with no unresolved claim, the partner releases `H` to the provider with **no second commission**. Provider service and Platform commission invoices and their VAT follow applicable tax timing, not automatically the cash-release dates.
- If a warranty dispute arises, `PLATFORM_OPERATOR` coordinates internal review; use of the retained amount requires contractual/legal grounds and does not preclude external remedies.

**Validation and exception requirements:** Closing a ticket preserves all assessments, order versions, work logs, before/after evidence, decisions, and audit history.

**Result:** The repair is certified complete, warranty obligations are discharged, and the defect lifecycle is closed.

### 3.9 FE-08 Dashboard, Analytics and Notifications

FE-08 provides role- and scope-filtered dashboards, operational summaries, defect and service analytics, asset history, workload visibility, and workflow notifications. The feature does not expose data outside the authenticated user's organization, ownership, assignment, or release scope.

#### 3.9.1 Scoped Dashboard and Analytics

- `PLATFORM_ADMIN` views platform technical and security audit summaries within authorized scope; does not by default handle Provider commercial decisions.
- `PLATFORM_OPERATOR` views verified Provider/Client operations, complaints and reconciled partner payment statuses within authorized business scope.
- `PROVIDER_MANAGER` views only their Provider organization's requests, accepted quotations, assignments, report release, maintenance work and settlement statements.
- Client views the organization's assets, requests, released reports, maintenance tickets, and invoice or payment status.
- Inspector and Maintenance Engineer view assigned work queues, deadlines, evidence status, and relevant history.

#### 3.9.2 Workflow Notifications

- The system notifies the next responsible actor after material assignments, review decisions, releases, correction requests, deadlines, and Client decisions.
- Notifications do not grant access; every linked page and API request applies the normal authorization and resource-scope checks.
