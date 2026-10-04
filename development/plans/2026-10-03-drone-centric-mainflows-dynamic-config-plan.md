# Drone-Centric 5 Main Flows & Operator Dynamic Configuration Plan

> **Goal:** Refactor the entire `SmartDroneInspection-docs` documentation suite to:
> 1. Downgrade Onboarding, Vetting & Asset CRUD to a **Supporting Flow (SF)**, focusing the Main Flows purely on the core drone inspection transactional lifecycle.
> 2. Create a dedicated **Drone-Centric Main Flow (MF2)** emphasizing **Drone Mission Planning & Airspace Clearance** (mission-specific GSD and overlap targets, Shot List, `cambay.mod.gov.vn` airspace check, flight permits per *Luật Phòng không nhân dân 2024* & *Nghị định 288/2025/NĐ-CP*); technical targets come from the agreed SOW/Mission Plan, not hardcoded global defaults.
> 3. Eliminate all hardcoded business values by granting **`PLATFORM_OPERATOR`** the authority to dynamically configure commercial parameters (uniform commission rate r, retention rate H, auto-settlement review period, cancellation terms, warranty duration) with a **Contract Snapshot Pattern** protecting active contracts from retroactive changes.
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
* **MF1 — Yêu cầu Khảo sát, Đấu thầu Báo giá & Thanh toán có Điều kiện (Survey Request, Quotation Sourcing & Conditional Funding)**
  * Client tạo yêu cầu khảo sát, chọn Provider trực tiếp hoặc phát hành yêu cầu chào giá mở (Open RFQ).
  * Provider Manager xem xét sơ bộ, phản hồi Báo giá (chỉ gồm công bay, kỹ thuật, vật tư di chuyển, VAT — không tính phí Platform AI/MinIO).
  * Hợp đồng điện tử 3 bên được ký kết; khoản nạp trước và điều kiện giải ngân theo policy được cấu hình, chấp thuận và snapshot qua đối tác ngân hàng/trung gian thanh toán phù hợp pháp luật. Không mặc định ký quỹ 100% hoặc coi sản phẩm thanh toán nào cũng hỗ trợ giữ tiền có điều kiện.
  * **Cơ chế Snapshot**: Ghi lại hoa hồng chung `r`, thời hạn nghiệm thu, tỷ lệ nạp trước và chính sách hủy đã công bố/được chấp thuận vào Service Order tại thời điểm ký kết.

* **MF2 — Lập Kế hoạch Bay Drone Chuyên dụng & Thẩm định Không phận (Drone Mission Planning & Airspace Clearance) 🚀 [FLOW NỔI BẬT DRONE]**
  * **Tính toán trắc địa ảnh**: Xác định độ phân giải mặt đất mục tiêu **GSD (Ground Sampling Distance - mm/pixel)** theo tiêu chuẩn phát hiện vết nứt theo yêu cầu độ phân giải đã thỏa thuận trong SOW; tính toán độ cao bay an toàn (AGL) và tỷ lệ chồng phủ ảnh Forward/Side theo cấu kiện, cảm biến và phương án khảo sát đã duyệt. Không áp một ngưỡng mặc định cho mọi công trình.
  * **Lập danh mục góc chụp cấu kiện (Structural Shot List & Gimbal Pitch)**: Thiết lập tọa độ waypoint, hướng bay, góc nghiêng camera gimbal phù hợp với từng cấu kiện và được ghi rõ trong Mission Plan tương ứng với từng cấu kiện công trình (mặt đứng, mái, dầm mố).
  * **Thẩm định an toàn không phận số**: Đối chiếu tự động tọa độ bay với bản đồ vùng cấm/hạn chế bay số quốc gia (`cambay.mod.gov.vn` theo QĐ 18/2020/QĐ-TTg).
  * **Kiểm soát pháp lý bay theo Luật PKND 2024**: Provider đính kèm Giấy phép bay Cục Tác chiến - Bộ Tổng Tham mưu; hệ thống kiểm tra mã định danh phương tiện bay của Bộ Quốc phòng và chứng chỉ phi công của Inspector. Provider Manager ký lệnh bay chuyển trạng thái `READY_FOR_FLIGHT`.

* **MF3 — Khảo sát Hiện trường, Thu nạp Telemetry & Phân tích AI YOLO (Flight Survey Execution, Telemetry Capture & AI Defect Verification)**
  * Inspector thực hiện bay khảo sát theo Mission Plan đã phê duyệt; tải ảnh/video lên MinIO qua Web/Mobile.
  * Hệ thống tự động bóc tách **dữ liệu không gian (Spatial Telemetry / EXIF GPS 3D, độ cao, góc gimbal)** và tính mã băm SHA-256 bảo đảm toàn vẹn chứng cứ số.
  * AI YOLO tập trung do Platform cung cấp tự động nhận diện khuyết tật (vết nứt, rỉ sét, bong tróc); tính toán kích thước vật lý thực tế của vết nứt dựa trên GSD đã tính ở MF2.
  * Inspector Confirm/Modify/Rejects or manually adds findings, then personally verifies and edits the AI-generated report draft against evidence, checklist and SOW. Provider Manager checks deliverable completeness and releases the QA report.

* **MF4 — Nghiệm thu Báo cáo, Quyết toán Tự động & Xử lý Khiếu nại Nội bộ (Report Acceptance, Commission Settlement & Internal Complaint Handling)**
  * Client thẩm định báo cáo kỹ thuật trong thời hạn nghiệm thu được cấu hình và snapshot vào hợp đồng.
  * **Quyết toán theo điều khoản**: Sau khi Client nghiệm thu hoặc điều kiện deemed-acceptance đã thỏa thuận được đáp ứng, đối tác thanh toán xử lý tiền theo chính sách đã khóa và tính hoa hồng chung `C = r × B`.
  * **Xử lý khiếu nại nội bộ**: Nếu khiếu nại hợp lệ, chỉ khoản tiền đối tác có thể giữ theo sản phẩm và hợp đồng mới bị tạm dừng; `PLATFORM_OPERATOR` đối chiếu hợp đồng MF1, kế hoạch bay MF2 và dữ liệu telemetry/ảnh MF3, ra quyết định nội bộ theo Platform Terms, không phải phán quyết trọng tài pháp lý.

* **MF5 — Xử lý Khiếm khuyết, Đơn hàng Bảo trì & Tiền Bảo lãnh Hoàn công (Defect Rectification, Maintenance Execution & Warranty Retention)**
  * Chuyển các khuyết tật từ báo cáo drone thành đơn hàng sửa chữa công trình.
  * Snapshot tỷ lệ bảo lãnh hoàn công H và thời hạn bảo hành do Operator cấu hình vào Maintenance Order.
  * Kỹ sư thi công và nạp ảnh đối chứng Before/After bắt buộc.
  * Giải ngân theo hai mốc đã thỏa thuận: phần không giữ lại sau nghiệm thu hoàn công, phần retention sau thời hạn bảo hành nếu không còn khiếu nại hợp lệ.

---

## II. Phân định Trách nhiệm Cấu hình Động (Dynamic Configuration Policy)

| Loại Tham số | Phân loại | Vai trò Quản lý | Phạm vi & Tác động | Cơ chế Bảo vệ |
| :--- | :--- | :---: | :--- | :--- |
| **Tỷ lệ hoa hồng sàn (`commission_rate` - r)** | Thương mại | **`PLATFORM_OPERATOR`** | Áp dụng chung cho toàn sàn, điều chỉnh theo giai đoạn kinh doanh. | **Contract Snapshot**: Khóa tỷ lệ vào Service Order lúc ký kết; không hồi tố đơn hàng cũ. |
| **Tỷ lệ bảo lãnh bảo trì (`warranty_retention_rate` - H)** | Thương mại | **`PLATFORM_OPERATOR`** | Tỷ lệ phần trăm giữ lại bảo hành hoàn công được Operator cấu hình theo chính sách công bố; không đặt mặc định hay dải giá trị trong tài liệu này. | Khóa vào Maintenance Order lúc Client duyệt báo giá bảo trì. |
| **Thời hạn nghiệm thu tự động (`auto_settlement_review_days`)** | Nghiệp vụ | **`PLATFORM_OPERATOR`** | Số ngày làm việc Client được quyền rà soát báo cáo trước khi tự động giải ngân được Operator cấu hình và snapshot theo hợp đồng. | Khóa vào Service Order lúc ký kết. |
| **Chính sách hủy (`cancellation_policy`)** | Thương mại | **`PLATFORM_OPERATOR`** | Điều kiện, cửa sổ và cơ sở chi phí hủy được Operator cấu hình, công bố và snapshot theo hợp đồng; không đặt sẵn tỷ lệ hay mốc thời gian mặc định. | Quy định trong Quy chế sàn, snapshot vào điều khoản đơn hàng. |
| **Thời hạn bảo hành tiêu chuẩn (`standard_warranty_days`)** | Nghiệp vụ | **`PLATFORM_OPERATOR`** | Thời gian theo dõi trước khi giải ngân tiền giữ lại bảo hành được Operator cấu hình và snapshot theo maintenance order. | Khóa vào Maintenance Order. |
| **Ngưỡng tin cậy AI YOLO (`yolo_confidence_threshold`)** | Kỹ thuật | **`PLATFORM_ADMIN`** | Ngưỡng lọc candidate defects được PLATFORM_ADMIN cấu hình theo model/version và đánh giá validation đã công bố. | Áp dụng toàn hệ thống cho pipeline suy luận AI của Sàn. |
| **Giới hạn kích thước upload MinIO (`max_upload_size_mb`)** | Kỹ thuật | **`PLATFORM_ADMIN`** | Cấu hình giới hạn phân mảnh upload ảnh/video. | Hạ tầng lưu trữ MinIO. |
| **Mẫu Checklist kiểm định chuẩn (`standard_checklist_templates`)** | Kỹ thuật / Chuẩn | **`PLATFORM_ADMIN`** | Khung danh mục câu hỏi kiểm tra kỹ thuật công trình. | Phiên bản hóa danh mục (versioned catalog). |

---

## III. Kế hoạch Thực thi Chi tiết (7 Tasks)

### Task 1: Tái cấu trúc Tài liệu Nghiệp vụ Core (`project-reference/business-flows.md`)
- [ ] Bổ sung mục **Supporting Flow (SF)** về Đăng ký, Thẩm định Provider & Khai báo tài sản.
- [ ] Viết lại trọn vẹn **MF1 đến MF5** theo kiến trúc Drone-Centric (MF2 chuyên sâu về mission-specific GSD, Overlap, Shot List và Không phận; các mục tiêu kỹ thuật được chốt trong SOW/Mission Plan).
- [ ] Bổ sung cơ chế **Cấu hình Động của `PLATFORM_OPERATOR`** và nguyên tắc **Contract Snapshot**.
- [ ] Trả lời đầy đủ **5 câu hỏi ngoại lệ bắt buộc** cho cả 5 Main Flows (`error-prevention.md`).
- [ ] Cập nhật bảng RACI matrix phản ánh rõ SF và MF1–MF5 cho 6 roles.

### Task 2: Cập nhật Thiết kế Cơ sở Dữ liệu (`project-reference/database-design.md`)
- [ ] Bổ sung bảng `platform_configurations` lưu trữ các tham số thương mại do Operator cấu hình (có version, effective_from, updated_by), gồm tỷ lệ hoa hồng thống nhất, tỷ lệ nạp trước, thời hạn nghiệm thu, chính sách hủy, tỷ lệ retention và thời hạn bảo hành; không ghi sẵn giá trị mặc định.
- [ ] Bổ sung bảng `drone_mission_plans` và `mission_shot_items` (lưu GSD mục tiêu, độ cao bay AGL, tỷ lệ overlap, gimbal pitch, waypoint tọa độ, giấy phép Cục Tác chiến).
- [ ] Bổ sung các trường Snapshot trong `inspection_service_orders`: `locked_commission_rate`, `locked_review_period_days`, `locked_cancellation_policy`, `locked_advance_funding_rate`.
- [ ] Bổ sung các trường Snapshot trong `maintenance_orders`: `locked_commission_rate`, `commission_policy_version`, `locked_funding_rate`/`funding_policy_version` khi funding áp dụng, `locked_retention_rate`/`retention_policy_version` khi retention được adopted, và `locked_warranty_days` khi warranty áp dụng.

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
2. MF2 thể hiện rõ nghiệp vụ đặc thù của Drone (GSD, Overlap, Shot List, `cambay.mod.gov.vn`, giấy phép bay Cục Tác chiến); mục tiêu kỹ thuật được xác định theo SOW/Mission Plan, không dùng ví dụ làm default toàn cục.
3. Không dùng tỷ lệ phần trăm, số ngày, thời hạn hủy hoặc ngưỡng kỹ thuật như giá trị mặc định toàn cục; chính sách thương mại do `PLATFORM_OPERATOR` cấu hình, mục tiêu kỹ thuật được chốt theo SOW/Mission Plan, và các giá trị đã chấp thuận được snapshot vào đơn hàng. Nạp trước và retention là tùy chọn theo order/product; thiếu funding yêu cầu thì không tạo funding gate. Callback partner phải có identity idempotent.
4. Cơ chế Contract Snapshot được thể hiện rõ ràng trong database design và business rules để bảo vệ tính bất biến của hợp đồng.
5. Đáp ứng đầy đủ 5 câu hỏi ngoại lệ cho cả 5 Main Flows theo `error-prevention.md`.
6. Tất cả Use Case giữ đúng chuẩn Verb + Noun.
7. Báo cáo Report 5 giữ nguyên số liệu trung thực, toàn bộ tính năng mục tiêu mới đánh dấu `Pending`.
8. Zero code changes đối với backend, frontend, mobile.
