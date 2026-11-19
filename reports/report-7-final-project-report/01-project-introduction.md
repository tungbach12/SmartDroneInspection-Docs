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
| `CUSTOMER` | Customer Organization Manager or Owner |
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
| Trần Hoàng Trung Hiếu | Team Leader, Backend and Frontend Engineer | hieuthtse184212@fpt.edu.vn | 0963832382 |
| Phùng Trung Quốc | Backend and Mobile Engineer | quocptse170027@fpt.edu.vn | 0896986551 |
| Trần Tùng Bách | Full-Stack and AI Engineer | bachttse180220@fpt.edu.vn | 0378351050 |
| Trương Thái Như | Full-Stack Engineer | nhuttse180082@fpt.edu.vn | 0328416716 |
| Phạm Minh Trí | Supervisor | tripm14@fpt.edu.vn | — |
| Đặng Ngọc Minh Đức | External Supervisor and Lecturer | ducdnm2@fpt.edu.vn | — |

## 2. Product Background

Buildings age, and the parts that age fastest — roofs, curtain walls, facades, balconies, rooftop equipment, and structural seams — are exactly the parts that are hardest to reach and safest to ignore. A leaking roof or a hairline facade crack is cheap to repair early and expensive to repair late, yet the routine check that would catch it demands scaffolding, rope access, or a cherry picker. For most building owners that means the inspection happens later than it should, is documented in photographs and notes that nobody can compare across years, and produces a recommendation that is difficult to act on.

Vietnam's building stock has grown faster than its maintenance discipline. High-rise offices, apartment towers, commercial podiums, and industrial sheds now dominate urban skylines, and facility teams are asked to keep them in service with budgets that assume the work is periodic and the records are complete. Neither assumption holds. The result is a familiar cycle: a visible defect is discovered by a tenant rather than by an inspection, the response is reactive, the repair is larger than it needed to be, and the record of what was found and when is lost when the technician who found it moves on.

Drone photography has changed what is technically possible. A trained pilot can capture a facade at close range in minutes, and computer vision can scan those images for cracks, corrosion, leakage stains, bulging render, and detached cladding far faster than a human reviewer can. What has been missing is not the flight and not the detection, but the coordination layer between them: a place where a building owner can request an inspection, a platform can quote and schedule it, a licensed partner pilot can be dispatched with a registered drone and a verified flight permit, the resulting evidence can be turned into confirmed findings, and the whole chain can end in a report that a customer accepts and pays for.

SmartDroneInspection is that coordination layer. It does not fly the aircraft and it does not replace the licensed pilot or the reviewing engineer. It makes the sequence between them auditable.

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
- **Cons:** Mining and earthworks focus means building envelope defects such as facade cracks and leakage are not its primary detection target; no inspection-specific lifecycle from permit verification to independent report publication; not aimed at a marketplace of partner inspectors.

The gap across all three is the same. They are strong at capturing and analysing imagery and weak at governing a multi-party inspection: who applied to be a partner, whose licence is still valid on the mission date, who uploaded the permit and who verified it, who wrote the report and who was allowed to publish it, and whether the customer has accepted and settled it. SmartDroneInspection addresses that governance layer and treats detection as one advisory input to it.

## 4. Business Opportunity

The opportunity sits between two groups that need each other and currently find each other informally.

On one side are building owners and facility operators — office landlords, apartment management boards, retail and industrial park operators, hospitals, hotels, and telecom tower owners — who need periodic envelope and structural inspections but do not own drones or employ pilots. On the other side are licensed drone pilots who own serviceable equipment and want recurring, well-documented work rather than one-off jobs sourced through personal contacts.

Today that match is made over the phone. There is no standard quotation, no record of what was agreed, no verification that the pilot's licence and the drone's registration are valid on the day of the flight, no structured evidence trail, and no report format a customer can rely on or an insurer will accept.

A platform that standardises the chain — request, quotation in VND, signed agreement, dispatch, permit verification, field execution, evidence, confirmed findings, published report, accepted and settled — turns an ad-hoc arrangement into a repeatable service. That repeatability is the commercial proposition: it lets an owner budget for inspections instead of discovering them, it lets a pilot build a portfolio of documented work, and it lets the platform charge for coordination rather than for flight hours.

## 5. Software Product Vision

For building owners who need to know the true condition of their structures, and for licensed drone pilots who need dependable work, SmartDroneInspection is a coordination platform that turns a building inspection from an informal arrangement into an auditable service. Unlike aerial-mapping tools that stop at imagery and analytics, SmartDroneInspection governs the whole chain — partner admission, quotation, agreement, dispatch, permit verification, field execution, confirmed findings, independent publication, and settlement — and treats machine detection as advisory input that a human must confirm before it becomes an official finding.

## 6. Project Scope & Limitations

### 6.1 Major Features

1. **`MF1` `FE-01` — Registration, Sign-in and Account Access.** A customer organization registers itself and its first building, is screened against prohibited airspace, and signs in securely with one-time codes or Google; sessions rotate, and every portal exposes only the sections its role may use.
2. **`MF1` `FE-02` — Partner Inspector and Drone Registration.** A prospective partner inspector applies publicly with licence details, platform staff review and approve, and the inspector then registers owned drones against the required document set for platform approval.
3. **`MF2` `FE-03` — Buildings, Airspace Screening and Notifications.** A customer maintains its buildings, inspection checkpoints, and reference documents under the airspace gate; restrictive-airspace registrations are reviewed by platform staff; recurring requests generate their planned occurrences; and lifecycle notices reach the responsible users without duplication.
4. **`MF2` `FE-04` — Service Requests, VND Quotations, Agreements and Dispatch.** A manager claims the request, negotiates in an order chat, issues a VND quotation, records the signed agreement, and assigns a qualified inspector and an eligible drone to each occurrence.
5. **`MF3` `FE-05` — Flight Permit and On-site Field Sessions.** The assigned inspector uploads the mission flight permit, a different manager verifies it, and the field session can start; the session is recorded to completion or a reasoned abort, with manager follow-up.
6. **`MF3` `FE-06` — Evidence Intake and Human-Reviewed Defect Detection.** The inspector captures photographs and video, the platform proposes candidate building defects for confirmation, and the confirmed findings become the official baseline. A `DroneKnowledgeAI` chip strip (“Similar Cases & Guide”) surfaces advisory matched cases and engineering standards with one-click application into the Inspector’s technical note.
7. **`MF4` `FE-07` — Inspection Report Preparation, Review and Publication.** The platform compiles the report from the confirmed findings, drafts an executive summary, and an independent manager reviews and publishes a locked PDF version. The advisory executive summary also carries “Matched Cases & Standards” knowledge references.
8. **`MF4` `FE-08` — Customer Report Acceptance and Payment Settlement.** The customer accepts the published report and settles through PayOS VietQR or VNPay; the platform tracks partner payouts and refunds and supports a re-inspection that re-assesses each confirmed defect.

### 6.2 Limitations & Exclusions

- **`LI-1` — No aircraft control.** The platform does not pilot, steer, or command any aircraft. It records the governance around a flight — who is assigned, whose licence is valid, which permit was verified — and leaves the flight itself to the licensed human pilot.
- **`LI-2` — Buildings only.** The supported categories are high-rise office and curtain-wall towers, residential apartment towers, commercial malls and podiums, industrial factories and warehouses, hotel, hospital and public complexes, and telecom rooftop masts with antenna structures. Bridges, transmission towers, solar farms, roads, dams, tunnels, ports, and pipelines are outside the delivered scope, and the defect classes and inspection checkpoints shipped with this release are building-specific.
- **`LI-3` — No corrective maintenance module.** Work orders, repair-scope advisory, repair execution, completion reporting, maintenance acceptance, and cost reconciliation are outside the delivered scope. What the platform does provide is a re-inspection loop opened against a published report, in which each originally confirmed defect is re-assessed as resolved, unresolved, or inconclusive. That loop reuses the request, dispatch, field, and reporting flows rather than adding a maintenance flow.
- **`LI-4` — Detection is advisory.** Candidate findings and the drafted narrative summary are advisory output. A human must confirm every finding, verify every permit, and publish every report. No automated output becomes an official decision.
- **`LI-5` — No photogrammetric reconstruction.** Evidence is reviewed as individual photographs and video. Three-dimensional modelling, volumetric measurement, and change detection across flights are not provided.
- **`LI-6` — Human-in-the-Loop Retrieval Boundary (`DroneKnowledgeAI`).** `DroneKnowledgeAI` does maintain a retrieval index — seeded engineering standards (`TCVN 9343:2012`, `TCVN 9361:2012`, `EN 1504-9`, `ISO 12944-5`, `ASTM C1583`) in `inspection_knowledge_chunks` and anonymized historical finding cases in `historical_finding_cases` — backed by a `pgvector` HNSW cosine index with a deterministic `HYBRID_MATCH` fallback when embeddings are unconfigured. Similar past findings and matched standards are surfaced as advisory context inside `FE-06` and `FE-07` on the web and on the Customer mobile inspection detail, and are referenced in the AI executive summary. Every recommendation remains strictly advisory: the human Inspector confirms, edits, or rejects each proposed finding, and private customer records stay tenant-isolated, so recommendations never expose another organization's data and never replace professional judgement. Corrective-maintenance repair knowledge (`repair_knowledge_chunks`) and work-order execution remain out of scope.
- **`LI-7` — Mobile is Customer-only.** The native mobile application admits `CUSTOMER` accounts only. Field capture, permit handling, and report preparation are performed by inspectors in the operations web portal.
- **`LI-8` — Recorded status is not legal clearance.** An airspace screening result, a verified permit, and a published report are the platform's own governance records. They are not government flight authorisation, and they do not transfer any aviation or structural obligation away from the licensed pilot or the responsible engineer.

