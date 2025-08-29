# Data Source Configuration for ClauseMate

## Overview

The ClauseMate analyzer supports multiple data source configurations to handle both public test data and private research data securely.

## Configuration Options

### 1. Environment Variable Configuration (Recommended)

Set environment variables to specify your data source:

```bash
# Option A: Local private directory
export CLAUSEMATE_DATA_SOURCE="local"
export CLAUSEMATE_DATA_PATH="/path/to/your/private/data"

# Option B: Secure remote source
export CLAUSEMATE_DATA_SOURCE="remote"
export CLAUSEMATE_DATA_URL="https://your-secure-server.com/data"
export CLAUSEMATE_DATA_TOKEN="your-access-token"

# Option C: Cloud storage
export CLAUSEMATE_DATA_SOURCE="cloud"
export CLAUSEMATE_DATA_BUCKET="your-s3-bucket"
export CLAUSEMATE_AWS_ACCESS_KEY="your-key"
```

### 2. Data Source Priority

1. Environment variables (if set)
2. Local `data/input/private/` directory (if exists)
3. Default test data in `data/input/gotofiles/`

## Implementation

### Environment Variables Setup

Create a `.env` file (ignored by git):

```bash
# .env file (not committed to git)
CLAUSEMATE_DATA_SOURCE=local
CLAUSEMATE_DATA_PATH=/Users/yourname/Research/clausemate-data
CLAUSEMATE_RESEARCH_PASSWORD=your-research-password
```

### Programmatic Access

The analyzer automatically detects and uses the appropriate data source:

```python
# Automatic data source detection
analyzer = ClauseMateAnalyzer()  # Uses env vars or defaults
result = analyzer.analyze_directory()  # Works with any source
```

## Security Options

### Option A: Password-Protected ZIP

- Store data in encrypted ZIP file
- Program prompts for password at runtime
- Can be stored locally or downloaded

### Option B: Private Git Repository

- Create separate private repo for data
- Use git submodules or manual sync
- Full version control for data

### Option C: Secure Cloud Storage

- AWS S3 with presigned URLs
- Google Drive with API access
- Dropbox with app tokens

### Option D: Local Network Share

- Store on local network drive
- Access via mapped drives or UNC paths
- Good for institutional environments

## Recommended Workflow

1. **Development**: Use test data in `data/input/gotofiles/`
2. **Research**: Set environment variables to point to private data
3. **CI/CD**: Use test data automatically
4. **Distribution**: Include only test data in releases

## File Structure

```
clausemate/
├── data/
│   ├── input/
│   │   ├── gotofiles/          # Public test data (committed)
│   │   ├── private/            # Private data (gitignored)
│   │   └── examples/           # Sample formats (committed)
│   └── output/                 # Results (gitignored)
├── .env                        # Environment config (gitignored)
├── .env.example               # Template (committed)
└── scripts/
    └── setup_data_source.py   # Helper script
```

This approach keeps sensitive data secure while maintaining full functionality.
