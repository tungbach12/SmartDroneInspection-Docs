---
title: "Report 3 - Overall Description"
document_type: report3-srs-section
weight: 15
source: "report3-software-requirement-specification.docx"
---

# II. Software Requirement Specification

## 1. Overall Description

### 1.1 Product Overview

SmartDroneInspection is a target multi-provider infrastructure inspection and maintenance platform. Its one-time organization registration, Provider vetting, asset master-data management and recurring schedule setup form a **Supporting Flow (SF)**, not a Main Flow. The five transactional Main Flows cover survey request and quotation sourcing, **Drone Mission Planning & Airspace Clearance**, drone evidence and AI-assisted verification, report acceptance and conditional settlement, and maintenance/warranty resolution. Funding, retention and time windows are contractual policies configured by `PLATFORM_OPERATOR` and snapshotted per accepted order; no global numerical default or Platform custody is presumed.

The solution includes a responsive web application for platform administration, partner vetting, customer operations, commercial bidding, and dispute resolution; a mobile application for assigned field pilots and maintenance technicians; and a backend modular monolith that owns business rules, multi-tenant authorization, transactional data, digital evidence integrity, and integration contracts.

The platform supports six canonical actors across three actor zones:
1. **Platform Governance Zone**: `PLATFORM_ADMIN` (IT/system administration, standard checklist templates, security policies, and technical audit logs) and `PLATFORM_OPERATOR` (business operations, provider vetting, commercial-policy publication, customer matching, payment-partner coordination, and internal complaint handling). `PLATFORM_OPERATOR` configures commercial policy; `PLATFORM_ADMIN` configures technical settings.
2. **Customer Organization Zone**: `CLIENT` (customer organization representative who manages registered assets, issues inspection requests/RFQs, reviews and accepts policy terms, provides the funding required by the accepted order through a suitable authorized payment partner, reviews deliverables, files complaints, and opens maintenance tickets).
3. **Service Provider Zone**: Independent commercial service provider companies represented by `PROVIDER_MANAGER` (company executive who maintains provider profile, submits quotations, secures flight permits, assigns pilots, checks report completeness and releases QA reports), `INSPECTOR` (certified drone pilot/inspector who conducts field flights, uploads media and available metadata to MinIO, verifies AI YOLO candidates, and personally verifies/edits the AI-assisted report draft they authored), and `MAINTENANCE_ENGINEER` (technician who conducts defect assessments, executes physical repairs, and captures mandatory before/after photo evidence).

In the target model, the Platform provides and pays for shared MinIO storage, data processing, YOLO defect-candidate detection and on-demand LLM narrative assistance (possibly through infrastructure vendors under Platform control). Providers and Clients only use these Platform capabilities through authorized interfaces. Providers quote their own direct flight/engineering/logistics services and do not add separate Platform AI/data/storage charges to Client quotations. `PLATFORM_OPERATOR` publishes **one uniform, non-negotiable commission rate `r` for every Provider**, plus versioned funding, review, cancellation, retention and warranty policies. Parties see and accept applicable terms before confirmation; immutable order snapshots preserve the accepted values/policy versions, and future changes apply prospectively. `PLATFORM_ADMIN` manages technical parameters such as AI service configuration separately. Platform operating costs are funded from its own revenue, including that commission. No percentage or duration is selected as a global default.

The product does not pilot drones autonomously or replace civil aviation airspace control. Mission planning records applicable aircraft/pilot credential and authority permit checks under *Luật Phòng không nhân dân 2024* (Luật số 49/2024/QH15, as amended) and relevant implementing decrees, including *Nghị định 288/2025/NĐ-CP*; applicability must be verified for each mission. Published restricted-airspace information at `cambay.mod.gov.vn` per *Quyết định 18/2020/QĐ-TTg* supports pre-checks but does not grant flight clearance. MinIO checksums and timestamps support integrity and traceability under *Luật Giao dịch điện tử 2023* (Luật số 20/2023/QH15), not automatic conclusive legal proof. Platform complaint handling follows applicable consumer/e-commerce requirements when the transaction qualifies; internal resolution does not replace lawful court or commercial arbitration rights. Any conditional funding or hold requires an authorized bank/payment partner product and accepted terms; the Platform does not itself custody deposits, and no universal funding rate is assumed.

The five canonical transactional Main Flows are:

- **SF — Supporting Setup**: Client/provider organization registration and vetting, asset master data and periodic schedule setup; prerequisite work outside MF1–MF5.
- **MF1 — Survey Request, Quotation Sourcing & Conditional Funding**: Inspection request, direct selection or RFQ, versioned quotations, electronic service order and funding terms. Any advance funding uses an authorized partner product that can support the expressly agreed terms; no universal deposit rate or custody is assumed.
- **MF2 — Drone Mission Planning & Airspace Clearance**: Provider workforce establishes mission-specific GSD, overlap, equipment, AGL and structural shot items, with waypoint coordinates optional when the selected capture method uses them; verifies applicable airspace and permit requirements. An approved shot plan can be flown manually by the Inspector. The Platform does not pilot the drone or require automated route programming.
- **MF3 — Drone Survey, Evidence, AI Verification & QA Report**: Inspector captures evidence for the approved mission, verifies candidates, and personally checks/edits the AI-assisted draft they authored; Provider Manager checks deliverable completeness and releases the report.
- **MF4 (target)**: Client review under the order-snapshotted policy; the payment partner settles eligible amounts using the uniform Platform commission policy version captured in the order, or handles funds according to an accepted dispute/hold term. `PLATFORM_OPERATOR` handles internal complaints, not legal arbitration.
- **MF5**: Verified findings lead to separately approved maintenance; configured and order-snapshotted funding, retention and warranty terms govern before/after evidence, change control and release milestones.

![SmartDroneInspection system context](assets/context.png)

### 1.2 Business Rules

| ID | Rule Definition |
| --- | --- |
| BR-01 | Platform Governance, Customer Organization, and Service Provider identities use distinct actor zones; administrative and customer roles are mutually exclusive. |
| BR-02 | A Client can access only assets, requests, orders, reports, tickets, and financial records owned by the Client's organization. |
| BR-03 | A Provider Manager, Inspector, or Maintenance Engineer belongs to exactly one Service Provider organization and cannot access competitors' bids, orders, or flight data. |
| BR-04 | An Inspector or Maintenance Engineer can access only work assigned to that user within their owning Provider organization. |
| BR-05 | A Service Provider must hold `VERIFIED` status for the capability required by the work before submitting a quotation or receiving an assignment: inspection capability for inspection quotations and flight assignments; maintenance capability for maintenance quotations/orders and repair assignments. Verification of the other capability does not satisfy this gate. |
| BR-06 | The Supporting Flow (SF), outside MF1–MF5, handles customer/provider organization setup, provider eligibility review, asset master data and recurring schedules before transactional work begins. |
| BR-07 | Before a drone mission can be approved, mission-specific GSD, equipment, overlap, AGL and shot-item targets MUST be defined in the accepted SOW/Mission Plan. Waypoints/route coordinates are optional when the chosen capture method uses them; a manual-flight plan is valid if it meets the approved SOW and safety/permit requirements. No global numeric target is implied. |
| BR-08 | Mission planning MUST record airspace lookup/verification status against authoritative applicable sources, including public restricted-airspace information (`cambay.mod.gov.vn` per QĐ 18/2020/QĐ-TTg); a public map lookup is not a flight permit or clearance. |
| BR-09 | A recurring schedule can be activated only after the designated business reviewer approves a generated proposal and the Client selects it; a due cycle generates at most one request package. In the v1 baseline this reviewer is `SERVICE_MANAGER`; the target assigns the business review policy to `PLATFORM_OPERATOR`. |
| BR-10 | Provider quotations cover their own direct service costs and applicable Provider taxes, not separately charged Platform AI/LLM/data/storage costs. `PLATFORM_OPERATOR` publishes one uniform, non-negotiable commission rate `r` for all Providers, obtains acceptance of standard terms, and bears its own operating costs from its revenue. |
| BR-11 | `PLATFORM_OPERATOR` publishes versioned commercial policies, including one uniform commission rate, advance-funding terms, review period, cancellation policy, retention and warranty duration. Each applicable order snapshots the accepted policy versions and values; subsequent changes are prospective and cannot rewrite confirmed orders. |
| BR-12 | Quotation and order revisions create immutable sequential versions, preserving complete commercial and pricing history. |
| BR-13 | Cancellation and reimbursement are governed only by the cancellation terms explicitly disclosed and accepted in the relevant order; no global cancellation window, percentage, or fixed dry-run fee is implied. |
| BR-14 | Unfavorable weather (rain, high winds, fog) is recognized as flight safety force majeure; flight schedules may be postponed without contractual SLA penalties. |
| BR-15 | An Inspector assignment must be accepted before inspection status becomes `READY_FOR_INSPECTION`. Rejection requires a reason and returns the assignment to Provider Manager. |
| BR-16 | Manual drone piloting, flight control, and operational flight safety remain the operational responsibility of the Service Provider. |
| BR-17 | Evidence ingestion records a server-computed SHA-256 checksum and available capture/GPS metadata; these support technical integrity and traceability but do not automatically prove legal admissibility or conclusive authenticity. |
| BR-18 | Duplicate evidence checksums within the same inspection or maintenance work log are rejected. |
| BR-19 | Missing GPS is recorded but does not automatically invalidate otherwise acceptable visual evidence. |
| BR-20 | AI YOLO detections remain non-official defect candidates until verified (confirmed, modified, or rejected) by an assigned Inspector. |
| BR-21 | Rejected or unverified AI candidates are excluded from official defect statistics and customer reports. |
| BR-22 | An Inspector may manually record findings missed by the AI model; AI service unavailability triggers safe manual defect recording fallback. |
| BR-23 | The Inspector who authored the report verifies evidence support, defect classifications, checklist consistency, conclusions and AI-generated narrative, then edits/confirms the draft before submitting it to `PROVIDER_MANAGER`. |
| BR-24 | A report can be released to the Client after the author Inspector records draft verification and `PROVIDER_MANAGER` checks deliverable completeness against the accepted SOW. |
| BR-25 | Unverified AI candidates and unreleased draft report versions remain hidden from the Client; rejected AI candidates are excluded from the report. |
| BR-26 | An accepted report version is immutable; corrections require a new linked version. |
| BR-27 | A deemed-acceptance timer may run only for the review period explicitly disclosed and snapshotted in the accepted order, and only when no valid clarification or complaint is open. Settlement uses the order-locked uniform Provider-paid commission policy `C = r × B`; any configured review duration is a target policy, not an implemented or statutory default. |
| BR-28 | Client or Provider may file an order-scoped complaint on grounds such as defective imagery, missed shot items, safety concerns, or data integrity. A payment hold applies only where the authorized partner product and accepted order terms support it; `FROZEN_DISPUTED` is a workflow state, not proof that funds are held by the Platform. |
| BR-29 | `PLATFORM_OPERATOR` coordinates internal complaint handling under published Platform Terms. Internal resolution does not replace a court judgment or lawful commercial arbitration; MinIO metadata and hashes support integrity but are not automatically conclusive legal evidence. |
| BR-30 | Internal complaint remedies depend on the accepted contract, documented evidence, payment-partner product and applicable law; do not imply a fixed reshoot deadline or automatic full-refund rule. `PLATFORM_OPERATOR` does not issue a legally binding arbitration award. |
| BR-31 | A maintenance ticket must reference at least one verified defect from a Client-accepted inspection report. |
| BR-32 | A qualified Maintenance Engineer provides the technical maintenance assessment and estimate; Service Manager/Provider Manager does not fabricate technical estimates. |
| BR-33 | Maintenance retention and warranty duration are optional published policies configured by `PLATFORM_OPERATOR`; when adopted, the parties disclose/accept them and the order snapshots the version and values. If retention is not adopted, the order has no retention balance. A retained portion earns no second Platform commission on later release. |
| BR-34 | Material maintenance scope or cost growth requires an approved change order before additional work begins; supplemental funding follows the policy and payment-partner mechanism accepted for that maintenance order. |
| BR-35 | Maintenance work completion strictly requires verified before and after photo evidence uploaded to MinIO. |
| BR-36 | Proposed maintenance settlement releases eligible Provider proceeds net of the order-locked uniform Platform commission, with the order-snapshotted retention `H` held for the agreed warranty duration and released later without a second commission; Provider and Platform tax invoices remain separate. |
| BR-37 | Re-inspection requested during maintenance resolution creates a linked ad hoc inspection request returning to MF1 for sourcing and MF2 for mission planning. |
| BR-38 | Status transitions that affect assignment, approval, release, acceptance, dispute arbitration, or closure are audited. |
| BR-39 | File possession or an object-storage path alone does not grant access to evidence. |
| BR-40 | Password, role, status, and session-revocation changes invalidate affected active sessions. |
| BR-41 | `PLATFORM_OPERATOR` MUST maintain a separate vetting decision for every service capability declared by a Provider Organization. A decision to verify, request additional information for, or reject one capability applies only to that capability and MUST NOT implicitly change or verify another declared capability. |
