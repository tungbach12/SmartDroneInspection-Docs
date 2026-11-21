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
| WF3-033 | Platform Manager reconciles Partner Inspector payouts (`ELIGIBLE -> PAID`) with external bank reference while enforcing duplicate-payout idempotency and refund holds. | 1. Inspect `ELIGIBLE` payout generated upon captured Customer payment.<br>2. Record external transfer reference and payout date as `MANAGER`.<br>3. Replay the payout-recording request with duplicate reference and attempt payout while an active refund hold is open. | First reconciliation transitions payout to `PAID` with manager ID, timestamp, and transfer reference; duplicate replay is idempotent/guarded without double payout; active refund holds block payout release. | PostgreSQL 17 with captured payment (`PAID`), `ELIGIBLE` Inspector payout row, refund hold fixture, and `MANAGER` account. | N/A |  |  | Pending |  |  | Pending |  |  | [Target: FE-22 Standalone Payout Reconciliation Case] [Mode: Unexecuted standalone case (underlying V29 payout contract covered by FE-20 WF3-019 and FE-23 WF3-021; standalone FE-22 workbook execution pending)] [Owner: Trương Thái Như] |
