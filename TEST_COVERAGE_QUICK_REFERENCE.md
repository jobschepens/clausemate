# Test Coverage Improvement Plan - Quick Reference

## Current Status

- **Coverage**: 76.52% (3,228 total lines, 758 missing)
- **Tests**: 367 passed, 36 failed, 8 skipped
- **Target**: 85%+ coverage, 0 failed tests

## IMMEDIATE FIXES NEEDED (Blocking Many Tests)

### 1. SentenceContext Constructor (CRITICAL)

**Files**: `tests/test_pronoun_extractor.py` (13 failing tests)
**Problem**: Missing required args `critical_pronouns` and `coreference_phrases`
**Fix**: Update `src/data/models.py` SentenceContext or provide defaults

### 2. IncompleteFormatParser Features (CRITICAL)

**File**: `src/parsers/incomplete_format_parser.py:414`
**Problem**: Missing "morphological" key in `available_features`
**Fix**: Add missing feature keys to dictionary initialization

### 3. Multi-File Mock Issues (CRITICAL)

**Files**: `tests/test_multi_file_batch_processor.py`
**Problem**: Mock comparison errors (`'<' not supported between MagicMock and int`)
**Fix**: Set proper attributes on mock objects (e.g., `mock.sentence_num = 1`)

## HIGHEST IMPACT TARGETS (Add Most Coverage)

### Interactive Visualizer (12% → 60%+)

- **File**: `src/visualization/interactive_visualizer.py`
- **Missing**: 220+ lines
- **Strategy**: Mock matplotlib/plotly, test data transformations

### Utils Module (40% → 70%+)

- **File**: `src/utils/__init__.py`
- **Missing**: 131+ lines
- **Strategy**: Test utility functions, string processing, file handling

### Extractors (59-62% → 75%+)

- **Files**: All 4 extractor files
- **Missing**: 159 total lines
- **Strategy**: Fix SentenceContext first, then comprehensive extractor tests

### Adaptive TSV Parser (58% → 75%+)

- **File**: `src/parsers/adaptive_tsv_parser.py`
- **Missing**: 99 lines
- **Strategy**: Test format variations, error handling, integration

## TESTING APPROACH FOR AI AGENT

### Mock Setup Pattern

```python
# For SentenceContext:
context = SentenceContext(
    sentence_id="1",
    sentence_num=1,
    tokens=[token1, token2],
    first_words="Karl_sagte",
    critical_pronouns=[],  # ADD THIS
    coreference_phrases=[]  # ADD THIS
)

# For Multi-file mocks:
mock_relationship.sentence_num = 1  # Not MagicMock
mock_relationship.pronoun.idx = 0   # Set concrete values
```

### Test File Priorities

1. **Fix existing**: `test_pronoun_extractor.py`, `test_multi_file_batch_processor.py`
2. **Create new**: `test_interactive_visualizer.py`, `test_utils_module.py`
3. **Expand**: `test_adaptive_tsv_parser.py`, `test_format_detector.py`

### Success Metrics

- **Phase 1**: Fix 36 failing tests → 0 failed
- **Phase 2**: 76.5% coverage → 85%+
- **Phase 3**: Add ~80 new tests (367 → 450+)

## IMPLEMENTATION ORDER

1. **Week 1**: Fix critical blocking issues (SentenceContext, mocks)
2. **Week 2-3**: Target lowest coverage modules (visualizer, utils, extractors)
3. **Week 4**: Improve medium coverage modules to 85%+
4. **Week 5**: Polish and integration testing

**Estimated Effort**: 51-67 hours total

## Key Files to Work On

```bash
# CRITICAL FIXES (Week 1)
src/data/models.py                     # Fix SentenceContext
src/parsers/incomplete_format_parser.py # Fix available_features
tests/test_pronoun_extractor.py        # Update all SentenceContext usage
tests/test_multi_file_batch_processor.py # Fix mock setup

# HIGH IMPACT (Week 2-3)
src/visualization/interactive_visualizer.py # 12% → 60%+
src/utils/__init__.py                       # 40% → 70%+
src/extractors/*.py                         # 59-62% → 75%+
src/parsers/adaptive_tsv_parser.py         # 58% → 75%+

# NEW TEST FILES NEEDED
tests/test_interactive_visualizer.py
tests/test_utils_module.py
tests/test_adaptive_tsv_parser.py
```

This plan prioritizes maximum impact fixes first, then systematically improves coverage.
