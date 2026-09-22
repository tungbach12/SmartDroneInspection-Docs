---
title: "Report 3 - Overall Description"
document_type: report3-srs-section
weight: 15
source: "report3-software-requirement-specification.docx"
---

# II. Software Requirement Specification

## 1. Overall Description

### 1.1 Product Overview

SmartDroneInspection is an infrastructure inspection management platform. It coordinates the business lifecycle from customer assets and recurring inspection schedules to inspection requests, service orders, field evidence, verified findings, reports, maintenance tickets, and final resolution. The solution includes a web application for administration, customer operations, and service coordination; a mobile application for assigned field work; and a backend that owns business rules, authorization, transactional data, file access, and integration contracts.

The platform supports five actors: Admin, Service Manager, Inspector, Maintenance Engineer, and Client. A Client acts only within one customer organization. Inspectors and Maintenance Engineers work only on assigned resources. Service Managers coordinate service delivery across customer organizations. Admin manages platform configuration and identities but does not automatically receive permission to perform customer or service workflow actions.

A Client representative may self-register a new organization and the first Client account. The organization and account become active immediately after successful registration. Registration can create only the Client role; platform and service-workforce roles remain controlled by Admin. The Client signs in through the normal authentication flow after registration.

The product does not pilot drones, control flights, own drone telemetry, or replace site safety procedures. Inspection images may be transferred from a drone SD card, computer, web browser, or mobile device. MinIO stores authorized evidence objects. The configured YOLO service may propose defect candidates, but those candidates do not become official findings until an Inspector confirms or corrects them.

The main business flow is:

- WF1: the Client registers an asset and configures periodic inspection scheduling.
- WF2: the Client submits or completes an inspection request; the Service Manager reviews it, prepares a quotation and service order, and assigns an Inspector.
- WF3: the Inspector performs the inspection, uploads evidence, verifies AI candidates, prepares the report, and completes peer review before the Service Manager releases the report to the Client.
- WF4: the Client creates a maintenance ticket from verified findings; the Maintenance Engineer assesses and performs approved work; the Service Manager releases the result; and the Client accepts, requests rework, or requests re-inspection.

![SmartDroneInspection system context](assets/context.png)

### 1.2 Business Rules

| ID | Rule Definition |
| --- | --- |
| BR-01 | Admin, Client, and service-workforce identities use distinct actor zones; Admin and Client roles are exclusive. |
| BR-02 | A Client can access only data owned by the Client's organization. |
| BR-03 | An Inspector or Maintenance Engineer can access only work assigned to that user unless another explicit service role grants separate scope. |
| BR-04 | An asset code is unique within its organization. |
| BR-05 | An active recurring schedule requires an active asset and an available checklist template. |
| BR-06 | Only one periodic request may be generated for the same Asset, Schedule, and Due Cycle. |
| BR-07 | An ad hoc request must reference an asset owned by the Client's organization. |
| BR-08 | A quotation or order revision creates a new version and preserves earlier versions. |
| BR-09 | No upfront payment is required for inspection or maintenance work. |
| BR-10 | An unconfirmed inspection service order cannot proceed to Inspector assignment. |
| BR-11 | An Inspector assignment must be accepted before inspection status becomes `READY_FOR_INSPECTION`. |
| BR-12 | Assignment rejection requires a reason and returns the work to the Service Manager. |
| BR-13 | Manual drone piloting, flight control, and operational flight safety remain outside SmartDroneInspection. |
| BR-14 | Each evidence object has a checksum; duplicate content cannot create duplicate evidence in the same work context. |
| BR-15 | Missing GPS is recorded but does not automatically invalidate otherwise acceptable evidence. |
| BR-16 | AI candidates remain non-official until an Inspector confirms or modifies them. |
| BR-17 | Rejected or unverified AI candidates do not enter official defect statistics or reports. |
| BR-18 | An Inspector may manually add a defect that the AI service did not detect. |
| BR-19 | A report author cannot peer-review or technically approve the same report. |
| BR-20 | A report cannot be released before technical approval and deliverable-completeness review. |
| BR-21 | Internal drafts and peer-review comments are not visible to the Client. |
| BR-22 | An accepted report version is immutable; corrections require a new linked version. |
| BR-23 | A maintenance ticket must reference at least one verified finding in an accepted report. |
| BR-24 | A qualified Maintenance Engineer provides the technical maintenance assessment. |
| BR-25 | An assessment assignment does not authorize maintenance execution. |
| BR-26 | An approved maintenance order is required before execution assignment. |
| BR-27 | Material scope or cost growth requires an approved change-order version before additional work. |
| BR-28 | Before and after evidence is required before a maintenance ticket can be closed. |
| BR-29 | Only the Service Manager releases inspection and maintenance results to the Client. |
| BR-30 | The Client may accept a maintenance result, request rework, or request a linked re-inspection. |
| BR-31 | Rework preserves the existing ticket and creates a new execution cycle. |
| BR-32 | Re-inspection creates a linked ad hoc inspection request and returns it to WF2. |
| BR-33 | Status transitions that affect assignment, approval, release, acceptance, or closure are audited. |
| BR-34 | File possession or an object-storage path alone does not grant access to evidence. |
| BR-35 | Password, role, status, and session-revocation changes invalidate affected active sessions. |
