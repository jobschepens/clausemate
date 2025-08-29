"""Tests for advanced_analysis_features.py."""

import json
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

from src.data.models import ClauseMateRelationship, Phrase, Token
from src.multi_file.advanced_analysis_features import (
    AdvancedAnalysisEngine,
    CharacterMention,
    CharacterProfile,
    CrossChapterTransition,
    NarrativeFlowSegment,
    PerformanceMetrics,
)
from src.multi_file.enhanced_output_system import (
    ChapterMetadata,
    CrossChapterConnection,
)


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
        assert isinstance(self.engine, AdvancedAnalysisEngine)
        assert hasattr(self.engine, "output_dir")
        assert hasattr(self.engine, "logger")
        assert Path(self.temp_dir).exists()

    def test_analyze_character_tracking_basic(self):
        """Test basic character tracking analysis."""
        # Create mock relationships
        token1 = Token(
            idx=1,
            text="Karl",
            sentence_num=1,
            grammatical_role="SUBJ",
            thematic_role="AGENT",
        )
        token2 = Token(
            idx=2,
            text="er",
            sentence_num=1,
            grammatical_role="SUBJ",
            thematic_role="AGENT",
        )
        phrase = Phrase(
            text="Karl",
            coreference_id="115",
            start_idx=1,
            end_idx=1,
            grammatical_role="SUBJ",
            thematic_role="AGENT",
            coreference_type="PersPron[115]",
            animacy=MagicMock(),
            givenness="bekannt",
        )

        relationship = ClauseMateRelationship(
            sentence_id="1",
            sentence_num=1,
            pronoun=token2,
            clause_mate=phrase,
            num_clause_mates=1,
            antecedent_info=MagicMock(),
            pronoun_coref_ids=["115"],
        )

        # Create mock chapter metadata
        chapter_meta = ChapterMetadata(
            chapter_number=1,
            chapter_id="chapter_1",
            source_file="test.tsv",
            file_format="tsv",
            total_relationships=1,
            total_sentences=10,
            sentence_range=(1, 10),
            global_sentence_range=(1, 10),
            coreference_chains=1,
            processing_time=1.0,
            file_size_bytes=1024,
        )

        # Create mock cross-chapter connections
        cross_conn = CrossChapterConnection(
            chain_id="115",
            from_chapter=1,
            to_chapter=2,
            connection_type="coreference",
            strength=0.8,
            mentions_count=2,
            sentence_span=(1, 15),
        )

        with patch("logging.getLogger"):
            profiles = self.engine.analyze_character_tracking(
                [relationship], [chapter_meta], [cross_conn]
            )

        assert len(profiles) == 1
        assert "115" in profiles
        profile = profiles["115"]
        assert profile.character_id == "115"
        assert profile.primary_name == "Karl"
        assert profile.total_mentions == 2  # pronoun + clause mate
        assert profile.first_appearance_chapter == 1
        assert profile.last_appearance_chapter == 1

    def test_analyze_character_tracking_no_relationships(self):
        """Test character tracking with no relationships."""
        with patch("logging.getLogger"):
            profiles = self.engine.analyze_character_tracking([], [], [])

        assert profiles == {}

    def test_analyze_character_tracking_single_mention(self):
        """Test character tracking with single mention (should be filtered out)."""
        token = Token(
            idx=1,
            text="Karl",
            sentence_num=1,
            grammatical_role="SUBJ",
            thematic_role="AGENT",
        )
        phrase = Phrase(
            text="Karl",
            coreference_id="115",
            start_idx=1,
            end_idx=1,
            grammatical_role="SUBJ",
            thematic_role="AGENT",
            coreference_type="PersPron[115]",
            animacy=MagicMock(),
            givenness="bekannt",
        )

        relationship = ClauseMateRelationship(
            sentence_id="1",
            sentence_num=1,
            pronoun=token,
            clause_mate=phrase,
            num_clause_mates=1,
            antecedent_info=MagicMock(),
            pronoun_coref_ids=["115"],
        )

        chapter_meta = ChapterMetadata(
            chapter_number=1,
            chapter_id="chapter_1",
            source_file="test.tsv",
            file_format="tsv",
            total_relationships=1,
            total_sentences=10,
            sentence_range=(1, 10),
            global_sentence_range=(1, 10),
            coreference_chains=1,
            processing_time=1.0,
            file_size_bytes=1024,
        )

        with patch("logging.getLogger"):
            profiles = self.engine.analyze_character_tracking(
                [relationship], [chapter_meta], []
            )

        # Should be empty because character only has 1 mention (filtered out)
        assert profiles == {}

    def test_analyze_narrative_flow(self):
        """Test narrative flow analysis."""
        # Create mock relationships
        token = Token(
            idx=1,
            text="Karl",
            sentence_num=5,
            grammatical_role="SUBJ",
            thematic_role="AGENT",
        )
        phrase = Phrase(
            text="Mann",
            coreference_id="115",
            start_idx=1,
            end_idx=1,
            grammatical_role="SUBJ",
            thematic_role="AGENT",
            coreference_type="PersPron[115]",
            animacy=MagicMock(),
            givenness="bekannt",
        )

        relationship = ClauseMateRelationship(
            sentence_id="5",
            sentence_num=5,
            pronoun=token,
            clause_mate=phrase,
            num_clause_mates=1,
            antecedent_info=MagicMock(),
            pronoun_coref_ids=["115"],
        )

        # Create mock chapter metadata
        chapter_meta = ChapterMetadata(
            chapter_number=1,
            chapter_id="chapter_1",
            source_file="test.tsv",
            file_format="tsv",
            total_relationships=1,
            total_sentences=20,
            sentence_range=(1, 20),
            global_sentence_range=(1, 20),
            coreference_chains=1,
            processing_time=1.0,
            file_size_bytes=1024,
        )

        # Create mock character profiles
        mention = CharacterMention(
            chapter_number=1,
            sentence_id="5",
            global_sentence_id="1-5",
            mention_text="Karl",
            chain_id="115",
            grammatical_role="SUBJ",
            thematic_role="AGENT",
            sentence_position=0.2,
            narrative_importance=0.7,
        )

        profile = CharacterProfile(
            character_id="115",
            primary_name="Karl",
            alternative_names=[],
            first_appearance_chapter=1,
            last_appearance_chapter=1,
            total_mentions=1,
            chapters_present=[1],
            mentions=[mention],
            narrative_prominence=0.5,
            character_consistency=0.8,
            cross_chapter_continuity=0.6,
            dialogue_frequency=0.3,
        )

        with patch("logging.getLogger"):
            segments = self.engine.analyze_narrative_flow(
                [relationship], [chapter_meta], {"115": profile}
            )

        assert len(segments) == 4  # 4 segments per chapter
        assert all(s.chapter_number == 1 for s in segments)
        segment_types = {s.segment_type for s in segments}
        assert segment_types == {"introduction", "development", "climax", "resolution"}

    def test_analyze_cross_chapter_transitions(self):
        """Test cross-chapter transition analysis."""
        # Create mock chapter metadata
        chapter1 = ChapterMetadata(
            chapter_number=1,
            chapter_id="chapter_1",
            source_file="chapter1.tsv",
            file_format="tsv",
            total_relationships=5,
            total_sentences=10,
            sentence_range=(1, 10),
            global_sentence_range=(1, 10),
            coreference_chains=2,
            processing_time=1.0,
            file_size_bytes=1024,
        )

        chapter2 = ChapterMetadata(
            chapter_number=2,
            chapter_id="chapter_2",
            source_file="chapter2.tsv",
            file_format="tsv",
            total_relationships=7,
            total_sentences=15,
            sentence_range=(11, 25),
            global_sentence_range=(11, 25),
            coreference_chains=3,
            processing_time=1.5,
            file_size_bytes=2048,
        )

        # Create mock character profiles
        mention1 = CharacterMention(
            chapter_number=1,
            sentence_id="1",
            global_sentence_id="1-1",
            mention_text="Karl",
            chain_id="115",
            grammatical_role="SUBJ",
            thematic_role="AGENT",
            sentence_position=0.1,
            narrative_importance=0.8,
        )

        mention2 = CharacterMention(
            chapter_number=2,
            sentence_id="15",
            global_sentence_id="2-15",
            mention_text="Karl",
            chain_id="115",
            grammatical_role="SUBJ",
            thematic_role="AGENT",
            sentence_position=0.8,
            narrative_importance=0.7,
        )

        profile = CharacterProfile(
            character_id="115",
            primary_name="Karl",
            alternative_names=[],
            first_appearance_chapter=1,
            last_appearance_chapter=2,
            total_mentions=2,
            chapters_present=[1, 2],
            mentions=[mention1, mention2],
            narrative_prominence=0.6,
            character_consistency=0.9,
            cross_chapter_continuity=0.8,
            dialogue_frequency=0.4,
        )

        # Create mock cross-chapter connections
        cross_conn = CrossChapterConnection(
            chain_id="115",
            from_chapter=1,
            to_chapter=2,
            connection_type="coreference",
            strength=0.9,
            mentions_count=2,
            sentence_span=(1, 15),
        )

        with patch("logging.getLogger"):
            transitions = self.engine.analyze_cross_chapter_transitions(
                [chapter1, chapter2], {"115": profile}, [cross_conn]
            )

        assert len(transitions) == 1
        transition = transitions[0]
        assert transition.from_chapter == 1
        assert transition.to_chapter == 2
        assert "115" in transition.shared_characters
        assert transition.character_continuity == 1.0  # Karl appears in both chapters
        assert transition.thematic_continuity == 0.9  # Based on connection strength

    def test_generate_coreference_visualization_data(self):
        """Test coreference visualization data generation."""
        # Create mock character profiles
        mention = CharacterMention(
            chapter_number=1,
            sentence_id="1",
            global_sentence_id="1-1",
            mention_text="Karl",
            chain_id="115",
            grammatical_role="SUBJ",
            thematic_role="AGENT",
            sentence_position=0.1,
            narrative_importance=0.8,
        )

        profile = CharacterProfile(
            character_id="115",
            primary_name="Karl",
            alternative_names=["Herr Karl"],
            first_appearance_chapter=1,
            last_appearance_chapter=1,
            total_mentions=1,
            chapters_present=[1],
            mentions=[mention],
            narrative_prominence=0.8,
            character_consistency=0.9,
            cross_chapter_continuity=0.5,
            dialogue_frequency=0.3,
        )

        # Create mock cross-chapter connections
        cross_conn = CrossChapterConnection(
            chain_id="115",
            from_chapter=1,
            to_chapter=2,
            connection_type="coreference",
            strength=0.8,
            mentions_count=2,
            sentence_span=(1, 15),
        )

        with patch("logging.getLogger"):
            output_path = self.engine.generate_coreference_visualization_data(
                [], {"115": profile}, [cross_conn]
            )

        assert Path(output_path).exists()

        # Verify JSON content
        with open(output_path, encoding="utf-8") as f:
            data = json.load(f)

        assert "metadata" in data
        assert "nodes" in data
        assert "edges" in data
        assert "character_timelines" in data
        assert len(data["nodes"]) == 1
        assert len(data["edges"]) == 1
        assert data["nodes"][0]["id"] == "115"
        assert data["nodes"][0]["label"] == "Karl"

    def test_calculate_performance_metrics(self):
        """Test performance metrics calculation."""
        # Create mock processing stats
        processing_stats = {
            "processing_time_seconds": 10.5,
            "total_files": 3,
            "successful_parses": 3,
        }

        # Create mock chapter metadata
        chapters = [
            ChapterMetadata(
                chapter_number=i,
                chapter_id=f"chapter_{i}",
                source_file=f"chapter{i}.tsv",
                file_format="tsv",
                total_relationships=50,
                total_sentences=100,
                sentence_range=(1, 100),
                global_sentence_range=(1, 100),
                coreference_chains=5,
                processing_time=3.5,
                file_size_bytes=1024 * i,
            )
            for i in range(1, 4)
        ]

        # Create mock relationships
        relationships = []
        for i in range(150):  # 50 per chapter
            token = Token(
                idx=1,
                text="Karl",
                sentence_num=i % 100 + 1,
                grammatical_role="SUBJ",
                thematic_role="AGENT",
            )
            phrase = Phrase(
                text="Mann",
                coreference_id="115",
                start_idx=1,
                end_idx=1,
                grammatical_role="SUBJ",
                thematic_role="AGENT",
                coreference_type="PersPron[115]",
                animacy=MagicMock(),
                givenness="bekannt",
            )
            rel = ClauseMateRelationship(
                sentence_id=str(i),
                sentence_num=i % 100 + 1,
                pronoun=token,
                clause_mate=phrase,
                num_clause_mates=1,
                antecedent_info=MagicMock(),
                pronoun_coref_ids=["115"],
            )
            relationships.append(rel)

        with patch("logging.getLogger"):
            metrics = self.engine.calculate_performance_metrics(
                processing_stats, chapters, relationships
            )

        assert isinstance(metrics, PerformanceMetrics)
        assert metrics.total_processing_time == 10.5
        assert (
            metrics.relationships_per_second == 150 / 10.5
        )  # 150 relationships in 10.5 seconds
        assert len(metrics.per_chapter_times) == 3
        assert metrics.parser_success_rate == 1.0
        assert metrics.cross_chapter_detection_accuracy == 0.95

    def test_create_comprehensive_analysis_report(self):
        """Test comprehensive analysis report creation."""
        # Create mock character profiles
        mention = CharacterMention(
            chapter_number=1,
            sentence_id="1",
            global_sentence_id="1-1",
            mention_text="Karl",
            chain_id="115",
            grammatical_role="SUBJ",
            thematic_role="AGENT",
            sentence_position=0.1,
            narrative_importance=0.8,
        )

        profile = CharacterProfile(
            character_id="115",
            primary_name="Karl",
            alternative_names=[],
            first_appearance_chapter=1,
            last_appearance_chapter=1,
            total_mentions=1,
            chapters_present=[1],
            mentions=[mention],
            narrative_prominence=0.8,
            character_consistency=0.9,
            cross_chapter_continuity=0.5,
            dialogue_frequency=0.3,
        )

        # Create mock narrative segments
        segment = NarrativeFlowSegment(
            chapter_number=1,
            segment_start=1,
            segment_end=25,
            segment_type="introduction",
            character_density=0.5,
            coreference_density=0.3,
            narrative_tension=0.3,
            key_characters=["115"],
        )

        # Create mock transitions
        transition = CrossChapterTransition(
            from_chapter=1,
            to_chapter=2,
            character_continuity=0.8,
            thematic_continuity=0.7,
            temporal_gap_indicator=0.5,
            narrative_coherence=0.75,
            shared_characters=["115"],
            new_characters=[],
            dropped_characters=[],
        )

        # Create mock performance metrics
        metrics = PerformanceMetrics(
            total_processing_time=10.0,
            per_chapter_times={1: 5.0, 2: 5.0},
            memory_usage_peak=None,
            relationships_per_second=15.0,
            cross_chapter_resolution_time=2.0,
            parser_success_rate=1.0,
            cross_chapter_detection_accuracy=0.95,
            chain_resolution_completeness=0.9,
            processing_efficiency=15.0,
            memory_efficiency=0.0,
        )

        with patch("logging.getLogger"):
            output_path = self.engine.create_comprehensive_analysis_report(
                {"115": profile}, [segment], [transition], metrics
            )

        assert Path(output_path).exists()

        # Verify JSON content
        with open(output_path, encoding="utf-8") as f:
            report = json.load(f)

        assert "metadata" in report
        assert "executive_summary" in report
        assert "character_analysis" in report
        assert "narrative_analysis" in report
        assert "transition_analysis" in report
        assert "performance_analysis" in report
        assert "recommendations" in report

        assert report["executive_summary"]["total_characters"] == 1
        assert report["executive_summary"]["narrative_segments"] == 1
        assert report["executive_summary"]["chapter_transitions"] == 1

    def test_get_character_color(self):
        """Test character color assignment based on prominence."""
        # High prominence character
        profile1 = CharacterProfile(
            character_id="1",
            primary_name="Karl",
            alternative_names=[],
            first_appearance_chapter=1,
            last_appearance_chapter=1,
            total_mentions=50,
            chapters_present=[1],
            mentions=[],
            narrative_prominence=0.9,
            character_consistency=0.8,
            cross_chapter_continuity=0.7,
            dialogue_frequency=0.5,
        )

        # Medium prominence character
        profile2 = CharacterProfile(
            character_id="2",
            primary_name="Anna",
            alternative_names=[],
            first_appearance_chapter=1,
            last_appearance_chapter=1,
            total_mentions=20,
            chapters_present=[1],
            mentions=[],
            narrative_prominence=0.6,
            character_consistency=0.8,
            cross_chapter_continuity=0.7,
            dialogue_frequency=0.5,
        )

        # Low prominence character
        profile3 = CharacterProfile(
            character_id="3",
            primary_name="Diener",
            alternative_names=[],
            first_appearance_chapter=1,
            last_appearance_chapter=1,
            total_mentions=5,
            chapters_present=[1],
            mentions=[],
            narrative_prominence=0.1,
            character_consistency=0.8,
            cross_chapter_continuity=0.7,
            dialogue_frequency=0.5,
        )

        assert self.engine._get_character_color(profile1) == "#FF6B6B"  # Red for major
        assert (
            self.engine._get_character_color(profile2) == "#4ECDC4"
        )  # Teal for important
        assert (
            self.engine._get_character_color(profile3) == "#96CEB4"
        )  # Green for background

    def test_calculate_character_statistics(self):
        """Test character statistics calculation."""
        # Create mock profiles
        profiles = {
            "1": CharacterProfile(
                character_id="1",
                primary_name="Karl",
                alternative_names=[],
                first_appearance_chapter=1,
                last_appearance_chapter=1,
                total_mentions=50,
                chapters_present=[1],
                mentions=[],
                narrative_prominence=0.9,
                character_consistency=0.8,
                cross_chapter_continuity=0.7,
                dialogue_frequency=0.5,
            ),
            "2": CharacterProfile(
                character_id="2",
                primary_name="Anna",
                alternative_names=[],
                first_appearance_chapter=1,
                last_appearance_chapter=2,
                total_mentions=30,
                chapters_present=[1, 2],
                mentions=[],
                narrative_prominence=0.6,
                character_consistency=0.9,
                cross_chapter_continuity=0.8,
                dialogue_frequency=0.3,
            ),
            "3": CharacterProfile(
                character_id="3",
                primary_name="Diener",
                alternative_names=[],
                first_appearance_chapter=1,
                last_appearance_chapter=1,
                total_mentions=5,
                chapters_present=[1],
                mentions=[],
                narrative_prominence=0.1,
                character_consistency=0.7,
                cross_chapter_continuity=0.2,
                dialogue_frequency=0.1,
            ),
        }

        stats = self.engine._calculate_character_statistics(profiles)

        assert stats["total_characters"] == 3
        assert stats["major_characters"] == 1  # Karl with prominence > 0.8
        assert stats["minor_characters"] == 1  # Diener with prominence <= 0.2
        assert stats["cross_chapter_characters"] == 1  # Anna appears in 2 chapters
        assert 0.5 < stats["average_prominence"] < 0.6  # Average of 0.9, 0.6, 0.1
        assert 0.5 < stats["average_continuity"] < 0.6  # Average of 0.7, 0.8, 0.2

    def test_calculate_narrative_statistics(self):
        """Test narrative statistics calculation."""
        segments = [
            NarrativeFlowSegment(
                chapter_number=1,
                segment_start=1,
                segment_end=25,
                segment_type="introduction",
                character_density=0.5,
                coreference_density=0.3,
                narrative_tension=0.3,
                key_characters=["1"],
            ),
            NarrativeFlowSegment(
                chapter_number=1,
                segment_start=26,
                segment_end=50,
                segment_type="development",
                character_density=0.7,
                coreference_density=0.5,
                narrative_tension=0.6,
                key_characters=["1", "2"],
            ),
            NarrativeFlowSegment(
                chapter_number=1,
                segment_start=51,
                segment_end=75,
                segment_type="climax",
                character_density=0.9,
                coreference_density=0.8,
                narrative_tension=1.0,
                key_characters=["1", "2", "3"],
            ),
            NarrativeFlowSegment(
                chapter_number=1,
                segment_start=76,
                segment_end=100,
                segment_type="resolution",
                character_density=0.4,
                coreference_density=0.2,
                narrative_tension=0.4,
                key_characters=["1"],
            ),
        ]

        stats = self.engine._calculate_narrative_statistics(segments)

        assert stats["total_segments"] == 4
        assert stats["climax_segments"] == 1
        assert stats["development_segments"] == 1
        assert 0.6 < stats["average_character_density"] < 0.7  # Average of densities
        assert 0.5 < stats["average_narrative_tension"] < 0.6  # Average of tensions

    def test_calculate_transition_statistics(self):
        """Test transition statistics calculation."""
        transitions = [
            CrossChapterTransition(
                from_chapter=1,
                to_chapter=2,
                character_continuity=0.8,
                thematic_continuity=0.7,
                temporal_gap_indicator=0.5,
                narrative_coherence=0.75,
                shared_characters=["1", "2"],
                new_characters=["3"],
                dropped_characters=[],
            ),
            CrossChapterTransition(
                from_chapter=2,
                to_chapter=3,
                character_continuity=0.3,
                thematic_continuity=0.2,
                temporal_gap_indicator=0.8,
                narrative_coherence=0.25,
                shared_characters=["2"],
                new_characters=["4", "5"],
                dropped_characters=["1"],
            ),
        ]

        stats = self.engine._calculate_transition_statistics(transitions)

        assert stats["total_transitions"] == 2
        assert stats["strong_transitions"] == 1  # First transition has coherence > 0.7
        assert stats["weak_transitions"] == 1  # Second transition has coherence < 0.3
        assert (
            0.5 < stats["average_character_continuity"] < 0.6
        )  # Average of 0.8 and 0.3
        assert (
            0.4 < stats["average_narrative_coherence"] <= 0.5
        )  # Average of 0.75 and 0.25

    def test_generate_analysis_recommendations(self):
        """Test analysis recommendations generation."""
        # Create mock profiles with few major characters
        profiles = {
            "1": CharacterProfile(
                character_id="1",
                primary_name="Karl",
                alternative_names=[],
                first_appearance_chapter=1,
                last_appearance_chapter=1,
                total_mentions=10,
                chapters_present=[1],
                mentions=[],
                narrative_prominence=0.9,
                character_consistency=0.8,
                cross_chapter_continuity=0.7,
                dialogue_frequency=0.5,
            ),
            "2": CharacterProfile(
                character_id="2",
                primary_name="Anna",
                alternative_names=[],
                first_appearance_chapter=1,
                last_appearance_chapter=1,
                total_mentions=8,
                chapters_present=[1],
                mentions=[],
                narrative_prominence=0.4,
                character_consistency=0.8,
                cross_chapter_continuity=0.7,
                dialogue_frequency=0.5,
            ),
        }

        # Create mock segments with low tension
        segments = [
            NarrativeFlowSegment(
                chapter_number=1,
                segment_start=1,
                segment_end=50,
                segment_type="development",
                character_density=0.5,
                coreference_density=0.3,
                narrative_tension=0.2,  # Low tension
                key_characters=["1"],
            ),
        ]

        # Create mock transitions with weak coherence
        transitions = [
            CrossChapterTransition(
                from_chapter=1,
                to_chapter=2,
                character_continuity=0.2,
                thematic_continuity=0.1,
                temporal_gap_indicator=0.5,
                narrative_coherence=0.15,  # Weak coherence
                shared_characters=[],
                new_characters=["3"],
                dropped_characters=["1"],
            ),
        ]

        # Create mock performance metrics with low RPS
        metrics = PerformanceMetrics(
            total_processing_time=100.0,
            per_chapter_times={1: 50.0, 2: 50.0},
            memory_usage_peak=None,
            relationships_per_second=50.0,  # Low RPS
            cross_chapter_resolution_time=10.0,
            parser_success_rate=1.0,
            cross_chapter_detection_accuracy=0.95,
            chain_resolution_completeness=0.9,
            processing_efficiency=50.0,
            memory_efficiency=0.0,
        )

        recommendations = self.engine._generate_analysis_recommendations(
            profiles, segments, transitions, metrics
        )

        assert len(recommendations) == 4
        recommendation_texts = [rec.lower() for rec in recommendations]

        # Check that all expected recommendations are present
        assert any("major characters" in text for text in recommendation_texts)
        assert any("narrative tension" in text for text in recommendation_texts)
        assert any("character continuity" in text for text in recommendation_texts)
        assert any("optimizing processing" in text for text in recommendation_texts)
