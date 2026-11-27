import unittest
from support import REPORTS, assert_word_export
import export_report1


class Report1Tests(unittest.TestCase):
    def test_content_tables_images_and_official_format(self):
        result = assert_word_export(self, export_report1)
        self.assertEqual(result["tables"], 2)
        self.assertEqual(result["source_images"], 0)
        self.assertEqual(result["warnings"], [])
        headings = [
            b.text for b in export_report1.blocks(REPORTS)
            if b.kind == "heading" and b.level == 1
        ]
        self.assertEqual(headings, ["I. Record of Changes", "II. Project Introduction"])


if __name__ == "__main__":
    unittest.main()
