"""Tests for incomplete_format_parser.py."""

import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from src.parsers.incomplete_format_parser import IncompleteFormatParser


class TestIncompleteFormatParser:
    """Test the IncompleteFormatParser class."""

    def setup_method(self):
        """Set up test fixtures."""
        self.processor = MagicMock()
        self.parser = IncompleteFormatParser(self.processor)

    def test_initialization(self):
        """Test that the parser initializes correctly."""
        assert self.parser.limitations == []
        assert self.parser.available_features["basic_tokens"] is True
        assert self.parser.available_features["coreference"] is False
        assert hasattr(self.parser, "logger")

    def test_initialization_with_limitations(self):
        """Test initialization with custom limitations."""
        limitations = ["Test limitation"]
        parser = IncompleteFormatParser(self.processor, limitations)
        assert parser.limitations == limitations

    @patch("src.parsers.incomplete_format_parser.PreambleParser")
    @patch("src.parsers.incomplete_format_parser.extract_preamble_from_file")
    def test_setup_column_mapping_with_preamble(
        self, mock_extract, mock_preamble_parser
    ):
        """Test column mapping setup with preamble."""
        # Mock preamble parser
        mock_parser_instance = MagicMock()
        mock_preamble_parser.return_value = mock_parser_instance

        # Mock schema
        mock_schema = MagicMock()
        mock_parser_instance.parse_preamble_lines.return_value = mock_schema

        # Mock extract function
        mock_extract.return_value = ["# preamble line"]

        with tempfile.NamedTemporaryFile(mode="w", suffix=".tsv", delete=False) as f:
            f.write("test data")
            temp_file = f.name

        try:
            self.parser._setup_column_mapping_for_incomplete(temp_file)

            mock_extract.assert_called_once_with(temp_file)
            mock_parser_instance.parse_preamble_lines.assert_called_once_with(
                ["# preamble line"]
            )
            assert self.parser.current_annotation_schema == mock_schema

        finally:
            Path(temp_file).unlink()

    def test_setup_column_mapping_without_preamble(self):
        """Test column mapping setup without preamble (fallback)."""
        # Create a temporary file with 12 columns
        with tempfile.NamedTemporaryFile(mode="w", suffix=".tsv", delete=False) as f:
            f.write("1-1\t0-4\tKarl\tKarl\tNOUN\t_\t2\tamod\t_\t_\t_\t_\n")
            temp_file = f.name

        try:
            self.parser._setup_column_mapping_for_incomplete(temp_file)

            # Should detect 12 columns and set up 12-column mapping
            assert self.parser.column_mapping["token_id"] == 0
            assert self.parser.column_mapping["token_text"] == 2
            assert self.parser.available_features["coreference"] is True

        finally:
            Path(temp_file).unlink()

    def test_setup_12_column_mapping(self):
        """Test 12-column mapping setup."""
        self.parser._setup_12_column_mapping()

        expected_mapping = {
            "token_id": 0,
            "token_span": 1,
            "token_text": 2,
            "lemma": 3,
            "pos_tag": 4,
            "morph_features": 5,
            "dependency_head": 6,
            "dependency_rel": 7,
            "coreference_link": 8,
            "coreference_type": 9,
            "additional_1": 10,
            "additional_2": 11,
        }

        assert self.parser.column_mapping == expected_mapping
        assert self.parser.available_features["coreference"] is True

    def test_setup_13_column_mapping(self):
        """Test 13-column mapping setup."""
        self.parser._setup_13_column_mapping()

        expected_mapping = {
            "token_id": 0,
            "token_span": 1,
            "token_text": 2,
            "lemma": 3,
            "pos_tag": 4,
            "morph_features": 5,
            "dependency_head": 6,
            "dependency_rel": 7,
            "additional_1": 8,
            "coreference_link": 9,
            "coreference_type": 10,
            "additional_2": 11,
            "additional_3": 12,
        }

        assert self.parser.column_mapping == expected_mapping
        assert self.parser.available_features["coreference"] is True

    def test_setup_minimal_column_mapping(self):
        """Test minimal column mapping setup."""
        self.parser._setup_minimal_column_mapping()

        expected_mapping = {
            "token_id": 0,
            "token_span": 1,
            "token_text": 2,
            "lemma": 3,
            "pos_tag": 4,
        }

        assert self.parser.column_mapping == expected_mapping
        assert self.parser.available_features["coreference"] is False
        assert self.parser.available_features["morphological"] is False

    def test_detect_available_features_from_schema(self):
        """Test feature detection from schema."""
        # Mock column mapping with coreference
        self.parser.current_column_mapping = MagicMock()
        self.parser.current_column_mapping.coreference_link = 8
        self.parser.current_column_mapping.coreference_type = 9

        # Mock schema with morphological features
        mock_schema = MagicMock()
        mock_span_ann = MagicMock()
        mock_span_ann.get.return_value = "MorphologicalFeatures"
        mock_schema.span_annotations = [mock_span_ann]

        self.parser.current_annotation_schema = mock_schema

        self.parser._detect_available_features_from_schema()

        assert self.parser.available_features["coreference"] is True
        assert self.parser.available_features["morphological"] is True

    def test_extract_first_words(self):
        """Test first words extraction from sentence boundary."""
        # Test normal case
        line = "#Text=Karl sagte etwas Wichtiges."
        result = self.parser._extract_first_words(line)
        assert result == "Karl_sagte_etwas"

        # Test empty line
        result = self.parser._extract_first_words("")
        assert result == ""

        # Test line without #Text=
        result = self.parser._extract_first_words("regular line")
        assert result == ""

    def test_create_token_from_row_basic(self):
        """Test token creation from basic row."""
        # Set up column mapping
        self.parser.column_mapping = {
            "token_id": 0,
            "token_text": 2,
            "lemma": 3,
            "pos_tag": 4,
        }

        row = ["1-1", "0-4", "Karl", "Karl", "NOUN"]

        # Mock processor validation
        self.processor.validate_token.return_value = True

        result = self.parser._create_token_from_row(row, "1")

        assert result is not None
        assert result.idx == 1
        assert result.text == "Karl"
        assert result.sentence_num == 1
        assert result.grammatical_role == "NOUN"

    def test_create_token_from_row_with_coreference(self):
        """Test token creation with coreference information."""
        # Set up column mapping with coreference
        self.parser.column_mapping = {
            "token_id": 0,
            "token_text": 2,
            "coreference_link": 8,
            "coreference_type": 9,
        }
        self.parser.available_features["coreference"] = True

        row = ["1-1", "0-4", "er", "_", "_", "_", "_", "_", "*->140-1", "PersPron[1]"]

        # Mock processor validation
        self.processor.validate_token.return_value = True

        result = self.parser._create_token_from_row(row, "1")

        assert result is not None
        assert result.coreference_link == "*->140-1"
        assert result.coreference_type == "PersPron[1]"

    def test_create_token_from_row_short_row(self):
        """Test token creation with too few columns."""
        self.parser.column_mapping = {"token_id": 0, "token_text": 2}
        row = ["1-1", "0-4"]  # Only 2 columns, need at least 3

        result = self.parser._create_token_from_row(row, "1")

        assert result is None

    def test_create_token_from_row_invalid_token_id(self):
        """Test token creation with invalid token ID."""
        self.parser.column_mapping = {"token_id": 0, "token_text": 2}
        row = ["invalid", "0-4", "Karl"]

        result = self.parser._create_token_from_row(row, "1")

        assert result is None  # Should fail due to invalid token ID

    def test_get_limitations(self):
        """Test limitations retrieval."""
        # Test with all features available
        self.parser.available_features = {
            "coreference": True,
            "morphological": True,
        }

        result = self.parser.get_limitations()
        assert result == []

        # Test with missing features
        self.parser.available_features = {
            "coreference": False,
            "morphological": False,
        }

        result = self.parser.get_limitations()
        assert len(result) == 2
        assert "No coreference analysis available" in result
        assert "Limited morphological features" in result

    def test_get_compatibility_info(self):
        """Test compatibility info retrieval."""
        self.parser.column_mapping = {"token_id": 0, "token_text": 2}
        # Ensure morphological key exists (it should already be initialized)
        assert "morphological" in self.parser.available_features

        result = self.parser.get_compatibility_info()

        assert result["format_type"] == "incomplete"
        assert result["available_features"]["basic_tokens"] is True
        assert result["available_features"]["coreference"] is False
        assert "morphological" in result["available_features"]
        assert len(result["limitations"]) >= 1
        assert "column_mapping" in result
        assert "recommended_actions" in result

    @patch("src.parsers.incomplete_format_parser.open")
    def test_parse_sentence_streaming_basic(self, mock_open):
        """Test basic sentence streaming parsing."""
        # Mock file content
        mock_file = MagicMock()
        mock_file.__enter__.return_value = mock_file
        mock_file.__iter__.return_value = iter(
            [
                "#Text=Karl sagte etwas.",
                "1-1\t0-4\tKarl\tKarl\tNOUN\t_\t2\tamod\t_\t_\t_\t_",
                "1-2\t4-9\tsagte\tsagen\tVERB\t_\t0\troot\t_\t_\t_\t_",
                "",  # Empty line
                "#Text=Das war wichtig.",
                "2-1\t0-3\tDas\tder\tPRON\t_\t3\tnsubj\t_\t_\t_\t_",
            ]
        )
        mock_open.return_value = mock_file

        # Mock processor
        self.processor.validate_token.return_value = True

        # Mock sentence context creation
        with patch.object(self.parser, "_create_sentence_context") as mock_create:
            mock_context = MagicMock()
            mock_create.return_value = mock_context

            # Set up column mapping
            self.parser.column_mapping = {
                "token_id": 0,
                "token_text": 2,
                "lemma": 3,
                "pos_tag": 4,
            }

            sentences = list(self.parser._parse_incomplete_format_streaming("test.tsv"))

            assert len(sentences) == 2
            assert mock_create.call_count == 2

    def test_parse_sentence_streaming_file_not_found(self):
        """Test parsing with file not found error."""
        with (
            patch(
                "src.parsers.incomplete_format_parser.open",
                side_effect=FileNotFoundError,
            ),
            pytest.raises(FileNotFoundError),
        ):
            list(self.parser._parse_incomplete_format_streaming("nonexistent.tsv"))

    def test_parse_sentence_streaming_permission_error(self):
        """Test parsing with permission error."""
        with (
            patch(
                "src.parsers.incomplete_format_parser.open", side_effect=PermissionError
            ),
            pytest.raises(PermissionError),
        ):
            list(self.parser._parse_incomplete_format_streaming("protected.tsv"))

    @patch("src.parsers.incomplete_format_parser.SentenceContext")
    def test_create_sentence_context(self, mock_sentence_context):
        """Test sentence context creation."""
        # This would normally be inherited from parent class
        # but we can test the concept
        tokens = [MagicMock()]
        mock_context = MagicMock()
        mock_sentence_context.return_value = mock_context

        # The actual _create_sentence_context method would be in the parent class
        # but we can verify the concept works
        result = self.parser._create_sentence_context(
            sentence_id="1", sentence_num=1, tokens=tokens, first_words="Karl_sagte"
        )

        # In practice, this method would be implemented in the parent class
        # but our test shows the interface works
        assert result is not None
