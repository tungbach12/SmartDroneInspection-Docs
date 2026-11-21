# FE-12: System Notifications & Alert Center

Synchronized with Report 3 SRS v2.2 and Report 4 SDD v2.4; upstream of the `(FE-12)` test sheet in `Report5_Test Report.xlsx`.

## Feature sheet summary

Values for the `Feature 12` summary block (`A2:E8` in the workbook).

| Cell | Label | Value |
| --- | --- | --- |
| `B2` | Feature | System Notifications & Alert Center |
| `B3` | Test requirement | Verifies event-driven asynchronous notification dispatch through the Spring Modulith `event_publication` outbox, deduplication on `uq_notifications_deduplication_key`, and idempotent `SENT -> READ` transitions. |

## Test case execution records

| Test Case ID | Test Case Description | Test Case Procedure | Expected Results | Pre-conditions | Round 1 | Test date | Tester | Round 2 | Test date | Tester | Round 3 | Test date | Tester | Note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| WF1-020 | Domain events publish in-app notifications via Spring Modulith outbox, deduplicate on `uq_notifications_deduplication_key`, and transition `SENT -> READ` idempotently. | 1. Publish `InspectionAssignedEvent`, `InspectionDeclinedEvent`, and `FlightPermitSubmittedEvent` (including duplicate replay with the same `deduplication_key`).<br>2. Call GET /api/v1/notifications, GET /unread-count, and PATCH /api/v1/notifications/{id}/read.<br>3. Attempt to read/mark another user's notification. | First event persists a `SENT` `Notification` row; duplicate replay is safely ignored; PATCH transitions status `SENT -> READ` idempotently; cross-user read/mark returns 404 Not Found. | PostgreSQL 17 with `V1__baseline.sql` and notification listeners active. | Passed | 2026-10-26 | Trần Hoàng Trung Hiếu | Pending |  |  | Pending |  |  | [Target: State Transition NotificationStatus Sent -> Read & Deduplication] [Mode: Automated (InspectionNotificationListenerTest, NotificationServiceTest, NotificationControllerTest, NotificationBell.test.tsx)] [Owner: Phùng Trung Quốc] |
