# Documents-Led MF1–MF5 Refactor Design

**Date:** 2026-10-04  
**Status:** Draft for review  
**Scope:** Backend, frontend, mobile, database, and documentation repositories

## 1. Purpose and source of truth

This design defines the refactor required to bring the SmartDroneInspection source repositories into alignment with the current project documents. The authoritative product contract is the current Report 3 SRS, the Report 3 appendix, `docs/project-reference/business-flows.md`, and `docs/project-reference/database-design.md`. Existing source code and migrations are the implementation baseline, not the target contract: the documents explicitly state that the current code is v1 and that several target capabilities are not yet implemented.

The target is the six-role, three-actor-zone, multi-provider model and five canonical transactional Main Flows:

- `MF1` — Survey Request, Quotation Sourcing & Conditional Funding
- `MF2` — Drone Mission Planning & Airspace Clearance
- `MF3` — Drone Survey, Evidence, AI Verification & QA Report
- `MF4` — Report Acceptance, Settlement & Complaints
- `MF5` — Defect Rectification, Maintenance & Retention

Organization registration, Provider capability selection/vetting, asset master data, and recurring schedule setup remain the Supporting Flow (`SF`) and are prerequisites rather than a sixth Main Flow.

The refactor is intentionally large. It is not limited to the provider-capability wording already added to Report 3, and it is not a request to preserve every legacy type or table shape. Destructive changes must still be executed through reviewed forward migrations and compatibility steps, never by silently rewriting shared migration history.

## 2. Target architecture

### 2.1 Actor zones and roles

The implementation will converge on exactly six canonical roles:

- `PLATFORM_ADMIN`: technical configuration, security, checklist templates, and technical audit.
- `PLATFORM_OPERATOR`: business operations, Provider vetting, commercial-policy publication, payment-partner coordination, and internal complaint handling. It is not a legal arbitrator or deposit custodian.
- `CLIENT`: customer organization operations, asset/request/order/report/ticket decisions.
- `PROVIDER_MANAGER`: Provider Organization representative, quotations, mission planning, permits, workforce assignment, QA completeness, and maintenance quotations/orders.
- `INSPECTOR`: assigned manual field flight, evidence, AI-candidate verification, and verification/editing of the draft the Inspector authored.
- `MAINTENANCE_ENGINEER`: assigned technical assessment, repair work, work logs, and mandatory before/after evidence.

`PROVIDER_MANAGER` is not split into inspection and maintenance manager roles. Inspection and maintenance capability are organization eligibility data, not user roles. A Provider Organization may declare inspection, maintenance, or both, and each capability is vetted independently.

### 2.2 Module boundaries

The current Java modular monolith remains the physical architecture. The refactor evolves existing modules and adds only capabilities that have a concrete target slice:

- `users`: canonical identity, actor zones, Provider Organizations, Provider workforce linkage, sessions, role policy, and audit.
- `assets`: asset catalog, checklists, schedules, and Supporting Flow asset setup.
- `inspectionrequests`: MF1 request sourcing, quotations, service orders, conditional-funding contract snapshots, and assignments.
- `inspections`: MF2 mission-plan data and MF3 inspection execution, evidence, findings, reports, and release.
- `maintenance`: MF5 tickets, assessments, quotations, orders, assignments, work logs, change orders, and warranty/retention.
- `notifications`: post-commit workflow notifications.
- `dashboard`: read-only composition after the underlying slices exist.
- `shared`: response envelope, errors, security support, pagination, and cross-cutting contracts only.
- `infrastructure`: feature-owned outbound ports and MinIO/AI/payment-partner adapters; business modules never import it directly.

No global entity package, generic workflow module, separate drone-control platform, autonomous flight service, or generic “provider manager” abstraction will be introduced.

### 2.3 Data model

PostgreSQL remains the transactional source of truth and Flyway remains forward-only. MinIO stores file bytes; PostgreSQL stores object keys, checksums, sizes, media metadata, ownership, and workflow context.

The target identity model contains separate customer `organizations` and `provider_organizations`. Provider workforce users reference `provider_id`; customer users reference `organization_id`; platform users reference neither. `user_roles` stores the six canonical role codes.

Provider onboarding stores shared legal identity once and capability-specific records/evidence separately. The UI “both” choice creates two capability records. Each capability has its own status (`PENDING`, `ADDITIONAL_INFO_REQUIRED`, `VERIFIED`, `REJECTED`, with suspension/retirement behavior defined where the final state model requires it), decision actor, decision time, evidence, reason, and audit history. A capability-specific eligibility gate protects every inspection or maintenance quotation/order/assignment path.

Transactional records carry organization/provider/assignment scope in relational keys. Mutable aggregates use optimistic locking. Final quotations, orders, report versions, decisions, audit records, and evidence metadata remain historical rather than being overwritten or hard-deleted.

### 2.4 Contract and authorization model

Successful JSON uses the existing `ApiResponse<T>` envelope. Errors use RFC 9457 `ProblemDetail` with a stable application code and trace identifier. Browser access tokens remain in memory; refresh credentials use the protected cookie flow; mobile credentials use secure storage.

Authorization is enforced at the backend repository/service boundary, not only in route guards or UI visibility:

- Clients are scoped to their customer organization.
- Provider Managers, Inspectors, and Maintenance Engineers are scoped to their Provider Organization.
- Inspectors and Maintenance Engineers are additionally assignment-scoped.
- Platform Operator business permissions are distinct from Platform Admin technical permissions.
- Report release requires author-Inspector verification and Provider Manager completeness review.
- Mission clearance remains separate from Provider capability vetting.
- Approval of one Provider capability cannot verify or unlock another.

## 3. Main Flow implementation shape

### Supporting Flow

Implement organization/provider onboarding, capability selection and separate vetting, asset master data, and approved recurring schedule setup. Provider onboarding must not itself grant flight clearance, mission release, inspection eligibility, or maintenance eligibility until the relevant capability state is verified.

### MF1 — Survey Request, Quotation Sourcing & Conditional Funding

Refactor request sourcing around direct Provider selection or open RFQ. Quotations are versioned and cover Provider direct services, logistics, and applicable tax; Platform AI/data/storage costs are not separate Client quotation lines. The accepted Service Order snapshots applicable commercial policy versions and values. Funding-dependent execution is allowed only when an authorized payment-partner product supports the accepted terms; the Platform never becomes a deposit custodian.

### MF2 — Drone Mission Planning & Airspace Clearance

Add mission-plan and shot-item aggregates linked to the accepted service order. GSD, overlap, equipment, AGL, gimbal and shot items are mission/SOW-specific. Waypoint coordinates are optional when manual piloting under the approved shot plan is used. Mission-specific airspace and applicable permit checks are recorded before mission release. The Platform does not pilot the drone.

### MF3 — Drone Survey, Evidence, AI Verification & QA Report

Align inspection execution around assigned Inspectors, checklists, evidence integrity, optional AI candidates, human finding verification, and the author Inspector’s draft verification/edit confirmation. Remove any target requirement for cross/peer review from the new contract; retain historical v1 tests only as historical evidence. Provider Manager checks completeness and releases the report.

### MF4 — Report Acceptance, Settlement & Complaints

Implement the target Client accept/clarify/complaint decision path and immutable accepted report version. Settlement, hold, and release are partner-coordinated target integrations gated by accepted order terms. Platform Operator records internal Platform Terms outcomes and does not issue a legal arbitration award. No funding integration is claimed complete without a real adapter and integration evidence.

### MF5 — Defect Rectification, Maintenance & Retention

Refactor maintenance around verified defects from accepted reports, technical assessment, versioned quotation/order, assigned Maintenance Engineer, work logs, change orders, mandatory before/after evidence, Client completion decision, and optional order-snapshotted retention/warranty. Re-inspection creates a linked request returning to the documented sourcing/planning flow. Retention release earns no second Platform commission.

## 4. Repository responsibilities

### Backend repository

The backend is the source of authorization, workflow transitions, persistence, and integration contracts. It will receive the largest refactor:

- canonical role/actor-zone/provider linkage;
- Provider Organization and independent capability-vetting aggregates;
- forward migrations and persistence constraints;
- MF1–MF5 domain transitions and cross-module facades/events;
- mission-plan and shot-item persistence;
- report author-verification/completeness/release contract;
- maintenance completion/retention contract;
- partner integration ports with safe disabled/unconfigured behavior;
- scoped repositories, audit events, idempotency, optimistic locking, and Problem Details;
- full unit, integration, schema, and Modulith boundary tests.

### Frontend repository

The React application will move from the current portal/legacy role access model to document-aligned role and capability experiences:

- access policy based on six canonical roles and actor zones;
- Provider Manager onboarding/capability/evidence screens;
- Platform Operator vetting and independent status decisions;
- Client MF1 request/RFQ/order/funding, MF4 report decision/complaint, and MF5 ticket/order/acceptance screens;
- Provider Manager/Inspector MF2/MF3 mission, evidence, finding, and report workflow screens;
- maintenance evidence and retention state presentation;
- typed API services matching backend envelopes/errors;
- route guards treated as UX only, with backend authorization tested separately;
- feature-local tests for loading, empty, validation, conflict, unauthorized, and successful states.

### Mobile repository

The Flutter app will be aligned with assigned workforce workflows rather than becoming a second source of business rules:

- secure authentication/session behavior;
- Inspector assignment, mission/checklist, evidence upload, finding verification, and authored-draft verification UX;
- Maintenance Engineer assignment, assessment, work log, change request, and before/after evidence UX;
- capability/organization context only where required for assigned work;
- typed API models matching the shared response/error contracts;
- generated files regenerated from source, never hand-edited;
- Riverpod providers and repository tests for loading, retry, authorization, and upload failure paths.

### Documentation repository

Keep Report 3 and business-flow documents synchronized with actual implementation status. Update database design implementation status, API/architecture documentation, and Report 5 case index/details/statistics/cover only with real verification outcomes. Do not mark target payment/airspace/retention integrations implemented without adapter and integration evidence.

## 5. Delivery strategy

The refactor will be delivered in vertical phases, each leaving a buildable/testable baseline:

1. **Contract and baseline phase:** reconcile documents, role codes, actor zones, API envelope/errors, and repository baselines; record incompatibilities.
2. **Identity and Supporting Flow phase:** provider organizations, provider-linked users, canonical roles, capability selection, evidence metadata, independent vetting, scoped authorization.
3. **MF1/MF2 phase:** Provider eligibility gates, request/RFQ/quotation/order snapshots, mission plans, shot items, airspace/permit state, and assignment release.
4. **MF3 phase:** assigned inspection execution, evidence/telemetry, AI candidate fallback, verified findings, authored draft verification, Provider Manager release.
5. **MF4 phase:** Client decision, immutable acceptance, complaint workflow, partner integration ports, and internal Operator outcomes.
6. **MF5 phase:** maintenance assessment/order/assignment, change control, before/after evidence, completion, optional retention/warranty, and linked re-inspection.
7. **Client synchronization phase:** web and mobile vertical slices for each backend contract, with generated model and UI migration from legacy flows.
8. **Verification/documentation phase:** cross-repository contract tests, clean migration, architecture checks, frontend/mobile checks, Report 5 evidence, and final target-vs-implemented status.

Each phase uses a feature branch/worktree as appropriate, strict RED → GREEN → REFACTOR for behavioral changes, and a two-stage review: spec compliance first, code quality second. No phase is declared complete from file existence or compilation alone.

## 6. Migration and compatibility policy

- Never rewrite applied Flyway migrations. Add forward migrations with explicit constraints and rollback/backup notes where operationally relevant.
- Use a deliberate role transition for legacy values. Map old role values to canonical roles only after confirming current data and test fixtures; retain a compatibility reader only if needed for an intermediate release, then remove it in a later migration.
- Do not silently reinterpret `SERVICE_MANAGER` as `PROVIDER_MANAGER` or `PLATFORM_OPERATOR` without an explicit migration decision and authorization review.
- Preserve historical v1 workflow identifiers and Report 5 evidence while adding MF1–MF5 target identifiers.
- Preserve API clients through additive/versioned changes when a response or authorization contract is breaking. Update browser/mobile clients in the same compatible release where possible.
- Keep target-only integrations disabled until configured and verifiably tested; unsupported funding/hold/settlement paths must fail closed.
- Use data backfills that are idempotent, scoped, and auditable. Do not delete historical records to make the target schema appear clean.

## 7. Verification strategy

### Backend

- Focused red/green unit tests for each domain transition and role/capability gate.
- API integration tests for positive and negative organization/assignment scope.
- Clean-database Flyway migration and SQL contract tests.
- Persistence mapping tests for every new/changed table.
- Spring Modulith boundary verification.
- Full `./mvnw verify` before handoff.

### Frontend

- Feature tests for role visibility, capability selection, separate vetting status, workflow transitions, validation, empty/loading/error/conflict states.
- Typecheck/lint/build using the repository’s actual scripts.
- Verify that no UI-only permission is treated as security.

### Mobile

- `dart format --set-exit-if-changed .`
- `flutter analyze`
- `flutter test`
- Repository/model/provider tests for secure token use, assigned-scope enforcement, upload retry/failure, and response/error decoding.

### Cross-repository

- Contract fixtures must prove `ApiResponse<T>` and RFC 9457 error compatibility across backend, web, and mobile.
- Verify MF1→MF2→MF3→MF4→MF5 identifiers and transitions against the business-flow reference.
- Verify capability-specific provider eligibility in both inspection and maintenance paths.
- Verify all report/documentation claims against executed evidence.
- Run `git diff --check` and inspect all final diffs for unrelated work, generated files, secrets, and legacy-role drift.

## 8. Risks and decisions requiring review

1. **Legacy role migration:** current source and V3 migration use five older role values while the target documents require six canonical values. The implementation plan must include a data/fixture migration and a reviewed authorization matrix.
2. **Provider identity boundary:** `provider_organizations` exists in the target database design but not in current v1 migrations. The plan must make provider-to-user and provider-to-transaction foreign-key ownership explicit before coding.
3. **Workflow scope:** current maintenance and notifications are persistence-heavy/incremental; MF4 partner settlement and MF2 airspace/permit integrations are target capabilities. The plan must separate real implementation from target-only contracts.
4. **API compatibility:** response envelopes and role strings affect three clients. Backend and clients should move through an explicitly versioned/compatible contract, not independent silent edits.
5. **Academic evidence:** Report 5 must preserve historical WF1–WF4 test IDs and add new test coverage without claiming unexecuted target flows as passed.
6. **Repository isolation:** the docs repository currently contains the approved SRS edits, a generated `.hermes/` plan directory, and unrelated untracked slide files. Implementation must use isolated branches/worktrees and stage only intended files.

## 9. Definition of done for the design

This design is complete when the user confirms that the documents-led, multi-repository, MF1–MF5 refactor scope is correct. After written design approval, the next artifact is the detailed Superpowers implementation plan at `docs/superpowers/plans/YYYY-MM-DD-<feature-name>.md`. No source implementation begins from this design alone.
