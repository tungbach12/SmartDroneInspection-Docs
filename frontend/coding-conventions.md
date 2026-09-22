---
title: "Frontend React Conventions"
weight: 20
aliases:
  - /coding-conventions/frontend-react/
---

# Frontend React Conventions

The web portal uses React 19, strict TypeScript, Vite, Material UI, TanStack Query, Zustand, Axios, React Hook Form, and Zod.

## Structure

```text
src/
|-- app/                    # bootstrap, router, layouts, theme
|-- features/<feature>/     # feature-owned API, pages, components, state, types
`-- shared/                 # stable feature-neutral API and UI building blocks
```

- **FE-01 MUST** keep business behavior in the owning feature.
- **FE-02 SHOULD** create `api`, `components`, `hooks`, `pages`, `store`, or `types` folders only when the feature needs them.
- **FE-03 MUST NOT** import another feature through a deep relative path. Use an intentional public export or move truly shared code to `shared`.
- **FE-04 SHOULD** keep a component near its only consumer. Promote it to `shared/ui` only after it is genuinely reusable and feature-neutral.

## TypeScript and components

- **FE-05 MUST** keep strict TypeScript enabled. Avoid `any`; use `unknown` and narrow it when an external value is not trusted.
- **FE-06 MUST** define API request and response types explicitly. Do not cast an unvalidated response into the desired type.
- **FE-07 SHOULD** keep components focused on one UI responsibility and extract behavior into a hook only when it is reused or materially simplifies the component.
- **FE-08 SHOULD** prefer composition over large components controlled by many boolean props.
- **FE-09 SHOULD NOT** add `useMemo`, `useCallback`, or `React.memo` without a measured or clear render-cost reason.
- **FE-10 MUST** provide stable keys for lists and accessible labels for interactive controls.

## State and data fetching

- **FE-11 MUST** use TanStack Query for remote/server state, including cache invalidation and request status.
- **FE-12 MUST NOT** copy query data into Zustand or component state unless the user is editing a separate draft.
- **FE-13 SHOULD** use a query-key factory for resources with list/detail variants.
- **FE-14 SHOULD** keep local UI state local. Use Zustand only for small cross-route client state such as authenticated-user state or global notifications.
- **FE-15 MUST** handle loading, empty, error, and success states for data-driven pages.

## Forms, UI, and authentication

- **FE-16 SHOULD** use React Hook Form with Zod for non-trivial forms; the backend remains the authority for business validation.
- **FE-17 MUST** use the shared Material UI theme and existing UI primitives before creating one-off styling systems.
- **FE-18 MUST NOT** persist access tokens in `localStorage`, `sessionStorage`, IndexedDB, or Zustand persistence. Keep the access token in memory; the browser refresh credential is an HttpOnly cookie handled by the shared API client.
- **FE-19 MUST** centralize refresh/retry behavior in the Axios client. Feature code must not implement competing refresh loops.
- **FE-20 MUST** treat route guards as user experience only; backend authorization remains mandatory.

## Naming and testing

- Components/pages: `PascalCase.tsx`; hooks: `useXxx.ts`; stores: `xxxStore.ts`; non-component utilities: `camelCase.ts`.
- Test behavior visible to a user. Prefer role/label queries over DOM structure selectors.
- A defect fix SHOULD include a regression test when the affected area has a test harness.
- Run `npm run lint` and `npm run build` before handoff.
