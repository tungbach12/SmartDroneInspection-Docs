# SmartDroneInspection Documentation

Documentation for the SmartDroneInspection infrastructure inspection platform.

SmartDroneInspection manages assets, inspection planning, uploaded inspection evidence, reports, findings, and maintenance tickets. Inspection images are uploaded through the web or mobile application and stored in MinIO.

## Start here

- [Documentation home](_index.md) - the current documentation map.
- [Project reference](project-reference/) - workflows, data model, and project guides.
- [Reports](reports/) - formal reports, including Report 3 SRS and Report 5 test report.
- [Backend](backend/) - architecture, authentication, and Java/Spring conventions.
- [Frontend](frontend/) - architecture and React/TypeScript conventions.
- [Mobile](mobile/) - architecture and Flutter/Dart conventions.
- [Development guide](development/) - shared AI-agent, Git, and pull-request rules.

Repository-specific setup commands are documented in the `README.md` files of `backend/`, `frontend/`, and `mobile/`.

## Repositories

| Repository | Stack | Scope |
| --- | --- | --- |
| `backend/` | Java 21, Spring Boot, Spring Modulith, PostgreSQL, MinIO | Modular monolith API, persistence, business logic, evidence storage, and AI integration |
| `frontend/` | React 19, TypeScript, Vite, Material UI | Browser portal for platform, client, and service operations |
| `mobile/` | Flutter, Dart, Riverpod, GoRouter, Dio | Field workflows for inspectors and maintenance engineers |
| `docs/` | Markdown, Hugo | Project reports, architecture, API, and operational documentation |

## Current roles

- **Admin** - manages organizations, users, roles, categories, checklists, and platform configuration.
- **Client** - manages customer-organization assets, requests, approvals, released reports, and maintenance decisions.
- **Service Manager** - manages service requests, quotations, assignments, and result release.
- **Inspector** - works only on assigned inspections and reports.
- **Maintenance Engineer** - works only on assigned maintenance assessments and execution.

The platform uses deny-by-default authorization. Resource ownership, organization scope, assignment scope, and separation-of-duties are enforced in application services in addition to role checks.

## Documentation site

The repository is configured for Hugo using the `hugo-book` theme. The maintained documentation is organized in the top-level folders listed below; do not create a new `content/` or `docs/content/` tree.

## Folder layout

```text
backend/                 # Backend architecture and conventions
development/             # Agent rules, Git/PR rules, and implementation plans
frontend/                # Web architecture and conventions
mobile/                  # Mobile architecture and conventions
project-reference/       # Workflows, data model, and project guides
reports/                 # Self-contained formal report folders
tools/                   # Documentation/project-support tooling
```

Each report is maintained in one self-contained folder under `reports/`; do not add report content under legacy folders.
