---
title: "SEP490 Review 2 - BM01 Design Brief"
document_type: review2-bm01
version: "3.0"
date: "2026-11-09"
project_code: "GFA26SE139"
group_name: "FA26SE112"
---

# SEP490 – Review 2 Design Brief (BM01)

## 0. Header

| Field | Value |
| --- | --- |
| **Project code** | `GFA26SE139` |
| **Project name** | SmartDroneInspection: AI-powered Infrastructure Inspection Management Platform |
| **Group / Team members** | `FA26SE112` — Trần Hoàng Trung Hiếu (`SE184212`), Phùng Trung Quốc (`SE170027`), Trương Thái Như (`SE180082`), Trần Tùng Bách (`SE180220`) |
| **Supervisor(s)** | Phạm Minh Trí; Đặng Ngọc Minh Đức |
| **Repository URL & branch / tag for Review 2** | `https://github.com/tungbach12/SmartDroneInspection-backend` (tag: `review-2`) |
| **Document version** | `3.0` |
| **Submission date** | `09/11/2026` |

---

## 1. Scope

### 1.1 Registration Changes (Summary of BM03)

| Section | Current | Proposed | Reason |
| --- | --- | --- | --- |
| `§3.2.b` Actors | 5 actors (`Admin`, `Manager`, `Inspector`, `Maintenance Engineer`, `Viewer`). | 4 roles: `Admin`, `Manager`, `Customer`, `Inspector`. | Replaces passive `Viewer` with `Customer` and drops `Maintenance Engineer`. |
| `§3.2.b/c` Maintenance | Includes Maintenance Ticket / Work Order module. | Removed from scope; focuses on 4 drone inspection workflows. | Avoids construction ERP complexity to focus on drone inspection. |
| `§3.2.c` Service & Payment Flow | Basic request creation without quote or payment. | Adds Quotation, Contract, Report acceptance & online payment. | Completes the end-to-end inspection service workflow. |
| `§3.2.d/e` Tech Stack | ASP.NET Core, EF Core, SignalR, PostgreSQL. | Java 21, Spring Boot 4.1, Spring Modulith, PostgreSQL 17, MinIO. | Matches team expertise and modular monolith design. |

### 1.2 Out of Scope

| Item | Reason |
| --- | --- |
| Direct drone piloting & flight control | Handled externally by SmartDroneHub and the field pilot. |
| Corrective Maintenance & Work Orders | Repairs are handled externally by the Customer after receiving the report. |
| Government flight-permit issuance | Granted offline by authorities; platform only verifies uploaded permit files. |
| Unreviewed AI defect publishing | AI detections are advisory; Inspector and Manager review is mandatory. |

---

## 2. System at a Glance

SmartDroneInspection is a centralized platform connecting Customers with Partner Drone Inspectors to inspect infrastructure assets (bridges, buildings, power towers) safely and consistently.

Customers register assets, accept quotes, and complete online payment. Inspectors register drones, execute checklist-gated flights with SmartDroneHub telemetry, confirm `DroneVisionAI` (`YOLO11`) defects, and submit reports for Manager publication (Report 4 SDD §1.1).

---

## 3. Key Design Decisions

| ID | Decision | Options considered | Chosen option and rationale | Owner | Related FR / diagram |
| :---: | --- | --- | --- | --- | --- |
| `D1` | Backend architecture | Microservices vs. Modular monolith | Spring Modulith monolith: clear module boundaries and simple deployment. | Trần Hoàng Trung Hiếu | `F-01`, `F-02` / SDD §1.2 |
| `D2` | Flight integration | Built-in flight control vs. SmartDroneHub API | Consume SmartDroneHub telemetry/logs to isolate flight safety from business logic. | Phùng Trung Quốc | `F-04`, `F-05` / SDD §3.5 |
| `D3` | Field workflow | Single form vs. Step-by-step gated flow | 7-step gated flow (`Permit` → `Pre-flight` → `Flight` → `Post-flight & Items` → `Evidence` → `Findings` → `Report`). | Trần Tùng Bách | `F-05`, `F-06` / SDD §3.6 |
| `D4` | Media storage | DB BLOBs vs. Object storage | MinIO stores photos, MP4 videos, and PDFs; PostgreSQL stores metadata and hashes. | Trần Tùng Bách | `F-02`, `F-06` / SDD §2.2 |
| `D5` | AI & Report review | Auto-publish vs. Human review | Inspector confirms AI findings baseline; independent Manager approves and publishes PDF. | Trương Thái Như | `F-07`, `F-08` / SDD §3.7 |

---

## 4. Top Risks

| ID | Risk | Impact | How we verify or mitigate | Owner |
| :---: | --- | --- | --- | --- |
| `R1` | External service outage (SmartDroneHub, AI, Payment Gateway) | Blocks telemetry sync, defect detection, or payment webhook. | Use 5 s timeouts, manual finding fallback, and idempotent webhook retry. | Trần Tùng Bách |
| `R2` | Cross-role data leak or self-approval | Customer sees internal fees or Inspector approves own report. | Enforce backend role/org guards and block author self-publication (`BR-09`). | Trần Hoàng Trung Hiếu |
| `R3` | Incomplete field check or weather abort | Missing building items or aborted flight delays inspection. | Require reason for unchecked items and support Manager reschedule on abort. | Phùng Trung Quốc |

---

## 5. Known Gaps

| ID | Gap | Location | Plan | Owner | Due |
| :---: | --- | --- | --- | --- | --- |
| `G1` | Legacy Maintenance references in early docs | SRS §3, SDD §2–3 | Remove Maintenance from SRS/SDD to match 4-workflow scope. | Trương Thái Như | `12/11/2026` |
| `G2` | SDD state transition IDs not mapped to `F-01`..`F-08` | Report 4 SDD §2.2 | Update transition labels to match `F-01`..`F-08` and `BR-01`..`BR-10`. | Trần Hoàng Trung Hiếu | `12/11/2026` |
| `G3` | 5 staging walkthrough test cases still Pending | Report 5 Test Report | Run remaining 5 staging walkthroughs before Defense 1.1. | Trần Tùng Bách | `15/11/2026` |

---

## 6. Proposed Mandatory Features

| ID | Feature | Actor | Acceptance criteria (testable) | Test | Status |
| :---: | --- | --- | --- | --- | --- |
| `F-01` | Auth, 4-Role RBAC & Partner Profiles | Admin, Manager, Customer, Inspector | JWT/OAuth2 login works by role; 5 failed logins lock for 15 min; unauthorized access returns 403. | `WF1-001..005` | Done |
| `F-02` | Drone Registration & Safety Review | Inspector, Manager | Requires valid legal documents & unique serial; Manager approves or rejects with reason. | `WF1-006..016` | Done |
| `F-03` | Asset Airspace Gate & Inspection Items | Customer, Manager | Blocks assets in `NO_FLY_ZONE` (403); saves valid GPS asset and target `Inspection Items`. | `WF1-017..021` | Done |
| `F-04` | Service Request, Quote, Contract & Dispatch | Customer, Manager | Customer accepts quote; Manager uploads signed contract and dispatches conflict-free Inspector & Drone. | `WF2-001..009` | Done |
| `F-05` | Permit Gate, Checklists & Field Session | Inspector, Manager | Requires Permit & Pre-flight check to start; records MAVLink log, Building Items & Post-flight check on complete. | `WF2-010..020` | Done |
| `F-06` | Evidence Upload & AI Defect Confirmation | Inspector, DroneVisionAI | Photo/MP4 upload triggers `YOLO11` candidates; Inspector confirms/rejects findings and locks baseline. | `WF3-001..010` | Done |
| `F-07` | Auto-Compiled Report & Manager Review | Inspector, Manager | Compiles draft report with AI summary; independent Manager publishes immutable PDF or returns with reason. | `WF4-001..008` | Done |
| `F-08` | Customer Acceptance & Payment Settlement | Customer, Manager, Inspector | Customer accepts published report and completes online payment; system marks `PAID` and calculates net payout. | `WF3-011..017`, `WF4-009..016` | In progress |

---

## 7. Non-Functional Requirements

| ID | Quality attribute | Metric | Threshold | Measurement method |
| :---: | --- | --- | --- | --- |
| `NFR-01` | Performance | p95 API response time | ≤ 2.0 s at 50 concurrent users | Load test on staging API endpoints (`WF2-016`). |
| `NFR-02` | AI Latency | `YOLO11` detection & LLM summary time | ≤ 5.0 s per request | Timed integration test with sample drone images (`WF3-007`). |
| `NFR-03` | Authorization | Unauthorized cross-role/org requests blocked | 100% blocked (HTTP 401/403) | Automated RBAC negative test suite (`WF1-005`). |
| `NFR-04` | Auth Security | Brute-force login lockout & rate limit | 15 min lock after 5 fails; ≤ 10 req/min | Automated login security test (`WF1-004`). |
| `NFR-05` | Integrity | Published report PDF & contract immutability | 100% SHA-256 match; 0 edits after publish | Automated hash & mutation-rejection test (`WF3-016`). |

---

## 8. Ownership Map

| Member | Role | Owned parts (2–3) | Main workflow owned | Key decisions / PRs |
| --- | --- | --- | --- | --- |
| Trần Hoàng Trung Hiếu (`SE184212`) | Leader | `F-01` (Auth/RBAC), `F-02` (Drone Registration & Review) | `WF-01` — Partner Drone Registration & Review | `D1`, `R2` / PR #84, #88 |
| Phùng Trung Quốc (`SE170027`) | Member | `F-03` (Asset & Items), `F-04` (Quote & Dispatch) | `WF-02` — Quotation, Contract & Dispatch | `D2`, `R3` / PR #82, #83 |
| Trần Tùng Bách (`SE180220`) | Member | `F-05` (Permit, Checklists & Flight), `F-06` (Evidence & AI) | `WF-03` — Field Inspection & AI Defect Check | `D3`, `D4`, `R1` / PR #85, #89 |
| Trương Thái Như (`SE180082`) | Member | `F-07` (Report & Review), `F-08` (Acceptance & Payment) | `WF-04` — Report Review & Payment Settlement | `D5` / PR #86, #87 |
