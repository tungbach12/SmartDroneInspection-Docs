#!/usr/bin/env python3
"""
Populate the 4 official SWP490 Review 2 Word templates (BM01, BM02, BM03, BM04)
in-place at the XML level with concise, scannable content while keeping 100% of
fonts (Calibri), styles, colors (#14233A, #C9652A), borders (#D9D4CA), and margins.

Scope: 4 Inspection Workflows (WF-01 to WF-04) without Maintenance.
"""
from __future__ import annotations

import copy
import sys
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
XML_NS = "http://www.w3.org/XML/1998/namespace"
NS = {"w": W_NS}
ET.register_namespace("w", W_NS)


def w_tag(local: str) -> str:
    return f"{{{W_NS}}}{local}"


def set_cell_text(tc: ET.Element, text: str, bold: bool | None = None) -> None:
    """Sets text inside a table cell while preserving its original w:tcPr, w:pPr, and w:rPr."""
    paragraphs = tc.findall("w:p", NS)
    p = paragraphs[0] if paragraphs else ET.SubElement(tc, w_tag("p"))
    for extra_p in paragraphs[1:]:
        tc.remove(extra_p)

    runs = p.findall("w:r", NS)
    if runs:
        r0 = runs[0]
        rPr = r0.find("w:rPr", NS)
        rPr_clone = copy.deepcopy(rPr) if rPr is not None else None
        for r in runs:
            p.remove(r)
    else:
        rPr_clone = ET.Element(w_tag("rPr"))
        rf = ET.SubElement(rPr_clone, w_tag("rFonts"))
        for attr in ("ascii", "cs", "eastAsia", "hAnsi"):
            rf.set(w_tag(attr), "Calibri")
        sz = ET.SubElement(rPr_clone, w_tag("sz"))
        sz.set(w_tag("val"), "19")
        szCs = ET.SubElement(rPr_clone, w_tag("szCs"))
        szCs.set(w_tag("val"), "19")

    if rPr_clone is not None:
        # Clear placeholder italic and grey (#666666) styling from template example cells
        for i_tag in ("i", "iCs"):
            existing_i = rPr_clone.find(f"w:{i_tag}", NS)
            if existing_i is not None:
                rPr_clone.remove(existing_i)
            i_el = ET.SubElement(rPr_clone, w_tag(i_tag))
            i_el.set(w_tag("val"), "false")

        col_el = rPr_clone.find("w:color", NS)
        if col_el is not None and col_el.attrib.get(w_tag("val")) == "666666":
            rPr_clone.remove(col_el)

        if bold is not None:
            for b_tag in ("b", "bCs"):
                existing = rPr_clone.find(f"w:{b_tag}", NS)
                if existing is not None:
                    rPr_clone.remove(existing)
                b_el = ET.SubElement(rPr_clone, w_tag(b_tag))
                if not bold:
                    b_el.set(w_tag("val"), "false")

    lines = str(text).split("\n")
    for idx, line in enumerate(lines):
        r_new = ET.SubElement(p, w_tag("r"))
        if rPr_clone is not None:
            r_new.append(copy.deepcopy(rPr_clone))
        if idx > 0:
            ET.SubElement(r_new, w_tag("br"))
        t_el = ET.SubElement(r_new, w_tag("t"))
        t_el.set(f"{{{XML_NS}}}space", "preserve")
        t_el.text = line


def populate_kv_table(tbl: ET.Element, values: list[str], header_col1: str | None = None) -> None:
    """Populates a 2-column vertical key-value table where col 0 is the label and col 1 is the value."""
    rows = tbl.findall("w:tr", NS)
    if rows and rows[0].find("w:trPr/w:tblHeader", NS) is not None:
        if header_col1 is not None:
            hdr_cells = rows[0].findall("w:tc", NS)
            if len(hdr_cells) >= 2:
                set_cell_text(hdr_cells[1], header_col1)
        rows = rows[1:]
    for row, val in zip(rows, values):
        cells = row.findall("w:tc", NS)
        if len(cells) >= 2:
            set_cell_text(cells[1], val)


def populate_data_table(
    tbl: ET.Element,
    data_rows: list[list[str]],
    template_row_index: int = 1,
    bold_last_row: bool = False,
) -> None:
    """Replaces all non-header rows of a table using a cloned template data row to preserve exact cell widths & borders."""
    existing_rows = tbl.findall("w:tr", NS)
    if len(existing_rows) <= template_row_index:
        return
    proto_row = copy.deepcopy(existing_rows[template_row_index])
    for r in existing_rows[1:]:
        tbl.remove(r)

    for r_idx, row_values in enumerate(data_rows):
        new_tr = copy.deepcopy(proto_row)
        is_bold = bold_last_row and (r_idx == len(data_rows) - 1)
        cells = new_tr.findall("w:tc", NS)
        for c_idx, cell in enumerate(cells):
            val = row_values[c_idx] if c_idx < len(row_values) else ""
            set_cell_text(cell, val, bold=True if is_bold else None)
        tbl.append(new_tr)


def set_paragraph_body_text(p: ET.Element, text: str) -> None:
    """Sets standard Calibri 11pt (sz=22) body text on a Normal paragraph while keeping pPr."""
    for child in list(p):
        if child.tag != w_tag("pPr"):
            p.remove(child)
    r = ET.SubElement(p, w_tag("r"))
    rPr = ET.SubElement(r, w_tag("rPr"))
    rf = ET.SubElement(rPr, w_tag("rFonts"))
    for attr in ("ascii", "cs", "eastAsia", "hAnsi"):
        rf.set(w_tag(attr), "Calibri")
    sz = ET.SubElement(rPr, w_tag("sz"))
    sz.set(w_tag("val"), "22")
    szCs = ET.SubElement(rPr, w_tag("szCs"))
    szCs.set(w_tag("val"), "22")
    t_el = ET.SubElement(r, w_tag("t"))
    t_el.set(f"{{{XML_NS}}}space", "preserve")
    t_el.text = text


def save_modified_docx(src_path: Path, dst_paths: list[Path], xml_root: ET.Element) -> None:
    # Ensure no table cell in the document retains template placeholder italic or #666666 grey color
    for rPr in xml_root.findall(".//w:tbl//w:rPr", NS):
        for i_tag in ("i", "iCs"):
            existing_i = rPr.find(f"w:{i_tag}", NS)
            if existing_i is not None:
                rPr.remove(existing_i)
            i_el = ET.SubElement(rPr, w_tag(i_tag))
            i_el.set(w_tag("val"), "false")
        col_el = rPr.find("w:color", NS)
        if col_el is not None and col_el.attrib.get(w_tag("val")) == "666666":
            rPr.remove(col_el)

    xml_bytes = ET.tostring(xml_root, encoding="utf-8", xml_declaration=True)
    with zipfile.ZipFile(src_path, "r") as zin:
        items = [(info, zin.read(info.filename)) for info in zin.infolist()]

    for dst in dst_paths:
        dst.parent.mkdir(parents=True, exist_ok=True)
        try:
            with zipfile.ZipFile(dst, "w", compression=zipfile.ZIP_DEFLATED) as zout:
                for info, data in items:
                    if info.filename == "word/document.xml":
                        zout.writestr(info, xml_bytes)
                    else:
                        zout.writestr(info, data)
        except PermissionError:
            alt = dst.with_name(f"{dst.stem}_updated{dst.suffix}")
            with zipfile.ZipFile(alt, "w", compression=zipfile.ZIP_DEFLATED) as zout:
                for info, data in items:
                    if info.filename == "word/document.xml":
                        zout.writestr(info, xml_bytes)
                    else:
                        zout.writestr(info, data)
            print(f"  [WARN] {dst} is open in Word; saved updated copy to {alt}")


# ==============================================================================
# 1. BM01 — Design Brief (Concise)
# ==============================================================================
def build_bm01(src_docx: Path, dst_paths: list[Path]) -> None:
    with zipfile.ZipFile(src_docx, "r") as z:
        root = ET.fromstring(z.read("word/document.xml"))
    body = root.find("w:body", NS)
    assert body is not None

    tables = body.findall("w:tbl", NS)
    # TBL 0: 0. Header
    populate_kv_table(
        tables[0],
        [
            "GFA26SE139",
            "SmartDroneInspection: AI-powered Infrastructure Inspection Management Platform",
            "FA26SE112 — Trần Hoàng Trung Hiếu (SE184212), Phùng Trung Quốc (SE170027), Trương Thái Như (SE180082), Trần Tùng Bách (SE180220)",
            "Phạm Minh Trí; Đặng Ngọc Minh Đức",
            "https://github.com/tungbach12/SmartDroneInspection-backend (tag: review-2)",
            "3.0",
            "09/11/2026",
        ],
    )

    # TBL 1: 1.1 Registration Changes
    populate_data_table(
        tables[1],
        [
            [
                "§3.2.b Actors",
                "5 actors (Admin, Manager, Inspector, Maintenance Engineer, Viewer).",
                "4 roles: Admin, Manager, Customer, Inspector.",
                "Replaces passive Viewer with Customer and drops Maintenance Engineer.",
            ],
            [
                "§3.2.b/c Maintenance",
                "Includes Maintenance Ticket / Work Order module.",
                "Removed from scope; focuses on 4 drone inspection workflows.",
                "Avoids construction ERP complexity to focus on drone inspection.",
            ],
            [
                "§3.2.c Service & Payment Flow",
                "Basic request creation without quote or payment.",
                "Adds Quotation, Contract, Report acceptance & online payment.",
                "Completes the end-to-end inspection service workflow.",
            ],
            [
                "§3.2.d/e Tech Stack",
                "ASP.NET Core, EF Core, SignalR, PostgreSQL.",
                "Java 21, Spring Boot 4.1, Spring Modulith, PostgreSQL 17, MinIO.",
                "Matches team expertise and modular monolith design.",
            ],
        ],
    )

    # TBL 2: 1.2 Out of Scope
    populate_data_table(
        tables[2],
        [
            [
                "Direct drone piloting & flight control",
                "Handled externally by SmartDroneHub and the field pilot.",
            ],
            [
                "Corrective Maintenance & Work Orders",
                "Repairs are handled externally by the Customer after receiving the report.",
            ],
            [
                "Government flight-permit issuance",
                "Granted offline by authorities; platform only verifies uploaded permit files.",
            ],
            [
                "Unreviewed AI defect publishing",
                "AI detections are advisory; Inspector and Manager review is mandatory.",
            ],
        ],
    )

    # Section 2: System at a Glance (2 short paragraphs)
    all_children = list(body)
    h2_sys_idx = next(
        i
        for i, el in enumerate(all_children)
        if el.tag == w_tag("p")
        and "".join(t.text or "" for t in el.findall(".//w:t", NS)).strip() == "2. System at a Glance"
    )
    h2_dec_idx = next(
        i
        for i, el in enumerate(all_children)
        if el.tag == w_tag("p")
        and "".join(t.text or "" for t in el.findall(".//w:t", NS)).strip() == "3. Key Design Decisions"
    )
    body_ps = [
        el
        for el in all_children[h2_sys_idx + 1 : h2_dec_idx]
        if el.tag == w_tag("p")
        and "666666" not in [c.attrib.get(w_tag("val")) for c in el.findall(".//w:color", NS)]
    ]
    if len(body_ps) >= 1:
        set_paragraph_body_text(
            body_ps[0],
            "SmartDroneInspection is a centralized platform connecting Customers with Partner Drone Inspectors to inspect infrastructure assets (bridges, buildings, power towers) safely and consistently.",
        )
    if len(body_ps) >= 2:
        set_paragraph_body_text(
            body_ps[1],
            "Customers register assets, accept quotes, and pay via PayOS. Inspectors register drones, execute checklist-gated flights with SmartDroneHub telemetry, confirm DroneVisionAI (YOLO11) defects, and submit reports for Manager publication (Report 4 SDD §1.1).",
        )

    # TBL 3: 3. Key Design Decisions
    populate_data_table(
        tables[3],
        [
            [
                "D1",
                "Backend architecture",
                "Microservices vs. Modular monolith",
                "Spring Modulith monolith: clear module boundaries and simple deployment.",
                "Trần Hoàng Trung Hiếu",
                "F-01, F-02 / SDD §1.2",
            ],
            [
                "D2",
                "Flight integration",
                "Built-in flight control vs. SmartDroneHub API",
                "Consume SmartDroneHub telemetry/logs to isolate flight safety from business logic.",
                "Phùng Trung Quốc",
                "F-04, F-05 / SDD §3.5",
            ],
            [
                "D3",
                "Field workflow",
                "Single form vs. Step-by-step gated flow",
                "7-step gated flow (Permit -> Pre-flight -> Flight -> Post-flight & Items -> Evidence -> Findings -> Report).",
                "Trần Tùng Bách",
                "F-05, F-06 / SDD §3.6",
            ],
            [
                "D4",
                "Media storage",
                "DB BLOBs vs. Object storage",
                "MinIO stores photos, MP4 videos, and PDFs; PostgreSQL stores metadata and hashes.",
                "Trần Tùng Bách",
                "F-02, F-06 / SDD §2.2",
            ],
            [
                "D5",
                "AI & Report review",
                "Auto-publish vs. Human review",
                "Inspector confirms AI findings baseline; independent Manager approves and publishes PDF.",
                "Trương Thái Như",
                "F-07, F-08 / SDD §3.7",
            ],
        ],
    )

    # TBL 4: 4. Top Risks
    populate_data_table(
        tables[4],
        [
            [
                "R1",
                "External service outage (SmartDroneHub, AI, PayOS)",
                "Blocks telemetry sync, defect detection, or payment webhook.",
                "Use 5 s timeouts, manual finding fallback, and idempotent webhook retry.",
                "Trần Tùng Bách",
            ],
            [
                "R2",
                "Cross-role data leak or self-approval",
                "Customer sees internal fees or Inspector approves own report.",
                "Enforce backend role/org guards and block author self-publication (BR-09).",
                "Trần Hoàng Trung Hiếu",
            ],
            [
                "R3",
                "Incomplete field check or weather abort",
                "Missing building items or aborted flight delays inspection.",
                "Require reason for unchecked items and support Manager reschedule on abort.",
                "Phùng Trung Quốc",
            ],
        ],
    )

    # TBL 5: 5. Known Gaps
    populate_data_table(
        tables[5],
        [
            [
                "G1",
                "Legacy Maintenance references in early docs",
                "SRS §3, SDD §2–3",
                "Remove Maintenance from SRS/SDD to match 4-workflow scope.",
                "Trương Thái Như",
                "12/11/2026",
            ],
            [
                "G2",
                "SDD state transition IDs not mapped to F-01..F-08",
                "Report 4 SDD §2.2",
                "Update transition labels to match F-01..F-08 and BR-01..BR-10.",
                "Trần Hoàng Trung Hiếu",
                "12/11/2026",
            ],
            [
                "G3",
                "5 staging walkthrough test cases still Pending",
                "Report 5 Test Report",
                "Run remaining 5 staging walkthroughs before Defense 1.1.",
                "Trần Tùng Bách",
                "15/11/2026",
            ],
        ],
    )

    # TBL 6: 6. Proposed Mandatory Features
    populate_data_table(
        tables[6],
        [
            [
                "F-01",
                "Auth, 4-Role RBAC & Partner Profiles",
                "Admin, Manager, Customer, Inspector",
                "JWT/OAuth2 login works by role; 5 failed logins lock for 15 min; unauthorized access returns 403.",
                "WF1-001..005",
                "Done",
            ],
            [
                "F-02",
                "Drone Registration & Safety Review",
                "Inspector, Manager",
                "Requires valid legal documents & unique serial; Manager approves or rejects with reason.",
                "WF1-006..016",
                "Done",
            ],
            [
                "F-03",
                "Asset Airspace Gate & Inspection Items",
                "Customer, Manager",
                "Blocks assets in NO_FLY_ZONE (403); saves valid GPS asset and target Inspection Items.",
                "WF1-017..021",
                "Done",
            ],
            [
                "F-04",
                "Service Request, Quote, Contract & Dispatch",
                "Customer, Manager",
                "Customer accepts quote; Manager uploads signed contract and dispatches conflict-free Inspector & Drone.",
                "WF2-001..009",
                "Done",
            ],
            [
                "F-05",
                "Permit Gate, Checklists & Field Session",
                "Inspector, Manager",
                "Requires Permit & Pre-flight check to start; records MAVLink log, Building Items & Post-flight check on complete.",
                "WF2-010..020",
                "Done",
            ],
            [
                "F-06",
                "Evidence Upload & AI Defect Confirmation",
                "Inspector, DroneVisionAI",
                "Photo/MP4 upload triggers YOLO11 candidates; Inspector confirms/rejects findings and locks baseline.",
                "WF3-001..010",
                "Done",
            ],
            [
                "F-07",
                "Auto-Compiled Report & Manager Review",
                "Inspector, Manager",
                "Compiles draft report with AI summary; independent Manager publishes immutable PDF or returns with reason.",
                "WF4-001..008",
                "Done",
            ],
            [
                "F-08",
                "Customer Acceptance & PayOS Settlement",
                "Customer, Manager, Inspector",
                "Customer accepts published report and pays via PayOS (VietQR); system marks PAID and calculates net payout.",
                "WF3-011..017, WF4-009..016",
                "In progress",
            ],
        ],
    )

    # TBL 7: 7. Non-Functional Requirements
    populate_data_table(
        tables[7],
        [
            [
                "NFR-01",
                "Performance",
                "p95 API response time",
                "<= 2.0 s at 50 concurrent users",
                "Load test on staging API endpoints (WF2-016).",
            ],
            [
                "NFR-02",
                "AI Latency",
                "YOLO11 detection & LLM summary time",
                "<= 5.0 s per request",
                "Timed integration test with sample drone images (WF3-007).",
            ],
            [
                "NFR-03",
                "Authorization",
                "Unauthorized cross-role/org requests blocked",
                "100% blocked (HTTP 401/403)",
                "Automated RBAC negative test suite (WF1-005).",
            ],
            [
                "NFR-04",
                "Auth Security",
                "Brute-force login lockout & rate limit",
                "15 min lock after 5 fails; <= 10 req/min",
                "Automated login security test (WF1-004).",
            ],
            [
                "NFR-05",
                "Integrity",
                "Published report PDF & contract immutability",
                "100% SHA-256 match; 0 edits after publish",
                "Automated hash & mutation-rejection test (WF3-016).",
            ],
        ],
    )

    # TBL 8: 8. Ownership Map
    populate_data_table(
        tables[8],
        [
            [
                "Trần Hoàng Trung Hiếu (SE184212)",
                "Leader",
                "F-01 (Auth/RBAC), F-02 (Drone Registration & Review)",
                "WF-01 — Partner Drone Registration & Review",
                "D1, R2 / PR #84, #88",
            ],
            [
                "Phùng Trung Quốc (SE170027)",
                "Member",
                "F-03 (Asset & Items), F-04 (Quote & Dispatch)",
                "WF-02 — Quotation, Contract & Dispatch",
                "D2, R3 / PR #82, #83",
            ],
            [
                "Trần Tùng Bách (SE180220)",
                "Member",
                "F-05 (Permit, Checklists & Flight), F-06 (Evidence & AI)",
                "WF-03 — Field Inspection & AI Defect Check",
                "D3, D4, R1 / PR #85, #89",
            ],
            [
                "Trương Thái Như (SE180082)",
                "Member",
                "F-07 (Report & Review), F-08 (Acceptance & PayOS)",
                "WF-04 — Report Review & Payment Settlement",
                "D5 / PR #86, #87",
            ],
        ],
    )

    # TBL 9: Appendix A1. Main Workflows
    populate_data_table(
        tables[9],
        [
            [
                "WF-01",
                "Partner Drone Registration & Review",
                "Inspector, Manager, System",
                "Inspector submits drone with legal documents.",
                "Drone is verified and activated for dispatch.",
                "F-01, F-02",
                "DroneRegistration: PENDING -> APPROVED / REJECTED; Drone: -> ACTIVE",
                "Trần Hoàng Trung Hiếu",
            ],
            [
                "WF-02",
                "Quotation, Contract & Dispatch",
                "Customer, Manager, Inspector",
                "Customer registers asset and submits request.",
                "Quote accepted, contract uploaded, mission scheduled.",
                "F-03, F-04",
                "ServiceRequest: SUBMITTED -> QUOTED -> QUOTE_ACCEPTED -> DISPATCHED; Inspection: -> SCHEDULED",
                "Phùng Trung Quốc",
            ],
            [
                "WF-03",
                "Field Inspection & AI Defect Check",
                "Inspector, Manager, DroneVisionAI",
                "Inspector uploads permit and starts session.",
                "Checklists, building items, evidence & AI findings locked.",
                "F-05, F-06",
                "Inspection: SCHEDULED -> IN_PROGRESS -> FIELD_COMPLETED; Finding: CANDIDATE -> CONFIRMED",
                "Trần Tùng Bách",
            ],
            [
                "WF-04",
                "Report Review & Payment Settlement",
                "Inspector, Manager, Customer, PayOS",
                "Field inspection reaches FIELD_COMPLETED.",
                "Report published, accepted, paid via PayOS, and settled.",
                "F-07, F-08",
                "Report: DRAFT -> SUBMITTED -> PUBLISHED; Invoice: UNPAID -> PAID; Payout: -> SETTLED",
                "Trương Thái Như",
            ],
        ],
    )

    # TBL 10: Appendix A2. Demo Scenarios
    populate_data_table(
        tables[10],
        [
            [
                "DS-01a",
                "WF-01",
                "Main",
                "Active Inspector; valid drone legal documents.",
                "1. Submit drone & legal docs.\n2. Manager approves.",
                "Status -> APPROVED; Drone is ACTIVE.",
                "Trần Hoàng Trung Hiếu",
            ],
            [
                "DS-01b",
                "WF-01",
                "Exception",
                "Duplicate serial; reject without reason.",
                "1. Submit duplicate serial.\n2. Reject with empty reason.",
                "Blocked with 400/409 (BR-01, BR-02).",
                "Trần Hoàng Trung Hiếu",
            ],
            [
                "DS-02a",
                "WF-02",
                "Main",
                "Customer in CLEAR_ZONE; free Inspector+Drone.",
                "1. Create asset & request.\n2. Accept quote.\n3. Upload contract & dispatch.",
                "Request -> DISPATCHED; Inspection -> SCHEDULED.",
                "Phùng Trung Quốc",
            ],
            [
                "DS-02b",
                "WF-02",
                "Exception",
                "Asset in NO_FLY_ZONE; busy Inspector.",
                "1. Create asset in NFZ.\n2. Dispatch busy Inspector.",
                "Blocked with 403 NFZ (BR-03) & 409 Conflict (BR-05).",
                "Phùng Trung Quốc",
            ],
            [
                "DS-03a",
                "WF-03",
                "Main",
                "SCHEDULED mission; permit & media ready.",
                "1. Upload permit & pre-flight check -> Start.\n2. Check building items & post-flight.\n3. Upload media & confirm AI findings.",
                "Findings locked; Inspection -> FIELD_COMPLETED.",
                "Trần Tùng Bách",
            ],
            [
                "DS-03b",
                "WF-03",
                "Exception",
                "Missing permit; unchecked item without reason; abort.",
                "1. Start without permit.\n2. Complete with missing reason.\n3. Abort session.",
                "Steps 1–2 blocked; Step 3 sets ABORTED for reschedule.",
                "Trần Tùng Bách",
            ],
            [
                "DS-04a",
                "WF-04",
                "Main",
                "FIELD_COMPLETED mission with locked findings.",
                "1. Submit auto-compiled report.\n2. Manager publishes PDF.\n3. Customer accepts & pays via PayOS.",
                "Report -> PUBLISHED; Invoice -> PAID; Payout -> SETTLED.",
                "Trương Thái Như",
            ],
            [
                "DS-04b",
                "WF-04",
                "Exception",
                "Self-approval; return without reason; early pay.",
                "1. Author tries to publish.\n2. Return without reason.\n3. Pay before publish.",
                "Blocked with 403/400 (BR-09, BR-10).",
                "Trương Thái Như",
            ],
        ],
    )

    # TBL 11: Appendix A3. Functional Test Case Target
    populate_data_table(
        tables[11],
        [
            ["Mandatory features (F-01..F-08)", "8", "3", "42"],
            ["Main workflows (end-to-end)", "4", "1", "4"],
            ["State transitions of main entities", "14", "1", "14"],
            ["Agreed NFRs (NFR-01..NFR-05)", "5", "1", "5"],
            ["Committed total", "—", "—", "65 (56 Automated = 86.15%)"],
        ],
        bold_last_row=True,
    )

    for p in list(body.findall("w:p", NS)):
        colors = [c.attrib.get(w_tag("val")) for c in p.findall(".//w:color", NS)]
        if "666666" in colors:
            body.remove(p)

    save_modified_docx(src_docx, dst_paths, root)


# ==============================================================================
# 2. BM02 — SRS/SDD Self-Review Report (Concise)
# ==============================================================================
def build_bm02(src_docx: Path, dst_paths: list[Path]) -> None:
    with zipfile.ZipFile(src_docx, "r") as z:
        root = ET.fromstring(z.read("word/document.xml"))
    body = root.find("w:body", NS)
    assert body is not None
    tables = body.findall("w:tbl", NS)

    populate_kv_table(
        tables[0],
        [
            "GFA26SE139",
            "SmartDroneInspection: AI-powered Infrastructure Inspection Management Platform",
            "FA26SE112 — Trần Hoàng Trung Hiếu (SE184212), Phùng Trung Quốc (SE170027), Trương Thái Như (SE180082), Trần Tùng Bách (SE180220)",
            "Phạm Minh Trí; Đặng Ngọc Minh Đức",
            "Claude Code — Claude Sonnet 5.5",
            "04/11/2026",
            "tag: review-2",
            "v2.0 (Review 2 Registration Form)",
            "3.0",
            "09/11/2026",
        ],
    )

    findings_rows = [
        [
            "SR-01",
            "Scope",
            "Registration §3.2; SRS §3",
            "Maintenance Work Order module adds extra complexity outside core drone inspection.",
            "High",
            "SRS §§3.8–3.9 vs. 4-workflow scope",
            "Fixed – Removed Maintenance module from scope.",
        ],
        [
            "SR-02",
            "Requirements",
            "SRS §3; SDD §2.2",
            "SDD state transitions use legacy FR IDs instead of F-01..F-08.",
            "High",
            "SDD §2.2 state tables",
            "Planned – Trần Hoàng Trung Hiếu, due 12/11/2026.",
        ],
        [
            "SR-03",
            "Flows",
            "Report 5 Test Suite",
            "5 of 65 test cases (staging walkthroughs) are still Pending.",
            "High",
            "WF1-010, WF2-015, WF3-012, WF3-017, WF4-011",
            "Planned – Trần Tùng Bách, due 15/11/2026.",
        ],
        [
            "SR-04",
            "Scope",
            "SRS §3.6",
            "SRS adds Flight Permit gate, Pre/Post-flight checklists, and Building Items check.",
            "Medium",
            "FieldSessionPage & SRS §3.6",
            "Kept – Required for flight safety and field coverage.",
        ],
        [
            "SR-05",
            "Architecture",
            "Registration §3.2.b; SRS §3.7",
            "Registration uses DroneVisionAI while SRS/code also name YOLO11.",
            "Medium",
            "YoloInferenceClient.java & SRS §3.7",
            "Kept – DroneVisionAI is the module; YOLO11 is the model.",
        ],
        [
            "SR-06",
            "States",
            "Inspection.java; SDD §2.2",
            "State transition preconditions are enforced in service layer rather than entity setter.",
            "Medium",
            "InspectionWorkflowService.java",
            "Fixed – Verified by service state-transition tests.",
        ],
        [
            "SR-07",
            "Flows",
            "SDD §3.5.3 Activity Diagram",
            "Activity diagram omitted the ABORTED session reschedule branch.",
            "Low",
            "SDD §3.5.3 vs. /abort API",
            "Fixed – Added ABORTED -> Reschedule branch to diagram.",
        ],
        [
            "SR-08",
            "Requirements",
            "SRS §4.2 NFR prose",
            "General availability prose lacked a test method, unlike table NFR-01..NFR-05.",
            "Low",
            "SRS §4.2",
            "Fixed – Standardized on NFR-01..NFR-05 table.",
        ],
    ]
    populate_data_table(tables[2], findings_rows)

    populate_data_table(
        tables[3],
        [
            ["1", "SR-01", "Remove Maintenance module to focus 100% on the 4 Drone Inspection workflows (WF-01..WF-04)."],
            ["2", "SR-02", "Align SDD §2.2 state transition IDs with SRS feature IDs (F-01..F-08)."],
            ["3", "SR-03", "Complete the remaining 5 staging walkthrough test cases before Defense 1.1."],
            ["4", "SR-04", "Keep Flight Permit gate, Pre/Post-flight checklists, and Building Items check in WF-03."],
            ["5", "SR-05", "Clarify DroneVisionAI (subsystem) vs. YOLO11 (model) naming across docs."],
        ],
    )

    populate_data_table(
        tables[4],
        [
            ["High", "3", "1", "0", "2"],
            ["Medium", "3", "1", "2", "0"],
            ["Low", "2", "2", "0", "0"],
        ],
    )

    for p in list(body.findall("w:p", NS)):
        colors = [c.attrib.get(w_tag("val")) for c in p.findall(".//w:color", NS)]
        if "666666" in colors:
            body.remove(p)

    save_modified_docx(src_docx, dst_paths, root)


# ==============================================================================
# 3. BM03 — Registration Form Record of Changes (Concise)
# ==============================================================================
def build_bm03(src_docx: Path, dst_paths: list[Path]) -> None:
    with zipfile.ZipFile(src_docx, "r") as z:
        root = ET.fromstring(z.read("word/document.xml"))
    body = root.find("w:body", NS)
    assert body is not None
    tables = body.findall("w:tbl", NS)

    populate_kv_table(
        tables[0],
        [
            "GFA26SE139",
            "SmartDroneInspection: AI-powered Infrastructure Inspection Management Platform",
            "FA26SE112 — Trần Hoàng Trung Hiếu (SE184212), Phùng Trung Quốc (SE170027), Trương Thái Như (SE180082), Trần Tùng Bách (SE180220)",
            "Phạm Minh Trí; Đặng Ngọc Minh Đức",
            "v1.0 (19/08/2026)",
            "v2.0 (09/11/2026)",
            "3.0",
            "09/11/2026",
        ],
    )

    populate_data_table(
        tables[1],
        [
            [
                "01",
                "§3.2.b Human Actors",
                "5 actors: Admin, Manager, Inspector, Maintenance Engineer, Viewer.",
                "4 actors: Admin, Manager, Customer, Inspector.",
                "Replaces passive Viewer with Customer and drops Maintenance Engineer.",
                "Trần Hoàng Trung Hiếu",
            ],
            [
                "02",
                "§3.2.b/c/f Maintenance Scope",
                "Includes Maintenance Ticket / Work Order module.",
                "Removes Maintenance module; focuses on 4 Inspection workflows (WF-01..WF-04).",
                "Focuses depth on drone inspection and AI defect reporting.",
                "Trương Thái Như",
            ],
            [
                "03",
                "§3.2.b/c Service & Payment Flow",
                "Basic request creation without quote or payment.",
                "Adds Quotation, Contract, Report acceptance & online payment.",
                "Completes the end-to-end inspection service workflow.",
                "Phùng Trung Quốc",
            ],
            [
                "04",
                "§3.2.d/e Tech Stack",
                "ASP.NET Core, EF Core, SignalR, PostgreSQL.",
                "Java 21, Spring Boot 4.1, Spring Modulith, PostgreSQL 17, MinIO.",
                "Aligns with team expertise and modular monolith architecture.",
                "Trần Hoàng Trung Hiếu",
            ],
        ],
    )

    populate_data_table(
        tables[2],
        [
            ["01", "Pending Review 2", ""],
            ["02", "Pending Review 2", ""],
            ["03", "Pending Review 2", ""],
            ["04", "Pending Review 2", ""],
        ],
    )

    for p in list(body.findall("w:p", NS)):
        colors = [c.attrib.get(w_tag("val")) for c in p.findall(".//w:color", NS)]
        if "666666" in colors:
            body.remove(p)

    save_modified_docx(src_docx, dst_paths, root)


# ==============================================================================
# 4. BM04 — Review 2 Commitment (Concise)
# ==============================================================================
def build_bm04(src_docx: Path, dst_paths: list[Path]) -> None:
    with zipfile.ZipFile(src_docx, "r") as z:
        root = ET.fromstring(z.read("word/document.xml"))
    body = root.find("w:body", NS)
    assert body is not None

    children = list(body)

    def find_p_index(text_prefix: str) -> int:
        for i, el in enumerate(children):
            if el.tag == w_tag("p"):
                txt = "".join(t.text or "" for t in el.findall(".//w:t", NS)).strip()
                if txt.startswith(text_prefix):
                    return i
        return -1

    idx_65 = find_p_index("6.5 Workflow WF-05")
    idx_70 = find_p_index("7. Individual Commitments")
    if idx_65 != -1 and idx_70 != -1:
        for el in children[idx_65:idx_70]:
            body.remove(el)

    children = list(body)
    idx_75 = find_p_index("7.5 Member 5")
    idx_80 = find_p_index("8. Summary and Cross-check")
    if idx_75 != -1 and idx_80 != -1:
        for el in children[idx_75:idx_80]:
            body.remove(el)

    tables = body.findall("w:tbl", NS)

    # TBL 0: 1. Project Information
    populate_kv_table(
        tables[0],
        [
            "GFA26SE139",
            "SmartDroneInspection: AI-powered Infrastructure Inspection Management Platform",
            "FA26SE112 — Trần Hoàng Trung Hiếu (SE184212), Phùng Trung Quốc (SE170027), Trương Thái Như (SE180082), Trần Tùng Bách (SE180220)",
            "Phạm Minh Trí; Đặng Ngọc Minh Đức",
            "09/11/2026",
            "Reviewer 1",
            "Reviewer 2",
            "3.0",
            "09/11/2026",
        ],
    )

    # TBL 1: 2. Final Registration Form
    populate_kv_table(
        tables[1],
        [
            "v2.0 (09/11/2026)",
            "Yes (Pending committee sign-off)",
            "SWP490_GFA26SE139_R2_Registration.pdf",
        ],
    )

    # TBL 2: 3. Mandatory Features
    populate_data_table(
        tables[2],
        [
            [
                "F-01",
                "Auth, 4-Role RBAC & Partner Profiles",
                "Admin, Manager, Customer, Inspector",
                "Role-scoped JWT login; 15-min lockout after 5 fails; 403 on unauthorized access.",
                "WF-01",
                "Trần Hoàng Trung Hiếu",
            ],
            [
                "F-02",
                "Drone Registration & Safety Review",
                "Inspector, Manager",
                "Requires valid legal documents & unique serial; Manager approves (ACTIVE) or rejects with reason.",
                "WF-01",
                "Trần Hoàng Trung Hiếu",
            ],
            [
                "F-03",
                "Asset Airspace Gate & Inspection Items",
                "Customer, Manager",
                "Blocks NO_FLY_ZONE assets (403); saves valid GPS asset and Inspection Items.",
                "WF-02",
                "Phùng Trung Quốc",
            ],
            [
                "F-04",
                "Service Request, Quote, Contract & Dispatch",
                "Customer, Manager",
                "Customer accepts quote; Manager uploads contract and dispatches available Inspector+Drone.",
                "WF-02",
                "Phùng Trung Quốc",
            ],
            [
                "F-05",
                "Permit Gate, Checklists & Field Session",
                "Inspector, Manager",
                "Requires Permit & Pre-flight check to start; saves MAVLink log, Building Items & Post-flight check.",
                "WF-03",
                "Trần Tùng Bách",
            ],
            [
                "F-06",
                "Evidence Upload & AI Defect Confirmation",
                "Inspector, DroneVisionAI",
                "Media upload triggers YOLO11 candidates; Inspector confirms/rejects and locks baseline.",
                "WF-03",
                "Trần Tùng Bách",
            ],
            [
                "F-07",
                "Auto-Compiled Report & Manager Review",
                "Inspector, Manager",
                "Compiles draft report with AI summary; Manager publishes PDF or returns with reason.",
                "WF-04",
                "Trương Thái Như",
            ],
            [
                "F-08",
                "Customer Acceptance & PayOS Settlement",
                "Customer, Manager, Inspector",
                "Customer accepts published report and pays via PayOS; system marks PAID and settles payout.",
                "WF-04",
                "Trương Thái Như",
            ],
        ],
    )

    # TBL 3: 4. Non-Functional Requirements
    populate_data_table(
        tables[3],
        [
            [
                "NFR-01",
                "Performance",
                "p95 API response time",
                "<= 2.0 s (50 users)",
                "Load test on staging APIs (WF2-016).",
                "Phùng Trung Quốc",
            ],
            [
                "NFR-02",
                "AI Latency",
                "YOLO11 & LLM summary time",
                "<= 5.0 s / request",
                "Timed integration test (WF3-007).",
                "Trần Tùng Bách",
            ],
            [
                "NFR-03",
                "Authorization",
                "Unauthorized access blocked",
                "100% blocked (401/403)",
                "Automated RBAC negative tests (WF1-005).",
                "Trần Hoàng Trung Hiếu",
            ],
            [
                "NFR-04",
                "Auth Security",
                "Login lockout & rate limit",
                "5 fails -> 15m lock",
                "Automated brute-force test (WF1-004).",
                "Trần Hoàng Trung Hiếu",
            ],
            [
                "NFR-05",
                "Integrity",
                "Published PDF immutability",
                "100% SHA-256 match",
                "Automated hash & edit-block test (WF3-016).",
                "Trương Thái Như",
            ],
        ],
    )

    # TBL 4: 5. Out of Scope
    populate_data_table(
        tables[4],
        [
            [
                "Direct drone piloting & flight control",
                "Executed externally by SmartDroneHub and the field pilot.",
            ],
            [
                "Corrective Maintenance & Work Orders",
                "Repairs are handled externally by the Customer after inspection.",
            ],
            [
                "Government flight-permit issuance",
                "Granted offline by authorities; platform only verifies permit upload.",
            ],
            [
                "Unreviewed AI defect publishing",
                "AI detections are advisory; Inspector and Manager review is required.",
            ],
        ],
    )

    # Section 6: Workflow blocks (WF-01..WF-04)
    wf_specs = [
        {
            "kv": [
                "WF-01 · Partner Drone Registration & Review",
                "Trần Hoàng Trung Hiếu (SE184212)",
                "Phùng Trung Quốc (SE170027)",
                "Inspector, Manager, Admin, System",
                "Inspector submits a drone registration with legal documents.",
                "Drone is verified and activated in the fleet roster.",
                "DroneRegistration: PENDING -> APPROVED / REJECTED; Drone: -> ACTIVE",
                "Report 4 SDD §3.3.3",
            ],
            "features": [
                ["F-01", "Auth, 4-Role RBAC & Partner Profiles", "Role JWT login, 5-fail lockout, 403 on cross-role access.", "WF1-001..005"],
                ["F-02", "Drone Registration & Safety Review", "Valid legal documents & unique serial; Manager approves or rejects with reason.", "WF1-006..016"],
            ],
            "demos": [
                [
                    "DS-01a",
                    "Main",
                    "Active Inspector; valid drone legal documents.",
                    "1. Submit drone & legal docs.\n2. Manager reviews and approves.",
                    "Status -> APPROVED; Drone -> ACTIVE.",
                    "Trần Hoàng Trung Hiếu",
                ],
                [
                    "DS-01b",
                    "Exception",
                    "Duplicate serial; reject without reason.",
                    "1. Submit duplicate serial.\n2. Reject with empty reason.",
                    "Blocked with 400/409 (BR-01, BR-02).",
                    "Trần Hoàng Trung Hiếu",
                ],
            ],
            "tests": [
                ["Feature tests (≥ 3 per feature)", "12", "11", "Trần Hoàng Trung Hiếu"],
                ["End-to-end workflow test (≥ 1)", "1", "1", "Trần Hoàng Trung Hiếu"],
                ["State transition tests (≥ 1 per transition)", "3", "2", "Trần Hoàng Trung Hiếu"],
                ["Total for this workflow", "16", "14", "Trần Hoàng Trung Hiếu"],
            ],
            "pass": ["Yes", "Yes", "100%", "≥ 90%", "0"],
        },
        {
            "kv": [
                "WF-02 · Quotation, Contract & Dispatch",
                "Phùng Trung Quốc (SE170027)",
                "Trần Hoàng Trung Hiếu (SE184212)",
                "Customer, Manager, Inspector, System",
                "Customer registers an asset and submits a Service Request.",
                "Quote accepted, contract uploaded, and Inspector+Drone dispatched.",
                "ServiceRequest: SUBMITTED -> QUOTED -> QUOTE_ACCEPTED -> DISPATCHED; Inspection: -> SCHEDULED",
                "Report 4 SDD §3.5.3",
            ],
            "features": [
                ["F-03", "Asset Airspace Gate & Inspection Items", "Blocks NO_FLY_ZONE (403); saves valid asset & Inspection Items.", "WF1-017..021"],
                ["F-04", "Service Request, Quote, Contract & Dispatch", "Quote acceptance, contract upload & conflict-free dispatch.", "WF2-001..009, 016"],
            ],
            "demos": [
                [
                    "DS-02a",
                    "Main",
                    "Customer in CLEAR_ZONE; free Inspector+Drone.",
                    "1. Create asset & request.\n2. Accept quote.\n3. Upload contract & dispatch.",
                    "Request -> DISPATCHED; Inspection -> SCHEDULED.",
                    "Phùng Trung Quốc",
                ],
                [
                    "DS-02b",
                    "Exception",
                    "Asset in NO_FLY_ZONE; busy Inspector.",
                    "1. Create asset in NFZ.\n2. Dispatch busy Inspector.",
                    "Blocked with 403 NFZ & 409 Conflict.",
                    "Phùng Trung Quốc",
                ],
            ],
            "tests": [
                ["Feature tests (≥ 3 per feature)", "11", "10", "Phùng Trung Quốc"],
                ["End-to-end workflow test (≥ 1)", "1", "1", "Phùng Trung Quốc"],
                ["State transition tests (≥ 1 per transition)", "4", "3", "Phùng Trung Quốc"],
                ["Total for this workflow", "16", "14", "Phùng Trung Quốc"],
            ],
            "pass": ["Yes", "Yes", "100%", "≥ 90%", "0"],
        },
        {
            "kv": [
                "WF-03 · Field Inspection & AI Defect Check",
                "Trần Tùng Bách (SE180220)",
                "Phùng Trung Quốc (SE170027)",
                "Inspector, Manager, System (DroneVisionAI)",
                "Inspector uploads Flight Permit and starts pre-flight check.",
                "Checklists, building items, evidence & AI findings baseline locked.",
                "Inspection: SCHEDULED -> IN_PROGRESS -> FIELD_COMPLETED; Finding: CANDIDATE -> CONFIRMED",
                "Report 4 SDD §3.6.3",
            ],
            "features": [
                ["F-05", "Permit Gate, Checklists & Field Session", "Permit & Pre-flight gate; MAVLink log, Building Items & Post-flight check.", "WF2-010..015, 017..020"],
                ["F-06", "Evidence Upload & AI Defect Confirmation", "Photo/MP4 upload, YOLO11 detection & Findings Baseline lock.", "WF3-001..009, 017"],
            ],
            "demos": [
                [
                    "DS-03a",
                    "Main",
                    "SCHEDULED mission; permit & media ready.",
                    "1. Upload permit & pre-flight -> Start.\n2. Check building items & post-flight.\n3. Upload media & confirm AI findings.",
                    "Baseline locked; Inspection -> FIELD_COMPLETED.",
                    "Trần Tùng Bách",
                ],
                [
                    "DS-03b",
                    "Exception",
                    "Missing permit; unchecked item without reason; abort.",
                    "1. Start without permit.\n2. Complete without reason.\n3. Abort session.",
                    "Steps 1–2 blocked; Step 3 sets ABORTED.",
                    "Trần Tùng Bách",
                ],
            ],
            "tests": [
                ["Feature tests (≥ 3 per feature)", "12", "10", "Trần Tùng Bách"],
                ["End-to-end workflow test (≥ 1)", "1", "1", "Trần Tùng Bách"],
                ["State transition tests (≥ 1 per transition)", "4", "3", "Trần Tùng Bách"],
                ["Total for this workflow", "17", "14", "Trần Tùng Bách"],
            ],
            "pass": ["Yes", "Yes", "100%", "≥ 90%", "0"],
        },
        {
            "kv": [
                "WF-04 · Report Review & Payment Settlement",
                "Trương Thái Như (SE180082)",
                "Trần Tùng Bách (SE180220)",
                "Inspector, Manager, Customer, PayOS",
                "Inspection reaches FIELD_COMPLETED with locked findings.",
                "Report published, accepted, paid via PayOS, and settled to Inspector.",
                "Report: DRAFT -> SUBMITTED -> PUBLISHED; Invoice: UNPAID -> PAID; Payout: -> SETTLED",
                "Report 4 SDD §3.7.3",
            ],
            "features": [
                ["F-07", "Auto-Compiled Report & Manager Review", "Draft report with AI summary; Manager publishes PDF or returns with reason.", "WF3-010, WF4-001..008"],
                ["F-08", "Customer Acceptance & PayOS Settlement", "Customer accepts report, pays via PayOS, and triggers net payout.", "WF3-011..016, WF4-009..016"],
            ],
            "demos": [
                [
                    "DS-04a",
                    "Main",
                    "FIELD_COMPLETED mission with locked findings.",
                    "1. Submit report.\n2. Manager publishes PDF.\n3. Customer accepts & pays via PayOS.",
                    "Report -> PUBLISHED; Invoice -> PAID; Payout -> SETTLED.",
                    "Trương Thái Như",
                ],
                [
                    "DS-04b",
                    "Exception",
                    "Self-approval; return without reason; early pay.",
                    "1. Author tries to publish.\n2. Return without reason.\n3. Pay before publish.",
                    "Blocked with 403/400 (BR-09, BR-10).",
                    "Trương Thái Như",
                ],
            ],
            "tests": [
                ["Feature tests (≥ 3 per feature)", "12", "11", "Trương Thái Như"],
                ["End-to-end workflow test (≥ 1)", "1", "1", "Trương Thái Như"],
                ["State transition tests (≥ 1 per transition)", "3", "2", "Trương Thái Như"],
                ["Total for this workflow", "16", "14", "Trương Thái Như"],
            ],
            "pass": ["Yes", "Yes", "100%", "≥ 90%", "0"],
        },
    ]

    for idx, wf in enumerate(wf_specs):
        base = 5 + idx * 6
        populate_kv_table(tables[base + 0], wf["kv"])
        populate_data_table(tables[base + 1], wf["features"])
        populate_data_table(tables[base + 2], wf["demos"])
        populate_data_table(tables[base + 3], wf["tests"], bold_last_row=True)
        populate_kv_table(tables[base + 4], wf["pass"], header_col1="Target")
        populate_kv_table(tables[base + 5], [""])

    # Section 7: Individual Commitments (4 members)
    members_specs = [
        {
            "info": ["Trần Hoàng Trung Hiếu", "SE184212", "Team Leader"],
            "ownership": [
                ["Main workflow(s) owned", "WF-01", "Partner Drone Registration & Review"],
                ["Mandatory features owned", "F-01, F-02", "Auth/RBAC & Drone Registration Review"],
                ["Modules / entities owned", "users, drones", "UserAccount, InspectorProfile, Drone"],
                ["Design decisions owned (D-IDs)", "D1", "Spring Modulith monolith architecture"],
                ["NFRs responsible", "NFR-03, NFR-04", "RBAC authorization & login security"],
            ],
            "delivery": [
                ["Functional test cases written", "16", "15/11/2026"],
                ["Of which automated in CI", "14", "15/11/2026"],
                ["Demo scenarios presented", "2 (DS-01a, DS-01b)", "Defense 1.1"],
                ["Required fixes owned (section 9)", "FX-01, FX-02", "15/11/2026"],
                ["Documentation sections (Report / section)", "Report 1–2, SRS §2–3.3, SDD §1–2, BM01, BM03", "12/11/2026"],
            ],
        },
        {
            "info": ["Phùng Trung Quốc", "SE170027", "Member"],
            "ownership": [
                ["Main workflow(s) owned", "WF-02", "Quotation, Contract & Dispatch"],
                ["Mandatory features owned", "F-03, F-04", "Asset Airspace Gate & Quote/Dispatch"],
                ["Modules / entities owned", "assets, contracts", "Asset, ServiceRequest, ServiceQuote"],
                ["Design decisions owned (D-IDs)", "D2", "SmartDroneHub API consumer boundary"],
                ["NFRs responsible", "NFR-01", "p95 <= 2.0 s API performance"],
            ],
            "delivery": [
                ["Functional test cases written", "16", "15/11/2026"],
                ["Of which automated in CI", "14", "15/11/2026"],
                ["Demo scenarios presented", "2 (DS-02a, DS-02b)", "Defense 1.1"],
                ["Required fixes owned (section 9)", "FX-03", "15/11/2026"],
                ["Documentation sections (Report / section)", "SRS §§3.4–3.5, SDD §§3.4–3.5, Report 5", "12/11/2026"],
            ],
        },
        {
            "info": ["Trần Tùng Bách", "SE180220", "Member"],
            "ownership": [
                ["Main workflow(s) owned", "WF-03", "Field Inspection & AI Defect Check"],
                ["Mandatory features owned", "F-05, F-06", "Permit/Checklists & Evidence/AI Findings"],
                ["Modules / entities owned", "inspections, ai", "FieldSession, Evidence, Finding"],
                ["Design decisions owned (D-IDs)", "D3, D4", "7-step field flow & MinIO storage"],
                ["NFRs responsible", "NFR-02", "YOLO11 & LLM latency <= 5.0 s"],
            ],
            "delivery": [
                ["Functional test cases written", "17", "15/11/2026"],
                ["Of which automated in CI", "14", "15/11/2026"],
                ["Demo scenarios presented", "2 (DS-03a, DS-03b)", "Defense 1.1"],
                ["Required fixes owned (section 9)", "FX-04", "15/11/2026"],
                ["Documentation sections (Report / section)", "SRS §3.6, SDD §3.6, Report 5, BM02", "12/11/2026"],
            ],
        },
        {
            "info": ["Trương Thái Như", "SE180082", "Member"],
            "ownership": [
                ["Main workflow(s) owned", "WF-04", "Report Review & Payment Settlement"],
                ["Mandatory features owned", "F-07, F-08", "Report Review & PayOS Settlement"],
                ["Modules / entities owned", "reports, settlement", "InspectionReport, ServiceInvoice, Payout"],
                ["Design decisions owned (D-IDs)", "D5", "Human-in-the-loop report governance"],
                ["NFRs responsible", "NFR-05", "SHA-256 PDF immutability"],
            ],
            "delivery": [
                ["Functional test cases written", "16", "15/11/2026"],
                ["Of which automated in CI", "14", "15/11/2026"],
                ["Demo scenarios presented", "2 (DS-04a, DS-04b)", "Defense 1.1"],
                ["Required fixes owned (section 9)", "FX-05", "15/11/2026"],
                ["Documentation sections (Report / section)", "SRS §3.7, SDD §3.7, Report 5, BM04", "12/11/2026"],
            ],
        },
    ]

    for m_idx, mem in enumerate(members_specs):
        base = 29 + m_idx * 5
        populate_kv_table(tables[base + 0], mem["info"])
        populate_data_table(tables[base + 1], mem["ownership"])
        populate_data_table(tables[base + 2], mem["delivery"])
        populate_kv_table(tables[base + 4], [f"{mem['info'][0]} — 09/11/2026"])

    # Section 8: Summary and Cross-check
    populate_data_table(
        tables[49],
        [
            ["WF-01", "Trần Hoàng Trung Hiếu", "F-01, F-02", "2 (1 Main / 1 Exc)", "16", "14"],
            ["WF-02", "Phùng Trung Quốc", "F-03, F-04", "2 (1 Main / 1 Exc)", "16", "14"],
            ["WF-03", "Trần Tùng Bách", "F-05, F-06", "2 (1 Main / 1 Exc)", "17", "14"],
            ["WF-04", "Trương Thái Như", "F-07, F-08", "2 (1 Main / 1 Exc)", "16", "14"],
            ["Total", "4 Members", "8 Features", "8 (4 Main / 4 Exc)", "65", "56 (86.15%)"],
        ],
        bold_last_row=True,
    )

    populate_data_table(
        tables[50],
        [
            ["Trần Hoàng Trung Hiếu", "WF-01", "F-01, F-02", "16", "14", "DS-01a, DS-01b", "Pending"],
            ["Phùng Trung Quốc", "WF-02", "F-03, F-04", "16", "14", "DS-02a, DS-02b", "Pending"],
            ["Trần Tùng Bách", "WF-03", "F-05, F-06", "17", "14", "DS-03a, DS-03b", "Pending"],
            ["Trương Thái Như", "WF-04", "F-07, F-08", "16", "14", "DS-04a, DS-04b", "Pending"],
            ["Total", "4 Workflows", "8 Features", "65", "56 (86.15%)", "8 Scenarios", "—"],
        ],
        bold_last_row=True,
    )

    populate_kv_table(
        tables[51],
        [
            "4 (WF-01..WF-04)",
            "8 (4 Main / 4 Exception)",
            "65",
            "56 (86.15%)",
        ],
    )

    populate_data_table(
        tables[52],
        [
            ["Main workflows", "100% run end-to-end", "100% (4/4 workflows)"],
            ["Demo scenarios", "100% main; ≥ 80% exception", "100% main; 100% exception"],
            ["Test case count", "≥ committed number", "≥ 65 test cases"],
            ["Test pass rate", "≥ 90% overall; 100% main-path tests of mandatory features", "≥ 90% overall; 100% main-path"],
            ["Automation", "≥ 50% run in CI", "≥ 85% (56/65 in CI)"],
            ["Defects", "No open Critical or High defects", "0 Critical / High defects"],
            ["Individual", "Each member demos the workflow they own and meets their delivery commitments", "100% (4/4 members)"],
        ],
    )

    # Section 9: Required Fixes
    populate_data_table(
        tables[53],
        [
            ["FX-01", "Map SDD §2.2 state-transition IDs to F-01..F-08.", "WF-01..04", "Trần Hoàng Trung Hiếu", "12/11/2026"],
            ["FX-02", "Complete staging walkthrough for partner drone approval (WF1-010).", "WF-01", "Trần Hoàng Trung Hiếu", "15/11/2026"],
            ["FX-03", "Complete staging walkthrough for session abort & reschedule (WF2-015).", "WF-02, WF-03", "Phùng Trung Quốc", "15/11/2026"],
            ["FX-04", "Complete staging walkthroughs for PayOS & Vision fallback (WF3-012, 017).", "WF-03, WF-04", "Trần Tùng Bách", "15/11/2026"],
            ["FX-05", "Remove legacy Maintenance references from SRS/SDD (SR-01).", "WF-04", "Trương Thái Như", "12/11/2026"],
        ],
    )

    # Section 11: Confirmation
    populate_data_table(
        tables[54],
        [
            ["Reviewer 1", "", "", ""],
            ["Reviewer 2", "", "", ""],
            ["Supervisor", "Phạm Minh Trí / Đặng Ngọc Minh Đức", "", ""],
            ["Team leader", "Trần Hoàng Trung Hiếu (SE184212)", "", "09/11/2026"],
        ],
    )

    for p in list(body.findall("w:p", NS)):
        colors = [c.attrib.get(w_tag("val")) for c in p.findall(".//w:color", NS)]
        if "666666" in colors:
            body.remove(p)

    save_modified_docx(src_docx, dst_paths, root)


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    downloads = Path(r"C:\Users\trant\Downloads")
    repo_out = (
        Path(__file__).resolve().parent.parent
        / "reports"
        / "generated"
        / "review-2-pack"
    )

    bm01_src = downloads / "SWP490_R2_BM01_Design_Brief_1.docx"
    bm02_src = downloads / "SWP490_R2_BM02_Self_Review_Report_1.docx"
    bm03_src = downloads / "SWP490_R2_BM03_Record_of_Changes_1.docx"
    bm04_src = downloads / "SWP490_R2_BM04_Review2_Commitment_1.docx"

    build_bm01(
        bm01_src,
        [
            bm01_src,
            repo_out / "SWP490_GFA26SE139_R2_DesignBrief.docx",
        ],
    )
    print("Populated concise BM01 ->", bm01_src)

    build_bm02(
        bm02_src,
        [
            bm02_src,
            repo_out / "SWP490_GFA26SE139_R2_SelfReview.docx",
        ],
    )
    print("Populated concise BM02 ->", bm02_src)

    build_bm03(
        bm03_src,
        [
            bm03_src,
            repo_out / "SWP490_GFA26SE139_R2_Record_of_Changes.docx",
        ],
    )
    print("Populated concise BM03 ->", bm03_src)

    build_bm04(
        bm04_src,
        [
            bm04_src,
            repo_out / "SWP490_GFA26SE139_R2_Commitment.docx",
        ],
    )
    print("Populated concise BM04 ->", bm04_src)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
