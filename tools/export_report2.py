#!/usr/bin/env python3
"""Export Report 2 content using its official Project Management Plan format."""
from pathlib import Path
import sys

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parent))

from export_common import render_word
from report_ooxml import parse_markdown

TEMPLATE_NAME = "Report2_Project Management Plan.docx"
SOURCES = ["report-2-project-management-plan/report2-project-management-plan.md"]


def blocks(reports):
    source = parse_markdown(reports / SOURCES[0])
    start = next(i for i, block in enumerate(source)
                 if block.kind == "heading" and "Record of Changes" in block.text)
    return source[start:]


def export(template, reports, output):
    return render_word(template, reports, output, blocks(reports))


if __name__ == "__main__":
    from export_common import run_single
    run_single("report2", TEMPLATE_NAME, SOURCES, export)
