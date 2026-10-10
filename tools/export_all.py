#!/usr/bin/env python3
"""Run independent report exporters and collect their verification manifests."""
from datetime import datetime
from pathlib import Path
import sys

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parent))

import export_report1
import export_report2
import export_report3
import export_report5
import export_weekly
from export_common import (METADATA_SOURCE, input_hashes, original, parser,
                           project_metadata, validate_output_directory,
                           verify_inputs, write_manifest)

EXPORTERS = {
    "report1": export_report1,
    "report2": export_report2,
    "report3": export_report3,
    "report5": export_report5,
    "weekly": export_weekly,
}
MISSING_SOURCES = {
    "report4": "Report4_Software Design Document.docx",
    "report5-documentation": "Report5_Test Documentation.docx",
    "report5-unit": "Report5_Unit Test.xls",
    "report6": "Report6_Software User Guides.docx",
    "report7": "Report7_Final Project Report.docx",
    "project-tracking": "Report3_Project Tracking.xlsx",
}
TEMPLATES = {key: module.TEMPLATE_NAME for key, module in EXPORTERS.items()} | MISSING_SOURCES


def build(reports, official, output_dir, selected=None):
    validate_output_directory(reports, official, output_dir)
    artifacts = []
    for key, module in EXPORTERS.items():
        if selected and key not in selected:
            continue
        template = original(official, module.TEMPLATE_NAME)
        sources = [reports / relative for relative in module.SOURCES]
        hashes = input_hashes([template, reports / METADATA_SOURCE, *sources])
        if key == "weekly":
            metadata = project_metadata(reports)
            weekly_sources = sorted(sources[0].glob("week-*.md"))
            if not weekly_sources:
                raise ValueError("No weekly report sources")
            for source in weekly_sources:
                output = output_dir / f"Project Weekly Report_{metadata['group']}_{source.stem}.xlsx"
                result = module.export(template, source, output)
                artifacts.append({"report": source.stem, "status": "generated", "output": str(output),
                                  "sources": [str(source)], **result})
        else:
            output = output_dir / module.TEMPLATE_NAME
            result = module.export(template, reports, output)
            artifacts.append({"report": key, "status": "generated", "output": str(output),
                              "sources": [str(path) for path in sources], **result})
        verify_inputs(hashes)
    for key, template_name in MISSING_SOURCES.items():
        if selected and key not in selected:
            continue
        artifacts.append({"report": key, "status": "missing_source",
                          "template": str(original(official, template_name)),
                          "reason": "No corresponding editable source under reports/; no content fabricated"})
    return write_manifest(output_dir, reports, official, artifacts)


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    cli = parser(__doc__)
    cli.add_argument("--only", nargs="+", choices=list(TEMPLATES))
    cli.add_argument("--list", action="store_true")
    args = cli.parse_args()
    if args.list:
        for key, name in TEMPLATES.items():
            state = "source available" if key in EXPORTERS else "missing source"
            print(f"{key:24s} {state:18s} {name}")
        return
    output = args.output or args.sources / "generated" / datetime.now().strftime("%Y-%m-%d_%H%M%S_%f")
    try:
        result = build(args.sources, args.templates, output, set(args.only) if args.only else None)
    except (ValueError, FileNotFoundError) as exc:
        cli.exit(1, f"Generation failed: {exc}\n")
    for artifact in result["artifacts"]:
        print(f"{artifact['report']}: {artifact['status']}")
    print(f"Output: {output}")


if __name__ == "__main__":
    main()
