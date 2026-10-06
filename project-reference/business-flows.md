---
title: "SmartDroneInspection Multi-Provider Business Flows"
document_type: business-flow-reference
purpose: "Authoritative specification of the Supporting Flow (SF) and the five core Main Flows (MF1–MF5) for the multi-provider drone inspection & maintenance platform, including exception branches and non-linear feedback loops."
version: "3.3"
updated: 2026-10-06
---

# SmartDroneInspection Multi-Provider Business Flows (v3.3)

> This document is the authoritative specification of the Supporting Flow (SF) and the **five core transactional Main Flows (MF1–MF5)** of the SmartDroneInspection platform. The design is built on an **intermediary marketplace (Intermediary Platform)** model with deep **Drone Mission Planning & Telemetry** capabilities, electronic contracts under Vietnamese law, **direct bank-transfer settlement (no platform custody of funds)**, **dynamic `PLATFORM_OPERATOR` configuration**, internal complaint mediation, non-linear feedback loops, field incident handling, and the Capstone error-prevention guide (`error-prevention.md`).
>
> **v3.3 change from v3.2:** advance funding / partner escrow has been removed entirely. The platform is **never a custodian or intermediary of money**. The client pays the provider directly by bank transfer after acceptance; the platform only computes and invoices its commission.

---

## I. Vietnamese Legal Basis

> **Legal scope:** This is a target design for an academic project. The instruments below are the reference framework for drone surveys, electronic contracts, non-cash payment, and building maintenance in Vietnam. The platform has not been licensed, has not integrated any bank, and does not claim compliance certification.

1. **Law on Civil Air Defence 2024 (Law 49/2024/QH15, effective 01/07/2025) & Decree 288/2025/NĐ-CP (effective 05/11/2025) on the management of unmanned aircraft:**
   - Mandatory framework for checking: UAV registration/identification records; operator conditions (age, license class A/B per weight and flight mode); and flight permits/approvals when the flight falls into a permit-required case under current regulations. Authority names, permit types, and procedures are **not hard-coded** in the workflow until confirmed for each flight class; the system checks dossier completeness and validity only and **never issues flight permits on behalf of the state**.
   - *Note:* a draft amendment to Decree 288/2025 has been reported in 2026 — unverified at the time of writing; confirm with legal counsel before submission.
2. **Prime Minister Decision 18/2020/QĐ-TTg & the National No-Fly Portal (`cambay.mod.gov.vn`, publicly republished by the Ministry of National Defence from 15/06/2025):**
   - Digital airspace lookup for prohibited/restricted areas. It is a **pre-flight early warning layer** only; it is never a permit.
3. **Non-cash payment — Decree 52/2024/NĐ-CP (effective 01/07/2024):**
   - All settlement is ordinary **bank transfer from CLIENT directly to PROVIDER_MANAGER's bank account**. The platform is **not** a payment intermediary, not a deposit-taker, and not a credit organisation; it never holds, pools, or temporarily owns customer money. No escrow account, no advance funding, no platform-side hold exists anywhere in this design (Civil Code 2015 Article 330 ký quỹ is deliberately **not** relied upon).
4. **Law on Electronic Transactions 2023 (Law 20/2023/QH15, effective 01/07/2024):**
   - Legal basis for the bilateral electronic service contract (Inspection Service Order / Maintenance Work Order), electronic signatures, and data messages. Technical evidence storage (MinIO, SHA-256 checksums, 3D GPS coordinates, timestamps) guarantees data integrity and traceability, not automatic legal admissibility.
5. **Invoices and taxation — Law on VAT 48/2024/QH15 (effective 01/07/2025), Decree 123/2020/NĐ-CP as amended by Decree 70/2025/NĐ-CP (effective 01/06/2025), Circular 78/2021/TT-BTC:**
   - Clear division of invoice duties: `PROVIDER_MANAGER` (service supplier) issues its VAT service invoice to `CLIENT` for the inspection/maintenance fee; the **Platform** issues its own electronic invoice for the platform commission plus VAT on commission to `PROVIDER_MANAGER`. Commission is a provider-side expense, never a surcharge to the client.
6. **Law on E-Commerce 2025 (Law 122/2025/QH15, effective 01/07/2026) + Decree 248/2026/NĐ-CP; Law on Consumer Protection 2023 (Law 19/2023/QH15) + Decree 55/2024/NĐ-CP:**
   - Public platform terms, transparent provider capability information, an internal complaint mechanism with audit logs. Internal outcomes **never replace** the parties' right to sue in court or commercial arbitration (VIAC).
7. **Law on Personal Data Protection 91/2025/QH15 (effective 01/01/2026) + Decree 356/2025/NĐ-CP:**
   - Consent and purpose limitation for personal data (contact persons, GPS/capture metadata, field imagery). Secrets, raw tokens, and credentials are never stored.

---

## II. Roles & Actor Zones (6 Canonical Roles)

The system is organised into **three independent actor zones**, enforcing separation of duties:

```
┌────────────────────────────────────────────────────────────────────────┐
│               ZONE 1: PLATFORM GOVERNANCE (Platform owner)            │
│                                                                        │
│   🛠️ PLATFORM_ADMIN                  👔 PLATFORM_OPERATOR              │
│   (Technical & infrastructure admin)  (Business operations, policies,  │
│   • System config, checklists          & internal complaint mediation) │
│   • Permissions, security            • Vets Provider legal capability  │
│   • AI YOLO thresholds, MinIO caps   • Sets marketplace parameters     │
│   • Audit logs, data integrity       • Tracks payment progress         │
│                                      • Issues commission/VAT invoices  │
│                                      • Independent technical arbiter   │
└───────────────────┬──────────────────────────────────┬─────────────────┘
                    │                                  │
                    ▼                                  ▼
      ┌───────────────────────────┐      ┌───────────────────────────┐
      │ ZONE 2: CUSTOMER          │      │ ZONE 3: SERVICE PROVIDER  │
      │ 🏢 CLIENT (Asset owner)   │      │ 🏢 PROVIDER_MANAGER       │
      │                           │      │ 🚁 INSPECTOR (Pilot)      │
      │                           │      │ 🔧 MAINTENANCE_ENGINEER   │
      └───────────────────────────┘      └───────────────────────────┘
```

| Zone | Role | Canonical responsibility |
| :--- | :--- | :--- |
| **1. Platform Governance** | `PLATFORM_ADMIN` | Technical administration: user accounts, permissions, security, technical parameters (AI YOLO thresholds, MinIO storage), audit logs, data integrity. No commercial policy, no dispute decisions. |
| | `PLATFORM_OPERATOR` | Business operations: vets Provider legal capability (business licence, insurance, UAV registration, pilot certificates); configures marketplace parameters (acceptance review SLA, commission rate); tracks payment progress; issues the platform's commission & commission-VAT invoices; acts as **independent technical arbiter** for internal complaints (mediation only, never a legal tribunal). |
| **2. Customer** | `CLIENT` | Infrastructure owner: creates inspection requests, approves quotations, signs electronic contracts, **transfers payment directly to the provider** after acceptance, reviews & accepts reports, files complaints, creates maintenance tickets. |
| **3. Service Provider** | `PROVIDER_MANAGER` | The provider company's single representative: receives RFQs, submits quotations, prepares mission plans and attaches flight permits, assigns staff, approves report release, **confirms receipt of client payment**, pays platform commission & tax. |
| | `INSPECTOR` | Certified drone pilot / field technician: builds the structural shot list, performs live safety reconnaissance, flies the mission, checks image quality, verifies AI findings, finalises and signs the report draft as author. |
| | `MAINTENANCE_ENGINEER` | Repair technician: surveys defects on site, prepares technical method statements and material estimates, executes repairs, captures mandatory before/after evidence pairs for acceptance. |

---

## III. Contract Model & Direct-Transfer Settlement

### 1. Electronic contract (Platform Terms + Bilateral Service Order)

* **Platform Terms of Service**: binds CLIENT and PROVIDER when joining. Empowers `PLATFORM_OPERATOR` to publish commercial policies and mediate internal complaints; grants no adjudicatory power.
* **Service Order / Maintenance Order**: an electronic contract between CLIENT and PROVIDER for one engagement under the Law on Electronic Transactions 2023. Contains: scope of work (SOW), technical mission parameters (target GSD, shot list, overlap), committed schedule (SLA), provider price, review period, commission rate, cancellation policy, and warranty terms — all **snapshotted immutably at signing**.

### 2. Direct-Transfer Settlement Lifecycle (no platform custody)

The platform orchestrates **state and documents only**; money never touches the platform:

1. **Contract effective on signature (MF1-06).** Both parties sign electronically; the contract is legally effective immediately. There is **no advance funding** before execution.
2. **Payment Invoice (MF4-05.1 / MF5-07.1).** After acceptance, the SYSTEM generates an electronic Payment Invoice showing the contract amount and PROVIDER_MANAGER's bank account details.
3. **Direct transfer (MF4-05.2).** CLIENT transfers **100% of the fee directly to PROVIDER_MANAGER's bank account** by bank transfer.
4. **Receipt confirmation (MF4-05.3).** PROVIDER_MANAGER verifies the bank credit and clicks **"Confirm receipt"** → the system sets the order to **`PAID`**. The provider then sends its VAT service invoice to the client per tax law.
5. **Commission settlement (MF4-05.4).** The system computes the platform commission $C = r \times B$ (rate $r$ snapshotted from the order; $B$ = VAT-exclusive service value) plus VAT on the commission. `PLATFORM_OPERATOR` issues the platform's service invoice to PROVIDER_MANAGER, who pays the commission to the platform separately. The commission is never added to the client's bill.
6. **Complaint pause (MF4-03).** While an internal complaint is open, acceptance and payment confirmation are paused in the platform's state machine. No funds are frozen by the platform because it holds none; any remedy (free reshoot, refund between the parties) follows the contract terms and the parties' own transfers.

### 3. Dynamic `PLATFORM_OPERATOR` configuration & Contract Snapshot

No marketplace parameter is hard-coded. `PLATFORM_OPERATOR` publishes versioned policies:

| Parameter | Symbol | Authority | Scope & effect |
| :--- | :---: | :---: | :--- |
| **Platform commission rate** | $r$ (`commission_rate`) | `PLATFORM_OPERATOR` | Applied to providers; computed on the VAT-exclusive service value: $C = r \times B$. |
| **Acceptance review period** | $T_{rev}$ (`review_period_days`) | `PLATFORM_OPERATOR` | Client's review window; snapshotted per order (example value: 7 working days). Basis for contractual auto-acceptance (MF4-04b). |
| **Standard warranty duration** | $T_{war}$ (`warranty_days`) | `PLATFORM_OPERATOR` | Warranty clock after maintenance acceptance; snapshotted per maintenance order. |
| **Cancellation policy** | `cancellation_policy` | `PLATFORM_OPERATOR` | Refundable/chargeable conditions by timing and reason; snapshotted per order. |

* **Contract Snapshot pattern:** at signing, every parameter value is copied into the order row. Later policy changes apply **prospectively only** and never rewrite active contracts.
* **Removed in v3.3:** advance funding rate $D$, warranty retention $H$, and any partner-escrow state (`FUNDED_IN_PARTNER_ESCROW`, `FROZEN_DISPUTED`) no longer exist.

### 4. Platform-provided data, AI YOLO and LLM infrastructure

* MinIO object storage, the **YOLO** vision pipeline and the **LLM** drafting assistant are shared platform infrastructure, funded from the platform's commission $C$.
* **Providers must not itemise AI or storage fees** in quotations — quotes cover flight crew, technical labour, logistics, and the provider's VAT only.
* **Human-in-the-loop:** AI only proposes defect candidates and draft text. Official inspection results must always be verified, measured, edited, and signed by `INSPECTOR` (author) and released by `PROVIDER_MANAGER`.

---

## IV. End-to-End Dynamic Workflow (non-linear loops)

The platform runs a full lifecycle with feedback and exception handling:

```
                      ┌──────────────────────────────────────────┐
                      │    SF: ASSET & PROVIDER ONBOARDING       │
                      └────────────────────┬─────────────────────┘
                                           │
                                           ▼
                      ┌──────────────────────────────────────────┐
                      │    MF1: RFQ & E-CONTRACT (no funding)    │
                      └────────────────────┬─────────────────────┘
                                           │
                                           ▼
                      ┌──────────────────────────────────────────┐
                      │    MF2: FLIGHT PLANNING & CLEARANCE      │
                      └─────────┬──────────────────────┬─────────┘
                                │                      │
                        [Permit/Plan OK]        [Weather/Safety Abort]
                                │                      │
                                ▼                      ▼
                      ┌───────────────────┐    [Reschedule / Re-plan]
                      │ MF3: FIELD FLIGHT │
                      └─────────┬─────────┘
                                │
                                ▼
                      ┌──────────────────────────────────────────┐
                      │     EVIDENCE QUALITY & COVERAGE GATE     │
                      └─────────┬──────────────────────┬─────────┘
                                │                      │
                          [Data Valid]          [Blur / Missing / No GPS]
                                │                      │
                                │                      ▼
                                │              [Re-flight / Same-day fix]
                                │                      │
                                ├──────────────────────┘
                                ▼
                      ┌──────────────────────────────────────────┐
                      │ AI ESTIMATION & INSPECTOR VERIFICATION   │
                      └────────────────────┬─────────────────────┘
                                           │
                                           ▼
                      ┌──────────────────────────────────────────┐
                      │     LLM DRAFT & QA REPORT RELEASE        │
                      └────────────────────┬─────────────────────┘
                                           │
                                           ▼
                      ┌──────────────────────────────────────────┐
                      │         MF4: CLIENT ACCEPTANCE           │
                      └─────────┬──────────────┬───────────────┬─┘
                                │              │               │
                            [Accept]      [Clarify]        [Dispute]
                                │              │               │
                                ▼              ▼               ▼
                     [Payment Invoice &  [Revise Report] [Internal arbitration
                      DIRECT TRANSFER]                     & expert review]
                                │              │               │
                                │              └───────────────┘
                                ▼
                      ┌──────────────────────────────────────────┐
                      │     MF5: MAINTENANCE WORK ORDER          │
                      └────────────────────┬─────────────────────┘
                                           │
                                           ▼
                      ┌──────────────────────────────────────────┐
                      │    TECHNICAL ASSESSMENT & QUOTATION      │
                      └────────────────────┬─────────────────────┘
                                           │
                                           ▼
                      ┌──────────────────────────────────────────┐
                      │       REPAIR & BEFORE/AFTER EVIDENCE     │
                      └─────────┬──────────────────────┬─────────┘
                                │                      │
                          [Work Complete]        [Hidden Defect Found]
                                │                      │
                                │                      ▼
                                │             [Change Order Approval]
                                │                      │
                                ├──────────────────────┘
                                ▼
                      ┌──────────────────────────────────────────┐
                      │        MAINTENANCE ACCEPTANCE            │
                      └─────────┬──────────────────────┬─────────┘
                                │                      │
                            [Passed]                [Failed]
                                │                      │
                                ▼                      ▼
                     [Payment & Warranty Clock] [Rework Loop]
                                │
                                ▼
                     [Warranty expiry → Auto-close Ticket]
```

---

## V. Detailed Flows (Supporting Flow & 5 Core Main Flows)

---

### Supporting Flow (SF) — Master Data, Provider Vetting & Airspace Pre-check

> **Nature:** the prerequisite data-governance flow (onboarding) that establishes a safe, lawful operating environment for all transactions.

**Main actors**: `PLATFORM_ADMIN`, `PLATFORM_OPERATOR`, `CLIENT`, `PROVIDER_MANAGER`, `System`.

#### 1. Sequence steps

* **SF-01 (Client self-registration)**: the customer company registers an organisation account, provides its tax code and legal representative, and activates the `CLIENT` account.
* **SF-02 (Provider onboarding & vetting submission)**: PROVIDER_MANAGER registers the company dossier: business licence; UAV fleet with registration certificates issued under Law 49/2024 & Decree 288/2025; pilot roster with valid operator licences; valid third-party liability insurance certificates.
* **SF-03 (Operator vetting approval)**: `PLATFORM_OPERATOR` reviews the legal validity of the dossier. If compliant → `VERIFIED`; if incomplete/expired → `ADDITIONAL_INFO_REQUIRED` or `REJECTED`. Unvetted providers are blocked from all quotation activity. Inspection and maintenance capabilities are vetted **independently** (approving one never approves the other).
* **SF-04 (Asset profiling & airspace pre-check)**: the client records asset coordinates, access boundaries, structure height, and as-built drawings. The system queries national no-fly data (`cambay.mod.gov.vn` per Decision 18/2020/QĐ-TTg) and shows a reference warning when the asset sits inside or adjacent to a restricted zone.
* **SF-05 (Periodic schedule cadence)**: the platform generates schedule proposals from configured maintenance cycles; the client confirms an official schedule which then drives automatic request generation when due.

#### 2. SF exception handling

* **Forged or expired provider dossier**: Operator rejects, blocks marketplace participation, writes an audit log.
* **Asset inside an absolutely prohibited zone (military, critical areas)**: system raises `NO_FLY_ZONE_ALERT` and advises the client to prepare a special flight-permit application before publishing the RFQ.

---

### MF1 — Inspection Request, Smart RFQ & Electronic Contract

**Goal**: receive the inspection need, connect to capable providers, lock the quotation, and sign an electronic contract with clear schedule and payment milestones.

**Main actors**: `CLIENT`, `PLATFORM_OPERATOR`, `PROVIDER_MANAGER`, `System`.

#### 1. Main sequence

| Step | Role / Lane | Activity | Output |
| :--- | :--- | :--- | :--- |
| **MF1-01** | CLIENT | Create the inspection request: state objectives (concrete crack detection, steel corrosion), site location and desired deadline. Choose **(A) direct appointment** of a known partner or **(B) open RFQ**. | Inspection request (RFQ) |
| **MF1-02** | System | **Smart eligibility filter**: automatically shortlist providers by (1) operating region; (2) drone/sensor fit for the objective; (3) valid pilot licences; (4) `VERIFIED` dossier status; (5) calendar availability — and send RFQ invitations only to those. | Eligible provider list |
| **MF1-03** | PROVIDER_MANAGER | Remote reconnaissance from maps/drawings, then submit the **Quotation**: (1) flight crew cost; (2) technical labour; (3) mobilisation/logistics; (4) provider VAT. **Platform AI/MinIO costs are never itemised.** | Service quotation |
| **MF1-04** | CLIENT | Compare competing quotations; request revisions if needed, then approve the best offer. | Approved quotation |
| **MF1-05** | System | Generate the **electronic Service Order**: run the **contract snapshot** — commission rate $r$, review period $T_{rev}$, cancellation policy, warranty terms as applicable — all fixed at signing. | Contract ready to sign |
| **MF1-06** | CLIENT & PROVIDER_MANAGER | Both parties sign electronically. **The contract takes effect immediately. Payment will be made by direct bank transfer after acceptance** — there is no advance funding step. Mission planning begins. | Contract in force |

#### 2. MF1 exceptions & weather risk

* **No provider bids before RFQ close**: system suggests widening the geography or adjusting budget/schedule.
* **Force majeure weather (storm, wind beyond safe limits)**: both parties record a postponement minutes in the system; rescheduling carries no cancellation penalty and no SLA breach.
* **Client cancels before mobilisation**: apply the cancellation snapshot — deduct reasonable, evidenced preparation costs for the provider; the remainder is simply never transferred (no platform refund machinery, because the platform never held funds).

---

### MF2 — Mission Planning & Flight Compliance 🚀 [DRONE-CENTRED FLOW]

> **Technical focus**: separate photogrammetric capability from flight-safety authority; enforce the flight dossier under current law. The system checks records; it never grants permission.

**Main actors**: `INSPECTOR` (Pilot-in-Command), `PROVIDER_MANAGER`, `System`.

#### 1. Main sequence

| Step | Role / Lane | Activity | Output |
| :--- | :--- | :--- | :--- |
| **MF2-01** | INSPECTOR | **Photogrammetric calculation & recommended capture distance**: from the minimum crack width to detect (e.g. cracks ≥ 1.0 mm need GSD ≤ 0.5 mm/px), the pilot enters camera/sensor parameters (focal length, sensor size, resolution); the system recommends **capture distance and camera settings** — data-quality guidance only, never a safety-altitude determination. | Recommended GSD & capture distance |
| **MF2-02** | INSPECTOR | **Image overlap configuration**: forward overlap ≥ 75%, side overlap ≥ 60%, adapted to surface geometry so no blind spots remain and 3D defect modelling is possible. | Survey-grade overlap settings |
| **MF2-03** | INSPECTOR | **Structural shot list & gimbal pitch**: enumerate components to photograph, camera angles (0°, −45°, −90°). Define waypoints if flying a programmed route, otherwise a detailed manual shot list. Live field reconnaissance of obstacles (trees, power lines, wind) is performed on site. | Complete shot list (+ waypoints if used) |
| **MF2-04** | System | **Airspace check & regulatory alert**: intersect flight coordinates with the configured no-fly/restricted dataset (`cambay.mod.gov.vn` reference). Result is a **planning warning only** — not a permit and not a substitute for authority confirmation. | Reference airspace report |
| **MF2-05** | PROVIDER_MANAGER | **Flight-legal dossier**: attach the flight permit/approval issued by the competent military authority when the flight is permit-required under current regulations; verify UAV registration identity and pilot licence conditions. The provider owns the legality of the flight; the system only checks completeness and validity of provided records. | Complete flight-legal dossier |
| **MF2-06** | INSPECTOR & PROVIDER_MANAGER | **Pilot-in-command safety sign-off**: the pilot inspects live obstacles, structure clearance and weather, and **signs the flight-safety commitment**; PROVIDER_MANAGER approves and releases the mission. The order transitions to **`READY_FOR_FLIGHT`**. | Approved mission plan (`READY_FOR_FLIGHT`) |

#### 2. MF2 exceptions

* **Cannot obtain the flight permit**: the plan is rejected; PROVIDER_MANAGER notifies the CLIENT to extend the permit timeline or cancel under the legal force-majeure clause.
* **Camera cannot meet the required GSD**: approval is blocked; the pilot must change lens/sensor or (when safely possible) reduce capture distance.

---

### MF3 — Field Survey, Evidence Quality Gate, AI Analysis & QA Release

**Goal**: fly safely, enforce image quality on site, verify AI-assisted defect candidates with a human in the loop, compile the LLM draft, and release the official QA report.

**Main actors**: `INSPECTOR` (field pilot & report author), `PROVIDER_MANAGER`, Platform MinIO, Platform AI services, `System`.

#### 1. Main sequence

| Step | Role / Lane | Activity | Output |
| :--- | :--- | :--- | :--- |
| **MF3-01** | INSPECTOR | Open the mobile/web app on site, start the survey session (`IN_PROGRESS`), run the pre-flight check, and manually fly the approved shot list. (Severe weather → abort safely, log the reason, schedule a make-up flight.) | Logged field session |
| **MF3-02** | INSPECTOR | Upload all high-resolution photos/videos to platform MinIO via chunked upload. | Raw field imagery |
| **MF3-03** | System | **Telemetry extraction & integrity**: parse GPS 3D coordinates, relative AGL altitude, gimbal angle, timestamp; compute a **SHA-256** checksum per file to protect evidence integrity. | Integrity-protected evidence |
| **MF3-04** | System & INSPECTOR | **Evidence quality & coverage gate**: automatic checks for blur, GPS validity, and shot-list coverage. Blurry/underexposed/missing-angle images raise an alert so the pilot performs a **same-day re-flight** before leaving site. | Quality-passed evidence set |
| **MF3-05** | System (YOLO) | Platform YOLO pipeline scans valid images, detects defects (concrete cracks, rebar corrosion, spalling) and **estimates physical dimensions (mm)** from the defect region, GSD, and image geometry. Estimates support the expert; they are not final measurements until verified. Output: **defect candidates** with bounding boxes. | Candidate defects with GSD estimates |
| **MF3-06** | INSPECTOR (human-in-the-loop) | Review every image and candidate: **Confirm, Modify, or Reject**; add **manual findings** for anything the AI missed, using survey-grade measurement for exact dimensions. Complete the inspection checklist. | Professionally verified defect list |
| **MF3-07** | System (LLM) | The assistant compiles structured checklist/telemetry/evidence/verified-defect data into a **technical report draft**, marking AI-assisted content and model version. | Report draft |
| **MF3-08** | INSPECTOR (author) | **Self-verify, edit, take professional responsibility**: review each conclusion against the imagery, fix terminology and omissions, then electronically sign the finished draft before submitting to PROVIDER_MANAGER. Mandatory — an AI draft is never published directly. | Author-verified report |
| **MF3-09** | PROVIDER_MANAGER | Check administrative completeness and SOW conformity; if complete, **sign and release the official QA report** to the client. The system starts the acceptance countdown $T_{rev}$ snapshotted in the contract. | Released report & $T_{rev}$ started |

#### 2. MF3 field exceptions

* **In-flight incident (signal loss, battery drop, motor failure)**: pilot executes fail-safe return-to-home / emergency landing, files an **incident log** (cause, equipment state, site condition), notifies PROVIDER_MANAGER and CLIENT, reschedules after safety checks.
* **Sudden weather deterioration**: immediate abort; captured data preserved; make-up flight scheduled for the remainder.
* **YOLO/LLM service outage**: automatic **manual fallback** — the inspector boxes defects and drafts on the standard template so the delivery schedule holds.

---

### MF4 — Report Acceptance, Direct Settlement & Internal Complaint Handling

**Goal**: the client reviews the report, signs acceptance (or the contract auto-accepts), pays the provider **directly by bank transfer**, and the platform settles its commission through its own invoice; complaints are mediated internally with the platform as independent technical arbiter.

**Main actors**: `CLIENT`, `PROVIDER_MANAGER`, `PLATFORM_OPERATOR`, `System`.

#### 1. Main sequence

| Step | Role / Lane | Activity & money-flow transparency | Output |
| :--- | :--- | :--- | :--- |
| **MF4-01** | CLIENT | Review the official report on web/mobile (high-res defect photos, 3D positions, crack measurements, risk grades). The contractual review window $T_{rev}$ counts down. | Report under review |
| **MF4-02** | CLIENT & PROVIDER_MANAGER | **Clarification loop (if anything is unclear)**: the client raises a clarification request; PROVIDER_MANAGER/INSPECTOR respond with a supplementary or corrected report. Clients never edit professional conclusions directly. | Clarified / revised report |
| **MF4-03** | CLIENT, PROVIDER_MANAGER & PLATFORM_OPERATOR | **Complaint branch (material defect in the deliverable)**: either party clicks **"Open complaint"** → the system **pauses acceptance and payment confirmation**. `PLATFORM_OPERATOR` works with both sides (collects the client's account, requires the provider's response) and compares raw imagery and flight data on the platform to reach an objective finding — free re-flight, or rejection of the complaint. The platform acts as **independent technical arbiter**; its outcome is internal, never a court or VIAC ruling. | Unified complaint conclusion |
| **MF4-04a** | CLIENT | **Manual acceptance**: satisfied (or after clarification) → click **"Accept & sign minutes"**. | Acceptance minutes signed by both parties |
| **MF4-04b** | System | **Contractual auto-acceptance**: when the review period (example: 7 days) expires with no response and no open complaint → the system records acceptance per the contract terms snapshotted in MF1-05. | Auto-acceptance minutes |
| **MF4-05** | SYSTEM, CLIENT, PROVIDER_MANAGER & PLATFORM_OPERATOR | **Settlement & commission invoicing (direct transfer):** **(1)** SYSTEM generates the electronic Payment Invoice with the contract amount and PROVIDER_MANAGER's bank account. **(2)** CLIENT transfers **100% of the inspection fee directly to PROVIDER_MANAGER's bank account**. **(3)** PROVIDER_MANAGER verifies the credit and clicks **"Confirm receipt"** → status **`PAID`**; the provider sends its VAT service invoice to the client per tax law. **(4)** the system computes platform commission + commission VAT; `PLATFORM_OPERATOR` issues the platform's service invoice to PROVIDER_MANAGER, who pays the commission to the platform separately. | `PAID` status & platform commission invoice (with VAT) |

#### 2. MF4 exceptions

* **A party rejects the internal mediation outcome**: the platform's outcome is an internal mechanism under the Platform Terms only. Both parties retain the right to sue in the competent court or to commercial arbitration (VIAC).

---

### MF5 — Defect Rectification, Maintenance Orders & Warranty Closure

**Goal**: turn verified defects from the MF4 report into repair orders, control cost changes via change orders, verify before/after evidence, settle **directly**, and track the warranty to automatic closure.

**Main actors**: `CLIENT`, `PROVIDER_MANAGER` (maintenance-capable provider), `MAINTENANCE_ENGINEER`, `PLATFORM_OPERATOR`, `System`.

#### 1. Main sequence

| Step | Role / Lane | Activity & money-flow transparency | Output |
| :--- | :--- | :--- | :--- |
| **MF5-01** | CLIENT | Create a **maintenance ticket** by selecting dangerous defects directly from the MF4 report, and choose one of three dispatch modes: **(a) priority to the inspection provider** (the same company that flew the survey, if it holds verified maintenance capability); **(b) direct appointment** of a known maintenance partner; **(c) open RFQ** to capable maintenance providers. | Maintenance ticket (+ defect dossier from MF4) |
| **MF5-02** | PROVIDER_MANAGER | **Technical method statement & quotation**: from the drone defect dossier (sharp imagery, 3D positions, mm measurements) plus on-site survey, define the repair method (epoxy injection, polymer mortar, corrosion treatment), full cost estimate, and **warranty commitment (e.g. 6 or 12 months)**. | Technical plan & lump-sum quotation |
| **MF5-03** | CLIENT & PROVIDER_MANAGER | **Sign the electronic repair contract**: fix the lump-sum price, completion schedule, acceptance criteria, and the free-warranty clause. Contract effective on signature; payment later by direct transfer. | Repair contract in force |
| **MF5-04** | MAINTENANCE_ENGINEER | Execute the repair on site. **Mandatory capture of before/after evidence pairs at the same camera angle**, uploaded with the materials log. | Before/after evidence pair |
| **MF5-05** | MAINTENANCE_ENGINEER & PROVIDER_MANAGER | **Change-order flow**: hidden damage beyond the estimate → stop the affected work, photograph, and submit a **change order** for client approval of the additional cost before continuing. | Approved change order |
| **MF5-06** | CLIENT & PROVIDER_MANAGER | **Completion acceptance**: client compares the before/after pair on the app. Not achieved → **rework loop** (provider fixes free of charge within committed scope); achieved → both parties sign the completion acceptance minutes. | Signed completion minutes |
| **MF5-07** | SYSTEM, CLIENT, PROVIDER_MANAGER & PLATFORM_OPERATOR | **Settlement & commission (direct transfer):** **(1)** SYSTEM generates the electronic Payment Invoice for the accepted works value with PROVIDER_MANAGER's bank details. **(2)** CLIENT transfers **100% directly to PROVIDER_MANAGER's bank account**. **(3)** PROVIDER_MANAGER confirms receipt → status **`PAID`**. **(4)** the platform issues its commission + commission-VAT invoice to PROVIDER_MANAGER for separate payment. | `PAID` status & platform commission invoice |
| **MF5-08** | CLIENT & PROVIDER_MANAGER | **Warranty activation & ticket closure**: the system starts the warranty countdown snapshotted in the order. Defect recurrence within warranty → the client opens a warranty claim and the provider **must send an engineer to fix it free of charge** per contract. Warranty expires with a stable structure → the system **auto-closes the ticket**, completing 100% of the lifecycle. | Closed maintenance ticket (100% lifecycle) |

#### 2. Maintenance branches: rework / re-inspection

* **Before/After acceptance failure (rework loop)**: if the after-photo shows voids, wrong material colour, or an untreated crack → the client rejects acceptance with images. Provider-fault rework within committed scope is free; out-of-scope causes require a change request first.
* **Post-repair drone re-inspection**: for high or hazardous structures the client may open a new inspection request (or the contractual re-inspection mechanism) to photograph the repair quality from the air.

---

## VI. RACI Matrix (v3.3)

| Process / core business | `PLATFORM_ADMIN` | `PLATFORM_OPERATOR` | `CLIENT` | `PROVIDER_MANAGER` | `INSPECTOR` | `MAINTENANCE_ENGINEER` |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **SF: Provider vetting & UAV registration (Decree 288)** | I | **A / R** | I | **R** | C | - |
| **SF: Asset profiling & no-fly alerts** | I | C | **A / R** | - | - | - |
| **Policy: dynamic marketplace parameters** | I | **A / R** | I | I | - | - |
| **MF1: Smart eligibility filter & RFQ** | - | C | **A** | **R** | - | - |
| **MF1: E-contract signing (no funding step)** | I | C | **A / R** | **R** | - | - |
| **MF2: Mission planning (GSD, overlap, shot list)** | - | - | I | **A** | **R** | - |
| **MF2: Flight-legal dossier & safety sign-off** | I | C | I | **A / R** | **R (Pilot)** | - |
| **MF3: Field survey, incident handling & re-flight** | - | - | I | I | **A / R** | - |
| **MF3: YOLO detection & measurement verification** | - | - | - | I | **A / R** | - |
| **MF3: LLM draft self-review & QA release signature** | - | - | I | **A (Release)** | **R (Author)** | - |
| **MF4: Acceptance & payment invoice / direct transfer** | I | C | **A / R** | **R (Confirm receipt)** | - | - |
| **MF4: Complaint mediation & independent technical arbitration** | I | **A / R** | C | C | C | - |
| **MF5: Technical plan & maintenance quotation** | - | - | **A** | **R** | - | C |
| **MF5: Before/after execution & change order** | - | - | **A** | I | - | **R** |
| **MF5: Completion acceptance, warranty clock & auto-close** | I | C | **A** | I | - | I |
| **Commission & commission-VAT invoicing** | I | **A / R** | I | **R (Payer)** | - | - |

*Legend*:
* **R (Responsible)**: performs the work.
* **A (Accountable)**: final approval and ownership of the outcome.
* **C (Consulted)**: provides technical cross-check input.
* **I (Informed)**: receives the outcome.
