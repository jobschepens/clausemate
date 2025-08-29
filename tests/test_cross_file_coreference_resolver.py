"""Tests for CrossFileCoreferenceResolver."""

from collections import defaultdict
from unittest.mock import MagicMock, patch

from src.multi_file.cross_file_coreference_resolver import CrossFileCoreferenceResolver


class MockRelationship:
    """Mock relationship object for testing."""

    def __init__(
        self,
        pronoun_coref_ids=None,
        pronoun_text="er",
        clause_mate_coref_id=None,
        clause_mate_text="Karl",
    ):
        """Initialize mock relationship for testing."""
        self.pronoun_coref_ids = pronoun_coref_ids or []
        self.pronoun = MagicMock()
        self.pronoun.text = pronoun_text
        self.clause_mate = MagicMock()
        self.clause_mate.coreference_id = clause_mate_coref_id
        self.clause_mate.text = clause_mate_text


class TestCrossFileCoreferenceResolver:
    """Test the CrossFileCoreferenceResolver class."""

    def setup_method(self):
        """Set up test fixtures."""
        self.resolver = CrossFileCoreferenceResolver()

    def test_initialization(self):
        """Test that the resolver initializes correctly."""
        assert self.resolver.cross_chapter_chains == {}
        assert self.resolver.chain_connections == defaultdict(set)
        assert self.resolver.chapter_chains == {}
        assert hasattr(self.resolver, "logger")

    def test_resolve_cross_chapter_chains_empty_input(self):
        """Test resolving with empty input."""
        result = self.resolver.resolve_cross_chapter_chains({})
        assert result == {}
        assert self.resolver.chapter_chains == {}

    def test_resolve_cross_chapter_chains_single_chapter(self):
        """Test resolving with single chapter."""
        chapter_data = {
            "chapter1.tsv": [
                MockRelationship(pronoun_coref_ids=["chain_1"], pronoun_text="er"),
                MockRelationship(pronoun_coref_ids=["chain_2"], pronoun_text="sie"),
            ]
        }

        result = self.resolver.resolve_cross_chapter_chains(chapter_data)

        # Should have no cross-chapter chains with single chapter
        assert result == {}

        # Should have extracted chapter chains
        assert "chapter1.tsv" in self.resolver.chapter_chains
        assert "chain_1" in self.resolver.chapter_chains["chapter1.tsv"]
        assert "chain_2" in self.resolver.chapter_chains["chapter1.tsv"]

    def test_resolve_cross_chapter_chains_multiple_chapters_same_chains(self):
        """Test resolving with multiple chapters having same chain IDs."""
        chapter_data = {
            "chapter1.tsv": [
                MockRelationship(pronoun_coref_ids=["chain_1"], pronoun_text="Karl"),
                MockRelationship(pronoun_coref_ids=["chain_2"], pronoun_text="er"),
            ],
            "chapter2.tsv": [
                MockRelationship(pronoun_coref_ids=["chain_1"], pronoun_text="er"),
                MockRelationship(pronoun_coref_ids=["chain_3"], pronoun_text="sie"),
            ],
        }

        result = self.resolver.resolve_cross_chapter_chains(chapter_data)

        # Should have one unified chain for chain_1
        assert len(result) == 1
        unified_chain_key = list(result.keys())[0]
        assert unified_chain_key.startswith("unified_chain_")
        assert "Karl" in result[unified_chain_key]
        assert "er" in result[unified_chain_key]

    def test_resolve_cross_chapter_chains_no_cross_chapter_chains(self):
        """Test resolving with multiple chapters having different chain IDs."""
        chapter_data = {
            "chapter1.tsv": [
                MockRelationship(pronoun_coref_ids=["chain_1"], pronoun_text="Karl")
            ],
            "chapter2.tsv": [
                MockRelationship(pronoun_coref_ids=["chain_2"], pronoun_text="er")
            ],
        }

        result = self.resolver.resolve_cross_chapter_chains(chapter_data)

        # Should have no cross-chapter chains
        assert result == {}

    def test_extract_chapter_chains_with_pronoun_coref_ids(self):
        """Test extracting chains from pronoun coreference IDs."""
        relationships = [
            MockRelationship(pronoun_coref_ids=["chain_1"], pronoun_text="Karl"),
            MockRelationship(
                pronoun_coref_ids=["chain_1", "chain_2"], pronoun_text="er"
            ),
            MockRelationship(pronoun_coref_ids=["chain_2"], pronoun_text="sie"),
        ]

        chapter_data = {"chapter1.tsv": relationships}

        # Call private method directly for testing
        self.resolver._extract_chapter_chains(chapter_data)

        assert "chapter1.tsv" in self.resolver.chapter_chains
        chapter_chains = self.resolver.chapter_chains["chapter1.tsv"]

        assert "chain_1" in chapter_chains
        assert "chain_2" in chapter_chains
        assert "Karl" in chapter_chains["chain_1"]
        assert "er" in chapter_chains["chain_1"]
        assert "er" in chapter_chains["chain_2"]
        assert "sie" in chapter_chains["chain_2"]

    def test_extract_chapter_chains_with_clause_mate_coref(self):
        """Test extracting chains from clause mate coreference IDs."""
        relationships = [
            MockRelationship(clause_mate_coref_id="chain_1", clause_mate_text="Amerika")
        ]

        chapter_data = {"chapter1.tsv": relationships}

        self.resolver._extract_chapter_chains(chapter_data)

        assert "chapter1.tsv" in self.resolver.chapter_chains
        chapter_chains = self.resolver.chapter_chains["chapter1.tsv"]

        assert "chain_1" in chapter_chains
        assert "Amerika" in chapter_chains["chain_1"]

    def test_identify_cross_chapter_connections(self):
        """Test identifying connections between chapters."""
        # Set up chapter chains
        self.resolver.chapter_chains = {
            "chapter1.tsv": {"chain_1": ["Karl"], "chain_2": ["er"]},
            "chapter2.tsv": {"chain_1": ["er"], "chain_3": ["sie"]},
            "chapter3.tsv": {"chain_2": ["sie"], "chain_4": ["es"]},
        }

        connections = self.resolver._identify_cross_chapter_connections()

        # Should find connections for chain_1 and chain_2
        assert len(connections) == 2

        # Check that connections include the expected chain IDs
        connection_chains = {conn[1] for conn in connections}
        assert "chain_1" in connection_chains
        assert "chain_2" in connection_chains

    def test_merge_connected_chains(self):
        """Test merging connected chains into unified chains."""
        # Set up chapter chains
        self.resolver.chapter_chains = {
            "chapter1.tsv": {"chain_1": ["Karl"]},
            "chapter2.tsv": {"chain_1": ["er"]},
            "chapter3.tsv": {"chain_2": ["sie"]},
        }

        # Create connections
        connections = [("chapter1.tsv", "chain_1", "chapter2.tsv", "chain_1")]

        result = self.resolver._merge_connected_chains(connections)

        # Should have one unified chain
        assert len(result) == 1
        unified_chain_key = list(result.keys())[0]
        assert unified_chain_key.startswith("unified_chain_")

        # Should contain entities from both chapters
        entities = result[unified_chain_key]
        assert "Karl" in entities
        assert "er" in entities

    def test_dfs_connected_chains(self):
        """Test DFS traversal for finding connected chains."""
        # Create a simple graph
        graph = {
            "file1:chain1": {"file2:chain1"},
            "file2:chain1": {"file1:chain1", "file3:chain1"},
            "file3:chain1": {"file2:chain1"},
        }

        visited = set()
        result = self.resolver._dfs_connected_chains("file1:chain1", graph, visited)

        # Should find all connected chains
        expected = {"file1:chain1", "file2:chain1", "file3:chain1"}
        assert result == expected
        assert visited == expected

    def test_normalize_text(self):
        """Test text normalization."""
        # Test basic normalization
        assert self.resolver._normalize_text("Karl") == "karl"
        assert self.resolver._normalize_text("ER") == "er"
        assert self.resolver._normalize_text("Karl!") == "karl"
        assert self.resolver._normalize_text("Karl  Müller") == "karl müller"

        # Test empty text
        assert self.resolver._normalize_text("") == ""
        assert self.resolver._normalize_text(None) == ""

    def test_extract_chapter_number(self):
        """Test extracting chapter number from file path."""
        # Test various file path formats
        assert self.resolver._extract_chapter_number("chapter1.tsv") == 1
        assert self.resolver._extract_chapter_number("data/chapter2.tsv") == 2
        assert self.resolver._extract_chapter_number("file3.txt") == 3
        assert self.resolver._extract_chapter_number("no_number.txt") == 1

    def test_chains_are_connected_exact_match(self):
        """Test chain connection detection with exact chain ID match."""
        assert (
            self.resolver._chains_are_connected("chain_1", ["Karl"], "chain_1", ["er"])
            is True
        )

    def test_chains_are_connected_entity_overlap(self):
        """Test chain connection detection with entity overlap."""
        assert (
            self.resolver._chains_are_connected(
                "chain_1", ["Karl"], "chain_2", ["Karl"]
            )
            is True
        )

    def test_chains_are_connected_key_entity_overlap(self):
        """Test chain connection detection with key entity overlap."""
        assert (
            self.resolver._chains_are_connected("chain_1", ["er"], "chain_2", ["er"])
            is True
        )

    def test_chains_are_connected_no_connection(self):
        """Test chain connection detection with no connection."""
        assert (
            self.resolver._chains_are_connected(
                "chain_1", ["Karl"], "chain_2", ["Anna"]
            )
            is False
        )

    def test_get_cross_chapter_summary(self):
        """Test getting cross-chapter summary."""
        # Set up some test data
        self.resolver.cross_chapter_chains = {
            "chain1": ["Karl", "er"],
            "chain2": ["sie"],
        }
        self.resolver.chapter_chains = {
            "chapter1.tsv": {"chain1": ["Karl"]},
            "chapter2.tsv": {"chain2": ["sie"]},
        }

        summary = self.resolver.get_cross_chapter_summary()

        assert summary["total_unified_chains"] == 2
        assert summary["chapters_processed"] == 2
        assert "chapter1.tsv" in summary["chapter_chain_counts"]
        assert "chapter2.tsv" in summary["chapter_chain_counts"]
        assert summary["chapter_chain_counts"]["chapter1.tsv"] == 1
        assert summary["chapter_chain_counts"]["chapter2.tsv"] == 1

    @patch("src.multi_file.cross_file_coreference_resolver.logging")
    def test_logging_initialization(self, mock_logging):
        """Test that logging is properly initialized."""
        mock_logger = MagicMock()
        mock_logging.getLogger.return_value = mock_logger

        resolver = CrossFileCoreferenceResolver()

        mock_logging.getLogger.assert_called_with(
            "src.multi_file.cross_file_coreference_resolver"
        )
        mock_logger.info.assert_called_with("CrossFileCoreferenceResolver initialized")

    def test_resolve_cross_chapter_chains_with_complex_data(self):
        """Test resolving with more complex multi-chapter data."""
        chapter_data = {
            "chapter1.tsv": [
                MockRelationship(pronoun_coref_ids=["chain_1"], pronoun_text="Karl"),
                MockRelationship(pronoun_coref_ids=["chain_1"], pronoun_text="er"),
                MockRelationship(pronoun_coref_ids=["chain_2"], pronoun_text="Amerika"),
            ],
            "chapter2.tsv": [
                MockRelationship(pronoun_coref_ids=["chain_1"], pronoun_text="er"),
                MockRelationship(pronoun_coref_ids=["chain_3"], pronoun_text="sie"),
            ],
            "chapter3.tsv": [
                MockRelationship(pronoun_coref_ids=["chain_1"], pronoun_text="ihm"),
                MockRelationship(pronoun_coref_ids=["chain_2"], pronoun_text="es"),
            ],
        }

        result = self.resolver.resolve_cross_chapter_chains(chapter_data)

        # Should have unified chains for chain_1 and chain_2
        assert len(result) >= 2

        # Find the unified chains
        unified_chains = list(result.keys())
        assert all(chain.startswith("unified_chain_") for chain in unified_chains)

        # Check that entities are properly collected
        all_entities = []
        for entities in result.values():
            all_entities.extend(entities)

        assert "Karl" in all_entities
        assert "Amerika" in all_entities
