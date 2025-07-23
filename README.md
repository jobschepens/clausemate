# Clause Mates Analyzer

> **⚠️ Disclaimer**: This repository contains experimental research code developed through iterative "vibe coding" sessions. While the functionality is complete and tested, the codebase reflects rapid prototyping, multiple refactoring attempts, and exploratory development. Code quality and organization may vary across different phases of development. Use with appropriate expectations for research/experimental software.

A Python tool for extracting and analyzing clause mate relationships from German pronoun data for linguistic research.

## Project Status

- ✅ **Phase 1 Complete**: Self-contained monolithic version with full functionality
- ✅ **Phase 2 Complete**: Modular architecture with streaming support and comprehensive testing
- 📋 **Phase 3 Planned**: Advanced features and configuration system

## Description

This tool analyzes German pronouns and their clause mates in annotated linguistic data. It identifies critical pronouns (personal, demonstrative, and d-pronouns) and extracts their relationships with other referential expressions in the same sentence.

### Critical Pronouns Analyzed
- **Third person personal**: er, sie, es, ihm, ihr, ihn, ihnen
- **D-pronouns (pronominal)**: der, die, das, dem, den, deren, dessen, derer  
- **Demonstrative**: dieser, diese, dieses, diesem, diesen

## Features

- Parse TSV files with linguistic annotations
- Extract coreference relationships between pronouns and clause mates
- Calculate antecedent distances and sentence locations
- Export structured data for statistical analysis
- Comprehensive error handling and logging
- Type-safe implementation with full type hints

## Project Structure

```
├── phase1/                     # Phase 1 - Self-contained monolithic version
│   ├── clause_mates_complete.py    # Main analysis script
│   ├── config.py                   # Phase 1 configuration and constants
│   ├── utils.py                    # Phase 1 utility functions  
│   ├── pronoun_classifier.py       # Phase 1 pronoun classification logic
│   ├── exceptions.py               # Phase 1 custom exception classes
│   └── README.md                   # Phase 1 documentation
├── src/                        # Phase 2 - Complete modular architecture
│   ├── main.py                     # Main orchestrator
│   ├── config.py                   # Phase 2 configuration
│   ├── exceptions.py               # Phase 2 exception handling
│   ├── utils.py                    # Phase 2 utility functions
│   ├── pronoun_classifier.py       # Phase 2 pronoun classification
│   ├── run_phase2.py               # Entry point script for Phase 2
│   ├── verify_phase2.py            # Testing and verification script
│   ├── parsers/                    # TSV parsing components
│   ├── extractors/                 # Feature extraction components
│   ├── analyzers/                  # Analysis components
│   └── data/                       # Data models and structures
├── exportscript.py             # Independent legacy analysis script
└── gotofiles/                  # Input data files
```

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd clause-mates-analyzer
```

2. Install dependencies:
```bash
pip install pandas
```

## Usage

### Phase 1 - Self-Contained Version
```bash
python phase1/clause_mates_complete.py
```
Output: `phase1/clause_mates_phase1_export.csv` (463 relationships, 35 columns)

### Phase 2 - Modular Architecture
```bash
# Method 1: Direct execution
python src/run_phase2.py

# Method 2: Module execution  
python -m src.main
```
Output: `clause_mates_chap2_export.csv` (448 relationships, 34 columns)

### Legacy Export Script
```bash
python exportscript.py
```
Output: `clause_mates_export.csv` (processes curation files)

### Testing Phase 2 Components
```bash
python src/verify_phase2.py
```

### Configuration

#### Phase 1 Configuration
Edit `phase1/config.py` to customize Phase 1 settings:
- Input/output file paths for Phase 1
- Column mappings and constants

#### Phase 2 Configuration  
Edit `src/config.py` to customize Phase 2 settings:
- Input/output file paths for Phase 2
- Processing parameters and column mappings

## Output Format

### Phase 1 Output
- **File**: `phase1/clause_mates_phase1_export.csv`
- **463 relationships** across 222 sentences
- **35 columns** with complete linguistic features

### Phase 2 Output  
- **File**: `clause_mates_chap2_export.csv`
- **448 relationships** across 222 sentences
- **34 columns** with streamlined feature set
- **Clause mate features**: text, coreference ID, animacy, givenness
- **Antecedent information**: distances to most recent and first mentions
- **Numeric variables**: for statistical analysis

## Development

### Phase 1 Achievements ✅
- Extracted all magic numbers and strings to `config.py`
- Added comprehensive type hints throughout codebase
- Implemented structured error handling with custom exceptions
- Modularized utility functions and pronoun logic
- Established clean code architecture

### Phase 2 Goals 🔄
- Split monolithic script into focused modules
- Eliminate code duplication (~30% → <5%)
- Add comprehensive unit tests (>80% coverage)
- Improve maintainability and developer experience
- Create clear module boundaries

### Phase 3 Plans 📋
- External configuration system
- Plugin architecture for extensible analysis
- Advanced logging and monitoring

## Contributing

This is a research project. For contributions:
1. Follow the established code style and type hints
2. Add tests for new functionality
3. Update documentation as needed
4. Ensure backward compatibility with existing data

## Requirements

- Python 3.8+
- pandas
- Standard library modules (re, logging, collections, typing)

## License

Research project - please contact maintainers for usage permissions.

## Contact

For questions about the linguistic methodology or data format, please refer to the project documentation or contact the research team.
