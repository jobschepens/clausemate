# Project Organization

This document explains the new organized structure of the ClauseMate project.

## Directory Structure

```
clausemate/
├── 📁 config/              # Configuration files
│   ├── requirements*.txt   # Python dependencies
│   ├── requirements*.in    # Dependency source files
│   ├── .pre-commit-config.yaml
│   ├── .pylintrc
│   ├── .markdownlint.json
│   └── pytest.ini
├── 📁 docker/              # Docker & containerization
│   ├── Dockerfile          # Production container
│   ├── Dockerfile.dev      # Development container
│   ├── docker-compose.yml  # Container orchestration
│   ├── .dockerignore       # Docker ignore files
│   └── DOCKER_README.md    # Docker documentation
├── 📁 docs/                # Documentation
│   ├── project-plans/      # Planning documents
│   │   ├── updated_implementation_plan.md
│   │   ├── dockerplan.md
│   │   ├── TODO.md
│   │   └── ROADMAP.md
│   └── *.md                # Other documentation
├── 📁 src/                 # Source code
├── 📁 tests/               # Test suite
├── 📁 tools/               # Utility scripts
├── 📁 scripts/             # Analysis scripts
├── 📁 notebooks/           # Jupyter notebooks
├── 📁 data/                # Data files
└── 📁 archive/             # Historical code
```

## Quick Commands

### Development with Docker
```bash
# Start development environment
cd docker
docker-compose up clausemate-dev -d
docker exec -it clausemate-dev bash

# Start Jupyter Lab
docker-compose up clausemate-jupyter
# Access at http://localhost:8889

# Run production analysis
docker-compose up clausemate-prod
```

### Local Development
```bash
# Install dependencies
pip install -r config/requirements.txt

# Run tests
nox

# Format code
nox -s format
```

## File Moves Summary

- **Configuration files** → `config/`
- **Docker files** → `docker/`
- **Planning documents** → `docs/project-plans/`
- **Removed duplicates** → Cleaned up conflicted files and outdated notebooks

This organization makes the project root much cleaner and groups related files logically.
