#!/usr/bin/env python3
"""Enhanced data source loader for ClauseMate analyzer.

Supports multiple data source types while maintaining security for private research data.
"""

import logging
import os
import subprocess
from pathlib import Path
from typing import Any

# Load environment variables from .env file if it exists
try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    # dotenv not installed, continue with system environment variables only
    pass


class DataSourceLoader:
    """Handles loading data from various secure sources."""

    def __init__(self, project_root: Path | None = None):
        """Initialize the data source loader."""
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

        # Check for private directory (with or without git)
        private_dir = self.project_root / "data" / "input" / "private"
        if private_dir.exists() and list(private_dir.rglob("*.tsv")):
            if (private_dir / ".git").exists():
                self.logger.info(f"Using private git repository: {private_dir}")
                # Optionally update repository
                self.update_private_repository(private_dir)
            else:
                self.logger.info(f"Using private local data: {private_dir}")
            return private_dir

        # Default to test data
        default_dir = self.project_root / "data" / "input" / "gotofiles"
        self.logger.info(f"Using default test data: {default_dir}")
        return default_dir

    def update_private_repository(self, repo_path: Path) -> bool:
        """Update private git repository if possible."""
        try:
            # Check if git is available
            subprocess.run(["git", "--version"], capture_output=True, check=True)

            # Pull latest changes
            result = subprocess.run(
                ["git", "pull", "origin", "main"],
                cwd=repo_path,
                capture_output=True,
                text=True,
                timeout=30,
            )

            if result.returncode == 0:
                self.logger.info("Successfully updated private repository")
                return True
            else:
                self.logger.warning(f"Could not update repository: {result.stderr}")
                return False

        except (
            subprocess.CalledProcessError,
            subprocess.TimeoutExpired,
            FileNotFoundError,
        ):
            self.logger.debug(
                "Could not update private repository (git not available or no remote)"
            )
            return False

    def get_repository_status(self) -> dict[str, Any]:
        """Get git repository status for private data."""
        private_dir = self.project_root / "data" / "input" / "private"

        if not (private_dir / ".git").exists():
            return {"is_repository": False}

        try:
            # Get current branch
            branch_result = subprocess.run(
                ["git", "rev-parse", "--abbrev-ref", "HEAD"],
                cwd=private_dir,
                capture_output=True,
                text=True,
                check=True,
            )

            # Get remote URL
            remote_result = subprocess.run(
                ["git", "remote", "get-url", "origin"],
                cwd=private_dir,
                capture_output=True,
                text=True,
            )

            # Get last commit
            commit_result = subprocess.run(
                ["git", "log", "-1", "--pretty=format:%h %s (%ar)"],
                cwd=private_dir,
                capture_output=True,
                text=True,
                check=True,
            )

            return {
                "is_repository": True,
                "branch": branch_result.stdout.strip(),
                "remote": remote_result.stdout.strip()
                if remote_result.returncode == 0
                else None,
                "last_commit": commit_result.stdout.strip(),
            }

        except (subprocess.CalledProcessError, FileNotFoundError):
            return {"is_repository": True, "error": "Git operations failed"}

    def get_available_files(self) -> list[Path]:
        """Get list of available TSV files from current data source."""
        data_dir = self.get_data_directory()
        return list(data_dir.glob("*.tsv"))

    def get_data_source_info(self) -> dict[str, Any]:
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
            "is_private": "private" in str(data_dir) or source_type != "test_data",
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

    if info["files"]:
        print("\nAvailable Files:")
        for filename in info["files"]:
            print(f"  - {filename}")
    else:
        print("\n⚠️  No TSV files found!")
        print("Run: python scripts/setup_data_source.py")
