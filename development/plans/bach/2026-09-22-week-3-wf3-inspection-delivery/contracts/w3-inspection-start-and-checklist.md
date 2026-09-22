# Contract: FE-04 — Week 3 Inspection Start and Checklist

**Status**: Implemented and verified for `T023` and `T024`; the focused and full backend suites,
plus the mobile inspection test, pass in the Docker-backed environment.

**Jira parent**: `SCRUM-56 — FE-04 | WF3 — Inspection Execution & Evidence Management`
**Related parent features**: FE-02/WF1 supplies the checklist catalog; FE-05 handles later AI
candidate verification; FE-06 handles later report approval.

## Endpoints

### List accepted assignments

`GET /api/v1/inspections/assignments?status=ACCEPTED`

The server scopes the result to the authenticated active Inspector. The response contains
`assignmentId`, `serviceOrderId`, `assetId`, `deadline`, `status`, and nullable `inspectionId`.

### Start or resume

`POST /api/v1/inspections/start`

```json
{ "assignmentId": "uuid" }
```

The server derives all other IDs. A first call creates `READY_FOR_INSPECTION → IN_PROGRESS`; a
retry returns the existing inspection. A completed/released inspection cannot be reopened.

### Save checklist response

`PUT /api/v1/inspections/{inspectionId}/checklist-responses/{checklistItemId}`

```json
{
  "responseValue": {"value": "PASS"},
  "notes": "No visible damage"
}
```

The item must belong to the inspection's checklist template. The response records the authenticated
Inspector and server timestamp.

## Authorization and errors

- `401 AUTHENTICATION_REQUIRED`: missing/invalid token.
- `403 INSPECTION_SCOPE_DENIED`: not the accepted assignee or inactive Inspector.
- `404 INSPECTION_NOT_FOUND`: scoped resource is not visible.
- `409 INSPECTION_STATE_CONFLICT`: invalid current state or duplicate state change.
- `422 CHECKLIST_RESPONSE_INVALID`: invalid value, unknown item, or missing required response.

Do not disclose another organization, assignee, report draft, token, or stack trace.

## Acceptance tests

- Accepted assignee starts twice and receives one inspection ID.
- Non-assignee and inactive Inspector cannot list, start, or update.
- Blank required response and foreign-template item are rejected.
- Valid response stores the authenticated user and timestamp.
- Mobile renders only the scoped list and server error state.
