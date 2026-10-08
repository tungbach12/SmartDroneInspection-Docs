---
title: "Capstone Error-Prevention Guide"
description: "Checklist giúp nhóm tránh các lỗi phổ biến khi làm tài liệu, phát triển, kiểm thử và bảo vệ dự án SmartDroneInspection."
weight: 30
---

# Hướng dẫn tránh lỗi Capstone cho nhóm SmartDroneInspection

> **Status — 7 October 2026:** This guide contains useful general quality principles, but its scenario-specific role, workflow, demo-script and review-question examples were written against earlier project baselines. Treat those examples as historical, not current product scope or implementation evidence. The current target has four roles (`ADMIN`, `ORG_ADMIN`, `INSPECTOR`, `MAINTENANCE_ENGINEER`) and MF1–MF4; the backend reset has not implemented those workflow behaviors. Reconcile examples against current Report 3 and current runtime before using them in a demo or submission.

Tài liệu này chuyển các lưu ý trong *Cẩm nang tránh lỗi Capstone SE* thành checklist thực hành cho nhóm. Nguyên tắc quan trọng nhất: **tài liệu, mã nguồn, dữ liệu kiểm thử và nội dung demo phải mô tả cùng một hệ thống**. Không ghi một tính năng là đã hoàn thành nếu chưa có mã nguồn và bằng chứng kiểm thử tương ứng.

## 1. Sáu rủi ro cần ưu tiên

| Rủi ro | Dấu hiệu | Cách phòng tránh | Bằng chứng cần giữ |
|---|---|---|---|
| Tài liệu không khớp sản phẩm | SRS có chức năng nhưng demo hoặc code không có | Chốt baseline và cập nhật traceability sau mỗi sprint | Commit, test, ảnh màn hình, API contract |
| Mô hình mâu thuẫn | Actor, use case, workflow, ERD và màn hình dùng tên khác nhau | Dùng một từ điển thuật ngữ và một bộ role chính thức | Glossary, diagram source, review record |
| Thiếu luồng ngoại lệ | Chỉ mô tả happy path | Hỏi “Nếu... thì sao?” cho mọi bước quan trọng | Alternative/exception flows và test case |
| Hardcode nghiệp vụ | Giá, trạng thái, timeout hoặc role nằm rải rác trong code | Đưa cấu hình đúng chỗ và dùng enum/policy tập trung | Config, migration, policy test |
| AI bị trình bày quá khả năng | Kết quả AI được coi là kết luận cuối cùng | Công bố model/version/metric; bắt buộc người dùng xác minh | Dataset, metric, model version, review log |
| Demo thiếu chuẩn bị | Dữ liệu sai, mạng lỗi, thành viên không biết luồng | Diễn tập theo script và chuẩn bị phương án dự phòng | Demo script, seed data, video dự phòng |

## 2. Quy tắc viết và kiểm tra tài liệu

- Dùng đúng template chính thức, giữ cấu trúc, style, header/footer và đánh số trang.
- Xóa toàn bộ nội dung mẫu, placeholder, hướng dẫn trong ngoặc và bookmark lỗi trước khi nộp.
- Tên figure đặt **bên dưới** hình; tên table đặt **bên trên** bảng. Mọi figure/table quan trọng phải được nhắc đến trong phần mô tả.
- Cập nhật mục lục, số trang và cross-reference bằng Word trước khi xuất PDF.
- Dùng một ngôn ngữ nhất quán trong tài liệu tiếng Anh; chỉ giữ từ viết tắt đã được định nghĩa.
- Không mô tả planned feature như implemented feature. Ghi rõ ranh giới phiên bản và trạng thái triển khai.
- Trước khi nộp, mở Print Preview hoặc PDF và kiểm tra từng trang: không tràn bảng, không cắt hình, không có trang trắng bất thường.

## 3. Giữ mô hình hệ thống nhất quán

### Actor và quyền (mục tiêu hiện tại)

Bốn role liệt kê dưới đây là mục tiêu ngày 7 October 2026. Các ví dụ phía sau nhắc Service Manager, Client, Provider Manager, quotation/order, peer-review, billing hoặc demo WF1–WF4 thuộc baseline lịch sử, không phải scope hiện tại hay bằng chứng triển khai. Backend reset chưa hiện thực workflow MF1–MF4; không dùng các ví dụ đó như quy trình có thể chạy hiện nay.

Bốn actor nghiệp vụ chính thức của dự án là:

1. Admin (`ADMIN`)
2. Organization Administrator (`ORG_ADMIN`)
3. Inspector (`INSPECTOR`)
4. Maintenance Engineer (`MAINTENANCE_ENGINEER`)

Không dùng lại các tên role cũ như Viewer, Inspection Manager, Service Manager, Client, hay Provider trong tài liệu mới. Use case phải có tên dạng **động từ + đối tượng**, ví dụ “Approve Inspection Readiness”, không đặt tên chung chung như “Inspection Management”.

### Use case, workflow và activity diagram

- Use-case diagram trả lời **ai được làm gì**, không thay cho business workflow.
- Workflow/activity diagram trả lời **công việc diễn ra theo thứ tự nào**, ai chịu trách nhiệm và điều kiện chuyển bước là gì.
- Mỗi use case chính phải có precondition, trigger, main flow, alternative/exception flow và postcondition.
- Tên actor, trạng thái và đối tượng phải giống nhau trong SRS, UI, API và code.

### ERD và kiến trúc

- ERD trong SRS nên là mô hình khái niệm hoặc mức cao; không trộn ký hiệu tùy ý hay biến nó thành bản dump database vật lý.
- Mỗi quan hệ phải có cardinality hợp lý và phản ánh đúng workflow.
- Architecture diagram phải thể hiện đúng target stack và phân biệt rõ phần nào đang chạy, phần nào còn planned; ghi rõ inspection/maintenance workflows chưa được implement trong backend reset branch.
- Không tự thêm hệ thống hoặc tích hợp ngoài vào sơ đồ nếu workflow, code và phạm vi dự án không có. Ảnh kiểm tra hiện được tải lên từ SD card, máy tính hoặc thiết bị di động.

## 4. Business rule và luồng ngoại lệ

Mỗi business rule cần có mã định danh, nội dung rõ ràng và liên kết đến requirement, code/policy và test. Với từng target main flow, nhóm phải trả lời ít nhất năm câu hỏi; nội dung này là tiêu chí cần triển khai/kiểm thử, không phải bằng chứng runtime:

1. Nếu dữ liệu đầu vào thiếu hoặc sai thì sao?
2. Nếu người dùng không có quyền hoặc truy cập sai organization thì sao?
3. Nếu người dùng thao tác đồng thời hoặc gửi lại yêu cầu thì sao?
4. Nếu dịch vụ ngoài, mạng hoặc lưu trữ tạm thời lỗi thì sao?
5. Nếu người dùng từ chối, yêu cầu sửa hoặc hủy giữa luồng thì sao?

Các rule quan trọng của dự án:

Các rule mục tiêu ngày 7 October 2026 dưới đây là yêu cầu cần triển khai và kiểm thử, không phải tuyên bố rằng workflow runtime hiện đã tồn tại:

- Entitlement subscription và organization scope phải được kiểm tra khi bắt đầu công việc; schema không đồng nghĩa với access workflow đã hoàn tất.
- Inspector phải được gán đúng inspection mới chuẩn bị hoặc bắt đầu được.
- Inspector là tác giả phải xác minh và chỉnh sửa AI-generated report draft, đối chiếu evidence, findings và checklist trước khi ORG_ADMIN đủ chuyên môn kiểm tra và phát hành.
- AI chỉ tạo defect candidate; Inspector phải confirm, modify hoặc reject trước khi đưa vào báo cáo.
- ORG_ADMIN không tự đưa ra technical maintenance estimate thay cho Maintenance Engineer.
- Công việc maintenance phải có bằng chứng before/after; phát sinh ngoài phạm vi cần change approval.
- Dữ liệu và thao tác phải bị giới hạn theo organization hoặc assignment.

## 5. Tránh hardcode sai chỗ

- Role, state transition và authorization policy phải có định nghĩa tập trung.
- Secret, URL dịch vụ, thời hạn token và thông số môi trường đi qua configuration/secret management.
- Giá dịch vụ, ngưỡng vận hành hoặc nội dung có thể thay đổi phải đi qua dữ liệu/config phù hợp, không rải literal trong controller.
- Enum chỉ dùng cho tập giá trị ổn định; dữ liệu nghiệp vụ thường xuyên thay đổi nên lưu trong database.
- Mọi default quan trọng phải được ghi trong tài liệu triển khai và có thể override theo môi trường.

## 6. AI/YOLO: trình bày đúng và có kiểm soát

- Ghi rõ model name/version, dataset, metric, ngưỡng confidence và ngày đánh giá.
- Không dùng accuracy chung chung nếu bài toán cần precision, recall, F1 hoặc mAP.
- Mô tả false positive, false negative và các điều kiện hình ảnh model hoạt động kém.
- Lưu kết quả AI dưới dạng candidate kèm confidence và bounding box; không tự động biến candidate thành defect chính thức.
- Inspector phải là người xác minh cuối cùng. Candidate bị reject hoặc chưa review không được đưa vào report hay maintenance ticket.
- Khi AI lỗi hoặc không khả dụng, hệ thống phải cho phép quy trình manual phù hợp và ghi nhận lỗi để theo dõi.

## 7. Kiểm thử và traceability

- Test case phải xuất phát từ functional requirement, business rule và exception flow; không chỉ kiểm thử UI happy path.
- Lưu kết quả chạy test thực tế. Không dùng bảng test “Pass” nếu chưa chạy hoặc không có evidence.
- Ưu tiên test các ranh giới quyền của target workflow: cross-organization, unassigned Inspector/Engineer, report-author verification, ORG_ADMIN authority và unauthorized transitions. Các mục này là test obligations; chúng chưa khẳng định reset branch đã cung cấp các API đó.
- Viết case idempotency/concurrency cho các target write paths; chỉ ghi kết quả khi implementation tồn tại và test thực sự chạy. Report 5 target cases remain Pending until then.
- Ghi rõ khi test MinIO/AI adapters chưa chứng minh deployed integration hoặc workflow path.
- Traceability tối thiểu nên nối: `Workflow → Use Case → Requirement → Business Rule → Test Case → Demo Step`.

## 8. UI/UX và demo data

- Mỗi màn hình phải thể hiện quyền và trạng thái được hỗ trợ ở tested release; nút bị ẩn ở UI không thay thế authorization ở backend.
- Thông báo lỗi phải nói người dùng cần làm gì tiếp theo, không chỉ hiển thị mã kỹ thuật.
- Không lộ raw object-storage URL, token, secret, stack trace hoặc dữ liệu của organization khác.
- Chuẩn bị demo data nhỏ cho các workflow slices actually present and verified; không seed target behavior để trông như đã chạy.
- Demo nên dùng một bộ dữ liệu ổn định; không sửa dữ liệu trực tiếp trong database giữa phần trình bày nếu không nằm trong kịch bản.

## 9. Demo script — historical v1 example (not the current target)

The sequence below describes the retired five-role WF1–WF4/marketplace baseline. It is not a current Enterprise SaaS demo script, and it must not be presented as an end-to-end run of the reset branch. Build a replacement only from workflow slices that actually exist and have recorded verification evidence.

1. Historical example: Admin manages an account and role.
2. Historical example: Client registers an asset and recurring schedule (WF1).
3. Historical example: Service Manager reviews a request, prepares quotation/order and assigns an Inspector; Client approves and Inspector accepts (WF2).
4. Historical example: Inspector uploads evidence, reviews AI candidates, completes checklist and edits an AI-assisted report draft; Provider Manager releases; Client responds (v1 MF3/MF4).
5. Historical example: Service Manager creates a ticket; Maintenance Engineer assesses and repairs; Client approves changes/acceptance or requests rework (WF4).
6. For any actually runnable demo, show an access-denied or controlled-failure path and identify the tested software revision.

Chuẩn bị thêm video ngắn hoặc ảnh chụp cho các tích hợp phụ thuộc mạng, nhưng phải nói rõ đó là phương án dự phòng chứ không phải live demo.

## 10. Cách trả lời hội đồng

Dùng cấu trúc ngắn: **Có/Không → Lý do → Chỗ hiện thực → Hạn chế hoặc hướng cải tiến**.

Ví dụ: “Có. Báo cáo bắt buộc peer-review để giảm sai sót chuyên môn. Rule được kiểm tra tại service khi chuyển trạng thái; Inspector có `authorId` trùng report sẽ bị từ chối. Phiên bản hiện tại chưa hỗ trợ hội đồng review nhiều người.”

Nếu chưa làm, trả lời thẳng: “Chưa có trong phiên bản hiện tại”, sau đó nêu lý do ưu tiên và hướng mở rộng. Không ứng biến rằng tính năng đã có.

## 11. Quản lý nhóm và feedback

- Mỗi góp ý cần có bốn trường: vấn đề, người phụ trách, hạn xử lý, bằng chứng hoàn tất.
- Giữ lịch sử contribution qua issue, pull request, commit và review; không gom toàn bộ công việc vào một tài khoản.
- Sau mỗi buổi review, phân loại feedback thành: lỗi bắt buộc, rủi ro cần giảm, đề xuất cải thiện.
- Không đánh dấu feedback “done” chỉ vì đã sửa tài liệu; phải kiểm tra code/test/demo bị ảnh hưởng.

## 12. Security, privacy và pháp lý

- Không commit password, JWT signing secret, API key hoặc file môi trường thật.
- Kiểm soát tải xuống evidence/report tại backend; không dựa vào URL khó đoán.
- Audit thao tác nhạy cảm nhưng không log password, access/refresh token hoặc dữ liệu bí mật.
- Nêu rõ quyền sử dụng dataset, ảnh drone, thư viện và model; lưu license/attribution cần thiết.
- Chuẩn bị chính sách retention/xóa dữ liệu phù hợp với phạm vi đồ án.

## 13. Lịch tự kiểm trước buổi review

### D-14

- Chốt scope, role, workflow và baseline tài liệu.
- Lập traceability và danh sách gap giữa tài liệu với code.
- Giao người chịu trách nhiệm cho từng gap.

### D-7

- Hoàn tất chức năng đã thực sự triển khai trong release scope và chạy các integration test tương ứng.
- Lập demo script chỉ cho các đường đi hiện có bằng chứng; không quảng bá MF1–MF4 target như một luồng end-to-end đã chạy khi workflow còn chưa được implement.
- Đóng blocker đã xác minh và cập nhật sơ đồ/tài liệu theo trạng thái code hiện tại.

### D-3

- Đóng băng demo data và demo script.
- Review chéo Report 3, slide và câu trả lời hội đồng.
- Kiểm tra caption, TOC, số trang, link, chính tả và PDF export.

### D-1

- Diễn tập đủ thời lượng với đúng máy và môi trường sẽ dùng.
- Kiểm tra tài khoản, mạng, adapter, dữ liệu và bản backup.
- Không thêm feature lớn hoặc refactor rủi ro cao.

### Ngày bảo vệ

- Chạy smoke test trước giờ trình bày.
- Mở sẵn ứng dụng, tài liệu, log/evidence và demo data.
- Một người demo, một người theo dõi script/thời gian, các thành viên còn lại sẵn sàng trả lời phần mình phụ trách.

## 14. Câu hỏi nhóm phải tự trả lời được

- Tại sao hệ thống có đúng năm role này và quyền của từng role nằm ở đâu?
- Bằng cách nào ngăn truy cập chéo organization, và bằng chứng nào ghi nhận Inspector tác giả đã xác minh/chỉnh sửa report draft trước khi Provider Manager phát hành?
- Nếu YOLO đưa kết quả sai hoặc ngừng hoạt động, workflow tiếp tục ra sao?
- Requirement nào chứng minh một periodic request không bị tạo trùng?
- Khi maintenance phát sinh ngoài quotation đã duyệt, ai duyệt và hệ thống chặn ở bước nào?
- Dữ liệu nào được lưu ở PostgreSQL, dữ liệu nào ở MinIO, và quyền tải file được kiểm tra ra sao?
- Ảnh kiểm tra đi vào hệ thống bằng đường nào, được lưu ở đâu và ai có quyền truy cập?
- Bằng chứng nào cho thấy test đã chạy trên sản phẩm hiện tại?

## 15. Phiếu chấm rủi ro 0–2

Chấm từng mục: `0 = chưa có`, `1 = có nhưng chưa đủ bằng chứng`, `2 = hoàn chỉnh và đã kiểm tra`.

| Hạng mục | Điểm 0–2 |
|---|---:|
| Template, mục lục, caption và pagination đúng | |
| Actor/role nhất quán ở docs, code và demo | |
| WF1–WF4 có main/alternative/exception flows | |
| Use case, ERD, architecture và UI không mâu thuẫn | |
| Business rule có trace đến code và test | |
| AI có metric/version/human verification/fallback | |
| Authorization theo organization/assignment đã test | |
| Demo data và script đã chạy end-to-end | |
| Test result có evidence thật | |
| Feedback và contribution có lịch sử | |
| Security/privacy/license đã rà soát | |
| Mỗi thành viên trả lời được phần phụ trách | |

Nếu bất kỳ mục bắt buộc nào có điểm `0`, chưa nên chốt bản nộp. Nếu tổng điểm dưới `20/24`, ưu tiên sửa tính nhất quán và bằng chứng trước khi bổ sung tính năng mới.
