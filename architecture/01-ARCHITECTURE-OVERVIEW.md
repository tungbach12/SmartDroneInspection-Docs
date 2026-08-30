# Architecture Overview

> SmartDroneInspection — FA26SE112 · Capstone 09/2026 – 03/2027

## 1. System Context

```
┌─────────────────┐     REST/JSON      ┌──────────────────────────┐
│  Web Portal     │◄──────────────────►│                          │
│  React + MUI    │                    │   SmartDroneInspection   │
└─────────────────┘                    │   ASP.NET Core 9 API     │
                                       │                          │
┌─────────────────┐     REST/JSON      │  ┌────────────────────┐ │      ┌───────────────┐
│  Mobile App     │◄──────────────────►│  │  Business Modules  │ │      │ PostgreSQL    │
│  Flutter        │                    │  └────────────────────┘ │      │ (EF Core)     │
└─────────────────┘                    │                          │      └───────────────┘
                                       │  ┌────────────────────┐ │      ┌───────────────┐
┌─────────────────┐                    │  │  SignalR Hubs      │ │      │ MinIO         │
│ SmartDroneHub   │◄──────────────────►│  └────────────────────┘ │◄────►│ (evidence/    │
│ (external drone │  Mission API +     │                          │      │  images)      │
│  platform)      │  telemetry/images  │  ┌────────────────────┐ │      └───────────────┘
└─────────────────┘                    │  │  AI Integrations   │ │      ┌───────────────┐
                                       │  └────────────────────┘ │◄────►│ DroneVisionAI │
                                       └──────────────────────────┘      │ DroneKnow-    │
                                                                         │ ledgeAI, LLM  │
                                                                         └───────────────┘
```

**Key rule:** SmartDroneInspection is a *consumer* of SmartDroneHub, never a drone controller.

## 2. Backend — Clean Architecture

```
backend/
├─ SmartDroneInspection.sln
├─ src/
│  ├─ SmartDroneInspection.Domain/          # Layer 0: no dependencies
│  │  ├─ Common/                            #   BaseEntity, Result, Roles
│  │  └─ {Users|Assets|Inspections|Reports|Defects|Tickets|Ai}/   # entities + enums per module
│  ├─ SmartDroneInspection.Application/     # Layer 1: depends on Domain
│  │  ├─ Common/
│  │  │  ├─ Interfaces/                     #   ISmartDroneHubClient, IObjectStorage, ICurrentUserService
│  │  │  ├─ Behaviors/                      #   MediatR pipeline (ValidationBehavior)
│  │  │  └─ Mappings/
│  │  └─ {Users|Assets|Inspections|Reports|Defects|Tickets|Ai|Dashboard}/
│  │     └─ Commands/ Queries/ Dtos/        #   CQRS per module
│  ├─ SmartDroneInspection.Infrastructure/  # Layer 2: depends on Application
│  │  ├─ Persistence/                       #   ApplicationDbContext, Configurations/, Migrations/, Seed/
│  │  ├─ Auth/                              #   JwtTokenService, RBAC policies
│  │  ├─ External/SmartDroneHub/            #   typed HttpClient
│  │  ├─ External/AiServices/               #   DroneVisionAI, DroneKnowledgeAI, LLM clients
│  │  └─ Storage/                           #   MinioStorage (IObjectStorage)
│  └─ SmartDroneInspection.Api/             # Layer 3: host, depends on Infrastructure
│     ├─ Controllers/                       #   thin — HTTP mapping only
│     ├─ Hubs/                              #   SignalR (MissionHub)
│     └─ Middleware/
└─ tests/
   ├─ SmartDroneInspection.UnitTests/       # xUnit, folder per module
   └─ SmartDroneInspection.IntegrationTests/ # Testcontainers + real PostgreSQL
```

### Dependency rules (enforced by project references)

| Project | May reference | Must never reference |
|---------|--------------|---------------------|
| Domain | — nothing | anything |
| Application | Domain | Infrastructure, Api |
| Infrastructure | Application | Api |
| Api | Infrastructure | — |

Domain and Application contain **zero** EF Core / HTTP / MinIO code — only interfaces. Infrastructure implements them.

### Why this fits a 4-person team

- Each member owns **one module folder across all layers** (Assets → Quốc; Inspections+Missions → Như; Reports+Defects+Tickets → Như/Hiếu per WP3; Ai+Dashboard → Bách; Users+foundation → Hiếu).
- Cross-module calls go through `Application/Common/Interfaces` or MediatR events — never direct module references.
- `ApplicationDbContext` + migrations owned by one person (Leader); others contribute `IEntityTypeConfiguration` files inside their own module folder only.

## 3. Backend Patterns (decided)

| Concern | Decision |
|---------|----------|
| CQRS | MediatR, one command/query per operation, pipeline behaviors for validation/logging |
| Validation | FluentValidation via pipeline behavior |
| Repositories | **None** — handlers use `ApplicationDbContext` directly |
| Errors | `Result`/`Result<T>` for expected failures → ProblemDetails; exceptions for unexpected only |
| API docs | Built-in OpenAPI (`AddOpenApi`) + Scalar UI (dev only) |
| Logging | Serilog: console + file, request logging |
| Auth | JWT Bearer + role policies from `Domain/Common/Roles` |
| Migrations | Single `ApplicationDbContext`, per-module `IEntityTypeConfiguration` files |

## 4. Frontend — React 19 + TypeScript (feature-based)

```
frontend/src/
├─ app/                     # router, theme, layouts (AppShell), providers
├─ shared/
│  ├─ api/                  # axios instance, JWT interceptors, single-flight refresh
│  ├─ ui/                   # DataTable, LoadingButton, PageHeader, StatusChip, Toast, ConfirmDialog, QueryState
│  ├─ hooks/  utils/
└─ features/                # one folder per business module — owned by one dev
   ├─ auth/                 #   store (zustand), guards, login
   ├─ assets/  inspections/  reports/  ai/  users/
   │  └─ api/ components/ pages/ types/ (hooks/, store/ when needed)
```

- Server state: **TanStack Query**; client state: **Zustand** (persisted auth).
- Forms: **react-hook-form + zod**; routing: **react-router v7** with `RequireAuth` role guards and lazy-loaded pages.
- Feature export via `index.ts`; `@/` path alias to `src/`; no cross-feature relative imports.

## 5. Mobile — Flutter (feature-first)

```
mobile/lib/
├─ core/                    # router (GoRouter), DI, theme, env, token store
├─ shared/                  # shared widgets, utils
└─ features/
   └─ {auth|inspections|reports|maintenance}/
      ├─ data/              # repositories, DTOs, dio client per feature
      ├─ domain/            # Freezed models
      └─ presentation/      # screens, widgets, Riverpod providers
```

- State: **Riverpod 3** (provider colocated with its class, `Notifier`/`AsyncNotifier` for state).
- HTTP: **Dio** + JWT interceptor with single-flight refresh; tokens in `flutter_secure_storage`.
- Models: **Freezed + json_serializable**; generation committed.
- Scope: Inspector + Maintenance Engineer flows only (evidence photos, ticket updates, offline drafts).

## 6. Cross-cutting Decisions

| Concern | Decision |
|---------|----------|
| Database | PostgreSQL 16, all modules in one schema, Guid PKs |
| Storage | MinIO, presigned URLs for upload/download |
| Real-time | SignalR `MissionHub` for mission status push |
| Deployment | Docker Compose: api, postgres, minio (+ frontend/nginx) |
| Config | appsettings per env; secrets via env vars / user-secrets, never committed |
| Testing | Unit: xUnit per module. Integration: Testcontainers PostgreSQL + Respawn |
| CI law | `.editorconfig`, `dotnet format`, ESLint, `dart analyze` run in CI — linters are the enforcement, not memory |
