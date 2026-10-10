# FE-03: Inspection Request and Work Assignment

## Scope baseline

Inspection requests are raised against an organization's assets, reviewed and
confirmed into a service order, and an Inspector is assigned to carry out the
work. This is MF1/MF2 upstream of MF3.

## Current test coverage

Two workbook test cases are mapped to FE-03, both on the `Feature 1` sheet:
`WF2-008` and `WF2-009`, covering the MF2-07 readiness decision. They were
removed on 2026-10-09 as part of a reset that assumed MF2 had no runtime, then
restored on 2026-10-10 after the readiness service was re-integrated onto the
current `origin/main` (`d385a7d`) and re-verified there.

The remaining former `WF1`/`WF2` rows stay removed. The `WF1-011`–`WF1-019` rows
described the retired five-role baseline (periodic request generation, Service
Manager review, Client quotation and order approval); the `WF2-005`–`WF2-007`
rows described target designs that still have no implementation. Removed case
IDs stay reserved and are never reused.

**MF1, MF4 and MF2 outside MF2-07 remain unimplemented**, so there is no
runtime to test and no executed evidence to record for them. This is an explicit
coverage gap, not a claim that the requirements were dropped: they remain
required by Report 3 and are awaiting implementation.

This gap also constrains FE-04: there is no `/assignments`, `/start`, or
`/checklist` endpoint, so MF3 has no verified entry path other than the scoped
inspection list recorded as `WF3-009`.

## MF2-07 readiness cases

| Test Case ID | Test Case Description | Test Case Procedure | Expected Results | Pre-conditions | Round 1 | Test date | Tester | Round 2 | Test date | Tester | Round 3 | Test date | Tester | Note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| WF2-008 | Independent qualified ORG_ADMIN approves a current submitted preparation only when source ownership, verification, validity, pair chronology, applicability attestation and permit gates pass. | Seed two organizations, assigned Inspector, independent ORG_ADMIN, ACTIVE reviewer/Inspector credentials with verification and evidence attribution, an ACTIVE reviewed Drone document, an ACTIVE accepted pair responded before planned start, applicable ACTIVE permit, PREPARING inspection and current SUBMITTED preparation. Call the readiness approval service; repeat with same-person reviewer, wrong role, inactive/cross-tenant reviewer, foreign credential, null credential dates, missing credential evidence, unreviewed document, missing applicability basis, missing permit, late pair response and READY_FOR_FLIGHT inspection. | Valid approval persists one APPROVED decision with permit/credential/document snapshots, source IDs, reviewer and lowercase SHA-256 hash; preparation becomes READY and inspection becomes READY_FOR_FLIGHT. Every invalid actor/source/gate returns a stable business failure and creates no decision or state transition. Reviewer/document/credential checks are internal-record validation only, not external authority verification. | PostgreSQL 17/Testcontainers; V25/V28 schema; active organization, assigned Inspector, independent active ORG_ADMIN, current submitted preparation, real permit/credential/document/pair rows. | Passed | 2026-10-09 | Claude Code automated | Pending |  |  | Pending |  |  | `InspectionReadinessServiceTest` passed all 16 cases and `ReadinessSnapshotFactoryTest` passed 6 cases; re-verified on the integrated mainline branch on 2026-10-10 with `./mvnw.cmd clean verify` passing 293 tests, the JaCoCo gate and Modulith checks. Negative paths included wrong role/tenant/owner, inactive reviewer, missing evidence/date validity, permit blocker, non-current state and pair response at planned start. Internal record validation is not issuer-registry verification. |
| WF2-009 | Qualified reviewer can return a submitted preparation despite readiness-evidence gaps, with exact observed/unresolved IDs recorded as incomplete. | With a current submitted preparation and reviewer credential valid at decision time, remove the permit and supply reviewer-observed Inspector-credential/Drone-document IDs including one unresolved ID; return with a reason. Repeat with empty observed IDs and with a blank reason. | Return persists a RETURNED decision/reason and observed snapshots, retains exact requested IDs and unresolved IDs, sets `observedSourceSetComplete=false` even for empty selections, marks preparation RETURNED and leaves inspection PREPARING. Blank reason or invalid reviewer/scope creates no decision or state change. | PostgreSQL 17/Testcontainers; active independent ORG_ADMIN and reviewer credential verified/evidence-attributed with non-null dates covering decision time; current submitted preparation. | Passed | 2026-10-09 | Claude Code automated | Pending |  |  | Pending |  |  | `InspectionReadinessServiceTest` passed all 16 cases and `ReadinessSnapshotFactoryTest` passed 6 cases; same integrated run as WF2-008. Verified missing permit does not block return, observed/unresolved IDs are recorded with completeness false, and blank reason writes no decision. |

## Coverage boundary

These two cases verify the MF2-07 readiness decision only. They do not verify
the readiness HTTP API, material-change invalidation, or MF2-09/MF2-10 field
session start and postponement, none of which has an implemented contract yet.
They also say nothing about MF1 asset/pair setup or MF4.
