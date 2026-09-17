---
title: "SmartDroneInspection Documentation"
type: "docs"
---

# SmartDroneInspection

SmartDroneInspection is an infrastructure inspection management platform for the full lifecycle from assets and planning to drone missions, reports, defects, and maintenance tickets.

The backend consumes SmartDroneHub through REST APIs. Drone flight control, telemetry collection, and mission execution remain responsibilities of SmartDroneHub.

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

## Quick links

- [System specification](https://github.com/tungbach12/SmartDroneInspection-Docs/blob/main/01-SYSTEM-SPECIFICATION.md)
- [Getting started](getting-started/)
- [Architecture](architecture/)
- [Authentication](authentication/)
- [Architecture decisions](architecture-decisions/)
