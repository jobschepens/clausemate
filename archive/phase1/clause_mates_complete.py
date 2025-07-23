#!/usr/bin/env python3
"""
Complete clause mate extraction script with improved program style.
This script identifies critical pronouns and extracts their clause mates for analysis.

PHASE 1 IMPROVEMENTS APPLIED:
- ✅ Constants extracted to config.py
- ✅ Type hints added throughout
- ✅ Proper error handling with custom exceptions
- ✅ Functions broken down and modularized
- ✅ Utility functions separated

OUTPUT FILES:
- clause_mates_chap2_export.csv: Main data export with clause mate relationships
- clause_mates_data_documentation.md: Comprehensive documentation of data structure
- clause_mates_metadata.json: Technical metadata and specifications

DATA STRUCTURE:
Each row represents one clause mate relationship between a critical pronoun and 
one clause mate in the same sentence. Includes:
- 37 columns total
- Pronoun linguistic features (dependent variables)
- Clause mate features (independent variables)  
- Antecedent information (most recent + first in chain)
- Numeric versions of string variables for analysis

CRITICAL PRONOUNS:
- Third person personal: er, sie, es, ihm, ihr, ihn, ihnen
- D-pronouns (pronominal): der, die, das, dem, den, deren, dessen, derer
- Demonstrative: dieser, diese, dieses, diesem, diesen

For detailed documentation, see clause_mates_data_documentation.md
"""

import pandas as pd
import re
import logging
from typing import Dict, List, Optional, Set, Tuple, Any
from collections import defaultdict

# Import our new modules
from config import Constants, TSVColumns, FilePaths
from exceptions import ParseError, FileProcessingError, CoreferenceExtractionError
from utils import (
    validate_file_path, safe_get_column, parse_token_info,
    extract_coreference_id, extract_full_coreference_id, determine_givenness,
    extract_sentence_number, extract_coref_base_and_occurrence, extract_coref_link_numbers
)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def is_critical_pronoun_legacy(coreference_type: str, inanimate_coreference_type: str, token_text: str) -> bool:
    """
    Legacy wrapper for backward compatibility.
    """
    from pronoun_classifier import is_critical_pronoun
    
    token_data = {
        'token_text': token_text,
        'coreference_type': coreference_type,
        'inanimate_coreference_type': inanimate_coreference_type
    }
    return is_critical_pronoun(token_data)

def group_tokens_into_phrases(tokens_data: List[Tuple[str, str, int, str, str, str, str]]) -> List[Dict[str, Any]]:
    """
    Group tokens that belong to the same coreference entity into phrases.
    Uses Phase 2 logic: groups by entity ID rather than consecutive positioning.
    
    Args:
        tokens_data: List of tuples (token_text, coreference_id, token_index, grammatical_role, thematic_role, coreference_type, animacy)
    
    Returns:
        List of phrases, where each phrase is a dict with 'text', 'coreference_id', 'start_idx', 'end_idx', 'grammatical_role', 'thematic_role', 'coreference_type', 'animacy', 'givenness'
    """
    if not tokens_data:
        return []
    
    # Group tokens by entity ID (Phase 2 approach)
    entity_groups: Dict[str, List[Tuple[str, str, int, str, str, str, str]]] = {}
    
    for token_data in tokens_data:
        token_text, coreference_id, token_idx, grammatical_role, thematic_role, coreference_type, animacy = token_data
        if coreference_id is not None:
            if coreference_id not in entity_groups:
                entity_groups[coreference_id] = []
            entity_groups[coreference_id].append(token_data)
    
    # Convert groups to phrases
    phrases = []
    for entity_id, tokens in entity_groups.items():
        if tokens:  # Only create phrases for non-empty groups
            # Sort tokens by position to maintain order
            sorted_tokens = sorted(tokens, key=lambda x: x[2])  # Sort by token_idx
            
            # Build phrase text from sorted tokens
            phrase_text = ' '.join(token[0] for token in sorted_tokens)  # token_text is at index 0
            
            # Use first token's linguistic properties (they should be consistent within entity)
            first_token = sorted_tokens[0]
            token_text, coreference_id, token_idx, grammatical_role, thematic_role, coreference_type, animacy = first_token
            
            phrase = {
                'text': phrase_text,
                'coreference_id': entity_id,
                'start_idx': min(token[2] for token in sorted_tokens),  # token_idx is at index 2
                'end_idx': max(token[2] for token in sorted_tokens),
                'grammatical_role': grammatical_role,
                'thematic_role': thematic_role,
                'coreference_type': coreference_type,
                'animacy': animacy,
                'givenness': determine_givenness(entity_id)
            }
            phrases.append(phrase)
    
    return phrases

def extract_first_words(line: str) -> str:
    """
    Extract the first three words from a sentence text line.
    
    Args:
        line: The #Text= line from TSV file
        
    Returns:
        String with first three words joined by underscores
    """
    if line.startswith('#Text='):
        text_content = line[6:].strip()
        words = text_content.split()[:3]
        return '_'.join(words).replace(',', '').replace('.', '')
    return ''


def extract_clause_mates(file_path: str) -> List[Dict[str, Any]]:
    """
    Extract clause mate relationships from the TSV file.
    
    Args:
        file_path: Path to the TSV file
        
    Returns:
        List of dictionaries, each representing a clause mate relationship
        
    Raises:
        FileProcessingError: If file processing fails
        ParseError: If parsing fails
    """
    
    logger.info("Reading TSV file line by line...")
    # Use line-by-line reading to handle parsing issues
    lines = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                lines.append(line.strip().split('\t'))
    except IOError as e:
        raise FileProcessingError(f"Failed to read file: {file_path}") from e
    
    logger.info(f"Read {len(lines)} lines from file")
    
    # First pass: collect all sentence tokens
    all_sentence_tokens: Dict[int, List[Dict[str, Any]]] = {}
    sentence_first_words: Dict[int, str] = {}  # Store first words for each sentence
    current_sentence_tokens: List[Dict[str, Any]] = []
    current_sentence_id: Optional[int] = None
    current_first_words: Optional[str] = None
    
    logger.info("First pass: collecting all tokens...")
    
    processed_rows = 0
    
    for idx, row in enumerate(lines):
        # Handle #Text= lines to extract first words
        if len(row) == 1 and row[0].startswith('#Text='):
            current_first_words = extract_first_words(row[0])
            continue
            
        # Skip other header lines
        if str(row[0]).startswith('#'):
            continue
            
        # Check for empty lines or lines with just whitespace (sentence boundaries)
        if len(row) <= 1 or not row[0].strip():
            # Store the completed sentence with its first words
            if current_sentence_tokens and current_sentence_id:
                all_sentence_tokens[current_sentence_id] = current_sentence_tokens[:]
                if current_first_words:
                    sentence_first_words[current_sentence_id] = current_first_words
            
            # Reset for next sentence
            current_sentence_tokens = []
            current_sentence_id = None
            current_first_words = None
            continue
        
        # Skip rows that don't have enough columns
        if len(row) < Constants.MIN_COLUMNS_REQUIRED:
            continue
        
        processed_rows += 1
        
        # Extract token information
        try:
            token_info = safe_get_column(row, TSVColumns.TOKEN_ID)
            token_text = safe_get_column(row, TSVColumns.TOKEN_TEXT)
            
            # Extract grammatical and thematic roles
            grammatical_role = safe_get_column(row, TSVColumns.GRAMMATICAL_ROLE)
            thematic_role = safe_get_column(row, TSVColumns.THEMATIC_ROLE)
            
            # Extract coreference information
            coreference_link = safe_get_column(row, TSVColumns.COREFERENCE_LINK)
            coreference_type = safe_get_column(row, TSVColumns.COREFERENCE_TYPE)
            inanimate_coreference_link = safe_get_column(row, TSVColumns.INANIMATE_COREFERENCE_LINK)
            inanimate_coreference_type = safe_get_column(row, TSVColumns.INANIMATE_COREFERENCE_TYPE)
            
            # Extract sentence and token numbers
            sentence_num, token_num = parse_token_info(token_info)
            
            # Set sentence ID based on actual sentence number (use numeric ID)
            current_sentence_id = sentence_num
            
            # Add token to current sentence
            current_sentence_tokens.append({
                'token_idx': token_num,
                'sentence_num': sentence_num,
                'token_text': token_text,
                'grammatical_role': grammatical_role,
                'thematic_role': thematic_role,
                'coreference_link': coreference_link,
                'coreference_type': coreference_type,
                'inanimate_coreference_link': inanimate_coreference_link,
                'inanimate_coreference_type': inanimate_coreference_type,
                'is_critical_pronoun': is_critical_pronoun_legacy(coreference_type, inanimate_coreference_type, token_text)
            })
            
        except (ValueError, IndexError, ParseError) as e:
            logger.warning(f"Skipping malformed row {idx}: {e}")
            continue
    
    # Don't forget the last sentence
    if current_sentence_tokens and current_sentence_id:
        all_sentence_tokens[current_sentence_id] = current_sentence_tokens[:]
        if current_first_words:
            sentence_first_words[current_sentence_id] = current_first_words
    
    logger.info(f"Collected tokens from {len(all_sentence_tokens)} sentences")
    
    # Second pass: process sentences and extract relationships
    logger.info("Second pass: extracting relationships...")
    relationships: List[Dict[str, Any]] = []
    sentence_count = 0
    
    for sentence_id in sorted(all_sentence_tokens.keys()):
        sentence_tokens = all_sentence_tokens[sentence_id]
        sentence_count += 1
        first_words = sentence_first_words.get(sentence_id, "")
        sentence_relationships = process_sentence(sentence_tokens, sentence_id, all_sentence_tokens, first_words)
        relationships.extend(sentence_relationships)
        
        if sentence_count <= 3:
            logger.info(f"Sentence {sentence_count}: {len(sentence_tokens)} tokens, {len(sentence_relationships)} relationships")
    
    logger.info(f"Total sentences processed: {sentence_count}")
    logger.info(f"Total rows processed: {processed_rows}")
    
    return relationships

def process_sentence(sentence_tokens: List[Dict[str, Any]], sentence_id: int, all_sentence_tokens: Optional[Dict[int, List[Dict[str, Any]]]] = None, first_words: str = "") -> List[Dict[str, Any]]:
    """
    Process a single sentence to extract clause mate relationships.
    
    Args:
        sentence_tokens: List of token dictionaries for the sentence
        sentence_id: Numeric identifier for the sentence
        all_sentence_tokens: Dictionary mapping sentence_id to list of tokens (for antecedent calculation)
        first_words: First three words of the sentence joined by underscores
    
    Returns:
        List of clause mate relationship dictionaries
    """
    relationships = []
    
    # Find critical pronouns in the sentence
    critical_pronouns = []
    for token in sentence_tokens:
        if token['is_critical_pronoun']:
            # Extract full coreference IDs for the pronoun from link columns
            pronoun_coref_ids = set()
            
            # Try to get full ID from animate coreference link (column 10)
            animate_full_id = extract_full_coreference_id(token['coreference_link'])
            if animate_full_id is not None:
                pronoun_coref_ids.add(animate_full_id)
            
            # Try to get full ID from inanimate coreference link (column 12)  
            inanimate_full_id = extract_full_coreference_id(token['inanimate_coreference_link'])
            if inanimate_full_id is not None:
                pronoun_coref_ids.add(inanimate_full_id)
            
            # Fallback: if no full IDs found, use base IDs from type columns
            if not pronoun_coref_ids:
                animate_id = extract_coreference_id(token['coreference_type'])
                if animate_id is not None:
                    pronoun_coref_ids.add(animate_id)
                
                inanimate_id = extract_coreference_id(token['inanimate_coreference_type'])
                if inanimate_id is not None:
                    pronoun_coref_ids.add(inanimate_id)
            
            if pronoun_coref_ids:
                critical_pronouns.append({
                    'token': token,
                    'coreference_ids': pronoun_coref_ids
                })
    
    # For each critical pronoun, find its clause mates
    for pronoun_info in critical_pronouns:
        pronoun_token = pronoun_info['token']
        pronoun_coref_ids = pronoun_info['coreference_ids']
        
        # Collect all tokens in the sentence with coreference annotations
        sentence_coref_tokens = []
        for token in sentence_tokens:
            # Try to get full IDs from link columns first
            animate_full_id = extract_full_coreference_id(token['coreference_link'])
            inanimate_full_id = extract_full_coreference_id(token['inanimate_coreference_link'])
            
            # Add tokens with full IDs if available
            if animate_full_id is not None:
                sentence_coref_tokens.append((
                    token['token_text'], 
                    animate_full_id, 
                    token['token_idx'],
                    token['grammatical_role'],
                    token['thematic_role'],
                    token['coreference_type'],
                    'anim'  # Animate coreference layer
                ))
            if inanimate_full_id is not None:
                sentence_coref_tokens.append((
                    token['token_text'], 
                    inanimate_full_id, 
                    token['token_idx'],
                    token['grammatical_role'],
                    token['thematic_role'],
                    token['inanimate_coreference_type'],
                    'inanim'  # Inanimate coreference layer
                ))
            
            # Fallback: use base IDs from type columns if no full IDs found
            if animate_full_id is None and inanimate_full_id is None:
                animate_id = extract_coreference_id(token['coreference_type'])
                inanimate_id = extract_coreference_id(token['inanimate_coreference_type'])
                
                if animate_id is not None:
                    sentence_coref_tokens.append((
                        token['token_text'], 
                        animate_id, 
                        token['token_idx'],
                        token['grammatical_role'],
                        token['thematic_role'],
                        token['coreference_type'],
                        'anim'  # Animate coreference layer
                    ))
                if inanimate_id is not None:
                    sentence_coref_tokens.append((
                        token['token_text'], 
                        inanimate_id, 
                        token['token_idx'],
                        token['grammatical_role'],
                        token['thematic_role'],
                        token['inanimate_coreference_type'],
                        'inanim'  # Inanimate coreference layer
                    ))
        
        # Group tokens into phrases (using Phase 2 entity-based logic)
        phrases = group_tokens_into_phrases(sentence_coref_tokens)
        
        # Calculate number of clause mates for this pronoun
        clause_mate_coref_ids = set()
        for phrase in phrases:
            if phrase['coreference_id'] not in pronoun_coref_ids:
                clause_mate_coref_ids.add(phrase['coreference_id'])
        
        num_clause_mates = len(clause_mate_coref_ids)
        
        # Find clause mates (phrases with different coreference IDs)
        for phrase in phrases:
            if phrase['coreference_id'] not in pronoun_coref_ids:
                # This is a clause mate
                # Determine pronoun givenness from its coreference IDs
                pronoun_givenness = '_'
                if pronoun_coref_ids:
                    # Use the first coreference ID to determine givenness
                    first_coref_id = list(pronoun_coref_ids)[0]
                    pronoun_givenness = determine_givenness(first_coref_id)
                
                # Calculate antecedent distance if all_sentence_tokens is provided
                most_recent_antecedent_text = '_'
                most_recent_antecedent_distance = '_'
                first_antecedent_text = '_'
                first_antecedent_distance = '_'
                antecedent_sentence_id = -1  # Use -1 to indicate no antecedent found
                antecedent_choice = 0
                if all_sentence_tokens:
                    # Calculate antecedent distances and sentence location
                    most_recent_antecedent_text, most_recent_antecedent_distance, first_antecedent_text, first_antecedent_distance, antecedent_sentence_id = find_antecedent_and_distance(
                        pronoun_token, all_sentence_tokens, sentence_id
                    )
                    
                    # Calculate antecedent choice if we found an antecedent
                    if antecedent_sentence_id != -1 and antecedent_sentence_id in all_sentence_tokens:
                        antecedent_choice = calculate_antecedent_choice(
                            pronoun_token, all_sentence_tokens[antecedent_sentence_id], antecedent_sentence_id
                        )
                
                # Extract numeric values from string variables
                sentence_num = sentence_id  # sentence_id is already numeric
                
                # Extract numeric values for pronoun coreference IDs (use first ID if multiple)
                first_pronoun_coref_id = list(pronoun_coref_ids)[0] if pronoun_coref_ids else '_'
                pronoun_coref_base, pronoun_coref_occurrence = extract_coref_base_and_occurrence(first_pronoun_coref_id)
                
                # Extract numeric values for clause mate coreference ID
                clause_mate_coref_base, clause_mate_coref_occurrence = extract_coref_base_and_occurrence(phrase['coreference_id'])
                
                # Extract numeric values for pronoun coreference link
                pronoun_coref_link_base, pronoun_coref_link_occurrence = extract_coref_link_numbers(pronoun_token['coreference_link'])
                
                # Extract numeric values for pronoun inanimate coreference link
                pronoun_inanimate_coref_link_base, pronoun_inanimate_coref_link_occurrence = extract_coref_link_numbers(pronoun_token['inanimate_coreference_link'])
                
                relationship = {
                    'sentence_id': sentence_num,  # Now using numeric sentence ID
                    'sentence_id_numeric': sentence_num,
                    'sentence_id_prefixed': f"sent_{sentence_num}",  # Keep prefixed version for compatibility
                    'sentence_num': sentence_num,
                    'first_words': first_words,
                    'pronoun_text': pronoun_token['token_text'],
                    'pronoun_token_idx': pronoun_token['token_idx'],
                    'pronoun_grammatical_role': pronoun_token['grammatical_role'],
                    'pronoun_thematic_role': pronoun_token['thematic_role'],
                    'pronoun_givenness': pronoun_givenness,
                    'pronoun_coref_ids': list(pronoun_coref_ids),
                    'pronoun_coref_base_num': pronoun_coref_base,
                    'pronoun_coref_occurrence_num': pronoun_coref_occurrence,
                    'pronoun_most_recent_antecedent_text': most_recent_antecedent_text,
                    'pronoun_most_recent_antecedent_distance': most_recent_antecedent_distance,
                    'pronoun_first_antecedent_text': first_antecedent_text,
                    'pronoun_first_antecedent_distance': first_antecedent_distance,
                    'pronoun_antecedent_choice': antecedent_choice,
                    'num_clause_mates': num_clause_mates,
                    'clause_mate_text': phrase['text'],
                    'clause_mate_coref_id': phrase['coreference_id'],
                    'clause_mate_coref_base_num': clause_mate_coref_base,
                    'clause_mate_coref_occurrence_num': clause_mate_coref_occurrence,
                    'clause_mate_start_idx': phrase['start_idx'],
                    'clause_mate_end_idx': phrase['end_idx'],
                    'clause_mate_grammatical_role': phrase['grammatical_role'],
                    'clause_mate_thematic_role': phrase['thematic_role'],
                    'clause_mate_coreference_type': phrase['coreference_type'],
                    'clause_mate_animacy': phrase['animacy'],
                    'clause_mate_givenness': phrase['givenness'],
                    'pronoun_coreference_link': pronoun_token['coreference_link'],
                    'pronoun_coref_link_base_num': pronoun_coref_link_base,
                    'pronoun_coref_link_occurrence_num': pronoun_coref_link_occurrence,
                    'pronoun_coreference_type': pronoun_token['coreference_type'],
                    'pronoun_inanimate_coreference_link': pronoun_token['inanimate_coreference_link'],
                    'pronoun_inanimate_coref_link_base_num': pronoun_inanimate_coref_link_base,
                    'pronoun_inanimate_coref_link_occurrence_num': pronoun_inanimate_coref_link_occurrence,
                    'pronoun_inanimate_coreference_type': pronoun_token['inanimate_coreference_type']
                }
                relationships.append(relationship)
    
    return relationships

def calculate_antecedent_choice(pronoun_token: Dict[str, Any], antecedent_sentence_tokens: List[Dict[str, Any]], antecedent_sentence_id: int) -> int:
    """
    Calculate the number of potential antecedents in the same sentence as the actual antecedent.
    Uses animacy-based matching: count referential expressions that match the pronoun's animacy requirements.
    
    Args:
        pronoun_token: The pronoun token dictionary
        antecedent_sentence_tokens: List of tokens in the sentence where the antecedent is located
        antecedent_sentence_id: The numeric sentence ID where the antecedent is located
    
    Returns:
        int: Number of potential antecedents (including the actual antecedent)
    """
    if not antecedent_sentence_tokens:
        return 0
    
    # Determine pronoun animacy based on which coreference layer it appears in
    pronoun_animacy = None
    
    # Check if pronoun has animate coreference annotation
    if (pronoun_token['coreference_link'] and pronoun_token['coreference_link'] != '_') or \
       (pronoun_token['coreference_type'] and pronoun_token['coreference_type'] != '_'):
        pronoun_animacy = 'anim'
    
    # Check if pronoun has inanimate coreference annotation
    elif (pronoun_token['inanimate_coreference_link'] and pronoun_token['inanimate_coreference_link'] != '_') or \
         (pronoun_token['inanimate_coreference_type'] and pronoun_token['inanimate_coreference_type'] != '_'):
        pronoun_animacy = 'inanim'
    
    if not pronoun_animacy:
        return 0
    
    # Collect all referential expressions in the antecedent's sentence
    sentence_coref_tokens = []
    for token in antecedent_sentence_tokens:
        # Check animate coreference layer
        animate_full_id = extract_full_coreference_id(token['coreference_link'])
        if animate_full_id is not None:
            sentence_coref_tokens.append((
                token['token_text'], 
                animate_full_id, 
                token['token_idx'],
                token['grammatical_role'],
                token['thematic_role'],
                token['coreference_type'],
                'anim'  # Animate coreference layer
            ))
        
        # Check inanimate coreference layer
        inanimate_full_id = extract_full_coreference_id(token['inanimate_coreference_link'])
        if inanimate_full_id is not None:
            sentence_coref_tokens.append((
                token['token_text'], 
                inanimate_full_id, 
                token['token_idx'],
                token['grammatical_role'],
                token['thematic_role'],
                token['inanimate_coreference_type'],
                'inanim'  # Inanimate coreference layer
            ))
        
        # Fallback: use base IDs from type columns if no full IDs found
        if animate_full_id is None and inanimate_full_id is None:
            animate_id = extract_coreference_id(token['coreference_type'])
            if animate_id is not None:
                sentence_coref_tokens.append((
                    token['token_text'], 
                    animate_id, 
                    token['token_idx'],
                    token['grammatical_role'],
                    token['thematic_role'],
                    token['coreference_type'],
                    'anim'  # Animate coreference layer
                ))
            
            inanimate_id = extract_coreference_id(token['inanimate_coreference_type'])
            if inanimate_id is not None:
                sentence_coref_tokens.append((
                    token['token_text'], 
                    inanimate_id, 
                    token['token_idx'],
                    token['grammatical_role'],
                    token['thematic_role'],
                    token['inanimate_coreference_type'],
                    'inanim'  # Inanimate coreference layer
                ))
    
    # Group tokens into phrases
    phrases = group_tokens_into_phrases(sentence_coref_tokens)
    
    # Count phrases that match the pronoun's animacy
    compatible_antecedents = 0
    for phrase in phrases:
        if phrase['animacy'] == pronoun_animacy:
            compatible_antecedents += 1
    
    return compatible_antecedents

def extract_sentence_number(sentence_id: str) -> Optional[int]:
    """Extract numeric sentence number from sentence_id string like 'sent_34'."""
    if not sentence_id or sentence_id == '_':
        return None
    try:
        return int(sentence_id.replace('sent_', ''))
    except (ValueError, AttributeError):
        return None

def extract_coref_base_and_occurrence(coref_id: str) -> Tuple[Optional[int], Optional[int]]:
    """
    Extract base chain number and occurrence number from coreference ID.
    
    Args:
        coref_id: String like "115-4" or just "115"
    
    Returns:
        tuple: (base_number, occurrence_number) or (None, None) if parsing fails
    """
    if not coref_id or coref_id == '_':
        return None, None
    
    try:
        coref_str = str(coref_id)
        if '-' in coref_str:
            parts = coref_str.split('-')
            base_num = int(parts[0])
            occurrence_num = int(parts[1])
            return base_num, occurrence_num
        else:
            # Just base number, no occurrence
            return int(coref_str), None
    except (ValueError, IndexError, AttributeError):
        return None, None

def extract_coref_link_numbers(
    coref_link: str
) -> Tuple[Optional[int], Optional[int]]:
    """
    Extract base chain number and occurrence number from coreference link.
    
    Args:
        coref_link: String like "*->115-4" or "*->115"
    
    Returns:
        tuple: (base_number, occurrence_number) or (None, None) if parsing fails
    """
    if not coref_link or coref_link == '_':
        return None, None
    
    try:
        # Extract the target part after "->"
        if '->' in coref_link:
            target = coref_link.split('->')[-1]
            return extract_coref_base_and_occurrence(target)
        else:
            return None, None
    except (ValueError, AttributeError):
        return None, None

def find_antecedent_and_distance(pronoun_token: Dict[str, Any], all_sentence_tokens: Dict[int, List[Dict[str, Any]]], current_sentence_id: int) -> Tuple[str, str, str, str, int]:
    """
    Find both the most recent and first antecedent phrases of a pronoun and calculate the linear distances to them.
    
    Args:
        pronoun_token: The pronoun token dictionary
        all_sentence_tokens: Dictionary mapping sentence_id to list of tokens in that sentence
        current_sentence_id: The sentence ID where the pronoun appears
    
    Returns:
        tuple: (most_recent_antecedent_text, most_recent_distance, first_antecedent_text, first_distance, antecedent_sentence_id)
    """
    # Extract the pronoun's coreference chain base number (e.g., "115" from "115-4")
    pronoun_coref_ids = set()
    
    # Get full coreference IDs from link columns
    animate_full_id = extract_full_coreference_id(pronoun_token['coreference_link'])
    if animate_full_id:
        pronoun_coref_ids.add(animate_full_id)
    
    inanimate_full_id = extract_full_coreference_id(pronoun_token['inanimate_coreference_link'])
    if inanimate_full_id:
        pronoun_coref_ids.add(inanimate_full_id)
    
    if not pronoun_coref_ids:
        return Constants.MISSING_VALUE, Constants.MISSING_VALUE, Constants.MISSING_VALUE, Constants.MISSING_VALUE, -1
    
    # Get the base chain number (e.g., "115" from "115-4")
    chain_numbers = set()
    for coref_id in pronoun_coref_ids:
        if '-' in str(coref_id):
            base_num = str(coref_id).split('-', maxsplit=1)[0]
            chain_numbers.add(base_num)
        else:
            chain_numbers.add(str(coref_id))
    
    if not chain_numbers:
        return Constants.MISSING_VALUE, Constants.MISSING_VALUE, Constants.MISSING_VALUE, Constants.MISSING_VALUE, -1
    
    # Calculate the absolute position of the current pronoun
    current_sentence_num = current_sentence_id  # sentence_id is already numeric
    pronoun_absolute_pos = 0
    
    # Count tokens in all sentences before the current sentence
    for sent_id in sorted(all_sentence_tokens.keys()):
        sent_num = sent_id  # sent_id is already numeric
        if sent_num < current_sentence_num:
            pronoun_absolute_pos += len(all_sentence_tokens[sent_id])
        elif sent_num == current_sentence_num:
            # Add tokens before the pronoun in the current sentence
            pronoun_absolute_pos += pronoun_token['token_idx'] - 1  # -1 because token_idx is 1-based
            break
    
    # Find all antecedent phrases in the same coreference chain(s) that appear before this pronoun
    potential_antecedent_phrases = []
    
    # Look through all sentences up to and including the current one
    for sent_id in sorted(all_sentence_tokens.keys()):
        sent_num = sent_id  # sent_id is already numeric
        if sent_num > current_sentence_num:
            break
        
        # Skip tokens that come after the pronoun in the same sentence
        sentence_tokens = all_sentence_tokens[sent_id]
        if sent_num == current_sentence_num:
            # Only consider tokens before the pronoun
            sentence_tokens = [t for t in sentence_tokens if t['token_idx'] < pronoun_token['token_idx']]
        
        # Collect tokens with coreference annotations in this sentence
        sentence_coref_tokens = []
        for token in sentence_tokens:
            # Try to get full IDs from link columns
            animate_full_id = extract_full_coreference_id(token['coreference_link'])
            inanimate_full_id = extract_full_coreference_id(token['inanimate_coreference_link'])
            
            # Add tokens with full IDs if available
            if animate_full_id is not None:
                sentence_coref_tokens.append((
                    token['token_text'], 
                    animate_full_id, 
                    token['token_idx'],
                    token['grammatical_role'],
                    token['thematic_role'],
                    token['coreference_type'],
                    Constants.ANIMATE_LAYER
                ))
            if inanimate_full_id is not None:
                sentence_coref_tokens.append((
                    token['token_text'], 
                    inanimate_full_id, 
                    token['token_idx'],
                    token['grammatical_role'],
                    token['thematic_role'],
                    token['inanimate_coreference_type'],
                    Constants.INANIMATE_LAYER
                ))
            
            # Fallback: use base IDs from type columns if no full IDs found
            if animate_full_id is None and inanimate_full_id is None:
                animate_id = extract_coreference_id(token['coreference_type'])
                inanimate_id = extract_coreference_id(token['inanimate_coreference_type'])
                
                if animate_id is not None:
                    sentence_coref_tokens.append((
                        token['token_text'], 
                        animate_id, 
                        token['token_idx'],
                        token['grammatical_role'],
                        token['thematic_role'],
                        token['coreference_type'],
                        Constants.ANIMATE_LAYER
                    ))
                if inanimate_id is not None:
                    sentence_coref_tokens.append((
                        token['token_text'], 
                        inanimate_id, 
                        token['token_idx'],
                        token['grammatical_role'],
                        token['thematic_role'],
                        token['inanimate_coreference_type'],
                        Constants.INANIMATE_LAYER
                    ))
        
        # Group tokens into phrases
        phrases = group_tokens_into_phrases(sentence_coref_tokens)
        
        # Check which phrases are in the same coreference chain as our pronoun
        for phrase in phrases:
            phrase_chain_nums = set()
            occurrence_num = None
            
            # Extract chain number from phrase coreference ID
            if '-' in str(phrase['coreference_id']):
                base_num = str(phrase['coreference_id']).split('-', maxsplit=1)[0]
                phrase_chain_nums.add(base_num)
                occurrence_num = int(str(phrase['coreference_id']).split('-', maxsplit=1)[1])
            else:
                phrase_chain_nums.add(str(phrase['coreference_id']))
                occurrence_num = 999  # Default high number if no occurrence
            
            # If this phrase shares a chain number with our pronoun, it's a potential antecedent
            if phrase_chain_nums.intersection(chain_numbers):
                # Calculate absolute position for the phrase (use the first token's position)
                absolute_pos = 0
                # Count tokens in all sentences before this one
                for prev_sent_id in sorted(all_sentence_tokens.keys()):
                    prev_sent_num = prev_sent_id  # prev_sent_id is already numeric
                    if prev_sent_num < sent_num:
                        absolute_pos += len(all_sentence_tokens[prev_sent_id])
                    else:
                        break
                
                phrase_absolute_pos = absolute_pos + phrase['start_idx'] - 1  # -1 because token_idx is 1-based
                distance = pronoun_absolute_pos - phrase_absolute_pos
                
                potential_antecedent_phrases.append({
                    'phrase': phrase,
                    'absolute_pos': phrase_absolute_pos,
                    'distance': distance,
                    'sentence_id': sent_id,
                    'occurrence_num': occurrence_num
                })
    
    # Find both the most recent and first antecedent phrases
    if potential_antecedent_phrases:
        # Sort by absolute position for most recent (highest position = most recent)
        most_recent_antecedent = max(potential_antecedent_phrases, key=lambda x: x['absolute_pos'])
        
        # Sort by occurrence number for first mention (lowest occurrence number = first)
        first_antecedent = min(potential_antecedent_phrases, key=lambda x: x['occurrence_num'])
        
        return (most_recent_antecedent['phrase']['text'], str(most_recent_antecedent['distance']),
                first_antecedent['phrase']['text'], str(first_antecedent['distance']),
                most_recent_antecedent['sentence_id'])
    
    return Constants.MISSING_VALUE, Constants.MISSING_VALUE, Constants.MISSING_VALUE, Constants.MISSING_VALUE, -1

def main() -> Optional[pd.DataFrame]:
    """Main function to run the clause mate extraction."""
    
    # Use the configuration file path
    file_path = FilePaths.INPUT_FILE
    
    logger.info(f"Starting clause mate extraction from: {file_path}")
    
    try:
        # Validate file path
        validate_file_path(file_path)
        
        relationships = extract_clause_mates(file_path)
        
        logger.info(f"Extracted {len(relationships)} clause mate relationships")
        
        if relationships:
            logger.info("First 5 relationships:")
            for i, rel in enumerate(relationships[:5]):
                logger.info(f"{i+1}. Sentence: {rel['sentence_id']}")
                logger.info(f"   Pronoun: '{rel['pronoun_text']}' (idx: {rel['pronoun_token_idx']})")
                logger.info(f"   Clause mate: '{rel['clause_mate_text']}' (idx: {rel['clause_mate_start_idx']}-{rel['clause_mate_end_idx']})")
                logger.info(f"   Pronoun coref IDs: {rel['pronoun_coref_ids']}")
                logger.info(f"   Clause mate coref ID: {rel['clause_mate_coref_id']}")
        
        # Convert to DataFrame for analysis
        df_relationships = pd.DataFrame(relationships)
        
        if not df_relationships.empty:
            logger.info(f"DataFrame shape: {df_relationships.shape}")
            logger.info(f"Columns: {list(df_relationships.columns)}")
            
            # Show some statistics
            logger.info(f"Unique pronouns: {df_relationships['pronoun_text'].nunique()}")
            logger.info(f"Unique clause mates: {df_relationships['clause_mate_text'].nunique()}")
            logger.info(f"Unique sentences: {df_relationships['sentence_id'].nunique()}")
            
            # Export to CSV
            output_file = FilePaths.OUTPUT_FILE
            df_relationships.to_csv(output_file, index=False, encoding='utf-8')
            logger.info(f"Results exported to: {output_file}")
            
            return df_relationships
        else:
            logger.warning("No relationships found!")
            return None
            
    except FileNotFoundError as e:
        logger.error(f"File not found: {e}")
        return None
    except (ParseError, FileProcessingError) as e:
        logger.error(f"Processing error: {e}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error during processing: {e}")
        import traceback
        traceback.print_exc()
        return None

# Run the extraction
if __name__ == "__main__":
    result_df = main()
