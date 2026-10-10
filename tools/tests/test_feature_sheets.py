"""Report 5 must expose one workbook sheet per Report 3 feature.

The supplied template ships two ``Feature N`` sheets. Report 3 defines eight
product features (FE-01..FE-08, sections 3.2-3.9), so the generated workbook
carries eight feature sheets, ``Feature 1``..``Feature 8``, where sheet *N*
tests feature ``FE-0N``.

This is a deliberate generated-output extension requested for this report. The
supplied source template remains unchanged; the generator writes a separate copy.
"""
import re
import tempfile
import unittest
from pathlib import Path

from support import OFFICIAL, REPORTS, original
from export_report5 import FEATURE_SHEETS, TEMPLATE_NAME, export
from report_ooxml import Spreadsheet, descendants, find_table, plain

SHEET_COUNT = 8


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

    def test_sheets_without_cases_are_present_and_empty_not_missing(self):
        book, temp = generated_workbook()
        with temp:
            # FE-03 and FE-04 through FE-06 carry cases today.
            for sheet in ("Feature 1", "Feature 2", "Feature 7", "Feature 8"):
                self.assertEqual(book.value(sheet, "B4"), "0",
                                 f"{sheet} should report zero test cases")
                self.assertEqual(book.value(sheet, "B6"), "0", sheet)

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
            # Two MF2-07 cases belong to FE-03; five MF3 cases belong to FE-04–FE-06.
            self.assertEqual(len(counts["Feature 3"]), 2)
            self.assertCountEqual(counts["Feature 3"], ["WF2-008", "WF2-009"])
            self.assertEqual(len(counts["Feature 4"]), 2)
            self.assertEqual(len(counts["Feature 5"]), 1)
            self.assertEqual(len(counts["Feature 6"]), 2)
            self.assertEqual(sum(len(v) for v in counts.values()), 7)

    def test_statistics_lists_all_eight_modules_with_a_correct_subtotal(self):
        book, temp = generated_workbook()
        with temp:
            stats = "Test Statistics"
            for number, sheet in enumerate(FEATURE_SHEETS, 1):
                row = 10 + number
                self.assertEqual(book.value(stats, f"C{row}"), book.value(sheet, "B2"))
                self.assertEqual(book.value(stats, f"B{row}"), str(number))
            self.assertEqual(book.value(stats, "H19"), "7")
            self.assertEqual(book.value(stats, "D19"), "7")
            # Eight modules push Sub total to row 19 and coverage to rows 21/22.
            self.assertEqual(book.value(stats, "C19"), "Sub total")
            self.assertEqual(book.value(stats, "C21"), "Test coverage")
            self.assertEqual(book.value(stats, "E21"), "100.0")
            self.assertEqual(book.value(stats, "E22"), "100.0")


if __name__ == "__main__":
    unittest.main()