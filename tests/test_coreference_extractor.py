"""Tests for coreference_extractor.py."""

from src.data.models import (
    AnimacyType,
    CoreferenceChain,
    SentenceContext,
    Token,
)
from src.extractors.coreference_extractor import CoreferenceExtractor


class TestCoreferenceExtractor:
    """Test the CoreferenceExtractor class."""

    def setup_method(self):
        """Set up test fixtures."""
        self.extractor = CoreferenceExtractor()

    def test_initialization(self):
        """Test that the extractor initializes correctly."""
        assert isinstance(self.extractor, CoreferenceExtractor)
        assert hasattr(self.extractor, "coreference_pattern")
        assert hasattr(self.extractor, "critical_pronouns")

    def test_extract_basic(self):
        """Test basic coreference extraction."""
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

        # The extractor creates chains for all unique IDs found
        # "*->115-1" contains both "115" and "1", so we get 2 chains
        assert len(result.coreference_chains) == 2
        chain_ids = {chain.chain_id for chain in result.coreference_chains}
        assert "115" in chain_ids
        assert "1" in chain_ids

        # Both chains should have the same mentions
        for chain in result.coreference_chains:
            assert len(chain.mentions) == 2
            assert chain.animacy == AnimacyType.ANIMATE

        assert "115" in result.features["coreference_ids"]
        assert "1" in result.features["coreference_ids"]

    def test_extract_no_coreference(self):
        """Test extraction when no coreference information is present."""
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

        assert len(result.coreference_chains) == 0
        assert result.features["coreference_ids"] == set()

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

    def test_extract_coreference_chains_multiple_contexts(self):
        """Test extracting coreference chains from multiple contexts."""
        # Create first context
        token1 = Token(
            idx=1,
            text="Karl",
            sentence_num=1,
            grammatical_role="SUBJ",
            thematic_role="AGENT",
            coreference_link="*->115-1",
        )
        context1 = SentenceContext(
            sentence_id="1",
            sentence_num=1,
            tokens=[token1],
            critical_pronouns=[],
            coreference_phrases=[],
            first_words="Karl",
        )

        # Create second context with same coreference ID
        token2 = Token(
            idx=1,
            text="er",
            sentence_num=2,
            grammatical_role="SUBJ",
            thematic_role="AGENT",
            coreference_link="*->115-2",
        )
        context2 = SentenceContext(
            sentence_id="2",
            sentence_num=2,
            tokens=[token2],
            critical_pronouns=[],
            coreference_phrases=[],
            first_words="er",
        )

        chains = self.extractor.extract_coreference_chains([context1, context2])

        # We expect 3 chains: "115" (shared), "1" (from first context), "2" (from second context)
        assert len(chains) == 3
        chain_ids = {chain.chain_id for chain in chains}
        assert "115" in chain_ids
        assert "1" in chain_ids
        assert "2" in chain_ids

        # The "115" chain should have both mentions
        chain_115 = next(chain for chain in chains if chain.chain_id == "115")
        assert len(chain_115.mentions) == 2
        assert chain_115.animacy == AnimacyType.ANIMATE

    def test_find_mentions(self):
        """Test finding mentions in a sentence context."""
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
            text="er",
            sentence_num=1,
            grammatical_role="SUBJ",
            thematic_role="AGENT",
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

        mentions = self.extractor.find_mentions(context)

        assert len(mentions) == 2
        assert mentions[0].text == "Karl"
        assert mentions[1].text == "er"

    def test_link_mentions_to_existing_chains(self):
        """Test linking new mentions to existing coreference chains."""
        # Create existing chain
        existing_token = Token(
            idx=1,
            text="Karl",
            sentence_num=1,
            grammatical_role="SUBJ",
            thematic_role="AGENT",
            coreference_link="*->115-1",
        )
        existing_chain = CoreferenceChain(
            chain_id="115",
            mentions=[existing_token],
            animacy=AnimacyType.ANIMATE,
        )

        # Create new mention with same coreference ID
        new_token = Token(
            idx=2,
            text="er",
            sentence_num=2,
            grammatical_role="SUBJ",
            thematic_role="AGENT",
            coreference_link="*->115-2",
        )

        updated_chains = self.extractor.link_mentions([new_token], [existing_chain])

        # We expect 2 chains: "115" (existing + new), "2" (from new token)
        assert len(updated_chains) == 2
        chain_ids = {chain.chain_id for chain in updated_chains}
        assert "115" in chain_ids
        assert "2" in chain_ids

        # Check the "115" chain has both mentions
        chain_115 = next(chain for chain in updated_chains if chain.chain_id == "115")
        assert len(chain_115.mentions) == 2
        mention_texts = {mention.text for mention in chain_115.mentions}
        assert "Karl" in mention_texts
        assert "er" in mention_texts

    def test_link_mentions_creates_new_chain(self):
        """Test linking mentions that create new chains."""
        # Create existing chain
        existing_token = Token(
            idx=1,
            text="Karl",
            sentence_num=1,
            grammatical_role="SUBJ",
            thematic_role="AGENT",
            coreference_link="*->115-1",
        )
        existing_chain = CoreferenceChain(
            chain_id="115",
            mentions=[existing_token],
            animacy=AnimacyType.ANIMATE,
        )

        # Create new mention with different coreference ID
        new_token = Token(
            idx=2,
            text="Buch",
            sentence_num=2,
            grammatical_role="OBJ",
            thematic_role="PATIENT",
            inanimate_coreference_link="*->200-1",
        )

        updated_chains = self.extractor.link_mentions([new_token], [existing_chain])

        # We expect 3 chains: "115" (existing), "1" (from existing token), "200" (new), "1" (from new token)
        assert len(updated_chains) == 3
        chain_ids = {chain.chain_id for chain in updated_chains}
        assert "115" in chain_ids
        assert "200" in chain_ids
        assert "1" in chain_ids

        # Check existing "115" chain
        chain_115 = next(chain for chain in updated_chains if chain.chain_id == "115")
        assert len(chain_115.mentions) == 1
        assert chain_115.mentions[0].text == "Karl"

        # Check new "200" chain
        chain_200 = next(chain for chain in updated_chains if chain.chain_id == "200")
        assert len(chain_200.mentions) == 1
        assert chain_200.mentions[0].text == "Buch"
        assert chain_200.animacy == AnimacyType.INANIMATE

    def test_extract_all_ids_from_token_animate(self):
        """Test extracting all IDs from token with animate coreference."""
        token = Token(
            idx=1,
            text="Karl",
            sentence_num=1,
            grammatical_role="SUBJ",
            thematic_role="AGENT",
            coreference_link="*->115-1",
            coreference_type="PersPron[115]",
        )

        ids = self.extractor.extract_all_ids_from_token(token)

        assert "115" in ids
        assert "1" in ids  # Also extracts the occurrence number
        assert len(ids) == 2

    def test_extract_all_ids_from_token_inanimate(self):
        """Test extracting all IDs from token with inanimate coreference."""
        token = Token(
            idx=1,
            text="Buch",
            sentence_num=1,
            grammatical_role="OBJ",
            thematic_role="PATIENT",
            inanimate_coreference_link="*->200-1",
            inanimate_coreference_type="Inanim[200]",
        )

        ids = self.extractor.extract_all_ids_from_token(token)

        assert "200" in ids
        assert "1" in ids  # Also extracts the occurrence number
        assert len(ids) == 2

    def test_extract_all_ids_from_token_mixed(self):
        """Test extracting all IDs from token with mixed coreference types."""
        token = Token(
            idx=1,
            text="Karl",
            sentence_num=1,
            grammatical_role="SUBJ",
            thematic_role="AGENT",
            coreference_link="*->115-1",
            inanimate_coreference_link="*->200-1",
        )

        ids = self.extractor.extract_all_ids_from_token(token)

        assert "115" in ids
        assert "200" in ids
        assert "1" in ids  # From both links
        assert len(ids) == 3

    def test_extract_all_ids_from_token_no_coreference(self):
        """Test extracting IDs from token with no coreference information."""
        token = Token(
            idx=1,
            text="Karl",
            sentence_num=1,
            grammatical_role="SUBJ",
            thematic_role="AGENT",
        )

        ids = self.extractor.extract_all_ids_from_token(token)

        assert ids == set()

    def test_extract_ids_from_string(self):
        """Test extracting IDs from string patterns."""
        # Test various patterns
        assert self.extractor._extract_ids_from_string("*->115-1") == {"115", "1"}
        assert self.extractor._extract_ids_from_string("PersPron[200]") == {"200"}
        assert self.extractor._extract_ids_from_string("115-1->200-2") == {
            "115",
            "200",
            "1",
            "2",
        }
        assert self.extractor._extract_ids_from_string("_") == set()
        assert self.extractor._extract_ids_from_string("") == set()
        assert self.extractor._extract_ids_from_string("no_numbers") == set()

    def test_has_coreference_info(self):
        """Test checking if token has coreference information."""
        # Token with animate coreference
        token1 = Token(
            idx=1,
            text="Karl",
            sentence_num=1,
            grammatical_role="SUBJ",
            thematic_role="AGENT",
            coreference_link="*->115-1",
        )
        assert self.extractor._has_coreference_info(token1) is True

        # Token with inanimate coreference
        token2 = Token(
            idx=2,
            text="Buch",
            sentence_num=1,
            grammatical_role="OBJ",
            thematic_role="PATIENT",
            inanimate_coreference_type="Inanim[200]",
        )
        assert self.extractor._has_coreference_info(token2) is True

        # Token with underscore (no coreference)
        token3 = Token(
            idx=3,
            text="sagte",
            sentence_num=1,
            grammatical_role="VERB",
            thematic_role="ACTION",
            coreference_link="_",
        )
        assert self.extractor._has_coreference_info(token3) is False

        # Token with no coreference fields
        token4 = Token(
            idx=4,
            text="sagte",
            sentence_num=1,
            grammatical_role="VERB",
            thematic_role="ACTION",
        )
        assert self.extractor._has_coreference_info(token4) is False

    def test_build_local_chains(self):
        """Test building local coreference chains from mentions."""
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

        chains = self.extractor._build_local_chains([token1, token2, token3])

        # We expect 3 chains: "115", "1" (from animate links), "200" (from inanimate)
        assert len(chains) == 3
        chain_ids = {chain.chain_id for chain in chains}
        assert "115" in chain_ids
        assert "1" in chain_ids
        assert "200" in chain_ids

        # Check the "115" chain
        chain_115 = next(chain for chain in chains if chain.chain_id == "115")
        assert len(chain_115.mentions) == 2
        assert chain_115.animacy == AnimacyType.ANIMATE

        # Check the "200" chain
        chain_200 = next(chain for chain in chains if chain.chain_id == "200")
        assert len(chain_200.mentions) == 1
        assert chain_200.animacy == AnimacyType.INANIMATE

    def test_determine_chain_animacy_animate(self):
        """Test determining animacy for animate chain."""
        token = Token(
            idx=1,
            text="er",
            sentence_num=1,
            grammatical_role="SUBJ",
            thematic_role="AGENT",
            coreference_link="*->115-1",
        )

        animacy = self.extractor._determine_chain_animacy([token])

        assert animacy == AnimacyType.ANIMATE

    def test_determine_chain_animacy_inanimate(self):
        """Test determining animacy for inanimate chain."""
        token = Token(
            idx=1,
            text="Buch",
            sentence_num=1,
            grammatical_role="OBJ",
            thematic_role="PATIENT",
            inanimate_coreference_link="*->200-1",
        )

        animacy = self.extractor._determine_chain_animacy([token])

        assert animacy == AnimacyType.INANIMATE

    def test_determine_chain_animacy_default(self):
        """Test determining animacy with no clear indicators."""
        token = Token(
            idx=1,
            text="Karl",
            sentence_num=1,
            grammatical_role="SUBJ",
            thematic_role="AGENT",
            coreference_link="*->115-1",
        )

        animacy = self.extractor._determine_chain_animacy([token])

        # Should default to animate when uncertain
        assert animacy == AnimacyType.ANIMATE

    def test_determine_token_animacy(self):
        """Test determining animacy for a single token."""
        token = Token(
            idx=1,
            text="Buch",
            sentence_num=1,
            grammatical_role="OBJ",
            thematic_role="PATIENT",
            inanimate_coreference_link="*->200-1",
        )

        animacy = self.extractor._determine_token_animacy(token)

        assert animacy == AnimacyType.INANIMATE

    def test_extract_all_ids_from_context(self):
        """Test extracting all coreference IDs from a sentence context."""
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
        token3 = Token(
            idx=3,
            text="sagte",
            sentence_num=1,
            grammatical_role="VERB",
            thematic_role="ACTION",
        )

        context = SentenceContext(
            sentence_id="1",
            sentence_num=1,
            tokens=[token1, token2, token3],
            critical_pronouns=[],
            coreference_phrases=[],
            first_words="Karl_sagte",
        )

        ids = self.extractor._extract_all_ids_from_context(context)

        assert "115" in ids
        assert "200" in ids
        assert "1" in ids  # From the animate coreference link
        assert len(ids) == 3
