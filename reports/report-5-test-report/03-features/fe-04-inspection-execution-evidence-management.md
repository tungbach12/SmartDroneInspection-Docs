# FE-04: Inspection Execution and Evidence Management

## Scope baseline

The `inspections` module implements the MF3 evidence slice of FE-04: scoped
evidence upload with a server-computed checksum and idempotent retry, evidence
listing and streaming, the assigned Inspector's substantive evidence-quality
decision that gates AI analysis and report drafting, and the scoped inspection
and report collections that make those records reachable.

MF2 assignment acceptance and checklist execution are **not** implemented — there
is no `/assignments`, `/start`, or `/checklist` endpoint — so this feature has no
case for them. Manual drone piloting remains outside the platform target.

## Current cases

| Test Case ID | Test Case Description | Test Case Procedure | Expected Results | Pre-conditions | Round 1 | Test date | Tester | Round 2 | Test date | Tester | Round 3 | Test date | Tester | Note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| WF3-002 | Assigned Inspector uploads supported evidence with checksum and source traceability and records the evidence-quality decision. | Upload a valid PNG; retry the identical bytes; list and stream the evidence as the assignee and as a same-organization ORG_ADMIN; attempt upload and read as an unrelated Inspector; submit an unsupported content type and a half-supplied GPS pair; record an accepted decision with prose shot-list comparison; attempt a limited decision with no reason. | Object-store bytes and PostgreSQL metadata remain consistent; checksum/source/uploader are server-traceable; an identical re-upload returns the existing evidence rather than a duplicate; out-of-scope Inspectors are refused; unsupported content and half-supplied GPS are rejected; a limited/return decision without a stated reason is refused; the Inspector's prose survives the round trip. | An assigned inspection in `FIELD_COMPLETED` or `REPORT_DRAFT`, PostgreSQL, and an S3-compatible store (S3Mock in CI, MinIO at runtime) with a supported image available. | Passed | 2026-10-08 | Claude Code (automated) | Pending |  |  | Pending |  |  | Verified by `InspectionEvidenceApiIntegrationTest` (10 tests), which ran again on 2026-10-09 within the full backend suite of 156 passing tests. Live MinIO runtime was exercised during the earlier browser walkthrough. |
| WF3-009 | A caller reaches MF3 through a server-paged, role-scoped list, and the report queue is the same collection filtered to inspections that carry a report. | List as an assigned Inspector who also belongs to an organization holding an inspection assigned to someone else; list as a same-organization ORG_ADMIN; list as an ORG_ADMIN from another organization; list as a platform ADMIN; list as a MAINTENANCE_ENGINEER; request page 1 size 2 then page 3 of 5 rows; request `pageSize=5000`; filter to inspections with a report; read a row's inline report summary. | An Inspector sees only assigned inspections and never a colleague's; an ORG_ADMIN sees their own organization only and another organization sees nothing; a platform ADMIN reads across organizations but has no write path; MAINTENANCE_ENGINEER is refused; paging reports `totalCount`/`totalPages` and the last page holds the remainder; an oversized page size is clamped to 100; `/with-reports` returns only inspections carrying a report and carries each row's `reportStatus`/`reportVersionNo`. | Two organizations with fixtures for `INSPECTOR`, `ORG_ADMIN` and platform `ADMIN`, plus a `MAINTENANCE_ENGINEER`; PostgreSQL via Testcontainers. | Passed | 2026-10-09 | Claude Code (automated) | Pending |  |  | Pending |  |  | Verified by `InspectionListApiIntegrationTest` (11 tests). The platform-ADMIN case asserts membership of both tenants rather than an absolute total, because the suite shares one container. Two test-helper defects were found and fixed during this run: creating a cross-tenant fixture inspection violated the composite `(asset_id, organization_id)` and `(inspector_id, organization_id)` foreign keys, which the helper had to satisfy. |

## Coverage boundary

`WF3-002` covers evidence intake and the Inspector's quality decision. `WF3-009`
covers discovery and scoping of the same records, and the inline report summary
that keeps the inspections and reports screens consistent. Neither case covers
MF2 assignment/checklist entry, which has no runtime.
