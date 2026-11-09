# 4 Main Flows (`WF-01` – `WF-04`)

## WF-01 · Đăng ký và thẩm định thiết bị bay của đối tác
*(Precondition: Tài khoản đối tác `INSPECTOR` đã được cấp và kích hoạt)*

1. **`INSPECTOR`** gửi hồ sơ đăng ký thiết bị bay (`Drone`) kèm thông số kỹ thuật và bộ 3 chứng từ pháp lý bắt buộc (`REGISTRATION` — Giấy đăng ký, `OWNERSHIP` — Chứng nhận sở hữu, `INSPECTION` — Giấy kiểm định an toàn) → hệ thống chuyển `PENDING`.
2. **`SYSTEM`** kiểm tra tính đầy đủ của bộ 3 chứng từ, tính duy nhất của số Serial và hiệu lực thời hạn đăng kiểm (**BR-01**).
3. **`MANAGER`** thẩm định thông tin trên 3 chứng từ đối chiếu với thông số kỹ thuật và phê duyệt thiết bị bay (**BR-02**) → hệ thống chuyển `APPROVED` *(nếu chứng từ không hợp lệ thì từ chối sang `REJECTED` kèm lý do bắt buộc)*.
4. **`SYSTEM`** kích hoạt thiết bị bay vào danh sách nguồn lực sẵn sàng điều phối và gửi thông báo kết quả cho **`INSPECTOR`**.

---

## WF-02 · Báo giá, giao kết hợp đồng và điều phối ca kiểm định
*(Precondition: Hệ thống có ít nhất 1 cặp `INSPECTOR` và `DRONE` ở trạng thái `APPROVED`)*

1. **`CUSTOMER`** khai báo công trình (kèm tọa độ GPS, hạng mục cần kiểm tra) và gửi yêu cầu dịch vụ kiểm định một lần hoặc định kỳ → hệ thống chuyển `SUBMITTED`.
2. **`SYSTEM`** kiểm tra tọa độ công trình với dữ liệu không phận (**BR-03**), xác nhận nằm ngoài vùng cấm bay (`NO_FLY_ZONE`) và kích hoạt công trình (`ACTIVE`) *(nếu nằm trong `NO_FLY_ZONE` thì chặn yêu cầu)*.
3. **`MANAGER`** chọn cặp `INSPECTOR` – `DRONE` phù hợp và phát hành Báo giá dịch vụ → hệ thống chuyển `QUOTED`.
4. **`CUSTOMER`** thương lượng điều khoản và chấp thuận Báo giá (**BR-04**) → hệ thống chuyển `QUOTE_ACCEPTED` *(nếu yêu cầu chỉnh giá thì `MANAGER` phát hành phiên bản báo giá mới, bản cũ chuyển sang `SUPERSEDED`)*.
5. **`MANAGER`** ghi nhận Hợp đồng dịch vụ đã ký kết (`CONTRACT_UPLOADED`) và phát lệnh điều phối ca bay (**BR-05**) → hệ thống chuyển `DISPATCHED`.
6. **`SYSTEM`** khóa biểu phí vào đợt bay, khởi tạo lịch kiểm định (`Inspection` → `SCHEDULED`) và gửi thông báo nhận nhiệm vụ cho **`INSPECTOR`**.

---

## WF-03 · Khảo sát hiện trường và xác nhận khuyết tật bằng AI
*(Precondition: Ca kiểm định ở trạng thái `SCHEDULED`; người thực hiện là `INSPECTOR` được phân công)*

1. **`INSPECTOR`** cung cấp Giấy phép bay (`Flight Permit`) của nhiệm vụ và xác nhận đạt danh mục an toàn trước bay (`Pre-flight Checklist`).
2. **`SYSTEM`** kiểm tra điều kiện an toàn (**BR-06**), chuyển nhiệm vụ sang `IN_PROGRESS` và tự động thu thập nhật ký đường bay `MAVLink` từ Mission Planner.
3. **`INSPECTOR`** hoàn tất chuyến bay, đối chiếu hoàn thành các hạng mục công trình cần kiểm tra (`Inspection Items`), xác nhận danh mục an toàn sau bay (`Post-flight Checklist` — bắt buộc ghi rõ lý do nếu có hạng mục/tiêu chí chưa hoàn thành) và nộp bộ hình ảnh/video khảo sát (`Evidence`) (**BR-07**) *(nếu gặp sự cố thời tiết/GPS thì dừng khẩn cấp `ABORTED` kèm lý do để `MANAGER` dời lịch hoặc đổi nguồn lực)*.
4. **`SYSTEM (AI YOLO11)`** phân tích hình ảnh khảo sát, khoanh vùng hư hỏng và sinh danh sách khuyết tật gợi ý (`Finding` → `CANDIDATE`).
5. **`INSPECTOR`** thẩm định từng gợi ý của AI (xác nhận `CONFIRMED`, bác bỏ `REJECTED` hoặc bổ sung lỗi thủ công) và chốt danh sách khuyết tật chuẩn (**BR-08**).
6. **`SYSTEM`** khóa danh sách khuyết tật (`Findings Baseline`), chuyển ca kiểm định sang `FIELD_COMPLETED` và thông báo sẵn sàng lập báo cáo.

---

## WF-04 · Thẩm định báo cáo, nghiệm thu và quyết toán dịch vụ
*(Precondition: Ca kiểm định ở trạng thái `FIELD_COMPLETED` và đã khóa `Findings Baseline`)*

1. **`SYSTEM`** tự động tổng hợp dữ liệu công trình, nhật ký đường bay `MAVLink`, hình ảnh bằng chứng và các khuyết tật `CONFIRMED` thành bản dự thảo báo cáo (`InspectionReport` → `DRAFT`).
2. **`INSPECTOR`** rà soát nhận định chuyên môn và gửi Báo cáo kiểm định lên cấp quản lý → hệ thống chuyển báo cáo sang `SUBMITTED` và ca kiểm định sang `UNDER_REVIEW`.
3. **`MANAGER`** thẩm định độc lập (**BR-09**) và phê duyệt phát hành báo cáo chính thức → hệ thống chuyển `PUBLISHED` *(nếu chưa đạt yêu cầu thì trả về `RETURNED` kèm lý do bắt buộc để `INSPECTOR` hiệu chỉnh và gửi phiên bản mới)*.
4. **`SYSTEM`** kết xuất hồ sơ PDF bất biến, chuyển ca kiểm định sang `COMPLETED` và phát hành Hóa đơn dịch vụ (`ServiceInvoice` → `UNPAID`) cho **`CUSTOMER`**.
5. **`CUSTOMER`** nghiệm thu báo cáo kiểm định (`Accept Report`) và thanh toán phí dịch vụ trực tuyến qua cổng **PayOS (VietQR)** (**BR-10**).
6. **`SYSTEM`** xác nhận thanh toán (`ServiceInvoice` → `PAID`), tự động khấu trừ `VAT (8%)`, `Hoa hồng nền tảng (15%)`, `Thuế TNCN (10%)` và giải ngân thù lao thực nhận (`InspectorPayout` → `SETTLED`) cho **`INSPECTOR`** *(Nhánh phụ: Sau khi tự khắc phục hư hỏng, nếu `CUSTOMER` cần bay kiểm chứng lại thì gửi yêu cầu **Re-inspection** liên kết với báo cáo gốc để quay lại `WF-02` & `WF-03`)*.
