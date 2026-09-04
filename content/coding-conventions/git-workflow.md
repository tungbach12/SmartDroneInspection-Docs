---
title: "Git Workflow & PR Guidelines"
weight: 4
---

# Git Workflow & PR Guidelines

## 1. Branching Strategy
* **`main`**: Protected branch. Deploys to staging/production. Direct commits forbidden.
* **Feature branches**: Created from `main` with prefix `feat/<module>-<description>` or `fix/<description>`.
  * Examples: `feat/assets-paged-spec`, `fix/auth-token-expiry`.

## 2. Commit Message Standards (Conventional Commits)
All commit messages must follow the Conventional Commits specification:
```text
<type>(<scope>): <short summary>

[optional body]
```
* **Types**: `feat`, `fix`, `docs`, `refactor`, `test`, `chore`, `ci`.
* **Scopes**: `assets`, `missions`, `reports`, `tickets`, `auth`, `ai`, `infra`.
* Examples:
  * `feat(auth): implement refresh token single-use rotation`
  * `fix(assets): resolve null coordinates serialization in API response`

## 3. Pull Request (PR) Policy
* Every PR requires at least 1 review approval (or self-merge by repository owner).
* All automated CI checks (build, unit tests, code formatting) must pass.
* Merge method: **Squash and merge** only, to keep a clean commit history on `main`.
