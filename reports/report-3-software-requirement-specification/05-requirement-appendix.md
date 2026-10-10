---
title: "Report 3 - Other Requirements"
document_type: report3-srs-section
weight: 55
source: "report3-software-requirement-specification.docx"
---

## 5. Other Requirements

### 5.1 Appendix 1 - Application Messages List

Existing MSG01–MSG35 identifiers are retained as revised target message slots. This is a specification, not a claim that the deployed message/error catalog has been migrated. Additional target messages extend the sequence.

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
| 12 | MSG12 | Toast | MF1 inspection created | Inspection created with its asset and assigned Inspector/Drone snapshot. |
| 13 | MSG13 | In line | Stale report, plan or estimate version | A newer version is available. Refresh and review it before continuing. |
| 14 | MSG14 | Toast | Assignment accepted | Assignment accepted successfully. |
| 15 | MSG15 | Under field | Rejection lacks reason | Enter a reason for rejecting the assignment. |
| 16 | MSG16 | In line | Unsupported/corrupt/large evidence | This file cannot be uploaded. Check its type, integrity and size. |
| 17 | MSG17 | In line | Duplicate evidence | This evidence has already been uploaded in this scope. |
| 18 | MSG18 | Toast | Upload saved | Evidence uploaded. Inspector quality review is still required. |
| 19 | MSG19 | In line | AI unavailable | AI analysis is unavailable. Evidence is saved for manual review or later processing. |
| 20 | MSG20 | Toast | Inspection author submission | Author-verified draft submitted to Organization Admin for review. |
| 21 | MSG21 | In line | Author review incomplete | Verify each required report section against source evidence and scope before submitting. |
| 22 | MSG22 | Toast | Inspection report published | Approved inspection report version published successfully. |
| 23 | MSG23 | Toast | Repair change submitted | Scope/cost/time change submitted to Organization Admin for approval. Affected additional work is not yet authorized. |
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
| 38 | MSG38 | Toast | Inspector evidence confirmed | Evidence adequacy confirmed by the assigned Inspector; the source set is ready for compatible analysis. |
| 39 | MSG39 | In line | LLM draft failure | Draft generation failed. Source records are saved; the responsible author can retry or prepare a manual draft. |
| 40 | MSG40 | In line | Missing maintenance lead/author | Assign one team lead and one accountable report author before release. |
| 41 | MSG41 | In line | Unpriced/unsupported cost | Record the price basis and supporting reference. Unknown cost cannot be silently treated as zero. |
| 42 | MSG42 | Toast | Team reports completion | Work reported complete by the team. Independent acceptance and cost reconciliation are still required. |
| 43 | MSG43 | In line | Repair completion proof missing | Attach required before/after evidence and acceptance-test records for the affected tasks. |
| 44 | MSG44 | In line | Self-acceptance attempted | Authors and executing team members cannot independently accept their own work. |
| 45 | MSG45 | In line | Cost reconciliation unresolved | Resolve missing, duplicate or unapproved costs and variance explanations before final closure. |
| 46 | MSG46 | Toast | Maintenance author submits report | Author-verified maintenance completion draft submitted for independent acceptance. |

### 5.2 Appendix 2 - Common Requirements

- Validate identifier, required field, length, allowed value, workflow state and current version on every create/update/decision.
- Apply organization, assignment and designated lead/author/reviewer scope before lists/detail/file access, not after returning data.
- Dates representing events use UTC instants and display configured organization/user time zone. Legal-document validity uses the applicable date/time scope without assuming a timezone-independent full day.
- Monetary values use decimals with explicit currency, tax basis and rounding. Financial comparison/percentage conventions are defined in Functional Requirements §3.8.3.
- Successful JSON API bodies retain `{ success, message, data }` and authoritative status; `204`/binary streams remain unwrapped. Errors follow RFC 9457 with stable code and trace ID.
- Generic authentication errors do not reveal email existence. Evidence/API errors must not disclose another organization's records.
- Files are technically validated and scoped before storage/access; technical acceptance never substitutes for Inspector evidence-quality decisions.
- Important commands are idempotent/state-guarded: due-cycle generation, upload, assignment dispatch, report publication, draft work-order creation and final closure.
- Preserve prior evidence, pair/team assignment, estimate, report and approval versions. Changing source input or regenerating draft invalidates affected confirmations and cannot silently replace human edits.
- Application approvals/acknowledgments preserve identity/time/version; no qualified legal signature is presumed merely from a checkbox, hash or PDF.
- Audit logs are append-only in normal workflows and exclude passwords, raw tokens, private keys and protected document text.

### 5.3 Appendix 3 - Scope and Technology Constraints

- The current Report 3 target is Enterprise SaaS with four human roles and four MFs. This update is documentation-only and limited to Report 3. Historical deployed code/test results still describe the versions actually tested.
- No external provider marketplace, RFQ, commission, platform arbitration or Client–Provider repair-payment route is required. Supplier quote/receipt attachment is a cost reference, not a marketplace subsystem.
- No autonomous Drone flight, camera/SDK control, GSD/overlap/gimbal recommendation or automatically granted government clearance. Mission/field steps are platform preparation, checklists, recorded decisions and session logs.
- AI candidates and LLM text are suggestions/drafts. No autonomous official reporting, technical acceptance, budget approval or defect closure; a human author and qualified independent reviewer remain accountable.
- MF1 keeps asset creation with Inspector + Drone assignment and inspection creation; MF2 prepares/releases and records sessions; MF3 Inspector quality → AI Vision → LLM draft → author/reviewer gates; MF4 team, estimates/changes/actuals → LLM completion draft → author → independent acceptance/cost reconciliation → close.
- Team lead and report author are scoped Maintenance Engineer responsibilities; no additional login role is created. The same Engineer can do both, but cannot accept their own work.
- PostgreSQL is transactional source of truth; MinIO stores evidence/reports; backend mediates access. Web tokens remain in memory/protected cookie flow; mobile tokens use secure storage.
- No automatic ERP/procurement, payroll, payment gateway, government registry, certified digital signature, universal report accreditation or sector-specific safety certification is promised. Future integrations need explicit contracts and verification.
- The 7 October 2026 SRS revision updated Report 3 Markdown sources and did not implement or test the target. Selected documentation companions were synchronized on 7 October without changing Report 5 results; other documents, the proposal, DOCX/PNG baseline artifacts, and client repositories may remain on earlier contracts. The retained DOCX and PNG artifacts are not regenerated and are non-normative for the new target.

### 5.4 Feature and Flow Traceability

Existing FE product codes remain stable; the MF mapping below is a **revised target mapping**, not a new meaning for historical Report 5 rows.

| Product feature | Current Report 3 target responsibility | Flow / detailed step range |
| --- | --- | --- |
| FE-01 | Identity, entitlement, organization/workforce governance | Supporting gate; MF1-01–MF1-05 and authorization across all flows |
| FE-02 | Asset, Drone and compliance management; asset pair; inspection setup | MF1-01–MF1-14 |
| FE-03 | Assignment response, preparation, permits and readiness | MF2-01–MF2-12 |
| FE-04 | Session/evidence records and Inspector substantive quality | MF2-09–MF2-12; MF3-01–MF3-04 |
| FE-05 | Candidate generation and human finding decisions | MF3-05–MF3-06/MF3-09 |
| FE-06 | Source-grounded LLM draft, author review, qualified approval and publication | MF3-07–MF3-13 |
| FE-07 | Repair team, estimates, approvals, actuals, changes, LLM completion report and acceptance | MF4-01–MF4-21 |
| FE-08 | Scope-filtered queues, analytics, notifications and audit visibility | Cross-flow supporting functions |

Two-digit use-case slots, BR IDs and MSG IDs were retained/revised or extended, not renumbered. `MFx-nn` identifies the detailed target steps in this report only. Existing `WFx-yyy` workbook/test IDs and executed statuses outside Report 3 are untouched; acceptance tests for this target have not been run or recorded by this edit.
