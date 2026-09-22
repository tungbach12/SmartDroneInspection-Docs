---
title: "Git and Pull Request Workflow"
weight: 20
aliases:
  - /coding-conventions/git-and-pull-requests/
---

# Git and Pull Request Workflow

This page is the reference for creating a professional, reviewable pull request. It applies to each independent repository in the workspace.

The workspace contains independent Git repositories. Run Git commands from `backend`, `frontend`, `mobile`, or `docs`; never assume the workspace root represents all changes.

## 1. Before starting

- **GIT-01 MUST** identify the target repository and target branch.
- **GIT-02 MUST** read the nearest `AGENTS.md`, inspect the current implementation, and run `git status --short`.
- **GIT-03 MUST** fetch the target branch before creating a feature branch.
- **GIT-04 SHOULD** use `<type>/<scope>-<short-description>`, for example `feat/auth-role-rename` or `fix/reports-release-guard`.
- **GIT-05 MUST NOT** mix unrelated repositories or unrelated concerns into one pull request.
- **GIT-06 MUST** preserve unrelated user changes already present in the worktree.

For a change spanning repositories, create one focused PR per repository and cross-link them in each PR's `Related PRs` section. State the merge order when one PR depends on another.

## 2. Commits

Use Conventional Commits:

```text
<type>(<scope>): <short imperative summary>
```

Common types are `feat`, `fix`, `docs`, `refactor`, `test`, `chore`, and `ci`.

```text
feat(auth): rename roles to final codes
fix(reports): enforce reviewer separation
docs(development): define pull request standard
```

- **GIT-07 MUST** stage explicit intended paths and inspect `git diff --staged` before committing.
- **GIT-08 MUST NOT** commit secrets, local environment files, build output, IDE state, or unrelated generated files.
- **GIT-09 SHOULD** keep one logical concern per commit. Explain the reason in the body when the summary is not enough.
- **GIT-10 MUST** avoid commit messages such as `update`, `fix stuff`, or `changes`.

## 3. Pull request title

The PR title should follow the same Conventional Commit format as the main commit:

```text
<type>(<scope>): <what changed>
```

The title describes the outcome, not the implementation diary. Keep it short enough to scan and specific enough to distinguish from nearby work.

Good:

```text
feat(auth): rename roles to final codes
fix(inspections): prevent unassigned evidence access
docs(conventions): add AI agent PR rules
```

Avoid:

```text
Update files
Changes
Final version
```

## 4. Required PR body

A professional PR answers these questions without requiring the reviewer to reconstruct the story from the diff:

1. **What problem or requirement does this solve?**
2. **What changed and where?**
3. **What is intentionally out of scope?**
4. **How was it verified?**
5. **Does it change API, database, security, configuration, or deployment behavior?**
6. **What risk, migration, rollout step, or follow-up remains?**

Every PR body MUST include the following sections:

- **Summary** - two to five sentences describing the user/business outcome.
- **Changes** - concrete files, modules, endpoints, screens, migrations, or behavior changed.
- **Scope boundaries** - relevant non-goals; mention intentionally untouched areas.
- **Impact** - API, database, security, compatibility, configuration, observability, and deployment impact. Use `None` explicitly when a category does not apply.
- **Verification** - exact commands run and their result. Separate passed, failed, skipped, and blocked checks.
- **Risk and rollout** - migration order, feature flags, backward compatibility, rollback, or `None`.
- **Related work** - issue, requirement, design note, or related PR links. Use `None` only when genuinely absent.

Use screenshots, request/response examples, or short recordings for UI changes. Use a migration note or contract example for API/database changes.

## 5. Copy/paste PR template

Copy this template into the GitHub PR description and remove sections that truly do not apply only after writing `None` with a reason.

```markdown
## Summary

<!-- What user, business, or engineering problem does this solve? Keep this outcome-focused. -->

## Changes

-
-
-

## Scope boundaries

- In scope:
- Intentionally out of scope:

## Impact

| Area | Impact |
| --- | --- |
| API / contract | None, or describe changed endpoints and compatibility. |
| Database / migration | None, or describe migration, data backfill, and order. |
| Security / authorization | None, or describe changed roles, scopes, validation, or secrets. |
| Frontend / mobile | None, or describe affected screens and clients. |
| Configuration / deployment | None, or describe new variables, flags, or rollout steps. |
| Observability | None, or describe logs, metrics, traces, and audit events. |

## Verification

### Passed

- `command` - result

### Failed or blocked

- `command` - reason and follow-up

### Manual checks

- [ ] Relevant happy path checked.
- [ ] Relevant failure and authorization paths checked.
- [ ] UI screenshot/recording attached when applicable.

## Risk and rollout

- Risk:
- Rollout or migration order:
- Rollback plan:
- Follow-up:

## Related PRs / issues

- Related PRs:
- Issues or requirements:

## Reviewer notes

<!-- Point reviewers to non-obvious decisions, compatibility constraints, or files that deserve extra attention. -->
## Checklist

- [ ] Acceptance criteria are satisfied.
- [ ] The diff contains only this logical change.
- [ ] No secrets, tokens, debug output, or unrelated generated files are included.
- [ ] Tests and required checks are recorded accurately.
- [ ] API, database, security, and documentation changes are synchronized.
- [ ] Migration and deployment order are documented when applicable.
- [ ] Related PRs are linked and their merge order is clear.
```

## 6. Review and merge rules

- **GIT-11 MUST** describe the problem, solution, verification, impact, and remaining risk in the PR body.
- **GIT-12 MUST** update documentation and API contracts when behavior visible to another repository changes.
- **GIT-13 MUST** pass the repository's required formatting, build, tests, coverage, and architecture checks before merge.
- **GIT-14 SHOULD** keep a PR small enough to review as one coherent change. Split unrelated cleanup into another PR.
- **GIT-15 MUST** obtain at least one review approval unless the repository owner explicitly allows a self-merge.
- **GIT-16 SHOULD** use squash merge so the target branch receives one coherent Conventional Commit.
- **GIT-17 MUST** delete the remote feature branch after merge when it is no longer needed.
- **GIT-18 MUST NOT** push, open, close, merge, or delete a branch without explicit user authorization.

Before merging, the author and reviewer should be able to answer “yes” to all of these:

- Is the acceptance criterion clear and satisfied?
- Is the smallest safe solution implemented?
- Are authorization, validation, error, and compatibility paths covered?
- Are verification results reproducible and honestly reported?
- Can the change be rolled out and rolled back without guessing?
- Does the PR explain what reviewers should focus on?

## 7. Repository verification commands

| Repository | Required checks |
| --- | --- |
| Backend | `.\mvnw.cmd verify` on Windows, or `./mvnw verify` on Unix |
| Frontend | `npm run lint` and `npm run build` |
| Mobile | `dart format --set-exit-if-changed .`, `flutter analyze`, and `flutter test` |
| Docs | `git diff --check`, local link review, and Hugo build when Hugo is available |

If a check cannot run, record the exact command, the blocker, and the next action in `Failed or blocked`; never label a skipped check as passed.
