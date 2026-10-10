#!/usr/bin/env python3
"""Export Report 1 content using its official Project Introduction format."""
from pathlib import Path
import sys

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parent))

from export_common import render_word
from report_ooxml import parse_markdown

TEMPLATE_NAME = "Report1_Project Introduction.docx"
SOURCES = ["report-1-project-introduction/report1-project-introduction.md"]


def blocks(reports):
    source = parse_markdown(reports / SOURCES[0])
    start = next(i for i, block in enumerate(source)
                 if block.kind == "heading" and "Record of Changes" in block.text)
    # The source includes an extracted cover and textual TOC. Retain the
    # official cover/TOC shell rather than duplicating those source artifacts.
    return source[start:]


def export(template, reports, output):
    return render_word(template, reports, output, blocks(reports))


if __name__ == "__main__":
    from export_common import run_single
    run_single("report1", TEMPLATE_NAME, SOURCES, export)
