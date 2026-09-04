---
title: "Architecture & Design Decisions"
weight: 30
---

# Architectural Decision Records (ADRs)

## ADR-001: Minimal Clean Architecture & Vertical Slice Architecture (VSA)
* **Status**: Accepted
* **Context**: The four-person team needs to develop distinct business modules concurrently without git merge bottlenecks in monolithic controller files or multi-layer ceremony.
* **Decision**: Adopt **Minimal Clean Architecture** (single-project Vertical Slice Architecture). Each feature lives in `Features/<Module>/<Action>/` containing its Endpoint, Request/Response DTOs, and Validator.
* **Consequences**:
  * Eliminates Git merge conflicts across team members.
  * Faster build and testing iteration.
  * Preserves domain encapsulation and testability.

---

## ADR-002: FastEndpoints (REPR Pattern) over MVC Controllers
* **Status**: Accepted
* **Context**: Traditional ASP.NET Core MVC controllers easily devolve into God Controllers with multiple injected dependencies and hundreds of lines of code.
* **Decision**: Use **FastEndpoints** enforcing the Request-Endpoint-Response (REPR) pattern. Each endpoint is a single class with a single responsibility.
* **Consequences**:
  * Strict Single Responsibility Principle (SRP).
  * High-throughput Kestrel routing performance.
  * Native FluentValidation and Swagger integration.

---

## ADR-003: Consumer-Only Integration with SmartDroneHub REST API
* **Status**: Accepted
* **Context**: Drone flight control and hardware telemetry are handled by the external **SmartDroneHub** platform developed by AiTA Lab.
* **Decision**: SmartDroneInspection acts strictly as a **Consumer** calling SmartDroneHub via REST API to create flight missions and ingest post-flight telemetry, logs, and 4K images.
* **Consequences**:
  * Clear architectural boundaries.
  * Eliminates drone hardware control risks from the capstone scope.

---

## ADR-004: PostgreSQL 17 + pgvector for Hybrid Business & AI Storage
* **Status**: Accepted
* **Context**: Need a robust database supporting both transactional relational data (30 tables) and high-dimensional semantic search for AI knowledge retrieval.
* **Decision**: Use **PostgreSQL 17 with the `pgvector` extension** and **HNSW Cosine Index** (`vector(1536)`).
* **Consequences**:
  * Single database technology for both business transactions and vector embeddings.
  * Sub-millisecond similarity search across historical failure cases.

---

## ADR-005: 3-Tier AI Strategy
* **Status**: Accepted
* **Decision**:
  1. **DroneVisionAI**: Computer Vision model (YOLOv8/11 + SAHI) for automated defect detection on 4K drone imagery.
  2. **DroneKnowledgeAI**: RAG pipeline retrieving historical resolution cases via pgvector.
  3. **Report Summarization**: LLM-based executive summary generation for managers.

---

## ADR-006: SignalR Real-Time Telemetry Streaming
* **Status**: Accepted
* **Decision**: Stream live drone coordinates, battery status, and mission progress to the React web portal and Flutter mobile app using ASP.NET Core SignalR hubs.
