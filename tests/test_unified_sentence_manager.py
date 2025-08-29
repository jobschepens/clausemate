"""Tests for UnifiedSentenceManager."""

from src.multi_file.multi_file_batch_processor import ChapterInfo
from src.multi_file.unified_sentence_manager import UnifiedSentenceManager


class TestUnifiedSentenceManager:
    """Test the UnifiedSentenceManager class."""

    def setup_method(self):
        """Set up test fixtures."""
        self.manager = UnifiedSentenceManager()

    def test_initialization(self):
        """Test that the manager initializes correctly."""
        assert self.manager.chapter_sentence_ranges == {}
        assert self.manager.sentence_mapping == {}
        assert self.manager.global_sentence_counter == 0
        assert hasattr(self.manager, "logger")

    def test_process_chapters_empty_list(self):
        """Test processing with empty chapter list."""
        self.manager.process_chapters([])
        assert self.manager.chapter_sentence_ranges == {}
        assert self.manager.sentence_mapping == {}
        assert self.manager.global_sentence_counter == 0

    def test_process_chapters_single_chapter(self):
        """Test processing a single chapter."""
        chapter_info = ChapterInfo(
            file_path="/path/to/chapter1.tsv",
            chapter_number=1,
            format_type="standard",
            columns=15,
            relationships_count=10,
            sentence_range=(1, 5),
            compatibility_score=1.0,
        )

        self.manager.process_chapters([chapter_info])

        # Check chapter sentence range
        assert "/path/to/chapter1.tsv" in self.manager.chapter_sentence_ranges
        assert self.manager.chapter_sentence_ranges["/path/to/chapter1.tsv"] == (1, 5)

        # Check sentence mappings
        assert ("/path/to/chapter1.tsv", "1") in self.manager.sentence_mapping
        assert ("/path/to/chapter1.tsv", "5") in self.manager.sentence_mapping
        assert (
            self.manager.sentence_mapping[("/path/to/chapter1.tsv", "1")] == "global_1"
        )
        assert (
            self.manager.sentence_mapping[("/path/to/chapter1.tsv", "5")] == "global_5"
        )

        # Check global counter
        assert self.manager.global_sentence_counter == 5

    def test_process_chapters_multiple_chapters(self):
        """Test processing multiple chapters with continuous numbering."""
        chapters = [
            ChapterInfo(
                file_path="/path/to/chapter1.tsv",
                chapter_number=1,
                format_type="standard",
                columns=15,
                relationships_count=10,
                sentence_range=(1, 3),
                compatibility_score=1.0,
            ),
            ChapterInfo(
                file_path="/path/to/chapter2.tsv",
                chapter_number=2,
                format_type="extended",
                columns=37,
                relationships_count=15,
                sentence_range=(1, 4),
                compatibility_score=1.0,
            ),
            ChapterInfo(
                file_path="/path/to/chapter3.tsv",
                chapter_number=3,
                format_type="legacy",
                columns=14,
                relationships_count=8,
                sentence_range=(2, 5),
                compatibility_score=1.0,
            ),
        ]

        self.manager.process_chapters(chapters)

        # Check chapter ranges
        assert self.manager.chapter_sentence_ranges["/path/to/chapter1.tsv"] == (1, 3)
        assert self.manager.chapter_sentence_ranges["/path/to/chapter2.tsv"] == (4, 7)
        assert self.manager.chapter_sentence_ranges["/path/to/chapter3.tsv"] == (8, 11)

        # Check sentence mappings
        assert (
            self.manager.sentence_mapping[("/path/to/chapter1.tsv", "1")] == "global_1"
        )
        assert (
            self.manager.sentence_mapping[("/path/to/chapter1.tsv", "3")] == "global_3"
        )
        assert (
            self.manager.sentence_mapping[("/path/to/chapter2.tsv", "1")] == "global_4"
        )
        assert (
            self.manager.sentence_mapping[("/path/to/chapter2.tsv", "4")] == "global_7"
        )
        assert (
            self.manager.sentence_mapping[("/path/to/chapter3.tsv", "2")] == "global_8"
        )
        assert (
            self.manager.sentence_mapping[("/path/to/chapter3.tsv", "5")] == "global_11"
        )

        # Check global counter
        assert self.manager.global_sentence_counter == 11

    def test_get_global_sentence_id_mapped(self):
        """Test getting global sentence ID for mapped sentences."""
        # Set up mapping
        self.manager.sentence_mapping[("/path/to/chapter1.tsv", "5")] = "global_10"

        result = self.manager.get_global_sentence_id("/path/to/chapter1.tsv", "5")
        assert result == "global_10"

    def test_get_global_sentence_id_unmapped(self):
        """Test getting global sentence ID for unmapped sentences (fallback)."""
        result = self.manager.get_global_sentence_id("/path/to/chapter1.tsv", "3")
        assert result == "ch1_3"

    def test_get_global_sentence_id_unmapped_no_number(self):
        """Test getting global sentence ID for file without number (fallback)."""
        result = self.manager.get_global_sentence_id("/path/to/unknown.tsv", "5")
        assert result == "ch1_5"

    def test_get_chapter_sentence_range_existing(self):
        """Test getting sentence range for existing chapter."""
        self.manager.chapter_sentence_ranges["/path/to/chapter1.tsv"] = (5, 12)

        result = self.manager.get_chapter_sentence_range("/path/to/chapter1.tsv")
        assert result == (5, 12)

    def test_get_chapter_sentence_range_nonexistent(self):
        """Test getting sentence range for non-existent chapter."""
        result = self.manager.get_chapter_sentence_range("/path/to/missing.tsv")
        assert result == (0, 0)

    def test_get_total_sentences(self):
        """Test getting total number of sentences."""
        self.manager.global_sentence_counter = 25

        result = self.manager.get_total_sentences()
        assert result == 25

    def test_get_chapter_summary_empty(self):
        """Test getting chapter summary with no chapters."""
        result = self.manager.get_chapter_summary()
        assert result == {}

    def test_get_chapter_summary_with_chapters(self):
        """Test getting chapter summary with processed chapters."""
        # Set up chapter ranges
        self.manager.chapter_sentence_ranges = {
            "/path/to/chapter1.tsv": (1, 5),
            "/path/to/chapter2.tsv": (6, 12),
            "/path/to/chapter3.tsv": (13, 15),
        }

        result = self.manager.get_chapter_summary()

        expected = {
            "/path/to/chapter1.tsv": {
                "chapter_number": 1,
                "global_start": 1,
                "global_end": 5,
                "sentence_count": 5,
            },
            "/path/to/chapter2.tsv": {
                "chapter_number": 2,
                "global_start": 6,
                "global_end": 12,
                "sentence_count": 7,
            },
            "/path/to/chapter3.tsv": {
                "chapter_number": 3,
                "global_start": 13,
                "global_end": 15,
                "sentence_count": 3,
            },
        }

        assert result == expected

    def test_extract_chapter_number_with_number(self):
        """Test extracting chapter number from filename with number."""
        test_cases = [
            ("/path/to/chapter1.tsv", 1),
            ("/path/to/2.tsv", 2),
            ("data/chapter3.tsv", 3),
            ("chapter4.txt", 4),
            ("C:\\files\\5.tsv", 5),
        ]

        for file_path, expected in test_cases:
            result = self.manager._extract_chapter_number(file_path)
            assert result == expected

    def test_extract_chapter_number_without_number(self):
        """Test extracting chapter number from filename without number."""
        test_cases = [
            "/path/to/chapter_no_number.tsv",
            "/path/to/unknown_file.txt",
            "data/file_without_number.csv",
        ]

        for file_path in test_cases:
            result = self.manager._extract_chapter_number(file_path)
            assert result == 1  # Default fallback

    def test_process_chapters_with_gaps_in_sentence_ranges(self):
        """Test processing chapters with gaps in local sentence numbering."""
        chapters = [
            ChapterInfo(
                file_path="/path/to/chapter1.tsv",
                chapter_number=1,
                format_type="standard",
                columns=15,
                relationships_count=10,
                sentence_range=(1, 3),
                compatibility_score=1.0,
            ),
            ChapterInfo(
                file_path="/path/to/chapter2.tsv",
                chapter_number=2,
                format_type="extended",
                columns=37,
                relationships_count=15,
                sentence_range=(5, 8),  # Gap from 3 to 5
                compatibility_score=1.0,
            ),
        ]

        self.manager.process_chapters(chapters)

        # Check that global numbering is continuous despite local gaps
        assert self.manager.chapter_sentence_ranges["/path/to/chapter1.tsv"] == (1, 3)
        assert self.manager.chapter_sentence_ranges["/path/to/chapter2.tsv"] == (4, 7)

        # Check mappings account for the gap
        assert (
            self.manager.sentence_mapping[("/path/to/chapter2.tsv", "5")] == "global_4"
        )
        assert (
            self.manager.sentence_mapping[("/path/to/chapter2.tsv", "8")] == "global_7"
        )

    def test_process_chapters_resets_counter(self):
        """Test that processing chapters resets the global counter."""
        # First processing
        chapters1 = [
            ChapterInfo(
                file_path="/path/to/chapter1.tsv",
                chapter_number=1,
                format_type="standard",
                columns=15,
                relationships_count=5,
                sentence_range=(1, 2),
                compatibility_score=1.0,
            )
        ]

        self.manager.process_chapters(chapters1)
        assert self.manager.global_sentence_counter == 2

        # Second processing should reset counter
        chapters2 = [
            ChapterInfo(
                file_path="/path/to/chapter3.tsv",
                chapter_number=3,
                format_type="legacy",
                columns=14,
                relationships_count=8,
                sentence_range=(1, 3),
                compatibility_score=1.0,
            )
        ]

        self.manager.process_chapters(chapters2)
        assert self.manager.global_sentence_counter == 3

    def test_get_global_sentence_id_case_insensitive_fallback(self):
        """Test fallback ID generation handles various file path formats."""
        test_cases = [
            ("/Path/To/Chapter1.tsv", "5", "ch1_5"),
            ("C:\\Files\\2.tsv", "10", "ch2_10"),
            ("chapter3.txt", "1", "ch3_1"),
            ("unknown_file.tsv", "7", "ch1_7"),  # No number found
        ]

        for file_path, local_id, expected in test_cases:
            result = self.manager.get_global_sentence_id(file_path, local_id)
            assert result == expected
