# Project Report — Week 6

**Project name:** SmartDroneInspection: AI-powered Infrastructure Inspection Management Platform  
**Group:** FA26SE112  
**Reporting period:** 12–18 October 2026  
**Personal contribution recorded:** Trương Thái Như (WF4 / FE-07 Owner)  

---

## I. Status Report

| # | Project Task | In-charge | Status | Notes (Work Item in Details) |
|---:|---|---|---|---|
| 1 | Implement Backend Event-Driven Workflows & PDF Rendering | Trương Thái Như | Completed & Verified | Built `ReinspectionRequestedEvent` dispatch for re-inspection without circular module dependencies; implemented `MaintenanceReportRenderer` rendering formal completion reports to PDF with SHA-256 hash stored in MinIO; created `MaintenanceNotificationListener` for milestone in-app notifications. |
| 2 | Build Web Maintenance Management Console | Trương Thái Như | Completed & Tested | Built fully interactive `MaintenancePage.tsx` with MetricCards, server-paged Work Orders table, published Repair Candidates queue, and `WorkOrderDetailPanel.tsx` supporting team assignment, task planning, baseline approval, change orders, work log review, and cost reconciliation. |
| 3 | Build Mobile Field Engineer Tasks Application | Trương Thái Như | Completed & Tested | Implemented Flutter mobile tasks module (`tasks_page.dart`, `work_order_detail_page.dart`, `record_work_log_sheet.dart`) with Riverpod state management, pull-to-refresh (`AsyncValueWidget`), and offline-safe work log recording. |
| 4 | Author Automated Test Suites for WF4 | Trương Thái Như | Completed (25/25 tests passed) | Implemented `MaintenanceApiIntegrationTest.java` with 25 test cases covering tenant scope, separation of duties, duplicate prevention, and cost reconciliation; built `MaintenancePage.test.tsx` and `maintenance_repository_test.dart`. |

---

## II. Project Issues

| # | Project Issue | Owner | Status | Notes (Solution, Suggestion, etc.) |
|---:|---|---|---|---|
| 1 | Manual entry of corrective scope and acceptance criteria is prone to non-standard descriptions | Trương Thái Như | Solution proposed | Researching RAG approach utilizing engineering standards (TCVN, ISO, AASHTO) with `pgvector` to provide automated scope and criteria suggestions. |
| 2 | Separation of duties requires strict enforcement across client and backend | Trương Thái Như | Resolved | Enforced at domain level: executing team cannot accept its own work, and budget approver must remain outside the executing roster. |

---

## III. Next Week Plan

| # | Project Work Item | In-charge | Deadline | Notes (Task Details, etc.) |
|---:|---|---|---|---|
| 1 | Design and implement RAG-assisted maintenance scope advisor | Trương Thái Như | 22 Oct 2026 | Vectorize standard infrastructure repair manuals in `pgvector` and integrate OpenAI-compatible inference with deterministic fallback. |
| 2 | Conduct end-to-end integration audit across Web, Mobile, and Backend | Trương Thái Như | 23 Oct 2026 | Trace full lifecycle from candidate triage to closed work order; eliminate any integration edge cases. |
| 3 | Synchronize project documentation and Report 5 test records | Trương Thái Như | 23 Oct 2026 | Update Report 3 SRS §3.8, Report 5 FE-07, and personal development plans. |
