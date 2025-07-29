#!/usr/bin/env python3
"""Generate Comprehensive Visualizations and Reports.

This script creates all the visualization and reporting features requested:
- Cross-chapter coreference chain visualization
- Interactive relationship network graphs
- Chapter-by-chapter analysis reports
- Comparative analysis dashboards

Author: Kilo Code
Version: 3.1 - Visualization and Reporting Implementation
Date: 2025-07-28
"""

import csv
import json
import logging
import sys
from datetime import datetime
from pathlib import Path

# Add src to path for imports
sys.path.append("src")

import contextlib

from visualization.interactive_visualizer import InteractiveVisualizer


def setup_logging() -> logging.Logger:
    """Set up logging configuration."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler("visualization_generation.log"),
            logging.StreamHandler(sys.stdout),
        ],
    )
    return logging.getLogger(__name__)


def load_analysis_data(analysis_dir: str) -> tuple:
    """Load analysis data from the latest output directory.

    Args:
        analysis_dir: Path to analysis output directory

    Returns:
        Tuple of (relationships_data, cross_chapter_chains, processing_stats)
    """
    logger = logging.getLogger(__name__)
    analysis_path = Path(analysis_dir)

    # Load cross-chapter chains
    chains_file = analysis_path / "cross_chapter_chains.json"
    with open(chains_file, encoding="utf-8") as f:
        cross_chapter_chains = json.load(f)

    # Load processing statistics
    stats_file = analysis_path / "processing_statistics.json"
    with open(stats_file, encoding="utf-8") as f:
        processing_stats = json.load(f)

    # Load relationships data from CSV
    relationships_data = []
    csv_file = analysis_path / "unified_relationships.csv"

    with open(csv_file, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Convert numeric fields
            for field in ["chapter_number", "sentence_num", "pronoun_token_idx"]:
                if field in row and row[field]:
                    with contextlib.suppress(ValueError):
                        row[field] = int(row[field])

            # Convert boolean fields
            if "cross_chapter" in row:
                row["cross_chapter_relationship"] = (
                    row["cross_chapter"].lower() == "true"
                )

            relationships_data.append(row)

    logger.info(f"Loaded {len(relationships_data)} relationships from {csv_file}")
    logger.info(f"Loaded {len(cross_chapter_chains)} cross-chapter chains")

    return relationships_data, cross_chapter_chains, processing_stats


def main():
    """Main execution function."""
    logger = setup_logging()
    logger.info("Starting comprehensive visualization generation")

    # Configuration
    analysis_dir = "data/output/unified_analysis_20250728_231555"  # Latest analysis
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = f"data/output/visualizations_{timestamp}"

    try:
        # Load analysis data
        logger.info("Loading analysis data...")
        relationships_data, cross_chapter_chains, processing_stats = load_analysis_data(
            analysis_dir
        )

        # Initialize visualizer
        logger.info("Initializing interactive visualizer...")
        visualizer = InteractiveVisualizer(output_dir)

        # Generate visualizations
        logger.info("Generating cross-chapter network visualization...")
        network_path = visualizer.create_cross_chapter_network_visualization(
            cross_chapter_chains=cross_chapter_chains,
            relationships_data=relationships_data,
        )
        logger.info(f"✅ Network visualization created: {network_path}")

        logger.info("Generating chapter analysis reports...")
        reports_path = visualizer.create_chapter_analysis_reports(
            relationships_data=relationships_data, processing_stats=processing_stats
        )
        logger.info(f"✅ Chapter reports created: {reports_path}")

        logger.info("Generating comparative dashboard...")
        dashboard_path = visualizer.create_comparative_dashboard(
            relationships_data=relationships_data,
            cross_chapter_chains=cross_chapter_chains,
            processing_stats=processing_stats,
        )
        logger.info(f"✅ Comparative dashboard created: {dashboard_path}")

        # Generate summary report
        logger.info("Creating visualization summary...")
        summary_path = create_visualization_summary(
            output_dir,
            network_path,
            reports_path,
            dashboard_path,
            len(relationships_data),
            len(cross_chapter_chains),
            processing_stats,
        )
        logger.info(f"✅ Summary report created: {summary_path}")

        # Final summary
        logger.info("=" * 60)
        logger.info("VISUALIZATION GENERATION COMPLETE")
        logger.info("=" * 60)
        logger.info(f"Output Directory: {output_dir}")
        logger.info("Generated Files:")
        logger.info(f"  • Cross-Chapter Network: {Path(network_path).name}")
        logger.info(f"  • Chapter Reports: {Path(reports_path).name}")
        logger.info(f"  • Comparative Dashboard: {Path(dashboard_path).name}")
        logger.info(f"  • Summary Report: {Path(summary_path).name}")

        logger.info("\nVisualization Features Implemented:")
        logger.info("✅ Cross-chapter coreference chain visualization")
        logger.info("✅ Interactive relationship network graphs")
        logger.info("✅ Chapter-by-chapter analysis reports")
        logger.info("✅ Comparative analysis dashboards")

        return 0

    except Exception as e:
        logger.error(f"Visualization generation failed: {str(e)}")
        import traceback

        logger.error(f"Traceback: {traceback.format_exc()}")
        return 1


def create_visualization_summary(
    output_dir: str,
    network_path: str,
    reports_path: str,
    dashboard_path: str,
    total_relationships: int,
    total_chains: int,
    processing_stats: dict,
) -> str:
    """Create a summary report of all generated visualizations.

    Args:
        output_dir: Output directory path
        network_path: Path to network visualization
        reports_path: Path to chapter reports
        dashboard_path: Path to comparative dashboard
        total_relationships: Total number of relationships
        total_chains: Total number of cross-chapter chains
        processing_stats: Processing statistics

    Returns:
        Path to created summary file
    """
    summary_path = Path(output_dir) / "visualization_summary.html"

    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Multi-File Clause Mates Analysis - Visualization Summary</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; background-color: #f5f5f5; }}
            .container {{ max-width: 1000px; margin: 0 auto; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
            .header {{ text-align: center; margin-bottom: 40px; }}
            .header h1 {{ color: #2c3e50; margin-bottom: 10px; }}
            .header p {{ color: #7f8c8d; font-size: 1.1em; }}
            .stats-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin: 30px 0; }}
            .stat-card {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 8px; text-align: center; }}
            .stat-value {{ font-size: 2.5em; font-weight: bold; margin-bottom: 5px; }}
            .stat-label {{ font-size: 0.9em; opacity: 0.9; }}
            .visualization-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 25px; margin: 30px 0; }}
            .viz-card {{ background: #f8f9fa; border: 1px solid #dee2e6; border-radius: 8px; overflow: hidden; transition: transform 0.2s; }}
            .viz-card:hover {{ transform: translateY(-5px); box-shadow: 0 4px 15px rgba(0,0,0,0.1); }}
            .viz-header {{ background: #343a40; color: white; padding: 15px; }}
            .viz-header h3 {{ margin: 0; font-size: 1.2em; }}
            .viz-content {{ padding: 20px; }}
            .viz-description {{ color: #6c757d; margin-bottom: 15px; line-height: 1.5; }}
            .viz-link {{ display: inline-block; background: #007bff; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; transition: background 0.2s; }}
            .viz-link:hover {{ background: #0056b3; }}
            .features-list {{ background: #e8f5e8; padding: 20px; border-radius: 8px; margin: 20px 0; }}
            .features-list h3 {{ color: #155724; margin-top: 0; }}
            .features-list ul {{ margin: 10px 0; }}
            .features-list li {{ margin: 5px 0; color: #155724; }}
            .tech-info {{ background: #f8f9fa; padding: 20px; border-radius: 8px; margin: 20px 0; border-left: 4px solid #007bff; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>Multi-File Clause Mates Analysis</h1>
                <h2>Interactive Visualizations & Reports</h2>
                <p>Comprehensive visualization suite for cross-chapter coreference analysis</p>
                <p><strong>Generated:</strong> {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
            </div>

            <div class="stats-grid">
                <div class="stat-card">
                    <div class="stat-value">{total_relationships:,}</div>
                    <div class="stat-label">Total Relationships</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">{total_chains}</div>
                    <div class="stat-label">Cross-Chapter Chains</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">{processing_stats.get("total_chapters", 0)}</div>
                    <div class="stat-label">Chapters Analyzed</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">{processing_stats.get("processing_time_seconds", 0):.1f}s</div>
                    <div class="stat-label">Processing Time</div>
                </div>
            </div>

            <div class="visualization-grid">
                <div class="viz-card">
                    <div class="viz-header">
                        <h3>🕸️ Cross-Chapter Network</h3>
                    </div>
                    <div class="viz-content">
                        <div class="viz-description">
                            Interactive network visualization showing coreference chains that span across multiple chapters.
                            Features clickable nodes, dynamic layout, and detailed chain information.
                        </div>
                        <a href="{Path(network_path).name}" class="viz-link">Open Network Visualization</a>
                    </div>
                </div>

                <div class="viz-card">
                    <div class="viz-header">
                        <h3>📊 Chapter Analysis Reports</h3>
                    </div>
                    <div class="viz-content">
                        <div class="viz-description">
                            Comprehensive chapter-by-chapter analysis with detailed statistics, density metrics,
                            and comparative charts showing relationships, pronouns, and cross-chapter links.
                        </div>
                        <a href="{Path(reports_path).name}" class="viz-link">View Chapter Reports</a>
                    </div>
                </div>

                <div class="viz-card">
                    <div class="viz-header">
                        <h3>📈 Comparative Dashboard</h3>
                    </div>
                    <div class="viz-content">
                        <div class="viz-description">
                            Advanced comparative analysis dashboard with pronoun type distribution,
                            connectivity metrics, performance statistics, and cross-chapter comparison matrix.
                        </div>
                        <a href="{Path(dashboard_path).name}" class="viz-link">Open Dashboard</a>
                    </div>
                </div>
            </div>

            <div class="features-list">
                <h3>✅ Implemented Visualization Features</h3>
                <ul>
                    <li><strong>Cross-chapter coreference chain visualization</strong> - Interactive network graphs showing relationships between chapters</li>
                    <li><strong>Interactive relationship network graphs</strong> - Dynamic, clickable visualizations with detailed information</li>
                    <li><strong>Chapter-by-chapter analysis reports</strong> - Comprehensive statistics and metrics for each chapter</li>
                    <li><strong>Comparative analysis dashboards</strong> - Advanced analytics comparing patterns across chapters</li>
                </ul>
            </div>

            <div class="tech-info">
                <h3>🔧 Technical Implementation</h3>
                <p><strong>Technologies Used:</strong></p>
                <ul>
                    <li>HTML5 Canvas for custom charts and visualizations</li>
                    <li>Vis.js Network for interactive network graphs</li>
                    <li>D3.js for advanced data visualization capabilities</li>
                    <li>Responsive CSS Grid for adaptive layouts</li>
                    <li>JavaScript for interactive functionality</li>
                </ul>

                <p><strong>Data Sources:</strong></p>
                <ul>
                    <li>Unified relationships CSV ({total_relationships:,} relationships)</li>
                    <li>Cross-chapter chains JSON ({total_chains} chains)</li>
                    <li>Processing statistics and metadata</li>
                </ul>
            </div>

            <div style="text-align: center; margin-top: 40px; padding-top: 20px; border-top: 1px solid #dee2e6;">
                <p style="color: #6c757d;">
                    Multi-File Clause Mates Analysis System v3.1<br>
                    Enhanced with Interactive Visualizations & Reporting
                </p>
            </div>
        </div>
    </body>
    </html>
    """

    with open(summary_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    return str(summary_path)


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
