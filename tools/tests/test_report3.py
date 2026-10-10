import unittest
from support import REPORTS, assert_word_export
import export_report3


class Report3Tests(unittest.TestCase):
    def test_seven_sections_and_source_diagrams_are_not_lost(self):
        self.assertEqual(len(export_report3.SOURCES), 7)
        result = assert_word_export(self, export_report3)
        self.assertGreater(result["tables"], 9)
        self.assertTrue(any("Mermaid" in warning for warning in result["warnings"]))

    def test_section_order_is_explicit(self):
        headings = [b.text for b in export_report3.blocks(REPORTS) if b.kind == "heading"]
        self.assertLess(headings.index("I. Record of Changes"), headings.index("I. Project Report"))
        self.assertLess(headings.index("I. Project Report"), headings.index("II. Software Requirement Specification"))


if __name__ == "__main__":
    unittest.main()
