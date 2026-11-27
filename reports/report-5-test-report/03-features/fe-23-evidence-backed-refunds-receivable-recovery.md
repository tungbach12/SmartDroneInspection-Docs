# FE-23: Evidence-Backed Refunds & Receivable Recovery

Synchronized with Report 3 SRS v2.2 and Report 4 SDD v2.4; upstream of the `(FE-23)` test sheet in `Report5_Test Report.xlsx`.

## Feature sheet summary

Values for the `Feature 23` summary block (`A2:E8` in the workbook).

| Cell | Label | Value |
| --- | --- | --- |
| `B2` | Feature | Evidence-Backed Refunds & Receivable Recovery |
| `B3` | Test requirement | Verifies refund initiation holding unpaid partner payouts, transfer-reference completion with exact evidence-backed allocation, legacy refund-by-ID reconciliation, post-payout Inspector receivable creation and manual recovery without auto-offsetting, and cumulative caps. |

## Test case execution records

| Test Case ID | Test Case Description | Test Case Procedure | Expected Results | Pre-conditions | Round 1 | Test date | Tester | Round 2 | Test date | Tester | Round 3 | Test date | Tester | Note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| WF3-021 | Refund lifecycle, legacy reconciliation, post-payout Inspector receivables, and payout holds. | 1. Initiate a refund and confirm unpaid Inspector payout is automatically placed on hold.<br>2. Complete refund with valid external reference and exact allocation; verify duplicate/over-allocated amounts reject.<br>3. Reconcile legacy unallocated refund rows individually.<br>4. Initiate a refund after payout was already marked Paid and record partial then full manual receivable recovery. | Payout holds enforce pre-transfer safety; completed refunds are terminal and traceable; post-payout refunds create an audit receivable without mutating historical payouts or auto-deducting future pay. | Captured payment, pending/paid payout fixtures, Manager and Inspector test accounts. | Pending |  |  | Pending |  |  | Passed | 2026-11-19 | Trương Thái Như | Verified via automated integration & regression suite (Nov 2026). |
| WF3-037 | Refund allocation bounds, terminal completed refunds, and Inspector receivable recovery caps. | 1. Initiate or complete a refund with negative allocation, missing reference, or on an already completed refund.<br>2. Record a receivable recovery exceeding the outstanding balance or missing note/reference. | Negative allocations and missing references reject cleanly; completed refunds remain terminal; receivable recovery blocks amounts above outstanding balance. | Refundable occurrence and outstanding Inspector receivable record. | N/A |  |  | N/A |  |  | Passed | 2026-11-27 | Trương Thái Như | Verified via ServiceRefundTest (13/13) & InspectorReceivableTest (7/7). |
