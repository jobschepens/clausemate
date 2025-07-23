#!/usr/bin/env python3
"""Check for duplicate rows in the Phase 2 output."""

import pandas as pd


def main():
    df = pd.read_csv("phase2_cross_sentence_test.csv")

    # Check sentence 17 specifically
    sent17 = df[df["sentence_id"] == 17]
    print(f"Rows for sentence 17: {len(sent17)}")

    # Check pronouns in sentence 17
    print("\nPronouns in sentence 17:")
    for pronoun in sent17["pronoun_text"].unique():
        pronoun_rows = sent17[sent17["pronoun_text"] == pronoun]
        print(f'  "{pronoun}" appears {len(pronoun_rows)} times')

        # Show clause mates for this pronoun
        print("    Clause mates:")
        for i, row in pronoun_rows.iterrows():
            print(f'      - "{row["clause_mate_text"]}"')
        print()

    # Check if antecedent info is the same for duplicate pronouns
    sie_rows = sent17[sent17["pronoun_text"] == "sie"]
    if len(sie_rows) > 1:
        print('Antecedent info for "sie" rows:')
        for i, row in sie_rows.iterrows():
            print(
                f'  Row {i}: antecedent="{row["pronoun_most_recent_antecedent_text"]}", distance={row["pronoun_most_recent_antecedent_distance"]}'
            )


if __name__ == "__main__":
    main()
