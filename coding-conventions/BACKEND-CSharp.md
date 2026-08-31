# Coding Conventions — Backend (C# / ASP.NET Core)

> Rules are law: enforced by `.editorconfig`, `dotnet format`, and CI. Reviewers check logic, not style.

## 1. Naming

| Element | Rule | Example |
|---------|------|---------|
| Class / record / struct | PascalCase | `InspectionPlan` |
| Interface | I + PascalCase | `IObjectStorage` |
| Method | PascalCase, async ends with `Async` | `ApproveRequestAsync` |
| Property | PascalCase | `InspectionId` |
| Private field | `_camelCase` | `_smartDroneHubClient` |
| Local variable / parameter | camelCase | `inspectionId` |
| Constant (incl. private) | PascalCase | `MaxRetryCount` |
| Enum values | PascalCase | `InspectionStatus.Completed` |
| DTO (API contract) | `XxxRequest` / `XxxResponse` | `CreateAssetRequest` |
| DTO (internal map) | `XxxDto` | `MissionTelemetryDto` |

- Never `this.`; never public fields.
- Every async method ends with `Async`. No exceptions.

## 2. File & namespace organization

- **File-scoped namespaces** only:

```csharp
namespace SmartDroneInspection.Application.Assets.Commands;

public record CreateAssetCommand(...) : IRequest<AssetDto>;
```

- Folder path == namespace path. If the folder is `Assets/Commands`, the namespace is `SmartDroneInspection.Application.Assets.Commands`.

## 3. MediatR feature layout (Co-located Single-file Feature Slice)

For each operation, co-locate the **Command/Query record**, **Validator**, and **Handler** in a single file named after the command/query:

```
Application/Assets/Commands/
└─ CreateAssetCommand.cs            # Command record + Validator + Handler
Application/Assets/Queries/
├─ GetAssetsQuery.cs                # Query record + Handler
└─ GetAssetByIdQuery.cs             # Query record + Handler
Application/Assets/Dtos/
└─ AssetDtos.cs                     # Request/Response/Dto records for this module
```

- Commands: verb + noun → `CreateAssetCommand`, `AssignInspectorCommand`.
- Queries: noun / get + noun → `GetAssetByIdQuery`, `GetAssetsQuery`.
- Handler constructor injects `IApplicationDbContext` and necessary service interfaces directly — no generic repositories.

```csharp
public record CreateAssetCommand(...) : IRequest<AssetDto>;

public class CreateAssetCommandValidator : AbstractValidator<CreateAssetCommand>
{
    public CreateAssetCommandValidator()
    {
        RuleFor(x => x.Name).NotEmpty().MaximumLength(250);
        RuleFor(x => x.Code).NotEmpty().MaximumLength(100);
    }
}

public class CreateAssetCommandHandler(IApplicationDbContext db)
    : IRequestHandler<CreateAssetCommand, AssetDto>
{
    public async Task<AssetDto> Handle(CreateAssetCommand request, CancellationToken ct)
    {
        var normalizedCode = request.Code.Trim().ToUpperInvariant();
        var codeExists = await db.Assets
            .AnyAsync(a => a.OrganizationId == request.OrganizationId
                && a.NormalizedCode == normalizedCode, ct);
        if (codeExists)
        {
            throw new InvalidOperationException($"Asset code '{request.Code}' already exists");
        }

        var asset = new Asset { ... };
        db.Assets.Add(asset);
        await db.SaveChangesAsync(ct);

        return new AssetDto(...);
    }
}
```

## 4. Async & CancellationToken Propagation (MANDATORY)

Cancellation tokens ensure server resources, connection pools, and downstream services (AI, MinIO, SmartDroneHub) are immediately released when a client cancels or disconnects:

- **Every async controller action** must accept `CancellationToken ct` (injected automatically by ASP.NET Core from `HttpContext.RequestAborted`).
- **Every MediatR Request** passes `ct` to `mediator.Send(command, ct)`.
- **Every MediatR Handler and Service method** must receive `CancellationToken ct` and propagate it to all async calls:
  - EF Core calls: `CountAsync(ct)`, `ToListAsync(ct)`, `FirstOrDefaultAsync(ct)`, `SaveChangesAsync(ct)`.
  - HTTP clients & storage: `UploadAsync(..., ct)`, `DownloadAsync(..., ct)`.
- **Exception**: Use `CancellationToken.None` *only* for background or security-critical audit logging that must complete even if the user aborts the HTTP request.

## 5. API & Controllers

- Controllers are **thin**: HTTP mapping, rate limiting, and auth attributes only. Business logic lives in handlers.
- REST: plural nouns, no verbs in URLs.

| Operation | Route |
|-----------|-------|
| List | `GET /api/v1/assets` |
| Get one | `GET /api/v1/assets/{id}` |
| Create | `POST /api/v1/assets` → `201 Created` + `Location` |
| Update | `PUT /api/v1/assets/{id}` |
| Partial status | `PATCH /api/v1/assets/{id}/status` |
| Delete | `DELETE /api/v1/assets/{id}` → `204 NoContent` |

- Version in URL path (`/api/v1/...`) via `Asp.Versioning`.
- Controllers route via MediatR directly:

```csharp
[HttpPost]
[Authorize(Roles = $"{Roles.Administrator},{Roles.InspectionManager}")]
public async Task<ActionResult<Guid>> CreateAsync(CreateAssetRequest request, CancellationToken ct)
{
    var command = new CreateAssetCommand(...);
    var id = await mediator.Send(command, ct);
    return CreatedAtAction(nameof(GetByIdAsync), new { id, version = "1" }, id);
}
```

## 6. Error Handling — GlobalExceptionHandler & ProblemDetails (RFC 7807)

- **Handlers throw semantic exceptions**; the `GlobalExceptionHandler` (`IExceptionHandler`) automatically converts them to RFC 7807 ProblemDetails:
  - `ValidationException` (FluentValidation) → `400 Bad Request` with field error list.
  - `UnauthorizedAccessException` → `403 Forbidden` / `401 Unauthorized`.
  - `KeyNotFoundException` → `404 Not Found`.
  - `InvalidOperationException` → `409 Conflict` (e.g. duplicate code, invalid state transition).
  - Unhandled exceptions → `500 Internal Server Error` (logged with full stack trace, client gets generic message).
- Never catch-and-swallow. Never return raw exception stack traces to clients.

## 7. EF Core

- One `IEntityTypeConfiguration<T>` per entity, inside `Persistence/Configurations/`, grouped by module.
- Registration is central (one line, owned by Leader):

```csharp
modelBuilder.ApplyConfigurationsFromAssembly(typeof(ApplicationDbContext).Assembly);
```

- Migration naming: `AddInspectionTable`, `AddCompletedAtToInspection`, `AddUniqueIndexOnDefectCode`.
- **Only the Leader runs `dotnet ef migrations add`** — others write configurations; Leader generates migrations from them.
- Seed reference data (enums, categories) via `HasData()` in configuration; dev sample data via `Seed/` seeder, never `HasData`.

## 8. Testing

- Unit test project mirrors module folders: `UnitTests/Assets/CreateAssetCommandHandlerTests.cs`.
- Integration tests hit real PostgreSQL (Testcontainers), one `ICollectionFixture`, Respawn between tests.
- Test naming: `MethodName_Scenario_ExpectedResult` → `Handle_UnknownId_ReturnsFailure`.

## 9. Formatting (automated — do not hand-fix)

- `.editorconfig` + `dotnet format` on save / in CI. All files end with newline, UTF-8, 4-space indent C#.
- `var` when the type is apparent; explicit elsewhere.
- Braces always (no single-line `if` without braces).
