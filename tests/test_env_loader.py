"""Tests for environment loader utility."""

import os
import tempfile
from pathlib import Path
from unittest.mock import patch

from src.utils.env_loader import ensure_env_loaded, get_env_var, load_env_vars


class TestEnvLoader:
    """Test the environment loader utility functions."""

    def setup_method(self):
        """Set up test environment."""
        # Clean up any test environment variables
        test_vars = [
            "TEST_VAR1",
            "TEST_VAR2",
            "GEMINI_API_KEY",
            "GITHUB_PERSONAL_ACCESS_TOKEN",
        ]
        for var in test_vars:
            if var in os.environ:
                del os.environ[var]

    def teardown_method(self):
        """Clean up test environment."""
        # Clean up any test environment variables
        test_vars = [
            "TEST_VAR1",
            "TEST_VAR2",
            "GEMINI_API_KEY",
            "GITHUB_PERSONAL_ACCESS_TOKEN",
        ]
        for var in test_vars:
            if var in os.environ:
                del os.environ[var]

    def test_load_env_vars_nonexistent_file(self):
        """Test loading from non-existent .env file."""
        result = load_env_vars("nonexistent.env")
        assert result == {}
        assert isinstance(result, dict)

    def test_load_env_vars_empty_file(self):
        """Test loading from empty .env file."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".env", delete=False) as f:
            temp_file = f.name

        try:
            result = load_env_vars(temp_file)
            assert result == {}
        finally:
            Path(temp_file).unlink()

    def test_load_env_vars_with_variables(self):
        """Test loading environment variables from .env file."""
        env_content = """# Test environment file
TEST_VAR1=value1
TEST_VAR2="quoted value"
TEST_VAR3=unquoted_value
# Commented line
"""

        with tempfile.NamedTemporaryFile(mode="w", suffix=".env", delete=False) as f:
            f.write(env_content)
            temp_file = f.name

        try:
            result = load_env_vars(temp_file)

            # Check returned dictionary
            assert "TEST_VAR1" in result
            assert "TEST_VAR2" in result
            assert "TEST_VAR3" in result
            assert result["TEST_VAR1"] == "value1"
            assert result["TEST_VAR2"] == "quoted value"
            assert result["TEST_VAR3"] == "unquoted_value"

            # Check environment variables were set
            assert os.environ.get("TEST_VAR1") == "value1"
            assert os.environ.get("TEST_VAR2") == "quoted value"
            assert os.environ.get("TEST_VAR3") == "unquoted_value"

        finally:
            Path(temp_file).unlink()

    def test_load_env_vars_ignores_comments_and_empty_lines(self):
        """Test that comments and empty lines are ignored."""
        env_content = """
# This is a comment
TEST_VAR1=value1

# Another comment
TEST_VAR2=value2
"""

        with tempfile.NamedTemporaryFile(mode="w", suffix=".env", delete=False) as f:
            f.write(env_content)
            temp_file = f.name

        try:
            result = load_env_vars(temp_file)

            assert len(result) == 2
            assert "TEST_VAR1" in result
            assert "TEST_VAR2" in result

        finally:
            Path(temp_file).unlink()

    def test_get_env_var_with_value(self):
        """Test getting an environment variable that exists."""
        os.environ["TEST_VAR"] = "test_value"
        result = get_env_var("TEST_VAR")
        assert result == "test_value"

    def test_get_env_var_without_value(self):
        """Test getting an environment variable that doesn't exist."""
        result = get_env_var("NONEXISTENT_VAR")
        assert result is None

    def test_get_env_var_with_default(self):
        """Test getting an environment variable with default value."""
        result = get_env_var("NONEXISTENT_VAR", "default_value")
        assert result == "default_value"

    def test_get_env_var_with_existing_default(self):
        """Test getting an environment variable that exists ignores default."""
        os.environ["TEST_VAR"] = "existing_value"
        result = get_env_var("TEST_VAR", "default_value")
        assert result == "existing_value"

    @patch("src.utils.env_loader.load_env_vars")
    def test_ensure_env_loaded_no_keys(self, mock_load):
        """Test ensure_env_loaded when no API keys are set."""
        # Ensure no API keys are set
        assert "GEMINI_API_KEY" not in os.environ
        assert "GITHUB_PERSONAL_ACCESS_TOKEN" not in os.environ

        ensure_env_loaded()

        # Should call load_env_vars
        mock_load.assert_called_once()

    @patch("src.utils.env_loader.load_env_vars")
    def test_ensure_env_loaded_with_keys(self, mock_load):
        """Test ensure_env_loaded when API keys are already set."""
        # Set one of the API keys
        os.environ["GEMINI_API_KEY"] = "test_key"

        ensure_env_loaded()

        # Should not call load_env_vars since key is already set
        mock_load.assert_not_called()

    def test_load_env_vars_default_file(self):
        """Test loading with default .env file."""
        # This should work even if .env doesn't exist
        result = load_env_vars()
        assert isinstance(result, dict)

    def test_load_env_vars_custom_file(self):
        """Test loading with custom .env file path."""
        env_content = "CUSTOM_VAR=custom_value"

        with tempfile.NamedTemporaryFile(mode="w", suffix=".env", delete=False) as f:
            f.write(env_content)
            temp_file = f.name

        try:
            result = load_env_vars(temp_file)

            assert "CUSTOM_VAR" in result
            assert result["CUSTOM_VAR"] == "custom_value"
            assert os.environ.get("CUSTOM_VAR") == "custom_value"

        finally:
            Path(temp_file).unlink()
