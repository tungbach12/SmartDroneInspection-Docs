#!/usr/bin/env python3
"""Export the official Capstone Project Registration Form Word document using the official FPT University template."""
import sys
from pathlib import Path
import docx
from docx.shared import Pt, Inches

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parent))

from export_common import OFFICIAL, REPORTS

TEMPLATE_NAME = "Bản sao của FA26SE112_SMARTDRONEINSPECTION_AI_POWERED_INFRASTR_tripm14.docx"


def export_registration_doc(output_path: Path):
    template_path = Path(OFFICIAL) / TEMPLATE_NAME
    if not template_path.exists():
        raise FileNotFoundError(f"Official template not found at: {template_path}")

    doc = docx.Document(template_path)

    # 1. Keep Student Table (Table 1) exactly aligned with original registration
    student_table = doc.tables[1]
    students_data = [
        ("1", "Trần Hoàng Trung Hiếu", "SE184212", "0963832382", "hieuthtse184212@fpt.edu.vn", "Leader"),
        ("2", "Phùng Trung Quốc", "SE170027", "0896986551", "quocptse170027@fpt.edu.vn", "Member"),
        ("3", "Trương Thái Như", "SE180082", "0328416716", "nhuttse180082@fpt.edu.vn", "Member"),
        ("4", "Trần Tùng Bách", "SE180220", "0378351050", "bachttse180220@fpt.edu.vn", "Member"),
    ]
    for i, s_data in enumerate(students_data, start=1):
        if i < len(student_table.rows):
            row = student_table.rows[i]
            for col_idx, text_val in enumerate(s_data):
                row.cells[col_idx].text = text_val
                for p in row.cells[col_idx].paragraphs:
                    p.paragraph_format.line_spacing = 1.15
                    for run in p.runs:
                        run.font.name = "Times New Roman"
                        run.font.size = Pt(11)

    # 2. Keep original English & Vietnamese project names in 3.1
    for p in doc.paragraphs:
        if "3.1.1. English:" in p.text:
            p.text = "3.1.1. English: SmartDroneInspection: AI-powered Infrastructure Inspection Management Platform"
            p.runs[0].font.name = "Times New Roman"
            p.runs[0].font.size = Pt(12)
        elif "3.1.2. Vietnamese:" in p.text:
            p.text = "3.1.2. Vietnamese: SmartDroneInspection: Nền tảng Quản lý Kiểm tra Hạ tầng bằng Drone tích hợp AI"
            p.runs[0].font.name = "Times New Roman"
            p.runs[0].font.size = Pt(12)

    # 3. Locate the index of paragraph ("a) Context:") and ("4. Other comments")
    idx_context = -1
    idx_other = -1
    for i, p in enumerate(doc.paragraphs):
        t = p.text.strip()
        if t.startswith("a) Context:"):
            idx_context = i
        elif t.startswith("4. Other comments"):
            idx_other = i

    if idx_context == -1 or idx_other == -1:
        raise ValueError(f"Could not locate context ({idx_context}) or other comments ({idx_other}) in doc")

    for i in range(idx_context, idx_other):
        doc.paragraphs[i].text = ""

    content_sections = [
        ("heading", "a) Context:"),
        ("body", "Infrastructure assets such as buildings, bridges, roads, transmission towers, solar farms, industrial facilities, and telecommunication stations require regular inspections to ensure operational safety and lifecycle planning. Traditional inspection processes are often manual, labor-intensive, time-consuming, and potentially hazardous for inspectors."),
        ("body", "The increasing adoption of drones enables organizations to capture high-quality aerial images and videos efficiently. However, many organizations still lack a centralized platform for managing inspection requests, schedules, reports, detected defects, and historical inspection records."),
        ("body", "Furthermore, drone operation should be separated from business applications. Drone missions, telemetry, and flight operations should be managed by a common drone platform (SmartDroneHub), while inspection applications should focus on asset management and inspection workflows."),
        ("body", "This project proposes SmartDroneInspection, an AI-powered Infrastructure Inspection Management Platform that manages the complete inspection lifecycle while integrating with SmartDroneHub through standardized APIs for drone mission execution."),
        ("body", "Note: All required hardware components (if any) will be supported and provided by AiTA Lab to facilitate development, testing, and demonstration of the system."),

        ("heading", "b) Proposed Solutions:"),
        ("body", "SmartDroneInspection is designed as a business-oriented inspection management platform rather than a drone control system. The system manages infrastructure assets, inspection requests, inspection planning, reports, and defect tracking - while consuming drone operation services from SmartDroneHub through standardized APIs."),
        ("subheading", "Human Actors"),
        ("bullet", "Administrator - manages users, organizations, asset categories, and system configuration."),
        ("bullet", "Manager - creates inspection plans, approves requests, assigns inspectors, and reviews reports."),
        ("bullet", "Inspector - may apply to join the platform as a partner inspection-service provider and submit qualification information for review; after approval and assignment by the Inspection Manager, conducts inspections, records findings, uploads evidence, and generates reports."),
        ("bullet", "Customer - submits inspection requests, accepts quotations and reports, and makes payments."),

        ("subheading", "Five Core Subsystems"),
        ("numbered", "1. Asset Management\n"
                     "Manage infrastructure assets, categories, specifications, locations, technical documents, lifecycle status, and inspection history."),
        ("numbered", "2. Inspection Planning & Request Management\n"
                     "Support inspection scheduling, frequency configuration, priority assignment, inspector allocation, and digital request approval workflows."),
        ("numbered", "3. Drone Mission Integration\n"
                     "Integrate with SmartDroneHub via REST API to create inspection missions, retrieve telemetry, drone images, and flight logs. SmartDroneInspection acts as a consumer, not a drone controller."),
        ("numbered", "4. Inspection Report & Defect Management\n"
                     "Manage inspection reports, findings, evidence, defect classification, severity tracking, and inspection lifecycle."),
        ("numbered", "5. AI-assisted Services\n"
                     "Three focused AI features integrated within the 15-week project scope:"),
        ("bullet", "Inspection Image Analysis - detect potential defects from drone imagery using DroneVisionAI."),
        ("bullet", "Inspection Report Summarization - generate concise summaries from inspection reports using an LLM."),
        ("bullet", "Historical Case Recommendation - suggest similar past inspection cases and guidelines using DroneKnowledgeAI."),

        ("heading", "c) Functional Requirements:"),
        ("subheading", "User Management"),
        ("bullet", "Authentication, authorization, role-based access control"),
        ("bullet", "User profiles, audit logs"),

        ("subheading", "Asset Management"),
        ("bullet", "Create/update assets, manage asset categories and documents"),
        ("bullet", "Asset search, asset history, lifecycle tracking"),

        ("subheading", "Inspection Planning"),
        ("bullet", "Create inspection plans, schedule inspections, assign inspectors"),
        ("bullet", "Manage inspection calendars, inspection notifications"),

        ("subheading", "Inspection Request Management"),
        ("bullet", "Create, approve, track, and cancel inspection requests"),
        ("bullet", "Inspection request history"),

        ("subheading", "Drone Mission Integration"),
        ("bullet", "Create inspection missions via SmartDroneHub Mission API"),
        ("bullet", "Retrieve mission status, telemetry, inspection images, and flight reports"),

        ("subheading", "Inspection Report Management"),
        ("bullet", "Create reports, upload evidence, record findings"),
        ("bullet", "Approve and archive reports"),

        ("subheading", "Defect Management"),
        ("bullet", "Record and classify defects, assign severity"),
        ("bullet", "Track defect lifecycle, attach photo evidence"),

        ("subheading", "AI Services Integration"),
        ("bullet", "Inspection image analysis (DroneVisionAI)"),
        ("bullet", "Inspection report summarization"),
        ("bullet", "Historical case recommendation (DroneKnowledgeAI)"),

        ("subheading", "Dashboard & Analytics"),
        ("bullet", "Inspection statistics, defect analytics"),
        ("bullet", "Asset utilization, inspection KPIs, operational reports"),

        ("heading", "d) Non-Functional Requirements:"),
        ("bullet", "Responsive Web Application"),
        ("bullet", "Cross-platform Mobile Application (Flutter)"),
        ("bullet", "RESTful API Architecture"),
        ("bullet", "JWT Authentication"),
        ("bullet", "Role-Based Access Control (RBAC)"),
        ("bullet", "Integration with SmartDroneHub via standardized REST APIs"),
        ("bullet", "PostgreSQL Database"),
        ("bullet", "MinIO Object Storage for evidence and inspection images"),
        ("bullet", "Docker Containerization, Cloud-ready Deployment"),
        ("bullet", "Real-time mission status updates"),
        ("bullet", "Audit Logging, Secure File Storage"),
        ("bullet", "Scalable and High Availability Architecture"),

        ("heading", "e) Theory & Practical:"),
        ("subheading", "Applied Theory"),
        ("bullet", "Software Engineering: SDLC, Object-Oriented Analysis and Design, Software Architecture"),
        ("bullet", "Business Process Modeling, Workflow Management, Database Design"),
        ("bullet", "RESTful API Design, System Integration"),
        ("bullet", "Mobile Computing, Real-time Communication"),
        ("bullet", "AI Integration: Computer Vision, LLM-based summarization and recommendation"),
        ("bullet", "Software Testing, Deployment"),

        ("subheading", "Technologies"),
        ("bullet", "Backend: Java 21, Spring Boot, Spring Modulith, Spring Data JPA"),
        ("bullet", "Frontend: React TS, Material UI"),
        ("bullet", "Mobile: Flutter"),
        ("bullet", "Database: PostgreSQL"),
        ("bullet", "Storage: MinIO"),
        ("bullet", "AI: DroneVisionAI, DroneKnowledgeAI, LLM-based summarization"),
        ("bullet", "Deployment: Docker, Docker Compose, Cloud Deployment"),

        ("heading", "f) Products (Expected Deliverables):"),
        ("bullet", "SmartDroneInspection Web Portal (ReactJS + Material UI)"),
        ("bullet", "Flutter Mobile Application (Customer)"),
        ("bullet", "Asset Management Module"),
        ("bullet", "Inspection Planning Module"),
        ("bullet", "Inspection Request Module"),
        ("bullet", "Drone Mission Integration Module (SmartDroneHub API)"),
        ("bullet", "Inspection Report Module"),
        ("bullet", "Defect Management Module"),
        ("bullet", "AI Services: Image Analysis, Report Summarization, Case Recommendation"),
        ("bullet", "Dashboard & Analytics"),
        ("bullet", "RESTful APIs"),
        ("bullet", "Docker Deployment Package"),
        ("bullet", "Software Documentation"),

        ("heading", "g) Proposed Tasks:"),
        ("subheading", "Work Package 1 - Requirement Analysis & System Design"),
        ("bullet", "Requirement analysis, business workflow analysis"),
        ("bullet", "Software architecture design, database design"),
        ("bullet", "REST API specification, UI/UX design"),

        ("subheading", "Work Package 2 - Asset & Inspection Planning"),
        ("bullet", "Asset management module"),
        ("bullet", "Inspection planning, inspection request management"),
        ("bullet", "Inspection scheduling, notification services"),

        ("subheading", "Work Package 3 - Mission Integration & Report Management"),
        ("bullet", "SmartDroneHub Mission API integration"),
        ("bullet", "Inspection report management, defect management"),
        ("bullet", "Dashboard and analytical reporting"),

        ("subheading", "Work Package 4 - Mobile Application & AI Integration"),
        ("bullet", "Flutter mobile application (Customer)"),
        ("bullet", "Evidence management"),
        ("bullet", "AI services: image analysis, report summarization, case recommendation"),

        ("subheading", "Work Package 5 - Testing & Deployment"),
        ("bullet", "System integration testing, performance testing, security testing"),
        ("bullet", "Docker deployment"),
        ("bullet", "Software documentation, deployment guide"),
    ]

    ref_p = doc.paragraphs[idx_other]

    for kind, text in content_sections:
        new_p = ref_p.insert_paragraph_before()
        new_p.paragraph_format.line_spacing = 1.15
        new_p.paragraph_format.space_after = Pt(4)

        if kind == "heading":
            new_p.paragraph_format.space_before = Pt(8)
            new_p.paragraph_format.space_after = Pt(4)
            run = new_p.add_run(text)
            run.bold = True
            run.font.name = "Times New Roman"
            run.font.size = Pt(12)
        elif kind == "subheading":
            new_p.paragraph_format.space_before = Pt(4)
            new_p.paragraph_format.space_after = Pt(2)
            run = new_p.add_run(text)
            run.bold = True
            run.font.name = "Times New Roman"
            run.font.size = Pt(11)
        elif kind == "bullet":
            new_p.paragraph_format.left_indent = Inches(0.25)
            run = new_p.add_run("● " + text)
            run.font.name = "Times New Roman"
            run.font.size = Pt(11)
        elif kind == "numbered":
            new_p.paragraph_format.left_indent = Inches(0.2)
            run = new_p.add_run(text)
            run.font.name = "Times New Roman"
            run.font.size = Pt(11)
        else:
            run = new_p.add_run(text)
            run.font.name = "Times New Roman"
            run.font.size = Pt(11)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    doc.save(output_path)
    print(f"Successfully exported registration document to: {output_path}")


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    out_dir = REPORTS / "generated" / "registration"
    out_file = out_dir / "FA26SE112_SMARTDRONEINSPECTION_AI_POWERED_INFRASTR_tripm14.docx"
    export_registration_doc(out_file)

    pack_dir = REPORTS / "generated" / "review-2-pack"
    pack_file = pack_dir / "FA26SE112_Registration_Form.docx"
    export_registration_doc(pack_file)


if __name__ == "__main__":
    main()
