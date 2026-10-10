import tempfile
import unittest
from pathlib import Path
from zipfile import ZipFile

from support import OFFICIAL, REPORTS, original
from export_report5 import TEMPLATE_NAME, export, validate_cases
from report_ooxml import Spreadsheet, sha256


class Report5Tests(unittest.TestCase):
    def test_repeated_round_fields_remain_positional(self):
        cases, _, summaries = validate_cases(REPORTS / "report-5-test-report")
        # WF3-002 is FE-04, so it lands on the sheet for feature 4.
        row = next(row for _, row, _ in cases["Feature 4"] if row[0] == "WF3-002")
        self.assertEqual(len(row), 15)
        self.assertEqual(row[5:8], ["Passed", "2026-10-08", "Claude Code (automated)"])
        self.assertEqual(row[8:14], ["Pending", "", "", "Pending", "", ""])
        self.assertEqual(summaries["Feature 4"]["B2"], "MF3 inspection evidence, findings and reporting")

    def test_workbook_has_correct_metadata_rounds_styles_and_calculation_chain(self):
        template = original(OFFICIAL, TEMPLATE_NAME)
        initial_hash = sha256(template.read_bytes())
        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp) / TEMPLATE_NAME
            result = export(template, REPORTS, output)
            self.assertEqual(result["cases"], 7)
            self.assertTrue(result["format_parts_preserved"])
            book, source = Spreadsheet(output), Spreadsheet(template)
            self.assertEqual(list(book.sheets)[:5],
                             ["Cover", "Test Cases", "Test Statistics", "Feature 1", "Feature 2"])
            self.assertEqual(book.value("Feature 4", "B2"),
                             "MF3 inspection evidence, findings and reporting")
            for coord, expected in {"G12": "2026-10-08", "H12": "Claude Code (automated)",
                                    "J12": "", "K12": "", "M12": "", "N12": "",
                                    "B4": "2", "B6": "2", "B7": "0", "D7": "2", "D8": "2"}.items():
                self.assertEqual(book.value("Feature 4", coord), expected, coord)
            # One FE per sheet, so each sheet opens with a single function bar
            # at row 11 followed by its case rows.
            self.assertTrue(book.value("Feature 4", "A11").startswith("FE-04"))
            self.assertEqual(book.value("Feature 4", "A12"), "WF3-002")
            self.assertEqual(book.value("Test Statistics", "H19"), "7")
            self.assertEqual(book.value("Test Statistics", "E21"), "100.0")
            self.assertEqual(book.value("Cover", "E4"), "Creator")
            self.assertEqual(book.value("Test Statistics", "C3"), "SmartDroneInspection")
            self.assertNotIn("<List enviroment", book.value("Test Cases", "D5"))
            self.assertEqual(book.cell("Feature 4", "C12").getAttribute("s"),
                             source.cell("Feature 2", "C12").getAttribute("s"))
            self.assertEqual(book.cell("Feature 4", "C13").getAttribute("s"),
                             source.cell("Feature 2", "C12").getAttribute("s"))
            self.assertEqual(book.cell("Feature 4", "A11").getAttribute("s"),
                             source.cell("Feature 2", "A11").getAttribute("s"))
            with ZipFile(template) as original_zip, ZipFile(output) as output_zip:
                for part in ("xl/styles.xml", "xl/sharedStrings.xml", "xl/theme/theme1.xml"):
                    self.assertEqual(original_zip.read(part), output_zip.read(part), part)
                self.assertNotIn("xl/calcChain.xml", output_zip.namelist())
                self.assertNotIn(b"calcChain", output_zip.read("xl/_rels/workbook.xml.rels"))
        self.assertEqual(sha256(template.read_bytes()), initial_hash)


if __name__ == "__main__":
    unittest.main()
