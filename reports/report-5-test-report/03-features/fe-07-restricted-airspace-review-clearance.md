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
| WF1-009 | Customer registration in restricted airspace activates immediately with advisory MSG28 warning. | 1. Submit Customer registration with valid OTP and initial asset coordinates inside a Restricted Airspace zone.<br>2. Verify no Admin clearance queue or approval hold blocks activation.<br>3. Check the Web and Mobile banners for the MSG28 flight-permit advisory warning. | Account and initial asset activate immediately (201 Created) with restricted-zone classification and amber MSG28 advisory warning; No-Fly Zone coordinates remain blocked (403). | Customer registration flow enabled; Vietnam airspace zones seeded. | Passed | 2026-10-23 | Trần Hoàng Trung Hiếu | Pending |  |  | Passed | 2026-11-26 | Phùng Trung Quốc | Verified via automated backend, Web & Mobile regression (Nov 2026). |
| WF1-023 | Building perimeter overlapping an adjacent No-Fly Zone triggers warning and ceiling lookup. | 1. Evaluate airspace using an asset center outside a No-Fly Zone whose building footprint overlaps an adjacent NFZ.<br>2. Query a restricted zone for ceiling altitude and controlling authority metadata. | Perimeter overlap into an adjacent No-Fly Zone is flagged before registration/dispatch; restricted zone returns exact ceiling altitude in meters and controlling authority. | Seeded Vietnam NFZ and Restricted Airspace polygons; asset dimension data. | N/A |  |  | N/A |  |  | Passed | 2026-11-27 | Phùng Trung Quốc | Verified via AirspaceAdvisoryServiceTest perimeter & ceiling tests. |
