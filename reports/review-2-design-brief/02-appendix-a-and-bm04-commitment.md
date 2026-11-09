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
| **`WF-01`** | Partner Drone Registration & Review | Inspector, Manager, System | Inspector submits drone with legal documents. | Drone is verified and activated for dispatch. | `F-01`, `F-02` | `DroneRegistration`: `PENDING → APPROVED / REJECTED`; `Drone`: `→ ACTIVE` | Trần Hoàng Trung Hiếu |
| **`WF-02`** | Quotation, Contract & Dispatch | Customer, Manager, Inspector | Customer registers asset and submits request. | Quote accepted, contract uploaded, mission scheduled. | `F-03`, `F-04` | `ServiceRequest`: `SUBMITTED → QUOTED → QUOTE_ACCEPTED → DISPATCHED`; `Inspection`: `→ SCHEDULED` | Phùng Trung Quốc |
| **`WF-03`** | Field Inspection & AI Defect Check | Inspector, Manager, DroneVisionAI | Inspector uploads permit and starts session. | Checklists, building items, evidence & AI findings locked. | `F-05`, `F-06` | `Inspection`: `SCHEDULED → IN_PROGRESS → FIELD_COMPLETED`; `Finding`: `CANDIDATE → CONFIRMED` | Trần Tùng Bách |
| **`WF-04`** | Report Review & Payment Settlement | Inspector, Manager, Customer, PayOS | Field inspection reaches `FIELD_COMPLETED`. | Report published, accepted, paid via PayOS, and settled. | `F-07`, `F-08` | `Report`: `DRAFT → SUBMITTED → PUBLISHED`; `Invoice`: `UNPAID → PAID`; `Payout`: `→ SETTLED` | Trương Thái Như |

---

## 3. Demo Scenarios (`DS-01a` – `DS-04b`)

| ID | Workflow | Type | Preconditions and data | Main steps | Expected result | Presenter |
| :---: | :---: | :---: | --- | --- | --- | --- |
| **`DS-01a`** | `WF-01` | Main | Active Inspector; valid drone legal documents. | 1. Inspector opens Drone Registration form.<br>2. Enter drone specs and serial number.<br>3. Upload legal documents and submit.<br>4. System validates serial & expiry dates (`PENDING`).<br>5. Manager reviews documents against specs.<br>6. Manager approves; drone becomes `ACTIVE`. | Status → `APPROVED`; Drone is `ACTIVE`. | Trần Hoàng Trung Hiếu |
| **`DS-01b`** | `WF-01` | Exception | Duplicate serial; reject without reason. | 1. Submit drone with duplicate serial number.<br>2. System blocks with `409 Conflict` (`BR-01`).<br>3. Submit drone with expired inspection date.<br>4. Manager clicks Reject with empty reason.<br>5. System blocks until reason is entered (`BR-02`). | Blocked with `400/409` (`BR-01`, `BR-02`). | Trần Hoàng Trung Hiếu |
| **`DS-02a`** | `WF-02` | Main | Customer in `CLEAR_ZONE`; free Inspector+Drone. | 1. Customer creates asset with GPS & `Inspection Items`.<br>2. System verifies `CLEAR_ZONE` and activates asset.<br>3. Customer submits Service Request (`SUBMITTED`).<br>4. Manager issues Quotation (`QUOTED`).<br>5. Customer accepts Quotation (`QUOTE_ACCEPTED`).<br>6. Manager uploads contract & dispatches mission. | Request → `DISPATCHED`; Inspection → `SCHEDULED`. | Phùng Trung Quốc |
| **`DS-02b`** | `WF-02` | Exception | Asset in `NO_FLY_ZONE`; busy Inspector. | 1. Customer enters asset GPS inside `NO_FLY_ZONE`.<br>2. System blocks asset creation with `403` (`BR-03`).<br>3. Customer requests revision on Quotation.<br>4. Manager selects busy Inspector for dispatch.<br>5. System blocks dispatch with `409 Conflict` (`BR-05`). | Blocked with `403 NFZ` (`BR-03`) & `409 Conflict` (`BR-05`). | Phùng Trung Quốc |
| **`DS-03a`** | `WF-03` | Main | `SCHEDULED` mission; permit & media ready. | 1. Upload Flight Permit & complete Pre-flight Check.<br>2. Start session (`IN_PROGRESS`) & sync MAVLink log.<br>3. Check off Building `Inspection Items`.<br>4. Complete Post-flight Checklist.<br>5. Upload media; `DroneVisionAI` detects defects.<br>6. Confirm AI findings & lock `Findings Baseline`. | Findings locked; Inspection → `FIELD_COMPLETED`. | Trần Tùng Bách |
| **`DS-03b`** | `WF-03` | Exception | Missing permit; unchecked item without reason; abort. | 1. Click Start without Flight Permit.<br>2. System blocks session start (`BR-06`).<br>3. Leave Building Item unchecked without reason.<br>4. System blocks completion until reason is entered.<br>5. Click Abort session due to weather → `ABORTED`. | Steps 1–4 blocked; Step 5 sets `ABORTED` for reschedule. | Trần Tùng Bách |
| **`DS-04a`** | `WF-04` | Main | `FIELD_COMPLETED` mission with locked findings. | 1. System auto-compiles `DRAFT` report with AI summary.<br>2. Inspector reviews and submits report (`SUBMITTED`).<br>3. Independent Manager reviews report.<br>4. Manager approves & publishes PDF (`PUBLISHED`).<br>5. Customer clicks `Accept Report`.<br>6. Customer pays via PayOS → `PAID` & Payout `SETTLED`. | Report → `PUBLISHED`; Invoice → `PAID`; Payout → `SETTLED`. | Trương Thái Như |
| **`DS-04b`** | `WF-04` | Exception | Self-approval; return without reason; early pay. | 1. Report author attempts to publish own report.<br>2. System blocks with `403 Separation of Duties` (`BR-09`).<br>3. Manager clicks Return without entering reason.<br>4. System blocks return with `400 Bad Request`.<br>5. Customer attempts payment before `PUBLISHED` (blocked). | Blocked with `403/400` (`BR-09`, `BR-10`). | Trương Thái Như |

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
| `FX-02` | Complete staging walkthrough for partner drone approval (`WF1-010`). | `WF-01` | Trần Hoàng Trung Hiếu | `15/11/2026` |
| `FX-03` | Complete staging walkthrough for session abort & reschedule (`WF2-015`). | `WF-02`, `WF-03` | Phùng Trung Quốc | `15/11/2026` |
| `FX-04` | Complete staging walkthroughs for PayOS & Vision fallback (`WF3-012`, `017`). | `WF-03`, `WF-04` | Trần Tùng Bách | `15/11/2026` |
| `FX-05` | Remove legacy Maintenance references from SRS/SDD (`SR-01`). | `WF-04` | Trương Thái Như | `12/11/2026` |
