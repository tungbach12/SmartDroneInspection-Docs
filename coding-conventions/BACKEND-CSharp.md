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

- **One type per file**, filename == type name.
- **File-scoped namespaces** only:

```csharp
namespace SmartDroneInspection.Application.Assets.Commands;

public record CreateAssetCommand(...) : IRequest<Result<Guid>>;
```

- Folder path == namespace path. If the folder is `Assets/Commands`, the namespace is `...Application.Assets.Commands`.

## 3. MediatR feature layout

One feature = one folder, three files:

```
Application/Assets/Commands/
├─ CreateAssetCommand.cs            # record + parameters
├─ CreateAssetCommandHandler.cs     # handler
└─ CreateAssetCommandValidator.cs   # FluentValidation rules
```

- Commands: verb + noun → `CreateInspectionCommand`, `AssignInspectorCommand`.
- Queries: noun → `GetAssetByIdQuery`, `GetDefectsQuery`.
- Query handlers return `XxxResponse`; command handlers return `Result` or `Result<Guid>`.
- Handler constructor injects `ApplicationDbContext` and interfaces directly — no repositories.

```csharp
public class CreateAssetCommandHandler(ApplicationDbContext db)
    : IRequestHandler<CreateAssetCommand, Result<Guid>>
{
    public async Task<Result<Guid>> Handle(CreateAssetCommand request, CancellationToken ct)
    {
        var asset = new Asset { Name = request.Name, ... };
        db.Assets.Add(asset);
        await db.SaveChangesAsync(ct);
        return Result.Success(asset.Id);
    }
}
```

## 4. API & Controllers

- Controllers are **thin**: HTTP mapping + auth attributes only. Business logic lives in handlers.
- REST: plural nouns, no verbs in URLs.

| Operation | Route |
|-----------|-------|
| List | `GET /api/v1/assets` |
| Get one | `GET /api/v1/assets/{id}` |
| Create | `POST /api/v1/assets` → `201 Created` + `Location` |
| Update | `PUT /api/v1/assets/{id}` |
| Partial status | `PATCH /api/v1/assets/{id}/status` |
| Delete | `DELETE /api/v1/assets/{id}` → `204 NoContent` |

- Version in URL path (`/api/v1/...`).
- Status codes: 200 success · 201 create · 204 delete · 400 validation · 401/403 auth · 404 not found · 409 conflict.
- Controllers route via MediatR only:

```csharp
[HttpPost]
[Authorize(Roles = Roles.InspectionManager)]
public async Task<IActionResult> Create(CreateAssetRequest request, CancellationToken ct)
{
    var result = await _mediator.Send(request.ToCommand(), ct);
    return result.IsSuccess
        ? CreatedAtAction(nameof(GetById), new { id = result.Value }, result.Value)
        : result.ToProblem();
}
```

## 5. Error handling — Result vs Exception

- **Expected business failures** (not found, validation, conflict, external service down) → `Result.Failure(...)`. Handlers never throw for these.
- **Unexpected errors** (bugs, `DbUpdateException`, nulls) → let them throw; the global exception handler converts to ProblemDetails.
- Never catch-and-swallow. Never throw for control flow.

```csharp
var asset = await db.Assets.FindAsync(id, ct);
if (asset is null) return Result.Failure<Guid>($"Asset {id} not found");
```

## 6. EF Core

- One `IEntityTypeConfiguration<T>` per entity, inside `Persistence/Configurations/`, grouped by module.
- Registration is central (one line, owned by Leader):

```csharp
modelBuilder.ApplyConfigurationsFromAssembly(typeof(ApplicationDbContext).Assembly);
```

- Migration naming: `AddInspectionTable`, `AddCompletedAtToInspection`, `AddUniqueIndexOnDefectCode`.
- **Only the Leader runs `dotnet ef migrations add`** — others write configurations; Leader generates migrations from them.
- Seed reference data (enums, categories) via `HasData()` in configuration; dev sample data via `Seed/` seeder, never `HasData`.

## 7. Testing

- Unit test project mirrors module folders: `UnitTests/Assets/CreateAssetCommandHandlerTests.cs`.
- Integration tests hit real PostgreSQL (Testcontainers), one `ICollectionFixture`, Respawn between tests.
- Test naming: `MethodName_Scenario_ExpectedResult` → `Handle_UnknownId_ReturnsFailure`.

## 8. Formatting (automated — do not hand-fix)

- `.editorconfig` + `dotnet format` on save / in CI. All files end with newline, UTF-8, 4-space indent C#.
- `var` when the type is apparent; explicit elsewhere.
- Braces always (no single-line `if` without braces).
