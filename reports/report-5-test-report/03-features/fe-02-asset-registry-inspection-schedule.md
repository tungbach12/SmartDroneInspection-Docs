# FE-02: Asset, Drone, Workforce and Compliance Catalog — MF1

Report 3 §3.3 titles this feature "Asset, Drone, Workforce and Compliance
Catalog". The filename retains the earlier "asset registry / inspection
schedule" wording; the filename is stable, the scope is Report 3's.

## Scope baseline

MF1 retains the agreed asset-creation assignment: **ORG_ADMIN creates an asset
together with one responsible Inspector and one specific Drone**, then creates
inspections that inherit that pair. Re-inspecting an existing asset does not
recreate the asset. This is MF1, the source of the MF2 assignment FE-03
consumes.

The fourteen MF1 steps divide as:

| Steps | Actor | What it does |
| --- | --- | --- |
| MF1-01 – MF1-05 | `ORG_ADMIN` + `SYSTEM` | Organization identity and authorized reviewers; subscription entitlement check; Inspector/Engineer provisioning; skills and credential records; document validation with expiry warnings. |
| MF1-06 – MF1-07 | `ORG_ADMIN` | Drone registration by unique identifier, serviceability and documents; flight permits and compliance files with issuer, scope and conditions. |
| MF1-08 – MF1-10 | `ORG_ADMIN` + `SYSTEM` | Asset profile, and in the **same workflow** selection of exactly one Inspector and one Drone; validation and audit that saves asset and pair together. |
| MF1-11 – MF1-14 | `ORG_ADMIN` + `SYSTEM` | Create the inspection for that asset; inherit the current pair into a snapshot; confirm with a recorded reassignment reason; dispatch with document references. |

Gates worth stating because they are easy to misread as satisfied:

- **No partially created complete asset with a missing pair** (MF1-10). Asset
  assignment is not a flight permit, nor an exclusive reservation of the Drone.
- An updated asset default **never rewrites past inspection snapshots**
  (MF1-12).
- Unresolved conflicts, disabled users or unavailable Drones **block dispatch**
  (MF1-13).
- Cadence changes affect **future due work only**, not published history.
- An informational airspace warning **does not authorize flight** (MF1-08).
- Machine validation of a document **is not government verification** (MF1-05).

The four canonical roles are `ADMIN`, `ORG_ADMIN`, `INSPECTOR` and
`MAINTENANCE_ENGINEER`.

## Current test coverage

No workbook test case is mapped to FE-02 in this report. **All fourteen MF1
steps are unverified.**

The former `WF1-001`–`WF1-019` cases were removed on 2026-10-09 because they
described the retired five-role WF1 baseline (Service Manager review, Client
asset registration, schedule proposals). That is not the current system, so
their recorded results are not evidence for it.

The backend does implement a catalog with organization scoping and a paged
list, and the WF3 inspection collection depends on it. That is catalog CRUD,
not the MF1 resource-creation workflow, and **no executed test case is recorded
here for it**, so it is not reported as tested. This is an explicit, truthful
coverage gap: FE-02 verification is outstanding and must be executed and
recorded before the feature can be reported as verified.

### Steps that would be covered first

| Step | Gate to verify |
| --- | --- |
| MF1-09 – MF1-10 | An asset cannot be saved complete without exactly one Inspector and one Drone. |
| MF1-12 | An inspection snapshots the pair; later asset default changes do not rewrite it. |
| MF1-13 | A reassignment requires a recorded reason and is versioned. |
| MF1-02 | A lapsed subscription denies the operation without deleting existing history. |

The removed `WF1-*` case IDs stay reserved and are never reused.
