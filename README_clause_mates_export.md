# Clause Mates Analysis - Export Documentation

## Project Overview
This project extracts and analyzes clause mate relationships for German pronouns to test whether the presence and linguistic features of clause mates affect pronoun usage patterns.

## Files in This Export

### 📊 **Data Files**
- **`clause_mates_chap2_export.csv`** - Main dataset with clause mate relationships
  - 37 columns covering pronoun features, clause mate features, and antecedent information
  - Each row = one clause mate relationship
  - UTF-8 encoded CSV format

### 📋 **Documentation**
- **`clause_mates_data_documentation.md`** - Comprehensive data documentation
  - Column descriptions and data types
  - Usage examples and interpretation guide
  - Quality assurance information

- **`clause_mates_metadata.json`** - Technical metadata
  - JSON format specifications
  - Algorithm descriptions
  - Data validation rules
  - Analysis recommendations

### 🔧 **Source Code**
- **`clause_mates_complete.py`** - Main extraction script
  - Full implementation with phrase-level antecedent detection
  - Animacy-based antecedent choice calculation
  - Numeric conversion of string variables

### 📝 **Project Specification**
- **`task.md`** - Original task requirements and specifications

## Quick Start Guide

### 1. **Loading the Data**
```python
import pandas as pd

# Load the main dataset
df = pd.read_csv('clause_mates_chap2_export.csv', encoding='utf-8')

# Basic info
print(f"Dataset shape: {df.shape}")
print(f"Columns: {list(df.columns)}")
```

### 2. **Key Research Variables**

**Dependent Variables (Pronoun Behavior):**
- `pronoun_text` - Which pronoun was used
- `pronoun_grammatical_role` - Grammatical role of pronoun
- `pronoun_most_recent_antecedent_distance` - Distance to antecedent

**Independent Variables (Clause Mate Features):**
- `clause_mate_coreference_type` - Linguistic form of clause mate
- `clause_mate_grammatical_role` - Grammatical role of clause mate
- `clause_mate_animacy` - Animate vs inanimate clause mate
- `num_clause_mates` - Number of clause mates in sentence

### 3. **Example Analyses**

```python
# Test: Do pronouns appear more often with patient vs agent clause mates?
thematic_roles = df['clause_mate_thematic_role'].value_counts()

# Compare pronoun-antecedent distances with/without clause mates
with_mates = df[df['num_clause_mates'] > 1]['pronoun_most_recent_antecedent_distance']
single_mate = df[df['num_clause_mates'] == 1]['pronoun_most_recent_antecedent_distance']

# Analyze by animacy
animacy_analysis = df.groupby(['pronoun_text', 'clause_mate_animacy']).size()
```

## Data Quality Highlights

✅ **Validated Critical Pronouns**: Both annotation type and token text checked  
✅ **Phrase-Level Antecedents**: Multi-token expressions treated as units  
✅ **Complete Chain Tracking**: Both most recent and first antecedents included  
✅ **Numeric Conversions**: String variables converted for statistical analysis  
✅ **Cross-Sentence Distances**: Accurate token counting across sentence boundaries  

## Key Features

### 🎯 **Antecedent Detection**
- **Most Recent**: Closest mention before pronoun (linear distance)
- **First in Chain**: First mention in coreference chain (occurrence number)
- **Antecedent Choice**: Number of compatible alternatives in antecedent's sentence

### 🏷️ **Linguistic Annotation**
- **Animacy**: Determined by coreference layer (animate/inanimate)
- **Givenness**: New (first mention) vs Given (subsequent mention)
- **Roles**: Grammatical and thematic roles for both pronouns and clause mates

### 🔢 **Statistical Ready**
- All string variables have numeric counterparts
- Missing values properly handled
- Data types optimized for analysis

## Research Applications

This dataset enables investigation of:

1. **Pronoun Choice Patterns**
   - Which pronouns co-occur with specific clause mate types?
   - How does clause mate animacy affect pronoun selection?

2. **Distance Effects**  
   - Do clause mates affect pronoun-antecedent distance?
   - Is distance more consistent when clause mates are present?

3. **Ambiguity Resolution**
   - How many potential antecedents compete with the actual one?
   - Does clause mate presence correlate with antecedent choice complexity?

4. **Information Structure**
   - How do given/new clause mates pattern with pronoun usage?
   - What role do thematic roles play in clause mate distribution?

## Citation
When using this dataset, please reference:
- Source: WebAnno TSV annotations (Chapter 2)
- Processing: clause_mates_complete.py
- Date: June 27, 2025

---

*For technical questions, consult the metadata.json file.*  
*For detailed column descriptions, see the data documentation.*  
*For implementation details, refer to the source code.*
