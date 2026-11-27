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
                expected_sheets = ["Cover", "Functions", "Statistics"] + [f"Function {i}" for i in range(1, 15)]
                self.assertEqual(names, expected_sheets)

                cover = sheet_cells(zf, "xl/worksheets/sheet1.xml")
                functions = sheet_cells(zf, "xl/worksheets/sheet2.xml")
                stats = sheet_cells(zf, "xl/worksheets/sheet3.xml")
                self.assertEqual(cover["F5"][0], "Phạm Minh Trí")
                self.assertEqual(stats["G5"][0], "Phạm Minh Trí")
                self.assertEqual(stats["D27"][1], "SUM(D12:D25)")
                self.assertEqual(stats["J27"][1], "SUM(J12:J25)")

                for idx in range(1, 15):
                    row = 10 + idx
                    _, link_f = functions[f"F{row}"]
                    self.assertIn("HYPERLINK", link_f or "")
                    self.assertIn(f"Function {idx}", link_f or "")

                    fn_cells = sheet_cells(zf, f"xl/worksheets/sheet{3 + idx}.xml")
                    self.assertTrue((fn_cells["A7"][1] or "").startswith("COUNTIF("))
                    self.assertTrue((fn_cells["O7"][1] or "").startswith("COUNTA("))
                    self.assertIn(fn_cells["C3"][0], export_report5_unit.ALLOWED_TESTERS)
                    self.assertIn(fn_cells["L3"][0], export_report5_unit.ALLOWED_TESTERS)

                    stat_row = 11 + idx
                    self.assertEqual(stats[f"D{stat_row}"][1], f"'Function {idx}'!A7")
                    self.assertEqual(stats[f"J{stat_row}"][1], f"'Function {idx}'!O7")

                for name in zf.namelist():
                    if name.startswith("xl/worksheets/sheet"):
                        txt = zf.read(name).decode("utf-8")
                        self.assertNotIn("Claude", txt)
                        self.assertNotIn("Codex", txt)
                        self.assertNotIn("Antigravity", txt)


if __name__ == "__main__":
    unittest.main()
