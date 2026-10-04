---
title: "Report 3 - Non-Functional Requirements"
document_type: report3-srs-section
weight: 45
source: "report3-software-requirement-specification.docx"
---

## 4. Non-Functional Requirements

### 4.1 External Interfaces

- **Web browser:** The React web application communicates with the backend over HTTPS and supports current Chrome, Edge, and Firefox versions used by the project.
- **Mobile application:** The Flutter application communicates with the same versioned backend contract over HTTPS and stores mobile credentials only in platform secure storage.
- **REST API:** JSON endpoints are versioned under `/api/v1`. Successful JSON bodies use `{ success, message, data }`; HTTP status codes remain authoritative, while `204 No Content` and binary file streams are not wrapped. Errors use RFC 9457 Problem Details with a stable code and trace identifier. OpenAPI is available for development and protected appropriately in production.
- **PostgreSQL:** PostgreSQL is the source of truth for transactional state, authorization data, audit metadata, and workflow history.
- **MinIO:** S3-compatible object storage stores evidence and generated files; access is mediated by backend authorization rather than public object paths.
- **YOLO and LLM services (Platform-provided):** Platform hosts computer-vision YOLO inference and LLM narrative drafting; responses contain model version, labels, bounding boxes, or draft narrative. Providers and Clients consume these services through Platform interfaces without separate hosting or infrastructure fees.
- **Payment & Escrow Partner (target):** When conditional funding is integrated, communication occurs with licensed bank/payment intermediary APIs for transaction status confirmation and conditional release instructions; the platform does not independently operate deposit-taking accounts or act as a payment gateway.
- **Airspace Reference (target):** National restricted airspace and no-fly zone overlays reference public databases (`cambay.mod.gov.vn` per QĐ 18/2020/QĐ-TTg).

### 4.2 Quality Attributes

#### 4.2.1 Usability

- A trained user can complete the main workflow for the assigned role without developer tools.
- Validation errors identify the affected field and provide a corrective message.
- Web and mobile use consistent role names, workflow statuses, date and time formats, and action labels.
- Implemented web screens support keyboard navigation, visible focus, text alternatives, and sufficient contrast consistent with WCAG 2.1 AA targets.

#### 4.2.2 Reliability

- Committed transactional records are not lost after application restart, and multi-record workflow transitions are atomic.
- Periodic request generation is idempotent for the Asset, Schedule, and Due Cycle key.
- AI-service failure does not discard uploaded evidence or block manual finding entry.
- Report, quotation, order, commercial-policy and mission-plan revisions preserve prior versions and approval decisions.
- Policy publication is prospective, versioned and auditable. Confirmed order/maintenance records retain immutable snapshots of the policy values and terms accepted at confirmation; settlement must not read a newer live policy.
- Target mission plans are versioned and bound to the owning service order, Provider organization and permitted workforce; approved plan amendments preserve the previous plan and approval trail.
- Database and object-storage backups require a documented and tested restore procedure before production release.

#### 4.2.3 Performance

- Under the agreed project test load, 95 percent of standard JSON API requests complete within 2 seconds, excluding file-transfer time and third-party latency.
- List endpoints use server-side filtering, stable sorting, and bounded pagination.
- Evidence upload shows progress and can retry an interrupted transfer without creating a duplicate database record.
- Long-running AI processing is tracked independently from the original upload request so users can continue other work.

#### 4.2.4 Security, Privacy, Maintainability, and Compatibility

- All non-public endpoints require authentication and deny access unless role and resource-scope checks pass.
- Authorization enforces multi-tenant boundary checks: Client organizations cannot see other customers' assets or orders; independent Service Provider organizations cannot observe competitor quotations, margins, workforce records, or raw flight evidence.
- Separation of duties is enforced between `PLATFORM_ADMIN` (technical/security policy management) and `PLATFORM_OPERATOR` (business operations, provider vetting, commercial-policy publication and internal complaint handling). `PLATFORM_OPERATOR` is not a legal arbitrator or deposit custodian.
- Mission-plan, any waypoint-route data, drone/pilot and evidence reads/writes enforce Provider-organization, owning-order and assignment scope at the backend; waypoint records are optional, manual piloting under the accepted shot plan is supported, and public airspace lookup never substitutes for authority clearance.
- Commercial policy updates require an authorized Operator, schema validation, effective-time/version ordering and an audit event. No Provider-specific commission override is allowed; technical parameters belong to Platform Admin-controlled configuration.
- Passwords are hashed with the configured Spring Security password encoder and are never logged or returned.
- Browser refresh tokens use Secure, HttpOnly, SameSite=Strict cookies; browser access tokens remain in memory.
- Mobile tokens are returned only by the mobile authentication contract and are stored in secure platform storage.
- Passwords, raw tokens, credentials, private keys, protected evidence content, and unnecessary personal data are excluded from logs and JWT claims.
- Backend business capabilities remain separated by Spring Modulith boundaries, and schema changes use sequential forward Flyway migrations.
- Web and mobile clients consume the same versioned API while using the token-delivery profile appropriate to each client.
- Material security, commercial order, escrow transaction, and dispute events include event type, outcome, timestamp, and trace identifier without exposing secrets.
