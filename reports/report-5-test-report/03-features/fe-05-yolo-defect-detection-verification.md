# FE-05: YOLO-assisted Defect Detection and Verification

## Scope baseline

**Historical v1 scope record:** The earlier backend baseline included a YOLO adapter contract and candidate-review behavior. The reset removed the inspection workflow services; adapter/config or entity presence alone does not establish a current AI workflow. The current target uses AI Vision candidates plus LLM drafting with human review. Preserve the v1 notes below as historical evidence; they are not current runtime guarantees.

## Historical v1 acceptance case (retired from the Enterprise SaaS target)

WF3-003 maps to FE-05 in the earlier v1 baseline. Preserve the recorded outcome and detailed notes as historical test evidence, not as proof that the AI/inference workflow remains available in the reset branch; its inspection workflow services were removed. The target AI Vision/LLM acceptance checks remain Pending in FE-06.

| Test Case ID | Test Case Description | Test Case Procedure | Expected Results | Pre-conditions | Round 1 | Test date | Tester | Round 2 | Test date | Tester | Round 3 | Test date | Tester | Note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| WF3-003 | Inspector verifies AI candidates or records a manual finding. | Send eligible evidence to the deterministic inference stub; verify candidate provenance; confirm, modify, and reject candidates; create a manual finding; exercise inference failure and inspect official report findings. | Candidate decisions are scoped and auditable; only verified/manual findings become official; pending/rejected candidates stay non-official; an inference failure leaves evidence and manual entry usable. | Eligible evidence exists; deterministic inference stub and authorized Inspector are available. | Passed | 2026-09-24 | Codex (automated) | Pending |  |  | Pending |  |  | AiFindingServiceTest and AiFindingApiIntegrationTest passed with state/scope coverage; YoloInferenceClientTest and configuration tests passed using a local HTTP stub. No deployed/live YOLO model was connected; this result verifies the configured adapter contract and deterministic workflow. |
