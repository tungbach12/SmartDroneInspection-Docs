---
title: "Report 3 - Requirement Appendix"
document_type: report3-srs-section
weight: 55
source: "report3-software-requirement-specification.docx"
---

## 5. Requirement Appendix

### 5.1 Business Rules

The following rules govern the building-inspection service. Rule identifiers are referenced from §3 and from the test cases in Report 5.

| ID | Rule Definition |
| --- | --- |
| BR-01 | `ADMIN` and `MANAGER` perform platform responsibilities. `CUSTOMER` acts within its own organization; `INSPECTOR` acts as a partner and may serve customer organizations only through authorized dispatch. |
| BR-02 | A `CUSTOMER` accesses and manages only its own organization's buildings, service requests, published inspection reports, and payment records. |
| BR-03 | A `MANAGER` may view request details, messages, and commercial data only for requests they hold. An unassigned request is visible as a queue summary until claimed. |
| BR-04 | An `INSPECTOR` may act only on inspection occurrences assigned to them. |
| BR-05 | A `MANAGER` assigned to a request cannot be acted on by another Manager. Reassignment and unassignment are `ADMIN` actions and are recorded in the audit trail. |
| BR-06 | Customer onboarding and asset creation screen building locations against airspace information. Prohibited (`NO_FLY_ZONE`) locations are rejected; restricted (`RESTRICTED_ZONE`) locations emit an amber `MSG28` flight-permit advisory warning while allowing immediate activation and saving. Screening does not grant governmental flight clearance. |
| BR-07 | Only buildings are in scope. A registration for another infrastructure domain cannot be represented, because the category catalogue contains building categories only. |
| BR-08 | Partner admission does not require drone ownership. An Inspector application requires a nonblank licence number, a recognized licence class, an uploaded licence scan, and a future expiry. |
| BR-09 | An Inspector account is created only after a platform reviewer approves the application. A rejected application creates no account and records a reason. |
| BR-10 | Inspectors must hold current pilot credentials for flight assignment and field work. An expired credential prevents assignment and session start, and triggers a flag and notice rather than a silent expiry. |
| BR-11 | An Inspector-owned drone requires at least one photograph, structured outdoor flight capabilities, and the documents configured by `ADMIN`. Registration and ownership documents are required by default; the technical-inspection document is enabled by administrator configuration. |
| BR-12 | Drone weight is classified into the five categories of Article 4 of Decree 288/2025/ND-CP. An airframe at 2.0 kg or above requires a recognized Class B pilot licence. Unknown weight or unrecognized class fails eligibility, and Class A applies only to known airframes below 2.0 kg. |
| BR-13 | A drone is eligible only while its serviceability is active and its registration number, evidence file, and expiry are present and current for the planned flight start. Expiry affects eligibility; it does not by itself imply an automatic stored serviceability change. Inspectors may switch owned non-suspended drones between `ACTIVE`, `MAINTENANCE`, and `RETIRED` (retire/reactivate), while retired drones cannot submit renewal applications while retired. |
| BR-14 | Service quotations are stated in VND per occurrence, identify scope and timing, and are associated with an eligible Inspector and a drone owned by that Inspector. |
| BR-15 | A service request proceeds through request, quotation, Customer acceptance, signed agreement, and occurrence assignment. Dispatch requires the signed agreement to have been recorded by a Manager. |
| BR-16 | Acceptance of a quotation locks the agreed terms and stores an immutable snapshot. An accepted quotation cannot be revised; a change requires a new agreement. |
| BR-17 | A recurring request uses a monthly interval of 1 to 120 months and must resolve to between 2 and 100 occurrences. The Customer-requested first date is the schedule anchor and cannot be shifted by the Manager. |
| BR-18 | The first requested inspection date is at least 20 calendar days ahead in `Asia/Ho_Chi_Minh` business time. This is an internal scheduling policy, not a statutory deadline. |
| BR-19 | Before a recurring quotation is saved or accepted, and before occurrences are materialized, the selected Inspector's licence and drone registration must remain valid at every planned occurrence start. A failure rejects the operation without creating partial occurrence records. |
| BR-20 | A recurring agreement covers the occurrences within its stated term. Each occurrence still requires its own assignment, readiness review, inspection, reporting, and settlement. |
| BR-21 | Inspection assignment and reassignment consider overlapping commitments across customer organizations so that an Inspector or drone is not double-booked. |
| BR-22 | Assignment, rescheduling, reassignment, permit upload, and session start each revalidate the applicable credentials against the relevant planned time. Eligibility fails closed on unknown or incomplete data. |
| BR-23 | Before starting an on-site field session the assigned Inspector must have a valid, effective inspector-uploaded flight permit whose validity covers the actual flight time and whose drone serial matches, hold current credentials, and record a pre-flight safety note. |
| BR-24 | **SUPERSEDED** (2026-11-23) — inspector self-attestation replaces independent verification. Formerly: every flight permit entered pending review regardless of the building's airspace classification; verification required approval or a reasoned rejection by a distinct Manager or Administrator, and a submitter could not verify their own permit. Now a valid upload is effective immediately and no Manager/Admin approval or rejection step exists. |
| BR-25 | Changing the assigned drone, or rescheduling outside the permit window, invalidates the permit and requires the assigned Inspector to re-upload a valid permit. Permit uploads are locked once the occurrence leaves the scheduled state. |
| BR-26 | Airspace checks and permit records support internal readiness review only; they do not grant government aviation authorization. |
| BR-27 | Field sessions record completion or abort. An abort requires a reason and alerts a Manager to reschedule, reassign, or cancel the dispatch. |
| BR-28 | A flight trace may come from live telemetry, an imported log, or an accountable manual declaration. Absent source values are shown as unavailable and are never fabricated, and a manual declaration is never presented as measured telemetry. |
| BR-29 | Inspection progress distinguishes scheduled, active field work, field completion, report review, completion, and cancellation. Readiness is not evidence of governmental clearance. |
| BR-30 | Aircraft operation is a real-world action performed by qualified people. The service does not actuate aircraft and does not receive flight commands from the platform. |
| BR-31 | Inspection evidence retains its identity, upload time, and available capture information. Missing metadata is disclosed rather than invented. |
| BR-32 | A duplicate evidence filename is disambiguated with a sequential suffix and reported to the Inspector rather than rejecting the upload or overwriting an existing record. |
| BR-33 | Missing GPS or camera metadata does not automatically invalidate otherwise suitable evidence; the absence remains apparent to reviewers. |
| BR-34 | Candidate defect suggestions remain advisory until the assigned Inspector confirms, edits, or rejects them. Only human-confirmed findings are official. |
| BR-35 | Rejected and unconfirmed suggestions are excluded from the official findings and from inspection reports. |
| BR-36 | An Inspector may record a manual finding supported by evidence. A model-produced confidence value is never invented for a manual finding, and manual review remains possible when automated analysis is unavailable. |
| BR-37 | After confirming the findings baseline, the report author explicitly prepares and submits the report. Visiting a screen does not submit it. |
| BR-38 | A `MANAGER` distinct from the report author independently reviews the report and either publishes it or returns it with reasons (`ADMIN` retains read-only access only). An Inspector cannot review or publish their own report. |
| BR-39 | Customers may follow inspection progress but cannot access internal field records, unconfirmed findings, or unpublished reports as official deliverables. |
| BR-40 | Published inspection reports are preserved. Corrections are issued as new versions and prior versions remain available. Publication is not governmental or professional certification. |
| BR-41 | Commercial and reporting approvals require explicit, attributable human decisions. Silence or the passage of time is not approval. |
| BR-42 | Returning a report requires review reasons, preserves the prior version, and returns it to its author for revision. |
| BR-43 | The AI-drafted report summary is advisory and must remain visibly distinguished from confirmed findings. Official report sections are assembled deterministically from confirmed records rather than model-generated text. |
| BR-44 | When a Customer accepts a published report, the applicable service fee becomes due. The official deliverable is released according to the agreed payment rule after confirmation. |
| BR-45 | A payment is settled only after its gateway callback signature is verified or an authorised confirmation is recorded. An unsettled payment cannot be presented as settled. |
| BR-46 | Verified customer payment makes the Inspector payout eligible but does not record disbursement. A Manager records the actual payout with its external reference and actor attribution. |
| BR-47 | Non-online unresolved payment orders (`MANUAL_WIRE`) cannot be overwritten when starting online checkout until resolved; unpaid online gateway orders (`SEPAY`/`VNPAY`) auto-release when switching gateways or retrying VNPay, and any late or superseded gateway callbacks are recorded in `gateway_inbound_transactions` for reconciliation without double-settling. |
| BR-48 | A refund is initiated before any external transfer, holds the unpaid payout, and reserves the amount against the captured payment. Completion occurs only after the transfer, with an allocation that sums exactly to the transferred amount. |
| BR-49 | Cumulative completed plus pending refunds cannot exceed the captured payment. A pending refund may be cancelled only if no transfer occurred, with a recorded reason. |
| BR-50 | A refund against an already-disbursed payout leaves the historical payout immutable and creates a separately attributable Inspector receivable. The system never automatically offsets future payouts. |
| BR-51 | Important onboarding, application review, quotation acceptance, agreement recording, partner assignment, field abort, findings confirmation, report publication, and payment decisions are attributable to the responsible actor. Permit upload is attributable to the assigned Inspector; the former "permit verification" clause is **SUPERSEDED** (2026-11-23) because no Manager/Admin verification step exists. |
| BR-52 | A direct link, notification, or document reference does not grant access. Role, organization, assignment, and payment rules apply to each access attempt. |
| BR-53 | Password, role, account, and session changes take effect for active access without removing historical attribution. |
| BR-54 | Infrastructure outside the building domain, corrective maintenance execution, aircraft control, and three-dimensional reconstruction are out of application scope. Re-inspection of previously confirmed defects is in scope and reuses the dispatch, field, and reporting flows. |
| BR-55 | `DroneKnowledgeAI` advisory retrieval is in scope: recommendations are strictly isolated to the current customer organization plus anonymized benchmark cases, with the current inspection excluded from matching itself. Retrieval uses semantic vector similarity with an automatic keyword-matching fallback, and all recommendations remain advisory and human-confirmed. Confirmed findings are indexed automatically at report publication. A corrective-maintenance repair knowledge base, external CMMS integration, and work-order execution are out of scope. |

### 5.2 Common Requirements

- **Form validation.** Forms explain required information and reject incomplete, invalid, out-of-range, or inconsistent input.
- **Role, organization, and assignment checks.** Each action is limited by role, organization, partner relationship, and assignment. Screen visibility does not imply authority.
- **Date, time, and timezone display.** Dates and times are clear in the relevant organization's or schedule's timezone, and important decisions are attributable.
- **Currency and financial precision.** Service quotations, applicable taxes, and fees state their currency and are calculated consistently. Quotations are stated in VND.
- **Evidence and document handling.** Inspection media, agreements, qualification records, and reports are validated and shown only to authorized users.
- **Idempotent user actions.** Retries do not create duplicate occurrences, evidence records, payments, or lifecycle notices.
- **Document integrity and version history.** Signed agreements and published inspection reports are protected from unauthorized alteration. Changes are attributable and preserve history.
- **Bilingual display.** Every user-facing label is available in English and Vietnamese without changing route identifiers or authorization rules.

### 5.3 Application Messages List

| # | Message code | Message Type | Context | Content |
| --- | --- | --- | --- | --- |
| 1 | MSG01 | Inline | Search has no authorized records | No results found. |
| 2 | MSG02 | Under field | Required field empty | This field is required. |
| 3 | MSG03 | Under field | Configured length exceeded | Must not exceed {maxLength} characters. |
| 4 | MSG04 | Under field | Invalid email | Enter a valid email address. |
| 5 | MSG05 | Toast | Record created | Created successfully. |
| 6 | MSG06 | Toast | Record updated | Updated successfully. |
| 7 | MSG07 | Dialog | Versioned or irreversible action | Confirm this action and the version you are acting on. |
| 8 | MSG08 | Inline | Sign-in failed | Email or password is incorrect. |
| 9 | MSG09 | Inline | Disabled or unapproved account | Unable to sign in. Contact your administrator. |
| 10 | MSG10 | Inline | Expired access | Your session has expired. Sign in again. |
| 11 | MSG11 | Under field | Password policy failure | Password does not meet the security requirements. |
| 12 | MSG12 | Toast | Inspection dispatched | Inspection scheduled with its building and assigned partner. |
| 13 | MSG13 | Inline | Newer quotation or report version | A newer version is available. Refresh and review it before continuing. |
| 14 | MSG14 | Toast | Quotation or assignment accepted | Accepted successfully. |
| 15 | MSG15 | Under field | Rejection or abort lacks reason | Enter a reason before submitting. |
| 16 | MSG16 | Inline | Invalid file | This file cannot be uploaded. Check its type and size. |
| 17 | MSG17 | Inline | Duplicate evidence filename | This file name already exists in this inspection. It was saved as {suggestedName}. |
| 18 | MSG18 | Toast | Evidence received | Evidence is available for review. |
| 19 | MSG19 | Inline | Automated advisory unavailable | Automated guidance is unavailable. Continue with human review. |
| 20 | MSG20 | Toast | Inspection report submitted | Inspection report submitted for independent review. |
| 21 | MSG21 | Inline | Candidate findings remain unreviewed | Review all suggested findings before confirming the findings baseline. |
| 22 | MSG22 | Toast | Inspection report published | Approved inspection report published and available to the Customer. |
| 23 | MSG23 | Inline | Banned or unsupported infrastructure category | Only building categories can be registered. Select a building category. |
| 24 | MSG24 | Inline | Inspector application missing credentials | Provide a licence number, a recognized licence class, and a licence scan. |
| 25 | MSG25 | Toast | Inspector application decided | Application approved. The Inspector account has been created. |
| 26 | MSG26 | Inline | Required qualification or document missing | Provide all required qualification and supporting documents. |
| 27 | MSG27 | Toast | Compliance document recorded | Internal review does not replace statutory authorization. |
| 28 | MSG28 | Inline | Airspace alert | Location is within a prohibited area or requires review. |
| 29 | MSG29 | Toast | Request or quotation recorded | Service request or quotation saved. |
| 30 | MSG30 | Toast | Report returned | Returned to the author with review reasons. |
| 31 | MSG31 | Inline | Request already claimed | Another Manager has already claimed this request. |
| 32 | MSG32 | Under field | Safety note incomplete | Enter the required safety note before starting the field session. |
| 33 | MSG33 | Inline | Findings changed after report preparation | Confirm the findings and review the report before submitting it. |
| 34 | MSG34 | Inline | Attachment limit exceeded | A message supports up to five files, 10 MiB each and 20 MiB in total. |
| 35 | MSG35 | Toast | Signed agreement recorded | Signed service agreement recorded. |
| 36 | MSG36 | Inline | Partner or drone cannot be assigned | Select an eligible Inspector and an owned, approved, available drone. |
| 37 | MSG37 | Inline | Permit or qualification missing | Cannot start field work. Provide a valid mission permit uploaded by the assigned Inspector and current pilot credentials. |
| 38 | MSG38 | Toast | Findings baseline confirmed | Findings baseline confirmed. Prepare and submit the report for review. |
| 39 | MSG39 | Inline | Advisory summary unavailable | Automated summary is unavailable. Review confirmed findings directly. |
| 40 | MSG40 | Inline | No effective inspector-uploaded permit | No valid inspector-uploaded flight permit is in effect. Field work cannot start until the assigned Inspector uploads one. |
| 41 | MSG41 | Inline | Permit metadata outside planned window | The permit validity does not cover the planned inspection window. |
| 42 | MSG42 | Toast | Permit re-upload required | The permit was invalidated because the assigned drone or schedule changed. The Inspector must re-upload a valid permit. |
| 43 | MSG43 | Inline | Video still processing | The video is still being processed. Try again when it is ready. |
| 44 | MSG44 | Toast | Video processing failed | Video processing failed. Retry processing from the evidence panel. |
| 45 | MSG45 | Inline | Imported log unreadable | This flight log cannot be read or contains no position data. |
| 46 | MSG46 | Inline | Payment gateway unavailable | Payment is temporarily unavailable. Try again later. |
| 47 | MSG47 | Toast | Payment confirmed | Inspection service payment confirmed. |
| 48 | MSG48 | Inline | Payment required for deliverable | Accept the published report and complete the required payment to access the official deliverable. |
| 49 | MSG49 | Inline | Gateway order unresolved | An earlier payment attempt is unresolved. Resolve it before starting a new one. |
| 50 | MSG50 | Inline | Refund exceeds captured payment | The refund amount exceeds the captured payment or the remaining refundable amount. |

### 5.4 Other Requirements

#### 5.4.1 Scope and Operational Constraints

- **Building-only inspection domain.** The service inspects buildings. The category catalogue, inspection checkpoints, defect classes, and report template are all expressed for building structures and rooftop building assets. Non-building infrastructure is not supported.
- **Role and organization separation.** Platform responsibilities (`ADMIN`, `MANAGER`), customer responsibilities (`CUSTOMER`), and partner responsibilities (`INSPECTOR`) are separated by role, ownership, and assignment.
- **No direct aircraft control.** The service governs agreements, compliance documents, field sessions, evidence, analysis, inspection reports, and payment. Licensed partner pilots operate aircraft independently.
- **Human review of automated output.** Defect suggestions and report summaries are advisory. Official findings and published reports require explicit human confirmation.
- **Inspection knowledge retrieval in scope; corrective maintenance execution out of scope.** `DroneKnowledgeAI` advisory retrieval over engineering standards and tenant-isolated historical defect cases is part of the delivered inspection service (§3.18 / `FE-17`, `BR-55`). Repair planning, work orders, repair execution, maintenance cost closeout, a corrective-maintenance repair knowledge base, and external CMMS or work-order execution are outside the application. The Customer arranges corrective work externally. Re-inspecting previously confirmed defects is supported (`§3.25` / `FE-24`) and reuses the same dispatch, field-session, evidence, and reporting flows.
- **Data preservation.** Legacy maintenance tables and persisted rows are retained unchanged with no destructive migration, and are not exposed by the application.
- **Qualification and legal authority.** A service status or recorded document does not prove professional qualification or government flight clearance.

#### 5.4.2 Feature and Flow Traceability

This traceability matrix maps all twenty-four atomic product features (`FE-01` to `FE-24`) to their main flow, SRS section, operational responsibility, and supported use cases.

| Product Feature | Feature Name | Main Flow | SRS § | Operational Responsibility | Supported Use Cases |
| :---: | --- | :---: | :---: | --- | --- |
| `FE-01` | Account Authentication, OTP & 4-Role Access Control | `MF1` | §3.2 | Registration/login OTP, password lockout & IP rate limit, Google OAuth2, JWT refresh rotation, profile settings, and 4-role portal/API access boundaries | UC-01, UC-02, UC-03, UC-21 |
| `FE-02` | Partner Inspector Application & Qualification Management | `MF1` | §3.3 | Public partner Inspector application and licence scan, `MANAGER` approval/rejection & provisioning, `MANAGER` signed partner contract upload, licence renewals, and flight logs (`ADMIN` read-only view) | UC-02, UC-05 |
| `FE-03` | Inspector-Owned Drone Registration & Fleet Management | `MF1` | §3.4 | Admin-configurable drone document/feature rules, Inspector aircraft photos/capabilities/3-doc submissions, Decree 288 class gates, `MANAGER` approval/rejection (`ADMIN` read-only view), renewal & serviceability retire/reactivate | UC-02, UC-06 |
| `FE-04` | Interactive Location Map & No-Fly Zone Airspace Screening | `MF1` | §3.5 | Interactive Vietnam map coordinate picker across web and mobile and distance-based airspace zone evaluation (`Clear`, `Restricted`, `No-Fly`) blocking prohibited areas and warning on restricted areas | UC-03, UC-13 |
| `FE-05` | Financial History & Revenue/Payment Ledger | `MF4` | §3.6 | Role-scoped financial ledgers for `CUSTOMER`, `INSPECTOR`, and `MANAGER` tracking payments, commission, VAT, personal income tax, and net payouts | UC-18, UC-19, UC-20 |
| `FE-06` | Building Asset Registry, Checkpoints & Reference Documents | `MF2` | §3.7 | Six building-only categories, category-seeded checkpoints, dedicated plain-text ownership details, duplicate-free reference documents, and terminal retirement | UC-02, UC-04 |
| `FE-07` | Restricted Airspace Advisory Warning & Immediate Onboarding | `MF1` | §3.8 | `MSG28` amber permit advisory on `RESTRICTED_ZONE` coordinates (map picker, service request, asset overview) with immediate registration activation and removal of Admin airspace clearance queue | UC-03, UC-13 |
| `FE-08` | Service Requests (One-Time & Recurring) & VND Quotations | `MF2` | §3.9 | One-time/recurring requests (`>= 20`d lead time, `1–120`mo, `2–100` occurrences, concise titles), single Manager claim & immediate detail view, ADMIN assignment oversight, and streamlined VND quote UI | UC-07 |
| `FE-09` | Offline Signed Contract & Occurrence Dispatch Scheduling | `MF2` | §3.10 | Immutable quote acceptance snapshot, month-end anchored occurrence materialization, offline signed contract upload, cross-org partner dispatch, bulk crew assignment, and abort recovery | UC-08, UC-09 |
| `FE-10` | Dual-Channel Messaging (Order Chat & Inspection Chat) | `MF2` | §3.11 | Separated Customer–Manager commercial order chat and Customer–Inspector field mission chat with up to 5 verified attachments | UC-07, UC-09, UC-11 |
| `FE-11` | Assignment Acceptance Timeout & Escalation Handling | `MF2` | §3.12 | Configurable assignment acceptance deadline (`1–720`h, default `24`h) auto-cancelling unaccepted dispatches and notifying the owning Manager | UC-09, UC-20 |
| `FE-12` | System Notifications & Alert Center | `MF2` | §3.13 | Reliable deduplicated in-app notifications, unread counters, read-status tracking, and safe permission-respecting navigation links | UC-20 |
| `FE-13` | Flight Permit Upload & Inspector Self-Attestation Gate | `MF3` | §3.14 | Assigned-Inspector self-attested permit upload (`<= 25 MB`, validated document & metadata), effective immediately on validation with no Manager approval, session gate, re-upload on change, and Manager/Admin read-only audit view | UC-10 |
| `FE-14` | On-Site Field Session & SmartDroneHub MAVLink Telemetry | `MF3` | §3.15 | Detailed pre/post-flight safety checklists, accountable `Start` / `Complete` / reasoned `Abort` field sessions, multi-flight sorties, read-only `SmartDroneHub` live telemetry, log import, manual declaration, dashboards & calendar | UC-11, UC-12, UC-20 |
| `FE-15` | Field Evidence Intake & Chunked Video Processing Pipeline | `MF3` | §3.16 | Photo metadata extraction & normalization, resumable chunked MP4 uploads up to `2 GiB`, background playback transcoding, keyframe capture, duplicate filename numbering, and time-limited video playback | UC-14 |
| `FE-16` | AI Defect Detection (`YOLO11` + Vision Fallback) & Findings Confirmation | `MF3` | §3.17 | Automated building-defect detection with Vision fallback & user opt-out, `70%` default auto-confirm threshold, bounding boxes, status filter chips, and official baseline confirmation | UC-15 |
| `FE-17` | AI Case/Standard Retrieval (`pgvector` RAG), Note Drafting & Report Summary | `MF3` | §3.18 | Tenant-isolated historical-case & standard retrieval with keyword fallback, historical backfill, `Draft note with AI` / batch `Draft all notes`, summary references, and collapsible Mobile references | UC-15, UC-16 |
| `FE-18` | Inspection Report Compilation, Independent Review & Official Publication | `MF4` | §3.19 | Consistent fixed-section compilation from confirmed findings (`Submitted`, `Returned`, `Published`, `Superseded`), non-author Manager review/publication, and on-demand A4 PDF export | UC-16, UC-17 |
| `FE-19` | Customer Report Acceptance & Clarification Workflow | `MF4` | §3.20 | Owning-Customer deliverable review on Web and Mobile, explicit acceptance against published report version, Customer-only pre-acceptance clarification requests, and Customer/Manager Inspector rating against `ADMIN`-configured criteria | UC-18 |
| `FE-20` | Online Service Fee Payment (`Sepay` VietQR & `VNPay`) | `MF4` | §3.21 | Configuration-gated `Sepay` VietQR and `VNPay` checkout with verified payment gateway callbacks, unresolved order guards (`V67`–`V68`), and authorized manual settlement fallback | UC-18 |
| `FE-21` | Payment Deadlines, Invoices & Payment Document Management | `MF4` | §3.22 | Per-occurrence invoice rate snapshots, configurable payment due window (default 15 days), single overdue reminder without access revocation, and notice/receipt PDFs | UC-18, UC-20 |
| `FE-22` | Partner Inspector Payout Reconciliation | `MF4` | §3.23 | Explicit separation of payout eligibility on customer settlement from Manager-recorded disbursement (reference/timestamp), role masking, and payout holds | UC-19 |
| `FE-23` | Evidence-Backed Refunds & Receivable Recovery | `MF4` | §3.24 | Two-step refund lifecycle (hold unpaid payout -> external transfer -> balanced five-part allocation), legacy row reconciliation, and separate Inspector receivable recovery | UC-19 |
| `FE-24` | Post-Remediation Re-inspection & Defect Verification | `MF4` | §3.25 | Source-linked re-inspection creation, 3-way defect outcomes (`Resolved`, `Unresolved`, `Inconclusive`), fresh in-session evidence rule, `Resolved` verdict validity expiry, and Web/Mobile warnings | UC-15, UC-18 |

#### 5.4.3 Research Basis and References

- **Building inspection and non-destructive assessment.** Requirements reflect reproducible inspection methods, relevant evidence, and attributable technical reporting for building façades, roofs, and rooftop structures.
- **Building-defect datasets.** The detection model is trained on the MBDD2025 UAV building-defect dataset (CC BY 4.0), covering crack, leakage, abscission, corrosion, and bulge defects.
- **Artificial intelligence governance.** Automated defect suggestions and narrative summaries remain advisory and subject to human review.
- **Civil aviation responsibilities.** Airspace and permit records support readiness review but do not grant flight authorization. Aircraft weight categories and pilot-licence classes follow Article 4 and Article 27 of Decree 288/2025/ND-CP.
