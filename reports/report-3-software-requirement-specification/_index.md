---
title: "Report 3 SRS"
document_type: report3-srs
weight: 10
---

# Report 3 - Software Requirement Specification

This folder is the team-maintained Markdown source of Report 3. **Current revision: 23 November 2026 — Platform Inspection Service model, 4 implemented login roles (`ADMIN`, `MANAGER`, `CUSTOMER`, `INSPECTOR`), 24 atomic product features (`FE-01`–`FE-24`) across 4 connected Main Flows (`MF1`–`MF4`), and Flyway `V1`–`V4` + `V60`–`V69` (`assets.ownership_information`, `service_payments.gateway_order_created_at`, `gateway_inbound_transactions`, `inspection_flight_permits`, `field_session_telemetry`, the `FE-06` `AssetResponse.checkpointsLocked` contract, and MF2 flow alignment for ADMIN-only airspace review, quote-to-dispatch partner selection, and shared chat attachment limits).** `MAINTENANCE_ENGINEER` and the corrective-maintenance capability are planned and out of the current release scope; the four implemented roles are the only login roles in the backend enum, JWT constants, and account administration. Maintenance is outside current application scope; legacy maintenance schema and data remain preserved but are not exposed by the application.

## Sections

- [Record of Changes](00-record-of-changes.md)
- [Overall Description](01-overall-description.md)
- [User Requirements](02-user-requirements.md)
- [Functional Requirements](03-functional-requirements.md)
- [Non-Functional Requirements](04-non-functional-requirements.md)
- [Requirement Appendix](05-requirement-appendix.md)

Use `python -I tools/export_report3.py` to generate the official Word package from these six ordered section sources.
