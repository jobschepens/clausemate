#!/usr/bin/env python3
"""Analyze data quality issues in the unified relationships file."""

from pathlib import Path

import pandas as pd


def analyze_data_quality_issues():
    """Analyze the specific data quality issues mentioned by the user."""
    # Load the unified relationships file
    csv_path = Path(
        "data/output/deliverable_package_20250729/unified_relationships.csv"
    )

    if not csv_path.exists():
        print(f"❌ File not found: {csv_path}")
        return

    print(f"📊 Analyzing data quality issues in: {csv_path}")
    print("=" * 60)

    # Load the data
    df = pd.read_csv(csv_path)

    print(f"📈 Total relationships: {len(df)}")
    print(f"📋 Columns: {len(df.columns)}")
    print()

    # Check source file distribution
    if "source_file" in df.columns:
        print("📁 Source file distribution:")
        source_counts = df["source_file"].value_counts()
        for source, count in source_counts.items():
            print(f"   • {source}: {count} relationships")
        print()

    # Problem 1: Chapter 4 - thematic role info in grammatical role columns
    print("🔍 PROBLEM 1: Chapter 4 - Role information analysis")
    print("-" * 50)

    if "source_file" in df.columns:
        chapter4_data = df[df["source_file"].str.contains("4.tsv", na=False)]
        print(f"Chapter 4 relationships: {len(chapter4_data)}")

        if len(chapter4_data) > 0:
            # Check pronoun role columns
            pronoun_gram_roles = (
                chapter4_data["pronoun_grammatical_role"].dropna().unique()[:10]
            )
            pronoun_them_roles = (
                chapter4_data["pronoun_thematic_role"].dropna().unique()[:10]
            )

            print(f"Pronoun grammatical roles (first 10): {list(pronoun_gram_roles)}")
            print(f"Pronoun thematic roles (first 10): {list(pronoun_them_roles)}")

            # Check clause mate role columns
            cm_gram_roles = (
                chapter4_data["clause_mate_grammatical_role"].dropna().unique()[:10]
            )
            cm_them_roles = (
                chapter4_data["clause_mate_thematic_role"].dropna().unique()[:10]
            )

            print(f"Clause mate grammatical roles (first 10): {list(cm_gram_roles)}")
            print(f"Clause mate thematic roles (first 10): {list(cm_them_roles)}")

            # Check for thematic role patterns in grammatical role columns
            gram_roles_with_thematic = []
            for role in pronoun_gram_roles:
                if role and any(
                    thematic in str(role).lower()
                    for thematic in [
                        "agent",
                        "patient",
                        "theme",
                        "goal",
                        "source",
                        "experiencer",
                    ]
                ):
                    gram_roles_with_thematic.append(role)

            if gram_roles_with_thematic:
                print(
                    f"⚠️  Found thematic role patterns in grammatical role column: {gram_roles_with_thematic}"
                )

    print()

    # Problem 2: Chapter 1 - missing role information
    print("🔍 PROBLEM 2: Chapter 1 - Missing role information analysis")
    print("-" * 50)

    if "source_file" in df.columns:
        chapter1_data = df[df["source_file"].str.contains("1.tsv", na=False)]
        print(f"Chapter 1 relationships: {len(chapter1_data)}")

        if len(chapter1_data) > 0:
            # Check for missing values
            pronoun_gram_missing = (
                chapter1_data["pronoun_grammatical_role"].isna().sum()
            )
            pronoun_them_missing = chapter1_data["pronoun_thematic_role"].isna().sum()
            cm_gram_missing = chapter1_data["clause_mate_grammatical_role"].isna().sum()
            cm_them_missing = chapter1_data["clause_mate_thematic_role"].isna().sum()

            print(
                f"Missing pronoun grammatical roles: {pronoun_gram_missing}/{len(chapter1_data)} ({pronoun_gram_missing / len(chapter1_data) * 100:.1f}%)"
            )
            print(
                f"Missing pronoun thematic roles: {pronoun_them_missing}/{len(chapter1_data)} ({pronoun_them_missing / len(chapter1_data) * 100:.1f}%)"
            )
            print(
                f"Missing clause mate grammatical roles: {cm_gram_missing}/{len(chapter1_data)} ({cm_gram_missing / len(chapter1_data) * 100:.1f}%)"
            )
            print(
                f"Missing clause mate thematic roles: {cm_them_missing}/{len(chapter1_data)} ({cm_them_missing / len(chapter1_data) * 100:.1f}%)"
            )

            # Show sample of non-missing values
            sample_data = chapter1_data[
                [
                    "pronoun_text",
                    "pronoun_grammatical_role",
                    "pronoun_thematic_role",
                    "clause_mate_text",
                    "clause_mate_grammatical_role",
                    "clause_mate_thematic_role",
                ]
            ].head(5)
            print("\nSample Chapter 1 data:")
            print(sample_data.to_string(index=False))

    print()

    # Overall role information analysis
    print("🔍 OVERALL ANALYSIS: Role information across all chapters")
    print("-" * 50)

    role_columns = [
        "pronoun_grammatical_role",
        "pronoun_thematic_role",
        "clause_mate_grammatical_role",
        "clause_mate_thematic_role",
    ]

    for col in role_columns:
        if col in df.columns:
            missing_count = df[col].isna().sum()
            total_count = len(df)
            print(
                f"{col}: {missing_count}/{total_count} missing ({missing_count / total_count * 100:.1f}%)"
            )

    print()

    # Check for data type issues
    print("🔍 DATA TYPE ANALYSIS")
    print("-" * 50)

    for col in role_columns:
        if col in df.columns:
            unique_values = df[col].dropna().unique()
            print(f"{col}: {len(unique_values)} unique values")
            if len(unique_values) <= 20:
                print(f"   Values: {list(unique_values)}")
            else:
                print(f"   Sample values: {list(unique_values[:10])}")

    print()
    print("✅ Analysis complete!")


if __name__ == "__main__":
    analyze_data_quality_issues()
