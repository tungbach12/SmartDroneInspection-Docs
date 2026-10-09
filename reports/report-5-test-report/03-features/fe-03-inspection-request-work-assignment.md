# FE-03: Inspection Request and Work Assignment

## Scope baseline

Inspection requests are raised against an organization's assets, reviewed and
confirmed into a service order, and an Inspector is assigned to carry out the
work. This is MF1/MF2 upstream of MF3.

## Current test coverage

No workbook test case is mapped to FE-03 in this report.

The former `WF1-017`–`WF1-019` and `WF2-001`–`WF2-007` cases were removed on
2026-10-09. The `WF1`/`WF2` rows described the retired five-role baseline
(periodic request generation, Service Manager review, Client quotation and
order approval); the `WF2-005`–`WF2-007` rows described a target design that has
never been implemented. Neither is evidence for the current system.

**MF1 and MF2 are not implemented in the current backend**, so there is no
runtime to test and no executed evidence to record. This is an explicit coverage
gap, not a claim that the requirements were dropped: MF1 and MF2 remain
required by Report 3 and are awaiting implementation.

This gap also constrains FE-04: there is no `/assignments`, `/start`, or
`/checklist` endpoint, so MF3 has no verified entry path other than the scoped
inspection list recorded as `WF3-009`.

The removed case IDs stay reserved and are never reused.
