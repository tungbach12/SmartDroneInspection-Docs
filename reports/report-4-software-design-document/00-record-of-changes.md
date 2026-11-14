---
title: "Report 4 - Record of Changes"
document_type: report4-sdd-section
weight: 5
source: "report4-software-design-document.docx"
---

# I. Record of Changes

| Date | A* M, D | In charge | Change Description |
| --- | --- | --- | --- |
| 03 Nov 2026 | A | Project Team | Version 1.0: Initial release of the Software Design Document (SDD) for SmartDroneInspection covering System Design, Database Design (36 PostgreSQL 17 tables across V1–V28), and Detailed Design for the 8 product features (FE-01 to FE-08). |
| 05 Nov 2026 | M | Project Team | Updated the database design for migration V29: separated per-occurrence service invoices, customer payments, and Inspector payouts into three dedicated tables; the V29 target schema has 38 application tables plus `event_publication` and `flyway_schema_history` (40 total). |
| 11 Nov 2026 | M | Project Team | Removed maintenance application workflows from the target design. Legacy maintenance schema and persisted data are preserved without destructive migration and are not exposed by the application. |
| 11 Nov 2026 | M | Project Team | Added Flyway migrations V34–V36 for Admin-configurable drone document requirements (`drone_document_configs`), Admin-configurable drone features/safety checklist (`drone_feature_configs`), and JSONB/scalar capability, image, and document columns on `drone_registration_applications` and `drones` (32 active application tables; 34 total tables including `event_publication` and `flyway_schema_history`). |
| 11 Nov 2026 | M | Project Team | Updated FE-06 detailed finance design and database description for payout eligibility vs. actual disbursement, gateway order resolution, external refund ledger, refund payout hold, and attributed final payout reconciliation (renumbered to V44 on merge). |
| 12 Nov 2026 | M | Project Team | Updated the database and detailed design for refund allocation (V45) and refund lifecycle/receivables (V46): added refund status and initiation/completion/cancellation attribution to `service_refunds`, added `inspector_receivables` and `inspector_receivable_recoveries` for post-payout refunds without automatic future offset, added individual legacy allocation reconciliation by refund ID, and documented the four distinct Contracts UI forms. |
|  |  |  |  |
|  |  |  |  |
|  |  |  |  |

*A - Added M - Modified D - Deleted
