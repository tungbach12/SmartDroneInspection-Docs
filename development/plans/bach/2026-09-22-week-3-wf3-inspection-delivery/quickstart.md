# FE-04 — Week 3 WF3 Validation Guide

This guide is for parent `SCRUM-56` and its tasks `SCRUM-63`, `SCRUM-83`, and `SCRUM-84` after
implementation. It is not a claim that the current runtime already supports the endpoints.

## Preconditions

- PostgreSQL test infrastructure and the authentication/migration baseline are available through the
  FE-01 W3 foundation gate (`SCRUM-58/T001`). MinIO is a separate FE-04/WF3 evidence dependency
  owned by `T025/SCRUM-85`, not part of the current FE-01 gate or this start/checklist slice.
- The test fixture creates two organizations, an active Inspector in each, one accepted assignment,
  one active checklist template, and at least one required item.
- No default credentials or real secrets are stored in fixtures.

## Focused backend checks

```powershell
cd backend
.\mvnw.cmd -Dtest=InspectionFixtureTest,InspectionWorkflowTest test
```

Verify:

1. The accepted assignment fixture is deterministic and uses real domain constructors.
2. Start is idempotent and creates one inspection.
3. A different Inspector and an inactive Inspector are denied.
4. Required and foreign-template checklist responses are rejected.
5. A valid response is attributed to the authenticated Inspector.

## Mobile check

```powershell
cd mobile
dart format --set-exit-if-changed .
flutter analyze
flutter test
```

The assigned list calls the contract in
[w3-inspection-start-and-checklist.md](contracts/w3-inspection-start-and-checklist.md), renders
loading/empty/error states, and does not implement authorization locally.

## Week 3 exit evidence

Attach the focused test result, mobile verification result, API contract review, and a short
  screen capture or screenshot to the three Jira tasks. FE-05 AI verification and FE-06
  report/review work are not required to close this sprint slice.

## Recorded verification (2026-09-22)

- `backend/.\mvnw.cmd verify`: passed; 100 tests, zero failures/errors, coverage gate met, and
  Modulith checks passed.
- `backend/.\mvnw.cmd -Dtest=WorkflowBaselineTest test`: passed; Flyway V1-V9 and all five
  generated role logins were verified. MinIO Compose liveness was checked separately for the
  future FE-04 evidence task and is not counted as FE-01 coverage.
- Mobile `dart format --set-exit-if-changed lib/features/inspections test`, `flutter analyze`,
  and `flutter test`: passed.
