# Cross-Sentence Antecedent Detection Analysis Report

**Generated from Phase 2 implementation with cross-sentence antecedent analysis**

## Antecedent Detection Analysis

- **Total relationships**: 448
- **Successful antecedent detections**: 423
- **Success rate**: 94.4%

## Task Requirement Analysis

**Research Question**: Do pronouns appear at more consistent linear positions when clause mates are present?

### Clause Mate Presence Analysis

**With multiple clause mates** (400 cases):
- Average pronoun-antecedent distance: 34.4 tokens
- Distance variability (std dev): 228.3

**With few/no clause mates** (23 cases):
- Average pronoun-antecedent distance: 14.7 tokens
- Distance variability (std dev): 9.3

### Task Pattern Check

❌ **Different pattern**: Longer average distance when clause mates present
❌ **Different pattern**: More variable positions when clause mates present

## Cross-Sentence Detection Examples

**Cross-sentence antecedents found**: 113

### Diverse Examples
*Showing correct "most recent" antecedent selection across sentences:*

#### Example 1

**CURRENT SENTENCE 17**: "Ende Dezember sind sie aufgetaucht aus der Stadt, haben alles durcheinandergebracht, und Ende Jänner sind sie wieder verschwunden."

- **Critical pronoun**: "sie" (token 4)
- **Grammatical role**: Subj, **Thematic role**: Proto-Ag
- **Clause mate**: "Ende Dezember" (Oblique[14], *[14])
- **Total clause mates in sentence**: 5

**MOST RECENT ANTECEDENT**: "Die Polizei" (distance: 24 tokens)
  - Found in **Sentence 15**: "Die Polizei hat es ja schon Ende Jänner aufgegeben gehabt."


- **Antecedent choices available**: 1
- **Coreference links**: animate: *->129-2, inanimate: nan

#### Example 2

**CURRENT SENTENCE 26**: "Dazu mußt du wissen, daß sie steinreich gewesen sind."

- **Critical pronoun**: "sie" (token 7)
- **Grammatical role**: Subj, **Thematic role**: Proto-Ag
- **Clause mate**: "du" (Subj, Proto-Ag)
- **Total clause mates in sentence**: 1

**MOST RECENT ANTECEDENT**: "Die Toten" (distance: 18 tokens)
  - Found in **Sentence 25**: "Die Toten sind ja die amerikanischen Schwiegereltern vom Vergolder Antretter gewesen."

**FIRST ANTECEDENT**: "Die beiden Amerikaner" (distance: 270 tokens)
  - Found in **Sentence 5**: "Die beiden Amerikaner sind Ende Dezember am Sessellift in Zell erfroren."

- **Antecedent choices available**: 4
- **Coreference links**: animate: *->110-5, inanimate: nan

#### Example 3

**CURRENT SENTENCE 30**: "Natürlich haben sich die Zeller darüber gewundert, daß der zuerst als Polizist verschwindet, also der Brenner, und dann taucht er drei Wochen später als Privatdetektiv wieder auf."

- **Critical pronoun**: "der" (token 10)
- **Grammatical role**: Subj, **Thematic role**: Proto-Ag
- **Clause mate**: "die Zeller" (Subj[26], Proto-Ag[26])
- **Total clause mates in sentence**: 3

**MOST RECENT ANTECEDENT**: "der Brenner" (distance: 103 tokens)
  - Found in **Sentence 22**: "Und Anfang März taucht der Brenner auf einmal wieder auf."

**FIRST ANTECEDENT**: "ein Detektiv" (distance: 354 tokens)
  - Found in **Sentence 2**: "Aber vom Pinzgau aus gesehen: vierzig Hotels, neun Schulen, dreißig Dreitausender, achtundfünfzig Lifte, ein See, ein Detektiv."

- **Antecedent choices available**: 14
- **Coreference links**: animate: *->127-15, inanimate: nan

#### Example 4

**CURRENT SENTENCE 33**: "Die haben aber nicht ihren eigenen Detektiv aus Amerika herübergeschickt, weil erstens Sprachprobleme, und zweitens ist es ja viel einfacher."

- **Critical pronoun**: "Die" (token 1)
- **Grammatical role**: Subj, **Thematic role**: Proto-Ag
- **Clause mate**: "ihren" (dirObj[29], Proto-Pat[29])
- **Total clause mates in sentence**: 3

**MOST RECENT ANTECEDENT**: "der amerikanischen Versicherung" (distance: 23 tokens)
  - Found in **Sentence 31**: "Dann hat sich herausgestellt, daß es eine Versicherungsgeschichte war, von der amerikanischen Versicherung aus, weil es da ja um viel, viel Geld gegangen ist."


- **Antecedent choices available**: 1
- **Coreference links**: animate: *->115-2, inanimate: nan

#### Example 5

**CURRENT SENTENCE 34**: "Und billiger und effizienter und überhaupt, wenn sie ein hiesiges Detektivbüro beauftragen."

- **Critical pronoun**: "sie" (token 9)
- **Grammatical role**: Subj, **Thematic role**: Proto-Ag
- **Clause mate**: "ein hiesiges Detektivbüro" (dirObj[30], Proto-Pat[30])
- **Total clause mates in sentence**: 1

**MOST RECENT ANTECEDENT**: "ihren" (distance: 27 tokens)
  - Found in **Sentence 33**: "Die haben aber nicht ihren eigenen Detektiv aus Amerika herübergeschickt, weil erstens Sprachprobleme, und zweitens ist es ja viel einfacher."

**FIRST ANTECEDENT**: "der amerikanischen Versicherung" (distance: 54 tokens)
  - Found in **Sentence 31**: "Dann hat sich herausgestellt, daß es eine Versicherungsgeschichte war, von der amerikanischen Versicherung aus, weil es da ja um viel, viel Geld gegangen ist."

- **Antecedent choices available**: 3
- **Coreference links**: animate: *->115-4, inanimate: nan

#### Example 6

**CURRENT SENTENCE 37**: "Jetzt muß man wissen, daß der 19 Jahre bei der Kripo gewesen ist, weil mit 25 hat er angefangen, und jetzt ist er 44 gewesen."

- **Critical pronoun**: "der" (token 7)
- **Grammatical role**: Subj, **Thematic role**: Proto-Ag
- **Clause mate**: "man" (Subj, Proto-Ag)
- **Total clause mates in sentence**: 5

**MOST RECENT ANTECEDENT**: "der" (distance: 16 tokens)
  - Found in **Sentence 28**: "Ist ja schon der Vergolder selber steinreich, bestimmt der reichste Mann in Zell, weit vor dem Eder, weit vor dem Bürgermeister und meilenweit vor dem Fürstauer."

**FIRST ANTECEDENT**: "ein Detektiv" (distance: 498 tokens)
  - Found in **Sentence 2**: "Aber vom Pinzgau aus gesehen: vierzig Hotels, neun Schulen, dreißig Dreitausender, achtundfünfzig Lifte, ein See, ein Detektiv."

- **Antecedent choices available**: 19
- **Coreference links**: animate: *->127-20, inanimate: nan

#### Example 7

**CURRENT SENTENCE 41**: "Jetzt hat der aber vor drei Jahren einen neuen Chef gekriegt, den Nemec, der ja auch im Jänner hier in Zell aufgekreuzt ist."

- **Critical pronoun**: "der" (token 3)
- **Grammatical role**: Subj, **Thematic role**: Proto-Ag
- **Clause mate**: "vor drei Jahren" (Oblique[37], *[37])
- **Total clause mates in sentence**: 6

**MOST RECENT ANTECEDENT**: "der" (distance: 25 tokens)
  - Found in **Sentence 31**: "Dann hat sich herausgestellt, daß es eine Versicherungsgeschichte war, von der amerikanischen Versicherung aus, weil es da ja um viel, viel Geld gegangen ist."

**FIRST ANTECEDENT**: "ein Detektiv" (distance: 570 tokens)
  - Found in **Sentence 2**: "Aber vom Pinzgau aus gesehen: vierzig Hotels, neun Schulen, dreißig Dreitausender, achtundfünfzig Lifte, ein See, ein Detektiv."

- **Antecedent choices available**: 25
- **Coreference links**: animate: *->127-26, inanimate: nan

#### Example 8

**CURRENT SENTENCE 48**: "Aber mehr ruhiger, gemütlicher, und der Nemec hat ihn von Anfang an nicht haben wollen."

- **Critical pronoun**: "ihn" (token 11)
- **Grammatical role**: dirObj, **Thematic role**: Proto-Pat
- **Clause mate**: "der Nemec" (Subj[47], Proto-Ag[47])
- **Total clause mates in sentence**: 2

**MOST RECENT ANTECEDENT**: "er" (distance: 20 tokens)
  - Found in **Sentence 38**: "Aber er hat es nie richtig weit gebracht bei der Kripo."

**FIRST ANTECEDENT**: "ein Detektiv" (distance: 695 tokens)
  - Found in **Sentence 2**: "Aber vom Pinzgau aus gesehen: vierzig Hotels, neun Schulen, dreißig Dreitausender, achtundfünfzig Lifte, ein See, ein Detektiv."

- **Antecedent choices available**: 28
- **Coreference links**: animate: *->127-29, inanimate: nan
