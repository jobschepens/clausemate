# AI Agent Prompt: ClauseMate Test Coverage Improvement

## Project Overview

You are working on **ClauseMate**, a German linguistic research tool for extracting clause mate relationships from annotated pronoun data. This is a sophisticated Python codebase with type safety, modular architecture, and comprehensive testing requirements.

**Current Status:**

- Coverage: 77.38% (2,569/3,320 lines covered)
- Tests: 367 passed, 36 failed, 8 skipped (403 total)
- Target: Improve to 85%+ coverage and fix all failing tests
- Repository: Has private research data via git submodule at `data/input/private/`

## Your Mission

Systematically improve test coverage and fix failing tests following the detailed implementation plan in `TEST_COVERAGE_IMPROVEMENT_PLAN.md`. Focus on high-impact improvements that bring the most coverage increase for the effort invested.

## Critical Context

### Repository Structure

- **Main repo**: Public ClauseMate analyzer code
- **Private data**: Git submodule at `data/input/private/` (may not be available)
- **Test data**: Use `data/input/gotofiles/2.tsv` for reproducible testing
- **Expected results**: 448 relationships from single file analysis

### Key Technologies

- **Python 3.11+** with strict type hints
- **pytest** for testing with coverage reporting
- **nox** for task automation (`nox -s test` to run tests)
- **ruff** for linting/formatting
- **mypy** for type checking

### Architecture Patterns

```python
# Dual execution support (all main modules)
try:
    from .config import FilePaths  # Module execution
except ImportError:
    from src.config import FilePaths  # Script execution

# Type-safe models (use dataclasses, not dicts)
from src.data.models import Token, SentenceContext, ClauseMateRelationship

# Extractor pattern
class MyExtractor(BaseExtractor[InputType, OutputType]):
    def extract(self, context: SentenceContext) -> list[OutputType]:
        # Implementation
```

## Critical Issues to Fix First

### 1. SentenceContext Constructor (BLOCKING MANY TESTS)

**Problem**: Tests failing with "missing 2 required positional arguments: 'critical_pronouns' and 'coreference_phrases'"

**Files affected**: All tests using SentenceContext
**Action**: Check current SentenceContext constructor in `src/data/models.py` and fix test fixtures

### 2. Mock Setup Issues

**Problem**: "'<' not supported between instances of 'MagicMock' and 'int'"
**Files**: `tests/test_multi_file_batch_processor.py`, others
**Action**: Fix mock objects to use proper comparable values

### 3. Missing Dictionary Keys

**Problem**: `KeyError: 'morphological'` in `src/parsers/incomplete_format_parser.py:414`
**Action**: Ensure all expected keys exist in `available_features` dictionary

## High-Impact Coverage Targets

### Priority Order (from TEST_COVERAGE_IMPROVEMENT_PLAN.md)

1. **Critical Fixes** (Fix failing tests first)
2. **High Priority** (Coverage < 70%):
   - `src/utils/data_source_loader.py`: 0% → 70%+
   - `src/extractors/pronoun_extractor.py`: 59% → 85%+
   - `src/extractors/phrase_extractor.py`: 66% → 85%+
   - `src/extractors/coreference_extractor.py`: 65% → 85%+

3. **Medium Priority** (70-80% coverage):
   - `src/parsers/tsv_parser.py`: 74% → 85%+
   - `src/multi_file/advanced_analysis_features.py`: 76% → 85%+

4. **Major Improvement** (Very low coverage):
   - `src/visualization/interactive_visualizer.py`: 12% → 60%+
   - `src/utils/__init__.py`: 40% → 70%+

## Commands You Need

```bash
# Run tests with coverage
nox -s test

# Run specific test file
pytest tests/test_pronoun_extractor.py -v

# Check current coverage for specific file
pytest --cov=src.extractors.pronoun_extractor --cov-report=term-missing

# Format code
nox -s format

# Type check
nox -s mypy

# Test with actual data (if available)
python src/main.py data/input/gotofiles/2.tsv
```

## Implementation Strategy

### Phase 1: Critical Fixes (START HERE)

1. **Fix SentenceContext constructor issues**
   - Check `src/data/models.py` for current constructor signature
   - Update ALL test files that create SentenceContext objects
   - Ensure required parameters are provided

2. **Fix mock setup in multi-file tests**
   - Replace MagicMock with proper values for sentence_num, idx attributes
   - Ensure comparable types for sorting operations

3. **Fix missing dictionary keys**
   - Add missing keys to `available_features` initialization

### Phase 2: High-Impact Improvements

1. **data_source_loader.py (0% coverage)**
   - Test all methods: `get_data_directory()`, `update_private_repository()`, etc.
   - Test environment variable handling
   - Test git repository operations

2. **Pronoun/Phrase/Coreference Extractors**
   - Test extraction logic with various input scenarios
   - Test error handling and edge cases
   - Test coreference chain building across sentences

### Phase 3: Medium Priority

- Parser improvements
- Advanced analysis features
- Integration testing

### Phase 4: Major Features

- Visualization module (currently 12%)
- Utils module comprehensive testing

## Testing Patterns

### Unit Test Structure

```python
def test_method_name_scenario(self):
    """Test method under specific scenario."""
    # Arrange
    context = SentenceContext(
        sentence_id="1",
        sentence_num=1,
        tokens=[...],
        first_words="Karl_sagte",
        critical_pronouns=[...],  # Don't forget required params!
        coreference_phrases=[...]
    )

    # Act
    result = extractor.extract(context)

    # Assert
    assert len(result) == expected_count
    assert result[0].attribute == expected_value
```

### Error Testing

```python
def test_method_handles_invalid_input(self):
    """Test method with invalid input."""
    with pytest.raises(SpecificException) as exc_info:
        method_under_test(invalid_input)
    assert "expected error message" in str(exc_info.value)
```

## Validation

### Success Criteria

- **All 36 failing tests pass**
- **Coverage improves from 77.38% to 85%+**
- **No new test failures introduced**
- **Code follows existing patterns and type hints**

### Verification Commands

```bash
# Check overall progress
nox -s test

# Verify specific improvements
pytest --cov=src.extractors --cov-report=term-missing

# Ensure functionality still works
python src/main.py data/input/gotofiles/2.tsv  # Should output ~448 relationships
```

## Important Notes

1. **Preserve existing functionality** - Don't break working code
2. **Follow type hints** - Use mypy-compatible code
3. **Use existing patterns** - Follow the dual-execution and dataclass patterns
4. **Test incrementally** - Run tests frequently to catch issues early
5. **Focus on failing tests first** - Fix the 36 failures before adding new tests

## Files to Focus On

**Critical (fix first):**

- All test files using SentenceContext
- `tests/test_multi_file_batch_processor.py`
- `src/parsers/incomplete_format_parser.py`

**High-impact (after critical fixes):**

- `src/utils/data_source_loader.py` and its tests
- `src/extractors/pronoun_extractor.py` and its tests
- `src/extractors/phrase_extractor.py` and its tests
- `src/extractors/coreference_extractor.py` and its tests

Start with the critical fixes to get the test suite stable, then systematically work through the high-impact coverage improvements. The detailed implementation plan in `TEST_COVERAGE_IMPROVEMENT_PLAN.md` provides specific guidance for each module.

Good luck! Focus on one issue at a time and verify your changes frequently.
