# Reproducibility Guide

This guide provides step-by-step instructions for reproducing the analysis results of the Clause Mates Analyzer project.

## Prerequisites

- Python 3.8 or later
- Git (for cloning the repository)

## Step 1: Clone the Repository

```bash
git clone https://github.com/jobschepens/clausemate.git
cd clausemate
```

## Step 2: Set Up the Environment

### Option A: Using pip (recommended)

```bash
# Create a virtual environment
python -m venv .venv

# Activate the virtual environment
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate

# Install exact dependencies from lock files
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

### Option B: Using conda

```bash
conda env create -f environment.yml
conda activate clausemate
```

## Step 3: Verify Installation

```bash
# Run all tests to ensure everything is working
nox -s test

# Verify the code quality
nox -s lint
```

## Step 4: Run the Analysis

```bash
# Run the Phase 2 analysis
python src/run_phase2.py
```

## Step 5: Verify Reproducibility

The output should be saved as `data/output/clause_mates_chap2_export.csv`. To verify that your results match the reference:

```bash
# Compare your output with the reference
python tools/compare_outputs.py data/output/clause_mates_chap2_export.csv data/output/reference/clause_mates_reference.csv
```

## Expected Results

- **Number of relationships**: 448
- **Number of columns**: 34
- **Cross-sentence antecedent detection success rate**: 94.4%

## Troubleshooting

### Common Issues

1. **Import Errors**: Ensure you've activated the virtual environment and installed all dependencies.

2. **File Not Found Errors**: Make sure you're running commands from the project root directory.

3. **Different Results**:
   - Check that you're using the exact dependency versions from the lock files
   - Ensure you're using the same Python version (3.8+)
   - Verify that the input data hasn't been modified

### Getting Help

If you encounter issues:
1. Check that all tests pass: `nox -s test`
2. Verify your environment matches the requirements
3. Compare your Python version with the supported versions (3.8-3.12)

## Lock File Information

This project uses pip-tools for dependency locking:
- `requirements.txt`: Production dependencies with exact versions
- `requirements-dev.txt`: Development dependencies with exact versions

To regenerate lock files (only if needed):
```bash
pip-compile requirements.in
pip-compile requirements-dev.in
```

## Reference Data

The reference output was generated on:
- **Date**: [Generated when this file was created]
- **Python Version**: [Version used for reference]
- **Platform**: [Platform used for reference]
- **Commit SHA**: [Git commit hash]

For any questions about reproducibility, please refer to the project documentation or open an issue on GitHub.
