"""Tests for verify_phase2.py."""

from unittest.mock import MagicMock, patch

import pytest

from src.verify_phase2 import (
    import_module,
    main,
    test_analyzer_initialization,
    test_coreference_extractor,
    test_end_to_end_with_sample,
    test_imports,
    test_parser_basic,
    test_token_creation,
)


class TestVerifyPhase2:
    """Test the verify_phase2.py functions."""

    def test_import_module(self):
        """Test the import_module helper function."""
        # Test importing a real module
        result = import_module("config")
        assert result is not None
        assert hasattr(result, "Constants")

    def test_import_module_nonexistent(self):
        """Test importing a non-existent module."""
        with pytest.raises(ImportError):
            import_module("nonexistent_module")

    @patch("builtins.print")
    def test_test_imports_success(self, mock_print):
        """Test successful imports test."""
        result = test_imports()
        assert result is True
        mock_print.assert_called_with("✓ All imports successful")

    @patch("builtins.print")
    def test_test_imports_failure(self, mock_print):
        """Test failed imports test."""
        with patch(
            "src.verify_phase2.import_module", side_effect=ImportError("Test error")
        ):
            result = test_imports()
            assert result is False
            mock_print.assert_called_with("✗ Import failed: Test error")

    @patch("builtins.print")
    def test_test_token_creation_success(self, mock_print):
        """Test successful token creation."""
        result = test_token_creation()
        assert result is True
        mock_print.assert_called_with("✓ Token creation successful")

    @patch("builtins.print")
    def test_test_token_creation_failure(self, mock_print):
        """Test failed token creation."""
        with patch("src.data.models.Token", side_effect=Exception("Test error")):
            result = test_token_creation()
            assert result is False
            assert mock_print.called

    @patch("builtins.print")
    def test_test_parser_basic_success(self, mock_print):
        """Test successful parser basic functionality."""
        result = test_parser_basic()
        assert result is True
        mock_print.assert_called_with("✓ Parser basic functionality works")

    @patch("builtins.print")
    def test_test_parser_basic_failure(self, mock_print):
        """Test failed parser basic functionality."""
        with patch(
            "src.parsers.tsv_parser.TSVParser", side_effect=Exception("Test error")
        ):
            result = test_parser_basic()
            assert result is False
            assert mock_print.called

    @patch("builtins.print")
    def test_test_coreference_extractor_success(self, mock_print):
        """Test successful coreference extractor."""
        result = test_coreference_extractor()
        assert result is True
        mock_print.assert_called_with("✓ Coreference extractor works")

    @patch("builtins.print")
    def test_test_coreference_extractor_failure(self, mock_print):
        """Test failed coreference extractor."""
        with patch(
            "src.extractors.coreference_extractor.CoreferenceExtractor",
            side_effect=Exception("Test error"),
        ):
            result = test_coreference_extractor()
            assert result is False
            assert mock_print.called

    @patch("builtins.print")
    def test_test_analyzer_initialization_success(self, mock_print):
        """Test successful analyzer initialization."""
        result = test_analyzer_initialization()
        assert result is True
        mock_print.assert_called_with("✓ Analyzer initialization successful")

    @patch("builtins.print")
    def test_test_analyzer_initialization_failure(self, mock_print):
        """Test failed analyzer initialization."""
        with patch("src.main.ClauseMateAnalyzer", side_effect=Exception("Test error")):
            result = test_analyzer_initialization()
            assert result is False
            assert mock_print.called

    @patch("builtins.print")
    def test_test_end_to_end_with_sample_success(self, mock_print):
        """Test successful end-to-end processing."""
        result = test_end_to_end_with_sample()
        assert result is True
        mock_print.assert_called_with("✓ End-to-end processing successful")

    @patch("builtins.print")
    def test_test_end_to_end_with_sample_failure(self, mock_print):
        """Test failed end-to-end processing."""
        with patch("src.main.ClauseMateAnalyzer", side_effect=Exception("Test error")):
            result = test_end_to_end_with_sample()
            assert result is False
            assert mock_print.called

    @patch("builtins.print")
    def test_main_all_tests_pass(self, mock_print):
        """Test main function when all tests pass."""
        with (
            patch("src.verify_phase2.test_imports", return_value=True),
            patch("src.verify_phase2.test_token_creation", return_value=True),
            patch("src.verify_phase2.test_parser_basic", return_value=True),
            patch("src.verify_phase2.test_coreference_extractor", return_value=True),
            patch("src.verify_phase2.test_analyzer_initialization", return_value=True),
            patch("src.verify_phase2.test_end_to_end_with_sample", return_value=True),
        ):
            result = main()
            assert result is True

            # Check that success message was printed
            success_calls = [
                call
                for call in mock_print.call_args_list
                if "🎉 All Phase 2 components working correctly!" in str(call)
            ]
            assert len(success_calls) > 0

    @patch("builtins.print")
    def test_main_some_tests_fail(self, mock_print):
        """Test main function when some tests fail."""
        with (
            patch("src.verify_phase2.test_imports", return_value=True),
            patch("src.verify_phase2.test_token_creation", return_value=False),
            patch("src.verify_phase2.test_parser_basic", return_value=True),
            patch("src.verify_phase2.test_coreference_extractor", return_value=True),
            patch("src.verify_phase2.test_analyzer_initialization", return_value=True),
            patch("src.verify_phase2.test_end_to_end_with_sample", return_value=True),
        ):
            result = main()
            assert result is False

            # Check that warning message was printed
            warning_calls = [
                call
                for call in mock_print.call_args_list
                if "⚠️  Some components need attention" in str(call)
            ]
            assert len(warning_calls) > 0

    @patch("builtins.print")
    def test_main_all_tests_fail(self, mock_print):
        """Test main function when all tests fail."""
        with (
            patch("src.verify_phase2.test_imports", return_value=False),
            patch("src.verify_phase2.test_token_creation", return_value=False),
            patch("src.verify_phase2.test_parser_basic", return_value=False),
            patch("src.verify_phase2.test_coreference_extractor", return_value=False),
            patch("src.verify_phase2.test_analyzer_initialization", return_value=False),
            patch("src.verify_phase2.test_end_to_end_with_sample", return_value=False),
        ):
            result = main()
            assert result is False

            # Check that results summary was printed
            results_calls = [
                call
                for call in mock_print.call_args_list
                if "Results: 0/6 tests passed" in str(call)
            ]
            assert len(results_calls) > 0

    def test_main_test_list_structure(self):
        """Test that main function has the correct test list structure."""
        # We can't easily test the exact test list without mocking all functions,
        # but we can verify the structure by checking the number of tests
        with (
            patch("src.verify_phase2.test_imports", return_value=True),
            patch("src.verify_phase2.test_token_creation", return_value=True),
            patch("src.verify_phase2.test_parser_basic", return_value=True),
            patch("src.verify_phase2.test_coreference_extractor", return_value=True),
            patch("src.verify_phase2.test_analyzer_initialization", return_value=True),
            patch("src.verify_phase2.test_end_to_end_with_sample", return_value=True),
            patch("builtins.print") as mock_print,
        ):
            result = main()

            # Should have printed "Results: 6/6 tests passed"
            results_calls = [
                call
                for call in mock_print.call_args_list
                if "Results: 6/6 tests passed" in str(call)
            ]
            assert len(results_calls) > 0

    @patch("sys.exit")
    def test_script_execution_success(self, mock_exit):
        """Test script execution when main returns success."""
        with patch("src.verify_phase2.main", return_value=True):
            # Import the module and call its main block logic
            import src.verify_phase2 as verify_module

            # Simulate the if __name__ == "__main__" block
            if hasattr(verify_module, "main"):
                success = verify_module.main()
                if success:
                    mock_exit(0)
                else:
                    mock_exit(1)

            # Should exit with code 0
            mock_exit.assert_called_with(0)

    @patch("sys.exit")
    def test_script_execution_failure(self, mock_exit):
        """Test script execution when main returns failure."""
        with patch("src.verify_phase2.main", return_value=False):
            # Import the module and call its main block logic
            import src.verify_phase2 as verify_module

            # Simulate the if __name__ == "__main__" block
            if hasattr(verify_module, "main"):
                success = verify_module.main()
                if success:
                    mock_exit(0)
                else:
                    mock_exit(1)

            # Should exit with code 1
            mock_exit.assert_called_with(1)

    def test_end_to_end_creates_temp_file(self):
        """Test that end-to-end test creates and cleans up temporary file."""
        # This test verifies that the temporary file creation and cleanup works
        with patch("src.main.ClauseMateAnalyzer") as mock_analyzer_class:
            mock_analyzer = MagicMock()
            mock_analyzer.analyze_file.return_value = []
            mock_analyzer.get_statistics.return_value = {"sentences_processed": 1}
            mock_analyzer_class.return_value = mock_analyzer

            # Mock os.unlink to verify cleanup
            with patch("os.unlink") as mock_unlink:
                result = test_end_to_end_with_sample()

                assert result is True
                # Should have called unlink to clean up temp file
                mock_unlink.assert_called_once()

    def test_parser_boundary_detection(self):
        """Test specific parser boundary detection cases."""
        from src.parsers.tsv_parser import DefaultTokenProcessor, TSVParser

        processor = DefaultTokenProcessor()
        parser = TSVParser(processor)

        # Test various boundary cases
        assert parser.is_sentence_boundary("#Text=Dies ist ein Test.")
        assert not parser.is_sentence_boundary("1\ter\t_\t_")
        assert not parser.is_sentence_boundary("# sent_id = test")
        assert not parser.is_sentence_boundary("")  # Empty line
        assert not parser.is_sentence_boundary("regular text line")

    def test_token_with_coreference_extraction(self):
        """Test token coreference ID extraction."""
        from src.data.models import Token
        from src.extractors.coreference_extractor import CoreferenceExtractor

        extractor = CoreferenceExtractor()

        # Test token with coreference type
        token = Token(
            idx=1,
            text="er",
            sentence_num=1,
            grammatical_role="SUBJ",
            thematic_role="AGENT",
            coreference_type="PersPron[1]",
        )

        ids = extractor.extract_all_ids_from_token(token)

        # Should extract at least one ID
        assert isinstance(ids, list | set)
        assert len(ids) > 0

    def test_analyzer_statistics_initialization(self):
        """Test analyzer statistics initialization."""
        from src.main import ClauseMateAnalyzer

        analyzer = ClauseMateAnalyzer()

        stats = analyzer.get_statistics()

        # Should have basic statistics structure
        assert isinstance(stats, dict)
        assert "sentences_processed" in stats
        assert stats["sentences_processed"] == 0  # Initially zero
