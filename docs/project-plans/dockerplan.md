# Plan to Fix ClauseMate Binder and Script Issues

## Problem Analysis

1. **Binder auto-open failure**: Missing demo notebook and incorrect URL parameters
2. **ModuleNotFoundError**: Python path issues when running scripts outside project root
3. **Development environment**: Need WSL/Docker setup for consistent development

## Execution Plan

### Phase 1: Create Demo Notebook Infrastructure

**Goal**: Enable Binder to automatically open a functional demo notebook

#### Task 1.1: Create Demo Notebook Generator

````python
#!/usr/bin/env python3
"""Generate ClauseMate demo notebook for Binder."""

import nbformat as nbf
from pathlib import Path
import json

def create_demo_notebook():
    """Create a comprehensive demo notebook showcasing ClauseMate capabilities."""

    # Ensure notebooks directory exists
    notebooks_dir = Path(__file__).resolve().parents[1] / "notebooks"
    notebooks_dir.mkdir(exist_ok=True)

    # Create new notebook
    nb = nbf.v4.new_notebook()

    # Add metadata for better Binder experience
    nb.metadata = {
        "kernelspec": {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3"
        },
        "language_info": {
            "name": "python",
            "version": "3.8+"
        }
    }

    # Notebook cells
    cells = [
        nbf.v4.new_markdown_cell("""# ClauseMate: German Clause Mate Analysis Demo

This notebook demonstrates ClauseMate's capabilities for analyzing pronoun-clause mate relationships in German linguistic data.

## What is ClauseMate?
ClauseMate is a research tool that investigates whether pronouns appear at more consistent linear positions when clause mates are present vs. absent in German discourse.

### Key Features:
- **94.4% antecedent detection** across sentence boundaries
- **Cross-sentence coreference tracking** with chain analysis
- **German-specific pronoun classification** (3rd person, D-pronouns, demonstratives)
- **WebAnno TSV 3.3 format** support for linguistic annotations"""),

        nbf.v4.new_code_cell("""# Install ClauseMate in Binder environment
import sys
import subprocess

# Install the package in editable mode
subprocess.check_call([sys.executable, "-m", "pip", "install", "-e", "."])

print("✓ ClauseMate installed successfully!")"""),

        nbf.v4.new_code_cell("""# Import ClauseMate modules
try:
    from src.main import main
    from src.config import FilePaths, TSVColumns
    from src.data.models import SentenceContext, Token
    print("✓ ClauseMate modules imported successfully!")
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Make sure you're running from the project root directory.")"""),

        nbf.v4.new_markdown_cell("""## Demo Analysis

Let's run ClauseMate on the sample data to demonstrate its linguistic analysis capabilities."""),

        nbf.v4.new_code_cell("""# Check available sample data
from pathlib import Path
import os

data_dir = Path("data/input/gotofiles")
if data_dir.exists():
    tsv_files = list(data_dir.glob("*.tsv"))
    print(f"Found {len(tsv_files)} TSV files for analysis:")
    for file in tsv_files[:3]:  # Show first 3
        print(f"  - {file.name}")

    if tsv_files:
        sample_file = tsv_files[0]
        print(f"\\nUsing sample file: {sample_file.name}")
    else:
        print("❌ No TSV files found in data/input/gotofiles/")
else:
    print("❌ Data directory not found. Binder environment may need data setup.")"""),

        nbf.v4.new_code_cell("""# Run Phase 2 analysis (if data available)
import subprocess
import sys
from pathlib import Path

if Path("data/input/gotofiles").exists() and list(Path("data/input/gotofiles").glob("*.tsv")):
    try:
        # Run the modular Phase 2 analysis
        result = subprocess.run([
            sys.executable, "-m", "src.main"
        ], capture_output=True, text=True, timeout=60)

        if result.returncode == 0:
            print("✓ Phase 2 analysis completed successfully!")
            print("\\nOutput preview:")
            print(result.stdout[-500:])  # Last 500 chars
        else:
            print(f"❌ Analysis failed with return code {result.returncode}")
            print(f"Error: {result.stderr}")

    except subprocess.TimeoutExpired:
        print("⏱️ Analysis timed out (60s limit in demo)")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
else:
    print("⚠️ Skipping analysis - no sample data available in Binder environment")
    print("To run full analysis, upload TSV files to data/input/gotofiles/")"""),

        nbf.v4.new_markdown_cell("""## Understanding the Output

ClauseMate generates CSV files with detailed linguistic relationships:

### Key Columns:
- **pronoun_text**: The critical pronoun being analyzed
- **clause_mate_count**: Number of referential clause mates in same sentence
- **most_recent_antecedent_distance**: Linear distance to nearest mention in coreference chain
- **first_antecedent_distance**: Distance to chain's initial mention
- **givenness**: `neu` (first mention) vs `bekannt` (subsequent)
- **animacy**: `anim` vs `inanim` coreference layers

### Analysis Focus:
The tool investigates linear position consistency of pronouns relative to clause mates in German discourse."""),

        nbf.v4.new_code_cell("""# Show sample output structure (if available)
from pathlib import Path
import pandas as pd

output_files = list(Path("data/output").glob("*.csv")) if Path("data/output").exists() else []

if output_files:
    latest_output = max(output_files, key=lambda p: p.stat().st_mtime)
    print(f"Latest output file: {latest_output.name}")

    # Show sample of results
    df = pd.read_csv(latest_output)
    print(f"\\nDataset shape: {df.shape}")
    print(f"\\nColumns: {list(df.columns)}")
    print(f"\\nSample relationships:")
    print(df.head(3).to_string(index=False))

    # Basic statistics
    print(f"\\n📊 Quick Statistics:")
    print(f"  - Total relationships: {len(df)}")
    print(f"  - Unique pronouns: {df['pronoun_text'].nunique()}")
    print(f"  - Avg clause mates: {df['clause_mate_count'].mean():.1f}")
    if 'most_recent_antecedent_distance' in df.columns:
        print(f"  - Avg antecedent distance: {df['most_recent_antecedent_distance'].mean():.1f}")
else:
    print("No output files found. Run the analysis cell above first.")"""),

        nbf.v4.new_markdown_cell("""## Next Steps

To use ClauseMate with your own data:

1. **Prepare TSV files** in WebAnno TSV 3.3 format with coreference annotations
2. **Upload to `data/input/gotofiles/`** directory
3. **Run analysis** using `python -m src.main` or the analysis cell above
4. **Examine results** in `data/output/` CSV files

### Development Environment
For local development, use:
```bash
# Install dependencies
pip install -e .[dev]

# Run with nox task runner
nox                    # lint + test
nox -s test           # pytest only
nox -s format         # format code

# Manual execution
python -m src.main    # Phase 2 (preferred)
python src/run_phase2.py
```

### Research Applications
ClauseMate supports German linguistic research on:
- Pronoun resolution strategies
- Discourse coherence patterns
- Referential accessibility hierarchies
- Cross-sentence coreference tracking""")
    ]

    nb.cells = cells

    # Write notebook
    demo_path = notebooks_dir / "demo.ipynb"
    with open(demo_path, "w", encoding="utf-8") as f:
        nbf.write(nb, f)

    print(f"✓ Created demo notebook: {demo_path}")
    return demo_path

if __name__ == "__main__":
    create_demo_notebook()
````

#### Task 1.2: Update README Binder Badge

````markdown
# ...existing content...

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/YOUR_USERNAME/clausemate/main?urlpath=lab%2Ftree%2Fnotebooks%2Fdemo.ipynb)

# ...existing content...
````

### Phase 2: Fix Module Import Issues

**Goal**: Ensure scripts run from any location without ModuleNotFoundError

#### Task 2.1: Create Package Installation Script

````python
#!/usr/bin/env python3
"""Setup development environment for ClauseMate."""

import subprocess
import sys
from pathlib import Path

def setup_environment():
    """Install ClauseMate in editable mode for development."""

    project_root = Path(__file__).resolve().parents[1]

    print("Setting up ClauseMate development environment...")
    print(f"Project root: {project_root}")

    # Install in editable mode
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-e", "."
        ], cwd=project_root)
        print("✓ ClauseMate installed in editable mode")

        # Verify imports work
        subprocess.check_call([
            sys.executable, "-c",
            "from src.main import main; print('✓ Import verification successful')"
        ], cwd=project_root)

        return True

    except subprocess.CalledProcessError as e:
        print(f"❌ Setup failed: {e}")
        return False

if __name__ == "__main__":
    success = setup_environment()
    sys.exit(0 if success else 1)
````

#### Task 2.2: Add Robust Path Handling to Scripts

````python
#!/usr/bin/env python3
"""
Multi-file analysis script with robust path handling.
"""
import sys
from pathlib import Path

# Add project root to Python path for imports
project_root = Path(__file__).resolve().parents[1]
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

# ...existing imports...
try:
    from src.multi_file.multi_file_batch_processor import MultiFileBatchProcessor
except ImportError as e:
    print(f"❌ Import error: {e}")
    print(f"Project root: {project_root}")
    print("Try running: pip install -e . from the project root")
    sys.exit(1)

# ...existing code...
````

### Phase 3: Development Environment Setup

**Goal**: Provide clear setup instructions for WSL/Docker environments

#### Task 3.1: WSL Development Guide

````markdown
# ClauseMate WSL Development Setup

## Prerequisites
- Windows Subsystem for Linux (WSL2)
- Docker Desktop (optional)

## WSL Setup

### 1. Access Project in WSL
```bash
# Navigate to mounted Windows drive
cd /mnt/c/GitHub/clausemate

# Verify files are accessible
ls -la
```

### 2. Python Environment
```bash
# Install Python 3.8+ if not available
sudo apt update
sudo apt install python3 python3-pip python3-venv

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install ClauseMate in development mode
pip install -e .[dev]
```

### 3. Verify Installation
```bash
# Test imports
python -c "from src.main import main; print('✓ Imports working')"

# Run analysis
python -m src.main

# Run tests
nox -s test
```

### 4. Jupyter Development
```bash
# Install Jupyter
pip install jupyter

# Start Jupyter Lab (accessible from Windows browser)
jupyter lab --no-browser --ip=0.0.0.0 --port=8888

# Open in Windows browser: http://localhost:8888
```

## Docker Alternative

### Option 1: Development Container
```bash
# Build development image
docker build -t clausemate-dev .

# Run with volume mount
docker run --rm -it \
  -p 8888:8888 \
  -v /mnt/c/GitHub/clausemate:/workspace \
  -w /workspace \
  clausemate-dev bash
```

### Option 2: Jupyter Container
```bash
# Quick Jupyter setup
docker run --rm -p 8888:8888 \
  -v /mnt/c/GitHub/clausemate:/home/jovyan/work \
  jupyter/scipy-notebook:latest
```
````

#### Task 3.2: Create Dockerfile for Development

````dockerfile
FROM python:3.11-slim

WORKDIR /workspace

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt pyproject.toml ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Install ClauseMate in development mode
RUN pip install -e .[dev]

# Default command
CMD ["python", "-m", "src.main"]
````

### Phase 4: Testing and Validation

**Goal**: Ensure all fixes work across environments

#### Task 4.1: Environment Test Script

````python
#!/usr/bin/env python3
"""Test ClauseMate setup across different environments."""

import subprocess
import sys
from pathlib import Path

def test_imports():
    """Test that all imports work correctly."""
    try:
        from src.main import main
        from src.config import FilePaths
        from src.data.models import SentenceContext
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
        result = subprocess.run([
            sys.executable, "-m", "src.main", "--help"
        ], cwd=project_root, capture_output=True, text=True, timeout=10)

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

def main():
    """Run all environment tests."""
    print("Testing ClauseMate environment setup...")

    tests = [
        ("Import test", test_imports),
        ("Script execution", test_script_execution),
        ("Notebook creation", test_notebook_creation)
    ]

    results = []
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
````

## Execution Timeline

### Immediate (Next 30 minutes)

1. ✅ Run `python tools/create_demo_notebook.py` to create demo notebook
2. ✅ Update README.md with correct Binder badge URL
3. ✅ Run `python tools/setup_dev_environment.py` to fix import issues

### Short-term (Next 2 hours)

4. ✅ Test script execution: `python run_multi_file_analysis.py --verbose`
5. ✅ Create WSL setup documentation
6. ✅ Test Binder functionality with new demo notebook

### Medium-term (Next day)

7. ✅ Create Dockerfile for containerized development
8. ✅ Validate all environments with test script
9. ✅ Update main README with complete setup instructions

## Success Criteria

- [ ] **Binder auto-opens demo notebook** showing ClauseMate capabilities
- [ ] **Scripts run without ModuleNotFoundError** from any directory
- [ ] **WSL environment** supports full development workflow
- [ ] **Docker container** provides reproducible analysis environment
- [ ] **All tests pass** in environment validation script

This plan addresses the core issues while maintaining ClauseMate's modular architecture and German linguistic research focus.
