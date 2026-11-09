---
title: "SEP490 Review 2 - BM03 Record of Changes for Registration Form"
document_type: review2-bm03
version: "3.0"
date: "2026-11-09"
project_code: "GFA26SE139"
group_name: "FA26SE112"
---

# SEP490 – Registration Form Record of Changes (BM03)

## 1. Project Information

| Field | Value |
| --- | --- |
| **Project code** | `GFA26SE139` |
| **Project name** | SmartDroneInspection: AI-powered Infrastructure Inspection Management Platform |
| **Group / Team members** | `FA26SE112` — Trần Hoàng Trung Hiếu (`SE184212`), Phùng Trung Quốc (`SE170027`), Trương Thái Như (`SE180082`), Trần Tùng Bách (`SE180220`) |
| **Supervisor(s)** | Phạm Minh Trí; Đặng Ngọc Minh Đức |
| **Current approved Registration Form version** | `v1.0` (`19/08/2026`) |
| **Proposed Registration Form version** | `v2.0` (`09/11/2026`) |
| **Document version** | `3.0` |
| **Submission date** | `09/11/2026` |

---

## 2. Changes

| No. | Section in Registration Form | Current content | Proposed content | Reason | Proposed by |
| :---: | --- | --- | --- | --- | --- |
| `01` | `§3.2.b` Human Actors | 5 actors: Admin, Manager, Inspector, Maintenance Engineer, Viewer. | 4 actors: Admin, Manager, Customer, Inspector. | Replaces passive Viewer with Customer and drops Maintenance Engineer. | Trần Hoàng Trung Hiếu |
| `02` | `§3.2.b/c/f` Maintenance Scope | Includes Maintenance Ticket / Work Order module. | Removes Maintenance module; focuses on 4 Inspection workflows (`WF-01`..`WF-04`). | Focuses depth on drone inspection and AI defect reporting. | Trương Thái Như |
| `03` | `§3.2.b/c` Service & Payment Flow | Basic request creation without quote or payment. | Adds Quotation, Contract, Report acceptance & online payment. | Completes the end-to-end inspection service workflow. | Phùng Trung Quốc |
| `04` | `§3.2.d/e` Tech Stack | ASP.NET Core, EF Core, SignalR, PostgreSQL. | Java 21, Spring Boot 4.1, Spring Modulith, PostgreSQL 17, MinIO. | Aligns with team expertise and modular monolith architecture. | Trần Hoàng Trung Hiếu |

---

## 3. Decision at Review 2

| No. | Decision (Accepted / Adjusted / Rejected) | Reviewer note |
| :---: | --- | --- |
| `01` | Pending Review 2 | |
| `02` | Pending Review 2 | |
| `03` | Pending Review 2 | |
| `04` | Pending Review 2 | |
