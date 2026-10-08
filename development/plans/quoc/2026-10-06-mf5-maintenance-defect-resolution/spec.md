# Feature Specification: FE-07 — MF5 Maintenance Defect Rectification, Execution & Warranty Closure

**Feature Branch**: `feat/quoc-mf5-maintenance`
**Created**: 2026-10-06
**Status**: Approved
**Input**: User requirement: "hoàn chỉnh phần BE, FE, Mobile ở Mainflow 5"
**Authority**: `business-flows.md` v3.4, `business-flows-summary.md` v2.1, `mf1-mf5-contract-matrix.md` v1.0, and Flyway migrations `V8`, `V14`, `V16`, `V18`, `V21`.

**Owner**: Quốc
**Feature code**: `FE-07 — Maintenance Defect Resolution`
**Canonical roles involved**: `CLIENT`, `PROVIDER_MANAGER`, `MAINTENANCE_ENGINEER`, `PLATFORM_OPERATOR`, `PLATFORM_ADMIN`.

---

## 1. Outcome & User Value

Turn verified defects from accepted drone inspection reports (MF4) into actionable maintenance tickets, formalize contractor method statements and quotations with warranty commitments, execute field repairs with mandatory before/after evidence pairs at matching angles, support change orders for unforeseen damage, enable completion acceptance and direct settlement, and track warranty countdown to automatic ticket closure—completing 100% of the maintenance lifecycle.

---

## 2. Core User Stories & Acceptance Criteria

### Story 1: Create Maintenance Ticket from Accepted Drone Findings (MF5-01)
* **Actor**: `CLIENT`
* **Trigger**: Client opens an accepted inspection report version and selects one or more verified defects (`verified_findings`).
* **Function**: Client creates a maintenance ticket specifying asset, preferred deadline, priority (`LOW`, `NORMAL`, `HIGH`, `URGENT`), specific instructions, and dispatch preference (`PRIORITY_INSPECTION_PROVIDER`, `DIRECT_APPOINTMENT`, `OPEN_RFQ`).
* **Validation**:
  * Asset must belong to the Client's organization (`REQUEST_SCOPE_DENIED` on mismatch).
  * Report version must be accepted (`REPORT_NOT_ACCEPTED` if not accepted).
  * Ticket must contain at least one verified finding (`MAINTENANCE_FINDINGS_EMPTY` if none selected, satisfying BR-31).
* **Output**: `MaintenanceTicket` created in `SUBMITTED` status, linked via `maintenance_ticket_findings`.

### Story 2: Technical Method Statement, Assessment & Quotation (MF5-02)
* **Actor**: `PROVIDER_MANAGER` (provider with verified `MAINTENANCE` capability)
* **Function**: Provider Manager reviews the drone defect dossier (high-res imagery, 3D coordinates, mm crack measurements) and creates an engineering assessment (`MaintenanceAssessment` with required repair work, materials estimate, labor hours) along with a lump-sum quotation (`MaintenanceQuotation`).
* **Key Fields**:
  * `requiredWork`: detailed method statement (epoxy injection, polymer mortar patch, rebar rust treatment).
  * `totalAmount` & `currency` (`VND`).
  * `lockedWarrantyDays`: committed free warranty duration (e.g., 180 or 365 days).
* **Output**: `MaintenanceAssessment` saved, `MaintenanceQuotation` created in `SENT` status, ticket transitions to `AWAITING_CLIENT_APPROVAL`.

### Story 3: Approve Quotation & Establish Electronic Maintenance Order (MF5-03)
* **Actor**: `CLIENT`
* **Function**: Client reviews quotation and warranty terms, then approves.
* **Output**:
  * Quotation transitions to `APPROVED`.
  * System creates `MaintenanceOrder` (version 1) in `CONFIRMED` status, snapshotting `approvedAmount`, `scopeSnapshot`, `paymentTerms` (direct post-service transfer), and `lockedWarrantyDays`.
  * Ticket transitions to `ORDER_CONFIRMED`.

### Story 4: Assign Maintenance Engineer & Execute On-Site Repair with Mandatory Before/After Evidence Pair (MF5-04)
* **Actors**: `PROVIDER_MANAGER` & `MAINTENANCE_ENGINEER`
* **Function**:
  1. Provider Manager assigns active `MAINTENANCE_ENGINEER` to the order (`assignment_type = 'EXECUTION'`).
  2. Engineer opens assignment on mobile/web, starts work on site (`IN_PROGRESS`).
  3. Engineer takes and uploads the "Before" photo (`BEFORE_MAINTENANCE` evidence via MinIO).
  4. Engineer performs physical repair, then takes and uploads the "After" photo (`AFTER_MAINTENANCE` evidence at matching angle).
  5. Engineer submits `MaintenanceWorkLog` with materials used, labor hours, work summary, and links `before_evidence_id` and `after_evidence_id`.
* **Validation**:
  * DB check `ck_work_logs_evidence_pair`: `before_evidence_id` and `after_evidence_id` must both be present and distinct.
  * Work log status transitions to `SUBMITTED`. Provider Manager reviews and verifies (`VERIFIED`).
  * Ticket transitions to `INTERNAL_REVIEW` / `RELEASED`.

### Story 5: Handle Unforeseen Damage via Change Order (MF5-05)
* **Actors**: `MAINTENANCE_ENGINEER`, `PROVIDER_MANAGER`, `CLIENT`
* **Function**: If hidden structural damage is encountered beyond the estimate:
  1. Work log is paused (`status = 'PAUSED_FOR_CHANGE'`).
  2. Change request is created (`MaintenanceChangeRequest` with reason, additional scope, cost delta, field photos).
  3. Client approves change request -> order increments to version 2 (`change_request_id` populated, `approved_amount` updated).

### Story 6: Completion Acceptance, Direct Settlement & Warranty Clock Activation (MF5-06, MF5-07, MF5-08)
* **Actors**: `CLIENT`, `PROVIDER_MANAGER`, `PLATFORM_OPERATOR`, `System`
* **Function**:
  1. **Acceptance**: Client compares Before and After photos on web/mobile:
     * *Rework requested*: Client clicks "Request Rework" -> ticket transitions to `REWORK_REQUESTED` -> Provider re-assigns engineer for free rework.
     * *Acceptance signed*: Client signs completion minutes -> ticket records `accepted_at`, order transitions to `AWAITING_PAYMENT`.
  2. **Warranty Clock Activation**:
     * System computes `warranty_started_at = accepted_at` and `warranty_ends_at = accepted_at + lockedWarrantyDays`.
     * `maintenance_orders.warranty_end_date` is updated to match.
  3. **Direct Settlement**:
     * System generates Payment Invoice for 100% of the repair fee with Provider bank details.
     * Client transfers directly to Provider's bank account.
     * Provider clicks "Confirm receipt" -> order status becomes `PAID`.
     * System calculates commission and platform invoices Provider Manager.
  4. **Warranty Closure**:
     * When `warranty_ends_at` expires with no outstanding dispute, the ticket is automatically closed (`status = 'CLOSED'`, `closed_at = now()`), completing 100% of the lifecycle.

---

## 3. Scope Boundaries & Constraints

* **In Scope**: Full lifecycle from ticket creation, assessment/quotation, order confirmation, work log execution with before/after photos, change order, completion acceptance, direct settlement tracking, and warranty closure.
* **Out of Scope**:
  * Online escrow/payment gateway integration (direct bank transfer used per `business-flows.md` v3.4).
  * Modifications to applied Flyway migrations (`V1`–`V21`). All tables and constraints exist in DB.

---

## 4. Architectural Boundaries

* **Backend (`SmartDroneInspection-Backend`)**:
  * Module: `com.smartdroneinspection.maintenance`.
  * Update JPA entities to include V14/V16/V18 columns (`providerId`, `lockedWarrantyDays`, `warrantyEndDate`, `paidAt`, `acceptedAt`, `warrantyStartedAt`, `warrantyEndsAt`, `beforeEvidenceId`, `afterEvidenceId`).
  * Add 4 application services: `MaintenanceTicketService`, `MaintenanceQuotationService`, `MaintenanceOrderService`, `MaintenanceExecutionService`.
  * Add 4 controllers: `MaintenanceTicketController`, `MaintenanceQuotationController`, `MaintenanceOrderController`, `MaintenanceExecutionController`.
* **Frontend (`SmartDroneInspection-Frontend`)**:
  * Feature: `src/features/maintenance/`.
  * API client `maintenanceApi.ts` + TanStack Query hooks `useMaintenance.ts`.
  * Pages/Views:
    * Client view: List tickets, Create ticket from accepted finding, Review quotation, Review before/after photos for acceptance.
    * Provider Manager view: Review tickets, Create method statement & quote, Assign engineer, Manage change orders, Confirm payment receipt.
* **Mobile (`SmartDroneInspection-Mobile`)**:
  * Feature: `lib/features/tasks/`.
  * Engineer inbox: List assigned maintenance tasks (`EXECUTION`, `REWORK`).
  * Work execution screen: Camera capture for Before photo and After photo, materials input, submit work log.
