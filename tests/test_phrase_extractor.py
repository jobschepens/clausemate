"""Tests for phrase_extractor.py."""

from unittest.mock import MagicMock

from src.data.models import CoreferencePhrase, SentenceContext, Token
from src.extractors.phrase_extractor import PhraseExtractor


class TestPhraseExtractor:
    """Test the PhraseExtractor class."""

    def setup_method(self):
        """Set up test fixtures."""
        self.extractor = PhraseExtractor()

    def test_initialization(self):
        """Test that the extractor initializes correctly."""
        assert isinstance(self.extractor, PhraseExtractor)

    def test_extract_basic(self):
        """Test basic phrase extraction."""
        # Create tokens with coreference information
        token1 = Token(
            idx=1,
            text="Karl",
            sentence_num=1,
            grammatical_role="SUBJ",
            thematic_role="AGENT",
            coreference_link="*->115-1",
            coreference_type="PersPron[115]",
        )
        token2 = Token(
            idx=2,
            text="sagte",
            sentence_num=1,
            grammatical_role="VERB",
            thematic_role="ACTION",
        )
        token3 = Token(
            idx=3,
            text="er",
            sentence_num=1,
            grammatical_role="SUBJ",
            thematic_role="AGENT",
            coreference_link="*->115-1",
            coreference_type="PersPron[115]",
        )

        context = SentenceContext(
            sentence_id="1",
            sentence_num=1,
            tokens=[token1, token2, token3],
            critical_pronouns=[],
            coreference_phrases=[],
            first_words="Karl_sagte",
        )

        result = self.extractor.extract(context)

        assert len(result.phrases) == 1
        phrase = result.phrases[0]
        assert isinstance(phrase, CoreferencePhrase)
        assert phrase.entity_id == "115-1"
        assert len(phrase.tokens) == 2
        assert phrase.tokens[0].text == "Karl"
        assert phrase.tokens[1].text == "er"
        assert result.features["phrase_count"] == 1
        assert result.features["multi_token_phrases"] == 1
        assert context.coreference_phrases == result.phrases

    def test_extract_no_phrases(self):
        """Test extraction when no phrases are present."""
        # Create tokens without coreference information
        token1 = Token(
            idx=1,
            text="Karl",
            sentence_num=1,
            grammatical_role="SUBJ",
            thematic_role="AGENT",
        )
        token2 = Token(
            idx=2,
            text="sagte",
            sentence_num=1,
            grammatical_role="VERB",
            thematic_role="ACTION",
        )

        context = SentenceContext(
            sentence_id="1",
            sentence_num=1,
            tokens=[token1, token2],
            critical_pronouns=[],
            coreference_phrases=[],
            first_words="Karl_sagte",
        )

        result = self.extractor.extract(context)

        assert len(result.phrases) == 0
        assert result.features["phrase_count"] == 0
        assert result.features["multi_token_phrases"] == 0

    def test_can_extract_with_coreference_links(self):
        """Test can_extract with tokens having coreference links."""
        token = Token(
            idx=1,
            text="Karl",
            sentence_num=1,
            grammatical_role="SUBJ",
            thematic_role="AGENT",
            coreference_link="*->115-1",
        )

        context = SentenceContext(
            sentence_id="1",
            sentence_num=1,
            tokens=[token],
            critical_pronouns=[],
            coreference_phrases=[],
            first_words="Karl",
        )

        assert self.extractor.can_extract(context) is True

    def test_can_extract_with_coreference_types(self):
        """Test can_extract with tokens having coreference types."""
        token = Token(
            idx=1,
            text="Karl",
            sentence_num=1,
            grammatical_role="SUBJ",
            thematic_role="AGENT",
            coreference_type="PersPron[115]",
        )

        context = SentenceContext(
            sentence_id="1",
            sentence_num=1,
            tokens=[token],
            critical_pronouns=[],
            coreference_phrases=[],
            first_words="Karl",
        )

        assert self.extractor.can_extract(context) is True

    def test_can_extract_with_inanimate_coreference(self):
        """Test can_extract with inanimate coreference information."""
        token = Token(
            idx=1,
            text="Buch",
            sentence_num=1,
            grammatical_role="OBJ",
            thematic_role="PATIENT",
            inanimate_coreference_link="*->200-1",
        )

        context = SentenceContext(
            sentence_id="1",
            sentence_num=1,
            tokens=[token],
            critical_pronouns=[],
            coreference_phrases=[],
            first_words="Buch",
        )

        assert self.extractor.can_extract(context) is True

    def test_can_extract_no_coreference(self):
        """Test can_extract with no coreference information."""
        token = Token(
            idx=1,
            text="Karl",
            sentence_num=1,
            grammatical_role="SUBJ",
            thematic_role="AGENT",
        )

        context = SentenceContext(
            sentence_id="1",
            sentence_num=1,
            tokens=[token],
            critical_pronouns=[],
            coreference_phrases=[],
            first_words="Karl",
        )

        assert self.extractor.can_extract(context) is False

    def test_extract_phrases_multiple_entities(self):
        """Test extracting phrases with multiple different entities."""
        token1 = Token(
            idx=1,
            text="Karl",
            sentence_num=1,
            grammatical_role="SUBJ",
            thematic_role="AGENT",
            coreference_link="*->115-1",
        )
        token2 = Token(
            idx=2,
            text="sagte",
            sentence_num=1,
            grammatical_role="VERB",
            thematic_role="ACTION",
        )
        token3 = Token(
            idx=3,
            text="Buch",
            sentence_num=1,
            grammatical_role="OBJ",
            thematic_role="PATIENT",
            inanimate_coreference_link="*->200-1",
        )
        token4 = Token(
            idx=4,
            text="er",
            sentence_num=1,
            grammatical_role="SUBJ",
            thematic_role="AGENT",
            coreference_link="*->115-1",
        )

        context = SentenceContext(
            sentence_id="1",
            sentence_num=1,
            tokens=[token1, token2, token3, token4],
            critical_pronouns=[],
            coreference_phrases=[],
            first_words="Karl_sagte",
        )

        phrases = self.extractor.extract_phrases(context)

        assert len(phrases) == 2
        # Check first phrase (entity 115)
        assert phrases[0].entity_id == "115-1"
        assert len(phrases[0].tokens) == 2
        assert phrases[0].phrase_text == "Karl er"
        # Check second phrase (entity 200)
        assert phrases[1].entity_id == "200-1"
        assert len(phrases[1].tokens) == 1
        assert phrases[1].phrase_text == "Buch"

    def test_extract_phrases_single_token_phrases(self):
        """Test extracting single-token phrases."""
        token1 = Token(
            idx=1,
            text="Karl",
            sentence_num=1,
            grammatical_role="SUBJ",
            thematic_role="AGENT",
            coreference_link="*->115-1",
        )
        token2 = Token(
            idx=2,
            text="Buch",
            sentence_num=1,
            grammatical_role="OBJ",
            thematic_role="PATIENT",
            inanimate_coreference_link="*->200-1",
        )

        context = SentenceContext(
            sentence_id="1",
            sentence_num=1,
            tokens=[token1, token2],
            critical_pronouns=[],
            coreference_phrases=[],
            first_words="Karl",
        )

        phrases = self.extractor.extract_phrases(context)

        assert len(phrases) == 2
        assert phrases[0].entity_id == "115-1"
        assert phrases[1].entity_id == "200-1"
        assert all(len(phrase.tokens) == 1 for phrase in phrases)
        assert all(phrase.is_multi_token is False for phrase in phrases)

    def test_group_tokens_by_entity(self):
        """Test grouping tokens by entity ID."""
        token1 = Token(
            idx=1,
            text="Karl",
            sentence_num=1,
            grammatical_role="SUBJ",
            thematic_role="AGENT",
            coreference_link="*->115-1",
        )
        token2 = Token(
            idx=2,
            text="er",
            sentence_num=1,
            grammatical_role="SUBJ",
            thematic_role="AGENT",
            coreference_link="*->115-1",
        )
        token3 = Token(
            idx=3,
            text="Buch",
            sentence_num=1,
            grammatical_role="OBJ",
            thematic_role="PATIENT",
            inanimate_coreference_link="*->200-1",
        )

        groups = self.extractor.group_tokens_by_entity([token1, token2, token3])

        assert len(groups) == 2
        assert "115-1" in groups
        assert "200-1" in groups
        assert len(groups["115-1"]) == 2
        assert len(groups["200-1"]) == 1
        assert groups["115-1"][0].text == "Karl"
        assert groups["115-1"][1].text == "er"

    def test_is_phrase_boundary_same_entity(self):
        """Test phrase boundary detection for same entity."""
        token1 = Token(
            idx=1,
            text="Karl",
            sentence_num=1,
            grammatical_role="SUBJ",
            thematic_role="AGENT",
            coreference_link="*->115-1",
        )
        token2 = Token(
            idx=2,
            text="er",
            sentence_num=1,
            grammatical_role="SUBJ",
            thematic_role="AGENT",
            coreference_link="*->115-1",
        )

        assert self.extractor.is_phrase_boundary(token1, token2) is False

    def test_is_phrase_boundary_different_entity(self):
        """Test phrase boundary detection for different entities."""
        token1 = Token(
            idx=1,
            text="Karl",
            sentence_num=1,
            grammatical_role="SUBJ",
            thematic_role="AGENT",
            coreference_link="*->115-1",
        )
        token2 = Token(
            idx=2,
            text="Buch",
            sentence_num=1,
            grammatical_role="OBJ",
            thematic_role="PATIENT",
            inanimate_coreference_link="*->200-1",
        )

        assert self.extractor.is_phrase_boundary(token1, token2) is True

    def test_is_phrase_boundary_no_coreference(self):
        """Test phrase boundary detection with no coreference."""
        token1 = Token(
            idx=1,
            text="Karl",
            sentence_num=1,
            grammatical_role="SUBJ",
            thematic_role="AGENT",
        )
        token2 = Token(
            idx=2,
            text="sagte",
            sentence_num=1,
            grammatical_role="VERB",
            thematic_role="ACTION",
        )

        assert self.extractor.is_phrase_boundary(token1, token2) is True

    def test_get_coreference_ids_from_link(self):
        """Test getting coreference IDs from coreference link."""
        token = Token(
            idx=1,
            text="Karl",
            sentence_num=1,
            grammatical_role="SUBJ",
            thematic_role="AGENT",
            coreference_link="*->115-1",
        )

        ids = self.extractor._get_coreference_ids(token)

        assert "115-1" in ids

    def test_get_coreference_ids_from_type(self):
        """Test getting coreference IDs from coreference type."""
        token = Token(
            idx=1,
            text="Karl",
            sentence_num=1,
            grammatical_role="SUBJ",
            thematic_role="AGENT",
            coreference_type="PersPron[115]",
        )

        ids = self.extractor._get_coreference_ids(token)

        assert "115" in ids

    def test_get_coreference_ids_inanimate(self):
        """Test getting coreference IDs from inanimate sources."""
        token = Token(
            idx=1,
            text="Buch",
            sentence_num=1,
            grammatical_role="OBJ",
            thematic_role="PATIENT",
            inanimate_coreference_link="*->200-1",
            inanimate_coreference_type="Inanim[200]",
        )

        ids = self.extractor._get_coreference_ids(token)

        assert "200-1" in ids
        # Note: The extractor prioritizes full IDs from links over base IDs from types
        # So we only get "200-1" from the link, not "200" from the type

    def test_get_coreference_ids_no_coreference(self):
        """Test getting coreference IDs with no coreference information."""
        token = Token(
            idx=1,
            text="Karl",
            sentence_num=1,
            grammatical_role="SUBJ",
            thematic_role="AGENT",
        )

        ids = self.extractor._get_coreference_ids(token)

        assert ids == []

    def test_build_phrase_text(self):
        """Test building phrase text from tokens."""
        token1 = Token(
            idx=1,
            text="Karl",
            sentence_num=1,
            grammatical_role="SUBJ",
            thematic_role="AGENT",
        )
        token2 = Token(
            idx=3,
            text="er",
            sentence_num=1,
            grammatical_role="SUBJ",
            thematic_role="AGENT",
        )
        token3 = Token(
            idx=2,
            text="und",
            sentence_num=1,
            grammatical_role="CONJ",
            thematic_role="CONNECTOR",
        )

        text = self.extractor._build_phrase_text([token1, token2, token3])

        # Should be sorted by position: token1 (idx=1), token3 (idx=2), token2 (idx=3)
        assert text == "Karl und er"

    def test_build_phrase_text_empty(self):
        """Test building phrase text from empty token list."""
        text = self.extractor._build_phrase_text([])

        assert text == ""

    def test_validate_phrase_valid(self):
        """Test validating a valid phrase."""
        token1 = Token(
            idx=1,
            text="Karl",
            sentence_num=1,
            grammatical_role="SUBJ",
            thematic_role="AGENT",
            coreference_link="*->115-1",
        )
        token2 = Token(
            idx=2,
            text="er",
            sentence_num=1,
            grammatical_role="SUBJ",
            thematic_role="AGENT",
            coreference_link="*->115-1",
        )

        phrase = CoreferencePhrase(
            entity_id="115-1",
            tokens=[token1, token2],
            phrase_text="Karl er",
            start_position=1,
            end_position=2,
            sentence_id="1",
        )

        assert self.extractor.validate_phrase(phrase) is True

    def test_validate_phrase_empty_tokens(self):
        """Test validating a phrase with no tokens."""
        # Create a mock phrase to bypass constructor validation

        phrase = MagicMock()
        phrase.entity_id = "115"
        phrase.tokens = []
        phrase.phrase_text = ""

        assert self.extractor.validate_phrase(phrase) is False

    def test_validate_phrase_no_entity_id(self):
        """Test validating a phrase with no entity ID."""
        # Create a mock phrase to bypass constructor validation

        token = Token(
            idx=1,
            text="Karl",
            sentence_num=1,
            grammatical_role="SUBJ",
            thematic_role="AGENT",
        )

        phrase = MagicMock()
        phrase.entity_id = ""
        phrase.tokens = [token]
        phrase.phrase_text = "Karl"

        assert self.extractor.validate_phrase(phrase) is False

    def test_validate_phrase_mismatched_entity(self):
        """Test validating a phrase with mismatched entity IDs."""
        token1 = Token(
            idx=1,
            text="Karl",
            sentence_num=1,
            grammatical_role="SUBJ",
            thematic_role="AGENT",
            coreference_link="*->115-1",
        )
        token2 = Token(
            idx=2,
            text="er",
            sentence_num=1,
            grammatical_role="SUBJ",
            thematic_role="AGENT",
            coreference_link="*->200-1",  # Different entity ID
        )

        phrase = CoreferencePhrase(
            entity_id="115-1",
            tokens=[token1, token2],
            phrase_text="Karl er",
            start_position=1,
            end_position=2,
            sentence_id="1",
        )

        assert self.extractor.validate_phrase(phrase) is False
