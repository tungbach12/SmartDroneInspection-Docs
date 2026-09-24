---
title: "Mobile Architecture"
weight: 10
aliases:
  - /architecture/mobile-architecture/
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
        ├── presentation/        # Pages, widgets, and Riverpod providers
        ├── data/                # API and repository code, when needed
        └── domain/              # Business models or boundaries, when needed
```

Current features include `assets`, `auth`, `inspections`, `tasks`, and `profile`. A simple feature can contain only `presentation/`; add `data/` or `domain/` when the feature has enough networking or business behavior to justify those boundaries. Empty layers are not required.

## State and networking

- Riverpod 3 manages providers, screen state, and dependency injection.
- Prefer `AsyncNotifier` or `Notifier` for stateful workflows; use a simpler provider for simple reads.
- Dio uses an auth interceptor to attach access tokens and coordinate refresh after an expired token.
- Shared Dio clients unwrap successful `{ success, message, data }` API
  envelopes, including mobile auth and refresh responses. Problem Details,
  bodyless `204` responses, and binary evidence downloads remain unchanged.
- Tokens are stored with `flutter_secure_storage`; they are never persisted in ordinary preferences or logs.
- Mobile calls the versioned `/api/v1/mobile/auth/**` contract and stores the access and refresh tokens securely.

## Role boundaries

The mobile client is designed for `INSPECTOR` and `MAINTENANCE_ENGINEER` workflows. Client organization registration and customer approvals are web-first experiences, although the mobile API exposes the same controlled registration contract for clients that need it. Route visibility can improve the user experience, but the backend remains responsible for assignment scope, organization scope, and all final authorization decisions.

Run `flutter test` for tests and `dart run build_runner build --delete-conflicting-outputs` after changing generated Freezed or JSON-serializable models.
