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
│   • Cấu hình hệ thống, checklist     & Xử lý Khiếu nại Nội bộ)              │
│   • Phân quyền, bảo mật              • Thẩm định & Cấp phép Providers  │
│   • Ngưỡng AI YOLO, upload MinIO     • Cấu hình Tham số Thương mại Sàn │
│   • Giám sát hạ tầng, audit logs     • Xử lý khiếu nại nội bộ theo Terms│
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
| **2. Customer Organization** | `CLIENT` | **Khách hàng Doanh nghiệp / Chủ sở hữu hạ tầng**: Tự đăng ký pháp nhân; quản lý danh mục tài sản hạ tầng; tạo yêu cầu khảo sát (chỉ định hoặc chào thầu mở RFQ); ký Hợp đồng dịch vụ điện tử; **nạp khoản tiền theo tỷ lệ chính sách đã snapshot qua đối tác thanh toán được cấp phép**; nghiệm thu báo cáo kỹ thuật; mở tranh chấp khi có vi phạm; duyệt đơn bảo trì. |
| **3. Service Provider** | `PROVIDER_MANAGER` | **Quản lý Đơn vị Dịch vụ Drone / Bảo trì**: Khai báo hồ sơ công ty và đội ngũ phi công; tiếp nhận RFQ; lập Báo giá dịch vụ (chỉ gồm công bay, kỹ thuật, di chuyển, VAT — **không** tính phí AI/MinIO của Sàn); nộp giấy phép bay Cục Tác chiến; phê duyệt Kế hoạch bay Drone (Mission Plan); phân công phi công; duyệt phát hành báo cáo QA. |
| | `INSPECTOR` | **Phi công Drone / Thanh tra viên Hiện trường**: Lập kế hoạch bay chi tiết (tính GSD, Overlap, Shot list, góc Gimbal); bay khảo sát hiện trường; nạp ảnh/video lên MinIO kèm dữ liệu telemetry không gian (GPS 3D, độ cao, góc gimbal, mã SHA-256); xác minh ứng viên lỗi AI YOLO; duyệt chéo độc lập (Peer Review) báo cáo của đồng nghiệp. |
| | `MAINTENANCE_ENGINEER` | **Kỹ sư Bảo trì / Sửa chữa**: Khảo sát hiện trường khuyết tật sau kiểm định; lập dự toán vật tư & nhân công; thi công sửa chữa; **bắt buộc nạp ảnh đối chứng Trước/Sau (Before/After Evidence)** lên MinIO để nghiệm thu giải ngân đợt 1 và kích hoạt thời hạn bảo hành. |

---

## III. Mô hình Dòng tiền Ký quỹ (Escrow Cash Flow) & Hợp đồng Điện tử

### 1. Kiến trúc Hợp đồng 3 Bên (Tripartite Agreement)
* **Quy chế hoạt động Sàn (Platform Terms of Service)**: Ràng buộc cả Client và Provider khi tham gia nền tảng. Cho phép `PLATFORM_OPERATOR` công bố chính sách thương mại và điều phối xử lý khiếu nại nội bộ theo quy chế; không trao thẩm quyền trọng tài pháp lý.
* **Đơn dịch vụ điện tử (Inspection Service Order / Maintenance Work Order)**: Được sinh ra cho từng thương vụ kiểm định/bảo trì, có giá trị pháp lý theo *Luật Giao dịch điện tử 2023*. Bao gồm: Phạm vi công việc (SOW), Kế hoạch bay kỹ thuật (GSD, Shot list, Overlap), Tiến độ cam kết (SLA), Chi phí dịch vụ Provider và các điều khoản thương mại đã được khóa tại thời điểm ký kết.

### 2. Funding, Settlement và Complaint Hold theo Đối tác được Cấp phép
Các cơ chế dưới đây chỉ áp dụng nếu payment-partner product và điều khoản được các bên chấp thuận hỗ trợ:
1. **Funding theo hợp đồng**: Nếu Service Order yêu cầu nạp trước, Client nạp khoản tiền theo tỷ lệ/điều kiện đã snapshot qua sản phẩm của đối tác được cấp phép (`HELD_IN_ESCROW`). Nếu không yêu cầu nạp trước, không tạo payment gate. Nếu order yêu cầu nhưng đối tác không hỗ trợ, dừng funding-dependent execution hoặc dùng phương án riêng đã được rà soát/chấp thuận; Platform không tự giữ tiền. Chỉ orders có funding requirement mới phải đợi partner confirmation trước khi bắt đầu.
2. **Settlement theo terms (target)**: Sau Client acceptance hoặc điều kiện deemed-acceptance được ghi rõ trong order, chỉ instruct partner nếu product hỗ trợ; không suy diễn settlement tự động khi partner/order terms không cung cấp.
3. **Complaint hold (`FROZEN_DISPUTED`)**: Khi có complaint hợp lệ, chỉ gửi request hold cho phần tiền liên quan nếu product/accepted terms cho phép. `FROZEN_DISPUTED` là workflow state, không xác nhận Platform custody. Release/continuation follows partner confirmation, accepted contract terms and legally competent external mechanisms; Operator handles only internal Platform Terms review.

### 3. Chính sách Cấu hình Động của `PLATFORM_OPERATOR` & Nguyên tắc Contract Snapshot
Toàn bộ các tham số thương mại và vận hành trên sàn **tuyệt đối không bị hardcode**, mà được quản trị tập trung bởi `PLATFORM_OPERATOR` thông qua giao diện Quản trị Chính sách Thương mại:

| Tham số Cấu hình | Ký hiệu | Giá trị áp dụng | Thẩm quyền Quản lý | Phạm vi & Tác động |
| :--- | :---: | :---: | :---: | :--- |
| **Tỷ lệ hoa hồng sàn** | $r$ (`commission_rate`) | Operator ban hành theo kỳ | `PLATFORM_OPERATOR` | Áp dụng thống nhất cho toàn bộ Provider; tính trên doanh thu dịch vụ hợp lệ trước VAT: $C = r \times B$. |
| **Thời hạn nghiệm thu tự động** | $T_{rev}$ (`auto_settlement_review_days`) | Operator cấu hình theo policy | `PLATFORM_OPERATOR` | Thời hạn làm việc Client được quyền thẩm định báo cáo; giá trị được snapshot vào Service Order. |
| **Tỷ lệ nạp trước theo hợp đồng** | $D$ (`required_advance_funding_rate`) | Operator cấu hình theo policy và đối tác | `PLATFORM_OPERATOR` | Tỷ lệ tiền Client cần nạp trước khi khởi công; snapshot vào Service Order, nếu đối tác thanh toán hỗ trợ. |
| **Tỷ lệ bảo lãnh hoàn công** | $H$ (`warranty_retention_rate`) | Nếu áp dụng: Operator cấu hình theo policy | `PLATFORM_OPERATOR` | Tùy chọn retention được disclosure và chấp thuận trong Maintenance Order; nếu không adopted, không giữ khoản này. |
| **Thời hạn bảo hành** | $T_{war}$ (`standard_warranty_days`) | Operator cấu hình theo policy | `PLATFORM_OPERATOR` | Thời hạn bảo hành trước khi giải ngân nốt tiền giữ lại; giá trị được snapshot vào Maintenance Order. |
| **Điều khoản hủy chuyến** | `cancellation_policy` | Operator cấu hình theo policy | `PLATFORM_OPERATOR` | Chính sách, điều kiện và cách tính chi phí hủy được công bố và snapshot vào Service Order. |

* **Nguyên tắc Khóa Bất biến Hợp đồng (Contract Snapshot Pattern)**:
  * Khi Client và Provider ký kết Hợp đồng Dịch vụ (Service Order), hệ thống thực hiện sao chép (snapshot) các giá trị tham số tại thời điểm đó vào bản ghi hợp đồng (`locked_commission_rate`, `locked_review_period_days`, `locked_cancellation_policy`, `locked_advance_funding_rate`, `locked_retention_rate`, `locked_warranty_days`).
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
* **SF-05 (Periodic Schedule Cadence)**: Platform sinh các schedule proposal theo tần suất đã cấu hình cho category; `PLATFORM_OPERATOR` (hoặc vai trò nghiệp vụ được giao trong baseline) kiểm tra/điều chỉnh proposal, sau đó Client chọn một proposal hợp lệ để tạo lịch. Client không tạo schedule trực tiếp. Khi lịch đã chọn đến hạn, hệ thống sinh request package cho MF1 theo Asset + Schedule + Due Cycle identity.

#### 2. Xử lý Luồng Ngoại lệ SF (5 Câu hỏi Bắt buộc)
* **Q1: Dữ liệu đầu vào thiếu hoặc sai?** Hồ sơ Provider thiếu chứng chỉ phi công hoặc bảo hiểm: Operator từ chối duyệt, hệ thống chuyển trạng thái `ADDITIONAL_INFO_REQUIRED`. Tọa độ tài sản nằm trong vùng cấm bay quân sự: Hệ thống gắn cờ cảnh báo `RESTRICTED_AIRSPACE`, yêu cầu phải có giấy phép bay Cục Tác chiến đặc biệt trước khi phát thầu.
* **Q2: Truy cập trái phép / Sai tổ chức?** Client Org A không thể xem tài sản của Client Org B. Provider chưa được duyệt (`PENDING/SUSPENDED`) bị chặn toàn bộ các API xem danh sách tài sản hay nhận yêu cầu.
* **Q3: Thao tác đồng thời / Trùng lặp?** Mã số thuế và Mã tài sản (Asset Code) có ràng buộc duy nhất (Unique Constraint) trong phạm vi tổ chức. Gửi lại form bị chặn ngay với mã lỗi `DUPLICATE_ENTITY`.
* **Q4: Dịch vụ ngoài / Mạng lỗi?** Cổng tra cứu `cambay.mod.gov.vn` bị gián đoạn: Hệ thống lưu trạng thái `AIRSPACE_CHECK_PENDING`, cho phép lưu hồ sơ tài sản nhưng đánh dấu cần thẩm định không phận thủ công trước khi phát thầu.
* **Q5: Từ chối / Hủy giữa chừng?** Provider bị Operator từ chối có quyền bổ sung giấy tờ và gửi thẩm định lại tối đa 3 lần.

---

### MF1 — Yêu cầu Khảo sát, Đấu thầu Báo giá & Thanh toán có Điều kiện (Survey Request, Quotation Sourcing & Conditional Funding)

**Mục tiêu**: Khởi tạo nhu cầu kiểm định, kết nối Provider đủ điều kiện thông qua chỉ định hoặc đấu thầu mở (RFQ), ký hợp đồng điện tử 3 bên và nạp khoản tiền theo tỷ lệ đã cấu hình vào cơ chế thanh toán có điều kiện.

**Tác nhân chính**: `Client`, `Platform Operator`, `Provider Manager`, `System`.

#### 1. Quy trình chi tiết (Main Sequence)

| Bước | Vai trò / Lane | Hoạt động chi tiết | Sản phẩm đầu ra |
| :--- | :--- | :--- | :--- |
| **MF1-01** | Client | Khởi tạo Yêu cầu khảo sát (từ lịch định kỳ SF-05 hoặc đột xuất). Chọn phương thức chọn thầu: (A) **Chỉ định trực tiếp** Provider đối tác quen thuộc; hoặc (B) **Chào thầu mở (Open RFQ)** cho các Provider trong khu vực. Nêu rõ mục tiêu kiểm tra (tìm nứt bê tông, kiểm tra ăn mòn dầm thép). | Yêu cầu kiểm tra (RFQ) |
| **MF1-02** | Platform Operator | *(Tùy chọn hỗ trợ)*: Kiểm tra yêu cầu chào thầu mở của Client, hỗ trợ kết nối và gửi thông báo đến các Provider có năng lực và phạm vi hoạt động phù hợp. | Danh sách Provider tiếp cận RFQ |
| **MF1-03** | Provider Manager | Xem xét yêu cầu, khảo sát địa hình sơ bộ từ xa và lập **Báo giá dịch vụ (Quotation)**: Chỉ gồm (1) Chi phí nhân lực bay hiện trường; (2) Chi phí kỹ thuật chuyên môn; (3) Chi phí đi lại/triển khai hợp lệ; (4) Thuế VAT của Provider. **Tuyệt đối không tính phí xử lý AI/MinIO của Sàn vào báo giá.** | Báo giá dịch vụ (v1, v2) |
| **MF1-04** | Client | Xem xét các báo giá cạnh tranh. Có thể yêu cầu điều chỉnh (Revision) hoặc chọn Báo giá phù hợp nhất để chấp thuận. | Báo giá được chấp thuận |
| **MF1-05** | System | Khởi tạo **Hợp đồng Dịch vụ Điện tử (Inspection Service Order)**: Thực hiện **Contract Snapshot** để lưu tỷ lệ hoa hồng $r$, thời hạn nghiệm thu $T_{rev}$, tỷ lệ nạp trước $D$ và chính sách hủy do `PLATFORM_OPERATOR` ban hành tại thời điểm ký vào bản ghi hợp đồng. | Hợp đồng điện tử sẵn sàng ký |
| **MF1-06** | Client & Provider Manager | Hai bên chấp thuận/ký kết Service Order điện tử theo điều khoản đã công bố và pháp luật áp dụng. Nếu order quy định nạp trước, Client thanh toán qua đối tác được cấp phép; nếu không, áp dụng mốc thanh toán đã thỏa thuận. Funding status không tự quyết định thời điểm hình thành hợp đồng. | Service Order được chấp thuận; trạng thái funding theo order/đối tác |

#### 2. Chính sách Hủy Hợp đồng & Rủi ro Thời tiết (Theo Snapshot hợp đồng)
* **Hủy trước khi thực hiện**: Hoàn/khấu trừ khoản tiền theo điều khoản hủy đã công bố và snapshot vào Service Order; không mặc định cửa sổ hoặc tỷ lệ hoàn tiền toàn cục.
* **Hủy sau khi Provider đã phát sinh chi phí**: Áp dụng điều khoản chi phí hủy/chi phí đã thực hiện trong Service Order đã chấp thuận; không áp một tỷ lệ hoặc mốc thời gian mặc định cho mọi đơn.
* **Bất khả kháng do thời tiết xấu**: Nếu có bão, mưa lớn hoặc gió vượt ngưỡng an toàn bay, hai bên thống nhất dời lịch bay mà không phạt tiền và không tính vi phạm SLA.

#### 3. Xử lý Luồng Ngoại lệ MF1 (5 Câu hỏi Bắt buộc)
* **Q1: Dữ liệu đầu vào thiếu hoặc sai?** Yêu cầu khảo sát thiếu thông tin vị trí công trình hoặc mục tiêu kiểm định: Hệ thống yêu cầu Client bổ sung đầy đủ trước khi mở cổng nhận báo giá.
* **Q2: Truy cập trái phép / Sai tổ chức?** Provider A không thể xem nội dung giá thầu của Provider B trong cùng một gói RFQ.
* **Q3: Thao tác đồng thời / Trùng lặp?** Client bấm thanh toán 2 lần: Idempotency key và partner event/instruction identity ngăn hai chỉ thị funding hoặc giao dịch trùng cho cùng order/milestone.
* **Q4: Dịch vụ ngoài / Mạng lỗi?** Cổng thanh toán timeout khi order yêu cầu funding: đơn hàng giữ trạng thái `PAYMENT_PENDING`; chỉ trạng thái đã xác thực từ đối tác mới xác nhận funding. Nếu order không yêu cầu nạp trước, luồng thực hiện theo mốc thanh toán thay thế đã được các bên chấp thuận.
* **Q5: Từ chối / Hủy giữa chừng?** Client hủy yêu cầu trước khi chọn báo giá: RFQ tự động đóng (`CANCELLED`), thông báo cho các Provider đã nộp báo giá.

---

### MF2 — Lập Kế hoạch Bay Drone Chuyên dụng & Thẩm định Không phận (Drone Mission Planning & Airspace Clearance) 🚀 [FLOW NỔI BẬT DRONE]

> **Trọng tâm công nghệ Drone**: Đây là luồng kỹ thuật chuyên sâu làm nổi bật năng lực quản trị bay trắc địa và pháp lý không phận của nền tảng, thiết lập các tham số trắc địa ảnh chuẩn mực trước khi cất cánh.

**Tác nhân chính**: `Provider Manager`, `Inspector` (Phi công), `Platform Operator`, `System`.

#### 1. Quy trình chi tiết (Main Sequence)

| Bước | Vai trò / Lane | Hoạt động chi tiết | Sản phẩm đầu ra |
| :--- | :--- | :--- | :--- |
| **MF2-01** | Inspector | **Tính toán trắc địa ảnh & Độ phân giải mặt đất (Photogrammetric GSD Planning)**: Dựa trên yêu cầu phát hiện vết nứt của SOW (theo ngưỡng kích thước khuyết tật và GSD đã thỏa thuận trong SOW). Inspector nhập thông số camera/cảm biến drone (tiêu cự focal length, kích thước cảm biến sensor size, độ phân giải ảnh); hệ thống tính toán ra **Độ cao bay an toàn (AGL - Above Ground Level)** và **Khoảng cách chụp tối ưu** tới bề mặt kết cấu. | Tham số GSD & Độ cao bay chuẩn |
| **MF2-02** | Inspector | **Thiết lập tỷ lệ chồng phủ ảnh (Image Overlap Calculation)**: Cấu hình tỷ lệ chồng phủ dọc (Forward Overlap) và ngang (Side Overlap) theo loại cấu kiện, cảm biến, mục tiêu GSD và phương án bay đã duyệt để đảm bảo không bỏ sót điểm mù kết cấu và phục vụ mô hình hóa khuyết tật. | Tham số Overlap đạt chuẩn trắc địa |
| **MF2-03** | Inspector | **Xây dựng Danh mục Góc chụp Cấu kiện (Structural Shot List & Gimbal Pitch)**: Lập shot list theo từng cấu kiện, thiết lập hướng quan sát và góc gimbal phù hợp với camera, hình học bề mặt, mục tiêu GSD và tiêu chí nghiệm thu trong SOW. Waypoints/route coordinates là tùy chọn: ghi vào Mission Plan nếu Provider dùng lập trình waypoint; nếu không, Inspector dùng shot list đã duyệt để bay thủ công. | Structural Shot List hoàn chỉnh; waypoint plan nếu sử dụng |
| **MF2-04** | Inspector & System | **Thẩm định An toàn Không phận Số (Airspace Digital Clearance)**: Hệ thống tự động nạp tọa độ không gian 3D của khu vực bay, đối chiếu với Cổng thông tin Vùng cấm bay (`cambay.mod.gov.vn` theo QĐ 18/2020/QĐ-TTg). Nếu tọa độ nằm trong hành lang an toàn hàng không hoặc khu vực hạn chế bay, hệ thống kích hoạt cảnh báo bắt buộc đính kèm giấy phép đặc biệt. | Báo cáo thẩm định không phận số |
| **MF2-05** | Provider Manager | **Kiểm soát Pháp lý Bay theo Luật PKND 2024 & NĐ 288/2025/NĐ-CP**: Đính kèm số hiệu Giấy phép bay do Cục Tác chiến - Bộ Tổng Tham mưu cấp; chọn phi công `Inspector` có chứng chỉ bay hợp lệ; kiểm tra mã định danh drone của Bộ Quốc phòng; kiểm tra cam kết không có xung đột lợi ích. | Hồ sơ cấp phép bay hoàn tất |
| **MF2-06** | Provider Manager | Phê duyệt Kế hoạch Bay Drone (Drone Mission Plan), ký lệnh bay điện tử và phát hành Gói nhiệm vụ bay (Mission Package) cho phi công. Chuyển trạng thái đơn hàng sang **`READY_FOR_FLIGHT`**. | Kế hoạch bay được phê duyệt (`READY_FOR_FLIGHT`) |

#### 2. Xử lý Luồng Ngoại lệ MF2 (5 Câu hỏi Bắt buộc)
* **Q1: Dữ liệu đầu vào thiếu hoặc sai?** Inspector thiết lập thông số camera/độ cao không đáp ứng GSD hoặc shot requirement trong SOW: không phê duyệt Mission Plan cho đến khi sửa thiết bị/phương án. Waypoints chỉ được yêu cầu nếu route dùng waypoint; chúng không bắt buộc cho phương án bay tay đã đáp ứng tiêu chí nghiệm thu.
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
| **MF3-01** | Inspector | Mở ứng dụng Web/Mobile tại hiện trường, kích hoạt phiên khảo sát (`IN_PROGRESS`) và tự điều khiển drone thủ công theo quy định an toàn. Thực hiện shot list đã duyệt; nếu mission plan có waypoint thì có thể dùng waypoint, nếu không thì phi công tự điều khiển theo cấu kiện/góc chụp/yêu cầu SOW. Platform không điều khiển drone hoặc yêu cầu tự động hóa đường bay. | Phiên khảo sát hiện trường được ghi nhận |
| **MF3-02** | Inspector | Tải toàn bộ tệp ảnh/video độ phân giải cao thu được lên hệ thống MinIO do Platform cung cấp qua giao thức phân đoạn (Chunked Upload). | Bằng chứng kiểm định thô |
| **MF3-03** | System (Platform MinIO & Ingestion) | Tự động bóc tách **Dữ liệu Không gian Telemetry (Spatial Telemetry Metadata)**: Tọa độ GPS 3D, độ cao tương đối AGL, góc nghiêng gimbal camera, timestamp; tự động tính mã băm toàn vẹn **SHA-256** cho từng file ảnh. Từ chối tệp trùng lặp. | Bằng chứng số được bảo vệ toàn vẹn |
| **MF3-04** | System (Platform YOLO AI Service) | Pipeline AI YOLO do Platform trực tiếp host tự động quét toàn bộ ảnh hợp lệ; phát hiện các khuyết tật (vết nứt bê tông, gỉ sét cốt thép, bong tróc). Hệ thống **tự động tính kích thước vật lý thực tế của vết nứt (chiều dài mm, bề rộng mm)** bằng cách nhân kích thước pixel nhận diện với giá trị **GSD** đã thiết lập ở MF2. Tạo danh sách **Ứng viên lỗi (Defect Candidates)** kèm hộp bao (Bounding Box). | Danh mục ứng viên lỗi kèm kích thước vật lý (GSD) |
| **MF3-05** | Inspector (Người bay) | Kiểm tra trực quan từng ảnh và từng ứng viên AI: Chọn **Xác nhận (Confirm)**, **Sửa đổi (Modify)**, hoặc **Bác bỏ (Reject)**. Nếu AI bỏ sót, Inspector **thêm lỗi thủ công (Manual Finding)**. Hoàn tất trả lời checklist kỹ thuật. | Hồ sơ khiếm khuyết đã xác minh |
| **MF3-06** | System | Tự động tổng hợp Bản thảo Báo cáo Kỹ thuật (Draft Report v1.0) kết hợp checklist, dữ liệu telemetry, ảnh khuyết tật và phần tóm tắt thuyết minh do **Trợ lý AI LLM của Platform** tự động soạn thảo. Loại bỏ toàn bộ ứng viên AI bị bác bỏ khỏi báo cáo chính thức. | Bản thảo báo cáo kỹ thuật |
| **MF3-07** | Inspector (Người review chéo) | **Thẩm định chéo kỹ thuật (Internal Peer Review)**: Một Inspector độc lập khác trong cùng Provider thẩm định tính chính xác của báo cáo. *Quy tắc bắt buộc: Người bay tuyệt đối không được tự duyệt báo cáo của mình*. | Biên bản thẩm định chéo kỹ thuật |
| **MF3-08** | Inspector (Người bay) | Nếu reviewer yêu cầu chỉnh sửa: cập nhật lại báo cáo (v1.1) và nộp lại. Nếu đạt chuẩn, reviewer ký duyệt kỹ thuật (`TECHNICALLY_APPROVED`). | Báo cáo đạt chuẩn kỹ thuật |
| **MF3-09** | Provider Manager | Kiểm tra tổng thể hồ sơ bàn giao so với Service Order và chính thức **Ký phát hành Báo cáo (Release Final Report)** gửi Client. Hệ thống tự động kích hoạt đồng hồ đếm ngược thời hạn nghiệm thu theo $T_{rev}$ đã snapshot trong hợp đồng. | Báo cáo chính thức & Kích hoạt đồng hồ nghiệm thu |

#### 2. Xử lý Luồng Ngoại lệ MF3 (5 Câu hỏi Bắt buộc)
* **Q1: Dữ liệu đầu vào thiếu hoặc sai?** Ảnh tải lên bị mờ, rung lắc hoặc thiếu tọa độ GPS do mất tín hiệu vệ tinh: Hệ thống gắn cờ cảnh báo `METADATA_INCOMPLETE`. Nếu ảnh không đủ chuẩn đo lường vết nứt theo GSD, Inspector bắt buộc phải chụp lại ngay tại hiện trường.
* **Q2: Truy cập trái phép / Sai tổ chức?** Tác giả báo cáo cố tình chọn chính mình làm Peer Reviewer: Hệ thống chặn đứng ở tầng API với mã lỗi `PEER_REVIEW_SELF_APPROVAL_PROHIBITED`.
* **Q3: Thao tác đồng thời / Trùng lặp?** Mạng chập chờn khiến Inspector tải lên 1 tệp nhiều lần: Hệ thống đối soát mã băm SHA-256; nếu trùng lặp, bỏ qua file thứ hai mà không tạo bản ghi rác.
* **Q4: Dịch vụ ngoài / Mạng lỗi?** Dịch vụ AI YOLO của Platform bị quá tải hoặc tạm ngừng phục vụ: Hệ thống tự động chuyển sang cơ chế **Manual Fallback**, cho phép Inspector tự khoanh vùng và đo vẽ vết nứt thủ công trên ảnh, tiến độ bàn giao báo cáo không bị đình trệ.
* **Q5: Từ chối / Hủy giữa chừng?** Peer Reviewer phát hiện vết nứt bị đánh giá sai cấp độ nghiêm trọng: Từ chối duyệt, trả về trạng thái `REVISION_REQUIRED` kèm ghi chú kỹ thuật; tác giả phải kiểm tra lại dữ liệu đo lường GSD và hiệu chỉnh kết luận.

---

### MF4 — Nghiệm thu Báo cáo, Quyết toán Theo Điều khoản & Xử lý Khiếu nại Nội bộ (Report Acceptance, Conditional Settlement & Internal Complaint Handling)

**Mục tiêu**: Khách hàng thẩm định kết quả theo policy đã snapshot; đối tác thanh toán xử lý các mốc settlement theo điều khoản được chấp thuận; hoặc `PLATFORM_OPERATOR` điều phối xử lý khiếu nại nội bộ theo Platform Terms. Operator không phải trọng tài pháp lý và không tự ra lệnh vượt ngoài hợp đồng/sản phẩm đối tác.

**Tác nhân chính**: `Client`, `Provider Manager`, `PLATFORM_OPERATOR` (xử lý nội bộ), đối tác thanh toán được cấp phép khi áp dụng, `System`.

#### 1. Quy trình chi tiết (Main Sequence)

| Bước | Vai trò / Lane | Hoạt động chi tiết | Sản phẩm đầu ra |
| :--- | :--- | :--- | :--- |
| **MF4-01** | Client | Xem xét báo cáo kiểm định hoàn chỉnh trên Web/Mobile (ảnh khuyết tật độ phân giải cao, vị trí 3D, số đo vết nứt). Bắt đầu tính thời hạn nghiệm thu $T_{rev}$ theo giá trị snapshot đã khóa trong hợp đồng MF1. | Báo cáo đang thẩm định nghiệm thu |
| **MF4-02a** | Client (Nhánh Nghiệm thu) | Client hài lòng với chất lượng -> Bấm **"Nghiệm thu (Accept)"**. | Quyết định nghiệm thu |
| **MF4-02b** | System (Nhánh Auto-Settlement) | Quá thời hạn $T_{rev}$ đã snapshot, nếu Client không phản hồi và không mở tranh chấp hợp lệ -> Hệ thống tự động kích hoạt **Nghiệm thu mặc định (Auto-Settlement)** nhằm bảo vệ dòng tiền chính đáng cho Provider. | Quyết định nghiệm thu tự động |
| **MF4-03** | System và đối tác thanh toán | Báo cáo chuyển sang trạng thái bất biến (`COMPLETED`). **Giải ngân theo tỷ lệ hoa hồng đã khóa tại hợp đồng**: Với cơ sở tính phí $B$ và tỷ lệ hoa hồng $r$ đã khóa snapshot, hoa hồng sàn $C = r \times B$. Provider nhận số tiền ròng $B - C$; Platform ghi nhận hoa hồng $C$ kèm hóa đơn VAT riêng. Provider xuất hóa đơn dịch vụ đủ giá trị cho Client. | Dòng tiền tất toán (`DISBURSED`) & Hóa đơn riêng biệt |
| **MF4-04** | Client (Nhánh Yêu cầu Làm rõ) | Nếu có nội dung kỹ thuật chưa rõ ràng, Client gửi yêu cầu giải trình. Provider Manager giải trình hoặc phát hành bản báo cáo hiệu chỉnh (Client không được trực tiếp sửa nội dung chuyên môn). | Báo cáo giải trình hiệu chỉnh |
| **MF4-05** | Client / Provider (Nhánh Mở Tranh chấp) | Khi có mâu thuẫn nghiêm trọng (ảnh mờ sai lệch GSD cam kết, bỏ sót khuyết tật nghiêm trọng, làm rơi drone gây hư hỏng tài sản): Một trong hai bên bấm **"Mở Tranh chấp (Open Dispute)"**. | Hồ sơ tranh chấp (`OPENED`) |
| **MF4-06** | System và đối tác thanh toán (nếu được hỗ trợ) | Ghi nhận complaint state. Chỉ gửi yêu cầu hold cho phần tiền liên quan nếu order terms và partner product cho phép; không gọi platform ledger là khoản tiền bị phong tỏa. | Complaint đang mở; partner status riêng nếu có |
| **MF4-07** | Platform Operator | **Thụ lý nội bộ theo Platform Terms**: Nhận phản hồi/chứng cứ, đối chiếu SOW MF1, Mission Plan MF2, bằng chứng MF3 và ý kiến các bên; ghi nhận lý do, scope xem xét và đường khiếu nại/ngoại lệ. | Hồ sơ xử lý nội bộ có audit trail |
| **MF4-08** | Platform Operator & đối tác thanh toán (nếu được hỗ trợ) | Ghi nhận internal outcome/biện pháp hợp đồng được chấp thuận và gửi cho các bên. Chỉ instruct partner nếu sản phẩm và hợp đồng cho phép; outcome không phải phán quyết trọng tài pháp lý và không loại trừ cơ quan tài phán. | Internal complaint outcome; partner action/status nếu có |

#### 2. Outcome có thể ghi nhận trong xử lý khiếu nại nội bộ theo Platform Terms
* **Lỗi chất lượng có thể khắc phục (ví dụ ảnh/shot item thiếu so với SOW)**:
  - Operator có thể ghi nhận/đề xuất reshoot theo remedy đã được các bên chấp thuận trong Order/Terms; thời hạn là giá trị cụ thể đã snapshot, không phải lệnh pháp lý độc lập. Hold (nếu có) chỉ tồn tại tại partner khi sản phẩm và hợp đồng hỗ trợ.
* **Vi phạm nghiêm trọng / yêu cầu chấm dứt hoặc hoàn tiền**:
  - Operator ghi nhận căn cứ và phối hợp các bên theo hợp đồng, chứng cứ, pháp luật áp dụng và quyền của các bên. Phạt vi phạm, chấm dứt, đình chỉ hoặc chuyển tiền không tự động; chỉ thực hiện khi có căn cứ hợp đồng/pháp luật và đúng thẩm quyền.
* **Khiếu nại không có căn cứ**:
  - Operator ghi nhận kết quả xử lý nội bộ và lý do; đối tác chỉ xử lý khoản tiền đủ điều kiện theo hợp đồng/sản phẩm. Nếu có hoàn/giảm giá dịch vụ thực tế, commission được điều chỉnh theo policy và chứng từ liên quan.

#### 3. Xử lý Luồng Ngoại lệ MF4 (5 Câu hỏi Bắt buộc)
* **Q1: Dữ liệu đầu vào thiếu hoặc sai?** Đơn khiếu nại không có ảnh/video bằng chứng chứng minh: Operator yêu cầu bổ sung theo thời hạn xử lý đã công bố; quá hạn, khiếu nại được xử lý theo Platform Terms.
* **Q2: Truy cập trái phép / Sai tổ chức?** Nhân viên không có thẩm quyền trong Client Org cố tình bấm mở tranh chấp: Hệ thống chặn quyền ở tầng API, chỉ tài khoản đại diện pháp lý mới được mở tranh chấp.
* **Q3: Thao tác đồng thời / Trùng lặp?** Client vừa gửi nghiệm thu vừa gửi complaint: order transition phải serialize/idempotent; chỉ một state transition hợp lệ được ghi. Complaint chỉ gửi partner hold request nếu policy/order và partner product cho phép.
* **Q4: Dịch vụ ngoài / Mạng lỗi?** Notification gateway lỗi: complaint/outcome record vẫn được lưu với audit trail; không suy ra partner funds state khi webhook/status unavailable; cung cấp in-app retry/status.
* **Q5: Từ chối / Hủy giữa chừng?** Một bên phản đối outcome nội bộ hoặc remedy đề xuất: lưu phản hồi/appeal theo Platform Terms; không tự động phạt, chuyển tiền hoặc hạn chế quyền ngoài accepted terms/law; các bên giữ quyền external remedy.

---

### MF5 — Xử lý Khiếm khuyết, Đơn hàng Bảo trì & Tiền Bảo lãnh Hoàn công (Defect Rectification, Maintenance & Retention)

**Mục tiêu**: Chuyển các khuyết tật từ báo cáo drone thành đơn hàng sửa chữa công trình, kiểm soát phát sinh chi phí, nghiệm thu ảnh đối chứng Before/After và thực hiện các điều khoản funding/retention/warranty nếu các bên đã chấp thuận và payment-partner product hỗ trợ.

**Tác nhân chính**: `Client`, `Maintenance Provider Manager`, `Maintenance Engineer`, `Platform Operator`, `System`.

#### 1. Quy trình chi tiết (Main Sequence)

| Bước | Vai trò / Lane | Hoạt động chi tiết | Sản phẩm đầu ra |
| :--- | :--- | :--- | :--- |
| **MF5-01** | Client | Chọn các khuyết tật đã xác minh từ Báo cáo MF4 để tạo **Phiếu yêu cầu bảo trì (Maintenance Ticket)**. | Maintenance Ticket |
| **MF5-02** | Maintenance Provider Manager | Khảo sát hiện trường (qua ảnh/telemetry MF3 hoặc trực tiếp); lập Phương án kỹ thuật, dự toán vật tư và Báo giá bảo trì. Báo giá phải nêu rõ có/không áp dụng retention, cơ sở tính, policy/version, điều kiện và thời hạn warranty nếu có. | Báo giá bảo trì & Đơn dịch vụ |
| **MF5-03** | System | Khởi tạo **Đơn dịch vụ bảo trì (Maintenance Order)**: snapshot phiên bản policy và các giá trị hoa hồng, funding, retention (nếu các bên chấp thuận), warranty và hủy áp dụng cho đơn. Chỉ yêu cầu nạp trước nếu policy/order quy định và sản phẩm của đối tác thanh toán hỗ trợ các điều kiện đó. | Maintenance Order và trạng thái giao dịch do đối tác xác nhận (nếu có) |
| **MF5-04** | Maintenance Engineer | Tiếp nhận phân công thi công. Đến hiện trường sửa chữa (trám trét vết nứt bê tông, xử lý ăn mòn, thay cáp). **Bắt buộc chụp và nạp ảnh đối chứng Trước và Sau thi công (Before/After Evidence)** lên MinIO kèm nhật ký vật tư. | Nhật ký thi công & Cặp ảnh đối chứng Before/After |
| **MF5-05** | Maintenance Engineer & Provider Manager | Nếu phát hiện hư hỏng ngầm vượt quá dự toán: dừng phần việc phát sinh, lập **Yêu cầu thay đổi (Change Order)**. Client phê duyệt phiên bản mới; khoản nạp thêm chỉ bắt buộc nếu order đã chấp thuận yêu cầu và payment-partner product hỗ trợ điều kiện đó. | Change Order được duyệt và funding state theo order |
| **MF5-06** | Client & Provider Manager | **Nghiệm thu hoàn công**: Client đối soát cặp ảnh Before/After. Nếu đạt chuẩn, Client ký nghiệm thu theo order đã chấp thuận. | Kết quả nghiệm thu; partner instruction nếu được quy định/hỗ trợ |
| **MF5-07** | System và đối tác thanh toán | Theo các milestone và retention tùy chọn đã snapshot, đối tác giải ngân phần đủ điều kiện sau khi trừ một lần commission; nếu retention được chọn, giữ phần $H$ chỉ trong phạm vi sản phẩm/điều khoản đã chấp thuận. Kích hoạt warranty duration đã snapshot. | Partner settlement state và trạng thái maintenance được cập nhật |
| **MF5-08** | Client & Platform Operator | Khi warranty duration đã snapshot hết hạn và điều kiện release được đáp ứng, `PLATFORM_OPERATOR` phối hợp yêu cầu partner release retention chỉ khi retention đã được adopted và partner product cho phép. Không áp commission lần hai lên consideration đã tính phí. Đóng ticket khi các nghĩa vụ đã hoàn tất. | Partner confirmation (nếu retention áp dụng) & Ticket đóng |

#### 2. Nhánh Xử lý Rework / Re-inspection / Warranty Complaint
* **Yêu cầu làm lại (Rework)**: Nếu công việc không đạt SOW/Order, Client yêu cầu remedy theo điều khoản chất lượng/warranty đã chấp thuận; không tự suy diễn miễn phí ngoài scope/terms.
* **Yêu cầu kiểm tra lại bằng Drone (Re-inspection)**: Client có thể mở request mới liên kết với defect/work order để quay lại MF1 sourcing và MF2 mission planning.
* **Warranty complaint**: Nếu retention được adopt và còn tồn tại tại partner, khiếu nại có thể tạm dừng release theo product/accepted terms. `PLATFORM_OPERATOR` điều phối complaint process; không tự tịch thu, chiếm giữ hoặc chuyển khoản retention.

#### 3. Xử lý Luồng Ngoại lệ MF5 (5 Câu hỏi Bắt buộc)
* **Q1: Dữ liệu đầu vào thiếu hoặc sai?** Kỹ sư nộp nghiệm thu nhưng thiếu ảnh đối chứng Before/After: Hệ thống khóa nút Submit, bắt buộc phải đủ cặp ảnh đối chứng mới được trình nghiệm thu.
* **Q2: Truy cập trái phép / Sai tổ chức?** Đơn vị bảo trì A không thể xem hồ sơ sửa chữa của Đơn vị bảo trì B.
* **Q3: Thao tác đồng thời / Trùng lặp?** Kỹ sư gửi 2 Change Order liên tiếp: Hệ thống chỉ cho phép duy nhất 1 Change Order ở trạng thái `PENDING_APPROVAL` tại một thời điểm.
* **Q4: Dịch vụ ngoài / Mạng lỗi?** Mất sóng di động tại hầm công trình: Mobile app lưu ảnh offline vào bộ nhớ mã hóa an toàn thiết bị (`flutter_secure_storage`), tự động đồng bộ lên MinIO khi có mạng trở lại.
* **Q5: Từ chối / Hủy giữa chừng?** Client từ chối phê duyệt Change Order: đơn vị bảo trì dừng phần phát sinh và chỉ tiếp tục phạm vi đã duyệt. Cancellation/refund/retention follow the accepted order terms; partner action occurs only when its product supports them.

---

## V. Ma trận Phân quyền & Trách nhiệm (RACI Matrix)

| Quy trình / Nghiệp vụ cốt lõi | `PLATFORM_ADMIN` | `PLATFORM_OPERATOR` | `CLIENT` | `PROVIDER_MANAGER` | `INSPECTOR` | `MAINTENANCE_ENGINEER` |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **SF: Thẩm định Provider & Khai báo Drone** | I | **A / R** | I | **R** | C | - |
| **SF: Khai báo Tài sản & Cảnh báo Cấm bay** | I | C | **A / R** | - | - | - |
| **Chính sách: Cấu hình Động Tham số Thương mại** | I | **A / R** | I | I | - | - |
| **MF1: Đấu thầu RFQ & Báo giá Kiểm định** | - | C | **A** | **R** | - | - |
| **MF1: Ký Hợp đồng & Nạp tiền theo chính sách Escrow** | I | C | **A / R** | **R** | - | - |
| **MF2: Lập Kế hoạch Bay (GSD, Overlap, Shot List)** | - | - | I | **A** | **R** | - |
| **MF2: Kiểm tra Không phận Số & Giấy phép Bay** | I | C | I | **A / R** | **R** | - |
| **MF3: Khảo sát Hiện trường & Bóc tách Telemetry** | - | - | I | I | **A / R** | - |
| **MF3: Nhận diện AI YOLO & Xác minh Lỗi (GSD)** | - | - | - | I | **A / R** | - |
| **MF3: Thẩm định chéo (Internal Peer Review)** | - | - | - | I | **A / R** | - |
| **MF3: Ký phát hành Báo cáo Kỹ thuật QA** | - | - | I | **A / R** | I | - |
| **MF4: Nghiệm thu Báo cáo & Quyết toán Escrow** | I | C | **A / R** | I | - | - |
| **MF4: Xử lý khiếu nại nội bộ theo Terms** | I | **A / R** | C | C | C | - |
| **MF5: Tạo Ticket & Báo giá Bảo trì** | - | - | **A** | **R** | - | C |
| **MF5: Ký quỹ Bảo trì & Thi công Before/After** | - | - | **A** | I | - | **A / R** |
| **MF5: Nghiệm thu Hoàn công & Tất toán Bảo hành** | I | **R** | **A** | I | - | I |

*Ghi chú*:
* **R (Responsible)**: Người trực tiếp thực hiện công việc.
* **A (Accountable)**: Người chịu trách nhiệm phê duyệt cuối cùng và sở hữu kết quả.
* **C (Consulted)**: Người được tham vấn ý kiến, cung cấp dữ liệu đối soát.
* **I (Informed)**: Người được nhận thông báo kết quả.
