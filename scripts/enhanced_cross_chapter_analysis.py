#!/usr/bin/env python3
"""Enhanced Cross-Chapter Coreference Chain Analysis.

Tests whether coreference chains from chapter 4 appear in earlier chapters
(1.tsv, 2.tsv, 3.tsv) using production parsers for reliable data extraction.
"""

import re
import sys
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path

# Add src to path for imports
sys.path.append(str(Path(__file__).parent / "src"))

from src.main import ClauseMateAnalyzer


@dataclass
class ChainAnalysis:
    """Analysis results for coreference chains in a chapter."""

    file_path: str
    chapter_num: int
    relationships_count: int
    chains_by_id: dict[str, list[dict]]  # chain_id -> mentions
    chain_texts: dict[str, set[str]]  # chain_id -> unique texts
    sentence_range: tuple[int, int]


class EnhancedCrossChapterAnalyzer:
    """Enhanced analyzer focusing on cross-chapter chain detection."""

    def __init__(self):
        """Initializes the analyzer with chapter file paths."""
        self.chapter_files = [
            ("data/input/gotofiles/later/1.tsv", 1),  # Chapter 1
            ("data/input/gotofiles/2.tsv", 2),  # Chapter 2
            ("data/input/gotofiles/later/3.tsv", 3),  # Chapter 3
            ("data/input/gotofiles/later/4.tsv", 4),  # Chapter 4
        ]
        self.chapter_analyses: list[ChainAnalysis] = []

    def run_analysis(self):
        """Main analysis method."""
        print("=" * 80)
        print("ENHANCED CROSS-CHAPTER COREFERENCE ANALYSIS")
        print("Focus: Check if Chapter 4 chains appear in earlier chapters")
        print("=" * 80)
        print()

        # 1. Extract coreference chains from all chapters
        print("🔍 EXTRACTING COREFERENCE CHAINS FROM ALL CHAPTERS...")
        for file_path, chapter_num in self.chapter_files:
            try:
                analysis = self.extract_chains_from_chapter(file_path, chapter_num)
                self.chapter_analyses.append(analysis)
                print(
                    f"✅ Chapter {chapter_num}: {analysis.relationships_count} relationships, "
                    f"{len(analysis.chains_by_id)} unique chains."
                )
            except Exception as e:
                print(f"❌ Chapter {chapter_num}: Error - {e}")

        print()

        # 2. Analyze Chapter 4 chains specifically
        print("📊 ANALYZING CHAPTER 4 CHAINS...")
        chapter_4_analysis = next(
            (a for a in self.chapter_analyses if a.chapter_num == 4), None
        )
        if chapter_4_analysis:
            self.analyze_chapter_4_chains(chapter_4_analysis)
        else:
            print("❌ Chapter 4 analysis not available")

        print()

        # 3. Check for cross-chapter chain matches
        print("🔗 CHECKING FOR CROSS-CHAPTER CHAIN MATCHES...")
        self.check_cross_chapter_matches()

        print()

        # 4. Generate comprehensive report
        print("📋 GENERATING COMPREHENSIVE REPORT...")
        self.generate_enhanced_report()

    def extract_chains_from_chapter(
        self, file_path: str, chapter_num: int
    ) -> ChainAnalysis:
        """Extract coreference chains from a chapter using production analyzer."""
        if not Path(file_path).exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        # Create fresh analyzer for each file to avoid state persistence issues
        analyzer = ClauseMateAnalyzer(enable_adaptive_parsing=True)

        # Use production analyzer to get relationships
        relationships = analyzer.analyze_file(file_path)

        # Extract coreference chains from relationships
        chains_by_id = defaultdict(list)
        chain_texts = defaultdict(set)
        sentence_numbers = []

        for rel in relationships:
            sentence_numbers.append(rel.sentence_num)

            # Extract chain information from pronoun coreference link
            if (
                rel.pronoun.coreference_link
                and rel.pronoun.coreference_link != "_"
                and "->" in rel.pronoun.coreference_link
            ):
                chain_id = rel.pronoun.coreference_link.split("->")[1].split("-")[0]
                chains_by_id[chain_id].append(
                    {
                        "text": rel.pronoun.text,
                        "sentence": rel.sentence_num,
                        "type": "pronoun_link",
                        "position": rel.pronoun.idx,
                    }
                )
                chain_texts[chain_id].add(rel.pronoun.text.lower())

            # Extract chain information from pronoun coreference type
            if rel.pronoun.coreference_type and rel.pronoun.coreference_type != "_":
                match = re.search(r"\[(\d+)\]", rel.pronoun.coreference_type)
                if match:
                    chain_id = match.group(1)
                    chains_by_id[chain_id].append(
                        {
                            "text": rel.pronoun.text,
                            "sentence": rel.sentence_num,
                            "type": "pronoun_type",
                            "position": rel.pronoun.idx,
                        }
                    )
                    chain_texts[chain_id].add(rel.pronoun.text.lower())

            # Extract chain information from clause mate
            if rel.clause_mate.coreference_id and rel.clause_mate.coreference_id != "_":
                chain_id = rel.clause_mate.coreference_id
                chains_by_id[chain_id].append(
                    {
                        "text": rel.clause_mate.text,
                        "sentence": rel.sentence_num,
                        "type": "clause_mate",
                        "position": rel.clause_mate.start_idx,
                    }
                )
                chain_texts[chain_id].add(rel.clause_mate.text.lower())

        # Calculate sentence range
        sentence_range = (
            (min(sentence_numbers), max(sentence_numbers))
            if sentence_numbers
            else (0, 0)
        )

        return ChainAnalysis(
            file_path=file_path,
            chapter_num=chapter_num,
            relationships_count=len(relationships),
            chains_by_id=dict(chains_by_id),
            chain_texts=dict(chain_texts),
            sentence_range=sentence_range,
        )

    def analyze_chapter_4_chains(self, chapter_4: ChainAnalysis):
        """Analyze Chapter 4 chains in detail."""
        print(f"Chapter 4 contains {len(chapter_4.chains_by_id)} unique chains:")

        if not chapter_4.chains_by_id:
            print("\n⚠️  WARNING: Chapter 4 contains no coreference chains!")
            print("Expected: 695 relationships based on production system")
            print(f"Actual: {chapter_4.relationships_count} relationships extracted")
            print("This suggests a parser configuration issue with 4.tsv processing.")
            print("The production system shows 4.tsv should extract 695 relationships.")
            return

        # Sort chains by frequency (number of mentions)
        sorted_chains = sorted(
            chapter_4.chains_by_id.items(), key=lambda x: len(x[1]), reverse=True
        )

        print("\nTop 10 most frequent chains in Chapter 4:")
        for i, (chain_id, mentions) in enumerate(sorted_chains[:10]):
            texts = chapter_4.chain_texts.get(chain_id, set())
            sentences = [m["sentence"] for m in mentions]
            print(
                f"  {i + 1:2d}. Chain {chain_id}: {len(mentions)} mentions, "
                f"texts: {sorted(texts)}, sentences: {min(sentences)}-{max(sentences)}"
            )

        if chapter_4.chains_by_id:
            min_id = min(chapter_4.chains_by_id.keys())
            max_id = max(chapter_4.chains_by_id.keys())
            print(f"\nChain ID range in Chapter 4: {min_id} - {max_id}")

    def check_cross_chapter_matches(self):
        """Check if Chapter 4 chains appear in earlier chapters."""
        chapter_4 = next((a for a in self.chapter_analyses if a.chapter_num == 4), None)
        if not chapter_4:
            print("❌ Chapter 4 not available for comparison")
            return

        earlier_chapters = [a for a in self.chapter_analyses if a.chapter_num < 4]

        print("Checking Chapter 4 chains against earlier chapters...")

        cross_chapter_matches = []

        for earlier_chapter in earlier_chapters:
            print(f"\n🔍 Chapter 4 → Chapter {earlier_chapter.chapter_num}:")

            # Check for same chain IDs
            chapter_4_ids = set(chapter_4.chains_by_id.keys())
            earlier_ids = set(earlier_chapter.chains_by_id.keys())
            common_ids = chapter_4_ids.intersection(earlier_ids)

            if common_ids:
                print(f"  🎯 SAME CHAIN IDs FOUND: {len(common_ids)} chains")
                for chain_id in sorted(common_ids):
                    ch4_mentions = len(chapter_4.chains_by_id[chain_id])
                    earlier_mentions = len(earlier_chapter.chains_by_id[chain_id])
                    ch4_texts = chapter_4.chain_texts.get(chain_id, set())
                    earlier_texts = earlier_chapter.chain_texts.get(chain_id, set())

                    cross_chapter_matches.append(
                        {
                            "type": "same_chain_id",
                            "chain_id": chain_id,
                            "chapter_4_mentions": ch4_mentions,
                            "earlier_chapter": earlier_chapter.chapter_num,
                            "earlier_mentions": earlier_mentions,
                            "chapter_4_texts": ch4_texts,
                            "earlier_texts": earlier_texts,
                            "common_texts": ch4_texts.intersection(earlier_texts),
                        }
                    )

                    print(
                        f"    Chain {chain_id}: Ch4({ch4_mentions}) ↔ "
                        f"Ch{earlier_chapter.chapter_num}({earlier_mentions})"
                    )
                    common_texts = ch4_texts.intersection(earlier_texts)
                    if common_texts:
                        print(f"      Common texts: {sorted(common_texts)}")
            else:
                print("  ❌ No same chain IDs found")

            # Check for similar texts across different chain IDs
            text_matches = 0
            for ch4_id, ch4_texts in chapter_4.chain_texts.items():
                for earlier_id, earlier_texts in earlier_chapter.chain_texts.items():
                    if ch4_id != earlier_id:  # Different chain IDs
                        common_texts = ch4_texts.intersection(earlier_texts)
                        if common_texts:
                            text_matches += 1
                            cross_chapter_matches.append(
                                {
                                    "type": "similar_texts",
                                    "chapter_4_chain": ch4_id,
                                    "earlier_chapter": earlier_chapter.chapter_num,
                                    "earlier_chain": earlier_id,
                                    "common_texts": common_texts,
                                }
                            )

            if text_matches > 0:
                print(f"  🔤 Similar text matches: {text_matches} chain pairs")

        self.cross_chapter_matches = cross_chapter_matches

        print(
            f"\n📊 TOTAL CROSS-CHAPTER EVIDENCE: {len(cross_chapter_matches)} connections."
        )

    def generate_enhanced_report(self):
        """Generate comprehensive analysis report."""
        print("\n" + "=" * 80)
        print("ENHANCED CROSS-CHAPTER ANALYSIS REPORT")
        print("=" * 80)

        # System validation
        print("\n🔧 SYSTEM VALIDATION:")
        total_relationships = sum(a.relationships_count for a in self.chapter_analyses)
        expected_total = 1904  # 448 + 234 + 527 + 695
        print(f"  Total relationships extracted: {total_relationships}")
        print(f"  Expected total (production): {expected_total}")

        if total_relationships == expected_total:
            print("  ✅ VALIDATION PASSED: All files processed correctly.")
        else:
            warning_msg = (
                f"  ⚠️  VALIDATION WARNING: "
                f"{expected_total - total_relationships} relationships missing."
            )
            print(warning_msg)

        # Chapter summary
        print("\n📖 CHAPTER SUMMARY:")
        for analysis in self.chapter_analyses:
            min_sent, max_sent = analysis.sentence_range
            print(
                f"  Chapter {analysis.chapter_num} ({Path(analysis.file_path).name}): "
                f"{analysis.relationships_count} relationships, "
                f"sentences {min_sent}-{max_sent}, "
                f"{len(analysis.chains_by_id)} coreference chains"
            )

        # Cross-chapter evidence
        print("\n🔗 CROSS-CHAPTER EVIDENCE:")
        same_id_matches = [
            m for m in self.cross_chapter_matches if m["type"] == "same_chain_id"
        ]
        similar_text_matches = [
            m for m in self.cross_chapter_matches if m["type"] == "similar_texts"
        ]

        if self.cross_chapter_matches:
            print(
                f"  ✅ EVIDENCE FOUND: {len(self.cross_chapter_matches)} total connections."
            )

            if same_id_matches:
                print(
                    f"    🎯 Same Chain ID Evidence: {len(same_id_matches)} connections."
                )
                print(
                    "      This is STRONG evidence for cross-chapter coreference chains!"
                )
                for match in same_id_matches[:5]:  # Show first 5
                    print(
                        f"        Chain {match['chain_id']}: "
                        f"Ch4({match['chapter_4_mentions']}) ↔ "
                        f"Ch{match['earlier_chapter']}({match['earlier_mentions']})"
                    )
                    if match["common_texts"]:
                        print(
                            f"          Common texts: {sorted(match['common_texts'])}"
                        )

            if similar_text_matches:
                print(
                    f"    🔤 Similar Text Evidence: {len(similar_text_matches)} connections."
                )
                print(
                    "      This provides supporting evidence for character continuity."
                )
                for match in similar_text_matches[:3]:  # Show first 3
                    print(
                        f"        Ch4 Chain {match['chapter_4_chain']} ↔ "
                        f"Ch{match['earlier_chapter']} Chain {match['earlier_chain']}: "
                        f"{sorted(match['common_texts'])}"
                    )
        else:
            print("  ❌ NO EVIDENCE FOUND: No cross-chapter connections detected.")

        # Final recommendations
        print("\n💡 FINAL RECOMMENDATIONS:")
        if same_id_matches:
            print("  ✅ UNIFIED PROCESSING STRONGLY RECOMMENDED")
            print("    - Clear evidence of coreference chains spanning chapters")
            print("    - Same chain IDs found across chapter boundaries")
            print("    - Implement cross-chapter coreference resolution")
            print("    - Use unified sentence numbering system")
            print("    - Create single output file with chapter metadata")

            confidence = "VERY HIGH"
        elif similar_text_matches:
            print("  ⚠️  UNIFIED PROCESSING RECOMMENDED")
            print("    - Some evidence of character continuity across chapters")
            print("    - Consider unified processing for better coherence")

            confidence = "MEDIUM"
        else:
            print("  ℹ️  SEPARATE PROCESSING ACCEPTABLE")
            print("    - No clear evidence of cross-chapter coreference chains")
            print("    - Each chapter appears linguistically independent")

            confidence = "HIGH (for independence)"

        print(f"\n🎯 CONFIDENCE LEVEL: {confidence}")

        print("\n🏁 ANALYSIS COMPLETE")
        print("=" * 80)


def main():
    """Run the enhanced cross-chapter coreference analysis."""
    analyzer = EnhancedCrossChapterAnalyzer()

    try:
        analyzer.run_analysis()
    except KeyboardInterrupt:
        print("\n\n⚠️  Analysis interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Analysis failed: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    main()
