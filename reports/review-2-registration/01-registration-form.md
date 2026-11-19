---
title: "CAPSTONE PROJECT REGISTER"
document_type: review2-registration
version: "2.0"
date: "2026-11-19"
project_code: "GFA26SE139"
group_name: "FA26SE112"
---

# CAPSTONE PROJECT REGISTER

- **Duration time:** from 09/2026 To 03/2027
- (*) **Profession:** Software Engineer | **Specialty:** SE
- (*) **Kinds of person make registers:** Lecturer / Students

---

## 1. Register information for supervisor (if have)

| No. | Full name | Phone | E-Mail | Title |
| :---: | --- | :---: | --- | :---: |
| 1 | Phạm Minh Trí | | `tripm14@fpt.edu.vn` | Giảng viên |
| 2 | Đặng Ngọc Minh Đức | | `ducdnm2@fpt.edu.vn` | Giảng viên |

---

## 2. Register information for students (if have)

| No. | Full name | Student code | Phone | E-mail | Role in Group |
| :---: | --- | :---: | --- | --- | :---: |
| 1 | Trần Hoàng Trung Hiếu | `SE184212` | `0963832382` | `hieuthtse184212@fpt.edu.vn` | Leader |
| 2 | Phùng Trung Quốc | `SE170027` | `0896986551` | `quocptse170027@fpt.edu.vn` | Member |
| 3 | Trương Thái Như | `SE180082` | `0328416716` | `nhuttse180082@fpt.edu.vn` | Member |
| 4 | Trần Tùng Bách | `SE180220` | `0378351050` | `bachttse180220@fpt.edu.vn` | Member |

---

## 3. Register content of Capstone Project

### (*) 3.1. Capstone Project name:

- **3.1.1. English:** SmartDroneInspection: AI-powered Infrastructure Inspection Management Platform
- **3.1.2. Vietnamese:** SmartDroneInspection: Nền tảng Quản lý Kiểm tra Hạ tầng bằng Drone tích hợp AI

---

### (*) 3.2. Main proposal content (including result and product)

#### a) Context:

Infrastructure assets such as buildings, bridges, roads, transmission towers, solar farms, industrial facilities, and telecommunication stations require regular inspections to ensure operational safety and lifecycle planning. Traditional inspection processes are often manual, labor-intensive, time-consuming, and potentially hazardous for inspectors.

The increasing adoption of drones enables organizations to capture high-quality aerial images and videos efficiently. However, many organizations still lack a centralized platform for managing inspection requests, schedules, reports, detected defects, and historical inspection records.

Furthermore, drone operation should be separated from business applications. Drone missions, telemetry, and flight operations should be managed by a common drone platform (SmartDroneHub), while inspection applications should focus on asset management and inspection workflows.

This project proposes SmartDroneInspection, an AI-powered Infrastructure Inspection Management Platform that manages the complete inspection lifecycle while integrating with SmartDroneHub through standardized APIs for drone mission execution.

*Note: All required hardware components (if any) will be supported and provided by AiTA Lab to facilitate development, testing, and demonstration of the system.*

#### b) Proposed Solutions:

SmartDroneInspection is designed as a business-oriented inspection management platform rather than a drone control system. The system manages infrastructure assets, inspection requests, inspection planning, reports, and defect tracking - while consuming drone operation services from SmartDroneHub through standardized APIs.

**Human Actors**

- **Administrator** - manages users, organizations, asset categories, and system configuration.
- **Manager** - creates inspection plans, approves requests, assigns inspectors, and reviews reports.
- **Inspector** - may apply to join the platform as a partner inspection-service provider and submit qualification information for review; after approval and assignment by the Inspection Manager, conducts inspections, records findings, uploads evidence, and generates reports.
- **Customer** - submits inspection requests, accepts quotations and reports, and makes payments.

**Five Core Subsystems**

1. **Asset Management**
   Manage infrastructure assets, categories, specifications, locations, technical documents, lifecycle status, and inspection history.
2. **Inspection Planning & Request Management**
   Support inspection scheduling, frequency configuration, priority assignment, inspector allocation, and digital request approval workflows.
3. **Drone Mission Integration**
   Integrate with SmartDroneHub via REST API to create inspection missions, retrieve telemetry, drone images, and flight logs. SmartDroneInspection acts as a consumer, not a drone controller.
4. **Inspection Report & Defect Management**
   Manage inspection reports, findings, evidence, defect classification, severity tracking, and inspection lifecycle.
5. **AI-assisted Services**
   Three focused AI features integrated within the 15-week project scope:
   - **Inspection Image Analysis** - detect potential defects from drone imagery using `DroneVisionAI`.
   - **Inspection Report Summarization** - generate concise summaries from inspection reports using an LLM.
   - **Historical Case Recommendation** - suggest similar past inspection cases and guidelines using `DroneKnowledgeAI`.

#### c) Functional Requirements:

**User Management**

- Authentication, authorization, role-based access control
- User profiles, audit logs

**Asset Management**

- Create/update assets, manage asset categories and documents
- Asset search, asset history, lifecycle tracking

**Inspection Planning**

- Create inspection plans, schedule inspections, assign inspectors
- Manage inspection calendars, inspection notifications

**Inspection Request Management**

- Create, approve, track, and cancel inspection requests
- Inspection request history

**Drone Mission Integration**

- Create inspection missions via SmartDroneHub Mission API
- Retrieve mission status, telemetry, inspection images, and flight reports

**Inspection Report Management**

- Create reports, upload evidence, record findings
- Approve and archive reports

**Defect Management**

- Record and classify defects, assign severity
- Track defect lifecycle, attach photo evidence

**AI Services Integration**

- Inspection image analysis (`DroneVisionAI`)
- Inspection report summarization
- Historical case recommendation (`DroneKnowledgeAI`)

**Dashboard & Analytics**

- Inspection statistics, defect analytics
- Asset utilization, inspection KPIs, operational reports

#### d) Non-Functional Requirements:

- Responsive Web Application
- Cross-platform Mobile Application (Flutter)
- RESTful API Architecture
- JWT Authentication
- Role-Based Access Control (RBAC)
- Integration with SmartDroneHub via standardized REST APIs
- PostgreSQL Database
- MinIO Object Storage for evidence and inspection images
- Docker Containerization, Cloud-ready Deployment
- Real-time mission status updates
- Audit Logging, Secure File Storage
- Scalable and High Availability Architecture

#### e) Theory & Practical:

**Applied Theory**

- Software Engineering: SDLC, Object-Oriented Analysis and Design, Software Architecture
- Business Process Modeling, Workflow Management, Database Design
- RESTful API Design, System Integration
- Mobile Computing, Real-time Communication
- AI Integration: Computer Vision, LLM-based summarization and recommendation
- Software Testing, Deployment

**Technologies**

- **Backend:** Java 21, Spring Boot, Spring Modulith, Spring Data JPA
- **Frontend:** React TS, Material UI
- **Mobile:** Flutter
- **Database:** PostgreSQL
- **Storage:** MinIO
- **AI:** `DroneVisionAI`, `DroneKnowledgeAI`, LLM-based summarization
- **Deployment:** Docker, Docker Compose, Cloud Deployment

#### f) Products (Expected Deliverables):

- SmartDroneInspection Web Portal (ReactJS + Material UI)
- Flutter Mobile Application (Customer)
- Asset Management Module
- Inspection Planning Module
- Inspection Request Module
- Drone Mission Integration Module (SmartDroneHub API)
- Inspection Report Module
- Defect Management Module
- AI Services: Image Analysis, Report Summarization, Case Recommendation
- Dashboard & Analytics
- RESTful APIs
- Docker Deployment Package
- Software Documentation

#### g) Proposed Tasks:

**Work Package 1 - Requirement Analysis & System Design**

- Requirement analysis, business workflow analysis
- Software architecture design, database design
- REST API specification, UI/UX design

**Work Package 2 - Asset & Inspection Planning**

- Asset management module
- Inspection planning, inspection request management
- Inspection scheduling, notification services

**Work Package 3 - Mission Integration & Report Management**

- SmartDroneHub Mission API integration
- Inspection report management, defect management
- Dashboard and analytical reporting

**Work Package 4 - Mobile Application & AI Integration**

- Flutter mobile application (Customer)
- Evidence management
- AI services: image analysis, report summarization, case recommendation

**Work Package 5 - Testing & Deployment**

- System integration testing, performance testing, security testing
- Docker deployment
- Software documentation, deployment guide

---

## 4. Other comments (propose all relative things if have):

............................................................................................................................................................
............................................................................................................................................................

---

| Supervisor (If have)<br>*(Sign and full name)* | HCM, date 19/08/2026<br>On behalf of Registers<br>*(Sign and full name)* |
| :---: | :---: |
| **Phạm Minh Trí & Đặng Ngọc Minh Đức** | **Trần Hoàng Trung Hiếu** |
