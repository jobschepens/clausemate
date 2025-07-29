# Optional Tests

This directory contains tests that require optional dependencies that may not be available in all environments, particularly CI/CD pipelines.

## Tests in this directory:

### `test_property_based.py`
- **Requires**: `hypothesis` package
- **Purpose**: Property-based testing for data validation and edge cases
- **Install**: `pip install hypothesis` or `pip install -e ".[dev]"`

### `test_benchmark.py`
- **Requires**: `psutil` package
- **Purpose**: Performance benchmarking and system resource monitoring tests
- **Install**: `pip install psutil` or `pip install -e ".[benchmark]"`

## Running Optional Tests

To run these tests locally when you have the required dependencies installed:

```bash
# Run all optional tests
pytest tests/optional/ -v

# Run specific optional test files
pytest tests/optional/test_property_based.py -v
pytest tests/optional/test_benchmark.py -v

# Run with coverage
pytest tests/optional/ --cov=src --cov-report=term-missing
```

## CI/CD Exclusion

These tests are excluded from the main CI/CD pipeline via `pytest.ini` configuration (`--ignore=tests/optional`) to prevent failures when optional dependencies are not installed. The main test suite runs without these dependencies to ensure core functionality works in minimal environments.

## Installing Optional Dependencies

To install all optional dependencies for local development:

```bash
# Install development dependencies (includes hypothesis)
pip install -e ".[dev]"

# Install benchmark dependencies (includes psutil)
pip install -e ".[benchmark]"

# Install all optional dependencies
pip install -e ".[dev,benchmark]"