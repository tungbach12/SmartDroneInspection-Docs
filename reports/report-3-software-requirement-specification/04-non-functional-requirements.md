---
title: "Report 3 - Non-Functional Requirements"
document_type: report3-srs-section
weight: 45
source: "report3-software-requirement-specification.docx"
---

## 4. Non-Functional Requirements

These are target quality/interface requirements for the Enterprise SaaS revision. Existing execution history is not changed or newly claimed here. Selected companion documentation was synchronized on 7 October 2026. V24 aligns identity vocabulary, V25 adds the target schema, and V26 completed the runtime cutover to the exact 41-table target inventory on 8 October 2026 (verified by `./mvnw clean verify`, 88 tests, exit 0). MF1–MF4 workflow behavior remains outside reset scope. Schema structure alone does not establish workflow behavior. Report 5 continues to preserve prior test evidence as historical v1 results.

### 4.1 External Interfaces

- **Web browser:** React web application communicates over HTTPS; supports current project-supported Chrome, Edge and Firefox versions. Platform ADMIN and organization/workforce views use the same authoritative authorization rules.
- **Mobile:** Flutter uses the same versioned backend business contract, with secure mobile credential delivery/storage. Field Start/End is a recorded action, not a Drone SDK command; a connection must validate authoritative readiness before an operational Start is recorded. No offline approval bypass is assumed.
- **REST API:** JSON endpoints remain versioned under `/api/v1`. Successful JSON bodies use `{ success, message, data }`, with authoritative HTTP status; `204` and binary streams are unwrapped. Errors use RFC 9457 Problem Details with stable code/trace ID. This SRS does not invent new endpoint names or assert the current APIs already implement the target.
- **PostgreSQL / MinIO:** Database holds transactional state, tenancy, assignment, cost and review metadata; object storage holds source/derived documents. Evidence and reports are read through authorized backend access, not public object paths.
- **AI Vision / LLM:** Platform-managed services accept only authorized necessary input and return candidates or labelled report drafts with model/provenance information. Image/modality compatibility is explicit. Neither service grants flight clearance, prices repair work, signs a report or approves publication/acceptance.
- **Airspace / regulatory sources:** Public references such as `cambay.mod.gov.vn` assist human pre-checks. Lack of a registry API does not justify claiming automatic licence validation. Applicable law/permit review is required; stale/unavailable reference data is disclosed and unresolved required checks block readiness.
- **Subscription / repair cost:** ENTERPRISE billing records may reference confirmed payments; no online payment gateway is required. Repair actuals/quotes/receipts are an internal cost register, not an integrated bank, payroll, procurement or statutory tax-invoice service.
- **Digital signature:** Application approvals identify actor/version/time. A legally qualified digital signature requires an actual appropriate signer/certificate/service and applicable legal validation; PDF export or a checkbox cannot claim that status by itself.

### 4.2 Quality Attributes

#### 4.2.1 Usability

- A trained user can complete their assigned workflow without developer tools. Lead/report-author duties are labelled explicitly and distinguishable from general team membership.
- Validation identifies the affected item, blocker and remedy. A failure to satisfy credentials, readiness, assignment, evidence or budget approval must not be shown as generic success.
- Web/mobile use the same four role names and workflow meanings. `FIELD_COMPLETED`, report published, team work completed, technically accepted and closed are visually distinct.
- Generated text is clearly labelled draft/AI-assisted. Observations, suggestions, human-confirmed findings and unknown/not supplied data remain distinguishable.
- Author/reviewer can compare draft text to source evidence, change history and calculated financial tables without relying on the LLM's wording alone.
- Keyboard navigation, visible focus, text alternatives and contrast are consistent with the project's WCAG 2.1 AA target; this is a target, not a new accessibility certification.

#### 4.2.2 Reliability and Record Integrity

- Multi-record creation/transitions are atomic: asset plus default pair; inspection plus assignment snapshot; approval plus source version; final work-order closure plus published completion/acceptance record.
- Due-cycle generation is idempotent by asset/schedule/cycle. Upload retries, publication retries and work-order creation cannot duplicate evidence, reports or active corrective scope.
- Store a distinction between raw evidence, annotated/derived evidence, original findings, repair disposition and report versions. Repair never mutates the original published inspection report.
- Mandatory readiness conditions are revalidated at Start. Plan/pair/document/time changes invalidate affected prior approvals; missing mandatory authorization cannot be overridden by an internal exception button.
- Evidence-set changes invalidate dependent generation/author/review confirmations. Regeneration is explicit/versioned and cannot silently overwrite user edits; concurrent stale submissions/approvals are rejected or safely serialized.
- AI failure preserves source evidence and supports manual findings/report drafting under the same human gates. A draft-generation error cannot be converted into an automatically approved blank report.
- Preserve initial estimate, approved changes, supported actuals, correction/return history, author handover and independent acceptance. Record unapproved actual spending honestly as a deviation, without treating entry as authorization.
- Financial totals use deterministic decimal calculations and an explicit currency, tax basis and rounding convention. Missing price is not zero; variance percentage is N/A when the baseline is zero.
- Database/object-storage backup and restore procedures must be verified before a production release. Retention and post-subscription-expiry access require disclosed policies and applicable-law review; no source-derived foreign retention period is assumed universally.

#### 4.2.3 Performance

- Under agreed project test load, 95 percent of standard JSON API requests target completion within 2 seconds, excluding file transfer and external processing latency; no new benchmark is claimed here.
- Lists use scope-first filtering, stable sorting and bounded pagination.
- Uploads show progress and retry safely. Long-running inference/report drafting has separate processing/failure status so users can continue other tasks.
- Cost totals and comparisons use structured data; narrative processing must not block all access to saved work logs or inspection evidence.

#### 4.2.4 Security, Privacy and Maintainability

- All non-public actions deny by default unless both role and resource scope pass. Tenant boundaries cover workforce/health credentials, Drones, evidence, budget, work orders and draft/approved reports.
- ADMIN has no default customer approval/acceptance authority. Exceptional support access requires authorized purpose, minimum privilege and audit attribution.
- Inspector evidence quality is an assigned-person decision. Engineer lead may allocate only to approved team members; report submission requires the designated author. Independent acceptance rejects the author and executing team, regardless of route visibility.
- Budget approval, technical acceptance and cost reconciliation are distinct recorded actions. Human roles do not imply legal/professional qualifications; readiness/report release remains blocked where a required qualified reviewer is missing.
- Sensitive personal/medical/credential evidence is limited to relevant lawful records and minimum viewers. Do not send unnecessary identity or health files to AI/LLM services.
- Treat uploaded text/images/metadata and generated outputs as untrusted. They cannot issue commands, expand access, make policy changes or bypass approval through prompt content.
- Keep passwords hashed; exclude passwords, raw tokens, credentials, private keys and protected file contents from logs/JWT claims. Browser access tokens stay in memory and refresh tokens use Secure, HttpOnly, SameSite=Strict cookies; mobile tokens use platform secure storage.
- Audit records include action/resource/version, responsible identity, timestamp, result and reason where applicable. Append-only normal workflows preserve returns/rejections; no audit record claims governmental verification without evidence.
- Backend capabilities remain separated by Spring Modulith boundaries. Future schema work uses new forward Flyway migrations; no migration is changed by this document revision.
- Preserve versioned JSON/error/file contracts during future implementation or document and approve explicit changes. This target rewrite is not authorization to silently change clients or APIs.
