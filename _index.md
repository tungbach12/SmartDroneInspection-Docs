---
title: "SmartDroneInspection Documentation"
type: "docs"
---

# SmartDroneInspection

SmartDroneInspection is an infrastructure inspection management platform for the lifecycle from assets and planning to evidence, reports, findings, and maintenance tickets.

## Architecture at a glance

- Java 21 and Spring Boot modular monolith with Spring Modulith.
- PostgreSQL is the source of truth; MinIO stores inspection evidence and images.
- React 19 web portal and Flutter mobile app share the versioned REST API.
- Feature modules own their API, domain, application services, and persistence adapters.
- Authorization combines role checks with organization and assignment scope.

## Roles

- Admin
- Client
- Service Manager
- Inspector
- Maintenance Engineer

## Documentation map

- [Project reference](project-reference/): project reports, workflows, data model, and guides.
- [Backend](backend/): architecture, authentication, and Java/Spring conventions.
- [Frontend](frontend/): architecture and React/TypeScript conventions.
- [Mobile](mobile/): architecture and Flutter/Dart conventions.
- [Development guide](development/): shared AI-agent, Git, and pull-request rules.
- [Testing](testing/): editable Report 5 test cases, execution rounds, statistics, and the preserved workbook template.

Repository-specific setup commands are maintained in the `README.md` files of the backend, frontend, and mobile repositories.
