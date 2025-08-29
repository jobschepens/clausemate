"""Tests for preamble_parser.py."""

import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest

from src.parsers.preamble_parser import (
    AnnotationSchema,
    PreambleParser,
    extract_preamble_from_file,
)


class TestAnnotationSchema:
    """Test the AnnotationSchema dataclass."""

    def test_annotation_schema_creation(self):
        """Test creating an AnnotationSchema instance."""
        span_annotations = [{"type": "POS", "features": ["pos"]}]
        chain_annotations = [
            {"type": "CoreferenceLink", "features": ["referenceRelation"]}
        ]
        relation_annotations = [
            {"type": "Dependency", "features": ["head", "relation"]}
        ]
        column_mapping = {"POS|pos": 4, "CoreferenceLink|referenceRelation": 5}
        total_columns = 6

        schema = AnnotationSchema(
            span_annotations=span_annotations,
            chain_annotations=chain_annotations,
            relation_annotations=relation_annotations,
            column_mapping=column_mapping,
            total_columns=total_columns,
        )

        assert schema.span_annotations == span_annotations
        assert schema.chain_annotations == chain_annotations
        assert schema.relation_annotations == relation_annotations
        assert schema.column_mapping == column_mapping
        assert schema.total_columns == total_columns


class TestPreambleParser:
    """Test the PreambleParser class."""

    def setup_method(self):
        """Set up test fixtures."""
        self.parser = PreambleParser()

    def test_initialization(self):
        """Test that the parser initializes correctly."""
        assert self.parser.schema is None
        assert self.parser.column_mapping == {}
        assert self.parser.total_columns == 0

    def test_reset(self):
        """Test parser reset functionality."""
        # Set some state
        self.parser.schema = "test_schema"
        self.parser.column_mapping = {"test": 1}
        self.parser.total_columns = 5

        # Reset
        self.parser.reset()

        assert self.parser.schema is None
        assert self.parser.column_mapping == {}
        assert self.parser.total_columns == 0

    def test_parse_preamble_lines_span_annotations(self):
        """Test parsing preamble lines with span annotations."""
        preamble_lines = [
            "#T_SP=POS|pos|lemma",
            "#T_SP=MorphologicalFeatures|case|number|gender",
        ]

        result = self.parser.parse_preamble_lines(preamble_lines)

        assert isinstance(result, AnnotationSchema)
        assert len(result.span_annotations) == 2
        assert result.span_annotations[0]["type"] == "POS"
        assert result.span_annotations[0]["features"] == ["pos", "lemma"]
        assert result.span_annotations[1]["type"] == "MorphologicalFeatures"
        assert result.span_annotations[1]["features"] == ["case", "number", "gender"]

    def test_parse_preamble_lines_chain_annotations(self):
        """Test parsing preamble lines with chain annotations."""
        preamble_lines = [
            "#T_CH=CoreferenceLink|referenceRelation|referenceType",
        ]

        result = self.parser.parse_preamble_lines(preamble_lines)

        assert isinstance(result, AnnotationSchema)
        assert len(result.chain_annotations) == 1
        assert result.chain_annotations[0]["type"] == "CoreferenceLink"
        assert result.chain_annotations[0]["features"] == [
            "referenceRelation",
            "referenceType",
        ]

    def test_parse_preamble_lines_relation_annotations(self):
        """Test parsing preamble lines with relation annotations."""
        preamble_lines = [
            "#T_RL=Dependency|head|relation",
        ]

        result = self.parser.parse_preamble_lines(preamble_lines)

        assert isinstance(result, AnnotationSchema)
        assert len(result.relation_annotations) == 1
        assert result.relation_annotations[0]["type"] == "Dependency"
        assert result.relation_annotations[0]["features"] == ["head", "relation"]

    def test_parse_preamble_lines_mixed_annotations(self):
        """Test parsing preamble lines with mixed annotation types."""
        preamble_lines = [
            "#T_SP=POS|pos",
            "#T_CH=CoreferenceLink|referenceRelation",
            "#T_RL=Dependency|head",
        ]

        result = self.parser.parse_preamble_lines(preamble_lines)

        assert isinstance(result, AnnotationSchema)
        assert len(result.span_annotations) == 1
        assert len(result.chain_annotations) == 1
        assert len(result.relation_annotations) == 1

    def test_parse_preamble_lines_empty_features(self):
        """Test parsing preamble lines with empty features."""
        preamble_lines = [
            "#T_SP=POS|",
            "#T_SP=MorphologicalFeatures|case||gender",
        ]

        result = self.parser.parse_preamble_lines(preamble_lines)

        assert isinstance(result, AnnotationSchema)
        assert len(result.span_annotations) == 2
        assert result.span_annotations[0]["features"] == [""]  # Empty feature
        assert result.span_annotations[1]["features"] == ["case", "", "gender"]

    def test_calculate_column_positions_simple_span(self):
        """Test column position calculation for simple span annotations."""
        schema = {
            "span_annotations": [{"type": "POS", "features": []}],
            "chain_annotations": [],
            "relation_annotations": [],
        }

        column_mapping, total_columns = self.parser._calculate_column_positions(schema)

        assert column_mapping["POS"] == 4  # First annotation starts at column 4
        assert total_columns == 4

    def test_calculate_column_positions_span_with_features(self):
        """Test column position calculation for span annotations with features."""
        schema = {
            "span_annotations": [{"type": "POS", "features": ["pos", "lemma"]}],
            "chain_annotations": [],
            "relation_annotations": [],
        }

        column_mapping, total_columns = self.parser._calculate_column_positions(schema)

        assert column_mapping["POS|pos"] == 4
        assert column_mapping["POS|lemma"] == 5
        assert total_columns == 5

    def test_calculate_column_positions_mixed_annotations(self):
        """Test column position calculation for mixed annotation types."""
        schema = {
            "span_annotations": [{"type": "POS", "features": ["pos"]}],
            "chain_annotations": [
                {"type": "CoreferenceLink", "features": ["referenceRelation"]}
            ],
            "relation_annotations": [{"type": "Dependency", "features": ["head"]}],
        }

        column_mapping, total_columns = self.parser._calculate_column_positions(schema)

        # Span annotations first
        assert column_mapping["POS|pos"] == 4
        # Chain annotations second
        assert column_mapping["CoreferenceLink|referenceRelation"] == 5
        # Relation annotations last
        assert column_mapping["Dependency|head"] == 6
        assert total_columns == 6

    def test_calculate_column_positions_empty_features(self):
        """Test column position calculation with empty features."""
        schema = {
            "span_annotations": [{"type": "POS", "features": ["", "pos"]}],
            "chain_annotations": [],
            "relation_annotations": [],
        }

        column_mapping, total_columns = self.parser._calculate_column_positions(schema)

        assert column_mapping["POS|_"] == 4  # Empty feature
        assert column_mapping["POS|pos"] == 5
        assert total_columns == 5

    def test_get_coreference_columns_no_schema(self):
        """Test getting coreference columns when no schema is set."""
        result = self.parser.get_coreference_columns()
        assert result == {}

    def test_get_coreference_columns_with_schema(self):
        """Test getting coreference columns with schema."""
        # Set up a mock schema
        self.parser.schema = AnnotationSchema(
            span_annotations=[],
            chain_annotations=[],
            relation_annotations=[],
            column_mapping={
                "CoreferenceLink|referenceRelation": 5,
                "CoreferenceLink|referenceType": 6,
                "POS|pos": 4,
            },
            total_columns=6,
        )

        result = self.parser.get_coreference_columns()

        assert len(result) == 2
        assert result["CoreferenceLink|referenceRelation"] == 5
        assert result["CoreferenceLink|referenceType"] == 6

    def test_get_morphological_columns_no_schema(self):
        """Test getting morphological columns when no schema is set."""
        result = self.parser.get_morphological_columns()
        assert result == {}

    def test_get_morphological_columns_with_schema(self):
        """Test getting morphological columns with schema."""
        # Set up a mock schema
        self.parser.schema = AnnotationSchema(
            span_annotations=[],
            chain_annotations=[],
            relation_annotations=[],
            column_mapping={
                "MorphologicalFeatures|case": 5,
                "MorphologicalFeatures|number": 6,
                "POS|pos": 4,
            },
            total_columns=6,
        )

        result = self.parser.get_morphological_columns()

        assert len(result) == 2
        assert result["MorphologicalFeatures|case"] == 5
        assert result["MorphologicalFeatures|number"] == 6

    def test_get_pronoun_type_column_no_schema(self):
        """Test getting pronoun type column when no schema is set."""
        result = self.parser.get_pronoun_type_column()
        assert result is None

    def test_get_pronoun_type_column_found(self):
        """Test getting pronoun type column when found."""
        # Set up a mock schema
        self.parser.schema = AnnotationSchema(
            span_annotations=[],
            chain_annotations=[],
            relation_annotations=[],
            column_mapping={
                "MorphologicalFeatures|pronType": 5,
                "POS|pos": 4,
            },
            total_columns=5,
        )

        result = self.parser.get_pronoun_type_column()
        assert result == 5

    def test_get_pronoun_type_column_not_found(self):
        """Test getting pronoun type column when not found."""
        # Set up a mock schema without pronType
        self.parser.schema = AnnotationSchema(
            span_annotations=[],
            chain_annotations=[],
            relation_annotations=[],
            column_mapping={
                "MorphologicalFeatures|case": 5,
                "POS|pos": 4,
            },
            total_columns=5,
        )

        result = self.parser.get_pronoun_type_column()
        assert result is None

    def test_get_coreference_link_column_no_schema(self):
        """Test getting coreference link column when no schema is set."""
        result = self.parser.get_coreference_link_column()
        assert result is None

    def test_get_coreference_link_column_found(self):
        """Test getting coreference link column when found."""
        # Set up a mock schema
        self.parser.schema = AnnotationSchema(
            span_annotations=[],
            chain_annotations=[],
            relation_annotations=[],
            column_mapping={
                "CoreferenceLink|referenceRelation": 5,
                "POS|pos": 4,
            },
            total_columns=5,
        )

        result = self.parser.get_coreference_link_column()
        assert result == 5

    def test_get_coreference_type_column_no_schema(self):
        """Test getting coreference type column when no schema is set."""
        result = self.parser.get_coreference_type_column()
        assert result is None

    def test_get_coreference_type_column_found(self):
        """Test getting coreference type column when found."""
        # Set up a mock schema
        self.parser.schema = AnnotationSchema(
            span_annotations=[],
            chain_annotations=[],
            relation_annotations=[],
            column_mapping={
                "CoreferenceLink|referenceType": 6,
                "POS|pos": 4,
            },
            total_columns=6,
        )

        result = self.parser.get_coreference_type_column()
        assert result == 6

    def test_get_grammatical_role_column_no_schema(self):
        """Test getting grammatical role column when no schema is set."""
        result = self.parser.get_grammatical_role_column()
        assert result is None

    def test_get_grammatical_role_column_found(self):
        """Test getting grammatical role column when found."""
        # Set up a mock schema
        self.parser.schema = AnnotationSchema(
            span_annotations=[],
            chain_annotations=[],
            relation_annotations=[],
            column_mapping={
                "GrammatischeRolle|grammatischeRolle": 7,
                "POS|pos": 4,
            },
            total_columns=7,
        )

        result = self.parser.get_grammatical_role_column()
        assert result == 7

    def test_get_thematic_role_column_no_schema(self):
        """Test getting thematic role column when no schema is set."""
        result = self.parser.get_thematic_role_column()
        assert result is None

    def test_get_thematic_role_column_found(self):
        """Test getting thematic role column when found."""
        # Set up a mock schema
        self.parser.schema = AnnotationSchema(
            span_annotations=[],
            chain_annotations=[],
            relation_annotations=[],
            column_mapping={
                "GrammatischeRolle|thematischeRolle": 8,
                "POS|pos": 4,
            },
            total_columns=8,
        )

        result = self.parser.get_thematic_role_column()
        assert result == 8


class TestExtractPreambleFromFile:
    """Test the extract_preamble_from_file function."""

    def test_extract_preamble_from_file_success(self):
        """Test successful preamble extraction from file."""
        # Create a temporary file with preamble
        with tempfile.NamedTemporaryFile(mode="w", suffix=".tsv", delete=False) as f:
            f.write("#T_SP=POS|pos\n")
            f.write("#T_CH=CoreferenceLink|referenceRelation\n")
            f.write("# Comment line\n")
            f.write("\n")  # Empty line
            f.write("1-1\t0-4\tKarl\tKarl\tNOUN\n")  # First data line
            temp_file = f.name

        try:
            result = extract_preamble_from_file(temp_file)

            assert len(result) == 3
            assert result[0] == "#T_SP=POS|pos"
            assert result[1] == "#T_CH=CoreferenceLink|referenceRelation"
            assert result[2] == "# Comment line"

        finally:
            Path(temp_file).unlink()

    def test_extract_preamble_from_file_no_preamble(self):
        """Test preamble extraction when file has no preamble."""
        # Create a temporary file with no preamble
        with tempfile.NamedTemporaryFile(mode="w", suffix=".tsv", delete=False) as f:
            f.write("1-1\t0-4\tKarl\tKarl\tNOUN\n")  # First data line
            temp_file = f.name

        try:
            result = extract_preamble_from_file(temp_file)
            assert result == []

        finally:
            Path(temp_file).unlink()

    def test_extract_preamble_from_file_empty_file(self):
        """Test preamble extraction from empty file."""
        # Create an empty temporary file
        with tempfile.NamedTemporaryFile(mode="w", suffix=".tsv", delete=False) as f:
            temp_file = f.name

        try:
            result = extract_preamble_from_file(temp_file)
            assert result == []

        finally:
            Path(temp_file).unlink()

    def test_extract_preamble_from_file_file_not_found(self):
        """Test preamble extraction when file doesn't exist."""
        with pytest.raises(ValueError, match="Error reading preamble"):
            extract_preamble_from_file("/nonexistent/file.tsv")

    @patch("src.parsers.preamble_parser.open")
    def test_extract_preamble_from_file_encoding_error(self, mock_open):
        """Test preamble extraction with encoding error."""
        mock_open.side_effect = UnicodeDecodeError("utf-8", b"", 0, 1, "invalid")

        with pytest.raises(ValueError, match="Error reading preamble"):
            extract_preamble_from_file("test.tsv")
