---
title: "Backend C# Conventions"
weight: 1
---

# Backend C# Coding Conventions

## 1. Architecture & Structure
* All endpoints use **FastEndpoints** under `Features/<Module>/<Action>/`.
* One endpoint per file with the naming format `<Action><Entity>Endpoint.cs` (e.g. `CreateAssetEndpoint.cs`).
* Request and Response DTOs are declared as `sealed record` within the action folder or `Dtos.cs`.

## 2. Naming Conventions
* **Classes & Records**: PascalCase (`CreateAssetRequest`, `AssetByIdSpec`).
* **Async Methods**: Must end with `Async` (e.g. `ExecuteAsync`, `AddAsync`, `SaveChangesAsync`).
* **Strongly-Typed IDs**: Use Vogen structs (`AssetId.From(...)`).
* **Enums**: Use **Ardalis.SmartEnum** rather than primitive enums where business behavior exists.

## 3. Data Access & Querying
* Always use `Ardalis.Specification` for queries with filters, pagination, and sorting.
* Soft-deleted records are filtered automatically via EF Core global query filters (`ISoftDelete`).
* Audit fields (`CreatedAt`, `CreatedBy`, `UpdatedAt`, `UpdatedBy`) are populated automatically via DbContext interceptors.

## 4. Error Handling & Validation
* Validate inputs using **FluentValidation** (`Validator<TRequest>`).
* Expected domain failures return `Results<..., ValidationProblem, NotFound, ProblemHttpResult>`.
* Unexpected exceptions are handled globally via `AddProblemDetails`.
