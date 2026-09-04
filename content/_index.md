---
title: "SmartDroneInspection Documentation"
type: "docs"
weight: 1
---

# SmartDroneInspection Documentation

**SmartDroneInspection** (Capstone FA26SE112 — FPT University SWE) is an enterprise **Infrastructure Inspection & Maintenance Management Platform** built on the principles of **Ardalis Clean Architecture** and **Vertical Slice Architecture (VSA)**.

## Core System Philosophy

SmartDroneInspection manages the end-to-end lifecycle of infrastructure inspection:

1. **Asset Management**: Tracking bridges, transmission towers, wind turbines, and industrial assets with GPS coordinates and technical documentation.
2. **Inspection Planning**: Automated and periodic scheduling of drone inspection requests.
3. **Drone Mission Integration**: Consuming the external **SmartDroneHub REST API** (AiTA Lab) for flight operations, streaming telemetry via SignalR, and capturing high-resolution 4K imagery to MinIO Object Storage.
4. **AI-Powered Defect Detection**: Integrated **DroneVisionAI** (YOLOv8/11 + SAHI) for automated crack/corrosion detection, plus **Report Summarization** via LLM.
5. **Knowledge & Maintenance RAG**: **DroneKnowledgeAI** using PostgreSQL `pgvector` with HNSW Cosine Index for semantic retrieval of historical failure cases and repair procedures.
6. **Closed-Loop Maintenance**: Automated work-order ticket creation, assignment to Maintenance Engineers, and asset degradation history logging.

---

## Architectural Foundation

The backend adopts **Ardalis Clean Architecture** with two pragmatic options:

* **Minimal Clean Architecture (`MinimalClean`)**: A single-project Vertical Slice Architecture powered by **FastEndpoints (REPR pattern)**, **Ardalis.Specification**, **Ardalis.SmartEnum**, and **Vogen Strongly-Typed IDs**. Ideal for rapid iteration, modularity, and zero git merge conflicts.
* **Full Clean Architecture (`Clean.Architecture.*`)**: A traditional 4-layer separation (`Core`, `UseCases`, `Infrastructure`, `Web`) for strict compiler-enforced boundary isolation.

---

## Workspace Layout

SmartDroneInspection is structured across four repositories:

* **`backend/`**: ASP.NET Core 9/10 Web API (PostgreSQL + pgvector, FastEndpoints, MediatR/Ardalis.Specification, MinIO, SignalR).
* **`frontend/`**: React 19 + TypeScript + Vite + Material UI web portal (TanStack Query, Zustand).
* **`mobile/`**: Flutter cross-platform mobile app for field inspectors & maintenance engineers (Clean Architecture, Riverpod, GoRouter).
* **`docs/`**: Hugo-powered architectural documentation and team conventions.
