# FE-07: MF5 Maintenance Defect Rectification, Execution & Warranty Closure Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implement the complete FE-07 / MF5 lifecycle across Backend (Java 21/Spring Boot 4.1), Frontend (React 19/TS/MUI), Mobile (Flutter/Riverpod), and Docs: creating maintenance tickets from drone findings in accepted reports, contractor method statements and quotations with warranty terms, electronic repair orders, field execution enforcing mandatory distinct before/after evidence pairs, change orders for unforeseen damage, completion acceptance with warranty countdown, direct settlement tracking, and automatic ticket closure.

**Architecture:** Approach A. Backend adds 4 application services and 4 REST controllers in `com.smartdroneinspection.maintenance`, updates existing domain entities to map V14/V16/V18 columns, and enforces DB constraints (BR-31 defect linkage, V18 `ck_work_logs_evidence_pair`, V18 warranty clock, V16/V21 order status). Frontend builds a full `src/features/maintenance` module supporting Client and Provider Manager workflows. Mobile builds the `MAINTENANCE_ENGINEER` field task execution and before/after photo pair upload in `lib/features/tasks`.

**Tech Stack:** Java 21, Spring Boot 4.1.0, Spring Modulith, PostgreSQL 17, MinIO S3 object store, React 19, TypeScript 6.0, Material UI 9.4, TanStack Query v5, Zustand v5, Flutter ^3.13, Dart, Riverpod 3, GoRouter, Dio.

**Spec:** `SmartDroneInspection-Docs/development/plans/quoc/2026-10-06-mf5-maintenance-defect-resolution/spec.md`

## Global Constraints

- Work strictly on branch `feat/quoc-mf5-maintenance` across all 4 repositories.
- Do NOT add new Flyway migrations: the database schema is already deployed up to `V21` (`V8`, `V14`, `V15`, `V16`, `V18`, `V21` cover maintenance).
- Never trust client-supplied organization IDs or author IDs: derive caller identity and organization from the authenticated JWT principal.
- Client may only create tickets from accepted report versions belonging to their organization (`REPORT_NOT_ACCEPTED` or `REQUEST_SCOPE_DENIED` otherwise).
- Ticket creation MUST link at least one verified defect from the accepted report (`MAINTENANCE_FINDINGS_EMPTY` otherwise, enforcing BR-31).
- Work log completion strictly requires a verified pair of distinct before and after photos (`ck_work_logs_evidence_pair`).
- Direct bank transfer is recorded via status `AWAITING_PAYMENT` -> `PAID`; no online payment gateway is simulated.
- Warranty duration is a time-based free-rework obligation; ticket acceptance activates the clock (`warranty_started_at = accepted_at`, `warranty_ends_at = accepted_at + locked_warranty_days`).

## Review Focus

1. **Empty findings on ticket creation**: Attempting to create a ticket with empty `findingIds` must fail with `MAINTENANCE_FINDINGS_EMPTY`.
2. **Ticket creation from non-accepted or foreign report**: Attempting to create a ticket from a `DRAFT` or unreleased report, or a report belonging to another organization, must fail with `REQUEST_SCOPE_DENIED`.
3. **Work log submission without distinct before/after evidence**: Submitting a work log where `before_evidence_id` equals `after_evidence_id` or either is null must fail with `EVIDENCE_PAIR_INVALID`.
4. **Unassigned or wrong-role work log submission**: A user without `MAINTENANCE_ENGINEER` or an engineer not assigned to the order must receive `FORBIDDEN` or `MAINTENANCE_SCOPE_DENIED`.
5. **Change order approval updating order amount**: Approving a change request must advance the order to version 2 with updated `approved_amount` and `change_request_id`.

---

## File Structure

```text
SmartDroneInspection-Backend/
├── src/main/java/com/smartdroneinspection/maintenance/
│   ├── domain/
│   │   ├── MaintenanceTicket.java                              (modify: add acceptedAt, warrantyStartedAt, warrantyEndsAt)
│   │   ├── MaintenanceOrder.java                               (modify: add providerId, lockedWarrantyDays, warrantyEndDate, paidAt, bank details)
│   │   ├── MaintenanceQuotation.java                           (modify: add providerId, lockedWarrantyDays)
│   │   ├── MaintenanceWorkLog.java                             (modify: add beforeEvidenceId, afterEvidenceId)
│   │   └── enums/
│   │       └── MaintenanceOrderStatus.java                     (modify: add AWAITING_PAYMENT, PAID, DISPUTED)
│   ├── repository/
│   │   ├── MaintenanceTicketRepository.java                    (modify: add scoped queries)
│   │   ├── MaintenanceOrderRepository.java                     (modify: add active order queries)
│   │   ├── MaintenanceWorkLogRepository.java                   (modify: add query by assignment)
│   │   └── MaintenanceAssignmentRepository.java                (modify: add engineer inbox query)
│   ├── api/
│   │   ├── MaintenanceTicketController.java                    (create: client create ticket, list, detail)
│   │   ├── MaintenanceQuotationController.java                 (create: provider quote, client approve/reject)
│   │   ├── MaintenanceOrderController.java                     (create: client sign order, change requests, accept completion, confirm payment)
│   │   ├── MaintenanceExecutionController.java                 (create: assign engineer, engineer inbox, before/after upload, submit log)
│   │   └── dto/
│   │       ├── request/
│   │       │   ├── CreateMaintenanceTicketRequest.java         (create)
│   │       │   ├── CreateMaintenanceAssessmentQuotationRequest.java (create)
│   │       │   ├── CreateChangeRequestPayload.java             (create)
│   │       │   ├── SubmitWorkLogRequest.java                   (create)
│   │       │   └── AssignMaintenanceEngineerRequest.java       (create)
│   │       └── response/
│   │           ├── MaintenanceTicketSummaryResponse.java       (create)
│   │           ├── MaintenanceTicketDetailResponse.java        (create)
│   │           ├── MaintenanceQuotationResponse.java           (create)
│   │           ├── MaintenanceOrderResponse.java               (create)
│   │           └── MaintenanceWorkLogResponse.java             (create)
│   └── service/
│       ├── MaintenanceTicketService.java                       (create: ticket lifecycle + findings link)
│       ├── MaintenanceQuotationService.java                    (create: assessment & quotation orchestration)
│       ├── MaintenanceOrderService.java                        (create: order, change request, acceptance, payment)
│       └── MaintenanceExecutionService.java                    (create: assignment, before/after evidence, work log)
└── src/test/java/com/smartdroneinspection/maintenance/
    ├── MaintenanceTicketServiceTest.java                       (create: unit tests)
    ├── MaintenanceExecutionServiceTest.java                    (create: unit tests)
    └── MaintenanceWorkflowIntegrationTest.java                 (create: e2e workflow integration test)

SmartDroneInspection-Frontend/
└── src/features/maintenance/
    ├── api/
    │   └── maintenanceApi.ts                                   (create: types & Axios API endpoints)
    ├── hooks/
    │   └── useMaintenance.ts                                   (create: TanStack Query hooks & key factory)
    ├── pages/
    │   ├── MaintenancePage.tsx                                 (modify: full Client & Provider Manager views)
    │   ├── CreateTicketModal.tsx                               (create: select drone report findings)
    │   ├── QuotationReviewModal.tsx                            (create: review method statement & warranty days)
    │   └── CompletionAcceptanceModal.tsx                       (create: before/after photos comparison)
    └── pages/MaintenancePage.test.tsx                          (create: Vitest component tests)

SmartDroneInspection-Mobile/
├── lib/features/tasks/
│   ├── data/
│   │   └── maintenance_task_repository.dart                    (create: Dio repository for tasks & photo upload)
│   ├── domain/models/
│   │   └── maintenance_task.dart                               (create: Freezed models for assigned task & log)
│   └── presentation/
│       ├── tasks_page.dart                                     (modify: engineer task inbox)
│       ├── task_detail_page.dart                               (create: before/after photo capture & log submission)
│       └── providers/
│           └── maintenance_task_providers.dart                 (create: Riverpod providers)
└── test/features/tasks/
    └── maintenance_task_test.dart                              (create: unit & widget tests)
```

---

## Tasks

### Task 1: Backend Domain Entity Updates & Repository Enhancements

**Files:**
- Modify: `SmartDroneInspection-Backend/src/main/java/com/smartdroneinspection/maintenance/domain/enums/MaintenanceOrderStatus.java`
- Modify: `SmartDroneInspection-Backend/src/main/java/com/smartdroneinspection/maintenance/domain/MaintenanceOrder.java`
- Modify: `SmartDroneInspection-Backend/src/main/java/com/smartdroneinspection/maintenance/domain/MaintenanceTicket.java`
- Modify: `SmartDroneInspection-Backend/src/main/java/com/smartdroneinspection/maintenance/domain/MaintenanceWorkLog.java`
- Modify: `SmartDroneInspection-Backend/src/main/java/com/smartdroneinspection/maintenance/domain/MaintenanceQuotation.java`
- Modify: `SmartDroneInspection-Backend/src/main/java/com/smartdroneinspection/maintenance/repository/MaintenanceTicketRepository.java`
- Modify: `SmartDroneInspection-Backend/src/main/java/com/smartdroneinspection/maintenance/repository/MaintenanceOrderRepository.java`
- Modify: `SmartDroneInspection-Backend/src/main/java/com/smartdroneinspection/maintenance/repository/MaintenanceWorkLogRepository.java`
- Test: `SmartDroneInspection-Backend/src/test/java/com/smartdroneinspection/maintenance/MaintenanceEntityMappingTest.java`

**Interfaces:**
- Consumes: V14/V16/V18 database columns
- Produces: Updated entity getters/setters/constructors and repository query methods (`findByOrganizationIdOrderByCreatedAtDesc`, `findByMaintenanceTicketIdOrderByCreatedAtDesc`, `findByEngineerUserIdAndStatus`)

- [ ] **Step 1: Write the failing entity mapping test**

Create `SmartDroneInspection-Backend/src/test/java/com/smartdroneinspection/maintenance/MaintenanceEntityMappingTest.java`:
Verify that `MaintenanceOrderStatus` contains `AWAITING_PAYMENT`, `PAID`, `DISPUTED`, and that `MaintenanceOrder`, `MaintenanceTicket`, `MaintenanceWorkLog` have the new getters and setters.

- [ ] **Step 2: Run test to verify it fails**

Run: `.\mvnw.cmd -Dtest=MaintenanceEntityMappingTest test` (from `SmartDroneInspection-Backend` with Corretto 21)
Expected: FAIL (missing enum values or methods).

- [ ] **Step 3: Update entities and enum**

1. In `MaintenanceOrderStatus.java`: add `AWAITING_PAYMENT`, `PAID`, `DISPUTED`.
2. In `MaintenanceOrder.java`: add `@Column(name = "provider_id") private UUID providerId;`, `locked_warranty_days`, `warranty_end_date`, `payment_invoice_issued_at`, `paid_at`, `provider_bank_account_number`, `provider_bank_name`, plus getters and transition methods.
3. In `MaintenanceTicket.java`: add `@Column(name = "accepted_at") private Instant acceptedAt;`, `warranty_started_at`, `warranty_ends_at`, getters, and `recordAcceptance(Instant acceptedAt, int lockedWarrantyDays)`.
4. In `MaintenanceWorkLog.java`: add `@Column(name = "before_evidence_id") private UUID beforeEvidenceId;`, `@Column(name = "after_evidence_id") private UUID afterEvidenceId;`, getters and setters.
5. In `MaintenanceQuotation.java`: add `@Column(name = "provider_id") private UUID providerId;`, `@Column(name = "locked_warranty_days") private Integer lockedWarrantyDays;`.

- [ ] **Step 4: Update repositories**

Add query methods in `MaintenanceTicketRepository`, `MaintenanceOrderRepository`, and `MaintenanceWorkLogRepository`.

- [ ] **Step 5: Run test to verify it passes**

Run: `.\mvnw.cmd -Dtest=MaintenanceEntityMappingTest test`
Expected: PASS.

---

### Task 2: Backend MaintenanceTicketService and MaintenanceTicketController (MF5-01)

**Files:**
- Create: `SmartDroneInspection-Backend/src/main/java/com/smartdroneinspection/maintenance/api/dto/request/CreateMaintenanceTicketRequest.java`
- Create: `SmartDroneInspection-Backend/src/main/java/com/smartdroneinspection/maintenance/api/dto/response/MaintenanceTicketSummaryResponse.java`
- Create: `SmartDroneInspection-Backend/src/main/java/com/smartdroneinspection/maintenance/api/dto/response/MaintenanceTicketDetailResponse.java`
- Create: `SmartDroneInspection-Backend/src/main/java/com/smartdroneinspection/maintenance/service/MaintenanceTicketService.java`
- Create: `SmartDroneInspection-Backend/src/main/java/com/smartdroneinspection/maintenance/api/MaintenanceTicketController.java`
- Test: `SmartDroneInspection-Backend/src/test/java/com/smartdroneinspection/maintenance/MaintenanceTicketServiceTest.java`

**Interfaces:**
- Consumes: `MaintenanceTicketRepository`, `MaintenanceTicketFindingRepository`, `AssetRepository`, `ReportVersionRepository`, `VerifiedFindingRepository`, `UserAccess`
- Produces: `POST /api/v1/maintenance-tickets`, `GET /api/v1/maintenance-tickets`, `GET /api/v1/maintenance-tickets/{id}`

- [ ] **Step 1: Write failing unit test covering Story 1 (MF5-01) and Review Focus 1 & 2**

Create `SmartDroneInspection-Backend/src/test/java/com/smartdroneinspection/maintenance/MaintenanceTicketServiceTest.java`:
- Test 1: Empty `findingIds` throws `BusinessException("MAINTENANCE_FINDINGS_EMPTY")`.
- Test 2: Foreign organization asset throws `BusinessException("REQUEST_SCOPE_DENIED")`.
- Test 3: Unaccepted report version throws `BusinessException("REPORT_NOT_ACCEPTED")`.
- Test 4: Valid request creates ticket in `SUBMITTED` status and persists `MaintenanceTicketFinding` rows.

- [ ] **Step 2: Run test to verify it fails**

Run: `.\mvnw.cmd -Dtest=MaintenanceTicketServiceTest test`
Expected: FAIL.

- [ ] **Step 3: Implement DTOs, MaintenanceTicketService and MaintenanceTicketController**

Implement service and controller:
- `@PreAuthorize("hasRole('CLIENT')")` on create.
- Derive `organizationId` from authenticated caller via `UserAccess.findActiveUser(userId)`.
- Link findings into `maintenance_ticket_findings`.
- Controller returns `ApiResponse.success(ticketId)` for create, paged summary for list, full detail for get.

- [ ] **Step 4: Run test to verify it passes**

Run: `.\mvnw.cmd -Dtest=MaintenanceTicketServiceTest test`
Expected: PASS.

---

### Task 3: Backend MaintenanceQuotationService and MaintenanceQuotationController (MF5-02)

**Files:**
- Create: `SmartDroneInspection-Backend/src/main/java/com/smartdroneinspection/maintenance/api/dto/request/CreateMaintenanceAssessmentQuotationRequest.java`
- Create: `SmartDroneInspection-Backend/src/main/java/com/smartdroneinspection/maintenance/api/dto/response/MaintenanceQuotationResponse.java`
- Create: `SmartDroneInspection-Backend/src/main/java/com/smartdroneinspection/maintenance/service/MaintenanceQuotationService.java`
- Create: `SmartDroneInspection-Backend/src/main/java/com/smartdroneinspection/maintenance/api/MaintenanceQuotationController.java`
- Test: `SmartDroneInspection-Backend/src/test/java/com/smartdroneinspection/maintenance/MaintenanceQuotationServiceTest.java`

**Interfaces:**
- Consumes: `MaintenanceAssessmentRepository`, `MaintenanceQuotationRepository`, `MaintenanceTicketRepository`, `UserAccess`
- Produces: `POST /api/v1/maintenance-tickets/{id}/quotations`, `POST /api/v1/maintenance-quotations/{id}/approve`, `POST /api/v1/maintenance-quotations/{id}/reject`

- [ ] **Step 1: Write failing service unit test**

Create `SmartDroneInspection-Backend/src/test/java/com/smartdroneinspection/maintenance/MaintenanceQuotationServiceTest.java`:
- Provider Manager prepares assessment + quotation: creates `MaintenanceAssessment` with method statement and materials, then creates `MaintenanceQuotation` with `lockedWarrantyDays`. Ticket moves to `AWAITING_CLIENT_APPROVAL`.
- Client rejects quotation with reason -> quotation status `REJECTED`.
- Client approves quotation -> quotation status `APPROVED`.

- [ ] **Step 2: Run test to verify it fails**

Run: `.\mvnw.cmd -Dtest=MaintenanceQuotationServiceTest test`
Expected: FAIL.

- [ ] **Step 3: Implement service and controller**

Implement `MaintenanceQuotationService`:
- Validate provider has authority.
- In one `@Transactional`: save `MaintenanceAssessment`, then save `MaintenanceQuotation` (satisfying V8 foreign key `maintenance_assessment_id NOT NULL`).
- Implement Client approve and reject actions.
Implement `MaintenanceQuotationController`:
- `@PreAuthorize("hasRole('PROVIDER_MANAGER')")` on quote creation.
- `@PreAuthorize("hasRole('CLIENT')")` on approve/reject.

- [ ] **Step 4: Run test to verify it passes**

Run: `.\mvnw.cmd -Dtest=MaintenanceQuotationServiceTest test`
Expected: PASS.

---

### Task 4: Backend MaintenanceOrderService and MaintenanceOrderController (MF5-03, MF5-05, MF5-06, MF5-07, MF5-08)

**Files:**
- Create: `SmartDroneInspection-Backend/src/main/java/com/smartdroneinspection/maintenance/api/dto/request/CreateChangeRequestPayload.java`
- Create: `SmartDroneInspection-Backend/src/main/java/com/smartdroneinspection/maintenance/api/dto/response/MaintenanceOrderResponse.java`
- Create: `SmartDroneInspection-Backend/src/main/java/com/smartdroneinspection/maintenance/service/MaintenanceOrderService.java`
- Create: `SmartDroneInspection-Backend/src/main/java/com/smartdroneinspection/maintenance/api/MaintenanceOrderController.java`
- Test: `SmartDroneInspection-Backend/src/test/java/com/smartdroneinspection/maintenance/MaintenanceOrderServiceTest.java`

**Interfaces:**
- Consumes: `MaintenanceOrderRepository`, `MaintenanceQuotationRepository`, `MaintenanceTicketRepository`, `MaintenanceChangeRequestRepository`, `InvoiceRepository`, `UserAccess`
- Produces:
  - `POST /api/v1/maintenance-quotations/{quotationId}/order` (sign order)
  - `POST /api/v1/maintenance-orders/{id}/change-requests` (create change order)
  - `POST /api/v1/maintenance-change-requests/{id}/approve` (approve change order)
  - `POST /api/v1/maintenance-orders/{id}/accept-completion` (accept completion & start warranty)
  - `POST /api/v1/maintenance-orders/{id}/confirm-payment` (confirm bank transfer)

- [ ] **Step 1: Write failing service unit test**

Create `SmartDroneInspection-Backend/src/test/java/com/smartdroneinspection/maintenance/MaintenanceOrderServiceTest.java`:
- Test order creation: snapshots `locked_warranty_days`, status `CONFIRMED`.
- Test change order: creates `MaintenanceChangeRequest`, Client approves -> order version 2 created.
- Test completion acceptance: sets ticket `accepted_at`, computes `warranty_started_at` & `warranty_ends_at`, order becomes `AWAITING_PAYMENT`.
- Test payment confirmation: provider confirms receipt -> order becomes `PAID`, generates `invoices` record.

- [ ] **Step 2: Run test to verify it fails**

Run: `.\mvnw.cmd -Dtest=MaintenanceOrderServiceTest test`
Expected: FAIL.

- [ ] **Step 3: Implement service and controller**

Implement `MaintenanceOrderService` and `MaintenanceOrderController`:
- Adhere to `V18` warranty clock constraints:
  `warranty_started_at >= accepted_at` and `warranty_ends_at = warranty_started_at + lockedWarrantyDays`.
- Adhere to `V16` payment constraints: `provider_bank_account_number`, `provider_bank_name`, `paid_at`.

- [ ] **Step 4: Run test to verify it passes**

Run: `.\mvnw.cmd -Dtest=MaintenanceOrderServiceTest test`
Expected: PASS.

---

### Task 5: Backend MaintenanceExecutionService and MaintenanceExecutionController (MF5-04)

**Files:**
- Create: `SmartDroneInspection-Backend/src/main/java/com/smartdroneinspection/maintenance/api/dto/request/AssignMaintenanceEngineerRequest.java`
- Create: `SmartDroneInspection-Backend/src/main/java/com/smartdroneinspection/maintenance/api/dto/request/SubmitWorkLogRequest.java`
- Create: `SmartDroneInspection-Backend/src/main/java/com/smartdroneinspection/maintenance/api/dto/response/MaintenanceWorkLogResponse.java`
- Create: `SmartDroneInspection-Backend/src/main/java/com/smartdroneinspection/maintenance/service/MaintenanceExecutionService.java`
- Create: `SmartDroneInspection-Backend/src/main/java/com/smartdroneinspection/maintenance/api/MaintenanceExecutionController.java`
- Test: `SmartDroneInspection-Backend/src/test/java/com/smartdroneinspection/maintenance/MaintenanceExecutionServiceTest.java`

**Interfaces:**
- Consumes: `MaintenanceAssignmentRepository`, `MaintenanceWorkLogRepository`, `MaintenanceOrderRepository`, `EvidenceRepository`, `EvidenceObjectStore` (MinIO), `UserAccess`
- Produces:
  - `POST /api/v1/maintenance-orders/{id}/assignments` (assign engineer)
  - `GET /api/v1/maintenance-execution/my-assignments` (engineer task inbox)
  - `POST /api/v1/maintenance-orders/{id}/evidence` (upload before/after photo to MinIO, create `Evidence`)
  - `POST /api/v1/maintenance-orders/{id}/work-logs` (submit work log enforcing distinct before/after pair)

- [ ] **Step 1: Write failing service unit test covering Review Focus 3 & 4**

Create `SmartDroneInspection-Backend/src/test/java/com/smartdroneinspection/maintenance/MaintenanceExecutionServiceTest.java`:
- Test 1: Submitting work log with identical before and after photo IDs throws `BusinessException("EVIDENCE_PAIR_INVALID")`.
- Test 2: Submitting work log by an unassigned engineer throws `BusinessException("MAINTENANCE_SCOPE_DENIED")`.
- Test 3: Submitting valid work log with distinct photos saves `MaintenanceWorkLog` in `SUBMITTED` status.

- [ ] **Step 2: Run test to verify it fails**

Run: `.\mvnw.cmd -Dtest=MaintenanceExecutionServiceTest test`
Expected: FAIL.

- [ ] **Step 3: Implement service and controller**

Implement `MaintenanceExecutionService`:
- Upload evidence method: stores file in MinIO, creates `Evidence` with `evidenceKind = BEFORE_MAINTENANCE` or `AFTER_MAINTENANCE` and `inspection_id = null`.
- Submit work log method: checks `beforeEvidenceId != afterEvidenceId`, both exist, status becomes `SUBMITTED`.
Implement `MaintenanceExecutionController`.

- [ ] **Step 4: Run test to verify it passes**

Run: `.\mvnw.cmd -Dtest=MaintenanceExecutionServiceTest test`
Expected: PASS.

---

### Task 6: Backend End-to-End Workflow Integration Test

**Files:**
- Create: `SmartDroneInspection-Backend/src/test/java/com/smartdroneinspection/maintenance/MaintenanceWorkflowIntegrationTest.java`

- [ ] **Step 1: Write comprehensive workflow integration test**

Verify the complete 8-step lifecycle:
1. Client creates ticket from accepted finding (`SUBMITTED`).
2. Provider Manager creates assessment & quotation with 180 warranty days (`AWAITING_CLIENT_APPROVAL`).
3. Client approves quotation -> Order v1 created in `CONFIRMED`.
4. Provider Manager assigns Engineer (`EXECUTION`).
5. Engineer uploads Before photo, After photo, submits Work Log with distinct pair. Provider Manager verifies.
6. Client reviews Before/After pair, approves completion -> ticket records `accepted_at`, computes warranty end date, order becomes `AWAITING_PAYMENT`.
7. Provider Manager confirms direct payment receipt -> order becomes `PAID`.
8. Ticket warranty period is verified.

- [ ] **Step 2: Run test**

Run: `.\mvnw.cmd -Dtest=MaintenanceWorkflowIntegrationTest test`
Expected: PASS.

---

### Task 7: Frontend API Client and TanStack Query Hooks

**Files:**
- Create: `SmartDroneInspection-Frontend/src/features/maintenance/api/maintenanceApi.ts`
- Create: `SmartDroneInspection-Frontend/src/features/maintenance/hooks/useMaintenance.ts`
- Test: `SmartDroneInspection-Frontend/src/features/maintenance/api/maintenanceApi.test.ts`

- [ ] **Step 1: Write test for API client**

Create `maintenanceApi.test.ts`: mock Axios and verify paths for tickets, quotations, orders, work logs, and before/after upload.

- [ ] **Step 2: Implement maintenanceApi.ts**

Define TypeScript interfaces: `MaintenanceTicket`, `MaintenanceQuotation`, `MaintenanceOrder`, `MaintenanceWorkLog`, `CreateTicketInput`, `SubmitWorkLogInput`.
Call `/api/v1/maintenance-tickets`, `/api/v1/maintenance-quotations`, `/api/v1/maintenance-orders`, `/api/v1/maintenance-execution`.

- [ ] **Step 3: Implement useMaintenance.ts**

Query key factory `maintenanceKeys` + mutation hooks auto-invalidating `maintenanceKeys.all`.

- [ ] **Step 4: Run test**

Run: `npm test src/features/maintenance/api/maintenanceApi.test.ts`
Expected: PASS.

---

### Task 8: Frontend UI Screens in `features/maintenance`

**Files:**
- Modify: `SmartDroneInspection-Frontend/src/features/maintenance/pages/MaintenancePage.tsx`
- Create: `SmartDroneInspection-Frontend/src/features/maintenance/components/CreateTicketModal.tsx`
- Create: `SmartDroneInspection-Frontend/src/features/maintenance/components/QuotationReviewModal.tsx`
- Create: `SmartDroneInspection-Frontend/src/features/maintenance/components/CompletionAcceptanceModal.tsx`
- Test: `SmartDroneInspection-Frontend/src/features/maintenance/pages/MaintenancePage.test.tsx`

- [ ] **Step 1: Write failing component test**

Create `MaintenancePage.test.tsx`:
- Client view: shows "Create maintenance ticket" button, lists tickets, shows quotation approval dialog.
- Provider Manager view: shows quotations management, confirm payment button.

- [ ] **Step 2: Implement CreateTicketModal.tsx**

Form to select asset, paste accepted report ID, pick verified defect finding, set priority, instructions.

- [ ] **Step 3: Implement CompletionAcceptanceModal.tsx**

Side-by-side Before and After photo comparison viewer with "Accept & Sign Minutes" button and "Request Rework" button.

- [ ] **Step 4: Implement MaintenancePage.tsx**

Full dashboard layout with Material UI tabs (`Tickets`, `Orders`, `Work Logs`).

- [ ] **Step 5: Run lint & tests**

Run: `npm run lint` and `npm test src/features/maintenance/`
Expected: PASS with 0 errors.

---

### Task 9: Mobile Engineer Maintenance Task Inbox and Execution Screen

**Files:**
- Create: `SmartDroneInspection-Mobile/lib/features/tasks/data/maintenance_task_repository.dart`
- Create: `SmartDroneInspection-Mobile/lib/features/tasks/domain/models/maintenance_task.dart`
- Modify: `SmartDroneInspection-Mobile/lib/features/tasks/presentation/tasks_page.dart`
- Create: `SmartDroneInspection-Mobile/lib/features/tasks/presentation/task_detail_page.dart`
- Create: `SmartDroneInspection-Mobile/lib/features/tasks/presentation/providers/maintenance_task_providers.dart`
- Test: `SmartDroneInspection-Mobile/test/features/tasks/maintenance_task_test.dart`

- [ ] **Step 1: Write failing mobile tests**

Create `maintenance_task_test.dart`:
- Test repository mapping for `my-assignments` and work log submission.
- Test that submitting work log without both before and after photos is blocked.

- [ ] **Step 2: Implement maintenance_task_repository.dart and Freezed models**

Add methods: `getMyAssignments()`, `uploadPhoto({required File file, required String kind})`, `submitWorkLog(...)`.

- [ ] **Step 3: Implement tasks_page.dart and task_detail_page.dart**

- `tasks_page.dart`: List assigned maintenance tasks using `AsyncValueWidget`.
- `task_detail_page.dart`:
  - Show defect details and instructions.
  - Section 1: "Before Photo" button (camera capture + upload).
  - Section 2: "After Photo" button (camera capture + upload).
  - Section 3: Materials used & labor hours input.
  - "Submit Completion" button (enabled only when both photos exist).

- [ ] **Step 4: Run flutter analysis & tests**

Run:
`dart format --set-exit-if-changed .`
`flutter analyze`
`flutter test test/features/tasks/`
Expected: PASS.

---

### Task 10: Full Suite Verification Across All 4 Repositories

- [ ] **Step 1: Run Backend verification**

Run: `cd SmartDroneInspection-Backend; .\mvnw.cmd spotless:apply; .\mvnw.cmd test`
Verify all unit tests pass, spotless is clean.

- [ ] **Step 2: Run Frontend verification**

Run: `cd SmartDroneInspection-Frontend; npm run lint; npm run build; npm test`
Verify build succeeds with 0 lint errors.

- [ ] **Step 3: Run Mobile verification**

Run: `cd SmartDroneInspection-Mobile; dart format --set-exit-if-changed .; flutter analyze; flutter test`
Verify Flutter analysis and tests pass.

- [ ] **Step 4: Verify git status on all 4 repos**

Ensure all changes are clean and committed properly to branch `feat/quoc-mf5-maintenance`.
