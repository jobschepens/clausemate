"""Integration tests for TSV format processing with proper pytest structure."""

import time
from pathlib import Path

import pytest

from src.exceptions import ClauseMateExtractionError
from src.main import ClauseMateAnalyzer


@pytest.mark.integration
class TestFormatProcessing:
    """Integration tests for different TSV format processing."""

    @pytest.fixture(scope="class")
    def analyzer(self):
        """Create analyzer instance for integration tests."""
        return ClauseMateAnalyzer(enable_adaptive_parsing=True, enable_streaming=False)

    def test_format_detection_and_processing(self, analyzer, format_test_data):
        """Test format detection and processing for all supported formats."""
        format_type = format_test_data["format"]
        file_path = format_test_data["file_path"]
        expected_columns = format_test_data["expected_columns"]

        # Skip if file doesn't exist (for mock testing)
        if not Path(file_path).exists():
            pytest.skip(f"Test file {file_path} not found")

        # Test format detection
        analyzer._detect_and_configure_format(str(file_path))

        # Verify correct parser selection based on format
        if format_type == "standard":
            assert analyzer.parser == analyzer.adaptive_parser
        elif format_type == "incomplete":
            # Incomplete format may use adaptive parser if compatibility is high enough
            assert analyzer.parser in [
                analyzer.adaptive_parser,
                analyzer.incomplete_parser,
            ]
        elif format_type == "legacy":
            # Could be adaptive or legacy depending on compatibility
            assert analyzer.parser in [analyzer.adaptive_parser, analyzer.legacy_parser]

    @pytest.mark.slow
    def test_end_to_end_processing(self, analyzer, sample_tsv_files):
        """Test complete end-to-end processing for each format."""
        results = {}

        for format_name, file_path in sample_tsv_files.items():
            if not Path(file_path).exists():
                continue

            start_time = time.time()

            try:
                relationships = analyzer.analyze_file(str(file_path))
                processing_time = time.time() - start_time

                results[format_name] = {
                    "success": True,
                    "relationships_count": len(relationships),
                    "processing_time": processing_time,
                    "error": None,
                }

                # Basic validation
                assert isinstance(relationships, list)
                if relationships:
                    # Validate first relationship structure
                    rel = relationships[0]
                    assert hasattr(rel, "sentence_num")
                    assert hasattr(rel, "pronoun")
                    assert hasattr(rel, "clause_mate")
                    assert rel.sentence_num > 0

            except Exception as e:
                results[format_name] = {
                    "success": False,
                    "relationships_count": 0,
                    "processing_time": time.time() - start_time,
                    "error": str(e),
                }

        # Verify at least one format processed successfully
        successful_formats = [
            name for name, result in results.items() if result["success"]
        ]
        assert len(successful_formats) > 0, (
            f"No formats processed successfully: {results}"
        )

    def test_adaptive_parsing_fallback(self, analyzer, tmp_path):
        """Test adaptive parsing fallback mechanism."""
        # Create a malformed TSV file
        malformed_file = tmp_path / "malformed.tsv"
        malformed_file.write_text("""
#FORMAT=WebAnno TSV 3.6.1

#Text=Invalid format test
1-1	invalid	data	structure
""")

        # Should not crash, should fallback gracefully
        try:
            relationships = analyzer.analyze_file(str(malformed_file))
            # May return empty list or raise controlled exception
            assert isinstance(relationships, list)
        except ClauseMateExtractionError:
            # Controlled exception is acceptable
            pass

    def test_statistics_tracking(self, analyzer, sample_tsv_files):
        """Test that statistics are properly tracked during processing."""
        # Get a valid test file
        test_file = None
        for file_path in sample_tsv_files.values():
            if Path(file_path).exists():
                test_file = file_path
                break

        if not test_file:
            pytest.skip("No valid test files available")

        # Reset statistics
        analyzer.stats = {
            "sentences_processed": 0,
            "tokens_processed": 0,
            "relationships_found": 0,
            "coreference_chains_found": 0,
            "critical_pronouns_found": 0,
            "phrases_found": 0,
        }

        # Process file
        relationships = analyzer.analyze_file(str(test_file))

        # Verify statistics were updated
        stats = analyzer.get_statistics()
        assert stats["sentences_processed"] > 0
        assert stats["relationships_found"] == len(relationships)

        # Statistics should be consistent
        if relationships:
            assert stats["relationships_found"] > 0

    def test_export_functionality(self, analyzer, sample_tsv_files, tmp_path):
        """Test export functionality with different formats."""
        # Get a valid test file
        test_file = None
        for file_path in sample_tsv_files.values():
            if Path(file_path).exists():
                test_file = file_path
                break

        if not test_file:
            pytest.skip("No valid test files available")

        # Process file
        relationships = analyzer.analyze_file(str(test_file))

        if not relationships:
            pytest.skip("No relationships found for export testing")

        # Test export
        output_file = tmp_path / "test_output.csv"
        analyzer.export_results(relationships, str(output_file))

        # Verify export file was created
        assert output_file.exists()
        assert output_file.stat().st_size > 0

        # Verify CSV structure
        import pandas as pd

        df = pd.read_csv(output_file)
        assert len(df) == len(relationships)
        assert "sentence_num" in df.columns
        assert "pronoun_text" in df.columns
        assert "clause_mate_text" in df.columns


@pytest.mark.integration
class TestErrorHandling:
    """Integration tests for error handling scenarios."""

    @pytest.fixture
    def analyzer(self):
        """Create analyzer for error testing."""
        return ClauseMateAnalyzer()

    def test_nonexistent_file(self, analyzer):
        """Test handling of nonexistent files."""
        with pytest.raises(ClauseMateExtractionError):
            analyzer.analyze_file("nonexistent_file.tsv")

    def test_empty_file(self, analyzer, tmp_path):
        """Test handling of empty files."""
        empty_file = tmp_path / "empty.tsv"
        empty_file.write_text("")

        # Empty files should either raise an exception or return empty results
        try:
            relationships = analyzer.analyze_file(str(empty_file))
            assert isinstance(relationships, list)
            assert len(relationships) == 0
        except ClauseMateExtractionError:
            # This is also acceptable behavior
            pass

    def test_invalid_tsv_format(self, analyzer, tmp_path):
        """Test handling of invalid TSV format."""
        invalid_file = tmp_path / "invalid.tsv"
        invalid_file.write_text("This is not a valid TSV file")

        # Should handle gracefully
        try:
            relationships = analyzer.analyze_file(str(invalid_file))
            assert isinstance(relationships, list)
        except ClauseMateExtractionError:
            # Controlled exception is acceptable
            pass

    def test_export_to_readonly_location(self, analyzer, tmp_path):
        """Test export error handling."""
        relationships = []  # Empty relationships

        # Try to export to a location that doesn't exist
        nonexistent_path = tmp_path / "nonexistent" / "output.csv"

        # Should create directories automatically
        analyzer.export_results(relationships, str(nonexistent_path))


@pytest.mark.integration
@pytest.mark.performance
class TestPerformanceBaseline:
    """Performance baseline tests for integration testing."""

    @pytest.fixture
    def analyzer(self):
        """Create analyzer for performance testing."""
        return ClauseMateAnalyzer(enable_adaptive_parsing=True)

    def test_processing_performance(
        self, analyzer, sample_tsv_files, performance_thresholds
    ):
        """Test processing performance meets baseline requirements."""
        for format_name, file_path in sample_tsv_files.items():
            if not Path(file_path).exists():
                continue

            start_time = time.time()
            relationships = analyzer.analyze_file(str(file_path))
            processing_time = time.time() - start_time

            # Determine file size category
            file_size = Path(file_path).stat().st_size
            if file_size < 1000:  # Small file
                max_time = performance_thresholds["max_processing_time"]["small"]
            elif file_size < 10000:  # Medium file
                max_time = performance_thresholds["max_processing_time"]["medium"]
            else:  # Large file
                max_time = performance_thresholds["max_processing_time"]["large"]

            assert processing_time < max_time, (
                f"Processing time {processing_time:.2f}s exceeded threshold {max_time}s "
                f"for {format_name} format"
            )

    def test_memory_usage_baseline(self, analyzer, sample_tsv_files):
        """Test memory usage stays within reasonable bounds."""
        import os

        import psutil

        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB

        for format_name, file_path in sample_tsv_files.items():
            if not Path(file_path).exists():
                continue

            relationships = analyzer.analyze_file(str(file_path))
            current_memory = process.memory_info().rss / 1024 / 1024  # MB
            memory_increase = current_memory - initial_memory

            # Memory increase should be reasonable (less than 100MB for test files)
            assert memory_increase < 100, (
                f"Memory usage increased by {memory_increase:.2f}MB "
                f"for {format_name} format, which exceeds 100MB threshold"
            )


@pytest.mark.integration
class TestRegressionBaseline:
    """Regression baseline tests to establish expected behavior."""

    @pytest.fixture
    def analyzer(self):
        """Create analyzer for regression testing."""
        return ClauseMateAnalyzer(enable_adaptive_parsing=True)

    def test_relationship_extraction_consistency(self, analyzer, sample_tsv_files):
        """Test that relationship extraction is consistent across runs."""
        for format_name, file_path in sample_tsv_files.items():
            if not Path(file_path).exists():
                continue

            # Run analysis multiple times
            results = []
            for _ in range(3):
                relationships = analyzer.analyze_file(str(file_path))
                results.append(len(relationships))

            # Results should be consistent
            assert all(count == results[0] for count in results), (
                f"Inconsistent relationship counts for {format_name}: {results}"
            )

    def test_output_format_consistency(
        self, analyzer, sample_tsv_files, expected_columns
    ):
        """Test that output format is consistent."""
        for format_name, file_path in sample_tsv_files.items():
            if not Path(file_path).exists():
                continue

            relationships = analyzer.analyze_file(str(file_path))

            if relationships:
                # Test dictionary conversion
                data_dict = relationships[0].to_dict()

                # Should contain expected columns
                for col in expected_columns[:10]:  # Check first 10 columns
                    assert col in data_dict, (
                        f"Missing column {col} in {format_name} format output"
                    )
