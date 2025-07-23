"""Pytest configuration and fixtures for clause mate testing."""

import shutil
import tempfile
from pathlib import Path

import pandas as pd
import pytest


@pytest.fixture(scope="session")
def test_data_dir():
    """Provide path to test data directory."""
    return Path(__file__).parent / "fixtures"


@pytest.fixture(scope="session")
def sample_tsv_file(test_data_dir):
    """Provide sample TSV file for testing."""
    return test_data_dir / "sample_input.tsv"


@pytest.fixture
def temp_output_dir():
    """Create temporary directory for test outputs."""
    temp_dir = tempfile.mkdtemp()
    yield Path(temp_dir)
    shutil.rmtree(temp_dir)


@pytest.fixture
def mock_config(temp_output_dir):
    """Provide mock configuration for testing."""
    return {
        "input_file": "tests/fixtures/sample_input.tsv",
        "output_file": str(temp_output_dir / "test_output.csv"),
    }


@pytest.fixture
def expected_columns():
    """Standard column names for output validation."""
    return [
        "sentence_id",
        "sentence_id_numeric",
        "sentence_id_prefixed",
        "sentence_num",
        "first_words",
        "pronoun_text",
        "pronoun_token_idx",
        "pronoun_grammatical_role",
        "pronoun_thematic_role",
        "pronoun_givenness",
        "pronoun_coref_ids",
        "pronoun_coref_base_num",
        "pronoun_coref_occurrence_num",
        "pronoun_coreference_link",
        "pronoun_coref_link_base_num",
        "pronoun_coref_link_occurrence_num",
        "pronoun_coreference_type",
        "pronoun_inanimate_coreference_link",
        "pronoun_inanimate_coref_link_base_num",
        "pronoun_inanimate_coref_link_occurrence_num",
        "pronoun_inanimate_coreference_type",
        "pronoun_most_recent_antecedent_text",
        "pronoun_most_recent_antecedent_distance",
        "pronoun_first_antecedent_text",
        "pronoun_first_antecedent_distance",
        "pronoun_antecedent_choice",
        "num_clause_mates",
        "clause_mate_text",
        "clause_mate_coref_id",
        "clause_mate_coref_base_num",
        "clause_mate_coref_occurrence_num",
        "clause_mate_start_idx",
        "clause_mate_end_idx",
        "clause_mate_grammatical_role",
        "clause_mate_thematic_role",
        "clause_mate_coreference_type",
        "clause_mate_animacy",
        "clause_mate_givenness",
    ]


@pytest.fixture
def benchmark_data():
    """Performance benchmarking data."""
    return {
        "max_processing_time": 30,  # seconds
        "max_memory_usage": 500,  # MB
        "expected_output_size": (400, 450),  # rows range
    }


class TestDataValidator:
    """Utility class for validating test data."""

    @staticmethod
    def validate_csv_structure(csv_path: Path, expected_columns: list) -> bool:
        """Validate CSV has expected structure."""
        df = pd.read_csv(csv_path)
        return list(df.columns) == expected_columns

    @staticmethod
    def validate_reproducibility(csv1: Path, csv2: Path) -> bool:
        """Check if two CSV files are identical."""
        df1 = pd.read_csv(csv1)
        df2 = pd.read_csv(csv2)
        return df1.equals(df2)

    @staticmethod
    def validate_data_quality(csv_path: Path) -> dict:
        """Perform data quality checks."""
        df = pd.read_csv(csv_path)
        return {
            "total_rows": len(df),
            "missing_values": df.isnull().sum().sum(),
            "unique_sentences": df["sentence_id"].nunique(),
            "unique_pronouns": df["pronoun_text"].nunique(),
            "data_types_valid": all(df.dtypes.notna()),
        }
