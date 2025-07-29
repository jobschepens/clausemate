# Data Directory Structure

This directory contains the input and output data for the clausemate analysis tool.

## Directory Structure

```
data/
├── input/           # Input data files (not included in repository)
│   ├── FORMAT_OVERVIEW.md          # Documentation of supported formats
│   ├── gotofiles/                  # Standard format files
│   │   ├── 2.tsv                   # Standard format (15 columns) - NOT IN REPO
│   │   └── 2.tsv_DOCUMENTATION.md  # Format documentation
│   └── later/                      # Alternative format files
│       ├── 1.tsv                   # Extended format (37 columns) - NOT IN REPO
│       ├── 3.tsv                   # Legacy format (14 columns) - NOT IN REPO
│       ├── 4.tsv                   # Incomplete format (12 columns) - NOT IN REPO
│       ├── 1.tsv_DOCUMENTATION.md  # Extended format documentation
│       ├── 3.tsv_DOCUMENTATION.md  # Legacy format documentation
│       └── 4.tsv_DOCUMENTATION.md  # Incomplete format documentation
└── output/          # Generated analysis results (not included in repository)
    └── .gitkeep     # Keeps directory structure
```

## Data Privacy

**Important**: The actual data files (`.tsv` files) are **NOT included** in this repository for privacy reasons. The repository only contains:

- Format documentation files (`*_DOCUMENTATION.md`)
- Format overview (`FORMAT_OVERVIEW.md`)
- Directory structure (`.gitkeep` files)

## For Users

If you want to use this tool with your own data:

1. **Input Data**: Place your WebAnno TSV 3.3 format files in the appropriate directories:
   - `data/input/gotofiles/` for standard format files
   - `data/input/gotofiles/later/` for alternative format files

2. **Output Data**: Analysis results will be generated in `data/output/` with timestamped directories

3. **Supported Formats**: See [`FORMAT_OVERVIEW.md`](input/FORMAT_OVERVIEW.md) for detailed format specifications

## Format Support

The tool supports multiple WebAnno TSV 3.3 format variations:

| Format | Columns | Description | Location |
|--------|---------|-------------|----------|
| Standard | 15 | Basic linguistic annotations | `gotofiles/2.tsv` |
| Extended | 37 | Rich morphological features | `later/1.tsv` |
| Legacy | 14 | Compact annotation set | `later/3.tsv` |
| Incomplete | 12 | Limited annotations | `later/4.tsv` |

## Getting Started

1. Install the package: `pip install clausemate`
2. Place your TSV files in the appropriate input directories
3. Run analysis: `clausemate your-file.tsv`
4. Check results in `data/output/`

For more information, see the main [README.md](../README.md) and [documentation](../docs/).
