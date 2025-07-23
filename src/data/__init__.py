"""Data models and structures for the clause mates analyzer."""

from .models import AnimacyType, AntecedentInfo, ClauseMateRelationship, Phrase, Token

__all__ = [
    "Token",
    "Phrase",
    "ClauseMateRelationship",
    "AnimacyType",
    "AntecedentInfo",
]
