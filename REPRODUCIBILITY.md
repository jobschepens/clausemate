# Reproducibility Guide - Clause Mates Analyzer

This document provides step-by-step instructions for reproducing the results of the Clause Mates Analyzer, a German linguistic research tool that analyzes pronoun-antecedent relationships in WebAnno TSV format data.

## System Overview

The Clause Mates Analyzer has achieved **100% compatibility** across different WebAnno TSV format variations through adaptive parsing technology. The system automatically detects file formats and selects appropriate parsers to ensure consistent results.

### Current Capabilities
- **4 supported file formats** with different column structures (12-38 columns)
- **Adaptive parsing** with automatic format detection
- **Preamble-based column mapping** from WebAnno metadata
- **Timestamped output organization** for result tracking
- **Comprehensive testing suite** (6/6 tests passing)

## Quick Start

### Prerequisites
- Python 3.8 or higher
- Git (for cloning the repository)
- 8GB+ RAM recommended for processing large files

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/jobschepens/clausemate.git
   cd clausemate
   ```

2. **Set up environment (Choose one method)**

   **Method A: Using Conda (Recommended)**
   ```bash
   conda env create -f environment.yml
   conda activate clausemate
   ```

   **Method B: Using pip**
   ```bash
   pip install -e ".[dev]"
   ```

3. **Validate installation**
   ```bash
   python src/main.py --help
   ```

### Basic Usage

Run analysis on any supported file format:

```bash
# Standard format (15 columns, 448 relationships)
python src/main.py data/input/gotofiles/2.tsv

# Extended format (37 columns, 234 relationships)
python src/main.py data/input/gotofiles/later/1.tsv

# Legacy format (14 columns, 527 relationships)
python src/main.py data/input/gotofiles/later/3.tsv

# Incomplete format (12 columns, 695 relationships)
python src/main.py data/input/gotofiles/later/4.tsv
```

## Expected Results

### File Format Compatibility

| File | Format Type | Columns | Expected Relationships | Status |
|------|-------------|---------|----------------------|---------|
| `2.tsv` | Standard | 15 | 448 | ✅ Fully supported |
| `1.tsv` | Extended | 37 | 234 | ✅ Fully supported |
| `3.tsv` | Legacy | 14 | 527 | ✅ Fully supported |
| `4.tsv` | Incomplete | 12 | 695 | ✅ Fully supported |

### Output Structure

Each analysis produces timestamped results in `data/output/`:

```
data/output/
└── YYYY-MM-DD_HH-MM-SS/
    ├── clause_mates_analysis.csv    # Main results
    ├── processing_log.txt           # Detailed processing log
    ├── format_detection.json        # Format detection details
    └── metadata.json               # Run metadata
```

### Sample Output Verification

**Expected columns in `clause_mates_analysis.csv`:**
- `sentence_id`: Sentence identifier
- `pronoun_token_idx`: Position of pronoun in sentence
- `pronoun_token`: The pronoun text
- `pronoun_grammatical_role`: Grammatical role (subject, object, etc.)
- `pronoun_most_recent_antecedent_distance`: Distance to antecedent
- `num_clause_mates`: Number of clause mates found
- `clause_mate_animacy`: Animacy classification
- `clause_mate_givenness`: Information status
- `antecedent_choice_method1`: Antecedent choice result

## Detailed Reproduction Steps

### Step 1: Environment Setup

1. **Verify Python version**
   ```bash
   python --version  # Should be 3.8+
   ```

2. **Create isolated environment**
   ```bash
   # Using conda
   conda create -n clausemate-repro python=3.9
   conda activate clausemate-repro

   # Or using venv
   python -m venv clausemate-repro
   source clausemate-repro/bin/activate  # Linux/Mac
   # clausemate-repro\Scripts\activate   # Windows
   ```

3. **Install dependencies**
   ```bash
   pip install pandas>=1.3.0
   ```

### Step 2: Data Preparation

1. **Verify input files exist**
   ```bash
   ls -la data/input/gotofiles/2.tsv
   ls -la data/input/gotofiles/later/1.tsv
   ls -la data/input/gotofiles/later/3.tsv
   ls -la data/input/gotofiles/later/4.tsv
   ```

2. **Check file formats**
   ```bash
   head -20 data/input/gotofiles/2.tsv
   ```

### Step 3: Run Analysis

1. **Test with standard format first**
   ```bash
   python src/main.py data/input/gotofiles/2.tsv --verbose
   ```

2. **Verify expected output**
   - Check that 448 relationships are found
   - Verify output directory is created with timestamp
   - Confirm all expected output files are present

3. **Test all formats**
   ```bash
   # Run each format and verify relationship counts
   python src/main.py data/input/gotofiles/later/1.tsv --verbose  # Expect 234
   python src/main.py data/input/gotofiles/later/3.tsv --verbose  # Expect 527
   python src/main.py data/input/gotofiles/later/4.tsv --verbose  # Expect 695
   ```

### Step 4: Validate Results

1. **Check relationship counts**
   ```bash
   # Count relationships in each output file
   wc -l data/output/*/clause_mates_analysis.csv
   ```

2. **Verify format detection**
   ```bash
   # Check format detection logs
   grep "Format detected" data/output/*/processing_log.txt
   ```

3. **Compare with expected results**
   ```bash
   # Verify key statistics match expected values
   python -c "
   import pandas as pd
   df = pd.read_csv('data/output/[TIMESTAMP]/clause_mates_analysis.csv')
   print(f'Total relationships: {len(df)}')
   print(f'Unique pronouns: {df[\"pronoun_token\"].nunique()}')
   print(f'Average clause mates: {df[\"num_clause_mates\"].mean():.2f}')
   "
   ```

## Advanced Reproduction

### Running the Complete Test Suite

1. **Install development dependencies**
   ```bash
   pip install -e ".[dev]"
   ```

2. **Run all tests**
   ```bash
   python -m pytest tests/ -v
   ```

3. **Run integration tests**
   ```bash
   python -m pytest tests/test_integration.py -v
   ```

### Performance Benchmarking

1. **Time analysis runs**
   ```bash
   time python src/main.py data/input/gotofiles/2.tsv
   ```

2. **Memory usage monitoring**
   ```bash
   # Using memory_profiler (install with: pip install memory-profiler)
   mprof run python src/main.py data/input/gotofiles/2.tsv
   mprof plot
   ```

### Batch Processing

1. **Process all files at once**
   ```bash
   # Create batch processing script
   for file in data/input/gotofiles/2.tsv data/input/gotofiles/later/*.tsv; do
       echo "Processing $file..."
       python src/main.py "$file"
   done
   ```

2. **Compare batch results**
   ```bash
   # Compare relationship counts across all runs
   find data/output -name "clause_mates_analysis.csv" -exec wc -l {} \;
   ```

## Troubleshooting

### Common Issues

1. **Import errors**
   ```bash
   # Ensure you're in the project root directory
   pwd  # Should end with 'clausemate'

   # Check Python path
   python -c "import sys; print('\n'.join(sys.path))"
   ```

2. **File not found errors**
   ```bash
   # Verify file paths are correct
   find . -name "*.tsv" -type f
   ```

3. **Memory issues with large files**
   ```bash
   # Monitor memory usage
   python src/main.py data/input/gotofiles/2.tsv --verbose
   ```

4. **Inconsistent results**
   ```bash
   # Check for file modifications
   ls -la data/input/gotofiles/2.tsv

   # Verify Python version consistency
   python --version
   ```

### Debugging Steps

1. **Enable verbose logging**
   ```bash
   python src/main.py data/input/gotofiles/2.tsv --verbose
   ```

2. **Check format detection**
   ```bash
   python -c "
   from src.utils.format_detector import FormatDetector
   detector = FormatDetector()
   info = detector.detect_format('data/input/gotofiles/2.tsv')
   print(f'Format: {info.format_type}, Columns: {info.column_count}')
   "
   ```

3. **Validate input file structure**
   ```bash
   python -c "
   import pandas as pd
   df = pd.read_csv('data/input/gotofiles/2.tsv', sep='\t', comment='#', nrows=5)
   print(f'Columns: {len(df.columns)}')
   print(f'Shape: {df.shape}')
   "
   ```

## System Requirements

### Minimum Requirements
- **OS**: Windows 10, macOS 10.14, or Linux (Ubuntu 18.04+)
- **Python**: 3.8 or higher
- **RAM**: 4GB minimum, 8GB recommended
- **Storage**: 1GB free space for data and outputs
- **CPU**: Any modern processor (multi-core recommended for large files)

### Recommended Environment
- **Python**: 3.9 or 3.10
- **RAM**: 16GB for processing multiple large files
- **Storage**: 5GB for development and testing
- **OS**: Linux or macOS for best performance

### Dependencies
```
pandas>=1.3.0        # Core data processing
python>=3.8          # Minimum Python version

# Development dependencies (optional)
pytest>=7.0.0        # Testing framework
ruff>=0.1.0          # Linting and formatting
mypy>=1.0.0          # Type checking
```

## Validation Checklist

Use this checklist to verify successful reproduction:

### Basic Functionality
- [ ] Installation completed without errors
- [ ] All input files are accessible
- [ ] Basic analysis runs successfully on 2.tsv
- [ ] Output directory is created with timestamp
- [ ] Expected number of relationships found (448 for 2.tsv)

### Format Compatibility
- [ ] 1.tsv processes successfully (234 relationships)
- [ ] 3.tsv processes successfully (527 relationships)
- [ ] 4.tsv processes successfully (695 relationships)
- [ ] Format detection works correctly for each file
- [ ] No parsing errors or warnings

### Output Quality
- [ ] All expected output files are generated
- [ ] CSV files contain expected columns
- [ ] Processing logs show successful completion
- [ ] Metadata files contain correct information
- [ ] Results are consistent across multiple runs

### Advanced Features
- [ ] Verbose mode provides detailed logging
- [ ] Legacy mode (--disable-adaptive) works correctly
- [ ] Test suite passes (if development dependencies installed)
- [ ] Performance is acceptable for your use case

## Getting Help

### Documentation Resources
- **Format Specifications**: See `data/input/FORMAT_OVERVIEW.md`
- **API Documentation**: See docstrings in source code
- **Development Guide**: See `CONTRIBUTING.md`
- **Project Roadmap**: See `ROADMAP.md`

### Support Channels
- **GitHub Issues**: Report bugs or ask questions
- **GitHub Discussions**: Community support and discussions
- **Email**: Contact maintainers for urgent issues

### Reporting Issues

When reporting reproduction issues, please include:

1. **System information**
   ```bash
   python --version
   pip list | grep pandas
   uname -a  # Linux/Mac
   # systeminfo  # Windows
   ```

2. **Error messages**
   - Complete error traceback
   - Command that caused the error
   - Input file being processed

3. **Expected vs actual results**
   - What you expected to happen
   - What actually happened
   - Any differences in output

4. **Reproduction steps**
   - Exact commands used
   - Any modifications made
   - Environment setup details

## Citation

If you use this tool in your research, please cite:

```bibtex
@software{clausemate_analyzer,
  title={Clause Mates Analyzer: Adaptive Parsing for German Pronoun-Antecedent Analysis},
  author={[Author Names]},
  year={2024},
  url={https://github.com/jobschepens/clausemate},
  version={2.1}
}
```

---

**Last Updated**: 2024-07-28
**Version**: 2.1
**Compatibility**: All supported file formats (2.tsv, 1.tsv, 3.tsv, 4.tsv)

For the most up-to-date reproduction instructions, please check the project repository and documentation.
