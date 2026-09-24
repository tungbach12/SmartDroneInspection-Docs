# WF3 API and Handoff Contract

**Scope**: SCRUM-85–SCRUM-93 / FE-04–FE-06.<br>
**Status**: Reconciled against the current `/api/v1` clients and the existing Inspector-only `InspectionController`.<br>
**Authority**: The backend derives user, organization, asset, uploader, assignment, report author, and workflow scope from the authenticated principal and scoped resource lookup. Clients never submit those authority fields.

## Existing FE-04 contract (unchanged)

| Operation | Contract |
| --- | --- |
| List accepted assignments | `GET /api/v1/inspections/assignments?status=ACCEPTED`; active authenticated Inspector only. |
| Start/resume inspection | `POST /api/v1/inspections/start` with `{ assignmentId }`; an accepted assignment returns the existing inspection on retry. |
| Read checklist and saved responses | `GET /api/v1/inspections/{inspectionId}/checklist`; the active accepted assignee only; returns published checklist items, validation configuration, and current saved response/notes. |
| Save checklist response | `PUT /api/v1/inspections/{inspectionId}/checklist-responses/{checklistItemId}`; item/template and author scope are checked and the actor is server-attributed. |

See the [existing start/checklist contract](../../2026-09-22-week-3-wf3-inspection-delivery/contracts/w3-inspection-start-and-checklist.md). The existing controller is class-level `INSPECTOR`; Client, Manager, and reviewer APIs therefore use a separate report controller with per-operation role and resource checks.

## FE-04 evidence operations

| Operation | Contract |
| --- | --- |
| Upload evidence | `POST /api/v1/inspections/{inspectionId}/evidence` (`multipart/form-data`, `file` required; metadata fields `source`, `captureTime`, `latitude`, `longitude`, `externalReference`). Accepted active assignee only; supported content is validated before storage; SHA-256 is server-computed; identical inspection/checksum returns the existing resource. |
| List metadata | `GET /api/v1/inspections/{inspectionId}/evidence`; scoped Inspector access only; returns `AVAILABLE` evidence, never a bucket/object URL. |
| Stream content | `GET /api/v1/inspections/{inspectionId}/evidence/{evidenceId}/content`; verifies inspection/evidence relationship and assignment, then streams via the backend. |

Uploader, organization, inspection/asset ownership, checksum, object key, and upload state are server-owned. Web sends `WEB_UPLOAD`; Mobile sends `MOBILE_UPLOAD`; the other accepted values are `SD_CARD` and `IMPORTED`. Missing GPS is valid; latitude and longitude are either both present or both absent. Content limits are configured on the server and must follow the SRS/deployment setting rather than a client-provided value.

## FE-05 candidate and finding operations

| Operation | Contract |
| --- | --- |
| List candidates | `GET /api/v1/inspections/{inspectionId}/finding-candidates`; assigned active Inspector only. Pending/rejected candidates remain advisory. |
| Analyze/retry an image | `POST /api/v1/inspections/{inspectionId}/evidence/{evidenceId}/analyze`; assigned active Inspector only. The optional adapter is disabled by default and is configured by `YOLO_INFERENCE_ENABLED`, `YOLO_INFERENCE_BASE_URL`, `YOLO_INFERENCE_PREDICT_PATH`, and connect/read timeouts. It posts raw image bytes with the image media type and expects JSON detection objects (`modelName`, `modelVersion`, `predictedLabel`, `confidence`, `boundingBox`). An eligible image may produce zero or more candidates; an AI outage returns a stable unavailable error and does not change evidence availability. Upload itself succeeds independently of AI. |
| Review candidate | `POST /api/v1/inspections/{inspectionId}/finding-candidates/{candidateId}/review` with decision `CONFIRM`, `MODIFY`, or `REJECT`. `MODIFY` supplies verified label, severity, location, technical notes and optional recommendation; `REJECT` requires a reason. |
| Add manual finding | `POST /api/v1/inspections/{inspectionId}/findings` with required classification, severity, location, and technical notes; source is set to `MANUAL` by the server. |

Only confirmed/modified AI candidates and manual findings create official verified findings. Candidate provenance includes model name/version, predicted label, confidence in `[0,1]`, and bounding box. AI failure never blocks evidence reads or manual entry.

## FE-06 report operations

| Operation | Contract |
| --- | --- |
| List visible reports | `GET /api/v1/reports`; server filters by role: author/reviewer scope for Inspectors, service workflow for Managers, and own-organization released/accepted reports for Clients. |
| Read report | `GET /api/v1/reports/{reportId}`; same role and resource-scope rules. Client response excludes drafts and internal review comments. |
| Create/read initial draft | `POST` / `GET /api/v1/inspections/{inspectionId}/report`; author only for writes; POST is idempotent for initial creation and snapshots checklist, available evidence metadata, and verified findings. |
| Create revision | `POST /api/v1/reports/{reportId}/versions`; report author creates a new linked snapshot; older and accepted versions are never overwritten. |
| Assign reviewer | `PUT /api/v1/reports/{reportId}/versions/{versionId}/reviewer` with `{ reviewerId }`; active Service Manager only; reviewer must be a distinct active Inspector. |
| Submit version | `POST /api/v1/reports/{reportId}/versions/{versionId}/submit-review`; report author only, complete version with reviewer already assigned. |
| Record peer decision | `POST /api/v1/reports/{reportId}/versions/{versionId}/review` with `CHANGES_REQUESTED` or `APPROVED`; assigned reviewer only, never the author. |
| Release version | `POST /api/v1/reports/{reportId}/versions/{versionId}/release`; Service Manager only, after approval and completeness checks. |
| Client decision | `POST /api/v1/reports/{reportId}/versions/{versionId}/client-decision` with `ACCEPT` or `REQUEST_REVISION`; owning Client organization only. Acceptance locks that version and publishes one `ReportAcceptedEvent`; revision requests require a reason. `clientDecisionByUserId` and `clientDecisionReason` are persisted on the version. |
| Stream released evidence | `GET /api/v1/reports/{reportId}/versions/{versionId}/evidence/{evidenceId}/content`; Client can read only evidence linked to that released version and own organization. Other roles use the ordinary inspection-scoped endpoint. |

Report responses include report/version identifiers, inspection/asset context, lifecycle status, snapshot, and review assignment/decision as allowed to the caller. Internal peer comments and unreleased content are omitted from Client responses.

## Payload and error rules

- Reuse RFC 7807 `ProblemDetail`; response bodies never reveal stack traces, object keys, tokens, or protected evidence.
- Existing codes remain: `INSPECTION_SCOPE_DENIED`, `INSPECTION_NOT_FOUND`, `INSPECTION_STATE_CONFLICT`, and `CHECKLIST_RESPONSE_INVALID`.
- New stable codes: `EVIDENCE_INVALID`, `EVIDENCE_TOO_LARGE`, `EVIDENCE_STORAGE_UNAVAILABLE`, `EVIDENCE_NOT_FOUND`, `AI_INFERENCE_UNAVAILABLE`, `AI_CANDIDATE_NOT_FOUND`, `FINDING_INVALID`, `REPORT_SCOPE_DENIED`, `REPORT_NOT_FOUND`, `REPORT_STATE_CONFLICT`, and `REPORT_REVIEWER_INVALID`.
- A duplicate checksum is a successful idempotent upload response, not an error. Invalid/corrupt/unsupported media fails before it is exposed. A failed MinIO write or metadata transaction never returns `AVAILABLE` evidence.

## Accepted-report handoff

Client acceptance emits one transactional `ReportAcceptedEvent` containing `reportId`, `reportVersionId`, `inspectionId`, `organizationId`, `assetId`, `acceptedByUserId`, and `acceptedAt`. It contains no evidence bytes or secrets. Repeated acceptance of the same version returns the existing accepted state and does not publish another handoff. WF4/billing consumes the event through the existing Spring Modulith publication registry; this WF3 scope does not implement invoice persistence or payment processing.
