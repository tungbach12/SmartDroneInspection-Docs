---
title: "MF3 Inspection, Evidence and Report Runtime Flow"
weight: 40
---

# MF3 Inspection, Evidence and Report Runtime Flow

This describes the implemented Report 3 MF3 workflow inside the `inspections`
Spring Modulith module. Roles are the four Enterprise SaaS roles: `ADMIN`,
`ORG_ADMIN`, `INSPECTOR`, `MAINTENANCE_ENGINEER`. The assigned Inspector is
the human report author; AI is advisory only.

Access is decided by the authenticated principal and scoped lookups, never by
client-supplied user, organization, owner, or assignment identifiers. Write
operations require the *assigned* Inspector; read and review operations also
allow a same-organization `ORG_ADMIN`.

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

## MF2 preparation and readiness (FE-03, MF2-03 to MF2-07)

These routes live in the same `inspections` module but a separate controller
from MF3, because the two actors are different: an `INSPECTOR` prepares and
submits, an `ORG_ADMIN` decides.

| Operation | Endpoint | Actor |
| --- | --- | --- |
| List preparation versions | `GET /api/v1/inspections/{id}/preparation` | assigned Inspector |
| Get one preparation version | `GET /api/v1/inspections/{id}/preparation/{prepId}` | assigned Inspector |
| Record shot-list, evidence types, access limits, hazards | `PUT /api/v1/inspections/{id}/preparation` | assigned Inspector |
| Submit the preparation | `POST /api/v1/inspections/{id}/preparation/{prepId}/submission` | assigned Inspector |
| Link issued permit references | `POST /api/v1/inspections/{id}/preparation/compliance/permits` | same-org ORG_ADMIN |
| Evaluate the compliance gate | `GET /api/v1/inspections/{id}/preparation/compliance` | same-org ORG_ADMIN |
| Approve readiness | `POST /api/v1/inspections/{id}/readiness/{prepId}/approval` | same-org ORG_ADMIN |
| Return the preparation | `POST /api/v1/inspections/{id}/readiness/{prepId}/return` | same-org ORG_ADMIN |
| Reviewer's own credentials | `GET /api/v1/workforce/credentials/me` | same-org ORG_ADMIN |
| Review sources for an inspection | `GET /api/v1/inspections/{id}/readiness/sources` | same-org ORG_ADMIN |

The readiness body carries **no reviewer identity and no organization**. The
reviewer is taken from the authenticated principal, and organization, subject
ownership, credential scope and pair scope are re-derived server-side. A body
that carried `reviewedByUserId` would let a caller record a decision in someone
else's name, and a body that carried an organization id would let a caller
review another tenant's inspection.

**Where the reviewer's credential and the source ids come from.** The approval
body names `reviewerCredentialId`, `inspectorCredentialIds` and `droneDocumentIds`.
A client cannot invent any of them, so two read routes supply them:
`GET /api/v1/workforce/credentials/me` returns the caller's own credentials, and
`GET /api/v1/inspections/{id}/readiness/sources` returns the assigned Inspector's
credentials and the assigned Drone's documents. Without them the only way to approve
over HTTP would be to type UUIDs, which is not a workflow anyone completes. Both are
`ORG_ADMIN`, same-organization, and return metadata rather than document content;
`backend/authentication-and-authorization.md` records the scope rule and why it is
that narrow.

Approval is refused unless every gate passes: reviewer independence from the
assigned Inspector, an `ACTIVE` internally verified credential with source
evidence covering planned start, matching valid accepted pair, serviceable
Drone, reviewed Drone documents with verification attribution, a complete
applicability attestation with a traceable basis, and no machine-detectable
permit blocker. An empty credential or document selection is allowed but must be
explained, so "nothing applies" is a recorded judgement rather than an omission.

A compliance blocker arrives as `200` carrying the blocker list, not as an
error status: MF2-07 needs every blocker at once, and an empty list still means
a named human has to decide.

**Cross-tenant refusal is `404` with an `*_NOT_FOUND` code, not `403`.** A `403`
would confirm that an inspection with that id exists, so the readiness routes
follow the same rule as the report-review routes.

### What is not implemented yet

MF2-08 says a material plan, pair, permit or schedule change invalidates
readiness. The invalidation itself is **not** performed by any service today: there is no producer
that writes an `INVALIDATED` decision when a source changes. What exists is the reading side, and
the start check refuses anything but a currently approved decision.

The schema was already designed for this. `ck_inspection_readiness_decision` allows `INVALIDATED`
and `database-design.md` describes the table as append-only, so MF2-08 records invalidation by
appending a decision rather than editing the approval. That keeps the approval a reviewer actually
signed, and makes the withdrawal an attributable act of its own.

| Area | State |
| --- | --- |
| Reading an invalidated decision at session start | implemented; `InspectionFieldSessionService` |
| Writing an `INVALIDATED` decision when a source changes | **not implemented** — no writer exists |

The reason there is no writer is that nothing can currently change a readiness source after a
decision. The accepted-pair requirement means an Inspector cannot decline a pairing that has already
been approved, a `READY` preparation refuses new permit references, and permits, credentials and
Drone documents have no production writer. Adding an invalidation column before a producer exists
would be state nothing sets.

## Field sessions (FE-03, MF2-09 to MF2-11)

`InspectionFieldSessionController` exposes the field session. Only `INSPECTOR` reaches these routes.

| Operation | Endpoint | Actor |
| --- | --- | --- |
| List this inspection's sessions | `GET /api/v1/inspections/{id}/field-sessions` | assigned Inspector |
| Start a session | `POST /api/v1/inspections/{id}/field-sessions` | assigned Inspector |
| Postpone the session | `POST /api/v1/inspections/{id}/field-sessions/{sessionId}/postponement` | assigned Inspector |
| Abort the session | `POST /api/v1/inspections/{id}/field-sessions/{sessionId}/abort` | assigned Inspector |

An `ORG_ADMIN` may approve readiness and read the compliance gate, but the field session is the
Inspector's own record of work they performed, so the administrator cannot start or close one on their
behalf. A *different* Inspector in the same organization receives `409 SESSION_SCOPE_DENIED`: the
session exists and belongs to this tenant, so the refusal is about ownership, not visibility. `403` is
reserved for the wrong role.

The list is scoped to the caller rather than the organization, so an Inspector sees their own field
work and not a colleague's. A caller from another organization receives `404 INSPECTION_NOT_FOUND`
rather than an empty list, because an empty list would confirm the inspection exists.

Postponement and abort take the inspection id as well as the session id and look the session up
through both. A session id alone would let a caller close a session through a different inspection's
URL, and the scope check would then look at the wrong record — the same mistake the preparation
submission route guards against.

**Start rechecks readiness rather than trusting it.** MF2-07's approval is a statement about a source
basis at one instant. At start the service re-reads the newest decision for the inspection and refuses
unless that decision is `APPROVED`, so an `INVALIDATED` or `RETURNED` decision that was appended
later wins over an older approval. The inspection must still be `READY_FOR_FLIGHT` and the caller
must be its assigned Inspector.

A session records the `readiness_decision_id` it started against. That is what makes a later audit
answer "which approval did this flight rely on" rather than "some approval, at some point".

The pre-flight note is required, and it is prose rather than a checkbox flag: a boolean a client sets
automatically would attest to nothing. Over HTTP a blank note is a `400` from bean validation; the
same condition called on the service directly is `409 PREFLIGHT_CHECKLIST_REQUIRED`.

**A postponement returns the inspection to `READY_FOR_FLIGHT`.** Weather and site safety can stop a
correctly approved session, and the approval was not consumed by trying, so the same inspection may
be started again once conditions allow. **An abort does not.** An abort leaves the inspection in
progress, because an aborted session is not the same as one that never got going, and it carries an
abort reason rather than a postponement reason.

No Drone actuation happens here. Start records that the software agreed the paperwork and the
checklist were in order; it does not arm the aircraft, and `started_at` is not hardware flight time.

Lock ordering is inspection-first, the same order the preparation and readiness services use, so a
start cannot interleave with a preparation submission or a readiness decision on the same inspection.

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
the inline report summary, and paging bounds. Report 5 records the outcomes for
`WF3-001`–`WF3-004` on the fixed `Feature 2` sheet and for the target MF3 rows.

For MF2, `InspectionReadinessServiceTest` and `ReadinessSnapshotFactoryTest`
cover the MF2-07 decision rules, the deterministic source snapshot and its
hash, and every refusal path against PostgreSQL.
`InspectionPreparationApiIntegrationTest` covers the MF2-03 to MF2-06 endpoints
over HTTP, including the role separation between the two actors and the
compliance blocker list arriving as `200`.
`InspectionReadinessApiIntegrationTest` covers the two readiness endpoints:
approval and return by a qualified reviewer, a blank return reason, an empty
applicability attestation, an Inspector refused at the filter chain, an
unauthenticated caller, and a cross-tenant reviewer receiving
`404 INSPECTION_NOT_FOUND`. Report 5 records `WF2-008` and `WF2-009` on the
fixed `Feature 1` sheet.

`InspectionFieldSessionServiceTest` covers MF2-09 to MF2-11: a start against the
current approved decision, the decision id recorded on the session, refusal with
no decision or an invalidated one, an inspection no longer ready for flight,
another Inspector and another organization refused, a blank pre-flight note, a
duplicate start, postponement with its reason returning the inspection to
`READY_FOR_FLIGHT`, a blank postponement reason, another Inspector unable to
postpone, an abort recording its own reason and leaving the inspection in
progress, a blank abort reason, a restart after a postponement, the list returning
only the caller's own sessions, and a session that belongs to another inspection
being refused. `InspectionFieldSessionApiIntegrationTest` covers the same rules
over HTTP, including the role split between an Inspector and an ORG_ADMIN.

They have no workbook case yet.