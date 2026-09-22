---
title: "Report 3 - Project Report"
document_type: report3-project-section
weight: 5
source: "report3-software-requirement-specification.docx"
---

# I. Project Report

## 1. Status Report

As of 22 September 2026, SmartDroneInspection has an aligned requirements baseline for the four business workflows: asset registration and periodic scheduling (WF1), inspection request review and assignment (WF2), inspection execution and report release (WF3), and maintenance resolution and re-inspection (WF4). The baseline covers the five current roles: Admin, Client, Service Manager, Inspector, and Maintenance Engineer.

| Area | Status | Evidence and next step |
| --- | --- | --- |
| Product scope | Baseline aligned | The platform manages the inspection-to-maintenance lifecycle. Drone flight control, online payment processing, and autonomous AI approval remain out of scope. |
| Requirements | In progress | Report 3 defines actors, use cases, functional requirements, non-functional requirements, business rules, messages, and scope constraints. The team will update the baseline when an approved requirement changes. |
| Software foundation | In progress | The project uses separate backend, frontend, mobile, and documentation repositories. Authentication and role contracts are aligned; remaining business capabilities are delivered as focused vertical slices. |
| Verification | Ongoing | Each repository must run its relevant formatting, lint, build, and test checks before a release baseline is accepted. Environment-dependent failures must be recorded separately from code failures. |

## 2. Team Involvements

| Member | Role | Main involvement |
| --- | --- | --- |
| Trần Hoàng Trung Hiếu | Leader | Coordinates scope, planning, repository integration, document baselines, review preparation, and end-to-end workflow consistency. |
| Phùng Trung Quốc | Member | Contributes to backend domain implementation, asset and inspection workflow functions, data rules, and related verification. |
| Trương Thái Như | Member | Contributes to web and mobile workflow screens, report and AI-assisted review experiences, and user-facing validation. |
| Trần Tùng Bách | Member | Contributes to authentication, authorization, storage and integration concerns, backend implementation, and technical verification. |
| Phạm Minh Trí | Lecturer | Provides project supervision and academic review. |
| Đặng Ngọc Minh Đức | Lecturer | Provides project supervision and academic review. |

## 3. Issues and Suggestions

| Issue or risk | Suggestion |
| --- | --- |
| Requirements, implementation, and report sections can drift when roles or workflow states change. | Keep role names, workflow identifiers, business rules, API contracts, and test evidence aligned in the same change review. |
| The system spans backend, web, mobile, object storage, and AI services. | Deliver one bounded vertical slice at a time and verify the relevant repository and integration boundaries before expanding scope. |
| AI output can contain false positives, false negatives, or unsupported conclusions. | Treat AI output as a candidate only; require Inspector verification and preserve the evidence and model version used for each result. |
| Cross-organization and assignment access errors have high impact. | Test positive and negative authorization cases for organization ownership, assignment, release authority, and separation of duties. |
| Local infrastructure may not be available on every development machine. | Record blocked environment checks explicitly and rely on CI or an approved integration environment for the missing verification. |
