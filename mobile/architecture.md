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

## Field session (MF2-09 to MF2-11)

The field session has its own route, `/inspection/{id}/session`, rather than
living inside the inspection detail screen. MF2-09 has the Inspector on site
identifying the assigned Drone and completing the pre-flight checklist before
asking to start, postponing or aborting. That is a different act from reading the
checklist and evidence that screen exists to show, and folding the two together
made the captured record harder to reach.

The screen records only what the Inspector writes. The pre-flight note is typed
rather than ticked, because a checkbox a client can set without reading anything
would attest to nothing. An abort asks for confirmation before it fires: a
mistaken tap on a phone in the field ends a session that cannot resume, so the
extra tap is cheaper than the mistake. A postponement needs no confirmation,
because it hands the inspection back for another attempt.

The session stores the readiness decision it started against, which is what makes
a later audit able to answer which approval the field work relied on. Nothing on
this screen arms a Drone. Starting records that the software agreed the paperwork
and the pre-flight checklist were in order, and the session start time is not
hardware flight time.

`InspectionRepository` also still carries `listAssignments`, `start` and
`checklist` from an earlier baseline. Those endpoints do not exist in the current
backend, nothing calls them from the UI, and they are left in place rather than
removed, because deleting another baseline's surface is not this change's
business.

Run `flutter test` for tests and `dart run build_runner build --delete-conflicting-outputs` after changing generated Freezed or JSON-serializable models.
