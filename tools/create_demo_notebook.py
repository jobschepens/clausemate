#!/usr/bin/env python3
"""Generate ClauseMate demo notebook for Binder."""

from pathlib import Path

import nbformat as nbf


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
            "name": "python3",
        },
        "language_info": {"name": "python", "version": "3.8+"},
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
- Cross-sentence coreference tracking"""),
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
