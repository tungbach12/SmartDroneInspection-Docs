# Data Model: FE-04 — Week 3 WF3 Slice

## Existing records reused

- `inspection_assignments`: accepted assignment and `inspector_user_id` scope.
- `inspections`: one inspection per accepted assignment, with `asset_id`, `service_order_id`,
  `author_user_id`, `checklist_template_id`, status, and timestamps.
- `checklist_responses`: one response per inspection/checklist item, completed by the authenticated
  Inspector.
- `checklist_templates` and `checklist_items`: active template and required-item validation owned
  by FE-02/WF1 catalog data.

## Week 3 invariants

1. `inspection_assignments.status` must be `ACCEPTED`.
2. The authenticated Inspector must equal `inspector_user_id`.
3. Starting an accepted assignment is idempotent; the assignment cannot produce two inspections.
4. A checklist item must belong to `inspection.checklist_template_id`.
5. Required checklist responses reject blank/invalid values.
6. Author, asset, service order, and checklist IDs come from trusted assignment data, not the body.

No new migration is required for this slice. Test data is isolated per test and removed by the
existing test transaction/container lifecycle.
