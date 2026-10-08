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

## 5. Kết quả kiểm tra schema V25/V26 (đã xác minh)

### 5.1 Điểm 1 — Entity `Inspection` phải dựng lại hoàn toàn, không sửa

Bảng `inspections` **còn**, nhưng V26 đã thay toàn bộ hình dạng cột:

| Cột bị `DROP` ở V26 | Cột thay thế do V25 thêm vào |
| --- | --- |
| `service_order_id`, `accepted_assignment_id` | `asset_pair_assignment_id`, `drone_id`, `inspector_id` |
| `author_user_id` | `inspector_id` (FK composite kiểm tra cùng tổ chức) |
| `checklist_template_id` | `checklist_template_id`/`checklist_version` chuyển sang `field_sessions` |
| `started_at`, `completed_at` | `planned_start_at`, `planned_end_at`; trạng thái thật nằm ở `field_sessions` |

Cột **vẫn giữ**: `id`, `asset_id`, `status`, `created_at`, `updated_at`, `row_version`, `organization_id`, `schedule_id`, `due_cycle_key`, `objective`, `scope`, `component_scope`, `acceptance_criteria`, `planned_start_at`, `planned_end_at`.

`ck_inspections_status` được V26 định nghĩa lại thành đúng 11 giá trị mục tiêu:
`DRAFT`, `ASSIGNED`, `PREPARING`, `READY_FOR_FLIGHT`, `IN_PROGRESS`, `FIELD_COMPLETED`, `REPORT_DRAFT`, `REPORT_PUBLISHED`, `REPAIR_PENDING`, `COMPLETED`, `CANCELLED`.

**Kết luận**: entity `Inspection` phải viết mới theo đúng 18 cột này — không phải khôi phục bản cũ.

### 5.2 Điểm 2 — Dùng `asset_pair_assignments`, **không cần migration mới**

Bảng đã có sẵn và đúng nghĩa MF2-01:

```
asset_pair_assignments
  id, organization_id, asset_id
  inspector_user_id   ← MF2-01/02: người được phân công
  drone_id            ← MF2-03/04: drone được gán
  valid_from / valid_until
  status ∈ (DRAFT, ACTIVE, SUPERSEDED, SUSPENDED)
  reason, assigned_by_user_id, assigned_at
```

`inspections.asset_pair_assignment_id` trỏ tới đây, và V26 đã gắn FK composite
`fk_inspections_pair_tenant (asset_pair_assignment_id, organization_id, asset_id)` để chặn
trường hợp ghép cặp chéo tổ chức.

**Phản hồi nhận/từ chối của Inspector** chưa có cột riêng. Hai lựa chọn:

| Cách | Ảnh hưởng |
| --- | --- |
| Dùng `reason` + `status` của `asset_pair_assignments` | Không cần migration, nhưng gộp "lý do từ chối" với "lý do gán" |
| Thêm cột `assignment_response` + `responded_at` vào `asset_pair_assignments` | Rõ ràng hơn, cần migration `V27` |

**Đề xuất**: dùng `status = SUSPENDED` + `reason` để Inspector từ chối, giữ nguyên cam kết
"không thêm migration". Nếu bạn muốn phân biệt rõ hai loại lý do thì tôi tạo `V27`.

### 5.3 Điểm 3 — Cam kết 20 commit

Danh sách ở §4 là dự kiến. Cam kết: **tổng đúng 20 commit** trên 4 repo (Backend 17,
Frontend 2, Mobile 1), mỗi commit build/test độc lập được. Nếu cần thêm/bớt, tôi sẽ
bù lại để tổng vẫn là 20.

### 5.4 Quyết định đã chốt — migration `V27`

Owner chọn **Cách 2: thêm migration `V27`**, không tái dùng `reason`.

Lý do chọn: MF2-01 là một quyết định nghiệp vụ có chủ thể, không phải một đổi trạng thái
của cặp tài sản–drone. Gộp vào `reason` sẽ khiến một cột mang hai nghĩa khác nhau (lý do
ORG_ADMIN gán cặp, và lý do Inspector từ chối), đồng thời không lưu được thời điểm phản
hồi — tức không phân biệt được "trả lời muộn" với "chưa trả lời". SRS 3.1.4 yêu cầu mọi
chuyển tiếp đáng kể phải truy vết được, nên hai cột riêng là phương án đúng.

`V27__assignment_response.sql` thêm:

| Cột | Kiểu | Ý nghĩa |
| --- | --- | --- |
| `assignment_response` | `VARCHAR(24)` | `ACCEPTED` / `REJECTED` / `NULL` khi chưa trả lời |
| `responded_at` | `TIMESTAMPTZ` | Thời điểm Inspector trả lời |

Kèm hai CHECK:
- `ck_asset_pair_assignments_response` — response và responded_at cùng có hoặc cùng không.
- `ck_asset_pair_assignments_response_vocabulary` — chỉ nhận `ACCEPTED` / `REJECTED`.

Migration có pre-check `DO $$` đúng convention V15/V16/V18, dùng `ADD COLUMN IF NOT EXISTS`
nên idempotent. Migration không ghi response — `InspectionAssignmentService` sở hữu
chuyển tiếp đó. `assignment_response = 'ACCEPTED'` **không** phải `READY_FOR_FLIGHT`; đó là
quyết định riêng của MF2-07 với reviewer độc lập và snapshot riêng.

**Điều chỉnh danh sách commit**: commit 1 chuyển từ `feat(workforce)` sang
`feat(inspections): add V27 assignment response columns`, phần còn lại giữ nguyên thứ tự
(lùi 1 số).