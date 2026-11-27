---
title: "Report 3 - Functional Requirements"
document_type: report3-srs-section
weight: 35
source: "report3-software-requirement-specification.docx"
---

## 3. Functional Requirements

### 3.1 System Functional Overview

SmartDroneInspection delivers twenty-four atomic product features (`FE-01` to `FE-24`) organized under four connected main flows (`MF1` to `MF4`): identity, partner onboarding, airspace map & financial ledger (`FE-01`–`FE-05`); building assets, restricted-airspace decisions, service requests, quotations, signed agreements, dispatch, messaging, acceptance timeouts & notifications (`FE-06`–`FE-12`); flight permits, live field sessions, evidence processing, AI defect detection & `DroneKnowledgeAI` case/standard retrieval (`FE-13`–`FE-17`); and inspection report publication, acceptance, Sepay/VNPay checkout, payment documents, payouts, refunds & re-inspection verification (`FE-18`–`FE-24`, with `FE-05` surfacing financial ledgers across roles). The product scope is limited to **building structures**; every other infrastructure domain is excluded.

The service is delivered through four web portals, one per login role, and a Customer mobile application. Each portal exposes only the navigation sections its role may reach; a section a role may not use has no route at all rather than being hidden in the interface.

#### 3.1.1 Screens Flow

The application separates its four role-scoped Web portals from its Customer-only Mobile client. After authentication, each user lands strictly inside the portal or mobile navigation flow matching their canonical role (`ADMIN`, `MANAGER`, `CUSTOMER`, or `INSPECTOR`).

##### 3.1.1.1 Web Application Screen Flow

![Web Application Screen Flow Diagram](assets/diagrams/screen-flow-web.png)

Figure 3.1.1 Web Application Screen Flow across Public, Shared, Admin, Manager, Customer, and Inspector portals.

##### 3.1.1.2 Mobile Application Screen Flow

![Mobile Application Screen Flow Diagram](assets/diagrams/screen-flow-mobile.png)

Figure 3.1.2 Mobile Application Screen Flow (Customer App).

#### 3.1.2 Screen Descriptions

The screens below are the implemented application surfaces. Screenshots were captured from the running system with real project assets.

| # | Feature | Screen | Description |
| --- | --- | --- | --- |
| 1 | — | Public landing page | Introduces the service, its workflows, and the entry points to sign-in and registration. |
| 2 | FE-01, FE-04 | Customer account registration | Two-step public form collecting the Customer's account details, contact information, and initial building with interactive map coordinates for airspace screening. |
| 3 | FE-02 | Partner Inspector application | Public form collecting Inspector identity, pilot-licence details, and a licence scan for platform review. Accounts are created only after approval. |
| 4 | FE-01 | Sign-in | Credential sign-in with a one-time-code path and Google sign-in; routes the user to the portal for their role. |
| 5 | FE-01 | Password reset | Sends a one-time code and sets a new password. |
| 6 | FE-01 | Admin dashboard | Platform-wide counts of accounts, applications, buildings, and inspections, with recent activity. |
| 7 | FE-02, FE-03 | Onboarding reviews | Queue of partner Inspector applications and drone registration applications (`MANAGER` decides approve/reject; `ADMIN` read-only oversight view). |
| 8 | FE-01 | Platform accounts | Administrator-managed account list with activation, deactivation, and forced-password-change actions. |
| 9 | FE-06 | Building asset catalogue | Maintains the six building categories available to Customers. |
| 10 | FE-02 | UAV licence classes | Maintains the pilot-licence classes used for assignment qualification. |
| 11 | FE-03 | Required drone documents | Maintains the set of registration, ownership, and technical-inspection documents an Inspector must supply. |
| 12 | FE-20, FE-21 | Finance settings | Maintains the platform commission, VAT, TNCN, and payment-due window settings used in settlement. |
| 13 | FE-08 | Admin service requests | Read-only assignment registry letting `ADMIN` assign, reassign, or unassign Manager request ownership. |
| 14 | FE-06 | Admin buildings | Platform-wide building list across all Customer accounts. |
| 15 | FE-16 | AI settings | Maintains the system-wide AI configuration: automatic defect-confirmation threshold (`70%` default) and secondary vision fallback preference. |
| 16 | FE-14 | Manager dashboard | Workload summary for the Manager's claimed requests, inspections, and reports awaiting review. |
| 17 | FE-08, FE-09 | Manager service requests | Compact four-column queue (`Request & Asset`, `Schedule`, `Stage`, `Action`) with status chips and concise schedule ranges; claiming a request opens its commercial detail panel directly. |
| 18 | FE-10 | Manager messages | Dedicated inbox carrying the order-chat negotiation for assigned requests, with attachments. |
| 19 | FE-06 | Manager buildings | Building records across the Customer accounts the Manager serves. |
| 20 | FE-09, FE-13, FE-14 | Manager inspections | Every inspection occurrence with its assignment, acceptance timeout state, inspector-uploaded permit status (read-only), and delivery state. |
| 21 | FE-18 | Manager reports | Report queue filtered to occurrences whose report is submitted for review or already published. |
| 22 | FE-02 | Partner inspectors | Inspector roster with partner status, pilot-licence class and expiry, and linked drone eligibility. |
| 23 | FE-14, FE-19 | Inspection workspace — tracking | Occurrence summary, lifecycle position, and the role-appropriate next action. |
| 24 | FE-13 | Inspection workspace — permit | Inspector self-attested permit upload with structured metadata, effective immediately once validation passes; Manager/Admin read-only view and audit trail. |
| 25 | FE-14 | Inspection workspace — pre-flight checklist | Configurable pre-flight safety checklist recorded before the session starts. |
| 26 | FE-14 | Inspection workspace — field session | Start, complete, or abort the on-site session with optional `SmartDroneHub` live flight telemetry or log import. |
| 27 | FE-14 | Inspection workspace — post-flight checklist | Configurable post-flight checklist and target building checkpoint completion recorded at closure. |
| 28 | FE-15 | Inspection workspace — evidence | Photograph and video intake, resumable chunked MP4 upload, thumbnail review, and video keyframe extraction. |
| 29 | FE-16, FE-17, FE-24 | Inspection workspace — findings | Candidate defect proposals with confidence, confirmation filter chips, `DroneKnowledgeAI` `Draft note with AI` / batch `Draft all notes` + collapsed `References`, manual findings with bounding box, and three-way re-inspection verification. |
| 30 | FE-17, FE-18 | Inspection workspace — report | Report preparation, AI-drafted summary with `Matched Cases & Standards`, submission, and the published version. |
| 31 | FE-13, FE-14 | Inspection workspace — audit | Attributable permit upload and flight-session decision history for the occurrence. |
| 32 | FE-18, FE-22, FE-23 | Inspection workspace — review and settlement | Independent reviewer decision panel alongside the payout, refund, and receivable ledger. |
| 33 | FE-01, FE-14 | Customer dashboard | Summary of the Customer's buildings, active requests, upcoming inspections, and outstanding payment. |
| 34 | FE-08, FE-09 | Customer service requests | Create a one-time or recurring request and follow it through quotation, acceptance, agreement, and occurrence dispatch. |
| 35 | FE-10 | Customer messages | Unified messages inbox toggling between Manager order-chat threads and assigned-Inspector per-inspection threads. |
| 36 | FE-04, FE-06 | Customer buildings | Building inventory with interactive airspace map, plain-text ownership details, inspection checkpoints, and uploaded reference documents. |
| 37 | FE-14, FE-24 | Customer inspections | Occurrences for the Customer with progress, re-inspection creation, and verdict-expiry alerts. |
| 38 | FE-18, FE-19, FE-20, FE-21 | Customer reports | Published reports available for review, acceptance/clarification, notice/receipt PDF download, and Sepay/VNPay payment. |
| 39 | FE-01, FE-14 | Inspector dashboard | The Inspector's assigned workload, upcoming occurrences, and credential-expiry warnings. |
| 40 | FE-11, FE-14 | Inspector inspections | Assigned occurrences with accept/decline timeout status, readiness state, and entry into the inspection workspace. |
| 41 | FE-03 | My drones | Drone registration applications with photographs, capabilities, checklist items, and uploaded documents. |
| 42 | FE-12 | Notifications | In-app notices with read state, deduplicated per event. |
| 43 | FE-01 | Settings | Profile, security, and notification preferences for the signed-in user. |
| 44 | FE-05 | Financial history ledger | Role-scoped financial ledgers for the Customer (payments and receipts), Inspector (mission fees and net payouts), and Manager (platform revenue, commissions, and taxes). |

![Public landing page](assets/screens/public-landing.png)

Figure 3.1 Public landing page.

![Customer account registration](assets/screens/public-register-customer.png)

Figure 3.2 Customer registration at the account details step.

![Partner Inspector application](assets/screens/public-register-inspector.png)

Figure 3.3 Public partner Inspector application.

![Admin dashboard](assets/screens/admin-dashboard.png)

Figure 3.4 Administrator dashboard.

![Manager onboarding reviews](assets/screens/admin-onboarding-reviews.png)

Figure 3.5 Manager partner onboarding review queue.

![Partner inspectors roster](assets/screens/manager-partner-inspectors.png)

Figure 3.6 Manager partner Inspector roster.

![Manager service requests](assets/screens/manager-service-requests.png)

Figure 3.7 Manager service request queue.

![Customer buildings](assets/screens/client-assets.png)

Figure 3.8 Customer building inventory.

![Inspector inspection workspace — findings](assets/screens/inspector-ws-findings.png)

Figure 3.9 Inspection workspace findings review.

![Manager report review](assets/screens/manager-ws-review.png)

Figure 3.10 Manager report decision and publication readiness.

##### Role-specific screen examples

These screen examples use demonstration accounts and building data. The images include current web captures and retained demonstration states from Report 7. Each screen appears only for an authorized role and an applicable inspection or request state.

![Administrator account directory](assets/screens/adm-platform-accounts.png)

*Figure 3.11 — Administrator account directory (demo data).*

![Administrator building category catalog](assets/screens/adm-asset-catalog.png)

*Figure 3.12 — Administrator building category catalog (demo data).*

![Administrator flight-document configuration](assets/screens/adm-flight-config-documents.png)

*Figure 3.13 — Administrator flight-document configuration (demo data).*

![Administrator audit log](assets/screens/adm-audit-logs.png)

*Figure 3.14 — Administrator audit log (demo data).*

![Manager request and dispatch workspace](assets/screens/mgr-request-quote-dispatch.png)

*Figure 3.15 — Manager request and dispatch workspace (demo data).*

![Manager request conversations](assets/screens/mgr-messages.png)

*Figure 3.16 — Manager request conversations (demo data).*

![Manager inspection queue](assets/screens/mgr-inspections.png)

*Figure 3.17 — Manager inspection queue (demo data).*

![Manager field audit](assets/screens/mgr-ws-audit.png)

*Figure 3.18 — Manager field audit (demo data).*

![Manager financial history](assets/screens/mgr-finance-history.png)

*Figure 3.19 — Manager financial history (demo data).*

![Inspector drone inventory](assets/screens/ins-my-drones.png)

*Figure 3.20 — Inspector drone inventory (demo data).*

![Inspector inspection queue](assets/screens/ins-inspections.png)

*Figure 3.21 — Inspector inspection queue (demo data).*

![Inspector flight permit stage](assets/screens/ins-ws-permit.png)

*Figure 3.22 — Inspector flight permit stage (demo data).*

![Inspector pre-flight checklist](assets/screens/ins-ws-preflight.png)

*Figure 3.23 — Inspector pre-flight checklist (demo data).*

![Inspector field session](assets/screens/ins-ws-flightsession.png)

*Figure 3.24 — Inspector field session (demo data).*

![Inspector post-flight checks](assets/screens/ins-ws-postflight.png)

*Figure 3.25 — Inspector post-flight checks (demo data).*

![Inspector evidence workspace](assets/screens/ins-ws-evidence.png)

*Figure 3.26 — Inspector evidence workspace (demo data).*

![Inspector view of a published report](assets/screens/ins-ws-report.png)

*Figure 3.27 — Inspector view of a published report (demo data).*

![Customer building detail](assets/screens/cus-asset-detail.png)

*Figure 3.28 — Customer building detail (demo data).*

![Customer service requests](assets/screens/cus-service-requests.png)

*Figure 3.29 — Customer service requests (demo data).*

![Customer inspection progress](assets/screens/cus-inspection-tracking.png)

*Figure 3.30 — Customer inspection progress before Manager publication (demo data).*

![Customer published report](assets/screens/cus-inspection-report.png)

*Figure 3.31 — Customer published report (demo data).*

![Customer settlement](assets/screens/cus-inspection-settlement.png)

*Figure 3.32 — Customer settlement (demo data).*

![Mobile Customer home](assets/screens/mob-home.png)

*Figure 3.33 — Mobile Customer home (demo data).*

![Mobile Customer service requests](assets/screens/mob-requests.png)

*Figure 3.34 — Mobile Customer service requests (demo data).*

![Mobile Customer inspection progress](assets/screens/mob-inspection-detail.png)

*Figure 3.35 — Mobile Customer inspection progress (demo data).*

![Mobile Customer published report](assets/screens/mob-inspection-report.png)

*Figure 3.36 — Mobile Customer published report (demo data).*

#### 3.1.3 Screen Authorization

The matrix below states which roles may use each screen. A visible screen is not by itself permission to act: Customer ownership, work assignment, qualification, and separation of duties are enforced in addition to role. A section a role may not use is not routed for that role at all. The last two rows record the data-scope rule that applies across every screen.

| Screen | `ADMIN` | `MANAGER` | `CUSTOMER` | `INSPECTOR` |
| --- | :---: | :---: | :---: | :---: |
| Public landing, registration, Inspector application | X | X | X | X |
| Sign-in, password reset, account settings | X | X | X | X |
| Dashboard | X | X | X | X |
| Onboarding reviews | X | X |  |  |
| Platform accounts | X | X |  |  |
| Partner inspectors roster |  | X |  |  |
| Building asset catalogue | X |  |  |  |
| UAV licence classes | X |  |  |  |
| Required drone documents | X |  |  |  |
| Finance settings / Operations settings / AI settings | X |  |  |  |
| Service requests | X | X | X |  |
| Messages (Order chat, Partner chat & Inspection chat) |  | X | X | X |
| Buildings | X | X | X |  |
| Inspections | X | X | X | X |
| Reports | X | X | X | X |
| Financial history ledger |  | X | X | X |
| My drones |  |  |  | X |
| Notifications | X | X | X | X |
| Query All Data | X | X |  |  |
| Query Own Data |  |  | X | X |

`Query All Data` means the role may list records across the whole platform or across every Customer account it serves. `Query Own Data` means the list is restricted to the acting user's own Customer account or own work assignment. `ADMIN` and `MANAGER` are additionally subject to the ownership and assignment rules in §5.1; a Manager sees only requests they hold, and an Inspector sees only occurrences assigned to them.

#### 3.1.4 Non-Screen Functions

These capabilities have no dedicated screen of their own; they run inside a user action, on a schedule, or in response to a domain event.

| # | Feature | System Function | Description |
| --- | --- | --- | --- |
| 1 | FE-01 | One-time-code issue and verify | Issues and validates short-lived codes for registration, sign-in, and password reset, with per-IP rate limiting. |
| 2 | FE-01 | Session issuance and refresh rotation | Issues access and refresh credentials, rotates the refresh token, and records the prior hash so a replayed token can be detected. |
| 3 | FE-02 | Pilot-licence expiry sweep | A scheduled job that flags Inspectors whose licence has lapsed and notifies them and the platform. |
| 4 | FE-04 | Airspace position screening | Compares a building's coordinates with the configured airspace zones and returns a prohibited, review-required, or clear outcome. |
| 5 | FE-06 | Building-inspection item seeding | Generates the default inspection checkpoints for a building from its category on registration and stores plain-text building ownership details. |
| 6 | FE-09 | Occurrence materialization | Creates the individual inspection occurrences covered by an accepted recurring agreement with month-end anchoring. |
| 7 | FE-09 | Schedule-conflict detection | Detects overlapping Inspector or drone commitments across all Customer accounts before assignment. |
| 8 | FE-08, FE-09 | Quotation validity evaluation | Revalidates pilot licence and drone registration against every scheduled occurrence before a quote is saved or accepted. |
| 9 | FE-11 | Assignment acceptance timeout monitor | Scheduled job that automatically cancels unaccepted assignments after the administrator-configured response deadline, frees crew schedules, returns the occurrence for reassignment, and notifies the owning Manager. |
| 10 | FE-12 | Duplicate-notification suppression | Ensures retried lifecycle events produce at most one notification per intended recipient. |
| 11 | FE-13 | Permit re-upload required | Invalidates the inspector-uploaded permit and requires a fresh inspector upload when the drone is changed or the schedule moves outside the permit window. |
| 12 | FE-14 | Inspection lifecycle monitor | A scheduled job that advances or flags occurrences whose scheduled window has passed without the expected session activity. |
| 13 | FE-14 | Flight-log import and normalisation | Parses an imported SRT, CSV, KML, or GPX log and normalises available position, time, altitude, speed, heading, and battery values, marking absent fields as unavailable. |
| 14 | FE-15 | Image normalization and thumbnailing | Extracts available capture metadata, normalises oversized or rotated photographs, and generates a 480 px thumbnail alongside the original. |
| 15 | FE-15 | Asynchronous video processing | Converts uploaded inspection video into a web-playable format with a poster thumbnail in the background, retaining the original until processing succeeds. |
| 16 | FE-15 | Duplicate evidence disambiguation | Detects a repeated filename in an inspection and saves it with a sequential suffix rather than rejecting the upload. |
| 17 | FE-16 | Candidate defect inference | Runs the automated building-defect detection model and optional secondary vision fallback over evidence and records candidate defects with confidence scores (`70%` default auto-confirm setting). |
| 18 | FE-17 | Knowledge indexing & retrieval preparation | Indexes confirmed findings automatically when a report is published and maintains semantic similarity search with automatic keyword-matching fallback. |
| 19 | FE-17, FE-18 | Advisory narrative & note drafting + structured report compilation | Generates advisory finding notes or single-shot executive summary with matched references, while official report sections assemble consistently from confirmed findings. |
| 20 | FE-20 | Payment gateway callback verification | Verifies the cryptographic signature or authenticated service credentials of a Sepay or VNPay callback before treating a payment as settled. |
| 21 | FE-21 | Invoice & overdue reminder scan | Captures commercial rate snapshots when a report is accepted, sets the payment due date, and sends a single overdue reminder without revoking report access. |
| 22 | FE-22, FE-23 | Payout hold & allocation reconciliation | Enforces refund holds on unpaid payouts, requires balanced refund allocations after external transfer, and tracks separate Inspector receivables for post-payout refunds. |

#### 3.1.5 Entity Relationship Diagram

Figure 3.37 presents the conceptual Entity Relationship Diagram for the building-inspection domain across identity, buildings, partner onboarding, contracting, field operations, AI/knowledge retrieval, reporting, ratings, and financial settlement. The physical relational database schema, column definitions, constraints, and migration inventory are specified in Report 4 §2.

![Conceptual Entity Relationship Diagram (Chen)](assets/erd.png)

Figure 3.37 Conceptual Entity Relationship Diagram (Chen).

**Entities Description**

| # | Entity | Description |
| --- | --- | --- |
| 1 | User Account | Platform account holding a single canonical role, security lockout state, and per-user preference for secondary AI vision fallback. |
| 2 | Authentication Session | Active sign-in session tracking credential rotation and revocation state. |
| 3 | One-Time Verification Code | Short-lived verification code issued for registration, sign-in, or password reset with attempt limits and expiry. |
| 4 | Audit Event | Attributable record of an important governance, commercial, operational, or financial decision with actor, action, target, and timestamp. |
| 5 | Pilot Licence Class | Catalogue of recognized pilot-licence classes used to qualify an Inspector for an aircraft weight category. |
| 6 | Building Category | Catalogue of the six building structural categories available to Customers. |
| 7 | Building Asset | Customer-owned building with location coordinates, airspace classification, plain-text ownership details (up to 1,000 characters), structural specifications, and lifecycle state. |
| 8 | Building Reference Document | Engineering blueprint or reference file attached to a building with integrity checksum verification. |
| 9 | Inspection Checkpoint | Specific structural inspection checkpoint defined for a building or service request. |
| 10 | Checklist Template | Configurable pre-flight and post-flight safety checklist item. |
| 11 | Drone | Inspector-owned registered aircraft carrying model, serial number, weight category, capabilities, and serviceability state. |
| 12 | Drone Document Requirement | Administrator-configured rule defining required and optional drone compliance documents. |
| 13 | Drone Capability Configuration | Administrator-configured catalogue of drone capabilities and safety checklist items. |
| 14 | Drone Registration Application | Inspector drone registration or renewal submission together with supporting compliance documents and Manager review outcome. |
| 15 | Inspection Occurrence | Individual scheduled building inspection carrying lifecycle status, assigned Inspector and drone, checkpoints, and timing. |
| 16 | Mission Flight Permit | Inspector self-attested flight-permit submission with document integrity metadata, validity window, altitude limit, and audit trail. |
| 17 | Field Session | On-site field work session recording start, safety confirmations, completion or abort outcome, and reviewer audit notes. |
| 18 | Field Session Sortie | Individual flight sortie recorded within a field session, linked to its flight data record. |
| 19 | Flight Telemetry | Recorded flight metrics, GPS trace, and synchronized flight video for a field session. |
| 20 | Inspection Evidence | Field photograph or video capture with processing status, capture metadata, and derived video keyframe lineage. |
| 21 | Video Upload Session | Resumable chunked upload tracking record for large inspection videos. |
| 22 | Defect Finding | Candidate or Inspector-confirmed building defect with category, bounding region, notes, and advisory confidence score where model-produced. |
| 23 | Inspection Report | Versioned inspection deliverable with lifecycle status, review feedback, advisory summary, and published PDF archive reference. |
| 24 | Inspector Reliability Event | Assignment timeout or aborted-session reliability record attributed to an Inspector. |
| 25 | Re-inspection Verification | Post-remediation verification outcome (`Resolved`, `Unresolved`, or `Inconclusive`) linking an original defect to fresh follow-up evidence and validity expiry. |
| 26 | Service Request | One-time, recurring, or re-inspection request raised for a building by its owning Customer and managed by a claimed Manager. |
| 27 | Service Quotation | Current VND quotation stating inspection scope, schedule window, required drone capabilities, and per-occurrence fee. |
| 28 | Service Occurrence | Planned inspection visit materialized under an accepted service request, linking the commercial term to execution and settlement. |
| 29 | Order Chat Message | Commercial negotiation message and optional file attachments exchanged between Customer and assigned Manager. |
| 30 | Partner Chat Message | Private pre-dispatch coordination message and optional attachments exchanged between assigned Manager and assigned Inspector. |
| 31 | Inspection Chat Message | Site-access coordination message and optional attachments exchanged between Customer and assigned Inspector for an inspection. |
| 32 | Service Invoice | Financial obligation record generated per occurrence from accepted commercial terms and configured tax/commission rates. |
| 33 | Service Payment | Customer payment attempt and settlement record tracking gateway order reference, due date, overdue notice state, and refund totals. |
| 34 | Payment Callback Audit Record | Deduplicated log of inbound payment-gateway notifications for reconciliation and prevention of duplicate settlement. |
| 35 | Service Refund | Refund record tracking pending payout hold, external bank-transfer reference, and five-part accounting allocation. |
| 36 | Inspector Payout | Partner disbursement record tracking eligibility on report approval, payout hold status, and settled VietQR/wire transfer reference. |
| 37 | Inspector Receivable | Recoverable partner balance created when a customer refund follows an already-disbursed payout. |
| 38 | Receivable Recovery | Attributable collection record reducing an outstanding Inspector receivable. |
| 39 | Finance Settings | Platform-level rates for commission, VAT, personal income tax (TNCN), and default payment due window. |
| 40 | AI Settings | Platform-level automated defect-detection configuration including auto-confirm threshold and secondary vision fallback controls. |
| 41 | Operations Settings | Platform-level operations configuration including the assignment-acceptance timeout window. |
| 42 | Partner Inspector Application | Public self-service partner application with pilot-licence scan and Manager approval/rejection decision. |
| 43 | Inspector Profile | Approved partner Inspector profile holding qualification details, signed partner agreement reference, and receiving bank account. |
| 44 | Imported Flight Log | Imported third-party flight track or accountable manual flight declaration preserved with source provenance. |
| 45 | Notification | Deduplicated bilingual in-app or email alert scoped to an authorized recipient with read-state tracking. |
| 46 | Engineering Standard Reference | Searchable engineering standard excerpt used by `DroneKnowledgeAI` for grounding defect notes and summaries. |
| 47 | Historical Defect Case | Customer-isolated historical defect case or anonymized benchmark example used for advisory comparison. |
| 48 | Inspector Rating | Post-completion evaluation of an assigned Inspector submitted by the Customer or Manager within the configured edit window. |
| 49 | Rating Criterion | Administrator-configured evaluation criterion scoped by rater role (`CUSTOMER` or `MANAGER`). |

The table summarizes the domain's conceptual entities across identity, buildings, partner onboarding, commercial workflow, field operations, AI/knowledge retrieval, reporting, ratings, and financial settlement.

#### 3.1.6 Main Operational Flows (Activity Diagrams)

The five activity diagrams below illustrate the end-to-end operational behavior across `MF1A`, `MF1B`, `MF2`, `MF3`, and `MF4`, matching the implemented roles, gates, and settlement lifecycle.

![MF1A Customer Onboarding Activity Diagram](assets/diagrams/act-mf1a-customer-onboarding.png)

Figure 3.38 Activity Diagram — `MF1A` Customer Onboarding & Airspace Screening.

![MF1B Partner and Drone Onboarding Activity Diagram](assets/diagrams/act-mf1b-partner-drone.png)

Figure 3.39 Activity Diagram — `MF1B` Partner Inspector & Drone Onboarding.

![MF2 Commercial Contracting and Dispatch Activity Diagram](assets/diagrams/act-mf2-commercial-dispatch.png)

Figure 3.40 Activity Diagram — `MF2` Commercial Contracting & Dispatch.

![MF3 Permit, Field Execution and AI Activity Diagram](assets/diagrams/act-mf3-permit-field-ai.png)

Figure 3.41 Activity Diagram — `MF3` Self-Attested Permit, Field Execution & AI Analysis.

![MF4 Report, Finance and Reinspection Activity Diagram](assets/diagrams/act-mf4-report-finance-reinspection.png)

Figure 3.42 Activity Diagram — `MF4` Report Publication, Payout, Settlement & Re-inspection.

---

### 3.2 `MF1` — `FE-01` Account Authentication, OTP & 4-Role Access Control

- **Function trigger**: A prospective Customer registers a Customer account and its first building, a user signs in by password/OTP/Google, updates profile information, resets password, or ends an active session, or `ADMIN` manages platform accounts.
- **Actors**: All Roles (`ADMIN`, `MANAGER`, `CUSTOMER`, `INSPECTOR`); prospective Customer; automated identity service.
- **Function description**: Authenticate users securely across web and mobile portals, maintain refresh-token rotation and IP lockout controls, and enforce strict four-role access and scope separation across every role workspace and service action.
- **Screen layout (mock-up)**: Public landing, customer registration, credential/OTP/Google sign-in, password reset, Admin platform accounts console, and Account settings (`Profile` / `Security` / `Notification` tabs). See Figure 3.2 and Figure 3.4.
- **Requirements**:
  - Recognized human login roles are `ADMIN`, `MANAGER`, `CUSTOMER`, and `INSPECTOR`. Every user holds exactly one role.
  - Password sign-in locks an account for fifteen minutes after five consecutive failed attempts; sign-in and one-time-code actions enforce per-IP rate limiting.
  - Consolidated OTP challenges (registration, sign-in, password reset) expire after their window, enforce attempt caps, and reject reuse after consumption.
  - Federated Google Sign-In authenticates verified active accounts and issues a rotated user session for web portals or the Customer mobile application.
  - Authenticated users may update their own full name and phone number in Account Settings; email and role remain read-only. Security-sensitive changes (password change, deactivation, role update) revoke active sessions while retaining attributable history.
  - `CUSTOMER` access is restricted to its own buildings and records, `INSPECTOR` to its own assigned occurrences and owned drones, `MANAGER` to claimed requests and operational oversight, and `ADMIN` to platform governance (without bypassing separation of duties or issuing quotes/reports). Denied sections present no routes or actions in web or mobile interfaces.
- **Normal cases**: Authorized users sign in with password + OTP or Google, land on their single role portal, manage profile/password/sessions cleanly, and cannot reach unauthorized portal paths.
- **Abnormal cases**: Repeated invalid credentials trigger temporary lockout; excessive request bursts are throttled; replayed sessions or consumed OTP codes are refused; cross-role or cross-customer access attempts are blocked (`BR-01`, `BR-02`).

---

### 3.3 `MF1` — `FE-02` Partner Inspector Application & Qualification Management

- **Function trigger**: A prospective partner Inspector submits a public application, or `MANAGER` reviews it, records the signed partner contract, or updates qualification records (`ADMIN` retains read-only visibility).
- **Actors**: Public applicant, `MANAGER`, `INSPECTOR`, `ADMIN` (read-only view).
- **Function description**: Admit qualified partner drone pilots through a platform-reviewed self-service application (without requiring drone ownership at signup) and maintain pilot licence classes, expiry dates, scans, signed partner contracts, and flight logs.
- **Screen layout (mock-up)**: Multi-step public Inspector application form, Onboarding Reviews queue (`Inspector Applications` tab), Partner Inspectors roster, Admin UAV Licence Classes screen, and Inspector profile security/qualification panel. See Figure 3.3 and Figure 3.6.
- **Requirements**:
  - Public application collects identity, contact details, pilot-licence number, recognized licence class, future expiry date, and a verified licence scan stored in private object storage.
  - Submission creates no login account immediately. Only an attributable approval decision by `MANAGER` provisions an active `INSPECTOR` account and qualification profile together; rejection requires a written reason and notifies the applicant (`BR-09`), while `ADMIN` has read-only audit visibility.
  - Applicant emails must be unique across existing accounts and open pending applications.
  - Drone ownership is not a precondition of partner admission (`BR-08`). After admission, `MANAGER` records the offline signed partner contract scan against the approved application, and `INSPECTOR` or `MANAGER` may renew licence details while `MANAGER` records flight history logs.
  - A scheduled licence-expiry sweep checks active Inspector licences and flags lapsed credentials, sending duplicate-free alerts and blocking dispatch readiness until renewed (`BR-10`).
- **Normal cases**: A prospective Inspector submits complete licence details and scan; `MANAGER` inspects the scan, approves the application (provisioning the account), and records the signed partner contract.
- **Abnormal cases**: Duplicate email, missing/corrupt licence scan, expired licence at application time, unrecognized licence class, rejection without reason, or non-`MANAGER` approval/contract-upload attempt (including `ADMIN`) is rejected.

---

### 3.4 `MF1` — `FE-03` Inspector-Owned Drone Registration & Fleet Management

- **Function trigger**: An approved `INSPECTOR` submits, renews, maintains, or retires an owned drone, or `ADMIN` configures required drone documents and capability checklists, or `MANAGER` reviews a pending drone application (`ADMIN` retains read-only queue visibility).
- **Actors**: `INSPECTOR`, `MANAGER`, `ADMIN` (config & read-only view).
- **Function description**: Maintain administrator-configurable drone compliance rules and allow partner Inspectors to register owned drones with photographs, outdoor capabilities, and required documents for `MANAGER` review prior to mission dispatch.
- **Screen layout (mock-up)**: Inspector `My drones` fleet inventory and registration modal, Onboarding Reviews `Drone Registrations` tab, and Admin Flight & Drone Configuration (`Required Documents` and feature checklist tabs). See Figure 3.5.
- **Requirements**:
  - `ADMIN` maintains required and optional drone compliance documents (registration and ownership documents active and required by default; technical inspection document configurable) and configurable drone capability/safety checklist items (`BR-11`).
  - Inspector submissions require identifying serial, model, and manufacturer data, at least one real aircraft photograph, outdoor flight capabilities (wind resistance, optical zoom, thermal/RTK), selected safety checklist items, and all required supporting documents.
  - Aircraft weight categories follow Decree 288/2025/ND-CP Article 4; airframes at `>= 2.0 kg` require the assigned Inspector to hold a recognized Class B pilot licence (Article 27), whereas Class A covers known airframes `< 2.0 kg`. Unknown weight or unknown licence class fails eligibility (`BR-12`).
  - Duplicate serial numbers belonging to another owner or submitting a second pending update while one is already pending review are rejected.
  - Inspectors may renew active drone registrations or switch owned drone serviceability between Active, In Maintenance, and Retired (and reactivate a previously retired aircraft, while Admin-suspended drones remain locked and retired drones cannot submit renewal applications while retired). Only active, approved, non-expired drones owned by the assigned Inspector are selectable at dispatch (`BR-13`).
- **Normal cases**: `ADMIN` configures required documents; Inspector registers a `DJI` aircraft with real photos and required files; `MANAGER` approves the drone, enabling assignment.
- **Abnormal cases**: Missing photo or required document, duplicate external serial, Class A pilot paired with heavy drone, expired registration, retired/suspended serviceability, or non-`MANAGER` approval/rejection attempt (including `ADMIN`) blocks progression.

---

### 3.5 `MF1` — `FE-04` Interactive Location Map & No-Fly Zone Airspace Screening

- **Function trigger**: A Customer pins an initial building location during account registration or adds/edits a building, or any authorized user evaluates coordinates and altitude against Vietnam airspace zones.
- **Actors**: Public applicant, `CUSTOMER`, `ADMIN`, `MANAGER`, `INSPECTOR`, `SYSTEM`.
- **Function description**: Screen building and mission coordinates against platform-configured prohibited (`No-Fly Zone`), restricted (`Restricted Zone`), and clear (`Clear Zone`) airspace regions using interactive maps on Web and Mobile alongside server-side distance checks.
- **Screen layout (mock-up)**: Interactive coordinate picker modal on the Web portal, customer registration step-2 map preview, and mobile airspace advisory summary card. See Figure 3.2 and Figure 3.8.
- **Requirements**:
  - Airspace evaluation validates latitude (`[-90, 90]`) and longitude (`[-180, 180]`), measures proximity against active airspace polygons, and classifies locations into Clear Zone, Restricted Zone, or No-Fly Zone.
  - Coordinates falling inside a No-Fly Zone block self-service Customer registration and building creation.
  - Coordinates in a Restricted Zone attach advisory warning `MSG28` (naming the zone, authority, altitude ceiling, and `cambay.mod.gov.vn`) while permitting immediate registration (`FE-07`) and building creation/update.
  - Every UI surface explicitly states that airspace screening is an internal advisory check and does not grant statutory or military aviation clearance (`BR-06`, `BR-26`, `MSG27`, `MSG28`).
- **Normal cases**: User selects coordinates on the interactive map, inspects live zone classification and buffers, and proceeds when outside prohibited airspace.
- **Abnormal cases**: Out-of-bounds coordinates fail validation; prohibited zone coordinates fail closed and never create an active building.

---

### 3.6 `MF4` — `FE-05` Financial History & Revenue/Payment Ledger

- **Function trigger**: An authenticated `CUSTOMER`, `INSPECTOR`, or `MANAGER` opens their role-scoped financial history view or inspects per-occurrence invoice/payment/payout summaries.
- **Actors**: `CUSTOMER`, `INSPECTOR`, `MANAGER`.
- **Function description**: Provide each non-admin operational role with a dedicated, permission-scoped financial ledger tracking Customer payments and downloadable receipts, Inspector net payouts and deductions, and Platform Manager revenue, commissions, VAT/TNCN taxes, and refund adjustments.
- **Screen layout (mock-up)**: Dedicated role-scoped Financial History ledger pages and occurrence financial detail panels across Customer, Inspector, and Manager portals.
- **Requirements**:
  - Customer view lists only occurrences belonging to the signed-in Customer account, displaying agreed VND totals, invoice/VAT breakdown, payment due date/status, gateway transaction reference, and receipt download actions, while hiding internal partner payout and receivable figures.
  - Inspector view lists only occurrences assigned to the signed-in Inspector, showing mission gross amount, platform commission (`15%`), personal income tax (TNCN) withholding, hold status, and net disbursed payout reference.
  - Manager view aggregates platform inflows, earned commission revenue, VAT/TNCN totals, and occurrence-level payout, refund, and receivable summaries for managed occurrences.
  - Unauthenticated users or callers attempting to read another Customer's or unassigned occurrence's financial record are refused (`BR-02`, `BR-04`).
- **Normal cases**: Customer audits historical payments/receipts, Inspector verifies net earnings and TNCN deductions, and Manager reconciles platform revenue and commission totals.
- **Abnormal cases**: Cross-role or cross-customer ledger queries (such as a Customer opening Manager revenue totals or an Inspector inspecting a colleague's occurrence) are rejected.

---

### 3.7 `MF2` — `FE-06` Building Asset Registry, Checkpoints & Reference Documents

- **Function trigger**: `ADMIN` maintains the six building categories. `CUSTOMER` creates, updates, uploads reference documents for, or retires a building. `MANAGER` or `ADMIN` views authorized building records.
- **Actors**: `CUSTOMER`, `ADMIN`, `MANAGER`.
- **Function description**: Maintain the building-only asset inventory, category-seeded inspection checkpoints, plain-text ownership metadata, and duplicate-free engineering reference documents under the airspace gate.
- **Screen layout (mock-up)**: Customer `Assets` register and detail view, New/Edit Building modal, Admin `Asset Catalog` and category dialog, and Admin/Manager building directories. See Figure 3.8.
- **Requirements**:
  - Supported asset categories are restricted exclusively to the six platform-managed **building categories**. Non-building infrastructure categories cannot be registered (`BR-07`, `MSG23`). Updating a category does not retroactively mutate existing buildings' checkpoints.
  - Building ownership details are stored as dedicated plain text (up to `1,000` characters) alongside structural specifications so users can enter readable ownership notes directly without special formatting.
  - Asset creation validates a unique building code for the owning Customer, enforces the No-Fly Zone gate (`FE-04`), and seeds default inspection checkpoints from the chosen category. Customer building screens on web and mobile omit checkpoints, while authorized staff can view the checkpoint list in web building detail. The owning Customer may update building checkpoints only before the first inspection exists; once an inspection exists, checkpoint edits are rejected.
  - Reference documents compute cryptographic file checksums, reject empty or duplicate-checksum files for the same building, store files in private storage, and allow download exclusively after ownership and role authorization checks.
  - Retiring an active building preserves all historical inspections while blocking new service requests.
- **Normal cases**: Customer creates an active building with plain-text ownership details, uploads unique PDF/PNG CAD blueprints, and later retires it. The system seeds checkpoints from the selected category, and authorized staff can review them in the web building detail.
- **Abnormal cases**: Duplicate building code, duplicate file checksum, empty file, prohibited coordinates, post-inspection checkpoint mutation, another Customer's document read, or service request on a retired building is rejected.

---

### 3.8 `MF1` — `FE-07` Restricted Airspace Advisory Warning & Immediate Onboarding

- **Function trigger**: A prospective Customer registers an account with an initial building in a restricted airspace zone, a Customer creates/edits a building or service request in a restricted zone, or `MANAGER`/`INSPECTOR` views building and inspection airspace advisories.
- **Actors**: Prospective Customer, `CUSTOMER`, `MANAGER`, `INSPECTOR`, `SYSTEM`.
- **Function description**: Surface amber `MSG28` advisory warnings (zone name, governing authority, ceiling altitude `<= X m AGL`, and `https://cambay.mod.gov.vn` reference) whenever building coordinates lie in restricted airspace, activating accounts immediately without a pre-registration Administrator approval queue while enforcing the hard No-Fly Zone gate (`FE-04`) and the Inspector mission flight-permit gate (`FE-13`).
- **Screen layout (mock-up)**: Coordinate picker and Customer registration map amber `Alert` banner (`MSG28`), post-registration notice on Sign-In (Web & Mobile), Service Request inline alert, and Building/Overview `Restricted airspace · <= Xm AGL` badge.
- **Requirements**:
  - Customer registration whose initial building coordinates fall in restricted (or unclassified) airspace after valid OTP activates the `CUSTOMER` account and initial building immediately while returning the airspace classification and advisory notice (`MSG28`) instead of holding the account for pre-approval.
  - Coordinates falling inside a No-Fly Zone fail closed and prevent registration, building creation, and building updates.
  - Airspace screening serves uniformly as an immediate warning-only advisory check on Restricted Zones and a hard block on No-Fly Zones across all portals and mobile.
- **Normal cases**: Customer pins restricted-zone coordinates, sees the amber `MSG28` permit-requirement banner, activates the account and building immediately after OTP verification, sees the amber reminder when creating a Service Request, and Inspector/Manager view the restricted-airspace badge prior to mission permit upload (`FE-13`).
- **Abnormal cases**: Pinning No-Fly Zone coordinates disables submission in the interface and rejects creation on the server; malformed or out-of-range coordinates fail validation.

---

### 3.9 `MF2` — `FE-08` Service Requests (One-Time & Recurring) & VND Quotations

- **Function trigger**: A `CUSTOMER` creates a one-time or recurring request for an active building; an active `MANAGER` claims it (or `ADMIN` assigns/reassigns Manager ownership); and the `MANAGER` issues and updates a VND quotation.
- **Actors**: `CUSTOMER`, `MANAGER`, `ADMIN` (assignment oversight only).
- **Function description**: Capture one-time and monthly recurring inspection demand with deterministic scheduling bounds, single-Manager request ownership, and active VND quotation negotiation.
- **Screen layout (mock-up)**: Compact 4-column desktop request list (`Request & Asset`, `Schedule`, `Stage`, `Action`) with service-type chip, compact time range (`08:00 – 17:00`), occurrence count summary, clickable outer/inner role-scoped Overview (`Asset` detail modal and compact numbered `Checkpoints` modal), immediate detail opening after Manager claim, quote summary card, and streamlined Manager `Request review` / quote workspace embedding a compact single-row **Inspection Checkpoints** summary + popup configurator. See Figure 3.7.
- **Requirements**:
  - One-time requests specify a single date; recurring requests specify `1–120` month intervals and either `2–100` occurrences or an end date yielding `2–100` occurrences (`BR-17`). Auto-generated titles use concise readable patterns (such as `<Building> · Monthly inspection`).
  - First requested inspection date must be at least `20` calendar days ahead in Vietnam business time (`Asia/Ho_Chi_Minh`, `BR-18`).
  - Managers claim unassigned open requests safely without race conditions; claiming opens the commercial detail workspace immediately. Only the assigned `MANAGER` may view negotiation details or quote/dispatch; `ADMIN` sees an assignment oversight registry to assign, reassign, or unassign Managers with audit logging and never quotes or negotiates (`BR-03`, `BR-05`).
  - The assigned Manager may cancel an open or quoted request that cannot proceed. An accepted request cannot be cancelled through this action.
  - The assigned `MANAGER` configures per-request **Inspection Checkpoints** inside the `Request review` popup before any occurrence is dispatched (alongside or prior to saving the quotation). Existing building checkpoints act as selectable suggestions alongside `ADMIN`-configured building-category templates and custom items. Once any occurrence is dispatched, or the request becomes assigned or cancelled, checkpoint edits are locked.
  - `MANAGER` maintains a single active VND quotation per request using explicit start and end date-time schedule inputs. The first quoted occurrence may be on or after the Customer-requested start date but never earlier. A one-time quote may move to a later date; an end-date recurring quote keeps the Customer-selected end date and must retain `2–100` occurrences; a count-based recurring term shifts with the new first date. Any date change requires a revised quote and explicit Customer acceptance (`BR-14`, `BR-16`, `BR-19`). The quote deliberately does not select a partner Inspector or drone; partner eligibility is evaluated for the concrete occurrence during dispatch (`FE-09`).
  - Request Overview cards adapt strictly by role (`MANAGER` sees Asset specs, Customer, Manager, Location, Checkpoints, Schedule, Team/Drone, Price, Contract; `CUSTOMER` omits internal asset specs while retaining clickable Asset and Checkpoints modals plus read-only assigned `MANAGER` contact info without direct `Email`/`Call` action buttons).
- **Normal cases**: Customer creates a recurring request; Manager claims it, configures per-request checkpoints from building suggestions, category templates, or custom entries via the `Request review` popup, saves a VND quote with start/end date-times (moving the first inspection later when required), and Customer reviews and accepts the revised terms while inspecting compact Asset and Checkpoints popups in Overview.
- **Abnormal cases**: Start date inside 20-day lead time, multi-day range on a one-time request, fewer than 2 or more than 100 recurring occurrences, a quote earlier than the Customer-requested date, an end-date recurring revision that leaves fewer than two occurrences, checkpoint mutation by an unassigned Manager or after dispatch starts, concurrent Manager claim (`MSG31`), or `ADMIN` commercial mutation attempt is refused. An expired partner credential at dispatch of a planned occurrence is rejected by `FE-09`.

---

### 3.10 `MF2` — `FE-09` Offline Signed Contract & Occurrence Dispatch Scheduling

- **Function trigger**: A `CUSTOMER` accepts the active VND quotation, `MANAGER` uploads the executed offline paper contract scan, and `MANAGER` dispatches eligible Inspector/drone pairs to materialized occurrences (or recovers an aborted field session).
- **Actors**: `CUSTOMER`, `MANAGER`, `INSPECTOR`, Automated System.
- **Function description**: Lock accepted commercial terms into an immutable snapshot, materialize recurring inspection occurrences, record offline signed paper contracts, and dispatch qualified Inspectors and owned drones without cross-customer double-booking.
- **Screen layout (mock-up)**: Quote acceptance action, four-stage Contract Lifecycle Stepper, Signed Paper Contract card, Partner Candidate selection table (clear spaced columns and clean detail icon preventing button overlap), `Apply this team to the remaining` bulk modal, and Manager abort recovery dialog (`Reschedule`, `Reassign`, `Cancel`).
- **Requirements**:
  - Quotation acceptance verifies the latest quote version, stores an immutable snapshot of agreed terms (`BR-16`), and creates each inspection occurrence from the accepted first date using month-end date clamping (`Jan 31 -> Feb 28/29 -> Mar 31`). A revised first date is only effective after the Customer accepts the updated quote. Partner Inspector and drone eligibility is evaluated at dispatch (`BR-19`), not frozen into the quote.
  - `MANAGER` uploads the offline signed agreement (`PDF`/`DOCX`/`JPEG`/`PNG`) to private storage, moving the request to `Contract Signed`; dispatch is refused until the signed contract is recorded (`BR-15`).
  - Before dispatching any occurrence, the system verifies active Inspector status, valid pilot licence matching the drone's Decree 288 weight class, active owned approved drone with current registration, and zero cross-customer schedule conflicts (`BR-21`, `BR-22`). Dispatch propagates the request-configured inspection checkpoints onto the created inspection occurrence for flight documentation and report compilation, falling back to the building's default checkpoints only when the request has no custom selection.
  - Recurring engagements support bulk assignment (`Apply this team to the remaining`), validating each remaining unassigned occurrence independently and reporting skipped conflicts cleanly.
  - The assigned Manager may cancel an individual occurrence after contract signing, subject to the inspection and settlement states. A fully cancelled contracted request no longer blocks a new request for the building.
  - When the Inspector withdraws before field work, the inspection remains scheduled with the assignment marked declined and flagged as requiring Manager reassignment. The assigned Manager can reassign the crew or cancel the occurrence with a reason. Cancellation cancels the occurrence, clears the reassignment flag, and preserves both the Inspector's withdrawal reason and the Manager's cancellation reason.
  - Reassignment of an accepted occurrence returns it to pending Inspector acceptance, while reassigning an inspection whose field work is already completed is blocked. Following an aborted field session, `MANAGER` records an attributable reschedule, reassign, or cancellation (`BR-27`).
- **Normal cases**: Customer accepts quote -> occurrences materialize -> Manager uploads signed paper contract -> Manager dispatches eligible crew (single or bulk) cleanly -> occurrences enter `Scheduled` (`Pending Acceptance`).
- **Abnormal cases**: Dispatch before signed contract upload, conflicting Inspector or drone schedule for another Customer, expired credentials at occurrence start, unowned drone, or reassigning after field completion is rejected.

---

### 3.11 `MF2` — `FE-10` Messaging (Order Chat, Partner Chat & Inspection Chat)

- **Function trigger**: Customer and assigned Manager exchange pre-contract commercial messages on a request; Customer and assigned Inspector exchange per-inspection site-access messages on a dispatched occurrence; or the assigned Manager and an assigned/active Partner Inspector coordinate execution details in a private per-request **Partner Chat**.
- **Actors**: `CUSTOMER`, `MANAGER`, `INSPECTOR`.
- **Function description**: Provide strictly isolated contextual chat channels — commercial **Order Chat** (Customer ↔ assigned Manager), operational **Inspection Chat** (Customer ↔ assigned Inspector), and partner coordination **Partner Chat** (assigned Manager ↔ assigned Inspector per service request) — with verified attachment validation and read receipts.
- **Screen layout (mock-up)**: Unified Customer `Messages` inbox switching between `Service requests` (Order Chat) and `Inspector` (Inspection Chat) tabs; Manager `Messages` inbox switching between `Customers` (Order Chat) and `Inspectors` (Partner Chat) tabs plus a Step 4 Dispatch `Messages` entry; Inspector `Messages` inbox switching between `Customers` (Inspection Chat) and `Managers` (Partner Chat) tabs; and Customer Mobile chat screens.
- **Requirements**:
  - **Order Chat** exclusively connects the owning Customer and the single assigned Manager on that service request.
  - **Inspection Chat** exclusively connects the owning Customer and the assigned Inspector on that inspection occurrence, remaining completely isolated from commercial pricing and explicitly inaccessible to `ADMIN` and `MANAGER`.
  - **Partner Chat** exclusively connects the request's assigned `MANAGER` and an `INSPECTOR` linked to an occurrence on that service request (or currently dispatched to that Customer), remaining completely inaccessible to `CUSTOMER`, `ADMIN`, uninvolved Managers, and uninvolved Inspectors.
  - All three channels enforce a message body limit (`<= 4,000` characters, optional only when attachments exist) and up to `5` verified attachments (`PNG`/`JPG`/`WEBP`/`PDF`/`DOCX`, `10 MiB` per file and `20 MiB` total per message) stored privately with integrity checksums and file-type validation (`MSG34`).
  - `ADMIN` and uninvolved Managers, Inspectors, or other Customers are refused read, write, and attachment download access. Chat messages never alter quotation terms (`BR-41`).
- **Normal cases**: Customer negotiates quote terms with Manager in Order Chat; Manager coordinates dispatch logistics with the assigned Inspector in Partner Chat; Inspector coordinates rooftop access with Customer in Inspection Chat on Web or Mobile.
- **Abnormal cases**: Oversized/disallowed attachment types (`MSG34`), blank text with zero files (`MSG02`), Customer or `ADMIN` attempting to read/post in Partner Chat, Manager attempting to read Inspection Chat, or another Customer's download request fails closed.

---

### 3.12 `MF2` — `FE-11` Assignment Acceptance Timeout & Escalation Handling

- **Function trigger**: A dispatched inspection remains awaiting partner acceptance longer than the administrator-configured acceptance window without an Inspector response, or `ADMIN` updates the timeout setting.
- **Actors**: `ADMIN`, `MANAGER`, `INSPECTOR`, `SYSTEM`.
- **Function description**: Enforce a bounded response deadline for partner inspection assignments so unaccepted missions automatically release crew schedules and escalate back to the owning Manager.
- **Screen layout (mock-up)**: Admin Operations Settings (`1–720` hours, default `24`h), Inspector assignment accept/decline actions, Manager contracts/inspections warning badges, and escalation deep-link notifications.
- **Requirements**:
  - `ADMIN` configures the assignment acceptance deadline (`1–720` hours, default `24` hours) in Operations Settings. Non-administrators cannot change this setting.
  - When a dispatched occurrence in `Pending Acceptance` exceeds the configured timeout window from its assignment timestamp, the scheduled timeout monitor atomically cancels the unaccepted inspection, clears the crew reservation, returns the occurrence to `Pending Assignment` (reopening an assigned parent request so a new crew can be chosen), and records which Inspector timed out and when.
  - Duplicate-free timeout escalation notifications alert both the owning `MANAGER` (linking straight to the request detail for reassignment) and the timed-out `INSPECTOR`, plus an audit entry.
  - The assigned Inspector can withdraw an accepted assignment with a non-blank reason while the inspection is scheduled and field work for the current assignment has yet to start. An open session blocks withdrawal, and an aborted or closed session from an earlier assignment does not block withdrawal of a new assignment.
- **Normal cases**: Admin sets timeout policy; if an Inspector fails to respond within the window, the monitor cleanly unassigns the occurrence, notifies Manager and Inspector, and enables immediate crew re-dispatch.
- **Abnormal cases**: The system rejects timeouts below `1` or above `720` hours, refuses acceptance after timeout cancellation, refuses withdrawal while a field session is open, and blocks withdrawal once field work has started for the current assignment even after an abort.

---

### 3.13 `MF2` — `FE-12` System Notifications & Alert Center

- **Function trigger**: Operational lifecycle events occur across contracts and finance (request created, Manager assigned/reassigned/unassigned, quote issued/updated/accepted, signed contract uploaded, report accepted, payout settled, refund or receivable updated), inspections and reports (assignment issued/accepted/declined/cancelled/timed out/rescheduled/overdue, flight permit uploaded, field session completed or aborted, video processing ready/failed, report submitted/returned/withdrawn/approved/published, clarification requested, Inspector rated), fleet and onboarding (drone submitted/approved/rejected, 30/7/1/0-day drone registration and pilot-licence expiry reminders, partner application updated/approved/rejected), or account security (account status/role change, password change/reset, bulk session revocation), or a user opens Notifications or chat inboxes.
- **Actors**: All Login Roles (`ADMIN`, `MANAGER`, `CUSTOMER`, `INSPECTOR`), `SYSTEM`.
- **Function description**: Deliver reliable, deduplicated, role- and scope-isolated in-app notifications, bulk mark-all-as-read synchronization, localized unread counters across all three chat channels and in-app alerts, and critical email notices for onboarding, expiry, and security events.
- **Screen layout (mock-up)**: Top-bar Notification Bell unread badge and popover, localized Notifications inbox on Web and Customer Mobile, category badges, **Mark all as read** action (covering in-app alerts and all three chat channels), and role-appropriate deep links to the linked record.
- **Requirements**:
  - Lifecycle transitions emit transactional notifications asynchronously and deduplicate per intended recipient and event key so retried background jobs never generate duplicate alerts (`NFR-06`).
  - Critical bilingual (Vietnamese and English) in-app alerts cover all five operational pillars: contracts and finance, inspections/video/reporting, drone and licence compliance, partner onboarding, and account security.
  - For critical milestones (partner application decisions, 30/7/1/0-day drone registration and licence expiry reminders, and account security changes), the platform also dispatches best-effort bilingual email notifications when mail delivery is configured, without failing or rolling back core business transactions if mail delivery is unavailable.
  - Web and Mobile views render notification titles and bodies cleanly in the user's active locale (`vi` or `en`); marking all notifications as read updates unread state and timestamps consistently across devices.
  - The Notification Bell and Notifications view aggregate unread counts across all three chat channels (Order Chat, Inspection Chat, and Partner Chat), open only permitted destination tabs for the user's role, and enforce server-side role, Customer ownership, and assignment authorization (`BR-52`).
- **Normal cases**: Domain transitions produce one bilingual notice per authorized recipient even on retry; critical milestones also send best-effort email alerts; Web and Mobile display the user's locale cleanly; selecting **Mark all as read** clears unread badges and deep links navigate directly within authorized scope.
- **Abnormal cases**: Replayed events or scheduled daily expiry scans never insert duplicate notifications; mail-server unavailability logs a warning without failing core workflow persistence; reading or marking another user's notifications or navigating to an unauthorized or external redirect target is refused.

---

### 3.14 `MF3` — `FE-13` Flight Permit Upload & Inspector Self-Attestation Gate

- **Function trigger**: An assigned `INSPECTOR` uploads or replaces the aviation flight permit in Workspace Stage 1; a drone change or an out-of-window reschedule invalidates the current permit and requires an inspector re-upload.
- **Actors**: `INSPECTOR` (uploader and accountable self-attestor), `MANAGER`, `ADMIN` (read-only view and audit trail), `SYSTEM`.
- **Function description**: Enforce documented mission flight-permit submission (`<= 25 MB`, verified file signature & integrity checksum, structured permit metadata). The assigned Inspector uploads the permit and is responsible for it; the upload becomes effective immediately once validation passes, with no Manager or Admin approval. A valid, effective permit gates the start of any on-site field session, and Manager/Admin access is limited to read-only viewing and the audit trail.
- **Screen layout (mock-up)**: Inspector Workspace Stage 1 has the permit form with **Save flight permit** and an optional **Withdraw from assignment** action. Manager/Admin can read the permit and audit trail.
- **Requirements**:
  - Permit upload is restricted to the assigned `INSPECTOR` while the inspection is scheduled; the service verifies a non-empty file (`<= 25 MB`), valid file signature (`PDF`/`PNG`/`JPG`/`WEBP`), integrity checksum, permit number, issuing authority, validity dates covering the planned mission schedule, maximum altitude when supplied (`1–2,000 m`), assigned drone serial number match, and active pilot licence plus drone registration (`BR-23`). The Inspector's upload is the self-attestation that these details are accurate.
  - A restricted zone with a configured ceiling requires an approved maximum altitude and rejects omitted values or altitudes exceeding the zone ceiling.
  - A permit that passes validation becomes effective immediately with no `Pending Review` state and no `MANAGER`/`ADMIN` approval or rejection action; airspace classification (including `Clear Zone`) never changes this rule (`BR-24`).
  - `MANAGER` and `ADMIN` have read-only access to the permit and its audit trail only: they cannot approve, reject, or verify it. Permit actions remain attributable to the assigned Inspector (`BR-51`).
  - Reassigning a different drone or rescheduling outside the permit's validity window invalidates the permit and requires the assigned `INSPECTOR` to re-upload a valid permit (`BR-25`, `MSG42`). Upload or replacement is locked once field work begins.
  - The Flight Permit stage shows **Withdraw from assignment** only while the Inspector is eligible to withdraw prior to field work. The confirmation requires a reason. Successful withdrawal returns the Inspector to the inspections list and routes the occurrence to the Manager for reassignment or cancellation (`FE-09`, `FE-11`).
  - After acceptance, the Inspector workspace header shows the **Restricted Zone** badge without its altitude suffix. Pre-acceptance guidance appears while the assignment is awaiting a response. The permit form still requires the maximum altitude for a restricted zone with a configured ceiling.
- **Normal cases**: Inspector uploads a valid permit PDF with matching drone serial and validity dates; the permit is effective immediately, unlocking Stage 2 Pre-flight and Session Start, and the upload is recorded in the audit trail; Manager/Admin can view it read-only.
- **Abnormal cases**: Corrupt/oversized/mismatched file, missing or invalid metadata, permit dates outside the mission window, drone serial mismatch, or replacement after field start is rejected; invalidating changes (a different drone or an out-of-window reschedule) require a fresh inspector re-upload; no permit approve/reject/review action exists for any role.

---

### 3.15 `MF3` — `FE-14` On-Site Field Session & Flight Telemetry

- **Function trigger**: Assigned `INSPECTOR` completes pre-flight checklist and starts/completes/aborts a field session, connects read-only `SmartDroneHub` flight telemetry, imports an offline log, submits a manual flight declaration, or users open Dashboards / Calendar.
- **Actors**: `INSPECTOR`, `MANAGER`, `CUSTOMER`, `ADMIN`, `SmartDroneHub`.
- **Function description**: Execute accountable on-site field sessions gated by valid inspector-uploaded permits and safety checklists, capture read-only flight telemetry/traces and mission MP4 video (or log/manual fallbacks without fabrication), handle aborts, and surface operational schedule/dashboard views.
- **Screen layout (mock-up)**: Pre-flight safety checklist tab, Flight Operation console (with live `SmartDroneHub` telemetry & gimbal status), Post-flight target building checkpoint verification, four-role Dashboards, and the Inspector Schedule Calendar.
- **Requirements**:
  - Session start verifies that the inspection is scheduled, a valid inspector-uploaded permit is in effect and covers the actual flight time, the assigned drone serial matches, pilot/drone credentials remain current, the detailed drone-agnostic pre-flight safety checklist (8 pre-flight checks) plus a non-blank safety note are completed (`BR-23`, `BR-26`), and no other session is already active.
  - Active sessions support recording multiple flights/sorties with telemetry linked per sortie, and while an inspection remains `Field Completed` prior to findings baseline confirmation, the assigned Inspector may open additional field sessions/days and inspect aggregated multi-day totals.
  - Active sessions may optionally connect to `SmartDroneHub` in strictly read-only telemetry mode (flight status, mode, GPS coordinates, altitude, speed, heading, battery, waypoint, and gimbal status; never sending flight actuation commands `BR-30`), saving the flight trace and synchronizing mission MP4 video.
  - Only the assigned Inspector may read live telemetry during an active session. The owning Customer can follow inspection progress and may read flight summaries and traces once the inspection report is published.
  - When live telemetry is absent, Inspectors may import `SRT`, `CSV`, `KML`, or `GPX` flight logs (`<= 15 MB`) preserving missing fields as unavailable without fabrication, or submit an accountable manual flight declaration (reason, duration, altitude, note) clearly badged separately from measured telemetry (`BR-28`).
  - Completion records the detailed post-flight safety checklist (4 post-flight checks) and building checkpoints and moves the mission to `Field Completed`. Aborting requires a written reason (`BR-27`), records a reliability event against the Inspector, reopens the inspection to `Scheduled`, and notifies Managers. Role-scoped Dashboards count only confirmed findings, and the Inspector Schedule Calendar shows Month/Week/Agenda views with abort alerts.
- **Normal cases**: Inspector completes pre-flight checks, connects live telemetry via SmartDroneHub, flies mission, completes post-flight items -> `Field Completed`.
- **Abnormal cases**: Starting without a valid inspector-uploaded permit (`MSG37`, `MSG40`), expired permit/credentials, corrupt/position-less log import (`MSG45`), or missing safety/abort notes is rejected.

---

### 3.16 `MF3` — `FE-15` Field Evidence Intake & Chunked Video Processing Pipeline

- **Function trigger**: Assigned `INSPECTOR` uploads photographs or large MP4 videos, promotes video keyframes, or authorized users view thumbnails/stream playback via scoped tickets.
- **Actors**: `INSPECTOR`, `MANAGER`, `CUSTOMER`, `ADMIN`, `SYSTEM`.
- **Function description**: Handle reliable field photograph and large MP4 video intake with capture-metadata preservation, image normalization, resumable chunked uploads, background playback transcoding, duplicate filename auto-numbering, and secure time-limited media streaming.
- **Screen layout (mock-up)**: Inspector Workspace Stage 5 (`Evidence`) upload dropzone, chunked upload resume queue, Evidence grid with thumbnails/metadata/GPS map dialog, and video player with keyframe capture dialog.
- **Requirements**:
  - Photographs (`<= 10 MB`) preserve available capture metadata (GPS, timestamp, orientation) before upright resizing to a maximum `2,048 px` side length and generating a `480 px` thumbnail. Missing camera metadata is disclosed rather than fabricated (`BR-31`, `BR-33`).
  - Videos (`<= 2 GiB`) upload through resumable `10 MiB` chunks, retaining the raw upload safely until background conversion produces a web-playable `1080p` MP4 rendition and a `480 px` poster image (failed conversions remain retryable, `NFR-06`).
  - Duplicate filenames within the inspection auto-number cleanly (`name (1).ext`, `name (2).ext`) and notify the uploader (`MSG17`, `BR-32`).
  - Extracted video keyframes (`<= 1280×720`) promote into standalone linked evidence items. Stored media streams only through short-lived (`5-minute`) signed media tickets bound strictly to one evidence record and authorized user scope, supporting seekable playback (`NFR-05`).
- **Normal cases**: Inspector uploads crisp building photos and large MP4 inspection footage (resuming cleanly if network drops), extracts keyframes, and authorized reviewers stream 1080p video smoothly.
- **Abnormal cases**: Oversized or corrupt image, unsupported file type, requesting playback before video processing finishes (`MSG43`), expired or tampered playback token, or cross-customer stream attempt fails closed.

---

### 3.17 `MF3` — `FE-16` AI Defect Detection & Findings Confirmation

- **Function trigger**: Assigned `INSPECTOR` triggers batch/single image detection or video frame detection, filters candidates, edits/accepts/rejects/adds manual findings, or confirms the findings baseline; or `ADMIN` configures AI threshold.
- **Actors**: `INSPECTOR`, `ADMIN`, Automated Defect Detection Service, Optional Secondary Vision Fallback.
- **Function description**: Run automated building-defect detection across five structural defect classes (`crack`, `leakage`, `abscission`, `corrosion`, `bulge`) with optional secondary Vision fallback and require explicit Inspector human confirmation before findings become official.
- **Screen layout (mock-up)**: Stage 6 (`Findings`) toolbar (`All active`, `Unconfirmed`, `Confirmed` status filter chips; `Analyze all images`), annotated bounding-box finding cards, Admin `AI Settings` (`70%` default threshold), and Profile vision-fallback opt-out toggle.
- **Requirements**:
  - Automated detection runs the primary building-defect model; if the primary detector is unavailable or returns no detections and the acting user allows secondary fallback, an OpenAI-compatible Vision model runs automatically. Users who opt out in Account Settings never invoke external Vision fallback.
  - Candidate findings start as unconfirmed advisory proposals unless the administrator-configured auto-confirm threshold (`70%` default) applies. Re-analyzing replaces only unreviewed pending suggestions while preserving already-confirmed findings.
  - Inspectors can add manual findings (with no invented AI confidence score, `BR-36`) and draw or adjust normalized defect bounding boxes on imagery.
  - Confirming the findings baseline requires zero unreviewed pending findings (or explicit zero-defect acknowledgement) (`BR-34`, `BR-35`). Any subsequent edit to findings or evidence clears the confirmation lock until re-confirmed, and findings become read-only once a report is submitted or published.
- **Normal cases**: Inspector runs batch AI detection, filters `Unconfirmed` proposals, inspects boxes, adds any missed defect manually, and confirms the official findings baseline.
- **Abnormal cases**: Unauthorized caller running detection, confirming while unreviewed proposals remain (`MSG21`), editing findings while a report is under review, or complete detector outage still allows full manual finding entry.

---

### 3.18 `MF3` — `FE-17` AI Case & Standard Retrieval, Note Drafting & Report Summary

- **Function trigger**: `INSPECTOR` views finding references or clicks `Draft note with AI` / batch `Draft all notes`, or generates an inspection report's AI Executive Summary, or Customer opens Mobile inspection detail, or a report publishes.
- **Actors**: `INSPECTOR`, `CUSTOMER`, `MANAGER`, `ADMIN`, Automated System (`DroneKnowledgeAI`, Advisory Narrative Service).
- **Function description**: Ground Inspector finding notes and report summaries in customer-isolated historical defect cases and seeded engineering standards (`TCVN 9343:2012`, `TCVN 9361:2012`, `EN 1504-9`, `ISO 12944-5`, `ASTM C1583`) using multilingual semantic similarity with automatic keyword-matching fallback (`BR-55`).
- **Screen layout (mock-up)**: Finding-card `Draft note with AI` button + collapsed `References` disclosure, toolbar `Draft all notes (N)`, report `AI Executive Summary` with `Matched Cases & Standards` footer, and Customer Mobile collapsible matched-references strip.
- **Requirements**:
  - **Recommendations & Note Drafting**: Each finding displays up to three matched historical cases or engineering standards and lets the Inspector generate a localized bilingual draft note individually (`Draft note with AI`) or in batch (`Draft all notes`), indicating whether semantic similarity or keyword fallback was used. Drafted notes populate only the editable input field and never auto-save or auto-confirm findings (`BR-34`, `BR-55`).
  - **Customer Isolation**: Historical case matching restricts results strictly to the current Customer account plus anonymized benchmark cases (`6` benchmark cases with zero customer personal data), and always excludes the current inspection from matching itself (`BR-55`).
  - **Indexing & Fallback**: Semantic similarity search indexes newly confirmed findings automatically when a report is published (including re-inspection resolution outcomes). If the semantic search service is unavailable, retrieval degrades cleanly to keyword-based matching without blocking workflows.
  - **Report Summary Grounding**: The inspection report summary retrieves up to four compact matched historical cases and engineering standard references for reader context (`BR-43`, `BR-55`), while Customer Mobile hides the strip cleanly when no references apply. Corrective-maintenance repair knowledge bases remain out of scope.
- **Normal cases**: Inspector drafts bilingual standard-grounded technical notes individually or in batch, reviews references, and generates an executive summary linked to matched cases/standards; Customer sees matched standards read-only on published deliverables.
- **Abnormal cases**: Cross-customer case exposure, self-matching within the current inspection, or temporary retrieval service unavailability (handled by automatic keyword fallback or `MSG19`) never blocks findings or reporting workflows.

---

### 3.19 `MF4` — `FE-18` Inspection Report Compilation, Independent Review & Official Publication

- **Function trigger**: Assigned `INSPECTOR` opens Report tab / prepares & submits a report version after findings confirmation, or an independent `MANAGER` approves, publishes, or returns a submitted version (`ADMIN` retains read-only visibility), or an authorized reader downloads the rendered PDF.
- **Actors**: `INSPECTOR`, `MANAGER`, `CUSTOMER`, `ADMIN` (read-only view).
- **Function description**: Consistently compile versioned inspection reports from confirmed findings and field telemetry, enforce independent non-author `MANAGER` review (`Submitted`, `Returned`, `Approved`, `Published`, `Superseded`), publish immutable official versions, and generate A4 PDFs on demand without buffering video bytes.
- **Screen layout (mock-up)**: Stage 7 (`Report` authoring panel with single-shot advisory narrative draft & PDF preview), Manager `Reports` review queue, Manager Workspace `Review` screen (Approve / Return-with-Reason and Publish; `ADMIN` sees read-only inspection without decision actions), and Customer `Reports` archive. See Figure 3.10.
- **Requirements**:
  - **Compilation & Submission**: Report sections compile consistently from a fixed numbered structure using only confirmed findings, evidence metadata, and field session data once the findings baseline is confirmed (`BR-37`); opening the screen never submits automatically, and report generation never loads video files into memory (`NFR-05`, `NFR-06`). Authors may request a single advisory narrative draft clearly marked advisory (`BR-43`) before explicitly submitting the report for review.
  - **Independent Review & Publication**: Only a `MANAGER` who is not the report author independently approves and publishes the report (after commercial Inspector payout settlement in `FE-22`) or returns it with a mandatory written reason (`BR-38`, `BR-42`, reverting the inspection for revision); `ADMIN` holds read-only view access only and cannot review or publish. Previously published versions become `Superseded` while remaining preserved in history (`BR-40`).
  - **Customer Visibility & PDF**: Customers see only `Published` report versions (never `Submitted`, `Returned`, or un-published `Approved` drafts, `BR-39`). Normalized evidence photographs and confirmed findings render on demand into cached A4 PDFs stored privately.
- **Normal cases**: Inspector prepares report `v1`, edits optional advisory summary, and submits; another Manager reviews side-by-side evidence/findings, approves it, settles Inspector payout (`FE-22`), and publishes `v1` -> Customer downloads official PDF.
- **Abnormal cases**: Submitting before findings confirmation (`MSG33`), author attempting self-review or self-publication (`BR-38`), `ADMIN` or non-`MANAGER` attempting review/publication, returning without reason (`MSG15`), or Customer requesting an unpublished draft fails closed.

---

### 3.20 `MF4` — `FE-19` Customer Report Acceptance & Clarification Workflow

- **Function trigger**: An owning `CUSTOMER` inspects a published inspection report version on Web or Mobile and chooses to accept the official deliverable or request clarification/revision before acceptance.
- **Actors**: `CUSTOMER`, `MANAGER`, `INSPECTOR`.
- **Function description**: Record explicit Customer acceptance of a specific published report version to unlock billing settlement, and restrict pre-acceptance clarification requests strictly to the owning Customer account.
- **Screen layout (mock-up)**: Customer Web official report deliverable viewer and settlement card, Manager/Inspector acceptance badge, and Customer Mobile `Report` & `Settlement` tabs (`#1: Accept official report`).
- **Requirements**:
  - Accepting a report verifies that the referenced version is `Published`, records acceptance against that exact version, stamps the acceptance timestamp on the invoice, and transitions payment status to `Payment Due` (`BR-44`).
  - Before acceptance, only the owning `CUSTOMER` may submit a pre-acceptance clarification request (`MANAGER`, `ADMIN`, `INSPECTOR`, or another Customer cannot invoke clarification or acceptance). Acceptance cannot occur on unpublished versions or twice on an already-accepted occurrence.
  - Once an inspection reaches `Completed` with an assigned Inspector, the owning `CUSTOMER` (on Web or Customer Mobile) and `MANAGER` may each submit at most one Inspector rating scored `1–5` overall and across `ADMIN`-configured role criteria, editable within `7` days of creation. Aggregate rating summaries appear on Partner Candidate selection and Inspection detail while Customer views hide other Customers' comments, and submitting a rating notifies Stakeholders (`FE-12`).
- **Normal cases**: Owning Customer reviews published `v1` on Web or Mobile, optionally sends pre-acceptance clarification, clicks **Accept report** to move cleanly into settlement, and rates the Inspector after completion.
- **Abnormal cases**: Non-owning Customer, Manager, Admin, or Inspector invoking acceptance or clarification, accepting an unpublished/superseded version, or submitting clarification or rating edits outside the permitted window is rejected.

---

### 3.21 `MF4` — `FE-20` Online Service Fee Payment (`Sepay` VietQR & `VNPay`)

- **Function trigger**: After report acceptance (`Payment Due`), Customer initiates `Sepay` VietQR or `VNPay` checkout, payment gateways send verified confirmation callbacks, or Manager confirms manual payment / clears an unpaid gateway order.
- **Actors**: `CUSTOMER`, `MANAGER`, `Sepay`, `VNPay`.
- **Function description**: Process VND inspection fee settlement through configuration-gated online payment gateways with verified callback authentication and safe fallback to authorized manual confirmation.
- **Screen layout (mock-up)**: Step 2 of Customer Settlement card on Web and Customer Inspection detail on Mobile (Sepay VietQR dialog with copyable transfer code or VNPay launch), Customer/Manager unpaid-order reset action, Manager manual wire confirmation, and Finance Settings gateway switches.
- **Requirements**:
  - Initiating online checkout is allowed only after report acceptance (`Payment Due`) and validates whole-VND payable totals. Online checkout supports Sepay VietQR and VNPay across Web and Customer Mobile: Sepay generates a VietQR payment code carrying the occurrence transfer code and authenticates incoming bank-transfer notifications, checking the receiving account number, rejecting mismatched transfer amounts, and persisting every processed notification without duplicate settlement; Web and Mobile clients display the QR and bank details, refresh status automatically, and close cleanly once `Paid`. VNPay verifies its callback cryptographic signature (`BR-45`) and redirects Web or Customer Mobile back to the settlement screen, confirming settlement only after verified server-side confirmation (`Paid`), and receipt PDFs render the recorded settlement confirmation timestamp.
  - Switching between unpaid online gateways (Sepay or VNPay) or retrying checkout while `Payment Due` automatically releases the superseded unpaid online order reference so customers move smoothly between VietQR and VNPay without manual resets; unresolved manual wire orders remain guarded (`MSG49`, `BR-47`). Cancelled or timed-out online orders also release automatically, while any late or superseded callbacks are logged in the payment audit ledger for reconciliation without double-settling. Assigned Managers and owning Customers retain explicit unpaid-order cleanup actions when needed.
  - Both gateways may be disabled by configuration; when enabled in `Payment Due` after report acceptance, an authorized `MANAGER` may also record an attributable manual wire confirmation. Partner Inspector payout eligibility is governed independently by Manager report approval (`BR-46`).
- **Normal cases**: Customer pays via Sepay VietQR or VNPay -> verified callback arrives -> payment marks `Paid` and stakeholders are notified (`MSG47`).
- **Abnormal cases**: Payment attempt before report acceptance, switching gateway while a manual wire order is still pending (`MSG49`), forged callback credentials/signature or mismatched transfer amount, or duplicate/superseded gateway callback is handled cleanly without double-counting.

---

### 3.22 `MF4` — `FE-21` Payment Deadlines, Invoices & Payment Document Management

- **Function trigger**: Customer report acceptance creates/stamps an invoice and due deadline; a daily background check monitors unpaid due windows; or an authorized Customer, Manager, or assigned Inspector downloads the payment notice or receipt PDF.
- **Actors**: `CUSTOMER`, `MANAGER`, `INSPECTOR`, `SYSTEM`.
- **Function description**: Snapshot financial rates onto per-occurrence invoices, enforce configurable payment-due deadlines with a single overdue reminder without revoking report access, and generate role-scoped non-tax-invoice payment notice and receipt PDFs. The published report PDF is an inspection record: it is available to in-scope actors from publication onward, independent of payment status.
- **Screen layout (mock-up)**: Payment-due countdown badge on Customer/Manager views, settlement invoice rate breakdown (commission, VAT, personal income tax, due days), and **Download payment notice / receipt PDF** actions across Web and Mobile.
- **Requirements**:
  - Every service invoice captures the agreed VND price plus configured platform commission, VAT, and personal income tax (TNCN) percentages at creation time.
  - Accepting a report stamps the payment due date as `accepted date + configured window` (`15` days by default). When an unpaid invoice passes its due date, the system sends at most one overdue reminder notification to the owning Customer and active Managers; overdue status never revokes access to the published report or alters `Payment Due` state. Payment status never gates the published report PDF or Partner Inspector payout eligibility: an unpaid Customer receives the same immutable artefact as any other in-scope actor, and payment produces the Customer receipt only.
  - Requesting the payment document PDF is refused before report acceptance (`MSG48`), renders an internal A4 Payment Notice while payment is due (showing due date & VAT breakdown), and renders a Payment Receipt once paid (showing method, transaction reference, and timestamp). Both documents carry a non-VAT-tax-invoice notice, never mutate payment state, and are restricted to the owning Customer, assigned Inspector, `MANAGER`, and `ADMIN`.
- **Normal cases**: Customer reads the published report and its official PDF from publication onward, accepts it (`due +15d` stamped), downloads the notice PDF, pays later, and downloads the verified receipt PDF on Web or Mobile.
- **Abnormal cases**: Requesting payment document before report acceptance (`MSG48`), another Customer or unassigned Inspector requesting the document, or repeated daily checks firing duplicate overdue alerts is prevented cleanly.

---

### 3.23 `MF4` — `FE-22` Partner Inspector Payout Reconciliation

- **Function trigger**: `MANAGER` approves the submitted inspection report (`Approved`), opening payout eligibility (`Eligible`) and prompting Manager to settle the Inspector payout (`Paid`) before publishing the report to Customer (`Published`). The owning `MANAGER` generates a Sepay VietQR payout code targeting the Inspector's registered bank account and transfers net earnings via banking app; an authenticated outgoing transfer notification confirms settlement automatically (with manual bank transfer recording available as a fallback).
- **Actors**: `MANAGER`, `INSPECTOR`, `CUSTOMER`.
- **Function description**: Enforce a two-step Manager approval-to-publish gate so Partner Inspector disbursement is settled in a dedicated Manager workflow step before Customer deliverable publication, require Inspectors to configure a standardized VietQR bank account prior to disbursement, support automatic Sepay VietQR payout reconciliation, maintain strict separation between payout eligibility and actual partner disbursement, enforce payout holds and net reductions, and mask internal partner settlement fields from Customer views.
- **Screen layout (mock-up)**: Four-stage Manager inspection workspace (`1. Field Audit -> 2. Report Decision -> 3. Inspector Payout -> 4. Customer Settlement`), where Step 3 (`Inspector Payout`) displays net payout breakdown alongside the Inspector's registered bank details (standardized bank display, copyable account number and amount), Sepay VietQR brand emblem and `Pay Inspector via SePay (VietQR)` action opening the QR and transfer-code confirmation dialog, and the unlocked `Publish to Customer` action; complemented by `Inspector payouts` with the same Sepay VietQR payout modal, and Inspector bank-account configuration forms using standardized VietQR bank selections.
- **Requirements**:
  - Approving a submitted report locks the version at `Approved`, advances Manager to Step 3 (`Inspector Payout`), and immediately sets the Inspector's payout status to `Eligible` with no transfer reference (hidden from `CUSTOMER`); a payout transitions to `Paid` when Sepay delivers an authenticated outgoing transfer confirmation matching the payout order reference and rounded integer VND net payout (`BR-46`), or via an attributable manual bank-transfer record. Publishing (`Approved -> Published`) is blocked until the linked occurrence's payout is `Paid`.
  - Inspectors configure their complete receiving bank details (standardized VietQR bank name, account number, account holder, and optional branch) before any payout link or disbursement can be created, never falling back to a platform merchant account. Manager, Admin, and Inspector views display those bank details cleanly while Customer views always mask them.
  - Final payable amount is capped after verified refund reductions (`FE-23`), and any active pending refund or unreconciled historical refund holds payout disbursement until resolved or released.
  - Finance views hide internal platform commission, personal income tax (TNCN), payout references, bank account details, and receivable/recovery ledgers from `CUSTOMER` users while showing Manager/Inspector-permitted fields cleanly.
- **Normal cases**: Inspector selects a VietQR bank from the standardized list and saves account details -> Manager approves submitted report (`Approved`) -> Step 3 (`Inspector Payout`) shows net payout and Inspector bank details -> Manager initiates `Pay Inspector via SePay (VietQR)` -> scans QR or transfers with the generated order reference -> verified outgoing transfer confirmation marks payout `Paid` automatically -> Manager clicks `Publish to Customer` (`Published`) and advances to Step 4 (`Customer Settlement`).
- **Abnormal cases**: Attempting to publish an `Approved` report before Inspector payout is `Paid`, generating a Sepay payout QR or settling payout before Inspector configures complete bank details, outgoing callback from a mismatched source account or with mismatched VND payout amount, payout while a refund hold or unallocated historical refund is active, or Customer attempting payout actions or reading bank details is blocked.

---

### 3.24 `MF4` — `FE-23` Evidence-Backed Refunds & Receivable Recovery

- **Function trigger**: A `MANAGER` initiates a refund against a captured payment, completes it after offline external bank transfer with exact accounting allocation, cancels an untransferred pending refund, reconciles an older refund record individually, or records collection against a post-payout Inspector receivable.
- **Actors**: `MANAGER`, `INSPECTOR`.
- **Function description**: Track multi-stage offline-transferred refunds with exact five-way financial allocations, handle untransferred cancellations and historical row reconciliations, and record attributable post-payout Inspector receivables without modifying paid payouts or automatically deducting future payouts.
- **Screen layout (mock-up)**: Manager Settlement Console separate sections for Refund Initiation, Refund Completion/Cancellation, Historical Allocation Reconciliation (by refund), and Inspector Receivable Recovery ledger.
- **Requirements**:
  - **Initiation**: Initiating a refund verifies remaining refundable balance (`BR-49`) and request uniqueness, creates an `Initiated` refund record, reserves the amount, and immediately places a hold on any unpaid payout (`BR-48`).
  - **Completion & Allocation**: After offline external bank transfer, completing the refund requires a globally unique external reference and an exact five-way allocation (`Inspector payout reduction + Platform commission + VAT + TNCN + Platform absorption == Refund amount`, `BR-48`). Cancelling an untransferred refund requires a written reason and is forbidden once completed (`MSG15`).
  - **Historical Reconciliation**: Historical completed refunds lacking breakdown allocations are reconciled individually with a transfer evidence reference and note.
  - **Receivables & Recovery**: A refund against an already-disbursed payout leaves the paid payout immutable and creates an attributable Inspector receivable (`BR-50`). Recoveries are recorded separately against the receivable balance under concurrency protection and never automatically deduct from future mission payouts. Assigned `INSPECTOR` views expose a masked refund summary showing only payout reduction and receivable impact while hiding platform absorption, commission/VAT adjustments, and internal notes.
- **Normal cases**: Manager initiates refund -> executes external bank transfer -> completes with exact 5-part allocation -> if post-payout, tracks receivable and logs manual recovery reference.
- **Abnormal cases**: Refund exceeding captured payment (`MSG50`), allocation sum mismatch, duplicate external reference, cancelling a completed refund, over-recovering a receivable, or Customer/Inspector invoking refund actions is refused.

---

### 3.25 `MF4` — `FE-24` Post-Remediation Re-inspection & Defect Verification

- **Function trigger**: A `CUSTOMER` or `MANAGER` opens a follow-up re-inspection against a completed inspection with a `Published` report; assigned `INSPECTOR` verifies each prior finding three ways; Web and Mobile surface `Resolved` verdict expiry warnings.
- **Actors**: `CUSTOMER`, `MANAGER`, `INSPECTOR`, `ADMIN`.
- **Function description**: Reuse `MF2`–`MF4` flows to verify physical remediation outcomes (`Resolved`, `Unresolved`, `Inconclusive`) on each originally confirmed defect, enforcing fresh in-session evidence and verdict validity windows.
- **Screen layout (mock-up)**: Customer Inspections Re-inspection creation action, Before-vs-After defect verification cards, early `Resolved` verdict expiry banner on Web and Customer Mobile.
- **Requirements**:
  - Creating a re-inspection linked to a prior inspection is permitted only for the owning `CUSTOMER` or `MANAGER` against a completed inspection with a published report (`INSPECTOR` and `ADMIN` creation blocked), initializing one verification record per originally confirmed finding.
  - Each source inspection can have at most one active follow-up at a time. A pending recurring/commercial re-inspection request reserves that follow-up before dispatch, so competing service-request or quick re-inspection creation is rejected even under concurrent requests. A quick re-inspection releases the follow-up when completed or cancelled, while a dispatched commercial follow-up remains active until its remaining occurrences are cancelled or their reports are accepted.
  - Editing verification verdicts is restricted to the assigned `INSPECTOR`, refused while the re-inspection is still scheduled or in flight (must be `Field Completed`), and locked once a report version is submitted or published.
  - Marking any defect `Resolved` requires fresh evidence captured inside a **completed** field session **of that re-inspection**, taken during that session's start-to-end flight window and never reused from the original inspection (`BR-54`).
  - Every `Resolved` verdict records verification time and a derived validity expiration timestamp; both Web and Customer Mobile warn early (`14` days before expiry), while server checks block report preparation, submission, or publication whenever any `Resolved` verdict has expired.
- **Normal cases**: Customer schedules a post-remediation re-inspection from **Service Payment** on the original paid report -> submits the linked follow-up service request through quotation, contract, and dispatch -> Inspector completes a new field session with fresh evidence -> marks defect `Resolved` with Before/After proof -> submits & publishes within the validity window.
- **Abnormal cases**: Creating a second active follow-up for the same source, creating a re-inspection from an incomplete inspection or as an Inspector, submitting `Resolved` without fresh in-session capture, editing after report submission, or attempting publication after verdict expiry fails closed.

---

### 3.26 Out-of-Scope Domains and Retired Capability

The application scope is limited to **building inspection** as described in §1. The following are outside the delivered product:

- **Non-building infrastructure.** Bridges, viaducts, power transmission lines and towers, ground-mounted solar farms, roads, dams, tunnels, ports, and pipelines are not supported. The inspection-item catalogue, the defect classes (`crack`, `leakage`, `abscission`, `corrosion`, `bulge`), and the report template are all built for building surfaces and building rooftop assets.
- **Corrective maintenance execution.** Work-order creation from published defects, repair scoping, repair cost estimation, field repair execution, maintenance completion reporting, maintenance acceptance, and cost reconciliation are not part of the application. The service ends at report acceptance and payment; the Customer arranges corrective work outside the platform. What the platform does provide is the re-inspection loop (`FE-24`), reusing `MF2`–`MF4` to assess prior defects three ways (`Resolved`, `Unresolved`, `Inconclusive`).
- **Aircraft control.** The platform does not pilot, guide, or command an aircraft, and does not act as a ground control station.
- **Photogrammetric reconstruction.** Three-dimensional point-cloud and mesh generation are out of scope. Two-dimensional photographs and video, and the defect annotations derived from them, are in scope.
- **Inspection knowledge retrieval is in scope; maintenance knowledge is not.** `DroneKnowledgeAI` maintains an index of engineering standards and customer-isolated historical defect cases for advisory inspection use (§3.18 / `FE-17`, `BR-55`). A corrective-maintenance repair knowledge base, repair-scope or cost-norm advising, external CMMS integration, and work-order execution remain outside the application.
- **Mobile coverage for non-customer roles.** The mobile application serves the `CUSTOMER` role only; Inspectors and platform staff use the web portals.
