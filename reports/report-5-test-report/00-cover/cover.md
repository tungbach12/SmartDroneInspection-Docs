# Cover sheet source

This file mirrors the fields in the `Cover` sheet. Keep the labels unchanged
when transferring values into the workbook.

| Field | Value |
| --- | --- |
| Project Name | SmartDroneInspection |
| Project Code | SEP490 — *confirm with project owner* |
| Creator | *Enter team/member name* |
| Issue Date | *YYYY-MM-DD* |
| Document Code | *Enter document code* |
| Version | 0.6 |

## Record of change

The workbook's change table uses these columns. Add one row for each approved
revision; do not remove old entries.

| Effective Date | Version | Change Item | A / D / M | Change Description | Reference |
| --- | --- | --- | --- | --- | --- |
| 2026-09-22 | 0.1 | Initial Markdown test-report source | A | Split the supplied Report 5 template into editable sections and added the current WF1–WF4 baseline cases. | Report 5 template |
| 2026-09-22 | 0.2 | FE ownership alignment | M | Added FE-01 through FE-07 mapping, recorded the FE-01 W3 auth/migration gate, and split WF3 traceability across FE-04, FE-05, and FE-06 without changing test IDs or workbook sheets. | Jira SCRUM-56, SCRUM-58, SCRUM-106, SCRUM-107, SCRUM-108 |
| 2026-09-22 | 0.3 | Week 3 automated verification | M | Recorded the passed FE-01 foundation smoke gate and FE-04 execution/checklist acceptance evidence; recalculated Round 1 statistics without changing template case IDs or layout. | `WorkflowBaselineTest`, `InspectionWorkflowTest`, `InspectionFixtureTest`, mobile inspection test |
| 2026-09-22 | 0.4 | FE-01 scope correction | M | Removed MinIO from the FE-01 foundation scope and linked evidence storage/MinIO to FE-04/WF3 task T025; retained the separate infrastructure healthcheck evidence. | Jira SCRUM-58, SCRUM-85, SCRUM-108; Report 3 SRS 3.2 and 3.5 |
| 2026-09-22 | 0.5 | Workbook feature-sheet mapping clarification | M | Clarified that Feature 1/Feature 2 are fixed workbook sheets, while FE codes identify SRS capabilities and WF IDs identify business-flow test cases; documented the WF4-to-FE-07 mapping in Feature 2. | `README.md`, `template-layout.md`, `test-case-list.md`, feature sources, and test statistics |
| 2026-09-22 | 0.6 | FE-04/FE-05 case-boundary correction | M | Removed finding creation from the FE-04 evidence case and assigned AI candidate verification/manual findings to FE-05, preserving the existing WF3 test IDs. | Report 3 SRS 3.5–3.6; `feature-2.md`; `test-case-list.md` |
