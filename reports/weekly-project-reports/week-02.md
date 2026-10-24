# Project Report — Week 2

**Project name:** SmartDroneInspection: AI-powered Infrastructure Inspection Management Platform  
**Group:** FA26SE112  
**Reporting period:** 14–20 September 2026  
**Team members:** Trần Hoàng Trung Hiếu, Phùng Trung Quốc, Trần Tùng Bách, Trương Thái Như

> Week 2 focused on core workflow specifications (WF1–WF4), presentation slide decks, initial architecture baseline, and Spring Modulith capability definitions.

## I. Status Report

| # | Project Task | In-charge | Status | Notes (Work Item in Details) |
|---:|---|---|---|---|
| 1 | Design WF1 workflow and presentation slides: Asset Registration & Periodic Scheduling | Trần Hoàng Trung Hiếu | Completed | [SCRUM-35](https://capstonefall26.atlassian.net/browse/SCRUM-35). Outlined asset catalog, component hierarchy, drone registration, and periodic schedule rules. |
| 2 | Prepare presentation slides 1 & 5: Project Title, Team, Scope & End-to-End Lifecycle | Trần Hoàng Trung Hiếu | Completed | [SCRUM-39](https://capstonefall26.atlassian.net/browse/SCRUM-39). Visualized complete inspection lifecycle and platform actor interactions. |
| 3 | Draft SRS Section 3.1 (MF1): Asset hierarchy, drone fleet catalog, and periodic scheduling | Trần Hoàng Trung Hiếu | Completed | Specified functional requirements for asset registration, drone model specifications, and maintenance thresholds. |
| 4 | Design WF2 workflow and presentation slides: Inspection Request, Quotation & Assignment | Phùng Trung Quốc | Completed | [SCRUM-36](https://capstonefall26.atlassian.net/browse/SCRUM-36). Detailed request intake, quotation review, pilot credential check, and assignment. |
| 5 | Prepare presentation slides 4, 8 & 9: System Actors, Tech Stack, Current vs. Proposed State | Phùng Trung Quốc | Completed | [SCRUM-40](https://capstonefall26.atlassian.net/browse/SCRUM-40), [SCRUM-48](https://capstonefall26.atlassian.net/browse/SCRUM-48). Outlined actors, technical stack (Spring/React/Flutter), and solution benefits. |
| 6 | Draft SRS Section 3.2 (MF2): Inspection request review and readiness criteria | Phùng Trung Quốc | Completed | Specified request triage, flight permit checks, pilot availability, and safety checklist templates. |
| 7 | Design WF3 workflow and presentation slides: Inspection Execution, AI Verification & Reports | Trần Tùng Bách | Completed | [SCRUM-37](https://capstonefall26.atlassian.net/browse/SCRUM-37), [SCRUM-47](https://capstonefall26.atlassian.net/browse/SCRUM-47), [SCRUM-52](https://capstonefall26.atlassian.net/browse/SCRUM-52). Detailed manual RC flight, evidence upload, advisory AI, and report sign-off. |
| 8 | Design and initialize WF3 database schema baseline and physical workflow schema | Trần Tùng Bách | Completed | [SCRUM-43](https://capstonefall26.atlassian.net/browse/SCRUM-43). Defined relational schema baseline for inspections, evidence, findings, checklists, and reports. |
| 9 | Establish Spring Modulith capability boundaries, feature-owned persistence, and role naming | Trần Tùng Bách | Completed | Scaffolded modular backend roots, aligned persistence structure, and standardized canonical roles in codebase. |
| 10 | Design WF4 workflow and presentation slides: Maintenance Assessment & Defect Resolution | Trương Thái Như | Completed | [SCRUM-38](https://capstonefall26.atlassian.net/browse/SCRUM-38). Formulated post-inspection maintenance ticketing, work order dispatch, and sign-off. |
| 11 | Prepare presentation slides 2 & 3: Context, Problem Statement, System Actors & Responsibilities | Trương Thái Như | Completed | [SCRUM-42](https://capstonefall26.atlassian.net/browse/SCRUM-42), [SCRUM-49](https://capstonefall26.atlassian.net/browse/SCRUM-49). Highlighted post-inspection defect remediation delays and safety risks. |
| 12 | Draft SRS Section 3.4 (MF4): Defect-to-ticket conversion and contractor assignment | Trương Thái Như | Completed | Specified maintenance work order initiation from published findings, contractor assignment, and resolution verification. |

## II. Project Issues

| # | Project Issue | Owner | Status | Notes (Solution, Suggestion, etc.) |
|---:|---|---|---|---|
| 1 | Deprecated slide drafts existed alongside active presentation tasks | Trần Tùng Bách | Resolved | Marked historical task SCRUM-41 deprecated; kept SCRUM-37 as the active presentation deliverable. |
| 2 | Presentation and schema deliverables needed proof of runtime feasibility | Team | Addressed | Agreed to prioritize executable authentication, assignment fixtures, and Flyway migrations in Week 3. |

## III. Next Week Plan

| # | Project Work Item | In-charge | Deadline | Notes (Task Details, etc.) |
|---:|---|---|---|---|
| 1 | Smoke-test authentication fixtures, Flyway migrations, and role boundaries | Trần Tùng Bách | 28 Sep 2026 | [SCRUM-58]. Ensure clean Spring Boot startup and PostgreSQL schema creation. |
| 2 | Design relational database schemas for all four workflows in Report 4 (SDD) | All Members | 30 Sep 2026 | Map entities, foreign keys, and indexes for MF1–MF4. |
| 3 | Implement assignment-scoped inspection start and checklist responses | Trần Tùng Bách & Phùng Trung Quốc | 30 Sep 2026 | [SCRUM-83]. Enforce assigned-pilot authorization rules. |

## IV. Other Project Matters/Suggestions

| # | Project Matter/Suggestions | Raised By | Date | Notes |
|---:|---|---|---|---|
| 1 | Maintain strict separation between advisory AI detections and official findings | Trần Tùng Bách | 20 Sep 2026 | Emphasized in presentations and requirements that AI detections require human Inspector verification. |
