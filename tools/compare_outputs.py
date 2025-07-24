#!/usr/bin/env python3
"""Compare two CSV output files to verify reproducibility.

Usage:
    python tools/compare_outputs.py <file1.csv> <file2.csv>
"""

import sys
from pathlib import Path

import pandas as pd


def compare_csv_files(file1_path: str, file2_path: str) -> bool:
    """Compare two CSV files and report differences.

    Args:
        file1_path: Path to the first CSV file
        file2_path: Path to the second CSV file

    Returns:
        True if files are identical, False otherwise
    """
    try:
        # Read both files
        df1 = pd.read_csv(file1_path)
        df2 = pd.read_csv(file2_path)

        print("Comparing:")
        print(f"  File 1: {file1_path} ({len(df1)} rows, {len(df1.columns)} columns)")
        print(f"  File 2: {file2_path} ({len(df2)} rows, {len(df2.columns)} columns)")
        print()

        # Check dimensions
        if df1.shape != df2.shape:
            print("❌ MISMATCH: Different dimensions")
            print(f"  File 1: {df1.shape}")
            print(f"  File 2: {df2.shape}")
            return False

        # Check column names
        if list(df1.columns) != list(df2.columns):
            print("❌ MISMATCH: Different column names")
            print(f"  File 1 columns: {list(df1.columns)}")
            print(f"  File 2 columns: {list(df2.columns)}")
            return False

        # Check data equality
        if df1.equals(df2):
            print("✅ SUCCESS: Files are identical!")
            return True
        else:
            print("❌ MISMATCH: Files have different data")

            # Show some details about differences
            differences = df1.compare(df2, keep_shape=True, keep_equal=False)
            if not differences.empty:
                print("\nFirst few differences:")
                print(differences.head())

            return False

    except FileNotFoundError as e:
        print(f"❌ ERROR: File not found - {e}")
        return False
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False


def main():
    """Main function to handle command line arguments."""
    if len(sys.argv) != 3:
        print("Usage: python tools/compare_outputs.py <file1.csv> <file2.csv>")
        sys.exit(1)

    file1_path = sys.argv[1]
    file2_path = sys.argv[2]

    # Check that files exist
    if not Path(file1_path).exists():
        print(f"❌ ERROR: File not found: {file1_path}")
        sys.exit(1)

    if not Path(file2_path).exists():
        print(f"❌ ERROR: File not found: {file2_path}")
        sys.exit(1)

    # Compare files
    are_identical = compare_csv_files(file1_path, file2_path)

    # Exit with appropriate code
    sys.exit(0 if are_identical else 1)


if __name__ == "__main__":
    main()
