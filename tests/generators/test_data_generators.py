"""Test data generators for synthetic TSV files with known characteristics."""

import random
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from tests.fixtures.mock_data.mock_objects import MockDataFactory


@dataclass
class TSVGenerationConfig:
    """Configuration for TSV file generation."""

    num_sentences: int = 10
    tokens_per_sentence_range: tuple = (5, 15)
    pronoun_probability: float = 0.3
    coreference_probability: float = 0.4
    format_type: str = "standard"  # standard, extended, legacy, incomplete
    include_errors: bool = False
    error_probability: float = 0.1


class SyntheticTSVGenerator:
    """Generator for synthetic TSV files with controlled characteristics."""

    def __init__(self, config: TSVGenerationConfig | None = None):
        """Initialize the generator with configuration."""
        self.config = config or TSVGenerationConfig()
        self.mock_factory = MockDataFactory()

        # Predefined word lists for realistic text generation
        self.nouns = [
            "cat",
            "dog",
            "house",
            "car",
            "book",
            "table",
            "chair",
            "computer",
            "phone",
            "tree",
            "flower",
            "bird",
            "fish",
            "mountain",
            "river",
        ]

        self.verbs = [
            "runs",
            "walks",
            "sits",
            "stands",
            "reads",
            "writes",
            "thinks",
            "speaks",
            "listens",
            "watches",
            "plays",
            "works",
            "sleeps",
            "eats",
            "drinks",
        ]

        self.adjectives = [
            "big",
            "small",
            "red",
            "blue",
            "fast",
            "slow",
            "happy",
            "sad",
            "bright",
            "dark",
            "old",
            "new",
            "hot",
            "cold",
            "beautiful",
        ]

        self.pronouns = [
            "he",
            "she",
            "it",
            "they",
            "him",
            "her",
            "them",
            "his",
            "hers",
            "its",
        ]

        self.determiners = ["the", "a", "an", "this", "that", "these", "those"]

    def generate_word(self, word_type: str = "noun") -> str:
        """Generate a word of the specified type."""
        word_lists = {
            "noun": self.nouns,
            "verb": self.verbs,
            "adjective": self.adjectives,
            "pronoun": self.pronouns,
            "determiner": self.determiners,
        }
        return random.choice(word_lists.get(word_type, self.nouns))

    def generate_sentence_tokens(
        self, sentence_num: int, num_tokens: int
    ) -> list[dict[str, Any]]:
        """Generate tokens for a single sentence."""
        tokens = []
        coreference_id = None

        # Decide if this sentence will have coreference
        if random.random() < self.config.coreference_probability:
            coreference_id = f"coref_{sentence_num}_{random.randint(1, 5)}"

        for token_idx in range(1, num_tokens + 1):
            # Decide token type based on position and probability
            if token_idx == 1:
                word_type = "determiner" if random.random() < 0.3 else "noun"
            elif token_idx == num_tokens:
                word_type = "noun"
            elif random.random() < self.config.pronoun_probability:
                word_type = "pronoun"
            elif random.random() < 0.4:
                word_type = "verb"
            elif random.random() < 0.3:
                word_type = "adjective"
            else:
                word_type = "noun"

            word = self.generate_word(word_type)

            # Generate token data based on format type
            token_data = {
                "idx": token_idx,
                "text": word,
                "sentence_num": sentence_num,
                "lemma": word.lower(),
                "pos_tag": self._get_pos_tag(word_type),
                "grammatical_role": self._get_grammatical_role(token_idx, num_tokens),
                "thematic_role": self._get_thematic_role(word_type),
            }

            # Add coreference information if applicable
            if word_type == "pronoun" and coreference_id:
                token_data.update(
                    {
                        "coreference_id": coreference_id,
                        "coreference_type": "IDENT",
                        "coreference_link": f"{coreference_id}_link",
                        "coreference_link_type": "IDENT",
                    }
                )

            # Add format-specific columns
            if self.config.format_type == "extended":
                token_data.update(self._get_extended_columns(word_type))
            elif self.config.format_type == "incomplete":
                # Remove some columns for incomplete format
                token_data.pop("thematic_role", None)
                token_data.pop("coreference_link", None)

            tokens.append(token_data)

        return tokens

    def _get_pos_tag(self, word_type: str) -> str:
        """Get POS tag for word type."""
        pos_mapping = {
            "noun": "NN",
            "verb": "VB",
            "adjective": "JJ",
            "pronoun": "PRP",
            "determiner": "DT",
        }
        return pos_mapping.get(word_type, "NN")

    def _get_grammatical_role(self, token_idx: int, total_tokens: int) -> str:
        """Get grammatical role based on position."""
        if token_idx == 1:
            return "SUBJ"
        elif token_idx == total_tokens:
            return "OBJ"
        elif token_idx == 2:
            return "PRED"
        else:
            return random.choice(["ATTR", "ADV", "OTHER"])

    def _get_thematic_role(self, word_type: str) -> str:
        """Get thematic role for word type."""
        role_mapping = {
            "noun": random.choice(["AGENT", "PATIENT", "THEME"]),
            "pronoun": random.choice(["AGENT", "PATIENT"]),
            "verb": "PREDICATE",
            "adjective": "ATTRIBUTE",
            "determiner": "DETERMINER",
        }
        return role_mapping.get(word_type, "OTHER")

    def _get_extended_columns(self, word_type: str) -> dict[str, Any]:
        """Get additional columns for extended format."""
        return {
            "animacy": "ANIMATE" if word_type in ["noun", "pronoun"] else "INANIMATE",
            "givenness": random.choice(["GIVEN", "NEW", "ACCESSIBLE"]),
            "information_status": random.choice(["FOCUS", "BACKGROUND", "TOPIC"]),
            "semantic_role": self._get_thematic_role(word_type),
            "discourse_function": random.choice(["MAIN", "SUBORDINATE", "COORDINATE"]),
        }

    def generate_tsv_content(self) -> str:
        """Generate complete TSV file content."""
        lines = []

        # Add format header
        if self.config.format_type == "standard":
            lines.append("#FORMAT=WebAnno TSV 3.6.1")
        elif self.config.format_type == "extended":
            lines.append("#FORMAT=WebAnno TSV 3.6.1 Extended")
        elif self.config.format_type == "legacy":
            lines.append("#FORMAT=WebAnno TSV 3.5.0")
        else:
            lines.append("#FORMAT=WebAnno TSV 3.6.1 Incomplete")

        lines.append("")  # Empty line after header

        # Generate sentences
        for sentence_num in range(1, self.config.num_sentences + 1):
            # Add sentence text line
            num_tokens = random.randint(*self.config.tokens_per_sentence_range)
            tokens = self.generate_sentence_tokens(sentence_num, num_tokens)

            sentence_text = " ".join(token["text"] for token in tokens)
            lines.append(f"#Text={sentence_text}")

            # Add token lines
            for token in tokens:
                token_line = self._format_token_line(token, sentence_num)

                # Introduce errors if configured
                if (
                    self.config.include_errors
                    and random.random() < self.config.error_probability
                ):
                    token_line = self._introduce_error(token_line)

                lines.append(token_line)

            lines.append("")  # Empty line after sentence

        return "\n".join(lines)

    def _format_token_line(self, token: dict[str, Any], sentence_num: int) -> str:
        """Format a token as a TSV line."""
        # Base columns for all formats
        columns = [
            f"{sentence_num}-{token['idx']}",  # Token ID
            token["text"],  # Text
            token["lemma"],  # Lemma
            token["pos_tag"],  # POS tag
            token["grammatical_role"],  # Grammatical role
            token["thematic_role"],  # Thematic role
        ]

        # Add coreference columns
        columns.extend(
            [
                token.get("coreference_id", "_"),
                token.get("coreference_type", "_"),
                token.get("coreference_link", "_"),
                token.get("coreference_link_type", "_"),
            ]
        )

        # Add format-specific columns
        if self.config.format_type == "standard":
            # Standard 15-column format
            columns.extend(["_"] * 5)  # Additional standard columns
        elif self.config.format_type == "extended":
            # Extended 37-column format
            extended_data = self._get_extended_columns(token.get("text", ""))
            columns.extend(
                [
                    extended_data.get("animacy", "_"),
                    extended_data.get("givenness", "_"),
                    extended_data.get("information_status", "_"),
                    extended_data.get("semantic_role", "_"),
                    extended_data.get("discourse_function", "_"),
                ]
            )
            columns.extend(["_"] * 22)  # Fill remaining columns
        elif self.config.format_type == "legacy":
            # Legacy 14-column format
            columns.extend(["_"] * 4)
        elif self.config.format_type == "incomplete":
            # Incomplete 12-column format - remove some columns
            columns = columns[:8] + ["_"] * 4

        return "\t".join(columns)

    def _introduce_error(self, token_line: str) -> str:
        """Introduce a random error into a token line."""
        error_types = [
            "missing_column",
            "extra_column",
            "malformed_id",
            "empty_required_field",
        ]

        error_type = random.choice(error_types)
        columns = token_line.split("\t")

        if error_type == "missing_column" and len(columns) > 5:
            # Remove a random column
            columns.pop(random.randint(2, len(columns) - 1))
        elif error_type == "extra_column":
            # Add an extra column
            columns.insert(random.randint(2, len(columns)), "EXTRA")
        elif error_type == "malformed_id":
            # Malform the token ID
            columns[0] = "MALFORMED_ID"
        elif error_type == "empty_required_field":
            # Empty a required field
            if len(columns) > 1:
                columns[1] = ""

        return "\t".join(columns)

    def generate_file(self, output_path: Path) -> None:
        """Generate and save a TSV file."""
        content = self.generate_tsv_content()
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(content, encoding="utf-8")

    def generate_test_suite(self, output_dir: Path) -> dict[str, Path]:
        """Generate a complete test suite with different file types."""
        output_dir.mkdir(parents=True, exist_ok=True)
        generated_files = {}

        # Generate files for each format type
        formats = ["standard", "extended", "legacy", "incomplete"]

        for format_type in formats:
            # Clean files
            config = TSVGenerationConfig(
                num_sentences=10, format_type=format_type, include_errors=False
            )
            generator = SyntheticTSVGenerator(config)
            clean_file = output_dir / f"synthetic_{format_type}_clean.tsv"
            generator.generate_file(clean_file)
            generated_files[f"{format_type}_clean"] = clean_file

            # Files with errors
            config.include_errors = True
            config.error_probability = 0.2
            generator = SyntheticTSVGenerator(config)
            error_file = output_dir / f"synthetic_{format_type}_errors.tsv"
            generator.generate_file(error_file)
            generated_files[f"{format_type}_errors"] = error_file

        # Generate edge case files
        edge_cases = [
            (
                "minimal",
                TSVGenerationConfig(num_sentences=1, tokens_per_sentence_range=(1, 3)),
            ),
            (
                "large",
                TSVGenerationConfig(
                    num_sentences=100, tokens_per_sentence_range=(10, 25)
                ),
            ),
            (
                "high_coreference",
                TSVGenerationConfig(
                    coreference_probability=0.8, pronoun_probability=0.6
                ),
            ),
            (
                "no_coreference",
                TSVGenerationConfig(
                    coreference_probability=0.0, pronoun_probability=0.1
                ),
            ),
        ]

        for case_name, config in edge_cases:
            generator = SyntheticTSVGenerator(config)
            case_file = output_dir / f"synthetic_{case_name}.tsv"
            generator.generate_file(case_file)
            generated_files[case_name] = case_file

        return generated_files


def generate_test_data_suite():
    """Generate a complete test data suite for the project."""
    output_dir = Path("tests/fixtures/generated_data")
    generator = SyntheticTSVGenerator()
    return generator.generate_test_suite(output_dir)


if __name__ == "__main__":
    # Generate test data when run directly
    files = generate_test_data_suite()
    print("Generated test files:")
    for name, path in files.items():
        print(f"  {name}: {path}")
