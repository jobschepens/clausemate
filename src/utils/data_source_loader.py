#!/usr/bin/env python3
"""Enhanced data source loader for ClauseMate analyzer.

Supports multiple data source types while maintaining security for private research data.
"""

import os
import sys
from pathlib import Path
from typing import Optional, List, Dict, Any
import logging

# Load environment variables from .env file if it exists
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # dotenv not installed, continue with system environment variables only
    pass


class DataSourceLoader:
    """Handles loading data from various secure sources."""
    
    def __init__(self, project_root: Optional[Path] = None):
        self.project_root = project_root or Path(__file__).parent.parent
        self.logger = logging.getLogger(__name__)
        
    def get_data_directory(self) -> Path:
        """Get the appropriate data directory based on configuration."""
        source_type = os.getenv("CLAUSEMATE_DATA_SOURCE", "test_data")
        
        if source_type == "private_local":
            private_dir = self.project_root / "data" / "input" / "private"
            if private_dir.exists() and list(private_dir.glob("*.tsv")):
                self.logger.info(f"Using private local data: {private_dir}")
                return private_dir
                
        elif source_type == "local_path":
            custom_path = os.getenv("CLAUSEMATE_DATA_PATH")
            if custom_path:
                custom_dir = Path(custom_path)
                if custom_dir.exists():
                    self.logger.info(f"Using custom local path: {custom_dir}")
                    return custom_dir
                else:
                    self.logger.warning(f"Custom path not found: {custom_dir}")
        
        # Default to test data
        default_dir = self.project_root / "data" / "input" / "gotofiles"
        self.logger.info(f"Using default test data: {default_dir}")
        return default_dir
    
    def get_available_files(self) -> List[Path]:
        """Get list of available TSV files from current data source."""
        data_dir = self.get_data_directory()
        return list(data_dir.glob("*.tsv"))
    
    def get_data_source_info(self) -> Dict[str, Any]:
        """Get information about current data source."""
        data_dir = self.get_data_directory()
        files = self.get_available_files()
        
        source_type = os.getenv("CLAUSEMATE_DATA_SOURCE", "test_data")
        
        return {
            "source_type": source_type,
            "directory": str(data_dir),
            "files_count": len(files),
            "files": [f.name for f in files],
            "total_size_mb": sum(f.stat().st_size for f in files) / (1024 * 1024),
            "is_private": "private" in str(data_dir) or source_type != "test_data"
        }
    
    def ensure_data_available(self) -> bool:
        """Ensure data is available and accessible."""
        try:
            files = self.get_available_files()
            if not files:
                self.logger.warning("No TSV files found in data source")
                return False
            
            self.logger.info(f"Data source ready: {len(files)} files available")
            return True
            
        except Exception as e:
            self.logger.error(f"Error accessing data source: {e}")
            return False


def setup_data_source_for_main():
    """Set up data source for main analyzer functions."""
    loader = DataSourceLoader()
    
    # Check if data is available
    if not loader.ensure_data_available():
        print("⚠️  No data files found!")
        print("\nOptions:")
        print("1. Run: python scripts/setup_data_source.py")
        print("2. Place TSV files in: data/input/gotofiles/")
        print("3. Set CLAUSEMATE_DATA_PATH environment variable")
        return None
    
    # Return data directory for use
    return loader.get_data_directory()


if __name__ == "__main__":
    # Demo the data source loader
    loader = DataSourceLoader()
    info = loader.get_data_source_info()
    
    print("📊 ClauseMate Data Source Status")
    print("=" * 40)
    print(f"Source Type: {info['source_type']}")
    print(f"Directory: {info['directory']}")
    print(f"Files Count: {info['files_count']}")
    print(f"Total Size: {info['total_size_mb']:.2f} MB")
    print(f"Is Private: {'Yes' if info['is_private'] else 'No'}")
    
    if info['files']:
        print(f"\nAvailable Files:")
        for filename in info['files']:
            print(f"  - {filename}")
    else:
        print("\n⚠️  No TSV files found!")
        print("Run: python scripts/setup_data_source.py")
