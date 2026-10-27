# Project Report — Week 6

**Project name:** SmartDroneInspection: AI-powered Infrastructure Inspection Management Platform  
**Group:** FA26SE112  
**Reporting period:** 12–18 October 2026  
**Team members:** Trần Hoàng Trung Hiếu, Phùng Trung Quốc, Trần Tùng Bách, Trương Thái Như

> Week 6 focused on Org Admin resource management UI, CI/CD deploy serialization, finding verification CRUD with audit retirement, YOLO11 advisory detection, and maintenance cost estimation.

## I. Status Report

| # | Project Task | In-charge | Status | Notes (Work Item in Details) |
|---:|---|---|---|---|
| 1 | Frontend MF1: Implement Org Admin workforce route, user management, and credential review UI | Trần Hoàng Trung Hiếu | Completed | Delivered UI for workforce user listing, provisioning, credential verification, and one-time password display. |
| 2 | Frontend MF1: Implement Org Admin drone fleet management UI and flight permit management UI | Trần Hoàng Trung Hiếu | Completed | Built screens for drone inventory, maintenance status tags, permit file uploads, and validity date tracking. |
| 3 | Backend MF1: Expose evidence ownership port in shared package; reconcile shared readiness boundaries | Trần Hoàng Trung Hiếu | Completed | Refactored module boundaries: exposed evidence port and harmonized readiness checks across modules. |
| 4 | Docs / Report 5: Update Report 5 test case verification for frontend resource management (v4.11) | Trần Hoàng Trung Hiếu | Completed | Recorded frontend test execution results for FE-01 and FE-02 in Report 5 and verified route guards. |
| 5 | CI/CD: Implement file-based deployment lock on VPS runner to serialize compose stack mutations | Phùng Trung Quốc | Completed | Delivered CI fix: acquire deploy lock before mutating compose stack or rebuilding web container. |
| 6 | Backend & Frontend MF2: Review and verify PR #70 (Org Admin resource management integration) | Phùng Trung Quốc | Completed | Reviewed and merged backend/frontend resource management PRs ensuring readiness integration. |
| 7 | Report 4 Section 3: Document detailed API endpoint specifications for inspection readiness and field sessions | Phùng Trung Quốc | Completed | Documented HTTP endpoints, request bodies, query filters, and response status codes for MF2. |
| 8 | Report 5 Section 3: Author and execute test cases FE-03 (Request Triage) and FE-04 (Field Session) | Phùng Trung Quốc | Completed | Documented verification steps, assertions, and outcomes for inspection request approval and field visits. |
| 9 | Backend MF3: Implement finding confirmation, rejection, and manual finding CRUD (`FindingService`) | Trần Tùng Bách | Completed | Delivered finding verification service: Inspector confirms/rejects AI candidates and creates manual findings. |
| 10 | Backend MF3: Implement evidence retirement with shared audit reason, author withdrawal, and YOLO11 detection | Trần Tùng Bách | Completed | Added bulk evidence retirement, author report withdrawal, and advisory YOLO11 defect detection client. |
| 11 | Frontend MF3: Add bulk evidence retirement toolbar, register filter tabs, and staged reviewer workspace | Trần Tùng Bách | Completed | Built evidence management UI with bulk retire dialog, filter tabs, and redesigned reviewer workflow stages. |
| 12 | Docs / Report 5: Sync Report 3 SRS, Report 4 database design, and Report 5 test report (v4.11) for MF3 | Trần Tùng Bách | Completed | Documented findings lifecycle, evidence retirement audit rules, and test verification evidence. |
| 13 | Backend MF4: Implement maintenance work order estimation and cost-calculation services | Trương Thái Như | Completed | Delivered service logic: `recordTaskEstimate`, `addCostLine`, and automated total cost computation. |
| 14 | Report 3 Section 3.4 & 4: Review and refine Non-functional Requirements for maintenance tracking | Trương Thái Như | Completed | Specified data retention, audit trail immutability, and attachment storage requirements for maintenance. |
| 15 | Report 4 Section 1 & 3: Draft C4 Component diagram and sequence diagrams for Maintenance module | Trương Thái Như | Completed | Modeled maintenance service components, repository dependencies, and work order approval sequence. |
| 16 | Report 5 Section 3: Author test cases FE-07 (Maintenance Ticket) and FE-08 (Work Order Resolution) | Trương Thái Như | Completed | Documented test scenarios for converting inspection findings to maintenance tickets and verifying completion. |

## II. Project Issues

| # | Project Issue | Owner | Status | Notes (Solution, Suggestion, etc.) |
|---:|---|---|---|---|
| 1 | MinIO test container pull failed intermittently on GitHub Actions runner | Trần Tùng Bách | Resolved | Pointed Testcontainers MinIO container at a pinned, reliable Docker mirror in PR #67. |
| 2 | Finding decisions previously allowed contradictory state transitions | Trần Tùng Bách | Resolved | Strictly gated report generation: only confirmed findings appear in draft reports, unreviewed candidates block publishing. |

## III. Next Week Plan

| # | Project Work Item | In-charge | Deadline | Notes (Task Details, etc.) |
|---:|---|---|---|---|
| 1 | Implement Additional Session loop connecting MF3 evidence decisions with MF2 preparation | Trần Tùng Bách & Phùng Trung Quốc | 25 Oct 2026 | Allow Inspector to flag incomplete coverage and trigger a new field session preparation. |
| 2 | Integrate PayPal online subscription payment into Report 3 and Report 4 for Review 2 | Trần Tùng Bách | 25 Oct 2026 | Document `payment_transactions` table and Enterprise Inspection subscription billing. |
| 3 | Add assigned asset-drone pair column, status filter, and schedule conflict alert | Trần Hoàng Trung Hiếu | 25 Oct 2026 | Enhance Org Admin asset scheduling catalog UI. |
| 4 | Finalize maintenance work order closeout and client acceptance verification | Trương Thái Như | 25 Oct 2026 | Complete maintenance lifecycle verification for Report 5. |

## IV. Other Project Matters/Suggestions

| # | Project Matter/Suggestions | Raised By | Date | Notes |
|---:|---|---|---|---|
| 1 | Preparation for Milestone Review 2: ensure complete traceability from Report 3 to Report 5 | Trần Tùng Bách | 18 Oct 2026 | All functional requirements must trace to physical database tables, API endpoints, and test cases. |
