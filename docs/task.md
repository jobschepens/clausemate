# main goal

Test if the presence and the linguistic features of clause mates affect the use of personal pronouns and demonstratives. 

For example: a personal pronoun occurs significantly more often with a patient clause mate than with agent clause mates 


# Task

Export a data frame with clause mates for sentences which contain referential third person personal pronouns (er, sie, es), d-pronouns (der, die, das) and demonstrative pronouns (dieser, diese, dieses). 

clause mates are sentence parts: in a sentence like "He meets Robert at the university main building" the pronoun "he" would be our critical pronoun. All the other referential expressions in the sentence would be the clause mates (so "Robert" and "the university main building"), because they are additional referential expressions to our critical pronoun.

We define all additional referential expressions in the same utterance such as the personal pronoun, d-pronoun, or demonstrative pronoun as clause mates.

Clause mates can be single words or tokens but can also be phrases or noun phrases.

Note: We just need the linguistic expressions that are annotated within the "coreference" or the "coreference (inanimate)" layer. Thus, the relevant information about animacy, grammatical role, and thematic role is already annotated for these expressions.

# gotofiles folder
# The data is in the gotofiles folder. You can find the sentences there.
# only look at C:\Users\jobsc\sciebo\INF_Schepens\ind\robert\gotofiles\2.tsv

#FORMAT=WebAnno TSV 3.3
#T_SP=webanno.custom.Expressiv|
#T_SP=webanno.custom.GrammatischeRolle|grammatischeRolle|thematischeRolle
#T_SP=webanno.custom.Non3rdpers|non3rdpers
#T_SP=webanno.custom.Perspektive|Perspektive
#T_SP=webanno.custom.Plpers|plpers
#T_SP=webanno.custom.Segment|Segment
#T_CH=de.tudarmstadt.ukp.dkpro.core.api.coref.type.CoreferenceLink|referenceRelation|referenceType
#T_CH=webanno.custom.CoreferenceInanimateLink|referenceRelation|referenceType
#T_RL=webanno.custom.PluralRef|BT_webanno.custom.GrammatischeRolle

Column	Name	Description	Example
0	Token ID	Format: sentence-position	3-1, 3-2
1	Character Positions	Start-end positions in text	185-188
2	Token Text	The actual word/token	Der, Detektiv
3	Expressiv	Custom layer (usually empty)	_
4	Grammatical Role	Subj[2], dirObj[30], etc.	Subj[2]
5	Thematic Role	Proto-Ag[2], Proto-Pat[30], etc.	Proto-Ag[2]
6	Non3rdpers	Non-third person annotation	_
7	Perspektive	Perspective annotation	_ or Narrator
8	Plpers	Plural person annotation	_
9	Segment	Segment/clause annotation	*[248]
10	Coreference	Animate coreference links	*->127-2
11	Coreference Type	Type of coreference	defNP[127]
12	Inanimate Coreference	Inanimate coreference links	*->213-1
13	Inanimate Coreference Type	Type of inanimate coreference	indefNP[213]
14	PluralRef	Plural reference relation	_

#Text=Und billiger und effizienter und überhaupt, wenn sie ein hiesiges Detektivbüro beauftragen.
34-1	2590-2593	Und	_	_	_	_	_	_	*[302]	_	_	_	_	_	
34-2	2594-2602	billiger	_	_	_	_	_	_	*[302]	_	_	_	_	_	
34-3	2603-2606	und	_	_	_	_	_	_	*[302]	_	_	_	_	_	
34-4	2607-2618	effizienter	_	_	_	_	_	_	*[302]	_	_	_	_	_	
34-5	2619-2622	und	_	_	_	_	_	_	*[302]	_	_	_	_	_	
34-6	2623-2632	überhaupt	_	_	_	_	_	_	*[302]	_	_	_	_	_	
34-7	2632-2633	,	_	_	_	_	_	_	*[302]	_	_	_	_	_	
34-8	2634-2638	wenn	_	_	_	_	_	_	*[303]	_	_	_	_	_	
34-9	2639-2642	sie	_	Subj	Proto-Ag	_	_	_	*[303]	*->115-4	PersPron[115]	_	_	_	
34-10	2643-2646	ein	_	dirObj[30]	Proto-Pat[30]	_	_	_	*[303]	_	_	*->213-1	indefNP[213]	_	
34-11	2647-2655	hiesiges	_	dirObj[30]	Proto-Pat[30]	_	_	_	*[303]	_	_	*->213-1	indefNP[213]	_	
34-12	2656-2668	Detektivbüro	_	dirObj[30]	Proto-Pat[30]	_	_	_	*[303]	_	_	*->213-1	indefNP[213]	_	
34-13	2669-2680	beauftragen	_	_	_	_	_	_	*[303]	_	_	_	_	_	
34-14	2680-2681	.	_	_	_	_	_	_	*[303]	_	_	_	_	_	

Every row in the data frame should contain the following information in its columns:

column 1: sentence number (e.g. "34" in the example above)

column 2: the critical pronoun (the pronoun that we are interested in, e.g. "sie" in the example above). a pronoun can have multiple clause mates, so this is not a unique identifier. It can also have 0 clause mates, in which case the row will just contain the pronoun and no clause mates. If a pronoun itself is a clause mate of another pronoun, it should be seperately included in the data frame as a clause mate, but also as the critical pronoun.

Column 3 the clause mate. For example: one clause mate is: "ein hiesiges Detektivbüro". This should be a single row in the data frame. For the senetence "He meets Robert at the university main building" there would be two rows because there are two clause mates: "Robert" and "the university main building".




# Data frame columns (do this later)

independent vars:
- Linguistische Form of the clause mate (DP-type, e.g. "indefNP".)
- Grammatische Rolle/grammatical role of clause mate (e.g. "dirObj")
- Thematische Rolle/thematic role of clause mate (e.g. "Proto-Pat")
- Belebtheit/animacy of clause mate (e.g. "anim", "inanim")
- Linear Position im Satz/sentence position of clause mate (e.g. "34-10", "34-11", "34-12" should be "10", "11", and "12")
- Givenness (neu oder bekannt)/givenness (new or known) of clause mate (e.g. "neu", "bekannt"), for example if a referential expression is mentioned for the first time in the text, it is "neu", if it has been mentioned before, it is "bekannt". 
- Anzahl der Clause Mates im Satz/number of clause mates in the same sentence as the critical pronoun
- presence/absence of Clause Mates in the same sentence as the critical pronoun

dependent vars: 
- pronoun linguistic form (which pronoun, DP-type, e.g. "PersPron".)
- pronoun grammatical role (e.g. "Subj", "dirObj")
- pronoun thematic role (e.g. "Proto-Ag", "Proto-Pat")
- pronoun linear position (e.g. "34-9" should be "9" for the 9th token in sentence 34 
- pronoun linear distance to antecedent. This can be in a different sentence, so it is not always a token position, but rather a distance in tokens. For example, if the pronoun is in sentence 34 and the antecedent is in sentence 20, the distance would be the number of tokens between the pronoun and the antecedent. If the pronoun is in the same sentence as its antecedent, this is just the number of tokens between them.
- antecedent choice (antecedent is the referential expression that the pronoun refers to, e.g. "Robert" in the example above). If there are several potential ambiguous antecedents, this is the number of possible antecedents in the same sentence as where the actual antecedent is in. 

In inception, clause mates are always annotated with the "coreference" or the "coreference (inanimate)" layer. In this annotation, we find the information whether they are coreferential with any other phrase and what linguistic form they have. So each expression that appears in the same sentence as a personal or demonstrative pronoun which is annotated in one of those two layers counts as a clause mate. Furthermore, all these additional referential expressions are annotated with the layer "gramm+them Rolle" for grammatical role and thematic role information.




# antecedents

- personal pronoun appears significantly more often in the same linear position as its antecedent when a clause mate is present than when it is not present 
    - e.g. the average linear distance between pronoun and antecedent is 2.1 tokens when a clause mate is present, versus 4.5 tokens when absent
    - or the average linear position of the pronoun is 2.1 tokens when a clause mate is present and this is very constant. When there is no clause mate, the pronoun appears in a more variable position, e.g. 2.1, 3.5, 4.0, etc.

To identify the antecedent of a pronoun, check the annotation in the "coreference" or "coreference (inanimate)" layer. The pronoun will have a pointer (e.g., "*->20-4") indicating which referential expression it refers to. The target of this pointer is the antecedent.

For example, how do i determine the antecedent of "sie" in: 

"the answer should be the most recent one" ?

most recent antecedent is: 33-5
"middle" antecedent is: 33-1
1st antecedent is: 33-11

## chains antecedents:

to systematically determine the antecedent:

- Identify the coreference chain: Look for the chain number (here it's [20])
- Find all mentions in that chain: Look for other tokens with the same chain reference
- Select the most recent: Among all previous mentions in the chain, choose the one closest to the pronoun
- So the antecedent of "sie" (34-9) is the entity mentioned at 33-5, which is the most recent mention in the coreference chain [20] before the pronoun appears.]


# plan
- start building the rows of data frame
    - first make a df with only the clause mates
    - only look at C:\Users\jobsc\sciebo\INF_Schepens\ind\robert\gotofiles\2.tsv
- antecedent stuff later