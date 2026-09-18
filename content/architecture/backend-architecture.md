---
title: "Backend Architecture"
weight: 10
---

# Backend Architecture

The backend is a Java 21 Spring Boot modular monolith. Spring Modulith verifies the boundaries between direct feature packages so each team-owned capability stays focused.

## Package layout

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

Each feature owns its domain models. For example, authentication entities and rules live in `com.smartdroneinspection.users.domain`. Do not create a global `com.smartdroneinspection.domain` entity package.

## Feature module responsibilities

- `api/` contains thin controllers and feature-owned request/response records.
- `api/dto/request/` and `api/dto/response/` contain Java record DTOs for the public contract.
- `domain/` contains aggregates, value objects, enums, and business rules.
- `service/` contains application use cases and transaction boundaries.
- `repository/` contains persistence ports and Spring Data adapters.
- `security/` contains module-specific authorization helpers where needed.

Shared code is limited to cross-cutting concerns such as error handling, security configuration, result types, and pagination. It must not become a shared home for feature entities or use cases.

## Persistence and integrations

PostgreSQL is the source of truth. Flyway owns schema migrations, and MinIO stores inspection evidence and images. The `infrastructure/` area contains MinIO, AI, and notification adapters. Business modules depend on application ports rather than vendor SDK details.

Inspection evidence is uploaded through the web or mobile application. The current architecture has no dependency on a separate drone-operation platform.

## Error handling and verification

Expected business failures use `Result<T>` where appropriate. Unexpected failures are converted to RFC 7807 `ProblemDetail` by the global exception handler.

Backend changes should pass `./mvnw verify`, including formatting, tests, JaCoCo coverage, and Modulith boundary verification.
