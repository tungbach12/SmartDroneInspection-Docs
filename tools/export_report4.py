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
    return result


def export(template, reports, output):
    warnings = ["Historical change rows with extra reference cells are retained in the final description cell"]
    return render_word(template, reports, output, blocks(reports), warnings)


if __name__ == "__main__":
    from export_common import run_single
    run_single("report4", TEMPLATE_NAME, SOURCES, export)
