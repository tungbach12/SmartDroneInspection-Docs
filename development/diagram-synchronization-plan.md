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

> **Cập nhật hiện tại**: Các nhóm **Package, ERD, State, Activity (5 tab `MF1A`/`MF1B`/`MF2`/`MF3`/`MF4`), Screen Flow (Web & Mobile), Class (9 tab `FE-01`–`FE-24`) và Sequence (26 tab `FE-01A`–`FE-24`)** đã được đồng bộ với mã nguồn thực tế (`main` + `V70`/`V71`) và kiểm tra 0 lỗi/0 cảnh báo; bước tiếp theo là `Deployment` và `Process` diagrams trước khi xuất ảnh PNG thay thế Mermaid.

### Nhóm A — Đã hoàn thành & đã review

| STT | File `.drawio` | Các tab con | Vị trí thay Mermaid trong Reports | Trạng thái |
| :---: | :--- | :--- | :--- | :--- |
| 1 | `diagrams/smartdrone-context-diagram.drawio` | `Context Diagram` | Report 3 §1 (`Product Overview`), Report 7 §III.1 | Đã xong & đã review |
| 2 | `diagrams/smartdrone-architecture-diagram.drawio` | `System Architecture` | Report 4 §1.1 (`System Architecture`), Report 7 §IV.1.1 | Đã xong & đã review |
| 3 | `diagrams/smartdrone-use-case-diagrams.drawio` | `UC-1 Auth & Public Access`, `UC-2 Assets, Drones & Onboarding`, `UC-3 Contracting & Field Execution`, `UC-4 AI, Reporting & Settlement`, `UC-5 Platform Administration` | Report 3 §2.2.1 (`Use Case Diagram`), Report 7 §III.2 | Đã xong & đã review (5 tab) |
| 4 | `diagrams/smartdrone-package-diagrams.drawio` | `Backend Package Diagram`, `Web Portal Package Diagram`, `Mobile App Package Diagram` | Report 4 §1.2.1–1.2.3 & Report 7 | Đã xong & đã merge (#129) |
| 5 | `diagrams/smartdrone-erd-diagrams.drawio` | `ERD - Conceptual (43 Entities)`, `ERD - Full System (38 Tables)`, `Physical ERD - V1-V69` | Report 3 §3.1.5, Report 4 §2, Report 7 | Đã xong & đã merge (#129) |
| 6 | `diagrams/smartdrone-state-diagrams.drawio` | `ServiceRequest`, `Occurrence`, `Inspection`, `FieldSession`, `InspectionReport` | Report 4 & Report 7 (`contracts`, `inspections`) | Đã xong & đã merge (#129) |
| 7 | `diagrams/smartdrone-activity-diagrams.drawio` | `MF1A - Customer Onboarding`, `MF1B - Partner & Drone`, `MF2 - Commercial & Dispatch`, `MF3 - Permit, Field & AI`, `MF4 - Report, Finance & Reinspection` | Report 3 / Report 4 / Report 7 (Mainflows `MF1`–`MF4`) | Đã xong & đã review (5 tab) |
| 8 | `diagrams/smartdrone-screen-flow-diagrams.drawio` | `Web Application Screen Flow`, `Mobile Application Screen Flow` | Report 3 §3.1.1 & Report 7 §III.3.1.1 | Đã xong & đã review (2 tab) |
| 9 | `diagrams/smartdrone-class-diagrams.drawio` | `FE-01`, `FE-02`, `FE-03`, `FE-09`, `FE-14`, `FE-16`, `FE-17`, `FE-18`, `FE-24` | Report 4 §3 & Report 7 | Đã xong & đã review (9 tab) |
| 10 | `diagrams/smartdrone-sequence-diagrams.drawio` | `FE-01A`, `FE-01B`, `FE-02`, `FE-03`, `FE-04`, `FE-05`, `FE-06`, `FE-07`, `FE-08`, `FE-09`, `FE-10`, `FE-11`, `FE-12`, `FE-13`, `FE-14A`, `FE-14B`, `FE-15`, `FE-16`, `FE-17`, `FE-18`, `FE-19`, `FE-20`, `FE-21`, `FE-22`, `FE-23`, `FE-24` | Report 4 §3 & Report 7 | Đã xong 26 tab (đủ `MF1`–`MF4`, gồm `V70`/`V71`) |

### Nhóm B — Lộ trình tiếp theo

| Thứ tự | File `.drawio` mục tiêu | Các tab cần làm / rà soát | Nguồn code đối chiếu & nơi thay thế trong Reports | Trạng thái |
| :---: | :--- | :--- | :--- | :--- |
| **1 (Next)** | `diagrams/smartdrone-deployment-diagram.drawio` | `Physical Deployment` | Đối chiếu `docker-compose.yml`, Nginx SPA container, Oracle Cloud VPS, MinIO, Postgres pgvector, AI Inference, SmartDroneHub | Chưa tạo file riêng |
| **2** | `diagrams/smartdrone-process-diagrams.drawio` | `Agile Scrum Process`, `End-to-End Operational Flow` | Rà sửa tab `Agile Scrum Process` + dựng luồng nghiệp vụ tổng thể thay Mermaid Report 1 §6.1 & Report 6 §3.1 | Mới có `Agile Scrum Process` |

---

## 3. Giai đoạn cuối — Xuất ảnh & Thay thế Mermaid hàng loạt trong Reports

Sau khi hoàn tất và duyệt hết các file `.drawio` ở Mục 2:

1. Xuất toàn bộ các tab `.drawio` ra ảnh PNG độ phân giải cao (qua draw.io CLI / Chrome renderer) lưu vào thư mục assets tương ứng của từng report.
2. Thay thế các block ```` ```mermaid ... ``` ```` cũ trong **Report 1, Report 2, Report 3, Report 4, Report 6, Report 7** bằng liên kết ảnh từ `.drawio` (đồng thời cập nhật đồng bộ `PayOS` → `Sepay VietQR` trong các đoạn văn/diagram ở Report 4 & Report 7).
3. Chạy bộ kiểm tra tài liệu (`git diff --check`, `python -I -m unittest discover -s tools/tests -p "test_*.py" -v`) và export lại Word/PDF một lần duy nhất.
