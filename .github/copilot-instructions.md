# Copilot Instructions for Clause Mates Analyzer

## Project Overview

This is a **German linguistic research tool** for extracting clause mate relationships from annotated pronoun data. The tool investigates whether pronouns appear at more consistent linear positions when clause mates are present vs. absent, focusing on referential relationships in German discourse.

The codebase evolved through iterative development and contains **two complete implementations**:

- **Phase 1**: Monolithic version in `archive/phase1/` (463 relationships, 35 columns)
- **Phase 2**: Modular architecture in `src/` (448 relationships, 34 columns, 94.4% antecedent detection)

## Linguistic Methodology

### Clause Mate Theory

**Clause mates** are additional referential expressions in the same sentence as a critical pronoun that are annotated in coreference layers. The research investigates linear position consistency of pronouns relative to these clause mates.

### Critical Pronouns (German-Specific)

- **Third person personal**: `er, sie, es, ihm, ihr, ihn, ihnen` - core referential pronouns
- **D-pronouns (pronominal use)**: `der, die, das, dem, den, deren, dessen, derer` - demonstrative articles used pronominally
- **Demonstrative pronouns**: `dieser, diese, dieses, diesem, diesen` - explicit demonstratives

### Coreference Chain Analysis

The tool tracks coreference chains across sentences to calculate:

- **Most recent antecedent distance**: Linear tokens to nearest mention in chain
- **First antecedent distance**: Linear tokens to chain's initial mention
- **Cross-sentence detection**: 94.4% success rate for antecedents spanning sentence boundaries

### WebAnno TSV 3.3 Format

Input data uses specific linguistic annotation layers:

- **Column 0**: Token ID (`1-1`, `2-5`, etc. = sentence-token)
- **Column 2**: Token text
- **Column 4**: Grammatical role (`Subj`, `dirObj`, `indirObj`)
- **Column 5**: Thematic role (`Proto-Ag`, `Proto-Pat`)
- **Column 10**: Animate coreference link (`*->115-4`)
- **Column 11**: Animate coreference type (`PersPron[115]`, `indefNP[127]`)
- **Column 12/13**: Inanimate coreference (parallel to animate layer)

### Givenness & Animacy

- **Givenness**: `neu` (first mention) vs `bekannt` (subsequent mention)
- **Animacy**: `anim` (animate layer) vs `inanim` (inanimate layer)
- Links occurrence numbers to givenness: occurrence 1 = `neu`, >1 = `bekannt`

## Architecture Patterns

### Dual Execution Support

All main modules support both script and module execution:

```python
# Handle both python src/main.py and python -m src.main
try:
    from .config import FilePaths  # Module execution
except ImportError:
    from src.config import FilePaths  # Script execution
```

### Data Flow Architecture

The modular pipeline follows this pattern:

1. **TSVParser** → parses linguistic annotations from TSV files
2. **Extractors** → extract features (pronouns, phrases, coreferences, relationships)
3. **Analyzers** → analyze and calculate distances/positions
4. **Main orchestrator** → coordinates pipeline and exports CSV

### Type-Safe Models

Use `src/data/models.py` dataclasses instead of dictionaries:

- `Token` - individual tokens with linguistic annotations
- `CoreferencePhrase` - phrases with coreference information
- `ClauseMateRelationship` - final output relationships
- `SentenceContext` - sentence-level context for extractors

## Development Workflows

### Primary Commands

```bash
# Run Phase 2 analysis (preferred)
python src/run_phase2.py
python -m src.main

# Development with nox (cross-platform task runner)
nox                    # Default: lint + test
nox -s format         # Format with ruff
nox -s test           # Run pytest
nox -s mypy          # Type checking

# Analysis tools
python tools/analyze_results.py  # Generate comprehensive reports
python tools/check_duplicates.py # Verify relationship integrity
```

### Debugging Antecedent Detection Failures

When the 94.4% success rate fails, use these debugging workflows:

#### 1. Sentence-Level Debugging

```bash
# Check specific sentence context
python tools/check_duplicates.py  # Shows duplicate pronoun handling
```

#### 2. Coreference Chain Inspection

```python
# In your code - examine coreference patterns
context = SentenceContext(tokens=[...], sentence_num=17)
chains = coreference_extractor.extract_coreference_chains([context])
print(f"Chains found: {len(chains)}")
for chain in chains:
    print(f"Chain {chain.chain_id}: {[m.text for m in chain.mentions]}")
```

#### 3. TSV Data Validation

- Check for malformed coreference links (`*->115-4` format)
- Verify occurrence numbering consistency (`115-1`, `115-2`, etc.)
- Ensure both animate/inanimate layers are parsed correctly
- Look for missing `#Text=` sentence boundaries

#### 4. Cross-Sentence Boundary Issues

- Verify sentence context includes sufficient preceding sentences
- Check `SentenceContext.tokens` spans multiple sentences for antecedent search
- Debug `most_recent_antecedent_distance` calculations across boundaries

#### 5. Critical Pronoun Classification

```python
# Verify pronoun detection
from src.pronoun_classifier import is_critical_pronoun
token_text = "der"  # Test ambiguous cases
is_critical = is_critical_pronoun(token_text, context)
print(f"'{token_text}' classified as critical: {is_critical}")
```

### Modern Toolchain

- **ruff**: Fast linting/formatting (replaces black, isort, flake8)
- **nox**: Cross-platform task runner (replaces make/tox)
- **mypy**: Type checking with strict configuration
- **pytest**: Testing with 25%+ coverage requirement

## Critical Conventions

### Configuration Management

All constants centralized in `src/config.py`:

```python
class TSVColumns:
    TOKEN_TEXT = 2
    COREFERENCE_LINK = 10

class PronounSets:
    THIRD_PERSON_PRONOUNS = {"er", "sie", "es", ...}
```

### Cross-Sentence Antecedent Detection

The core innovation of Phase 2 - handles antecedents across sentence boundaries:

- Uses `CoreferenceExtractor` to build chains across sentences
- Calculates `most_recent_antecedent_distance` and `first_antecedent_distance`
- Success rate: 94.4% with comprehensive sentence context

### Linguistic Data Format

TSV files use specific column indices with German linguistic annotations:

- Token 0: ID, Token 2: Text, Token 4: Grammatical role
- Token 10/11: Animate coreference (link/type)
- Token 12/13: Inanimate coreference (link/type)
- Critical pronouns: 3rd person, D-pronouns, demonstrative

#### WebAnno TSV 3.3 Structure

```tsv
#FORMAT=WebAnno TSV 3.3
#Text=Von Amerika aus betrachtet, ist Zell ein winziger Punkt.
1-1 0-3 Von _ _ _ _ _ _ *[244] _ _ _ _ _
1-4 16-26 betrachtet _ Subj Proto-Ag _ _ _ *[244] *->43-1 zero[43] _ _ _
```

#### Key Annotation Patterns

- **Sentence boundaries**: `#Text=` followed by sentence content
- **Token IDs**: `{sentence}-{token}` format (e.g., `1-4`, `17-12`)
- **Coreference links**: `*->{chain_id}-{occurrence}` (e.g., `*->115-4`)
- **Coreference types**: `{type}[{chain_id}]` (e.g., `PersPron[115]`, `indefNP[127]`)
- **Missing values**: `_` indicates no annotation
- **Dual layers**: Columns 10-11 (animate) and 12-13 (inanimate) for different referent types

#### Grammatical Roles

- `Subj`, `dirObj`, `indirObj` - core argument structure
- May include indices: `Subj[1]`, `dirObj[2]` for multiple instances

#### Thematic Roles

- `Proto-Ag` (Proto-Agent), `Proto-Pat` (Proto-Patient) - semantic role categories
- Linked to grammatical roles with matching indices

### Error Handling Pattern

Custom exceptions in `src/exceptions.py` with structured error hierarchy:

```python
try:
    result = extractor.extract(context)
except ClauseMateExtractionError as e:
    logger.error(f"Extraction failed: {e}")
```

## File Organization Logic

### Phase Separation

- `archive/phase1/` - Complete self-contained implementation (preserve as-is)
- `src/` - Modern modular architecture (active development)
- Never mix imports between phases

### Modular Structure

- `src/parsers/` - TSV file parsing and token processing
- `src/extractors/` - Feature extraction (pronouns, phrases, relationships)
- `src/analyzers/` - Distance calculation and analysis
- `src/data/` - Type-safe models and data structures

### Output Standardization

Both phases export to standardized CSV format via `ExportColumns.STANDARD_ORDER` ensuring consistent column ordering for linguistic analysis.

## Testing Strategy

### Component Testing

Test individual extractors with `SentenceContext` fixtures:

```python
context = SentenceContext(tokens=[...], sentence_num=1)
result = extractor.extract(context)
```

### Integration Testing

Use `data/input/gotofiles/2.tsv` for reproducible CI testing. The reproducibility test verifies consistent relationship extraction across environments.

### Performance Benchmarks

CI includes benchmarking to detect performance regressions in the extraction pipeline.

## When Working on This Codebase

1. **Respect the dual-phase architecture** - Phase 1 is archived but functional
2. **Use type hints extensively** - This is a type-safe codebase with mypy enforcement
3. **Follow the extractor pattern** - Inherit from `BaseExtractor` for new features
4. **Test cross-sentence scenarios** - The core value is antecedent detection across sentences
5. **Maintain CSV column compatibility** - Linguistic researchers depend on consistent output format
