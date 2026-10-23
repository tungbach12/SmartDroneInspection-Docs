# Project Report — Week 7

**Project name:** SmartDroneInspection: AI-powered Infrastructure Inspection Management Platform  
**Group:** FA26SE112  
**Reporting period:** 19–23 October 2026  
**Personal contribution recorded:** Trương Thái Như (WF4 / FE-07 Owner)  

---

## I. Status Report

| # | Project Task | In-charge | Status | Notes (Work Item in Details) |
|---:|---|---|---|---|
| 1 | Implement RAG-Assisted Scope & Criteria Advisor | Trương Thái Như | Completed & Verified | Created Flyway migration `V29__repair_knowledge_base.sql` with `repair_knowledge_chunks` table, `vector(1536)` embeddings, and HNSW cosine distance index; seeded 5 civil engineering standards (TCVN, ISO, EN, ASTM); built `MaintenanceScopeAdvisorPort` SPI and `MaintenanceScopeAdvisorClient` RestClient; implemented `DeterministicScopeFallback` for zero-downtime safety; integrated "AI Suggest Scope & Criteria (RAG)" button into `RepairCandidatePanel.tsx`. |
| 2 | Remediate 6 WF4 End-to-End Workflow Defects | Trương Thái Như | Completed & Verified | Fixed task ID binding in cost reconciliation (unblocking closure); implemented team lead work log verification button (satisfying `markWorkCompleted`'s prerequisite); added state-guards on transition buttons to prevent 409 errors; hardened budget approver validation; added closed work order immutability guards; and added PDF completion report download link. |
| 3 | Author Comprehensive MF4 Technical Documentation Suite | Trương Thái Như | Completed | Authored 3 in-depth technical documents in `development/plans/nhu/`: `2026-10-23-mf4-rag-scope-advisor-design.md`, `mf4-api-and-contracts.md`, and `mf4-verification-and-bug-fixes.md`; synchronized personal development plan with day-by-day work log. |
| 4 | Run Integration & Unit Regression Tests | Trương Thái Như | Completed (100% Passed) | Ran all 25 `MaintenanceApiIntegrationTest` cases, 5 `DeterministicScopeFallbackTest` cases, 3 `MaintenanceScopeAdvisorServiceTest` cases, 2 `MaintenanceScopeAdvisorClientTest` cases, and `ModulithArchitectureTest`. All passed with 0 errors. |

---

## II. Project Issues

| # | Project Issue | Owner | Status | Notes (Solution, Suggestion, etc.) |
|---:|---|---|---|---|
| 1 | Cost reconciliation form previously sent finding ID instead of task ID | Trương Thái Như | Resolved | Corrected frontend form to populate and pass valid planned task IDs to `reconcile()` endpoint. |
| 2 | Inability to declare work completed due to unverified work logs | Trương Thái Như | Resolved | Added inline "Verify work log" action button for team leads in `WorkOrderDetailPanel.tsx`. |

---

## III. Next Week Plan

| # | Project Work Item | In-charge | Deadline | Notes (Task Details, etc.) |
|---:|---|---|---|---|
| 1 | Finalize end-to-end integration demo with live drone flight data | Trương Thái Như & Team | 26 Oct 2026 | Rehearse complete lifecycle: Drone inspection (MF2) -> Report publication (MF3) -> RAG Work order triage & repair closure (MF4). |
| 2 | Prepare final capstone presentation slides and defense artifacts | Trương Thái Như & Team | 28 Oct 2026 | Highlight RAG architecture, governance separation of duties, and verifiable test evidence. |
