---
title: "Mobile Flutter Conventions"
weight: 20
aliases:
  - /coding-conventions/mobile-flutter/
---

# Mobile Flutter Conventions

The mobile application uses Flutter, Dart, Riverpod, GoRouter, Dio, Freezed, and JSON serialization. Use feature-first organization without forcing full Clean Architecture into simple screens.

## Structure

```text
lib/
|-- core/                    # app-wide environment, network, router, theme
|-- features/<feature>/      # feature-owned code
|   |-- data/                # API models and repository implementation, when needed
|   |-- domain/              # meaningful business model or boundary, when needed
|   `-- presentation/        # pages, widgets, and Riverpod state
`-- shared/                  # stable reusable widgets and utilities
```

- **MO-01 MUST** keep feature-specific code inside its feature.
- **MO-02 SHOULD** start a simple feature in `presentation` and add `data` or `domain` only when actual behavior requires them.
- **MO-03 MUST NOT** create a repository interface and use-case class for a one-call screen unless they isolate meaningful business rules or an external boundary.
- **MO-04 SHOULD** move code into `core` or `shared` only when it is feature-neutral and reused.

## Dart, widgets, and state

- **MO-05 MUST** follow `analysis_options.yaml` and keep analyzer warnings at zero.
- **MO-06 SHOULD** use immutable models and `const` widgets where practical.
- **MO-07 SHOULD** split widgets by responsibility, not by arbitrary line count.
- **MO-08 MUST** use Riverpod for shared asynchronous or application state. Keep temporary visual state local to the widget when possible.
- **MO-09 SHOULD** use `Notifier` or `AsyncNotifier` only when the state has real transitions; a simple provider/future is sufficient for simple reads.
- **MO-10 MUST** represent loading, data, empty, and failure states explicitly for remote data.

## Networking and security

- **MO-11 MUST** use the shared Dio client and typed failure/result model. Features must not construct independent clients with different auth behavior.
- **MO-12 MUST** store mobile credentials only in `flutter_secure_storage`; never use preferences or source-code constants for secrets.
- **MO-13 MUST** keep token attachment and single-flight refresh behavior in the shared auth interceptor/token store.
- **MO-14 MUST NOT** log passwords, tokens, sensitive headers, or full sensitive response bodies.
- **MO-15 MUST** enforce role and assignment rules on the backend; hiding a mobile screen is not authorization.

## Generated code and naming

- **MO-16 MUST NOT** hand-edit `*.g.dart`, `*.freezed.dart`, or other generated files.
- Change the source file, then run `dart run build_runner build --delete-conflicting-outputs` when generation is required.
- Files use `snake_case.dart`; classes use `PascalCase`; members use `camelCase`; providers use descriptive lower-camel names.

## Testing and verification

- Unit-test business/state transitions and serialization where they can fail.
- Widget-test important loading, error, and user-action flows.
- Run `dart format --set-exit-if-changed .`, `flutter analyze`, and `flutter test` before handoff.
