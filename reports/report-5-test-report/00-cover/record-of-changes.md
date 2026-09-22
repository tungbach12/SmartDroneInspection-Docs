# Record of changes source

Use this file when the report needs a longer change history than fits on the
cover sheet. `A` means added, `D` means deleted, and `M` means modified.

| Effective Date | Version | Change Item | A / D / M | Change Description | Reference |
| --- | --- | --- | --- | --- | --- |
| 2026-09-22 | 0.1 | Report 5 working source | A | Created the editable test-case structure from the supplied workbook without changing the original template layout. | `template/Report5_Test Report.xlsx` |
| 2026-09-22 | 0.2 | FE ownership alignment | M | Added FE-01 through FE-07 mapping, recorded the FE-01 W3 auth/migration gate, and split WF3 traceability across FE-04, FE-05, and FE-06 without changing test IDs or workbook sheets. | Jira SCRUM-56, SCRUM-58, SCRUM-106, SCRUM-107, SCRUM-108 |
| 2026-09-22 | 0.3 | Week 3 automated verification | M | Recorded the passed FE-01 auth/migration smoke gate, separate MinIO infrastructure healthcheck, and FE-04 execution/checklist acceptance evidence; recalculated Round 1 statistics without changing template case IDs or layout. | `WorkflowBaselineTest`, `InspectionWorkflowTest`, `InspectionFixtureTest`, mobile inspection test, backend `mvnw verify` |
| 2026-09-22 | 0.4 | FE-01 scope correction | M | Removed MinIO from the FE-01 foundation scope and linked evidence storage/MinIO to FE-04/WF3 task T025; retained the separate infrastructure healthcheck evidence. | Jira SCRUM-58, SCRUM-85, SCRUM-108; Report 3 SRS 3.2 and 3.5 |
| 2026-09-22 | 0.5 | Workbook feature-sheet mapping clarification | M | Clarified that Feature 1/Feature 2 are fixed workbook sheets, while FE codes identify SRS capabilities and WF IDs identify business-flow test cases; documented the WF4-to-FE-07 mapping in Feature 2. | `README.md`, `template-layout.md`, `test-case-list.md`, feature sources, and test statistics |
| 2026-09-22 | 0.6 | FE-04/FE-05 case-boundary correction | M | Removed finding creation from the FE-04 evidence case and assigned AI candidate verification/manual findings to FE-05, preserving the existing WF3 test IDs. | Report 3 SRS 3.5–3.6; `feature-2.md`; `test-case-list.md` |
