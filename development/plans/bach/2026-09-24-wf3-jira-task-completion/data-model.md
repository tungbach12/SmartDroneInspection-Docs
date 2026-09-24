# WF3 Data Model Plan

The implementation reuses the WF3 schema introduced by backend migration V7 and adds only the Client-decision audit fields in forward migration V10. Canonical definitions are in [database-design.md](../../../../project-reference/database-design.md); no schema rewrite was performed.

## Entities and ownership

| Entity/table | Owner | Role in this delivery |
| --- | --- | --- |
| Inspection | inspections | Binds one confirmed service order and accepted assignment to an asset, author, checklist template, and inspection lifecycle. |
| ChecklistResponse | inspections | Stores one attributable response per inspection/checklist item. |
| Evidence | inspections | Stores validated metadata, server-computed SHA-256, uploader/source/capture metadata, upload state, and MinIO object key. Binary bytes remain in MinIO. |
| AiFindingCandidate | inspections | Stores only advisory YOLO output: model/version, label, confidence, bounding box, and review state. |
| VerifiedFinding | inspections | Stores official Inspector-verified or manual findings and references the source candidate when AI-derived. |
| InspectionReport | inspections | Aggregate for one report authored from the inspection. |
| ReportVersion | inspections | Immutable content snapshot and lifecycle timestamps for a particular draft/revision/release/acceptance. |
| PeerReview | inspections | Reviewer assignment, decision, comments, and timestamps for one submitted version. |
| EventPublication | Spring Modulith infrastructure | Tracks internal event listener publication/completion for handoffs; not a new WF3 business entity. |

## Relationships

```text
Accepted assignment + service order
               |
               v
Inspection ---- ChecklistResponse*
     |
     +---- Evidence* ---- MinIO object bytes
     |          |
     |          +---- AiFindingCandidate* ---- Inspector decision
     |          |                                    |
     |          +--------------------------------> VerifiedFinding*
     |
     +---- InspectionReport ---- ReportVersion* ---- PeerReview*
                                               |
                                    Client acceptance locks version
                                               |
                                  accepted-report / billing handoff
```

The database design defines inspection/assignment and report relationships as unique where applicable; evidence may be attached to exactly one inspection or maintenance-work parent. This WF3 plan must not weaken those invariants.

## Lifecycle and invariants

- Inspection: accepted assignment enters READY_FOR_INSPECTION; authorized start transitions it to IN_PROGRESS; completion records a server timestamp and required checklist state.
- Evidence: validate before making content available; persist upload state and metadata; retry scoped by inspection plus checksum; a duplicate must not create a second evidence row or MinIO object.
- Candidate: PENDING -> CONFIRMED, MODIFIED, or REJECTED. A candidate is never an official finding while PENDING or REJECTED.
- Verified finding: created from a confirmed/modified candidate or through the manual path. It is the only finding type eligible for official report content/statistics.
- Report: draft -> submitted for peer review -> changes requested or technically approved -> manager released -> Client accepted or revision requested. Each revised submission is a new linked ReportVersion.
- Peer review: reviewer differs from author; a Service Manager assigns the reviewer; review decisions remain associated with the version reviewed.
- Client visibility: only released versions are customer-visible; internal drafts and review comments remain hidden. Acceptance makes the accepted version append-only/immutable.
- Billing handoff: acceptance includes report/version/organization/asset identifiers and acceptance time; invoice creation is a separately owned downstream responsibility.

## Persistence decision

Migration V7 contains WF3 inspection, checklist, evidence, AI-candidate, verified-finding, report-version, and peer-review schema. Focused report acceptance tests identified missing persisted Client decision attribution and reason; forward migration V10 adds `client_decision_by_user_id` and `client_decision_reason` to report versions. V9 remains the notifications migration. No applied migration was edited and no other schema delta was needed.

## Sensitive and external data

- Do not store image bytes in PostgreSQL. Do not return MinIO credentials, bucket secrets, or unrestricted object URLs to clients.
- Keep organization, assignment, uploader, model, decision, version, and audit attribution server-derived or server-validated.
- Keep protected evidence content and credentials out of logs. Persist only necessary metadata and opaque object references.
- Do not persist a failed AI response as an official finding; failure must not make already stored evidence unavailable.

## Migration checklist for any future schema gap

1. Compare the required acceptance field/constraint with V7 and the current JPA entity/repository.
2. Prove the gap with a failing focused test before changing schema.
3. Add a new forward Flyway migration and preserve existing rows/history.
4. Update the database design and Report 3 only if the product contract changes.
5. Run backend verification and record results in Report 5 after the feature is implemented.
