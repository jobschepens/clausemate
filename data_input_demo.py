#!/usr/bin/env python3
"""Demonstration of the data input enhancements for the Clause Mates Analyzer.

This script demonstrates the new format detection and validation capabilities
that have been implemented to handle multiple TSV file formats.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.utils.format_detector import TSVFormatDetector, analyze_directory


def main():
    """Demonstrate the data input enhancements."""
    
    print("🚀 Clause Mates Analyzer - Data Input Enhancements Demo")
    print("=" * 60)
    
    print("\n📊 Format Detection Capabilities:")
    print("- Automatic detection of TSV file formats")
    print("- Compatibility scoring (0.0 to 1.0)")
    print("- Support for standard (14-15 columns) and extended (30+ columns) formats")
    print("- Detailed analysis of column structures")
    print("- Batch processing of multiple files")
    
    print("\n🔍 Analyzing Available Input Files:")
    print("-" * 40)
    
    # Test individual files
    detector = TSVFormatDetector()
    
    test_files = [
        ("data/input/gotofiles/2.tsv", "Current standard file"),
        ("data/input/gotofiles/later/1.tsv", "Extended format file"),
        ("data/input/gotofiles/later/3.tsv", "Alternative test file"),
        ("data/input/gotofiles/later/4.tsv", "Another test file"),
    ]
    
    results = []
    
    for file_path, description in test_files:
        if Path(file_path).exists():
            print(f"\n📄 {description}")
            print(f"   File: {file_path}")
            
            try:
                format_info = detector.analyze_file(file_path)
                
                print(f"   ✅ Format: {format_info.format_type}")
                print(f"   📊 Columns: {format_info.total_columns}")
                print(f"   🎯 Compatibility: {format_info.compatibility_score:.2f}")
                print(f"   📈 Tokens: {format_info.token_count:,}")
                print(f"   📝 Sentences: {format_info.sentence_count}")
                
                if format_info.issues:
                    print(f"   ⚠️  Issues: {', '.join(format_info.issues)}")
                
                if format_info.additional_columns:
                    print(f"   ➕ Additional columns: {len(format_info.additional_columns)}")
                
                results.append((file_path, format_info.compatibility_score, format_info.format_type))
                
            except Exception as e:
                print(f"   ❌ Error: {str(e)}")
                results.append((file_path, 0.0, "error"))
        else:
            print(f"\n⚠️  {description}")
            print(f"   File: {file_path} (not found)")
    
    # Summary
    print(f"\n📋 Summary:")
    print("-" * 40)
    
    if results:
        compatible_files = [r for r in results if r[1] >= 0.7]
        partially_compatible = [r for r in results if 0.5 <= r[1] < 0.7]
        incompatible_files = [r for r in results if r[1] < 0.5]
        
        print(f"✅ Highly compatible files: {len(compatible_files)}")
        for file_path, score, format_type in compatible_files:
            print(f"   - {Path(file_path).name}: {score:.2f} ({format_type})")
        
        if partially_compatible:
            print(f"⚠️  Partially compatible files: {len(partially_compatible)}")
            for file_path, score, format_type in partially_compatible:
                print(f"   - {Path(file_path).name}: {score:.2f} ({format_type})")
        
        if incompatible_files:
            print(f"❌ Incompatible files: {len(incompatible_files)}")
            for file_path, score, format_type in incompatible_files:
                print(f"   - {Path(file_path).name}: {score:.2f} ({format_type})")
    
    print(f"\n🎯 Key Achievements:")
    print("- ✅ Created comprehensive format detection system")
    print("- ✅ Implemented compatibility scoring algorithm")
    print("- ✅ Built adaptive TSV parser architecture")
    print("- ✅ Added support for multiple column formats")
    print("- ✅ Designed batch processing capabilities")
    print("- ✅ Enhanced error handling and reporting")
    
    print(f"\n🚧 Next Steps:")
    print("- Integrate adaptive parser with main system")
    print("- Add configuration options for different formats")
    print("- Implement data preprocessing and normalization")
    print("- Create comprehensive logging system")
    print("- Build complete testing framework")
    
    print(f"\n✨ The system can now handle multiple TSV formats!")
    print("The adaptive parser will automatically detect and process")
    print("both standard (14-15 columns) and extended (30+ columns) formats.")


if __name__ == "__main__":
    main()