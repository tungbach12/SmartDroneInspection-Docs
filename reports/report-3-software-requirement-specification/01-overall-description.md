---
title: "Report 3 - Overall Description"
document_type: report3-srs-section
weight: 15
source: "report3-software-requirement-specification.docx"
---

# II. Software Requirement Specification

## 1. Overall Description

### 1.1 Product Overview

**Report 3 target revision — 7 October 2026.** SmartDroneInspection is an Enterprise, multi-tenant SaaS application rented by infrastructure-owning companies to manage their own assets, workforce, Drones, compliance records, inspection evidence, reports and repairs. One ENTERPRISE offering supports payment periods of **1 month, 6 months or 12 months**. The platform supplies storage, AI Vision and LLM drafting through its authorized interfaces; it is not an inspection-service marketplace or a Drone flight-control product.

This revision supersedes Report 3's previous multi-provider target. It specifies intended behavior, not deployed functionality or completed workflow APIs. The Enterprise SaaS backend reset began on 7 October 2026 in a separate backend repository. V24 aligns identity vocabulary, V25 adds the target schema, and V26 completed the runtime cutover to the exact 41-table target inventory on 8 October 2026 (verified by `./mvnw clean verify`, 88 tests, exit 0). MF1–MF4 workflow behavior remains outside reset scope. On the date of this revision, related documents were not yet synchronized; the 7 October documentation reconciliation updated selected database, backend status, and Report 5 references while preserving their histories. Other references and client repositories may still describe earlier contracts. No feature-completion or runtime-test claim is made.

There are two ownership layers and **four human roles**:

- **Platform:** `ADMIN` manages SaaS customer workspaces, enterprise subscription activation/renewal, technical/security settings and authorized platform audit/support. It does not make customer technical conclusions, repair-budget decisions or internal work acceptance.
- **Customer organization:** `ORG_ADMIN` manages its workforce, credentials, Drone fleet, assets with assigned Inspector/Drone pairs, inspection creation, readiness review, final inspection findings/report approval, maintenance team/budget assignment and independent acceptance. Each technical reviewer must actually be qualified for the scope; account privileges do not establish qualifications.
- **Customer workforce:** `INSPECTOR` accepts assigned inspection work, prepares/checks the shot-list and compliance inputs, records field sessions on app, uploads evidence, directly decides its completeness/quality and verifies/edits the inspection report draft.
- **Customer workforce:** `MAINTENANCE_ENGINEER` works within assigned repair teams/tasks, supplies technical assessment/estimates, records work/evidence/actuals and, when designated, leads the team or authors the maintenance report. Team lead and report author are scoped responsibilities, not extra roles.

`SYSTEM`, AI Vision and LLM are automatic components, not account roles. No `PLATFORM_OPERATOR`, `PROVIDER_MANAGER` or `CLIENT` role is used in this target. There is no external Provider sourcing, RFQ, commission, Client–Provider settlement or Platform arbitration workflow.

#### Four connected Main Flows

| Flow | Primary responsibility | Output used by the next flow |
| --- | --- | --- |
| MF1 — Resources, Assets, Assignment and Inspection Setup | Organization Admin manages Inspectors/Engineers, credentials, identified Drones and applicable compliance files; creates an asset **with one Inspector and one specific Drone assigned**; creates an inspection inheriting that pair. | Inspection ID, asset/scope/dates, pair snapshot and document references for MF2. |
| MF2 — Preparation, Compliance and Field-Session Records | Inspector accepts/prepares; qualified Organization Admin reviews compliance/readiness; Inspector completes current pre-flight checklist and records Start/End/postponement on app. | Ended session(s), checklist/shot-list, assigned pair and approval basis for MF3. |
| MF3 — Evidence, AI Vision, LLM Inspection Report and Review | Inspector decides evidence quality; SYSTEM detects candidates and produces a draft; Inspector authors/verifies; qualified Organization Admin confirms findings and approves publication. | Immutable inspection report version and confirmed repair-required findings for MF4; a no-repair outcome closes without an empty work order. |
| MF4 — Team Repairs, Costs, LLM Completion Report and Acceptance | Organization Admin assigns team/lead/report author; Engineers plan and document work; scope/budget/changes require approval; LLM drafts; report author verifies; independent qualified Organization Admin accepts and reconciles costs. | Published repair completion/acceptance record, reconciled cost and updated asset history; required open work stays visible. |

Registration/authentication and subscription activation are **supporting gates**, not a fifth MF. Assets remain master records; later inspections reuse the asset and create a new inspection ID in MF1. The pair assigned at asset creation is a default, not an exclusive lifetime reservation of a Drone. Inspection-specific changes preserve past snapshots. MF4 never overwrites the original MF3 report.

**Boundaries:** Flying by RC, adjusting equipment and doing physical repairs are outside software steps. The application stores preparations/observations/results; it does not pilot, arm, isolate or prove hardware safety. Flight/compliance logs are separate from the asset-condition inspection report. Informational public restricted-airspace data is not permission. Applicable issued permits, legal exemptions, credentials and operating conditions must be reviewed for the mission; missing mandatory authorization cannot be waived by Organization Admin. Research/application limits are explained in [Functional Requirements §3.10](../03-functional-requirements/#310-research-basis-and-applicability).

SHA-256, timestamps and version histories support technical integrity/traceability, not automatically conclusive legal proof. Logged application approval is not automatically a legally qualified digital signature. LLM produces a labelled source-grounded draft only; missing data remains unknown, numerical totals come from structured calculations, and humans remain accountable for official conclusions and acceptance.

The ENTERPRISE subscription pays for use of the software. Repair labor/material/equipment costs are the enterprise's internal work-order expenses, recorded separately from SaaS revenue. Supplier quotes/receipts can be attachments; supplier payment, payroll, procurement/accounting integration and statutory tax-invoice issuance are not included by implication.

The retained `assets/context.png` illustrates an earlier baseline and is not normative for this revision. The current textual flow and [detailed steps](../03-functional-requirements/) define this Report 3 target; binary diagram/DOCX regeneration is not included.

### 1.2 Business Rules

Existing `BR-01`–`BR-41` identifiers are retained with revised definitions for this target. Their prior meanings remain in change history/Git; they must not be read as mappings to unchanged historical tests. Additional rules extend the sequence instead of renaming existing IDs.

| ID | Rule Definition |
| --- | --- |
| BR-01 | Only Platform Admin is platform-owned; Organization Admin, Inspector and Maintenance Engineer are customer-workspace roles. Platform administration and customer operational identities are separate. |
| BR-02 | Organization Admin can manage only its own organization's assets, resources, inspections, reports, work orders and cost records. |
| BR-03 | Customer workforce identities belong to the relevant organization; a team or role cannot bridge tenant boundaries. |
| BR-04 | Inspectors/Engineers can act only on assigned inspections, work orders or tasks; lead/report-author designation further scopes actions. |
| BR-05 | Active users and applicable qualifications/documents are required for operational release. Each credential is checked for the relevant activity; unrelated qualifications do not satisfy it. |
| BR-06 | Enterprise registration, authentication and subscription activation are supporting gates; MF1–MF4 are the four connected business flows. |
| BR-07 | Preparation requires a component shot-list and safety/compliance checklist. No automatic GSD, overlap, gimbal, waypoint or physical flight-setting recommendation is required. |
| BR-08 | Mission readiness records applicable airspace/permit checks, dates and conditions; public map lookup and internal approval never grant government authorization. |
| BR-09 | Periodic due work is idempotent for asset/schedule/cycle and inherits the current asset pair into a new inspection snapshot. |
| BR-10 | ENTERPRISE is the sole software plan, with 1-, 6- or 12-month payment periods; no trial, discount, unlimited quota or price is presumed. |
| BR-11 | Subscription terms and entitlement decisions are versioned/audited; future updates do not rewrite agreed or historical records. |
| BR-12 | Report versions, estimate baselines, scope changes and approval decisions preserve prior versions; published reports cannot be silently changed. |
| BR-13 | Subscription renewal/cancellation/expiry follows explicitly disclosed terms; expiry never automatically marks open business work complete. |
| BR-14 | Inspector records postponement/abort when weather/site conditions are unsafe; a prior readiness decision does not force operational Start. |
| BR-15 | Assigned Inspector must accept the assignment before readiness release; rejection requires a reason and returns to Organization Admin. |
| BR-16 | Manual flight and physical repair remain real-world responsibilities of qualified customer personnel; software Start/End is recordkeeping, not device control. |
| BR-17 | Evidence retains server-computed SHA-256, source links and available metadata; missing metadata is disclosed, and hashes do not confer legal admissibility by themselves. |
| BR-18 | Duplicate evidence in the same inspection/work-log scope is rejected and retry cannot create duplicate intake records. |
| BR-19 | Missing GPS/telemetry is recorded, not invented and not an automatic quality failure for otherwise suitable visual evidence. |
| BR-20 | AI detections remain candidates until human review; the qualified Organization Admin's final finding decisions govern the published report. |
| BR-21 | Rejected/unverified candidates never enter official defect statistics or approved corrective-work scope. |
| BR-22 | Inspector can add source-backed manual observations/findings; AI unavailability does not discard evidence or prevent manual reporting. |
| BR-23 | Inspector is responsible for evidence-quality decisions and author verification/editing of every required inspection-report section before submission. |
| BR-24 | A qualified Organization Admin distinct from the inspection author reviews findings/text/limits and approves publication; missing qualifications/approval block release. |
| BR-25 | Draft/unverified content is restricted to assigned authors and authorized reviewers and clearly separated from approved results. |
| BR-26 | Published report versions are immutable; corrections create linked revisions and invalidate affected prior review confirmations. |
| BR-27 | No silence-based or timer-based technical acceptance is presumed. Publication and maintenance acceptance require attributable human decisions. |
| BR-28 | An incomplete report returns to its named author with reasons and preserved versions; no marketplace complaint/payment-hold flow exists. |
| BR-29 | Platform Admin governs/supports SaaS, not customer technical approval, repair-budget approval or legal arbitration. |
| BR-30 | App acknowledgments/approvals are auditable records, not automatically government permits, qualified signatures, safety certificates or court determinations. |
| BR-31 | Corrective work references at least one confirmed repair-required finding from a published own-organization inspection report version. |
| BR-32 | Assigned qualified Engineer/lead supplies technical scope, tasks and itemized estimate; LLM does not invent labor rates, quantities or repair prices. |
| BR-33 | Follow-up/warranty conditions apply only when actually supplied and applicable; no standard warranty duration or expiry-based proof of safe repair is presumed. |
| BR-34 | Scope/budget/time growth requires approved change control before the affected additional work is authorized; initial baseline stays unchanged. |
| BR-35 | Repair completion submission requires paired before/after evidence per relevant defect/task and required tests/checklists; photos alone do not establish every acceptance criterion. |
| BR-36 | Repair cost is an internal tenant cost register, separate from software subscription billing; no Platform repair commission or routing/custody of repair payments. |
| BR-37 | Separate re-inspection creates a linked new inspection in MF1; additional missing evidence for the current inspection returns to MF2 under that same inspection. |
| BR-38 | Assignment, compliance, quality, findings, report, scope/budget/change, acceptance and closure decisions are audited with identity/time/version/outcome. |
| BR-39 | File possession, notification links and object paths confer no authorization; backend role and scope checks remain mandatory. |
| BR-40 | Password, role, status and session-revocation changes invalidate affected sessions; reassignment ends future scoped authority without erasing prior actions. |
| BR-41 | Workforce/compliance catalog management is in MF1; mission-specific approval is in MF2; permit applicability is assessed against authoritative current law and recorded evidence. |
| BR-42 | Asset creation includes exactly one responsible Inspector and one identified Drone in the same workflow; dispatch requires an inspection snapshot of that pair and resolved conflicts. |
| BR-43 | Only the assigned Inspector decides substantive evidence completeness/quality before AI; technical upload validation does not substitute for that decision. |
| BR-44 | MF3 order is evidence quality → AI Vision → LLM draft → Inspector verification → qualified Organization Admin findings/report review → publication. AI/LLM cannot bypass it. |
| BR-45 | Each MF4 work order has an approved Engineer team, exactly one lead and one accountable report author; lead and author may be the same person but neither accepts their own team's work. |
| BR-46 | Every task has a responsible approved team member; lead allocates only within approved membership, and Organization Admin records lead/author replacement and handover. |
| BR-47 | SYSTEM computes authorized budget and actual/variance totals with decimals and consistent currency/tax basis; missing cost is not zero, and contingency is not an incurred expense. |
| BR-48 | LLM drafts both report types solely from permitted sources and preserves uncertainty/provenance; it cannot invent measurements, causes, completion, financial evidence or approval. |
| BR-49 | MF4 report author verifies and submits the completion draft; a qualified Organization Admin outside the executing team performs independent technical acceptance. |
| BR-50 | Team-declared work completion, technical acceptance, financial reconciliation and closure are distinct. CLOSED requires all required tasks, evidence, decisions and pending changes resolved. |
| BR-51 | MF3 records point-in-time observed condition; MF4 records executed work, actuals and acceptance. Original published findings/report remain unchanged by repair. |
| BR-52 | Readiness is rechecked at field-session Start and after material changes; expired/revoked mandatory authorization cannot be bypassed by internal exception approval. |
| BR-53 | A no-repair MF3 outcome closes without an empty work order. Where corrective work is required, open related work prevents a false overall-completed outcome. |
| BR-54 | GenAI failure allows a structured manual draft under identical author/review gates; regeneration is explicit/versioned and cannot silently overwrite human edits. |
