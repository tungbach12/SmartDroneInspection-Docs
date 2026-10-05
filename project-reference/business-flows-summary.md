---
title: "SmartDroneInspection - Tóm tắt Quy trình Nghiệp vụ & Vai trò (MF1–MF5)"
document_type: business-flow-summary
purpose: "Bản tóm tắt tinh gọn về 6 vai trò chính và 5 luồng nghiệp vụ cốt lõi (MF1–MF5) của hệ thống SmartDroneInspection, dễ hiểu, giữ nguyên thuật ngữ chuyên môn."
version: "1.0"
updated: 2026-10-05
---

# SmartDroneInspection - Tóm tắt Quy trình Nghiệp vụ & Vai trò (MF1–MF5)

Tài liệu này cung cấp cái nhìn tổng quan, súc tích và mạch lạc về cách thức hoạt động của nền tảng SmartDroneInspection. Toàn bộ quy trình tập trung vào việc kết nối giữa **Khách hàng sở hữu công trình (Client)** và **Đơn vị cung cấp dịch vụ bay drone / bảo trì (Provider)**, hỗ trợ bởi công nghệ AI và đối tác thanh toán bảo đảm.

---

## I. Hệ thống 6 Vai trò Chính (6 Canonical Roles)

Hệ thống phân định rõ quyền hạn và trách nhiệm theo 3 khối (Platform Governance, Customer, Service Provider):

| STT | Mã Role (English) | Tên gọi tiếng Việt | Trách nhiệm chính trong hệ thống |
| :---: | :--- | :--- | :--- |
| 1 | `PLATFORM_ADMIN` | Quản trị viên Kỹ thuật & Hệ thống | Quản lý tài khoản người dùng, phân quyền bảo mật, thiết lập checklist kỹ thuật mẫu, cấu hình hệ thống AI YOLO và giám sát hạ tầng lưu trữ MinIO. Không can thiệp vào giá cả hay giải quyết khiếu nại. |
| 2 | `PLATFORM_OPERATOR` | Quản trị viên Vận hành Sàn | Thẩm định hồ sơ năng lực pháp lý của Provider; ban hành các chính sách thương mại (tỷ lệ hoa hồng $r$, thời hạn nghiệm thu, tỷ lệ bảo lãnh); giám sát thanh toán có điều kiện và chủ trì hòa giải khiếu nại nội bộ giữa hai bên. |
| 3 | `CLIENT` | Khách hàng / Chủ tài sản | Đăng ký và quản lý tài sản công trình; tạo yêu cầu khảo sát (chỉ định hoặc phát thầu mở RFQ); ký Hợp đồng điện tử (Service Order); nạp tiền đảm bảo qua cổng thanh toán; nghiệm thu báo cáo và đặt hàng sửa chữa bảo trì. |
| 4 | `PROVIDER_MANAGER` | Quản lý Đơn vị Dịch vụ | Khai báo hồ sơ công ty và đội bay; nhận yêu cầu RFQ và lập Báo giá dịch vụ; đính kèm giấy phép/hồ sơ bay hợp lệ; phân công phi công; kiểm tra tính đầy đủ của báo cáo và ký phát hành báo cáo QA chính thức gửi Khách hàng. |
| 5 | `INSPECTOR` | Phi công Drone / Kỹ thuật viên | Tính toán thông số chụp ảnh kỹ thuật (GSD, Overlap, Shot List); chịu trách nhiệm an toàn bay tại hiện trường (Pilot-in-Command); bay bổ sung (Re-flight) khi ảnh lỗi; xác minh các khuyết tật do AI đề xuất; tự hoàn thiện và ký xác nhận bản thảo báo cáo. |
| 6 | `MAINTENANCE_ENGINEER` | Kỹ sư Sửa chữa / Bảo trì | Khảo sát thực tế các hư hỏng; lập phương án kỹ thuật và dự toán sửa chữa; lập phiếu phát sinh (Change Order) nếu gặp sự cố ngầm; trực tiếp thi công; chụp bắt buộc cặp ảnh đối chứng Trước/Sau (Before/After) để nghiệm thu. |

---

## II. Chi tiết 5 Luồng Nghiệp vụ Giao dịch Cốt lõi (MF1 – MF5)

---

### MF1 — Yêu cầu Khảo sát, Đấu thầu & Nạp tiền Đảm bảo Thanh toán (Survey Request, Smart RFQ & Conditional Payment)

**Mục tiêu**: Khách hàng phát yêu cầu kiểm định, chọn nhà cung cấp phù hợp, ký hợp đồng điện tử và nạp khoản tiền đảm bảo qua đối tác thanh toán được cấp phép trước khi bay.

* **MF1-01 (Tạo yêu cầu RFQ)**: `CLIENT` tạo yêu cầu khảo sát công trình. Có thể **chỉ định đích danh** một Provider hoặc **phát thầu mở (Open RFQ)** kèm theo mục tiêu kiểm tra (nứt bê tông, gỉ sét, thấm dột), danh mục cấu kiện và tiến độ mong muốn.
* **MF1-02 (Bộ lọc thông minh)**: `System` tự động rà soát và chỉ gửi thư mời chào thầu (RFQ Invitation) tới các Provider đáp ứng đủ tiêu chí: khu vực hoạt động, có trang thiết bị/cảm biến phù hợp, phi công có chứng chỉ hợp lệ và đã được xác thực (`VERIFIED`).
* **MF1-03 (Lập Báo giá - Quotation)**: `PROVIDER_MANAGER` nghiên cứu yêu cầu và gửi Báo giá chi tiết (công phi công, thiết bị, đi lại, thuế). *Lưu ý: Provider không được tính thêm phí AI hay phí lưu trữ đám mây của Sàn vào báo giá.*
* **MF1-04 (Chấp thuận Báo giá)**: `CLIENT` so sánh các báo giá, trao đổi điều chỉnh nếu cần và chọn báo giá phù hợp nhất để chấp thuận.
* **MF1-05 (Khởi tạo Hợp đồng điện tử)**: `System` tự động tạo Đơn dịch vụ điện tử (**Inspection Service Order**), khóa cố định (snapshot) các điều khoản: tỷ lệ nạp tiền đảm bảo $D$, tỷ lệ hoa hồng $r$, thời hạn nghiệm thu $T_{rev}$ và chính sách hủy.
* **MF1-06 (Ký số & Nạp tiền đảm bảo)**: `CLIENT` và `PROVIDER_MANAGER` ký xác nhận hợp đồng điện tử. `CLIENT` nạp số tiền đảm bảo vào tài khoản chỉ định của đối tác thanh toán được cấp phép (trạng thái `FUNDED_IN_PARTNER_ESCROW`). Hợp đồng có hiệu lực để bắt đầu chuẩn bị bay.

#### Các tình huống xử lý ngoại lệ (MF1):
* **Hết hạn không có ai báo giá**: Hệ thống báo Khách hàng mở rộng phạm vi tìm kiếm hoặc điều chỉnh lại ngân sách/tiến độ.
* **Thời tiết xấu bất khả kháng**: Hai bên thỏa thuận dời lịch trên hệ thống mà không bị phạt hay vi phạm tiến độ.
* **Khách hàng hủy chuyến bay trước giờ xuất phát**: Áp dụng quy chế bồi hoàn đã chốt trong hợp đồng: trừ chi phí chuẩn bị thực tế hợp lý cho bên bay, tiền còn lại trả về cho Khách hàng.

---

### MF2 — Lập Kế hoạch Bay, Tiêu chuẩn Kỹ thuật & Hồ sơ Bay (Mission Planning & Flight Compliance)

**Mục tiêu**: Chuẩn bị đầy đủ các thông số chụp ảnh để đảm bảo phát hiện được vết nứt nhỏ nhất, đồng thời kiểm tra đầy đủ hồ sơ pháp lý và an toàn bay trước khi cất cánh.

* **MF2-01 (Đề xuất khoảng cách chụp theo GSD mục tiêu)**: `INSPECTOR` nhập kích thước khuyết tật nhỏ nhất cần tìm (ví dụ vết nứt $\ge 1.0\text{ mm}$ yêu cầu độ phân giải mặt đất $\text{GSD} \le 0.5\text{ mm/pixel}$) cùng thông số camera. Hệ thống tự động tính toán và đề xuất khoảng cách chụp ảnh tối ưu.
* **MF2-02 (Thiết lập độ chồng phủ ảnh - Overlap)**: `INSPECTOR` cài đặt tỷ lệ chụp gối đầu (chồng phủ dọc $\ge 75\%$, chồng phủ ngang $\ge 60\%$) để đảm bảo ảnh chụp không bị điểm mù và đủ điều kiện dựng lại vị trí hư hỏng.
* **MF2-03 (Lập danh mục chụp & góc camera - Shot List & Gimbal)**: `INSPECTOR` lên danh mục từng cấu kiện cần chụp, góc nghiêng camera (Gimbal Pitch: $0^\circ, -45^\circ, -90^\circ$) và đường bay tự động (Waypoints) hoặc sơ đồ bay tay có hướng dẫn.
* **MF2-04 (Kiểm tra cảnh báo không phận)**: `System` đối chiếu tọa độ khu vực bay với dữ liệu vùng cấm/hạn chế bay để đưa ra cảnh báo sớm giúp phi công chủ động đường bay an toàn.
* **MF2-05 (Kiểm soát hồ sơ bay)**: `PROVIDER_MANAGER` đính kèm giấy phép/chấp thuận bay cần thiết của cơ quan thẩm quyền, thông tin định danh phương tiện bay và chứng chỉ phi công theo quy định hiện hành.
* **MF2-06 (Cam kết an toàn bay - Safety Sign-off)**: `INSPECTOR` trực tiếp kiểm tra thực địa (vật cản, thời tiết, tầm nhìn), ký xác nhận an toàn bay (Pilot-in-Command). `PROVIDER_MANAGER` phê duyệt ban hành Kế hoạch bay. Hệ thống chuyển trạng thái sang **`READY_FOR_FLIGHT`**.

#### Các tình huống xử lý ngoại lệ (MF2):
* **Không được cấp phép bay**: Kế hoạch bay bị dừng; Provider thông báo Khách hàng để xin gia hạn hoặc hủy hợp đồng theo điều khoản bất khả kháng.
* **Thiết bị không đáp ứng độ nét yêu cầu**: Hệ thống nhắc nhở phi công đổi ống kính hoặc camera đạt chuẩn trước khi duyệt bay.

---

### MF3 — Bay Khảo sát, Kiểm soát Chất lượng Ảnh, AI Nhận diện & Phát hành Báo cáo (Field Survey, Quality Gate, AI Analysis & QA Release)

**Mục tiêu**: Thực hiện chuyến bay an toàn, kiểm tra chất lượng ảnh ngay tại công trường, phát hiện hư hỏng sơ bộ bằng AI YOLO, con người kiểm chứng lại và xuất báo cáo chính thức.

* **MF3-01 (Thực hiện bay hiện trường)**: `INSPECTOR` kích hoạt phiên bay trên ứng dụng, kiểm tra an toàn trước bay (Pre-flight Check) và điều khiển drone chụp đầy đủ danh mục cấu kiện theo kế hoạch.
* **MF3-02 (Tải ảnh lên hệ thống)**: `INSPECTOR` tải toàn bộ ảnh/video gốc độ phân giải cao lên kho lưu trữ MinIO của hệ thống bằng cơ chế tải phân đoạn (Chunked Upload).
* **MF3-03 (Bóc tách dữ liệu không gian & Chống giả mạo)**: `System` tự động trích xuất thông tin bay (Telemetry: tọa độ GPS 3D, độ cao, góc chụp, thời gian) và tính mã băm **SHA-256** cho từng bức ảnh để bảo vệ tính toàn vẹn của bằng chứng.
* **MF3-04 (Cổng kiểm tra chất lượng ảnh - Evidence Quality Gate)**: Hệ thống tự động quét nhanh để phát hiện ảnh mờ (blur), ảnh thiếu sáng hoặc thiếu góc chụp quan trọng. Nếu phát hiện lỗi, `INSPECTOR` tiến hành **bay bổ sung / bay bù (Re-flight)** ngay tại hiện trường trước khi ra về.
* **MF3-05 (AI YOLO quét ứng viên lỗi)**: Hệ thống AI của Sàn tự động phân tích ảnh, khoanh vùng các hư hỏng (nứt bê tông, gỉ thép, bong tróc) và ước lượng kích thước ban đầu (chiều dài, độ rộng vết nứt) dưới dạng danh sách **Ứng viên lỗi (Defect Candidates)** kèm khung bao (Bounding Box).
* **MF3-06 (Chuyên gia thẩm định - Human-in-the-loop)**: `INSPECTOR` xem xét từng ảnh: bấm **Xác nhận (Confirm)**, **Sửa kích thước/vị trí (Modify)**, hoặc **Bác bỏ (Reject)** lỗi AI nhận diện sai; tự bổ sung các lỗi AI bỏ sót (Manual Finding) bằng công cụ đo đạc chính xác.
* **MF3-07 (Trợ lý LLM soạn bản thảo)**: Hệ thống LLM tổng hợp ảnh, tọa độ và các hư hỏng đã được phi công xác nhận để tự động soạn ra bản thảo Báo cáo kỹ thuật ban đầu.
* **MF3-08 (Phi công tự kiểm tra & ký tên)**: `INSPECTOR` (với tư cách tác giả báo cáo) đọc lại bản thảo, chuẩn hóa câu chữ, kết luận nguyên nhân và ký điện tử xác nhận bản báo cáo hoàn thiện.
* **MF3-09 (Ký phát hành báo cáo QA)**: `PROVIDER_MANAGER` kiểm tra tính đầy đủ theo hợp đồng, ký phát hành Báo cáo Chính thức (Final QA Report) gửi cho Khách hàng. Hệ thống bắt đầu tính thời hạn nghiệm thu $T_{rev}$.

#### Các tình huống xử lý ngoại lệ (MF3):
* **Drone gặp sự cố khi đang bay (yếu pin, mất sóng)**: Phi công kích hoạt chế độ tự quay về hạ cánh an toàn (Fail-safe Return-to-Home), lập biên bản sự cố trên ứng dụng và hẹn lịch bay lại.
* **Thời tiết chuyển xấu bất ngờ (mưa gió)**: Phi công lập tức thu hồi drone, lưu lại các ảnh đã chụp thành công và xếp lịch bay bù phần còn thiếu.
* **Hệ thống AI tạm thời gián đoạn**: Chuyển sang cơ chế làm thủ công (Manual Fallback), phi công tự đánh dấu lỗi trên ảnh để không làm trễ hạn giao báo cáo cho khách.

---

### MF4 — Nghiệm thu Báo cáo, Quyết toán & Xử lý Khiếu nại (Report Acceptance, Settlement & Internal Dispute Resolution)

**Mục tiêu**: Khách hàng kiểm tra kết quả kiểm định, giải ngân tiền dịch vụ theo điều khoản hợp đồng hoặc tham gia hòa giải nội bộ nếu có khúc mắc kỹ thuật.

* **MF4-01 (Khách hàng thẩm định)**: `CLIENT` mở báo cáo trên Web/Mobile, xem hình ảnh sắc nét, vị trí hư hỏng trên mô hình 3D và số đo vết nứt. Bắt đầu đếm ngược thời hạn nghiệm thu $T_{rev}$.
* **MF4-02a (Nghiệm thu đạt)**: Nếu đồng ý với kết quả kiểm định, `CLIENT` bấm **"Nghiệm thu (Accept)"**.
* **MF4-02b (Tự động nghiệm thu theo hợp đồng)**: Nếu hết thời hạn $T_{rev}$ mà Khách hàng không có phản hồi và không gửi yêu cầu làm rõ hay khiếu nại, hệ thống kích hoạt **Nghiệm thu mặc định (Auto-Acceptance)** đúng theo thỏa thuận hợp đồng để tránh ngâm vốn của bên cung cấp dịch vụ.
* **MF4-03 (Giải ngân & Xuất hóa đơn)**: Hệ thống gửi lệnh sang cổng thanh toán: chuyển tiền dịch vụ ròng $(B - C)$ cho Provider và chuyển phí hoa hồng $C$ cho Sàn. Đồng thời, `PROVIDER_MANAGER` xuất hóa đơn GTGT dịch vụ cho `CLIENT`, và Nền tảng xuất hóa đơn phí sàn cho Provider.
* **MF4-04 (Yêu cầu làm rõ kỹ thuật - Clarification Loop)**: Nếu có điểm chưa rõ, `CLIENT` gửi yêu cầu làm rõ trên hệ thống. `PROVIDER_MANAGER` và `INSPECTOR` rà soát ảnh gốc, cập nhật giải trình hoặc đính chính báo cáo để Khách hàng nghiệm thu lại.
* **MF4-05 (Mở khiếu nại/tranh chấp)**: Trường hợp có sai sót nghiêm trọng (chụp sai lệch thông số, bỏ sót khuyết tật lớn, drone va quẹt làm hỏng công trình), một trong hai bên bấm **"Mở Tranh chấp"** và nộp bằng chứng.
* **MF4-06 (Tạm dừng thanh toán)**: Hệ thống ghi nhận trạng thái tranh chấp (`FROZEN_DISPUTED`) và gửi yêu cầu tạm giữ khoản tiền liên quan sang đối tác thanh toán (nếu cổng thanh toán hỗ trợ cơ chế này).
* **MF4-07 (Sàn chủ trì hòa giải nội bộ)**: `PLATFORM_OPERATOR` mở phiên hòa giải: đối chiếu hợp đồng ban đầu, dữ liệu bay, ảnh gốc và mã băm SHA-256. Nếu cần, có thể yêu cầu bên thứ ba độc lập kiểm tra kỹ thuật.
* **MF4-08 (Thực thi kết quả hòa giải)**: `PLATFORM_OPERATOR` đưa ra kết quả xử lý: (1) yêu cầu Provider bay chụp bổ sung; (2) hoàn tiền một phần hoặc toàn bộ cho Khách hàng; hoặc (3) đóng khiếu nại và giải ngân nếu khiếu nại không có cơ sở.

#### Các tình huống xử lý ngoại lệ (MF4):
* **Không đồng ý với kết quả hòa giải của Sàn**: Hòa giải của Sàn là giải pháp nội bộ để xử lý giao dịch. Nếu không tìm được tiếng nói chung, các bên có toàn quyền khởi kiện vụ việc ra Tòa án hoặc Trọng tài thương mại (VIAC) theo quy định của pháp luật.

---

### MF5 — Đơn hàng Bảo trì, Thi công Sửa chữa & Bảo hành (Defect Rectification, Maintenance & Retention)

**Mục tiêu**: Chuyển các khuyết tật từ báo cáo kiểm định thành đơn sửa chữa thực tế, kiểm soát phát sinh chi phí, nghiệm thu qua ảnh đối chứng Trước/Sau và bảo hành hoàn công.

* **MF5-01 (Tạo phiếu yêu cầu sửa chữa)**: `CLIENT` tích chọn các khuyết tật cần xử lý từ Báo cáo MF4 (ví dụ vết nứt dầm bê tông, rỉ sét lan can) để tạo **Phiếu yêu cầu bảo trì (Maintenance Ticket)**.
* **MF5-02 (Lập phương án kỹ thuật & Báo giá)**: `MAINTENANCE_ENGINEER` khảo sát thực tế, phân loại hư hỏng, chọn vật tư chuyên dụng (keo epoxy, vữa sửa chữa polyme, sơn chống gỉ) và lên dự toán chi phí. `PROVIDER_MANAGER` gửi báo giá chi tiết cho Khách hàng.
* **MF5-03 (Ký hợp đồng bảo trì & Nạp tiền)**: `System` tạo Đơn dịch vụ bảo trì (**Maintenance Work Order**), khóa cố định tỷ lệ giữ lại bảo hành $H$ (nếu có) và thời hạn bảo hành $T_{war}$. `CLIENT` nạp tiền đảm bảo qua cổng thanh toán.
* **MF5-04 (Thi công & Nạp ảnh Trước/Sau)**: `MAINTENANCE_ENGINEER` tiến hành thi công sửa chữa theo đúng thiết kế. **Bắt buộc chụp và nạp cặp ảnh đối chứng Trước và Sau khi sửa (Before/After Evidence)** kèm nhật ký vật tư lên hệ thống.
* **MF5-05 (Xử lý phát sinh hư hỏng ngầm - Change Order)**: Nếu trong lúc đục phá phát hiện hư hỏng ngầm nghiêm trọng vượt quá dự tính (cốt thép rỉ mục), kỹ sư dừng ngay phần việc đó, chụp ảnh hiện trạng và lập **Yêu cầu Thay đổi (Change Order)**. Khách hàng xem xét và phê duyệt bổ sung chi phí trước khi làm tiếp.
* **MF5-06 (Khách hàng nghiệm thu hoàn công)**: `CLIENT` kiểm tra trực tiếp hoặc đối chiếu cặp ảnh Trước/Sau và nhật ký vật tư trên ứng dụng; ký biên bản nghiệm thu nếu công việc đạt chất lượng.
* **MF5-07 (Thanh toán đợt 1 & Bắt đầu tính bảo hành)**: Cổng thanh toán giải ngân phần tiền thi công chính cho Provider; giữ lại phần trăm bảo lãnh hoàn công $H$ (thường từ 5%–10%) theo hợp đồng. Kích hoạt đồng hồ tính thời gian bảo hành $T_{war}$.
* **MF5-08 (Tất toán tiền bảo lãnh bảo hành)**: Hết thời gian bảo hành $T_{war}$, nếu công trình không phát sinh hư hỏng lại, hệ thống gửi chỉ thị giải ngân nốt phần tiền bảo lãnh $H$ cho đơn vị bảo trì. Đóng phiếu bảo trì thành công.

#### Các nhánh xử lý phát sinh (MF5):
* **Chất lượng sửa chữa chưa đạt (Rework Loop)**: Nếu ảnh Sau thi công cho thấy vết nứt chưa kín, màu sắc vật liệu lem nhem: Khách hàng từ chối nghiệm thu. Kỹ sư phải làm lại cho đúng cam kết mà không được tính thêm phí phát sinh (nếu lỗi do thi công).
* **Bay drone kiểm tra lại sau sửa chữa (Post-repair Re-inspection)**: Với vị trí trên cao nguy hiểm, Khách hàng có thể đặt thêm một yêu cầu bay drone mới để ghi hình nghiệm thu chất lượng sửa chữa từ trên không.

---

## III. Bảng Tổng hợp Ma trận Phân công Trách nhiệm (RACI Matrix)

| Nghiệp vụ / Luồng cốt lõi | `PLATFORM_ADMIN` | `PLATFORM_OPERATOR` | `CLIENT` | `PROVIDER_MANAGER` | `INSPECTOR` | `MAINTENANCE_ENGINEER` |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **MF1: Tiếp nhận RFQ & Chốt Báo giá** | - | Tham vấn (C) | Phê duyệt (A) | Thực hiện (R) | - | - |
| **MF1: Ký Hợp đồng & Nạp tiền Đảm bảo** | Theo dõi (I) | Tham vấn (C) | Phê duyệt (A) | Thực hiện (R) | - | - |
| **MF2: Lập Kế hoạch Bay (GSD, Overlap, Shot List)** | - | - | Theo dõi (I) | Phê duyệt (A) | Thực hiện (R) | - |
| **MF2: Hồ sơ Bay & Ký Cam kết An toàn** | Theo dõi (I) | Tham vấn (C) | Theo dõi (I) | Phê duyệt (A) | Ký an toàn (R) | - |
| **MF3: Bay Hiện trường & Tải ảnh MinIO** | - | - | Theo dõi (I) | Theo dõi (I) | Chịu trách nhiệm (A/R) | - |
| **MF3: Thẩm định lỗi AI & Ký tên Báo cáo** | - | - | - | Theo dõi (I) | Tác giả ký (A/R) | - |
| **MF3: Ký phát hành Báo cáo Chính thức (QA)** | - | - | Theo dõi (I) | Phê duyệt ký (A) | Tác giả (R) | - |
| **MF4: Nghiệm thu Báo cáo & Lập Hóa đơn** | Theo dõi (I) | Tham vấn (C) | Nghiệm thu (A) | Xuất HĐ (R) | - | - |
| **MF4: Hòa giải Tranh chấp Sàn** | Theo dõi (I) | Chủ trì (A/R) | Tham gia (C) | Tham gia (C) | Tham gia (C) | - |
| **MF5: Phương án Kỹ thuật & Báo giá Sửa chữa** | - | - | Phê duyệt (A) | Quản lý (R) | - | Khảo sát (C) |
| **MF5: Thi công Trước/Sau & Báo phát sinh** | - | - | Phê duyệt (A) | Theo dõi (I) | - | Thực hiện (A/R) |
| **MF5: Nghiệm thu Hoàn công & Tất toán Bảo hành** | Theo dõi (I) | Giải ngân (R) | Nghiệm thu (A) | Theo dõi (I) | - | Theo dõi (I) |

*Ghi chú*:
* **R (Responsible)**: Người trực tiếp thực hiện công việc.
* **A (Accountable)**: Người chịu trách nhiệm phê duyệt và kết quả cuối cùng.
* **C (Consulted)**: Người được hỏi ý kiến hoặc phối hợp cung cấp dữ liệu.
* **I (Informed)**: Người nhận thông báo kết quả.
