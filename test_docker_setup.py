#!/usr/bin/env python3
"""
Test script to verify ClauseMate Docker setup works correctly.
This script tests the fixes for ModuleNotFoundError and other issues.
"""

import sys
import os
from pathlib import Path

def test_path_setup():
    """Test that Python path is set up correctly."""
    print("[TEST] Testing Python path setup...")

    # Add project root to path (simulating Docker environment)
    project_root = Path(__file__).resolve().parents[1]
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))
        print(f"  [OK] Added {project_root} to Python path")

    return True

def test_imports():
    """Test that all critical imports work."""
    print("[TEST] Testing imports...")

    try:
        from src.main import ClauseMateAnalyzer
        print("  [OK] src.main import successful")
    except ImportError as e:
        print(f"  [FAIL] src.main import failed: {e}")
        return False

    try:
        from src.multi_file.multi_file_batch_processor import MultiFileBatchProcessor
        print("  [OK] Multi-file processor import successful")
    except ImportError as e:
        print(f"  [FAIL] Multi-file processor import failed: {e}")
        return False

    try:
        from src.config import CRITICAL_PRONOUNS
        print("  [OK] Config import successful")
    except (ImportError, AttributeError) as e:
        print(f"  [FAIL] Config import failed: {e}")
        return False

    return True

def test_script_execution():
    """Test that scripts can run without ModuleNotFoundError."""
    print("[TEST] Testing script execution...")

    # Test the multi-file analysis script
    try:
        # Import the script module
        from scripts.run_multi_file_analysis import MultiFileBatchProcessor
        print("  [OK] Script import successful")
    except ImportError as e:
        print(f"  [FAIL] Script import failed: {e}")
        return False

    # Test with help flag (should not fail on imports)
    import subprocess
    try:
        result = subprocess.run([
            sys.executable, "scripts/run_multi_file_analysis.py", "--help"
        ], capture_output=True, text=True, cwd=Path(__file__).resolve().parents[1])

        if result.returncode == 0:
            print("  [OK] Script execution successful")
            return True
        else:
            print(f"  [FAIL] Script execution failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"  [FAIL] Script execution error: {e}")
        return False

def test_notebook_imports():
    """Test that notebook-style imports work."""
    print("[TEST] Testing notebook-style imports...")

    try:
        import pandas as pd
        print("  [OK] pandas import successful")
    except ImportError as e:
        print(f"  [FAIL] pandas import failed: {e}")
        return False

    return True

def test_data_access():
    """Test data directory access."""
    print("[TEST] Testing data access...")

    project_root = Path(__file__).resolve().parents[1]

    # Check if data directories exist
    data_paths = [
        project_root / "data" / "input" / "gotofiles",
        project_root / "data" / "input",
        project_root / "data"
    ]

    for path in data_paths:
        if path.exists():
            print(f"  [OK] Data path exists: {path}")
            # List contents
            try:
                contents = list(path.glob("*"))
                print(f"    [INFO] Contains {len(contents)} items")
                if contents:
                    print(f"    [INFO] Sample: {contents[0].name}")
            except Exception as e:
                print(f"    [WARN] Could not list contents: {e}")
        else:
            print(f"  [WARN] Data path not found: {path}")

    return True

def main():
    """Run all tests."""
    print("=" * 60)
    print("CLAUSEMATE DOCKER SETUP TEST")
    print("=" * 60)
    print(f"Python version: {sys.version}")
    print(f"Working directory: {Path.cwd()}")
    print(f"Script location: {Path(__file__).resolve()}")
    print()

    tests = [
        ("Path Setup", test_path_setup),
        ("Imports", test_imports),
        ("Script Execution", test_script_execution),
        ("Notebook Imports", test_notebook_imports),
        ("Data Access", test_data_access)
    ]

    results = []
    for name, test_func in tests:
        print(f"\n{name}:")
        results.append(test_func())

    print("\n" + "=" * 60)
    print("TEST RESULTS SUMMARY")
    print("=" * 60)

    success_count = sum(results)
    total_count = len(results)

    for i, (name, _) in enumerate(tests):
        status = "[PASS]" if results[i] else "[FAIL]"
        print(f"{name}: {status}")

    print(f"\n[SUMMARY] Overall: {success_count}/{total_count} tests passed")

    if success_count == total_count:
        print("[SUCCESS] All tests passed! Docker environment is ready.")
        return True
    else:
        print("[WARNING] Some tests failed. Check the output above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)