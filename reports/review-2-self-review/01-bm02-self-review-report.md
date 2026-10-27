---
title: "SWP490 Review 2 - BM02 SRS/SDD Self-Review Report"
document_type: review2-bm02
version: "1.0"
date: "2026-10-27"
project_code: "GFA26SE139"
group_name: "FA26SE112"
---

# I. BM02 – SRS/SDD Self-Review Report

## 1. Self-Review Execution Metadata

| Field | Value |
| --- | --- |
| **Document Code** | `SWP490_GFA26SE139_R2_SelfReview` |
| **Project Code & Name** | `GFA26SE139` — SmartDroneInspection: AI-powered Infrastructure Inspection Management Platform |
| **Group Name** | `FA26SE112` |
| **Coding Agent / Tool Used** | `Claude Code / Pi Coding Agent` (with full read access to workspace repositories) |
| **AI Model** | `Claude Opus 4.6` |
| **Execution Date** | `2026-10-27` |
| **Registration Form Baseline** | `Version 2.0 (Proposed Final at Review 2, accompanied by BM03 Record of Changes)` |
| **Repository Tag Reviewed** | `review-2` (`SmartDroneInspection-backend`, `SmartDroneInspection-frontend`, `SmartDroneInspection-mobile`, `SmartDroneInspection-docs`) |

## 2. Standard Review Prompt Executed (Unmodified)

```text
You are reviewing the SRS and SDD of a software capstone project against its
registration form and source code. Report only; do not change any file.
Inputs: the registration form, SRS, SDD (with diagrams), source code and
database script in this repository.
Check:
1. Scope: FRs in the SRS not covered by the registration form, and
   registration items with no FR.
2. Requirements: FRs without an actor or testable acceptance criteria;
   NFRs without metric, threshold and measurement method.
3. Data: entities missing from the Logical ERD; ERD entities or attributes
   missing from the database script, and tables not in the ERD.
4. States: for each main entity, states used in code but missing from its
   state machine; transitions with no triggering FR; states with no exit.
5. Flows: main business flows in activity diagrams with no implementation
   or no test.
6. Architecture: components or third-party services in code but not in the
   architecture diagram, and the reverse.
7. Design vs code: modules, APIs or business rules implemented differently
   from the SDD.
Output one table: ID | Category | Location | Finding | Severity
(High/Medium/Low) | Evidence. Then list the 5 most important findings.
If something cannot be verified from the repository, say so; do not guess.
```

---

## 3. Raw AI Self-Review Output (Unedited)

### 3.1 Findings Table (`ID | Category | Location | Finding | Severity | Evidence`)

| ID | Category | Location | Finding | Severity | Evidence |
| :---: | --- | --- | --- | :---: | --- |
| `SR-01` | `1. Scope` | Registration Form v1.0 (`19/08/2026`) vs. SRS Report 3 (`§1.1`, `§3.2–3.9`) & Backend Code | The original v1.0 Registration Form referenced an external `SmartDroneHub` REST API for drone mission telemetry, a `Viewer` actor, `DroneKnowledgeAI` historical case recommendation, and an `ASP.NET Core / EF Core / SignalR` stack, whereas the implemented codebase and SRS/SDD deliver a self-contained 5-role Enterprise SaaS & B2B Drone Leasing platform (`Platform Admin`, `Platform Manager`, `Organization Manager`, `Inspector`, `Maintenance Engineer`) on `Java 21 / Spring Boot 4.1.0 / Spring Modulith 2.1.1` with `YOLO11`, `LLM Report Drafting`, and `pgvector` `RAG Maintenance Scope Advisor`. | `High` | Google Doc Registration v1.0 vs. `SmartDroneInspection-backend/pom.xml`, `UserRole.java`, `V1`–`V5` migrations, and Registration v2.0 + `BM03`. |
| `SR-02` | `7. Design vs code` | Report 4 SDD (`01-system-design.md §1.2`, `03-detailed-design.md §3.1–3.8`) vs. Backend Code | Prior to the Review 2 SDD sync, Report 4 §1.2 listed 8 legacy packages (`auth`, `users`, `assets`, `inspections`, `ai`, `reports`, `maintenance`, `common`) and §3.1–3.8 class diagrams referenced retired classes (`Credential`, `AssetPair`, `FieldSessionController`, `EvidenceController`, `DefectAnalysisController`), whereas the actual backend enforces 9 Spring Modulith modules (`users`, `workforce`, `subscriptions`, `assets`, `inspections`, `maintenance`, `notifications`, `dashboard`, `infrastructure`) and 21 controllers (`BrowserAuthController`, `InspectionFieldSessionController`, `InspectionController`, `MaintenanceExecutionController`, etc.). | `High` | `ModulithArchitectureTest.java`, `SmartDroneInspection-backend/src/main/java/com/smartdroneinspection/*`, and Report 4 `01-system-design.md` / `03-detailed-design.md`. |
| `SR-03` | `4. States` | Report 3 SRS (`§3.8.1`) & Report 4 SDD (`§2.2`, `§3.7`) vs. `WorkOrderStatus.java` | Report 3 §3.8.1 and Report 4 §3.7.2 previously referred to initial work order creation status as `PLANNING` and omitted explicit State Machine diagrams in SDD, whereas `MaintenanceWorkOrder.java` (`WorkOrderStatus` enum) implements a 12-state lifecycle starting at `Draft` (`Draft`, `Awaiting Approval`, `Approved`, `Ready`, `In Progress`, `Work Completed`, `Submitted for Acceptance`, `Accepted`, `Rework Required`, `Re-Inspection Required`, `Cost Reconciled`, `Closed`). | `High` | `MaintenanceWorkOrder.java`, `WorkOrderStatus.java`, Report 3 `03-functional-requirements.md §3.8`, Report 4 `02-database-design.md §2.2`. |
| `SR-04` | `2. Requirements` | Report 3 SRS (`03-functional-requirements.md`, `04-non-functional-requirements.md`) | While Report 3 §3.2–3.9 specified Inputs, Validations, Processing, and Outputs for each function, it lacked a consolidated FR-to-Actor-and-Testable-Acceptance-Criteria matrix (`AC-FE01`–`AC-FE08`) and §4.2 lacked a unified NFR table binding every NFR (`NFR-01`–`NFR-06`) to an explicit Metric, Threshold, and Measurement Method. | `Medium` | Report 3 `03-functional-requirements.md §3.10` and `04-non-functional-requirements.md §4.2.5`. |
| `SR-05` | `3. Data` | Report 3 (`§3.1.5`) & Report 4 (`02-database-design.md`) ERD vs. `V3__drop_unused_wf1_columns.sql` | The Mermaid Logical ERD previously included `ORGANIZATION ||--o{ ASSET_CATEGORY : defines`, whereas `V3__drop_unused_wf1_columns.sql` dropped `asset_categories.organization_id`, making `asset_categories` a global platform catalog managed by `ADMIN`. Additionally, `repair_knowledge_chunks` (standalone RAG reference table) and `event_publication` (Spring Modulith outbox table) exist in `V1` and runtime schema inventory alongside the 29 relational domain tables. | `Medium` | `V1__baseline.sql`, `V3__drop_unused_wf1_columns.sql`, `FullDatabaseSchemaMigrationTest.java`, `RuntimePersistenceInventoryTest.java`, and Report 4 `02-database-design.md`. |
| `SR-06` | `3. Data` | `drone_leases` vs. `payment_transactions` in `V1__baseline.sql` & `V2__role_restructure_and_drone_leasing.sql` | `payment_transactions` has a foreign key `subscription_id -> subscriptions(id)` for Enterprise Subscription PayPal orders, whereas B2B Drone Leases (`drone_leases` in `V2`) persist `paypal_order_id`, `paypal_capture_id`, and `external_reference` directly on `drone_leases` rather than writing a row to `payment_transactions`. | `Low` | `V1__baseline.sql` (`payment_transactions`), `V2__role_restructure_and_drone_leasing.sql` (`drone_leases`), `DroneLease.java`. |
| `SR-07` | `3. Data` | `audit_events` in `V1__baseline.sql` vs. JPA Entity Inventory | `audit_events` is one of the 30 application tables in PostgreSQL (`V1__baseline.sql`) and appears in the Logical ERD, but is written and queried via `JdbcTemplate` (`SecurityAuditService.java`) rather than a mutable JPA `@Entity` class to guarantee append-only immutability. | `Low` | `SecurityAuditService.java`, `PersistenceEntityOwnershipTest.java`, `RuntimePersistenceInventoryTest.java`. |
| `SR-08` | `5. Flows` | Report 5 (`Report5_Test Report.xlsx`) vs. Main Workflows `WF-01`–`WF-04` | Prior to Review 2 workbook consolidation (v5.00), `Report5_Test Report.xlsx` only had 8 feature sheets (`11` rows total). After expanding to 12 feature sheets (`Feature 1`–`Feature 12` for `FE-01`–`FE-12`, `64` rows total: `60 Passed`, `4 Pending`), 4 manual staging/mobile scenarios (`WF1-010` live PayPal webhook on staging, `WF2-015` mobile multi-session field walkthrough, `WF3-012` staging browser no-repair handoff branches, and `WF4-011` mobile maintenance work order & Lead verify walkthrough) remain `Pending` for Milestone 4. | `Medium` | `SmartDroneInspection-docs/reports/report-5-test-report/01-test-cases/test-case-list.md`, `02-test-statistics/test-statistics.md`, `03-features/fe-01..fe-12.md`. |
| `SR-09` | `6. Architecture` | Report 3 (`§3.9.2`) vs. `NotificationService.java` & Mobile Repo (`SmartDroneInspection-mobile`) | Report 3 §3.9.2 general prose mentions SMTP email and WebSocket delivery, while the normative §3.9.2 delivery slice note and backend code (`NotificationService.java`, `NotificationController.java`) implement a deduplicated **in-app notification inbox** (`NotificationChannel.IN_APP`) on Web and REST API (`/api/v1/notifications`), with no SMTP server, WebSocket push, or Flutter mobile notification tab currently wired. | `Medium` | `NotificationService.java`, `NotificationController.java`, `SmartDroneInspection-mobile/lib/core/router/app_router.dart`, Report 3 `03-functional-requirements.md §3.9.2`. |
| `SR-10` | `7. Design vs code` | Frontend `src/features/assets/pages/` vs. `accessPolicy.ts` | Three legacy frontend component files (`AssetReviewPage.tsx`, `InspectionSchedulesPage.tsx`, `ScheduleProposalsPage.tsx`) remain in the repository from an earlier iteration, though `accessPolicy.ts` assigns `[]` roles to `asset-review` and active routing uses `AssetsPage.tsx`, `RecurringSchedulesPage.tsx`, and `InspectionsPage.tsx`. | `Low` | `SmartDroneInspection-frontend/src/app/permissions/accessPolicy.ts`, `src/app/router/router.tsx`. |

### 3.2 Top 5 Most Important Findings (Raw AI Summary)
1. **`SR-01` (High — Scope Alignment)**: Registration Form v1.0 (`19/08/2026`) must be updated to v2.0 (with `BM03 Record of Changes`) to reflect the self-contained 5-role Enterprise SaaS & B2B Drone Leasing scope, `Java 21 / Spring Boot 4.1` stack, and `YOLO11 + LLM + pgvector RAG` AI architecture.
2. **`SR-02` (High — Design vs. Code)**: Report 4 (SDD) package diagram, class diagrams, and sequence diagrams must match the 9 Spring Modulith modules and 21 REST controllers in `SmartDroneInspection-backend` rather than earlier pre-consolidation class names.
3. **`SR-03` (High — State Machines)**: Report 3 and Report 4 must use the exact 12-state `WorkOrderStatus` enum (`Draft`..`Closed`, not `PLANNING`) and include explicit Mermaid `stateDiagram-v2` state machines for all main lifecycle entities.
4. **`SR-08` (Medium — Flows & Test Coverage)**: Report 5 (`Report5_Test Report.xlsx`) must populate all 8 feature sheets (`Feature 1`–`Feature 12`) to meet the Review 2 Section 09.3 formula (`64` test cases across `WF-01`–`WF-04`), and track the 4 `Pending` staging/mobile scenarios to closure before Defense 1.1.
5. **`SR-04` & `SR-05` (Medium — Requirements & ERD)**: Report 3 must include explicit testable Acceptance Criteria (`AC-FE01`–`AC-FE08`) and quantified NFR metrics/thresholds/measurement methods (`NFR-01`–`NFR-06`), and the ERD must reflect global `ASSET_CATEGORY` (`V3`).

---

## 4. Team Response & Resolution Plan

| ID | Severity | Team Response (`Fixed` / `Kept` / `Planned`) | Resolution Details (Commit / File Reference, Rationale, or Owner & Deadline) |
| :---: | :---: | :---: | --- |
| `SR-01` | `High` | **`Fixed`** | Authored proposed final Registration Form **v2.0** (`reports/review-2-registration/01-registration-form.md`) and **BM03 Record of Changes** (`02-bm03-record-of-changes.md`) reconciling all 7 scope/stack updates from v1.0 (`19/08/2026`) to the 5-role Enterprise SaaS & B2B Drone Leasing baseline (`review-2` tag). |
| `SR-02` | `High` | **`Fixed`** | Updated Report 4 SDD (`01-system-design.md §1.1–1.3` and `03-detailed-design.md §3.0–3.8`) with the exact 9 Spring Modulith packages, 5-group Technology Declaration tables, 4 Main Workflow Activity Diagrams (`WF-01`–`WF-04`), and 21 production controllers. |
| `SR-03` | `High` | **`Fixed`** | Updated Report 3 (`§3.8`) to the exact 12-state `MaintenanceWorkOrder` lifecycle (`Draft`..`Closed`) and added complete Mermaid `stateDiagram-v2` State Machine diagrams and transition tables in Report 4 (`02-database-design.md §2.2`). |
| `SR-04` | `Medium` | **`Fixed`** | Added the normative FR-to-Actor-and-Acceptance-Criteria matrix (`FR-01`–`FR-17` / `AC-FE01-01`–`AC-FE08-01` in Report 3 `§3.10`) and the quantified NFR table (`NFR-01`–`NFR-06` in Report 3 `§4.2.5`). |
| `SR-05` | `Medium` | **`Fixed`** | Removed the obsolete `ORGANIZATION ||--o{ ASSET_CATEGORY` edge in both Report 3 (`§3.1.5`) and Report 4 (`§2.0`) Mermaid ERDs and documented all 30 application tables + `event_publication` outbox table. |
| `SR-06` | `Low` | **`Kept`** | **Rationale**: Intentional schema design in `V2__role_restructure_and_drone_leasing.sql`. Storing `paypal_order_id`, `paypal_capture_id`, and `external_reference` directly on `drone_leases` keeps lease settlement atomic on the contract row without polymorphic FK ambiguity on `payment_transactions`. Documented in SDD `§2.0`. |
| `SR-07` | `Low` | **`Kept`** | **Rationale**: Intentional security control. Writing `audit_events` exclusively through `JdbcTemplate` in `SecurityAuditService` prevents accidental JPA entity dirty-checking updates or deletions, guaranteeing append-only audit integrity (`BR-38`). Verified by `RuntimePersistenceInventoryTest`. |
| `SR-08` | `Medium` | **`Fixed` (Workbook) / `Planned` (4 Pending TCs)** | **Fixed**: Expanded `Report5_Test Report.xlsx` v5.00 to **64 Test Cases** across **12 Feature sheets (`Feature 1`–`Feature 12` for `FE-01`–`FE-12`)** (`60 Passed`, `4 Pending`, `93.75%` pass rate; `87.50%` automated in CI) and authored `Report5_Test Documentation.docx`.<br>**Planned**: Execute the 4 remaining `Pending` manual staging/mobile cases (`WF1-010` Owner: **Trần Hoàng Trung Hiếu**, `WF2-015` Owner: **Phùng Trung Quốc**, `WF3-012` Owner: **Trần Tùng Bách**, `WF4-011` Owner: **Trương Thái Như** — Deadline: **`2026-11-15`**). |
| `SR-09` | `Medium` | **`Kept` (In-App Scope) / `Planned` (Mobile UI)** | **Kept**: Per SRS `§3.5.2` delivery slice note, notifications use the deduplicated `IN_APP` inbox (`notifications` + `event_publication` outbox); external SMTP/OS push are out of scope.<br>**Planned**: Deliver the Flutter mobile notification inbox list & mark-as-read screen consuming `GET /api/v1/notifications` (Owner: **Trần Hoàng Trung Hiếu**, Deadline: **`2026-11-12`**). |
| `SR-10` | `Low` | **`Planned`** | Remove unrouted legacy frontend component files (`AssetReviewPage.tsx`, `InspectionSchedulesPage.tsx`, `ScheduleProposalsPage.tsx`) during Milestone 4 cleanup (Owner: **Trần Hoàng Trung Hiếu**, Deadline: **`2026-11-05`**). |
