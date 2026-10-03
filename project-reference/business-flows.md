---
title: "SmartDroneInspection Multi-Provider Business Flows"
document_type: business-flow-reference
purpose: "Đặc tả chi tiết Luồng Bổ trợ (SF) và 5 Luồng nghiệp vụ cốt lõi (MF1–MF5) chuyên sâu Drone cho Nền tảng Kiểm định Hạ tầng nhiều Nhà cung cấp (Multi-Provider Platform)"
version: "2.1"
updated: 2026-10-03
---

# SmartDroneInspection Multi-Provider Business Flows (v2.1)

> Tài liệu này là đặc tả chuẩn mực về Luồng Bổ trợ (Supporting Flow - SF) và **5 Luồng nghiệp vụ giao dịch cốt lõi (MF1–MF5)** của nền tảng SmartDroneInspection. Toàn bộ thiết kế được xây dựng dựa trên mô hình Nền tảng số trung gian (Intermediary Platform), kiến trúc chuyên sâu về **Nhiệm vụ Khảo sát Drone (Drone Mission Planning & Telemetry)**, cơ chế Hợp đồng điện tử, Dòng tiền Ký quỹ có điều kiện (Escrow), chính sách **Cấu hình Động của `PLATFORM_OPERATOR`**, Trọng tài xử lý tranh chấp nội bộ sàn, tuân thủ nghiêm ngặt Hướng dẫn tránh lỗi Capstone (`error-prevention.md`) và căn cứ theo hệ thống pháp luật Việt Nam mới nhất.

---

## I. Căn cứ Pháp lý Việt Nam Áp dụng

> **Phạm vi pháp lý:** Đây là bản thiết kế mục tiêu của dự án đồ án. Các văn bản dưới đây là khung tham chiếu đang được rà soát; không được suy luận rằng nền tảng đã hoạt động, đã tuân thủ, đã tích hợp ngân hàng/đơn vị thanh toán, hoặc đã được cấp bất kỳ giấy phép nào.

1. **Luật Phòng không nhân dân 2024 (Luật số 49/2024/QH15, hiệu lực từ 01/07/2025), được sửa đổi bởi Luật số 98/2025/QH15, hướng dẫn bởi Nghị định 198/2025/NĐ-CP và Nghị định 288/2025/NĐ-CP**:
   - Khung pháp lý bắt buộc để kiểm tra đăng ký định danh phương tiện bay không người lái (UAV) do Bộ Quốc phòng cấp, chứng chỉ/giấy phép điều khiển phương tiện bay của phi công (Inspector), giấy phép bay do Cục Tác chiến - Bộ Tổng Tham mưu cấp và kiểm soát không phận bay.
   - Không áp dụng Nghị định 36/2008/NĐ-CP và Nghị định 79/2011/NĐ-CP như văn bản duy nhất còn hiệu lực.
2. **Quyết định số 18/2020/QĐ-TTg & Cổng thông tin Vùng cấm bay (`cambay.mod.gov.vn`)**:
   - Tra cứu tham khảo công khai về khu vực cấm bay, khu vực hạn chế bay số quốc gia. Việc triển khai chuyến bay thực tế bắt buộc phải kiểm tra giấy phép bay và ranh giới không phận có thẩm quyền.
3. **Luật Giao dịch điện tử 2023 (Luật số 20/2023/QH15, hiệu lực từ 01/07/2024)**:
   - Dùng làm căn cứ thiết kế Hợp đồng điện tử 3 bên và quản lý thông điệp dữ liệu số.
   - Hệ thống lưu trữ MinIO, dữ liệu không gian GPS 3D, mã băm SHA-256 và timestamp hỗ trợ bảo đảm tính toàn vẹn kỹ thuật và truy xuất nguồn gốc; không tự suy diễn là chứng cứ pháp lý mặc nhiên nếu chưa qua quy trình tố tụng/giám định tư pháp.
4. **Luật Bảo vệ quyền lợi người tiêu dùng 2023 (Luật số 19/2023/QH15, hiệu lực từ 01/07/2024)** và Nghị định 55/2024/NĐ-CP:
   - Căn cứ thiết kế trách nhiệm công khai quy chế sàn, minh bạch thông tin Provider và cơ chế tiếp nhận, xử lý khiếu nại. Phán quyết nội bộ của Sàn không thay thế quyền khởi kiện ra Tòa án hoặc trọng tài thương mại (VIAC).
5. **Khung pháp luật thương mại điện tử hiện hành từ 01/07/2026**:
   - Đối chiếu **Luật Thương mại điện tử 2025 (Luật số 122/2025/QH15)** và **Nghị định 248/2026/NĐ-CP** (thay thế/bổ sung Nghị định 52/2013/NĐ-CP và Nghị định 85/2021/NĐ-CP).
6. **Thanh toán, bảo đảm thanh toán và ký quỹ**:
   - Tích hợp tài khoản đảm bảo thanh toán với ngân hàng thương mại hoặc tổ chức trung gian thanh toán được cấp phép theo **Nghị định 52/2024/NĐ-CP** và Điều 330 Bộ luật Dân sự 2015. Platform không tự xưng là tổ chức tín dụng và không trực tiếp nhận tiền gửi độc lập.

---

## II. Hệ thống Vai trò & Khối Tác quyền (Actor Zones & 6 Canonical Roles)

Hệ thống được tổ chức thành **3 Khối tác nhân (Actor Zones)** độc lập, đảm bảo nguyên tắc phân chia trách nhiệm (Separation of Duties) và ngăn chặn xung đột lợi ích:

```
┌────────────────────────────────────────────────────────────────────────┐
│               KHỐI 1: PLATFORM GOVERNANCE (Đơn vị chủ quản Sàn)        │
│                                                                        │
│   🛠️ PLATFORM_ADMIN                  👔 PLATFORM_OPERATOR              │
│   (Quản trị Kỹ thuật & Hạ tầng)      (Quản trị Nghiệp vụ, Chính sách   │
│   • Cấu hình hệ thống, checklist     & Hòa giải viên Sàn)              │
│   • Phân quyền, bảo mật              • Thẩm định & Cấp phép Providers  │
│   • Ngưỡng AI YOLO, upload MinIO     • Cấu hình Tham số Thương mại Sàn │
│   • Giám sát hạ tầng, audit logs     • Trọng tài Phân xử Tranh chấp    │
│                                      • Điều phối Dòng tiền Ký quỹ      │
└───────────────────┬──────────────────────────────────┬─────────────────┘
                    │                                  │
                    ▼                                  ▼
      ┌───────────────────────────┐      ┌───────────────────────────┐
      │ KHỐI 2: CUSTOMER (Client) │      │ KHỐI 3: SERVICE PROVIDER  │
      │ 🏢 CLIENT (Chủ tài sản)   │      │ 🏢 PROVIDER_MANAGER       │
      │                           │      │ 🚁 INSPECTOR (Phi công)   │
      │                           │      │ 🔧 MAINTENANCE_ENGINEER   │
      └───────────────────────────┘      └───────────────────────────┘
```

| Khối quyền lực (Actor Zone) | Mã Role | Định danh & Trách nhiệm chuẩn mực |
| :--- | :--- | :--- |
| **1. Platform Governance** | `PLATFORM_ADMIN` | **Quản trị viên Kỹ thuật & Hệ thống**: Quản trị tài khoản, cấu hình bảo mật, duy trì bộ Checklist tiêu chuẩn ngành, cấu hình ngưỡng AI YOLO (`yolo_confidence_threshold`), giới hạn upload MinIO, kiểm tra audit log. Không can thiệp vào tham số thương mại hay phân xử tranh chấp. |
| | `PLATFORM_OPERATOR` | **Quản trị viên Vận hành Nghiệp vụ & Hòa giải Sàn**: Thẩm định năng lực pháp lý Provider (giấy phép, bảo hiểm, định danh drone); **quản trị và điều chỉnh các tham số thương mại sàn (Tỷ lệ hoa hồng $r$, Tỷ lệ bảo lãnh $H$, Thời hạn nghiệm thu, Phí phạt hủy dry-run)**; giám sát Escrow; **phán xử tranh chấp nội bộ theo quy chế sàn**. |
| **2. Customer Organization** | `CLIENT` | **Khách hàng Doanh nghiệp / Chủ sở hữu hạ tầng**: Tự đăng ký pháp nhân; quản lý danh mục tài sản hạ tầng; tạo yêu cầu khảo sát (chỉ định hoặc chào thầu mở RFQ); ký Hợp đồng dịch vụ điện tử; **nạp 100% tiền ký quỹ Escrow qua đối tác thanh toán được cấp phép**; nghiệm thu báo cáo kỹ thuật; mở tranh chấp khi có vi phạm; duyệt đơn bảo trì. |
| **3. Service Provider** | `PROVIDER_MANAGER` | **Quản lý Đơn vị Dịch vụ Drone / Bảo trì**: Khai báo hồ sơ công ty và đội ngũ phi công; tiếp nhận RFQ; lập Báo giá dịch vụ (chỉ gồm công bay, kỹ thuật, di chuyển, VAT — **không** tính phí AI/MinIO của Sàn); nộp giấy phép bay Cục Tác chiến; phê duyệt Kế hoạch bay Drone (Mission Plan); phân công phi công; duyệt phát hành báo cáo QA. |
| | `INSPECTOR` | **Phi công Drone / Thanh tra viên Hiện trường**: Lập kế hoạch bay chi tiết (tính GSD, Overlap, Shot list, góc Gimbal); bay khảo sát hiện trường; nạp ảnh/video lên MinIO kèm dữ liệu telemetry không gian (GPS 3D, độ cao, góc gimbal, mã SHA-256); xác minh ứng viên lỗi AI YOLO; duyệt chéo độc lập (Peer Review) báo cáo của đồng nghiệp. |
| | `MAINTENANCE_ENGINEER` | **Kỹ sư Bảo trì / Sửa chữa**: Khảo sát hiện trường khuyết tật sau kiểm định; lập dự toán vật tư & nhân công; thi công sửa chữa; **bắt buộc nạp ảnh đối chứng Trước/Sau (Before/After Evidence)** lên MinIO để nghiệm thu giải ngân đợt 1 và kích hoạt thời hạn bảo hành. |

---

## III. Mô hình Dòng tiền Ký quỹ (Escrow Cash Flow) & Hợp đồng Điện tử

### 1. Kiến trúc Hợp đồng 3 Bên (Tripartite Agreement)
* **Quy chế hoạt động Sàn (Platform Terms of Service)**: Ràng buộc cả Client và Provider khi tham gia nền tảng. Trao quyền cho `PLATFORM_OPERATOR` ban hành chính sách thương mại và phán xử tranh chấp nội bộ theo quy chế đã công bố.
* **Đơn dịch vụ điện tử (Inspection Service Order / Maintenance Work Order)**: Được sinh ra cho từng thương vụ kiểm định/bảo trì, có giá trị pháp lý theo *Luật Giao dịch điện tử 2023*. Bao gồm: Phạm vi công việc (SOW), Kế hoạch bay kỹ thuật (GSD, Shot list, Overlap), Tiến độ cam kết (SLA), Chi phí dịch vụ Provider và các điều khoản thương mại đã được khóa tại thời điểm ký kết.

### 2. Mô hình Bảo vệ Giao dịch Có Điều kiện Qua Đối tác Thanh toán Được Cấp phép (Escrow Safeguard)
Nhằm giải quyết rủi ro *"Client sợ mất tiền khi Provider làm ẩu"* và *"Provider sợ bị bùng tiền sau khi đã bay"*:
1. **Nạp tiền ký quỹ 100% trước khi bay**: Client nạp 100% giá trị hợp đồng dịch vụ đã duyệt vào tài khoản đảm bảo thanh toán của đối tác ngân hàng/trung gian thanh toán (`HELD_IN_ESCROW`). Provider chỉ nhận lệnh cất cánh sau khi hệ thống nhận được xác nhận chính thức từ cổng thanh toán.
2. **Quyết toán tự động (Auto-Settlement)**: Khi Client bấm "Nghiệm thu (Accept)" HOẶC hết thời hạn nghiệm thu tự động mà Client không phản hồi và không mở tranh chấp: Đối tác thanh toán tự động giải ngân tiền dịch vụ ròng cho Provider sau khi khấu trừ hoa hồng sàn theo chính sách đã khóa trong hợp đồng.
3. **Đóng băng khi có Tranh chấp (`FROZEN_DISPUTED`)**: Tiền ký quỹ lập tức bị phong tỏa ngay khi một bên mở tranh chấp hợp lệ. Tiền chỉ được giải tỏa khi có phán quyết nội bộ của `PLATFORM_OPERATOR` hoặc quyết định của cơ quan tài phán có thẩm quyền.

### 3. Chính sách Cấu hình Động của `PLATFORM_OPERATOR` & Nguyên tắc Contract Snapshot
Toàn bộ các tham số thương mại và vận hành trên sàn **tuyệt đối không bị hardcode**, mà được quản trị tập trung bởi `PLATFORM_OPERATOR` thông qua giao diện Quản trị Chính sách Thương mại:

| Tham số Cấu hình | Ký hiệu | Giá trị Mặc định | Thẩm quyền Quản lý | Phạm vi & Tác động |
| :--- | :---: | :---: | :---: | :--- |
| **Tỷ lệ hoa hồng sàn** | $r$ (`commission_rate`) | Ban hành theo kỳ | `PLATFORM_OPERATOR` | Áp dụng thống nhất cho toàn bộ Provider; tính trên doanh thu dịch vụ hợp lệ trước VAT: $C = r \times B$. |
| **Thời hạn nghiệm thu tự động** | $T_{rev}$ (`auto_settlement_review_days`) | 5 ngày làm việc | `PLATFORM_OPERATOR` | Số ngày làm việc Client được quyền thẩm định báo cáo trước khi tự động giải ngân. |
| **Tỷ lệ bảo lãnh hoàn công** | $H$ (`warranty_retention_rate`) | 10% | `PLATFORM_OPERATOR` | Tỷ lệ phần trăm giữ lại bảo hành sau khi hoàn thành sửa chữa bảo trì (MF5). |
| **Thời hạn bảo hành tiêu chuẩn** | $T_{war}$ (`standard_warranty_days`) | 30 ngày | `PLATFORM_OPERATOR` | Khoảng thời gian bảo hành công trình trước khi giải ngân nốt tiền giữ lại. |
| **Phí phạt hủy chuyến sát giờ** | $P_{dry}$ (`dry_run_penalty_rate`) | 20% chi phí di chuyển | `PLATFORM_OPERATOR` | Mức phạt áp dụng khi Client hủy hợp đồng trong vòng 24h trước giờ bay. |

* **Nguyên tắc Khóa Bất biến Hợp đồng (Contract Snapshot Pattern)**:
  * Khi Client và Provider ký kết Hợp đồng Dịch vụ (Service Order), hệ thống thực hiện sao chép (snapshot) các giá trị tham số tại thời điểm đó vào bản ghi hợp đồng (`locked_commission_rate`, `locked_review_period_days`, `locked_dry_run_rate`, `locked_retention_rate`, `locked_warranty_days`).
  * Mọi sự điều chỉnh chính sách của `PLATFORM_OPERATOR` sau đó **chỉ có hiệu lực đối với các hợp đồng phát sinh mới**, tuyệt đối không hồi tố (non-retroactive) làm thay đổi quyền lợi của các hợp đồng đang thực hiện.

### 4. Hạ tầng Dữ liệu, Mô hình AI YOLO và Trợ lý LLM do Nền tảng (Platform) Cung cấp Tập trung
* **Nguyên tắc Nền tảng cung cấp trọn gói**: Hệ thống lưu trữ MinIO, đường ống xử lý dữ liệu, mô hình **AI YOLO** và **trợ lý LLM** là **Năng lực dùng chung do Platform trực tiếp host, cung cấp và tự chi trả chi phí vận hành** (GPU, API tokens, storage) từ nguồn thu hoa hồng của Sàn.
* **Người dùng thuần túy (Consumers)**:
  - **Provider**: Chỉ sử dụng công cụ AI trên Web/Mobile của Platform để hỗ trợ khảo sát và lập báo cáo. Provider **không được phép bóc tách hoặc tính thêm bất kỳ khoản phí AI / xử lý dữ liệu nào vào Báo giá gửi Client**. Báo giá chỉ bao gồm công bay, nhân lực kỹ thuật, chi phí di chuyển và thuế của Provider.
  - **Client**: Xem hộp bao khuyết tật AI và đối soát kích thước vật lý dựa trên thông số trắc địa GSD.
  - AI chỉ đóng vai trò đề xuất ứng viên (Candidate), không thay thế sự thẩm định và xác nhận của con người (Inspector).

---

## IV. Chi tiết Luồng Nghiệp vụ (Supporting Flow & 5 Core Main Flows)

---

### Supporting Flow (SF) — Onboarding Doanh nghiệp, Thẩm định Pháp lý & Quản trị Danh mục Tài sản

> **Bản chất**: Đây là Luồng Bổ trợ Tiền đề (Supporting Flow) quản lý dữ liệu danh mục ban đầu (Master Data Management / Onboarding), diễn ra một lần hoặc định kỳ cập nhật hồ sơ, là điều kiện tiên quyết để vận hành các Main Flows giao dịch cốt lõi.

**Tác nhân chính**: `Platform Admin`, `Platform Operator`, `Client`, `Provider Manager`, `System`.

#### 1. Quy trình chi tiết (Sequence Steps)
* **SF-01 (Client Self-Registration)**: Đại diện doanh nghiệp khách hàng tự đăng ký tài khoản tổ chức, cung cấp mã số thuế, hồ sơ pháp lý công ty và kích hoạt tài khoản `CLIENT`.
* **SF-02 (Provider Onboarding & Vetting)**: Provider Manager đăng ký hồ sơ năng lực của công ty bay drone: Giấy phép kinh doanh, Danh mục drone kèm số đăng ký định danh phương tiện bay của Bộ Quốc phòng theo *Luật Phòng không nhân dân 2024* & *Nghị định 288/2025/NĐ-CP*, Danh sách phi công kèm chứng chỉ điều khiển bay hợp lệ, và Chứng thư bảo hiểm trách nhiệm dân sự bên thứ ba.
* **SF-03 (Operator Vetting Approval)**: `PLATFORM_OPERATOR` thẩm định tính hợp lệ của hồ sơ Provider. Nếu đạt, cấp trạng thái `VERIFIED`. Nếu thiếu, yêu cầu bổ sung hoặc từ chối (`REJECTED`). Provider chưa được duyệt bị chặn toàn bộ quyền tham gia báo giá.
* **SF-04 (Asset Profiling & Airspace Pre-check)**: Client khai báo thông tin tài sản công trình: Tọa độ địa lý (kinh độ, vĩ độ), ranh giới tiếp cận, cao độ kết cấu, tài liệu bản vẽ hoàn công. Hệ thống tự động tra cứu dữ liệu không phận công khai (`cambay.mod.gov.vn` theo QĐ 18/2020/QĐ-TTg) để hiển thị cảnh báo tham khảo nếu công trình nằm trong hoặc gần vùng cấm/hạn chế bay.
* **SF-05 (Periodic Schedule Cadence)**: Client thiết lập lịch kiểm tra định kỳ cho tài sản (1 tháng, 3 tháng, 6 tháng, 1 năm). Khi đến hạn chu kỳ, hệ thống tự động sinh ra gói Yêu cầu kiểm tra chuyển tiếp sang MF1.

#### 2. Xử lý Luồng Ngoại lệ SF (5 Câu hỏi Bắt buộc)
* **Q1: Dữ liệu đầu vào thiếu hoặc sai?** Hồ sơ Provider thiếu chứng chỉ phi công hoặc bảo hiểm: Operator từ chối duyệt, hệ thống chuyển trạng thái `ADDITIONAL_INFO_REQUIRED`. Tọa độ tài sản nằm trong vùng cấm bay quân sự: Hệ thống gắn cờ cảnh báo `RESTRICTED_AIRSPACE`, yêu cầu phải có giấy phép bay Cục Tác chiến đặc biệt trước khi phát thầu.
* **Q2: Truy cập trái phép / Sai tổ chức?** Client Org A không thể xem tài sản của Client Org B. Provider chưa được duyệt (`PENDING/SUSPENDED`) bị chặn toàn bộ các API xem danh sách tài sản hay nhận yêu cầu.
* **Q3: Thao tác đồng thời / Trùng lặp?** Mã số thuế và Mã tài sản (Asset Code) có ràng buộc duy nhất (Unique Constraint) trong phạm vi tổ chức. Gửi lại form bị chặn ngay với mã lỗi `DUPLICATE_ENTITY`.
* **Q4: Dịch vụ ngoài / Mạng lỗi?** Cổng tra cứu `cambay.mod.gov.vn` bị gián đoạn: Hệ thống lưu trạng thái `AIRSPACE_CHECK_PENDING`, cho phép lưu hồ sơ tài sản nhưng đánh dấu cần thẩm định không phận thủ công trước khi phát thầu.
* **Q5: Từ chối / Hủy giữa chừng?** Provider bị Operator từ chối có quyền bổ sung giấy tờ và gửi thẩm định lại tối đa 3 lần.

---

### MF1 — Yêu cầu Khảo sát, Đấu thầu Báo giá & Ký quỹ Escrow (Survey Request, Quotation Sourcing & Escrow Funding)

**Mục tiêu**: Khởi tạo nhu cầu kiểm định, kết nối Provider đủ điều kiện thông qua chỉ định hoặc đấu thầu mở (RFQ), ký hợp đồng điện tử 3 bên và nạp 100% tiền ký quỹ vào tài khoản đảm bảo thanh toán có điều kiện.

**Tác nhân chính**: `Client`, `Platform Operator`, `Provider Manager`, `System`.

#### 1. Quy trình chi tiết (Main Sequence)

| Bước | Vai trò / Lane | Hoạt động chi tiết | Sản phẩm đầu ra |
| :--- | :--- | :--- | :--- |
| **MF1-01** | Client | Khởi tạo Yêu cầu khảo sát (từ lịch định kỳ SF-05 hoặc đột xuất). Chọn phương thức chọn thầu: (A) **Chỉ định trực tiếp** Provider đối tác quen thuộc; hoặc (B) **Chào thầu mở (Open RFQ)** cho các Provider trong khu vực. Nêu rõ mục tiêu kiểm tra (tìm nứt bê tông, kiểm tra ăn mòn dầm thép). | Yêu cầu kiểm tra (RFQ) |
| **MF1-02** | Platform Operator | *(Tùy chọn hỗ trợ)*: Kiểm tra yêu cầu chào thầu mở của Client, hỗ trợ kết nối và gửi thông báo đến các Provider có năng lực và phạm vi hoạt động phù hợp. | Danh sách Provider tiếp cận RFQ |
| **MF1-03** | Provider Manager | Xem xét yêu cầu, khảo sát địa hình sơ bộ từ xa và lập **Báo giá dịch vụ (Quotation)**: Chỉ gồm (1) Chi phí nhân lực bay hiện trường; (2) Chi phí kỹ thuật chuyên môn; (3) Chi phí đi lại/triển khai hợp lệ; (4) Thuế VAT của Provider. **Tuyệt đối không tính phí xử lý AI/MinIO của Sàn vào báo giá.** | Báo giá dịch vụ (v1, v2) |
| **MF1-04** | Client | Xem xét các báo giá cạnh tranh. Có thể yêu cầu điều chỉnh (Revision) hoặc chọn Báo giá phù hợp nhất để chấp thuận. | Báo giá được chấp thuận |
| **MF1-05** | System | Khởi tạo **Hợp đồng Dịch vụ Điện tử (Inspection Service Order)**: Thực hiện **Contract Snapshot** khóa cứng tỷ lệ hoa hồng $r$, thời hạn nghiệm thu $T_{rev}$ và phí hủy chuyến $P_{dry}$ do `PLATFORM_OPERATOR` ban hành tại thời điểm này vào bản ghi hợp đồng. | Hợp đồng điện tử sẵn sàng ký |
| **MF1-06** | Client & Provider Manager | Hai bên thực hiện ký số điện tử hợp đồng theo *Luật Giao dịch điện tử 2023*. Client tiến hành nạp 100% giá trị hợp đồng qua cổng thanh toán của đối tác ngân hàng/trung gian thanh toán được cấp phép (`HELD_IN_ESCROW`). Hợp đồng chính thức có hiệu lực (`LEGALLY_BINDING`). | Hợp đồng có hiệu lực & Tiền ký quỹ an toàn |

#### 2. Chính sách Hủy Hợp đồng & Rủi ro Thời tiết (Theo Snapshot hợp đồng)
* **Hủy trước 24 giờ**: Client hủy chuyến trước 24h được hoàn lại 100% tiền ký quỹ dịch vụ (sau khi trừ phí giao dịch cổng thanh toán nếu có).
* **Hủy sát giờ trong vòng 24 giờ**: Áp dụng mức phạt di chuyển `locked_dry_run_rate` (mặc định 20% chi phí di chuyển) khấu trừ đền bù cho Provider; phần còn lại hoàn trả cho Client.
* **Bất khả kháng do thời tiết xấu**: Nếu có bão, mưa lớn hoặc gió vượt ngưỡng an toàn bay, hai bên thống nhất dời lịch bay mà không phạt tiền và không tính vi phạm SLA.

#### 3. Xử lý Luồng Ngoại lệ MF1 (5 Câu hỏi Bắt buộc)
* **Q1: Dữ liệu đầu vào thiếu hoặc sai?** Yêu cầu khảo sát thiếu thông tin vị trí công trình hoặc mục tiêu kiểm định: Hệ thống yêu cầu Client bổ sung đầy đủ trước khi mở cổng nhận báo giá.
* **Q2: Truy cập trái phép / Sai tổ chức?** Provider A không thể xem nội dung giá thầu của Provider B trong cùng một gói RFQ.
* **Q3: Thao tác đồng thời / Trùng lặp?** Client bấm thanh toán 2 lần: Cơ chế Idempotency Key khóa cổng thanh toán, ngăn chặn tạo 2 giao dịch ký quỹ trùng lặp cho một đơn hàng.
* **Q4: Dịch vụ ngoài / Mạng lỗi?** Cổng thanh toán timeout khi Client đang nạp tiền: Đơn hàng giữ trạng thái `PAYMENT_PENDING`; hệ thống chỉ chuyển sang `HELD_IN_ESCROW` khi nhận webhook xác thực hợp lệ từ cổng thanh toán.
* **Q5: Từ chối / Hủy giữa chừng?** Client hủy yêu cầu trước khi chọn báo giá: RFQ tự động đóng (`CANCELLED`), thông báo cho các Provider đã nộp báo giá.

---

### MF2 — Lập Kế hoạch Bay Drone Chuyên dụng & Thẩm định Không phận (Drone Mission Planning & Airspace Clearance) 🚀 [FLOW NỔI BẬT DRONE]

> **Trọng tâm công nghệ Drone**: Đây là luồng kỹ thuật chuyên sâu làm nổi bật năng lực quản trị bay trắc địa và pháp lý không phận của nền tảng, thiết lập các tham số trắc địa ảnh chuẩn mực trước khi cất cánh.

**Tác nhân chính**: `Provider Manager`, `Inspector` (Phi công), `Platform Operator`, `System`.

#### 1. Quy trình chi tiết (Main Sequence)

| Bước | Vai trò / Lane | Hoạt động chi tiết | Sản phẩm đầu ra |
| :--- | :--- | :--- | :--- |
| **MF2-01** | Inspector | **Tính toán trắc địa ảnh & Độ phân giải mặt đất (Photogrammetric GSD Planning)**: Dựa trên yêu cầu phát hiện vết nứt của SOW (ví dụ: vết nứt bê tông $\ge 0.5$ mm cần GSD $\le 1.0$ mm/pixel). Inspector nhập thông số camera/cảm biến drone (tiêu cự focal length, kích thước cảm biến sensor size, độ phân giải ảnh); hệ thống tính toán ra **Độ cao bay an toàn (AGL - Above Ground Level)** và **Khoảng cách chụp tối ưu** tới bề mặt kết cấu. | Tham số GSD & Độ cao bay chuẩn |
| **MF2-02** | Inspector | **Thiết lập tỷ lệ chồng phủ ảnh (Image Overlap Calculation)**: Cấu hình tỷ lệ chồng phủ dọc (Forward Overlap) và ngang (Side Overlap) tối thiểu từ 70% – 80% để đảm bảo không bỏ sót điểm mù kết cấu và phục vụ mô hình hóa khuyết tật. | Tham số Overlap đạt chuẩn trắc địa |
| **MF2-03** | Inspector | **Xây dựng Danh mục Góc chụp Cấu kiện (Structural Shot List & Gimbal Pitch)**: Lập danh sách các điểm chụp (Waypoints) tương ứng với từng hạng mục cấu kiện: (1) Mặt đứng công trình (Gimbal $0^\circ$ chụp ngang); (2) Mặt dưới dầm sàn / mố cầu (Gimbal $+30^\circ$ đến $+45^\circ$ chụp hất lên); (3) Mái vòm / Mặt trên kết cấu (Gimbal $-90^\circ$ chụp thẳng góc Nadir). | Structural Shot List hoàn chỉnh |
| **MF2-04** | Inspector & System | **Thẩm định An toàn Không phận Số (Airspace Digital Clearance)**: Hệ thống tự động nạp tọa độ không gian 3D của khu vực bay, đối chiếu với Cổng thông tin Vùng cấm bay (`cambay.mod.gov.vn` theo QĐ 18/2020/QĐ-TTg). Nếu tọa độ nằm trong hành lang an toàn hàng không hoặc khu vực hạn chế bay, hệ thống kích hoạt cảnh báo bắt buộc đính kèm giấy phép đặc biệt. | Báo cáo thẩm định không phận số |
| **MF2-05** | Provider Manager | **Kiểm soát Pháp lý Bay theo Luật PKND 2024 & NĐ 288/2025/NĐ-CP**: Đính kèm số hiệu Giấy phép bay do Cục Tác chiến - Bộ Tổng Tham mưu cấp; chọn phi công `Inspector` có chứng chỉ bay hợp lệ; kiểm tra mã định danh drone của Bộ Quốc phòng; kiểm tra cam kết không có xung đột lợi ích. | Hồ sơ cấp phép bay hoàn tất |
| **MF2-06** | Provider Manager | Phê duyệt Kế hoạch Bay Drone (Drone Mission Plan), ký lệnh bay điện tử và phát hành Gói nhiệm vụ bay (Mission Package) cho phi công. Chuyển trạng thái đơn hàng sang **`READY_FOR_FLIGHT`**. | Kế hoạch bay được phê duyệt (`READY_FOR_FLIGHT`) |

#### 2. Xử lý Luồng Ngoại lệ MF2 (5 Câu hỏi Bắt buộc)
* **Q1: Dữ liệu đầu vào thiếu hoặc sai?** Inspector thiết lập độ cao bay quá cao khiến GSD tính toán vượt ngưỡng cho phép phát hiện vết nứt (ví dụ GSD = 3.5 mm/pixel trong khi yêu cầu $\le 1.0$ mm/pixel): Hệ thống báo lỗi đỏ, chặn không cho phê duyệt Mission Plan cho đến khi giảm độ cao bay hoặc chọn camera có tiêu cự phù hợp.
* **Q2: Truy cập trái phép / Sai tổ chức?** Phi công thuộc Provider A không thể xem hoặc chỉnh sửa Kế hoạch bay của Provider B. Inspector chưa có chứng chỉ bay không được phép gán vào Mission Plan.
* **Q3: Thao tác đồng thời / Trùng lặp?** Hai người quản lý cùng gán phi công cho một gói nhiệm vụ: Hệ thống áp dụng khóa lạc quan (Optimistic Lock) trên Mission Plan; lệnh gán thứ hai bị từ chối với thông báo nhiệm vụ đã được phân công.
* **Q4: Dịch vụ ngoài / Mạng lỗi?** Cổng thông tin không phận số `cambay.mod.gov.vn` bị gián đoạn kết nối: Hệ thống gắn cờ `AIRSPACE_MANUAL_VERIFY_REQUIRED`, yêu cầu Provider Manager đối chiếu bản đồ giấy/văn bản cấp phép của Bộ Quốc phòng trước khi phê duyệt bay.
* **Q5: Từ chối / Hủy giữa chừng?** Inspector được phân công nhận thấy hiện trường có chướng ngại vật nguy hiểm mới phát sinh (cần cẩu, đường điện cao thế): Inspector từ chối nhận lệnh bay kèm biên bản giải trình an toàn; Mission Plan được trả lại cho Provider Manager để điều chỉnh đường bay hoặc đổi phương án.

---

### MF3 — Khảo sát Hiện trường, Thu nạp Telemetry & Phân tích AI YOLO (Flight Survey, Telemetry Capture & AI Defect Verification)

**Mục tiêu**: Thực hiện bay khảo sát theo kế hoạch đã duyệt, thu thập hình ảnh kèm dữ liệu không gian telemetry (GPS 3D, gimbal pitch), bảo đảm toàn vẹn chứng cứ số bằng mã SHA-256, chạy mô hình AI YOLO tập trung của Platform để phát hiện khuyết tật, tính toán kích thước vật lý theo GSD, thẩm định chéo nội bộ (Peer Review) và phát hành báo cáo kỹ thuật QA.

**Tác nhân chính**: `Inspector` (Người bay), `Inspector` (Người review chéo), `Provider Manager`, `Platform MinIO`, `Platform AI YOLO Service`, `System`.

#### 1. Quy trình chi tiết (Main Sequence)

| Bước | Vai trò / Lane | Hoạt động chi tiết | Sản phẩm đầu ra |
| :--- | :--- | :--- | :--- |
| **MF3-01** | Inspector | Mở ứng dụng Web/Mobile tại hiện trường, kích hoạt phiên bay (`IN_PROGRESS`). Điều khiển drone thực hiện chụp ảnh/quay video bám sát các Waypoints và góc nghiêng Gimbal trong Structural Shot List đã lập ở MF2. | Phiên bay hiện trường kích hoạt |
| **MF3-02** | Inspector | Tải toàn bộ tệp ảnh/video độ phân giải cao thu được lên hệ thống MinIO do Platform cung cấp qua giao thức phân đoạn (Chunked Upload). | Bằng chứng kiểm định thô |
| **MF3-03** | System (Platform MinIO & Ingestion) | Tự động bóc tách **Dữ liệu Không gian Telemetry (Spatial Telemetry Metadata)**: Tọa độ GPS 3D, độ cao tương đối AGL, góc nghiêng gimbal camera, timestamp; tự động tính mã băm toàn vẹn **SHA-256** cho từng file ảnh. Từ chối tệp trùng lặp. | Bằng chứng số được bảo vệ toàn vẹn |
| **MF3-04** | System (Platform YOLO AI Service) | Pipeline AI YOLO do Platform trực tiếp host tự động quét toàn bộ ảnh hợp lệ; phát hiện các khuyết tật (vết nứt bê tông, gỉ sét cốt thép, bong tróc). Hệ thống **tự động tính kích thước vật lý thực tế của vết nứt (chiều dài mm, bề rộng mm)** bằng cách nhân kích thước pixel nhận diện với giá trị **GSD** đã thiết lập ở MF2. Tạo danh sách **Ứng viên lỗi (Defect Candidates)** kèm hộp bao (Bounding Box). | Danh mục ứng viên lỗi kèm kích thước vật lý (GSD) |
| **MF3-05** | Inspector (Người bay) | Kiểm tra trực quan từng ảnh và từng ứng viên AI: Chọn **Xác nhận (Confirm)**, **Sửa đổi (Modify)**, hoặc **Bác bỏ (Reject)**. Nếu AI bỏ sót, Inspector **thêm lỗi thủ công (Manual Finding)**. Hoàn tất trả lời checklist kỹ thuật. | Hồ sơ khiếm khuyết đã xác minh |
| **MF3-06** | System | Tự động tổng hợp Bản thảo Báo cáo Kỹ thuật (Draft Report v1.0) kết hợp checklist, dữ liệu telemetry, ảnh khuyết tật và phần tóm tắt thuyết minh do **Trợ lý AI LLM của Platform** tự động soạn thảo. Loại bỏ toàn bộ ứng viên AI bị bác bỏ khỏi báo cáo chính thức. | Bản thảo báo cáo kỹ thuật |
| **MF3-07** | Inspector (Người review chéo) | **Thẩm định chéo kỹ thuật (Internal Peer Review)**: Một Inspector độc lập khác trong cùng Provider thẩm định tính chính xác của báo cáo. *Quy tắc bắt buộc: Người bay tuyệt đối không được tự duyệt báo cáo của mình*. | Biên bản thẩm định chéo kỹ thuật |
| **MF3-08** | Inspector (Người bay) | Nếu reviewer yêu cầu chỉnh sửa: cập nhật lại báo cáo (v1.1) và nộp lại. Nếu đạt chuẩn, reviewer ký duyệt kỹ thuật (`TECHNICALLY_APPROVED`). | Báo cáo đạt chuẩn kỹ thuật |
| **MF3-09** | Provider Manager | Kiểm tra tổng thể hồ sơ bàn giao so với Service Order và chính thức **Ký phát hành Báo cáo (Release Final Report)** gửi Client. Hệ thống tự động kích hoạt đồng hồ đếm ngược thời hạn nghiệm thu ($T_{rev}$ - mặc định 5 ngày làm việc theo snapshot hợp đồng). | Báo cáo chính thức & Kích hoạt đồng hồ nghiệm thu |

#### 2. Xử lý Luồng Ngoại lệ MF3 (5 Câu hỏi Bắt buộc)
* **Q1: Dữ liệu đầu vào thiếu hoặc sai?** Ảnh tải lên bị mờ, rung lắc hoặc thiếu tọa độ GPS do mất tín hiệu vệ tinh: Hệ thống gắn cờ cảnh báo `METADATA_INCOMPLETE`. Nếu ảnh không đủ chuẩn đo lường vết nứt theo GSD, Inspector bắt buộc phải chụp lại ngay tại hiện trường.
* **Q2: Truy cập trái phép / Sai tổ chức?** Tác giả báo cáo cố tình chọn chính mình làm Peer Reviewer: Hệ thống chặn đứng ở tầng API với mã lỗi `PEER_REVIEW_SELF_APPROVAL_PROHIBITED`.
* **Q3: Thao tác đồng thời / Trùng lặp?** Mạng chập chờn khiến Inspector tải lên 1 tệp nhiều lần: Hệ thống đối soát mã băm SHA-256; nếu trùng lặp, bỏ qua file thứ hai mà không tạo bản ghi rác.
* **Q4: Dịch vụ ngoài / Mạng lỗi?** Dịch vụ AI YOLO của Platform bị quá tải hoặc tạm ngừng phục vụ: Hệ thống tự động chuyển sang cơ chế **Manual Fallback**, cho phép Inspector tự khoanh vùng và đo vẽ vết nứt thủ công trên ảnh, tiến độ bàn giao báo cáo không bị đình trệ.
* **Q5: Từ chối / Hủy giữa chừng?** Peer Reviewer phát hiện vết nứt bị đánh giá sai cấp độ nghiêm trọng: Từ chối duyệt, trả về trạng thái `REVISION_REQUIRED` kèm ghi chú kỹ thuật; tác giả phải kiểm tra lại dữ liệu đo lường GSD và hiệu chỉnh kết luận.

---

### MF4 — Nghiệm thu Báo cáo, Quyết toán Tự động & Trọng tài Xử lý Tranh chấp (Report Acceptance, Commission Settlement & Operator Dispute Resolution)

**Mục tiêu**: Khách hàng thẩm định kết quả khảo sát trong thời hạn đã khóa; tự động quyết toán giải ngân theo hoa hồng đã ấn định; hoặc kích hoạt cơ chế Trọng tài phân xử nội bộ của `PLATFORM_OPERATOR` khi phát sinh mâu thuẫn.

**Tác nhân chính**: `Client`, `Provider Manager`, `Platform Operator` (Trọng tài), `System`.

#### 1. Quy trình chi tiết (Main Sequence)

| Bước | Vai trò / Lane | Hoạt động chi tiết | Sản phẩm đầu ra |
| :--- | :--- | :--- | :--- |
| **MF4-01** | Client | Xem xét báo cáo kiểm định hoàn chỉnh trên Web/Mobile (ảnh khuyết tật độ phân giải cao, vị trí 3D, số đo vết nứt). Bắt đầu tính thời hạn nghiệm thu $T_{rev}$ (theo giá trị snapshot đã khóa trong hợp đồng MF1, mặc định 5 ngày làm việc). | Báo cáo đang thẩm định nghiệm thu |
| **MF4-02a** | Client (Nhánh Nghiệm thu) | Client hài lòng với chất lượng -> Bấm **"Nghiệm thu (Accept)"**. | Quyết định nghiệm thu |
| **MF4-02b** | System (Nhánh Auto-Settlement) | Quá thời hạn $T_{rev}$, nếu Client không phản hồi và không mở tranh chấp hợp lệ -> Hệ thống tự động kích hoạt **Nghiệm thu mặc định (Auto-Settlement)** nhằm bảo vệ dòng tiền chính đáng cho Provider. | Quyết định nghiệm thu tự động |
| **MF4-03** | System và đối tác thanh toán | Báo cáo chuyển sang trạng thái bất biến (`COMPLETED`). **Giải ngân theo tỷ lệ hoa hồng đã khóa tại hợp đồng**: Với cơ sở tính phí $B$ và tỷ lệ hoa hồng $r$ đã khóa snapshot, hoa hồng sàn $C = r \times B$. Provider nhận số tiền ròng $B - C$; Platform ghi nhận hoa hồng $C$ kèm hóa đơn VAT riêng. Provider xuất hóa đơn dịch vụ đủ giá trị cho Client. | Dòng tiền tất toán (`DISBURSED`) & Hóa đơn riêng biệt |
| **MF4-04** | Client (Nhánh Yêu cầu Làm rõ) | Nếu có nội dung kỹ thuật chưa rõ ràng, Client gửi yêu cầu giải trình. Provider Manager giải trình hoặc phát hành bản báo cáo hiệu chỉnh (Client không được trực tiếp sửa nội dung chuyên môn). | Báo cáo giải trình hiệu chỉnh |
| **MF4-05** | Client / Provider (Nhánh Mở Tranh chấp) | Khi có mâu thuẫn nghiêm trọng (ảnh mờ sai lệch GSD cam kết, bỏ sót khuyết tật nghiêm trọng, làm rơi drone gây hư hỏng tài sản): Một trong hai bên bấm **"Mở Tranh chấp (Open Dispute)"**. | Hồ sơ tranh chấp (`OPENED`) |
| **MF4-06** | System và đối tác thanh toán | **Tiền ký quỹ lập tức bị đóng băng (`FROZEN_DISPUTED`)**. Chuyển toàn bộ hồ sơ sang bàn làm việc của `PLATFORM_OPERATOR`. | Tiền ký quỹ bị phong tỏa |
| **MF4-07** | Platform Operator | **Thụ lý & Hòa giải nội bộ theo Quy chế sàn**: Yêu cầu các bên cung cấp chứng cứ bổ sung. Operator tiến hành đối soát: Hợp đồng SOW & Kế hoạch bay MF2 (GSD, Shot list) ↔ Bằng chứng MinIO kèm dữ liệu telemetry và mã SHA-256 (MF3) ↔ Đơn khiếu nại của Client ↔ Giải trình của Provider. | Biên bản thẩm tra chứng cứ số |
| **MF4-08** | Platform Operator | **Ban hành Phán quyết Xử lý Nội bộ** theo 1 trong 3 biện pháp của Sàn (không thay thế quyền khởi kiện Tòa án hoặc trọng tài thương mại). | Phán quyết xử lý có hiệu lực điều phối Escrow |

#### 2. Ba biện pháp xử lý nội bộ của `PLATFORM_OPERATOR`
* **Biện pháp A — Lỗi chất lượng có thể khắc phục (Ảnh mờ, thiếu góc chụp so với Shot list)**:
  - Operator ra lệnh cho **Provider bay chụp lại miễn phí (Free Reshoot)** hoàn thành trong vòng 48 giờ. Tiền ký quỹ tiếp tục bị đóng băng cho đến khi Client nhận và nghiệm thu báo cáo bay lại.
* **Biện pháp B — Vi phạm nghiêm trọng / Gian lận dữ liệu / Gây thiệt hại công trình**:
  - Operator quyết định chấm dứt hợp đồng; đối tác thanh toán hoàn lại 100% tiền ký quỹ cho Client; áp dụng chế tài phạt vi phạm đối với Provider và đình chỉ hoạt động (`SUSPENDED`).
* **Biện pháp C — Client khiếu nại không có căn cứ**:
  - Operator bác khiếu nại; đối tác thanh toán tự động giải ngân cho Provider theo đúng hợp đồng. Trường hợp có giảm giá/hoàn tiền một phần $Q$, hoa hồng sàn tự động đảo tỷ lệ tương ứng $r \times Q$.

#### 3. Xử lý Luồng Ngoại lệ MF4 (5 Câu hỏi Bắt buộc)
* **Q1: Dữ liệu đầu vào thiếu hoặc sai?** Đơn khiếu nại không có ảnh/video bằng chứng chứng minh: Operator yêu cầu bổ sung trong 24h; quá hạn, khiếu nại tự động bị bác bỏ.
* **Q2: Truy cập trái phép / Sai tổ chức?** Nhân viên không có thẩm quyền trong Client Org cố tình bấm mở tranh chấp: Hệ thống chặn quyền ở tầng API, chỉ tài khoản đại diện pháp lý mới được mở tranh chấp.
* **Q3: Thao tác đồng thời / Trùng lặp?** Client vừa bấm "Accept" vừa bấm "Open Dispute" cùng thời điểm: Giao dịch dùng Pessimistic Lock trên Service Order; trạng thái đầu tiên commit thành công sẽ chặn đứng thao tác còn lại.
* **Q4: Dịch vụ ngoài / Mạng lỗi?** Cổng gửi SMS/Email thông báo phán quyết bị lỗi: Phán quyết vẫn lưu bất biến trong database kèm Audit Log; các bên nhận thông báo qua In-app Notification ngay khi đăng nhập.
* **Q5: Từ chối / Hủy giữa chừng?** Provider từ chối thực hiện phán quyết "Free Reshoot": Operator kích hoạt chuyển sang Biện pháp B (hủy hợp đồng, hoàn tiền cho Client, phạt Provider).

---

### MF5 — Xử lý Khiếm khuyết, Đơn hàng Bảo trì & Tiền Bảo lãnh Hoàn công (Defect Rectification, Maintenance & Retention)

**Mục tiêu**: Chuyển các khuyết tật từ báo cáo drone thành đơn hàng sửa chữa công trình, kiểm soát phát sinh chi phí, nghiệm thu ảnh đối chứng Before/After và quản lý Dòng tiền Bảo lãnh hoàn công (Retention Money).

**Tác nhân chính**: `Client`, `Maintenance Provider Manager`, `Maintenance Engineer`, `Platform Operator`, `System`.

#### 1. Quy trình chi tiết (Main Sequence)

| Bước | Vai trò / Lane | Hoạt động chi tiết | Sản phẩm đầu ra |
| :--- | :--- | :--- | :--- |
| **MF5-01** | Client | Chọn các khuyết tật đã xác minh từ Báo cáo MF4 để tạo **Phiếu yêu cầu bảo trì (Maintenance Ticket)**. | Maintenance Ticket |
| **MF5-02** | Maintenance Provider Manager | Khảo sát hiện trường (qua ảnh zoom 3D MF3 hoặc trực tiếp); lập Phương án kỹ thuật, dự toán vật tư và Báo giá bảo trì (Maintenance Quotation). Hợp đồng thi công bắt buộc áp dụng **Tiền bảo lãnh hoàn công** theo tỷ lệ đã cấu hình. | Báo giá bảo trì & Đơn dịch vụ |
| **MF5-03** | System | Khởi tạo **Đơn dịch vụ bảo trì (Maintenance Order)**: Thực hiện **Contract Snapshot** khóa cứng tỷ lệ bảo lãnh $H$ (mặc định 10%) và thời hạn bảo hành $T_{war}$ (mặc định 30 ngày) do Operator ban hành vào đơn hàng. Client nạp 100% tiền ký quỹ vào tài khoản Escrow. | Tiền bảo trì ký quỹ Escrow |
| **MF5-04** | Maintenance Engineer | Tiếp nhận phân công thi công. Đến hiện trường sửa chữa (trám trét vết nứt bê tông, xử lý ăn mòn, thay cáp). **Bắt buộc chụp và nạp ảnh đối chứng Trước và Sau thi công (Before/After Evidence)** lên MinIO kèm nhật ký vật tư. | Nhật ký thi công & Cặp ảnh đối chứng Before/After |
| **MF5-05** | Maintenance Engineer & Provider Manager | Nếu phát hiện hư hỏng ngầm vượt quá dự toán: Dừng ngay phần việc phát sinh, lập **Yêu cầu thay đổi (Change Order)**. Client xem xét và ký quỹ bổ sung thì mới được thi công tiếp. | Change Order được duyệt |
| **MF5-06** | Client & Provider Manager | **Nghiệm thu Đợt 1 (Nghiệm thu hoàn công)**: Client đối soát cặp ảnh Before/After. Nếu đạt chuẩn, Client ký biên bản nghiệm thu hoàn công. | Quyết toán Đợt 1 |
| **MF5-07** | System và đối tác thanh toán | Đối tác giải ngân tiền đợt 1: Giải ngân phần dịch vụ hoàn công đủ điều kiện $(100\% - H)$ cho Đơn vị bảo trì sau khi trừ hoa hồng sàn; **giữ lại khoản bảo lãnh $H$ (10%)** trong tài khoản Escrow. Khuyết tật chuyển trạng thái `RESOLVED`. Kích hoạt thời hạn bảo hành $T_{war}$ (30 ngày). | Giải ngân Đợt 1 & Giữ lại tiền bảo lãnh $H$ |
| **MF5-08** | Client & Platform Operator | **Nghiệm thu Đợt 2 (Hết hạn bảo hành)**: Sau khi hết thời gian $T_{war}$, nếu không có khiếu nại hoặc tái hỏng: Đối tác thanh toán giải ngân nốt số tiền giữ lại $H$ cho Đơn vị bảo trì (**không tính thêm hoa hồng sàn lần 2**). Đóng vĩnh viễn vòng đời khuyết tật (`CLOSED`). | Giải ngân nốt tiền bảo lãnh & Đóng Ticket |

#### 2. Nhánh Xử lý Rework / Re-inspection / Tranh chấp Bảo hành
* **Yêu cầu làm lại (Rework)**: Chất lượng chắp vá cẩu thả -> Client yêu cầu Đơn vị bảo trì thi công lại miễn phí trước khi nghiệm thu Đợt 1.
* **Yêu cầu kiểm tra lại bằng Drone (Re-inspection)**: Vị trí sửa chữa trên cao nguy hiểm khó nhìn bằng mắt thường -> Client kích hoạt yêu cầu bay chụp lại, tạo ra một đơn kiểm định liên kết quay trở lại MF1 & MF2.
* **Tranh chấp bảo hành**: Mối hàn bị nứt lại trong thời hạn bảo hành nhưng Provider từ chối bảo hành -> Client mở tranh chấp; `PLATFORM_OPERATOR` xử lý theo quy chế: sử dụng khoản tiền giữ lại $H$ để thuê đơn vị khác khắc phục hoặc hoàn tiền cho Client.

#### 3. Xử lý Luồng Ngoại lệ MF5 (5 Câu hỏi Bắt buộc)
* **Q1: Dữ liệu đầu vào thiếu hoặc sai?** Kỹ sư nộp nghiệm thu nhưng thiếu ảnh đối chứng Before/After: Hệ thống khóa nút Submit, bắt buộc phải đủ cặp ảnh đối chứng mới được trình nghiệm thu.
* **Q2: Truy cập trái phép / Sai tổ chức?** Đơn vị bảo trì A không thể xem hồ sơ sửa chữa của Đơn vị bảo trì B.
* **Q3: Thao tác đồng thời / Trùng lặp?** Kỹ sư gửi 2 Change Order liên tiếp: Hệ thống chỉ cho phép duy nhất 1 Change Order ở trạng thái `PENDING_APPROVAL` tại một thời điểm.
* **Q4: Dịch vụ ngoài / Mạng lỗi?** Mất sóng di động tại hầm công trình: Mobile app lưu ảnh offline vào bộ nhớ mã hóa an toàn thiết bị (`flutter_secure_storage`), tự động đồng bộ lên MinIO khi có mạng trở lại.
* **Q5: Từ chối / Hủy giữa chừng?** Client từ chối phê duyệt Change Order: Đơn vị bảo trì dừng phần phát sinh, chỉ thi công đúng phạm vi hợp đồng ban đầu.

---

## V. Ma trận Phân quyền & Trách nhiệm (RACI Matrix)

| Quy trình / Nghiệp vụ cốt lõi | `PLATFORM_ADMIN` | `PLATFORM_OPERATOR` | `CLIENT` | `PROVIDER_MANAGER` | `INSPECTOR` | `MAINTENANCE_ENGINEER` |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **SF: Thẩm định Provider & Khai báo Drone** | I | **A / R** | I | **R** | C | - |
| **SF: Khai báo Tài sản & Cảnh báo Cấm bay** | I | C | **A / R** | - | - | - |
| **Chính sách: Cấu hình Động Tham số Thương mại** | I | **A / R** | I | I | - | - |
| **MF1: Đấu thầu RFQ & Báo giá Kiểm định** | - | C | **A** | **R** | - | - |
| **MF1: Ký Hợp đồng & Ký quỹ Escrow 100%** | I | C | **A / R** | **R** | - | - |
| **MF2: Lập Kế hoạch Bay (GSD, Overlap, Shot List)** | - | - | I | **A** | **R** | - |
| **MF2: Kiểm tra Không phận Số & Giấy phép Bay** | I | C | I | **A / R** | **R** | - |
| **MF3: Khảo sát Hiện trường & Bóc tách Telemetry** | - | - | I | I | **A / R** | - |
| **MF3: Nhận diện AI YOLO & Xác minh Lỗi (GSD)** | - | - | - | I | **A / R** | - |
| **MF3: Thẩm định chéo (Internal Peer Review)** | - | - | - | I | **A / R** | - |
| **MF3: Ký phát hành Báo cáo Kỹ thuật QA** | - | - | I | **A / R** | I | - |
| **MF4: Nghiệm thu Báo cáo & Quyết toán Escrow** | I | C | **A / R** | I | - | - |
| **MF4: Thụ lý & Trọng tài Phân xử Tranh chấp** | I | **A / R** | C | C | C | - |
| **MF5: Tạo Ticket & Báo giá Bảo trì** | - | - | **A** | **R** | - | C |
| **MF5: Ký quỹ Bảo trì & Thi công Before/After** | - | - | **A** | I | - | **A / R** |
| **MF5: Nghiệm thu Hoàn công & Tất toán Bảo hành** | I | **R** | **A** | I | - | I |

*Ghi chú*:
* **R (Responsible)**: Người trực tiếp thực hiện công việc.
* **A (Accountable)**: Người chịu trách nhiệm phê duyệt cuối cùng và sở hữu kết quả.
* **C (Consulted)**: Người được tham vấn ý kiến, cung cấp dữ liệu đối soát.
* **I (Informed)**: Người được nhận thông báo kết quả.
