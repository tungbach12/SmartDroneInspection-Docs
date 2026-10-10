#!/usr/bin/env python3
"""Export one official-format workbook for each weekly Markdown report."""
from pathlib import Path
import re
import sys

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parent))

from export_common import number
from report_ooxml import Spreadsheet, children, descendants, element, parse_markdown, plain

TEMPLATE_NAME = "Project Weekly Report_GroupName.xlsx"
SOURCES = ["weekly-project-reports"]


def metadata(path):
    text = path.read_text(encoding="utf-8")
    def value(key):
        match = re.search(r"\*\*" + re.escape(key) + r":\*\*\s*([^\n]+)", text)
        return plain(match[1]) if match else "Not supplied"
    return value("Group"), value("Reporting period")


def export(template, source, output):
    book = Spreadsheet(template)
    group, period = metadata(source)
    book.put("Wx", "B2", group)
    book.put("Wx", "B3", period)
    blocks = [b for b in parse_markdown(source) if b.kind == "table"]
    if len(blocks) != 4 or any(len(b.rows[0]) != 5 for b in blocks):
        raise ValueError(f"Weekly report must contain four five-column tables: {source}")
    prototypes = [(book.row_template("Wx", bar), book.row_template("Wx", header),
                   book.row_template("Wx", data)) for bar, header, data in
                  ((4, 5, 6), (10, 11, 12), (16, 17, 18), (22, 23, 24))]
    titles = [book.value("Wx", f"A{r}") for r in (4, 10, 16, 22)]
    merges = descendants(book.sheet("Wx"), "mergeCells")
    if merges:
        container = merges[0]
        for merge in list(children(container, "mergeCell")):
            if int(re.search(r"\d+", merge.getAttribute("ref"))[0]) >= 4:
                container.removeChild(merge)
    book.clear_rows("Wx", 4)
    row_no, warnings = 4, []
    for block, prototypes_for_section, title in zip(blocks, prototypes, titles):
        bar, header, data = prototypes_for_section
        book.clone_row("Wx", row_no, bar)
        book.put("Wx", f"A{row_no}", title)
        if merges:
            container.appendChild(element(book.sheet("Wx"), container.namespaceURI, "mergeCell",
                                           {"ref": f"A{row_no}:E{row_no}"}))
        row_no += 1
        book.clone_row("Wx", row_no, header)
        for col, value in enumerate(block.rows[0], 1):
            book.put("Wx", f"{chr(64 + col)}{row_no}", plain(value))
        row_no += 1
        for row in block.rows[1:]:
            book.clone_row("Wx", row_no, data)
            for col, value in enumerate(row, 1):
                book.put("Wx", f"{chr(64 + col)}{row_no}", number(value))
            if book.fit_height("Wx", row_no, row, [6, 42, 25, 24, 95]):
                warnings.append(f"Row {row_no} reaches Excel's row-height limit")
            row_no += 1
        row_no += 1
    if merges:
        container.setAttribute("count", str(len(children(container, "mergeCell"))))
    book.dimensions("Wx", "E", row_no - 1)
    audit = book.save(output)
    return {**audit, "source_tables": 4,
            "source_rows": sum(len(b.rows) - 1 for b in blocks),
            "warnings": warnings, "content_complete": True}


if __name__ == "__main__":
    from export_common import run_single
    run_single("weekly", TEMPLATE_NAME, SOURCES, export)
