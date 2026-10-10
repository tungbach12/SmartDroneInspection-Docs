# Test Cases sheet source

This table mirrors the `Test Cases` sheet. The workbook columns and order are
fixed: `No`, `Function Name`, `Sheet Name`, `Description`, `Pre-Condition`.

## Project and environment notes

| Field | Value |
| --- | --- |
| Project Name | SmartDroneInspection |
| Project Code | SEP490 — *confirm with project owner* |
| Test environment | Local/integration environment with PostgreSQL, backend API, and web client; MinIO is used for runtime/storage verification, while S3Mock 5.2.3 is used by CI S3 API integration tests. |
| Baseline | **Verified MF2-07 readiness decisions and the implemented MF3 slice.** Current roles: `ADMIN`, `ORG_ADMIN`, `INSPECTOR`, `MAINTENANCE_ENGINEER`. Other MF2 steps remain partial or unimplemented as documented in FE-03. |

## Reset and reconciliation scope (2026-10-09 to 2026-10-10)

The earlier content mixed a retired five-role WF1–WF4 baseline with the current
four-role Enterprise SaaS target. The 2026-10-09 reset removed obsolete and
unimplemented cases; this 2026-10-10 reconciliation adds only the two MF2-07
readiness cases backed by the merged backend implementation and CI evidence.

Removed during the reset, because they describe behavior that no longer exists
or was never implemented:

- `WF1-001`–`WF1-019` and `WF2-001`–`WF2-007`: retired five-role asset,
  schedule, quotation, order and assignment behavior.
- `WF3-001`: retired assignment acceptance/checklist case (its former
  `/assignments`, `/start`, and `/checklist` contract does not apply to the
  current MF3 test case structure).
- `WF3-004`: five-role report review, Manager release and Client acceptance.
  Publication is now an ORG_ADMIN act with no Client acceptance step.
- `WF3-007`, `WF3-008`: despite the `WF3` prefix these describe **MF4** team,
  cost and completion-report gates, outside FE-06 and unimplemented MF4 scope.
- `WF4-001`–`WF4-005`: MF4 maintenance, triage and cost reconciliation.

Retained MF3 cases: `WF3-002`, `WF3-003`, `WF3-005`, `WF3-006`, and `WF3-009`.
The removed IDs remain reserved. New MF3 cases continue from `WF3-010`.

The 2026-10-10 merge of backend PR #64 (`84fcc16`), frontend PR #37
(`287d5a4`) and mobile PR #9 (`91092e6`) added MF2 runtime. `WF2-008` and
`WF2-009` now record MF2-07 readiness approve/return verification only; they do
not claim full MF2 completion. MF2-08 invalidation is partial and MF2-12
session-end handoff remains unimplemented. MF1 and MF4 remain gaps. FE-01
supporting verification remains outside the workbook case index and functional
case statistics; see `03-features/fe-01-identity-access-governance.md`.

## Case index

The `Sheet Name` column refers to the generated workbook sheet, not to an SRS
feature code. The exporter maps `Feature N` to `FE-0N`; `WFx-yyy` remains the
stable business-flow test-case ID.

| No | Function Name | Sheet Name | Description | Pre-Condition |
| ---: | --- | --- | --- | --- |
| 1 | `[WF2-008]` FE-03 — MF2 readiness approval | Feature 3 | An independent qualified ORG_ADMIN approves current submitted preparation only when actor, organization, source attribution, validity, pair chronology, applicability, and permit gates pass; invalid paths do not persist a decision or state transition. | PostgreSQL 17/Testcontainers, V25/V28 schema, assigned Inspector, independent active ORG_ADMIN, current submitted preparation, and persisted permit/credential/document/pair records. |
| 2 | `[WF2-009]` FE-03 — MF2 readiness return | Feature 3 | A qualified reviewer returns submitted preparation despite evidence gaps, preserving the reason and exact observed/unresolved source IDs with completeness false; invalid reviewer/scope or blank reason changes no state. | PostgreSQL 17/Testcontainers, active independent ORG_ADMIN with valid reviewer credential, and current submitted preparation. |
| 3 | `[WF3-002]` FE-04 — MF3 evidence and traceability | Feature 4 | Assigned Inspector uploads supported evidence with a server-computed checksum and source metadata, retry-safe persistence, and scoped read access; the Inspector records the substantive evidence-quality decision. | Assigned inspection past field work; valid image, PostgreSQL, and an S3-compatible endpoint (S3Mock in CI, MinIO at runtime). |
| 4 | `[WF3-003]` FE-05 — MF3 AI candidate and finding review | Feature 5 | Inspector reviews AI candidates or records a manual finding; pending/rejected detections stay non-official, and AI failure preserves the manual path. | Accepted evidence set; deterministic inference stub or manual fallback available. |
| 5 | `[WF3-005]` FE-06 — MF3 human verification gates | Feature 6 | Candidates and the report draft are verified by the author Inspector and approved by a qualified ORG_ADMIN before publication; a manual structured draft remains possible when drafting is unavailable. | Confirmed evidence set, an assigned Inspector, and a qualified reviewer in the same organization. |
| 6 | `[WF3-006]` FE-06 — MF3 immutable approved report | Feature 6 | The approved report version is immutable and source-traceable, and hands only repair-required findings to MF4. | Published MF3 review artifacts exist. |
| 7 | `[WF3-009]` FE-04 — MF3 scoped inspection and report collections | Feature 4 | A caller reaches MF3 through a server-paged, role-scoped list instead of a hand-entered identifier; the report review queue is the same collection filtered to inspections that carry a report. | Two organizations and fixtures for each of the four roles exist. |

## Coverage gaps

These are stated as gaps rather than filled with fabricated cases or statuses.

- **MF1** (asset/schedule setup) and **MF4** (maintenance, triage, cost
  reconciliation) remain unimplemented and have no cases.
- **MF2** is only partly covered: `WF2-008` and `WF2-009` test MF2-07 readiness
  approval/return. Assignment response, preparation/compliance, source-change
  invalidation, field-session start/postpone/abort and session-end handoff are not
  represented by Report 5 cases. MF2-08 invalidation is partial in runtime;
  MF2-12 session end/`FIELD_COMPLETED` remains unimplemented.
- **FE-08** dashboard, analytics and notifications has no assigned case.

The MF2-07 cases and the five MF3 cases have backend/web test evidence. The
Report 5 case index does not claim mobile app verification for these cases; mobile
checks are recorded separately in supporting statistics where run.
