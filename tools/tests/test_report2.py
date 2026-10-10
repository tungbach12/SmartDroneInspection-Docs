import unittest
from support import assert_word_export
import export_report2


class Report2Tests(unittest.TestCase):
    def test_all_management_tables_and_official_format(self):
        result = assert_word_export(self, export_report2)
        self.assertEqual(result["tables"], 9)
        self.assertEqual(result["source_images"], 1)
        self.assertEqual(result["warnings"], [])


if __name__ == "__main__":
    unittest.main()
