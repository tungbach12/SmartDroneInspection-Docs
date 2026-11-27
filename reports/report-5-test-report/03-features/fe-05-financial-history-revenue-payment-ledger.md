# FE-05: Financial History & Revenue/Payment Ledger

Synchronized with Report 3 SRS v2.2 and Report 4 SDD v2.4; upstream of the `(FE-05)` test sheet in `Report5_Test Report.xlsx`.

## Feature sheet summary

Values for the `Feature 5` summary block (`A2:E8` in the workbook).

| Cell | Label | Value |
| --- | --- | --- |
| `B2` | Feature | Financial History & Revenue/Payment Ledger |
| `B3` | Test requirement | Verifies role-scoped financial history and revenue/payment ledger tables across Customer payment history, Partner Inspector earnings history, and Platform Manager revenue ledger filters without cross-tenant disclosure. |

## Test case execution records

| Test Case ID | Test Case Description | Test Case Procedure | Expected Results | Pre-conditions | Round 1 | Test date | Tester | Round 2 | Test date | Tester | Round 3 | Test date | Tester | Note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| WF3-032 | Role-scoped financial history ledgers and cross-portal access isolation. | 1. Open `/manager/finance-history` and `/manager/payout-settlements` as Manager.<br>2. Open `/operations/finance-history` as Inspector and `/client/finance-history` as Customer.<br>3. Attempt to open `/client/finance-history` as Manager and `/manager/finance-history` as Customer/Inspector. | Each role sees accurate filtered financial KPIs and ledger rows; cross-role finance URLs redirect immediately to the 403 Forbidden screen. | Active Manager, Inspector, and Customer accounts with settled inspection records. | N/A |  |  | Pending |  |  | Passed | 2026-11-27 | Trần Hoàng Trung Hiếu | Verified via live Web walkthrough (agent-browser) & finance integration tests. |
| WF3-034 | Role-based financial data masking hides internal commission and TNCN tax from Customers. | 1. Query occurrence finance breakdown as Manager.<br>2. Query the same occurrence as the assigned Inspector.<br>3. Query as the owning Customer and probe cross-portal URLs. | Manager sees full revenue, commission, TNCN, and payout breakdown; Inspector sees payout breakdown without receivables/reviewer fields; Customer sees only billed fee/VAT with internal payouts masked. | Settled inspection occurrence with calculated VAT, commission, TNCN, and payout. | N/A |  |  | N/A |  |  | Passed | 2026-11-27 | Trần Hoàng Trung Hiếu | Verified via occurrence finance response unit & API integration tests. |
