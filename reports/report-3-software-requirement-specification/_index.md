---
title: "Report 3 SRS"
document_type: report3-srs
weight: 10
---

# Report 3 - Software Requirement Specification

This folder is the team-maintained Markdown source of Report 3. **Current target revision: 7 October 2026 — Enterprise SaaS, four roles and four connected Main Flows.** The authoritative detailed actor-by-step flows, MF3 inspection report and MF4 team/cost/completion report requirements are in [Functional Requirements](03-functional-requirements/).

**Revision boundary:** The 7 October 2026 change defined the Enterprise SaaS requirements in Report 3 and was not implementation or runtime-test evidence. A separate backend reset has since completed its runtime schema cutover. On 7 October, selected documentation companions (database status, backend runtime caveats, and Report 5 scope) were reconciled without changing historical test evidence. This index does not claim all references, proposals, or frontend/mobile contracts are synchronized.

The retained [Report 3 DOCX](report3-software-requirement-specification.docx) and `assets/*.png` diagrams are earlier baseline artifacts, **not regenerated or authoritative for this revision**. Use the Markdown sections and current embedded Mermaid diagrams for the new target; DOCX/diagram regeneration is a separate deliverable.

## Sections

- [Project Report](00-project-report/)
- [Overall Description](01-overall-description/)
- [User Requirements](02-user-requirements/)
- [Functional Requirements](03-functional-requirements/)
- [Non-Functional Requirements](04-non-functional-requirements/)
- [Other Requirements](05-requirement-appendix/)

The record of changes is retained in `00-record-of-changes.md` as supporting
history and is not a numbered section of the official Report 3 format.

Report 3 defines target requirements, not a claim that every requirement is deployed. Backend V24/V25/V26 completed the identity/schema/runtime cutover; MF3 is implemented, and a partial MF4 backend REST/workflow slice was added and verified on 10 October 2026. MF1/MF2 workflows and the explicit MF4 gaps recorded in §3.8 remain outstanding. The Markdown section files above define the SRS; see the implementation-status note in §3.8 and current source for deployment details.
