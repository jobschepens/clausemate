#!/usr/bin/env python3
"""Detailed analysis script for 4.tsv to understand structure and compatibility issues.

This script compares 4.tsv with working files to identify:
1. Missing annotation layers in preamble
2. Column structure differences
3. Data content variations
4. Potential solutions for compatibility
"""

import os
from typing import Any, Dict, List


def extract_preamble(file_path: str) -> List[str]:
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


def analyze_preamble_structure(preamble: List[str]) -> Dict[str, Any]:
    """Analyze preamble structure and extract annotation information."""
    analysis = {
        "total_lines": len(preamble),
        "format_version": None,
        "annotation_layers": [],
        "span_layers": [],
        "chain_layers": [],
        "relation_layers": [],
        "missing_elements": [],
    }

    for line in preamble:
        if line.startswith("#FORMAT="):
            analysis["format_version"] = line.split("=", 1)[1]
        elif line.startswith("#T_SP="):
            # Span layer annotation
            layer_info = line.split("=", 1)[1]
            analysis["span_layers"].append(layer_info)
        elif line.startswith("#T_CH="):
            # Chain layer annotation
            layer_info = line.split("=", 1)[1]
            analysis["chain_layers"].append(layer_info)
        elif line.startswith("#T_RL="):
            # Relation layer annotation
            layer_info = line.split("=", 1)[1]
            analysis["relation_layers"].append(layer_info)

    # Check for common missing elements
    has_coreference = any(
        "coref" in layer.lower()
        for layer in analysis["chain_layers"] + analysis["relation_layers"]
    )
    if not has_coreference:
        analysis["missing_elements"].append("coreference_annotations")

    return analysis


def sample_data_rows(file_path: str, num_rows: int = 10) -> List[List[str]]:
    """Sample first few data rows from TSV file."""
    data_rows = []
    try:
        with open(file_path, encoding="utf-8") as f:
            # Skip preamble
            for line in f:
                line = line.strip()
                if line.startswith("#") or line == "":
                    continue
                else:
                    # First data line found, start sampling
                    data_rows.append(line.split("\t"))
                    break

            # Sample additional rows
            for i, line in enumerate(f):
                if i >= num_rows - 1:
                    break
                line = line.strip()
                if line and not line.startswith("#"):
                    data_rows.append(line.split("\t"))

    except Exception as e:
        print(f"Error sampling data from {file_path}: {e}")
        return []

    return data_rows


def analyze_column_structure(data_rows: List[List[str]]) -> Dict[str, Any]:
    """Analyze column structure from data rows."""
    if not data_rows:
        return {"error": "No data rows available"}

    analysis = {
        "column_count": len(data_rows[0]) if data_rows else 0,
        "consistent_columns": True,
        "column_variations": [],
        "sample_data": data_rows[:5],  # First 5 rows for inspection
        "potential_coreference_columns": [],
    }

    # Check column consistency
    expected_cols = len(data_rows[0]) if data_rows else 0
    for i, row in enumerate(data_rows):
        if len(row) != expected_cols:
            analysis["consistent_columns"] = False
            analysis["column_variations"].append(
                f"Row {i + 1}: {len(row)} columns (expected {expected_cols})"
            )

    # Look for potential coreference data in columns
    if data_rows:
        for col_idx in range(len(data_rows[0])):
            col_values = [
                row[col_idx] if col_idx < len(row) else "" for row in data_rows[:10]
            ]
            # Check if column contains coreference-like data (numbers, references)
            has_coref_pattern = any(
                val and (val.isdigit() or "-" in val or "[" in val or "]" in val)
                for val in col_values
            )
            if has_coref_pattern:
                analysis["potential_coreference_columns"].append(
                    {"column_index": col_idx, "sample_values": col_values[:5]}
                )

    return analysis


def compare_files_detailed(files_info: Dict[str, str]) -> Dict[str, Any]:
    """Compare all files in detail."""
    comparison = {
        "files_analyzed": {},
        "preamble_comparison": {},
        "column_comparison": {},
        "compatibility_assessment": {},
    }

    for name, path in files_info.items():
        print(f"\n=== Analyzing {name} ===")

        if not os.path.exists(path):
            print(f"File not found: {path}")
            comparison["files_analyzed"][name] = {"error": "File not found"}
            continue

        # Extract and analyze preamble
        preamble = extract_preamble(path)
        preamble_analysis = analyze_preamble_structure(preamble)

        # Sample and analyze data
        data_rows = sample_data_rows(path)
        column_analysis = analyze_column_structure(data_rows)

        comparison["files_analyzed"][name] = {
            "path": path,
            "preamble_analysis": preamble_analysis,
            "column_analysis": column_analysis,
            "file_exists": True,
        }

        print(f"  Preamble lines: {preamble_analysis['total_lines']}")
        print(f"  Columns: {column_analysis.get('column_count', 'unknown')}")
        print(f"  Span layers: {len(preamble_analysis['span_layers'])}")
        print(f"  Chain layers: {len(preamble_analysis['chain_layers'])}")
        print(f"  Relation layers: {len(preamble_analysis['relation_layers'])}")
        if preamble_analysis["missing_elements"]:
            print(f"  Missing: {', '.join(preamble_analysis['missing_elements'])}")

    return comparison


def generate_compatibility_report(comparison: Dict[str, Any]) -> str:
    """Generate detailed compatibility report."""
    report = []
    report.append("# 4.tsv Compatibility Analysis Report")
    report.append("=" * 50)

    # Working files summary
    working_files = ["1.tsv", "2.tsv", "3.tsv"]
    problem_files = ["4.tsv"]

    report.append("\n## Working Files Analysis")
    for name in working_files:
        if name in comparison["files_analyzed"]:
            file_info = comparison["files_analyzed"][name]
            preamble = file_info["preamble_analysis"]
            columns = file_info["column_analysis"]

            report.append(f"\n### {name}")
            report.append(f"- Columns: {columns.get('column_count', 'unknown')}")
            report.append(f"- Preamble lines: {preamble['total_lines']}")
            report.append(f"- Span layers: {len(preamble['span_layers'])}")
            report.append(f"- Chain layers: {len(preamble['chain_layers'])}")
            report.append(f"- Relation layers: {len(preamble['relation_layers'])}")

    report.append("\n## Problem Files Analysis")
    for name in problem_files:
        if name in comparison["files_analyzed"]:
            file_info = comparison["files_analyzed"][name]
            preamble = file_info["preamble_analysis"]
            columns = file_info["column_analysis"]

            report.append(f"\n### {name}")
            report.append(f"- Columns: {columns.get('column_count', 'unknown')}")
            report.append(f"- Preamble lines: {preamble['total_lines']}")
            report.append(f"- Span layers: {len(preamble['span_layers'])}")
            report.append(f"- Chain layers: {len(preamble['chain_layers'])}")
            report.append(f"- Relation layers: {len(preamble['relation_layers'])}")

            if preamble["missing_elements"]:
                report.append(
                    f"- **Missing elements**: {', '.join(preamble['missing_elements'])}"
                )

            if columns.get("potential_coreference_columns"):
                report.append("- **Potential coreference columns found**:")
                for col_info in columns["potential_coreference_columns"]:
                    report.append(
                        f"  - Column {col_info['column_index']}: {col_info['sample_values']}"
                    )

    # Recommendations
    report.append("\n## Compatibility Recommendations")

    if "4.tsv" in comparison["files_analyzed"]:
        file_4_info = comparison["files_analyzed"]["4.tsv"]
        columns_4 = file_4_info["column_analysis"].get("column_count", 0)

        if columns_4 == 13:
            report.append("\n### Option 1: Enhanced Format Detection")
            report.append("- Modify format detector to recognize 13-column variant")
            report.append("- Implement partial compatibility scoring")
            report.append("- Provide clear user feedback about limitations")

            report.append("\n### Option 2: Graceful Degradation")
            report.append("- Extract available linguistic features")
            report.append("- Skip coreference analysis if data missing")
            report.append("- Provide partial results with clear warnings")

            report.append("\n### Option 3: Preprocessing Pipeline")
            report.append("- Add missing columns with default values")
            report.append("- Transform to compatible format")
            report.append("- Maintain data integrity")

    return "\n".join(report)


def main():
    """Main analysis function."""
    print("4.tsv Detailed Compatibility Analysis")
    print("=" * 50)

    # Define files to analyze
    files_to_analyze = {
        "2.tsv": "data/input/gotofiles/2.tsv",
        "1.tsv": "data/input/gotofiles/later/1.tsv",
        "3.tsv": "data/input/gotofiles/later/3.tsv",
        "4.tsv": "data/input/gotofiles/later/4.tsv",
    }

    # Perform detailed comparison
    comparison = compare_files_detailed(files_to_analyze)

    # Generate and save report
    report = generate_compatibility_report(comparison)

    # Save report to file
    report_path = "4tsv_compatibility_report.md"
    try:
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(report)
        print(f"\n✅ Detailed report saved to: {report_path}")
    except Exception as e:
        print(f"\n❌ Error saving report: {e}")

    # Print summary
    print("\n" + "=" * 50)
    print("Analysis Summary:")

    for name, file_info in comparison["files_analyzed"].items():
        if "error" in file_info:
            print(f"  {name}: ERROR - {file_info['error']}")
        else:
            cols = file_info["column_analysis"].get("column_count", "unknown")
            missing = file_info["preamble_analysis"].get("missing_elements", [])
            status = "❌ INCOMPATIBLE" if missing else "✅ COMPATIBLE"
            print(f"  {name}: {cols} columns - {status}")
            if missing:
                print(f"    Missing: {', '.join(missing)}")

    print(f"\n📄 Full analysis report: {report_path}")


if __name__ == "__main__":
    main()
