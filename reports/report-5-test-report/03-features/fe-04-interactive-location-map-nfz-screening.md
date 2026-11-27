# FE-04: Interactive Location Map & No-Fly Zone Airspace Screening

Synchronized with Report 3 SRS v2.2 and Report 4 SDD v2.4; upstream of the `(FE-04)` test sheet in `Report5_Test Report.xlsx`.

## Feature sheet summary

Values for the `Feature 4` summary block (`A2:E8` in the workbook).

| Cell | Label | Value |
| --- | --- | --- |
| `B2` | Feature | Interactive Location Map & No-Fly Zone Airspace Screening |
| `B3` | Test requirement | Verifies `AirspaceAdvisoryService`, Web `AirspaceNoFlyMap`, and Mobile `AirspaceAdvisoryCard` zone classification (`CLEAR_ZONE`, `RESTRICTED_ZONE`, `NO_FLY_ZONE`), hard registration blocks inside prohibited zones, and out-of-bounds latitude/longitude validation. |

## Test case execution records

| Test Case ID | Test Case Description | Test Case Procedure | Expected Results | Pre-conditions | Round 1 | Test date | Tester | Round 2 | Test date | Tester | Round 3 | Test date | Tester | Note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| WF1-002 | Customer registration enforces No-Fly Zone airspace gate, immediate `RESTRICTED_ZONE` advisory warning, and input validation. | 1. Submit POST /api/v1/auth/register with `firstAsset` coordinates inside a prohibited NO_FLY_ZONE.<br>2. Submit POST /api/v1/auth/register with `firstAsset` inside a RESTRICTED_ZONE.<br>3. Submit weak password (<8 chars), duplicate `organizationCode` or `email`, or invalid OTP code. | Prohibited NO_FLY_ZONE coordinates are rejected (`403 ASSET_IN_NO_FLY_ZONE`); restricted-airspace registration activates the Customer account and initial asset immediately with `airspaceClassification=RESTRICTED_ZONE` and `MSG28` advisory warning (no admin approval queue); weak password, duplicate email/code, or invalid OTP is rejected with 400/409. | Existing tenant fixture and airspace screening service, Backend database. | Passed | 2026-10-22 | Trần Tùng Bách | Pending |  |  | Passed | 2026-11-26 | Trần Hoàng Trung Hiếu | Verified via automated integration & regression suite (Nov 2026). |
| WF2-004 | airspace screening service, Web `AirspaceNoFlyMap`, and Mobile `AirspaceAdvisoryCard` classify coordinates into No-Fly Zone, Restricted Zone, or Clear Zone with `MSG28` warnings. | 1. Query GET /api/v1/airspace/zones.<br>2. Evaluate coordinates inside Tan Son Nhat / Ba Dinh prohibited zone, inside restricted buffer, and in clear airspace via GET /api/v1/airspace/evaluate.<br>3. Render `AirspaceNoFlyMap` on Web (with Nominatim search) and `AirspaceAdvisoryCard` on Mobile. | Returns accurate Haversine classification (`NO_FLY_ZONE`, `RESTRICTED_ZONE`, `CLEAR_ZONE`), surfaces `MSG28` warning and `cambay.mod.gov.vn` reference, and renders interactive vector overlays. | Backend airspace screening service, Web `AirspaceNoFlyMap`, and Mobile `AirspaceAdvisoryCard`. | Passed | 2026-10-27 | Phùng Trung Quốc | Pending |  |  | Passed | 2026-11-26 | Trần Hoàng Trung Hiếu | Verified via automated backend & Web regression suite (Nov 2026). |
| WF2-005 | Airspace evaluation endpoint rejects invalid latitude/longitude bounds. | 1. Call GET /api/v1/airspace/evaluate with `latitude=95.0` or `longitude=190.0`.<br>2. Verify validation error response. | Out-of-bounds coordinates outside `[-90..90]` and `[-180..180]` are rejected with 400 Bad Request. | `AirspaceController` and airspace screening service. | Passed | 2026-10-27 | Phùng Trung Quốc | Pending |  |  | Passed | 2026-11-26 | Trần Hoàng Trung Hiếu | Verified via automated integration & regression suite (Nov 2026). |
