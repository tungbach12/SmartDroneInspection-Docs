---
title: "Minimal Clean Architecture"
weight: 20
---

# Minimal Clean Architecture in SmartDroneInspection

## Overview

The **Minimal Clean Architecture** implementation in SmartDroneInspection adapts Steve Smith's (Ardalis) Single-Project **Vertical Slice Architecture (VSA)**. It eliminates inter-project friction while preserving strict Clean Architecture principles: **Dependency Inversion**, **Domain Encapsulation**, and **Testability**.

---

## Directory Structure

```text
backend/MinimalClean/src/MinimalClean.Architecture.Web/
├── Domain/                         # Pure Domain Model (No Framework Dependencies)
│   ├── Assets/                     # Asset, AssetDocument, AssetLifecycleLog
│   ├── Missions/                   # DroneMission, InspectionRequest, MissionTelemetry, MissionImage
│   ├── Planning/                   # InspectionPlan, InspectionSchedule, CalendarEvent
│   ├── Reports/                    # InspectionReport, Defect, MaintenanceTicket, TicketHistory
│   ├── Users/                      # User, Organization, RefreshToken, AuditLog
│   ├── Ai/                         # KnowledgeCase, KnowledgeCaseEmbedding, AiAnalysisJob
│   └── Common/                     # EntityBase, IAuditable, ISoftDelete, Roles
│
├── Infrastructure/                 # Persistence & External Integrations
│   ├── Data/
│   │   ├── AppDbContext.cs         # EF Core DbContext with pgvector & global filters
│   │   ├── Config/                 # 29 Entity Configurations (indices, constraints, FKs)
│   │   └── EfRepository.cs         # Ardalis.Specification generic repository
│   └── Auth/                       # JwtTokenService, PasswordHasherAdapter, JwtOptions
│
├── Features/                       # Vertical Slices (One Folder per Endpoint)
│   ├── Assets/
│   │   ├── Create/                 # CreateAssetEndpoint.cs, CreateAssetValidator, DTOs
│   │   ├── GetById/                # GetAssetByIdEndpoint.cs
│   │   ├── List/                   # ListAssetsEndpoint.cs + PagedAssetsSpec.cs
│   │   ├── Update/                 # UpdateAssetEndpoint.cs
│   │   └── Delete/                 # DeleteAssetEndpoint.cs (Soft Delete)
│   ├── Auth/
│   │   ├── Login/                  # LoginEndpoint.cs (Lockout protection, JWT issuance)
│   │   └── RefreshToken/           # RefreshTokenEndpoint.cs (Single-use rotation)
│   ├── Missions/
│   │   ├── Create/                 # CreateInspectionRequestEndpoint.cs
│   │   ├── GetById/                # GetInspectionRequestByIdEndpoint.cs
│   │   └── List/                   # ListInspectionRequestsEndpoint.cs
│   ├── Reports/
│   │   ├── Create/                 # CreateInspectionReportEndpoint.cs
│   │   └── List/                   # ListInspectionReportsEndpoint.cs
│   └── Tickets/
│       ├── Create/                 # CreateMaintenanceTicketEndpoint.cs
│       └── List/                   # ListMaintenanceTicketsEndpoint.cs
│
└── Configurations/                 # Service registration, Serilog, Middleware, OpenAPI
```

---

## Key Ardalis Patterns Applied

### 1. REPR Pattern with FastEndpoints
Endpoints follow the **Request-Endpoint-Response (REPR)** pattern instead of God Controllers:

```csharp
public sealed class CreateAssetEndpoint(IRepository<Asset> repository) 
    : Endpoint<CreateAssetRequest, Results<Created<AssetDto>, ValidationProblem, ProblemHttpResult>>
{
    public override void Configure()
    {
        Post("/assets");
        AllowAnonymous(); // Configure authentication policies here
        Tags("Assets");
    }

    public override async Task<Results<Created<AssetDto>, ValidationProblem, ProblemHttpResult>> ExecuteAsync(
        CreateAssetRequest req, CancellationToken ct)
    {
        // Business logic with encapsulated entity
        var asset = new Asset(req.OrganizationId, req.CategoryId, req.Code, req.Name, req.Location, req.Coordinates);
        await repository.AddAsync(asset, ct);
        await repository.SaveChangesAsync(ct);

        return TypedResults.Created($"/assets/{asset.Id.Value}", new AssetDto(...));
    }
}
```

### 2. Ardalis.Specification Pattern
Queries are encapsulated as reusable, testable specification objects:

```csharp
public sealed class PagedAssetsSpec : Specification<Asset>
{
    public PagedAssetsSpec(Guid organizationId, int page, int pageSize, string? searchTerm = null)
    {
        var query = Query.Where(a => a.OrganizationId == organizationId);
        if (!string.IsNullOrWhiteSpace(searchTerm))
        {
            var term = searchTerm.Trim().ToUpperInvariant();
            query.Where(a => a.NormalizedCode.Contains(term) || a.Name.ToUpper().Contains(term));
        }

        query.OrderBy(a => a.Code)
             .Skip((page - 1) * pageSize)
             .Take(pageSize);
    }
}
```

### 3. Vogen Strongly-Typed IDs
Guards against accidental cross-entity ID misassignments (e.g., passing a `UserId` into an `AssetId` parameter):

```csharp
[ValueObject<Guid>]
public readonly partial struct AssetId { }
```

### 4. Vector Search Integration (pgvector)
Database configuration supports high-performance HNSW Cosine vector indexing for RAG:

```csharp
builder.Property(x => x.Embedding)
       .HasColumnType("vector(1536)")
       .IsRequired();

builder.HasIndex(x => x.Embedding)
       .HasMethod("hnsw")
       .HasOperators("vector_cosine_ops");
```
