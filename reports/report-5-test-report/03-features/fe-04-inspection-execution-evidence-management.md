# FE-04: Inspection Execution and Evidence Management

## Scope baseline

The Flutter application supports assignment acceptance, inspection sessions, evidence upload/retry and metadata. Evidence records the inspection, asset, Inspector, capture time and source; GPS or external mission references are retained when available. Manual drone piloting stays outside the platform.

## Current acceptance cases

WF3-001 and WF3-002 map to FE-04. Evidence storage and MinIO belong to this feature, not to the FE-01 identity foundation gate.

| Test Case ID | Test Case Description | Test Case Procedure | Expected Results | Pre-conditions | Round 1 | Test date | Tester | Round 2 | Test date | Tester | Round 3 | Test date | Tester | Note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| WF3-001 | Assigned Inspector starts the inspection and completes the required checklist. | Sign in as the accepted assignee; start the inspection; load the checklist; save a required response; reload it; try the checklist as another Inspector and an Inspector from another organization. | Start is retry-safe; the published checklist and saved value/timestamp are returned to the assignee; both out-of-scope Inspectors receive INSPECTION_SCOPE_DENIED. | Active Inspector owns an accepted assignment; the checklist is published. | Passed | 2026-09-24 | Codex (automated) | Pending |  |  | Pending |  |  | Full backend mvnw verify passed 134 tests with JaCoCo and Modulith checks. InspectionWorkflowTest covers assignment/start/checklist rules; EvidenceApiIntegrationTest.returnsChecklistAndSavedResponseOnlyToTheAcceptedAssignee verifies the HTTP read/save contract and both denial paths; mobile assignment/repository/capture tests passed. |
| WF3-002 | Assigned Inspector uploads supported evidence with checksum and source traceability. | Upload a valid PNG from the started inspection; retry the same bytes; list and stream evidence as the assignee; submit corrupt content and read as out-of-scope Inspectors. | Object-store bytes and PostgreSQL metadata remain consistent; checksum/source/uploader are server-traceable; retry is idempotent; corrupt content is rejected and unrelated Inspectors receive INSPECTION_SCOPE_DENIED. | Inspection is in progress; PostgreSQL and an S3-compatible test endpoint are available (S3Mock in CI; MinIO for runtime verification); a supported image is available. | Passed | 2026-09-24 | Codex (automated) | Passed | 2026-09-25 | Codex (GitHub Actions) | Pending |  |  | The 2026-09-24 full backend verification passed using real PostgreSQL and MinIO containers. GitHub Actions run 36090635549 initially failed before tests because the MinIO image pull was unauthorized. After switching the test containers to S3Mock 5.2.3, full backend verify run 36092639825 passed: EvidenceApiIntegrationTest (3 tests) and MinioEvidenceObjectStoreIntegrationTest (1 test) both passed. S3Mock covers the S3 API subset and is not a MinIO server test. The post-change local targeted run could not start because the Docker Desktop API pipe was unavailable. |

## Coverage boundary

The current WF3-002 case records source metadata and storage traceability. It does not separately identify an assertion for optional GPS or external mission references.
