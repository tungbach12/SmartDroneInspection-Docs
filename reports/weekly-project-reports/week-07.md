# Project Report — Week 7

**Project name:** SmartDroneInspection: AI-powered Infrastructure Inspection Management Platform  
**Group:** FA26SE112  
**Reporting period:** 19–25 October 2026  
**Team members:** Trần Hoàng Trung Hiếu, Phùng Trung Quốc, Trần Tùng Bách, Trương Thái Như

> Week 7 delivered the Additional Session loop (MF2-MF3), Reviewer workspace redesign, PayPal subscription payment integration, YOLO11 MBDD2025 model retraining, and Report 4 Word exporter for Review 2.

## I. Status Report

| # | Project Task | In-charge | Status | Notes (Work Item in Details) |
|---:|---|---|---|---|
| 1 | Frontend MF1: Implement assigned asset-drone pair column, status filter, and schedule conflict alert | Trần Hoàng Trung Hiếu | Completed | Delivered frontend PR #50: added pair status column, status filters, and real-time conflict alert banner. |
| 2 | Backend MF1: Complete Org Admin resource management endpoints and integration tests | Trần Hoàng Trung Hiếu | Completed | Delivered backend PR #76: comprehensive tests for asset, drone, credential, and compliance endpoints. |
| 3 | Docs / Report 5: Record MF1-08 to MF1-14 asset pairing and inspection dispatch verification | Trần Hoàng Trung Hiếu | Completed | Updated Report 5: verified asset-drone pairing, schedule conflict detection, and inspector dispatch (v4.15). |
| 4 | Docs / Report 5: Record MF2 field session, MF4 work order, and FE-01 platform account verification | Trần Hoàng Trung Hiếu | Completed | Updated Report 5: verified field session outcomes, maintenance work order transitions, and platform accounts (v4.16). |
| 5 | Mobile & Frontend MF2: Refine mobile preparation checklist UI and field session completion UX | Phùng Trung Quốc | Completed | Polished Flutter preparation UI, handled session abort/completion scenarios, and verified offline session caching. |
| 6 | Backend & Docs MF2: Reconcile additional-session handoff semantics with preparation draft lifecycle | Phùng Trung Quốc | Completed | Aligned MF2 readiness review with superseding preparations and ensured invalidated prior decisions append audit records. |
| 7 | Report 4 Section 1 & 2: Review and verify component interactions between MF2 preparation and MF1 registries | Phùng Trung Quốc | Completed | Checked component interaction diagrams and reconciled database schema descriptions with latest Flyway migrations. |
| 8 | Report 5 Section 3: Execute integration test pass for MF2 readiness decision invalidation | Phùng Trung Quốc | Completed | Verified that expiration of flight permits or pilot credentials automatically invalidates prior readiness approvals. |
| 9 | Backend MF2/MF3: Implement Additional Session loop and merge findings into unified table with tombstones | Trần Tùng Bách | Completed | Delivered PR #77: `requestAdditionalSession`, readiness invalidation, migration V37 (unified `findings` table with restore). |
| 10 | Frontend MF3: Redesign Reviewer workspace around decision phases (Readiness, Report Review, Corrective) | Trần Tùng Bách | Completed | Delivered PR #51: created dedicated review tabs, pendingAction server computation, and findings review page. |
| 11 | AI / Model Retraining: Clean Kaggle YOLO11 retraining pipeline on MBDD2025 UAV defect dataset | Trần Tùng Bách | In Progress | Fixed out-of-bounds XML boxes, bypassed Ray Tune callback issue, and launched GPU T4 training on Kaggle. |
| 12 | Docs & Reports (Review 2 Package): Integrate PayPal subscription payment into Reports 1–4 and build SDD Word exporter | Trần Tùng Bách | Completed | Integrated PayPal billing, documented `payment_transactions`, aligned 41-table ERD, and built docx exporter with diagrams. |
| 13 | Backend MF4: Finalize maintenance ticket closeout validation and handoff to billing/client notification | Trương Thái Như | Completed | Completed maintenance lifecycle validation: verified work order completion triggers client sign-off and report closure. |
| 14 | Report 4 Section 2 & 3: Verify the 41-table ERD maintenance tables and draft detailed data dictionary | Trương Thái Như | Completed | Verified maintenance tables (`maintenance_tickets`, `work_orders`, `cost_lines`) and documented field constraints. |
| 15 | Report 5 Section 3: Finalize test execution statistics and pass/fail metrics for FE-07 and FE-08 | Trương Thái Như | Completed | Updated test summary matrices for maintenance ticket creation, estimate review, and defect rectification. |
| 16 | Review 2 Preparation: Cross-check maintenance use cases in Report 3 with software design in Report 4 | Trương Thái Như | Completed | Audited consistency between SRS maintenance requirements and SDD class/sequence diagrams. |

## II. Project Issues

| # | Project Issue | Owner | Status | Notes (Solution, Suggestion, etc.) |
|---:|---|---|---|---|
| 1 | Kaggle YOLO training kernel encountered out-of-bounds XML coordinates and Ray Tune callback conflict | Trần Tùng Bách | Resolved | Auto-clipped coordinates to image dimensions, uninstalled conflicting ray package, and resumed training. |
| 2 | Report 3 and Report 4 ERD needed exact reconciliation with all 41 Flyway-managed PostgreSQL tables | Trần Tùng Bách & Trương Thái Như | Resolved | Reconciled all 41 tables including `payment_transactions` for Review 2 compliance. |

## III. Next Week Plan

| # | Project Work Item | In-charge | Deadline | Notes (Task Details, etc.) |
|---:|---|---|---|---|
| 1 | Finalize Milestone Review 2 presentation and deliverable document exports (Word & PDF) | All Members | 28 Oct 2026 | Export Reports 1–5 using the automated document generator tools. |
| 2 | Conduct end-to-end rehearsal across web, mobile, and AI inference services | All Members | 29 Oct 2026 | Walk through asset registration, request triage, mobile field session, defect review, and maintenance. |
| 3 | Evaluate candidate YOLO11 defect detector on real inspection evidence and hold-out test set | Trần Tùng Bách | 30 Oct 2026 | Compare retrained candidate metrics against deployed baseline. |

## IV. Other Project Matters/Suggestions

| # | Project Matter/Suggestions | Raised By | Date | Notes |
|---:|---|---|---|---|
| 1 | All four workflows (WF1–WF4) and platform subscription billing are fully implemented and tested | Trần Tùng Bách | 25 Oct 2026 | The project is fully prepared for Milestone Review 2 with comprehensive test evidence. |
