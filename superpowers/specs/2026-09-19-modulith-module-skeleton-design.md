# Spring Modulith Capability Module Skeleton

## Status

Proposed design for review before implementation.

## Intent

Make the intended business-capability structure visible in the backend before
WF3 and WF4 runtime work begins. The skeleton must establish stable Modulith
module roots without inventing domain entities, controllers, services, events,
or ports that no current use case needs.

## Target module roots

```text
com.smartdroneinspection/
├── users/                 # implemented: identity and administration
├── assets/                # implemented: WF1 asset catalog and schedules
├── inspectionrequests/    # implemented: WF2 requests and assignments
├── inspections/           # scaffolded: WF3 runtime comes later
├── maintenance/           # scaffolded: WF4 runtime comes later
├── notifications/         # scaffolded supporting capability
├── dashboard/             # scaffolded read-only composition
├── shared/                # implemented minimal cross-cutting contracts
└── infrastructure/        # scaffolded outbound-adapter boundary
```

The four implemented modules keep their existing production code. Each
scaffolded module receives only a root `package-info.java` with an explicit
display name and conservative dependency policy. Empty nested packages such as
`api`, `domain`, `service`, `events`, and `spi` are not added yet; they will be
created with the first real vertical slice that owns code there.

## Dependency policy

The intended graph remains acyclic:

```text
users -> shared::auth, shared::config, shared::exception
assets -> shared
inspectionrequests -> assets, shared
inspections -> inspectionrequests, assets, shared
maintenance -> inspections, inspectionrequests, shared
notifications -> feature-owned events when those interfaces exist
dashboard -> feature root read APIs when implemented
infrastructure -> feature-owned SPI and shared when implemented
```

Until event and SPI packages contain real interfaces, scaffolded modules do
not declare speculative named-interface dependencies. Concrete dependencies
are added with the runtime slice that needs them. Business modules never
depend on `infrastructure`.

## Cleanup boundary

The checkout root may contain empty legacy directories named `ai`, `missions`,
`reports`, `defects`, and `tickets`. They are not tracked source packages and
will be removed from the active checkout after confirming they contain no
files. Existing unrelated worktrees are not inspected or modified.

## Documentation alignment

Backend onboarding, architecture, conventions, and database-status guidance
will describe scaffolded roots separately from implemented runtime modules.
The documentation will continue to state that reports/findings/AI candidates
belong inside WF3, maintenance tickets belong inside `maintenance`, and
adapters belong inside `infrastructure`.

## Non-goals

- No database migration, table, column, or Flyway-history change.
- No API, authentication, authorization, or persisted-value behavior change.
- No placeholder business entities, controllers, services, events, or ports.
- No changes to the approved SRS or business-flow reference documents.

## Verification and integration

- Run `ApplicationModules.verify()` through the backend architecture test.
- Run the targeted SQL-contract tests and the full backend verification when
  Docker is available.
- Run docs link and whitespace checks; run Hugo only when installed.
- Commit backend and docs separately on feature branches, open focused PRs,
  and merge backend before docs.
