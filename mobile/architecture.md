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

The mobile client is designed for `INSPECTOR` and `MAINTENANCE_ENGINEER` workflows. Organization registration and customer approvals are web-first experiences, although the mobile API exposes the same controlled registration contract for clients that need it. Route visibility can improve the user experience, but the backend remains responsible for assignment scope, organization scope, and all final authorization decisions.

## Assignment inbox and field sessions

The inspection feature includes an Inspector assignment inbox backed by
`/api/v1/inspection-assignments/mine`. It displays unanswered pairings and
submits accept/reject responses through
`POST /api/v1/inspection-assignments/{assignmentId}/response`, requiring a reason
for rejection. The backend resolves the caller and assignment scope; the client
does not choose an Inspector or organization. Assignment acceptance does not
grant readiness.

The field-session screens list an Inspector's sessions for an assigned
inspection, record a pre-flight note and request Start, and support postponement
or abort with a reason. Start is available only after backend readiness/state
checks; it records a software session and does not control or arm the Drone.
Source-change invalidation is partial in the backend, and no session-end /
`FIELD_COMPLETED` operation is currently available. These are server-enforced
boundaries, not client-only workflow assumptions.

## Inspection capture

An Inspector opens a detail flow for an assigned inspection that reads the
scoped evidence and the evidence-quality decision history. Camera capture uses
`image_picker`; uploads send multipart image bytes with source `MOBILE_UPLOAD`
and capture time. A failed upload keeps the selected image available for retry.
The backend validates content, computes the checksum, enforces assignment scope,
and streams stored evidence; the mobile client does not access MinIO directly.
On iOS, the camera usage message is configured in `Info.plist`.

Report authoring, review, and publication stay web-only. They are governance
decisions with a separation-of-duties requirement, not field capture, so the
mobile client does not duplicate them.

Run `flutter test` for tests and `dart run build_runner build --delete-conflicting-outputs` after changing generated Freezed or JSON-serializable models.
