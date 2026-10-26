---
title: "Report 3 - Record of Changes"
document_type: report3-srs-section
weight: 5
source: "report3-software-requirement-specification.docx"
---

# I. Record of Changes

| Date | A* M, D | In charge | Change Description |
| --- | --- | --- | --- |
| 21 Sep 2026 | A | Project Team | Initial SmartDroneInspection Software Requirement Specification baseline. |
| 21 Oct 2026 | M | Project Team | Finalized SRS aligned with the four core roles (ADMIN, ORG_ADMIN, INSPECTOR, MAINTENANCE_ENGINEER), end-to-end workflows (MF1–MF4), AI-assisted defect inspection, and batch maintenance handoff. |
| 22 Oct 2026 | M | Project Team | Simplified MF3 pre-report flow: removed the evidence-quality decision gate and evidence-file SHA-256 requirement; moved Additional Session requests to MF2; made AI analysis Inspector-invoked; required explicit acknowledgment for an empty findings set; moved coverage/limitations into report authoring; aligned version submission/return fields and per-finding maintenance forwarding. Retained inspection scope fields, evidence soft-delete, and published-PDF checksum. This is a requirements/design update; runtime implementation and test outcomes are not implied. |
| 23 Oct 2026 | M | Project Team | Clarified that per-finding forwarding timestamps identify forwarded items while an append-only `audit_events` record preserves the Organization Manager, report version, selected IDs and aggregate status transition. No duplicate handoff fields or no-repair rationale are stored on the inspection. Marked the report-version evidence/finding junction tables as reserved and documented that exact per-version source membership is not currently persisted by runtime. |
| 23 Oct 2026 | M | Hiếu | Documented optional PayPal Orders v2 settlement for enterprise subscriptions while retaining corporate wire/invoice reconciliation. Added V41/V42 migrations. |
| 24 Oct 2026 | M | Như | Documented RAG-assisted maintenance scope and acceptance criteria advisor (`V43__repair_knowledge_base.sql`, `repair_knowledge_chunks`) and full-stack MF4 work order execution, cost reconciliation, and completion report PDF verification. |
| 25 Oct 2026 | M | Project Team | Restructured human roles to five roles (`ADMIN`, `PLATFORM_MANAGER`, `ORG_MANAGER`, `INSPECTOR`, `MAINTENANCE_ENGINEER`) with strict platform-zone separation of duties (`ADMIN` XOR `PLATFORM_MANAGER`), renamed `ORG_ADMIN` to `ORG_MANAGER` (*Organization Manager*), and specified the B2B Drone Leasing lifecycle (`platform_drones`, `drone_leases`, and customer `drones` ownership/lease provisioning and reclaim). |
| 26 Oct 2026 | M | Project Team | Consolidated MF2 database schema and workflows: merged `inspection_readiness_decisions` into `inspection_preparations` (16 columns: `reviewed_by_user_id`, `reviewed_at`, `review_reason`, `status` in `DRAFT`, `SUBMITTED`, `RETURNED`, `READY`, `SUPERSEDED`; dropped transitive `inspector_user_id`), streamlined `field_sessions` (13 columns, linked via `preparation_id`; dropped transitive `inspector_user_id` and `drone_id`), `checklist_responses` (8 columns scoped by `(inspection_id, checklist_item_id)`; dropped transitive `completed_by_user_id`), `checklist_templates` (14 columns), `checklist_items` (14 columns), and `inspections` (18 columns), and aligned §3.4 status vocabulary (`SUBMITTED`, `READY`, `RETURNED`, `SUPERSEDED` on `inspection_preparations`; `PREPARING` and `READY_FOR_FLIGHT` on `inspections`). |

| 26 Oct 2026 | A | Project Team | Clarified BR-09 periodic scheduling as Organization Manager-managed recurrence with original-anchor timezone arithmetic, separate assigned inspections, visible blocked occurrences, scoped pause/resume/end and deduplicated in-app Inspector reminders (default 3 days). Implementation is in progress; no complete API, scheduler or notification acceptance is claimed. |

*A - Added M - Modified D - Deleted
