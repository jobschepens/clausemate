"""Tests for the analyzers package."""

from abc import ABC

import pytest

from src.analyzers import (
    BaseAnalyzer,
    BaseClauseMateAnalyzer,
    BaseCoreferenceAnalyzer,
    BasePronounAnalyzer,
    BaseStatisticalAnalyzer,
    BaseValidationAnalyzer,
)
from src.data.models import ExtractionResult


class TestAnalyzerImports:
    """Test that analyzer imports work correctly."""

    def test_base_analyzer_import(self):
        """Test that BaseAnalyzer can be imported."""
        assert BaseAnalyzer is not None
        assert issubclass(BaseAnalyzer, ABC)

    def test_statistical_analyzer_import(self):
        """Test that BaseStatisticalAnalyzer can be imported."""
        assert BaseStatisticalAnalyzer is not None
        assert issubclass(BaseStatisticalAnalyzer, BaseAnalyzer)

    def test_coreference_analyzer_import(self):
        """Test that BaseCoreferenceAnalyzer can be imported."""
        assert BaseCoreferenceAnalyzer is not None
        assert issubclass(BaseCoreferenceAnalyzer, BaseAnalyzer)

    def test_pronoun_analyzer_import(self):
        """Test that BasePronounAnalyzer can be imported."""
        assert BasePronounAnalyzer is not None
        assert issubclass(BasePronounAnalyzer, BaseAnalyzer)

    def test_clause_mate_analyzer_import(self):
        """Test that BaseClauseMateAnalyzer can be imported."""
        assert BaseClauseMateAnalyzer is not None
        assert issubclass(BaseClauseMateAnalyzer, BaseAnalyzer)

    def test_validation_analyzer_import(self):
        """Test that BaseValidationAnalyzer can be imported."""
        assert BaseValidationAnalyzer is not None
        assert issubclass(BaseValidationAnalyzer, BaseAnalyzer)


class TestBaseAnalyzerInterface:
    """Test the BaseAnalyzer interface definition."""

    def test_abstract_methods(self):
        """Test that BaseAnalyzer has the expected abstract methods."""
        # Check that the class has the expected abstract methods
        expected_methods = ["analyze", "can_analyze"]
        for method_name in expected_methods:
            assert hasattr(BaseAnalyzer, method_name)
            # The methods should be abstract (defined but not implemented)
            method = getattr(BaseAnalyzer, method_name)
            assert callable(method)

    def test_is_abstract(self):
        """Test that BaseAnalyzer is abstract and cannot be instantiated."""
        with pytest.raises(TypeError):
            BaseAnalyzer()


class TestStatisticalAnalyzerInterface:
    """Test the BaseStatisticalAnalyzer interface."""

    def test_abstract_methods(self):
        """Test that BaseStatisticalAnalyzer has the expected abstract methods."""
        expected_methods = [
            "compute_descriptive_statistics",
            "compute_frequency_distributions",
            "compute_correlations",
        ]
        for method_name in expected_methods:
            assert hasattr(BaseStatisticalAnalyzer, method_name)

    def test_inheritance(self):
        """Test that BaseStatisticalAnalyzer inherits from BaseAnalyzer."""
        assert issubclass(BaseStatisticalAnalyzer, BaseAnalyzer)


class TestCoreferenceAnalyzerInterface:
    """Test the BaseCoreferenceAnalyzer interface."""

    def test_abstract_methods(self):
        """Test that BaseCoreferenceAnalyzer has the expected abstract methods."""
        expected_methods = [
            "analyze_coreference_patterns",
            "compute_chain_statistics",
            "analyze_animacy_patterns",
        ]
        for method_name in expected_methods:
            assert hasattr(BaseCoreferenceAnalyzer, method_name)


class TestPronounAnalyzerInterface:
    """Test the BasePronounAnalyzer interface."""

    def test_abstract_methods(self):
        """Test that BasePronounAnalyzer has the expected abstract methods."""
        expected_methods = [
            "analyze_pronoun_distribution",
            "analyze_pronoun_contexts",
            "analyze_antecedent_patterns",
        ]
        for method_name in expected_methods:
            assert hasattr(BasePronounAnalyzer, method_name)


class TestClauseMateAnalyzerInterface:
    """Test the BaseClauseMateAnalyzer interface."""

    def test_abstract_methods(self):
        """Test that BaseClauseMateAnalyzer has the expected abstract methods."""
        expected_methods = [
            "analyze_clause_mate_distribution",
            "analyze_syntactic_patterns",
            "analyze_thematic_role_patterns",
        ]
        for method_name in expected_methods:
            assert hasattr(BaseClauseMateAnalyzer, method_name)


class TestValidationAnalyzerInterface:
    """Test the BaseValidationAnalyzer interface."""

    def test_abstract_methods(self):
        """Test that BaseValidationAnalyzer has the expected abstract methods."""
        expected_methods = [
            "validate_data_consistency",
            "check_completeness",
            "identify_anomalies",
        ]
        for method_name in expected_methods:
            assert hasattr(BaseValidationAnalyzer, method_name)


class MockAnalyzer(BaseAnalyzer):
    """Mock implementation of BaseAnalyzer for testing."""

    def analyze(self, extraction_result: ExtractionResult) -> dict[str, bool]:
        """Mock analyze method."""
        return {"mock_result": True}

    def can_analyze(self, extraction_result: ExtractionResult) -> bool:
        """Mock can_analyze method."""
        return True


class TestMockAnalyzer:
    """Test the mock analyzer implementation."""

    def test_mock_analyzer_creation(self):
        """Test that MockAnalyzer can be instantiated."""
        analyzer = MockAnalyzer()
        assert analyzer is not None

    def test_mock_analyze(self):
        """Test the mock analyze method."""
        analyzer = MockAnalyzer()
        result = ExtractionResult(
            pronouns=[],
            phrases=[],
            relationships=[],
            coreference_chains=[],
            features={},
        )

        analysis_result = analyzer.analyze(result)
        assert analysis_result == {"mock_result": True}

    def test_mock_can_analyze(self):
        """Test the mock can_analyze method."""
        analyzer = MockAnalyzer()
        result = ExtractionResult(
            pronouns=[],
            phrases=[],
            relationships=[],
            coreference_chains=[],
            features={},
        )

        can_analyze = analyzer.can_analyze(result)
        assert can_analyze is True
