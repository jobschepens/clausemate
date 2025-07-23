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

    MISSING_VALUE = "_"
    SENTENCE_PREFIX = "sent_"
    MIN_COLUMNS_REQUIRED = 15

    # Coreference types
    PERSONAL_PRONOUN_TYPE = "PersPron"
    D_PRONOUN_TYPE = "D-Pron"
    DEMONSTRATIVE_PRONOUN_TYPE = "DemPron"

    # Givenness values
    NEW_MENTION = "neu"
    GIVEN_MENTION = "bekannt"

    # Animacy layers
    ANIMATE_LAYER = "anim"
    INANIMATE_LAYER = "inanim"


class PronounSets:
    """Sets of critical pronouns."""

    THIRD_PERSON_PRONOUNS: Set[str] = {"er", "sie", "es", "ihm", "ihr", "ihn", "ihnen"}

    D_PRONOUNS: Set[str] = {
        "der",
        "die",
        "das",
        "dem",
        "den",
        "deren",
        "dessen",
        "derer",
    }

    DEMONSTRATIVE_PRONOUNS: Set[str] = {"dieser", "diese", "dieses", "diesem", "diesen"}


class FilePaths:
    """Default file paths - using relative paths for portability."""

    INPUT_FILE = r"data/input/gotofiles/2.tsv"
    OUTPUT_FILE = r"data/output/clause_mates_phase2_export.csv"


class RegexPatterns:
    """Common regex patterns."""

    COREFERENCE_TYPE_PATTERN = r"([a-zA-Z-]+)\["
    COREFERENCE_ID_PATTERN = r"\[(\d+-?\d*)\]"
    COREFERENCE_ID_FALLBACK_PATTERN = r"\[(\d+)\]"
    COREFERENCE_LINK_PATTERN = r"\*->(\d+-\d+)"
    COREFERENCE_LINK_FALLBACK_PATTERN = r"\*->(\d+)"


class ExportColumns:
    """Standardized column order for clause mates export (both Phase 1 and Phase 2)."""

    STANDARD_ORDER = [
        # Sentence Information
        "sentence_id",
        "sentence_id_numeric",
        "sentence_id_prefixed",
        "sentence_num",
        "first_words",
        # Pronoun Basic Information
        "pronoun_text",
        "pronoun_token_idx",
        "pronoun_grammatical_role",
        "pronoun_thematic_role",
        "pronoun_givenness",
        # Pronoun Coreference Information
        "pronoun_coref_ids",
        "pronoun_coref_base_num",
        "pronoun_coref_occurrence_num",
        # Pronoun Coreference Links
        "pronoun_coreference_link",
        "pronoun_coref_link_base_num",
        "pronoun_coref_link_occurrence_num",
        "pronoun_coreference_type",
        # Pronoun Inanimate Coreference Links
        "pronoun_inanimate_coreference_link",
        "pronoun_inanimate_coref_link_base_num",
        "pronoun_inanimate_coref_link_occurrence_num",
        "pronoun_inanimate_coreference_type",
        # Pronoun Antecedent Information
        "pronoun_most_recent_antecedent_text",
        "pronoun_most_recent_antecedent_distance",
        "pronoun_first_antecedent_text",
        "pronoun_first_antecedent_distance",
        "pronoun_antecedent_choice",
        # Clause Mate Information
        "num_clause_mates",
        "clause_mate_text",
        "clause_mate_coref_id",
        "clause_mate_coref_base_num",
        "clause_mate_coref_occurrence_num",
        "clause_mate_start_idx",
        "clause_mate_end_idx",
        "clause_mate_grammatical_role",
        "clause_mate_thematic_role",
        "clause_mate_coreference_type",
        "clause_mate_animacy",
        "clause_mate_givenness",
    ]
