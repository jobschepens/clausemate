# Clause Mates- **Complete separation of concerns**
- **Comprehensive testing suite** (6/6 tests passing)
- **Organized in dedicated `src/` package**
- **Entry point and verification scripts**

### Current Project Structure ✅
```
├── phase1/                    # Self-contained Phase 1 (463 relationships, 35 cols)
├── src/                       # Complete Phase 2 package (448 relationships, 34 cols)  
├── exportscript.py            # Independent legacy script
└── tests/                     # Project-wide testing
```

### How to Run ✅
```bash
# Phase 1
python phase1/clause_mates_complete.py

# Phase 2  
python src/run_phase2.py

# Phase 2 Testing
python src/verify_phase2.py
```

---

## Phase 3: Enhanced Antecedent Choice Methods 📋s - Development Roadmap

## Current Status (v2.0) ✅

### Phase 1 Complete ✅
- **Self-contained monolithic version** 
- **463 relationships** extracted with **35 columns**
- **Complete phrase-level antecedent detection**
- **Method 1 antecedent choice** (animacy-based)
- **Full documentation** and metadata

### Phase 2 Complete ✅  
- **Modular architecture** with streaming support
- **448 relationships** extracted with **34 columns**
- **Complete separation of concerns**
- **Comprehensive testing suite** (6/6 tests passing)
- **Organized in dedicated `src/` package**
- **Entry point and verification scripts**

---

## Phase 3: Enhanced Antecedent Choice Methods �

### 3.1 Method 2: Morphological Compatibility (High Priority)
**Goal**: Implement gender/number-based antecedent choice calculation

#### Implementation Plan
```python
# Dependencies
import spacy
nlp = spacy.load("de_core_news_sm")  # German language model

# Enhanced pronoun features mapping
PRONOUN_FEATURES = {
    'er': {'gender': 'masc', 'number': 'sing'},
    'sie': {'gender': 'fem', 'number': 'sing'},  # or plural - needs disambiguation
    'es': {'gender': 'neut', 'number': 'sing'},
    'ihn': {'gender': 'masc', 'number': 'sing'},
    'ihm': {'gender': 'masc', 'number': 'sing'},
    'ihr': {'gender': 'fem', 'number': 'sing'},  # or possessive
    'ihnen': {'gender': 'any', 'number': 'plur'},
    # ... D-pronouns and demonstratives
}
```

#### Technical Approach
1. **Morphological Analysis**
   - Use spaCy's German model for automatic feature extraction
   - Extract gender/number from noun phrases
   - Handle article-noun agreement patterns

2. **Pronoun Disambiguation**
   - Implement context-based "sie" disambiguation (fem.sg vs plural)
   - Use syntactic patterns and verb agreement
   - Fall back to animacy method when ambiguous

3. **Compatibility Scoring**
   - Exact match: gender + number agreement
   - Partial match: number agreement only
   - Weighted scoring for ambiguous cases

#### Expected Output
```python
# New columns to add:
'pronoun_antecedent_choice_method2'  # Morphological compatibility count
'pronoun_gender'                     # Extracted pronoun gender
'pronoun_number'                     # Extracted pronoun number
'clause_mate_gender'                 # Clause mate gender (if determinable)
'clause_mate_number'                 # Clause mate number
```

### 2.2 Method 3: Combined Scoring (Medium Priority)
**Goal**: Hybrid approach combining animacy + morphology

```python
def calculate_antecedent_choice_combined(pronoun, candidates):
    """
    Combined scoring: animacy (weight=0.7) + morphology (weight=0.3)
    Returns both discrete count and continuous compatibility score
    """
    pass
```

### 2.3 Method 4: Syntactic Constraints (Low Priority)
**Goal**: Add syntactic compatibility (c-command, binding constraints)

---

## Phase 3: Advanced Linguistic Features 🔮

### 3.1 Enhanced Givenness Detection
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

### 3.2 Thematic Role Hierarchy
**Goal**: Implement thematic role prominence scales

```python
THEMATIC_HIERARCHY = [
    'Agent', 'Experiencer', 'Instrument', 'Theme', 'Patient', 'Location', 'Goal'
]

def calculate_thematic_prominence(role1, role2):
    """Compare thematic roles on animacy/prominence scales"""
    pass
```

### 3.3 Clause Structure Analysis
**Goal**: Distinguish main vs subordinate clauses

- Extract clause boundaries from segment annotations
- Analyze pronoun distribution across clause types
- Test clause-mate co-occurrence patterns by clause type

---

## Phase 4: Cross-Linguistic Extension 📚

### 4.1 Multi-Chapter Analysis
**Goal**: Extend beyond Chapter 2 to full corpus

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

### 4.2 Comparative Studies
**Goal**: Compare patterns across different text types

- **Literary vs technical texts**
- **Dialogue vs narrative**
- **Genre-specific pronoun patterns**

---

## Phase 5: Statistical Modeling 📊

### 5.1 Predictive Models
**Goal**: Build models to predict pronoun choice

#### Features for Modeling
```python
MODELING_FEATURES = {
    'pronoun_features': [
        'pronoun_token_idx', 'pronoun_grammatical_role', 
        'pronoun_most_recent_antecedent_distance'
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

### 5.2 Causal Inference
**Goal**: Test causal relationships between clause mates and pronoun choice

```python
# Propensity score matching
# Instrumental variable analysis
# Regression discontinuity (if applicable)
```

---

## Phase 6: Visualization & Interface 🎨

### 6.1 Interactive Dashboard
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

### 6.2 Linguistic Annotation Tool
**Goal**: Semi-automated annotation assistance

- **Suggest clause mate boundaries**
- **Validate coreference chains**
- **Quality control interface**

---

## Phase 7: Performance & Scalability 🚀

### 7.1 Code Optimization
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

### 7.2 Memory Optimization
- **Streaming processing** for large files
- **Chunk-based analysis** for memory efficiency
- **Database backend** for very large corpora

### 7.3 Caching System
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

### **Q3 2025**: Method 2 Implementation
- [ ] Set up spaCy German pipeline
- [ ] Implement morphological feature extraction
- [ ] Add gender/number compatibility scoring
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

### **New Dependencies**
```python
# Method 2 requirements
spacy>=3.4.0
de-core-news-sm>=3.4.0  # German language model

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

### **Immediate Applications** (Phases 2-3)
1. **Pronoun Resolution Systems**: Improved antecedent choice algorithms
2. **Discourse Analysis**: Information structure patterns
3. **Language Learning**: Pronoun usage difficulty prediction

### **Long-term Applications** (Phases 4-7)
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

**Next milestone**: Method 2 implementation with spaCy morphological analysis  
**Contact**: See main project documentation for contributor information
