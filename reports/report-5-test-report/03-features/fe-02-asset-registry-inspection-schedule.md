# FE-02: Asset Registry and Inspection Schedule

## Scope baseline

An organization registers and maintains its assets, asset documents and
recurring inspection schedules; categories and checklist templates are
maintained centrally. The current roles are `ADMIN`, `ORG_ADMIN`, `INSPECTOR`
and `MAINTENANCE_ENGINEER`.

## Current test coverage

No workbook test case is mapped to FE-02 in this report.

The former `WF1-001`–`WF1-019` cases were removed on 2026-10-09 because they
described the retired five-role WF1 baseline (Service Manager review, Client
asset registration, schedule proposals). That is not the current system, so
their recorded results are not evidence for it.

The current backend does implement an asset catalog with organization scoping
and a paged list, but **no executed test case is recorded here for it**, so it
is not reported as tested. This is an explicit, truthful coverage gap: FE-02
verification is outstanding and must be executed and recorded before the
feature can be reported as verified.

The removed `WF1-*` case IDs stay reserved and are never reused.
