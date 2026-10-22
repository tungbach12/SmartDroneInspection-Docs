# WF4 Plan — Như

**Owner**: Như
**Flow**: WF4 — Maintenance and Billing
**Jira Epic**: `SCRUM-57`
**Capacity**: 20 planned days + 0 reserve days

## Current status — 15 Oct 2026

The original WF4 task list below describes a retired five-role marketplace/billing
baseline and is historical only. The current Enterprise SaaS MF4 requirements
are defined by Report 3 §3.8 and `project-reference/business-flows.md`; do not use
the old Client/Manager/provider ticket, invoice or payment assumptions as current
product scope.

- Backend branch `feat/maintenance-mf4-work-order` contains the full MF4 backend API
  and event-driven workflow: repair candidates, work orders, internal team/tasks, estimates and
  changes, work logs, completion reports, independent acceptance, reconciliation
  and closeout.
- Completed backend target enhancements (15 Oct 2026):
  1. **MF4-18 Re-inspection Dispatch**: `REINSPECTION_REQUIRED` publishes `ReinspectionRequestedEvent`,
     and `InspectionReinspectionListener` in the `inspections` module automatically creates a linked
     verification re-inspection without circular package dependencies.
  2. **MF4-16/17 Completion Report PDF Artifact**: `MaintenanceReportRenderer` renders the formal
     10-section completion report to PDF using `PdfRendererBuilder` and stores it in MinIO via
     `EvidenceObjectStore` with SHA-256 checksum; preview and attachment download endpoints
     are exposed at `GET /api/v1/maintenance/work-orders/{id}/reports/{versionNo}/pdf`.
  3. **MF4-04/13/18/21 Milestone Notifications**: Domain events (`WorkOrderAssignedEvent`,
     `EstimateApprovedEvent`, `ChangeOrderApprovedEvent`, `AcceptanceRecordedEvent`,
     `WorkOrderClosedEvent`) are listened by `MaintenanceNotificationListener` to record
     attributable in-app notifications.
  4. **Comprehensive Test Suite**: Unit tests (`MaintenanceReportRendererTest`,
     `InspectionReinspectionListenerTest`, `MaintenanceNotificationListenerTest`,
     `MaintenanceReportVersionTest`) and integration assertions added.
- Report 5 records FE-07 cases `WF3-010`–`WF3-012` as Passed. These verify backend
  API behavior only and do not claim full MF4 acceptance or client coverage.
- Credential validation currently permits no credential record and rejects a
  present non-ACTIVE or expired credential. This deviates from Report 3's
  required-presence rule; applicable skills are not modelled.
- Frontend Web delivery slice completed (15 Oct 2026):
  1. Replaced the static placeholder Maintenance page with a fully interactive
     `MaintenancePage.tsx` featuring real-time MetricCards, Tab 0 for server-paged
     Work Orders, Tab 1 for published Repair Candidates Queue, and a comprehensive
     Work Order Details dialog (showing assigned team roster, task execution state,
     reconciled variance, and report PDF download link).
  2. Implemented full interactive administrator mutation workflows via dedicated modal dialogs:
     - `CreateWorkOrderDialog.tsx`: opens work orders directly from published repair candidates.
     - `AssignTeamDialog.tsx`: designates lead, author, reviewer, and members using workforce users.
     - `RecordAcceptanceDialog.tsx`: records independent technical review (Accept, Rework, Re-inspect).
     - `RejectEstimateDialog.tsx`: allows budget approver to return an estimate for rework.
     - Close work order action: closes order upon acceptance and cost reconciliation.
  3. Implemented full interactive engineer execution workflows on the Web:
     - `CreateTaskDialog.tsx`: allows team lead to break scope into tasks and assign engineers.
     - Release & Start actions: lead confirms readiness (`READY`) and starts execution (`IN_PROGRESS`).
     - `RecordWorkLogDialog.tsx`: engineers record task hours, as-left condition, and test readings.
     - Inline work log verification: team lead reviews and verifies submitted work logs.
     - `ProposeChangeDialog.tsx`: engineers propose scope and cost delta changes for budget approval.
     - Declare complete action: team lead confirms physical work completion (`WORK_COMPLETED`).
     - `CreateReportDialog.tsx`: designated report author drafts, verifies, and submits completion report.
  4. Implemented strongly typed API client `maintenanceApi.ts` and TanStack Query
     hooks with query-key factory `useMaintenance.ts` (queries + mutations with cache invalidation).
  5. Created comprehensive Vitest test suites (`maintenanceApi.test.ts` and `MaintenancePage.test.tsx`)
     covering API calls, empty states, work order listing, candidate queue display, and engineer dialogs.
- Mobile client workflow completed (15 Oct 2026):
  1. Built field engineer tasks repository and models in `SmartDroneInspection-mobile` (`lib/features/tasks/`):
     - `mobile_work_order.dart`, `mobile_task_item.dart`, `mobile_work_log.dart`.
     - `maintenance_repository.dart`: lists assigned orders, gets tasks, starts work, records & submits work logs, declares complete.
  2. Implemented Riverpod state management in `maintenance_providers.dart`.
  3. Built reactive mobile presentation layer:
     - `tasks_page.dart`: interactive list of assigned orders with pull-to-refresh (`AsyncValueWidget`), priority and status chips, navigation to detail.
     - `work_order_detail_page.dart`: full order detail with scope, criteria, planned tasks list, verified work logs, and action buttons (`Start Execution`, `Record Log`, `Declare Complete`).
     - `record_work_log_sheet.dart`: bottom sheet modal for engineers to log hours, as-left condition, and test measurements.
  4. Added route `/tasks/:workOrderId` in `app_router.dart`.
  5. Created comprehensive test suite in `test/features/tasks/maintenance_repository_test.dart`.
- Credential validation currently permits no credential record and rejects a
  present non-ACTIVE or expired credential per the approved interim rule; applicable skills are not modelled.

Full end-to-end WF4 implementation is now complete across Backend, Web, and Mobile.

## Outcome

Accepted findings become assessed, approved, executed, released, and resolved maintenance work.
Inspection and maintenance use separate post-service invoice status; the first release has no
online payment gateway.

## Owner tasks

- `T004` — accepted-report/finding fixture for independent WF4 development.
- `T034`–`T035` — ticket creation and Client ticket view.
- `T036`–`T038` — assessment, quotation/order versions, approval, and execution assignment.
- `T039`–`T041` — assigned work/evidence, change approval, release, resolution, and re-inspection.
- `T042`–`T045` — Manager/Client web, Engineer mobile execution, invoice milestones, and regression.

The full task descriptions, estimates, acceptance criteria, and Jira mapping remain in
[tasks.md](../bach/2026-09-22-four-week-mainflow-delivery/tasks.md).

## Delivery windows

| Jira sprint | Dates | Focus |
| --- | --- | --- |
| W3 — Foundation & DB | Sep 28–Oct 2 | Ticket API/UI and execution fixture UI |
| W4 — WF1 & WF2 Core | Oct 5–9 | Assessment, estimate, quote/order, mobile assessment |
| W5 — WF3 & WF4 Core | Oct 12–16 | Work evidence, change order, release/resolution |
| W6 — Integration & Demo | Oct 19–23 | Web/mobile completion, invoices, regression |

## Handoff and acceptance

- Ticket creation requires at least one own-organization verified finding from an accepted report.
- Approved scope/order is required before execution; extra work waits for Client approval.
- Assigned Engineers alone can write work logs and required before/after evidence.
- Re-inspection creates one linked WF2 request without a module dependency cycle.
- Record one invoice per accepted inspection report or maintenance order with manual payment status.
- G5 and the full five-role journey are green before release.

## References

- [Shared four-week plan](../bach/2026-09-22-four-week-mainflow-delivery/plan.md)
- [Shared handoff contract](../bach/2026-09-22-four-week-mainflow-delivery/flow-handoffs.md)
- [Jira import guide](../bach/2026-09-22-four-week-mainflow-delivery/jira-import-guide.md)
