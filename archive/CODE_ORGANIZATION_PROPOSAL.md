# Code Organization Proposal - COMPLETED ✅

## Status: IMPLEMENTATION COMPLETE (2025-07-23)

This proposal has been fully implemented. The repository has been successfully reorganized using **Option B: Research-Friendly** structure.

## Original Issues - RESOLVED ✅

- ~~`phase1/` folder suggests incomplete migration to Phase 2~~ → **Moved to `archive/phase1/`**
- ~~`old/` folder contains many experimental files and duplicates~~ → **Externally backed up and removed**
- ~~Multiple CSV outputs scattered in root directory~~ → **Organized in `data/output/`**
- ~~Unclear which code is "current" vs "archived"~~ → **Clear separation: `src/` vs `archive/`**

## Proposed Structure

### Option A: Git-Based (Recommended for Production)

```
src/                    # Current active development
├── main.py             # Phase 2 main entry point
├── config.py           # Current configuration
├── data/               # Data models
├── extractors/         # Feature extractors
├── parsers/            # File parsers
└── analyzers/          # Analysis components

tests/                  # Test suite
docs/                   # Documentation
├── README.md
├── ROADMAP.md
├── PYLINT_README.md
└── phase_comparison/   # Comparison analysis (moved from root)

data/                   # Input/output data
├── input/              # Source TSV files
├── output/             # Generated CSV files
└── annotation/         # Annotation files

# Archive previous phases using git tags:
# git tag phase1-final
# git tag phase2-milestone
```

## IMPLEMENTED STRUCTURE ✅

The final implemented structure (Option B: Research-Friendly):

```
├── archive/              # Historical versions and deprecated code - ✅ CREATED
│   ├── phase1/          # Original Phase 1 implementation - ✅ MOVED
│   └── *.json           # Old project exports - ✅ MOVED
├── data/                # All data files organized by purpose - ✅ CREATED
│   ├── input/           # Source data and annotations - ✅ CREATED
│   │   ├── annotation/  # Annotation files by chapter - ✅ MOVED
│   │   ├── source/      # Original text files - ✅ MOVED
│   │   ├── gotofiles/   # Navigation/reference files - ✅ MOVED
│   │   ├── annotation_ser/ # Serialized annotation data - ✅ MOVED
│   │   ├── curation/    # Curated datasets - ✅ MOVED
│   │   └── curation_ser/ # Serialized curation data - ✅ MOVED
│   └── output/          # Generated files and results - ✅ CREATED
│       ├── *.csv        # Analysis results - ✅ MOVED
│       ├── *.log        # Processing logs - ✅ MOVED
│       └── log/         # Log directories - ✅ MOVED
├── docs/                # Documentation and references - ✅ CREATED
│   ├── README.md        # Main documentation - ✅ MOVED
│   ├── task.md          # Project task description - ✅ MOVED
│   ├── hyp.txt          # Hypothesis file - ✅ MOVED
│   └── *.png            # Screenshots and diagrams - ✅ MOVED
├── tools/               # Analysis scripts and utilities - ✅ CREATED
│   └── *.py             # All Python analysis tools - ✅ MOVED
└── src/                 # Current implementation (Phase 2) - ✅ UNCHANGED
```

## VERIFICATION RESULTS ✅

- **Phase 2 Testing**: Successfully processed `data\input\gotofiles\2.tsv` → `data\output\test_reorganized_phase2.csv`
- **Output Generated**: 448 relationships extracted from 222 sentences
- **Dependencies**: Python environment configured with pandas installed
- **File Paths**: All imports and file references work correctly with new structure
- **External Backup**: `old/` folder safely preserved outside repository

## IMPLEMENTATION COMPLETED ✅

### ✅ Phase 1: Handle Reference Files (COMPLETED)

1. ✅ **External backup created** - `old/` folder safely preserved outside repository
2. ✅ **Repository cleaned** - `old/` folder removed from tracking
3. ✅ **Documentation updated** - All changes documented

### ✅ Phase 2: Create New Structure (COMPLETED)

1. ✅ **New folder structure created** - archive/, data/, docs/, tools/ directories
2. ✅ **Files moved** to new locations according to plan
3. ✅ **Phase 2 tested** - Confirmed working with new file paths

### ✅ Phase 3: Verification (COMPLETED)

1. ✅ **Functionality verified** - Phase 2 successfully processes data with new structure
2. ✅ **Dependencies installed** - Python environment properly configured
3. ✅ **Output validated** - 448 relationships extracted from test run

### ✅ Phase 4: Optional Cleanup (COMPLETED)

1. ✅ Updated `.gitignore` to exclude data/output from future commits
2. ✅ Updated pylint workflow to exclude archive folders and use new paths
3. ✅ Tested GitHub Actions with new file paths (pylint passes 10.0/10)
4. ✅ Updated documentation links in README.md to reflect new structure

## Detailed Migration Plan

### ✅ Step 1: Reference Files Preserved (COMPLETED)

- External backup created and stored safely
- Ready to remove `old/` folder from repository

### Step 2: Remove Old Files and Create Structure

```bash
# Remove old folder from repository (safe since backed up)
git rm -r old/
rm -rf old/  # Remove from filesystem too

# Create new directory structure
mkdir -p archive/experiments docs data/input data/output tools

# Document what was in the old folder
echo "# Old Folder Contents Reference" > OLD_FOLDER_REFERENCE.md
echo "External backup created on $(date)" >> OLD_FOLDER_REFERENCE.md
echo "Backup contains experimental and reference files from development process" >> OLD_FOLDER_REFERENCE.md
```

### Step 3: Move Files to New Structure

```bash
# Move phase1 to archive (keep as working reference)
mv phase1/ archive/

# Move data folders to organized structure
mv annotation/ data/input/
mv source/ data/input/
mv gotofiles/ data/input/
mv curation/ data/input/
mv annotation_ser/ data/input/
mv curation_ser/ data/input/

# Move output data
mv exports_sent_to_robert/ data/output/
mv shared_robert_exports/ data/output/
mv clause_mates_*.csv data/output/

# Move documentation to docs folder
mkdir docs
mv phase_comparison/ docs/
mv ROADMAP.md docs/
mv PYLINT_README.md docs/
mv CODE_ORGANIZATION_PROPOSAL.md docs/
mv PHASE2_COMPLETION_REPORT.md docs/

# Move utility tools
mv verify_first_words.py tools/
mv verify_pronoun_coref_ids.py tools/
```

### Step 4: Update Configurations and Paths

```bash
# Update .gitignore to exclude outputs and cache
cat >> .gitignore << EOF
# Data outputs (generated files)
data/output/*.csv
data/output/*.json

# Python cache
__pycache__/
.pytest_cache/
*.pyc

# IDE files
.vscode/
*.code-workspace

# Temporary files
*.log
*.tmp
EOF

# Update pylint workflow to reflect new structure
# (Will need to edit .github/workflows/pylint.yml)
```

### Step 5: Update Import Paths (If Needed)

- Check if any scripts reference moved files
- Update file paths in Phase 2 configuration if needed
- Test that `python src/run_phase2.py` still works

### Step 6: Update Documentation

- Update README.md with new project structure
- Update any hardcoded paths in documentation
- Commit all changes

## Ready-to-Execute Commands

Since the external backup is complete, here are the exact commands to run:

```bash
# 1. Remove old folder (safe since backed up)
git rm -r old/
rm -rf old/

# 2. Create new structure
mkdir -p archive docs data/input data/output tools

# 3. Move everything (run these one by one and test)
mv phase1/ archive/
mv annotation/ data/input/
mv source/ data/input/
mv gotofiles/ data/input/
mv curation/ data/input/
mv annotation_ser/ data/input/
mv curation_ser/ data/input/
mv exports_sent_to_robert/ data/output/
mv shared_robert_exports/ data/output/
mv phase_comparison/ docs/
mv ROADMAP.md docs/
mv PYLINT_README.md docs/
mv CODE_ORGANIZATION_PROPOSAL.md docs/
mv PHASE2_COMPLETION_REPORT.md docs/
mv verify_first_words.py tools/
mv verify_pronoun_coref_ids.py tools/

# 4. Move CSV files
mv clause_mates_*.csv data/output/ 2>/dev/null || echo "No CSV files to move"

# 5. Create reference document
echo "# Old Folder Contents Reference" > OLD_FOLDER_REFERENCE.md
echo "External backup created on $(date)" >> OLD_FOLDER_REFERENCE.md
echo "Contains experimental code and reference files from iterative development" >> OLD_FOLDER_REFERENCE.md
echo "Backup preserved outside repository for future reference" >> OLD_FOLDER_REFERENCE.md

# 6. Test Phase 2 still works
python src/run_phase2.py --help
```

## Handling the `old/` Folder

### ✅ COMPLETED: External Preservation

- ✅ **External backup created** and stored safely
- ✅ **Reference files preserved** outside repository
- **Ready for removal** from active repository

### Next Steps

1. **Remove from repo**: `git rm -r old/ && rm -rf old/`
2. **Document preservation**: Create `OLD_FOLDER_REFERENCE.md`
3. **Clean repository**: Proceed with reorganization

### Benefits Now Achievable

- ✅ **Reference files safely preserved**
- 🔄 **Cleaner repository** (after removal)
- 🔄 **Faster operations** (fewer files to scan)
- 🔄 **Clearer project structure** (after reorganization)
- ✅ **No risk of data loss** (backup created)

## Immediate Next Steps

**Now that external backup is complete:**

### ✅ Priority 1: Reference Files (COMPLETED)

- ✅ **External backup created** and stored safely
- **Next**: Remove `old/` folder from repository

### Priority 2: Execute Reorganization (Ready to Go)

- **Run the ready-to-execute commands** provided above
- **Test** that Phase 2 functionality remains intact
- **One-by-one approach** recommended for safety

### Priority 3: Update Configurations (Low Risk)

- **Update `.gitignore`** for new structure
- **Update GitHub Actions** paths
- **Update README** with new project structure

### Priority 4: Validate and Document (Final Step)

- **Test all functionality** works with new paths
- **Update any hardcoded paths** in scripts
- **Commit reorganized structure**

**You're now ready to execute the reorganization safely!** The most risky step (preserving reference files) is complete, so you can proceed with confidence.
