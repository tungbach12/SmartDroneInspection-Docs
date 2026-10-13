# MF1-11–14 Inspection Setup and Dispatch Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Create tenant-scoped inspections from existing assets, snapshot scope and the active Inspector/Drone pair, support optional cadence with idempotent due-cycle generation, detect known schedule conflicts, record reasoned reassignment, and dispatch only after ORG_ADMIN confirmation.

**Architecture:** Implement inspection setup and dispatch in the `inspections` module; it references assets through scalar IDs and an assets-owned facade for the current pair/resource validity. Reuse V25/V26 `inspections`, `inspection_schedules`, `asset_pair_assignments`, due-cycle uniqueness, and tenant composite FKs; add forward schema only if verified tests show a gap. Keep dispatch and audit/notification writes transactional and do not implement MF2 readiness, field sessions, flight operation or evidence.

**Tech Stack:** Java 21, Spring Boot 4.1, Spring Modulith, JPA, PostgreSQL Testcontainers, MockMvc, JUnit 5, AssertJ, current shared `ApiResponse<T>`/ProblemDetail.

**Spec:** `docs/superpowers/specs/2026-10-08-mf1-organization-resources-inspection-setup-design.md`

## Dependencies

- **Predecessor Plan 1:** entitlement facade, active workforce/credentials, same-org Drone/compliance lookups.
- **Predecessor Plan 2:** atomically created asset and active `AssetPairAssignment`, including pair ID/version and same-org references.
- **Successor:** MF2 consumes a dispatched inspection handoff; this plan does not implement MF2 behavior.
- This plan is MF1-11–14 only. Supporting Flow activation, retired WF1 proposals, MF2–MF4 and marketplace behavior are excluded.

## Global Constraints

- Roles: `ADMIN`, `ORG_ADMIN`, `INSPECTOR`, `MAINTENANCE_ENGINEER` only.
- ORG_ADMIN tenant scope is derived from authenticated principal; all inspection/asset/pair queries are organization-scoped.
- Snapshot fields are immutable for a created inspection; changing the asset default never rewrites earlier inspections.
- Cadence is optional. No due-cycle scheduler request is generated when cadence is absent.
- Idempotency is `(schedule_id, due_cycle_key)` as required by V25/V26; retries must return/recognize existing inspection and not duplicate dispatch notification.
- Conflicts cover known planned intervals in the application database only; do not claim external calendar or real-world availability.
- Reassignment must record actor, reason, target, scope (inspection-only vs future asset default), version and timestamp.
- Dispatch is not readiness, permit approval, flight session, drone control or clearance.
- Never rewrite V1–V26; preserve historical Report 5 WF1 cases/outcomes.
- No push/PR/merge/deploy/Jira without explicit user authorization.

## Review Focus

1. Due-cycle retry or concurrent worker attempts same schedule/cycle → exactly one inspection and one dispatch/notification record.
2. Asset default pair changes after inspection creation → old inspection retains original pair snapshot.
3. Cross-tenant asset, pair, Inspector or Drone IDs → non-disclosing rejection before writes.
4. Two overlapping active inspection intervals for same Inspector or Drone → block confirmation/dispatch with conflict IDs; no silent override.
5. Reassignment races with dispatch or another reassignment → stale version returns 409; no mixed pair snapshot or duplicate dispatch.

---

## File Structure

```text
backend/src/main/java/com/smartdroneinspection/inspections/
  api/InspectionSetupController.java              (new; MF1 create/list/detail/confirm/reassign/dispatch)
  api/dto/request/CreateInspectionRequest.java    (new)
  api/dto/request/ConfirmInspectionRequest.java   (new)
  api/dto/request/ReassignInspectionRequest.java  (new)
  api/dto/response/InspectionSetupResponse.java   (new; snapshot fields, status/version)
  domain/Inspection.java                          (new mapping/aggregate over V25/V26 inspection columns)
  domain/InspectionSchedule.java                  (new inspections-owned mapping if table ownership confirmed in Task 1)
  repository/InspectionRepository.java            (new tenant-scoped, conflict/idempotency queries)
  repository/InspectionScheduleRepository.java    (new if schedule owner is inspections)
  service/InspectionSetupService.java              (new transactional MF1 use cases)
  spi/AssetPairLookup.java                          (new only as a real assets→inspections module boundary)
  events/InspectionDispatched.java                 (new only if an existing notification/event contract consumes it)
backend/src/main/java/com/smartdroneinspection/assets/
  facade/AssetPairAccess.java                       (only if Plan 2 did not already expose a root/named-interface facade)
backend/src/test/java/com/smartdroneinspection/inspections/
  InspectionSetupApiIntegrationTest.java           (new)
  InspectionScheduleIdempotencyTest.java            (new)
  InspectionConflictIntegrationTest.java             (new)
  InspectionReassignmentTest.java                    (new)
  InspectionDispatchTest.java                        (new)
backend/src/test/java/com/smartdroneinspection/assets/
  AssetPairAccessTest.java                          (only if facade added)
docs/reports/report-5-test-report/
  01-test-cases/test-case-list.md                  (new MF1 target cases)
  03-features/fe-02-asset-registry-inspection-schedule.md
  02-test-statistics/test-statistics.md
  00-cover/cover.md
  00-cover/record-of-changes.md
```

## Task 1: Lock module ownership and exact schema contracts

**Files:** read V25/V26, existing assets facade/entity contracts from Plan 2, `Inspection` columns and Hibernate naming; modify no schema unless tests prove required columns/indexes absent.

**Interfaces:**
- Consumes: Plan 2 pair result (`assetId`, `organizationId`, `assignmentId`, `inspectorId`, `droneId`, active state, row version), Plan 1 entitlement/eligibility facades.
- Produces: inspection setup contract `CreateInspectionRequest(objective, scope, componentScope, acceptanceCriteria, plannedStartAt, plannedEndAt, cadenceUnit?, cadenceInterval?)`; response contains `inspectionId`, `organizationId`, `assetId`, pair snapshot, status, version, optional schedule/due-cycle data.

- [ ] Step 1: Verify schema has all required columns and exact FK/index names in V25/V26; confirm `inspection_schedules` owner with the agreed module map.
- [ ] Step 2: Confirm assets exposes pair/resource reads without importing its controllers/repositories/entities. If not, add only the assets-owned facade contract in Plan 2 before continuing.
- [ ] Step 3: Record concrete task interface signatures before test implementation; no guessed cross-module types.

**Verification:** source/schema inspection and existing `RuntimePersistenceInventoryTest`; no product edits in this task.

## Task 2: Inspection creation and immutable pair/scope snapshot

**Files:** `InspectionSetupController`, request/response, `Inspection`, `InspectionRepository`, `InspectionSetupService`, `InspectionSetupApiIntegrationTest`.

**Interfaces:** consumes Task 1 contracts; produces tenant-scoped draft inspection creation.

- [ ] Step 1: Add `InspectionSetupApiIntegrationTest` cases for valid same-org create, missing/foreign asset and pair, body tenant-ID forgery, immutable pair/scope snapshot after asset-default change, and inactive asset/pair or denied entitlement.
- [ ] Step 2: Run `./mvnw -Dtest=InspectionSetupApiIntegrationTest test`; observe expected RED because the API/aggregate is absent.
- [ ] Step 3: Implement scoped service: authorize ORG_ADMIN and entitlement, resolve active asset/pair through facade, validate scope/dates, persist Inspection with snapshot in one transaction.
- [ ] Step 4: Run focused tests and JPA schema validation.
- [ ] Step 5: Commit `feat(inspections): create tenant-scoped MF1 inspection snapshots`.

## Task 3: Optional cadence and due-cycle idempotency

**Files:** schedule mapping/repository only if assigned to inspections; schedule API/use case as needed; `InspectionScheduleIdempotencyTest`.

**Interfaces:** consumes Task 2 inspection aggregate and V26 unique `(schedule_id, due_cycle_key)` index; produces one inspection for each due cycle, without reviving schedule proposals.

- [ ] Step 1: Add `InspectionScheduleIdempotencyTest` cases for no cadence/no generated inspection; valid cadence; repeated `(schedule_id,due_cycle_key)` produces one inspection; different due-cycle keys produce distinct inspections; concurrent duplicate processors leave one row.
- [ ] Step 2: Run `./mvnw -Dtest=InspectionScheduleIdempotencyTest test`; observe expected RED on missing idempotent processor.
- [ ] Step 3: Implement due processing with database uniqueness as the final concurrency guard; handle duplicate-key race by loading and returning the existing inspection within a safe transaction boundary.
- [ ] Step 4: Test concurrent/duplicate processing against PostgreSQL Testcontainers and rerun focused tests.
- [ ] Step 5: Commit `feat(inspections): add idempotent MF1 cadence processing`.

## Task 4: Known schedule conflict detection

**Files:** conflict repository query/DTO and `InspectionConflictIntegrationTest`.

**Interfaces:** consumes planned inspection intervals and active assignment snapshot; produces a typed list of conflicting inspection IDs/times for the same Inspector or Drone in the same organization.

- [ ] Step 1: Add `InspectionConflictIntegrationTest` fixtures for same-Inspector overlap, same-Drone overlap, half-open boundary non-overlap, cancelled/completed exclusions, and foreign-organization records not appearing in conflict details.
- [ ] Step 2: Run `./mvnw -Dtest=InspectionConflictIntegrationTest test`; observe expected RED.
- [ ] Step 3: Implement organization-scoped interval query using half-open intervals `[start,end)` and exclude terminal/cancelled records per status contract; return no external-calendar claim.
- [ ] Step 4: Run query tests and ensure conflict details expose only same-tenant records.
- [ ] Step 5: Commit `feat(inspections): detect MF1 assignment conflicts`.

## Task 5: Confirm and reasoned reassignment

**Files:** confirm/reassign request DTOs, domain transition methods, service, repository lock/version query, `InspectionReassignmentTest`.

**Interfaces:** consumes conflict query and Plan 2 pair lookup; produces versioned assignment snapshot plus actor/reason/scope history.

- [ ] Step 1: Add `InspectionReassignmentTest` cases for ORG_ADMIN confirmation, unresolved conflict denial, same-org active replacement with mandatory reason, inspection-only reassignment preserving future default, future-default reassignment preserving old snapshots, and stale row version returning 409.
- [ ] Step 2: Run `./mvnw -Dtest=InspectionReassignmentTest test`; observe expected RED.
- [ ] Step 3: Implement state transitions under transaction/optimistic locking; validate new pair active, same tenant, Inspector role and Drone serviceability; require non-blank reason for reassignment.
- [ ] Step 4: Run focused API and persistence tests.
- [ ] Step 5: Commit `feat(inspections): confirm and reassign MF1 inspections`.

## Task 6: Dispatch, audit and notification

**Files:** dispatch endpoint/use case, `InspectionDispatched` only if an existing event/notification contract needs it, notification repository/service usage, `InspectionDispatchTest`.

**Interfaces:** consumes confirmed versioned inspection snapshot; produces persisted dispatched status, audit attribution and one in-app notification for assigned Inspector.

- [ ] Step 1: Add `InspectionDispatchTest` cases for dispatch requiring confirmation; inactive user/Drone, stale snapshot, unresolved conflict and denied entitlement; duplicate dispatch producing one state change/audit/notification; cross-tenant dispatch denied.
- [ ] Step 2: Run `./mvnw -Dtest=InspectionDispatchTest test`; observe expected RED.
- [ ] Step 3: Implement transactional dispatch with named actor/time and current assignment version; use existing notification pattern. Do not add a new queue/event bus. If notification is represented by an existing Modulith event, publish after commit using established infrastructure.
- [ ] Step 4: Run dispatch tests and verify MF2 receives only the intended inspection/asset/scope/date/Inspector/Drone/document references.
- [ ] Step 5: Commit `feat(inspections): dispatch confirmed MF1 inspection`.

## Task 7: Documentation, Report 5 and full verification

**Files:** Report 3 FE-02/FE-03 boundary if affected; business-flows MF1-11–14 only if implementation clarifies contract; database-design implementation status; backend flow/API docs; Report 5 new target case index/details/statistics/cover/change history.

- [ ] Step 1: Add new stable MF1 test cases; never rename/reuse historical WF1 case IDs. Map FE and fixed workbook sheet according to Report 5 mapping rules.
- [ ] Step 2: Record only executed test evidence; keep all unrun cases `Pending`.
- [ ] Step 3: Recount statistics and update cover/version/change history.
- [ ] Step 4: Run focused inspection tests, `./mvnw spotless:check`, `./mvnw verify`, and `git diff --check`; review links and ensure docs state runtime vs schema-only accurately.
- [ ] Step 5: Commit docs separately from backend; no push/PR.

## Final Verification

```powershell
cd D:\CTP\SmartDroneInspection-Backend
.\mvnw.cmd spotless:check
.\mvnw.cmd verify
cd D:\CTP\SmartDroneInspection-Docs
git diff --check
```

No frontend/mobile code is included unless a later approved plan explicitly changes a web API consumer.
