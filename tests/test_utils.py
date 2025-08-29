"""Tests for utils.py."""

from unittest.mock import MagicMock, patch

from src.utils import (
    determine_givenness,
    extract_coref_base_and_occurrence,
    extract_coref_link_numbers,
    extract_coreference_id,
    extract_coreference_type,
    extract_full_coreference_id,
)

# Note: Some functions are not exported by utils.__init__.py
# They would need to be imported directly from utils.py if needed


# Note: Some utility functions are not exported by the utils package
# Only testing the functions that are available from src.utils import


class TestExtractCoreferenceType:
    """Test the extract_coreference_type function."""

    def test_extract_coreference_type_valid_perspron(self):
        """Test extracting type from valid PersPron annotation."""
        result = extract_coreference_type("PersPron[127-4]")
        assert result == "PersPron"

    def test_extract_coreference_type_valid_dpron(self):
        """Test extracting type from valid D-Pron annotation."""
        result = extract_coreference_type("D-Pron[56-2]")
        assert result == "D-Pron"

    def test_extract_coreference_type_invalid_format(self):
        """Test extracting type from invalid format."""
        result = extract_coreference_type("invalid_format")
        assert result is None

    def test_extract_coreference_type_empty_string(self):
        """Test extracting type from empty string."""
        result = extract_coreference_type("")
        assert result is None

    def test_extract_coreference_type_missing_value(self):
        """Test extracting type from missing value placeholder."""
        result = extract_coreference_type("_")
        assert result is None


class TestExtractCoreferenceId:
    """Test the extract_coreference_id function."""

    def test_extract_coreference_id_full_format(self):
        """Test extracting ID from full format annotation."""
        result = extract_coreference_id("PersPron[127-4]")
        assert result == "127-4"

    def test_extract_coreference_id_base_only(self):
        """Test extracting ID from base-only format annotation."""
        result = extract_coreference_id("PersPron[127]")
        assert result == "127"

    def test_extract_coreference_id_invalid_format(self):
        """Test extracting ID from invalid format."""
        result = extract_coreference_id("invalid_format")
        assert result is None

    def test_extract_coreference_id_empty_string(self):
        """Test extracting ID from empty string."""
        result = extract_coreference_id("")
        assert result is None

    def test_extract_coreference_id_missing_value(self):
        """Test extracting ID from missing value placeholder."""
        result = extract_coreference_id("_")
        assert result is None


class TestExtractFullCoreferenceId:
    """Test the extract_full_coreference_id function."""

    def test_extract_full_coreference_id_valid_link(self):
        """Test extracting ID from valid coreference link."""
        result = extract_full_coreference_id("*->115-4")
        assert result == "115-4"

    def test_extract_full_coreference_id_base_only_link(self):
        """Test extracting ID from base-only coreference link."""
        result = extract_full_coreference_id("*->115")
        assert result == "115"

    def test_extract_full_coreference_id_invalid_format(self):
        """Test extracting ID from invalid coreference link format."""
        result = extract_full_coreference_id("invalid_format")
        assert result is None

    def test_extract_full_coreference_id_no_arrow(self):
        """Test extracting ID from coreference link without arrow."""
        result = extract_full_coreference_id("115-4")
        assert result is None

    def test_extract_full_coreference_id_empty_string(self):
        """Test extracting ID from empty string."""
        result = extract_full_coreference_id("")
        assert result is None

    def test_extract_full_coreference_id_missing_value(self):
        """Test extracting ID from missing value placeholder."""
        result = extract_full_coreference_id("_")
        assert result is None


class TestDetermineGivenness:
    """Test the determine_givenness function."""

    def test_determine_givenness_first_mention(self):
        """Test determining givenness for first mention."""
        result = determine_givenness("115-1")
        assert result == "neu"

    def test_determine_givenness_subsequent_mention(self):
        """Test determining givenness for subsequent mention."""
        result = determine_givenness("115-4")
        assert result == "bekannt"

    def test_determine_givenness_base_only(self):
        """Test determining givenness for base-only ID."""
        result = determine_givenness("115")
        assert result == "_"

    def test_determine_givenness_invalid_format(self):
        """Test determining givenness for invalid format."""
        result = determine_givenness("invalid")
        assert result == "_"

    def test_determine_givenness_empty_string(self):
        """Test determining givenness for empty string."""
        result = determine_givenness("")
        assert result == "_"

    def test_determine_givenness_missing_value(self):
        """Test determining givenness for missing value placeholder."""
        result = determine_givenness("_")
        assert result == "_"


# Note: extract_sentence_number is not exported by utils.__init__.py


class TestExtractCorefBaseAndOccurrence:
    """Test the extract_coref_base_and_occurrence function."""

    def test_extract_coref_base_and_occurrence_full_format(self):
        """Test extracting base and occurrence from full format."""
        base, occurrence = extract_coref_base_and_occurrence("115-4")
        assert base == 115
        assert occurrence == 4

    def test_extract_coref_base_and_occurrence_base_only(self):
        """Test extracting base and occurrence from base-only format."""
        base, occurrence = extract_coref_base_and_occurrence("115")
        assert base == 115
        assert occurrence is None

    def test_extract_coref_base_and_occurrence_invalid_format(self):
        """Test extracting base and occurrence from invalid format."""
        base, occurrence = extract_coref_base_and_occurrence("invalid")
        assert base is None
        assert occurrence is None

    def test_extract_coref_base_and_occurrence_empty_string(self):
        """Test extracting base and occurrence from empty string."""
        base, occurrence = extract_coref_base_and_occurrence("")
        assert base is None
        assert occurrence is None

    def test_extract_coref_base_and_occurrence_missing_value(self):
        """Test extracting base and occurrence from missing value placeholder."""
        base, occurrence = extract_coref_base_and_occurrence("_")
        assert base is None
        assert occurrence is None


class TestExtractCorefLinkNumbers:
    """Test the extract_coref_link_numbers function."""

    def test_extract_coref_link_numbers_valid_link(self):
        """Test extracting numbers from valid coreference link."""
        base, occurrence = extract_coref_link_numbers("*->115-4")
        assert base == 115
        assert occurrence == 4

    def test_extract_coref_link_numbers_base_only_link(self):
        """Test extracting numbers from base-only coreference link."""
        base, occurrence = extract_coref_link_numbers("*->115")
        assert base == 115
        assert occurrence is None

    def test_extract_coref_link_numbers_no_arrow(self):
        """Test extracting numbers from coreference link without arrow."""
        base, occurrence = extract_coref_link_numbers("115-4")
        assert base is None
        assert occurrence is None

    def test_extract_coref_link_numbers_invalid_format(self):
        """Test extracting numbers from invalid coreference link format."""
        base, occurrence = extract_coref_link_numbers("invalid")
        assert base is None
        assert occurrence is None

    def test_extract_coref_link_numbers_empty_string(self):
        """Test extracting numbers from empty string."""
        base, occurrence = extract_coref_link_numbers("")
        assert base is None
        assert occurrence is None

    def test_extract_coref_link_numbers_missing_value(self):
        """Test extracting numbers from missing value placeholder."""
        base, occurrence = extract_coref_link_numbers("_")
        assert base is None
        assert occurrence is None


class TestUtilsInitFallbackFunctions:
    """Test the fallback functions in utils/__init__.py."""

    @patch("importlib.util.spec_from_file_location")
    def test_fallback_functions_when_spec_creation_fails(self, mock_spec_from_file):
        """Test fallback functions when spec creation fails."""
        # Mock spec_from_file_location to return None
        mock_spec_from_file.return_value = None

        # Force reimport of the module to trigger fallback
        import sys

        if "src.utils" in sys.modules:
            del sys.modules["src.utils"]

        # Import with mocked spec
        with patch("pathlib.Path.exists", return_value=True):
            import src.utils as utils_module

        # Test fallback functions
        assert utils_module.extract_coreference_id("test") is None
        assert utils_module.extract_full_coreference_id("test") is None
        assert utils_module.extract_coreference_type("test") is None
        assert utils_module.determine_givenness("test") == "_"

        base, occurrence = utils_module.extract_coref_base_and_occurrence("test")
        assert base is None
        assert occurrence is None

        base, occurrence = utils_module.extract_coref_link_numbers("test")
        assert base is None
        assert occurrence is None

    @patch("pathlib.Path.exists")
    def test_fallback_functions_when_utils_file_not_exists(self, mock_exists):
        """Test fallback functions when utils.py file doesn't exist."""
        # Mock Path.exists to return False
        mock_exists.return_value = False

        # Force reimport of the module to trigger fallback
        import sys

        if "src.utils" in sys.modules:
            del sys.modules["src.utils"]

        # Import with mocked file existence
        import src.utils as utils_module

        # Test fallback functions
        assert utils_module.extract_coreference_id("test") is None
        assert utils_module.extract_full_coreference_id("test") is None
        assert utils_module.extract_coreference_type("test") is None
        assert utils_module.determine_givenness("test") == "_"

        base, occurrence = utils_module.extract_coref_base_and_occurrence("test")
        assert base is None
        assert occurrence is None

        base, occurrence = utils_module.extract_coref_link_numbers("test")
        assert base is None
        assert occurrence is None

    @patch("importlib.util.spec_from_file_location")
    def test_fallback_functions_when_spec_loader_is_none(self, mock_spec_from_file):
        """Test fallback functions when spec loader is None."""
        # Mock spec with None loader
        mock_spec = MagicMock()
        mock_spec.loader = None
        mock_spec_from_file.return_value = mock_spec

        # Force reimport of the module to trigger fallback
        import sys

        if "src.utils" in sys.modules:
            del sys.modules["src.utils"]

        # Import with mocked spec loader
        with patch("pathlib.Path.exists", return_value=True):
            import src.utils as utils_module

        # Test fallback functions
        assert utils_module.extract_coreference_id("test") is None
        assert utils_module.extract_full_coreference_id("test") is None
        assert utils_module.extract_coreference_type("test") is None
        assert utils_module.determine_givenness("test") == "_"

        base, occurrence = utils_module.extract_coref_base_and_occurrence("test")
        assert base is None
        assert occurrence is None

        base, occurrence = utils_module.extract_coref_link_numbers("test")
        assert base is None
        assert occurrence is None

    def test_fallback_function_signatures(self):
        """Test that fallback functions have correct signatures and behavior."""
        # Force reimport to ensure we're testing fallback functions
        import sys

        if "src.utils" in sys.modules:
            del sys.modules["src.utils"]

        # Mock to force fallback path
        with patch("pathlib.Path.exists", return_value=False):
            import src.utils as utils_module

        # Test extract_coreference_id
        assert utils_module.extract_coreference_id("any_value") is None
        assert utils_module.extract_coreference_id("") is None

        # Test extract_full_coreference_id
        assert utils_module.extract_full_coreference_id("any_value") is None
        assert utils_module.extract_full_coreference_id("") is None

        # Test extract_coreference_type
        assert utils_module.extract_coreference_type("any_value") is None
        assert utils_module.extract_coreference_type("") is None

        # Test determine_givenness
        assert utils_module.determine_givenness("any_value") == "_"
        assert utils_module.determine_givenness("") == "_"

        # Test extract_coref_base_and_occurrence
        base, occurrence = utils_module.extract_coref_base_and_occurrence("any_value")
        assert base is None
        assert occurrence is None

        # Test extract_coref_link_numbers
        base, occurrence = utils_module.extract_coref_link_numbers("any_value")
        assert base is None
        assert occurrence is None

    def test_utils_init_all_exports(self):
        """Test that __all__ exports are properly defined."""
        import src.utils as utils_module

        # Check that all expected functions are in __all__
        expected_exports = [
            "extract_coreference_id",
            "extract_full_coreference_id",
            "extract_coreference_type",
            "determine_givenness",
            "extract_coref_base_and_occurrence",
            "extract_coref_link_numbers",
        ]

        for export in expected_exports:
            assert hasattr(utils_module, export), f"Missing export: {export}"
            assert export in utils_module.__all__, f"Export not in __all__: {export}"
