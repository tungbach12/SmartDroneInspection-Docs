---
title: "SmartDroneInspection Multi-Provider Business Flows"
document_type: business-flow-reference
purpose: "Đặc tả chi tiết 5 Luồng nghiệp vụ cốt lõi (MF1–MF5) cho Nền tảng Kiểm định Hạ tầng bằng Drone nhiều Nhà cung cấp (Multi-Provider Platform)"
version: "2.0"
updated: 2026-10-03
---

# SmartDroneInspection Multi-Provider Business Flows (v2.0)

> Tài liệu này là đặc tả chuẩn mực về 5 Luồng nghiệp vụ chính thức (MF1–MF5) của nền tảng SmartDroneInspection. Toàn bộ thiết kế được xây dựng dựa trên mô hình Nền tảng số trung gian (Intermediary Platform), cơ chế Hợp đồng điện tử, Dòng tiền Ký quỹ (Escrow), Trọng tài phân xử tranh chấp nội bộ, tuân thủ nghiêm ngặt Hướng dẫn tránh lỗi Capstone (`error-prevention.md`) và căn cứ theo hệ thống pháp luật Việt Nam mới nhất.

---

## I. Căn cứ Pháp lý Việt Nam Áp dụng

> **Phạm vi pháp lý:** Đây là bản thiết kế mục tiêu của dự án đồ án. Các văn bản dưới đây là khung tham chiếu đang được rà soát; không được suy luận rằng nền tảng đã hoạt động, đã tuân thủ, đã tích hợp ngân hàng/đơn vị thanh toán, hoặc đã được cấp bất kỳ giấy phép nào.

1. **Luật Phòng không nhân dân 2024 (Luật số 49/2024/QH15, hiệu lực từ 01/07/2025), được sửa đổi bởi Luật số 98/2025/QH15, hướng dẫn bởi Nghị định 198/2025/NĐ-CP và Nghị định 288/2025/NĐ-CP**:
   - Dự thảo mục tiêu dùng khung drone hiện hành để mô hình hoá kiểm tra định danh UAV, đào tạo/giấy phép điều khiển, phép bay và kiểm soát không phận.
   - Không dùng Nghị định 36/2008/NĐ-CP và Nghị định 79/2011/NĐ-CP như văn bản còn hiệu lực duy nhất; trường hợp hủy bỏ/kế thừa cụ thể cần đối chiếu văn bản ký chính thức trước khi triển khai.
2. **Quyết định số 18/2020/QĐ-TTg & Cổng thông tin Vùng cấm bay (`cambay.mod.gov.vn`)**:
   - Tra cứu tham khảo công khai về khu vực cấm/hạn chế bay. Việc áp dụng cho một chuyến bay cụ thể cần kiểm tra phép bay và ranh giới có thẩm quyền.
3. **Luật Giao dịch điện tử 2023 (Luật số 20/2023/QH15, hiệu lực từ 01/07/2024)**:
   - Dùng làm căn cứ thiết kế Hợp đồng điện tử và quản lý thông điệp dữ liệu.
   - MinIO, GPS, SHA-256 và timestamp chỉ hỗ trợ tính toàn vẹn/truy xuất nguồn gốc; tài liệu không coi chúng tự động là chứng cứ hợp pháp, đã đủ nhận dạng, hoặc đã được Toà án/trọng tài thương mại chấp nhận.
4. **Luật Bảo vệ quyền lợi người tiêu dùng 2023 (Luật số 19/2023/QH15, hiệu lực từ 01/07/2024)** và văn bản chi tiết/hợp nhất có liên quan:
   - Dùng làm căn cứ thiết kế trách nhiệm công khai quy chế, minh bạch Provider, và tiếp nhận khiếu nại.
   - Mua dịch vụ kiểm định cho mục đích thương mại không mặc nhiên thuộc hoặc không thuộc phạm vi người tiêu dùng; cần xét mục đích giao dịch cụ thể. Phán quyết nội bộ của Sàn không thay thế quyền khiếu nại, kiện tụng, hoặc trọng tài thương mại hợp pháp.
5. **Khung pháp luật thương mại điện tử hiện hành từ 01/07/2026**:
   - Thiết kế mục tiêu trước khi vận hành thật phải đối chiếu **Luật Thương mại điện tử 2025 (Luật số 122/2025/QH15)** và **Nghị định 248/2026/NĐ-CP**, vì đây là khung pháp lý mới hơn Nghị định 52/2013/NĐ-CP và Nghị định 85/2021/NĐ-CP. Không được trình bày NĐ 52/2013 + NĐ 85/2021 như toàn bộ khung hiện hành.
6. **Thanh toán, bảo đảm thanh toán và ký quỹ**:
   - Tài liệu mô tả tài khoản/thỏa thuận bảo vệ giao dịch cần tích hợp ngân hàng hoặc đơn vị trung gian thanh toán được cấp phép. Platform không tự xưng là ngân hàng và không tự mở hoạt động giữ tiền nếu chưa được phân loại pháp lý và ký hợp đồng thanh toán phù hợp.
   - Ký quỹ theo Điều 330 Bộ luật Dân sự 2015 phải có tổ chức tín dụng phong tỏa theo luật định; sổ cái trễ thanh toán nội bộ của Platform không được gọi là ký quỹ pháp lý nếu không đáp ứng điều kiện đó.
   - 100% trả trước, 5 ngày tự động nghiệm thu, tỷ lệ hoa hồng, giữ lại 10%, phạt di chuyển 20%, bay lại trong 48 giờ và yêu cầu bảo hiểm là chính sách thương mại đề xuất, không phải nghĩa vụ pháp luật đã được xác minh.

---

## II. Hệ thống Vai trò & Khối Tác quyền (Actor Zones & 6 Canonical Roles)

Hệ thống được tổ chức thành **3 Khối tác nhân (Actor Zones)** độc lập, đảm bảo nguyên tắc phân chia trách nhiệm (Separation of Duties) và ngăn chặn xung đột lợi ích:

```
┌────────────────────────────────────────────────────────────────────────┐
│               KHỐI 1: PLATFORM GOVERNANCE (Đơn vị chủ quản Sàn)        │
│                                                                        │
│   🛠️ PLATFORM_ADMIN                  👔 PLATFORM_OPERATOR              │
│   (Quản trị Kỹ thuật & Hệ thống)     (Quản trị Nghiệp vụ & Trọng tài)  │
│   • Cấu hình hệ thống, checklist     • Thẩm định & Cấp phép Providers  │
│   • Phân quyền, bảo mật              • Hỗ trợ & Khớp nối Khách hàng    │
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
| **1. Platform Governance** | `PLATFORM_ADMIN` | **Quản trị viên Hệ thống**: Quản trị tài khoản, cấu hình tham số bảo mật, duy trì bộ Checklist tiêu chuẩn ngành, quản trị hạ tầng server/storage, kiểm tra system audit log. Không trực tiếp can thiệp vào nghiệp vụ thương mại hay phân xử tranh chấp. |
| | `PLATFORM_OPERATOR` | **Chuyên viên Vận hành Sàn & Xử lý khiếu nại nội bộ**: Tiếp nhận và thẩm định năng lực Provider (giấy phép, bảo hiểm, định danh drone); hỗ trợ Client kết nối thầu; giám sát SLA; điều phối chỉ thị giao dịch có điều kiện tới đối tác thanh toán; **xử lý tranh chấp nội bộ theo quy chế đã công bố**. |
| **2. Customer Organization** | `CLIENT` | **Khách hàng Doanh nghiệp / Chủ sở hữu hạ tầng**: Tự đăng ký pháp nhân; quản lý danh mục tài sản hạ tầng; tạo yêu cầu kiểm tra; chọn Provider; ký Hợp đồng dịch vụ điện tử; **thanh toán/đặt cọc hợp đồng qua đối tác thanh toán được cấp phép theo chính sách mục tiêu**; nghiệm thu báo cáo kỹ thuật; kích hoạt Mở Tranh chấp nếu có sai sót; tạo Ticket bảo trì. |
| **3. Service Provider** | `PROVIDER_MANAGER` | **Quản lý Đơn vị Dịch vụ Kiểm định / Bảo trì**: Khai báo hồ sơ năng lực công ty; tiếp nhận yêu cầu; lập Báo giá dịch vụ (Quotation); ký Hợp đồng dịch vụ (Service Order); xin phép bay Cục Tác chiến; phân công Inspector/Engineer; kiểm duyệt QA nội bộ và ký phát hành báo cáo. |
| | `INSPECTOR` | **Phi công Drone / Chuyên viên Kiểm định thuộc Provider**: Sử dụng công cụ Platform cung cấp để bay khảo sát theo Shot list, nạp bằng chứng lên MinIO (GPS, timestamp, SHA-256), và xác minh ứng viên lỗi từ AI YOLO do Platform cung cấp. Không tự triển khai mô hình AI riêng cho quy trình nền tảng. |
| | `MAINTENANCE_ENGINEER` | **Kỹ sư Bảo trì / Sửa chữa**: Khảo sát hiện trường lỗi; lập dự toán vật tư & nhân công; thực hiện thi công sửa chữa; nạp ảnh đối chứng Trước/Sau (Before/After Evidence) phục vụ nghiệm thu hoàn công và giải ngân bảo hành. |

---

## III. Mô hình Dòng tiền Ký quỹ (Escrow Cash Flow) & Hợp đồng Điện tử

### 1. Kiến trúc Hợp đồng 3 Bên (Tripartite Agreement)
* **Quy chế hoạt động Sàn (Platform Terms of Service)**: Ràng buộc cả Client và Provider khi tham gia nền tảng. Trao quyền cho `PLATFORM_OPERATOR` điều phối chỉ thị giao dịch theo hợp đồng và xử lý nội bộ khiếu nại theo quy chế đã công bố. Quyết định nội bộ này không thay thế Toà án hoặc trọng tài thương mại hợp pháp.
* **Đơn dịch vụ điện tử (Inspection Service Order / Maintenance Work Order)**: Được sinh ra cho từng thương vụ kiểm định/bảo trì, có giá trị pháp lý theo *Luật Giao dịch điện tử 2023*. Bao gồm: Phạm vi công việc (SOW), Danh mục góc chụp bắt buộc (Shot list), Độ phân giải ảnh yêu cầu (GSD), Tiến độ cam kết (SLA), Dự toán chi phí dịch vụ Provider, chính sách chi phí vận hành nền tảng do Platform tự chịu và Trách nhiệm an toàn bay.

### 2. Mô hình Bảo vệ Giao dịch Có Điều kiện Qua Đối tác Thanh toán Được Cấp phép (Cùng ký hiệu trạng thái `HELD_IN_ESCROW`, `FROZEN_DISPUTED`, `DISBURSED`, `REFUNDED`)
Nhằm giải quyết rủi ro *"Client sợ mất tiền khi Provider làm ẩu"* và *"Provider sợ bị bùng tiền sau khi đã bay"* cho bản mục tiêu:
1. **Đặt cọc 100% trước khi bay qua đối tác được cấp phép**: Client nộp 100% giá trị hợp đồng đã duyệt qua đối tác ngân hàng/thanh toán được cấp phép (`HELD_IN_ESCROW`). Chỉ sau khi đối tác xác nhận tiền đã được giữ theo điều kiện hợp đồng, Provider mới nhận lệnh khởi công. Đây là chính sách mục tiêu, chưa được triển khai hoặc xác minh pháp lý.
2. **Công thức hoa hồng chung do Platform ấn định**:
   - Platform công bố **một tỷ lệ duy nhất `r` cho mọi Provider**, áp dụng đồng nhất và không thương lượng riêng.
   - Gọi `B` là cơ sở tính hoa hồng: giá dịch vụ Provider trước VAT, sau chiết khấu do Provider tài trợ, trừ phần giá đã hoàn/giảm hợp lệ; không bao gồm VAT của Provider, VAT của hoa hồng, tiền giữ bảo hành tính hai lần, hoặc các khoản thu hộ riêng.
   - Hoa hồng mục tiêu `C = r × B`; hóa đơn/chứng từ hoa hồng của Platform thể hiện riêng `C` và thuế áp dụng.
   - Client thanh toán đúng số tiền dịch vụ phải trả; khoản hoa hồng không cộng thêm vào hóa đơn khách hàng. Hóa đơn dịch vụ của Provider và hóa đơn hoa hồng của Platform là hai chứng từ riêng.
   - Tỷ lệ `r` chưa được chọn trong tài liệu; cấm dùng bất kỳ tỷ lệ nào được đề cập trong ví dụ minh họa làm chính sách chính thức.
3. **Quyết toán & Tự động nghiệm thu hợp đồng (Auto-Settlement)**:
   - Khi Client bấm "Nghiệm thu (Accept)" HOẶC quá **5 ngày làm việc** kể từ ngày Provider giao báo cáo mà Client không phản hồi và không mở khiếu nại hợp lệ:
     - Đối tác thanh toán phân phối phần dịch vụ đủ điều kiện theo chính sách hoa hồng đã khóa tại hợp đồng: Provider nhận phần dịch vụ ròng sau hoa hồng; Platform nhận phần hoa hồng tương ứng theo hóa đơn riêng.
4. **Tạm giữ khi có Tranh chấp (`FROZEN_DISPUTED`)**: Đối tác tạm giữ phần tiền liên quan theo điều kiện hợp đồng và phạm vi sản phẩm được cho phép ngay khi một bên mở khiếu nại hợp lệ; không ai được rút phần bị giữ cho đến khi có quyết định xử lý nội bộ của `PLATFORM_OPERATOR` hoặc cơ chế pháp lý có thẩm quyền.
5. **Tiền bảo lãnh hoàn công (Retention Money `h = 10%`)**: Áp dụng riêng cho dịch vụ thi công sửa chữa bảo trì (MF5): giữ `H = h × B` khỏi lần giải ngân đầu tiên; chi trả phần còn lại khi hết bảo hành nếu không còn khiếu nại; không phát sinh hoa hồng mới khi giải ngân phần giữ lại.

### 3. Hạ tầng Dữ liệu, Mô hình AI YOLO và Trợ lý LLM do Nền tảng (Platform) Cung cấp Tập trung
* **Nguyên tắc then chốt cho bản mục tiêu**: Hệ thống lưu trữ MinIO, đường ống xử lý dữ liệu, mô hình **AI YOLO** và **trợ lý AI LLM** là **Năng lực dùng chung do Platform cung cấp qua giao diện chính thức**. Platform chịu trách nhiệm vận hành/ký hợp đồng hạ tầng và trang trải chi phí từ nguồn thu của mình.
* **Phân định vai trò Người dùng (Consumers)**:
  - **Provider (Provider Manager, Inspector, Maintenance Engineer)**: Chỉ sử dụng công cụ AI do Platform cấp sẵn trên Web/Mobile. Provider không tự host model riêng cho quy trình nền tảng; không được phép tính thêm phí xử lý AI/data vào báo giá gửi Client.
  - **Client**: Tra cứu ảnh, xem hộp bao khuyết tật do AI đề xuất, và tải báo cáo đã phát hành.
* **Chính sách chi phí**: Chi phí GPU chạy suy luận YOLO, token API LLM và lưu trữ MinIO thuộc trách nhiệm kinh tế nội bộ của Platform. Tài liệu không khẳng định nhà cung cấp hạ tầng cụ thể nào, cũng không hứa miễn phí vĩnh viễn; chính sách thương mại chính thức phải được công bố và khóa phiên bản trước khi áp dụng cho hợp đồng.

---

## IV. Chi tiết 5 Main Flows (MF1 → MF5)

---

### MF1 — Onboarding Pháp lý Đối tác, Thẩm định & Quản trị Hồ sơ Tài sản

**Mục tiêu**: Thiết lập tư cách pháp nhân trên nền tảng cho Client và Provider, thẩm định điều kiện an toàn bay theo *Luật Phòng không nhân dân 2024*, và số hóa hồ sơ tài sản hạ tầng cần kiểm tra.

**Tác nhân chính**: `Platform Admin`, `Platform Operator`, `Client`, `Provider Manager`, `System`.

#### 1. Quy trình chi tiết (Main Sequence)

| Bước | Vai trò / Lane | Hoạt động chi tiết | Sản phẩm đầu ra |
| :--- | :--- | :--- | :--- |
| **MF1-01** | Client | Đại diện doanh nghiệp tự đăng ký tổ chức khách hàng, cung cấp mã số thuế, thông tin người đại diện và kích hoạt tài khoản quản trị Client. | Tổ chức Client & Tài khoản kích hoạt |
| **MF1-02** | Provider Manager | Đăng ký hồ sơ năng lực của công ty dịch vụ drone: Giấy phép kinh doanh, Danh sách thiết bị drone kèm số đăng ký định danh theo khung drone hiện hành, Danh sách phi công kèm giấy tờ đào tạo/chứng chỉ hoặc giấy phép được công nhận, và hồ sơ bảo hiểm trách nhiệm theo chính sách mục tiêu của Platform. Đăng ký nội bộ không thay thế giấy phép nhà nước. | Hồ sơ Provider chờ thẩm định (`PENDING`) |
| **MF1-03** | Platform Operator | Thẩm định hồ sơ năng lực pháp lý của Provider: Đối chiếu tính hợp lệ của giấy phép, chứng chỉ phi công và bảo hiểm. Nếu đạt, phê duyệt cấp phép hoạt động (`VERIFIED`). Nếu thiếu, yêu cầu bổ sung hoặc từ chối (`REJECTED`). | Quyết định cấp phép Provider |
| **MF1-04** | Client | Khai báo hồ sơ tài sản hạ tầng: Mã tài sản, tên công trình, loại hạ tầng, tọa độ địa lý (kinh độ/vĩ độ), ranh giới tiếp cận, tài liệu hoàn công/thiết kế và thông số mặc định cho kiểm tra (mức ưu tiên, người liên hệ hiện trường). | Hồ sơ tài sản (`ACTIVE`) |
| **MF1-05** | System | Đối chiếu tọa độ tài sản với dữ liệu tham khảo công khai về cấm/hạn chế bay (`cambay.mod.gov.vn`, Quyết định 18/2020/QĐ-TTg) khi có thể truy cập. Cảnh báo, không tự cấp phép bay; phép bay từng chuyến vẫn cần cơ chế pháp lý có thẩm quyền. | Báo cáo tham khảo an toàn không phận của tài sản |
| **MF1-06** | Client | Thiết lập chu kỳ kiểm tra định kỳ (PERIODIC cadence: 1 tháng, 3 tháng, 6 tháng, 1 năm). Khi đến hạn, hệ thống tự động kế thừa thông số tài sản và phát sinh Yêu cầu kiểm định sẵn sàng chuyển tiếp sang MF2. | Lịch định kỳ hoạt động & Yêu cầu sẵn sàng |

#### 2. Xử lý Luồng Ngoại lệ (5 Câu hỏi Bắt buộc theo `error-prevention.md`)

* **Q1: Dữ liệu đầu vào thiếu hoặc sai?**
  * *Hồ sơ Provider thiếu chứng chỉ phi công hoặc bảo hiểm*: `PLATFORM_OPERATOR` từ chối duyệt, hệ thống chuyển trạng thái `ADDITIONAL_INFO_REQUIRED` và thông báo Provider tải lại tài liệu hợp lệ; Provider chưa thể tham gia chào giá ở MF2.
  * *Tọa độ tài sản không hợp lệ hoặc có dấu hiệu thuộc vùng cấm/hạn chế bay*: Hệ thống cảnh báo và gắn cờ `RESTRICTED_AIRSPACE`, yêu cầu xác minh phép bay phù hợp theo quy định hiện hành trước khi phát thầu; không tự suy ra miễn trừ chỉ vì trọng lượng drone nhỏ.
* **Q2: Người dùng không có quyền hoặc truy cập sai Organization?**
  * Client Org A tuyệt đối không xem được danh mục tài sản hoặc tài liệu mật của Client Org B. Provider chưa được duyệt (`PENDING/SUSPENDED`) bị chặn toàn bộ các API xem danh sách tài sản hay nhận yêu cầu.
* **Q3: Người dùng thao tác đồng thời hoặc gửi lại yêu cầu?**
  * Mã số thuế doanh nghiệp (Client/Provider) và Mã tài sản (Asset Code) trong cùng một Organization có ràng buộc duy nhất (Unique Constraint). Gửi lại form đăng ký lập tức bị chặn với lỗi `DUPLICATE_ENTITY`.
* **Q4: Dịch vụ ngoài, mạng hoặc lưu trữ tạm thời lỗi?**
  * Cổng tra cứu không phận `cambay.mod.gov.vn` bị gián đoạn: Hệ thống lưu trạng thái `AIRSPACE_CHECK_PENDING`, cho phép lưu hồ sơ tài sản nhưng đánh dấu cần thẩm định không phận thủ công trước khi bay.
* **Q5: Người dùng từ chối, yêu cầu sửa hoặc hủy giữa luồng?**
  * Client có thể sửa thông tin tài sản bất kỳ lúc nào khi chưa có đơn hàng đang chạy. Provider bị Operator từ chối cấp phép có quyền cập nhật lại tài liệu và gửi yêu cầu thẩm định lại (tối đa 3 lần).

---

### MF2 — Lập Yêu cầu, Khớp nối Provider, Hợp đồng Điện tử & Ký quỹ Escrow

**Mục tiêu**: Kết nối nhu cầu kiểm định của Client với Provider đủ điều kiện, ký kết Hợp đồng dịch vụ điện tử theo *Luật Giao dịch điện tử 2023*, thu 100% tiền ký quỹ vào Escrow Pool và phân công phi công bay hợp pháp.

**Tác nhân chính**: `Client`, `Platform Operator`, `Provider Manager`, `Inspector`, `System`.

#### 1. Quy trình chi tiết (Main Sequence)

| Bước | Vai trò / Lane | Hoạt động chi tiết | Sản phẩm đầu ra |
| :--- | :--- | :--- | :--- |
| **MF2-01** | Client | Khởi tạo Yêu cầu kiểm tra (từ lịch định kỳ MF1 hoặc đột xuất). Xác định phương thức chọn thầu: (A) **Chỉ định trực tiếp** Provider quen thuộc; hoặc (B) **Chào thầu công khai (Open RFQ)** cho các Provider đủ chuẩn trong bán kính khu vực. Đính kèm Checklist áp dụng, Shot list và yêu cầu độ phân giải GSD. | Yêu cầu kiểm tra (RFQ) |
| **MF2-02** | Platform Operator | *(Tùy chọn hỗ trợ)*: Kiểm tra các yêu cầu thầu mở, hỗ trợ điều phối gửi thông báo cho các Provider có phạm vi bay phù hợp với địa điểm của tài sản. | Danh sách Provider tiếp cận yêu cầu |
| **MF2-03** | Provider Manager | Xem xét phạm vi yêu cầu, khảo sát từ xa và lập Báo giá (Quotation) cho phần dịch vụ Provider trực tiếp thực hiện: (1) Phí bay hiện trường; (2) Nhân công kỹ thuật và chi phí tác nghiệp hợp lệ; (3) Chi phí đi lại/triển khai nếu có; (4) Thuế/thuế VAT áp dụng đúng phương pháp của Provider. **Provider không báo giá và không thu riêng phí xử lý dữ liệu/AI/LLM, lưu trữ hoặc phí nền tảng; các chi phí này thuộc trách nhiệm kinh tế nội bộ của Platform.** | Báo giá dịch vụ Provider theo phiên bản (v1, v2) |
| **MF2-04** | Client | Xem xét báo giá. Có thể yêu cầu điều chỉnh (Revision Request) hoặc chọn Báo giá tốt nhất để chấp thuận. Tổng phải thanh toán hiển thị riêng phí dịch vụ Provider, chiết khấu, thuế và mọi chi phí do Client trả; hoa hồng do Provider trả không cộng thêm vào hóa đơn khách hàng. | Báo giá được chọn duyệt |
| **MF2-05** | System & Client | Hệ thống lập **Đơn dịch vụ kiểm định điện tử (Inspection Service Order)** đính kèm điều khoản, SLA, phạm vi SOW và chính sách hoa hồng `r` đã khóa phiên bản. Client ký hợp đồng điện tử và nộp tiền qua đối tác ngân hàng/thanh toán được cấp phép (`HELD_IN_ESCROW`). | Tiền được giữ có điều kiện & Hợp đồng có hiệu lực (`LEGALLY_BINDING`) |
| **MF2-06** | Provider Manager | Sau khi đối tác xác nhận tiền được giữ theo điều kiện hợp đồng, thực hiện thủ tục bay: nộp tài liệu phép bay có thẩm quyền (khi thuộc diện phải xin phép), chọn phi công `Inspector` có giấy tờ phù hợp, không xung đột lợi ích, và phát Gói nhiệm vụ (Assignment Package). | Lệnh phân công Inspector |
| **MF2-07** | Inspector | Xem xét gói nhiệm vụ (tọa độ, checklist, shot list, thời hạn bay). Chấp nhận nhiệm vụ. Hệ thống chuyển trạng thái đợt kiểm tra sang `READY_FOR_INSPECTION`. | Nhiệm vụ sẵn sàng thực hiện |

#### 2. Chính sách Hủy Hợp đồng & Thời tiết xấu (Chính sách mục tiêu, cần hợp đồng và tư vấn pháp lý xác nhận)
* **Hủy trước 24 giờ**: Mục tiêu Client hủy trước giờ bay 24h được hoàn lại phần tiền chưa phát sinh dịch vụ theo chính sách đã khóa tại hợp đồng; mọi khoản phí ngân hàng/đối tác thực tế vẫn xử lý theo chứng từ thanh toán.
* **Hủy trong vòng 24 giờ (hoặc phi công đã đến hiện trường)**: Mục tiêu áp dụng phí di chuyển khô/tới hiện trường `dry_run_fee` cho Client trong trường hợp hủy chủ quan; hoàn phần còn lại cho Client. Văn bản hiện chưa chọn số phần trăm cố định.
* **Bất khả kháng thời tiết**: Mục tiêu hoãn lịch bay khi điều kiện an toàn không đảm bảo, có bằng chứng thời tiết; hai bên thống nhất lịch mới và xem xét miễn trừ SLA theo quy chế; không mặc nhiên áp một ngưỡng gió cố định cho mọi khu vực bay.

#### 3. Xử lý Luồng Ngoại lệ (5 Câu hỏi Bắt buộc)

* **Q1: Dữ liệu đầu vào thiếu hoặc sai?**
  * SOW thiếu shot list hoặc checklist: Provider Manager không thể gửi báo giá hợp lệ, hệ thống yêu cầu Client hoàn thiện thông số trước khi mở cổng báo giá.
* **Q2: Người dùng không có quyền hoặc truy cập sai Organization?**
  * Provider A không thể xem giá thầu của Provider B trong cùng một gói RFQ. Inspector không thể nhận assignment nếu không thuộc danh sách nhân sự của Provider trúng thầu.
* **Q3: Người dùng thao tác đồng thời hoặc gửi lại yêu cầu?**
  * Client bấm thanh toán ký quỹ 2 lần: Cơ chế Idempotency Key khóa cổng thanh toán, ngăn chặn tạo 2 giao dịch nạp tiền trùng lặp cho một Service Order.
* **Q4: Dịch vụ ngoài, mạng hoặc lưu trữ tạm thời lỗi?**
  * Cổng ngân hàng/trung gian thanh toán timeout: Đơn hàng giữ trạng thái `PAYMENT_PENDING`; hệ thống chỉ chuyển sang đã giữ tiền khi nhận xác nhận chính thức từ đối tác thanh toán, không tự suy ra đã thanh toán từ timeout/webhook chưa xác thực.
* **Q5: Người dùng từ chối, yêu cầu sửa hoặc hủy giữa luồng?**
  * Inspector từ chối nhận phân công (phải kèm lý do): Lệnh phân công bị hủy (`REJECTED`), công việc tự động trả về cho Provider Manager để phân công phi công khác trong vòng 12h.

---

### MF3 — Khảo sát Drone Hiện trường, Xử lý AI & Báo cáo Kỹ thuật (QA)

**Mục tiêu**: Thu thập hình ảnh/video hiện trường bằng drone theo chuẩn chứng cứ số (*Luật Giao dịch điện tử 2023*), xử lý AI phát hiện khiếm khuyết, kiểm duyệt kỹ thuật chéo nội bộ Provider và phát hành báo cáo.

**Tác nhân chính**: `Inspector` (Người bay), `Inspector` (Người review chéo), `Provider Manager`, `MinIO do Platform cung cấp`, `AI YOLO Service do Platform cung cấp`.

#### 1. Quy trình chi tiết (Main Sequence)

| Bước | Vai trò / Lane | Hoạt động chi tiết | Sản phẩm đầu ra |
| :--- | :--- | :--- | :--- |
| **MF3-01** | Inspector | Mở ứng dụng Web/Mobile, kích hoạt phiên bay kiểm tra tại hiện trường (`IN_PROGRESS`). Thực hiện bay khảo sát theo đúng Shot list, checklist và ranh giới cho phép. | Phiên bay hiện trường kích hoạt |
| **MF3-02** | Inspector | Tải toàn bộ hình ảnh/video độ phân giải cao thu thập từ thẻ nhớ drone lên hệ thống MinIO qua giao thức phân đoạn (Chunked Upload). | Bằng chứng kiểm định thô |
| **MF3-03** | System (MinIO & Validator do Platform cung cấp) | Tự động kiểm tra định dạng, dung lượng; trích xuất siêu dữ liệu EXIF (Tọa độ GPS, độ cao, góc camera, timestamp); tính toán mã băm toàn vẹn **SHA-256** cho từng file ảnh. Từ chối file trùng lặp. Dữ liệu hỗ trợ truy xuất và đối chiếu; việc công nhận chứng cứ thuộc cơ chế pháp lý có thẩm quyền. | Bằng chứng số được bảo vệ toàn vẹn ở mức kỹ thuật |
| **MF3-04** | System (YOLO AI Service do Platform cung cấp) | Khi cấu hình AI bật: Dịch vụ YOLO do Platform cung cấp phân tích các ảnh hợp lệ, nhận diện vết nứt, gỉ sét, bong tróc, sụt lún và tạo ra các **Ứng viên lỗi (Defect Candidates)** kèm nhãn, độ tin cậy (confidence score) và tọa độ hộp bao (bounding box). Provider và Client chỉ dùng kết quả này trên giao diện Platform; AI không tự động biến thành lỗi chính thức. | Danh sách ứng viên lỗi đề xuất |
| **MF3-05** | Inspector (Người bay) | Kiểm tra trực quan từng ảnh và từng ứng viên AI: Chọn **Xác nhận (Confirm)**, **Hiệu chỉnh (Modify)**, hoặc **Bác bỏ (Reject)**. Nếu AI bỏ sót, Inspector **tự thêm lỗi thủ công (Manual Finding)**. Hoàn tất câu trả lời checklist kỹ thuật. | Hồ sơ khiếm khuyết đã xác minh |
| **MF3-06** | System | Tự động biên soạn Bản thảo Báo cáo Kỹ thuật (Draft Report v1.0) từ checklist, hình ảnh và danh mục lỗi đã xác minh. Loại bỏ hoàn toàn các ứng viên AI bị bác bỏ khỏi báo cáo chính thức. | Bản thảo báo cáo kỹ thuật |
| **MF3-07** | Inspector (Người review chéo) | **Thẩm định chéo (Internal Peer Review)**: Một Inspector độc lập khác trong Provider thẩm định tính chính xác của báo cáo. *Quy tắc bất di bất dịch: Người bay không được tự duyệt báo cáo của chính mình (chống gian lận/làm ẩu nội bộ)*. | Biên bản thẩm định chéo |
| **MF3-08** | Inspector (Người bay) | Nếu reviewer yêu cầu chỉnh sửa: cập nhật lại báo cáo (v1.1, v1.2) và nộp lại. Nếu đạt, reviewer ký xác nhận đạt chuẩn kỹ thuật (`TECHNICALLY_APPROVED`). | Báo cáo đạt chuẩn kỹ thuật |
| **MF3-09** | Provider Manager | Kiểm tra tính đầy đủ của hồ sơ bàn giao so với Service Order đã ký và chính thức **Ký phát hành Báo cáo (Release Final Report)** cho Client. Kích hoạt đồng hồ đếm ngược nghiệm thu 5 ngày. | Báo cáo chính thức gửi Client |

#### 2. Xử lý Luồng Ngoại lệ (5 Câu hỏi Bắt buộc)

* **Q1: Dữ liệu đầu vào thiếu hoặc sai?**
  * Ảnh chụp bị mờ, hỏng file hoặc thiếu thông tin GPS: Hệ thống gắn cờ cảnh báo `METADATA_INCOMPLETE`. Nếu ảnh không đủ chuẩn đọc vết nứt, Inspector bắt buộc phải bay bổ sung ngay khi còn ở hiện trường.
* **Q2: Người dùng không có quyền hoặc truy cập sai Organization?**
  * Tác giả báo cáo cố tình chọn chính mình làm Peer Reviewer: Hệ thống chặn đứng với mã lỗi `PEER_REVIEW_SELF_APPROVAL_PROHIBITED`.
* **Q3: Người dùng thao tác đồng thời hoặc gửi lại yêu cầu?**
  * Mạng chập chờn khiến Inspector tải lên 1 ảnh nhiều lần: Hệ thống đối chiếu mã băm SHA-256; nếu trùng lặp, bỏ qua file thứ hai mà không tạo thêm bản ghi rác.
* **Q4: Dịch vụ ngoài, mạng hoặc lưu trữ tạm thời lỗi?**
  * Dịch vụ AI YOLO bị quá tải hoặc offline: Hệ thống tự động ghi log lỗi, chuyển sang cơ chế **Manual Fallback** cho phép Inspector tự đánh dấu lỗi thủ công trên ảnh, đảm bảo tiến độ bàn giao báo cáo không bị đình trệ.
* **Q5: Người dùng từ chối, yêu cầu sửa hoặc hủy giữa luồng?**
  * Peer Reviewer từ chối thông qua báo cáo do phát hiện kết luận sai lệch: Báo cáo bị trả về trạng thái `REVISION_REQUIRED` kèm ghi chú lỗi kỹ thuật chi tiết; tác giả phải giải trình hoặc chỉnh sửa lại.

---

### MF4 — Nghiệm thu Báo cáo, Quyết toán Tự động & Trọng tài Phân xử Tranh chấp

**Mục tiêu**: Khách hàng đánh giá chất lượng bàn giao, thực hiện quyết toán tự động giải ngân Escrow theo *Nghị định 52/2024/NĐ-CP*, hoặc kích hoạt cơ chế Trọng tài phân xử tranh chấp của `PLATFORM_OPERATOR` theo *Luật Bảo vệ quyền lợi người tiêu dùng 2023*.

**Tác nhân chính**: `Client`, `Provider Manager`, `Platform Operator` (Trọng tài), `System`.

#### 1. Quy trình chi tiết (Main Sequence)

```
                            [ Client Nhận Báo Cáo ]
                                       │
                     Khảo sát / Đánh giá trong 5 ngày làm việc
                                       │
        ┌──────────────────────────────┼──────────────────────────────┐
        ▼                              ▼                              ▼
 [ Hướng 1: Nghiệm thu ]   [ Hướng 2: Yêu cầu Làm rõ ]     [ Hướng 3: MỞ TRANH CHẤP ]
        │                              │                              │
 Báo cáo trở thành                     │                      ĐÓNG BĂNG TIỀN ESCROW
  BẤT BIẾN (COMPLETED)          Provider giải trình                   │
        │                       & cập nhật báo cáo           Platform Operator thụ lý
        ▼                              │                     đối soát chứng cứ số
GIẢI NGÂN THEO HOA HỒNG ĐÃ KHÓA           ▼                              │
 Provider: B - C             Client xem xét lại              ┌─────────┴─────────┐
 Platform: C + thuế riêng                                   ▼                   ▼
                                                      Khiếu nại có căn cứ  Khiếu nại không căn cứ
                                                            │                   │
                                                    Bay lại/hoàn tiền/     Giải ngân phần đủ
                                                    xử lý theo quy chế     điều kiện cho Provider
```

| Bước | Vai trò / Lane | Hoạt động chi tiết | Sản phẩm đầu ra |
| :--- | :--- | :--- | :--- |
| **MF4-01** | Client | Xem xét báo cáo kiểm định hoàn chỉnh trên Web/Mobile. Bắt đầu tính thời hạn nghiệm thu **5 ngày làm việc**. | Hồ sơ nghiệm thu đang mở |
| **MF4-02a** | Client (Nhánh Nghiệm thu) | Client xác nhận báo cáo đạt yêu cầu chất lượng -> Chọn **"Nghiệm thu (Accept)"**. | Quyết định nghiệm thu |
| **MF4-02b** | System (Nhánh Auto-Settlement) | Quá thời hạn 5 ngày làm việc, nếu Client không xác nhận và không mở khiếu nại hợp lệ -> Hệ thống tự động kích hoạt **Nghiệm thu mặc định (Auto-Settlement)** nhằm bảo vệ nhà thầu Provider chống bùng tiền. | Quyết định nghiệm thu tự động |
| **MF4-03** | System và đối tác thanh toán | Báo cáo chuyển sang trạng thái bất biến (`COMPLETED`). **Giải ngân theo chính sách hoa hồng đã khóa tại hợp đồng**: Gọi `B` là cơ sở tính hoa hồng trước VAT, `r` là tỷ lệ hoa hồng chung do Platform công bố, `C = r × B`; Provider nhận phần dịch vụ đủ điều kiện sau khi trừ `C`, Platform ghi nhận `C` riêng kèm thuế theo phương pháp của Platform. Provider vẫn xuất hóa đơn dịch vụ đầy đủ cho Client, không thu hẹp doanh thu theo số tiền ròng. | Dòng tiền tất toán (`DISBURSED`) & hóa đơn riêng |
| **MF4-04** | Client (Nhánh Yêu cầu Làm rõ) | Nếu có nội dung kỹ thuật chưa rõ ràng, Client gửi yêu cầu giải trình (Clarification Request). Provider Manager có trách nhiệm giải trình hoặc phát hành bản báo cáo hiệu chỉnh (Client không được trực tiếp sửa nội dung chuyên môn). | Báo cáo hiệu chỉnh |
| **MF4-05** | Client / Provider (Nhánh Mở Tranh chấp) | Khi phát sinh mâu thuẫn nghiêm trọng không thể tự hòa giải: (1) Ảnh chụp mờ/sai góc so với Shot list cam kết; (2) Kết luận sai lệch bản chất hư hỏng; (3) Làm rơi drone gây thiệt hại tài sản; (4) Gian lận dữ liệu cũ: Một trong hai bên bấm **"Mở Tranh chấp (Open Dispute)"**. | Hồ sơ tranh chấp (`OPENED`) |
| **MF4-06** | System và đối tác thanh toán | **Tạm giữ phần tiền liên quan theo điều kiện hợp đồng (`FROZEN_DISPUTED`)**. Chỉ giữ phần được hợp đồng và sản phẩm thanh toán cho phép; phần không tranh chấp có thể quyết toán theo quy chế. Chuyển hồ sơ sang bộ phận xử lý khiếu nại nội bộ. | Phần tiền liên quan bị tạm giữ |
| **MF4-07** | Platform Operator | **Thụ lý & xử lý khiếu nại nội bộ theo quy chế đã công bố**: Yêu cầu hai bên nộp chứng cứ bổ sung trong thời hạn hợp lý. Operator đối soát: Hợp đồng SOW (MF2) ↔ Chứng cứ ảnh/video gốc MinIO kèm mã băm SHA-256 & tọa độ GPS (MF3) ↔ Khiếu nại của Client ↔ Giải trình của Provider; bảo đảm quyền khiếu nại, kháng nghị, khởi kiện hoặc trọng tài thương mại theo luật. | Biên bản xử lý nội bộ |
| **MF4-08** | Platform Operator | **Ra quyết định xử lý nội bộ của Sàn** theo 1 trong 3 biện pháp dưới đây; quyết định không thay thế Toà án hoặc trọng tài thương mại hợp pháp: | Quyết định nội bộ có hiệu lực điều phối giao dịch |

#### 2. Ba biện pháp xử lý nội bộ của `PLATFORM_OPERATOR`
1. **Biện pháp A — Provider vi phạm chất lượng có thể khắc phục (Ảnh mờ, thiếu góc chụp)**:
   - Operator yêu cầu **Provider bay chụp lại miễn phí (Free Reshoot)** trong thời hạn hợp đồng; đề xuất mục tiêu 48 giờ cần được khóa trong quy chế, không mặc định là nghĩa vụ pháp luật.
   - Phần tiền liên quan tiếp tục bị tạm giữ cho đến khi Client nhận và nghiệm thu báo cáo bay lại.
2. **Biện pháp B — Provider vi phạm nghiêm trọng / Gian lận / Gây thiệt hại**:
   - Operator đề xuất **chấm dứt hợp đồng theo quy chế**.
   - Đối tác hoàn lại phần tiền đủ điều kiện cho Client; mọi khoản phạt, bồi thường hoặc đình chỉ tài khoản (`SUSPENDED`) phải tuân thủ hợp đồng và pháp luật, không tự áp đặt ngoài quy chế.
3. **Biện pháp C — Client khiếu nại không có căn cứ**:
   - Operator bác khiếu nại theo quy chế.
   - Đối tác giải ngân phần dịch vụ đủ điều kiện cho Provider theo hợp đồng; khi hoàn/giảm giá, đảo hoa hồng tương ứng `r × Q` và điều chỉnh hóa đơn theo chứng từ thuế, không thu hoa hồng trên phần đã hoàn.

#### 3. Xử lý Luồng Ngoại lệ (5 Câu hỏi Bắt buộc)

* **Q1: Dữ liệu đầu vào thiếu hoặc sai?**
  * Đơn mở tranh chấp không có bằng chứng chứng minh: Operator yêu cầu bổ sung bằng chứng trong 24h. Quá 24h không nộp bằng chứng, tranh chấp bị tự động bác bỏ.
* **Q2: Người dùng không có quyền hoặc truy cập sai Organization?**
  * Thành viên không có thẩm quyền trong Client Org cố tình bấm mở tranh chấp: Hệ thống kiểm tra quyền, chỉ tài khoản đại diện pháp nhân / quản trị viên hợp đồng mới được kích hoạt tranh chấp.
* **Q3: Người dùng thao tác đồng thời hoặc gửi lại yêu cầu?**
  * Client vừa bấm "Accept" vừa bấm "Open Dispute" cùng thời điểm: Giao dịch cơ sở dữ liệu dùng Pessimistic Lock trên Service Order; trạng thái đầu tiên được commit thành công sẽ chặn đứng thao tác còn lại.
* **Q4: Dịch vụ ngoài, mạng hoặc lưu trữ tạm thời lỗi?**
  * Hệ thống thông báo SMS/Email phán quyết trọng tài bị lỗi: Trạng thái phán quyết vẫn được ghi nhận bất biến trong database kèm Audit Log; các bên nhận thông báo qua In-app Notification khi đăng nhập.
* **Q5: Người dùng từ chối, yêu cầu sửa hoặc hủy giữa luồng?**
  * Provider từ chối thực hiện lệnh "Free Reshoot" của Operator: Operator kích hoạt chuyển sang Kịch bản B (Hủy hợp đồng, hoàn tiền cho Client, phạt Provider).

---

### MF5 — Xử lý Khiếm khuyết, Đơn hàng Bảo trì & Tiền Bảo lãnh Hoàn công

**Mục tiêu**: Chuyển các khuyết tật kỹ thuật đã được nghiệm thu thành công việc sửa chữa thực tế, kiểm soát phát sinh chi phí, nghiệm thu ảnh đối chứng Before/After và quản lý Dòng tiền Bảo lãnh hoàn công (Retention Money 10%).

**Tác nhân chính**: `Client`, `Maintenance Provider Manager`, `Maintenance Engineer`, `Platform Operator`, `System`.

#### 1. Quy trình chi tiết (Main Sequence)

| Bước | Vai trò / Lane | Hoạt động chi tiết | Sản phẩm đầu ra |
| :--- | :--- | :--- | :--- |
| **MF5-01** | Client | Chọn một hoặc nhiều lỗi kỹ thuật đã được xác nhận (Verified Defects) từ Báo cáo kiểm định MF4 để tạo **Phiếu yêu cầu bảo trì (Maintenance Ticket)**. | Maintenance Ticket |
| **MF5-02** | Maintenance Provider Manager | Khảo sát hiện trường (trực tiếp hoặc qua mô hình 3D/ảnh zoom MF3); lập Phương án kỹ thuật, dự toán vật tư, nhân công và Báo giá bảo trì (Maintenance Quotation). Hợp đồng thi công bắt buộc có điều khoản: **Tiền giữ lại bảo lãnh bảo hành (Retention Money: 10%)**. | Báo giá bảo trì & Đơn dịch vụ |
| **MF5-03** | Client | Xem xét và phê duyệt Đơn dịch vụ bảo trì (Maintenance Work Order). Client thực hiện nộp 100% tiền thi công vào **Tài khoản Ký quỹ Escrow**. | Tiền bảo trì ký quỹ Escrow |
| **MF5-04** | Maintenance Engineer | Tiếp nhận phân công thi công. Đến hiện trường thực hiện sửa chữa (hàn nứt, thay cáp, xử lý ăn mòn). **Bắt buộc chụp và nạp ảnh đối chứng Trước và Sau thi công (Before/After Evidence)** lên MinIO kèm nhật ký vật tư. | Nhật ký thi công & Ảnh Before/After |
| **MF5-05** | Maintenance Engineer & Provider Manager | Nếu phát hiện hư hỏng ngầm vượt quá dự toán ban đầu: Kỹ sư dừng ngay phần việc phát sinh, lập **Yêu cầu thay đổi (Change Order)**. Client xem xét và ký quỹ bổ sung phần tiền phát sinh thì mới được phép thi công tiếp. | Change Order được duyệt |
| **MF5-06** | Client & Provider Manager | **Nghiệm thu Đợt 1 (Nghiệm thu hoàn công)**: Client đối soát ảnh Trước/Sau. Nếu đạt chuẩn, Client ký biên bản nghiệm thu: | Quyết toán Đợt 1 |
| **MF5-07** | System và đối tác thanh toán | Đối tác giải ngân phần dịch vụ hoàn công đủ điều kiện cho Đơn vị bảo trì theo chính sách hoa hồng đã khóa, đồng thời giữ `H = h × B` làm tiền bảo lãnh (`h = 10%` theo chính sách mục tiêu; thời hạn bảo hành và điều kiện giữ lại do hợp đồng quy định). Khuyết tật được chuyển trạng thái `RESOLVED`. | Giải ngân đợt 1 & tiền giữ bảo hành |
| **MF5-08** | Client & Platform Operator | **Nghiệm thu Đợt 2 (Hết hạn bảo hành)**: Nếu không còn khiếu nại hoặc tái hỏng trong thời hạn bảo hành, đối tác giải ngân nốt phần giữ lại cho Đơn vị bảo trì, không phát sinh hoa hồng mới. Đóng vĩnh viễn vòng đời khuyết tật (`CLOSED`). | Tất toán phần giữ lại & Đóng Ticket |

#### 2. Nhánh Xử lý Rework / Re-inspection / Tranh chấp Bảo hành
* **Yêu cầu làm lại (Rework)**: Nếu chất lượng chắp vá cẩu thả -> Client yêu cầu Đơn vị bảo trì thi công lại miễn phí trước khi nghiệm thu Đợt 1.
* **Yêu cầu kiểm tra lại bằng Drone (Re-inspection)**: Nếu việc sửa chữa ở vị trí nguy hiểm khó nhìn bằng mắt thường -> Client kích hoạt yêu cầu bay chụp lại, tạo ra một đơn kiểm định liên kết quay trở lại MF2.
* **Tranh chấp bảo hành**: Nếu trong thời hạn bảo hành mà mối hàn bị nứt lại nhưng Provider từ chối bảo hành -> Client bấm Mở Tranh chấp; `PLATFORM_OPERATOR` xử lý theo quy chế: có thể dùng phần giữ lại để khắc phục thiệt hại được chấp nhận hoặc hoàn lại cho Client theo hợp đồng; mọi quyết định giữ/tịch thu phải có căn cứ hợp đồng và pháp luật.

#### 3. Xử lý Luồng Ngoại lệ (5 Câu hỏi Bắt buộc)

* **Q1: Dữ liệu đầu vào thiếu hoặc sai?**
  * Kỹ sư nộp báo cáo hoàn công nhưng thiếu ảnh đối chứng Before/After: Hệ thống chặn nút Submit, bắt buộc phải có đủ cặp ảnh đối chứng mới được trình nghiệm thu.
* **Q2: Người dùng không có quyền hoặc truy cập sai Organization?**
  * Đơn vị bảo trì A cố tình truy cập hồ sơ khiếm khuyết của Client khi chưa được Client mời chào giá: Hệ thống chặn quyền truy cập ở tầng API.
* **Q3: Người dùng thao tác đồng thời hoặc gửi lại yêu cầu?**
  * Kỹ sư gửi 2 yêu cầu Change Order liên tiếp cho cùng một lỗi phát sinh: Hệ thống chỉ cho phép duy nhất 1 Change Order ở trạng thái `PENDING_APPROVAL` tại một thời điểm.
* **Q4: Dịch vụ ngoài, mạng hoặc lưu trữ tạm thời lỗi?**
  * Mất sóng di động khi chụp ảnh tại hiện trường công trình ngầm: Mobile app lưu ảnh offline vào bộ nhớ mã hóa an toàn của thiết bị (`flutter_secure_storage`), tự động đồng bộ lên MinIO khi có mạng trở lại.
* **Q5: Người dùng từ chối, yêu cầu sửa hoặc hủy giữa luồng?**
  * Client từ chối phê duyệt phát sinh chi phí Change Order: Đơn vị bảo trì chỉ thi công đúng phạm vi hợp đồng ban đầu; phần phát sinh không được thi công và không tính tiền.

---

## V. Ma trận Phân quyền & Trách nhiệm (RACI Matrix)

| Quy trình / Nghiệp vụ cốt lõi | `PLATFORM_ADMIN` | `PLATFORM_OPERATOR` | `CLIENT` | `PROVIDER_MANAGER` | `INSPECTOR` | `MAINTENANCE_ENGINEER` |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **MF1: Thẩm định Provider & Khai báo Drone** | I | **A / R** | I | **R** | C | - |
| **MF1: Khai báo Tài sản & Cảnh báo Cấm bay** | I | C | **A / R** | - | - | - |
| **MF2: Đấu thầu RFQ & Báo giá Kiểm định** | - | C | **A** | **R** | - | - |
| **MF2: Ký Hợp đồng & Ký quỹ Escrow 100%** | I | C | **A / R** | **R** | - | - |
| **MF2: Phân công Phi công & Giấy phép bay** | I | C | I | **A / R** | **R** | - |
| **MF3: Khảo sát Drone & Nạp ảnh MinIO** | - | - | I | I | **A / R** | - |
| **MF3: Xác minh AI YOLO & Lập báo cáo** | - | - | - | I | **A / R** | - |
| **MF3: Thẩm định chéo (Internal Peer Review)**| - | - | - | I | **A / R** | - |
| **MF3: Ký phát hành Báo cáo Kỹ thuật** | - | - | I | **A / R** | I | - |
| **MF4: Nghiệm thu Báo cáo & Quyết toán Escrow**| I | C | **A / R** | I | - | - |
| **MF4: Thụ lý & Trọng tài Phân xử Tranh chấp** | I | **A / R** | C | C | C | - |
| **MF5: Tạo Ticket & Báo giá Bảo trì** | - | - | **A** | **R** | - | C |
| **MF5: Ký quỹ Bảo trì & Thi công Before/After** | - | - | **A** | I | - | **A / R** |
| **MF5: Nghiệm thu Hoàn công & Tất toán Bảo hành**| I | **R** | **A** | I | - | I |

*Ghi chú*:
* **R (Responsible)**: Người trực tiếp thực hiện công việc.
* **A (Accountable)**: Người chịu trách nhiệm phê duyệt cuối cùng và sở hữu kết quả.
* **C (Consulted)**: Người được tham vấn ý kiến, cung cấp dữ liệu đối soát.
* **I (Informed)**: Người được nhận thông báo kết quả.
