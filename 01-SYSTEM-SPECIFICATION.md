# SmartDroneInspection — System Specification

> AI-powered Infrastructure Inspection Management Platform
> FA26SE112 · Capstone Project · Duration: 09/2026 – 03/2027
> Supervisors: Phạm Minh Trí (tripm14@fpt.edu.vn), Đặng Ngọc Minh Đức (ducdnm2@fpt.edu.vn)

---

## 1. Overview

SmartDroneInspection manages the complete infrastructure inspection lifecycle — assets, inspection planning, requests, drone missions, reports, defects, and maintenance tickets — while consuming drone operation services from **SmartDroneHub** via standardized REST APIs.

**Key architectural rule:** SmartDroneInspection is a *business-oriented inspection management platform*, NOT a drone control system. It is a **consumer** of SmartDroneHub services, never a controller.

### 1.1 Stakeholders & Labs
- Hardware (drones) provided by **AiTA Lab** for development, testing, and demo.
- Drone missions, telemetry, flight ops are managed by **SmartDroneHub** (common drone platform).

### 1.2 Repository Layout

| Path | Contents |
|------|----------|
| `docs/` | System specification, API spec, database design, UI/UX design |
| `backend/` | ASP.NET Core Web API solution (`SmartDroneInspection.sln`) |
| `frontend/` | ReactJS + Material UI web portal |
| `mobile/` | Flutter application (Inspector + Maintenance Engineer) |
| `deploy/` | Docker Compose deployment package |

---

## 2. Actors & Roles (RBAC)

| Role | Responsibilities |
|------|------------------|
| **Administrator** | Manages users, organizations, asset categories, system configuration |
| **Inspection Manager** | Creates inspection plans, approves requests, assigns inspectors, reviews reports |
| **Inspector** | Reviews assigned inspections, records findings, uploads evidence, generates reports |
| **Maintenance Engineer** | Manages maintenance tickets, updates repair status, tracks maintenance history |
| **Viewer** | Searches inspection records, views dashboards and historical reports |

---

## 3. Main Flows

### MF1 — Asset Management
1. Admin creates/updates asset categories.
2. Manager registers an asset: specifications, location, technical documents.
3. Asset lifecycle status is tracked (active, under maintenance, retired).
4. Inspection history accumulates per asset.

### MF2 — Inspection Planning & Request Management
1. Manager creates an inspection plan: asset(s), frequency, priority.
2. Plan generates a schedule; manager assigns inspectors.
3. A digital inspection request is created (manually or from a plan).
4. Manager approves / rejects / cancels the request.
5. Calendar + notifications are generated for scheduled inspections.

### MF3 — Drone Mission Execution (Integration)
1. Approved inspection request triggers a mission creation call to **SmartDroneHub Mission API**.
2. Mission status updates stream in real time via **SignalR**.
3. On completion, the system pulls telemetry, inspection images, and flight logs from SmartDroneHub.
4. Images are stored in **MinIO** and linked to the inspection record.

### MF4 — Inspection Report & Defect Management
1. Inspector reviews assigned inspection + drone images.
2. Inspector runs **DroneVisionAI** image analysis to detect potential defects.
3. Findings are recorded; evidence (photos) is attached.
4. Defects are classified with severity and repair recommendations.
5. Report is submitted; Manager reviews and approves/archives the report.
6. Optional: LLM generates a summary of the report.

### MF5 — Maintenance Ticket Lifecycle
1. Confirmed defect creates a maintenance ticket.
2. Ticket is assigned to a Maintenance Engineer.
3. Engineer updates repair progress (statuses until closed).
4. Closed tickets maintain a repair history per asset.

### MF6 — Authentication & Access Control (cross-cutting)
1. User authenticates → JWT issued.
2. All endpoints enforce RBAC per the role table above.
3. All sensitive actions write audit logs.

### AI Services (cross-cutting)
- **DroneVisionAI** — Inspection image analysis (defect detection). Used in MF4.
- **Report Summarization** — LLM-based concise report summaries. Used in MF4.
- **DroneKnowledgeAI** — Historical case recommendation (similar past cases + guidelines). Supports MF4/MF5.

---

## 4. Functional Requirements

### 4.1 User Management
- FR-UM-1 Authentication (login/logout, JWT)
- FR-UM-2 Authorization, role-based access control
- FR-UM-3 User profiles
- FR-UM-4 Audit logs

### 4.2 Asset Management
- FR-AM-1 Create/update assets
- FR-AM-2 Manage asset categories and documents
- FR-AM-3 Asset search
- FR-AM-4 Asset history, lifecycle tracking

### 4.3 Inspection Planning
- FR-IP-1 Create inspection plans
- FR-IP-2 Schedule inspections, assign inspectors
- FR-IP-3 Manage inspection calendars
- FR-IP-4 Inspection notifications

### 4.4 Inspection Request Management
- FR-IR-1 Create / approve / track / cancel inspection requests
- FR-IR-2 Inspection request history

### 4.5 Drone Mission Integration
- FR-DM-1 Create inspection missions via SmartDroneHub Mission API
- FR-DM-2 Retrieve mission status, telemetry, inspection images, flight reports

### 4.6 Inspection Report Management
- FR-RM-1 Create reports, upload evidence, record findings
- FR-RM-2 Approve and archive reports

### 4.7 Defect Management
- FR-DF-1 Record and classify defects, assign severity
- FR-DF-2 Track defect lifecycle, attach photo evidence

### 4.8 Maintenance Ticket Management
- FR-MT-1 Create and assign maintenance tickets
- FR-MT-2 Update repair progress, close tickets, maintain history

### 4.9 AI Services Integration
- FR-AI-1 Inspection image analysis (DroneVisionAI)
- FR-AI-2 Inspection report summarization (LLM)
- FR-AI-3 Historical case recommendation (DroneKnowledgeAI)

### 4.10 Dashboard & Analytics
- FR-DA-1 Inspection statistics, defect analytics, maintenance KPIs
- FR-DA-2 Asset utilization, inspection KPIs, operational reports

---

## 5. Non-Functional Requirements

| NFR | Detail |
|-----|--------|
| Web | Responsive Web Application (ReactJS + Material UI) |
| Mobile | Cross-platform Mobile Application (Flutter) |
| API | RESTful API architecture |
| Auth | JWT authentication |
| Access | Role-Based Access Control (RBAC) |
| Integration | SmartDroneHub via standardized REST APIs |
| Database | PostgreSQL |
| Storage | MinIO object storage for evidence and inspection images |
| Deployment | Docker containerization, cloud-ready |
| Real-time | SignalR for mission status updates |
| Security | Audit logging, secure file storage |
| Scale | Scalable, high-availability architecture |

---

## 6. Technology Stack

| Layer | Technology |
|-------|-----------|
| Backend | ASP.NET Core Web API, Entity Framework Core, SignalR |
| Frontend | ReactJS, Material UI |
| Mobile | Flutter |
| Database | PostgreSQL |
| Storage | MinIO |
| AI | DroneVisionAI, DroneKnowledgeAI, LLM-based summarization |
| Deployment | Docker, Docker Compose, Cloud |

---

## 7. Team Assignment

| Member | Work Package | Scope |
|--------|--------------|-------|
| Trần Hoàng Trung Hiếu (Leader, SE184212) | WP1 | Requirement analysis, architecture, DB design, API spec, UI/UX; project foundation (auth, RBAC, audit log); Dashboard & Analytics; coordination & code review |
| Phùng Trung Quốc (SE170027) | WP2 | Asset Management module; Inspection Planning & Request Management; scheduling + notification services |
| Trương Thái Như (SE180082) | WP3 | SmartDroneHub integration (Mission API, telemetry, SignalR); Inspection Report, Defect, Maintenance Ticket modules |
| Trần Tùng Bách (SE180220) | WP4 | Flutter mobile app (Inspector + Maintenance Engineer flows); Evidence management (MinIO); AI services (DroneVisionAI, Report Summarization, DroneKnowledgeAI) |
| All | WP5 | Integration/performance/security testing; Docker deployment; software documentation + deployment guide |

### Timeline (15 weeks)

| Weeks | Milestone |
|-------|-----------|
| 1–3 | WP1 complete: requirements frozen, DB schema, API spec, UI mockups |
| 4–12 | WP2–WP4 in parallel (backend modules, frontend portal, mobile app, AI services) |
| 8 | Mid-term demo: core flows MF1, MF2 end-to-end |
| 12 | Feature freeze: all main flows demoable |
| 12–15 | WP5: testing, Docker deployment, documentation, final defense |

---

## 8. Deliverables

- SmartDroneInspection Web Portal (ReactJS + Material UI)
- Flutter Mobile Application (Inspector + Maintenance)
- Asset Management Module
- Inspection Planning Module
- Inspection Request Module
- Drone Mission Integration Module (SmartDroneHub API)
- Inspection Report Module
- Defect Management Module
- Maintenance Ticket Module
- AI Services: Image Analysis, Report Summarization, Case Recommendation
- Dashboard & Analytics
- RESTful APIs
- Docker Deployment Package
- Software Documentation
