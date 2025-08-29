# Set Up Private Repository for Your Research Data

## Current Situation

Your private data is currently in the main ClauseMate repository. We need to create a separate private repository for security and organization.

## Step-by-Step Instructions

### 1. Create Private GitHub Repository

1. Go to GitHub.com and log in
2. Click "New repository"
3. Name: `clausemate-private-data` (or your choice)
4. **Make it PRIVATE** ✅
5. Initialize with README
6. Click "Create repository"

### 2. Backup Your Current Data

```powershell
# From the clausemate root directory
cd data\input
cp -r private private_backup
```

### 3. Set Up Private Repository Locally

```powershell
# Clone your new private repository
cd C:\GitHub  # or your preferred location
git clone https://github.com/yourusername/clausemate-private-data.git

# Copy your data to the private repository
cd clausemate-private-data
cp -r ..\clausemate\data\input\private\* .

# Commit your data
git add .
git commit -m "Initial commit: Add research data"
git push origin main
```

### 4. Set Up as Git Submodule (Option A - Recommended)

```powershell
# From clausemate root directory
cd C:\GitHub\clausemate

# Remove the current private directory
rm -rf data\input\private

# Add private repository as submodule
git submodule add https://github.com/yourusername/clausemate-private-data.git data/input/private

# Commit the submodule
git add .gitmodules data\input\private
git commit -m "Add private data as submodule"
git push origin main
```

### 5. Alternative: Symbolic Link (Option B)

```powershell
# From clausemate root directory
rm -rf data\input\private

# Create symbolic link (Windows - requires admin privileges)
New-Item -ItemType SymbolicLink -Path "data\input\private" -Target "C:\GitHub\clausemate-private-data"

# Or use junction (no admin required)
cmd /c mklink /J "data\input\private" "C:\GitHub\clausemate-private-data"
```

## Benefits of This Setup

✅ **Version Control**: Full git history for your research data
✅ **Private & Secure**: Only you (and collaborators you invite) can access it
✅ **Backup**: Data backed up to GitHub
✅ **Clean Separation**: Private data never gets committed to public repo
✅ **Team Collaboration**: Invite colleagues to private repo only
✅ **Professional Workflow**: Standard practice for research projects

## Daily Workflow

### Updating Your Data

```powershell
# Go to private data directory
cd data\input\private

# Pull latest changes (if working with team)
git pull origin main

# Make your changes to TSV files
# ... edit files ...

# Commit changes
git add .
git commit -m "Update research data: describe changes"
git push origin main
```

### Running Analysis

```powershell
# From clausemate root - works exactly the same!
python src\main.py data\input\private\2.tsv
python scripts\run_multi_file_analysis.py --input data\input\private\
```

### Updating Submodule Reference (if using Option A)

```powershell
# After updating private data, update the main repository reference
git add data\input\private
git commit -m "Update private data reference"
git push origin main
```

## Security Notes

🔒 **Your private repository**:

- Only accessible to people you invite
- Never referenced in public ClauseMate repo
- Full version control and backup

🔓 **Public ClauseMate repository**:

- Contains only the analysis code
- No private data ever committed
- Clean and shareable

## Team Collaboration

To share with colleagues:

1. Invite them to your private repository
2. They clone both repositories:

   ```powershell
   git clone https://github.com/jobschepens/clausemate.git
   git clone https://github.com/yourusername/clausemate-private-data.git
   # Create symbolic link as in step 5
   ```

## Next Steps

1. ✅ **Create private GitHub repository**
2. ✅ **Copy your data there**
3. ✅ **Choose setup method** (submodule recommended)
4. ✅ **Test the workflow**
5. ✅ **Invite collaborators if needed**

This gives you professional-grade data management! 🚀
