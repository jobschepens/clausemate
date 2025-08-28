# Cross-Chapter Coreference Analysis Specification

## Objective

Create a test script to determine whether coreference chains can span across chapter boundaries in the sequential book chapters (1.tsv → 2.tsv → 3.tsv → 4.tsv).

## Hypothesis

The files represent sequential book chapters in numerical order, and coreference chains may continue across chapter boundaries, requiring unified processing to capture complete pronoun-antecedent relationships.

## Analysis Requirements

### 1. Chapter Boundary Detection

**File Processing Order**: 1.tsv → 2.tsv → 3.tsv → 4.tsv

**Key Analysis Points**:

- Extract the highest sentence number from each file
- Identify potential sentence numbering gaps or overlaps
- Analyze narrative continuity indicators

### 2. Coreference Chain Analysis

**Chain Extraction Strategy**:

- Extract all coreference chains from each file individually
- Identify chain IDs and their sentence ranges
- Look for chains that end near chapter boundaries
- Look for chains that begin near chapter boundaries

**Cross-Chapter Indicators**:

- Chains ending in the last sentences of a chapter
- Chains beginning in the first sentences of the next chapter
- Shared character references across chapter boundaries
- Pronoun references without clear antecedents in the same chapter

### 3. Character Continuity Analysis

**Character Tracking**:

- Extract character mentions (especially "Amerikaner", "Amerikanerin", proper names)
- Track character introductions vs. continued references
- Identify pronouns referring to characters introduced in previous chapters

**Narrative Elements**:

- Location references (Zell, Amerika)
- Temporal continuity markers
- Plot element continuity

## Implementation Specification

### Script Structure: `test_cross_chapter_coreference.py`

```python
#!/usr/bin/env python3
"""
Cross-Chapter Coreference Analysis Script

Tests whether coreference chains span across chapter boundaries
in the sequential book chapters (1.tsv → 2.tsv → 3.tsv → 4.tsv).
"""

class CrossChapterAnalyzer:
    """Analyzes coreference chains across multiple chapter files."""

    def __init__(self):
        self.chapter_files = [
            "data/input/gotofiles/later/1.tsv",  # Chapter 1
            "data/input/gotofiles/2.tsv",        # Chapter 2
            "data/input/gotofiles/later/3.tsv",  # Chapter 3
            "data/input/gotofiles/later/4.tsv"   # Chapter 4
        ]
        self.chapter_data = {}
        self.cross_chapter_evidence = []

    def analyze_all_chapters(self):
        """Main analysis method."""
        # 1. Extract data from each chapter
        # 2. Analyze sentence numbering patterns
        # 3. Extract coreference chains
        # 4. Identify cross-chapter candidates
        # 5. Generate comprehensive report

    def extract_chapter_data(self, file_path: str) -> dict:
        """Extract key data from a chapter file."""
        # - Sentence range (min/max sentence numbers)
        # - All coreference chains with their sentence ranges
        # - Character mentions and their contexts
        # - Pronoun references and their targets

    def analyze_sentence_continuity(self) -> dict:
        """Analyze sentence numbering across chapters."""
        # - Check if sentence numbers continue sequentially
        # - Identify gaps or overlaps
        # - Determine chapter boundary sentence numbers

    def identify_boundary_chains(self) -> list:
        """Identify chains near chapter boundaries."""
        # - Chains ending in last 5 sentences of a chapter
        # - Chains beginning in first 5 sentences of next chapter
        # - Potential cross-chapter chain candidates

    def analyze_character_continuity(self) -> dict:
        """Analyze character references across chapters."""
        # - Track character introductions vs. continued references
        # - Identify pronouns without local antecedents
        # - Find character mentions spanning chapters

    def detect_cross_chapter_evidence(self) -> list:
        """Detect evidence of cross-chapter coreference."""
        # Evidence types:
        # 1. Chain ID continuity across files
        # 2. Character references without local introduction
        # 3. Pronoun-antecedent gaps at chapter boundaries
        # 4. Narrative continuity indicators

    def generate_report(self) -> str:
        """Generate comprehensive analysis report."""
        # Detailed findings with evidence
        # Recommendations for unified processing
        # Specific cross-chapter relationship candidates
```

### Key Analysis Functions

#### 1. Sentence Range Analysis

```python
def analyze_sentence_ranges(self):
    """
    Extract sentence ranges from each chapter:
    - Chapter 1 (1.tsv): sentences X-Y
    - Chapter 2 (2.tsv): sentences A-B
    - Chapter 3 (3.tsv): sentences C-D
    - Chapter 4 (4.tsv): sentences E-F

    Check for:
    - Sequential numbering (Y+1 = A, B+1 = C, etc.)
    - Overlapping ranges (indicating same content)
    - Gap patterns (indicating missing content)
    """
```

#### 2. Coreference Chain Extraction

```python
def extract_coreference_chains(self, file_path: str):
    """
    For each chapter, extract:
    - All chain IDs and their sentence spans
    - Chain types (PersPron, DemPron, etc.)
    - First and last mentions in each chain
    - Chains that end near chapter end
    - Chains that begin near chapter start
    """
```

#### 3. Cross-Chapter Evidence Detection

```python
def detect_cross_chapter_evidence(self):
    """
    Look for evidence of cross-chapter relationships:

    1. Chain Continuity:
       - Chain ending in chapter N, similar chain starting in chapter N+1
       - Same character referenced across boundary

    2. Pronoun Resolution Gaps:
       - Pronouns in chapter N+1 without clear antecedents
       - References to entities introduced in chapter N

    3. Narrative Continuity:
       - Character actions spanning chapters
       - Location/temporal continuity
       - Plot element references
    """
```

### Expected Output Format

```
CROSS-CHAPTER COREFERENCE ANALYSIS REPORT
==========================================

CHAPTER STRUCTURE:
- Chapter 1 (1.tsv): Sentences 1-X (Y relationships)
- Chapter 2 (2.tsv): Sentences A-B (Z relationships)
- Chapter 3 (3.tsv): Sentences C-D (W relationships)
- Chapter 4 (4.tsv): Sentences E-F (V relationships)

SENTENCE CONTINUITY: [SEQUENTIAL/OVERLAPPING/GAPPED]

COREFERENCE CHAIN ANALYSIS:
- Total chains per chapter: [counts]
- Boundary chains (ending near chapter end): [count and examples]
- Boundary chains (starting near chapter start): [count and examples]

CROSS-CHAPTER EVIDENCE:
1. Chain Continuity Evidence:
   - [Specific examples of chains that may span chapters]

2. Character Continuity Evidence:
   - [Characters referenced across chapters]
   - [Pronouns without local antecedents]

3. Narrative Continuity Evidence:
   - [Plot elements spanning chapters]
   - [Location/temporal continuity]

RECOMMENDATIONS:
- [UNIFIED PROCESSING REQUIRED] if cross-chapter chains detected
- [SEPARATE PROCESSING SUFFICIENT] if no cross-chapter evidence
- [SPECIFIC IMPLEMENTATION NOTES] for unified processing

CONFIDENCE LEVEL: [HIGH/MEDIUM/LOW]
```

## Validation Criteria

### Positive Evidence for Cross-Chapter Chains

1. **Chain ID Continuity**: Same chain IDs appearing in consecutive chapters
2. **Character Reference Gaps**: Pronouns referring to characters introduced in previous chapters
3. **Narrative Continuity**: Plot elements, locations, or temporal references spanning chapters
4. **Sentence Numbering**: Sequential sentence numbering across files

### Negative Evidence (Separate Chapters)

1. **Independent Sentence Numbering**: Each file starts from sentence 1
2. **Self-Contained Chains**: All coreference chains complete within each file
3. **Character Reintroductions**: Characters reintroduced in each chapter
4. **Narrative Independence**: Each chapter tells a complete story

## Implementation Priority

**High Priority Analysis**:

1. Sentence numbering patterns across files
2. Character mention analysis (especially "Amerika" references)
3. Coreference chain boundary analysis
4. Chain ID overlap detection

**Medium Priority Analysis**:

1. Narrative continuity indicators
2. Temporal reference analysis
3. Location reference continuity
4. Plot element tracking

## Success Metrics

**Script Success Criteria**:

- ✅ Processes all 4 chapter files successfully
- ✅ Extracts sentence ranges and coreference data
- ✅ Identifies potential cross-chapter relationships
- ✅ Generates clear, actionable recommendations
- ✅ Provides confidence level for findings

**Analysis Success Criteria**:

- ✅ Clear determination of cross-chapter chain existence
- ✅ Specific examples of cross-chapter relationships (if found)
- ✅ Quantified evidence supporting conclusions
- ✅ Implementation recommendations for unified processing

## Next Steps After Analysis

**If Cross-Chapter Chains Detected**:

1. Proceed with unified multi-file processing implementation
2. Design cross-chapter coreference resolution system
3. Implement global sentence numbering
4. Create unified output format

**If No Cross-Chapter Chains Detected**:

1. Modify plan to focus on batch processing with separate outputs
2. Implement file aggregation without cross-chain resolution
3. Create combined output with chapter metadata
4. Maintain separate chain numbering per chapter

---

**Implementation Note**: This script should be implemented in Code mode as `test_cross_chapter_coreference.py` and run before proceeding with the full unified processing system implementation.
