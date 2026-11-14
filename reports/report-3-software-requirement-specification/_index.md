---
title: "Report 3 SRS"
document_type: report3-srs
weight: 10
---

# Report 3 - Software Requirement Specification

This folder is the team-maintained Markdown source of Report 3. **Current revision: 12 November 2026 — Platform Inspection Service model, 4 canonical login roles (`ADMIN`, `MANAGER`, `CUSTOMER`, `INSPECTOR`), 6 product features (`FE-01`–`FE-06`), 3 connected Main Flows (`MF1`–`MF3`), and explicit payout/refund controls for FE-06.** Maintenance is outside application scope; legacy maintenance schema and data remain preserved but are not exposed by the application.

## Sections

- [Record of Changes](00-record-of-changes.md)
- [Overall Description](01-overall-description.md)
- [User Requirements](02-user-requirements.md)
- [Functional Requirements](03-functional-requirements.md)
- [Non-Functional Requirements](04-non-functional-requirements.md)
- [Requirement Appendix](05-requirement-appendix.md)

Use `python -I tools/export_report3.py` to generate the official Word package from these six ordered section sources.
