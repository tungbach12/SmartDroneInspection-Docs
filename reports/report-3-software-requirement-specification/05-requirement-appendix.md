---
title: "Report 3 - Other Requirements"
document_type: report3-srs-section
weight: 55
source: "report3-software-requirement-specification.docx"
---

## 5. Other Requirements

### 5.1 Appendix 1 - Application Messages List

The system defines standard user-facing messages, validation alerts, and toast notifications to guide operational workflows across web and mobile clients.

| # | Message code | Message Type | Context | Content |
| --- | --- | --- | --- | --- |
| 1 | MSG01 | In line | Search has no authorized records | No results found. |
| 2 | MSG02 | Under field | Required field empty | This field is required. |
| 3 | MSG03 | Under field | Configured length exceeded | Must not exceed {maxLength} characters. |
| 4 | MSG04 | Under field | Invalid email | Enter a valid email address. |
| 5 | MSG05 | Toast | Record created | Created successfully. |
| 6 | MSG06 | Toast | Record updated | Updated successfully. |
| 7 | MSG07 | Dialog | Irreversible/versioned action | Confirm this action and the version you are acting on. |
| 8 | MSG08 | In line | Authentication failed | Email or password is incorrect. |
| 9 | MSG09 | In line | Disabled/suspended account | Unable to sign in. Contact your administrator. |
| 10 | MSG10 | In line | Expired/revoked session | Your session has expired. Sign in again. |
| 11 | MSG11 | Under field | Password policy failure | Password does not meet the security requirements. |
| 12 | MSG12 | Toast | Inspection mission created | Inspection created with its asset and assigned Inspector/Drone snapshot. |
| 13 | MSG13 | In line | Stale report, plan or estimate version | A newer version is available. Refresh and review it before continuing. |
| 14 | MSG14 | Toast | Assignment accepted | Assignment accepted successfully. |
| 15 | MSG15 | Under field | Rejection lacks reason | Enter a reason for rejecting the assignment. |
| 16 | MSG16 | In line | Unsupported/corrupt/large evidence | This file cannot be uploaded. Check its type, integrity and size. |
| 17 | MSG17 | In line | Duplicate evidence | This evidence has already been uploaded in this scope. |
| 18 | MSG18 | Toast | Upload saved | Evidence uploaded and available for findings. |
| 19 | MSG19 | In line | AI unavailable | AI analysis is unavailable. Evidence is saved for manual review or later processing. |
| 20 | MSG20 | Toast | Inspection author submission | Author-verified draft submitted to Organization Manager for review. |
| 21 | MSG21 | In line | Author review incomplete | Verify each required report section against source evidence and scope before submitting. |
| 22 | MSG22 | Toast | Inspection report published | Approved inspection report version published successfully. |
| 23 | MSG23 | Toast | Repair change submitted | Scope/cost/time change submitted to Organization Manager for approval. Affected additional work is not yet authorized. |
| 24 | MSG24 | In line | Unapproved additional work | Additional work requires an approved change. Recording actual spending does not approve it. |
| 25 | MSG25 | Toast | Work order closed | Accepted and cost-reconciled work order closed; source inspection history is preserved. |
| 26 | MSG26 | In line | Required credential/compliance missing | Provide and review the documents applicable to this activity. Internal approval cannot waive required legal authorization. |
| 27 | MSG27 | Toast | Credential internal verification | Credential review recorded. This is an internal record, not a government-issued authorization. |
| 28 | MSG28 | In line | Public airspace warning | A possible restriction is indicated. Verify current applicable authority permission; this lookup is not a flight permit. |
| 29 | MSG29 | Toast | Subscription billing reference saved | Enterprise subscription billing record saved. This record is not automatically a statutory tax invoice. |
| 30 | MSG30 | Toast | Report returned | Report returned to its designated author with review reasons. |
| 31 | MSG31 | In line | Independent reviewer missing | Assign a qualified accepting reviewer who is not the author or a member of the executing team. |
| 32 | MSG32 | Under field | Preparation/checklist incomplete | Complete the component shot-list and applicable safety/compliance records before requesting readiness approval. |
| 33 | MSG33 | In line | Source records changed | Relevant source data changed. Previous generation/review confirmations are no longer sufficient. |
| 34 | MSG34 | Toast | Scope/budget baseline approved | Scope and estimate version approved. The original baseline is preserved. |
| 35 | MSG35 | Toast | Enterprise payment confirmed | Authorized subscription payment confirmation recorded for the selected 1/6/12-month period. |
| 36 | MSG36 | In line | Missing pair at asset creation | Select one responsible Inspector and one identified own-organization Drone. |
| 37 | MSG37 | In line | Expired/revoked readiness basis | Cannot start this session. Review current assignment, plan, required permits and credential validity. |
| 38 | MSG38 | Toast | Findings confirmed | Findings set confirmed by the assigned Inspector; ready for report drafting. |
| 39 | MSG39 | In line | LLM draft failure | Draft generation failed. Source records are saved; the responsible author can retry or prepare a manual draft. |
| 40 | MSG40 | In line | Missing maintenance lead/author | Assign one team lead and one accountable report author before release. |
| 41 | MSG41 | In line | Unpriced/unsupported cost | Record the price basis and supporting reference. Unknown cost cannot be silently treated as zero. |
| 42 | MSG42 | Toast | Team reports completion | Work reported complete by the team. Independent acceptance and cost reconciliation are still required. |
| 43 | MSG43 | In line | Repair completion proof missing | Attach required before/after evidence and acceptance-test records for the affected tasks. |
| 44 | MSG44 | In line | Self-acceptance attempted | Authors and executing team members cannot independently accept their own work. |
| 45 | MSG45 | In line | Cost reconciliation unresolved | Resolve missing, duplicate or unapproved costs and variance explanations before final closure. |
| 46 | MSG46 | Toast | Maintenance author submits report | Author-verified maintenance completion draft submitted for independent acceptance. |
| 47 | MSG47 | Toast | Subscription payment confirmed | The authorized settlement has been verified and the subscription is active. |
| 48 | MSG48 | In line | Online payment unavailable or failed | Online payment is unavailable or could not be verified. Use the corporate wire/invoice process or contact the Platform Manager for assistance. |

### 5.2 Appendix 2 - Common Requirements

- **Validation Rules**: Validate identifier existence, required fields, maximum length, allowable enum values, current workflow state, and active version numbers on every create, update, and decision action.
- **Tenant Authorization Scope**: Enforce organization tenancy, mission assignment, and designated leadership roles prior to executing database queries or file streaming; never filter authorization client-side.
- **Temporal Consistency**: Persist event timestamps as UTC instants; display formatted times in user or enterprise configured local timezones. Regulatory validity periods evaluate explicit start and expiration timestamps.
- **Deterministic Currency & Math**: Financial values (estimates, actuals, variance) use decimal representations with explicit currency (VND) and standard rounding conventions; avoid IEEE 754 floating-point errors.
- **Standardized API Structure**: Successful JSON responses return `{ success, message, data }`; bodyless responses use HTTP `204`. Error responses implement the RFC 9457 Problem Details specification with machine-readable codes and unique trace IDs.
- **Privacy & Security Masking**: Authentication failures provide generic messages without disclosing user account existence. Error traces do not reveal sensitive file paths, credentials, or cross-tenant records.
- **File Validation & Antivirus**: Uploaded media are checked for MIME type integrity, valid magic bytes, and allowed file sizes prior to persistence.
- **Idempotency Protection**: Key transactional commands—including periodic generation, evidence upload, mission dispatch, report publication, and work order closure—are state-guarded and idempotent.
- **Cryptographic Traceability**: All report deliverables and visual evidence store server-calculated SHA-256 digests, supporting non-repudiation and tamper detection.

### 5.3 Appendix 3 - Scope and Technology Constraints

- **Multi-Tenant Architecture**: The system operates as an Enterprise SaaS platform isolating multiple infrastructure-owning organizations within a unified database schema using tenant foreign key discriminators.
- **Separation of Flight Control**: The platform is an information and decision management system; it does not connect to drone flight controllers, execute autopilot routes, or transmit remote-control telemetry.
- **Human Accountability for AI**: Automated computer vision (YOLO11s) and generative language models (LLM) provide advisory suggestions and draft texts. All defect findings, report deliverables, and maintenance closures require attributable human approval.
- **Technology Stack Specifications**:
  - *Backend*: Java 21, Spring Boot 3, Spring Data JPA, Spring Security, Flyway database migration, OpenHTMLtoPDF.
  - *Database & Storage*: PostgreSQL 17 with `pgvector` extension; MinIO S3-compatible distributed object storage.
  - *Web Client*: React 19, TypeScript, Material-UI (MUI), Vite, TanStack React Query.
  - *Mobile Client*: Flutter 3, Dart, Riverpod state management.
  - *Optional Payment Gateway*: PayPal REST API v2 (Orders v2 & Webhooks), enabled by deployment configuration only; secrets supplied through environment configuration, with no online checkout when disabled.
  - *AI Services*: Python 3.11, FastAPI, Ultralytics YOLO11s (MBDD2025 dataset), OpenAI-compatible LLM gateway.

### 5.4 Feature and Flow Traceability

This traceability matrix maps the eight core product features (`FE-01` to `FE-08`) to system use cases and operational responsibilities across the platform lifecycle.

| Product Feature | Operational Responsibility | Supported Use Cases |
| --- | --- | --- |
| FE-01 | Identity, tenant governance, workforce accounts, credentials, versioned terms, and subscription settlement | UC-01, UC-02, UC-03, UC-05 |
| FE-02 | Infrastructure asset inventory, owned and B2B leased drone fleet management, and flight permit linkage | UC-04, UC-06, UC-07, UC-08 |
| FE-03 | Inspection mission planning, shot-list preparation, and flight readiness authorization | UC-09, UC-10, UC-11 |
| FE-04 | Field survey logging and digital evidence intake | UC-12, UC-13, UC-14 |
| FE-05 | Advisory YOLO11s defect detection and human findings verification | UC-15, UC-32 |
| FE-06 | Context-grounded report drafting, administrative review, publication, and maintenance handoff | UC-16, UC-17, UC-18, UC-19, UC-20, UC-21 |
| FE-07 | Maintenance work orders, cost estimation, change control, repair logs, and acceptance | UC-23, UC-24, UC-25, UC-26, UC-27, UC-28, UC-29, UC-30, UC-31 |
| FE-08 | Role-tailored dashboards, analytical metrics, notifications, and operational audit trail | UC-22, UC-32 |

### 5.5 Appendix 4 - Research Basis and References

The system requirements incorporate industry standards, civil aviation regulations, and established asset management methodologies:

- **Non-Destructive Testing & Inspection Reporting:** Incorporates American Society for Nondestructive Testing (ASNT) guidelines regarding reproducible inspection techniques, explicit equipment and methodology disclosure, and attributable technician accountability. Visual capture annotations follow Pix4D inspection reporting benchmarks.
- **Maintenance Lifecycle & Work Order Governance:** Maintenance workflows reflect standards from enterprise asset management benchmarks (Oracle PeopleSoft Maintenance Management, IBM Maximo), distinguishing physical task completion from formal administrative and financial closure.
- **Cost Estimation & Engineering Change Control:** Engineering change orders follow established principles from construction and plant engineering (Primavera Unifier), enforcing itemized cost baselines, explicit change justification, and independent budget approval.
- **Artificial Intelligence Governance:** AI defect detection and report drafting comply with National Institute of Standards and Technology (NIST AI 600-1) recommendations on generative artificial intelligence risk management, ensuring source-grounded synthesis and mandatory human oversight.
- **Civil Aviation Regulations:** Drone compliance references Vietnamese Government Decree No. 288/2025/NĐ-CP governing the management of unmanned aerial vehicles and other flying craft, enforcing flight permit verification and remote pilot credential tracking.

#### Document References

- [1] ASNT Pulse. *Nondestructive Testing Report Writing: Back to Basics*. American Society for Nondestructive Testing. https://www.asnt.org/standards-publications/blog/nondestructive-testing-report-writing-back-to-basics
- [2] Oracle Corporation. *PeopleSoft Maintenance Management Process Flow*. Oracle Help Center. https://docs.oracle.com/en/applications/peoplesoft/financials-and-supply-chain-management/9.2.056/peoplesoft-maintenance-management/peoplesoft-maintenance-management-process-flow.html
- [3] IBM Corporation. *Maximo Manage: Work Order Statuses*. IBM Documentation. https://www.ibm.com/docs/en/maximo-manage/cd?topic=orders-work-order-statuses
- [4] Oracle Corporation. *Primavera Unifier: Change Order Business Process*. Oracle Help Center. https://docs.oracle.com/en/industries/construction-engineering/primavera-unifier/26/accelerator-user/changeorderbusinessprocess-10296629a.html
- [5] National Institute of Standards and Technology. *Artificial Intelligence Risk Management Framework: Generative Artificial Intelligence Profile (NIST AI 600-1)*. U.S. Department of Commerce. https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf
- [6] Chính phủ nước Cộng hòa Xã hội Chủ nghĩa Việt Nam. *Nghị định số 288/2025/NĐ-CP: Quy định về quản lý tàu bay không người lái và phương tiện bay khác*. Cổng Thông tin điện tử Chính phủ. https://vanban.chinhphu.vn/?docid=215810&pageid=27160
- [7] Pix4D. *Annotations Report - PIX4Dcloud Pro*. Pix4D Support. https://support.pix4d.com/hc/en-us/articles/13552115283613
- [8] Oracle Corporation. *Understanding Work Orders in Maintenance Management*. Oracle Documentation. https://docs.oracle.com/cd/G47724_01/fscm92pbr55/eng/fscm/fwkm/UnderstandingWorkOrders-c9f12c.html
