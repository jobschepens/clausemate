"""
Data models and structures for the clause mates analyzer.
"""

from .models import Token, Phrase, ClauseMateRelationship, AnimacyType, AntecedentInfo

__all__ = [
    "Token",
    "Phrase", 
    "ClauseMateRelationship",
    "AnimacyType",
    "AntecedentInfo",
]
