---
title: "Report 3 - Requirement Appendix"
document_type: report3-srs-section
weight: 55
source: "report3-software-requirement-specification.docx"
---

## 5. Requirement Appendix

### 5.1 Business Rules

The following rules govern the current inspection service. Maintenance work orders, corrective repair workflows, maintenance-specific re-inspection, and maintenance cost closeout are outside application scope. Existing maintenance schema and records are retained unchanged; no destructive migration is performed, and those records are not exposed by the application.

| ID | Rule Definition |
| --- | --- |
| BR-01 | `ADMIN` and `MANAGER` perform platform responsibilities. `CUSTOMER` acts within its organization; `INSPECTOR` acts as a partner and may serve customer organizations only through authorized dispatch. |
| BR-02 | A `CUSTOMER` accesses and manages only its organization's assets, service requests, published inspection reports, and payment records. |
| BR-04 | An `INSPECTOR` may act only on assigned inspection work. |
| BR-05 | Inspectors must have current pilot credentials for flight assignment and field work. An expired credential prevents assignment or field work. |
| BR-06 | Customer onboarding screens the initial asset location against applicable airspace information. A prohibited No-Fly Zone location is not accepted; a location requiring review remains pending for an `ADMIN` decision. Screening does not grant governmental flight clearance. |
| BR-07 | Before starting an on-site field session, the assigned Inspector must provide the required flight permit, have current pilot credentials, and record a pre-flight safety note. |
| BR-08 | Airspace checks and permit records support internal readiness review only; they do not grant government aviation authorization. |
| BR-09 | Inspection assignment and reassignment consider overlapping commitments across customer organizations so an Inspector or drone is not double-booked. |
| BR-10 | Service quotations are stated in VND per occurrence, identify scope and timing, and are associated with an eligible Inspector and a drone owned by that Inspector. |
| BR-11 | Service requests proceed through request, quotation, Customer acceptance, signed agreement, and occurrence assignment. Dispatch requires the signed agreement to be recorded by `MANAGER`. |
| BR-12 | Service quotations and inspection reports preserve attributable versions. Published records cannot be silently modified in place. |
| BR-13 | A recurring request agreement may cover occurrences within its agreed term. Each occurrence requires its own assignment, readiness review, report, and settlement. |
| BR-14 | Field sessions record completion or abort. An abort requires a reason and alerts `MANAGER` to reschedule, reassign, or cancel the inspection. |
| BR-15 | Inspection progress distinguishes scheduled, active field work, field completion, report review, completion, and cancellation. Readiness is not evidence of governmental clearance. |
| BR-16 | Aircraft operation is a real-world action performed by qualified people. The service does not actuate aircraft. |
| BR-17 | Inspection evidence retains its identity, upload time, and available capture information. Missing metadata is identified rather than invented. |
| BR-18 | Duplicate evidence within an inspection is identified and is not treated as an independent capture without review. |
| BR-19 | Missing GPS or camera metadata does not automatically invalidate otherwise suitable evidence; missing information remains apparent to reviewers. |
| BR-20 | AI defect suggestions remain advisory until reviewed by the assigned `INSPECTOR`. Only human-confirmed findings are official. |
| BR-21 | Rejected and unconfirmed AI suggestions are excluded from official defect reporting and inspection reports. |
| BR-22 | Inspectors may record manual findings supported by evidence. Manual review remains possible if automated analysis is unavailable. |
| BR-23 | After confirming the findings baseline, the report author explicitly prepares and submits the inspection report. Visiting a screen does not submit it. |
| BR-24 | A `MANAGER` or `ADMIN` distinct from the report author independently reviews the report, publishes it or returns it with reasons. An Inspector cannot review or publish their own report. |
| BR-25 | Customers may follow inspection progress but cannot access internal field records, unconfirmed findings, or unpublished reports as official deliverables. |
| BR-26 | Published inspection reports are preserved. Corrections are issued as new versions; prior versions remain available. Publication is not governmental or professional certification. |
| BR-27 | Commercial and reporting approvals require explicit, attributable human decisions. Silence or passage of time is not approval. |
| BR-28 | Returning an inspection report requires review reasons, preserves the prior version, and returns it to its author for revision. |
| BR-30 | Service workflow approvals are auditable business decisions; they do not constitute statutory engineering seals or governmental aviation authorizations. |
| BR-33 | When a Customer accepts a published report, the applicable service fee becomes due. The official deliverable is made available according to the agreed payment rule after confirmation. Partner settlement is tracked separately. |
| BR-38 | Important onboarding, quote acceptance, agreement recording, partner assignment, field abort, findings confirmation, report publication, and payment decisions are attributable to the responsible actor. |
| BR-39 | A direct link, notification, or document reference does not grant access. Role, organization, assignment, and payment rules apply to each access attempt. |
| BR-40 | Password, role, account, and session changes take effect for active access without removing historical attribution. |
| BR-41 | Partner admission does not require drone ownership. An Inspector may register an owned drone with `REGISTRATION`, `OWNERSHIP`, and `INSPECTION` documents. Platform staff provision Inspector accounts; self-service applications are unavailable. |
| BR-42 | Infrastructure asset registration is subject to No-Fly Zone screening and identifies inspection checkpoints. |
| BR-44 | Inspection reports follow submission, return, publication, and supersession outcomes. |

### 5.2 Common Requirements

- **Form Validation**: Forms explain required information and reject incomplete, invalid, out-of-range, or inconsistent input.
- **Role, Organization, and Assignment Checks**: Each action is limited by role, organization, partner relationship, and assignment. Screen visibility does not imply authority.
- **Date, Time, and Timezone Display**: Dates and times are clear in the relevant organization's or schedule's timezone; important decisions are attributable.
- **Currency and Financial Precision**: Service quotations, applicable taxes, and fees state their currency and are calculated consistently. Current quotations use VND.
- **Evidence and Document Handling**: Inspection media, agreements, qualification records, and reports are validated and shown only to authorized users.
- **Idempotent User Actions**: Retries do not create duplicate occurrences, evidence records, payments, or lifecycle notices.
- **Document Integrity and Version History**: Signed agreements and published inspection reports are protected from unauthorized alteration. Changes are attributable and preserve history.

### 5.3 Application Messages List

| # | Message code | Message Type | Context | Content |
| --- | --- | --- | --- | --- |
| 1 | MSG01 | Inline | Search has no authorized records | No results found. |
| 2 | MSG02 | Under field | Required field empty | This field is required. |
| 3 | MSG03 | Under field | Configured length exceeded | Must not exceed {maxLength} characters. |
| 4 | MSG04 | Under field | Invalid email | Enter a valid email address. |
| 5 | MSG05 | Toast | Record created | Created successfully. |
| 6 | MSG06 | Toast | Record updated | Updated successfully. |
| 7 | MSG07 | Dialog | Versioned action | Confirm this action and the version you are acting on. |
| 8 | MSG08 | Inline | Sign-in failed | Email or password is incorrect. |
| 9 | MSG09 | Inline | Disabled account | Unable to sign in. Contact your administrator. |
| 10 | MSG10 | Inline | Expired access | Your session has expired. Sign in again. |
| 11 | MSG11 | Under field | Password policy failure | Password does not meet the security requirements. |
| 12 | MSG12 | Toast | Inspection dispatched | Inspection scheduled with its asset and assigned partner. |
| 13 | MSG13 | Inline | Newer quotation or report version | A newer version is available. Refresh and review it before continuing. |
| 14 | MSG14 | Toast | Quote or assignment accepted | Accepted successfully. |
| 15 | MSG15 | Under field | Rejection or abort lacks reason | Enter a reason before submitting. |
| 16 | MSG16 | Inline | Invalid file | This file cannot be uploaded. Check its type and size. |
| 17 | MSG17 | Inline | Duplicate evidence | This evidence file has already been provided for this inspection. |
| 18 | MSG18 | Toast | Evidence received | Evidence is available for review. |
| 19 | MSG19 | Inline | Automated advisory unavailable | Automated guidance is unavailable. Continue with human review. |
| 20 | MSG20 | Toast | Inspection report submitted | Inspection report submitted for independent review. |
| 21 | MSG21 | Inline | Candidate findings remain unreviewed | Review all suggested findings before confirming the findings baseline. |
| 22 | MSG22 | Toast | Inspection report published | Approved inspection report published and available to the Customer. |
| 26 | MSG26 | Inline | Required qualification or document missing | Provide all required qualification and supporting documents. |
| 27 | MSG27 | Toast | Compliance document recorded | Internal review does not replace statutory authorization. |
| 28 | MSG28 | Inline | Airspace alert | Location is within a prohibited area or requires review. |
| 29 | MSG29 | Toast | Request or quotation recorded | Service request or quotation saved. |
| 30 | MSG30 | Toast | Report returned | Returned to the author with review reasons. |
| 32 | MSG32 | Under field | Safety note incomplete | Enter the required safety note before starting the field session. |
| 33 | MSG33 | Inline | Findings changed after report preparation | Confirm the findings and review the report before submitting it. |
| 35 | MSG35 | Toast | Signed agreement recorded | Signed service agreement recorded. |
| 36 | MSG36 | Inline | Partner or drone cannot be assigned | Select an eligible Inspector and an owned, approved, available drone. |
| 37 | MSG37 | Inline | Permit or qualification missing | Cannot start field work. Provide the mission permit and current pilot credentials. |
| 38 | MSG38 | Toast | Findings baseline confirmed | Findings baseline confirmed. Prepare and submit the report for review. |
| 39 | MSG39 | Inline | Advisory summary unavailable | Automated summary is unavailable. Review confirmed findings directly. |
| 47 | MSG47 | Toast | Payment confirmed | Inspection service payment confirmed. |
| 48 | MSG48 | Inline | Payment required for deliverable | Accept the published report and complete the required payment to access the official deliverable. |

### 5.4 Other Requirements

#### 5.4.1 Scope and Operational Constraints

- **Role and Organization Separation**: Platform (`ADMIN`, `MANAGER`), customer (`CUSTOMER`), and Inspector responsibilities (`INSPECTOR`) are separated by role, ownership, and assignment.
- **No Direct Drone Flight Control**: The service governs agreements, compliance documents, field sessions, evidence, analysis, inspection reports, and payment. Licensed partner pilots operate aircraft independently.
- **Human Review of AI**: Defect suggestions and report summaries are advisory. Official findings and published reports require explicit human confirmation.
- **Data Preservation**: Legacy maintenance tables and persisted rows are retained unchanged, with no destructive migration. They are not exposed by the application.
- **Qualification and Legal Authority**: A service status or recorded document does not prove professional qualification or government flight clearance.

#### 5.4.2 Feature and Flow Traceability

This traceability matrix maps the six current product features (`FE-01` to `FE-06`) to business responsibilities and use cases.

| Product Feature | Feature Name | Operational Responsibility | Supported Use Cases |
| :---: | --- | --- | --- |
| `FE-01` | Customer Registration, Sign-in and Account Access | Customer onboarding with initial asset screening; account security and access | UC-01, UC-02, UC-03, UC-28 |
| `FE-02` | Partner Onboarding, Assets and Drone Registration | Inspector qualifications, asset screening, and Inspector-owned drone documentation and review | UC-02, UC-04, UC-05, UC-06 |
| `FE-03` | Recurring Service Requests, Occurrences and Notifications | One-time and recurring requests, occurrence coordination, and notices | UC-07, UC-08, UC-20 |
| `FE-04` | Service Requests, VND Quotations, Agreements and Dispatch | Request negotiation, quotations, signed agreements, partner assignment, and dispatch changes | UC-07, UC-08, UC-09, UC-13 |
| `FE-05` | Flight Permit and On-site Field Sessions | Permit and qualification checks and field-session records | UC-10, UC-11 |
| `FE-06` | Evidence, Findings, Reporting and Payment | Evidence intake, confirmed findings, report preparation and publication, Customer acceptance, and payment | UC-14, UC-15, UC-16, UC-17, UC-18 |

#### 5.4.3 Research Basis and References

- **Inspection Reporting and Nondestructive Testing**: Requirements reflect reproducible inspection methods, relevant evidence, and attributable technical reporting.
- **Artificial Intelligence Governance**: AI defect suggestions and summaries remain advisory and subject to human review.
- **Civil Aviation Responsibilities**: Airspace and permit records support readiness review but do not grant flight authorization.
