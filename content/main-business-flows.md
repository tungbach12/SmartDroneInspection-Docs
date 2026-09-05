---
title: "Main Business Flows — Details & Priority"
weight: 15
---

# Main Business Flows — Details & Priority (Production-Level)

This document is the **single source of truth** for the end-to-end business flows of SmartDroneInspection. It defines each flow in production-grade detail (actors, triggers, state transitions, exit criteria) and assigns an implementation priority based on real-world inspection platform and CMMS practices.

Sources grounding these decisions:
* Industry drone inspection workflow standards (mission planning → flight → processing → AI detection → **human review** → report).
* CMMS work-order lifecycle best practices (6-stage lifecycle: request capture → triage → assignment → execution → verified closure → analysis).
* Human-in-the-Loop (HITL) paradigms for AI-assisted civil infrastructure inspection.

---

## 1. Priority Model

| Priority | Meaning | Scope Rule |
| :--- | :--- | :--- |
| **P0 — Core Loop** | The inspection closed loop must run end-to-end. Required for capstone defense demo. | No P0 feature may ship without its state machine + audit trail. |
| **P1 — Production Completeness** | Required for a credible production deployment, but demo can be performed without it. | Slated for WP5 (testing/hardening phase). |
| **P2 — Enhancement** | Analytics, optimization, nice-to-have UX. | Only after P0/P1 are stable. |

The **P0 spine** (must-work demo path):

```text
Asset exists → Plan/Request approved → Drone mission executed via SmartDroneHub
→ AI detects defects (HITL confirmed by Inspector) → Report approved by Manager
→ Maintenance ticket assigned → Engineer closes ticket → Asset history updated
```

---

## 2. MF1 — Asset Management (Priority: P0)

**Owner role**: Administrator, Inspection Manager.
**Entities**: `Asset`, `AssetCategory`, `AssetDocument`, `AssetLifecycleLog`.

1. Admin/Manager creates an **Asset Category** (e.g., Bridge, Transmission Tower, Solar Farm).
2. Manager registers an **Asset**: name, unique code (normalized for search), specifications, GPS coordinates (lat/long), category, organization.
3. Manager uploads **technical documents** (PDF drawings, manuals) → stored in MinIO, metadata in `asset_documents`.
4. Every status change (Active → UnderMaintenance → Retired) appends an entry to `asset_lifecycle_logs` (immutable history).

Production rules:
* Asset code uniqueness enforced per organization (unique index on normalized code).
* Soft delete only — retired assets remain queryable for historical inspections.
* All reads are organization-scoped (multi-tenant boundary via `OrganizationId` in every specification).

---

## 3. MF2 — Inspection Planning & Request (Priority: P0)

**Owner role**: Inspection Manager.
**Entities**: `InspectionPlan`, `InspectionSchedule`, `InspectionRequest`, `InspectionCalendarEvent`, `Notification`.

1. Manager creates a **Plan**: target assets, frequency (weekly/monthly/quarterly), priority, assigned inspector pool.
2. System generates **Schedules** from plan frequency; each due date produces a calendar event + notification.
3. A schedule (or ad-hoc need) generates an **Inspection Request** (`Pending`).
4. Manager reviews and decides: `Approved` / `Rejected` (with reason) / `Cancelled`.
5. On approval → flow proceeds to MF3 (mission creation).

Production rules:
* Request state machine is explicit: `Pending → Approved | Rejected | Cancelled`; invalid transitions are rejected at the domain level (Guard clauses), not just the API level.
* Duplicate-request guard: an asset cannot have two open requests for the same scheduled window (idempotency check before create).

---

## 4. MF3 — Drone Mission Integration via SmartDroneHub (Priority: P0)

**Owner role**: System (automated) + Inspection Manager (oversight).
**Boundary rule**: SmartDroneInspection is a **consumer** of the SmartDroneHub Mission API — never a drone controller.

1. Approved inspection request triggers `POST` to SmartDroneHub Mission API (typed `HttpClient`, resiliency: retry + timeout + circuit breaker).
2. Mission status is streamed back via **SignalR** hub to Web/Mobile dashboards in real time.
3. On mission completion, the system pulls: **telemetry** (`mission_telemetry`), **4K images** (`mission_images` → MinIO), **flight logs** (`mission_flight_logs`).
4. Images are linked to the mission and become the input corpus for MF4 AI analysis.

Production rules:
* Outbound integration failures must not corrupt local state: mission record persists with `IntegrationFailed` status and a retry mechanism.
* Every inbound payload is validated and persisted transactionally (telemetry bulk-insert, images deduplicated by hash).

---

## 5. MF4 — Inspection Report & Defect Management (AI + HITL) (Priority: P0 core, P1 for AI)

**Owner role**: Inspector (findings), Inspection Manager (approval).
**Entities**: `InspectionReport`, `ReportFinding`, `ReportEvidence`, `Defect`, `DefectEvidence`.

1. Inspector opens the completed mission's image set.
2. **DroneVisionAI** (P1 for model quality; P0 uses manual finding entry fallback) scans images and proposes candidate defects with bounding boxes + confidence scores.
3. **Human-in-the-Loop review (mandatory)**: Inspector validates each AI finding — confirm (→ `Defect` with severity), edit, or reject as false positive. Raw AI output is never auto-promoted to a defect.
4. Inspector attaches **evidence** (annotated imagery) and writes findings into an **Inspection Report** (`Draft`).
5. Report submitted (`Submitted`) → Manager reviews → `Approved` or `Rejected` (with reason, back to Inspector).
6. Approved report can be summarized by an LLM (`Summary`, `SummaryModelVersion` recorded) for executive readers.

Production rules:
* Report state machine: `Draft → Submitted → Approved | Rejected`; `Rejected` returns to `Draft` with mandatory reject reason.
* Defect lifecycle tracked independently: `Open → Confirmed → InRepair (linked ticket) → Resolved → Verified`.
* Every AI proposal stores model version + confidence for auditability and future model improvement (active-learning loop).

---

## 6. MF5 — Maintenance Ticket Lifecycle (Priority: P0)

**Owner role**: Maintenance Engineer; tickets originate from confirmed defects.
**Entities**: `MaintenanceTicket`, `TicketHistory`.

Implements the industry-standard 6-stage work-order lifecycle:

1. **Request capture**: confirmed defect auto-proposes a ticket (defectId linked); manual tickets also allowed.
2. **Triage & prioritization**: severity (defect) + asset criticality → ticket priority (`Low/Medium/High/Critical`). Emergency bypass: `Critical` severity on safety-relevant assets skips the normal queue.
3. **Assignment & planning**: Manager/engineer lead assigns a Maintenance Engineer, sets due date and estimated cost.
4. **Execution & tracking**: engineer updates status `Open → InProgress`; progress entries append to `ticket_history`.
5. **Verified closure**: closing requires resolution notes, actual cost, and status `Resolved → Closed`. Closure data is mandatory (no silent closes).
6. **Analysis & learning**: closed ticket data feeds asset history, maintenance KPIs, and (via DroneKnowledgeAI RAG) becomes retrievable knowledge for future similar defects.

Production rules:
* Ticket state machine: `Open → InProgress → Resolved → Closed` (+ `Cancelled`); every transition writes `ticket_history` with actor + timestamp.
* SLA targets (from CMMS practice): Critical = same-day response, High ≤ 72h, Medium/Low = scheduled backlog.

---

## 7. MF6 — Authentication, RBAC & Audit (Priority: P0 — enabler)

**Entities**: `User`, `Organization`, `RefreshToken`, `AuditLog`.

1. Login with email + password (PBKDF2 hashing, constant-time verification, account lockout after 5 failures).
2. JWT access token (short-lived) + single-use refresh token rotation (old token revoked on refresh).
3. All endpoints enforce role-based authorization: `Administrator`, `InspectionManager`, `Inspector`, `MaintenanceEngineer`, `Viewer`.
4. Sensitive mutations (approve, assign, delete, ticket transitions) write `audit_logs` entries.

---

## 8. Cross-Cutting Flows (Priority: P1/P2)

* **Notifications (P1)**: schedule reminders, request decisions, ticket assignments — via `notifications` table + UI toasts (email/webhook channels are P2).
* **Dashboards & Analytics (P2)**: inspection KPIs, defect density per asset class, maintenance MTTR, asset condition trend.
* **DroneKnowledgeAI RAG (P1)**: on defect confirmation, retrieve top-K similar historical cases (pgvector HNSW cosine) and attach recommendations to the ticket.

---

## 9. Implementation Priority Summary

* **P0 (Core loop, defense-critical)**: MF1, MF2, MF3 (with SmartDroneHub mock/stub fallback), MF4 (manual finding path + report state machine), MF5 (ticket lifecycle), MF6 (auth/RBAC).
* **P1 (Production completeness)**: DroneVisionAI integration + HITL tooling, DroneKnowledgeAI RAG, notifications, LLM report summarization hardening.
* **P2 (Enhancement)**: analytics dashboards, KPI exports, email/webhook channels, advanced asset condition modeling.

Team members should map their Work Packages against this priority table: WP2/WP3 cover the P0 spine; WP4 delivers the P1 AI services; WP5 hardens P1/P2.
