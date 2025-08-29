"""Tests for pronoun_extractor.py."""

from unittest.mock import MagicMock

from src.data.models import SentenceContext, Token
from src.extractors.pronoun_extractor import PronounExtractor


class TestPronounExtractor:
    """Test the PronounExtractor class."""

    def setup_method(self):
        """Set up test fixtures."""
        self.extractor = PronounExtractor()

    def test_initialization(self):
        """Test that the extractor initializes correctly."""
        assert hasattr(self.extractor, "critical_pronouns")
        assert len(self.extractor.critical_pronouns) > 0

    def test_extract_basic(self):
        """Test basic pronoun extraction."""
        # Create mock tokens
        token1 = Token(
            idx=1,
            text="Karl",
            sentence_num=1,
            grammatical_role="SUBJ",
            thematic_role="AGENT",
        )
        token2 = Token(
            idx=2,
            text="er",
            sentence_num=1,
            grammatical_role="SUBJ",
            thematic_role="AGENT",
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

        assert len(result.pronouns) == 1
        assert result.pronouns[0].text == "er"
        assert result.features["critical_pronoun_count"] == 1
        assert context.critical_pronouns == result.pronouns

    def test_extract_no_pronouns(self):
        """Test extraction when no pronouns are present."""
        # Create mock tokens without pronouns
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

        assert len(result.pronouns) == 0
        assert result.features["critical_pronoun_count"] == 0

    def test_can_extract_with_tokens(self):
        """Test can_extract with tokens present."""
        context = SentenceContext(
            sentence_id="1",
            sentence_num=1,
            tokens=[MagicMock()],
            critical_pronouns=[],
            coreference_phrases=[],
            first_words="Karl_sagte",
        )

        assert self.extractor.can_extract(context) is True

    def test_can_extract_empty_tokens(self):
        """Test can_extract with no tokens."""
        # Create a minimal token for SentenceContext validation
        dummy_token = Token(
            idx=1,
            text="dummy",
            sentence_num=1,
            grammatical_role="DUMMY",
            thematic_role="DUMMY",
        )

        context = SentenceContext(
            sentence_id="1",
            sentence_num=1,
            tokens=[dummy_token],  # Provide a token to satisfy validation
            critical_pronouns=[],
            coreference_phrases=[],
            first_words="Karl_sagte",
        )

        # Mock the tokens to be empty for the actual test
        context.tokens = []

        assert self.extractor.can_extract(context) is False

    def test_extract_pronouns_mixed_tokens(self):
        """Test pronoun extraction from mixed tokens."""
        token1 = Token(
            idx=1,
            text="Karl",
            sentence_num=1,
            grammatical_role="SUBJ",
            thematic_role="AGENT",
        )
        token2 = Token(
            idx=2,
            text="er",
            sentence_num=1,
            grammatical_role="SUBJ",
            thematic_role="AGENT",
        )
        token3 = Token(
            idx=3,
            text="sie",
            sentence_num=1,
            grammatical_role="OBJ",
            thematic_role="PATIENT",
        )
        token4 = Token(
            idx=4,
            text="sagte",
            sentence_num=1,
            grammatical_role="VERB",
            thematic_role="ACTION",
        )

        context = SentenceContext(
            sentence_id="1",
            sentence_num=1,
            tokens=[token1, token2, token3, token4],
            critical_pronouns=[],
            coreference_phrases=[],
            first_words="Karl_sagte",
        )

        pronouns = self.extractor.extract_pronouns(context)

        assert len(pronouns) == 2
        assert pronouns[0].text == "er"
        assert pronouns[1].text == "sie"
        assert pronouns[0].is_critical_pronoun is True
        assert pronouns[1].is_critical_pronoun is True

    def test_classify_pronoun_personal_masculine(self):
        """Test pronoun classification for personal masculine pronoun."""
        pronoun = Token(
            idx=2,
            text="er",
            sentence_num=1,
            grammatical_role="SUBJ",
            thematic_role="AGENT",
        )

        context = SentenceContext(
            sentence_id="1",
            sentence_num=1,
            tokens=[pronoun],
            critical_pronouns=[],
            coreference_phrases=[],
            first_words="Karl_sagte",
        )

        classification = self.extractor.classify_pronoun(pronoun, context)

        assert classification["text"] == "er"
        assert classification["type"] == "personal"
        assert classification["person"] == "3rd"
        assert classification["gender"] == "masculine"
        assert classification["number"] == "singular"

    def test_classify_pronoun_personal_feminine(self):
        """Test pronoun classification for personal feminine pronoun."""
        pronoun = Token(
            idx=2,
            text="sie",
            sentence_num=1,
            grammatical_role="SUBJ",
            thematic_role="AGENT",
        )

        context = SentenceContext(
            sentence_id="1",
            sentence_num=1,
            tokens=[pronoun],
            critical_pronouns=[],
            coreference_phrases=[],
            first_words="Karl_sagte",
        )

        classification = self.extractor.classify_pronoun(pronoun, context)

        assert classification["text"] == "sie"
        assert classification["type"] == "personal"
        assert classification["person"] == "3rd"
        assert classification["gender"] == "feminine_or_plural"
        assert classification["number"] == "singular_or_plural"

    def test_classify_pronoun_personal_neuter(self):
        """Test pronoun classification for personal neuter pronoun."""
        pronoun = Token(
            idx=2,
            text="es",
            sentence_num=1,
            grammatical_role="SUBJ",
            thematic_role="AGENT",
        )

        context = SentenceContext(
            sentence_id="1",
            sentence_num=1,
            tokens=[pronoun],
            critical_pronouns=[],
            coreference_phrases=[],
            first_words="Karl_sagte",
        )

        classification = self.extractor.classify_pronoun(pronoun, context)

        assert classification["text"] == "es"
        assert classification["type"] == "personal"
        assert classification["person"] == "3rd"
        assert classification["gender"] == "neuter"
        assert classification["number"] == "singular"

    def test_classify_pronoun_personal_plural(self):
        """Test pronoun classification for personal plural pronoun."""
        pronoun = Token(
            idx=2,
            text="ihnen",
            sentence_num=1,
            grammatical_role="OBJ",
            thematic_role="PATIENT",
        )

        context = SentenceContext(
            sentence_id="1",
            sentence_num=1,
            tokens=[pronoun],
            critical_pronouns=[],
            coreference_phrases=[],
            first_words="Karl_sagte",
        )

        classification = self.extractor.classify_pronoun(pronoun, context)

        assert classification["text"] == "ihnen"
        assert classification["type"] == "personal"
        assert classification["person"] == "3rd"
        assert classification["gender"] == "plural"
        assert classification["number"] == "plural"

    def test_classify_pronoun_d_pronoun(self):
        """Test pronoun classification for D-pronoun."""
        pronoun = Token(
            idx=2,
            text="der",
            sentence_num=1,
            grammatical_role="SUBJ",
            thematic_role="AGENT",
        )

        context = SentenceContext(
            sentence_id="1",
            sentence_num=1,
            tokens=[pronoun],
            critical_pronouns=[],
            coreference_phrases=[],
            first_words="Karl_sagte",
        )

        classification = self.extractor.classify_pronoun(pronoun, context)

        assert classification["text"] == "der"
        assert classification["type"] == "d_pronoun"
        assert classification["person"] == "3rd"

    def test_classify_pronoun_demonstrative(self):
        """Test pronoun classification for demonstrative pronoun."""
        pronoun = Token(
            idx=2,
            text="dieser",
            sentence_num=1,
            grammatical_role="SUBJ",
            thematic_role="AGENT",
        )

        context = SentenceContext(
            sentence_id="1",
            sentence_num=1,
            tokens=[pronoun],
            critical_pronouns=[],
            coreference_phrases=[],
            first_words="Karl_sagte",
        )

        classification = self.extractor.classify_pronoun(pronoun, context)

        assert classification["text"] == "dieser"
        assert classification["type"] == "demonstrative"
        assert classification["person"] == "3rd"

    def test_classify_pronoun_with_coreference_animate(self):
        """Test pronoun classification with animate coreference."""
        pronoun = Token(
            idx=2,
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
            tokens=[pronoun],
            critical_pronouns=[],
            coreference_phrases=[],
            first_words="Karl_sagte",
        )

        classification = self.extractor.classify_pronoun(pronoun, context)

        assert classification["animacy"] == "animate"

    def test_classify_pronoun_with_inanimate_coreference(self):
        """Test pronoun classification with inanimate coreference."""
        pronoun = Token(
            idx=2,
            text="es",
            sentence_num=1,
            grammatical_role="SUBJ",
            thematic_role="AGENT",
            inanimate_coreference_link="*->200-1",
            inanimate_coreference_type="Inanim[200]",
        )

        context = SentenceContext(
            sentence_id="1",
            sentence_num=1,
            tokens=[pronoun],
            critical_pronouns=[],
            coreference_phrases=[],
            first_words="Karl_sagte",
        )

        classification = self.extractor.classify_pronoun(pronoun, context)

        assert classification["animacy"] == "inanimate"

    def test_classify_pronoun_unknown(self):
        """Test pronoun classification for unknown pronoun."""
        pronoun = Token(
            idx=2,
            text="unknown",
            sentence_num=1,
            grammatical_role="SUBJ",
            thematic_role="AGENT",
        )

        context = SentenceContext(
            sentence_id="1",
            sentence_num=1,
            tokens=[pronoun],
            critical_pronouns=[],
            coreference_phrases=[],
            first_words="Karl_sagte",
        )

        classification = self.extractor.classify_pronoun(pronoun, context)

        assert classification["text"] == "unknown"
        assert classification["type"] == "unknown"
        assert classification["animacy"] == "unknown"
        assert classification["person"] == "unknown"
        assert classification["gender"] == "unknown"
        assert classification["number"] == "unknown"

    def test_is_pronoun_critical_pronoun(self):
        """Test is_pronoun with critical pronoun."""
        token = Token(
            idx=2,
            text="er",
            sentence_num=1,
            grammatical_role="SUBJ",
            thematic_role="AGENT",
        )

        assert self.extractor.is_pronoun(token) is True

    def test_is_pronoun_non_pronoun(self):
        """Test is_pronoun with non-pronoun."""
        token = Token(
            idx=2,
            text="sagte",
            sentence_num=1,
            grammatical_role="VERB",
            thematic_role="ACTION",
        )

        assert self.extractor.is_pronoun(token) is False

    def test_is_pronoun_with_coreference_annotation(self):
        """Test is_pronoun with pronoun coreference annotation."""
        token = Token(
            idx=2,
            text="unknown_word",
            sentence_num=1,
            grammatical_role="SUBJ",
            thematic_role="AGENT",
            coreference_type="PersPron[115]",
        )

        assert self.extractor.is_pronoun(token) is True

    def test_is_pronoun_with_inanimate_coreference_annotation(self):
        """Test is_pronoun with inanimate pronoun coreference annotation."""
        token = Token(
            idx=2,
            text="unknown_word",
            sentence_num=1,
            grammatical_role="SUBJ",
            thematic_role="AGENT",
            inanimate_coreference_type="D-Pron[200]",
        )

        assert self.extractor.is_pronoun(token) is True

    def test_is_critical_pronoun(self):
        """Test _is_critical_pronoun method."""
        token = Token(
            idx=2,
            text="er",
            sentence_num=1,
            grammatical_role="SUBJ",
            thematic_role="AGENT",
        )

        assert self.extractor._is_critical_pronoun(token) is True

    def test_has_pronoun_coreference_annotation_personal(self):
        """Test _has_pronoun_coreference_annotation with personal pronoun."""
        token = Token(
            idx=2,
            text="word",
            sentence_num=1,
            grammatical_role="SUBJ",
            thematic_role="AGENT",
            coreference_type="PersPron[115]",
        )

        assert self.extractor._has_pronoun_coreference_annotation(token) is True

    def test_has_pronoun_coreference_annotation_d_pronoun(self):
        """Test _has_pronoun_coreference_annotation with D-pronoun."""
        token = Token(
            idx=2,
            text="word",
            sentence_num=1,
            grammatical_role="SUBJ",
            thematic_role="AGENT",
            coreference_type="D-Pron[115]",
        )

        assert self.extractor._has_pronoun_coreference_annotation(token) is True

    def test_has_pronoun_coreference_annotation_demonstrative(self):
        """Test _has_pronoun_coreference_annotation with demonstrative pronoun."""
        token = Token(
            idx=2,
            text="word",
            sentence_num=1,
            grammatical_role="SUBJ",
            thematic_role="AGENT",
            coreference_type="DemPron[115]",
        )

        assert self.extractor._has_pronoun_coreference_annotation(token) is True

    def test_has_pronoun_coreference_annotation_inanimate(self):
        """Test _has_pronoun_coreference_annotation with inanimate pronoun."""
        token = Token(
            idx=2,
            text="word",
            sentence_num=1,
            grammatical_role="SUBJ",
            thematic_role="AGENT",
            inanimate_coreference_type="PersPron[200]",
        )

        assert self.extractor._has_pronoun_coreference_annotation(token) is True

    def test_has_pronoun_coreference_annotation_no_pronoun(self):
        """Test _has_pronoun_coreference_annotation with non-pronoun."""
        token = Token(
            idx=2,
            text="word",
            sentence_num=1,
            grammatical_role="SUBJ",
            thematic_role="AGENT",
            coreference_type="Noun[115]",
        )

        assert self.extractor._has_pronoun_coreference_annotation(token) is False

    def test_has_pronoun_coreference_annotation_no_coreference(self):
        """Test _has_pronoun_coreference_annotation with no coreference."""
        token = Token(
            idx=2,
            text="word",
            sentence_num=1,
            grammatical_role="SUBJ",
            thematic_role="AGENT",
        )

        assert self.extractor._has_pronoun_coreference_annotation(token) is False
