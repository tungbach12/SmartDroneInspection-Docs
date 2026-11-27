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
| WF3-032 | Customer, Partner Inspector, and Platform Manager query their scoped financial history and revenue/payment ledger views without cross-organization leakage. | 1. Open `/client/finance`, `/operations/earnings`, and `/manager/finance` with seeded paid/unpaid invoices and payouts.<br>2. Filter by status and date range and inspect ledger pagination and role-masked fields.<br>3. Probe another organization's or foreign Inspector's financial record ID. | Each role sees only its authorized financial ledger projection (`CUSTOMER`: organization invoices/payments; `INSPECTOR`: own payouts/receivables; `MANAGER`: platform revenue ledger with masked/unmasked boundaries); cross-scope queries return 403/404. | PostgreSQL 17 with Flyway `V29`–`V66`, seeded invoices, payments, and Inspector payouts across two tenants. | N/A |  |  | Pending |  |  | Passed | 2026-11-27 | Trần Hoàng Trung Hiếu | [Target: FE-05 Standalone Ledger Walkthrough] [Mode: Unexecuted standalone case (core V29 ledger persistence covered by FE-20 WF3-018/WF3-019; standalone multi-role ledger UI walkthrough pending)] [Owner: Trần Hoàng Trung Hiếu] [Round 3 (2026-11-27): Passed — verified live role-scoped ledgers via agent-browser (`/manager/finance-history` ₫62,000,000 net / ₫8,454,545 commission / ₫5,636,364 VAT; `/manager/payout-settlements` 5 payouts; `/operations/finance-history` 2 PAID payouts; `/client/finance-history` 4 PAID records) & cross-portal `/forbidden` 403 redirects, plus `InspectionFinanceApiIntegrationTest.completeInspectionFinanceWorkflow` & `OccurrenceFinanceResponseTest`.] |
