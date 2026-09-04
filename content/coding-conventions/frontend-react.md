---
title: "Frontend React Conventions"
weight: 2
---

# Frontend React Conventions

## 1. Project Structure (Feature-Based)
* Code is organized by business feature under `src/features/<module>/` (`auth`, `assets`, `inspections`, `reports`, `ai`, `users`).
* Each feature folder contains:
  * `api/`: TanStack Query hooks, query keys factory, API calls.
  * `components/`: UI components specific to the feature.
  * `pages/`: Page-level components.
  * `types.ts`: TypeScript interfaces and types.

## 2. State Management
* **Server State**: Managed exclusively with **TanStack Query (React Query v5)**.
* **Query Keys**: Use consistent key factories:
  ```typescript
  export const assetKeys = {
    all: ['assets'] as const,
    lists: () => [...assetKeys.all, 'list'] as const,
    list: (filters: AssetFilters) => [...assetKeys.lists(), filters] as const,
    details: () => [...assetKeys.all, 'detail'] as const,
    detail: (id: string) => [...assetKeys.details(), id] as const,
  };
  ```
* **Client State**: Global UI state (user auth, active organization, toast notifications) uses **Zustand**.

## 3. UI & Styling
* **Material UI (MUI v6)** with unified theme system (`light`/`dark` modes).
* Reusable dumb components placed in `src/shared/ui/` (`DataTable`, `LoadingButton`, `StatusChip`, `PageHeader`).
