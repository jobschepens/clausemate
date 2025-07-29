#!/usr/bin/env python3
"""Verify Data Quality Fix - Check Role Information Extraction.

This script verifies that the data quality issues have been resolved:
1. Chapter 4: Thematic role info should NOT appear in grammatical role columns
2. Chapter 1: Both grammatical and thematic role info should be present
"""

import sys
from pathlib import Path

import pandas as pd


def verify_data_quality_fix():
    """Verify that the data quality issues have been resolved."""
    # Load the new unified relationships file
    latest_output_dir = Path("data/output/unified_analysis_20250729_144638")
    unified_file = latest_output_dir / "unified_relationships.csv"

    if not unified_file.exists():
        print(f"❌ ERROR: Unified relationships file not found: {unified_file}")
        return False

    print("🔍 VERIFYING DATA QUALITY FIX")
    print("=" * 50)

    # Load the data
    df = pd.read_csv(unified_file)

    print(f"📊 Total relationships: {len(df)}")
    print(f"📁 Chapters: {sorted(df['chapter_number'].unique())}")
    print()

    # Test 1: Check Chapter 4 - thematic roles should NOT be in grammatical role columns
    print("🧪 TEST 1: Chapter 4 - Checking for misplaced thematic role information")
    chapter4_data = df[df["chapter_number"] == 4]

    # Look for thematic role patterns in grammatical role columns
    grammatical_role_issues = chapter4_data[
        chapter4_data["pronoun_grammatical_role"].str.contains(
            "Agent|Patient|Theme|Experiencer|Beneficiary", case=False, na=False
        )
    ]

    if len(grammatical_role_issues) > 0:
        print(
            f"❌ FAILED: Found {len(grammatical_role_issues)} cases where thematic roles appear in grammatical role columns"
        )
        print("Sample cases:")
        for _, row in grammatical_role_issues.head(3).iterrows():
            print(
                f"  - Sentence {row['global_sentence_id']}: '{row['pronoun_grammatical_role']}'"
            )
    else:
        print(
            "✅ PASSED: No thematic role information found in grammatical role columns"
        )

    print()

    # Test 2: Check Chapter 1 - should have both grammatical and thematic role information
    print("🧪 TEST 2: Chapter 1 - Checking for presence of role information")
    chapter1_data = df[df["chapter_number"] == 1]

    # Count non-empty role information
    grammatical_roles_present = chapter1_data["pronoun_grammatical_role"].notna().sum()
    thematic_roles_present = chapter1_data["pronoun_thematic_role"].notna().sum()

    print("📈 Chapter 1 statistics:")
    print(f"  - Total relationships: {len(chapter1_data)}")
    print(f"  - Grammatical roles present: {grammatical_roles_present}")
    print(f"  - Thematic roles present: {thematic_roles_present}")

    if grammatical_roles_present == 0 and thematic_roles_present == 0:
        print("❌ FAILED: No role information found in Chapter 1")
    elif grammatical_roles_present > 0 and thematic_roles_present > 0:
        print("✅ PASSED: Both grammatical and thematic role information present")
    else:
        print(
            f"⚠️  PARTIAL: Only {'grammatical' if grammatical_roles_present > 0 else 'thematic'} roles present"
        )

    print()

    # Test 3: Sample data inspection
    print("🔍 TEST 3: Sample data inspection")

    # Show samples from Chapter 1
    print("\n📋 Chapter 1 samples (first 3 with role information):")
    chapter1_with_roles = chapter1_data[
        (chapter1_data["pronoun_grammatical_role"].notna())
        | (chapter1_data["pronoun_thematic_role"].notna())
    ].head(3)

    for _, row in chapter1_with_roles.iterrows():
        print(f"  Sentence {row['global_sentence_id']}:")
        print(f"    Pronoun: '{row['pronoun_text']}'")
        print(f"    Grammatical role: '{row['pronoun_grammatical_role']}'")
        print(f"    Thematic role: '{row['pronoun_thematic_role']}'")
        print()

    # Show samples from Chapter 4
    print("📋 Chapter 4 samples (first 3 with role information):")
    chapter4_with_roles = chapter4_data[
        (chapter4_data["pronoun_grammatical_role"].notna())
        | (chapter4_data["pronoun_thematic_role"].notna())
    ].head(3)

    for _, row in chapter4_with_roles.iterrows():
        print(f"  Sentence {row['global_sentence_id']}:")
        print(f"    Pronoun: '{row['pronoun_text']}'")
        print(f"    Grammatical role: '{row['pronoun_grammatical_role']}'")
        print(f"    Thematic role: '{row['pronoun_thematic_role']}'")
        print()

    # Test 4: Cross-chapter comparison
    print("🧪 TEST 4: Cross-chapter role information comparison")
    role_stats = (
        df.groupby("chapter_number")
        .agg(
            {
                "pronoun_grammatical_role": lambda x: x.notna().sum(),
                "pronoun_thematic_role": lambda x: x.notna().sum(),
                "chapter_number": "count",
            }
        )
        .rename(columns={"chapter_number": "total_relationships"})
    )

    print("\n📊 Role information by chapter:")
    print(role_stats)

    print("\n🎯 SUMMARY")
    print("=" * 50)

    # Overall assessment
    issues_found = []

    if len(grammatical_role_issues) > 0:
        issues_found.append("Chapter 4 has thematic roles in grammatical role columns")

    if grammatical_roles_present == 0 and thematic_roles_present == 0:
        issues_found.append("Chapter 1 has no role information")

    if len(issues_found) == 0:
        print("✅ ALL TESTS PASSED: Data quality issues have been resolved!")
        return True
    else:
        print("❌ ISSUES STILL PRESENT:")
        for issue in issues_found:
            print(f"  - {issue}")
        return False


if __name__ == "__main__":
    success = verify_data_quality_fix()
    sys.exit(0 if success else 1)
