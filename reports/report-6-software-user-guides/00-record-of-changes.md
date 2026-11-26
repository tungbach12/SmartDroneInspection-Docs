---
title: "Report 6 - Record of Changes"
document_type: report6-section
weight: 5
source: "Report6_Software User Guides.docx"
---

# I. Record of Changes

| Date | A*M, D | In charge | Change Description |
| --- | --- | --- | --- |
| 17 Nov 2026 | A | Project Team | Version 1.0: Initial release of the Release Package and User Guides for SmartDroneInspection. Covers the nine-item deliverable package, the hardware and software system requirements, the containerized installation procedure, and eight end-to-end workflows — customer onboarding, partner admission and drone registration, service request and quotation, dispatch and field session, evidence and findings, report submission and publication, report acceptance and payment, and the Customer-only mobile application — each illustrated with a captured interface screenshot. |

| 18 Nov 2026 | M | Project Team | Version 1.1 — workflow headings now name the main flow and features each guide serves (`MF1`–`MF4`, `FE-01`–`FE-08`), and the deliverable table points at the eight-feature backlog. Step content and screenshots are unchanged. |

| 19 Nov 2026 | M | Project Team | Version 1.2 — synchronized the release package and user guides with the 19 Nov 2026 baseline. The database deliverable now lists Flyway `V1`–`V4` and `V60`–`V62` (45 application tables / 47 total PostgreSQL 17 tables with `pgvector`), and the deliverable table references Report 5's 19 Nov 2026 baseline. Installation notes cover the `pgvector`-backed knowledge migration and automatic `HYBRID_MATCH` fallback without new required environment variables. The evidence/findings guide describes the collapsible "Similar Cases & Guide" chip strip (matched-case percentages, standard codes such as `TCVN 9343:2012`, one-click **Apply** into the technical note); the report guide notes the "Matched Cases & Standards" chips in the AI Executive Summary; the acceptance/settlement guide covers the payment-due badge and countdown, notice/receipt PDF download, re-inspection `RESOLVED` verdict expiry, and Inspector–Customer chat; and the customer mobile guide reflects parity for those views plus the collapsible `KnowledgeReferencesStrip`. |
| 20 Nov 2026 | M | Project Team | Version 1.3 — synchronized the release package and user guides with Flyway `V63`–`V65` (`V1`–`V4` and `V60`–`V65`, retaining 45 application tables / 47 total PostgreSQL 17 tables): lowered default auto-confirm confidence to `70%` (`V63`), added published-case backfill (`V64`), enabled built-in local `fastembed` `vector(384)` multilingual embeddings inside `ai-inference` (`V65`), and updated the findings user guide for quick status filter chips (`All active`, `Unconfirmed`, `Confirmed`), `Draft note with AI` with collapsed `References`, and batch `Draft all notes`. |
| 21 Nov 2026 | M | Project Team | Version 1.4 — synchronized the release package and workflow guides with the twenty-four atomic product features (`FE-01`–`FE-24`) across `MF1`–`MF4`, plain-text building ownership details, concise recurring service-request titles and streamlined commercial request/quotation workflows, and Report 5 `v3.9` (`24` sheets / `67` active test cases). |
| 22 Nov 2026 | M | Trương Thái Như | Version 1.5 — updated Workflow 7 (Report Acceptance and Payment) and Section 3.1 from PayOS to **Sepay VietQR** and **VNPay v2.1.0** (`V67`–`V68`): documented **Pay with VNPay** (direct `/settlement` return redirect and automatic order release on cancel/expiry so customers can retry immediately), **Pay with VietQR (Sepay)** (QR dialog with manual bank-transfer details and copy buttons, 3-second automatic settlement polling that closes the dialog on `PAID`, and **Check payment status**), the partner payout lifecycle (`PENDING -> ELIGIBLE -> PAID` via Manager UNC recording), and role-scoped Finance History views. |
| 26 Nov 2026 | M | Project Team | Refreshed the role-based walkthroughs, capture references, and publication and settlement instructions. |

*A - Added M - Modified D - Deleted
