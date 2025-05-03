# -*- coding: utf-8 -*-
"""
fetchdocstrings.py

This script traverses all indicator directories in the bamboo_ta package, extracts docstrings from each indicator,
and writes them to a single Markdown file (indicators.md) in the /documentation directory.

- Each indicator category (directory) is an H1 header.
- Each indicator file is an H2 header.
- The main docstring is extracted from the main indicator function (matching the filename) or, if not found, from the module.
- The script creates the documentation directory if it does not exist.

Usage:
    python fetchdocstrings.py
"""

import os
import sys
import importlib
import inspect
from pathlib import Path

# List of indicator categories (directories)
CATEGORIES = [
    "candles", "cycles", "momentum", "performance", "statistics",
    "trend", "utility", "volatility", "volume"
]

ROOT = Path(__file__).parent
BAMBOO_TA_DIR = ROOT / "bamboo_ta"
DOCS_DIR = ROOT / "documentation"
OUTPUT_FILE = DOCS_DIR / "indicators.md"


def snake_to_title(name: str) -> str:
    """Convert snake_case to Title Case."""
    return name.replace("_", " ").title()


def get_indicator_doc(module, indicator_name: str) -> str:
    """
    Extract the docstring from the main indicator function (matching the filename),
    or from the module if not found.
    """
    # Try to get the function docstring
    func = getattr(module, indicator_name, None)
    if func and callable(func) and func.__doc__:
        return func.__doc__
    # Try to get module-level docstring
    if hasattr(module, "__doc__") and module.__doc__:
        return module.__doc__
    # Try to get __doc__ attribute set as <func>.__doc__ = "..."
    for name, obj in inspect.getmembers(module):
        if name == f"{indicator_name}.__doc__" and isinstance(obj, str):
            return obj
    # Try to find any function with a docstring
    for name, obj in inspect.getmembers(module):
        if callable(obj) and obj.__doc__:
            return obj.__doc__
    return "*No docstring found.*"


def main():
    if not BAMBOO_TA_DIR.exists():
        print(f"Error: {BAMBOO_TA_DIR} does not exist.")
        sys.exit(1)
    DOCS_DIR.mkdir(exist_ok=True)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as out:
        out.write("# Bamboo TA Indicators Documentation\n\n")
        for category in CATEGORIES:
            category_dir = BAMBOO_TA_DIR / category
            if not category_dir.is_dir():
                continue
            out.write(f"# {snake_to_title(category)}\n\n")
            for file in sorted(category_dir.glob("*.py")):
                if file.name.startswith("__"):
                    continue
                indicator_name = file.stem
                module_path = f"bamboo_ta.{category}.{indicator_name}"
                try:
                    module = importlib.import_module(module_path)
                except Exception as e:
                    out.write(f"## {snake_to_title(indicator_name)}\n")
                    out.write(f"*Error importing module: {e}*\n\n")
                    continue
                doc = get_indicator_doc(module, indicator_name)
                out.write(f"## {snake_to_title(indicator_name)}\n")
                out.write(doc.strip() + "\n\n")
    print(f"Documentation written to {OUTPUT_FILE}")

if __name__ == "__main__":
    main() 