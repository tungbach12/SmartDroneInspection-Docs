---
title: "Report 3 - Non-Functional Requirements"
document_type: report3-srs-section
weight: 45
source: "report3-software-requirement-specification.docx"
---

## 4. Non-Functional Requirements

This section specifies the non-functional requirements and quality attributes for the SmartDroneInspection platform, defining the architectural performance, reliability, security, maintainability, and external interface standards necessary for enterprise-grade operation across cloud and mobile environments.

### 4.1 External Interfaces

- **Web Browser Client:** The responsive web application (React, TypeScript, Material-UI) communicates over secure HTTPS with strict TLS 1.3 encryption. Supports current evergreen versions of Google Chrome, Microsoft Edge, Mozilla Firefox, and Apple Safari across desktop and tablet viewports.
- **Mobile Client:** The field inspection mobile application (Flutter, Dart) operates on modern Android (API 28+) and iOS (15+) devices. Mobile authentication utilizes secure on-device credential storage (Android Keystore, iOS Keychain) with encrypted biometric/PIN session unlock.
- **RESTful Application Programming Interface:** Backend microservices expose versioned REST APIs under `/api/v1`. Successful API responses follow a standardized JSON envelope (`{ success, message, data }`) while preserving HTTP semantic statuses (200, 201, 204). Error responses adhere to the RFC 9457 Problem Details standard, supplying machine-readable error codes and unique request trace IDs.
- **Database & Object Storage:** Relational and spatial data are persisted in PostgreSQL 17 with `pgvector` extensions for embeddings. High-resolution imagery, video captures, and generated PDF reports are persisted in S3-compatible object storage (MinIO) with pre-signed URL access controls.
- **AI Computer Vision & Language Services:** Dedicated microservices communicate via REST. The YOLO11s computer vision microservice ingests image bytes and returns structured bounding boxes and defect classifications. The LLM drafting service synthesizes structured Markdown report narratives from grounded database prompts.
- **Payment Gateway (PayPal):** Interfaces with PayPal REST API v2 (`/v2/checkout/orders`) over HTTPS TLS 1.3 to execute online enterprise subscription orders, capture authorizations, and receive asynchronous IPN webhook event notifications (`PAYMENT.CAPTURE.COMPLETED`) with HMAC-SHA256 signature verification.
- **Aviation & Geospatial Interfaces:** Integrates geospatial mapping layers (OpenStreetMap / Leaflet) and public aviation advisory sources (e.g., Civil Aviation Authority / Ministry of National Defence airspace portals) for visual flight planning.

### 4.2 Quality Attributes

#### 4.2.1 Usability

- **Intuitive Workflow Guidance:** Operational screens guide users through logical sequence steps (Preparation → Flight Session → Evidence → Findings → Report → Maintenance). Complex multi-step actions feature progress steppers and contextual validation hints.
- **High-Contrast Outdoor Readability:** The mobile application provides high-contrast typography, large touch targets (minimum 48x48 dp), and outdoor-optimized color schemes suitable for direct sunlight field conditions.
- **Clear AI Delineation:** Machine-generated defect candidates and draft texts are visually distinguished from human-verified findings using distinctive badges, ensuring reviewers clearly perceive automated suggestions versus official data.
- **Accessibility Standards:** Web interfaces comply with Web Content Accessibility Guidelines (WCAG 2.1) Level AA, ensuring full keyboard navigation, aria-labels for screen readers, and high text contrast ratios (minimum 4.5:1).

#### 4.2.2 Reliability and Record Integrity

- **Transactional Atomicity:** Multi-entity operations (e.g., asset creation with default pair, inspection creation with pair snapshot, report publication with PDF archival) execute within atomic database transactions to prevent partial or orphaned records.
- **Idempotent Operations:** File uploads, due-cycle mission generations, and report publication requests are fully idempotent; duplicate submissions with identical SHA-256 digests or parameters are safely deduplicated without creating duplicate state.
- **Cryptographic Evidence Integrity:** All uploaded inspection photographs and documents are fingerprinted using server-calculated SHA-256 cryptographic hashes immediately upon ingestion, guaranteeing proof of tamper-free storage.
- **Graceful Degradation:** If automated AI defect detection or LLM drafting services become temporarily unreachable, the system allows inspectors to proceed with full manual defect recording and structured report authoring without loss of data.
- **Deterministic Financial Computation:** Financial calculations for budgets, itemized estimates, approved change orders, and actual costs use fixed-precision decimal arithmetic to prevent floating-point rounding discrepancies.

#### 4.2.3 Performance

- **API Response Latency:** Under standard enterprise workload, 95% of standard JSON API requests complete within 2.0 seconds (excluding large binary file upload/download transfer times).
- **Efficient Data Pagination:** All tabular data queries across assets, missions, evidence items, findings, and work orders utilize server-side indexed pagination with stable sorting, ensuring rapid rendering regardless of catalog size.
- **Asynchronous Processing:** Long-running operations such as deep learning defect inference, PDF document rendering, and batch email dispatch execute asynchronously in background task queues without blocking user interface responsiveness.
- **Scalable Image Optimization:** The system automatically generates optimized responsive image thumbnails upon upload to enable rapid gallery rendering while preserving original full-resolution files for detailed inspection.

#### 4.2.4 Security, Privacy and Maintainability

- **Strict Multi-Tenant Isolation:** Complete logical tenant data isolation is enforced at the database and application levels. Every query and command strictly verifies the authenticated user's organization tenancy.
- **Role-Based and Attribute-Based Access Control:** All endpoints enforce granular RBAC/ABAC permissions. Sensitive actions (e.g., report approval, budget release, technical acceptance) enforce mandatory separation of duties (authors cannot approve their own work).
- **Secure Authentication & Token Management:** Passwords are encrypted using Argon2id with per-user salt. Web clients store ephemeral access tokens in memory and use HttpOnly, Secure, SameSite=Strict cookies for refresh tokens to prevent cross-site scripting (XSS) and CSRF attacks.
- **Payment Security & PCI-DSS Boundaries:** Cardholder numbers, CVVs, and PayPal login credentials are processed entirely within PayPal's hosted PCI-DSS Level 1 compliant checkout interface. The application server stores only PayPal transaction tokens, capture IDs, and payment audit logs, eliminating server-side card data liability. Webhooks verify cryptographic transmission signatures before activating subscription periods.
- **Data Protection and Privacy:** Sensitive personal data (pilot health certificates, identity credentials) are restricted to authorized administrators and excluded from general staff views and external AI prompts.
- **Comprehensive Audit Logging:** Security-critical events—including login attempts, permission changes, flight readiness decisions, report publication, and financial approvals—are recorded in immutable, append-only audit logs with user identity, timestamp, and IP address.
