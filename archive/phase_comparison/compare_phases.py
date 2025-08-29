#!/usr/bin/env python3
"""Phase Comparison Script.

This script runs both Phase 1 and Phase 2 of the clause mate extraction system
and provides a comprehensive comparison of their outputs, performance, and features.

Usage:
    python compare_phases.py
"""

import json
import logging
import subprocess
import sys
import time
from pathlib import Path
from typing import Any, Dict, List

import pandas as pd

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class PhaseComparator:
    """Compare Phase 1 and Phase 2 outputs and performance."""

    def __init__(self):
        self.results = {
            'phase1': {},
            'phase2': {},
            'comparison': {}
        }

        # File paths
        self.phase1_script = "archive/phase1/clause_mates_complete.py"
        self.phase1_output = "data/output/clause_mates_phase1_export.csv"
        self.phase2_script = "src/main.py"
        self.phase2_output = "data/output/clause_mates_phase2_export.csv"
        self.python_exe = self._find_python_executable()

    def _find_python_executable(self) -> str:
        """Find the correct Python executable."""
        # Try the specific virtual environment first
        venv_python = "C:/global_venv/Scripts/python.exe"
        if Path(venv_python).exists():
            return venv_python
        return sys.executable

    def run_phase1(self) -> dict[str, Any]:
        """Run Phase 1 and collect performance metrics."""
        logger.info("🚀 Running Phase 1...")

        start_time = time.time()

        try:
            result = subprocess.run(
                [self.python_exe, self.phase1_script],
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout
            )

            end_time = time.time()
            execution_time = end_time - start_time

            if result.returncode != 0:
                raise RuntimeError(f"Phase 1 failed: {result.stderr}")

            # Parse output for statistics
            output_lines = result.stdout.split('\n')
            stats = self._parse_phase1_output(output_lines)

            # Check if output file exists
            output_exists = Path(self.phase1_output).exists()
            file_size = Path(self.phase1_output).stat().st_size if output_exists else 0

            phase1_results = {
                'success': True,
                'execution_time': execution_time,
                'output_file': self.phase1_output,
                'output_exists': output_exists,
                'file_size_bytes': file_size,
                'statistics': stats,
                'stdout': result.stdout,
                'stderr': result.stderr
            }

            logger.info(f"✅ Phase 1 completed in {execution_time:.2f}s")
            return phase1_results

        except Exception as e:
            logger.error(f"❌ Phase 1 failed: {e}")
            return {
                'success': False,
                'error': str(e),
                'execution_time': time.time() - start_time
            }

    def run_phase2(self) -> dict[str, Any]:
        """Run Phase 2 and collect performance metrics."""
        logger.info("🚀 Running Phase 2...")

        start_time = time.time()

        try:
            result = subprocess.run(
                [self.python_exe, self.phase2_script],
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout
            )

            end_time = time.time()
            execution_time = end_time - start_time

            if result.returncode != 0:
                raise RuntimeError(f"Phase 2 failed: {result.stderr}")

            # Parse output for statistics
            output_lines = result.stdout.split('\n')
            stats = self._parse_phase2_output(output_lines)

            # Check if output file exists
            output_exists = Path(self.phase2_output).exists()
            file_size = Path(self.phase2_output).stat().st_size if output_exists else 0

            phase2_results = {
                'success': True,
                'execution_time': execution_time,
                'output_file': self.phase2_output,
                'output_exists': output_exists,
                'file_size_bytes': file_size,
                'statistics': stats,
                'stdout': result.stdout,
                'stderr': result.stderr
            }

            logger.info(f"✅ Phase 2 completed in {execution_time:.2f}s")
            return phase2_results

        except Exception as e:
            logger.error(f"❌ Phase 2 failed: {e}")
            return {
                'success': False,
                'error': str(e),
                'execution_time': time.time() - start_time
            }

    def _parse_phase1_output(self, output_lines: list[str]) -> dict[str, Any]:
        """Parse Phase 1 output for statistics."""
        stats = {}

        for line in output_lines:
            if "Total sentences processed:" in line:
                stats['sentences_processed'] = int(line.split(':')[1].strip())
            elif "Total rows processed:" in line:
                stats['tokens_processed'] = int(line.split(':')[1].strip())
            elif "Extracted" in line and "clause mate relationships" in line:
                # Extract number from "Extracted 463 clause mate relationships"
                parts = line.split()
                for _i, part in enumerate(parts):
                    if part.isdigit():
                        stats['relationships_found'] = int(part)
                        break

        return stats

    def _parse_phase2_output(self, output_lines: list[str]) -> dict[str, Any]:
        """Parse Phase 2 output for statistics."""
        stats = {}

        for line in output_lines:
            if "sentences_processed:" in line:
                stats['sentences_processed'] = int(line.split(':')[1].strip())
            elif "tokens_processed:" in line:
                stats['tokens_processed'] = int(line.split(':')[1].strip())
            elif "relationships_found:" in line:
                stats['relationships_found'] = int(line.split(':')[1].strip())
            elif "coreference_chains_found:" in line:
                stats['coreference_chains_found'] = int(line.split(':')[1].strip())
            elif "critical_pronouns_found:" in line:
                stats['critical_pronouns_found'] = int(line.split(':')[1].strip())
            elif "phrases_found:" in line:
                stats['phrases_found'] = int(line.split(':')[1].strip())

        return stats

    def compare_csv_outputs(self) -> dict[str, Any]:
        """Compare the CSV outputs from both phases."""
        logger.info("📊 Comparing CSV outputs...")

        comparison = {}

        try:
            # Load both CSV files
            df1 = pd.read_csv(self.phase1_output, encoding='utf-8')
            df2 = pd.read_csv(self.phase2_output, encoding='utf-8')

            comparison['phase1'] = {
                'rows': len(df1),
                'columns': len(df1.columns),
                'column_names': list(df1.columns),
                'file_size_mb': round(Path(self.phase1_output).stat().st_size / (1024*1024), 2)
            }

            comparison['phase2'] = {
                'rows': len(df2),
                'columns': len(df2.columns),
                'column_names': list(df2.columns),
                'file_size_mb': round(Path(self.phase2_output).stat().st_size / (1024*1024), 2)
            }

            # Compare columns
            common_columns = set(df1.columns) & set(df2.columns)
            phase1_only = set(df1.columns) - set(df2.columns)
            phase2_only = set(df2.columns) - set(df1.columns)

            comparison['columns'] = {
                'common_count': len(common_columns),
                'common_columns': sorted(common_columns),
                'phase1_only_count': len(phase1_only),
                'phase1_only': sorted(phase1_only),
                'phase2_only_count': len(phase2_only),
                'phase2_only': sorted(phase2_only)
            }

            # Compare data types for common columns
            dtype_comparison = {}
            for col in common_columns:
                dtype_comparison[col] = {
                    'phase1': str(df1[col].dtype),
                    'phase2': str(df2[col].dtype),
                    'same': str(df1[col].dtype) == str(df2[col].dtype)
                }

            comparison['data_types'] = dtype_comparison

            # Sample data comparison for key columns
            key_columns = ['sentence_id', 'pronoun_text', 'clause_mate_text']
            sample_comparison = {}

            for col in key_columns:
                if col in common_columns:
                    sample_comparison[col] = {
                        'phase1_unique': df1[col].nunique(),
                        'phase2_unique': df2[col].nunique(),
                        'phase1_sample': df1[col].head(3).tolist(),
                        'phase2_sample': df2[col].head(3).tolist()
                    }

            comparison['sample_data'] = sample_comparison

            logger.info("✅ CSV comparison completed")
            return comparison

        except Exception as e:
            logger.error(f"❌ CSV comparison failed: {e}")
            return {'error': str(e)}

    def run_comparison(self) -> dict[str, Any]:
        """Run complete comparison of both phases."""
        logger.info("🔄 Starting Phase Comparison...")

        # Run both phases
        self.results['phase1'] = self.run_phase1()
        self.results['phase2'] = self.run_phase2()

        # Compare outputs if both succeeded
        if (self.results['phase1'].get('success') and
            self.results['phase2'].get('success')):
            self.results['comparison'] = self.compare_csv_outputs()

        return self.results

    def generate_report(self, results: dict[str, Any]) -> str:
        """Generate a human-readable comparison report."""
        report = []
        report.append("=" * 80)
        report.append("CLAUSE MATES PHASE COMPARISON REPORT")
        report.append("=" * 80)
        report.append("")

        # Phase 1 Results
        report.append("📋 PHASE 1 RESULTS")
        report.append("-" * 40)
        phase1 = results['phase1']
        if phase1.get('success'):
            report.append("✅ Status: SUCCESS")
            report.append(f"⏱️  Execution Time: {phase1['execution_time']:.2f} seconds")
            report.append(f"📁 Output File: {phase1['output_file']}")
            report.append(f"💾 File Size: {phase1['file_size_bytes']:,} bytes")

            if 'statistics' in phase1:
                stats = phase1['statistics']
                report.append("📊 Statistics:")
                for key, value in stats.items():
                    report.append(f"   {key}: {value:,}")
        else:
            report.append("❌ Status: FAILED")
            report.append(f"❗ Error: {phase1.get('error', 'Unknown error')}")

        report.append("")

        # Phase 2 Results
        report.append("📋 PHASE 2 RESULTS")
        report.append("-" * 40)
        phase2 = results['phase2']
        if phase2.get('success'):
            report.append("✅ Status: SUCCESS")
            report.append(f"⏱️  Execution Time: {phase2['execution_time']:.2f} seconds")
            report.append(f"📁 Output File: {phase2['output_file']}")
            report.append(f"💾 File Size: {phase2['file_size_bytes']:,} bytes")

            if 'statistics' in phase2:
                stats = phase2['statistics']
                report.append("📊 Statistics:")
                for key, value in stats.items():
                    report.append(f"   {key}: {value:,}")
        else:
            report.append("❌ Status: FAILED")
            report.append(f"❗ Error: {phase2.get('error', 'Unknown error')}")

        report.append("")

        # Performance Comparison
        if phase1.get('success') and phase2.get('success'):
            report.append("⚡ PERFORMANCE COMPARISON")
            report.append("-" * 40)
            time_diff = phase2['execution_time'] - phase1['execution_time']
            faster_phase = "Phase 2" if time_diff < 0 else "Phase 1"
            time_savings = abs(time_diff)

            report.append(f"Phase 1 Time: {phase1['execution_time']:.2f}s")
            report.append(f"Phase 2 Time: {phase2['execution_time']:.2f}s")
            report.append(f"Difference: {time_diff:+.2f}s ({faster_phase} is {time_savings:.2f}s faster)")

            # File size comparison
            size_diff = phase2['file_size_bytes'] - phase1['file_size_bytes']
            size_diff_mb = size_diff / (1024*1024)
            report.append(f"File Size Difference: {size_diff:+,} bytes ({size_diff_mb:+.2f} MB)")

            report.append("")

        # Output Comparison
        if 'comparison' in results and 'error' not in results['comparison']:
            comp = results['comparison']
            report.append("📊 OUTPUT COMPARISON")
            report.append("-" * 40)

            report.append(f"Phase 1: {comp['phase1']['rows']:,} rows, {comp['phase1']['columns']} columns")
            report.append(f"Phase 2: {comp['phase2']['rows']:,} rows, {comp['phase2']['columns']} columns")
            report.append(f"Row Difference: {comp['phase2']['rows'] - comp['phase1']['rows']:+,}")
            report.append(f"Column Difference: {comp['phase2']['columns'] - comp['phase1']['columns']:+}")

            report.append("")
            report.append("📋 COLUMN ANALYSIS")
            report.append(f"Common Columns: {comp['columns']['common_count']}")

            if comp['columns']['phase1_only_count'] > 0:
                report.append(f"Phase 1 Only ({comp['columns']['phase1_only_count']}):")
                for col in comp['columns']['phase1_only'][:5]:  # Show first 5
                    report.append(f"   • {col}")
                if comp['columns']['phase1_only_count'] > 5:
                    report.append(f"   ... and {comp['columns']['phase1_only_count'] - 5} more")

            if comp['columns']['phase2_only_count'] > 0:
                report.append(f"Phase 2 Only ({comp['columns']['phase2_only_count']}):")
                for col in comp['columns']['phase2_only'][:5]:  # Show first 5
                    report.append(f"   • {col}")
                if comp['columns']['phase2_only_count'] > 5:
                    report.append(f"   ... and {comp['columns']['phase2_only_count'] - 5} more")

            report.append("")

        # Summary
        report.append("🎯 SUMMARY")
        report.append("-" * 40)

        if phase1.get('success') and phase2.get('success'):
            report.append("✅ Both phases executed successfully")

            # Get key statistics for comparison
            p1_stats = phase1.get('statistics', {})
            p2_stats = phase2.get('statistics', {})

            if 'relationships_found' in p1_stats and 'relationships_found' in p2_stats:
                rel_diff = p2_stats['relationships_found'] - p1_stats['relationships_found']
                report.append(f"📈 Relationships: Phase 1: {p1_stats['relationships_found']:,}, "
                            f"Phase 2: {p2_stats['relationships_found']:,} (Δ{rel_diff:+,})")

            # Performance summary
            if phase2['execution_time'] < phase1['execution_time']:
                improvement = ((phase1['execution_time'] - phase2['execution_time']) /
                             phase1['execution_time']) * 100
                report.append(f"🚀 Phase 2 is {improvement:.1f}% faster")
            else:
                slowdown = ((phase2['execution_time'] - phase1['execution_time']) /
                          phase1['execution_time']) * 100
                report.append(f"⏳ Phase 2 is {slowdown:.1f}% slower")

        else:
            failed_phases = []
            if not phase1.get('success'):
                failed_phases.append("Phase 1")
            if not phase2.get('success'):
                failed_phases.append("Phase 2")
            report.append(f"❌ {', '.join(failed_phases)} failed to execute")

        report.append("")
        report.append("=" * 80)

        return "\n".join(report)


def main():
    """Main execution function."""
    print("🔄 Phase Comparison Tool")
    print("=" * 50)

    comparator = PhaseComparator()

    # Run comparison
    results = comparator.run_comparison()

    # Generate and display report
    report = comparator.generate_report(results)
    print(report)

    # Save detailed results to JSON
    results_file = "data/output/phase_comparison_results.json"
    with open(results_file, 'w', encoding='utf-8') as f:
        # Convert any non-serializable objects to strings
        serializable_results = json.loads(json.dumps(results, default=str))
        json.dump(serializable_results, f, indent=2, ensure_ascii=False)

    print(f"\n💾 Detailed results saved to: {results_file}")

    # Save report to text file
    report_file = "data/output/phase_comparison_report.txt"
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(report)

    print(f"📄 Report saved to: {report_file}")


if __name__ == "__main__":
    main()
