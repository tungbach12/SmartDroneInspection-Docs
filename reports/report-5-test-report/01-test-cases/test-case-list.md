# Test Cases sheet source

This table mirrors the `Test Cases` sheet. The workbook columns and order are
fixed: `No`, `Function Name`, `Sheet Name`, `Description`, `Pre-Condition`.

## Project and environment notes

| Field | Value |
| --- | --- |
| Project Name | SmartDroneInspection |
| Project Code | SEP490 — *confirm with project owner* |
| Test environment | Local/integration environment with PostgreSQL, backend API, and web client; MinIO is used for runtime/storage verification, while S3Mock 5.2.3 is used by CI S3 API integration tests. |
| Baseline | **Executed backend scope: MF2-07 readiness, selected MF3 behavior, and selected MF4 backend API behavior.** Roles are `ADMIN`, `ORG_ADMIN`, `INSPECTOR`, `MAINTENANCE_ENGINEER`. Remaining requirements are listed as coverage gaps. |

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
- `WF3-007`, `WF3-008`: despite the `WF3` prefix these described **MF4** team,
  cost and completion-report gates and remain reserved.
- `WF4-001`–`WF4-005`: prior MF4 cases removed on 2026-10-09; IDs remain
  reserved and are never reused.

Retained at reset: `WF3-002`, `WF3-003`, `WF3-005`, `WF3-006`, `WF3-009`,
`WF2-008` and `WF2-009`; the MF2 readiness cases were restored on 2026-10-10
after integration onto the current mainline and re-verification. Added the three
selected FE-07 backend cases `WF3-010`–`WF3-012` on 2026-10-10.

All removed IDs remain reserved and are never reused. After `WF3-009`, the new
selected backend cases continue at `WF3-010`.

This report records only tested portions: MF2 readiness approval/return, selected
MF3 cases and selected MF4 backend REST behavior. It does not claim all MF1, MF2
or MF4 requirements are implemented; remaining work stays explicit in the
coverage gap and FE-specific notes.

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
| 8 | `[WF3-010]` FE-07 — MF4 work-order source and tenant scope | Feature 2 | ORG_ADMIN reads published repair candidates and opens one draft work order; duplicate active finding is rejected, cross-tenant reads are 404, and non-admin creation is denied. | PostgreSQL/Testcontainers; published MF3 report with human-confirmed repair-required finding; two organizations and active users. |
| 9 | `[WF3-011]` FE-07 — MF4 team, estimate and change control | Feature 2 | ORG_ADMIN assigns an independent team, lead prepares priced estimate, SYSTEM calculates total, only designated budget approver decides, invalid credential is blocked, and rejected change remains unapproved. | Draft work order; active same-org engineers and ORG_ADMIN; credentials absent or expired in the tested scenario. |
| 10 | `[WF3-012]` FE-07 — MF4 execution, acceptance and reconciliation | Feature 2 | Team work logs are submitted and lead-verified before completion; author submits report; independent reviewer accepts; currency-checked actuals reconcile and close. Rework/resume and mismatch paths are exercised. | Approved work order/estimate, team/task/logs, report author and independent reviewer; PostgreSQL/Testcontainers. |
## Coverage gaps

These are stated as gaps rather than filled with fabricated cases or statuses.

- **MF1** (workspace entitlement, asset/Drone/Inspector pair setup) is
  unimplemented, so it has no case.
- **MF2 outside MF2-07** — assignment response, shot-list preparation and the
  field session — has no executed case beyond the two readiness cases above.
- **MF4** has selected backend API cases `WF3-010`–`WF3-012`; full scope remains
  incomplete. Skills/credential administration, notifications, MF1 re-inspection
  dispatch, evidence object upload/report rendering and web/mobile clients remain
  unverified.
- **FE-08** dashboard, analytics and notifications has no assigned case.
- **MF3 assignment/checklist entry** has no endpoint, so there is no case.

Mobile application verification is not recorded in this round; every case below
is evidenced by backend and web tests only.
