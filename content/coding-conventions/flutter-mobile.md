---
title: "Mobile Flutter Conventions"
weight: 3
---

# Mobile Flutter Conventions

## 1. Clean Architecture Structure
```text
lib/
├── core/                           # Network (Dio), Token Storage, Theme, Router (GoRouter)
└── features/
    └── <feature_name>/
        ├── data/                   # Data sources, Models, Repositories implementation
        ├── domain/                 # Entities, Repository interfaces, Use cases
        └── presentation/           # Riverpod controllers, Widgets, Screens
```

## 2. State Management & DI
* **Riverpod 3** is used for reactive state management and dependency injection.
* Prefer `AsyncNotifier` / `Notifier` for complex stateful screens.

## 3. Security & Storage
* Auth tokens (JWT & Refresh Token) are stored securely using `flutter_secure_storage`.
* Dio HTTP client uses an Auth Interceptor with automatic 401 token refresh queue.
