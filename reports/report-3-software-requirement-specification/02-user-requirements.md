---
title: "Report 3 - User Requirements"
document_type: report3-srs-section
weight: 25
source: "report3-software-requirement-specification.docx"
---

## 2. User Requirements

This section defines the actors of the building-inspection service and the business goals they pursue. The scope is limited to building structures as described in §1, and the use cases below are grouped across the four main flows `MF1`–`MF4` that §3 details as twenty-four atomic features (`FE-01`–`FE-24`). Partner Inspector admission is a public self-service application reviewed by platform staff; an Inspector account is created only after that review succeeds. Recurring service requests are supported, and accepting a quotation materializes their planned occurrences. Occurrence materialization is acceptance-triggered, not time-based generation.

### 2.1 Actors

| # | Actor | Description |
| --- | --- | --- |
| 1 | `ADMIN` | Platform administrator. Manages platform accounts and the building asset category catalogue; views partner Inspector applications and drone registrations in read-only oversight mode; maintains pilot-licence classes, required drone document configuration, finance settings, and AI inference settings; and reviews platform activity records. |
| 2 | `MANAGER` | Platform manager. Coordinates Inspector and drone records, reviews and approves partner Inspector applications and drone registrations, responds to customer service requests, negotiates and issues VND quotations, records signed service agreements, assigns Inspectors and drones to inspection occurrences, manages dispatch changes, independently reviews and publishes inspection reports, and manages partner payouts and refunds. |
| 3 | `CUSTOMER` | Customer organization representative. Registers its organization and initial building subject to airspace screening; manages buildings, inspection checkpoints, and building documents; requests one-time or recurring inspections; negotiates and accepts quotations; follows inspection progress; accepts published reports; and pays service fees. |
| 4 | `INSPECTOR` | Partner drone inspector. Submits a public self-service application with pilot credentials and partner information; after platform approval an account is created. The Inspector then registers owned drones with registration, ownership, and technical inspection documents, conducts assigned field work, provides inspection evidence, reviews proposed findings, and prepares and submits inspection reports. Drone ownership is not a condition of partner admission. |
| 5 | Automated System and AI Actors | Four automated actors act without a login: `SYSTEM` performs airspace screening, schedule-conflict checks, lifecycle notices, assignment timeouts, and other scheduled jobs; `YOLO11` analyses building imagery for candidate defects with a configured vision fallback; `LLM` drafts advisory report narrative and executive summaries; and `DroneKnowledgeAI` retrieves tenant-isolated historical defect cases and engineering standards over `pgvector`. Automated output is advisory; official findings and decisions require human review. |
| 6 | External Payment and Identity Services | Google OAuth2 sign-in, Sepay VietQR and VNPay service-payment processing. These services do not replace the platform's authorization, review, or recordkeeping responsibilities. |
| 7 | SmartDroneHub | An optional ground-station integration that supplies read-only MAVLink telemetry, flight traces, and mission video for a permitted field session. It does not receive flight commands from the platform. |

The `CUSTOMER` role is also served by a native mobile application that mirrors the web experience for verdict expiry, the payment-notice and payment-receipt PDF, Inspector–Customer chat, and the compact knowledge-references strip. Other roles use the web portals.

### 2.2 Use Cases

#### 2.2.1 Diagram(s)

The system use cases are organized into five role- and capability-focused UML views (`UC-1` through `UC-5`), covering public access and authentication, asset/drone onboarding, commercial contracting and field execution, AI inspection and settlement, and platform administration.

![UC-1 Authentication and Public Access Use Case Diagram](assets/diagrams/uc-1-auth-public.png)

Figure 2.1 Use Case Diagram — `UC-1` Authentication & Public Access.

![UC-2 Assets, Drones and Partner Onboarding Use Case Diagram](assets/diagrams/uc-2-assets-drones-onboarding.png)

Figure 2.2 Use Case Diagram — `UC-2` Assets, Drones & Partner Onboarding.

![UC-3 Contracting, Dispatch and Field Execution Use Case Diagram](assets/diagrams/uc-3-contracting-field.png)

Figure 2.3 Use Case Diagram — `UC-3` Contracting, Dispatch & Field Execution.

![UC-4 AI Inspection, Reporting and Financial Settlement Use Case Diagram](assets/diagrams/uc-4-ai-reporting-settlement.png)

Figure 2.4 Use Case Diagram — `UC-4` AI Inspection, Reporting & Financial Settlement.

![UC-5 Platform Administration and Analytics Use Case Diagram](assets/diagrams/uc-5-platform-admin.png)

Figure 2.5 Use Case Diagram — `UC-5` Platform Administration & Analytics.

#### 2.2.2 Descriptions

| ID | Use Case | Actors | Use Case Description |
| --- | --- | --- | --- |
| UC-01 | Sign In and Manage Account | All Roles | Users securely sign in by password, one-time code, or Google, manage their personal account information, and end their own active sessions. |
| UC-02 | Govern Platform Accounts, Building Categories, and Finance | `ADMIN`, `MANAGER` | Authorized platform staff manage platform accounts and the building asset category catalogue; `ADMIN` maintains pilot-licence classes, required drone-document configuration, Inspector rating criteria, finance settings, and AI inference settings. |
| UC-03 | Register Customer Organization and Initial Building | `CUSTOMER`, public | A prospective Customer registers its organization with an initial building. The service screens the location: prohibited airspace prevents registration, restricted airspace attaches an advisory warning (`MSG28`) requiring a valid mission flight permit while activating the account and initial building immediately, and clear locations proceed normally. Screening does not grant governmental clearance. |
| UC-04 | Manage Buildings, Checkpoints, and Documents | `CUSTOMER` | Customers register and maintain organization buildings, their inspection checkpoints, and reference documents, and may retire buildings no longer in service. Building locations are screened for prohibited airspace. |
| UC-05 | Submit and Review Partner Inspector Application | Public, `INSPECTOR`, `MANAGER`, `ADMIN` (read-only) | A prospective partner Inspector submits a public application with identity, pilot-licence details, and a licence scan. `MANAGER` reviews it, approves it or rejects it with reasons, and records the signed partner contract (`ADMIN` has read-only oversight). An account is created only after approval; approval does not require drone ownership. |
| UC-06 | Register and Review Inspector-Owned Drones | `INSPECTOR`, `MANAGER`, `ADMIN` (config &amp; read-only) | An Inspector registers an owned drone with photographs, outdoor flight capabilities, safety checklist items, and the registration, ownership, and technical-inspection documents configured by `ADMIN`. `MANAGER` reviews and approves or rejects the application before the drone becomes eligible for assignment. |
| UC-07 | Request Inspection, Negotiate, and Accept a Quotation | `CUSTOMER`, `MANAGER` | A Customer submits a one-time or recurring service request for a building, exchanges messages with the assigned `MANAGER`, reviews a VND quotation, and accepts the current active quotation. Changes to commercial terms require a revised quotation. |
| UC-08 | Record Signed Service Agreement and Arrange Occurrences | `MANAGER`, `CUSTOMER` | After the parties sign an offline service agreement, `MANAGER` records the signed document. For a recurring request, the agreement covers the occurrences within its agreed term. Each occurrence is separately prepared for assignment and delivery. |
| UC-09 | Assign, Reschedule, Reassign, or Cancel an Inspection | `MANAGER`, `INSPECTOR`, Automated System | `MANAGER` assigns a qualified Inspector and an eligible owned drone to an occurrence, accounting for availability across customer organizations. After an aborted field session, `MANAGER` may reschedule, reassign, or cancel the dispatch. |
| UC-10 | Provide Mission Flight Permit (Inspector Self-Attestation) | `INSPECTOR` (uploader and accountable self-attestor), `MANAGER`/`ADMIN` (read-only view and audit trail) | The assigned Inspector uploads the mission flight permit with structured metadata and is responsible for it; the permit becomes effective immediately once validation passes, with no Manager or Administrator verification or approval step. A drone change or an out-of-window reschedule invalidates the permit and requires an Inspector re-upload. The service's document check is not government authorization. |
| UC-11 | Record Field Session | `INSPECTOR` | The assigned Inspector records the start, multi-flight sorties, normal completion, or abort of an on-site session, including the required pre-flight safety checklist and an outcome or abort reason. An abort prompts dispatch follow-up by `MANAGER`. |
| UC-12 | Capture Flight Evidence | `INSPECTOR`, SmartDroneHub | The Inspector provides read-only MAVLink telemetry, imports an exported flight log, submits an accountable manual flight declaration, or receives mission video, and the persisted flight trace can be reviewed afterwards. |
| UC-13 | Review Airspace Information | All Roles | Users may review airspace information relevant to building and mission locations. Information shown is advisory and does not constitute permission to fly. |
| UC-14 | Provide Inspection Evidence | `INSPECTOR`, `MANAGER`, `CUSTOMER` | Inspectors upload building photographs and video, associate them with structural locations, and identify unusable captures. Authorized users review evidence according to their responsibilities. |
| UC-15 | Review Candidate Findings and Confirm Findings | `INSPECTOR`, Automated System | The service suggests candidate building defects from inspection images. The assigned Inspector reviews, edits, rejects, or supplements each suggestion, and confirms the findings baseline. Only human-confirmed findings become official inspection findings. |
| UC-16 | Prepare and Submit Inspection Report | `INSPECTOR`, Automated System | After confirming findings, the report author prepares and submits the inspection report for independent review. The service may supply an AI-drafted summary as advisory material. Submission is an explicit action, not the act of opening a screen. |
| UC-17 | Independently Review and Publish Inspection Report | `MANAGER`, `ADMIN` (read-only) | A `MANAGER` who is not the report author independently reviews a submitted report, approves it for publication or returns it with reasons, and publishes the approved official report (`ADMIN` retains read-only visibility only). Published reports are preserved; corrections are issued as a new version. |
| UC-18 | Follow Inspection, Accept Report, Rate Inspector, and Pay Service Fee | `CUSTOMER`, `MANAGER`, Payment Service | Customers follow inspection progress, review the published report, record acceptance, optionally rate the assigned Inspector against configured criteria, and settle the applicable service fee through Sepay VietQR or VNPay. Official deliverables are available from publication onward, while Partner settlement gates publication (`FE-22`). |
| UC-19 | Manage Partner Settlement, Payouts, and Refunds | `MANAGER` | `MANAGER` records Inspector payouts against verified customer payment, initiates and completes refunds with evidence-backed allocations, and records recovery of Inspector receivables. |
| UC-20 | View Role-Appropriate Dashboard, Calendar, and Notifications | All Roles | Users review operational information, inspection schedules, progress, and available notices within their authorized responsibilities. |
| UC-21 | Review Activity History | Authorized Roles | Authorized users review attributable records of important onboarding, commercial, inspection, payment, and acceptance decisions within their access scope. |
