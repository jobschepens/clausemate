# Clause Mates Analyzer

<!-- Badges -->
<p align="left">
  <a href="https://github.com/jobschepens/clausemate/actions">
    <img src="https://github.com/jobschepens/clausemate/actions/workflows/python-app.yml/badge.svg" alt="Build Status">
  </a>
  <a href="https://codecov.io/gh/jobschepens/clausemate">
    <img src="https://codecov.io/gh/jobschepens/clausemate/branch/main/graph/badge.svg" alt="Coverage">
  </a>
  <a href="https://www.python.org/downloads/release/python-380/">
    <img src="https://img.shields.io/badge/python-3.8%2B-blue.svg" alt="Python 3.8+">
  </a>
  <a href="https://github.com/charliermarsh/ruff">
    <img src="https://img.shields.io/badge/linting-ruff-%23f7ca18" alt="Ruff Linting">
  </a>
  <a href="https://pre-commit.com/">
    <img src="https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit" alt="pre-commit">
  </a>
  <a href="https://github.com/jobschepens/clausemate/blob/main/LICENSE">
    <img src="https://img.shields.io/badge/license-research-lightgrey.svg" alt="License">
  </a>
  <a href="https://github.com/jobschepens/clausemate/tree/main/docs">
    <img src="https://img.shields.io/badge/docs-available-brightgreen.svg" alt="Docs">
  </a>
</p>

> **⚠️ Disclaimer**: This repository contains experimental research code developed through iterative "vibe coding" sessions. While the functionality is complete and tested, the codebase reflects rapid prototyping, multiple refactoring attempts, and exploratory development. Code quality and organization may vary across different phases of development. Use with appropriate expectations for research/experimental software.

A Python tool for extracting and analyzing clause mate relationships from German pronoun data for linguistic research.

## Project Status

- ✅ **Phase 1 Complete**: Self-contained monolithic version with full functionality
- ✅ **Phase 2 Complete**: Modular architecture with adaptive parsing and 100% file compatibility
- ✅ **Documentation Complete**: Comprehensive format documentation for all supported file types
- 📋 **Phase 3 Planned**: Enhanced morphological features and advanced analysis capabilities

> 📄 **Latest Achievement**: Complete WebAnno TSV format compatibility with adaptive parsing system supporting 4 different file formats (12-38 columns) with automatic format detection and graceful degradation.

## Description

This tool analyzes German pronouns and their clause mates in annotated linguistic data. It identifies critical pronouns (personal, demonstrative, and d-pronouns) and extracts their relationships with other referential expressions in the same sentence.

### Critical Pronouns Analyzed

- **Third person personal**: er, sie, es, ihm, ihr, ihn, ihnen
- **D-pronouns (pronominal)**: der, die, das, dem, den, deren, dessen, derer
- **Demonstrative**: dieser, diese, dieses, diesem, diesen

## Features

- **Adaptive TSV Parsing**: Supports multiple WebAnno TSV 3.3 format variations (12-38 columns)
- **Automatic Format Detection**: Preamble-based dynamic column mapping
- **100% File Compatibility**: Works with standard, extended, legacy, and incomplete formats
- **Cross-sentence Analysis**: Antecedent detection with 94.4% success rate
- **Comprehensive Documentation**: Detailed format specifications for all supported files
- **Robust Error Handling**: Graceful degradation and clear user feedback
- **Type-safe Implementation**: Full type hints and comprehensive testing
- **Timestamped Output**: Automatic organization with date/time-stamped directories

## Supported File Formats

| Format | Columns | Description | Relationships | Status |
|--------|---------|-------------|---------------|---------|
| **Standard** | 15 | Basic linguistic annotations | 448 | ✅ Fully supported |
| **Extended** | 37 | Rich morphological features | 234 | ✅ Fully supported |
| **Legacy** | 14 | Compact annotation set | 527 | ✅ Fully supported |
| **Incomplete** | 12 | Limited annotations | 695 | ✅ Graceful handling |

> 📊 **Format Documentation**: See [`data/input/FORMAT_OVERVIEW.md`](data/input/FORMAT_OVERVIEW.md) for comprehensive technical specifications.

## Project Structure

```
├── src/                        # Phase 2 - Complete modular architecture
│   ├── main.py                     # Main orchestrator with adaptive parsing
│   ├── config.py                   # Generalized configuration system
│   ├── parsers/                    # Adaptive TSV parsing components
│   │   ├── adaptive_tsv_parser.py      # Preamble-based dynamic parsing
│   │   ├── incomplete_format_parser.py # Specialized incomplete format handler
│   │   ├── preamble_parser.py          # WebAnno schema extraction
│   │   └── tsv_parser.py               # Legacy parser (fallback)
│   ├── extractors/                 # Feature extraction components
│   ├── utils/                      # Format detection and utilities
│   │   └── format_detector.py          # Automatic format analysis
│   └── data/                       # Data models and structures
├── data/                       # Input and output data
│   ├── input/                      # Source TSV files with documentation
│   │   ├── FORMAT_OVERVIEW.md          # Comprehensive format comparison
│   │   ├── gotofiles/                  # Standard and extended formats
│   │   │   ├── 2.tsv_DOCUMENTATION.md      # Standard format (15 cols)
│   │   │   └── later/                      # Alternative formats
│   │   │       ├── 1.tsv_DOCUMENTATION.md      # Extended format (37 cols)
│   │   │       ├── 3.tsv_DOCUMENTATION.md      # Legacy format (14 cols)
│   │   │       └── 4.tsv_DOCUMENTATION.md      # Incomplete format (12 cols)
│   │   └── output/                 # Timestamped analysis results
├── tests/                      # Comprehensive test suite
├── tools/                      # Analysis and utility scripts
└── docs/                       # Project documentation
```

## Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd clause-mates-analyzer
   ```

2. **Set up environment** (choose one):

   **Option A: pip (recommended)**
   ```bash
   python -m venv .venv
   # Windows:
   .venv\Scripts\activate
   # macOS/Linux:
   source .venv/bin/activate
   
   pip install -e .[dev,benchmark]
   ```

   **Option B: conda**
   ```bash
   conda env create -f environment.yml
   conda activate clausemate
   ```

## Usage

### Current System (Phase 2)

The system automatically detects file formats and selects the appropriate parser:

```bash
# Automatic format detection and adaptive parsing
python src/main.py data/input/gotofiles/2.tsv                    # Standard format
python src/main.py data/input/gotofiles/later/1.tsv              # Extended format  
python src/main.py data/input/gotofiles/later/3.tsv              # Legacy format
python src/main.py data/input/gotofiles/later/4.tsv              # Incomplete format

# Force legacy parser (disable adaptive features)
python src/main.py --disable-adaptive data/input/gotofiles/2.tsv

# Verbose output with format detection details
python src/main.py --verbose data/input/gotofiles/later/1.tsv
```

**Output**: Automatically creates timestamped directories in `data/output/YYYYMMDD_HHMMSS/`

### Analysis Results by Format

| File | Format | Sentences | Tokens | Relationships | Coreference Chains |
|------|--------|-----------|--------|---------------|-------------------|
| **2.tsv** | Standard | 222 | 3,665 | **448** | 235 |
| **1.tsv** | Extended | 127 | 2,267 | **234** | 195 |
| **3.tsv** | Legacy | 207 | 3,786 | **527** | 244 |
| **4.tsv** | Incomplete | 243 | 4,412 | **695** | 245 |

### Analysis Tools

```bash
# Generate comprehensive analysis reports
python tools/analyze_results.py

# Check file format compatibility
python tools/check_file_format.py

# Compare analysis outputs
python tools/compare_outputs.py
```

## Development

### Quick Start

```bash
# Install development dependencies
pip install -e .[dev,benchmark]

# Run quality checks
nox                      # Run default sessions (lint, test)
nox -s lint              # Fast ruff linting
nox -s format            # Code formatting
nox -s test              # Run tests
nox -s ci                # Full CI pipeline

# Run tests directly
pytest
```

### Code Quality

This project uses **ruff** for fast, comprehensive code quality checking and formatting:

- **ruff**: Fast linting and formatting (replaces black, isort, flake8)
- **mypy**: Type checking
- **pytest**: Testing framework
- **pre-commit**: Git hooks for quality assurance

## Requirements

- **Python**: 3.8+
- **Core Dependencies**: pandas, standard library modules
- **Development**: ruff, mypy, pytest, pre-commit

## Contributing

This is a research project. For contributions:

1. Follow the established code style and type hints
2. Add tests for new functionality
3. Update documentation as needed
4. Ensure backward compatibility with existing data

See [`CONTRIBUTING.md`](CONTRIBUTING.md) for detailed setup instructions.

## Reproducibility

For exact result reproduction, see [`REPRODUCIBILITY.md`](REPRODUCIBILITY.md) for step-by-step instructions using locked dependencies and reference outputs.

## License

Research project - please contact maintainers for usage permissions.

## Contact

For questions about the linguistic methodology or data format, please refer to the project documentation or contact the research team.
