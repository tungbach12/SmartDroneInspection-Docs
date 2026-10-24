# MF3 Entity Field Audit and Table Streamlining

**Owner:** Bach (natsumeeei)  
**Date:** 2026-10-22 (Updated: 2026-10-24)  
**Status:** COMPLETED  
**Branch:** `docs/streamline-mf3-tables` / `refactor/streamline-mf3-tables`  
**Domain Scope:** Main Flow 3 (FE-04 Field Evidence, FE-05 Defect Findings, FE-06 Inspection Reports)  
**Entities Audited:** `evidence`, `findings`, `inspection_reports`  

---

## 1. Objective and Context

The MF3 domain entities underwent a comprehensive field audit to eliminate redundant foreign keys, retire unused status columns and intermediate states, streamline AI model provenance, and standardize soft-delete semantics across all three core tables.

### Key Goals:
1. **Reduce Schema Bloat**: Eliminate foreign keys and columns that can be deterministically resolved through parent aggregates (e.g., resolving organization and author via `inspections`).
2. **Standardize Soft Deletes**: Replace fragmented, inconsistent soft-delete timestamps (`retired_at`, `deleted_at`) with uniform boolean flags (`is_deleted`, defaulting to `false`).
3. **Decouple Cross-Domain Links**: Remove legacy maintenance foreign keys from inspection evidence to cleanly isolate inspection captures from MF4 maintenance remediation.
4. **Simplify Report Versioning**: Consolidate version records directly into `inspection_reports` with linear `version_no` ordering, dropping obsolete self-referential parent version IDs and withdrawal metadata.

---

## 2. Streamlined Table Audits

### 2.1 `evidence` Table (13 Columns)

Stores digital capture metadata for images and media recorded during inspection field sessions and stored in MinIO.

#### Final Column Inventory:
| # | Column Name | Data Type | Nullable | Default | Description |
| - | :--- | :--- | :---: | :--- | :--- |
| 1 | `id` | `uuid` | No | `gen_random_uuid()` | Primary key. Unique identifier of the evidence item. |
| 2 | `inspection_id` | `uuid` | No | — | Foreign key to `inspections(id)`. Authoritative tenant anchor. |
| 3 | `field_session_id` | `uuid` | Yes | `NULL` | Foreign key to `field_sessions(id)`. Optional link to on-site flight session. |
| 4 | `file_name` | `varchar(500)` | No | — | Sanitized original media filename. |
| 5 | `content_type` | `varchar(160)` | No | — | MIME content type (e.g. `image/jpeg`). |
| 6 | `size_bytes` | `bigint` | No | — | File size in bytes (> 0). |
| 7 | `object_key` | `varchar(1000)` | No | — | MinIO object storage path/key. |
| 8 | `capture_time` | `timestamptz` | Yes | `NULL` | EXIF capture timestamp. |
| 9 | `latitude` | `numeric(9,6)` | Yes | `NULL` | GPS latitude coordinate (-90 to +90). |
| 10 | `longitude` | `numeric(9,6)` | Yes | `NULL` | GPS longitude coordinate (-180 to +180). |
| 11 | `location_description` | `varchar(1000)` | Yes | `NULL` | Structural location notes (e.g. `Span 4 East Face`). |
| 12 | `is_deleted` | `boolean` | No | `false` | Soft-delete boolean flag. |
| 13 | `created_at` | `timestamptz` | No | `CURRENT_TIMESTAMP` | Row creation timestamp. |

#### Dropped Columns & Rationales:
- `organization_id`: Dropped. Redundant because tenant isolation is strictly resolved through `inspections.organization_id`.
- `upload_status`: Dropped. Media upload and MinIO persistence are atomic; intermediate `UPLOADING` state is unnecessary.
- `evidence_kind`: Dropped. All records in this table represent inspection captures; category is not needed.
- `retired_at`: Replaced by `is_deleted` boolean flag (`false` by default; set to `true` when retired).
- `maintenance_work_log_id`, `maintenance_work_order_id`, `maintenance_task_id`: Dropped. Decouples inspection evidence from MF4 maintenance execution.

---

### 2.2 `findings` Table (15 Columns)

Unified defect observation table managing advisory AI defect proposals and human Inspector-confirmed official findings.

#### Final Column Inventory:
| # | Column Name | Data Type | Nullable | Default | Description |
| - | :--- | :--- | :---: | :--- | :--- |
| 1 | `id` | `uuid` | No | `gen_random_uuid()` | Primary key. Unique identifier of the finding. |
| 2 | `inspection_id` | `uuid` | No | — | Foreign key to `inspections(id)`. |
| 3 | `evidence_id` | `uuid` | No | — | Foreign key to `evidence(id)`. Supporting capture photo. |
| 4 | `finding_code` | `varchar(64)` | No | — | Inspection-scoped reference identifier (e.g. `FND-001`). |
| 5 | `defect_label` | `varchar(160)` | No | — | Defect classification label (e.g. `Cracking`, `Spalling`). |
| 6 | `severity` | `varchar(24)` | No | — | Defect severity rating: `LOW`, `MEDIUM`, `HIGH`, or `CRITICAL`. |
| 7 | `bounding_box` | `jsonb` | No | — | Bounding box coordinates `{x, y, width, height}`. |
| 8 | `technical_notes` | `varchar(4000)` | No | — | Inspector narrative describing defect dimensions and condition. |
| 9 | `recommended_action` | `varchar(4000)` | Yes | `NULL` | Recommended engineering intervention. |
| 10 | `status` | `varchar(24)` | No | — | Finding lifecycle state: `PENDING` or `CONFIRMED`. |
| 11 | `model_name` | `varchar(160)` | Yes | `NULL` | Detection model identifier (e.g. `YOLO11s`); null for manual observations. |
| 12 | `confidence` | `numeric(6,5)` | Yes | `NULL` | Model prediction confidence score (0.0 to 1.0). |
| 13 | `forwarded_to_maintenance_at` | `timestamptz` | Yes | `NULL` | Timestamp when finding was forwarded to MF4 remediation triage. |
| 14 | `is_deleted` | `boolean` | No | `false` | Soft-delete boolean flag. |
| 15 | `created_at` | `timestamptz` | No | `CURRENT_TIMESTAMP` | Row creation timestamp. |

#### Dropped Columns & Rationales:
- `updated_at`: Dropped. Finding lifecycle changes are represented cleanly through status transitions and creation timestamps.
- `deleted_at`: Replaced by `is_deleted` boolean flag.
- `inspector_confirmed_at`: Dropped. Official confirmation is directly represented by `status = 'CONFIRMED'`.
- `model_version`, `model_provider`: Dropped. `model_name` and `confidence` provide sufficient AI provenance without unnecessary metadata overhead.

---

### 2.3 `inspection_reports` Table (13 Columns)

Versioned inspection report deliverables, content snapshots, review gates, and published PDF deliverable references.

#### Final Column Inventory:
| # | Column Name | Data Type | Nullable | Default | Description |
| - | :--- | :--- | :---: | :--- | :--- |
| 1 | `id` | `uuid` | No | `gen_random_uuid()` | Primary key. Unique report version identifier. |
| 2 | `inspection_id` | `uuid` | No | — | Foreign key to `inspections(id)`. |
| 3 | `version_no` | `integer` | No | — | 1-based sequential version number (> 0). |
| 4 | `status` | `varchar(32)` | No | — | Version state: `DRAFT`, `AUTHOR_VERIFIED`, `SUBMITTED`, `RETURNED`, `APPROVED`, `PUBLISHED`, `SUPERSEDED`. |
| 5 | `content_snapshot` | `jsonb` | No | `'{}'::jsonb` | Structured JSON containing authored report sections. |
| 6 | `submitted_at` | `timestamptz` | Yes | `NULL` | Submission timestamp for administrative review. |
| 7 | `reviewer_user_id` | `uuid` | Yes | `NULL` | Foreign key to `users(id)` for the reviewing Organization Admin. |
| 8 | `reviewed_at` | `timestamptz` | Yes | `NULL` | Administrative review decision timestamp. |
| 9 | `return_reason` | `varchar(2000)` | Yes | `NULL` | Reviewer comments recorded when status is `RETURNED`. |
| 10 | `rendered_object_key` | `varchar(1000)` | Yes | `NULL` | MinIO object key for the published immutable PDF deliverable. |
| 11 | `rendered_checksum_sha256` | `char(64)` | Yes | `NULL` | Cryptographic SHA-256 digest of published PDF. |
| 12 | `published_at` | `timestamptz` | Yes | `NULL` | Publication timestamp. |
| 13 | `created_at` | `timestamptz` | No | `CURRENT_TIMESTAMP` | Row creation timestamp. |

#### Dropped Columns & Rationales:
- `author_user_id`: Dropped. Author identity is deterministically resolved through `inspections.inspector_id`.
- `source_version_id`: Dropped. Clean linear sequencing via `version_no` per inspection renders parent version pointers redundant.
- `withdrawn_at`, `withdrawal_reason`: Dropped. Author withdrawal simply reverts a report version from `SUBMITTED` back to `DRAFT`.

---

## 3. Database Constraints and Indexes

### Index Strategy:
```sql
-- evidence: inspection captures ordered by creation
CREATE INDEX ix_evidence_inspection_time ON evidence USING btree (inspection_id, created_at DESC);

-- findings: findings query by inspection and status
CREATE INDEX ix_findings_inspection_status ON findings USING btree (inspection_id, status);

-- inspection_reports: version lookup by inspection and status
CREATE INDEX ix_inspection_reports_inspection_status ON inspection_reports USING btree (inspection_id, status, version_no DESC);
```

### Foreign Key Constraints:
- `evidence(inspection_id)` -> `inspections(id)` ON DELETE RESTRICT
- `evidence(field_session_id)` -> `field_sessions(id)` ON DELETE RESTRICT
- `findings(inspection_id)` -> `inspections(id)` ON DELETE RESTRICT
- `findings(evidence_id)` -> `evidence(id)` ON DELETE RESTRICT
- `inspection_reports(inspection_id)` -> `inspections(id)` ON DELETE RESTRICT
- `inspection_reports(reviewer_user_id)` -> `users(id)` ON DELETE RESTRICT

---

## 4. Completion Checklist

- [x] Audited all MF3 entity attributes against domain and workflow requirements
- [x] Streamlined `evidence` table down to 13 essential columns
- [x] Streamlined `findings` table down to 15 essential columns
- [x] Streamlined `inspection_reports` table down to 13 essential columns
- [x] Standardized soft deletes via `is_deleted` boolean flags
- [x] Dropped obsolete foreign keys (`organization_id`, `author_user_id`, maintenance FKs)
- [x] Updated backend domain entities (`Evidence.java`, `Finding.java`, `InspectionReportVersion.java`)
- [x] Updated backend DTOs, controllers, services, repositories, and integration test fixtures
- [x] Synchronized `project-reference/database-design.md`
- [x] Synchronized `reports/report-4-software-design-document/02-database-design.md`
- [x] Synchronized `reports/report-3-software-requirement-specification/03-functional-requirements.md`
