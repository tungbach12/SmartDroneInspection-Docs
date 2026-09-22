# Planning Decisions and Evidence

**Date**: 2026-09-22
**Scope**: Four-week WF1–WF4 delivery with four flow owners.

## Decision 1: Plan from runtime, not table count

**Decision**: Treat migrations V1–V9 and their JPA entities/repositories as reusable schema only.
Schedule application services, APIs, authorization queries, clients, and tests as new work.

**Rationale**: The backend currently has runtime controllers/services in `users`, while `assets`,
`inspectionrequests`, `inspections`, and `maintenance` contain mainly persistence models. The web
asset client calls an API that is not yet implemented; inspection and maintenance web/mobile screens
are mostly placeholders. The database-design reference itself says physical schema does not imply
runtime completion.

**Alternatives considered**: Count every migrated table as a completed feature. Rejected because
that would underestimate the implementation and integration effort.

## Decision 2: One flow owner delivers a vertical slice

**Decision**: Hiếu owns WF1, Quốc owns WF2, Bách owns WF3, and Như owns WF4. Each owner delivers
the relevant backend, web UI, focused mobile UI, tests, and contract documentation. Mobile focuses
on assignment and field actions for Inspector and Maintenance Engineer; customer and manager
decisions are web-first.

**Rationale**: This matches the source-owner lines in `business-flows.md` and gives each developer
a reviewable flow outcome. It also preserves the product's current web/mobile role split.

**Alternatives considered**: Assign one person per platform. Rejected because the four flow
boundaries would then require handoff between developers for nearly every issue.

## Decision 3: Start downstream work with fixtures and integrate at gates

**Decision**: WF2 may start with a seeded asset, WF3 with a seeded accepted assignment, and WF4
with a seeded accepted report/finding. Real handoffs are integrated as soon as predecessor gates
are green. WF1 publishes a due-schedule event consumed by WF2; WF4 publishes a re-inspection
request consumed by WF2 to avoid circular module imports.

**Rationale**: WF1→WF2→WF3→WF4 is the business dependency chain, but four owners must work
concurrently to fit the time box.

**Alternatives considered**: Wait for each previous flow to be complete before starting the next.
Rejected because it leaves downstream owners idle and compresses testing into Week 4.

## Decision 4: Keep the four-week scope demonstrable

**Decision**: Deliver all four main paths plus the required revision, rejection, peer-review,
change-order, rework, and re-inspection decisions. Reuse existing auth and storage. Support manual
findings if AI is unavailable. Do not add online payments, drone piloting, model training, broad
analytics, email automation, or offline-first mobile behavior to this time box.

**Rationale**: The current runtime baseline and 80 total person-days make a full implementation of
every SRS exception unrealistic. The main business lifecycle remains testable end to end.

**Alternatives considered**: Full SRS feature parity in four weeks. Rejected as an unbounded
commitment given the current absence of most flow services and clients.

## Decision 5: Put cross-flow invoicing in a small billing capability

**Decision**: WF4 owner handles the invoice/payment-status slice for both post-service milestones
in Week 4. The implementation plan calls for a forward migration that lets one invoice reference
either an accepted inspection report or a maintenance order, with a check that exactly one source
is present. Move the existing invoice entity/repository to a `billing` capability only when that
runtime slice is built.

**Rationale**: The physical schema currently supports maintenance invoices only, while the
approved WF3 and WF4 flow requires separate inspection and maintenance milestones. One explicit
owner avoids two incompatible invoice lifecycles.

**Alternatives considered**: A second inspection-only invoice table or a generic polymorphic
`source_type/source_id` pair. Rejected because both duplicate or weaken existing relational
constraints.

## Decision 6: Use Jira Cloud's current Parent import mapping

**Decision**: Produce a UTF-8 CSV ordered with four Epic rows before their Task rows. Give every
row a unique `Work item ID`; Task rows reference their Epic's ID in `Parent`. Put owner and week
in Labels and in the description. Leave `Assignee` out until actual Jira account IDs are known.

**Rationale**: Atlassian's current Jira Cloud documentation uses `Work item ID`, `Work type`, and
`Parent` for CSV hierarchy; `Parent` replaces older `Epic Link` import guidance. The bulk creation
importer cannot preserve a multi-level hierarchy, so the external-system CSV import is required.

**Alternatives considered**: Legacy `Epic Name`/`Epic Link` columns, or filling assignee with
display names. Rejected due to Cloud field migration and unknown account identities.

**References**:

- [Atlassian: prepare a CSV file for import](https://support.atlassian.com/jira-software-cloud/docs/prepare-a-csv-file-for-import/)
- [Atlassian: import data from a CSV file](https://support.atlassian.com/jira-cloud-administration/docs/import-data-from-a-csv-file/)
- [Atlassian: CSV parent/child mapping](https://support.atlassian.com/jira/kb/map-issueid-parentid-fields-jira-csv-import/)
- [Atlassian: bulk CSV importer limits](https://support.atlassian.com/jira-software-cloud/docs/create-issues-using-the-csv-importer/)
