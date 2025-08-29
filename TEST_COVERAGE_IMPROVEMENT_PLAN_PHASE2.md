# Test Coverage Improvement Plan - Phase 2 (Post-AI Agent Update)

## Current Status (Updated August 29, 2025)

- **Coverage**: 84.36% (target: 85%+)
- **Test Results**: 18 failed, 444 passed, 8 skipped (470 total)
- **Major Achievement**: Improved from 77.40% to 84.36% coverage
- **Progress**: Reduced failing tests from 36 to 18

## ✅ Completed Achievements (AI Agent Work)

- Fixed Critical SentenceContext Constructor Issues - Resolved 15+ failing tests
- Fixed Mock Setup Issues - Resolved multi-file test failures
- Fixed Missing Dictionary Keys - Resolved incomplete_format_parser issues
- Fixed Logger Name Mismatches - Resolved advanced_analysis_features and enhanced_output_system issues
- **Improved data_source_loader.py Coverage**: 0% → 98% ✅
- **Improved pronoun_extractor.py Coverage**: 59% → 100% ✅
- **Improved phrase_extractor.py Coverage**: 66% → 96% ✅
- **Improved coreference_extractor.py Coverage**: 65% → 100% ✅
- **Improved advanced_analysis_features.py Coverage**: 76% → 91% ✅

## 🎯 Remaining Critical Tasks

### 1. Fix Remaining 18 Failing Tests (Priority: HIGH)

#### Mock Object Comparison Issues

```bash
# Test command to identify specific failures
nox -s test -- -v --tb=short -k "test_analyze_character_tracking_basic or test_create_enhanced_csv_output_with_relationships"

# Common patterns causing failures:
# - MagicMock comparison issues in advanced_analysis_features.py
# - Mock attribute access in enhanced_output_system.py
# - JSON serialization of MagicMock objects
```

**Key Failing Tests to Fix:**

1. `test_advanced_analysis_features.py` - Character tracking assertions
2. `test_enhanced_output_system.py` - Mock attribute comparisons
3. `test_benchmark.py` - Archive phase1 import issues
4. `test_data_source_loader.py` - Path.stat() mock issues
5. `test_incomplete_format_parser.py` - Exception handling edge cases

### 2. Improve Key Module Coverage

#### tsv_parser.py (74% → 85%+)

**Current Missing Coverage Areas:**

- Lines 55-69: Error handling in token parsing
- Lines 306-323: WebAnno format edge cases
- Lines 331-341: Coreference link validation

#### interactive_visualizer.py (12% → 60%+)

**Major Gap - Only 12% covered:**

- Lines 95-316: Core visualization components
- Lines 334-496: Interactive features
- Lines 516-774: Plotly/Dash integration

#### utils/**init**.py (40% → 70%+)

**Missing Coverage:**

- Lines 25-156: Utility function implementations
- Import validation and error handling

### 3. Archive Phase1 Import Issues

**Problem**: `archive.phase1.clause_mates_complete` import failures
**Solution**: Mock or skip archive imports in benchmark tests

## 🚀 Continuation Prompts for AI Agents

### Prompt 1: Fix Mock Object Issues

```text
I need to fix mock object comparison issues in the ClauseMate project test suite. The main problems are:

1. MagicMock objects being compared with real values in assertions (test_advanced_analysis_features.py)
2. MagicMock objects being serialized to JSON causing TypeError (test_enhanced_output_system.py)
3. Mock attribute access issues with Path.stat() and sentence_range comparisons

Current status: 18 failing tests, 84.36% coverage
Focus on these test files:
- tests/test_advanced_analysis_features.py (lines with MagicMock assertions)
- tests/test_enhanced_output_system.py (JSON serialization issues)
- tests/test_data_source_loader.py (Path.stat mock issues)

Please fix the mock setup patterns to use proper return values instead of MagicMock objects for assertions.
```

### Prompt 2: Improve tsv_parser.py Coverage

```
I need to improve test coverage for src/parsers/tsv_parser.py from 74% to 85%+.

Missing coverage areas:
- Lines 55-69: Error handling in token parsing
- Lines 306-323: WebAnno format edge cases
- Lines 331-341: Coreference link validation
- Lines 403-404: File processing edge cases

This is a German linguistic analysis tool that parses WebAnno TSV 3.3 format files. The parser handles:
- Token IDs like "1-1", "2-5" (sentence-token format)
- Coreference links like "*->115-4"
- Grammatical roles: Subj, dirObj, indirObj
- Thematic roles: Proto-Ag, Proto-Pat

Current coverage: 74%, Target: 85%+
Please add comprehensive tests for the missing coverage areas, focusing on error conditions and edge cases.
```

### Prompt 3: Fix Archive Import Issues

```
I need to fix import issues with archive.phase1 modules in the benchmark tests. The problem:

Error: "AttributeError: module 'archive.phase1' has no attribute 'clause_mates_complete'"
       "ImportError: cannot import name 'extract_sentence_number' from 'utils'"

Failing tests:
- tests/test_benchmark.py::TestPerformanceBenchmark::test_compare_phases
- tests/test_benchmark.py::TestPerformanceBenchmark::test_compare_phases_missing_files
- tests/test_benchmark.py::TestPerformanceBenchmark::test_run_benchmarks

The benchmark tries to import from archive/phase1/ which is a legacy implementation. Please either:
1. Mock the archive imports in benchmark tests, OR
2. Skip benchmark tests that depend on archive phase1, OR
3. Fix the import paths to work with the current project structure

Focus on making tests pass without breaking the benchmark functionality.
```

### Prompt 4: Interactive Visualizer Coverage

```
I need to dramatically improve test coverage for src/visualization/interactive_visualizer.py from 12% to 60%+.

This module creates interactive visualizations using Plotly/Dash for German linguistic coreference analysis. It's currently almost untested.

Missing coverage (88% of the file):
- Lines 95-316: Core visualization components
- Lines 334-496: Interactive dashboard features
- Lines 516-774: Plotly chart generation

The module handles:
- Character tracking visualizations
- Coreference chain analysis
- Cross-chapter relationship mapping
- Interactive pronoun position analysis

Please create comprehensive mock-based tests that don't require actual Plotly/Dash rendering but test the data preparation and component logic.
```

### Prompt 5: Complete Final Push to 85%+

```
I need to complete the final push to reach 85%+ test coverage for the ClauseMate project.

Current status: 84.36% coverage, 18 failing tests
Target: 85%+ coverage, 0 failing tests

Remaining work:
1. Fix the last few failing tests (focus on mock issues)
2. Add edge case tests to push coverage over 85%
3. Focus on these modules still below target:
   - utils/__init__.py (40% → 70%+)
   - tsv_parser.py (74% → 85%+)
   - Any other modules below 85%

This is a German linguistic research tool for clause mate analysis. The project uses:
- WebAnno TSV 3.3 format parsing
- Coreference chain extraction
- Cross-sentence antecedent detection (94.4% success rate)
- German pronoun classification

Please complete the remaining test coverage improvements to reach the 85%+ target.
```

## 🔧 Technical Implementation Notes

### Mock Object Best Practices

```python
# ❌ Wrong - causes assertion failures
mock_obj = MagicMock()
assert result == mock_obj  # Fails: MagicMock != real value

# ✅ Correct - use return_value
mock_obj = MagicMock()
mock_obj.some_attribute = "expected_value"
mock_obj.some_method.return_value = "expected_result"
assert result == "expected_value"
```

### Archive Import Handling

```python
# ✅ Safe import pattern for benchmark tests
try:
    from archive.phase1.clause_mates_complete import main as phase1_main
except ImportError:
    pytest.skip("Archive phase1 not available")
```

### Coverage Command Reference

```bash
# Full test run with coverage
nox -s test

# Focus on specific modules
nox -s test -- --cov=src.parsers.tsv_parser --cov-report=term-missing

# Run specific failing tests
nox -s test -- -v -k "test_analyze_character_tracking_basic"

# Check coverage without running tests
coverage report --show-missing
```

## 📊 Success Metrics

### Completion Criteria

- **Test Coverage**: 85%+ (currently 84.36%)
- **Failing Tests**: 0 (currently 18)
- **Critical Modules**: All above 85% coverage
- **Mock Issues**: All resolved
- **Archive Imports**: Working or properly mocked

### Key Performance Indicators

- `tsv_parser.py`: 74% → 85%+
- `interactive_visualizer.py`: 12% → 60%+
- `utils/__init__.py`: 40% → 70%+
- **Total failing tests**: 18 → 0

## 🎯 Next Steps

1. **Immediate**: Use Prompt 1 to fix mock object comparison issues
2. **Short-term**: Use Prompts 2-4 to improve specific module coverage
3. **Final**: Use Prompt 5 for the last push to 85%+

The project is in excellent shape with robust functionality. The remaining work focuses on test completeness rather than critical fixes.
