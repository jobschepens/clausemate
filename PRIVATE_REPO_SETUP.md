# Private GitHub Repository Setup for ClauseMate Data

## Overview

This guide helps you create a private GitHub repository for your research data while keeping it integrated with the public ClauseMate analyzer.

## Method 1: Git Submodule (Recommended)

### Step 1: Create Private Repository

1. Go to GitHub and create a new **private** repository
   - Name: `clausemate-private-data` (or your preferred name)
   - Visibility: **Private**
   - Initialize with README

### Step 2: Set Up Local Private Data Repository

```bash
# Navigate to your private data directory
cd data/input/private

# Initialize git repository
git init

# Add remote (replace with your private repo URL)
git remote add origin https://github.com/yourusername/clausemate-private-data.git

# Create initial commit
echo "# ClauseMate Private Research Data" > README.md
git add .
git commit -m "Initial commit with research data"

# Push to private repository
git push -u origin main
```

### Step 3: Add as Submodule to Main Repository

```bash
# From the clausemate root directory
cd /path/to/clausemate

# Remove existing private directory
rm -rf data/input/private

# Add as submodule
git submodule add https://github.com/yourusername/clausemate-private-data.git data/input/private

# Commit the submodule reference
git add .gitmodules data/input/private
git commit -m "Add private data as submodule"
```

### Step 4: Update .gitignore for Submodule

The submodule reference will be tracked, but the actual data stays private.

## Method 2: Separate Repository with Symbolic Link

### Step 1: Create Private Repository (Same as Method 1)

### Step 2: Clone Private Repository Separately

```bash
# Clone to a separate location
cd /path/to/your/research
git clone https://github.com/yourusername/clausemate-private-data.git

# Create symbolic link in ClauseMate
cd /path/to/clausemate
rm -rf data/input/private
ln -s /path/to/your/research/clausemate-private-data data/input/private
```

## Method 3: Environment Variable with Private Repository

### Update .env Configuration

```bash
# In your .env file
CLAUSEMATE_DATA_SOURCE=git_repository
CLAUSEMATE_DATA_REPO=https://github.com/yourusername/clausemate-private-data.git
CLAUSEMATE_DATA_BRANCH=main
CLAUSEMATE_LOCAL_PATH=data/input/private
```

## Recommended Workflow

### For Development

```bash
# Update private data
cd data/input/private
git pull origin main

# Make changes to your data
# ... edit TSV files ...

# Commit changes
git add .
git commit -m "Update research data"
git push origin main

# Update main ClauseMate repository
cd ../../..
git add data/input/private  # Updates submodule reference
git commit -m "Update private data reference"
```

### For Collaboration

```bash
# When others clone the main repository
git clone https://github.com/jobschepens/clausemate.git
cd clausemate

# Initialize and update submodules
git submodule init
git submodule update

# Or in one command
git clone --recurse-submodules https://github.com/jobschepens/clausemate.git
```

## Security Benefits

✅ **Private data stays private** - Only accessible to authorized users
✅ **Version control** - Full git history for your research data
✅ **Backup** - Data is backed up to GitHub
✅ **Collaboration** - Share with specific collaborators
✅ **Public repo stays clean** - No private data leaks

## File Structure After Setup

```
clausemate/
├── data/
│   ├── input/
│   │   ├── gotofiles/     # Public test data
│   │   └── private/       # Submodule → private repository
│   │       ├── .git/      # Private repo git data
│   │       ├── README.md
│   │       ├── 1.tsv
│   │       ├── 2.tsv
│   │       └── later/
│   │           ├── 3.tsv
│   │           └── 4.tsv
│   └── output/
├── .gitmodules           # Submodule configuration
└── ...
```

## Quick Commands

```bash
# Update private data
cd data/input/private && git pull

# Commit changes to private data
cd data/input/private
git add . && git commit -m "Update data" && git push

# Update submodule reference in main repo
git add data/input/private && git commit -m "Update data reference"

# Check submodule status
git submodule status
```

## Access Control

### Private Repository Settings

1. Go to your private repository settings
2. **Manage access** → **Invite collaborators**
3. Add team members with appropriate permissions:
   - **Read**: View and clone only
   - **Write**: Can push changes
   - **Admin**: Full control

## Backup Strategy

Your data is now protected with:

- **Local git history** (in `data/input/private/.git/`)
- **GitHub backup** (private repository)
- **Submodule reference** (in main ClauseMate repository)
- **Multiple clone locations** (team members' machines)

## Next Steps

1. **Choose your method** (Git Submodule recommended)
2. **Create private GitHub repository**
3. **Set up local integration**
4. **Test the workflow**
5. **Share access with collaborators**

This gives you professional-grade version control for your research data while maintaining security!
