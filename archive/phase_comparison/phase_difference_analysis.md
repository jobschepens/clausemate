# Comprehensive Phase Difference Analysis

**Generated:** 2025-07-23 23:15:49

##  COMPREHENSIVE DIFFERENCE ANALYSIS

---


###  BASIC STATISTICS:
Phase 1: 448 relationships, 38 columns
Phase 2: 448 relationships, 38 columns
Difference: +0 relationships

###  COLUMN DIFFERENCES:
Common columns: 38

###  SENTENCE ID PATTERN ANALYSIS:

---

Phase 1 sentence ID columns:
  sentence_id (primary): Sample values [4, 7, 7, 7, 7]
  sentence_id_numeric: Sample values [4, 7, 7, 7, 7]
  sentence_id_prefixed: Sample values ['sent_4', 'sent_7', 'sent_7', 'sent_7', 'sent_7']

Phase 2 sentence ID columns:
  sentence_id (primary): Sample values [4, 7, 7, 7, 7]
  sentence_id_numeric: Sample values [4, 7, 7, 7, 7]
  sentence_id_prefixed: Sample values ['sent_4', 'sent_7', 'sent_7', 'sent_7', 'sent_7']

Numeric sentence ID comparison:
  Phase 1 unique numeric IDs: 101
  Phase 2 unique numeric IDs: 101
  Common numeric IDs: 101

###  PROCESSING ORDER ANALYSIS:

---

Phase 1: First 10 sentences by numeric sentence ID:
      1. Sent   4: 1 relationships, tokens: [1]
      2. Sent   7: 4 relationships, tokens: [3, 3, 10, 10]
      3. Sent  10: 1 relationships, tokens: [8]
      4. Sent  11: 15 relationships, tokens: [2, 2, 2, 2, 2, 7, 7, 7, 7, 7, 17, 17, 17, 17, 17]
      5. Sent  12: 2 relationships, tokens: [3, 3]
      6. Sent  17: 10 relationships, tokens: [4, 4, 4, 4, 4, 18, 18, 18, 18, 18]
      7. Sent  26: 1 relationships, tokens: [7]
      8. Sent  29: 2 relationships, tokens: [6, 6]
      9. Sent  30: 6 relationships, tokens: [10, 10, 10, 23, 23, 23]
     10. Sent  33: 3 relationships, tokens: [1, 1, 1]

Phase 2: First 10 sentences by numeric sentence ID:
      1. Sent   4: 1 relationships, tokens: [1]
      2. Sent   7: 4 relationships, tokens: [3, 3, 10, 10]
      3. Sent  10: 1 relationships, tokens: [8]
      4. Sent  11: 15 relationships, tokens: [2, 2, 2, 2, 2, 7, 7, 7, 7, 7, 17, 17, 17, 17, 17]
      5. Sent  12: 2 relationships, tokens: [3, 3]
      6. Sent  17: 10 relationships, tokens: [4, 4, 4, 4, 4, 18, 18, 18, 18, 18]
      7. Sent  26: 1 relationships, tokens: [7]
      8. Sent  29: 2 relationships, tokens: [6, 6]
      9. Sent  30: 6 relationships, tokens: [10, 10, 10, 23, 23, 23]
     10. Sent  33: 3 relationships, tokens: [1, 1, 1]

###  SORTING PATTERN ANALYSIS:

---

Phase 1 - First 10 rows after sorting by sentence_id_numeric:
      1. Sent   4, Token  1: 'Der' → 'der Liftgeschichte'
      2. Sent   7, Token  3: 'er' → 'das Gefühl'
      3. Sent   7, Token  3: 'er' → 'er'
      4. Sent   7, Token 10: 'er' → 'er'
      5. Sent   7, Token 10: 'er' → 'das Gefühl'
      6. Sent  10, Token  8: 'er' → 'der Detektiv'
      7. Sent  11, Token  2: 'er' → 'er'
      8. Sent  11, Token  2: 'er' → 'Zell'
      9. Sent  11, Token  2: 'er' → 'er'
     10. Sent  11, Token  2: 'er' → 'den aussichtslosen Fall der beiden Amerikaner'

Phase 2 - First 10 rows after sorting by sentence_id_numeric:
      1. Sent   4, Token  1: 'Der' → 'der Liftgeschichte'
      2. Sent   7, Token  3: 'er' → 'das Gefühl'
      3. Sent   7, Token  3: 'er' → 'er'
      4. Sent   7, Token 10: 'er' → 'er'
      5. Sent   7, Token 10: 'er' → 'das Gefühl'
      6. Sent  10, Token  8: 'er' → 'der Detektiv'
      7. Sent  11, Token  2: 'er' → 'er'
      8. Sent  11, Token  2: 'er' → 'Zell'
      9. Sent  11, Token  2: 'er' → 'er'
     10. Sent  11, Token  2: 'er' → 'den aussichtslosen Fall der beiden Amerikaner'

✓ All sentences present in both phases when using numeric IDs

###  DATA CONTENT ANALYSIS:

---

Pronoun frequency comparison:

Clause mate analysis:
  Phase 1 unique clause mates: 191
  Phase 2 unique clause mates: 191

Missing value analysis:
  pronoun_text: Phase1=0, Phase2=0
  clause_mate_text: Phase1=0, Phase2=0
  pronoun_coref_ids: Phase1=0, Phase2=0

###  PRONOUN ANALYSIS:
Phase 1 unique pronouns: 16
Phase 2 unique pronouns: 16

Top 5 pronouns in Phase 1:
  er: 181 → 181 (Δ+0)
  der: 66 → 66 (Δ+0)
  sie: 46 → 46 (Δ+0)
  ihn: 36 → 36 (Δ+0)
  ihm: 31 → 31 (Δ+0)

###  SENTENCE ANALYSIS:
Phase 1 unique sentences: 101
Phase 2 unique sentences: 101

###  SAMPLE RELATIONSHIP COMPARISON:
First 3 relationships in Phase 1:
  1. Sent 4: 'Der' → 'der Liftgeschichte'
  2. Sent 7: 'er' → 'das Gefühl'
  3. Sent 7: 'er' → 'er'

First 3 relationships in Phase 2:
  1. Sent 4: 'Der' → 'der Liftgeschichte'
  2. Sent 7: 'er' → 'das Gefühl'
  3. Sent 7: 'er' → 'er'

###  FILE SIZE ANALYSIS:
Phase 1: 102,655 bytes (0.10 MB)
Phase 2: 94,311 bytes (0.09 MB)
Size difference: -8,344 bytes (-0.01 MB)
Size change: -8.1%

###  EFFICIENCY METRICS:
Phase 1: 4.5 relationships per KB
Phase 2: 4.9 relationships per KB
Efficiency change: +8.8%

###  KEY FINDINGS SUMMARY:

---

1. Row difference: +0 relationships
2. Column compatibility: ✓ Perfect
3. Sentence ID format: Phase 1 uses prefixed, Phase 2 uses numeric
4. Performance: Phase 2 is 1.1x more efficient
5. Missing sentences: 0 sentences have different relationship counts


---
*Analysis completed at 2025-07-23 23:15:49*
