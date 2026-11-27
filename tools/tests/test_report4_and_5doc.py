import tempfile
import unittest
from pathlib import Path

from support import OFFICIAL, REPORTS, assert_word_export, original
import export_project_tracking
import export_report4
import export_report5_doc
from report_ooxml import Package, Spreadsheet, WordDocument, children, descendants


class Report4And5DocTests(unittest.TestCase):
    def test_report4_sdd_exports_with_embedded_diagrams_and_tables(self):
        result = assert_word_export(self, export_report4)
        self.assertGreaterEqual(result["tables"], 10)
        self.assertEqual(result["source_images"], 92)
        self.assertFalse(any("Mermaid" in w for w in result["warnings"]))

    def test_report4_tables_follow_architecture_figures_and_use_school_format(self):
        template = original(OFFICIAL, export_report4.TEMPLATE_NAME)
        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp) / export_report4.TEMPLATE_NAME
            export_report4.export(template, REPORTS, output)
            package = Package(output)
            document = package.xml("word/document.xml")
            settings = package.xml("word/settings.xml")

        compression = descendants(settings, "doNotAutoCompressPictures")
        self.assertEqual(compression[0].getAttribute("w:val"), "true")

        body = children(descendants(document, "body")[0])
        tables = [node for node in body if node.localName == "tbl"]
        self.assertEqual(len(tables), 60)
        for table in tables:
            header, *data = children(table, "tr")
            fills = [cell.getAttribute("w:fill") for cell in descendants(header, "shd")]
            self.assertEqual(fills, ["FFE8E1"] * len(children(header, "tc")))
            self.assertTrue(descendants(header, "tblHeader"))
            for row in data:
                self.assertFalse(descendants(row, "shd"))
                for paragraph in descendants(row, "p"):
                    self.assertEqual(len(children(paragraph, "pPr")), 1)
                    self.assertNotIn("comment", [s.getAttribute("w:val")
                                                 for s in descendants(paragraph, "pStyle")])

        captions = [(i, node) for i, node in enumerate(body) if node.localName == "p"
                    and WordDocument.text(node).startswith("Figure 4.")
                    and descendants(body[i - 1], "drawing")]
        self.assertEqual(len(captions), 92)
        for i, caption in captions:
            self.assertFalse(WordDocument.text(caption).endswith("*"))
            self.assertEqual(descendants(caption, "jc")[0].getAttribute("w:val"), "center")
            self.assertTrue(descendants(body[i - 1], "keepNext"))
        for i, caption in captions[:4]:
            table = body[i + 2]
            self.assertEqual(table.localName, "tbl", WordDocument.text(caption))
            widths = [int(col.getAttribute("w:w")) for col in descendants(table, "gridCol")]
            self.assertEqual(sum(widths), 9350)
            self.assertEqual(max(widths), widths[-1])

    def test_report4_each_feature_has_design_views_and_verification(self):
        blocks = export_report4.blocks(REPORTS)
        for feature in range(1, 25):
            prefix = f"3.{feature}."
            headings = [b.text.removeprefix(prefix) for b in blocks
                        if b.kind == "heading" and b.text.startswith(prefix)]
            self.assertEqual(headings, ["1 Components and Responsibilities", "2 Main Sequence",
                                        "3 Alternative Sequence", "4 Design Verification"])
        self.assertEqual(sum(b.kind == "image" and b.text.endswith("-alternate.png")
                             for b in blocks), 24)

    def test_report5_documentation_preserves_merged_header_table_and_styles(self):
        result = assert_word_export(self, export_report5_doc)
        self.assertEqual(result["tables"], 13)
        self.assertTrue(result["format_parts_preserved"])

    def test_project_tracking_workbook_populates_all_four_sheets(self):
        template = original(OFFICIAL, export_project_tracking.TEMPLATE_NAME)
        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp) / export_project_tracking.TEMPLATE_NAME
            result = export_project_tracking.export(template, REPORTS, output)
            self.assertTrue(result["format_parts_preserved"])
            self.assertEqual(result["wbs_items"], 25)
            self.assertEqual(result["issues"], 5)
            self.assertEqual(result["defects"], 6)
            self.assertEqual(result["qa_items"], 4)
            book = Spreadsheet(output)
            self.assertEqual(book.value("WBS", "B8"), "Organization Registration & User Sign-In")
            self.assertEqual(book.value("Defects", "F4"), "Closed")


if __name__ == "__main__":
    unittest.main()
