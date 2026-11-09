---
title: "SEP490 Review 2 - BM02 SRS/SDD Self-Review Report"
document_type: review2-bm02
version: "3.0"
date: "2026-11-09"
project_code: "GFA26SE139"
group_name: "FA26SE112"
---

# SEP490 – SRS/SDD Self-Review Report (BM02)

## 1. Run Information

| Field | Value |
| --- | --- |
| **Project code** | `GFA26SE139` |
| **Project name** | SmartDroneInspection: AI-powered Infrastructure Inspection Management Platform |
| **Group / Team members** | `FA26SE112` — Trần Hoàng Trung Hiếu (`SE184212`), Phùng Trung Quốc (`SE170027`), Trương Thái Như (`SE180082`), Trần Tùng Bách (`SE180220`) |
| **Supervisor(s)** | Phạm Minh Trí; Đặng Ngọc Minh Đức |
| **AI tool & model used** | Claude Code — Claude Sonnet 5.5 |
| **Date of run** | `04/11/2026` |
| **Repository commit / tag checked** | tag: `review-2` |
| **Registration form version checked against** | `v2.0` (Review 2 Registration Form) |
| **Document version** | `3.0` |
| **Submission date** | `09/11/2026` |

---

## 2. Standard Prompt

```text
You are reviewing the SRS and SDD of a software capstone project against its registration form and source code. Report only; do not change any file.
Inputs: the registration form, SRS, SDD (with diagrams), source code and database script in this repository.
Check:
1. Scope: FRs in the SRS not covered by the registration form, and registration items with no FR.
2. Requirements: FRs without an actor or testable acceptance criteria; NFRs without metric, threshold and measurement method.
3. Data: entities missing from the Logical ERD; ERD entities or attributes missing from the database script, and tables not in the ERD.
4. States: for each main entity, states used in code but missing from its state machine; transitions with no triggering FR; states with no exit.
5. Flows: main business flows in activity diagrams with no implementation or no test.
6. Architecture: components or third-party services in code but not in the architecture diagram, and the reverse.
7. Design vs code: modules, APIs or business rules implemented differently from the SDD.
Output one table: ID | Category | Location | Finding | Severity (High/Medium/Low) | Evidence. Then list the 5 most important findings.
If something cannot be verified from the repository, say so; do not guess.
```

---

## 3. Findings and Team Response

| ID | Category | Location | Finding | Severity | Evidence | Team response (Fixed / Kept / Planned) |
| :---: | --- | --- | --- | :---: | --- | --- |
| `SR-01` | Scope | Registration §3.2; SRS §3 | Maintenance Work Order module adds extra complexity outside core drone inspection. | High | SRS §§3.8–3.9 vs. 4-workflow scope | **Fixed** – Removed Maintenance module from scope. |
| `SR-02` | Requirements | SRS §3; SDD §2.2 | SDD state transitions use legacy FR IDs instead of `F-01`..`F-08`. | High | SDD §2.2 state tables | **Planned** – Trần Hoàng Trung Hiếu, due `12/11/2026`. |
| `SR-03` | Flows | Report 5 Test Suite | 5 of 65 test cases (staging walkthroughs) are still Pending. | High | `WF1-010`, `WF2-015`, `WF3-012`, `WF3-017`, `WF4-011` | **Planned** – Trần Tùng Bách, due `15/11/2026`. |
| `SR-04` | Scope | SRS §3.6 | SRS adds Flight Permit gate, Pre/Post-flight checklists, and Building Items check. | Medium | `FieldSessionPage` & SRS §3.6 | **Kept** – Required for flight safety and field coverage. |
| `SR-05` | Architecture | Registration §3.2.b; SRS §3.7 | Registration uses `DroneVisionAI` while SRS/code also name `YOLO11`. | Medium | `YoloInferenceClient.java` & SRS §3.7 | **Kept** – `DroneVisionAI` is the module; `YOLO11` is the model. |
| `SR-06` | States | `Inspection.java`; SDD §2.2 | State transition preconditions are enforced in service layer rather than entity setter. | Medium | `InspectionWorkflowService.java` | **Fixed** – Verified by service state-transition tests. |
| `SR-07` | Flows | SDD §3.5.3 Activity Diagram | Activity diagram omitted the `ABORTED` session reschedule branch. | Low | SDD §3.5.3 vs. `/abort` API | **Fixed** – Added `ABORTED` → Reschedule branch to diagram. |
| `SR-08` | Requirements | SRS §4.2 NFR prose | General availability prose lacked a test method, unlike table `NFR-01`..`NFR-05`. | Low | SRS §4.2 | **Fixed** – Standardized on `NFR-01`..`NFR-05` table. |

---

## 4. Top 5 Findings (as reported by the AI)

| # | Finding ID | Summary |
| :---: | :---: | --- |
| 1 | `SR-01` | Remove Maintenance module to focus 100% on the 4 Drone Inspection workflows (`WF-01`..`WF-04`). |
| 2 | `SR-02` | Align SDD §2.2 state transition IDs with SRS feature IDs (`F-01`..`F-08`). |
| 3 | `SR-03` | Complete the remaining 5 staging walkthrough test cases before Defense 1.1. |
| 4 | `SR-04` | Keep Flight Permit gate, Pre/Post-flight checklists, and Building Items check in `WF-03`. |
| 5 | `SR-05` | Clarify `DroneVisionAI` (subsystem) vs. `YOLO11` (model) naming across docs. |

---

## 5. Summary

| Severity | Total | Fixed | Kept | Planned |
| --- | :---: | :---: | :---: | :---: |
| **High** | 3 | 1 | 0 | 2 |
| **Medium** | 3 | 1 | 2 | 0 |
| **Low** | 2 | 2 | 0 | 0 |
