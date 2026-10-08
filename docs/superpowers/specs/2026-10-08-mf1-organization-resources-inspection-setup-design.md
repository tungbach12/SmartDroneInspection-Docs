# MF1 Organization Resources and Inspection Setup Design

**Date:** 2026-10-08  
**Status:** Draft for user review  
**Scope:** Full current MF1-01–MF1-14 backend workflow, with ORG_ADMIN web support only where needed to operate MF1.  
**Out of scope:** Supporting Flow organization registration and subscription activation; MF2 readiness/field sessions; MF3 evidence/findings/reports; MF4 maintenance; external permit issuance/registry verification; Drone flight control; marketplace/provider/quotation/settlement behavior; mobile workflow UI.

## 1. Purpose and current contract

Deliver the current four-role Enterprise SaaS MF1 from organization resource management through an identified, assigned inspection dispatched to its Inspector. MF1 must not restore the retired WF1 schedule-proposal flow or the marketplace model.

Binding requirements:

- `project-reference/business-flows.md` v4.0, §I, §IV MF1-01–MF1-14 and §VII.
- Report 3 `reports/report-3-software-requirement-specification/03-functional-requirements.md`, FE-01 and FE-02, especially §3.3.1.
- Storage contract: `project-reference/database-design.md` §6.1–§6.4 and §7.
- Backend reset guardrails: backend `.hermes/plans/2026-10-07_enterprise-saas-backend-and-full-db.md`.

Current roles are exactly `ADMIN`, `ORG_ADMIN`, `INSPECTOR`, and `MAINTENANCE_ENGINEER`. Supporting Flow registers an organization and activates its subscription; MF1 consumes that established organization and entitlement. `ADMIN` does not perform customer technical decisions.

The previous five-role WF1 schedule-proposal implementation was removed in the Enterprise SaaS reset. Historical WF1 tests/results remain historical evidence only and must not be reinterpreted as current MF1 verification.

## 2. Goals and non-goals

### Goals

1. Let an ORG_ADMIN manage organization resources used by MF1: workspace contacts/reviewers, own workforce, applicable credential records, Drone inventory/documents, and permit/compliance records.
2. Create an asset with exactly one active default Inspector/Drone pair, validating same-organization scope and saving atomically.
3. Create an inspection for an existing asset; snapshot the selected asset pair, scope, dates and applicable source-document references.
4. Generate a scheduled inspection idempotently for an explicit schedule/due-cycle identity when cadence is configured.
5. Detect known Inspector/Drone time conflicts, support reasoned versioned reassignment, and dispatch only after ORG_ADMIN confirmation.
6. Notify the assigned Inspector and preserve audit attribution without implying actual flight control or permit verification by an authority.

### Non-goals

- Organization registration or subscription plan activation/renewal screens: Supporting Flow.
- MF2 preparation, permit readiness approval, pre-flight checklist, field-session start/end or flight telemetry.
- MF3 evidence acceptance, AI findings, report authoring/review/publication.
- MF4 work orders, repair execution, cost management or acceptance.
- Government registry/permit verification, external email delivery guarantee, certified e-signature, drone control, or live schedule-conflict integration with external calendars.
- Retired provider/marketplace schedule proposals, RFQ, quotation, commission, Client role or old six-role behavior.

## 3. Verified implementation baseline on 2026-10-08

Backend `main` is `36b2e3b`; docs `main` is `f8f8352`; frontend `main` is `786a3bf`; mobile `main` is `bc5c6d0`.

Present on backend `main`:

- Four-role authentication, organization registration, role/actor-zone checks, platform user management and audit migration/runtime.
- Asset category/checklist and organization-scoped asset CRUD/document behavior, with changes from the Enterprise SaaS reset.
- V24–V26 target schema: Drone inventory, asset-pair assignments, cadence fields, inspection snapshots and workflow storage tables.

Not present as Java runtime on backend `main`:

- ORG_ADMIN workforce provisioning and credential CRUD/review.
- Subscription entitlement application facade/API used by MF1.
- Drone entity/repository/API and Drone document management.
- Flight-permit/compliance record management.
- Asset-pair assignment entity/repository/use cases.
- Inspection creation, cadence/due-cycle generation, pair/scope snapshots, conflict checks, reassignment history, dispatch and MF1 notification production.

Schema existence is not workflow implementation. No current MF1 API or test may be claimed complete until runtime and executable tests exist.

## 4. MF1 behavior

### 4.1 Organization context and entitlement (MF1-01–02)

- ORG_ADMIN can view/update the permitted organization workspace profile fields and maintain named authorized reviewers inside their own tenant.
- All MF1 mutations resolve the actor from the authenticated principal and organization membership from the users module; tenant IDs in request bodies are rejected/ignored, never used to select scope.
- Every new MF1 resource/inspection creation or dispatch checks organization status and current subscription entitlement through a subscriptions-owned boundary. Expired/suspended entitlement blocks new work but does not delete or hide historical records. Exact rules use subscription state/status and effective dates already defined by current docs; no hard-coded trial, grace period, fee or renewal behavior is introduced.
- ADMIN subscription activation remains Supporting Flow. MF1 does not create or activate subscriptions.

### 4.2 Workforce and credentials (MF1-03–05)

- ORG_ADMIN can provision only `INSPECTOR` and `MAINTENANCE_ENGINEER` users in their own organization, and can update/suspend/reactivate only those users in that organization. ORG_ADMIN cannot create ADMIN or ORG_ADMIN accounts, change tenant ownership, or elevate a user to a platform role.
- Account creation uses the current password setup/session policy; no raw credential is logged or returned as a reusable access token. Account activation is distinct from credential qualification.
- Credential records are person- and organization-scoped, typed, dated, attributable, and retain evidence reference/status/review actor where current schema supports it. Credentials are relevant records, not claims of government verification or professional certification by the platform.
- Validation may calculate date-based states/expiry warnings but cannot infer statutory licensing requirements or issue a government validation result. Human review is explicitly attributable.

### 4.3 Drone and compliance records (MF1-06–07)

- ORG_ADMIN can create, read, update and retire organization-owned Drones, with organization-local serial uniqueness and serviceability state (`ACTIVE`, `MAINTENANCE`, `SUSPENDED`, `RETIRED`). Retire/suspend does not erase historical pair or inspection snapshots.
- Drone documents and applicable permit records retain issuer/reference, scope, validity, status, evidence reference and human review attribution where defined in schema. Application, issued permit, expiry, rejection, revocation and not-applicable remain distinct states.
- A Drone is eligible for a new asset pair only when it belongs to the caller organization and is `ACTIVE`. MF1 records permit/compliance inputs; MF1 does not declare flight readiness or verify an external authority registry.

### 4.4 Asset and default pair (MF1-08–10)

- ORG_ADMIN creates an asset with organization-local asset code, category, components/type, location, technical context, access/contact context, source-document references and known limitations.
- The asset creation contract requires one `inspectorId` and one `droneId`. The backend resolves both within the authenticated organization; the Inspector must be active and role `INSPECTOR`, and the Drone must be serviceable `ACTIVE`.
- The asset and one `ACTIVE` `asset_pair_assignments` record are persisted in one transaction. Pair status, organization, asset, Inspector, Drone, `valid_from` and assigning ORG_ADMIN are stored. If any validation or persistence step fails, neither the asset nor pair remains.
- Asset code uniqueness is enforced for the organization. Pair uniqueness/tenant composite FKs use V26 schema constraints. The pair is a mutable default for future inspections, not an exclusive Drone reservation, permit or readiness decision.
- Asset read/list/update and asset-document operations remain scoped to the caller tenant. This feature does not add ADMIN global asset access; any audited support access needs a separate approved authorization contract.

### 4.5 Inspection setup, cadence and snapshot (MF1-11–12)

- ORG_ADMIN creates an inspection against an existing same-organization asset with objective, component scope, acceptance criteria, planned dates and optional cadence.
- The system inherits the asset's current active pair, creates an immutable/versioned inspection assignment snapshot containing the pair and relevant defaults/source-document references, and keeps it distinct from later changes to the asset default.
- If cadence is absent, only a manually initiated inspection is created; the system must not invent a schedule. If cadence is present, a scheduler/explicit due processor creates one inspection per `(schedule_id, due_cycle_key)` using the database unique identity and idempotent retry behavior.
- Inspection status starts at `DRAFT` or `ASSIGNED` according to the explicit ORG_ADMIN confirmation step; no state implies MF2 readiness or field execution.

### 4.6 Conflict check, reassignment and dispatch (MF1-13–14)

- The system checks known overlapping planned intervals against other non-cancelled inspections for the selected Inspector and Drone in the same organization. It returns the conflicting inspection identifiers and times; it does not consult an external calendar or claim conflict-free real-world availability.
- Unresolved conflict, inactive/suspended person, unavailable Drone, missing entitlement, incomplete scope, or invalid source records block confirmation/dispatch.
- ORG_ADMIN explicitly confirms the pair, dates and scope. Reassignment records a reason and an explicit scope: current inspection only or future asset default. Assignment history is append-only/versioned; past inspections never change when the asset default changes.
- Dispatch is a persisted workflow transition and an in-app notification/audit record. It includes inspection, asset, scope, dates, Inspector, Drone, assignment version and relevant document references. Notification delivery does not grant resource access. Dispatch is not mission readiness, permit approval or drone control.

## 5. Module and transaction boundaries

- `users`: identity, organization and role checks; expose the minimum users-owned facade to verify active user/role/tenant. No cross-module controller or repository imports.
- `subscriptions`: read-only entitlement facade for MF1; subscription creation/activation stays Supporting Flow.
- `workforce`: credentials and their review/evidence references.
- `assets`: asset catalog, Drone inventory/documents, permit/compliance records, asset-pair assignment history. Drone/pair owner remains `assets` per the reset approval.
- `inspections`: schedule, inspection aggregate, immutable assignment/scope snapshots, due-cycle identity, conflict check and dispatch use cases.
- `notifications`: in-app records produced after successful dispatch; notifications never grant authorization.
- `shared`: existing API envelope, ProblemDetail and security context contracts only.

Required transaction units:

1. Asset + initial pair creation is atomic in one `assets` application-service transaction.
2. Inspection + assignment snapshot + cadence/due-cycle identity is atomic in one `inspections` transaction.
3. ORG_ADMIN reassignment changes the current inspection snapshot/version and optionally the future asset default in one transaction; immutable historical versions remain.
4. Dispatch state, audit event and notification record are committed together, or published through an already configured transactional event mechanism if one exists. Do not add a new queue/event bus solely for this work.

Cross-module references remain scalar UUID/facade calls. Keep repository queries organization-scoped; never load globally then filter in memory.

## 6. Proposed API surface

Exact route names may follow current controller conventions in the implementation plan, but semantics are fixed:

| Capability | Role/scope | Required behavior |
| --- | --- | --- |
| View/update own workspace profile and authorized reviewers | ORG_ADMIN, own org | No tenant selector in body; preserve creator and audit history. |
| Provision/list/update/suspend workforce | ORG_ADMIN, own org | Only INSPECTOR/MAINTENANCE_ENGINEER; no role escalation or cross-org IDs. |
| Create/list/update Drone and Drone documents | ORG_ADMIN, own org | Serial uniqueness per org; eligible selection requires ACTIVE serviceability. |
| Create/list/update permit/compliance records | ORG_ADMIN, own org | Record human review and source; no external verification claim. |
| Create asset with pair | ORG_ADMIN, own org | Asset and pair atomic; pair IDs required. |
| List/detail/update asset | ORG_ADMIN, own org | Keep tenant scope; no new global ADMIN grant. |
| Create/list inspection | ORG_ADMIN, own org | Existing asset only; explicit scope/date/cadence; pair snapshot. |
| Reassign/confirm inspection | ORG_ADMIN, own org | Reasoned, versioned; resolve known conflicts. |
| Process due cadence | SYSTEM | Idempotent per schedule/due-cycle key. |
| Dispatch inspection | ORG_ADMIN confirmation then SYSTEM | Persist status/audit/notification; no MF2 readiness. |

All successful JSON uses `ApiResponse<T>`; expected errors use RFC 9457 ProblemDetail with stable codes. Cross-tenant resources return non-disclosing 404. Input records use Jakarta validation. Do not expose provider, client marketplace, schedule-proposal, quotation, commission, or old six-role APIs.

## 7. Data and concurrency rules

- Use current V25/V26 target schema; first plan task must compare every required column/FK/index with live schema and add a forward migration only for a proven gap. Never modify V1–V26.
- Pair assignment must satisfy composite tenant FKs for asset, Inspector and Drone and the partial unique active-pair-per-asset index.
- Inspection snapshots store pair assignment ID and denormalized Inspector/Drone IDs plus organization, scope and source references; read-time behavior must not silently substitute current asset defaults.
- Due-cycle idempotency uses `(schedule_id, due_cycle_key)`; retry returns/recognizes the existing inspection and does not create duplicate dispatch/notification records.
- Concurrent asset-code or active-pair conflicts map to expected 409 ProblemDetail, not 500. Concurrent reassign/confirm uses row version/optimistic locking; a stale update returns conflict and leaves the newer assignment intact.
- Conflict detection is a conservative application query over current organization records and planned intervals. It is informational until ORG_ADMIN resolves; no automatic reassignment or unlogged override.

## 8. Failure and security behavior

- Caller missing/inactive or wrong role: 401/403 as current security policy.
- ORG_ADMIN has no organization or organization/subscription is not eligible: deny creation/dispatch with stable `ORGANIZATION_REQUIRED` / `SUBSCRIPTION_INACTIVE` codes; history remains readable according to current role/tenant policy.
- Foreign asset/Inspector/Drone/credential/permit: non-disclosing 404.
- Same-tenant inactive user, wrong role, suspended/retired Drone, expired/revoked applicable record, invalid asset category, invalid dates or incomplete required fields: 400/409 with a stable code and actionable safe detail.
- Duplicate asset code or one-active-pair constraint violation: 409; transaction rolls back all new rows.
- Inspection snapshot persistence failure: no partial inspection record; test against real PostgreSQL.
- Known overlap: return conflict list; dispatch stays blocked until ORG_ADMIN resolves through reschedule or versioned reassignment.
- Notification failure must not silently mark a transition uncommitted or claim delivery; persist the in-app notification with dispatch or use existing transactional delivery behavior.

## 9. Acceptance and verification

MF1 is accepted only when all groups below have runtime and executable tests:

1. **01–02:** own workspace, role/tenant/subscription checks; expired entitlement blocks new work and preserves history.
2. **03–05:** ORG_ADMIN provisions only allowed workforce roles; credentials are tenant/user scoped; disabled/wrong-role users cannot pair.
3. **06–07:** Drone/permit CRUD and document references are tenant-scoped; unavailable Drone cannot pair; no authority-verification claims.
4. **08–10:** asset + pair atomicity, tenant equality, role/state checks, duplicate code and rollback.
5. **11–12:** inspection creation only for existing asset; pair/scope snapshot immutability; cadence optional; due-cycle retry idempotency.
6. **13–14:** date-overlap conflict response; versioned reassignment with reason/scope; dispatch authorization, audit and notification exactly once.
7. **Cross-cutting:** role matrix, cross-tenant negative tests, Modulith boundary, clean Flyway migration + JPA validation, web client tests for any changed API, Report 5 evidence.

Use Testcontainers PostgreSQL for persistence/transaction/constraint tests. Run focused tests for each slice, `./mvnw spotless:check`, then `./mvnw verify`. Frontend tests/build are required only for a changed web contract. Report 5 target cases stay `Pending` until exact executable evidence passes; preserve historical WF1 rows/outcomes unchanged.

## 10. Risks and explicit boundaries

- MF1 is a cross-module workflow. Implement it in the dependency order: entitlement/workforce/Drone/compliance → asset/pair → inspection/snapshot/cadence/conflict → reassignment/dispatch.
- Subscription activation and organization registration are Supporting Flow prerequisites, not MF1 deliverables.
- The current documents do not specify entitlement grace periods, invitation email delivery, external credential verification, conflict override, or global ADMIN support-access policy. Do not invent these; use fail-closed defaults and surface any needed human ruling in the implementation plan.
- MF1 dispatch hands off to MF2. Do not implement MF2 acceptance, readiness, permits approval, field sessions or flight execution as part of MF1.
- The old WF1 proposal flow, old v1 roles, marketplace, direct-transfer/commission and MF5 reset logic are historical and must not be reintroduced.
