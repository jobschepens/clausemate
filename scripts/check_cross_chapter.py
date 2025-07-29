import glob

import pandas as pd

# Find the latest output directory
output_dirs = glob.glob("data/output/unified_analysis_*")
latest_dir = max(output_dirs)
csv_file = f"{latest_dir}/unified_relationships.csv"

print(f"Reading from: {csv_file}")
df = pd.read_csv(csv_file)

print(f"Total relationships: {len(df)}")
print(f"Cross-chapter relationships: {df['cross_chapter'].sum()}")
print(f"Cross-chapter percentage: {df['cross_chapter'].sum() / len(df) * 100:.1f}%")

print("\nSample cross-chapter relationships:")
cross_chapter_rels = df[df["cross_chapter"]]
if len(cross_chapter_rels) > 0:
    for _i, row in cross_chapter_rels.head(5).iterrows():
        print(
            f"  Chapter {row['chapter_number']}, Sentence {row['sentence_id']}: {row['pronoun_text']} -> {row['clause_mate_text']}"
        )
        print(f"    Chain context: {row['chapter_boundary_context']}")
else:
    print("  No cross-chapter relationships found")

print("\nBreakdown by chapter:")
chapter_breakdown = df.groupby("chapter_number")["cross_chapter"].agg(["count", "sum"])
chapter_breakdown["percentage"] = (
    chapter_breakdown["sum"] / chapter_breakdown["count"] * 100
).round(1)
print(chapter_breakdown)
