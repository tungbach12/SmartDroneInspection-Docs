---
title: "Report 4 - Record of Changes"
document_type: report4-sdd-section
weight: 5
source: "report4-software-design-document.docx"
---

# I. Record of Changes

| Date | A* M, D | In charge | Change Description |
| --- | --- | --- | --- |
| 21 Sep 2026 | A | Project Team | Initial SmartDroneInspection Software Design Document baseline. |
| 21 Oct 2026 | M | Project Team | Finalized Software Design Document specifying system architecture, Spring Modulith packages, PostgreSQL database schema, class specifications, and sequence diagrams for all core features. |
| 26 Oct 2026 | M | Project Team | Consolidated database architecture to **30 application tables** (26 in baseline + 2 drone leasing + 2 recurring schedule tables `recurring_inspection_schedules` and `schedule_occurrences`), applied forward WF1 column cleanup (`V3__drop_unused_wf1_columns.sql`), and streamlined MF1–MF2: dropped 8 intermediary tables (`checklist_templates`, `checklist_items`, `checklist_responses`, `inspection_preparations`, `asset_pair_assignments`, `flight_permits`, `drone_documents`, `workforce_credentials`); added `inspection_items` to `assets`, direct registration columns to `drones`, self-declared pilot license columns to `users`, self-service flight permit file attributes and `recurring_schedule_id` to `inspections`, and decoupled `field_sessions` from preparations. |
*A - Added M - Modified D - Deleted
