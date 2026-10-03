# Multi-Provider Platform, Escrow Cash Flow, Platform Operator & 5 Main Flows Docs Redesign Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Overhaul the entire `SmartDroneInspection-docs` documentation suite to transform the platform architecture into a Multi-Provider Drone Inspection Platform structured around 5 canonical Main Flows (MF1–MF5) and 6 specialized roles across 3 Actor Zones—specifically adding `PLATFORM_OPERATOR` distinct from `PLATFORM_ADMIN` to manage providers, customer organizations, escrow oversight, and dispute arbitration—while making the Platform the sole owner/operator of YOLO inference, data processing, MinIO storage, and LLM narrative assistance; strictly conforming to `project-reference/error-prevention.md` and the latest Vietnamese legal framework.

**Architecture:** Redesign documentation across all SRS layers:
1. `project-reference/business-flows.md`: Complete rewrite into 5 Main Flows with tripartite governance, operator arbitration, and mandatory 5 exception questions per flow.
2. `project-reference/database-design.md`: Updated with `PLATFORM_OPERATOR` role, Provider organizations, pilot registry, Escrow transaction lifecycle, and Dispute entities.
3. Report 1 and Report 2 current-scope sections: Update product vision, stakeholder/role model, scope boundaries, risk, and delivery plan to describe the approved multi-provider architecture without rewriting historical dated records.
4. Report 3 SRS sections (00, 01, 02, 03, 04, 05): Aligned with 6 canonical roles, 3 Actor Zones, updated Business Rules (BR-01 through BR-40+), and Use Cases named strictly as **Verb + Noun**.
5. Report 5 test report (cover, README/layout, test cases, statistics, all eight feature files): Synchronized to version 2.0 with truthful separation of implemented baseline (v1.x) vs. planned multi-provider/dispute acceptance cases (marked `Pending`).
6. Development planning handoffs updated.

**Tech Stack:** Markdown, Hugo, Mermaid diagrams, Git, GitHub PR workflow.

**Spec / design review:** `project-reference/business-flows.md` is an unapproved target draft being revised alongside this plan; it is not implemented behavior. The council's `project-reference/error-prevention.md` governs traceability and truthfulness. Legal applicability and proposed payment operations require primary-source verification before being stated as obligations or deployed features. No separate approved written spec exists yet.

## Global Constraints

- **Strict Document-Only Scope**: Do not edit Java backend code, React frontend code, Flutter mobile code, or Flyway SQL migrations in this plan.
- **Platform-Owned AI and Data Services**:
  - The Platform owns, configures, makes available, and pays for YOLO inference, data processing, MinIO storage, and LLM narrative assistance; an external infrastructure or model vendor may operate components under Platform control.
  - Provider and Client accounts only consume these services through Platform Web/Mobile screens; they do not self-host models or add AI/data-processing line items to Client quotations.
  - AI output remains a candidate until Inspector verification; LLM narrative remains a draft until human review and peer review.
- **One Platform-Set Commission Policy for Every Provider**:
  - Platform publishes one uniform, non-negotiable commission rate and calculation rule for all participating Provider organizations. There are no individually negotiated rates. Changes apply prospectively to new orders after notice; an accepted order retains its captured policy version.
  - Client pays the accepted Provider service price; Provider quotation excludes AI/data/LLM/storage charges and must not separately add a Platform fee. Platform funds those operating costs from its commission revenue and other Platform resources.
  - At settlement, the authorized payment partner distributes the service proceeds according to the captured commission policy: Provider payout = eligible settled service amount minus Platform commission; Platform commission is accounted for separately from the Provider's service invoice and taxes. No 100%-to-Provider or universal 10% split is presumed.
  - The commission percentage remains **unselected** until research and Platform cost assumptions justify it. Define the fee base, tax treatment, refunds, cancellation, disputes, and maintenance retention before documenting any worked split; do not invent a fixed percentage.
- **Council Error-Prevention Compliance (`error-prevention.md`)**:
  - *No False Completion Claims*: Do not describe planned multi-provider or dispute features as implemented in Report 5. Keep new cases strictly as `Pending`.
  - *Unified Vocabulary*: Consistent names for all 6 roles, states, and entities across Business Flows, Report 3, Database Design, and Report 5.
  - *Verb + Noun Use Cases*: Every use case must follow the verb-object naming convention (e.g., "Vet Service Provider", "Approve Service Order", "Arbitrate Dispute").
  - *Mandatory 5 Exception Questions*: Every main flow (MF1–MF5) must explicitly document invalid input, unauthorized/cross-organization access, concurrency/idempotency, external service/network failure, and refusal/cancellation/dispute/revision.
  - *AI/YOLO Control*: Platform hosts AI/data processing; outputs remain strictly non-official defect candidates, Inspector human verification is mandatory, and manual defect creation fallback is guaranteed.
  - *No unsupported legal claims*: `PLATFORM_OPERATOR` issues an internal platform resolution under published terms; this does not replace a court judgment or legally recognized commercial arbitration. The plan must not call the Operator a supreme tribunal.
  - *No unlicensed escrow claims*: Model escrow as an account/payment flow integrated with a bank or authorized payment provider; do not describe the Platform as a bank or independently accepting deposits.
- **6 Canonical Roles across 3 Actor Zones**:
  1. `PLATFORM_GOVERNANCE`:
     - `PLATFORM_ADMIN`: System administration, security policies, catalog & checklist standard templates, technical infrastructure, global audit logs.
     - `PLATFORM_OPERATOR`: Business operations, Provider vetting & onboarding, Customer success & matching, Escrow fund release/freeze execution, and **Primary Dispute Arbitrator**.
  2. `CUSTOMER_ORGANIZATION`:
     - `CLIENT`: Infrastructure owner, asset registration, RFQ/Provider selection, contract signing, 100% Escrow deposit, report acceptance, defect ticketing, dispute filing.
  3. `SERVICE_PROVIDER`:
     - `PROVIDER_MANAGER`: Drone/Maintenance company executive, profile & pilot compliance, quotation drafting, flight authorization (Cục Tác chiến), staff assignment, QA report release.
     - `INSPECTOR`: Certified drone pilot/inspector, field flight execution, MinIO evidence upload (GPS/EXIF/SHA-256), Platform-hosted AI candidate review, cross-peer review.
     - `MAINTENANCE_ENGINEER`: Field technician, defect assessment, maintenance execution, before/after evidence capture.
- **5 Canonical Main Flows**:
  - `MF1`: Onboarding Pháp lý Đối tác, Thẩm định & Quản trị Hồ sơ Tài sản.
  - `MF2`: Lập Yêu cầu, Khớp nối Provider, Hợp đồng Điện tử & Ký quỹ Escrow.
  - `MF3`: Khảo sát Drone Hiện trường, Xử lý AI & Báo cáo Kỹ thuật (QA).
  - `MF4`: Nghiệm thu, Tự động Quyết toán & Trọng tài Phân xử Tranh chấp.
  - `MF5`: Xử lý Khiếm khuyết, Đơn hàng Bảo trì & Tiền Bảo lãnh Hoàn công.
- **Latest Vietnamese Legal Grounding**: Explicitly cite and apply:
  - *Luật Phòng không nhân dân 2024 (Luật số 49/2024/QH15, hiệu lực 01/07/2025)*, *Nghị định 198/2025/NĐ-CP (hiệu lực 22/08/2025)*, and *Nghị định 288/2025/NĐ-CP (hiệu lực 05/11/2025)*: drone/UAV registration and operation rules, pilot certification, Cục Tác chiến flight permits, and no-fly/restricted-airspace controls.
  - *Luật Giao dịch điện tử 2023 (Luật số 20/2023/QH15, hiệu lực 01/07/2024)*: legal electronic contracts, data messages, timestamps, and MinIO SHA-256 evidence.
  - *Luật Bảo vệ quyền lợi người tiêu dùng 2023 (Luật số 19/2023/QH15, hiệu lực 01/07/2024)* and *Nghị định 55/2024/NĐ-CP*: intermediary platform transparency and complaint-handling duties; operator resolution is internal platform handling, not a replacement for court or commercial arbitration.
  - *Nghị định 85/2021/NĐ-CP (sửa đổi NĐ 52/2013/NĐ-CP về TMĐT)*: platform rules, complaint/mediation mechanism, and transaction record cooperation.
  - *Nghị định 52/2024/NĐ-CP*: non-cash payment and payment intermediary/account safeguards; escrow must be integrated with an authorized bank/payment provider, not treated as a Platform bank account.
- **Traceability Preservation**: Report 3 and Report 5 must maintain cross-referencing integrity and clear changelogs. Version numbers represent document revisions, not proof of feature delivery.
- **Commission formula for every report**: `r` is one published Platform-set rate accepted as a standard Provider participation term, identical across Provider organizations and service categories, never negotiated per Provider. `B = eligible VAT-exclusive Provider service subtotal − Provider-funded discount − valid VAT-exclusive service-price refund`, floored at zero; `C = r × B`. Lock the `r`/base-rule version at order confirmation. Provider invoices Client for the full eligible service consideration and applicable Provider VAT; Platform invoices Provider for `C` plus Platform-service VAT as applicable. Refunds reverse proportionate commission, maintenance retention is not charged a second time, and provider VAT and platform VAT remain distinct. Do not select a numerical `r` without cost evidence.
- **Commercial terms are not law**: 100% advance funding, five working days for review, 10% retention, 20% dry-run, 48-hour reshoot, 30-day warranty and mandatory provider insurance are proposals requiring express published terms and legal review; do not present them as statutory or implemented.

## Review Focus

1. **Error-Prevention Checklist Alignment**: Ensure all 6 risk categories in `error-prevention.md` (Tài liệu không khớp, Mô hình mâu thuẫn, Thiếu luồng ngoại lệ, Hardcode, AI quá mức, Demo thiếu chuẩn bị) are defended in the docs text.
2. **5 Exception Questions per Flow**: Verify that MF1 through MF5 each have a dedicated subsection answering all 5 exception questions.
3. **Role Boundary Separation**: Verify strict separation between `PLATFORM_ADMIN` (IT/system/standards) and `PLATFORM_OPERATOR` (business/providers/customers/arbitration) in all use cases and permission matrices.
4. **Provider Data Isolation**: Ensure `PROVIDER_MANAGER`, `INSPECTOR`, and `MAINTENANCE_ENGINEER` are strictly scoped to their owning Provider Organization, preventing cross-provider leakage.
5. **Platform Capability Ownership**: Verify every Report 3 and Report 5 reference says Platform supplies/hosts YOLO, data processing, MinIO, and LLM, while Provider/Client only consume them and provider quotation excludes those costs.
6. **Legal Accuracy**: Verify drone references include NĐ 198/2025/NĐ-CP and NĐ 288/2025/NĐ-CP, escrow references do not turn Platform into a bank, and Operator dispute decisions are explicitly internal platform resolutions.
7. **Truthful Test Reporting**: Ensure Report 5 strictly marks new multi-provider and dispute test cases as `Pending` without false "Passed" claims.

---

### Task 1: Rebuild Core Business Flows Reference (MF1–MF5)

**Files:**
- Modify: `SmartDroneInspection-docs/project-reference/business-flows.md`

**Interfaces:**
- Consumes: User-approved 5 Main Flows architecture, 6 roles, Vietnamese legal framework, and `error-prevention.md` guidelines.
- Produces: Authoritative business-flow specification referenced by Report 3 SRS, Report 5 Test Report, and developer plans.

- [x] **Step 1: Write header, legal framework, and 6-role canonical matrix**
  - Define 3 Actor Zones: `PLATFORM_GOVERNANCE` (`PLATFORM_ADMIN`, `PLATFORM_OPERATOR`), `CUSTOMER_ORGANIZATION` (`CLIENT`), `SERVICE_PROVIDER` (`PROVIDER_MANAGER`, `INSPECTOR`, `MAINTENANCE_ENGINEER`).
  - Cite Vietnamese laws: Luật PKND 2024 (Số 49/2024/QH15), NĐ 198/2025/NĐ-CP (effective 22/08/2025), NĐ 288/2025/NĐ-CP (effective 05/11/2025), Luật GDĐT 2023 (Số 20/2023/QH15), Luật BVQLNTD 2023 (Số 19/2023/QH15), NĐ 85/2021/NĐ-CP, NĐ 52/2024/NĐ-CP, QĐ 18/2020/QĐ-TTg (`cambay.mod.gov.vn`).

- [x] **Step 2: Detail MF1 — Onboarding Đối tác, Thẩm định & Hồ sơ Tài sản**
  - MF1-01: Client Enterprise Self-Registration.
  - MF1-02: Provider Vetting by `PLATFORM_OPERATOR` (Kiểm tra giấy phép kinh doanh, khai báo định danh drone theo Luật PKND 2024, chứng chỉ phi công, chứng thư bảo hiểm trách nhiệm bên thứ ba). Operator phê duyệt, yêu cầu bổ sung hoặc từ chối.
  - MF1-03: Asset & Airspace Profiling (Khai báo tọa độ, ranh giới, tra cứu bản đồ cấm bay `cambay.mod.gov.vn`).
  - MF1-04: Periodic Inspection Cadence & Request Package Generation.
  - *Exception Section*: Answer all 5 questions for MF1 (invalid license, unverified provider bid, duplicate asset code, portal timeout, application rejection).

- [x] **Step 3: Detail MF2 — Yêu cầu Kiểm định, Khớp nối Provider, Hợp đồng & Ký quỹ Escrow**
  - MF2-01: Sourcing & RFQ (Chỉ định trực tiếp hoặc chào thầu mở; `PLATFORM_OPERATOR` hỗ trợ kết nối đối tác nếu cần; Shot list, yêu cầu độ phân giải GSD).
  - MF2-02: Versioned Quotation Breakdown (Phí bay + nhân công/kỹ thuật Provider + chi phí triển khai hợp lệ + VAT). Platform centrally absorbs YOLO, data processing, MinIO storage, and LLM costs; these are never Provider quotation line items.
  - MF2-03: Electronic Service Order & 100% Escrow Deposit (Ký hợp đồng điện tử theo Luật GDĐT 2023; Client nộp 100% tiền vào Platform Escrow Pool theo NĐ 52/2024/NĐ-CP; trạng thái `LEGALLY_BINDING`).
  - MF2-04: Pilot Assignment & Flight Authorization (Giấy phép bay Cục Tác chiến; kiểm tra xung đột lợi ích; trạng thái `READY_FOR_INSPECTION`).
  - Cancellation Policy: Trước 24h hoàn 100%; Trong 24h phạt phí di chuyển Dry-run fee 20%; Bất khả kháng thời tiết dời lịch miễn phí.
  - *Exception Section*: Answer all 5 questions for MF2 (incomplete SOW, foreign provider quote, duplicate escrow payment, bank gateway timeout, quotation revision / cancellation).

- [x] **Step 4: Detail MF3 — Khảo sát Drone Hiện trường, Xử lý AI & Báo cáo Kỹ thuật (QA)**
  - MF3-01: Field Survey & Evidence Ingestion (Nạp ảnh/video lên MinIO qua Web/Mobile; trích xuất GPS, timestamp; tính SHA-256 checksum chống trùng lặp và làm chứng cứ số hợp pháp).
  - MF3-02: YOLO AI Detection & Inspector Verification (AI phát hiện lỗi; Inspector Confirm/Modify/Reject; Manual finding entry fallback).
  - MF3-03: Internal Peer Review (Inspector độc lập cùng Provider duyệt chéo; người bay không duyệt báo cáo của mình).
  - MF3-04: Provider Manager Release (Ký duyệt phát hành báo cáo kỹ thuật; kích hoạt đồng hồ nghiệm thu 5 ngày).
  - *Exception Section*: Answer all 5 questions for MF3 (corrupt photo/missing GPS, cross-assignment edit, duplicate upload retry, YOLO service down / MinIO failure, peer-review change request).

- [x] **Step 5: Detail MF4 — Nghiệm thu Báo cáo, Quyết toán Tự động & Trọng tài Phân xử Tranh chấp**
  - MF4-01: Client Technical Review & Clarification (Yêu cầu giải trình/sửa đổi trong 5 ngày làm việc).
  - MF4-02: Happy Path & Auto-Settlement (Client bấm Accept hoặc hết thời hạn nghiệm thu theo điều khoản đã duyệt; báo cáo trở thành bất biến `COMPLETED`; đối tác thanh toán giải ngân phần dịch vụ đủ điều kiện sau khi khấu trừ hoa hồng `C = r × B` theo một tỷ lệ chung do Platform công bố và khóa theo Service Order; Platform tự chịu chi phí AI/data/storage/LLM).
  - MF4-03: Dispute Filing (Client hoặc Provider mở tranh chấp; tiền Escrow lập tức bị ĐÓNG BĂNG `FROZEN_DISPUTED`).
  - MF4-04: `PLATFORM_OPERATOR` Internal Platform Resolution (Operator thụ lý hồ sơ theo Platform Terms; đối soát Hợp đồng MF2 vs. Bằng chứng MinIO MF3 vs. Khiếu nại; 3 biện pháp nội bộ: Free Reshoot / Hủy hợp đồng + hoàn tiền + phạt theo Terms / Bác khiếu nại + giải ngân; không thay thế Tòa án hoặc trọng tài thương mại).
  - *Exception Section*: Answer all 5 questions for MF4 (invalid dispute evidence, unauthorized third-party dispute access, concurrent dispute & accept, notification gateway down, provider appeal / reshoot refusal).

- [x] **Step 6: Detail MF5 — Xử lý Khiếm khuyết, Đơn hàng Bảo trì & Tiền Bảo lãnh Hoàn công**
  - MF5-01: Defect-to-Maintenance Ticket Creation.
  - MF5-02: Maintenance Quotation & Work Order (Ký quỹ gói bảo trì; áp dụng điều khoản Tiền giữ lại bảo hành Retention Money 10%).
  - MF5-03: Execution & Before/After Evidence (Kỹ sư thi công, nạp ảnh đối chứng trước/sau bắt buộc).
  - MF5-04: Change Order Management (Phát sinh hư hỏng ngầm vượt dự toán; Client duyệt và ký quỹ bổ sung mới làm tiếp).
  - MF5-05: Two-Stage Settlement & Final Closure (Giai đoạn 1: Nghiệm thu hoàn công -> giải ngân 90%, giữ 10% Retention; Giai đoạn 2: Sau 30 ngày bảo hành không tái hỏng -> giải ngân nốt 10%; Operator xử lý tranh chấp bảo hành nội bộ theo Platform Terms).
  - *Exception Section*: Answer all 5 questions for MF5 (missing before/after photos, unauthorized engineer execution, duplicate change request, storage failure, client re-inspection / rework request).

- [x] **Step 7: Verify formatting and commit Task 1**
  - Run: `git -C SmartDroneInspection-docs diff --check`
  - Commit: `docs(flows): rebuild business flows with 6 roles, multi-provider platform, escrow and operator arbitration`

---

### Task 2: Update Database Design & Domain Model Documentation

**Files:**
- Modify: `SmartDroneInspection-docs/project-reference/database-design.md`

**Interfaces:**
- Consumes: 6 roles, Provider organizations, Escrow, and Dispute models from Task 1.
- Produces: Data model specifications aligning schema tables and constraints with multi-provider requirements.

- [x] **Step 1: Document Provider Organization, Pilot Registry & Operator Role Extensions**
  - Add `provider_organizations` (id, legal_name, tax_code, business_license_no, drone_permit_code, insurance_policy_no, status `PENDING/VERIFIED/SUSPENDED/BANNED`, rating_score, created_at, approved_by_operator_id).
  - Document role extension in `user_roles`: `PLATFORM_OPERATOR` in `PLATFORM_GOVERNANCE` zone; `provider_id` foreign key for `SERVICE_WORKFORCE` zone.
  - Document pilot registry: pilot license number, certified drone models, flight log summary.

- [x] **Step 2: Document Contract & Escrow Transaction Schema**
  - Add target settlement/transaction records with `order_id`, `client_org_id`, `provider_org_id`, partner reference, customer-funded amount, eligible fee base `B`, uniform policy version/rate `r`, calculated commission `C`, separate Provider-service and Platform-commission tax amounts, Provider net payout, disputed/retained/refunded amounts, and statuses `PAYMENT_PENDING/HELD_IN_ESCROW/FROZEN_DISPUTED/DISBURSED/REFUNDED/PARTIALLY_REFUNDED`. Distinguish these proposed tables from the current Flyway schema. The platform must integrate a bank/licensed payment provider whose actual product permits conditional release; it is not an independent bank or deposit-taking entity.
  - Extend `inspection_service_orders` with legal terms, shot list/GSD JSONB, flight permit number, SLA deadlines, escrow reference, and a clear statement that YOLO/data/MinIO/LLM costs are platform operational overhead rather than Provider quotation lines.

- [x] **Step 3: Document Dispute Entity Schema**
  - Add `dispute_tickets` (id, order_id, raised_by_user_id, client_org_id, provider_org_id, dispute_category `QUALITY/AIRSPACE_SAFETY/TIMELINESS/BILLING`, dispute_reason, client_claim, provider_response, status `OPENED/UNDER_ARBITRATION/RESOLVED/CLOSED`, resolution_decision `FREE_RESHOOT/FULL_REFUND/REJECTED_DISPUTE`, decided_by_operator_id, decided_at, penalty_amount).
  - Add `dispute_evidence` (dispute_id, uploaded_by_user_id, evidence_type, minio_object_key, sha256_checksum, description).

- [x] **Step 4: Update Maintenance Retention & Invoices Schema**
  - Add retention fields to `maintenance_orders`: `retention_percentage`, `retention_amount`, `warranty_end_date`, `retention_status` (`HELD/RELEASED/FORFEITED`).
  - Document dual-invoice model: Platform commission invoice (Platform -> Provider) and full Service invoice (Provider -> Client); their respective VAT classifications and invoice timing require tax review. Include proportional fee reversal for actual service-price refunds and no duplicate commission on the warranty-retention release.

- [x] **Step 5: Verify formatting and commit Task 2**
  - Run: `git -C SmartDroneInspection-docs diff --check`
  - Commit: `docs(database): document multi-provider, operator governance, escrow and dispute schemas`

---

### Task 3: Align Report 1 and Report 2 Current Scope

**Files:**
- Modify: `SmartDroneInspection-docs/reports/report-1-project-introduction/report1-project-introduction.md`
- Modify: `SmartDroneInspection-docs/reports/report-2-project-management-plan/report2-project-management-plan.md`

**Interfaces:**
- Consumes: MF1–MF5, six roles, Platform-owned AI/data capabilities, and scope boundaries from `business-flows.md`.
- Produces: Current product vision and management-plan sections consistent with Report 3 without rewriting dated historical baselines.

- [x] **Step 1: Update Report 1 current product scope and role narrative**
  - Describe the platform as a multi-provider service marketplace connecting Client organizations with verified Provider organizations.
  - Introduce `PLATFORM_ADMIN`, `PLATFORM_OPERATOR`, `CLIENT`, `PROVIDER_MANAGER`, `INSPECTOR`, and `MAINTENANCE_ENGINEER` in current-scope sections.
  - State explicitly that Platform supplies/operates YOLO, data processing, MinIO, and LLM narrative assistance; providers and clients only consume these tools.
  - Add the current legal references (Luật PKND 2024, NĐ 198/2025/NĐ-CP, NĐ 288/2025/NĐ-CP, Luật GDĐT 2023, Luật BVQLNTD 2023, NĐ 85/2021/NĐ-CP, NĐ 52/2024/NĐ-CP) without claiming undocumented implementation.

- [x] **Step 2: Update Report 2 current scope, risks, responsibilities, and technology plan**
  - Replace current five-role target language with the six-role / three-zone target for the approved redesign.
  - Add delivery risks for provider isolation, authorized payment/escrow integration, airspace permit compliance, internal dispute resolution, and Platform AI availability.
  - Identify implementation dependencies as planned work; do not convert any new capability into a passed status.

- [x] **Step 3: Verify formatting and commit Task 3**
  - Run: `git -C SmartDroneInspection-docs diff --check`
  - Commit: `docs(scope): align Reports 1 and 2 with approved multi-provider architecture`

---

### Task 4: Overhaul Report 3 SRS — Overall Description & User Requirements

**Files:**
- Modify: `SmartDroneInspection-docs/reports/report-3-software-requirement-specification/01-overall-description.md`
- Modify: `SmartDroneInspection-docs/reports/report-3-software-requirement-specification/02-user-requirements.md`

**Interfaces:**
- Consumes: 6 canonical roles, legal citations, and use cases adhering to Verb + Noun format.
- Produces: System context, business rules, and user requirements.

- [x] **Step 1: Rewrite Product Overview and Actor Zones in `01-overall-description.md`**
  - Describe the Multi-Provider Drone Inspection Platform and explicitly state that Platform owns/operates YOLO inference, data processing, MinIO storage, and LLM narrative assistance; Provider and Client only consume these capabilities.
  - Define the 3 Actor Zones and 6 canonical roles:
    - Platform Governance: `PLATFORM_ADMIN`, `PLATFORM_OPERATOR`.
    - Customer Organization: `CLIENT`.
    - Service Provider: `PROVIDER_MANAGER`, `INSPECTOR`, `MAINTENANCE_ENGINEER`.
  - Cite current legal stack: Luật PKND 2024, NĐ 198/2025/NĐ-CP, NĐ 288/2025/NĐ-CP, Luật GDĐT 2023, Luật BVQLNTD 2023, NĐ 55/2024/NĐ-CP, NĐ 85/2021/NĐ-CP, NĐ 52/2024/NĐ-CP.

- [x] **Step 2: Revise Business Rules Table (BR-01 to BR-45+) in `01-overall-description.md`**
  - Retain core evidence & AI rules (checksum, GPS, AI non-official, peer review separation).
  - Add Operator & Provider governance rules:
    - Provider must be verified by `PLATFORM_OPERATOR` before bidding/taking orders.
    - Operator cannot be affiliated with any Client or Provider org.
  - Add Platform Capability rules:
    - Platform hosts/pays for YOLO inference, data processing, MinIO storage, and LLM narrative assistance.
    - Provider quotations exclude Platform AI, storage, and data-processing costs; Provider and Client only consume Platform capabilities.
  - Add Legal & Airspace rules:
    - Flights must comply with Luật PKND 2024, NĐ 198/2025/NĐ-CP, NĐ 288/2025/NĐ-CP, Cục Tác chiến permits, and no-fly zones (`cambay.mod.gov.vn`).
  - Add Escrow & Dispute rules:
    - 100% Escrow deposit required to activate `LEGALLY_BINDING` order through an authorized bank/payment provider.
    - 5-day client review window with auto-settlement.
    - Dispute freezes escrow; `PLATFORM_OPERATOR` issues internal platform resolution under Platform Terms, without replacing courts or commercial arbitration.
    - Maintenance retention money (10%) held for 30-day warranty.

- [x] **Step 3: Update System Actors in `02-user-requirements.md`**
  - Add detailed actor definitions for `PLATFORM_ADMIN` vs. `PLATFORM_OPERATOR`, `CLIENT`, `PROVIDER_MANAGER`, `INSPECTOR`, and `MAINTENANCE_ENGINEER`.

- [x] **Step 4: Update Use Case Matrix & Descriptions in `02-user-requirements.md` (Strict Verb + Noun)**
  - Ensure every Use Case (UC01–UC32) follows Verb + Object naming and matches the actual six-role matrix:
    - Authenticate User; Configure System Security; Vet Service Provider; Register Infrastructure Asset; Manage Asset Documents; Schedule Periodic Inspection.
    - Solicit Quotations; Issue Inspection Quotation; Approve Service Order; Deposit Escrow Funds; Authorize Flight Assignment; Respond to Flight Assignment.
    - Conduct Drone Survey; Upload Chunked Evidence; Verify Defect Candidates; Compile Draft Report; Peer-Review Inspection Report; Release Inspection Report; Review Final Report.
    - Settle Escrow Payout; File Contract Dispute; Arbitrate Contract Dispute; Create Maintenance Ticket; Assess Defect Condition; Issue Maintenance Quotation; Approve Maintenance Order; Execute Maintenance Repair; Capture Before-After Evidence; Manage Maintenance Change; Verify Repair Completion; Release Warranty Retention.

- [x] **Step 5: Verify formatting and commit Task 3**
  - Run: `git -C SmartDroneInspection-docs diff --check`
  - Commit: `docs(srs): align overall description and user requirements with 6 roles, operator arbitration and verb-noun use cases`

---

### Task 5: Overhaul Report 3 SRS — Functional Requirements, NFRs, Appendix & Changelog

**Files:**
- Modify: `SmartDroneInspection-docs/reports/report-3-software-requirement-specification/03-functional-requirements.md`
- Modify: `SmartDroneInspection-docs/reports/report-3-software-requirement-specification/04-non-functional-requirements.md`
- Modify: `SmartDroneInspection-docs/reports/report-3-software-requirement-specification/05-requirement-appendix.md`
- Modify: `SmartDroneInspection-docs/reports/report-3-software-requirement-specification/00-record-of-changes.md`

**Interfaces:**
- Consumes: Detailed feature specifications mapped to MF1–MF5 and `error-prevention.md`.
- Produces: Complete functional requirements for all software capabilities (FE-01 to FE-08).

- [x] **Step 1: Update Screen & Non-Screen Function Matrices in `03-functional-requirements.md`**
  - Add screens: Provider Verification Portal, RFQ/Bidding Screen, Escrow Payment & Transaction Screen, Dispute Filing & Internal Resolution Portal, Platform AI Candidate/Narrative Review.
  - Update non-screen functions: Escrow deposit verification via authorized payment provider, 5-day auto-settlement timer, airspace no-fly zone geofence check, frozen-funds enforcement, Platform-hosted YOLO inference, Platform-hosted LLM narrative generation, and manual fallback.
  - Update Screen Authorization Matrix for all 6 roles.

- [x] **Step 2: Update FE-01 (Identity, Provider Vetting & Platform Governance)**
  - Detail `PLATFORM_OPERATOR` workflow: vetting Provider license, drone registry, pilot certification, insurance.

- [x] **Step 3: Update FE-02 (Asset Registry & Airspace Compliance)**
  - Integrate airspace compliance checking (`cambay.mod.gov.vn` no-fly zone lookup at asset coordinates).

- [x] **Step 4: Update FE-03 (Inspection Sourcing, Quotation, Escrow & Order)**
  - Sourcing mechanisms (direct select vs. open RFQ).
  - Quotation breakdown limited to Provider direct flight/labor/logistics/VAT; Platform AI/data/storage/LLM costs are excluded and absorbed by Platform.
  - Escrow deposit payment integration through authorized bank/payment provider.
  - Inspector assignment with flight permit validation.

- [x] **Step 5: Update FE-06 (Report Approval, Settlement & Internal Dispute Resolution)**
  - Contractually agreed client review period and auto-settlement: provider invoice remains on the full accepted service price while the licensed settlement partner pays the provider net of `C = r × B` and separately records Platform commission and applicable tax.
  - Dispute filing workflow with evidence attachment and immediate escrow freeze.
  - `PLATFORM_OPERATOR` internal platform resolution with three Platform Terms outcomes; explicitly preserve access to court/commercial arbitration where legally applicable.
  - Platform operational AI/data/storage costs are not deducted as Provider quotation lines.

- [x] **Step 6: Update FE-07 (Maintenance, Work Orders & Warranty Retention)**
  - Maintenance quotation with 10% retention money.
  - Before/After evidence validation.
  - Two-stage milestone payment release.

- [x] **Step 7: Update `00-record-of-changes.md`**
  - Append Version 2.0 entry: Complete architectural transition to Multi-Provider Drone Inspection Platform with `PLATFORM_OPERATOR`, Platform-owned YOLO/data/MinIO/LLM capabilities, escrow, and internal platform dispute resolution based on Luật PKND 2024, NĐ 198/2025/NĐ-CP, NĐ 288/2025/NĐ-CP, Luật GDĐT 2023, Luật BVQLNTD 2023, NĐ 85/2021/NĐ-CP, and NĐ 52/2024/NĐ-CP.

- [x] **Step 8: Update non-functional requirements and requirement appendix**
  - Document multi-tenant isolation, Provider data boundaries, escrow/payment-provider security, AI availability/manual fallback, MinIO evidence integrity, auditability, privacy, and legal/compliance boundaries.
  - State that Platform-owned YOLO/data/MinIO/LLM capabilities are service dependencies, not Provider or Client infrastructure responsibilities.
  - Remove or qualify unsupported claims about online payment, procurement, drone-operation integrations, or Platform being a financial institution.

- [x] **Step 9: Update `00-record-of-changes.md`**
  - Append Version 2.0 entry: Complete architectural transition to Multi-Provider Drone Inspection Platform with `PLATFORM_OPERATOR`, Platform-owned YOLO/data/MinIO/LLM capabilities, escrow, and internal platform dispute resolution based on the current legal stack.

- [x] **Step 10: Verify formatting and commit Task 5**
  - Run: `git -C SmartDroneInspection-docs diff --check`
  - Commit: `docs(srs): update functional, non-functional and legal requirement sources`

---

### Task 6: Synchronize Report 5 Test Report (Traceability & Truthful Reporting)

**Files:**
- Modify: `SmartDroneInspection-docs/reports/report-5-test-report/00-cover/cover.md`
- Modify: `SmartDroneInspection-docs/reports/report-5-test-report/00-cover/record-of-changes.md`
- Modify: `SmartDroneInspection-docs/reports/report-5-test-report/01-test-cases/test-case-list.md`
- Modify: `SmartDroneInspection-docs/reports/report-5-test-report/02-test-statistics/test-statistics.md`
- Modify: `SmartDroneInspection-docs/reports/report-5-test-report/03-features/fe-01-identity-access-governance.md`
- Modify: `SmartDroneInspection-docs/reports/report-5-test-report/03-features/fe-03-inspection-request-work-assignment.md`
- Modify: `SmartDroneInspection-docs/reports/report-5-test-report/03-features/fe-06-inspection-report-approval.md`
- Modify: `SmartDroneInspection-docs/reports/report-5-test-report/03-features/fe-02-asset-registry-inspection-schedule.md`
- Modify: `SmartDroneInspection-docs/reports/report-5-test-report/03-features/fe-04-inspection-execution-evidence-management.md`
- Modify: `SmartDroneInspection-docs/reports/report-5-test-report/03-features/fe-05-yolo-defect-detection-verification.md`
- Modify: `SmartDroneInspection-docs/reports/report-5-test-report/03-features/fe-07-maintenance-defect-resolution.md`
- Modify: `SmartDroneInspection-docs/reports/report-5-test-report/03-features/fe-08-dashboard-analytics-notifications.md`
- Modify: `SmartDroneInspection-docs/reports/report-5-test-report/README.md`
- Modify: `SmartDroneInspection-docs/reports/report-5-test-report/template-layout.md`

**Interfaces:**
- Consumes: Test case requirements for all newly introduced and modified workflows.
- Produces: Fully reconciled Report 5 test plan showing verified baseline and pending multi-provider/operator/dispute test cases without false completion claims.

- [x] **Step 1: Update Cover and Record of Changes in Report 5**
  - Bump Version to 2.0 in `cover.md` and `record-of-changes.md`.
  - Document modification scope: Multi-Provider test cases, Platform Operator vetting, Platform-owned AI/data/storage consumption, authorized escrow lifecycle verification, and internal Platform dispute resolution test cases.

- [x] **Step 2: Update Test Case Index in `test-case-list.md`**
  - Add test cases for Provider vetting by Operator (FE-01), Platform-owned YOLO/LLM/data-processing consumption and manual fallback (FE-05/FE-06), Escrow deposit (FE-03), Auto-settlement (FE-06), Dispute filing and Operator internal resolution (FE-06), and Maintenance retention money (FE-07).
  - Ensure all case IDs maintain a strict, non-overlapping format (`WF2-005`, `WF3-005`, `WF4-004`, etc.).

- [x] **Step 3: Update Test Statistics in `test-statistics.md` (Strict Compliance with `error-prevention.md`)**
  - Recalculate totals, passed, and pending counts.
  - Ensure new multi-provider and dispute cases are strictly marked `Pending` with truthful notes explaining that they define the target Multi-Provider acceptance baseline, preserving the council's rule: "Không mô tả planned feature như implemented feature".

- [x] **Step 4: Update all eight detailed feature sources (`03-features/`)**
  - Update FE-01/FE-02/FE-03/FE-04/FE-05/FE-06/FE-07/FE-08 scope baselines and procedures.
  - Add new Provider vetting, Platform AI/data consumption, escrow, auto-settlement, dispute, retention, and cross-provider authorization cases as `Pending` because no corresponding runtime implementation exists yet.
  - Preserve existing passed evidence only where it still matches the current implementation; do not rewrite historical results.

- [x] **Step 5: Update Report 5 README and template layout**
  - Preserve fixed workbook sheets and stable WFx IDs; document the new MF1–MF5/FE mapping and identify any newly planned cases as pending.

- [x] **Step 6: Verify formatting and commit Task 6**
  - Run: `git -C SmartDroneInspection-docs diff --check`
  - Commit: `docs(reports): synchronize Report 5 with operator governance, platform AI, escrow and dispute cases`

---

### Task 7: Synchronize Development Plans & Final Consistency Review

**Files:**
- Modify: `SmartDroneInspection-docs/development/plans/bach/2026-09-22-four-week-mainflow-delivery/spec.md`
- Modify: `SmartDroneInspection-docs/development/plans/bach/2026-09-22-four-week-mainflow-delivery/plan.md`
- Modify: `SmartDroneInspection-docs/development/plans/bach/2026-09-22-four-week-mainflow-delivery/tasks.md`
- Modify: `SmartDroneInspection-docs/development/plans/quoc/plan.md`

**Interfaces:**
- Consumes: Completed SRS and Test Report revisions.
- Produces: Fully aligned development plans for engineering team implementation.

- [x] **Step 1: Align Four-Week Plan Documents**
  - Update `spec.md`, `plan.md`, `tasks.md`, and `quoc/plan.md` to reference the 5 Main Flows, 6 roles (including `PLATFORM_OPERATOR`), Platform-owned YOLO/data/MinIO/LLM capabilities, authorized escrow milestones, internal dispute resolution, and the current NĐ 198/2025 + NĐ 288/2025 drone legal stack.
  - Correct legacy single-provider/Service Manager language in current planning sections while preserving dated historical context where needed.

- [x] **Step 2: Run Documentation Integrity Suite**
  - Run: `git -C SmartDroneInspection-docs diff --check`
  - Run relative link verification across all modified files.
  - Verify that no source code files or migrations in other repositories were modified.

- [x] **Step 3: Review Full Working Tree Diff and Commit Task 7**
  - Check `git -C SmartDroneInspection-docs status --short`
  - Run `git -C SmartDroneInspection-docs diff --check`.
  - Search modified reports for stale roles, stale fee splits, unsupported legal claims, and planned features marked as Passed.
  - Commit: `docs(plans): align development plans with multi-provider platform and operator governance`

---

## Plan Self-Review Checklist

- [x] **Spec coverage**: Covers Multi-Provider, `PLATFORM_OPERATOR`, Platform-owned YOLO/data/MinIO/LLM capabilities, authorized escrow, electronic contracts, internal dispute resolution, current Vietnamese legal stack, and `error-prevention.md` guidelines.
- [x] **No placeholders**: Every step contains concrete files, specific schemas, enums, legal references, and explicit actions.
- [x] **Type and Term consistency**: Canonical roles (`PLATFORM_ADMIN`, `PLATFORM_OPERATOR`, `CLIENT`, `PROVIDER_MANAGER`, `INSPECTOR`, `MAINTENANCE_ENGINEER`), escrow states, and flow codes (MF1–MF5) are uniform across all tasks.
- [x] **Review Focus**: Handles operator vs admin duties, provider data isolation, Platform AI ownership, authorized escrow boundaries, dispute internal-resolution wording, cancellation rules, truthful test status, and all reports/documentation sources.
