#!/usr/bin/env python3
"""Compatibility name for export_report5.py; the shared command is export_all.py."""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from export_report5 import TEMPLATE_NAME, SOURCES, export
from export_common import run_single

if __name__ == "__main__":
    run_single("report5", TEMPLATE_NAME, SOURCES, export)
