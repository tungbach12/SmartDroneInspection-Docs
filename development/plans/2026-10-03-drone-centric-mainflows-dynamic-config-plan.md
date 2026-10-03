# Drone-Centric 5 Main Flows & Operator Dynamic Configuration Plan

> **Goal:** Refactor the entire `SmartDroneInspection-docs` documentation suite to:
> 1. Downgrade Onboarding, Vetting & Asset CRUD to a **Supporting Flow (SF)**, focusing the Main Flows purely on the core drone inspection transactional lifecycle.
> 2. Create a dedicated **Drone-Centric Main Flow (MF2)** emphasizing **Drone Mission Planning & Airspace Clearance** (GSD calculation, Overlap %, Shot List, `cambay.mod.gov.vn` airspace check, flight permits per *Luật Phòng không nhân dân 2024* & *Nghị định 288/2025/NĐ-CP*).
> 3. Eliminate all hardcoded business values by granting **`PLATFORM_OPERATOR`** the authority to dynamically configure commercial parameters (Commission rate r, Retention rate H, Auto-settlement review days, Dry-run cancellation penalty %, Warranty duration) with a **Contract Snapshot Pattern** protecting active contracts from retroactive changes.
> 4. Grant **`PLATFORM_ADMIN`** technical parameter configuration (YOLO confidence thresholds, MinIO chunk limits).
> 5. Strictly preserve compliance with `error-prevention.md` (5 mandatory exception questions per flow, Verb + Noun use case naming, truthful `Pending` test cases in Report 5, and zero executable code/migration modifications).

---

## I. Cấu trúc Luồng Nghiệp vụ Mới (Supporting Flow + 5 Drone-Centric Main Flows)

### Supporting Flow (SF) — Tiền đề & Quản trị Danh mục (Supporting Setup)
* **SF**: *Đăng ký Doanh nghiệp, Thẩm định Pháp lý Provider & Quản trị Hồ sơ Công trình (Onboarding, Legal Vetting & Asset Master Data)*.
  * Đăng ký tài khoản Client; Thẩm định hồ sơ năng lực Provider bởi `PLATFORM_OPERATOR`.
  * Khai báo hồ sơ tài sản công trình; Quản lý tài liệu kỹ thuật hoàn công.

---

### 5 Main Flows Cốt lõi (Core Transactional Value Chain)
* **MF1 — Yêu cầu Khảo sát, Đấu thầu Báo giá & Ký quỹ Escrow (Survey Request, Quotation Sourcing & Escrow Funding)**
  * Client tạo yêu cầu khảo sát, chọn Provider trực tiếp hoặc phát hành yêu cầu chào giá mở (Open RFQ).
  * Provider Manager xem xét sơ bộ, phản hồi Báo giá (chỉ gồm công bay, kỹ thuật, vật tư di chuyển, VAT — không tính phí Platform AI/MinIO).
  * Hợp đồng điện tử 3 bên được ký kết; Client nạp tiền ký quỹ có điều kiện 100% qua đối tác ngân hàng/trung gian thanh toán có thẩm quyền (NĐ 52/2024/NĐ-CP).
  * **Cơ chế Snapshot**: Khóa cứng mức hoa hồng r và thời hạn nghiệm thu do `PLATFORM_OPERATOR` ban hành tại thời điểm ký kết vào Service Order.

* **MF2 — Lập Kế hoạch Bay Drone Chuyên dụng & Thẩm định Không phận (Drone Mission Planning & Airspace Clearance) 🚀 [FLOW NỔI BẬT DRONE]**
  * **Tính toán trắc địa ảnh**: Xác định độ phân giải mặt đất mục tiêu **GSD (Ground Sampling Distance - mm/pixel)** theo tiêu chuẩn phát hiện vết nứt (ví dụ: vết nứt >= 0.5 mm cần GSD <= 1.0 mm/pixel); tính toán độ cao bay an toàn (AGL) và tỷ lệ chồng phủ ảnh (**Forward/Side Overlap 70%–80%**).
  * **Lập danh mục góc chụp cấu kiện (Structural Shot List & Gimbal Pitch)**: Thiết lập tọa độ waypoint, hướng bay, góc nghiêng camera gimbal (0°, -45°, -90°) tương ứng với từng cấu kiện công trình (mặt đứng, mái, dầm mố).
  * **Thẩm định an toàn không phận số**: Đối chiếu tự động tọa độ bay với bản đồ vùng cấm/hạn chế bay số quốc gia (`cambay.mod.gov.vn` theo QĐ 18/2020/QĐ-TTg).
  * **Kiểm soát pháp lý bay theo Luật PKND 2024**: Provider đính kèm Giấy phép bay Cục Tác chiến - Bộ Tổng Tham mưu; hệ thống kiểm tra mã định danh phương tiện bay của Bộ Quốc phòng và chứng chỉ phi công của Inspector. Provider Manager ký lệnh bay chuyển trạng thái `READY_FOR_FLIGHT`.

* **MF3 — Khảo sát Hiện trường, Thu nạp Telemetry & Phân tích AI YOLO (Flight Survey Execution, Telemetry Capture & AI Defect Verification)**
  * Inspector thực hiện bay khảo sát theo Mission Plan đã phê duyệt; tải ảnh/video lên MinIO qua Web/Mobile.
  * Hệ thống tự động bóc tách **dữ liệu không gian (Spatial Telemetry / EXIF GPS 3D, độ cao, góc gimbal)** và tính mã băm SHA-256 bảo đảm toàn vẹn chứng cứ số.
  * AI YOLO tập trung do Platform cung cấp tự động nhận diện khuyết tật (vết nứt, rỉ sét, bong tróc); tính toán kích thước vật lý thực tế của vết nứt dựa trên GSD đã tính ở MF2.
  * Inspector Xác nhận (Confirm) / Sửa đổi (Modify) / Bác bỏ (Reject) hoặc thêm lỗi thủ công; duyệt chéo độc lập (Peer Review); Provider Manager phát hành Báo cáo Kỹ thuật QA (kích hoạt đồng hồ nghiệm thu tự động).

* **MF4 — Nghiệm thu Báo cáo, Quyết toán Tự động & Trọng tài Xử lý Tranh chấp (Report Acceptance, Commission Settlement & Operator Dispute Resolution)**
  * Client thẩm định báo cáo kỹ thuật trong thời hạn nghiệm thu đã khóa trong hợp đồng (mặc định 5 ngày làm việc do Operator cấu hình).
  * **Quyết toán tự động**: Hết thời hạn mà Client không khiếu nại, hợp đồng tự động nghiệm thu; đối tác thanh toán giải ngân tiền cho Provider sau khi khấu trừ hoa hồng sàn C = r * B (theo tỷ lệ r đã khóa snapshot).
  * **Trọng tài xử lý tranh chấp nội bộ**: Nếu có khiếu nại, tiền ký quỹ lập tức bị đóng băng (`FROZEN_DISPUTED`); `PLATFORM_OPERATOR` đối soát hợp đồng MF1, kế hoạch bay MF2 và dữ liệu telemetry/ảnh MinIO MF3 để ra phán quyết nội bộ theo Platform Terms (Free Reshoot / Hủy & phạt / Bác khiếu nại).

* **MF5 — Xử lý Khiếm khuyết, Đơn hàng Bảo trì & Tiền Bảo lãnh Hoàn công (Defect Rectification, Maintenance Execution & Warranty Retention)**
  * Chuyển các khuyết tật từ báo cáo drone thành đơn hàng sửa chữa công trình.
  * Khóa mức tỷ lệ bảo lãnh hoàn công H (mặc định 10% do Operator cấu hình) và thời hạn bảo hành (mặc định 30 ngày do Operator cấu hình) vào Maintenance Order.
  * Kỹ sư thi công và nạp ảnh đối chứng Before/After bắt buộc.
  * Giải ngân 2 giai đoạn: Giai đoạn 1 giải ngân 100% - H khi nghiệm thu hoàn công; Giai đoạn 2 giải ngân nốt H sau khi hết thời hạn bảo hành không tái hỏng.

---

## II. Phân định Trách nhiệm Cấu hình Động (Dynamic Configuration Policy)

| Loại Tham số | Phân loại | Vai trò Quản lý | Phạm vi & Tác động | Cơ chế Bảo vệ |
| :--- | :--- | :---: | :--- | :--- |
| **Tỷ lệ hoa hồng sàn (`commission_rate` - r)** | Thương mại | **`PLATFORM_OPERATOR`** | Áp dụng chung cho toàn sàn, điều chỉnh theo giai đoạn kinh doanh. | **Contract Snapshot**: Khóa tỷ lệ vào Service Order lúc ký kết; không hồi tố đơn hàng cũ. |
| **Tỷ lệ bảo lãnh bảo trì (`warranty_retention_rate` - H)** | Thương mại | **`PLATFORM_OPERATOR`** | Tỷ lệ phần trăm giữ lại bảo hành hoàn công (mặc định 10%, có thể chỉnh 5%–15%). | Khóa vào Maintenance Order lúc Client duyệt báo giá bảo trì. |
| **Thời hạn nghiệm thu tự động (`auto_settlement_review_days`)** | Nghiệp vụ | **`PLATFORM_OPERATOR`** | Số ngày làm việc Client được quyền rà soát báo cáo trước khi tự động giải ngân (mặc định 5 ngày). | Khóa vào Service Order lúc ký kết. |
| **Phí phạt hủy sát giờ (`dry_run_penalty_rate`)** | Thương mại | **`PLATFORM_OPERATOR`** | Phí phạt Client hủy trong vòng 24h trước giờ bay (mặc định 20% chi phí di chuyển). | Quy định trong Quy chế sàn, snapshot vào điều khoản đơn hàng. |
| **Thời hạn bảo hành tiêu chuẩn (`standard_warranty_days`)** | Nghiệp vụ | **`PLATFORM_OPERATOR`** | Thời gian theo dõi trước khi giải ngân tiền giữ lại bảo hành (mặc định 30 ngày). | Khóa vào Maintenance Order. |
| **Ngưỡng tin cậy AI YOLO (`yolo_confidence_threshold`)** | Kỹ thuật | **`PLATFORM_ADMIN`** | Ngưỡng lọc candidate defects (ví dụ: 0.65, 0.70). | Áp dụng toàn hệ thống cho pipeline suy luận AI của Sàn. |
| **Giới hạn kích thước upload MinIO (`max_upload_size_mb`)** | Kỹ thuật | **`PLATFORM_ADMIN`** | Cấu hình giới hạn phân mảnh upload ảnh/video. | Hạ tầng lưu trữ MinIO. |
| **Mẫu Checklist kiểm định chuẩn (`standard_checklist_templates`)** | Kỹ thuật / Chuẩn | **`PLATFORM_ADMIN`** | Khung danh mục câu hỏi kiểm tra kỹ thuật công trình. | Phiên bản hóa danh mục (versioned catalog). |

---

## III. Kế hoạch Thực thi Chi tiết (7 Tasks)

### Task 1: Tái cấu trúc Tài liệu Nghiệp vụ Core (`project-reference/business-flows.md`)
- [ ] Bổ sung mục **Supporting Flow (SF)** về Đăng ký, Thẩm định Provider & Khai báo tài sản.
- [ ] Viết lại trọn vẹn **MF1 đến MF5** theo kiến trúc Drone-Centric (MF2 chuyên sâu về Mission Planning, GSD, Overlap, Không phận).
- [ ] Bổ sung cơ chế **Cấu hình Động của `PLATFORM_OPERATOR`** và nguyên tắc **Contract Snapshot**.
- [ ] Trả lời đầy đủ **5 câu hỏi ngoại lệ bắt buộc** cho cả 5 Main Flows (`error-prevention.md`).
- [ ] Cập nhật bảng RACI matrix phản ánh rõ SF và MF1–MF5 cho 6 roles.

### Task 2: Cập nhật Thiết kế Cơ sở Dữ liệu (`project-reference/database-design.md`)
- [ ] Bổ sung bảng `platform_configurations` lưu trữ các tham số thương mại do Operator cấu hình (có version, effective_from, updated_by).
- [ ] Bổ sung bảng `drone_mission_plans` và `mission_shot_items` (lưu GSD mục tiêu, độ cao bay AGL, tỷ lệ overlap, gimbal pitch, waypoint tọa độ, giấy phép Cục Tác chiến).
- [ ] Bổ sung các trường Snapshot trong `inspection_service_orders`: `locked_commission_rate`, `locked_review_period_days`, `locked_dry_run_rate`.
- [ ] Bổ sung các trường Snapshot trong `maintenance_orders`: `locked_retention_rate`, `locked_warranty_days`.

### Task 3: Đồng bộ Báo cáo Giới thiệu & Quản lý Dự án (Report 1 & Report 2)
- [ ] Cập nhật Report 1: Bổ sung định vị Drone Mission Planning (GSD, không phận) và vai trò Operator quản trị tham số kinh doanh.
- [ ] Cập nhật Report 2: Bổ sung rủi ro về lập kế hoạch bay drone phức tạp, thay đổi chính sách hoa hồng động và bảo đảm tính bất biến của hợp đồng đang chạy.

### Task 4: Cập nhật SRS Report 3 — Tổng quan & Yêu cầu Người dùng
- [ ] Cập nhật `01-overall-description.md`: Cập nhật Business Rules (BR-01 đến BR-42+) ghi rõ quyền điều chỉnh tham số thương mại của `PLATFORM_OPERATOR` và nguyên tắc Contract Snapshot; bổ sung các quy tắc kỹ thuật về GSD và kiểm tra không phận.
- [ ] Cập nhật `02-user-requirements.md`: Điều chỉnh 32 Use Cases chuẩn định dạng **Verb + Noun**:
  - Thêm Use Case cho Operator: "Configure Commercial Policies", "Audit Platform Configurations".
  - Thêm Use Case cho Provider Manager/Inspector: "Plan Drone Mission", "Authorize Flight Clearance", "Verify Telemetry Integrity".

### Task 5: Cập nhật SRS Report 3 — Yêu cầu Chức năng & NFRs
- [ ] Cập nhật `03-functional-requirements.md`:
  - Bổ sung màn hình cấu hình thương mại cho Operator (`Operator Commercial Settings Screen`).
  - Bổ sung màn hình lập kế hoạch bay drone (`Drone Mission Planning Screen`).
  - Cập nhật ma trận phân quyền 6 roles.
  - Cập nhật chi tiết FE-01 đến FE-08 theo luồng MF1–MF5 mới.
- [ ] Cập nhật `04-non-functional-requirements.md` và `05-requirement-appendix.md`.
- [ ] Ghi nhận thay đổi vào `00-record-of-changes.md` (Version 2.1).

### Task 6: Đồng bộ Báo cáo Kiểm thử Report 5 (Tuân thủ Tuyệt đối `error-prevention.md`)
- [ ] Cập nhật `01-test-cases/test-case-list.md`: Cập nhật mô tả các test case mục tiêu phản ánh Drone Mission Planning, GSD calculation, dynamic commission snapshot (vẫn giữ đúng 33 cases).
- [ ] Cập nhật `02-test-statistics/test-statistics.md`: Giữ vững số liệu 13 Passed (baseline v1), 20 Pending (mục tiêu mới), 0 Failed, coverage 39.4%.
- [ ] Cập nhật 8 file chi tiết trong `03-features/` và README/template layout.

### Task 7: Đồng bộ Kế hoạch Triển khai & Kiểm tra Toàn diện
- [ ] Cập nhật amendment notes trong các file kế hoạch team con (`bach/`, `quoc/`).
- [ ] Chạy `git diff --check` kiểm tra định dạng và khoảng trắng.
- [ ] Kiểm tra xác nhận 3 repository code (`backend`, `frontend`, `mobile`) hoàn toàn không bị chỉnh sửa.

---

## IV. Tiêu chí Nghiệm thu (Acceptance Criteria)
1. Luồng Onboarding & Vetting được hạ xuống thành Supporting Flow (SF), 5 Main Flows (MF1–MF5) thuần túy là chuỗi giá trị giao dịch kiểm định drone.
2. MF2 thể hiện rõ nghiệp vụ đặc thù của Drone (GSD, Overlap, Shot List, `cambay.mod.gov.vn`, giấy phép bay Cục Tác chiến).
3. Tuyệt đối không còn giá trị phần trăm hoặc số ngày nào bị fix cứng trong mô tả nghiệp vụ mà không có cơ chế cấu hình động bởi `PLATFORM_OPERATOR`.
4. Cơ chế Contract Snapshot được thể hiện rõ ràng trong database design và business rules để bảo vệ tính bất biến của hợp đồng.
5. Đáp ứng đầy đủ 5 câu hỏi ngoại lệ cho cả 5 Main Flows theo `error-prevention.md`.
6. Tất cả Use Case giữ đúng chuẩn Verb + Noun.
7. Báo cáo Report 5 giữ nguyên số liệu trung thực, toàn bộ tính năng mục tiêu mới đánh dấu `Pending`.
8. Zero code changes đối với backend, frontend, mobile.
