import tempfile
import unittest
from pathlib import Path

from support import OFFICIAL, REPORTS, assert_word_export, original
import export_project_tracking
import export_report4
import export_report5_doc
from report_ooxml import Spreadsheet


class Report4And5DocTests(unittest.TestCase):
    def test_report4_sdd_exports_with_embedded_mermaid_diagrams_and_tables(self):
        result = assert_word_export(self, export_report4)
        self.assertGreaterEqual(result["tables"], 10)
        self.assertGreaterEqual(result["source_images"], 20)
        self.assertTrue(any("Mermaid" in w for w in result["warnings"]))

    def test_report5_documentation_preserves_merged_header_table_and_styles(self):
        result = assert_word_export(self, export_report5_doc)
        self.assertEqual(result["tables"], 6)
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
