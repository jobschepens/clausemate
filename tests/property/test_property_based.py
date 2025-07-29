"""Property-based tests for data validation and edge cases using Hypothesis."""

import string

import pytest
from hypothesis import assume, given, settings
from hypothesis import strategies as st
from hypothesis.strategies import composite

from src.data.models import Phrase, SentenceContext, Token
from src.exceptions import ValidationError


# Custom strategies for generating test data
@composite
def valid_token_data(draw):
    """Generate valid token data for property-based testing."""
    idx = draw(st.integers(min_value=1, max_value=1000))
    text = draw(
        st.text(
            alphabet=string.ascii_letters + string.digits + " .-",
            min_size=1,
            max_size=50,
        )
    )
    sentence_num = draw(st.integers(min_value=1, max_value=100))
    return {
        "idx": idx,
        "text": text.strip() or "word",  # Ensure non-empty text
        "sentence_num": sentence_num,
        "grammatical_role": draw(
            st.sampled_from(["SUBJ", "OBJ", "PRED", "ATTR", "ADV", "OTHER"])
        ),
        "pos_tag": draw(st.sampled_from(["NN", "VB", "JJ", "RB", "DT", "IN", "PRP"])),
        "lemma": draw(
            st.text(alphabet=string.ascii_lowercase, min_size=1, max_size=20)
        ),
    }


@composite
def valid_phrase_data(draw):
    """Generate valid phrase data for property-based testing."""
    start_idx = draw(st.integers(min_value=1, max_value=50))
    end_idx = draw(st.integers(min_value=start_idx, max_value=start_idx + 20))
    text = draw(
        st.text(
            alphabet=string.ascii_letters + string.digits + " .-",
            min_size=1,
            max_size=100,
        )
    )
    return {
        "start_idx": start_idx,
        "end_idx": end_idx,
        "text": text.strip() or "phrase",
        "phrase_type": draw(st.sampled_from(["NP", "VP", "PP", "ADJP", "ADVP"])),
        "coref_id": draw(st.one_of(st.none(), st.text(min_size=1, max_size=10))),
    }


@composite
def valid_sentence_context_data(draw):
    """Generate valid sentence context data."""
    sentence_num = draw(st.integers(min_value=1, max_value=100))
    sentence_id = f"sent_{sentence_num}"
    num_tokens = draw(st.integers(min_value=1, max_value=20))

    tokens = []
    for i in range(num_tokens):
        token_data = draw(valid_token_data())
        token_data["idx"] = i + 1
        token_data["sentence_num"] = sentence_num
        tokens.append(Token(**token_data))

    return {
        "sentence_id": sentence_id,
        "sentence_num": sentence_num,
        "tokens": tokens,
        "text": " ".join(token.text for token in tokens),
    }


@pytest.mark.property
class TestPropertyBasedValidation:
    """Property-based tests for data model validation."""

    @given(valid_token_data())
    @settings(max_examples=50)
    def test_token_creation_always_valid(self, token_data):
        """Test that valid token data always creates valid tokens."""
        token = Token(**token_data)

        # Properties that should always hold
        assert token.idx > 0
        assert len(token.text.strip()) > 0
        assert token.sentence_num > 0
        assert isinstance(token.grammatical_role, str)
        assert isinstance(token.pos_tag, str)

    @given(st.integers(max_value=0))
    def test_token_invalid_idx_always_fails(self, invalid_idx):
        """Test that invalid token indices always fail validation."""
        with pytest.raises(ValidationError):
            Token(
                idx=invalid_idx,
                text="word",
                sentence_num=1,
                grammatical_role="SUBJ",
                pos_tag="NN",
            )

    @given(st.text(max_size=0))
    def test_token_empty_text_always_fails(self, empty_text):
        """Test that empty token text always fails validation."""
        assume(len(empty_text.strip()) == 0)
        with pytest.raises(ValidationError):
            Token(
                idx=1,
                text=empty_text,
                sentence_num=1,
                grammatical_role="SUBJ",
                pos_tag="NN",
            )

    @given(valid_phrase_data())
    @settings(max_examples=50)
    def test_phrase_creation_always_valid(self, phrase_data):
        """Test that valid phrase data always creates valid phrases."""
        phrase = Phrase(**phrase_data)

        # Properties that should always hold
        assert phrase.start_idx > 0
        assert phrase.end_idx >= phrase.start_idx
        assert len(phrase.text.strip()) > 0
        assert isinstance(phrase.phrase_type, str)

    @given(st.integers(min_value=1, max_value=100), st.integers(max_value=0))
    def test_phrase_invalid_indices_always_fail(self, start_idx, invalid_end_idx):
        """Test that invalid phrase indices always fail validation."""
        assume(invalid_end_idx < start_idx)
        with pytest.raises(ValidationError):
            Phrase(
                start_idx=start_idx,
                end_idx=invalid_end_idx,
                text="phrase",
                phrase_type="NP",
            )

    @given(valid_sentence_context_data())
    @settings(max_examples=30)
    def test_sentence_context_creation_always_valid(self, context_data):
        """Test that valid sentence context data always creates valid contexts."""
        context = SentenceContext(**context_data)

        # Properties that should always hold
        assert context.sentence_num > 0
        assert len(context.sentence_id.strip()) > 0
        assert len(context.tokens) > 0
        assert all(isinstance(token, Token) for token in context.tokens)
        assert len(context.text.strip()) > 0

    @given(st.integers(max_value=0))
    def test_sentence_context_invalid_sentence_num_always_fails(self, invalid_num):
        """Test that invalid sentence numbers always fail validation."""
        with pytest.raises(ValidationError):
            SentenceContext(
                sentence_id="sent_1",
                sentence_num=invalid_num,
                tokens=[
                    Token(
                        idx=1,
                        text="word",
                        sentence_num=1,
                        grammatical_role="SUBJ",
                        pos_tag="NN",
                    )
                ],
                text="word",
            )


@pytest.mark.property
class TestPropertyBasedEdgeCases:
    """Property-based tests for edge cases and boundary conditions."""

    @given(st.text(alphabet=string.whitespace, min_size=1, max_size=10))
    def test_whitespace_only_text_handling(self, whitespace_text):
        """Test handling of whitespace-only text in various contexts."""
        # Should fail for tokens
        with pytest.raises(ValidationError):
            Token(
                idx=1,
                text=whitespace_text,
                sentence_num=1,
                grammatical_role="SUBJ",
                pos_tag="NN",
            )

        # Should fail for phrases
        with pytest.raises(ValidationError):
            Phrase(start_idx=1, end_idx=2, text=whitespace_text, phrase_type="NP")

    @given(st.integers(min_value=1, max_value=1000))
    def test_large_indices_handling(self, large_idx):
        """Test handling of large index values."""
        # Should work for reasonable large values
        token = Token(
            idx=large_idx,
            text="word",
            sentence_num=large_idx,
            grammatical_role="SUBJ",
            pos_tag="NN",
        )
        assert token.idx == large_idx
        assert token.sentence_num == large_idx

    @given(
        st.text(
            alphabet=string.ascii_letters + string.digits + string.punctuation,
            min_size=1,
            max_size=200,
        )
    )
    def test_special_characters_in_text(self, text_with_special_chars):
        """Test handling of special characters in text fields."""
        assume(len(text_with_special_chars.strip()) > 0)

        # Should handle special characters gracefully
        token = Token(
            idx=1,
            text=text_with_special_chars,
            sentence_num=1,
            grammatical_role="SUBJ",
            pos_tag="NN",
        )
        assert token.text == text_with_special_chars

    @given(st.lists(st.integers(min_value=1, max_value=100), min_size=1, max_size=50))
    def test_token_sequence_properties(self, token_indices):
        """Test properties of token sequences."""
        tokens = []
        for i, idx in enumerate(token_indices):
            token = Token(
                idx=idx,
                text=f"word_{i}",
                sentence_num=1,
                grammatical_role="SUBJ",
                pos_tag="NN",
            )
            tokens.append(token)

        # Properties that should hold for any token sequence
        assert len(tokens) == len(token_indices)
        assert all(isinstance(token, Token) for token in tokens)
        assert all(token.sentence_num == 1 for token in tokens)


@pytest.mark.property
class TestPropertyBasedInvariants:
    """Property-based tests for system invariants."""

    @given(valid_token_data(), valid_token_data())
    @settings(max_examples=30)
    def test_token_equality_invariants(self, token_data1, token_data2):
        """Test token equality invariants."""
        token1 = Token(**token_data1)
        token2 = Token(**token_data2)

        # Reflexivity: token equals itself
        assert token1 == token1

        # If tokens have same data, they should be equal
        if token_data1 == token_data2:
            assert token1 == token2

        # Hash consistency
        if token1 == token2:
            assert hash(token1) == hash(token2)

    @given(valid_phrase_data())
    @settings(max_examples=30)
    def test_phrase_span_invariants(self, phrase_data):
        """Test phrase span invariants."""
        phrase = Phrase(**phrase_data)

        # Span invariants
        assert phrase.end_idx >= phrase.start_idx
        span_length = phrase.end_idx - phrase.start_idx + 1
        assert span_length > 0

        # If span is 1, it's a single token phrase
        if span_length == 1:
            assert phrase.start_idx == phrase.end_idx

    @given(valid_sentence_context_data())
    @settings(max_examples=20)
    def test_sentence_context_invariants(self, context_data):
        """Test sentence context invariants."""
        context = SentenceContext(**context_data)

        # All tokens should belong to the same sentence
        assert all(
            token.sentence_num == context.sentence_num for token in context.tokens
        )

        # Token indices should be positive
        assert all(token.idx > 0 for token in context.tokens)

        # Text should be derivable from tokens (basic check)
        token_texts = [token.text for token in context.tokens]
        assert len(token_texts) == len(context.tokens)


@pytest.mark.property
@pytest.mark.slow
class TestPropertyBasedPerformance:
    """Property-based tests for performance characteristics."""

    @given(st.lists(valid_token_data(), min_size=1, max_size=100))
    @settings(max_examples=10)
    def test_token_creation_performance_scales_linearly(self, token_data_list):
        """Test that token creation performance scales reasonably."""
        import time

        start_time = time.time()
        tokens = [Token(**data) for data in token_data_list]
        end_time = time.time()

        creation_time = end_time - start_time

        # Performance should be reasonable (less than 1ms per token on average)
        avg_time_per_token = creation_time / len(token_data_list)
        assert avg_time_per_token < 0.001, (
            f"Token creation too slow: {avg_time_per_token:.6f}s per token"
        )

        # All tokens should be created successfully
        assert len(tokens) == len(token_data_list)
        assert all(isinstance(token, Token) for token in tokens)
