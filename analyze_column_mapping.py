#!/usr/bin/env python3
"""
Script to analyze WebAnno TSV column mapping based on preambles.
"""

import os
from pathlib import Path

def extract_preamble(file_path):
    """Extract preamble lines from a TSV file."""
    preamble_lines = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line.startswith('#'):
                    preamble_lines.append(line)
                elif line == '':
                    continue
                else:
                    # First non-comment, non-empty line - stop reading preamble
                    break
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return []
    
    return preamble_lines

def parse_annotation_schema(preamble_lines):
    """Parse the annotation schema from preamble lines."""
    schema = {
        'span_annotations': [],  # T_SP
        'chain_annotations': [], # T_CH  
        'relation_annotations': [] # T_RL
    }
    
    for line in preamble_lines:
        if line.startswith('#T_SP='):
            # Span annotation: #T_SP=type|feature1|feature2|...
            parts = line[6:].split('|')  # Remove '#T_SP='
            annotation_type = parts[0]
            features = parts[1:] if len(parts) > 1 else []
            schema['span_annotations'].append({
                'type': annotation_type,
                'features': features
            })
        elif line.startswith('#T_CH='):
            # Chain annotation: #T_CH=type|feature1|feature2|...
            parts = line[6:].split('|')  # Remove '#T_CH='
            annotation_type = parts[0]
            features = parts[1:] if len(parts) > 1 else []
            schema['chain_annotations'].append({
                'type': annotation_type,
                'features': features
            })
        elif line.startswith('#T_RL='):
            # Relation annotation: #T_RL=type|feature1|feature2|...
            parts = line[6:].split('|')  # Remove '#T_RL='
            annotation_type = parts[0]
            features = parts[1:] if len(parts) > 1 else []
            schema['relation_annotations'].append({
                'type': annotation_type,
                'features': features
            })
    
    return schema

def calculate_column_positions(schema):
    """Calculate column positions based on annotation schema."""
    # WebAnno TSV format:
    # Columns 1-3: sentence_id, token_id, token_text
    current_column = 4  # Start after basic columns
    column_mapping = {}
    
    # Process span annotations (T_SP)
    for span_ann in schema['span_annotations']:
        ann_type = span_ann['type']
        features = span_ann['features']
        
        if not features:
            # Single column for annotation without features
            column_mapping[ann_type] = current_column
            current_column += 1
        else:
            # Multiple columns for features
            for feature in features:
                if feature:  # Skip empty features
                    column_mapping[f"{ann_type}|{feature}"] = current_column
                    current_column += 1
                else:
                    # Empty feature still takes a column
                    column_mapping[f"{ann_type}|_"] = current_column
                    current_column += 1
    
    # Process chain annotations (T_CH)
    for chain_ann in schema['chain_annotations']:
        ann_type = chain_ann['type']
        features = chain_ann['features']
        
        if not features:
            # Single column for annotation without features
            column_mapping[ann_type] = current_column
            current_column += 1
        else:
            # Multiple columns for features
            for feature in features:
                if feature:  # Skip empty features
                    column_mapping[f"{ann_type}|{feature}"] = current_column
                    current_column += 1
    
    # Process relation annotations (T_RL)
    for rel_ann in schema['relation_annotations']:
        ann_type = rel_ann['type']
        features = rel_ann['features']
        
        if not features:
            # Single column for annotation without features
            column_mapping[ann_type] = current_column
            current_column += 1
        else:
            # Multiple columns for features
            for feature in features:
                if feature:  # Skip empty features
                    column_mapping[f"{ann_type}|{feature}"] = current_column
                    current_column += 1
    
    return column_mapping, current_column - 1  # Total columns

def analyze_file_detailed(file_path):
    """Analyze a single TSV file's column mapping in detail."""
    print(f"\n=== Detailed Analysis of {file_path} ===")
    
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return None
    
    preamble = extract_preamble(file_path)
    schema = parse_annotation_schema(preamble)
    column_mapping, total_columns = calculate_column_positions(schema)
    
    print(f"Total columns: {total_columns}")
    print(f"Schema summary:")
    print(f"  - Span annotations: {len(schema['span_annotations'])}")
    print(f"  - Chain annotations: {len(schema['chain_annotations'])}")
    print(f"  - Relation annotations: {len(schema['relation_annotations'])}")
    
    print(f"\nColumn mapping:")
    print("  Basic columns:")
    print("    1: sentence_id")
    print("    2: token_id") 
    print("    3: token_text")
    
    print("  Annotation columns:")
    for annotation, column in sorted(column_mapping.items(), key=lambda x: x[1]):
        print(f"    {column}: {annotation}")
    
    # Look for coreference-related columns
    print(f"\nCoreference-related columns:")
    coref_columns = {}
    for annotation, column in column_mapping.items():
        if 'CoreferenceLink' in annotation or 'coref' in annotation.lower():
            coref_columns[annotation] = column
            print(f"    {column}: {annotation}")
    
    # Look for morphological features (pronType)
    print(f"\nMorphological feature columns:")
    morph_columns = {}
    for annotation, column in column_mapping.items():
        if 'MorphologicalFeatures' in annotation:
            morph_columns[annotation] = column
            print(f"    {column}: {annotation}")
    
    return {
        'schema': schema,
        'column_mapping': column_mapping,
        'total_columns': total_columns,
        'coref_columns': coref_columns,
        'morph_columns': morph_columns
    }

def main():
    """Main analysis function."""
    files_to_analyze = [
        'data/input/gotofiles/2.tsv',
        'data/input/gotofiles/later/1.tsv',
        'data/input/gotofiles/later/3.tsv',
        'data/input/gotofiles/later/4.tsv'
    ]
    
    print("WebAnno TSV Column Mapping Analysis")
    print("=" * 60)
    
    results = {}
    for file_path in files_to_analyze:
        result = analyze_file_detailed(file_path)
        if result:
            results[file_path] = result
    
    # Compare files
    print(f"\n{'=' * 60}")
    print("COMPARISON SUMMARY")
    print("=" * 60)
    
    for file_path, result in results.items():
        filename = os.path.basename(file_path)
        print(f"\n{filename}:")
        print(f"  Total columns: {result['total_columns']}")
        print(f"  Coreference columns: {len(result['coref_columns'])}")
        print(f"  Morphological columns: {len(result['morph_columns'])}")
        
        # Show coreference column positions
        if result['coref_columns']:
            print(f"  Coreference positions:")
            for annotation, column in result['coref_columns'].items():
                print(f"    Column {column}: {annotation}")
        
        # Show morphological column positions  
        if result['morph_columns']:
            print(f"  Morphological positions:")
            for annotation, column in result['morph_columns'].items():
                print(f"    Column {column}: {annotation}")

if __name__ == '__main__':
    main()