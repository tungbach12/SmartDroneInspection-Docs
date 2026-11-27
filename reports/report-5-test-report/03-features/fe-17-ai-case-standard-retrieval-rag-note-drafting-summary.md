# FE-17: AI Case/Standard Retrieval (pgvector RAG), Note Drafting & Report Summary

Synchronized with Report 3 SRS v2.2 and Report 4 SDD v2.4; upstream of the `(FE-17)` test sheet in `Report5_Test Report.xlsx`.

## Feature sheet summary

Values for the `Feature 17` summary block (`A2:E8` in the workbook).

| Cell | Label | Value |
| --- | --- | --- |
| `B2` | Feature | AI Case/Standard Retrieval (pgvector RAG), Note Drafting & Report Summary |
| `B3` | Test requirement | Verifies tenant-isolated `DroneKnowledgeAI` recommendation lookup (`inspection_knowledge_chunks`, `historical_finding_cases` backfilled in `V64`), local `fastembed` `vector(384)` cosine retrieval (`V65`) with `HYBRID_MATCH` fallback, per-finding and batch AI note drafting (`Draft note with AI` / `Draft all notes`), Mobile `KnowledgeReferencesStrip`, and `ReportAiSummaryCard` executive summary references. |

## Test case execution records

| Test Case ID | Test Case Description | Test Case Procedure | Expected Results | Pre-conditions | Round 1 | Test date | Tester | Round 2 | Test date | Tester | Round 3 | Test date | Tester | Note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| WF3-029 | AI note drafting (DroneKnowledgeAI), local 384-dim RAG retrieval, confirmation filters, and tenant isolation. | 1. Filter findings by All / Unconfirmed / Confirmed status.<br>2. Click Draft Note with AI on a finding and Run Batch Draft.<br>3. Inspect matched historical cases and standards footer plus Mobile strip parity. | AI drafts grounded notes referencing top matched standards/cases; auto-confirm threshold respects policy; historical benchmark cases isolate organization PII; Mobile renders matched references cleanly. | Inspection with findings; 384-dim vector index and local embedding service active. | N/A |  |  | N/A |  |  | Passed | 2026-11-20 | Trần Tùng Bách | Verified via automated backend & Web regression suite (Nov 2026). |
| WF3-030 | AI Executive Summary displays advisory narrative and matched historical cases/standards footer. | 1. Generate an AI Executive Summary on an inspection with confirmed findings.<br>2. Inspect the summary narrative and the Matched Cases & Standards footer.<br>3. Submit and review the report as an independent Manager. | Summary displays grounded narrative marked clearly as advisory alongside matched references and similarity scores without altering report approval rules. | Field-completed inspection with confirmed findings and seeded reference cases. | N/A |  |  | N/A |  |  | Passed | 2026-11-20 | Trần Tùng Bách | Verified via automated backend & Web regression suite (Nov 2026). |
| WF3-038 | AI retrieval degrades gracefully on embedding errors and supports Vietnamese note drafting. | 1. Simulate embedding service failure or mismatched vector dimensions during historical case retrieval.<br>2. Request deterministic note drafting with Vietnamese locale and an existing Inspector draft. | Retrieval falls back cleanly to lexical matching without throwing an error; deterministic drafting generates compact Vietnamese notes while preserving existing Inspector comments. | Published historical cases, standards table, and mock embedding failure state. | N/A |  |  | N/A |  |  | Passed | 2026-11-27 | Trần Tùng Bách | Verified via HistoricalCaseServiceTest fallback & locale unit tests. |
