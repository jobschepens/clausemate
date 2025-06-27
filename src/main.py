"""
Main orchestrator for the clause mates analyzer.

This module provides the primary interface for running the analysis pipeline,
coordinating between parsers, extractors, and analyzers in a clean, modular way.
"""

import logging
from pathlib import Path
from typing import List, Dict, Any, Optional

# Import from the modular components
try:
    # Try relative imports first (when run as module)
    from .parsers.tsv_parser import TSVParser, DefaultTokenProcessor
    from .extractors.coreference_extractor import CoreferenceExtractor
    from .extractors.pronoun_extractor import PronounExtractor
    from .extractors.phrase_extractor import PhraseExtractor
    from .extractors.relationship_extractor import RelationshipExtractor
    from .data.models import ClauseMateRelationship, SentenceContext
except ImportError:
    # Fall back to absolute imports (when run directly)
    import sys
    from pathlib import Path
    sys.path.append(str(Path(__file__).parent.parent))
    
    from src.parsers.tsv_parser import TSVParser, DefaultTokenProcessor
    from src.extractors.coreference_extractor import CoreferenceExtractor
    from src.extractors.pronoun_extractor import PronounExtractor
    from src.extractors.phrase_extractor import PhraseExtractor
    from src.extractors.relationship_extractor import RelationshipExtractor
    from src.data.models import ClauseMateRelationship, SentenceContext

# Import from root directory modules
import sys
sys.path.append(str(Path(__file__).parent.parent))
from config import FilePaths
from exceptions import ClauseMateExtractionError


class ClauseMateAnalyzer:
    """
    Main analyzer class that orchestrates the complete processing pipeline.
    
    This class provides a clean, simple interface for clause mate analysis
    while maintaining the modular architecture underneath.
    """
    
    def __init__(
        self, 
        enable_streaming: bool = False,
        log_level: int = logging.INFO
    ):
        """
        Initialize the clause mate analyzer.
        
        Args:
            enable_streaming: Whether to use streaming parsing for large files
            log_level: Logging level for the analyzer
        """
        # Set up logging
        logging.basicConfig(level=log_level, format='%(asctime)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger(__name__)
        
        # Initialize components
        self.token_processor = DefaultTokenProcessor()
        self.parser = TSVParser(self.token_processor)
        self.coreference_extractor = CoreferenceExtractor()
        self.pronoun_extractor = PronounExtractor()
        self.phrase_extractor = PhraseExtractor()
        self.relationship_extractor = RelationshipExtractor()
        
        self.enable_streaming = enable_streaming
        
        # Statistics
        self.stats = {
            'sentences_processed': 0,
            'tokens_processed': 0,
            'relationships_found': 0,
            'coreference_chains_found': 0,
            'critical_pronouns_found': 0,
            'phrases_found': 0
        }
    
    def analyze_file(self, file_path: str) -> List[ClauseMateRelationship]:
        """
        Analyze a TSV file and extract clause mate relationships.
        
        Args:
            file_path: Path to the TSV file to analyze
            
        Returns:
            List of clause mate relationships found
            
        Raises:
            ClauseMateExtractionError: If analysis fails
        """
        self.logger.info(f"Starting analysis of file: {file_path}")
        
        try:
            if self.enable_streaming:
                return self._analyze_streaming(file_path)
            else:
                return self._analyze_complete(file_path)
                
        except Exception as e:
            self.logger.error(f"Analysis failed: {str(e)}")
            raise ClauseMateExtractionError(f"Failed to analyze file {file_path}: {str(e)}")
    
    def _analyze_complete(self, file_path: str) -> List[ClauseMateRelationship]:
        """
        Analyze file by loading all sentences into memory.
        
        This approach prioritizes simplicity and maintainability over memory efficiency.
        """
        self.logger.info("Using complete file analysis (prioritizing maintainability)")
        
        # Parse all sentences
        sentences = self.parser.parse_file(file_path)
        self.stats['sentences_processed'] = len(sentences)
        
        # Create sentence contexts
        contexts = []
        for sentence_id, tokens in sentences.items():
            # Extract sentence number from ID
            sentence_num = self._extract_sentence_number(sentence_id)
            
            context = SentenceContext(
                sentence_id=sentence_id,
                sentence_num=sentence_num,
                tokens=tokens,
                critical_pronouns=[],  # Will be populated
                coreference_phrases=[]  # Will be populated
            )
            contexts.append(context)
            self.stats['tokens_processed'] += len(tokens)
        
        # Extract coreference information
        all_chains = self.coreference_extractor.extract_coreference_chains(contexts)
        self.stats['coreference_chains_found'] = len(all_chains)
        
        # Extract pronouns and phrases for each context
        total_pronouns = 0
        total_phrases = 0
        all_relationships = []
        
        for context in contexts:
            # Extract pronouns
            pronoun_result = self.pronoun_extractor.extract(context)
            total_pronouns += len(pronoun_result.pronouns)
            
            # Extract phrases
            phrase_result = self.phrase_extractor.extract(context)
            total_phrases += len(phrase_result.phrases)
            
            # Extract relationships
            if context.has_critical_pronouns and context.has_coreference_phrases:
                relationship_result = self.relationship_extractor.extract(context)
                all_relationships.extend(relationship_result.relationships)
            
        self.stats['critical_pronouns_found'] = total_pronouns
        self.stats['phrases_found'] = total_phrases
        self.stats['relationships_found'] = len(all_relationships)
        
        # Return the relationships we found
        relationships = all_relationships
        
        self.logger.info(f"Analysis complete. Statistics: {self.stats}")
        return relationships
    
    def _analyze_streaming(self, file_path: str) -> List[ClauseMateRelationship]:
        """
        Analyze file using streaming for memory efficiency.
        
        This approach processes sentences one at a time to handle large files.
        """
        self.logger.info("Using streaming analysis (memory efficient)")
        
        all_relationships = []
        contexts = []
        
        # Process sentences one by one
        for context in self.parser.parse_sentence_streaming(file_path):
            contexts.append(context)
            self.stats['sentences_processed'] += 1
            self.stats['tokens_processed'] += len(context.tokens)
            
            # Extract coreference information for this sentence
            extraction_result = self.coreference_extractor.extract(context)
            
            # Process relationships (placeholder for now)
            # relationships = self._extract_relationships(context)
            # all_relationships.extend(relationships)
        
        # Extract cross-sentence coreference chains
        all_chains = self.coreference_extractor.extract_coreference_chains(contexts)
        self.stats['coreference_chains_found'] = len(all_chains)
        
        self.stats['relationships_found'] = len(all_relationships)
        self.logger.info(f"Streaming analysis complete. Statistics: {self.stats}")
        return all_relationships
    
    def export_results(
        self, 
        relationships: List[ClauseMateRelationship], 
        output_path: str
    ) -> None:
        """
        Export analysis results to a CSV file.
        
        Args:
            relationships: List of relationships to export
            output_path: Path to the output CSV file
        """
        import pandas as pd
        
        if not relationships:
            self.logger.warning("No relationships to export")
            return
        
        try:
            # Convert relationships to dictionaries
            data = [rel.to_dict() for rel in relationships]
            
            # Create DataFrame and export
            df = pd.DataFrame(data)
            df.to_csv(output_path, index=False)
            
            self.logger.info(f"Results exported to: {output_path}")
            self.logger.info(f"Exported {len(relationships)} relationships")
            
        except Exception as e:
            self.logger.error(f"Export failed: {str(e)}")
            raise ClauseMateExtractionError(f"Failed to export results: {str(e)}")
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get analysis statistics.
        
        Returns:
            Dictionary containing analysis statistics
        """
        return self.stats.copy()
    
    def _extract_sentence_number(self, sentence_id: str) -> int:
        """Extract sentence number from sentence ID."""
        import re
        match = re.search(r'(\d+)', sentence_id)
        return int(match.group(1)) if match else 1


def main():
    """
    Main entry point for the application.
    
    This function provides a simple command-line interface for the analyzer.
    """
    import argparse
    
    parser = argparse.ArgumentParser(description="Clause Mate Analyzer - Phase 2")
    parser.add_argument(
        "input_file", 
        nargs='?',
        default=FilePaths.INPUT_FILE,
        help="Input TSV file path"
    )
    parser.add_argument(
        "-o", "--output", 
        default=FilePaths.OUTPUT_FILE,
        help="Output CSV file path"
    )
    parser.add_argument(
        "--streaming", 
        action="store_true",
        help="Use streaming processing for large files"
    )
    parser.add_argument(
        "--verbose", "-v", 
        action="store_true",
        help="Enable verbose logging"
    )
    
    args = parser.parse_args()
    
    # Set logging level
    log_level = logging.DEBUG if args.verbose else logging.INFO
    
    # Create analyzer
    analyzer = ClauseMateAnalyzer(
        enable_streaming=args.streaming,
        log_level=log_level
    )
    
    try:
        # Run analysis
        relationships = analyzer.analyze_file(args.input_file)
        
        # Export results
        analyzer.export_results(relationships, args.output)
        
        # Show statistics
        stats = analyzer.get_statistics()
        print("\nAnalysis Summary:")
        for key, value in stats.items():
            print(f"  {key}: {value}")
        
    except ClauseMateExtractionError as e:
        print(f"Error: {e}")
        return 1
    except KeyboardInterrupt:
        print("\nAnalysis interrupted by user")
        return 1
    except Exception as e:
        print(f"Unexpected error: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
