#!/usr/bin/env python3
"""Assemble seven Report 3 sources into the official SRS document format."""
from pathlib import Path
import sys

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parent))

from export_common import render_word
from report_ooxml import parse_markdown

TEMPLATE_NAME = "Report3_Software Requirement Specification.docx"
SOURCES = ["report-3-software-requirement-specification/" + name + ".md" for name in (
    "00-record-of-changes", "01-overall-description",
    "02-user-requirements", "03-functional-requirements", "04-non-functional-requirements",
    "05-requirement-appendix")]


TABLE_WIDTHS = {
    ("Lifecycle Entity", 3): (1750, 2150, 5032),
    ("Domain & Feature", 4): (1750, 1850, 2500, 2704),
    ("External Interface", 3): (2050, 1850, 5032),
    ("NFR ID", 6): (850, 1250, 2350, 1450, 1650, 1450),
    ("Product Feature", 6): (850, 2150, 750, 750, 3432, 1150),
    ("Reference Source", 3): (2400, 1750, 4782),
    ("Use Case Element", 2): (2100, 6832),
    ("ID", 2): (1050, 8032),
}


def blocks(reports):
    result = []
    for relative in SOURCES:
        result.extend(parse_markdown(reports / relative, strict_tables=False))
    for block in result:
        if block.kind == "table" and block.rows:
            key = (block.rows[0][0], len(block.rows[0]))
            if key in TABLE_WIDTHS:
                block.table_widths = TABLE_WIDTHS[key]
    return result


def export(template, reports, output):
    warnings = ["Historical change rows with extra reference cells are retained in the final description cell"]
    return render_word(template, reports, output, blocks(reports), warnings)


if __name__ == "__main__":
    from export_common import run_single
    run_single("report3", TEMPLATE_NAME, SOURCES, export)
