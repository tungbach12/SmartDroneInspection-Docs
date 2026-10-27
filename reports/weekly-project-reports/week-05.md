# Project Report — Week 5

**Project name:** SmartDroneInspection: AI-powered Infrastructure Inspection Management Platform  
**Group:** FA26SE112  
**Reporting period:** 5–11 October 2026  
**Team members:** Trần Hoàng Trung Hiếu, Phùng Trung Quốc, Trần Tùng Bách, Trương Thái Như

> Week 5 delivered the Enterprise Inspection architecture cutover, full MF1 resource/credential management, MF2 mobile field sessions, MF4 work orders, and MF3 report authoring with landing page.

## I. Status Report

| # | Project Task | In-charge | Status | Notes (Work Item in Details) |
|---:|---|---|---|---|
| 1 | Backend MF1: Implement Drone inventory, compliance inputs, flight permits, and ORG_ADMIN provisioning | Trần Hoàng Trung Hiếu | Completed | Added Drone and FlightPermit entities, tenant compliance inputs, and organization admin user creation. |
| 2 | Backend MF1: Implement workforce credentials, review decisions, 60-day expiry warning, upload caps | Trần Hoàng Trung Hiếu | Completed | Added credential review flow, configurable document upload limits, and 60-day expiry warning horizon. |
| 3 | Backend MF1: Expose tenant subscription entitlement checks and enforce role quotas at user facade | Trần Hoàng Trung Hiếu | Completed | Integrated subscription entitlement validations to restrict user creation according to tenant plan limits. |
| 4 | Docs MF1: Record MF1-02–MF1-07 verification, permit verification, and Round 4 test report in Report 5 | Trần Hoàng Trung Hiếu | Completed | Documented verification evidence and test results for workforce credentials and flight permit validation. |
| 5 | Mobile MF2: Implement MF2-01 & MF2-02 assignment inbox and MF2-09 to MF2-11 field session route | Phùng Trung Quốc | Completed | Delivered mobile PR #9: assignment inbox, pre-flight checklist, and live field session execution screen. |
| 6 | Backend MF2: Implement `InspectionReadinessDecision` entity with snapshot hashing and pre-flight re-check | Phùng Trung Quốc | Completed | Persisted immutable readiness decisions with snapshot hashes and re-validated readiness at session start. |
| 7 | Backend MF2: Expose HTTP endpoints for readiness review sources, decisions, and field sessions | Phùng Trung Quốc | Completed | Delivered backend PR #64: endpoints for preparation review, readiness decisions, and session lifecycle. |
| 8 | Frontend MF2: Implement mission preparation panel (`MF2-03`–`06`) and readiness review panel (`MF2-07`) | Phùng Trung Quốc | Completed | Delivered frontend PR #37: preparation forms, permit links, shot lists, and admin readiness approval panel. |
| 9 | Architecture & CI: Execute Enterprise Inspection role/schema cutover; set up automated VPS2 deploy via Tailscale | Trần Tùng Bách | Completed | Applied V22–V25 migrations, updated security filters, and configured automated CI deployment to VPS2. |
| 10 | Backend MF3: Implement multi-section report drafting, immutable PDF deliverable, MinIO test infra | Trần Tùng Bách | Completed | Delivered section-scoped report authoring, PDF rendering with defect photos, and standalone MinIO test setup. |
| 11 | Frontend MF3 & UI: Build responsive commercial landing page, role dashboards, and section-by-section report editor | Trần Tùng Bách | Completed | Delivered landing page (dark tech theme, animejs), auth styling, role dashboards, and multi-section report UI. |
| 12 | Mobile MF3: Implement mobile evidence quality decisions repository and wire session hydration | Trần Tùng Bách | Completed | Delivered mobile PR #8: evidence quality decision model, repository, and auth state persistence. |
| 13 | Update business flows to v3.2 and author summary documents in docs repository | Trương Thái Như | Completed | Committed PR #33: updated business flow documentation to v3.2 and added executive summary briefs. |
| 14 | Backend MF4: Implement `MaintenanceWorkOrder` aggregate, tasks, estimates, and cost lines (MF4-01–08) | Trương Thái Như | Completed | Implemented work order aggregate root, itemized repair tasks, cost lines, and estimation entities. |
| 15 | Backend MF4: Implement scoped maintenance repositories, technician credential checks, team integrity | Trương Thái Như | Completed | Enforced tenant isolation on maintenance tables and validated technician credentials before team assignment. |
| 16 | Draft SDD Section 3 (MF4): Detailed class diagram and API contracts for maintenance work order lifecycle | Trương Thái Như | Completed | Documented REST endpoints, request/response DTOs, and state machine transition rules for maintenance. |

## II. Project Issues

| # | Project Issue | Owner | Status | Notes (Solution, Suggestion, etc.) |
|---:|---|---|---|---|
| 1 | Concurrent deployment on VPS2 caused Docker container rebuild race condition | Phùng Trung Quốc & Trần Tùng Bách | Identified | Both web and backend rebuilds attempted to mutate Compose stack simultaneously; planned deploy lock in Week 6. |
| 2 | Report drafting required per-section narrative generation rather than single monolithic blob | Trần Tùng Bách | Resolved | Refactored `ReportDraftClient` and data models to generate and persist individual section narratives. |

## III. Next Week Plan

| # | Project Work Item | In-charge | Deadline | Notes (Task Details, etc.) |
|---:|---|---|---|---|
| 1 | Frontend Org Admin resource management: user management, drone fleet, and permits UI | Trần Hoàng Trung Hiếu | 18 Oct 2026 | Build UI for managing organization fleet, permits, and credential reviews. |
| 2 | Serialize VPS deployment script with file lock to prevent race conditions | Phùng Trung Quốc | 18 Oct 2026 | Add deployment locking in GitHub Actions deployment workflow. |
| 3 | Implement finding verification CRUD, evidence retirement with audit reasons, and YOLO11 detection | Trần Tùng Bách | 18 Oct 2026 | Build findings review interface and integrate advisory defect detection service. |
| 4 | Implement maintenance estimation and cost tracking services | Trương Thái Như | 18 Oct 2026 | Deliver business logic for recording repair estimates and material cost lines. |

## IV. Other Project Matters/Suggestions

| # | Project Matter/Suggestions | Raised By | Date | Notes |
|---:|---|---|---|---|
| 1 | All four workflows (WF1–WF4) now have executable backend foundations in the main branch | Trần Tùng Bách | 11 Oct 2026 | Focus for Week 6 shifts toward end-to-end integration, UI polish, and test verification. |
