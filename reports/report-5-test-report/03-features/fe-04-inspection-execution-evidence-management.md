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
| WF3-002 | Assigned Inspector uploads supported evidence with checksum and source traceability and records the evidence-quality decision. | Upload a valid PNG; retry the identical bytes; list and stream the evidence as the assignee and as a same-organization ORG_ADMIN; attempt upload and read as an unrelated Inspector; submit an unsupported content type and a half-supplied GPS pair; record an accepted decision with prose shot-list comparison; attempt a limited decision with no reason. | Object-store bytes and PostgreSQL metadata remain consistent; checksum/source/uploader are server-traceable; an identical re-upload returns the existing evidence rather than a duplicate; out-of-scope Inspectors are refused; unsupported content and half-supplied GPS are rejected; a limited/return decision without a stated reason is refused; the Inspector's prose survives the round trip. | An assigned inspection in `FIELD_COMPLETED` or `REPORT_DRAFT`, PostgreSQL, and an S3-compatible store (S3Mock in CI, MinIO at runtime) with a supported image available. | Passed | 2026-10-08 | Claude Code (automated) | Pending |  |  | Pending |  |  | Verified by `InspectionEvidenceApiIntegrationTest` (10 tests), which ran again on 2026-10-09 within the full backend suite of 156 passing tests. Live MinIO runtime was exercised during the earlier browser walkthrough. |
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
