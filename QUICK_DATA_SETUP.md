# ClauseMate Data Setup - Quick Start Guide

## Problem
You need to use private/sensitive research data with ClauseMate without committing it to the public GitHub repository.

## Recommended Solutions (Pick One)

### Option 1: Simple Local Directory (Easiest)
**Best for: Personal research, local development**

1. Create a private data directory:
```bash
mkdir -p data/input/private
```

2. Copy your TSV files there:
```bash
cp /path/to/your/research/*.tsv data/input/private/
```

3. Run analyzer (it will automatically detect private data):
```bash
python src/main.py
python scripts/run_multi_file_analysis.py
```

**Pros:** Simple, immediate, works out of the box
**Cons:** Manual file management

### Option 2: Environment Variables (Flexible)
**Best for: Multiple environments, team development**

1. Create `.env` file:
```bash
cp .env.example .env
```

2. Edit `.env` file:
```bash
CLAUSEMATE_DATA_SOURCE=local_path
CLAUSEMATE_DATA_PATH=/Users/yourname/Research/clausemate-data
```

3. Put your data in the specified path and run normally.

**Pros:** Flexible, shareable configuration, works across machines
**Cons:** Requires environment setup

### Option 3: Password-Protected ZIP (Secure)
**Best for: Sensitive data, sharing with collaborators**

1. Create encrypted ZIP of your data:
```bash
# Using 7zip (cross-platform)
7z a -p"your-password" research_data.zip *.tsv

# Using zip (Mac/Linux)
zip -e research_data.zip *.tsv
```

2. Run the setup script:
```bash
python scripts/setup_data_source.py
# Choose option 2 (password-protected)
# Choose "zip" and provide path and password
```

3. Run analyzer normally (it will extract data when needed).

**Pros:** Secure, portable, can be shared safely
**Cons:** Requires password management

### Option 4: Cloud Storage (Advanced)
**Best for: Remote access, large datasets, team collaboration**

1. Upload data to secure cloud storage (S3, Google Drive, etc.)
2. Set up access credentials
3. Use setup script to configure remote access

**Pros:** Remote access, scalable, professional
**Cons:** Requires cloud setup and credentials

## Current Status Check

Run this to see what data is currently available:
```bash
python src/utils/data_source_loader.py
```

## Quick Setup Script

For interactive setup:
```bash
python scripts/setup_data_source.py
```

## File Structure After Setup

```
clausemate/
├── data/
│   ├── input/
│   │   ├── gotofiles/     # Test data (public, in git)
│   │   │   ├── 1.tsv
│   │   │   ├── 2.tsv
│   │   │   └── 3.tsv
│   │   └── private/       # Your data (private, ignored by git)
│   │       ├── your_file1.tsv
│   │       ├── your_file2.tsv
│   │       └── README.md
│   └── output/            # Results (ignored by git)
├── .env                   # Your config (ignored by git)
├── .env.example          # Template (in git)
└── scripts/
    └── setup_data_source.py
```

## Security Notes

✅ **Safe (ignored by git):**
- `data/input/private/`
- `.env` file
- Any `*.zip` files
- Any directories named `*private*` or `*secure*`

❌ **Avoid committing:**
- Real research data
- Passwords or tokens
- Personal file paths
- Sensitive configuration

## Quick Commands

```bash
# Check current data status
python src/utils/data_source_loader.py

# Set up new data source
python scripts/setup_data_source.py

# Run analysis with current data
python src/main.py

# Run multi-file analysis
python scripts/run_multi_file_analysis.py

# Run with verbose output
python src/main.py --verbose
```

## My Recommendation for You

**Start with Option 1 (Simple Local Directory):**

1. `mkdir -p data/input/private`
2. Copy your real TSV files there
3. Run `python src/main.py` - it will automatically use your private data
4. Upgrade to Option 2 (Environment Variables) later if needed

This gets you working immediately while keeping your data secure!
