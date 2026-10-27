#!/usr/bin/env python3
"""Export Report3_Project Tracking.xlsx from Markdown tables while preserving template styles."""
from pathlib import Path
import sys

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parent))

from export_common import number
from export_report5 import discard_stale_calculation_chain
from report_ooxml import Spreadsheet, plain, tables

TEMPLATE_NAME = "Report3_Project Tracking.xlsx"
SOURCES = ["project-tracking/project-tracking.md"]


def export(template, reports, output):
    source = reports / SOURCES[0]
    all_tables = tables(source)
    if len(all_tables) != 4:
        raise ValueError(f"Expected 4 tables (WBS, Issues, Defects, Q&A) in {source}, found {len(all_tables)}")
    wbs_rows, issue_rows, defect_rows, qa_rows = all_tables

    book = Spreadsheet(template)
    warnings = []

    # 1. WBS sheet (header at row 7, data starts at row 8)
    wbs_proto = book.row_template("WBS", 8)
    book.clear_rows("WBS", 8)
    for row_no, row in enumerate(wbs_rows[1:], 8):
        book.clone_row("WBS", row_no, wbs_proto)
        book.put("WBS", f"A{row_no}", row_no - 7, f"ROW()-7")
        for col_idx, val in enumerate(row[1:], 2):
            book.put("WBS", f"{chr(64 + col_idx)}{row_no}", number(val))
        book.fit_height("WBS", row_no, row, [6, 32, 12, 12, 55, 14, 14])
    book.dimensions("WBS", "G", len(wbs_rows) + 6)

    # 2. Issues sheet (header at row 3, data starts at row 4)
    iss_proto = book.row_template("Issues", 4)
    book.clear_rows("Issues", 4)
    for row_no, row in enumerate(issue_rows[1:], 4):
        book.clone_row("Issues", row_no, iss_proto)
        book.put("Issues", f"A{row_no}", row_no - 3, f"ROW()-3")
        for col_idx, val in enumerate(row[1:], 2):
            book.put("Issues", f"{chr(64 + col_idx)}{row_no}", plain(val))
        book.fit_height("Issues", row_no, row, [6, 36, 32, 12, 22, 14, 14, 12, 45])
    book.dimensions("Issues", "I", len(issue_rows) + 2)

    # 3. Defects sheet (header at row 3, data starts at row 4)
    def_proto = book.row_template("Defects", 4)
    book.clear_rows("Defects", 4)
    for row_no, row in enumerate(defect_rows[1:], 4):
        book.clone_row("Defects", row_no, def_proto)
        for col_idx, val in enumerate(row, 1):
            book.put("Defects", f"{chr(64 + col_idx)}{row_no}", plain(val))
        book.fit_height("Defects", row_no, row, [12, 28, 22, 48, 22, 12, 48])
    book.dimensions("Defects", "G", len(defect_rows) + 2)

    # 4. Q&A sheet (header at row 3, data starts at row 4)
    qa_proto = book.row_template("Q&A", 4)
    book.clear_rows("Q&A", 4)
    for row_no, row in enumerate(qa_rows[1:], 4):
        book.clone_row("Q&A", row_no, qa_proto)
        for col_idx, val in enumerate(row, 1):
            book.put("Q&A", f"{chr(64 + col_idx)}{row_no}", plain(val))
        book.fit_height("Q&A", row_no, row, [14, 42, 24, 12, 12, 48])
    book.dimensions("Q&A", "F", len(qa_rows) + 2)

    extra = discard_stale_calculation_chain(book)
    audit = book.save(output, extra)
    return {**audit, "wbs_items": len(wbs_rows) - 1, "issues": len(issue_rows) - 1,
            "defects": len(defect_rows) - 1, "qa_items": len(qa_rows) - 1,
            "warnings": warnings}


if __name__ == "__main__":
    from export_common import run_single
    run_single("project-tracking", TEMPLATE_NAME, SOURCES, export)
