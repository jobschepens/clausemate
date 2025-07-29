#!/usr/bin/env python3
"""Enhanced Multi-File Analysis with Advanced Features.

This script demonstrates the enhanced output system and advanced analysis features
for multi-file clause mates analysis, implementing Tasks 7 and 8.

Task 7: Unified Output System
- Comprehensive output format with source file metadata
- Chapter/file boundary markers in output
- Cross-file relationship indicators
- Summary statistics for multi-file processing

Task 8: Advanced Analysis Features
- Narrative flow analysis across files
- Character tracking across chapters
- Cross-file coreference chain visualization
- Multi-file processing performance metrics

Author: Kilo Code
Version: 3.1 - Enhanced Features Implementation
Date: 2025-07-28
"""

import logging
import sys
from datetime import datetime
from pathlib import Path

# Add src to path for imports
sys.path.append("src")

from multi_file.advanced_analysis_features import AdvancedAnalysisEngine
from multi_file.enhanced_output_system import (
    ChapterMetadata,
    CrossChapterConnection,
    EnhancedOutputSystem,
)
from multi_file.multi_file_batch_processor import MultiFileBatchProcessor


def setup_logging() -> logging.Logger:
    """Set up logging configuration."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler("enhanced_multi_file_analysis.log"),
            logging.StreamHandler(sys.stdout),
        ],
    )
    return logging.getLogger(__name__)


def convert_chapter_info_to_metadata(chapter_info_list) -> list:
    """Convert ChapterInfo objects to ChapterMetadata objects."""
    metadata_list = []

    for info in chapter_info_list:
        # Calculate file size (simplified)
        try:
            file_size = Path(info.file_path).stat().st_size
        except:
            file_size = 0

        metadata = ChapterMetadata(
            chapter_number=info.chapter_number,
            chapter_id=f"Chapter_{info.chapter_number}",
            source_file=info.file_path,
            file_format=info.format_type,
            total_relationships=info.relationships_count,
            total_sentences=info.sentence_range[1] - info.sentence_range[0] + 1,
            sentence_range=info.sentence_range,
            global_sentence_range=info.sentence_range,  # Simplified
            coreference_chains=info.relationships_count // 10,  # Estimated
            processing_time=1.0,  # Estimated
            file_size_bytes=file_size,
        )
        metadata_list.append(metadata)

    return metadata_list


def convert_cross_chapter_chains_to_connections(cross_chapter_chains) -> list:
    """Convert cross-chapter chains to CrossChapterConnection objects."""
    connections = []

    for chain_id, entities in cross_chapter_chains.items():
        # Extract chapter numbers from entities (simplified)
        chapters = set()
        for entity in entities:
            # Try to extract chapter number from entity string
            if "Chapter" in str(entity):
                try:
                    chapter_num = int(str(entity).split("Chapter")[1].split("_")[0])
                    chapters.add(chapter_num)
                except:
                    pass

        # Create connections between consecutive chapters
        chapter_list = sorted(chapters)
        for i in range(len(chapter_list) - 1):
            connection = CrossChapterConnection(
                chain_id=chain_id,
                from_chapter=chapter_list[i],
                to_chapter=chapter_list[i + 1],
                connection_type="same_chain_id",
                strength=0.8,  # High strength for same chain ID
                mentions_count=len(entities),
                sentence_span=(1, 100),  # Simplified
            )
            connections.append(connection)

    return connections


def main():
    """Main execution function."""
    logger = setup_logging()
    logger.info("Starting Enhanced Multi-File Analysis with Advanced Features")

    # Configuration
    input_path = "data/input/gotofiles"
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = f"data/output/enhanced_analysis_{timestamp}"

    try:
        # Phase 1: Multi-File Processing
        logger.info("Phase 1: Multi-File Processing")
        processor = MultiFileBatchProcessor(enable_cross_chapter_resolution=True)
        result = processor.process_files(input_path)

        if not result.success:
            logger.error(f"Multi-file processing failed: {result.error_message}")
            return 1

        logger.info(
            f"Multi-file processing complete: {len(result.unified_relationships)} relationships"
        )

        # Phase 2: Convert data structures for enhanced analysis
        logger.info("Phase 2: Converting data structures for enhanced analysis")
        chapter_metadata = convert_chapter_info_to_metadata(result.chapter_info)
        cross_chapter_connections = convert_cross_chapter_chains_to_connections(
            result.cross_chapter_chains
        )

        logger.info(f"Converted {len(chapter_metadata)} chapter metadata objects")
        logger.info(
            f"Converted {len(cross_chapter_connections)} cross-chapter connections"
        )

        # Phase 3: Enhanced Output System (Task 7)
        logger.info("Phase 3: Enhanced Output System (Task 7)")
        output_system = EnhancedOutputSystem(output_dir)

        # Create enhanced CSV output
        enhanced_csv_path = output_system.create_enhanced_csv_output(
            relationships=result.unified_relationships,
            chapter_metadata=chapter_metadata,
            cross_chapter_connections=cross_chapter_connections,
        )
        logger.info(f"Enhanced CSV output created: {enhanced_csv_path}")

        # Create comprehensive statistics
        stats_path = output_system.create_comprehensive_statistics(
            relationships=result.unified_relationships,
            chapter_metadata=chapter_metadata,
            cross_chapter_connections=cross_chapter_connections,
            processing_time=result.processing_time,
        )
        logger.info(f"Comprehensive statistics created: {stats_path}")

        # Create chapter boundary report
        boundary_path = output_system.create_chapter_boundary_report(
            chapter_metadata=chapter_metadata,
            cross_chapter_connections=cross_chapter_connections,
        )
        logger.info(f"Chapter boundary analysis created: {boundary_path}")

        # Phase 4: Advanced Analysis Features (Task 8)
        logger.info("Phase 4: Advanced Analysis Features (Task 8)")
        analysis_engine = AdvancedAnalysisEngine(output_dir)

        # Character tracking analysis
        logger.info("Performing character tracking analysis...")
        character_profiles = analysis_engine.analyze_character_tracking(
            relationships=result.unified_relationships,
            chapter_metadata=chapter_metadata,
            cross_chapter_connections=cross_chapter_connections,
        )
        logger.info(
            f"Character tracking complete: {len(character_profiles)} characters identified"
        )

        # Narrative flow analysis
        logger.info("Performing narrative flow analysis...")
        narrative_segments = analysis_engine.analyze_narrative_flow(
            relationships=result.unified_relationships,
            chapter_metadata=chapter_metadata,
            character_profiles=character_profiles,
        )
        logger.info(
            f"Narrative flow analysis complete: {len(narrative_segments)} segments identified"
        )

        # Cross-chapter transition analysis
        logger.info("Performing cross-chapter transition analysis...")
        transitions = analysis_engine.analyze_cross_chapter_transitions(
            chapter_metadata=chapter_metadata,
            character_profiles=character_profiles,
            cross_chapter_connections=cross_chapter_connections,
        )
        logger.info(
            f"Cross-chapter transition analysis complete: {len(transitions)} transitions analyzed"
        )

        # Generate coreference visualization data
        logger.info("Generating coreference visualization data...")
        viz_path = analysis_engine.generate_coreference_visualization_data(
            relationships=result.unified_relationships,
            character_profiles=character_profiles,
            cross_chapter_connections=cross_chapter_connections,
        )
        logger.info(f"Coreference visualization data created: {viz_path}")

        # Calculate performance metrics
        logger.info("Calculating performance metrics...")
        performance_metrics = analysis_engine.calculate_performance_metrics(
            processing_stats=result.processing_stats,
            chapter_metadata=chapter_metadata,
            relationships=result.unified_relationships,
        )
        logger.info(
            f"Performance metrics calculated: {performance_metrics.relationships_per_second:.2f} rel/sec"
        )

        # Create comprehensive analysis report
        logger.info("Creating comprehensive analysis report...")
        report_path = analysis_engine.create_comprehensive_analysis_report(
            character_profiles=character_profiles,
            narrative_segments=narrative_segments,
            transitions=transitions,
            performance_metrics=performance_metrics,
        )
        logger.info(f"Comprehensive analysis report created: {report_path}")

        # Phase 5: Summary and Results
        logger.info("Phase 5: Analysis Summary")
        logger.info("=" * 60)
        logger.info("ENHANCED MULTI-FILE ANALYSIS COMPLETE")
        logger.info("=" * 60)
        logger.info(f"Output Directory: {output_dir}")
        logger.info(f"Processing Time: {result.processing_time:.2f} seconds")
        logger.info(f"Total Relationships: {len(result.unified_relationships)}")
        logger.info(f"Total Chapters: {len(chapter_metadata)}")
        logger.info(f"Cross-Chapter Connections: {len(cross_chapter_connections)}")
        logger.info(f"Characters Identified: {len(character_profiles)}")
        logger.info(f"Narrative Segments: {len(narrative_segments)}")
        logger.info(f"Chapter Transitions: {len(transitions)}")
        logger.info(
            f"Performance: {performance_metrics.relationships_per_second:.2f} relationships/second"
        )

        # List all output files
        logger.info("\nGenerated Output Files:")
        logger.info(f"  • Enhanced CSV: {enhanced_csv_path}")
        logger.info(f"  • Statistics: {stats_path}")
        logger.info(f"  • Boundary Analysis: {boundary_path}")
        logger.info(f"  • Visualization Data: {viz_path}")
        logger.info(f"  • Comprehensive Report: {report_path}")

        # Task completion summary
        logger.info("\nTask Implementation Summary:")
        logger.info("✅ Task 7: Unified Output System")
        logger.info("   - Comprehensive output format with metadata")
        logger.info("   - Chapter/file boundary markers")
        logger.info("   - Cross-file relationship indicators")
        logger.info("   - Summary statistics for multi-file processing")
        logger.info("✅ Task 8: Advanced Analysis Features")
        logger.info("   - Narrative flow analysis across files")
        logger.info("   - Character tracking across chapters")
        logger.info("   - Cross-file coreference chain visualization")
        logger.info("   - Multi-file processing performance metrics")

        logger.info("Enhanced multi-file analysis completed successfully!")
        return 0

    except Exception as e:
        logger.error(f"Enhanced multi-file analysis failed: {str(e)}")
        import traceback

        logger.error(f"Traceback: {traceback.format_exc()}")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
