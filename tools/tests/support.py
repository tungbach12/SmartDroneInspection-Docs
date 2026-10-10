"""Shared assertions; report-specific expectations stay in each test module."""
from pathlib import Path
import sys
import tempfile

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from export_common import OFFICIAL, REPORTS, original
from report_ooxml import Package, descendants, plain, text_of


def assert_word_export(test, exporter):
    template = original(OFFICIAL, exporter.TEMPLATE_NAME)
    with tempfile.TemporaryDirectory() as temp:
        output = Path(temp) / exporter.TEMPLATE_NAME
        result = exporter.export(template, REPORTS, output)
        test.assertTrue(result["format_parts_preserved"])
        test.assertTrue(result["content_complete"])
        source, generated = Package(template), Package(output)
        for part in ("word/styles.xml", "word/numbering.xml", "word/fontTable.xml"):
            test.assertEqual(source.parts[part], generated.parts[part], part)
        test.assertEqual(
            [node.toxml() for node in descendants(source.xml("word/document.xml"), "sectPr")],
            [node.toxml() for node in descendants(generated.xml("word/document.xml"), "sectPr")])
        document = generated.xml("word/document.xml")
        def visible(node):
            if node.nodeType == node.ELEMENT_NODE and node.localName == "t":
                return text_of(node)
            if node.nodeType == node.ELEMENT_NODE and node.localName == "br":
                return "\n"
            return "".join(visible(child) for child in node.childNodes)

        text = visible(document)
        for block in exporter.blocks(REPORTS):
            if block.kind == "table":
                for row in block.rows:
                    for value in row:
                        test.assertIn(plain(value), text)
            elif block.kind in {"heading", "paragraph", "list"}:
                test.assertIn(plain(block.text), text)
        test.assertIn("SmartDroneInspection", text)
        test.assertNotIn("Hanoi, August 2019", text)
        return result
