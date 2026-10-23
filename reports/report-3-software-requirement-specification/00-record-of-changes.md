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
| 23 Oct 2026 | M | Project Team | Clarified that per-finding forwarding timestamps identify forwarded items while an append-only `audit_events` record preserves the Organization Admin, report version, selected IDs and aggregate status transition. No duplicate handoff fields or no-repair rationale are stored on the inspection. Marked the report-version evidence/finding junction tables as reserved and documented that exact per-version source membership is not currently persisted by runtime. |
| 23 Oct 2026 | M | Hiếu | Documented optional PayPal Orders v2 settlement for enterprise subscriptions while retaining corporate wire/invoice reconciliation. Added V41/V42 migrations. |

*A - Added M - Modified D - Deleted
