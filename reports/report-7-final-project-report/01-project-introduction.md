---
title: "Report 7 - Project Introduction"
document_type: report7-section
weight: 10
source: "Report7_Final Project Report.docx"
---
# Acknowledgement

The team thanks its supervisors for their guidance across the planning, design, build, and testing phases of this capstone project. Their reviews of the requirement specification and the design document shaped both the scope and the rigour of the delivered system.

The team also thanks the lecturers of the Software Engineering programme at FPT University for the foundation on which this work rests, and the customer and partner organisations that reviewed early builds and gave the feedback that turned an inspection concept into a working service.

Finally, the team thanks the open-source communities behind Spring Boot, Spring Modulith, React, Flutter, PostgreSQL, MinIO, Ultralytics YOLO, and FFmpeg. This product is built on their work.

# Definition and Acronyms

| Acronym | Definition |
| --- | --- |
| `ADMIN` | Platform Administrator |
| AI | Artificial Intelligence |
| API | Application Programming Interface |
| `BR` | Business Rule |
| CDD | Containerized Database Deployment |
| `CUSTOMER` | Building owner or customer account holder |
| ERD | Entity Relationship Diagram |
| `FE` | Feature |
| FFmpeg | Fast Forward Moving Picture Experts Group (media toolkit) |
| HMAC | Hash-based Message Authentication Code |
| `INSPECTOR` | Partner Drone Inspector |
| JWT | JSON Web Token |
| `MANAGER` | Platform Manager |
| `MF` | Main Flow |
| MinIO | High-performance S3-compatible object storage |
| MP4 | MPEG-4 Part 14 (video container) |
| NFR | Non-Functional Requirement |
| OAuth | Open Authorization |
| PDF | Portable Document Format |
| RBAC | Role-Based Access Control |
| SDD | Software Design Description |
| SRS | Software Requirement Specification |
| `UC` | Use Case |
| VND | Vietnamese Dong |
| VNPay | Vietnam Payment Solution Joint Stock Company gateway |
| YOLO | You Only Look Once (object detection model family) |

# I. Project Introduction

## 1. Overview

### 1.1 Project Information

- **Project name:** SmartDroneInspection — AI-Powered Infrastructure Inspection Coordination Platform
- **Project code:** GFA26SE139
- **Group name:** FA26SE112
- **Software type:** Web application, native mobile application, and self-hosted AI detection service

### 1.2 Project Team

| Full Name | Role | Email | Mobile |
| --- | --- | --- | --- |
| Trần Hoàng Trung Hiếu (`SE184212`) | Leader | hieuthtse184212@fpt.edu.vn | 0963832382 |
| Phùng Trung Quốc (`SE170027`) | Member | quocptse170027@fpt.edu.vn | 0896986551 |
| Trần Tùng Bách (`SE180220`) | Member | bachttse180220@fpt.edu.vn | 0378351050 |
| Trương Thái Như (`SE180082`) | Member | nhuttse180082@fpt.edu.vn | 0328416716 |
| Phạm Minh Trí | Supervisor | tripm14@fpt.edu.vn | — |
| Đặng Ngọc Minh Đức | External Supervisor and Lecturer | ducdnm2@fpt.edu.vn | — |

## 2. Product Background

Roofs, facades, and other exterior building surfaces can be difficult to inspect from the ground. Drone imagery helps inspectors document these areas and compare observations across visits. When quotations, permits, evidence, and reports are handled separately, it is harder to trace a reported finding back to the inspection that produced it.

SmartDroneInspection connects the service request, quotation, Inspector and drone assignment, permit record, field evidence, findings, published report, and payment. Partner Inspectors conduct the flights and verify findings. The platform records their work and supports review with image analysis.

## 3. Existing Systems

Three existing products were studied as comparators. Each solves part of the problem; none of them solves the coordination problem that this project targets.

### 3.1 DroneDeploy

- **Description:** A cloud platform for drone-based aerial mapping and site documentation, widely used in construction and agriculture, with photogrammetry, progress tracking, and machine-learning analysis of aerial imagery.
- **Link:** https://www.dronedeploy.com
- **Pros:** Mature flight planning and automated capture; strong photogrammetric reconstruction and site-accuracy tooling; a large integration ecosystem; well-suited to comparing site progress across time.
- **Cons:** Oriented toward the organisation that operates its own drones, so a building owner without a flight operation is not the primary user; no partner-marketplace model for dispatching an independent licensed inspector; the commercial chain from request to quotation to signed agreement to settlement sits outside the product.

### 3.2 Flyability Inspector

- **Description:** A software suite and collision-tolerant indoor drone offering for confined-space and indoor inspection, with a structured inspection workflow and reporting aimed at asset owners and inspection service companies.
- **Link:** https://www.flyability.com
- **Pros:** Excellent fit for confined and indoor spaces where a conventional drone cannot safely fly; a structured, checklist-driven inspection flow; inspection-grade image and video capture; report generation built into the workflow.
- **Cons:** Hardware-coupled, so adopting it means adopting a specific aircraft; aimed mainly at industrial assets rather than the broader building portfolio; no cross-organisation dispatch of independent partner pilots and no customer-facing settlement process.

### 3.3 Skycatch

- **Description:** An enterprise drone data platform focused on construction and mining, providing automated capture, 3D reconstruction, volumetric analysis, and integration with project management systems.
- **Link:** https://www.skycatch.com
- **Pros:** Strong automation of the capture-to-model pipeline; useful volumetric and progress analytics; designed to feed existing project-management systems rather than replace them; industry-specific reporting.
- **Cons:** Mining and earthworks focus means building envelope defects such as facade cracks and leakage are not its primary detection target; no inspection-specific lifecycle from permit submission to independent report publication; not aimed at a marketplace of partner inspectors.

The three products reviewed focus on capturing or analysing drone imagery. SmartDroneInspection focuses on coordinating a building inspection between independent parties, from partner qualification and assignment to report publication and payment.

## 4. Business Opportunity


Building owners and facility operators need periodic inspections of roofs, facades, and other exterior surfaces. Licensed drone pilots can provide this service using their own equipment.

When quotations, flight records, and reports are shared separately, it is harder for an owner to verify what was agreed or trace a finding back to its evidence.

A shared inspection record helps owners plan repeat inspections and gives Inspectors a record of completed work.

## 5. Software Product Vision

SmartDroneInspection gives building owners, Managers, and Partner Inspectors a shared record from quotation and assignment through report publication and payment. AI suggests defects from uploaded evidence. The Inspector confirms findings before they appear in an official report.

## 6. Project Scope & Limitations

### 6.1 Major Features (`FE-01`–`FE-24`)

Twenty-four atomic product features define the delivered scope across the four main operational flows (`MF1`–`MF4`):

**Main Flow 1 (`MF1`) — Identity, Partner/Drone Onboarding & Airspace Screening (`FE-01`–`FE-04`)**

1. **`MF1` `FE-01` — Account Authentication, OTP & 4-Role Access Control.** Customer account and initial building onboarding, password sign-in with lockout and email one-time-code verification, Google sign-in across web and mobile, session refresh management, self-service profile updates, bilingual UI, and strict four-role access boundaries across Administrators, Managers, Customers, and Inspectors.
2. **`MF1` `FE-02` — Partner Inspector Application & Qualification Management.** Public partner application with pilot-licence scan, safe duplicate-email handling, platform review and account creation upon approval, pilot-licence qualification profiles, flight history logs, and automated expiry readiness checks.
3. **`MF1` `FE-03` — Inspector-Owned Drone Registration & Fleet Management.** Administrator-configurable document and capability requirements, Inspector drone submission/renewal with required documents, at least one real photograph, weight classification, and active, maintenance, or retired serviceability states.
4. **`MF1` `FE-04` — Interactive Location Map & No-Fly Zone Airspace Screening.** Interactive Vietnam map coordinate picker across web and customer mobile, coordinate validation, and airspace zone screening refusing prohibited locations while displaying advisory restricted-zone warnings (`MSG28`).
5. **`MF4` `FE-05` — Financial History & Revenue/Payment Ledger.** Role-scoped Customer payment history, Inspector payout/receivable ledger, and Manager platform revenue, commission, and tax views without cross-organization data leakage.

**Main Flow 2 (`MF2`) — Buildings, Airspace Screening, Commercial Service, Messaging & Notifications (`FE-06`–`FE-12`)**

6. **`MF2` `FE-06` — Building Asset Registry, Checkpoints & Reference Documents.** Building registry across six supported structural categories with plain-text ownership details, structural specifications, default inspection checkpoints (locked read-only once an inspection exists), duplicate-free reference documents, and permanent retirement locking.
7. **`MF2` `FE-07` — Restricted Airspace Advisory Warning & Immediate Onboarding.** Customers can save buildings in clear and restricted zones. The restricted-zone advisory explains the permit requirement and links to airspace rules. No-fly zones block building registration.
8. **`MF2` `FE-08` — Service Requests (One-Time & Recurring) & VND Quotations.** Compact commercial request and quotation workflow with concise recurring titles, checkpoint snapshots (`V80`), monthly cadence rules (2–100 occurrences, 20-day lead time), month-end date anchoring, single-Manager claim with direct detail view, and VND quotation negotiation.
9. **`MF2` `FE-09` — Offline Signed Contract & Occurrence Dispatch Scheduling.** Signed paper agreement recording, automatic creation of recurring inspection occurrences, cross-organization schedule-conflict and qualification checks before dispatch, bulk crew assignment, abort recovery, and mobile tracking parity.
10. **`MF2` `FE-10` — Messaging (Order Chat, Partner Chat & Inspection Chat).** Separated Customer–Manager commercial order chat, Manager–Partner Inspector pre-dispatch coordination chat (`V79`), and private Customer–Inspector per-inspection coordination chat supporting up to five verified attachments (`10 MiB`/file, `20 MiB`/message), Administrator exclusion, and read-only Manager contact cards.
11. **`MF2` `FE-11` — Assignment Acceptance Timeout & Escalation Handling.** Administrator-configurable assignment acceptance deadline (default 24 hours) enforced automatically to cancel unaccepted dispatches, free crew schedules, return occurrences for reassignment, and notify the owning Manager.
12. **`MF2` `FE-12` — System Notifications & Alert Center.** Reliable, duplicate-free bilingual (Vietnamese and English) in-app and SMTP critical notification center across all five workflow pillars, supporting `PATCH /api/v1/notifications/read-all`, unread badge counters, and safe deep links respecting access boundaries.

**Main Flow 3 (`MF3`) — Flight Permits, Field Execution, Evidence Pipeline & AI Defect Analysis (`FE-13`–`FE-17`)**

13. **`MF3` `FE-13` — Flight Permit Upload & Self-Attestation Gate.** Mission flight permit upload (`<= 25 MB` verified file with permit number, issuing authority, validity dates, and drone serial) immediately granting `APPROVED` readiness via assigned Inspector self-attestation, automatic reset to `PENDING_REVIEW` if the drone swaps or schedule moves outside validity, pre-session enforcement, and read-only Manager permit audit views.
14. **`MF3` `FE-14` — On-Site Field Session & SmartDroneHub MAVLink Telemetry.** Field session lifecycle (start, complete, or reasoned abort reopening the occurrence), multi-sortie flight tracking (`field_session_flights`, `V72`), read-only SmartDroneHub telemetry and GPS trace capture for the assigned Inspector, imported flight-log and manual flight declarations, role dashboards, and Inspector schedule calendar. The owning Customer can view flight data once the inspection report is published.
15. **`MF3` `FE-15` — Field Evidence Intake & Chunked Video Processing Pipeline.** Metadata-preserving photo intake with automatic upright sizing and thumbnails, duplicate filename auto-numbering, resumable `2 GiB` chunked MP4 video uploads, background playback optimization, and secure time-limited video streaming.
16. **`MF3` `FE-16` — AI Defect Detection (`YOLO11` + Vision Fallback) & Findings Confirmation.** Automated detection of five building defect classes on photos and video frames (`70%` default auto-confirm setting), optional secondary vision fallback respecting user opt-out, confirmation status filters (`All active`, `Unconfirmed`, `Confirmed`), explicit Inspector baseline confirmation, and fresh re-inspection evidence checks.
17. **`MF3` `FE-17` — AI Case/Standard Retrieval (`pgvector` RAG), Note Drafting & Report Summary.** Tenant-isolated `DroneKnowledgeAI` recommendation advisor retrieving relevant historical defect cases and engineering standards with keyword fallback, finding-level `Draft note with AI` and batch `Draft all notes`, collapsible mobile references, and AI executive summary grounding.
18. **`MF4` `FE-18` — Inspection Report Compilation, Independent Review & Official Publication.** Four-state report lifecycle (`Submitted`, `Returned`, `Approved`, `Published`, `Superseded`), consistent compilation from confirmed findings, independent Manager review banning self-publication (`MANAGER`-only adjudication; `ADMIN` read-only), on-demand A4 PDF export once `PUBLISHED`, and version history preservation.

**Main Flow 4 (`MF4`) — Report Publication, Acceptance, Payment Settlement, Financial Ledger & Re-inspection (`FE-05`, `FE-18`–`FE-24`)**

19. **`MF4` `FE-19` — Customer Report Acceptance & Clarification Workflow.** Customer review of published inspection reports, structured Customer/Manager Inspector Rating (`inspector_ratings` `V70`, configurable criteria `V73`), formal deliverable acceptance gating commercial invoicing, and Customer-only pre-acceptance clarification requests.
20. **`MF4` `FE-20` — Online Service Fee Payment (`Sepay` VietQR & `VNPay`).** Online checkout via Sepay (VietQR) and VNPay with verified gateway callbacks (`V67`–`V68`), authorized manual payment fallback when gateways are disabled, and automatic payout eligibility updates.
21. **`MF4` `FE-21` — Payment Deadlines, Invoices & Payment Document Management.** Acceptance-stamped payment due deadline (default 15 days), single daily overdue reminder without revoking report access, and downloadable non-tax-invoice payment notice and receipt PDFs across web and mobile.
22. **`MF4` `FE-22` — Partner Inspector Payout Reconciliation.** Integrated `Approved -> Sepay VietQR Payout (SDIPAY, V78) -> Published` release sequence and Manager payout reconciliation turning eligible balances into recorded disbursements with bank transfer references, duplicate-payout prevention, and active refund-hold caps.
23. **`MF4` `FE-23` — Evidence-Backed Refunds & Receivable Recovery.** Refund initiation holding unpaid payouts, completion after external bank transfer with balanced multi-part financial allocations, legacy refund reconciliation, and separate Inspector receivable recovery tracking without automatically deducting future payouts.
24. **`MF4` `FE-24` — Post-Remediation Re-inspection & Defect Verification.** Follow-up re-inspection creation linked to a published report, three-way defect verification (`Resolved`, `Unresolved`, `Inconclusive`), `Resolved` verdict expiry tracking with early warning banners, and Customer Mobile parity.

### 6.2 Limitations & Exclusions

- **`LI-1` — No aircraft control.** The platform does not pilot, steer, or command any aircraft. It records the governance around a flight — who is assigned, whose licence is valid, which permit the Inspector self-attested — and leaves the flight itself to the licensed human pilot.
- **`LI-2` — Buildings only.** The supported categories are high-rise office and curtain-wall towers, residential apartment towers, commercial malls and podiums, industrial factories and warehouses, hotel, hospital and public complexes, and telecom rooftop masts with antenna structures. Bridges, transmission towers, solar farms, roads, dams, tunnels, ports, and pipelines are outside the delivered scope, and the defect classes and inspection checkpoints shipped with this release are building-specific.
- **`LI-3` — No corrective maintenance module.** Work orders, repair-scope advisory, repair execution, completion reporting, maintenance acceptance, and cost reconciliation are outside the delivered scope. What the platform does provide is a re-inspection loop opened against a published report, in which each originally confirmed defect is re-assessed as resolved, unresolved, or inconclusive. That loop reuses the request, dispatch, field, and reporting flows rather than adding a maintenance flow.
- **`LI-4` — Detection is advisory.** Candidate findings and the drafted narrative summary are advisory output. A human must confirm every finding, verify every permit, and publish every report. No automated output becomes an official decision.
- **`LI-5` — No photogrammetric reconstruction.** Evidence is reviewed as individual photographs and video. Three-dimensional modelling, volumetric measurement, and change detection across flights are not provided.
- **`LI-6` — Advisory use of DroneKnowledgeAI.** The system suggests relevant inspection standards and similar defect cases during findings review and in the report summary. Retrieval is scoped to each Customer, with anonymized benchmarks available as references. The Inspector decides which findings to confirm.
- **`LI-7` — Mobile is Customer-only.** The native mobile application admits `CUSTOMER` accounts only. Field capture, permit handling, and report preparation are performed by inspectors in the operations web portal.
- **`LI-8` — Recorded status is not legal clearance.** An airspace screening result, a self-attested permit, and a published report are the platform's own governance records. They are not government flight authorisation, and they do not transfer any aviation or structural obligation away from the licensed pilot or the responsible engineer.

