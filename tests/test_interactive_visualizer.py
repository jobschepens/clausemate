"""Tests for interactive_visualizer.py."""

import tempfile
from pathlib import Path
from unittest.mock import patch

from src.visualization.interactive_visualizer import InteractiveVisualizer


class TestInteractiveVisualizer:
    """Test the InteractiveVisualizer class."""

    def setup_method(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.visualizer = InteractiveVisualizer(self.temp_dir)

    def teardown_method(self):
        """Clean up test fixtures."""
        import shutil

        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_initialization(self):
        """Test that the visualizer initializes correctly."""
        assert isinstance(self.visualizer, InteractiveVisualizer)
        assert hasattr(self.visualizer, "output_dir")
        assert hasattr(self.visualizer, "logger")
        assert Path(self.temp_dir).exists()

    def test_create_cross_chapter_network_visualization(self):
        """Test cross-chapter network visualization creation."""
        # Mock data
        cross_chapter_chains = {
            "unified_chain_115": ["Karl", "er", "Mann"],
            "unified_chain_200": ["Anna", "sie"],
        }

        relationships_data = [
            {"chapter_number": 1, "pronoun_text": "er", "clause_mate_text": "Karl"},
            {"chapter_number": 2, "pronoun_text": "sie", "clause_mate_text": "Anna"},
        ]

        with patch("logging.getLogger"):
            output_path = self.visualizer.create_cross_chapter_network_visualization(
                cross_chapter_chains, relationships_data
            )

        # Verify output file was created
        assert Path(output_path).exists()

        # Verify HTML content
        with open(output_path, encoding="utf-8") as f:
            content = f.read()

        assert "Cross-Chapter Coreference Network" in content
        assert "Chapter 1" in content
        assert "Chapter 2" in content
        assert "Chain 115" in content
        assert "Chain 200" in content
        assert "vis.Network" in content  # JavaScript visualization

    def test_create_cross_chapter_network_visualization_empty_data(self):
        """Test cross-chapter network visualization with empty data."""
        cross_chapter_chains = {}
        relationships_data = []

        with patch("logging.getLogger"):
            output_path = self.visualizer.create_cross_chapter_network_visualization(
                cross_chapter_chains, relationships_data
            )

        assert Path(output_path).exists()

        with open(output_path, encoding="utf-8") as f:
            content = f.read()

        assert "Cross-Chapter Coreference Network" in content
        assert "Chapter 1" in content  # Default chapters
        assert "Chapter 2" in content
        assert "Chapter 3" in content
        assert "Chapter 4" in content

    def test_create_cross_chapter_network_visualization_custom_filename(self):
        """Test cross-chapter network visualization with custom filename."""
        cross_chapter_chains = {"unified_chain_115": ["Karl"]}
        relationships_data = [{"chapter_number": 1}]

        with patch("logging.getLogger"):
            output_path = self.visualizer.create_cross_chapter_network_visualization(
                cross_chapter_chains, relationships_data, "custom_network.html"
            )

        expected_path = Path(self.temp_dir) / "custom_network.html"
        assert output_path == str(expected_path)
        assert expected_path.exists()

    def test_create_chapter_analysis_reports(self):
        """Test chapter analysis reports creation."""
        relationships_data = [
            {
                "chapter_number": 1,
                "pronoun_text": "er",
                "clause_mate_text": "Karl",
                "sentence_num": 1,
                "cross_chapter_relationship": False,
            },
            {
                "chapter_number": 1,
                "pronoun_text": "sie",
                "clause_mate_text": "Anna",
                "sentence_num": 2,
                "cross_chapter_relationship": True,
            },
            {
                "chapter_number": 2,
                "pronoun_text": "er",
                "clause_mate_text": "Mann",
                "sentence_num": 1,
                "cross_chapter_relationship": False,
            },
        ]

        processing_stats = {"processing_time_seconds": 10.5}

        with patch("logging.getLogger"):
            output_path = self.visualizer.create_chapter_analysis_reports(
                relationships_data, processing_stats
            )

        assert Path(output_path).exists()

        with open(output_path, encoding="utf-8") as f:
            content = f.read()

        assert "Chapter-by-Chapter Analysis Reports" in content
        assert "Chapter 1 Analysis" in content
        assert "Chapter 2 Analysis" in content
        assert "Total Relationships" in content
        assert "Cross-Chapter Links" in content
        assert "10.50s" in content  # Processing time

    def test_create_chapter_analysis_reports_empty_data(self):
        """Test chapter analysis reports with empty data."""
        relationships_data = []
        processing_stats = {}

        with patch("logging.getLogger"):
            output_path = self.visualizer.create_chapter_analysis_reports(
                relationships_data, processing_stats
            )

        assert Path(output_path).exists()

        with open(output_path, encoding="utf-8") as f:
            content = f.read()

        assert "Chapter-by-Chapter Analysis Reports" in content
        assert "0" in content  # Should show zero chapters

    def test_create_chapter_analysis_reports_custom_filename(self):
        """Test chapter analysis reports with custom filename."""
        relationships_data = [{"chapter_number": 1}]
        processing_stats = {}

        with patch("logging.getLogger"):
            output_path = self.visualizer.create_chapter_analysis_reports(
                relationships_data, processing_stats, "custom_reports.html"
            )

        expected_path = Path(self.temp_dir) / "custom_reports.html"
        assert output_path == str(expected_path)
        assert expected_path.exists()

    def test_create_comparative_dashboard(self):
        """Test comparative dashboard creation."""
        relationships_data = [
            {
                "chapter_number": 1,
                "pronoun_coreference_type": "PersPron",
                "cross_chapter_relationship": False,
                "pronoun_most_recent_antecedent_distance": 2,
                "pronoun_givenness": "bekannt",
            },
            {
                "chapter_number": 1,
                "pronoun_coreference_type": "PersPron",
                "cross_chapter_relationship": True,
                "pronoun_most_recent_antecedent_distance": 3,
                "pronoun_givenness": "neu",
            },
            {
                "chapter_number": 2,
                "pronoun_coreference_type": "DemonPron",
                "cross_chapter_relationship": False,
                "pronoun_most_recent_antecedent_distance": 1,
                "pronoun_givenness": "bekannt",
            },
        ]

        cross_chapter_chains = {
            "chain_1": ["entity1", "entity2"],
            "chain_2": ["entity3"],
        }

        processing_stats = {"processing_time_seconds": 15.5}

        with patch("logging.getLogger"):
            output_path = self.visualizer.create_comparative_dashboard(
                relationships_data, cross_chapter_chains, processing_stats
            )

        assert Path(output_path).exists()

        with open(output_path, encoding="utf-8") as f:
            content = f.read()

        assert "Comparative Analysis Dashboard" in content
        assert "Chapter Comparison Matrix" in content
        assert "Pronoun Type Distribution" in content
        assert "Cross-Chapter Connectivity" in content
        assert "PersPron" in content
        assert "DemonPron" in content
        assert "15.50s" in content  # Processing time

    def test_create_comparative_dashboard_empty_data(self):
        """Test comparative dashboard with empty data."""
        relationships_data = []
        cross_chapter_chains = {}
        processing_stats = {}

        with patch("logging.getLogger"):
            output_path = self.visualizer.create_comparative_dashboard(
                relationships_data, cross_chapter_chains, processing_stats
            )

        assert Path(output_path).exists()

        with open(output_path, encoding="utf-8") as f:
            content = f.read()

        assert "Comparative Analysis Dashboard" in content
        assert "0" in content  # Should show zero values

    def test_create_comparative_dashboard_custom_filename(self):
        """Test comparative dashboard with custom filename."""
        relationships_data = [{"chapter_number": 1}]
        cross_chapter_chains = {}
        processing_stats = {}

        with patch("logging.getLogger"):
            output_path = self.visualizer.create_comparative_dashboard(
                relationships_data,
                cross_chapter_chains,
                processing_stats,
                "custom_dashboard.html",
            )

        expected_path = Path(self.temp_dir) / "custom_dashboard.html"
        assert output_path == str(expected_path)
        assert expected_path.exists()

    def test_create_comparative_dashboard_pronoun_type_analysis(self):
        """Test pronoun type analysis in comparative dashboard."""
        relationships_data = [
            {"chapter_number": 1, "pronoun_coreference_type": "PersPron"},
            {"chapter_number": 1, "pronoun_coreference_type": "DemonPron"},
            {"chapter_number": 2, "pronoun_coreference_type": "PersPron"},
            {"chapter_number": 2, "pronoun_coreference_type": "PersPron"},
        ]

        cross_chapter_chains = {}
        processing_stats = {}

        with patch("logging.getLogger"):
            output_path = self.visualizer.create_comparative_dashboard(
                relationships_data, cross_chapter_chains, processing_stats
            )

        with open(output_path, encoding="utf-8") as f:
            content = f.read()

        # Should contain pronoun type analysis
        assert "PersPron" in content
        assert "DemonPron" in content

        # Should contain chapter comparison data
        assert "Chapter 1" in content
        assert "Chapter 2" in content

    def test_create_comparative_dashboard_distance_analysis(self):
        """Test distance analysis in comparative dashboard."""
        relationships_data = [
            {"chapter_number": 1, "pronoun_most_recent_antecedent_distance": 2},
            {"chapter_number": 1, "pronoun_most_recent_antecedent_distance": 4},
            {"chapter_number": 2, "pronoun_most_recent_antecedent_distance": 1},
        ]

        cross_chapter_chains = {}
        processing_stats = {}

        with patch("logging.getLogger"):
            output_path = self.visualizer.create_comparative_dashboard(
                relationships_data, cross_chapter_chains, processing_stats
            )

        with open(output_path, encoding="utf-8") as f:
            content = f.read()

        # Should contain average distance calculations
        assert "3.0" in content  # Average for chapter 1: (2+4)/2
        assert "1.0" in content  # Average for chapter 2: 1/1

    def test_create_comparative_dashboard_givenness_analysis(self):
        """Test givenness analysis in comparative dashboard."""
        relationships_data = [
            {"chapter_number": 1, "pronoun_givenness": "bekannt"},
            {"chapter_number": 1, "pronoun_givenness": "neu"},
            {"chapter_number": 2, "pronoun_givenness": "bekannt"},
        ]

        cross_chapter_chains = {}
        processing_stats = {}

        with patch("logging.getLogger"):
            output_path = self.visualizer.create_comparative_dashboard(
                relationships_data, cross_chapter_chains, processing_stats
            )

        with open(output_path, encoding="utf-8") as f:
            content = f.read()

        # Should contain givenness type tracking
        assert "bekannt" in content
        assert "neu" in content

    def test_create_comparative_dashboard_performance_metrics(self):
        """Test performance metrics display in comparative dashboard."""
        relationships_data = [
            {"chapter_number": 1},
            {"chapter_number": 2},
            {"chapter_number": 3},
        ]

        cross_chapter_chains = {"chain1": ["a", "b"]}
        processing_stats = {"processing_time_seconds": 12.5}

        with patch("logging.getLogger"):
            output_path = self.visualizer.create_comparative_dashboard(
                relationships_data, cross_chapter_chains, processing_stats
            )

        with open(output_path, encoding="utf-8") as f:
            content = f.read()

        # Should contain performance calculations
        assert "12.50s" in content  # Total processing time
        assert "3" in content  # Chapters analyzed
        assert "1" in content  # Cross-chapter chains

    def test_output_directory_creation(self):
        """Test that output directory is created if it doesn't exist."""
        import shutil

        temp_dir = Path(tempfile.mkdtemp())

        # Remove the directory to test creation
        if temp_dir.exists():
            shutil.rmtree(temp_dir)

        visualizer = InteractiveVisualizer(str(temp_dir))

        assert temp_dir.exists()
        assert temp_dir.is_dir()

        # Clean up
        shutil.rmtree(temp_dir, ignore_errors=True)

    def test_html_content_structure(self):
        """Test that generated HTML has proper structure."""
        cross_chapter_chains = {"chain1": ["entity1"]}
        relationships_data = [{"chapter_number": 1}]

        with patch("logging.getLogger"):
            output_path = self.visualizer.create_cross_chapter_network_visualization(
                cross_chapter_chains, relationships_data
            )

        with open(output_path, encoding="utf-8") as f:
            content = f.read()

        # Check HTML structure
        assert "<!DOCTYPE html>" in content
        assert "<html lang=" in content
        assert "<head>" in content
        assert "<body>" in content
        assert "</html>" in content

        # Check CSS classes
        assert "container" in content
        assert "header" in content
        assert "network-container" in content

        # Check JavaScript
        assert "vis.Network" in content
        assert "DataSet" in content

    def test_json_data_serialization(self):
        """Test that data is properly serialized to JSON in JavaScript."""
        cross_chapter_chains = {"chain1": ["entity1", "entity2"]}
        relationships_data = [{"chapter_number": 1}]

        with patch("logging.getLogger"):
            output_path = self.visualizer.create_cross_chapter_network_visualization(
                cross_chapter_chains, relationships_data
            )

        with open(output_path, encoding="utf-8") as f:
            content = f.read()

        # Should contain valid JSON data
        assert "nodes" in content
        assert "edges" in content
        assert '"id":' in content
        assert '"label":' in content

    def test_timestamp_in_output(self):
        """Test that generated files contain timestamps."""
        cross_chapter_chains = {"chain1": ["entity1"]}
        relationships_data = [{"chapter_number": 1}]

        with patch("logging.getLogger"):
            output_path = self.visualizer.create_cross_chapter_network_visualization(
                cross_chapter_chains, relationships_data
            )

        with open(output_path, encoding="utf-8") as f:
            content = f.read()

        # Should contain a timestamp in YYYY-MM-DD format
        import re

        timestamp_pattern = r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}"
        assert re.search(timestamp_pattern, content) is not None

    def test_logger_usage(self):
        """Test that logger is used appropriately."""
        cross_chapter_chains = {"chain1": ["entity1"]}
        relationships_data = [{"chapter_number": 1}]

        with patch.object(self.visualizer.logger, "info") as mock_info:
            self.visualizer.create_cross_chapter_network_visualization(
                cross_chapter_chains, relationships_data
            )

            # Should have called info method
            mock_info.assert_called()

    def test_file_encoding_utf8(self):
        """Test that output files are written with UTF-8 encoding."""
        cross_chapter_chains = {"chain1": ["entity1"]}
        relationships_data = [{"chapter_number": 1}]

        with patch("logging.getLogger"):
            output_path = self.visualizer.create_cross_chapter_network_visualization(
                cross_chapter_chains, relationships_data
            )

        # Try to read with UTF-8 encoding (should not raise exception)
        with open(output_path, encoding="utf-8") as f:
            content = f.read()

        assert len(content) > 0
        assert "Cross-Chapter Coreference Network" in content
