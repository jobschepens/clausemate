#!/usr/bin/env python3
"""Multi-File Clause Mates Analysis Runner.

This script provides a command-line interface for running unified multi-file
analysis across all chapter files using the Phase 3.1 implementation.

Based on definitive evidence showing 8,723 cross-chapter connections and
245 same chain ID matches across sequential book chapters.

Author: Kilo Code
Version: 3.1 - Phase 3.1 Integration
Date: 2025-07-28
"""

import argparse
import json
import logging
import sys
from datetime import datetime
from pathlib import Path

# Add project root to Python path for imports
project_root = Path(__file__).resolve().parents[1]
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

try:
    from src.multi_file.multi_file_batch_processor import MultiFileBatchProcessor
except ImportError as e:
    print(f"❌ Import error: {e}")
    print(f"Project root: {project_root}")
    print("Try running: pip install -e . from the project root")
    sys.exit(1)


def setup_logging(verbose: bool = False) -> None:
    """Set up logging configuration."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler("multi_file_analysis.log"),
        ],
    )


def save_unified_results(result, output_dir: Path) -> None:
    """Save unified processing results to files."""
    # Create timestamped output directory
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    unified_output_dir = output_dir / f"unified_analysis_{timestamp}"
    unified_output_dir.mkdir(parents=True, exist_ok=True)

    # Save unified relationships as CSV
    relationships_file = unified_output_dir / "unified_relationships.csv"
    with open(relationships_file, "w", encoding="utf-8", newline="") as f:
        import csv

        writer = csv.writer(f)

        # Import the standardized column order from config
        try:
            from src.config import ExportColumns
            standard_columns = ExportColumns.STANDARD_ORDER
        except ImportError:
            # Fallback if config import fails - use basic column order
            standard_columns = [
                "sentence_id", "pronoun_text", "pronoun_token_idx", "pronoun_start_idx",
                "pronoun_end_idx", "clause_mate_text", "clause_mate_start_idx", "clause_mate_end_idx",
                "relationship_type", "distance", "sentence_text", "layer"
            ]

        # Write header using standardized column order plus multi-file specific columns
        multi_file_columns = [
            "chapter_file",
            "chapter_number",
            "chapter_id",
            "global_sentence_id",
            "cross_chapter",
            "source_file_path",
        ]

        # Combine standardized columns with multi-file specific columns
        header_columns = multi_file_columns + standard_columns
        writer.writerow(header_columns)

        # Write relationships
        for rel in result.unified_relationships:
            # Extract just the filename for clearer chapter identification
            from pathlib import Path

            chapter_file = Path(rel.source_file).name
            chapter_id = f"Chapter_{rel.chapter_number}"

            # Create multi-file specific data
            multi_file_data = {
                "chapter_file": chapter_file,
                "chapter_number": rel.chapter_number,
                "chapter_id": chapter_id,
                "global_sentence_id": rel.global_sentence_id,
                "cross_chapter": rel.cross_chapter_relationship,
                "source_file_path": rel.source_file,
            }

            # Get standardized relationship data (this should be a ClauseMateRelationship object)
            if hasattr(rel, "to_dict"):
                standard_data = rel.to_dict()
            else:
                # Fallback: create basic data structure if to_dict not available
                standard_data = dict.fromkeys(standard_columns, "")
                # Fill in what we can from the unified relationship
                if hasattr(rel, "sentence_id"):
                    standard_data["sentence_id"] = rel.sentence_id
                if hasattr(rel, "pronoun") and rel.pronoun:
                    standard_data["pronoun_text"] = rel.pronoun.text
                    standard_data["pronoun_token_idx"] = rel.pronoun.idx
                if hasattr(rel, "clause_mate") and rel.clause_mate:
                    standard_data["clause_mate_text"] = rel.clause_mate.text
                    standard_data["clause_mate_start_idx"] = rel.clause_mate.start_idx
                    standard_data["clause_mate_end_idx"] = rel.clause_mate.end_idx

            # Combine multi-file data with standard data
            row_data = []
            for col in header_columns:
                if col in multi_file_data:
                    row_data.append(multi_file_data[col])
                elif col in standard_data:
                    row_data.append(standard_data[col])
                else:
                    row_data.append("")  # Empty value for missing columns

            writer.writerow(row_data)

    # Save processing statistics as JSON
    stats_file = unified_output_dir / "processing_statistics.json"
    with open(stats_file, "w", encoding="utf-8") as f:
        stats = {
            "processing_stats": result.processing_stats,
            "chapter_info": [
                {
                    "chapter_number": info.chapter_number,
                    "file_path": info.file_path,
                    "format_type": info.format_type,
                    "columns": info.columns,
                    "relationships_count": info.relationships_count,
                    "sentence_range": info.sentence_range,
                    "compatibility_score": info.compatibility_score,
                }
                for info in result.chapter_info
            ],
            "cross_chapter_chains": result.cross_chapter_chains,
            "success": result.success,
            "processing_time": result.processing_time,
        }
        json.dump(stats, f, indent=2, ensure_ascii=False)

    # Save cross-chapter chains as separate file
    chains_file = unified_output_dir / "cross_chapter_chains.json"
    with open(chains_file, "w", encoding="utf-8") as f:
        json.dump(result.cross_chapter_chains, f, indent=2, ensure_ascii=False)

    print(f"\nResults saved to: {unified_output_dir}")
    print(f"   - Unified relationships: {relationships_file}")
    print(f"   - Processing statistics: {stats_file}")
    print(f"   - Cross-chapter chains: {chains_file}")


def main():
    """Main entry point for multi-file analysis."""
    parser = argparse.ArgumentParser(
        description="Run unified multi-file clause mates analysis",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Process all chapters from default directory
  python run_multi_file_analysis.py

  # Process chapters from specific directory
  python run_multi_file_analysis.py --input data/input/gotofiles

  # Disable cross-chapter resolution
  python run_multi_file_analysis.py --no-cross-chapter

  # Enable verbose logging
  python run_multi_file_analysis.py --verbose

  # Custom output directory
  python run_multi_file_analysis.py --output results/custom
        """,
    )

    parser.add_argument(
        "--input",
        "-i",
        type=str,
        default="data/input/gotofiles",
        help="Input directory containing chapter files (default: data/input/gotofiles)",
    )

    parser.add_argument(
        "--output",
        "-o",
        type=str,
        default="data/output",
        help="Output directory for results (default: data/output)",
    )

    parser.add_argument(
        "--no-cross-chapter",
        action="store_true",
        help="Disable cross-chapter coreference resolution",
    )

    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Enable verbose logging"
    )

    parser.add_argument(
        "--summary-only",
        action="store_true",
        help="Show only summary statistics without detailed output",
    )

    args = parser.parse_args()

    # Setup logging
    setup_logging(args.verbose)
    logger = logging.getLogger(__name__)

    print("=" * 70)
    print("UNIFIED MULTI-FILE CLAUSE MATES ANALYSIS")
    print("=" * 70)
    print("Version: 3.1 - Phase 3.1 Integration")
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    try:
        # Initialize multi-file processor
        enable_cross_chapter = not args.no_cross_chapter
        processor = MultiFileBatchProcessor(
            enable_cross_chapter_resolution=enable_cross_chapter
        )

        print(f"Input directory: {args.input}")
        print(f"Output directory: {args.output}")
        cross_chapter_status = "Enabled" if enable_cross_chapter else "Disabled"
        print(f"Cross-chapter resolution: {cross_chapter_status}")
        print()

        # Process files
        logger.info("Starting unified multi-file analysis")
        result = processor.process_files(args.input)

        if not result.success:
            print(f"Processing failed: {result.error_message}")
            sys.exit(1)

        # Display results
        print("PROCESSING COMPLETED SUCCESSFULLY!")
        print()
        print("SUMMARY STATISTICS:")
        stats = result.processing_stats
        print(f"   - Total chapters processed: {stats['total_chapters']}")
        print(f"   - Total unified relationships: {stats['total_relationships']}")
        print(f"   - Cross-chapter chains: {stats['cross_chapter_chains']}")
        print(f"   - Processing time: {result.processing_time:.2f} seconds")
        print()

        if not args.summary_only:
            print("CHAPTER BREAKDOWN:")
            for info in result.chapter_info:
                print(
                    f"   - Chapter {info.chapter_number}: "
                    f"{info.relationships_count} relationships"
                )
                print(f"     File: {info.file_path}")
                print(f"     Format: {info.format_type} ({info.columns} columns)")
                print(
                    f"     Sentences: {info.sentence_range[0]}-{info.sentence_range[1]}"
                )
                print()

        # Save results
        output_dir = Path(args.output)
        save_unified_results(result, output_dir)

        print("Multi-file analysis complete!")

    except Exception as e:
        logger.error("Multi-file analysis failed: %s", str(e))
        print(f"❌ Error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
