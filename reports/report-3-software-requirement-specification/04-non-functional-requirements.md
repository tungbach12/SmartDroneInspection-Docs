---
title: "Report 3 - Non-Functional Requirements"
document_type: report3-srs-section
weight: 45
source: "report3-software-requirement-specification.docx"
---

## 4. Non-Functional Requirements

### 4.1 External Interfaces

This section defines the external boundary interfaces through which human actors, drone telemetry sources, and third-party services interact with SmartDroneInspection. External responses inform platform workflows but never bypass internal authorization, validation, or human confirmation rules.

#### 4.1.1 User Interfaces

- **Responsive Web Portals (`ADMIN`, `MANAGER`, `CUSTOMER`, `INSPECTOR`).** The service operates through four role-dedicated web portals supporting desktop (`1600×1000` reference layout) and mobile browser viewports across current Chromium, Firefox, Safari, and Edge releases.
- **Role-Isolated Navigation & Bilingual Presentation.** Navigation routes are filtered strictly by the authenticated user's single role; unauthorized routes are absent rather than merely visually hidden. All user-facing labels, validation hints, toast messages (`MSG01`–`MSG50`), and notifications support English (`en`) and Vietnamese (`vi`) without altering authorization or route identifiers.
- **Customer Native Mobile Interface (`CUSTOMER` only).** A native Android and iOS application provides Customer self-registration, sign-in/OTP/Google OAuth2, building registration with airspace screening, service request creation and quotation acceptance, Order/Inspection chat, inspection tracking, published report viewing, Inspector rating, VietQR/VNPay settlement, downloadable payment-notice/receipt PDFs, and collapsible `DroneKnowledgeAI` references. Field-session control, evidence upload, and staff workflows remain exclusively on Web portals.
- **Advisory vs. Official Visual Separation.** AI-generated defect bounding boxes, drafted finding notes, report executive summaries, and airspace screening banners are visually badged as advisory, distinguishing them from human-confirmed findings, published reports, and statutory aviation permits.

#### 4.1.2 Hardware and Telemetry Interfaces

- **Aircraft Photographic & Video Sensors (Indirect File Intake).** The service imposes no proprietary drone hardware lock-in and accepts standard JPEG/PNG/WEBP building photographs (`<= 10 MB`) and MP4 mission video (`<= 2 GiB`). Available EXIF capture timestamps, camera orientation, and GPS coordinates are preserved when present and disclosed as unavailable when absent (`BR-31`, `BR-33`).
- **Offline Flight Log Formats.** Where live telemetry is unavailable, the platform ingests exported `SRT`, `CSV`, `KML`, and `GPX` flight logs (`<= 15 MB`), normalizing available latitude, longitude, altitude, speed, heading, battery, and timestamp series while preserving absent sensor fields without fabrication (`BR-28`).
- **SmartDroneHub Ground-Station Integration.** During an active field session, an optional ground-station hub supplies read-only flight status, flight mode, GPS coordinates, altitude, speed, heading, battery level, waypoint progress, gimbal state, and mission MP4 video. The interface is strictly unidirectional: SmartDroneInspection never transmits flight actuation, takeoff, landing, or waypoint commands to aircraft (`BR-30`).

#### 4.1.3 Software and External Service Interfaces

| External Interface | Role in Lifecycle | Contract & Degraded-Mode Behaviour |
| --- | --- | --- |
| **Primary AI Defect Detection Service** | Candidate defect inference (`FE-16`) | Accepts inspection imagery and returns bounding boxes, labels across the five building defect classes (`crack`, `leakage`, `abscission`, `corrosion`, `bulge`), and confidence scores. Failures degrade gracefully to secondary fallback or manual finding entry (`BR-36`). |
| **OpenAI-Compatible Vision & Narrative LLM** | Secondary detection fallback (`FE-16`) & advisory drafting (`FE-17`, `FE-18`) | Invoked for secondary detection only when the primary detector returns empty/unavailable and the acting user has not opted out in Account Settings; drafts bilingual finding notes and single-shot report summaries strictly marked advisory (`BR-43`). |
| **Semantic Vector Retrieval (`DroneKnowledgeAI`)** | Historical case & engineering standard retrieval (`FE-17`) | Indexes confirmed findings at report publication and performs customer-isolated similarity lookup over prior cases and seeded standards; automatically falls back to keyword matching when vector search is unavailable (`BR-55`). |
| **Sepay VietQR & VNPay Gateways** | Online Customer settlement (`FE-20`) & Inspector VietQR payout (`FE-22`) | Configuration-gated online gateways. Generates VietQR / hosted checkout payloads, verifies cryptographic signatures or authenticated transfer notifications before marking `PAID`, records superseded/late callbacks idempotently, and supports authorized manual settlement when disabled (`BR-45`, `BR-47`). |
| **Google OAuth2 Identity Service** | Federated sign-in (`FE-01`) | Authenticates verified active accounts for Web and Customer Mobile without bypassing platform role assignment, account status checks, or session-rotation controls. |
| **Private Object Storage & SMTP Mail** | Document/media persistence & email notices (`FE-02`–`FE-21`) | Private bucket storage isolates permits, contracts, evidence, and PDFs behind server authorization and signed media tickets; SMTP email alerts run best-effort asynchronously so mail outages never roll back business transactions (`FE-12`). |

#### 4.1.4 Communications and Data Exchange Interfaces

- **Transport & API Boundary.** Client-to-server traffic runs over HTTPS/TLS using typed JSON request/response payloads and standardized problem-detail error responses with localized user messages.
- **Webhook & Callback Integrity.** Payment gateway notifications (`Sepay` and `VNPay`) are accepted only after cryptographic signature or credential verification, receiving-account validation, exact whole-VND amount verification, and idempotent order-reference matching (`BR-45`, `BR-47`).
- **Large-Media Transfer & Streaming.** Video uploads up to `2 GiB` use resumable `10 MiB` chunked transfers that resume from confirmed offsets after network interruption; playback uses HTTP byte-range streaming authorized by `5-minute` evidence-scoped signed tickets (`NFR-06`).
- **Asynchronous Processing Decoupling.** Video transcoding, semantic knowledge indexing, scheduled expiry/timeout sweeps, and transactional notification fan-out execute asynchronously outside interactive request threads so heavy background jobs do not block user portals.

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

- **Ownership and assignment privacy.** Users access only information permitted by their role, Customer ownership, partner relationship, and explicit work assignment. A direct link, a notice, or knowledge of a record identifier must not grant additional access.
- **Route-level denial.** A navigation section a role may not use has no route for that role, so the denial is enforced at the routing boundary as well as at the service layer.
- **Role permissions and independent decisions.** The service enforces the role responsibilities in this specification. A report author cannot review or publish their own report, and mission flight permits follow assigned-Inspector self-attestation with read-only audit visibility for Managers and Administrators.
- **Account and session protection.** Credentials and active access are protected against unauthorised use. Repeated failed sign-in attempts are restricted, refresh tokens rotate, and a security-sensitive account change ends affected sessions. Passwords are stored with a memory-hard hash and must satisfy the configured policy.
- **Media access control.** Stored evidence is served only through short-lived, evidence-scoped signed tickets. A ticket does not itself grant access to any other record.
- **Attributable activity history.** Important onboarding, commercial, assignment, inspection, publication, payment, and acceptance decisions are recorded with the responsible actor and time. Historical records are not silently rewritten.
- **Secret handling.** Credentials for gateways, storage, mail, and the language model are supplied as configuration and never committed to the repositories.

#### 4.2.5 Maintainability and Portability

- **Module boundaries.** The application service is organised into modules with enforced boundaries; a change that introduces a cross-module dependency outside the declared interface fails verification.
- **Schema discipline.** Database evolution is forward-only, and automated migration checks verify the applied schema sequence so accidental changes fail before release.
- **Deployment portability.** The service runs from container images orchestrated by a compose stack, with the database, object storage, detection service, and application as separate services.
- **Bilingual content separation.** Display labels are separated from route identifiers and access rules, so copy changes and locale changes do not alter authorization.

**Summary of Quantified Non-Functional Requirements (`NFR-01` to `NFR-08`)**

The thresholds below are requirements and acceptance targets. They are not evidence that the current service meets them. Verification is recorded separately in Report 5.

| NFR ID | Category | Requirement Statement | Metric | Target Threshold | Verification Method |
| :---: | --- | --- | --- | --- | --- |
| `NFR-01` | Performance | Standard user actions, searches, and paged list views respond promptly under concurrent use. | 95th percentile response time and server error rate. | `p95 <= 2.0 s` and `0%` server errors under `50` concurrent users. | Concurrent user-journey and list-view assessment. |
| `NFR-02` | Performance | Supported image analysis remains within interactive response limits. | Processing time per supported image. | `<= 5.0 s` per request. | Timed assessment of supported workflows. |
| `NFR-03` | Security | Users are prevented from accessing records or actions outside their role, Customer ownership, partner relationship, or assignment. | Unauthorised and cross-scope access attempts blocked. | `100%` blocked; `0` unauthorised disclosures. | Role, ownership, and assignment access assessment across all four portals. |
| `NFR-04` | Security | Sign-in resists repeated guessing and revoked access cannot continue to be used. | Failed-attempt lockout and sign-in request rate. | Restriction for `15 minutes` after `5` failures; more than `10` sign-in requests per minute per address blocked. | Sign-in and access-revocation assessment. |
| `NFR-05` | Reliability | Signed documents, building documents, and published reports remain intact; published records cannot be silently altered. | File integrity and prevention of in-place changes. | `100%` integrity for retained records; `100%` of unauthorised in-place changes prevented. | Retention, access, and version-history assessment. |
| `NFR-06` | Reliability | Large video evidence survives an interrupted upload and a failed transcode. | Resume success and retry availability. | `100%` of interrupted uploads resumable; `100%` of failed transcodes retained for retry. | Upload interruption and transcode-failure assessment. |
| `NFR-07` | Maintainability | Core business rules and all twenty-four atomic product features (`FE-01`–`FE-24`) have repeatable verification, and module boundaries hold. | Business-rule and feature verification coverage; boundary violations. | All twenty-four features have applicable verification cases; `0` module boundary violations. | Review of test evidence and architecture-boundary test. |
| `NFR-08` | Portability | The service can be rebuilt and started reliably from its stated container dependencies. | Clean-environment startup and schema readiness. | Starts cleanly from the container stack with all required application database migrations applied automatically and verified against the release schema baseline. | Clean-environment deployment assessment and schema verification tests. |

### 4.3 Design and Operational Constraints

The following operational constraints and system-level assumptions govern how requirements in §3 and §4 are delivered and verified:

- **Single Canonical Role & Direct Customer Ownership.** Every human account holds exactly one of the four login roles (`ADMIN`, `MANAGER`, `CUSTOMER`, `INSPECTOR`), and building ownership attaches directly to a `CUSTOMER` account without intermediate organizational hierarchies.
- **Single-Currency VND Accounting.** All commercial quotations, invoices, VAT, personal income tax (TNCN) withholdings, platform commissions, payouts, refunds, and receivable recoveries are denominated and rounded in Vietnamese Dong (`VND`).
- **Vietnam Time-Zone Business Anchoring.** Commercial lead times (`ADMIN`-configurable `0–365` calendar days, default `20`), recurring month-end clamping, permit validity windows, and daily expiry/overdue scans evaluate business dates in `Asia/Ho_Chi_Minh` (`UTC+07:00`).
- **Client Token Storage Boundaries.** Web clients keep short-lived access tokens strictly in memory and rely on HTTP-only cookies for refresh rotation; the Customer Mobile client stores session credentials exclusively in platform-encrypted secure storage (`NFR-04`).
- **Regulatory & Professional Non-Substitution.** Platform onboarding approvals, airspace classifications, self-attested permit records, AI defect suggestions, and published inspection reports constitute internal operational records only and never substitute for statutory civil-aviation permits or licensed structural-engineering certification (`BR-26`, `BR-40`).
