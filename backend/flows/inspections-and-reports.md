---
title: "WF3 Inspection and Report Runtime Flow"
weight: 40
---

# Historical WF3 Inspection and Report Runtime Flow

> **Status as of 7 October 2026, `feat/enterprise-saas-reset`: historical and non-authoritative.** The detailed endpoint, service and verification descriptions below refer to the earlier v1 inspection runtime and are retained only as a record of the prior implementation/test baseline. The reset removed the inspection workflow controllers and services and their workflow tests; remaining inspection entities/repositories and V24/V25 migration structures provide persistence/schema only, not runtime workflow behavior. Do not treat any endpoint below as currently available. The current Enterprise SaaS target uses four roles and MF1–MF4, but this reset does not implement those workflow behaviors; see Report 3 and the database design. Historical Report 5 results remain evidence of the version that was actually tested, not of this reset branch.

The removed v1 WF3 behavior was previously implemented inside the `inspections` Spring Modulith module. The endpoint and service details below are a historical snapshot, not a current API contract. In that earlier runtime, the authenticated backend principal and scoped resource lookups—not client-supplied user, organization, owner, or assignment IDs—decided access.

## Inspection, checklist, and evidence (FE-04)

The Inspector must have an active accepted assignment for each inspection
operation. The inspection controller additionally requires the `INSPECTOR`
role. A checklist read returns published items, validation configuration, and
the current saved response/notes; response writes remain scoped to that
inspection and checklist item.

| Operation | Endpoint | Behavior |
| --- | --- | --- |
| List accepted assignments | `GET /api/v1/inspections/assignments?status=ACCEPTED` | Returns the signed-in Inspector's accepted assignments. |
| Start/resume | `POST /api/v1/inspections/start` | Idempotently starts or returns the inspection for the accepted assignment. |
| Read checklist | `GET /api/v1/inspections/{inspectionId}/checklist` | Returns published checklist items and saved responses for the assigned Inspector. |
| Save response | `PUT /api/v1/inspections/{inspectionId}/checklist-responses/{checklistItemId}` | Validates item membership and response shape; actor is derived from the token. |
| Upload evidence | `POST /api/v1/inspections/{inspectionId}/evidence` | Multipart `file` plus source and optional capture/GPS/reference metadata. |
| List evidence | `GET /api/v1/inspections/{inspectionId}/evidence` | Returns available metadata only; it does not expose MinIO object keys or URLs. |
| Stream evidence | `GET /api/v1/inspections/{inspectionId}/evidence/{evidenceId}/content` | Rechecks evidence-to-inspection and assignment scope before streaming. |

Allowed evidence source values are `SD_CARD`, `WEB_UPLOAD`, `MOBILE_UPLOAD`,
and `IMPORTED`. The backend validates supported content and configured size,
computes SHA-256, and treats a repeated inspection/checksum upload
idempotently. Missing GPS is allowed; latitude and longitude must be supplied
together. A MinIO deployment enables storage with `MINIO_ENABLED=true` and
environment-supplied endpoint, bucket, access key, and secret key. The feature
does not return direct object-store URLs.

## AI candidates and verified findings (FE-05)

AI is optional. `YOLO_INFERENCE_ENABLED` defaults to `false`; when enabled, the
adapter posts raw eligible image bytes with their media type to the configured
`YOLO_INFERENCE_BASE_URL` plus `YOLO_INFERENCE_PREDICT_PATH` (default
`/predict`). Connect/read timeouts are configurable. The adapter expects a JSON
array with `modelName`, `modelVersion`, `predictedLabel`, `confidence`, and
`boundingBox` per detection. This is the adapter contract; it does not assert
that a separately hosted model has been deployed or live-verified.

| Operation | Endpoint | Behavior |
| --- | --- | --- |
| List candidates | `GET /api/v1/inspections/{inspectionId}/finding-candidates` | Lists advisory candidates for the assigned Inspector. |
| Analyze evidence | `POST /api/v1/inspections/{inspectionId}/evidence/{evidenceId}/analyze` | Persists validated model output as non-official candidates. |
| Review candidate | `POST /api/v1/inspections/{inspectionId}/finding-candidates/{candidateId}/review` | Inspector confirms, modifies, or rejects the candidate; rejection requires a reason. |
| Add manual finding | `POST /api/v1/inspections/{inspectionId}/findings` | Creates an official manual finding for eligible inspection evidence. |

Only confirmed/modified AI candidates and manual findings create official
verified findings. Rejected or pending candidates do not enter report
snapshots. An AI failure does not remove stored evidence or block the manual
finding path.

## Versioned reports and Client decision (FE-06)

| Operation | Endpoint | Required actor/scope |
| --- | --- | --- |
| List/read reports | `GET /api/v1/reports`, `GET /api/v1/reports/{reportId}` | Inspector author/reviewer, ORG_ADMIN, or organization member; results are filtered per actor. |
| Create/read inspection draft | `POST` / `GET /api/v1/inspections/{inspectionId}/report` | Assigned Inspector; draft snapshot requires all required checklist responses and at least one available evidence item. |
| Create linked revision | `POST /api/v1/reports/{reportId}/versions` | Report author after a review or ORG_ADMIN revision request. |
| Assign reviewer | `PUT /api/v1/reports/{reportId}/versions/{versionId}/reviewer` | ORG_ADMIN; reviewer is an active, distinct Inspector. |
| Submit/review | `POST .../submit-review`, `POST .../review` | Author submits; only the assigned, distinct Inspector reviews. |
| Release | `POST /api/v1/reports/{reportId}/versions/{versionId}/release` | ORG_ADMIN, after technical approval and completeness checks. |
| Organization decision | `POST /api/v1/reports/{reportId}/versions/{versionId}/org-admin-decision` | ORG_ADMIN belonging to the report's organization, on the current released version. |
| Stream released evidence | `GET /api/v1/reports/{reportId}/versions/{versionId}/evidence/{evidenceId}/content` | Owning organization; evidence must be present in that visible version snapshot. |

Organization responses exclude internal review comments and unreleased content.
Accepting a released version records the ORG_ADMIN actor, makes the version
immutable, and publishes one `ReportAcceptedEvent`; an idempotent repeated
acceptance does not publish a second handoff. A revision request requires a
reason, stores both decision actor and reason on `report_versions`, and leaves
the released version in the organization-visible history. Migration
`V10__inspection_report_client_decision_audit.sql` adds that audit data without
rewriting the notification migration `V9`.

The acceptance event is the boundary to WF4/billing. This WF3 slice does not
persist invoices or implement payment processing; the billing owner consumes
the handoff and records the separate post-service milestone.

## Verification records

**Historical verification record (pre-reset only):** The former service and API tests covered assignment scope, evidence validation and idempotency, AI provenance/review states, report separation of duties, organization scope/decisions, and the event handoff. Report 5 records the outcomes for `WF3-001`–`WF3-004` on the fixed `Feature 2` sheet. Those recorded results are preserved as evidence of the earlier v1 baseline; they do not assert that the corresponding workflow tests or runtime remain in this reset branch.
