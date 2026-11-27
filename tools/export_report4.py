#!/usr/bin/env python3
"""Assemble four Report 4 sources into the official SDD document format."""
from pathlib import Path
import re
import sys

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parent))

from export_common import render_word
from report_ooxml import descendants, parse_markdown

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
            # Each page groups a design view with its explanation, or a full
            # set of checks for one feature. The diagrams stay at reading size.
            if (block.level == 1
                    or re.match(r"^(?:3\.\d+ FE-|3\.\d+\.(?:[2-9]|\d{2,}) )", block.text)):
                block.page_break_before = True
        if block.kind == "table":
            header = block.rows[0][0]
            if header == "Component":
                block.table_widths = (2510, 2185, 4655)
            elif block.rows[0][:2] == ["No", "Package"]:
                block.table_widths = (650, 3250, 5450)
            elif block.rows[0][:2] == ["No", "Table"]:
                block.table_widths = (650, 3900, 4800)
            elif block.rows[0][:2] == ["No", "Class or Component"]:
                block.table_widths = (650, 3700, 5000)
            elif header == "Step":
                block.table_widths = (2400, 2800, 4150)
            elif header == "Case":
                block.table_widths = (1150, 3350, 4850)
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
    return result


def prepare_cover(document, _metadata):
    # The first heading starts its own page. A separate break paragraph
    # can overflow a full table of contents and create a blank page.
    separator = document.cover[-1]
    if (separator.localName == "p" and not document.text(separator).strip()
            and [br.getAttribute("w:type") for br in descendants(separator, "br")] == ["page"]):
        document.body.removeChild(document.cover.pop())


def export(template, reports, output):
    warnings = ["Historical change rows with extra reference cells are retained in the final description cell"]
    return render_word(template, reports, output, blocks(reports), warnings, prepare_cover=prepare_cover)


if __name__ == "__main__":
    from export_common import run_single
    run_single("report4", TEMPLATE_NAME, SOURCES, export)
