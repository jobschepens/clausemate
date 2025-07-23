"""Extractors package for coreference and relationship extraction."""

import sys
from pathlib import Path

from src.extractors.coreference_extractor import CoreferenceExtractor

# Add the parent directory to the path to import from root
sys.path.append(str(Path(__file__).parent.parent.parent))


__all__ = [
    "CoreferenceExtractor",
]
