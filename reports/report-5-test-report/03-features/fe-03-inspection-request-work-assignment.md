# FE-03: Mission Preparation, Assignment Response and Readiness — MF2

Report 3 §3.4 titles this feature "Mission Preparation, Assignment Response
and Readiness". The filename retains the earlier "inspection request / work
assignment" wording; the filename is stable, the scope is Report 3's.

## Scope baseline

MF2 **receives** the assignment created in MF1; it does not create one. Per
Report 3 §3.4, MF2 does not source a Provider, does not calculate recommended
GSD, overlap, gimbal or flight-control settings, and has no procurement/RFQ
step. Hardware configuration is outside its scope.

The twelve MF2 steps divide into two halves:

| Steps | Actor | What it does |
| --- | --- | --- |
| MF2-01 – MF2-08 | `INSPECTOR` + `ORG_ADMIN` | Assignment accept/reject with a reason; component shot-list and required evidence types; permit/credential linking; blocker validation; safety acknowledgments; qualified ORG_ADMIN readiness approval producing `READY_FOR_FLIGHT`; snapshot of the approved plan. Implementation is partial across this range: MF2-08 source-change invalidation is not produced. |
| MF2-09 – MF2-12 | `INSPECTOR` + `SYSTEM` | Pre-flight checklist, Start request or postponement/interruption, recheck of entitlement and readiness version, `IN_PROGRESS` recording, session end, and `FIELD_COMPLETED`. Session end and `FIELD_COMPLETED` are not implemented. |

Gates worth stating because they are easy to misread as satisfied:

- Accepting an assignment **does not** establish readiness (MF2-02). Only the
  ORG_ADMIN approval at MF2-07 produces `READY_FOR_FLIGHT`, and only when all
  applicable mandatory conditions pass.
- A missing permit **cannot be waived by an internal approval** (MF2-04).
- Ambiguous authority or geographic conditions require **human verification, not
  inferred automatic clearance** (MF2-05).
- Start does **not** arm the aircraft or establish actual flight time from
  hardware (MF2-10). A Start action never arms or pilots a Drone.
- `FIELD_COMPLETED` marks one ended session, **not** overall inspection
  completion or report approval (MF2-12).

An earlier draft of this file described a request being "reviewed and confirmed
into a service order", which came from the retired five-role marketplace
baseline. Report 3 §3.4 has no service order, quotation or procurement step,
so that text was removed rather than kept as historical context.

## Feature sheet summary

Values for the `Feature 3` summary block (`A2:E8` in the workbook).
The template reads these back by formula, so an export needs them
recorded here.

| Cell | Label | Value |
| --- | --- | --- |
| `B2` | Feature | Mission Preparation, Assignment Response and Readiness — MF2 |
| `B3` | Test requirement | Verify assignment response and MF2 preparation/readiness gates, including organization scope, independent review, validity, source attribution, permit blockers, reasoned return and observed/unresolved source snapshots. |

## MF2-07 readiness cases

| Test Case ID | Test Case Description | Test Case Procedure | Expected Results | Pre-conditions | Round 1 | Test date | Tester | Round 2 | Test date | Tester | Round 3 | Test date | Tester | Note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| WF2-008 | Independent qualified ORG_ADMIN approves a current submitted preparation only when source ownership, verification, validity, pair chronology, applicability attestation and permit gates pass. | Seed two organizations, an assigned Inspector, an independent ORG_ADMIN, ACTIVE reviewer/Inspector credentials with verification and evidence attribution, an ACTIVE reviewed Drone document, an ACTIVE accepted pair responded before planned start, an applicable ACTIVE permit, a PREPARING inspection and current SUBMITTED preparation. Call the readiness approval service; repeat with same-person reviewer, wrong role, inactive/cross-tenant reviewer, foreign credential, null credential dates, missing credential evidence, unreviewed document, missing applicability basis, missing permit, late pair response and READY_FOR_FLIGHT inspection. | Valid approval persists one APPROVED decision with permit/credential/document snapshots, source IDs, reviewer and lowercase SHA-256 hash; preparation becomes READY and inspection becomes READY_FOR_FLIGHT. Every invalid actor/source/gate returns a stable business failure and creates no decision or state transition. Reviewer/document/credential checks are internal-record validation only, not external authority verification. | PostgreSQL 17/Testcontainers; V25/V28 schema; active organization, assigned Inspector, independent active ORG_ADMIN, current submitted preparation, real permit/credential/document/pair rows. | Passed | 2026-10-09 | Claude Code automated | Pending |  |  | Pending |  |  | `InspectionReadinessServiceTest` (16 tests) and `ReadinessSnapshotFactoryTest` (6 tests) are included in backend PR #64 CI on 2026-10-10. The merged backend CI ran `./mvnw.cmd verify`: 334 tests, 0 failures/errors/skips; JaCoCo and Modulith checks passed. The local Windows `mvnw.cmd -o verify` attempt could not initialize Testcontainers because Docker was unavailable; this is an environment limitation, not a product test result. Negative cases include wrong role/tenant/owner, inactive reviewer, missing evidence/date validity, permit blocker, non-current state and pair response at planned start. Internal record validation is not issuer-registry verification. |
| WF2-009 | Qualified reviewer can return a submitted preparation despite readiness-evidence gaps, with exact observed/unresolved IDs recorded as incomplete. | With a current submitted preparation and reviewer credential valid at decision time, remove the permit and supply reviewer-observed Inspector-credential/Drone-document IDs including one unresolved ID; return with a reason. Repeat with empty observed IDs and with a blank reason. | Return persists a RETURNED decision/reason and observed snapshots, retains exact requested IDs and unresolved IDs, sets `observedSourceSetComplete=false` even for empty selections, marks preparation RETURNED and leaves inspection PREPARING. Blank reason or invalid reviewer/scope creates no decision or state change. | PostgreSQL 17/Testcontainers; active independent ORG_ADMIN and reviewer credential verified/evidence-attributed with non-null dates covering decision time; current submitted preparation. | Passed | 2026-10-09 | Claude Code automated | Pending |  |  | Pending |  |  | `InspectionReadinessServiceTest` (16 tests) and `ReadinessSnapshotFactoryTest` (6 tests), included in backend PR #64 CI on 2026-10-10. The same integrated CI run passed the full backend suite (334 tests) and coverage/Modulith gates; the local test attempt was blocked because Docker was unavailable. The case covers return with a missing permit, exact observed/unresolved IDs with completeness false, and blank reason writes no decision. |

## Implemented and unverified boundaries

Backend MF2-01/02 assignment response, MF2-03/06 preparation and compliance, MF2-07 approval/return, and MF2-09/11 field-session start/postpone/abort are implemented on the current `main` baseline. The web client supplies assignment, preparation and readiness-review panels; mobile supplies assignment inbox and field-session screens.

MF2-08 invalidation is partial: session start requires the newest readiness decision to be `APPROVED`; `INVALIDATED` exists as a decision type, but no source-change workflow appends it. MF2-12 session end and the `FIELD_COMPLETED` handoff remain unimplemented. These gaps are not covered by WF2-008/009. Field-session behavior has backend service/API tests but no Report 5 case yet.

The two cases verify readiness decision behavior. `InspectionReadinessApiIntegrationTest` adds HTTP coverage for approval/return scope and failure paths; it ran in the successful backend PR #64 CI suite. These results do not cover MF2-08 source-change invalidation or MF2-12 session end/`FIELD_COMPLETED`. They also say nothing about MF1 or MF4.
