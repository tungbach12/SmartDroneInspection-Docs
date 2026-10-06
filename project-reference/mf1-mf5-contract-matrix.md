---
title: "MF1–MF5 Canonical Contract Matrix"
document_type: contract-matrix
purpose: "Single canonical role, actor-zone, flow, API, and data matrix. Records the documented target, the as-implemented current state, and every gap with the task number that owns closing it."
version: "1.0"
updated: 2026-10-06
---

# MF1–MF5 Canonical Contract Matrix (v1.0)

## 0. How to read this document

This matrix is the contract that Phase 1 through Phase 7 build against. It exists so
no later task has to rediscover a documented-vs-implemented difference.

**Authority order.** Where two sources disagree, this ranking applies:

1. The six canonical roles and the capability-vetting model below (settled decisions,
   recorded in §2). These are not re-litigated by any task.
2. Report 3 (`reports/report-3-software-requirement-specification/`) and
   `project-reference/business-flows.md` (v3.4 — flight phase = MF2 / processing phase = MF3; direct-transfer settlement, no platform
   custody of funds) define the **target**.
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
| `backend` (main) | `7b40ef46f7a32bcb8688443d9f0820f9bed14394` | The `main` baseline: post `d3a9f5d` (PR #51 — migrations `V12`–`V20`, canonical six roles, peer-review removal), `dc143ca` (PR #52 — comment-only `MF3-09`→`MF3-08` renames) and `7b40ef4` (PR #53 — `V21`, maintenance `DISPUTED` state). Superseded the `04a254f` reading this matrix originally shipped with; see §0.2 `C-7`. |
| `backend` (`refactor/wf1-contract`) | `1a5c88e955bb4fe3e82ad345e1516372edbd92cb` | **Not an ancestor of `main`** (`git merge-base --is-ancestor 1a5c88e origin/main` → false, re-verified 2026-10-06). Its `V12__wf1_contract_alignment.sql` does **not** exist on `main`, where `V12` is `V12__provider_organizations_and_capability_vetting.sql`. Historical reading only; no row below is sourced from it. |
| `frontend` (main) | `d717fb3` | Role union, portal policy, route guards. |
| `mobile` (main) | `aaa946b` | Consumed API paths. |
| `docs` (this worktree) | `585ca3c0763d7e1f8bf81a10883c02fcbfb58ebb` | The target documents. |
| `backend` (`refactor/mf1-mf5-backend`) | `451a2af` | Task 1.4 branch, **still unmerged**: not an ancestor of `main` (`git merge-base --is-ancestor 451a2af origin/main` → false, re-verified 2026-10-06). Post-fix-round-1 rows were originally read from this tree; every row citing "implemented at 451a2af" was re-read against `dc143ca` on 2026-10-06 and was **not** found on `main` (see §0.2 `C-7`, §3.1 SF-02/SF-03, §4.2, `GAP-A-01`). |

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

**The 2026-10-06 reconciliation (§0.2 `C-7`) also produced no test evidence.** It is a
source-reading pass over backend `main` @ `dc143ca` — `git`, `grep` and file reads only, no
build and no test run — and every status it changed carries a file:line, `V<nn>` or test-class
pointer inside the row it changed.

### 0.2 Documented-vs-implemented conflict resolutions

| # | Conflict | Resolution applied here |
| --- | --- | --- |
| C-1 | The task brief names the output path `docs/superpowers/plans/mf1-mf5-contract-matrix.md`. The `docs` repository content root has no nested `docs/` directory on `main`; content lives at `project-reference/`, `reports/`, `backend/`, etc. The plan file itself is only reachable at `docs/docs/superpowers/plans/…` from the `docs/provider-capability-vetting` branch. | Matrix written to `project-reference/mf1-mf5-contract-matrix.md`, matching the actual repository layout and the instruction that the matrix belongs under `docs/project-reference/`. Recorded as `GAP-D-22`. |
| C-2 | The plan and brief spell source paths as `docs/project-reference/…` and `docs/backend/…`. Those paths do not resolve on this branch. | All paths in this matrix are repository-relative and verified to exist. Recorded as `GAP-D-22`. |
| C-3 | Report 3 §2.1 defines `PLATFORM_ADMIN`; `database-design.md` §6.1 defines actor zones `PLATFORM_GOVERNANCE` / `CUSTOMER_ORGANIZATION` / `SERVICE_PROVIDER`; the implementation enum defines `PLATFORM` / `CUSTOMER_ORGANIZATION` / `SERVICE_WORKFORCE`. | The documented target zone names win. Two of three zone names change. `GAP-R-02`. |
| C-4 | Report 3 `business-flows.md` SF-03 grants a single organization-wide `VERIFIED` and blocks an unapproved Provider from "all quotation rights", which contradicts the capability-scoped BR-05 gate. | The capability-scoped gate wins. `business-flows.md` SF-03 must be rewritten in Task 7.1. `GAP-R-06`, `GAP-F-01`. |
| C-5 | `database-design.md` §12 asserts `V1`–`V11` implement "37 application tables", but the inventory closure requires counting `provider_organizations` as implemented and omitting `peer_reviews`, which has DDL. | Actual DDL was enumerated directly: 38 `CREATE TABLE` statements = 37 application tables + `event_publication`. The doc's *count* is right; its *inventory membership* is wrong. `GAP-D-01`, `GAP-D-18`. |
| C-6 | Report 3 uncommitted edits require four per-capability vetting outcomes but never name them as an enum. | The four-value vocabulary is fixed in §2.4 of this matrix, sourced from `business-flows.md` SF-03 and the design spec §2.3, and is now binding for all tasks. `GAP-R-06`. |
| C-8 | 2026-10-06 MF2/MF3 runtime follow-on. C-7 left the MF2 mission-planning rows (MF2-01…MF2-06, `GAP-F-08/-09/-10`, `GAP-A-03`) and `GAP-D-04` marked open because their runtime was absent on `main`. | Backend PR #54 (branch `feat/supporting-code-no-mainflows`, `364a23e` + `1de6a7a`) lands that runtime: `DroneMissionPlanController`/`DroneMissionPlanService`/`DroneMissionPlan`/`MissionShotItem`, `InspectionOrderStatus.READY_FOR_FLIGHT` transition in `approve` (`:212,:224`), and `V22`'s six author/completeness provenance columns on `report_versions`. **Closed:** `GAP-F-08`, `GAP-F-09`, `GAP-A-03`, `GAP-D-04`. **Updated in place:** MF2-01/-02/-03 → `implemented`; MF2-04/-05 stay `partial` (no authority lookup, no conflict-of-interest check); `GAP-F-10` (dossier fields now persisted; validation absent); `GAP-F-16` (review-clock stamping now written at release `:247-258`; deemed-acceptance sweep still absent); `GAP-D-02` note (`providerId` now exists on `User`/`UserAccess` additively); MF3-04/`GAP-F-12` (GSD storable/editable; mm derivation still absent); MF2-07/`GAP-F-11` unchanged (no `mission_plan_id` on inspections). Rows otherwise unchanged. |
| C-7 | 2026-10-06 reconciliation. This matrix's §0.1 baseline recorded backend `main` = `04a254f`, but `main` then merged PR #51 (squash `d3a9f5d` = `85e4f5b` + `a9ed17d`) and PR #52 (`dc143ca`). Rows in §3.1/§4.2/§5/§6 had also been read from `refactor/mf1-mf5-backend` @ `451a2af` and `refactor/wf1-contract` @ `1a5c88e`, neither of which is an ancestor of `main` (both `merge-base --is-ancestor` checks re-run on 2026-10-06 and false). | Baseline moved to `dc143ca`. Re-verified against `main`: `V12`–`V20` exist (`provider_organizations`, `provider_capabilities`, `provider_capability_evidence`, `provider_vetting_decisions`, `platform_configurations`, `drone_mission_plans`, `mission_shot_items`, `dispute_tickets`; `peer_reviews` dropped by `V19`; `locked_*` policy snapshots; direct-transfer status sets; warranty clock); the canonical six roles are live in `V13`, `Roles.java`, `UserRole.java` and every `@PreAuthorize` string; peer-review code is deleted; `POST …/submit-review` is the Inspector author-verify step and `POST …/release` is `PROVIDER_MANAGER` + completeness. **Closed:** `GAP-R-01`, `GAP-R-03`, `GAP-R-06`, `GAP-F-14`, `GAP-F-15`, `GAP-F-20`, `GAP-A-05`, `GAP-A-13`, `GAP-D-02`, `GAP-D-06`, `GAP-D-07`, `GAP-D-08`, `GAP-D-09`, `GAP-D-11`, `GAP-D-12`, `GAP-D-14`, `GAP-D-18`. **Re-opened:** `GAP-A-01` (the four provider-organization endpoints are not on `main` — `grep -rn provider-organizations src/` returns nothing) and the runtime half of `GAP-F-01` (SF-02/SF-03 have no Java on `main`; its text half is now closed — `business-flows.md:229`). **Stayed open with fresh evidence:** `GAP-R-04`, `GAP-R-05`, `GAP-R-07`, `GAP-R-08`, `GAP-R-15`, `GAP-D-01`, `GAP-D-04`, `GAP-D-05`, `GAP-D-13` (standing endpoint not on `main`), `GAP-D-17`, and the runtime/data halves of `GAP-F-02`, `GAP-F-06`, `GAP-F-08`, `GAP-F-09`, `GAP-F-10`, `GAP-F-12`, `GAP-F-16`, `GAP-F-17`, `GAP-F-18`, `GAP-F-21`, `GAP-F-23`. **Deliberately unchanged:** the frozen `V16` header keeps its stale `(MF3-09)` comment by design (PR #52 renumbered source comments only); frontend and mobile rows keep their own baselines; Report 5, `business-flows.md`, `database-design.md` and all `GAP-*` ids are untouched. **Observed, not edited:** `V20`'s header claims `DISPUTED` is admitted by `maintenance_orders.status`, but `V16:308-311` does not include it (backend was read-only for this task) — **resolved the same day** by backend PR #53 (merge `7b40ef4`): `V21` widens `ck_maintenance_orders_status` with `DISPUTED`, head assertions moved 20→21, suite 208/0/0; `database-design.md` §6.5/§6.6/§8/§12 updated in the accompanying docs pass. |

---

## 1. Canonical vocabulary

### 1.1 Six canonical roles and three actor zones

These six rows are the complete role set. There is **no** `MAINTENANCE_PROVIDER_MANAGER`
and no seventh role may be introduced by any task.

| # | Role | Actor zone | Canonical responsibility |
| --- | --- | --- | --- |
| 1 | `PLATFORM_ADMIN` | `PLATFORM_GOVERNANCE` | Technical configuration, security policy, checklist templates, technical audit. Cannot publish commercial policy or vet a Provider. |
| 2 | `PLATFORM_OPERATOR` | `PLATFORM_GOVERNANCE` | Provider vetting, commercial-policy publication, payment-status tracking, commission & commission-VAT invoicing, internal complaint handling. Not a legal arbitrator, not a deposit custodian. |
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

**Reconciliation note (2026-10-06, §0.2 `C-7`).** The observables this section describes
(`ProviderEligibilityFacade`, the standing endpoint, `organizationStatus` on the
capability-decision response) were read from `refactor/mf1-mf5-backend@451a2af`, which is
**not** on `main` (§0.1). On `dc143ca` only the schema half exists —
`provider_organizations.standing_decision_reason` (`V12:63`) guarded by
`ck_provider_org_standing_reason` (`V12:90`) — while no provider-organization controller,
service, entity or facade exists (`GAP-A-01` re-opened, `GAP-R-04`). The rule itself stays
settled.

Settled rule:

| Rule | Detail |
| --- | --- |
| Standing is decided only by its own action | `POST /api/v1/provider-organizations/{providerId}/standing/decisions`. No capability decision writes `provider_organizations.status`, in any direction. |
| Owner | `PLATFORM_OPERATOR`, per §1.1 "Provider vetting". No seventh role (§10 rule 4). |
| Independent of capabilities | Exercisable with no capability declared. Reads and writes no capability, evidence, or decision-history row. |
| Reason required | A legal-identity approval with no stated ground is refused. Persisted in `provider_organizations.standing_decision_reason` (`V12:63`, main numbering — the earlier `(V15)` citation came from the unmerged fix-round branch). |
| Own audit event | `PROVIDER_ORGANIZATION_LEGAL_IDENTITY_ACCEPTED`, distinct from `PROVIDER_CAPABILITY_VETTED`. |
| Observable | The capability-decision response carries `organizationStatus`, so a caller can see that the decision did not move standing rather than inferring it from an absent field. |

`PENDING` → `VERIFIED` only. `SUSPENDED` and `BANNED` remain unreachable from any
endpoint, which is a **known open item**, not a settled part of this rule: they need their
own operator action and their own lifecycle, and no task currently owns them. Recorded
here so a later task does not mistake the four-value vocabulary for a four-value API.

An approval without a recorded `standing_decision_reason` remains representable on purpose:
it is how a Provider accepted before `V12` exists looks. A fabricated reason would be worse
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
| `MF4` | `inspections` + `infrastructure` (settlement/invoice ports) + `notifications` |
| `MF5` | `maintenance` |

### 3.1 Supporting Flow (SF)

| Step | Target | Implemented state | Status | Gap |
| --- | --- | --- | --- | --- |
| SF-01 Client organization self-registration | `POST /api/v1/auth/register`, creates organization + first `CLIENT` in one transaction | Present. `BrowserAuthController:57`, `MobileAuthController:40`. Assigns only `CLIENT` in `CUSTOMER_ORGANIZATION`. | `implemented` | — |
| SF-02 Provider onboarding, capability declaration, evidence submission | `POST /api/v1/provider-organizations` | **No runtime on `main`.** The schema half landed in `V12`: `provider_organizations` (`V12:50`), `provider_capabilities` (`V12:105`), `provider_capability_evidence` (`V12:176`), `provider_vetting_decisions` (`V12:148`), `users.provider_id` (`V12:208`). `src/main/java` contains no provider-organization class at all (`find src/main/java -iname "*Provider*"` → empty) and `grep -rn provider-organizations src/` → empty, so `POST /api/v1/provider-organizations` has no controller. The onboarding code this row previously cited lives only on the unmerged branch `refactor/mf1-mf5-backend@451a2af` (§0.1). | `target-only` (runtime) | `GAP-R-04`, `GAP-A-01` |
| SF-03 Operator vetting, per capability | `GET /api/v1/provider-organizations/{providerId}/capabilities`, `POST /api/v1/provider-organizations/{providerId}/capabilities/{capability}/decisions`, `POST /api/v1/provider-organizations/{providerId}/standing/decisions` | **No runtime on `main`**: no `ProviderVettingController`, no `ProviderOrganizationController`, no capability-decision or standing endpoint (`grep -rn provider-organizations src/` → empty). The vocabulary half is in `V12`: four-outcome `ck_provider_capabilities_status` (`V12:126-127`), append-only decision history (`V12:148-161`), organization standing kept on its own axis (`provider_organizations.status` `V12:74-75`, `standing_decision_reason` `V12:63`, `ck_provider_org_standing_reason` `V12:90`). The endpoint code cited previously exists only on unmerged `451a2af` (§0.1); see §2.6. | `target-only` (runtime) | `GAP-R-04`, `GAP-R-05`, `GAP-A-01` |
| SF-04 Asset profile + airspace pre-check | Asset CRUD present; airspace pre-check warning | Asset CRUD implemented. Asset-level pre-check still absent: no `ALTER TABLE assets` in `V12`–`V20` and no airspace symbol in `src/main/java`, so no `AIRSPACE_CHECK_PENDING` / `RESTRICTED_AIRSPACE` state exists for an asset. **What changed:** mission-level airspace determination now exists (`V17:57`, `ck_drone_mission_plans_airspace` `V17:83-86` — `NOT_CHECKED`, `CLEARANCE_REQUIRED`, `MANUAL_REVIEW`, `CLEARED`, `BLOCKED`) — plan-scoped and a different vocabulary, so it does not satisfy this asset pre-check. | `partial` | `GAP-F-02`, `GAP-D-15` |
| SF-05 Due cycle → one MF1 request package | `assets` publishes `InspectionScheduleDue`; `inspectionrequests` consumes and creates the request | Publisher exists (`InspectionScheduleDuePublisher`, `assets/events/InspectionScheduleDue`). **No listener exists; `inspectionrequests` has zero services.** | `partial` | `GAP-F-03` |
| SF-05 schedule proposal review by business reviewer | Target reviewer is `PLATFORM_OPERATOR` | Role strings were renamed in `d3a9f5d` but the reviewer is still not the target: `ScheduleProposalController:47` hardcodes `PROVIDER_MANAGER` or `PLATFORM_ADMIN` in-method and `:54` is `hasRole('PROVIDER_MANAGER')` (list at `:37` = `hasAnyRole('CLIENT','PROVIDER_MANAGER','PLATFORM_ADMIN')`). `PLATFORM_OPERATOR` is granted by no endpoint in `src/main/java`. | `partial` | `GAP-R-08` |

### 3.2 MF1 — Survey request, quotation sourcing, electronic contract

| Step | Target | Implemented state | Status | Gap |
| --- | --- | --- | --- | --- |
| MF1-01 Create request, direct selection or open RFQ | `inspectionrequests` service + API | Entities and repositories exist. **Zero services, zero controllers.** No HTTP path can create a request. | `target-only` (runtime) | `GAP-F-04`, `GAP-A-02` |
| MF1-02 Optional Operator RFQ broadcast | Notification + provider matching | Not present. | `target-only` | `GAP-F-26` (orphan) |
| MF1-03 Versioned Provider quotation | Capability-gated, excludes Platform AI/data/storage charges | Entity + immutability constraints exist. No service, no API, no capability gate, no charge-exclusion rule. | `partial` | `GAP-F-05` |
| MF1-04 Client revision/accept | Versioned revisions | Version columns exist; no service. | `partial` | `GAP-A-02` |
| MF1-05 Order policy snapshot | `locked_commission_rate`, `locked_review_period_days`, `locked_cancellation_policy`, `locked_terms_snapshot` | **Schema exists, writer does not.** `V15:88-95` adds all four `locked_*` columns to `inspection_service_orders` (rate/date pre-checks `V15:116-179`), fed by `platform_configurations` (`V15:40`, policy-key allow-list `V15:60-61`, one published version per key `V15:81-82`). Nothing snapshots anything: `inspectionrequests` still has zero services and zero controllers. | `partial` | `GAP-F-06`; `GAP-D-06` (CLOSED by `V15`) |
| MF1-06 Signature, contract effectiveness | Both parties sign electronically; the contract takes effect immediately and payment happens later by direct bank transfer — no funding step, no Platform custody | No contract-signature flow exists in `src/main/java`; no funding or escrow code exists because the target no longer contains either. | `target-only` | `GAP-F-07`, `GAP-D-10` (both obsolete) |
| MF1 cancellation / weather force majeure (MF1 §2) | Order-snapshotted cancellation terms; BR-13, BR-14 | **Policy source exists, snapshot writer does not.** `platform_configurations` accepts the `CANCELLATION` key (`V15:60-61`) and `inspection_service_orders.locked_cancellation_policy` exists (`V15:90`); no runtime writes a cancellation term because MF1 has no services. | `partial` | `GAP-F-06`; `GAP-D-08` (CLOSED by `V15`) |

### 3.3 MF2 — Drone mission planning, airspace clearance and field execution

| Step | Target | Implemented state | Status | Gap |
| --- | --- | --- | --- | --- |
| MF2-01 GSD → AGL and capture distance | Mission-specific, equipment-derived | **Runtime delivered by PR #54 (`364a23e`).** `DroneMissionPlanService.updateEquipmentAndSow` (`:125`) persists camera model, drone registration, pilot, `targetGsdMmPerPixel`, `plannedAglM`, overlaps, sensor/focal inputs (`UpdateMissionPlanRequest`); entity `DroneMissionPlan` and DTOs carry GSD/AGL. No derived capture-distance computation in code. | `implemented` | `GAP-D-09` (CLOSED by `V17`) |
| MF2-02 Forward/side overlap | SOW-specific | **Stored at runtime by PR #54 (`364a23e`).** `UpdateMissionPlanRequest` carries `forwardOverlapPercent`/`sideOverlapPercent`, persisted via `DroneMissionPlanService.updateEquipmentAndSow` (`:125`) on `drone_mission_plans`. No derivation or enforcement logic beyond persistence. | `implemented` | — |
| MF2-03 Structural shot list + gimbal pitch; waypoints optional | Shot items required; waypoints optional | **Shot items are runtime-managed by PR #54 (`364a23e`).** `DroneMissionPlanService.addShotItem` (`:149`) persists ordered shot items with `gimbalPitchDegrees` and optional waypoints via `MissionShotItem` entity + `MissionShotItemCoordinateConstraintTest`; approval gate still refuses incomplete plans. Remains `implemented`; the coordinate/gimbal CHECK-backed constraint is exercised by `MissionShotItemCoordinateConstraintTest`. | `implemented` | — |
| MF2-04 Airspace digital clearance | Lookup ≠ clearance; `AIRSPACE_MANUAL_VERIFY_REQUIRED` on outage | **Runtime airspace pre-check delivered by PR #54 (`364a23e`).** `DroneMissionPlanService.recordAirspacePreCheck` (`:174`) persists a plan-level `AirspaceCheckStatus` (five values: `NOT_CHECKED, CLEARANCE_REQUIRED, MANUAL_REVIEW, CLEARED, BLOCKED` — `AirspaceCheckStatus.java`), and `DroneMissionPlan.recordAirspacePreCheck` drives the V17 clearance gate. Still absent: asset-level pre-check (SF-04), outage/`AIRSPACE_MANUAL_VERIFY_REQUIRED` path (the enum carries `MANUAL_REVIEW` instead), and real lookup runtime. | `partial` | `GAP-F-02` |
| MF2-05 Legal flight clearance, certified pilot, drone registration, conflict-of-interest | Recorded before approval | **Dossier fields recorded at runtime by PR #54 (`364a23e`).** `DroneMissionPlanService.verifyFlightPermit` (`:187`) stamps the flight-permit reference; `updateEquipmentAndSow` persists `droneRegistrationId` and `pilotUserId`; approval is gated by the clearance check. Still absent: licence/credential *validation against an authority registry*, any conflict-of-interest field or check, and provider scoping on `inspection_assignments`. | `partial` | `GAP-F-10`; `GAP-D-02` (CLOSED by `V12`/`V14`/`V17`/`V20`) |
| MF2-06 Provider Manager approves plan, issues mission package, `READY_FOR_FLIGHT` | Order transitions to `READY_FOR_FLIGHT` | **Runtime delivered by PR #54 (`364a23e`).** `DroneMissionPlanService.approve` (`:212`) runs `plan.approve(callerUserId)` and moves the parent order via `order.markReadyForFlight()` (`:224`) in the same transaction; `InspectionOrderStatus` now includes `READY_FOR_FLIGHT` (`InspectionOrderStatus.java`). Approval is gated on a completed non-blocked airspace determination plus permit reference (`V17:95-100`). | `implemented` | — |
| MF2-07 Field execution of the approved shot list; session logged (moved from old MF3-01 in `business-flows.md` v3.4) | Assigned Inspector only, mission-linked; weather abort returns to MF2-05 for a new-date clearance | `InspectionController` is class-level `hasRole('INSPECTOR')` (`:49`) with assignment scoping in service. **`inspections` has no `mission_plan_id` in `V1`–`V20`** — the only `mission_plan_id` is the FK on `mission_shot_items` (`V17:146`) — so execution is still not mission-linked. | `partial` | `GAP-F-11` |

### 3.4 MF3 — Evidence ingestion, quality gate, AI verification, QA report

| Step | Target | Implemented state | Status | Gap |
| --- | --- | --- | --- | --- |
| MF3-01 Chunked upload to MinIO | Server-computed SHA-256, retry-safe | Implemented. `EvidenceService:74` computes checksum; `uq_evidence_inspection_checksum` and `uq_evidence_work_log_checksum` reject duplicates; object key is `inspections/{inspectionId}/{objectId}`. | `implemented` | — |
| MF3-02 Spatial telemetry: 3D GPS, AGL, gimbal angle, timestamp | Per-file spatial metadata | `evidence` stores `latitude`, `longitude`, `capture_time`. **No altitude/AGL, no gimbal angle, no 3D coordinate.** | `partial` | `GAP-F-13`, `GAP-D-15` |
| MF3-03 Evidence quality & coverage gate (blur, exposure, GPS validity, shot-list coverage) | Automatic gate with same-day re-flight alert (re-entry MF2-07) | **No blur, sharpness, exposure, or coverage assessment exists anywhere** in the implementation (v1 or `main`); only checksum integrity and duplicate rejection exist (row MF3-01). | `target-only` | `GAP-F-28` |
| MF3-04 YOLO candidates + GSD-derived physical defect size in mm | Multiply pixel size by mission GSD | `AiInferencePort` exists; candidates persist. GSD is now stored and editable via the mission plan (`DroneMissionPlanService.updateEquipmentAndSow`:125), but `grep -rni gsd src/main/java` now matches only plan/DTO/entity fields — still no physical-size derivation multiplying pixel size by GSD, and `AiInferencePort` carries no GSD input. | `partial` | `GAP-F-12` |
| MF3-05 Inspector confirm/modify/reject, manual finding, checklist | Non-official until verified | Implemented. `AiFindingCandidateStatus`, `VerifiedFindingSource`, `VerifiedFindingStatus`, manual finding endpoint. | `implemented` | — |
| MF3-06 Platform LLM narrative draft | Labelled draft, not released directly | `ReportDraftPort` + `ai-draft` endpoint exist. | `implemented` | — |
| MF3-07 **Author verification and edit by the authoring Inspector** | Required before submit; BR-23 | **Author verification is implemented.** `POST /reports/{r}/versions/{v}/submit-review` is `hasRole('INSPECTOR')` (`InspectionReportController:98-103`) and `InspectionReportService.submitForReview` (`:214-230`) refuses a non-author (`:218`), refuses anything but `DRAFT` (`:221`), runs the completeness check `ensureComplete` (`:224`) and sets `TECHNICALLY_APPROVED` (`:226`; `ReportVersion.verify()` `:147-152` stamps `submitted_at` and `technically_approved_at`). The peer-review workflow this row used to describe is **gone**: `PeerReview`, `PeerReviewDecision`, `PeerReviewRepository` and both peer-review endpoints were deleted in `d3a9f5d`, and `V19:66` drops `peer_reviews`. As of PR #54 (`1de6a7a`), the runtime now stamps `author_verified_by_user_id` / `author_verified_at` / `author_verification_snapshot` via `ReportVersion.verify(actorId, contentSnapshot)`, backed by the `V22` columns (`V22__report_author_verification_and_completeness.sql`, `GAP-D-04` closed). The target status vocabulary (`AUTHOR_VERIFIED` / `COMPLETENESS_RETURNED`) remains `GAP-D-05`. | `implemented` | `GAP-D-04` (CLOSED by `V22`), `GAP-D-05` (`GAP-F-14` CLOSED by `d3a9f5d`) |
| MF3-08 Provider Manager completeness check with reasons, then signed release; review clock starts from snapshot | BR-24: release requires author verification **and** Manager completeness | **Release gate implemented.** `POST .../release` is `hasRole('PROVIDER_MANAGER')` (`InspectionReportController:105-109`); `InspectionReportService.release` (`:233-246`) refuses anything but `TECHNICALLY_APPROVED` (`:237`) — a state only the author step can produce — and re-runs `ensureComplete` (`:240`, definition `:565-572`: non-empty evidence plus every required checklist item answered, reported as one conflict message rather than itemized reasons). The review clock is now stamped at release: `InspectionReportService.release` (PR #54 `1de6a7a`) records `completeness_checked_by_user_id` / `completeness_checked_at` via `version.markCompletenessChecked(actorId)` and sets `client_review_ends_at` from the order's `locked_review_period_days` (`:247-258`). The old peer-review `PUT .../reviewer` and `POST .../review` endpoints no longer exist (`d3a9f5d`). Deemed-acceptance sweep runtime still absent. | `partial` | `GAP-F-16` (deemed-acceptance runtime; review-clock stamping delivered by `1de6a7a`); `GAP-F-14`, `GAP-F-15`, `GAP-A-05` CLOSED by `d3a9f5d` |
| BR-25 Client visibility | Unverified candidates and unreleased drafts hidden | Service-scoped reads exist. | `implemented` | — |

### 3.5 MF4 — Report acceptance, settlement, internal complaints

| Step | Target | Implemented state | Status | Gap |
| --- | --- | --- | --- | --- |
| MF4-01 Client reviews released report | Own-organization scope | `GET /reports`, `GET /reports/{id}`, evidence content endpoint. | `implemented` | — |
| MF4-02a Client accepts | Immutable accepted version | `POST /reports/{id}/versions/{v}/client-decision` (`hasRole('CLIENT')`); `V10` added `client_decision_by_user_id`/`client_decision_reason` with a `REVISION_REQUESTED` reason CHECK. | `implemented` | — |
| MF4-02b Deemed acceptance on snapshotted `T_rev` | Only when terms expressly provide it | **Snapshot exists, timer does not.** `locked_review_period_days` (`V15:89`) and `client_review_ends_at` with the `AWAITING_ACCEPTANCE` milestone rules (`V16:50`, `V16:151-191`) exist; no runtime starts, stores or sweeps the window. | `partial` | `GAP-F-16`; `GAP-D-06` (CLOSED by `V15`) |
| MF4-03 Settlement `C = r × B`, single commission | Direct transfer CLIENT → PROVIDER bank account; the Platform issues its commission invoice separately and is never a custodian | **Representable in SQL, absent in Java.** `invoices.invoice_type` (`MAINTENANCE_SERVICE` / `INSPECTION_SERVICE` / `COMMISSION`) with its order and provider references (`V16:448-450`), the per-type binding CHECK `ck_invoices_type_and_order` (`V16:573-589`), and one live commission invoice per order (`uq_invoices_commission_inspection` `V16:653`, `uq_invoices_commission_maintenance` `V16:659`); the rate is snapshotted by `locked_commission_rate` (`V15:88`, `V15:187`). `grep -rni commission src/main/java` → empty: no calculation, no issuance path. | `partial` | `GAP-F-18`; `GAP-D-14` (CLOSED by `V16`) |
| MF4-04 Clarification request → corrected report | Distinct clarification state | Only `REVISION_REQUESTED` exists; there is no clarification state distinct from revision. | `partial` | `GAP-A-08` |
| MF4-05 Complaint filing, order-scoped | Client or Provider | **Table exists, runtime does not.** `V20:39` creates `dispute_tickets`: unique dispute number, polymorphic `order_id` + `order_type` with **no FK by design** (`V20:16-28`), parties, category/status/decision CHECKs, `provider_organization_id` (`V20:47`). Complaint attachments live in `dispute_tickets.evidence` JSONB (`V20:58`, array CHECK `V20:100-101`); **there is no `dispute_evidence` table and none is planned** — folded by the minimal-schema decision (`V20:9-11`). No entity, repository, service or controller exists (`grep -rni dispute src/main/java` → empty). | `partial` | `GAP-F-17`; `GAP-D-11` (CLOSED by `V20`) |
| MF4-06 Complaint state `DISPUTED` (workflow only) | A complaint pauses acceptance and payment as a workflow state; no funds are ever held by the Platform | **Both order tables admit `DISPUTED`.** `ck_inspection_service_orders_status` (`V16:120`) and — since `V21` (PR #53, merged `7b40ef4`) — `ck_maintenance_orders_status`. `InspectionOrderStatus.READY_FOR_FLIGHT` was added by PR #54 (`364a23e`); `InspectionOrderStatus`/`MaintenanceOrderStatus` still do not carry `DISPUTED`, and no code performs the transition; freeze is documented as workflow-level only with no money hold (`V20:16-24`). | `partial` | `GAP-F-18` |
| MF4-07/08 Operator internal outcome under Platform Terms | Not a legal arbitration | The duty now has a role: `PLATFORM_OPERATOR` exists in `V13`, `Roles.java` and `UserRole.java`. But no `@PreAuthorize` in `src/main/java` grants it (grep → enum/constant definitions only) and no complaint runtime exists to hold the outcome. | `target-only` | `GAP-F-17`, `GAP-R-07` |

### 3.6 MF5 — Maintenance, before/after evidence, warranty

| Step | Target | Implemented state | Status | Gap |
| --- | --- | --- | --- | --- |
| MF5 module runtime | Services and API | **The `maintenance` module has 9 entities and 9 repositories and zero services and zero controllers** — 9 of the 10 files under `maintenance/domain` carry `@Entity` (`MaintenanceTicketFindingId` is the embeddable key class); the previously recorded "10 entities and 10 repositories" was a miscount and is corrected here. Nothing is reachable over HTTP. | `target-only` | `GAP-F-19`, `GAP-A-04` |
| MF5-01 Ticket from verified finding in an accepted report | BR-31 | `maintenance_tickets.accepted_report_version_id` NOT NULL FK + `maintenance_ticket_findings` junction exist. **No service enforces "at least one finding", and no CHECK requires a finding row.** | `partial` | `GAP-F-22` |
| MF5-02 Maintenance capability gate before quotation | BR-05 capability gate | **Data model exists, gate does not run:** `provider_capabilities` with the four-outcome CHECK and `(provider_id, capability_type)` unique key (`V12:105-142`), but no eligibility facade, service or controller consults it (`grep -rln ProviderCapability src/main/java` → empty). | `partial` | `GAP-F-21`, `GAP-R-05` |
| MF5-03 Maintenance order policy snapshot | Commission and warranty snapshots | **All snapshot columns exist:** `locked_commission_rate` and `locked_terms_snapshot` (`V15:187-189`), `locked_warranty_days` and `warranty_end_date` (`V18:50-51`, consistency CHECK `ck_maintenance_orders_warranty` `V18:103-114`). Nothing writes them — no maintenance runtime. | `partial` | `GAP-F-23`; `GAP-D-07` (CLOSED by `V15`/`V18`) |
| MF5-04 Assigned Engineer executes; **mandatory paired before/after evidence** | BR-35: completion strictly requires a verified pair | **The pair is now constraint-enforced:** `maintenance_work_logs.before_evidence_id` / `after_evidence_id` (`V18:238-239`) are two distinct FKs to `evidence` (`V18:290`, `V18:293`) and `ck_work_logs_evidence_pair` (`V18:341-345`) requires both present and different; `ck_evidence_maintenance_pair` (`V18:226-229`) keeps `BEFORE_MAINTENANCE` / `AFTER_MAINTENANCE` rows attached to a work log. Still absent: any upload path (`maintenance` has no controller). | `partial` | `GAP-D-17` (`GAP-F-20` CLOSED by `V18`) |
| MF5-05 Change order pauses extra work | Single `PENDING_APPROVAL` change at a time | Tables exist; no service, no single-pending constraint. | `target-only` | `GAP-F-25` |
| MF5-06 Client accepts / rework / re-inspection | Three distinct decisions | `resolution_decision` CHECK allows `ACCEPT_RESOLUTION, REQUEST_REWORK, REQUEST_REINSPECTION`; no service. | `partial` | `GAP-A-04` |
| MF5-07 Settlement by direct transfer, single commission, warranty start | SYSTEM issues the Payment Invoice; CLIENT transfers 100% to PROVIDER; Platform invoices its commission separately | **Columns and vocabulary exist, flow does not.** `maintenance_orders` gains `payment_invoice_issued_at`, `paid_at`, `provider_bank_account_number`, `provider_bank_name` (`V16:261-265`) with `ck_maintenance_orders_settlement` (`V16:355-367`) and the bank-pair CHECK (`V16:410-423`); its status set gains `AWAITING_PAYMENT` / `PAID` (`V16:308-311`); `invoices.invoice_type` covers `MAINTENANCE_SERVICE` / `COMMISSION` (`V16:448-458`); warranty starts via `V18` clock columns. No runtime issues an invoice or records a transfer. | `partial` | `GAP-F-18`, `GAP-F-23` |
| MF5-08 Warranty countdown, free-rework claim, auto-close ticket | Warranty duration is snapshotted at signing; no amount is retained by anyone | **Warranty DDL exists, sweep does not run.** Order snapshot `locked_warranty_days` / `warranty_end_date` (`V18:50-51`), ticket clock `accepted_at` / `warranty_started_at` / `warranty_ends_at` (`V18:118-121`, CHECK `V18:171-180`), auto-close sweep index `ix_maintenance_tickets_warranty_close` (`V18:184-185`), `WARRANTY_DURATION` is a legal policy key (`V15:61`). No countdown job, no free-rework claim flow, no maintenance service. | `partial` | `GAP-F-23` |
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
| `POST /api/v1/provider-organizations` | `PROVIDER_MANAGER` declares capabilities | **absent on `main`** — no such controller (`grep -rn provider-organizations src/` → empty); the endpoint exists only on unmerged `451a2af` (§0.1). Schema prerequisite is on `main` (`V12`). | `target-only` | `GAP-A-01` |
| `GET /api/v1/provider-organizations/{providerId}/capabilities` | `PROVIDER_MANAGER` own org, `PLATFORM_OPERATOR` any | **absent on `main`** (same evidence as the row above; the `V12` table and its indexes exist, no endpoint reads them) | `target-only` | `GAP-A-01` |
| `POST /api/v1/provider-organizations/{providerId}/capabilities/{capability}/decisions` | `PLATFORM_OPERATOR` only | **absent on `main`** — and no `@PreAuthorize` anywhere in `src/main/java` grants `PLATFORM_OPERATOR` (grep of all `@PreAuthorize`). Decision vocabulary is enforced in `V12:126-134`. | `target-only` | `GAP-A-01`, `GAP-R-07` |
| `POST /api/v1/provider-organizations/{providerId}/standing/decisions` | `PLATFORM_OPERATOR` accepts the legal identity (§2.6) | **absent on `main`** (same grep); the standing axis exists only as schema — `V12:63` `standing_decision_reason` + `ck_provider_org_standing_reason` `V12:90` (§2.6 note). | `target-only` | `GAP-A-01`, `GAP-R-07` |
| Mission plan CRUD + approve | `PROVIDER_MANAGER` manage, `INSPECTOR` manage assigned, `CLIENT` view agreed | **Runtime delivered by PR #54 (`364a23e`)**: `DroneMissionPlanController` (116 lines) exposes create/get/list/update/addShotItem/airspace-pre-check/verifyPermit/submit/approve; `DroneMissionPlanService` implements them with provider scoping and `PROVIDER_MANAGER` approval (`:287`). | `implemented` | — (closed; was `GAP-A-03`) |
| Inspection request create / RFQ | `CLIENT` own org | **absent** — `inspectionrequests` has no controller | `target-only` | `GAP-A-02` |
| Quotation create / revise / decide | `PROVIDER_MANAGER` own org, `CLIENT` decide | **absent** | `target-only` | `GAP-A-02` |
| Service order confirm | `CLIENT` decide | **absent** | `target-only` | `GAP-A-02` |
| Maintenance ticket / assessment / order / work log / evidence | `CLIENT`, `MAINTENANCE_ENGINEER` assigned, `PROVIDER_MANAGER` own org | **absent** — `maintenance` has no controller | `target-only` | `GAP-A-04` |
| `GET /api/v1/asset-categories` | all authenticated | `isAuthenticated()` | `implemented` | — |
| `POST/PUT/DELETE /api/v1/asset-categories/**` | `PLATFORM_ADMIN` | `hasRole('PLATFORM_ADMIN')` (`AssetCatalogController:42,49,63,71`) | `implemented` | — |
| `GET/POST /api/v1/assets` | `CLIENT` own org manage; `PLATFORM_OPERATOR`/`PLATFORM_ADMIN` view | `hasRole('CLIENT')` / `hasAnyRole('CLIENT','PLATFORM_ADMIN')` (`AssetController:41,49,68`) — no provider-scoped grant on the asset profile itself | `partial` | `GAP-A-07` |
| `GET /api/v1/assets/pending-review`, `POST /{assetId}/review` | `PLATFORM_OPERATOR` | `hasRole('PROVIDER_MANAGER')` (`AssetController:59,84`) — role renamed in `d3a9f5d`, still not the target `PLATFORM_OPERATOR` | `partial` | `GAP-R-08` |
| `GET /api/v1/inspection-schedules`, `/{id}/pause`, `/{id}/activate` | `CLIENT` | `hasAnyRole('CLIENT','PLATFORM_ADMIN')` / `hasRole('CLIENT')` (`InspectionScheduleController:29,36,43`) | `implemented` | — |
| `GET /api/v1/schedule-proposals` | `CLIENT`, reviewer, `PLATFORM_ADMIN` | `hasAnyRole('CLIENT','PROVIDER_MANAGER','PLATFORM_ADMIN')` (`ScheduleProposalController:37`) | `partial` | `GAP-R-08` |
| `POST /schedule-proposals/{id}/review` | `PLATFORM_OPERATOR` | `hasRole('PROVIDER_MANAGER')` (`ScheduleProposalController:54`) | `partial` | `GAP-R-08` |
| `POST /schedule-proposals/{id}/select` | `CLIENT` | `hasRole('CLIENT')` (`ScheduleProposalController:64`) | `implemented` | — |
| `POST /api/v1/assets/{assetId}/documents` | `CLIENT` own org | `hasAnyRole('CLIENT','PLATFORM_ADMIN')` (`AssetDocumentController:37`) | `implemented` | — |
| `GET /assets/{assetId}/documents`, `/{documentId}/content` | `CLIENT` own org, `PROVIDER_MANAGER` view own provider scope, `PLATFORM_ADMIN` audit | `hasAnyRole('CLIENT','PLATFORM_ADMIN','PROVIDER_MANAGER')` (`AssetDocumentController:51,58`) — the provider grant exists at method level, but no `assets` service scopes it to the caller's provider (`grep PROVIDER src/main/java/.../assets/service/` → empty), so own-provider isolation is unenforced | `partial` | `GAP-A-07` |
| `GET /api/v1/inspections/**` (assignments, start, checklist, evidence, findings) | `INSPECTOR` assigned only | class-level `hasRole('INSPECTOR')`, assignment scope in service | `implemented` | — |
| `GET /api/v1/reports`, `/{reportId}` | `CLIENT` released, `PROVIDER_MANAGER` own provider, `INSPECTOR` authored | `hasAnyRole('INSPECTOR','PROVIDER_MANAGER','CLIENT')` (`InspectionReportController:41,47`) — three roles at method level; isolation rests entirely on service scoping | `partial` | `GAP-A-06` |
| `POST /inspections/{id}/report`, `PUT .../narrative`, `POST .../versions`, `POST .../submit-review` | `INSPECTOR` (author) | `hasRole('INSPECTOR')` (`InspectionReportController:54-103`); `submit-review` additionally enforces author-only and `DRAFT`-only in the service (`InspectionReportService:218-221`) | `implemented` | — |
| `PUT /reports/{r}/versions/{v}/reviewer` | Reviewer assignment — a peer-review step removed from the target with peer review (Report 3 record-of-changes, 04 Oct 2026) | **Endpoint removed**: no `PUT .../reviewer` mapping exists in `InspectionReportController`; `AssignPeerReviewerRequest` and the `PeerReview*` classes were deleted in `d3a9f5d`, and `V19:66` drops `peer_reviews` | `target-only` (step removed from target and implementation) | `GAP-A-05` (CLOSED) |
| `POST /reports/{r}/versions/{v}/review` | Target: Manager completeness check (MF3-08) | **Endpoint removed with peer review** (`d3a9f5d`); the completeness duty it contradicted now runs inside `POST .../release` (`InspectionReportService:240` → `ensureComplete` `:565-572`) | `target-only` (no standalone endpoint; duty enforced in `release`) | `GAP-A-05` (CLOSED) |
| `POST /reports/{r}/versions/{v}/release` | `PROVIDER_MANAGER` **after** author verification + completeness | `hasRole('PROVIDER_MANAGER')` (`InspectionReportController:105-109`) with the full precondition chain: `TECHNICALLY_APPROVED` only (`InspectionReportService:237`, reachable only via the author step `:218-226`) plus `ensureComplete` (`:240`) | `implemented` | — (`GAP-F-15` CLOSED by `d3a9f5d`) |
| `POST /reports/{r}/versions/{v}/client-decision` | `CLIENT` accept or request revision | `hasRole('CLIENT')` | `partial` | `GAP-A-08` |
| `GET /reports/{r}/versions/{v}/evidence/{e}/content` | `CLIENT` own org | `hasRole('CLIENT')` | `implemented` | — |
| `/api/v1/auth/**` (csrf, register, login, password/setup, refresh, logout, logout-all, me, password/change) | all roles | authenticated | `implemented` | — |
| `/api/v1/mobile/auth/**` | mobile profile | authenticated | `implemented` | — |
| `/api/v1/platform/users/**` (create, reset-password, roles, status) | `PLATFORM_ADMIN`; roles/status may not mint `PLATFORM_OPERATOR` business powers without duty separation | class-level `hasRole('PLATFORM_ADMIN')` (`PlatformUserController:32`) | `partial` | `GAP-R-07` |

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
| `GAP-R-01` | Role code set | 6 canonical codes | **CLOSED on the backend by `V13` + `d3a9f5d`**: `user_roles.role` is redeclared over the canonical six (`V13:203-212`), `Roles.java` and `UserRole.java` hold exactly `PLATFORM_ADMIN`, `PLATFORM_OPERATOR`, `CLIENT`, `PROVIDER_MANAGER`, `INSPECTOR`, `MAINTENANCE_ENGINEER`, and every `@PreAuthorize`/`hasRole` string in `src/main/java` is canonical (grep of all `@PreAuthorize` returns no `ADMIN` and no `SERVICE_MANAGER`). Client and mobile unions still model the legacy set and stay open under `GAP-R-09` / `GAP-R-11`. | — (closed) |
| `GAP-R-02` | Actor-zone vocabulary | `PLATFORM_GOVERNANCE`, `CUSTOMER_ORGANIZATION`, `SERVICE_PROVIDER` | `PLATFORM`, `CUSTOMER_ORGANIZATION`, `SERVICE_WORKFORCE` (enum + `V3` CHECK) | **1.2** |
| `GAP-R-03` | Provider linkage column | `users.provider_id` FK | **CLOSED by `V12`**: `ALTER TABLE users ADD COLUMN provider_id UUID` (`V12:208`), FK `fk_users_provider` (`V12:259-260`) plus the provider indexes (`V12:210`, partial active index `V12:214-216`) and zone exclusivity `ck_users_organization_provider_exclusive` (`V12:298-300`) — `grep provider_id src/main/resources/db/migration` now matches `V12`, `V14`, `V17`, `V20`. | — (closed) |
| `GAP-R-04` | Provider Organization aggregate | Table + JPA entity | **Table exists, code does not**: `CREATE TABLE provider_organizations` (`V12:50`) with `provider_capabilities` (`V12:105`), `provider_vetting_decisions` (`V12:148`) and `provider_capability_evidence` (`V12:176`); but `find src/main/java -iname "*Provider*"` → empty, so no JPA entity, repository, service or controller exists on `main`. The aggregate was built only on unmerged `451a2af` (§0.1). | **1.3** |
| `GAP-R-05` | Capability aggregate and eligibility gate | `ProviderCapabilityType`, `ProviderCapabilityStatus`, evidence, decision history | **Data half exists** — `V12:105-142` (`uq_provider_capabilities_capability` `V12:123`, four-outcome CHECK `V12:126-127`, decision-pairing CHECK `V12:131-134`), evidence with the `DRONE_REGISTRATION`/`PILOT_LICENSE` kinds (`V12:176-194`) and append-only decisions (`V12:148-161`). **Gate still absent**: no `ProviderCapabilityType`/`ProviderCapabilityStatus` enum, no eligibility facade, and no `providerId` field anywhere in `src/main/java`, so no quotation, order or assignment path is capability-gated. | **1.3** |
| `GAP-R-06` | Vetting status vocabulary conflict | Report 3 edits require four outcomes but name none; `business-flows.md` SF-03 uses four; `database-design.md` `provider_organizations.status` uses `PENDING/VERIFIED/SUSPENDED/BANNED` | **CLOSED**: the two axes now exist with their own vocabularies — organization standing `PENDING/VERIFIED/SUSPENDED/BANNED` (`V12:74-75`) and per-capability `PENDING/ADDITIONAL_INFO_REQUIRED/VERIFIED/REJECTED` (`V12:126-127`) plus append-only decisions (`V12:148-161`); `business-flows.md:229` now states the four outcomes and independence; §2.4 binds them. Residual noted, not a gap: Report 3 still never enumerates the four outcomes (`grep -rl ADDITIONAL_INFO_REQUIRED reports/report-3-…/` → none), so §2.4 remains their binding source. | — (closed) |
| `GAP-R-07` | Separation of duties | `PLATFORM_ADMIN` technical vs `PLATFORM_OPERATOR` business; Provider may not self-approve | **Half closed**: the six roles exist (`V13`, `Roles.java`, `UserRole.java`) and `PlatformUserController` is now `hasRole('PLATFORM_ADMIN')` (`:32`). **Still open**: no `@PreAuthorize` in `src/main/java` grants `PLATFORM_OPERATOR` (grep of all `@PreAuthorize`), `RolePolicy.validate` still has no `PLATFORM_OPERATOR` branch (the `PLATFORM` case admits only `PLATFORM_ADMIN`), and with no provider-organization endpoint there is no path on which Provider self-approval could even be refused. | **1.2** (add roles), **1.4** (scoping) |
| `GAP-R-08` | Schedule-proposal reviewer | `PLATFORM_OPERATOR` | Still not `PLATFORM_OPERATOR`: `ScheduleProposalController:47` hardcodes `PROVIDER_MANAGER`/`PLATFORM_ADMIN` in-method and `:54` is `hasRole('PROVIDER_MANAGER')` (list `:37`); the asset review queue follows the same non-target role (`AssetController:59,84` `hasRole('PROVIDER_MANAGER')`). The `SERVICE_MANAGER`→`PROVIDER_MANAGER` rename happened in `d3a9f5d`; `PLATFORM_OPERATOR` is granted by no endpoint. | **1.2** |
| `GAP-R-09` | Frontend role union and portal model | 6 roles, 3 zones | 5 roles, 3 portals that collapse the target zones | **6.1** |
| `GAP-R-10` | Frontend session typing | Typed zone + `providerId` | `actorZone: string`; no `providerId` field | **6.1** |
| `GAP-R-11` | Mobile role/zone awareness | Assigned-work scoping | No role or zone concept in `mobile/lib` | **6.4** |
| `GAP-R-12` | Frontend business-review visibility | `PLATFORM_OPERATOR` | `asset-review: ['SERVICE_MANAGER']` | **6.1** |
| `GAP-R-13` | Frontend capability gating | Maintenance UI gated on `MAINTENANCE = VERIFIED` | No capability input to the UI at all | **6.3** |
| `GAP-R-14` | Role policy API | `allowedZone(role)`, `canPerform(role, action)` | `RolePolicy` exposes only `validate(zone, orgId, roles)`; neither method exists | **1.1**, **1.2** |
| `GAP-R-15` | Provider-scope grant path on SF/WF1 endpoints | `PROVIDER_MANAGER` may view own-provider asset and document scope | **Half closed**: provider roles now exist (`UserRole.serviceRole()` = `PROVIDER_MANAGER`/`INSPECTOR`/`MAINTENANCE_ENGINEER`) and document endpoints grant `PROVIDER_MANAGER` (`AssetDocumentController:51,58`). **Still open**: the asset profile itself does not (`AssetController:49,68` = `CLIENT`/`PLATFORM_ADMIN` only) and no service scopes the document grant to the caller's own provider (`grep PROVIDER src/main/java/.../assets/service/` → empty), so own-provider scope is neither granted on read nor enforced. | **1.2**, **6.3** |

**Role-area gap count: 15.**

---

## 6. Flow, API, and data gap register

### 6.1 Flow gaps

| ID | Gap | Owner |
| --- | --- | --- |
| `GAP-F-01` | **Text half CLOSED, runtime half open on `main`.** Text: `business-flows.md:229` (SF-03) now grants per-capability `VERIFIED` / `ADDITIONAL_INFO_REQUIRED` / `REJECTED` with explicit independence, so the C-4 contradiction is gone. Runtime: SF-02/SF-03 have **no Java on `main`** at `dc143ca` — only the `V12` schema landed (`grep -rn provider-organizations src/` → empty); the closure this row previously claimed came from unmerged `451a2af` (§0.1) and is re-opened as `GAP-A-01`. | **1.4** (runtime; 7.1 text verified done) |
| `GAP-F-02` | Asset-level airspace pre-check absent: no `ALTER TABLE assets` in `V12`–`V20` and no airspace symbol in `src/main/java`, so no `RESTRICTED_AIRSPACE`, `AIRSPACE_CHECK_PENDING` or `AIRSPACE_MANUAL_VERIFY_REQUIRED` state exists for an asset. Mission-level airspace determination now exists (`V17:83-86`: `NOT_CHECKED`/`CLEARANCE_REQUIRED`/`MANUAL_REVIEW`/`CLEARED`/`BLOCKED`) but is plan-scoped and a different vocabulary, so it does not satisfy SF-04. | **2.3** |
| `GAP-F-03` | Due-cycle publisher has no consumer. `InspectionScheduleDuePublisher` emits; nothing in `inspectionrequests` listens, so MF1 request packages are never generated. | **2.1** |
| `GAP-F-04` | MF1 request creation and RFQ sourcing have no runtime. | **2.1** |
| `GAP-F-05` | MF1 quotation has no capability-gate runtime — the capability tables now exist (`V12:105-142`) but nothing consults them (no `providerId` field in `src/main/java`) — and no Platform-AI/data/storage charge-exclusion rule (`grep -rni commission src/main/java` → empty). | **2.1** (gate), **2.2** (charges) |
| `GAP-F-06` | **Data half CLOSED by `V15`**: `platform_configurations` (`V15:40`, policy-key allow-list `V15:60-61`, one published version per key `V15:81-82`) and all four order snapshot columns (`V15:88-95`). Runtime half still open: nothing snapshots a policy at signing or records cancellation terms, because `inspectionrequests` has zero services and zero controllers. | **2.2** |
| `GAP-F-07` | **Removed from target by direct-transfer contract change (`business-flows.md` v3.3)** — the target has no funding or escrow step, so there is nothing to build. Row retained so the id stays reserved. | **4.2** (close as obsolete) |
| `GAP-F-08` | **CLOSED by PR #54 (`364a23e`)**: `DroneMissionPlanService.updateEquipmentAndSow` (`:125`) persists GSD/AGL/overlap/camera inputs on `drone_mission_plans`, and `addShotItem` (`:149`) persists gimbal/waypoint data on `mission_shot_items`; entities `DroneMissionPlan`/`MissionShotItem`, DTOs, and `DroneMissionPlanTest`/`MissionPlanApiIntegrationTest` cover the runtime. DDL half had closed by `V17`. | — (closed 2026-10-06) |
| `GAP-F-09` | **CLOSED by PR #54 (`364a23e`)**: `DroneMissionPlanService.approve` (`:212`) runs `plan.approve(...)` then `order.markReadyForFlight()` (`:224`) in one transaction, and `InspectionOrderStatus` now includes `READY_FOR_FLIGHT`. The V16/V17 data half was already closed. | — (closed 2026-10-06) |
| `GAP-F-10` | **Partially delivered by PR #54 (`364a23e`)**: `DroneMissionPlanService` persists `droneRegistrationId`, `pilotUserId` and the flight-permit reference (`verifyFlightPermit` `:187`, `updateEquipmentAndSow` `:125`), and mission plans are provider-scoped (`findByIdAndProviderId`). The checks themselves are still absent: no licence/credential validation against an authority registry, no conflict-of-interest field or rule anywhere in `src/main/java`, and no provider scoping on `inspection_assignments` (`V14:38-41` covers only quotations and orders). | **2.3** |
| `GAP-F-11` | MF2 field execution (MF2-07) is not mission-linked; `inspections` has no `mission_plan_id`. | **3.1** |
| `GAP-F-12` | GSD is stored and edited (`drone_mission_plans.target_gsd_mm_per_pixel`, `DroneMissionPlanService.updateEquipmentAndSow`:125) but the mm derivation still does not exist: no code multiplies pixel size by GSD, and `AiInferencePort` carries no GSD input. | **3.1** (with **2.3**) |
| `GAP-F-13` | Spatial telemetry depth missing: no AGL, no gimbal angle, no 3D coordinate on `evidence`. | **3.1** |
| `GAP-F-14` | **CLOSED by `d3a9f5d` (PR #51)**: peer review was deleted (`PeerReview`, `PeerReviewDecision`, `PeerReviewRepository`, both peer-review endpoints) and `V19:66` drops `peer_reviews`. The flow is now Inspector author verification (`submitForReview`, `InspectionReportService:214-230` — author-only `:218`, `DRAFT`-only `:221`, `ensureComplete` `:224`) followed by Provider Manager completeness and release (`:233-246`). The vocabulary difference this used to imply is tracked separately as `GAP-D-05`. | — (closed) |
| `GAP-F-15` | **CLOSED by `d3a9f5d`**: `POST .../release` is `hasRole('PROVIDER_MANAGER')` (`InspectionReportController:105-109`) and `release()` refuses anything but `TECHNICALLY_APPROVED` (`InspectionReportService:237`) — a state only the author step can produce (`:218-226`) — re-running `ensureComplete` at release (`:240`, definition `:565-572`). | — (closed) |
| `GAP-F-16` | **Data half CLOSED by `V15` + `V16`**: `locked_review_period_days` (`V15:89`) and `client_review_ends_at` with the `AWAITING_ACCEPTANCE` milestone rules (`V16:50`, `V16:151-191`). Timer runtime still absent: no code computes the review window or sweeps for deemed acceptance. | **4.2** |
| `GAP-F-17` | **Data half CLOSED by `V20`**: `dispute_tickets` exists (`V20:39`) with unique dispute number, polymorphic `order_id`+`order_type` (no FK by design, `V20:16-28`), parties/category/status/decision CHECKs, `provider_organization_id` (`V20:47`) and `evidence` JSONB (`V20:58`) — there is no `dispute_evidence` table by the minimal-schema decision (`V20:9-11`). Runtime still absent: no entity, service or controller (`grep -rni dispute src/main/java` → empty) and `PLATFORM_OPERATOR` is granted by no endpoint. | **4.1** |
| `GAP-F-18` | **Data half CLOSED by `V16`**: direct-transfer status sets (`V16:117-121` inspection, `V16:308-311` maintenance), milestone CHECKs (`V16:151-191`, `V16:355-367`), provider bank pair on both order tables (`V16:53-54`, `V16:264-265`), payment/paid instants (`V16:50-52`, `V16:262-263`) and `invoices.invoice_type` with one live commission per order (`V16:448-450`, `V16:653`, `V16:659`). Runtime half open: no invoice issuance, transfer confirmation or settlement code exists. | **4.2**, **5.3** |
| `GAP-F-19` | The entire MF5 runtime is absent: **9 entities, 9 repositories, 0 services, 0 controllers** — 9 of the 10 files under `maintenance/domain` carry `@Entity` (`MaintenanceTicketFindingId` is the embeddable key class); the previously recorded "10 entities, 10 repositories" was a miscount, corrected in this reconciliation. | **5.1**, **5.2** |
| `GAP-F-20` | **CLOSED by `V18`**: `ck_work_logs_evidence_pair` (`V18:341-345`) requires `before_evidence_id` and `after_evidence_id` present and distinct on a `VERIFIED` work log, both are separate FKs to `evidence` (`V18:290`, `V18:293`), and `ck_evidence_maintenance_pair` (`V18:226-229`) keeps `BEFORE_MAINTENANCE`/`AFTER_MAINTENANCE` rows attached to a work log. | — (closed) |
| `GAP-F-21` | **Data half exists** (`V12:105-142`: `provider_capabilities` with the four-outcome CHECK and the `(provider_id, capability_type)` unique key), gate runtime still absent: MF5 has no maintenance-capability check because no service or controller consults `provider_capabilities` (`grep -rln ProviderCapability src/main/java` → empty). | **5.1** |
| `GAP-F-22` | BR-31 ("at least one verified defect from an accepted report") is not enforced: the junction table exists but no service or CHECK requires a finding. | **5.1** |
| `GAP-F-23` | **Data half CLOSED by `V15` + `V18`**: order snapshot `locked_warranty_days`/`warranty_end_date` (`V18:50-51`, CHECK `V18:103-114`), ticket clock `accepted_at`/`warranty_started_at`/`warranty_ends_at` (`V18:118-121`, CHECK `V18:171-180`), auto-close sweep index `ix_maintenance_tickets_warranty_close` (`V18:184-185`), and `WARRANTY_DURATION` is a legal policy key (`V15:61`). Runtime half open: no countdown job, no free-rework claim flow, no maintenance service. | **5.2**, **5.3** |
| `GAP-F-24` | BR-37 re-inspection linkage is a bare column with no foreign key and no writer. | **5.3** |
| `GAP-F-25` | MF5 Q3 single-pending-change-request rule absent. | **5.2** |
| `GAP-F-26` | Notification delivery runtime absent although MF1 Q5, MF4 Q4, and FE-08 all require it. | **ORPHAN** |
| `GAP-F-27` | `dashboard` is a package-only module; FE-08 has no runtime and no Report 5 case. | **ORPHAN** |
| `GAP-F-28` | MF3 evidence quality & coverage gate absent: no blur, exposure, GPS-validity, or shot-list-coverage assessment exists in any form; no re-flight alert can be raised. | **3.1** |

**Flow-area gap count: 28** (26 owned, 2 orphan).

### 6.2 API gaps

| ID | Gap | Owner |
| --- | --- | --- |
| `GAP-A-01` | **OPEN on `main` — the previous closure cited an unmerged branch.** The four endpoints (onboarding POST, capabilities GET, per-capability decision POST, legal-identity standing POST; recorded in §4.2 and §2.6) do not exist at `dc143ca`: `grep -rn provider-organizations src/` → empty and none of the 10 `@RestController` classes on `main` is a provider-organization controller (asset catalog, asset document, asset, inspection schedule, schedule proposal, inspection, inspection report, browser auth, mobile auth, platform users). They exist only on `refactor/mf1-mf5-backend@451a2af`, which is not an ancestor of `origin/main` (§0.1). Schema prerequisite has landed: `V12` creates the four tables and `users.provider_id`. | **1.4** |
| `GAP-A-02` | `inspectionrequests` has zero controllers, so **no HTTP path can create a request, quotation, or order**. MF1 is unreachable, yet `inspections` requires a confirmed service order to start. | **2.1** |
| `GAP-A-03` | **CLOSED by PR #54 (`364a23e`)**: `DroneMissionPlanController` + `DroneMissionPlanService` + `DroneMissionPlan`/`MissionShotItem` entities + 7 DTOs + `MissionPlanApiIntegrationTest`/`DroneMissionPlanTest` deliver the endpoints; schema was already landed (`V17:38`, `V17:143`). | — (closed 2026-10-06) |
| `GAP-A-04` | `maintenance` has zero controllers: no ticket, assessment, order, work-log, evidence, or completion endpoint. | **5.1**, **5.2** |
| `GAP-A-05` | **CLOSED by `d3a9f5d` (PR #51)**: `PUT .../reviewer` and `POST .../review` were deleted with the peer-review code (`AssignPeerReviewerRequest`, `PeerReviewDecisionRequest`, the controller mappings), and `V19:66` drops `peer_reviews`. The completeness check they contradicted now runs inside `POST .../release` (`InspectionReportController:105-109` → `InspectionReportService:240` → `ensureComplete` `:565-572`) under `PROVIDER_MANAGER`, while `POST .../submit-review` is the author step (`:214-230`). No reviewer-assignment endpoint exists, matching the v3.4 target. | — (closed) |
| `GAP-A-06` | `GET /api/v1/reports` and `GET /api/v1/reports/{reportId}` grant three roles at the method level (`hasAnyRole('INSPECTOR','PROVIDER_MANAGER','CLIENT')`, `InspectionReportController:41,47`); cross-provider isolation depends entirely on service-level scoping with no cross-client contract test. | **3.2**, **8.1** |
| `GAP-A-07` | **Half closed by `d3a9f5d`**: document endpoints now grant `PROVIDER_MANAGER` (`AssetDocumentController:51,58` `hasAnyRole('CLIENT','PLATFORM_ADMIN','PROVIDER_MANAGER')`) and the review queue grants it too (`AssetController:59,84`), so a provider-scoped grant path exists. **Still open**: the asset reads themselves do not (`AssetController:49,68` = `hasAnyRole('CLIENT','PLATFORM_ADMIN')`), no `assets` service scopes the document grant to the caller's own provider, and zone mixing remains. | **1.2**, **6.3** |
| `GAP-A-08` | `client-decision` supports accept and revision only; no clarification state distinct from revision, no complaint branch. | **4.1** |
| `GAP-A-09` | No checked-in or published API contract artifact; springdoc exists in code only. | **8.1** |
| `GAP-A-10` | Mobile consumes only four paths and has no maintenance feature, though MF5 requires mobile before/after upload. | **6.4** |
| `GAP-A-11` | No cross-client Problem Details fixture pins `code`/`traceId`. On frontend `main` the `errorMessage`/problem-decoding logic is not shared; the Task 0.5 branch (`d28f700`) reports `problemError` duplicated in **4 files**, so the duplication will survive into Phase 6 unless it is consolidated there. | **8.1**, **6.1** |
| `GAP-A-12` | No legacy-role compatibility contract: nothing defines whether a client should reject, translate, or temporarily accept `ADMIN`/`SERVICE_MANAGER` during the migration window. The backend side is now decided — `V13` refuses to migrate while any `SERVICE_MANAGER` row exists (`V13:47-82`, with per-row remediation SQL) and Java only ever writes canonical codes (`Roles.java`, `UserRole.java`) — but no cross-client (web/mobile) behavior is specified. | **1.2** |
| `GAP-A-13` | **CLOSED by `V13` + `d3a9f5d`**: no `@PreAuthorize` in `src/main/java` authorizes `SERVICE_MANAGER` any more — asset review is `hasRole('PROVIDER_MANAGER')` (`AssetController:59,84`) and asset documents are `hasAnyRole('CLIENT','PLATFORM_ADMIN','PROVIDER_MANAGER')` (`AssetDocumentController:37,51,58`) — and `V13` removes the role from the data. Whether the reviewer *should* be `PLATFORM_OPERATOR` is tracked by `GAP-R-08`. | — (closed) |

**API-area gap count: 13.**

### 6.3 Data gaps

| ID | Gap | Owner |
| --- | --- | --- |
| `GAP-D-01` | **DDL half CLOSED by `V12`**: `CREATE TABLE provider_organizations` (`V12:50`) makes the table real, so counting it as implemented is no longer wrong. **Still open**: no JPA entity on `main` (`find src/main/java -iname "*Provider*"` → empty — tracked together with `GAP-R-04`). Documentation half CLOSED 2026-10-06: `database-design.md` §12 now records `V1`–`V21` and the deployed 44-application-table inventory. | **1.3** |
| `GAP-D-02` | **CLOSED by `V12`/`V14`/`V17`/`V20`**: every documented column now exists — `users.provider_id` (`V12:208`), `inspection_quotations` and `inspection_service_orders` (`V14:38-39`), `maintenance_orders` (`V14:41`, plus `maintenance_quotations` `V14:40`), `drone_mission_plans.provider_id` (`V17:42`, FK `V17:66-67`) and `dispute_tickets.provider_organization_id` (`V20:47`, named for its target table by design). `grep -rn provider_id src/main/resources/db/migration` now matches `V12`, `V14`, `V17`, `V20`. Note for the runtime tasks: no `providerId` field exists in `src/main/java` yet, and `inspection_assignments` was never given one (`V14:38-41`). | — (closed) |
| `GAP-D-03` | `security_audit_events` has no `organization_id`, `entity_type`, `entity_id`, or `details`. Only `actor_user_id`/`subject_user_id` exist. BR-38 (audit every material transition) is unrepresentable because workflow events cannot reference an entity. | **1.4** (first consumer), **7.1** (document) |
| `GAP-D-04` | **CLOSED by `V22` (PR #54, `1de6a7a`)**: `V22__report_author_verification_and_completeness.sql` adds `author_verified_by_user_id`, `author_verified_at`, `author_verification_snapshot`, `completeness_checked_by_user_id`, `completeness_checked_at`, `completeness_return_reason` (six nullable columns, backfilled from `technically_approved_at`/`created_by_user_id`, no CHECK/status edits). `ReportVersion.verify(actorId, contentSnapshot)` and `InspectionReportService.release` now stamp them. The runtime's re-validation of completeness in memory is unchanged; the columns now record who checked and when. | — (closed 2026-10-06) |
| `GAP-D-05` | Still open; implemented side re-verified at `dc143ca`. `ck_report_versions_status` is untouched since `V7` (`V7:232-233`: `DRAFT, AWAITING_PEER_REVIEW, CHANGES_REQUESTED, TECHNICALLY_APPROVED, RELEASED, REVISION_REQUESTED, ACCEPTED`) — `AWAITING_PEER_REVIEW` is now unreachable dead vocabulary since `V19` dropped `peer_reviews` and `ReportStatus` no longer contains it, while the Java enum (`DRAFT, CHANGES_REQUESTED, TECHNICALLY_APPROVED, RELEASED, REVISION_REQUESTED, ACCEPTED`) and the runtime deliberately reuse `TECHNICALLY_APPROVED` for author verification instead of the target's `AUTHOR_VERIFIED` / `COMPLETENESS_RETURNED` (`database-design.md:658`, `:863`). | **3.2** |
| `GAP-D-06` | **CLOSED by `V15`**: all four columns added at `V15:88-95` with pre-checks on the rate and day count (`V15:116-179`) and `locked_terms_snapshot` commented as the signing-time snapshot (`V15:105`). | — (closed) |
| `GAP-D-07` | **CLOSED by `V15` + `V18`**: `locked_commission_rate` and `locked_terms_snapshot` (`V15:187-189`, pre-check `V15:199-230`), `locked_warranty_days` and `warranty_end_date` (`V18:50-51`) with `ck_maintenance_orders_warranty` (`V18:103-114`). | — (closed) |
| `GAP-D-08` | **CLOSED by `V15`**: `CREATE TABLE platform_configurations` (`V15:40`) with the four-key allow-list `ck_platform_configurations_policy_key` (`V15:60-61`: `STANDARD_COMMISSION`, `CLIENT_REVIEW_PERIOD`, `CANCELLATION`, `WARRANTY_DURATION`), `uq_platform_configurations_key_version` (`V15:52`) and the one-published-per-key index `uq_platform_configurations_published` (`V15:81-82`). | — (closed) |
| `GAP-D-09` | **CLOSED by `V17`**: `CREATE TABLE drone_mission_plans` (`V17:38`) and `CREATE TABLE mission_shot_items` (`V17:143`) with the status, airspace, clearance-gate, approval-pairing, waypoint-pairing and GSD CHECKs (`V17:78-100`, `V17:159-175`). | — (closed) |
| `GAP-D-10` | **Removed from target by direct-transfer contract change (`business-flows.md` v3.3)** — the target contains no `escrow_transactions` table to create. Row retained so the id stays reserved. | **4.2** (close as obsolete) |
| `GAP-D-11` | **CLOSED by `V20`**: `CREATE TABLE dispute_tickets` (`V20:39`) with unique dispute number, `order_id` + `order_type` polymorphic pair (no FK by design, `V20:16-28`), parties, category/status/reason/decision CHECKs, resolution pairing rules and `evidence` JSONB (`V20:58`, array CHECK `V20:100-101`). **`dispute_evidence` is not a gap and never was a planned table**: the contract owner folded attachments into `dispute_tickets.evidence` (`V20:9-11`). | — (closed) |
| `GAP-D-12` | **CLOSED by `V12`**: `CREATE TABLE provider_capabilities` (`V12:105`), `uq_provider_capabilities_capability UNIQUE (provider_id, capability_type)` (`V12:123`), four-outcome `ck_provider_capabilities_status` (`V12:126-127`) plus the decide-pairing CHECK (`V12:131-134`) — BR-41 independence is now representable, with `provider_vetting_decisions` (`V12:148-161`) as the append-only history. | — (closed) |
| `GAP-D-13` | **CLOSED by `V12`** (main numbering — the earlier `V14` citation came from the unmerged task branch): `provider_organizations.status` (`V12:74-75`: `PENDING/VERIFIED/SUSPENDED/BANNED`) and `provider_capabilities.status` (`V12:126-127`: `PENDING/ADDITIONAL_INFO_REQUIRED/VERIFIED/REJECTED`) are two columns with two CHECK vocabularies, so a per-capability rejection and `ADDITIONAL_INFO_REQUIRED` are both expressible. **Correction from this reconciliation**: the "independently *reachable*" extension cited a standing endpoint that is **not on `main`** (`GAP-A-01` re-opened); on `dc143ca` the two axes are schema-reachable only (`standing_decision_reason` `V12:63`, `ck_provider_org_standing_reason` `V12:90`). `SUSPENDED`/`BANNED` remain unreachable from any endpoint; no task owns that lifecycle yet. | — (closed); suspension lifecycle unowned |
| `GAP-D-14` | **CLOSED by `V16`**: `invoices.invoice_type` (`V16:448`: `MAINTENANCE_SERVICE` default, `INSPECTION_SERVICE`, `COMMISSION`) with `inspection_service_order_id` and `provider_organization_id` (`V16:449-450`), the per-type binding CHECK `ck_invoices_type_and_order` (`V16:573-589`), and BR-36's single-commission rule as two unique indexes — `uq_invoices_commission_inspection` (`V16:653`), `uq_invoices_commission_maintenance` (`V16:659`) — over non-VOID commission invoices (`V16:599-648`). | — (closed) |
| `GAP-D-15` | `evidence` has `latitude`, `longitude`, `capture_time` but no altitude/AGL, no gimbal angle, no 3D coordinate. `assets` has no airspace-restriction column. | **3.1**, **2.3** |
| `GAP-D-16` | `inspection_requests.linked_maintenance_ticket_id` (`V6:13`) is a bare `UUID` with **no foreign key** to `maintenance_tickets`. | **5.3** |
| `GAP-D-17` | **Constraint half CLOSED by `V18`**: `maintenance_work_logs.before_evidence_id`/`after_evidence_id` (`V18:238-239`) are two FKs (`V18:290`, `V18:293`) guarded by `ck_work_logs_evidence_pair` (`V18:341-345`, both present and distinct on a `VERIFIED` log), and `ck_evidence_maintenance_pair` (`V18:226-229`) keeps `BEFORE_MAINTENANCE`/`AFTER_MAINTENANCE` rows attached to a work log. **API half still open**: `maintenance` has zero controllers, so no path can create either row (`GAP-A-04`). | **5.2** |
| `GAP-D-18` | **CLOSED by `V19` + the documentation update**: `V19:66` drops `peer_reviews` behind a fail-closed pre-check (`V19:19-54`), so the table no longer exists in the physical schema, and `database-design.md:45` now records the removal explicitly ("`peer_reviews` … removed by the V12+ migration set"), while no `report_versions` prose references peer review any more (`grep -i peer` over `database-design.md` matches only that removal note). Inventory and schema now agree: 44 application tables + `event_publication`. | — (closed) |
| `GAP-D-19` | Report 5 baseline is 33 cases: 13 Passed, 20 Pending, 0 Failed. Nine target cases (`WF2-005`–`WF2-007`, `WF3-005`–`WF3-008`, `WF4-004`–`WF4-005`) are Pending with no execution. FE-08 has zero cases. `FE01-T01`/`FE01-T02` are Pending. `WF1-005`–`WF1-010` are unallocated and must not be reused. | **7.2** |
| `GAP-D-20` | Report 5 internal staleness: `fe-01-…md:9` and `README.md:47` still say "15-case workbook totals" while the total is 33; `cover.md`'s change table skips version 1.4 which exists in `00-cover/record-of-changes.md`; `fe-02-…md` has UTF-8 mojibake (`Hi?u`, `organizationâ€™s`); a stale 15-case preview artifact sits in `outputs/`. | **7.2** |
| `GAP-D-21` | No Report 5 test ID exists for five of the seven mandatory negative obligations in §7: role migration, provider-capability independence, unassigned-workforce access, author-verification release, and before/after completion. Only cross-provider bid isolation (`WF2-005`) and partner fail-closed (`WF3-008`) have IDs, and both are Pending. | **7.2** |
| `GAP-D-22` | Document path prefixes are wrong throughout the plan and brief: they spell repository content as `docs/project-reference/…`, `docs/backend/…`, `docs/reports/…`, but this repository's content root has no nested `docs/` on `main`. Every such path in the plan fails to resolve. | **7.1** |

**Data-area gap count: 22.**

### 6.4 Gap totals

| Area | Gaps | Owned by a task | Orphan |
| --- | ---: | ---: | ---: |
| Role / actor-zone | 15 | 15 | 0 |
| Flow | 28 | 26 | 2 |
| API | 13 | 13 | 0 |
| Data | 22 | 21 | 1 (same as `GAP-F-26`) |
| **Total recorded** | **78** | **75** | **3** |

`GAP-F-07` and `GAP-D-10` are **obsolete by contract change**: `business-flows.md` v3.3
removed funding/escrow from the target entirely, so their owning task closes them as
"no longer applicable". Their rows stay so the ids remain reserved and the counts above
stay stable.

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
| N-10 | **No payment integration** | No payment integration exists anywhere: settlement is a direct bank transfer between Client and Provider, so no partner or product support is required for any flow, and no Platform-side custody of funds is possible. The order, report, and maintenance state is preserved unchanged. | 2.2, 4.2, 5.3 | `PaymentPartnerBoundaryTest`, `ComplaintHoldBoundaryTest`, `SettlementPolicyTest`; `WF3-008` (Pending) |
| N-11 | **Commission applied once** | Commission applies once to eligible VAT-exclusive value; a refund reverses it proportionally; no second commission is ever charged on the same order. | 4.2, 5.3 | `SettlementPolicyTest`; `WF3-007`, `WF4-004`, `WF4-005` (Pending) |
| N-12 | **Accepted-report immutability** | An accepted report version cannot be updated; a correction creates a linked version. | 3.2, 4.1 | `InspectionReportApiIntegrationTest` |
| N-13 | **Complaint pauses acceptance and payment** | A timely complaint blocks deemed acceptance and moves the order to workflow state `DISPUTED`; an unresolved warranty claim blocks automatic ticket closure. Concurrent accept and complaint serialize to one transition. | 4.1, 5.3 | `ComplaintWorkflowTest`, `MaintenanceWarrantyRetentionTest` |
| N-14 | **Evidence duplicate and integrity** | A duplicate SHA-256 within one inspection or one maintenance work log is rejected without creating a junk row. Missing GPS is recorded, not rejected. An object-storage path alone grants no access. | 3.1, 5.2 | `EvidenceServiceTest`, `EvidenceApiIntegrationTest`; `WF3-002` (Passed) |
| N-15 | **AI failure fallback** | YOLO or LLM unavailability never discards evidence and never blocks manual finding entry. Rejected or unverified candidates never reach Client-visible statistics or reports. | 3.1 | `InspectionWorkflowTest`; `WF3-003` (Passed) |
| N-16 | **Onboarding grants no downstream authority** | Provider onboarding must not create an accepted order, grant inspection or maintenance eligibility, or grant mission clearance. | 1.4 | `ProviderOnboardingApiIntegrationTest.onboardingGrantsNoCapabilityEligibilityThroughTheGate_N16` (asserted through `ProviderEligibilityFacade`, not only through the record) |
| N-17 | **Client-contract drift** | Web and mobile must decode the same success envelope, `204`, binary stream, and Problem Details with `code`/`traceId`, and must not silently break on legacy role strings. | 6.1, 6.4, 8.1 | Cross-client contract fixtures |
| N-18 | **Separation of duties** | `PLATFORM_ADMIN` cannot publish commercial policy or vet a Provider. `PLATFORM_OPERATOR` cannot administer platform security settings. | 1.2, 1.4 | `RolePolicyTest`, `ProviderVettingApiIntegrationTest` |

---

## 8. Unique root causes

The 78 recorded gaps reduce to these root causes. Fixing a root cause closes every gap
listed against it. Excluded here: `GAP-F-07` and `GAP-D-10` (obsolete by the
direct-transfer contract change) and `GAP-F-28` (no single root cause in this table; tracked
only in §6). Ids marked **CLOSED** were already closed at this baseline — see their §5/§6
rows for the evidence — and stay listed against the root cause that produced them.

| Root cause | Gaps closed |
| --- | --- |
| R-A. Legacy five-role identity with no provider linkage and the wrong zone names | `GAP-R-01` **CLOSED**, `GAP-R-02`, `GAP-R-03` **CLOSED**, `GAP-R-14`, `GAP-R-15`, `GAP-A-12`, and the role-rename part of `GAP-R-08`, `GAP-A-07`, `GAP-A-13` **CLOSED** |
| R-B. No Provider Organization aggregate or capability model | `GAP-R-04`, `GAP-R-05`, `GAP-R-06` **CLOSED**, `GAP-D-01`, `GAP-D-02` **CLOSED**, `GAP-D-12` **CLOSED**, `GAP-D-13` **CLOSED**, `GAP-F-01`, `GAP-A-01`, and the capability-gate half of `GAP-F-05` |
| R-C. `inspectionrequests` is persistence-only | `GAP-F-03`, `GAP-F-04`, `GAP-A-02` |
| R-D. No commercial-policy or snapshot layer | `GAP-F-06`, `GAP-D-06` **CLOSED**, `GAP-D-08` **CLOSED**, and the charge-exclusion half of `GAP-F-05` |
| R-E. MF2 mission planning absent | `GAP-F-08` **CLOSED**, `GAP-F-09` **CLOSED**, `GAP-F-10`, `GAP-A-03` **CLOSED**, `GAP-D-09` **CLOSED** |
| R-F. Field execution not mission-linked; telemetry depth insufficient | `GAP-F-02`, `GAP-F-11`, `GAP-F-12`, `GAP-F-13`, `GAP-D-15` |
| R-G. Report workflow was peer review, not author verification | `GAP-F-14` **CLOSED**, `GAP-F-15` **CLOSED**, `GAP-D-04` **CLOSED**, `GAP-D-05`, `GAP-A-05` **CLOSED** |
| R-H. No complaint or direct-settlement layer | `GAP-F-16`, `GAP-F-17`, `GAP-F-18`, `GAP-A-08`, `GAP-D-11` **CLOSED**, `GAP-D-14` **CLOSED** |
| R-I. `maintenance` is persistence-only | `GAP-F-19`, `GAP-F-20` **CLOSED**, `GAP-F-21`, `GAP-F-22`, `GAP-F-23`, `GAP-F-24`, `GAP-F-25`, `GAP-A-04`, `GAP-D-07` **CLOSED**, `GAP-D-16`, `GAP-D-17` |
| R-J. Clients still model the v1 role/portal world | `GAP-R-09`, `GAP-R-10`, `GAP-R-11`, `GAP-R-12`, `GAP-R-13`, `GAP-A-06`, `GAP-A-10`, `GAP-A-11` |
| R-K. Documentation has no enforced consistency check | `GAP-R-07`, `GAP-A-09`, `GAP-D-03`, `GAP-D-18` **CLOSED**, `GAP-D-19`, `GAP-D-20`, `GAP-D-21`, `GAP-D-22` |
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
3. **Migration numbers are forward-only.** On `main` @ `7b40ef4` the chain is `V1`–`V21`
   with no gaps (`ls src/main/resources/db/migration`; `WorkflowBaselineTest:90-107`
   derives the head and the exact 1..N history from the directory itself): `V12` provider
   organizations and capability vetting, `V13` canonical roles, `V14` provider-scoped
   commercial records, `V15` MF1 commercial policy snapshots, `V16` direct-transfer
   settlement, `V17` drone mission plans, `V18` MF5 warranty and evidence closure, `V19`
   drops `peer_reviews`, `V20` dispute tickets, `V21` maintenance `DISPUTED` state.
   **The next free number is `V23`** (V22 landed 2026-10-06 via PR #54). The
   plan's illustrative `V12`–`V15` numbers are spent, and the branch-local numbering
   quoted in earlier revisions of this rule (`refactor/wf1-contract`'s `V12`, the fix
   round's `V15`) belonged to branches that are **not** on `main` (§0.1) and must not be
   reused as citations.
4. **Never introduce `MAINTENANCE_PROVIDER_MANAGER`** or any seventh role. If a
   requirement appears to need one, the requirement is wrong, not the role list.
5. **A capability decision never cascades.** If a code path, constraint, or UI action
   would let one capability's decision change another, that is a defect in the new code,
   not an interpretation of BR-41.
6. **Target-only integrations fail closed.** No adapter means the operation is blocked
   and the order/report state is preserved. A deterministic test fixture is acceptable
   evidence of contract behavior; it is never evidence that a real external integration
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
