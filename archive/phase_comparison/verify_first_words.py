#!/usr/bin/env python3
"""Quick verification that first_words field is working correctly in both phases."""

import pandas as pd


def compare_first_words():
    """Compare first_words between Phase 1 and Phase 2."""
    # Load both CSV files
    df1 = pd.read_csv("archive/phase1/clause_mates_phase1_export.csv", encoding='utf-8')
    df2 = pd.read_csv("clause_mates_phase2_export.csv", encoding='utf-8')

    print("🔍 FIRST_WORDS FIELD VERIFICATION")
    print("=" * 60)

    # Check if field exists in both
    phase1_has_field = 'first_words' in df1.columns
    phase2_has_field = 'first_words' in df2.columns

    print(f"Phase 1 has first_words: {phase1_has_field}")
    print(f"Phase 2 has first_words: {phase2_has_field}")

    if not (phase1_has_field and phase2_has_field):
        print("❌ Field missing in one or both phases!")
        return

    print("\n📊 SAMPLE DATA COMPARISON:")
    print("Phase 1 sample first_words:")
    for i in range(min(5, len(df1))):
        row = df1.iloc[i]
        print(f"  {row['sentence_id']}: {row['first_words']}")

    print("\nPhase 2 sample first_words:")
    for i in range(min(5, len(df2))):
        row = df2.iloc[i]
        print(f"  {row['sentence_id']}: {row['first_words']}")

    # Check field statistics
    print("\n📈 FIELD STATISTICS:")
    print(f"Phase 1 non-null values: {df1['first_words'].notna().sum()}/{len(df1)}")
    print(f"Phase 2 non-null values: {df2['first_words'].notna().sum()}/{len(df2)}")

    # Check data types
    print(f"\nPhase 1 first_words data type: {df1['first_words'].dtype}")
    print(f"Phase 2 first_words data type: {df2['first_words'].dtype}")

    # Check for complete column compatibility
    common_columns = set(df1.columns) & set(df2.columns)
    total_columns_1 = len(df1.columns)
    total_columns_2 = len(df2.columns)

    print("\n🏆 COMPLETE COMPATIBILITY CHECK:")
    print(f"Phase 1 total columns: {total_columns_1}")
    print(f"Phase 2 total columns: {total_columns_2}")
    print(f"Common columns: {len(common_columns)}")

    if len(common_columns) == total_columns_1 == total_columns_2:
        print("✅ PERFECT: Complete column compatibility achieved!")
        print("🎉 Both phases now have identical column structure!")
    else:
        print("❌ Partial compatibility")
        only_in_1 = set(df1.columns) - set(df2.columns)
        only_in_2 = set(df2.columns) - set(df1.columns)
        if only_in_1:
            print(f"Only in Phase 1: {sorted(only_in_1)}")
        if only_in_2:
            print(f"Only in Phase 2: {sorted(only_in_2)}")

if __name__ == "__main__":
    compare_first_words()
