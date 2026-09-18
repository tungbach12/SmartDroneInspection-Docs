# SmartDroneInspection Documentation

Documentation for the SmartDroneInspection infrastructure inspection platform.

SmartDroneInspection manages assets, inspection planning, uploaded inspection evidence, reports, defects, and maintenance tickets. Inspection images are uploaded through the web or mobile application and stored in MinIO.

## Start here

- [Project overview](content/overview/) - system specification and business flows.
- [System architecture](content/architecture/) - backend, frontend, and mobile structure.
- [Authentication](content/security/authentication.md) - current login, token, role, and session contract.
- [Coding conventions](content/coding-conventions/) - backend, web, mobile, and Git practices.

Repository-specific setup commands are documented in the `README.md` files of `backend/`, `frontend/`, and `mobile/`.

## Repositories

| Repository | Stack | Scope |
| --- | --- | --- |
| `backend/` | Java 21, Spring Boot, Spring Modulith, PostgreSQL, MinIO | Modular monolith API, persistence, business logic, evidence storage, and AI integration |
| `frontend/` | React 19, TypeScript, Vite, Material UI | Browser portal for platform, organization, and service operations |
| `mobile/` | Flutter, Dart, Riverpod, GoRouter, Dio | Field workflows for inspectors and maintenance engineers |
| `docs/` | Markdown, Hugo | Specifications, architecture, API, and operational documentation |

## Current roles

- **Platform Administrator** - manages organizations, users, roles, categories, checklists, and platform configuration.
- **Organization Manager** - manages customer-organization assets, requests, plans, and reports.
- **Service Operations Manager** - manages service requests, quotations, assignments, and result release.
- **Inspector** - works only on assigned inspections and reports.
- **Maintenance Engineer** - works only on assigned maintenance assessments and execution.

The platform uses deny-by-default authorization. Resource ownership, organization scope, assignment scope, and separation-of-duties are enforced in application services in addition to role checks.

## Documentation site

The repository is configured for Hugo using the `hugo-book` theme. The Markdown files under `content/` are the source for the documentation site.

`01-SYSTEM-SPECIFICATION.md` is kept as a compatibility pointer; the maintained copy is `content/overview/system-specification.md`.

## Folder layout

```text
content/
├── overview/                  # What the product does and how work flows
├── architecture/              # Backend, frontend, and mobile architecture
│   ├── backend-architecture.md
│   ├── frontend-architecture.md
│   └── mobile-architecture.md
├── security/                  # Authentication and access control
└── coding-conventions/        # Backend, web, mobile, and Git practices
references/                    # Non-site source notes
```
