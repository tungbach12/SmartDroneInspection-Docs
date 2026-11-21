---
title: "Report 7 - Release Package & User Guides"
document_type: report7-section
weight: 60
source: "Report7_Final Project Report.docx"
---
# VI. Release Package & User Guides

## 1. Deliverable Package

| No. | Deliverable Item | Description |
| --- | --- | --- |
| 1 | Project Schedule/Tracking | Task schedule, milestone dates, and effort tracking against the weighted plan in Report 2 (`208` md). |
| 2 | Project Backlog | The twenty-four atomic feature backlog (`FE-01`–`FE-24`) across `MF1`–`MF4`. |
| 3 | Source Codes | Four independent repositories: backend service (`SmartDroneInspection-backend`), web portals (`SmartDroneInspection-frontend`), Customer mobile client (`SmartDroneInspection-mobile`), and documentation (`SmartDroneInspection-docs`). |
| 4 | Database Script(s) | Automated schema migration scripts (`V1`–`V4` and `V60`–`V66`) defining the PostgreSQL 17 database (45 application tables), `pgvector` support for `DroneKnowledgeAI`, and plain-text building ownership details. |
| 5 | Final Report Document | Reports 1–7 of this documentation set, exported against the official templates. |
| 6 | Test Cases Document | `Report5_Test Report.xlsx` (`v3.9`) with twenty-four feature sheets (`Feature 1`–`Feature 24`) covering `67` active cases, plus the executed results in Report 5 §5. |
| 7 | Defects List | The defect log, including the two open defects recorded above. |
| 8 | Issues List | Outstanding issues and known limitations, including the out-of-scope items in Part III §3.8 (Report 3 §3.26). |
| 9 | Slide | The defence presentation used for the final review. |

## 2. Installation Guides

### 2.1 System Requirements

**Hardware Requirements**

| Component | Minimum Specification | Recommended Specification | Notes |
| --- | --- | --- | --- |
| Processor | 64-bit x86_64, 4 logical cores | 8+ logical cores | Detection inference (`YOLO11`) and FFmpeg video transcoding are CPU/RAM intensive. |
| Memory (RAM) | 8 GB | 16 GB | Allocate at least 8 GB to Docker Desktop when running `ai-inference` alongside Postgres and backend. |
| Disk Space | 40 GB free | 60+ GB SSD | Required for container images, PostgreSQL storage, and MinIO photo/MP4 evidence buckets. |
| Network / Ports | Localhost loopback | Stable broadband / LAN (`14551/udp`, `5762/tcp`) | Required for package installs, optional OpenAI/PayOS/VNPay callbacks, and Mission Planner MAVLink bridge. |

**Software Prerequisites**

| Layer | Requirement | Purpose |
| --- | --- | --- |
| Containerization | Docker Engine 27+ with Compose plugin | Runs `postgres` (`pgvector:pg17`), `minio`, `ai-inference`, `smartdronehub`, and `backend`. |
| Backend Runtime | Java 21 (Temurin) | Local backend builds (`./mvnw test`, `./mvnw verify`). |
| Frontend Toolchain | Node.js 22+ & npm | Builds and serves the React 19 + TypeScript Web Portal (`vite`). |
| Mobile SDK | Flutter SDK + Android toolchain / Chrome | Builds and runs the `CUSTOMER` mobile client (`flutter run`). |
| Client Browser | Modern Chrome / Edge | Runs all four web portals cleanly in Light/Dark mode. |

### 2.2 Installation Instruction

#### Step 1 — Clone Repositories and Configure Environment

Clone the four repositories into sibling directories so cross-repo proxies and tooling resolve as configured. In `SmartDroneInspection-backend/`, copy the environment template to `.env` and populate PostgreSQL credentials, MinIO bucket and keys, JWT/ticket signing secrets (long random values — never commit real secrets), allowed CORS origin (`http://localhost:3000`), and bootstrap administrator credentials. Optional integrations (`ai-inference` Vision fallback, PayOS, VNPay, and Google OAuth2) default cleanly to disabled/manual modes when keys are omitted.

#### Step 2 — Start Backend Stack and Apply Flyway Migrations

Launch all five containers inside `SmartDroneInspection-backend/` with `docker compose up -d --build`. On first startup, automated database migrations configure all schema tables, enable vector knowledge search, load built-in engineering standards and historical case backfill, and prepare plain-text building ownership fields with no manual database steps required. Verify service readiness via `docker compose ps` and `curl http://localhost:8080/actuator/health` returning `UP`.

#### Step 3 — Start Web Portal and Mobile Client

In `SmartDroneInspection-frontend/`, copy the frontend `.env` example, run `npm install`, and start `npm run dev` on `http://localhost:3000` (proxies `/api/*` directly to `http://localhost:8080`). In `SmartDroneInspection-mobile/`, run `flutter pub get` and launch `flutter run --dart-define=API_BASE_URL=http://10.0.2.2:8080/api/v1` (Android emulator) or configure the LAN/loopback host matching the backend.

#### Step 4 — Bootstrap Login and Troubleshooting

Sign in using the bootstrap `ADMIN` account, rotate credentials immediately, and provision additional accounts in `/admin/platform-users`. If the backend container fails on startup, verify both JWT/media signing secrets meet minimum length; if file uploads fail while API calls succeed, inspect MinIO credentials and bucket creation; if the AI embedding service is unavailable, finding drafting and recommendations automatically fall back to deterministic keyword matching without blocking workflows.

## 3. User Manual

### 3.1 Overview

SmartDroneInspection organizes daily operations into six end-to-end workflows across its four authenticated Web Portals (`CUSTOMER`, `INSPECTOR`, `MANAGER`, `ADMIN`) and the Customer Mobile App (`CUSTOMER` only). Every figure in §3.2–§3.7 marks interactive controls using numbered red callouts (`❶`, `❷`, `❸`, `❹`) matched directly to each step.

```mermaid
%% title: Workflow 1 — Customer Onboarding, Airspace Screening and Asset Setup
flowchart LR
  W1A["1. Public Landing & Sign Up"] --> W1B["2. Customer Registration + OTP"]
  W1B --> W1C["3. Building Form & Airspace Map"]
  W1C -->|"Restricted Zone"| W1D["4. Admin Onboarding Review"]
  W1C -->|"Clear Zone"| W1E["5. Building Register & Detail"]
  W1D --> W1E
  W1E --> W1F["6. Notifications & Settings"]
```

```mermaid
%% title: Workflow 2 — Partner Inspector Admission and Drone Registration
flowchart LR
  W2A["1. Public Inspector Apply (3 Steps)"] --> W2B["2. Staff Onboarding Queue Review"]
  W2B --> W2C["3. Partner Roster Qualified"]
  W2C --> W2D["4. Inspector Opens My Drones"]
  W2D --> W2E["5. Submit Specs, Photos & Docs"]
  W2E -->|"Staff Approve"| W2C
```

```mermaid
%% title: Workflow 3 — Service Request, Negotiation, Contract and Dispatch
flowchart LR
  W3A["1. Customer Submits Request"] --> W3B["2. Manager Claims & Quotes"]
  W3A <-->|"Order Chat"| W3C["3. Customer & Manager Negotiate"]
  W3B --> W3D["4. Customer Accepts Quote"]
  W3D --> W3E["5. Signed Paper Contract Uploaded"]
  W3E --> W3F["6. Manager Dispatches Inspector + Drone"]
  W3F --> W3G["7. Scheduled Inspection Occurrence"]
```

```mermaid
%% title: Workflow 4 — Mission Execution, Flight Permit and Live Hub Telemetry
flowchart LR
  W4A["1. Inspector Accepts Assignment"] --> W4B["2. Upload Flight Permit & Metadata"]
  W4B --> W4C["3. Manager Permit Audit"]
  W4C -->|"Approved"| W4D["4. Pre-flight Safety Checklist"]
  W4D --> W4E["5. Connect Live MAVLink Telemetry"]
  W4E --> W4F["6. Complete Flight & Post-flight Items"]
```

```mermaid
%% title: Workflow 5 — Field Evidence Intake, AI Detection and Findings Confirmation
flowchart LR
  W5A["1. Upload Photos & Resumable MP4 Video"] --> W5B["2. Run Batch / Image YOLO11 Detection"]
  W5B --> W5C["3. Draft Note with AI & Cite Standards"]
  W5C --> W5D["4. Confirm Official Findings Baseline"]
```

```mermaid
%% title: Workflow 6 — Report Authoring, Review, Acceptance and Financial Settlement
flowchart LR
  W6A["1. Compile & Submit Report + AI Summary"] --> W6B["2. Manager Independent Review"]
  W6B -->|"Publish v1+"| W6C["3. Customer Reviews Official Report"]
  W6C --> W6D["4. Accept & Pay (PayOS VietQR / VNPay)"]
  W6D --> W6E["5. Customer & Manager Finance Ledgers"]
  W6E --> W6F["6. Partner Net Payout & Settlement"]
```

### 3.2 Workflow 1: Customer Onboarding, Airspace Screening and Asset Setup (`FE-01`, `FE-04`, `FE-06`, `FE-07`, `FE-12`)

**Purpose.** Onboard a new customer organization, screen building coordinates against Vietnam airspace zones, configure inspection checkpoints and ownership notes, and verify notification settings.
**Actors.** Prospective Customer (public), `CUSTOMER`, `ADMIN`.
**Preconditions.** Backend and Web Portal are reachable; target building coordinates and category are known.

**Step 1 — Navigate from Public Landing.** Open the platform landing page (`http://localhost:3000/`). Review the navigation in Header bar ❶, click **Sign in** ❷ if already registered, or select **Sign up** ❸ / **Get a consultation** ❹ to begin onboarding.

![Workflow 1 Step 1 — Public landing page entry controls.](assets/manual/wf1-01-landing.png)

*Figure 7.11 — Workflow 1 Step 1 — Public landing page entry controls.*

**Step 2 — Complete Customer Registration.** Fill organization identity, administrator name, email, and policy-compliant password inside the **Registration form** ❶ (or follow **Inspector link** ❷ to switch to partner onboarding), then click **Submit button** ❸ and confirm the email OTP challenge.

![Workflow 1 Step 2 — Customer registration form and OTP submission trigger.](assets/manual/wf1-02-customer-register.png)

*Figure 7.12 — Workflow 1 Step 2 — Customer registration form and OTP submission trigger.*

**Step 3 — Screen Building Coordinates on Airspace Map.** Sign in as `CUSTOMER`, open **Assets -> + New asset**, enter structural height/footprint, and click **Pick on Google Maps** to launch the **Interactive Airspace Map dialog** ❶. Pin the exact building coordinates; clear locations proceed directly whereas prohibited zones block submission.

![Workflow 1 Step 3 — Interactive Airspace Map dialog evaluating building coordinates.](assets/manual/wf1-03-airspace-map.png)

*Figure 7.13 — Workflow 1 Step 3 — Interactive Airspace Map dialog evaluating building coordinates.*

**Step 4 — Adjudicate Restricted-Zone Queue (if flagged).** When an application falls in a restricted airspace zone, `ADMIN` opens **Onboarding reviews**, selects **Onboarding queue tabs** ❶ (`Customer Airspace` / `Drone Registrations`), filters entries, and records the decision inside **Review panel** ❷.

![Workflow 1 Step 4 — Admin onboarding and airspace review console.](assets/manual/wf1-04-admin-onboarding-review.png)

*Figure 7.14 — Workflow 1 Step 4 — Admin onboarding and airspace review console.*

**Step 5 — Manage Building Register.** Inside your **Assets** page, click **+ New asset** ❶ to add more structures (including structural specs and plain-text Ownership Information), narrow the register using **Search & status filter** ❷, or click **Detail** ❸ on `VHS-TPHCM` to inspect checkpoints and documents.

![Workflow 1 Step 5 — Customer building inventory and filter controls.](assets/manual/wf1-05-customer-assets.png)

*Figure 7.15 — Workflow 1 Step 5 — Customer building inventory and filter controls.*

**Step 6 — Maintain Checkpoints and Reference Documents.** In the building modal, verify coordinates and status in **Asset detail header** ❶, and customize building inspection checkpoints alongside duplicate-checked blueprints inside **Checkpoints and documents** ❷.

![Workflow 1 Step 6 — Customer building detail checkpoints and document attachments.](assets/manual/wf1-06-customer-asset-detail.png)

*Figure 7.16 — Workflow 1 Step 6 — Customer building detail checkpoints and document attachments.*

**Step 7 — Verify Notification Inbox and Account Settings.** Open **Notifications** ❶ from the account sidebar to inspect deduplicated onboarding and lifecycle updates inside **Notice list** ❷.

![Workflow 1 Step 7 — Account notifications inbox and deep-link alerts.](assets/manual/wf1-07-notifications-settings.png)

*Figure 7.17 — Workflow 1 Step 7 — Account notifications inbox and deep-link alerts.*

### 3.3 Workflow 2: Partner Inspector Admission and Drone Registration (`FE-02`, `FE-03`)

**Purpose.** Admit a qualified drone pilot through public application review and register an airframe eligible for mission dispatch under Decree 288/2025/ND-CP.
**Actors.** Prospective Inspector (public), `INSPECTOR`, `MANAGER` / `ADMIN`.
**Preconditions.** Applicant holds a valid civil pilot licence scan; drone registration/ownership documents are ready.

**Step 1 — Submit Public Inspector Application.** Open the Partner Inspector registration page, follow the **3-step stepper** ❶ (`Account -> CCCD & Licence -> OTP & Submit`), complete credentials and licence details inside **Applicant inputs** ❷, attach the licence scan, and verify OTP.

![Workflow 2 Step 1 — Three-step Partner Inspector public application form.](assets/manual/wf2-01-inspector-apply.png)

*Figure 7.18 — Workflow 2 Step 1 — Three-step Partner Inspector public application form.*

**Step 2 — Review Application or Drone Queue.** A `MANAGER` or `ADMIN` opens **Onboarding reviews**, toggles **Queue tabs** ❶ (`Inspector Applications` / `Drone Registrations`), applies status chips inside **Filters & queue area** ❷, and approves qualified records (provisioning the Inspector account upon approval).

![Workflow 2 Step 2 — Onboarding compliance review tabs and filters.](assets/manual/wf2-02-review-queue.png)

*Figure 7.19 — Workflow 2 Step 2 — Onboarding compliance review tabs and filters.*

**Step 3 — Confirm Eligibility in Partner Roster.** Open **Partner inspectors** and inspect **Partner inspector row** ❶ to verify active status, pilot licence class (`Class B` / `Class A`), licence expiry, and eligible aircraft.

![Workflow 2 Step 3 — Manager partner inspectors eligibility directory.](assets/manual/wf2-03-partner-roster.png)

*Figure 7.20 — Workflow 2 Step 3 — Manager partner inspectors eligibility directory.*

**Step 4 — Open My Drones Registry.** The approved `INSPECTOR` signs in, navigates to **My drones**, reviews existing approvals on **Owned drone card** ❷ (`DJI Mavic 3 Enterprise`), or clicks **Register drone** ❶ to add a new airframe.

![Workflow 2 Step 4 — Inspector owned drone fleet registry.](assets/manual/wf2-04-my-drones.png)

*Figure 7.21 — Workflow 2 Step 4 — Inspector owned drone fleet registry.*

**Step 5 — Submit Aircraft Specs, Photos and Documents.** Confirm details under **Register drone title** ❶, fill serial number, Decree 288 MTOW category, real photos, capability checkboxes, and mandatory documents in **Drone specs & docs** ❷, and submit for staff review.

![Workflow 2 Step 5 — Register owned drone specification and document form.](assets/manual/wf2-05-drone-register-form.png)

*Figure 7.22 — Workflow 2 Step 5 — Register owned drone specification and document form.*

### 3.4 Workflow 3: Service Request, Quotation, Contract and Dispatch (`FE-08`–`FE-11`)

**Purpose.** Create a building inspection request, negotiate commercial terms via Order Chat, record customer acceptance and the signed offline contract, and dispatch an eligible partner crew.
**Actors.** `CUSTOMER`, `MANAGER`.
**Preconditions.** At least one `ACTIVE` building exists and an approved Inspector + owned Drone pair is eligible.

**Step 1 — Open Customer Service Requests.** In **Service Requests**, track active requests with concise recurring request titles cleanly displayed in the compact four-column list via **Request row** ❷ or click **+ New service request** ❶ to start a new booking.

![Workflow 3 Step 1 — Customer service requests list and creation button.](assets/manual/wf3-01-cus-requests.png)

*Figure 7.23 — Workflow 3 Step 1 — Customer service requests list and creation button.*

**Step 2 — Define Schedule and Recurrence Cadence.** Inside **Dialog title** ❶, select target building, first inspection date (`>= 20` days lead time in `Asia/Ho_Chi_Minh`), flight hours, and one-time or recurring interval inside **Request schedule & recurrence form** ❷, then submit.

![Workflow 3 Step 2 — Customer service request form with schedule validation.](assets/manual/wf3-02-cus-new-request.png)

*Figure 7.24 — Workflow 3 Step 2 — Customer service request form with schedule validation.*

**Step 3 — Claim Request as Platform Manager.** Manager opens `/manager/contracts`, selects an unassigned or claimed **Service request card** ❶, and steps into the commercial quote workspace.

![Workflow 3 Step 3 — Manager incoming service requests queue.](assets/manual/wf3-03-mgr-requests.png)

*Figure 7.25 — Workflow 3 Step 3 — Manager incoming service requests queue.*

**Step 4 — Negotiate Scope via Manager Order Chat.** Open **Messages**, choose the **Request thread** ❶, and respond to Customer questions or share scope clarifications using **Order chat reply** ❷.

![Workflow 3 Step 4 — Manager Order Chat workspace.](assets/manual/wf3-04-mgr-messages.png)

*Figure 7.26 — Workflow 3 Step 4 — Manager Order Chat workspace.*

**Step 5 — Reply from Customer Messages Portal.** On `/client/messages`, switch modes with **Manager/Inspector toggle** ❶ (`Service requests`) and post messages or attachments using **Chat composer** ❷.

![Workflow 3 Step 5 — Customer Order Chat negotiation panel.](assets/manual/wf3-05-cus-messages.png)

*Figure 7.27 — Workflow 3 Step 5 — Customer Order Chat negotiation panel.*

**Step 6 — Issue VND Quote, Upload Contract and Dispatch Crew.** After Customer accepts the VND quotation, Manager follows **Commercial & dispatch stepper** ❶, records the scanned offline contract in **Paper contract card** ❷, validates eligible candidates, and dispatches crew on **Assigned occurrence & invoice** ❸.

![Workflow 3 Step 6 — Manager commercial quotation, signed contract, and occurrence dispatch.](assets/manual/wf3-06-mgr-quote-agreement.png)

*Figure 7.28 — Workflow 3 Step 6 — Manager commercial quotation, signed contract, and occurrence dispatch.*

**Step 7 — Verify Accepted Quote and Occurrence on Customer Side.** Customer opens the request detail to inspect **Contract lifecycle stepper** ❶, download the agreement via **Download signed contract** ❷, and launch tracking via **Open inspection** ❸.

![Workflow 3 Step 7 — Customer request detail showing accepted quote and signed contract.](assets/manual/wf3-07-cus-quote-review.png)

*Figure 7.29 — Workflow 3 Step 7 — Customer request detail showing accepted quote and signed contract.*

**Step 8 — Confirm Dispatched Inspection in Manager Queue.** Manager opens **Inspections** to verify **Scheduled occurrence** ❶ shows crew acceptance status (`Pending Acceptance` within the response window or `Accepted`) before field work begins.

![Workflow 3 Step 8 — Manager scheduled occurrence monitor.](assets/manual/wf3-08-mgr-inspections.png)

*Figure 7.30 — Workflow 3 Step 8 — Manager scheduled occurrence monitor.*

### 3.5 Workflow 4: Mission Execution, Flight Permit and Live Hub Telemetry (`FE-10`, `FE-13`, `FE-14`)

**Purpose.** Accept partner dispatch, submit and independently audit the regulatory flight permit, execute pre-flight checks, connect live ArduPilot/Mission Planner MAVLink telemetry (`SmartDroneHub`), and close post-flight verification.
**Actors.** `INSPECTOR`, `MANAGER`, SmartDroneHub (`14551/udp` / `5762/tcp`).
**Preconditions.** Dispatched inspection is `SCHEDULED` and accepted by `INSPECTOR`; flight permit document (`<= 25 MB`) is available.

**Step 1 — Open Assigned Inspection.** `INSPECTOR` opens **Inspections** in the operations portal and selects **Assigned building inspection** ❶ to accept the mission before the response deadline and enter the workspace.

![Workflow 4 Step 1 — Inspector assigned inspections schedule.](assets/manual/wf4-01-ins-inspections.png)

*Figure 7.31 — Workflow 4 Step 1 — Inspector assigned inspections schedule.*

**Step 2 — Coordinate Access via Inspection Chat.** Open `/operations/messages`, reply to Customer site instructions using **Inspection chat composer** ❷, or jump directly to field stages via **Open inspection shortcut** ❶.

![Workflow 4 Step 2 — Inspector per-inspection chat with Customer.](assets/manual/wf4-02-ins-messages.png)

*Figure 7.32 — Workflow 4 Step 2 — Inspector per-inspection chat with Customer.*

**Step 3 — Review Workspace Lifecycle Tracker.** In Stage 0 (`/tracking`), inspect **Inspection stepper** ❶ across all seven stages and follow the guided prompt inside **Next action panel** ❷.

![Workflow 4 Step 3 — Inspection workspace tracking and stage progress.](assets/manual/wf4-03-ins-tracking.png)

*Figure 7.33 — Workflow 4 Step 3 — Inspection workspace tracking and stage progress.*

**Step 4 — Upload Mission Flight Permit.** Open Stage 1 via **Workspace stage bar** ❶, inspect or enter permit number, issuing authority, validity window, drone serial, and max altitude in **Permit details card** ❷, or click **Replace permit** ❸ (`184/TC-QC.pdf`).

![Workflow 4 Step 4 — Inspector mission flight permit panel.](assets/manual/wf4-04-ins-permit.png)

*Figure 7.34 — Workflow 4 Step 4 — Inspector mission flight permit panel.*

**Step 5 — Approve Permit Independently (Manager).** A distinct `MANAGER` navigates via **Manager stage stepper** ❶ to inspect metadata and approve or reject with reason inside **Permit audit card** ❷.

![Workflow 4 Step 5 — Manager independent flight permit verification panel.](assets/manual/wf4-08-mgr-audit.png)

*Figure 7.35 — Workflow 4 Step 5 — Manager independent flight permit verification panel.*

**Step 6 — Complete Pre-flight Safety Checklist.** Once the permit is approved, `INSPECTOR` opens **Pre-flight stage active** ❶, verifies all items inside **Checklist items** ❷ (or clicks **Check all** ❸), adds a site observation note, and starts the field session (`In Progress`).

![Workflow 4 Step 6 — Pre-flight safety checklist verification.](assets/manual/wf4-05-ins-preflight.png)

*Figure 7.36 — Workflow 4 Step 6 — Pre-flight safety checklist verification.*

**Step 7 — Connect Live MAVLink Telemetry (`SmartDroneHub`).** On **Flight Operation stage** ❶, start ArduPilot SITL / Mission Planner (loaded with `wp.waypoints`), click **Connect Flight Operations**, monitor real-time `IN_FLIGHT`, `Mode: AUTO`, GPS, altitude, speed, heading, battery, waypoint, and `Gimbal Active` inside **Live MAVLink telemetry & Gimbal feed** ❷ (or import an `SRT/CSV/KML/GPX` log if flying offline), then click **Complete flight** ❸ when the mission finishes.

![Workflow 4 Step 7 — Live ArduPilot/Mission Planner MAVLink telemetry streaming in SmartDroneHub.](assets/manual/wf4-06-ins-flightsession.png)

*Figure 7.37 — Workflow 4 Step 7 — Live ArduPilot/Mission Planner MAVLink telemetry streaming in SmartDroneHub.*

**Step 8 — Verify Post-flight and Target Building Items.** Advance to **Post-flight stage stepper** ❶, tick each inspected structural checkpoint inside **Target building inspection items** ❷ and post-flight checks, and submit **Complete session** to complete the field work.

![Workflow 4 Step 8 — Post-flight checklist and target building checkpoint completion.](assets/manual/wf4-07-ins-postflight.png)

*Figure 7.38 — Workflow 4 Step 8 — Post-flight checklist and target building checkpoint completion.*

### 3.6 Workflow 5: Evidence Intake, AI Defect Detection and Findings Confirmation (`FE-15`, `FE-16`, `FE-17`)

**Purpose.** Upload building photos and resumable MP4 video from the mission, run AI defect detection, refine notes using `DroneKnowledgeAI`, and confirm the official finding baseline.
**Actors.** `INSPECTOR`, Automated AI Pipeline (`YOLO11`, `DroneKnowledgeAI`, media processor).
**Preconditions.** Field session is active or completed; inspection photos and MP4 footage are staged locally.

**Step 1 — Upload Field Photos and MP4 Video.** Open Stage 5 (**Evidence**), select photos (`<= 10 MB`) and MP4 video (`<= 2 GB`, automatically resumable in chunks if interrupted) via **Choose files & Upload** ❶, wait for background video optimization to finish, and review captures/playback inside **Evidence register card** ❷.

![Workflow 5 Step 1 — Field evidence upload controls and register with photos and transcoded MP4 video.](assets/manual/wf5-01-ins-evidence.png)

*Figure 7.39 — Workflow 5 Step 1 — Field evidence upload controls and register with photos and transcoded MP4 video.*

**Step 2 — Filter Findings and Trigger Batch AI Analysis.** Open Stage 6 (`/findings`), slice captures with **Status filter chips** ❶ (`All active`, `Unconfirmed`, `Confirmed`), invoke **Batch analyze all images** ❸ (`YOLO11`), or generate technical notes across unconfirmed defects via **Batch Draft all notes** ❷.

![Workflow 5 Step 2 — Defect findings filter chips and batch AI actions.](assets/manual/wf5-02-ins-findings-toolbar.png)

*Figure 7.40 — Workflow 5 Step 2 — Defect findings filter chips and batch AI actions.*

**Step 3 — Review Bounding Box and Draft Note with AI.** Inspect the normalized lesion bounding box on **Annotated evidence frame** ❸, click **Draft note with AI** ❶ to generate an editable engineering-standard note (and inspect cited `References` when drafted), then finalize using **Confirm** ❷.

![Workflow 5 Step 3 — Finding card with bounding region, AI-drafted ASTM note, and human confirmation.](assets/manual/wf5-03-ins-findings-card.png)

*Figure 7.41 — Workflow 5 Step 3 — Finding card with bounding region, AI-drafted ASTM note, and human confirmation.*

**Step 4 — Confirm Official Findings Baseline.** Confirm every valid finding via **Confirm findings baseline** ❶ (or acknowledge zero defects) so Stage 7 report authoring unlocks.

![Workflow 5 Step 4 — Explicit findings baseline confirmation action.](assets/manual/wf5-04-ins-findings-confirm.png)

*Figure 7.42 — Workflow 5 Step 4 — Explicit findings baseline confirmation action.*

### 3.7 Workflow 6: Report Authoring, Review, Acceptance and Financial Settlement (`FE-05`, `FE-17`–`FE-24`)

**Purpose.** Prepare and publish the official inspection report, allow the Customer to accept and pay online through PayOS VietQR or VNPay, and record Partner Inspector payouts.
**Actors.** `INSPECTOR`, `MANAGER`, `CUSTOMER`, Payment Gateway (PayOS / VNPay).
**Preconditions.** Official findings baseline has been confirmed.

**Step 1 — Generate AI Summary and Submit Report.** In Stage 7 (`/report`), generate/review **AI Executive Summary & Matched Cases** ❶, inspect formatting with **Preview PDF** ❷ or **Download report** ❸, and submit version `v1` for independent review.

![Workflow 6 Step 1 — Inspector report preparation, AI summary, and PDF preview controls.](assets/manual/wf6-01-ins-report.png)

*Figure 7.43 — Workflow 6 Step 1 — Inspector report preparation, AI summary, and PDF preview controls.*

**Step 2 — Locate Submitted Report in Manager Queue.** A distinct `MANAGER` opens **Reports** and selects **Submitted/Published report row** ❶.

![Workflow 6 Step 2 — Manager inspection reports review queue.](assets/manual/wf6-02-mgr-reports.png)

*Figure 7.44 — Workflow 6 Step 2 — Manager inspection reports review queue.*

**Step 3 — Perform Independent Review and Publication.** Inside **Report Decision stage** ❶, verify findings and narrative in **Submitted report & AI summary** ❷, download verification copy via **Download report** ❸, and either **Publish official report** or **Return for revision** with reason.

![Workflow 6 Step 3 — Manager independent report review and publication screen.](assets/manual/wf6-03-mgr-review.png)

*Figure 7.45 — Workflow 6 Step 3 — Manager independent report review and publication screen.*

**Step 4 — Open Published Deliverable (Customer).** `CUSTOMER` selects **Inspections menu item** ❶ and opens **Published inspection row** ❷ (`Report ready · v1`).

![Workflow 6 Step 4 — Customer inspections list highlighting published deliverable.](assets/manual/wf6-04-cus-inspections.png)

*Figure 7.46 — Workflow 6 Step 4 — Customer inspections list highlighting published deliverable.*

**Step 5 — Accept Report and Pay via PayOS VietQR / VNPay.** Track progress along **Acceptance & Payment stepper** ❶, download the VAT invoice notice using **Payment notice / document button** ❷, accept the official report, and complete payment via **PayOS / VNPay payment card** ❸.

![Workflow 6 Step 5 — Customer official report acceptance and PayOS/VNPay settlement panel.](assets/manual/wf6-05-cus-report-pay.png)

*Figure 7.47 — Workflow 6 Step 5 — Customer official report acceptance and PayOS/VNPay settlement panel.*

**Step 6 — Verify Customer Payment Ledger.** Open **Finance History** in the customer portal to confirm verified payment status, gateway/manual method, and receipt download inside **Payment ledger table** ❶.

![Workflow 6 Step 6 — Customer payment history ledger.](assets/manual/wf6-06-cus-finance.png)

*Figure 7.48 — Workflow 6 Step 6 — Customer payment history ledger.*

**Step 7 — Record Partner Payout and Manage Refunds (Manager).** After verified customer payment unlocks eligibility, `MANAGER` opens the inspection's **Settlement** tab and records external payout reference or refund allocations inside **Payout & refund ledger** ❶.

![Workflow 6 Step 7 — Manager partner payout, refund, and receivable settlement console.](assets/manual/wf6-07-mgr-settlement.png)

*Figure 7.49 — Workflow 6 Step 7 — Manager partner payout, refund, and receivable settlement console.*

**Step 8 — Audit Platform Revenue, Commission and Taxes.** Open **Finance History** in the manager portal to inspect platform inflows, earned commission (`15%`), VAT/personal income tax withholdings in **Revenue, commission & tax KPIs** ❶ and per-occurrence rows inside **Commission, VAT & payout table** ❷.

![Workflow 6 Step 8 — Manager platform revenue, commission, tax, and payout history ledger.](assets/manual/wf6-08-mgr-finance-history.png)

*Figure 7.50 — Workflow 6 Step 8 — Manager platform revenue, commission, tax, and payout history ledger.*
