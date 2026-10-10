import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from zipfile import ZipFile

from support import OFFICIAL, REPORTS, original
from export_all import build
from report_ooxml import Package, plain, split_row

TOOLS = Path(__file__).resolve().parent.parent


class CommonTests(unittest.TestCase):
    def test_escaped_pipes_and_windows_paths_are_preserved(self):
        self.assertEqual(split_row(r"| A\|B | C:\work\file |"), ["A|B", r"C:\work\file"])

    def test_inline_markup_becomes_visible_text(self):
        self.assertEqual(plain("**Passed** `B2`<br>Next"), "Passed B2\nNext")

    def test_noop_preserves_every_original_package_member(self):
        template = original(OFFICIAL, "Report5_Test Report.xlsx")
        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp) / "clone.xlsx"
            Package(template).save(output)
            with ZipFile(template) as source, ZipFile(output) as clone:
                self.assertEqual(source.namelist(), clone.namelist())
                for part in source.namelist():
                    self.assertEqual(source.read(part), clone.read(part), part)

    def test_existing_output_is_never_overwritten(self):
        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp) / "existing.xlsx"
            output.write_bytes(b"user data")
            with self.assertRaisesRegex(ValueError, "overwrite"):
                Package(original(OFFICIAL, "Report5_Test Report.xlsx")).save(output)
            self.assertEqual(output.read_bytes(), b"user data")

    def test_format_part_change_is_rejected(self):
        package = Package(original(OFFICIAL, "Report5_Test Report.xlsx"))
        package.parts["xl/styles.xml"] = b"altered"
        with self.assertRaisesRegex(ValueError, "Unexpected"):
            package.audit({"xl/worksheets/sheet1.xml"})

    def test_source_and_original_directories_are_protected(self):
        for output in (OFFICIAL / "unsafe-generated", REPORTS / "report-1-project-introduction/unsafe"):
            with self.subTest(output=output), self.assertRaisesRegex(ValueError, "Output"):
                build(REPORTS, OFFICIAL, output, {"report1"})
            self.assertFalse(output.exists())

    def test_missing_source_is_not_exported_as_a_completed_report(self):
        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp) / "output"
            result = build(REPORTS, OFFICIAL, output, {"report4"})
            self.assertEqual(result["artifacts"][0]["status"], "missing_source")
            self.assertEqual([p.name for p in output.iterdir()], ["manifest.json"])

    def test_each_independent_exporter_runs_in_isolated_python(self):
        for name in ("report1", "report2", "report3", "report5", "weekly"):
            with self.subTest(report=name), tempfile.TemporaryDirectory() as temp:
                script = TOOLS / ("export_weekly.py" if name == "weekly" else f"export_{name}.py")
                output = Path(temp) / "output"
                command = [sys.executable, "-I", str(script), "--output", str(output)]
                if name == "weekly":
                    command += ["--week", "week-05"]
                result = subprocess.run(command, capture_output=True, text=True, encoding="utf-8", timeout=60)
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                self.assertTrue((output / "manifest.json").is_file())
                self.assertEqual(len(list(output.glob("*.docx"))) + len(list(output.glob("*.xlsx"))), 1)


if __name__ == "__main__":
    unittest.main()
