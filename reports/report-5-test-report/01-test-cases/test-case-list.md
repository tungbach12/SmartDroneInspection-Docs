# Test Cases sheet source

This table mirrors the `Test Cases` sheet. The workbook columns and order are
fixed: `No`, `Function Name`, `Sheet Name`, `Description`, `Pre-Condition`.

## Project and environment notes

| Field | Value |
| --- | --- |
| Project Name | SmartDroneInspection |
| Project Code | SEP490 — *confirm with project owner* |
| Test environment | Local/integration environment with PostgreSQL, Redis, MinIO, backend API, web client, and mobile client configured according to the active test run. |
| Baseline | Current WF1–WF4 main-flow scope; no autonomous drone flight control. |

The FE-01 supporting verification is intentionally outside the workbook case
index and functional-case statistics; its auth-flow and role-policy evidence is
recorded in `03-features/feature-1.md`.

## Case index

The `Sheet Name` column refers to the fixed workbook sheet, not to an SRS
feature code. `FE-xx` identifies the product feature and `WFx-yyy` identifies
the business-flow test case. For example, `WF4-001` is correctly placed on
the `Feature 2` sheet because the template groups WF3 and WF4 there; it maps
to FE-07, not FE-02.

The FE-01 role-aware portal/navigation policy check, browser authentication
flow checks, and cross-cutting API response-envelope contract checks are
recorded separately in `03-features/feature-1.md`. These supporting checks
verify SRS access and API contracts; they are not additional WFx functional
cases or workbook rows.

| No | Function Name | Sheet Name | Description | Pre-Condition |
| ---: | --- | --- | --- | --- |
| 1 | `[WF1-001]` FE-02 — WF1 asset catalog and scheduling | Feature 1 | Admin maintains an inspection category/checklist and the system exposes it for planning. | Admin is authenticated; the category/checklist is valid and active. |
| 2 | `[WF1-002]` FE-02 — WF1 asset catalog and scheduling | Feature 1 | Client creates an asset for the client organization and can view its own asset. | Client is active and belongs to an organization. |
| 3 | `[WF1-003]` FE-02 — WF1 asset catalog and scheduling | Feature 1 | A client cannot read or modify an asset owned by another organization. | Two organizations exist; the client is authenticated in organization A. |
| 4 | `[WF1-004]` FE-02 — WF1 asset catalog and scheduling | Feature 1 | An active periodic schedule creates one due request for the correct asset and cycle. | Active asset and schedule exist; the due cycle is reached. |
| 5 | `[WF2-001]` FE-03 — WF2 request and quotation | Feature 1 | Client creates an ad-hoc inspection request with scope, location, and preferred timing. | Client owns the organization and required asset exists. |
| 6 | `[WF2-002]` FE-03 — WF2 request and quotation | Feature 1 | Service Manager prepares a versioned quotation and sends it to the client. | A valid request is visible to the Service Manager; pricing data is complete. |
| 7 | `[WF2-003]` FE-03 — WF2 order and assignment | Feature 1 | Client approves the quotation and the system records the confirmed order and billing milestone. | Quotation is in an approvable state; client has organization scope. |
| 8 | `[WF2-004]` FE-03 — WF2 order and assignment | Feature 1 | Service Manager assigns an Inspector; an unassigned or conflicting Inspector cannot access the task. | Confirmed order exists; candidate Inspector is active. |
| 9 | `[WF3-001]` FE-04 — WF3 inspection execution | Feature 2 | Assigned Inspector starts the inspection and completes the required checklist. | Inspector is assigned to the order; checklist is published. |
| 10 | `[WF3-002]` FE-04 — WF3 evidence and traceability | Feature 2 | Inspector uploads authorized evidence with checksum, retry safety, and traceable source metadata. | Inspection is started; evidence type and file constraints are valid. |
| 11 | `[WF3-003]` FE-05 — WF3 AI candidate review | Feature 2 | Inspector confirms, modifies, rejects AI candidates, or adds a manual finding; only official findings enter report content. | Eligible evidence exists; AI integration is available or manual fallback is enabled. |
| 12 | `[WF3-004]` FE-06 — WF3 report review and release | Feature 2 | Report author cannot peer-review their own report; a different authorized reviewer can approve it. | Draft report exists; author and reviewer are distinct users. |
| 13 | `[WF4-001]` FE-07 — WF4 maintenance ticket | Feature 2 | Client creates a maintenance ticket from an accepted finding and sees only its organization data. | A released report contains an accepted finding. |
| 14 | `[WF4-002]` FE-07 — WF4 assessment and execution | Feature 2 | Maintenance Engineer views and updates only assigned assessment/execution work. | Ticket is assigned to the engineer; required service scope exists. |
| 15 | `[WF4-003]` FE-07 — WF4 rework and billing | Feature 2 | Client approval, rework/reinspection, and post-service invoice/payment status follow the configured milestone. | Maintenance work is complete or requires rework; invoice status is available. |
