#!/usr/bin/env python3
"""Script to analyze WebAnno TSV preambles and understand column mapping logic."""

import os


def extract_preamble(file_path):
    """Extract preamble lines from a TSV file."""
    preamble_lines = []
    try:
        with open(file_path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line.startswith("#"):
                    preamble_lines.append(line)
                elif line == "":
                    continue
                else:
                    # First non-comment, non-empty line - stop reading preamble
                    break
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return []

    return preamble_lines


def analyze_file(file_path):
    """Analyze a single TSV file's preamble."""
    print(f"\n=== Analysis of {file_path} ===")

    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return

    preamble = extract_preamble(file_path)

    if not preamble:
        print("No preamble found")
        return

    print(f"Preamble lines ({len(preamble)}):")
    for i, line in enumerate(preamble, 1):
        print(f"{i:2d}: {line}")

    # Extract specific annotation types
    print("\nAnnotation types found:")
    for line in preamble:
        if (
            line.startswith("#T_SP=")
            or line.startswith("#T_CH=")
            or line.startswith("#T_RL=")
        ):
            print(f"  {line}")


def main():
    """Main analysis function."""
    files_to_analyze = [
        "data/input/gotofiles/2.tsv",
        "data/input/gotofiles/later/1.tsv",
        "data/input/gotofiles/later/3.tsv",
        "data/input/gotofiles/later/4.tsv",
    ]

    print("WebAnno TSV Preamble Analysis")
    print("=" * 50)

    for file_path in files_to_analyze:
        analyze_file(file_path)

    print("\n" + "=" * 50)
    print("Analysis complete")


if __name__ == "__main__":
    main()
