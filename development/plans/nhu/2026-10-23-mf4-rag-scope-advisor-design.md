# MF4 RAG-Assisted Maintenance Scope & Acceptance Criteria Advisor — Technical Design

**Owner:** Như  
**Date:** 23 October 2026  
**Status:** Implemented and Verified  
**Feature:** FE-07 / MF4; Report 3 §3.8.2 (Step MF4-02 & MF4-05)  
**Components:** `SmartDroneInspection-Backend` (maintenance, infrastructure.ai), `SmartDroneInspection-Frontend`  

---

## 1. Problem Statement & Motivation

During the initial triage of confirmed inspection findings (MF4-01 / MF4-02), an Organization Administrator (`ORG_ADMIN`) or Team Lead (`MAINTENANCE_ENGINEER`) opens a repair work order and must define two critical fields:
1. `correctiveScope`: The technical repair method, materials, surface preparation, and curing requirements.
2. `acceptanceCriteria`: Objective, quantifiable thresholds used by an independent reviewer to accept or return the physical repair (MF4-18).

### Why Standard LLM Fails (The Need for RAG)
In civil infrastructure, ungrounded generative AI suffers from severe confabulation (hallucination):
- Inventing proprietary chemical mixing ratios or non-existent material grades.
- Citing foreign or non-applicable building codes rather than approved Vietnamese Construction Standards (TCVN) or international standards (ISO, AASHTO, ACI).
- Producing vague, unverifiable statements (e.g. *"ensure the crack is fixed nicely"*).

### RAG Solution
We implement a **Retrieval-Augmented Generation (RAG)** pipeline:
1. Relevant engineering standards and manufacturer method statements (e.g., TCVN 9343:2012, ISO 12944-5, EN 1504-9, Sika method statements) are indexed into PostgreSQL using `pgvector` and an HNSW cosine distance index.
2. Defect metadata (type, dimension/measurement, structural component, severity, location) is used to retrieve top-k matching technical guidelines.
3. An OpenAI-compatible LLM synthesizes these retrieved standards into strict JSON containing actionable scope, measurable criteria, and sequential task breakdowns.
4. A **Deterministic Rule-Based Fallback** guarantees 100% availability if the external LLM is disabled or offline.

---

## 2. System Architecture & Spring Modulith Isolation

The solution strictly honors the project's **Hexagonal Architecture** and **Spring Modulith** boundary invariants:

```text
[Frontend: RepairCandidatePanel]
        │
        ▼ POST /api/v1/maintenance/suggest-scope
[Backend: MaintenanceController]
        │
        ▼
[MaintenanceScopeAdvisorService] ──────────► [DeterministicScopeFallback] (Safety Fallback)
        │                                             ▲
        ├─────────────────────────────────────────────┤ (When AI disabled or network error)
        ▼                                             │
[RepairKnowledgeChunkRepository]             [MaintenanceScopeAdvisorPort] (SPI)
(pgvector <=> & category query)                       ▲
                                                      │ implements
                                             [MaintenanceScopeAdvisorClient]
                                             (RestClient -> /v1/chat/completions)
```

### Module Boundaries
- `com.smartdroneinspection.maintenance`:
  - Contains domain models, service orchestration, and outbound SPI port `MaintenanceScopeAdvisorPort`.
  - Package `maintenance.spi` is marked with `@org.springframework.modulith.NamedInterface("spi")`.
  - **Never imports from `infrastructure`**.
- `com.smartdroneinspection.infrastructure.ai`:
  - Implements `MaintenanceScopeAdvisorPort` via `MaintenanceScopeAdvisorClient`.
  - Configures Spring `RestClient` with explicit timeouts.
  - Allowed dependency on `"maintenance::spi"` declared in `infrastructure/package-info.java`.

---

## 3. Database Schema & Vector Indexing (Flyway V29)

Flyway migration `V29__repair_knowledge_base.sql` introduces:

```sql
CREATE TABLE IF NOT EXISTS repair_knowledge_chunks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    standard_code VARCHAR(64) NOT NULL,
    title VARCHAR(255) NOT NULL,
    category VARCHAR(64) NOT NULL,
    defect_patterns VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    reference_url VARCHAR(500),
    embedding vector(1536),
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_repair_knowledge_chunks_category 
    ON repair_knowledge_chunks(category);

CREATE INDEX IF NOT EXISTS idx_repair_knowledge_chunks_hnsw 
    ON repair_knowledge_chunks USING hnsw (embedding vector_cosine_ops)
    WITH (m = 16, ef_construction = 64);
```

### Seeded Standards (5 Foundational Sets):
1. **`CONCRETE_CRACK`**: TCVN 9343:2012 / ACI 224.1R — Low-pressure epoxy injection (Sikadur-752/731), UPV velocity recovery $\ge 90\%$, pull-off adhesion $\ge 1.5\text{ MPa}$.
2. **`SPALLING`**: TCVN 9343:2012 / EN 1504-9 — Perimeter saw-cutting (20mm depth), rebar rust removal to Sa 2, zinc-rich slurry, polymer-modified repair mortar. Sound test 100% solid, pull-off $\ge 1.5\text{ MPa}$.
3. **`STEEL_CORROSION`**: ISO 12944-5 / AASHTO — Abrasive blast cleaning to Sa 2.5, 3-coat system (Zinc-rich epoxy primer, MIO intermediate, Aliphatic Polyurethane topcoat). Total DFT $\ge 225\ \mu\text{m}$, ISO 2409 adhesion rating 0–1.
4. **`WATER_LEAKAGE`**: TCVN 9343:2012 / ASTM C1583 — $45^\circ$ hole drilling intersecting crack, mechanical packers, hydrophilic PU pressure injection (15–30 bar). 72h continuous observation zero dampness.
5. **`STRUCTURAL_DEFORMATION`**: TCVN 9361:2012 / AASHTO — Closed-cell PE backer rod installation, elastomeric polyurethane sealant (Sikaflex PRO-3). Zero debonding, elongation at break $\ge 400\%$.

---

## 4. API Specification

### Endpoint: `POST /api/v1/maintenance/suggest-scope`
- **Authorized Roles:** `ORG_ADMIN`, `MAINTENANCE_ENGINEER`.
- **Request:**
  ```json
  {
    "sourceReportVersionId": "d02826e9-18bc-4cc2-9abc-36328b6bbc61",
    "sourceFindingId": "593f5492-80e5-40b7-915c-f7fbfc16fc53",
    "defectLabel": "Nứt dầm bê tông",
    "description": "Vết nứt dọc theo dầm T, bề rộng 0.35mm",
    "component": "Dầm T",
    "severity": "HIGH",
    "measurement": "0.35mm"
  }
  ```
- **Response (`ApiResponse<SuggestScopeResponse>`):**
  ```json
  {
    "success": true,
    "message": "Success",
    "data": {
      "correctiveScope": "Vệ sinh bề mặt vết nứt tại Dầm T; gắn bát bơm epoxy chuyên dụng cách nhau 150-200mm; trám kín khe nứt bằng keo trám epoxy hai thành phần Sikadur-731; bơm keo epoxy độ nhớt thấp Sikadur-752 áp lực thấp (0.15-0.35 MPa) từ dưới lên trên; bảo dưỡng tối thiểu 48 giờ.",
      "acceptanceCriteria": "Kiểm tra siêu âm xung (UPV) theo TCVN 9357:2012 đạt độ phục hồi vận tốc sóng âm >= 90%; Thử kéo đứt theo TCVN 9349 đạt cường độ bám dính >= 1.5 MPa; Bề mặt phẳng, không xuất hiện vết nứt thứ cấp sau 14 ngày.",
      "referenceStandards": ["TCVN 9343:2012", "TCVN 9357:2012", "TCVN 9349"],
      "suggestedTasks": [
        {
          "taskNumber": 1,
          "name": "Khảo sát và vệ sinh khe nứt",
          "method": "Làm sạch bằng chổi kim loại và thổi khí nén",
          "acceptanceCriteria": "Khe nứt sạch bụi và dầu mỡ"
        },
        {
          "taskNumber": 2,
          "name": "Gắn bát bơm và trám bịt khe nứt",
          "method": "Gắn bát khoảng cách 150-200mm, trám keo epoxy cường độ cao",
          "acceptanceCriteria": "Keo trám kín kín khít, chịu được áp lực bơm 0.4 MPa"
        }
      ],
      "modelName": "gpt-4o-mini",
      "fallbackApplied": false
    }
  }
  ```

---

## 5. Frontend User Experience (UX)

In `SmartDroneInspection-Frontend/src/features/maintenance/components/RepairCandidatePanel.tsx`:
1. The **"Open work order"** modal displays a dedicated action header:
   ```tsx
   <LoadingButton
     size="small"
     variant="outlined"
     startIcon={<AutoAwesomeOutlined />}
     loading={suggestScope.isPending}
     onClick={() => handleAiSuggest()}
   >
     {t('AI Suggest Scope & Criteria (RAG)')}
   </LoadingButton>
   ```
2. When clicked:
   - Spinner activates on the button while awaiting inference.
   - Automatically populates both multiline inputs: `correctiveScope` and `acceptanceCriteria`.
   - Renders interactive MUI `Chip` badges for each cited standard (e.g. `[TCVN 9343:2012]`, `[ISO 12944-5]`) to provide clear engineering provenance.
   - The user retains 100% control to review and fine-tune the drafted text before saving.

---

## 6. Verification & Automated Test Coverage

- **`DeterministicScopeFallbackTest.java`**: 5 unit tests validating that each defect domain (cracking, spalling, corrosion, leakage, general) generates non-blank, standard-grounded scopes and quantifiable criteria.
- **`MaintenanceScopeAdvisorClientTest.java`**: 2 unit tests with local HTTP server verifying JSON prompt serialization, SSE avoidance, and `extractJsonObject` robustness.
- **`MaintenanceScopeAdvisorServiceTest.java`**: 3 unit tests verifying multi-tenant isolation, AI response conversion, and seamless fallback activation upon timeout.
