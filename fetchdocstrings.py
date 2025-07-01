# -*- coding: utf-8 -*-
"""
fetchdocstrings.py

This script traverses all indicator directories in the bamboo_ta package, extracts docstrings from each indicator,
and writes them to a single Markdown file (indicators.md) in the /documentation directory.
Additionally, it automatically updates the indicator list in README.md.

Documentation generation:
- Each indicator category (directory) is an H1 header.
- Each indicator file is an H2 header.
- The main docstring is extracted from the main indicator function (matching the filename) or, if not found, from the module.
- The script creates the documentation directory if it does not exist.

README.md update:
- Automatically updates the "## Indicator Categories" section in README.md
- Preserves category headings and descriptions
- Lists all indicators organized by category
- Handles empty categories (shows description only)

Usage:
    python fetchdocstrings.py
"""

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
README_FILE = ROOT / "README.md"


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


def collect_indicators_by_category():
    """Collect all indicators organized by category."""
    indicators_by_category = {}
    
    for category in CATEGORIES:
        category_dir = BAMBOO_TA_DIR / category
        if not category_dir.is_dir():
            continue
        
        indicators = []
        for file in sorted(category_dir.glob("*.py")):
            if file.name.startswith("__"):
                continue
            indicator_name = file.stem
            indicators.append(snake_to_title(indicator_name))
        
        if indicators:
            indicators_by_category[category] = indicators
    
    return indicators_by_category


def update_readme_indicators(indicators_by_category):
    """Update the indicator section in README.md."""
    if not README_FILE.exists():
        print(f"Error: {README_FILE} does not exist.")
        return
    
    # Read the current README content
    with open(README_FILE, "r", encoding="utf-8") as f:
        lines = f.readlines()
    
    # Find the indicator categories section boundaries
    start_line = None
    end_line = None
    
    for i, line in enumerate(lines):
        if line.strip() == "## Indicator Categories":
            start_line = i
        elif start_line is not None and line.strip().startswith("To access detailed documentation"):
            end_line = i
            break
    
    if start_line is None:
        print("Error: Could not find '## Indicator Categories' section in README.md")
        return
    
    if end_line is None:
        print("Error: Could not find end of indicator categories section in README.md")
        return
    
    # Create the new indicator section
    new_section = []
    new_section.append("## Indicator Categories\n")
    new_section.append("\n")
    new_section.append("Bamboo-TA includes a wide range of technical analysis indicators organized into the following categories:\n")
    new_section.append("\n")
    
    # Category descriptions
    category_descriptions = {
        "candles": "Indicators for candlestick pattern analysis and transformations:",
        "cycles": "Indicators for analyzing market cycles:",
        "momentum": "Indicators that measure the rate of change in price movements:",
        "performance": "*Note: This category is currently under development.*",
        "statistics": "*Note: This category is currently under development.*",
        "trend": "Indicators that help identify the direction of market trends:",
        "utility": "Utility functions and indicators for various calculations:",
        "volatility": "Indicators that measure the rate and magnitude of price changes:",
        "volume": "Indicators that incorporate trading volume to confirm price movements:"
    }
    
    for category in CATEGORIES:
        new_section.append(f"### {snake_to_title(category)}\n")
        new_section.append("\n")
        
        # Add category description
        if category in category_descriptions:
            new_section.append(f"{category_descriptions[category]}\n")
            new_section.append("\n")
        
        # Add indicators for this category (if any exist)
        if category in indicators_by_category:
            for indicator in indicators_by_category[category]:
                new_section.append(f"- {indicator}\n")
            new_section.append("\n")
        else:
            # Add a blank line for empty categories
            new_section.append("\n")
    
    # Replace the old section with the new one
    new_lines = lines[:start_line] + new_section + lines[end_line:]
    
    # Write the updated README
    with open(README_FILE, "w", encoding="utf-8") as f:
        f.writelines(new_lines)
    
    print(f"README.md indicator section updated")


def main():
    if not BAMBOO_TA_DIR.exists():
        print(f"Error: {BAMBOO_TA_DIR} does not exist.")
        sys.exit(1)
    DOCS_DIR.mkdir(exist_ok=True)

    # Collect indicators by category
    indicators_by_category = collect_indicators_by_category()

    # Generate documentation file
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
    
    # Update README.md indicator section
    update_readme_indicators(indicators_by_category)

if __name__ == "__main__":
    main() 