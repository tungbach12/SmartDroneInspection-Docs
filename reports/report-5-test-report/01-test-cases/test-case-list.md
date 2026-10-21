# Test Cases sheet source

This table mirrors the `Test Cases` sheet. The workbook columns and order are
fixed: `No`, `Function Name`, `Sheet Name`, `Description`, `Pre-Condition`.

## Project and environment notes

| Field | Value |
| --- | --- |
| Project Name | SmartDroneInspection |
| Project Code | SEP490 — *confirm with project owner* |
| Test environment | Local/integration environment with PostgreSQL, backend API, and web client; integration suites use a real MinIO container for object storage, and S3Mock 5.2.3 covers the S3 API subset in the adapter test. |
| Baseline | **Verified MF2-07 readiness decisions and the implemented MF3 slice.** Current roles: `ADMIN`, `ORG_ADMIN`, `INSPECTOR`, `MAINTENANCE_ENGINEER`. The MF3-12/13 post-publication corrective-outcome and handoff code exists and its backend paths executed green on 2026-10-16 (81 targeted WF3 tests and the 650-test full `verify` gate), but `WF3-012` remains Pending until its complete end-to-end procedure is executed. Other MF2 steps remain partial or unimplemented as documented in FE-03. |

## Reset and reconciliation scope (2026-10-09 to 2026-10-10)

The earlier content mixed a retired five-role WF1–WF4 baseline with the current
four-role Enterprise SaaS target. The 2026-10-09 reset removed obsolete and
unimplemented cases. The 2026-10-10 reconciliation restored the two MF2-07
readiness cases backed by merged backend PR #64 and its CI evidence; `WF2-010`
was added later for the scoped preparation-history listing. The current
additional-session loop and MF2-12 completion have focused tests but no complete
Report 5 end-to-end case yet.

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
The removed IDs remain reserved. `WF3-010`, `WF3-011` and `WF3-012` are active; new MF3 cases continue from `WF3-013`.

The 2026-10-10 merge of backend PR #64 (`84fcc16`), frontend PR #37
(`287d5a4`) and mobile PR #9 (`91092e6`) added MF2 runtime. `WF2-008` and
`WF2-009` now record MF2-07 readiness approve/return verification only; they do
not claim full MF2 completion. MF2-08 generic invalidation is partial, and
MF2-12 normal session completion is implemented without a Report 5 case. MF1 and
MF4 remain gaps. FE-01
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
| 2a | `[WF2-010]` FE-03 — MF2 preparation listing scope | Feature 3 | An authorized Inspector reads the preparation history of an inspection in their own organization with `200`; an Inspector in another organization is refused with `404` rather than a server error, because the read path takes no pessimistic lock. | Two organizations each with an `INSPECTOR`; one inspection in the first organization; PostgreSQL 17/Testcontainers. |
| 3 | `[WF3-002]` FE-04 — MF3 evidence and traceability | Feature 4 | Assigned Inspector uploads supported evidence with a server-computed checksum and source metadata, retry-safe persistence, and scoped read access; type, size (10 MB per file / 20 MB per request), empty and corrupt/undecodable input are refused with a corrective action; the Inspector records the substantive evidence-quality decision together with its shot-list comparison, which both client and server require to be non-blank. | Assigned inspection past field work; valid image, PostgreSQL via Testcontainers, and MinIO via the shared test infrastructure initializer. |
| 4 | `[WF3-003]` FE-05 — MF3 AI candidate and finding review | Feature 5 | Inspector reviews AI candidates or records a manual finding; pending/rejected detections stay non-official; a confirmed candidate creates an undecided finding that only an independent ORG_ADMIN other than the finding creator can make official under MF3-09 (runtime checks role, organization and independence; reviewer credential qualification is not validated). | Accepted evidence set; deterministic inference stub or manual fallback available. |
| 5 | `[WF3-005]` FE-06 — MF3 human verification gates and section-scoped drafting | Feature 6 | Candidates and the report draft are verified by the author Inspector and approved by an independent ORG_ADMIN before publication; automated drafting proposes section values without altering the reviewed findings, and a manual structured draft remains possible when drafting is unavailable. Evidence changes after draft creation stale its snapshot; verify/submit refuses a stale version. | Confirmed evidence set, an assigned Inspector, and an independent active ORG_ADMIN in the same organization. |
| 6 | `[WF3-006]` FE-06 — MF3 immutable approved report with PDF deliverable | Feature 6 | The approved report version is immutable and source-traceable, publication stores its PDF deliverable and records the checksum, only findings with an MF3-12 corrective-work outcome are handed to MF4, and the PDF evidence register shows linked official finding component/location when capture location is absent. | Published MF3 review artifacts exist; report preview fixtures include linked evidence and a confirmed finding with component/location. |
| 7 | `[WF3-009]` FE-04 — MF3 scoped inspection and report collections | Feature 4 | A caller reaches MF3 through a server-paged, role-scoped list instead of a hand-entered identifier; the report review queue is the server-paged `/with-reports` collection shown as the inspections list's `?view=reports` filtered view, with saved `/reports` links redirecting to it. | Two organizations and fixtures for each of the four roles exist. |
| 8 | `[WF3-010]` FE-05 — MF3 reviewed-candidate correction and rejection | Feature 5 | The assigned Inspector can correct their reviewed candidate and linked undecided finding before an ORG_ADMIN decision or downstream report lock; correction is refused after either lock. Rejecting the corrected candidate removes its linked undecided proposal, while final reviewer decisions remain immutable. | Reviewed candidate, linked finding, assigned Inspector, and report fixtures covering unlocked, submitted/locked and reviewer-decided states. |
| 9 | `[WF3-011]` FE-06 — MF3 findings confirmation and separate draft choice | Feature 6 | Inspector resolves all AI candidates, confirms the complete findings set, and reaches Report without an implicit draft/version or AI call; empty scope requires acknowledgment. AI-assisted and manual draft choices remain separate, and stale evidence/findings require reopening and reconfirmation. | Assigned Inspector, completed inspection, accepted evidence-quality decision, API/UI tests for pending candidate, zero findings, confirmation, AI/manual paths, stale-source and reviewer-decision gates. |
| 10 | `[WF3-012]` FE-06 — MF3 post-publication corrective outcome and handoff | Feature 6 | After the immutable PDF is published, the Organization Admin records one attributable corrective-action outcome per confirmed/modified finding (work required with rationale and priority, optional due date; or no action with rationale); the System records the MF3-13 handoff and marks only work-required findings for MF4. The handoff completes the inspection when every official finding was recorded as no-action, and an explicitly confirmed empty findings set closes with a reasoned no-repair outcome through `no-corrective-work`. The handoff does not create an MF4 work order; the published PDF is never modified. Partly executed 2026-10-17 through the running web client and API: publication ended at `REPORT_PUBLISHED` with the stored checksummed PDF, the pre-outcome handoff was refused with `409 CORRECTIVE_ACTION_REVIEW_INCOMPLETE`, the work-required and no-action outcomes were recorded, a priority on a no-action outcome was refused with `400`, repeating an outcome returned `409 CORRECTIVE_ACTION_ALREADY_RECORDED`, the handoff moved the inspection to `REPAIR_PENDING` with only the work-required finding handed off and no MF4 work order created, repeating it returned `409 CORRECTIVE_HANDOFF_ALREADY_COMPLETED`, and `no-corrective-work` with official findings returned `409 CORRECTIVE_ACTION_REVIEW_REQUIRED`. Still Pending: the all-no-action close (`COMPLETED` with no handed-off findings) and the explicitly confirmed empty-findings no-repair close have not been executed. | Published MF3 report with confirmed/modified findings (plus an empty-findings variant); active independent ORG_ADMIN; PostgreSQL via Testcontainers; current backend source with V30. |

## Coverage gaps

These are stated as gaps rather than filled with fabricated cases or statuses.

- **MF1** (asset/schedule setup) and **MF4** (maintenance, triage, cost
  reconciliation) remain unimplemented and have no cases.
- **MF2** is only partly covered: `WF2-008` and `WF2-009` test MF2-07 readiness
  approval/return, while `WF2-010` covers the scoped preparation-history read.
  Assignment response, preparation/compliance, source-change
  invalidation, field-session start/postpone/abort/completion and the full
  additional-session round trip are not represented by Report 5 cases. MF2-08
  generic invalidation remains partial in runtime; MF2-12 completion is now implemented.
- **FE-08** dashboard, analytics and notifications has no assigned case.

The MF2-07 cases and five of the eight MF3 cases have executed backend/web test
evidence. `WF3-010` is Pending until its correction/rejection/lock procedure
executes; `WF3-011` is Pending until the aggregate gate, separate draft choices,
stale-source and independent-review procedure executes; `WF3-012` is Pending
until the all-no-action close and the empty-findings no-repair close of the
post-publication corrective-outcome and handoff scenario execute against a green
run; the remaining steps of that scenario ran 2026-10-17 through the web client and
API. The case index does not
claim mobile app verification for these cases; mobile checks are recorded
separately in supporting statistics where run.
