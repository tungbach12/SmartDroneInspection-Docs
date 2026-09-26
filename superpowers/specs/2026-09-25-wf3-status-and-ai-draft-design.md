# Design: WF3 Inspection Close-out and AI Report Draft

**Date**: 2026-09-25
**Status**: Approved design, pending implementation plan
**Scope**: Backend `inspections` module (plus `infrastructure/ai` adapter and cross-repo test/report updates)

## Context

WF3 is fully implemented and verified (Report 5 WF3-001–004 all Passed), but two gaps remain against the specification:

1. `InspectionStatus` defines six values while code only ever writes two (`READY_FOR_INSPECTION → IN_PROGRESS`). In particular, an inspection never reaches `COMPLETED`, so "is this inspection finished?" cannot be answered from the inspection record.
2. Business-flow WF3-11 permits optional LLM-assisted report drafting ("subject to human review"). No draft-generation mechanism exists; `ReportVersion.pdfObjectKey` and other speculative fields are unrelated and out of scope.

## Goals

- Close the inspection lifecycle: an accepted report transitions its inspection to `COMPLETED` atomically with client acceptance.
- Add an explicit, human-reviewed AI narrative draft step for report versions, following the existing YOLO/SPI integration pattern.

## Non-goals

- `CANCELLED` inspection state: no cancellation flow exists in WF3; writing a transition with no trigger would be speculative.
- PDF generation (`pdfObjectKey` remains unused).
- Automatic LLM call inside `createDraft`.
- Persisting LLM output outside the version snapshot.
- Carrying the narrative forward across report revisions.
- WF4 billing behavior beyond the existing `ReportAcceptedEvent` publication (unchanged).

## Decisions (settled during brainstorming)

| # | Question | Decision |
| --- | --- | --- |
| 1 | When does an inspection complete? | On Client `ACCEPT` in `clientDecision`, same transaction. Release is not terminal (revision requests can reopen work); acceptance matches the billing milestone in WF3-20/21 and pairs 1:1 with `ReportStatus.ACCEPTED`. |
| 2 | LLM mechanism | External HTTP API, OpenAI-compatible `POST {baseUrl}/chat/completions`, configuration-driven. |
| 3 | Draft entry point | Explicit `POST` endpoint, version must be current and `DRAFT`; AI failure returns 503 and leaves the draft usable. |
| 4 | LLM payload data | Snapshot content minus GPS and uploader identity: checklist Q&A, verified findings (label/severity/notes), evidence filename/type only. |
| 5 | Provider shape | OpenAI-compatible chat completions; works with cloud providers and local gateways (Ollama, vLLM). |
| 6 | Where narrative lives | Approach A: optional `aiDraftNarrative` field inside the existing `ReportSnapshot` JSONB, plus a human-edit `PUT` endpoint. |

## Design

### 1. Inspection close-out

No schema change: `InspectionStatus.COMPLETED` already exists in the enum and the `V7` check constraint.

- Add `Inspection.complete()` in `inspections/domain/Inspection.java`:
  - `IN_PROGRESS → COMPLETED` only.
  - Any other state throws the existing state-conflict style error (no idempotent overwrite; callers guard idempotency).
- In `InspectionReportService.clientDecision`, inside the `ACCEPT` branch (after `version.accept(...)` and `ReportAcceptedEvent` publication), resolve the inspection and call `complete()` within the same transaction.
- The existing "already accepted" early-return makes the transition fire exactly once; repeated `ACCEPT` calls do not re-transition.
- Inspection states `READY_FOR_INSPECTION`, `AWAITING_AI_REVIEW`, `AWAITING_REPORT`, and `CANCELLED` remain unwritten; `AWAITING_REPORT`/`COMPLETED` acceptance in `requireAssignedInspection` is unchanged.

### 2. AI report draft

#### 2.1 Port and adapter

- `inspections/spi/ReportDraftPort`: feature-owned outbound port in the existing `@NamedInterface("spi")` package.
  - Input: sanitized draft request (checklist entries, finding entries, evidence name/type pairs, report/asset context identifiers as plain strings).
  - Output: non-blank narrative text.
  - Failure: `IOException`-style checked contract mapped by the service, mirroring `AiInferencePort`.
- `infrastructure/ai/ReportDraftClient` implements the port; `infrastructure/ai/ReportDraftProperties` binds `app.report-draft.{base-url,api-key,model,timeout}` from environment configuration. No credentials in source.
- Injected as `Optional<ReportDraftPort>`; missing configuration yields 503 `REPORT_DRAFT_UNAVAILABLE` (same pattern as `AI_INFERENCE_UNAVAILABLE` and `EVIDENCE_STORAGE_UNAVAILABLE`).

#### 2.2 Snapshot change

- `ReportSnapshot` gains an optional `aiDraftNarrative` field (nullable string).
- **Compatibility rule**: snapshots already stored in `report_versions.content_snapshot` lack this property. Deserialization must default it to `null` for existing rows; no backfill migration and no Flyway change (jsonb column already exists).
- The narrative is version content: it is included in `toResponse`, visible to Clients on client-visible versions, and covered by existing immutability rules.

#### 2.3 Endpoints

Both endpoints require the report author (Inspector), the target version to be the report's current version, and version status `DRAFT`; both use the existing pessimistic locking style.

| Endpoint | Behavior |
| --- | --- |
| `POST /api/v1/reports/{reportId}/versions/{versionId}/ai-draft` | Build sanitized payload from current snapshot; call `ReportDraftPort`; validate response (non-blank, configured length cap); merge into `content_snapshot.aiDraftNarrative`; save. |
| `PUT /api/v1/reports/{reportId}/versions/{versionId}/narrative` | Body `{ "text": string }`; size cap; overwrite `aiDraftNarrative`; save. This is the "subject to human review" correction step. |

Error mapping:

| Condition | Response |
| --- | --- |
| Draft port absent or call fails/timeout/invalid payload | 503 `REPORT_DRAFT_UNAVAILABLE`, snapshot unchanged |
| Not the author | 403 `REPORT_SCOPE_DENIED` |
| Version not current or not `DRAFT` | 409 `REPORT_STATE_CONFLICT` |
| Blank or oversized narrative text | 422 `REPORT_DRAFT_INVALID` (matches existing `*_INVALID` convention) |

#### 2.4 Revision rule

`createRevision` recomposes the snapshot from live data and does **not** copy `aiDraftNarrative`. Stale prose must not describe new checklist/finding content. The inspector re-runs `ai-draft` on the new version when wanted.

### 3. Security and data handling

- AI payload excludes latitude, longitude, uploader identity, and review comments; only fields listed in Decisions #4 are sent.
- Never log narrative content, payloads, API keys, or response bodies; log only failure metadata (status code, timeout) as the YOLO client does.
- Authorization remains backend-enforced: author-only endpoints, DRAFT-only, org scope unchanged from existing report rules.
- API key read from environment configuration; validate presence at startup when the adapter is enabled.

## Testing (TDD — write failing tests first)

**Service-level (`InspectionReportServiceTest` extension or sibling):**

1. Client `ACCEPT` sets `InspectionStatus.COMPLETED`; report/version become `ACCEPTED`; event still published once.
2. Repeat `ACCEPT` is idempotent (early-return path) with no state thrash.
3. `ai-draft` happy path persists narrative into snapshot.
4. AI port failure → `REPORT_DRAFT_UNAVAILABLE`, snapshot unchanged.
5. Narrative `PUT` rejects non-`DRAFT` version, non-author, blank and oversized text.
6. Revision omits narrative from recomposed snapshot.

**Adapter (`ReportDraftClientTest`, HTTP stub like `YoloInferenceClientTest`):**

1. Request body contains checklist/findings/evidence names and **no** `latitude`/`longitude`/uploader fields.
2. Timeout and non-2xx responses map to the port failure contract.

**API integration (`InspectionReportApiIntegrationTest` extension):**

1. Author can `PUT` narrative and `POST` ai-draft on a current DRAFT version.
2. Non-author Inspector → 403; Client → 403; non-DRAFT version → 409.

## Documentation impact

Per AGENTS.md synchronization requirements, the same change must update:

- Report 3 `03-functional-requirements.md`: FE-06 AI-draft behavior and inspection completion on client acceptance, plus `00-record-of-changes.md` row.
- `docs/project-reference/business-flows.md`: WF3-11 (LLM draft step), WF3-20 (inspection terminal state).
- Report 5: new or updated FE-06 case covering AI draft (failure path included) and `COMPLETED` transition; recount statistics; stable IDs only, no fabricated rows.
- Backend contract docs (`docs/backend/`) if endpoint documentation exists for report APIs.
- No `database-design.md` change; no Flyway migration.

## Risks and open questions

- **Narrative edit surface**: the `PUT` makes the narrative human-editable inside a snapshot otherwise derived from structured data; review flows already treat snapshot as authoritative, so no additional reader changes are needed.
- **Third-party LLM availability**: all paths fail closed (503) without affecting existing draft/report flows; deterministic stub in tests, live provider run recorded honestly in Report 5 as pending if not executed.
- **Payload minimization vs. draft quality**: decision #4 may produce thinner drafts than sending GPS/evidence metadata; acceptable trade-off, revisitable if draft quality is insufficient in practice.
