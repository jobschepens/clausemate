"""Mock data objects for unit testing.

This module provides mock objects and test data for isolated unit testing
of individual components without requiring full file parsing.
"""

from typing import Any, Dict, List, Optional

# Import the actual data models
try:
    from src.data.models import (
        AnimacyType,
        AntecedentInfo,
        ClauseMateRelationship,
        CoreferencePhrase,
        Phrase,
        SentenceContext,
        Token,
    )
except ImportError:
    # Fallback for when running tests directly
    import sys
    from pathlib import Path

    sys.path.append(str(Path(__file__).parent.parent.parent / "src"))
    from data.models import (
        AnimacyType,
        AntecedentInfo,
        ClauseMateRelationship,
        CoreferencePhrase,
        Phrase,
        SentenceContext,
        Token,
    )


class MockDataFactory:
    """Factory for creating mock test data objects."""

    @staticmethod
    def create_mock_token(
        idx: int = 1,
        text: str = "He",
        sentence_num: int = 1,
        grammatical_role: str = "nsubj",
        thematic_role: str = "agent",
        coreference_link: Optional[str] = None,
        is_critical_pronoun: bool = False,
    ) -> Token:
        """Create a mock Token object."""
        return Token(
            idx=idx,
            text=text,
            sentence_num=sentence_num,
            grammatical_role=grammatical_role,
            thematic_role=thematic_role,
            coreference_link=coreference_link,
            is_critical_pronoun=is_critical_pronoun,
        )

    @staticmethod
    def create_mock_antecedent_info(
        most_recent_text: str = "book",
        most_recent_distance: str = "0",
        first_text: str = "book",
        first_distance: str = "0",
        sentence_id: str = "1",
        choice_count: int = 1,
    ) -> AntecedentInfo:
        """Create a mock AntecedentInfo object."""
        return AntecedentInfo(
            most_recent_text=most_recent_text,
            most_recent_distance=most_recent_distance,
            first_text=first_text,
            first_distance=first_distance,
            sentence_id=sentence_id,
            choice_count=choice_count,
        )

    @staticmethod
    def create_mock_phrase(
        text: str = "the book",
        coreference_id: str = "(2)",
        start_idx: int = 3,
        end_idx: int = 4,
        grammatical_role: str = "obj",
        thematic_role: str = "theme",
        coreference_type: str = "defNP",
        animacy: AnimacyType = AnimacyType.INANIMATE,
        givenness: str = "new",
    ) -> Phrase:
        """Create a mock Phrase object."""
        return Phrase(
            text=text,
            coreference_id=coreference_id,
            start_idx=start_idx,
            end_idx=end_idx,
            grammatical_role=grammatical_role,
            thematic_role=thematic_role,
            coreference_type=coreference_type,
            animacy=animacy,
            givenness=givenness,
        )

    @staticmethod
    def create_mock_sentence_context(
        sentence_id: str = "1",
        sentence_num: int = 1,
        tokens: Optional[List[Token]] = None,
        critical_pronouns: Optional[List[Token]] = None,
        coreference_phrases: Optional[List[CoreferencePhrase]] = None,
    ) -> SentenceContext:
        """Create a mock SentenceContext object."""
        if tokens is None:
            tokens = [
                MockDataFactory.create_mock_token(
                    1, "He", 1, "nsubj", "agent", "(1)", True
                ),
                MockDataFactory.create_mock_token(2, "reads", 1, "root", "action"),
                MockDataFactory.create_mock_token(3, "the", 1, "det", "determiner"),
                MockDataFactory.create_mock_token(4, "book", 1, "obj", "theme", "(2)"),
            ]

        if critical_pronouns is None:
            critical_pronouns = [token for token in tokens if token.is_critical_pronoun]

        if coreference_phrases is None:
            coreference_phrases = []

        return SentenceContext(
            sentence_id=sentence_id,
            sentence_num=sentence_num,
            tokens=tokens,
            critical_pronouns=critical_pronouns,
            coreference_phrases=coreference_phrases,
        )

    @staticmethod
    def create_mock_relationship(
        sentence_id: str = "1",
        sentence_num: int = 1,
        pronoun: Optional[Token] = None,
        clause_mate: Optional[Phrase] = None,
        num_clause_mates: int = 1,
        antecedent_info: Optional[AntecedentInfo] = None,
    ) -> ClauseMateRelationship:
        """Create a mock ClauseMateRelationship object."""
        if pronoun is None:
            pronoun = MockDataFactory.create_mock_token(
                1, "He", 1, "nsubj", "agent", "(1)", True
            )

        if clause_mate is None:
            clause_mate = MockDataFactory.create_mock_phrase()

        if antecedent_info is None:
            antecedent_info = MockDataFactory.create_mock_antecedent_info()

        return ClauseMateRelationship(
            sentence_id=sentence_id,
            sentence_num=sentence_num,
            pronoun=pronoun,
            clause_mate=clause_mate,
            num_clause_mates=num_clause_mates,
            antecedent_info=antecedent_info,
        )


class MockTSVData:
    """Mock TSV data for different formats."""

    STANDARD_15COL_HEADER = [
        "sentence_id",
        "token_id",
        "token_start",
        "token_end",
        "token",
        "pos",
        "lemma",
        "deprel",
        "head",
        "misc",
        "coreference",
        "segment",
        "morphology",
        "syntax",
        "semantics",
    ]

    EXTENDED_37COL_HEADER = STANDARD_15COL_HEADER + [
        f"extra_col_{i}"
        for i in range(22)  # 37 - 15 = 22 extra columns
    ]

    LEGACY_14COL_HEADER = [
        "sentence_id",
        "token_id",
        "token_start",
        "token_end",
        "token",
        "pos",
        "lemma",
        "deprel",
        "head",
        "misc",
        "coreference",
        "segment",
        "morphology",
        "syntax",
    ]

    INCOMPLETE_12COL_HEADER = [
        "sentence_id",
        "token_id",
        "token_start",
        "token_end",
        "token",
        "pos",
        "lemma",
        "deprel",
        "head",
        "misc",
        "coreference",
        "segment",
    ]

    @staticmethod
    def get_sample_row(format_type: str = "standard") -> List[str]:
        """Get a sample data row for the specified format."""
        base_row = [
            "1-1",
            "1",
            "0",
            "2",
            "He",
            "PRP",
            "he",
            "nsubj",
            "2",
            "_",
            "(1)",
            "_",
        ]

        if format_type == "standard":
            return base_row + ["_", "_", "_"]
        elif format_type == "extended":
            return base_row + ["_"] * 25  # 37 - 12 = 25 extra columns
        elif format_type == "legacy":
            return base_row + ["_", "_"]
        elif format_type == "incomplete":
            return base_row
        else:
            raise ValueError(f"Unknown format type: {format_type}")


class MockParserResults:
    """Mock parser results for testing."""

    @staticmethod
    def create_mock_parser_result(
        format_type: str = "standard", relationship_count: int = 2
    ) -> Dict[str, Any]:
        """Create mock parser results."""
        return {
            "format_detected": format_type,
            "relationships_found": relationship_count,
            "sentences_processed": 2,
            "tokens_processed": 8,
            "coreference_chains": 2,
            "processing_time": 0.5,
            "memory_usage": "25MB",
        }


class MockFileSystem:
    """Mock file system operations for testing."""

    @staticmethod
    def create_mock_file_content(format_type: str = "standard") -> str:
        """Create mock file content for testing."""
        preamble = """#FORMAT=WebAnno TSV 3.6.1
#T_SP=webanno.custom.Referentiality|entity|head
#T_RL=webanno.custom.Referentiality|entity|BT_webanno.custom.Referentiality


"""

        if format_type == "standard":
            content = """#Text=He reads the book.
1-1	0-2	He	PRP	he	nsubj	2	_	_	(1)	_	_	_	_	_
1-2	3-8	reads	VBZ	read	root	0	_	_	_	_	_	_	_	_
1-3	9-12	the	DT	the	det	4	_	_	_	_	_	_	_	_
1-4	13-17	book	NN	book	obj	2	_	_	(2)	_	_	_	_	_
"""
        elif format_type == "incomplete":
            content = """#Text=He reads the book.
1-1	0-2	He	PRP	he	nsubj	2	_	_	(1)	_	_
1-2	3-8	reads	VBZ	read	root	0	_	_	_	_	_
1-3	9-12	the	DT	the	det	4	_	_	_	_	_
1-4	13-17	book	NN	book	obj	2	_	_	(2)	_	_
"""
        else:
            content = """#Text=He reads the book.
1-1	0-2	He	PRP	he	nsubj	2	_	_	(1)	_	_	_	_
1-2	3-8	reads	VBZ	read	root	0	_	_	_	_	_	_	_
1-3	9-12	the	DT	the	det	4	_	_	_	_	_	_	_
1-4	13-17	book	NN	book	obj	2	_	_	(2)	_	_	_	_
"""

        return preamble + content


# Convenience functions for quick mock creation
def mock_token(**kwargs) -> Token:
    """Quick mock token creation."""
    return MockDataFactory.create_mock_token(**kwargs)


def mock_antecedent_info(**kwargs) -> AntecedentInfo:
    """Quick mock antecedent info creation."""
    return MockDataFactory.create_mock_antecedent_info(**kwargs)


def mock_phrase(**kwargs) -> Phrase:
    """Quick mock phrase creation."""
    return MockDataFactory.create_mock_phrase(**kwargs)


def mock_sentence_context(**kwargs) -> SentenceContext:
    """Quick mock sentence context creation."""
    return MockDataFactory.create_mock_sentence_context(**kwargs)


def mock_relationship(**kwargs) -> ClauseMateRelationship:
    """Quick mock relationship creation."""
    return MockDataFactory.create_mock_relationship(**kwargs)


# Test data constants
TEST_FORMATS = ["standard", "extended", "legacy", "incomplete"]
TEST_RELATIONSHIP_COUNTS = {"standard": 2, "extended": 3, "legacy": 2, "incomplete": 1}
TEST_COLUMN_COUNTS = {"standard": 15, "extended": 37, "legacy": 14, "incomplete": 12}

# Performance test data
PERFORMANCE_TEST_DATA = {
    "small_file": {"rows": 100, "expected_time": 0.5},
    "medium_file": {"rows": 1000, "expected_time": 2.0},
    "large_file": {"rows": 5000, "expected_time": 8.0},
}
