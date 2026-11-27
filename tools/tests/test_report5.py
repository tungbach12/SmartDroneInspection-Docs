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
        self.assertEqual(row[5:8], ["Passed", "2026-11-16", "Trần Tùng Bách"])
        self.assertEqual(row[8:11], ["Pending", "", ""])
        self.assertEqual(row[11:14], ["Passed", "2026-11-26", "Trần Tùng Bách"])
        for case_id in ("WF3-006", "WF3-016"):
            case_row = next(row for _, row, _ in cases["Feature 18"] if row[0] == case_id)
            self.assertEqual(case_row[5:8][0], "Passed")
            self.assertEqual(case_row[8:11], ["Pending", "", ""])
            self.assertEqual(case_row[11:14], ["Passed", "2026-11-03", "Trần Tùng Bách"])
        self.assertEqual(summaries["Feature 15"]["B2"],
                         "Field Evidence Intake & Chunked Video Processing Pipeline")

    def test_workbook_has_correct_metadata_rounds_styles_and_calculation_chain(self):
        template = original(OFFICIAL, TEMPLATE_NAME)
        initial_hash = sha256(template.read_bytes())
        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp) / TEMPLATE_NAME
            result = export(template, REPORTS, output)
            self.assertEqual(result["cases"], 90)
            self.assertTrue(result["format_parts_preserved"])
            book, source = Spreadsheet(output), Spreadsheet(template)
            self.assertEqual(list(book.sheets)[:5],
                             ["Cover", "Test Cases", "Test Statistics", "Feature 1", "Feature 2"])
            self.assertEqual(book.value("Feature 15", "B2"),
                             "Field Evidence Intake & Chunked Video Processing Pipeline")
            for coord, expected in {"G12": "2026-11-16", "H12": "Trần Tùng Bách",
                                    "J12": "", "K12": "", "M12": "2026-11-26", "N12": "Trần Tùng Bách",
                                    "B4": "5", "B6": "1", "B7": "0", "B8": "5", "D7": "5", "D8": "0"}.items():
                self.assertEqual(book.value("Feature 15", coord), expected, coord)
            self.assertTrue(book.value("Feature 15", "A11").startswith("FE-15"))
            self.assertEqual(book.value("Feature 15", "A12"), "WF3-002")
            self.assertEqual(book.value("Feature 15", "A13"), "WF3-022")
            self.assertEqual(book.value("Feature 15", "F13"), "N/A")
            self.assertEqual(book.value("Feature 16", "A16"), "WF3-008")
            self.assertEqual(book.value("Feature 16", "A18"), "WF3-017")
            self.assertEqual(book.value("Feature 16", "F18"), "Pending")
            self.assertEqual(book.value("Feature 16", "I18"), "Pending")
            self.assertEqual(book.value("Feature 16", "L18"), "Passed")
            self.assertEqual(book.value("Feature 18", "A13"), "WF3-006")
            self.assertEqual(book.value("Feature 18", "L13"), "Passed")
            self.assertEqual(book.value("Feature 18", "A14"), "WF3-009")
            self.assertEqual(book.value("Feature 19", "A12"), "WF3-012")
            self.assertEqual(book.value("Feature 19", "F12"), "Pending")
            self.assertEqual(book.value("Feature 19", "L12"), "Passed")
            self.assertEqual(book.value("Feature 20", "A13"), "WF3-019")
            self.assertEqual(book.value("Feature 20", "F13"), "N/A")
            self.assertEqual(book.value("Feature 20", "I13"), "N/A")
            self.assertEqual(book.value("Feature 20", "L13"), "Passed")
            self.assertEqual(book.value("Feature 5", "A12"), "WF3-032")
            self.assertEqual(book.value("Feature 5", "F12"), "N/A")
            self.assertEqual(book.value("Feature 5", "I12"), "Pending")
            self.assertEqual(book.value("Feature 5", "L12"), "Passed")
            self.assertEqual(book.value("Feature 13", "L12"), "N/A")
            self.assertEqual(book.value("Feature 9", "L15"), "N/A")
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
            self.assertEqual(book.value("Test Statistics", "G4"), "Phạm Minh Trí")
            self.assertEqual(book.value("Test Statistics", "H35"), "90")
            self.assertEqual(book.value("Test Statistics", "D35"), "87")
            self.assertEqual(book.value("Test Statistics", "F35"), "0")
            self.assertEqual(book.value("Test Statistics", "G35"), "3")
            self.assertEqual(book.value("Test Statistics", "H36"), "56")
            self.assertEqual(book.value("Test Statistics", "D36"), "45")
            self.assertEqual(book.value("Test Statistics", "F36"), "8")
            self.assertEqual(book.value("Test Statistics", "H37"), "87")
            self.assertEqual(book.value("Test Statistics", "D37"), "87")
            self.assertEqual(book.value("Test Statistics", "C36"), "Historical Round 1")
            self.assertEqual(book.value("Test Statistics", "C37"), "Round 3 executed")
            self.assertEqual(book.value("Test Statistics", "C38"), "V29 Round 3")
            self.assertEqual(book.value("Test Statistics", "H38"), "2")
            self.assertEqual(book.value("Test Statistics", "D38"), "2")
            self.assertEqual(book.value("Test Statistics", "F38"), "0")
            self.assertEqual(book.value("Test Statistics", "G38"), "0")
            self.assertAlmostEqual(float(book.value("Test Statistics", "E40")), 100.0, places=2)
            self.assertAlmostEqual(float(book.value("Test Statistics", "E41")), 100.0, places=2)
            self.assertEqual(book.value("Cover", "E4"), "Creator")
            self.assertEqual(book.value("Test Statistics", "C3"), "SmartDroneInspection")
            self.assertNotIn("<List enviroment", book.value("Test Cases", "D5"))
            self.assertEqual(book.cell("Feature 15", "C12").getAttribute("s"), "42")
            self.assertEqual(book.cell("Feature 15", "C13").getAttribute("s"), "42")
            self.assertEqual(book.cell("Feature 15", "A11").getAttribute("s"),
                             source.cell("Feature 2", "A11").getAttribute("s"))
            self.assertEqual(book.cell("Test Cases", "C9").getAttribute("s"), "42")
            self.assertEqual(book.cell("Test Cases", "D9").getAttribute("s"), "101")
            self.assertEqual(book.cell("Test Cases", "E9").getAttribute("s"), "42")
            self.assertEqual(book.cell("Test Cases", "F9").getAttribute("s"), "42")
            self.assertEqual(book.cell("Test Statistics", "C11").getAttribute("s"), "42")
            cases, _, _, _ = validate_cases(REPORTS / "report-5-test-report")
            for sheet_grp in cases.values():
                for _, row, _ in sheet_grp:
                    self.assertTrue(row[2].startswith("1. "), f"Missing step numbering in {row[0]}")
                    self.assertNotRegex(row[2], r"(?<!^)(?<!<br>)\s+\d+\.\s+", f"Unsplit step in {row[0]}")
                    self.assertLessEqual(len(row[14]), 140, f"Note too long on {row[0]}: {row[14]}")
            with ZipFile(template) as original_zip, ZipFile(output) as output_zip:
                for part in ("xl/styles.xml", "xl/sharedStrings.xml", "xl/theme/theme1.xml"):
                    self.assertEqual(original_zip.read(part), output_zip.read(part), part)
                self.assertNotIn("xl/calcChain.xml", output_zip.namelist())
                self.assertNotIn(b"calcChain", output_zip.read("xl/_rels/workbook.xml.rels"))
                for part in output_zip.namelist():
                    if part.startswith("xl/worksheets/sheet"):
                        txt = output_zip.read(part).decode("utf-8")
                        for forbidden in ("Claude", "Codex", "Antigravity", "Pham Trung Quoc"):
                            self.assertNotIn(forbidden, txt, f"{forbidden} found in {part}")
        self.assertEqual(sha256(template.read_bytes()), initial_hash)


if __name__ == "__main__":
    unittest.main()
