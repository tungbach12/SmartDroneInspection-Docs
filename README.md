# SmartDroneInspection Documentation (`SmartDroneInspection-docs`)

Kho lưu trữ tài liệu chính thức (single source of truth) của đồ án tốt nghiệp **SmartDroneInspection: AI-powered Infrastructure Inspection Management Platform** (Mã đề tài: `GFA26SE139` · Nhóm: `FA26SE112`).

Toàn bộ báo cáo chính thức (`Reports 1–7`), nhật ký theo dõi dự án, báo cáo tuần, hồ sơ Review 2, phiếu tự đánh giá và hệ thống sơ đồ kỹ thuật được viết dưới dạng **Markdown** và **XML `.drawio`** có kiểm soát phiên bản, sau đó xuất sang đúng bộ template Word/Excel của trường bằng toolchain Python trong `tools/`.

---

## Mục lục

1. [Phạm vi hệ thống & cấu trúc kho tài liệu](#1-phạm-vi-hệ-thống--cấu-trúc-kho-tài-liệu)
2. [Cách sử dụng repo & quy trình cập nhật tài liệu](#2-cách-sử-dụng-repo--quy-trình-cập-nhật-tài-liệu)
3. [Skill đính kèm draw.io & cách chỉnh sửa `.drawio` local](#3-skill-đính-kèm-drawio--cách-chỉnh-sửa-drawio-local)
4. [Công cụ export báo cáo (`tools/`) & kiểm tra chất lượng](#4-công-cụ-export-báo-cáo-tools--kiểm-tra-chất-lượng)
5. [Cách viết, Target Reader & Giọng văn cho từng Report](#5-cách-viết-target-reader--giọng-văn-cho-từng-report)

---

## 1. Phạm vi hệ thống & cấu trúc kho tài liệu

### 1.1 Đường cơ sở sản phẩm hiện hành

Mọi tài liệu, sơ đồ và ảnh minh họa mới phải phản ánh đúng mã nguồn đang chạy trên nhánh `main` của các repo code:

- **4 vai trò đăng nhập (không có vai trò thứ 5):** `ADMIN`, `MANAGER`, `CUSTOMER`, `INSPECTOR` (sở hữu tài sản gắn trực tiếp với `CUSTOMER`; không có thực thể tổ chức phân cấp hay `MAINTENANCE_ENGINEER`).
- **4 actor tự động (không đăng nhập):** `SYSTEM`, `YOLO11`, `LLM`, `DroneKnowledgeAI` (chỉ mang tính gợi ý/hỗ trợ, mọi quyết định chính thức đều do con người xác nhận).
- **4 luồng chính (`MF1`–`MF4`) và 24 tính năng nguyên tử (`FE-01`–`FE-24`):**
  - `MF1` (`FE-01`–`FE-04`): Xác thực & phân quyền 4 vai trò, tuyển chọn Partner Inspector, đăng ký Drone sở hữu cá nhân, sàng lọc vùng cấm bay trên bản đồ Việt Nam.
  - `MF2` (`FE-06`–`FE-12`): Quản lý công trình tòa nhà & điểm kiểm tra, duyệt vùng bay hạn chế (`ADMIN`), yêu cầu dịch vụ (đơn lẻ/định kỳ) & báo giá VND, hợp đồng giấy & điều phối lịch, chat hai kênh, timeout nhận việc & thông báo hệ thống.
  - `MF3` (`FE-13`–`FE-17`): Cổng nộp giấy phép bay, phiên thực địa & telemetry `SmartDroneHub`, thu nhận ảnh & video MP4 dung lượng lớn, phát hiện lỗi `YOLO11` + Vision fallback & chốt findings, gợi ý `DroneKnowledgeAI` (`pgvector`) & soạn ghi chú/tóm tắt bằng AI.
  - `MF4` (`FE-05`, `FE-18`–`FE-24`): Biên tập/duyệt/xuất bản báo cáo kiểm tra, nghiệm thu & yêu cầu làm rõ của khách hàng, thanh toán trực tuyến `Sepay VietQR` & `VNPay`, hạn thanh toán & chứng từ PDF, chi trả đối tác (`ELIGIBLE -> PAID`), hoàn tiền & thu hồi công nợ, kiểm tra lại sau khắc phục (`RE_INSPECTION`) và sổ cái tài chính theo vai trò.
- **Ranh giới loại trừ bắt buộc:** Chỉ hỗ trợ **công trình tòa nhà** (`buildings`); **không** điều khiển bay/autopilot trực tiếp; **không** bao gồm phân hệ thi công bảo trì khắc phục (`corrective maintenance`); **không** dựng mô hình 3D photogrammetry; ứng dụng Mobile (`Flutter`) chỉ phục vụ vai trò **`CUSTOMER`**.

### 1.2 Hệ sinh thái các repository anh em

Tool export và tài liệu tham chiếu mặc định các thư mục được clone **song song** cùng cấp trong thư mục cha (ví dụ `E:/Dev/Repos/Capstone/`):

| Thư mục | Stack & vai trò |
| --- | --- |
| `SmartDroneInspection-backend/` | Java 21, Spring Boot 4.1, Spring Modulith, PostgreSQL 17 (`pgvector`), MinIO, tích hợp YOLO11/LLM/SmartDroneHub/Sepay/VNPay |
| `SmartDroneInspection-frontend/` | React 19, TypeScript, Vite, Material UI — 4 cổng web (`/admin`, `/manager`, `/client`, `/operations`) |
| `SmartDroneInspection-mobile/` | Flutter, Dart, Riverpod, GoRouter, Dio — ứng dụng Mobile **chỉ dành cho `CUSTOMER`** |
| `SmartDroneInspection-docs/` | Markdown, `.drawio`, `.mmd`, Python OOXML exporter — kho tài liệu này |
| `capstone-official-docs/` | Thư mục chứa template `.docx`/`.xlsx` gốc của trường (**chỉ đọc**, không chỉnh sửa trực tiếp) |

### 1.3 Cấu trúc thư mục trong `SmartDroneInspection-docs`

```text
SmartDroneInspection-docs/
├── _index.md                       # Bản đồ điều hướng Hugo cho toàn bộ tài liệu
├── README.md                       # Hướng dẫn sử dụng repo, draw.io, export & chuẩn viết report
├── hugo.toml                       # Cấu hình trang tài liệu Hugo
├── development/                    # Quy trình Git/PR, kế hoạch đồng bộ sơ đồ, pending log, review phân quyền
├── diagrams/                       # Sơ đồ nguồn .drawio (1 loại = 1 file), DBML, ERD HTML & Mermaid .mmd
├── project-reference/              # Cẩm nang tránh lỗi Capstone, baseline hiện thực, guideline mainflows
├── reports/                        # Nguồn Markdown cho từng report + thư mục generated/ (gitignored)
│   ├── report-1-project-introduction/
│   ├── report-2-project-management-plan/
│   ├── report-3-software-requirement-specification/
│   ├── report-4-software-design-document/
│   ├── report-5-test-documentation/
│   ├── report-5-test-report/       # Nguồn cho Report5_Test Report.xlsx (Cover, Index, Stats, fe-01..fe-24)
│   ├── report-6-software-user-guides/
│   ├── report-7-final-project-report/
│   ├── project-tracking/           # Nguồn cho Report3_Project Tracking.xlsx
│   ├── weekly-project-reports/     # Nguồn week-01.md .. week-07.md + tasks-import.csv
│   ├── review-2-registration/      # Registration Form v2.0 & BM03
│   ├── review-2-design-brief/      # BM01 Design Brief, Appendix A & BM04
│   ├── review-2-self-review/       # BM02 SRS/SDD Self-Review
│   ├── final-self-evaluation/      # Phiếu tự đánh giá nộp cuối kỳ (tiếng Việt)
│   └── generated/                  # Đầu ra .docx/.xlsx/PDF (bị Git ignore trừ review-2-pack/)
├── tools/                          # Bộ exporter Python OOXML, script kiểm tra Office & unit tests
└── .claude/skills/capstone-report-export/  # Skill hướng dẫn export, chụp screenshot & scripts/check_output.py
```

### 1.4 Liên kết nhanh

- [Bản đồ tài liệu (`_index.md`)](_index.md)
- [Hướng dẫn tránh lỗi Capstone (`project-reference/error-prevention.md`)](project-reference/error-prevention.md)
- [Quy trình Git & Pull Request (`development/git-and-pull-requests.md`)](development/git-and-pull-requests.md)
- [Kế hoạch đồng bộ sơ đồ (`development/diagram-synchronization-plan.md`)](development/diagram-synchronization-plan.md)
- [Nhật ký thay đổi chờ gộp (`development/pending-docs-updates.md`)](development/pending-docs-updates.md)
- [Hướng dẫn chi tiết bộ tool export (`tools/README.md`)](tools/README.md)
- [Cấu trúc template Report 5 (`reports/report-5-test-report/template-layout.md`)](reports/report-5-test-report/template-layout.md)

---

## 2. Cách sử dụng repo & quy trình cập nhật tài liệu

### 2.1 Nguyên tắc làm việc cốt lõi

1. **Không làm việc và không commit trực tiếp trên `main`.** Luôn kiểm tra trạng thái và tạo nhánh riêng theo quy ước `<type>/<scope>-<short-description>` (ví dụ `docs/srs-sync-fe13`, `fix/report5-totals`):
   ```powershell
   git -C SmartDroneInspection-docs status --short
   git -C SmartDroneInspection-docs checkout -b docs/my-task
   ```
2. **Giữ nguyên các thay đổi chưa liên quan** đang có trong worktree; khi commit chỉ `git add` đích danh file mình sửa theo chuẩn Conventional Commits (`docs(srs): ...`, `fix(tools): ...`).
3. **Kiểm chứng từ code thật trước khi viết.** Khi tài liệu cũ và mã nguồn khác nhau, phải đọc controller/service/migration/UI thực tế ở backend, frontend, mobile trước rồi mới cập nhật tài liệu — không chép lại prose lỗi thời.
4. **Gom batch khi code đang biến động nhanh.** Trong lúc sửa code liên tục qua nhiều lượt, ghi nhận thay đổi vào [nhật ký chờ (`development/pending-docs-updates.md`)](development/pending-docs-updates.md), sau đó cập nhật đồng loạt vào Reports và `.drawio` trong một lượt thống nhất để tránh lệch giữa các chương.
5. **Không commit file sinh tự động.** Thư mục `reports/generated/`, file tạm Office `~$*.docx`, `__pycache__/` đã được liệt kê trong `.gitignore`.

### 2.2 Quy trình cập nhật chuẩn từ đầu đến cuối

1. **Xác định tài liệu bị ảnh hưởng:** Nếu thay đổi nghiệp vụ, vai trò, API, DB hoặc kiểm thử, kiểm tra xem cần cập nhật những file nào trong `Report 3`, `Report 4`, `Report 5`, `Report 6`, `Report 7` và `diagrams/*.drawio`.
2. **Chỉnh sửa theo đúng thứ tự:**
   - Cập nhật file `.drawio` trước và chạy `check --verbose` cho đến khi sạch lỗi.
   - Chụp lại ảnh màn hình thật (nếu giao diện thay đổi đáng kể) hoặc xuất ảnh sơ đồ vào thư mục `assets/` của từng report liên quan.
   - Cập nhật Markdown trong `reports/` kèm một dòng mới trong `00-record-of-changes.md` (hoặc mục `Record of Changes` đầu file).
3. **Chạy kiểm tra trước khi commit/export:**
   ```powershell
   git diff --check
   python -I -m unittest discover -s tools/tests -p "test_*.py" -v
   ```
4. **Xuất file nộp & kiểm tra hiển thị:** Chạy `export_all.py` (hoặc exporter của report tương ứng), kiểm tra bằng `check_output.py` và `verify_office_reports.ps1`, mở PDF/Word đọc lướt bảng biểu trước khi chốt nộp.

### 2.3 Chụp ảnh màn hình giao diện cho Report 3, 5, 6, 7

- Các báo cáo nhúng ảnh màn hình thật của ứng dụng đang chạy ở độ phân giải thống nhất **`1600×1000` (PNG)**, lưu trong `reports/report-<n>/assets/screens/`.
- Tham khảo hướng dẫn đầy đủ bằng `agent-browser` tại [.claude/skills/capstone-report-export/SKILL.md](.claude/skills/capstone-report-export/SKILL.md).
- Quy ước đặt tên file: `{portal}-{screen}.png` (hoặc `{portal}-ws-{tab}.png` cho các tab trong inspection workspace, ví dụ `inspector-ws-permit.png`, `manager-ws-review.png`).
- **Lưu ý quan trọng:** Bốn report dùng chung bộ screenshot (`Report 3`, `Report 5`, `Report 6`, `Report 7`) đều giữ bản copy riêng trong `assets/screens/` của chính folder đó. Nếu thêm hoặc thay ảnh mới, phải chép vào đủ các folder report có tham chiếu ảnh đó; exporter sẽ dừng và báo lỗi nếu thiếu file hoặc sai định dạng PNG.

---

## 3. Skill đính kèm draw.io & cách chỉnh sửa `.drawio` local

### 3.1 Giới thiệu skill `drawio-diagram-skill`

Repo sử dụng chuẩn của skill **`drawio-diagram-skill`** (đặt tại máy cục bộ ở `C:/Users/trant/.gemini/skills/drawio-diagram-skill/`):

- Tài liệu hướng dẫn skill: `C:/Users/trant/.gemini/skills/drawio-diagram-skill/SKILL.md`
- Script CLI đi kèm: `C:/Users/trant/.gemini/skills/drawio-diagram-skill/scripts/drawio.mjs` (chạy bằng **Node.js**, không cần cài thư viện ngoài).

> **Mẹo dùng cho thành viên mới / máy khác:** Nếu bạn không dùng Antigravity CLI hoặc chạy trên máy chưa cài skill ở `C:/Users/<user>/.gemini/skills/drawio-diagram-skill/`, chỉ cần copy thư mục `drawio-diagram-skill/` về máy mình hoặc gọi trực tiếp `node "<path-to>/drawio.mjs" ...`. Đối với thao tác sửa tay trực quan, bạn cũng có thể dùng extension **Draw.io Integration** trong VS Code hoặc ứng dụng **draw.io Desktop** mở thẳng các file `.drawio` trong `diagrams/`.

### 3.2 Danh sách file `.drawio` trong `diagrams/` (1 loại sơ đồ = 1 file nhiều tab)

Mỗi loại sơ đồ gom các biến thể/tính năng thành nhiều tab `<diagram>` trong **cùng 1 file `.drawio`** (tránh tách lẻ hàng chục file rời rạc):

| File `.drawio` | Số tab | Nội dung các tab | Dùng chính cho Report |
| --- | :---: | --- | --- |
| `diagrams/smartdrone-context-diagram.drawio` | 1 | `Context Diagram` | Report 3 §1, Report 7 §III.1 |
| `diagrams/smartdrone-architecture-diagram.drawio` | 1 | `System Architecture` | Report 4 §1.1, Report 7 §IV.1.1 |
| `diagrams/smartdrone-use-case-diagrams.drawio` | 5 | `UC-1` .. `UC-5` theo cụm nghiệp vụ | Report 3 §2.2, Report 7 §III.2 |
| `diagrams/smartdrone-package-diagrams.drawio` | 3 | `Backend`, `Web Portal`, `Mobile App` | Report 4 §1.2, Report 7 §IV.1.2 |
| `diagrams/smartdrone-erd-diagrams.drawio` | 6 | `Conceptual Overview (Chen)` + `Logical 1`..`5` | Report 3 §3.1.5, Report 4 §2, Report 7 |
| `diagrams/smartdrone-state-diagrams.drawio` | 7 | `ServiceRequest`, `Occurrence`, `Inspection`, `FieldSession`, `InspectionReport`, `ServicePayment`, `InspectorPayout` | Report 4 §2/3, Report 7 §IV |
| `diagrams/smartdrone-activity-diagrams.drawio` | 5 | `MF1A`, `MF1B`, `MF2`, `MF3`, `MF4` | Report 3, Report 4, Report 7 |
| `diagrams/smartdrone-screen-flow-diagrams.drawio` | 2 | `Web Application Screen Flow`, `Mobile Application Screen Flow` | Report 3 §3.1.1, Report 7 §III.3.1.1 |
| `diagrams/smartdrone-class-diagrams.drawio` | 9 | `FE-01`, `FE-02`, `FE-03`, `FE-09`, `FE-14`, `FE-16`, `FE-17`, `FE-18`, `FE-24` | Report 4 §3, Report 7 §IV.3 |
| `diagrams/smartdrone-sequence-diagrams.drawio` | 26 | `FE-01A` .. `FE-24` đủ `MF1`–`MF4` | Report 4 §3, Report 7 §IV.3 |
| `diagrams/smartdrone-process-diagrams.drawio` | 1 | `Agile Scrum Process` | Report 2 §2.1, Report 7 §II.2.1 |

*(Xem thêm tiến độ đồng bộ và thay thế Mermaid bằng ảnh PNG xuất từ `.drawio` trong [development/diagram-synchronization-plan.md](development/diagram-synchronization-plan.md).)*

### 3.3 Các lệnh CLI của `drawio.mjs` để kiểm tra & mở edit local

Đặt biến đường dẫn cho gọn trong PowerShell rồi chạy từ gốc `SmartDroneInspection-docs`:

```powershell
$DRAWIO = "C:/Users/trant/.gemini/skills/drawio-diagram-skill/scripts/drawio.mjs"

# 1. Xem danh sách tab, ID, số cell/vertex/edge và kích thước canvas
node $DRAWIO info diagrams/smartdrone-sequence-diagrams.drawio

# 2. Kiểm tra lỗi XML, thiếu parent/source/target, vertex đè nhau & cạnh cắt ngang vertex
node $DRAWIO check diagrams/smartdrone-sequence-diagrams.drawio --verbose

# 3. Trích xuất XML thuần (<mxGraphModel>) của đúng 1 tab theo tên, ID hoặc số thứ tự
node $DRAWIO extract diagrams/smartdrone-use-case-diagrams.drawio --page "UC-3 Contracting & Field Execution"

# 4. Mở file local trực tiếp trong app.diagrams.net trên trình duyệt mặc định
#    (tạo HTTP redirect 1-shot tại 127.0.0.1:41999/open, tự tắt ngay sau khi mở)
node $DRAWIO open diagrams/smartdrone-activity-diagrams.drawio

# Chỉ in URL localhost để tự mở hoặc truyền sang công cụ trình duyệt (không tự bật OS browser)
node $DRAWIO open diagrams/smartdrone-activity-diagrams.drawio --no-launch --port 41999

# 5. Sinh trực tiếp URL https://app.diagrams.net/...#R... chứa đủ mọi tab
node $DRAWIO url diagrams/smartdrone-context-diagram.drawio

# 6. Nén lại XML thành chuỗi base64 (khi cần làm việc với <diagram> dạng nén)
node $DRAWIO pack path/to/model.xml
```

### 3.4 Quy trình & quy chuẩn edit `.drawio` local

1. **File local là nguồn chân lý duy nhất.** Dùng định dạng XML `<mxfile>` chứa `<mxGraphModel>` không nén để dễ đọc diff trên Git. **Không** sửa tay chuỗi base64 nén, **không** tạo file `preview.html` bọc `viewer-static.min.js`, **không** tự ý copy-paste chuỗi `#R...` dài vào tool trình duyệt, và **không** lưu đè lên Google Drive trừ khi có yêu cầu.
2. **Sửa an toàn trên file nhiều tab:** Luôn định vị tab bằng `name` hoặc `id` (tránh phụ thuộc chỉ số thứ tự), giữ nguyên `id="0"`, `id="1"`, chuỗi `parent`, và giữ các tab không sửa **giống hệt từng byte**. Khi thêm hoặc xóa tab, cập nhật lại thuộc tính `pages="N"` trên thẻ `<mxfile>`.
3. **Escape XML chặt chẽ:** Mọi ký tự đặc biệt trong thuộc tính `value="..."` phải escape đúng (`&amp;`, `&lt;`, `&gt;`, `&quot;`); với `html=1` thì thẻ xuống dòng/in đậm viết là `&lt;br&gt;`, `&lt;b&gt;`.
4. **Quy chuẩn hình thức UML thống nhất:**
   - **Không đặt khung tiêu đề/subtitle trên canvas** (`SmartDroneInspection - ... Diagram`): việc đánh số `Figure` do tiêu đề dưới hình trong report đảm nhiệm.
   - **Màu mặc định trắng/đen:** Nền `#FFFFFF`, viền `#000000`, `strokeWidth=1`, `fontColor=#000000`, font `Helvetica`.
   - **Activity Diagram:** Dùng container `swimlane` dọc đặt sát nhau (`startSize=34;fillColor=#EEEEEE;swimlaneFillColor=#FFFFFF;strokeColor=#000000;strokeWidth=1;fontStyle=1;`), viền liền nét 1px, nhãn điều kiện không dùng ngoặc vuông (`Yes`, `No`, `Publish`, `Return`), không chèn mã `(FE-xx)` gây rối mắt trong ô hành động.
   - **Use Case Diagram:** Mỗi Use Case là một mục tiêu nguyên tử (`Động từ + Đối tượng`), chia nhiều tab (`~10–14` oval/tab) thay vì nhồi nhét. Nếu có từ 3 nhánh kế thừa trở lên trỏ vào cùng Use Case/Class cha, gom nhánh ngang vào một trục dọc (`2×2` junction) và nối **1 mũi tên tam giác rỗng** (`endArrow=block;endFill=0;`) vào cha.
   - **Đường nối sạch sẽ:** Ghi rõ `exitX`, `exitY`, `entryX`, `entryY` trên cạnh `edgeStyle=none` và chạy `drawio.mjs check --verbose` để xử lý hết `ERROR` và các cảnh báo `overlap` / `crosses vertex`.
5. **Mở xem trực quan & lưu lại:** Nếu chỉnh sửa XML bằng script/editor, chạy `drawio.mjs open <file.drawio>` để kiểm tra trực quan từng tab trên `app.diagrams.net`. Nếu chỉnh sửa trực tiếp trên `app.diagrams.net` hoặc VS Code *Draw.io Integration*, lưu lại về đúng file `.drawio` local rồi chạy `drawio.mjs check --verbose` trước khi commit.

---

## 4. Công cụ export báo cáo (`tools/`) & kiểm tra chất lượng

### 4.1 Điều kiện chạy & nguyên tắc hoạt động

- **Môi trường:** Python **3.10+** (chỉ dùng thư viện chuẩn, **không** cần cài thêm gói `pip`). Để chạy `verify_office_reports.ps1`, cần Windows đã cài Microsoft Word và Excel.
- **Template nguồn:** Thư mục `../capstone-official-docs/` chứa các file `.docx`/`.xlsx` mẫu của trường (**tuyệt đối chỉ đọc**). Các file `.docx` cũ nằm rải rác nếu có trong `reports/` không phải template chuẩn.
- **Cam kết bảo toàn định dạng (Fidelity contract):**
  - Exporter sao chép nguyên vẹn gói ZIP OOXML của template gốc và chỉ thay đổi phần XML nội dung (`word/document.xml`, dữ liệu sheet Excel...). Toàn bộ style, numbering, theme, font, header/footer, margin, thiết lập trang in và các phần ZIP không liên quan được giữ **byte-for-byte**.
  - **Không bao giờ ghi đè thư mục output đã tồn tại** (tránh làm hỏng file đang mở chỉnh sửa tay). Luôn sinh một thư mục mới dưới `reports/generated/<run>/` kèm `manifest.json` lưu mã băm SHA-256 của đầu vào/đầu ra và danh sách cảnh báo.
  - Ngắt trang và chiều cao dòng có thể thay đổi theo độ dài nội dung mới; cần kiểm tra lại bản PDF/Word trước khi nộp.

### 4.2 Danh sách exporter & lệnh chạy

Chạy các lệnh sau từ thư mục gốc `SmartDroneInspection-docs`:

```powershell
# Liệt kê tất cả key exporter và trạng thái nguồn
python -I tools/export_all.py --list

# Xuất toàn bộ các report có nguồn vào thư mục tự đặt tên theo timestamp
python -I tools/export_all.py

# Xuất vào thư mục chỉ định (thư mục chưa được tồn tại trước đó)
python -I tools/export_all.py --output reports/generated/final-check

# Chỉ xuất một hoặc vài report cụ thể
python -I tools/export_all.py --only report1 report3 report4 report5 report7 --output reports/generated/selected-run

# Chỉ định đường dẫn thư mục template khác mặc định (../capstone-official-docs)
python -I tools/export_all.py --templates "E:/Dev/Repos/Capstone/capstone-official-docs" --output reports/generated/my-preview
```

Hoặc chạy lẻ từng exporter (tự xuất vào `reports/generated/<timestamp>-<key>/` nếu không truyền `--output`):

| Lệnh | Artifact đầu ra | Nguồn Markdown |
| --- | --- | --- |
| `python -I tools/export_report1.py` | `Report1_Project Introduction.docx` | `reports/report-1-project-introduction/report1-project-introduction.md` |
| `python -I tools/export_report2.py` | `Report2_Project Management Plan.docx` | `reports/report-2-project-management-plan/report2-project-management-plan.md` |
| `python -I tools/export_report3.py` | `Report3_Software Requirement Specification.docx` | 6 file `00`–`05` trong `reports/report-3-software-requirement-specification/` |
| `python -I tools/export_report4.py` | `Report4_Software Design Document.docx` | 4 file `00`–`03` trong `reports/report-4-software-design-document/` |
| `python -I tools/export_report5_doc.py` | `Report5_Test Documentation.docx` | 2 file `00`–`01` trong `reports/report-5-test-documentation/` |
| `python -I tools/export_report5.py` | `Report5_Test Report.xlsx` (clone đủ 24 sheet `Feature 1`–`Feature 24`) | `reports/report-5-test-report/` (`00-cover`, `01-test-cases`, `02-test-statistics`, `fe-01`..`fe-24`) |
| `python -I tools/export_report6.py` | `Report6_Software User Guides.docx` | 2 file `00`–`01` trong `reports/report-6-software-user-guides/` |
| `python -I tools/export_report7.py` | `Report7_Final Project Report.docx` | 7 file `00`–`06` trong `reports/report-7-final-project-report/` |
| `python -I tools/export_project_tracking.py` | `Report3_Project Tracking.xlsx` | `reports/project-tracking/project-tracking.md` (4 bảng: WBS, Issues, Defects, Q&A) |
| `python -I tools/export_weekly.py [--week week-05]` | `Project Weekly Report_<group>_week-XX.xlsx` | `reports/weekly-project-reports/week-*.md` |

> **Lưu ý:** Khi chạy `export_all.py`, dòng `report5-unit: missing_source` là bình thường vì template `Report5_Unit Test.xls` không có nguồn Markdown trong repo.

**Các công cụ phụ trợ khác trong `tools/`:**

- `tools/render_mermaid.py`: trích các block `mermaid` trong `reports/` ra `diagrams/mermaid/*.mmd` và (khi truyền cờ render) xuất PNG vào `assets/mermaid/` của từng report.
- `tools/apply_role_wording.py`: rà soát/chuẩn hóa văn phong gọi tên vai trò trong văn xuôi Report 3 (mặc định dry-run; truyền `--apply` để ghi).
- `tools/export_review2_pack.py`, `tools/export_registration.py`, `tools/populate_review2_bms_docx.py`: bộ script phục vụ gói nộp Review 2 (`BM01`–`BM04`) và Registration Form.
- `tools/build_pdf_html.py`: script tạo HTML/PDF cho gói Review 2 cũ (lưu ý danh sách file `fe-01`..`fe-08` trong script này thuộc cấu trúc cũ trước đợt tách 24 FE).

### 4.3 Bộ 3 bước kiểm tra sau khi export

```powershell
# Bước 1: Chạy bộ unit test của exporter & kiểm tra git whitespace (nếu vừa sửa code/Markdown)
python -I -m unittest discover -s tools/tests -p "test_*.py" -v
git diff --check

# Bước 2: Kiểm tra nhanh cấu trúc gói .docx/.xlsx vừa xuất (không cần mở Word)
# Phát hiện: lọt ký tự ` hoặc |, bảng lệch số cột, bảng đánh số bị nhảy cóc dòng, thụt lề âm, cột quá hẹp
python -I .claude/skills/capstone-report-export/scripts/check_output.py reports/generated/final-check

# Bước 3: Mở kiểm chứng thật bằng Microsoft Word & Excel COM (Windows)
# Mở read-only, cập nhật TOC trong bộ nhớ, tính lại toàn bộ công thức Excel, kiểm tra chéo tổng Report 5
./tools/verify_office_reports.ps1 -OutputDirectory reports/generated/final-check
# Tùy chọn thêm -ExportPdf để xuất PDF preview (lưu tại reports/generated/final-check/pdf-previews/):
./tools/verify_office_reports.ps1 -OutputDirectory reports/generated/final-check -ExportPdf
```

### 4.4 Lưu ý cú pháp Markdown để exporter không bị lỗi

- **Bảng Markdown:** Mọi hàng trong cùng một bảng phải có **đúng số cột** như hàng header; không dùng pipe `|` trần trong nội dung ô mà không escape; giữ `test_readability.py` luôn pass.
- **Danh sách gạch đầu dòng (`- `):** Không cần hack khoảng trắng; `report_ooxml.py` chuyển `- ` thành `ListParagraph` chuẩn của Word với đúng 1 `numPr`.
- **Hình ảnh nhúng:** Cú pháp `![Mô tả ngắn](assets/.../ten-file.png)` phải trỏ tới **file PNG thật**. Nếu file bị thiếu hoặc không phải PNG, exporter sẽ ném lỗi và dừng ngay thay vì xuất ra hình trắng.
- **Chú thích hình & bảng:** Theo quy chuẩn Capstone (`project-reference/error-prevention.md`), **tên Figure đặt bên dưới hình**, **tên Table đặt bên trên bảng**, và mọi hình/bảng quan trọng đều phải được nhắc tới trong văn xuôi.
- **Cover & TOC:** Không xóa bảng Cover/TOC của template gốc; Report 1, 2, 7 exporter tự cắt phần header trước `Record of Changes` trong Markdown để ghép vào phần vỏ bìa + mục lục sẵn có của template trường.

---

## 5. Cách viết, Target Reader & Giọng văn cho từng Report

### 5.1 Phân tầng độ sâu kỹ thuật & quy ước chung

**Nguyên tắc phân tầng độ sâu giữa các report:**

- **Nhóm không đi quá sâu về kỹ thuật (`Reports 1, 2, 3, 5, 6`):** Tập trung vào bài toán nghiệp vụ, quản lý dự án, đặc tả hành vi người dùng/hệ thống có thể kiểm chứng, bằng chứng kiểm thử và thao tác sử dụng. **Tránh** đưa chi tiết cài đặt nội bộ (tên class/method Java, hook React, tên cột/bảng SQL chi tiết, cấu trúc package hay cơ chế kỹ thuật tầng thấp) vào văn xuôi của nhóm này — phần đó thuộc về Report 4.
- **Nhóm đi sâu về kỹ thuật (`Report 4 — SDD`):** Mô tả đầy đủ kiến trúc phần mềm, ranh giới module/package, thiết kế CSDL vật lý & logic, object storage, Class Diagram, Sequence Diagram, API endpoint, DTO/error code và các bất biến (*invariants*) khớp 100% với mã nguồn đang chạy.
- **Báo cáo tổng hợp (`Report 7 — Final Project Report`):** Tổng hợp tinh gọn toàn bộ `Reports 1–6` thành một quyển hoàn chỉnh cho Hội đồng bảo vệ, giữ đúng độ sâu tương ứng cho từng chương (chương I, II, III, V, VI mạch lạc, dễ đọc cho hội đồng; chương IV SDD giữ phần thiết kế kỹ thuật trọng tâm; mọi số liệu, danh sách `FE-01`–`FE-24` và kết quả test thống nhất xuyên suốt).

**Quy ước chung xuyên suốt mọi báo cáo:**

1. **Ngôn ngữ:** Toàn bộ **Reports 1–7**, **Project Tracking**, **Weekly Reports** và bộ **Review 2 (`Registration`, `BM01`–`BM04`)** viết bằng **tiếng Anh kỹ thuật** nhất quán. Riêng **Phiếu tự đánh giá (`final-self-evaluation/`)** và tài liệu điều phối nội bộ (`development/`, `project-reference/`) viết bằng tiếng Việt.
2. **Nhất quán thuật ngữ & số liệu:**
   - Gọi đúng 4 vai trò (`ADMIN`, `MANAGER`, `CUSTOMER`, `INSPECTOR`), 4 main flows (`MF1`–`MF4`), 24 features (`FE-01`–`FE-24`), tên tích hợp thật (`PostgreSQL 17 pgvector`, `MinIO`, `YOLO11`, `DroneKnowledgeAI`, `SmartDroneHub`, `Sepay VietQR`, `VNPay`, `Google OAuth 2.0`).
   - Số lượng bảng PostgreSQL, số phiên bản Flyway `V*`, số lượng test case/test suite phải đồng bộ giữa các report ở cùng một thời điểm chốt mốc.
3. **Trung thực về phạm vi & bằng chứng:**
   - Không mô tả tính năng chưa có hoặc đã loại bỏ (`MAINTENANCE_ENGINEER`, sửa chữa bảo trì, dựng 3D, điều khiển bay tự động) như tính năng đang hoạt động.
   - Phân biệt rạch ròi **mục tiêu yêu cầu (*acceptance target*)** với **kết quả đo đạc thực tế (*measured result*)**; không điền `Passed`, ngày test hay tên tester cho test case chưa chạy.
   - Mọi chỉnh sửa phải ghi thêm một dòng lịch sử vào `Record of Changes` của report đó.

### 5.2 Ma trận Target Reader, Giọng văn, Độ sâu & Cách viết từng Report

| Tài liệu | Thư mục nguồn | Độ sâu kỹ thuật | Target Reader | Giọng văn (Tone & Voice) | Trọng tâm nội dung & cách viết |
| --- | --- | --- | --- | --- | --- |
| **Report 1 — Project Introduction** | `reports/report-1-project-introduction/` | **Thấp (Nghiệp vụ & bài toán)** | Hội đồng xét duyệt đề tài, Giảng viên hướng dẫn, Stakeholder phi kỹ thuật | **Thuyết phục, mạch lạc, định hướng bài toán – giá trị nghiệp vụ**; không sa đà chi tiết công nghệ/code | Mở bằng vấn đề vận hành thực tế tại Việt Nam -> đối chiếu khách quan 3 sản phẩm hiện có (`DroneDeploy`, `Flyability Inspector`, `Skycatch`: *Description / Actors / Features / Pros / Cons*) -> cơ hội thị trường & Product Vision -> tóm tắt 4 `MF` / 24 `FE` ở góc độ giá trị -> chốt ranh giới loại trừ (`LI-1`..`LI-9`). |
| **Report 2 — Project Management Plan** | `reports/report-2-project-management-plan/` | **Thấp – Vừa (Quản trị & công cụ ở mức kế hoạch)** | Giảng viên hướng dẫn, Hội đồng đánh giá quy trình PM/QA, các thành viên nhóm | **Chặt chẽ, định lượng, mang tính cam kết & quản trị**; dùng thuật ngữ PM chuẩn | WBS tách khớp 24 `FE` + các hạng mục nền (`CC-01`..`CC-04`), đối chiếu nỗ lực `208` man-days trên `300` raw person-days theo tỷ lệ thực tế từng thành viên (`24%/24%/28%/24%`); Risk Register có Impact/Possibility/Response rõ ràng; Quality Gates, RACI (`D/R/S/I`), Training Plan và Tools ở mức tổng quan quy trình Git/CI/Docker của nhóm. |
| **Report 3 — Software Requirement Specification (SRS)** | `reports/report-3-software-requirement-specification/` | **Trung lập cài đặt (Hành vi & ràng buộc nghiệp vụ)** | Backend/Web/Mobile Developer, QA/Tester viết test case, Reviewer nghiệp vụ | **Đặc tả chuẩn mực — chính xác, đơn nghĩa, kiểm thử được (*testable*)**; câu chủ động nêu rõ Actor (`CUSTOMER`, `MANAGER`, `INSPECTOR`, `ADMIN`, `SYSTEM`), **không lộ chi tiết cài đặt tầng code** | Chia 6 file (`00`–`05`): Overview & Domain Tòa nhà -> Actors & Use Cases (`Động từ + Đối tượng`, mỗi UC một mục tiêu nguyên tử) -> Screens Flow, Screen Descriptions, Screen Authorization (`Query All Data` / `Query Own Data`), Non-Screen Functions, ERD khái niệm/mức cao, đặc tả hành vi `FE-01`..`FE-24` (Trigger, Precondition, Normal/Alternative/Exception flows, Screen layout thật) -> NFR (`NFR-01`..`NFR-08` đủ Metric + Threshold + Verification Method) -> Business Rules (`BR-01`..`BR-55`, đánh dấu `SUPERSEDED` nếu đổi rule), Common Requirements, `MSGxx` & Traceability Matrix 24 dòng. |
| **Report 4 — Software Design Document (SDD)** | `reports/report-4-software-design-document/` | **Sâu (Kiến trúc, DB, Class, Sequence, API)** | Kỹ sư phần mềm (Dev/Architect), thành viên bảo trì, Hội đồng chấm kỹ thuật chuyên sâu | **Kỹ thuật chuẩn xác (*as-built*), súc tích, bám sát mã nguồn**; dùng đúng tên module, class, method, endpoint, migration `V*`, bảng/cột DB và error code thật | Chia 4 file (`00`–`03`): System Design (Kiến trúc tổng thể + Package Diagram cho Backend 8 Spring Modulith packages, Web Portal, Mobile App + bảng mô tả package) -> Database Design (chính xác chuỗi Flyway `V*`, số bảng thật, bố cục key MinIO, ERD + bảng mô tả toàn bộ bảng) -> Detailed Design 1-1 cho `FE-01`..`FE-24` (Class Diagram, Sequence Diagram, Class/Endpoint Spec, Invariants) + mục Design Constraints & Exclusions. |
| **Report 5 — Test Documentation** | `reports/report-5-test-documentation/` | **Vừa (Chiến lược, phạm vi & kết quả kiểm chứng)** | QA/Tester, Reviewer kiểm chứng chất lượng, Hội đồng chấm kiểm thử | **Thực chứng, khách quan, truy vết rõ ràng**; tập trung vào chiến lược, tiêu chí chấp nhận và bằng chứng chạy test, không giải thích sâu cấu trúc code nội bộ | Nêu rõ Scope (`FE-01`..`FE-24`, `NFR-01`..`NFR-08`), tách riêng **Items Not to be Tested**, mô tả Test Strategy (Equivalence Partitioning, Boundary Analysis, State Transition, Scope Isolation, AI Fallback), 4 Test Levels (Unit, Integration, System, Acceptance), môi trường test & số liệu chạy thực tế có ngày xác nhận. |
| **Report 5 — Test Report (`.xlsx`)** | `reports/report-5-test-report/` | **Vừa (Kịch bản thao tác & kết quả kiểm thử)** | QA Lead, Giảng viên & Hội đồng đối chiếu từng case kiểm thử | **Ngắn gọn, tái lập được (*reproducible*), trung thực trạng thái**; mô tả bước test theo hành vi chức năng & kết quả mong đợi | Chỉ sửa các file Markdown trong `00-cover/`, `01-test-cases/`, `02-test-statistics/`, `03-features/fe-01..fe-24.md`; giữ ổn định ID `WFx-xxx` và đúng 15 cột execution (3 Round). Case `Pending`/`N/A` tuyệt đối không bịa ngày/tester; thống kê tổng ở `test-statistics.md` phải khớp tổng từng sheet. Đọc [template-layout.md](reports/report-5-test-report/template-layout.md) trước khi sửa. |
| **Report 6 — Software User Guides** | `reports/report-6-software-user-guides/` | **Thấp (Thao tác người dùng cuối & cài đặt cơ bản)** | Người dùng cuối theo 4 vai trò (`CUSTOMER`, `INSPECTOR`, `MANAGER`, `ADMIN`) và người cài đặt/demo hệ thống | **Hướng dẫn thực hành (*how-to / imperative*), rõ ràng, thân thiện**; phần User Manual tránh hoàn toàn thuật ngữ kỹ thuật/API/DB nội bộ | Phần 1: Deliverable Package. Phần 2: System Requirements & Installation Guide từng bước (clone 4 repo song song, `.env`, `docker compose`, web/mobile, bootstrap & xử lý sự cố cơ bản). Phần 3: User Manual theo từng luồng nghiệp vụ đầu-cuối, chia bước đánh số khớp với chú thích trên ảnh chụp thật (`1600×1000`). |
| **Report 7 — Final Project Report** | `reports/report-7-final-project-report/` | **Tổng hợp (Phân tầng theo từng chương)** | **Hội đồng bảo vệ khóa luận tốt nghiệp** (đọc tổng hợp toàn bộ dự án trong một quyển duy nhất) | **Học thuật trang trọng, mạch lạc, cô đọng và dễ đọc** cho hội đồng không cần đọc hết từng report lẻ | Hợp nhất 6 chương (`01` Intro -> `02` PMP -> `03` SRS -> `04` SDD -> `05` Testing -> `06` Release & User Guides) kèm `Acknowledgement` và `Definition and Acronyms`. Chương I, II, III, V, VI viết súc tích, dễ hiểu, không nhồi chi tiết cài đặt thừa; chương IV giữ trọng tâm thiết kế kỹ thuật từ SDD; rà chéo để số liệu DB, danh sách `FE-01`..`FE-24`, cổng thanh toán (`Sepay VietQR` + `VNPay`), 4 vai trò và kết quả test khớp 100% giữa mọi chương. |
| **Project Tracking & Weekly Reports** | `reports/project-tracking/`, `reports/weekly-project-reports/` | **Vừa (Nhật ký công việc & lỗi)** | Giảng viên hướng dẫn theo dõi tiến độ hàng tuần & Leader điều phối | **Súc tích dạng nhật ký vận hành (*log style*), định hướng hành động** | `project-tracking.md`: giữ đúng 4 bảng (WBS, Issues, Defects, Q&A), mỗi lỗi đóng phải ghi rõ commit/PR/test xác nhận. `week-XX.md`: giữ đúng 4 bảng 5 cột (*Status Report, Project Issues, Next Week Plan, Other Matters*), gắn mã Jira `SCRUM-*`, người phụ trách và trạng thái. |
| **Review 2 Package (`Registration`, `BM01`–`BM04`)** | `reports/review-2-*/` | **Vừa (Tóm tắt quyết định & phạm vi)** | Hội đồng chấm Review 2 đọc lướt nhanh trong buổi đánh giá | **Cực kỳ cô đọng (*scannable*), tập trung vào điểm thay đổi & quyết định** | Viết dạng bảng súc tích: `BM03` làm rõ thay đổi so với đăng ký gốc; `BM01` nêu quyết định thiết kế (`D1`–`D5`), top risks, gaps; `BM02` ghi trung thực kết quả self-review + phản hồi nhóm; `BM04` khóa phạm vi 4 workflow & kịch bản demo (`DS-*`). |
| **Final Self-Evaluation** | `reports/final-self-evaluation/` | **Thấp – Vừa (Tổng kết học thuật & tự đánh giá)** | Giảng viên hướng dẫn & Hội đồng chấm tốt nghiệp | **Tiếng Việt, trang trọng, khách quan, tự phản tỉnh trung thực** | Nêu đúng tên đề tài tiếng Việt/tiếng Anh theo quyết định, tóm tắt kết quả nội dung/hình thức/thái độ và % đóng góp từng thành viên, đối chiếu mức độ đạt được so với đề cương gốc và thẳng thắn chỉ ra các hạn chế hiện tại của sản phẩm. |
