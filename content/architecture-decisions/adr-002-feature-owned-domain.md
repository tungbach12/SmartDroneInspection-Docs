---
title: "ADR-002: Feature-owned domain packages"
weight: 2
---

# ADR-002: Feature-owned domain packages

- **Status:** Accepted
- **Date:** 2026-09-17

## Context

The backend is a Spring Modulith modular monolith. A single global domain package makes unrelated entities look like one shared module and lets feature code depend on persistence details from other features. The authentication work also needs a clear home for users, roles, sessions, and credentials.

## Decision

Keep domain code inside the feature that owns the business capability. Authentication entities and rules live under `com.smartdroneinspection.users.domain`; asset entities live under the assets module, and so on. Each module may contain `api`, `domain`, `service`, and `repository` packages as needed.

Do not add a top-level `com.smartdroneinspection.domain` package for shared entities. Shared packages are reserved for genuinely cross-cutting primitives and configuration.

## Consequences

- Module ownership is visible from the package name.
- Spring Modulith can enforce boundaries at direct feature-package level.
- Feature changes are easier to review and test in isolation.
- Cross-feature queries require an explicit application API or integration event instead of reaching into another module's entities.
- Moving existing entities may require import updates, but no database table rename is needed.
