---
title: SmartDroneInspection — Report 3 Software Requirement Specification
document_type: software-requirement-specification
source_docx: Report3_Software_Requirement_Specification_SmartDroneInspection_corrected.docx
purpose: AI-readable companion with searchable headings, tables, workflows, and rules
updated: 2026-09-18
---

# SmartDroneInspection — Report 3

> This Markdown file is the text-first companion to the official-template DOCX. It is intended for AI retrieval, review, and change impact analysis. The DOCX remains the presentation baseline for submission and visual diagrams.

Official presentation file: [Report 3 DOCX](Report3_Software_Requirement_Specification_SmartDroneInspection_corrected.docx).

## Canonical project context

- Product: SmartDroneInspection infrastructure inspection management platform.
- Roles: Admin, Service Manager, Inspector, Maintenance Engineer, Client.
- Workflow: WF1 asset registration and periodic scheduling → WF2 request review, service order, and Inspector assignment → WF3 inspection execution, AI-assisted verification, and report delivery → WF4 maintenance assessment, execution, and defect resolution.
- Evidence flow: images are uploaded through the web or mobile application, stored in MinIO, and optionally analyzed by the YOLO/AI service for non-official defect candidates. Inspector verification is required before findings become official.
- Boundary: the product does not pilot drones or depend on a separate drone-operation platform.

## How to use this file

- Use headings to retrieve a requirement section and tables to retrieve IDs, actors, rules, validations, and acceptance conditions.
- Treat the DOCX as the authoritative visual layout; diagrams are represented here by their captions and surrounding textual requirements.
- The companion [Capstone error-prevention guide](capstone-error-prevention-guide.md) contains review, implementation, testing, demo, and defense checks.

---

# I. Record of Changes

**Table 1 - Record of changes**

| Date | A M D | In charge | Change Description |
| --- | --- | --- | --- |
| 17 Sep 2026 | A | Project Team | Initial SRS baseline aligned with the final WF1-WF4 workflows and five-role authorization model. |

A - Added M - Modified D - Deleted

# II. Software Requirement Specification

This Software Requirement Specification defines the functional and non-functional requirements for SmartDroneInspection. The baseline covers asset registration, inspection service delivery, AI-assisted finding verification, report approval, and maintenance resolution. The specification is organized around the final WF1-WF4 business workflows and the roles Admin, Service Manager, Inspector, Maintenance Engineer, and Client.

## 1. Product Overview

SmartDroneInspection is an infrastructure inspection management platform that coordinates the lifecycle from customer assets and recurring inspection schedules to service orders, field evidence, verified defects, reports, and maintenance tickets. The product consists of a browser portal for administrative, customer, and service operations and a mobile application for assigned field work.

The platform does not depend on a separate drone-operation platform and does not pilot drones, execute flight missions, or replace field safety procedures. Inspection images are uploaded from a drone SD card, a computer, or a mobile device. MinIO stores evidence objects, while the YOLO service proposes defect candidates that remain non-official until an Inspector verifies them.

Figure 1 defines the system boundary and the external actors and services that exchange information with the platform.

> [Visual diagram omitted from this text export; use the DOCX for the rendered figure.]

**Figure 1 - SmartDroneInspection system context**

### 1.1 Product Scope

**Table 2 - Product scope and boundaries**

| Boundary | Definition |
| --- | --- |
| In scope | Identity and role administration; organization-scoped asset management; recurring schedules; periodic and ad hoc inspection requests; quotations and service orders; assignments; field inspection; evidence storage; AI candidate review; report versioning and peer review; maintenance assessment and execution; notifications; audit history. |
| External dependency | MinIO object storage and the YOLO/AI image-analysis service. |
| Out of scope | Manual drone piloting, flight control, telemetry ownership, public self-registration, online payment processing, procurement, inventory accounting, and autonomous approval of AI findings. |

### 1.2 Operating Assumptions

- Organizations, customer accounts, asset categories, and checklist templates are configured before operational use.

- Clients own the business decision to approve quotations, service orders, released reports, maintenance changes, and final resolution outcomes.

- Service Managers coordinate work but do not substitute for an Inspector's technical inspection judgment or a Maintenance Engineer's technical assessment.

- Evidence without GPS remains usable when the missing metadata is recorded; evidence provenance and checksum remain required.

- No upfront payment is required in WF2 or WF4. The Client accepts post-service payment terms before work proceeds.

## 2. User Requirements

### 2.1 Actors

Table 3 defines the five business roles used throughout this SRS. Internal role codes are included only to align the requirements with backend authorization.

**Table 3 - System actors**

| # | Actor | Internal role code | Description |
| --- | --- | --- | --- |
| 1 | Admin | PLATFORM_ADMINISTRATOR | Administers organizations, accounts, role assignments, categories, checklist templates, and platform configuration. Does not automatically perform customer or service workflow actions. |
| 2 | Service Manager | SERVICE_OPERATIONS_MANAGER | Reviews requests, creates quotations and orders, assigns qualified staff, coordinates peer review, and releases customer-visible results across organizations. |
| 3 | Inspector | INSPECTOR | Accesses only assigned inspections or peer reviews; completes checklists, evidence, verified findings, and report work. A report author cannot approve the same report as peer reviewer. |
| 4 | Maintenance Engineer | MAINTENANCE_ENGINEER | Accesses only assigned maintenance assessments or execution work; supplies technical estimates, work evidence, change requests, and completion reports. |
| 5 | Client | ORGANIZATION_MANAGER | Acts for one customer organization; manages that organization's assets, requests, approvals, released reports, maintenance tickets, and resolution decisions. |

### 2.2 Use Cases

#### 2.2.1 Diagrams

Figures 2 through 4 separate the use cases by operational area so actor associations remain readable. The diagrams describe user goals rather than execution sequences.

> [Visual diagram omitted from this text export; use the DOCX for the rendered figure.]

**Figure 2 - Administration and client use cases**

> [Visual diagram omitted from this text export; use the DOCX for the rendered figure.]

**Figure 3 - Inspection service use cases**

> [Visual diagram omitted from this text export; use the DOCX for the rendered figure.]

**Figure 4 - Maintenance service use cases**

#### 2.2.2 Descriptions

**Table 4 - Use case catalog**

| ID | Use Case | Actors | Use Case Description |
| --- | --- | --- | --- |
| UC-01 | Authenticate User | All roles | Sign in with an issued account, complete first-password setup when required, refresh the session, change the password, and sign out. |
| UC-02 | Manage Users and Organizations | Admin | Create organizations and accounts, assign valid roles, reset credentials, change status, and revoke sessions. |
| UC-03 | Configure Categories and Checklists | Admin | Maintain asset categories, checklist templates, and platform-level business configuration. |
| UC-04 | Register Asset | Client | Create and update an asset inside the Client's organization. |
| UC-05 | Manage Asset Documents | Client | Upload and maintain technical drawings, manuals, previous reports, and maintenance history. |
| UC-06 | Schedule Periodic Inspection | Client | Create and activate a recurring schedule for an asset and checklist template. |
| UC-07 | Submit Ad Hoc Inspection Request | Client | Create a non-periodic inspection request with scope, priority, deadline, access constraints, contacts, and attachments. |
| UC-08 | Review Inspection Request | Service Manager | Assess request completeness, feasibility, and service capacity. |
| UC-09 | Prepare Quotation and Service Order | Service Manager | Create versioned commercial terms and the proposed service scope. |
| UC-10 | Approve Service Order | Client | Approve the current quotation and post-service payment terms or request a revision. |
| UC-11 | Assign Inspector | Service Manager | Select a qualified, available Inspector without a known conflict of interest. |
| UC-12 | Respond to Inspection Assignment | Inspector | Accept or reject the assigned inspection; rejection requires a reason. |
| UC-13 | Conduct Inspection | Inspector | Start an assigned session and execute the confirmed checklist and scope. |
| UC-14 | Upload Evidence | Inspector | Upload inspection evidence with validation, checksum, duplicate prevention, and metadata. |
| UC-15 | Verify AI Candidates | Inspector | Confirm, modify, or reject AI defect candidates and add missed findings manually. |
| UC-16 | Complete Checklist and Findings | Inspector | Complete checklist answers and technical details for verified defects. |
| UC-17 | Prepare Report | Inspector | Review, correct, version, and submit a draft inspection report. |
| UC-18 | Peer Review Report | Inspector | Review another Inspector's report, request changes, or technically approve it. |
| UC-19 | Release Report | Service Manager | Check deliverable completeness and release the technically approved report. |
| UC-20 | Accept or Revise Report | Client | Accept the released report or request clarification and revision without directly editing technical content. |
| UC-21 | Create Maintenance Ticket | Client | Create a ticket from one or more verified defects in an accepted report. |
| UC-22 | Assess Maintenance Work | Maintenance Engineer | Assess the defect remotely or on site and estimate work, materials, labor, duration, risks, assumptions, and cost range. |
| UC-23 | Prepare Maintenance Quotation | Service Manager | Create a versioned maintenance quotation and draft order based on the Engineer's assessment. |
| UC-24 | Approve Maintenance Order | Client | Approve scope and post-service payment terms or request revision. |
| UC-25 | Execute Maintenance Work | Maintenance Engineer | Accept the execution assignment, perform approved work, and record progress. |
| UC-26 | Manage Maintenance Change Request | Maintenance Engineer, Service Manager, Client | Stop unapproved additional work, revise the order, and obtain the Client's decision before continuing. |
| UC-27 | Release Maintenance Result | Service Manager | Verify the completion report, evidence, and cost before releasing the result. |
| UC-28 | Resolve Maintenance Ticket | Client | Accept resolution, request rework, or request a linked re-inspection. |
| UC-29 | View Operational Dashboard | Admin, Service Manager | View role-appropriate operational counts and status summaries without bypassing resource scope. |
| UC-30 | Manage Password and Session | All roles | Change the password and terminate the current or all active sessions. |

## 3. Functional Requirements

### 3.1 System Functional Overview

#### 3.1.1 Screens Flow

Figure 5 shows the primary navigation paths. Browser screens support administrative, customer, and service operations; mobile screens support assigned Inspector and Maintenance Engineer work.

> [Visual diagram omitted from this text export; use the DOCX for the rendered figure.]

**Figure 5 - Primary browser and mobile screen flow**

#### 3.1.2 Screen Descriptions

**Table 5 - Screen descriptions**

| # | Feature | Screen | Description |
| --- | --- | --- | --- |
| 1 | Authentication | Login | Authenticate an issued user account and route the user to the permitted client experience. |
| 2 | Authentication | First Password Setup | Replace the administrator-issued temporary password before normal access. |
| 3 | Common | Dashboard | Show role-scoped work queues, counts, deadlines, and recent results. |
| 4 | Common | Profile and Password | View account information, change password, and sign out of one or all sessions. |
| 5 | Administration | Organizations | Create, activate, suspend, and review customer organizations. |
| 6 | Administration | Users | Provision accounts, assign role/zone, reset credentials, change status, and revoke sessions. |
| 7 | Administration | Asset Categories | Maintain categories used to classify assets. |
| 8 | Administration | Checklist Templates | Create and version checklist templates and checklist items. |
| 9 | Administration | Platform Configuration | Maintain allowed business parameters, file constraints, and service settings. |
| 10 | Assets | Asset List | Search, filter, and open organization-scoped assets. |
| 11 | Assets | Asset Details | View and update asset data, documents, schedules, requests, reports, and maintenance history. |
| 12 | Planning | Inspection Schedules | Create, activate, pause, and review recurring inspection schedules. |
| 13 | Requests | Inspection Request | Create or review a periodic/ad hoc request and its attachments. |
| 14 | Commercial | Quotation and Service Order | Create versions, review scope and terms, approve, or request revision. |
| 15 | Assignments | Inspection Assignment | Assign an Inspector and record accept/reject responses. |
| 16 | Inspection | My Inspection Assignments | List only inspections assigned to the signed-in Inspector. |
| 17 | Inspection | Inspection Session | Start work, complete the checklist, and record inspection progress. |
| 18 | Inspection | Evidence Upload | Upload images and documents with metadata and upload status. |
| 19 | AI | AI Candidate Review | Confirm, modify, or reject AI candidates and add manual findings. |
| 20 | Reports | Draft Report | Review generated content, edit the working version, and submit for peer review. |
| 21 | Reports | Peer Review | Review another Inspector's report and request changes or approve technical content. |
| 22 | Reports | Report Release | Check required deliverables and release the final report to the Client. |
| 23 | Reports | Released Report | View, download, accept, or request clarification/revision. |
| 24 | Maintenance | Maintenance Ticket | Create or review a ticket linked to verified defects. |
| 25 | Maintenance | Assessment Assignment | Assign and complete the technical maintenance assessment. |
| 26 | Maintenance | Maintenance Quotation and Order | Prepare, revise, and approve maintenance scope and terms. |
| 27 | Maintenance | Execution Task | Accept work, record progress, and submit before/after evidence. |
| 28 | Maintenance | Change Request | Document additional damage/cost and collect the Client decision before work continues. |
| 29 | Maintenance | Completion and Resolution | Verify, release, and accept the result or route it to rework/re-inspection. |
| 30 | Audit | Audit History | Search security and workflow events allowed for the current role and scope. |

#### 3.1.3 Screen Authorization

The matrix uses M = manage, O = own organization, A = assigned resource, R = release/coordinate, V = view. A blank cell means denied. Backend resource checks remain authoritative.

**Table 6 - Screen authorization matrix**

| Screen | Admin | Service Mgr | Inspector | Maint Eng | Client |
| --- | --- | --- | --- | --- | --- |
| Dashboard | V | V | V | V | V |
| Organizations | M |  |  |  |  |
| Users | M |  |  |  |  |
| Categories and Checklists | M | V | V | V | V |
| Platform Configuration | M |  |  |  |  |
| Asset List and Details | V |  |  |  | M O |
| Inspection Schedules | V |  |  |  | M O |
| Inspection Requests | V | M R | A V |  | M O |
| Quotation and Service Order | V | M R | A V |  | O Approve |
| Inspection Assignment | V | M R | A Respond |  | O V |
| Inspection Session | V | R V | A M |  | O V |
| Evidence and AI Review | V | R V | A M |  | O V |
| Draft Report | V | R V | A M |  |  |
| Peer Review | V | R Assign | A M |  |  |
| Report Release | V | M R | A V |  | O Accept |
| Maintenance Ticket | V | M R |  | A V | M O |
| Assessment Assignment | V | M R |  | A M | O V |
| Maintenance Quotation | V | M R |  | A V | O Approve |
| Execution Task | V | R V |  | A M | O V |
| Change Request | V | M R |  | A M | O Decide |
| Completion and Resolution | V | M R |  | A M | O Decide |
| Audit History | M V | V | A V | A V | O V |

#### 3.1.4 Non-Screen Functions

**Table 7 - Non-screen functions**

| # | Feature | System Function | Description |
| --- | --- | --- | --- |
| 1 | Authentication | Access-token validation | Validate token signature, issuer, audience, expiry, session, user status, auth version, role, and resource scope. |
| 2 | Authentication | Refresh rotation | Rotate opaque refresh tokens and reject reuse or a revoked/expired session. |
| 3 | Planning | Periodic request generation | Monitor active schedules and create one periodic request for each Asset + Schedule + Due Cycle key. |
| 4 | Files | Evidence intake | Validate file type and size, calculate a checksum, prevent duplicates, and store authorized objects in MinIO. |
| 5 | AI | Image inference | Submit eligible images to the YOLO service and persist model version, label, confidence, and bounding box as candidates. |
| 6 | Reports | Draft compilation | Compile a versioned report draft from checklist responses, evidence, and verified findings. |
| 7 | Reports | Immutable acceptance | Freeze the accepted report version while preserving the revision and approval history. |
| 8 | Maintenance | Linked re-inspection | Create an ad hoc inspection request from a re-inspection decision and return it to WF2. |
| 9 | Notifications | Event notification | Notify relevant actors about requests, assignments, decisions, deadlines, releases, and required corrections. |
| 10 | Audit | Security and workflow audit | Append security and material workflow events without storing passwords, raw tokens, or protected evidence content. |
| 11 | Cleanup | Retention processing | Remove expired refresh-token history and apply configured evidence/audit retention rules. |

#### 3.1.5 Entity Relationship Diagram

Figure 6 presents the conceptual lifecycle entities. Authentication and audit support the User entity; detailed physical keys, indexes, and storage types belong in the Software Design Document.

> [Visual diagram omitted from this text export; use the DOCX for the rendered figure.]

**Figure 6 - High-level entity relationship diagram**

**Table 8 - Entity descriptions**

| # | Entity | Description |
| --- | --- | --- |
| 1 | Organization | Customer organization that owns assets and Client accounts. |
| 2 | User | Issued account with status, actor zone, organization scope, and authentication version. |
| 3 | UserRole | Role assignment constrained to the user's actor zone. |
| 4 | AuthSession | Web or mobile login session that can be revoked independently. |
| 5 | AssetCategory | Admin-managed asset classification. |
| 6 | ChecklistTemplate | Versioned inspection checklist definition. |
| 7 | Asset | Organization-owned infrastructure item subject to inspection and maintenance. |
| 8 | AssetDocument | Technical document linked to an asset. |
| 9 | InspectionSchedule | Recurring schedule that generates periodic requests. |
| 10 | InspectionRequest | Periodic or ad hoc request with scope, priority, deadline, and access constraints. |
| 11 | Quotation | Versioned commercial proposal for inspection or maintenance service. |
| 12 | ServiceOrder | Confirmed inspection scope and post-service payment terms. |
| 13 | Assignment | Accepted/rejected assignment for inspection, peer review, assessment, or execution. |
| 14 | Inspection | Field inspection session governed by an accepted assignment. |
| 15 | ChecklistResponse | Recorded response to a checklist item for an inspection. |
| 16 | Evidence | Stored file with checksum, provenance, metadata, and object-storage reference. |
| 17 | AIFindingCandidate | Non-official model output awaiting Inspector verification. |
| 18 | VerifiedFinding | Confirmed or manually added defect with location, severity, notes, and recommendation. |
| 19 | InspectionReport | Report aggregate linked to one inspection. |
| 20 | ReportVersion | Versioned report content and approval state. |
| 21 | PeerReview | Technical review result by an Inspector other than the report author. |
| 22 | MaintenanceTicket | Client request linked to one or more verified findings. |
| 23 | MaintenanceAssessment | Engineer-provided technical scope, estimate, risks, and assumptions. |
| 24 | MaintenanceOrder | Approved maintenance scope and commercial terms. |
| 25 | MaintenanceAssignment | Assessment or execution assignment to a Maintenance Engineer. |
| 26 | MaintenanceWorkLog | Progress, materials, duration, cost, and before/after evidence. |
| 27 | ChangeRequest | Material change in scope or cost requiring Client decision. |
| 28 | Invoice | Final actual-cost and payment-status record issued after completion. |
| 29 | Notification | Delivery record for a user-facing workflow notification. |
| 30 | AuditEvent | Append-only security or material workflow event. |

### 3.2 WF1 Asset Registration and Periodic Inspection Scheduling

Primary actors: Client and System.

Required outcome: A valid PERIODIC inspection request ready for WF2.

**Table 9 - WF1 functional sequence**

| Step | Role or Lane | System Requirement | Expected Output |
| --- | --- | --- | --- |
| WF1-01 | Client | Create an asset record with the asset name, code, category, location, ownership information and operational status. | Draft asset record |
| WF1-02 | System | Validate the organization scope, required fields and asset-code uniqueness before saving the asset. | Validated asset record |
| WF1-03 | Client | Upload available asset documents, such as technical drawings, manuals, previous inspection reports and maintenance history. | Asset documentation |
| WF1-04 | Client | Create a recurring inspection schedule by selecting the asset, inspection frequency, next due date and applicable checklist template. | Draft inspection schedule |
| WF1-05 | System | Validate the schedule, calculate future due cycles and activate the recurring schedule. | Active inspection schedule |
| WF1-06 | System | Monitor active schedules and identify schedules whose due date has been reached. | Due inspection cycle |
| WF1-07 | System | Generate one PERIODIC inspection request using the unique Asset + Schedule + Due Cycle idempotency key. | Periodic inspection request |
| WF1-08 | System | Link the request to the asset, schedule and checklist template, then notify the Client and Service Manager. | Request ready for WF2 |

#### 3.2.1 Validation and Exception Requirements

- Missing required asset data prevents schedule activation.

- An inactive asset pauses its schedule.

- The same due cycle cannot generate more than one request.

- An unavailable checklist template routes the request to manual review.

### 3.3 WF2 Request Review, Service Order, and Inspector Assignment

Primary actors: Client, Service Manager, Inspector, and System.

Required outcome: A confirmed service order and accepted Inspector assignment with status READY_FOR_INSPECTION.

**Table 10 - WF2 functional sequence**

| Step | Role or Lane | System Requirement | Expected Output |
| --- | --- | --- | --- |
| WF2-01 | System / Client | Receive a system-generated PERIODIC request or create a new AD_HOC inspection request. | Inspection request |
| WF2-02 | Client | Complete the request with the inspection scope, priority, preferred deadline, site-access constraints, contact information and supporting documents. | Completed inspection request |
| WF2-03 | System | Validate the required request information and verify that the selected asset belongs to the requester’s organization. | Valid request |
| WF2-04 | Service Manager | Review the request, determine whether the requested scope is feasible and check available service capacity. | Feasibility decision |
| WF2-05 | Service Manager | Prepare a versioned quotation and draft service order containing the agreed scope, deliverables, estimated price or applicable rates, expected duration and post-service payment terms. | Quotation and draft service order |
| WF2-06 | Client | Review the quotation and service order. Approve them and accept the post-service payment terms, or request a revised quotation. | Approved order or revision request |
| WF2-07 | Service Manager | When the order is approved, mark the service order as confirmed and select an Inspector based on qualifications, availability, workload and potential conflicts of interest. | Inspector assignment |
| WF2-08 | System | Create an assignment package containing the asset information, confirmed scope, checklist, deadline, access instructions and supporting documents, then notify the Inspector. | Assigned inspection package |
| WF2-09 | Inspector | Review the assignment package and accept or reject the assignment. A rejection must include a reason. | Accepted or rejected assignment |
| WF2-10 | Service Manager | If the Inspector rejects the assignment, select another qualified Inspector. If accepted, mark the inspection job as READY_FOR_INSPECTION. | Accepted Inspector assignment |

#### 3.3.1 Validation and Exception Requirements

- An incomplete request cannot be accepted for quotation.

- A quotation revision creates a new version; the previous version is retained.

- An unconfirmed order cannot proceed to assignment.

- A rejected Inspector assignment returns to the Service Manager for reassignment.

### 3.4 WF3 Inspection Execution AI Assisted Verification and Report Delivery

Primary actors: Inspector, Service Manager, Client, System, MinIO, and YOLO Service.

Required outcome: A technically reviewed, customer-released, and customer-accepted inspection report.

**Table 11 - WF3 functional sequence**

| Step | Role or Lane | System Requirement | Expected Output |
| --- | --- | --- | --- |
| WF3-01 | Inspector — Author | Open the accepted assignment and start a new inspection session. | Active inspection session |
| WF3-02 | System | Change the inspection status from READY_FOR_INSPECTION to IN_PROGRESS and record the session start time and responsible Inspector. | Inspection in progress |
| WF3-03 | Inspector — Author | Conduct the field inspection according to the assigned checklist and confirmed service scope. Manual drone piloting remains outside the platform. | Field inspection results |
| WF3-04 | Inspector — Author | Capture or collect inspection images and transfer them from the drone’s SD card, computer or mobile device to the platform. | Uploaded evidence |
| WF3-05 | System: Upload Service | Validate the file type and size, calculate a checksum, prevent duplicate evidence and retry interrupted uploads without creating duplicate records. | Validated evidence |
| WF3-06 | System: MinIO | Store the evidence and associate it with the inspection, asset, Inspector, capture time, source and available GPS or external mission reference. | Stored inspection evidence |
| WF3-07 | System: YOLO Service | Analyze eligible images and generate defect candidates containing the predicted label, confidence score, bounding box and model version. | AI defect candidates |
| WF3-08 | Inspector — Author | Review every AI candidate and select Confirm, Modify or Reject. The Inspector may also manually add a defect missed by the AI model. | Inspector-verified findings |
| WF3-09 | System | Exclude rejected and unverified AI candidates from official defect statistics and report content. | Official verified findings |
| WF3-10 | Inspector — Author | Complete the checklist and add the defect location, severity, technical notes and recommended action for each verified finding. | Completed inspection record |
| WF3-11 | System | Compile a versioned draft report from the checklist, evidence and verified findings. LLM assistance may be used only with authorized data and remains subject to human review. | Versioned draft report |
| WF3-12 | Inspector — Author | Review the draft report, correct its content and submit it for internal peer review. | Report awaiting peer review |
| WF3-13 | Service Manager | Assign another qualified Inspector as the Peer Reviewer. The report author cannot review their own report. | Peer-review assignment |
| WF3-14 | Inspector — Peer Reviewer | Verify that the evidence supports the findings and check defect classification, severity, location, checklist consistency and technical conclusions. | Peer-review result |
| WF3-15 | Inspector — Peer Reviewer | Request changes when issues are found, or mark the report as TECHNICALLY_APPROVED when the technical content is acceptable. | Technically approved report |
| WF3-16 | Inspector — Author | If changes are requested, revise the report and resubmit it to the same Peer Reviewer. | Revised report version |
| WF3-17 | Service Manager | Check that the technically approved report is complete and contains all deliverables required by the confirmed service order. | Internally released report |
| WF3-18 | Service Manager | Release the final report to the Client . Internal drafts and peer-review comments remain hidden from the customer. | Final customer report |
| WF3-19 | Client | Review the released report and accept it or request clarification and revision. The Client does not directly edit the technical content. | Accepted report or revision request |
| WF3-20 | System | When the customer accepts the report, mark the version as immutable and preserve the complete approval and revision history. | Customer-accepted report |

#### 3.4.1 Validation and Exception Requirements

- Unsupported or corrupted evidence is rejected.

- Interrupted uploads retry without duplicate evidence records.

- YOLO unavailability queues or defers inference without losing evidence.

- Rejected or unverified AI candidates never enter official statistics.

- The report author cannot peer-review the same report.

- An accepted report is corrected through a new version rather than overwritten.

### 3.5 WF4 Maintenance Assessment Work Execution and Defect Resolution

Primary actors: Client, Service Manager, Maintenance Engineer, and System.

Required outcome: A closed ticket and resolved defect, an active rework cycle, or a linked re-inspection request returned to WF2.

**Table 12 - WF4 functional sequence**

| Step | Role or Lane | System Requirement | Expected Output |
| --- | --- | --- | --- |
| WF4-01 | Client | Select one or more verified defects from an accepted report and create a maintenance ticket with the required priority, preferred deadline and additional instructions. | Maintenance ticket |
| WF4-02 | System | Link the ticket to the organization, asset, inspection report, verified findings and supporting evidence. | Traceable maintenance ticket |
| WF4-03 | Service Manager | Review the ticket for completeness and determine whether a technical assessment can be performed remotely or requires a site visit. | Assessment plan |
| WF4-04 | Service Manager | Assign a qualified Maintenance Engineer to perform the technical assessment. This is an assessment assignment, not yet an execution assignment. | Assessment assignment |
| WF4-05 | Maintenance Engineer — Assessor | Review the defect evidence and, when necessary, conduct an on-site assessment. | Assessed defect condition |
| WF4-06 | Maintenance Engineer — Assessor | Estimate the required work, materials, labor, expected duration, technical risks, assumptions and estimated cost range. | Technical assessment and estimate |
| WF4-07 | Service Manager | Use the technical assessment and approved pricing rules to prepare a versioned maintenance quotation and draft maintenance order. | Maintenance quotation and draft order |
| WF4-08 | Client | Review the quotation and maintenance order. Approve the scope and post-service payment terms, or request revision. | Approved maintenance order |
| WF4-09 | Service Manager | Confirm the approved maintenance order and assign the same Engineer or another qualified Engineer to perform the work. | Execution assignment |
| WF4-10 | Maintenance Engineer — Executor | Review and accept the execution assignment. If rejected, the Service Manager selects another Engineer. | Accepted execution assignment |
| WF4-11 | Maintenance Engineer — Executor | Perform the maintenance work according to the approved maintenance order and record the work progress. | Maintenance work |
| WF4-12 | Maintenance Engineer — Executor | If additional damage or a significant cost increase is discovered, stop the additional work and submit a change request. | Change request |
| WF4-13 | Service Manager | Prepare a revised maintenance-order version based on the additional technical assessment. | Revised maintenance order |
| WF4-14 | Client | Approve or reject the change request before the Engineer performs the additional work. | Approved or rejected change |
| WF4-15 | Maintenance Engineer — Executor | Complete the approved work and upload before/after evidence, work logs, materials used, actual duration and final cost. | Maintenance completion report |
| WF4-16 | Service Manager | Check that the completion report, evidence and final cost are consistent with the approved maintenance order and approved changes. | Internally verified result |
| WF4-17 | Service Manager | Release the maintenance result to the Client . | Customer-visible maintenance result |
| WF4-18 | Client | Review the result and select Accept Resolution, Request Rework or Request Re-inspection. | Resolution decision |
| WF4-19 | System | If accepted, close the ticket and linked defect. If rework is requested, return the ticket to the execution stage. If re-inspection is requested, create a linked AD_HOC request for WF2. | Closed, rework or re-inspection state |
| WF4-20 | System | Finalize the actual cost, issue the invoice, record payment status, send notifications and preserve the audit history. | Completed maintenance record |

#### 3.5.1 Validation and Exception Requirements

- A technical assessment may be remote or on site, but must be performed by a qualified Maintenance Engineer.

- Material scope or cost growth stops additional work until the Client approves a versioned change order.

- Before/after evidence is required before closure.

- Rework returns to execution; re-inspection creates a linked ad hoc request for WF2.

### 3.6 Identity and Platform Administration

**Table 13 - Identity and administration requirements**

| ID | Function | Requirement and Acceptance Condition |
| --- | --- | --- |
| FR-IAM-01 | Issue Account | Admin creates an account with email, full name, actor zone, valid role set, and organization when required. The system issues a temporary credential; there is no public registration. |
| FR-IAM-02 | First Password Setup | A provisioned user must replace the temporary password before receiving normal application access. |
| FR-IAM-03 | Authenticate | The system authenticates email and password, returns a short-lived access token, and establishes a revocable web or mobile session. |
| FR-IAM-04 | Refresh Session | The system rotates the opaque refresh token. Expired, revoked, or reused tokens are rejected. |
| FR-IAM-05 | Change Password | The user supplies the current password and a compliant new password. Successful change invalidates existing sessions. |
| FR-IAM-06 | Assign Role | Admin assigns only role combinations allowed by the actor zone. Admin and Client roles remain exclusive; supported service roles may be combined. |
| FR-IAM-07 | Change Status | Admin may activate, suspend, or disable an account. Suspension or disablement revokes active sessions. |
| FR-IAM-08 | Protect Resources | Every protected request is denied by default unless role, organization/assignment scope, user status, session, and separation-of-duties checks pass. |

### 3.7 Shared Supporting Functions

**Table 14 - Shared supporting requirements**

| ID | Function | Requirement and Acceptance Condition |
| --- | --- | --- |
| FR-SYS-01 | Notifications | The system notifies the next responsible actor after material workflow transitions and records delivery status. |
| FR-SYS-02 | Audit | The system records login, account, authorization, assignment, approval, release, revision, and resolution events with timestamp and trace identifier. |
| FR-SYS-03 | Search and Pagination | List screens support server-side filtering, stable sorting, and pagination within the caller's authorized scope. |
| FR-SYS-04 | Problem Responses | API failures use RFC 7807 Problem Details with a stable code and traceId; authentication failures do not reveal whether an account exists. |
| FR-SYS-05 | File Access | Evidence and report downloads require an authorized request; raw object-storage URLs are not treated as authorization. |
| FR-SYS-06 | Dashboard | Operational counts and deadlines are calculated from source records and filtered by the signed-in role and resource scope. |

## 4. Non Functional Requirements

### 4.1 External Interfaces

**Table 15 - External interface requirements**

| ID | Interface | Requirement |
| --- | --- | --- |
| EI-01 | Web browser | Responsive React web portal over HTTPS; current Chrome, Edge, and Firefox versions supported. |
| EI-02 | Mobile application | Flutter client over HTTPS for Inspector and Maintenance Engineer workflows; tokens use platform secure storage. |
| EI-03 | REST API | Versioned JSON API under /api/v1 with OpenAPI in development and authenticated access in production. |
| EI-04 | MinIO | S3-compatible object storage for evidence and generated files; access mediated by backend authorization. |
| EI-05 | YOLO service | Image inference request/response containing evidence reference, model version, label, confidence, and bounding box. |
| EI-06 | Database | PostgreSQL is the source of truth for transactional state and audit metadata. |

### 4.2 Quality Attributes

**Table 16 - Quality attribute requirements**

| ID | Attribute | Measurable Requirement |
| --- | --- | --- |
| NFR-US-01 | Usability | A trained user can complete the primary role workflow without relying on developer tools; validation errors identify the affected field and corrective action. |
| NFR-US-02 | Usability | Web and mobile use consistent domain terms, date/time formats, status labels, and action placement. |
| NFR-US-03 | Accessibility | Keyboard navigation, visible focus, text alternatives, and contrast meet WCAG 2.1 AA for implemented web screens. |
| NFR-RL-01 | Reliability | Committed transactional records are not lost after application restart; multi-record state transitions are atomic. |
| NFR-RL-02 | Reliability | Periodic request generation is idempotent for Asset + Schedule + Due Cycle. |
| NFR-RL-03 | Reliability | External AI failure does not discard uploaded evidence or block manual finding entry. |
| NFR-PF-01 | Performance | Under the agreed test load, 95 percent of standard JSON API requests complete within 2 seconds excluding file transfer and third-party latency. |
| NFR-PF-02 | Performance | Paged list endpoints return at most the configured page size and do not load unbounded result sets into client memory. |
| NFR-PF-03 | Performance | Evidence upload reports progress and can retry an interrupted transfer without creating a duplicate database record. |
| NFR-SC-01 | Security | All non-public endpoints require authenticated access and deny by default. |
| NFR-SC-02 | Security | Authorization enforces role plus organization, assignment, ownership, or release scope as applicable. |
| NFR-SC-03 | Security | Passwords use Argon2id through Spring Security DelegatingPasswordEncoder and are never logged or returned. |
| NFR-SC-04 | Security | Browser refresh tokens use Secure, HttpOnly, SameSite=Strict cookies; browser access tokens remain in memory. |
| NFR-SC-05 | Security | Mobile tokens are returned only by the mobile auth contract and stored in secure platform storage; browser Origin requests to mobile auth are rejected. |
| NFR-SC-06 | Security | Secrets, API keys, refresh-token pepper, and production credentials are supplied outside source control. |
| NFR-PR-01 | Privacy | JWTs and logs exclude passwords, raw tokens, evidence content, and unnecessary personal profile data. |
| NFR-PR-02 | Privacy | Users can retrieve files only through authorized application requests; possession of an object path alone grants no access. |
| NFR-MN-01 | Maintainability | Backend modules own their domain, API, service, and repository code; Modulith tests enforce feature boundaries. |
| NFR-MN-02 | Maintainability | API contracts are versioned and documented; database schema changes use sequential Flyway migrations. |
| NFR-AT-01 | Auditability | Material security and workflow events include event type, outcome, actor or subject where applicable, timestamp, and trace identifier. |
| NFR-RC-01 | Recoverability | Database and object-storage backups are tested with a documented restore procedure before production release. |
| NFR-CM-01 | Compatibility | The web portal and mobile app consume the same versioned backend contract while using the token delivery profile appropriate to each client. |
| NFR-CF-01 | Configurability | Business thresholds, supported file rules, and integration endpoints are configuration or managed data rather than unexplained magic numbers in workflow code. |

## 5. Requirement Appendix

### 5.1 Business Rules

**Table 17 - Business rules**

| ID | Rule Definition |
| --- | --- |
| BR-01 | Admin, Client, and service-workforce identities use distinct actor zones; Admin and Client roles are exclusive. |
| BR-02 | A Client can access only data owned by the Client's organization. |
| BR-03 | An Inspector or Maintenance Engineer can access only work assigned to that user unless another explicit service role grants a separate scope. |
| BR-04 | An asset code is unique within its organization. |
| BR-05 | An active recurring schedule requires an active asset and an available checklist template. |
| BR-06 | Only one periodic request may be generated for the same Asset + Schedule + Due Cycle. |
| BR-07 | An ad hoc request must reference an asset owned by the Client's organization. |
| BR-08 | A quotation revision creates a new version; an approved historical version is retained. |
| BR-09 | No upfront payment is required for inspection or maintenance work. |
| BR-10 | An unconfirmed service order cannot proceed to Inspector assignment. |
| BR-11 | An Inspector assignment must be accepted before inspection status can become READY_FOR_INSPECTION. |
| BR-12 | Assignment rejection requires a reason and returns the work to the Service Manager. |
| BR-13 | Manual drone piloting and flight control remain outside SmartDroneInspection. |
| BR-14 | Each evidence object has a checksum; the same content cannot create duplicate evidence within the same inspection. |
| BR-15 | Missing GPS is recorded but does not invalidate otherwise acceptable evidence. |
| BR-16 | AI candidates are non-official until an Inspector confirms or modifies them. |
| BR-17 | Rejected and unverified AI candidates are excluded from official statistics and reports. |
| BR-18 | An Inspector may manually add a finding missed by AI. |
| BR-19 | The author of a report cannot be its peer reviewer. |
| BR-20 | A report cannot be released until a different Inspector technically approves it and the Service Manager confirms deliverable completeness. |
| BR-21 | Internal drafts and peer-review comments are hidden from the Client. |
| BR-22 | The Client may request clarification or revision but cannot directly edit technical report content. |
| BR-23 | An accepted report version is immutable; later correction creates a new version. |
| BR-24 | A maintenance ticket references at least one verified finding from a Client-accepted report. |
| BR-25 | The Service Manager does not independently create the technical maintenance estimate. |
| BR-26 | A qualified Maintenance Engineer supplies the technical assessment and estimate. |
| BR-27 | The estimate is a planning range and may differ from final actual cost. |
| BR-28 | Assessment and execution assignments are distinct even when assigned to the same Engineer. |
| BR-29 | A material scope or cost increase requires a versioned change request and Client approval before additional work. |
| BR-30 | Before/after evidence is required before a maintenance ticket can close. |
| BR-31 | Accept Resolution closes the ticket and linked defects; Request Rework returns to execution; Request Re-inspection creates a linked ad hoc request for WF2. |
| BR-32 | Final cost and invoice are recorded after completion and internal verification. |
| BR-33 | Passwords contain 15 to 128 Unicode characters and are not trimmed or normalized. |
| BR-34 | Login errors are generic and do not disclose whether an email exists. |
| BR-35 | Password change, role change, disablement, or logout-all revokes affected sessions. |

### 5.2 Common Requirements

**Table 18 - Common requirements**

| ID | Common Requirement |
| --- | --- |
| CR-01 | All timestamps are stored with time zone and displayed in the user's configured local time. |
| CR-02 | All identifiers exposed by the API use non-sequential UUID values unless an external reference requires another format. |
| CR-03 | Required text is validated for presence, permitted length, and domain format on both client and server; server validation is authoritative. |
| CR-04 | Mutation endpoints reject stale or invalid state transitions with a conflict response instead of silently overwriting a newer decision. |
| CR-05 | Search results are paginated and sorted deterministically. |
| CR-06 | Files are validated against configured type and size rules before they become workflow evidence. |
| CR-07 | API errors use RFC 7807 with code and traceId and never expose stack traces in production. |
| CR-08 | Deletion of business records is logical or restricted when audit/history relationships must be preserved. |
| CR-09 | Statuses are changed only by defined workflow actions; clients cannot set arbitrary status values. |
| CR-10 | Every decision that affects a customer-visible scope, cost, assignment, report, or resolution records the actor and timestamp. |
| CR-11 | Notification failure does not roll back a successfully committed business transition; it is recorded for retry or follow-up. |
| CR-12 | The same terminology and status names are used in SRS, API, UI, test cases, and demo data. |

### 5.3 Application Messages List

**Table 19 - Application messages**

| # | Type | Context | Content |
| --- | --- | --- | --- |
| MSG-001 | Inline | No matching list records | No results found. |
| MSG-002 | Field | Required value is empty | This field is required. |
| MSG-003 | Field | Input is longer than allowed | Maximum length is {maxLength} characters. |
| MSG-004 | Inline | Login fails | Email or password is incorrect. |
| MSG-005 | Toast | Asset saved | Asset saved successfully. |
| MSG-006 | Inline | Duplicate asset code | An asset with this code already exists in your organization. |
| MSG-007 | Toast | Schedule activated | Inspection schedule activated. |
| MSG-008 | Inline | Schedule cannot activate | Activate the asset and select an available checklist template first. |
| MSG-009 | Toast | Request submitted | Inspection request submitted. |
| MSG-010 | Inline | Quotation revision required | A newer quotation version is available. Review it before approval. |
| MSG-011 | Toast | Assignment accepted | Assignment accepted. |
| MSG-012 | Field | Assignment rejected without reason | Enter a rejection reason. |
| MSG-013 | Inline | Unsupported file | This file type is not supported. |
| MSG-014 | Inline | Duplicate evidence | This evidence file has already been uploaded. |
| MSG-015 | Toast | Upload complete | Evidence uploaded successfully. |
| MSG-016 | Inline | AI service unavailable | AI analysis is temporarily unavailable. You can continue manually. |
| MSG-017 | Inline | Unreviewed AI candidate | Review every AI candidate before submitting the inspection. |
| MSG-018 | Inline | Self peer review attempted | The report author cannot review this report. |
| MSG-019 | Toast | Report submitted | Report submitted for peer review. |
| MSG-020 | Toast | Report released | Report released to the Client. |
| MSG-021 | Inline | Ticket lacks defect | Select at least one verified defect. |
| MSG-022 | Inline | Unapproved additional work | Submit and obtain approval for a change request before continuing. |
| MSG-023 | Inline | Completion evidence missing | Upload before and after evidence before completing the work. |
| MSG-024 | Toast | Resolution accepted | Maintenance ticket and linked defects closed. |
| MSG-025 | Inline | Access denied | You do not have permission to access this resource. |
| MSG-026 | Inline | Session expired | Your session has expired. Sign in again. |

### 5.4 Requirement Traceability

**Table 20 - Requirement traceability summary**

| Flow | Use Cases | Functional Requirements | Business Rules | Demo Outcome |
| --- | --- | --- | --- | --- |
| WF1 | UC-04, UC-05, UC-06 | WF1-01 to WF1-08 | BR-02, BR-04 to BR-06 | Asset registration to periodic request generation |
| WF2 | UC-07 to UC-12 | WF2-01 to WF2-10 | BR-07 to BR-12 | Request, quotation, confirmed order, and accepted Inspector assignment |
| WF3 | UC-13 to UC-20 | WF3-01 to WF3-20 | BR-13 to BR-23 | Inspection, evidence, verified findings, peer review, release, and acceptance |
| WF4 | UC-21 to UC-28 | WF4-01 to WF4-20 | BR-24 to BR-32 | Maintenance assessment, order, execution, change, release, and resolution |
| Identity | UC-01, UC-02, UC-30 | FR-IAM-01 to FR-IAM-08 | BR-01, BR-33 to BR-35 | Account lifecycle and deny-by-default access control |

### 5.5 Abbreviations and Definitions

**Table 21 - Abbreviations and definitions**

| Term | Definition |
| --- | --- |
| AD_HOC | Inspection request created manually for a specific need rather than by a recurring schedule. |
| AI | Artificial intelligence; in this system, the YOLO image-analysis service that proposes defect candidates. |
| API | Application Programming Interface. |
| Client | Customer-organization actor mapped to the internal ORGANIZATION_MANAGER role code. |
| Evidence | Image or document stored with checksum, provenance, and authorization metadata. |
| Inspector Author | Inspector responsible for conducting the inspection and drafting its report. |
| Peer Reviewer | Different qualified Inspector who reviews the report's technical content. |
| PERIODIC | Inspection request created automatically for a due recurring schedule cycle. |
| SRS | Software Requirement Specification. |
| Verified Finding | Defect confirmed or manually added by an Inspector; eligible for official reports and maintenance. |
| WF1-WF4 | The four approved end-to-end business workflows defined in this SRS. |
| YOLO | External object-detection service that returns candidate labels, confidence values, and bounding boxes. |

### 5.6 Implementation Status Boundary

This document is the approved requirement baseline. A requirement is considered implemented only when the corresponding code, migration, test evidence, and demo path exist. At the time of this baseline, authentication and user administration have concrete backend implementation, while other feature modules are completed incrementally according to the project schedule. Test reports and demonstrations must distinguish implemented behavior from planned behavior.
