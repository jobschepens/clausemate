# ClauseMate Docker Configurations

This repository provides multiple Docker configurations for different use cases:

## 🐳 Docker Files Overview

### 1. `Dockerfile` (Production)

- **Purpose**: Production deployment and CI/CD
- **Features**: Multi-stage build with testing, minimal runtime image
- **User**: `app` (non-root)
- **Command**: `python src/main.py`
- **Use Case**: Deploy ClauseMate for analysis in production environments

### 2. `Dockerfile.dev` (Development)

- **Purpose**: Local development with full tooling
- **Features**: Jupyter Lab, development packages, debugging tools
- **User**: `clausemate` (non-root with proper home directory)
- **Command**: `bash` (interactive) or Jupyter Lab
- **Use Case**: Development, research, interactive analysis

## 🚀 Quick Start

### Option 1: Docker Compose (Recommended)

```bash
# Clone the repository
git clone https://github.com/jobschepens/clausemate.git
cd clausemate

# Start development environment
docker-compose -f docker-compose.dev.yml up -d

# Access the container
docker exec -it clausemate-dev bash

# Inside container, run tests
python test_docker_setup.py
```

### Option 2: Docker Build

```bash
# Build development image
docker build -f Dockerfile.dev -t clausemate-dev .

# Run container
docker run -it --rm \
  -v $(pwd):/workspace \
  -p 8888:8888 \
  clausemate-dev bash

# Inside container
python test_docker_setup.py
```

## Development Workflow

### Running Scripts

```bash
# Multi-file analysis (now works without ModuleNotFoundError)
python scripts/run_multi_file_analysis.py --verbose

# Single file analysis
python -m src.main data/input/gotofiles/2.tsv

# Run tests
python -m pytest tests/
```

### Jupyter Development

```bash
# Start Jupyter Lab
jupyter lab --ip=0.0.0.0 --port=8888 --no-browser

# Access at: http://localhost:8888
```

## Testing Binder Functionality

### 1. Test Local Binder-like Environment

```bash
# Simulate Binder environment
docker run -it --rm \
  -v $(pwd):/workspace \
  clausemate-dev bash

# Inside container, run postBuild script
bash .binder/postBuild

# Test notebook execution
jupyter nbconvert --to notebook --execute notebooks/demo_analysis.ipynb
```

### 2. Validate Key Fixes

The following issues have been resolved:

#### ✅ ModuleNotFoundError Fix

```bash
# This now works from any directory
python scripts/run_multi_file_analysis.py --verbose
```

#### ✅ Binder Auto-Open Fix

- Updated README.md Binder badge URL
- Enhanced demo notebook with robust installation
- Improved .binder/postBuild script

#### ✅ Docker Development Environment

- Created Dockerfile.dev for development
- Added docker-compose.dev.yml for easy setup
- Included .dockerignore.dev for optimized builds

### 3. Test Results Summary

Run `python test_docker_setup.py` to verify:

- ✅ Python path setup works correctly
- ✅ Main ClauseMate imports work
- ✅ Script execution works without ModuleNotFoundError
- ✅ Config imports work (including CRITICAL_PRONOUNS)
- ✅ Data directory structure is accessible

## Troubleshooting

### Import Errors

If you encounter import errors, ensure you're running from the project root:

```bash
cd /workspace  # In Docker container
python scripts/run_multi_file_analysis.py
```

### Missing Dependencies

```bash
# Install additional packages if needed
pip install pandas matplotlib jupyter
```

### Permission Issues

```bash
# Fix permissions if needed
chown -R clausemate:clausemate /workspace
```

## File Structure

```
clausemate/
├── Dockerfile.dev              # Development Docker image
├── docker-compose.dev.yml      # Development compose setup
├── .dockerignore.dev          # Development ignore file
├── .binder/
│   └── postBuild              # Enhanced Binder setup script
├── notebooks/
│   └── demo_analysis.ipynb    # Enhanced demo notebook
├── scripts/
│   └── run_multi_file_analysis.py  # Fixed script with path handling
├── test_docker_setup.py       # Docker environment test script
└── src/
    └── config.py              # Added CRITICAL_PRONOUNS export
```

## Next Steps

1. **Test Binder**: Click the Binder badge in README.md
2. **Verify Demo**: Ensure demo_analysis.ipynb opens and runs
3. **Run Scripts**: Test multi-file analysis in Docker
4. **Development**: Use Docker for consistent development environment

## Support

- Report issues on GitHub
- Check test_docker_setup.py output for diagnostics
- Ensure Docker Desktop is running (on Windows/macOS)
