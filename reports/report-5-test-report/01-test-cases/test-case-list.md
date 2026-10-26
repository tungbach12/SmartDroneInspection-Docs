# Test Cases sheet source

This table mirrors the `Test Cases` sheet. The workbook columns and order are
fixed: `No`, `Function Name`, `Sheet Name`, `Description`, `Pre-Condition`.

## Project and environment notes

| Field | Value |
| --- | --- |
| Project Name | SmartDroneInspection |
| Project Code | SEP490 — *confirm with project owner* |
| Test environment | Local/integration environment with PostgreSQL, backend API, and web client; integration suites use a real MinIO container for object storage, and S3Mock 5.2.3 covers the S3 API subset in the adapter test. |
| Baseline | **Verified MF2-07 readiness decisions and the implemented MF3 slice.** Current roles: `ADMIN`, `PLATFORM_MANAGER`, `ORG_MANAGER`, `INSPECTOR`, `MAINTENANCE_ENGINEER`. The MF3-12/13 post-publication corrective-outcome and handoff code exists and its backend paths executed green on 2026-10-16 (81 targeted WF3 tests and the 650-test full `verify` gate), but `WF3-012` remains Pending until its complete end-to-end procedure is executed. Other MF2 steps remain partial or unimplemented as documented in FE-03. |

## Recurring inspection and in-app notifications implementation (2026-10-26)

FE-03 recurrence schedules and FE-08 in-app notification inbox have 96 passing backend unit/service/controller tests, 200 passing frontend tests, and 6 mobile test suites, recorded as supporting evidence in the FE-03 source. Full PostgreSQL/Docker integration tests remain Pending because Docker was unavailable. No reserved WFx ID is reused and no workbook case status or denominator changes.

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
  Publication is now an `ORG_MANAGER` act with no Client acceptance step.
- `WF3-007`, `WF3-008`: despite the `WF3` prefix these describe **MF4** team,
  cost and completion-report gates, outside FE-06 and unimplemented MF4 scope.
- `WF4-001`–`WF4-005`: MF4 maintenance, triage and cost reconciliation.

Retained MF3 cases: `WF3-002`, `WF3-003`, `WF3-005`, `WF3-006`, and `WF3-009`.
The removed IDs remain reserved. `WF3-010`, `WF3-011` and `WF3-012` are active; new MF3 cases continue from `WF3-013`.

The 2026-10-10 merge of backend PR #64 (`84fcc16`), frontend PR #37
(`287d5a4`) and mobile PR #9 (`91092e6`) added MF2 runtime. `WF2-008` and
`WF2-009` now record MF2-07 readiness approve/return verification only; they do
not claim full MF2 completion. MF2-08 generic invalidation is partial, and
MF2-12 normal session completion is implemented in code and has focused tests but no Report 5 case. MF1 and
MF4 remain gaps. FE-01
supporting verification remains outside the workbook case index and functional
case statistics; see `03-features/fe-01-identity-access-governance.md`.

## Case index

The `Sheet Name` column refers to the generated workbook sheet, not to an SRS
feature code. The exporter maps `Feature N` to `FE-0N`; `WFx-yyy` remains the
stable business-flow test-case ID.

| No | Function Name | Sheet Name | Description | Pre-Condition |
| ---: | --- | --- | --- | --- |
| 1 | `[WF2-008]` FE-03 — MF2 readiness approval | Feature 3 | An independent qualified ORG_MANAGER approves current submitted preparation only when actor, organization, source attribution, validity, pair chronology, applicability, and permit gates pass; invalid paths do not persist a decision or state transition. | PostgreSQL 17/Testcontainers, V25/V28 schema, assigned Inspector, independent active ORG_MANAGER, current submitted preparation, and persisted permit/credential/document/pair records. |
| 2 | `[WF2-009]` FE-03 — MF2 readiness return | Feature 3 | A qualified reviewer returns submitted preparation despite evidence gaps, preserving the reason and exact observed/unresolved source IDs with completeness false; invalid reviewer/scope or blank reason changes no state. | PostgreSQL 17/Testcontainers, active independent ORG_MANAGER with valid reviewer credential, and current submitted preparation. |
| 2a | `[WF2-010]` FE-03 — MF2 preparation listing scope | Feature 3 | An authorized Inspector reads the preparation history of an inspection in their own organization with `200`; an Inspector in another organization is refused with `404` rather than a server error, because the read path takes no pessimistic lock. | Two organizations each with an `INSPECTOR`; one inspection in the first organization; PostgreSQL 17/Testcontainers. |
| 3 | `[WF3-002]` FE-04 — MF3 evidence intake | Feature 4 | Assigned Inspector uploads supported evidence with file metadata and scoped read access; type, size (10 MB per file / 20 MB per request), empty and corrupt/undecodable input are refused with a corrective action; no evidence-quality decision, checksum identity or shot-list comparison is required. | Assigned inspection past field work; valid image, PostgreSQL via Testcontainers, and MinIO via the shared test infrastructure initializer. |
| 4 | `[WF3-003]` FE-05 — MF3 AI candidate and finding review | Feature 5 | Assigned Inspector invokes analysis on selected active evidence or records a manual finding; proposals remain advisory until resolved; the Inspector explicitly confirms the complete findings set, including acknowledgment when it is empty. No evidence-acceptance gate or automatic analysis applies. | Active evidence; deterministic inference stub or manual path available. |
| 5 | `[WF3-005]` FE-06 — MF3 human verification gates and section-scoped drafting | Feature 6 | Inspector-confirmed findings and the report draft are verified by the author Inspector and approved by an independent ORG_MANAGER before publication; coverage/limitations are authored in the report, and AI drafting is invoked only when selected. Manual authoring remains available if drafting is unavailable. | Active evidence and confirmed findings set, assigned Inspector, and independent active ORG_MANAGER in the same organization. |
| 6 | `[WF3-006]` FE-06 — MF3 immutable approved report with PDF deliverable | Feature 6 | The approved report version is immutable and source-traceable, publication stores its PDF deliverable and records the PDF checksum, and the evidence register shows linked finding/evidence location metadata. Per-finding forwarding occurs after publication (see `WF3-012`). | Published MF3 review artifacts exist; report preview fixtures include linked evidence and a confirmed finding with component/location. |
| 7 | `[WF3-009]` FE-04 — MF3 scoped inspection and report collections | Feature 4 | A caller reaches MF3 through a server-paged, role-scoped list instead of a hand-entered identifier; the report review queue is the server-paged `/with-reports` collection shown as the inspections list's `?view=reports` filtered view, with saved `/reports` links redirecting to it. | Two organizations and fixtures for each of the roles exist. |
| 8 | `[WF3-010]` FE-05 — MF3 reviewed-candidate correction and rejection | Feature 5 | The assigned Inspector can correct their reviewed candidate and linked undecided finding before an ORG_MANAGER decision or downstream report lock; correction is refused after either lock. Rejecting the corrected candidate removes its linked undecided proposal, while final reviewer decisions remain immutable. | Reviewed candidate, linked finding, assigned Inspector, and report fixtures covering unlocked, submitted/locked and reviewer-decided states. |
| 9 | `[WF3-011]` FE-06 — MF3 findings confirmation and separate draft choice | Feature 6 | Inspector resolves all AI proposals, confirms the complete findings set, and reaches Report without an implicit draft/version or AI call; empty scope requires acknowledgment. AI-assisted and manual draft choices remain separate; AI analysis is invoked explicitly and evidence quality is not a gate. | Assigned Inspector, completed inspection with active evidence, API/UI tests for pending proposal, zero findings, acknowledgment, confirmation, AI/manual paths and stale-source gates. |
| 10 | `[WF3-012]` FE-06 — MF3 post-publication per-finding forwarding | Feature 6 | After the immutable PDF is published, the Organization Manager selects confirmed findings to forward to MF4; the System records `forwarded_to_maintenance_at` per selected finding and sets inspection status to `REPAIR_PENDING` or `COMPLETED`. No per-finding corrective rationale/priority/due date or inspection-level no-repair rationale/handoff actor/time is required; forwarding does not create an MF4 work order. Historical 2026-10-17 walkthrough exercised the superseded corrective-outcome flow and is not evidence for this target. Still Pending: per-finding selection/forwarding, no-selection completion and explicitly acknowledged empty-findings completion under the target contract. | Published MF3 report with confirmed findings plus no-selection and acknowledged-empty variants; active independent ORG_MANAGER; PostgreSQL via Testcontainers; target implementation. |

## Coverage gaps

These are stated as gaps rather than filled with fabricated cases or statuses.

- **MF1** (asset/schedule setup) and **MF4** (maintenance, triage, cost
  reconciliation) carry executed supporting verification recorded in FE-02 and FE-07
  rather than as new workbook rows, so those sheets stay empty and the totals do
  not move. MF1-01 to MF1-07 and the MF4-21 follow-up/warranty condition are
  still not represented by Report 5 cases.
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
