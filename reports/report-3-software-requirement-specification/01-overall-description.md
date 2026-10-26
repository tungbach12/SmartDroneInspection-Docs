---
title: "Report 3 - Overall Description"
document_type: report3-srs-section
weight: 15
source: "report3-software-requirement-specification.docx"
---

# II. Software Requirement Specification

## 1. Overall Description

### 1.1 Product Overview

SmartDroneInspection is an Enterprise, multi-tenant Software-as-a-Service (SaaS) platform engineered for infrastructure-owning enterprises (such as industrial plant operators, energy utilities, and civil engineering asset managers) to manage their physical infrastructure assets, drone fleet, personnel credentials, regulatory flight permits, inspection evidence, AI-assisted defect analysis, certified inspection reports, and maintenance remediation. The platform offers an ENTERPRISE subscription model supporting flexible billing intervals of 1 month, 6 months, or 12 months with integrated online payment processing via PayPal (supporting PayPal wallet and international credit/debit card checkout).

The software replaces manual, hazardous, and fragmented inspection practices with an end-to-end digital inspection and maintenance management workflow. The system integrates cloud-based multi-tenant management, mobile field applications, secure object storage, computer vision for defect detection (YOLO11s), and automated report drafting within strict human-in-the-loop review boundaries.

The system defines two governance layers and **five human roles**:

- **Platform Layer (strict single-role separation of duties: `ADMIN` XOR `PLATFORM_MANAGER`):**
  - `Platform Admin` (`ADMIN`): Governs multi-tenant platform technical administration, provisions and manages platform-level accounts (`ADMIN`, `PLATFORM_MANAGER`) and initial workspace accounts, maintains standard infrastructure asset categories, configures system-wide security policies, and reviews security/audit logs and read-only commercial views. Platform administrators do not approve commercial subscription or drone lease settlements and do not participate in operational inspection evaluations, repair budgeting, or technical work acceptance.
  - `Platform Manager` (`PLATFORM_MANAGER`): Governs platform commercial and equipment-leasing operations. Reviews enterprise subscription requests and negotiated pricing proposals, reconciles corporate wire/PayPal subscription payments to activate tenant entitlements, manages the platform's serial-numbered leasable drone pool (`platform_drones`), approves and provisions B2B drone lease contracts (`drone_leases`) into customer fleets, and reclaims leased drones upon contract completion.

- **Customer Enterprise Layer:**
  - `Organization Manager` (`ORG_MANAGER`): Manages the customer enterprise workspace (formerly `Organization Admin` / `ORG_ADMIN`), including enterprise subscription and B2B drone lease requests, workforce accounts, drone fleet records (owned and leased with registration data), infrastructure assets with standardized inspection checkpoints, direct inspection mission dispatch (selecting Inspector and Drone), approves final inspection reports, assigns maintenance teams, approves repair budgets, and performs final technical acceptance.
  - `Inspector` (`INSPECTOR`): Conducts on-site inspection activities. Self-declares remote pilot license credentials, uploads mission-specific flight permits, executes field survey sessions guided by asset inspection checkpoints via the mobile application, uploads raw capture evidence, reviews and verifies AI defect candidates, authors inspection findings, and verifies the inspection report draft.
  - `Maintenance Engineer` (`MAINTENANCE_ENGINEER`): Executes corrective maintenance tasks. Assesses defect repair requirements, prepares itemized cost estimates (labor, material, equipment), records repair execution logs with before/after photographic proof, and drafts maintenance completion reports. Designated Engineers may serve as Maintenance Team Lead or Report Author.

Automated components (`SYSTEM`, YOLO11s AI Vision microservice, and LLM Report Drafting engine) provide automated data processing, candidate suggestions, and initial text synthesis. They operate strictly under human oversight and hold no legal, approving, or licensing authority.

**Core Operational Stages**

| Stage | Operational Scope | Primary Output |
| --- | --- | --- |
| Stage 1: Asset Onboarding & Inspection Scheduling | Organization Manager registers assets with standardized inspection checkpoints (`inspectionItems`); registers owned and platform-leased drone hardware with registration data; schedules inspection missions with direct Inspector and Drone selection and conflict detection. | Scheduled inspection record in `ASSIGNED` status with asset context and assigned Inspector/Drone. |
| Stage 2: Self-Service Permit Gate & Field Execution | Inspector uploads mission flight permit, automatically transitioning inspection from `ASSIGNED` to `READY_FOR_FLIGHT`; Inspector conducts field sessions guided by asset inspection checkpoints and logs pre-flight checks and flight outcomes. | Completed field session record, pre-flight checklist notes, and survey execution logs. |
| Stage 3: Evidence Intake, AI Detection & Reporting | Inspector uploads raw capture media and evaluates coverage; YOLO11s detects defect candidates upon Inspector request; Inspector verifies findings and drafts report; Organization Manager approves and publishes immutable PDF report. | Formally published inspection report with cryptographic checksum, and confirmed defects ready for maintenance. |
| Stage 4: Maintenance Remediation & Cost Control | Organization Manager creates work orders from confirmed defects and assigns engineering team; Team Lead plans tasks and estimates costs; Organization Manager approves budget; Engineers execute repairs and log before/after evidence; Organization Manager performs independent technical acceptance and cost reconciliation. | Closed work order with reconciled costs, documented repair proof, and updated asset condition history. |

**System Boundaries and Safety Disclaimers**

- **Flight Control Separation**: The software manages operational planning, compliance records, and inspection data. It does not interface directly with drone flight controllers, execute radio-control (RC) commands, or automate physical aircraft flight. Drone piloting remains the direct real-world responsibility of licensed remote pilots.
- **Airspace and Permit Compliance**: Informational airspace queries (e.g., restricted zone references) assist operational planning but do not constitute legal flight authorization. Enterprise managers and remote pilots must obtain and verify valid flight permits from relevant aviation authorities (such as the Ministry of National Defence under Decree No. 288/2025/NĐ-CP).
- **Advisory AI Boundaries**: Computer vision detections and LLM report drafts are strictly advisory suggestions. Detections become official findings only upon explicit human Inspector verification. AI services cannot price maintenance work, certify legal compliance, or authorize report publication.
- **Payment Processing Scope**: Enterprise SaaS subscription requests and B2B drone lease contracts remain pending until a Platform Manager confirms a reconciled corporate wire/invoice payment (or PayPal checkout capture completes). PayPal Orders v2 is an optional deployment-configured channel, disabled by default; when enabled, the server creates and captures provider orders and verifies the provider-reported amount/currency and webhook signature. No browser-supplied capture ID or amount is treated as payment evidence. Repair labor, material, and equipment actuals remain internal enterprise cost records, not e-commerce checkout.
- **Data Integrity and Legal Validity**: SHA-256 cryptographic hashing, audit timestamps, and append-only version histories ensure document and evidence traceability. System approvals represent recorded enterprise workflow decisions and do not substitute for statutory digital signatures unless explicitly configured with certified public-key infrastructure.

### 1.2 Business Rules

| ID | Rule Definition |
| --- | --- |
| BR-01 | Platform Admin (`ADMIN`) and Platform Manager (`PLATFORM_MANAGER`) accounts are platform-scoped (`organization_id = null`) and enforce strict single-role separation of duties (`ADMIN` XOR `PLATFORM_MANAGER`); Organization Manager (`ORG_MANAGER`), Inspector (`INSPECTOR`), and Maintenance Engineer (`MAINTENANCE_ENGINEER`) accounts are scoped strictly to their respective enterprise tenant. |
| BR-02 | An Organization Manager can access and manage only the assets, resources, inspections, reports, and maintenance records belonging to their own enterprise organization. |
| BR-03 | Workforce identities belong to a single enterprise tenant; no user account or operational role can bridge across organization boundaries. |
| BR-04 | Inspectors and Maintenance Engineers can access and act only upon inspection missions, work orders, or repair tasks explicitly assigned to them. |
| BR-05 | Active user accounts and unexpired self-declared pilot licenses are mandatory for flight readiness; expired pilot licenses automatically block the self-service flight permit gate. |
| BR-06 | Enterprise tenant registration, identity management, subscription activation, and B2B drone leasing serve as supporting governance gates for the primary inspection and maintenance lifecycle. |
| BR-07 | Flight session start requires an unexpired flight permit and a mandatory pre-flight safety checklist note confirming aircraft, battery, and environmental suitability. |
| BR-08 | Self-service flight readiness verifies the uploaded flight permit and pilot license currency; software approvals do not grant governmental flight exemptions. |
| BR-09 | Inspection scheduling directly specifies the active Inspector and Drone for the mission, checking for scheduling conflicts across active missions. |
| BR-10 | ENTERPRISE subscriptions offer fixed standard pricing for 1-, 6-, and 12-month periods; custom 1–120-month durations and customer price proposals remain pending until a Platform Manager confirms a final amount and reconciled payment. Optional PayPal checkout is disabled by default and may settle only a platform-approved amount verified server-to-server. |
| BR-11 | Subscription and B2B drone lease requests preserve versioned terms and actor attribution; entitlement or leased drone provisioning begins only after authorized payment confirmation. Optional PayPal transactions record provider-issued order/capture IDs, server-verified amount/currency and settlement time, with duplicate captures rejected and webhook events signature-verified before application. |
| BR-12 | Report drafts, cost estimate baselines, scope change requests, and approval decisions preserve complete version histories; published records cannot be modified in place. |
| BR-13 | Subscription renewal, cancellation, and expiration follow transparent contractual terms; subscription expiration preserves historical business records and does not auto-complete open work. |
| BR-14 | Remote pilots and Inspectors must record session postponement or abort whenever adverse weather or site conditions compromise flight safety. |
| BR-15 | Inspections are dispatched directly to the designated Inspector and transition to `READY_FOR_FLIGHT` upon the Inspector's flight permit upload. |
| BR-16 | Aircraft flight operation and physical structural repair are real-world technical actions; system Start and End commands represent software session logging, not hardware actuation. |
| BR-17 | Uploaded digital evidence retains an upload timestamp, file identity, and original capture metadata; missing telemetry is explicitly noted. |
| BR-18 | Duplicate evidence files within the same inspection scope are rejected based on sanitized filename matching. |
| BR-19 | Absence of GPS coordinates or camera telemetry is recorded as missing metadata and does not automatically invalidate otherwise suitable visual evidence. |
| BR-20 | AI vision detections remain unconfirmed candidates until reviewed by a qualified Inspector; only human-verified findings enter the official inspection record. |
| BR-21 | Rejected AI defect suggestions are excluded from official defect metrics, inspection report deliverables, and maintenance repair scopes. |
| BR-22 | Inspectors may record manual defect findings backed by capture evidence; unavailability of AI services does not prevent manual inspection reporting. |
| BR-23 | The assigned Inspector is responsible for reviewing evidence coverage, authoring coverage/limitation disclosures, and verifying every authored section of the inspection report before submission. |
| BR-24 | An Organization Manager distinct from the report author reviews findings and approves report publication; lack of independent review blocks publication. |
| BR-25 | Draft, returned, and unverified inspection content remains restricted to assigned authors and reviewers, strictly separated from published documents. |
| BR-26 | Published inspection report versions are immutable; subsequent corrections require creating a new linked revision with renewed administrative approval. |
| BR-27 | System workflows require explicit, attributable human decisions; no automated timer-based or silence-based approval is permitted for report publication or maintenance acceptance. |
| BR-28 | A returned inspection or maintenance report is directed back to its designated author with mandatory review comments while preserving prior version history. |
| BR-29 | Platform Admin provides technical SaaS governance, platform user provisioning, and standard asset category maintenance, while Platform Manager governs commercial subscription and B2B drone lease settlements; neither holds authority over customer engineering assessments or repair budgets. |
| BR-30 | Application workflow approvals represent auditable software authorizations and do not constitute certified statutory signatures or governmental safety warranties. |
| BR-31 | Maintenance work orders must reference at least one confirmed defect requiring repair from a published inspection report within the same organization. |
| BR-32 | The designated Maintenance Team Lead prepares itemized repair estimates; automated systems do not generate arbitrary labor rates, material quantities, or prices. |
| BR-33 | Maintenance warranty and defect follow-up terms apply only when explicitly specified and contracted; no universal statutory warranty is presumed. |
| BR-34 | Any increase in repair scope, cost, or delivery schedule requires an approved Change Request prior to executing the additional work; the initial baseline remains immutable. |
| BR-35 | Maintenance completion reports require paired before-and-after photographic evidence and documented test results for each repaired defect. |
| BR-36 | Repair cost is an internal tenant cost register, separate from software subscription and B2B drone lease billing; PayPal online payment processes SaaS platform subscriptions and drone leases, while internal repair actuals are operational expenditures. |
| BR-37 | A separate re-inspection creates a new linked inspection mission; additional field coverage required for an existing inspection can be initiated directly via an additional field session in MF2. |
| BR-38 | All assignment, readiness, finding verification, report publication, budget approval, and acceptance actions are logged in an immutable audit trail. |
| BR-39 | Direct URL access, notification links, and raw file paths confer no authority; backend multi-tenant boundary checks and role verifications remain mandatory on every request. |
| BR-40 | Password resets, role modifications, and session revocations immediately invalidate active tokens; user reassignment terminates future permissions without altering past audit logs. |
| BR-41 | Owned and leased drone equipment records include government registration numbers and expiration dates. Pilot licenses are self-declared in inspector user profiles. Mission flight permits are uploaded per inspection. |
| BR-42 | Asset registration defines standardized structural inspection checkpoints (`inspectionItems`) inherited across inspections for on-site field survey guidance and technical reporting. |
| BR-43 | The assigned Inspector holds sole authority to evaluate evidence completeness and quality; automated technical upload checks do not replace human quality review. |
| BR-44 | The inspection workflow follows a strict sequential gate: Evidence Quality Review → AI Defect Detection → Report Draft Synthesis → Author Verification → Organization Manager Approval → Publication. |
| BR-45 | Each maintenance work order designates an approved engineering team, exactly one Team Lead, and one Report Author; neither may perform final acceptance on their team's work. |
| BR-46 | Every repair task is allocated to an approved team member; the Team Lead manages task assignments within approved membership, with all changes audited. |
| BR-47 | Financial totals for budgets, change orders, and actual expenditures are calculated using exact decimal precision; missing item costs cannot default to zero. |
| BR-48 | Automated language models synthesize report drafts exclusively from verified source records, preserving uncertainty disclosures and preventing fabricated assertions. |
| BR-49 | The designated Report Author verifies and submits the maintenance completion report; an independent Organization Manager performs final technical acceptance. |
