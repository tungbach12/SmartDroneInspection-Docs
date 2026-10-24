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

- **RAG-Assisted Repair Scope & Acceptance Criteria Advisor (23 Oct 2026)**:
  1. **Knowledge Base & pgvector (V29)**: Created `repair_knowledge_chunks` table with `vector(1536)`
     embeddings, category index, and HNSW cosine distance index (`vector_cosine_ops`). Seeded 5 standard
     civil/infrastructure repair guidelines:
     - TCVN 9343:2012 / ACI 224.1R for concrete crack epoxy injection (UPV >= 90%, pull-off >= 1.5 MPa).
     - TCVN 9343:2012 / EN 1504-9 for spalling breakout, rebar Sa 2 rust removal, and polymer mortar.
     - ISO 12944-5 / AASHTO for steel corrosion abrasive blasting (Sa 2.5) and 3-coat protective system.
     - TCVN 9343:2012 / ASTM C1583 for hydrophilic PU pressure injection water leakage control.
     - TCVN 9361:2012 / AASHTO for expansion joint sealant and settlement monitoring.
  2. **Hexagonal Architecture & Spring Modulith Compliance**:
     - Declared `@NamedInterface("spi")` in `com.smartdroneinspection.maintenance.spi.package-info.java`.
     - Defined `MaintenanceScopeAdvisorPort` outbound SPI in `maintenance::spi`.
     - Implemented `MaintenanceScopeAdvisorClient` in `infrastructure.ai` using Spring `RestClient`
       against OpenAI-compatible `/v1/chat/completions` with strict JSON schema response format.
     - Bound properties via `@ConfigurationProperties("app.maintenance-advisor")`.
     - Added `"maintenance::spi"` to `infrastructure`'s allowed Modulith dependencies.
  3. **Zero-Downtime Deterministic Fallback**:
     - Built `DeterministicScopeFallback` component that categorizes defects into standard engineering
       domains and returns actionable methodology and quantifiable acceptance criteria when external
       AI inference is disabled or unreachable.
     - Orchestrated in `MaintenanceScopeAdvisorService` with multi-tenant check and fallback activation.
     - Exposed endpoint `POST /api/v1/maintenance/suggest-scope` with `@PreAuthorize("hasAnyRole('ORG_ADMIN', 'MAINTENANCE_ENGINEER')")`.
  4. **Frontend UI Integration**:
     - Added "AI Suggest Scope & Criteria (RAG)" button with `AutoAwesomeOutlined` icon in
       `RepairCandidatePanel.tsx`'s "Open work order" modal.
     - Automatically populates `correctiveScope` and `acceptanceCriteria`, while rendering reference
       standard chips (e.g., `[TCVN 9343:2012]`, `[ISO 12944-5]`) for engineering traceability.

- **WF4 End-to-End Defect Remediation & Verification (23 Oct 2026)**:
  1. **Fixed Cost Reconciliation Task Reference**: Corrected `CostsTab` in `WorkOrderDetailPanel.tsx`
     to bind actual cost lines to planned tasks (`taskId`) rather than finding ID, resolving the
     `400 COST_LINE_TASK_UNKNOWN` error and unblocking `markCostsReconciled` and work order closure.
  2. **Implemented Team Lead Work Log Verification**: Added `useVerifyWorkLog` mutation and inline
     "Verify work log" action in `WorkOrderDetailPanel.tsx`, allowing team leads to verify submitted
     logs and satisfying `markWorkCompleted`'s prerequisite.
  3. **Added State-Guarded Action Buttons**: Updated engineer transitions in `WorkOrderDetailPanel.tsx`
     to disable buttons incompatible with the current order status, preventing 409 conflict errors.
  4. **Hardened Budget Approver Validation**: Added validation in `WorkOrderService.create` ensuring
     `budgetApproverUserId` is an active `ORG_ADMIN` belonging to the caller's organization.
  5. **Protected Closed Work Order Immutability**: Added status guards across `createTask`,
     `createEstimateVersion`, `recordWork`, and `proposeChange` to throw `409 WORK_ORDER_CLOSED`
     if an order has reached terminal closure.
  6. **Formal PDF Artifact Download**: Integrated PDF report download link in `WorkOrderDetailPanel.tsx`
     pointing to `GET /api/v1/maintenance/work-orders/{id}/reports/{versionNo}/pdf`.

Full end-to-end WF4 implementation is now complete and hardened across Backend, Web, and Mobile.

---

## Detailed Personal Work Log & Timeline — Trương Thái Như

| Tuần / Giai đoạn | Ngày thực hiện | Hạng mục công việc & Đầu ra cụ thể | Jira / Mã Task | Trạng thái |
| :--- | :--- | :--- | :--- | :--- |
| **Tuần 1: Khởi động & Lập kế hoạch** | 07/09 – 11/09/2026 | • Phân tích đối sánh các giải pháp quản lý kiểm định hiện có (`Existing Solutions Benchmark`).<br>• Lập bảng quản trị rủi ro & kế hoạch ứng phó (`Risk Register & Response Plan`).<br>• Rà soát chất lượng template và kiểm tra chéo báo cáo Report 1 & Report 2. | [SCRUM-23](https://capstonefall26.atlassian.net/browse/SCRUM-23)<br>[SCRUM-28](https://capstonefall26.atlassian.net/browse/SCRUM-28)<br>[SCRUM-26](https://capstonefall26.atlassian.net/browse/SCRUM-26) | ✅ Hoàn thành 100% |
| **Tuần 2: Thiết kế Quy trình WF4** | 14/09 – 20/09/2026 | • Thiết kế luồng nghiệp vụ WF4: Tiếp nhận khuyết tật, đánh giá hiện trường, thi công sửa chữa.<br>• Soạn thảo slide bối cảnh, bài toán, giải pháp và trách nhiệm các tác nhân trong hệ thống. | [SCRUM-38](https://capstonefall26.atlassian.net/browse/SCRUM-38)<br>[SCRUM-42](https://capstonefall26.atlassian.net/browse/SCRUM-42)<br>[SCRUM-49](https://capstonefall26.atlassian.net/browse/SCRUM-49) | ✅ Hoàn thành 100% |
| **Tuần 3: Thiết kế Cơ sở dữ liệu** | 21/09 – 02/10/2026 | • Thiết kế và khởi tạo lược đồ cơ sở dữ liệu WF4: Bảng `maintenance_work_orders`, `maintenance_tasks`, `maintenance_work_logs`, `maintenance_cost_lines`.<br>• Tích hợp migration Flyway ban đầu cho luồng bảo trì. | [SCRUM-46](https://capstonefall26.atlassian.net/browse/SCRUM-46) | ✅ Hoàn thành 100% |
| **Tuần 4: Tái cấu trúc Enterprise SaaS** | 03/10 – 09/10/2026 | • Tái cấu trúc WF4 từ mô hình sàn marketplace sang mô hình **Enterprise SaaS nội bộ** theo Report 3 §3.8.<br>• Thiết lập ma trận phân quyền độc lập (Separation of Duties): Tách biệt người duyệt ngân sách, đội thi công và người nghiệm thu kỹ thuật. | `REWORK-WF4`<br>[SCRUM-57](https://capstonefall26.atlassian.net/browse/SCRUM-57) | ✅ Hoàn thành 100% |
| **Tuần 5: Lập trình Backend API Slice** | 10/10 – 15/10/2026 | • Xây dựng Backend API slice: Khởi tạo work order từ repair candidates, phân công team, lập task, lập & duyệt dự toán (Estimate), đề xuất thay đổi (Change Order), nghiệm thu và quyết toán.<br>• Soạn thảo tài liệu thiết kế giao diện Web & Mobile (`2026-10-10-mf4-web-mobile-design.md`). | `T034`–`T041`<br>[SCRUM-57](https://capstonefall26.atlassian.net/browse/SCRUM-57) | ✅ Hoàn thành 100% |
| **Tuần 6: Hoàn thiện Web, Mobile & Test Suites** | 16/10 – 18/10/2026 | • **Backend:** Triển khai cơ chế Event Modulith tái kiểm định (`ReinspectionRequestedEvent`), xuất báo cáo PDF (`MaintenanceReportRenderer`), lắng nghe thông báo (`MaintenanceNotificationListener`).<br>• **Web:** Xây dựng toàn bộ giao diện `MaintenancePage.tsx` và `WorkOrderDetailPanel.tsx` với TanStack Query và Material UI.<br>• **Mobile:** Xây dựng màn hình nhiệm vụ Flutter (`tasks_page.dart`, `work_order_detail_page.dart`, `record_work_log_sheet.dart`) với Riverpod.<br>• **Testing:** Xây dựng 25 bài test tích hợp `MaintenanceApiIntegrationTest.java` (đạt 25/25 Passed). | `T042`–`T045`<br>`WF3-010`–`WF3-012` | ✅ Hoàn thành 100% |
| **Tuần 7: Tích hợp RAG AI & Vá lỗi toàn diện** | 19/10 – 23/10/2026 | • **RAG Maintenance Scope Advisor:** Tạo migration `V29__repair_knowledge_base.sql`, chỉ mục `pgvector` HNSW, SPI `MaintenanceScopeAdvisorPort`, Client gọi OpenAI API, bộ sinh quy tắc `DeterministicScopeFallback` và nút bấm **✨ AI Suggest Scope & Criteria** trên Web.<br>• **Vá lỗi luồng WF4:** Sửa triệt để 6 bugs (lỗi task cost reconciliation, nút verify work log cho Lead, status guards chống lỗi 409, validate budget approver, immutability closed order, tải file PDF).<br>• **Hồ sơ báo cáo:** Soạn thảo 3 tài liệu kỹ thuật chuyên sâu (`mf4-rag-scope-advisor-design.md`, `mf4-api-and-contracts.md`, `mf4-verification-and-bug-fixes.md`). | [SCRUM-57](https://capstonefall26.atlassian.net/browse/SCRUM-57)<br>FE-07 / MF4 | ✅ Hoàn thành 100% |

---

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
