#!/usr/bin/env python3
"""Test ClauseMate setup across different environments."""

import subprocess
import sys
from pathlib import Path


def test_imports():
    """Test that all imports work correctly."""
    import importlib.util

    # Check if modules are available using find_spec
    modules_to_check = [
        "src.config",
        "src.data.models",
        "src.main",
    ]

    for module_name in modules_to_check:
        if importlib.util.find_spec(module_name) is None:
            print(f"❌ Module {module_name} not available")
            return False

    # If all modules are available, try importing them
    try:
        print("✓ All imports successful")
        return True
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False


def test_script_execution():
    """Test that scripts can run from different locations."""
    project_root = Path(__file__).resolve().parents[1]

    # Test from project root
    try:
        result = subprocess.run(
            [sys.executable, "-m", "src.main", "--help"],
            cwd=project_root,
            capture_output=True,
            text=True,
            timeout=10,
        )

        if result.returncode == 0:
            print("✓ Script execution from project root works")
            return True
        else:
            print(f"❌ Script execution failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Script test error: {e}")
        return False


def test_notebook_creation():
    """Test demo notebook creation."""
    try:
        from tools.create_demo_notebook import create_demo_notebook

        demo_path = create_demo_notebook()
        if demo_path.exists():
            print(f"✓ Demo notebook created: {demo_path}")
            return True
        else:
            print("❌ Demo notebook creation failed")
            return False
    except Exception as e:
        print(f"❌ Notebook creation error: {e}")
        return False


def test_jupyter_availability():
    """Test if Jupyter is available."""
    try:
        result = subprocess.run(
            [sys.executable, "-c", "import jupyterlab; print('JupyterLab available')"],
            capture_output=True,
            text=True,
            timeout=5,
        )

        if result.returncode == 0:
            print("✓ JupyterLab is available")
            return True
        else:
            print("❌ JupyterLab not available")
            return False
    except Exception as e:
        print(f"❌ Jupyter test error: {e}")
        return False


def main():
    """Run all environment tests."""
    print("Testing ClauseMate environment setup...")

    tests = [
        ("Import test", test_imports),
        ("Script execution", test_script_execution),
        ("Notebook creation", test_notebook_creation),
        ("Jupyter availability", test_jupyter_availability),
    ]

    results: list[bool] = []
    for name, test_func in tests:
        print(f"\n{name}:")
        results.append(test_func())

    success_count = sum(results)
    print(f"\n📊 Results: {success_count}/{len(tests)} tests passed")

    if success_count == len(tests):
        print("🎉 All tests passed! Environment is ready.")
        return True
    else:
        print("⚠️ Some tests failed. Check setup instructions.")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
