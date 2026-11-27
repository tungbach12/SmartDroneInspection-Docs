# FE-20: Online Service Fee Payment (Sepay VietQR & VNPay)

Synchronized with Report 3 SRS v2.2 and Report 4 SDD v2.4; upstream of the `(FE-20)` test sheet in `Report5_Test Report.xlsx`.

## Feature sheet summary

Values for the `Feature 20` summary block (`A2:E8` in the workbook).

| Cell | Label | Value |
| --- | --- | --- |
| `B2` | Feature | Online Service Fee Payment (Sepay VietQR & VNPay) |
| `B3` | Test requirement | Verifies normalized `V29` finance tables (`service_invoices`, `service_payments`, `inspector_payouts`) plus `V67` (`gateway_order_created_at`) and `V68` (`gateway_inbound_transactions`), Sepay VietQR (`Authorization: Apikey`, receiving-account check, idempotent inbound audit trail) and VNPay v2.1.0 (HMAC-SHA512 checkout/Return/IPN verification, cancel/expiry order release), whole-VND validation, and role-masked financial projections. |

## Test case execution records

| Test Case ID | Test Case Description | Test Case Procedure | Expected Results | Pre-conditions | Round 1 | Test date | Tester | Round 2 | Test date | Tester | Round 3 | Test date | Tester | Note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| WF3-018 | Separate billing, payment, and Inspector payout data models cleanly per occurrence | 1. Run database setup on a clean test database.<br>2. Inspect invoice, payment, and payout table definitions.<br>3. Save a scheduled inspection and verify invoice price, payment reference, and payout recipient details. | Setup succeeds cleanly. Separate billing, payment, and payout records are stored per occurrence, and legacy duplicate columns are removed. | Active test database with seeded service request, Customer, Inspector, drone, and inspection data. | N/A |  |  | N/A |  |  | Passed | 2026-11-05 | Trương Thái Như | Verified via automated integration tests (Nov 2026). |
| WF3-019 | Report acceptance, payment confirmation, and Manager-recorded Inspector payout update billing records consistently | 1. Publish and accept a report, then confirm a matching payment via Sepay (VietQR) or VNPay.<br>2. Verify Inspector payout status becomes ELIGIBLE without auto-paying.<br>3. Record the Inspector payout as Manager and check role-based masking across Customer, Inspector, and Manager views. | Invoice snapshot stays intact, confirmed payment marks payout ELIGIBLE only, and Manager payout recording saves PAID status, recipient, and reference while masking sensitive fields per role. | Published inspection report and occurrence with Customer, Inspector, Manager, and payment webhook test data. | N/A |  |  | N/A |  |  | Passed | 2026-11-19 | Trương Thái Như | Verified via automated billing & payment integration tests (Nov 2026). |
| WF3-039 | Sepay webhook enforces API-key security, idempotent redelivery, and mismatch rejection. | 1. Send a Sepay webhook payload with an invalid or unconfigured API key.<br>2. Replay an already processed incoming transfer ID.<br>3. Send a webhook with a wrong transfer amount or mismatched receiving bank account. | Invalid API key fails closed (401); duplicate webhook deliveries are ignored idempotently; amount or account mismatches are recorded safely without marking the invoice Paid. | Active Sepay payment order and webhook receiver configuration. | N/A |  |  | N/A |  |  | Passed | 2026-11-27 | Trương Thái Như | Verified via SepayWebhookControllerTest (14/14) & SepayGatewayTest (6/6). |
