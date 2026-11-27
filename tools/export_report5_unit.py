#!/usr/bin/env python3
"""Export Report 5 Unit Test workbook following the official SEP490 .xls template."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parent))

from export_common import run_single
from report_ooxml import Spreadsheet, descendants

TEMPLATE_NAME = "Report5_Unit Test.xls"
OUTPUT_NAME = "Report5_Unit Test.xlsx"
TEMPLATE_SHELL = Path(__file__).resolve().parent / "templates" / "Report5_Unit Test.template.xlsx"
DATA_PATH = Path("report-5-unit-test/unit-test-data.json")
SOURCES = [str(DATA_PATH)]
ALLOWED_TESTERS = {
    "Trần Hoàng Trung Hiếu",
    "Phùng Trung Quốc",
    "Trần Tùng Bách",
    "Trương Thái Như",
}


def col_letter(idx: int) -> str:
    out = ""
    while idx > 0:
        idx, rem = divmod(idx - 1, 26)
        out = chr(65 + rem) + out
    return out


def validate_data(data: dict) -> list[str]:
    errors: list[str] = []
    cover = data.get("cover", {})
    for role_key in ("creator", "reviewer_approver"):
        if not str(cover.get(role_key, "")).strip():
            errors.append(f"Missing cover.{role_key}")
    functions = data.get("functions", [])
    if len(functions) != 14:
        errors.append(f"Expected 14 functions, found {len(functions)}")
    seen_sheets: set[str] = set()
    for idx, fn in enumerate(functions, 1):
        if fn.get("no") != idx:
            errors.append(f"Function {idx} has mismatched no={fn.get('no')}")
        sheet = fn.get("sheet_name")
        if sheet != f"Function {idx}":
            errors.append(f"Function {idx} has unexpected sheet_name={sheet!r}")
        if sheet in seen_sheets:
            errors.append(f"Duplicate sheet_name {sheet}")
        seen_sheets.add(str(sheet))
        for field in ("created_by", "executed_by"):
            if fn.get(field) not in ALLOWED_TESTERS:
                errors.append(f"{sheet} {field}={fn.get(field)!r} is not one of the 4 canonical team testers")
        cases = fn.get("cases", [])
        if not cases:
            errors.append(f"{sheet} has no cases")
        for c_idx, case in enumerate(cases, 1):
            if case.get("type") not in {"N", "A", "B"}:
                errors.append(f"{sheet} case {c_idx} invalid type {case.get('type')!r}")
            if case.get("result") not in {"P", "F", "U"}:
                errors.append(f"{sheet} case {c_idx} invalid result {case.get('result')!r}")
    if errors:
        raise ValueError("; ".join(errors))
    return []


def discard_calc_chain(book: Spreadsheet) -> None:
    if "xl/calcChain.xml" in book.package.parts:
        del book.package.parts["xl/calcChain.xml"]
        rels = book.package.xml("xl/_rels/workbook.xml.rels")
        for rel in list(descendants(rels, "Relationship")):
            if rel.getAttribute("Target") == "calcChain.xml":
                rel.parentNode.removeChild(rel)
        book.package.set_xml("xl/_rels/workbook.xml.rels", rels)
    workbook = book.package.xml("xl/workbook.xml")
    for calc in descendants(workbook, "calcPr"):
        calc.setAttribute("fullCalcOnLoad", "1")
        calc.setAttribute("forceFullCalc", "1")
    # Update _xlnm.Print_Area so Statistics prints rows 1..53 (including both Pie Charts)
    # and Function sheets / Functions are never cropped by sample template ranges.
    sheet_names = list(book.sheets.keys())
    stats_sid = str(sheet_names.index("Statistics")) if "Statistics" in sheet_names else None
    fns_sid = str(sheet_names.index("Functions")) if "Functions" in sheet_names else None
    for dn in list(descendants(workbook, "definedName")):
        name = dn.getAttribute("name")
        val = "".join(t.data for t in dn.childNodes if getattr(t, "data", None))
        lsid = dn.getAttribute("localSheetId")
        if "[1]Function3" in val or "#REF!" in val or ".wvu." in name:
            dn.parentNode.removeChild(dn)
        elif name == "_xlnm.Print_Area":
            if lsid == stats_sid:
                for ch in list(dn.childNodes):
                    dn.removeChild(ch)
                dn.appendChild(workbook.createTextNode("Statistics!$A$1:$I$53"))
            elif lsid == fns_sid:
                for ch in list(dn.childNodes):
                    dn.removeChild(ch)
                dn.appendChild(workbook.createTextNode("Functions!$A$1:$H$30"))
            elif lsid not in ("0", "1") and lsid != stats_sid and lsid != fns_sid:
                dn.parentNode.removeChild(dn)
    book.package.set_xml("xl/workbook.xml", workbook)


def strip_sheet_comments(book: Spreadsheet, sheet_name: str) -> None:
    """Remove sticky comments / VML drawings inherited from sample sheets."""
    sheet = book.sheet(sheet_name)
    for node in list(descendants(sheet, "legacyDrawing")):
        node.parentNode.removeChild(node)
    part_path = book.sheets[sheet_name][0]
    rels_path = part_path.replace("xl/worksheets/", "xl/worksheets/_rels/") + ".rels"
    if rels_path in book.package.parts:
        rels = book.package.xml(rels_path)
        removed_any = False
        for rel in list(descendants(rels, "Relationship")):
            rtype = rel.getAttribute("Type")
            if rtype.endswith("/comments") or rtype.endswith("/vmlDrawing"):
                rel.parentNode.removeChild(rel)
                removed_any = True
        if removed_any:
            if not descendants(rels, "Relationship"):
                del book.package.parts[rels_path]
            else:
                book.package.set_xml(rels_path, rels)


def set_row_height(book: Spreadsheet, sheet_name: str, row_no: int, height: float) -> None:
    target = str(row_no)
    for row in descendants(book.sheet(sheet_name), "row"):
        if row.getAttribute("r") == target:
            row.setAttribute("ht", str(height))
            row.setAttribute("customHeight", "1")
            return


def set_fit_to_page(book: Spreadsheet, sheet_name: str, width: int = 1, height: int = 0) -> None:
    """Scale worksheet columns cleanly onto landscape/portrait page width without clipping."""
    sheet = book.sheet(sheet_name)
    root = sheet.documentElement
    ns = root.namespaceURI
    spr_list = [n for n in root.childNodes if getattr(n, "localName", None) == "sheetPr"]
    if spr_list:
        spr = spr_list[0]
    else:
        spr = sheet.createElementNS(ns, "sheetPr")
        root.insertBefore(spr, root.firstChild)
    psp_list = [n for n in spr.childNodes if getattr(n, "localName", None) == "pageSetUpPr"]
    psp = psp_list[0] if psp_list else sheet.createElementNS(ns, "pageSetUpPr")
    if not psp_list:
        spr.appendChild(psp)
    psp.setAttribute("fitToPage", "1")
    for ps in descendants(sheet, "pageSetup"):
        ps.setAttribute("fitToWidth", str(width))
        ps.setAttribute("fitToHeight", str(height))
        if ps.hasAttribute("scale"):
            ps.removeAttribute("scale")


def set_col_widths(book: Spreadsheet, sheet_name: str, widths: dict[int, float]) -> None:
    sheet = book.sheet(sheet_name)
    cols_nodes = [n for n in sheet.documentElement.childNodes if getattr(n, "localName", None) == "cols"]
    if not cols_nodes:
        return
    cols_el = cols_nodes[0]
    doc = sheet
    ns = cols_el.namespaceURI
    new_specs = []
    for node in list(cols_el.childNodes):
        if getattr(node, "localName", None) != "col":
            continue
        cmin = int(node.getAttribute("min"))
        cmax = int(node.getAttribute("max"))
        attrs = {node.attributes.item(i).name: node.attributes.item(i).value for i in range(node.attributes.length)}
        cuts = sorted(c for c in widths if cmin <= c <= cmax)
        if not cuts:
            new_specs.append(attrs)
        else:
            cur = cmin
            for c in cuts:
                if cur < c:
                    new_specs.append(dict(attrs, min=str(cur), max=str(c - 1)))
                new_specs.append(dict(attrs, min=str(c), max=str(c), width=str(widths[c]), customWidth="1"))
                cur = c + 1
            if cur <= cmax:
                new_specs.append(dict(attrs, min=str(cur), max=str(cmax)))
        cols_el.removeChild(node)
    for spec in new_specs:
        el = doc.createElementNS(ns, "col")
        for k, v in spec.items():
            el.setAttribute(k, v)
        cols_el.appendChild(el)


def ensure_cols_up_to(book: Spreadsheet, sheet_name: str, max_col: int, width: float = 4.2) -> None:
    """Ensure UTCID matrix columns F..max_col exist with compact uniform width."""
    sheet = book.sheet(sheet_name)
    cols_nodes = [n for n in sheet.documentElement.childNodes if getattr(n, "localName", None) == "cols"]
    if not cols_nodes:
        return
    cols_el = cols_nodes[0]
    doc = sheet
    ns = cols_el.namespaceURI
    widths = {col_idx: width for col_idx in range(6, max_col + 1)}
    set_col_widths(book, sheet_name, widths)
    # Check highest defined column in <cols>; extend if < max_col
    highest = 0
    for node in descendants(cols_el, "col"):
        highest = max(highest, int(node.getAttribute("max")))
    if highest < max_col:
        el = doc.createElementNS(ns, "col")
        el.setAttribute("min", str(highest + 1))
        el.setAttribute("max", str(max_col))
        el.setAttribute("width", str(width))
        el.setAttribute("customWidth", "1")
        cols_el.appendChild(el)


def extend_top_merges(book: Spreadsheet, sheet_name: str, right_col_idx: int) -> None:
    """Extend Function N header/counter merges from col T to right_col_idx when cases > 15."""
    if right_col_idx <= 20:
        return
    right_letter = col_letter(right_col_idx)
    sheet = book.sheet(sheet_name)
    for mc in descendants(sheet, "mergeCell"):
        ref = mc.getAttribute("ref")
        if ":T" in ref:
            mc.setAttribute("ref", re.sub(r":T(\d+)$", f":{right_letter}\\1", ref))


def ensure_cell_with_style(book: Spreadsheet, sheet_name: str, coord: str, template_coord: str) -> None:
    """Create cell if missing and copy style attribute from template_coord."""
    c = book.cell(sheet_name, coord)
    src = book.cell(sheet_name, template_coord)
    if src.hasAttribute("s"):
        c.setAttribute("s", src.getAttribute("s"))


def populate_cover(book: Spreadsheet, cover: dict) -> None:
    set_fit_to_page(book, "Cover", width=1, height=1)
    set_col_widths(book, "Cover", {3: 22, 5: 46, 6: 56})
    book.put("Cover", "B4", cover["project_name"])
    book.put("Cover", "B5", cover["project_code"])
    book.put("Cover", "B6", cover["document_code"], 'B5&"_Unit Test_v"&F6')
    book.cell("Cover", "B6").setAttribute("t", "str")
    book.put("Cover", "F4", cover["creator"])
    book.put("Cover", "F5", cover["issue_date"])
    book.put("Cover", "F6", cover["version"])

    changelog = cover.get("changelog", [])
    for idx in range(7):
        row_no = 11 + idx
        if idx < len(changelog):
            entry = changelog[idx]
            vals = [entry["date"], entry["version"], entry["item"], entry["action"], entry["description"], entry["reference"]]
            for col_i, val in enumerate(vals, 1):
                book.put("Cover", f"{col_letter(col_i)}{row_no}", val)
                if col_i in (3, 5, 6):
                    book.cell("Cover", f"{col_letter(col_i)}{row_no}").setAttribute("s", "163")
            book.fit_height("Cover", row_no, vals, [18, 9, 20, 7, 44, 52])
        else:
            for col_i in range(1, 7):
                book.put("Cover", f"{col_letter(col_i)}{row_no}", "")


def populate_functions(book: Spreadsheet, data: dict) -> None:
    set_fit_to_page(book, "Functions", width=1, height=0)
    cover = data["cover"]
    env_text = "\n".join(f"{i}. {line}" for i, line in enumerate(cover.get("environment", []), 1))
    book.put("Functions", "E4", cover["project_name"], "Cover!B4")
    book.cell("Functions", "E4").setAttribute("t", "str")
    book.put("Functions", "E5", cover["project_code"], "Cover!B5")
    book.cell("Functions", "E5").setAttribute("t", "str")
    book.put("Functions", "E6", int(cover.get("normal_tcs_per_kloc", 15)))
    book.put("Functions", "E7", env_text)
    book.cell("Functions", "E7").setAttribute("s", "53")
    book.fit_height("Functions", 7, [env_text], [95])

    set_col_widths(book, "Functions", {1: 5, 2: 26, 3: 32, 4: 34, 5: 13, 6: 12, 7: 42, 8: 34})

    proto = book.row_template("Functions", 11)
    book.clear_rows("Functions", 11)
    for idx, fn in enumerate(data["functions"]):
        r_no = 11 + idx
        sheet = fn["sheet_name"]
        book.clone_row("Functions", r_no, proto)
        vals = [
            fn["no"],
            fn["requirement_name"],
            fn["class_name"],
            fn["function_name"],
            fn["code"],
            sheet,
            fn["description"],
            fn["precondition"],
        ]
        for col_i, val in enumerate(vals, 1):
            coord = f"{col_letter(col_i)}{r_no}"
            if col_i == 6:
                book.put("Functions", coord, sheet, f'HYPERLINK("#\'{sheet}\'!A1","{sheet}")')
                book.cell("Functions", coord).setAttribute("t", "str")
                book.cell("Functions", coord).setAttribute("s", "54")
            else:
                book.put("Functions", coord, val)
                if col_i in (2, 3, 4, 5, 7, 8):
                    book.cell("Functions", coord).setAttribute("s", "53")
        book.fit_height("Functions", r_no, [str(v) for v in vals], [5, 24, 29, 24, 11, 11, 38, 31])
    book.dimensions("Functions", "H", 10 + len(data["functions"]))


def populate_statistics(book: Spreadsheet, data: dict) -> dict:
    set_fit_to_page(book, "Statistics", width=1, height=1)
    cover = data["cover"]
    book.put("Statistics", "B4", cover["project_name"], "Cover!B4")
    book.cell("Statistics", "B4").setAttribute("t", "str")
    book.put("Statistics", "B5", cover["project_code"], "Cover!B5")
    book.cell("Statistics", "B5").setAttribute("t", "str")
    book.put("Statistics", "B6", cover["document_code"], 'B5&"_Unit Test_v"&Cover!F6')
    book.cell("Statistics", "B6").setAttribute("t", "str")
    book.put("Statistics", "B7", cover["notes"])
    book.cell("Statistics", "B7").setAttribute("s", "41")
    book.fit_height("Statistics", 7, [cover["notes"]], [85])
    book.put("Statistics", "F4", cover["creator"])
    book.put("Statistics", "F5", cover["reviewer_approver"])
    book.put("Statistics", "F6", cover["issue_date"])

    set_col_widths(book, "Statistics", {1: 16, 2: 26, 3: 11, 4: 10, 5: 11, 6: 8, 7: 8, 8: 8, 9: 18, 10: 9})

    proto_mod = book.row_template("Statistics", 12)
    proto_sub = book.row_template("Statistics", 17)
    proto_spc = book.row_template("Statistics", 18)
    proto_pct1 = book.row_template("Statistics", 19)
    proto_pct2 = book.row_template("Statistics", 21)
    book.clear_rows("Statistics", 12)

    first_row = 12
    tot = {"P": 0, "F": 0, "U": 0, "N": 0, "A": 0, "B": 0, "total": 0}
    for offset, fn in enumerate(data["functions"]):
        r_no = first_row + offset
        sheet = fn["sheet_name"]
        cases = fn["cases"]
        p = sum(1 for c in cases if c["result"] == "P")
        f = sum(1 for c in cases if c["result"] == "F")
        u = sum(1 for c in cases if c["result"] == "U")
        n = sum(1 for c in cases if c["type"] == "N")
        a = sum(1 for c in cases if c["type"] == "A")
        b = sum(1 for c in cases if c["type"] == "B")
        total = len(cases)
        for k, v in (("P", p), ("F", f), ("U", u), ("N", n), ("A", a), ("B", b), ("total", total)):
            tot[k] += v

        book.clone_row("Statistics", r_no, proto_mod)
        book.put("Statistics", f"A{r_no}", fn["no"])
        book.put("Statistics", f"B{r_no}", f"{fn['code']} ({sheet})", f'HYPERLINK("#\'{sheet}\'!A1","{sheet}")')
        book.cell("Statistics", f"B{r_no}").setAttribute("t", "str")
        book.put("Statistics", f"C{r_no}", p, f"'{sheet}'!A7")
        book.put("Statistics", f"D{r_no}", f, f"'{sheet}'!C7")
        book.put("Statistics", f"E{r_no}", u, f"'{sheet}'!F7")
        book.put("Statistics", f"F{r_no}", n, f"'{sheet}'!L7")
        book.put("Statistics", f"G{r_no}", a, f"'{sheet}'!M7")
        book.put("Statistics", f"H{r_no}", b, f"'{sheet}'!N7")
        book.put("Statistics", f"I{r_no}", total, f"'{sheet}'!O7")

    last_row = first_row + len(data["functions"]) - 1
    sub_row = last_row + 2  # row 27 for 14 functions
    book.clone_row("Statistics", sub_row - 1, proto_spc)
    book.clone_row("Statistics", sub_row, proto_sub)
    book.put("Statistics", f"B{sub_row}", "Sub total")
    for col_l, val in zip("CDEFGHI", (tot["P"], tot["F"], tot["U"], tot["N"], tot["A"], tot["B"], tot["total"])):
        book.put("Statistics", f"{col_l}{sub_row}", val, f"SUM({col_l}{first_row}:{col_l}{last_row})")

    book.clone_row("Statistics", sub_row + 1, proto_spc)
    metrics = [
        ("Test coverage", round((tot["P"] + tot["F"]) * 100.0 / tot["total"], 2), f"(C{sub_row}+D{sub_row})*100/I{sub_row}", proto_pct1),
        ("Test successful coverage", round(tot["P"] * 100.0 / tot["total"], 2), f"C{sub_row}*100/I{sub_row}", proto_pct1),
        ("Normal case", round(tot["N"] * 100.0 / tot["total"], 2), f"F{sub_row}*100/I{sub_row}", proto_pct2),
        ("Abnormal case", round(tot["A"] * 100.0 / tot["total"], 2), f"G{sub_row}*100/I{sub_row}", proto_pct2),
        ("Boundary case", round(tot["B"] * 100.0 / tot["total"], 2), f"H{sub_row}*100/I{sub_row}", proto_pct2),
    ]
    for offset, (label, val, formula, proto_row) in enumerate(metrics, sub_row + 2):
        book.clone_row("Statistics", offset, proto_row)
        book.put("Statistics", f"B{offset}", label)
        book.put("Statistics", f"D{offset}", val, formula)
        book.put("Statistics", f"E{offset}", "%")
    book.dimensions("Statistics", "I", sub_row + 6)

    # Shift the two Pie Chart anchors below row 33 so they never overlap rows 24..33
    drawing_path = "xl/drawings/drawing2.xml"
    if drawing_path in book.package.parts:
        txt = book.package.parts[drawing_path].decode("utf-8")
        txt = txt.replace("<xdr:row>24</xdr:row>", "<xdr:row>35</xdr:row>")
        txt = txt.replace("<xdr:row>39</xdr:row>", "<xdr:row>51</xdr:row>")
        book.package.parts[drawing_path] = txt.encode("utf-8")

    # Point Pie Charts at sub_row (27) and strip template #REF! caches
    for chart_path, old_ref, new_ref, new_vals in (
        ("xl/charts/chart2.xml", "Statistics!$C$17:$E$17", f"Statistics!$C${sub_row}:$E${sub_row}", (tot["P"], tot["F"], tot["U"])),
        ("xl/charts/chart1.xml", "Statistics!$F$17:$H$17", f"Statistics!$F${sub_row}:$H${sub_row}", (tot["N"], tot["A"], tot["B"])),
    ):
        if chart_path in book.package.parts:
            ctxt = book.package.parts[chart_path].decode("utf-8")
            ctxt = ctxt.replace(old_ref, new_ref)
            ctxt = ctxt.replace("Statistics!$C$16:$E$16", f"Statistics!$C${sub_row - 1}:$E${sub_row - 1}")
            ctxt = ctxt.replace("Statistics!$F$16:$H$16", f"Statistics!$F${sub_row - 1}:$H${sub_row - 1}")
            ctxt = ctxt.replace("Statistics!#REF!", new_ref)
            ctxt = ctxt.replace('<c:numFmt formatCode="0%" sourceLinked="0"/>', '<c:numFmt formatCode="0%;;&quot;&quot;" sourceLinked="0"/>')
            ctxt = ctxt.replace('<c:showCatName val="1"/>', '<c:showCatName val="0"/>')
            # Refresh the cached pt idx=0..2 numbers cleanly
            for idx_v, num_v in enumerate(new_vals):
                ctxt = re.sub(
                    rf'(<c:pt idx="{idx_v}"><c:v>)\d+(?:\.\d+)?(</c:v></c:pt>)',
                    rf"\g<1>{num_v}\g<2>",
                    ctxt,
                )
            book.package.parts[chart_path] = ctxt.encode("utf-8")
    return tot


def populate_function_sheet(book: Spreadsheet, fn: dict, kloc_target: int) -> None:
    sheet = fn["sheet_name"]
    set_fit_to_page(book, sheet, width=1, height=0)
    r_fn = 10 + fn["no"]
    cases = fn["cases"]
    n_cases = len(cases)
    end_col_idx = 5 + n_cases  # F is col 6
    end_letter = col_letter(end_col_idx)
    right_col_idx = max(end_col_idx, 20)

    ensure_cols_up_to(book, sheet, right_col_idx, width=4.8)
    set_col_widths(book, sheet, {1: 7.5, 2: 13.0, 3: 10.5, 4: 48.0, 5: 1.8})
    extend_top_merges(book, sheet, right_col_idx)

    p = sum(1 for c in cases if c["result"] == "P")
    f = sum(1 for c in cases if c["result"] == "F")
    u = sum(1 for c in cases if c["result"] == "U")
    n = sum(1 for c in cases if c["type"] == "N")
    a = sum(1 for c in cases if c["type"] == "A")
    b = sum(1 for c in cases if c["type"] == "B")
    lack = max(0, round(fn["loc"] * kloc_target / 1000.0 - n_cases))

    book.put(sheet, "C2", fn["code"], f"Functions!E{r_fn}")
    book.cell(sheet, "C2").setAttribute("t", "str")
    book.put(sheet, "L2", fn["function_name"], f"Functions!D{r_fn}")
    book.cell(sheet, "L2").setAttribute("t", "str")
    book.put(sheet, "C3", fn["created_by"])
    book.put(sheet, "L3", fn["executed_by"])
    book.put(sheet, "C4", fn["loc"])
    book.put(sheet, "L4", lack, f'IF(Functions!$E$6<>"N/A",MAX(0,ROUND(C4*Functions!$E$6/1000-O7,0)),"N/A")')
    book.put(sheet, "C5", fn["description"])
    set_row_height(book, sheet, 5, 24)

    book.put(sheet, "A7", p, f'COUNTIF(F40:{end_letter}40,"P")')
    book.put(sheet, "C7", f, f'COUNTIF(F40:{end_letter}40,"F")')
    book.put(sheet, "F7", u, f"SUM(O7,-A7,-C7)")
    book.put(sheet, "L7", n, f'COUNTIF(F39:{end_letter}39,"N")')
    book.put(sheet, "M7", a, f'COUNTIF(F39:{end_letter}39,"A")')
    book.put(sheet, "N7", b, f'COUNTIF(F39:{end_letter}39,"B")')
    book.put(sheet, "O7", n_cases, f"COUNTA(F9:{end_letter}9)")

    # Clear dummy cells across rows 9..42 cols D..end_max cleanly
    sheet_el = book.sheet(sheet)
    for r_no in range(9, 43):
        for col_i in range(4, 24):
            c_ref = f"{col_letter(col_i)}{r_no}"
            if r_no == 9 or col_i >= 6:
                book.put(sheet, c_ref, "")
            elif r_no in range(10, 39):
                book.put(sheet, c_ref, "")
        # Clear any hardcoded label in B14..B30 except structural headings
        if r_no in (14, 18, 22, 26):
            book.put(sheet, f"B{r_no}", "")

    # Populate Precondition & grouped Decision-Table Conditions matching official layout
    book.put(sheet, "D11", fn["precondition"])
    book.cell(sheet, "D11").setAttribute("s", "382")
    book.fit_height(sheet, 11, [fn["precondition"]], [45])
    book.put(sheet, "B14", "Test Scope & Scenario")
    book.put(sheet, "D15", "Happy path / valid workflow")
    book.put(sheet, "D16", "Invalid / rejected input")
    book.put(sheet, "D17", "Boundary / state transition")

    book.put(sheet, "B18", "JUnit 5 Suites")
    suites = fn.get("source_tests", [])
    for idx_s, s_name in enumerate(suites[:3]):
        book.put(sheet, f"D{19 + idx_s}", s_name)

    # Confirm block (rows 31..38)
    book.put(sheet, "D32", "Expected output asserted")
    book.put(sheet, "D33", "Fallback / edge state asserted")
    book.put(sheet, "D35", "Guard / exception raised")
    book.put(sheet, "D37", "Verified pass in JUnit 5")
    book.put(sheet, "D38", "Error path verified in JUnit 5")

    # Populate UTCID columns F..{end}
    exec_short = fn["executed_date"][8:10] + "/" + fn["executed_date"][5:7]
    for idx, case in enumerate(cases):
        col_i = 6 + idx
        cl = col_letter(col_i)
        # Clone styles from col F (if col > T) cleanly for every matrix row 9..42
        if col_i > 20:
            for r_no in range(9, 43):
                ensure_cell_with_style(book, sheet, f"{cl}{r_no}", f"F{r_no}")

        book.put(sheet, f"{cl}9", f"UTCID{idx + 1:02d}")
        book.put(sheet, f"{cl}11", "O")

        ctype = case["type"]
        if ctype == "N":
            book.put(sheet, f"{cl}15", "O")
            book.put(sheet, f"{cl}32", "O")
            book.put(sheet, f"{cl}37", "O")
        elif ctype == "B":
            book.put(sheet, f"{cl}17", "O")
            book.put(sheet, f"{cl}33", "O")
            book.put(sheet, f"{cl}37", "O")
        else:
            book.put(sheet, f"{cl}16", "O")
            book.put(sheet, f"{cl}35", "O")
            book.put(sheet, f"{cl}38", "O")

        # Mark corresponding JUnit suite row (row 19..21)
        suite_offset = idx % max(1, min(3, len(suites)))
        book.put(sheet, f"{cl}{19 + suite_offset}", "O")

        book.put(sheet, f"{cl}39", ctype)
        book.put(sheet, f"{cl}40", case["result"])
        book.put(sheet, f"{cl}41", exec_short)
        book.cell(sheet, f"{cl}41").setAttribute("s", "118")
        book.put(sheet, f"{cl}42", "")

    set_row_height(book, sheet, 41, 18)
    set_row_height(book, sheet, 42, 18)
    book.dimensions(sheet, col_letter(right_col_idx), 42)
    del sheet_el  # unused reference


def export(template: Path, reports_root: Path, output_path: Path) -> dict:
    """Generate Report5_Unit Test.xlsx preserving official SEP490 .xls template styles & charts."""
    shell = template if template.suffix.lower() == ".xlsx" else TEMPLATE_SHELL
    source_path = reports_root / DATA_PATH
    data = json.loads(source_path.read_text(encoding="utf-8"))
    warnings = validate_data(data)

    book = Spreadsheet(shell)
    for clean_target in ("Function 1", "Function 2"):
        strip_sheet_comments(book, clean_target)

    for to_drop in ("Function3", "Example"):
        if to_drop in book.sheets:
            book.remove_sheet(to_drop)

    for n in range(3, 15):
        book.duplicate_sheet("Function 2", f"Function {n}")

    kloc_target = int(data["cover"].get("normal_tcs_per_kloc", 15))
    populate_cover(book, data["cover"])
    populate_functions(book, data)
    populate_statistics(book, data)
    for fn in data["functions"]:
        populate_function_sheet(book, fn, kloc_target)

    discard_calc_chain(book)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    allowed_extra = {
        "xl/workbook.xml",
        "xl/calcChain.xml",
        "xl/_rels/workbook.xml.rels",
        "xl/charts/chart1.xml",
        "xl/charts/chart2.xml",
        "xl/drawings/drawing2.xml",
        "xl/worksheets/_rels/sheet5.xml.rels",
        "xl/worksheets/_rels/sheet6.xml.rels",
    }
    audit = book.save(output_path, allowed_extra)
    total_cases = sum(len(fn["cases"]) for fn in data["functions"])
    return {
        **audit,
        "warnings": warnings,
        "functions": len(data["functions"]),
        "cases": total_cases,
    }


if __name__ == "__main__":
    raise SystemExit(run_single("report5-unit", TEMPLATE_NAME, SOURCES, export, output_name=OUTPUT_NAME))
