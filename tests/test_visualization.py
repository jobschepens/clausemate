"""Tests for the visualization module."""

import tempfile
from pathlib import Path

from src.visualization import InteractiveVisualizer


class TestVisualizationImports:
    """Test visualization module imports."""

    def test_interactive_visualizer_import(self):
        """Test that InteractiveVisualizer can be imported."""
        # This test verifies that the import from __init__.py works
        assert InteractiveVisualizer is not None

        # Check that it's a class
        assert isinstance(InteractiveVisualizer, type)

    def test_interactive_visualizer_instantiation(self):
        """Test that InteractiveVisualizer can be instantiated."""
        # This should not raise an error
        with tempfile.TemporaryDirectory() as temp_dir:
            visualizer = InteractiveVisualizer(temp_dir)
            assert visualizer is not None
            assert visualizer.output_dir == Path(temp_dir)

    def test_interactive_visualizer_has_expected_methods(self):
        """Test that InteractiveVisualizer has expected public methods."""
        with tempfile.TemporaryDirectory() as temp_dir:
            visualizer = InteractiveVisualizer(temp_dir)

            # Check for key methods that should exist
            expected_methods = [
                "create_cross_chapter_network_visualization",
                "create_chapter_analysis_reports",
                "create_comparative_dashboard",
            ]

            for method_name in expected_methods:
                assert hasattr(visualizer, method_name)
                method = getattr(visualizer, method_name)
                assert callable(method)

    def test_module_docstring(self):
        """Test that the module has proper documentation."""
        import src.visualization

        assert src.visualization.__doc__ is not None
        assert "Visualization module" in src.visualization.__doc__

    def test_module_all_exports(self):
        """Test that __all__ exports work correctly."""
        import src.visualization

        assert hasattr(src.visualization, "__all__")
        assert "InteractiveVisualizer" in src.visualization.__all__

    def test_visualizer_logger(self):
        """Test that the visualizer has a logger."""
        with tempfile.TemporaryDirectory() as temp_dir:
            visualizer = InteractiveVisualizer(temp_dir)
            assert hasattr(visualizer, "logger")
            assert visualizer.logger is not None
