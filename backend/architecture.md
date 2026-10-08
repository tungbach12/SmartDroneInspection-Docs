---
title: "Backend Architecture"
weight: 10
aliases:
  - /architecture/backend-architecture/
---

# Backend Architecture

> **Current worktree status — 7 October 2026, `feat/enterprise-saas-reset`:** This page combines target architecture guidance with an older runtime inventory. It is not a claim that the Enterprise SaaS target is implemented. The backend reset removed provider request/marketplace runtime code and the inspection workflow controllers/services; surviving inspection JPA records and repositories plus V24/V25 migration schema are persistence/schema only. Asset/catalog/scheduling runtime and authentication remain, but the full MF1–MF4 workflow behavior is out of reset scope and not implemented. V24 aligns identity vocabulary, V25 adds the target schema, and V26 completes the runtime cutover to the exact 41-table target inventory (verified by `./mvnw clean verify`, 88 tests, exit 0, on 8 October 2026). Read the runtime-status table and verify against the current source before treating target modules or behaviors as shipped.

The target backend architecture is a Java 21 Spring Boot modular monolith. Spring Modulith verifies the boundaries between direct feature packages so each team-owned capability stays focused.

## Capability modules

By default, each direct package under `com.smartdroneinspection` is one Spring
Modulith application module. A module represents a business capability, not a
workflow number or a group of tables.

```text
com.smartdroneinspection/
|-- users/                 # Implemented: identity, organizations, users, roles, sessions
|-- subscriptions/         # Enterprise subscription plan/period/status/entitlement
|-- workforce/             # Inspector/engineer credentials, qualifications, compliance documents
|-- assets/                # Asset catalog, asset documents, drones, pair assignments, checklist templates
|-- inspections/           # Inspection setup snapshots, readiness/session records, evidence, findings, reports
|-- maintenance/           # Work orders, teams, tasks, cost lines, change orders, work logs, reports, acceptance
|-- notifications/         # In-app/email notification records and event-facing contracts
|-- dashboard/             # Read-only aggregation; no ownership of business tables
|-- shared/                # Cross-cutting contracts: ApiResponse, ProblemDetail, security context, audit base
`-- infrastructure/        # Outbound adapters for feature-owned ports
```

| Module | Capability | Runtime status |
| --- | --- | --- |
| `users` | Identity, authentication, organization, audit, and user administration | Auth/organization runtime and persistence remain; target organization-registration/auth contracts are still being reset. |
| `subscriptions` | Enterprise subscription management | Package root only; the `subscriptions` table is schema, not subscription runtime. |
| `workforce` | Credentials, qualifications, and compliance documents | Package root only; the `workforce_credentials` table is schema, not workforce runtime. |
| `assets` | Asset catalog, asset documents, categories/checklists, and schedules | Asset/catalog/scheduling entities, repositories, controllers, and services remain; the reset branch is reconciling authorization and does not complete all MF1 target behavior. |
| `inspections` | Inspection setup, readiness, field records, evidence, findings, and reports | Workflow controllers/services and inspection workflow tests were removed in the reset; residual entities/repositories and V24/V25 schema are storage only, not an inspection workflow runtime. |
| `maintenance` | Target work orders, teams, costs, work logs, reports, and acceptance | Legacy maintenance persistence artifacts remain; the MF4 target workflow implementation is not present. |
| `notifications` | Notification records and delivery | Existing notification persistence may remain; target delivery behavior is not established by the reset. |
| `dashboard` | Read-only composition of capability data | Package metadata only; no runtime slice. |
| `infrastructure` | Outbound adapters for feature-owned ports | Legacy MinIO/AI adapters may remain; they do not make removed workflow use cases available. |

`dashboard` currently contains only package metadata. Before the reset, the `inspections` runtime slice included assigned execution/checklists, evidence, optional AI-assisted findings, versioned reports, release, and organization decision; its workflow controllers and services have since been removed. The older inspection workflow details in [the runtime flow guide](../backend/flows/inspections-and-reports/) are historical, not currently callable endpoints. Current MF1–MF4 runtime behavior remains to be implemented in separate workflow slices. Each feature owns its domain models; do not create a global `com.smartdroneinspection.domain` entity package.

## Module visibility and responsibilities

The module root is the default public Java API. Nested packages are internal
unless explicitly exposed with `@NamedInterface`.

| Package | Visibility and responsibility |
| --- | --- |
| `<module>/api` | Internal HTTP controllers and transport DTOs. |
| `<module>/domain` | Internal JPA entities, value objects, and rules owned by the module. |
| `<module>/domain/enums` | Internal domain enums owned by the module. |
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
users -------------------------------> shared::api, shared::auth, shared::config, shared::exception
subscriptions -----------------------> users, shared
workforce ---------------------------> users, shared
assets ------------------------------> shared, users
inspections -------------------------> assets, shared::api, shared
maintenance -------------------------> inspections, shared
notifications -----------------------> feature::events
dashboard ---------------------------> feature root read APIs
infrastructure ----------------------> feature::spi, shared
```

Business modules never import `infrastructure`; adapters implement ports owned by
the feature. When periodic request generation is implemented, `assets` publishes
`assets::events InspectionScheduleDue` and the consumer in the owning module listens and
creates the request. Add that event and facade with the periodic-request use case,
not as speculative plumbing.

## Persistence and integrations

PostgreSQL is the target persistence source of truth. Flyway owns schema migrations. On the reset branch V26 has completed the runtime schema cutover to the exact target inventory; do not infer that every table has a current entity, repository, API or workflow consumer. The target architecture assigns tables to owning features, except framework infrastructure such as Spring Modulith `event_publication`; the live ownership map must be reconciled against current entities and migrations before claiming full parity. Cross-feature references should use scalar IDs at the persistence boundary instead of coupling modules through each other's entities. The `infrastructure/` area may contain outbound adapters for feature-owned ports. Reports, findings, and AI candidates are target responsibilities of `inspections`; maintenance work orders are target responsibilities of `maintenance`; these workflow features are not implemented by schema presence.

Inspection evidence is uploaded through the web or mobile application. The optional YOLO adapter is environment-configured and disabled by default. The current architecture has no dependency on a separate drone-operation platform.

## Error handling and verification

Successful JSON bodies use the shared `ApiResponse<T>` contract: `{ success, message, data }`. Controllers keep the HTTP status authoritative; `204 No Content` and binary evidence streams are not wrapped. Browser and mobile clients unwrap the envelope in their shared HTTP clients.

Changing an already-published response body is breaking: deploy the backend and
first-party clients as a compatible release. If an external `/api/v1` consumer
exists, keep its old contract during migration or introduce a new API version
instead of silently switching its response shape.

Expected business failures use `Result<T>` where appropriate. Errors use RFC 9457 `ProblemDetail` with a stable application `code` and `traceId`; MVC and Spring Security failures share this error shape. Unexpected failures are sanitized by the global exception handler.

Backend changes should pass `./mvnw verify`, including formatting, tests, JaCoCo coverage, and Modulith boundary verification.
