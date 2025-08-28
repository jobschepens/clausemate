# Analysis Tools

This directory contains analysis scripts for examining the Phase 2 cross-sentence antecedent detection results.

## Scripts

### `analyze_results.py`

**Purpose**: Comprehensive analysis of Phase 2 results with complete sentence context

**Features**:

- ✅ 94.4% success rate analysis
- Cross-sentence antecedent detection examples (113 cases)
- Complete sentence text for context
- Diverse example selection (8 examples covering different pronoun types)
- Dual output: console display + markdown report generation

**Usage**:

```bash
python tools/analyze_results.py
```

**Output**:

- Console display with formatted results
- `docs/CROSS_SENTENCE_ANALYSIS_REPORT.md` - Comprehensive markdown report

**Dependencies**:

- `phase2_cross_sentence_test.csv` (Phase 2 results)
- `data/input/gotofiles/2.tsv` (TSV source for sentence text)

### `check_duplicates.py`

**Purpose**: Analyze duplicate rows in Phase 2 output (expected behavior)

**Features**:

- Counts total vs unique relationships
- Groups duplicates by sentence and clause mate combinations
- Explains why duplicates occur (multiple clause mates per pronoun)

**Usage**:

```bash
python tools/check_duplicates.py
```

**Key Insights**: Duplicates are expected - each pronoun can have multiple clause mates, creating one row per pronoun-clause mate pair as per task specification.

### `check_file_format.py`

**Purpose**: Validate TSV file format and structure

**Features**:

- Checks WebAnno TSV 3.3 format compliance
- Validates sentence boundaries (#Text= lines)
- Examines token annotation structure
- Reports file statistics

**Usage**:

```bash
python tools/check_file_format.py
```

## Analysis Results Summary

**Phase 2 Cross-Sentence Implementation**:

- ✅ 94.4% antecedent detection success rate
- ✅ 113 cross-sentence antecedent cases found
- ✅ Distances up to 695+ tokens successfully handled
- ✅ Sophisticated antecedent choice handling (1-28 options)
- ✅ Complete sentence context retrieval

**Key Achievement**: Successfully implemented cross-sentence antecedent analysis matching Phase 1's capability, with comprehensive documentation and analysis tools.
