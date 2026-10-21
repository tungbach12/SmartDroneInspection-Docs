---
title: "Report 1 Project Introduction"
document_type: capstone-report
report_number: 1
source_docx: report1-project-introduction.docx
source_google_doc: "https://docs.google.com/document/d/1BTy_bPy7gZWQ4DpKzzTkUtTgripTy2iJRdyEgI0uxGk/edit"
retrieved: 2026-09-21
status: "historical-baseline — superseded by the four-role Enterprise SaaS target"
---

> **Status — 10 October 2026: HISTORICAL BASELINE, SUPERSEDED.** This report was written for the retired multi-provider marketplace target: six roles (`PLATFORM_OPERATOR`, `Provider`, `Client` and related), flows MF1–MF5, RFQ/quotation/electronic-contract, and pilot-credential judgement. **None of that is the current system.** The current target has **four** roles — `ADMIN`, `ORG_ADMIN`, `INSPECTOR`, `MAINTENANCE_ENGINEER` — and flows MF1–MF4, defined in [Report 3](../report-3-software-requirement-specification/) and [business-flows.md](../../project-reference/business-flows.md) v4.0.
>
> Role names, workflow step names, Figure 1 and any implementation claim in this document are historical and **must not** be presented as current product scope or as evidence of what the backend does. A label such as "MF1 — Survey Request, Quotation Sourcing & Electronic Contract" below means something entirely different from the current "MF1 — Resources, assets, pair assignment and inspection setup".
>
> **Before submission this report must be regenerated against the four-role target**, or its scope explicitly reduced to the background/introductory material that is still accurate. The same applies to [Report 2](../report-2-project-management-plan/), which shares this baseline.

# report 1

![Report 1 figure](assets/image2.png)

CAPSTONE PROJECT REPORT

Report 1 – Project Introduction

SmartDroneInspection

AI-powered Infrastructure Inspection-as-a-Service Platform

– Ho Chi Minh City, September 2026 –

Table of Contents

I. Record of Changes	3

II. Project Introduction	4

1. Overview	4

1.1 Project Information	4

1.2 Project Team	4

2. Product Background	4

3. Existing Systems	5

3.1 DroneDeploy Inspection AI	5

3.2 Flyability Inspector	5

4. Business Opportunity	5

5. Software Product Vision	6

6. Project Scope & Limitations	6

6.1 Major Features	6

6.2 Limitations & Exclusions	8

# I. Record of Changes

| Date | A* M, D | In charge | Change Description |
| --- | --- | --- | --- |
| 11 Sep 2026 | A | Team | Version 1.0: complete project-specific content and team information. |
| 12 Sep 2026 | M | Team | Version 1.1: clarified Review 1 target users and scope boundaries. |
| 21 Sep 2026 | M | Team | Version 1.2: aligned roles, Client organization self-registration, post-service billing milestones, and scope exclusions with the current business flow. |
| 21 Oct 2026 | M | Team | Version 1.3: integrated PayPal online checkout for Enterprise SaaS subscription billing, dynamic plan pricing, and aligned four-role governance model. |

*A - Added M - Modified D - Deleted

# II. Project Introduction

## 1. Overview

### 1.1 Project Information

- Project name: SmartDroneInspection: AI-powered Infrastructure Inspection Management Platform

- Project code: GFA26SE139

- Group name: FA26SE112

- Software type: Responsive Web Portal, Flutter Field Application, REST APIs and server-side AI services

### 1.2 Project Team

| Full Name | Role | Email | Mobile |
| --- | --- | --- | --- |
| Phạm Minh Trí | Lecturer | tripm14@fpt.edu.vn |  |
| Đặng Ngọc Minh Đức | Lecturer | ducdnm2@fpt.edu.vn |  |
| Trần Hoàng Trung Hiếu | Leader | hieuthtse184212@fpt.edu.vn | 0963832382 |
| Phùng Trung Quốc | Member | quocptse170027@fpt.edu.vn | 0896986551 |
| Trương Thái Như | Member | nhuttse180082@fpt.edu.vn | 0328416716 |
| Trần Tùng Bách | Member | bachttse180220@fpt.edu.vn | 0378351050 |

## 2. Product Background

Organizations that own or manage infrastructure assets need to perform inspections regularly to identify defects, assess asset conditions, and verify repairs. In practice, inspection requests, captured images, findings, approvals, and maintenance updates may be handled through separate tools or manual processes, making it difficult to track the latest condition and resolution status of each defect. This can lead to fragmented information, slower follow-up, and difficulty connecting inspection evidence with the related asset and maintenance activity. SmartDroneInspection is proposed to centralize this process in a shared platform for requesting inspection services, managing inspection evidence, reviewing findings, and tracking defect resolution. The intended customers are organizations that own or manage infrastructure assets and require inspection services.

## 3. Existing Systems

The following products provide relevant references for inspection evidence, findings and reporting. Their published capabilities inform the design comparison; the scope-fit observations below are project assessments, not claims that the products lack all other capabilities.

### 3.1 DroneDeploy

Description: DroneDeploy is a cloud-based drone data platform for flight planning, image processing, inspection, analysis, and reporting.

Actors: Organization Owner/Admin, Coordinator, Member, External User, Pilot, Editor/Analyst, Upload-only User, and Viewer.

Main features: Automated flight planning, drone image upload and processing, 2D/3D mapping, measurements, issue tagging, inspection reports, collaboration, and permission management.

Pros: Provides an integrated inspection workflow, strong visualization and analysis tools, flexible access control, and good support for collaboration.

Cons: Advanced features may require higher-tier plans, some inspection tasks are more desktop-oriented, and its workflow focuses more on drone data and inspection management than on service-order processes such as quotations, deposits, provider assignment, and remediation requests.

Reference: DroneDeploy, https://www.dronedeploy.com/

### 3.2 Flyability Inspector

Description: Flyability Inspector is companion software designed for organizing, reviewing, and reporting inspection data captured by Elios 3 drones.

Actors: Inspection Teams, Engineers, and Asset Owners.

Main features: Asset-based organization, visual review with points of interest (POI), spatial context mapping, historical data comparison over time, structured report generation, and stakeholder collaboration.

Pros: Allows findings to be reviewed with strong visual and spatial context, and supports inspection history comparisons over time.

Cons: Specialized specifically for Elios 3 data rather than general service management or standard uploaded-image workflows, and lacks a built-in 3D digital-twin requirement for this project's scope.

Reference: Flyability, “Inspector”, https://www.flyability.com/inspector (accessed 11 September 2026).

## 4. Business Opportunity

Infrastructure owners need a more convenient way to purchase, manage, and track occasional or recurring inspection services. When service requests, quotations, inspection evidence, findings, reports, and defect follow-up are handled separately, customers may have difficulty understanding the current status of an inspection or tracing a defect from discovery to resolution. SmartDroneInspection provides a shared platform where customers can define inspection needs, review and confirm service orders, access inspection evidence and reports, and follow defect resolution. For the service provider, the same platform supports resource allocation and maintains a traceable history of inspection activities.

Compared with solutions that primarily focus on drone data capture, mapping, or inspection analysis, SmartDroneInspection focuses on connecting inspection-service ordering with evidence management, AI-assisted defect detection, reporting, and follow-up activities. This makes the proposed system suitable for organizations that need inspection services without operating their own inspection teams or drone infrastructure. The expected benefits are clearer service coordination, easier retrieval of inspection evidence, more consistent defect follow-up, and better visibility of service progress.

## 5. Software Product Vision

For organizations that need reliable infrastructure inspection services without managing an internal provider workforce, SmartDroneInspection is a B2B web and field application that connects service requests and confirmed prices to manual field inspections, human-verified AI findings, customer-approved reports, and separately ordered remediation.

Unlike fragmented manual communications and generic software lacking complete service workflows, SmartDroneInspection gives customers a clear record of what was purchased, what was observed, who verified the findings, and how defects were resolved. It gives the service provider a consistent way to allocate resources and deliver traceable evidence, prioritizing a demonstrable end-to-end service lifecycle with a limited, validated AI detection scope.

## 6. Project Scope & Limitations

The software product scope is structured around an Enterprise, multi-tenant Software-as-a-Service (SaaS) architecture engineered for infrastructure-owning enterprises to manage their physical assets, drone fleet, personnel credentials, regulatory permits, inspection evidence, AI-assisted defect analysis, certified inspection reports, and maintenance remediation. The platform offers an ENTERPRISE subscription model supporting flexible billing intervals of 1 month, 6 months, or 12 months with integrated online payment processing via PayPal (supporting PayPal wallet and international credit/debit card checkout).

The operational lifecycle is organized into four core stages:

- **Stage 1: Asset Onboarding & Inspection Scheduling**: Organization Admin manages enterprise workforce accounts, credentials, drone hardware, and regulatory flight permits; registers physical infrastructure assets with default Inspector-Drone operational assignments; schedules inspection missions with automated schedule conflict detection.
- **Stage 2: Mission Preparation & Flight Execution**: Inspector accepts the assigned mission, prepares component shot-lists and pre-flight compliance; Organization Admin authorizes flight readiness; Inspector logs field survey sessions via the mobile app with pre-flight safety checks and capture notes.
- **Stage 3: Evidence Intake, AI Detection & Reporting**: Inspector uploads raw capture media with SHA-256 integrity verification and evaluates quality; YOLO11s detects defect candidates; Inspector verifies findings and authors the report draft; Organization Admin reviews, approves, and publishes the immutable PDF report deliverable.
- **Stage 4: Maintenance Remediation & Cost Control**: Organization Admin creates work orders from confirmed defects and assigns the engineering team; Team Lead plans repair tasks and itemized cost estimates (labor, materials, equipment); Organization Admin approves the repair budget; Engineers execute repairs and log paired before/after photographic evidence; Organization Admin performs independent technical acceptance and cost reconciliation.

**Governance Model and Roles**

The platform supports four human roles across two operational zones:
- **Platform Layer**: `Platform Admin` (`ADMIN`) governs customer tenant workspaces, manages subscription pricing catalogs and resource quotas, verifies PayPal billing records, configures system-wide parameters, and audits access. Platform Admin does not participate in customer operational evaluations or repair budgeting.
- **Customer Enterprise Layer**: `Organization Admin` (`ORG_ADMIN`) manages company assets, fleet, workforce credentials, mission authorizations, report releases, and maintenance acceptance; `Inspector` (`INSPECTOR`) accepts missions, completes pre-flight checks, captures evidence, verifies AI candidates, and authors report drafts; `Maintenance Engineer` (`MAINTENANCE_ENGINEER`) executes repairs, logs actuals with before/after evidence, and drafts completion reports.

**Payment Processing Boundaries**

Online payment processing is integrated specifically for enterprise SaaS subscription activation and renewal via the PayPal REST API v2 (Orders v2 API and asynchronous IPN webhooks for automated quota unlocking and subscription term extension). Repair labor, material, and equipment actuals remain an internal enterprise cost accounting register (operational expenditures), not an online e-commerce checkout.

The proposed product is evaluated against *Luật Phòng không nhân dân 2024 (Luật số 49/2024/QH15, as amended)*, *Nghị định 198/2025/NĐ-CP*, *Nghị định 288/2025/NĐ-CP*, and published restricted-airspace information at `cambay.mod.gov.vn`. Electronic contracts and data messages follow *Luật Giao dịch điện tử 2023*; GPS coordinates and SHA-256 cryptographic hashes support traceability but do not automatically create conclusive legal evidence.

The project may include assembling and configuring a prototype drone using commercially available components for demonstration and system integration. The drone is manually operated using its designated controller and is used to capture inspection evidence for upload to SmartDroneInspection.

The project does not include fully autonomous drone operation, custom flight-control algorithms, commercial-grade drone manufacturing, or a complete 3D digital-twin platform. AI-generated defect candidates must be reviewed by an Inspector and do not replace professional judgment. The capstone release is limited to the defined inspection and maintenance workflows; additional hardware, advanced analytics, or commercial features are outside the current scope unless formally approved as a scope change.

### 6.1 Major Features

Feature identifiers FE-01 to FE-08 form the scope baseline for requirements, work estimates, and acceptance tests.

FE-01: Identity, Enterprise Subscription & Access Governance. Enterprise tenant registration, workforce account provisioning, professional credential tracking, and online ENTERPRISE subscription billing integrated with PayPal REST API v2 (Orders v2 checkout, IPN webhook listeners, and corporate billing records).

FE-02: Asset Registry & Inspection Schedule. Organization-scoped master inventory of physical infrastructure assets, drone fleet serviceability, regulatory flight permit linkage, and idempotent periodic inspection schedule generation.

FE-03: Inspection Mission Planning & Readiness Authorization. Mission shot-list preparation, component target definition, pre-flight safety checklists, and administrative flight readiness review.

FE-04: Inspection Execution & Evidence Management. Flutter mobile field application supporting assignment acceptance, survey session logging, pre-flight safety checklist completion, tamper-evident MinIO object storage uploads with SHA-256 checksums, and substantive evidence quality review.

FE-05: YOLO-assisted Defect Detection & Verification. Server-side defect detection microservice (Ultralytics YOLO11s trained on MBDD2025) generating candidate bounding boxes and classifications; Inspector human-in-the-loop review (Confirm, Modify, Reject, Manual Add).

FE-06: Inspection Report & Administrative Review. Context-grounded LLM narrative drafting, Inspector author verification, administrative approval, and cryptographic publication of A4 PDF reports with embedded defect summaries and SHA-256 digests.

FE-07: Maintenance Remediation & Cost Control. Corrective maintenance work orders generated from confirmed defects, task assignment, itemized baseline cost estimation (labor, materials, equipment), change order variance control, paired before/after photographic proof, and independent technical acceptance.

FE-08: Dashboard, Analytics & Notifications. Role-scoped dashboards summarizing mission status, asset health condition history, defect trends, and maintenance progress, with event-driven notifications for mission readiness and approvals.

![Report 1 figure](assets/image15.png)

Figure 1. Core operational workflow diagram from inspection planning through field capture, AI defect verification, certified reporting, and maintenance remediation.

### 6.2 Limitations & Exclusions

The first release is limited to infrastructure inspection and maintenance management. The following items define either excluded capabilities or mandatory product constraints. These boundaries apply to the software release and project demonstration; they do not prevent the system from retaining records for the supported inspection-to-maintenance lifecycle.

LI-1: The platform does not provide autonomous drone flight control, flight-path programming, drone piloting, or automatic drone telemetry collection. Manual capture may occur outside the platform, but only authorized evidence is uploaded and managed by the product.

LI-2: AI is limited to generating candidate findings. An Inspector must review and verify each candidate before it can become an official finding. The system does not automatically publish AI-generated findings.

LI-3: A Client representative may self-register a new customer organization and its first Client account. Provider organization onboarding requires separate Platform Operator review. Self-registration cannot grant `PLATFORM_ADMIN`, `PLATFORM_OPERATOR`, `PROVIDER_MANAGER`, `INSPECTOR`, or `MAINTENANCE_ENGINEER` roles. Anonymous access to protected system data is not supported.

LI-4: Access is scoped by customer organization, provider organization, and accepted assignment. A Client cannot view another customer's records; a Provider cannot view a competitor's quotation, workforce, or evidence; an Inspector or Maintenance Engineer can access only authorized assigned work. Platform Admin and Operator have separate technical and business authority.

LI-5: An inspection report version accepted by the Client is immutable. Any subsequent correction or change must create a new version and preserve the previously accepted version.

LI-6: General-purpose photogrammetry, 3D reconstruction, and unrelated consumer use are outside the product scope.

LI-7: Integration with external drone-management platforms or other unconfirmed third-party systems is excluded from the release. The system does not provide certified digital-signature services; approval is recorded as an authenticated and versioned application record.
