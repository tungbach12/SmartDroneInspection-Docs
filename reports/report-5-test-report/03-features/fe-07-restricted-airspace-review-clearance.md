# FE-07: Restricted Airspace Advisory Warning & Immediate Onboarding

Synchronized with Report 3 SRS v2.7 and Report 4 SDD v2.9; upstream of the `(FE-07)` test sheet in `Report5_Test Report.xlsx`.

## Feature sheet summary

Values for the `Feature 7` summary block (`A2:E8` in the workbook).

| Cell | Label | Value |
| --- | --- | --- |
| `B2` | Feature | Restricted Airspace Advisory Warning & Immediate Onboarding |
| `B3` | Test requirement | Verifies immediate Customer account + initial building activation when registering in `RESTRICTED_ZONE`, amber `MSG28` flight-permit warning banners (zone name, authority, altitude ceiling, `cambay.mod.gov.vn`) across registration, coordinate picker, and service requests, hard `NO_FLY_ZONE` rejection, and removal of legacy `AirspaceReviewController`. |

## Test case execution records

| Test Case ID | Test Case Description | Test Case Procedure | Expected Results | Pre-conditions | Round 1 | Test date | Tester | Round 2 | Test date | Tester | Round 3 | Test date | Tester | Note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| WF1-009 | Restricted-airspace Customer onboarding activates immediately with `MSG28` advisory warning and drops legacy Admin airspace clearance queue. | 1. Submit POST /api/v1/auth/register with valid OTP and `firstAsset` coordinates inside a `RESTRICTED_ZONE` (e.g., Tan Son Nhat CTR).<br>2. Verify no request enters `PENDING_AIRSPACE_REVIEW` and the legacy `/api/v1/platform/customer-airspace-reviews` & `customer-airspace` admin route are absent.<br>3. Verify Web/Mobile UI display amber `MSG28` warning on pin selection, post-registration sign-in banner, service-request creation, and asset overview badge. | Registration returns 201 Created with `UserStatus.ACTIVE`, active initial building, `airspaceClassification=RESTRICTED_ZONE`, and advisory `reviewMessage`; `NO_FLY_ZONE` still fails with 403 `ASSET_IN_NO_FLY_ZONE`; Admin cannot mutate onboarding or report review/publish endpoints (403). | PostgreSQL 17 with `AirspaceAdvisoryService` and seeded Customer/Manager/Admin roles. | Passed | 2026-10-23 | Trần Hoàng Trung Hiếu | Pending |  |  | Pending |  |  | [Target: FE-07 Restricted Airspace Advisory BR-06] [Mode: Automated (OrganizationRegistrationServiceTest, OrganizationRegistrationApiIntegrationTest, Mf1ReviewPage.test.tsx, vitest, flutter test)] [Owner: Trần Hoàng Trung Hiếu]; Re-verified 2026-11-25: Backend `./mvnw test` `1052/1052`, Frontend `vitest run` `826/826` (`116/120` files, `4` deprecated skipped), Mobile `flutter test` `58/58`. |
