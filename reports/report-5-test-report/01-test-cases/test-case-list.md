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
  quotation, order and assignment behavior. The current roles are different
  and MF1/MF2 runtime does not exist.
- `WF3-001`: assignment acceptance and checklist execution. There is no
  `/assignments`, `/start`, or `/checklist` endpoint in the current backend.
- `WF3-004`: five-role report review, Manager release and Client acceptance.
  Publication is now an ORG_ADMIN act with no Client acceptance step.
- `WF3-007`, `WF3-008`: despite the `WF3` prefix these describe **MF4** team,
  cost and completion-report gates. They belong to FE-07 and are removed with
  the rest of the unimplemented MF4 scope.
- `WF4-001`–`WF4-005`: MF4 maintenance, triage and cost reconciliation. Not
  implemented.

Retained: `WF3-002`, `WF3-003`, `WF3-005`, `WF3-006`, `WF3-009`, which describe
behavior that exists and has an executed test behind it, plus `WF2-008` and
`WF2-009`, which were restored on 2026-10-10 after the MF2-07 readiness service
was re-integrated onto the current MF3 mainline and re-verified there.

The removed IDs stay reserved and are never reused. New cases continue from
`WF3-010`.

**This reset does not claim MF1, MF2 or MF4 are all tested, and does not claim
they are out of scope.** Only MF2-07 readiness approval and return have executed
evidence (`WF2-008`, `WF2-009`); the rest of MF2, all of MF1 and all of MF4 remain
unimplemented, so they have no executed evidence to record. Those areas are
recorded as an accurate coverage gap, not as a formatting error.

The FE-01 supporting verification is intentionally outside the workbook case
index and functional-case statistics; its auth-flow and role-policy evidence is
recorded in `03-features/fe-01-identity-access-governance.md`.

## Case index

The `Sheet Name` column refers to the fixed workbook sheet, not to an SRS
feature code. `FE-xx` identifies the product feature and `WFx-yyy` identifies
the business-flow test case.

| No | Function Name | Sheet Name | Description | Pre-Condition |
| ---: | --- | --- | --- | --- |
| 1 | `[WF2-008]` FE-03 — MF2-07 independent readiness approval | Feature 1 | A separate active ORG_ADMIN whose reviewer credential is internally verified and evidence-attributed approves a currently submitted preparation only when the selected Inspector credentials, reviewed Drone documents, accepted-pair chronology and permit gates all pass. Invalid scope, attribution, validity, applicability attestation or a non-overridable permit blocker leaves the decision and both statuses unchanged. | PostgreSQL fixtures provide two organizations, an assigned INSPECTOR, an independent active ORG_ADMIN reviewer, a current SUBMITTED preparation, an accepted pair under `V28`, an ACTIVE permit, ACTIVE credentials with verification and evidence attribution, and an ACTIVE reviewed Drone document. |
| 2 | `[WF2-009]` FE-03 — MF2-07 readiness return with observed-source audit | Feature 1 | A qualified independent ORG_ADMIN returns a submitted preparation with a reason even when readiness evidence is missing. The snapshot stores exactly the reviewer-observed and unresolved source IDs, records `observedSourceSetComplete=false`, and leaves the inspection `PREPARING`. | PostgreSQL fixtures provide an active ORG_ADMIN, a reviewer credential valid at decision time and a current SUBMITTED preparation. The permit or selected readiness records may be missing. |
| 3 | `[WF3-002]` FE-04 — MF3 evidence and traceability | Feature 2 | Assigned Inspector uploads supported evidence with a server-computed checksum and source metadata, retry-safe persistence, and scoped read access; the Inspector records the substantive evidence-quality decision. | Assigned inspection past field work; valid image, PostgreSQL, and an S3-compatible endpoint (S3Mock in CI, MinIO at runtime). |
| 4 | `[WF3-003]` FE-05 — MF3 AI candidate and finding review | Feature 2 | Inspector reviews AI candidates or records a manual finding; pending/rejected detections stay non-official, and AI failure preserves the manual path. | Accepted evidence set; deterministic inference stub or manual fallback available. |
| 5 | `[WF3-005]` FE-06 — MF3 human verification gates | Feature 2 | Candidates and the report draft are verified by the author Inspector and approved by a qualified ORG_ADMIN before publication; a manual structured draft remains possible when drafting is unavailable. | Confirmed evidence set, an assigned Inspector, and a qualified reviewer in the same organization. |
| 6 | `[WF3-006]` FE-06 — MF3 immutable approved report | Feature 2 | The approved report version is immutable and source-traceable, and hands only repair-required findings to MF4. | Published MF3 review artifacts exist. |
| 7 | `[WF3-009]` FE-04 — MF3 scoped inspection and report collections | Feature 2 | A caller reaches MF3 through a server-paged, role-scoped list instead of a hand-entered identifier; the report review queue is the same collection filtered to inspections that carry a report. | Two organizations and fixtures for each of the four roles exist. |

## Coverage gaps

These are stated as gaps rather than filled with fabricated cases or statuses.

- **MF1** (workspace entitlement, asset/Drone/Inspector pair setup) is
  unimplemented, so it has no case.
- **MF2 outside MF2-07** — assignment response, shot-list preparation and the
  field session — has no executed case beyond the two readiness cases above.
- **MF4** (maintenance, triage, cost reconciliation) is unimplemented, so it has
  no case.
- **FE-08** dashboard, analytics and notifications has no assigned case.
- **MF3 assignment/checklist entry** has no endpoint, so there is no case.

Mobile application verification is not recorded in this round; every case below
is evidenced by backend and web tests only.
