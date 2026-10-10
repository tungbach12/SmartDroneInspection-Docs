---
title: "MF3 Inspection, Evidence and Report Runtime Flow"
weight: 40
---

# MF2/MF3 Inspection, Preparation and Report Runtime Flow

This describes the implemented Report 3 MF2 slice and MF3 workflow inside the
`inspections` Spring Modulith module. Roles are the four Enterprise SaaS roles:
`ADMIN`, `ORG_ADMIN`, `INSPECTOR`, `MAINTENANCE_ENGINEER`. The assigned
Inspector is the human report author; AI is advisory only. MF2-08 source-change
invalidation is partial; MF2-12 session end and `FIELD_COMPLETED` handoff are
not implemented.

Access is decided by the authenticated principal and scoped lookups, never by
client-supplied user, organization, owner, or assignment identifiers. Write
operations require the *assigned* Inspector; read and review operations also
allow a same-organization `ORG_ADMIN`.

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
and is permitted only while the inspection is `PREPARING`.

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

## Field sessions (FE-03, MF2-09/11; partial handoff)

An assigned active `INSPECTOR` may list their sessions, start a session, record
postponement, or abort an open session. Start requires an inspection in
`READY_FOR_FLIGHT`, a non-blank pre-flight checklist note, no other open session,
and the newest readiness decision to be `APPROVED`. Start records a software
session and moves the inspection to `IN_PROGRESS`; it never actuates or pilots
the Drone. Postponement reopens the inspection to `READY_FOR_FLIGHT`; abort
records the abort but leaves the inspection `IN_PROGRESS`.

The `INVALIDATED` readiness decision type exists, and start checks the newest
decision so an appended invalidation would prevent reuse of an older approval.
However, no source-change workflow currently appends `INVALIDATED`; that part of
MF2-08 is partial. There is no session-end route to close an aborted/started
session or transition the inspection to `FIELD_COMPLETED`; MF2-12 remains
unimplemented.

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

| Operation | Endpoint | Actor |
| --- | --- | --- |
| Upload evidence | `POST /api/v1/inspections/{inspectionId}/evidence` | assigned Inspector, same-org ORG_ADMIN |
| List evidence | `GET /api/v1/inspections/{inspectionId}/evidence` | assigned Inspector, same-org ORG_ADMIN |
| Stream evidence | `GET /api/v1/inspections/{inspectionId}/evidence/{evidenceId}/content` | assigned Inspector, same-org ORG_ADMIN |

Multipart fields are `file` (required), `source`
(`SD_CARD`|`WEB_UPLOAD`|`MOBILE_UPLOAD`|`IMPORTED`, default `WEB_UPLOAD`),
`captureTime`, `latitude`, `longitude`, `externalReference`.

Accepted content types are `image/png`, `image/jpeg`, `image/webp`,
`image/tiff`, `video/mp4`, `application/pdf`. The service caps a file at 50 MB;
`EVIDENCE_MAX_FILE_SIZE` (default `1MB`) and `EVIDENCE_MAX_REQUEST_SIZE`
(default `10MB`) cap the container request, so the effective limit is the
smaller of the two.

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

## AI candidates and verified findings (FE-05, MF3-05/06/09)

| Operation | Endpoint | Actor |
| --- | --- | --- |
| List candidates | `GET /api/v1/inspections/{inspectionId}/finding-candidates` | assigned Inspector, same-org ORG_ADMIN |
| Analyze evidence | `POST /api/v1/inspections/{inspectionId}/evidence/{evidenceId}/analyze` | assigned Inspector |
| Review candidate | `POST /api/v1/inspections/{inspectionId}/finding-candidates/{candidateId}/review` | assigned Inspector |
| List findings | `GET /api/v1/inspections/{inspectionId}/findings` | assigned Inspector, same-org ORG_ADMIN |
| Add manual finding | `POST /api/v1/inspections/{inspectionId}/findings` | assigned Inspector |
| Record finding decision | `POST /api/v1/inspections/{inspectionId}/findings/{findingId}/decision` | same-org ORG_ADMIN |

AI is optional. Both `YOLO_INFERENCE_ENABLED` and `COMPATIBLE_VISION_ENABLED`
default to `false`; configure at most one provider. When YOLO is selected, the
adapter posts raw eligible image bytes with their media type to
`YOLO_INFERENCE_BASE_URL` plus `YOLO_INFERENCE_PREDICT_PATH` (default
`/predict`). The YOLO endpoint returns detections in its documented array
contract. When the OpenAI-compatible vision provider is selected, it sends the
image as a MIME-aware base64 data URI to `<COMPATIBLE_VISION_BASE_URL>/v1/chat/completions`,
sets `stream:false`, and asks for a JSON `detections` object. Configure
`COMPATIBLE_VISION_MODEL`, `COMPATIBLE_VISION_API_KEY`, and
`COMPATIBLE_VISION_TIMEOUT`; the key is supplied from the local environment and
must not be committed. The adapter validates the label, confidence in `[0,1]`,
and normalized `xMin`, `yMin`, `xMax`, `yMax` coordinates in `[0,1]` with
positive box dimensions. Candidates retain the configured model alias and the
provider-reported model version. These adapters provide advisory suggestions
only; they do not make an AI result an official finding.

Analysis is refused until the Inspector accepts the evidence. An inference
failure returns `503 AI_INFERENCE_UNAVAILABLE` and the manual finding path
stays available. Only a `CONFIRMED` or `MODIFIED` decision makes a finding
official; pending and rejected candidates never enter report snapshots. A
rejected candidate returns `204 No Content`.

## Report authoring, review and publication (FE-06, MF3-07 to MF3-13)

| Operation | Endpoint | Actor |
| --- | --- | --- |
| Generate AI draft | `POST /api/v1/inspections/{inspectionId}/report/draft` | assigned Inspector |
| Author manual draft | `POST /api/v1/inspections/{inspectionId}/report/draft/manual` | assigned Inspector |
| List versions | `GET /api/v1/inspections/{inspectionId}/report/versions` | assigned Inspector, same-org ORG_ADMIN |
| Read version | `GET /api/v1/inspections/{inspectionId}/report/versions/{versionId}` | assigned Inspector, same-org ORG_ADMIN |
| Verify as author | `POST /api/v1/inspections/{inspectionId}/report/versions/{versionId}/verify` | assigned Inspector |
| Submit for review | `POST /api/v1/inspections/{inspectionId}/report/versions/{versionId}/submit` | assigned Inspector |
| Review | `POST /api/v1/inspections/{inspectionId}/report/versions/{versionId}/review` | qualified same-org ORG_ADMIN |
| Publish | `POST /api/v1/inspections/{inspectionId}/report/versions/{versionId}/publish` | qualified same-org ORG_ADMIN |

Version status moves `DRAFT` → `AUTHOR_VERIFIED` → `SUBMITTED` → (`RETURNED` |
`APPROVED`) → `PUBLISHED` → `SUPERSEDED`.

**Manual authoring is required, not optional.** Report 3 states that failed LLM
generation permits the author to complete a structured manual draft with the
same review gates. `POST /report/draft` therefore reports
`503 REPORT_DRAFT_UNAVAILABLE` when no `ReportDraftPort` is configured, and the
author uses `POST /report/draft/manual` with `narrative` (required) and an
optional `omissionDisclosure` recording which analysis was omitted. The manual
version records `llmModel` as `manual-authoring`, so a reader can tell that the
narrative is the author's own.

Drafting moves the inspection from `FIELD_COMPLETED` to `REPORT_DRAFT`.
Publication requires that state and then moves the inspection to
`REPORT_PUBLISHED`, and finally to `REPAIR_PENDING` or `COMPLETED`.

Separation of duties is enforced twice. Only the assigned Inspector may author
or verify, and only a same-organization `ORG_ADMIN` who is not the author may
review or publish; the author is refused with `REPORT_SCOPE_DENIED` or
`REPORT_REVIEWER_INVALID`. A return requires a non-blank `reason` and returns the
version to the author, who must verify and submit again before it can be
approved.

Listing versions for an inspection that has no report returns an empty list
rather than a missing-resource failure, because "no report yet" is the normal
state before an author drafts one.

Publication emits `ReportPublishedEvent` carrying the confirmed repair-required
finding IDs. An empty list means no corrective work was required within the
observed scope and the inspection completes; it never creates an empty work
order.

## Verification records

`InspectionReportVersionTest` and `AiFindingCandidateTest` cover the version
state machine and candidate review states.
`InspectionEvidenceApiIntegrationTest` and
`InspectionReportApiIntegrationTest` exercise MF3-01 through MF3-13 over the
real HTTP surface, including the manual authoring path, the return/resubmit
cycle, self-review refusal, and the full draft-to-publish sequence.
`InspectionListApiIntegrationTest` covers the collections: assignment scope for
an Inspector, organization scope for an ORG_ADMIN, cross-tenant read for a
platform `ADMIN`, refusal for `MAINTENANCE_ENGINEER`, the report-only filter,
the inline report summary, and paging bounds. MF2 service and API coverage
includes `InspectionReadinessServiceTest`, `ReadinessSnapshotFactoryTest`,
`InspectionReadinessApiIntegrationTest`, `InspectionPreparationApiIntegrationTest`,
and the field-session service/API tests. The complete backend PR #64 CI run
passed 334 tests with no failures/errors/skips, and the JaCoCo/Modulith checks
passed. Report 5 records `WF2-008`/`WF2-009` for MF2-07 on `Feature 3`, and the
MF3 cases on `Feature 4`–`Feature 6`; session end and source-change invalidation
remain uncovered as noted above.