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
| MF2-01 – MF2-08 | `INSPECTOR` + `ORG_ADMIN` | Assignment accept/reject with a reason; component shot-list and required evidence types; permit/credential linking; blocker validation; safety acknowledgments; qualified ORG_ADMIN readiness approval producing `READY_FOR_FLIGHT`; snapshot of the approved plan. |
| MF2-09 – MF2-12 | `INSPECTOR` + `SYSTEM` | Pre-flight checklist, Start request or postponement/interruption, recheck of entitlement and readiness version, `IN_PROGRESS` recording, session end, and `FIELD_COMPLETED`. |

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

Values for the `Feature 1` summary block (`A2:E8` in the workbook). Even though
this sheet carries no cases, `Test Statistics!C11` still reads `Feature 1!B2`,
so it must not be left as the template's `<Feature Name1>` placeholder.

| Cell | Label | Value |
| --- | --- | --- |
| `B2` | Feature | MF1/MF2 (not implemented) |
| `B3` | Test requirement | Catalog creation, assignment response and readiness approval — no runtime, no case. |

## Current test coverage

No workbook test case is mapped to FE-03 in this report. **All twelve MF2 steps
are unverified.**

The former `WF1-017`–`WF1-019` and `WF2-001`–`WF2-007` cases were removed on
2026-10-09. The `WF1`/`WF2` rows described the retired five-role baseline
(periodic request generation, Service Manager review, Client quotation and
order approval); the `WF2-005`–`WF2-007` rows described a target design that has
never been implemented. Neither is evidence for the current system.

**MF1 and MF2 have no workflow runtime in the current backend.** An
`InspectionOrder` planning class was delivered on 6 October 2026 under a
supporting-code branch and is recorded in Report 3's change log; Report 3 §3.1
subsequently superseded that as reset scope, so it is not counted as MF2
implementation here. There is therefore no workflow runtime to test and no
executed evidence to record. This is an explicit coverage gap, not a claim that
the requirements were dropped: MF1 and MF2 remain required by Report 3 and are
awaiting implementation.

### Steps that would be covered first

If MF2 is implemented, these steps carry the highest verification value because
each encodes a gate that protects an authorization or safety decision rather
than a screen transition:

| Step | Gate to verify |
| --- | --- |
| MF2-02 | Only the assigned Inspector may respond to an assignment. |
| MF2-04 | A missing permit cannot be waived by an internal approval. |
| MF2-07 | `READY_FOR_FLIGHT` requires the qualified ORG_ADMIN, and only when all mandatory conditions pass. |
| MF2-10 | Stale, expired or revoked readiness is rejected at Start. |
| MF2-12 | `FIELD_COMPLETED` is per session; earlier sessions are preserved. |

### Effect on FE-04

Report 3 §3.5 assigns FE-04 the MF2 session-record obligations (MF2-09–MF2-12)
alongside MF3-01–MF3-04, so those four steps are owned by FE-04 rather than here.
There is no `/assignments`, `/start`, or `/checklist` endpoint, so that half is
unverified too, and MF3 has no verified entry path other than the scoped
inspection list recorded as `WF3-009`.

The removed case IDs stay reserved and are never reused.
