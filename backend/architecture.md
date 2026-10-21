---
title: "Backend Architecture"
weight: 10
aliases:
  - /architecture/backend-architecture/
---

# Backend Architecture

> **Current worktree status — 21 October 2026:** This page combines target architecture guidance with runtime inventory. The `inspections` module implements MF2 assignment response, preparation/compliance, readiness approval/return, session start/postpone/abort and normal completion, plus MF3 evidence, quality decisions, findings and reports. Additional-session requests return to `PREPARING`, invalidate the prior readiness, supersede the old approved preparation and create a next-version draft. Session start is bound to the latest READY preparation and its latest APPROVED readiness decision. Generic MF2-08 source-change invalidation remains partial; the additional-session path is covered. MF2-12 has focused implementation tests but not a Report 5 case. MF1 and MF4 remain incomplete workflow implementations. Verify runtime status against current source before treating target behaviors as shipped.

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
|-- inspections/           # Implemented (MF3): evidence, quality decisions, findings, versioned reports
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
| `inspections` | Assignment response, mission preparation/compliance, readiness, field sessions, evidence, findings, and versioned reports | MF2-01/02, MF2-03/06, MF2-07, MF2-09/11 and MF2-12 normal completion are implemented. Additional-session return invalidates prior readiness and requires a new version/window/readiness approval; Start is bound to that current approval. Generic MF2-08 source-change invalidation is partial. MF2 additional-session/session-end code has focused implementation tests, not a full Report 5 scenario. MF3-01 through MF3-13 coding is present, including the MF3-12/13 corrective-outcome and handoff paths; that change executed green on 2026-10-16 (81 targeted WF3 tests and the 650-test full `verify` gate), and runtime review does not validate reviewer credentials. V37 consolidates detector suggestions and Inspector findings in `findings`; rejected AI suggestions are removed rather than retained as finding-level audit records, while explicit finding removal keeps its tombstone. In this task backend `./mvnw verify` passed 684 tests before the final AI-suggestion rejection-path correction; final `./mvnw -DskipTests package` passed without tests after that correction. Frontend production build passed. Mobile code generation passed, but no Android SDK or configured web target was available for an artifact build. Inspection creation remains in MF1; this module receives the assigned inspection. |
| `maintenance` | Target work orders, teams, costs, work logs, reports, and acceptance | Legacy maintenance persistence artifacts remain; the MF4 target workflow implementation is not present. |
| `notifications` | Notification records and delivery | Existing notification persistence may remain; target delivery behavior is not established by the reset. |
| `dashboard` | Read-only composition of capability data | Package metadata only; no runtime slice. |
| `infrastructure` | Outbound adapters for feature-owned ports | MinIO storage, the advisory image-inference adapters (the self-hosted YOLO detector as the default and an optional OpenAI-compatible vision endpoint behind it), and the independently configurable LLM report-draft adapter are available; MF3 retains manual finding and report-authoring paths. |

The `inspections` runtime supports MF2 assignment response, preparation/compliance, readiness decisions and field-session start/postpone/abort, as well as MF3 scoped evidence upload with server-side checksum/idempotency, the Inspector's substantive evidence-quality decision, advisory detections stored as findings alongside the Inspector's own observations, manual finding entry on AI failure, and versioned report authoring/review/publication. See [the inspection runtime flow guide](../backend/flows/inspections-and-reports/) for implementation boundaries and endpoint details. Each feature owns its domain models; do not create a global `com.smartdroneinspection.domain` entity package.

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

PostgreSQL is the target persistence source of truth. Flyway owns schema migrations. On the reset branch V26 has completed the runtime schema cutover to the exact target inventory; do not infer that every table has a current entity, repository, API or workflow consumer. The target architecture assigns tables to owning features, except framework infrastructure such as Spring Modulith `event_publication`; the live ownership map must be reconciled against current entities and migrations before claiming full parity. Cross-feature references should use scalar IDs at the persistence boundary instead of coupling modules through each other's entities. The `infrastructure/` area may contain outbound adapters for feature-owned ports. Reports, findings, and AI candidates are responsibilities of `inspections`, which implements the MF3 slice of them; maintenance work orders are target responsibilities of `maintenance` and are not implemented by schema presence.

Inspection evidence is uploaded through the web or mobile application. Image inference is optional; the self-hosted YOLO detector is the default advisory provider and is served by the `ai-inference` service in this repository, while the OpenAI-compatible multimodal vision adapter is an option that answers only for images the detector could not process. With no provider configured the analysis endpoints report that automated analysis is not configured, and report drafting remains independently configurable with manual findings and report authoring always available. The current architecture has no dependency on a separate drone-operation platform.

## Error handling and verification

Successful JSON bodies use the shared `ApiResponse<T>` contract: `{ success, message, data }`. Controllers keep the HTTP status authoritative; `204 No Content` and binary evidence streams are not wrapped. Browser and mobile clients unwrap the envelope in their shared HTTP clients.

Changing an already-published response body is breaking: deploy the backend and
first-party clients as a compatible release. If an external `/api/v1` consumer
exists, keep its old contract during migration or introduce a new API version
instead of silently switching its response shape.

Expected business failures use `Result<T>` where appropriate. Errors use RFC 9457 `ProblemDetail` with a stable application `code` and `traceId`; MVC and Spring Security failures share this error shape. Unexpected failures are sanitized by the global exception handler.

Backend changes should pass `./mvnw verify`, including formatting, tests, JaCoCo coverage, and Modulith boundary verification.
