#!/usr/bin/env python3
"""
Entry point for the Phase 2 Clause Mates Analyzer.

This script provides the main command-line interface for running the modular
clause mates analysis pipeline.
"""

import sys
from pathlib import Path

# Add the src directory to the Python path
src_path = Path(__file__).parent / 'src'
sys.path.insert(0, str(src_path))
sys.path.insert(0, str(Path(__file__).parent))

# Now we can import from our modules
from src.main import main

if __name__ == "__main__":
    sys.exit(main())
