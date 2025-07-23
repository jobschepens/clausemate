#!/usr/bin/env python3
"""
Entry point for the Phase 2 Clause Mates Analyzer.

This script provides the main command-line interface for running the modular
clause mates analysis pipeline.
"""

import sys
from pathlib import Path

# Add parent directory to path so we can import src modules
parent_dir = Path(__file__).parent.parent
sys.path.insert(0, str(parent_dir))

from src.main import main

if __name__ == "__main__":
    sys.exit(main())
