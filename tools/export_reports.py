#!/usr/bin/env python3
"""Compatibility command; use export_all.py or the individual report exporters."""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from export_all import main

if __name__ == "__main__":
    main()
