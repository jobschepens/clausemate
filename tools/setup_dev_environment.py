#!/usr/bin/env python3
"""Setup development environment for ClauseMate."""

import subprocess
import sys
from pathlib import Path

def setup_environment():
    """Install ClauseMate in editable mode for development."""
    
    project_root = Path(__file__).resolve().parents[1]
    
    print("Setting up ClauseMate development environment...")
    print(f"Project root: {project_root}")
    
    # Install in editable mode
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-e", "."
        ], cwd=project_root)
        print("✓ ClauseMate installed in editable mode")
        
        # Verify imports work
        subprocess.check_call([
            sys.executable, "-c", 
            "from src.main import main; print('✓ Import verification successful')"
        ], cwd=project_root)
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Setup failed: {e}")
        return False

if __name__ == "__main__":
    success = setup_environment()
    sys.exit(0 if success else 1)
