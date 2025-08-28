# Clause Mates Analyzer - Development Roadmap

## Current Status (v3.1) ✅

### Phase 1 Complete ✅

- **Self-contained monolithic version**
- **448 relationships** extracted with **38 columns**
- **Complete phrase-level antecedent detection**
- **Method 1 antecedent choice** (animacy-based)
- **Full documentation** and metadata

### Phase 2 Complete ✅

- **Modular architecture** with adaptive parsing
- **100% file compatibility** across all WebAnno TSV format variations
- **Preamble-based dynamic column mapping**
- **Automatic format detection** and parser selection
- **Comprehensive documentation** for all supported formats
- **Complete separation of concerns**
- **Comprehensive testing suite** (6/6 tests passing)
- **Organized in dedicated `src/` package**
- **Entry point and verification scripts**

### Phase 3.1 Complete ✅

- **Unified multi-file processing** with cross-chapter coreference resolution
- **Single comprehensive dataset** (1,904 relationships from all 4 chapters)
- **Cross-chapter chain resolution** (36 unified coreference chains)
- **Professional deliverable package** with interactive HTML report
- **Interactive visualizations** embedded in comprehensive analysis report
- **Complete collaboration package** ready for delivery

### Current Project Structure ✅

```
├── src/                       # Complete Phase 2 package with adaptive parsing
├── data/                      # Input and output data with comprehensive documentation
│   ├── input/                 # Source data files with format specifications
│   │   ├── FORMAT_OVERVIEW.md     # Comprehensive format comparison
│   │   ├── gotofiles/             # Standard and extended formats
│   │   │   ├── 2.tsv_DOCUMENTATION.md  # Standard format (15 cols, 448 relationships)
│   │   │   └── later/                  # Alternative formats
│   │   │       ├── 1.tsv_DOCUMENTATION.md  # Extended format (37 cols, 234 relationships)
│   │   │       ├── 3.tsv_DOCUMENTATION.md  # Legacy format (14 cols, 527 relationships)
│   │   │       └── 4.tsv_DOCUMENTATION.md  # Incomplete format (12 cols, 695 relationships)
│   │   └── output/            # Timestamped analysis results
├── archive/                   # Historical code and analysis
│   ├── phase1/                # Self-contained Phase 1
│   ├── phase_comparison/      # Phase comparison analysis and planning
│   └── planning_docs/         # Project planning and completion reports
├── tests/                     # Project-wide testing
└── tools/                     # Analysis and utility scripts
```

### How to Run ✅

```bash
# Current System (Adaptive Parsing)
python src/main.py data/input/gotofiles/2.tsv                    # Standard format (448 relationships)
python src/main.py data/input/gotofiles/later/1.tsv              # Extended format (234 relationships)
python src/main.py data/input/gotofiles/later/3.tsv              # Legacy format (527 relationships)
python src/main.py data/input/gotofiles/later/4.tsv              # Incomplete format (695 relationships)

# Legacy mode (disable adaptive features)
python src/main.py --disable-adaptive data/input/gotofiles/2.tsv

# Verbose output with format detection
python src/main.py --verbose data/input/gotofiles/later/1.tsv
```

---

## Computational Reproducibility Status ✅

### ✅ **Current Implementation (v2.1)**

- **Modular Architecture**: Clean separation of concerns with `src/` package structure
- **Adaptive Parsing**: 100% compatibility across WebAnno TSV format variations
- **Testing Suite**: Comprehensive unit tests with 6/6 tests passing
- **Code Quality**: Ruff integration with GitHub Actions for fast, comprehensive linting
- **File Organization**: Structured archive and output management
- **Cross-platform Compatibility**: Relative path handling and platform-independent code
- **Format Documentation**: Comprehensive specifications for all supported file types

### 🚀 **Modern Development Standards (v2.1)**

#### **Dependency Management**

- ✅ `pyproject.toml`: Modern Python packaging with version constraints
- ✅ `environment.yml`: Conda environment specification for reproducibility
- ✅ Optional dependencies: Development, future features, and benchmarking tools

#### **Continuous Integration & Testing**

- ✅ **Multi-OS Testing**: Ubuntu, Windows, macOS across Python 3.8-3.11
- ✅ **Code Quality Pipeline**: Type checking (mypy), linting and formatting (ruff)
- ✅ **Test Coverage**: Automated coverage reporting with Codecov integration
- ✅ **Reproducibility Validation**: Automated checks for identical outputs across runs
- ✅ **Performance Benchmarking**: Execution time and memory usage monitoring

#### **Development Workflow**

- ✅ **Pre-commit Hooks**: Automated code quality checks before commits
- ✅ **Docker Support**: Containerized environment for consistent execution
- ✅ **Makefile**: Development task automation (test, lint, format, benchmark)
- ✅ **Type Safety**: MyPy configuration with strict type checking

#### **Data Management & Versioning**

- ✅ **Data Provenance**: SHA-256 hashing and metadata tracking
- ✅ **Processing Metadata**: Comprehensive logging of runs with environment info
- ✅ **Reproducibility Validation**: Automated hash comparison for output verification
- ✅ **Performance Tracking**: Historical benchmarking data

### 📋 **Setup Instructions**

```bash
# 1. Clone and set up environment
git clone https://github.com/jobschepens/clausemate.git
cd clausemate

# 2. Using Conda (Recommended)
conda env create -f environment.yml
conda activate clausemate

# 3. Or using pip
pip install -e ".[dev]"

# 4. Set up development tools
make dev-setup  # Installs pre-commit hooks

# 5. Validate setup
make validate-setup

# 6. Run tests
make test

# 7. Run analysis
make test-integration
```

### 🐳 **Docker Usage**

```bash
# Build image
docker build -t clausemate:latest .

# Run analysis
docker run --rm -v $(pwd)/data:/app/data clausemate:latest

# Run tests in container
docker run --rm clausemate:latest python -m pytest tests/ -v
```

### 📊 **Quality Assurance**

#### **Automated Checks**

- **Code Coverage**: Minimum 80% test coverage requirement
- **Type Safety**: 100% type annotation coverage in `src/`
- **Code Style**: Ruff formatting and linting (replaces black, isort, flake8)
- **Security**: Bandit security scanning + safety dependency checks
- **Performance**: Execution time < 30s, memory usage monitoring

#### **Manual Validation**

```bash
# Run all quality checks
make ci-test

# Performance benchmarking
make benchmark

# Memory profiling
make memory-profile

# Pre-release validation
make release-check
```

---

## Phase 3: Enhanced Morphological Features 🔄

### 3.1 Morphological Feature Extraction (High Priority)

**Goal**: Implement pronoun type extraction using detected morphological columns

#### Implementation Plan

```python
# Enhanced pronoun features mapping
PRONOUN_FEATURES = {
    'er': {'gender': 'masc', 'number': 'sing', 'type': 'PersPron'},
    'sie': {'gender': 'fem', 'number': 'sing', 'type': 'PersPron'},  # or plural - needs disambiguation
    'es': {'gender': 'neut', 'number': 'sing', 'type': 'PersPron'},
    'der': {'gender': 'masc', 'number': 'sing', 'type': 'DemPron'},  # D-pronoun
    'die': {'gender': 'fem', 'number': 'sing', 'type': 'DemPron'},   # D-pronoun
    'das': {'gender': 'neut', 'number': 'sing', 'type': 'DemPron'},  # D-pronoun
    # ... additional mappings
}
```

#### Technical Approach

1. **Morphological Analysis**
   - Use detected pronType column (column 16 in 1.tsv)
   - Extract gender/number from morphological features
   - Map WebAnno types to system types (Dem→DemPron, Pers→PersPron)

2. **Enhanced Critical Pronoun Detection**
   - Integrate morphological data with existing pronoun analysis
   - Improve pronoun classification accuracy
   - Add support for ambiguous pronoun resolution

3. **Extended Output Format**

   ```python
   # New columns to add:
   'pronoun_morphological_type'     # Extracted from morphological features
   'pronoun_gender'                 # Extracted pronoun gender
   'pronoun_number'                 # Extracted pronoun number
   'morphological_features_raw'     # Raw morphological feature string
   ```

### 3.2 Advanced Antecedent Choice Methods (Medium Priority)

**Goal**: Implement multiple antecedent choice strategies

#### Method 2: Morphological Compatibility

```python
def calculate_antecedent_choice_morphological(pronoun, candidates):
    """
    Gender/number-based antecedent choice calculation
    Returns compatibility scores based on morphological agreement
    """
    pass
```

#### Method 3: Combined Scoring

```python
def calculate_antecedent_choice_combined(pronoun, candidates):
    """
    Combined scoring: animacy (weight=0.7) + morphology (weight=0.3)
    Returns both discrete count and continuous compatibility score
    """
    pass
```

### 3.3 Schema-Aware Processing (Low Priority)

**Goal**: Extend schema awareness for advanced linguistic features

- **Enhanced Schema Detection**: Identify available morphological layers
- **Feature Extraction Strategy**: Pluggable extractors for different annotation types
- **Command Line Options**: User control over morphological feature extraction

---

## Phase 4: Advanced Linguistic Features 🔮

### 4.1 Enhanced Givenness Detection

**Current**: Binary new/given based on occurrence number
**Proposed**: Multi-level information status

- **Brand-new**: First mention in discourse
- **Unused**: Previously mentioned but inactive
- **Given**: Recently active in discourse
- **Accessible**: Inferrable or associated

#### Implementation

```python
def calculate_discourse_status(coreference_chain, current_position):
    """
    Calculate fine-grained information status based on:
    - Recency of last mention
    - Frequency of mentions
    - Intervening discourse units
    """
    pass
```

### 4.2 Thematic Role Hierarchy

**Goal**: Implement thematic role prominence scales

```python
THEMATIC_HIERARCHY = [
    'Agent', 'Experiencer', 'Instrument', 'Theme', 'Patient', 'Location', 'Goal'
]

def calculate_thematic_prominence(role1, role2):
    """Compare thematic roles on animacy/prominence scales"""
    pass
```

### 4.3 Clause Structure Analysis

**Goal**: Distinguish main vs subordinate clauses

- Extract clause boundaries from segment annotations
- Analyze pronoun distribution across clause types
- Test clause-mate co-occurrence patterns by clause type

---

## Phase 5: Cross-Linguistic Extension 📚

### 5.1 Multi-Chapter Analysis

**Goal**: Extend beyond single chapters to full corpus

#### Data Integration

```python
# Process multiple chapters
chapters = ['chap_1_aktuell.tsv', 'chap_2_aktuell.tsv', 'chap_3_aktuell.tsv', 'chap_4_aktuell.tsv']

def process_full_corpus(chapter_files):
    """
    Combine data from all chapters with:
    - Chapter-level statistics
    - Cross-chapter coreference tracking
    - Discourse progression analysis
    """
    pass
```

### 5.2 Comparative Studies

**Goal**: Compare patterns across different text types

- **Literary vs technical texts**
- **Dialogue vs narrative**
- **Genre-specific pronoun patterns**

---

## Phase 6: Statistical Modeling 📊

### 6.1 Predictive Models

**Goal**: Build models to predict pronoun choice

#### Features for Modeling

```python
MODELING_FEATURES = {
    'pronoun_features': [
        'pronoun_token_idx', 'pronoun_grammatical_role',
        'pronoun_most_recent_antecedent_distance', 'pronoun_morphological_type'
    ],
    'clause_mate_features': [
        'num_clause_mates', 'clause_mate_animacy',
        'clause_mate_thematic_role', 'clause_mate_givenness'
    ],
    'contextual_features': [
        'sentence_length', 'clause_complexity',
        'discourse_position'
    ]
}
```

#### Model Types

- **Logistic Regression**: Baseline interpretable model
- **Random Forest**: Feature importance analysis
- **Neural Networks**: Complex interaction patterns

### 6.2 Causal Inference

**Goal**: Test causal relationships between clause mates and pronoun choice

```python
# Propensity score matching
# Instrumental variable analysis
# Regression discontinuity (if applicable)
```

---

## Phase 7: Visualization & Interface 🎨

### 7.1 Interactive Dashboard

**Goal**: Web-based exploration interface

#### Features

- **Filter by pronoun type, animacy, roles**
- **Distance distribution plots**
- **Antecedent choice heatmaps**
- **Export custom subsets**

#### Technology Stack

```python
# Backend: FastAPI + pandas
# Frontend: Streamlit or Plotly Dash
# Visualization: Plotly, seaborn
```

### 7.2 Linguistic Annotation Tool

**Goal**: Semi-automated annotation assistance

- **Suggest clause mate boundaries**
- **Validate coreference chains**
- **Quality control interface**

---

## Phase 8: Performance & Scalability 🚀

### 8.1 Code Optimization

**Current**: Sequential sentence processing
**Proposed**: Parallel processing

```python
from multiprocessing import Pool
from functools import partial

def process_sentences_parallel(sentences, num_workers=4):
    """
    Parallel sentence processing for large corpora
    """
    with Pool(num_workers) as pool:
        results = pool.map(process_sentence, sentences)
    return results
```

### 8.2 Memory Optimization

- **Streaming processing** for large files
- **Chunk-based analysis** for memory efficiency
- **Database backend** for very large corpora

### 8.3 Caching System

```python
import joblib
from functools import lru_cache

@lru_cache(maxsize=1000)
def cached_antecedent_search(pronoun_id, sentence_range):
    """Cache expensive antecedent calculations"""
    pass
```

---

## Implementation Timeline 📅

### **Q3 2025**: Enhanced Morphological Features

- [x] **Phase 2 completion**: 100% file compatibility achieved
- [x] **Comprehensive documentation**: All formats documented
- [ ] Implement morphological feature extraction using detected columns
- [ ] Add pronoun type mapping (Dem→DemPron, Pers→PersPron)
- [ ] Validate against manual annotations

### **Q4 2025**: Advanced Features

- [ ] Enhanced givenness detection
- [ ] Thematic role hierarchy
- [ ] Multi-chapter integration
- [ ] Performance optimization

### **Q1 2026**: Modeling & Analysis

- [ ] Statistical modeling pipeline
- [ ] Causal inference analysis
- [ ] Cross-linguistic comparisons
- [ ] Publication-ready results

### **Q2 2026**: Tools & Interface

- [ ] Interactive dashboard
- [ ] Annotation assistance tools
- [ ] Documentation for wider release
- [ ] API for external users

---

## Dependencies & Requirements 📋

### **Current Dependencies**

```python
# Core requirements
pandas>=1.3.0
python>=3.11

# Development
ruff>=0.1.0
mypy>=1.0.0
pytest>=7.0.0
pre-commit>=2.0.0
```

### **Phase 3 Requirements**

```python
# Morphological analysis (if needed)
spacy>=3.4.0
de-core-news-sm>=3.4.0  # German language model (optional)

# Statistical modeling
scikit-learn>=1.0.0
statsmodels>=0.13.0
scipy>=1.7.0

# Visualization
plotly>=5.0.0
streamlit>=1.0.0
seaborn>=0.11.0

# Performance
joblib>=1.1.0
dask>=2021.0.0  # For larger datasets
```

### **System Requirements**

- **Memory**: 8GB+ for full corpus processing
- **Storage**: 2GB+ for cached models and data
- **CPU**: Multi-core recommended for parallel processing

---

## Research Applications 🔬

### **Immediate Applications** (Phases 3-4)

1. **Pronoun Resolution Systems**: Improved antecedent choice algorithms
2. **Discourse Analysis**: Information structure patterns
3. **Language Learning**: Pronoun usage difficulty prediction

### **Long-term Applications** (Phases 5-8)

1. **Machine Translation**: Context-aware pronoun translation
2. **Text Generation**: Coherent pronoun patterns in generated text
3. **Linguistic Theory**: Empirical testing of binding theory predictions

---

## Contribution Guidelines 🤝

### **For Linguists**

- Suggest additional linguistic features to extract
- Provide theoretical grounding for new methods
- Validate results against linguistic intuitions

### **For Developers**

- Optimize algorithms for performance
- Add new visualization capabilities
- Extend to other languages/annotation formats

### **For Data Scientists**

- Develop novel modeling approaches
- Create feature importance analysis
- Design evaluation metrics

---

*This roadmap is a living document. Priorities may shift based on research findings and user feedback.*

**Current milestone**: Phase 3 - Enhanced morphological features with detected pronoun type columns
**Contact**: See main project documentation for contributor information
