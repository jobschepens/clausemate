"""Tests for data_source_loader.py."""

import os
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

from src.utils.data_source_loader import (
    DataSourceLoader,
    setup_data_source_for_main,
)


class TestDataSourceLoader:
    """Test the DataSourceLoader class."""

    def setup_method(self):
        """Set up test fixtures."""
        self.temp_dir = Path(tempfile.mkdtemp())
        self.loader = DataSourceLoader(self.temp_dir)

    def teardown_method(self):
        """Clean up test fixtures."""
        import shutil

        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_initialization(self):
        """Test that the loader initializes correctly."""
        assert self.loader.project_root == self.temp_dir
        assert hasattr(self.loader, "logger")

    def test_initialization_default_root(self):
        """Test initialization with default project root."""
        loader = DataSourceLoader()
        assert loader.project_root.exists()
        assert "clausemate" in str(loader.project_root).lower()

    @patch.dict(os.environ, {"CLAUSEMATE_DATA_SOURCE": "test_data"})
    def test_get_data_directory_test_data(self):
        """Test get_data_directory with test_data source."""
        # Create test data directory
        test_dir = self.temp_dir / "data" / "input" / "gotofiles"
        test_dir.mkdir(parents=True)

        result = self.loader.get_data_directory()
        assert result == test_dir

    @patch.dict(os.environ, {"CLAUSEMATE_DATA_SOURCE": "private_local"})
    def test_get_data_directory_private_local_exists(self):
        """Test get_data_directory with private_local when directory exists."""
        # Create private directory with files
        private_dir = self.temp_dir / "data" / "input" / "private"
        private_dir.mkdir(parents=True)
        (private_dir / "test.tsv").touch()

        result = self.loader.get_data_directory()
        assert result == private_dir

    @patch.dict(os.environ, {"CLAUSEMATE_DATA_SOURCE": "private_local"})
    def test_get_data_directory_private_local_not_exists(self):
        """Test get_data_directory with private_local when directory doesn't exist."""
        # Create test data directory as fallback
        test_dir = self.temp_dir / "data" / "input" / "gotofiles"
        test_dir.mkdir(parents=True)

        result = self.loader.get_data_directory()
        assert result == test_dir

    @patch.dict(
        os.environ,
        {
            "CLAUSEMATE_DATA_SOURCE": "local_path",
            "CLAUSEMATE_DATA_PATH": "/custom/path",
        },
    )
    def test_get_data_directory_custom_path_exists(self):
        """Test get_data_directory with custom path that exists."""
        with patch("pathlib.Path.exists", return_value=True):
            result = self.loader.get_data_directory()
            assert str(result) == str(Path("/custom/path"))

    @patch.dict(
        os.environ,
        {
            "CLAUSEMATE_DATA_SOURCE": "local_path",
            "CLAUSEMATE_DATA_PATH": "/nonexistent/path",
        },
    )
    def test_get_data_directory_custom_path_not_exists(self):
        """Test get_data_directory with custom path that doesn't exist."""
        # Create test data directory as fallback
        test_dir = self.temp_dir / "data" / "input" / "gotofiles"
        test_dir.mkdir(parents=True)

        result = self.loader.get_data_directory()
        assert result == test_dir

    def test_get_data_directory_private_git_repo(self):
        """Test get_data_directory with private git repository."""
        # Create private directory with .git
        private_dir = self.temp_dir / "data" / "input" / "private"
        private_dir.mkdir(parents=True)
        (private_dir / ".git").mkdir()
        (private_dir / "test.tsv").touch()

        result = self.loader.get_data_directory()
        assert result == private_dir

    @patch("subprocess.run")
    def test_update_private_repository_success(self, mock_subprocess):
        """Test successful private repository update."""
        # Mock successful git operations
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = ""
        mock_result.stderr = ""
        mock_subprocess.return_value = mock_result

        repo_path = self.temp_dir / "repo"
        repo_path.mkdir()

        result = self.loader.update_private_repository(repo_path)
        assert result is True

        # Verify git pull was called
        mock_subprocess.assert_called_with(
            ["git", "pull", "origin", "main"],
            cwd=repo_path,
            capture_output=True,
            text=True,
            timeout=30,
        )

    @patch("subprocess.run")
    def test_update_private_repository_failure(self, mock_subprocess):
        """Test failed private repository update."""
        # Mock failed git operations
        mock_result = MagicMock()
        mock_result.returncode = 1
        mock_result.stderr = "Pull failed"
        mock_subprocess.return_value = mock_result

        repo_path = self.temp_dir / "repo"
        repo_path.mkdir()

        result = self.loader.update_private_repository(repo_path)
        assert result is False

    @patch("subprocess.run")
    def test_update_private_repository_no_git(self, mock_subprocess):
        """Test private repository update when git is not available."""
        # Mock git not found
        mock_subprocess.side_effect = FileNotFoundError

        repo_path = self.temp_dir / "repo"
        repo_path.mkdir()

        result = self.loader.update_private_repository(repo_path)
        assert result is False

    def test_get_repository_status_no_repo(self):
        """Test get_repository_status when no repository exists."""
        result = self.loader.get_repository_status()
        assert result == {"is_repository": False}

    @patch("subprocess.run")
    def test_get_repository_status_with_repo(self, mock_subprocess):
        """Test get_repository_status with valid repository."""
        # Create private directory with .git
        private_dir = self.temp_dir / "data" / "input" / "private"
        private_dir.mkdir(parents=True)
        (private_dir / ".git").mkdir()

        # Mock git commands
        def mock_run(cmd, **kwargs):
            result = MagicMock()
            if "rev-parse" in cmd:
                result.stdout = "main\n"
                result.returncode = 0
            elif "remote" in cmd:
                result.stdout = "https://github.com/user/repo.git\n"
                result.returncode = 0
            elif "log" in cmd:
                result.stdout = "abc123 Initial commit (2 hours ago)\n"
                result.returncode = 0
            return result

        mock_subprocess.side_effect = mock_run

        result = self.loader.get_repository_status()

        expected = {
            "is_repository": True,
            "branch": "main",
            "remote": "https://github.com/user/repo.git",
            "last_commit": "abc123 Initial commit (2 hours ago)",
        }
        assert result == expected

    @patch("subprocess.run")
    def test_get_repository_status_git_failure(self, mock_subprocess):
        """Test get_repository_status when git operations fail."""
        # Create private directory with .git
        private_dir = self.temp_dir / "data" / "input" / "private"
        private_dir.mkdir(parents=True)
        (private_dir / ".git").mkdir()

        # Mock git failure
        mock_subprocess.side_effect = FileNotFoundError

        result = self.loader.get_repository_status()

        expected = {"is_repository": True, "error": "Git operations failed"}
        assert result == expected

    def test_get_available_files(self):
        """Test get_available_files method."""
        # Create test data directory with files
        data_dir = self.temp_dir / "data" / "input" / "gotofiles"
        data_dir.mkdir(parents=True)
        (data_dir / "file1.tsv").touch()
        (data_dir / "file2.tsv").touch()
        (data_dir / "other.txt").touch()  # Non-TSV file

        with patch.object(self.loader, "get_data_directory", return_value=data_dir):
            result = self.loader.get_available_files()

            # Should only return TSV files
            assert len(result) == 2
            filenames = [f.name for f in result]
            assert "file1.tsv" in filenames
            assert "file2.tsv" in filenames
            assert "other.txt" not in filenames

    def test_get_data_source_info(self):
        """Test get_data_source_info method."""
        # Create test data directory with files
        data_dir = self.temp_dir / "data" / "input" / "gotofiles"
        data_dir.mkdir(parents=True)
        (data_dir / "file1.tsv").touch()
        (data_dir / "file2.tsv").touch()

        with patch.object(self.loader, "get_data_directory", return_value=data_dir):
            result = self.loader.get_data_source_info()

            assert result["source_type"] == "test_data"
            assert result["directory"] == str(data_dir)
            assert result["files_count"] == 2
            assert len(result["files"]) == 2
            assert result["total_size_mb"] >= 0  # At least some size
            assert result["is_private"] is False

    @patch.dict(os.environ, {"CLAUSEMATE_DATA_SOURCE": "private_local"})
    def test_get_data_source_info_private(self):
        """Test get_data_source_info with private data source."""
        # Create private directory
        private_dir = self.temp_dir / "data" / "input" / "private"
        private_dir.mkdir(parents=True)

        with patch.object(self.loader, "get_data_directory", return_value=private_dir):
            result = self.loader.get_data_source_info()

            assert result["source_type"] == "private_local"
            assert result["is_private"] is True

    def test_ensure_data_available_success(self):
        """Test ensure_data_available with available data."""
        # Create test data directory with files
        data_dir = self.temp_dir / "data" / "input" / "gotofiles"
        data_dir.mkdir(parents=True)
        (data_dir / "test.tsv").touch()

        with patch.object(self.loader, "get_data_directory", return_value=data_dir):
            result = self.loader.ensure_data_available()

            assert result is True

    def test_ensure_data_available_no_files(self):
        """Test ensure_data_available with no files."""
        # Create empty test data directory
        data_dir = self.temp_dir / "data" / "input" / "gotofiles"
        data_dir.mkdir(parents=True)

        with patch.object(self.loader, "get_data_directory", return_value=data_dir):
            result = self.loader.ensure_data_available()

            assert result is False

    def test_ensure_data_available_error(self):
        """Test ensure_data_available with access error."""
        with patch.object(self.loader, "get_data_directory", side_effect=OSError):
            result = self.loader.ensure_data_available()

            assert result is False


class TestSetupDataSourceForMain:
    """Test the setup_data_source_for_main function."""

    @patch("src.utils.data_source_loader.DataSourceLoader")
    def test_setup_data_source_for_main_success(self, mock_loader_class):
        """Test successful setup_data_source_for_main."""
        # Mock loader
        mock_loader = MagicMock()
        mock_loader.ensure_data_available.return_value = True
        mock_loader.get_data_directory.return_value = Path("/test/data")
        mock_loader_class.return_value = mock_loader

        result = setup_data_source_for_main()

        assert result == Path("/test/data")
        mock_loader.ensure_data_available.assert_called_once()
        mock_loader.get_data_directory.assert_called_once()

    @patch("src.utils.data_source_loader.DataSourceLoader")
    @patch("builtins.print")
    def test_setup_data_source_for_main_no_data(self, mock_print, mock_loader_class):
        """Test setup_data_source_for_main with no data available."""
        # Mock loader
        mock_loader = MagicMock()
        mock_loader.ensure_data_available.return_value = False
        mock_loader_class.return_value = mock_loader

        result = setup_data_source_for_main()

        assert result is None
        mock_print.assert_called()


if __name__ == "__main__":
    # Run basic functionality test
    loader = DataSourceLoader()
    info = loader.get_data_source_info()

    print("Data Source Loader Test Results:")
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
        print("\nNo TSV files found!")
