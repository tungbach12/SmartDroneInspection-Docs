# WF3 Completion Validation Guide

Use this guide to repeat the WF3 regression. The automated checks below were
executed on 2026-09-24; their outcomes are recorded below and in Report 5. The
interactive walkthrough and live external YOLO call were not executed, so this
record does not claim validation against a deployed AI service.

## Preconditions

- Docker Desktop/daemon is running.
- Backend PostgreSQL and MinIO services start from backend/docker-compose.yml. Supply local credentials through the documented local environment mechanism; never copy local defaults or real secrets into source control.
- A configured YOLO endpoint is available for live inference checks. Unit/integration tests use a deterministic stub so the suite does not require external AI credentials.
- Test fixtures provide two active Inspectors, at least two organizations, a confirmed service order, an accepted assignment, and a checklist with a required response.

## Automated checks

From PowerShell at the workspace root:

```powershell
Set-Location backend
docker compose up -d
.\mvnw.cmd -Dtest=InspectionFixtureTest,InspectionWorkflowTest test
.\mvnw.cmd verify

Set-Location ../frontend
npm.cmd test
npm.cmd run lint
npm.cmd run build

Set-Location ../mobile
flutter pub get
dart format --set-exit-if-changed .
flutter analyze
flutter test

Set-Location ../docs
git diff --check
```

Record exact commands and outcomes; do not mark skipped live-AI checks as passed. Run the project Hugo build only when Hugo and the configured theme are available.

## Execution record — 2026-09-24

| Repository | Command/check | Result |
| --- | --- | --- |
| Backend | `.\mvnw.cmd verify` from `backend/` | **Passed** — 134 tests, 0 failures/errors/skips; Spotless, JaCoCo coverage gate, and Spring Modulith boundary verification passed. Testcontainers exercised PostgreSQL and MinIO. |
| Frontend | `npm.cmd test` from `frontend/` | **Passed** — 9 files, 52 tests. |
| Frontend | `npm.cmd run lint` from `frontend/` | **Passed** — exit 0; existing fast-refresh and irregular-whitespace warnings remain. |
| Frontend | `npm.cmd run build` from `frontend/` | **Passed** — TypeScript and Vite production build completed. |
| Mobile | `dart format --set-exit-if-changed .` from `mobile/` | **Passed** — 45 files checked, 0 changed. |
| Mobile | `flutter analyze` from `mobile/` | **Passed** — no issues found. |
| Mobile | `flutter test` from `mobile/` | **Passed** — all 8 tests passed. |
| Docs | `git diff --check` and local Markdown link review | **Passed** — no whitespace errors or broken local links across 23 changed/untracked Markdown files. |
| Docs | Hugo build | **Skipped** — Hugo is not installed in this environment. |
| External integration | Live YOLO service and interactive browser/device walkthrough | **Not run** — deterministic local inference stub and automated web/mobile tests were used. |

The stable Report 5 functional cases `WF3-001`–`WF3-004` are recorded as
Round 1 Passed; WF1/WF2 and WF4 cases remain Pending. No failed functional
case is hidden or converted to Passed.

## End-to-end acceptance walkthrough

1. Seed an accepted WF2 assignment and open it as the assigned Inspector. Confirm one inspection starts and a repeated start returns the same inspection. Verify a different Inspector and another organization are denied.
2. Complete a valid required checklist response. Upload a valid supported image and verify its checksum/metadata and object exist; upload the same content again and confirm only one evidence record exists. Read the image through the authorized API as the assignee, then confirm an unrelated Inspector/organization cannot read it.
3. Try corrupt and unsupported files and confirm stable validation errors. Interrupt/retry an upload and confirm it neither duplicates metadata nor exposes a partial object. Remove GPS metadata and confirm valid evidence remains accepted with GPS recorded as absent.
4. With the AI stub enabled, verify the candidate contains model/version/label/confidence/bounding box. Exercise confirm, modify, and reject. Verify a rejected or pending candidate is absent from official findings and report content; create a manual finding.
5. Make the AI stub fail. Verify stored evidence remains readable and manual finding remains available; no failed inference is promoted to an official defect.
6. Generate report version 1 and submit it for review. Confirm self-review is denied; a distinct assigned Inspector can request changes or technically approve. On changes, create version 2 and preserve version 1 and its decision.
7. Confirm the Client cannot read internal drafts/comments. After technical approval, release the report as Service Manager; verify the Client can read only the released version and its linked evidence, then accept/request revision without editing findings.
8. On acceptance, verify the accepted version becomes immutable, history is retained, and one accepted-report/billing handoff is emitted. Confirm the separate billing consumer can use that handoff without the WF3 module importing its internals.
9. Exercise web and mobile loading, empty, validation, retry, permission-denied, and success states. Finish with the WF3 regression and record evidence in Report 5.

## Report 5 closeout

- Preserve the workbook's fixed sheets and stable WFx identifiers: WF3-001/WF3-002 map to FE-04, WF3-003 to FE-05, and WF3-004 to FE-06.
- Add or adjust only cases needed to cover the Jira acceptance criteria and negative scope paths.
- Update the case index, detailed Feature 2 procedure/results, statistics, cover, and record of changes. A case is Passed only after its documented procedure actually ran.
- Update Report 3 and its record of changes only if implementation changes a requirement; update the current backend flow guide and client documentation when their contracts change.
