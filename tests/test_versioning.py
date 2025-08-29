"""Tests for versioning.py."""

import json
import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest

from src.data.versioning import (
    DataVersionManager,
    create_processing_config,
    get_version,
)


class TestVersioningFunctions:
    """Test standalone functions in versioning.py."""

    def test_get_version(self):
        """Test get_version function."""
        version = get_version()
        assert isinstance(version, str)
        assert version == "1.0.0"

    def test_create_processing_config(self):
        """Test create_processing_config function."""
        config = create_processing_config()

        assert isinstance(config, dict)
        assert "python_version" in config
        assert "platform" in config
        assert "timestamp" in config
        assert "working_directory" in config

        # Check that values are reasonable
        assert isinstance(config["python_version"], str)
        assert isinstance(config["platform"], str)
        assert isinstance(config["timestamp"], str)
        assert isinstance(config["working_directory"], str)


class TestDataVersionManager:
    """Test the DataVersionManager class."""

    def setup_method(self):
        """Set up test fixtures."""
        self.temp_dir = Path(tempfile.mkdtemp())
        self.manager = DataVersionManager(self.temp_dir)

    def teardown_method(self):
        """Clean up test fixtures."""
        # Remove temp directory and all contents
        import shutil

        shutil.rmtree(self.temp_dir)

    def test_initialization(self):
        """Test DataVersionManager initialization."""
        assert self.manager.data_dir == self.temp_dir
        assert self.manager.metadata_file == self.temp_dir / "metadata.json"

    def test_initialization_default_path(self):
        """Test DataVersionManager initialization with default path."""
        manager = DataVersionManager()
        assert manager.data_dir == Path("data")
        assert manager.metadata_file == Path("data/metadata.json")

    def test_compute_file_hash(self):
        """Test file hash computation."""
        # Create a test file
        test_file = self.temp_dir / "test.txt"
        test_content = b"Hello, World!"
        test_file.write_bytes(test_content)

        hash_value = self.manager.compute_file_hash(test_file)

        assert isinstance(hash_value, str)
        assert len(hash_value) == 64  # SHA-256 hash length

        # Hash should be consistent
        hash_value2 = self.manager.compute_file_hash(test_file)
        assert hash_value == hash_value2

    def test_compute_file_hash_nonexistent_file(self):
        """Test file hash computation for non-existent file."""
        nonexistent_file = self.temp_dir / "nonexistent.txt"

        with pytest.raises(FileNotFoundError):
            self.manager.compute_file_hash(nonexistent_file)

    def test_create_metadata_basic(self):
        """Test basic metadata creation."""
        # Create test files
        input_file = self.temp_dir / "input.txt"
        output_file = self.temp_dir / "output.txt"
        input_file.write_text("input content")
        output_file.write_text("output content")

        processing_config = {"test": "config"}

        metadata = self.manager.create_metadata(
            input_file=input_file,
            output_file=output_file,
            processing_config=processing_config,
            phase="test_phase",
        )

        assert isinstance(metadata, dict)
        assert metadata["phase"] == "test_phase"
        assert metadata["input"]["file"] == str(input_file)
        assert metadata["output"]["file"] == str(output_file)
        assert metadata["processing"] == processing_config
        assert "timestamp" in metadata
        assert "environment" in metadata

    def test_create_metadata_nonexistent_output(self):
        """Test metadata creation when output file doesn't exist."""
        input_file = self.temp_dir / "input.txt"
        output_file = self.temp_dir / "nonexistent_output.txt"
        input_file.write_text("input content")

        processing_config = {"test": "config"}

        metadata = self.manager.create_metadata(
            input_file=input_file,
            output_file=output_file,
            processing_config=processing_config,
        )

        assert metadata["output"]["hash"] is None
        assert metadata["output"]["size_bytes"] is None
        assert "statistics" not in metadata["output"]

    @patch("src.data.versioning.pd.read_csv")
    def test_create_metadata_with_csv_statistics(self, mock_read_csv):
        """Test metadata creation with CSV statistics."""
        # Create test files
        input_file = self.temp_dir / "input.txt"
        output_file = self.temp_dir / "output.csv"
        input_file.write_text("input content")
        output_file.write_text(
            "col1,col2,sentence_id,pronoun_text\n1,2,sent1,er\n3,4,sent2,sie"
        )  # Create actual CSV

        # Mock DataFrame with proper behavior
        from unittest.mock import MagicMock

        mock_df = MagicMock()
        mock_df.__len__ = MagicMock(return_value=2)
        mock_df.columns = ["col1", "col2", "sentence_id", "pronoun_text"]

        # Mock column access using side_effect
        mock_sentence_series = MagicMock()
        mock_sentence_series.nunique.return_value = 2

        mock_pronoun_series = MagicMock()
        mock_pronoun_series.nunique.return_value = 2

        def mock_getitem(key):
            if key == "sentence_id":
                return mock_sentence_series
            elif key == "pronoun_text":
                return mock_pronoun_series
            return mock_df

        mock_df.__getitem__.side_effect = mock_getitem
        mock_read_csv.return_value = mock_df

        processing_config = {"test": "config"}

        metadata = self.manager.create_metadata(
            input_file=input_file,
            output_file=output_file,
            processing_config=processing_config,
        )

        assert "statistics" in metadata["output"]
        stats = metadata["output"]["statistics"]
        assert stats["rows"] == 2
        assert stats["columns"] == 4
        assert stats["unique_sentences"] == 2
        assert stats["unique_pronouns"] == 2

    def test_save_metadata_new_file(self):
        """Test saving metadata to a new file."""
        metadata = {"test": "data", "timestamp": "2023-01-01T00:00:00"}

        self.manager.save_metadata(metadata)

        assert self.manager.metadata_file.exists()

        with open(self.manager.metadata_file) as f:
            saved_data = json.load(f)

        assert len(saved_data) == 1
        assert saved_data[0] == metadata

    def test_save_metadata_existing_file(self):
        """Test saving metadata to an existing file with data."""
        # Create existing metadata
        existing_metadata = [{"existing": "data"}]
        with open(self.manager.metadata_file, "w") as f:
            json.dump(existing_metadata, f)

        new_metadata = {"new": "data", "timestamp": "2023-01-01T00:00:00"}

        self.manager.save_metadata(new_metadata)

        with open(self.manager.metadata_file) as f:
            saved_data = json.load(f)

        assert len(saved_data) == 2
        assert saved_data[0] == existing_metadata[0]
        assert saved_data[1] == new_metadata

    def test_validate_reproducibility_matching(self):
        """Test reproducibility validation with matching hashes."""
        # Create test file
        test_file = self.temp_dir / "test.txt"
        test_file.write_text("test content")

        original_hash = self.manager.compute_file_hash(test_file)

        assert self.manager.validate_reproducibility(original_hash, test_file) is True

    def test_validate_reproducibility_different(self):
        """Test reproducibility validation with different content."""
        # Create test files
        file1 = self.temp_dir / "file1.txt"
        file2 = self.temp_dir / "file2.txt"
        file1.write_text("content 1")
        file2.write_text("content 2")

        hash1 = self.manager.compute_file_hash(file1)

        assert self.manager.validate_reproducibility(hash1, file2) is False

    def test_get_latest_metadata_no_file(self):
        """Test getting latest metadata when no metadata file exists."""
        result = self.manager.get_latest_metadata()
        assert result is None

    def test_get_latest_metadata_empty_file(self):
        """Test getting latest metadata from empty file."""
        with open(self.manager.metadata_file, "w") as f:
            json.dump([], f)

        result = self.manager.get_latest_metadata()
        assert result is None

    def test_get_latest_metadata_with_data(self):
        """Test getting latest metadata from file with data."""
        metadata_list = [
            {"timestamp": "2023-01-01T00:00:00", "phase": "phase1"},
            {"timestamp": "2023-01-02T00:00:00", "phase": "phase2"},
            {"timestamp": "2023-01-03T00:00:00", "phase": "phase1"},
        ]

        with open(self.manager.metadata_file, "w") as f:
            json.dump(metadata_list, f)

        result = self.manager.get_latest_metadata()
        assert result == metadata_list[-1]

    def test_get_latest_metadata_with_phase_filter(self):
        """Test getting latest metadata with phase filter."""
        metadata_list = [
            {"timestamp": "2023-01-01T00:00:00", "phase": "phase1"},
            {"timestamp": "2023-01-02T00:00:00", "phase": "phase2"},
            {"timestamp": "2023-01-03T00:00:00", "phase": "phase1"},
        ]

        with open(self.manager.metadata_file, "w") as f:
            json.dump(metadata_list, f)

        result = self.manager.get_latest_metadata("phase2")
        assert result == metadata_list[1]

    def test_get_latest_metadata_phase_not_found(self):
        """Test getting latest metadata for non-existent phase."""
        metadata_list = [
            {"timestamp": "2023-01-01T00:00:00", "phase": "phase1"},
            {"timestamp": "2023-01-02T00:00:00", "phase": "phase2"},
        ]

        with open(self.manager.metadata_file, "w") as f:
            json.dump(metadata_list, f)

        result = self.manager.get_latest_metadata("nonexistent")
        assert result is None
