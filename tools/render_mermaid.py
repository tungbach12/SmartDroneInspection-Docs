#!/usr/bin/env python3
"""Extract Mermaid diagrams from report Markdown sources into .mmd files and manifest."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parent))

from report_ooxml import parse_markdown, sha256

ROOT = Path(__file__).resolve().parent.parent
REPORTS_DIR = ROOT / "reports"
MERMAID_SRC_DIR = ROOT / "diagrams" / "mermaid"


def infer_title(code: str) -> str:
    match = re.search(r"%%\s*title:\s*(.+)$", code, re.M | re.I)
    if match:
        return match.group(1).strip()
    text_lower = code.lower()
    if "sequencediagram" in text_lower:
        return "Sequence Diagram"
    if "classdiagram" in text_lower:
        return "Class Diagram"
    if "statediagram" in text_lower:
        return "State Machine Diagram"
    if "package" in text_lower:
        return "Package Diagram"
    if "architecture" in text_lower:
        return "System Architecture Diagram"
    if "erdiagram" in text_lower or "entity relationship" in text_lower:
        return "Entity Relationship Diagram (ERD)"
    if "flowchart lr" in text_lower or "use case" in text_lower:
        return "Use Case Diagram"
    if "screens flow" in text_lower or "flowchart td" in text_lower:
        return "Screens Flow Diagram"
    return "System Diagram"


def slugify(text: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return slug[:48] or "diagram"


def collect_mermaid_blocks() -> list[dict]:
    MERMAID_SRC_DIR.mkdir(parents=True, exist_ok=True)
    items = []
    idx = 0
    for md_path in sorted(REPORTS_DIR.rglob("*.md")):
        if "generated" in md_path.parts:
            continue
        blocks = parse_markdown(md_path, strict_tables=False)
        for block in blocks:
            if block.kind == "code" and block.language == "mermaid":
                idx += 1
                code = block.text.strip()
                digest = sha256(code.encode("utf-8"))[:12]
                title = infer_title(code)
                report_name = md_path.parent.name
                mmd_filename = f"{idx:02d}_{slugify(report_name)}_{slugify(title)}_{digest}.mmd"
                mmd_path = MERMAID_SRC_DIR / mmd_filename
                mmd_path.write_text(code + "\n", encoding="utf-8")

                png_dir = md_path.parent / "assets" / "mermaid"
                png_dir.mkdir(parents=True, exist_ok=True)
                png_path = png_dir / f"{digest}.png"

                items.append({
                    "index": idx,
                    "digest": digest,
                    "title": title,
                    "source_md": str(md_path.relative_to(ROOT)).replace("\\", "/"),
                    "mmd_path": str(mmd_path.relative_to(ROOT)).replace("\\", "/"),
                    "png_path": str(png_path.resolve()).replace("\\", "/"),
                    "code": code,
                })
    manifest_path = MERMAID_SRC_DIR / "manifest.json"
    manifest_path.write_text(json.dumps(items, ensure_ascii=False, indent=2), encoding="utf-8")
    return items


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    items = collect_mermaid_blocks()
    print(f"Extracted {len(items)} Mermaid diagram(s) to {MERMAID_SRC_DIR}")
    for item in items:
        exists = Path(item["png_path"]).is_file()
        print(f"  [{item['index']:02d}] {item['digest']} ({'PNG exists' if exists else 'needs PNG'}) - {item['title']} ({item['source_md']})")


if __name__ == "__main__":
    main()
