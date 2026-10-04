---
title: "Report 3 - Other Requirements"
document_type: report3-srs-section
weight: 55
source: "report3-software-requirement-specification.docx"
---

## 5. Other Requirements

### 5.1 Appendix 1 - Application Messages List

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
| 26 | MSG26 | In line | Provider onboarding documents are incomplete | Upload valid business registration, drone registration, pilot credentials, and insurance before submitting for verification. |
| 27 | MSG27 | Toast | Provider verification is approved | Service Provider verified successfully. |
| 28 | MSG28 | In line | Preliminary restricted-airspace warning | Public airspace data indicates a possible restriction. Verify applicable authority clearance; this lookup is not a flight permit. |
| 29 | MSG29 | Toast | Partner funding status received | Payment partner confirmed the transaction status. This status alone does not establish electronic-contract validity. |
| 30 | MSG30 | Toast | Complaint received | Complaint submitted. Any payment hold depends on the authorized partner product and accepted order terms. |
| 31 | MSG31 | Dialog | Internal complaint outcome recorded | Platform Operator recorded an internal outcome under Platform Terms; external legal remedies remain available. |
| 32 | MSG32 | Under field | Mission target conflicts with SOW or equipment | Revise mission-specific GSD, overlap, equipment or shot items to match the accepted SOW before requesting approval. |
| 33 | MSG33 | In line | Commercial policy changed | New policy applies only to eligible future orders. Accepted order snapshots remain unchanged. |
| 34 | MSG34 | Toast | Policy version published | Versioned commercial policy published with an effective date and audit record. |
| 35 | MSG35 | In line | Payment partner cannot support requested terms | This funding or hold option is unavailable. Choose a reviewed supported payment arrangement; the Platform does not hold funds. |

### 5.2 Appendix 2 - Common Requirements

- Every create or update request validates required fields, identifier format, length, allowed values, and current workflow state.
- Search screens provide authorized filtering, stable sorting, pagination, empty-result behavior, and clear loading or error states.
- Dates and times are stored as UTC instants when they represent events and are displayed using the configured user or organization time zone.
- Monetary values use decimal storage with an explicit currency and are not calculated with binary floating-point types.
- Successful JSON API bodies use the common `{ success, message, data }` response envelope; the HTTP status remains authoritative, and `204 No Content` and binary streams have no envelope.
- API errors use RFC 9457 Problem Details with a stable application code and trace identifier.
- Authentication failures use a generic message and do not reveal whether an email address exists.
- File upload validates type, size, checksum, ownership, and workflow context before the object becomes available.
- Important workflow commands are idempotent or protected by state and uniqueness constraints against duplicate execution.
- All list and detail queries apply organization, ownership, assignment, or release scope before returning data.
- Audit records are append-only from normal application workflows and do not contain passwords, raw tokens, or protected file contents.
- Commercial policies are versioned, effective-dated and published only by authorized `PLATFORM_OPERATOR` users; updates apply prospectively, with accepted policy values preserved in immutable order snapshots.
- Drone mission targets (including GSD, overlap, altitude, gimbal and shot items) are mission/equipment/SOW-specific and require scoped Provider/assignment authorization. Waypoint coordinates are optional for waypoint-assisted capture; manual piloting under the approved shot plan is supported, with no autonomous flight control implied.
- Payment/funding/hold operations must check the authorized partner product and order terms. Platform roles may coordinate instructions but cannot custody funds or claim legal arbitration authority.

### 5.3 Appendix 3 - Scope and Technology Constraints

- The implemented v1 solution supports Client organization self-registration. The target design treats organization registration, Provider vetting, asset master data and schedule setup as SF, outside the five transactional MF1–MF5. Target drone mission planning is not evidence of deployed mission or flight-control functionality. Neither version provides anonymous consumer registration, direct autonomous drone flight control, or autonomous publishing of AI findings.
- Advance funding, conditional release, dispute holds and retention are target integrations requiring an authorized bank/payment partner product that supports the accepted order terms; the Platform does not hold customer deposits or act as a financial institution. These target integrations are not implemented in v1.
- Web access tokens remain in memory. Browser refresh credentials are delivered only through the protected cookie flow. Mobile credentials use platform secure storage.
- PostgreSQL is the transactional source of truth. MinIO stores evidence objects. The backend mediates authorized file access.
- Use cases use the template's two-digit IDs with Verb + Noun naming. Business rules and application messages retain `BR` and `MSG` prefixes. The business-flow reference defines five canonical Main Flows (`MF1` through `MF5`), while historical v1 tests retain their stable `WFx` identifiers in Report 5.
