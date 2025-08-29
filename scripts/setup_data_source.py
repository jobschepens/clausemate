#!/usr/bin/env python3
"""Data Source Setup Script for ClauseMate Analyzer.

This script helps set up secure data sources for the ClauseMate analyzer,
supporting multiple options for private research data while maintaining
security and not exposing sensitive data in public repositories.
"""

import os
import sys
import getpass
import zipfile
import shutil
from pathlib import Path
from typing import Optional, Dict, Any
import requests
import json


class DataSourceManager:
    """Manages different data source configurations for ClauseMate."""
    
    def __init__(self, project_root: Optional[Path] = None):
        self.project_root = project_root or Path(__file__).parent
        self.data_dir = self.project_root / "data" / "input"
        self.private_dir = self.data_dir / "private"
        self.env_file = self.project_root / ".env"
        
    def detect_current_source(self) -> Dict[str, Any]:
        """Detect currently configured data source."""
        config = {
            "source_type": "test_data",
            "path": str(self.data_dir / "gotofiles"),
            "files_count": 0,
            "description": "Default test data"
        }
        
        # Check environment variables
        if os.getenv("CLAUSEMATE_DATA_SOURCE"):
            config["source_type"] = os.getenv("CLAUSEMATE_DATA_SOURCE")
            config["description"] = "Environment configured"
            
        # Check private directory
        if self.private_dir.exists():
            tsv_files = list(self.private_dir.glob("*.tsv"))
            if tsv_files:
                config.update({
                    "source_type": "private_local",
                    "path": str(self.private_dir),
                    "files_count": len(tsv_files),
                    "description": f"Private local data ({len(tsv_files)} files)"
                })
                
        # Count files in current path
        if Path(config["path"]).exists():
            config["files_count"] = len(list(Path(config["path"]).glob("*.tsv")))
            
        return config
    
    def setup_private_directory(self) -> bool:
        """Set up private data directory structure."""
        try:
            self.private_dir.mkdir(parents=True, exist_ok=True)
            
            # Create README for private directory
            readme_path = self.private_dir / "README.md"
            readme_content = """# Private Data Directory

This directory contains private research data that is not committed to git.

## Usage
- Place your TSV files here
- The analyzer will automatically use this data when available
- Files here take precedence over test data

## Security
- This directory is in .gitignore
- No files here will be committed to the repository
- Use appropriate file permissions for sensitive data
"""
            readme_path.write_text(readme_content)
            return True
        except Exception as e:
            print(f"Error creating private directory: {e}")
            return False
    
    def setup_password_protected_source(self) -> bool:
        """Set up password-protected data source."""
        print("\n📁 Setting up password-protected data source...")
        
        source_type = input("Data source type [zip/url/local]: ").strip().lower()
        
        if source_type == "zip":
            return self._setup_encrypted_zip()
        elif source_type == "url":
            return self._setup_remote_url()
        elif source_type == "local":
            return self._setup_local_path()
        else:
            print("❌ Invalid source type")
            return False
    
    def _setup_encrypted_zip(self) -> bool:
        """Set up encrypted ZIP file data source."""
        zip_path = input("Path to encrypted ZIP file: ").strip()
        if not Path(zip_path).exists():
            print(f"❌ File not found: {zip_path}")
            return False
            
        password = getpass.getpass("ZIP password: ")
        
        try:
            # Test password
            with zipfile.ZipFile(zip_path, 'r') as zip_file:
                zip_file.testzip()
                # Try to extract one file to test password
                names = zip_file.namelist()
                if names:
                    zip_file.read(names[0], pwd=password.encode())
            
            # Save configuration
            self._save_env_config({
                "CLAUSEMATE_DATA_SOURCE": "encrypted_zip",
                "CLAUSEMATE_ZIP_PATH": zip_path,
                "CLAUSEMATE_ZIP_PASSWORD": password  # Note: Consider more secure storage
            })
            
            print("✅ Encrypted ZIP configured successfully")
            return True
            
        except Exception as e:
            print(f"❌ Error testing ZIP file: {e}")
            return False
    
    def _setup_remote_url(self) -> bool:
        """Set up remote URL data source."""
        url = input("Data download URL: ").strip()
        token = getpass.getpass("Access token (optional): ")
        
        # Test URL
        try:
            headers = {}
            if token:
                headers["Authorization"] = f"Bearer {token}"
            
            response = requests.head(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            # Save configuration
            config = {
                "CLAUSEMATE_DATA_SOURCE": "remote_url",
                "CLAUSEMATE_DATA_URL": url
            }
            if token:
                config["CLAUSEMATE_ACCESS_TOKEN"] = token
                
            self._save_env_config(config)
            
            print("✅ Remote URL configured successfully")
            return True
            
        except Exception as e:
            print(f"❌ Error testing URL: {e}")
            return False
    
    def _setup_local_path(self) -> bool:
        """Set up local path data source."""
        path = input("Local data directory path: ").strip()
        path_obj = Path(path).expanduser().resolve()
        
        if not path_obj.exists():
            create = input(f"Directory doesn't exist. Create it? [y/N]: ").strip().lower()
            if create == 'y':
                try:
                    path_obj.mkdir(parents=True, exist_ok=True)
                except Exception as e:
                    print(f"❌ Error creating directory: {e}")
                    return False
            else:
                return False
        
        # Save configuration
        self._save_env_config({
            "CLAUSEMATE_DATA_SOURCE": "local_path",
            "CLAUSEMATE_DATA_PATH": str(path_obj)
        })
        
        print("✅ Local path configured successfully")
        return True
    
    def _save_env_config(self, config: Dict[str, str]) -> None:
        """Save configuration to .env file."""
        env_content = []
        
        # Read existing .env if it exists
        if self.env_file.exists():
            with open(self.env_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        key = line.split('=')[0]
                        if key not in config:
                            env_content.append(line)
        
        # Add new configuration
        env_content.append("# ClauseMate Data Source Configuration")
        for key, value in config.items():
            env_content.append(f"{key}={value}")
        
        # Write .env file
        with open(self.env_file, 'w') as f:
            f.write('\n'.join(env_content) + '\n')
    
    def load_data_source(self) -> bool:
        """Load data from configured source."""
        source_type = os.getenv("CLAUSEMATE_DATA_SOURCE", "test_data")
        
        if source_type == "encrypted_zip":
            return self._load_from_zip()
        elif source_type == "remote_url":
            return self._load_from_url()
        elif source_type == "local_path":
            return self._load_from_local_path()
        else:
            print("ℹ️  Using default test data")
            return True
    
    def _load_from_zip(self) -> bool:
        """Load data from encrypted ZIP file."""
        zip_path = os.getenv("CLAUSEMATE_ZIP_PATH")
        password = os.getenv("CLAUSEMATE_ZIP_PASSWORD")
        
        if not password:
            password = getpass.getpass("Enter ZIP password: ")
        
        try:
            self.setup_private_directory()
            
            with zipfile.ZipFile(zip_path, 'r') as zip_file:
                zip_file.extractall(self.private_dir, pwd=password.encode())
            
            print(f"✅ Data extracted to {self.private_dir}")
            return True
            
        except Exception as e:
            print(f"❌ Error extracting ZIP: {e}")
            return False
    
    def _load_from_url(self) -> bool:
        """Load data from remote URL."""
        url = os.getenv("CLAUSEMATE_DATA_URL")
        token = os.getenv("CLAUSEMATE_ACCESS_TOKEN")
        
        try:
            headers = {}
            if token:
                headers["Authorization"] = f"Bearer {token}"
            
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            
            self.setup_private_directory()
            
            # Assume ZIP format for now
            zip_path = self.private_dir / "downloaded_data.zip"
            with open(zip_path, 'wb') as f:
                f.write(response.content)
            
            # Extract if it's a ZIP
            if zipfile.is_zipfile(zip_path):
                with zipfile.ZipFile(zip_path, 'r') as zip_file:
                    zip_file.extractall(self.private_dir)
                zip_path.unlink()  # Remove the ZIP after extraction
            
            print(f"✅ Data downloaded to {self.private_dir}")
            return True
            
        except Exception as e:
            print(f"❌ Error downloading data: {e}")
            return False
    
    def _load_from_local_path(self) -> bool:
        """Load data from local path."""
        source_path = Path(os.getenv("CLAUSEMATE_DATA_PATH"))
        
        if not source_path.exists():
            print(f"❌ Source path doesn't exist: {source_path}")
            return False
        
        # Copy TSV files to private directory
        self.setup_private_directory()
        
        copied_count = 0
        for tsv_file in source_path.glob("*.tsv"):
            shutil.copy2(tsv_file, self.private_dir)
            copied_count += 1
        
        print(f"✅ Copied {copied_count} files to {self.private_dir}")
        return True


def main():
    """Main entry point for data source setup."""
    print("🔧 ClauseMate Data Source Setup")
    print("=" * 40)
    
    manager = DataSourceManager()
    
    # Show current configuration
    current = manager.detect_current_source()
    print(f"📊 Current data source: {current['description']}")
    print(f"   Path: {current['path']}")
    print(f"   Files: {current['files_count']} TSV files")
    
    # Menu
    print("\nOptions:")
    print("1. Set up private local directory")
    print("2. Configure password-protected source")
    print("3. Load data from configured source")
    print("4. Show current configuration")
    print("5. Exit")
    
    choice = input("\nSelect option [1-5]: ").strip()
    
    if choice == "1":
        if manager.setup_private_directory():
            print("✅ Private directory set up successfully")
            print(f"   Place your TSV files in: {manager.private_dir}")
        else:
            print("❌ Failed to set up private directory")
    
    elif choice == "2":
        manager.setup_password_protected_source()
    
    elif choice == "3":
        manager.load_data_source()
    
    elif choice == "4":
        config = manager.detect_current_source()
        print(f"\n📋 Current Configuration:")
        print(f"   Source Type: {config['source_type']}")
        print(f"   Path: {config['path']}")
        print(f"   Files Count: {config['files_count']}")
        print(f"   Description: {config['description']}")
        
        # Show environment variables
        env_vars = [k for k in os.environ.keys() if k.startswith("CLAUSEMATE_")]
        if env_vars:
            print(f"\n🔧 Environment Variables:")
            for var in env_vars:
                value = os.getenv(var)
                # Hide sensitive values
                if "PASSWORD" in var or "TOKEN" in var:
                    value = "*" * len(value) if value else "Not set"
                print(f"   {var}={value}")
    
    elif choice == "5":
        print("👋 Goodbye!")
        return
    
    else:
        print("❌ Invalid choice")


if __name__ == "__main__":
    main()
