---
title: "SmartDroneInspection Documentation"
type: "docs"
---

# SmartDroneInspection

SmartDroneInspection documentation defines the target for a platform-managed infrastructure inspection and corrective maintenance service across `MF1`–`MF4` and 8 features (`FE-01`–`FE-08`). This target description is not a claim that all workflows are implemented.

## Architecture at a glance

- Java 21 and Spring Boot 4.1 modular monolith with Spring Modulith.
- PostgreSQL 17 (`pgvector`) is the source of truth; MinIO stores inspection evidence (photos & MP4 videos), permits, signed contracts, and immutable PDF reports.
- React 19 web portal (`/admin`, `/manager`, `/client`, `/operations`) and Customer-only Flutter mobile app share the versioned REST API and Google OAuth2 / JWT authentication.
- Online VietQR / bank-card settlement via Sepay / VNPay after Customer report acceptance.
- Authorization combines the 4 login roles (`ADMIN`, `MANAGER`, `CUSTOMER`, `INSPECTOR`) with ownership (`ownerCustomerId`), assignment (`inspectorId`), and separation-of-duties scope.

## Roles

- `ADMIN` (system administration, catalog/airspace governance, and account management)
- `MANAGER` (partner onboarding review, service-request quotes, dispatch, report review/publication)
- `CUSTOMER` (direct customer account managing assets, service requests, report acceptance, and settlement; no organization hierarchy)
- `INSPECTOR` (partner drone inspector owning drones, flight permits, field sessions, evidence, findings, and report submission)

## Documentation map

- [Project reference](project-reference/): workflows, error-prevention checks, and mainflow references.
- [Mainflows & Role Architecture](bao-cao-thay-doi-mainflows-5-roles.md): target workflow and implementation comparison for `MF1`–`MF4` and 8 features (`FE-01`–`FE-08`); the file keeps its historical name but the implemented login roles are the four listed above, with `MAINTENANCE_ENGINEER` planned.
- [Diagram assignments](phan-cong-ve-so-do.md): 35-diagram ownership map across the 8 features.
- [Formal reports](reports/):
  - [Report 1 — Project Introduction](reports/report-1-project-introduction/)
  - [Report 2 — Project Management Plan](reports/report-2-project-management-plan/)
  - [Report 3 — Software Requirement Specification (SRS)](reports/report-3-software-requirement-specification/)
  - [Report 4 — Software Design Document (SDD)](reports/report-4-software-design-document/)
  - [Report 5 — Software Test Report](reports/report-5-test-report/)
- [Development guide](development/): Git/PR rules and implementation plans.
- [Export & verification tools](tools/): Python OOXML exporters and verification suites.

Repository-specific setup commands are maintained in the `README.md` and `AGENTS.md` files of the backend, frontend, and mobile repositories.
