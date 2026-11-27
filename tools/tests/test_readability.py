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
import export_report1
import export_report3
import export_report6
import export_report7


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


class CoverTests(unittest.TestCase):
    def test_report7_cover_uses_real_project_and_team_details(self):
        from export_common import original, project_metadata

        document = WordDocument(original(OFFICIAL, export_report7.TEMPLATE_NAME))
        metadata = project_metadata(REPORTS)
        document.fill_cover(metadata["project"], metadata["location"])
        export_report7.prepare_cover(REPORTS / export_report1.SOURCES[0], document, metadata)
        cover = "\n".join(document.text(node) for node in document.cover)
        for text in ("SmartDroneInspection", "FA26SE112", "GFA26SE139", "SE184212",
                     "SE170027", "SE180220", "SE180082", "Phạm Minh Trí",
                     "Đặng Ngọc Minh Đức", "November 2026"):
            self.assertIn(text, cover)
        self.assertNotRegex(cover, r"\[Project name\]|<Group Name>|<Member name>|<month>")


class ListMarkerTests(unittest.TestCase):
    def test_no_body_paragraph_starts_with_a_literal_list_marker(self):
        body = exported_document()
        # The cover carries a deliberately dashed date line, e.g.
        # "- Hanoi, November 2026 -", so it is not a leaked list marker.
        offenders = [text for node, text in paragraphs(body)
                     if re.match(r"^[-*+]\s", text)
                     and not re.match(r"^-\s+[^,]+,\s+\w+\s+\d{4}\s+-$", text)]
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
        self.assertGreaterEqual(len(tables[0].rows), 2)

    def test_no_paragraph_looks_like_a_raw_markdown_table_row(self):
        body = exported_document()
        # Mermaid source legitimately contains '|'; only prose is checked.
        offenders = [text for node, text in paragraphs(body)
                     if text.count("|") >= 3 and "flowchart" not in text]
        self.assertEqual(offenders, [],
                         f"{len(offenders)} raw table row(s) exported as prose: "
                         f"{offenders[:2]}")

    def test_report7_two_column_body_tables_ignore_cover_layout_tables(self):
        from export_common import original
        document = WordDocument(original(OFFICIAL, "Report7_Final Project Report.docx"))
        self.assertEqual(len(document.table_prototypes), 2)
        rendered = document.table([
            ["Category", "Tools / Infrastructure"],
            ["Technology", "Java 21, Spring Boot 4.1"],
        ])
        xml = rendered.toxml()
        self.assertNotIn('w:val="nil"', xml)
        self.assertNotIn('w:val="32"', xml)

    def test_report7_body_tables_use_peach_headers(self):
        from tempfile import TemporaryDirectory
        from export_common import original

        template = original(OFFICIAL, export_report7.TEMPLATE_NAME)
        with TemporaryDirectory() as temp:
            output = Path(temp) / export_report7.TEMPLATE_NAME
            export_report7.export(template, REPORTS, output)
            body = descendants(Package(output).xml("word/document.xml"), "body")[0]

        elements = children(body)
        start = next(i for i, node in enumerate(elements)
                     if node.localName == "p" and WordDocument.text(node) == "Record of Changes")
        tables = [node for node in elements[start:] if node.localName == "tbl"]
        self.assertTrue(tables)
        for table in tables:
            header, *body_rows = children(table, "tr")
            for cell in children(header, "tc"):
                fills = [node.getAttribute("w:fill") for node in descendants(cell, "shd")]
                self.assertEqual(fills, ["FFE8E1"], WordDocument.text(header))
            for row in body_rows:
                fills = [node.getAttribute("w:fill") for node in descendants(row, "shd")]
                self.assertNotIn("FFE8E1", fills, WordDocument.text(header))

    def test_report3_table_cells_allow_wrapping_and_avoid_bottom_alignment(self):
        body = exported_document()
        tables = [node for node in body if node.localName == "tbl"]
        self.assertTrue(tables)
        for tbl in tables:
            self.assertEqual(descendants(tbl, "noWrap"), [])
            bottom_aligns = [
                va for va in descendants(tbl, "vAlign")
                if va.getAttribute("w:val") == "bottom"
            ]
            self.assertEqual(bottom_aligns, [])


class DiagramTests(unittest.TestCase):
    def test_report7_manual_callouts_stay_with_their_figure(self):
        from export_common import original

        document = WordDocument(original(OFFICIAL, export_report7.TEMPLATE_NAME))
        document.fill_cover("SmartDroneInspection", "")
        chapter = export_report6.chapter_blocks(REPORTS / export_report6.SOURCES[-1])
        figure_count = sum(
            block.kind == "image" and block.text.startswith("assets/manual/")
            for block in chapter
        )
        document.append(chapter)
        manual_steps = []
        active = None
        for node, prose in paragraphs(children(document.body)):
            if re.match(r"^Step \d+ — ", prose) and not style(node).startswith("Heading"):
                self.assertTrue(descendants(node, "keepNext"))
                active = [node]
            elif active is not None:
                if prose.startswith("Figure 6."):
                    self.assertTrue(descendants(active[-1], "drawing"))
                    self.assertTrue(all(descendants(p, "keepNext") for p in active))
                    self.assertFalse(descendants(node, "keepNext"))
                    manual_steps.append(active)
                    active = None
                else:
                    active.append(node)
        self.assertGreater(figure_count, 0)
        self.assertEqual(len(manual_steps), figure_count)

    def test_report7_uses_all_six_standalone_report_bodies(self):
        assembled = export_report7.blocks(REPORTS)
        for title, exporter in export_report7.CHAPTERS:
            start = next(i for i, b in enumerate(assembled) if b.kind == "heading" and b.text == title)
            source = exporter.blocks(REPORTS)
            main = next(i for i, b in enumerate(source)
                        if b.kind == "heading" and b.level == 1 and b.text.startswith("II. "))
            self.assertEqual(assembled[start + 1:start + len(source) - main], source[main + 1:])

    def test_mermaid_keeps_line_structure_and_is_marked_as_source(self):
        body = exported_document()
        placeholders = [
            "".join(text_of(t) for t in descendants(node, "t"))
            for node in body
            if node.localName == "tbl"
            and "Figure Placeholder:" in "".join(text_of(t) for t in descendants(node, "t"))
        ]
        embedded_drawings = [
            node for node in body
            if node.localName == "p" and descendants(node, "drawing")
        ]
        if placeholders:
            self.assertGreaterEqual(len(placeholders), 2)
            for text in placeholders:
                self.assertIn("Insert ", text)
        else:
            self.assertGreaterEqual(len(embedded_drawings), 2)


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

    def test_toc_entries_preserve_dotted_leader_tabs_and_pageref_hyperlinks(self):
        body = exported_document()
        sdt = next(node for node in body if node.localName == "sdt")
        toc_paras = [
            p for p in descendants(sdt, "p")
            if style(p) in {"TOC1", "TOC2", "TOC3"}
        ]
        self.assertGreaterEqual(len(toc_paras), 20)
        for p in toc_paras:
            tabs = descendants(p, "tab")
            self.assertTrue(
                any(
                    t.getAttribute("w:val") == "right"
                    and t.getAttribute("w:leader") == "dot"
                    and t.getAttribute("w:pos") == "9040"
                    for t in tabs
                ),
                "Every TOC entry must include right-aligned dotted leader tab at 9040",
            )
            self.assertTrue(descendants(p, "hyperlink"), "Every TOC entry must include hyperlink anchor")
            self.assertTrue(
                any("PAGEREF _Toc" in "".join(text_of(t) for t in descendants(r, "instrText"))
                    for r in descendants(p, "r")),
                "Every TOC entry must include PAGEREF field",
            )


if __name__ == "__main__":
    unittest.main()
