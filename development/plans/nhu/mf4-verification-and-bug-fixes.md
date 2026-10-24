# MF4 Defect Remediation & Verification Report

**Owner:** Như
**Feature:** FE-07 / MF4 — Team Maintenance, Cost Control and Completion Reporting
**Verification Date:** 24 October 2026
**Status:** 100% Passed

---

## 1. Automated Test Suite Inventory

| Test Class | Focus | Assertions | Result |
| :--- | :--- | :--- | :--- |
| `MaintenanceApiIntegrationTest` | End-to-end API lifecycle, multi-tenant isolation, separation of duties, duplicate prevention, plain-text `jsonb` normalization, `REINSPECTION_REQUIRED` resumption, and cost reconciliation | 26 integration tests | ✅ Passed (0 failures) |
| `DeterministicScopeFallbackTest` | Rule-based engineering fallback across all defect categories (cracks, spalling, corrosion, leakage, deformation) | 5 unit tests | ✅ Passed (0 failures) |
| `MaintenanceScopeAdvisorServiceTest` | Tenant verification, RAG knowledge retrieval, LLM response handling, and fallback failover | 3 unit tests | ✅ Passed (0 failures) |
| `MaintenanceScopeAdvisorClientTest` | OpenAI REST client payload construction, SSE immunity, and robust JSON extraction | 2 unit tests | ✅ Passed (0 failures) |
| `ModulithArchitectureTest` | Spring Modulith module boundaries, acyclic dependencies, and package-info compliance | 3 architecture tests | ✅ Passed (0 failures) |
| `MaintenancePage.test.tsx` | Web UI rendering, KPI cards, candidate queue, dialog forms, and role-based action gating | 8 component tests | ✅ Passed (0 failures) |
| `maintenance_repository_test.dart` | Mobile tasks repository, Riverpod state updates, work log submission, execution release/resume/verify, and API failure mapping | 8 mobile unit tests | ✅ Passed (0 failures) |

---

## 2. Remediated Defects & Integration Gaps

During comprehensive end-to-end workflow verification, 6 integration defects were identified and resolved:

### 1. Cost Reconciliation Invalid Task Reference
- **Defect:** In `WorkOrderDetailPanel.tsx` (`CostsTab`), submitting actual cost lines sent `taskId: workOrder.sourceFindingId`. The backend rejects non-existent tasks with `400 COST_LINE_TASK_UNKNOWN`.
- **Impact:** Blocked cost reconciliation (`markCostsReconciled`), which in turn blocked work order closure (`close()`).
- **Fix:** Loaded planned tasks via `useTasks(workOrder.id)`, added a task selection dropdown in the cost reconciliation form, and bound actual cost lines to real task UUIDs.

### 2. Missing Lead Work Log Verification Action
- **Defect:** In `WorkOrderDetailPanel.tsx` (`ExecutionTab`), submitted work logs (`SUBMITTED`) lacked a verification action button for the team lead.
- **Impact:** Backend invariant requires `verifiedWorkLogs == submittedWorkLogs > 0` before `markWorkCompleted` can succeed. Without a verification button, declaring completion always threw `409 Conflict`.
- **Fix:** Integrated `useVerifyWorkLog` mutation hook and added the inline **"Verify work log"** button for submitted logs.

### 3. Transition Button State-Guard Enforcement
- **Defect:** In `WorkOrderDetailPanel.tsx` (`OverviewTab`), all four engineer transition buttons (`Mark ready`, `Start execution`, `Declare work completed`, `Resume after rework`) were displayed simultaneously.
- **Impact:** Clicking an action invalid for the current order status resulted in 409 Conflict error alerts.
- **Fix:** Added `isActionDisabled(action)` to enable only the action matching the current lifecycle status (`APPROVED` -> `READY` -> `IN_PROGRESS` -> `WORK_COMPLETED` / `REWORK_REQUIRED`).

### 4. Unvalidated Budget Approver Assignment
- **Defect:** `WorkOrderService.create` persisted `budgetApproverUserId` without verifying user existence, active status, `ORG_ADMIN` role, or tenant matching.
- **Impact:** An invalid approver stranded the work order in `AWAITING_APPROVAL` indefinitely.
- **Fix:** Added `userAccess.findActiveUser(request.budgetApproverUserId())` and verified role and tenant equality, returning `400 WORK_ORDER_APPROVER_INVALID` on mismatch.

### 5. Mutation of Closed Work Orders
- **Defect:** Write endpoints (`createTask`, `createEstimateVersion`, `recordWork`, `proposeChange`) lacked a check for the `CLOSED` terminal status.
- **Impact:** Closed work orders could still accumulate tasks, work logs, and change orders, violating Report 3 §3.8 snapshot immutability.
- **Fix:** Enforced `if (order.getStatus() == WorkOrderStatus.CLOSED) throw new BusinessException(HttpStatus.CONFLICT, "WORK_ORDER_CLOSED", ...)` across all four services.

### 6. Missing Completion Report PDF Artifact Access & Authenticated Download
- **Defect:** While the backend provided `GET /reports/{versionNo}/pdf`, the frontend completion report tab initially had no download action and later used a plain `<a href>` which did not attach the in-memory `Authorization: Bearer <token>` header (causing `401 Unauthorized`).
- **Impact:** Users could not download the official rendered PDF report deliverable from the browser.
- **Fix:** Added `downloadReportPdf` in `maintenanceApi.ts` using the authenticated Axios `api` client (`responseType: 'blob'`) and wired the **"Download PDF"** button to open the authenticated PDF blob URL.

### 7. PostgreSQL `jsonb` Plain-Text Serialization Across All 8 Maintenance Entities
- **Defect:** `V25` defines 13 columns across the 8 `maintenance_*` tables as `jsonb` (`corrective_scope`, `acceptance_criteria`, `tax_basis`, `assumptions`, `snapshot`, `tax_treatment`, `actual_cost_references`, `test_readings`, `affected_tasks`, `supporting_evidence`, `content_snapshot`, `acceptance_checklist`, `test_result`), while Web, Mobile, and RAG send plain prose strings rather than JSON literals.
- **Impact:** Creating work orders, tasks, estimates, work logs, change orders, reports, or acceptance decisions from the UI failed with PostgreSQL `invalid input syntax for type json`.
- **Fix:** Added `JsonbText` helper in `com.smartdroneinspection.maintenance.domain` to normalize plain text into valid JSON string literals on write while preserving JSON objects/arrays (`{...}`, `[...]`) and unwrapping JSON string literals on read.

### 8. Work Log Time Interval Constraint (`chk_maintenance_work_logs_interval`)
- **Defect:** `V25` enforces `started_at IS NULL OR ended_at IS NULL OR ended_at >= started_at`, and `MaintenanceWorkLog.submit()` requires `startedAt != null && endedAt != null`. When Web/Mobile submitted `hours` without explicit timestamps, `startedAt` defaulted to `Instant.now()` while `endedAt` remained `null`.
- **Impact:** Submitting a work log recorded from Web or Mobile failed with `409 WORK_LOG_WINDOW_REQUIRED`.
- **Fix:** Derived `[startedAt, endedAt]` from `hours` when `endedAt` is omitted in `MaintenanceExecutionService.recordWork`, and stamped `endedAt` on `submitWorkLog` if absent.

### 9. Resuming Execution After `REINSPECTION_REQUIRED`
- **Defect:** `MaintenanceWorkOrder.resumeAfterRework()` only allowed `WorkOrderStatus.REWORK_REQUIRED`, leaving work orders in `REINSPECTION_REQUIRED` with no transition back to `IN_PROGRESS`.
- **Impact:** Any work order returned with `REINSPECTION_REQUIRED` was permanently stranded.
- **Fix:** Updated `MaintenanceWorkOrder.resumeAfterRework()` and `WorkOrderDetailPanel.tsx` (`OverviewTab`) to support resuming from both `REWORK_REQUIRED` and `REINSPECTION_REQUIRED`.

### 10. Unique Index Supersession on Re-approval of Estimates and Reports
- **Defect:** Partial unique indexes `uk_maintenance_estimates_one_approved_per_order` and `uk_maintenance_reports_one_approved_per_order` allow only one `APPROVED` row per work order, but approving a second estimate or report version did not supersede the prior `APPROVED` row.
- **Impact:** Re-approving an estimate or report after rework failed with a database unique constraint violation.
- **Fix:** Superseded any prior `APPROVED` estimate version in `WorkOrderService.approveEstimate` and any prior `APPROVED` report version in `MaintenanceExecutionService.recordAcceptance`.

### 11. Client-Server Enum Alignment (`Priority`, `WorkLogStatus`, `ChangeOrderStatus`, `CostLineKind`)
- **Defect:** Frontend used `priority: 'MEDIUM' | 'CRITICAL'`, checked `log.status === 'DRAFT'` for work log submission, checked `change.status === 'PROPOSED'` for change order approval, and sent `lineKind: 'SERVICE'`. Backend enums use `NORMAL`/`URGENT`, `IN_PROGRESS`, `AWAITING_APPROVAL`, and `EXTERNAL_SERVICE`.
- **Impact:** Creating a default-priority work order returned `400 VALIDATION_FAILED`, the **"Submit for verification"** button never appeared on new work logs, and **"Approve / Reject / Return"** buttons never appeared on pending change orders.
- **Fix:** Aligned all frontend/mobile enum values with backend enums and added `@JsonCreator` aliases (`MEDIUM -> NORMAL`, `CRITICAL -> URGENT`) on `MaintenancePriority`.

### 12. Role-Scoped Workforce Queries & PDF Scope/Criteria Rendering
- **Defect:** `WorkOrderDetailPanel.tsx` called `/api/v1/workforce/users` for `MAINTENANCE_ENGINEER` (returning `403 Forbidden`), and `MaintenanceExecutionService.buildRenderContext` passed hardcoded placeholder strings for `correctiveScope` and `acceptanceCriteria` into the PDF template.
- **Impact:** Engineers could not select task assignees from the team, and downloaded PDFs showed generic boilerplate instead of the work order's actual corrective scope and acceptance criteria.
- **Fix:** Gated `useWorkforceUsers(isOrgAdmin)`, populated task assignee options from `useTeam(workOrder.id)`, and passed `order.getCorrectiveScope()` and `order.getAcceptanceCriteria()` into `MaintenanceReportRenderContext`.
