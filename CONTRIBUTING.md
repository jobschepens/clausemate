# Contributing to ClauseMate

Thank you for your interest in contributing to the ClauseMate project! This guide will help you get started with development.

## Development Setup

### Prerequisites
- Python 3.8 or higher
- pip (recommended) or conda

### Recommended Setup: pip + venv

1. **Clone the repository**
   ```bash
   git clone https://github.com/jobschepens/clausemate.git
   cd clausemate
   ```

2. **Create and activate virtual environment**
   ```bash
   # Create virtual environment
   python -m venv .venv

   # Activate it
   # Windows:
   .venv\Scripts\activate
   # macOS/Linux:
   source .venv/bin/activate
   ```

3. **Install with development dependencies**
   ```bash
   pip install -e .[dev,benchmark]
   ```

### Alternative Setup: conda

1. **Create conda environment**
   ```bash
   conda env create -f environment.yml
   conda activate clausemate
   ```

## Development Workflow

### Code Quality Tools
This project uses **ruff** for fast, comprehensive code quality checking and formatting.

```bash
# Using nox (recommended - cross-platform)
nox                    # Run default sessions (lint, test)
nox -s lint            # Run linting
nox -s format          # Format code
nox -s test            # Run tests on current Python
nox -s test-3.9        # Run tests on Python 3.9
nox -s test-3.10       # Run tests on Python 3.10
nox -s ci              # Full CI pipeline
nox -l                 # List all available sessions

# Or use tools directly
ruff check src/        # Check for issues
ruff format src/       # Format code
ruff check --fix src/  # Auto-fix issues
```

### Multi-Python Testing
Nox makes it easy to test against multiple Python versions:

```bash
# Test on all supported versions (3.8-3.12)
nox -s test

# Test on specific version
nox -s test-3.9
nox -s test-3.11
```

### Pre-commit Hooks
Install pre-commit hooks to automatically check code quality before commits:

```bash
pre-commit install
```

### Running Tests
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src

# Run specific test file
pytest tests/test_phase2_components.py
```

### Project Structure
- `src/`: Main source code
- `tests/`: Unit tests
- `tools/`: Analysis and utility scripts
- `archive/`: Legacy code and previous phases
- `data/`: Input and output data files

## Code Standards

- **Configuration**: All tool configuration consolidated in `pyproject.toml`
- **Linting**: Ruff (replaces black, isort, flake8)
- **Type Checking**: mypy
- **Security**: bandit
- **Testing**: pytest
- **Pre-commit**: Automated quality checks

## Submitting Changes

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Make your changes
4. Run quality checks (`make ci-test`)
5. Commit your changes (`git commit -am 'Add some feature'`)
6. Push to the branch (`git push origin feature/your-feature`)
7. Create a Pull Request

## Questions?

For questions about the linguistic methodology or data format, please refer to the project documentation or contact the research team.
