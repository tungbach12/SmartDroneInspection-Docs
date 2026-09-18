---
title: "Git and Pull Request Workflow"
weight: 20
aliases:
  - /coding-conventions/git-and-pull-requests/
---

# Git and Pull Request Workflow

The workspace contains independent Git repositories. Run Git commands from `backend`, `frontend`, `mobile`, or `docs`; never assume the workspace root represents all changes.

## Branches

- **GIT-01 MUST** branch from the current target branch after fetching its latest state.
- **GIT-02 SHOULD** use `<type>/<scope>-<short-description>`, for example `feat/auth-login` or `fix/reports-release-guard`.
- **GIT-03 MUST NOT** mix unrelated repositories or unrelated concerns into one pull request.
- **GIT-04 MUST** preserve user changes already present in the worktree.

## Commits

Use Conventional Commits:

```text
<type>(<scope>): <short imperative summary>
```

Allowed common types are `feat`, `fix`, `docs`, `refactor`, `test`, `chore`, and `ci`.

Examples:

```text
feat(auth): add session revocation
fix(reports): enforce reviewer separation
docs(conventions): add AI agent rules
```

- **GIT-05 MUST** stage explicit intended paths and review `git diff --staged` before committing.
- **GIT-06 MUST NOT** commit secrets, local environment files, build output, IDE state, or unrelated generated files.
- **GIT-07 SHOULD** keep a commit focused on one logical change and explain the reason in the body when the summary is insufficient.

## Pull requests

- **GIT-08 MUST** describe the problem, the solution, verification performed, and any known risk or follow-up.
- **GIT-09 MUST** update documentation and API contracts when behavior visible to another repository changes.
- **GIT-10 MUST** pass the repository's required formatting, build, tests, coverage, and architecture checks.
- **GIT-11 SHOULD** keep pull requests small enough to review as one coherent change.
- **GIT-12 MUST** obtain at least one review approval unless the repository owner explicitly allows a self-merge.
- **GIT-13 SHOULD** use squash merge so the target branch receives one coherent Conventional Commit.
- **GIT-14 MUST NOT** push, open, close, or merge a pull request without explicit user authorization.

## Pull request checklist

- [ ] Acceptance criteria are satisfied.
- [ ] Authorization and failure paths were considered.
- [ ] Tests were added or updated where behavior changed.
- [ ] Required checks pass and their results are recorded.
- [ ] API/docs are synchronized across affected repositories.
- [ ] The diff contains no unrelated work, debug code, or secrets.
