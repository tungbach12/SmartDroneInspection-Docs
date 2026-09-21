---
title: "Report 3 - Requirement Appendix"
document_type: report3-srs-section
weight: 55
source: "report3-software-requirement-specification.docx"
---

## 5. Requirement Appendix

### 5.1 Business Rules

| ID | Rule Definition |
| --- | --- |
| BR-01 | Admin, Client, and service-workforce identities use distinct actor zones; Admin and Client roles are exclusive. |
| BR-02 | A Client can access only data owned by the Client's organization. |
| BR-03 | An Inspector or Maintenance Engineer can access only work assigned to that user unless another explicit service role grants separate scope. |
| BR-04 | An asset code is unique within its organization. |
| BR-05 | An active recurring schedule requires an active asset and an available checklist template. |
| BR-06 | Only one periodic request may be generated for the same Asset, Schedule, and Due Cycle. |
| BR-07 | An ad hoc request must reference an asset owned by the Client's organization. |
| BR-08 | A quotation or order revision creates a new version and preserves earlier versions. |
| BR-09 | No upfront payment is required for inspection or maintenance work. |
| BR-10 | An unconfirmed inspection service order cannot proceed to Inspector assignment. |
| BR-11 | An Inspector assignment must be accepted before inspection status becomes `READY_FOR_INSPECTION`. |
| BR-12 | Assignment rejection requires a reason and returns the work to the Service Manager. |
| BR-13 | Manual drone piloting, flight control, and operational flight safety remain outside SmartDroneInspection. |
| BR-14 | Each evidence object has a checksum; duplicate content cannot create duplicate evidence in the same work context. |
| BR-15 | Missing GPS is recorded but does not automatically invalidate otherwise acceptable evidence. |
| BR-16 | AI candidates remain non-official until an Inspector confirms or modifies them. |
| BR-17 | Rejected or unverified AI candidates do not enter official defect statistics or reports. |
| BR-18 | An Inspector may manually add a defect that the AI service did not detect. |
| BR-19 | A report author cannot peer-review or technically approve the same report. |
| BR-20 | A report cannot be released before technical approval and deliverable-completeness review. |
| BR-21 | Internal drafts and peer-review comments are not visible to the Client. |
| BR-22 | An accepted report version is immutable; corrections require a new linked version. |
| BR-23 | A maintenance ticket must reference at least one verified finding in an accepted report. |
| BR-24 | A qualified Maintenance Engineer provides the technical maintenance assessment. |
| BR-25 | An assessment assignment does not authorize maintenance execution. |
| BR-26 | An approved maintenance order is required before execution assignment. |
| BR-27 | Material scope or cost growth requires an approved change-order version before additional work. |
| BR-28 | Before and after evidence is required before a maintenance ticket can be closed. |
| BR-29 | Only the Service Manager releases inspection and maintenance results to the Client. |
| BR-30 | The Client may accept a maintenance result, request rework, or request a linked re-inspection. |
| BR-31 | Rework preserves the existing ticket and creates a new execution cycle. |
| BR-32 | Re-inspection creates a linked ad hoc inspection request and returns it to WF2. |
| BR-33 | Status transitions that affect assignment, approval, release, acceptance, or closure are audited. |
| BR-34 | File possession or an object-storage path alone does not grant access to evidence. |
| BR-35 | Password, role, status, and session-revocation changes invalidate affected active sessions. |

### 5.2 Common Requirements

- Every create or update request validates required fields, identifier format, length, allowed values, and current workflow state.
- Search screens provide authorized filtering, stable sorting, pagination, empty-result behavior, and clear loading or error states.
- Dates and times are stored as UTC instants when they represent events and are displayed using the configured user or organization time zone.
- Monetary values use decimal storage with an explicit currency and are not calculated with binary floating-point types.
- APIs use RFC 7807 Problem Details with a stable application code and trace identifier for errors.
- Authentication failures use a generic message and do not reveal whether an email address exists.
- File upload validates type, size, checksum, ownership, and workflow context before the object becomes available.
- Important workflow commands are idempotent or protected by state and uniqueness constraints against duplicate execution.
- All list and detail queries apply organization, ownership, assignment, or release scope before returning data.
- Audit records are append-only from normal application workflows and do not contain passwords, raw tokens, or protected file contents.

### 5.3 Application Messages List

| # | Message code | Message Type | Context | Content |
| --- | --- | --- | --- | --- |
| 1 | MSG01 | In line | A search returns no authorized records | No results found. |
| 2 | MSG02 | Under field | A required field is empty | This field is required. |
| 3 | MSG03 | Under field | An input exceeds the configured length | Must not exceed {maxLength} characters. |
| 4 | MSG04 | Under field | An email address is invalid | Enter a valid email address. |
| 5 | MSG05 | Toast | A record is created successfully | Created successfully. |
| 6 | MSG06 | Toast | A record is updated successfully | Updated successfully. |
| 7 | MSG07 | Dialog | The user starts a destructive or irreversible action | Are you sure you want to continue? |
| 8 | MSG08 | In line | Authentication fails | Email or password is incorrect. |
| 9 | MSG09 | In line | The account is suspended or disabled | Unable to sign in. Contact an administrator. |
| 10 | MSG10 | In line | The session is expired or revoked | Your session has expired. Sign in again. |
| 11 | MSG11 | Under field | A password does not meet the configured policy | Password does not meet the security requirements. |
| 12 | MSG12 | Toast | An inspection request is submitted | Inspection request submitted successfully. |
| 13 | MSG13 | In line | The quotation or order version is stale | A newer version is available. Refresh and review it before continuing. |
| 14 | MSG14 | Toast | An assignment is accepted | Assignment accepted successfully. |
| 15 | MSG15 | Under field | Assignment rejection has no reason | Enter a reason for rejecting the assignment. |
| 16 | MSG16 | In line | An evidence file is unsupported or too large | This file cannot be uploaded. Check its type and size. |
| 17 | MSG17 | In line | Duplicate evidence is detected | This evidence has already been uploaded. |
| 18 | MSG18 | Toast | Evidence upload completes | Evidence uploaded successfully. |
| 19 | MSG19 | In line | The AI service is temporarily unavailable | AI analysis is unavailable. The evidence is saved for manual review or later processing. |
| 20 | MSG20 | Toast | A report is submitted for peer review | Report submitted for peer review. |
| 21 | MSG21 | In line | The report author attempts self-review | The report author cannot review the same report. |
| 22 | MSG22 | Toast | A report is released | Report released to the Client successfully. |
| 23 | MSG23 | Toast | A maintenance change request is submitted | Change request submitted for Client review. |
| 24 | MSG24 | In line | Additional work is attempted without approval | Additional work requires an approved change request. |
| 25 | MSG25 | Toast | A maintenance ticket is resolved | Maintenance ticket closed successfully. |

### 5.4 Other Requirements

- The solution supports controlled Client organization self-registration, but does not provide anonymous consumer registration, online payment processing, procurement, inventory accounting, or autonomous approval of AI findings in this release.
- Web access tokens remain in memory. Browser refresh credentials are delivered only through the protected cookie flow. Mobile credentials use platform secure storage.
- PostgreSQL is the transactional source of truth. MinIO stores evidence objects. The backend mediates authorized file access.
- Use cases use the template's two-digit IDs. Business rules and application messages retain `BR` and `MSG` prefixes. Workflow steps retain `WF1` through `WF4` identifiers in the business-flow reference.
