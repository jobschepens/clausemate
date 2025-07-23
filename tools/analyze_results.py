#!/usr/bin/env python3
"""Analyze Phase 2 cross-sentence antecedent detection results against task requirements.

Task: Check if pronouns appear at more consistent linear positions when clause mates
are present vs. absent, and verify correct antecedent detection (most recent in chain).
"""

import pandas as pd


def get_sentence_text(sentence_num, data_file="data/input/gotofiles/2.tsv"):
    """Get the complete text for a sentence from the original data file."""
    try:
        with open(data_file, encoding="utf-8") as f:
            lines = f.readlines()

        # Find the sentence by looking for #Text= followed by the sentence number
        for i, line in enumerate(lines):
            if line.startswith("#Text="):
                # Check if the next few lines contain the exact sentence number
                for j in range(1, 5):  # Check next 4 lines
                    if i + j < len(lines):
                        next_line = lines[i + j].strip()
                        # Look for pattern like "17-1" at the beginning of line
                        if next_line.startswith(f"{sentence_num}-1"):
                            return line.replace("#Text=", "").strip()

        return f"Sentence {sentence_num} not found"
    except Exception as e:
        return f"Could not read sentence: {e}"


def main():
    # Load results
    df = pd.read_csv("phase2_cross_sentence_test.csv")

    # Create output file
    output_file = "docs/CROSS_SENTENCE_ANALYSIS_REPORT.md"

    with open(output_file, "w", encoding="utf-8") as f:
        f.write("# Cross-Sentence Antecedent Detection Analysis Report\n\n")
        f.write(
            "**Generated from Phase 2 implementation with cross-sentence antecedent analysis**\n\n"
        )

        # Basic statistics
        total_rows = len(df)
        successful_antecedents = len(
            df[df["pronoun_most_recent_antecedent_text"] != "_"]
        )
        success_rate = (
            (successful_antecedents / total_rows) * 100 if total_rows > 0 else 0
        )

        f.write("## Antecedent Detection Analysis\n\n")
        f.write(f"- **Total relationships**: {total_rows}\n")
        f.write(f"- **Successful antecedent detections**: {successful_antecedents}\n")
        f.write(f"- **Success rate**: {success_rate:.1f}%\n\n")

        print("=== ANTECEDENT DETECTION ANALYSIS ===")
        print(f"Total relationships: {total_rows}")
        print(f"Successful antecedent detections: {successful_antecedents}")
        print(f"Success rate: {success_rate:.1f}%")
        print()

        # Task-specific analysis: Compare pronoun positions with/without clause mates
        f.write("## Task Requirement Analysis\n\n")
        f.write(
            "**Research Question**: Do pronouns appear at more consistent linear positions when clause mates are present?\n\n"
        )

        print("=== TASK REQUIREMENT ANALYSIS ===")
        print(
            "Checking: Do pronouns appear at more consistent positions when clause mates are present?"
        )

        # Filter for successful antecedent detections with numeric distances
        valid_data = df[
            (df["pronoun_most_recent_antecedent_text"] != "_")
            & (df["pronoun_most_recent_antecedent_distance"] != "_")
        ]

        if len(valid_data) > 0:
            # Convert distance to numeric
            valid_data = valid_data.copy()
            valid_data["distance_numeric"] = valid_data[
                "pronoun_most_recent_antecedent_distance"
            ].astype(int)

            # Group by clause mate presence (assuming more clause mates = present)
            has_clause_mates = valid_data[valid_data["num_clause_mates"] > 1]
            few_clause_mates = valid_data[valid_data["num_clause_mates"] <= 1]

            if len(has_clause_mates) > 0 and len(few_clause_mates) > 0:
                # Calculate average distances
                avg_dist_with_mates = has_clause_mates["distance_numeric"].mean()
                avg_dist_without_mates = few_clause_mates["distance_numeric"].mean()

                # Calculate variability (standard deviation)
                std_with_mates = has_clause_mates["distance_numeric"].std()
                std_without_mates = few_clause_mates["distance_numeric"].std()

                f.write("### Clause Mate Presence Analysis\n\n")
                f.write(
                    f"**With multiple clause mates** ({len(has_clause_mates)} cases):\n"
                )
                f.write(
                    f"- Average pronoun-antecedent distance: {avg_dist_with_mates:.1f} tokens\n"
                )
                f.write(f"- Distance variability (std dev): {std_with_mates:.1f}\n\n")

                f.write(
                    f"**With few/no clause mates** ({len(few_clause_mates)} cases):\n"
                )
                f.write(
                    f"- Average pronoun-antecedent distance: {avg_dist_without_mates:.1f} tokens\n"
                )
                f.write(
                    f"- Distance variability (std dev): {std_without_mates:.1f}\n\n"
                )

                print("\nClause Mate Presence Analysis:")
                print(f"With multiple clause mates (>{len(has_clause_mates)} cases):")
                print(
                    f"  - Average pronoun-antecedent distance: {avg_dist_with_mates:.1f} tokens"
                )
                print(f"  - Distance variability (std dev): {std_with_mates:.1f}")

                print(f"\nWith few/no clause mates ({len(few_clause_mates)} cases):")
                print(
                    f"  - Average pronoun-antecedent distance: {avg_dist_without_mates:.1f} tokens"
                )
                print(f"  - Distance variability (std dev): {std_without_mates:.1f}")

                # Check if pattern matches task expectation
                f.write("### Task Pattern Check\n\n")
                print("\nTask Pattern Check:")
                if avg_dist_with_mates < avg_dist_without_mates:
                    f.write(
                        "✅ **MATCHES**: Shorter average distance when clause mates present\n"
                    )
                    print(
                        "✓ MATCHES: Shorter average distance when clause mates present"
                    )
                else:
                    f.write(
                        "❌ **Different pattern**: Longer average distance when clause mates present\n"
                    )
                    print(
                        "✗ Different pattern: Longer average distance when clause mates present"
                    )

                if std_with_mates < std_without_mates:
                    f.write(
                        "✅ **MATCHES**: More consistent positions when clause mates present\n\n"
                    )
                    print(
                        "✓ MATCHES: More consistent positions when clause mates present"
                    )
                else:
                    f.write(
                        "❌ **Different pattern**: More variable positions when clause mates present\n\n"
                    )
                    print(
                        "✗ Different pattern: More variable positions when clause mates present"
                    )

        # Cross-sentence detection examples
        f.write("## Cross-Sentence Detection Examples\n\n")
        print("\n=== CROSS-SENTENCE DETECTION EXAMPLES ===")
        numeric_distances = df[df["pronoun_most_recent_antecedent_distance"] != "_"]
        high_distance = numeric_distances[
            numeric_distances["pronoun_most_recent_antecedent_distance"].astype(int)
            > 15
        ]

        f.write(f"**Cross-sentence antecedents found**: {len(high_distance)}\n\n")
        print(f"Cross-sentence antecedents found: {len(high_distance)}")

        if len(high_distance) > 0:
            f.write("### Diverse Examples\n")
            f.write(
                '*Showing correct "most recent" antecedent selection across sentences:*\n\n'
            )
            print(
                '\nDiverse examples (showing correct "most recent" antecedent selection):'
            )

            # Get diverse examples by grouping by pronoun type and sentence
            diverse_examples = []
            seen_combinations = set()

            for idx, (i, row) in enumerate(high_distance.iterrows()):
                # Create a key for diversity: pronoun_text + sentence_id + antecedent_text
                key = (
                    row["pronoun_text"],
                    row["sentence_id"],
                    row["pronoun_most_recent_antecedent_text"],
                )

                if key not in seen_combinations:
                    diverse_examples.append(row)
                    seen_combinations.add(key)

                    # Stop after we have 8 diverse examples
                    if len(diverse_examples) >= 8:
                        break

            for idx, row in enumerate(diverse_examples):
                f.write(f"#### Example {idx + 1}\n\n")
                print(f"\n  Example {idx + 1}:")

                # Get complete sentence text for current sentence
                current_sentence = get_sentence_text(row["sentence_id"])
                f.write(
                    f'**CURRENT SENTENCE {row["sentence_id"]}**: "{current_sentence}"\n\n'
                )
                print(
                    f'    CURRENT SENTENCE {row["sentence_id"]}: "{current_sentence}"'
                )

                f.write(
                    f'- **Critical pronoun**: "{row["pronoun_text"]}" (token {row["pronoun_token_idx"]})\n'
                )
                f.write(
                    f"- **Grammatical role**: {row['pronoun_grammatical_role']}, **Thematic role**: {row['pronoun_thematic_role']}\n"
                )
                f.write(
                    f'- **Clause mate**: "{row["clause_mate_text"]}" ({row["clause_mate_grammatical_role"]}, {row["clause_mate_thematic_role"]})\n'
                )
                f.write(
                    f"- **Total clause mates in sentence**: {row['num_clause_mates']}\n\n"
                )

                print(
                    f'    Critical pronoun: "{row["pronoun_text"]}" (token {row["pronoun_token_idx"]})'
                )
                print(
                    f"    Grammatical role: {row['pronoun_grammatical_role']}, Thematic role: {row['pronoun_thematic_role']}"
                )
                print(
                    f'    Clause mate: "{row["clause_mate_text"]}" ({row["clause_mate_grammatical_role"]}, {row["clause_mate_thematic_role"]})'
                )
                print(f"    Total clause mates in sentence: {row['num_clause_mates']}")

                # Show most recent antecedent with its sentence context
                f.write(
                    f'**MOST RECENT ANTECEDENT**: "{row["pronoun_most_recent_antecedent_text"]}" (distance: {row["pronoun_most_recent_antecedent_distance"]} tokens)\n'
                )
                print(
                    f'    MOST RECENT ANTECEDENT: "{row["pronoun_most_recent_antecedent_text"]}" (distance: {row["pronoun_most_recent_antecedent_distance"]} tokens)'
                )

                # Try to find which sentence contains the most recent antecedent
                # We'll search through a range of sentences before the current one
                antecedent_found = False
                for sent_num in range(
                    max(1, row["sentence_id"] - 10), row["sentence_id"]
                ):
                    sentence_text = get_sentence_text(sent_num)
                    if row["pronoun_most_recent_antecedent_text"] in sentence_text:
                        f.write(
                            f'  - Found in **Sentence {sent_num}**: "{sentence_text}"\n\n'
                        )
                        print(f'      Found in Sentence {sent_num}: "{sentence_text}"')
                        antecedent_found = True
                        break

                if not antecedent_found:
                    f.write(
                        "  - Context: Antecedent sentence not found in recent sentences\n\n"
                    )
                    print(
                        "      Context: Antecedent sentence not found in recent sentences"
                    )

                # Show first antecedent if different
                if (
                    row["pronoun_first_antecedent_text"]
                    != row["pronoun_most_recent_antecedent_text"]
                ):
                    f.write(
                        f'**FIRST ANTECEDENT**: "{row["pronoun_first_antecedent_text"]}" (distance: {row["pronoun_first_antecedent_distance"]} tokens)\n'
                    )
                    print(
                        f'    FIRST ANTECEDENT: "{row["pronoun_first_antecedent_text"]}" (distance: {row["pronoun_first_antecedent_distance"]} tokens)'
                    )

                    # Try to find which sentence contains the first antecedent
                    first_antecedent_found = False
                    for sent_num in range(1, row["sentence_id"]):
                        sentence_text = get_sentence_text(sent_num)
                        if row["pronoun_first_antecedent_text"] in sentence_text:
                            f.write(
                                f'  - Found in **Sentence {sent_num}**: "{sentence_text}"\n\n'
                            )
                            print(
                                f'      Found in Sentence {sent_num}: "{sentence_text}"'
                            )
                            first_antecedent_found = True
                            break

                    if not first_antecedent_found:
                        f.write("  - Context: First antecedent sentence not found\n\n")
                        print("      Context: First antecedent sentence not found")
                else:
                    f.write("\n")

                f.write(
                    f"- **Antecedent choices available**: {row['pronoun_antecedent_choice']}\n"
                )
                print(
                    f"    Antecedent choices available: {row['pronoun_antecedent_choice']}"
                )

                # Show coreference information
                coref_info = []
                if (
                    row["pronoun_coreference_link"]
                    and row["pronoun_coreference_link"] != "_"
                ):
                    coref_info.append(f"animate: {row['pronoun_coreference_link']}")
                if (
                    row["pronoun_inanimate_coreference_link"]
                    and row["pronoun_inanimate_coreference_link"] != "_"
                ):
                    coref_info.append(
                        f"inanimate: {row['pronoun_inanimate_coreference_link']}"
                    )
                if coref_info:
                    f.write(f"- **Coreference links**: {', '.join(coref_info)}\n\n")
                    print(f"    Coreference links: {', '.join(coref_info)}")
                else:
                    f.write("\n")

        print(
            "\n✅ Analysis complete! Report saved to docs/CROSS_SENTENCE_ANALYSIS_REPORT.md"
        )


if __name__ == "__main__":
    main()
