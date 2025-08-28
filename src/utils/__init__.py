"""Utilities package for the clause mates analyzer."""

# Import utility functions from the parent utils.py file
from pathlib import Path

# Add parent directory to path to import utils.py
utils_path = Path(__file__).parent.parent / "utils.py"
if utils_path.exists():
    import importlib.util

    spec = importlib.util.spec_from_file_location("utils_module", utils_path)
    if spec and spec.loader:
        utils_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(utils_module)

        extract_coreference_id = utils_module.extract_coreference_id
        extract_full_coreference_id = utils_module.extract_full_coreference_id
        extract_coreference_type = utils_module.extract_coreference_type
        determine_givenness = utils_module.determine_givenness
        extract_coref_base_and_occurrence = (
            utils_module.extract_coref_base_and_occurrence
        )
        extract_coref_link_numbers = utils_module.extract_coref_link_numbers
    else:
        # Fallback if spec creation fails
        def extract_coreference_id(value: str) -> str | None:
            """Extract coreference ID from a value string.

            Args:
                value: The value string to extract from.

            Returns:
                The extracted coreference ID or None if not found.
            """
            return None

        def extract_full_coreference_id(value: str) -> str | None:
            """Extract full coreference ID from a value string.

            Args:
                value: The value string to extract from.

            Returns:
                The extracted full coreference ID or None if not found.
            """
            return None

        def extract_coreference_type(value: str) -> str | None:
            """Extract coreference type from a value string.

            Args:
                value: The value string to extract from.

            Returns:
                The extracted coreference type or None if not found.
            """
            return None

        def determine_givenness(value: str) -> str:
            """Determine givenness from a value string.

            Args:
                value: The value string to analyze.

            Returns:
                The givenness value.
            """
            return "_"

        def extract_coref_base_and_occurrence(value: str):
            """Extract coreference base and occurrence numbers from a value string.

            Args:
                value: The value string to extract from.

            Returns:
                A tuple of (base_number, occurrence_number) or (None, None) if not found.
            """
            return None, None

        def extract_coref_link_numbers(value: str):
            """Extract coreference link numbers from a value string.

            Args:
                value: The value string to extract from.

            Returns:
                A tuple of (base_number, occurrence_number) or (None, None) if not found.
            """
            return None, None
else:
    # Fallback if utils.py doesn't exist
    def extract_coreference_id(value: str) -> str | None:
        """Extract coreference ID from a value string.

        Args:
            value: The value string to extract from.

        Returns:
            The extracted coreference ID or None if not found.
        """
        return None

    def extract_full_coreference_id(value: str) -> str | None:
        """Extract full coreference ID from a value string.

        Args:
            value: The value string to extract from.

        Returns:
            The extracted full coreference ID or None if not found.
        """
        return None

    def extract_coreference_type(value: str) -> str | None:
        """Extract coreference type from a value string.

        Args:
            value: The value string to extract from.

        Returns:
            The extracted coreference type or None if not found.
        """
        return None

    def determine_givenness(value: str) -> str:
        """Determine givenness from a value string.

        Args:
            value: The value string to analyze.

        Returns:
            The givenness value.
        """
        return "_"

    def extract_coref_base_and_occurrence(value: str):
        """Extract coreference base and occurrence numbers from a value string.

        Args:
            value: The value string to extract from.

        Returns:
            A tuple of (base_number, occurrence_number) or (None, None) if not found.
        """
        return None, None

    def extract_coref_link_numbers(value: str):
        """Extract coreference link numbers from a value string.

        Args:
            value: The value string to extract from.

        Returns:
            A tuple of (base_number, occurrence_number) or (None, None) if not found.
        """
        return None, None


__all__ = [
    "extract_coreference_id",
    "extract_full_coreference_id",
    "extract_coreference_type",
    "determine_givenness",
    "extract_coref_base_and_occurrence",
    "extract_coref_link_numbers",
]
