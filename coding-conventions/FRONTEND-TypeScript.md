# Coding Conventions — Frontend (React + TypeScript + MUI)

> Enforced by `tsconfig` strict mode + ESLint in CI. Reviewers check logic, not style.

## 1. Naming

| Element | Rule | Example |
|---------|------|---------|
| Component | PascalCase | `AssetList.tsx` → `export function AssetList()` |
| Hook | `use` + PascalCase | `useInspections.ts` → `useInspections()` |
| Component file | PascalCase.tsx | `AssetDetailDrawer.tsx` |
| Hook / util / api file | camelCase.ts | `assetApi.ts`, `formatDate.ts` |
| Type / Interface | PascalCase, **no I prefix** | `Inspection`, `InspectionStatus` |
| Union / alias | `type` | `type Role = 'Admin' \| 'Viewer'` |
| Constant | UPPER_SNAKE_CASE (module-level only) | `MAX_UPLOAD_MB = 50` |
| Zustand store | `use` + Domain + `Store` | `useAuthStore` |
| Query key factory | Domain + `Keys` | `inspectionKeys` |

## 2. Components & files

- Function components only. No classes, no `React.FC`.
- **Named exports everywhere** — never mix default and named in one file:

```tsx
export function StatusChip({ status }: StatusChipProps) { ... }
```

- Props: `interface` for object props; `type` only for unions/aliases.
- One component per file (tiny sub-components used by only one parent may live in the same file above the parent).
- Colocation: everything a feature needs lives in `features/<module>/`. Only cross-feature code goes to `shared/`.

## 3. Folder layout per feature

```
features/inspections/
├─ api/
│  ├─ inspectionApi.ts          # endpoint functions, typed
│  └─ inspectionKeys.ts         # query-key factory
├─ components/                  # feature-specific components
├─ pages/                       # route targets (lazy-loaded)
├─ hooks/
├─ store/                       # only if the module needs client state
└─ types.ts
```

## 4. TanStack Query

- One key factory per module, `as const` arrays, nested structure:

```ts
export const inspectionKeys = {
  all: ['inspections'] as const,
  lists: () => [...inspectionKeys.all, 'list'] as const,
  list: (filters: InspectionFilters) => [...inspectionKeys.lists(), filters] as const,
  detail: (id: string) => [...inspectionKeys.all, 'detail', id] as const,
};
```

- Use keys everywhere — `useQuery({ queryKey: inspectionKeys.list(filters) })`.
- Invalidation uses the broadest matching key (`inspectionKeys.all`) after mutations that affect the domain.
- Mutations show success/error via `shared/ui/Toast` (`useToastStore.getState().showToast(...)`).

## 5. Zustand

- One store per domain, in `features/<domain>/store/`.
- Access with selectors, never the whole store:

```ts
const userName = useAuthStore((s) => s.userName);          // ✅
const store = useAuthStore();                               // ❌ re-renders on every change
```

- If a store exceeds ~5 actions, split into slices or move server data to TanStack Query.

## 6. Forms

- `react-hook-form` + `@hookform/resolvers/zodResolver`; schema defines the single source of truth:

```ts
const schema = z.object({
  name: z.string().min(1, 'Name is required'),
  frequencyDays: z.coerce.number().int().positive(),
});
type CreateAssetForm = z.infer<typeof schema>;
```

- MUI inputs integrate via `Controller`.

## 7. API layer

- All HTTP goes through `shared/api/client.ts` — never `axios.get` bare, never `fetch`.
- Feature API modules return typed promises:

```ts
// features/inspections/api/inspectionApi.ts
export const inspectionApi = {
  list: (filters: InspectionFilters) =>
    api.get<InspectionResponse[]>('/inspections', { params: filters }).then((r) => r.data),
};
```

- Refresh/401 handling is already implemented in the client — do not duplicate it.

## 8. Imports

Order (blank line between groups):
1. External packages (`react`, `@mui/*`, `@tanstack/*`, …)
2. `@/` alias imports
3. Relative imports (same feature only)
4. `import type` last

- Cross-feature imports always use `@/features/…` — **never `../` across feature boundaries**.
- `@/` maps to `src/` (tsconfig paths + Vite).

## 9. TypeScript strictness

- `strict`, `noUncheckedIndexedAccess`, `exactOptionalPropertyTypes` are on — do not weaken them.
- No `any`. Use `unknown` + narrowing. Only exception: third-party types you can't control (comment why).
- Prefer inference for local values; annotate function return types for exported functions.

## 10. MUI

- Spacing/layout via theme tokens (`sx={{ p: 2, gap: 1 }}`) — no hardcoded pixel margins.
- Colors from `theme.palette` — never raw hex in components (brand hex lives only in `app/theme/theme.ts`).
- Reusable UI primitives (buttons, tables, chips, dialogs) belong in `shared/ui/`; a component used by 2+ features must move there.
