# FE-04: Field Records, Evidence and Inspector Quality Decision

Report 3 §3.5 titles this feature "Field Records, Evidence and Inspector
Quality Decision". The filename retains the earlier "inspection execution /
evidence management" wording; the filename is stable, the scope is Report 3's.

## Scope baseline

Report 3 §3.5 gives FE-04 two halves: the **session-record obligations of MF2**
(MF2-09–MF2-12) and the **evidence steps of MF3** (MF3-01–MF3-04). Only the MF3
half is implemented and verified.

The `inspections` module implements the MF3 half: scoped evidence upload with a
server-computed checksum and idempotent retry, evidence listing and streaming,
the assigned Inspector's substantive evidence-quality decision that gates AI
analysis and report drafting, and the scoped inspection and report collections
that make those records reachable.

The MF2 half — field-session start/end, postponement and interruption records —
is **not** implemented: there is no `/assignments`, `/start`, or `/checklist`
endpoint, so this feature has no case for it. Manual drone piloting remains
outside the platform target.

## Feature sheet summary

Values for the `Feature 4` summary block (`A2:E8` in the workbook). The
template reads these back by formula, so an export needs them recorded here.

| Cell | Label | Value |
| --- | --- | --- |
| `B2` | Feature | MF3 inspection evidence, findings and reporting |
| `B3` | Test requirement | An authorized Inspector uploads evidence with server-computed traceability, records the evidence-quality decision, and reaches assigned MF3 work through a role-scoped list. |

`B4` (`Number of TCs`) and `B5:E8` (per-round counts) are workbook formulas
over the case rows below; do not type values into the Markdown for them.

## Current cases

| Test Case ID | Test Case Description | Test Case Procedure | Expected Results | Pre-conditions | Round 1 | Test date | Tester | Round 2 | Test date | Tester | Round 3 | Test date | Tester | Note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| WF3-002 | Assigned Inspector uploads supported evidence with checksum and source traceability and records the evidence-quality decision with its shot-list comparison. | Upload a valid PNG; retry the identical bytes; list and stream the evidence as the assignee and as a same-organization ORG_ADMIN; attempt upload and read as an unrelated Inspector; submit an unsupported content type, an empty file, an oversize file, a truncated PNG header, and non-image bytes declared as `image/png`; submit a half-supplied GPS pair; attempt every quality decision before writing a shot-list comparison; record an accepted decision with a prose shot-list comparison; attempt a limited decision with no reason; confirm the stored decision carries the comparison. | Object-store bytes and PostgreSQL metadata remain consistent; checksum/source/uploader are server-traceable; an identical re-upload returns the existing evidence rather than a duplicate; out-of-scope Inspectors are refused; unsupported content, empty, oversize and **corrupt/undecodable image** input are rejected and leave no evidence row; half-supplied GPS is rejected; **no decision is recorded without a shot-list comparison**; a limited/return decision without a stated reason is refused; the Inspector's prose and the comparison survive the round trip. | An assigned inspection in `FIELD_COMPLETED` or `REPORT_DRAFT`, PostgreSQL via Testcontainers, MinIO via shared test infrastructure, and a supported image available. | Passed | 2026-10-11 | Claude Code (automated) | Pending |  |  | Pending |  |  | Verified by `InspectionEvidenceApiIntegrationTest` (10 tests), which ran again on 2026-10-11 within the full backend suite of 362 passing tests (`./mvnw.cmd verify`, JaCoCo gate met, Modulith boundary clean). Object storage is exercised through a real MinIO container, not an in-memory store, so bucket creation and streaming put/get run on every suite. Live MinIO runtime was exercised during the earlier browser walkthrough, and again on 2026-10-11 through the end-to-end API walkthrough against the running stack. **A defect found by walking MF3 in a browser on 2026-10-12, fixed.** `EvidenceQualityDecisionRequest` has carried `shotListComparison` since the decision contract was written and the seeded fixtures filled it, but the Inspector workspace never sent one, so a decision recorded through the product stored `shot_list_comparison` null while the seeded rows on the same database stored a value. The workspace now collects the comparison, refuses to record any of the four decisions until it is written, and sends it with whichever one the Inspector reaches. Verified live on inspection `2586669b-bb13-487b-902b-10af6591cb70`: the new `ACCEPTED` row stores the comparison as `{"summary": "…"}` where the earlier UI-recorded row on the same inspection was null. Covered by frontend `InspectorWorkspace.test.tsx`, which asserts the accept action stays disabled until a comparison is written and that the limited action sends the comparison and the limitation together. The workspace also moved onto the inspection's own route — `/operations/inspections/{id}` for an Inspector, `/client/inspections/{id}` for an ORG_ADMIN — so a deep link and a row click reach the same MF3-01/02 → MF3-03 flow; previously a row click expanded a panel beneath the table while that row's `Open` button led to a read-only page offering upload and no way to decide, which is how the missing decision was found. |
| WF3-009 | A caller reaches MF3 through a server-paged, role-scoped list, and the report queue is the same collection filtered to inspections that carry a report. | List as an assigned Inspector who also belongs to an organization holding an inspection assigned to someone else; list as a same-organization ORG_ADMIN; list as an ORG_ADMIN from another organization; list as a platform ADMIN; list as a MAINTENANCE_ENGINEER; request page 1 size 2 then page 3 of 5 rows; request `pageSize=5000`; filter to inspections with a report; read a row's inline report summary. | An Inspector sees only assigned inspections and never a colleague's; an ORG_ADMIN sees their own organization only and another organization sees nothing; a platform ADMIN reads across organizations but has no write path; MAINTENANCE_ENGINEER is refused; paging reports `totalCount`/`totalPages` and the last page holds the remainder; an oversized page size is clamped to 100; `/with-reports` returns only inspections carrying a report and carries each row's `reportStatus`/`reportVersionNo`. | Two organizations with fixtures for `INSPECTOR`, `ORG_ADMIN` and platform `ADMIN`, plus a `MAINTENANCE_ENGINEER`; PostgreSQL via Testcontainers. | Passed | 2026-10-09 | Claude Code (automated) | Pending |  |  | Pending |  |  | Verified by `InspectionListApiIntegrationTest` (11 tests). The platform-ADMIN case asserts membership of both tenants rather than an absolute total, because the suite shares one container. Two test-helper defects were found and fixed during this run: creating a cross-tenant fixture inspection violated the composite `(asset_id, organization_id)` and `(inspector_id, organization_id)` foreign keys, which the helper had to satisfy. |

## Coverage boundary

`WF3-002` covers evidence intake and the Inspector's quality decision. `WF3-009`
covers discovery and scoping of the same records, and the inline report summary
that keeps the inspections and reports screens consistent.

Neither case covers the MF2 session-record obligations assigned to FE-04 by
Report 3. Session start, postponement and abort have backend runtime and tests,
but Report 5 has no case for them; session end and the `FIELD_COMPLETED` handoff
remain unimplemented. Report 3 §3.7.2 and §3.7.3 (required report content and
LLM safeguards) belong to FE-06 and are likewise not asserted by these cases;
see `fe-06-…md`.
