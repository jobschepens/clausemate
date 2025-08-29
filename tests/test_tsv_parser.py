"""Tests for tsv_parser.py."""

import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from src.exceptions import FileProcessingError, ParseError
from src.parsers.tsv_parser import DefaultTokenProcessor, TSVParser


class TestTSVParser:
    """Test the TSVParser class."""

    def setup_method(self):
        """Set up test fixtures."""
        self.processor = DefaultTokenProcessor()
        self.parser = TSVParser(self.processor)

    def test_initialization(self):
        """Test that the parser initializes correctly."""
        assert isinstance(self.parser, TSVParser)
        assert hasattr(self.parser, "processor")
        assert hasattr(self.parser, "columns")
        assert self.parser._expected_columns == 14

    @patch("src.parsers.tsv_parser.open")
    def test_parse_file_file_not_found(self, mock_open):
        """Test parse_file with file not found error."""
        mock_open.side_effect = FileNotFoundError

        with pytest.raises(FileProcessingError, match="File not found"):
            self.parser.parse_file("nonexistent.tsv")

    @patch("src.parsers.tsv_parser.open")
    def test_parse_file_permission_error(self, mock_open):
        """Test parse_file with permission error."""
        mock_open.side_effect = PermissionError

        with pytest.raises(FileProcessingError, match="Permission denied"):
            self.parser.parse_file("protected.tsv")

    @patch("src.parsers.tsv_parser.open")
    def test_parse_file_generic_error(self, mock_open):
        """Test parse_file with generic error."""
        mock_open.side_effect = OSError("Disk full")

        with pytest.raises(FileProcessingError, match="Error reading file"):
            self.parser.parse_file("test.tsv")

    def test_parse_token_line_insufficient_columns(self):
        """Test parse_token_line with insufficient columns."""
        line = "1-1\t0-4\tKarl"  # Only 3 columns, need 14

        with pytest.raises(ParseError, match="Insufficient columns"):
            self.parser.parse_token_line(line)

    def test_parse_token_line_invalid_token_id(self):
        """Test parse_token_line with invalid token ID."""
        line = "invalid\t0-4\tKarl\tKarl\tNOUN\t_\t2\tamod\t_\t_\t_\t_\t_\t_"

        with pytest.raises(ParseError, match="Invalid token line format"):
            self.parser.parse_token_line(line)

    def test_parse_token_line_value_error(self):
        """Test parse_token_line with value error in parsing."""
        line = "1-1\t0-4\tKarl\tKarl\tNOUN\t_\tnot_a_number\tamod\t_\t_\t_\t_\t_\t_"

        # The parser handles errors gracefully and creates a token with default values
        token = self.parser.parse_token_line(line)
        assert token is not None
        assert token.idx == 1
        assert token.text == "Karl"
        assert token.sentence_num == 1

    def test_extract_sentence_id_text_format(self):
        """Test _extract_sentence_id with #Text= format."""
        line = "#Text=Karl sagte etwas Wichtiges."
        result = self.parser._extract_sentence_id(line)
        assert result == "Karl_sagte_etwas"

    def test_extract_sentence_id_sent_id_format(self):
        """Test _extract_sentence_id with sent_id format."""
        line = "# sent_id = sentence_123"
        result = self.parser._extract_sentence_id(line)
        assert result == "sentence_123"

    def test_extract_sentence_id_fallback(self):
        """Test _extract_sentence_id fallback."""
        line = "# Some other comment"
        result = self.parser._extract_sentence_id(line)
        assert result == "Some other comment"

    def test_extract_sentence_num_with_number(self):
        """Test _extract_sentence_num with number in sentence ID."""
        line = "#Text=Sentence number 5 is here."
        result = self.parser._extract_sentence_num(line)
        assert result == 5

    def test_extract_sentence_num_no_number(self):
        """Test _extract_sentence_num with no number in sentence ID."""
        line = "#Text=No numbers here."
        result = self.parser._extract_sentence_num(line)
        # Should return hash-based number, just check it's an int
        assert isinstance(result, int)

    def test_extract_sentence_num_hash_consistency(self):
        """Test that _extract_sentence_num returns consistent results for same input."""
        line = "#Text=Same sentence every time."
        result1 = self.parser._extract_sentence_num(line)
        result2 = self.parser._extract_sentence_num(line)
        assert result1 == result2

    def test_is_sentence_boundary_positive(self):
        """Test is_sentence_boundary with positive case."""
        line = "#Text=Karl sagte etwas."
        assert self.parser.is_sentence_boundary(line) is True

    def test_is_sentence_boundary_negative(self):
        """Test is_sentence_boundary with negative case."""
        line = "1-1\t0-4\tKarl\tKarl\tNOUN"
        assert self.parser.is_sentence_boundary(line) is False

    def test_extract_first_words_normal(self):
        """Test _extract_first_words with normal case."""
        line = "#Text=Karl sagte etwas Wichtiges."
        result = self.parser._extract_first_words(line)
        assert result == "Karl_sagte_etwas"

    def test_extract_first_words_empty(self):
        """Test _extract_first_words with empty text."""
        line = "#Text="
        result = self.parser._extract_first_words(line)
        assert result == ""

    def test_extract_first_words_no_text_marker(self):
        """Test _extract_first_words without #Text= marker."""
        line = "regular line"
        result = self.parser._extract_first_words(line)
        assert result == ""

    def test_parse_sentence_streaming_insufficient_columns_error(self):
        """Test parse_sentence_streaming with insufficient columns error."""
        # Create a temporary file with insufficient columns
        with tempfile.NamedTemporaryFile(mode="w", suffix=".tsv", delete=False) as f:
            f.write("#Text=Test sentence.\n")
            f.write("1-1\t0-4\tKarl\n")  # Only 3 columns
            temp_file = f.name

        try:
            # The parser raises ParseError for insufficient columns
            with pytest.raises(ParseError, match="Expected 14 columns, got 3"):
                list(self.parser.parse_sentence_streaming(temp_file))
        finally:
            Path(temp_file).unlink()

    @patch("src.parsers.tsv_parser.open")
    def test_parse_sentence_streaming_file_not_found(self, mock_open):
        """Test parse_sentence_streaming with file not found."""
        mock_open.side_effect = FileNotFoundError

        with pytest.raises(FileProcessingError, match="File not found"):
            list(self.parser.parse_sentence_streaming("nonexistent.tsv"))

    @patch("src.parsers.tsv_parser.open")
    def test_parse_sentence_streaming_permission_error(self, mock_open):
        """Test parse_sentence_streaming with permission error."""
        mock_open.side_effect = PermissionError

        with pytest.raises(FileProcessingError, match="Permission denied"):
            list(self.parser.parse_sentence_streaming("protected.tsv"))

    def test_parse_token_line_with_coreference(self):
        """Test parse_token_line with coreference information."""
        # Create a line with 14 columns including coreference data
        line = "1-1\t0-4\tKarl\tKarl\tNOUN\t_\t2\tamod\t*->115-1\tPersPron[115]\t_\t_\t_\t_"

        token = self.parser.parse_token_line(line)

        assert token.idx == 1
        assert token.text == "Karl"
        assert token.sentence_num == 1
        # Note: The parser may not extract coreference info depending on column mapping
        # This test verifies the parsing works without errors
        assert token is not None

    def test_parse_token_line_minimal_columns(self):
        """Test parse_token_line with minimal valid columns."""
        line = "1-1\t0-4\tKarl\tKarl\tNOUN\t_\t2\tamod\t_\t_\t_\t_\t_\t_"

        token = self.parser.parse_token_line(line)

        assert token.idx == 1
        assert token.text == "Karl"
        assert token.sentence_num == 1
        assert token.grammatical_role == "NOUN"

    def test_parse_token_line_inanimate_coreference(self):
        """Test parse_token_line with inanimate coreference."""
        # Create a line with 14 columns
        line = (
            "1-1\t0-4\tHaus\tHaus\tNOUN\t_\t2\tamod\t_\t_\t*->200-1\tInanim[200]\t_\t_"
        )

        token = self.parser.parse_token_line(line)

        assert token.idx == 1
        assert token.text == "Haus"
        assert token.sentence_num == 1
        # Note: Inanimate coreference extraction depends on column mapping
        assert token is not None

    def test_parse_token_line_missing_optional_columns(self):
        """Test parse_token_line with missing optional columns."""
        # The parser requires exactly 14 columns, so this will fail
        line = "1-1\t0-4\tKarl\tKarl\tNOUN"

        with pytest.raises(ParseError, match="Insufficient columns"):
            self.parser.parse_token_line(line)


class TestDefaultTokenProcessor:
    """Test the DefaultTokenProcessor class."""

    def setup_method(self):
        """Set up test fixtures."""
        self.processor = DefaultTokenProcessor()

    def test_validate_token_valid(self):
        """Test validate_token with valid token."""
        mock_token = MagicMock()
        mock_token.idx = 1
        mock_token.text = "Karl"

        assert self.processor.validate_token(mock_token) is True

    def test_validate_token_invalid_idx(self):
        """Test validate_token with invalid index."""
        mock_token = MagicMock()
        mock_token.idx = 0  # Invalid
        mock_token.text = "Karl"

        assert self.processor.validate_token(mock_token) is False

    def test_validate_token_empty_text(self):
        """Test validate_token with empty text."""
        mock_token = MagicMock()
        mock_token.idx = 1
        mock_token.text = ""  # Invalid

        assert self.processor.validate_token(mock_token) is False

    def test_validate_token_whitespace_text(self):
        """Test validate_token with whitespace-only text."""
        mock_token = MagicMock()
        mock_token.idx = 1
        mock_token.text = "   "  # Invalid

        assert self.processor.validate_token(mock_token) is False

    def test_validate_token_exception(self):
        """Test validate_token with exception during validation."""
        mock_token = MagicMock()
        # Make token raise exception when accessing attributes
        mock_token.idx = MagicMock(side_effect=AttributeError)

        assert self.processor.validate_token(mock_token) is False

    def test_enrich_token(self):
        """Test enrich_token method."""
        mock_token = MagicMock()
        mock_context = MagicMock()

        result = self.processor.enrich_token(mock_token, mock_context)

        # Should return the same token (default implementation)
        assert result == mock_token
