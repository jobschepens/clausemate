#!/usr/bin/env python3
"""Configuration module for clause mate extraction script.
Contains all constants, column definitions, and configuration settings.
"""

from typing import Set


class TSVColumns:
    """Column indices for TSV file parsing."""
    TOKEN_ID = 0
    TOKEN_TEXT = 2
    GRAMMATICAL_ROLE = 4
    THEMATIC_ROLE = 5
    COREFERENCE_LINK = 10
    COREFERENCE_TYPE = 11
    INANIMATE_COREFERENCE_LINK = 12
    INANIMATE_COREFERENCE_TYPE = 13


# Alias for backwards compatibility
ColumnIndices = TSVColumns


class Constants:
    """Application constants."""
    MISSING_VALUE = '_'
    SENTENCE_PREFIX = 'sent_'
    MIN_COLUMNS_REQUIRED = 15

    # Coreference types
    PERSONAL_PRONOUN_TYPE = 'PersPron'
    D_PRONOUN_TYPE = 'D-Pron'
    DEMONSTRATIVE_PRONOUN_TYPE = 'DemPron'

    # Givenness values
    NEW_MENTION = 'neu'
    GIVEN_MENTION = 'bekannt'

    # Animacy layers
    ANIMATE_LAYER = 'anim'
    INANIMATE_LAYER = 'inanim'


class PronounSets:
    """Sets of critical pronouns."""
    THIRD_PERSON_PRONOUNS: Set[str] = {
        'er', 'sie', 'es', 'ihm', 'ihr', 'ihn', 'ihnen'
    }

    D_PRONOUNS: Set[str] = {
        'der', 'die', 'das', 'dem', 'den', 'deren', 'dessen', 'derer'
    }

    DEMONSTRATIVE_PRONOUNS: Set[str] = {
        'dieser', 'diese', 'dieses', 'diesem', 'diesen'
    }


class FilePaths:
    """Default file paths - using relative paths for portability."""
    INPUT_FILE = r'../../data/input/gotofiles/2.tsv'
    OUTPUT_FILE = r'../../data/output/clause_mates_phase1_export.csv'


class RegexPatterns:
    """Common regex patterns."""
    COREFERENCE_TYPE_PATTERN = r'([a-zA-Z-]+)\['
    COREFERENCE_ID_PATTERN = r'\[(\d+-?\d*)\]'
    COREFERENCE_ID_FALLBACK_PATTERN = r'\[(\d+)\]'
    COREFERENCE_LINK_PATTERN = r'\*->(\d+-\d+)'
    COREFERENCE_LINK_FALLBACK_PATTERN = r'\*->(\d+)'
