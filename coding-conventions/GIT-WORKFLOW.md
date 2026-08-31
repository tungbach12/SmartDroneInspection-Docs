# Coding Conventions — Git Workflow (4-person team)

> One rule above all: **`main` is always shippable.** Nothing merges to code repositories (`backend`, `frontend`, `mobile`) without CI green.

## 1. Branches

```
main                      # protected for code repos — always deployable
feature/<slug>            # new functionality
bugfix/<slug>             # non-blocking fixes
hotfix/<slug>             # urgent fix off main, merged back immediately
chore/<slug>              # tooling, deps, docs
```

- Short-lived: branch off `main`, merge within ~2–3 days. Long-lived branches = merge hell.
- Slug: lowercase, kebab-case, descriptive — `feature/inspection-request-approval`, not `feature/update`.
- **Code repositories (`backend/`, `frontend/`, `mobile/`)**: Never commit directly to `main`. All changes go through PR + review.
- **Documentation repository (`docs/`)**: Direct commits and pushes to `main` are permitted without requiring PR review to facilitate rapid documentation sync.

## 2. Commits — Conventional Commits

Format: `<type>(<scope>): <subject>` — imperative mood, lowercase, ≤ 72 chars.

```
feat(assets): add asset detail drawer
fix(inspections): return 404 for unknown inspection id
chore(deps): update MUI to 9.4.0
docs(architecture): add backend conventions
test(reports): cover defect severity validation
```

Types: `feat` · `fix` · `docs` · `chore` · `refactor` · `test` · `perf`.

- Scope = module folder (`assets`, `inspections`, `reports`, `ai`, `api`, `mobile`, `fe`, …).
- One logical change per commit — "work in progress" stays local.

## 3. Pull Requests

| Rule | Value |
|------|-------|
| Size | < ~400 changed lines (split otherwise) |
| Scope | One feature per PR |
| Reviews | **Required: 0 approvals** (ruleset `main-protection` enforces PR + linear history + delete-block + squash/merge only). Reviewers are encouraged but not blocking. The repo owner can self-merge when alone or when an external reviewer is not yet available. Shared layers (`Application/Common`, API contracts, DB migrations) still request a second pair of eyes via a normal review request — the rule does not block. |
| CI | All checks green before merge |
| Linkage | References the issue/task in description |
| Merge | Squash-merge; delete branch after |
| Latency | Open < 48h — rotate reviewers so nobody blocks |

PR description template (paste into every PR):

```markdown
## What
<1–3 sentences>

## Why
<link/issue + motivation>

## How tested
- [ ] unit tests
- [ ] manual verification (steps)
```

## 4. Ownership map (who reviews what)

| Member | Owns | Reviews |
|--------|------|---------|
| Hiếu (Leader) | Users, foundation, Dashboard, migrations | DB migrations, `Application/Common`, API contracts |
| Quốc | Assets, Planning & Requests | Assets/Inspections FE + BE |
| Như | Missions, Reports, Defects, Tickets | integration & external clients |
| Bách | Flutter app, AI services, MinIO | mobile, AI integration |

## 5. Do / Don't

- ✅ Pull `main` into your branch daily (or rebase if no one else consumes it).
- ✅ Small commits while working; tidy history matters less than a clean PR.
- ❌ Never `--force` push to shared branches (`--force-with-lease` to your own feature branch only, when truly needed).
- ❌ Never merge red CI. Fix forward.
- ❌ No secrets, connection strings, or `.env` values in commits — secrets live in env vars / user-secrets.
