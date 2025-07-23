#!/usr/bin/env python3
"""
Quick verification that pronoun_coref_ids field is working correctly in Phase 2.
"""

import pandas as pd

def compare_pronoun_coref_ids():
    """Compare pronoun_coref_ids between Phase 1 and Phase 2."""

    # Load both CSV files
    df1 = pd.read_csv("archive/phase1/clause_mates_phase1_export.csv", encoding='utf-8')
    df2 = pd.read_csv("clause_mates_phase2_export.csv", encoding='utf-8')

    print("🔍 PRONOUN_COREF_IDS FIELD VERIFICATION")
    print("=" * 60)

    # Check if field exists in both
    phase1_has_field = 'pronoun_coref_ids' in df1.columns
    phase2_has_field = 'pronoun_coref_ids' in df2.columns

    print(f"Phase 1 has pronoun_coref_ids: {phase1_has_field}")
    print(f"Phase 2 has pronoun_coref_ids: {phase2_has_field}")

    if not (phase1_has_field and phase2_has_field):
        print("❌ Field missing in one or both phases!")
        return

    print("\n📊 SAMPLE DATA COMPARISON:")
    print("Phase 1 sample pronoun_coref_ids:")
    for i in range(min(5, len(df1))):
        row = df1.iloc[i]
        print(f"  {row['sentence_id']}: {row['pronoun_text']} → {row['pronoun_coref_ids']}")

    print("\nPhase 2 sample pronoun_coref_ids:")
    for i in range(min(5, len(df2))):
        row = df2.iloc[i]
        print(f"  {row['sentence_id']}: {row['pronoun_text']} → {row['pronoun_coref_ids']}")

    # Check field statistics
    print(f"\n📈 FIELD STATISTICS:")
    print(f"Phase 1 non-null values: {df1['pronoun_coref_ids'].notna().sum()}/{len(df1)}")
    print(f"Phase 2 non-null values: {df2['pronoun_coref_ids'].notna().sum()}/{len(df2)}")

    # Check data types
    print(f"\nPhase 1 pronoun_coref_ids data type: {df1['pronoun_coref_ids'].dtype}")
    print(f"Phase 2 pronoun_coref_ids data type: {df2['pronoun_coref_ids'].dtype}")

    print(f"\n✅ SUCCESS: Both phases now include pronoun_coref_ids field!")
    print(f"Column compatibility improved: Phase 2 now has {len(set(df1.columns) & set(df2.columns))} common columns with Phase 1")

if __name__ == "__main__":
    compare_pronoun_coref_ids()
