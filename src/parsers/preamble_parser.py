"""
WebAnno TSV Preamble Parser

Parses WebAnno TSV preambles to determine dynamic column mapping based on annotation schema.
This enables handling different TSV formats with varying column arrangements.
"""

import re
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass


@dataclass
class AnnotationSchema:
    """Represents a parsed WebAnno annotation schema."""
    span_annotations: List[Dict[str, Any]]
    chain_annotations: List[Dict[str, Any]]
    relation_annotations: List[Dict[str, Any]]
    column_mapping: Dict[str, int]
    total_columns: int


class PreambleParser:
    """Parser for WebAnno TSV preambles to extract annotation schema and column mapping."""
    
    def __init__(self):
        self.reset()
    
    def reset(self):
        """Reset parser state."""
        self.schema = None
        self.column_mapping = {}
        self.total_columns = 0
    
    def parse_preamble_lines(self, preamble_lines: List[str]) -> AnnotationSchema:
        """
        Parse preamble lines to extract annotation schema and calculate column positions.
        
        Args:
            preamble_lines: List of preamble lines starting with #
            
        Returns:
            AnnotationSchema with parsed information and column mapping
        """
        schema = {
            'span_annotations': [],
            'chain_annotations': [],
            'relation_annotations': []
        }
        
        # Parse annotation definitions
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
        
        # Calculate column positions
        column_mapping, total_columns = self._calculate_column_positions(schema)
        
        self.schema = AnnotationSchema(
            span_annotations=schema['span_annotations'],
            chain_annotations=schema['chain_annotations'],
            relation_annotations=schema['relation_annotations'],
            column_mapping=column_mapping,
            total_columns=total_columns
        )
        
        return self.schema
    
    def _calculate_column_positions(self, schema: Dict) -> Tuple[Dict[str, int], int]:
        """
        Calculate column positions based on annotation schema.
        
        WebAnno TSV format:
        - Columns 1-3: sentence_id, token_id, token_text
        - Columns 4+: Annotations in order: T_SP, T_CH, T_RL
        
        Args:
            schema: Parsed schema dictionary
            
        Returns:
            Tuple of (column_mapping, total_columns)
        """
        current_column = 4  # Start after basic columns (1-3)
        column_mapping = {}
        
        # Process span annotations (T_SP) first
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
                    if feature:  # Non-empty feature
                        column_mapping[f"{ann_type}|{feature}"] = current_column
                    else:
                        # Empty feature still takes a column
                        column_mapping[f"{ann_type}|_"] = current_column
                    current_column += 1
        
        # Process chain annotations (T_CH) second
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
                    if feature:  # Non-empty feature
                        column_mapping[f"{ann_type}|{feature}"] = current_column
                    else:
                        # Empty feature still takes a column
                        column_mapping[f"{ann_type}|_"] = current_column
                    current_column += 1
        
        # Process relation annotations (T_RL) last
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
                    if feature:  # Non-empty feature
                        column_mapping[f"{ann_type}|{feature}"] = current_column
                    else:
                        # Empty feature still takes a column
                        column_mapping[f"{ann_type}|_"] = current_column
                    current_column += 1
        
        return column_mapping, current_column - 1
    
    def get_coreference_columns(self) -> Dict[str, int]:
        """
        Get column positions for coreference-related annotations.
        
        Returns:
            Dictionary mapping coreference annotation names to column positions
        """
        if not self.schema:
            return {}
        
        coref_columns = {}
        for annotation, column in self.schema.column_mapping.items():
            if 'CoreferenceLink' in annotation or 'coref' in annotation.lower():
                coref_columns[annotation] = column
        
        return coref_columns
    
    def get_morphological_columns(self) -> Dict[str, int]:
        """
        Get column positions for morphological feature annotations.
        
        Returns:
            Dictionary mapping morphological annotation names to column positions
        """
        if not self.schema:
            return {}
        
        morph_columns = {}
        for annotation, column in self.schema.column_mapping.items():
            if 'MorphologicalFeatures' in annotation:
                morph_columns[annotation] = column
        
        return morph_columns
    
    def get_pronoun_type_column(self) -> Optional[int]:
        """
        Get the column position for pronoun type information.
        
        Returns:
            Column number for pronType feature, or None if not found
        """
        if not self.schema:
            return None
        
        # Look for MorphologicalFeatures|pronType
        for annotation, column in self.schema.column_mapping.items():
            if 'MorphologicalFeatures' in annotation and 'pronType' in annotation:
                return column
        
        return None
    
    def get_coreference_link_column(self) -> Optional[int]:
        """
        Get the column position for coreference link information.
        
        Returns:
            Column number for CoreferenceLink|referenceRelation, or None if not found
        """
        if not self.schema:
            return None
        
        # Look for CoreferenceLink|referenceRelation
        for annotation, column in self.schema.column_mapping.items():
            if 'CoreferenceLink' in annotation and 'referenceRelation' in annotation:
                return column
        
        return None
    
    def get_coreference_type_column(self) -> Optional[int]:
        """
        Get the column position for coreference type information.
        
        Returns:
            Column number for CoreferenceLink|referenceType, or None if not found
        """
        if not self.schema:
            return None
        
        # Look for CoreferenceLink|referenceType
        for annotation, column in self.schema.column_mapping.items():
            if 'CoreferenceLink' in annotation and 'referenceType' in annotation:
                return column
        
        return None


def extract_preamble_from_file(file_path: str) -> List[str]:
    """
    Extract preamble lines from a WebAnno TSV file.
    
    Args:
        file_path: Path to the TSV file
        
    Returns:
        List of preamble lines (starting with #)
    """
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
        raise ValueError(f"Error reading preamble from {file_path}: {e}")
    
    return preamble_lines