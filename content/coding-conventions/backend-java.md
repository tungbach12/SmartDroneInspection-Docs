---
title: "Backend Java Conventions"
weight: 1
---

# Backend Java Coding Conventions

## Architecture and structure

- The backend is a Spring Boot modular monolith verified by Spring Modulith.
- Keep each business capability in a direct module package such as `users`, `assets`, or `reports`.
- A feature module may contain `api`, `domain`, `service`, and `repository` packages.
- Keep domain entities inside the owning feature; do not create a global `com.smartdroneinspection.domain` entity package.

## API and DTOs

- Controllers stay thin and delegate business rules to application services.
- Use records for request and response DTOs.
- Keep feature DTOs under `<module>/api/dto/request` and `<module>/api/dto/response`.
- Validate request records with Jakarta Bean Validation.
- Use `ResponseEntity` only when status or headers need to be explicit.

Example:

```text
users/api/
└── dto/
    ├── request/
    │   └── LoginRequest.java
    └── response/
        └── AuthFlowResponse.java
```

## Services and persistence

- Use constructor injection.
- Put transaction boundaries on application services.
- Keep repositories focused on persistence queries; enforce organization and assignment scope in the service/repository query.
- Expected business failures use the shared `Result<T>` type where appropriate.
- Unexpected failures are converted to RFC 7807 `ProblemDetail` by the global exception handler.

## Security

- Authentication implementation belongs to `users/security`.
- Cross-cutting role constants belong to `shared/auth`.
- HTTP filter-chain configuration belongs to `shared/config`.
- Never log passwords, tokens, or other credential material.

## Verification

Run `./mvnw verify` before opening a PR. This runs formatting, tests, JaCoCo coverage, and Modulith boundary checks.
