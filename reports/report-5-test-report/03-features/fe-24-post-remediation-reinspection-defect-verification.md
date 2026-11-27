# FE-24: Post-Remediation Re-inspection & Defect Verification

Synchronized with Report 3 SRS v2.2 and Report 4 SDD v2.4; upstream of the `(FE-24)` test sheet in `Report5_Test Report.xlsx`.

## Feature sheet summary

Values for the `Feature 24` summary block (`A2:E8` in the workbook).

| Cell | Label | Value |
| --- | --- | --- |
| `B2` | Feature | Post-Remediation Re-inspection & Defect Verification |
| `B3` | Test requirement | Verifies follow-up re-inspection creation against published reports, duplicate open re-inspection blocking (`409 REINSPECTION_ALREADY_OPEN`), three-way defect verification verdicts (`RESOLVED`, `UNRESOLVED`, `INCONCLUSIVE`), fresh in-session evidence rules, `RESOLVED` verdict expiry warnings across Inspector, Manager, and Customer Web (`VerdictExpiryBanner`) plus Mobile (`verdict_expiry.dart`), and Customer Mobile parity (`PR #27`). |

## Test case execution records

| Test Case ID | Test Case Description | Test Case Procedure | Expected Results | Pre-conditions | Round 1 | Test date | Tester | Round 2 | Test date | Tester | Round 3 | Test date | Tester | Note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| WF3-028 | RESOLVED re-inspection requires fresh current-session evidence and blocks duplicate open follow-ups. | 1. Submit RESOLVED using source-inspection evidence, uncompleted session, or out-of-window capture (expect 400 rejections).<br>2. Submit RESOLVED with fresh evidence captured inside the completed re-inspection session.<br>3. Open a quick re-inspection while an MF2 request for the same source is already open (and concurrently). | Stale or out-of-session evidence fails with clear 400 error codes; fresh evidence saves RESOLVED; duplicate or concurrent second re-inspection for the same source returns 409 REINSPECTION_ALREADY_OPEN. | Published source inspection with confirmed defects and a completed re-inspection session. | Pending |  |  | Pending |  |  | Passed | 2026-11-18 | Trương Thái Như | Verified via automated integration & regression suite (Nov 2026). |
| WF3-031 | Web and Mobile sync RESOLVED defect expiry banners, payment documents, chat, and knowledge display. | 1. View a published report with a RESOLVED verdict expiring within 14 days across Inspector, Manager, and Customer Web (`VerdictExpiryBanner`) and Mobile.<br>2. Verify Customer notice/receipt PDF, Inspector chat visibility, and empty knowledge strip handling.<br>3. Probe Customer Mobile access with non-Customer roles and foreign accounts. | All portals display consistent verdict expiry alerts (`VerdictExpiryBanner` and Mobile); payment documents and chat stay scoped strictly to the owning Customer; foreign customers and non-Customer roles are blocked. | Published report with expiry window, payment due date, and active Customer Mobile build. | N/A |  |  | N/A |  |  | Passed | 2026-11-19 | Trương Thái Như | Verified via automated backend, Web & Mobile regression (Nov 2026). |
| WF3-041 | Post-remediation RESOLVED verdict stamps validity window while UNRESOLVED leaves no expiry. | 1. Record a RESOLVED defect verdict with validity duration and verify calculated expiry timestamp.<br>2. Advance clock past the expiry date and check expired verdict flag.<br>3. Record an UNRESOLVED verdict or RESOLVED without duration. | RESOLVED stamps exact expiry timestamp and raises expiry flag once overdue; UNRESOLVED or durationless verdicts carry no artificial validity window. | Completed re-inspection with defect verification records. | N/A |  |  | N/A |  |  | Passed | 2026-11-27 | Trương Thái Như | Verified via ReinspectionDefectVerificationTest (4/4). |
