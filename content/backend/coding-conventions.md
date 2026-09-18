---
title: "Backend Java Conventions"
weight: 20
aliases:
  - /coding-conventions/backend-java/
---

# Backend Java Conventions

The backend is a Java 21, Spring Boot modular monolith. Spring Modulith verifies module boundaries. Use feature ownership and simple Spring patterns; do not reproduce enterprise layers that the project does not need.

## Feature structure

A business capability is a direct package under `com.smartdroneinspection`, for example `users`, `assets`, or `reports`.

```text
<feature>/
|-- api/
|   `-- dto/
|       |-- request/
|       `-- response/
|-- domain/
|-- repository/
|-- service/
`-- security/          # only when the feature owns security behavior
```

- **BE-01 MUST** keep entities and business rules in the feature that owns them. Do not create a global entity package.
- **BE-02 SHOULD** create only the packages a feature needs.
- **BE-03 MAY** use JPA annotations on feature-owned domain entities. Do not duplicate every entity into a persistence model solely to claim framework independence.
- **BE-04 MUST** access another module through its public API or published event, not its internal repository or entity implementation.

## API and DTOs

- **BE-05 MUST** keep controllers thin: parse transport input, invoke one application use case, and map the result to HTTP.
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
- **BE-16 SHOULD** use the shared `Result<T>` for expected business outcomes already modeled by the application. Unexpected exceptions are mapped to RFC 7807 `ProblemDetail` centrally.

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
