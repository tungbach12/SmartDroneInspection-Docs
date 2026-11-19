"""Report 5 must expose one workbook sheet per Report 3 feature (FE-01..FE-08)."""
import re
import tempfile
import unittest
from pathlib import Path

from support import OFFICIAL, REPORTS, original
from export_report5 import FEATURE_SHEETS, TEMPLATE_NAME, export
from report_ooxml import Spreadsheet, descendants, find_table, plain

SHEET_COUNT = 8
EXPECTED_CASE_COUNTS = {"Feature 1": 8, "Feature 2": 7, "Feature 3": 8, "Feature 4": 8,
                       "Feature 5": 7, "Feature 6": 14, "Feature 7": 5, "Feature 8": 7}


def generated_workbook():
    template = original(OFFICIAL, TEMPLATE_NAME)
    temp = tempfile.TemporaryDirectory()
    output = Path(temp.name) / TEMPLATE_NAME
    export(template, REPORTS, output)
    return Spreadsheet(output), temp


class FeatureSheetTests(unittest.TestCase):
    def test_workbook_has_one_sheet_per_report3_feature(self):
        book, temp = generated_workbook()
        with temp:
            names = list(book.sheets)
            self.assertEqual(names[:3], ["Cover", "Test Cases", "Test Statistics"])
            self.assertEqual(names[3:], [f"Feature {n}" for n in range(1, SHEET_COUNT + 1)])
            self.assertEqual(len(names[3:]), SHEET_COUNT)

    def test_each_sheet_names_its_own_report3_feature(self):
        book, temp = generated_workbook()
        with temp:
            for number, sheet in enumerate(FEATURE_SHEETS, 1):
                label = book.value(sheet, "B2")
                self.assertTrue(label, f"{sheet} has no Feature name in B2")
                self.assertNotIn("<", label, f"{sheet} still shows the template placeholder")

    def test_every_fe_source_has_its_own_matching_summary_block(self):
        feature_dir = REPORTS / "report-5-test-report/03-features"
        sources = sorted(feature_dir.glob("fe-*.md"))
        self.assertEqual(len(sources), SHEET_COUNT)
        for number, source in enumerate(sources, 1):
            summary = find_table(source, "Cell")
            self.assertEqual(summary[0], ["Cell", "Label", "Value"], source.name)
            values = {plain(row[0]): plain(row[2]) for row in summary[1:]}
            self.assertIn("B2", values, f"{source.name} has no Feature summary")
            self.assertIn("B3", values, f"{source.name} has no Test requirement")
            self.assertNotIn("<", values["B2"], source.name)
            self.assertNotIn("<", values["B3"], source.name)

    def test_all_eight_sheets_are_populated(self):
        book, temp = generated_workbook()
        with temp:
            for sheet in FEATURE_SHEETS:
                self.assertEqual(book.value(sheet, "B4"), str(EXPECTED_CASE_COUNTS[sheet]), sheet)
                self.assertGreaterEqual(int(book.value(sheet, "B4")), 4, sheet)

    def test_case_ids_land_on_the_sheet_matching_their_feature(self):
        book, temp = generated_workbook()
        with temp:
            counts = {}
            for sheet in FEATURE_SHEETS:
                data = descendants(book.sheet(sheet), "sheetData")[0]
                ids = []
                for row in data.getElementsByTagName("row"):
                    if int(row.getAttribute("r")) < 12:
                        continue
                    for cell in row.getElementsByTagName("c"):
                        ref = cell.getAttribute("r")
                        if re.fullmatch(r"A\d+", ref):
                            value = book.value(sheet, ref)
                            if re.fullmatch(r"WF\d-\d{3}", value or ""):
                                ids.append(value)
                counts[sheet] = ids
                self.assertEqual(len(ids), EXPECTED_CASE_COUNTS[sheet], sheet)
            self.assertIn("WF1-001", counts["Feature 1"])
            self.assertIn("WF1-006", counts["Feature 2"])
            self.assertIn("WF1-015", counts["Feature 2"])
            self.assertIn("WF1-011", counts["Feature 3"])
            self.assertIn("WF1-017", counts["Feature 3"])
            self.assertIn("WF1-009", counts["Feature 3"])
            self.assertIn("WF2-001", counts["Feature 4"])
            self.assertIn("WF1-021", counts["Feature 4"])
            self.assertIn("WF2-008", counts["Feature 5"])
            self.assertIn("WF3-020", counts["Feature 5"])
            for case_id in ("WF3-001", "WF3-002", "WF3-010", "WF3-017",
                            "WF3-022", "WF3-023", "WF3-024", "WF3-025", "WF3-029"):
                self.assertIn(case_id, counts["Feature 6"])
            for case_id in ("WF3-005", "WF3-006", "WF3-016", "WF3-030"):
                self.assertIn(case_id, counts["Feature 7"])
            for case_id in ("WF3-018", "WF3-019", "WF3-021", "WF3-031"):
                self.assertIn(case_id, counts["Feature 8"])
            self.assertEqual(sum(len(v) for v in counts.values()), 64)

    def test_statistics_lists_all_eight_modules_with_a_correct_subtotal(self):
        book, temp = generated_workbook()
        with temp:
            stats = "Test Statistics"
            for number, sheet in enumerate(FEATURE_SHEETS, 1):
                row = 10 + number
                self.assertEqual(book.value(stats, f"C{row}"), book.value(sheet, "B2"))
                self.assertEqual(book.value(stats, f"B{row}"), str(number))
            self.assertEqual(book.value(stats, "H19"), "64")
            self.assertEqual(book.value(stats, "D19"), "45")
            self.assertEqual(book.value(stats, "E19"), "0")
            self.assertEqual(book.value(stats, "F19"), "9")
            self.assertEqual(book.value(stats, "G19"), "10")
            self.assertEqual(book.value(stats, "C19"), "Sub total")
            self.assertEqual(book.value(stats, "C20"), "Historical Round 1")
            self.assertEqual(book.value(stats, "D20"), "45")
            self.assertEqual(book.value(stats, "F20"), "8")
            self.assertEqual(book.value(stats, "G20"), "3")
            self.assertEqual(book.value(stats, "H20"), "56")
            self.assertEqual(book.value(stats, "C21"), "Round 3 executed")
            self.assertEqual(book.value(stats, "D21"), "13")
            self.assertEqual(book.value(stats, "H21"), "13")
            self.assertEqual(book.value(stats, "C22"), "V29 Round 3")
            self.assertEqual(book.value(stats, "D22"), "2")
            self.assertEqual(book.value(stats, "F22"), "0")
            self.assertEqual(book.value(stats, "G22"), "0")
            self.assertEqual(book.value(stats, "H22"), "2")
            self.assertEqual(book.value(stats, "C24"), "Test coverage")
            self.assertEqual(book.value(stats, "C25"), "Test successful coverage")
            self.assertAlmostEqual(float(book.value(stats, "E24")), 45 / 54 * 100, places=2)
            self.assertAlmostEqual(float(book.value(stats, "E25")), 45 / 54 * 100, places=2)

if __name__ == "__main__":
    unittest.main()
