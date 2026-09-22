---
title: "Plan - Align Report 2 with Current Roles and Business Flows"
type: "agent-plan"
status: "ready"
updated: 2026-09-21
---

# Plan: Align Report 2 with the Current Product Contract

## 1. Objective

Update Report 2 - Project Management Plan so its scope, WBS, effort narrative, risk register, deliverables, responsibility matrix, and DOCX/Markdown versions match the current SmartDroneInspection roles and WF1-WF4 business flows.

This file is standalone so another AI agent can execute Report 2 without relying on chat history.

## 2. Repository and working protocol

Target repository:

~~~text
E:\Dev\Repos\Capstone\docs
~~~

Before editing:

1. Read E:\Dev\Repos\Capstone\AGENTS.md.
2. Read content/development/ai-agent-rules.md.
3. Read content/development/git-and-pull-requests.md.
4. Run git status --short and preserve unrelated work.
5. Create a normal branch, for example:
   docs/update-report2-current-flow
6. Do not use a worktree.
7. Do not commit to main.
8. Do not commit, push, create a PR, or merge unless explicitly authorized.

## 3. Files in scope

~~~text
content/project-reference/reports/report-2-project-management-plan/report2-project-management-plan.md
content/project-reference/reports/report-2-project-management-plan/report2-project-management-plan.docx
~~~

Report 1 and Report 3 are read-only references for this task. Do not edit them.

## 4. Source of truth

Read before editing:

1. content/project-reference/reports/report-3-software-requirement-specification/
2. content/project-reference/workflows/business-flows.md
3. content/project-reference/reports/report-2-project-management-plan/report2-project-management-plan.md
4. content/project-reference/reports/report-2-project-management-plan/report2-project-management-plan.docx
5. README.md
6. E:\Dev\Repos\Capstone\AGENTS.md

Report 3 and business-flows.md override stale statements in Report 2. Do not invent behavior, roles, payment gates, or features not supported by these sources.

## 5. Current product roles

Use exactly these five human product roles wherever Report 2 describes product behavior:

| Human-readable role | Backend code | Responsibility boundary |
| --- | --- | --- |
| Admin | ADMIN | Platform organizations, users, roles, categories, checklists, and configuration. Not automatically a customer or service-workflow actor. |
| Client | CLIENT | Customer organization assets, schedules, inspection requests, quotation/order decisions, released results, maintenance tickets, and customer decisions. |
| Service Manager | SERVICE_MANAGER | Service request review, quotations, service orders, assignment, capacity, result verification, and result release. |
| Inspector | INSPECTOR | Assigned inspection execution, evidence, AI candidate verification, report authoring, and assigned peer review. Author and reviewer must be different users. |
| Maintenance Engineer | MAINTENANCE_ENGINEER | Assigned technical assessment and maintenance execution, work logs, completion data, and before/after evidence. |

Use human-readable names in management-plan prose and WBS. Use uppercase codes only for technical examples or authorization matrices.

### Terminology migration rules

| Legacy wording | Required handling |
| --- | --- |
| Administrator / Platform Administrator | Admin |
| Organization Manager / Customer Manager | Client |
| Manager | Client for customer responsibilities; Service Manager for provider responsibilities |
| Viewer | Remove from current role model |
| Inspector Author / Inspector Peer Reviewer | Inspector responsibilities, not new roles |
| SmartDroneHub | Remove; no separate drone-operation platform is part of the product |
| System, MinIO, YOLO Service | System/external actors, not human project roles |

Do not blindly replace Manager. Use the WBS function and workflow lane to determine Client versus Service Manager. Historical change-log entries may retain old wording only when clearly historical.

## 6. Current business-flow baseline

### WF1 - Asset Registration and Periodic Inspection Scheduling

- Client manages organization assets and recurring schedules.
- Admin configures categories and checklist templates.
- System generates one PERIODIC request per Asset + Schedule + Due Cycle.
- Duplicate due-cycle requests are prohibited.

### WF2 - Inspection Request Review, Service Order and Inspector Assignment

- Client creates AD_HOC requests or completes PERIODIC requests.
- Service Manager reviews scope and capacity, then prepares versioned quotation/order.
- Client approves or requests revision.
- No upfront payment is required; Client approves post-service payment terms.
- Service Manager confirms the order and assigns an Inspector.
- Inspector accepts or rejects; rejection returns to Service Manager for reassignment.

### WF3 - Inspection Execution, AI-Assisted Verification and Report Delivery

- Inspector works only on assigned inspections.
- Inspector captures/uploads evidence and completes the checklist.
- YOLO produces candidates; Inspector Confirm, Modify, Reject, or Manual Add determines official findings.
- Only verified findings enter reports/statistics.
- Inspector authors and submits a report for peer review.
- An Inspector cannot peer-review their own report.
- Service Manager assigns a different Inspector and releases the approved result.
- Client accepts or requests clarification/revision.
- Accepted versions are immutable.

### WF4 - Maintenance Assessment, Work Execution and Defect Resolution

- Client creates a maintenance ticket from verified defects.
- Service Manager assigns a Maintenance Engineer for technical assessment.
- Maintenance Engineer provides technical scope and estimate.
- Service Manager prepares and confirms a versioned maintenance order.
- Client approves scope and post-service payment terms.
- Service Manager assigns execution.
- Maintenance Engineer performs work and uploads before/after evidence.
- Service Manager verifies/releases the result.
- Client accepts, requests rework, or requests re-inspection.
- Re-inspection returns through a linked AD_HOC request to WF2.
- No upfront payment is required.

## 7. Detailed execution steps

### Step 1 - Baseline audit

1. Read every Report 2 heading, WBS row, estimate, risk, deliverable, responsibility row, communication item, and configuration statement.
2. Search Markdown and DOCX for:
   Viewer, Administrator, Platform Administrator, Organization Manager, Customer Manager, SmartDroneHub, and ambiguous Manager.
3. Identify all references to product roles versus team roles such as Leader and Member.
4. Compare every conflict against Report 3 and business-flows.md.
5. Record intended changes before editing.

### Step 2 - Update scope, objectives, and risks

Update the existing sections without changing their official order or table structure.

Scope must describe:

- A B2B infrastructure inspection service platform.
- Assets and recurring schedules.
- Periodic and ad-hoc requests.
- Quotation and service-order confirmation.
- Inspector assignment and field evidence.
- YOLO-assisted candidate detection with mandatory human verification.
- Versioned report review and release.
- Maintenance assessment, execution, evidence, and resolution.
- No autonomous drone piloting.
- No separate SmartDroneHub dependency.
- No upfront payment; post-service payment terms are approved by Client.

Objectives and quality targets must not promise unsupported features, real payment settlement, autonomous flight, or full enterprise CMMS.

Risks must remain aligned with the current product boundary. Keep valid existing risks, but correct any role, payment, drone-platform, or workflow assumptions that are stale.

### Step 3 - Align FE-01 through FE-08 WBS

Preserve the current feature identifiers and effort model unless the source documents prove an existing value is wrong. The current total is 135 man-days; do not change it merely for terminology cleanup.

Expected feature alignment:

#### FE-01 - Identity and Access Governance

- Covers authentication and authorization for Admin, Client, Service Manager, Inspector, and Maintenance Engineer.
- Includes organization, ownership, assignment, and separation-of-duties scope.
- Does not include Viewer.

#### FE-02 - Asset Registry and Inspection Schedule

- Client owns customer-organization asset and schedule actions.
- Admin maintains categories and checklist templates.
- System generates idempotent due-cycle requests.

#### FE-03 - Inspection Request and Work Assignment

- Client creates/completes requests and approves quotations/orders.
- Service Manager reviews, quotes, confirms orders, and assigns Inspector.
- Inspector accepts/rejects assignment.
- No upfront payment gate; post-service payment terms are approved.

#### FE-04 - Inspection Execution and Evidence Management

- Inspector executes assigned inspections.
- Evidence upload/retry, metadata, MinIO storage, and assignment scope are included.
- Mobile is the field-work client for Inspector.

#### FE-05 - YOLO-Assisted Defect Detection and Verification

- YOLO creates candidates with label, confidence, bounding box, and model version.
- Inspector Confirm, Modify, Reject, or Manual Add determines official findings.
- Unverified candidates are excluded from official statistics.

#### FE-06 - Inspection Report and Approval

- Inspector authors a versioned report.
- A different Inspector performs peer review.
- Service Manager verifies deliverables and releases the result.
- Client accepts or requests clarification/revision.
- Accepted versions are immutable.

#### FE-07 - Maintenance and Defect Resolution

- Client creates maintenance tickets from verified defects.
- Service Manager plans assessment, quotations, order confirmation, assignment, and release.
- Maintenance Engineer assesses and executes assigned work.
- Before/after evidence and rework/re-inspection decisions are included.
- No upfront payment.

#### FE-08 - Dashboard, Analytics and Notifications

- Scoped operational, defect, service, workload, deadline, and notification views.
- Do not expand this feature into live drone telemetry, autonomous flight control, or unrelated enterprise CMMS.

### Step 4 - Align responsibility matrix

Keep team assignment columns and team abbreviations intact unless the existing template requires a correction. Team roles such as Leader, Member, Do, Review, Support, and Informed are project-management roles, not product roles.

Where a WBS function describes product behavior, ensure the responsible function is correctly described:

- Admin: platform configuration and administration.
- Client: customer organization actions and decisions.
- Service Manager: provider operations, quotation/order, assignment, verification, and release.
- Inspector: assigned inspection, evidence, verification, authoring, and peer review.
- Maintenance Engineer: technical assessment and maintenance execution.

Do not create additional columns for product roles if the existing template has a team responsibility matrix. Describe product roles in the WBS text and notes instead.

### Step 5 - Align deliverables, communication, and configuration sections

- Deliverables must refer to the current Report 1/2/3 and workflow baseline.
- Milestones must not promise out-of-scope drone automation or unsupported payment settlement.
- Communications may mention customer/service review, Inspector peer review, and Engineer assessment without inventing extra roles.
- Configuration management must point to the canonical report folder:
  content/project-reference/reports/
- Do not reference deleted markdown, source-documents, source-materials, or requirements/report3-srs paths.

### Step 6 - Synchronize the DOCX

Apply the approved changes to the DOCX while preserving the existing template.

Mandatory constraints:

- Preserve section order, fonts, colors, spacing, headers, footers, tables, and page structure.
- Do not add table columns.
- Do not create speculative tables or sections.
- Do not redesign the report.
- Keep Markdown and DOCX equivalent.
- Update the change log only using the existing format.
- Use the document skill render-and-verify process when available.

If the DOCX cannot be edited without changing the supplied layout, stop and report the exact blocker.

## 8. Verification

Run:

~~~powershell
cd E:\Dev\Repos\Capstone\docs
git diff --check
~~~

Also run:

1. Relative Markdown-link and image-path check.
2. Stale-term search for Viewer, SmartDroneHub, Organization Manager, Customer Manager, and ambiguous Manager.
3. A search ensuring no deleted legacy paths remain.
4. DOCX ZIP/package validation.
5. DOCX rendering and page-by-page inspection when render_docx.py, LibreOffice, and dependencies are available.
6. Hugo build only if Hugo is installed.

Report Passed, Failed, Skipped, and Blocked checks separately. Never claim a blocked renderer or Hugo build passed.

## 9. Acceptance criteria

- Report 2 Markdown and DOCX use exactly the five current product roles.
- No active current content uses Viewer or SmartDroneHub.
- Every current Manager reference resolves to Client or Service Manager.
- Team roles are not confused with product roles.
- FE-01 through FE-08 match the current WF1-WF4 responsibilities.
- Scope and risks reflect no autonomous drone piloting and no SmartDroneHub.
- Payment wording reflects no upfront payment and Client approval of post-service payment terms.
- Inspector assignment and author/reviewer separation are explicit.
- Maintenance Engineer assessment/execution responsibilities are explicit.
- Existing effort totals and dates are preserved unless a source-backed correction is documented.
- Existing DOCX template layout is preserved.
- Markdown and DOCX are synchronized.
- No broken links or references to deleted legacy folders remain.
- Final diff contains only the Report 2 task.
- Do not commit, push, create PR, or merge without separate authorization.

## 10. Handoff

Return:

1. Changed Report 2 sections and WBS rows.
2. Legacy-to-current terminology mapping.
3. Flow and responsibility-matrix alignment summary.
4. Any preserved estimates/dates and any source-backed corrections.
5. Exact verification commands and results.
6. Any DOCX/Hugo blocker.
7. Current branch and git status summary.
