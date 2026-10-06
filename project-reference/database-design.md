---
title: "Database Design"
description: "Target PostgreSQL schema for the SmartDroneInspection code-first domain model."
weight: 25
---

# SmartDroneInspection Database Design

This document defines the target PostgreSQL schema for the Java/JPA code-first domain model. It is the physical-design companion to the conceptual entities in the Report 3 SRS and the WF1-WF4 business-flow reference.

It is not an executable Flyway migration and does not claim that every table below is already implemented. The current implementation boundary is recorded in [Implementation status](#implementation-status).

## 1. Design goals

- Support the six canonical roles across three actor zones:
  - `PLATFORM_GOVERNANCE`: `PLATFORM_ADMIN`, `PLATFORM_OPERATOR`.
  - `CUSTOMER_ORGANIZATION`: `CLIENT`.
  - `SERVICE_PROVIDER`: `PROVIDER_MANAGER`, `INSPECTOR`, `MAINTENANCE_ENGINEER`.
- Support Multi-Provider multi-tenancy, isolating provider business assets, bids, assignments, and flight data.
- Model the electronic contract, the direct-transfer settlement lifecycle (payment invoice, Provider receipt confirmation, Platform commission invoicing), and internal complaint records. The Platform never holds funds, so no escrow or ledger table exists.
- Preserve organization, ownership, assignment, and separation-of-duties scope in relational keys.
- Cover MF1–MF5 without adding speculative subsystems.
- Preserve required quotation, order, report, assignment, approval, dispute, and resolution history.
- Store transactional state and metadata in PostgreSQL while MinIO stores file bytes.
- Keep JPA entities inside the feature that owns the business capability.
- Use forward-only Flyway migrations for deployed environments; never use Hibernate schema update in production.

## 2. Right-sized schema

The target contains **42 application tables** plus the Spring Modulith `event_publication` infrastructure table. The target report-version model stores the Inspector author's verification/edit confirmation and Provider Manager completeness/release metadata.

| Capability | Tables | Count |
| --- | --- | ---: |
| Identity, multi-provider and access | `organizations`, `provider_organizations`, `users`, `user_roles`, `auth_sessions`, `refresh_tokens` | 6 |
| Audit | `security_audit_events` | 1 |
| Asset catalog and planning | `asset_categories`, `category_frequency_suggestions`, `checklist_templates`, `checklist_items`, `assets`, `asset_documents`, `inspection_schedules`, `schedule_proposals` | 8 |
| MF1 request, quotation & direct settlement | `inspection_requests`, `inspection_request_attachments`, `inspection_quotations`, `inspection_service_orders`, `inspection_assignments` | 5 |
| MF2 drone mission planning | `drone_mission_plans`, `mission_shot_items` | 2 |
| MF3 inspection and report delivery | `inspections`, `checklist_responses`, `evidence`, `ai_finding_candidates`, `verified_findings`, `inspection_reports`, `report_versions` | 7 |
| MF4 dispute arbitration | `dispute_tickets`, `dispute_evidence` | 2 |
| MF5 maintenance and billing | `maintenance_tickets`, `maintenance_ticket_findings`, `maintenance_assessments`, `maintenance_quotations`, `maintenance_orders`, `maintenance_assignments`, `maintenance_work_logs`, `maintenance_change_requests`, `invoices` | 9 |
| Platform governance and supporting workflow | `platform_configurations`, `notifications` | 2 |
| Framework infrastructure | `event_publication` | 1 |

The design deliberately does not create separate lookup tables for roles, statuses, priorities, severities, or actor zones. These are stable Java enums persisted as constrained strings. It also does not create dashboard, search-index, notification-template, or file-blob tables. Platform-operated AI (YOLO inference and LLM narrative drafting) is delivered as centralized platform capability with metadata and candidate findings persisted directly in the core tables.

## 3. Code-first and migration policy

The Java model is written first, but the production database remains migration-controlled:

1. Model an aggregate with JPA entities and value types inside its owning feature.
2. Generate or draft the PostgreSQL DDL from the reviewed model.
3. Convert it into a new forward Flyway migration and review all foreign keys, checks, indexes, and delete behavior.
4. Run production with Hibernate schema validation, not automatic schema mutation.

Recommended mappings:

| Java | PostgreSQL | Rule |
| --- | --- | --- |
| `UUID` | `UUID` | Generated with `gen_random_uuid()`; public identifiers are non-sequential. |
| `Instant` | `TIMESTAMPTZ` | All stored timestamps represent an absolute instant. |
| `BigDecimal` | `NUMERIC(14,2)` | Monetary values never use floating point. |
| Java enum | `VARCHAR` + check constraint | Enum names are persisted; renames require a migration. |
| `@Version long` | `BIGINT` | Used on mutable aggregates to reject stale updates. |
| Snapshot/value structure | `JSONB` | Limited to immutable commercial/report snapshots and flexible metadata. |

Cross-module references should normally be stored as UUID fields in Java instead of cross-module JPA object graphs. PostgreSQL still enforces the foreign key. Relationships inside the same aggregate may use lazy JPA associations. Cascades must not cross aggregate boundaries.

## 4. Common physical conventions

- Table and column names use `snake_case`; Java types use the project Java naming conventions.
- Every aggregate/entity table has `id UUID PRIMARY KEY DEFAULT gen_random_uuid()`, except pure junction tables and framework-owned tables.
- Mutable aggregates have `created_at`, `updated_at`, and `row_version`.
- Append-only versions, decisions, evidence metadata, and audit records have `created_at` and are not overwritten after becoming final.
- Required customer-visible decisions record the actor and decision timestamp.
- Business records referenced by history are not hard-deleted. Their status is changed to an inactive, cancelled, retired, or superseded state.
- Foreign-key delete behavior defaults to `RESTRICT`. Authentication children may use `CASCADE`; optional actor references may use `SET NULL`.
- File tables store `object_key`, checksum, size, and media metadata only. File bytes remain in MinIO.
- Sensitive credentials, raw refresh tokens, access tokens, and object-storage secrets are never stored.

## 5. Relationship overview

The diagrams are split by workflow so the physical model remains readable.

### 5.1 Identity, assets, and schedules

```mermaid
erDiagram
    ORGANIZATIONS ||--o{ USERS : contains
    USERS ||--o{ USER_ROLES : has
    USERS ||--o{ AUTH_SESSIONS : opens
    AUTH_SESSIONS ||--o{ REFRESH_TOKENS : rotates
    USERS ||--o{ PLATFORM_CONFIGURATIONS : publishes
    ORGANIZATIONS ||--o{ ASSETS : owns
    ASSET_CATEGORIES ||--o{ ASSETS : classifies
    ASSET_CATEGORIES ||--o{ CHECKLIST_TEMPLATES : supports
    CHECKLIST_TEMPLATES ||--o{ CHECKLIST_ITEMS : contains
    ASSETS ||--o{ ASSET_DOCUMENTS : documents
    ASSETS ||--o{ INSPECTION_SCHEDULES : schedules
    CHECKLIST_TEMPLATES ||--o{ INSPECTION_SCHEDULES : configures
```

### 5.2 Inspection request and execution

```mermaid
erDiagram
    ASSETS ||--o{ INSPECTION_REQUESTS : requests
    INSPECTION_SCHEDULES o|--o{ INSPECTION_REQUESTS : generates
    INSPECTION_REQUESTS ||--o{ INSPECTION_REQUEST_ATTACHMENTS : includes
    INSPECTION_REQUESTS ||--o{ INSPECTION_QUOTATIONS : quotes
    INSPECTION_QUOTATIONS ||--o| INSPECTION_SERVICE_ORDERS : approves
    INSPECTION_SERVICE_ORDERS ||--o{ DRONE_MISSION_PLANS : plans
    DRONE_MISSION_PLANS ||--o{ MISSION_SHOT_ITEMS : contains
    INSPECTION_SERVICE_ORDERS ||--o{ INSPECTION_ASSIGNMENTS : assigns
    INSPECTION_ASSIGNMENTS ||--o| INSPECTIONS : starts
    INSPECTIONS ||--o{ CHECKLIST_RESPONSES : records
    INSPECTIONS ||--o{ EVIDENCE : stores
```

### 5.3 Findings and reports

```mermaid
erDiagram
    EVIDENCE ||--o{ AI_FINDING_CANDIDATES : produces
    INSPECTIONS ||--o{ VERIFIED_FINDINGS : confirms
    AI_FINDING_CANDIDATES o|--o| VERIFIED_FINDINGS : becomes
    INSPECTIONS ||--|| INSPECTION_REPORTS : compiles
    INSPECTION_REPORTS ||--o{ REPORT_VERSIONS : versions
```

### 5.4 Maintenance and supporting records

```mermaid
erDiagram
    REPORT_VERSIONS ||--o{ MAINTENANCE_TICKETS : originates
    MAINTENANCE_TICKETS ||--o{ MAINTENANCE_TICKET_FINDINGS : contains
    VERIFIED_FINDINGS ||--o{ MAINTENANCE_TICKET_FINDINGS : links
    MAINTENANCE_TICKETS ||--o{ MAINTENANCE_ASSIGNMENTS : assigns
    MAINTENANCE_ASSIGNMENTS ||--o| MAINTENANCE_ASSESSMENTS : assesses
    MAINTENANCE_TICKETS ||--o{ MAINTENANCE_QUOTATIONS : quotes
    MAINTENANCE_QUOTATIONS ||--o| MAINTENANCE_ORDERS : approves
    MAINTENANCE_ORDERS ||--o{ MAINTENANCE_ASSIGNMENTS : executes
    MAINTENANCE_ASSIGNMENTS ||--o{ MAINTENANCE_WORK_LOGS : records
    MAINTENANCE_WORK_LOGS ||--o{ EVIDENCE : proves
    MAINTENANCE_TICKETS ||--o{ MAINTENANCE_CHANGE_REQUESTS : changes
    MAINTENANCE_ORDERS ||--o| INVOICES : invoices
    USERS ||--o{ NOTIFICATIONS : receives
```

## 6. Data dictionary

When a definition below says **mutable aggregate columns**, it means `created_at TIMESTAMPTZ`, `updated_at TIMESTAMPTZ`, and `row_version BIGINT NOT NULL DEFAULT 0`. Append-only child/version tables include `created_at TIMESTAMPTZ`. Existing identity tables retain their current timestamp and locking shape unless a target addition is explicitly listed.

### 6.1 Identity and access

#### `organizations` (Customer Organizations)

| Column | Type | Null | Constraint or purpose |
| --- | --- | --- | --- |
| `id` | `UUID` | No | Primary key. |
| `name` | `VARCHAR(200)` | No | Display name. |
| `code` | `VARCHAR(64)` | No | Unique stable organization code, normalized to uppercase. A Client representative may create the organization together with the first active Client account. |
| `description` | `VARCHAR(2000)` | Yes | Administrative description. |
| `active` | `BOOLEAN` | No | Defaults to `TRUE`. |
| `created_at` | `TIMESTAMPTZ` | No | Creation time. |
| `updated_at` | `TIMESTAMPTZ` | No | Last update time. |

Indexes: unique `code`; index `active` when organization administration requires filtering.

#### `provider_organizations` (Service Provider Organizations)

| Column | Type | Null | Constraint or purpose |
| --- | --- | --- | --- |
| `id` | `UUID` | No | Primary key. |
| `name` | `VARCHAR(200)` | No | Trade/display name. |
| `legal_name` | `VARCHAR(250)` | No | Full legal company name per Business Registration. |
| `tax_code` | `VARCHAR(32)` | No | Unique corporate tax code. |
| `business_license_no` | `VARCHAR(64)` | No | Business registration certificate number. |
| `drone_permit_code` | `VARCHAR(64)` | Yes | UAV registration identification code per Luật Phòng không nhân dân 2024 & Nghị định 288/2025/NĐ-CP. |
| `insurance_policy_no` | `VARCHAR(128)` | Yes | Third-party aviation liability insurance certificate. |
| `status` | `VARCHAR(32)` | No | `PENDING`, `VERIFIED`, `SUSPENDED`, or `BANNED`. |
| `rating_score` | `NUMERIC(3,2)` | Yes | Quality rating calculated from completed orders (1.00 - 5.00). |
| `approved_by_operator_id` | `UUID` | Yes | FK to `users` (`PLATFORM_OPERATOR` who vetted the provider). |
| `approved_at` | `TIMESTAMPTZ` | Yes | Timestamp of vetting approval. |
| `created_at` | `TIMESTAMPTZ` | No | Creation time. |
| `updated_at` | `TIMESTAMPTZ` | No | Last update time. |

Indexes: unique `tax_code`; index `status`.

#### `users`

| Column | Type | Null | Constraint or purpose |
| --- | --- | --- | --- |
| `id` | `UUID` | No | Primary key. |
| `email` | `VARCHAR(320)` | No | Original display value. |
| `normalized_email` | `VARCHAR(320)` | No | Unique lower-case lookup value. |
| `full_name` | `VARCHAR(200)` | No | User display name. |
| `password_hash` | `VARCHAR(1024)` | Yes | Adaptive password hash; null only during controlled provisioning if supported. |
| `status` | `VARCHAR(32)` | No | `ACTIVE`, `SUSPENDED`, or `DISABLED`. |
| `actor_zone` | `VARCHAR(32)` | No | `PLATFORM_GOVERNANCE`, `CUSTOMER_ORGANIZATION`, or `SERVICE_PROVIDER`. |
| `organization_id` | `UUID` | Yes | FK to `organizations`; required only for customer identities. |
| `provider_id` | `UUID` | Yes | FK to `provider_organizations`; required for service provider workforce. |
| `auth_version` | `INTEGER` | No | Incremented when all tokens must become stale. |
| `failed_login_count` | `INTEGER` | No | Non-negative failed-attempt counter. |
| `lockout_until` | `TIMESTAMPTZ` | Yes | Temporary login cooldown. |
| `must_change_password` | `BOOLEAN` | No | Requires password setup/change before normal access. |
| `last_login_at` | `TIMESTAMPTZ` | Yes | Last successful login. |
| `last_login_ip` | `VARCHAR(45)` | Yes | IPv4/IPv6 text. |
| `created_at` | `TIMESTAMPTZ` | No | Creation time. |
| `updated_at` | `TIMESTAMPTZ` | No | Last update time. |

Constraints: normalized email is unique; customer-zone users require `organization_id` (and null `provider_id`); service-provider-zone users require `provider_id` (and null `organization_id`); platform-governance-zone users have both null.

#### `user_roles`

| Column | Type | Null | Constraint or purpose |
| --- | --- | --- | --- |
| `id` | `UUID` | No | Primary key. |
| `user_id` | `UUID` | No | FK to `users`, cascade on user deletion before operational history exists. |
| `role` | `VARCHAR(64)` | No | One of the six canonical role codes: `PLATFORM_ADMIN`, `PLATFORM_OPERATOR`, `CLIENT`, `PROVIDER_MANAGER`, `INSPECTOR`, `MAINTENANCE_ENGINEER`. |

Constraints: unique `(user_id, role)`; actor-zone combinations are validated in the domain policy and tests.

#### `auth_sessions`

| Column | Type | Null | Constraint or purpose |
| --- | --- | --- | --- |
| `id` | `UUID` | No | Session identifier embedded in access tokens. |
| `user_id` | `UUID` | No | FK to `users`. |
| `client_type` | `VARCHAR(16)` | No | `WEB` or `MOBILE`. |
| `expires_at` | `TIMESTAMPTZ` | No | Absolute session expiry. |
| `revoked_at` | `TIMESTAMPTZ` | Yes | Revocation timestamp. |
| `revoked_reason` | `VARCHAR(128)` | Yes | Logout, role change, password change, disablement, or reuse reason. |

Indexes: `(user_id, revoked_at)` and `expires_at` for cleanup.

#### `refresh_tokens`

| Column | Type | Null | Constraint or purpose |
| --- | --- | --- | --- |
| `id` | `UUID` | No | Primary key. |
| `session_id` | `UUID` | No | FK to `auth_sessions`, cascade on session deletion. |
| `token_hash` | `VARCHAR(64)` | No | Unique keyed hash; never stores a raw token. |
| `issued_at` | `TIMESTAMPTZ` | No | Issue time. |
| `expires_at` | `TIMESTAMPTZ` | No | Token expiry after issue time. |
| `revoked_at` | `TIMESTAMPTZ` | Yes | Rotation or revocation time. |
| `revoke_reason` | `VARCHAR(128)` | Yes | Stable operational reason. |

Indexes: unique `token_hash`; `(session_id, issued_at DESC)`; `expires_at` for retention cleanup.

#### `platform_configurations` (versioned target commercial policies)

One immutable row represents one published version of a Platform commercial policy. This is a target schema addition, not an implemented table or migration. `PLATFORM_OPERATOR` may publish a prospective version; old versions remain queryable for contract/audit traceability. Platform technical settings owned by `PLATFORM_ADMIN` are outside this commercial-policy table.

| Column | Type | Null | Constraint or purpose |
| --- | --- | --- | --- |
| `id` | `UUID` | No | Primary key. |
| `policy_key` | `VARCHAR(96)` | No | Stable key such as `STANDARD_COMMISSION`, `CLIENT_REVIEW_PERIOD`, `CANCELLATION`, or `WARRANTY_DURATION`. No funding or retention policy key exists — the Platform holds no funds. |
| `version` | `INTEGER` | No | Positive, monotonically increasing version for a policy key. |
| `policy_value` | `JSONB` | No | Validated policy data; schema depends on `policy_key`, with no implicit numeric defaults. |
| `status` | `VARCHAR(24)` | No | `DRAFT`, `PUBLISHED`, `SUPERSEDED`, or `RETIRED`. |
| `effective_from` | `TIMESTAMPTZ` | No | Prospective effective instant; publication cannot mutate already snapshotted orders. |
| `effective_until` | `TIMESTAMPTZ` | Yes | Optional end instant when superseded or retired. |
| `published_by_user_id` | `UUID` | No | FK to `users`; must identify an authorized `PLATFORM_OPERATOR`. |
| `published_at` | `TIMESTAMPTZ` | No | Publication audit time. |
| `created_at` | `TIMESTAMPTZ` | No | Creation time. |

Constraints: unique `(policy_key, version)`; at most one published version per key/effective interval; policy values are validated against the policy key and may not encode provider-specific commission rates. Every policy edit and publication is audited. Policy rows are append-only after publication.

#### `security_audit_events`

This existing table remains the single append-only audit stream for authentication and material workflow events. The name is retained to avoid an unnecessary rename.

| Column | Type | Null | Constraint or purpose |
| --- | --- | --- | --- |
| `id` | `UUID` | No | Primary key. |
| `actor_user_id` | `UUID` | Yes | FK to `users`, set null when required. |
| `subject_user_id` | `UUID` | Yes | Affected user for identity events. |
| `organization_id` | `UUID` | Yes | Scope of a workflow event. Target addition. |
| `event_type` | `VARCHAR(96)` | No | Stable event name. |
| `outcome` | `VARCHAR(16)` | No | `SUCCESS`, `FAILURE`, or `DENIED`. |
| `entity_type` | `VARCHAR(64)` | Yes | Business entity type. Target addition. |
| `entity_id` | `UUID` | Yes | Business entity identifier. Target addition. |
| `details` | `JSONB` | Yes | Non-secret structured audit metadata. Target addition. |
| `ip_address` | `VARCHAR(45)` | Yes | Request source when applicable. |
| `user_agent` | `VARCHAR(1000)` | Yes | Client metadata when applicable. |
| `correlation_id` | `VARCHAR(128)` | Yes | Trace identifier. |
| `occurred_at` | `TIMESTAMPTZ` | No | Event time. |

Indexes: `(event_type, occurred_at DESC)`, `(subject_user_id, occurred_at DESC)`, and `(entity_type, entity_id, occurred_at DESC)`.

### 6.2 Asset catalog and planning

#### `asset_categories`

Columns: `id`, unique `code VARCHAR(64)`, `name VARCHAR(160)`, `description VARCHAR(2000)`, `active BOOLEAN`, and the mutable aggregate timestamps/version.

#### `checklist_templates`

| Column | Type | Null | Constraint or purpose |
| --- | --- | --- | --- |
| `id` | `UUID` | No | Version identifier. |
| `template_key` | `VARCHAR(64)` | No | Stable key shared by all versions. |
| `version_number` | `INTEGER` | No | Positive version number. |
| `asset_category_id` | `UUID` | Yes | Optional FK to `asset_categories`. |
| `name` | `VARCHAR(200)` | No | Template name. |
| `description` | `VARCHAR(2000)` | Yes | Template purpose. |
| `status` | `VARCHAR(24)` | No | `DRAFT`, `ACTIVE`, or `RETIRED`. |
| `created_by_user_id` | `UUID` | No | Admin who created the version. |
| `published_at` | `TIMESTAMPTZ` | Yes | Time the version became active. |

Constraints: unique `(template_key, version_number)`; a published version is immutable.

#### `checklist_items`

| Column | Type | Null | Constraint or purpose |
| --- | --- | --- | --- |
| `id` | `UUID` | No | Primary key. |
| `template_id` | `UUID` | No | FK to one checklist-template version. |
| `item_code` | `VARCHAR(64)` | No | Stable code within the version. |
| `section_name` | `VARCHAR(160)` | Yes | Display grouping. |
| `prompt` | `VARCHAR(1000)` | No | Inspection instruction/question. |
| `response_type` | `VARCHAR(24)` | No | `PASS_FAIL`, `TEXT`, `NUMBER`, `BOOLEAN`, or `CHOICE`. |
| `required` | `BOOLEAN` | No | Whether completion is mandatory. |
| `display_order` | `INTEGER` | No | Non-negative ordering value. |
| `guidance` | `VARCHAR(2000)` | Yes | Field guidance. |
| `validation_config` | `JSONB` | Yes | Allowed choices or numeric bounds. |

Constraints: unique `(template_id, item_code)` and `(template_id, display_order)`.

#### `assets`

| Column | Type | Null | Constraint or purpose |
| --- | --- | --- | --- |
| `id` | `UUID` | No | Primary key. |
| `organization_id` | `UUID` | No | Owning organization. |
| `category_id` | `UUID` | No | FK to `asset_categories`. |
| `code` | `VARCHAR(64)` | No | Unique inside the organization. |
| `name` | `VARCHAR(200)` | No | Asset name. |
| `description` | `VARCHAR(2000)` | Yes | Asset description. |
| `location_text` | `VARCHAR(500)` | No | Human-readable location. |
| `latitude` | `NUMERIC(9,6)` | Yes | Optional WGS84 latitude. |
| `longitude` | `NUMERIC(9,6)` | Yes | Optional WGS84 longitude. |
| `ownership_information` | `VARCHAR(1000)` | Yes | Customer-provided ownership detail. |
| `default_scope` | `VARCHAR(4000)` | Yes | Default inspection scope inherited by periodic requests. |
| `default_priority` | `VARCHAR(16)` | No | `LOW`, `NORMAL`, `HIGH`, `URGENT` default priority (default `NORMAL`). |
| `site_access_constraints` | `VARCHAR(2000)` | Yes | Site-access constraints inherited by periodic requests. |
| `contact_name` | `VARCHAR(200)` | Yes | On-site contact name for inspections. |
| `contact_phone` | `VARCHAR(32)` | Yes | On-site contact phone number. |
| `contact_email` | `VARCHAR(320)` | Yes | On-site contact email address. |
| `status` | `VARCHAR(24)` | No | `PENDING_REVIEW`, `ACTIVE`, `INACTIVE`, `REJECTED`, or `RETIRED`. |
| `created_by_user_id` | `UUID` | No | Client actor in the same organization. |

Constraints: unique `(organization_id, code)`; latitude/longitude ranges are checked; `status` is constrained to the five values above.

#### `category_frequency_suggestions`

Admin-configured inspection cadences offered for an asset category. Columns: `id`, `asset_category_id` (FK to `asset_categories`), `frequency_unit` (`DAY`, `WEEK`, `MONTH`, `YEAR`), `frequency_interval` (positive), `sort_order`, `row_version`.

Constraints: unique `(asset_category_id, frequency_unit, frequency_interval)`. Index: `(asset_category_id, sort_order)`.

#### `asset_documents`

Columns: `id`, `asset_id`, `uploaded_by_user_id`, `document_type`, `file_name`, `content_type`, `size_bytes`, `checksum_sha256`, unique `object_key`, optional `document_date`, and `created_at`.

Indexes: `(asset_id, created_at DESC)` and `(asset_id, checksum_sha256)`.

#### `inspection_schedules`

| Column | Type | Null | Constraint or purpose |
| --- | --- | --- | --- |
| `id` | `UUID` | No | Primary key. |
| `asset_id` | `UUID` | No | Scheduled asset. |
| `checklist_template_id` | `UUID` | No | Published template version. |
| `frequency_unit` | `VARCHAR(16)` | No | `DAY`, `WEEK`, `MONTH`, or `YEAR`. |
| `frequency_interval` | `INTEGER` | No | Positive interval. |
| `next_due_at` | `TIMESTAMPTZ` | No | Next due cycle. |
| `last_generated_due_cycle` | `DATE` | Yes | Last successfully generated cycle. |
| `status` | `VARCHAR(24)` | No | `ACTIVE`, `PAUSED`, or `DISABLED`. |
| `created_by_user_id` | `UUID` | No | Client actor in the asset organization. |

Indexes: `(status, next_due_at)` for the scheduler and `asset_id` for scoped retrieval.

A row is created only when a Client selects a `MANAGER_APPROVED` schedule proposal; the Client cannot create a schedule directly.

#### `schedule_proposals`

Supporting Flow schedule setup: Platform-generated inspection-cadence options for an asset are reviewed/approved by the designated business reviewer (`PLATFORM_OPERATOR` in the target role model; `SERVICE_MANAGER` in the implemented v1 baseline), then selected by the Client to create the active schedule. The Client does not create an active schedule directly. Columns: `id`, `asset_id` (FK to `assets`), `checklist_template_id` (FK to `checklist_templates`), `frequency_unit`, `frequency_interval`, `status`, `manager_note`, `reviewed_by_user_id`, `selected_by_user_id`, `created_at`, `updated_at`, `row_version`.

`status` is one of `GENERATED`, `MANAGER_APPROVED`, `MANAGER_REJECTED`, `CLIENT_SELECTED`, or `SUPERSEDED`.

Constraints: unique `(asset_id, frequency_unit, frequency_interval)`. Index: `(asset_id, status)`.

### 6.3 WF2 request, quotation, order, and assignment

#### `inspection_requests`

| Column | Type | Null | Constraint or purpose |
| --- | --- | --- | --- |
| `id` | `UUID` | No | Primary key. |
| `organization_id` | `UUID` | No | Denormalized owner scope. |
| `asset_id` | `UUID` | No | Requested asset. |
| `schedule_id` | `UUID` | Yes | Required for periodic requests. |
| `checklist_template_id` | `UUID` | No | Checklist version used for the work. |
| `request_type` | `VARCHAR(16)` | No | `PERIODIC` or `AD_HOC`. |
| `due_cycle` | `DATE` | Yes | Required for periodic requests. |
| `linked_maintenance_ticket_id` | `UUID` | Yes | Source when created by a re-inspection decision. |
| `requested_by_user_id` | `UUID` | Yes | Null only for scheduler-created periodic requests. |
| `scope` | `VARCHAR(4000)` | No | Requested inspection scope. |
| `priority` | `VARCHAR(16)` | No | `LOW`, `NORMAL`, `HIGH`, or `URGENT`. |
| `preferred_deadline` | `TIMESTAMPTZ` | Yes | Customer preference. |
| `site_access_constraints` | `VARCHAR(2000)` | Yes | Access and safety notes. |
| `contact_name` | `VARCHAR(200)` | Yes | Site contact. |
| `contact_phone` | `VARCHAR(32)` | Yes | Site contact phone. |
| `contact_email` | `VARCHAR(320)` | Yes | Site contact email. |
| `status` | `VARCHAR(40)` | No | Controlled WF1/WF2 state. |
| `submitted_at` | `TIMESTAMPTZ` | Yes | Submission time. |

Constraints: periodic rows require schedule and due cycle; ad hoc rows must not have a due cycle; unique `(asset_id, schedule_id, due_cycle)` where type is `PERIODIC`.

#### `inspection_request_attachments`

Columns: `id`, `inspection_request_id`, `uploaded_by_user_id`, `file_name`, `content_type`, `size_bytes`, `checksum_sha256`, unique `object_key`, optional `description`, and `created_at`.

#### `inspection_quotations`

Each row is one immutable commercial version prepared by the bidding or selected Service Provider. Mission-planning values are negotiated and persisted against the service-order/SOW snapshot, not inferred from a global default.

| Column | Type | Null | Constraint or purpose |
| --- | --- | --- | --- |
| `id` | `UUID` | No | Quotation-version identifier. |
| `quotation_series_id` | `UUID` | No | Stable identifier shared by revisions. |
| `inspection_request_id` | `UUID` | No | Quoted request. |
| `provider_id` | `UUID` | No | FK to `provider_organizations` (Bidding Provider). |
| `version_number` | `INTEGER` | No | Positive version number. |
| `previous_version_id` | `UUID` | Yes | Self-FK to the prior version. |
| `prepared_by_user_id` | `UUID` | No | FK to `users` (`PROVIDER_MANAGER`). |
| `currency` | `CHAR(3)` | No | ISO currency code (defaults to `VND`). |
| `subtotal` | `NUMERIC(14,2)` | No | Non-negative service fee (flight + technical labor). |
| `tax_amount` | `NUMERIC(14,2)` | No | Non-negative VAT. |
| `total_amount` | `NUMERIC(14,2)` | No | Total contract fee payable by Client to Provider. |
| `pricing_details` | `JSONB` | No | Immutable line-item snapshot (flight fee, pilot labor, logistics). Excludes AI/storage fees (absorbed by Platform). |
| `scope_snapshot` | `JSONB` | No | Agreed scope, required GSD, and deliverables snapshot. |
| `estimated_duration_hours` | `NUMERIC(10,2)` | Yes | Positive estimate. |
| `payment_terms` | `VARCHAR(2000)` | No | Payment milestones and direct-transfer terms (the Provider bank account is shown on the Payment Invoice). |
| `status` | `VARCHAR(32)` | No | Draft, sent, revision requested, approved, rejected, or superseded. |
| `sent_at` | `TIMESTAMPTZ` | Yes | Customer-visible time. |
| `decided_by_user_id` | `UUID` | Yes | Client decision actor. |
| `decided_at` | `TIMESTAMPTZ` | Yes | Decision time. |
| `revision_reason` | `VARCHAR(2000)` | Yes | Required when revision is requested. |
| `created_at` | `TIMESTAMPTZ` | No | Creation time. |
| `row_version` | `BIGINT` | No | Optimistic-lock version for concurrent quotation decisions. |

Constraints: unique `(quotation_series_id, version_number)`; only an approved version can create a service order. The commercial snapshot is immutable after finalization, while `row_version` protects concurrent state transitions before that point.

#### `inspection_service_orders`

Each row is a target tripartite order under *Luật Giao dịch điện tử 2023*. It snapshots the commercial policy accepted for that order; policy changes apply prospectively and must not rewrite confirmed orders.

| Column | Type | Null | Constraint or purpose |
| --- | --- | --- | --- |
| `id` | `UUID` | No | Primary key. |
| `order_number` | `VARCHAR(64)` | No | Unique business identifier. |
| `approved_quotation_id` | `UUID` | No | FK to `inspection_quotations`. |
| `inspection_request_id` | `UUID` | No | FK to `inspection_requests`. |
| `client_organization_id`| `UUID` | No | FK to `organizations`. |
| `provider_id` | `UUID` | No | FK to `provider_organizations`. |
| `flight_permit_no` | `VARCHAR(128)` | Yes | Flight permit reference issued by Cục Tác chiến - Bộ Tổng Tham mưu. |
| `confirmed_by_user_id` | `UUID` | No | Client actor confirming the order. |
| `confirmed_at` | `TIMESTAMPTZ` | No | Order confirmation time. |
| `scope_snapshot` | `JSONB` | No | SOW, resolution requirements, asset coordinates. |
| `shot_list_snapshot` | `JSONB` | No | Mandatory camera angles, elevation, GSD specs. |
| `deliverables` | `JSONB` | No | Expected deliverable files and reports. |
| `payment_terms` | `VARCHAR(2000)` | No | Human-readable payment milestones and direct-transfer terms agreed for this order. |
| `locked_commission_rate` | `NUMERIC(7,5)` | No | Uniform Platform commission rate accepted for this order; copied from its policy version, not read live during settlement. |
| `locked_review_period_days` | `INTEGER` | No | Client review period in business days, copied from the accepted policy; calendar/holiday interpretation is stated in the order terms. |
| `locked_cancellation_policy` | `JSONB` | No | Accepted cancellation conditions, windows, and eligible-cost rules as an immutable order snapshot; no global numeric default. |
| `commission_policy_version` | `VARCHAR(64)` | No | Published one-rate commission policy version used to calculate the fee. |
| `review_policy_version` | `VARCHAR(64)` | No | Published client-review policy version used by the order timer. |
| `cancellation_policy_version` | `VARCHAR(64)` | No | Published cancellation policy version used by this order. |
| `locked_terms_snapshot` | `JSONB` | No | Immutable snapshot of the accepted business terms, values, display labels, and policy version identifiers used to construct the electronic order. |
| `status` | `VARCHAR(32)` | No | `CONFIRMED` (signed & in force), `ASSIGNMENT_PENDING`, `READY_FOR_INSPECTION`, `READY_FOR_FLIGHT`, `IN_PROGRESS`, `COMPLETED` (accepted), `AWAITING_PAYMENT` (Payment Invoice issued), `PAID` (Provider confirmed the direct transfer), `DISPUTED` (complaint pauses acceptance/payment), `CANCELLED`. |
| `started_at` | `TIMESTAMPTZ` | Yes | Execution start time. |
| `completed_at` | `TIMESTAMPTZ` | Yes | Final acceptance / auto-acceptance time. |
| `payment_invoice_issued_at` | `TIMESTAMPTZ` | Yes | Time the SYSTEM issued the Payment Invoice after acceptance. |
| `paid_at` | `TIMESTAMPTZ` | Yes | Time the Provider confirmed receipt of the Client's direct bank transfer (status `PAID`). |
| `created_at` | `TIMESTAMPTZ` | No | Creation time. |
| `updated_at` | `TIMESTAMPTZ` | No | Last update time. |
| `row_version` | `BIGINT` | No | Optimistic locking. |

#### Settlement & payment records (deliberately no ledger table)

The direct-transfer model means **no escrow, ledger, or payment-partner table exists**: the Client transfers 100% of the fee to the Provider's own bank account outside the platform, and the platform never holds, routes, or freezes money (Decree 52/2024/NĐ-CP; providing payment-intermediary services would require an SBV licence the Platform does not seek). What the platform records is:

| Where | What is recorded |
| --- | --- |
| `inspection_service_orders.status` | The `AWAITING_PAYMENT` → `PAID` transition driven by the Provider's "Confirm receipt" action, plus `paid_at` / confirming user. |
| `invoices` | The Payment Invoice issued after acceptance, and the Platform's commission (+ commission VAT) invoice issued to the Provider (§6.6). |
| `provider_organizations` bank columns | Bank name, account number, account holder displayed on the Payment Invoice — account numbers only, never tokens or secrets. |

A complaint (MF4-03) flips the order to `DISPUTED`, which pauses acceptance and therefore the payment sequence. This is a workflow state only — there are no platform-held funds to freeze.

#### `drone_mission_plans` (target mission-planning aggregate)

A versioned operational plan is created from a confirmed inspection service order. It captures mission-specific engineering targets agreed in the SOW; no universal GSD, overlap, altitude, or camera-angle default is implied. This target entity is not implemented in the current schema.

| Column | Type | Null | Constraint or purpose |
| --- | --- | --- | --- |
| `id` | `UUID` | No | Primary key. |
| `service_order_id` | `UUID` | No | FK to `inspection_service_orders`. |
| `provider_id` | `UUID` | No | Provider organization owning the mission plan; must match the order provider. |
| `version_number` | `INTEGER` | No | Positive version; approved plan revisions create a new version. |
| `previous_version_id` | `UUID` | Yes | Prior mission plan version. |
| `created_by_user_id` | `UUID` | No | Assigned Provider workforce actor with mission-planning permission. |
| `drone_registration_id` | `VARCHAR(128)` | Yes | Provider's registered drone identifier. |
| `pilot_user_id` | `UUID` | Yes | Planned Inspector/pilot; must belong to the order Provider and meet applicable credential checks. |
| `flight_permit_reference` | `VARCHAR(128)` | Yes | Applicable authority-issued flight permit reference; presence is validated for the mission's legal conditions. |
| `camera_model` | `VARCHAR(200)` | Yes | Camera/sensor model used for planning. |
| `sensor_width_mm` | `NUMERIC(10,4)` | Yes | Sensor input used in GSD calculation where available. |
| `focal_length_mm` | `NUMERIC(10,4)` | Yes | Lens input used in GSD calculation where available. |
| `image_width_px` | `INTEGER` | Yes | Image width used in GSD calculation where available. |
| `target_gsd_mm_per_pixel` | `NUMERIC(12,6)` | Yes | SOW-agreed ground-sampling target; positive where specified. |
| `planned_agl_m` | `NUMERIC(10,3)` | Yes | Planned above-ground-level altitude, subject to flight authorization and safety constraints. |
| `forward_overlap_percent` | `NUMERIC(5,2)` | Yes | Mission-specific planned forward overlap; constrained to the valid percentage range. |
| `side_overlap_percent` | `NUMERIC(5,2)` | Yes | Mission-specific planned side overlap; constrained to the valid percentage range. |
| `airspace_check_status` | `VARCHAR(32)` | No | `NOT_CHECKED`, `CLEARANCE_REQUIRED`, `MANUAL_REVIEW`, `CLEARED`, or `BLOCKED`; public map lookup is not itself a permit. |
| `status` | `VARCHAR(32)` | No | `DRAFT`, `SUBMITTED`, `REVISION_REQUIRED`, `APPROVED`, `CANCELLED`, or `SUPERSEDED`. |
| `approved_by_user_id` | `UUID` | Yes | Provider Manager who approves the mission version. |
| `approved_at` | `TIMESTAMPTZ` | Yes | Approval time. |
| `created_at` | `TIMESTAMPTZ` | No | Creation time. |
| `updated_at` | `TIMESTAMPTZ` | No | Last update time. |
| `row_version` | `BIGINT` | No | Optimistic locking for concurrent plan edits/approval. |

Constraints: unique `(service_order_id, version_number)`; exactly one current approved plan per service order; cross-provider plan access is denied. Permit, pilot credential, drone registration, airspace clearance, and SOW consistency checks remain application/domain rules where external authorities determine applicability.

#### `mission_shot_items` (target shot/waypoint rows)

Ordered, mission-specific capture instructions belonging to one drone mission plan. Waypoint fields are optional when the approved plan uses manual piloting; mission objectives, required shot items and SOW acceptance targets still apply.

| Column | Type | Null | Constraint or purpose |
| --- | --- | --- | --- |
| `id` | `UUID` | No | Primary key. |
| `mission_plan_id` | `UUID` | No | FK to `drone_mission_plans`. |
| `sequence_number` | `INTEGER` | No | Positive order within the plan; unique per mission plan. |
| `component_reference` | `VARCHAR(200)` | No | Asset/component or surface being inspected. |
| `waypoint_latitude` | `NUMERIC(10,7)` | Yes | Latitude where a waypoint is specified. |
| `waypoint_longitude` | `NUMERIC(10,7)` | Yes | Longitude where a waypoint is specified. |
| `waypoint_altitude_m` | `NUMERIC(10,3)` | Yes | Planned altitude reference, explicitly identified as AGL/AMSL in the plan. |
| `camera_heading_degrees` | `NUMERIC(7,3)` | Yes | Planned camera heading where applicable. |
| `gimbal_pitch_degrees` | `NUMERIC(7,3)` | Yes | Mission-specific gimbal pitch; not constrained to a fixed list of angles. |
| `target_gsd_mm_per_pixel` | `NUMERIC(12,6)` | Yes | Optional shot-specific SOW target. |
| `capture_instructions` | `VARCHAR(2000)` | Yes | Human-readable angle, overlap, focus, and evidence notes. |
| `created_at` | `TIMESTAMPTZ` | No | Creation time. |

Constraints: unique `(mission_plan_id, sequence_number)`; waypoint latitude/longitude, when supplied, must be supplied together and fall within valid geographic ranges. A manual-flight plan may contain shot items without waypoint coordinates. Gimbal and camera parameters are validated for the selected equipment and flight plan.

#### `inspection_assignments`

| Column | Type | Null | Constraint or purpose |
| --- | --- | --- | --- |
| `id` | `UUID` | No | Assignment attempt. |
| `service_order_id` | `UUID` | No | Confirmed inspection order. |
| `inspector_user_id` | `UUID` | No | Assigned Inspector (must belong to the winning Provider). |
| `assigned_by_user_id` | `UUID` | No | `PROVIDER_MANAGER`. |
| `status` | `VARCHAR(24)` | No | `PENDING`, `ACCEPTED`, `REJECTED`, `CANCELLED`, or `COMPLETED`. |
| `deadline` | `TIMESTAMPTZ` | Yes | Assignment deadline. |
| `access_instructions` | `VARCHAR(2000)` | Yes | Assignment package instructions. |
| `responded_at` | `TIMESTAMPTZ` | Yes | Accept/reject time. |
| `rejection_reason` | `VARCHAR(1000)` | Yes | Required when rejected. |

Constraint: only one pending or accepted Inspector assignment per service order; a rejected assignment remains as history.

### 6.4 WF3 inspection, evidence, findings, and reports

#### `inspections`

Columns: `id`, unique `service_order_id`, unique `accepted_assignment_id`, `asset_id`, `author_user_id`, `checklist_template_id`, `status`, optional `started_at`, optional `completed_at`, and mutable aggregate columns.

#### `checklist_responses`

Columns: `id`, `inspection_id`, `checklist_item_id`, `response_value JSONB`, optional `notes`, `completed_by_user_id`, `completed_at`, and `created_at`/`updated_at`.

Constraints: unique `(inspection_id, checklist_item_id)`; value shape must match the checklist item's response type.

#### `evidence`

| Column | Type | Null | Constraint or purpose |
| --- | --- | --- | --- |
| `id` | `UUID` | No | Primary key. |
| `inspection_id` | `UUID` | Yes | Inspection owner. |
| `maintenance_work_log_id` | `UUID` | Yes | Maintenance owner. |
| `uploaded_by_user_id` | `UUID` | No | Assigned field worker. |
| `evidence_kind` | `VARCHAR(32)` | No | `INSPECTION`, `BEFORE_MAINTENANCE`, `AFTER_MAINTENANCE`, or `OTHER`. |
| `file_name` | `VARCHAR(500)` | No | Original file name. |
| `content_type` | `VARCHAR(160)` | No | Validated media type. |
| `size_bytes` | `BIGINT` | No | Positive file size. |
| `checksum_sha256` | `CHAR(64)` | No | Duplicate-detection checksum. |
| `object_key` | `VARCHAR(1000)` | No | Unique MinIO object key. |
| `capture_time` | `TIMESTAMPTZ` | Yes | Original capture time. |
| `source` | `VARCHAR(32)` | No | SD card, web upload, mobile upload, or imported source. |
| `latitude` | `NUMERIC(9,6)` | Yes | Optional GPS metadata. |
| `longitude` | `NUMERIC(9,6)` | Yes | Optional GPS metadata. |
| `external_reference` | `VARCHAR(200)` | Yes | Optional external mission/reference value. |
| `upload_status` | `VARCHAR(24)` | No | `UPLOADING`, `AVAILABLE`, `FAILED`, or `QUARANTINED`. |

Constraints: exactly one parent is set; partial unique indexes prevent duplicate checksums inside the same inspection or maintenance work log.

#### `ai_finding_candidates`

Columns: `id`, `evidence_id`, `model_name`, `model_version`, `predicted_label`, `confidence NUMERIC(6,5)`, `bounding_box JSONB`, `status`, optional `reviewed_by_user_id`, optional `reviewed_at`, optional `rejection_reason`, and `created_at`.

Constraints: confidence is between zero and one; candidate status is `PENDING`, `CONFIRMED`, `MODIFIED`, or `REJECTED`.

#### `verified_findings`

| Column | Type | Null | Constraint or purpose |
| --- | --- | --- | --- |
| `id` | `UUID` | No | Official finding identifier. |
| `inspection_id` | `UUID` | No | Owning inspection. |
| `evidence_id` | `UUID` | Yes | Supporting evidence. |
| `ai_candidate_id` | `UUID` | Yes | Source candidate; null for manual findings. |
| `created_by_user_id` | `UUID` | No | Inspector who verified/created it. |
| `source` | `VARCHAR(24)` | No | `AI_CONFIRMED`, `AI_MODIFIED`, or `MANUAL`. |
| `finding_code` | `VARCHAR(64)` | No | Unique within the inspection. |
| `defect_label` | `VARCHAR(160)` | No | Verified classification. |
| `severity` | `VARCHAR(16)` | No | `LOW`, `MEDIUM`, `HIGH`, or `CRITICAL`. |
| `location_description` | `VARCHAR(1000)` | No | Defect location. |
| `bounding_box` | `JSONB` | Yes | Verified image coordinates. |
| `technical_notes` | `VARCHAR(4000)` | No | Inspector conclusion. |
| `recommended_action` | `VARCHAR(4000)` | Yes | Recommended next action. |
| `status` | `VARCHAR(24)` | No | `OPEN`, `IN_MAINTENANCE`, or `RESOLVED`. |
| `resolved_at` | `TIMESTAMPTZ` | Yes | Resolution time. |

Constraints: unique `(inspection_id, finding_code)`; manual findings must not reference a candidate; AI-derived findings must reference one.

#### `inspection_reports`

Columns: `id`, unique `inspection_id`, `author_user_id`, `status`, `current_version_number`, and mutable aggregate columns.

#### `report_versions`

| Column | Type | Null | Constraint or purpose |
| --- | --- | --- | --- |
| `id` | `UUID` | No | Version identifier. |
| `report_id` | `UUID` | No | Parent report. |
| `version_number` | `INTEGER` | No | Positive sequential number. |
| `source_version_id` | `UUID` | Yes | Version corrected or revised. |
| `created_by_user_id` | `UUID` | No | Report author. |
| `content_snapshot` | `JSONB` | No | Immutable report content snapshot. |
| `pdf_object_key` | `VARCHAR(1000)` | Yes | Generated report file in MinIO. |
| `status` | `VARCHAR(32)` | No | Draft, `AUTHOR_VERIFIED`, `COMPLETENESS_RETURNED`, `RELEASED`, `REVISION_REQUESTED`, or `ACCEPTED`. |
| `author_verified_by_user_id` | `UUID` | Yes | Report-author Inspector who verified/edited the draft; must equal `created_by_user_id` for submission. |
| `author_verified_at` | `TIMESTAMPTZ` | Yes | Time the author confirmed evidence, findings, checklist and AI-assisted text. |
| `author_verification_snapshot` | `JSONB` | Yes | Version-specific checklist/confirmation flags and edit provenance. |
| `completeness_checked_by_user_id` | `UUID` | Yes | Provider Manager who checked deliverables against SOW. |
| `completeness_checked_at` | `TIMESTAMPTZ` | Yes | Time of Provider Manager completeness check. |
| `completeness_return_reason` | `VARCHAR(2000)` | Yes | Reason returned to author when required deliverables are incomplete. |
| `submitted_at` | `TIMESTAMPTZ` | Yes | Author submission time after verification. |
| `released_at` | `TIMESTAMPTZ` | Yes | Provider Manager release time after completeness check. |
| `accepted_at` | `TIMESTAMPTZ` | Yes | Client acceptance time. |
| `client_decision_by_user_id` | `UUID` | Yes | Authenticated Client who accepted or requested revision; references `users.id`. |
| `client_decision_reason` | `VARCHAR(2000)` | Yes | Required non-blank reason when the version status is `REVISION_REQUESTED`; absent for acceptance. |
| `immutable` | `BOOLEAN` | No | Must be true after acceptance. |

Constraints: unique `(report_id, version_number)`; an accepted version is append-only and cannot be updated.

### 6.5 MF4 dispute arbitration

#### `dispute_tickets`

Target internal complaint records coordinated by `PLATFORM_OPERATOR` under published Platform Terms. The operator's decision is not a court judgment or commercial arbitration award; applicability of consumer law depends on transaction purpose.

| Column | Type | Null | Constraint or purpose |
| --- | --- | --- | --- |
| `id` | `UUID` | No | Primary key. |
| `dispute_number` | `VARCHAR(64)` | No | Unique business identifier (e.g., `DSP-2026-0001`). |
| `order_id` | `UUID` | No | Inspection service order or maintenance order ID. |
| `order_type` | `VARCHAR(32)` | No | `INSPECTION` or `MAINTENANCE`. |
| `raised_by_user_id` | `UUID` | No | FK to `users` (Client admin or Provider manager). |
| `client_organization_id`| `UUID` | No | FK to `organizations`. |
| `provider_organization_id`| `UUID`| No | FK to `provider_organizations`. |
| `category` | `VARCHAR(32)` | No | `QUALITY_DEFECT`, `MISSING_SHOTS`, `AIRSPACE_SAFETY`, `TIMELINESS`, or `BILLING`. |
| `reason` | `VARCHAR(4000)` | No | Detailed explanation of the dispute. |
| `client_claim` | `VARCHAR(4000)` | Yes | Specific relief requested by Client (e.g., reshoot, refund). |
| `provider_response` | `VARCHAR(4000)` | Yes | Explanation submitted by Provider within the response period published for the case. |
| `status` | `VARCHAR(32)` | No | `OPENED`, `UNDER_ARBITRATION`, `RESOLVED`, or `CLOSED`. |
| `resolution_decision` | `VARCHAR(32)` | Yes | `FREE_RESHOOT`, `FULL_REFUND`, or `REJECTED_DISPUTE`. |
| `resolved_by_operator_id` | `UUID` | Yes | FK to `users` (`PLATFORM_OPERATOR` internal complaint handler; not a legal arbitrator). |
| `resolved_at` | `TIMESTAMPTZ` | Yes | Timestamp of recorded internal Platform Terms outcome; external remedies remain available. |
| `resolution_notes` | `VARCHAR(4000)` | Yes | Recorded rationale and terms-based outcome; not a court/arbitration award. |
| `penalty_amount` | `NUMERIC(14,2)` | Yes | Optional contractually/lawfully grounded amount; not automatically imposed by an Operator. |
| `created_at` | `TIMESTAMPTZ` | No | Filing timestamp (pauses acceptance and the payment sequence — workflow state only). |
| `updated_at` | `TIMESTAMPTZ` | No | Last update time. |

Indexes: unique `dispute_number`; index `order_id`; index `status`.

#### `dispute_evidence`

Binds forensic digital evidence to a dispute ticket.

| Column | Type | Null | Constraint or purpose |
| --- | --- | --- | --- |
| `id` | `UUID` | No | Primary key. |
| `dispute_ticket_id` | `UUID` | No | FK to `dispute_tickets`. |
| `uploaded_by_user_id` | `UUID` | No | Submitting party. |
| `evidence_type` | `VARCHAR(32)` | No | `FLIGHT_LOG`, `MINIO_IMAGE`, `CONTRACT_DOCUMENT`, or `DAMAGE_REPORT`. |
| `minio_object_key` | `VARCHAR(1000)` | No | MinIO storage key. |
| `checksum_sha256` | `CHAR(64)` | No | SHA-256 data integrity checksum. |
| `description` | `VARCHAR(1000)` | Yes | Context note. |
| `created_at` | `TIMESTAMPTZ` | No | Creation timestamp. |

### 6.6 MF5 maintenance, billing & warranty

#### `maintenance_tickets`

| Column | Type | Null | Constraint or purpose |
| --- | --- | --- | --- |
| `id` | `UUID` | No | Primary key. |
| `organization_id` | `UUID` | No | Customer scope. |
| `asset_id` | `UUID` | No | Affected asset. |
| `accepted_report_version_id` | `UUID` | No | Client-accepted source report. |
| `created_by_user_id` | `UUID` | No | Client actor. |
| `priority` | `VARCHAR(16)` | No | Shared priority values. |
| `preferred_deadline` | `TIMESTAMPTZ` | Yes | Customer preference. |
| `instructions` | `VARCHAR(4000)` | Yes | Additional customer instructions. |
| `status` | `VARCHAR(40)` | No | Controlled WF4 state. |
| `resolution_decision` | `VARCHAR(32)` | Yes | Accept, rework, or re-inspection. |
| `released_at` | `TIMESTAMPTZ` | Yes | Customer-visible result time. |
| `closed_at` | `TIMESTAMPTZ` | Yes | Final closure time. |

#### `maintenance_ticket_findings`

Columns: `maintenance_ticket_id`, `verified_finding_id`, and `created_at`; composite primary key `(maintenance_ticket_id, verified_finding_id)`.

Rule: every ticket has at least one finding from its accepted report and asset; a finding cannot belong to multiple active tickets.

#### `maintenance_assessments`

Columns: `id`, unique `assessment_assignment_id`, `maintenance_ticket_id`, `engineer_user_id`, `assessment_mode`, `required_work`, `materials_estimate JSONB`, `labor_hours_estimate`, `duration_hours_estimate`, `risk_notes`, `assumptions`, `estimated_cost_min`, `estimated_cost_max`, `currency`, `completed_at`, and immutable record timestamps.

Constraints: assessment mode is `REMOTE` or `ON_SITE`; minimum cost cannot exceed maximum cost.

#### `maintenance_quotations`

Each row is one immutable version. Columns mirror `inspection_quotations` and use `quotation_series_id`, `maintenance_ticket_id`, `maintenance_assessment_id`, `provider_id`, `version_number`, `previous_version_id`, pricing/scope snapshots, payment terms, status, and Client decision metadata.

Constraints: unique `(quotation_series_id, version_number)`; the technical scope must originate from a completed Engineer assessment.

#### `maintenance_orders`

Each row is an immutable approved order version so approved changes never overwrite the previous scope.

| Column | Type | Null | Constraint or purpose |
| --- | --- | --- | --- |
| `id` | `UUID` | No | Order-version identifier. |
| `order_series_id` | `UUID` | No | Stable order identifier. |
| `order_number` | `VARCHAR(64)` | No | Customer-visible number. |
| `maintenance_ticket_id` | `UUID` | No | Parent ticket. |
| `approved_quotation_id` | `UUID` | Yes | Required for the initial version. |
| `provider_id` | `UUID` | No | FK to `provider_organizations`. |
| `change_request_id` | `UUID` | Yes | Required for an approved changed version. |
| `version_number` | `INTEGER` | No | Positive version number. |
| `previous_version_id` | `UUID` | Yes | Prior approved order version. |
| `scope_snapshot` | `JSONB` | No | Approved work scope and materials. |
| `approved_amount` | `NUMERIC(14,2)` | No | Approved contract amount. |
| `locked_commission_rate` | `NUMERIC(7,5)` | No | Uniform Platform commission rate accepted for this maintenance order; copied from policy version. |
| `commission_policy_version` | `VARCHAR(64)` | No | Published uniform commission policy version captured at order confirmation. |
| `locked_terms_snapshot` | `JSONB` | No | Immutable snapshot of accepted maintenance order terms and applicable policy-version identifiers. |
| `locked_warranty_days` | `INTEGER` | Yes | Contract-snapshotted warranty duration (a free-rework time obligation only — no money is ever retained). |
| `warranty_end_date` | `TIMESTAMPTZ` | Yes | Warranty end instant calculated from completion and the locked warranty duration. |
| `currency` | `CHAR(3)` | No | ISO currency code. |
| `payment_terms` | `VARCHAR(2000)` | No | Two-stage milestone payment terms. |
| `status` | `VARCHAR(24)` | No | `CONFIRMED`, `IN_PROGRESS`, `COMPLETED`, `SUPERSEDED`, or `CANCELLED`. |
| `approved_by_user_id` | `UUID` | No | Client actor. |
| `approved_at` | `TIMESTAMPTZ` | No | Approval time. |

Constraints: unique `(order_series_id, version_number)` and unique `(order_number, version_number)`. `locked_commission_rate` and `commission_policy_version` are required on every approved order; `locked_warranty_days` and `warranty_end_date` are populated together once the order is accepted. No funding or retention columns exist — the Platform holds no funds.

#### `maintenance_assignments`

Columns: `id`, `maintenance_ticket_id`, optional `maintenance_order_id`, `engineer_user_id`, `assigned_by_user_id`, `assignment_type`, `status`, optional `deadline`, optional `responded_at`, optional `rejection_reason`, and mutable aggregate columns.

Rules: type is `ASSESSMENT`, `EXECUTION`, or `REWORK`; assessment does not require an order, while execution/rework requires an approved order; only one active assignment per type and ticket.

#### `maintenance_work_logs`

Columns: `id`, `maintenance_ticket_id`, `execution_assignment_id`, `engineer_user_id`, `started_at`, optional `ended_at`, `progress_percent`, `work_summary`, `materials_used JSONB`, `labor_hours`, optional `actual_cost`, `currency`, `status`, optional `submitted_at`, optional `verified_by_user_id`, optional `verified_at`, and mutable aggregate columns.

Constraints: progress is between zero and one hundred; completion requires before/after evidence.

#### `maintenance_change_requests`

| Column | Type | Null | Constraint or purpose |
| --- | --- | --- | --- |
| `id` | `UUID` | No | Primary key. |
| `maintenance_ticket_id` | `UUID` | No | Parent ticket. |
| `work_log_id` | `UUID` | No | Work that discovered the change. |
| `current_order_id` | `UUID` | No | Approved order before the change. |
| `requested_by_user_id` | `UUID` | No | Maintenance Engineer. |
| `reason` | `VARCHAR(2000)` | No | Newly discovered condition. |
| `additional_scope` | `VARCHAR(4000)` | No | Requested additional work. |
| `estimated_cost_delta` | `NUMERIC(14,2)` | Yes | Technical estimate, not final price. |
| `currency` | `CHAR(3)` | Yes | Required with cost delta. |
| `status` | `VARCHAR(24)` | No | Submitted through implemented/rejected lifecycle. |
| `decided_by_user_id` | `UUID` | Yes | Client actor. |
| `decided_at` | `TIMESTAMPTZ` | Yes | Decision time. |
| `decision_reason` | `VARCHAR(2000)` | Yes | Optional customer comment. |

The approved changed order links back through `maintenance_orders.change_request_id`; a second reverse foreign key is intentionally omitted to avoid a circular schema dependency.

#### `invoices`

One row is one electronic invoice. Three types exist under the direct-transfer model (an `invoice_type` CHECK):

| `invoice_type` | Issued by | Billed to | Trigger |
| --- | --- | --- | --- |
| `MAINTENANCE_SERVICE` | Provider (recorded) | Client organization | Accepted maintenance work (existing v1 behaviour). |
| `INSPECTION_SERVICE` | Provider (recorded) | Client organization | Accepted inspection report (MF4-05). |
| `COMMISSION` | Platform | Provider organization | Platform commission $C = r \times B$ plus commission VAT, invoiced after the order reaches `PAID` (MF4-05.4 / MF5-07.4). |

Columns: `id`, unique `invoice_number`, `invoice_type`, `organization_id` (billing customer organization for service invoices), optional `provider_organization_id` (billed party for commission invoices), optional `inspection_service_order_id`, optional `maintenance_order_id`, optional `maintenance_ticket_id`, `currency`, `subtotal`, `tax_amount`, `total_amount`, `status`, `issued_at`, `due_at`, optional `paid_at`, and immutable timestamps.

Constraints: every invoice references exactly one order row (inspection or maintenance, depending on type); a `COMMISSION` invoice additionally references the provider organization it was computed from. Commission is a Provider-side expense and is never added to the Client's bill. Invoice issuance content and timing follow Decree 123/2020/NĐ-CP as amended by Decree 70/2025/NĐ-CP.

### 6.6 Supporting workflow

#### `notifications`

| Column | Type | Null | Constraint or purpose |
| --- | --- | --- | --- |
| `id` | `UUID` | No | Primary key. |
| `recipient_user_id` | `UUID` | No | Notification recipient. |
| `organization_id` | `UUID` | Yes | Optional customer scope. |
| `event_type` | `VARCHAR(96)` | No | Triggering workflow event. |
| `channel` | `VARCHAR(16)` | No | `IN_APP` or `EMAIL`. |
| `title` | `VARCHAR(300)` | No | User-facing title. |
| `body` | `VARCHAR(4000)` | No | User-facing content. |
| `target_path` | `VARCHAR(1000)` | Yes | Authorized application route, never a raw MinIO URL. |
| `status` | `VARCHAR(24)` | No | `PENDING`, `SENT`, `FAILED`, or `READ`. |
| `attempt_count` | `INTEGER` | No | Non-negative delivery attempts. |
| `last_error_code` | `VARCHAR(96)` | Yes | Safe operational error code. |
| `sent_at` | `TIMESTAMPTZ` | Yes | Delivery time. |
| `read_at` | `TIMESTAMPTZ` | Yes | In-app read time. |
| `created_at` | `TIMESTAMPTZ` | No | Creation time. |

Indexes: `(recipient_user_id, status, created_at DESC)` and `(status, created_at)` for delivery workers.

#### `event_publication`

This table is owned by Spring Modulith, not by a JPA business entity. Its schema follows the framework's PostgreSQL event-publication registry and supports reliable event delivery between modules.

### 6.7 Stable value sets

These values are persisted as strings and must use the same names in Java, API contracts, tests, and demo data.

| Field | Values |
| --- | --- |
| User role | `PLATFORM_ADMIN`, `PLATFORM_OPERATOR`, `CLIENT`, `PROVIDER_MANAGER`, `INSPECTOR`, `MAINTENANCE_ENGINEER` |
| Actor zone | `PLATFORM_GOVERNANCE`, `CUSTOMER_ORGANIZATION`, `SERVICE_PROVIDER` |
| User status | `ACTIVE`, `SUSPENDED`, `DISABLED` |
| Asset status | `ACTIVE`, `INACTIVE`, `RETIRED` |
| Template status | `DRAFT`, `ACTIVE`, `RETIRED` |
| Schedule status | `ACTIVE`, `PAUSED`, `DISABLED` |
| Request status | `DRAFT`, `SUBMITTED`, `UNDER_REVIEW`, `REVISION_REQUIRED`, `QUOTED`, `AWAITING_CLIENT_APPROVAL`, `ORDER_CONFIRMED`, `ASSIGNMENT_PENDING`, `READY_FOR_INSPECTION`, `MANUAL_REVIEW`, `CANCELLED` |
| Quotation status | `DRAFT`, `SENT`, `REVISION_REQUESTED`, `APPROVED`, `REJECTED`, `SUPERSEDED` |
| Inspection order status | `CONFIRMED`, `ASSIGNMENT_PENDING`, `READY_FOR_INSPECTION`, `READY_FOR_FLIGHT`, `IN_PROGRESS`, `COMPLETED`, `AWAITING_PAYMENT`, `PAID`, `DISPUTED`, `CANCELLED` |
| Assignment status | `PENDING`, `ACCEPTED`, `REJECTED`, `CANCELLED`, `COMPLETED` |
| Inspection status | `READY_FOR_INSPECTION`, `IN_PROGRESS`, `AWAITING_AI_REVIEW`, `AWAITING_REPORT`, `COMPLETED`, `CANCELLED` |
| Target report-version status | `DRAFT`, `AUTHOR_VERIFIED`, `COMPLETENESS_RETURNED`, `RELEASED`, `REVISION_REQUESTED`, `ACCEPTED` |
| Finding severity | `LOW`, `MEDIUM`, `HIGH`, `CRITICAL` |
| Finding status | `OPEN`, `IN_MAINTENANCE`, `RESOLVED` |
| Maintenance ticket status | `SUBMITTED`, `ASSESSMENT_PENDING`, `ASSESSED`, `QUOTATION_PENDING`, `AWAITING_CLIENT_APPROVAL`, `ORDER_CONFIRMED`, `EXECUTION_PENDING`, `IN_PROGRESS`, `CHANGE_PENDING`, `INTERNAL_REVIEW`, `RELEASED`, `REWORK_REQUESTED`, `REINSPECTION_REQUESTED`, `CLOSED`, `CANCELLED` |
| Maintenance assignment type | `ASSESSMENT`, `EXECUTION`, `REWORK` |
| Work-log status | `IN_PROGRESS`, `PAUSED_FOR_CHANGE`, `SUBMITTED`, `VERIFIED` |
| Change-request status | `SUBMITTED`, `QUOTED`, `APPROVED`, `REJECTED`, `IMPLEMENTED` |
| Invoice status | `DRAFT`, `ISSUED`, `PAID`, `OVERDUE`, `VOID` |
| Mission plan status | `DRAFT`, `SUBMITTED`, `REVISION_REQUIRED`, `APPROVED`, `CANCELLED`, `SUPERSEDED` |
| Airspace check status | `NOT_CHECKED`, `CLEARANCE_REQUIRED`, `MANUAL_REVIEW`, `CLEARED`, `BLOCKED` |
| Platform configuration status | `DRAFT`, `PUBLISHED`, `SUPERSEDED`, `RETIRED` |

## 7. Critical database constraints

The following rules must exist in the database where relational checks are practical, and must also be enforced in the domain/application service:

| Rule | Enforcement |
| --- | --- |
| Asset code unique within organization | Unique `(organization_id, code)`. |
| One periodic request per due cycle | Partial unique `(asset_id, schedule_id, due_cycle)` for `PERIODIC`. |
| Quotation/order/report versions are retained | Unique series/version keys; final versions are append-only. |
| Rejected assignment has a reason | Check constraint tied to assignment status. |
| Evidence is not duplicated in one work context | Partial unique parent/checksum indexes. |
| AI candidate is not an official defect | Only `verified_findings` feed reports and tickets. |
| Report release requires author verification and Provider Manager completeness check | State transition validation requires an author-verification snapshot and a successful SOW deliverable check by Provider Manager. |
| Ticket contains at least one accepted-report finding | Transactional service validation plus join-table constraint. |
| Assessment and execution are distinct assignments | `assignment_type` and active-assignment uniqueness. |
| Additional work waits for Client approval | State-transition service checks using an approved changed order version. |
| Ticket closure requires before/after evidence | Transactional query and workflow test. |
| Cross-organization access is denied | Organization-scoped repository queries, not in-memory filtering. |

## 8. Index strategy

Create indexes only for demonstrated authorization, workflow, scheduler, and cleanup queries:

- Every foreign key used for scoped lookup receives a B-tree index.
- Customer lists start with `organization_id` followed by status/date or a stable sort key.
- Assignment inboxes use `(assignee_user_id, status, deadline)`.
- Scheduler polling uses `(status, next_due_at)`.
- Report and quotation version lookup uses `(parent_or_series_id, version_number DESC)`.
- Evidence checksum indexes are scoped by the owning inspection or work log.
- Audit queries use entity/user plus descending time.
- Cleanup jobs use token/session expiry columns.

Do not add indexes for every enum or boolean. Verify expensive queries with PostgreSQL query plans before adding composite indexes beyond this baseline.

## 9. Authorization-oriented repository boundaries

The database model supports, but does not replace, application authorization. Repository methods must start from the caller's scope:

- Client queries include `organization_id` from the authenticated principal.
- Inspector queries join the accepted inspection assignment to the signed-in user; report draft verification is scoped to its author Inspector.
- Maintenance Engineer queries join the active assessment/execution assignment to the signed-in user.
- Service Manager queries may cross organizations but only for service workflows.
- Admin queries do not automatically grant customer-workflow mutation privileges.
- Target report release requires the author-verification snapshot and Provider Manager completeness check.

## 10. Transaction and concurrency boundaries

- Creating a periodic request and advancing the schedule occur in one transaction; the unique due-cycle key provides the final idempotency guard.
- Approving a quotation and creating its order occur in one transaction.
- Accepting an assignment uses optimistic locking and active-assignment uniqueness.
- Confirming/modifying an AI candidate and creating a verified finding occur in one transaction.
- Accepting a report locks the accepted version against mutation.
- Approving a maintenance change creates a new order version; it never overwrites an approved version.
- Resolving a maintenance ticket, updating linked findings, and optionally creating a re-inspection request occur in one transaction.
- Notifications are created after the business transition commits through module events; notification failure does not roll back the business transaction.

## 11. Retention and deletion

- Authentication refresh-token history is removed after its operational reuse-detection window.
- Expired sessions may be removed only after related audit needs are satisfied.
- Accepted quotations, orders, report versions, author verification snapshots, assessments, changes, invoices, and audit events are retained as business history.
- MinIO object deletion is coordinated with database retention; deleting a database row alone must not orphan or prematurely expose an object.
- Organization, asset, user, finding, report, and ticket records referenced by business history are disabled or retired rather than hard-deleted.

## 12. Implementation status

As of 2026-09-28, Flyway migrations `V1` through `V11` implement the **v1 physical schema**: 37 application tables plus the Spring Modulith `event_publication` registry. The additional target tables `platform_configurations`, `drone_mission_plans`, and `mission_shot_items`, plus the commercial/technical snapshot columns in this plan, are documentation-only target design and are **not** implemented by those migrations or current JPA entities. The table inventory above includes these target additions, not only the deployed v1 schema. The physical-schema phases are:

| Migration | Physical scope |
| --- | --- |
| `V1`-`V4` | Extensions, event publication, authentication, and role-value alignment. |
| `V5` | WF1 asset catalog and recurring inspection scheduling. |
| `V6` | WF2 requests, attachments, quotations, service orders, and Inspector assignments. |
| `V7` | Historical v1 WF3 schema: inspections, checklist responses, evidence, AI candidates, verified findings, reports, versions, and the v1 report-review records. This is migration history only; it does not define the current target MF3 report workflow. |
| `V8` | WF4 maintenance tickets, findings, assessments, quotations, orders, assignments, work logs, change requests, and invoices. |
| `V9` | Supporting notification delivery records. |
| `V10` | Client actor and revision-reason audit columns on WF3 `report_versions`. |
| `V11` | WF1 schedule proposals and Admin category frequency policy; widens the `assets.status` check for `PENDING_REVIEW` and `REJECTED`. |

Physical tables do not by themselves mean that a workflow is runtime-complete. Every application table in `V1`-`V11`
now has a feature-owned JPA entity and repository: identity tables belong to `users`; WF1 tables to `assets`; WF2
tables to `inspectionrequests`; WF3 tables to `inspections`; WF4 tables to `maintenance`; and notifications to
`notifications`. The Spring Modulith `event_publication` registry remains framework-owned and has no business entity.
The `inspections`, `maintenance`, and `notifications` modules therefore have their persistence model in place. WF3
inspection/evidence, candidate-verification, and report-review/release/acceptance use cases and HTTP APIs are now
implemented; delivery verification is tracked in Report 5. WF1 asset catalog, organization-scoped asset CRUD, asset
documents, asset review, and schedule proposals are implemented; schedule lifecycle and due-cycle publication remain
incremental work. WF4 and notification delivery remain incremental work.
`dashboard` remains a package-only boundary.

## 13. Recommended implementation order

1. **WF1 foundation:** categories, checklist versions/items, assets, documents, and schedules.
2. **WF2 preparation:** requests, attachments, quotations, orders, and Inspector assignments.
3. **MF3 execution:** mission-linked inspection sessions, checklist responses, evidence/telemetry, AI candidates, Inspector-verified findings, author-verified report drafts, Provider Manager completeness checks and released report versions.
4. **WF4 maintenance:** tickets, finding links, assessments, quotations, orders, assignments, work logs, change requests, and invoices.
5. **Supporting workflow:** notifications and the additional general-audit columns.

Each phase should land as a small forward migration and a matching feature-level JPA/test slice. Do not create all planned tables in a single unreviewed migration.

## 14. Source references

- [Report 3 Software Requirement Specification](../reports/report-3-software-requirement-specification/)
- [Capstone Business Flow](business-flows.md)
- [Authentication and Access Control](../backend/authentication-and-authorization.md)
- [Backend Architecture](../backend/architecture.md)
- [AI Agent Rules](../development/ai-agent-rules.md)
