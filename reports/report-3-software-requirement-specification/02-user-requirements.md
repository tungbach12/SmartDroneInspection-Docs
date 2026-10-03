---
title: "Report 3 - User Requirements"
document_type: report3-srs-section
weight: 25
source: "report3-software-requirement-specification.docx"
---

## 2. User Requirements

### 2.1 System Actors

| # | Actor | Description |
| --- | --- | --- |
| 1 | Platform Admin (`PLATFORM_ADMIN`) | Manages technical platform infrastructure, authentication policies, security configurations, standard checklist templates, and system audit views. Platform Admin does not perform commercial operations, customer management, or dispute arbitration. |
| 2 | Platform Operator (`PLATFORM_OPERATOR`) | Manages business operations, vets Provider eligibility, publishes versioned commercial policies (one uniform commission, advance-funding terms, review period, cancellation, retention and warranty), coordinates supported payment-partner actions, and handles internal complaints under Platform Terms. Operator is not a legal arbitrator; policy updates are prospective and orders retain accepted snapshots. |
| 3 | Client (`CLIENT`) | Represents an infrastructure customer organization. Uses registered assets and schedules, issues inspection requests/RFQs, selects Providers, reviews and accepts electronic service terms, provides funding required by the accepted order through a supported payment partner, reviews deliverables, files complaints, and creates maintenance tickets. |
| 4 | Provider Manager (`PROVIDER_MANAGER`) | Executive/lead of an independent service provider company. Maintains company profile and pilot roster, reviews client RFQs, issues versioned quotations, coordinates Cục Tác chiến flight permits, assigns certified inspectors, and signs off QA reports. |
| 5 | Inspector (`INSPECTOR`) | Certified drone pilot and inspection technician employed by a service provider. Conducts field flight surveys, uploads chunked media with GPS/EXIF/SHA-256 to MinIO, confirms or rejects AI YOLO candidate findings, and performs cross peer reviews. Cannot approve self-authored reports. |
| 6 | Maintenance Engineer (`MAINTENANCE_ENGINEER`) | Repair technician employed by a maintenance provider. Performs defect assessments, provides technical estimates, executes physical maintenance work, and captures mandatory before/after photo evidence. |

### 2.2 Use Cases

#### 2.2.1 Diagram(s)

![SmartDroneInspection use cases](assets/use-cases.png)

#### 2.2.2 Descriptions

| ID | Use Case | Actors | Use Case Description |
| --- | --- | --- | --- |
| 01 | Authenticate User | All roles | Register an enterprise customer organization or sign in with an issued account, complete multi-factor verification, refresh active sessions, update passwords, and sign out. |
| 02 | Configure Technical Settings | Platform Admin | Configure technical platform parameters and infrastructure settings, standard checklist templates and security controls; cannot edit commercial policy. |
| 03 | Vet Service Provider | Platform Operator, Provider Manager | Submit company credentials, drone registration numbers per Luật PKND 2024, pilot licenses, and third-party insurance; Platform Operator verifies or rejects provider onboarding. |
| 04 | Register Infrastructure Asset | Client | Create and maintain the organization-scoped asset profile and source documents; optional public airspace lookup is informational and does not grant flight authorization. |
| 05 | Configure Commercial Policies | Platform Operator | Create and publish versioned, uniform commercial policies for all Providers, including commission, funding, review, cancellation, retention and warranty terms; record effective dates, audit actor and prospective-only change behavior. |
| 06 | Audit Platform Configurations | Platform Operator | Review version history and audit records for commercial policies; confirm the actor and effective time without modifying accepted order snapshots. |
| 07 | Solicit Quotations | Client | Publish an inspection request via direct provider selection or open RFQ with inspection objectives and known constraints; mission-specific GSD, overlap and capture targets are agreed in the SOW/Mission Plan. |
| 08 | Issue Inspection Quotation | Provider Manager | Submit versioned quotations covering Provider direct flight/engineering/logistics services and applicable tax, not separately charging Platform AI/data services. Display one Platform-published commission rate and fee-base rule accepted by all Providers before they accept new orders; the commission is a Provider expense, not an extra Client charge. |
| 09 | Approve Service Order | Client, Provider Manager | Review and approve quotation terms into a legally binding electronic service order under Luật Giao dịch điện tử 2023. |
| 10 | Fund Service Order | Client, System, authorized payment partner | Apply the advance-funding policy version and rate snapshotted in the order through an authorized partner product that supports the agreed terms. If no supported product exists, block this funding path or use a separately reviewed alternative; the Platform does not custody funds. |
| 11 | Plan Drone Mission | Provider Manager, Inspector | Create a versioned, equipment- and structure-specific mission plan with SOW-agreed GSD, overlap, AGL/waypoints and shot items; no universal numeric defaults are implied. |
| 12 | Authorize Flight Clearance | Provider Manager, Inspector | Check the applicable airspace status, provider drone registration, pilot credentials and required authority permit; block mission release until required clearance is verified. |
| 13 | Conduct Drone Survey | Inspector | Conduct field flight operations adhering to authorized parameters, safety zones, and checklist scope. |
| 14 | Upload Chunked Evidence | Inspector, System | Upload high-resolution imagery and video to Platform MinIO with server-computed checksum and available capture metadata for technical integrity and traceability, not as automatic proof of legal admissibility. |
| 15 | Verify Defect Candidates | Inspector, System | Review AI YOLO detections (cracks, spalling, corrosion); confirm, modify, reject candidates, or manually record unflagged defects. |
| 16 | Compile Draft Report | Inspector, System | Compile draft technical report with checklist answers, verified findings, and on-demand LLM narrative summary provided by Platform. |
| 17 | Peer-Review Inspection Report | Inspector | Review another Inspector's report within the same Provider; approve technical quality or request revisions (self-review strictly prohibited). |
| 18 | Release Inspection Report | Provider Manager | Verify deliverable completeness and release the final inspection report; start the client review period stored in the accepted order snapshot. |
| 19 | Review Final Report | Client | Review released report; accept deliverables, request clarification, or initiate complaint under the applicable order terms. |
| 20 | Settle Provider Payout | System, Platform Operator, authorized payment partner | At Client acceptance or an expressly agreed deemed-acceptance condition, process eligible funds and the order-snapshotted uniform commission policy `C = r × B`; settlement depends on an approved supported partner product and is target-only, not implemented. |
| 21 | File Contract Dispute | Client, Provider Manager | File an order-scoped contractual quality, safety, or payment complaint; request a partner hold only where the authorized payment product and accepted terms support it. |
| 22 | Resolve Contract Dispute | Platform Operator | Review the contract and traceable evidence, record an internal Platform Terms outcome, and coordinate only partner actions supported by the product and accepted terms; preserve access to court or commercial arbitration. |
| 23 | Create Maintenance Ticket | Client | Create repair ticket linked directly to verified defects from an accepted inspection report. |
| 24 | Assess Defect Condition | Maintenance Engineer | Perform remote or on-site defect assessment; submit required scope, materials, labor hours, and cost estimates. |
| 25 | Issue Maintenance Quotation | Provider Manager | Issue a versioned maintenance quotation; any retention and warranty terms must be disclosed, accepted and captured in the maintenance-order snapshot. |
| 26 | Approve Maintenance Order | Client, Provider Manager, authorized payment partner | Approve maintenance scope, configured funding/retention policy versions and the immutable policy values captured in the order; conditional release depends on a supported authorized payment-partner product. |
| 27 | Execute Maintenance Repair | Maintenance Engineer | Perform physical repair work according to approved scope; log materials and labor hours. |
| 28 | Capture Before-After Evidence | Maintenance Engineer | Upload mandatory paired before-and-after photo evidence to MinIO to substantiate repair completion. |
| 29 | Manage Maintenance Change | Maintenance Engineer, Client | Submit a versioned change order for unexpected conditions; additional work pauses pending Client approval and any funding required by the accepted maintenance policy and supported partner terms. |
| 30 | Verify Repair Completion | Client, Provider Manager, authorized payment partner | Inspect before/after evidence; if approved, release the milestone and start the warranty period according to the values snapshotted in the maintenance order. |
| 31 | Release Warranty Retention | System, Platform Operator, authorized payment partner | Release the retained portion after the order-snapshotted warranty period if the contract conditions are met and no unresolved claim remains; do not charge Platform commission twice on the same eligible service consideration. |
| 32 | Verify Telemetry Integrity | Inspector, System | Validate mission evidence against the approved plan and available GPS, altitude, gimbal, checksum and capture references; record missing metadata without claiming conclusive legal proof. |
