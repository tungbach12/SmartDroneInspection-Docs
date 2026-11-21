# FE-19: Customer Report Acceptance & Clarification Workflow

Synchronized with Report 3 SRS v2.2 and Report 4 SDD v2.4; upstream of the `(FE-19)` test sheet in `Report5_Test Report.xlsx`.

## Feature sheet summary

Values for the `Feature 19` summary block (`A2:E8` in the workbook).

| Cell | Label | Value |
| --- | --- | --- |
| `B2` | Feature | Customer Report Acceptance & Clarification Workflow |
| `B3` | Test requirement | Verifies Customer review of published inspection reports, formal report acceptance (`ACCEPTED`) triggering commercial invoicing readiness, clarification request paths, and live staging Customer acceptance walkthroughs. |

## Test case execution records

| Test Case ID | Test Case Description | Test Case Procedure | Expected Results | Pre-conditions | Round 1 | Test date | Tester | Round 2 | Test date | Tester | Round 3 | Test date | Tester | Note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| WF3-012 | Live staging walkthrough of Customer report acceptance, Sepay VietQR / VNPay settlement, and PDF download. | 1. On staging (`smartdroneinspection.duckdns.org`), log in as `CUSTOMER` on a `PUBLISHED` report and click Accept Report.<br>2. Generate a Sepay VietQR code and scan it, or open the VNPay checkout link; verify webhook settlement (`PAID`), and download the A4 PDF report. | Customer report acceptance transitions occurrence to `PAYMENT_DUE`, payment callback transitions occurrence to `PAID`, and PDF report downloads cleanly; no maintenance workflow is available. | Published MF3 reports on staging (`smartdroneinspection.duckdns.org`) and `CUSTOMER` account. | Pending |  |  | Pending |  |  | Pending |  |  | [Target: State Transition Report Acceptance, Sepay/VNPay PAID & Handoff] [Mode: Manual (Staging Browser Walkthrough)] [Owner: Trần Tùng Bách]; [Sepay swap automated re-verification 2026-11-21 on Testcontainers PostgreSQL 17: `SepayGatewayTest` 6/6 (VietQR URL composition, merchant-account fallback, constant-time API-key verification), `SepayWebhookControllerTest` 5/5 (401 without/with a wrong `Apikey`, `SDI<orderCode>` resolved only from the transfer content, outgoing transfers ignored, unknown order rejected), `SepayPaymentIntegrationTest` 2/2 (create VietQR, reject wrong API key, reject amount mismatch, settle with `PAID`, duplicate webhook idempotent); full backend `.\mvnw.cmd verify` ran 711 tests with 0 failures and 4 pre-existing `ffmpeg` environment errors. Live staging walkthrough remains Pending because the staging backend is not currently running.] |
