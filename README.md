# SmartDroneInspection Documentation

Documentation for the SmartDroneInspection infrastructure inspection platform.

SmartDroneInspection manages assets, inspection planning, uploaded inspection evidence, reports, defects, and maintenance tickets. Inspection images are uploaded through the web or mobile application and stored in MinIO.

## Start here

- [Project reference](content/project-reference/) - business flows, SRS, source documents, and AI-readable Markdown.
- [Backend](content/backend/) - architecture and Java/Spring conventions.
- [Frontend](content/frontend/) - architecture and React/TypeScript conventions.
- [Mobile](content/mobile/) - architecture and Flutter/Dart conventions.
- [Authentication](content/backend/authentication-and-authorization.md) - current login, token, role, and session contract.
- [Development guide](content/development/) - shared AI-agent, Git, and pull-request rules.

Repository-specific setup commands are documented in the `README.md` files of `backend/`, `frontend/`, and `mobile/`.

## Repositories

| Repository | Stack | Scope |
| --- | --- | --- |
| `backend/` | Java 21, Spring Boot, Spring Modulith, PostgreSQL, MinIO | Modular monolith API, persistence, business logic, evidence storage, and AI integration |
| `frontend/` | React 19, TypeScript, Vite, Material UI | Browser portal for platform, organization, and service operations |
| `mobile/` | Flutter, Dart, Riverpod, GoRouter, Dio | Field workflows for inspectors and maintenance engineers |
| `docs/` | Markdown, Hugo | Specifications, architecture, API, and operational documentation |

## Current roles

- **Admin** - manages organizations, users, roles, categories, checklists, and platform configuration.
- **Client** - manages customer-organization assets, requests, approvals, released reports, and maintenance decisions.
- **Service Manager** - manages service requests, quotations, assignments, and result release.
- **Inspector** - works only on assigned inspections and reports.
- **Maintenance Engineer** - works only on assigned maintenance assessments and execution.

The platform uses deny-by-default authorization. Resource ownership, organization scope, assignment scope, and separation-of-duties are enforced in application services in addition to role checks.

## Documentation site

The repository is configured for Hugo using the `hugo-book` theme. The Markdown files under `content/` are the source for the documentation site.

`01-SYSTEM-SPECIFICATION.md` is kept as a compatibility pointer; the maintained requirement baseline is `content/project-reference/markdown/report3-software-requirement-specification.md`.

## Folder layout

```text
content/
├── project-reference/         # Business flows, SRS, source docs, and AI-readable Markdown
│   ├── markdown/
│   └── source-documents/
├── backend/                   # Backend architecture, authentication, and conventions
├── frontend/                  # Web architecture and conventions
├── mobile/                    # Mobile architecture and conventions
└── development/               # Shared AI-agent, Git, and pull-request rules
references/                    # Non-site source notes
```
