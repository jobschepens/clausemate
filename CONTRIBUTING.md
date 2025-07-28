# Contributing to Clause Mates Analyzer

Thank you for your interest in contributing to the Clause Mates Analyzer project! This document provides guidelines for contributing to this German linguistic research tool.

## Project Overview

The Clause Mates Analyzer is a research tool for analyzing pronoun-antecedent relationships in German text using WebAnno TSV format data. The project has achieved 100% compatibility across different WebAnno annotation schemes through adaptive parsing technology.

### Current System Capabilities
- **Adaptive Parsing**: Automatic format detection and parser selection
- **100% File Compatibility**: Supports 4 different WebAnno TSV format variations (12-38 columns)
- **Preamble-based Column Mapping**: Dynamic schema detection from WebAnno metadata
- **Comprehensive Testing**: 6/6 tests passing with full coverage
- **Timestamped Output**: Automatic organization of analysis results

## Development Setup

### Prerequisites
- Python 3.8 or higher
- Git
- Either Conda or pip for package management

### Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/jobschepens/clausemate.git
   cd clausemate
   ```

2. **Set up development environment**

   **Option A: Using Conda (Recommended)**
   ```bash
   conda env create -f environment.yml
   conda activate clausemate
   ```

   **Option B: Using pip**
   ```bash
   pip install -e ".[dev]"
   ```

3. **Install development tools**
   ```bash
   make dev-setup  # Installs pre-commit hooks
   ```

4. **Validate setup**
   ```bash
   make validate-setup
   make test
   ```

### Project Structure

```
clausemate/
├── src/                       # Main source code
│   ├── __init__.py
│   ├── main.py               # Entry point
│   ├── config.py             # Configuration management
│   ├── parsers/              # Format-specific parsers
│   │   ├── adaptive_tsv_parser.py
│   │   ├── incomplete_format_parser.py
│   │   └── legacy_tsv_parser.py
│   └── utils/                # Utility modules
│       ├── format_detector.py
│       └── preamble_parser.py
├── data/                     # Input and output data
│   ├── input/               # Source TSV files with documentation
│   └── output/              # Timestamped analysis results
├── tests/                   # Test suite
├── archive/                 # Historical versions and analysis
├── tools/                   # Development and analysis scripts
├── docs/                    # Project documentation
├── pyproject.toml          # Modern Python packaging
├── environment.yml         # Conda environment specification
└── Makefile               # Development task automation
```

## Development Workflow

### Code Quality Standards

We maintain high code quality through automated tools:

- **Linting & Formatting**: Ruff (replaces black, isort, flake8)
- **Type Checking**: MyPy with strict configuration
- **Testing**: Pytest with coverage reporting
- **Pre-commit Hooks**: Automated quality checks

### Making Changes

1. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**
   - Follow existing code style and patterns
   - Add tests for new functionality
   - Update documentation as needed

3. **Run quality checks**
   ```bash
   make lint      # Run ruff linting
   make format    # Format code with ruff
   make typecheck # Run mypy type checking
   make test      # Run test suite
   ```

4. **Commit your changes**
   ```bash
   git add .
   git commit -m "feat: add new feature description"
   ```

   Use conventional commit messages:
   - `feat:` for new features
   - `fix:` for bug fixes
   - `docs:` for documentation changes
   - `test:` for test additions/changes
   - `refactor:` for code refactoring

5. **Push and create pull request**
   ```bash
   git push origin feature/your-feature-name
   ```

### Testing Guidelines

#### Running Tests
```bash
# Run all tests
make test

# Run specific test file
pytest tests/test_adaptive_parser.py -v

# Run with coverage
make test-coverage

# Run integration tests
make test-integration
```

#### Writing Tests
- Place tests in the `tests/` directory
- Use descriptive test names: `test_adaptive_parser_handles_extended_format`
- Include both unit tests and integration tests
- Test edge cases and error conditions
- Maintain test coverage above 80%

#### Test Structure
```python
import pytest
from src.parsers.adaptive_tsv_parser import AdaptiveTSVParser

class TestAdaptiveTSVParser:
    def test_parser_detects_standard_format(self):
        """Test that parser correctly identifies standard 15-column format."""
        # Arrange
        parser = AdaptiveTSVParser()

        # Act
        result = parser.detect_format("data/input/gotofiles/2.tsv")

        # Assert
        assert result.format_type == "standard"
        assert result.column_count == 15
```

### Code Style Guidelines

#### Python Style
- Follow PEP 8 conventions
- Use type hints for all function parameters and return values
- Write docstrings for all public functions and classes
- Keep functions focused and under 50 lines when possible
- Use meaningful variable and function names

#### Example Code Style
```python
from typing import List, Optional, Dict, Any
from dataclasses import dataclass

@dataclass
class TSVFormatInfo:
    """Information about detected TSV format structure."""
    format_type: str
    column_count: int
    has_morphology: bool
    schema_layers: List[str]

def detect_format(file_path: str) -> TSVFormatInfo:
    """
    Detect TSV format from file preamble and structure.

    Args:
        file_path: Path to the TSV file to analyze

    Returns:
        TSVFormatInfo object with detected format details

    Raises:
        FileNotFoundError: If the specified file doesn't exist
        ValueError: If the file format cannot be determined
    """
    # Implementation here
    pass
```

#### Documentation Style
- Use Google-style docstrings
- Include type information in docstrings
- Provide examples for complex functions
- Document all parameters, return values, and exceptions

## Contributing Areas

### 1. Core Parser Development
- **Adaptive Parsing**: Enhance format detection algorithms
- **New Format Support**: Add support for additional WebAnno variations
- **Performance Optimization**: Improve parsing speed for large files

### 2. Linguistic Features
- **Morphological Analysis**: Extract pronoun type and gender information
- **Enhanced Antecedent Detection**: Improve antecedent choice algorithms
- **Discourse Analysis**: Add information structure features

### 3. Testing & Quality Assurance
- **Test Coverage**: Expand test suite for edge cases
- **Integration Tests**: Add end-to-end testing scenarios
- **Performance Testing**: Benchmark parsing performance

### 4. Documentation
- **User Guides**: Create tutorials for different use cases
- **API Documentation**: Document all public interfaces
- **Format Specifications**: Document supported file formats

### 5. Tools & Utilities
- **Analysis Scripts**: Create tools for data exploration
- **Validation Tools**: Build format validation utilities
- **Visualization**: Add data visualization capabilities

## Submitting Issues

### Bug Reports
When reporting bugs, please include:
- Python version and operating system
- Complete error message and stack trace
- Minimal code example that reproduces the issue
- Input file format details (if applicable)

### Feature Requests
For feature requests, please provide:
- Clear description of the proposed feature
- Use case and motivation
- Suggested implementation approach (if any)
- Potential impact on existing functionality

### Issue Templates
Use the provided issue templates:
- **Bug Report**: For reporting problems
- **Feature Request**: For suggesting enhancements
- **Documentation**: For documentation improvements

## Code Review Process

### Review Criteria
All contributions are reviewed for:
- **Functionality**: Does the code work as intended?
- **Code Quality**: Is the code well-structured and readable?
- **Testing**: Are there adequate tests for the changes?
- **Documentation**: Is the code properly documented?
- **Compatibility**: Does it maintain backward compatibility?

### Review Timeline
- Initial review within 48 hours
- Follow-up reviews within 24 hours
- Merge after approval from at least one maintainer

## Release Process

### Version Numbering
We use semantic versioning (SemVer):
- **Major** (X.0.0): Breaking changes
- **Minor** (0.X.0): New features, backward compatible
- **Patch** (0.0.X): Bug fixes, backward compatible

### Release Checklist
- [ ] All tests pass
- [ ] Documentation updated
- [ ] Version number bumped
- [ ] Changelog updated
- [ ] Performance benchmarks run
- [ ] Integration tests pass

## Getting Help

### Communication Channels
- **GitHub Issues**: For bug reports and feature requests
- **GitHub Discussions**: For questions and general discussion
- **Email**: Contact maintainers for sensitive issues

### Resources
- **Project Documentation**: See `docs/` directory
- **Format Specifications**: See `data/input/FORMAT_OVERVIEW.md`
- **Development Tools**: See `Makefile` for available commands

### Mentorship
New contributors are welcome! We provide:
- Code review feedback and guidance
- Help with development environment setup
- Assistance with understanding the codebase
- Pairing sessions for complex features

## Recognition

### Contributors
All contributors are recognized in:
- `CONTRIBUTORS.md` file
- Release notes
- Project documentation

### Types of Contributions
We value all types of contributions:
- Code contributions
- Documentation improvements
- Bug reports and testing
- Feature suggestions
- Community support

## License

By contributing to this project, you agree that your contributions will be licensed under the same license as the project. Please see the LICENSE file for details.

## Code of Conduct

This project follows a code of conduct to ensure a welcoming environment for all contributors. Please read and follow our community guidelines.

---

## Quick Reference

### Common Commands
```bash
# Development setup
make dev-setup

# Code quality
make lint format typecheck

# Testing
make test test-coverage test-integration

# Build and validation
make validate-setup benchmark

# Clean up
make clean
```

### File Locations
- **Source code**: `src/`
- **Tests**: `tests/`
- **Documentation**: `docs/` and root `.md` files
- **Configuration**: `pyproject.toml`, `environment.yml`
- **Data**: `data/input/` and `data/output/`

### Key Concepts
- **Adaptive Parsing**: Automatic format detection and parser selection
- **Preamble-based Mapping**: Column mapping from WebAnno metadata
- **Format Compatibility**: Support for multiple TSV variations
- **Timestamped Output**: Organized results with automatic dating

Thank you for contributing to the Clause Mates Analyzer project! Your contributions help advance German linguistic research and improve tools for the research community.
