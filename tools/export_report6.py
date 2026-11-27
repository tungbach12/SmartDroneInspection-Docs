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


def chapter_blocks(source):
    chapter = parse_markdown(source, strict_tables=False)
    in_step = False
    for index, block in enumerate(chapter):
        if block.kind == "paragraph":
            if block.text.startswith("**Step "):
                in_step = True
            elif in_step:
                chapter[index - 1].keep_with_next = True
            continue
        if in_step and block.kind == "image" and block.text.startswith("assets/manual/"):
            chapter[index - 1].keep_with_next = True
            block.keep_with_next = True
        in_step = False
    return chapter


def blocks(reports):
    history = parse_markdown(reports / SOURCES[0], strict_tables=False)
    manual = chapter_blocks(reports / SOURCES[1])
    previous_step = False
    for block in manual:
        if block.kind == "paragraph" and block.text.startswith("**Step "):
            block.page_break_before = previous_step
            previous_step = True
    return history + manual


def export(template, reports, output):
    return render_word(template, reports, output, blocks(reports))


if __name__ == "__main__":
    from export_common import run_single
    run_single("report6", TEMPLATE_NAME, SOURCES, export)
