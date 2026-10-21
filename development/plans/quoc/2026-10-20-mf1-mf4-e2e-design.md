# MF1–MF4 Full-Flow E2E Design

**Date:** 2026-10-20  
**Status:** Design approved in conversation; awaiting review of this written spec.  
**Scope:** Complete and verify one connected Enterprise SaaS lifecycle across Backend, Frontend, Mobile and Docs, using a disposable local test environment only.  
**Execution gate:** No implementation begins until the user approves this spec and then approves a separate implementation plan.

## 1. Goal and outcome

Enable a test organization to move through the complete four-flow lifecycle without direct database state changes between steps:

```text
ORG_ADMIN creates resources + paired asset + inspection
  → Inspector accepts, prepares and records an ended field session
  → Inspector records evidence/findings and authors the inspection report
  → ORG_ADMIN reviews/publishes and records corrective work
  → ORG_ADMIN opens a work order and assigns the maintenance team
  → MAINTENANCE_ENGINEER plans/estimates/executes and reports completion
  → independent ORG_ADMIN accepts, reconciles cost and closes the order
```

The deliverable is both a working client-to-API journey and reliable automated evidence of its handoffs and refusal paths. Existing unit, widget and API integration suites remain valuable, but none alone will be presented as proof of the entire MF1–MF4 journey.

## 2. Constraints and assumptions

### Confirmed

- The authoritative workflow is Report 3 §3.3–§3.8 and `project-reference/business-flows.md` MF1–MF4.
- The selected client split is Web for `ORG_ADMIN` administration/review and Inspector report governance; Flutter for Inspector field operations and Maintenance Engineer tasks. Do not duplicate every screen across both clients.
- The E2E target is Flutter Web on Chrome, which is available locally. It verifies the Flutter UI/API contract, not Android-native camera, secure-storage, or device behavior.
- The current repositories contain uncommitted user/assistant work. Preserve it; never reset, checkout over, stage broadly, or include unrelated files.
- Existing compose has fixed `container_name` values and default ports/volumes. It must not be started/recreated as the E2E stack.
- No production system, customer credentials, customer files, or externally hosted AI service is used by the E2E.

### Technical boundaries to resolve during implementation planning

- Backend has no MF1 inspection-creation/dispatch API and no MF2 normal field-session end/`FIELD_COMPLETED` operation. MF3 gates require that completed state; this is a real transition blocker, not a fixture-seeding task.
- Mobile’s assignment inbox currently has no navigation from an assignment into its detail/session flow. Current Mobile also lacks maintenance APIs/screens; current Frontend maintenance is a static placeholder despite Backend MF4 APIs/tests.
- Current Mobile upload is not sufficient proof for all capture metadata required by Report 3. Implement only metadata that the app/platform can provide honestly; never synthesize GPS, altitude, gimbal, or actual aircraft-flight values.
- Backend `MaintenanceApiIntegrationTest` covers an API lifecycle, but the current API request surfaces do not establish all Report 3 MF4 requirements, notably automated maintenance-report drafting and explicit paired before/after evidence references. Those contracts must be inspected against Report 3 before coding.
- Database changes may be required for asset-pair snapshots, field-session completion, and maintenance evidence/report provenance. Any required schema change is a new forward-only Flyway migration, never a rewrite of an applied migration.

## 3. User journeys and ownership

### MF1 — Resource setup and dispatch (Web, ORG_ADMIN; Backend authoritative)

1. Sign in to the disposable organization workspace and create/manage Inspector and Maintenance Engineer users and applicable credentials.
2. Register a Drone, required Drone documents and permit/compliance records.
3. Create an asset and, in that same complete-asset workflow, assign exactly one active Inspector and one eligible Drone. Backend validates tenant, active workforce, Drone serviceability and uniqueness and commits the asset and default pair atomically. The existing `AssetPairAssignment` represents this asset-level default pair and remains distinct from a per-inspection assignment.
4. Create an inspection for the existing asset with objective, component scope, acceptance criteria and requested dates/cadence as applicable.
5. Backend snapshots the current Inspector/Drone pair and relevant defaults, rejects known conflicts/unavailable resources, preserves historical inspections when defaults change, records reassignment reasons, and atomically creates a new inspection-specific dispatch/assignment record. Each inspection-specific assignment has its own Inspector response and timestamp and is visible to that Inspector.

The current V28 `assignment_response`/`responded_at` fields on `asset_pair_assignments` are legacy pair-level response fields. The new MF1/MF2 dispatch contract must use a distinct per-inspection record so accepting one inspection cannot accept all future inspections attached to an asset.

**Gate:** This phase cannot be called complete until the inspection can be created and assigned through supported application/API operations; direct SQL is prohibited in the flow test.

### MF2 — Preparation, readiness and field session (Web for ORG_ADMIN review; Flutter Web for INSPECTOR)

1. Inspector opens the assigned inspection from the mobile inbox, reviews the assigned asset/Drone/scope, and accepts or rejects with the required reason.
2. Inspector creates/saves a versioned shot-list, evidence requirements, site/access limitations, proposed session time and hazards, then submits preparation with safety acknowledgement.
3. ORG_ADMIN links the actual applicable permit/credential/Drone records, reviews compliance blockers and human-verification requirements, and independently approves or returns with required evidence/reasons.
4. Inspector opens the inspection from the inbox/detail route, sees the current readiness sources/status, records the on-site pre-flight checklist and starts or postpones/aborts with reasons.
5. Inspector ends a started session through a distinct normal-end action. Backend records checklist/session outcome, actor/time and audit reference; only then may it set `FIELD_COMPLETED` and expose the next MF3 gate. Aborted and postponed sessions do not masquerade as completed.

**Gate:** Readiness becomes unusable after every defined material source change; start rechecks current readiness, assignment, entitlement, pair and validity. No UI state alone grants clearance.

### MF3 — Evidence, findings, report and disposition (Flutter Web for field evidence where appropriate; Web for findings/report/review)

1. Inspector uploads real test image files to the assigned inspection/session; Backend validates size/type/content, stores bytes in the isolated MinIO service, computes checksum and preserves source provenance.
2. Inspector records a non-empty comparison with the shot-list and an explicit evidence-quality decision. Only an accepted current evidence set unlocks eligible advisory analysis/report drafting.
3. Inspector reviews advisory candidates or creates manual findings, then explicitly confirms the findings set. AI candidates never become official findings automatically.
4. Inspector authors an AI-assisted or structured manual report, reviews source-backed content, verifies and submits it.
5. A different authorized ORG_ADMIN reviews, returns or approves the report; publication stores an immutable PDF and checksum.
6. After publication, ORG_ADMIN records a corrective outcome for each official finding and performs the MF3-13 handoff or a reasoned no-repair close.

**Gate:** No role may self-review; tenant/assignment scope remains enforced by Backend. Live external LLM/model quality is not part of this E2E; deterministic local test adapters exercise the request/response/workflow boundary while the human review gate remains real.

### MF4 — Work order through closeout (Web for ORG_ADMIN; Flutter Web for Maintenance Engineer)

1. ORG_ADMIN opens repair candidates, selects the eligible handed-off finding scope, creates one traceable work order, triages priority/dates/safety/access/acceptance criteria, and assigns team lead, members, report author and independent accepting/cost reviewer.
2. Backend checks tenant, source report/finding, duplicate scope, membership, applicable credential rules, team integrity and separation of duties.
3. Team lead creates tasks and an itemized estimate. ORG_ADMIN approves or returns/rejects the baseline before release/start.
4. Assigned Engineer records task progress, hours, materials, actual costs and attributable evidence. Required before/after evidence must be paired to the same task/finding/component; missing proof blocks completion/report submission as specified by Report 3.
5. Team submits change requests for additional scope/cost/time; only the designated approver may approve, reject or return them. Approved changes alone alter authorized budget.
6. Team lead declares physical completion only after required logs/evidence are present. Designated report author requests a report draft (local deterministic draft adapter for E2E), edits/verifies it, and submits it.
7. An independent ORG_ADMIN accepts, returns for rework, or requests re-inspection with reasons. Cost reviewer reconciles actuals/receipts against the approved baseline and changes. Work order closes only when the completion, acceptance, cost and pending-change gates pass.

**Gate:** Native maintenance report generation may use a configured provider in production, with structured manual authoring as an explicit fallback. The E2E’s deterministic adapter proves workflow integration only; it does not claim LLM quality. A requested re-inspection must not be reported as complete until the MF1 inspection-creation path exists and is linked.

## 4. Test architecture and data safety

### Disposable E2E environment

- Add a dedicated Compose definition/override or equivalent isolated launcher for E2E. It must omit fixed container names, use a distinct Compose project, named volumes and network, and non-conflicting or dynamically assigned host ports. It must not include `compose down` on the existing project or reuse the current `smartdroneinspection-*` volumes.
- Start isolated PostgreSQL and MinIO; run Backend and Web against those services. Local AI/draft adapters are deterministic and do not require external API keys or network services.
- Use browser automation for Web and Flutter Web. Check required Flutter web plugin support before choosing the concrete implementation; if a plugin cannot run on web, provide an explicit deterministic test seam for the browser flow without claiming native-device coverage.
- Add a single E2E orchestrator with readiness polling and cleanup scoped only to the unique E2E Compose project. Teardown may delete only that run’s isolated volumes after evidence/artifacts are collected.
- Create initial organization/admin identity through the approved registration/bootstrap path. Create all subsequent users, roles, resources, workflow transitions and business records through application UI/API; no direct SQL fixture/state changes in the E2E scenario.
- Test users/passwords and files are generated synthetic data in the isolated environment. Never log or commit credentials, tokens, images with personal data, or local secrets.

### Test layers

1. **TDD regression tests:** add a failing API/client test for each missing contract before implementation.
2. **Backend integration:** Testcontainers/PostgreSQL and MinIO verify persistence, migrations, state transitions, authorization, rollback and error contracts.
3. **Client tests:** Vitest component/API tests and Flutter repository/widget tests cover loading, validation, errors, retry and role-specific actions.
4. **Cross-client E2E:** one orchestrated journey executes actual browser UI requests through the versioned API and verifies downstream state through UI/read API. Capture screenshots/log summaries without credentials or sensitive payloads.
5. **Failure-path E2E:** at minimum wrong tenant/assignment, non-independent reviewer, invalid readiness, session end blocked before checklist, stale state, duplicate work-order scope, missing cost/evidence, and attempted close before acceptance/reconciliation.

## 5. Acceptance criteria

The full work is complete only when:

- The happy path completes MF1→MF4 through Web and Flutter Web, with no direct database mutation between steps.
- The inspection ID, organization, asset, pair, readiness decision, field-session outcome, evidence, report/PDF, corrective handoff, work order, team/tasks, approved estimates/changes, work logs, paired evidence, acceptance and cost reconciliation remain traceably linked.
- Invalid role, tenant, assignment, separation-of-duties, state and missing-proof actions fail with stable client-visible errors and leave no partial state.
- Reinspection and maintenance completion are not represented as complete if the MF1 link or required MF4 report/evidence capability is missing.
- Backend full verification, Frontend lint/build/test, Mobile format/analyze/test, E2E run and Docs check all pass; exact commands/results are recorded.
- Report 3 §3.2–§3.8, business flow, database/API/backend/frontend/mobile docs and Report 5 are synchronized. Report 5 uses stable existing mappings where possible, adds only valid cases after their procedures exist, updates all required source/statistics/cover/history files, and never marks unexecuted behavior Passed.
- No push, PR, merge or deploy occurs without separate authorization. Each changed repo remains an independent change/PR with explicit merge order if later requested.

## 6. Explicit non-goals and limitations

- No production/VPS execution, production credentials/data, real customer organization, or external AI/LLM call.
- No Drone piloting, arming, live telemetry, legal/issuer verification, or professional qualification inference.
- No Android-native verification in this run. Flutter Web on Chrome is the agreed Mobile E2E target; camera/secure-storage/native plugin behavior needs a later emulator or device pass.
- No claim of legal/professional inspection certification, and no fabricated evidence from synthetic images.
- No workflow case is created or marked Passed merely because the full unit/API test suite passes.

## 7. Risks and rollout order

1. Preserve existing Backend and Docs dirty working-tree changes; implementation branches must be based on current `origin/main` without discarding this work.
2. E2E isolation is a first implementation gate: prove container names, ports, network and volumes are distinct before starting the new stack.
3. Implement in dependency order: MF1 create/pair/dispatch → MF2 preparation/readiness/session end → MF3 complete handoff and reviewer/report gates → MF4 client/API evidence/report/closeout → full cross-client orchestration.
4. Use forward-only migrations if required; test clean and populated migration paths. Do not rewrite V1–V35.
5. If any stage reveals contradictory acceptance criteria, stop and reconcile with Report 3 before proceeding. A failed stage stays documented as failed/blocked; do not skip it by direct DB edits.
6. At final acceptance, retain the isolated test run’s sanitized evidence; clean up only its own containers/volumes and do not alter existing local compose data.
