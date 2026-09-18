---
title: "AI Agent Rules"
weight: 10
aliases:
  - /coding-conventions/ai-agent-rules/
---

# AI Agent Rules

These rules apply to AI coding agents and are also a useful review checklist for humans. Repository-specific instructions take precedence when they are more restrictive.

## 1. Before changing files

- **AI-01 MUST** identify the target repository. `backend`, `frontend`, `mobile`, and `docs` are independent Git repositories; the workspace root is not a repository.
- **AI-02 MUST** read the nearest `AGENTS.md` or equivalent repository guidance before editing.
- **AI-03 MUST** run `git status --short` in the target repository and preserve unrelated or pre-existing changes.
- **AI-04 MUST** inspect the current implementation, adjacent tests, and API contract. Do not implement from documentation alone when executable code exists.
- **AI-05 SHOULD** state any assumption that changes behavior, data, authorization, or public API. Ask for input only when the choice cannot be safely inferred.

## 2. Scope and design

- **AI-06 MUST** implement the smallest complete vertical slice required by the task.
- **AI-07 MUST NOT** create generic base controllers, services, repositories, response wrappers, or utility layers without at least one concrete current use case.
- **AI-08 MUST NOT** add an interface for a single class unless it represents a real external boundary, supports multiple implementations, or materially improves testing.
- **AI-09 MUST NOT** add a new service, cache, queue, event bus, background job, or dependency only for a hypothetical future requirement.
- **AI-10 SHOULD** keep code inside the owning feature. Move code to `shared` or `core` only when it is stable, feature-neutral, and used by multiple features.
- **AI-11 SHOULD** follow nearby naming and structure. Create only folders that contain real code; empty architecture layers are not required.
- **AI-12 MAY** refactor code directly affected by the change when that makes the result safer or clearer. Unrelated cleanup belongs in a separate task.

## 3. Implementation quality

- **AI-13 MUST** keep public contracts strongly typed and validate untrusted input at the system boundary.
- **AI-14 MUST** preserve authorization scope: role checks do not replace organization, ownership, assignment, or separation-of-duties checks.
- **AI-15 MUST NOT** log or commit passwords, access tokens, refresh tokens, secrets, recovery codes, or private keys.
- **AI-16 SHOULD** prefer explicit names and short functions over explanatory comments. Comments explain *why*, not what the code already says.
- **AI-17 SHOULD** use early returns to avoid deep nesting and replace meaningful repeated literals with named constants.
- **AI-18 SHOULD** reuse an existing project dependency or utility before adding another one.
- **AI-19 MUST NOT** edit generated files. Change the source annotation/schema and regenerate them with the project command.

## 4. Tests and verification

- **AI-20 MUST** add or update tests when behavior changes or a defect is fixed.
- **AI-21 SHOULD** test observable behavior and important failure paths instead of implementation details.
- **AI-22 MUST** run the narrowest useful check during development, then the repository's required verification before handoff when practical.
- **AI-23 MUST** report exactly which checks ran and whether they passed. Never claim a check that was not executed.
- **AI-24 MUST** inspect the final diff for accidental generated files, secrets, debug output, unrelated formatting, and API drift.

Required handoff checks:

| Repository | Commands |
| --- | --- |
| Backend | `.\mvnw.cmd verify` on Windows, or `./mvnw verify` on Unix |
| Frontend | `npm run lint` and `npm run build` |
| Mobile | `dart format --set-exit-if-changed .`, `flutter analyze`, and `flutter test` |
| Docs | `git diff --check`, link/path review, and Hugo build when Hugo is available |

## 5. Data and repository safety

- **AI-25 MUST NOT** create or modify a Flyway migration unless the task explicitly assigns database migration work to the team leader.
- **AI-26 MUST** use a new forward migration for an already-shared database change; never rewrite an applied migration.
- **AI-27 MUST NOT** delete, reset, overwrite, or stage unrelated user work.
- **AI-28 MUST** stage explicit files and review the staged diff before committing.
- **AI-29 MUST NOT** push, open a pull request, merge, deploy, or send external messages unless the user explicitly requests that action.
- **AI-30 SHOULD** keep one logical concern per commit and use Conventional Commits.

## 6. Definition of done

A change is done only when:

- the acceptance criteria are implemented;
- input, error, and authorization paths are handled;
- relevant tests exist and verification results are reported;
- public API and documentation are updated when they changed;
- the final diff contains no unrelated work or secrets;
- the handoff lists changed files, verification, and any remaining risk.
