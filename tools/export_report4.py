#!/usr/bin/env python3
"""Assemble four Report 4 sources into the official SDD document format."""
from pathlib import Path
import sys

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parent))

from export_common import render_word
from report_ooxml import parse_markdown

TEMPLATE_NAME = "Report4_Software Design Document.docx"
SOURCES = ["report-4-software-design-document/" + name + ".md" for name in (
    "00-record-of-changes", "01-system-design", "02-database-design", "03-detailed-design")]


def blocks(reports):
    result = []
    for relative in SOURCES:
        result.extend(parse_markdown(reports / relative, strict_tables=False))
    for index, block in enumerate(result):
        if block.kind == "heading":
            block.keep_with_next = True
        if block.kind == "paragraph" and block.text == "**Explanation of Architecture Components**":
            block.keep_with_next = True
        if block.kind == "table":
            header = block.rows[0][0]
            if header == "Component":
                block.table_widths = (2510, 2185, 4655)
            elif block.rows[0][:2] == ["No", "Package"]:
                block.table_widths = (650, 3250, 5450)
            elif header == "No":
                block.table_widths = (650, 2750, 5950)
            elif header == "Boundary":
                block.table_widths = (2400, 2800, 4150)
            elif header == "Date":
                block.table_widths = (1175, 810, 1234, 5585)
            previous = result[index - 1]
            if previous.kind in {"paragraph", "heading"}:
                previous.keep_with_next = True
        if block.kind == "image" and index + 1 < len(result):
            caption = result[index + 1]
            if caption.kind == "paragraph" and caption.text.lstrip("*").startswith("Figure 4."):
                block.keep_with_next = True
                caption.kind = "caption"
                if block.source == reports / SOURCES[1]:
                    caption.keep_with_next = True
                    previous = result[index - 1]
                    if previous.kind == "paragraph" and previous.text.startswith("Figure 4."):
                        previous.keep_with_next = True
    return result


def export(template, reports, output):
    warnings = ["Historical change rows with extra reference cells are retained in the final description cell"]
    return render_word(template, reports, output, blocks(reports), warnings)


if __name__ == "__main__":
    from export_common import run_single
    run_single("report4", TEMPLATE_NAME, SOURCES, export)
