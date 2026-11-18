---
title: "Report 5 - Test Documentation Record of Changes"
document_type: report5-doc-section
weight: 5
source: "Report5_Test Documentation.docx"
---

# I. Record of Changes

| Date | A*M, D | In charge | Change Description |
| --- | --- | --- | --- |
| 03 Nov 2026 | A | Project Team | Version 1.0: Initial release of the Software Test Documentation for SmartDroneInspection covering test scope, strategy, levels, environment, and traceability across the 8 product features (FE-01 to FE-08, Feature 1 to Feature 8). |
| 17 Nov 2026 | M | Project Team | Version 2.0 — rewritten against the delivered product and re-executed. **Scope corrected to `FE-01`–`FE-06`** and the retired `FE-07`/`FE-08`, `MAINTENANCE_ENGINEER`, `MF4`, and `pgvector`/RAG claims removed from every table. **Corrections applied:** Flyway `V1`–`V28`/36 tables replaced by `V1` + `V2` and 41 tables; `NFR-01`–`NFR-06` replaced by `NFR-01`–`NFR-08`; `BR-01`–`BR-49` replaced by `BR-01`–`BR-54`; the five-role matrix replaced by the delivered four roles; and the mobile application documented as Customer-only. **Results re-executed on 17 Nov 2026:** backend `119` classes / `627` tests, `0` failures, JaCoCo line coverage `72.2%`; frontend `89` files / `627` tests (`623` passed, `4` skipped); mobile `13` files / `42` tests, all passed. **Two defects recorded as open** rather than omitted: the mobile `UserRole` enum still parses the retired `MAINTENANCE_ENGINEER` role, and `e2e/scripts/run-e2e.mjs` resolves a frontend directory that does not exist. |

| 18 Nov 2026 | M | Project Team | Version 2.1 — restructured to the eight-feature model (`FE-01`–`FE-08`, two features per main flow `MF1`–`MF4`). Scope, NFR-07, test levels, resource ownership, milestones, the workbook description, and the statistics pointer now enumerate eight features and eight `Feature` sheets. `FE-07` covers report preparation, review and publication; `FE-08` covers customer acceptance, PayOS and VNPay settlement, the re-inspection loop, and partner payouts. Corrective maintenance execution remains out of scope. |

*A - Added M - Modified D - Deleted
