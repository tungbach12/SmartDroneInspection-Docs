#!/usr/bin/env python3
"""Assemble the Report 7 source into the official Final Project Report format."""
from functools import partial
from pathlib import Path
import re
import sys

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parent))

from export_common import render_word
from report_ooxml import children, descendants, parse_markdown, plain
import export_report1
import export_report2
import export_report3
import export_report4
import export_report5_doc
import export_report6

TEMPLATE_NAME = "Report7_Final Project Report.docx"
HISTORY = "report-7-final-project-report/00-record-of-changes.md"
INDEX = "report-7-final-project-report/07-submission-index.md"
CHAPTERS = (
    ("I. Project Introduction", export_report1),
    ("II. Project Management Plan", export_report2),
    ("III. Software Requirement Specification", export_report3),
    ("IV. Software Design Description", export_report4),
    ("V. Software Testing Documentation", export_report5_doc),
    ("VI. Release Package & User Guides", export_report6),
)
SOURCES = [HISTORY, *(path for _, exporter in CHAPTERS for path in exporter.SOURCES), INDEX]


def blocks(reports):
    result = parse_markdown(reports / HISTORY)
    for number, (title, exporter) in enumerate(CHAPTERS, 1):
        chapter = exporter.blocks(reports)
        start = next(i for i, block in enumerate(chapter)
                     if block.kind == "heading" and block.level == 1 and block.text.startswith("II. "))
        if number == 1:
            front = next(i for i, block in enumerate(chapter)
                         if block.kind == "heading" and block.text == "Acknowledgement")
            result.extend(chapter[front:start])
        chapter[start].text = title
        chapter[start].page_break_before = True
        result.extend(chapter[start:])
    result.extend(parse_markdown(reports / INDEX))
    return result


def prepare_cover(chapter, document, metadata):
    team = next(block.rows[1:] for block in parse_markdown(chapter, strict_tables=False)
                if block.kind == "table" and block.rows[0][:2] == ["Full Name", "Role"])
    members = []
    supervisors = {}
    for name, role, *_ in team:
        if role in {"Leader", "Member"}:
            match = re.fullmatch(r"(.+) \((SE\d+)\)", plain(name))
            if match is None:
                raise ValueError(f"Missing student ID on the Report 7 cover: {name}")
            members.append(f"{match[1]} ({match[2]})")
        else:
            supervisors[role] = plain(name)

    cover_paragraphs = [p for node in document.cover if node.localName == "tbl"
                        for p in descendants(node, "p")]
    member_slots = [p for p in cover_paragraphs if document.text(p).startswith("<Member name>")]
    if not 0 < len(members) <= len(member_slots):
        raise ValueError("The Report 7 cover must have a slot for each student")

    labeled_rows = {}
    for table in (node for node in document.cover if node.localName == "tbl"):
        for row in children(table, "tr"):
            cells = children(row, "tc")
            if len(cells) == 2:
                labeled_rows[document.text(cells[0]).strip()] = children(cells[1], "p")[0]

    values = {
        "[Project name]": metadata["project"],
        "<Group Name>": metadata["group"],
    }
    for placeholder, value in values.items():
        paragraph = next(p for p in cover_paragraphs if document.text(p) == placeholder)
        descendants(paragraph, "t")[0].firstChild.data = value
    for paragraph, name in zip(member_slots, members):
        first, *extra = descendants(paragraph, "t")
        first.firstChild.data = name
        for node in extra:
            node.parentNode.removeChild(node)
    for paragraph in member_slots[len(members):]:
        paragraph.parentNode.removeChild(paragraph)
    for label, value in {
        "Supervisor": supervisors["Supervisor"],
        "Ext Supervisor": supervisors["External Supervisor and Lecturer"],
        "Capstone Project code": metadata["code"],
    }.items():
        paragraph = labeled_rows[label]
        for run in children(paragraph, "r"):
            paragraph.removeChild(run)
        paragraph.appendChild(document.run(value))


def export(template, reports, output):
    return render_word(template, reports, output, blocks(reports),
                       prepare_cover=partial(prepare_cover, reports / SOURCES[1]),
                       fallback_table_header_fill="FFE8E1")


if __name__ == "__main__":
    from export_common import run_single
    run_single("report7", TEMPLATE_NAME, SOURCES, export)
