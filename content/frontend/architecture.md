---
title: "Frontend Architecture"
weight: 10
aliases:
  - /architecture/frontend-architecture/
---

# Frontend Architecture

The web portal is a React 19 and TypeScript application built with Vite and Material UI. Its structure follows business features so pages, API calls, and UI components can evolve together.

## Source layout

```text
frontend/src/
├── app/
│   ├── layouts/                 # App shell and layout components
│   ├── router/                  # Routes and route guards
│   └── theme/                   # Material UI theme
├── features/
│   ├── auth/                    # Client registration, login, and role guard
│   ├── assets/                  # Asset pages, API, and hooks
│   └── ai/                      # AI dashboard pages
├── shared/
    ├── api/                     # Axios client and shared transport helpers
    └── ui/                      # Reusable presentation components
└── assets/                      # Static images and icons
```

Feature folders are added as their screens are implemented. A feature may contain `api/`, `components/`, `pages/`, `hooks/`, and local types. Cross-feature relative imports are avoided; shared behavior belongs under `src/shared/`.

## State and data flow

- TanStack Query owns server state, cache invalidation, and request lifecycle.
- Query key factories keep list and detail caches predictable.
- Zustand owns small client-only state such as the current user, active organization, and UI notifications.
- Axios provides the versioned `/api/v1` client and a single-flight queue for access-token refresh after a `401` response.

## Routing and authorization

React Router lazy-loads feature routes. `RequireAuth` protects authenticated pages and checks the roles returned by the backend. These checks improve navigation but do not replace backend organization, assignment, or resource authorization.

The current role names are `ADMIN`, `CLIENT`, `SERVICE_MANAGER`, `INSPECTOR`, and `MAINTENANCE_ENGINEER`.

The web auth feature owns the Client onboarding form as well as login and session UX. The first Client representative can create a new organization and account through the backend registration contract; the web does not collect or persist a refresh token in application state.

## UI conventions

Material UI provides the shared theme, including light and dark color schemes. Reusable components such as `DataTable`, `LoadingButton`, `StatusChip`, `PageHeader`, `ConfirmDialog`, and `QueryState` live in `src/shared/ui/`.

Run `npm run build` for the strict TypeScript build and `npm run lint` for Oxlint checks.
