# Clause Mates Analyzer

A Python tool for extracting and analyzing clause mate relationships from German pronoun data for linguistic research.

## Project Status

- ✅ **Phase 1 Complete**: Constants extraction, type hints, error handling, modularization
- 🔄 **Phase 2 Ready**: Structural improvements, testing, code deduplication  
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
├── clause_mates_complete.py    # Main analysis script
├── config.py                   # Configuration and constants
├── utils.py                    # Utility functions
├── pronoun_classifier.py       # Pronoun classification logic
├── exceptions.py               # Custom exception classes
├── phase2_improvement_plan.md  # Development roadmap
└── old/                       # Legacy scripts (archived)
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

### Basic Usage
```bash
python clause_mates_complete.py
```

The script will process the configured input file and generate:
- `clause_mates_chap2_export.csv` - Main analysis results
- `clause_mates_data_documentation.md` - Data structure documentation  
- `clause_mates_metadata.json` - Technical metadata

### Configuration

Edit `config.py` to customize:
- Input/output file paths
- Column mappings for TSV format
- Processing constants

## Output Format

Each row in the output represents one clause mate relationship:
- **37 columns total**
- **Pronoun features**: text, position, grammatical/thematic roles
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
