"""Unit tests for data models with comprehensive validation."""

import pytest

from src.data.models import (
    AnimacyType,
    AntecedentInfo,
    ClauseMateRelationship,
    Phrase,
    SentenceContext,
    Token,
)
from tests.fixtures.mock_data.mock_objects import (
    MockDataFactory,
    mock_antecedent_info,
    mock_phrase,
    mock_relationship,
    mock_sentence_context,
    mock_token,
)


class TestToken:
    """Unit tests for Token data model."""

    def test_token_creation_valid(self):
        """Test creating a valid token."""
        token = mock_token(idx=1, text="He", sentence_num=1)

        assert token.idx == 1
        assert token.text == "He"
        assert token.sentence_num == 1
        assert token.grammatical_role == "nsubj"
        assert token.thematic_role == "agent"

    def test_token_validation_invalid_idx(self):
        """Test token validation with invalid index."""
        with pytest.raises(ValueError, match="Token index must be positive"):
            Token(
                idx=0,
                text="test",
                sentence_num=1,
                grammatical_role="test",
                thematic_role="test",
            )

    def test_token_validation_negative_sentence_num(self):
        """Test token validation with negative sentence number."""
        with pytest.raises(ValueError, match="Sentence number cannot be negative"):
            Token(
                idx=1,
                text="test",
                sentence_num=-1,
                grammatical_role="test",
                thematic_role="test",
            )

    def test_token_validation_empty_text(self):
        """Test token validation with empty text."""
        with pytest.raises(ValueError, match="Token text cannot be empty"):
            Token(
                idx=1,
                text="",
                sentence_num=1,
                grammatical_role="test",
                thematic_role="test",
            )

    def test_token_columns_initialization(self):
        """Test token columns are properly initialized."""
        token = mock_token()
        assert token.columns == []


class TestPhrase:
    """Unit tests for Phrase data model."""

    def test_phrase_creation_valid(self):
        """Test creating a valid phrase."""
        phrase = mock_phrase(
            text="the book", coreference_id="(2)", start_idx=3, end_idx=4
        )

        assert phrase.text == "the book"
        assert phrase.coreference_id == "(2)"
        assert phrase.start_idx == 3
        assert phrase.end_idx == 4
        assert phrase.length == 2

    def test_phrase_validation_invalid_indices(self):
        """Test phrase validation with invalid indices."""
        with pytest.raises(
            ValueError, match="Start index cannot be greater than end index"
        ):
            Phrase(
                text="test",
                coreference_id="(1)",
                start_idx=5,
                end_idx=3,
                grammatical_role="test",
                thematic_role="test",
                coreference_type="test",
                animacy=AnimacyType.ANIMATE,
                givenness="test",
            )

    def test_phrase_validation_zero_indices(self):
        """Test phrase validation with zero indices."""
        with pytest.raises(ValueError, match="Phrase indices must be positive"):
            Phrase(
                text="test",
                coreference_id="(1)",
                start_idx=0,
                end_idx=1,
                grammatical_role="test",
                thematic_role="test",
                coreference_type="test",
                animacy=AnimacyType.ANIMATE,
                givenness="test",
            )

    def test_phrase_validation_empty_text(self):
        """Test phrase validation with empty text."""
        with pytest.raises(ValueError, match="Phrase text cannot be empty"):
            Phrase(
                text="",
                coreference_id="(1)",
                start_idx=1,
                end_idx=2,
                grammatical_role="test",
                thematic_role="test",
                coreference_type="test",
                animacy=AnimacyType.ANIMATE,
                givenness="test",
            )

    def test_phrase_validation_empty_coref_id(self):
        """Test phrase validation with empty coreference ID."""
        with pytest.raises(ValueError, match="Coreference ID cannot be empty"):
            Phrase(
                text="test",
                coreference_id="",
                start_idx=1,
                end_idx=2,
                grammatical_role="test",
                thematic_role="test",
                coreference_type="test",
                animacy=AnimacyType.ANIMATE,
                givenness="test",
            )


class TestAntecedentInfo:
    """Unit tests for AntecedentInfo data model."""

    def test_antecedent_info_creation_valid(self):
        """Test creating valid antecedent info."""
        info = mock_antecedent_info(
            most_recent_text="book", first_text="book", choice_count=1
        )

        assert info.most_recent_text == "book"
        assert info.first_text == "book"
        assert info.choice_count == 1

    def test_antecedent_info_validation_negative_choice_count(self):
        """Test antecedent info validation with negative choice count."""
        with pytest.raises(ValueError, match="Choice count cannot be negative"):
            AntecedentInfo(
                most_recent_text="test",
                most_recent_distance="0",
                first_text="test",
                first_distance="0",
                sentence_id="1",
                choice_count=-1,
            )


class TestSentenceContext:
    """Unit tests for SentenceContext data model."""

    def test_sentence_context_creation_valid(self):
        """Test creating valid sentence context."""
        context = mock_sentence_context(sentence_id="1", sentence_num=1)

        assert context.sentence_id == "1"
        assert context.sentence_num == 1
        assert len(context.tokens) == 4
        assert context.has_critical_pronouns
        assert not context.has_coreference_phrases  # Empty by default

    def test_sentence_context_validation_invalid_sentence_num(self):
        """Test sentence context validation with invalid sentence number."""
        with pytest.raises(ValueError, match="Sentence number must be positive"):
            SentenceContext(
                sentence_id="1",
                sentence_num=0,
                tokens=[],
                critical_pronouns=[],
                coreference_phrases=[],
            )

    def test_sentence_context_validation_empty_sentence_id(self):
        """Test sentence context validation with empty sentence ID."""
        with pytest.raises(ValueError, match="Sentence ID cannot be empty"):
            SentenceContext(
                sentence_id="",
                sentence_num=1,
                tokens=[mock_token()],
                critical_pronouns=[],
                coreference_phrases=[],
            )

    def test_sentence_context_validation_no_tokens(self):
        """Test sentence context validation with no tokens."""
        with pytest.raises(ValueError, match="Sentence must have at least one token"):
            SentenceContext(
                sentence_id="1",
                sentence_num=1,
                tokens=[],
                critical_pronouns=[],
                coreference_phrases=[],
            )


class TestClauseMateRelationship:
    """Unit tests for ClauseMateRelationship data model."""

    def test_relationship_creation_valid(self):
        """Test creating valid clause mate relationship."""
        relationship = mock_relationship(
            sentence_id="1", sentence_num=1, num_clause_mates=1
        )

        assert relationship.sentence_id == "1"
        assert relationship.sentence_num == 1
        assert relationship.num_clause_mates == 1
        assert relationship.pronoun.text == "He"
        assert relationship.clause_mate.text == "the book"

    def test_relationship_validation_invalid_sentence_num(self):
        """Test relationship validation with invalid sentence number."""
        with pytest.raises(ValueError, match="Sentence number must be positive"):
            ClauseMateRelationship(
                sentence_id="1",
                sentence_num=0,
                pronoun=mock_token(),
                clause_mate=mock_phrase(),
                num_clause_mates=1,
                antecedent_info=mock_antecedent_info(),
            )

    def test_relationship_validation_invalid_clause_mates_count(self):
        """Test relationship validation with invalid clause mates count."""
        with pytest.raises(ValueError, match="Number of clause mates must be positive"):
            ClauseMateRelationship(
                sentence_id="1",
                sentence_num=1,
                pronoun=mock_token(),
                clause_mate=mock_phrase(),
                num_clause_mates=0,
                antecedent_info=mock_antecedent_info(),
            )

    def test_relationship_validation_empty_sentence_id(self):
        """Test relationship validation with empty sentence ID."""
        with pytest.raises(ValueError, match="Sentence ID cannot be empty"):
            ClauseMateRelationship(
                sentence_id="",
                sentence_num=1,
                pronoun=mock_token(),
                clause_mate=mock_phrase(),
                num_clause_mates=1,
                antecedent_info=mock_antecedent_info(),
            )

    def test_relationship_to_dict_conversion(self):
        """Test relationship conversion to dictionary."""
        relationship = mock_relationship()
        data_dict = relationship.to_dict()

        # Check key fields are present
        assert "sentence_num" in data_dict
        assert "pronoun_text" in data_dict
        assert "clause_mate_text" in data_dict
        assert "pronoun_grammatical_role" in data_dict
        assert "clause_mate_animacy" in data_dict

        # Check values are correct
        assert data_dict["sentence_num"] == 1
        assert data_dict["pronoun_text"] == "He"
        assert data_dict["clause_mate_text"] == "the book"


@pytest.mark.unit
class TestMockDataFactory:
    """Unit tests for MockDataFactory functionality."""

    def test_factory_creates_consistent_objects(self):
        """Test that factory creates consistent mock objects."""
        token1 = MockDataFactory.create_mock_token()
        token2 = MockDataFactory.create_mock_token()

        # Should have same default values
        assert token1.text == token2.text
        assert token1.grammatical_role == token2.grammatical_role
        assert token1.thematic_role == token2.thematic_role

    def test_factory_accepts_custom_parameters(self):
        """Test that factory accepts custom parameters."""
        token = MockDataFactory.create_mock_token(
            text="Custom", grammatical_role="custom_role"
        )

        assert token.text == "Custom"
        assert token.grammatical_role == "custom_role"

    def test_factory_creates_valid_relationships(self):
        """Test that factory creates valid relationships."""
        relationship = MockDataFactory.create_mock_relationship()

        # Should not raise validation errors
        assert relationship.sentence_num > 0
        assert relationship.num_clause_mates > 0
        assert relationship.sentence_id != ""
        assert relationship.pronoun.text != ""
        assert relationship.clause_mate.text != ""
