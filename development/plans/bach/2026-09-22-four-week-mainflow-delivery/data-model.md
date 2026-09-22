# Data and State Handoffs

The authoritative physical schema is the existing
[database design](../../../../project-reference/data-model/database-design.md) and backend Flyway
migrations V1–V9. This file records the parts the four-week runtime plan must use and the one
identified schema gap; it is not a replacement data dictionary.

## WF1 — assets

`asset_categories` and `checklist_templates`/`checklist_items` are Admin-managed inputs. An
`asset` belongs to exactly one organization and has a code unique within that organization.
`asset_documents` refer to authorized asset files. An active `inspection_schedule` references an
active asset and an available checklist version. A due cycle emits one periodic request keyed by
`asset_id + schedule_id + due_cycle`; retry must return the same business outcome.

State: asset `ACTIVE/INACTIVE/RETIRED`; schedule `ACTIVE/PAUSED/DISABLED`. An inactive asset cannot
produce a new executable due request. WF1 records the due cycle and publishes a durable event;
WF2 creates the request idempotently, with database uniqueness as the final duplicate guard.

## WF2 — inspection requests

`inspection_requests` contain organization, asset, type (`PERIODIC/AD_HOC`), scope, priority,
deadline, contact, and access context. `inspection_request_attachments` store supporting files.
`inspection_quotations` are immutable versions; a Client decision applies only to the current
version. A confirmed `inspection_service_order` references the approved quotation.
`inspection_assignments` record Inspector, deadline, acceptance or rejection, and rejection reason.

State: submitted → reviewed → quoted → Client decision → confirmed order → pending assignment →
accepted assignment/`READY_FOR_INSPECTION`. Revision and rejection return to the responsible role
without overwriting earlier versions. Assignment before order confirmation is invalid.

## WF3 — inspections and reports

An `inspection` begins from an accepted WF2 assignment. `checklist_responses` record the selected
checklist version's answers. `evidence` stores file metadata, checksum, source, and object key;
file contents live in MinIO. `ai_finding_candidates` remain non-official. A
`verified_finding` is created only after Inspector confirmation/modification or manual entry.

`inspection_reports` group immutable `report_versions`; `peer_reviews` record decisions from an
Inspector other than the report author. Customer visibility begins only after Service Manager
release. Accepted versions cannot be edited; later correction creates a linked version.

State: ready → in progress → findings reviewed → draft → peer review → technically approved →
released → Client accepted or revision requested. Rejected AI candidates do not enter official
reports or maintenance ticket sources.

## WF4 — maintenance

A `maintenance_ticket` belongs to the same organization and asset as an accepted report version.
`maintenance_ticket_findings` link at least one verified finding in that report. A
`maintenance_assignment` of type `ASSESSMENT` permits an Engineer to write one assessment with
technical scope and cost range. Versioned `maintenance_quotations` and `maintenance_orders` bind
the Client's approved scope and post-service terms. `EXECUTION`/`REWORK` assignments authorize
work logs and before/after evidence. A material `maintenance_change_request` leads to a new order
version only after Client approval.

State: submitted → assessed → quoted → approved order → execution → internal review → released →
accepted/closed, rework, or re-inspection. Re-inspection emits a linked ad hoc WF2 request.
Closure requires before/after evidence and a released result. Rejected changes do not alter the
current approved order.

## Cross-flow invoice gap

Existing `invoices` rows are maintenance-linked only. Report 3 requires a separate inspection
invoice after report acceptance, with the same manual/external payment-status lifecycle.
The implementation must use a **new forward migration** that:

1. Adds a nullable accepted `report_version_id` reference to `invoices`.
2. Makes maintenance source columns nullable where needed.
3. Enforces exactly one source: accepted inspection report **or** maintenance order/ticket.
4. Preserves existing maintenance invoice rows and unique invoice numbers.
5. Makes invoice creation idempotent per accepted source and keeps `DRAFT/ISSUED/PAID/OVERDUE/VOID`
   status names stable.

The invoice entity/repository and service move to a small `billing` capability when this runtime
change lands. The schema and JPA mapping must be checked together before choosing exact SQL null
constraints; no applied migration is edited.

## Authorization and invariants

| Actor | Scoped records | Denied cases |
| --- | --- | --- |
| Client | Their organization's assets, requests, quotations, released reports, tickets, invoices. | Another organization; internal drafts/peer comments. |
| Service Manager | Service workflow records across organizations. | Admin-only configuration or unapproved release/assignment transitions. |
| Inspector | Accepted inspection assignment or separate peer-review assignment. | Other Inspector's work; self-review. |
| Maintenance Engineer | Accepted assessment/execution/rework assignment. | Other Engineer's ticket; execution before approved order. |
| Admin | Organizations, users, category/checklist configuration, authorized audit view. | Customer approval or field-work mutation solely by Admin role. |

Repository queries must include the authenticated organization/assignment scope before loading
mutable records. Web/mobile visibility is not the final authorization check.
