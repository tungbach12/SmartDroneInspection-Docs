# FE-22: Partner Inspector Payout Reconciliation

Synchronized with Report 3 SRS v2.2 and Report 4 SDD v2.4; upstream of the `(FE-22)` test sheet in `Report5_Test Report.xlsx`.

## Feature sheet summary

Values for the `Feature 22` summary block (`A2:E8` in the workbook).

| Cell | Label | Value |
| --- | --- | --- |
| `B2` | Feature | Partner Inspector Payout Reconciliation |
| `B3` | Test requirement | Verifies Platform Manager partner Inspector payout ledger transitions (`ELIGIBLE -> PAID`), manual bank transfer reference recording, idempotent duplicate-payout protection, and payout caps against captured occurrence revenue and active refund holds. |

## Test case execution records

| Test Case ID | Test Case Description | Test Case Procedure | Expected Results | Pre-conditions | Round 1 | Test date | Tester | Round 2 | Test date | Tester | Round 3 | Test date | Tester | Note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| WF3-033 | Manager reconciles eligible Partner Inspector payouts with duplicate reference guards and holds. | 1. Open Manager Inspector Payouts and select an Eligible payout.<br>2. Submit bank transfer payout reference and confirm status transitions to Paid.<br>3. Attempt duplicate reference or settlement while payout hold is active. | Valid reconciliation settles payout with transfer reference and audit trail; duplicate references and held payouts are blocked cleanly. | Settled customer order producing an Eligible payout; active Manager account. | N/A |  |  | Pending |  |  | Passed | 2026-11-26 | Trương Thái Như | Verified via automated integration & regression suite (Nov 2026). |
| WF3-036 | Payout gate blocks disbursement before publication and validates outgoing payout webhook fields. | 1. Attempt Manager payout recording on an occurrence before its report is Published.<br>2. Send an outgoing Sepay payout webhook with wrong amount or mismatched Inspector bank account. | Payout recording is blocked until report publication; outgoing payout webhooks reject wrong amounts or destination accounts without settling the payout. | Paid occurrence before publication; Inspector payout bank account configured. | N/A |  |  | N/A |  |  | Passed | 2026-11-27 | Trương Thái Như | Verified via InspectionFinanceApiIntegrationTest & SepayWebhookControllerTest. |
