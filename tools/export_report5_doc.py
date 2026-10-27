#!/usr/bin/env python3
"""Assemble Report 5 Test Documentation sources into the official Word template."""
from pathlib import Path
import sys

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parent))

from export_common import render_word
from report_ooxml import parse_markdown

TEMPLATE_NAME = "Report5_Test Documentation.docx"
SOURCES = ["report-5-test-documentation/" + name + ".md" for name in (
    "00-record-of-changes", "01-testing-documentation")]


def blocks(reports):
    result = []
    for relative in SOURCES:
        result.extend(parse_markdown(reports / relative, strict_tables=False))
    return result


def export(template, reports, output):
    warnings = ["Test Levels matrix preserves the template's two-row merged header structure"]
    return render_word(template, reports, output, blocks(reports), warnings)


if __name__ == "__main__":
    from export_common import run_single
    run_single("report5-documentation", TEMPLATE_NAME, SOURCES, export)
