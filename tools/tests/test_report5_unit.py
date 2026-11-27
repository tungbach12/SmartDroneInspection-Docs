import re
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path

TOOLS = Path(__file__).resolve().parents[1]
REPORTS = TOOLS.parent / "reports"
OFFICIAL = Path(r"E:\Dev\Repos\Capstone\capstone-official-docs")
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

import export_report5_unit  # noqa: E402

NS = {"s": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}


def sheet_cells(zf: zipfile.ZipFile, sheet_path: str) -> dict[str, tuple[str | None, str | None]]:
    root = ET.fromstring(zf.read(sheet_path))
    out: dict[str, tuple[str | None, str | None]] = {}
    for c in root.findall(".//s:c", NS):
        ref = c.attrib["r"]
        f = c.findtext("s:f", default=None, namespaces=NS)
        v = c.findtext("s:v", default=None, namespaces=NS)
        if v is None:
            v = c.findtext("s:is/s:t", default=None, namespaces=NS)
        out[ref] = (v, f)
    return out


class Report5UnitExportTests(unittest.TestCase):
    def test_unit_test_workbook_exports_code_backed_sheets_and_formulas(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / export_report5_unit.OUTPUT_NAME
            result = export_report5_unit.export(OFFICIAL / "2_SEP490" / "Report5_Unit Test.xls", REPORTS, out)
            self.assertEqual(result["warnings"], [])
            self.assertEqual(result["functions"], 14)
            self.assertEqual(result["cases"], 202)
            with zipfile.ZipFile(out, "r") as zf:
                wb_root = ET.fromstring(zf.read("xl/workbook.xml"))
                names = [el.attrib["name"] for el in wb_root.findall(".//s:sheet", NS)]
                expected_sheets = ["Guideline", "Cover", "Functions", "Statistics"] + [
                    f"Function {i}" for i in range(1, 15)
                ]
                self.assertEqual(names, expected_sheets)
                self.assertIn("xl/media/image1.png", zf.namelist())
                self.assertNotIn("xl/calcChain.xml", zf.namelist())

                cover = sheet_cells(zf, "xl/worksheets/sheet2.xml")
                functions = sheet_cells(zf, "xl/worksheets/sheet3.xml")
                stats = sheet_cells(zf, "xl/worksheets/sheet4.xml")
                self.assertEqual(cover["B4"][0], "SmartDroneInspection")
                self.assertEqual(stats["F4"][0], "Trần Tùng Bách")
                self.assertEqual(stats["F5"][0], "Phạm Minh Trí")
                self.assertEqual(stats["C27"][1], "SUM(C12:C25)")
                self.assertEqual(stats["I27"][1], "SUM(I12:I25)")

                # Pie charts must point at Sub total row 27 and contain zero #REF!
                for chart_part in ("xl/charts/chart1.xml", "xl/charts/chart2.xml"):
                    ctxt = zf.read(chart_part).decode("utf-8")
                    self.assertNotIn("#REF!", ctxt, chart_part)
                    self.assertIn("$27", ctxt, chart_part)

                for idx in range(1, 15):
                    row = 10 + idx
                    _, link_f = functions[f"F{row}"]
                    self.assertIn("HYPERLINK", link_f or "")
                    self.assertIn(f"Function {idx}", link_f or "")

                    stat_row = 11 + idx
                    self.assertEqual(stats[f"C{stat_row}"][1], f"'Function {idx}'!A7")
                    self.assertEqual(stats[f"I{stat_row}"][1], f"'Function {idx}'!O7")

                # Verify Function 1 and Function 2 matrix markers and zero dummy DFIDs
                f1_txt = zf.read("xl/worksheets/sheet5.xml").decode("utf-8")
                self.assertNotIn("DFID", f1_txt)
                self.assertIn("UTCID01", f1_txt)

                for name in zf.namelist():
                    if name.startswith("xl/worksheets/sheet"):
                        txt = zf.read(name).decode("utf-8")
                        self.assertNotIn("Claude", txt)
                        self.assertNotIn("Codex", txt)
                        self.assertNotIn("Antigravity", txt)


if __name__ == "__main__":
    unittest.main()
