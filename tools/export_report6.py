#!/usr/bin/env python3
"""Assemble the Report 6 sources into the official Software User Guides format."""
from pathlib import Path
import sys

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parent))

from export_common import render_word
from report_ooxml import parse_markdown

TEMPLATE_NAME = "Report6_Software User Guides.docx"
SOURCES = ["report-6-software-user-guides/" + name + ".md"
           for name in ("00-record-of-changes", "01-user-guides")]


def blocks(reports):
    result = []
    for relative in SOURCES:
        result.extend(parse_markdown(reports / relative, strict_tables=False))
    return result


def export(template, reports, output):
    return render_word(template, reports, output, blocks(reports))


if __name__ == "__main__":
    from export_common import run_single
    run_single("report6", TEMPLATE_NAME, SOURCES, export)
