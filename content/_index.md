---
title: "SmartDroneInspection Documentation"
type: "docs"
---

# SmartDroneInspection

SmartDroneInspection is an infrastructure inspection management platform for the full lifecycle from assets and planning to uploaded inspection evidence, reports, defects, and maintenance tickets.

Inspection images are uploaded through the web or mobile application. The platform stores authorized evidence in MinIO and can submit eligible images to the YOLO analysis service.

## Architecture at a glance

- Java 21 and Spring Boot modular monolith with Spring Modulith.
- PostgreSQL is the source of truth; MinIO stores inspection evidence and images.
- React 19 web portal and Flutter mobile app share the versioned REST API.
- Feature modules own their API, domain, application services, and persistence adapters.
- Authorization combines role checks with organization and assignment scope.

## Roles

- Platform Administrator
- Organization Manager
- Service Operations Manager
- Inspector
- Maintenance Engineer

## Documentation map

- [Project reference](project-reference/)
  - [Report 3 SRS for AI](project-reference/markdown/report3-software-requirement-specification.md)
  - [Business flow for AI](project-reference/markdown/capstone-business-flow.md)
  - [Report 3 source DOCX](project-reference/source-documents/Report3_Software_Requirement_Specification_SmartDroneInspection.docx)
  - [Business flow source DOCX](project-reference/source-documents/Capstone-reports-businessflow.docx)
- [System architecture](architecture/)
- [Backend architecture](architecture/backend-architecture/)
- [Frontend architecture](architecture/frontend-architecture/)
- [Mobile architecture](architecture/mobile-architecture/)
- [Security](security/)
  - [Authentication and access control](security/authentication/)
- [Coding conventions](coding-conventions/)

Repository-specific setup commands are maintained in the `README.md` files of the backend, frontend, and mobile repositories.
