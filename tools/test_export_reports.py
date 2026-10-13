"""Compatibility test entry point for the report-specific suites in tests/."""
from pathlib import Path
import unittest


def load_tests(loader, tests, pattern):
    directory = Path(__file__).resolve().parent / "tests"
    return loader.discover(str(directory), pattern="test_*.py")


if __name__ == "__main__":
    unittest.main()
