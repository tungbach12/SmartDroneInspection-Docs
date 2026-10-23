# MF4 Defect Remediation & Verification Report

**Owner:** Như  
**Feature:** FE-07 / MF4 — Team Maintenance, Cost Control and Completion Reporting  
**Verification Date:** 23 October 2026  
**Status:** 100% Passed  

---

## 1. Automated Test Suite Inventory

| Test Class | Focus | Assertions | Result |
| :--- | :--- | :--- | :--- |
| `MaintenanceApiIntegrationTest` | End-to-end API lifecycle, multi-tenant isolation, separation of duties, duplicate prevention, and cost reconciliation | 25 integration tests | ✅ Passed (0 failures) |
| `DeterministicScopeFallbackTest` | Rule-based engineering fallback across all defect categories (cracks, spalling, corrosion, leakage, deformation) | 5 unit tests | ✅ Passed (0 failures) |
| `MaintenanceScopeAdvisorServiceTest` | Tenant verification, RAG knowledge retrieval, LLM response handling, and fallback failover | 3 unit tests | ✅ Passed (0 failures) |
| `MaintenanceScopeAdvisorClientTest` | OpenAI REST client payload construction, SSE immunity, and robust JSON extraction | 2 unit tests | ✅ Passed (0 failures) |
| `ModulithArchitectureTest` | Spring Modulith module boundaries, acyclic dependencies, and package-info compliance | 3 architecture tests | ✅ Passed (0 failures) |
| `MaintenancePage.test.tsx` | Web UI rendering, KPI cards, candidate queue, dialog forms, and role-based action gating | 8 component tests | ✅ Passed (0 failures) |
| `maintenance_repository_test.dart` | Mobile tasks repository, Riverpod state updates, work log submission, and API failure mapping | 5 mobile unit tests | ✅ Passed (0 failures) |

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

### 6. Missing Completion Report PDF Artifact Access
- **Defect:** While the backend provided `GET /reports/{versionNo}/pdf`, the frontend completion report tab only displayed text snapshots.
- **Impact:** Users could not download the official rendered PDF report deliverable.
- **Fix:** Added `getReportPdfUrl` in `maintenanceApi.ts` and an interactive **"Download PDF"** link with `PictureAsPdfOutlined` icon on every report version.
