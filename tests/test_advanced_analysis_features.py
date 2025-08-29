"""Tests for advanced_analysis_features.py."""

import json
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

from src.multi_file.advanced_analysis_features import (
    AdvancedAnalysisEngine,
    CharacterMention,
    CharacterProfile,
    CrossChapterTransition,
    NarrativeFlowSegment,
    PerformanceMetrics,
)


class TestCharacterMention:
    """Test the CharacterMention dataclass."""

    def test_character_mention_creation(self):
        """Test creating a CharacterMention instance."""
        mention = CharacterMention(
            chapter_number=1,
            sentence_id="sent_1",
            global_sentence_id="global_1",
            mention_text="Karl",
            chain_id="chain_1",
            grammatical_role="SUBJ",
            thematic_role="AGENT",
            sentence_position=0.5,
            narrative_importance=0.8,
        )

        assert mention.chapter_number == 1
        assert mention.sentence_id == "sent_1"
        assert mention.global_sentence_id == "global_1"
        assert mention.mention_text == "Karl"
        assert mention.chain_id == "chain_1"
        assert mention.grammatical_role == "SUBJ"
        assert mention.thematic_role == "AGENT"
        assert mention.sentence_position == 0.5
        assert mention.narrative_importance == 0.8


class TestCharacterProfile:
    """Test the CharacterProfile dataclass."""

    def test_character_profile_creation(self):
        """Test creating a CharacterProfile instance."""
        mentions = [
            CharacterMention(
                chapter_number=1,
                sentence_id="sent_1",
                global_sentence_id="global_1",
                mention_text="Karl",
                chain_id="chain_1",
                grammatical_role="SUBJ",
                thematic_role="AGENT",
                sentence_position=0.5,
                narrative_importance=0.8,
            )
        ]

        profile = CharacterProfile(
            character_id="char_1",
            primary_name="Karl",
            alternative_names=["he"],
            first_appearance_chapter=1,
            last_appearance_chapter=2,
            total_mentions=10,
            chapters_present=[1, 2],
            mentions=mentions,
            narrative_prominence=0.9,
            character_consistency=0.8,
            cross_chapter_continuity=0.7,
            dialogue_frequency=0.3,
        )

        assert profile.character_id == "char_1"
        assert profile.primary_name == "Karl"
        assert profile.alternative_names == ["he"]
        assert profile.first_appearance_chapter == 1
        assert profile.last_appearance_chapter == 2
        assert profile.total_mentions == 10
        assert profile.chapters_present == [1, 2]
        assert len(profile.mentions) == 1
        assert profile.narrative_prominence == 0.9
        assert profile.character_consistency == 0.8
        assert profile.cross_chapter_continuity == 0.7
        assert profile.dialogue_frequency == 0.3


class TestNarrativeFlowSegment:
    """Test the NarrativeFlowSegment dataclass."""

    def test_narrative_flow_segment_creation(self):
        """Test creating a NarrativeFlowSegment instance."""
        segment = NarrativeFlowSegment(
            chapter_number=1,
            segment_start=1,
            segment_end=25,
            segment_type="introduction",
            character_density=0.8,
            coreference_density=1.2,
            narrative_tension=0.6,
            key_characters=["Karl", "Anna"],
        )

        assert segment.chapter_number == 1
        assert segment.segment_start == 1
        assert segment.segment_end == 25
        assert segment.segment_type == "introduction"
        assert segment.character_density == 0.8
        assert segment.coreference_density == 1.2
        assert segment.narrative_tension == 0.6
        assert segment.key_characters == ["Karl", "Anna"]


class TestCrossChapterTransition:
    """Test the CrossChapterTransition dataclass."""

    def test_cross_chapter_transition_creation(self):
        """Test creating a CrossChapterTransition instance."""
        transition = CrossChapterTransition(
            from_chapter=1,
            to_chapter=2,
            character_continuity=0.8,
            thematic_continuity=0.7,
            temporal_gap_indicator=0.5,
            narrative_coherence=0.75,
            shared_characters=["Karl"],
            new_characters=["Anna"],
            dropped_characters=["Peter"],
        )

        assert transition.from_chapter == 1
        assert transition.to_chapter == 2
        assert transition.character_continuity == 0.8
        assert transition.thematic_continuity == 0.7
        assert transition.temporal_gap_indicator == 0.5
        assert transition.narrative_coherence == 0.75
        assert transition.shared_characters == ["Karl"]
        assert transition.new_characters == ["Anna"]
        assert transition.dropped_characters == ["Peter"]


class TestPerformanceMetrics:
    """Test the PerformanceMetrics dataclass."""

    def test_performance_metrics_creation(self):
        """Test creating a PerformanceMetrics instance."""
        metrics = PerformanceMetrics(
            total_processing_time=45.2,
            per_chapter_times={1: 15.0, 2: 20.0, 3: 10.2},
            memory_usage_peak=150.5,
            relationships_per_second=95.3,
            cross_chapter_resolution_time=8.5,
            parser_success_rate=0.98,
            cross_chapter_detection_accuracy=0.92,
            chain_resolution_completeness=0.89,
            processing_efficiency=85.7,
            memory_efficiency=120.4,
        )

        assert metrics.total_processing_time == 45.2
        assert metrics.per_chapter_times == {1: 15.0, 2: 20.0, 3: 10.2}
        assert metrics.memory_usage_peak == 150.5
        assert metrics.relationships_per_second == 95.3
        assert metrics.cross_chapter_resolution_time == 8.5
        assert metrics.parser_success_rate == 0.98
        assert metrics.cross_chapter_detection_accuracy == 0.92
        assert metrics.chain_resolution_completeness == 0.89
        assert metrics.processing_efficiency == 85.7
        assert metrics.memory_efficiency == 120.4


class TestAdvancedAnalysisEngine:
    """Test the AdvancedAnalysisEngine class."""

    def setup_method(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.engine = AdvancedAnalysisEngine(self.temp_dir)

    def teardown_method(self):
        """Clean up test fixtures."""
        import shutil

        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_initialization(self):
        """Test that the engine initializes correctly."""
        assert self.engine.output_dir == Path(self.temp_dir)
        assert hasattr(self.engine, "logger")

    @patch("src.multi_file.advanced_analysis_features.logging")
    def test_initialization_with_logger(self, mock_logging):
        """Test initialization with logging setup."""
        mock_logger = MagicMock()
        mock_logging.getLogger.return_value = mock_logger

        engine = AdvancedAnalysisEngine(self.temp_dir)

        mock_logging.getLogger.assert_called_once_with(__name__)
        assert engine.logger == mock_logger

    def test_analyze_character_tracking_empty_relationships(self):
        """Test character tracking with empty relationships."""
        result = self.engine.analyze_character_tracking([], [], [])
        assert result == {}

    def test_analyze_character_tracking_single_relationship(self):
        """Test character tracking with a single relationship."""
        # Create mock relationship
        mock_relationship = MagicMock()
        mock_relationship.chapter_number = 1
        mock_relationship.sentence_id = "sent_1"
        mock_relationship.sentence_num = 1
        mock_relationship.pronoun_coref_ids = ["chain_1"]
        mock_relationship.pronoun = MagicMock()
        mock_relationship.pronoun.text = "er"
        mock_relationship.pronoun.grammatical_role = "SUBJ"
        mock_relationship.pronoun.thematic_role = "AGENT"
        mock_relationship.clause_mate = MagicMock()
        mock_relationship.clause_mate.coreference_id = None

        # Create mock chapter metadata
        mock_chapter_meta = MagicMock()
        mock_chapter_meta.chapter_number = 1
        mock_chapter_meta.sentence_range = (1, 10)

        result = self.engine.analyze_character_tracking(
            [mock_relationship], [mock_chapter_meta], []
        )

        # Should have one character profile
        assert len(result) == 1
        assert "chain_1" in result
        profile = result["chain_1"]
        assert profile.primary_name == "er"
        assert profile.total_mentions == 1
        assert profile.first_appearance_chapter == 1
        assert profile.last_appearance_chapter == 1

    def test_analyze_narrative_flow_empty_relationships(self):
        """Test narrative flow analysis with empty relationships."""
        result = self.engine.analyze_narrative_flow([], [], {})
        assert result == []

    def test_analyze_cross_chapter_transitions_empty_metadata(self):
        """Test cross-chapter transitions with empty metadata."""
        result = self.engine.analyze_cross_chapter_transitions([], {}, [])
        assert result == []

    def test_analyze_cross_chapter_transitions_single_transition(self):
        """Test cross-chapter transitions with single transition."""
        # Create mock chapter metadata
        mock_chapter1 = MagicMock()
        mock_chapter1.chapter_number = 1
        mock_chapter1.total_relationships = 10

        mock_chapter2 = MagicMock()
        mock_chapter2.chapter_number = 2
        mock_chapter2.total_relationships = 15

        # Create mock character profiles
        mock_profile = MagicMock()
        mock_profile.chapters_present = [1, 2]

        character_profiles = {"char_1": mock_profile}

        result = self.engine.analyze_cross_chapter_transitions(
            [mock_chapter1, mock_chapter2], character_profiles, []
        )

        assert len(result) == 1
        transition = result[0]
        assert transition.from_chapter == 1
        assert transition.to_chapter == 2
        assert transition.character_continuity == 1.0  # All characters continue
        assert transition.shared_characters == ["char_1"]
        assert transition.new_characters == []
        assert transition.dropped_characters == []

    def test_calculate_performance_metrics(self):
        """Test performance metrics calculation."""
        processing_stats = {
            "processing_time_seconds": 30.0,
            "total_relationships": 1500,
        }

        # Create mock chapter metadata
        mock_chapter = MagicMock()
        mock_chapter.chapter_number = 1
        mock_chapter.total_relationships = 1500

        # Create mock relationships
        mock_relationships = [MagicMock() for _ in range(1500)]

        result = self.engine.calculate_performance_metrics(
            processing_stats, [mock_chapter], mock_relationships
        )

        assert isinstance(result, PerformanceMetrics)
        assert result.total_processing_time == 30.0
        assert result.relationships_per_second == 50.0  # 1500 / 30
        assert result.parser_success_rate == 1.0
        assert result.cross_chapter_detection_accuracy == 0.95

    def test_generate_coreference_visualization_data(self):
        """Test coreference visualization data generation."""
        # Create mock character profiles
        mock_profile = MagicMock()
        mock_profile.primary_name = "Karl"
        mock_profile.narrative_prominence = 0.9
        mock_profile.chapters_present = [1, 2]
        mock_profile.total_mentions = 25

        character_profiles = {"char_1": mock_profile}

        # Create mock relationships
        mock_relationships = [MagicMock()]

        # Create mock cross-chapter connections
        mock_connection = MagicMock()
        mock_connection.from_chapter = 1
        mock_connection.to_chapter = 2
        mock_connection.strength = 0.8
        mock_connection.connection_type = "coreference"
        mock_connection.chain_id = "chain_1"

        result_path = self.engine.generate_coreference_visualization_data(
            mock_relationships, character_profiles, [mock_connection]
        )

        # Check that file was created
        assert Path(result_path).exists()

        # Check file contents
        with open(result_path) as f:
            data = json.load(f)

        assert "metadata" in data
        assert "nodes" in data
        assert "edges" in data
        assert len(data["nodes"]) == 1
        assert len(data["edges"]) == 1
        assert data["nodes"][0]["label"] == "Karl"
        assert data["edges"][0]["weight"] == 0.8

    def test_create_comprehensive_analysis_report(self):
        """Test comprehensive analysis report creation."""
        # Create mock data
        mock_profile = MagicMock()
        mock_profile.primary_name = "Karl"
        mock_profile.narrative_prominence = 0.9
        mock_profile.cross_chapter_continuity = 0.8
        mock_profile.chapters_present = [1, 2]

        character_profiles = {"char_1": mock_profile}

        mock_segment = MagicMock()
        mock_segment.segment_type = "introduction"
        mock_segment.narrative_tension = 0.6
        mock_segment.character_density = 0.8

        narrative_segments = [mock_segment]

        mock_transition = MagicMock()
        mock_transition.narrative_coherence = 0.75
        mock_transition.character_continuity = 0.8

        transitions = [mock_transition]

        mock_metrics = MagicMock()
        mock_metrics.total_processing_time = 30.0
        mock_metrics.relationships_per_second = 50.0

        result_path = self.engine.create_comprehensive_analysis_report(
            character_profiles, narrative_segments, transitions, mock_metrics
        )

        # Check that file was created
        assert Path(result_path).exists()

        # Check file contents
        with open(result_path) as f:
            data = json.load(f)

        assert "metadata" in data
        assert "executive_summary" in data
        assert "character_analysis" in data
        assert "narrative_analysis" in data
        assert "transition_analysis" in data
        assert "performance_analysis" in data
        assert "recommendations" in data

        assert data["executive_summary"]["total_characters"] == 1
        assert data["executive_summary"]["narrative_segments"] == 1
        assert data["executive_summary"]["chapter_transitions"] == 1

    def test_get_character_color(self):
        """Test character color assignment based on prominence."""
        # Test major character (high prominence)
        mock_profile = MagicMock()
        mock_profile.narrative_prominence = 0.9

        color = self.engine._get_character_color(mock_profile)
        assert color == "#FF6B6B"  # Red for major characters

        # Test important character
        mock_profile.narrative_prominence = 0.6
        color = self.engine._get_character_color(mock_profile)
        assert color == "#4ECDC4"  # Teal for important characters

        # Test minor character
        mock_profile.narrative_prominence = 0.3
        color = self.engine._get_character_color(mock_profile)
        assert color == "#45B7D1"  # Blue for minor characters

        # Test background character
        mock_profile.narrative_prominence = 0.1
        color = self.engine._get_character_color(mock_profile)
        assert color == "#96CEB4"  # Green for background characters

    def test_calculate_character_statistics_empty_profiles(self):
        """Test character statistics calculation with empty profiles."""
        result = self.engine._calculate_character_statistics({})
        assert result == {}

    def test_calculate_character_statistics_with_profiles(self):
        """Test character statistics calculation with profiles."""
        mock_profile1 = MagicMock()
        mock_profile1.narrative_prominence = 0.9
        mock_profile1.cross_chapter_continuity = 0.8
        mock_profile1.chapters_present = [1, 2]

        mock_profile2 = MagicMock()
        mock_profile2.narrative_prominence = 0.3
        mock_profile2.cross_chapter_continuity = 0.5
        mock_profile2.chapters_present = [1]

        profiles = {"char_1": mock_profile1, "char_2": mock_profile2}

        result = self.engine._calculate_character_statistics(profiles)

        assert result["total_characters"] == 2
        assert result["major_characters"] == 1
        assert result["minor_characters"] == 1
        assert result["cross_chapter_characters"] == 1
        assert result["average_prominence"] == 0.6
        assert result["average_continuity"] == 0.65

    def test_calculate_narrative_statistics_empty_segments(self):
        """Test narrative statistics calculation with empty segments."""
        result = self.engine._calculate_narrative_statistics([])
        assert result == {}

    def test_calculate_narrative_statistics_with_segments(self):
        """Test narrative statistics calculation with segments."""
        mock_segment1 = MagicMock()
        mock_segment1.segment_type = "introduction"
        mock_segment1.narrative_tension = 0.6
        mock_segment1.character_density = 0.8

        mock_segment2 = MagicMock()
        mock_segment2.segment_type = "climax"
        mock_segment2.narrative_tension = 1.0
        mock_segment2.character_density = 1.2

        segments = [mock_segment1, mock_segment2]

        result = self.engine._calculate_narrative_statistics(segments)

        assert result["total_segments"] == 2
        assert result["average_character_density"] == 1.0
        assert result["average_narrative_tension"] == 0.8
        assert result["climax_segments"] == 1
        assert result["development_segments"] == 0

    def test_calculate_transition_statistics_empty_transitions(self):
        """Test transition statistics calculation with empty transitions."""
        result = self.engine._calculate_transition_statistics([])
        assert result == {}

    def test_calculate_transition_statistics_with_transitions(self):
        """Test transition statistics calculation with transitions."""
        mock_transition1 = MagicMock()
        mock_transition1.character_continuity = 0.8
        mock_transition1.narrative_coherence = 0.9

        mock_transition2 = MagicMock()
        mock_transition2.character_continuity = 0.4
        mock_transition2.narrative_coherence = 0.2

        transitions = [mock_transition1, mock_transition2]

        result = self.engine._calculate_transition_statistics(transitions)

        assert result["total_transitions"] == 2
        assert result["average_character_continuity"] == 0.6
        assert result["average_narrative_coherence"] == 0.55
        assert result["strong_transitions"] == 1
        assert result["weak_transitions"] == 1

    def test_generate_analysis_recommendations(self):
        """Test analysis recommendations generation."""
        # Create mock data with issues that should trigger recommendations
        mock_profile = MagicMock()
        mock_profile.narrative_prominence = 0.3  # Not major character

        character_profiles = {"char_1": mock_profile}

        mock_segment = MagicMock()
        mock_segment.narrative_tension = 0.3  # Low tension

        narrative_segments = [mock_segment]

        mock_transition = MagicMock()
        mock_transition.narrative_coherence = 0.2  # Weak coherence

        transitions = [mock_transition]

        mock_metrics = MagicMock()
        mock_metrics.relationships_per_second = 50  # Low performance

        recommendations = self.engine._generate_analysis_recommendations(
            character_profiles, narrative_segments, transitions, mock_metrics
        )

        # Should generate multiple recommendations
        assert len(recommendations) >= 3
        assert any("major characters" in rec for rec in recommendations)
        assert any("narrative tension" in rec for rec in recommendations)
        assert any("character continuity" in rec for rec in recommendations)
        assert any("processing pipeline" in rec for rec in recommendations)
