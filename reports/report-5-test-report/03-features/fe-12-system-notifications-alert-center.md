# FE-12: System Notifications & Alert Center

Synchronized with Report 3 SRS v2.2 and Report 4 SDD v2.4; upstream of the `(FE-12)` test sheet in `Report5_Test Report.xlsx`.

## Feature sheet summary

Values for the `Feature 12` summary block (`A2:E8` in the workbook).

| Cell | Label | Value |
| --- | --- | --- |
| `B2` | Feature | System Notifications & Alert Center |
| `B3` | Test requirement | Verifies event-driven asynchronous notification dispatch through the Spring Modulith `event_publication` outbox, deduplication on `uq_notifications_deduplication_key`, idempotent `SENT -> READ` transitions, and a deduplicated new-service-request notice to every active Manager. |

## Test case execution records

| Test Case ID | Test Case Description | Test Case Procedure | Expected Results | Pre-conditions | Round 1 | Test date | Tester | Round 2 | Test date | Tester | Round 3 | Test date | Tester | Note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| WF2-025 | A new Customer service request notifies every active Manager. | 1. Create a one-time or recurring service request as the owning Customer.<br>2. Inspect the notifications of two active Managers and one inactive Manager.<br>3. Replay new request notification event with the same request identifier and verify no duplicate row.<br>4. Follow the notice target as a Manager. | Each active Manager receives exactly one `SERVICE_REQUEST_CREATED` notice containing the request description and date, with target `/manager/contracts?requestId={id}`; the inactive Manager receives nothing, replay is ignored by the deduplication key, and the deep link opens the Manager request detail. | backend database notification schema, active/inactive Manager fixtures, new request notification event, notification listener, notification tests, and `ServiceRequestNotificationListenerTest`. | Passed | 2026-11-23 | Phùng Trung Quốc | Pending |  |  | Passed | 2026-11-26 | Phùng Trung Quốc | Verified via automated integration & regression suite (Nov 2026). |
| WF1-020 | Domain events publish in-app notifications via Spring Modulith outbox, deduplicate on notification deduplication rule, and transition `SENT -> READ` idempotently. | 1. Publish `InspectionAssignedEvent`, `InspectionDeclinedEvent`, `FlightPermitSubmittedEvent`, and new request notification event (including duplicate replay with the same `deduplication_key`).<br>2. Call GET /api/v1/notifications, GET /unread-count, and PATCH /api/v1/notifications/{id}/read.<br>3. Attempt to read/mark another user's notification. | First event persists a `SENT` `Notification` row; duplicate replay is safely ignored; PATCH transitions status `SENT -> READ` idempotently; cross-user read/mark returns 404 Not Found. | backend database with `V1__baseline.sql` and notification listeners active. | Passed | 2026-10-26 | Trần Hoàng Trung Hiếu | Pending |  |  | Passed | 2026-11-26 | Phùng Trung Quốc | Verified via automated backend & Web regression suite (Nov 2026). |
| WF2-028 | Full-lifecycle bilingual (VI/EN) in-app notifications, critical emails, and mark-all-read synchronization. | 1. Trigger domain events across commercial, dispatch, field session, media, report, drone expiry, and security flows.<br>2. Mark individual notices read and call Mark All as Read.<br>3. Switch Web locale between Vietnamese and English and verify localized alerts across notification inbox and 3 chat channels (`Order`, `Inspection`, `Partner`). | Events create deduplicated bilingual notifications without cross-module errors; critical alerts trigger email delivery; Mark All as Read updates only the signed-in user; UI displays only active locale text. | Notification outbox, optional mail sender, and all 4 roles configured. | Passed | 2026-11-25 | Phùng Trung Quốc | Pending |  |  | Passed | 2026-11-26 | Phùng Trung Quốc | Verified via automated backend & Web regression suite (Nov 2026). |
