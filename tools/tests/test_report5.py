import tempfile
import unittest
from pathlib import Path
from zipfile import ZipFile

from support import OFFICIAL, REPORTS, original
from export_report5 import TEMPLATE_NAME, export, validate_cases
from report_ooxml import Spreadsheet, sha256


class Report5Tests(unittest.TestCase):
    def test_repeated_round_fields_remain_positional(self):
        cases, _, summaries, historical_round1_counts = validate_cases(REPORTS / "report-5-test-report")
        self.assertEqual(dict(historical_round1_counts), {"Passed": 45, "Pending": 8, "N/A": 3})
        # WF3-002 is FE-15, so it lands on the sheet for feature 15.
        row = next(row for _, row, _ in cases["Feature 15"] if row[0] == "WF3-002")
        self.assertEqual(len(row), 15)
        self.assertEqual(row[5:8], ["Passed", "2026-11-16", "Antigravity (automated)"])
        self.assertEqual(row[8:14], ["Pending", "", "", "Pending", "", ""])
        for case_id in ("WF3-006", "WF3-016"):
            case_row = next(row for _, row, _ in cases["Feature 18"] if row[0] == case_id)
            self.assertEqual(case_row[5:8][0], "Passed")
            self.assertEqual(case_row[8:11], ["Pending", "", ""])
            self.assertEqual(case_row[11:14], ["Passed", "2026-11-03", "Claude Code (automated)"])
        self.assertEqual(summaries["Feature 15"]["B2"],
                         "Field Evidence Intake & Chunked Video Processing Pipeline")

    def test_workbook_has_correct_metadata_rounds_styles_and_calculation_chain(self):
        template = original(OFFICIAL, TEMPLATE_NAME)
        initial_hash = sha256(template.read_bytes())
        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp) / TEMPLATE_NAME
            result = export(template, REPORTS, output)
            self.assertEqual(result["cases"], 80)
            self.assertTrue(result["format_parts_preserved"])
            book, source = Spreadsheet(output), Spreadsheet(template)
            self.assertEqual(list(book.sheets)[:5],
                             ["Cover", "Test Cases", "Test Statistics", "Feature 1", "Feature 2"])
            self.assertEqual(book.value("Feature 15", "B2"),
                             "Field Evidence Intake & Chunked Video Processing Pipeline")
            for coord, expected in {"G12": "2026-11-16", "H12": "Antigravity (automated)",
                                    "J12": "", "K12": "", "M12": "", "N12": "",
                                    "B4": "5", "B6": "1", "B7": "0", "D7": "5", "D8": "5"}.items():
                self.assertEqual(book.value("Feature 15", coord), expected, coord)
            self.assertTrue(book.value("Feature 15", "A11").startswith("FE-15"))
            self.assertEqual(book.value("Feature 15", "A12"), "WF3-002")
            self.assertEqual(book.value("Feature 15", "A13"), "WF3-022")
            self.assertEqual(book.value("Feature 15", "F13"), "N/A")
            self.assertEqual(book.value("Feature 16", "A16"), "WF3-008")
            self.assertEqual(book.value("Feature 16", "A18"), "WF3-017")
            self.assertEqual(book.value("Feature 16", "F18"), "Pending")
            self.assertEqual(book.value("Feature 16", "I18"), "Pending")
            self.assertEqual(book.value("Feature 16", "L18"), "Pending")
            self.assertEqual(book.value("Feature 18", "A13"), "WF3-006")
            self.assertEqual(book.value("Feature 18", "L13"), "Passed")
            self.assertEqual(book.value("Feature 18", "A14"), "WF3-009")
            self.assertEqual(book.value("Feature 19", "A12"), "WF3-012")
            self.assertEqual(book.value("Feature 19", "F12"), "Pending")
            self.assertEqual(book.value("Feature 20", "A13"), "WF3-019")
            self.assertEqual(book.value("Feature 20", "F13"), "N/A")
            self.assertEqual(book.value("Feature 20", "I13"), "N/A")
            self.assertEqual(book.value("Feature 20", "L13"), "Passed")
            self.assertEqual(book.value("Feature 5", "A12"), "WF3-032")
            self.assertEqual(book.value("Feature 5", "F12"), "N/A")
            self.assertEqual(book.value("Feature 5", "I12"), "Pending")
            self.assertEqual(book.value("Feature 5", "L12"), "Pending")
            self.assertEqual(book.value("Feature 11", "A12"), "WF2-021")
            for sheet, row, case_id in (
                ("Feature 11", 13, "WF2-032"),
                ("Feature 13", 17, "WF2-033"),
                ("Feature 9", 18, "WF2-034"),
            ):
                self.assertEqual(book.value(sheet, f"A{row}"), case_id)
                self.assertEqual(book.value(sheet, f"F{row}"), "N/A")
                self.assertEqual(book.value(sheet, f"L{row}"), "Passed")
            self.assertEqual(book.value("Feature 22", "A12"), "WF3-033")
            self.assertEqual(book.value("Test Statistics", "H35"), "80")
            self.assertEqual(book.value("Test Statistics", "D35"), "52")
            self.assertEqual(book.value("Test Statistics", "F35"), "9")
            self.assertEqual(book.value("Test Statistics", "G35"), "19")
            self.assertEqual(book.value("Test Statistics", "H36"), "56")
            self.assertEqual(book.value("Test Statistics", "D36"), "45")
            self.assertEqual(book.value("Test Statistics", "F36"), "8")
            self.assertEqual(book.value("Test Statistics", "H37"), "16")
            self.assertEqual(book.value("Test Statistics", "D37"), "16")
            self.assertEqual(book.value("Test Statistics", "C36"), "Historical Round 1")
            self.assertEqual(book.value("Test Statistics", "C37"), "Round 3 executed")
            self.assertEqual(book.value("Test Statistics", "C38"), "V29 Round 3")
            self.assertEqual(book.value("Test Statistics", "H38"), "2")
            self.assertEqual(book.value("Test Statistics", "D38"), "2")
            self.assertEqual(book.value("Test Statistics", "F38"), "0")
            self.assertEqual(book.value("Test Statistics", "G38"), "0")
            self.assertAlmostEqual(float(book.value("Test Statistics", "E40")), 52 / 61 * 100, places=2)
            self.assertAlmostEqual(float(book.value("Test Statistics", "E41")), 52 / 61 * 100, places=2)
            self.assertEqual(book.value("Cover", "E4"), "Creator")
            self.assertEqual(book.value("Test Statistics", "C3"), "SmartDroneInspection")
            self.assertNotIn("<List enviroment", book.value("Test Cases", "D5"))
            self.assertEqual(book.cell("Feature 15", "C12").getAttribute("s"),
                             source.cell("Feature 2", "C12").getAttribute("s"))
            self.assertEqual(book.cell("Feature 15", "C13").getAttribute("s"),
                             source.cell("Feature 2", "C12").getAttribute("s"))
            self.assertEqual(book.cell("Feature 15", "A11").getAttribute("s"),
                             source.cell("Feature 2", "A11").getAttribute("s"))
            with ZipFile(template) as original_zip, ZipFile(output) as output_zip:
                for part in ("xl/styles.xml", "xl/sharedStrings.xml", "xl/theme/theme1.xml"):
                    self.assertEqual(original_zip.read(part), output_zip.read(part), part)
                self.assertNotIn("xl/calcChain.xml", output_zip.namelist())
                self.assertNotIn(b"calcChain", output_zip.read("xl/_rels/workbook.xml.rels"))
        self.assertEqual(sha256(template.read_bytes()), initial_hash)


if __name__ == "__main__":
    unittest.main()
