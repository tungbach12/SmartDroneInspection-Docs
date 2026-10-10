# FE-07: Team Maintenance, Cost Control and Completion Reporting — MF4

Report 3 §3.8 titles this feature "Team Maintenance, Cost Control and
Completion Reporting". The filename retains the earlier "maintenance / defect
resolution" wording; the filename is stable, the scope is Report 3's.

## Scope baseline

MF4 receives **published MF3 findings requiring repair**. It manages the
enterprise's internal repair team, approved scope, estimates, changes, actuals
and closeout. It is not a provider marketplace or payment/commission flow;
supplier quotes can be attached as cost evidence without creating a supplier
user role, bidding portal, accounting ledger or procurement integration.

### Team responsibilities (Report 3 §3.8.1)

| Responsibility | Login role | Named by | What this person does |
| --- | --- | --- | --- |
| Work-order owner / budget approver | `ORG_ADMIN` | — | Selects corrective scope; names team, lead, report author and accepting reviewer; approves baseline and changes; records closure authorization. |
| Repair team lead | `MAINTENANCE_ENGINEER` | ORG_ADMIN, exactly one per work order | Coordinates assessment, task allocation, method, estimate, resource readiness, consolidated completion and actuals. |
| Team member / task assignee | `MAINTENANCE_ENGINEER` | ORG_ADMIN selects team; lead allocates tasks | Accepts tasks; records own work, consumption and time; uploads before/during/after proof. |
| Accountable repair-report author | `MAINTENANCE_ENGINEER` | ORG_ADMIN, exactly one per work order | Collects the team's records, requests/verifies/edits the LLM completion report, submits it; remains the author even when the LLM drafted the text. |
| Independent accepting reviewer | `ORG_ADMIN` | — | Not on the executing team and not the report author. Checks scope, evidence and residual issues; accepts or returns. Cost reconciliation is a **separate recorded decision**. |
| Re-inspection verifier, if required | `INSPECTOR` | Assigned through a linked MF1 inspection | Records independent evidence; **cannot stand in for a repair engineer's work log**. |
| Automated assistant | `SYSTEM` / LLM | Authorized workflow | Validates references, computes totals, drafts narrative, publishes only after approval. |

Separation-of-duties rules that carry real risk:

- Final acceptance **cannot** be performed by the repair-team lead/report author
  or by the executing team.
- Budget approval and technical acceptance are **distinct actions**, even when
  the same qualified non-executing `ORG_ADMIN` performs both under company
  policy.
- If **no qualified independent reviewer exists, the work remains awaiting
  review**. The platform does not create a professional qualification.
- Replacing the lead or report author is done by `ORG_ADMIN` with a recorded
  reason and handover; **old logs retain their authors**.

## Current test coverage

No workbook test case is mapped to FE-07 in this report.

The former `WF4-001`–`WF4-005` cases were removed on 2026-10-09 because they
described the retired five-role baseline or unimplemented Enterprise SaaS MF4
target behavior. The `maintenance` module has persistence foundations but no
implemented MF4 use-case/API workflow, so there is no runtime to execute and no
MF4 test result to record.

`WF3-006` verifies that publication hands repair-required finding IDs to the
maintenance boundary. That is an MF3 publication test owned by FE-06; it does
**not** verify maintenance ticket creation, execution, cost control, or
acceptance.

This is an explicit coverage gap. The removed `WF4-*` IDs stay reserved and are
never reused.

## Feature sheet summary

Values for the `Feature 7` summary block (`A2:E8` in the workbook).
The template reads these back by formula, so an export needs them
recorded here.

| Cell | Label | Value |
| --- | --- | --- |
| `B2` | Feature | Team Maintenance, Cost Control and Completion Reporting — MF4 |
| `B3` | Test requirement | Would verify repair team assignment, cost reconciliation and completion acceptance. MF4 is unimplemented, so no case is recorded. |
