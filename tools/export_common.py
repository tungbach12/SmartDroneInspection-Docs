"""Shared input lookup and Word rendering, without report-specific mappings."""
from pathlib import Path
from datetime import datetime
import argparse
import json
import re
import sys

from report_ooxml import WordDocument, plain

ROOT = Path(__file__).resolve().parent.parent
REPORTS = ROOT / "reports"
OFFICIAL = ROOT.parent / "capstone-official-docs"
METADATA_SOURCE = "report-1-project-introduction/report1-project-introduction.md"


def original(directory, filename):
    paths = list(directory.rglob(filename))
    if len(paths) != 1:
        raise ValueError(f"Expected one official template {filename!r}; found {len(paths)}")
    return paths[0]


def project_metadata(reports):
    text = (reports / METADATA_SOURCE).read_text(encoding="utf-8")

    def value(label):
        match = re.search(r"^- " + re.escape(label) + r":\s*(.+)$", text, re.M)
        return plain(match[1]) if match else "Not supplied"

    location = re.search(r"^.*Ho Chi Minh City[^\n]+$", text, re.M)
    return {"project": value("Project name").split(":", 1)[0],
            "code": value("Project code"), "group": value("Group name"),
            "location": location[0] if location else ""}


def render_word(template, reports, output, blocks, warnings=()):
    metadata = project_metadata(reports)
    document = WordDocument(template)
    document.fill_cover(metadata["project"], metadata["location"])
    document.warnings.extend(warnings)
    document.append(blocks)
    content = document.text(document.body)
    for block in blocks:
        if block.kind in {"heading", "paragraph", "list"} and plain(block.text) not in content:
            raise ValueError(f"Missing exported content from {block.source}: {block.text[:80]}")
    audit = document.save(output)
    return {**audit, "source_blocks": len(blocks), "content_complete": True}


def number(value):
    cleaned = plain(value)
    return int(cleaned) if cleaned.isdigit() else cleaned


def validate_output_directory(reports, official, output):
    if output.exists():
        raise ValueError(f"Use a new output directory (will not overwrite): {output}")
    target = output.resolve()
    if target == reports.resolve() or target.is_relative_to(official.resolve()):
        raise ValueError("Output cannot replace or write inside an official template directory")
    generated = (reports / "generated").resolve()
    if target.is_relative_to(reports.resolve()) and not target.is_relative_to(generated):
        raise ValueError("Outputs inside reports/ must use its separate generated/ directory")


def input_hashes(paths):
    from report_ooxml import sha256
    files = set()
    for path in paths:
        if path.is_dir():
            files.update(p for p in path.rglob("*") if p.is_file())
        else:
            if not path.is_file():
                raise FileNotFoundError(f"Missing source: {path}")
            files.add(path)
    return {path: sha256(path.read_bytes()) for path in files}


def verify_inputs(hashes):
    from report_ooxml import sha256
    for path, before in hashes.items():
        if not path.is_file() or sha256(path.read_bytes()) != before:
            raise ValueError(f"An input changed during generation: {path}")


def write_manifest(output, reports, official, artifacts):
    from report_ooxml import sha256
    for artifact in artifacts:
        if artifact["status"] == "generated":
            artifact["output"] = str(Path(artifact["output"]).resolve())
            artifact["output_sha256"] = sha256(Path(artifact["output"]).read_bytes())
    manifest = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "content_root": str(reports), "format_root": str(official),
        "input_hashes_unchanged": True, "artifacts": artifacts,
        "format_contract": "Original format parts preserved; new content changes pagination and row heights",
    }
    output.mkdir(parents=True, exist_ok=True)
    (output / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    return manifest


def parser(description):
    result = argparse.ArgumentParser(description=description)
    result.add_argument("--sources", type=Path, default=REPORTS)
    result.add_argument("--templates", type=Path, default=OFFICIAL)
    result.add_argument("--output", type=Path)
    return result


def run_single(report, template_name, sources, exporter):
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    cli = parser(f"Export {report} using its own official format")
    if report == "weekly":
        cli.add_argument("--week", help="Select a source stem such as week-05 (default: all weeks)")
    args = cli.parse_args()
    output = args.output or args.sources / "generated" / (
        datetime.now().strftime("%Y-%m-%d_%H%M%S_%f") + "-" + report)
    try:
        validate_output_directory(args.sources, args.templates, output)
        template = original(args.templates, template_name)
        source_paths = [args.sources / relative for relative in sources]
        hashes = input_hashes([template, args.sources / METADATA_SOURCE, *source_paths])
        artifacts = []
        if report == "weekly":
            weekly_sources = sorted(source_paths[0].glob("week-*.md"))
            if args.week:
                weekly_sources = [p for p in weekly_sources if p.stem == args.week]
            if not weekly_sources:
                raise ValueError("No matching weekly report source")
            metadata = project_metadata(args.sources)
            for source in weekly_sources:
                target = output / f"Project Weekly Report_{metadata['group']}_{source.stem}.xlsx"
                result = exporter(template, source, target)
                artifacts.append({"report": source.stem, "status": "generated", "output": str(target),
                                  "sources": [str(source)], **result})
        else:
            target = output / template_name
            result = exporter(template, args.sources, target)
            artifacts.append({"report": report, "status": "generated", "output": str(target),
                              "sources": [str(p) for p in source_paths], **result})
        verify_inputs(hashes)
        write_manifest(output, args.sources, args.templates, artifacts)
    except (ValueError, FileNotFoundError) as exc:
        cli.exit(1, f"Generation failed: {exc}\n")
    for artifact in artifacts:
        print(f"{artifact['report']}: {artifact['status']}")
    print(f"Output: {output}")
