# Enterprise SaaS Backend Reset — Status Addendum

> **Observed 7 October 2026.** This is a documentation-repository status addendum to the backend-owned plan [`backend/.hermes/plans/2026-10-07_enterprise-saas-backend-and-full-db.md`](../../../backend/.hermes/plans/2026-10-07_enterprise-saas-backend-and-full-db.md). It corrects baseline/version claims without replacing that plan's phases or dropping still-needed work. The referenced backend plan and migrations live in a separate repository and are not edited by this addendum.

## Verified source-tree state

- Backend branch: `feat/enterprise-saas-reset`; checked HEAD: `b00e0b9` (`fix(security): permit provider register/activate endpoints (#58)`). The backend reset worktree is dirty and includes both staged and unstaged changes. The migration files below were present as untracked files in the checked worktree; their presence does not prove they were committed or applied to a database.
- The last migration sequence recorded before the reset was `V23__provider_onboarding.sql`. The reset worktree now contains forward migration sources `V24__enterprise_saas_role_and_schema_alignment.sql` and `V25__enterprise_saas_target_schema.sql`; do not describe V25 as the final migration or assume it has run.
- V24 aligns identity/role/actor-zone vocabulary and uses fail-closed prechecks for ambiguous legacy workforce/provider identities, scope problems, and target-role collisions. It does not complete removal of all legacy schema.
- V25 is additive and creates the target tables. `V26__enterprise_saas_runtime_cutover.sql` then completes the runtime cutover: it drops every non-target marketplace, old-client and MF5 table, tightens composite tenant foreign keys, and enforces target status vocabularies. The resulting runtime schema is exactly the 41 application tables plus `event_publication` and `flyway_schema_history`, asserted by `FullDatabaseSchemaMigrationTest` and `RuntimePersistenceInventoryTest`.
- The reset worktree retains asset/catalog/scheduling controllers, services, repositories and entities. Current code guards asset review, proposal review and selection as `ORG_ADMIN`; service lookups require organization scope. `ADMIN` has the asset-category catalog role and a global proposal-list branch, but does not have global asset-review authority.
- The inspection workflow controllers/services and their workflow tests have been removed from the reset worktree. Remaining inspection domain/repository classes and database rows are persistence/schema only, not callable MF1–MF4 workflow behavior. Subscription/workforce package roots and V25 tables likewise do not establish complete runtime services. The current target workflow implementation remains explicitly outside reset scope.
- Verification run on 8 October 2026 (backend `./mvnw clean verify`, 88 tests, exit 0; frontend `npm run lint && npm test && npm run build`, 128 tests, exit 0; mobile `dart format` + `flutter analyze` + `flutter test`, 16 tests, exit 0). Report 5's nine target workflow cases remain `Pending` — this reset implements no MF1-MF4 workflow behavior, and prior executed v1 outcomes remain historical evidence for the version actually tested.

## Work that remains open

Keep the backend plan's remaining phases and acceptance criteria active until separately verified. In particular:

1. ~~Verify V24/V25/V26 on empty and populated databases~~ — done on 8 October 2026: `./mvnw clean verify` passed 88 tests (exit 0), including empty-database migration, populated V1-V23 fail-closed prechecks, target constraints/indexes, and exact physical schema inventory.
2. Complete persistence/entity/repository ownership for the required target schema, and reconcile existing ORM mappings with V25 without treating table creation as feature completion.
3. Identity and organization registration are delivered and verified (`POST /api/v1/auth/register` creates the organization and its first `ORG_ADMIN` and writes an `ORGANIZATION_REGISTRATION` row to `audit_events`). Subscription entitlement and workforce modules remain package roots without runtime; `ADMIN` global-asset-access limitations still need a deliberate decision.
4. ~~Legacy-table retirement~~ — done in V26 under the explicit start-fresh authorization. Migration history `V1`-`V23` is preserved untouched; only the runtime schema and code were cut over.
5. Implement MF1–MF4 workflow behavior in separate approved slices. Readiness, inspection sessions/evidence, AI/LLM review and publication, maintenance team/cost control, and independent acceptance remain workflow tasks—not outcomes of this schema reset.
6. Preserve Report 5's historical results and all nine target `Pending` rows until matching target execution and evidence are recorded. Do not infer a pass from test source files or migration files alone.

This addendum is an as-observed source/worktree note, not a migration execution report, database verification, or claim that any remaining task is complete.