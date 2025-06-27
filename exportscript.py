import os
import re
import csv

# Define pronoun lists (lowercase for matching)
PERSONAL_PRONOUNS = {"er", "sie", "es"}
D_PRONOUNS = {"der", "die", "das"}
DEMONSTRATIVES = {"dieser", "diese", "dieses"}

# Helper: Check if a token is a relevant pronoun
def is_relevant_pronoun(token):
    t = token.lower()
    return t in PERSONAL_PRONOUNS or t in D_PRONOUNS or t in DEMONSTRATIVES

# Helper: Get all utterances from a TSV file
def parse_webanno_tsv(filepath):
    utterances = []
    current_utt = []
    with open(filepath, encoding="utf-8") as f:
        for line in f:
            if line.startswith("#Text="):
                if current_utt:
                    utterances.append(current_utt)
                    current_utt = []
            elif line.strip() and not line.startswith("#"):
                current_utt.append(line.strip().split('\t'))
        if current_utt:
            utterances.append(current_utt)
    return utterances

# Helper: Extract features for each clause mate in an utterance
def extract_features(utterance):
    tokens = [tok[2] for tok in utterance]
    forms = [tok[2] for tok in utterance]
    clause_mates = []
    pronoun_indices = [i for i, tok in enumerate(tokens) if is_relevant_pronoun(tok)]
    if not pronoun_indices:
        return []
    # All referential expressions in the utterance are clause mates
    for i, tok in enumerate(tokens):
        # Only consider referential expressions (pronouns, DPs, etc.)
        # Here, we treat all nouns and pronouns as referential for simplicity
        if re.match(r"^[A-ZÄÖÜ][a-zäöüß]+$", tok) or is_relevant_pronoun(tok):
            mate = {
                "token": tok,
                "index": i,
                "grammatical_role": utterance[i][3] if len(utterance[i]) > 3 else "",
                "thematic_role": utterance[i][4] if len(utterance[i]) > 4 else "",
                "animacy": "animate" if tok.lower() in {"er", "sie", "der", "die", "dieser", "diese"} else "inanimate",
                "sentence_position": i + 1,
                "linguistic_form": "pronoun" if is_relevant_pronoun(tok) else "DP",
                "givenness": "known" if "*" in utterance[i] else "new",
                "coreference": utterance[i][5] if len(utterance[i]) > 5 else "",
            }
            # Distance to each pronoun in the utterance
            mate["distances_to_pronouns"] = [abs(i - pi) for pi in pronoun_indices]
            clause_mates.append(mate)
    return clause_mates

def process_folder(folder, output_csv):
    with open(output_csv, "w", newline='', encoding="utf-8") as csvfile:
        fieldnames = [
            "file", "utterance_idx", "token", "grammatical_role", "thematic_role", "animacy",
            "sentence_position", "distances_to_pronouns", "linguistic_form", "coreference", "givenness",
            "num_clause_mates"
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for root, dirs, files in os.walk(folder):
            for file in files:
                if file.endswith(".tsv"):
                    utterances = parse_webanno_tsv(os.path.join(root, file))
                    for idx, utt in enumerate(utterances):
                        mates = extract_features(utt)
                        if mates:
                            num_mates = len(mates)
                            for mate in mates:
                                row = {
                                    "file": file,
                                    "utterance_idx": idx,
                                    "token": mate["token"],
                                    "grammatical_role": mate["grammatical_role"],
                                    "thematic_role": mate["thematic_role"],
                                    "animacy": mate["animacy"],
                                    "sentence_position": mate["sentence_position"],
                                    "distances_to_pronouns": ";".join(map(str, mate["distances_to_pronouns"])),
                                    "linguistic_form": mate["linguistic_form"],
                                    "coreference": mate["coreference"],
                                    "givenness": mate["givenness"],
                                    "num_clause_mates": num_mates
                                }
                                writer.writerow(row)

if __name__ == "__main__":
    # Set your curation folder path here
    curation_root = r"c:\Users\jobsc\sciebo\INF_Schepens\ind\robert\curation"
    output_csv = "clause_mates_export.csv"
    process_folder(curation_root, output_csv)
    print(f"Exported clause mates to {output_csv}")