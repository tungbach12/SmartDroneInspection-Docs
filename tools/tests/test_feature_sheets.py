"""Report 5 must expose one workbook sheet per Report 3 feature (FE-01..FE-24)."""
import re
import tempfile
import unittest
from pathlib import Path

from support import OFFICIAL, REPORTS, original
from export_report5 import FEATURE_SHEETS, TEMPLATE_NAME, export
from report_ooxml import Spreadsheet, descendants, find_table, plain

SHEET_COUNT = 24
EXPECTED_CASE_COUNTS = {
    "Feature 1": 7, "Feature 2": 4, "Feature 3": 3, "Feature 4": 3,
    "Feature 5": 2, "Feature 6": 3, "Feature 7": 2, "Feature 8": 6,
    "Feature 9": 7, "Feature 10": 3, "Feature 11": 2, "Feature 12": 3,
    "Feature 13": 6, "Feature 14": 5, "Feature 15": 5, "Feature 16": 7,
    "Feature 17": 3, "Feature 18": 4, "Feature 19": 2, "Feature 20": 3,
    "Feature 21": 3, "Feature 22": 2, "Feature 23": 2, "Feature 24": 3,
}


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

    def test_all_twenty_four_sheets_are_populated(self):
        book, temp = generated_workbook()
        with temp:
            for sheet in FEATURE_SHEETS:
                self.assertEqual(book.value(sheet, "B4"), str(EXPECTED_CASE_COUNTS[sheet]), sheet)
                self.assertGreaterEqual(int(book.value(sheet, "B4")), 1, sheet)

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
            self.assertIn("WF1-015", counts["Feature 3"])
            self.assertIn("WF1-002", counts["Feature 4"])
            self.assertIn("WF2-004", counts["Feature 4"])
            self.assertIn("WF3-032", counts["Feature 5"])
            self.assertIn("WF1-011", counts["Feature 6"])
            self.assertIn("WF1-009", counts["Feature 7"])
            self.assertIn("WF1-017", counts["Feature 8"])
            self.assertIn("WF1-021", counts["Feature 9"])
            self.assertIn("WF2-001", counts["Feature 10"])
            self.assertIn("WF2-021", counts["Feature 11"])
            self.assertIn("WF1-020", counts["Feature 12"])
            self.assertIn("WF2-008", counts["Feature 13"])
            self.assertIn("WF2-011", counts["Feature 14"])
            self.assertIn("WF3-020", counts["Feature 14"])
            for case_id in ("WF3-002", "WF3-022", "WF3-023", "WF3-024", "WF3-025"):
                self.assertIn(case_id, counts["Feature 15"])
            for case_id in ("WF3-001", "WF3-003", "WF3-008", "WF3-010", "WF3-017"):
                self.assertIn(case_id, counts["Feature 16"])
            for case_id in ("WF3-029", "WF3-030"):
                self.assertIn(case_id, counts["Feature 17"])
            for case_id in ("WF3-005", "WF3-006", "WF3-009", "WF3-016"):
                self.assertIn(case_id, counts["Feature 18"])
            self.assertIn("WF3-012", counts["Feature 19"])
            for case_id in ("WF3-018", "WF3-019"):
                self.assertIn(case_id, counts["Feature 20"])
            for case_id in ("WF3-026", "WF3-027"):
                self.assertIn(case_id, counts["Feature 21"])
            self.assertIn("WF3-033", counts["Feature 22"])
            self.assertIn("WF3-021", counts["Feature 23"])
            for case_id in ("WF3-028", "WF3-031"):
                self.assertIn(case_id, counts["Feature 24"])
            self.assertEqual(sum(len(v) for v in counts.values()), 90)

    def test_statistics_lists_all_twenty_four_modules_with_a_correct_subtotal(self):
        book, temp = generated_workbook()
        with temp:
            stats = "Test Statistics"
            for number, sheet in enumerate(FEATURE_SHEETS, 1):
                row = 10 + number
                self.assertEqual(book.value(stats, f"C{row}"), book.value(sheet, "B2"))
                self.assertEqual(book.value(stats, f"B{row}"), str(number))
            self.assertEqual(book.value(stats, "H35"), "90")
            self.assertEqual(book.value(stats, "D35"), "87")
            self.assertEqual(book.value(stats, "E35"), "0")
            self.assertEqual(book.value(stats, "F35"), "0")
            self.assertEqual(book.value(stats, "G35"), "3")
            self.assertEqual(book.value(stats, "C35"), "Sub total")
            self.assertEqual(book.value(stats, "C36"), "Historical Round 1")
            self.assertEqual(book.value(stats, "D36"), "45")
            self.assertEqual(book.value(stats, "F36"), "8")
            self.assertEqual(book.value(stats, "G36"), "3")
            self.assertEqual(book.value(stats, "H36"), "56")
            self.assertEqual(book.value(stats, "C37"), "Round 3 executed")
            self.assertEqual(book.value(stats, "D37"), "87")
            self.assertEqual(book.value(stats, "H37"), "87")
            self.assertEqual(book.value(stats, "C38"), "V29 Round 3")
            self.assertEqual(book.value(stats, "D38"), "2")
            self.assertEqual(book.value(stats, "F38"), "0")
            self.assertEqual(book.value(stats, "G38"), "0")
            self.assertEqual(book.value(stats, "H38"), "2")
            self.assertEqual(book.value(stats, "C40"), "Test coverage")
            self.assertEqual(book.value(stats, "C41"), "Test successful coverage")
            self.assertAlmostEqual(float(book.value(stats, "E40")), 100.0, places=2)
            self.assertAlmostEqual(float(book.value(stats, "E41")), 100.0, places=2)

if __name__ == "__main__":
    unittest.main()
