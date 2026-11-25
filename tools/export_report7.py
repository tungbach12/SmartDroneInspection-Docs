#!/usr/bin/env python3
"""Assemble the Report 7 source into the official Final Project Report format."""
from pathlib import Path
import sys

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parent))

from export_common import render_word
from report_ooxml import parse_markdown

TEMPLATE_NAME = "Report7_Final Project Report.docx"
SOURCES = ["report-7-final-project-report/" + name + ".md"
           for name in (
               "00-record-of-changes",
               "01-project-introduction",
               "02-project-management-plan",
               "03-software-requirement-specification",
               "04-software-design-description",
               "05-software-testing-documentation",
               "06-release-package-and-user-guides",
           )]


def chapter_blocks(source):
    chapter = parse_markdown(source, strict_tables=False)
    for index, block in enumerate(chapter):
        if block.kind != "image" or not block.text.startswith("assets/manual/"):
            continue
        start = index - 1
        while start >= 0 and chapter[start].kind == "paragraph":
            if chapter[start].text.startswith("**Step "):
                for paragraph in chapter[start:index + 1]:
                    paragraph.keep_with_next = True
                break
            start -= 1
    return chapter


def blocks(reports):
    result = []
    for relative in SOURCES[:-1]:
        result.extend(parse_markdown(reports / relative, strict_tables=False))
    result.extend(chapter_blocks(reports / SOURCES[-1]))
    # The official template supplies its own FPT cover and TOC shell, so the
    # source begins at the Record of Changes rather than duplicating them.
    start = next(i for i, block in enumerate(result)
                 if block.kind == "heading" and "Record of Changes" in block.text)
    return result[start:]


def export(template, reports, output):
    return render_word(template, reports, output, blocks(reports))


if __name__ == "__main__":
    from export_common import run_single
    run_single("report7", TEMPLATE_NAME, SOURCES, export)
