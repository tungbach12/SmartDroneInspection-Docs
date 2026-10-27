---
title: "Report 3 - Non-Functional Requirements"
document_type: report3-srs-section
weight: 45
source: "report3-software-requirement-specification.docx"
---

## 4. Non-Functional Requirements

### 4.1 External Interfaces

- **Web Portal Interface**: Responsive web application accessible on modern desktop and tablet browsers (Google Chrome, Microsoft Edge, Mozilla Firefox, Apple Safari) over secure HTTPS connections, supporting both Light and Dark themes and English/Vietnamese languages.
- **Mobile Application Interface**: Cross-platform mobile application (Android and iOS) designed for field Inspectors and Maintenance Engineers to check airspace warnings, upload flight permits, log flight sessions, upload photos, and record repair work logs on site.
- **AI Defect Detection & Advisory Services**: Internal service interfaces that analyze inspection photographs (`YOLO11`) to suggest defect bounding boxes and assist users in drafting inspection reports and standard-based maintenance repair scopes.
- **Online Payment & Mapping Interfaces**: Optional integration with PayPal for online subscription and drone lease checkout (alongside standard bank transfer confirmation), and integration with OpenStreetMap layers for displaying infrastructure assets and Vietnam restricted airspace zones.

### 4.2 Quality Attributes

#### 4.2.1 Usability

- **Step-by-Step Workflow Guidance**: Screens guide users clearly through each stage of the workflow (Schedule -> Flight Permit -> Field Session -> Evidence -> Findings -> Report -> Maintenance) with clear status badges and validation hints.
- **Field-Ready Mobile Design**: The mobile interface uses high-contrast text and clear action buttons suitable for outdoor field use.
- **Clear AI Labeling**: AI-suggested defects and AI-drafted text are clearly badged as `Pending` or `Draft` so users can easily distinguish automated suggestions from human-verified records.
- **Bilingual Support**: Users can switch between English (`EN`) and Vietnamese (`VI`) at any time without losing entered data.

#### 4.2.2 Reliability

- **Service Availability**: Target system availability is at least `99.5%` during standard operating hours (`06:00–22:00 ICT`).
- **Recovery & Backup**: Automated daily database backups allow the system to recover within `30 minutes` (`MTTR <= 30 minutes`) in the event of a server failure.
- **Manual Fallback When AI or Payment Services Are Offline**: If the AI detection service, AI report drafting service, or online payment gateway is temporarily unavailable, users can still record manual findings, write manual reports, use built-in repair templates, and confirm bank transfer payments without interruption.
- **Accurate Financial & Document Records**: All subscription, lease, estimate, and actual repair costs are calculated to two decimal places without rounding drift, and published PDF reports are locked against modification.

#### 4.2.3 Performance

- **Screen & Action Response Time**: At least `95%` of standard user actions, searches, and list loads complete within `2.0 seconds` under normal concurrent usage (`50` active users).
- **AI Defect Detection Time**: Single-image AI defect analysis completes within `5.0 seconds` for standard inspection photographs up to `10 MB`.
- **Paginated Lists**: Large tables (assets, inspections, photos, findings, reports, work orders, notifications) load in pages so screens remain fast as data grows.

#### 4.2.4 Security and Maintainability

- **Strict Organization Isolation**: Every customer organization can view and modify only its own workforce, assets, drones, inspections, reports, and maintenance work orders.
- **Role-Based Permissions & Separation of Duties**: Each screen and action is restricted to authorized roles. Authors and executing team members cannot approve or accept their own inspection reports, cost estimates, or maintenance work.
- **Account & Session Protection**: Passwords are stored in encrypted form, accounts are temporarily locked for `15 minutes` after `5` consecutive failed sign-in attempts, and sessions are automatically invalidated when a user's password, role, or account status changes.
- **Audit Trail**: Important actions — including registration, user creation, payment confirmation, flight readiness, report publication, budget approval, and work order closure — are recorded in an uneditable audit history.

**Summary of Quantified Non-Functional Requirements (`NFR-01` to `NFR-06`)**

| NFR ID | Category | Requirement Statement | Metric | Target Threshold | Verification Method |
| :---: | --- | --- | --- | --- | --- |
| `NFR-01` | Performance (System Response) | Standard list views, searches, and workflow actions must respond quickly under multi-user load. | 95th percentile (`p95`) response time and error rate. | `p95 <= 2.0 seconds` and `0%` server errors under `50` concurrent users. | Automated concurrent load test on the staging environment (`WF2-016`). |
| `NFR-02` | Performance (AI Detection) | On-demand `YOLO11` defect detection on a single inspection photograph must complete within interactive limits. | Processing time per image (up to `10 MB` JPEG/PNG). | `<= 5.0 seconds` per image (with automatic fallback or manual entry if offline). | Automated AI inference timing test (`WF3-007`). |
| `NFR-03` | Security (Multi-Tenant & Role Isolation) | Users must be blocked from accessing screens or records belonging to another organization or an unauthorized role. | Rejection rate for unauthorized role or cross-organization requests. | `100%` of unauthorized or cross-organization requests blocked (`0` data leaks). | Automated role-matrix and cross-organization security test suite (`WF1-005`). |
| `NFR-04` | Security (Sign-In Protection) | Sign-in screens must block brute-force password guessing and expired sessions. | Failed sign-in lockout threshold and rate limit per network address. | Account locks for `15 minutes` after `5` failed attempts; `> 10` sign-in requests per minute blocked. | Automated authentication and rate-limit security test (`WF1-004`). |
| `NFR-05` | Reliability (Document & PDF Integrity) | Uploaded asset documents and published PDF reports must remain intact and uneditable after publication. | File integrity match rate and post-publish edit rejection rate. | `100%` file integrity verification; `100%` of edits to published reports blocked. | Automated PDF publication and file integrity test (`WF3-016`). |
| `NFR-06` | Maintainability (Automated Testing) | Core business rules and workflows must be continuously verified by automated tests. | Automated unit/integration coverage and functional test automation rate. | `>= 80%` backend test coverage and `>= 50%` of functional test cases automated. | Continuous integration test pipeline execution (`WF4-005`). |
