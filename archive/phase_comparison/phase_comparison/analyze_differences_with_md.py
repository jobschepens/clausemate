#!/usr/bin/env python3
"""Comprehensive difference analysis between Phase 1 and Phase 2 outputs.
Includes detailed sorting analysis and data processing order investigation.
"""

from datetime import datetime
from pathlib import Path

import pandas as pd


class OutputCapture:
    """Capture print output for both console and markdown file."""

    def __init__(self, filename):
        self.filename = filename
        self.content = []

    def print(self, *args, **kwargs):
        """Print to both console and capture for markdown."""
        # Print to console
        print(*args, **kwargs)

        # Capture for markdown (remove emoji for better compatibility)
        text = " ".join(str(arg) for arg in args)
        # Convert emojis to text equivalents for markdown
        text = text.replace("🔍", "## ")
        text = text.replace("📊", "### ")
        text = text.replace("📋", "### ")
        text = text.replace("🆔", "### ")
        text = text.replace("🔄", "### ")
        text = text.replace("👥", "### ")
        text = text.replace("📝", "### ")
        text = text.replace("🔬", "### ")
        text = text.replace("💾", "### ")
        text = text.replace("⚡", "### ")
        text = text.replace("🎯", "### ")
        text = text.replace("⚠️", "**Warning:**")
        text = text.replace("✅", "✓")
        text = text.replace("❌", "✗")

        self.content.append(text)

    def save_markdown(self):
        """Save captured content to markdown file."""
        with open(self.filename, "w", encoding="utf-8") as f:
            f.write("# Comprehensive Phase Difference Analysis\n\n")
            f.write(
                f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
            )

            # Process content for markdown formatting
            for line in self.content:
                # Convert separator lines to horizontal rules
                if line.startswith("=") or line.startswith("-"):
                    f.write("\n---\n\n")
                # Add code blocks for data samples
                elif any(
                    keyword in line.lower()
                    for keyword in ["sent_", "token", "phase 1:", "phase 2:"]
                ):
                    if line.strip().startswith(
                        ("1.", "2.", "3.", "4.", "5.", "6.", "7.", "8.", "9.", "10.")
                    ):
                        f.write(f"   {line}\n")
                    else:
                        f.write(f"{line}\n")
                else:
                    f.write(f"{line}\n")

            f.write(
                f"\n\n---\n*Analysis completed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n"
            )


def analyze_sentence_id_patterns(df1, df2, output):
    """Analyze sentence ID patterns and formats."""
    output.print("\n🆔 SENTENCE ID PATTERN ANALYSIS:")
    output.print("-" * 40)

    # Now we have both formats in both phases
    output.print("Phase 1 sentence ID columns:")
    output.print(
        f"  sentence_id (primary): Sample values {list(df1['sentence_id'].head())}"
    )
    output.print(
        f"  sentence_id_numeric: Sample values {list(df1['sentence_id_numeric'].head())}"
    )
    output.print(
        f"  sentence_id_prefixed: Sample values {list(df1['sentence_id_prefixed'].head())}"
    )

    output.print("\nPhase 2 sentence ID columns:")
    output.print(
        f"  sentence_id (primary): Sample values {list(df2['sentence_id'].head())}"
    )
    output.print(
        f"  sentence_id_numeric: Sample values {list(df2['sentence_id_numeric'].head())}"
    )
    output.print(
        f"  sentence_id_prefixed: Sample values {list(df2['sentence_id_prefixed'].head())}"
    )

    # Compare the numeric IDs which should be identical
    nums1 = set(df1["sentence_id_numeric"])
    nums2 = set(df2["sentence_id_numeric"])

    output.print("\nNumeric sentence ID comparison:")
    output.print(f"  Phase 1 unique numeric IDs: {len(nums1)}")
    output.print(f"  Phase 2 unique numeric IDs: {len(nums2)}")
    output.print(f"  Common numeric IDs: {len(nums1 & nums2)}")

    return nums1, nums2


def analyze_processing_order(df1, df2, output):
    """Analyze the order in which data was processed."""
    output.print("\n📋 PROCESSING ORDER ANALYSIS:")
    output.print("-" * 40)

    # Group by numeric sentence ID to make comparison meaningful
    sentences_1 = (
        df1.groupby("sentence_id_numeric")
        .agg({"pronoun_text": "count", "pronoun_token_idx": lambda x: list(x)})
        .rename(columns={"pronoun_text": "relationship_count"})
    )

    sentences_2 = (
        df2.groupby("sentence_id_numeric")
        .agg({"pronoun_text": "count", "pronoun_token_idx": lambda x: list(x)})
        .rename(columns={"pronoun_text": "relationship_count"})
    )

    # Sort by numeric sentence ID for meaningful comparison
    sentences_1_sorted = sentences_1.sort_index()
    sentences_2_sorted = sentences_2.sort_index()

    output.print("Phase 1: First 10 sentences by numeric sentence ID:")
    for i, (sent_id, row) in enumerate(sentences_1_sorted.head(10).iterrows()):
        token_indices = sorted(row["pronoun_token_idx"])
        output.print(
            f"  {i + 1:2d}. Sent {sent_id:3d}: {row['relationship_count']} relationships, tokens: {token_indices}"
        )

    output.print("\nPhase 2: First 10 sentences by numeric sentence ID:")
    for i, (sent_id, row) in enumerate(sentences_2_sorted.head(10).iterrows()):
        token_indices = sorted(row["pronoun_token_idx"])
        output.print(
            f"  {i + 1:2d}. Sent {sent_id:3d}: {row['relationship_count']} relationships, tokens: {token_indices}"
        )

    return sentences_1_sorted, sentences_2_sorted


def analyze_sorting_differences(df1, df2, output):
    """Analyze sorting differences between the two phases."""
    output.print("\n🔄 SORTING PATTERN ANALYSIS:")
    output.print("-" * 40)

    # Use the existing sentence_id_numeric column for both phases
    df1_sorted = df1.sort_values(
        ["sentence_id_numeric", "pronoun_token_idx"]
    ).reset_index(drop=True)
    df2_sorted = df2.sort_values(
        ["sentence_id_numeric", "pronoun_token_idx"]
    ).reset_index(drop=True)

    output.print("Phase 1 - First 10 rows after sorting by sentence_id_numeric:")
    for i in range(min(10, len(df1_sorted))):
        row = df1_sorted.iloc[i]
        output.print(
            f"  {i + 1:2d}. Sent {row['sentence_id_numeric']:3d}, Token {row['pronoun_token_idx']:2d}: '{row['pronoun_text']}' → '{row['clause_mate_text']}'"
        )

    output.print("\nPhase 2 - First 10 rows after sorting by sentence_id_numeric:")
    for i in range(min(10, len(df2_sorted))):
        row = df2_sorted.iloc[i]
        output.print(
            f"  {i + 1:2d}. Sent {row['sentence_id_numeric']:3d}, Token {row['pronoun_token_idx']:2d}: '{row['pronoun_text']}' → '{row['clause_mate_text']}'"
        )

    # Compare using numeric sentence IDs to see if any sentences are missing
    sent_nums_1 = set(df1["sentence_id_numeric"])
    sent_nums_2 = set(df2["sentence_id_numeric"])

    missing_in_2 = sent_nums_1 - sent_nums_2
    missing_in_1 = sent_nums_2 - sent_nums_1

    if missing_in_2:
        output.print(
            f"\n⚠️  Sentences in Phase 1 but not Phase 2: {sorted(missing_in_2)}"
        )
    if missing_in_1:
        output.print(
            f"\n⚠️  Sentences in Phase 2 but not Phase 1: {sorted(missing_in_1)}"
        )

    # Show that when normalized, the data is essentially identical
    if len(missing_in_1) == 0 and len(missing_in_2) == 0:
        output.print("\n✅ All sentences present in both phases when using numeric IDs")

    return df1_sorted, df2_sorted


def analyze_data_content_differences(df1, df2, output):
    """Analyze differences in actual data content."""
    output.print("\n📊 DATA CONTENT ANALYSIS:")
    output.print("-" * 40)

    # Compare pronoun types
    pronoun_types_1 = df1["pronoun_text"].value_counts()
    pronoun_types_2 = df2["pronoun_text"].value_counts()

    all_pronouns = set(pronoun_types_1.index) | set(pronoun_types_2.index)

    output.print("Pronoun frequency comparison:")
    significant_diffs = []
    for pronoun in sorted(all_pronouns):
        count1 = pronoun_types_1.get(pronoun, 0)
        count2 = pronoun_types_2.get(pronoun, 0)
        diff = count2 - count1
        if abs(diff) > 0:
            significant_diffs.append((pronoun, count1, count2, diff))

    # Show top differences
    significant_diffs.sort(key=lambda x: abs(x[3]), reverse=True)
    for pronoun, c1, c2, diff in significant_diffs[:10]:
        output.print(f"  '{pronoun}': {c1} → {c2} ({diff:+})")

    # Analyze clause mate patterns
    output.print("\nClause mate analysis:")
    cm_counts_1 = df1["clause_mate_text"].value_counts()
    cm_counts_2 = df2["clause_mate_text"].value_counts()

    output.print(f"  Phase 1 unique clause mates: {len(cm_counts_1)}")
    output.print(f"  Phase 2 unique clause mates: {len(cm_counts_2)}")

    # Check for null/missing values
    output.print("\nMissing value analysis:")
    for col in ["pronoun_text", "clause_mate_text", "pronoun_coref_ids"]:
        if col in df1.columns and col in df2.columns:
            null1 = df1[col].isnull().sum() + (df1[col] == "_").sum()
            null2 = df2[col].isnull().sum() + (df2[col] == "_").sum()
            output.print(f"  {col}: Phase1={null1}, Phase2={null2}")


def analyze_differences():
    """Comprehensive analysis of differences between Phase 1 and Phase 2 outputs."""
    # Generate unique filename with current timestamp
    from datetime import datetime

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"data/output/phase_difference_analysis_{timestamp}.md"

    # Initialize output capture
    output = OutputCapture(filename)

    # Load both CSV files
    df1 = pd.read_csv("data/output/clause_mates_phase1_export.csv", encoding="utf-8")
    df2 = pd.read_csv("data/output/clause_mates_phase2_export.csv", encoding="utf-8")

    output.print("🔍 COMPREHENSIVE DIFFERENCE ANALYSIS")
    output.print("=" * 60)

    # Basic statistics
    output.print("\n📊 BASIC STATISTICS:")
    output.print(f"Phase 1: {len(df1):,} relationships, {len(df1.columns)} columns")
    output.print(f"Phase 2: {len(df2):,} relationships, {len(df2.columns)} columns")
    output.print(f"Difference: {len(df2) - len(df1):+,} relationships")

    # Column differences
    cols1 = set(df1.columns)
    cols2 = set(df2.columns)
    common_cols = cols1 & cols2
    only_in_1 = cols1 - cols2
    only_in_2 = cols2 - cols1

    output.print("\n📋 COLUMN DIFFERENCES:")
    output.print(f"Common columns: {len(common_cols)}")
    if only_in_1:
        output.print(f"Only in Phase 1: {sorted(only_in_1)}")
    if only_in_2:
        output.print(f"Only in Phase 2: {sorted(only_in_2)}")

    # Analyze sentence ID patterns
    nums1, nums2 = analyze_sentence_id_patterns(df1, df2, output)

    # Analyze processing order
    sentences_1, sentences_2 = analyze_processing_order(df1, df2, output)

    # Analyze sorting differences
    df1_sorted, df2_sorted = analyze_sorting_differences(df1, df2, output)

    # Analyze data content differences
    analyze_data_content_differences(df1, df2, output)

    # Original analysis from previous version
    output.print("\n👥 PRONOUN ANALYSIS:")
    pronoun_counts_1 = df1["pronoun_text"].value_counts()
    pronoun_counts_2 = df2["pronoun_text"].value_counts()

    output.print(f"Phase 1 unique pronouns: {len(pronoun_counts_1)}")
    output.print(f"Phase 2 unique pronouns: {len(pronoun_counts_2)}")

    output.print("\nTop 5 pronouns in Phase 1:")
    for pronoun, count in pronoun_counts_1.head().items():
        count_2 = pronoun_counts_2.get(pronoun, 0)
        diff = count_2 - count
        output.print(f"  {pronoun}: {count} → {count_2} (Δ{diff:+})")

    # Sentence distribution using numeric IDs for proper comparison
    output.print("\n📝 SENTENCE ANALYSIS:")
    sent_counts_1 = df1["sentence_id_numeric"].value_counts()
    sent_counts_2 = df2["sentence_id_numeric"].value_counts()

    output.print(f"Phase 1 unique sentences: {len(sent_counts_1)}")
    output.print(f"Phase 2 unique sentences: {len(sent_counts_2)}")

    # Find sentences with different relationship counts using numeric IDs
    sent_diff = {}
    all_sentences = set(sent_counts_1.index) | set(sent_counts_2.index)

    for sent in all_sentences:
        count_1 = sent_counts_1.get(sent, 0)
        count_2 = sent_counts_2.get(sent, 0)
        if count_1 != count_2:
            sent_diff[sent] = (count_1, count_2, count_2 - count_1)

    if sent_diff:
        output.print("\n📊 SENTENCES WITH DIFFERENT RELATIONSHIP COUNTS:")
        output.print(f"Found {len(sent_diff)} sentences with differences")

        # Show top 10 differences
        sorted_diffs = sorted(
            sent_diff.items(), key=lambda x: abs(x[1][2]), reverse=True
        )
        for sent, (c1, c2, diff) in sorted_diffs[:10]:
            output.print(f"  {sent}: {c1} → {c2} (Δ{diff:+})")

        if len(sorted_diffs) > 10:
            output.print(f"  ... and {len(sorted_diffs) - 10} more")

    # Look at specific examples of differences
    output.print("\n🔬 SAMPLE RELATIONSHIP COMPARISON:")

    # Sort both phases by numeric sentence ID for meaningful comparison
    df1_sorted = df1.sort_values(["sentence_id_numeric", "pronoun_token_idx"])
    df2_sorted = df2.sort_values(["sentence_id_numeric", "pronoun_token_idx"])

    # Take first few relationships from each
    output.print("First 3 relationships in Phase 1:")
    for i in range(min(3, len(df1_sorted))):
        row = df1_sorted.iloc[i]
        output.print(
            f"  {i + 1}. Sent {row['sentence_id_numeric']}: '{row['pronoun_text']}' → '{row['clause_mate_text']}'"
        )

    output.print("\nFirst 3 relationships in Phase 2:")
    for i in range(min(3, len(df2_sorted))):
        row = df2_sorted.iloc[i]
        output.print(
            f"  {i + 1}. Sent {row['sentence_id_numeric']}: '{row['pronoun_text']}' → '{row['clause_mate_text']}'"
        )

    # File size analysis
    size1 = Path("data/output/clause_mates_phase1_export.csv").stat().st_size
    size2 = Path("data/output/clause_mates_phase2_export.csv").stat().st_size

    output.print("\n💾 FILE SIZE ANALYSIS:")
    output.print(f"Phase 1: {size1:,} bytes ({size1 / (1024 * 1024):.2f} MB)")
    output.print(f"Phase 2: {size2:,} bytes ({size2 / (1024 * 1024):.2f} MB)")
    output.print(
        f"Size difference: {size2 - size1:+,} bytes ({(size2 - size1) / (1024 * 1024):+.2f} MB)"
    )
    output.print(f"Size change: {((size2 - size1) / size1) * 100:+.1f}%")

    # Performance implications
    rows_per_kb_1 = len(df1) / (size1 / 1024)
    rows_per_kb_2 = len(df2) / (size2 / 1024)

    output.print("\n⚡ EFFICIENCY METRICS:")
    output.print(f"Phase 1: {rows_per_kb_1:.1f} relationships per KB")
    output.print(f"Phase 2: {rows_per_kb_2:.1f} relationships per KB")
    output.print(
        f"Efficiency change: {((rows_per_kb_2 - rows_per_kb_1) / rows_per_kb_1) * 100:+.1f}%"
    )

    # Summary of key findings
    output.print("\n🎯 KEY FINDINGS SUMMARY:")
    output.print("-" * 40)
    output.print(f"1. Row difference: {len(df2) - len(df1):+} relationships")
    output.print(
        f"2. Column compatibility: {'✅ Perfect' if len(only_in_1) == 0 and len(only_in_2) == 0 else '❌ Issues found'}"
    )
    output.print("3. Sentence ID format: Phase 1 uses prefixed, Phase 2 uses numeric")
    output.print(
        f"4. Performance: Phase 2 is {rows_per_kb_2 / rows_per_kb_1:.1f}x more efficient"
    )
    output.print(
        f"5. Missing sentences: {len(sent_diff)} sentences have different relationship counts"
    )

    # Save markdown file
    output.save_markdown()
    print(f"\n📄 Analysis saved to: {output.filename}")


if __name__ == "__main__":
    analyze_differences()
