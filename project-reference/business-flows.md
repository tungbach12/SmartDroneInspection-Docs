---
title: "SmartDroneInspection Multi-Provider Business Flows"
document_type: business-flow-reference
purpose: "Đặc tả chi tiết Luồng Bổ trợ (SF), 5 Luồng nghiệp vụ cốt lõi (MF1–MF5), Các nhánh Ngoại lệ (Exceptions) và Vòng lặp Phi tuyến tính (Non-linear Loops) chuyên sâu Drone cho Nền tảng Kiểm định & Bảo trì Hạ tầng"
version: "3.2"
updated: 2026-10-05
---

# SmartDroneInspection Multi-Provider Business Flows (v3.2)

> Tài liệu này là đặc tả chuẩn mực về Luồng Bổ trợ (Supporting Flow - SF) và **5 Luồng nghiệp vụ giao dịch cốt lõi (MF1–MF5)** của nền tảng SmartDroneInspection. Toàn bộ thiết kế được xây dựng dựa trên mô hình **Nền tảng số trung gian (Intermediary Platform)**, kiến trúc chuyên sâu về **Nhiệm vụ Khảo sát Drone (Drone Mission Planning & Telemetry)**, cơ chế Hợp đồng điện tử, **Điều phối dòng tiền thanh toán có điều kiện (Conditional Payment Lifecycle Orchestration)** qua đối tác thanh toán được cấp phép, chính sách **Cấu hình Động của `PLATFORM_OPERATOR`**, bổ sung **Các vòng lặp phản hồi phi tuyến tính (Feedback Loops)** và **Xử lý sự cố hiện trường (Incident & Exception Handling)**, tuân thủ nghiêm ngặt Hướng dẫn tránh lỗi Capstone (`error-prevention.md`) và căn cứ theo hệ thống pháp luật Việt Nam hiện hành.

---

## I. Căn cứ Pháp lý Việt Nam Áp dụng

> **Phạm vi pháp lý:** Đây là bản thiết kế mục tiêu phục vụ đồ án kỹ thuật. Các văn bản dưới đây là khung tham chiếu pháp luật áp dụng cho các hoạt động khảo sát drone, hợp đồng số, thanh toán trung gian và bảo trì công trình tại Việt Nam:

Lưu ý cập nhật pháp lý 2026: Nghị định 288/2025/NĐ-CP đang có hiệu lực. Có thông tin cho biết Chính phủ đang lấy ý kiến dự thảo sửa đổi Nghị định này — **thông tin này chưa được kiểm chứng tại thời điểm cập nhật tài liệu và cần được xác nhận lại với cố vấn pháp lý trước khi nộp**. Vì vậy workflow chỉ mô hình hóa bước kiểm tra điều kiện/hồ sơ và không hard-code cơ quan hoặc thủ tục cấp phép nếu chưa được xác nhận theo quy định áp dụng cho từng chuyến bay.

1. **Luật Phòng không nhân dân 2024 (Luật số 49/2024/QH15, hiệu lực từ 01/07/2025) & Nghị định số 288/2025/NĐ-CP (hiệu lực từ 05/11/2025 về Quản lý tàu bay không người lái và phương tiện bay siêu nhẹ)**:
   - Khung pháp lý bắt buộc để kiểm tra: thông tin đăng ký/định danh phương tiện bay; điều kiện của người điều khiển; và giấy phép/chấp thuận bay khi thuộc trường hợp phải có theo quy định hiện hành. Tên cơ quan, loại giấy phép và quy trình cụ thể không được hard-code trong workflow nếu chưa được xác nhận theo quy định áp dụng cho từng chuyến bay.
   - Hệ thống quản lý hồ sơ giấy phép và kiểm soát điều kiện bay trước khi phát lệnh cất cánh; **hệ thống không tự ý cấp phép bay thay cơ quan nhà nước**.
2. **Quyết định số 18/2020/QĐ-TTg & Cổng thông tin Vùng cấm bay quốc gia (`cambay.mod.gov.vn`)**:
   - Tra cứu tham khảo không phận số về khu vực cấm bay, hạn chế bay. Đóng vai trò lớp cảnh báo sớm (Pre-flight Early Warning) trong giai đoạn lập kế hoạch.
3. **Quy định về Thanh toán không dùng tiền mặt và Dịch vụ Trung gian Thanh toán**:
   - Tuân thủ **Nghị định số 52/2024/NĐ-CP** và Điều 330 Bộ luật Dân sự 2015. Nền tảng đóng vai trò đơn vị điều phối trạng thái thanh toán (Payment Orchestration) tích hợp với Ngân hàng thương mại / Cổng trung gian thanh toán được cấp phép (qua tài khoản chuyên dụng/đảm bảo thanh toán). Nền tảng không trực tiếp nắm giữ tiền gửi hoặc hoạt động như tổ chức tín dụng.
4. **Luật Giao dịch điện tử 2023 (Luật số 20/2023/QH15, hiệu lực từ 01/07/2024)**:
   - Căn cứ pháp lý cho Hợp đồng Dịch vụ Điện tử (Inspection Service Order / Maintenance Work Order). Lưu trữ bằng chứng số (MinIO, mã băm SHA-256, tọa độ không gian 3D, timestamp) bảo đảm tính toàn vẹn dữ liệu kỹ thuật và chuỗi truy xuất nguồn gốc.
5. **Nghị định số 123/2020/NĐ-CP & Thông tư số 78/2021/TT-BTC về Hóa đơn, Chứng từ điện tử**:
   - Phân định rõ trách nhiệm hóa đơn: `PROVIDER_MANAGER` (đơn vị cung cấp dịch vụ) lập hóa đơn giá trị gia tăng dịch vụ kiểm định/bảo trì gửi `CLIENT`; Nền tảng (Platform) lập hóa đơn điện tử thu phí dịch vụ sàn (hoa hồng kết nối $C$) gửi `PROVIDER_MANAGER`.
6. **Luật Thương mại điện tử 2025 & Luật Bảo vệ quyền lợi người tiêu dùng 2023**:
   - Quy chế công khai điều khoản sàn, minh bạch năng lực Provider, cơ chế hòa giải khiếu nại nội bộ có ghi nhận audit log, không hạn chế quyền khởi kiện của các bên ra Tòa án hoặc Trọng tài thương mại (VIAC).

---

## II. Hệ thống Vai trò & Khối Tác quyền (Actor Zones & 6 Canonical Roles)

Hệ thống được tổ chức thành **3 Khối tác nhân (Actor Zones)** độc lập, bảo đảm nguyên tắc phân chia trách nhiệm (Separation of Duties):

```
┌────────────────────────────────────────────────────────────────────────┐
│               KHỐI 1: PLATFORM GOVERNANCE (Đơn vị chủ quản Sàn)        │
│                                                                        │
│   🛠️ PLATFORM_ADMIN                  👔 PLATFORM_OPERATOR              │
│   (Quản trị Kỹ thuật & Hạ tầng)      (Quản trị Nghiệp vụ, Chính sách   │
│   • Cấu hình hệ thống, checklist     & Xử lý Khiếu nại Nội bộ)         │
│   • Phân quyền, bảo mật              • Thẩm định & Cấp phép Providers  │
│   • Ngưỡng AI YOLO, upload MinIO     • Cấu hình Tham số Thương mại Sàn │
│   • Giám sát hạ tầng, audit logs     • Tiếp nhận & Hòa giải Khiếu nại  │
│                                      • Điều phối Trạng thái Thanh toán │
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
| **1. Platform Governance** | `PLATFORM_ADMIN` | **Quản trị viên Kỹ thuật & Hệ thống**: Quản trị tài khoản, cấu hình bảo mật, duy trì bộ Checklist tiêu chuẩn ngành, cấu hình ngưỡng phát hiện AI YOLO (`yolo_confidence_threshold`), giám sát đường ống dữ liệu MinIO, kiểm tra audit log. Không can thiệp vào tham số thương mại hay phân xử tranh chấp. |
| | `PLATFORM_OPERATOR` | **Quản trị viên Vận hành Nghiệp vụ & Hòa giải Sàn**: Thẩm định năng lực pháp lý Provider (giấy phép kinh doanh, bảo hiểm, định danh drone, chứng chỉ bay); **quản trị và điều chỉnh các tham số thương mại sàn (Tỷ lệ hoa hồng $r$, Tỷ lệ bảo lãnh $H$, Thời hạn nghiệm thu, Phí phạt hủy)**; giám sát luồng thanh toán có điều kiện; **chủ trì hòa giải khiếu nại nội bộ theo Quy chế Sàn (Platform Terms)**. Khi có tranh chấp kỹ thuật phức tạp, có thẩm quyền yêu cầu biên bản giám định của bên thứ ba độc lập do các bên cung cấp. |
| **2. Customer Organization** | `CLIENT` | **Khách hàng Doanh nghiệp / Chủ sở hữu hạ tầng**: Quản lý danh mục tài sản hạ tầng; tạo yêu cầu khảo sát (chỉ định hoặc chào thầu mở RFQ); ký Hợp đồng dịch vụ điện tử; thực hiện nạp tiền đảm bảo thanh toán qua đối tác thanh toán được cấp phép; nghiệm thu báo cáo kỹ thuật; mở khiếu nại/tranh chấp khi có sai lệch kỹ thuật; duyệt đơn bảo trì và nghiệm thu hoàn công. |
| **3. Service Provider** | `PROVIDER_MANAGER` | **Quản lý Đơn vị Dịch vụ Drone / Bảo trì**: Khai báo hồ sơ công ty và đội ngũ kỹ thuật; tiếp nhận RFQ; lập Báo giá dịch vụ (chỉ gồm công bay, kỹ thuật, vật tư, di chuyển, VAT — **không** tính phí AI/MinIO của Sàn); đính kèm giấy phép bay của cơ quan có thẩm quyền; phê duyệt Kế hoạch bay Drone (Mission Plan); phân công phi công; kiểm tra tính đầy đủ và ký phát hành báo cáo QA chính thức. |
| | `INSPECTOR` | **Phi công Drone / Thanh tra viên Hiện trường**: Lập kế hoạch trắc địa (GSD, overlap, shot items, gimbal); **chịu trách nhiệm trực tiếp về an toàn bay tại hiện trường (Pilot-in-Command)**; kích hoạt bay bù/bay lại khi ảnh không đạt chuẩn; nạp ảnh và bóc tách telemetry; xác minh và hiệu chỉnh kích thước khuyết tật do AI ước lượng; tự hoàn thiện và ký xác nhận bản thảo báo cáo trước khi trình Provider Manager. |
| | `MAINTENANCE_ENGINEER` | **Kỹ sư Bảo trì / Sửa chữa**: Khảo sát hiện trường khuyết tật; lập Phương án kỹ thuật sửa chữa & dự toán vật tư; dừng thi công và lập Change Order khi phát hiện hư hỏng ngầm; thi công sửa chữa; **bắt buộc nạp cặp ảnh đối chứng Trước/Sau (Before/After Evidence)** kèm nhật ký vật tư để làm căn cứ nghiệm thu. |

---

## III. Mô hình Điều phối Thanh toán có Điều kiện (Conditional Payment) & Hợp đồng Điện tử

### 1. Mô hình Hợp đồng Điện tử (Platform Terms + Bilateral Service Order)
* **Quy chế hoạt động Sàn (Platform Terms of Service)**: Ràng buộc Client và Provider khi tham gia nền tảng. Trao quyền cho `PLATFORM_OPERATOR` điều chỉnh chính sách thương mại công khai và đóng vai trò trung gian hòa giải khiếu nại theo quy chế; không thay thế cơ quan tài phán nhà nước.
* **Đơn dịch vụ điện tử (Inspection Service Order / Maintenance Work Order)**: Hợp đồng giao kết điện tử giữa Client và Provider cho từng thương vụ, tuân thủ *Luật Giao dịch điện tử 2023*. Bao gồm: Phạm vi công việc (SOW), Kế hoạch bay kỹ thuật (GSD mục tiêu, Shot list, Overlap), Tiến độ cam kết (SLA), Chi phí dịch vụ Provider và các điều khoản thương mại đã được khóa bất biến (Snapshot) tại thời điểm ký kết.

### 2. Quản lý Vòng đời Thanh toán có Điều kiện qua Đối tác Thanh toán được Cấp phép
1. **Nạp tiền đảm bảo thanh toán (Advance Funding)**: Nếu Service Order quy định nạp trước, Client chuyển tiền vào tài khoản đảm bảo thanh toán mở tại Ngân hàng thương mại / Cổng trung gian thanh toán đối tác được cấp phép theo Nghị định 52/2024/NĐ-CP. Trạng thái hợp đồng ghi nhận `FUNDED_IN_PARTNER_ESCROW`. Platform **chỉ quản lý máy trạng thái (State Machine)**, không trực tiếp nắm giữ tiền gửi của khách hàng.
2. **Giải ngân theo điều kiện nghiệm thu (Settlement on Acceptance)**: Sau khi Client bấm "Nghiệm thu (Accept)" hoặc điều kiện tự động nghiệm thu theo hợp đồng đạt đến, Platform gửi chỉ thị thanh toán điện tử sang đối tác cổng thanh toán để giải ngân phần tiền ròng $(B - C)$ cho Provider và trích phí hoa hồng $C$ cho Platform.
3. **Tạm dừng thanh toán khi có tranh chấp (`FROZEN_DISPUTED`)**: Khi một bên mở tranh chấp hợp lệ, Platform ghi nhận trạng thái tranh chấp và chỉ gửi yêu cầu tạm dừng/không giải ngân nếu đối tác thanh toán hỗ trợ cơ chế này theo hợp đồng tích hợp. Nếu không hỗ trợ, giao dịch được xử lý theo cơ chế dispute/refund/settlement của đối tác. Khoản tiền chỉ được giải quyết theo điều khoản hợp đồng, kết quả hòa giải được các bên chấp thuận hoặc quyết định của cơ quan tài phán có thẩm quyền.

### 3. Chính sách Cấu hình Động của `PLATFORM_OPERATOR` & Nguyên tắc Contract Snapshot
Toàn bộ các tham số thương mại và vận hành trên sàn **tuyệt đối không bị hardcode**, được cấu hình tập trung bởi `PLATFORM_OPERATOR`:

| Tham số Cấu hình | Ký hiệu | Giá trị áp dụng | Thẩm quyền Quản lý | Phạm vi & Tác động |
| :--- | :---: | :---: | :---: | :--- |
| **Tỷ lệ hoa hồng sàn** | $r$ (`commission_rate`) | Operator ban hành theo kỳ | `PLATFORM_OPERATOR` | Áp dụng cho Provider; tính trên doanh thu dịch vụ hợp lệ trước VAT: $C = r \times B$. |
| **Thời hạn nghiệm thu hợp đồng** | $T_{rev}$ (`contract_review_period_days`) | Operator cấu hình theo policy | `PLATFORM_OPERATOR` | Thời hạn Client thẩm định báo cáo; giá trị được snapshot vào Service Order làm căn cứ nghiệm thu mặc định. |
| **Tỷ lệ nạp tiền đảm bảo** | $D$ (`advance_funding_rate`) | Operator cấu hình theo policy | `PLATFORM_OPERATOR` | Tỷ lệ tiền Client cần nạp trước khi khởi công; snapshot vào Service Order. |
| **Tỷ lệ bảo lãnh hoàn công** | $H$ (`warranty_retention_rate`) | Operator cấu hình theo policy | `PLATFORM_OPERATOR` | Tỷ lệ giữ lại bảo hành hoàn công trong Maintenance Order (nếu hai bên thỏa thuận áp dụng). |
| **Thời hạn bảo hành tiêu chuẩn** | $T_{war}$ (`standard_warranty_days`) | Operator cấu hình theo policy | `PLATFORM_OPERATOR` | Thời hạn bảo hành công trình trước khi giải ngân phần tiền bảo lãnh $H$. |
| **Chính sách hủy và bồi hoàn** | `cancellation_policy` | Operator cấu hình theo policy | `PLATFORM_OPERATOR` | Quy định mức bồi hoàn/chi phí phát sinh theo từng mốc thời gian và lý do hủy chuyến bay. |

* **Nguyên tắc Khóa Bất biến Hợp đồng (Contract Snapshot Pattern)**:
  * Khi Service Order được xác lập, hệ thống sao chép (snapshot) toàn bộ giá trị tham số tại thời điểm đó vào bản ghi hợp đồng.
  * Mọi thay đổi chính sách của `PLATFORM_OPERATOR` sau đó chỉ áp dụng cho các hợp đồng tạo mới, tuyệt đối không làm thay đổi các hợp đồng đang thực hiện.

### 4. Hạ tầng Dữ liệu, Mô hình AI YOLO và LLM do Nền tảng Cung cấp Tập trung
* Hệ thống lưu trữ đối tượng MinIO, pipeline thị giác máy tính **AI YOLO** và trợ lý **LLM** là năng lực hạ tầng dùng chung do Platform trực tiếp host và chịu chi phí vận hành từ nguồn thu hoa hồng $C$.
* **Provider** không được phép bóc tách hay tính thêm chi phí xử lý AI/lưu trữ dữ liệu vào Báo giá gửi Client.
* **Nguyên tắc Phản biện Con người (Human-in-the-loop)**: AI chỉ đóng vai trò trợ lý đề xuất ứng viên lỗi (Candidates) và soạn thảo bản thảo (Draft). Toàn bộ kết quả kiểm định chính thức bắt buộc phải do con người (`INSPECTOR` và `PROVIDER_MANAGER`) thẩm định, đo đạc, chỉnh sửa và ký duyệt.

---

## IV. Sơ đồ Kiến trúc Nghiệp vụ Tổng thể & Vòng lặp Phi tuyến tính (End-to-End Dynamic Workflow)

Hệ thống hoạt động theo mô hình vòng đời hoàn chỉnh có phản hồi và xử lý ngoại lệ:

```
                      ┌──────────────────────────────────────────┐
                      │    SF: ASSET & PROVIDER ONBOARDING       │
                      └────────────────────┬─────────────────────┘
                                           │
                                           ▼
                      ┌──────────────────────────────────────────┐
                      │    MF1: RFQ & CONDITIONAL FUNDING        │
                      └────────────────────┬─────────────────────┘
                                           │
                                           ▼
                      ┌──────────────────────────────────────────┐
                      │    MF2: FLIGHT PLANNING & CLEARANCE      │
                      └─────────┬──────────────────────┬─────────┘
                                │                      │
                        [Permit/Plan OK]        [Weather/Safety Abort]
                                │                      │
                                ▼                      ▼
                      ┌───────────────────┐    [Reschedule / Re-plan]
                      │ MF3: FIELD FLIGHT │
                      └─────────┬─────────┘
                                │
                                ▼
                      ┌──────────────────────────────────────────┐
                      │     EVIDENCE QUALITY & COVERAGE GATE     │
                      └─────────┬──────────────────────┬─────────┘
                                │                      │
                          [Data Valid]          [Blur / Missing / No GPS]
                                │                      │
                                │                      ▼
                                │              [Re-flight / Bay bù]
                                │                      │
                                ├──────────────────────┘
                                ▼
                      ┌──────────────────────────────────────────┐
                      │ AI ESTIMATION & INSPECTOR VERIFICATION   │
                      └────────────────────┬─────────────────────┘
                                           │
                                           ▼
                      ┌──────────────────────────────────────────┐
                      │     LLM DRAFT & QA REPORT RELEASE        │
                      └────────────────────┬─────────────────────┘
                                           │
                                           ▼
                      ┌──────────────────────────────────────────┐
                      │         MF4: CLIENT ACCEPTANCE           │
                      └─────────┬──────────────┬───────────────┬─┘
                                │              │               │
                            [Accept]      [Clarify]        [Dispute]
                                │              │               │
                                ▼              ▼               ▼
                        [Disburse Funds] [Revise Report] [Internal Dispute
                                │              │         & Expert Review]
                                │              └───────────────┘
                                ▼
                      ┌──────────────────────────────────────────┐
                      │     MF5: MAINTENANCE WORK ORDER          │
                      └────────────────────┬─────────────────────┘
                                           │
                                           ▼
                      ┌──────────────────────────────────────────┐
                      │    TECHNICAL ASSESSMENT & QUOTATION      │
                      └────────────────────┬─────────────────────┘
                                           │
                                           ▼
                      ┌──────────────────────────────────────────┐
                      │       REPAIR & BEFORE/AFTER EVIDENCE     │
                      └─────────┬──────────────────────┬─────────┘
                                │                      │
                          [Work Complete]        [Hidden Defect Found]
                                │                      │
                                │                      ▼
                                │             [Change Order Approval]
                                │                      │
                                ├──────────────────────┘
                                ▼
                      ┌──────────────────────────────────────────┐
                      │        MAINTENANCE ACCEPTANCE            │
                      └─────────┬──────────────────────┬─────────┘
                                │                      │
                            [Passed]                [Failed]
                                │                      │
                                ▼                      ▼
                        [Warranty Clock]        [Rework Loop]
                                │
                                ▼
                         [Ticket Closed]
```

---

## V. Chi tiết Luồng Nghiệp vụ (Supporting Flow & 5 Core Main Flows)

---

### Supporting Flow (SF) — Khai báo Danh mục, Thẩm định Pháp lý & Quản trị Không phận Ban đầu

> **Bản chất**: Luồng Tiền đề quản trị dữ liệu danh mục ban đầu (Master Data Management / Onboarding) để thiết lập môi trường hoạt động an toàn và hợp pháp cho các giao dịch.

**Tác nhân chính**: `PLATFORM_ADMIN`, `PLATFORM_OPERATOR`, `CLIENT`, `PROVIDER_MANAGER`, `System`.

#### 1. Quy trình chi tiết (Sequence Steps)
* **SF-01 (Client Self-Registration)**: Đại diện doanh nghiệp khách hàng tự đăng ký tài khoản tổ chức, cung cấp mã số thuế, thông tin người đại diện theo pháp luật và kích hoạt tài khoản `CLIENT`.
* **SF-02 (Provider Onboarding & Vetting Submission)**: Provider Manager đăng ký hồ sơ năng lực của công ty: Giấy phép kinh doanh dịch vụ khảo sát; Danh mục phương tiện bay drone kèm Giấy chứng nhận đăng ký định danh phương tiện bay của Bộ Quốc phòng theo *Nghị định 288/2025/NĐ-CP*; Danh sách phi công kèm Chứng chỉ điều khiển phương tiện bay hợp lệ; Chứng thư bảo hiểm trách nhiệm dân sự bên thứ ba còn hiệu lực.
* **SF-03 (Operator Vetting Approval)**: `PLATFORM_OPERATOR` thẩm định tính pháp lý và hiệu lực của hồ sơ Provider. Nếu đạt, cấp trạng thái `VERIFIED`. Nếu thiếu hoặc hết hạn, chuyển `ADDITIONAL_INFO_REQUIRED` hoặc `REJECTED`. Provider chưa được duyệt bị chặn toàn bộ quyền tham gia báo giá.
* **SF-04 (Asset Profiling & Airspace Pre-check)**: Client khai báo thông tin tài sản công trình: Tọa độ địa lý (kinh độ, vĩ độ), ranh giới tiếp cận, chiều cao đỉnh công trình, bản vẽ hoàn công. Hệ thống tự động tra cứu dữ liệu không phận số (`cambay.mod.gov.vn` theo QĐ 18/2020/QĐ-TTg) để hiển thị cảnh báo tham khảo sớm nếu tài sản nằm trong hoặc tiếp giáp vùng cấm/hạn chế bay.
* **SF-05 (Periodic Schedule Cadence)**: Platform tự động sinh các đề xuất lịch kiểm định (Schedule Proposals) theo chu kỳ bảo trì cấu hình sẵn cho từng loại công trình; Client rà soát và xác nhận lịch chính thức để làm căn cứ tự động tạo gói yêu cầu kiểm tra khi đến hạn.

#### 2. Xử lý Ngoại lệ SF
* **Hồ sơ Provider giả mạo hoặc hết hạn bảo hiểm**: Operator từ chối duyệt, khóa quyền tham gia sàn và ghi log kiểm toán.
* **Tài sản nằm trong vùng cấm bay tuyệt đối (khu quân sự, khu vực trọng yếu)**: Hệ thống gắn cờ cảnh báo `NO_FLY_ZONE_ALERT`, khuyến cáo Client cần chuẩn bị phương án xin cấp phép bay đặc biệt trước khi phát hành RFQ.

---

### MF1 — Yêu cầu Khảo sát, Đấu thầu Chọn thầu Thông minh & Nạp tiền Đảm bảo Thanh toán (Survey Request, Smart RFQ & Conditional Funding)

**Mục tiêu**: Tiếp nhận nhu cầu kiểm định, kết nối thông minh đến các Provider đủ năng lực, chốt báo giá, ký hợp đồng điện tử song phương và nạp tiền đảm bảo thanh toán theo điều kiện hợp đồng.

**Tác nhân chính**: `CLIENT`, `PLATFORM_OPERATOR`, `PROVIDER_MANAGER`, `System`.

#### 1. Quy trình chi tiết (Main Sequence)

| Bước | Vai trò / Lane | Hoạt động chi tiết | Sản phẩm đầu ra |
| :--- | :--- | :--- | :--- |
| **MF1-01** | Client | Khởi tạo Yêu cầu khảo sát: Chọn phương thức (A) **Chỉ định trực tiếp** Provider quen thuộc, hoặc (B) **Chào thầu mở (Open RFQ)**. Xác định rõ mục tiêu kiểm tra (tìm nứt bê tông, gỉ sét cấu kiện, thấm dột), phạm vi cấu kiện và tiến độ mong muốn. | Yêu cầu kiểm tra (RFQ) |
| **MF1-02** | System | **Bộ lọc Nhà cung cấp Đủ điều kiện (Smart Eligibility Filter)**: Hệ thống tự động lọc danh sách Provider dựa trên: (1) Khu vực địa lý hoạt động; (2) Sở hữu loại drone và cảm biến phù hợp với mục tiêu kiểm định; (3) Phi công có chứng chỉ hợp lệ; (4) Trạng thái hồ sơ `VERIFIED`; (5) Lịch khả dụng. Chỉ gửi thư mời chào thầu (RFQ Invitation) tới các Provider đáp ứng tiêu chí. | Danh sách Eligible Providers nhận RFQ |
| **MF1-03** | Provider Manager | Nghiên cứu yêu cầu, khảo sát thực địa từ xa qua bản đồ/bản vẽ và lập **Báo giá dịch vụ (Quotation)**: Chi tiết hóa gồm (1) Chi phí nhân lực phi công hiện trường; (2) Chi phí thiết bị drone/cảm biến; (3) Chi phí di chuyển/triển khai; (4) Thuế VAT. **Tuyệt đối không tính phí xử lý AI/MinIO của Sàn vào báo giá.** | Báo giá dịch vụ (Quotation) |
| **MF1-04** | Client | Xem xét các báo giá cạnh tranh. Có thể gửi yêu cầu đàm phán/hiệu chỉnh (Revision) hoặc chọn Báo giá tối ưu nhất để chấp thuận. | Báo giá được chấp thuận |
| **MF1-05** | System | Khởi tạo **Hợp đồng Dịch vụ Điện tử (Inspection Service Order)**: Thực hiện **Contract Snapshot** lưu trữ bất biến các giá trị tỷ lệ hoa hồng $r$, thời hạn nghiệm thu $T_{rev}$, tỷ lệ nạp tiền đảm bảo $D$ và chính sách hủy tại thời điểm giao kết. | Hợp đồng điện tử sẵn sàng ký |
| **MF1-06** | Client & Provider Manager | Hai bên thực hiện ký số/chấp thuận Service Order điện tử. Client nạp khoản tiền đảm bảo $D$ vào tài khoản chỉ định của đối tác thanh toán được cấp phép (theo NĐ 52/2024/NĐ-CP). Hệ thống cập nhật trạng thái hợp đồng sang `FUNDED_IN_PARTNER_ESCROW` và kích hoạt luồng lập kế hoạch bay. | Hợp đồng có hiệu lực & Trạng thái thanh toán kích hoạt |

#### 2. Xử lý Ngoại lệ & Rủi ro Thời tiết MF1
* **Không có Provider nào nộp báo giá sau thời hạn RFQ**: Hệ thống thông báo Client mở rộng phạm vi địa lý hoặc điều chỉnh ngân sách/tiến độ mong muốn.
* **Thời tiết bất khả kháng (Mưa bão, gió lớn vượt ngưỡng bay an toàn)**: Hai bên lập biên bản hoãn chuyến bay trên hệ thống; dời lịch bay mà không áp dụng chế tài phạt hủy hay tính vi phạm tiến độ SLA.
* **Client hủy chuyến bay trước khi khởi hành**: Áp dụng chính sách bồi hoàn snapshot trong Service Order: Khấu trừ chi phí chuẩn bị thực tế hợp lý cho Provider (nếu có), phần còn lại đối tác thanh toán hoàn trả Client.

---

### MF2 — Lập Kế hoạch Bay Chuyên dụng, Đề xuất GSD & Kiểm tra Điều kiện Bay & Hồ sơ Pháp lý (Mission Planning & Flight Compliance) 🚀 [FLOW NỔI BẬT DRONE]

> **Trọng tâm kỹ thuật Drone**: Phân tách rõ ràng giữa năng lực tính toán trắc địa ảnh và thẩm quyền an toàn bay; kiểm soát chặt chẽ hồ sơ cấp phép bay theo quy định pháp luật mới nhất.

**Tác nhân chính**: `INSPECTOR` (Phi công - Pilot in Command), `PROVIDER_MANAGER`, `System`.

#### 1. Quy trình chi tiết (Main Sequence)

| Bước | Vai trò / Lane | Hoạt động chi tiết | Sản phẩm đầu ra |
| :--- | :--- | :--- | :--- |
| **MF2-01** | Inspector | **Tính toán trắc địa ảnh & Đề xuất khoảng cách chụp theo GSD mục tiêu**: Dựa trên độ rộng vết nứt tối thiểu cần phát hiện (ví dụ vết nứt $\ge 1.0\text{ mm}$ yêu cầu $\text{GSD} \le 0.5\text{ mm/pixel}$). Inspector nhập thông số camera/cảm biến (tiêu cự focal length, kích thước cảm biến sensor size, độ phân giải). Hệ thống tính toán/đề xuất **khoảng cách chụp và thông số ảnh phù hợp**; thông số này chỉ phục vụ chất lượng dữ liệu, không được hiểu là hệ thống tự xác định độ cao bay an toàn. | Thông số GSD & Khoảng cách chụp khuyến nghị |
| **MF2-02** | Inspector | **Thiết lập tỷ lệ chồng phủ ảnh (Image Overlap Calculation)**: Cấu hình tỷ lệ chồng phủ dọc (Forward Overlap $\ge 75\%$) và ngang (Side Overlap $\ge 60\%$) phù hợp với hình học bề mặt kết cấu, bảo đảm không có điểm mù và phục vụ dựng mô hình khuyết tật 3D. | Tham số Overlap đạt chuẩn trắc địa |
| **MF2-03** | Inspector | **Xây dựng Danh mục Điểm chụp Cấu kiện (Structural Shot List & Gimbal Pitch)**: Thiết lập danh mục cấu kiện cần chụp, góc nghiêng camera (Gimbal Pitch: $0^\circ, -45^\circ, -90^\circ$). Thiết lập tọa độ điểm bay (Waypoints) nếu dùng chế độ bay lập trình, hoặc shot list hướng dẫn chi tiết nếu bay thủ công. | Structural Shot List & Waypoint Mission Plan |
| **MF2-04** | Inspector & System | **Kiểm tra Không phận & Cảnh báo Quy định (Airspace Check & Regulatory Alert)**: Hệ thống kiểm tra tọa độ/khu vực bay với nguồn dữ liệu không phận được cấu hình hoặc cập nhật hợp lệ; có thể tham chiếu Cổng thông tin Vùng cấm bay. Kết quả chỉ là cảnh báo hỗ trợ lập kế hoạch, không phải giấy phép bay và không thay thế xác nhận của cơ quan có thẩm quyền. | Báo cáo kiểm tra không phận tham khảo |
| **MF2-05** | Provider Manager | **Kiểm soát Hồ sơ Pháp lý & Điều kiện Bay (Theo quy định hiện hành)**: Đính kèm giấy phép/chấp thuận hoặc hồ sơ pháp lý cần thiết nếu hoạt động thuộc trường hợp phải thực hiện thủ tục; kiểm tra thông tin định danh phương tiện bay và điều kiện của người điều khiển theo quy định hiện hành. Provider chịu trách nhiệm bảo đảm hồ sơ pháp lý của chuyến bay; hệ thống chỉ kiểm tra tính đầy đủ và thời hạn của hồ sơ đã được cung cấp. | Hồ sơ cấp phép bay hoàn tất |
| **MF2-06** | Inspector & Provider Manager | **Xác nhận An toàn Bay Hiện trường (Pilot-in-Command Safety Sign-off)**: Phi công trực tiếp kiểm tra chướng ngại vật thực địa, tĩnh không công trình và điều kiện khí tượng. **Phi công ký cam kết an toàn bay**; Provider Manager phê duyệt ban hành Kế hoạch bay. Hệ thống chuyển trạng thái đơn hàng sang **`READY_FOR_FLIGHT`**. | Kế hoạch bay được phê duyệt (`READY_FOR_FLIGHT`) |

#### 2. Xử lý Ngoại lệ MF2
* **Không xin được giấy phép bay của cơ quan có thẩm quyền**: Kế hoạch bay bị từ chối; Provider Manager thông báo Client để gia hạn thời gian xin phép hoặc hủy hợp đồng theo điều khoản bất khả kháng pháp lý.
* **Thiết bị camera không đạt GSD yêu cầu**: Hệ thống chặn bước phê duyệt, yêu cầu Inspector thay đổi ống kính/loại cảm biến hoặc giảm khoảng cách chụp tiếp cận (khi điều kiện an toàn cho phép).

---

### MF3 — Khảo sát Hiện trường, Cổng kiểm soát Chất lượng Ảnh, AI YOLO & Phát hành Báo cáo (Field Survey, Evidence Quality Gate, AI Analysis & QA Release)

**Mục tiêu**: Thực hiện chuyến bay an toàn, kiểm soát chất lượng ảnh chụp ngay tại hiện trường, ước lượng khuyết tật qua AI YOLO có người xác minh (Human-in-the-loop), tổng hợp báo cáo bằng LLM và phát hành báo cáo QA chính thức.

**Tác nhân chính**: `Inspector` (Phi công hiện trường & tác giả báo cáo), `Provider Manager`, Platform MinIO, Platform AI Services, `System`.

#### 1. Quy trình chi tiết (Main Sequence)

| Bước | Vai trò / Lane | Hoạt động chi tiết | Sản phẩm đầu ra |
| :--- | :--- | :--- | :--- |
| **MF3-01** | Inspector | Mở ứng dụng Mobile/Web tại hiện trường, kích hoạt phiên khảo sát (`IN_PROGRESS`). Thực hiện kiểm tra an toàn trước bay (Pre-flight Check). Trực tiếp điều khiển drone thực hiện danh mục chụp cấu kiện theo Mission Plan đã duyệt. | Phiên bay hiện trường được ghi nhận |
| **MF3-02** | Inspector | Tải toàn bộ tệp ảnh/video độ phân giải cao thu được lên hệ thống lưu trữ MinIO của Platform qua cơ chế tải phân đoạn (Chunked Upload). | Dữ liệu hình ảnh thô |
| **MF3-03** | System (MinIO & Metadata Ingestion) | Tự động bóc tách **Dữ liệu Không gian Telemetry**: Tọa độ GPS 3D, độ cao tương đối AGL, góc gimbal, timestamp; tính mã băm toàn vẹn **SHA-256** cho từng file ảnh để chống giả mạo bằng chứng số. | Bằng chứng số được bảo vệ toàn vẹn |
| **MF3-04** | Inspector & System | **Cổng Kiểm soát Chất lượng & Độ bao phủ Bằng chứng (Evidence Quality & Coverage Gate)**: Hệ thống tự động kiểm tra độ sắc nét (phát hiện ảnh mờ/blur), tính hợp lệ của GPS và độ đủ của shot list. Nếu phát hiện ảnh mờ, thiếu sáng hoặc thiếu góc chụp cấu kiện quan trọng, hệ thống kích hoạt cảnh báo. Inspector thực hiện **Chuyến bay bổ sung / Bay bù (Re-flight / Additional Flight)** ngay tại hiện trường trước khi thu dọn thiết bị. | Bộ bằng chứng kiểm định đạt chuẩn |
| **MF3-05** | System (Platform YOLO AI Service) | Pipeline AI YOLO của Platform tự động quét các ảnh hợp lệ; nhận diện các khuyết tật (vết nứt bê tông, gỉ sét cốt thép, bong tróc). Hệ thống **ước lượng kích thước hình học sơ bộ của khuyết tật** dựa trên GSD, thông tin hiệu chuẩn/hình học ảnh và vùng khuyết tật được AI nhận diện. Kết quả là ước lượng hỗ trợ chuyên gia, không được coi là số đo kiểm định cuối cùng nếu chưa được Inspector xác minh. Xuất danh mục **Ứng viên lỗi (Defect Candidates)** kèm hộp bao (Bounding Box). | Danh mục ứng viên lỗi kèm ước lượng GSD |
| **MF3-06** | Inspector (Human-in-the-loop) | Trực quan kiểm tra từng ảnh và ứng viên AI: **Xác nhận (Confirm)**, **Hiệu chỉnh kích thước/vị trí (Modify)**, hoặc **Bác bỏ (Reject)** các nhận diện sai của AI. Nếu AI bỏ sót khuyết tật, Inspector **thêm lỗi thủ công (Manual Finding)** và sử dụng thước đo trắc địa để nhập số đo chính xác. Hoàn tất checklist kiểm định. | Danh mục khuyết tật đã thẩm định chuyên môn |
| **MF3-07** | System (Platform LLM Assistant) | Trợ lý LLM tổng hợp dữ liệu có cấu trúc từ checklist, telemetry, ảnh bằng chứng và các khuyết tật đã được Inspector xác nhận; tự động tạo bản thảo báo cáo kỹ thuật. Đánh dấu rõ nội dung do AI hỗ trợ soạn thảo và phiên bản model. | Bản thảo Báo cáo Kỹ thuật (Draft) |
| **MF3-08** | Inspector (Tác giả Báo cáo) | **Tự xác minh, chỉnh sửa và chịu trách nhiệm chuyên môn**: Inspector rà soát từng kết luận, phân tích nguyên nhân sơ bộ, khuyến nghị khắc phục, sửa đổi câu chữ cho chuẩn xác thuật ngữ xây dựng. Ký điện tử xác nhận bản thảo hoàn thiện trình Provider Manager. | Báo cáo hoàn chỉnh do Inspector xác nhận |
| **MF3-09** | Provider Manager | Kiểm tra tính đầy đủ hành chính và mức độ tuân thủ SOW/hợp đồng. Nếu đạt, **Ký phát hành Báo cáo Chính thức (Release Final QA Report)** gửi Client. Hệ thống kích hoạt thời hạn nghiệm thu $T_{rev}$ đã snapshot trong hợp đồng. | Báo cáo chính thức ban hành & Kích hoạt $T_{rev}$ |

#### 2. Xử lý Ngoại lệ Hiện trường MF3 (Exception Flows)
* **Sự cố drone giữa chuyến bay (In-flight Hardware/Telemetry Failure)**:
  - Nếu mất tín hiệu điều khiển, pin tụt đột ngột hoặc hỏng động cơ: Inspector kích hoạt quy trình hạ cánh khẩn cấp an toàn (Fail-safe Return-to-Home / Emergency Landing).
  - Inspector lập **Biên bản sự cố hiện trường (Incident Log)** trên hệ thống, ghi nhận nguyên nhân, tình trạng hư hỏng thiết bị và hiện trạng tài sản công trình.
  - Thông báo Provider Manager và Client để dời lịch bay lại (Reschedule) sau khi đã kiểm tra an toàn thiết bị thay thế.
* **Thời tiết xấu đột xuất khi đang bay (Gió giật, mưa bất chợt)**:
  - Inspector ra lệnh thu hồi drone ngay lập tức (Abort Flight). Chuyến bay được tạm dừng, lưu trữ phần dữ liệu đã chụp thành công và thiết lập lịch bay bù cho phần còn lại.
* **Dịch vụ AI YOLO / LLM tạm thời gián đoạn**:
  - Hệ thống tự động chuyển sang cơ chế **Manual Fallback**: Inspector tự khoanh vùng khuyết tật và lập báo cáo thủ công trên mẫu chuẩn, bảo đảm tiến độ bàn giao báo cáo cho Client không bị đình trệ.

---

### MF4 — Nghiệm thu Báo cáo, Quyết toán Theo Điều khoản & Xử lý Khiếu nại Nội bộ (Report Acceptance, Settlement & Internal Dispute Resolution)

**Mục tiêu**: Khách hàng thẩm định kết quả kiểm định; thực hiện thanh toán giải ngân theo hợp đồng đã snapshot; giải quyết yêu cầu làm rõ kỹ thuật và hòa giải khiếu nại nội bộ bảo vệ quyền lợi các bên.

**Tác nhân chính**: `Client`, `Provider Manager`, `PLATFORM_OPERATOR`, Đối tác thanh toán được cấp phép, `System`.

#### 1. Quy trình chi tiết (Main Sequence)

| Bước | Vai trò / Lane | Hoạt động chi tiết | Sản phẩm đầu ra |
| :--- | :--- | :--- | :--- |
| **MF4-01** | Client | Nhận thông báo và xem xét Báo cáo kỹ thuật chính thức trên Web/Mobile (ảnh khuyết tật độ phân giải cao, tọa độ 3D, số đo vết nứt, phân loại mức độ rủi ro). Bắt đầu đếm ngược thời hạn nghiệm thu $T_{rev}$ đã snapshot trong hợp đồng. | Báo cáo trong giai đoạn thẩm định |
| **MF4-02a** | Client (Nhánh Nghiệm thu Đạt) | Client hài lòng với chất lượng báo cáo -> Bấm **"Nghiệm thu (Accept)"**. | Quyết định nghiệm thu chính thức |
| **MF4-02b** | System (Nhánh Nghiệm thu Mặc định theo Hợp đồng) | Hết thời hạn $T_{rev}$ theo thỏa thuận trong Service Order mà Client không có phản hồi và không mở yêu cầu làm rõ/tranh chấp -> Hệ thống kích hoạt **Nghiệm thu mặc định (Contractual Auto-Acceptance)** chỉ được kích hoạt khi Service Order quy định rõ thời hạn nghiệm thu và cơ chế này được áp dụng cho giao dịch đó. | Quyết định nghiệm thu theo điều khoản hợp đồng |
| **MF4-03** | System & Đối tác Thanh toán | Hợp đồng chuyển trạng thái hoàn thành (`COMPLETED`). Platform gửi chỉ thị thanh toán điện tử sang đối tác cổng thanh toán: Giải ngân số tiền ròng $(B - C)$ cho Provider; trích hoa hồng sàn $C = r \times B$ cho Platform. **Nghĩa vụ Hóa đơn Điện tử (NĐ 123/2020/NĐ-CP)**: `PROVIDER_MANAGER` (đơn vị cung cấp dịch vụ) thực hiện lập hóa đơn điện tử cho dịch vụ cung cấp cho `CLIENT` theo phương pháp và quy định thuế áp dụng; Nền tảng (Platform) thực hiện nghĩa vụ hóa đơn đối với khoản phí dịch vụ sàn/hoa hồng mà Provider phải trả theo quy định áp dụng. | Lệnh giải ngân hoàn tất & Hóa đơn điện tử hợp lệ |
| **MF4-04** | Client & Provider Manager | **Nhánh Yêu cầu Làm rõ Kỹ thuật (Clarification Loop)**: Nếu một số kết luận chưa rõ, Client gửi yêu cầu làm rõ trên hệ thống kèm mốc thời gian phản hồi. Provider Manager và Inspector rà soát dữ liệu ảnh gốc, cập nhật báo cáo giải trình hoặc phát hành bản báo cáo hiệu chỉnh (Client không được tự ý sửa đổi kết luận chuyên môn). Client thẩm định lại để nghiệm thu. | Báo cáo giải trình hiệu chỉnh |
| **MF4-05** | Client / Provider | **Nhánh Mở Tranh chấp (Open Dispute)**: Khi có mâu thuẫn kỹ thuật nghiêm trọng (ảnh chụp sai lệch GSD cam kết dẫn đến đo sai vết nứt, bỏ sót khuyết tật nguy hiểm, drone va quẹt gây hư hỏng công trình): Một trong hai bên bấm **"Mở Tranh chấp"** và nộp hồ sơ chứng cứ. | Hồ sơ tranh chấp (`DISPUTE_OPENED`) |
| **MF4-06** | System & Đối tác Thanh toán | Hệ thống ghi nhận trạng thái tranh chấp. Nếu đối tác thanh toán hỗ trợ cơ chế giữ/tạm dừng theo hợp đồng tích hợp, hệ thống gửi yêu cầu tạm dừng giải ngân (`FROZEN_DISPUTED`). Nếu không hỗ trợ, xử lý theo cơ chế dispute/refund/settlement mà đối tác cung cấp. | Trạng thái thanh toán bị tạm giữ |
| **MF4-07** | Platform Operator | **Chủ trì Hòa giải Nội bộ theo Quy chế Sàn (Platform Terms)**: Tiếp nhận chứng cứ hai bên; đối chiếu SOW MF1, Mission Plan MF2, ảnh gốc MinIO và dữ liệu telemetry SHA-256. Trường hợp tranh chấp phức tạp về an toàn kết cấu, Operator có thể yêu cầu các bên cung cấp đánh giá kỹ thuật độc lập để hỗ trợ hòa giải. Platform không tự xác định trách nhiệm chuyên môn thay cho đơn vị giám định hoặc cơ quan có thẩm quyền. | Biên bản hòa giải / Kết quả xử lý nội bộ |
| **MF4-08** | Platform Operator & Đối tác Thanh toán | Thực hiện kết quả xử lý theo Quy chế Sàn và điều khoản hợp đồng: (1) yêu cầu Provider khắc phục/bay bổ sung nếu thuộc trách nhiệm Provider; (2) thực hiện hoàn tiền hoặc điều chỉnh thanh toán nếu có căn cứ và cơ chế thanh toán hỗ trợ; hoặc (3) đóng khiếu nại nếu không có căn cứ. Trường hợp không đạt được thỏa thuận, các bên giữ quyền sử dụng cơ chế giải quyết tranh chấp được quy định trong hợp đồng. Đối tác thanh toán thực hiện lệnh chuyển tiền căn cứ trên kết quả hòa giải đã được các bên chấp thuận. | Kết quả tranh chấp xử lý xong & Tài chính tất toán |

#### 2. Xử lý Ngoại lệ MF4
* **Một bên không đồng ý với kết quả hòa giải nội bộ của Sàn**: Kết quả xử lý của Sàn chỉ là cơ chế giải quyết nội bộ theo Quy chế tham gia sàn, không phải phán quyết tài phán. Các bên giữ nguyên quyền khởi kiện vụ việc ra Tòa án có thẩm quyền hoặc Trọng tài thương mại (VIAC) theo quy định pháp luật.

---

### MF5 — Xử lý Khuyết tật, Đơn hàng Bảo trì & Quản lý Bảo hành Hoàn công (Defect Rectification, Maintenance & Retention)

**Mục tiêu**: Chuyển giao các khuyết tật từ báo cáo kiểm định thành đơn hàng sửa chữa công trình, lập phương án kỹ thuật thi công, kiểm soát chi phí phát sinh qua Change Order, đối soát ảnh Before/After và quản lý bảo lãnh bảo hành.

**Tác nhân chính**: `Client`, `PROVIDER_MANAGER` (đơn vị có năng lực bảo trì), `Maintenance Engineer`, `Platform Operator`, `System`.

#### 1. Quy trình chi tiết (Main Sequence)

| Bước | Vai trò / Lane | Hoạt động chi tiết | Sản phẩm đầu ra |
| :--- | :--- | :--- | :--- |
| **MF5-01** | Client | Chọn các khuyết tật cần xử lý từ Báo cáo MF4 (ví dụ vết nứt bê tông dầm, rỉ sét lan can) để khởi tạo **Phiếu yêu cầu sửa chữa (Maintenance Ticket)**. | Maintenance Ticket |
| **MF5-02** | Provider Manager & Kỹ sư | **Lập Phương án Kỹ thuật Sửa chữa & Báo giá (Technical Assessment & Quotation)**: Kỹ sư bảo trì khảo sát thực tế và phân tích: (1) Phân loại khuyết tật (kết cấu hay bề mặt); (2) Đề xuất biện pháp xử lý (bơm keo epoxy áp lực, trám vữa polyme, cạo rỉ sơn chống ăn mòn); (3) Tiêu chuẩn vật tư sử dụng; (4) Dự toán nhân công và thời gian thi công. Lập Báo giá bảo trì chi tiết gửi Client. | Hồ sơ Phương án kỹ thuật & Báo giá bảo trì |
| **MF5-03** | System | Khởi tạo **Đơn dịch vụ bảo trì (Maintenance Work Order)**: Snapshot các tham số tỷ lệ bảo lãnh hoàn công $H$ (nếu áp dụng), thời hạn bảo hành $T_{war}$ và điều khoản hủy. Client nạp khoản tiền đảm bảo qua đối tác thanh toán. | Maintenance Order có hiệu lực |
| **MF5-04** | Maintenance Engineer | Tiếp nhận phân công thi công. Đến hiện trường thực hiện sửa chữa theo đúng phương án kỹ thuật đã duyệt. **Bắt buộc chụp và nạp tệp ảnh đối chứng Trước và Sau khi thi công (Before/After Evidence)** lên hệ thống MinIO kèm nhật ký vật tư và định vị cấu kiện. | Nhật ký thi công & Cặp ảnh đối chứng Before/After |
| **MF5-05** | Maintenance Engineer & Provider Manager | **Xử lý Phát sinh Hư hỏng Ngầm (Change Order Flow)**: Nếu trong quá trình đục phá phát hiện hư hỏng ngầm nghiêm trọng vượt quá dự toán ban đầu (cốt thép rỉ mục hoàn toàn): Kỹ sư dừng ngay phần việc phát sinh, chụp ảnh hiện trạng và lập **Yêu cầu Thay đổi (Change Order)**. Client thẩm định và phê duyệt phương án bổ sung chi phí trước khi tiếp tục thi công. | Change Order được phê duyệt & Cập nhật hợp đồng |
| **MF5-06** | Client & Provider Manager | **Nghiệm thu Hoàn công Kỹ thuật**: Client kiểm tra đối soát cặp ảnh Before/After và nhật ký vật tư trên ứng dụng. Nếu đạt chuẩn, Client ký Biên bản nghiệm thu hoàn công. | Biên bản nghiệm thu hoàn công |
| **MF5-07** | System & Đối tác Thanh toán | Căn cứ điều khoản snapshot: Đối tác thanh toán giải ngân phần tiền thi công đến hạn cho Provider theo hợp đồng; tạm giữ lại tỷ lệ bảo lãnh hoàn công $H$ (ví dụ 5%–10% giá trị gói sửa chữa) tại đối tác thanh toán nếu hợp đồng có áp dụng. Kích hoạt đồng hồ tính thời hạn bảo hành $T_{war}$. | Giải ngân đợt 1 & Kích hoạt thời hạn bảo hành |
| **MF5-08** | Client, Provider & Operator | Hết thời hạn bảo hành $T_{war}$, nếu công trình không phát sinh tái nứt/hư hỏng, hệ thống tự động gửi lệnh giải ngân nốt khoản bảo lãnh hoàn công $H$ cho Provider. Chính thức đóng hồ sơ Maintenance Ticket. | Giải ngân bảo hành $H$ & Đóng ticket hoàn tất |

#### 2. Nhánh Xử lý Rework / Re-inspection trong Bảo trì
* **Nghiệm thu Before/After không đạt chuẩn (Maintenance Rework Loop)**:
  - Nếu ảnh After cho thấy vết trám bị rỗ, màu sắc vật liệu không đạt hoặc vết nứt chưa được xử lý kín: Client bấm "Từ chối nghiệm thu" kèm hình ảnh yêu cầu sửa đổi.
  - Nếu lỗi thuộc trách nhiệm của Provider và nằm trong phạm vi công việc đã cam kết, Kỹ sư bảo trì thực hiện Rework mà không tính thêm chi phí; nếu phát sinh do thay đổi phạm vi hoặc nguyên nhân ngoài trách nhiệm Provider thì phải lập Change Request/Change Order trước khi thực hiện.
* **Yêu cầu kiểm tra lại bằng Drone (Post-repair Drone Re-inspection)**:
  - Với các công trình trên cao hoặc vị trí nguy hiểm, Client có thể tạo yêu cầu kiểm tra lại bằng drone theo một Inspection Request mới hoặc theo cơ chế Re-inspection đã quy định trong hợp đồng để bay chụp đối chứng chất lượng sửa chữa ở độ cao lớn.

---

## VI. Ma trận Phân quyền & Trách nhiệm (RACI Matrix v3.2)

| Quy trình / Nghiệp vụ cốt lõi | `PLATFORM_ADMIN` | `PLATFORM_OPERATOR` | `CLIENT` | `PROVIDER_MANAGER` | `INSPECTOR` | `MAINTENANCE_ENGINEER` |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **SF: Thẩm định Provider & Đăng ký Drone (NĐ 288)** | I | **A / R** | I | **R** | C | - |
| **SF: Khai báo Tài sản & Cảnh báo Cấm bay** | I | C | **A / R** | - | - | - |
| **Chính sách: Cấu hình Động Tham số Thương mại** | I | **A / R** | I | I | - | - |
| **MF1: Lọc Thông minh Eligible Providers & RFQ** | - | C | **A** | **R** | - | - |
| **MF1: Ký Hợp đồng & Nạp tiền Đảm bảo Thanh toán** | I | C | **A / R** | **R** | - | - |
| **MF2: Lập Kế hoạch Bay (GSD, Overlap, Shot List)** | - | - | I | **A** | **R** | - |
| **MF2: Hồ sơ Cấp phép Bay & Ký Cam kết An toàn** | I | C | I | **A / R** | **R (Pilot)** | - |
| **MF3: Khảo sát Hiện trường, Xử lý Sự cố & Re-flight** | - | - | I | I | **A / R** | - |
| **MF3: Nhận diện AI YOLO & Xác minh Kích thước Lỗi** | - | - | - | I | **A / R** | - |
| **MF3: Tự xác minh bản thảo LLM & Ký phát hành QA** | - | - | I | **A (Release)**| **R (Author)**| - |
| **MF4: Nghiệm thu Báo cáo & Lập Hóa đơn Điện tử** | I | C | **A / R** | **R (Invoice)**| - | - |
| **MF4: Hòa giải Tranh chấp & Thẩm định Độc lập** | I | **A / R** | C | C | C | - |
| **MF5: Phương án Kỹ thuật & Báo giá Bảo trì** | - | - | **A** | **R** | - | C |
| **MF5: Thi công Before/After & Change Order** | - | - | **A** | I | - | **A / R** |
| **MF5: Nghiệm thu Hoàn công, Rework & Tất toán $H$** | I | **R** | **A** | I | - | I |

*Ghi chú*:
* **R (Responsible)**: Người trực tiếp thực hiện công việc.
* **A (Accountable)**: Người chịu trách nhiệm phê duyệt cuối cùng và sở hữu kết quả.
* **C (Consulted)**: Người được tham vấn ý kiến, cung cấp dữ liệu đối soát kỹ thuật.
* **I (Informed)**: Người được nhận thông báo kết quả.
