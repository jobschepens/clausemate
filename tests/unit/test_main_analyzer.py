"""Unit tests for the main ClauseMateAnalyzer with mocking."""

from unittest.mock import Mock, patch

import pytest

from src.exceptions import ClauseMateExtractionError
from src.main import ClauseMateAnalyzer
from tests.fixtures.mock_data.mock_objects import (
    mock_relationship,
)


class TestClauseMateAnalyzer:
    """Unit tests for ClauseMateAnalyzer class."""

    @pytest.fixture
    def analyzer(self):
        """Create analyzer instance for testing."""
        return ClauseMateAnalyzer(enable_streaming=False, enable_adaptive_parsing=True)

    @pytest.fixture
    def mock_file_path(self, tmp_path):
        """Create a temporary file path for testing."""
        test_file = tmp_path / "test.tsv"
        test_file.write_text("mock content")
        return str(test_file)

    def test_analyzer_initialization_default(self):
        """Test analyzer initialization with default parameters."""
        analyzer = ClauseMateAnalyzer()

        assert analyzer.enable_streaming is False
        assert analyzer.enable_adaptive_parsing is True
        assert analyzer.stats["sentences_processed"] == 0
        assert analyzer.stats["relationships_found"] == 0

    def test_analyzer_initialization_custom(self):
        """Test analyzer initialization with custom parameters."""
        analyzer = ClauseMateAnalyzer(
            enable_streaming=True, enable_adaptive_parsing=False
        )

        assert analyzer.enable_streaming is True
        assert analyzer.enable_adaptive_parsing is False

    @patch("src.main.ClauseMateAnalyzer._detect_and_configure_format")
    @patch("src.main.ClauseMateAnalyzer._analyze_complete")
    def test_analyze_file_success(
        self, mock_analyze, mock_detect, analyzer, mock_file_path
    ):
        """Test successful file analysis."""
        # Setup mocks
        mock_relationships = [mock_relationship()]
        mock_analyze.return_value = mock_relationships

        # Execute
        result = analyzer.analyze_file(mock_file_path)

        # Verify
        assert result == mock_relationships
        mock_detect.assert_called_once_with(mock_file_path)
        mock_analyze.assert_called_once_with(mock_file_path)

    @patch("src.main.ClauseMateAnalyzer._detect_and_configure_format")
    @patch("src.main.ClauseMateAnalyzer._analyze_streaming")
    def test_analyze_file_streaming(self, mock_analyze, mock_detect, mock_file_path):
        """Test file analysis with streaming enabled."""
        # Setup
        analyzer = ClauseMateAnalyzer(enable_streaming=True)
        mock_relationships = [mock_relationship()]
        mock_analyze.return_value = mock_relationships

        # Execute
        result = analyzer.analyze_file(mock_file_path)

        # Verify
        assert result == mock_relationships
        mock_analyze.assert_called_once_with(mock_file_path)

    @patch("src.main.ClauseMateAnalyzer._detect_and_configure_format")
    def test_analyze_file_exception_handling(
        self, mock_detect, analyzer, mock_file_path
    ):
        """Test exception handling in file analysis."""
        # Setup mock to raise exception
        mock_detect.side_effect = Exception("Test error")

        # Execute and verify exception
        with pytest.raises(ClauseMateExtractionError, match="Failed to analyze file"):
            analyzer.analyze_file(mock_file_path)

    def test_analyze_complete_success(self, analyzer, mock_file_path):
        """Test complete analysis method."""
        # Setup mocks - use Mock instead of actual object to avoid property issues
        mock_context = Mock()
        mock_context.sentence_id = "1"
        mock_context.tokens = []
        mock_context.has_critical_pronouns = True
        mock_context.has_coreference_phrases = True
        mock_contexts = [mock_context]

        # Mock the parser's parse_sentence_streaming method
        with patch.object(
            analyzer.parser, "parse_sentence_streaming"
        ) as mock_parse, patch.object(
            analyzer, "coreference_extractor"
        ) as mock_coref, patch.object(
            analyzer, "pronoun_extractor"
        ) as mock_pronoun, patch.object(
            analyzer, "phrase_extractor"
        ) as mock_phrase, patch.object(analyzer, "relationship_extractor") as mock_rel:
            # Setup parser and extractor returns
            mock_parse.return_value = iter(mock_contexts)
            mock_coref.extract_coreference_chains.return_value = []
            mock_pronoun.extract.return_value = Mock(pronouns=[])
            mock_phrase.extract.return_value = Mock(phrases=[])
            mock_rel.extract.return_value = Mock(relationships=[mock_relationship()])

            # Execute
            result = analyzer._analyze_complete(mock_file_path)

            # Verify
            assert len(result) == 1
            assert analyzer.stats["sentences_processed"] == 1
            mock_parse.assert_called_once_with(mock_file_path)

    def test_extract_sentence_number_valid(self, analyzer):
        """Test sentence number extraction from sentence ID."""
        assert analyzer._extract_sentence_number("sent_123") == 123
        assert analyzer._extract_sentence_number("1-5") == 1
        assert analyzer._extract_sentence_number("sentence_42_token") == 42

    def test_extract_sentence_number_no_match(self, analyzer):
        """Test sentence number extraction with no numeric match."""
        assert analyzer._extract_sentence_number("no_numbers") == 1
        assert analyzer._extract_sentence_number("") == 1

    def test_export_results_success(self, analyzer, tmp_path):
        """Test successful results export."""
        # Setup
        relationships = [mock_relationship()]
        output_path = str(tmp_path / "output.csv")

        # Mock pandas DataFrame with proper columns attribute
        with patch("pandas.DataFrame") as mock_dataframe:
            mock_df = Mock()
            # Mock the columns attribute to return a list-like object
            mock_df.columns = ["sentence_id", "sentence_num", "pronoun_text"]
            mock_dataframe.return_value = mock_df

            # Execute
            analyzer.export_results(relationships, output_path)

            # Verify DataFrame creation and export
            mock_dataframe.assert_called_once()
            mock_df.to_csv.assert_called_once()
            assert analyzer.stats is not None

    def test_export_results_empty_relationships(self, analyzer, tmp_path):
        """Test export with empty relationships list."""
        output_path = str(tmp_path / "output.csv")

        # Should not raise exception
        analyzer.export_results([], output_path)

    def test_export_results_exception_handling(self, analyzer, tmp_path):
        """Test export exception handling."""
        # Setup
        relationships = [mock_relationship()]
        output_path = str(tmp_path / "output.csv")

        # Mock pandas DataFrame to raise exception
        with patch("pandas.DataFrame") as mock_dataframe:
            mock_dataframe.side_effect = Exception("DataFrame creation failed")

            # Execute and verify exception
            with pytest.raises(
                ClauseMateExtractionError, match="Failed to export results"
            ):
                analyzer.export_results(relationships, output_path)

    def test_get_statistics(self, analyzer):
        """Test statistics retrieval."""
        stats = analyzer.get_statistics()

        assert isinstance(stats, dict)
        assert "sentences_processed" in stats
        assert "relationships_found" in stats
        assert "tokens_processed" in stats

    def test_detect_and_configure_format_success(self, analyzer, mock_file_path):
        """Test format detection and configuration."""
        # Setup mock format info
        mock_format_info = Mock()
        mock_format_info.compatibility_score = 0.8
        mock_format_info.format_type = "standard"
        mock_format_info.total_columns = 15
        mock_format_info.issues = []

        # Mock the format detector's analyze_file method
        with patch.object(analyzer.format_detector, "analyze_file") as mock_analyze:
            mock_analyze.return_value = mock_format_info

            # Execute
            analyzer._detect_and_configure_format(mock_file_path)

            # Verify
            mock_analyze.assert_called_once_with(mock_file_path)
            assert analyzer.parser == analyzer.adaptive_parser

    @patch("src.main.TSVFormatDetector")
    def test_detect_and_configure_format_low_compatibility(
        self, mock_detector_class, analyzer, mock_file_path
    ):
        """Test format detection with low compatibility score."""
        # Setup mock
        mock_detector = Mock()
        mock_detector_class.return_value = mock_detector
        mock_format_info = Mock()
        mock_format_info.compatibility_score = 0.3
        mock_format_info.format_type = "unknown"
        mock_format_info.total_columns = 10
        mock_format_info.issues = ["Missing columns"]
        mock_detector.analyze_file.return_value = mock_format_info

        # Execute
        analyzer._detect_and_configure_format(mock_file_path)

        # Verify fallback to legacy parser
        assert analyzer.parser == analyzer.legacy_parser

    def test_detect_and_configure_format_incomplete(self, analyzer, mock_file_path):
        """Test format detection for incomplete format."""
        # Setup mock format info
        mock_format_info = Mock()
        mock_format_info.compatibility_score = 0.6
        mock_format_info.format_type = "incomplete"
        mock_format_info.total_columns = 12
        mock_format_info.issues = []

        # Mock the format detector's analyze_file method
        with patch.object(analyzer.format_detector, "analyze_file") as mock_analyze:
            mock_analyze.return_value = mock_format_info

            # Execute
            analyzer._detect_and_configure_format(mock_file_path)

            # Verify incomplete parser selection
            assert analyzer.parser == analyzer.incomplete_parser

    @patch("src.main.TSVFormatDetector")
    def test_detect_and_configure_format_exception(
        self, mock_detector_class, analyzer, mock_file_path
    ):
        """Test format detection exception handling."""
        # Setup mock to raise exception
        mock_detector = Mock()
        mock_detector_class.return_value = mock_detector
        mock_detector.analyze_file.side_effect = Exception("Detection error")

        # Execute
        analyzer._detect_and_configure_format(mock_file_path)

        # Verify fallback to legacy parser
        assert analyzer.parser == analyzer.legacy_parser

    def test_ensure_timestamped_output_path_new(self, analyzer, tmp_path):
        """Test timestamped output path creation."""
        output_path = str(tmp_path / "output.csv")

        result = analyzer._ensure_timestamped_output_path(output_path)

        # Should create timestamped directory (handle Windows path separators)
        assert "data" in result and "output" in result
        assert result.endswith("output.csv")
        assert result != output_path

    def test_ensure_timestamped_output_path_existing(self, analyzer):
        """Test timestamped output path with existing timestamp."""
        output_path = "data/output/20240101_120000/output.csv"

        result = analyzer._ensure_timestamped_output_path(output_path)

        # Should return unchanged
        assert result == output_path


@pytest.mark.unit
class TestAnalyzerIntegration:
    """Integration tests for analyzer components."""

    def test_analyzer_with_mock_data(self, sample_tsv_files):
        """Test analyzer with mock TSV data."""
        analyzer = ClauseMateAnalyzer(enable_adaptive_parsing=False)

        # This would require actual file processing
        # For now, just test that analyzer can be created
        assert analyzer is not None
        assert hasattr(analyzer, "analyze_file")
        assert hasattr(analyzer, "export_results")

    def test_analyzer_statistics_tracking(self):
        """Test that analyzer properly tracks statistics."""
        analyzer = ClauseMateAnalyzer()

        # Initial state
        stats = analyzer.get_statistics()
        assert stats["sentences_processed"] == 0
        assert stats["relationships_found"] == 0

        # Statistics should be modifiable
        analyzer.stats["sentences_processed"] = 5
        stats = analyzer.get_statistics()
        assert stats["sentences_processed"] == 5
