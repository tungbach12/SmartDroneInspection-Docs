---
title: "Report 3 - Non-Functional Requirements"
document_type: report3-srs-section
weight: 45
source: "report3-software-requirement-specification.docx"
---

## 4. Non-Functional Requirements

### 4.1 External Interfaces

- **Web interface.** The service is available through a responsive web experience on current, commonly used desktop and mobile browsers. User-facing labels and guidance support English and Vietnamese.
- **Mobile interface.** The Customer role has a native mobile application on supported Android and iOS devices covering sign-in, registration, buildings, service requests with negotiation, inspection tracking, published reports, and notifications. Field capture and field-session recording are performed by Inspectors through the operations web portal, not the mobile application.
- **Detection service.** Building-defect detection is served by a self-hosted inference service. When that service cannot process an image, an OpenAI-compatible vision model is used as a fallback, and a user may opt out of the fallback for their own account.
- **Narrative drafting service.** An OpenAI-compatible language model drafts the report narrative once per draft from the confirmed inspection context. The service returns strict JSON and is instructed not to invent facts.
- **Payment and identity services.** PayOS VietQR and VNPay process service-payment settlement, and Google OAuth2 provides federated sign-in. Both payment gateways are configuration-gated and can be disabled; the application still starts and records payment through an authorised manual confirmation when they are off.
- **Ground-station integration.** An optional hub integration supplies read-only telemetry, flight traces, and mission video. A response from any external service does not replace the platform's own authorization or human review obligations.

### 4.2 Quality Attributes

#### 4.2.1 Usability

- **Understandable workflow.** Each inspection stage communicates its purpose, current status, responsible role, required next action, and any decision or evidence still needed.
- **Efficient field and office work.** Users can review assigned work, provide required evidence, and complete frequent verification and reporting tasks without unnecessary repetition. Any suggested or prepared content remains subject to user review before submission or approval.
- **Clear advisory labels.** Candidate findings and the report summary are visibly identified as advisory, and a manual finding is distinguishable from a model-detected one.
- **Bilingual support.** Users can work in English or Vietnamese. Generated reports follow the language selected for the engagement.

#### 4.2.2 Reliability

- **Service availability.** The service targets availability of at least `99.5%` during standard operating hours (`06:00–22:00 ICT`). This is an acceptance target, not a measured claim.
- **Recovery and backup.** Service records and documents are backed up daily. The recovery-time target is thirty minutes or less. This is an acceptance target, not evidence that recovery has been tested.
- **Degraded external services.** Unavailability of detection, narrative drafting, or a payment gateway must not cause the service to record an unconfirmed finding or an unconfirmed payment as confirmed. Detection may fall back to the secondary provider or to manual finding entry; narrative drafting may be skipped; payment may fall back to an authorised recorded confirmation.
- **Upload resilience.** A large video upload may be resumed after interruption without re-sending bytes already accepted, and a failed transcode retains its source for an explicit retry.
- **Financial and record integrity.** VND prices, applicable taxes, and platform fees are calculated and recorded consistently with their stated currency and agreed rules. Signed documents and published reports are protected from unauthorised alteration; changes to issued records are attributable and preserve prior versions.
- **Idempotency.** A retried event does not create a duplicate occurrence, evidence record, payment, or lifecycle notice.

#### 4.2.3 Performance

- **User response time.** Under normal operating conditions, at least 95% of standard user actions, searches, and paged list views complete within 2.0 seconds with 50 active users. This is a performance acceptance target, not a measured result.
- **Detection latency.** A single-image defect suggestion completes within 5.0 seconds under normal operating conditions for supported inputs. Report submission must not block on drafting; the narrative is advisory and may be retried.
- **Report compilation.** Compiling an inspection report must complete without reading video objects into memory, so report generation cost does not scale with the size of the stored evidence.
- **Media access.** Supported inspection video and images are reviewable without making the rest of the experience unusable during transfer, through range-based streaming and thumbnails.
- **Background processing.** Video transcoding runs in a bounded worker pool so that concurrent large uploads cannot starve interactive requests.

#### 4.2.4 Security and Data Protection

- **Organization and assignment privacy.** Users access only information permitted by their role, customer organization, partner relationship, and explicit work assignment. A direct link, a notice, or knowledge of a record identifier must not grant additional access.
- **Route-level denial.** A navigation section a role may not use has no route for that role, so the denial is enforced at the routing boundary as well as at the API and service layers.
- **Role permissions and independent decisions.** The service enforces the role responsibilities in this specification. A report author cannot review or publish their own report, and a permit submitter cannot verify their own permit.
- **Account and session protection.** Credentials and active access are protected against unauthorised use. Repeated failed sign-in attempts are restricted, refresh tokens rotate, and a security-sensitive account change ends affected sessions. Passwords are stored with a memory-hard hash and must satisfy the configured policy.
- **Media access control.** Stored evidence is served only through short-lived, evidence-scoped signed tickets. A ticket does not itself grant access to any other record.
- **Attributable activity history.** Important onboarding, commercial, assignment, inspection, publication, payment, and acceptance decisions are recorded with the responsible actor and time. Historical records are not silently rewritten.
- **Secret handling.** Credentials for gateways, storage, mail, and the language model are supplied as configuration and never committed to the repositories.

#### 4.2.5 Maintainability and Portability

- **Module boundaries.** The backend is organised into modules with enforced boundaries; a change that introduces a cross-module dependency outside the declared interface fails the build.
- **Schema discipline.** Database evolution is forward-only. The migration history is the consolidated `V1` baseline plus forward migrations `V2`, `V3`, `V4`, `V60`, `V61`, `V62`, `V63`, `V64`, and `V65`; a test asserts the exact applied set so an accidental renumbering fails.
- **Deployment portability.** The service runs from container images orchestrated by a compose stack, with the database, object storage, detection service, and application as separate services.
- **Bilingual content separation.** Display labels are separated from route identifiers and access rules, so copy changes and locale changes do not alter authorization.

**Summary of Quantified Non-Functional Requirements (`NFR-01` to `NFR-08`)**

The thresholds below are requirements and acceptance targets. They are not evidence that the current service meets them. Verification is recorded separately in Report 5.

| NFR ID | Category | Requirement Statement | Metric | Target Threshold | Verification Method |
| :---: | --- | --- | --- | --- | --- |
| `NFR-01` | Performance | Standard user actions, searches, and paged list views respond promptly under concurrent use. | 95th percentile response time and server error rate. | `p95 <= 2.0 s` and `0%` server errors under `50` concurrent users. | Concurrent user-journey and list-view assessment. |
| `NFR-02` | Performance | Supported image analysis remains within interactive response limits. | Processing time per supported image. | `<= 5.0 s` per request. | Timed assessment of supported workflows. |
| `NFR-03` | Security | Users are prevented from accessing records or actions outside their role, organization, partner relationship, or assignment. | Unauthorised and cross-scope access attempts blocked. | `100%` blocked; `0` unauthorised disclosures. | Role, organization, and assignment access assessment across all four portals. |
| `NFR-04` | Security | Sign-in resists repeated guessing and revoked access cannot continue to be used. | Failed-attempt lockout and sign-in request rate. | Restriction for `15 minutes` after `5` failures; more than `10` sign-in requests per minute per address blocked. | Sign-in and access-revocation assessment. |
| `NFR-05` | Reliability | Signed documents, building documents, and published reports remain intact; published records cannot be silently altered. | File integrity and prevention of in-place changes. | `100%` integrity for retained records; `100%` of unauthorised in-place changes prevented. | Retention, access, and version-history assessment. |
| `NFR-06` | Reliability | Large video evidence survives an interrupted upload and a failed transcode. | Resume success and retry availability. | `100%` of interrupted uploads resumable; `100%` of failed transcodes retained for retry. | Upload interruption and transcode-failure assessment. |
| `NFR-07` | Maintainability | Core business rules and all eight product features have repeatable verification, and module boundaries hold. | Business-rule and feature verification coverage; boundary violations. | All eight features have applicable verification cases; `0` module boundary violations. | Review of test evidence and architecture-boundary test. |
| `NFR-08` | Portability | The service can be rebuilt and started from its stated dependencies. | Clean-environment start and migration set. | Starts from the compose stack with the exact applied Flyway set `V1`, `V2`, `V3`, `V4`, `V60`, `V61`, `V62`, `V63`, `V64`, `V65` (`["1","2","3","4","60","61","62","63","64","65"]`); `FullDatabaseSchemaMigrationTest` and `RuntimePersistenceInventoryTest` assert this set and the 45 application tables / 44 JPA runtime entities. | Clean-environment deployment assessment and asserted migration/inventory tests. |
