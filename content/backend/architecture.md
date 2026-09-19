---
title: "Backend Architecture"
weight: 10
aliases:
  - /architecture/backend-architecture/
---

# Backend Architecture

The backend is a Java 21 Spring Boot modular monolith. Spring Modulith verifies the boundaries between direct feature packages so each team-owned capability stays focused.

## Capability modules

By default, each direct package under `com.smartdroneinspection` is one Spring
Modulith application module. A module represents a business capability, not a
workflow number or a group of tables.

```text
com.smartdroneinspection/
|-- users/                 # Current: identity and administration
|-- assets/                # Current: WF1
|-- inspectionrequests/    # Current: WF2
|-- shared/                # Current: minimal cross-cutting contracts
|-- inspections/           # Planned with the first WF3 runtime slice
|-- maintenance/           # Planned with the first WF4 runtime slice
|-- notifications/         # Planned supporting capability
|-- dashboard/             # Planned read-only query capability
`-- infrastructure/        # Planned outbound adapters
```

| Module | Capability | Runtime status |
| --- | --- | --- |
| `users` | Identity, authentication, and user administration | Implemented |
| `assets` | Asset catalog, checklists, and schedules (WF1) | Entities and repositories implemented |
| `inspectionrequests` | Requests, quotations, orders, and assignments (WF2) | Entities and repositories implemented |
| `inspections` | Execution, evidence, findings, reports, and peer review (WF3) | Schema only; module not created |
| `maintenance` | Assessment, execution, changes, and resolution (WF4) | Schema only; module not created |
| `notifications` | In-app and email notification delivery | Schema only; module not created |

Create a planned module only when its first real runtime slice is ready. Do not
create empty packages for future workflow phases. Each feature owns its domain
models; do not create a global `com.smartdroneinspection.domain` entity package.

## Module visibility and responsibilities

The module root is the default public Java API. Nested packages are internal
unless explicitly exposed with `@NamedInterface`.

| Package | Visibility and responsibility |
| --- | --- |
| `<module>/api` | Internal HTTP controllers and transport DTOs. |
| `<module>/domain` | Internal entities, value objects, enums, and rules. |
| `<module>/repository` | Internal Spring Data repositories and scoped queries. |
| `<module>/service` | Internal use-case orchestration and transactions. |
| `<module>/events` | Public only when marked `@NamedInterface("events")`. |
| `<module>/spi` | Public only when marked `@NamedInterface("spi")`. |

Another module must not import a controller, HTTP DTO, entity, repository, or
service from a different module. Cross-module calls use a facade in the module
root or a named interface. `ApplicationModules.verify()` is the build-time guard.

Shared code is limited to cross-cutting concerns such as error handling, security configuration, result types, and pagination. It must not become a shared home for feature entities or use cases.

## Dependency direction

```text
users -------------------------------> shared
assets ------------------------------> shared
inspectionrequests ------------------> assets, shared
inspections -------------------------> inspectionrequests, assets, shared
maintenance -------------------------> inspections, inspectionrequests, shared
notifications -----------------------> feature::events
dashboard ---------------------------> feature root read APIs
infrastructure ----------------------> feature::spi, shared
```

Business modules never import `infrastructure`; adapters implement ports owned by
the feature. WF1 and WF2 must not form a cycle. When periodic request generation
is implemented, `assets` publishes `assets::events InspectionScheduleDue`,
`inspectionrequests` listens and creates the request, and `inspectionrequests`
may synchronously call an `assets` root facade for immediate validation. Add that
event and facade with the periodic-request use case, not as speculative plumbing.

## Persistence and integrations

PostgreSQL is the source of truth. Flyway owns schema migrations, and MinIO stores inspection evidence and images. The `infrastructure/` area contains outbound adapters for feature-owned ports. Reports, findings, and AI candidates belong inside WF3; maintenance tickets belong inside `maintenance`; a YOLO client belongs under `infrastructure/ai` when implemented.

Inspection evidence is uploaded through the web or mobile application. The current architecture has no dependency on a separate drone-operation platform.

## Error handling and verification

Expected business failures use `Result<T>` where appropriate. Unexpected failures are converted to RFC 7807 `ProblemDetail` by the global exception handler.

Backend changes should pass `./mvnw verify`, including formatting, tests, JaCoCo coverage, and Modulith boundary verification.
