# FE-21: Payment Deadlines, Invoices & Payment Document Management

Synchronized with Report 3 SRS v2.2 and Report 4 SDD v2.4; upstream of the `(FE-21)` test sheet in `Report5_Test Report.xlsx`.

## Feature sheet summary

Values for the `Feature 21` summary block (`A2:E8` in the workbook).

| Cell | Label | Value |
| --- | --- | --- |
| `B2` | Feature | Payment Deadlines, Invoices & Payment Document Management |
| `B3` | Test requirement | Verifies acceptance-stamped `payment_due_at` deadlines (default 15 days), daily single overdue reminder events (`PaymentDueExpiryService`) without revoking report access, and role-scoped `GET /api/v1/inspections/{id}/report/payment-document` notice and receipt PDFs. |

## Test case execution records

| Test Case ID | Test Case Description | Test Case Procedure | Expected Results | Pre-conditions | Round 1 | Test date | Tester | Round 2 | Test date | Tester | Round 3 | Test date | Tester | Note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| WF3-026 | Report acceptance starts 15-day payment deadline and triggers idempotent overdue alerts. | 1. Accept a published report as Customer and inspect the generated payment due date.<br>2. Run the overdue scan past the due date once, then run a second scan.<br>3. Confirm Customer still retains access to the published report. | Payment deadline is stamped once upon acceptance; overdue scan sends exactly one deduplicated alert to Customer and active Managers; repeat scans do not duplicate alerts and report access stays open. | Accepted inspection report with an unpaid invoice and active Customer/Manager accounts. | Pending |  |  | Pending |  |  | Passed | 2026-11-19 | Trương Thái Như | Verified via automated integration & regression suite (Nov 2026). |
| WF3-027 | Download Customer Payment Notice PDF while unpaid and Payment Receipt PDF after settlement. | 1. Request payment PDF before Customer accepts the report (expect 409).<br>2. Accept report and download PDF while unpaid (Notice PDF).<br>3. Confirm payment and download PDF again (Receipt PDF).<br>4. Probe endpoint as another organization or unassigned Inspector. | Unaccepted reports reject download (409); unpaid orders return a Notice PDF with breakdown and due date; paid orders return a Receipt PDF with transaction timestamp/reference; unauthorized users get 404. | Published inspection report with unpaid then paid settlement states. | Pending |  |  | Pending |  |  | Passed | 2026-11-19 | Trương Thái Như | Verified via automated integration & regression suite (Nov 2026). |
| WF3-040 | Idempotent overdue deadline marking and clearing upon Customer payment confirmation. | 1. Confirm Customer acceptance sets a single payment deadline.<br>2. Stamp overdue status twice after the deadline expires.<br>3. Record payment confirmation and inspect deadline/reminder flags. | Overdue marking is idempotent without duplicating reminder timestamps; payment confirmation clears the overdue deadline state cleanly. | Accepted inspection report transitioning from unpaid to paid status. | N/A |  |  | N/A |  |  | Passed | 2026-11-27 | Trương Thái Như | Verified via ServicePaymentTest deadline & settlement tests. |
