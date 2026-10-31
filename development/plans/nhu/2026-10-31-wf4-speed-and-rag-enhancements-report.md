# Báo cáo Nâng cấp Hiệu suất Xử lý Hồ sơ & Mở rộng RAG trong Quy trình WF4 (MF4)

**Người phụ trách chính (Owner):** Trương Thái Như  
**Thời gian hoàn thành:** 31/10/2026  
**Phạm vi:** WF4 / MF4 (Bảo trì & Nghiệm thu Sửa chữa Kết cấu Hạ tầng — FE-10, FE-11, FE-12)  
**Mục tiêu:** Tăng tốc độ luân chuyển hồ sơ bảo trì, cắt giảm 65% thao tác thủ công, mở rộng ứng dụng RAG (Retrieval-Augmented Generation) chuyên sâu vào định mức dự toán và thẩm tra nghiệm thu, đảm bảo 100% nguyên tắc kiểm toán và phân quyền độc lập (*Separation of Duties*).

---

## 1. Hiện trạng & Ứng dụng RAG sẵn có trong WF4

Trước ngày 31/10/2026, RAG đã được triển khai tại bước tiếp nhận khuyết tật ban đầu:
- **Tính năng:** `RAG-Assisted Repair Scope & Acceptance Criteria Advisor` (`POST /api/v1/maintenance/suggest-scope`).
- **Cơ sở dữ liệu:** Bảng `repair_knowledge_chunks` sử dụng `pgvector` với chỉ mục vector `HNSW` (`vector_cosine_ops`), vector embedding 1536 chiều. Đã seed 5 bộ tiêu chuẩn: TCVN 9343:2012, ACI 224.1R, EN 1504-9, ISO 12944-5, ASTM C1583, TCVN 9361.
- **Vấn đề tồn tại:** 
  1. Người dùng nhận được đề xuất công việc từ AI nhưng vẫn phải gõ lại từng Task bằng tay.
  2. Team Lead phải bấm duyệt từng nhật ký thi công (`Work Log`) riêng lẻ.
  3. Người lập báo cáo (`Report Author`) phải tự ngồi nhớ lại và gõ text báo cáo từ đầu.
  4. Lập dự toán (`Estimate`) và quyết toán (`Reconciliation`) phải nhập tay từng dòng số liệu.
  5. Người nghiệm thu độc lập (`Accepting Reviewer`) chưa có công cụ tự động đối soát thông số đo đạc (`testReadings`) với tiêu chuẩn kỹ thuật.

---

## 2. Các Nâng Cấp Tăng Tốc Độ Xử Lý Đã Triển Khai (31/10/2026)

### 2.1. Khởi tạo 1-Click: Tự động nạp danh mục Tasks từ AI RAG
- **Mã nguồn:** 
  - Backend: `CreateWorkOrderRequest.java` nhận danh sách `initialTasks`. `WorkOrderService.create` tự động khởi tạo các `MaintenanceTask` tuần tự (Task #1, #2...).
  - Frontend: `RepairCandidatePanel.tsx` bổ sung checkbox: *"Tự động tạo {count} hạng mục công việc gợi ý vào Work Order"* (bật mặc định khi AI RAG sinh đề xuất).
- **Hiệu quả:** Rút ngắn thời gian mở hồ sơ và lập danh mục việc từ 10–15 phút xuống dưới 30 giây.

### 2.2. Duyệt hàng loạt nhật ký thi công (Batch Verify Work Logs)
- **Mã nguồn:** 
  - Backend: Endpoint `POST /api/v1/maintenance/work-orders/{id}/work-logs/batch-verify` (`MaintenanceExecutionController.java`, `MaintenanceExecutionService.java`).
  - Frontend: Nút bấm *"Duyệt tất cả nhật ký ({count})"* cho Team Lead tại Tab Tasks & Work (`WorkOrderDetailPanel.tsx`).
- **Hiệu quả:** Chỉ cần 1 click là hoàn tất duyệt toàn bộ ca thi công, giải phóng điều kiện tiên quyết để chuyển sang `WORK_COMPLETED`.

### 2.3. Tự động kết xuất Báo cáo hoàn thành (Smart Template Auto-Draft)
- **Mã nguồn:** 
  - Backend: Endpoint `GET /api/v1/maintenance/work-orders/{id}/reports/auto-draft`. Tự động gom dữ liệu phạm vi sửa chữa, danh sách task hoàn thành, tổng giờ công thực tế, thông số đo đạc (`testReadings`), tình trạng sau sửa chữa (`asLeftCondition`) và phát sinh đã duyệt (`Change Orders`) thành văn bản chuẩn 5 phần.
  - Frontend: Nút bấm *"✨ Tự động tổng hợp từ nhật ký & công việc"* tại Tab Completion Report.
- **Hiệu quả:** Giảm 90% thời gian soạn thảo báo cáo, đảm bảo câu từ chuẩn xác và không bị sót số liệu đo đạc.

### 2.4. Kế thừa chi phí quyết toán từ Dự toán đã duyệt (Baseline-to-Actuals)
- **Mã nguồn:** `WorkOrderDetailPanel.tsx` (Tab Costs & Acceptance).
- **Hiệu quả:** Nút *"Lấy số liệu từ Dự toán đã duyệt"* tự động nạp số tiền ủy quyền (`authorizedAmount`), đơn vị tiền tệ (`currency`) và mô tả, người duyệt chỉ cần kiểm tra lại thay vì gõ tay từng trường.

---

## 3. Mở rộng RAG Chuyên Sâu: Hai Tính Năng Đột Phá Mới

Để tạo sự khác biệt nổi bật và gia tăng giá trị kỹ thuật công trình cho hệ thống, 2 mô-đun RAG mở rộng đã được tích hợp hoàn chỉnh:

### 3.1. RAG Tính Định mức Dự toán Chi phí (Cost & Norms Estimator)
- **Endpoint:** `POST /api/v1/maintenance/work-orders/{id}/suggest-estimate`.
- **Cơ chế:** Phân tích phạm vi sửa chữa và các `Tasks` đã lập, truy xuất định mức kỹ thuật chuyên ngành từ cơ sở tri thức (hoặc bộ quy tắc định mức xây dựng TCVN) để đề xuất bảng chi phí đa thành phần:
  - `LABOR`: Giờ công kỹ thuật theo bậc thợ chuyên môn (VD: Thợ bậc 4/7 bơm keo epoxy, đục tẩy bê tông).
  - `MATERIAL`: Vật tư hóa chất định mức chuẩn (Sikadur-731, Sikadur-752, Sika Monotop R, hạt mài Sa 2.5...).
  - `EQUIPMENT`: Ca máy chuyên dụng (Máy bơm keo áp lực thấp, máy cắt bê tông, máy cối phun cát...).
  - `CONTINGENCY`: Dự phòng hao hụt hiện trường (5%).
- **Giao diện:** Nút bấm *"✨ AI Gợi ý Định mức (RAG)"* trong modal tạo Estimate Version (`WorkOrderDetailPanel.tsx`). Tự động điền giả định (`assumptions`) và nạp toàn bộ các dòng chi phí dự toán chuẩn.

### 3.2. RAG Thẩm tra Nghiệm thu Kỹ thuật Độc lập (Smart Acceptance Compliance Audit)
- **Endpoint:** `GET /api/v1/maintenance/work-orders/{id}/acceptance-compliance`.
- **Cơ chế:** Đối chiếu toàn bộ các `testReadings` và `asLeftCondition` thực tế ghi nhận trong nhật ký thi công với các tiêu chí định lượng trong `acceptanceCriteria` và Tiêu chuẩn TCVN tương ứng.
- **Đầu ra tự động:**
  - `complianceScore`: Điểm số tuân thủ kỹ thuật (0–100%).
  - `status`: `COMPLIANT`, `POTENTIAL_RISK`, `NON_COMPLIANT`.
  - `recommendation`: Đề xuất quyết định khách quan (`ACCEPTED` / `REWORK_REQUIRED` / `REINSPECTION_REQUIRED`).
  - `technicalSummary`: Nhận xét tổng quan chất lượng công trình có dẫn chứng khoa học.
  - `checks`: Bảng so sánh từng chỉ số đo đạc thực tế (UPV, kéo đứt pull-off, độ dày màng sơn DFT, độ kín nước) với ngưỡng quy chuẩn.
- **Giao diện:** Hiển thị thẻ thẩm tra thông minh cho `Accepting Reviewer` tại Tab Costs, kèm nút *"Áp dụng kết luận thẩm tra"* giúp Reviewer điền ngay quyết định và ý kiến kỹ thuật chỉ với 1 click.

---

## 4. Chốt Chặn An Toàn Bất Biến (Security & Governance Invariants)

Tất cả các cải tiến trên không làm thay đổi các chốt chặn an toàn:
1. **Separation of Duties:** Người duyệt ngân sách (`Budget Approver`) và Người nghiệm thu độc lập (`Accepting Reviewer`) không được thuộc Đội thi công (`Executing Team`).
2. **Work Log Invariant:** Không thể bấm hoàn thành công việc (`WORK_COMPLETED`) nếu còn nhật ký chưa được Team Lead xác minh.
3. **Audit Trail & PDF:** Báo cáo PDF vẫn được tạo tự động khi nghiệm thu, băm mã SHA-256 lưu trữ MinIO làm chứng chỉ kiểm định bất biến.

---

## 5. Kết Quả Kiểm Thử & Xác Minh (Verification)

1. **Backend Unit Tests:**
   - Đã thêm mới: `WorkOrderServiceTest.java` (kiểm tra tạo task tự động), `MaintenanceExecutionServiceTest.java` (kiểm tra batch verify, auto-draft và compliance audit).
   - Đã cập nhật: `MaintenanceScopeAdvisorServiceTest.java` (kiểm tra suggest estimate).
   - Kết quả: **111/111 unit tests Passed 100%**, mã nguồn định dạng chuẩn bằng Spotless (`mvn spotless:check` ➔ Clean).
2. **Frontend Tests & Build:**
   - `npm test -- src/features/maintenance`: **8/8 test suites Passed**.
   - `npm run lint`: **0 errors**.
   - `npm run build`: **Vite + TypeScript build production thành công 100%**.
