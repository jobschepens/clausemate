# Test Coverage Improvement Plan for ClauseMate

## Current Status
- **Total Coverage**: 76.52% (2,470 lines covered out of 3,228)
- **Test Results**: 367 passed, 36 failed, 8 skipped
- **Target**: Increase coverage to 85%+ and fix all failing tests

## Priority Areas for Test Coverage Improvement

### CRITICAL FIXES (Must Fix First)
These are blocking many tests and need immediate attention:

#### 1. SentenceContext Constructor Issues
**File**: `src/data/models.py`  
**Problem**: Tests failing due to missing required arguments in SentenceContext  
**Lines Affected**: Multiple test files using SentenceContext  
**Action Required**:
- Fix `SentenceContext.__init__()` signature or provide default values
- Update all test files to use correct constructor parameters
- Files to update: `tests/test_pronoun_extractor.py` (all 13 failing tests)

#### 2. IncompleteFormatParser Missing Features
**File**: `src/parsers/incomplete_format_parser.py`  
**Problem**: `available_features` dictionary missing "morphological" key  
**Lines Affected**: Line 414  
**Action Required**:
- Add missing feature keys to `available_features` initialization
- Ensure all expected feature keys are present

#### 3. Multi-File Processing Mock Issues
**Files**: `tests/test_multi_file_batch_processor.py`  
**Problem**: Mock objects causing comparison errors  
**Lines Affected**: Lines causing "'<' not supported between instances of 'MagicMock' and 'int'"  
**Action Required**:
- Fix mock setup to use proper comparable values
- Ensure mock relationships have proper sentence_num attributes

### HIGH PRIORITY (Coverage < 70%)

#### 1. Interactive Visualizer (12% coverage)
**File**: `src/visualization/interactive_visualizer.py`  
**Missing Lines**: 95-316, 334-496, 516-774 (220+ lines)  
**Test Strategy**:
- Create mock-based tests for visualization components
- Test data transformation methods
- Test error handling in visualization pipeline
- Mock external dependencies (matplotlib, plotly, etc.)

#### 2. Utils Module (40% coverage)
**File**: `src/utils/__init__.py`  
**Missing Lines**: 25-156 (131+ lines)  
**Test Strategy**:
- Test utility functions individually
- Add edge case testing for string processing
- Test file handling utilities
- Add error condition testing

#### 3. Adaptive TSV Parser (58% coverage)
**File**: `src/parsers/adaptive_tsv_parser.py`  
**Missing Lines**: 79-105, 122, 132, 140-142, 147, 161-177, etc. (99 lines total)  
**Test Strategy**:
- Test different TSV format variations
- Test error handling for malformed files
- Test adaptive parsing logic
- Add integration tests with real TSV samples

#### 4. Extractors (59-62% coverage)
**Files**: 
- `src/extractors/pronoun_extractor.py` (59% coverage, 28 missing lines)
- `src/extractors/coreference_extractor.py` (60% coverage, 40 missing lines)
- `src/extractors/phrase_extractor.py` (61% coverage, 31 missing lines)
- `src/extractors/relationship_extractor.py` (62% coverage, 60 missing lines)

**Test Strategy**:
- Fix SentenceContext issues first
- Add comprehensive extractor tests with various input scenarios
- Test error conditions and edge cases
- Test coreference chain building logic

### MEDIUM PRIORITY (Coverage 70-85%)

#### 1. Format Detector (69% coverage)
**File**: `src/utils/format_detector.py`  
**Missing Lines**: 90, 167-168, 173-175, etc. (60 lines total)  
**Test Strategy**:
- Test format detection with various file types
- Test compatibility scoring logic
- Add negative test cases for unsupported formats

#### 2. TSV Parser (69% coverage)
**File**: `src/parsers/tsv_parser.py`  
**Missing Lines**: 55-69, 105-108, 145-146, etc. (49 lines total)  
**Test Strategy**:
- Test WebAnno TSV 3.3 format parsing
- Test coreference link parsing
- Test sentence boundary detection

#### 3. Unified Relationship Model (70% coverage)
**File**: `src/multi_file/unified_relationship_model.py`  
**Missing Lines**: 40-41, 45, 49, 53, 58-71 (8 lines total)  
**Test Strategy**:
- Test relationship merging logic
- Test cross-chapter relationship handling

#### 4. Advanced Analysis Features (76% coverage)
**File**: `src/multi_file/advanced_analysis_features.py`  
**Missing Lines**: 166-169, 197-207, etc. (70 lines total)  
**Test Strategy**:
- Fix existing test failures first
- Add comprehensive character tracking tests
- Test statistical calculation methods

#### 5. Benchmark Module (77% coverage)
**File**: `src/benchmark.py`  
**Missing Lines**: 14-15, 56-57, 93-112, 161-164 (18 lines total)  
**Test Strategy**:
- Fix import issues in benchmark tests
- Test performance measurement logic
- Mock file operations for consistent testing

### LOW PRIORITY (Coverage > 85%)

These modules have good coverage but could use minor improvements:

#### 1. Data Models (85% coverage)
**File**: `src/data/models.py`  
**Missing Lines**: Property validators and edge cases (29 lines)

#### 2. Incomplete Format Parser (87% coverage)
**File**: `src/parsers/incomplete_format_parser.py`  
**Missing Lines**: Error handling paths (25 lines)

#### 3. Enhanced Output System (92% coverage)
**File**: `src/multi_file/enhanced_output_system.py`  
**Missing Lines**: Complex formatting edge cases (12 lines)

#### 4. Preamble Parser (94% coverage)
**File**: `src/parsers/preamble_parser.py`  
**Missing Lines**: Edge case handling (8 lines)

#### 5. Multi-File Batch Processor (95% coverage)
**File**: `src/multi_file/multi_file_batch_processor.py`  
**Missing Lines**: Error recovery paths (10 lines)

## Implementation Strategy for AI Agent

### Phase 1: Critical Fixes (Week 1)
```python
# Priority Order:
1. Fix SentenceContext constructor in src/data/models.py
2. Fix IncompleteFormatParser.available_features
3. Fix multi-file processing mock setup
4. Verify all critical tests pass
```

### Phase 2: High-Impact Areas (Week 2-3)
```python
# Focus on modules with lowest coverage:
1. Interactive Visualizer (12% → 60%+)
2. Utils Module (40% → 70%+)
3. Adaptive TSV Parser (58% → 75%+)
4. All Extractors (59-62% → 75%+)
```

### Phase 3: Medium Priority (Week 4)
```python
# Bring medium coverage modules to 85%+:
1. Format Detector (69% → 85%+)
2. TSV Parser (69% → 85%+)
3. Advanced Analysis Features (76% → 85%+)
4. Benchmark Module (77% → 85%+)
```

### Phase 4: Polish (Week 5)
```python
# Fine-tune high-coverage modules:
1. Complete remaining edge cases
2. Add integration tests
3. Verify all error paths are tested
```

## Test File Structure to Create/Update

### New Test Files Needed:
```bash
tests/test_interactive_visualizer.py      # New - highest impact
tests/test_utils_module.py                # New - missing completely
tests/test_adaptive_tsv_parser.py         # New - complex logic
tests/test_format_detector.py             # Expand existing
```

### Test Files to Fix:
```bash
tests/test_pronoun_extractor.py           # Fix SentenceContext usage
tests/test_multi_file_batch_processor.py  # Fix mock setup
tests/test_incomplete_format_parser.py    # Fix feature dictionary
tests/test_benchmark.py                   # Fix import errors
tests/test_advanced_analysis_features.py  # Fix multiple mock issues
tests/test_enhanced_output_system.py      # Fix boundary marker logic
```

## Testing Guidelines for AI Agent

### Mock Strategy:
- Use `unittest.mock.MagicMock` for external dependencies
- Mock file operations consistently
- Ensure mock objects have required attributes for comparisons
- Use `patch` decorators at class level when possible

### Data Generation:
- Create reusable test fixtures for common data structures
- Use factory patterns for generating test data
- Ensure test data matches production data schemas

### Error Testing:
- Test all exception paths
- Verify error messages are helpful
- Test edge cases (empty files, malformed data, etc.)

### Integration Testing:
- Test module interactions
- Use real (small) data files for integration tests
- Verify end-to-end workflows

## Success Metrics

### Coverage Targets:
- **Overall**: 76.5% → 85%+ (increase by ~9%)
- **Critical modules**: All extractors, parsers, and analyzers to 85%+
- **Visualization**: 12% → 60%+ (major improvement)
- **Utils**: 40% → 70%+ (foundational improvement)

### Test Health:
- **Failing tests**: 36 → 0 (fix all failures)
- **Test count**: 367 → 450+ (add ~80+ new tests)
- **Test stability**: No flaky tests, consistent results

### Quality Indicators:
- All modules have comprehensive error handling tests
- All public APIs are tested
- All critical business logic paths are covered
- Edge cases and boundary conditions are tested

## Estimated Effort

### Time Investment:
- **Phase 1 (Critical Fixes)**: 8-12 hours
- **Phase 2 (High Impact)**: 20-25 hours  
- **Phase 3 (Medium Priority)**: 15-20 hours
- **Phase 4 (Polish)**: 8-10 hours
- **Total**: 51-67 hours of focused development

### Complexity Assessment:
- **Low**: Config, simple utilities, basic parsers
- **Medium**: Extractors, analyzers, most business logic
- **High**: Multi-file processing, visualization, complex mocking
- **Very High**: Integration testing, performance testing

This plan prioritizes fixing broken tests first, then systematically improves coverage in order of impact and difficulty.
