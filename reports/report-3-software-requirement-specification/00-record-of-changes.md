---
title: "Report 3 - Record of Changes"
document_type: report3-srs-section
weight: 5
source: "report3-software-requirement-specification.docx"
---

# I. Record of Changes

| Date | A* M, D | In charge | Change Description |
| --- | --- | --- | --- |
| 03 Nov 2026 | A | Project Team | Version 1.0: Initial release of the Software Requirement Specification (SRS) for SmartDroneInspection covering the 5-role Platform Inspection Service model (ADMIN, MANAGER, CUSTOMER, INSPECTOR, MAINTENANCE_ENGINEER) and 8 product features (FE-01 to FE-08) across MF1–MF4. |
| 08 Nov 2026 | M | Project Team | Version 1.1: Clarified section 3.3.2 Drone MTOW classification (Categories 1–5 per Article 4 Decree 288/2025/ND-CP) and Class A vs. Class B pilot license enforcement (Article 27), plus section 3.9.2 re-inspection compliance and RAG-grounded acceptance workflow rules. |
| 10 Nov 2026 | M | Project Team | Clarified FE-05 field session fallback for aircraft without live MAVLink: supported SRT/CSV/KML/GPX import and distinctly labelled, accountable manual declarations when no supported log exists; absent source telemetry must not be fabricated. |
| 11 Nov 2026 | M | Project Team | Section 3.5.1 (FE-04): Single-quote model without version history, direct active quote editing prior to acceptance, ONE_TIME single-date constraint, immutable accepted terms snapshot, and dedicated left-nav Messages inbox for Customer/Manager replacing floating chat. |
| 11 Nov 2026 | M | Project Team | Sections 3.4.1 (FE-03) and 3.5.1 (FE-04): Simplified Customer request creation to asset/date/type, moved detailed scope into Manager quotation, added monthly recurrence intervals (1–120 months) and 2–100 occurrence bounds, clarified anchored month-end previews/term calculation, and set a 20-calendar-day internal scheduling lead time in Asia/Ho_Chi_Minh business time. |
| 11 Nov 2026 | M | Project Team | Sections 3.4.1 (FE-03) and 3.5.1 (FE-04): Require recurring quotation and preview to keep the Customer-requested first date as the schedule anchor; reject shifted first occurrences and end-date schedules with more than 100 occurrences. |
| 11 Nov 2026 | M | Project Team | Section 3.5.1 (FE-04): Require recurring quotations and previews to keep the Customer-requested first date as the schedule anchor; reject quotes that shift the first occurrence or whose end-date bound yields more than 100 occurrences. |
| 11 Nov 2026 | M | Project Team | Section 3.5.1 (FE-04): Clarify the four-stage request lifecycle indicator with role-specific Customer/Manager labels and no explanatory subtext. |
| 11 Nov 2026 | M | Project Team | Section 3.5.1 (FE-04): Align Service Requests list status chips with the shared inspection chip style and add a compact four-step request progress subtitle. |
| 11 Nov 2026 | M | Project Team | Sections 3.4.1 and 3.5.2 (FE-03/FE-04): Require partner Inspector pilot-license and drone-registration validity at every scheduled recurring occurrence before quote save/acceptance and occurrence materialization. |
| 11 Nov 2026 | M | Project Team | Section 3.5.1 (FE-04): Clarify that partner qualification validity covers every planned recurring occurrence before quotation persistence, Customer acceptance, and occurrence creation; no partial schedule is persisted when a license or registration expires before a planned start. |
| 11 Nov 2026 | M | Project Team | Reduced the current application scope to four login roles, FE-01–FE-06, and MF1–MF3; retired the Maintenance Engineer role and corrective maintenance requirements. Historical v1.0 scope above is retained as change history. Existing maintenance schema and data remain unchanged without destructive migration and are not exposed by the application. |
| 11 Nov 2026 | M | Project Team | Updated FE-02 §3.3.2 drone registration requirements: added Admin-configurable document requirements (`drone_document_configs` with `REGISTRATION` and `OWNERSHIP` active/required by default and `INSPECTION` optional/inactive by default), mandatory drone photo upload (`>= 1` `DRONE_IMAGE`), structured outdoor flight capabilities (wind resistance, optical zoom, thermal/RTK flags), Admin-configurable features/safety checklist (`drone_feature_configs`), and Inspector renewal/update of own existing drones. |
| 11 Nov 2026 | M | Project Team | Clarified FE-06 finance lifecycle: customer payment grants payout eligibility but does not record Inspector disbursement; Manager-attributed payout, verifiable unpaid-order cancellation, externally transferred refund ledger, cumulative refund cap, payout hold, and explicit final-payout reconciliation. |
| 12 Nov 2026 | M | Project Team | Clarified the refund lifecycle: Managers initiate and hold payout before manual external transfer, complete only after transfer evidence, cancel only untransferred requests, reconcile legacy rows individually, and create/recover Inspector receivables after an already-paid payout without automatically offsetting future payouts. Each completed external refund must be allocated across Inspector payout reduction, platform commission, VAT, TNCN, or platform absorption; final payout is capped after verified reductions. |
|  |  |  |  |
|  |  |  |  |

*A - Added M - Modified D - Deleted
