# FE-02: Asset Registry and Inspection Schedule

## Scope baseline

Clients create and manage their organization’s assets, documents, inspection history and recurring schedules. Admins maintain categories and checklist templates. WF1 generates periodic requests with an Asset + Schedule + Due Cycle idempotency key.

## Current acceptance cases

Workbook function groups are retained in the case index. These four cases map to FE-02 and WF1.

| Test Case ID | Test Case Description | Test Case Procedure | Expected Results | Pre-conditions | Round 1 | Test date | Tester | Round 2 | Test date | Tester | Round 3 | Test date | Tester | Note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| WF1-001 | Admin publishes an inspection category and checklist. | Sign in as Admin; create or update the category and checklist; activate it; read it from planning. | Only a valid active category/checklist is available for planning and its version is retained. | Admin is active; checklist validation passes. | Pending |  |  | Pending |  |  | Pending |  |  |  |
| WF1-002 | Client creates an asset for its own organization. | Sign in as Client; submit asset identity and location; save; open the asset list. | Asset is created once, linked to the client organization, and visible to that organization. | Client is active and has organization scope. | Pending |  |  | Pending |  |  | Pending |  |  |  |
| WF1-003 | Client cannot access another organization's asset. | Sign in as a client from organization A; request an asset owned by organization B; try read and update operations. | The API denies both operations without exposing asset details. | Organizations A and B and their assets exist. | Pending |  |  | Pending |  |  | Pending |  |  |  |
| WF1-004 | Periodic schedule creates one due inspection request. | Create an active schedule; advance to its due cycle; run the scheduler twice; inspect requests. | Exactly one request is created for the asset and cycle; a retry does not duplicate it. | Active asset, schedule, checklist, and scheduler are available. | Pending |  |  | Pending |  |  | Pending |  |  |  |
