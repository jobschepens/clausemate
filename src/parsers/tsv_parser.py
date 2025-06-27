"""
TSV parser implementation for clause mates data.

This module provides a concrete implementation of the BaseParser interface
specifically for parsing TSV files with linguistic annotations.
"""

import csv
from typing import Dict, List, Iterator
from pathlib import Path

from .base import BaseParser, BaseTokenProcessor
from ..data.models import Token, SentenceContext
import sys
from pathlib import Path

# Add the parent directory to the path to import from root
sys.path.append(str(Path(__file__).parent.parent.parent))

from exceptions import FileProcessingError, ParseError


class TSVParser(BaseParser):
    """
    Concrete implementation of BaseParser for TSV files.
    
    Handles parsing of tab-separated value files containing linguistic annotations
    with the expected column structure for clause mate analysis.
    """
    
    def __init__(self, processor: BaseTokenProcessor):
        """
        Initialize the TSV parser.
        
        Args:
            processor: Token processor for validation and enrichment
        """
        self.processor = processor
        self._expected_columns = 14  # Updated based on actual TSV structure
        
        # Import column mappings from config
        sys.path.append(str(Path(__file__).parent.parent.parent))
        from config import TSVColumns
        self.columns = TSVColumns()
    
    def parse_file(self, file_path: str) -> Dict[str, List[Token]]:
        """
        Parse a TSV file and return all sentences with their tokens.
        
        Args:
            file_path: Path to the TSV file to parse
            
        Returns:
            Dictionary mapping sentence IDs to lists of tokens
            
        Raises:
            FileProcessingError: If file cannot be read
            ParseError: If file format is invalid
        """
        sentences = {}
        
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                for sentence_context in self.parse_sentence_streaming(file_path):
                    sentences[sentence_context.sentence_id] = sentence_context.tokens
        except FileNotFoundError:
            raise FileProcessingError(f"File not found: {file_path}")
        except PermissionError:
            raise FileProcessingError(f"Permission denied: {file_path}")
        except Exception as e:
            raise FileProcessingError(f"Error reading file {file_path}: {str(e)}")
        
        return sentences
    
    def parse_sentence_streaming(self, file_path: str) -> Iterator[SentenceContext]:
        """
        Parse a TSV file sentence by sentence for memory efficiency.
        
        Args:
            file_path: Path to the TSV file to parse
            
        Yields:
            SentenceContext objects for each sentence
            
        Raises:
            FileProcessingError: If file cannot be processed
            ParseError: If file format is invalid
        """
        current_tokens = []
        current_sentence_id = None
        current_sentence_num = None
        
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                reader = csv.reader(file, delimiter='\t')
                
                for line_num, row in enumerate(reader, 1):
                    try:
                        # Skip empty lines and comments
                        if not row or (len(row) == 1 and not row[0].strip()):
                            continue
                        
                        # Check for sentence boundary
                        line_text = '\t'.join(row)
                        if self.is_sentence_boundary(line_text):
                            # Yield previous sentence if we have tokens
                            if current_tokens and current_sentence_id:
                                yield self._create_sentence_context(
                                    current_sentence_id, 
                                    current_sentence_num or 1, 
                                    current_tokens
                                )
                            
                            # Start new sentence
                            current_tokens = []
                            current_sentence_id = self._extract_sentence_id(line_text)
                            current_sentence_num = self._extract_sentence_num(line_text)
                            continue
                        
                        # Parse token line
                        if len(row) < self._expected_columns:
                            raise ParseError(
                                f"Line {line_num}: Expected {self._expected_columns} columns, "
                                f"got {len(row)}"
                            )
                        
                        token = self.parse_token_line(line_text)
                        
                        # Validate and enrich token if we have a sentence context
                        if current_sentence_id:
                            if self.processor.validate_token(token):
                                # Note: enrichment will be done when we have full context
                                current_tokens.append(token)
                        
                    except ParseError:
                        raise  # Re-raise parse errors
                    except Exception as e:
                        raise ParseError(f"Line {line_num}: {str(e)}")
                
                # Yield final sentence if we have tokens
                if current_tokens and current_sentence_id:
                    yield self._create_sentence_context(
                        current_sentence_id, 
                        current_sentence_num or 1, 
                        current_tokens
                    )
                    
        except FileNotFoundError:
            raise FileProcessingError(f"File not found: {file_path}")
        except PermissionError:
            raise FileProcessingError(f"Permission denied: {file_path}")
        except Exception as e:
            if isinstance(e, (ParseError, FileProcessingError)):
                raise
            raise FileProcessingError(f"Error processing file {file_path}: {str(e)}")
    
    def parse_token_line(self, line: str) -> Token:
        """
        Parse a single TSV line into a Token object.
        
        Args:
            line: TSV line to parse
            
        Returns:
            Token object with extracted information
            
        Raises:
            ParseError: If line format is invalid
        """
        try:
            parts = line.strip().split('\t')
            
            if len(parts) < self._expected_columns:
                raise ParseError(f"Insufficient columns: expected {self._expected_columns}, got {len(parts)}")
            
            # Extract token information using correct column indices
            idx = int(parts[self.columns.TOKEN_ID])
            text = parts[self.columns.TOKEN_TEXT]
            grammatical_role = parts[self.columns.GRAMMATICAL_ROLE] if len(parts) > self.columns.GRAMMATICAL_ROLE else ""
            thematic_role = parts[self.columns.THEMATIC_ROLE] if len(parts) > self.columns.THEMATIC_ROLE else ""
            
            # Extract coreference information from correct columns
            coreference_link = None
            coreference_type = None
            inanimate_coreference_link = None
            inanimate_coreference_type = None
            
            if len(parts) > self.columns.COREFERENCE_LINK and parts[self.columns.COREFERENCE_LINK] != "_":
                coreference_link = parts[self.columns.COREFERENCE_LINK]
            
            if len(parts) > self.columns.COREFERENCE_TYPE and parts[self.columns.COREFERENCE_TYPE] != "_":
                coreference_type = parts[self.columns.COREFERENCE_TYPE]
                
            if len(parts) > self.columns.INANIMATE_COREFERENCE_LINK and parts[self.columns.INANIMATE_COREFERENCE_LINK] != "_":
                inanimate_coreference_link = parts[self.columns.INANIMATE_COREFERENCE_LINK]
                
            if len(parts) > self.columns.INANIMATE_COREFERENCE_TYPE and parts[self.columns.INANIMATE_COREFERENCE_TYPE] != "_":
                inanimate_coreference_type = parts[self.columns.INANIMATE_COREFERENCE_TYPE]
            
            return Token(
                idx=idx,
                text=text,
                sentence_num=1,  # Temporary value, will be updated in context
                grammatical_role=grammatical_role,
                thematic_role=thematic_role,
                coreference_link=coreference_link,
                coreference_type=coreference_type,
                inanimate_coreference_link=inanimate_coreference_link,
                inanimate_coreference_type=inanimate_coreference_type
            )
            
        except (ValueError, IndexError) as e:
            raise ParseError(f"Invalid token line format: {line}. Error: {str(e)}")
    
    def is_sentence_boundary(self, line: str) -> bool:
        """
        Check if a line represents a sentence boundary.
        
        Args:
            line: Line to check
            
        Returns:
            True if line is a sentence boundary
        """
        line = line.strip()
        
        # Check for sentence markers (from original script patterns)
        return bool(
            line.startswith('#') or
            line.startswith('# sent_id') or
            'sent_id' in line or
            (line and not line[0].isdigit() and '\t' not in line)
        )
    
    def _extract_sentence_id(self, line: str) -> str:
        """Extract sentence ID from a sentence boundary line."""
        line = line.strip()
        
        # Handle different sentence ID formats
        if 'sent_id' in line:
            parts = line.split('=')
            if len(parts) > 1:
                return parts[1].strip()
        
        # Fallback: use the entire line as ID (cleaned)
        return line.replace('#', '').strip()
    
    def _extract_sentence_num(self, line: str) -> int:
        """Extract sentence number from sentence ID."""
        sentence_id = self._extract_sentence_id(line)
        
        # Try to extract number from various formats
        import re
        match = re.search(r'(\d+)', sentence_id)
        if match:
            return int(match.group(1))
        
        # Fallback: return 1 if no number found
        return 1
    
    def _create_sentence_context(
        self, 
        sentence_id: str, 
        sentence_num: int, 
        tokens: List[Token]
    ) -> SentenceContext:
        """Create a SentenceContext with enriched tokens."""
        # Update sentence numbers in tokens
        for token in tokens:
            token.sentence_num = sentence_num
        
        # Create basic context (will be enriched by extractors)
        context = SentenceContext(
            sentence_id=sentence_id,
            sentence_num=sentence_num,
            tokens=tokens,
            critical_pronouns=[],  # Will be populated by pronoun extractor
            coreference_phrases=[]  # Will be populated by phrase extractor
        )
        
        # Enrich tokens with context
        enriched_tokens = []
        for token in tokens:
            enriched_token = self.processor.enrich_token(token, context)
            enriched_tokens.append(enriched_token)
        
        context.tokens = enriched_tokens
        return context


class DefaultTokenProcessor(BaseTokenProcessor):
    """
    Default implementation of BaseTokenProcessor.
    
    Provides basic token validation and enrichment functionality.
    """
    
    def validate_token(self, token: Token) -> bool:
        """
        Validate that a token has all required fields.
        
        Args:
            token: Token to validate
            
        Returns:
            True if token is valid
        """
        try:
            # Basic validation
            if token.idx < 1:
                return False
            if not token.text or not token.text.strip():
                return False
            
            # Additional validation can be added here
            return True
            
        except Exception:
            return False
    
    def enrich_token(self, token: Token, context: SentenceContext) -> Token:
        """
        Enrich a token with additional computed information.
        
        Args:
            token: Token to enrich
            context: Sentence context for enrichment
            
        Returns:
            Enriched token
        """
        # For now, just return the token as-is
        # Additional enrichment logic can be added here
        return token
