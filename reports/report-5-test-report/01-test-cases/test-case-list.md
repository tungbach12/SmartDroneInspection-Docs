# Test Cases sheet source

This table mirrors the `Test Cases` sheet. The workbook columns and order are
fixed: `No`, `Function Name`, `Sheet Name`, `Description`, `Pre-Condition`.

## Project and environment notes

| Field | Value |
| --- | --- |
| Project Name | SmartDroneInspection |
| Project Code | SEP490 — *confirm with project owner* |
| Test environment | Local/integration environment with PostgreSQL, backend API, and web client; MinIO is used for runtime/storage verification, while S3Mock 5.2.3 is used by CI S3 API integration tests. |
| Baseline | **Executed backend scope: MF3 plus the implemented MF4 backend slice.** The four roles are `ADMIN`, `ORG_ADMIN`, `INSPECTOR`, `MAINTENANCE_ENGINEER`. MF4 skill matching, notification delivery, MF1 re-inspection dispatch, and web/mobile clients remain unverified. |

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
- `WF4-001`–`WF4-005`: prior MF4 cases were removed on 2026-10-09. These IDs
  remain reserved and are never reused; the new backend-slice cases continue at
  `WF3-010`.

Retained at reset: `WF3-002`, `WF3-003`, `WF3-005`, `WF3-006`. Added after reset:
`WF3-009` for scoped inspection/report collections, and `WF3-010`–`WF3-012` for
the independently tested MF4 backend slice. See FE-07 for exact test procedures
and limitations.

The removed IDs stay reserved and are never reused. After `WF3-009`, the new
selected cases continue with `WF3-010`–`WF3-012`.

**The 2026-10-09 reset did not claim MF1, MF2 or MF4 were tested or out of
scope.** The 2026-10-10 addition records only the selected MF4 backend cases
listed below; it does not claim the whole MF4 target is implemented. The
`Feature 1` sheet remains empty because MF1/MF2 have no executed cases; that is
an accurate gap, not a formatting error.

The FE-01 supporting verification is intentionally outside the workbook case
index and functional-case statistics; its auth-flow and role-policy evidence is
recorded in `03-features/fe-01-identity-access-governance.md`.

## Case index

The `Sheet Name` column refers to the fixed workbook sheet, not to an SRS
feature code. `FE-xx` identifies the product feature and `WFx-yyy` identifies
the business-flow test case.

| No | Function Name | Sheet Name | Description | Pre-Condition |
| ---: | --- | --- | --- | --- |
| 1 | `[WF3-002]` FE-04 — MF3 evidence and traceability | Feature 2 | Assigned Inspector uploads supported evidence with a server-computed checksum and source metadata, retry-safe persistence, and scoped read access; the Inspector records the substantive evidence-quality decision. | Assigned inspection past field work; valid image, PostgreSQL, and an S3-compatible endpoint (S3Mock in CI, MinIO at runtime). |
| 2 | `[WF3-003]` FE-05 — MF3 AI candidate and finding review | Feature 2 | Inspector reviews AI candidates or records a manual finding; pending/rejected detections stay non-official, and AI failure preserves the manual path. | Accepted evidence set; deterministic inference stub or manual fallback available. |
| 3 | `[WF3-005]` FE-06 — MF3 human verification gates | Feature 2 | Candidates and the report draft are verified by the author Inspector and approved by a qualified ORG_ADMIN before publication; a manual structured draft remains possible when drafting is unavailable. | Confirmed evidence set, an assigned Inspector, and a qualified reviewer in the same organization. |
| 4 | `[WF3-006]` FE-06 — MF3 immutable approved report | Feature 2 | The approved report version is immutable and source-traceable, and hands only repair-required findings to MF4. | Published MF3 review artifacts exist. |
| 5 | `[WF3-009]` FE-04 — MF3 scoped inspection and report collections | Feature 2 | A caller reaches MF3 through a server-paged, role-scoped list instead of a hand-entered identifier; the report review queue is the same collection filtered to inspections that carry a report. | Two organizations and fixtures for each of the four roles exist. |
| 6 | `[WF3-010]` FE-07 — MF4 work-order source and tenant scope | Feature 2 | ORG_ADMIN reads published repair candidates and opens one draft work order; duplicate active finding is rejected, cross-tenant reads are 404, and non-admin creation is denied. | PostgreSQL/Testcontainers; published MF3 report with human-confirmed repair-required finding; two organizations and active users. |
| 7 | `[WF3-011]` FE-07 — MF4 team, estimate and change control | Feature 2 | ORG_ADMIN assigns an independent team, team lead prepares a priced estimate, SYSTEM calculates total, only designated budget approver can approve/return, invalid credentials are blocked, and rejected change does not become approved scope. | MF4-01 draft work order; engineers and same-organization ORG_ADMIN fixtures; credential absent or expired per exercised scenario. |
| 8 | `[WF3-012]` FE-07 — MF4 work execution, independent acceptance and reconciliation | Feature 2 | Assigned team records and verifies work logs, completion is blocked until all logs are verified, author submits completion report, independent ORG_ADMIN accepts, currency-checked actuals reconcile against authorized baseline, then authorized reviewer closes the order. Rework/resume and currency-mismatch paths are also exercised. | Approved work order and estimate; tasks/team/logs; report author and distinct accepting reviewer; PostgreSQL/Testcontainers. |

## Coverage gaps

These are stated as gaps rather than filled with fabricated cases or statuses.

- **MF1 and MF2** (asset/schedule setup, readiness) are unimplemented, so they
  have no case.
- **MF4** has backend cases `WF3-010`–`WF3-012` for the implemented API slice;
  full product coverage is still incomplete: skills/credential issuance,
  notifications, linked MF1 re-inspection dispatch, evidence upload/rendering,
  web/mobile clients, and the remaining target gates are not verified.
- **FE-08** dashboard, analytics and notifications has no assigned case.
- **MF3 assignment/checklist entry** has no endpoint, so there is no case.

Mobile application verification is not recorded in this round; every case below
is evidenced by backend and web tests only.
