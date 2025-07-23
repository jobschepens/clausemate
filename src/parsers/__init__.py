"""Parsers package for TSV file parsing and token processing."""

import sys
from pathlib import Path

from src.parsers.tsv_parser import TSVParser

# Add the parent directory to the path to import from root
sys.path.append(str(Path(__file__).parent.parent.parent))


__all__ = [
    "TSVParser",
]
