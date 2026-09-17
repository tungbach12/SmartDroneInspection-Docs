---
title: "Architecture"
weight: 20
---

# Architecture

## Backend module boundaries

The backend is a Spring Modulith modular monolith. Each direct package under `com.smartdroneinspection` is a business or technical module. A feature module keeps its implementation details inside the module and exposes only its intended application API.

```text
com.smartdroneinspection
├── users/
│   ├── api/
│   │   └── dto/
│   │       ├── request/
│   │       └── response/
│   ├── domain/
│   ├── repository/
│   ├── security/
│   └── service/
├── assets/
├── inspections/
├── missions/
├── reports/
├── defects/
├── tickets/
├── planning/
├── dashboard/
├── ai/
├── shared/
└── infrastructure/
```

Feature modules such as `users`, `assets`, and `inspections` own their domain models. For example, authentication entities belong in `com.smartdroneinspection.users.domain`.

Do not create a global `com.smartdroneinspection.domain` entity module. A global domain package couples unrelated features and weakens Modulith boundary checks.

## What belongs in a feature module

- `api/` — controllers and public request/response records.
- `api/dto/request/` and `api/dto/response/` — feature-owned request and response records.
- `domain/` — aggregates, value objects, enums, and domain rules.
- `service/` — application use cases and transaction boundaries.
- `repository/` — persistence ports and Spring Data adapters.
- `security/` — module-specific authorization rules where needed.

Shared code is limited to genuinely cross-cutting concerns such as error handling, security configuration, result types, and pagination. It must not become a dumping ground for feature entities or use cases.

## Client structure

- The React app is feature-first under `frontend/src/features/`; TanStack Query owns server state and Zustand owns small client-only state.
- The Flutter app is feature-first under `mobile/lib/features/`, with `domain/`, `data/`, and `presentation/` layers per feature.
- Both clients call the versioned `/api/v1` contract. Browser and mobile token delivery differ as documented in [Authentication](authentication/).

## Integration boundary

SmartDroneInspection is a consumer of SmartDroneHub. The `infrastructure/` area contains outbound REST/WebSocket and object-storage adapters. Business modules depend on application ports, not on SmartDroneHub SDK details.

## Verification

Architecture boundaries are checked by Spring Modulith tests. Backend changes should pass `./mvnw verify`, including formatting, tests, JaCoCo coverage, and Modulith verification.

## Reference patterns

This layout follows Spring Modulith's feature-module model: direct subpackages under the application package are modules, while nested packages are implementation details. Spring Petclinic uses the same feature-oriented placement for domain types such as `owner.Owner`.

- [Spring Modulith fundamentals](https://docs.spring.io/spring-modulith/reference/fundamentals.html)
- [Spring Petclinic owner module](https://github.com/spring-projects/spring-petclinic/tree/main/src/main/java/org/springframework/samples/petclinic/owner)
## Reference patterns
This layout follows Spring Modulith's feature-module model: direct subpackages under the application package are modules, while nested packages are implementation details. Spring Petclinic uses the same feature-oriented placement for domain types such as `owner.Owner`.
- [Spring Modulith fundamentals](https://docs.spring.io/spring-modulith/reference/fundamentals.html)
- [Spring Petclinic owner module](https://github.com/spring-projects/spring-petclinic/tree/main/src/main/java/org/springframework/samples/petclinic/owner)
