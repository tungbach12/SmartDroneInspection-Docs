#!/usr/bin/env python3
"""Export Review 2 specific Word packages (Registration + BM03, BM02 Self-Review, BM01 Design Brief + Appendix A, BM04 Commitment)."""
from __future__ import annotations

from pathlib import Path
import sys

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parent))

from export_common import OFFICIAL, REPORTS, original, render_word
from report_ooxml import parse_markdown

PACK_SPECS = [
    {
        "key": "registration",
        "docx_name": "SWP490_GFA26SE139_R2_Registration.docx",
        "pdf_name": "SWP490_GFA26SE139_R2_Registration.pdf",
        "title": "SWP490 Review 2 – Registration Form (v2.0) & BM03 Record of Changes",
        "sources": [
            "review-2-registration/01-registration-form.md",
            "review-2-registration/02-bm03-record-of-changes.md",
        ],
    },
    {
        "key": "self-review",
        "docx_name": "SWP490_GFA26SE139_R2_SelfReview.docx",
        "pdf_name": "SWP490_GFA26SE139_R2_SelfReview.pdf",
        "title": "SWP490 Review 2 – BM02 SRS/SDD Self-Review Report",
        "sources": [
            "review-2-self-review/01-bm02-self-review-report.md",
        ],
    },
    {
        "key": "design-brief",
        "docx_name": "SWP490_GFA26SE139_R2_DesignBrief.docx",
        "pdf_name": "SWP490_GFA26SE139_R2_DesignBrief.pdf",
        "title": "SWP490 Review 2 – BM01 Design Brief & Appendix A (Defense 1.1 Targets)",
        "sources": [
            "review-2-design-brief/01-bm01-design-brief.md",
            "review-2-design-brief/02-appendix-a-and-bm04-commitment.md",
        ],
    },
    {
        "key": "commitment",
        "docx_name": "SWP490_GFA26SE139_R2_Commitment.docx",
        "pdf_name": "SWP490_GFA26SE139_R2_Commitment.pdf",
        "title": "SWP490 Review 2 – BM04 Review 2 Commitment Baseline",
        "sources": [
            "review-2-registration/01-registration-form.md",
            "review-2-design-brief/01-bm01-design-brief.md",
            "review-2-design-brief/02-appendix-a-and-bm04-commitment.md",
        ],
    },
]


def export_pack(output_dir: Path, reports: Path = REPORTS, official: Path = OFFICIAL) -> list[dict]:
    template = original(official, "Report3_Software Requirement Specification.docx")
    output_dir.mkdir(parents=True, exist_ok=True)
    results = []
    for spec in PACK_SPECS:
        blocks = []
        for rel in spec["sources"]:
            blocks.extend(parse_markdown(reports / rel, strict_tables=False))
        target_docx = output_dir / spec["docx_name"]
        res = render_word(template, reports, target_docx, blocks)
        results.append({
            "key": spec["key"],
            "docx": str(target_docx),
            "pdf": str(output_dir / spec["pdf_name"]),
            "title": spec["title"],
            "sources": spec["sources"],
            **res,
        })
    return results


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else REPORTS / "generated" / "review-2-pack"
    results = export_pack(out)
    for r in results:
        print(f"{r['key']}: generated -> {r['docx']}")


if __name__ == "__main__":
    main()
