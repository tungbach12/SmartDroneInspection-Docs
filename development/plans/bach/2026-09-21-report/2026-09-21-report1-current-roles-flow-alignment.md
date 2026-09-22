---
title: "Plan - Align Report 1 with Current Roles and Business Flows"
type: "agent-plan"
status: "ready"
updated: 2026-09-21
---

# Plan: Align Report 1 with the Current Product Contract

## 1. Objective

Update Report 1 - Project Introduction so its Markdown and DOCX versions describe the current SmartDroneInspection roles, product boundary, web/mobile users, and WF1-WF4 business flows. Preserve the supplied report structure and formatting; change content, not the template design.

This file is standalone so another AI agent can execute Report 1 without relying on chat history.

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
   docs/update-report1-current-flow
6. Do not use a worktree.
7. Do not commit to main.
8. Do not commit, push, create a PR, or merge unless explicitly authorized.

## 3. Files in scope

~~~text
content/project-reference/reports/report-1-project-introduction/report1-project-introduction.md
content/project-reference/reports/report-1-project-introduction/report1-project-introduction.docx
~~~

Report 2 and Report 3 are read-only references for this task. Do not edit them.

## 4. Source of truth

Read before editing:

1. content/project-reference/reports/report-3-software-requirement-specification/
2. content/project-reference/workflows/business-flows.md
3. content/project-reference/reports/report-1-project-introduction/report1-project-introduction.md
4. content/project-reference/reports/report-1-project-introduction/report1-project-introduction.docx
5. README.md
6. E:\Dev\Repos\Capstone\AGENTS.md

Report 3 and business-flows.md override stale statements in Report 1. Do not invent behavior not supported by these sources.

## 5. Current product roles

Use exactly these five human product roles:

| Human-readable role | Backend code | Scope |
| --- | --- | --- |
| Admin | ADMIN | Organizations, users, roles, categories, checklists, and platform configuration. Admin does not automatically perform customer or service workflow actions. |
| Client | CLIENT | Customer organization assets, schedules, inspection requests, quotation/order approval, released results, maintenance tickets, and customer decisions. |
| Service Manager | SERVICE_MANAGER | Service requests, feasibility, quotations, service orders, Inspector/Maintenance Engineer assignment, result verification and release, and service capacity. |
| Inspector | INSPECTOR | Assigned inspection execution, evidence, AI candidate verification, report authoring, and assigned peer review. An author cannot peer-review their own report. |
| Maintenance Engineer | MAINTENANCE_ENGINEER | Assigned technical assessment and maintenance execution, work logs, completion data, and before/after evidence. |

Use human-readable names in the report. Use uppercase codes only for implementation examples.

### Legacy terminology rules

Do not blindly replace every word. Resolve the responsibility in context.

| Legacy wording | Required replacement |
| --- | --- |
| Administrator / Platform Administrator | Admin |
| Organization Manager / Customer Manager | Client |
| Manager | Client for customer actions; Service Manager for provider operations |
| Viewer | Remove from current role list and active scope |
| Inspector Author / Inspector Peer Reviewer | Responsibilities of Inspector, not extra roles |
| SmartDroneHub | Remove; it is not a product dependency |
| System, MinIO, YOLO Service | External/system actors, not human roles |

Historical change-log entries may retain old terminology when clearly marked historical. Current product content must use the new names.

## 6. Business-flow baseline

### WF1 - Asset Registration and Periodic Inspection Scheduling

- Client manages assets belonging to its organization.
- Client creates recurring schedules.
- Admin maintains categories and checklist templates.
- System creates one PERIODIC request per Asset + Schedule + Due Cycle.
- Duplicate due-cycle requests are prohibited.

### WF2 - Inspection Request Review, Service Order and Inspector Assignment

- Client creates AD_HOC requests or completes PERIODIC requests.
- Client provides scope, priority, deadline, access constraints, contact details, and supporting documents.
- Service Manager reviews feasibility and capacity.
- Service Manager prepares versioned quotation and service order.
- Client approves or requests revision.
- No upfront payment is required; Client approves post-service payment terms.
- After order confirmation, Service Manager assigns an Inspector.
- Inspector accepts or rejects; rejection returns to Service Manager for reassignment.

### WF3 - Inspection Execution, AI-Assisted Verification and Report Delivery

- Inspector accesses only assigned inspections and authorized evidence.
- Inspector executes checklist and uploads evidence.
- MinIO stores evidence; YOLO creates candidates only.
- Inspector Confirm, Modify, Reject, or Manual Add actions determine official findings.
- Only verified findings enter reports and statistics.
- Inspector authors a versioned report and submits it for peer review.
- The author cannot peer-review their own report.
- Service Manager assigns another qualified Inspector as reviewer and releases the result.
- Client accepts or requests clarification/revision.
- Accepted versions are immutable; corrections create a new version.

### WF4 - Maintenance Assessment, Work Execution and Defect Resolution

- Client creates a maintenance ticket from verified defects in an accepted report.
- Service Manager plans assessment and assigns a Maintenance Engineer.
- Maintenance Engineer provides technical scope, risks, materials, duration, and estimate.
- Service Manager prepares a versioned maintenance order.
- Client approves scope and post-service payment terms.
- Service Manager confirms order and assigns execution.
- Maintenance Engineer performs work and uploads work logs plus before/after evidence.
- Service Manager verifies/releases the result.
- Client accepts, requests rework, or requests re-inspection.
- Re-inspection creates a linked AD_HOC request returning to WF2.
- No upfront payment is required.

## 7. Detailed execution steps

### Step 1 - Audit

1. Read every heading, table, actor list, role list, scope paragraph, feature description, and limitation.
2. Search Report 1 Markdown and DOCX for:
   Viewer, Administrator, Platform Administrator, Organization Manager, Customer Manager, SmartDroneHub, and ambiguous Manager.
3. Classify matches as current text, historical change-log text, or false positive.
4. Compare conflicts against Report 3 and business-flows.md.
5. Record the intended change list before editing.

### Step 2 - Update Report 1 content

Review and update the existing sections without changing their order:

- Product information and product type.
- Product background and business opportunity.
- Existing-system comparison where it contains stale project terminology.
- Software product vision.
- Project scope and limitations.
- Major features FE-01 through FE-08.
- Actor and role descriptions.
- Web and mobile application purpose.

The updated Report 1 must clearly state:

- Admin is platform administration only.
- Client performs customer-organization actions.
- Service Manager performs provider/service operations.
- Inspector and Maintenance Engineer work from assignments.
- Web is used primarily by Admin, Client, and Service Manager.
- Mobile supports field work for Inspector and Maintenance Engineer.
- SmartDroneInspection manages inspection services, evidence, findings, reports, and maintenance follow-up; it does not pilot drones.
- YOLO output is a candidate until Inspector verification.
- Report author and peer reviewer must be different Inspector users.
- No upfront payment is required; post-service payment terms are approved by Client.
- SmartDroneHub is not an actor or external dependency.

Do not change team-management roles such as Lecturer, Leader, or Member into product roles.

### Step 3 - Synchronize the DOCX

Apply the same approved text changes to the DOCX.

Mandatory constraints:

- Preserve the official template's section order.
- Preserve fonts, colors, spacing, headers, footers, tables, and page structure.
- Do not add columns.
- Do not add speculative sections or new tables.
- Do not redesign the report.
- Keep Markdown and DOCX content equivalent.
- Update the change log only according to the existing format.
- Use the document skill render-and-verify process when available.

If preserving layout is not possible, stop and report the exact blocker instead of producing a replacement with a different format.

## 8. Verification

Run:

~~~powershell
cd E:\Dev\Repos\Capstone\docs
git diff --check
~~~

Also run:

1. Relative Markdown-link and image-path check.
2. Stale-term search for Viewer, SmartDroneHub, Organization Manager, Customer Manager, and ambiguous Manager.
3. DOCX ZIP/package validation.
4. DOCX rendering and page-by-page inspection when render_docx.py, LibreOffice, and dependencies are available.
5. Hugo build only if Hugo is installed.

Report Passed, Failed, Skipped, and Blocked checks separately. Never call a blocked render a pass.

## 9. Acceptance criteria

- Report 1 Markdown and DOCX use exactly the five current human product roles.
- No active current text contains Viewer or SmartDroneHub.
- Manager references are resolved to Client or Service Manager.
- Web/mobile responsibilities are accurate.
- WF1-WF4 descriptions match the current business-flow reference.
- No-upfront-payment and post-service payment-term rules are correct.
- Inspector assignment scope and peer-review separation are explicit.
- Autonomous drone piloting remains out of scope.
- Markdown and DOCX are synchronized.
- Existing template layout is preserved.
- No broken links or legacy-folder references remain.
- Final diff contains only the Report 1 task.
- Do not commit, push, create PR, or merge without separate authorization.

## 10. Handoff

Return:

1. Changed Report 1 sections.
2. Legacy-to-current terminology mapping.
3. Workflow alignment summary.
4. Exact verification commands and results.
5. Any DOCX/Hugo blocker.
6. Current branch and git status summary.
