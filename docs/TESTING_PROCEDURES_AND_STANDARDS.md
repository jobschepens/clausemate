# Testing Procedures and Standards

## Overview

This document outlines the comprehensive testing procedures and standards for the ClauseMate project. It serves as a guide for developers to understand, maintain, and extend the testing framework.

## Table of Contents

1. [Testing Philosophy](#testing-philosophy)
2. [Test Organization](#test-organization)
3. [Test Categories](#test-categories)
4. [Testing Standards](#testing-standards)
5. [Test Execution](#test-execution)
6. [Test Data Management](#test-data-management)
7. [Continuous Integration](#continuous-integration)
8. [Best Practices](#best-practices)
9. [Troubleshooting](#troubleshooting)

## Testing Philosophy

### Core Principles

1. **Test Pyramid**: Focus on unit tests (fast, isolated), supported by integration tests (realistic workflows), and minimal end-to-end tests
2. **Test-Driven Development**: Write tests before or alongside implementation
3. **Comprehensive Coverage**: Aim for high test coverage while focusing on critical paths
4. **Maintainable Tests**: Write clear, readable tests that serve as documentation
5. **Fast Feedback**: Prioritize quick test execution for rapid development cycles

### Quality Gates

- **Minimum Coverage**: 25% overall coverage (currently achieving 58.96%)
- **Critical Path Coverage**: 80%+ coverage for core functionality
- **No Failing Tests**: All tests must pass before merging
- **Performance Regression**: No significant performance degradation

## Test Organization

### Directory Structure

```
tests/
├── fixtures/                 # Test data and fixtures
│   ├── sample_tsvs/          # Sample TSV files for all formats
│   ├── expected_outputs/     # Golden master files
│   └── mock_data/            # Mock objects and factories
├── unit/                     # Unit tests
│   ├── test_data_models.py   # Data model validation
│   └── test_main_analyzer.py # Main analyzer components
├── integration/              # Integration tests
│   └── test_format_processing.py # End-to-end format processing
├── property/                 # Property-based tests
│   └── test_property_based.py # Hypothesis-based testing
├── generators/               # Test data generators
│   └── test_data_generators.py # Synthetic TSV generation
└── conftest.py              # Pytest configuration and fixtures
```

### File Naming Conventions

- **Test files**: `test_*.py`
- **Test classes**: `Test*` (PascalCase)
- **Test methods**: `test_*` (snake_case)
- **Fixtures**: `*_fixture` or descriptive names
- **Mock objects**: `mock_*` or `Mock*`

## Test Categories

### 1. Unit Tests (`@pytest.mark.unit`)

**Purpose**: Test individual components in isolation

**Characteristics**:
- Fast execution (< 1ms per test)
- No external dependencies
- Use mocking for dependencies
- Focus on single responsibility

**Example**:
```python
@pytest.mark.unit
def test_token_creation_valid():
    """Test valid token creation."""
    token = Token(idx=1, text="word", sentence_num=1,
                  grammatical_role="SUBJ", thematic_role="AGENT")
    assert token.idx == 1
    assert token.text == "word"
```

### 2. Integration Tests (`@pytest.mark.integration`)

**Purpose**: Test component interactions and workflows

**Characteristics**:
- Moderate execution time (< 1s per test)
- Test realistic scenarios
- Use real data when possible
- Validate end-to-end functionality

**Example**:
```python
@pytest.mark.integration
def test_format_detection_and_processing():
    """Test complete format detection and processing workflow."""
    analyzer = ClauseMateAnalyzer()
    relationships = analyzer.analyze_file("sample.tsv")
    assert len(relationships) > 0
```

### 3. Property-Based Tests (`@pytest.mark.property`)

**Purpose**: Test system properties with generated data

**Characteristics**:
- Use Hypothesis for data generation
- Test invariants and properties
- Discover edge cases automatically
- Validate assumptions

**Example**:
```python
@pytest.mark.property
@given(valid_token_data())
def test_token_creation_always_valid(token_data):
    """Test that valid token data always creates valid tokens."""
    token = Token(**token_data)
    assert token.idx > 0
    assert len(token.text.strip()) > 0
```

### 4. Performance Tests (`@pytest.mark.performance`)

**Purpose**: Validate performance characteristics

**Characteristics**:
- Measure execution time and memory usage
- Establish performance baselines
- Detect performance regressions
- Test scalability

**Example**:
```python
@pytest.mark.performance
def test_processing_performance(analyzer, sample_files):
    """Test processing performance meets baseline requirements."""
    start_time = time.time()
    analyzer.analyze_file(sample_file)
    processing_time = time.time() - start_time
    assert processing_time < MAX_PROCESSING_TIME
```

### 5. Slow Tests (`@pytest.mark.slow`)

**Purpose**: Tests that take significant time to execute

**Characteristics**:
- Execution time > 5 seconds
- Comprehensive integration scenarios
- Large dataset processing
- Can be skipped during development

## Testing Standards

### Code Quality

1. **Test Readability**:
   - Clear, descriptive test names
   - Arrange-Act-Assert pattern
   - Minimal setup and teardown
   - Self-documenting assertions

2. **Test Independence**:
   - Tests should not depend on each other
   - Use fixtures for shared setup
   - Clean up resources after tests
   - Avoid global state modifications

3. **Error Handling**:
   - Test both success and failure paths
   - Use `pytest.raises()` for exception testing
   - Validate error messages and types
   - Test edge cases and boundary conditions

### Mock Usage Guidelines

1. **When to Mock**:
   - External dependencies (files, network, databases)
   - Slow operations
   - Non-deterministic behavior
   - Complex setup requirements

2. **Mock Best Practices**:
   - Mock at the boundary of your system
   - Use `patch.object()` for specific methods
   - Verify mock calls when behavior matters
   - Keep mocks simple and focused

3. **Mock Patterns**:
```python
# Mock external dependencies
@patch('src.main.pandas.DataFrame')
def test_export_with_mocked_pandas(mock_df):
    # Test implementation
    pass

# Mock object methods
with patch.object(analyzer.parser, 'parse_file') as mock_parse:
    mock_parse.return_value = expected_data
    result = analyzer.analyze_file("test.tsv")
```

### Assertion Guidelines

1. **Specific Assertions**:
   - Use specific assertions over generic ones
   - Test exact values when possible
   - Use `pytest.approx()` for floating-point comparisons

2. **Multiple Assertions**:
   - Group related assertions in single tests
   - Use descriptive assertion messages
   - Consider using `assert_that()` for complex validations

3. **Custom Assertions**:
```python
def assert_valid_relationship(relationship):
    """Assert that a relationship object is valid."""
    assert relationship.sentence_num > 0
    assert len(relationship.pronoun.text) > 0
    assert len(relationship.clause_mate.text) > 0
```

## Test Execution

### Local Development

```bash
# Run all tests
pytest

# Run specific test categories
pytest -m unit                    # Unit tests only
pytest -m integration            # Integration tests only
pytest -m "not slow"             # Skip slow tests
pytest -m "unit or integration"  # Multiple categories

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test files
pytest tests/unit/test_data_models.py
pytest tests/integration/ -v

# Run tests matching pattern
pytest -k "test_token" -v
```

### Continuous Integration

```bash
# Full test suite with coverage
pytest --cov=src --cov-report=term-missing --cov-fail-under=25

# Performance regression testing
pytest -m performance --benchmark-only

# Property-based testing with more examples
pytest -m property --hypothesis-max-examples=100
```

### Test Configuration

Key pytest configuration options in `pyproject.toml`:

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = [
    "--cov=src",
    "--cov-report=term-missing",
    "--cov-report=html",
    "--cov-fail-under=25",
    "--strict-markers",
]
markers = [
    "unit: Unit tests",
    "integration: Integration tests",
    "property: Property-based tests",
    "performance: Performance tests",
    "slow: Slow tests",
]
```

## Test Data Management

### Fixtures

1. **Scope Management**:
   - `function`: Default, new instance per test
   - `class`: Shared within test class
   - `module`: Shared within test module
   - `session`: Shared across entire test session

2. **Fixture Dependencies**:
```python
@pytest.fixture
def sample_data():
    return {"key": "value"}

@pytest.fixture
def processed_data(sample_data):
    return process(sample_data)
```

### Test Data Files

1. **Sample TSV Files** (`tests/fixtures/sample_tsvs/`):
   - `standard_15col.tsv`: Standard format
   - `extended_37col.tsv`: Extended format
   - `legacy_14col.tsv`: Legacy format
   - `incomplete_12col.tsv`: Incomplete format

2. **Expected Outputs** (`tests/fixtures/expected_outputs/`):
   - Golden master files for regression testing
   - Version-controlled reference outputs
   - Format-specific expected results

3. **Generated Data** (`tests/generators/`):
   - Synthetic TSV file generation
   - Configurable test scenarios
   - Error injection capabilities

### Mock Data Factory

```python
from tests.fixtures.mock_data.mock_objects import MockDataFactory

factory = MockDataFactory()
token = factory.create_token(text="example")
relationship = factory.create_relationship()
```

## Continuous Integration

### GitHub Actions Integration

The project uses GitHub Actions for automated testing:

1. **Reproducibility Workflow** (`.github/workflows/reproducibility.yml`):
   - Tests across multiple Python versions
   - Validates reproducible results
   - Runs on push and pull requests

2. **Code Quality Workflow** (`.github/workflows/pylint.yml`):
   - Linting with pylint
   - Code style validation
   - Static analysis

### CI Best Practices

1. **Fast Feedback**:
   - Run unit tests first
   - Parallel test execution
   - Fail fast on critical errors

2. **Comprehensive Coverage**:
   - Full test suite on main branch
   - Performance regression testing
   - Cross-platform validation

3. **Artifact Management**:
   - Store test reports
   - Coverage reports
   - Performance benchmarks

## Best Practices

### Writing Effective Tests

1. **Test Naming**:
```python
# Good: Descriptive and specific
def test_token_creation_with_valid_data_succeeds():
    pass

def test_token_creation_with_negative_idx_raises_validation_error():
    pass

# Bad: Vague and unclear
def test_token():
    pass

def test_error():
    pass
```

2. **Test Structure**:
```python
def test_feature():
    # Arrange: Set up test data and conditions
    input_data = create_test_data()
    expected_result = calculate_expected()

    # Act: Execute the functionality being tested
    actual_result = function_under_test(input_data)

    # Assert: Verify the results
    assert actual_result == expected_result
```

3. **Parameterized Tests**:
```python
@pytest.mark.parametrize("input_value,expected", [
    ("valid_input", "expected_output"),
    ("another_input", "another_output"),
])
def test_function_with_various_inputs(input_value, expected):
    result = function_under_test(input_value)
    assert result == expected
```

### Test Maintenance

1. **Regular Review**:
   - Remove obsolete tests
   - Update tests for API changes
   - Refactor duplicated test code
   - Improve test coverage

2. **Performance Monitoring**:
   - Track test execution time
   - Identify slow tests
   - Optimize test performance
   - Monitor CI pipeline duration

3. **Documentation Updates**:
   - Keep test documentation current
   - Update examples and guidelines
   - Document new testing patterns
   - Share testing knowledge

## Troubleshooting

### Common Issues

1. **Import Errors**:
```python
# Solution: Add src to Python path
import sys
sys.path.append('src')
```

2. **Fixture Not Found**:
```python
# Solution: Check conftest.py location and fixture scope
@pytest.fixture(scope="session")
def shared_fixture():
    return create_shared_resource()
```

3. **Mock Not Working**:
```python
# Solution: Patch at the right location
# Patch where the function is used, not where it's defined
@patch('module_under_test.external_function')
```

4. **Flaky Tests**:
   - Use `pytest.mark.flaky` for known flaky tests
   - Add retries for network-dependent tests
   - Use deterministic test data
   - Avoid time-dependent assertions

### Debugging Tests

1. **Verbose Output**:
```bash
pytest -v -s  # Verbose with print statements
pytest --tb=long  # Detailed tracebacks
```

2. **Debug Mode**:
```python
import pytest
pytest.set_trace()  # Debugger breakpoint
```

3. **Test Isolation**:
```bash
pytest tests/unit/test_specific.py::TestClass::test_method
```

### Performance Issues

1. **Slow Tests**:
   - Profile test execution
   - Optimize fixture setup
   - Use appropriate test scope
   - Consider parallel execution

2. **Memory Issues**:
   - Clean up resources in teardown
   - Use memory-efficient test data
   - Monitor memory usage in CI

## Conclusion

This testing framework provides a solid foundation for maintaining code quality and reliability in the ClauseMate project. By following these procedures and standards, developers can:

- Write effective, maintainable tests
- Ensure comprehensive coverage of critical functionality
- Detect regressions early in the development cycle
- Maintain high code quality standards
- Facilitate confident refactoring and feature development

Regular review and updates of these procedures ensure the testing framework evolves with the project's needs and maintains its effectiveness over time.
