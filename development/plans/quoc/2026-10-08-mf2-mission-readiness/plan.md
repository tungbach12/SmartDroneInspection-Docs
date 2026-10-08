# Kế hoạch triển khai MF2 — Mission Preparation, Assignment Response and Readiness

**Owner**: Quốc
**Nhánh**: `feat/quoc-enterprise-mf1-mf8` (cả 4 repo)
**Ngày**: 2026-10-08
**Đặc tả**: `reports/report-3-software-requirement-specification/03-functional-requirements.md` §3.4 FE-03
**Trạng thái schema**: V25 đã tạo bảng, V26 đã dọn MF1–MF5 cũ — MF2 hiện **chưa có runtime**.

---

## 1. MF2 làm gì

MF2 đi từ **phân công Inspector** đến **sẵn sàng bay và bắt đầu phiên bay hiện trường**.

| Bước | Ai | Việc |
| --- | --- | --- |
| MF2-01 | INSPECTOR | Mở phân công; xem asset, phạm vi, drone được gán; **nhận hoặc từ chối** kèm lý do |
| MF2-02 | SYSTEM | Kiểm tra scope; ghi nhận phản hồi; thông báo ORG_ADMIN |
| MF2-03 | INSPECTOR | Lập **shot-list**, loại bằng chứng yêu cầu, checklist; ghi rủ t ro hạ tầng, giờ dự kiến, nguy hiểm |
| MF2-04 | ORG_ADMIN | Liên kết **giấy phép bay** thực tế + hồ sơ năng lực/drone; ghi nguồn kiểm tra không phận |
| MF2-05 | SYSTEM | Kiểm tra liên kết, ngày hiệu lực, xung đột; liệt kê blocker |
| MF2-06 | INSPECTOR | Đọc hạn chế; ghi nhận an toàn; nộp phần chuẩn bị |
| MF2-07 | ORG_ADMIN | **Duyệt hoặc trả lại** kèm lý do → `READY_FOR_FLIGHT` |
| MF2-08 | SYSTEM | Snapshot kế hoạch đã duyệt; thông báo |
| MF2-09 | INSPECTOR | Tại hiện trường: nhận diện drone, pre-flight checklist, yêu cầu Start hoặc ghi lý do hoãn |
| MF2-10 | SYSTEM | Kiểm tra lại entitlement/assignment/readiness; ghi `IN_PROGRESS` |

**Ranh giới quan trọng**: phần mềm **không điều khiển drone**. `READY_FOR_FLIGHT` là quyết định của người có thẩm quyền, không phải giấy phép do hệ thống cấp.

---

## 2. Schema đã có sẵn (không cần migration mới)

V25 đã tạo đủ 3 bảng trọng yếu:

| Bảng | Cột chính |
| --- | --- |
| `inspection_preparations` | `inspection_id`, `inspector_user_id`, `preparation_version`, `shot_list`, `evidence_types`, `access_constraints`, `safety_observations`, `permit_document_references`, `status` |
| `inspection_readiness_decisions` | `inspection_id`, `preparation_id`, `decision`, `reviewed_by_user_id`, `reason`, `permit_snapshot`, `credential_snapshot`, `drone_document_snapshot`, `source_hash` |
| `field_sessions` | `inspection_id`, `organization_id`, `inspector_user_id`, `drone_id`, `readiness_decision_id`, `status`, `started_at`, `ended_at`, `postponement_reason`, `abort_reason`, `checklist_template_id`, `readiness_version` |

Bảng hỗ trợ đã có: `drones`, `drone_documents`, `flight_permits`, `workforce_credentials`, `asset_pair_assignments`.

---

## 3. Khoảng cách hiện tại

| Tầng | Backend | Frontend | Mobile |
| --- | --- | --- | --- |
| Entity | ❌ chưa có | — | — |
| Repository | ❌ chưa có | — | — |
| Service | ❌ chưa có | — | — |
| Controller | ❌ chưa có | — | — |
| Test | ❌ chưa có | — | — |
| UI | — | ❌ chưa có | ❌ chưa có |

Module `inspectionrequests` đã bị V26 xóa hoàn toàn. Module `inspections` còn 4 entity (`Evidence`, `InspectionReport`, `VerifiedFinding`, `AiFindingCandidate`) và 2 SPI, nhưng **không có `Inspection` entity** dù bảng `inspections` còn tồn tại.

---

## 4. Kế hoạch 20 commit

### Nhóm A — Nền tảng dùng chung (commit 1–4)

| # | Commit | Nội dung |
| --- | --- | --- |
| 1 | `feat(workforce): map V25 workforce_credentials schema` | Entity `WorkforceCredential` + enum loại/chứng chỉ |
| 2 | `feat(assets): map V25 drones, flight permits and asset pairs` | Entity `Drone`, `DroneDocument`, `FlightPermit`, `AssetPairAssignment` |
| 3 | `feat(inspections): restore Inspection entity on V25/V26 schema` | Entity `Inspection` (bảng còn, entity đã mất) |
| 4 | `feat(shared): add typed error codes for MF2 readiness gates` | Mã lỗi ổn định dùng chung |

### Nhóm B — MF2-01/02 Phân công & phản hồi (commit 5–7)

| # | Commit | Nội dung |
| --- | --- | --- |
| 5 | `feat(inspections): preparation and readiness repositories` | 3 repository cho preparation/decision/session |
| 6 | `feat(inspections): inspection assignment accept/reject service` | `InspectionAssignmentService` — MF2-01/02 |
| 7 | `feat(inspections): assignment response API endpoints` | Controller `/api/v1/inspections/{id}/assignment-response` |

### Nhóm C — MF2-03..06 Chuẩn bị & nộp (commit 8–11)

| # | Commit | Nội dung |
| --- | --- | --- |
| 8 | `feat(inspections): preparation draft entity transitions` | State machine `DRAFT → SUBMITTED` trên `InspectionPreparation` |
| 9 | `feat(inspections): shot list and safety acknowledgment service` | MF2-03 + MF2-06 |
| 10 | `feat(inspections): preparation API with permit reference links` | MF2-04/05 validation + endpoint |
| 11 | `test(inspections): preparation scope and missing-permit denial` | Test cho Review Focus |

### Nhóm D — MF2-07/08 Duyệt & snapshot (commit 12–14)

| # | Commit | Nội dung |
| --- | --- | --- |
| 12 | `feat(inspections): readiness decision entity with snapshot hash` | `InspectionReadinessDecision` |
| 13 | `feat(inspections): reviewer approval service gating READY_FOR_FLIGHT` | MF2-07 — reviewer phải độc lập |
| 14 | `feat(inspections): readiness API and change invalidation` | MF2-08 — đổi kế hoạch → mất readiness |

### Nhóm E — MF2-09/10 Phiên bay (commit 15–17)

| # | Commit | Nội dung |
| --- | --- | --- |
| 15 | `feat(inspections): field session entity with postponement reasons` | `FieldSession` |
| 16 | `feat(inspections): session start service re-checking readiness version` | MF2-09/10 — stale readiness bị chặn |
| 17 | `test(inspections): field session start integration tests` | Test tích hợp có DB |

### Nhóm F — Frontend & Mobile (commit 18–20)

| # | Commit | Nội dung |
| --- | --- | --- |
| 18 | `feat(inspections): MF2 preparation screens for Inspector` | Shot list, checklist, acknowledge an toàn |
| 19 | `feat(inspections): MF2 readiness review screen for ORG_ADMIN` | Duyệt/trả lại kèm lý do |
| 20 | `feat(inspections): mobile pre-flight checklist and session start` | Mobile: nhận diện drone, Start/hoãn |

### Tổng: **20 commit** (Backend 17, Frontend 2, Mobile 1)

Docs sẽ có commit riêng khi cập nhật Report 5 — có thể thay thế một commit nhóm F nếu cần giữ đúng 20.

---

## 5. Rủi ro cần xác nhận trước khi code

1. **`inspections` entity đã mất** nhưng bảng còn — cần xác nhận `inspections` có còn cột `service_order_id`/`assignment_id` hay V26 đã đổi.
2. **`assignment` không có bảng riêng** — MF2-01 cần một nơi lưu phân công Inspector. Có thể dùng `asset_pair_assignments` (V25) hoặc cần migration mới.
3. **Danh sách 20 commit là dự kiến** — khi code sẽ có thể điều chỉnh, chỉ cần giữ tổng số bằng 20 là đạt yêu cầu.