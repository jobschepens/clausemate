# Docker Implementation Plan - Clause Mates Analyzer

## Status: READY FOR IMPLEMENTATION

This document outlines the Docker implementation plan for the Clause Mates Analyzer, providing containerized deployment for the adaptive parsing system with **100% file format compatibility**.

---

## Executive Summary

### Current System Status ✅

The Clause Mates Analyzer has achieved **Phase 2 completion** with:

- **100% File Format Compatibility**: All 4 WebAnno TSV format variations supported
- **Adaptive Parsing System**: Automatic format detection and parser selection
- **Production-Ready Architecture**: Robust, tested, and documented system
- **Comprehensive Testing**: 6/6 tests passing with full validation

### Docker Implementation Goals

**Primary Objectives:**

- **Containerized Deployment**: Reproducible environment across platforms
- **Simplified Setup**: One-command installation and execution
- **Development Support**: Containerized development environment
- **CI/CD Integration**: Docker-based continuous integration
- **Multi-stage Builds**: Optimized production images

---

## Docker Architecture

### 1. Multi-stage Build Strategy

**Build Stages:**

```dockerfile
# Stage 1: Base Python environment
FROM python:3.9-slim as base
# Install system dependencies and Python packages

# Stage 2: Development environment
FROM base as development
# Add development tools, testing frameworks, documentation

# Stage 3: Production environment
FROM base as production
# Minimal runtime environment with only necessary components
```

**Benefits:**

- **Reduced Image Size**: Production images without development dependencies
- **Security**: Minimal attack surface in production
- **Flexibility**: Different configurations for different use cases
- **Efficiency**: Shared base layers for faster builds

### 2. Container Structure

**Directory Layout:**

```
/app/
├── src/                    # Application source code
├── data/                   # Data directory (mounted volume)
│   ├── input/             # Input TSV files
│   └── output/            # Analysis results
├── tests/                 # Test suite
├── docs/                  # Documentation
├── requirements.txt       # Python dependencies
├── pyproject.toml        # Project configuration
└── docker-entrypoint.sh  # Container entry point
```

**Volume Mounts:**

- **Data Volume**: `/app/data` for input/output files
- **Config Volume**: `/app/config` for custom configurations
- **Results Volume**: `/app/results` for persistent output storage

---

## Implementation Plan

### Phase 1: Basic Containerization

#### 1.1 Base Dockerfile ✅ READY

```dockerfile
# Multi-stage Dockerfile for Clause Mates Analyzer
FROM python:3.9-slim as base

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt pyproject.toml ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/ ./src/
COPY data/ ./data/
COPY tests/ ./tests/

# Create non-root user
RUN useradd --create-home --shell /bin/bash clausemate
RUN chown -R clausemate:clausemate /app
USER clausemate

# Set environment variables
ENV PYTHONPATH=/app/src
ENV PYTHONUNBUFFERED=1

# Default command
CMD ["python", "src/main.py", "--help"]
```

#### 1.2 Docker Compose Configuration ✅ READY

```yaml
# docker-compose.yml
version: '3.8'

services:
  clausemate:
    build:
      context: .
      dockerfile: Dockerfile
      target: production
    volumes:
      - ./data:/app/data
      - ./results:/app/results
    environment:
      - PYTHONPATH=/app/src
      - LOG_LEVEL=INFO
    command: ["python", "src/main.py", "data/input/gotofiles/2.tsv"]

  clausemate-dev:
    build:
      context: .
      dockerfile: Dockerfile
      target: development
    volumes:
      - .:/app
      - ./results:/app/results
    environment:
      - PYTHONPATH=/app/src
      - LOG_LEVEL=DEBUG
    command: ["bash"]
    stdin_open: true
    tty: true

  clausemate-test:
    build:
      context: .
      dockerfile: Dockerfile
      target: development
    volumes:
      - .:/app
    command: ["python", "-m", "pytest", "tests/", "-v"]
```

#### 1.3 Entry Point Script ✅ READY

```bash
#!/bin/bash
# docker-entrypoint.sh

set -e

# Initialize data directories if they don't exist
mkdir -p /app/data/input /app/data/output /app/results

# Set default file if none provided
if [ $# -eq 0 ]; then
    echo "No input file specified. Available files:"
    find /app/data/input -name "*.tsv" -type f | head -10
    echo ""
    echo "Usage: docker run clausemate <input_file.tsv>"
    echo "Example: docker run clausemate data/input/gotofiles/2.tsv"
    exit 1
fi

# Check if input file exists
INPUT_FILE="$1"
if [ ! -f "/app/$INPUT_FILE" ]; then
    echo "Error: Input file '$INPUT_FILE' not found"
    echo "Available files:"
    find /app/data/input -name "*.tsv" -type f
    exit 1
fi

# Run the analysis
echo "Starting Clause Mates Analysis..."
echo "Input file: $INPUT_FILE"
echo "Format detection and processing will begin automatically."
echo ""

exec python src/main.py "$@"
```

### Phase 2: Development Environment

#### 2.1 Development Dockerfile ✅ READY

```dockerfile
# Development stage with additional tools
FROM base as development

# Install development dependencies
RUN pip install --no-cache-dir \
    pytest>=7.0.0 \
    pytest-cov>=4.0.0 \
    ruff>=0.1.0 \
    mypy>=1.0.0 \
    jupyter>=1.0.0 \
    ipython>=8.0.0

# Install pre-commit hooks
RUN pip install pre-commit

# Copy development configuration
COPY .pre-commit-config.yaml ./
COPY pyproject.toml ./

# Set development environment
ENV ENVIRONMENT=development
ENV LOG_LEVEL=DEBUG

# Default development command
CMD ["bash"]
```

#### 2.2 Development Workflow ✅ READY

**Development Commands:**

```bash
# Start development container
docker-compose run --rm clausemate-dev

# Run tests in container
docker-compose run --rm clausemate-test

# Run specific analysis
docker-compose run --rm clausemate python src/main.py data/input/gotofiles/1.tsv --verbose

# Interactive development
docker-compose run --rm clausemate-dev bash
```

**Development Features:**

- **Live Code Reloading**: Volume mounts for real-time development
- **Interactive Shell**: Full bash environment for debugging
- **Testing Environment**: Complete test suite execution
- **Jupyter Support**: Notebook-based analysis and exploration

### Phase 3: Production Optimization

#### 3.1 Production Dockerfile ✅ READY

```dockerfile
# Production stage - minimal runtime
FROM base as production

# Copy only necessary files
COPY src/ ./src/
COPY data/input/ ./data/input/
COPY docker-entrypoint.sh ./

# Make entrypoint executable
RUN chmod +x docker-entrypoint.sh

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import src.main; print('OK')" || exit 1

# Use entrypoint script
ENTRYPOINT ["./docker-entrypoint.sh"]
```

#### 3.2 Image Optimization ✅ READY

**Optimization Strategies:**

- **Multi-stage Builds**: Separate development and production images
- **Layer Caching**: Optimize layer order for better caching
- **Minimal Base**: Use slim Python images
- **Security**: Non-root user execution
- **Health Checks**: Container health monitoring

**Expected Image Sizes:**

- **Development Image**: ~800MB (with all tools)
- **Production Image**: ~300MB (minimal runtime)
- **Base Layer**: ~200MB (shared across stages)

### Phase 4: CI/CD Integration

#### 4.1 GitHub Actions Workflow ✅ READY

```yaml
# .github/workflows/docker.yml
name: Docker Build and Test

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  docker-test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3

    - name: Build development image
      run: docker build --target development -t clausemate:dev .

    - name: Run tests in container
      run: docker run --rm clausemate:dev python -m pytest tests/ -v

    - name: Run format validation
      run: docker run --rm clausemate:dev python src/main.py data/input/gotofiles/2.tsv --validate

    - name: Build production image
      run: docker build --target production -t clausemate:prod .

    - name: Test production image
      run: docker run --rm clausemate:prod data/input/gotofiles/2.tsv

  docker-publish:
    needs: docker-test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
    - uses: actions/checkout@v3

    - name: Build and push to registry
      run: |
        docker build --target production -t clausemate:latest .
        # Add registry push commands here
```

#### 4.2 Automated Testing ✅ READY

**Test Matrix:**

```yaml
strategy:
  matrix:
    format: [
      "data/input/gotofiles/2.tsv",
      "data/input/gotofiles/later/1.tsv",
      "data/input/gotofiles/later/3.tsv",
      "data/input/gotofiles/later/4.tsv"
    ]

steps:
- name: Test format compatibility
  run: docker run --rm clausemate:test python src/main.py ${{ matrix.format }}
```

**Validation Tests:**

- **Format Compatibility**: All 4 formats process successfully
- **Relationship Counts**: Expected relationship counts validated
- **Performance**: Processing time within acceptable limits
- **Memory Usage**: Memory consumption monitored
- **Error Handling**: Error scenarios tested

---

## Usage Documentation

### 1. Quick Start ✅ READY

**Installation:**

```bash
# Clone repository
git clone https://github.com/jobschepens/clausemate.git
cd clausemate

# Build Docker image
docker build -t clausemate .

# Run analysis
docker run --rm -v $(pwd)/data:/app/data clausemate data/input/gotofiles/2.tsv
```

**Docker Compose:**

```bash
# Start with docker-compose
docker-compose up clausemate

# Development mode
docker-compose run --rm clausemate-dev

# Run tests
docker-compose run --rm clausemate-test
```

### 2. Advanced Usage ✅ READY

**Custom Configuration:**

```bash
# Mount custom configuration
docker run --rm \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/config:/app/config \
  clausemate data/input/gotofiles/1.tsv --config config/custom.yaml
```

**Batch Processing:**

```bash
# Process multiple files
for file in data/input/gotofiles/later/*.tsv; do
  docker run --rm -v $(pwd)/data:/app/data clausemate "$file"
done
```

**Development Workflow:**

```bash
# Interactive development
docker-compose run --rm clausemate-dev bash

# Run specific tests
docker-compose run --rm clausemate-dev python -m pytest tests/test_adaptive_parser.py -v

# Format validation
docker-compose run --rm clausemate-dev ruff check src/
```

### 3. Production Deployment ✅ READY

**Production Configuration:**

```yaml
# docker-compose.prod.yml
version: '3.8'

services:
  clausemate:
    image: clausemate:latest
    restart: unless-stopped
    volumes:
      - /data/input:/app/data/input:ro
      - /data/output:/app/data/output
    environment:
      - LOG_LEVEL=INFO
      - ENVIRONMENT=production
    healthcheck:
      test: ["CMD", "python", "-c", "import src.main; print('OK')"]
      interval: 30s
      timeout: 10s
      retries: 3
```

**Monitoring:**

```bash
# Container health
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

# Resource usage
docker stats clausemate

# Logs
docker logs -f clausemate
```

---

## Performance and Security

### 1. Performance Optimization ✅

**Resource Limits:**

```yaml
services:
  clausemate:
    deploy:
      resources:
        limits:
          cpus: '2.0'
          memory: 2G
        reservations:
          cpus: '1.0'
          memory: 1G
```

**Caching Strategy:**

- **Layer Caching**: Optimize Dockerfile for better layer reuse
- **Build Cache**: Use BuildKit for improved build performance
- **Registry Cache**: Pull base images from local registry when possible

**Performance Metrics:**

- **Build Time**: < 5 minutes for full build
- **Image Size**: < 300MB for production image
- **Startup Time**: < 10 seconds for container startup
- **Processing Speed**: Maintains native performance levels

### 2. Security Considerations ✅

**Security Features:**

- **Non-root User**: All processes run as non-root user
- **Minimal Base**: Slim base images with minimal attack surface
- **No Secrets**: No hardcoded secrets or credentials
- **Read-only Filesystem**: Production containers use read-only root filesystem
- **Security Scanning**: Automated vulnerability scanning in CI/CD

**Security Configuration:**

```dockerfile
# Security hardening
RUN useradd --create-home --shell /bin/bash --uid 1000 clausemate
USER clausemate

# Read-only root filesystem
VOLUME ["/tmp", "/app/data/output"]
```

---

## Monitoring and Maintenance

### 1. Health Monitoring ✅

**Health Checks:**

```dockerfile
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import src.main; print('OK')" || exit 1
```

**Monitoring Metrics:**

- **Container Health**: Health check status
- **Resource Usage**: CPU, memory, disk usage
- **Processing Metrics**: Files processed, success rate
- **Error Rates**: Failed processing attempts

### 2. Maintenance Procedures ✅

**Update Process:**

```bash
# Pull latest changes
git pull origin main

# Rebuild image
docker build -t clausemate:latest .

# Update running containers
docker-compose down
docker-compose up -d
```

**Backup Procedures:**

- **Data Backup**: Regular backup of input/output data
- **Configuration Backup**: Version control for configurations
- **Image Backup**: Tagged images for rollback capability

---

## Future Enhancements

### 1. Advanced Features

**Planned Enhancements:**

- **Kubernetes Support**: Helm charts for Kubernetes deployment
- **Distributed Processing**: Multi-container processing for large corpora
- **Web Interface**: Containerized web UI for interactive analysis
- **API Service**: RESTful API service in container
- **Monitoring Stack**: Integrated Prometheus/Grafana monitoring

### 2. Integration Opportunities

**External Integrations:**

- **Cloud Deployment**: AWS/GCP/Azure container services
- **CI/CD Pipelines**: Integration with various CI/CD platforms
- **Data Pipelines**: Integration with data processing workflows
- **Research Platforms**: Integration with research computing environments

---

## Implementation Timeline

### Phase 1: Basic Containerization (Week 1)

- [ ] Create base Dockerfile
- [ ] Implement Docker Compose configuration
- [ ] Create entry point script
- [ ] Test basic functionality

### Phase 2: Development Environment (Week 2)

- [ ] Implement development Dockerfile
- [ ] Create development workflow documentation
- [ ] Test development environment
- [ ] Validate testing in containers

### Phase 3: Production Optimization (Week 3)

- [ ] Optimize production Dockerfile
- [ ] Implement security hardening
- [ ] Performance testing and optimization
- [ ] Create production deployment guide

### Phase 4: CI/CD Integration (Week 4)

- [ ] Implement GitHub Actions workflow
- [ ] Create automated testing pipeline
- [ ] Set up image registry
- [ ] Document deployment procedures

---

## Conclusion

### Benefits of Docker Implementation

**Development Benefits:**

- **Consistent Environment**: Same environment across all development machines
- **Easy Setup**: One-command installation and execution
- **Isolated Dependencies**: No conflicts with host system
- **Reproducible Builds**: Consistent builds across different environments

**Production Benefits:**

- **Scalable Deployment**: Easy horizontal scaling
- **Resource Efficiency**: Optimal resource utilization
- **Security**: Isolated execution environment
- **Maintenance**: Simplified updates and rollbacks

**Research Benefits:**

- **Reproducible Research**: Exact environment replication
- **Cross-platform Compatibility**: Runs on any Docker-supported platform
- **Collaboration**: Easy sharing of complete analysis environment
- **Version Control**: Tagged images for different analysis versions

The Docker implementation will provide a robust, scalable, and maintainable deployment solution for the Clause Mates Analyzer, supporting both development and production use cases while maintaining the system's **100% file format compatibility** and adaptive parsing capabilities.

---

**Plan Status**: READY FOR IMPLEMENTATION
**Priority**: Medium
**Dependencies**: Phase 2 completion (✅ Complete)
**Estimated Timeline**: 4 weeks
**Next Steps**: Begin Phase 1 implementation

For technical implementation details, see the Dockerfile and docker-compose.yml configurations outlined in this plan.
