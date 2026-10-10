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

## Assignment inbox (MF2-01/02)

The home inspections screen is the entry point to MF2: an Inspector sees the
pairings the organization administrator opened for them, and accepts or declines
with a reason. Without this inbox there is no way to begin MF2 from the device the
Inspector carries into the field, because preparation, readiness and the field
session all sit downstream of a pairing the Inspector took.

The inbox shows the asset, the assigned Drone and its validity window so the answer
can be given without opening three other screens. Accepting records that the
Inspector took the job; it is not flight clearance. MF2-07 decides separately,
with a named independent reviewer, whether the mission may fly. A decline stays
disabled until the Inspector writes a reason, because the server refuses without
one and only the Inspector knows whether they lack a qualification, a date or a
willingness.

The repository calls `/inspection-assignments/mine` and
`/inspection-assignments/{id}/response`. The earlier `listAcceptedAssignments`
and `start` used `/inspections/assignments` and `/inspections/start`, which this
backend does not have; they and the models used only by those calls are removed.
The inspection checklist remains on the current backend contract and is not
reached by this inbox.

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

Run `flutter test` for tests and `dart run build_runner build --delete-conflicting-outputs` after changing generated Freezed or JSON-serializable models.
