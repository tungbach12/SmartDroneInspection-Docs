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

Values for the `Feature 3` summary block (`A2:E8` in the workbook).
The template reads these back by formula, so an export needs them
recorded here.

| Cell | Label | Value |
| --- | --- | --- |
| `B2` | Feature | Mission Preparation, Assignment Response and Readiness — MF2 |
| `B3` | Test requirement | MF2 assignment, preparation, readiness and field-session requirements; no workflow endpoints or executed test cases are present in the current backend baseline. |

## Current test coverage

No workbook test case is currently mapped to FE-03. **All twelve MF2 steps are unverified.**

The current backend contains MF2 storage schema, including `inspection_preparations` and `inspection_readiness_decisions`, but the migration documents those tables as storage-only; schema presence is not workflow implementation or test evidence. The readiness, assignment-response, preparation and field-session services and API tests referenced by the merged docs change are not present in backend `main` at `d385a7d`. Therefore `WF2-008` and `WF2-009` are not restored as passed cases, and their IDs remain reserved rather than reused.

The existing MF2 requirements remain valid in Report 3; this status describes implementation and test evidence only. MF1 and MF2 have no workflow runtime in the current backend baseline, so they remain coverage gaps, not dropped requirements.
