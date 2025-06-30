"""
Relationship extractor implementation.

This module provides concrete implementations for extracting clause mate
relationships between critical pronouns and their clause mates within sentences.
"""

from typing import List, Dict, Any, Set, Optional
import sys
from pathlib import Path

# Add the parent directory to the path to import from root
sys.path.append(str(Path(__file__).parent.parent.parent))

from src.extractors.base import BaseRelationshipExtractor
from src.data.models import (
    Token, SentenceContext, ExtractionResult, CoreferencePhrase,
    ClauseMateRelationship, Phrase, AntecedentInfo
)
from utils import extract_coreference_id, extract_full_coreference_id, determine_givenness


class RelationshipExtractor(BaseRelationshipExtractor):
    """
    Concrete implementation for extracting clause mate relationships.
    
    This extractor identifies relationships between critical pronouns and
    their clause mates within the same sentence.
    """
    
    def __init__(self):
        """Initialize the relationship extractor."""
        pass
    
    def extract(self, context: SentenceContext) -> ExtractionResult:
        """
        Extract relationship features from a sentence context.
        
        Args:
            context: The sentence context to analyze
            
        Returns:
            ExtractionResult containing relationship information
        """
        relationships = self.extract_relationships(context)
        
        return ExtractionResult(
            pronouns=context.critical_pronouns,
            phrases=context.coreference_phrases,
            relationships=relationships,
            coreference_chains=[],  # Already handled by coreference extractor
            features={
                'relationship_count': len(relationships),
                'pronouns_with_clause_mates': len(set(rel.pronoun.idx for rel in relationships))
            }
        )
    
    def can_extract(self, context: SentenceContext) -> bool:
        """
        Check if this extractor can process the given context.
        
        Args:
            context: The sentence context to check
            
        Returns:
            True if extractor can process this context
        """
        # Can extract if we have critical pronouns and coreference phrases
        return (
            len(context.critical_pronouns) > 0 and 
            len(context.coreference_phrases) > 0
        )
    
    def extract_relationships(self, context: SentenceContext) -> List[ClauseMateRelationship]:
        """
        Extract all clause mate relationships from a sentence context.
        
        Args:
            context: The sentence context to analyze
            
        Returns:
            List of clause mate relationships
        """
        relationships = []
        
        # For each critical pronoun, find its clause mates
        for pronoun in context.critical_pronouns:
            pronoun_coref_ids = self._get_pronoun_coreference_ids(pronoun)
            
            if not pronoun_coref_ids:
                continue  # Skip pronouns without coreference information
            
            # Find clause mates (phrases with different coreference IDs)
            clause_mates = []
            for phrase in context.coreference_phrases:
                if phrase.entity_id not in pronoun_coref_ids:
                    clause_mates.append(phrase)
            
            num_clause_mates = len(clause_mates)
            
            # Create relationship for each clause mate
            for clause_mate in clause_mates:
                # Convert CoreferencePhrase to Phrase for compatibility
                phrase = self._convert_to_phrase(clause_mate)
                
                # Create antecedent info (placeholder for now)
                antecedent_info = AntecedentInfo(
                    most_recent_text='_',
                    most_recent_distance='_',
                    first_text='_',
                    first_distance='_',
                    sentence_id='_',
                    choice_count=0
                )
                
                relationship = ClauseMateRelationship(
                    sentence_id=str(context.sentence_num),
                    sentence_num=context.sentence_num,
                    pronoun=pronoun,
                    clause_mate=phrase,
                    num_clause_mates=num_clause_mates,
                    antecedent_info=antecedent_info,
                    first_words=getattr(context, 'first_words', "")
                )
                
                relationships.append(relationship)
        
        return relationships
    
    def find_clause_mates(
        self, 
        pronoun: Token, 
        context: SentenceContext
    ) -> List[CoreferencePhrase]:
        """
        Find all clause mates for a given pronoun in a sentence.
        
        Args:
            pronoun: The pronoun to find clause mates for
            context: The sentence context
            
        Returns:
            List of clause mate phrases
        """
        pronoun_coref_ids = self._get_pronoun_coreference_ids(pronoun)
        
        clause_mates = []
        for phrase in context.coreference_phrases:
            if phrase.entity_id not in pronoun_coref_ids:
                clause_mates.append(phrase)
        
        return clause_mates
    
    def validate_relationship(self, relationship: ClauseMateRelationship) -> bool:
        """
        Validate that a relationship is well-formed.
        
        Args:
            relationship: The relationship to validate
            
        Returns:
            True if the relationship is valid
        """
        # Basic validation checks
        if not relationship.pronoun.is_critical_pronoun:
            return False
        
        if relationship.num_clause_mates < 1:
            return False
        
        if not relationship.sentence_id:
            return False
        
        if relationship.sentence_num < 1:
            return False
        
        return True
    
    def _get_pronoun_coreference_ids(self, pronoun: Token) -> Set[str]:
        """
        Get all coreference IDs for a pronoun.
        
        Args:
            pronoun: The pronoun token
            
        Returns:
            Set of coreference IDs
        """
        ids = set()
        
        # Try to get full ID from animate coreference link
        if pronoun.coreference_link and pronoun.coreference_link != '_':
            full_id = extract_full_coreference_id(pronoun.coreference_link)
            if full_id:
                ids.add(full_id)
        
        # Try to get full ID from inanimate coreference link
        if pronoun.inanimate_coreference_link and pronoun.inanimate_coreference_link != '_':
            full_id = extract_full_coreference_id(pronoun.inanimate_coreference_link)
            if full_id:
                ids.add(full_id)
        
        # Fallback: get base IDs from type columns
        if not ids:
            if pronoun.coreference_type and pronoun.coreference_type != '_':
                base_id = extract_coreference_id(pronoun.coreference_type)
                if base_id:
                    ids.add(base_id)
            
            if pronoun.inanimate_coreference_type and pronoun.inanimate_coreference_type != '_':
                base_id = extract_coreference_id(pronoun.inanimate_coreference_type)
                if base_id:
                    ids.add(base_id)
        
        return ids
    
    def _convert_to_phrase(self, coreference_phrase: CoreferencePhrase) -> Phrase:
        """
        Convert a CoreferencePhrase to a Phrase for compatibility.
        
        Args:
            coreference_phrase: The coreference phrase to convert
            
        Returns:
            Converted Phrase object
        """
        # Determine givenness from entity ID
        givenness = determine_givenness(coreference_phrase.entity_id)
        
        # Use head token for grammatical/thematic roles
        head_token = coreference_phrase.get_head_token()
        
        return Phrase(
            text=coreference_phrase.phrase_text,
            coreference_id=coreference_phrase.entity_id,
            start_idx=coreference_phrase.start_position,
            end_idx=coreference_phrase.end_position,
            grammatical_role=head_token.grammatical_role,
            thematic_role=head_token.thematic_role,
            coreference_type=head_token.coreference_type or head_token.inanimate_coreference_type or '_',
            animacy=self._determine_animacy(head_token),
            givenness=givenness
        )
    
    def _determine_animacy(self, token: Token) -> Any:
        """
        Determine animacy type from token coreference information.
        
        Args:
            token: The token to examine
            
        Returns:
            AnimacyType enum value
        """
        from src.data.models import AnimacyType
        
        # Check if token has animate coreference annotation
        if (token.coreference_link and token.coreference_link != '_') or \
           (token.coreference_type and token.coreference_type != '_'):
            return AnimacyType.ANIMATE
        
        # Check if token has inanimate coreference annotation
        elif (token.inanimate_coreference_link and token.inanimate_coreference_link != '_') or \
             (token.inanimate_coreference_type and token.inanimate_coreference_type != '_'):
            return AnimacyType.INANIMATE
        
        # Default to animate if uncertain
        return AnimacyType.ANIMATE
