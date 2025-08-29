"""Tests for enhanced_output_system.py."""

import json
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

from src.multi_file.enhanced_output_system import (
    ChapterMetadata,
    CrossChapterConnection,
    EnhancedOutputSystem,
    ProcessingStatistics,
)


class TestChapterMetadata:
    """Test the ChapterMetadata dataclass."""

    def test_chapter_metadata_creation(self):
        """Test creating a ChapterMetadata instance."""
        metadata = ChapterMetadata(
            chapter_number=1,
            chapter_id="chap_1",
            source_file="/path/to/file.tsv",
            file_format="standard",
            total_relationships=100,
            total_sentences=50,
            sentence_range=(1, 50),
            global_sentence_range=(1, 50),
            coreference_chains=5,
            processing_time=2.5,
            file_size_bytes=1024,
            encoding="utf-8",
        )

        assert metadata.chapter_number == 1
        assert metadata.chapter_id == "chap_1"
        assert metadata.source_file == "/path/to/file.tsv"
        assert metadata.file_format == "standard"
        assert metadata.total_relationships == 100
        assert metadata.total_sentences == 50
        assert metadata.sentence_range == (1, 50)
        assert metadata.global_sentence_range == (1, 50)
        assert metadata.coreference_chains == 5
        assert metadata.processing_time == 2.5
        assert metadata.file_size_bytes == 1024
        assert metadata.encoding == "utf-8"


class TestCrossChapterConnection:
    """Test the CrossChapterConnection dataclass."""

    def test_cross_chapter_connection_creation(self):
        """Test creating a CrossChapterConnection instance."""
        connection = CrossChapterConnection(
            chain_id="chain_1",
            from_chapter=1,
            to_chapter=2,
            connection_type="same_chain_id",
            strength=0.8,
            mentions_count=5,
            sentence_span=(10, 25),
        )

        assert connection.chain_id == "chain_1"
        assert connection.from_chapter == 1
        assert connection.to_chapter == 2
        assert connection.connection_type == "same_chain_id"
        assert connection.strength == 0.8
        assert connection.mentions_count == 5
        assert connection.sentence_span == (10, 25)


class TestProcessingStatistics:
    """Test the ProcessingStatistics dataclass."""

    def test_processing_statistics_creation(self):
        """Test creating a ProcessingStatistics instance."""
        chapter_metadata = [
            ChapterMetadata(
                chapter_number=1,
                chapter_id="chap_1",
                source_file="/path/to/file1.tsv",
                file_format="standard",
                total_relationships=100,
                total_sentences=50,
                sentence_range=(1, 50),
                global_sentence_range=(1, 50),
                coreference_chains=5,
                processing_time=2.5,
                file_size_bytes=1024,
            )
        ]

        cross_chapter_connections = [
            CrossChapterConnection(
                chain_id="chain_1",
                from_chapter=1,
                to_chapter=2,
                connection_type="same_chain_id",
                strength=0.8,
                mentions_count=5,
                sentence_span=(10, 25),
            )
        ]

        stats = ProcessingStatistics(
            total_chapters=2,
            total_relationships=200,
            total_sentences=100,
            total_coreference_chains=10,
            cross_chapter_chains=2,
            cross_chapter_relationships=15,
            processing_time_seconds=5.0,
            memory_usage_mb=150.5,
            chapter_breakdown=chapter_metadata,
            cross_chapter_connections=cross_chapter_connections,
            average_relationships_per_sentence=2.0,
            average_chain_length=20.0,
            cross_chapter_percentage=20.0,
        )

        assert stats.total_chapters == 2
        assert stats.total_relationships == 200
        assert stats.total_sentences == 100
        assert stats.total_coreference_chains == 10
        assert stats.cross_chapter_chains == 2
        assert stats.cross_chapter_relationships == 15
        assert stats.processing_time_seconds == 5.0
        assert stats.memory_usage_mb == 150.5
        assert len(stats.chapter_breakdown) == 1
        assert len(stats.cross_chapter_connections) == 1
        assert stats.average_relationships_per_sentence == 2.0
        assert stats.average_chain_length == 20.0
        assert stats.cross_chapter_percentage == 20.0


class TestEnhancedOutputSystem:
    """Test the EnhancedOutputSystem class."""

    def setup_method(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.system = EnhancedOutputSystem(self.temp_dir)

    def teardown_method(self):
        """Clean up test fixtures."""
        import shutil

        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_initialization(self):
        """Test that the system initializes correctly."""
        assert self.system.output_dir == Path(self.temp_dir)
        assert hasattr(self.system, "logger")

    @patch("src.multi_file.enhanced_output_system.logging")
    def test_initialization_with_logger(self, mock_logging):
        """Test initialization with logging setup."""
        mock_logger = MagicMock()
        mock_logging.getLogger.return_value = mock_logger

        system = EnhancedOutputSystem(self.temp_dir)

        mock_logging.getLogger.assert_called_once_with(
            "src.multi_file.enhanced_output_system"
        )
        assert system.logger == mock_logger

    def test_create_enhanced_csv_output_empty_relationships(self):
        """Test enhanced CSV output with empty relationships."""
        result_path = self.system.create_enhanced_csv_output([], [], [])
        assert Path(result_path).exists()

        # Check that file contains headers
        with open(result_path) as f:
            content = f.read()
            assert "chapter_file" in content
            assert "chapter_number" in content
            assert "global_sentence_id" in content

    def test_create_enhanced_csv_output_with_relationships(self):
        """Test enhanced CSV output with relationships."""
        # Create mock relationship
        mock_relationship = MagicMock()
        mock_relationship.sentence_num = 5
        mock_relationship.pronoun = MagicMock()
        mock_relationship.pronoun.text = "er"
        mock_relationship.pronoun.idx = 2
        mock_relationship.clause_mate = MagicMock()
        mock_relationship.clause_mate.text = "Karl"
        mock_relationship.clause_mate.start_idx = 10
        mock_relationship.clause_mate.end_idx = 14

        # Set default attributes
        mock_relationship.chapter_file = "test.tsv"
        mock_relationship.chapter_number = 1
        mock_relationship.source_file_path = "/path/to/test.tsv"
        mock_relationship.global_sentence_id = "global_5"
        mock_relationship.cross_chapter = False
        mock_relationship.first_words = "Karl sagte"

        # Create mock chapter metadata
        mock_chapter_meta = MagicMock()
        mock_chapter_meta.chapter_number = 1
        mock_chapter_meta.file_format = "standard"
        mock_chapter_meta.file_size_bytes = 1024

        result_path = self.system.create_enhanced_csv_output(
            [mock_relationship], [mock_chapter_meta], []
        )

        assert Path(result_path).exists()

        # Check CSV content
        with open(result_path) as f:
            lines = f.readlines()
            assert len(lines) >= 2  # Header + 1 data row
            header = lines[0]
            data_row = lines[1]

            # Check that key fields are present
            assert "chapter_file" in header
            assert "test.tsv" in data_row
            assert "er" in data_row
            assert "Karl" in data_row

    def test_create_comprehensive_statistics_empty_data(self):
        """Test comprehensive statistics with empty data."""
        result_path = self.system.create_comprehensive_statistics([], [], [], 0.0)
        assert Path(result_path).exists()

        # Check JSON content
        with open(result_path) as f:
            data = json.load(f)

        assert "total_chapters" in data
        assert "total_relationships" in data
        assert "generated_at" in data
        assert "system_version" in data
        assert data["total_chapters"] == 0
        assert data["total_relationships"] == 0

    def test_create_comprehensive_statistics_with_data(self):
        """Test comprehensive statistics with actual data."""
        # Create mock chapter metadata
        mock_chapter_meta1 = MagicMock()
        mock_chapter_meta1.chapter_number = 1
        mock_chapter_meta1.total_sentences = 50
        mock_chapter_meta1.coreference_chains = 5

        mock_chapter_meta2 = MagicMock()
        mock_chapter_meta2.chapter_number = 2
        mock_chapter_meta2.total_sentences = 60
        mock_chapter_meta2.coreference_chains = 6

        chapter_metadata = [mock_chapter_meta1, mock_chapter_meta2]

        # Create mock relationships
        mock_relationships = [MagicMock() for _ in range(100)]
        for i, rel in enumerate(mock_relationships):
            rel.cross_chapter = i < 10  # 10 cross-chapter relationships

        # Create mock cross-chapter connections
        cross_chapter_connections = [MagicMock() for _ in range(3)]

        result_path = self.system.create_comprehensive_statistics(
            mock_relationships, chapter_metadata, cross_chapter_connections, 5.0
        )

        assert Path(result_path).exists()

        # Check JSON content
        with open(result_path) as f:
            data = json.load(f)

        assert data["total_chapters"] == 2
        assert data["total_relationships"] == 100
        assert data["total_sentences"] == 110
        assert data["total_coreference_chains"] == 11
        assert data["cross_chapter_chains"] == 3
        assert data["cross_chapter_relationships"] == 10
        assert data["processing_time_seconds"] == 5.0
        assert "generated_at" in data
        assert "system_version" in data

    def test_create_chapter_boundary_report_empty_data(self):
        """Test chapter boundary report with empty data."""
        result_path = self.system.create_chapter_boundary_report([], [])
        assert Path(result_path).exists()

        # Check JSON content
        with open(result_path) as f:
            data = json.load(f)

        assert "chapter_transitions" in data
        assert "boundary_statistics" in data
        assert "cross_chapter_patterns" in data
        assert "metadata" in data
        assert data["chapter_transitions"] == []
        assert data["boundary_statistics"]["total_boundaries"] == 0

    def test_create_chapter_boundary_report_with_data(self):
        """Test chapter boundary report with actual data."""
        # Create mock chapter metadata
        mock_chapter1 = MagicMock()
        mock_chapter1.chapter_number = 1
        mock_chapter1.global_sentence_range = (1, 50)

        mock_chapter2 = MagicMock()
        mock_chapter2.chapter_number = 2
        mock_chapter2.global_sentence_range = (51, 100)

        chapter_metadata = [mock_chapter1, mock_chapter2]

        # Create mock cross-chapter connections
        mock_connection1 = MagicMock()
        mock_connection1.from_chapter = 1
        mock_connection1.to_chapter = 2
        mock_connection1.connection_type = "same_chain_id"
        mock_connection1.strength = 0.8

        mock_connection2 = MagicMock()
        mock_connection2.from_chapter = 1
        mock_connection2.to_chapter = 2
        mock_connection2.connection_type = "similar_mentions"
        mock_connection2.strength = 0.6

        cross_chapter_connections = [mock_connection1, mock_connection2]

        result_path = self.system.create_chapter_boundary_report(
            chapter_metadata, cross_chapter_connections
        )

        assert Path(result_path).exists()

        # Check JSON content
        with open(result_path) as f:
            data = json.load(f)

        assert len(data["chapter_transitions"]) == 1
        transition = data["chapter_transitions"][0]
        assert transition["from_chapter"] == 1
        assert transition["to_chapter"] == 2
        assert transition["sentence_gap"] == 1  # 51 - 50
        assert transition["connections_count"] == 2
        assert transition["average_strength"] == 0.7

        assert data["boundary_statistics"]["total_boundaries"] == 1
        assert data["boundary_statistics"]["boundaries_with_connections"] == 1

        assert "same_chain_id" in data["cross_chapter_patterns"]
        assert "similar_mentions" in data["cross_chapter_patterns"]

    def test_analyze_cross_chapter_relationship_no_connections(self):
        """Test cross-chapter relationship analysis with no connections."""
        mock_relationship = MagicMock()
        mock_relationship.pronoun_coref_ids = ["chain_1"]

        result = self.system._analyze_cross_chapter_relationship(mock_relationship, [])

        assert result["chain_id"] == ""
        assert result["connection_type"] == "within_chapter"
        assert result["strength"] == 0.0
        assert result["is_cross_chapter"] is False

    def test_analyze_cross_chapter_relationship_with_connection(self):
        """Test cross-chapter relationship analysis with matching connection."""
        mock_relationship = MagicMock()
        mock_relationship.pronoun_coref_ids = ["chain_1"]

        mock_connection = MagicMock()
        mock_connection.chain_id = "chain_1"
        mock_connection.connection_type = "same_chain_id"
        mock_connection.strength = 0.8

        result = self.system._analyze_cross_chapter_relationship(
            mock_relationship, [mock_connection]
        )

        assert result["chain_id"] == "chain_1"
        assert result["connection_type"] == "same_chain_id"
        assert result["strength"] == 0.8
        assert result["is_cross_chapter"] is True

    def test_calculate_analysis_scores_basic_relationship(self):
        """Test analysis scores calculation for basic relationship."""
        mock_relationship = MagicMock()
        mock_relationship.sentence_num = 25
        mock_relationship.pronoun = MagicMock()
        mock_relationship.pronoun.coreference_type = "PersPron[1]"
        mock_relationship.pronoun.most_recent_antecedent_distance = 5

        mock_chapter_meta = MagicMock()
        mock_chapter_meta.sentence_range = (1, 50)

        result = self.system._calculate_analysis_scores(
            mock_relationship, mock_chapter_meta
        )

        assert "narrative_position" in result
        assert "character_continuity_score" in result
        assert "discourse_coherence_score" in result
        assert "chain_importance_score" in result

        # Check narrative position (25 out of 1-50 range)
        assert abs(result["narrative_position"] - 0.49) < 0.01  # (25-1)/(50-1) ≈ 0.49

        # Check chain importance (PersPron should get bonus)
        assert result["chain_importance_score"] > 0.5

    def test_calculate_analysis_scores_no_chapter_meta(self):
        """Test analysis scores calculation without chapter metadata."""
        mock_relationship = MagicMock()
        mock_relationship.sentence_num = 25
        mock_relationship.pronoun = MagicMock()

        result = self.system._calculate_analysis_scores(mock_relationship, None)

        assert result["narrative_position"] == 0.0  # No chapter meta = 0.0
        assert "character_continuity_score" in result
        assert "discourse_coherence_score" in result
        assert "chain_importance_score" in result

    def test_create_boundary_marker_chapter_beginning(self):
        """Test boundary marker creation for chapter beginning."""
        mock_relationship = MagicMock()
        mock_relationship.sentence_num = 3  # Near beginning
        mock_relationship.chapter_number = 1  # Set chapter number for lookup

        mock_chapter_meta = MagicMock()
        mock_chapter_meta.chapter_number = 1
        mock_chapter_meta.sentence_range = (1, 50)

        result = self.system._create_boundary_marker(
            mock_relationship, [mock_chapter_meta]
        )

        assert result == "chapter_beginning"

    def test_create_boundary_marker_chapter_end(self):
        """Test boundary marker creation for chapter end."""
        mock_relationship = MagicMock()
        mock_relationship.sentence_num = 48  # Near end
        mock_relationship.chapter_number = 1  # Set chapter number for lookup

        mock_chapter_meta = MagicMock()
        mock_chapter_meta.chapter_number = 1
        mock_chapter_meta.sentence_range = (1, 50)

        result = self.system._create_boundary_marker(
            mock_relationship, [mock_chapter_meta]
        )

        assert result == "chapter_end"

    def test_create_boundary_marker_chapter_middle(self):
        """Test boundary marker creation for chapter middle."""
        mock_relationship = MagicMock()
        mock_relationship.sentence_num = 25  # Middle
        mock_relationship.chapter_number = 1  # Set chapter number for lookup

        mock_chapter_meta = MagicMock()
        mock_chapter_meta.chapter_number = 1
        mock_chapter_meta.sentence_range = (1, 50)

        result = self.system._create_boundary_marker(
            mock_relationship, [mock_chapter_meta]
        )

        assert result == "chapter_middle"

    def test_calculate_narrative_continuity_no_connections(self):
        """Test narrative continuity calculation with no connections."""
        mock_current = MagicMock()
        mock_next = MagicMock()

        result = self.system._calculate_narrative_continuity(
            mock_current, mock_next, []
        )

        assert result == 0.0

    def test_calculate_narrative_continuity_with_connections(self):
        """Test narrative continuity calculation with connections."""
        mock_current = MagicMock()
        mock_next = MagicMock()

        # Create mock connections with different types and strengths
        mock_conn1 = MagicMock()
        mock_conn1.connection_type = "same_chain_id"
        mock_conn1.strength = 0.8

        mock_conn2 = MagicMock()
        mock_conn2.connection_type = "similar_mentions"
        mock_conn2.strength = 0.6

        connections = [mock_conn1, mock_conn2]

        result = self.system._calculate_narrative_continuity(
            mock_current, mock_next, connections
        )

        # Should be greater than 0 due to connections
        assert result > 0.0
        assert result <= 1.0

        # Calculate expected result:
        # base_score = 2/10.0 = 0.2
        # strength_bonus = (0.8 + 0.6) / 2 = 0.7
        # diversity_bonus = 2 / 3.0 ≈ 0.667
        # total_score = (0.2 + 0.7 + 0.667) / 3.0 ≈ 0.522
        assert abs(result - 0.522) < 0.01
