# FE-07: Maintenance and Defect Resolution

## Scope baseline

MF4 begins when a published MF3 report identifies repair-required findings.
The intended flow includes internal team assignment, an estimate/change/actual
cost record, and an independent ORG_ADMIN acceptance gate.

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
