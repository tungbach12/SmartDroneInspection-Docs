---
title: "Diagram Synchronization & Mermaid Replacement Plan"
weight: 25
---

# Diagram Synchronization & Mermaid Replacement Plan

Kế hoạch đồng bộ toàn bộ hệ thống sơ đồ kỹ thuật trong [diagrams/](../diagrams/) theo mã nguồn thực tế (`main`) và thay thế các block Mermaid cũ trong **Reports 1–7** bằng ảnh xuất chuẩn từ các file `.drawio` tách theo từng loại (**1 diagram type = 1 `.drawio` file**).

## 1. Quy ước tổ chức & quy trình chuẩn hóa

- **Cấu trúc file**: Mỗi loại sơ đồ dùng đúng **1 file `.drawio`** riêng tại `SmartDroneInspection-docs/diagrams/`, bên trong chứa nhiều tab con cùng loại; bỏ các file/tab thừa (`feature tree`, `WF02` rỗng, `State - WorkOrder` và `WF-04 Activity` ngoài phạm vi release).
- **Quy chuẩn trình bày**:
  - Đồng bộ trực tiếp với code thực tế của 3 repo (`SmartDroneInspection-backend`, `SmartDroneInspection-frontend`, `SmartDroneInspection-mobile`): **4 vai trò** (`ADMIN`, `MANAGER`, `CUSTOMER`, `INSPECTOR`), thanh toán **Sepay VietQR + VNPay** (thay PayOS), **8 Spring Modulith packages** (`dashboard`, `notifications`, `infrastructure`, `contracts`, `inspections`, `assets`, `users`, `shared`), ứng dụng Mobile **Customer-only**, và hệ quản trị DB Flyway `pgvector`.
  - Không đặt khung tiêu đề (title/subtitle box) trên canvas `.drawio` (việc đánh số `Figure` do tài liệu report đảm nhiệm).
  - Phong cách UML mặc định trắng/đen (`#FFFFFF` / `#000000`), tách Use Case đơn lẻ (atomic), cụm kế thừa ≥ 3 nhánh dùng cây phân nhánh vuông góc 1 mũi tên tam giác rỗng.
- **Công cụ kiểm tra & xem nhanh**:
  - Chạy `node "C:/Users/trant/.gemini/skills/drawio-diagram-skill/scripts/drawio.mjs" check --verbose <file.drawio>` bảo đảm `0 errors`.
  - Mở xem trực tiếp bằng `drawio.mjs url <file.drawio>` trên `app.diagrams.net` hoặc VS Code (*Draw.io Integration*).

---

## 2. Trạng thái hiện tại & Lộ trình thực hiện lần lượt

> **Điểm bắt đầu tiếp theo: `Package Diagrams`** (`smartdrone-package-diagrams.drawio` đã được dựng từ code thực tế của Backend, Web Portal và Mobile App, **đang chờ review trước khi chuyển sang ERD**).

### Nhóm A — Đã hoàn thành & đã review

| STT | File `.drawio` | Các tab con | Vị trí thay Mermaid trong Reports | Trạng thái |
| :---: | :--- | :--- | :--- | :--- |
| 1 | `diagrams/smartdrone-context-diagram.drawio` | `Context Diagram` | Report 3 §1 (`Product Overview`), Report 7 §III.1 | Đã xong & đã review |
| 2 | `diagrams/smartdrone-architecture-diagram.drawio` | `System Architecture` | Report 4 §1.1 (`System Architecture`), Report 7 §IV.1.1 | Đã xong & đã review |
| 3 | `diagrams/smartdrone-use-case-diagrams.drawio` | `UC-1 Auth & Public Access`, `UC-2 Assets, Drones & Onboarding`, `UC-3 Contracting & Field Execution`, `UC-4 AI, Reporting & Settlement`, `UC-5 Platform Administration` | Report 3 §2.2.1 (`Use Case Diagram`), Report 7 §III.2 | Đã xong & đã review (5 tab) |

### Nhóm B — Lộ trình tiếp theo (bắt đầu từ Package Diagrams)

| Thứ tự | File `.drawio` mục tiêu | Các tab cần làm / rà soát | Nguồn code đối chiếu & nơi thay thế trong Reports | Trạng thái |
| :---: | :--- | :--- | :--- | :--- |
| **1 (Next)** | `diagrams/smartdrone-package-diagrams.drawio` | `Backend Package Diagram`, `Web Portal Package Diagram`, `Mobile App Package Diagram` | Đối chiếu `package-info.java` (8 modules) và import TS/Dart thực tế; bỏ `maintenance` & `workforce`; thay `PayOS` → `Sepay` ở Report 4 §1.2.1–1.2.3 & Report 7 | **Chờ review** *(đã vẽ xong bản local, mở sẵn tab Chrome)* |
| **2** | `diagrams/smartdrone-erd-diagrams.drawio` | `Main Entities ERD`, `Full ERD (Chen)`, `Database Schema ERD` *(rà gộp gọn)* | Đối chiếu JPA entities + Flyway migrations (`V1`–`V66`) trong backend; thay Mermaid ERD ở Report 3 §3.1.5, Report 4 §2, Report 7 §III.3.1.5 & §IV.2 | Chưa rà soát |
| **3** | `diagrams/smartdrone-state-diagrams.drawio` | `ServiceRequest`, `Occurrence`, `Inspection`, `FieldSession`, `InspectionReport` *(bỏ `WorkOrder`)* | Kéo từ tab Drive/source và đối chiếu enum trạng thái + service transitions trong `contracts` & `inspections` | Chưa tạo file riêng |
| **4** | `diagrams/smartdrone-activity-diagrams.drawio` | `WF-01 Activity`, `WF-02 Activity`, `WF-03 Activity` *(bỏ `WF-04`)* | Rà sửa role/PayOS → Sepay VietQR, timeout, field abort & report workflow khớp backend | Đã tách file, chưa rà nội dung |
| **5** | `diagrams/smartdrone-screen-flow-diagrams.drawio` | `Web Screen Flow`, `Mobile Screen Flow` | Đối chiếu `router.tsx` + `accessPolicy.ts` (Web) và `app_router.dart` (Mobile Customer-only); thay Mermaid ở Report 3 §3.1.1 & Report 7 §III.3.1.1 | Chưa tạo file riêng |
| **6** | `diagrams/smartdrone-deployment-diagram.drawio` | `Physical Deployment` | Đối chiếu `docker-compose.yml`, Nginx SPA container, Oracle Cloud VPS, MinIO, Postgres pgvector, AI Inference, SmartDroneHub | Chưa tạo file riêng |
| **7** | `diagrams/smartdrone-process-diagrams.drawio` | `Agile Scrum Process`, `End-to-End Operational Flow` | Rà sửa tab `Agile Scrum Process` + dựng luồng nghiệp vụ tổng thể thay Mermaid Report 1 §6.1 & Report 6 §3.1 | Mới có `Agile Scrum Process` |
| **8** | `diagrams/smartdrone-class-diagrams.drawio` | Các tab Class Diagram cốt lõi (`FE-01`–`FE-24`) | Rà `bách-fe05-class`, `bách-fe06-class`, kéo/bổ sung các Class Diagram còn lại từ source & Drive khớp Report 4 §3 & Report 7 | Mới gộp 2 tab |
| **9** | `diagrams/smartdrone-sequence-diagrams.drawio` | Các tab Sequence Diagram cốt lõi (`FE-01`–`FE-24`) | Rà `bách-fe05-seq`, `bách-fe06-seq` (chuyển PayOS → Sepay, rà endpoint/method thực tế), bổ sung các tab còn lại khớp Report 4 §3 & Report 7 | Mới gộp 2 tab |

---

## 3. Giai đoạn cuối — Xuất ảnh & Thay thế Mermaid hàng loạt trong Reports

Sau khi hoàn tất và duyệt hết các file `.drawio` ở Mục 2:

1. Xuất toàn bộ các tab `.drawio` ra ảnh PNG độ phân giải cao (qua draw.io CLI / Chrome renderer) lưu vào thư mục assets tương ứng của từng report.
2. Thay thế các block ```` ```mermaid ... ``` ```` cũ trong **Report 1, Report 2, Report 3, Report 4, Report 6, Report 7** bằng liên kết ảnh từ `.drawio` (đồng thời cập nhật đồng bộ `PayOS` → `Sepay VietQR` trong các đoạn văn/diagram ở Report 4 & Report 7).
3. Chạy bộ kiểm tra tài liệu (`git diff --check`, `python -I -m unittest discover -s tools/tests -p "test_*.py" -v`) và export lại Word/PDF một lần duy nhất.
