# Clause Mates Analysis Project

This project analyzes clause mate relationships for referential pronouns in German text data using WebAnno TSV annotations.

## Project Overview

Extracts clause mate relationships for sentences containing:
- Third person personal pronouns (er, sie, es)
- D-pronouns (der, die, das) 
- Demonstrative pronouns (dieser, diese, dieses)

## Data Sources

- `source/` - WebAnno TSV files with rich linguistic and coreference annotations
- `annotation/` - Individual annotator files
- `curation/` - Finalized annotations (lacking coreference layers)

## Scripts

- `clause_mates_clause_level_analyzer.py` - Main analysis script (clause-level export)
- `clause_mates_relationships_analyzer.py` - Alternative relationship-level export
- `clause_mates_analyzer.py` - Initial token-based analyzer
- `debug_parser.py` - Debug script for TSV structure inspection
- `compare_outputs.py` - Compare different export formats

## Output Files

- `clause_mates_clause_level.csv` - **Main output**: 1,433 clauses with clause mates
- `clause_mates_relationships.csv` - Alternative: 31,691 individual relationships
- `clause_mates_coreference_analysis.csv` - Token-based export

## Features Analyzed

- Grammatical role
- Thematic role  
- Animacy
- Sentence position
- Distance to antecedent
- Linguistic form
- Coreference links
- Givenness
- Number of clause mates

## Requirements

- Python 3.x
- pandas
- Standard library modules (os, re, pathlib, dataclasses, typing)

## Usage

```bash
python clause_mates_clause_level_analyzer.py
```

## Output Format

Each row represents a clause containing a target pronoun with all its clause mates:
- Target pronoun features
- All clause mates as pipe-separated lists
- Complete linguistic annotation for analysis
