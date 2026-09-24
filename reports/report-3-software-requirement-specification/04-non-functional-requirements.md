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
- **YOLO service:** Eligible images may be sent for inference; responses contain the model version, predicted label, confidence, and bounding box.

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
- Report and order revisions preserve prior versions and approval decisions.
- Database and object-storage backups require a documented and tested restore procedure before production release.

#### 4.2.3 Performance

- Under the agreed project test load, 95 percent of standard JSON API requests complete within 2 seconds, excluding file-transfer time and third-party latency.
- List endpoints use server-side filtering, stable sorting, and bounded pagination.
- Evidence upload shows progress and can retry an interrupted transfer without creating a duplicate database record.
- Long-running AI processing is tracked independently from the original upload request so users can continue other work.

#### 4.2.4 Security, Privacy, Maintainability, and Compatibility

- All non-public endpoints require authentication and deny access unless role and resource-scope checks pass.
- Authorization enforces organization, ownership, assignment, release authority, and separation of duties as applicable.
- Passwords are hashed with the configured Spring Security password encoder and are never logged or returned.
- Browser refresh tokens use Secure, HttpOnly, SameSite=Strict cookies; browser access tokens remain in memory.
- Mobile tokens are returned only by the mobile authentication contract and are stored in secure platform storage.
- Passwords, raw tokens, credentials, private keys, protected evidence content, and unnecessary personal data are excluded from logs and JWT claims.
- Backend business capabilities remain separated by Spring Modulith boundaries, and schema changes use sequential forward Flyway migrations.
- Web and mobile clients consume the same versioned API while using the token-delivery profile appropriate to each client.
- Material security and workflow events include event type, outcome, timestamp, and trace identifier without exposing secrets.
