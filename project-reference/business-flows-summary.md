---
title: "SmartDroneInspection - Business Flow Summary (MF1–MF5)"
document_type: business-flow-summary
purpose: "Concise English summary of the 6 canonical roles and the 5 core main flows (MF1–MF5), aligned with business-flows.md v3.3 (direct-transfer settlement, no platform custody of funds)."
version: "2.0"
updated: 2026-10-06
---

# SmartDroneInspection — Business Flow Summary (MF1–MF5)

This document is the concise, plain-language view of how the SmartDroneInspection marketplace works: it connects **infrastructure owners (Client)** with **drone inspection / maintenance providers (Provider)**, supported by platform-hosted AI. Settlement is a **direct bank transfer from Client to Provider** after acceptance; the platform never holds money — it only computes and invoices its commission.

---

## I. The 6 Canonical Roles

| # | Role code | Who they are | Main responsibilities |
| :---: | :--- | :--- | :--- |
| 1 | `PLATFORM_ADMIN` | System administrator | Manages user accounts, security permissions, technical parameters (AI YOLO thresholds, MinIO storage limits), monitors audit logs and data integrity. Never touches commercial policy or dispute decisions. |
| 2 | `PLATFORM_OPERATOR` | Marketplace operations specialist | Vets Provider legal capability (licence, insurance, UAV registration, pilot certificates); configures marketplace parameters (acceptance review SLA, commission rate); tracks payment progress; issues the platform's commission & commission-VAT invoices; acts as **independent technical arbiter** for internal complaints. |
| 3 | `CLIENT` | Facility owner / customer | Creates inspection requests (direct appointment or open RFQ), approves quotations, signs electronic contracts, **pays the provider directly by bank transfer**, reviews & accepts reports, files complaints, creates maintenance tickets. |
| 4 | `PROVIDER_MANAGER` | Drone company / maintenance contractor manager | Receives RFQs, submits quotations, prepares mission plans and attaches flight permits, assigns staff, approves report release, **confirms receipt of client payment**, pays platform commission and tax. |
| 5 | `INSPECTOR` | Drone pilot / field technician | Builds the structural shot list and GSD/overlap parameters, performs live safety reconnaissance (Pilot-in-Command), flies the mission, re-flights on bad images, verifies AI findings, finalises and signs the report draft as author. |
| 6 | `MAINTENANCE_ENGINEER` | On-site repair engineer | Surveys defects, prepares method statements and material estimates, files change orders for hidden damage, executes repairs, captures mandatory before/after evidence pairs for acceptance. |

---

## II. The 5 Core Main Flows (MF1–MF5)

### MF1 — Inspection Request, Quotation & Electronic Contract

**Goal**: receive the inspection need, pick a capable provider, and sign a contract that fixes scope, price, schedule and payment terms.

- **MF1-01**: `CLIENT` states the objective (concrete cracks, steel corrosion, leakage), site and deadline; chooses **direct appointment** of a known partner or **open RFQ**.
- **MF1-02**: `SYSTEM` shortlists providers with suitable drones/sensors, valid flight certificates, free schedule and nearby location — then invites only those to quote.
- **MF1-03**: `PROVIDER_MANAGER` surveys remotely and quotes flight crew, technical labour, logistics and VAT — **never platform AI/storage fees**.
- **MF1-04**: `CLIENT` compares quotations, may request revisions, and approves the chosen one.
- **MF1-05**: `SYSTEM` generates the electronic service contract, **snapshotting** scope, price, review period, commission rate, cancellation policy and bad-weather rescheduling terms.
- **MF1-06**: both parties sign electronically. **The contract takes effect immediately; payment happens later by direct bank transfer after acceptance** — there is no advance-funding step.

*Exceptions*: no bids before RFQ close → widen geography or adjust budget; force-majeure weather → free reschedule, no penalty; client cancels pre-mobilisation → only reasonable evidenced preparation costs are deducted (per contract), remainder is simply never transferred.

### MF2 — Mission Planning & Flight-Legal Checks

**Goal**: set image sharpness parameters, guarantee flight safety, and attach the flight permit before mobilising.

- **MF2-01**: from the minimum crack size to find (e.g. ≥ 1.0 mm needs GSD ≤ 0.5 mm/px), the system recommends capture distance and camera settings for resolvable imagery.
- **MF2-02**: `INSPECTOR` sets overlap ratios (forward ≥ 75%, side ≥ 60%) so no structural corner is missed.
- **MF2-03**: `INSPECTOR` lists every component/angle (gimbal 0°/−45°/−90°) plus waypoints for programmed flight or a guided manual shot list, and scouts live obstacles (trees, power lines, wind) on site.
- **MF2-04**: `SYSTEM` cross-checks site coordinates against the national no-fly map (`cambay.mod.gov.vn`) — **a planning warning only, never a permit**.
- **MF2-05**: `PROVIDER_MANAGER` attaches the permit number issued by the competent military authority (when permit-required under current regulations) and verifies UAV registration and pilot licence conditions.
- **MF2-06**: pilot signs the live safety commitment; `PROVIDER_MANAGER` approves and releases the order: **`READY_FOR_FLIGHT`**.

*Exceptions*: no permit obtainable → plan rejected, notify client for extension or force-majeure cancellation; camera cannot meet GSD → approval blocked until equipment/geometry corrected.

### MF3 — Field Flight, Quality Gate, AI Detection & Technical Report

**Goal**: fly safely, enforce image quality on site, use AI to spot cracks, and release the report through mandatory human verification.

- **MF3-01**: `INSPECTOR` activates the session, runs the pre-flight check and flies the planned angles. Severe weather → safe abort, reason logged, make-up flight scheduled.
- **MF3-02**: `INSPECTOR` uploads all high-resolution originals to platform MinIO (chunked upload).
- **MF3-03**: `SYSTEM` stores GPS coordinates, altitude, gimbal angle, timestamp and a tamper-evident **SHA-256** checksum per file.
- **MF3-04**: quality gate flags blurry/dark/incomplete images so the pilot **re-shoots on the spot** before leaving site.
- **MF3-05**: `SYSTEM` (YOLO) boxes cracks/corrosion/spalling and **estimates length/width in mm** from capture geometry → defect candidates with bounding boxes.
- **MF3-06**: `INSPECTOR` reviews each candidate: **Confirm / Modify / Reject**, and draws anything the AI missed (manual findings) with survey-grade measurement.
- **MF3-07**: `SYSTEM` (LLM) compiles flight data, approved defects and evidence images into a report draft, marking AI-assisted content.
- **MF3-08**: `INSPECTOR` (as author) re-reads the draft against the imagery, fixes wording and conclusions, and **electronically signs it**.
- **MF3-09**: `PROVIDER_MANAGER` checks completeness against the contract and **signs the official release**; the contractual review clock $T_{rev}$ starts.

*Exceptions*: in-flight incident (signal/battery/motor) → fail-safe landing, incident log, reschedule; sudden weather → abort and preserve captured data; AI service outage → manual fallback so the deadline holds.

### MF4 — Report Review, Acceptance & Direct Payment

**Goal**: the client reviews and accepts (or the contract auto-accepts), then pays the provider **directly by bank transfer**, and the platform settles its commission through its own invoice.

- **MF4-01**: `CLIENT` inspects the report on web/phone (zoomable photos, defect positions on the 3D model, risk grades); the contractual review period counts down.
- **MF4-02 (clarification)**: `CLIENT` raises questions; `PROVIDER_MANAGER`/`INSPECTOR` explain or issue a corrected report before acceptance.
- **MF4-03 (complaint)**: either party clicks **"Open complaint"** → the system **pauses acceptance and payment confirmation**. `PLATFORM_OPERATOR` works with both sides and compares raw imagery and flight data to reach an objective finding (free re-flight, or rejection).
- **MF4-04a (manual acceptance)**: satisfied → **"Accept & sign minutes"**; minutes carry both parties' signatures.
- **MF4-04b (auto acceptance)**: review period expires (example: 7 days) with no response and no complaint → the system records acceptance per the contract.
- **MF4-05 (payment & commission — direct transfer)**:
  1. `SYSTEM` generates the electronic **Payment Invoice** with the contract amount and PROVIDER_MANAGER's bank account.
  2. `CLIENT` transfers **100% of the inspection fee directly to PROVIDER_MANAGER's bank account**.
  3. `PROVIDER_MANAGER` verifies the credit and clicks **"Confirm receipt"** → status **`PAID`**; the provider then sends its VAT service invoice to the client per tax law.
  4. The system computes platform commission + commission VAT; `PLATFORM_OPERATOR` issues the platform's service invoice to PROVIDER_MANAGER, who pays the commission to the platform separately.

*Exception*: a party rejecting the platform's internal mediation outcome keeps its full right to sue in court or arbitration (VIAC).

### MF5 — Defect Repair, Maintenance Payment & Warranty

**Goal**: turn MF4 defects into repair orders with controlled changes, before/after acceptance, direct settlement, and a warranty tracked to automatic closure.

- **MF5-01**: `CLIENT` selects dangerous defects from the MF4 report and picks one of three dispatch modes: **priority to the inspection provider** (if it holds verified maintenance capability), **direct appointment** of a known maintenance partner, or **open RFQ** to capable contractors.
- **MF5-02**: `PROVIDER_MANAGER` builds the technical method statement (epoxy injection, polymer mortar, corrosion treatment), full cost estimate and **warranty commitment (e.g. 6 or 12 months)** from the drone defect dossier plus site survey.
- **MF5-03**: both parties sign the electronic repair contract: lump-sum price, schedule, acceptance criteria and free-warranty clause.
- **MF5-04**: `MAINTENANCE_ENGINEER` repairs on site — **mandatory before/after photo pair at the same angle**, uploaded with the materials log.
- **MF5-05 (change order)**: hidden damage beyond the estimate → stop, photograph, and obtain client approval of the extra cost before continuing.
- **MF5-06 (completion acceptance)**: `CLIENT` compares before/after pairs on the app — not achieved → **rework loop** (free within committed scope); achieved → both sign the completion minutes.
- **MF5-07 (payment & commission — direct transfer)**: the same four-step pattern as MF4-05 — invoice → direct transfer to the provider's bank account → provider confirms → **`PAID`**, plus the platform's commission invoice.
- **MF5-08 (warranty & closure)**: the system starts the warranty countdown snapshotted in the order. Defect recurrence within warranty → client opens a warranty claim and the provider fixes it **free of charge** per contract. Warranty expires with a stable structure → the system **auto-closes the ticket**, completing 100% of the lifecycle.

*Branches*: before/after rejection → provider reworks free within scope (otherwise a change request first); high/hazardous structures → optional post-repair drone re-inspection via a new inspection request.

---

## III. RACI Matrix (summary)

| Core process | `PLATFORM_ADMIN` | `PLATFORM_OPERATOR` | `CLIENT` | `PROVIDER_MANAGER` | `INSPECTOR` | `MAINTENANCE_ENGINEER` |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **MF1: RFQ & quotation approval** | - | C | **A** | **R** | - | - |
| **MF1: E-contract signing (no funding step)** | I | C | **A / R** | **R** | - | - |
| **MF2: Mission plan (GSD, overlap, shot list)** | - | - | I | **A** | **R** | - |
| **MF2: Flight dossier & safety sign-off** | I | C | I | **A / R** | **R (Pilot)** | - |
| **MF3: Field flight & evidence upload** | - | - | I | I | **A / R** | - |
| **MF3: AI verification & author signature** | - | - | - | I | **A / R** | - |
| **MF3: QA release signature** | - | - | I | **A (Release)** | **R (Author)** | - |
| **MF4: Acceptance & payment invoice / direct transfer** | I | C | **A / R** | **R (Confirm receipt)** | - | - |
| **MF4: Complaint mediation** | I | **A / R** | C | C | C | - |
| **MF5: Technical plan & quotation** | - | - | **A** | **R** | - | C |
| **MF5: Before/after execution & change order** | - | - | **A** | I | - | **R** |
| **MF5: Completion acceptance & warranty closure** | I | C | **A** | I | - | I |
| **Commission & commission-VAT invoicing** | I | **A / R** | I | **R (Payer)** | - | - |

*Legend*: **R** = responsible, **A** = accountable, **C** = consulted, **I** = informed.

---

*Full detail, exception branches, feedback loops and the complete RACI matrix: see [business-flows.md](business-flows.md) v3.3.*
