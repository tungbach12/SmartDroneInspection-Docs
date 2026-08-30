# Coding Conventions — Mobile (Flutter / Dart)

> Enforced by `flutter_lints` + `dart analyze` in CI. App scope: Inspector + Maintenance Engineer flows.

## 1. Naming

| Element | Rule | Example |
|---------|------|---------|
| Class | PascalCase | `InspectionRepository` |
| File | snake_case | `inspection_repository.dart` |
| Variable / method / constant | lowerCamelCase | `maxRetries`, `_controller` |
| Private member | `_` prefix | `_client` |
| Riverpod provider | class name, first letter lowercased | `class InspectionRepository` → `inspectionRepositoryProvider` |
| DTO model | PascalCase, `@freezed` | `InspectionSummary` |

## 2. Folder layout (feature-first)

```
lib/
├─ core/
│  ├─ router/                 # GoRouter config, redirects for auth/roles
│  ├─ di/                     # top-level providers
│  ├─ theme/  env/  token/    # flutter_secure_storage wrapper
├─ shared/
│  ├─ widgets/  utils/
└─ features/
   ├─ auth/
   │  ├─ data/                # dio client, repository, DTOs
   │  ├─ domain/              # Freezed models
   │  └─ presentation/        # screens, widgets, Riverpod providers
   ├─ inspections/  reports/  maintenance/
```

- Provider colocation: the provider lives in the **same file** as the class it exposes. No one-global `providers.dart`.
- Stateful providers use `Notifier` / `AsyncNotifier` (Riverpod 3). State classes live under `presentation/`.

## 3. Riverpod rules

```dart
final inspectionRepositoryProvider = Provider<InspectionRepository>((ref) {
  final api = ref.watch(dioProvider);
  return InspectionRepository(api);
});
```

- Widgets watch providers; they never construct repositories directly.
- Side effects (navigation, toasts) go through `ref.listen` — never inside `build`.
- Reading providers in event handlers uses `ref.read` (after ensuring the provider is initialized).

## 4. Models — Freezed + json_serializable

- One model per file, under `features/<feature>/domain/models/`.

```dart
@freezed
class Inspection with _$Inspection {
  const factory Inspection({
    required String id,
    required String assetId,
    @JsonKey(name: 'status') required String status,
  }) = _Inspection;

  factory Inspection.fromJson(Map<String, dynamic> json) => _$InspectionFromJson(json);
}
```

- API contract naming: `@JsonKey(name: '...')` mirrors the backend `XxxResponse` fields (snake_case on the wire).
- After changing models, regenerate: `dart run build_runner build --delete-conflicting-outputs`.
- Commit generated `.freezed.dart` / `.g.dart` files.

## 5. Networking (Dio)

- Single shared `dioProvider` in `core/di/` with the JWT interceptor (attach token, single-flight 401 refresh, force-logout on refresh failure).
- Feature repositories expose only typed methods; they never leak `Response<dynamic>` upward.
- Image upload uses presigned MinIO URLs (PUT), obtained from the backend first.

## 6. State, offline, security

- Tokens: `flutter_secure_storage` only — never `SharedPreferences`.
- Evidence photo flow: `image_picker` → optional local draft queue (`drift`/`isar`) → upload when online (`connectivity_plus` to gate).
- No secrets in code; API base URL from `--dart-define` / env, never hardcoded.

## 7. Formatting & lints

- `flutter_lints` (default for `flutter create`) stays enabled; analyzer warnings fail CI.
- Run `dart format` before every commit — formatting is not a review topic.
