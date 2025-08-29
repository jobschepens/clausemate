# ClauseMate Type Annotation Style Guide

This document establishes consistent typing conventions for the ClauseMate project.

## Modern Python 3.11+ Type Annotations

We use modern type annotation syntax supported by Python 3.11+.

### ✅ Preferred (Modern Syntax)

```python
# Built-in collections (Python 3.9+)
def process_data(data: dict[str, list[int]]) -> tuple[str, int]:
    return "result", 42

# Union types (Python 3.10+)
def handle_value(value: str | int | None) -> bool:
    return value is not None

# Generic types
from collections.abc import Sequence, Mapping
def process_items(items: Sequence[str]) -> Mapping[str, int]:
    return {item: len(item) for item in items}
```

### ❌ Avoid (Legacy Syntax)

```python
# Legacy typing imports (pre-3.9)
from typing import Dict, List, Tuple, Union, Optional

def process_data(data: Dict[str, List[int]]) -> Tuple[str, int]:
    return "result", 42

def handle_value(value: Union[str, int, None]) -> bool:
    return value is not None

def handle_optional(value: Optional[str]) -> bool:
    return value is not None
```

## Type Annotation Guidelines

### 1. Function Signatures
Always annotate public function parameters and return types:

```python
def extract_relationships(
    sentences: list[SentenceContext],
    config: dict[str, Any],
) -> list[ClauseMateRelationship]:
    """Extract clause mate relationships from sentences."""
    # Implementation here
    return []
```

### 2. Class Attributes
Use dataclasses with type annotations:

```python
from dataclasses import dataclass

@dataclass
class ProcessingResult:
    relationships: list[ClauseMateRelationship]
    metadata: dict[str, Any]
    errors: list[str] = None
    
    def __post_init__(self) -> None:
        if self.errors is None:
            self.errors = []
```

### 3. Complex Types
Define type aliases for complex or repeated types:

```python
from typing import TypeAlias

# Type aliases for clarity
TokenDict: TypeAlias = dict[str, str | int]
RelationshipList: TypeAlias = list[ClauseMateRelationship]
ChapterMetadata: TypeAlias = dict[str, str | int | float]

def process_chapters(
    metadata: ChapterMetadata,
    tokens: list[TokenDict],
) -> RelationshipList:
    # Implementation
    return []
```

### 4. Generic Classes
Use proper generic syntax:

```python
from typing import Generic, TypeVar

T = TypeVar('T')

class DataProcessor(Generic[T]):
    def process(self, data: list[T]) -> list[T]:
        return data
```

## Tool Configuration

### Ruff Configuration
Our `pyproject.toml` includes pyupgrade rules to enforce modern syntax:

```toml
[tool.ruff.lint]
select = [
    "UP",    # pyupgrade - enforces modern syntax
    # ... other rules
]
```

### Pylance Configuration
VS Code settings configured to prefer modern syntax:

```json
{
    "python.analysis.typeCheckingMode": "basic",
    "python.analysis.diagnosticSeverityOverrides": {
        "reportUnknownParameterType": "information",
        "reportUnknownVariableType": "information"
    }
}
```

## Migration Strategy

1. **New Code**: Always use modern syntax
2. **Existing Code**: Use `ruff check --fix --select UP` to modernize
3. **Scripts vs Libraries**: 
   - Core library code (`src/`): Full type annotation coverage
   - Scripts (`scripts/`): Basic annotations, focus on functionality
   - Tools (`tools/`): Minimal annotations acceptable

## Enforcement

- **Pre-commit hooks**: Catch style violations before commit
- **Ruff**: Enforces modern syntax via pyupgrade rules
- **CI/CD**: Type checking in continuous integration

## Examples by Module Type

### Core Data Models (`src/data/models.py`)
```python
@dataclass
class ClauseMateRelationship:
    sentence_id: str
    pronoun: Token
    clause_mate: Phrase
    metadata: dict[str, Any] = None
    
    def to_dict(self) -> dict[str, str | int | None]:
        """Convert to dictionary for export."""
        return {...}
```

### Analysis Scripts (`scripts/`)
```python
def analyze_data(
    input_file: str,
    output_dir: str,
) -> None:
    """Analyze clause mate data and generate reports."""
    # Basic annotations sufficient for scripts
    pass
```

### Utility Functions (`src/utils/`)
```python
def extract_coreference_id(
    value: str,
) -> str | None:
    """Extract coreference ID from annotation value."""
    if not value or value == "_":
        return None
    # Implementation
    return extracted_id
```

This style guide ensures consistency across the codebase while leveraging modern Python features.
