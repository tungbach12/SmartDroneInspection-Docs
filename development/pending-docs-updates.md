---
title: "Pending Documentation Updates (Session Batch)"
type: "docs"
---

# Pending Documentation Updates (Session Batch)

Rolling change log for code and requirement changes made in this workspace session.
**Rule:** Do not edit formal reports or `.drawio` diagrams piecemeal during rapid code iterations. Record every change here as it happens, then apply all remaining targets in **one combined documentation & diagram pass** when requested.

---

## 1. `FE-13` — Flight Permit: Inspector Self-Attestation (No Manager Approval)

**Date:** 2026-11-23
**Status:**
- **Backend & Frontend code changes complete and verified** (Orca Run `run_c9df64a22a1e`, all workers settled: Docs `ctx_cd6d650cefd9`, Frontend `ctx_af0fc7b330bf`, Backend `ctx_57214d9b30aa`):
  - Backend: `rg -n "reviewFlightPermit|approveFlightPermit|FlightPermitReviewed|PERMIT_REVIEW" src` -> 0 matches; `./mvnw spotless:check` -> BUILD SUCCESS; 12 targeted flight-permit test classes (`37` tests run, `0` failures, `0` errors, `0` skipped) -> BUILD SUCCESS. *(Note: full `./mvnw clean test` reported 2 unrelated failures outside permit scope: `FindingTest.editingAFindingTakesBackItsConfirmation` from pre-existing `Finding.java` edit, and `SepayPaymentIntegrationTest.testFullSepayLifecycle` 400-vs-200 HEAD regression.)*
  - Frontend: `rg -n "reviewFlightPermit|useReviewFlightPermit|PERMIT_REVIEW|Pending Manager Verification|Approved by Manager" src` -> 0 matches; `npm run lint` -> 0 errors (51 pre-existing warnings); `npm test` -> 94 files passed / 4 skipped (721 tests passed / 4 skipped); `npm run build` -> clean (`vite build` succeeded).
- **Already edited in `SmartDroneInspection-docs` working tree** (by Docs worker `ctx_cd6d650cefd9`, prior to the "only change docs when asked" rule):
  - `reports/report-3-software-requirement-specification/03-functional-requirements.md`
  - `reports/report-3-software-requirement-specification/05-requirement-appendix.md`
  - `reports/report-3-software-requirement-specification/02-user-requirements.md`
  - `reports/report-3-software-requirement-specification/00-record-of-changes.md`
  - `bao-cao-thay-doi-mainflows-5-roles.md`
  - `project-reference/mainflows-4-workflows-guideline-v3.md`
  - `reports/report-5-test-report/01-test-cases/test-case-list.md` (new cases `WF2-029`–`WF2-031` currently marked unexecuted/planned; ready to mark executed/passed in the combined docs pass based on `FlightPermitVerificationIntegrationTest` and targeted backend tests above)

### Behavioral & Contract Summary
- **Self-attested upload (`APPROVED` immediately):** When the assigned `INSPECTOR` uploads a valid permit (`InspectionFlightPermit.record(...)`), `verificationStatus` is set immediately to `APPROVED` with `verifiedBy = uploadedBy` and `verifiedAt = uploadedAt` (self-attestation), clearing `rejectionReason` and `reviewNotes`. No Manager/Admin approval step is required to unlock Stage 2 Pre-flight or Field Session Start.
- **Validation retained at upload & flight start:** File validation (`<= 25 MB`, PDF/PNG/JPG/WEBP signature, SHA-256), metadata & schedule window checks, drone serial match, active pilot licence, and current drone registration remain enforced (`FlightPermitPolicy`).
- **Auto-invalidation (`PENDING_REVIEW` = re-upload required):** No DB schema migration or new enum value was added. Reassigning a different drone or rescheduling outside the permit validity window calls `requireReupload()` (`requireFlightPermitReupload()`), resetting status to `PENDING_REVIEW` and clearing verified fields so the inspector must upload an updated permit before flight start (`REJECTED` remains only for legacy rows and also requires inspector re-upload).
- **Removed Manager review API, events, notifications, and UI actions:**
  - Deleted `POST /api/inspections/{id}/flight-permit/review`, `InspectionCreationService.reviewFlightPermit(...)`, `ReviewFlightPermitRequest`, `FlightPermitReviewedEvent`, `InspectionNotificationListener.onFlightPermitReviewed`, and `InspectionNotificationService.recordFlightPermitReviewed`.
  - `InspectionNotificationService.recordFlightPermitSubmitted` now notifies managers FYI that the assigned inspector uploaded the permit and is responsible for its validity (no "awaiting verification" language).
  - Removed `'PERMIT_REVIEW'` from `InspectionListService.pendingAction(...)` and from frontend `InspectionsPage` filter/counters, `InspectionListTable`, and `workflowStepResolver`.
- **Frontend (`FieldSessionPage.tsx`, `FlightPermitVerificationPanel.tsx`, `FlightPermitPreviewDialog.tsx`):**
  - Removed the `NOT_UPLOADED` `<StatusChip>` from the Flight Permit header in `FieldSessionPage.tsx`, and `FlightPermitVerificationPanel` returns `null` when hidden flags (`hideHeader`, `hideEmptyNotice`, `!showAirspace`) leave no visible body on an un-uploaded permit.
  - `FlightPermitVerificationPanel` is now read-only (`canReview` and decision controls removed); status labels updated (`APPROVED` -> "Submitted by Inspector" / "Inspector đã nộp", `PENDING_REVIEW` -> "Re-upload required" / "Cần tải lại giấy phép", `REJECTED` -> "Invalid — re-upload required").

### Remaining Docs & Diagrams to Update in Combined Pass
- **Report 4 SDD** (`reports/report-4-software-design-document/`):
  - `01-system-design.md` — remove Manager permit verification gate from MF3 architecture/workflow summary.
  - `02-database-design.md` — clarify `inspection_flight_permits.verification_status` / `verified_by` semantics (`APPROVED` set on upload as inspector self-attestation; `PENDING_REVIEW` = re-upload required).
  - `03-detailed-design.md` — remove `POST /flight-permit/review`, `ReviewFlightPermitRequest`, `FlightPermitReviewedEvent`, `approveFlightPermit`, `rejectFlightPermit`; update `InspectionFlightPermit.record` & `requireReupload` and `Inspection.requireFlightPermitReupload`.
  - `00-record-of-changes.md` — append SDD change entry.
- **Report 5 Test Report** (`reports/report-5-test-report/`):
  - Once backend & frontend tests pass and are verified, update `WF2-029`, `WF2-030`, `WF2-031` status/evidence from unexecuted/planned to executed results, and update `02-test-execution/` / statistics if applicable.
- **Report 6 User Guides** (`reports/report-6-software-user-guides/01-user-guides.md`):
  - Remove Manager permit approve/reject instructions; document Inspector self-attested upload, immediate unlock, and re-upload after drone/schedule changes; note Manager/Admin read-only audit view.
- **Report 7 Final Project Report** (`reports/report-7-final-project-report/`):
  - `01-project-introduction.md`, `02-project-management-plan.md`, `03-software-requirement-specification.md`, `04-software-design-description.md`, `05-software-testing-documentation.md`, `06-release-package-and-user-guides.md`, `00-record-of-changes.md` — mirror the `FE-13` SRS/SDD/Test/User-guide updates.
- **Diagrams** (`diagrams/`):
  - `smartdrone-activity-diagrams.drawio` (`MF3 - Permit, Field & AI`) — remove Manager approve/reject swimlane step; show upload validation -> immediate effective permit -> pre-flight gate, plus drone/schedule change re-upload loop.
  - `smartdrone-sequence-diagrams.drawio` — remove `POST /flight-permit/review` and `FlightPermitReviewedEvent` interactions; update `uploadFlightPermit` sequence.
  - `smartdrone-class-diagrams.drawio` — remove `approveFlightPermit`/`rejectFlightPermit`/`reviewFlightPermit`/`ReviewFlightPermitRequest`/`FlightPermitReviewedEvent`; update `InspectionFlightPermit.requireReupload()`.
  - `smartdrone-use-case-diagrams.drawio` (`UC-3 Contracting & Field Execution`) — remove Manager permit verification use case/association if present.
  - `smartdrone-screen-flow-diagrams.drawio` — remove Manager permit decision branch from Web flow.
  - `diagrams/mermaid/` (`22_*`, `23_*`, `31_*`, `40_*`, `41_*`, `44_*`) — update or retire when Mermaid blocks are replaced per `development/diagram-synchronization-plan.md`.

---

## 2. `FE-16` / `FE-17` — Findings: Preserve `CONFIRMED` Status on Note Edit & Hide AI Draft Action

**Date:** 2026-11-23
**Status:** Code changes present in working tree (`SmartDroneInspection-backend`, `SmartDroneInspection-frontend`); docs not yet edited.

### Behavioral & Contract Summary
- **Backend (`Finding.java`, `FindingServiceReviewTest.java`):**
  - `Finding.updateDetails(...)` no longer resets `this.status = FindingStatus.PENDING`. Updating defect label, severity, or technical notes (including AI-drafted notes) on an already `CONFIRMED` finding preserves `FindingStatus.CONFIRMED`.
  - Unit test added: `FindingServiceReviewTest#preservesConfirmedStatusWhenUpdatingFindingNotes`.
- **Frontend (`EvidenceCaptureGroup.tsx`, `InspectionFindingsPage.test.tsx`):**
  - `DraftNoteAction` returns `null` when `finding.status === 'CONFIRMED'`, hiding `Draft note with AI` and `References` once a finding is confirmed.
  - Unit test added in `InspectionFindingsPage.test.tsx`.

### Docs & Diagrams to Update in Combined Pass
- **Report 3 SRS** (`03-functional-requirements.md` §3.17 `FE-16` / §3.18 `FE-17`): note that editing technical notes on a confirmed finding retains `CONFIRMED` status and AI note drafting actions are hidden for already-confirmed findings.
- **Report 4 SDD** (`03-detailed-design.md`): update `Finding.updateDetails` domain behavior note.
- **Report 5 Test Report** (`01-test-cases/test-case-list.md`): note or add coverage for `CONFIRMED` status preservation and hiding AI draft action after confirmation.
- **Report 6 User Guides** (`01-user-guides.md`): note in Inspector Findings section that `Draft note with AI` / `References` disappear after a finding is confirmed.

---

## 3. `FE-17` / `FE-18` — Report Compilation Toast & Audit Flight Operations Guard

**Date:** 2026-11-23
**Status:** Code changes present in working tree (`SmartDroneInspection-frontend`); docs not yet edited.

### Behavioral & Contract Summary
- **Frontend (`InspectionReportPage.tsx`, `InspectionReportPage.test.tsx`):**
  - Report compilation success (`"Report compiled successfully. Review the sections below."`) is surfaced via `useToastStore` toast on mutation `onSuccess` instead of a persistent inline success `<Alert>` banner.
- **Frontend (`ManagerReportReviewPage.tsx`):**
  - `FlightOperationsReportView` in the audit stage is rendered only when `auditFieldSessionId` is non-null.

### Docs to Update in Combined Pass
- **Report 6 User Guides** (`01-user-guides.md`) / **Report 7** (§ User Guides): minor UI alignment if screenshots or inline banner descriptions are referenced (no functional requirement or API contract change).

---

## 4. `FE-24` — Remove Re-inspection Info Alert Banner from Inspection Workspace

**Date:** 2026-11-23
**Status:** Code change applied in `SmartDroneInspection-frontend` (`InspectionDetailPage.tsx`); docs not yet edited.

### Behavioral & Contract Summary
- **Backend (`InspectionResponse.java`, `InspectionCreationService.java`, `InspectionController.java`, `InspectionCreationApiIntegrationTest.java`):**
  - Added `inspectorAvatarUrl`, `ownerCustomerAvatarUrl`, `managerAvatarUrl`, and `assetPhotoDocumentIds` to `InspectionResponse` (fixing `managerUser` resolution so it does not use `flightPermitVerifiedBy` after inspector self-attestation, and eagerly fetching asset `documents` via `findAssetForResponse` -> `assets.findDetailedById`).
  - Added `GET /api/v1/inspections/{inspectionId}/asset-photos/{documentId}/content` scoped to inspection participants (`INSPECTOR` assigned, owning `CUSTOMER`, `MANAGER`, `ADMIN`) so all roles can view asset photos without widening `/api/v1/assets/**` role scope.
  - Added `InspectionCreationApiIntegrationTest#inspectionDetailExposesParticipantAvatarsAndAssetPhotosAcrossRoles` verifying avatars and asset photo bytes across `INSPECTOR`, `CUSTOMER`, and `MANAGER` roles.
- **Frontend (`InspectionDetailPage.tsx`, `InspectionContextDialogs.tsx`, `InspectionOverviewDetails.tsx`, `OverviewStakeholdersSection.tsx`, `inspectionApi.ts`, `viCatalog.ts`):**
  - Removed the `RE_INSPECTION` info `<Alert>` banner (`"This mission verifies the original repair outcome..."`) from the inspection workspace header (`Re-inspection · #<id>` chip remains visible).
  - Made the header Asset title clickable (with real asset photo thumbnail when present, no placeholder icon box) to open an Asset Detail dialog (real asset photo gallery when uploaded, location, copyable coordinates, Google Maps link, airspace classification + matching zone, planned schedule, assigned drone, permit summary, and interactive site map; target checkpoints list omitted), and made `Customer` / `Manager` / `Inspector` summary values clickable with real user avatars (`ownerCustomerAvatarUrl`, `managerAvatarUrl`, `inspectorAvatarUrl`; removed hardcoded SVG portrait placeholders in `OverviewStakeholdersSection.tsx`) to open contact detail dialogs (avatar, name, copyable phone/email, asset context, and Messages link; removed role `<Chip>` tag inside the detail popups).
  - Removed the duplicated `InspectionOverviewDetails` panel and `inspection-evidence-trace` (`Captures` / `Confirmed findings` / `Report`) summary from the `Overview` collapse in `InspectionDetailPage.tsx` (now `Overview` only appears when role-specific payout or stakeholder cards apply).

### Docs to Update in Combined Pass
- **Report 6 User Guides** (`01-user-guides.md`): minor UI/screenshot alignment if the re-inspection info banner is shown.

---

## 5. Mobile Localization Formatting (`SmartDroneInspection-mobile`)

**Date:** 2026-11-23
**Status:** Pre-existing working-tree formatting/lint updates in `lib/l10n/app_localizations*.dart`; no functional flight-permit changes needed (mobile is Customer-only and has no permit review workflow).

---

## 6. Cross-Repo Stale Role & Organization Cleanup

**Date:** 2026-11-23
**Status:** Applied and verified across `AGENTS.md`, `SmartDroneInspection-backend`, `SmartDroneInspection-frontend`, `SmartDroneInspection-mobile`, and `SmartDroneInspection-docs/_index.md`.

### Summary
- Enforced strictly 4 human login roles (`ADMIN`, `MANAGER`, `CUSTOMER`, `INSPECTOR`) with direct Customer ownership (`ownerCustomerId = user.id`; no separate Organization entity or hierarchy) across `Roles.java`, `UserRole.java`, `UserAccess.java`, `Mf2ActorPolicy.java`, frontend `authStore.ts`, mobile `user_role.dart` / `auth_user.dart`, UI labels, and localization catalogs (`messages_vi.properties`, `viCatalog.ts`, `app_en.arb`, `app_vi.arb`).
- Replaced stale `"Platform Manager"` / `"Organization Manager"` / `"Quản lý nền tảng"` / `"Quản lý tổ chức"` UI strings and comments with `"Manager"` / `"Customer"` / `"Quản lý"` / `"Khách hàng"` (preserving wire DTO keys `organizationName`/`organizationCode` on `/customer-registrations` for DB compatibility).

### Remaining Docs & Diagrams to Update in Combined Pass
- Report 3 SRS, Report 4 SDD, Report 5 Test Report, Report 6 User Guides, Report 7, and `.drawio` diagrams: sweep any remaining references to `Organization` hierarchy, `ORG_MANAGER`, `ORG_ADMIN`, `PLATFORM_MANAGER`, or `MAINTENANCE_ENGINEER` so only the 4 active roles and direct Customer ownership appear.

---

## 7. Inspector Rating & Evaluation System (Customer & Manager)

**Date:** 2026-11-23
**Status:** Implemented across Backend (`V70__inspector_ratings.sql`), Web Frontend, and Customer-only Mobile Flutter app.

### Behavioral & Contract Summary
- **Database (`V70__inspector_ratings.sql`):** Added `inspector_ratings` table (`unique (inspection_id, rater_role)`, `rater_role IN ('CUSTOMER', 'MANAGER')`, `overall_score 1..5`, `criterion_scores jsonb`, `comment text`).
- **Business Rules (`InspectorRating`, `InspectionRatingService`, `InspectorRatingController`):**
  - Open only when `inspection.status == COMPLETED` and `inspectorId != null`.
  - Max 1 rating per `(inspection_id, rater_role)`. Owning `CUSTOMER` evaluates `evidenceQuality`, `communication`, `professionalism`; active `MANAGER` evaluates `sopAndSafety`, `technicalAccuracy`, `timeliness`; `ADMIN` has read-only access; `INSPECTOR` sees received ratings on their own inspections/dashboard.
  - Editable within **7 days** of `created_at` (`409 RATING_EDIT_WINDOW_EXPIRED` afterwards).
  - Endpoints: `GET/PUT /api/v1/inspections/{inspectionId}/inspector-rating`, `GET /api/v1/inspectors/{inspectorId}/ratings`, `GET /api/v1/inspectors/me/ratings`.
  - Privacy: `CUSTOMER` profile lookup receives aggregate summary only (`historyVisible = false`, no comments from other Customers).
- **SPI, Inspection DTO & Notifications:**
  - Extended `PartnerReliabilityQuery.ReliabilityCounts` & `PartnerCandidateResponse` (`averageRating`, `ratingCount`, `customerAverageRating`, `managerAverageRating`) and `InspectionResponse` (`inspectorAverageRating`, `inspectorRatingCount`).
  - Added `InspectorRatedEvent` -> `InspectionNotificationListener.onInspectorRated` -> `INSPECTOR_RATED` in-app notification for the Inspector.
- **Web Frontend & Customer Mobile:**
  - Web: concise `InspectorRatingPromptCard` + `InspectorRatingDialog` on `CustomerReportDeliverablePage` and `ManagerReportReviewPage`, `InspectorRatingSummaryBadge` in `PartnerCandidateResults` & `InspectionContextDialogs`, Ratings tab in `InspectorProfileDialog`, and `Ratings & Reviews` section in `InspectorDashboardPage`.
  - Mobile (`SmartDroneInspection-mobile` — Customer-only): added `InspectorRating` model/provider/repository methods, star badge beside Inspector in `_TrackingTab`, and compact `CustomerInspectorRatingCard` + bottom-sheet form in `_SettlementTab`.

### Docs & Diagrams to Update in Combined Pass
- Report 3 SRS (`03-functional-requirements.md`, `00-record-of-changes.md`): add Inspector Rating & Evaluation feature requirements and authorization matrix.
- Report 4 SDD (`02-database-design.md`, `03-detailed-design.md`): add `inspector_ratings` table schema, `InspectorRatingController`, `InspectionRatingService`, `InspectorRatedEvent`, and extended `PartnerReliabilityQuery` / `InspectionResponse`.
- Report 5 Test Report (`01-test-cases/`, `02-test-execution/`): add test cases & executed results for `InspectorRatingTest`, `InspectionRatingServiceTest`, `InspectorRatingApiIntegrationTest`, Frontend Vitest, and Mobile Flutter tests.
- Report 6 User Guides & Report 7 & Diagrams (`smartdrone-er-diagrams.drawio`, `smartdrone-sequence-diagrams.drawio`, `smartdrone-class-diagrams.drawio`, `smartdrone-use-case-diagrams.drawio`): add rating workflows and `inspector_ratings` entity/endpoints.
