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
    "00-record-of-changes", "00-project-report", "01-overall-description",
    "02-user-requirements", "03-functional-requirements", "04-non-functional-requirements",
    "05-requirement-appendix")]


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
    run_single("report3", TEMPLATE_NAME, SOURCES, export)
