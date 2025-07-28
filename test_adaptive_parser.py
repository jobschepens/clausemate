#!/usr/bin/env python3
"""Test script for the adaptive TSV parser.

This script tests the new adaptive parser with different input files
to verify that it can handle multiple column formats correctly.
"""

import logging
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.parsers.adaptive_tsv_parser import AdaptiveTSVParser
from src.parsers.tsv_parser import DefaultTokenProcessor

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)


def test_file(file_path: str, description: str):
    """Test parsing a single file with the adaptive parser."""
    
    print(f"\n{'='*60}")
    print(f"Testing: {description}")
    print(f"File: {file_path}")
    print(f"{'='*60}")
    
    try:
        # Create parser with default processor
        processor = DefaultTokenProcessor()
        parser = AdaptiveTSVParser(processor)
        
        # Parse the file
        sentences = parser.parse_file(file_path)
        
        # Get format info and statistics
        format_info = parser.get_format_info()
        stats = parser.get_parsing_statistics()
        
        # Display results
        print(f"✅ SUCCESS: Parsed {len(sentences)} sentences")
        
        if format_info:
            print(f"📊 Format Type: {format_info.format_type}")
            print(f"📊 Total Columns: {format_info.total_columns}")
            print(f"📊 Compatibility Score: {format_info.compatibility_score:.2f}")
            print(f"📊 Token Count: {format_info.token_count}")
            print(f"📊 Sentence Count: {format_info.sentence_count}")
            
            if format_info.issues:
                print(f"⚠️  Issues: {', '.join(format_info.issues)}")
            
            if format_info.additional_columns:
                print(f"📈 Additional Columns: {len(format_info.additional_columns)}")
        
        # Show sample sentences
        print(f"\n📝 Sample sentences:")
        for i, (sentence_id, tokens) in enumerate(list(sentences.items())[:3]):
            print(f"  Sentence {sentence_id}: {len(tokens)} tokens")
            if tokens:
                sample_tokens = tokens[:5]  # First 5 tokens
                token_texts = [token.text for token in sample_tokens]
                print(f"    Tokens: {' '.join(token_texts)}{'...' if len(tokens) > 5 else ''}")
                
                # Show coreference info for first token if available
                first_token = tokens[0]
                if first_token.coreference_link or first_token.coreference_type:
                    print(f"    Coreference: link={first_token.coreference_link}, type={first_token.coreference_type}")
        
        return True
        
    except Exception as e:
        print(f"❌ FAILED: {str(e)}")
        logger.error(f"Error testing {file_path}: {str(e)}", exc_info=True)
        return False


def main():
    """Run tests on all available input files."""
    
    print("🚀 Testing Adaptive TSV Parser")
    print("Testing multiple input file formats for compatibility")
    
    # Test files to check
    test_files = [
        ("data/input/gotofiles/2.tsv", "Current standard file (15 columns)"),
        ("data/input/gotofiles/later/1.tsv", "Extended format file (38 columns)"),
        ("data/input/gotofiles/later/3.tsv", "Alternative test file"),
        ("data/input/gotofiles/later/4.tsv", "Another alternative test file"),
    ]
    
    results = []
    
    for file_path, description in test_files:
        if Path(file_path).exists():
            success = test_file(file_path, description)
            results.append((file_path, success))
        else:
            print(f"\n⚠️  SKIPPED: {file_path} (file not found)")
            results.append((file_path, None))
    
    # Summary
    print(f"\n{'='*60}")
    print("📋 SUMMARY")
    print(f"{'='*60}")
    
    successful = sum(1 for _, success in results if success is True)
    failed = sum(1 for _, success in results if success is False)
    skipped = sum(1 for _, success in results if success is None)
    
    print(f"✅ Successful: {successful}")
    print(f"❌ Failed: {failed}")
    print(f"⚠️  Skipped: {skipped}")
    
    if failed == 0 and successful > 0:
        print(f"\n🎉 All available files parsed successfully!")
        print(f"The adaptive parser is working correctly with multiple formats.")
    elif failed > 0:
        print(f"\n⚠️  Some files failed to parse. Check the errors above.")
    else:
        print(f"\n⚠️  No files were successfully parsed.")
    
    return failed == 0


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)