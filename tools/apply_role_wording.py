"""Rewrite bare role enum tokens in Report 3 prose to readable role names.

The SRS already defines the role vocabulary in section 2.1 using the pattern
``Organization Admin (`ORG_ADMIN`)``. This applies the same naming to prose so
the document reads as English rather than as code, while keeping the literal
enum in backticks wherever it is a technical identifier.

Skipped, deliberately:
  * text inside backticks        - a technical identifier, keep the enum
  * fenced code blocks           - Mermaid/diagram source, keep the enum
  * table cells that *are* the actor definition (section 2.1) - already correct
  * record-of-changes history    - it quotes what earlier revisions literally said

Run once, then review the diff. It refuses to touch anything outside the
Report 3 source folder.
"""
from pathlib import Path
import argparse
import re
import sys

REPORTS = Path(__file__).resolve().parent.parent / "reports" / \
    "report-3-software-requirement-specification"

# Longest first: ORG_ADMIN must not be matched as the ADMIN inside it.
ROLES = [
    ("MAINTENANCE_ENGINEER", "Maintenance Engineer"),
    ("ORG_ADMIN", "Organization Admin"),
    ("INSPECTOR", "Inspector"),
    ("ADMIN", "Platform Admin"),
]

# The actor table in section 2.1 already pairs name and enum; leave it alone.
SKIP_MARKERS = ("document_type:", "weight:", "source:", "title:")


def split_protected(text):
    """Return (segment, is_protected) pairs covering the whole text."""
    pattern = re.compile(r"`[^`]*`|```.*?```", re.S)
    out, index = [], 0
    for match in pattern.finditer(text):
        if match.start() > index:
            out.append((text[index:match.start()], False))
        out.append((match.group(0), True))
        index = match.end()
    if index < len(text):
        out.append((text[index:], False))
    return out


def rewrite(text, actor_table):
    changed = 0
    result = []
    for segment, protected in split_protected(text):
        if protected:
            result.append(segment)
            continue
        if any(marker in segment for marker in actor_table):
            result.append(segment)
            continue
        for enum, name in ROLES:
            # A bare token: not part of a longer identifier, not already backticked.
            pattern = re.compile(r"(?<![A-Za-z0-9_`])" + enum + r"(?![A-Za-z0-9_`])")
            segment, hits = pattern.subn(name, segment)
            changed += hits
        result.append(segment)
    return "".join(result), changed


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true",
                        help="write changes; without it, only report counts")
    parser.add_argument("--include-history", action="store_true",
                        help="also rewrite 00-record-of-changes.md")
    args = parser.parse_args()

    files = sorted(REPORTS.glob("0*.md"))
    if not files:
        sys.exit(f"No Report 3 sources found in {REPORTS}")
    total = 0
    for path in files:
        if path.name.startswith("00-record-of-changes") and not args.include_history:
            print(f"  skip (history): {path.name}")
            continue
        # Section 2.1 of 02-user-requirements.md is the actor definition table.
        actor_table = ("# Actor |",) if path.name.startswith("02-") else ()
        original = path.read_text(encoding="utf-8-sig")
        updated, changed = rewrite(original, actor_table)
        if changed:
            total += changed
            print(f"  {path.name}: {changed} replacement(s)")
            if args.apply:
                path.write_text(updated, encoding="utf-8")
        else:
            print(f"  {path.name}: unchanged")
    print(f"Total replacements: {total}")
    if not args.apply:
        print("Dry run. Re-run with --apply to write.")


if __name__ == "__main__":
    main()