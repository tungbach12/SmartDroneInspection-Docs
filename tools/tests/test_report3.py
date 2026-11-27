import unittest
from pathlib import Path
from support import OFFICIAL, REPORTS, assert_word_export
import export_report3


class Report3Tests(unittest.TestCase):
    def test_six_sections_and_source_diagrams_are_not_lost(self):
        self.assertEqual(len(export_report3.SOURCES), 6)
        result = assert_word_export(self, export_report3)
        self.assertGreater(result["tables"], 9)
        self.assertFalse(any("Mermaid" in warning for warning in result["warnings"]))

    def test_section_order_is_explicit(self):
        headings = [b.text for b in export_report3.blocks(REPORTS) if b.kind == "heading"]
        self.assertLess(headings.index("I. Record of Changes"), headings.index("II. Software Requirement Specification"))

    def test_all_tables_use_dxa_widths_and_balanced_columns(self):
        from tempfile import TemporaryDirectory
        from export_common import original
        from report_ooxml import Package, descendants

        template = original(OFFICIAL, export_report3.TEMPLATE_NAME)
        with TemporaryDirectory() as temp:
            output = Path(temp) / export_report3.TEMPLATE_NAME
            export_report3.export(template, REPORTS, output)
            document = Package(output).xml("word/document.xml")
            for table in descendants(document, "tbl"):
                grid_cols = [int(c.getAttribute("w:w") or 0) for c in descendants(table, "gridCol")]
                self.assertTrue(grid_cols, "every table must define tblGrid columns")
                self.assertGreaterEqual(grid_cols[-1], 1100, f"crushed final column in {grid_cols}")
                for tcw in descendants(table, "tcW"):
                    self.assertNotEqual(tcw.getAttribute("w:type"), "pct")


if __name__ == "__main__":
    unittest.main()
