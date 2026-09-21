# SmartDroneInspection Documentation

Documentation for the SmartDroneInspection infrastructure inspection platform.

SmartDroneInspection manages assets, inspection planning, uploaded inspection evidence, reports, findings, and maintenance tickets. Inspection images are uploaded through the web or mobile application and stored in MinIO.

## Start here

- [Project reference](content/project-reference/) - project reports, workflows, data model, and project guides.
- [Backend](content/backend/) - architecture, authentication, and Java/Spring conventions.
- [Frontend](content/frontend/) - architecture and React/TypeScript conventions.
- [Mobile](content/mobile/) - architecture and Flutter/Dart conventions.
- [Development guide](content/development/) - shared AI-agent, Git, and pull-request rules.

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

The repository is configured for Hugo using the `hugo-book` theme. Markdown files under `content/` are the source for the documentation site.

`01-SYSTEM-SPECIFICATION.md` remains a compatibility pointer. Each report is maintained in one self-contained folder under `content/project-reference/reports/`.

## Folder layout

```text
content/
├── project-reference/
│   ├── reports/                     # Report 1-3: Markdown, DOCX, images, and indexes
│   │   ├── report-1-project-introduction/
│   │   ├── report-2-project-management-plan/
│   │   └── report-3-software-requirement-specification/
│   ├── workflows/                   # WF1-WF4 business flows
│   ├── data-model/                  # Database design
│   ├── guides/                      # Project and defense checklists
├── backend/                          # Backend architecture and conventions
├── frontend/                         # Web architecture and conventions
├── mobile/                           # Mobile architecture and conventions
└── development/                     # Shared AI-agent and Git/PR rules

references/                           # Non-site provenance notes
superpowers/                           # Internal planning artifacts, not site content
```

Each report is maintained in one self-contained folder under `content/project-reference/reports/`; do not add report content under legacy folders.
