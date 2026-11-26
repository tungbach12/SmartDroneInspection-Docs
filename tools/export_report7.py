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
    result = []
    for relative in SOURCES[:-1]:
        result.extend(parse_markdown(reports / relative, strict_tables=False))
    result.extend(chapter_blocks(reports / SOURCES[-1]))
    # The official template supplies its own FPT cover and TOC shell, so the
    # source begins at the Record of Changes rather than duplicating them.
    start = next(i for i, block in enumerate(result)
                 if block.kind == "heading" and "Record of Changes" in block.text)
    return result[start:]


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
                       prepare_cover=partial(prepare_cover, reports / SOURCES[1]))


if __name__ == "__main__":
    from export_common import run_single
    run_single("report7", TEMPLATE_NAME, SOURCES, export)
