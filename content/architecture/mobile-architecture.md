---
title: "Mobile Architecture"
weight: 30
---

# Mobile Architecture

The mobile application is a Flutter feature-first client for Inspector and Maintenance Engineer workflows. It uses Riverpod for state and dependency management, GoRouter for navigation, and Dio for HTTP communication.

## Source layout

```text
mobile/lib/
├── core/
│   ├── env/                      # Environment and API configuration
│   ├── network/                  # Dio, auth interceptor, token store, failures
│   ├── router/                   # GoRouter navigation
│   └── theme/                    # App theme and design tokens
├── shared/                       # Reusable widgets
└── features/
    └── <feature>/
        ├── domain/              # Freezed models and repository contracts
        ├── data/                # Data sources and repository implementations
        └── presentation/        # Pages, widgets, and Riverpod providers
```

Current features include `assets`, `auth`, `inspections`, `tasks`, and `profile`. Each feature follows the same `domain`, `data`, and `presentation` separation. Domain models do not depend on Flutter widgets or network implementations.

## State and networking

- Riverpod 3 manages providers, screen state, and dependency injection.
- Prefer `AsyncNotifier` or `Notifier` for stateful workflows.
- Dio uses an auth interceptor to attach access tokens and coordinate refresh after an expired token.
- Tokens are stored with `flutter_secure_storage`; they are never persisted in ordinary preferences or logs.
- Mobile calls the versioned `/api/v1/mobile/auth/**` contract and stores the access and refresh tokens securely.

## Role boundaries

The mobile client is designed for `INSPECTOR` and `MAINTENANCE_ENGINEER` workflows. Route visibility can improve the user experience, but the backend remains responsible for assignment scope, organization scope, and all final authorization decisions.

Run `flutter test` for tests and `dart run build_runner build --delete-conflicting-outputs` after changing generated Freezed or JSON-serializable models.
