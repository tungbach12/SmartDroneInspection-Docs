# FE-03: Inspection Request and Work Assignment

## Implemented v1 baseline and proposed MF2 target

The existing WF2 case descriptions below describe the five-role, post-service-billing implementation baseline: periodic request handoff, Service Manager review, versioned quotation/order intent and assignment. They **do not** prove multi-provider quotation, funding, payment-partner integration, provider commission, or the proposed six-role authorization. MF2 target cases are listed separately below and remain `Pending` until executed against that implementation.

## Current acceptance cases

These four cases map to FE-03 and WF2. WF2-001 and WF2-002 were in workbook Function B; WF2-003 and WF2-004 were in Function C.

| Test Case ID | Test Case Description | Test Case Procedure | Expected Results | Pre-conditions | Round 1 | Test date | Tester | Round 2 | Test date | Tester | Round 3 | Test date | Tester | Note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| WF2-001 | System generates and routes a periodic request for Service Manager review. | A recurring inspection schedule reaches its due cycle; the system generates the PERIODIC request with scope, priority, access constraints, and contact inherited from the asset profile, dispatches the Client notification, and routes the request to the Service Manager. | PERIODIC request is created once for the due cycle with inherited asset defaults; the Client notification is recorded; the request is available to the Service Manager for review. | Active asset with inspection defaults and active schedule reached due cycle. | Pending |  |  | Pending |  |  | Pending |  |  | Pending |  |  |  |
| WF2-002 | Service Manager prepares and sends a quotation. | Sign in as Service Manager; open the request; add price, scope, and validity; save a version; send it. | A versioned quotation is stored and visible to the correct client; prior versions remain traceable. | Request is actionable; manager is active. | Pending |  |  | Pending |  |  | Pending |  |  |  |
| WF2-003 | Client approves a quotation and confirms the service order. | Sign in as Client; review the latest quotation; approve it; open the order and billing status. | The approved quotation becomes the confirmed order; the first service billing milestone is recorded. | Quotation is in an approvable state; client owns the request. | Pending |  |  | Pending |  |  | Pending |  |  |  |
| WF2-004 | Service Manager assigns an Inspector with assignment scope. | Sign in as Service Manager; assign an active Inspector; open the task as the Inspector; attempt an unrelated task. | Assigned Inspector can access only the assigned task; unassigned or conflicting access is denied. | Confirmed order exists; candidate Inspector is active. | Pending |  |  | Pending |  |  | Pending |  |  |  |




## WF1 schedule-proposal revision (2026-09-28)

The 2026-09-28 WF1 revision adds the due-cycle event, document-upload rules, and the negative scope sweep. These three cases map to FE-03 and WF1 on the `Feature 1` workbook sheet. `WF1-017` is a **producer-side** verification: it asserts event identity, payload, and per-cycle idempotency with an in-process listener standing in for the WF2 consumer. The consumer half (one `PERIODIC` request per replayed event) is pending T021.

| Test Case ID | Test Case Description | Test Case Procedure | Expected Results | Pre-conditions | Round 1 | Test date | Tester | Round 2 | Test date | Tester | Round 3 | Test date | Tester | Note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| WF1-017 | The due-cycle publisher emits one event per cycle. | Force `next_due_at` into the past; run the publisher twice; inspect the published events. | Exactly one `InspectionScheduleDue` event carries the correct organization, asset, checklist template, and due cycle; a replayed run publishes nothing. | An `ACTIVE` schedule has `next_due_at` in the past. | Passed | 2026-09-28 | Hiếu | Passed | 2026-09-28 | Hiếu | Passed | 2026-09-28 | Hiếu | Automated evidence: `PeriodicRequestHandoffTest.publishesExactlyOneEventPerDueScheduleCycleAndReplayIsSilent`; `AssetWorkflowIntegrationTest.fullWf1FlowFromAssetCreationToDueEvent`. |
| WF1-018 | Asset document upload is validated and scoped. | Upload a png/jpeg/webp/pdf within 10 MB to an active asset; upload an unsupported type, an oversize file, and a document to a pending asset; list and stream as another organization. | Only supported types within the size limit reach storage; unsupported types and oversize files are rejected; a pending asset rejects upload; another organization cannot list or stream the document. | An active asset exists; type and size fixtures are available. | Passed | 2026-09-28 | Hiếu | Passed | 2026-09-28 | Hiếu | Passed | 2026-09-28 | Hiếu | Automated evidence: `AssetDocumentApiIntegrationTest.activeAssetDocumentUploadsAndListsForOwnOrgOnly`; `unsupportedTypeOversizeAndPendingAssetsAreRejected`; `returnsAssetOnlyForItsOrganization`. |
| WF1-019 | Negative scope sweep across every WF1 endpoint. | Exercise each WF1 endpoint across two organizations and the five roles, including unauthenticated access. | Role and organization scope are enforced on every endpoint; a Service Manager cannot create assets or manage the catalog; a Client cannot review assets; unauthenticated access returns a Problem Details 401. | Two organizations and the five role fixtures exist. | Passed | 2026-09-28 | Hiếu | Passed | 2026-09-28 | Hiếu | Passed | 2026-09-28 | Hiếu | Automated evidence: `AssetWorkflowIntegrationTest.negativeScopeSweepAcrossEveryWf1Endpoint`; `managerReviewQueueIsPlatformScopedAndClosedToOtherRoles`. |

## Coverage boundary

WF1-004 and WF1-017 verify the existing producer-side schedule event; WF2-001 remains Pending for the consumer-side automated periodic request with inherited defaults. None of these cases verifies Provider bidding or conditional funding.

## Proposed MF2 target cases (not executed)

The fixed workbook `Feature 1` sheet remains the output grouping. These are additional FE-03 cases, all Pending in every round; the quoted `r` is the same published Platform rate for every Provider and is not yet assigned a numerical percentage.

| Test Case ID | Test Case Description | Test Case Procedure | Expected Results | Pre-conditions | Round 1 | Test date | Tester | Round 2 | Test date | Tester | Round 3 | Test date | Tester | Note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| WF2-005 | Verified Provider may quote only eligible RFQs; competitors cannot inspect each other's bid. | Create two verified Provider organizations and one unverified Provider; publish an RFQ; submit two quotations; attempt unverified bid and cross-Provider quotation read. | Only verified eligible Providers can bid; each sees own bid and approved customer request context; rival pricing remains hidden. | Two Provider orgs, one unverified org and a Client RFQ exist. | Pending |  |  | Pending |  |  | Pending |  |  | Target MF2; no runtime evidence. |
| WF2-006 | Platform publishes one Provider commission rule and excludes AI/data charges from Provider quotation. | Publish one policy `r`; have two Provider orgs accept it; prepare quotations with service subtotal, Provider-funded discount and applicable Provider tax; attempt separate AI/LLM/MinIO charge and Provider-specific `r`. | Both Providers receive the same accepted policy; quotation has no Platform AI/data line; `B` excludes Provider VAT and Provider-funded discount; a Provider-specific commission override is denied. | Platform policy is published; two verified Providers and one RFQ exist. | Pending |  |  | Pending |  |  | Pending |  |  | Target policy; rate percentage not selected. |
| WF2-007 | Order locks commission policy and waits for verified payment-partner funding. | Client approves a quotation; record policy version and `r`; attempt assignment before funding; send duplicate, failed and authenticated partner success notifications; change published `r` afterward. | Confirmed order preserves original rate/version; duplicate notifications cannot duplicate funding; assignment stays blocked until authorized partner confirms the agreed funding requirement; future policy changes do not reprice existing order. | Approved Provider quotation and contracted licensed-partner test fixture exist. | Pending |  |  | Pending |  |  | Pending |  |  | Target only; no bank/payment integration is claimed. |
