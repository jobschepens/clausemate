# Phase 2 Improvement Plan for Clause Mates Analyzer

## Executive Summary

Phase 2 focuses on **Structural Improvements** to transform our well-functioning but monolithic script into a maintainable, testable, and efficient modular architecture. This phase builds on the solid foundation established in Phase 1.

## Current State Assessment

### ✅ Phase 1 Achievements

- **Constants extracted** to `config.py` (✓ Complete)
- **Type hints added** throughout codebase (✓ Complete)
- **Error handling implemented** with custom exceptions (✓ Complete)
- **Utility functions modularized** into separate modules (✓ Complete)
- **Clean workspace** with Phase 1 files properly archived

### 📊 Current Architecture

```
Current Structure:
├── clause_mates_complete.py    # Main script (600+ lines)
├── config.py                   # Constants & configuration
├── utils.py                    # General utilities
├── pronoun_classifier.py       # Pronoun logic
├── exceptions.py               # Custom exceptions
├── exportscript.py            # Separate utility
└── phase1_archive/            # Archived Phase 1 files
```

## Phase 2 Goals & Objectives

### 🎯 Primary Objectives

1. **Split monolithic script** into focused, single-responsibility modules
2. **Eliminate code duplication** through abstraction and reusable components
3. **Add comprehensive unit tests** to ensure refactoring safety
4. **Establish clear module boundaries** and interfaces
5. **Improve code maintainability** and readability

### 📈 Success Metrics

- **Reduce main script** from 600+ lines to <200 lines
- **Achieve <5% code duplication** (currently ~30%)
- **Reach >80% test coverage** for core functionality
- **Clear module separation** with single responsibilities
- **Improved developer experience** and code clarity

## Detailed Implementation Plan

### **Task 1: Modular Architecture Design** (Week 1)

#### 1.1 Create Module Structure

```
src/
├── __init__.py
├── main.py                     # Orchestration & CLI interface
├── parsers/
│   ├── __init__.py
│   ├── tsv_parser.py          # TSV file parsing logic
│   └── token_processor.py     # Token extraction & validation
├── extractors/
│   ├── __init__.py
│   ├── coreference_extractor.py    # Coreference ID extraction
│   └── relationship_extractor.py   # Clause mate relationships
├── analyzers/
│   ├── __init__.py
│   ├── antecedent_analyzer.py      # Antecedent distance calculation
│   ├── sentence_processor.py       # Sentence-level processing
│   └── phrase_grouper.py           # Token-to-phrase grouping
├── data/
│   ├── __init__.py
│   └── models.py               # Data classes and structures
└── tests/
    ├── __init__.py
    ├── test_parsers.py
    ├── test_extractors.py
    ├── test_analyzers.py
    └── fixtures/               # Test data
```

#### 1.2 Define Module Interfaces

Create clear interfaces between modules using abstract base classes:

```python
# src/parsers/base.py
from abc import ABC, abstractmethod
from typing import Iterator, Dict, Any

class BaseParser(ABC):
    @abstractmethod
    def parse_file(self, file_path: str) -> Iterator[Dict[str, Any]]:
        """Parse file and yield sentence tokens."""
        pass

# src/extractors/base.py
class BaseExtractor(ABC):
    @abstractmethod
    def extract_relationships(self, sentences: Iterator[Dict]) -> List[Dict]:
        """Extract clause mate relationships."""
        pass
```

### **Task 2: Data Structure Optimization** (Week 1-2)

#### 2.1 Create Structured Data Models

Replace dictionaries with typed data classes:

```python
# src/data/models.py
from dataclasses import dataclass
from typing import Optional, List, Set
from enum import Enum

class AnimacyType(Enum):
    ANIMATE = "anim"
    INANIMATE = "inanim"

@dataclass
class Token:
    idx: int
    text: str
    sentence_num: int
    grammatical_role: str
    thematic_role: str
    coreference_link: Optional[str] = None
    coreference_type: Optional[str] = None
    inanimate_coreference_link: Optional[str] = None
    inanimate_coreference_type: Optional[str] = None

@dataclass
class Phrase:
    text: str
    coreference_id: str
    start_idx: int
    end_idx: int
    grammatical_role: str
    thematic_role: str
    coreference_type: str
    animacy: AnimacyType
    givenness: str

@dataclass
class ClauseMateRelationship:
    sentence_id: str
    sentence_num: int
    pronoun: Token
    clause_mate: Phrase
    num_clause_mates: int
    antecedent_info: 'AntecedentInfo'
```

#### 2.2 Simplified Data Processing

Replace complex data structures with clean, readable implementations:

```python
# src/parsers/simple_parser.py
def parse_file_completely(file_path: str) -> Dict[str, List[Token]]:
    """Parse entire file into sentence groups - prioritizing clarity over memory."""
    all_sentences = {}
    current_sentence = []
    current_sentence_id = None

    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            # Clear, straightforward parsing logic
            if is_sentence_boundary(line):
                if current_sentence and current_sentence_id:
                    all_sentences[current_sentence_id] = current_sentence
                current_sentence = []
                current_sentence_id = None
            else:
                token = parse_token_line(line)
                if token:
                    current_sentence.append(token)

    return all_sentences
```

### **Task 3: Code Duplication Elimination** (Week 2)

#### 3.1 Abstract Coreference Processing

Currently, coreference ID extraction logic appears 6+ times. Create single source of truth:

```python
# src/extractors/coreference_extractor.py
class CoreferenceExtractor:
    """Single source of truth for all coreference ID extraction."""

    def extract_all_ids(self, token: Token) -> Set[str]:
        """Extract all coreference IDs from a token."""
        ids = set()

        # Animate layer
        if animate_id := self._extract_from_link(token.coreference_link):
            ids.add(animate_id)
        elif animate_id := self._extract_from_type(token.coreference_type):
            ids.add(animate_id)

        # Inanimate layer
        if inanimate_id := self._extract_from_link(token.inanimate_coreference_link):
            ids.add(inanimate_id)
        elif inanimate_id := self._extract_from_type(token.inanimate_coreference_type):
            ids.add(inanimate_id)

        return ids

    def _extract_from_link(self, link: Optional[str]) -> Optional[str]:
        """Extract ID from coreference link format."""
        # Centralized implementation
        pass

    def _extract_from_type(self, type_str: Optional[str]) -> Optional[str]:
        """Extract ID from coreference type format."""
        # Centralized implementation
        pass
```

#### 3.2 Abstract Token Processing Patterns

```python
# src/analyzers/token_analyzer.py
class TokenAnalyzer:
    """Reusable token processing patterns."""

    def group_by_coreference(self, tokens: List[Token]) -> Dict[str, List[Token]]:
        """Group tokens by coreference ID."""
        pass

    def filter_critical_pronouns(self, tokens: List[Token]) -> List[Token]:
        """Filter tokens to only critical pronouns."""
        pass

    def build_sentence_context(self, tokens: List[Token]) -> SentenceContext:
        """Build rich context object for sentence."""
        pass
```

### **Task 4: Comprehensive Testing** (Week 2-3)

#### 4.1 Unit Test Suite

```python
# tests/test_parsers.py
import pytest
from src.parsers.tsv_parser import TSVParser
from src.data.models import Token

class TestTSVParser:
    def test_parse_valid_token_line(self):
        """Test parsing a valid token line."""
        parser = TSVParser()
        line = "1-1\ter\t...\t..."  # Sample TSV line
        token = parser.parse_token_line(line)

        assert token.text == "er"
        assert token.idx == 1
        assert token.sentence_num == 1

    def test_parse_malformed_line(self):
        """Test handling of malformed input."""
        parser = TSVParser()
        with pytest.raises(ParseError):
            parser.parse_token_line("invalid\tline")

    def test_streaming_parsing(self):
        """Test memory-efficient streaming parsing."""
        parser = TSVParser()
        sentences = list(parser.parse_sentences_streaming("test_file.tsv"))

        assert len(sentences) > 0
        assert all(isinstance(s, list) for s in sentences)
```

#### 4.2 Integration Tests

```python
# tests/test_integration.py
class TestEndToEnd:
    def test_complete_pipeline(self):
        """Test complete processing pipeline."""
        from src.main import ClauseMateAnalyzer

        analyzer = ClauseMateAnalyzer()
        relationships = analyzer.analyze_file("tests/fixtures/sample.tsv")

        assert len(relationships) > 0
        assert all(r.pronoun.text in CRITICAL_PRONOUNS for r in relationships)
```

#### 4.3 Functional Tests

```python
# tests/test_functionality.py
class TestFunctionality:
    def test_output_consistency(self):
        """Ensure refactored code produces identical results."""
        from src.main import ClauseMateAnalyzer

        analyzer = ClauseMateAnalyzer()
        relationships = analyzer.analyze_file("tests/fixtures/sample.tsv")

        # Verify relationships match expected format and content
        assert len(relationships) > 0
        assert all(r.pronoun.text in CRITICAL_PRONOUNS for r in relationships)

        # Compare with known good output
        expected_df = pd.read_csv("tests/fixtures/expected_output.csv")
        actual_df = pd.DataFrame([r.to_dict() for r in relationships])

        pd.testing.assert_frame_equal(actual_df, expected_df)
```

### **Task 5: Clean Module Integration** (Week 3)

#### 5.1 Simplified Processing Pipeline

```python
# src/main.py
class ClauseMateAnalyzer:
    """Clean, straightforward analyzer focusing on maintainability."""

    def __init__(self):
        self.parser = TSVParser()
        self.extractor = RelationshipExtractor()
        self.pronoun_classifier = PronounClassifier()

    def analyze_file(self, file_path: str) -> List[ClauseMateRelationship]:
        """Simple, clear analysis pipeline."""
        # Parse all sentences
        sentences = self.parser.parse_file_completely(file_path)

        # Extract relationships
        all_relationships = []
        for sentence_id, tokens in sentences.items():
            relationships = self.extractor.extract_from_sentence(tokens, sentences)
            all_relationships.extend(relationships)

        return all_relationships
```

#### 5.2 Clear Configuration Management

```python
# src/config_manager.py
class ConfigurationManager:
    """Centralized configuration without complex optimization."""

    def __init__(self):
        self.tsv_columns = TSVColumns()
        self.file_paths = FilePaths()
        self.constants = Constants()

    def get_column_mapping(self) -> Dict[str, int]:
        """Return clear column mappings."""
        return {
            'token_id': self.tsv_columns.TOKEN_ID,
            'token_text': self.tsv_columns.TOKEN_TEXT,
            'grammatical_role': self.tsv_columns.GRAMMATICAL_ROLE,
            # ... other mappings
        }
```

### **Task 6: Main Script Refactoring** (Week 4)

#### 6.1 Slim Main Script

```python
# clause_mates_complete.py (refactored)
#!/usr/bin/env python3
"""
Clause mate extraction script - Phase 2 refactored version.
Main orchestration script using modular architecture.
"""

from src.main import ClauseMateAnalyzer
from src.config import FilePaths
import logging

def main():
    """Main entry point - orchestrates the analysis pipeline."""
    logging.basicConfig(level=logging.INFO)

    analyzer = ClauseMateAnalyzer()

    try:
        # Simple, clean main function
        relationships = analyzer.analyze_file(FilePaths.INPUT_FILE)
        analyzer.export_results(relationships, FilePaths.OUTPUT_FILE)

        logging.info(f"Successfully processed {len(relationships)} relationships")

    except Exception as e:
        logging.error(f"Analysis failed: {e}")
        raise

if __name__ == "__main__":
    main()
```

#### 6.2 CLI Interface Enhancement

```python
# src/cli.py
import argparse
from pathlib import Path

def create_parser() -> argparse.ArgumentParser:
    """Create command-line argument parser."""
    parser = argparse.ArgumentParser(description="Clause Mate Analyzer")

    parser.add_argument("input_file", help="Input TSV file path")
    parser.add_argument("-o", "--output", help="Output CSV file path")
    parser.add_argument("--streaming", action="store_true",
                       help="Use streaming processing for large files")
    parser.add_argument("--verbose", "-v", action="store_true",
                       help="Enable verbose logging")

    return parser
```

## Implementation Timeline

### **Week 1: Architecture Foundation**

- **Days 1-2**: Design module structure and interfaces
- **Days 3-4**: Create data models and base classes
- **Day 5**: Implement basic parsing module

### **Week 2: Core Refactoring**

- **Days 1-2**: Extract and abstract coreference processing
- **Days 3-4**: Implement relationship extraction module
- **Day 5**: Create comprehensive unit tests

### **Week 3: Testing & Integration**

- **Days 1-2**: Complete test suite development
- **Days 3-4**: Module integration and validation
- **Day 5**: Documentation and code cleanup

### **Week 4: Final Integration**

- **Days 1-2**: Refactor main script and CLI interface
- **Days 3-4**: End-to-end testing and validation
- **Day 5**: Final documentation and cleanup

## Risk Mitigation

### **Technical Risks**

1. **Breaking existing functionality** → Comprehensive test suite before refactoring
2. **Complex refactoring** → Incremental changes with validation at each step
3. **Module integration issues** → Clear interfaces and integration testing

### **Mitigation Strategies**

- **Keep backup** of working Phase 1 code
- **Incremental development** with frequent testing
- **Parallel development** - new modules alongside existing code
- **Output validation** - compare results between old and new implementations

## Quality Assurance

### **Code Quality Gates**

- **100% test coverage** for new modules
- **Type checking** with mypy passes
- **Linting** with flake8/black passes
- **Functional equivalence** - identical output to Phase 1 script
- **Code organization** - clear module boundaries and responsibilities

### **Validation Criteria**

- **Functional equivalence** - identical output to Phase 1 script
- **Maintainability** - reduced cyclomatic complexity
- **Testability** - isolated, mockable components
- **Code clarity** - improved readability and documentation

## Expected Outcomes

### **Technical Benefits**

- **Modular architecture** enables easy testing and maintenance
- **Clear code organization** improves readability and understanding
- **Comprehensive testing** ensures reliability and confidence
- **Better error handling** with specific, actionable error messages

### **Development Benefits**

- **Faster debugging** through isolated components
- **Easier feature addition** via clear module boundaries
- **Better collaboration** through well-defined interfaces
- **Confident refactoring** backed by comprehensive tests

### **Long-term Value**

- **Foundation for Phase 3** advanced features
- **Maintainable architecture** for future requirements
- **Production-ready codebase** suitable for deployment
- **Knowledge base** for team development

## Next Steps After Phase 2

### **Immediate Validation**

1. **Run full test suite** and ensure 100% pass rate
2. **Output validation** - byte-for-byte comparison with existing results
3. **Code review** and documentation completion
4. **Module integration verification**

### **Preparation for Phase 3**

1. **Plugin architecture** foundation in place
2. **Configuration system** ready for external config files
3. **Logging infrastructure** prepared for advanced features
4. **Clean module boundaries** ready for extension

---

**Phase 2 represents a crucial transformation from working prototype to maintainable, well-structured software. The modular architecture will serve as a solid foundation for all future enhancements while delivering immediate benefits in maintainability, testability, and code clarity.**
