# Test Cases sheet source

This table mirrors the `Test Cases` sheet. The workbook columns and order are
fixed: `No`, `Function Name`, `Sheet Name`, `Description`, `Pre-Condition`.

## Project and environment notes

| Field | Value |
| --- | --- |
| Project Name | SmartDroneInspection |
| Project Code | SEP490 — *confirm with project owner* |
| Test environment | Local/integration environment with PostgreSQL, backend API, and web client; MinIO is used for runtime/storage verification, while S3Mock 5.2.3 is used by CI S3 API integration tests. |
| Baseline | **MF3 (inspection evidence, findings, and reporting) only.** The four roles are `ADMIN`, `ORG_ADMIN`, `INSPECTOR`, `MAINTENANCE_ENGINEER`. |

## Reset scope (2026-10-09)

This report was reset to the implemented slice. The earlier content mixed two
different systems — a retired five-role WF1–WF4 baseline and the current
four-role Enterprise SaaS target — which made the totals meaningless as
evidence of the current system.

Removed, because they describe behavior that no longer exists:

- `WF1-001`–`WF1-019` and `WF2-001`–`WF2-007`: five-role asset, schedule,
  quotation, order and assignment behavior. The current roles are different;
  MF1/MF2 workflow requirements remain, but their runtime is not present in
  the current backend baseline.
- `WF3-001`: assignment acceptance and checklist execution. There is no
  `/assignments`, `/start`, or `/checklist` endpoint in the current backend.
- `WF3-004`: five-role report review, Manager release and Client acceptance.
  Publication is now an ORG_ADMIN act with no Client acceptance step.
- `WF3-007`, `WF3-008`: despite the `WF3` prefix these describe **MF4** team,
  cost and completion-report gates. They belong to FE-07 and are removed with
  the rest of the unimplemented MF4 scope.
- `WF4-001`–`WF4-005`: MF4 maintenance, triage and cost reconciliation. Not
  implemented.

Retained: `WF3-002`, `WF3-003`, `WF3-005`, `WF3-006`, which describe behavior
that exists and has an executed test behind it.

The removed IDs stay reserved and are never reused. `WF3-009` was then assigned
to the scoped collection case recorded below, so new cases continue from
`WF3-010`.

**This reset does not claim MF1, MF2 or MF4 are tested, and does not claim they
are out of scope.** Their requirements remain, but workflow services/endpoints
and executed evidence are absent from the current baseline. In the generated
workbook, Feature 2 (FE-02/MF1), Feature 3 (FE-03/MF2), and Feature 7
(FE-07/MF4) therefore have no cases. FE-01 is supporting evidence only, and
FE-08 has no assigned case. These are accurate gaps, not formatting errors.

The FE-01 supporting verification is intentionally outside the workbook case
index and functional-case statistics; its auth-flow and role-policy evidence is
recorded in `03-features/fe-01-identity-access-governance.md`.

## Case index

The `Sheet Name` column refers to the generated workbook sheet, not to an SRS
feature code. The exporter maps `Feature N` to `FE-0N`; `WFx-yyy` remains the
stable business-flow test-case ID.

| No | Function Name | Sheet Name | Description | Pre-Condition |
| ---: | --- | --- | --- | --- |
| 1 | `[WF3-002]` FE-04 — MF3 evidence and traceability | Feature 4 | Assigned Inspector uploads supported evidence with a server-computed checksum and source metadata, retry-safe persistence, and scoped read access; the Inspector records the substantive evidence-quality decision. | Assigned inspection past field work; valid image, PostgreSQL, and an S3-compatible endpoint (S3Mock in CI, MinIO at runtime). |
| 2 | `[WF3-003]` FE-05 — MF3 AI candidate and finding review | Feature 5 | Inspector reviews AI candidates or records a manual finding; pending/rejected detections stay non-official, and AI failure preserves the manual path. | Accepted evidence set; deterministic inference stub or manual fallback available. |
| 3 | `[WF3-005]` FE-06 — MF3 human verification gates | Feature 6 | Candidates and the report draft are verified by the author Inspector and approved by a qualified ORG_ADMIN before publication; a manual structured draft remains possible when drafting is unavailable. | Confirmed evidence set, an assigned Inspector, and a qualified reviewer in the same organization. |
| 4 | `[WF3-006]` FE-06 — MF3 immutable approved report | Feature 6 | The approved report version is immutable and source-traceable, and hands only repair-required findings to MF4. | Published MF3 review artifacts exist. |
| 5 | `[WF3-009]` FE-04 — MF3 scoped inspection and report collections | Feature 4 | A caller reaches MF3 through a server-paged, role-scoped list instead of a hand-entered identifier; the report review queue is the same collection filtered to inspections that carry a report. | Two organizations and fixtures for each of the four roles exist. |

## Coverage gaps

These are stated as gaps rather than filled with fabricated cases or statuses.

- **MF1 and MF2** (asset/schedule setup, readiness) remain in Report 3, but
  workflow implementation and executed test evidence are absent from the current
  baseline, so they have no case.
- **MF4** (maintenance, triage, cost reconciliation) is unimplemented, so it has
  no case.
- **FE-08** dashboard, analytics and notifications has no assigned case.
- **MF3 assignment/checklist entry** has no endpoint, so there is no case.

Mobile application verification is not recorded in this round; every case below
is evidenced by backend and web tests only.
