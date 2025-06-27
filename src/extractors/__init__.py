"""
Extractors package for coreference and relationship extraction.
"""

import sys
from pathlib import Path

# Add the parent directory to the path to import from root
sys.path.append(str(Path(__file__).parent.parent.parent))

from src.extractors.coreference_extractor import CoreferenceExtractor

__all__ = [
    "CoreferenceExtractor",
]
