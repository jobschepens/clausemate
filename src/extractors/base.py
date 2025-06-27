"""
Base interfaces for extraction components.

This module defines abstract base classes for different types of extraction
operations, ensuring consistent behavior and easy extensibility.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Iterator, Optional, Set, Any
from ..data.models import (
    Token, SentenceContext, CoreferenceChain, 
    ClauseMateRelationship, ExtractionResult
)


class BaseExtractor(ABC):
    """
    Abstract base class for all extraction operations.
    
    This interface establishes the contract for extracting linguistic features
    from parsed text data.
    """
    
    @abstractmethod
    def extract(self, context: SentenceContext) -> ExtractionResult:
        """
        Extract features from a sentence context.
        
        Args:
            context: The sentence context to analyze
            
        Returns:
            ExtractionResult containing extracted features
            
        Raises:
            ExtractionError: If extraction fails
        """
        pass
    
    @abstractmethod
    def can_extract(self, context: SentenceContext) -> bool:
        """
        Check if this extractor can process the given context.
        
        Args:
            context: The sentence context to check
            
        Returns:
            True if extractor can process this context
        """
        pass


class BaseCoreferenceExtractor(BaseExtractor):
    """
    Abstract base class for coreference extraction.
    
    Handles identification and linking of coreferential expressions.
    """
    
    @abstractmethod
    def extract_coreference_chains(
        self, 
        contexts: List[SentenceContext]
    ) -> List[CoreferenceChain]:
        """
        Extract coreference chains from multiple sentences.
        
        Args:
            contexts: List of sentence contexts to analyze
            
        Returns:
            List of identified coreference chains
        """
        pass
    
    @abstractmethod
    def find_mentions(self, context: SentenceContext) -> List[Token]:
        """
        Find all mentions in a sentence that could participate in coreference.
        
        Args:
            context: The sentence context to search
            
        Returns:
            List of tokens that are potential mentions
        """
        pass
    
    @abstractmethod
    def link_mentions(
        self, 
        mentions: List[Token], 
        existing_chains: List[CoreferenceChain]
    ) -> List[CoreferenceChain]:
        """
        Link new mentions to existing coreference chains.
        
        Args:
            mentions: New mentions to link
            existing_chains: Existing coreference chains
            
        Returns:
            Updated list of coreference chains
        """
        pass


class BasePronounExtractor(BaseExtractor):
    """
    Abstract base class for pronoun extraction and classification.
    
    Handles identification of pronouns and their linguistic properties.
    """
    
    @abstractmethod
    def extract_pronouns(self, context: SentenceContext) -> List[Token]:
        """
        Extract all pronouns from a sentence context.
        
        Args:
            context: The sentence context to search
            
        Returns:
            List of pronoun tokens
        """
        pass
    
    @abstractmethod
    def classify_pronoun(self, pronoun: Token, context: SentenceContext) -> Dict[str, str]:
        """
        Classify a pronoun's linguistic properties.
        
        Args:
            pronoun: The pronoun token to classify
            context: The sentence context
            
        Returns:
            Dictionary of pronoun properties (person, gender, etc.)
        """
        pass
    
    @abstractmethod
    def is_pronoun(self, token: Token) -> bool:
        """
        Check if a token is a pronoun.
        
        Args:
            token: Token to check
            
        Returns:
            True if token is a pronoun
        """
        pass


class BaseClauseMateExtractor(BaseExtractor):
    """
    Abstract base class for clause mate extraction.
    
    Handles identification of clause mate relationships between linguistic elements.
    """
    
    @abstractmethod
    def extract_clause_mates(
        self, 
        context: SentenceContext
    ) -> List[ClauseMateRelationship]:
        """
        Extract clause mate relationships from a sentence.
        
        Args:
            context: The sentence context to analyze
            
        Returns:
            List of clause mate relationships
        """
        pass
    
    @abstractmethod
    def find_clause_boundaries(self, context: SentenceContext) -> List[int]:
        """
        Identify clause boundaries in a sentence.
        
        Args:
            context: The sentence context to analyze
            
        Returns:
            List of token indices marking clause boundaries
        """
        pass
    
    @abstractmethod
    def group_tokens_by_clause(
        self, 
        context: SentenceContext
    ) -> Dict[int, List[Token]]:
        """
        Group tokens by their clause membership.
        
        Args:
            context: The sentence context to analyze
            
        Returns:
            Dictionary mapping clause IDs to token lists
        """
        pass


class BaseFeatureExtractor(BaseExtractor):
    """
    Abstract base class for linguistic feature extraction.
    
    Handles extraction of various linguistic features from tokens and contexts.
    """
    
    @abstractmethod
    def extract_features(
        self, 
        token: Token, 
        context: SentenceContext
    ) -> Dict[str, Any]:
        """
        Extract linguistic features from a token in context.
        
        Args:
            token: The token to analyze
            context: The sentence context
            
        Returns:
            Dictionary of extracted features
        """
        pass
    
    @abstractmethod
    def get_supported_features(self) -> Set[str]:
        """
        Get the set of features this extractor can provide.
        
        Returns:
            Set of feature names this extractor supports
        """
        pass
