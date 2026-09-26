# FE-05: YOLO-assisted Defect Detection and Verification

## Scope baseline

Server-side inference generates candidates with defect label, confidence, bounding box and model version. Inspector Confirm, Modify, Reject and Manual Add actions determine official findings. Unverified candidates are excluded from official defect statistics.

## Current acceptance case

WF3-003 maps to FE-05.

| Test Case ID | Test Case Description | Test Case Procedure | Expected Results | Pre-conditions | Round 1 | Test date | Tester | Round 2 | Test date | Tester | Round 3 | Test date | Tester | Note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| WF3-003 | Inspector verifies AI candidates or records a manual finding. | Send eligible evidence to the deterministic inference stub; verify candidate provenance; confirm, modify, and reject candidates; create a manual finding; exercise inference failure and inspect official report findings. | Candidate decisions are scoped and auditable; only verified/manual findings become official; pending/rejected candidates stay non-official; an inference failure leaves evidence and manual entry usable. | Eligible evidence exists; deterministic inference stub and authorized Inspector are available. | Passed | 2026-09-24 | Codex (automated) | Pending |  |  | Pending |  |  | AiFindingServiceTest and AiFindingApiIntegrationTest passed with state/scope coverage; YoloInferenceClientTest and configuration tests passed using a local HTTP stub. No deployed/live YOLO model was connected; this result verifies the configured adapter contract and deterministic workflow. |
