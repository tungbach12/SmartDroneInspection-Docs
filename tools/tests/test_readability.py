"""Source Markdown must not leak its syntax into the exported document.

These are regression tests for readability defects seen in a generated
Report 3: literal list markers, tables broken by blank lines, and Mermaid
source dumped as a single run-on paragraph.
"""
import re
import unittest
from pathlib import Path

from support import OFFICIAL, REPORTS, assert_word_export
from report_ooxml import (Package, WordDocument, children, descendants,
                          parse_markdown, text_of)
import export_report3


def exported_document():
    """Return the generated document body so tests read the real result."""
    import tempfile

    from export_common import original

    template = original(OFFICIAL, export_report3.TEMPLATE_NAME)
    with tempfile.TemporaryDirectory() as temp:
        output = Path(temp) / export_report3.TEMPLATE_NAME
        export_report3.export(template, REPORTS, output)
        package = Package(output)
        body = descendants(package.xml("word/document.xml"), "body")[0]
        return list(body.childNodes)


def paragraphs(body):
    def text(node):
        return "".join(t.firstChild.data if t.firstChild else ""
                       for t in descendants(node, "t"))
    return [(node, text(node)) for node in body if node.localName == "p"]


def style(node):
    styles = descendants(node, "pStyle")
    return styles[0].getAttribute("w:val") if styles else ""


class ListMarkerTests(unittest.TestCase):
    def test_no_body_paragraph_starts_with_a_literal_list_marker(self):
        body = exported_document()
        offenders = [text for node, text in paragraphs(body)
                     if re.match(r"^[-*+]\s", text)]
        self.assertEqual(offenders, [],
                         f"{len(offenders)} paragraph(s) still begin with '-': "
                         f"{offenders[:3]}")

    def test_source_lists_become_numbered_word_lists(self):
        body = exported_document()
        listed = [node for node, text in paragraphs(body)
                  if descendants(node, "numPr")]
        self.assertGreaterEqual(len(listed), 100,
                                "every Markdown list item should render as a real Word list")

    def test_each_list_item_carries_exactly_one_numbering_definition(self):
        body = exported_document()
        offenders = []
        for node in body:
            if node.localName != "p":
                continue
            numbering = descendants(node, "numPr")
            if len(numbering) > 1 or any(len(children(n, "numId")) > 1
                                         for n in numbering):
                offenders.append(text_of(node)[:40])
        self.assertEqual(offenders, [],
                         "duplicate numPr makes Word resolve the list ambiguously")


class TableContinuityTests(unittest.TestCase):
    def test_record_of_changes_is_one_table_not_three(self):
        blocks = parse_markdown(
            REPORTS / "report-3-software-requirement-specification/00-record-of-changes.md",
            strict_tables=False)
        tables = [b for b in blocks if b.kind == "table"]
        self.assertEqual(len(tables), 1,
                         "blank lines inside the change table split it into fragments")
        self.assertGreater(len(tables[0].rows), 20)

    def test_no_paragraph_looks_like_a_raw_markdown_table_row(self):
        body = exported_document()
        # Mermaid source legitimately contains '|'; only prose is checked.
        offenders = [text for node, text in paragraphs(body)
                     if text.count("|") >= 3 and "flowchart" not in text]
        self.assertEqual(offenders, [],
                         f"{len(offenders)} raw table row(s) exported as prose: "
                         f"{offenders[:2]}")


class DiagramTests(unittest.TestCase):
    def test_mermaid_keeps_line_structure_and_is_marked_as_source(self):
        body = exported_document()
        diagrams = [text for node, text in paragraphs(body)
                    if re.search(r"flowchart (LR|TD)", text)]
        self.assertEqual(len(diagrams), 2)
        for text in diagrams:
            self.assertIn("-->", text)
        breaks = sum(len(descendants(node, "br")) for node in body)
        self.assertGreaterEqual(breaks, 20,
                                "Mermaid source must keep its line breaks")


class OutlineTests(unittest.TestCase):
    """Table header cells must not appear as entries in the document outline.

    ``HeadingLv1`` is the template's own table-header style (bold Tahoma, brown,
    centred). It has no ``outlineLvl``, so it never reaches the TOC. These
    tests therefore check the real requirement - that header text is not a
    body-level heading - rather than the style name.
    """

    def test_no_table_header_text_becomes_a_body_level_heading(self):
        body = exported_document()
        body_headings = {text for node, text in paragraphs(body)
                         if node.parentNode is body
                         and style(node).startswith("Heading")}
        for header in ("Step", "Responsible actor", "Change Description",
                       "Output and gate", "In charge"):
            self.assertNotIn(header, body_headings)

    def test_table_header_cells_keep_the_template_style(self):
        body = exported_document()
        tables = [node for node in body if node.localName == "tbl"]
        self.assertTrue(tables)
        styled = [
            style(paragraph)
            for table in tables[:3]
            for cell in descendants(table, "tc")
            for paragraph in children(cell, "p")
        ]
        self.assertIn("HeadingLv1", styled,
                      "header cells should keep the template's original style")


if __name__ == "__main__":
    unittest.main()