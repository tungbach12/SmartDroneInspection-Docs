import tempfile
import unittest
from pathlib import Path

from support import OFFICIAL, REPORTS, original
from export_weekly import TEMPLATE_NAME, export
from report_ooxml import Spreadsheet, parse_markdown, plain


class WeeklyTests(unittest.TestCase):
    def test_each_week_contains_all_table_data_and_original_sheet_name(self):
        template = original(OFFICIAL, TEMPLATE_NAME)
        for source in sorted((REPORTS / "weekly-project-reports").glob("week-*.md")):
            with self.subTest(week=source.stem), tempfile.TemporaryDirectory() as temp:
                output = Path(temp) / "week.xlsx"
                result = export(template, source, output)
                book = Spreadsheet(output)
                self.assertEqual(list(book.sheets), ["Wx"])
                self.assertEqual(book.value("Wx", "B2"), "FA26SE112")
                self.assertTrue(result["format_parts_preserved"])
                visible = " ".join(book.value("Wx", f"{col}{row}")
                                   for row in range(1, 100) for col in "ABCDE")
                count = 0
                for block in parse_markdown(source):
                    if block.kind == "table":
                        count += len(block.rows) - 1
                        for row in block.rows:
                            for cell in row:
                                self.assertIn(plain(cell), visible)
                self.assertEqual(result["source_rows"], count)


if __name__ == "__main__":
    unittest.main()
