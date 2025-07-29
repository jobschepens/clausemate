"""Pytest configuration and fixtures for clause mate testing."""

import shutil
import tempfile
from pathlib import Path

import pandas as pd
import pytest

# Import mock data factory
from tests.fixtures.mock_data.mock_objects import MockDataFactory


@pytest.fixture(scope="session")
def test_data_dir():
    """Provide path to test data directory."""
    return Path(__file__).parent / "fixtures"


@pytest.fixture(scope="session")
def sample_tsv_files(test_data_dir):
    """Provide all sample TSV files for testing different formats."""
    return {
        "standard": test_data_dir / "sample_tsvs" / "standard_15col.tsv",
        "extended": test_data_dir / "sample_tsvs" / "extended_37col.tsv",
        "legacy": test_data_dir / "sample_tsvs" / "legacy_14col.tsv",
        "incomplete": test_data_dir / "sample_tsvs" / "incomplete_12col.tsv",
    }


@pytest.fixture(scope="session")
def expected_outputs_dir(test_data_dir):
    """Provide path to expected outputs directory."""
    return test_data_dir / "expected_outputs"


@pytest.fixture(scope="session")
def mock_data_dir(test_data_dir):
    """Provide path to mock data directory."""
    return test_data_dir / "mock_data"


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


@pytest.fixture
def mock_token():
    """Create a mock token for testing."""
    return MockDataFactory.create_mock_token()


@pytest.fixture
def mock_phrase():
    """Create a mock phrase for testing."""
    return MockDataFactory.create_mock_phrase()


@pytest.fixture
def mock_antecedent_info():
    """Create mock antecedent info for testing."""
    return MockDataFactory.create_mock_antecedent_info()


@pytest.fixture
def mock_sentence_context():
    """Create a mock sentence context for testing."""
    return MockDataFactory.create_mock_sentence_context()


@pytest.fixture
def mock_relationship():
    """Create a mock clause mate relationship for testing."""
    return MockDataFactory.create_mock_relationship()


@pytest.fixture(params=["standard", "extended", "legacy", "incomplete"])
def format_type(request):
    """Parametrized fixture for testing all TSV formats."""
    return request.param


@pytest.fixture
def format_test_data(format_type, sample_tsv_files):
    """Provide test data for specific format."""
    return {
        "format": format_type,
        "file_path": sample_tsv_files[format_type],
        "expected_columns": {
            "standard": 15,
            "extended": 37,
            "legacy": 14,
            "incomplete": 12,
        }[format_type],
    }


@pytest.fixture
def performance_thresholds():
    """Performance testing thresholds."""
    return {
        "max_processing_time": {
            "small": 1.0,  # < 100 rows
            "medium": 5.0,  # 100-1000 rows
            "large": 15.0,  # > 1000 rows
        },
        "max_memory_usage": 100,  # MB
        "min_relationships_per_second": 50,
    }


@pytest.fixture
def regression_test_config():
    """Configuration for regression testing."""
    return {
        "tolerance": 0.001,  # Floating point comparison tolerance
        "ignore_columns": [
            "processing_time",
            "timestamp",
        ],  # Columns to ignore in comparison
        "required_columns": [
            "sentence_num",
            "pronoun_text",
            "clause_mate_text",
            "pronoun_coref_ids",
            "clause_mate_coref_id",
        ],
    }


@pytest.fixture
def test_categories():
    """Test categorization markers."""
    return {
        "unit": "Unit tests for individual components",
        "integration": "Integration tests for component interaction",
        "slow": "Tests that take longer than 5 seconds",
        "regression": "Regression tests with golden master comparison",
        "performance": "Performance and benchmark tests",
    }
