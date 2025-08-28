"""Tests for the run_phase2 entry point script."""

import sys
from pathlib import Path


class TestRunPhase2EntryPoint:
    """Test the run_phase2.py entry point script."""

    def test_script_imports(self):
        """Test that the script can import required modules."""
        # Import the script module
        sys.path.insert(0, str(Path(__file__).parent.parent))

        try:
            import src.run_phase2

            assert src.run_phase2 is not None
        finally:
            # Clean up path
            if str(Path(__file__).parent.parent) in sys.path:
                sys.path.remove(str(Path(__file__).parent.parent))

    def test_main_function_import(self):
        """Test that the main function can be imported from the script."""
        # This test verifies that the script's imports work correctly
        script_path = Path(__file__).parent.parent / "src" / "run_phase2.py"

        with open(script_path) as f:
            content = f.read()

        # Verify the script imports the main function
        assert "from src.main import main" in content
        assert "main()" in content

    def test_script_structure(self):
        """Test that the script has the expected structure."""
        script_path = Path(__file__).parent.parent / "src" / "run_phase2.py"

        # Read the script content
        with open(script_path) as f:
            content = f.read()

        # Check for expected elements
        assert "#!/usr/bin/env python3" in content
        assert 'if __name__ == "__main__":' in content
        assert "sys.exit(main())" in content
        assert "from src.main import main" in content

    def test_path_setup(self):
        """Test that the script sets up the path correctly."""
        script_path = Path(__file__).parent.parent / "src" / "run_phase2.py"

        with open(script_path) as f:
            content = f.read()

        # Check that parent directory is added to path
        assert "parent_dir = Path(__file__).parent.parent" in content
        assert "sys.path.insert(0, str(parent_dir))" in content

    def test_script_execution_path(self):
        """Test that the script sets up execution path correctly."""
        # This test verifies that the script structure allows for proper execution
        script_path = Path(__file__).parent.parent / "src" / "run_phase2.py"

        with open(script_path) as f:
            content = f.read()

        # Verify the script has proper execution guards
        assert 'if __name__ == "__main__":' in content
        assert "sys.exit(" in content
        assert "main()" in content
