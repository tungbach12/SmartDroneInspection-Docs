---
title: "MF3 Inspection, Evidence and Report Runtime Flow"
weight: 40
---

# MF2/MF3 Inspection, Preparation and Report Runtime Flow

This describes the implemented Report 3 MF2 slice and MF3 workflow inside the
`inspections` Spring Modulith module. Roles are the four Enterprise SaaS roles:
`ADMIN`, `ORG_ADMIN`, `INSPECTOR`, `MAINTENANCE_ENGINEER`. The assigned
Inspector is the human report author; AI is advisory only. MF2-12 normal
completion and the MF3 additional-session return to MF2 are implemented.
Generic MF2-08 source-change invalidation remains partial.

Access is decided by the authenticated principal and scoped lookups, never by
client-supplied user, organization, owner, or assignment identifiers. Write
operations require the *assigned* Inspector; read and review operations also
allow a same-organization `ORG_ADMIN`. Write decisions remain backend-owned;
no decision automatically starts a field session.

## Assignment inbox and assignment response (FE-03, MF2-01/02)

Assignment response is separate from readiness approval. The Inspector may accept
or reject only their own assigned inspection; a rejection requires a reason and
returns the inspection to the organization workflow. Acceptance records the
response but does not establish `READY_FOR_FLIGHT`.

The API is rooted at `/api/v1/inspection-assignments`: `GET /mine` lists the
caller's unanswered assignments, `GET /{assignmentId}` reads one scoped
assignment, and `POST /{assignmentId}/response` records a response. All three
require `INSPECTOR`; the service derives the actor/organization from the
principal and checks that the pairing belongs to the assigned Inspector. The
response contract is represented by `AssetPairAssignmentResponse` and the
request by `RespondToAssignmentRequest`. A rejection needs a reason; acceptance
records response only and does not make the inspection ready for flight.

## Mission preparation and compliance (FE-03, MF2-03/06)

Preparation is versioned under an assigned inspection at
`/api/v1/inspections/{inspectionId}/preparation`. The assigned `INSPECTOR` can
list the history (`GET`), read a preparation (`GET /{preparationId}`), update
the shot-list (`PUT`), and submit the current version (`POST
/{preparationId}/submission`). Submission is serialized with readiness review
and is permitted only while the inspection is `PREPARING`. An MF3
`ADDITIONAL_SESSION_REQUIRED` decision returns the inspection to `PREPARING`,
appends readiness invalidation, supersedes the prior approved preparation, and
creates a next-version draft preserving the Inspector's shot-list, evidence
requirements and safety/access notes. Permit references are re-linked during
MF2 review rather than silently copied. The Inspector must set both a new future
planned start/end window on the additional-session preparation before the ORG_ADMIN
can re-evaluate credentials, Drone documents, pair validity and permits against
the revised time.

An `ORG_ADMIN` links applicable permit records with
`POST /compliance/permits` and reads the compliance gate with
`GET /compliance`. Source lookup is scoped to the organization; a permit link
is not a waiver, and the compliance result reports blockers rather than
granting readiness. External issuer/authority verification is not implied by
internal record status.

## Readiness approval and return (FE-03, MF2-07)

An active `ORG_ADMIN` who is not the submitting Inspector may approve or return
the current submitted preparation through
`/api/v1/inspections/{inspectionId}/readiness/{preparationId}/approval` or
`/return`. Approval requires a qualified reviewer with internally verified
credential and evidence attribution, valid source records, applicability
attestations, a timely accepted assignment pair, and no mandatory permit
blocker. Approval stores a source snapshot/hash and changes the preparation and
inspection readiness state. A return requires a reason and may be recorded
despite readiness gaps; its snapshot preserves observed and unresolved source
IDs and explicitly does not claim exhaustive observation.

The supporting routes `GET /api/v1/workforce/credentials/me` and
`GET /api/v1/inspections/{inspectionId}/readiness/sources` require `ORG_ADMIN`
and resolve records within the caller's organization. These internal record
checks are not external registry verification. `WF2-008` and `WF2-009` are the
Report 5 cases for approval/return rules; they do not cover all MF2 behavior.

## Inspection checklist (FE-04, MF2-11)

The assigned active `INSPECTOR` records checklist results against the
inspection. `GET /api/v1/inspections/{inspectionId}/checklist` returns the
checklist items and any answer already recorded against them, and
`PUT /api/v1/inspections/{inspectionId}/checklist-responses/{checklistItemId}`
records or replaces one answer. Both routes are restricted to the assigned
Inspector; a caller from another organization receives not-found rather than
another tenant's checklist.

The applicable checklist is the newest `ACTIVE` template for the inspection's
asset category, because templates are platform-scoped rather than
organization-scoped. An inspection whose category has no active template has no
checklist, and the list is empty rather than a missing-resource failure.

The checklist's own text — section, prompt, guidance — is system-managed and
follows the requested locale, with English as the explicit fallback when a
Vietnamese version has not been recorded. The Inspector's answer value, note and
completion time are their own record and are returned exactly as written: a note
is evidence of what was observed on site, not system copy to be translated.
Responses are refused once the inspection is published.

## Field sessions (FE-03, MF2-09/12)

An assigned active `INSPECTOR` may list their sessions, start a session, record
postponement, abort an open session, or normally complete it. Start requires an
inspection in `READY_FOR_FLIGHT`, a non-blank pre-flight checklist note, no
other open session, and the newest readiness decision to be `APPROVED`. That
approval must reference the latest preparation ID/version and the preparation
must be `READY`. Start records a software session and moves the inspection to
`IN_PROGRESS`; it never actuates or pilots the Drone. Postponement reopens the
inspection to `READY_FOR_FLIGHT`; abort records the abort but leaves the
inspection `IN_PROGRESS`.

The additional-session handoff appends `INVALIDATED` after verifying the
current approval belongs to the latest preparation. Generic permit/pair/credential
source-change workflows do not yet append invalidation, so MF2-08 remains partial.

Normal completion is `POST /api/v1/inspections/{inspectionId}/field-sessions/{sessionId}/completion`
with required `outcomeNotes`. It is restricted to the assigned active Inspector
and the current session/readiness decision. In one transaction it records
session `FIELD_COMPLETED`, end time and outcome notes and changes the inspection
from `IN_PROGRESS` to `FIELD_COMPLETED`; previous sessions/evidence remain.
Weather/site-safety postponement is separate and only applies while a session is
open. An aborted session is terminal and remains `ABORTED`; it cannot be converted
to `FIELD_COMPLETED`. No aircraft control, hardware telemetry or statutory
incident reporting is implied.

## Inspection and report collections (FE-04, FE-06)

| Operation | Endpoint | Actor |
| --- | --- | --- |
| List inspections | `GET /api/v1/inspections` | assigned Inspector, same-org ORG_ADMIN, platform ADMIN |
| List inspections with a report | `GET /api/v1/inspections/with-reports` | assigned Inspector, same-org ORG_ADMIN, platform ADMIN |

These routes live in `InspectionListController`, separate from
`InspectionController`, because every route in the latter is nested under
`/{inspectionId}` and a collection route would otherwise be ambiguous.

Both endpoints are **server-paged**: `page` starts at 1, `pageSize` defaults to
20 and is clamped to 100, and the response is
`{items, page, pageSize, totalCount, totalPages}`. An out-of-range page size is
clamped rather than rejected, matching the asset list contract. Rows are sorted
by `createdAt` then `id`; the `id` tie-breaker is required, because a
non-unique sort key lets the same row appear on two pages.

Scope is resolved from the caller and never from a query parameter:

| Caller | Sees |
| --- | --- |
| `INSPECTOR` | only inspections assigned to them |
| `ORG_ADMIN` | every inspection in their own organization |
| `ADMIN` (platform) | every organization, read-only |
| `MAINTENANCE_ENGINEER` | nothing; the request is refused |

Each row carries `reportId`, `reportStatus` and `reportVersionNo` for the
inspection's latest report, or `null` when it has none. A report belongs to an
inspection, so `/with-reports` is a filtered view of the same collection rather
than a second resource, and both screens read one source rather than
disagreeing about a report's state.

**Platform scope.** Cross-tenant read is an explicitly separate administrative
capability, so `ADMIN` holds no write path on this resource and the platform
plane is checked before organization scope (a platform user has no organization
by rule). Cross-tenant reads are recorded in the application log rather than
`audit_events`: an authorized administrative read is not a privileged write,
and durable audit rows are reserved for authentication, authorization changes,
writes and exports. Denied or unexpected cross-tenant attempts remain the
condition that must be monitored.

## Evidence intake (FE-04, MF3-01/02)

The Inspector may record a substantive evidence-quality decision only in
`FIELD_COMPLETED`. On `ADDITIONAL_SESSION_REQUIRED`, the previous completed
capture set and decision history remain auditable, but the old set becomes
read-only for further assessment/upload while the inspection is `PREPARING`.
After new preparation is submitted, independent ORG_ADMIN readiness review is
required before another start. Once that session is normally completed, the
inspection returns to `FIELD_COMPLETED`, and the Inspector can add captures and
assess the current active evidence set again. Only the latest `ACCEPTED` decision
unlocks advisory analysis and drafting. Weather/safety during field work remains
an MF2 postponement/abort, not an MF3 evidence-quality decision.


| Operation | Endpoint | Actor |
| --- | --- | --- |
| Upload evidence | `POST /api/v1/inspections/{inspectionId}/evidence` | assigned Inspector, same-org ORG_ADMIN |
| Retire evidence | `POST /api/v1/inspections/{inspectionId}/evidence/{evidenceId}/retire` | assigned Inspector |
| Bulk retire evidence | `POST /api/v1/inspections/{inspectionId}/evidence/bulk-retire` | assigned Inspector |
| List evidence | `GET /api/v1/inspections/{inspectionId}/evidence` | assigned Inspector, same-org ORG_ADMIN |
| Query evidence (filtered, paged) | `GET /api/v1/inspections/{inspectionId}/evidence/query` | assigned Inspector, same-org ORG_ADMIN |
| Stream evidence | `GET /api/v1/inspections/{inspectionId}/evidence/{evidenceId}/content` | assigned Inspector, same-org ORG_ADMIN |

Multipart fields are `file` (required), `source`
(`SD_CARD`|`WEB_UPLOAD`|`MOBILE_UPLOAD`|`IMPORTED`, default `WEB_UPLOAD`),
`captureTime`, `latitude`, `longitude`, `externalReference`.

Accepted content types are `image/png`, `image/jpeg`, `image/webp`,
`image/tiff`, `video/mp4`, `application/pdf`. The per-file cap is 10 MB
(`EVIDENCE_MAX_FILE_SIZE`, applied by both the Spring multipart parser and the
service guard); the request cap is 20 MB (`EVIDENCE_MAX_REQUEST_SIZE`), leaving
room for multipart framing across the single-file endpoint. An over-limit
request is rejected with `413`: the multipart parser answers `PAYLOAD_TOO_LARGE`,
while the service guard answers `EVIDENCE_TOO_LARGE` and derives its message from
the enforced 10 MB limit.

`GET .../evidence/query` is the filtered, paged read used by the evidence
register. Query parameters: `status` (`ACTIVE`|`RETIRED`|`ALL`, default `ALL`),
`mediaType` (`IMAGE`|`VIDEO`|`DOCUMENT`|`ALL`, default `ALL`), optional `search`
(case-insensitive file-name or content-type substring), `page` (1-based, default
1) and `pageSize` (default 50, clamped to 1–100). Filtering and paging happen in
the database, and rows are ordered by `createdAt` then `id` so a page cannot
repeat or skip a row. The response carries `items`, `page`, `pageSize`,
`totalCount`, `totalPages`, the inspection's `activeCount`/`retiredCount`, and
`latestCreatedAt`/`latestRetiredAt` — the newest capture-added and
capture-retired instants — so a client can show the status counts and detect a
evidence-quality decision that predates the current set without loading every
row. The original `GET .../evidence` list contract is unchanged.

Latitude and longitude must be supplied together. The server computes SHA-256
and treats a repeated inspection/checksum upload idempotently, returning the
existing evidence rather than a duplicate. Evidence responses expose metadata
only — never object-store keys or URLs. `MINIO_ENABLED=true` plus the endpoint,
bucket, access key and secret key enable real storage; without an
`EvidenceObjectStore` bean the upload fails with `EVIDENCE_STORAGE_UNAVAILABLE`.

## Evidence quality decision (FE-04, MF3-03/04)

| Operation | Endpoint | Actor |
| --- | --- | --- |
| Record decision | `POST /api/v1/inspections/{inspectionId}/evidence-quality-decisions` | assigned Inspector |
| Decision history | `GET /api/v1/inspections/{inspectionId}/evidence-quality-decisions` | assigned Inspector, same-org ORG_ADMIN |

`decision` is `PENDING`|`ACCEPTED`|`REUPLOAD_REQUIRED`|
`ADDITIONAL_SESSION_REQUIRED`|`LIMITED`. `PENDING` is rejected at runtime with
`EVIDENCE_QUALITY_INVALID`. `LIMITED`, `REUPLOAD_REQUIRED` and
`ADDITIONAL_SESSION_REQUIRED` each require a non-blank `limitationReason`.

The decision requires the inspection to be `FIELD_COMPLETED` or `REPORT_DRAFT`.
Only an accepted decision makes the evidence set eligible for advisory
detection and report drafting.

`shotListComparison` is stored in a `jsonb` column while the Inspector writes
prose, so the service stores the text as a single `summary` entry and returns it
unchanged. The same applies to a finding's `measurement`.

## Findings (FE-05, MF3-05/06/09)

| Operation | Endpoint | Actor |
| --- | --- | --- |
| List findings | `GET /api/v1/inspections/{inspectionId}/findings` | assigned Inspector, same-org ORG_ADMIN |
| List removed findings | `GET /api/v1/inspections/{inspectionId}/findings/removed` | assigned Inspector, same-org ORG_ADMIN |
| List completed evidence analysis status (including zero detections) | `GET /api/v1/inspections/{inspectionId}/evidence/analysis-status` | assigned Inspector, same-org ORG_ADMIN |
| Analyze evidence | `POST /api/v1/inspections/{inspectionId}/evidence/{evidenceId}/analyze[?replace=true]` | assigned Inspector |
| Confirm finding | `POST /api/v1/inspections/{inspectionId}/findings/{findingId}/confirmation` | assigned Inspector |
| Add manual finding | `POST /api/v1/inspections/{inspectionId}/findings` | assigned Inspector |
| Update finding | `PUT /api/v1/inspections/{inspectionId}/findings/{findingId}` | assigned Inspector |
| Remove finding | `DELETE /api/v1/inspections/{inspectionId}/findings/{findingId}` | assigned Inspector |
| Restore removed finding | `POST /api/v1/inspections/{inspectionId}/findings/{findingId}/restore` | assigned Inspector |
| Record corrective outcome | `PUT /api/v1/inspections/{inspectionId}/findings/{findingId}/corrective-action` | same-org ORG_ADMIN |

Successful analysis timestamps and detection counts are persisted on evidence so a valid empty detector result is distinguishable from an image not yet analysed and does not repeat on reload. A deliberate `replace=true` request performs a new pass. A valid zero-detection YOLO response does not trigger fallback.

AI is optional. `YOLO_INFERENCE_ENABLED` selects the self-hosted detector, which is
the default advisory provider and is served by the `ai-inference` service in this
repository; `COMPATIBLE_VISION_ENABLED` adds the OpenAI-compatible vision endpoint
as the option behind it. The detector is tried first, and the vision endpoint
answers only when the detector cannot — a connection failure, a timeout, an error
status or an empty response. An image the detector processed with no detections is
an answer, not a failure, and is not re-checked by the option. With neither
provider configured the analysis endpoints report that automated analysis is not
configured.

A finding is one observation, whoever made it. The detector proposes and the Inspector
records what they saw, and both are the same kind of row: a `PENDING` finding that the
Inspector has yet to look at, and a `CONFIRMED` finding that is official. The model
provenance travels with the row when there is one, so a caller can see which findings
came from the detector without the workflow depending on that distinction.

Analysis without `replace` answers with the capture's existing findings instead
of running the detector again, so the automatic pass and a re-opened workspace do
not accumulate duplicates. `replace=true` is the explicit re-run: it runs the
detector again and swaps the capture's **undecided** findings for the new
result, while findings the Inspector already confirmed survive. Detections are produced before the previous
suggestions are removed, so a detector failure leaves them in place, and a re-run
that finds nothing leaves the capture with no suggestions rather than stale ones
from the previous detector.

When the detector answers, the adapter posts raw eligible image bytes with their
media type to `YOLO_INFERENCE_BASE_URL` plus `YOLO_INFERENCE_PREDICT_PATH`
(default `/predict`), and expects detections in its documented array contract. The
service in `ai-inference/` serves the YOLO11s model trained on MBDD2025 and
answers that contract; compose runs it as the `ai-inference` service, and the
backend reaches it at `http://ai-inference:8000`.

When the vision option answers, it sends the
image as a MIME-aware base64 data URI to `<COMPATIBLE_VISION_BASE_URL>/v1/chat/completions`,
sets `stream:false`, and asks for a JSON `detections` object. Configure
`COMPATIBLE_VISION_MODEL`, `COMPATIBLE_VISION_API_KEY`, and
`COMPATIBLE_VISION_TIMEOUT`; the key is supplied from the local environment and
must not be committed. The adapter validates the label, confidence in `[0,1]`,
and normalized `xMin`, `yMin`, `xMax`, `yMax` coordinates in `[0,1]` with
positive box dimensions. Candidates retain the configured model alias and the
provider-reported model version, so a finding records which detector produced
it. These adapters provide advisory suggestions
only; they do not make an AI result an official finding.

Analysis is refused until the Inspector accepts the evidence. An inference
failure returns `503 AI_INFERENCE_UNAVAILABLE` and the manual finding path
stays available. A finding becomes official only when the assigned Inspector confirms it;
the Organization Admin later approves or returns the whole report rather than deciding each finding.
Undecided findings never enter report snapshots.

Confirming a finding the Inspector already confirmed is refused with
`409 FINDING_ALREADY_CONFIRMED`: the confirmation is a statement about the content, so
the content cannot move underneath a decision that was already made. Editing a finding
takes the confirmation back, and the Inspector confirms it again.

Removing a finding hides it from the working set rather than erasing it. The row stays
for audit, reads filter it out, and `GET /findings/removed` lists what was removed.
`POST /findings/{findingId}/restore` brings one back, so a removal made by mistake is
recoverable.

## Report authoring, review and publication (FE-06, MF3-07 to MF3-13)

| Operation | Endpoint | Actor |
| --- | --- | --- |
| Generate AI draft | `POST /api/v1/inspections/{inspectionId}/report/draft` | assigned Inspector |
| Author manual draft | `POST /api/v1/inspections/{inspectionId}/report/draft/manual` | assigned Inspector |
| List versions | `GET /api/v1/inspections/{inspectionId}/report/versions` | assigned Inspector, same-org ORG_ADMIN |
| Read version and source-backed report context | `GET /api/v1/inspections/{inspectionId}/report/versions/{versionId}` | assigned Inspector, same-org ORG_ADMIN |
| Verify as author | `POST /api/v1/inspections/{inspectionId}/report/versions/{versionId}/verify` | assigned Inspector |
| Submit for review | `POST /api/v1/inspections/{inspectionId}/report/versions/{versionId}/submit` | assigned Inspector |
| Withdraw submission | `POST /api/v1/inspections/{inspectionId}/report/versions/{versionId}/withdraw` | assigned Inspector |
| Review | `POST /api/v1/inspections/{inspectionId}/report/versions/{versionId}/review[?approve=...&reason=...&reasonType=...]` | independent same-org ORG_ADMIN (report-level decision) |
| Publish | `POST /api/v1/inspections/{inspectionId}/report/versions/{versionId}/publish` | independent same-org ORG_ADMIN |
| Record per-finding corrective outcome | `PUT /api/v1/inspections/{inspectionId}/findings/{findingId}/corrective-action` | ORG_ADMIN |
| Record corrective handoff | `POST /api/v1/inspections/{inspectionId}/report/corrective-handoff` | ORG_ADMIN |
| Declare no corrective work | `POST /api/v1/inspections/{inspectionId}/report/no-corrective-work` | ORG_ADMIN |

Version status moves `DRAFT` → `AUTHOR_VERIFIED` → `SUBMITTED` → (`RETURNED` |
`APPROVED`) → `PUBLISHED` → `SUPERSEDED`.

"Independent" means the runtime validates role, organization, active account and
separation of duties (the author cannot review). Reviewer credential or
professional-qualification checks do not exist at runtime, so a report approval
recorded here is an Organization Admin decision, not proof of professional qualification. There is no per-finding Admin decision endpoint.

**Manual authoring is required, not optional.** Report 3 states that failed LLM
generation permits the author to complete a structured manual draft with the
same review gates. `POST /report/draft` therefore reports
`503 REPORT_DRAFT_UNAVAILABLE` when no `ReportDraftPort` is configured, and the
author uses `POST /report/draft/manual` with `narrative` (required) and an
optional `omissionDisclosure` recording which analysis was omitted. The manual
version records `llmModel` as `manual-authoring`, so a reader can tell that the
narrative is the author's own.

The report-version response includes read-only, organization-scoped identity labels and recorded Drone, preparation/readiness, evidence-quality, field-session and findings-confirmation context. The same source records are composed into the PDF where present; missing session/checklist rows do not produce boilerplate that claims they exist. The session pre-flight note is persisted by V35 and is rendered as an Inspector-entered note, not proof that a checklist or flight was completed. Item-level checklist responses are included only when stored against the inspection and linked to the relevant session checklist template. This response context is not a qualification, permit-clearance or aircraft-operation verification.

Drafting moves the inspection from `FIELD_COMPLETED` to `REPORT_DRAFT`.
Publication requires that state and moves the inspection to `REPORT_PUBLISHED`
only; it stores and checksums the PDF. Forwarding findings to Maintenance occurs
afterwards:

1. **Forward to Maintenance** — after report publication, `POST .../report/corrective-handoff`
   accepts `findingIds` (confirmed findings selected to forward as repair candidates). All
   confirmed defect findings are selected by default; the administrator may deselect items to
   postpone. No per-finding rationales, priorities or due dates are required during report review.
   Forwarded findings transition the inspection to `REPAIR_PENDING` and enter the Maintenance
   candidates inbox (`/repair-candidates`); deselecting all items leaves the report published
   without handoff, allowing forward later.
2. **No-repair close** — for an inspection with no confirmed defect findings,
   `POST .../report/no-corrective-work` records the reviewer's explicit rationale and moves
   the inspection to `COMPLETED`.

Separation of duties is enforced twice. Only the assigned Inspector may author
or verify, and only a same-organization `ORG_ADMIN` who is not the author may
review or publish; the author is refused with `REPORT_SCOPE_DENIED` or
`REPORT_REVIEWER_INVALID`. A return requires a non-blank `reason` and returns the
version to the author, who must verify and submit again before it can be
approved.

Listing versions for an inspection that has no report returns an empty list
rather than a missing-resource failure, because "no report yet" is the normal
state before an author drafts one.

A repeated corrective outcome or handoff is refused with
`409 CORRECTIVE_ACTION_ALREADY_RECORDED` or
`409 CORRECTIVE_HANDOFF_ALREADY_COMPLETED`, so the published outcome chain
cannot be silently rewritten.

## Verification records

`InspectionReportVersionTest` and `AiFindingCandidateTest` cover the version
state machine and candidate review states.
`InspectionEvidenceApiIntegrationTest` and
`InspectionReportApiIntegrationTest` contain assertions for MF3-01 through
MF3-13 over the real HTTP surface, including the manual authoring path, the
return/resubmit cycle, self-review refusal, the full draft-to-publish sequence,
and the post-publication corrective-outcome/handoff/no-repair paths. These
tests executed green on 2026-10-16: the five named MF3 suites passed 81 tests
(12/11/26/10/22) with zero failures, and the full `.\mvnw.cmd verify` gate passed
650 tests with the Spotless, JaCoCo and Modulith checks met.
`InspectionListApiIntegrationTest`
covers the collections: assignment scope for an Inspector, organization scope
for an ORG_ADMIN, cross-tenant read for a platform `ADMIN`, refusal for
`MAINTENANCE_ENGINEER`, the report-only filter, the inline report summary, and
paging bounds. MF2 service and API coverage includes
`InspectionReadinessServiceTest`, `ReadinessSnapshotFactoryTest`,
`InspectionReadinessApiIntegrationTest`, `InspectionPreparationApiIntegrationTest`,
and the field-session service/API tests. The complete backend PR #64 CI run
passed 334 tests with no failures/errors/skips, and the JaCoCo/Modulith checks
passed; it predates the MF3-12/13 change. Report 5 records
`WF2-008`/`WF2-009` for MF2-07 on `Feature 3`, the MF3 cases on `Feature 4`–`Feature 6`,
plus the new Pending `WF3-012` for MF3-12/13; session end and source-change
invalidation remain uncovered as noted above.
### Added contracts (2026-10-22)

- Bilingual system-managed content follows the requested locale, with English as the explicit default and fallback. `GET /api/v1/inspections/{inspectionId}/checklist` and `PUT /api/v1/inspections/{inspectionId}/checklist-responses/{checklistItemId}` are Inspector-only routes; the checklist's section, prompt and guidance are read in the requested locale, while the Inspector's answer value, note and completion time are returned exactly as recorded.
- `V39__add_vietnamese_checklist_content.sql` adds nullable Vietnamese columns to `checklist_templates` and `checklist_items`. The migration is additive: existing checklist content is unchanged, and a localized read falls back to the English columns when no Vietnamese value is recorded. The columns are read-only in this release: no API writes a Vietnamese checklist value yet, and the repository ships no checklist seed data, so checklist content currently reads as English in either locale.
- The AI drafting prompt is written in the requested language and instructs the model to preserve supplied source values verbatim, so an Inspector-authored note is never translated or paraphrased into the draft. The recorded prompt version moves to `mf3-report-v3-bilingual`.
- The generated report document renders its system-managed labels, headings and page furniture in the requested locale. Authored narrative sections, finding text and recorded notes are embedded unchanged.

### Added contracts (2026-10-18)

- Evidence upload response includes `deduplicated`. Same inspection + same SHA-256 active retry returns the existing row with `deduplicated=true`; a matching retired audit copy returns `409 EVIDENCE_DUPLICATE_RETIRED`. Filename alone is not duplicate identity.
- `PUT /api/v1/inspections/{inspectionId}/evidence/{evidenceId}/location` is assigned-Inspector-only; it saves one shared asset-area location on evidence and propagates it to linked findings.
- `PUT /api/v1/auth/me/ai-fallback-preference` is Inspector-only and persists `visionFallbackEnabled`; default is enabled. YOLO remains primary, a valid empty result does not fall back, and the configured vision model is attempted only after detector failure when the Inspector preference is enabled.
- `V33__mf3_evidence_locations_and_inspector_ai_preferences.sql` adds the evidence location, Inspector confirmation timestamp and per-user fallback preference; old reviewer decision columns remain readable for historical compatibility.
