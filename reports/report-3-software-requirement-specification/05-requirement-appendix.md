---
title: "Report 3 - Requirement Appendix"
document_type: report3-srs-section
weight: 55
source: "report3-software-requirement-specification.docx"
---

## 5. Requirement Appendix

### 5.1 Business Rules

The system enforces 49 normative business rules across multi-tenant isolation, aviation compliance, advisory AI oversight, report immutability, and maintenance cost control:

| ID | Rule Definition |
| --- | --- |
| BR-01 | Platform Admin and Platform Manager accounts are platform-scoped (platform-scoped) and enforce strict single-role separation of duties (Platform Admin and Platform Manager are mutually exclusive); Organization Manager, Inspector, and Maintenance Engineer accounts are scoped strictly to their respective enterprise tenant. |
| BR-02 | An Organization Manager can access and manage only the assets, resources, inspections, reports, and maintenance records belonging to their own enterprise organization. |
| BR-03 | Workforce identities belong to a single enterprise tenant; no user account or operational role can bridge across organization boundaries. |
| BR-04 | Inspectors and Maintenance Engineers can access and act only upon inspection missions, work orders, or repair tasks explicitly assigned to them. |
| BR-05 | Active user accounts and unexpired self-declared pilot licenses are mandatory for flight readiness; expired pilot licenses automatically block the self-service flight permit gate. |
| BR-06 | Enterprise tenant registration, identity management, subscription activation, and drone equipment leasing serve as supporting governance gates for the primary inspection and maintenance lifecycle. |
| BR-07 | Flight session start requires an unexpired flight permit and a mandatory pre-flight safety checklist note confirming aircraft, battery, and environmental suitability. |
| BR-08 | Self-service flight readiness verifies the uploaded flight permit and pilot license currency; software approvals do not grant governmental flight exemptions. |
| BR-09 | Inspection scheduling directly specifies the active Inspector and Drone for the mission, checking for scheduling conflicts across active missions. |
| BR-10 | ENTERPRISE subscriptions offer fixed standard pricing for 1-, 6-, and 12-month periods; custom 1–120-month durations and customer price proposals remain pending until a Platform Manager confirms a final amount and reconciled payment. Online PayPal checkout is used only for platform-approved subscription and lease amounts. |
| BR-11 | Subscription and drone equipment lease requests preserve versioned terms and actor attribution; entitlement or leased drone provisioning begins only after authorized payment confirmation. Online PayPal payments are verified by the system before activating the subscription or drone lease, and duplicate payment notifications are ignored. |
| BR-12 | Report drafts, cost estimate baselines, scope change requests, and approval decisions preserve complete version histories; published records cannot be modified in place. |
| BR-13 | Subscription renewal, cancellation, and expiration follow transparent contractual terms; subscription expiration preserves historical business records and does not auto-complete open work. |
| BR-14 | Remote pilots and Inspectors must record session postponement or abort whenever adverse weather or site conditions compromise flight safety. |
| BR-15 | Inspections are dispatched directly to the designated Inspector and transition to `Ready for Flight` upon the Inspector's flight permit upload. |
| BR-16 | Aircraft flight operation and physical structural repair are real-world technical actions; system Start and End commands represent software session logging, not hardware actuation. |
| BR-17 | Uploaded digital evidence retains an upload timestamp, file identity, and original capture metadata; missing telemetry is explicitly noted. |
| BR-18 | Duplicate evidence files within the same inspection scope are rejected based on sanitized filename matching. |
| BR-19 | Absence of GPS coordinates or camera telemetry is recorded as missing metadata and does not automatically invalidate otherwise suitable visual evidence. |
| BR-20 | AI vision detections remain unconfirmed candidates until reviewed by a qualified Inspector; only human-verified findings enter the official inspection record. |
| BR-21 | Rejected AI defect suggestions are excluded from official defect metrics, inspection report deliverables, and maintenance repair scopes. |
| BR-22 | Inspectors may record manual defect findings backed by capture evidence; unavailability of AI services does not prevent manual inspection reporting. |
| BR-23 | The assigned Inspector is responsible for reviewing evidence coverage, authoring coverage/limitation disclosures, and verifying every authored section of the inspection report before submission. |
| BR-24 | An Organization Manager distinct from the report author reviews findings and approves report publication; lack of independent review blocks publication. |
| BR-25 | Draft, returned, and unverified inspection content remains restricted to assigned authors and reviewers, strictly separated from published documents. |
| BR-26 | Published inspection report versions are immutable; subsequent corrections require creating a new linked revision with renewed administrative approval. |
| BR-27 | System workflows require explicit, attributable human decisions; no automated timer-based or silence-based approval is permitted for report publication or maintenance acceptance. |
| BR-28 | A returned inspection or maintenance report is directed back to its designated author with mandatory review comments while preserving prior version history. |
| BR-29 | Platform Admin provides technical Platform governance, platform user provisioning, and standard asset category maintenance, while Platform Manager governs commercial subscription and drone equipment lease settlements; neither holds authority over customer engineering assessments or repair budgets. |
| BR-30 | Application workflow approvals represent auditable software authorizations and do not constitute certified statutory signatures or governmental safety warranties. |
| BR-31 | Maintenance work orders must reference at least one confirmed defect requiring repair from a published inspection report within the same organization. |
| BR-32 | The designated Maintenance Team Lead prepares itemized repair estimates; automated systems do not generate arbitrary labor rates, material quantities, or prices. |
| BR-33 | Maintenance warranty and defect follow-up terms apply only when explicitly specified and contracted; no universal statutory warranty is presumed. |
| BR-34 | Any increase in repair scope, cost, or delivery schedule requires an approved Change Request prior to executing the additional work; the initial baseline remains immutable. |
| BR-35 | Maintenance completion reports require paired before-and-after photographic evidence and documented test results for each repaired defect. |
| BR-36 | Repair cost is an internal tenant cost register, separate from software subscription and drone equipment lease billing; PayPal online payment processes Enterprise platform subscriptions and drone leases, while internal repair actuals are operational expenditures. |
| BR-37 | A separate re-inspection creates a new linked inspection mission; additional field coverage required for an existing inspection can be initiated directly via an additional field session in MF2. |
| BR-38 | All assignment, readiness, finding verification, report publication, budget approval, and acceptance actions are logged in an immutable audit trail. |
| BR-39 | Direct URL access, notification links, and raw file paths confer no authority; backend multi-tenant boundary checks and role verifications remain mandatory on every request. |
| BR-40 | Password resets, role modifications, and session revocations immediately invalidate active tokens; user reassignment terminates future permissions without altering past audit logs. |
| BR-41 | Owned and leased drone equipment records include government registration numbers and expiration dates. Pilot licenses are self-declared in inspector user profiles. Mission flight permits are uploaded per inspection. |
| BR-42 | Asset registration defines standardized structural inspection checkpoints  inherited across inspections for on-site field survey guidance and technical reporting. |
| BR-43 | The assigned Inspector holds sole authority to evaluate evidence completeness and quality; automated technical upload checks do not replace human quality review. |
| BR-44 | The inspection workflow follows a strict sequential gate: Evidence Intake → AI Defect Detection → Findings Confirmation → Report Draft Synthesis → Author Verification → Organization Manager Approval → Publication. |
| BR-45 | Each maintenance work order designates an approved engineering team, exactly one Team Lead, and one Report Author; neither may perform final acceptance on their team's work. |
| BR-46 | Every repair task is allocated to an approved team member; the Team Lead manages task assignments within approved membership, with all changes audited. |
| BR-47 | Financial totals for budgets, change orders, and actual expenditures are calculated using exact decimal precision; missing item costs cannot default to zero. |
| BR-48 | Automated language models synthesize report drafts exclusively from verified source records, preserving uncertainty disclosures and preventing fabricated assertions. |
| BR-49 | The designated Report Author verifies and submits the maintenance completion report; an independent Organization Manager performs final technical acceptance. |

### 5.2 Common Requirements

- **Form Validation**: All input forms validate required fields, text length limits, numeric bounds, valid date ranges, and current workflow status before saving changes.
- **Organization & Role Access Checks**: Every screen and action verifies the signed-in user's role, organization membership, and mission/task assignment on the server.
- **Date, Time & Timezone Display**: Dates and times are stored consistently and displayed in the organization's or user's local timezone.
- **Currency & Cost Precision**: All subscription prices, drone lease rates, repair estimates, change orders, and actual costs are calculated to two decimal places with explicit currency labels (`USD` or `VND`).
- **File Upload Limits**: Uploaded images and PDF documents are checked for valid file format and size (up to `10 MB` per file and `20 MB` per upload batch).
- **Duplicate Prevention**: Repeated clicks or network retries on schedule generation, file upload, payment confirmation, or notification delivery are safely deduplicated so duplicate records are never created.
- **Document Integrity**: Published PDF inspection reports, maintenance completion reports, and asset engineering documents are locked upon publication so they cannot be altered in place.

### 5.3 Application Messages List

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

### 5.4 Other Requirements

#### 5.4.1 Scope and Operational Constraints
- **Multi-Tenant Workspace Isolation**: Each customer organization operates in an isolated workspace where its users, assets, drones, inspections, reports, and maintenance work orders are separated from all other organizations.
- **No Direct Drone Flight Control**: The platform manages planning, compliance documents, field logs, photos, reports, and maintenance workflows; physical drone piloting is performed by licensed pilots using their aircraft flight controllers.
- **Human-in-the-Loop AI Governance**: AI defect detection (`YOLO11`), AI report drafting, and AI repair scope suggestions are decision-support tools. Every finding, report, and maintenance budget requires explicit human review and approval.

#### 5.4.2 Feature and Flow Traceability

This traceability matrix maps the twelve core product features (`FE-01` to `FE-12`) to system use cases and operational responsibilities across the platform lifecycle.

| Product Feature | Feature Name | Operational Responsibility & Owner | Supported Use Cases |
| :---: | --- | --- | --- |
| `FE-01` | Authentication & Access Control | Organization self-registration, Web/Mobile sign-in, session security, and 5-role access control *(Trần Tùng Bách)* | UC-01, UC-02, UC-32 |
| `FE-02` | Workforce & Subscription Management | Workforce account management, pilot license profile, and Enterprise Subscription billing via bank transfer & PayPal *(Trần Hoàng Trung Hiếu)* | UC-02, UC-03, UC-05 |
| `FE-03` | Asset & Drone Fleet Management | Asset catalog, inspection checkpoints, reference documents, owned drones, and Drone Equipment Leasing *(Trần Hoàng Trung Hiếu)* | UC-04, UC-06 |
| `FE-04` | Recurring Schedule & Notifications | Timezone-anchored recurring inspection schedules, upcoming mission generation, and in-app notifications *(Trần Hoàng Trung Hiếu)* | UC-07, UC-22 |
| `FE-05` | Mission Dispatch & Airspace Advisory | One-off mission scheduling, resource conflict checking, and interactive Vietnam Airspace & No-Fly Zone Map *(Phùng Trung Quốc)* | UC-07, UC-08, UC-12 |
| `FE-06` | Flight Readiness & Field Execution | Self-service flight permit upload (`Ready for Flight`) and Web/Mobile on-site field flight sessions *(Phùng Trung Quốc)* | UC-09, UC-10, UC-11 |
| `FE-07` | Operational Dashboard & Schedule Calendar | Multi-role operational analytics dashboards, Inspector Schedule Calendar, dark mode, and EN/VI localization *(Phùng Trung Quốc)* | UC-22, UC-32 |
| `FE-08` | Evidence Management & AI Defect Detection | Inspection photo upload, camera time/GPS reading, `YOLO11` visual defect detection, and human finding confirmation *(Trần Tùng Bách)* | UC-13, UC-14, UC-15 |
| `FE-09` | Inspection Reporting & Publication | AI-assisted & manual report drafting, independent review, official PDF report publication, and maintenance handoff *(Trần Tùng Bách)* | UC-16, UC-17, UC-18, UC-19, UC-20, UC-21 |
| `FE-10` | Maintenance Planning & AI Scope Advisory | Forwarded defect triage, standards-based AI Repair Scope Advisor (`TCVN`/`EN`/`ISO`), and team/task assignment *(Trương Thái Như)* | UC-23, UC-24, UC-26 |
| `FE-11` | Cost Estimation & Repair Execution | Itemized cost estimation, independent budget approval, Change Orders, and Web/Mobile field repair work log verification *(Trương Thái Như)* | UC-25, UC-26, UC-27, UC-28, UC-29 |
| `FE-12` | Maintenance Acceptance & Cost Closure | Author-verified completion report PDF, independent technical acceptance, actual cost reconciliation, and work order closure *(Trương Thái Như)* | UC-30, UC-31, UC-32 |

#### 5.4.3 Research Basis and References

- **Non-Destructive Testing & Inspection Reporting:** Incorporates American Society for Nondestructive Testing (ASNT) guidelines regarding reproducible inspection techniques, explicit equipment and methodology disclosure, and attributable technician accountability. Visual capture annotations follow Pix4D inspection reporting benchmarks.
- **Maintenance Lifecycle & Work Order Governance:** Maintenance workflows reflect standards from enterprise asset management benchmarks (Oracle PeopleSoft Maintenance Management, IBM Maximo), distinguishing physical task completion from formal administrative and financial closure.
- **Cost Estimation & Engineering Change Control:** Engineering change orders follow established principles from construction and plant engineering (Primavera Unifier), enforcing itemized cost baselines, explicit change justification, and independent budget approval.
- **Artificial Intelligence Governance:** AI defect detection and report drafting comply with National Institute of Standards and Technology (NIST AI 600-1) recommendations on generative artificial intelligence risk management, ensuring source-grounded synthesis and mandatory human oversight.
- **Civil Aviation Regulations:** Drone compliance references Vietnamese Government Decree No. 288/2025/NĐ-CP governing the management of unmanned aerial vehicles and other flying craft, enforcing flight permit verification and remote pilot credential tracking.

- [1] ASNT Pulse. *Nondestructive Testing Report Writing: Back to Basics*. American Society for Nondestructive Testing. https://www.asnt.org/standards-publications/blog/nondestructive-testing-report-writing-back-to-basics
- [2] Oracle Corporation. *PeopleSoft Maintenance Management Process Flow*. Oracle Help Center. https://docs.oracle.com/en/applications/peoplesoft/financials-and-supply-chain-management/9.2.056/peoplesoft-maintenance-management/peoplesoft-maintenance-management-process-flow.html
- [3] IBM Corporation. *Maximo Manage: Work Order Statuses*. IBM Documentation. https://www.ibm.com/docs/en/maximo-manage/cd?topic=orders-work-order-statuses
- [4] Oracle Corporation. *Primavera Unifier: Change Order Business Process*. Oracle Help Center. https://docs.oracle.com/en/industries/construction-engineering/primavera-unifier/26/accelerator-user/changeorderbusinessprocess-10296629a.html
- [5] National Institute of Standards and Technology. *Artificial Intelligence Risk Management Framework: Generative Artificial Intelligence Profile (NIST AI 600-1)*. U.S. Department of Commerce. https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf
- [6] Chính phủ nước Cộng hòa Xã hội Chủ nghĩa Việt Nam. *Nghị định số 288/2025/NĐ-CP: Quy định về quản lý tàu bay không người lái và phương tiện bay khác*. Cổng Thông tin điện tử Chính phủ. https://vanban.chinhphu.vn/?docid=215810&pageid=27160
- [7] Pix4D. *Annotations Report - PIX4Dcloud Pro*. Pix4D Support. https://support.pix4d.com/hc/en-us/articles/13552115283613
- [8] Oracle Corporation. *Understanding Work Orders in Maintenance Management*. Oracle Documentation. https://docs.oracle.com/cd/G47724_01/fscm92pbr55/eng/fscm/fwkm/UnderstandingWorkOrders-c9f12c.html
