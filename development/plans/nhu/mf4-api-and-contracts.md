# MF4 API Contracts and Governance Rules

**Owner:** Như  
**Feature:** FE-07 / MF4 — Team Maintenance, Cost Control and Completion Reporting  
**Specification:** Report 3 §3.8; `project-reference/business-flows.md`  

---

## 1. Lifecycle State Machine

Work order progression follows a strict non-linear state machine enforced by `MaintenanceWorkOrder.java`:

```text
       [DRAFT]
          │ triage() / assignTeam()
          ▼
 [AWAITING_APPROVAL] ◄──────────────────┐
          │                             │ returnEstimateForRework()
          ├─────────────────────────────┘
          │ approveEstimate()
          ▼
      [APPROVED]
          │ markReady()
          ▼
       [READY]
          │ markInProgress()
          ▼
    [IN_PROGRESS] ◄─────────────────────┐
          │                             │ resumeExecutionAfterRework()
          ├─────────────────────────────┘
          │ markWorkCompleted() (Requires 100% verified work logs)
          ▼
   [WORK_COMPLETED]
          │ markSubmittedForAcceptance()
          ▼
[SUBMITTED_FOR_ACCEPTANCE]
          │
          ├──► requireReworkAfterAcceptance() ──► [REWORK_REQUIRED] ──► resumeExecutionAfterRework() ──► [IN_PROGRESS]
          │
          ├──► requireReinspection() ──────────► [REINSPECTION_REQUIRED] ──► (Dispatches MF1 Re-inspection)
          │
          └──► accept()
                 ▼
             [ACCEPTED]
                 │ markCostsReconciled()
                 ▼
          [COST_RECONCILED]
                 │ close()
                 ▼
              [CLOSED] (Terminal, immutable)
```

---

## 2. Separation of Duties Matrix

In accordance with Report 3 §3.8.1, the backend strictly rejects conflicting role combinations:

| Action | Allowed Role | Mandatory Separation Invariant | Enforced At |
| :--- | :--- | :--- | :--- |
| **Create Work Order** | `ORG_ADMIN` | Must belong to asset's organization; finding must be published & repair-required. | `WorkOrderService.create` |
| **Assign Team** | `ORG_ADMIN` | Lead and Report Author must be eligible Engineers; Reviewer must be `ORG_ADMIN`; Reviewer cannot be Lead or Author. | `WorkOrderService.assignTeam` |
| **Approve Estimate** | `ORG_ADMIN` | Must be the designated `budgetApproverUserId`; cannot be Lead, Author, or Reviewer (executing team). | `WorkOrderService.approveEstimate` |
| **Record Work Log** | `MAINTENANCE_ENGINEER` | Must be an active member of this work order's team. | `MaintenanceExecutionService.recordWork` |
| **Verify Work Log** | `MAINTENANCE_ENGINEER` | Must be the designated `teamLeadUserId`. | `MaintenanceExecutionService.verifyWorkLog` |
| **Declare Work Complete** | `MAINTENANCE_ENGINEER` | Must be the designated `teamLeadUserId`; requires count(submitted) == count(verified) > 0. | `MaintenanceExecutionService.markWorkCompleted` |
| **Submit Completion Report** | `MAINTENANCE_ENGINEER` | Must be the designated `reportAuthorUserId`. | `MaintenanceExecutionService.submitReport` |
| **Independent Acceptance** | `ORG_ADMIN` | Must be the designated `acceptingReviewerUserId`; cannot be Lead, Author, or Member. | `MaintenanceExecutionService.recordAcceptance` |
| **Reconcile Costs** | `ORG_ADMIN` | Must be the designated `acceptingReviewerUserId` (authorized cost reviewer). | `MaintenanceExecutionService.reconcile` |
| **Close Work Order** | `ORG_ADMIN` | Work order must be in `COST_RECONCILED` status. | `MaintenanceExecutionService.close` |

---

## 3. REST API Endpoint Catalog

All routes reside under `/api/v1/maintenance`:

### Triage & Planning
- `GET /repair-candidates`: List triage-ready published findings without an active work order.
- `POST /suggest-scope`: RAG-assisted technical scope and acceptance criteria advisor.
- `GET /work-orders`: List organization work orders (server-paged, assignment-scoped for engineers).
- `GET /work-orders/{id}`: Detailed work order header.
- `POST /work-orders`: Open a new work order from a verified candidate (supports optional `initialTasks` for 1-click provisioning).
- `GET /work-orders/{id}/team`: List designated team roster and active statuses.
- `POST /work-orders/{id}/team`: Designate lead, author, reviewer, and members.

### Task & Cost Baseline
- `GET /work-orders/{id}/tasks`: List planned tasks and execution statuses.
- `POST /work-orders/{id}/tasks`: Add a task (Lead only).
- `POST /work-orders/{id}/suggest-estimate`: RAG-assisted technical norm and cost estimation advisor.
- `GET /work-orders/{id}/estimate-versions`: List cost estimate baseline history.
- `POST /work-orders/{id}/estimate-versions`: Prepare an estimate version with priced lines (Lead only).
- `POST /work-orders/{id}/estimate-versions/{v}/submit`: Submit estimate for approval.
- `POST /work-orders/{id}/estimate-versions/{v}/approve`: Approve initial baseline (Budget Approver).
- `POST /work-orders/{id}/estimate-versions/{v}/reject`: Return estimate for rework (Budget Approver).

### Execution, Logs & Changes
- `POST /work-orders/{id}/release`: Confirm readiness (`READY`).
- `POST /work-orders/{id}/start`: Start execution (`IN_PROGRESS`).
- `GET /work-orders/{id}/work-logs`: List recorded time, materials, and test readings.
- `POST /work-orders/{id}/work-logs`: Record progress on a planned task.
- `POST /work-orders/{id}/work-logs/{logId}/submit`: Submit work log for verification.
- `POST /work-orders/{id}/work-logs/{logId}/verify`: Verify work log (Team Lead).
- `POST /work-orders/{id}/work-logs/batch-verify`: Verify all submitted work logs for this work order at once (Team Lead).
- `GET /work-orders/{id}/changes`: List scope/cost change requests.
- `POST /work-orders/{id}/changes`: Propose a change request with delta cost and evidence.
- `POST /work-orders/{id}/changes/{no}/approve`: Approve change delta (Budget Approver).
- `POST /work-orders/{id}/changes/{no}/reject`: Reject change delta (Budget Approver).
- `POST /work-orders/{id}/declare-complete`: Declare physical completion (`WORK_COMPLETED`).

### Reporting, Acceptance & Closure
- `GET /work-orders/{id}/reports`: List completion report versions.
- `GET /work-orders/{id}/reports/auto-draft`: Auto-populate completion report draft narrative from verified tasks and logs.
- `POST /work-orders/{id}/reports`: Draft completion report snapshot (Report Author).
- `POST /work-orders/{id}/reports/{v}/verify`: Verify report against sources (Report Author).
- `POST /work-orders/{id}/reports/{v}/submit`: Submit report for independent review (Report Author).
- `GET /work-orders/{id}/reports/{v}/pdf`: Download rendered completion report PDF deliverable.
- `GET /work-orders/{id}/acceptance-decisions`: List technical acceptance review records.
- `GET /work-orders/{id}/acceptance-compliance`: RAG-assisted technical acceptance compliance audit against TCVN standards.
- `POST /work-orders/{id}/acceptance-decisions`: Record acceptance, rework, or re-inspection.
- `POST /work-orders/{id}/resume-after-rework`: Resume execution after rework.
- `GET /work-orders/{id}/cost-reconciliation`: View baseline, changes, actuals, and variance.
- `POST /work-orders/{id}/cost-reconciliation`: Reconcile actual cost lines against tasks.
- `POST /work-orders/{id}/close`: Formal administrative closure (`CLOSED`).
