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

The system defines two governance layers and **four human roles**:

- **Platform Layer:**
  - `Platform Admin`: Governs customer enterprise tenant accounts, manages SaaS subscription lifecycles, configures system-wide parameters, and reviews security/audit logs. Platform administrators do not participate in operational inspection evaluations, repair budgeting, or technical work acceptance.

- **Customer Enterprise Layer:**
  - `Organization Admin`: Manages the enterprise workspace, including workforce accounts, professional credentials, drone fleet records, infrastructure assets with assigned Inspector-Drone pairs, flight permit compliance, and inspection mission dispatch. Conducts independent readiness authorization, approves final inspection reports, assigns maintenance teams, approves repair budgets, and performs final technical acceptance.
  - `Inspector`: Conducts on-site inspection activities. Prepares inspection shot-lists and compliance documentation, executes field survey sessions via the mobile application, uploads raw capture evidence, evaluates evidence completeness and quality, reviews and verifies AI defect candidates, authors inspection findings, and verifies the inspection report draft.
  - `Maintenance Engineer`: Executes corrective maintenance tasks. Assesses defect repair requirements, prepares itemized cost estimates (labor, material, equipment), records repair execution logs with before/after photographic proof, and drafts maintenance completion reports. Designated Engineers may serve as Maintenance Team Lead or Report Author.

Automated components (`SYSTEM`, YOLO11s AI Vision microservice, and LLM Report Drafting engine) provide automated data processing, candidate suggestions, and initial text synthesis. They operate strictly under human oversight and hold no legal, approving, or licensing authority.

**Core Operational Stages**

| Stage | Operational Scope | Primary Output |
| --- | --- | --- |
| Stage 1: Asset Onboarding & Inspection Scheduling | Organization Admin manages personnel, credentials, drone hardware, and regulatory permits; registers assets with default Inspector and Drone assignments; schedules inspection missions with conflict detection. | Scheduled inspection record with asset context, assigned pair snapshot, and compliance references. |
| Stage 2: Mission Preparation & Flight Execution | Inspector accepts assignment, prepares component shot-lists and pre-flight compliance; Organization Admin authorizes flight readiness; Inspector conducts field sessions and logs pre-flight checks and flight outcomes. | Completed field session record, pre-flight checklist notes, and survey execution logs. |
| Stage 3: Evidence Intake, AI Detection & Reporting | Inspector uploads raw capture media with SHA-256 verification and evaluates quality; YOLO11s detects defect candidates; Inspector verifies findings and drafts report; Organization Admin approves and publishes immutable PDF report. | Formally published inspection report with cryptographic checksum, and confirmed defects ready for maintenance. |
| Stage 4: Maintenance Remediation & Cost Control | Organization Admin creates work orders from confirmed defects and assigns engineering team; Team Lead plans tasks and estimates costs; Organization Admin approves budget; Engineers execute repairs and log before/after evidence; Organization Admin performs independent technical acceptance and cost reconciliation. | Closed work order with reconciled costs, documented repair proof, and updated asset condition history. |

**System Boundaries and Safety Disclaimers**

- **Flight Control Separation**: The software manages operational planning, compliance records, and inspection data. It does not interface directly with drone flight controllers, execute radio-control (RC) commands, or automate physical aircraft flight. Drone piloting remains the direct real-world responsibility of licensed remote pilots.
- **Airspace and Permit Compliance**: Informational airspace queries (e.g., restricted zone references) assist operational planning but do not constitute legal flight authorization. Enterprise administrators and remote pilots must obtain and verify valid flight permits from relevant aviation authorities (such as the Ministry of National Defence under Decree No. 288/2025/NĐ-CP).
- **Advisory AI Boundaries**: Computer vision detections and LLM report drafts are strictly advisory suggestions. Detections become official findings only upon explicit human Inspector verification. AI services cannot price maintenance work, certify legal compliance, or authorize report publication.
- **Payment Processing Scope**: Online payment processing is integrated specifically for enterprise SaaS subscription activation and renewal via PayPal REST API v2. Repair labor, material, and equipment actuals remain an internal enterprise cost accounting register, not an online e-commerce checkout.
- **Data Integrity and Legal Validity**: SHA-256 cryptographic hashing, audit timestamps, and append-only version histories ensure document and evidence traceability. System approvals represent recorded enterprise workflow decisions and do not substitute for statutory digital signatures unless explicitly configured with certified public-key infrastructure.

### 1.2 Business Rules

| ID | Rule Definition |
| --- | --- |
| BR-01 | Platform Admin accounts are platform-scoped; Organization Admin, Inspector, and Maintenance Engineer accounts are scoped strictly to their respective enterprise tenant. |
| BR-02 | An Organization Admin can access and manage only the assets, resources, inspections, reports, and maintenance records belonging to their own enterprise organization. |
| BR-03 | Workforce identities belong to a single enterprise tenant; no user account or operational role can bridge across organization boundaries. |
| BR-04 | Inspectors and Maintenance Engineers can access and act only upon inspection missions, work orders, or repair tasks explicitly assigned to them. |
| BR-05 | Active user accounts and valid professional credentials/permits are mandatory for mission release; expired or revoked credentials automatically block operational authorization. |
| BR-06 | Enterprise tenant registration, identity management, and subscription activation serve as supporting governance gates for the primary inspection and maintenance lifecycle. |
| BR-07 | Inspection preparation requires a defined component shot-list and mandatory pre-flight safety checklist prior to readiness submission. |
| BR-08 | Mission readiness authorization verifies valid flight permits, credential currency, and environmental suitability; internal approvals do not grant governmental flight exemptions. |
| BR-09 | Periodic inspection generation is idempotent per asset, schedule, and cycle, inheriting the asset's active default Inspector and Drone pair into the inspection snapshot. |
| BR-10 | ENTERPRISE is the sole platform subscription plan, supporting configurable billing periods of 1, 6, or 12 months with online payment settlement via PayPal or corporate billing records. |
| BR-11 | Subscription entitlements, service quotas, and contractual terms are versioned and audited; PayPal transactions record unique order and capture IDs for audit reconciliation. |
| BR-12 | Report drafts, cost estimate baselines, scope change requests, and approval decisions preserve complete version histories; published records cannot be modified in place. |
| BR-13 | Subscription renewal, cancellation, and expiration follow transparent contractual terms; subscription expiration preserves historical business records and does not auto-complete open work. |
| BR-14 | Remote pilots and Inspectors must record session postponement or abort whenever adverse weather or site conditions compromise flight safety. |
| BR-15 | An assigned Inspector must explicitly accept or reject an inspection assignment; rejection requires a mandatory justification and returns the mission to the administrator. |
| BR-16 | Aircraft flight operation and physical structural repair are real-world technical actions; system Start and End commands represent software session logging, not hardware actuation. |
| BR-17 | Uploaded digital evidence retains a server-calculated SHA-256 checksum, upload timestamp, and original capture metadata; missing telemetry is explicitly noted. |
| BR-18 | Duplicate evidence files within the same inspection scope are rejected based on SHA-256 checksum matching; upload retries are idempotent. |
| BR-19 | Absence of GPS coordinates or camera telemetry is recorded as missing metadata and does not automatically invalidate otherwise suitable visual evidence. |
| BR-20 | AI vision detections remain unconfirmed candidates until reviewed by a qualified Inspector; only human-verified findings enter the official inspection record. |
| BR-21 | Rejected AI defect suggestions are excluded from official defect metrics, inspection report deliverables, and maintenance repair scopes. |
| BR-22 | Inspectors may record manual defect findings backed by capture evidence; unavailability of AI services does not prevent manual inspection reporting. |
| BR-23 | The assigned Inspector is responsible for evaluating evidence quality and verifying every authored section of the inspection report before submission. |
| BR-24 | An Organization Admin distinct from the report author reviews findings and approves report publication; lack of independent review blocks publication. |
| BR-25 | Draft, returned, and unverified inspection content remains restricted to assigned authors and reviewers, strictly separated from published documents. |
| BR-26 | Published inspection report versions are immutable; subsequent corrections require creating a new linked revision with renewed administrative approval. |
| BR-27 | System workflows require explicit, attributable human decisions; no automated timer-based or silence-based approval is permitted for report publication or maintenance acceptance. |
| BR-28 | A returned inspection or maintenance report is directed back to its designated author with mandatory review comments while preserving prior version history. |
| BR-29 | Platform Admin provides technical SaaS governance and infrastructure maintenance, holding no authority over customer engineering assessments or repair budgets. |
| BR-30 | Application workflow approvals represent auditable software authorizations and do not constitute certified statutory signatures or governmental safety warranties. |
| BR-31 | Maintenance work orders must reference at least one confirmed defect requiring repair from a published inspection report within the same organization. |
| BR-32 | The designated Maintenance Team Lead prepares itemized repair estimates; automated systems do not generate arbitrary labor rates, material quantities, or prices. |
| BR-33 | Maintenance warranty and defect follow-up terms apply only when explicitly specified and contracted; no universal statutory warranty is presumed. |
| BR-34 | Any increase in repair scope, cost, or delivery schedule requires an approved Change Request prior to executing the additional work; the initial baseline remains immutable. |
| BR-35 | Maintenance completion reports require paired before-and-after photographic evidence and documented test results for each repaired defect. |
| BR-36 | Repair cost is an internal tenant cost register, separate from software subscription billing; PayPal online payment processes SaaS platform subscriptions, while internal repair actuals are operational expenditures. |
| BR-37 | A separate re-inspection creates a new linked inspection mission; additional evidence required for an existing inspection returns the mission to the preparation phase. |
| BR-38 | All assignment, readiness, evidence quality, finding verification, report publication, budget approval, and acceptance actions are logged in an immutable audit trail. |
| BR-39 | Direct URL access, notification links, and raw file paths confer no authority; backend multi-tenant boundary checks and role verifications remain mandatory on every request. |
| BR-40 | Password resets, role modifications, and session revocations immediately invalidate active tokens; user reassignment terminates future permissions without altering past audit logs. |
| BR-41 | Personnel credentials and drone equipment are registered in the resource catalog; mission-specific flight authorization is evaluated prior to starting field sessions. |
| BR-42 | Asset creation requires assigning exactly one responsible Inspector and one identified Drone; inspection mission dispatch inherits this operational pair snapshot. |
| BR-43 | The assigned Inspector holds sole authority to evaluate evidence completeness and quality; automated technical upload checks do not replace human quality review. |
| BR-44 | The inspection workflow follows a strict sequential gate: Evidence Quality Review → AI Defect Detection → Report Draft Synthesis → Author Verification → Admin Approval → Publication. |
| BR-45 | Each maintenance work order designates an approved engineering team, exactly one Team Lead, and one Report Author; neither may perform final acceptance on their team's work. |
| BR-46 | Every repair task is allocated to an approved team member; the Team Lead manages task assignments within approved membership, with all changes audited. |
| BR-47 | Financial totals for budgets, change orders, and actual expenditures are calculated using exact decimal precision; missing item costs cannot default to zero. |
| BR-48 | Automated language models synthesize report drafts exclusively from verified source records, preserving uncertainty disclosures and preventing fabricated assertions. |
| BR-49 | The designated Report Author verifies and submits the maintenance completion report; an independent Organization Admin performs final technical acceptance. |
