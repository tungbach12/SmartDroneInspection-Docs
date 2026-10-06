---
title: "MF1–MF5 Canonical Contract Matrix"
document_type: contract-matrix
purpose: "Single canonical role, actor-zone, flow, API, and data matrix. Records the documented target, the as-implemented current state, and every gap with the task number that owns closing it."
version: "1.0"
updated: 2026-10-05
---

# MF1–MF5 Canonical Contract Matrix (v1.0)

## 0. How to read this document

This matrix is the contract that Phase 1 through Phase 7 build against. It exists so
no later task has to rediscover a documented-vs-implemented difference.

**Authority order.** Where two sources disagree, this ranking applies:

1. The six canonical roles and the capability-vetting model below (settled decisions,
   recorded in §2). These are not re-litigated by any task.
2. Report 3 (`reports/report-3-software-requirement-specification/`) and
   `project-reference/business-flows.md` define the **target**.
3. `project-reference/database-design.md` defines the **target schema**.
4. The Java/React/Flutter source defines the **as-implemented state**.

**The target is never described as implemented.** Every target row is paired with an
implementation row and a status.

**Status vocabulary** — only these four values are used:

| Status | Meaning |
| --- | --- |
| `implemented` | Exists in the implementation with executable code or schema, verified against the source tree at the commit recorded in §0.1. |
| `partial` | Some of the documented behavior exists; a named part is missing. The missing part is a numbered gap. |
| `target-only` | Documented; no implementation exists. |
| `blocked-by-baseline` | Cannot be implemented until a baseline data or decision problem is resolved by a human. Named blocker is stated. |

**Gap IDs.** `GAP-R-nn` role/actor-zone, `GAP-F-nn` flow, `GAP-A-nn` API,
`GAP-D-nn` data. Every gap names exactly one owning task, or `ORPHAN` when no task in
the plan owns it. Orphan gaps require a controller ruling before the owning phase
starts.

**Counting note.** Gaps are recorded per area because each area is worked by a
different task. Some gaps share a root cause across areas (for example `GAP-R-04` and
`GAP-D-01` are the same missing Provider Organization table seen from two sides). The
per-area counts are therefore larger than the count of unique root causes; §8 lists the
root causes.

### 0.1 Verification basis

Everything marked as implemented state below was read from these trees, not from
documentation:

| Repository | Commit | Role of this reading |
| --- | --- | --- |
| `backend` (main) | `04a254f45d83dc0c1fe8264ddd56febd040c05e8` | The `main` baseline. |
| `backend` (`refactor/wf1-contract`) | `1a5c88e955bb4fe3e82ad345e1516372edbd92cb` | Forward-most backend state; adds `V12__wf1_contract_alignment.sql`. Used for schema where it is forward of `main`. |
| `frontend` (main) | `d717fb3` | Role union, portal policy, route guards. |
| `mobile` (main) | `aaa946b` | Consumed API paths. |
| `docs` (this worktree) | `585ca3c0763d7e1f8bf81a10883c02fcbfb58ebb` | The target documents. |
| `backend` (`refactor/mf1-mf5-backend`) | `451a2af` | Task 1.4, commit under review. Post-fix-round-1 rows below were read from this tree, not from the documents. |

**Report 3 capability-vetting basis.** This worktree is based on `main` and therefore
does **not** contain the uncommitted Report 3 edits living in
`/home/ubuntu/SmartDroneInspection/docs` on branch `docs/provider-capability-vetting`
(`365f156`). Those edits were read as reference only and are reflected in §2.3–§2.5 of
this matrix, per the settled decision. The four Report 3 files are the only files that
differ between the two checkouts; `business-flows.md` and `database-design.md` are
byte-identical, which is why the conflicts in `GAP-R-06`, `GAP-F-01`, and `GAP-D-13`
exist at all.

**This task produced no test evidence.** No test was executed for this matrix. Every
`implemented` status is a source-reading claim, and every Report 5 status quoted in §6
is a pre-existing recorded status from the documents, not a new result.

### 0.2 Documented-vs-implemented conflict resolutions

| # | Conflict | Resolution applied here |
| --- | --- | --- |
| C-1 | The task brief names the output path `docs/superpowers/plans/mf1-mf5-contract-matrix.md`. The `docs` repository content root has no nested `docs/` directory on `main`; content lives at `project-reference/`, `reports/`, `backend/`, etc. The plan file itself is only reachable at `docs/docs/superpowers/plans/…` from the `docs/provider-capability-vetting` branch. | Matrix written to `project-reference/mf1-mf5-contract-matrix.md`, matching the actual repository layout and the instruction that the matrix belongs under `docs/project-reference/`. Recorded as `GAP-D-22`. |
| C-2 | The plan and brief spell source paths as `docs/project-reference/…` and `docs/backend/…`. Those paths do not resolve on this branch. | All paths in this matrix are repository-relative and verified to exist. Recorded as `GAP-D-22`. |
| C-3 | Report 3 §2.1 defines `PLATFORM_ADMIN`; `database-design.md` §6.1 defines actor zones `PLATFORM_GOVERNANCE` / `CUSTOMER_ORGANIZATION` / `SERVICE_PROVIDER`; the implementation enum defines `PLATFORM` / `CUSTOMER_ORGANIZATION` / `SERVICE_WORKFORCE`. | The documented target zone names win. Two of three zone names change. `GAP-R-02`. |
| C-4 | Report 3 `business-flows.md` SF-03 grants a single organization-wide `VERIFIED` and blocks an unapproved Provider from "all quotation rights", which contradicts the capability-scoped BR-05 gate. | The capability-scoped gate wins. `business-flows.md` SF-03 must be rewritten in Task 7.1. `GAP-R-06`, `GAP-F-01`. |
| C-5 | `database-design.md` §12 asserts `V1`–`V11` implement "37 application tables", but the inventory closure requires counting `provider_organizations` as implemented and omitting `peer_reviews`, which has DDL. | Actual DDL was enumerated directly: 38 `CREATE TABLE` statements = 37 application tables + `event_publication`. The doc's *count* is right; its *inventory membership* is wrong. `GAP-D-01`, `GAP-D-18`. |
| C-6 | Report 3 uncommitted edits require four per-capability vetting outcomes but never name them as an enum. | The four-value vocabulary is fixed in §2.4 of this matrix, sourced from `business-flows.md` SF-03 and the design spec §2.3, and is now binding for all tasks. `GAP-R-06`. |

---

## 1. Canonical vocabulary

### 1.1 Six canonical roles and three actor zones

These six rows are the complete role set. There is **no** `MAINTENANCE_PROVIDER_MANAGER`
and no seventh role may be introduced by any task.

| # | Role | Actor zone | Canonical responsibility |
| --- | --- | --- | --- |
| 1 | `PLATFORM_ADMIN` | `PLATFORM_GOVERNANCE` | Technical configuration, security policy, checklist templates, technical audit. Cannot publish commercial policy or vet a Provider. |
| 2 | `PLATFORM_OPERATOR` | `PLATFORM_GOVERNANCE` | Provider vetting, commercial-policy publication, payment-partner coordination, internal complaint handling. Not a legal arbitrator, not a deposit custodian. |
| 3 | `CLIENT` | `CUSTOMER_ORGANIZATION` | Customer-organization assets, requests, orders, report decisions, complaints, maintenance tickets. |
| 4 | `PROVIDER_MANAGER` | `SERVICE_PROVIDER` | The **single** Provider Organization representative. Quotations, mission-plan approval, permits, workforce assignment, QA completeness/release, maintenance quotations and orders. |
| 5 | `INSPECTOR` | `SERVICE_PROVIDER` | Assigned manual flight, evidence, AI-candidate verification, and verification/editing of the draft they authored. |
| 6 | `MAINTENANCE_ENGINEER` | `SERVICE_PROVIDER` | Assigned technical assessment, repair execution, work logs, mandatory before/after evidence. |

Zone invariants (Report 3 BR-01, `database-design.md` §6.1):

- `PLATFORM_GOVERNANCE` users have **neither** `organization_id` **nor** `provider_id`.
- `CUSTOMER_ORGANIZATION` users require `organization_id` and a null `provider_id`.
- `SERVICE_PROVIDER` users require `provider_id` and a null `organization_id`.
- Zone membership is exclusive. A user in one zone cannot hold a role from another zone.

### 1.2 Actor-zone → module ownership

| Actor zone | Owning backend module | Client surface |
| --- | --- | --- |
| `PLATFORM_GOVERNANCE` | `users` | Platform governance workspace |
| `CUSTOMER_ORGANIZATION` | `assets` (WF1/SF), `inspectionrequests` (MF1), `inspections` (MF3/MF4 reports), `maintenance` (MF5) | Customer workspace |
| `SERVICE_PROVIDER` | `inspectionrequests` (MF1 quotes/assignments), `inspections` (MF2/MF3), `maintenance` (MF5) | Provider workspace + mobile assigned-work screens |

---

## 2. Provider capability model (settled decision)

### 2.1 Capability is organization data, not a role

Inspection capability and maintenance capability are **records on a Provider
Organization**, not user roles. Selecting "both" in any UI creates **two capability
records**. There is no `BOTH` enum value.

### 2.2 Who declares and who vets

| Action | Role | Never |
| --- | --- | --- |
| Declare capability set, submit shared legal identity once | `PROVIDER_MANAGER` | — |
| Submit capability-specific evidence | `PROVIDER_MANAGER` | Provider may not self-approve (`GAP-R-07`) |
| Record a vetting decision | `PLATFORM_OPERATOR` | `PLATFORM_ADMIN` may not vet; `PROVIDER_MANAGER` may not vet |

### 2.3 Capability types

| Value | Meaning |
| --- | --- |
| `INSPECTION` | Drone/pilot/insurance evidence for declared inspection scope. |
| `MAINTENANCE` | Declared repair scope, qualified personnel, applicable credentials/insurance. |

Inspection evidence is never substituted for maintenance evidence, or vice versa.
Mission-specific flight permits and airspace clearance are verified separately in MF2
and are **not** part of capability vetting.

### 2.4 Vetting status vocabulary (binding)

Exactly four values, per capability:

| Value | Meaning | Effect on eligibility |
| --- | --- | --- |
| `PENDING` | Declared, not yet decided. | Ineligible. |
| `ADDITIONAL_INFO_REQUIRED` | Evidence requested; decision deferred. | Ineligible until re-decided. |
| `VERIFIED` | Approved for that capability. | Eligible **only** for that capability's activities. |
| `REJECTED` | Refused for that capability. | Ineligible. |

Suspension/retirement of an entire Provider Organization is a separate
`provider_organizations.status` concern and must not be conflated with a capability
status. See `GAP-D-13`.

### 2.5 Capability gates (BR-05, BR-41)

| Activity | Required capability | Owning task |
| --- | --- | --- |
| Submit an inspection quotation | `INSPECTION = VERIFIED` | 2.1 |
| Receive a flight assignment / issue a mission plan | `INSPECTION = VERIFIED` | 2.1, 2.3 |
| Be listed as an inspection-provider choice on an RFQ | `INSPECTION = VERIFIED` | 2.1 |
| Issue a maintenance quotation or order | `MAINTENANCE = VERIFIED` | 5.1 |
| Receive a maintenance assignment / perform repair work | `MAINTENANCE = VERIFIED` | 5.1 |

**BR-41 independence rule.** A decision on one capability MUST NOT implicitly change,
verify, or unlock the other. Verifying inspection leaves maintenance at whatever status
it independently holds, and rejecting maintenance leaves inspection untouched. There is
no cascade path in code, in the UI, or in a database constraint.

**No capability decision exists for an undeclared capability.** A decision against a
capability the Provider did not declare is rejected.

### 2.6 Organization standing is its own operator decision (settled, Task 1.4 fix round 1)

Matrix §2.4 separates organization standing from capability eligibility, and `GAP-D-13`
exists because a single `status` column conflated them. That separation fixes more than
the schema. `ProviderEligibilityFacade` ANDs the two, so standing is a **precondition**
of eligibility — which means a design that reaches standing *through* a capability
decision makes the gate a product of the decision it is supposed to constrain.

Settled rule:

| Rule | Detail |
| --- | --- |
| Standing is decided only by its own action | `POST /api/v1/provider-organizations/{providerId}/standing/decisions`. No capability decision writes `provider_organizations.status`, in any direction. |
| Owner | `PLATFORM_OPERATOR`, per §1.1 "Provider vetting". No seventh role (§10 rule 4). |
| Independent of capabilities | Exercisable with no capability declared. Reads and writes no capability, evidence, or decision-history row. |
| Reason required | A legal-identity approval with no stated ground is refused. Persisted in `provider_organizations.standing_decision_reason` (V15). |
| Own audit event | `PROVIDER_ORGANIZATION_LEGAL_IDENTITY_ACCEPTED`, distinct from `PROVIDER_CAPABILITY_VETTED`. |
| Observable | The capability-decision response carries `organizationStatus`, so a caller can see that the decision did not move standing rather than inferring it from an absent field. |

`PENDING` → `VERIFIED` only. `SUSPENDED` and `BANNED` remain unreachable from any
endpoint, which is a **known open item**, not a settled part of this rule: they need their
own operator action and their own lifecycle, and no task currently owns them. Recorded
here so a later task does not mistake the four-value vocabulary for a four-value API.

An approval without a recorded `standing_decision_reason` remains representable on purpose:
it is how a Provider accepted before V15 exists looks. A fabricated reason would be worse
than a missing one, because a missing one is visibly missing.

---

## 3. Flow matrix

Mandatory flow → module mapping (fixed):

| Flow | Owning module(s) |
| --- | --- |
| `SF` | `users` + `assets` |
| `MF1` | `inspectionrequests` |
| `MF2` | `inspections` |
| `MF3` | `inspections` |
| `MF4` | `inspections` + `infrastructure` (partner ports) + `notifications` |
| `MF5` | `maintenance` |

### 3.1 Supporting Flow (SF)

| Step | Target | Implemented state | Status | Gap |
| --- | --- | --- | --- | --- |
| SF-01 Client organization self-registration | `POST /api/v1/auth/register`, creates organization + first `CLIENT` in one transaction | Present. `BrowserAuthController:57`, `MobileAuthController:40`. Assigns only `CLIENT` in `CUSTOMER_ORGANIZATION`. | `implemented` | — |
| SF-02 Provider onboarding, capability declaration, evidence submission | `POST /api/v1/provider-organizations` | Implemented at backend `451a2af` (fix round 1: see §0.2). `ProviderOrganizationController.onboard` + `ProviderOnboardingService.onboard`. One transaction writes `provider_organizations`, one row per declared capability, its evidence rows, `users.provider_id`, and one `PROVIDER_ORGANIZATION_ONBOARDED` audit row. Every capability lands PENDING; no order, quotation or clearance is created. | `implemented` | — |
| SF-03 Operator vetting, per capability | `GET /api/v1/provider-organizations/{providerId}/capabilities`, `POST /api/v1/provider-organizations/{providerId}/capabilities/{capability}/decisions`, `POST /api/v1/provider-organizations/{providerId}/standing/decisions` | Implemented at backend `451a2af` (fix round 1: see §0.2). `ProviderVettingController` (capability decisions, `PLATFORM_OPERATOR` only) and `ProviderOrganizationController.capabilities` (read, own provider or any for the `VET_PROVIDER` duty). The third endpoint is **organization standing**, added by the fix round and described under §2.6. | `implemented` | — |
| SF-04 Asset profile + airspace pre-check | Asset CRUD present; airspace pre-check warning | Asset CRUD implemented. **No airspace column, no lookup, no `AIRSPACE_CHECK_PENDING` / `RESTRICTED_AIRSPACE` state anywhere in source or migrations.** | `partial` | `GAP-F-02`, `GAP-D-15` |
| SF-05 Due cycle → one MF1 request package | `assets` publishes `InspectionScheduleDue`; `inspectionrequests` consumes and creates the request | Publisher exists (`InspectionScheduleDuePublisher`, `assets/events/InspectionScheduleDue`). **No listener exists; `inspectionrequests` has zero services.** | `partial` | `GAP-F-03` |
| SF-05 schedule proposal review by business reviewer | Target reviewer is `PLATFORM_OPERATOR` | `ScheduleProposalController:47` hardcodes `SERVICE_MANAGER` or `ADMIN`. | `partial` | `GAP-R-08` |

### 3.2 MF1 — Survey request, quotation sourcing, conditional funding

| Step | Target | Implemented state | Status | Gap |
| --- | --- | --- | --- | --- |
| MF1-01 Create request, direct selection or open RFQ | `inspectionrequests` service + API | Entities and repositories exist. **Zero services, zero controllers.** No HTTP path can create a request. | `target-only` (runtime) | `GAP-F-04`, `GAP-A-02` |
| MF1-02 Optional Operator RFQ broadcast | Notification + provider matching | Not present. | `target-only` | `GAP-F-26` (orphan) |
| MF1-03 Versioned Provider quotation | Capability-gated, excludes Platform AI/data/storage charges | Entity + immutability constraints exist. No service, no API, no capability gate, no charge-exclusion rule. | `partial` | `GAP-F-05` |
| MF1-04 Client revision/accept | Versioned revisions | Version columns exist; no service. | `partial` | `GAP-A-02` |
| MF1-05 Order policy snapshot | `locked_commission_rate`, `locked_review_period_days`, `locked_advance_funding_rate`, `locked_cancellation_policy`, `locked_terms_snapshot` | `inspection_service_orders` has `scope_snapshot`, `deliverables`, `payment_terms` only. **None of the `locked_*` columns exist.** | `partial` | `GAP-F-06`, `GAP-D-06` |
| MF1-06 Signature and conditional funding | Authorized partner product; no Platform custody | No escrow code of any kind in `src/main/java`; `escrow_transactions` has no DDL. | `target-only` | `GAP-F-07`, `GAP-D-10` |
| MF1 cancellation / weather force majeure (MF1 §2) | Order-snapshotted cancellation terms; BR-13, BR-14 | No cancellation terms, no policy source. | `target-only` | `GAP-F-06`, `GAP-D-08` |

### 3.3 MF2 — Drone mission planning and airspace clearance

| Step | Target | Implemented state | Status | Gap |
| --- | --- | --- | --- | --- |
| MF2-01 GSD → AGL and capture distance | Mission-specific, equipment-derived | No mission aggregate. `drone_mission_plans` and `mission_shot_items` have no DDL. | `target-only` | `GAP-F-08`, `GAP-D-09` |
| MF2-02 Forward/side overlap | SOW-specific | Absent. | `target-only` | `GAP-F-08` |
| MF2-03 Structural shot list + gimbal pitch; waypoints optional | Shot items required; waypoints optional | Absent. | `target-only` | `GAP-F-08` |
| MF2-04 Airspace digital clearance | Lookup ≠ clearance; `AIRSPACE_MANUAL_VERIFY_REQUIRED` on outage | Absent entirely. | `target-only` | `GAP-F-02`, `GAP-F-09` |
| MF2-05 Legal flight clearance, certified pilot, drone registration, conflict-of-interest | Recorded before approval | `inspection_assignments` carries `inspector_user_id` and `assigned_by_user_id` only. No credential/licence linkage, no conflict check. | `target-only` | `GAP-F-10`, `GAP-D-02` |
| MF2-06 Provider Manager approves plan, issues mission package, `READY_FOR_FLIGHT` | Order transitions to `READY_FOR_FLIGHT` | **`READY_FOR_FLIGHT` does not exist in any enum or CHECK constraint.** Order status set is `CONFIRMED, ASSIGNMENT_PENDING, READY_FOR_INSPECTION, IN_PROGRESS, COMPLETED, CANCELLED`. | `target-only` | `GAP-F-09` |

### 3.4 MF3 — Field survey, evidence, AI verification, QA report

| Step | Target | Implemented state | Status | Gap |
| --- | --- | --- | --- | --- |
| MF3-01 Start assigned session | Assigned Inspector only, mission-linked | `InspectionController` is class-level `hasRole('INSPECTOR')` with assignment scoping in service. **`inspections` has no `mission_plan_id`; execution is not mission-linked.** | `partial` | `GAP-F-11` |
| MF3-02 Chunked upload to MinIO | Server-computed SHA-256, retry-safe | Implemented. `EvidenceService:74` computes checksum; `uq_evidence_inspection_checksum` and `uq_evidence_work_log_checksum` reject duplicates; object key is `inspections/{inspectionId}/{objectId}`. | `implemented` | — |
| MF3-03 Spatial telemetry: 3D GPS, AGL, gimbal angle, timestamp | Per-file spatial metadata | `evidence` stores `latitude`, `longitude`, `capture_time`. **No altitude/AGL, no gimbal angle, no 3D coordinate.** | `partial` | `GAP-F-13`, `GAP-D-15` |
| MF3-04 YOLO candidates + GSD-derived physical defect size in mm | Multiply pixel size by mission GSD | `AiInferencePort` exists; candidates persist. **No GSD anywhere in the codebase, so no physical-size derivation.** | `partial` | `GAP-F-12` |
| MF3-05 Inspector confirm/modify/reject, manual finding, checklist | Non-official until verified | Implemented. `AiFindingCandidateStatus`, `VerifiedFindingSource`, `VerifiedFindingStatus`, manual finding endpoint. | `implemented` | — |
| MF3-06 Platform LLM narrative draft | Labelled draft, not released directly | `ReportDraftPort` + `ai-draft` endpoint exist. | `implemented` | — |
| MF3-07 **Author verification and edit by the authoring Inspector** | Required before submit; BR-23 | **Not implemented. The workflow uses peer review instead:** `peer_reviews` table, `PeerReviewDecision{PENDING, CHANGES_REQUESTED, APPROVED}`, report status `AWAITING_PEER_REVIEW`, and `technically_approved_at`. `report_versions` has **no** author-verification or completeness column. | `target-only` | `GAP-F-14`, `GAP-D-04`, `GAP-D-05` |
| MF3-08 Provider Manager completeness check with reasons | `PROVIDER_MANAGER` checks SOW deliverables | Absent. `POST /reports/{id}/versions/{v}/review` is `hasRole('INSPECTOR')` — the peer-review decision endpoint, not a Manager completeness check. | `target-only` | `GAP-F-14`, `GAP-A-05` |
| MF3-09 Manager releases report; review clock starts from snapshot | BR-24: release requires author verification **and** Manager completeness | `POST /reports/{id}/versions/{v}/release` is `hasRole('SERVICE_MANAGER')` with **no verification precondition**, because neither state exists. Review-period snapshot does not exist. | `partial` | `GAP-F-15` |
| BR-25 Client visibility | Unverified candidates and unreleased drafts hidden | Service-scoped reads exist. | `implemented` | — |

### 3.5 MF4 — Report acceptance, settlement, internal complaints

| Step | Target | Implemented state | Status | Gap |
| --- | --- | --- | --- | --- |
| MF4-01 Client reviews released report | Own-organization scope | `GET /reports`, `GET /reports/{id}`, evidence content endpoint. | `implemented` | — |
| MF4-02a Client accepts | Immutable accepted version | `POST /reports/{id}/versions/{v}/client-decision` (`hasRole('CLIENT')`); `V10` added `client_decision_by_user_id`/`client_decision_reason` with a `REVISION_REQUESTED` reason CHECK. | `implemented` | — |
| MF4-02b Deemed acceptance on snapshotted `T_rev` | Only when terms expressly provide it | Absent. No review-period snapshot, no timer. | `target-only` | `GAP-F-16`, `GAP-D-06` |
| MF4-03 Settlement `C = r × B`, single commission | Partner-coordinated; Platform not custodian | No commission concept anywhere in `src/main/java`. `escrow_transactions` has no DDL. `invoices` has no commission/platform-fee split. | `target-only` | `GAP-F-18`, `GAP-D-10`, `GAP-D-14` |
| MF4-04 Clarification request → corrected report | Distinct clarification state | Only `REVISION_REQUESTED` exists; there is no clarification state distinct from revision. | `partial` | `GAP-A-08` |
| MF4-05 Complaint filing, order-scoped | Client or Provider | `dispute_tickets` and `dispute_evidence` have no DDL, entity, or service. | `target-only` | `GAP-F-17`, `GAP-D-11` |
| MF4-06 Complaint state + conditional partner hold | Only where product and terms support | Absent. | `target-only` | `GAP-F-18` |
| MF4-07/08 Operator internal outcome under Platform Terms | Not a legal arbitration | Absent. No Operator role exists to hold this duty. | `target-only` | `GAP-F-17`, `GAP-R-07` |

### 3.6 MF5 — Maintenance, before/after evidence, retention

| Step | Target | Implemented state | Status | Gap |
| --- | --- | --- | --- | --- |
| MF5 module runtime | Services and API | **The `maintenance` module has 10 entities and 10 repositories and zero services and zero controllers.** Nothing is reachable over HTTP. | `target-only` | `GAP-F-19`, `GAP-A-04` |
| MF5-01 Ticket from verified finding in an accepted report | BR-31 | `maintenance_tickets.accepted_report_version_id` NOT NULL FK + `maintenance_ticket_findings` junction exist. **No service enforces "at least one finding", and no CHECK requires a finding row.** | `partial` | `GAP-F-22` |
| MF5-02 Maintenance capability gate before quotation | BR-05 capability gate | No capability model exists. | `target-only` | `GAP-F-21`, `GAP-R-05` |
| MF5-03 Maintenance order policy snapshot | Commission, funding, retention, warranty snapshots | `maintenance_orders` has `scope_snapshot`, `approved_amount`, `payment_terms`. **No `locked_*`, `retention_*`, `locked_warranty_days`, or `warranty_end_date`.** | `partial` | `GAP-F-23`, `GAP-D-07` |
| MF5-04 Assigned Engineer executes; **mandatory paired before/after evidence** | BR-35: completion strictly requires a verified pair | `evidence.evidence_kind` includes `BEFORE_MAINTENANCE` / `AFTER_MAINTENANCE`, but **no constraint requires a pair**, and no maintenance upload endpoint exists. | `partial` | `GAP-F-20`, `GAP-D-17` |
| MF5-05 Change order pauses extra work | Single `PENDING_APPROVAL` change at a time | Tables exist; no service, no single-pending constraint. | `target-only` | `GAP-F-25` |
| MF5-06 Client accepts / rework / re-inspection | Three distinct decisions | `resolution_decision` CHECK allows `ACCEPT_RESOLUTION, REQUEST_REWORK, REQUEST_REINSPECTION`; no service. | `partial` | `GAP-A-04` |
| MF5-07 Milestone settlement, single commission, warranty start | Partner-coordinated | Absent. | `target-only` | `GAP-F-18`, `GAP-F-23` |
| MF5-08 Warranty retention release, no second commission | Operator coordinates only when adopted | Absent. | `target-only` | `GAP-F-23` |
| BR-37 Re-inspection creates a linked request | Linked ad hoc request returning to MF1/MF2 | **`inspection_requests.linked_maintenance_ticket_id` exists in `V6` as a bare `UUID` with no foreign key, and nothing writes it.** | `target-only` | `GAP-F-24`, `GAP-D-16` |

### 3.7 Cross-cutting: notification and dashboard

| Capability | Target | Implemented state | Status | Gap |
| --- | --- | --- | --- | --- |
| Workflow notifications | Notify next responsible actor after material transitions | `notifications` has one entity and one repository. No service, no listener, no controller. MF1 Q5, MF4 Q4, and every exception path that requires notification are unserved. | `target-only` | `GAP-F-26` (**ORPHAN**) |
| Dashboard / analytics (FE-08) | Role- and scope-filtered dashboards | `dashboard` contains only `package-info.java`. | `target-only` | `GAP-F-27` (**ORPHAN**) |

---

## 4. API matrix

### 4.1 Envelope and error contract

| Concern | Target | Implemented | Status |
| --- | --- | --- | --- |
| Success envelope | `{ success, message, data }`; `204` and binary streams unwrapped | `ApiResponse<T>(boolean success, String message, T data)` — matches. | `implemented` |
| Error shape | RFC 9457 `ProblemDetail` with stable `code` and `traceId` | Present in the global handler. No cross-client fixture pins it. | `partial` (`GAP-A-11`) |
| API versioning | `/api/v1` | All controllers under `/api/v1`. | `implemented` |
| OpenAPI | Available in development, protected in production | `springdoc-openapi-starter-webmvc-ui` present; `application-prod.yml` configures it. **No checked-in or published API contract artifact exists.** | `partial` (`GAP-A-09`) |

### 4.2 Endpoint inventory — implemented vs target

`@PreAuthorize` values are quoted verbatim from the source.

| Endpoint | Target role | Implemented `@PreAuthorize` | Status | Gap |
| --- | --- | --- | --- | --- |
| `POST /api/v1/provider-organizations` | `PROVIDER_MANAGER` declares capabilities | `hasRole('PROVIDER_MANAGER')` | `implemented` | — |
| `GET /api/v1/provider-organizations/{providerId}/capabilities` | `PROVIDER_MANAGER` own org, `PLATFORM_OPERATOR` any | `hasAnyRole('PLATFORM_OPERATOR', 'PROVIDER_MANAGER')`, foreign provider refused 403 in service | `implemented` | — |
| `POST /api/v1/provider-organizations/{providerId}/capabilities/{capability}/decisions` | `PLATFORM_OPERATOR` only | class-level `hasRole('PLATFORM_OPERATOR')` | `implemented` | — |
| `POST /api/v1/provider-organizations/{providerId}/standing/decisions` | `PLATFORM_OPERATOR` accepts the legal identity (§2.6) | class-level `hasRole('PLATFORM_OPERATOR')` | `implemented` | — |
| Mission plan CRUD + approve | `PROVIDER_MANAGER` manage, `INSPECTOR` manage assigned, `CLIENT` view agreed | **absent** | `target-only` | `GAP-A-03` |
| Inspection request create / RFQ | `CLIENT` own org | **absent** — `inspectionrequests` has no controller | `target-only` | `GAP-A-02` |
| Quotation create / revise / decide | `PROVIDER_MANAGER` own org, `CLIENT` decide | **absent** | `target-only` | `GAP-A-02` |
| Service order confirm | `CLIENT` decide | **absent** | `target-only` | `GAP-A-02` |
| Maintenance ticket / assessment / order / work log / evidence | `CLIENT`, `MAINTENANCE_ENGINEER` assigned, `PROVIDER_MANAGER` own org | **absent** — `maintenance` has no controller | `target-only` | `GAP-A-04` |
| `GET /api/v1/asset-categories` | all authenticated | `isAuthenticated()` | `implemented` | — |
| `POST/PUT/DELETE /api/v1/asset-categories/**` | `PLATFORM_ADMIN` | `hasRole('ADMIN')` | `partial` (role rename) | `GAP-R-01` |
| `GET/POST /api/v1/assets` | `CLIENT` own org manage; `PLATFORM_OPERATOR`/`PLATFORM_ADMIN` view | `hasRole('CLIENT')` / `hasAnyRole('CLIENT','ADMIN')` | `partial` | `GAP-A-07` |
| `GET /api/v1/assets/pending-review`, `POST /{assetId}/review` | `PLATFORM_OPERATOR` | `hasRole('SERVICE_MANAGER')` | `partial` | `GAP-R-08`, `GAP-A-13` |
| `GET /api/v1/inspection-schedules`, `/{id}/pause`, `/{id}/activate` | `CLIENT` | `hasAnyRole('CLIENT','ADMIN')` / `hasRole('CLIENT')` | `implemented` | — |
| `GET /api/v1/schedule-proposals` | `CLIENT`, reviewer, `PLATFORM_ADMIN` | `hasAnyRole('CLIENT','SERVICE_MANAGER','ADMIN')` | `partial` | `GAP-R-08` |
| `POST /schedule-proposals/{id}/review` | `PLATFORM_OPERATOR` | `hasRole('SERVICE_MANAGER')` | `partial` | `GAP-R-08` |
| `POST /schedule-proposals/{id}/select` | `CLIENT` | `hasRole('CLIENT')` | `implemented` | — |
| `POST /api/v1/assets/{assetId}/documents` | `CLIENT` own org | `hasAnyRole('CLIENT','ADMIN')` | `partial` | `GAP-A-13` |
| `GET /assets/{assetId}/documents`, `/{documentId}/content` | `CLIENT` own org, `PROVIDER_MANAGER` view own provider scope, `PLATFORM_ADMIN` audit | `hasAnyRole('CLIENT','ADMIN','SERVICE_MANAGER')` | `partial` | `GAP-A-07`, `GAP-A-13` |
| `GET /api/v1/inspections/**` (assignments, start, checklist, evidence, findings) | `INSPECTOR` assigned only | class-level `hasRole('INSPECTOR')`, assignment scope in service | `implemented` | — |
| `GET /api/v1/reports`, `/{reportId}` | `CLIENT` released, `PROVIDER_MANAGER` own provider, `INSPECTOR` authored | `hasAnyRole('INSPECTOR','SERVICE_MANAGER','CLIENT')` — three roles at method level; isolation rests entirely on service scoping | `partial` | `GAP-A-06` |
| `POST /inspections/{id}/report`, `PUT .../narrative`, `POST .../versions`, `POST .../submit-review` | `INSPECTOR` (author) | `hasRole('INSPECTOR')` | `implemented` | — |
| `PUT /reports/{r}/versions/{v}/reviewer` | `PROVIDER_MANAGER` assigns reviewer | `hasRole('SERVICE_MANAGER')` | `partial` | `GAP-A-05` |
| `POST /reports/{r}/versions/{v}/review` | Target: Manager completeness. Implemented: peer-review decision by an Inspector | `hasRole('INSPECTOR')` | `target-only` (wrong behavior) | `GAP-A-05` |
| `POST /reports/{r}/versions/{v}/release` | `PROVIDER_MANAGER` **after** author verification + completeness | `hasRole('SERVICE_MANAGER')`, no precondition | `partial` | `GAP-F-15` |
| `POST /reports/{r}/versions/{v}/client-decision` | `CLIENT` accept or request revision | `hasRole('CLIENT')` | `partial` | `GAP-A-08` |
| `GET /reports/{r}/versions/{v}/evidence/{e}/content` | `CLIENT` own org | `hasRole('CLIENT')` | `implemented` | — |
| `/api/v1/auth/**` (csrf, register, login, password/setup, refresh, logout, logout-all, me, password/change) | all roles | authenticated | `implemented` | — |
| `/api/v1/mobile/auth/**` | mobile profile | authenticated | `implemented` | — |
| `/api/v1/platform/users/**` (create, reset-password, roles, status) | `PLATFORM_ADMIN`; roles/status may not mint `PLATFORM_OPERATOR` business powers without duty separation | class-level `hasRole('ADMIN')` | `partial` | `GAP-R-07` |

**Endpoint names recorded as required by the Task 1.4 brief** ("final endpoint names must
be recorded in the contract matrix"): `POST /api/v1/provider-organizations`,
`GET /api/v1/provider-organizations/{providerId}/capabilities`,
`POST /api/v1/provider-organizations/{providerId}/standing/decisions` (added by the Task 1.4
fix round; see §2.6 for why organization standing needed its own endpoint),
`POST /api/v1/provider-organizations/{providerId}/capabilities/{capability}/decisions`.
These are binding on Task 1.4.

### 4.3 Client-side role and portal policy

| Concern | Target | Implemented | Status | Gap |
| --- | --- | --- | --- | --- |
| Role union | 6 canonical values | `ROLE_CODES = ['ADMIN','CLIENT','SERVICE_MANAGER','INSPECTOR','MAINTENANCE_ENGINEER']` | `partial` | `GAP-R-09` |
| Portal model | 3 zones | `PORTAL_ROLE_ACCESS = { admin, client, operations }`. `operations` lumps `PROVIDER_MANAGER`+`INSPECTOR`+`MAINTENANCE_ENGINEER`; `admin` collapses both platform roles. | `partial` | `GAP-R-09` |
| Actor-zone typing | Typed union | `actorZone: string` (untyped) | `partial` | `GAP-R-10` |
| Provider identity in session | `providerId` present | `AuthUser` has `organizationId` only, no `providerId` | `partial` | `GAP-R-10` |
| Asset review visibility | `PLATFORM_OPERATOR` | `asset-review: ['SERVICE_MANAGER']` | `partial` | `GAP-R-12` |
| Capability-gated provider UI | Maintenance screens hidden/disabled without `MAINTENANCE = VERIFIED` | `maintenance: ['SERVICE_MANAGER','MAINTENANCE_ENGINEER']`, no capability input | `target-only` | `GAP-R-13` |
| Mobile role/zone awareness | Assigned-work only, zone-aware | **No role or zone identifier appears anywhere in `mobile/lib`.** Access depends entirely on backend 403s. | `target-only` | `GAP-R-11` |

### 4.4 Mobile consumed API surface

The complete set of backend paths the Flutter client calls today:

| Path | Purpose | Gap |
| --- | --- | --- |
| `/mobile/auth/refresh` | Token rotation | — |
| `/assets` | Asset list | — |
| `/inspections/assignments` | Assigned missions | — |
| `/inspections/start` | Start session | — |

Mobile consumes **no** checklist, evidence, finding, report, maintenance, or complaint
endpoint. `mobile/lib/features/` contains `assets`, `auth`, `inspections`, `profile`,
`tasks` — there is **no `maintenance` feature directory**, although MF5 requires the
Maintenance Engineer to upload paired before/after evidence from mobile. `GAP-A-10`.

Token storage uses `flutter_secure_storage`, matching the documented mobile credential
rule. Recorded as conformant.

---

## 5. Role and actor-zone gap register

| ID | Gap | Documented | Implemented | Owner |
| --- | --- | --- | --- | --- |
| `GAP-R-01` | Role code set | 6 canonical codes | 5 legacy codes; `PLATFORM_OPERATOR` and `PROVIDER_MANAGER` absent, `SERVICE_MANAGER` present | **1.1**, **1.2** |
| `GAP-R-02` | Actor-zone vocabulary | `PLATFORM_GOVERNANCE`, `CUSTOMER_ORGANIZATION`, `SERVICE_PROVIDER` | `PLATFORM`, `CUSTOMER_ORGANIZATION`, `SERVICE_WORKFORCE` (enum + `V3` CHECK) | **1.2** |
| `GAP-R-03` | Provider linkage column | `users.provider_id` FK | `users` has `organization_id` only; `grep provider_id` across all migrations returns nothing | **1.2** |
| `GAP-R-04` | Provider Organization aggregate | Table + JPA entity | Absent entirely | **1.3** |
| `GAP-R-05` | Capability aggregate and eligibility gate | `ProviderCapabilityType`, `ProviderCapabilityStatus`, evidence, decision history | Absent; no quotation, order, or assignment path is capability-gated | **1.3** |
| `GAP-R-06` | Vetting status vocabulary conflict | Report 3 edits require four outcomes but name none; `business-flows.md` SF-03 uses four; `database-design.md` `provider_organizations.status` uses `PENDING/VERIFIED/SUSPENDED/BANNED` | Single org-level status column with the wrong vocabulary | **1.3** (bind §2.4), **7.1** (rewrite SF-03) |
| `GAP-R-07` | Separation of duties | `PLATFORM_ADMIN` technical vs `PLATFORM_OPERATOR` business; Provider may not self-approve | Only `ADMIN` exists; `PlatformUserController` is uniformly `hasRole('ADMIN')`; no Operator role to separate from | **1.2** (add roles), **1.4** (scoping) |
| `GAP-R-08` | Schedule-proposal reviewer | `PLATFORM_OPERATOR` | `SERVICE_MANAGER` hardcoded at `ScheduleProposalController:47` | **1.2** |
| `GAP-R-09` | Frontend role union and portal model | 6 roles, 3 zones | 5 roles, 3 portals that collapse the target zones | **6.1** |
| `GAP-R-10` | Frontend session typing | Typed zone + `providerId` | `actorZone: string`; no `providerId` field | **6.1** |
| `GAP-R-11` | Mobile role/zone awareness | Assigned-work scoping | No role or zone concept in `mobile/lib` | **6.4** |
| `GAP-R-12` | Frontend business-review visibility | `PLATFORM_OPERATOR` | `asset-review: ['SERVICE_MANAGER']` | **6.1** |
| `GAP-R-13` | Frontend capability gating | Maintenance UI gated on `MAINTENANCE = VERIFIED` | No capability input to the UI at all | **6.3** |
| `GAP-R-14` | Role policy API | `allowedZone(role)`, `canPerform(role, action)` | `RolePolicy` exposes only `validate(zone, orgId, roles)`; neither method exists | **1.1**, **1.2** |
| `GAP-R-15` | Provider-scope grant path on SF/WF1 endpoints | `PROVIDER_MANAGER` may view own-provider asset and document scope | No provider role exists to grant; `SERVICE_MANAGER` is the only service-zone role and has no provider identity | **1.2**, **6.3** |

**Role-area gap count: 15.**

---

## 6. Flow, API, and data gap register

### 6.1 Flow gaps

| ID | Gap | Owner |
| --- | --- | --- |
| `GAP-F-01` | **Runtime half CLOSED by Task 1.4** (backend `451a2af`, fix round 1): SF-02 and SF-03 are `implemented` per §3.1, with organization standing decided by its own operator action rather than as a side effect of a capability verdict (§2.6). **Text half still open**: `business-flows.md` SF-03 still grants org-wide `VERIFIED` and blocks all quotation rights, contradicting the capability-scoped BR-05 gate (C-4). | **7.1** (SF-03 text) |
| `GAP-F-02` | Asset-level airspace pre-check absent; no `RESTRICTED_AIRSPACE`, `AIRSPACE_CHECK_PENDING`, or `AIRSPACE_MANUAL_VERIFY_REQUIRED` state exists in any form. | **2.3** |
| `GAP-F-03` | Due-cycle publisher has no consumer. `InspectionScheduleDuePublisher` emits; nothing in `inspectionrequests` listens, so MF1 request packages are never generated. | **2.1** |
| `GAP-F-04` | MF1 request creation and RFQ sourcing have no runtime. | **2.1** |
| `GAP-F-05` | MF1 quotation has no capability gate and no Platform-AI/data/storage charge exclusion. | **2.1** (gate), **2.2** (charges) |
| `GAP-F-06` | MF1 order policy snapshot absent; no cancellation terms and no `T_rev` review period. | **2.2** |
| `GAP-F-07` | MF1 conditional funding absent; no escrow or partner integration of any kind. | **4.2** |
| `GAP-F-08` | MF2 mission plan, shot items, GSD, overlap, AGL, gimbal all absent. | **2.3** |
| `GAP-F-09` | MF2 clearance/permit state absent and `READY_FOR_FLIGHT` does not exist as a status. | **2.3** |
| `GAP-F-10` | MF2 pilot-credential, drone-registration, and conflict-of-interest checks absent. | **2.3** |
| `GAP-F-11` | MF3 execution is not mission-linked; `inspections` has no `mission_plan_id`. | **3.1** |
| `GAP-F-12` | GSD-derived physical defect size (mm) cannot exist; no GSD value is stored anywhere. | **3.1** (with **2.3**) |
| `GAP-F-13` | Spatial telemetry depth missing: no AGL, no gimbal angle, no 3D coordinate on `evidence`. | **3.1** |
| `GAP-F-14` | MF3 uses peer review instead of author verification plus Provider Manager completeness. | **3.2** |
| `GAP-F-15` | Report release is not gated on author verification or Manager completeness (BR-24 unenforced). | **3.2** |
| `GAP-F-16` | MF4 deemed-acceptance timer absent. | **4.2** |
| `GAP-F-17` | MF4 complaint filing, evidence, and Operator internal outcome absent. | **4.1** |
| `GAP-F-18` | MF4/MF5 settlement, commission `C = r × B`, hold, and retention release absent. | **4.2**, **5.3** |
| `GAP-F-19` | The entire MF5 runtime is absent: 10 entities, 10 repositories, 0 services, 0 controllers. | **5.1**, **5.2** |
| `GAP-F-20` | Mandatory before/after evidence pairing is not enforced by any constraint. | **5.2** |
| `GAP-F-21` | MF5 has no maintenance-capability gate. | **5.1** |
| `GAP-F-22` | BR-31 ("at least one verified defect from an accepted report") is not enforced: the junction table exists but no service or CHECK requires a finding. | **5.1** |
| `GAP-F-23` | MF5 retention and warranty snapshot, warranty clock, and release absent. | **5.2**, **5.3** |
| `GAP-F-24` | BR-37 re-inspection linkage is a bare column with no foreign key and no writer. | **5.3** |
| `GAP-F-25` | MF5 Q3 single-pending-change-request rule absent. | **5.2** |
| `GAP-F-26` | Notification delivery runtime absent although MF1 Q5, MF4 Q4, and FE-08 all require it. | **ORPHAN** |
| `GAP-F-27` | `dashboard` is a package-only module; FE-08 has no runtime and no Report 5 case. | **ORPHAN** |

**Flow-area gap count: 27** (25 owned, 2 orphan).

### 6.2 API gaps

| ID | Gap | Owner |
| --- | --- | --- |
| `GAP-A-01` | **CLOSED by Task 1.4** (backend `451a2af`, fix round 1). Four endpoints, recorded in §4.2 and listed under §2.6: onboarding POST, capabilities GET, per-capability decision POST, and legal-identity standing POST. | — (closed) |
| `GAP-A-02` | `inspectionrequests` has zero controllers, so **no HTTP path can create a request, quotation, or order**. MF1 is unreachable, yet `inspections` requires a confirmed service order to start. | **2.1** |
| `GAP-A-03` | No mission-plan endpoint of any kind. | **2.3** |
| `GAP-A-04` | `maintenance` has zero controllers: no ticket, assessment, order, work-log, evidence, or completion endpoint. | **5.1**, **5.2** |
| `GAP-A-05` | Report peer-review endpoints contradict the target: `PUT .../reviewer` is `SERVICE_MANAGER`, `POST .../review` is `INSPECTOR`. Neither is a Provider Manager completeness check. | **3.2** |
| `GAP-A-06` | `GET /reports` and `GET /reports/{id}` grant three roles at the method level; cross-provider isolation depends entirely on service-level scoping with no cross-client contract test. | **3.2**, **8.1** |
| `GAP-A-07` | Asset endpoints mix zones (`hasAnyRole('CLIENT','ADMIN')`) with no provider-scoped grant path, so the documented `PROVIDER_MANAGER` asset-view scope cannot be expressed. | **1.2**, **6.3** |
| `GAP-A-08` | `client-decision` supports accept and revision only; no clarification state distinct from revision, no complaint branch. | **4.1** |
| `GAP-A-09` | No checked-in or published API contract artifact; springdoc exists in code only. | **8.1** |
| `GAP-A-10` | Mobile consumes only four paths and has no maintenance feature, though MF5 requires mobile before/after upload. | **6.4** |
| `GAP-A-11` | No cross-client Problem Details fixture pins `code`/`traceId`. On frontend `main` the `errorMessage`/problem-decoding logic is not shared; the Task 0.5 branch (`d28f700`) reports `problemError` duplicated in **4 files**, so the duplication will survive into Phase 6 unless it is consolidated there. | **8.1**, **6.1** |
| `GAP-A-12` | No legacy-role compatibility contract: nothing defines whether a client should reject, translate, or temporarily accept `ADMIN`/`SERVICE_MANAGER` during the migration window. | **1.2** |
| `GAP-A-13` | Asset review and asset-document endpoints authorize `SERVICE_MANAGER`, a role that will not exist after migration and carries no provider identity. | **1.2**, **6.3** |

**API-area gap count: 13.**

### 6.3 Data gaps

| ID | Gap | Owner |
| --- | --- | --- |
| `GAP-D-01` | `provider_organizations` is documented in §6.1 with a full column list and is counted as implemented in §12, but **has no `CREATE TABLE` in any migration and no JPA entity**. §12's "37 application tables" only closes by wrongly including it. | **1.3** (create), **7.1** (correct the doc) |
| `GAP-D-02` | Every documented `provider_id` column is fictional. `grep -rn provider_id` over all migrations returns nothing, yet `users`, `inspection_quotations`, `inspection_service_orders`, `maintenance_orders`, `drone_mission_plans`, `escrow_transactions`, and `dispute_tickets` are all documented with one. Provider scoping is unrepresentable. | **1.3**, **2.1**, **2.2**, **5.1** |
| `GAP-D-03` | `security_audit_events` has no `organization_id`, `entity_type`, `entity_id`, or `details`. Only `actor_user_id`/`subject_user_id` exist. BR-38 (audit every material transition) is unrepresentable because workflow events cannot reference an entity. | **1.4** (first consumer), **7.1** (document) |
| `GAP-D-04` | `report_versions` has no author-verification or completeness columns. `V7` supplies `created_by_user_id`, `submitted_at`, `technically_approved_at`, `released_at`, `accepted_at`; `V10` adds only the two Client-decision columns. | **3.2** |
| `GAP-D-05` | `ck_report_versions_status` allows `DRAFT, AWAITING_PEER_REVIEW, CHANGES_REQUESTED, TECHNICALLY_APPROVED, RELEASED, REVISION_REQUESTED, ACCEPTED`. The target requires `AUTHOR_VERIFIED`, `MANAGER_RELEASED`, `CLIENT_ACCEPTED`, `CLIENT_CLARIFICATION`, `COMPLAINT`. | **3.2** |
| `GAP-D-06` | `inspection_service_orders` lacks `locked_commission_rate`, `locked_review_period_days`, `locked_advance_funding_rate`, `locked_cancellation_policy`, `locked_terms_snapshot`. | **2.2** |
| `GAP-D-07` | `maintenance_orders` lacks `locked_*`, `retention_rate`, `retention_base`, `locked_warranty_days`, `warranty_end_date`. | **5.2**, **5.3** |
| `GAP-D-08` | `platform_configurations` has no DDL, so no published commercial policy can exist and `WF2-006` has no source. | **2.2** |
| `GAP-D-09` | `drone_mission_plans` and `mission_shot_items` have no DDL. | **2.3** |
| `GAP-D-10` | `escrow_transactions` has no DDL. | **4.2** |
| `GAP-D-11` | `dispute_tickets` and `dispute_evidence` have no DDL. | **4.1** |
| `GAP-D-12` | No capability table, no `(provider_id, capability)` unique key, no status CHECK. BR-41 is unrepresentable. | **1.3** |
| `GAP-D-13` | **CLOSED by Task 1.3** (V14): `provider_organizations.status` and `provider_capabilities.status` are two columns with two CHECK vocabularies, so a per-capability rejection and `ADDITIONAL_INFO_REQUIRED` are both expressible. **Extended by the Task 1.4 fix round**: the two axes are now also independently *reachable* — standing via its own endpoint and audit event (§2.6), capability status via its own. `SUSPENDED`/`BANNED` remain unreachable from any endpoint; no task owns that lifecycle yet. | — (closed); suspension lifecycle unowned |
| `GAP-D-14` | `invoices` has no commission or platform-fee split, so BR-36's single-commission rule and `WF3-007`/`WF4-004` are unrepresentable. | **4.2** |
| `GAP-D-15` | `evidence` has `latitude`, `longitude`, `capture_time` but no altitude/AGL, no gimbal angle, no 3D coordinate. `assets` has no airspace-restriction column. | **3.1**, **2.3** |
| `GAP-D-16` | `inspection_requests.linked_maintenance_ticket_id` (`V6:13`) is a bare `UUID` with **no foreign key** to `maintenance_tickets`. | **5.3** |
| `GAP-D-17` | No database constraint ties a maintenance work log to a `BEFORE_MAINTENANCE` + `AFTER_MAINTENANCE` pair, and no API path can create either. | **5.2** |
| `GAP-D-18` | `peer_reviews` has live DDL but appears **nowhere** in `database-design.md`'s 44-entry inventory, while `report_versions` references the peer-review workflow in prose. The documented inventory and the physical schema disagree in both directions. | **7.1** |
| `GAP-D-19` | Report 5 baseline is 33 cases: 13 Passed, 20 Pending, 0 Failed. Nine target cases (`WF2-005`–`WF2-007`, `WF3-005`–`WF3-008`, `WF4-004`–`WF4-005`) are Pending with no execution. FE-08 has zero cases. `FE01-T01`/`FE01-T02` are Pending. `WF1-005`–`WF1-010` are unallocated and must not be reused. | **7.2** |
| `GAP-D-20` | Report 5 internal staleness: `fe-01-…md:9` and `README.md:47` still say "15-case workbook totals" while the total is 33; `cover.md`'s change table skips version 1.4 which exists in `00-cover/record-of-changes.md`; `fe-02-…md` has UTF-8 mojibake (`Hi?u`, `organizationâ€™s`); a stale 15-case preview artifact sits in `outputs/`. | **7.2** |
| `GAP-D-21` | No Report 5 test ID exists for five of the seven mandatory negative obligations in §7: role migration, provider-capability independence, unassigned-workforce access, author-verification release, and before/after completion. Only cross-provider bid isolation (`WF2-005`) and partner fail-closed (`WF3-008`) have IDs, and both are Pending. | **7.2** |
| `GAP-D-22` | Document path prefixes are wrong throughout the plan and brief: they spell repository content as `docs/project-reference/…`, `docs/backend/…`, `docs/reports/…`, but this repository's content root has no nested `docs/` on `main`. Every such path in the plan fails to resolve. | **7.1** |

**Data-area gap count: 22.**

### 6.4 Gap totals

| Area | Gaps | Owned by a task | Orphan |
| --- | ---: | ---: | ---: |
| Role / actor-zone | 15 | 15 | 0 |
| Flow | 27 | 25 | 2 |
| API | 13 | 13 | 0 |
| Data | 22 | 21 | 1 (same as `GAP-F-26`) |
| **Total recorded** | **77** | **74** | **3** |

---

## 7. Negative test obligations

Every obligation below must fail closed and must be proven by a test that would actually
fail if the guard were removed. Existing Report 5 IDs are reused where they exist; new
cases stay `Pending` until executed.

| # | Obligation | What must be denied | Owning task(s) | Test artifact |
| --- | --- | --- | --- | --- |
| N-1 | **Legacy role migration** | `SERVICE_MANAGER` rows must not be silently reinterpreted. If the data cannot distinguish `PLATFORM_OPERATOR` from `PROVIDER_MANAGER`, migration stops at `blocked-by-baseline` and ambiguous rows are rejected rather than guessed. | 1.1, 1.2 | `RolePolicyTest`, `AdminUserServiceTest`, migration contract test |
| N-2 | **No maintenance-manager role** | `MAINTENANCE_PROVIDER_MANAGER` must not exist in any enum, role string, JWT claim, or UI role union. | 1.1, 6.1 | `RolePolicyTest` enum assertion; frontend role-union test |
| N-3 | **Provider capability independence** | Verifying `INSPECTION` must leave `MAINTENANCE` at its prior status. Rejecting `MAINTENANCE` must leave `INSPECTION` verified. All four combinations (neither, inspection only, maintenance only, both) plus a decision on an undeclared capability must be covered. | 1.3, 1.4 | `ProviderCapabilityDomainTest` (four combinations); `ProviderVettingApiIntegrationTest.platformOperatorVerifiesInspectionOnly_maintenanceRemainsPending_BR41` (over HTTP, asserting both persisted rows, the untouched organization standing, and `ProviderEligibilityFacade` before and after the standing decision); Report 5 case in 7.2 |
| N-4 | **Provider self-approval** | A `PROVIDER_MANAGER` attempting a capability decision must receive 403, not 400 or 500. The same applies to the legal-identity standing decision. | 1.4 | `ProviderAuthorizationScopeTest.providerManagerDecisionAttempt_returns403Forbidden`, `platformAdminDecisionAttempt_returns403Forbidden`, `clientDecisionAttempt_returns403Forbidden`, `providerManagerStandingDecisionAttempt_returns403Forbidden`, `platformAdminStandingDecisionAttempt_returns403Forbidden` |
| N-5 | **Capability-scoped commercial gating** | A maintenance-only verified Provider cannot quote inspection or receive a flight assignment. An inspection-only verified Provider cannot issue a maintenance quotation or receive a repair assignment. | 2.1, 5.1 | `ProviderEligibilityInspectionTest`, `ProviderEligibilityMaintenanceTest` |
| N-6 | **Cross-organization reads** | Client Org A cannot read Client Org B's assets, requests, orders, reports, tickets, or financials. Provider A cannot read Provider B's quotations, margins, workforce, orders, or raw flight evidence. | 2.1, 3.2, 5.1 | `ProviderAuthorizationScopeTest`; existing `WF1-003`, `WF1-016`, `WF1-019`, `WF2-005` |
| N-7 | **Unassigned workforce access** | An Inspector or Maintenance Engineer with no assignment cannot read or mutate the target inspection, checklist, evidence, report, work log, or ticket. Assignment scope is enforced before the record is loaded, not after. | 3.1, 5.2, 6.4 | `InspectionWorkflowTest`, mobile widget tests; new Report 5 case in 7.2 |
| N-8 | **Author-verification release gate** | A report cannot be released without the authoring Inspector's verification confirmation **and** a Provider Manager completeness check. A non-author Inspector cannot verify another author's draft. | 3.2 | `ReportAuthorVerificationTest`; new Report 5 case in 7.2 |
| N-9 | **Before/after completion gate** | Maintenance completion submission without a paired `BEFORE_MAINTENANCE` + `AFTER_MAINTENANCE` set on the same work log is rejected. | 5.2 | `MaintenanceEvidenceApiIntegrationTest`; new Report 5 case in 7.2 |
| N-10 | **Unsupported partner integration** | With no configured partner, or with a partner that does not support the requested operation, funding, settlement, hold, and retention-release paths are blocked. The order, report, and maintenance state is preserved unchanged. No claim of Platform custody anywhere. | 2.2, 4.2, 5.3 | `PaymentPartnerBoundaryTest`, `ComplaintHoldBoundaryTest`, `SettlementPolicyTest`; `WF3-008` (Pending) |
| N-11 | **Commission applied once** | Commission applies once to eligible VAT-exclusive value; a refund reverses it proportionally; a retention release earns no second commission. | 4.2, 5.3 | `SettlementPolicyTest`; `WF3-007`, `WF4-004`, `WF4-005` (Pending) |
| N-12 | **Accepted-report immutability** | An accepted report version cannot be updated; a correction creates a linked version. | 3.2, 4.1 | `InspectionReportApiIntegrationTest` |
| N-13 | **Complaint blocks deemed acceptance and release** | A timely complaint blocks deemed acceptance. An unresolved supported warranty complaint blocks eligible retention release. Concurrent accept and complaint serialize to one transition. | 4.1, 5.3 | `ComplaintWorkflowTest`, `MaintenanceWarrantyRetentionTest` |
| N-14 | **Evidence duplicate and integrity** | A duplicate SHA-256 within one inspection or one maintenance work log is rejected without creating a junk row. Missing GPS is recorded, not rejected. An object-storage path alone grants no access. | 3.1, 5.2 | `EvidenceServiceTest`, `EvidenceApiIntegrationTest`; `WF3-002` (Passed) |
| N-15 | **AI failure fallback** | YOLO or LLM unavailability never discards evidence and never blocks manual finding entry. Rejected or unverified candidates never reach Client-visible statistics or reports. | 3.1 | `InspectionWorkflowTest`; `WF3-003` (Passed) |
| N-16 | **Onboarding grants no downstream authority** | Provider onboarding must not create an accepted order, grant inspection or maintenance eligibility, or grant mission clearance. | 1.4 | `ProviderOnboardingApiIntegrationTest.onboardingGrantsNoCapabilityEligibilityThroughTheGate_N16` (asserted through `ProviderEligibilityFacade`, not only through the record) |
| N-17 | **Client-contract drift** | Web and mobile must decode the same success envelope, `204`, binary stream, and Problem Details with `code`/`traceId`, and must not silently break on legacy role strings. | 6.1, 6.4, 8.1 | Cross-client contract fixtures |
| N-18 | **Separation of duties** | `PLATFORM_ADMIN` cannot publish commercial policy or vet a Provider. `PLATFORM_OPERATOR` cannot administer platform security settings. | 1.2, 1.4 | `RolePolicyTest`, `ProviderVettingApiIntegrationTest` |

---

## 8. Unique root causes

The 77 recorded gaps reduce to these root causes. Fixing a root cause closes every gap
listed against it.

| Root cause | Gaps closed |
| --- | --- |
| R-A. Legacy five-role identity with no provider linkage and the wrong zone names | `GAP-R-01`, `GAP-R-02`, `GAP-R-03`, `GAP-R-14`, `GAP-A-12`, and the role-rename part of `GAP-R-08`, `GAP-A-07`, `GAP-A-13` |
| R-B. No Provider Organization aggregate or capability model | `GAP-R-04`, `GAP-R-05`, `GAP-R-06`, `GAP-D-01`, `GAP-D-02`, `GAP-D-12`, `GAP-D-13`, `GAP-F-01`, `GAP-A-01` |
| R-C. `inspectionrequests` is persistence-only | `GAP-F-03`, `GAP-F-04`, `GAP-A-02` |
| R-D. No commercial-policy or snapshot layer | `GAP-F-06`, `GAP-F-07`, `GAP-D-06`, `GAP-D-08` |
| R-E. MF2 mission planning absent | `GAP-F-08`, `GAP-F-09`, `GAP-F-10`, `GAP-A-03`, `GAP-D-09` |
| R-F. MF3 execution not mission- or telemetry-linked | `GAP-F-11`, `GAP-F-12`, `GAP-F-13`, `GAP-D-15` |
| R-G. Report workflow is peer review, not author verification | `GAP-F-14`, `GAP-F-15`, `GAP-D-04`, `GAP-D-05`, `GAP-A-05` |
| R-H. No complaint, settlement, or partner layer | `GAP-F-16`, `GAP-F-17`, `GAP-F-18`, `GAP-D-10`, `GAP-D-11`, `GAP-D-14` |
| R-I. `maintenance` is persistence-only | `GAP-F-19`, `GAP-F-20`, `GAP-F-21`, `GAP-F-22`, `GAP-F-23`, `GAP-F-24`, `GAP-F-25`, `GAP-A-04`, `GAP-D-07`, `GAP-D-16`, `GAP-D-17` |
| R-J. Clients still model the v1 role/portal world | `GAP-R-09`, `GAP-R-10`, `GAP-R-11`, `GAP-R-12`, `GAP-R-13`, `GAP-A-06`, `GAP-A-10`, `GAP-A-11` |
| R-K. Documentation has no enforced consistency check | `GAP-R-07`, `GAP-A-09`, `GAP-D-03`, `GAP-D-18`, `GAP-D-19`, `GAP-D-20`, `GAP-D-21`, `GAP-D-22` |
| R-L. No notification or dashboard runtime | `GAP-F-26`, `GAP-F-27` |

---

## 9. Orphan gaps requiring a controller ruling

These have no owning task in the plan. They are recorded here so they are not silently
dropped, and each needs a decision before the phase that depends on it.

| ID | Gap | Why it is orphaned | Recommendation |
| --- | --- | --- | --- |
| `GAP-F-26` | Notification delivery runtime. `notifications` has an entity and a repository but no service, listener, or controller. MF1 Q5 (notify quoting Providers on cancellation), MF3 Q5 (correction requests), MF4 Q4 (in-app retry/status when the notification gateway fails), FE-08, and Report 3 §3.9.2 all require it. No task in the plan owns `notifications`. | The plan allocates work by flow, and notification delivery is cross-flow. | Add a task, or assign to Task 4.1 with an explicit scope extension. **Blocking for MF1 Q5 and MF4 Q4 acceptance.** |
| `GAP-F-27` | `dashboard` is a package-only module and FE-08 has zero Report 5 cases. Report 5 states FE-08 is "an explicit, truthful coverage gap" and excludes it from the coverage denominator. | No task covers FE-08 or dashboards; the design spec defers dashboard to "after the underlying slices exist". | Confirm FE-08 stays out of this refactor's scope, and record that exclusion in Task 7.1 so Report 5 does not imply a passing feature. **Not blocking.** |
| `GAP-D-03` | Workflow audit-event entity reference. BR-38 requires auditing every assignment, approval, release, acceptance, dispute, and closure transition, but `security_audit_events` cannot reference a business entity. | Task 1.4 says "emit audit events" but does not own the schema change. | Task 1.3 owns the next capability migration and can add the four columns additively. **Confirm with the controller before Task 1.3 starts.** |

---

## 10. Rules for tasks building against this matrix

1. **Do not restate a target as implemented.** If a row says `target-only`, the work has
   not started. If it says `partial`, the named gap is the work.
2. **Every gap you close must be updated here in the same commit that closes it**, with
   the evidence (commit SHA, test name, executed result). A gap closed in code but still
   open in this matrix will be re-opened by the reviewer.
3. **Migration numbers are forward-only.** `V1`–`V11` are applied. `V12` exists on
   `refactor/wf1-contract`. Tasks 1.2, 1.3, 2.2, 2.3, 4.1, 4.2, 5.2, and 5.3 each add a
   new version and must re-check the highest applied version before choosing a number —
   the plan's illustrative `V12`–`V15` numbers are stale: Task 0.4 took `V12`, Task 1.3
   took `V14`, and the Task 1.4 fix round took `V15`. `V13` is applied on this branch, so
   the chain has a deliberate gap at `V12` until WF1 lands.
4. **Never introduce `MAINTENANCE_PROVIDER_MANAGER`** or any seventh role. If a
   requirement appears to need one, the requirement is wrong, not the role list.
5. **A capability decision never cascades.** If a code path, constraint, or UI action
   would let one capability's decision change another, that is a defect in the new code,
   not an interpretation of BR-41.
6. **Target-only integrations fail closed.** No adapter means the operation is blocked
   and the order/report state is preserved. A deterministic test fixture is acceptable
   evidence of contract behavior; it is never evidence that a real partner integration
   exists.
7. **Report 5 statuses stay truthful.** New cases are `Pending` until the exact command
   runs. Existing v1 `WFx` IDs and outcomes never change, and `WF1-005`–`WF1-010` are
   never reused.

---

## 11. Source references

- [Report 3 — Overall Description](../reports/report-3-software-requirement-specification/01-overall-description.md)
- [Report 3 — User Requirements](../reports/report-3-software-requirement-specification/02-user-requirements.md)
- [Report 3 — Functional Requirements](../reports/report-3-software-requirement-specification/03-functional-requirements.md)
- [Report 3 — Non-Functional Requirements](../reports/report-3-software-requirement-specification/04-non-functional-requirements.md)
- [Report 3 — Other Requirements](../reports/report-3-software-requirement-specification/05-requirement-appendix.md)
- [Business Flows — SF and MF1–MF5](business-flows.md)
- [Database Design](database-design.md)
- [Report 5 — Test Cases](../reports/report-5-test-report/01-test-cases/test-case-list.md)
- [Report 5 — Test Statistics](../reports/report-5-test-report/02-test-statistics/test-statistics.md)
- [Backend Architecture](../backend/architecture.md)
- [Authentication and Access Control](../backend/authentication-and-authorization.md)
- [AI Agent Rules](../development/ai-agent-rules.md)
- Implementation plan: `docs/superpowers/plans/2026-10-04-documents-led-mf1-mf5-refactor.md`
  (note the path-prefix defect recorded as `GAP-D-22`)
- Design spec: `docs/superpowers/specs/2026-10-04-documents-led-mf1-mf5-refactor-design.md`
