---
title: "SWP490 Review 2 - BM01 Appendix A & BM04 Review 2 Commitment"
document_type: review2-appendix-a-bm04
version: "3.0"
date: "2026-11-09"
project_code: "GFA26SE139"
group_name: "FA26SE112"
---

# SWP490 – BM01 Appendix A & Review 2 Commitment (BM04)

## 1. Project Information

| Field | Value |
| --- | --- |
| **Project code** | `GFA26SE139` |
| **Project name** | SmartDroneInspection: AI-powered Infrastructure Inspection Management Platform |
| **Group / Team members** | `FA26SE112` — Trần Hoàng Trung Hiếu (`SE184212`), Phùng Trung Quốc (`SE170027`), Trương Thái Như (`SE180082`), Trần Tùng Bách (`SE180220`) |
| **Supervisor(s)** | Phạm Minh Trí; Đặng Ngọc Minh Đức |
| **Review 2 date** | `09/11/2026` |
| **Document version** | `3.0` |

---

## 2. Main Workflows (`WF-01` – `WF-04`, No Maintenance)

| ID | Workflow | Actors | Trigger | Business outcome | Features | Entity states | Owner |
| :---: | --- | --- | --- | --- | :---: | --- | --- |
| **`WF-01`** | Partner Drone Registration & Review | Inspector, Manager, System | Inspector submits drone with 3 legal docs. | Drone is verified and activated for dispatch. | `F-01`, `F-02` | `DroneRegistration`: `PENDING → APPROVED / REJECTED`; `Drone`: `→ ACTIVE` | Trần Hoàng Trung Hiếu |
| **`WF-02`** | Quotation, Contract & Dispatch | Customer, Manager, Inspector | Customer registers asset and submits request. | Quote accepted, contract uploaded, mission scheduled. | `F-03`, `F-04` | `ServiceRequest`: `SUBMITTED → QUOTED → QUOTE_ACCEPTED → DISPATCHED`; `Inspection`: `→ SCHEDULED` | Phùng Trung Quốc |
| **`WF-03`** | Field Inspection & AI Defect Check | Inspector, Manager, DroneVisionAI | Inspector uploads permit and starts session. | Checklists, building items, evidence & AI findings locked. | `F-05`, `F-06` | `Inspection`: `SCHEDULED → IN_PROGRESS → FIELD_COMPLETED`; `Finding`: `CANDIDATE → CONFIRMED` | Trần Tùng Bách |
| **`WF-04`** | Report Review & Payment Settlement | Inspector, Manager, Customer, PayOS | Field inspection reaches `FIELD_COMPLETED`. | Report published, accepted, paid via PayOS, and settled. | `F-07`, `F-08` | `Report`: `DRAFT → SUBMITTED → PUBLISHED`; `Invoice`: `UNPAID → PAID`; `Payout`: `→ SETTLED` | Trương Thái Như |

---

## 3. Demo Scenarios (`DS-01a` – `DS-04b`)

| ID | Workflow | Type | Preconditions and data | Main steps | Expected result | Presenter |
| :---: | :---: | :---: | --- | --- | --- | --- |
| **`DS-01a`** | `WF-01` | Main | Active Inspector; 3 valid drone PDFs. | 1. Submit drone & 3 docs.<br>2. Manager approves. | Status → `APPROVED`; Drone is `ACTIVE`. | Trần Hoàng Trung Hiếu |
| **`DS-01b`** | `WF-01` | Exception | Duplicate serial; reject without reason. | 1. Submit duplicate serial.<br>2. Reject with empty reason. | Blocked with `400/409` (`BR-01`, `BR-02`). | Trần Hoàng Trung Hiếu |
| **`DS-02a`** | `WF-02` | Main | Customer in `CLEAR_ZONE`; free Inspector+Drone. | 1. Create asset & request.<br>2. Accept quote.<br>3. Upload contract & dispatch. | Request → `DISPATCHED`; Inspection → `SCHEDULED`. | Phùng Trung Quốc |
| **`DS-02b`** | `WF-02` | Exception | Asset in `NO_FLY_ZONE`; busy Inspector. | 1. Create asset in NFZ.<br>2. Dispatch busy Inspector. | Blocked with `403 NFZ` (`BR-03`) & `409 Conflict` (`BR-05`). | Phùng Trung Quốc |
| **`DS-03a`** | `WF-03` | Main | `SCHEDULED` mission; permit & media ready. | 1. Upload permit & pre-flight check → Start.<br>2. Check building items & post-flight.<br>3. Upload media & confirm AI findings. | Findings locked; Inspection → `FIELD_COMPLETED`. | Trần Tùng Bách |
| **`DS-03b`** | `WF-03` | Exception | Missing permit; unchecked item without reason; abort. | 1. Start without permit.<br>2. Complete with missing reason.<br>3. Abort session. | Steps 1–2 blocked; Step 3 sets `ABORTED` for reschedule. | Trần Tùng Bách |
| **`DS-04a`** | `WF-04` | Main | `FIELD_COMPLETED` mission with locked findings. | 1. Submit auto-compiled report.<br>2. Manager publishes PDF.<br>3. Customer accepts & pays via PayOS. | Report → `PUBLISHED`; Invoice → `PAID`; Payout → `SETTLED`. | Trương Thái Như |
| **`DS-04b`** | `WF-04` | Exception | Self-approval; return without reason; early pay. | 1. Author tries to publish.<br>2. Return without reason.<br>3. Pay before publish. | Blocked with `403/400` (`BR-09`, `BR-10`). | Trương Thái Như |

---

## 4. Functional Test Case Target (`65` Total, `56` Automated in CI)

| Source | Count | Minimum per item | Subtotal |
| --- | :---: | :---: | :---: |
| Mandatory features (`F-01`..`F-08`) | 8 | 3 | 42 |
| Main workflows (end-to-end) | 4 | 1 | 4 |
| State transitions of main entities | 14 | 1 | 14 |
| Agreed NFRs (`NFR-01`..`NFR-05`) | 5 | 1 | 5 |
| **Committed total** | **—** | **—** | **65 (56 Automated = 86.15%)** |

---

## 5. Summary and Cross-Check (`BM04` §8)

### 5.1 By Workflow

| Workflow | Owner | Features | Demo scenarios (main / exception) | Test cases | Automated |
| :---: | --- | :---: | :---: | :---: | :---: |
| `WF-01` | Trần Hoàng Trung Hiếu | `F-01`, `F-02` | 2 (1 Main / 1 Exc) | 16 | 14 |
| `WF-02` | Phùng Trung Quốc | `F-03`, `F-04` | 2 (1 Main / 1 Exc) | 16 | 14 |
| `WF-03` | Trần Tùng Bách | `F-05`, `F-06` | 2 (1 Main / 1 Exc) | 17 | 14 |
| `WF-04` | Trương Thái Như | `F-07`, `F-08` | 2 (1 Main / 1 Exc) | 16 | 14 |
| **Total** | **4 Members** | **8 Features** | **8 (4 Main / 4 Exc)** | **65** | **56 (86.15%)** |

### 5.2 By Member

| Member | Workflows owned | Features | Test cases | Automated | Demo scenarios | Review 2 verification |
| --- | :---: | :---: | :---: | :---: | :---: | :---: |
| Trần Hoàng Trung Hiếu | `WF-01` | `F-01`, `F-02` | 16 | 14 | `DS-01a`, `DS-01b` | Pending |
| Phùng Trung Quốc | `WF-02` | `F-03`, `F-04` | 16 | 14 | `DS-02a`, `DS-02b` | Pending |
| Trần Tùng Bách | `WF-03` | `F-05`, `F-06` | 17 | 14 | `DS-03a`, `DS-03b` | Pending |
| Trương Thái Như | `WF-04` | `F-07`, `F-08` | 16 | 14 | `DS-04a`, `DS-04b` | Pending |
| **Total** | **4 Workflows** | **8 Features** | **65** | **56 (86.15%)** | **8 Scenarios** | **—** |

### 5.3 Required Fixes (`BM04` §9)

| ID | Item | Related workflow | Owner | Due |
| :---: | --- | --- | --- | --- |
| `FX-01` | Map SDD §2.2 state-transition IDs to `F-01`..`F-08`. | `WF-01`..`04` | Trần Hoàng Trung Hiếu | `12/11/2026` |
| `FX-02` | Complete staging walkthrough for 3-doc drone approval (`WF1-010`). | `WF-01` | Trần Hoàng Trung Hiếu | `15/11/2026` |
| `FX-03` | Complete staging walkthrough for session abort & reschedule (`WF2-015`). | `WF-02`, `WF-03` | Phùng Trung Quốc | `15/11/2026` |
| `FX-04` | Complete staging walkthroughs for PayOS & Vision fallback (`WF3-012`, `017`). | `WF-03`, `WF-04` | Trần Tùng Bách | `15/11/2026` |
| `FX-05` | Remove legacy Maintenance references from SRS/SDD (`SR-01`). | `WF-04` | Trương Thái Như | `12/11/2026` |
