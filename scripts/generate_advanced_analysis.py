#!/usr/bin/env python3
"""Generate Advanced Analysis Files for Multi-File Clause Mates Analysis.

This script runs the advanced analysis engine to generate the missing
advanced analysis files including character tracking, narrative flow analysis,
and comprehensive reports.
"""

import csv
import json
import sys
from pathlib import Path

# Add src to path
sys.path.append("src")

from src.data.models import (
    AnimacyType,
    AntecedentInfo,
    ClauseMateRelationship,
    Phrase,
    Token,
)
from src.multi_file.advanced_analysis_features import AdvancedAnalysisEngine
from src.multi_file.enhanced_output_system import (
    ChapterMetadata,
    CrossChapterConnection,
)


def load_existing_data():
    """Load existing analysis data from the unified output directory.

    Returns:
        Tuple containing processing statistics, cross-chapter chains, and relationships.
    """
    output_dir = "data/output/unified_analysis_20250728_231555"

    # Load processing statistics
    stats_file = Path(output_dir) / "processing_statistics.json"
    with open(stats_file, encoding="utf-8") as f:
        processing_stats = json.load(f)

    # Load cross-chapter chains
    chains_file = Path(output_dir) / "cross_chapter_chains.json"
    with open(chains_file, encoding="utf-8") as f:
        cross_chapter_chains = json.load(f)

    # Load unified relationships
    relationships_file = Path(output_dir) / "unified_relationships.csv"
    relationships = []

    with open(relationships_file, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Create ClauseMateRelationship objects from CSV data
            pronoun = Token(
                idx=int(row.get("pronoun_token_idx", 1)),
                text=row["pronoun_text"],
                sentence_num=int(row["sentence_num"]),
                grammatical_role=row["pronoun_grammatical_role"],
                thematic_role=row["pronoun_thematic_role"],
                coreference_link=row.get("pronoun_coreference_link"),
                coreference_type=row.get("pronoun_coreference_type"),
                inanimate_coreference_link=row.get(
                    "pronoun_inanimate_coreference_link"
                ),
                inanimate_coreference_type=row.get(
                    "pronoun_inanimate_coreference_type"
                ),
                is_critical_pronoun=True,
            )

            clause_mate = Phrase(
                text=row["clause_mate_text"],
                coreference_id=row.get("clause_mate_coref_id", ""),
                start_idx=int(row.get("clause_mate_start_idx", 1)),
                end_idx=int(row.get("clause_mate_end_idx", 1)),
                grammatical_role=row["clause_mate_grammatical_role"],
                thematic_role=row["clause_mate_thematic_role"],
                coreference_type=row.get("clause_mate_coreference_type", ""),
                animacy=AnimacyType.ANIMATE
                if row.get("clause_mate_animacy") == "anim"
                else AnimacyType.INANIMATE,
                givenness=row.get("clause_mate_givenness", ""),
            )

            # Parse coreference IDs
            pronoun_coref_ids = []
            if row.get("pronoun_coref_ids"):
                try:
                    # Handle different formats: ['95-145'] or 95-145
                    coref_str = row["pronoun_coref_ids"].strip("[]'\"")
                    if coref_str:
                        pronoun_coref_ids = [coref_str]
                except Exception:
                    pass

            # Fill required fields for ClauseMateRelationship
            relationship = ClauseMateRelationship(
                sentence_id=row["sentence_id"],
                sentence_num=int(row["sentence_num"]),
                pronoun=pronoun,
                clause_mate=clause_mate,
                num_clause_mates=int(row.get("num_clause_mates", 1)),
                antecedent_info=AntecedentInfo(
                    most_recent_text=row.get("pronoun_most_recent_antecedent_text", ""),
                    most_recent_distance=row.get(
                        "pronoun_most_recent_antecedent_distance", ""
                    ),
                    first_text=row.get("pronoun_first_antecedent_text", ""),
                    first_distance=row.get("pronoun_first_antecedent_distance", ""),
                    sentence_id=row["sentence_id"],
                    choice_count=int(row.get("pronoun_antecedent_choice", 0)),
                ),
                first_words=row.get("first_words", ""),
                pronoun_coref_ids=pronoun_coref_ids,
                pronoun_coref_base_num=None,
                pronoun_coref_occurrence_num=None,
                clause_mate_coref_base_num=None,
                clause_mate_coref_occurrence_num=None,
                pronoun_coref_link_base_num=None,
                pronoun_coref_link_occurrence_num=None,
                pronoun_inanimate_coref_link_base_num=None,
                pronoun_inanimate_coref_link_occurrence_num=None,
            )
            relationships.append(relationship)

    return processing_stats, cross_chapter_chains, relationships


def create_chapter_metadata(relationships):
    """Create chapter metadata from relationships.

    Args:
        relationships: List of ClauseMateRelationship objects.

    Returns:
        List of ChapterMetadata objects.
    """
    chapters = {}

    for rel in relationships:
        chapter_num = rel.chapter_number
        if chapter_num not in chapters:
            chapters[chapter_num] = {
                "sentences": set(),
                "relationships": 0,
                "cross_chapter_relationships": 0,
            }

        chapters[chapter_num]["sentences"].add(rel.sentence_num)
        chapters[chapter_num]["relationships"] += 1
        if rel.is_cross_chapter:
            chapters[chapter_num]["cross_chapter_relationships"] += 1

    metadata = []
    for chapter_num in sorted(chapters.keys()):
        data = chapters[chapter_num]
        sentences = sorted(data["sentences"])

        meta = ChapterMetadata(
            chapter_number=chapter_num,
            chapter_id=f"chapter_{chapter_num}",
            source_file=(
                f"data/input/gotofiles/{'later/' if chapter_num != 2 else ''}"
                f"{chapter_num}.tsv"
            ),
            file_format="tsv",
            total_relationships=data["relationships"],
            total_sentences=len(sentences),
            sentence_range=(sentences[0], sentences[-1]) if sentences else (0, 0),
            global_sentence_range=(sentences[0], sentences[-1])
            if sentences
            else (0, 0),
            coreference_chains=0,  # Placeholder
            processing_time=1.0,  # Placeholder
            file_size_bytes=0,  # Placeholder
            encoding="utf-8",
        )
        metadata.append(meta)

    return metadata


def create_cross_chapter_connections(cross_chapter_chains):
    """Create cross-chapter connections from chains data.

    Args:
        cross_chapter_chains: Dictionary of cross-chapter chains.

    Returns:
        List of CrossChapterConnection objects.
    """
    connections = []

    for chain_name, terms in cross_chapter_chains.items():
        if len(terms) >= 2:  # Only chains with multiple terms
            # Create connections between consecutive chapters
            for i in range(len(terms) - 1):
                connection = CrossChapterConnection(
                    chain_id=chain_name,
                    from_chapter=i + 1,
                    to_chapter=i + 2,
                    connection_type="coreference",
                    strength=0.8,
                    mentions_count=2,
                    sentence_span=(0, 0),
                )
                connections.append(connection)

    return connections


def main():
    """Main function to generate advanced analysis files.

    Loads existing data, creates metadata, runs advanced analysis, and prints summary.
    """
    print("🔍 Loading existing analysis data...")
    processing_stats, cross_chapter_chains, relationships = load_existing_data()

    print(
        f"📊 Loaded {len(relationships)} relationships and "
        f"{len(cross_chapter_chains)} cross-chapter chains"
    )

    # Create metadata and connections
    chapter_metadata = create_chapter_metadata(relationships)
    cross_chapter_connections = create_cross_chapter_connections(cross_chapter_chains)

    print(f"📚 Created metadata for {len(chapter_metadata)} chapters")
    print(f"🔗 Created {len(cross_chapter_connections)} cross-chapter connections")

    # Initialize advanced analysis engine
    output_dir = "data/output/unified_analysis_20250728_231555"
    engine = AdvancedAnalysisEngine(output_dir)

    print("🚀 Starting advanced analysis...")

    # 1. Character Tracking Analysis
    print("👥 Analyzing character tracking...")
    character_profiles = engine.analyze_character_tracking(
        relationships, chapter_metadata, cross_chapter_connections
    )

    # 2. Narrative Flow Analysis
    print("📖 Analyzing narrative flow...")
    narrative_segments = engine.analyze_narrative_flow(
        relationships, chapter_metadata, character_profiles
    )

    # 3. Cross-Chapter Transitions
    print("🔄 Analyzing cross-chapter transitions...")
    transitions = engine.analyze_cross_chapter_transitions(
        chapter_metadata, character_profiles, cross_chapter_connections
    )

    # 4. Performance Metrics
    print("⚡ Calculating performance metrics...")
    performance_metrics = engine.calculate_performance_metrics(
        processing_stats, chapter_metadata, relationships
    )

    # 5. Generate Visualization Data
    print("📊 Generating coreference visualization data...")
    viz_file = engine.generate_coreference_visualization_data(
        relationships, character_profiles, cross_chapter_connections
    )

    # 6. Create Comprehensive Report
    print("📋 Creating comprehensive analysis report...")
    report_file = engine.create_comprehensive_analysis_report(
        character_profiles, narrative_segments, transitions, performance_metrics
    )

    print("\n✅ Advanced analysis complete!")
    print(f"📁 Generated files in: {output_dir}")
    print(f"   - Character profiles: {len(character_profiles)} characters")
    print(f"   - Narrative segments: {len(narrative_segments)} segments")
    print(f"   - Chapter transitions: {len(transitions)} transitions")
    print(f"   - Visualization data: {viz_file}")
    print(f"   - Comprehensive report: {report_file}")

    # Create summary of key findings
    print("\n🔍 Key Findings:")
    major_characters = sum(
        1 for p in character_profiles.values() if p.narrative_prominence > 0.8
    )
    cross_chapter_chars = sum(
        1 for p in character_profiles.values() if len(p.chapters_present) > 1
    )
    avg_coherence = (
        sum(t.narrative_coherence for t in transitions) / len(transitions)
        if transitions
        else 0
    )

    print(f"   - Major characters: {major_characters}")
    print(f"   - Cross-chapter characters: {cross_chapter_chars}")
    print(f"   - Average narrative coherence: {avg_coherence:.2f}")
    print(
        f"   - Processing rate: {performance_metrics.relationships_per_second:.1f} "
        f"relationships/second"
    )


if __name__ == "__main__":
    main()
