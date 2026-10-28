# Phân công vẽ sơ đồ dự án SmartDroneInspection (Bản chuẩn hóa theo Report 1, 2, 3)

Tài liệu căn cứ:
- **Report 1: Project Introduction (Mục 1.2 - 12 Features, 5 Roles & Governance)**
- **Report 2: Project Management Plan (Mục 1.1 WBS, 1.2 Scope & Mục 4 RACI Responsibility Matrix)**
- **Report 3: Software Requirement Specification (Mục 2 User Requirements & Phụ lục 5.1 Business Rules/RACI)**
- **Report 4: Software Design Document (Mục 1 Architecture, Mục 2 Database & Mục 3 Detailed Design)**
- Kho mã nguồn sơ đồ: `diagrams/mermaid/` và file vẽ tổng hợp: `diagrams/smartdrone-use-cases.drawio`

> ⏰ **THỜI HẠN HOÀN THÀNH (DEADLINE): Trước Thứ 7 Tuần 8 (31/10/2026)**
> Đã được ghi nhận vào hệ thống theo dõi tiến độ tuần (`reports/weekly-project-reports/tasks-import.csv`).

---

## 1. Phân bổ phạm vi & Tính năng phụ trách (Feature Ownership)

Mỗi thành viên phụ trách **3 Feature lớn (tương ứng 6 chức năng WBS)** và các sơ đồ kiến trúc/hệ thống tương ứng:

| Thành viên | Mã sinh viên | 3 Feature đảm nhận chính | Trọng tâm sơ đồ đảm nhận |
| :--- | :---: | :--- | :--- |
| **Trần Tùng Bách** | **SE180220** | **FE-01, FE-08, FE-09** | System Context, System Architecture, Database ERD (31 tables), sơ đồ Auth, AI YOLO11, Báo cáo & PDF |
| **Trương Thái Như** | **SE180082** | **FE-10, FE-11, FE-12** | **Use Case Diagram (toàn hệ thống - không chia nhỏ)**, Screens Flow, Backend Package Diagram, toàn bộ sơ đồ Module Bảo trì & RAG Advisor |
| **Trần Hoàng Trung Hiếu** | **SE184212** | **FE-02, FE-03, FE-04** | Toàn bộ 4 State Machine / Lifecycle Diagrams, sơ đồ Nhân sự, Thuê drone/PayPal, Thông báo outbox |
| **Phùng Trung Quốc** | **SE170027** | **FE-05, FE-06, FE-07** | Toàn bộ 4 Activity Diagrams (Quy trình nghiệp vụ WF-01..04), sơ đồ Điều phối, Bản đồ cấm bay, Giấy phép bay, Field Session |

---

## 2. Chi tiết phân công sơ đồ cho từng thành viên

### 👤 1. Trần Tùng Bách (SE180220)
* **Tính năng đảm nhận:**
  - **FE-01: Authentication & Access Control** (Đăng ký tổ chức, Argon2id sign-in, JWT/Refresh token, 5-role RBAC)
  - **FE-08: Evidence Management & AI Defect Detection** (Tải ảnh MinIO, trích xuất GPS/EXIF, YOLO11 AI defect detection, xác thực finding)
  - **FE-09: Inspection Reporting & Publication** (Tạo dự thảo báo cáo bằng AI/Thủ công, duyệt báo cáo, xuất PDF bất biến, bàn giao bảo trì)

| STT | Tên sơ đồ | Loại | Mã tệp Mermaid (`diagrams/mermaid/`) / Vị trí tài liệu |
| :---: | :--- | :---: | :--- |
| 1 | **System Context Diagram** | Context | `01_report-3-..._system-context-diagram_076430d8b186.mmd` *(SRS 1.1)* |
| 2 | **System Architecture Diagram** | Architecture | `29_report-4-..._system-architecture-diagram_1847a5137a52.mmd` *(SDD 1.1)* |
| 3 | **Database Entity Relationship Diagram (ERD)** | ERD | `04_...` / `31_report-4-..._database-entity-relationship-diagram-erd_8100b531f290.mmd` *(SRS 3.1.5 / SDD 2.0)* |
| 4 | **Identity, Workforce and Subscription Class Diagram** *(phần Auth/User)* | Class | `36_report-4-..._identity-workforce-and-subscription-class-diagra_b306a9c86f64.mmd` *(SDD 3.1.1)* |
| 5 | **User Authentication Sequence Diagram** | Sequence | `37_report-4-..._user-authentication-sequence-diagram_0a420defa049.mmd` *(SDD 3.1.2)* |
| 6 | **YOLO11 Defect Detection & Finding Verification Class Diagram** | Class | `50_report-4-..._yolo11-defect-detection-and-finding-verification_64eb1d90feeb.mmd` *(SDD 3.8.1)* |
| 7 | **YOLO11 Defect Detection & Verification Sequence Diagram** | Sequence | `51_report-4-..._yolo11-defect-detection-and-verification-sequenc_436962a7b8b8.mmd` *(SDD 3.8.2)* |
| 8 | **Inspection Report Authoring, Review & PDF Publication Class Diagram** | Class | `52_report-4-..._inspection-report-authoring-review-and-pdf-publi_e00807180de7.mmd` *(SDD 3.9.1)* |
| 9 | **Report Synthesis, Review & Immutable Publication Sequence Diagram** | Sequence | `53_report-4-..._report-synthesis-review-and-immutable-publicatio_2065932a94b4.mmd` *(SDD 3.9.2)* |

---

### 👤 2. Trương Thái Như (SE180082)
* **Tính năng đảm nhận:**
  - **FE-10: Maintenance Planning & AI Scope Advisory** (Tiếp nhận lỗi hỏng, pgvector RAG tư vấn tiêu chuẩn TCVN/EN/ISO, lập Work Order, phân công đội ngũ)
  - **FE-11: Cost Estimation & Repair Execution** (Dự toán chi phí 3 thành phần, duyệt ngân sách, quản lý Change Order, ghi nhận nhật ký thi công)
  - **FE-12: Maintenance Acceptance & Cost Closure** (Báo cáo hoàn thành PDF, nghiệm thu kỹ thuật độc lập, quyết toán chênh lệch chi phí, đóng Work Order)

| STT | Tên sơ đồ | Loại | Mã tệp Mermaid (`diagrams/mermaid/`) / Vị trí tài liệu |
| :---: | :--- | :---: | :--- |
| 1 | **Use Case Diagram (Toàn hệ thống - Thống nhất 1 sơ đồ hoàn chỉnh)** | Use Case | `02_report-3-..._use-case-diagram_f568970e5ba2.mmd` *(tab "use cases" trong `diagrams/smartdrone-use-cases.drawio` - SRS 2.0)* |
| 2 | **Screens Flow Diagram** | Screen Flow | `03_report-3-..._screens-flow-diagram_351dade920d7.mmd` *(SRS 3.1.1)* |
| 3 | **Backend Subsystem Package Diagram** | Package | `30_report-4-..._backend-subsystem-package-diagram_0fa0880aa8fb.mmd` *(SDD 1.2)* |
| 4 | **Maintenance Work Order, RAG Advisor & Cost Control Class Diagram** | Class | `55_report-4-..._maintenance-work-order-rag-advisor-and-cost-cont_8b41a0e47679.mmd` *(SDD 3.10.1)* |
| 5 | **FE-10: Work Order Planning & AI RAG Scope Advisory Sequence Diagram** | Sequence | Tách từ `56_...` *(SDD 3.10.2: Triage finding, gợi ý tiêu chuẩn, phân công đội ngũ)* |
| 6 | **FE-11: Cost Estimation Approval & Change Order Sequence Diagram** | Sequence | Tách từ `56_...` *(SDD 3.11.2: Lập dự toán, OM duyệt ngân sách độc lập & Change Order)* |
| 7 | **FE-11: Field Repair Execution & Work Log Verification Sequence Diagram** | Sequence | Tách từ `56_...` *(SDD 3.11.2: Bắt đầu thi công, ghi nhật ký, Lead xác thực)* |
| 8 | **FE-12: Completion Report, Technical Acceptance & Cost Reconciliation Sequence Diagram** | Sequence | Tách từ `56_...` *(SDD 3.12.2: Xuất PDF hoàn thành có SHA-256, nghiệm thu & quyết toán)* |

---

### 👤 3. Trần Hoàng Trung Hiếu (SE184212)
* **Tính năng đảm nhận:**
  - **FE-02: Workforce & Subscription Management** (Cấp tài khoản nhân sự, khai báo bằng lái bay, thanh toán gói Enterprise qua Chuyển khoản & PayPal)
  - **FE-03: Asset & Drone Fleet Management** (Danh mục tài sản, trắc địa GPS, hồ sơ kỹ thuật MinIO, đội drone nội bộ & Thuê thiết bị drone từ Platform)
  - **FE-04: Recurring Schedule & Notifications** (Lịch kiểm định định kỳ neo theo múi giờ, tự sinh lịch 14 ngày, thông báo Outbox phi đồng bộ)

| STT | Tên sơ đồ | Loại | Mã tệp Mermaid (`diagrams/mermaid/`) / Vị trí tài liệu |
| :---: | :--- | :---: | :--- |
| 1 | **Subscription and Drone Equipment Lease State Machines** | State | `32_report-4-..._subscription-and-drone-equipment-lease-state-mac_d532e1bb2148.mmd` *(SDD 2.0)* |
| 2 | **Inspection, FieldSession & InspectionReport State Machine** | State | `33_report-4-..._inspection-fieldsession-and-inspectionreport-sta_53a33f372cdf.mmd` *(SDD 2.0)* |
| 3 | **InspectionReport Version Lifecycle State Machine Diagram** | State | `34_report-4-..._inspectionreport-version-lifecycle-state-machine_4400d944dca4.mmd` *(SDD 2.0)* |
| 4 | **MaintenanceWorkOrder 12-State Lifecycle Diagram** | State | `35_report-4-..._maintenanceworkorder-12-state-lifecycle-diagram_1750d55011cc.mmd` *(SDD 2.0)* |
| 5 | **Workforce Provisioning & Pilot License Sequence Diagram** | Sequence | `38_report-4-..._workforce-provisioning-and-pilot-license-sequenc_f01a93088565.mmd` *(SDD 3.2.2)* |
| 6 | **PayPal Subscription Payment & Webhook Capture Sequence Diagram** | Sequence | `39_report-4-..._paypal-subscription-payment-and-webhook-capture-_18cdcd15e4f4.mmd` *(SDD 3.2.3)* |
| 7 | **Asset, Drone Fleet & Drone Equipment Leasing Class Diagram** | Class | `40_report-4-..._asset-drone-fleet-and-drone-equipment-leasing-cl_5efd1e2bdde2.mmd` *(SDD 3.3.1)* |
| 8 | **Drone Equipment Leasing & Fleet Provisioning Sequence Diagram** | Sequence | `41_report-4-..._drone-equipment-leasing-and-fleet-provisioning-s_65adc355e88c.mmd` *(SDD 3.3.2)* |
| 9 | **Notification Inbox & Event Listeners Class Diagram** | Class | `42_report-4-..._notification-inbox-and-event-listeners-class-dia_43ef662062fa.mmd` *(SDD 3.4.1)* |
| 10 | **Event-Driven Transactional Outbox Notification Sequence Diagram** | Sequence | `43_report-4-..._event-driven-transactional-outbox-notification-s_0e6cc48673be.mmd` *(SDD 3.4.2)* |

---

### 👤 4. Phùng Trung Quốc (SE170027)
* **Tính năng đảm nhận:**
  - **FE-05: Mission Dispatch & Airspace Advisory** (Lập lịch kiểm định đột xuất, kiểm tra xung đột nguồn lực, bản đồ vùng cấm bay & hạn chế bay OpenStreetMap)
  - **FE-06: Flight Readiness & Field Execution** (Cổng tải giấy phép bay self-service, kiểm tra bằng lái, ghi nhận phiên bay thực địa Web/Mobile)
  - **FE-07: Operational Dashboard & Schedule Calendar** (Dashboard phân tích vận hành theo vai trò, lịch làm việc Inspector dạng Calendar, giao diện song ngữ)

| STT | Tên sơ đồ | Loại | Mã tệp Mermaid (`diagrams/mermaid/`) / Vị trí tài liệu |
| :---: | :--- | :---: | :--- |
| 1 | **WF-01 Activity Diagram: Enterprise Onboarding, Leasing & Scheduling** | Activity | `44_report-4-..._wf-01-activity-diagram-enterprise-onboarding-dro_26036e59e988.mmd` *(SDD 3.4.3)* |
| 2 | **WF-02 Activity Diagram: Mission Dispatch, Permit Gate & Execution** | Activity | `49_report-4-..._wf-02-activity-diagram-mission-dispatch-flight-p_b38950c713f6.mmd` *(SDD 3.6.3)* |
| 3 | **WF-03 Activity Diagram: AI Defect Detection & Report Publication** | Activity | `54_report-4-..._wf-03-activity-diagram-ai-defect-detection-repor_c8f1710d6cb7.mmd` *(SDD 3.9.3)* |
| 4 | **WF-04 Activity Diagram: Maintenance Work Order Lifecycle** | Activity | `57_report-4-..._wf-04-activity-diagram-maintenance-work-order-li_12bbeb320003.mmd` *(SDD 3.12.3)* |
| 5 | **Inspection Mission, Recurring Schedule & Permit Gate Class Diagram** | Class | `45_report-4-..._inspection-mission-recurring-schedule-and-permit_e1af3b4245e9.mmd` *(SDD 3.5.1)* |
| 6 | **Mission Dispatch & Self-Service Permit Upload Sequence Diagram** | Sequence | `46_report-4-..._mission-dispatch-and-self-service-permit-upload-_4ec4bbad15f8.mmd` *(SDD 3.5.2)* |
| 7 | **Field Session & Evidence Management Class Diagram** | Class | `47_report-4-..._field-session-and-evidence-management-class-diag_44ec52e3b942.mmd` *(SDD 3.6.1)* |
| 8 | **Field Flight Session & Evidence Upload Sequence Diagram** | Sequence | `48_report-4-..._field-flight-session-and-evidence-upload-sequenc_c480adaed363.mmd` *(SDD 3.6.2)* |

---

## 3. Tổng hợp số lượng sơ đồ chốt

| Thành viên | Số lượng | Feature đảm nhận (WBS / RACI) | Trọng tâm sơ đồ chính |
| :--- | :---: | :--- | :--- |
| **Trần Tùng Bách** | **9** | **FE-01, FE-08, FE-09** | System Context, Architecture, 31-table ERD + Luồng Auth, AI YOLO11, Báo cáo |
| **Trương Thái Như** | **8** | **FE-10, FE-11, FE-12** | **Use Case tổng hoàn chỉnh (không chia)**, Screens Flow, Package + Luồng Bảo trì/RAG |
| **Trần Hoàng Trung Hiếu** | **10** | **FE-02, FE-03, FE-04** | 4 State Machine lớn + Module Nhân sự, Thuê drone/PayPal, Thông báo |
| **Phùng Trung Quốc** | **8** | **FE-05, FE-06, FE-07** | 4 Activity Diagram quy trình lớn (WF-01..04) + Module Dispatch, Giấy phép bay, Field Session |
| **TỔNG CỘNG** | **35** | **12 Features (FE-01..12)** | Phân chia công bằng, chuẩn xác theo phân công chức năng trong Reports |
