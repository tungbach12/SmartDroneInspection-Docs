---
title: "Report 3 - Project Report"
document_type: report3-project-section
weight: 5
source: "report3-software-requirement-specification.docx"
---

# I. Project Report

## 1. Status Report

The SmartDroneInspection project develops an Enterprise SaaS platform designed for infrastructure asset management, automated UAV-assisted inspection, AI defect detection, and maintenance lifecycle coordination. The system establishes an end-to-end digital audit trail across four primary operational roles: `Platform Admin`, `Organization Admin`, `Inspector`, and `Maintenance Engineer`.

The software requirements baseline is structured around the complete operational cycle: onboarding infrastructure assets and drone equipment, planning inspection missions, executing field flight surveys, detecting visual defects via computer vision (YOLO11s), synthesizing human-reviewed inspection reports, and handing over confirmed defects to maintenance remediation with cost estimation and independent acceptance.

| Area | Status | Evidence and next step |
| --- | --- | --- |
| Product scope | Baseline aligned | The platform manages the inspection-to-maintenance lifecycle. Hardware flight control, online payment processing, and autonomous AI approval remain out of scope. |
| Requirements | Finalized | Report 3 defines system actors, use cases, functional requirements (FE-01 to FE-08), non-functional requirements, business rules, messages, and technology constraints. |
| Software foundation | In progress | The system utilizes a multi-repository architecture comprising Spring Boot backend, React web portal, Flutter mobile application, and AI inference microservice. |
| Verification | Ongoing | Continuous integration gates ensure multi-layer testing, code formatting, security analysis, and schema consistency across all client and server components. |

## 2. Team Involvements

| Member | Role | Main involvement |
| --- | --- | --- |
| Trần Hoàng Trung Hiếu | Leader | Coordinates project scope, architecture planning, document baselines, and end-to-end operational workflow consistency. |
| Phùng Trung Quốc | Member | Contributes to backend domain implementation, asset and inspection workflow functions, data validation, and database design. |
| Trương Thái Như | Member | Contributes to web and mobile frontend interfaces, report drafting experience, and client-side validation flows. |
| Trần Tùng Bách | Member | Contributes to authentication, authorization, object storage, AI inference integration, and backend service verification. |
| Phạm Minh Trí | Lecturer | Provides project supervision, academic guidance, and milestone reviews. |
| Đặng Ngọc Minh Đức | Lecturer | Provides project supervision, academic guidance, and milestone reviews. |

## 3. Issues and Suggestions

| Issue or risk | Suggestion |
| --- | --- |
| Requirements, implementation, and report sections can drift when roles or workflow states change. | Keep role names, workflow identifiers, business rules, API contracts, and test evidence aligned in the same change review. |
| The system spans backend, web, mobile, object storage, and AI services. | Deliver bounded vertical slices and verify API and data contracts at each service boundary before expanding functionality. |
| AI output can contain false positives, false negatives, or unsupported conclusions. | Treat AI detection output as advisory candidates only; require mandatory human Inspector verification before findings become official. |
| Cross-organization and assignment access errors have high impact in multi-tenant environments. | Enforce strict organization-level data isolation and role-based permissions on all backend queries and mutations. |
| Operational field conditions can vary significantly during UAV inspection missions. | Provide dedicated pre-flight checklist verification, session postponement, and terminal abort workflows to ensure safety compliance. |
