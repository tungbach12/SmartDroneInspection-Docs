---
title: "Role and Admin Authority Review"
type: "docs"
---

# Role and Admin Authority Review

**Status:** Accepted · **Accepted:** 19 November 2026 · **Implemented:** 19 November 2026
**Scope:** Admin workspace navigation (`/admin`), the capabilities behind it, and every capability that
could let a platform account exceed its business accountability.
**Non-goal:** This document does not change code. It is the Step 1 gap register and decision input.

## 1. Purpose

The question under review is whether `ADMIN` holds more authority than the product needs. The answer
cannot come from the navigation alone: the frontend route table and the backend service layer disagree in
several places. This document records what is actually enforced today, where enforcement and
documentation diverge, and which decisions must be made before any code is changed.

## 2. Method and evidence

Reviewed sources:

- `SmartDroneInspection-frontend/src/app/permissions/accessPolicy.ts` — portal/section role matrix.
- `SmartDroneInspection-frontend/src/app/router/router.tsx` — route-level role gates.
- `SmartDroneInspection-frontend/src/app/layouts/AppShell.tsx` — the admin navigation in the screenshot.
- `SmartDroneInspection-frontend/src/features/admin/**` — accounts, onboarding review, finance, license
  classes, AI configuration, inspector profile dialog.
- `SmartDroneInspection-backend/src/main/java/**/api/*Controller.java` — transport-level `@PreAuthorize`.
- The owning service classes — the effective actor scope (`Mf2ActorPolicy`, `AssetService`,
  `ContractWorkflowService`, `AdminUserService`, `InspectorProfileService`, `PlatformAiSettingsService`).
- Report 3 SRS sections 3.2–3.9 and the workspace `AGENTS.md`.

Effective permission = the narrower of the controller annotation and the service-level actor check.
A controller that admits `ADMIN` but whose service rejects `ADMIN` grants nothing; it only produces a
misleading UI.

## 3. Source-of-truth policy

Neither the SRS nor the code is automatically correct. The working rule for authorization is:

> A role may perform an action only when it is accountable for the outcome of that action. Platform
> administration is not a substitute for customer, inspector, or manager accountability.

When the SRS and the code disagree, classify the divergence and resolve it deliberately:

| Class | Meaning | Required action |
| --- | --- | --- |
| A | Code is wrong | Fix code, add a negative-scope test, keep SRS |
| B | SRS is stale | Fix the SRS section and append `00-record-of-changes.md`; keep code |
| C | Both are incomplete | Record the decision here, then update code and SRS together |

The SRS is internally inconsistent today, which is direct evidence for class B. `SmartDroneInspection-docs/_index.md`
and the workspace `AGENTS.md` describe **five** login roles including `MAINTENANCE_ENGINEER`, while
`report-3-software-requirement-specification/_index.md` still says **four** roles and six features, and the
backend `UserRole` enum contains only four roles. See G-07 and G-08.

## 4. As-built access surface

### 4.1 Portal and section access (frontend)

Source: `accessPolicy.ts` lines 130–200, `router.tsx` lines 190–343.

| Section | `/admin` | `/manager` | `/client` | `/operations` |
| --- | --- | --- | --- | --- |
| Dashboard | ADMIN | MANAGER | CUSTOMER | INSPECTOR |
| Service requests | ADMIN (read-only registry) | MANAGER | CUSTOMER | — |
| Assets | ADMIN | MANAGER | CUSTOMER | — |
| Inspections | ADMIN | MANAGER | CUSTOMER | INSPECTOR |
| Reports | ADMIN | MANAGER | CUSTOMER | INSPECTOR |
| Asset catalog | ADMIN | — | — | — |
| Onboarding reviews | ADMIN | MANAGER | — | — |
| Platform accounts | ADMIN | MANAGER (inspectors only) | — | — |
| Finance settings | ADMIN | — | — | — |
| UAV license classes | ADMIN | — | — | — |
| AI configuration (`/admin/ai-settings`) | ADMIN | — | — | — |
| Notifications | ADMIN | MANAGER | CUSTOMER | INSPECTOR |
| Settings | all four roles | | | |

The admin inspection workspace additionally exposes `permit`, `pre-flight`, `field-session`,
`post-flight`, `audit`, `review`, and `settlement` child routes to `ADMIN` and `MANAGER`
(`router.tsx` lines 228–298). Several of those pages render actions the service layer will reject.

### 4.2 Capability matrix (effective enforcement)

| # | Capability | ADMIN | MANAGER | CUSTOMER | INSPECTOR | Enforced by | Evidence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | List platform accounts | Yes (all) | Yes (Inspectors only) | No | No | controller + service | `PlatformUserController` 34, 43; `AdminUserService.list` |
| 2 | Create account | Any of 4 roles | Inspector only | No | No | controller + service | `PlatformUserController` 48–68 |
| 3 | Reset password / change roles / change status | Yes (not self) | No | No | No | controller + service | `PlatformUserController` 81–129, `AdminUserService` 176–184 |
| 4 | Review Inspector applications, approve/reject, upload signed contract | Yes | Yes | No | No (public self-apply only) | controller | `InspectorApplicationController` 57–141 |
| 5 | Review drone registrations | Yes | Yes | No | Own registrations only | controller | `DroneRegistrationApplicationController` 155–184 |
| 6 | Review customer airspace cases | Yes | No | No | No | controller | `AirspaceReviewController` 23–24 |
| 7 | View/edit Inspector profile, license scan, partner contract | Yes | Yes | No | Own profile | controller + service | `InspectorProfileController` 43–160, 202–211 |
| 8 | Record / delete Inspector flight logs | Yes | Yes | No | No | controller | `InspectorProfileController` 171–187 |
| 9 | Approve/reject Inspector onboarding | Yes | Yes | No | No | controller | `InspectorProfileController` 144–160 |
| 10 | Asset category catalog | Read + write | Read | Read | Read | controller | `AssetCatalogController` 38–58 |
| 10a | Checklist templates (default checkpoints) | Read + write | Read | Read | Read | controller | `AssetCatalogController` 66–86 |
| 11 | Asset records list/read (platform-wide) | Yes | Yes | Own organization | No | service | `AssetService.list/get` |
| 12 | Asset create / update / retire | No | No | Yes (owner) | No | controller | `AssetController` 38–91 |
| 13 | Edit asset inspection checkpoints | No | No | Yes, owning organization, before first inspection | No | controller + service | `AssetController` 81; `AssetService` 191–235; `AssetsPage.tsx` 1438, 2400 |
| 14 | Service request list/detail | Assignment registry only, redacted | Own queue | Own organization | No | service | `ContractWorkflowService` 425–470 |
| 15 | Claim request, quote, dispatch occurrence | No | Yes (assigned) | No | No | service | `ContractWorkflowService` |
| 16 | Reassign / unassign request manager | Yes | No | No | No | service | `ContractWorkflowService` 2894, 2904, 2949 |
| 17 | Read/post order chat, download attachments | No (explicitly forbidden) | Assigned only | Own organization | No | service | `ContractWorkflowService` 677–690, 798–810, 1050–1065 |
| 18 | Read signed contract | No (explicitly forbidden) | Assigned only | Own organization | No | service | `ContractWorkflowService` 1126–1140 |
| 19 | Upload flight permit | No | No | No | Assigned inspector only | controller + service | `InspectionController` 194–249; `InspectionCreationService.uploadFlightPermit` |
| 19a | Review/verify flight permit | Yes, not the uploader | Yes, not the uploader | No | No | controller + service | `InspectionController` 251–263; `InspectionCreationService.reviewFlightPermit` |
| 20 | Start / complete / abort field session | No | No | No | Yes | controller | `InspectionFieldSessionController` 57–183, 252 |
| 21 | Upload evidence, confirm findings baseline | No | No | No | Yes | controller | `InspectionController` 403–500, 547–668 |
| 22 | Draft / submit / withdraw report | No | No | No | Yes | controller | `InspectionController` 710–751 |
| 23 | Review and publish report | Yes (not author) | Yes (not author) | No | No | controller + service | `InspectionController` 763, SRS BR-38 |
| 24 | Accept published report | No — service requires CUSTOMER | Service requires CUSTOMER | Yes (owner) | No | service | `ContractWorkflowService` 1314–1320 |
| 24a | Request report clarification | No | No | Owning customer | No | controller + service | `InspectionController` clarification; `ReportService.requireOwningCustomer` |
| 25 | Create PayOS payment link | No — explicit `forbidden()` | Assigned only | Own organization | No | service | `ContractWorkflowService` 1856–1868 |
| 26 | Confirm manual payment | No | Assigned only | No | No | service | `ContractWorkflowService` 1356–1361 |
| 27 | Record Inspector payout, refunds, receivables | No | Assigned only | No | No | service | `ContractWorkflowService` 1609–1612 |
| 28 | Finance settings read/write | Yes | No | No | No | controller | `InspectionFinanceSettingsController` 29, 36 |
| 29 | AI settings read / write | Read + write | Read | No | Read | controller | `PlatformAiSettingsController` 29, 35 |
| 30 | Pilot license classes read / write | Read + write | Read | Read | Read | controller | `PilotLicenseClassController` 33–60 |
| 31 | Drone document and feature configuration read / write | Read + write | Read | Read | Read | controller | `DroneDocumentConfigController`, `DroneFeatureConfigController` |
| 32 | Review platform activity history | Read-only | No | No | No | controller + service | `AdminAuditLogController`, `AdminAuditLogService` |
| 33 | Upload asset documents | No | No | Owning organization | No | controller + service | `AssetDocumentController` upload; `AssetDocumentService.requireOwnedAssetForWrite` |
| 34 | Create re-inspection | No | Yes | Owning organization | No | controller + service | `InspectionController` 1055–1064; `InspectionCreationService.createQuickReinspection` |
| 35 | Update re-inspection verification | No | No | No | Assigned inspector only | controller + service | `InspectionController` 1076–1092; `ReinspectionVerificationService.requireCanEdit` |

**Reading the matrix:** the backend already stops `ADMIN` from acting as Inspector, Customer, or
assigned Manager in most workflows. The admin role is not a general superuser. Onboarding review, report
review, and platform configuration (rows 4–6, 9, 23, 28, 30–31) are intended `ADMIN` powers per the SRS.
The concrete gaps are G-01 to G-14 in section 5; all are resolved as of 19 November 2026.

## 5. Gap register

Severity: **S1** confidentiality/availability, **S2** decision integrity, **S3** consistency/UX,
**S4** documentation. Class follows section 3.

| ID | Sev | Gap | Evidence | Class | Recommended resolution |
| --- | --- | --- | --- | --- | --- |
| G-01 | S1 | `MANAGER` receives every platform account from `GET /platform/users`, including `ADMIN` and `CUSTOMER` emails and roles. The UI filters to Inspectors, but the API does not. | `PlatformUserController` 34, 43–46; `PlatformUsersPage.tsx` 91–94 | A | Scope the service by caller role: pure Manager sees Inspector accounts only. Add a negative-scope test. |
| G-02 | S2 | `ADMIN` and `MANAGER` can rewrite an asset's inspection checkpoints at any time, including after inspections and published reports. This contradicts "a by-category change does not retroactively rewrite checkpoints already captured". | `AssetController` 81–87; `AssetService` 191–227; `AssetsPage.tsx` 1438, 2400; SRS §3.4.1 | C | Decide the owner. Recommended: Customer only, before the first inspection; after that, a new checkpoint set requires a new request. If Admin break-glass is required, it must be attributed and audited and must not mutate historical reports. |
| G-03 | S2 | AI "apply to pending" retroactively marks matching `PENDING` model findings `CONFIRMED` across every inspection in one write. This bypasses Inspector baseline confirmation and is not scoped to an inspection. | `PlatformAiSettingsService` 112–130; `AdminAiModelAnalyticsPanel.tsx` 46–82, 196–210 | C | Decide whether retroactive confirmation is a product feature. If kept: scope by inspection, record per-finding attribution, and add an SRS rule. If not: remove `applyToPending` and confirm only new detections. |
| G-04 | S2 | Inspector licence number, class, expiry, flight hours, certified models, and flight-log deletions are mutable by `ADMIN`/`MANAGER` with no security-audit event. These fields drive dispatch eligibility and legal compliance. | `InspectorProfileService` 83–150, 270–303 (no audit call); `InspectorProfileController` 58–187 | A | Record `SecurityAuditService` events for profile and flight-log mutations, including actor, target, field set, and reason. Consider requiring a reason for licence-field changes. |
| G-05 | S1 | No last-admin guard. Any Admin can demote, suspend, or disable the final remaining Admin; only self-modification is blocked. | `AdminUserService` 119–184; `RolePolicy` requires exactly one role | A | Reject role/status changes that would leave zero active `ADMIN` accounts. Add a test for the final-admin case. |
| G-06 | S3 | Route and controller gates are broader than the service. `/admin/inspections/:id/settlement` and report acceptance render Admin actions that return `403`; Admin field-session pages render Inspector controls that return `403`. | `router.tsx` 228–298; `InspectionController` 777–814; `ContractWorkflowService` 1314, 1860 | A | Align the frontend capability model with the service, or render an explicit read-only oversight mode. Keep the service as the final authority. |
| G-07 | S4 | The workspace `AGENTS.md` and the docs home claim five login roles including `MAINTENANCE_ENGINEER`; the backend enum, JWT role constants, and account administration support four. A database test explicitly asserts the role is absent, and Report 3 §3.2.2 is titled "Account Management and Four-Role Access". | `SmartDroneInspection-docs/_index.md` 16, 24; backend `UserRole.java`; `V25TargetSchemaFoundationTest` 316; SRS §3.2.2 | B | Either implement the fifth role end to end or remove it from the target documents. Do not leave the 5-role claim in onboarding material. |
| G-08 | S4 | Report 3 `_index.md` still states four roles, six features, and `MF1–MF3`, while the functional requirements define eight features (`FE-01`–`FE-08`) and `MF1–MF4` on four login roles. | `report-3-software-requirement-specification/_index.md` 9 vs `03-functional-requirements.md` §3.2.2 and §3.1 | B | Refresh the Report 3 index and append a change record. |
| G-09 | S4 | Finance settings and AI settings changes store `updated_by` but emit no activity event; the SRS promises that Admin "reviews platform activity history", and no such page or endpoint exists. | `PlatformAiSettingsService` 91–110; `InspectionFinanceSettingsService` 47–56; no audit read endpoint | C | Decide whether an activity viewer is in scope. If yes, add a read-only endpoint and page. If no, narrow the SRS wording. |
| G-10 | S2 | A `MANAGER` or `ADMIN` can upload a flight permit and then verify it themselves. Review only rejects the assigned Inspector, not the uploader. `CUSTOMER` may also upload a permit, which the SRS does not allow. | `InspectionCreationService` 497–506, 614–640; `InspectionController` 194–263; SRS §3.6.1 | A | Require reviewer ≠ uploader for every role, and restrict upload to the assigned Inspector. Add negative tests for self-upload-then-approve and customer upload. |
| G-11 | S3 | Checklist templates that feed asset checkpoint defaults can be created, updated, and deleted by `MANAGER`; the SRS assigns catalogue maintenance to `ADMIN`. | `AssetCatalogController` 66–86; SRS §3.4.1 | C | Confirm whether Managers need template ownership operationally. If not, restrict writes to Admin; if yes, record it in the SRS. |
| G-12 | S1 | `ADMIN` could upload asset documents through `POST /api/v1/assets/{assetId}/documents`; evidence attached to a customer asset must be customer-owned. | `AssetDocumentController` upload annotation; `AssetDocumentService.requireOwnedAsset` | A | Restrict upload to the owning `CUSTOMER`; keep `ADMIN`/`MANAGER` read-only through list and download. |
| G-13 | S2 | `ADMIN`/`MANAGER` could edit re-inspection defect verifications, and `ADMIN` could create a quick re-inspection. The field verdict belongs to the assigned Inspector; the request belongs to the customer/manager. | `ReinspectionVerificationService.requireCanEdit`; `InspectionCreationService.createQuickReinspection` | A | Restrict verification edits to the assigned `INSPECTOR`; restrict creation to the owning `CUSTOMER` or a platform `MANAGER`. |
| G-14 | S2 | `ADMIN`/`MANAGER` could request customer clarification on a published report; the clarification request is a customer acceptance-side action. | `InspectionController` clarification annotation; `ReportService.requestCustomerClarification` | A | Restrict to the owning `CUSTOMER`, matching report acceptance. Pending coordination because `ReportService.java` is being edited by another worker. |

### Accepted risks (no change proposed)

- **Any Admin may reset another Admin's password** (not self). At this project size this is the
  documented break-glass path; it is audited as `USER_PASSWORD_RESET`. Revisit if the platform gains
  independent platform operators.
- **Admin reads all customer assets, requests, and inspections.** This is read-only oversight and is
  consistent with the SRS "Query All Data" scope for platform roles.
- **Admin reviews onboarding and reports created by others.** The SRS explicitly permits `ADMIN` as
  reviewer; the separation rule is reviewer ≠ author, and `ADMIN` cannot author a report. Flight-permit
  upload/review separation is a separate gap, recorded as G-10.

### 5.1 Resolution status (19 November 2026)

| Gap | Status | Implemented behaviour |
| --- | --- | --- |
| G-01 | Resolved | `GET /platform/users` returns Inspectors only to a pure `MANAGER`; `ADMIN` still sees the full directory. |
| G-02 | Resolved | Checkpoint writes are `CUSTOMER`-only and return `INSPECTION_HISTORY_EXISTS` once any inspection exists for the asset. |
| G-03 | Resolved | `applyToPending` removed from the request, service, and UI. Threshold changes affect new detections only and emit `AI_SETTINGS_UPDATED`. |
| G-04 | Resolved | Inspector profile, licence-scan, partner-contract, onboarding, flight-log record, and flight-log delete operations emit audit events. |
| G-05 | Resolved | Role/status changes that would leave zero active `ADMIN` accounts are rejected with `LAST_ADMIN_REQUIRED`. |
| G-06 | Resolved | Admin no longer gets customer settlement or Inspector field-session stages; those pages and routes are scoped to the accountable portal. |
| G-07 | Resolved (docs) | Workspace documents align on four implemented login roles; `MAINTENANCE_ENGINEER` and corrective-maintenance MF4 are marked planned/out of current release scope. |
| G-08 | Resolved (docs) | Report 3 index refreshed to eight features and `MF1`–`MF4` on four login roles. |
| G-09 | Resolved | Read-only `GET /api/v1/admin/audit-logs` and the `/admin/audit-logs` Activity log page are available to `ADMIN`. |
| G-10 | Resolved | Flight permit upload is assigned-`INSPECTOR` only; the uploader cannot verify the same permit. |
| G-11 | Resolved | Checklist template writes are `ADMIN`-only. |
| G-12 | Resolved | Asset document upload is owning-`CUSTOMER` only; platform staff keep read access. |
| G-13 | Resolved | Re-inspection verification edits are assigned-`INSPECTOR` only; quick re-inspection creation is `CUSTOMER`/`MANAGER` only. |
| G-14 | Resolved | Report clarification (request revision) is owning-`CUSTOMER` only; `ADMIN`, `MANAGER`, and `INSPECTOR` receive `403`, and a customer from another organization is denied. |

Verification evidence is recorded in the backend and frontend test runs; see the handoff for the exact
commands and results.

## 6. Accepted decisions

Accepted on 19 November 2026. The Step 2 implementation followed these choices.| # | Decision | Options | Recommendation |
| --- | --- | --- | --- |
| D-01 | Who may edit asset inspection checkpoints after the first inspection exists? | (a) Admin/Manager any time; (b) Customer only before first inspection; (c) new checkpoint set through a new request | (b) plus (c) |
| D-02 | Keep the AI retroactive `applyToPending`? | (a) keep platform-wide; (b) keep but scope per inspection + attribution; (c) remove | (c), or (b) if required for the demo |
| D-03 | Is an Admin activity/audit viewer in scope? | (a) add read-only page; (b) remove the SRS claim | (a) is the smaller long-term risk; (b) is acceptable for the current milestone if recorded |
| D-04 | Is `MAINTENANCE_ENGINEER` a real target role? | (a) implement end to end; (b) remove from `AGENTS.md` and docs home | (b) for the current scope, unless the maintenance flow is being built now |
| D-05 | Should pure `MANAGER` list only Inspectors? | (a) yes, enforce in service; (b) keep visibility of all accounts | (a) |
| D-06 | Who may upload a flight permit, and can the uploader verify it? | (a) assigned Inspector uploads, distinct Manager/Admin verifies; (b) keep Manager/Admin/Customer upload but forbid self-verification | (a) per SRS §3.6.1 |

## 7. Implemented target matrix

The accepted decisions are reflected in the current implementation:

| Capability | Today | Target |
| --- | --- | --- |
| Platform account list | Manager sees all | Manager sees Inspectors only |
| Asset checkpoint edit | Admin/Manager any time | Customer before first inspection; later changes via new request |
| Checklist template ownership | Admin + Manager write | Follow the D-01 ownership decision |
| AI auto-confirm | Retroactive platform-wide | New detections only; threshold changes audited |
| Inspector profile / flight log mutation | No audit event | Security-audit event with actor and field set |
| Flight permit upload/verify | Uploader can self-verify; Customer can upload | Assigned Inspector uploads; distinct Manager/Admin verifies |
| Asset document upload | Customer or Admin | Owning Customer only |
| Re-inspection verification edit | Inspector, Manager, or Admin | Assigned Inspector only |
| Re-inspection creation | Customer, Manager, or Admin | Owning Customer or Manager |
| Final Admin demotion/suspension | Allowed | Rejected |
| Admin business-stage UI | Renders actions that 403 | Read-only oversight mode or hidden actions |
| Activity history | Absent | Read-only Admin page backed by the existing audit table |
| Role model in docs | 5 claimed, 4 implemented | One consistent number in `AGENTS.md`, docs home, and SRS |

## 8. Next steps

1. ~~Resolve D-01 to D-06 and mark this document `Accepted`.~~ Done 19 November 2026.
2. ~~Implement the accepted S1/S2 items with targeted tests.~~ Done; see §5.1.
3. ~~Align frontend capabilities with the server, keeping the server as the authority.~~ Done.
4. ~~Complete G-14 in `ReportService.java` once the concurrent notification edit releases the file.~~ Done 19 November 2026.
5. Update Report 5 evidence for the new negative-scope tests (Report 3 role/feature alignment is applied).
