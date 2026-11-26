#!/usr/bin/env python3
"""Assemble four Report 4 sources into the official SDD document format."""
from pathlib import Path
import re
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
        if block.kind == "heading" and re.match(r"[34]\.\d+\s", block.text):
            block.page_break_before = True
        if block.kind == "heading" and block.level == 4 and "Sequence Diagram" in block.text:
            block.page_break_before = True
        if block.kind == "paragraph" and re.fullmatch(r"\*\*Class.*Specifications\*\*", block.text):
            block.page_break_before = True
            block.keep_with_next = True
        if block.kind == "image" and index + 1 < len(result):
            caption = result[index + 1]
            if caption.kind == "paragraph" and caption.text.lstrip("*").startswith("Figure 4."):
                block.keep_with_next = True
    return result


def export(template, reports, output):
    warnings = ["Historical change rows with extra reference cells are retained in the final description cell"]
    return render_word(template, reports, output, blocks(reports), warnings)


if __name__ == "__main__":
    from export_common import run_single
    run_single("report4", TEMPLATE_NAME, SOURCES, export)
