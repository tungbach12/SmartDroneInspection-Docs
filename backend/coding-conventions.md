---
title: "Backend Java Conventions"
weight: 20
aliases:
  - /coding-conventions/backend-java/
---

# Backend Java Conventions

The backend is a Java 21, Spring Boot modular monolith. Spring Modulith verifies module boundaries. Use feature ownership and simple Spring patterns; do not reproduce enterprise layers that the project does not need.

## Feature structure

A business capability is a direct package under `com.smartdroneinspection`, for example `users`, `assets`, or `inspectionrequests`. Name modules with business language; never use `wf1` or `wf2` as a package name.

```text
<feature>/
|-- api/
|   `-- dto/
|       |-- request/
|       `-- response/
|-- domain/
|   `-- enums/          # domain enums; keep transport enums with API DTOs
|-- repository/
|-- service/
`-- security/          # only when the feature owns security behavior
```

- **BE-01 MUST** keep entities and business rules in the feature that owns them. Do not create a global entity package.
- **BE-02 SHOULD** create only the packages a feature needs.
- **BE-03 MAY** use JPA annotations on feature-owned domain entities. Do not duplicate every entity into a persistence model solely to claim framework independence.
- **BE-04 MUST** access another module through its public API or published event, not its internal repository or entity implementation.
- **BE-DB-01 MUST** place a table-backed entity in `<feature>/domain` and its Spring Data repository in `<feature>/repository`. The owning feature is the capability that owns the business lifecycle, not the table name alone.
- **BE-DB-05 MUST** place domain enums in `<feature>/domain/enums`. Keep API-only enums, such as authentication flow steps, in the owning `api/dto` package. Do not use a Java package named `enum`; `enum` is a reserved keyword, so the valid package name is `enums`.
- **BE-DB-02 MUST** keep `inspections` and `inspectionrequests` separate: requests, quotations, service orders, and Inspector assignments belong to `inspectionrequests`; inspection execution, evidence, findings, reports, versions, and peer reviews belong to `inspections`.
- **BE-DB-03 SHOULD** model cross-feature foreign keys as scalar `UUID` fields. Do not create JPA relationships to another Modulith module's entity; use a module facade or event when behavior needs the other capability.
- **BE-DB-04 MUST NOT** create a business entity for framework-owned `event_publication`, and must not add empty domain/repository packages to scaffold-only modules.

## Spring Modulith boundaries

- **BE-MOD-01 MUST** treat every direct package under `com.smartdroneinspection` as a capability module. A workflow or table group is not a reason to create a separate module.
- **BE-MOD-02 MUST** treat the module root as the default Java API. Nested `api`, `domain`, `repository`, and `service` packages are internal unless explicitly exposed with `@NamedInterface`.
- **BE-MOD-03 MUST NOT** import another module's controllers, HTTP DTOs, entities, repositories, or services. Use a facade in the module root or a named `events`/`spi` interface.
- **BE-MOD-04 MUST** keep HTTP DTOs as transport contracts; they are never cross-module contracts.
- **BE-MOD-05 SHOULD** use events for module handoff and side effects, and synchronous facades for immediate results or validation. Do not turn every call into an event.
- **BE-MOD-06 MUST** define ports in the feature that owns the use case; `infrastructure` implements those ports and is never imported by business modules.
- **BE-MOD-07 MUST** keep `ApplicationModules.verify()` green. Add `@ApplicationModuleTest` when a module has runtime components worth bootstrapping.
- **BE-MOD-08 MUST** allow approved capability roots to contain `package-info.java` before runtime code exists. Do not add empty nested packages or speculative business types; create nested packages with the first vertical slice that owns real code.

## API and DTOs

- **BE-05 MUST** keep controllers thin: parse transport input, invoke one application use case, and map successful JSON results to `shared.api.ApiResponse<T>` while preserving the endpoint's HTTP status. Keep `204 No Content` and binary streaming responses unwrapped.
- **BE-06 MUST** use Java records for request and response DTOs unless framework behavior requires a class.
- **BE-07 MUST** place request DTOs in `<feature>/api/dto/request` and response DTOs in `<feature>/api/dto/response`.
- **BE-08 MUST** validate requests with Jakarta Bean Validation and `@Valid`; service methods still enforce business invariants.
- **BE-09 SHOULD** use `ResponseEntity` only when status, headers, or an empty body must be explicit.
- **BE-10 MUST NOT** expose JPA entities directly from controllers.

## Services, domain, and persistence

- **BE-11 MUST** use constructor injection. Field injection is not allowed.
- **BE-12 SHOULD** put transaction boundaries on application-service methods that coordinate a use case.
- **BE-13 SHOULD** place state-transition invariants on the entity/value object when they belong to that model; orchestration remains in the service.
- **BE-14 MUST** scope repository queries by organization, owner, or assignment when access depends on that scope. Fetching broadly and filtering in memory is not authorization.
- **BE-15 MUST NOT** create `XxxService` plus `XxxServiceImpl`, or a repository wrapper around Spring Data, unless there is a real alternative implementation or boundary.
- **BE-16 SHOULD** use the shared `Result<T>` for expected business outcomes already modeled by the application. Errors are mapped to RFC 9457 `ProblemDetail` with a stable code and trace identifier; unexpected exceptions are handled centrally.

## Security

- **BE-17 MUST** keep authentication behavior in `users/security`; cross-cutting filter-chain configuration and role constants remain under `shared`.
- **BE-18 MUST** deny access by default and enforce both role and resource scope in the service or scoped repository query.
- **BE-19 MUST NOT** trust a client-provided organization ID, user ID, or role without matching it to the authenticated principal and allowed scope.
- **BE-20 MUST NOT** log credential or token material.

## Naming and style

- Classes and records: `PascalCase`; methods, fields, and packages: `camelCase` / lowercase packages.
- API contracts: `XxxRequest`, `XxxResponse`; controllers: `XxxController`; application services: `XxxService`; repositories: `XxxRepository`.
- Prefer domain verbs such as `assignInspector` or `releaseReport` over generic methods such as `process`.
- Use Google Java Format through Spotless; do not hand-format around it.

## Testing and verification

- Unit-test business rules and authorization decisions without Spring when practical.
- Use integration tests for persistence queries, security filters, transactions, and API contracts.
- A defect fix SHOULD include a regression test that fails before the fix.
- Run `.\mvnw.cmd verify` on Windows or `./mvnw verify` on Unix before handoff.
