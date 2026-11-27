---
title: "SmartDroneInspection Documentation"
type: "docs"
---

# SmartDroneInspection

SmartDroneInspection documentation defines the building infrastructure inspection platform across four main workflows (`MF1`–`MF4`) and twenty-four atomic features (`FE-01`–`FE-24`), covering onboarding, quoting, dispatch, flight permits, field sessions, AI defect detection, report publication, Sepay VietQR / VNPay settlement, and post-remediation re-inspection. Direct flight control, 3D photogrammetry, and corrective maintenance execution remain out of scope.

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

- [Main workflow guide](bao-cao-thay-doi-mainflows-5-roles.md) outlines the active lifecycle from partner drone registration and customer onboarding through report acceptance and settlement.
- [Formal reports](reports/):
  - [Report 1 — Project Introduction](reports/report-1-project-introduction/)
  - [Report 2 — Project Management Plan](reports/report-2-project-management-plan/)
  - [Report 3 — Software Requirement Specification (SRS)](reports/report-3-software-requirement-specification/)
  - [Report 4 — Software Design Document (SDD)](reports/report-4-software-design-document/)
  - [Report 5 — Test Documentation](reports/report-5-test-documentation/) & [Report 5 — Software Test Report](reports/report-5-test-report/) & [Unit Tests](reports/report-5-unit-test/)
  - [Report 6 — Software User Guides](reports/report-6-software-user-guides/)
  - [Report 7 — Final Project Report (Assembled wrapper)](reports/report-7-final-project-report/)
- [Development guide](development/): Git/PR rules and conventions.
- [Export & verification tools](tools/): Python OOXML exporters and verification suites.

Repository-specific setup commands are maintained in the `README.md` and `AGENTS.md` files of the backend, frontend, and mobile repositories.
