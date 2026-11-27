#!/usr/bin/env python3
"""Export Report 5 Unit Test workbook from structured JSON backed by JUnit tests."""
from __future__ import annotations

import json
import sys
import zipfile
from pathlib import Path
from xml.sax.saxutils import escape

from export_common import run_single

TEMPLATE_NAME = "Report5_Unit Test.xls"
OUTPUT_NAME = "Report5_Unit Test.xlsx"
DATA_PATH = Path("report-5-unit-test/unit-test-data.json")
SOURCES = [str(DATA_PATH)]
ALLOWED_TESTERS = {
    "Trần Hoàng Trung Hiếu",
    "Phùng Trung Quốc",
    "Trần Tùng Bách",
    "Trương Thái Như",
}

# Predefined style indexes in _STYLES_XML below:
S_DEFAULT = 0       # Tahoma 10 black
S_TITLE = 1         # Tahoma 18 bold center
S_LABEL = 2         # Tahoma 10 bold, band fill, border, left
S_TEXT = 3          # Tahoma 10, white fill, border, left wrap
S_CENTER = 4        # Tahoma 10, white fill, border, center wrap
S_HEADER_NAVY = 5   # Tahoma 10 bold white on #000080, border, center
S_HEADER_SLATE = 6  # Tahoma 10 bold white on #333399, border, center
S_LINK = 7          # Tahoma 10 blue underline, white fill, border, center
S_LINK_LEFT = 8     # Tahoma 10 blue underline, white fill, border, left
S_SUBTOTAL = 9      # Tahoma 10 bold black on #D9E1F2, border, center
S_SUBTOTAL_L = 10   # Tahoma 10 bold black on #D9E1F2, border, left
S_PCT = 11          # Tahoma 10 bold black, border, right, 0.00
S_SM_LABEL = 12     # Tahoma 9 bold black, band fill, border, left wrap
S_SM_BAND_C = 13    # Tahoma 9 bold black, band fill, border, center wrap
S_SM_TEXT = 14      # Tahoma 9 black, white fill, border, left wrap
S_SM_CENTER = 15    # Tahoma 9 black, white fill, border, center wrap
S_SM_HDR_NAVY = 16  # Tahoma 9 bold white on #000080, border, center
S_SM_HDR_SLATE = 17 # Tahoma 9 bold white on #333399, border, center
S_PASS = 18         # Tahoma 9 bold black on #E2EFDA, border, center
S_FAIL = 19         # Tahoma 9 bold black on #FCE4D6, border, center
S_BOLD_C = 20       # Tahoma 10 bold black, white fill, border, center


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


class SheetBuilder:
    def __init__(self, title: str):
        self.title = title
        self.cells: dict[tuple[int, int], tuple[object, int, str | None]] = {}
        self.merges: list[str] = []
        self.col_widths: dict[int, float] = {}
        self.row_heights: dict[int, float] = {}

    def put(self, row: int, col: int, value: object = None, style: int = S_TEXT, formula: str | None = None) -> None:
        self.cells[(row, col)] = (value, style, formula)

    def put_range_empty(self, r1: int, c1: int, r2: int, c2: int, style: int) -> None:
        for r in range(r1, r2 + 1):
            for c in range(c1, c2 + 1):
                if (r, c) not in self.cells:
                    self.cells[(r, c)] = (None, style, None)

    def merge(self, r1: int, c1: int, r2: int, c2: int, style: int | None = None) -> None:
        self.merges.append(f"{col_letter(c1)}{r1}:{col_letter(c2)}{r2}")
        if style is not None:
            self.put_range_empty(r1, c1, r2, c2, style)

    def to_xml(self) -> str:
        cols_xml = ""
        if self.col_widths:
            col_tags = "".join(
                f'<col min="{c}" max="{c}" width="{w}" customWidth="1"/>'
                for c, w in sorted(self.col_widths.items())
            )
            cols_xml = f"<cols>{col_tags}</cols>"

        rows_by_no: dict[int, list[int]] = {}
        for r, c in self.cells:
            rows_by_no.setdefault(r, []).append(c)

        row_parts: list[str] = []
        for r in sorted(rows_by_no):
            ht = f' ht="{self.row_heights[r]}" customHeight="1"' if r in self.row_heights else ""
            c_parts: list[str] = []
            for c in sorted(rows_by_no[r]):
                val, style, formula = self.cells[(r, c)]
                ref = f"{col_letter(c)}{r}"
                if formula is not None:
                    f_xml = f"<f>{escape(formula)}</f>"
                    if isinstance(val, (int, float)) and not isinstance(val, bool):
                        c_parts.append(f'<c r="{ref}" s="{style}">{f_xml}<v>{val}</v></c>')
                    elif val is not None:
                        c_parts.append(f'<c r="{ref}" t="str" s="{style}">{f_xml}<v>{escape(str(val))}</v></c>')
                    else:
                        c_parts.append(f'<c r="{ref}" s="{style}">{f_xml}</c>')
                elif val is None:
                    c_parts.append(f'<c r="{ref}" s="{style}"/>')
                elif isinstance(val, (int, float)) and not isinstance(val, bool):
                    c_parts.append(f'<c r="{ref}" s="{style}"><v>{val}</v></c>')
                else:
                    s_val = escape(str(val))
                    c_parts.append(f'<c r="{ref}" t="inlineStr" s="{style}"><is><t xml:space="preserve">{s_val}</t></is></c>')
            row_parts.append(f'<row r="{r}"{ht}>{"".join(c_parts)}</row>')

        merges_xml = ""
        if self.merges:
            m_tags = "".join(f'<mergeCell ref="{m}"/>' for m in self.merges)
            merges_xml = f'<mergeCells count="{len(self.merges)}">{m_tags}</mergeCells>'

        return (
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"'
            ' xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
            '<sheetViews><sheetView workbookViewId="0"/></sheetViews>'
            '<sheetFormatPr defaultRowHeight="18"/>'
            f"{cols_xml}<sheetData>{''.join(row_parts)}</sheetData>{merges_xml}"
            "</worksheet>"
        )


def build_cover(data: dict) -> SheetBuilder:
    ws = SheetBuilder("Cover")
    cover = data["cover"]
    ws.put(2, 2, "UNIT TEST DOCUMENT", S_TITLE)
    ws.merge(2, 2, 2, 6)
    ws.row_heights[2] = 34

    meta_rows = [
        (4, "Project Name", cover["project_name"], None, "Creator", cover["creator"]),
        (5, "Project Code", cover["project_code"], None, "Reviewer/Approver", cover["reviewer_approver"]),
        (6, "Document Code", cover["document_code"], 'B5&"_Unit Test_v"&F7', "Issue Date", cover["issue_date"]),
        (7, "Notes", cover["notes"], None, "Version", cover["version"]),
    ]
    for r, l1, v1, f1, l2, v2 in meta_rows:
        ws.put(r, 1, l1, S_LABEL)
        ws.put(r, 2, v1, S_TEXT, f1)
        ws.merge(r, 2, r, 4, S_TEXT)
        ws.put(r, 5, l2, S_LABEL)
        ws.put(r, 6, v2, S_TEXT)
        ws.row_heights[r] = 42 if r == 7 else 22

    ws.put(9, 1, "Record of change", S_DEFAULT)
    headers = ["Effective Date", "Version", "Change Item", "*A,D,M", "Change description", "Reference"]
    for idx, label in enumerate(headers, 1):
        ws.put(10, idx, label, S_HEADER_NAVY)
    ws.row_heights[10] = 24

    changelog = cover.get("changelog", [])
    for idx in range(5):
        row_no = 11 + idx
        if idx < len(changelog):
            entry = changelog[idx]
            vals = [entry["date"], entry["version"], entry["item"], entry["action"], entry["description"], entry["reference"]]
        else:
            vals = ["", "", "", "", "", ""]
        for col, val in enumerate(vals, 1):
            ws.put(row_no, col, val, S_CENTER if col in (1, 2, 4) else S_TEXT)
        ws.row_heights[row_no] = 36 if idx < len(changelog) else 20

    for col, w in enumerate([18, 18, 22, 12, 48, 26], 1):
        ws.col_widths[col] = w
    return ws


def build_functions(data: dict) -> SheetBuilder:
    ws = SheetBuilder("Functions")
    cover = data["cover"]
    ws.put(2, 1, "Function List", S_TITLE)
    ws.merge(2, 1, 2, 8)
    ws.row_heights[2] = 32

    env_text = "\n".join(f"{i}. {line}" for i, line in enumerate(cover.get("environment", []), 1))
    info_rows = [
        (4, "Project Name", cover["project_name"], "Cover!B4", 22),
        (5, "Project Code", cover["project_code"], "Cover!B5", 22),
        (6, "Normal number of Test cases/KLOC", cover.get("normal_tcs_per_kloc", 15), None, 22),
        (7, "Test Environment Setup Description", env_text, None, 54),
    ]
    for r, label, val, formula, height in info_rows:
        ws.put(r, 1, label, S_LABEL)
        ws.merge(r, 1, r, 4, S_LABEL)
        ws.put(r, 5, val, S_TEXT, formula)
        ws.merge(r, 5, r, 8, S_TEXT)
        ws.row_heights[r] = height

    headers = ["No", "Requirement Name", "Class Name", "Function Name", "Function Code", "Sheet Name", "Description", "Pre-Condition"]
    for col, title in enumerate(headers, 1):
        ws.put(10, col, title, S_HEADER_SLATE)
    ws.row_heights[10] = 26

    for r_idx, fn in enumerate(data["functions"], 11):
        sheet = fn["sheet_name"]
        ws.put(r_idx, 1, fn["no"], S_CENTER)
        ws.put(r_idx, 2, fn["requirement_name"], S_TEXT)
        ws.put(r_idx, 3, fn["class_name"], S_TEXT)
        ws.put(r_idx, 4, fn["function_name"], S_TEXT)
        ws.put(r_idx, 5, fn["code"], S_CENTER)
        ws.put(r_idx, 6, sheet, S_LINK, f'HYPERLINK("#\'{sheet}\'!A1","{sheet}")')
        ws.put(r_idx, 7, fn["description"], S_TEXT)
        ws.put(r_idx, 8, fn["precondition"], S_TEXT)
        ws.row_heights[r_idx] = 40

    for col, w in enumerate([6, 30, 34, 30, 14, 14, 42, 34], 1):
        ws.col_widths[col] = w
    return ws


def build_statistics(data: dict) -> SheetBuilder:
    ws = SheetBuilder("Statistics")
    cover = data["cover"]
    ws.put(2, 2, "UNIT TEST REPORT", S_TITLE)
    ws.merge(2, 2, 2, 10)
    ws.row_heights[2] = 32

    meta = [
        (4, "Project Name", cover["project_name"], "Cover!B4", "Creator", cover["creator"]),
        (5, "Project Code", cover["project_code"], "Cover!B5", "Reviewer/Approver", cover["reviewer_approver"]),
        (6, "Document Code", cover["document_code"], 'C5&"_Unit Test_v"&Cover!F7', "Issue Date", cover["issue_date"]),
    ]
    for r, l1, v1, f1, l2, v2 in meta:
        ws.put(r, 2, l1, S_LABEL)
        ws.put(r, 3, v1, S_TEXT, f1)
        ws.merge(r, 3, r, 4, S_TEXT)
        ws.put(r, 5, l2, S_LABEL)
        ws.merge(r, 5, r, 6, S_LABEL)
        ws.put(r, 7, v2, S_TEXT)
        ws.merge(r, 7, r, 10, S_TEXT)
        ws.row_heights[r] = 22

    ws.put(7, 2, "Notes", S_LABEL)
    ws.put(7, 3, cover["notes"], S_TEXT)
    ws.merge(7, 3, 7, 10, S_TEXT)
    ws.row_heights[7] = 38

    headers = ["No", "Function code", "Passed", "Failed", "Untested", "N", "A", "B", "Total Test Cases"]
    for col, title in enumerate(headers, 2):
        ws.put(11, col, title, S_HEADER_NAVY)
    ws.row_heights[11] = 24

    first_row = 12
    tot = {"P": 0, "F": 0, "U": 0, "N": 0, "A": 0, "B": 0, "total": 0}
    for offset, fn in enumerate(data["functions"]):
        r = first_row + offset
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

        ws.put(r, 2, fn["no"], S_CENTER)
        ws.put(r, 3, sheet, S_LINK_LEFT, f'HYPERLINK("#\'{sheet}\'!A1","{sheet}")')
        ws.put(r, 4, p, S_CENTER, f"'{sheet}'!A7")
        ws.put(r, 5, f, S_CENTER, f"'{sheet}'!C7")
        ws.put(r, 6, u, S_CENTER, f"'{sheet}'!F7")
        ws.put(r, 7, n, S_CENTER, f"'{sheet}'!L7")
        ws.put(r, 8, a, S_CENTER, f"'{sheet}'!M7")
        ws.put(r, 9, b, S_CENTER, f"'{sheet}'!N7")
        ws.put(r, 10, total, S_CENTER, f"'{sheet}'!O7")
        ws.row_heights[r] = 20

    last_row = first_row + len(data["functions"]) - 1
    sub_row = last_row + 2
    ws.put(sub_row, 2, "", S_SUBTOTAL)
    ws.put(sub_row, 3, "Sub total", S_SUBTOTAL_L)
    for col_idx, val in zip(range(4, 11), (tot["P"], tot["F"], tot["U"], tot["N"], tot["A"], tot["B"], tot["total"])):
        cl = col_letter(col_idx)
        ws.put(sub_row, col_idx, val, S_SUBTOTAL, f"SUM({cl}{first_row}:{cl}{last_row})")
    ws.row_heights[sub_row] = 22

    metrics = [
        ("Test coverage", round((tot["P"] + tot["F"]) * 100.0 / tot["total"], 2), f"=(D{sub_row}+E{sub_row})*100/J{sub_row}".lstrip("=")),
        ("Test successful coverage", round(tot["P"] * 100.0 / tot["total"], 2), f"D{sub_row}*100/J{sub_row}"),
        ("Normal case", round(tot["N"] * 100.0 / tot["total"], 2), f"G{sub_row}*100/J{sub_row}"),
        ("Abnormal case", round(tot["A"] * 100.0 / tot["total"], 2), f"H{sub_row}*100/J{sub_row}"),
        ("Boundary case", round(tot["B"] * 100.0 / tot["total"], 2), f"I{sub_row}*100/J{sub_row}"),
    ]
    for offset, (label, val, formula) in enumerate(metrics, sub_row + 2):
        ws.put(offset, 3, label, S_LABEL)
        ws.merge(offset, 3, offset, 4, S_LABEL)
        ws.put(offset, 5, val, S_PCT, formula)
        ws.put(offset, 6, "%", S_CENTER)
        ws.row_heights[offset] = 20

    for col, w in enumerate([4, 14, 18, 12, 12, 12, 10, 10, 10, 18], 1):
        ws.col_widths[col] = w
    return ws


def build_function_sheet(fn: dict, kloc_target: int) -> SheetBuilder:
    ws = SheetBuilder(fn["sheet_name"])
    r_fn = 10 + fn["no"]
    cases = fn["cases"]
    start_col = 6  # F
    end_col = start_col + len(cases) - 1
    end_letter = col_letter(end_col)
    right_span = max(end_col, 15)

    p = sum(1 for c in cases if c["result"] == "P")
    f = sum(1 for c in cases if c["result"] == "F")
    u = sum(1 for c in cases if c["result"] == "U")
    n = sum(1 for c in cases if c["type"] == "N")
    a = sum(1 for c in cases if c["type"] == "A")
    b = sum(1 for c in cases if c["type"] == "B")
    total = len(cases)
    lack = max(0, round(fn["loc"] * kloc_target / 1000.0 - total))

    ws.put(2, 1, "Function Code", S_SM_LABEL)
    ws.put(2, 3, fn["code"], S_SM_TEXT, f"Functions!E{r_fn}")
    ws.put(2, 6, "Function Name", S_SM_LABEL)
    ws.put(2, 12, fn["function_name"], S_SM_TEXT, f"Functions!D{r_fn}")

    ws.put(3, 1, "Created By", S_SM_LABEL)
    ws.put(3, 3, fn["created_by"], S_SM_TEXT)
    ws.put(3, 6, "Executed By", S_SM_LABEL)
    ws.put(3, 12, fn["executed_by"], S_SM_TEXT)

    ws.put(4, 1, "Lines of code", S_SM_LABEL)
    ws.put(4, 3, fn["loc"], S_SM_TEXT)
    ws.put(4, 6, "Lack of test cases", S_SM_LABEL)
    ws.put(4, 12, lack, S_SM_TEXT, f'IF(Functions!$E$6<>"N/A",MAX(0,ROUND(C4*Functions!$E$6/1000-O7,0)),"N/A")')

    ws.put(5, 1, "Test requirement", S_SM_LABEL)
    ws.put(5, 3, fn["description"], S_SM_TEXT)

    ws.put(6, 1, "Passed", S_SM_BAND_C)
    ws.put(6, 3, "Failed", S_SM_BAND_C)
    ws.put(6, 6, "Untested", S_SM_BAND_C)
    ws.put(6, 12, "N/A/B", S_SM_BAND_C)
    ws.put(6, 15, "Total Test Cases", S_SM_BAND_C)

    ws.put(7, 1, p, S_BOLD_C, f'COUNTIF(F21:{end_letter}21,"P")')
    ws.put(7, 3, f, S_BOLD_C, f'COUNTIF(F21:{end_letter}21,"F")')
    ws.put(7, 6, u, S_BOLD_C, f'COUNTIF(F21:{end_letter}21,"U")')
    ws.put(7, 12, n, S_BOLD_C, f'COUNTIF(F20:{end_letter}20,"N")')
    ws.put(7, 13, a, S_BOLD_C, f'COUNTIF(F20:{end_letter}20,"A")')
    ws.put(7, 14, b, S_BOLD_C, f'COUNTIF(F20:{end_letter}20,"B")')
    ws.put(7, 15, total, S_BOLD_C, f"COUNTA(F9:{end_letter}9)")

    top_merges = [
        (2, 1, 2, 2, S_SM_LABEL), (2, 3, 2, 5, S_SM_TEXT), (2, 6, 2, 11, S_SM_LABEL), (2, 12, 2, right_span, S_SM_TEXT),
        (3, 1, 3, 2, S_SM_LABEL), (3, 3, 3, 5, S_SM_TEXT), (3, 6, 3, 11, S_SM_LABEL), (3, 12, 3, right_span, S_SM_TEXT),
        (4, 1, 4, 2, S_SM_LABEL), (4, 3, 4, 5, S_SM_TEXT), (4, 6, 4, 11, S_SM_LABEL), (4, 12, 4, right_span, S_SM_TEXT),
        (5, 1, 5, 2, S_SM_LABEL), (5, 3, 5, right_span, S_SM_TEXT),
        (6, 1, 6, 2, S_SM_BAND_C), (6, 3, 6, 5, S_SM_BAND_C), (6, 6, 6, 11, S_SM_BAND_C), (6, 12, 6, 14, S_SM_BAND_C), (6, 15, 6, right_span, S_SM_BAND_C),
        (7, 1, 7, 2, S_BOLD_C), (7, 3, 7, 5, S_BOLD_C), (7, 6, 7, 11, S_BOLD_C), (7, 15, 7, right_span, S_BOLD_C),
    ]
    for r1, c1, r2, c2, st in top_merges:
        ws.merge(r1, c1, r2, c2, st)
    for r in range(2, 8):
        ws.row_heights[r] = 30 if r == 5 else 20

    ws.put(9, 1, "Suite: " + ", ".join(fn["source_tests"]), S_SM_LABEL)
    ws.merge(9, 1, 9, 5, S_SM_LABEL)
    for idx in range(len(cases)):
        ws.put(9, start_col + idx, f"UTCID{idx + 1:02d}", S_SM_HDR_SLATE)
    ws.row_heights[9] = 22

    # Section labels
    sections = [
        (10, 15, "Condition"),
        (16, 19, "Confirm"),
        (20, 22, "Result"),
    ]
    for r1, r2, title in sections:
        ws.put(r1, 1, title, S_SM_HDR_NAVY)
        ws.merge(r1, 1, r2, 1, S_SM_HDR_NAVY)

    ws.put(10, 2, "Precondition", S_SM_LABEL)
    ws.merge(10, 2, 10, 3, S_SM_LABEL)
    ws.put(10, 4, fn["precondition"], S_SM_TEXT)
    ws.merge(10, 4, 10, 5, S_SM_TEXT)

    sub_rows = [
        (11, "JUnit @Test Method"),
        (12, "Input / Scenario"),
        (13, "Module Scope"),
        (14, "Class Under Test"),
        (15, "Test Suite File"),
        (16, "Expected Output / Assertion"),
        (17, "Exception / Guard"),
        (18, "Verification Note"),
        (19, "Execution Evidence"),
        (20, "Type (N : Normal, A : Abnormal, B : Boundary)"),
        (21, "Passed/Failed"),
        (22, "Executed Date"),
    ]
    for r, label in sub_rows:
        ws.put(r, 2, label, S_SM_LABEL)
        ws.merge(r, 2, r, 5, S_SM_LABEL)

    for idx, case in enumerate(cases):
        col = start_col + idx
        ws.put(10, col, "Ready", S_SM_CENTER)
        ws.put(11, col, case["method"], S_SM_TEXT)
        ws.put(12, col, case["input"], S_SM_TEXT)
        ws.put(13, col, fn["requirement_name"], S_SM_TEXT)
        ws.put(14, col, fn["class_name"], S_SM_TEXT)
        ws.put(15, col, ", ".join(fn["source_tests"]), S_SM_TEXT)
        ws.put(16, col, case["expected"], S_SM_TEXT)
        ws.put(17, col, "Asserted" if case["type"] in ("A", "B") else "-", S_SM_CENTER)
        ws.put(18, col, "Executed cleanly in JUnit 5", S_SM_TEXT)
        ws.put(19, col, "./mvnw test (Nov 26, 2026)", S_SM_TEXT)
        ws.put(20, col, case["type"], S_SM_CENTER)
        res_style = S_PASS if case["result"] == "P" else (S_FAIL if case["result"] == "F" else S_SM_CENTER)
        ws.put(21, col, case["result"], res_style)
        ws.put(22, col, fn["executed_date"], S_SM_CENTER)

    for r in (11, 12, 16):
        ws.row_heights[r] = 38
    for r in (10, 13, 14, 15, 17, 18, 19, 20, 21, 22):
        ws.row_heights[r] = 22

    for idx, w in enumerate([12, 14, 10, 10, 10], 1):
        ws.col_widths[idx] = w
    for col in range(start_col, right_span + 1):
        ws.col_widths[col] = 24
    return ws


_STYLES_XML = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<styleSheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
  <numFmts count="1">
    <numFmt numFmtId="164" formatCode="0.00"/>
  </numFmts>
  <fonts count="7">
    <font><sz val="10"/><color rgb="FF000000"/><name val="Tahoma"/></font>
    <font><b/><sz val="18"/><color rgb="FF000000"/><name val="Tahoma"/></font>
    <font><b/><sz val="10"/><color rgb="FF000000"/><name val="Tahoma"/></font>
    <font><b/><sz val="10"/><color rgb="FFFFFFFF"/><name val="Tahoma"/></font>
    <font><u/><sz val="10"/><color rgb="FF0000FF"/><name val="Tahoma"/></font>
    <font><sz val="9"/><color rgb="FF000000"/><name val="Tahoma"/></font>
    <font><b/><sz val="9"/><color rgb="FF000000"/><name val="Tahoma"/></font>
  </fonts>
  <fills count="8">
    <fill><patternFill patternType="none"/></fill>
    <fill><patternFill patternType="gray125"/></fill>
    <fill><patternFill patternType="solid"><fgColor rgb="FFFFFFFF"/><bgColor indexed="64"/></patternFill></fill>
    <fill><patternFill patternType="solid"><fgColor rgb="FFF2F4F8"/><bgColor indexed="64"/></patternFill></fill>
    <fill><patternFill patternType="solid"><fgColor rgb="FF000080"/><bgColor indexed="64"/></patternFill></fill>
    <fill><patternFill patternType="solid"><fgColor rgb="FF333399"/><bgColor indexed="64"/></patternFill></fill>
    <fill><patternFill patternType="solid"><fgColor rgb="FFD9E1F2"/><bgColor indexed="64"/></patternFill></fill>
    <fill><patternFill patternType="solid"><fgColor rgb="FFE2EFDA"/><bgColor indexed="64"/></patternFill></fill>
  </fills>
  <borders count="2">
    <border><left/><right/><top/><bottom/><diagonal/></border>
    <border>
      <left style="thin"><color rgb="FFBFBFBF"/></left>
      <right style="thin"><color rgb="FFBFBFBF"/></right>
      <top style="thin"><color rgb="FFBFBFBF"/></top>
      <bottom style="thin"><color rgb="FFBFBFBF"/></bottom>
      <diagonal/>
    </border>
  </borders>
  <cellStyleXfs count="1"><xf numFmtId="0" fontId="0" fillId="0" borderId="0"/></cellStyleXfs>
  <cellXfs count="21">
    <xf numFmtId="0" fontId="0" fillId="0" borderId="0" xfId="0"/>
    <xf numFmtId="0" fontId="1" fillId="0" borderId="0" xfId="0" applyFont="1" applyAlignment="1"><alignment horizontal="center" vertical="center"/></xf>
    <xf numFmtId="0" fontId="2" fillId="3" borderId="1" xfId="0" applyFont="1" applyFill="1" applyBorder="1" applyAlignment="1"><alignment horizontal="left" vertical="center" wrapText="1"/></xf>
    <xf numFmtId="0" fontId="0" fillId="2" borderId="1" xfId="0" applyFont="1" applyFill="1" applyBorder="1" applyAlignment="1"><alignment horizontal="left" vertical="center" wrapText="1"/></xf>
    <xf numFmtId="0" fontId="0" fillId="2" borderId="1" xfId="0" applyFont="1" applyFill="1" applyBorder="1" applyAlignment="1"><alignment horizontal="center" vertical="center" wrapText="1"/></xf>
    <xf numFmtId="0" fontId="3" fillId="4" borderId="1" xfId="0" applyFont="1" applyFill="1" applyBorder="1" applyAlignment="1"><alignment horizontal="center" vertical="center" wrapText="1"/></xf>
    <xf numFmtId="0" fontId="3" fillId="5" borderId="1" xfId="0" applyFont="1" applyFill="1" applyBorder="1" applyAlignment="1"><alignment horizontal="center" vertical="center" wrapText="1"/></xf>
    <xf numFmtId="0" fontId="4" fillId="2" borderId="1" xfId="0" applyFont="1" applyFill="1" applyBorder="1" applyAlignment="1"><alignment horizontal="center" vertical="center" wrapText="1"/></xf>
    <xf numFmtId="0" fontId="4" fillId="2" borderId="1" xfId="0" applyFont="1" applyFill="1" applyBorder="1" applyAlignment="1"><alignment horizontal="left" vertical="center" wrapText="1"/></xf>
    <xf numFmtId="0" fontId="2" fillId="6" borderId="1" xfId="0" applyFont="1" applyFill="1" applyBorder="1" applyAlignment="1"><alignment horizontal="center" vertical="center"/></xf>
    <xf numFmtId="0" fontId="2" fillId="6" borderId="1" xfId="0" applyFont="1" applyFill="1" applyBorder="1" applyAlignment="1"><alignment horizontal="left" vertical="center"/></xf>
    <xf numFmtId="164" fontId="2" fillId="2" borderId="1" xfId="0" applyNumberFormat="1" applyFont="1" applyFill="1" applyBorder="1" applyAlignment="1"><alignment horizontal="right" vertical="center"/></xf>
    <xf numFmtId="0" fontId="6" fillId="3" borderId="1" xfId="0" applyFont="1" applyFill="1" applyBorder="1" applyAlignment="1"><alignment horizontal="left" vertical="center" wrapText="1"/></xf>
    <xf numFmtId="0" fontId="6" fillId="3" borderId="1" xfId="0" applyFont="1" applyFill="1" applyBorder="1" applyAlignment="1"><alignment horizontal="center" vertical="center" wrapText="1"/></xf>
    <xf numFmtId="0" fontId="5" fillId="2" borderId="1" xfId="0" applyFont="1" applyFill="1" applyBorder="1" applyAlignment="1"><alignment horizontal="left" vertical="center" wrapText="1"/></xf>
    <xf numFmtId="0" fontId="5" fillId="2" borderId="1" xfId="0" applyFont="1" applyFill="1" applyBorder="1" applyAlignment="1"><alignment horizontal="center" vertical="center" wrapText="1"/></xf>
    <xf numFmtId="0" fontId="3" fillId="4" borderId="1" xfId="0" applyFont="1" applyFill="1" applyBorder="1" applyAlignment="1"><alignment horizontal="center" vertical="center" wrapText="1"/></xf>
    <xf numFmtId="0" fontId="3" fillId="5" borderId="1" xfId="0" applyFont="1" applyFill="1" applyBorder="1" applyAlignment="1"><alignment horizontal="center" vertical="center" wrapText="1"/></xf>
    <xf numFmtId="0" fontId="6" fillId="7" borderId="1" xfId="0" applyFont="1" applyFill="1" applyBorder="1" applyAlignment="1"><alignment horizontal="center" vertical="center"/></xf>
    <xf numFmtId="0" fontId="6" fillId="3" borderId="1" xfId="0" applyFont="1" applyFill="1" applyBorder="1" applyAlignment="1"><alignment horizontal="center" vertical="center"/></xf>
    <xf numFmtId="0" fontId="2" fillId="2" borderId="1" xfId="0" applyFont="1" applyFill="1" applyBorder="1" applyAlignment="1"><alignment horizontal="center" vertical="center"/></xf>
  </cellXfs>
</styleSheet>
"""


def write_xlsx(sheets: list[SheetBuilder], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    sheet_entries = []
    rel_entries = []
    ct_entries = [
        '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>',
        '<Default Extension="xml" ContentType="application/xml"/>',
        '<Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>',
        '<Override PartName="/xl/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml"/>',
    ]
    for idx, sheet in enumerate(sheets, 1):
        sheet_entries.append(f'<sheet name="{escape(sheet.title)}" sheetId="{idx}" r:id="rId{idx}"/>')
        rel_entries.append(f'<Relationship Id="rId{idx}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet{idx}.xml"/>')
        ct_entries.append(f'<Override PartName="/xl/worksheets/sheet{idx}.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>')

    rel_entries.append(
        f'<Relationship Id="rId{len(sheets) + 1}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>'
    )
    workbook_xml = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"'
        ' xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
        f'<sheets>{"".join(sheet_entries)}</sheets>'
        '</workbook>'
    )
    wb_rels_xml = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        f'{"".join(rel_entries)}'
        '</Relationships>'
    )
    root_rels_xml = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/>'
        '</Relationships>'
    )
    content_types_xml = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
        f'{"".join(ct_entries)}'
        '</Types>'
    )

    with zipfile.ZipFile(output_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("[Content_Types].xml", content_types_xml)
        zf.writestr("_rels/.rels", root_rels_xml)
        zf.writestr("xl/workbook.xml", workbook_xml)
        zf.writestr("xl/_rels/workbook.xml.rels", wb_rels_xml)
        zf.writestr("xl/styles.xml", _STYLES_XML)
        for idx, sheet in enumerate(sheets, 1):
            zf.writestr(f"xl/worksheets/sheet{idx}.xml", sheet.to_xml())


def export(template: Path, reports_root: Path, output_path: Path) -> dict:
    """Generate Report5_Unit Test.xlsx from code-backed unit-test-data.json."""
    del template  # Binary .xls template is tracked as presence input only; clean .xlsx built directly.
    source_path = reports_root / DATA_PATH
    data = json.loads(source_path.read_text(encoding="utf-8"))
    warnings = validate_data(data)

    kloc_target = int(data["cover"].get("normal_tcs_per_kloc", 15))
    sheets = [build_cover(data), build_functions(data), build_statistics(data)]
    for fn in data["functions"]:
        sheets.append(build_function_sheet(fn, kloc_target))
    write_xlsx(sheets, output_path)
    total_cases = sum(len(fn["cases"]) for fn in data["functions"])
    return {
        "warnings": warnings,
        "functions": len(data["functions"]),
        "cases": total_cases,
    }


if __name__ == "__main__":
    raise SystemExit(run_single("report5-unit", TEMPLATE_NAME, SOURCES, export, output_name=OUTPUT_NAME))
